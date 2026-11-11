# CLAUDE.md: DjangoStudyProject

Instructions for AI agents working in this repository. Read this file, `README.md` and `docs/TASKS.md` before changing anything.

## Purpose

A learning project that shows practical Django skills. The target is a small social network in the spirit of Facebook: user accounts, profiles, posts, a feed, comments, likes and friends. The goal is to demonstrate correct, secure and well-tested Django code, not to run a production service.

Portfolio demo: synthetic data only. No real people, no real personal data, no real photos of people.

## Current state

- Django 6.0.2 (`requirements.txt`), Python 3.12.
- One app, `main`, with two template pages (`/` and `/new`) on a shared layout and a navigation include.
- No models yet. `main/tests.py` is empty.
- Known issues to fix first: `DEBUG` and the secret key have insecure defaults (see Security), the layout has two `<title>` elements, and `views.py` has an unused import.

The order of features is defined by the Tech Lead in `docs/TASKS.md`. Do not start a feature that is not in that file.

## Roles

Five roles. The Tech Lead receives the work from the owner, distributes it and handles every question. Other roles report to the Tech Lead.

### 1. Tech Lead
- Receives requests from the owner and turns them into items in `docs/TASKS.md`. Each item has an ID, a goal, acceptance criteria and a branch name.
- Assigns one item at a time to a Developer. Decides on architecture: models, URL layout, app structure, template structure.
- Reviews every PR against this file and the acceptance criteria before merging. Merges only when all checks pass.
- Records open questions in `docs/OPEN-QUESTIONS.md`. Answers them itself when the answer is in these instructions or the TZ; otherwise escalates to the owner (see "Stop and ask").
- Creates any materials the project needs: text, copy, sample posts and usernames, asset plans, links. See "Materials".

### 2. Developer
- Implements exactly one item from `docs/TASKS.md` in a branch `task/<id>-<slug>`.
- Writes the code and the tests for that item. Keeps commits small, one logical step per commit.
- Does not change CSS or unrelated templates unless the item says so.
- Updates `README.md` when behaviour or setup changes.
- Before asking for review, runs all checks in "Workflow" and reports the result.

### 3. Tester
- Verifies the item independently from the Developer. Does not edit application code.
- Checks each acceptance criterion against tests or a documented manual check.
- Writes tests for routes, templates, forms and access rules when the Developer has not.
- Runs the security checks in "Security" and the dependency audit.
- Reports `pass` or `fail` for each criterion, with the exact command output for every failure.

### 4. Designer
- Owns the visual layer: `main/static/main/css/main.css`, static images and template class names.
- Takes visual references from Figma through the connected Figma connector when it is available. If it is not available, writes the design decisions in `docs/DESIGN.md` (colours, type scale, spacing, components, breakpoints) so the Developer can follow them.
- Does not change Python code, models, views or URLs. Template markup changes need the Developer or Tech Lead.
- Keeps the design accessible: text contrast of at least 4.5:1, visible focus states, `alt` text on every meaningful image, no information carried by colour alone.
- Replaces the current pink background with the agreed design in one dedicated PR.

### 5. User (feedback)
- Not a code role. Uses the site in a browser by the scenarios listed in `docs/SCENARIOS.md`.
- Records every problem in `docs/FEEDBACK.md`: an ID, the page, the steps, the expected result, the actual result, and a screenshot path if one is available.
- Does not edit code or docs other than `docs/FEEDBACK.md`.
- The Tech Lead turns feedback into tasks or closes it with a reason.

## Workflow

- One task per branch named `task/<id>-<slug>`, one PR per task. Each PR links to its item in `docs/TASKS.md`.
- Never push to `main`. Open a PR, and merge it only after every check passes.
- Before a PR is ready, these commands must pass with no errors:
  - `python manage.py check --deploy` with the production variables set (see Security)
  - `python manage.py makemigrations --check --dry-run`
  - `python manage.py test`
  - `ruff check .`
- When a task is complete, the Tech Lead marks it `done` in `docs/TASKS.md` in the same PR.
- Commit messages and identifiers are in English. Documentation is in English.

## Security (mandatory)

These rules apply to every role. A PR that breaks one of them is rejected.

### Settings (`ZeroCoder/settings.py`)
- `SECRET_KEY` is read from the environment with no default. If it is missing, the process must fail at startup with a clear error. Remove the current `django-insecure-...` default.
- `DEBUG` is `False` unless `DJANGO_DEBUG` is exactly `1`.
- `ALLOWED_HOSTS` comes from `DJANGO_ALLOWED_HOSTS`. When `DEBUG` is `False` and the list is empty, the process must fail at startup.
- When `DEBUG` is `False`, enable:
  - `SECURE_SSL_REDIRECT = True`
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
  - `SECURE_HSTS_SECONDS = 3600` (raise it only after the owner agrees)
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`
  - `SECURE_REFERRER_POLICY = "same-origin"`
  - `X_FRAME_OPTIONS = "DENY"`
- Keep the four password validators. Do not weaken them.
- Do not create a default superuser in code or migrations.

### Tests and settings
- Tests run with `DEBUG = False` defaults. Requests in tests that would be redirected by `SECURE_SSL_REDIRECT` must use `secure=True`, or the test must use `@override_settings`. Never disable the security settings to make tests pass.

### Application code
- Use Django forms or `ModelForm` for every input. Validate on the server.
- Every state-changing request is a `POST` with CSRF protection. Never change data on `GET`.
- Never use `|safe`, `mark_safe` or `autoescape off` on user-provided content.
- Authorisation is checked on the server for every view that reads or changes user data. Users can edit only their own profile and posts. Use `LoginRequiredMixin` or `login_required` where needed.
- Use the Django ORM. No raw SQL built with string formatting. If raw SQL is ever needed, use parameters.
- Passwords are handled only by `django.contrib.auth`. Never write custom password hashing or store plain passwords.
- Uploaded files: validate the type and size on the server, store them under `MEDIA_ROOT` with generated names, and never execute or render them as HTML. Image handling needs Pillow, which is a new dependency. Ask the owner first (see "Stop and ask").
- Do not log passwords, session IDs, tokens or full IP addresses.
- Do not store IP addresses longer than needed for the feature in progress.

### Secrets and data
- Never commit `.env`, keys, tokens, database files or real data. `.env.example` lists variable names only, never values.
- All data in the project is synthetic. Seed data is generated by a management command or a fixture written by the Developer.

### Dependency and audit checks
- `requirements.txt` pins exact versions.
- Before a release-ready PR, the Tester runs `pip-audit` against `requirements.txt` and reports any finding. A known vulnerability blocks the PR until the Tech Lead decides on the fix.

## Approved dependencies

- Runtime: `Django==6.0.2`.
- Development only: `ruff`, `pip-audit`.

Any other dependency needs owner approval first. When it is approved, the Tech Lead adds it to this list in the same PR.

## Materials

The Tech Lead and the other agents create every material the project needs. Do not ask the owner for them.

- **Text** (copy, sample posts, bios, usernames, descriptions): generated by the agents, synthetic only.
- **Images**: prefer CSS, inline SVG or generated SVG files. If a raster image is needed, use a CC0 or public-domain source, and record the source URL, author and licence in `docs/ASSETS.md`. No photos of real people.
- **Links**: stored in the docs they belong to, with a note on why they are there.

## Documentation the agents maintain

- `docs/TASKS.md`: the task list, owned by the Tech Lead.
- `docs/OPEN-QUESTIONS.md`: questions and the answers given.
- `docs/SCENARIOS.md`: user scenarios for manual checks, owned by the Tech Lead.
- `docs/FEEDBACK.md`: problems found by the User, owned by the User.
- `docs/DESIGN.md`: design decisions, owned by the Designer.
- `docs/ASSETS.md`: sources and licences of non-code assets, owned by the Tech Lead.
- `README.md`: setup and run instructions, kept accurate by the Developer.

## Stop and ask the owner

The Tech Lead handles everything else alone. Ask the owner only in these cases, and only once per decision:

1. Adding a dependency that is not in "Approved dependencies".
2. Turning off or weakening any setting in "Settings".
3. Storing any data that is not synthetic, or any data about real people.
4. Changing the repository visibility, or pushing to `main`.
5. Raising `SECURE_HSTS_SECONDS` above the first value in this file.

Write the question in `docs/OPEN-QUESTIONS.md` with two or three options and a recommendation. Continue with other work while waiting.
