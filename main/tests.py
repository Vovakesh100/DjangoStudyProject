from django.test import TestCase
from django.urls import reverse


class PageTests(TestCase):
    """Tests for the two public pages.

    Requests use secure=True so they pass when SECURE_SSL_REDIRECT is on.
    """

    def get(self, name):
        return self.client.get(reverse(name), secure=True)

    def test_index_returns_200_with_heading(self):
        response = self.get('index')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>1 lesson</h1>', html=True)

    def test_new_returns_200_with_heading(self):
        response = self.get('new')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h4>2 page of site</h4>', html=True)

    def test_pages_do_not_require_login(self):
        for name in ('index', 'new'):
            with self.subTest(page=name):
                response = self.get(name)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_pages_use_expected_templates(self):
        self.assertTemplateUsed(self.get('index'), 'main/index.html')
        self.assertTemplateUsed(self.get('new'), 'main/new.html')
