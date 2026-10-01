# Part 2: a measured cost signal, and what could not be measured

Two things are here. A controlled A/B on one rule, run attended so the app's own readouts could be taken, and a per-run record across the scheduled agents that are live. Both are small. Each is reported with its n, and each says what it cannot show before a reader has to find out.

## The A/B: one rule, one task, one prompt

### What was tested

One of the scheduled agents carries a rule that says, in short, never read a long file whole: grep for headings and read a slice. The A/B ran the log-reading part of that agent's own task twice, once with the rule and once without, on a frozen copy of the file it reads.

| | |
|---|---|
| Task | read the last three dated entries of a long working log, extract each day's type, its count of completed bullets and every `Releases:` line, and write one summary entry |
| Input | a frozen copy of the log, 1,179,571 bytes, 6,826 lines, sha256 `a6bbbe31f4e2ee03c932e15c5334e7cda34510bb27b8c71966923ee868e7ae88` |
| The only difference between the arms | the rule block, verbatim from the live prompt: [`rule-block.diff`](rule-block.diff), four lines added, none removed |
| Model and settings | Opus 5.5 as the app's selector names it, Medium effort, the same in both arms |
| Surface | the Claude desktop app, Code tab, one fresh session per arm, nothing else run in it |
| Date | 30 September 2026, run in sequence, A then B |
| n | **1 per arm** |

The input is private: it is a working log and names clients and people. Its size and fingerprint are published so the record can later show that both arms read the identical file and that it was not swapped. **A reader cannot re-run this test.** The full prompt is private for the same reason; the diff between the arms is the whole of what was varied, and it is published.

### What happened, per run

| | Arm A, with the rule | Arm B, without the rule |
|---|---|---|
| Bytes read from the input (a proxy, see below) | 4,090 | 3,931 |
| Reads of the input | 4 | 1 |
| Tool calls | 5 | 2 |
| Duration, as the app's usage readout reports active time | 41 s | 35 s |
| Read the file whole | no | no |
| Wrote the entry, with all three days | yes | yes |

**Neither arm read the file whole.** The arm without the rule did not need telling: asked for the last three entries, it wrote one two-pass extract and read 3,931 bytes. The arm with the rule did what the rule says, step by step, and took four reads and three more tool calls to arrive at almost the same number of bytes. On this task the rule changed how the reading was done, not how much was read.

**Bytes are a proxy, and are labelled as one wherever they appear.** Each arm tallied what came back from each read, not the size of the file it read from. They are not tokens and are never converted into tokens here.

### Where the rule would be expected to matter

This task asks for the last three entries. That is a narrow request, and a capable model answers a narrow request narrowly without a rule to make it. The null result is real, and it is narrow: it says the rule is not needed **on this task**. The rule is aimed at a different situation, a task that tempts a whole-file read, such as "summarise the week" or "check the log for anything unresolved", where the obvious first move is to open the whole file. That situation was not tested here.

One more limit narrows it further. The harness itself caps what a whole-file read returns, so the arm without the rule was never running without protection. It measured "no rule, harness caps still on". Had arm B tried to read the file whole, it would have got back a truncated slice, not 1.18 MB. It did not try, so the cap did not come into play, but it is why even a positive result here could not have been credited to the rule alone.

### Cost, as the app showed it

The arm **with** the rule cost more: **$0.78 against $0.69**, as shown by the app's usage readout for each session. The likely mechanism is the extra tool calls. Each call re-reads the session's cached context, and the app showed 621k cache-read tokens for arm A against 271k for arm B. A rule written to save context cost money on a task where it saved nothing.

These two figures are the app's display for two attended sessions. They are not billed amounts reconciled against an account, and they are the only cost figures in this repository.

### Context tokens: context only

The app reported each session's context at the end of the run: **119k for arm A, 118.1k for arm B**, out of a 1M window. About 118k of each is fixed session overhead (system prompt, tools, instructions) that is present before the task starts, so a context total cannot resolve a difference of a few kilobytes of reading. The figures are recorded and they are not the result. They are context tokens as shown by the app, not tokens billed.

The app's usage readout also shows input and output token counts. **They are not quoted here.** The output figure was 52 for arm A, a session that wrote a 2,524-byte file, which is more than 52 tokens could carry. So that figure is not a session total, and until it is known what it does count, it is not used.

### What this is not

- **Not a fleet result.** The rule lives in one prompt. The other scheduled agents do not carry it.
- **Not a study.** One run per arm. An earlier pair the same morning was voided: both arms stopped to wait for a go before starting, although the prompt said not to ask, so each session carried a second message the task did not specify. Its figures are kept in the private record and not used.
- **Not billed tokens.** Every token figure above is the app's display.
- **Not evidence about where the rule came from.** The rule's own header says it was added because of three silent overnight failures and calls that the "likely cause". When checked against the log, one of the three was a genuine rest day, one has no recorded cause, and one was a provider outage. The rule is sound; its origin story is not established, and this repository's claim that every rule traces to a specific failure does not hold for this one. It is said here so a reader does not have to find it.
- **Not a clean test of the whole block.** The block tells the model to write its output early, "Step 6". The task edition used here has no Step 6, so that sentence points at nothing. It was left verbatim so the arms differ by the block alone; editing it would have been a second difference.

## The per-run record

### What it is

From 25 September 2026, each live scheduled agent appends one line about itself to a tab-separated record when it finishes: duration, bytes read into context, files read, and tool calls. [`run-record.tsv`](run-record.tsv) is that record as of 1 October 2026, 28 runs across five agents, with the agents' free-text notes removed because they describe private work. Rows that only corrected an earlier row are applied rather than published, and the attended A/B rows are reported above rather than here.

### What it cannot carry, and why

**No tokens and no cost, on any row.** A scheduled run cannot observe its own token counts: they are metadata on the response, and they never re-enter the context the model reads. Cost is an account fact, not a run fact; it depends on the plan, the pricing and the cache, none of which a run can see. So those columns are absent, rather than estimated. A bytes figure is never divided by four and published as a token count.

**Every figure is self-reported by the run.** The agent times itself, and counts its own reads and calls. Tool calls in particular are approximate, and are a shape rather than a measurement. Where a run could not total a figure it wrote `-`, and `-` is kept. Unknown is never written as zero.

### What it shows, with its n

| Agent | Runs | Duration, median (range) | Bytes read, runs that reported it | Bytes read, median (range) |
|---|---|---|---|---|
| `morning-review` | 7 | 281 s (145 to 7,352) | 2 of 7 | 171,000 (114,000 to 228,000) |
| `daily-smallest-win` | 7 | 169 s (101 to 257) | 7 of 7 | 17,461 (7,655 to 91,441) |
| `study-on-ramp` | 7 | 33 s (25 to 91) | 7 of 7 | 2,100 (0 to 42,237) |
| `daily-completion-log` | 6 | 188 s (125 to 441) | 1 of 6 | 165,000 |
| `friday-adversarial-audit` | 1 | 852 s | 1 of 1 | 156,254 |

Read it with its n. Seven days is a capture window, not a profile. The longest `morning-review` run continued as an attended session for two hours, which is why its range is wide; the median is the figure to read. Four of the seven `study-on-ramp` runs stopped at their own day gate in under 35 seconds, and a short run is still a run.

**The gap that matters most:** `daily-completion-log` is the agent that carries the rule tested above, and five of its six runs could not total their bytes read. So the record cannot yet show what the rule does in production, which is the question the A/B could only answer narrowly. That is the next thing to fix in the instrumentation, not something to estimate around.

There is no historical baseline. The fleet was never instrumented before 25 September 2026, and there is nothing earlier to recover, so there is no before and after, only a start.

## Share-safe statement

This part reports a method and its numbers. It deliberately excludes the A/B's input file, the full prompts of both arms, the scheduled agents' prompts, and the free-text notes from the per-run record, all of which describe private work, clients and people. What is published of the input is its size and sha256, so a reader cannot re-run the A/B and is told so. The rule block in `rule-block.diff` is verbatim, including the unestablished claim in its header, which is addressed above rather than edited out. The identity guard was run over every file in this directory before it was committed, in its strictest mode, with the escape hatch disabled.
