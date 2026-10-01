#!/usr/bin/env bash
# bootstrap-guard.sh: install the identity guard into another repository, in one command.
#
# This repository is the template master. The guard files are COPIED FROM HERE at run
# time and nothing keeps a second copy, so a repository bootstrapped today and one
# bootstrapped next month get whatever this repository holds on the day, and the two
# cannot have been built from different templates.
#
# What it does, in order, and it stops at the first failure:
#   1. copies the guard file set into the target (never overwrites without --force);
#   2. adds the plaintext denylist to the target's .gitignore;
#   3. writes a CLAUDE.md from template/CLAUDE.md.stub if the target has none;
#   4. sets core.hooksPath to .githooks in the target;
#   5. seeds tools/identity-denylist-private.txt from --denylist, or from the example;
#   6. stages, by name, exactly the files it wrote (the sweep and suite read the tracked tree);
#   7. generates tools/identity-denylist.hashes, sweeping it against that tree, and stages it;
#   8. runs tests/test_repo_identity.py in the target, and exits non-zero unless green.
#
# SCOPE IS WRITTEN INTO THE TOOL, not left to memory. The guard is standard where a
# repository is or could become public, and opt-in where it is permanently private:
#   - a target whose CLAUDE.md declares "Publicity: PERMANENTLY PRIVATE" is refused
#     unless --opt-in is passed;
#   - a target listed in the never-list is refused outright, --opt-in or not. The list is
#     private and lives outside every repository (default ~/.config/identity-guard/never,
#     one absolute path per line, # for comments; override with IDENTITY_GUARD_NEVER).
#     It exists for repositories whose commit path is automated, where a blocking hook
#     would break a working job. It is kept out of this repository because it names them.
#
# It STAGES but does NOT commit. The commit is the target owner's decision, and it is the
# moment the guard starts protecting history. `git restore --staged <path>` undoes a stage.
#
# Usage: bootstrap-guard.sh <target-repo> [--denylist <private-source>] [--opt-in] [--force]
# Exit 0 installed and green, 1 refused or a step failed, 2 misuse.

set -uo pipefail

MASTER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NEVER_LIST="${IDENTITY_GUARD_NEVER:-$HOME/.config/identity-guard/never}"

FILES=(
  tools/check-identity.sh
  tools/generate-identity-hashes.sh
  tools/identity-denylist-private.example.txt
  .githooks/pre-commit
  .githooks/commit-msg
  tests/test_repo_identity.py
)
PRIVATE_REL="tools/identity-denylist-private.txt"

usage() {
  echo "usage: bootstrap-guard.sh <target-repo> [--denylist <private-source>] [--opt-in] [--force]" >&2
  exit 2
}

say()  { echo "bootstrap: $*"; }
fail() { echo "bootstrap: REFUSED: $*" >&2; exit 1; }

TARGET="" DENYLIST="" OPT_IN=0 FORCE=0 wrote_claude=""
while [ $# -gt 0 ]; do
  case "$1" in
    --denylist) [ $# -ge 2 ] || usage; DENYLIST="$2"; shift 2 ;;
    --opt-in)   OPT_IN=1; shift ;;
    --force)    FORCE=1; shift ;;
    -*)         usage ;;
    *)          [ -z "$TARGET" ] || usage; TARGET="$1"; shift ;;
  esac
done
[ -n "$TARGET" ] || usage
[ -d "$TARGET" ] || fail "no such directory: $TARGET"
TARGET="$(cd "$TARGET" && pwd -P)"

# --- the target must be the root of a git repository, and not this one -------------------
top="$(git -C "$TARGET" rev-parse --show-toplevel 2>/dev/null)" || fail "$TARGET is not a git repository"
[ "$(cd "$top" && pwd -P)" = "$TARGET" ] || fail "$TARGET is inside a repository rooted at $top; pass the root"
[ "$TARGET" != "$(cd "$MASTER" && pwd -P)" ] || fail "the target is the template master itself"

# --- scope ----------------------------------------------------------------------------------
if [ -f "$NEVER_LIST" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    line="${line%%#*}"; line="$(printf '%s' "$line" | sed 's/[[:space:]]*$//')"
    [ -n "$line" ] || continue
    never="$(cd "$line" 2>/dev/null && pwd -P || printf '%s' "$line")"
    [ "$never" = "$TARGET" ] && fail "$TARGET is on the never-list ($NEVER_LIST). Not overridable here."
  done < "$NEVER_LIST"
fi

if [ -f "$TARGET/CLAUDE.md" ] && grep -q 'Publicity: PERMANENTLY PRIVATE' "$TARGET/CLAUDE.md"; then
  [ "$OPT_IN" -eq 1 ] || fail "$TARGET declares PERMANENTLY PRIVATE; the guard is opt-in there. Pass --opt-in to proceed."
  say "PERMANENTLY PRIVATE target, proceeding on --opt-in"
fi

if [ -n "$DENYLIST" ] && [ ! -f "$DENYLIST" ]; then
  fail "denylist source not found: $DENYLIST"
fi

# --- 1. the file set ------------------------------------------------------------------------
if [ "$FORCE" -eq 0 ]; then
  clash=()
  for f in "${FILES[@]}"; do [ -e "$TARGET/$f" ] && clash+=("$f"); done
  [ ${#clash[@]} -eq 0 ] || fail "already present in the target: ${clash[*]}. Compare them first; --force overwrites."
fi
for f in "${FILES[@]}"; do
  [ -f "$MASTER/$f" ] || fail "template master is missing $f"
  mkdir -p "$TARGET/$(dirname "$f")"
  cp -p "$MASTER/$f" "$TARGET/$f"
  say "copied $f"
done

# --- 2. gitignore ---------------------------------------------------------------------------
if ! grep -qxF "$PRIVATE_REL" "$TARGET/.gitignore" 2>/dev/null; then
  {
    [ -s "$TARGET/.gitignore" ] && [ -n "$(tail -c1 "$TARGET/.gitignore")" ] && echo
    echo "# The PLAINTEXT identity denylist. Gitignored by design: the tracked half is the"
    echo "# generated hash file, and the plaintext never enters history."
    echo "$PRIVATE_REL"
  } >> "$TARGET/.gitignore"
  say "added $PRIVATE_REL to .gitignore"
fi

# --- 3. CLAUDE.md ---------------------------------------------------------------------------
if [ -f "$TARGET/CLAUDE.md" ]; then
  grep -q 'Publicity:' "$TARGET/CLAUDE.md" \
    || say "WARNING: CLAUDE.md carries no Publicity: line. Absent one, the repository may not be published."
else
  cp "$MASTER/template/CLAUDE.md.stub" "$TARGET/CLAUDE.md"; wrote_claude=1
  say "wrote CLAUDE.md from the stub. Its Publicity: line is blank on purpose; fill it."
fi

# --- 4. hooks -------------------------------------------------------------------------------
git -C "$TARGET" config core.hooksPath .githooks || fail "could not set core.hooksPath"
say "core.hooksPath = .githooks"

# --- 5. the private denylist ----------------------------------------------------------------
if [ -n "$DENYLIST" ]; then
  cp "$DENYLIST" "$TARGET/$PRIVATE_REL"
  say "seeded the private denylist from the given source"
elif [ -f "$TARGET/$PRIVATE_REL" ]; then
  say "kept the existing private denylist"
else
  cp "$TARGET/tools/identity-denylist-private.example.txt" "$TARGET/$PRIVATE_REL"
  say "seeded the private denylist from the FICTIONAL example. Replace it with real tokens."
fi
chmod 600 "$TARGET/$PRIVATE_REL"

# --- 6. stage, by name, so the collision sweep and the suite see the guard files ---
STAGE=("${FILES[@]}" .gitignore)
[ -n "$wrote_claude" ] && STAGE+=(CLAUDE.md)
git -C "$TARGET" add -- "${STAGE[@]}" || fail "could not stage the guard files"
say "staged: ${STAGE[*]}"

# --- 7. hashes ------------------------------------------------------------------------------
( cd "$TARGET" && IDENTITY_SIBLING=/nonexistent bash tools/generate-identity-hashes.sh ) \
  || fail "hash generation failed (above). Nothing is committed; fix the denylist and rerun with --force."

git -C "$TARGET" add -- tools/identity-denylist.hashes || fail "could not stage the hash file"

# --- 8. tests -------------------------------------------------------------------------------
( cd "$TARGET" && python3 -m unittest discover -s tests -p test_repo_identity.py ) \
  || fail "the identity suite is not green in the target (above)."

say "installed and green in $TARGET. Staged, not committed: review the stage, then commit."
