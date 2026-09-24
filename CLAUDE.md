# pix-harness — Project Agent Context

**`Publicity: MAY BE PUBLISHED`**

Declared at creation, 2026-09-24, and this line is the source. Absent an explicit
declaration a repository may not be published, so the declaration is written when the
repository is created rather than when someone first wants to push it.

**Default branch:** `main`, lowercase.
**Created:** 2026-09-24. **History starts clean:** one squashed first commit, nothing
cloned in from a private repository.

---

## 0  Read this first: this repository is public

Everything committed here is published, immediately and permanently, and git history
cannot be selectively un-published later. A mistake in a private repository is a tidy-up.
The same mistake here is a disclosure.

That inverts the usual default. The question is not *"is there any reason to keep this
out?"* It is **"is there any reason this may go in?"**

## 1  The guard runs on this repository, not only in it

`tools/check-identity.sh` is both the artefact and the working guard. Install it in every
clone before committing:

```sh
git config core.hooksPath .githooks
```

The plaintext denylist source is gitignored and absent from clones by design. That absence
is expected, not broken. Start from `tools/identity-denylist-private.example.txt`.

Run the guard's own suite before any commit that touches `tools/`, `.githooks/` or
`tests/`:

```sh
python3 -m unittest discover -s tests -v
```

## 2  Every promoted artefact carries a `## Share-safe statement`

Anything added here from private working material ends with one, naming what it
deliberately excludes. A judgement made once at promotion evaporates. A statement carried
inside the artefact travels with the file, and makes the exclusion checkable against the
file's own stated boundary rather than a reviewer's guess at one.

**If something cannot honestly carry one, it is not ready to be published.**

## 3  House rules

- **Flag freely, diagnose tentatively.** Raise anything inconsistent, risky or possibly
  wrong as a question, not a verdict. A wrong flag is cheaper than a missed one.
- **Go to the primary artefact, not the thing describing it.** A file's name is not
  evidence of its contents, and a summary asserting a fact is not a reading of it.
- **Check the date from the shell before writing one:** `date '+%Y-%m-%d %H:%M %Z'`.
- **Every git read uses `--no-optional-locks`.** A stale index lock in a mounted
  repository breaks scheduled jobs silently.
- **Never `git add -A` here.** Add paths explicitly. The gitignore is a second line, not
  the first.
- **House style:** British English, no em-dashes, each point made once. This repository is
  public, so house style is the published voice rather than a preference.

## 4  What is here

| Path | What it is |
|---|---|
| `tools/` | The identity guard and its hash generator. |
| `.githooks/` | The two hooks that call the guard. Wiring only. |
| `tests/` | The guard as a test, so a fresh clone is guarded before install. |

Parts 1 and 2 of the three-part artefact, the skill-trigger eval suite and the fleet cost
instrumentation, are not here yet. `README.md` says so with a date, and that date is the
thing to keep true.

**Live status is the repository, never this file.**
