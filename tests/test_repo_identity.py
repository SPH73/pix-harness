"""No OEM, customer or person identity may sit in the tracked tree.

**Why this is a TEST and not only a git hook.** A hook must be installed
(`git config core.hooksPath .githooks`), is not cloned as an active hook, and is bypassed
by `git commit --no-verify`. A test needs no install step, travels with the clone, and
cannot be waved through with a flag. The hook is the fast feedback; this is the one that
actually holds.

It runs the SAME `tools/check-identity.sh` the hooks and the scheduled sweep run, rather
than carrying its own copy of the denylist. Two copies of a rule drift apart, and then the
question of which one is the rule has no answer.

**Commit messages are covered too, and less strongly, which is said rather than implied.**
File content can be swept whole, so this test holds it absolutely. A message cannot: a test
cannot read one that does not exist yet, so `.githooks/commit-msg` is the only layer that
stops a bad message at creation, and `--no-verify` still walks through it. What a test CAN
do is refuse to let a new one survive unnoticed, which is `TestCommitMessageHistory` below:
it sweeps history against a named baseline of what is already there.

The rule it enforces: **clean at creation.** Git history travels with a repository and
cannot be selectively un-published later, so anything reaching history has to come out
afterwards with a filter-repo purge. The exposure this pattern was built after needed
three passes.
"""

import hashlib
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
GUARD = REPO / "tools" / "check-identity.sh"

# The commit messages already in history that carry an identifier. A BASELINE, not an
# exemption: it is what a `filter-repo` purge has to reach, and it is here rather than
# inside the guard so it stays visible and can empty. Both tests below act on it, so a
# stale entry fails loudly instead of quietly widening the hole.
#
# The purge rewrites SHAs, so when it lands these keys stop resolving and the second test
# says so. Scaffolding that does not announce its own retirement becomes permanent.
#
# EMPTY HERE, and that is the point rather than an omission: this repository's history
# starts clean, so there is nothing to purge. The mechanism still ships, because a
# repository adopting the guard mid-life will have entries, and an empty baseline is an
# honest starting state where an absent one would be a missing layer.
KNOWN_HISTORY_OFFENDERS: dict[str, str] = {}


class TestTheGuardIsPresent(unittest.TestCase):
    """The SENTINEL, deliberately unguarded (skip-audit 2026-08-24, class C ruling).

    Every other identity test skips when the guard script is absent, for tidy
    reporting — which means deleting tools/check-identity.sh would turn all of them
    green-by-skip and the suite would certify a repo with zero identity cover. This
    one test cannot skip: the guard is TRACKED, so in any honest clone it exists,
    and its absence is a broken repo, not an environment."""

    def test_the_guard_script_exists_and_is_executable(self) -> None:
        self.assertTrue(GUARD.is_file(),
                        "tools/check-identity.sh is missing: every other identity "
                        "test is now silently skipping, and nothing is guarded")
        self.assertTrue(os.access(GUARD, os.X_OK),
                        "tools/check-identity.sh is not executable: the hooks "
                        "refuse and the Friday sweep fails")

    def test_both_hooks_exist_and_are_executable(self) -> None:
        """Same sentinel, same reason: the hooks are tracked, and if one vanished
        the fails-closed tests would silently skip (found by the skip-allowlist
        scanner on its first run, 2026-08-24)."""
        for hook in ("pre-commit", "commit-msg"):
            with self.subTest(hook=hook):
                path = REPO / ".githooks" / hook
                self.assertTrue(path.is_file(), f".githooks/{hook} is missing")
                self.assertTrue(os.access(path, os.X_OK),
                                f".githooks/{hook} is not executable")


class TestTrackedCoreCarriesNoIdentity(unittest.TestCase):
    @unittest.skipUnless(shutil.which("git"), "git not available")
    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_no_identifiers_in_tracked_files(self) -> None:
        result = subprocess.run(
            ["bash", str(GUARD)], capture_output=True, text=True, cwd=str(REPO)
        )
        self.assertEqual(
            result.returncode, 0,
            "the tracked tree carries OEM, customer or person identity:\n"
            f"{result.stdout}{result.stderr}\n"
            "If an identifier is genuinely needed, mark the line with 'oem-allow: <reason>'.",
        )

    @unittest.skipUnless(shutil.which("git"), "git not available")
    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_the_guard_actually_catches_something(self) -> None:
        """A guard nobody has seen fail is not a guard. Proves the pattern bites, so a
        pass above means 'nothing found', not 'the scan silently did nothing'."""
        probe = REPO / "tests" / "_identity_probe_tmp.py"
        probe.write_text('PART = "pq7-9100"\n')  # oem-allow: the probe must look real
        try:
            subprocess.run(["git", "add", "-f", str(probe)], cwd=str(REPO),
                           capture_output=True, check=False)
            result = subprocess.run(["bash", str(GUARD), "--staged"],
                                    capture_output=True, text=True, cwd=str(REPO))
            self.assertEqual(result.returncode, 1, "the guard did not catch a real part number")
            self.assertIn("pq7-9100", result.stdout)  # oem-allow: it must report what it caught
        finally:
            # `git rm --cached`, not `git reset HEAD`: in a repository with no commits
            # yet HEAD does not resolve, the reset fails, and the probe stays in the
            # index to be caught by the next commit. Found on this repository's own
            # first commit, by this repository's own guard.
            subprocess.run(["git", "rm", "-q", "--cached", "--ignore-unmatch", str(probe)],
                           cwd=str(REPO), capture_output=True, check=False)
            probe.unlink(missing_ok=True)

    def test_the_guard_source_is_clean_by_its_own_matcher(self) -> None:
        """The guard proves its own source clean via --file --ignore-allow: the real
        matcher, with the oem-allow exemption disabled so even a marked line cannot
        park an identifier here. No identifier is named in this test — an earlier
        version named three in plaintext to assert their absence, which put back
        exactly what the hashed design removes.

        ⚠ PAIRED TEST — this one is HALF of an invariant. Alone it is circular: a
        broken matcher that matches nothing would vacuously certify the guard clean.
        The other half is TestHashedDenylist.test_a_hashed_token_is_blocked_unmarked
        and test_a_prefix_sibling_is_blocked, which prove the matcher bites on every
        run. If those are ever removed, this test degrades to self-certification and
        must not stand alone."""
        result = subprocess.run(
            ["bash", str(GUARD), "--file", str(GUARD), "--ignore-allow"],
            capture_output=True, text=True, cwd=str(REPO),
        )
        self.assertEqual(
            result.returncode, 0,
            f"the guard's own source matches its denylist:\n{result.stdout}{result.stderr}",
        )


class TestCommitMessagesAreGuarded(unittest.TestCase):
    """`.githooks/commit-msg` mode: the message text itself, not the files it commits."""

    def _scan(self, message: str) -> subprocess.CompletedProcess:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write(message)
            path = handle.name
        try:
            return subprocess.run(
                ["bash", str(GUARD), "--message", path],
                capture_output=True, text=True, cwd=str(REPO),
            )
        finally:
            pathlib.Path(path).unlink(missing_ok=True)

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_a_part_number_in_a_message_is_blocked(self) -> None:
        result = self._scan("fix: correct the pq7-9100 band\n")  # oem-allow: the probe must look real
        self.assertEqual(result.returncode, 1, "a real part number reached the message unblocked")
        self.assertIn("pq7-9100", result.stdout)  # oem-allow: it must report what it caught

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_a_person_in_a_message_is_blocked(self) -> None:
        result = self._scan("docs: write up what Marchetti said on the bench\n")  # oem-allow: the probe must look real
        self.assertEqual(result.returncode, 1, "a person's name reached the message unblocked")

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_the_trailer_covers_the_whole_message_not_its_own_line(self) -> None:
        """The subject carries the identifier and the trailer sits at the bottom, which is
        the normal shape. A per-line marker would refuse this, so this is the test that
        pins the message-level rule."""
        result = self._scan(
            "fix: correct the pq7-9100 band\n"  # oem-allow: the probe must look real
            "\n"
            "oem-allow: the part number is the subject of the fix\n"
        )
        self.assertEqual(result.returncode, 0, "the allow trailer did not cover the subject line")

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_an_ordinary_message_passes(self) -> None:
        result = self._scan("chore: tidy the pack loader\n\nNo identifiers here.\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_gits_own_comment_lines_are_not_the_message(self) -> None:
        """A `--verbose` commit puts the whole diff below a scissors line, and the template
        comments quote branch and status. None of it reaches history, so none of it may
        block a commit."""
        result = self._scan(
            "chore: tidy the pack loader\n"
            "\n"
            "# Please enter the commit message. Lines starting with '#' are ignored.\n"
            "# On branch main mentioning Marchetti\n"  # oem-allow: the probe must look real
            "# ------------------------ >8 ------------------------\n"
            "diff --git a/x b/x\n"
            "+PART = \"pq7-9100\"\n"  # oem-allow: the probe must look real
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TestCommitMessageHistory(unittest.TestCase):
    """History cannot be cleaned by a hook, so it is held to a named baseline instead."""

    def _history(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", str(GUARD), "--history"],
            capture_output=True, text=True, cwd=str(REPO),
        )

    @unittest.skipUnless(shutil.which("git"), "git not available")
    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_no_offending_message_outside_the_known_baseline(self) -> None:
        """This is the layer the commit-msg hook cannot be: it catches a message that got
        in with `--no-verify`, or before anyone ran the hooksPath install step."""
        found = {
            line.split()[1]
            for line in self._history().stdout.splitlines()
            if line.strip().startswith("BLOCKED")
        }
        new = found - set(KNOWN_HISTORY_OFFENDERS)
        self.assertEqual(
            new, set(),
            f"commit message(s) carrying an identifier are not in the known baseline: {sorted(new)}\n"
            "Either purge them, or if the identifier is deliberate, amend the message to carry "
            "an 'oem-allow: <reason>' trailer.",
        )

    @unittest.skipUnless(shutil.which("git"), "git not available")
    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_every_baseline_entry_still_earns_its_place(self) -> None:
        """A baseline is a worklist. When the purge lands these SHAs stop resolving, and
        this test is what says so rather than letting the list ossify."""
        stdout = self._history().stdout
        for sha, why in KNOWN_HISTORY_OFFENDERS.items():
            resolves = subprocess.run(
                ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                cwd=str(REPO), capture_output=True,
            ).returncode == 0
            self.assertTrue(
                resolves,
                f"baseline entry {sha} ({why}) no longer exists. If the history purge has "
                "landed, delete it from KNOWN_HISTORY_OFFENDERS.",
            )
            self.assertIn(
                sha, stdout,
                f"baseline entry {sha} ({why}) no longer offends. If it has been amended, "
                "delete it from KNOWN_HISTORY_OFFENDERS.",
            )


class TestHashedDenylist(unittest.TestCase):
    """The hashed category: tokens the guard blocks without naming. A real maker is
    named only once it has authorised that use, so the guard cannot carry the name in
    plaintext. The tracked hash file is GENERATED from a private,
    gitignored source; these tests use a SYNTHETIC token via the IDENTITY_HASHES
    override so they never name a real one."""

    HASHFILE = REPO / "tools" / "identity-denylist.hashes"
    GENERATOR = REPO / "tools" / "generate-identity-hashes.sh"
    PRIVATE = REPO / "tools" / "identity-denylist-private.txt"

    def _scan_message(self, message: str, hashes_path: str) -> subprocess.CompletedProcess:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write(message)
            path = handle.name
        try:
            return subprocess.run(
                ["bash", str(GUARD), "--message", path],
                capture_output=True, text=True, cwd=str(REPO),
                env={**os.environ, "IDENTITY_HASHES": hashes_path},
            )
        finally:
            pathlib.Path(path).unlink(missing_ok=True)

    def _synthetic_hashes(self, token: str) -> str:
        digest = hashlib.sha256(token.lower().encode()).hexdigest()
        handle = tempfile.NamedTemporaryFile("w", suffix=".hashes", delete=False)
        handle.write(f"# synthetic test denylist\n{len(token)} {digest}\n")
        handle.close()
        self.addCleanup(pathlib.Path(handle.name).unlink)
        return handle.name

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_a_missing_hash_file_fails_loudly_never_silently(self) -> None:
        """Pix, 2026-08-24: 'the guard failing loudly is a must or the system is
        broken doubly.' A guard that passes without its denylist reports success
        it has not earned."""
        result = self._scan_message("chore: nothing here\n", "/nonexistent/denylist.hashes")
        self.assertNotEqual(result.returncode, 0, "the guard passed with its denylist absent")
        self.assertEqual(result.returncode, 2)
        self.assertIn("MISSING", result.stderr)

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_a_hashed_token_is_blocked_unmarked(self) -> None:
        """⚠ PAIRED TEST — with test_the_guard_source_is_clean_by_its_own_matcher
        (and test_a_prefix_sibling_is_blocked below). This half proves the matcher
        BITES; the self-scan half uses the matcher to certify the guard's source
        clean. Remove this and the self-scan degrades to self-certification — a
        guard vacuously approving itself."""
        hashes = self._synthetic_hashes("examplecorp-forbidden")
        result = self._scan_message("docs: notes on Examplecorp-Forbidden tables\n", hashes)
        self.assertEqual(result.returncode, 1, "a hashed-denylist token went unblocked")
        self.assertIn("hashed-denylist token", result.stdout)

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_the_allow_trailer_covers_a_hashed_token(self) -> None:
        hashes = self._synthetic_hashes("examplecorp-forbidden")
        result = self._scan_message(
            "docs: notes on examplecorp-forbidden tables\n"
            "\n"
            "oem-allow: the token is the subject of the note\n",
            hashes,
        )
        self.assertEqual(result.returncode, 0, "the trailer did not cover a hashed hit")

    @unittest.skipUnless(shutil.which("git"), "git not available")
    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_a_hashed_token_in_a_tracked_path_is_blocked(self) -> None:
        """A pack file NAMED after a maker, with clean contents, is the likeliest
        re-entry shape, so paths are scanned like content."""
        hashes = self._synthetic_hashes("examplecorp-forbidden")
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = pathlib.Path(tmp)
            subprocess.run(["git", "init", "-q", str(sandbox)], check=True, capture_output=True)
            offender = sandbox / "packs" / "examplecorp-forbidden.toml"
            offender.parent.mkdir()
            offender.write_text("# perfectly clean contents\n")
            subprocess.run(["git", "-C", str(sandbox), "add", "."], check=True,
                           capture_output=True)
            result = subprocess.run(
                ["bash", str(GUARD)],
                capture_output=True, text=True, cwd=str(sandbox),
                env={**os.environ, "HARNESS_REPO": str(sandbox), "IDENTITY_HASHES": hashes},
            )
            self.assertEqual(result.returncode, 1,
                             f"a hashed token in a tracked PATH went unblocked:\n{result.stdout}")
            self.assertIn("tracked path", result.stdout)

    def test_the_tracked_hash_file_is_generated_shape(self) -> None:
        """Every non-comment line is '<length> <sha256>' and nothing else: the tracked
        half is generated, never hand-written, so plaintext cannot leak into it. The
        length is the prefix length the scanner tests at. The REAL floor (5, with
        marked exceptions collision-swept every generation) is enforced by the
        generator and proven by the generator tests below; this shape test cannot see
        the private markers, so it holds only the sanity line: nothing shorter than
        3, the smallest ruled exception, ever reaches the tracked file."""
        self.assertTrue(self.HASHFILE.is_file(), "tracked hash denylist is absent")
        entries = [
            line.strip()
            for line in self.HASHFILE.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        ]
        self.assertGreater(len(entries), 0, "the hash denylist holds no entries")
        for entry in entries:
            self.assertRegex(entry, r"^\d+ [0-9a-f]{64}$",
                             "a non-'length digest' line sits in the generated hash file")
            self.assertGreaterEqual(int(entry.split()[0]), 3,
                                    "an entry sits below even the exception floor")

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_a_prefix_sibling_is_blocked(self) -> None:
        """A prefix entry must catch a family member that is NOT in the source
        verbatim — that is what makes one entry cover an open-ended family.

        ⚠ PAIRED TEST — see test_a_hashed_token_is_blocked_unmarked: together they
        are the bite half of the invariant whose other half is
        test_the_guard_source_is_clean_by_its_own_matcher."""
        hashes = self._synthetic_hashes("examplecorp")
        result = self._scan_message("docs: notes on the examplecorp-9910 variant\n", hashes)
        self.assertEqual(result.returncode, 1, "a prefix sibling went unblocked")
        self.assertIn("examplecorp-9910", result.stdout)

    def _generate(self, source_text: str) -> subprocess.CompletedProcess:
        """Run the generator against a temporary private source, sibling sweep off."""
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write(source_text)
            src = handle.name
        self.addCleanup(pathlib.Path(src).unlink)
        out = src + ".hashes"
        self.addCleanup(lambda: pathlib.Path(out).unlink(missing_ok=True))
        return subprocess.run(
            ["bash", str(self.GENERATOR)],
            capture_output=True, text=True, cwd=str(REPO),
            env={**os.environ, "IDENTITY_PRIVATE": src, "IDENTITY_HASHES": out,
                 "IDENTITY_SIBLING": "/nonexistent"},
        )

    def test_the_generator_refuses_a_below_floor_entry(self) -> None:
        """A short prefix would block half the vocabulary, so the floor is enforced
        where entries are made, loudly and non-zero."""
        result = self._generate("abc\n")
        self.assertEqual(result.returncode, 2, "a 3-character entry was not refused")
        self.assertIn("REFUSED", result.stderr)

    def test_a_floor_exception_admits_a_short_entry_still_swept(self) -> None:
        """The marker admits a short entry past the floor and nothing else: the
        collision sweep still runs on it every generation. The synthetic stem is
        chosen to collide with nothing in this repo's tree."""
        result = self._generate("zq9  # floor-exception: synthetic test stem\n")  # oem-allow: the sweep found this very line, correctly; the probe stem must not fail its own test
        self.assertEqual(result.returncode, 0,
                         f"a marked below-floor entry was refused:\n{result.stderr}")

    def test_the_sweep_refuses_a_colliding_entry(self) -> None:
        """The hard-fail collision sweep: an entry that would block something already
        legitimately tracked refuses generation until resolved (Pix,
        2026-08-24: the friction is chosen deliberately). 'tests' collides with
        this repo's own tree by construction."""
        result = self._generate("tests\n")
        self.assertEqual(result.returncode, 1, "a colliding entry was not refused")
        self.assertIn("collides", result.stderr)

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_file_mode_refuses_a_missing_path(self) -> None:
        result = subprocess.run(
            ["bash", str(GUARD), "--file", "/nonexistent/nothing.txt"],
            capture_output=True, text=True, cwd=str(REPO),
        )
        self.assertEqual(result.returncode, 2)

    @unittest.skipUnless(PRIVATE.is_file(), "private source absent (gitignored; not every machine)")
    def test_the_tracked_hashes_match_the_private_source(self) -> None:
        """Drift check: regenerate to a temp file and compare. If this fails, the
        private source was edited without rerunning the generator."""
        with tempfile.NamedTemporaryFile(suffix=".hashes", delete=False) as handle:
            out = handle.name
        self.addCleanup(pathlib.Path(out).unlink)
        result = subprocess.run(
            ["bash", str(self.GENERATOR)],
            capture_output=True, text=True, cwd=str(REPO),
            # The sibling sweep is skipped (nonexistent path): this test compares
            # hashes, and the sibling report is informational output, not part of them.
            env={**os.environ, "IDENTITY_HASHES": out, "IDENTITY_SIBLING": "/nonexistent"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        current = [l for l in self.HASHFILE.read_text().splitlines() if not l.startswith("#")]
        fresh = [l for l in pathlib.Path(out).read_text().splitlines() if not l.startswith("#")]
        self.assertEqual(current, fresh,
                         "tracked hashes drift from the private source: rerun "
                         "tools/generate-identity-hashes.sh")


class TestTheGuardFailsClosed(unittest.TestCase):
    """An absent guard must refuse the commit, not wave it through. Both hooks say so in
    prose; this is the one that proves it."""

    @unittest.skipUnless(shutil.which("git"), "git not available")
    def test_a_hook_with_no_guard_refuses(self) -> None:
        for hook in ("pre-commit", "commit-msg"):
            with self.subTest(hook=hook):
                source = REPO / ".githooks" / hook
                if not source.is_file():
                    self.skipTest(f"{hook} not present")
                with tempfile.TemporaryDirectory() as tmp:
                    sandbox = pathlib.Path(tmp)
                    subprocess.run(["git", "init", "-q", str(sandbox)], check=True,
                                   capture_output=True)
                    message = sandbox / "MSG"
                    message.write_text("chore: nothing to see\n")
                    result = subprocess.run(
                        ["bash", str(source), str(message)],
                        cwd=str(sandbox), capture_output=True, text=True,
                    )
                    self.assertEqual(
                        result.returncode, 1,
                        f"{hook} did not refuse with the guard absent:\n{result.stdout}{result.stderr}",
                    )
                    self.assertIn("guard missing", result.stderr)


if __name__ == "__main__":
    unittest.main()
