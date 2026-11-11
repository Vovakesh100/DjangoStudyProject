"""Tests for the security settings in ZeroCoder/settings.py.

Settings are read when the module is imported, so each case runs in a fresh
subprocess with an explicit, clean environment. Nothing here disables a
security setting.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_KEY = 'test-only-key-not-a-real-secret-0123456789'

SETTINGS_SCRIPT = """
import json
from django.conf import settings
names = [
    'DEBUG', 'ALLOWED_HOSTS', 'SECURE_SSL_REDIRECT', 'SESSION_COOKIE_SECURE',
    'CSRF_COOKIE_SECURE', 'SECURE_HSTS_SECONDS',
    'SECURE_HSTS_INCLUDE_SUBDOMAINS', 'SECURE_CONTENT_TYPE_NOSNIFF',
    'SECURE_REFERRER_POLICY', 'X_FRAME_OPTIONS',
]
data = {n: getattr(settings, n) for n in names}
data['validators'] = len(settings.AUTH_PASSWORD_VALIDATORS)
print(json.dumps(data))
"""

REQUEST_SCRIPT = """
import json
import django
django.setup()
from django.test import Client
client = Client(SERVER_NAME='localhost')
plain = client.get('/')
secure = client.get('/', secure=True)
print(json.dumps({
    'plain_status': plain.status_code,
    'plain_location': plain.headers.get('Location', ''),
    'secure_status': secure.status_code,
    'headers': dict(secure.headers),
}))
"""


def run_python(script, **env_vars):
    """Run a script with Django settings and only the given variables."""
    env = {
        'PATH': os.environ.get('PATH', ''),
        'PYTHONPATH': str(BASE_DIR),
        'DJANGO_SETTINGS_MODULE': 'ZeroCoder.settings',
    }
    env.update(env_vars)
    return subprocess.run(
        [sys.executable, '-c', 'import django; django.setup()\n' + script],
        check=False,
        cwd=BASE_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def load_settings(**env_vars):
    result = run_python(SETTINGS_SCRIPT, **env_vars)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


class StartupFailureTests(SimpleTestCase):
    def test_missing_secret_key_fails(self):
        result = run_python(
            'pass',
            DJANGO_DEBUG='1',
            DJANGO_ALLOWED_HOSTS='localhost',
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ImproperlyConfigured', result.stderr)
        self.assertIn('DJANGO_SECRET_KEY', result.stderr)

    def test_empty_secret_key_fails(self):
        result = run_python(
            'pass',
            DJANGO_SECRET_KEY='',
            DJANGO_DEBUG='1',
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DJANGO_SECRET_KEY', result.stderr)

    def test_missing_allowed_hosts_with_debug_off_fails(self):
        result = run_python('pass', DJANGO_SECRET_KEY=TEST_KEY)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ImproperlyConfigured', result.stderr)
        self.assertIn('DJANGO_ALLOWED_HOSTS', result.stderr)

    def test_blank_allowed_hosts_with_debug_off_fails(self):
        result = run_python(
            'pass',
            DJANGO_SECRET_KEY=TEST_KEY,
            DJANGO_ALLOWED_HOSTS=' , ',
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DJANGO_ALLOWED_HOSTS', result.stderr)

    def test_missing_allowed_hosts_with_debug_on_starts(self):
        data = load_settings(DJANGO_SECRET_KEY=TEST_KEY, DJANGO_DEBUG='1')
        self.assertTrue(data['DEBUG'])


class DebugFlagTests(SimpleTestCase):
    def test_debug_off_by_default(self):
        data = load_settings(
            DJANGO_SECRET_KEY=TEST_KEY,
            DJANGO_ALLOWED_HOSTS='localhost',
        )
        self.assertIs(data['DEBUG'], False)

    def test_debug_only_on_for_exactly_one(self):
        for value in ('true', 'True', 'yes', '0', '11', ' 1', ''):
            with self.subTest(value=value):
                data = load_settings(
                    DJANGO_SECRET_KEY=TEST_KEY,
                    DJANGO_ALLOWED_HOSTS='localhost',
                    DJANGO_DEBUG=value,
                )
                self.assertIs(data['DEBUG'], False)

    def test_debug_on_for_exactly_one(self):
        data = load_settings(
            DJANGO_SECRET_KEY=TEST_KEY,
            DJANGO_ALLOWED_HOSTS='localhost',
            DJANGO_DEBUG='1',
        )
        self.assertIs(data['DEBUG'], True)


class ProductionSettingsTests(SimpleTestCase):
    def setUp(self):
        self.data = load_settings(
            DJANGO_SECRET_KEY=TEST_KEY,
            DJANGO_ALLOWED_HOSTS='example.test, www.example.test',
            DJANGO_DEBUG='0',
        )

    def test_allowed_hosts_come_from_environment(self):
        self.assertEqual(
            self.data['ALLOWED_HOSTS'], ['example.test', 'www.example.test']
        )

    def test_security_settings_enabled(self):
        self.assertIs(self.data['SECURE_SSL_REDIRECT'], True)
        self.assertIs(self.data['SESSION_COOKIE_SECURE'], True)
        self.assertIs(self.data['CSRF_COOKIE_SECURE'], True)
        self.assertEqual(self.data['SECURE_HSTS_SECONDS'], 3600)
        self.assertIs(self.data['SECURE_HSTS_INCLUDE_SUBDOMAINS'], True)
        self.assertIs(self.data['SECURE_CONTENT_TYPE_NOSNIFF'], True)
        self.assertEqual(self.data['SECURE_REFERRER_POLICY'], 'same-origin')
        self.assertEqual(self.data['X_FRAME_OPTIONS'], 'DENY')

    def test_four_password_validators_kept(self):
        self.assertEqual(self.data['validators'], 4)


class ProductionHeadersTests(SimpleTestCase):
    def setUp(self):
        result = run_python(
            REQUEST_SCRIPT,
            DJANGO_SECRET_KEY=TEST_KEY,
            DJANGO_ALLOWED_HOSTS='localhost',
            DJANGO_DEBUG='0',
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.data = json.loads(result.stdout.strip().splitlines()[-1])
        self.headers = {k.lower(): v for k, v in self.data['headers'].items()}

    def test_http_request_is_redirected_to_https(self):
        self.assertEqual(self.data['plain_status'], 301)
        self.assertTrue(self.data['plain_location'].startswith('https://'))

    def test_https_response_has_security_headers(self):
        self.assertEqual(self.data['secure_status'], 200)
        self.assertEqual(
            self.headers['strict-transport-security'],
            'max-age=3600; includeSubDomains',
        )
        self.assertEqual(self.headers['x-content-type-options'], 'nosniff')
        self.assertEqual(self.headers['referrer-policy'], 'same-origin')
        self.assertEqual(self.headers['x-frame-options'], 'DENY')
