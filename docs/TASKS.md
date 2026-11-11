# Tasks

Owner: Tech Lead. Rules are in `CLAUDE.md` (Roles, Workflow, Security).

One task per branch `task/<id>-<slug>`, one PR per task. A task is marked `done` in the same PR that completes it. Status values: `todo`, `in progress`, `done`.

Entry format:

```
## TASK-NN: <title>
- Status: todo
- Role: Developer | Designer | Tester
- Branch: task/<id>-<slug>
- Goal: <one or two sentences>
- Acceptance criteria:
  - [ ] <checkable statement>
```

Checks required for every PR (from `CLAUDE.md`): `python manage.py check --deploy` with production variables set, `python manage.py makemigrations --check --dry-run`, `python manage.py test`, `ruff check .`.

---

## TASK-01: Security settings
- Status: done
- Role: Developer
- Branch: task/01-security-settings
- Goal: Bring `ZeroCoder/settings.py` in line with the Security > Settings section of `CLAUDE.md`.
- Acceptance criteria:
  - [x] `SECRET_KEY` is read from the environment with no default; the `django-insecure-...` value is removed; a missing key stops startup with a clear error.
  - [x] `DEBUG` is `False` unless `DJANGO_DEBUG` is exactly `1`.
  - [x] `ALLOWED_HOSTS` comes from `DJANGO_ALLOWED_HOSTS`; with `DEBUG=False` and an empty list, startup fails with a clear error.
  - [x] With `DEBUG=False`: `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS=3600`, `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`, `SECURE_CONTENT_TYPE_NOSNIFF=True`, `SECURE_REFERRER_POLICY="same-origin"`, `X_FRAME_OPTIONS="DENY"`.
  - [x] The four password validators are unchanged.
  - [x] `python manage.py check --deploy` passes with production variables set.
  - [x] `README.md` lists the environment variables and how to run locally.

## TASK-02: Template title and unused import
- Status: done
- Role: Developer
- Branch: task/task-02-title-and-import
- Goal: Remove the duplicate `<title>` from the layout and the unused import from `main/views.py`.
- Acceptance criteria:
  - [x] Each rendered page has exactly one `<title>` element.
  - [x] `main/views.py` has no unused import.
  - [x] `ruff check .` passes.

## TASK-03: Tests for `/` and `/new`
- Status: done
- Role: Developer (Tester verifies)
- Branch: task/task-03-page-tests
- Goal: Cover the two existing pages with tests in `main/tests.py`.
- Acceptance criteria:
  - [x] `/` returns 200 and contains its heading text.
  - [x] `/new` returns 200 and contains its heading text.
  - [x] Both pages are reachable without logging in.
  - [x] Tests run with `DEBUG=False` defaults and use `secure=True` where `SECURE_SSL_REDIRECT` applies; no security setting is disabled to pass.
  - [x] `python manage.py test` passes.

## TASK-04: Visual design
- Status: todo
- Role: Designer
- Branch: task/task-04-design
- Goal: Replace the current pink background with the design recorded in `docs/DESIGN.md`, in one PR.
- Acceptance criteria:
  - [ ] `docs/DESIGN.md` records colours, type scale, spacing, components and breakpoints (from Figma if the connector is available, otherwise decided by the Designer).
  - [ ] Only `main/static/main/css/main.css`, static images and template class names change; no Python code, models, views or URLs.
  - [ ] Text contrast is at least 4.5:1, focus states are visible, meaningful images have `alt` text, no information is carried by colour alone.
  - [ ] Any non-code asset is recorded in `docs/ASSETS.md`.

## TASK-05: User accounts
- Status: todo
- Role: Developer
- Branch: task/task-05-accounts
- Goal: Registration, login and logout using `django.contrib.auth` only.
- Acceptance criteria:
  - [ ] Registration uses a Django form with server-side validation and the existing password validators.
  - [ ] Login and logout use `django.contrib.auth`; logout is a `POST`.
  - [ ] Navigation shows login/registration for anonymous users and logout for signed-in users.
  - [ ] No custom password handling and no default superuser.
  - [ ] Tests cover registration, login, logout and invalid input.

## TASK-06: Profile
- Status: todo
- Role: Developer
- Branch: task/task-06-profile
- Goal: A profile model linked to the user, a profile page and an edit form.
- Acceptance criteria:
  - [ ] Profile model is linked to the user and created for each new user; fields are defined by the Tech Lead in the PR description before coding (no image field, see OQ-01).
  - [ ] Profile page is visible to signed-in users.
  - [ ] A user can edit only their own profile; editing another profile is rejected on the server.
  - [ ] Migration included; `makemigrations --check` is clean.
  - [ ] Tests cover view, edit own, and edit someone else's (rejected).

## TASK-07: Posts
- Status: todo
- Role: Developer
- Branch: task/task-07-posts
- Goal: Post model with create, view, edit and delete.
- Acceptance criteria:
  - [ ] Post has an author, text and creation time.
  - [ ] Create, edit and delete are `POST` requests with CSRF protection.
  - [ ] Only the author can edit or delete a post; other users are rejected on the server.
  - [ ] User text is escaped in templates (no `|safe`, no `mark_safe`).
  - [ ] Migration included; tests cover create, edit/delete by author, and rejection for others.

## TASK-08: Friends
- Status: todo
- Role: Developer
- Branch: task/task-08-friends
- Goal: Friend requests between users.
- Acceptance criteria:
  - [ ] A user can send, accept, decline and remove a friend relation; each action is a `POST`.
  - [ ] A user cannot send a request to themselves or create a duplicate.
  - [ ] Only the recipient can accept or decline a request.
  - [ ] Migration included; tests cover each action and the rejection cases.

## TASK-09: Feed
- Status: todo
- Role: Developer
- Branch: task/task-09-feed
- Goal: A feed page of posts for the signed-in user.
- Acceptance criteria:
  - [ ] Feed requires login.
  - [ ] Posts are ordered newest first; scope (own plus friends' or all) follows the answer to OQ-02.
  - [ ] Tests cover ordering, scope, and redirect for anonymous users.

## TASK-10: Comments
- Status: todo
- Role: Developer
- Branch: task/task-10-comments
- Goal: Comments on posts.
- Acceptance criteria:
  - [ ] A signed-in user can add a comment to a post via a form (`POST`, CSRF).
  - [ ] Only the comment author can delete their comment.
  - [ ] User text is escaped in templates.
  - [ ] Migration included; tests cover add, delete own, and rejection for others.

## TASK-11: Likes
- Status: todo
- Role: Developer
- Branch: task/task-11-likes
- Goal: Likes on posts.
- Acceptance criteria:
  - [ ] A signed-in user can like and unlike a post; each is a `POST`.
  - [ ] A user can like a given post at most once (enforced by the database).
  - [ ] The like count is shown on the post.
  - [ ] Migration included; tests cover like, unlike, duplicate like.

## TASK-12: Synthetic seed data
- Status: todo
- Role: Developer
- Branch: task/task-12-seed-data
- Goal: A management command that creates synthetic users, profiles, posts, comments, likes and friends for demos.
- Acceptance criteria:
  - [ ] All generated data is synthetic; no real people or personal data.
  - [ ] The command can be run twice without errors or duplicates.
  - [ ] No superuser is created; no data files are committed.
  - [ ] `README.md` documents the command.
  - [ ] A test runs the command.
