# Open questions

Owner: Tech Lead. Questions that `CLAUDE.md` and the task description do not answer.

The Tech Lead answers a question itself when the answer is in `CLAUDE.md`. The owner is asked only in the cases listed in "Stop and ask the owner" in `CLAUDE.md`. Work continues on other tasks while a question is open.

Entry format:

```
## OQ-NN: <question>
- Status: open | answered
- Needs owner: yes | no
- Options:
  1. <option>
  2. <option>
- Recommendation: <option and why>
- Answer: <text, who answered, date>
```

---

## OQ-01: How are profile pictures handled?
- Status: open
- Needs owner: yes (a new dependency, Pillow, is required for image uploads; "Stop and ask" case 1)
- Options:
  1. No uploaded images. Use a generated initials avatar made with CSS.
  2. Add Pillow and allow image uploads with server-side type and size checks.
  3. Use pre-made synthetic SVG avatars chosen from a fixed set.
- Recommendation: Option 1 for now. It needs no dependency, keeps the data synthetic and can be changed later. TASK-06 is written without an image field.
- Answer:

## OQ-02: What does the feed show?
- Status: open
- Needs owner: no
- Options:
  1. Posts from the user and their friends only.
  2. All posts from all users.
- Recommendation: Option 1. It matches the friends feature in `CLAUDE.md` and keeps TASK-09 after TASK-08.
- Answer:

## OQ-03: Where are development dependencies recorded?
- Status: open
- Needs owner: no
- Options:
  1. A separate `requirements-dev.txt` with pinned `ruff` and `pip-audit`, plus a `[tool.ruff]` config.
  2. Add them to `requirements.txt`.
- Recommendation: Option 1. `CLAUDE.md` marks them as development only, so runtime installs stay minimal. Both tools are already approved; only the file is new. This will be done in TASK-01 together with the README update, since `ruff check .` is a required check.
- Answer:

## OQ-04: Are friend relations mutual?
- Status: open
- Needs owner: no
- Options:
  1. Mutual: a request must be accepted by the recipient (as in TASK-08).
  2. One-way following without acceptance.
- Recommendation: Option 1. The task list calls the feature "friends" and TASK-08 is written that way.
- Answer:
