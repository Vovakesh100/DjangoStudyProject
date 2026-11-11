# DjangoStudyProject

A learning project in Django 6.0 that shows practical Django skills. The target is a small social network (accounts, profiles, posts, feed, comments, likes, friends). Currently there is one app, `main`, with two pages. All data is synthetic.

Rules for contributors and AI agents are in `CLAUDE.md`; the task list is in `docs/TASKS.md`.

## Environment variables

The project does not start without `DJANGO_SECRET_KEY`. Names only are listed in `.env.example`.

| Variable | Meaning |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required. No default. Generate one: `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DJANGO_DEBUG` | Debug mode is on only when this is exactly `1`. Anything else, or unset, means off. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host names. Required when debug is off; the project refuses to start with an empty list. |

With debug off, the project redirects HTTP to HTTPS, sets secure cookies, HSTS (3600 seconds, with subdomains), `nosniff`, `Referrer-Policy: same-origin` and `X-Frame-Options: DENY`.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then fill in the values; .env is git-ignored
set -a; source .env; set +a   # load the variables into the shell
python manage.py migrate
python manage.py runserver
```

For local development set `DJANGO_DEBUG=1` and `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1` in `.env`. Open http://127.0.0.1:8000/

## Checks

Load `.env` first (see above), then:

```bash
python manage.py makemigrations --check --dry-run
python manage.py test
ruff check .
DJANGO_DEBUG=0 DJANGO_ALLOWED_HOSTS=localhost python manage.py check --deploy
```

`ruff` is a development-only tool: `pip install ruff`.

`check --deploy` reports one warning, `security.W021` (`SECURE_HSTS_PRELOAD`). The preload list needs a long HSTS period that `CLAUDE.md` does not allow without the owner's agreement, so the warning is expected for now.
