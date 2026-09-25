# pix-harness

An agent harness: the guardrails, verification, supervision and context layers that decide whether an agent can be trusted to run when nobody is watching. Addy Osmani's framing in *AI Engineering* is that an agent is a model plus a harness, and that the harness is the durable half because the model underneath it depreciates. This repository is the harness half, taken out of a private working system and published as it stands. It is not a framework and it is not a demo. Each piece runs in production against real work, and each piece is here because something went wrong once without it.

## How it was built, and why that is the point

None of it was designed up front. It accumulated. Every rule exists because a specific thing went wrong, and the record of what went wrong is kept beside the rule rather than in a changelog nobody opens. Osmani's version of this is that every line in a good agent instructions file should be traceable back to a specific failure. That is a description of how the files in this repository were actually written.

One worked example, in full, because the claim is only believable from a traceable instance.

**The guard that published what it existed to hide.**

The identity guard keeps maker names, part numbers, customer names and person names out of a tracked tree. The first version held its denylist in plaintext, so a human could read and edit it. The guard is itself a tracked file, which meant the guard's source now carried every identifier it existed to keep out, in a repository whose whole purpose was not to carry them. The mechanism was the leak.

Then the fix made it worse before it made it better. A test was written to prove the guard's source clean. To assert that three identifiers were absent, it named all three in plaintext, in a tracked test file. The check written to confirm the problem was solved reintroduced the problem.

What came out of that is the shape in `tools/` today:

- The denylist is **hashed**. The tracked file holds `<length> <sha256>` pairs and nothing else, so the guard blocks a token without naming it.
- The plaintext source is **private and gitignored**, and nobody hand-maintains the tracked half, so the two cannot drift.
- The guard **proves its own source clean using its own matcher**, via `--file --ignore-allow`, which disables the escape hatch so a marked line cannot park an identifier in the guard itself.

And that fix created a hazard of its own, which is the part worth showing. A guard certifying itself with its own matcher is circular: a broken matcher that matched nothing would certify the guard clean and report success it had not earned. So the self-scan is marked in the source as half of an invariant, and its pair is the test that proves the matcher bites on every run. Both docstrings say so, and both say what breaks if the other is deleted. See `TestTrackedCoreCarriesNoIdentity.test_the_guard_source_is_clean_by_its_own_matcher` and `TestHashedDenylist.test_a_hashed_token_is_blocked_unmarked`.

Three failures, three rules, and every one of them still readable next to the code it produced.

## What is here now

**The identity guard, extracted and genericised.** It is designed to leak nothing, so it publishes as it stands.

### What it does

It refuses to let an identifier enter a repository's history: OEM makers and part numbers, customer names, and person names. Not a secret scanner, which looks for the shape of a credential. This looks for a named list of things that must not be published, and it does so without publishing the list.

### The shape

| Piece | What it is |
|---|---|
| `tools/check-identity.sh` | The whole matcher and the only denylist. Five modes: `--staged`, `--message`, `--file`, `--history`, and the default tracked sweep. |
| `.githooks/pre-commit` | Scans the staged diff. Wiring only. |
| `.githooks/commit-msg` | Scans the commit message, which is history too and which a content scan cannot see. Wiring only. |
| `tests/test_repo_identity.py` | The same sweep as a test, so a fresh clone is guarded before anyone runs the install step. |
| `tools/generate-identity-hashes.sh` | Regenerates the tracked hash file from the private plaintext source, refusing a denylist that would misfire. |

Four callers share one denylist, so they cannot drift apart about what counts. That is the design decision the rest follows from. Two copies of a rule drift, and then the question of which one is the rule has no answer.

Three details that are easy to leave out and expensive to leave out:

- **The commit message is history.** A file-content scan cannot see it, so there is a second hook rather than a cleverer first one.
- **The escape hatch is a line marker, `oem-allow: <reason>`.** It is how a test can name an identifier in order to assert its absence, and it makes every real identifier a deliberate, reviewable choice instead of an accident. Exemptions are enumerated in the guard's output, never applied silently, because an invisible exemption is how a marker becomes a way to mute the check. In a commit message the marker is a trailer and covers the whole message, since the identifier is normally in the subject while the trailer sits at the bottom.
- **The guard fails loudly with its denylist absent.** Exit 2, not exit 0. A guard that passes without its list reports success it has not earned, which is worse than no guard because something now depends on it.

### The test that tests the guard

A hook has to be installed, is not cloned as an active hook, and is bypassed by `git commit --no-verify`. All three are reasons a hook is fast feedback and not the thing that holds. `tests/test_repo_identity.py` needs no install step, travels with the clone, and cannot be waved through with a flag. It also contains the test that proves the pattern bites, on the principle that a guard nobody has seen fail is not a guard: a pass has to mean "nothing found" rather than "the scan silently did nothing".

### Install

```sh
git config core.hooksPath .githooks        # activate both hooks in this clone
cp tools/identity-denylist-private.example.txt tools/identity-denylist-private.txt
# edit that file: your tokens, one per line
bash tools/generate-identity-hashes.sh     # regenerate the tracked hash file
python3 -m unittest discover -s tests -v   # the guard, proving itself
```

The repository ships with four fictional tokens in the example source so the guard works, and its tests pass, in a fresh clone. Replace them. The generator refuses an entry below a five-character floor, because a short prefix blocks half the vocabulary, and it hard-fails on a collision with anything already legitimately tracked rather than quietly blocking it.

## What is coming, and when

This repository is the third of three parts. The other two are specified and not yet here, which is said plainly rather than left for a reader to discover.

**Part 1, a skill-trigger eval suite.** A corpus of realistic user phrasings, including the near-misses and the explicit anti-triggers the skill descriptions already anticipate, scored for whether the right skill fires. Precision and recall per skill. This is agent-behaviour testing, not domain testing, and there is very little published work on it.

**Part 2, a measured cost signal for the scheduled agents, and a plain account of what could not be measured.** A controlled A/B on a fixed task, run attended so the token counts are real, measuring the effect of the rule that stopped agents reading long files whole. Alongside it, a per-run record across the scheduled agents that are live, capturing bytes read into context, duration, and files read. Bytes are a proxy and are labelled as one throughout: a scheduled run cannot observe its own token counts, and cost is an account fact rather than a run fact, so no per-run cost figure is published here. The fleet was never instrumented and there is no historical baseline to recover, so the record begins on 25 September 2026 and is reported with its n, which is a capture window and not a profile.

**Both land by Friday 2 October 2026.**

## The method

Described here rather than dumped, because the files themselves are working documents rather than a publishable framework.

**CRIT** is the brief format: Context, Role, Interview, Task. The step that does the work is **Interview**, and it is assigned to the model rather than to the person writing the brief. The model asks its questions before it starts, which is where most of the value is, because the questions surface the assumptions the brief did not know it was making. **Context** carries a required **Constraints** field, added 2026-09-24: enumerate what is in force, then name which of those actually bear on this task. Enumerating without selecting is how a constraints list becomes decoration.

**The flagging protocol** has two halves that are usually run together and should not be. *Flag freely*: raise anything that looks inconsistent, risky or possibly wrong, because a wrong flag is cheaper than a missed one. *Diagnose tentatively*: raise it as a question rather than a verdict, because a confident wrong cause is more expensive than no cause at all. It also carries a stagnation protocol for the case where an agent is going round the same loop, which is the failure mode that burns a budget with nothing to show.

**The handoff contract** is the part that is genuinely a contract rather than a convention. A session ends by writing a mandatory `## Continue here` section, and a separate downstream agent lifts that section by name. It is a machine-readable interface between two agents, not a notes folder that a human is trusted to have read.

## Share-safe statement

This repository reports method and publishes one working pattern. It intentionally excludes private IP, client-sensitive context, and the plaintext denylist the guard is built around. The identity guard was run over every file here before publication, in its strictest mode, with the escape hatch disabled. The tokens in the example denylist are fictional. The history starts clean by construction, not by tidying: the first commit is the first commit, and nothing was cloned in from a private repository.

## Provenance and licence

Written by Sue Holder. The identity guard was extracted from a private working repository and genericised for publication: the repository names, the private sibling path and the real denylist were replaced, and the test probes were rewritten to fictional tokens. The pattern is unchanged.

Licensed under the Apache Licence, Version 2.0. See `LICENSE`.

The publicity declaration for this repository lives in its own `CLAUDE.md`, per the house rule that a repository states its intent in one line where a session opened directly on it will see it.
