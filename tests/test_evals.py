"""The eval suite's own tests: the corpus is well formed, the field loader reads the
frontmatter shapes that exist on disk, the metrics are what they say, the canary bites,
and the corpus carries no identity the guard would block.

They use a FICTIONAL field built in a temp dir, so they need neither the private skill
snapshot nor a key, and they prove the runner rather than any result.
"""

import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
EVALS = REPO / "evals"
GUARD = REPO / "tools" / "check-identity.sh"
sys.path.insert(0, str(EVALS))

import run  # noqa: E402  (evals/run.py)


def fake_field(root: pathlib.Path) -> None:
    (root / "bake-bread").mkdir()
    (root / "bake-bread" / "SKILL.md").write_text(
        '---\nname: "bake-bread"\ndescription: "Bake a loaf. Trigger on \\"bake me a loaf\\", '
        '\\"make bread\\". NOT for cakes."\n---\nbody\n', encoding="utf-8")
    (root / "ice-cake").mkdir()
    (root / "ice-cake" / "SKILL.md").write_text(
        "---\nname: ice-cake\ndescription: |\n  Ice a cake with buttercream.\n"
        "  Fires on \"ice this cake\", \"decorate the sponge\".\n---\n", encoding="utf-8")
    (root / "plain").mkdir()
    (root / "plain" / "SKILL.md").write_text(
        "---\nname: plain\ndescription: Sweep the floor and nothing else.\n---\n", encoding="utf-8")


class TestFrontmatter(unittest.TestCase):
    def test_the_three_shapes_on_disk_parse(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            fake_field(root)
            field = run.load_field(root)
        self.assertEqual(set(field), {"bake-bread", "ice-cake", "plain"})
        self.assertIn('"bake me a loaf"', field["bake-bread"])  # quoted, with escapes
        self.assertIn("decorate the sponge", field["ice-cake"])  # block scalar joined
        self.assertEqual(field["plain"], "Sweep the floor and nothing else.")

    def test_the_six_subjects_load_from_the_repo(self) -> None:
        field = run.load_field(EVALS / "subjects")
        self.assertEqual(len(field), 6)
        self.assertTrue(all(len(d) > 100 for d in field.values()))


class TestCorpus(unittest.TestCase):
    def test_cases_tsv_is_well_formed(self) -> None:
        cases = run.load_cases()  # exits on a malformed corpus
        self.assertTrue(cases)

    def test_validate_names_each_fault(self) -> None:
        good = run.Case({"id": "x-01", "phrasing": "p", "expected": "NONE", "class": "N",
                         "provenance": "here", "judged": "Pix 2026-10-09"})
        canary = run.Case({"id": "canary-01", "phrasing": "p", "expected": "NONE", "class": "C",
                           "provenance": "built to fail", "judged": "agent"})
        self.assertEqual(run.validate([good, canary], subjects=set()), [])
        bad = run.Case({"id": "x-01", "phrasing": "", "expected": "nope", "class": "Z",
                        "provenance": "", "judged": ""})
        problems = run.validate([good, bad], subjects=set())
        joined = "\n".join(problems)
        for fault in ("duplicated", "phrasing is empty", "no provenance", "not judged",
                      "class 'Z'", "not a subject", "no canary"):
            self.assertIn(fault, joined)

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_the_corpus_carries_no_identity_even_under_ignore_allow(self) -> None:
        """Flag 9 of the scope: realistic phrasings carry real names. Strict mode."""
        result = subprocess.run(["bash", str(GUARD), "--file", str(EVALS / "cases.tsv"), "--ignore-allow"],
                                capture_output=True, text=True, cwd=str(REPO))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TestLexicalArm(unittest.TestCase):
    def setUp(self) -> None:
        self.field = {
            "bake-bread": 'Bake a loaf. Trigger on "bake me a loaf", "make bread". NOT for cakes.',
            "ice-cake": 'Ice a cake with buttercream. Fires on "ice this cake", "decorate the sponge".',
            "plain": "Sweep the floor and nothing else.",
        }
        self.lex = run.Lexical(self.field)

    def test_a_verbatim_phrase_scores_one(self) -> None:
        self.assertEqual(self.lex.pick("bake me a loaf", 0.5), ("bake-bread", 1.0))

    def test_an_unrelated_phrase_is_none(self) -> None:
        self.assertEqual(self.lex.pick("tune the piano", 0.5)[0], run.NONE)

    def test_verbatim_beats_overlap_however_short(self) -> None:
        field = {"quoted": 'Fires on "go now".', "wordy": "Go here, go there, go anywhere, go go go."}
        name, score = run.Lexical(field).pick("go now", 0.5)
        self.assertEqual((name, score), ("quoted", 1.0))
        self.assertLessEqual(run.Lexical(field).scores("go now")["wordy"], run.OVERLAP_CAP)

    def test_overlap_is_weighted_and_bounded(self) -> None:
        name, score = self.lex.pick("decorate a cake", 0.3)
        self.assertEqual(name, "ice-cake")
        self.assertTrue(0 < score <= 1)


class TestMetricsAndCanary(unittest.TestCase):
    def case(self, id, expected, cls="T"):
        return run.Case({"id": id, "phrasing": id, "expected": expected, "class": cls,
                         "provenance": "test", "judged": "test"})

    def test_precision_recall_and_too_few(self) -> None:
        cases = [self.case("a1", "s"), self.case("a2", "s"), self.case("a3", "s"),
                 self.case("b1", "NONE", "N"), self.case("c1", "t")]
        preds = {"a1": "s", "a2": "s", "a3": "NONE", "b1": "s", "c1": "t"}
        m = run.metrics(cases, preds, {"s", "t"})
        self.assertEqual((m["s"]["tp"], m["s"]["fp"], m["s"]["fn"]), (2, 1, 1))
        self.assertAlmostEqual(m["s"]["precision"], 2 / 3)
        self.assertAlmostEqual(m["s"]["recall"], 2 / 3)
        self.assertEqual(m["t"]["note"], "too few to score")

    def test_other_is_scored_by_field_membership(self) -> None:
        c = self.case("o1", "other:design-handoff", "D")
        self.assertTrue(run.correct(c, "design-handoff", {"design-handoff": ""}))
        self.assertFalse(run.correct(c, "handoff", {"design-handoff": ""}))
        self.assertTrue(run.correct(c, run.NONE, {"handoff": ""}))  # not in field: NONE is right

    def test_the_canary_bites_and_an_unbitten_canary_fails_the_run(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            fake_field(root)
            cases = root / "cases.tsv"
            cases.write_text("\t".join(run.COLUMNS) + "\n"
                             "canary-01\tbake me a loaf\tice-cake\tC\tbuilt to fail\tagent\n", encoding="utf-8")
            # The real run exits 0: lexical says bake-bread, expected ice-cake, so it bit.
            self.assertEqual(run.main(["--field", str(root), "--subjects", str(root), "--cases", str(cases)]), 0)
            # Flip the expectation to the truth and the canary no longer fails: exit 3.
            cases.write_text("\t".join(run.COLUMNS) + "\n"
                             "canary-01\tbake me a loaf\tbake-bread\tC\tbuilt to fail\tagent\n", encoding="utf-8")
            self.assertEqual(run.main(["--field", str(root), "--subjects", str(root), "--cases", str(cases)]), 3)


if __name__ == "__main__":
    unittest.main()
