# Golden PR set

Snapshots of merged WPT PRs that received substantive human review, paired
with a human-verified answer key. Where the **seed** set measures precision on
planted defects and the **corpus** set measures run-to-run consistency, the
**golden** set measures whether the evaluator
find what a human reviewer found — recall against real review comments.

Each golden entry is one WPT test at the exact commit a reviewer commented on,
plus the rule(s) that comment maps to. The harness stages that test, runs the
evaluator, and scores its findings against the reviewer's.

```
golden/
  candidates/     # <pr>.json — machine snapshots (harvested, public-safe)
  annotated/      # <pr>.yaml — the answer key (human-verified)
```

- **`ANNOTATION.md`** — the annotation skill (how a candidate becomes an answer key).

---

## The workflow, end to end

### 1. Harvest candidates

`harvest_wpt_prs.py` walks merged WPT PRs in a date window and snapshots the
ones with substantive review — a `CHANGES_REQUESTED` comment left by a reviewer
(not the author) on a test file. It writes one `candidates/<pr>.json` per
qualifying PR.

There is **no resume cursor**: a run harvests exactly the `--since`/`--until`
window you give it (or a `--pr` set). What has already been harvested is the set
of `candidates/*.json` on disk — `--skip-existing` leaves those untouched. This
keeps the dev/holdout boundary explicit: the window you pass *is* the decision,
not a cursor that silently creeps forward past it.

```bash
# Preview what would be harvested — writes nothing:
python scripts/benchmark/harvest_wpt_prs.py --dry-run

# Extend the dev set: harvest new PRs up to the boundary. --until MUST be
# <= the current dev/holdout boundary (see the model-cutoff table below);
# --skip-existing leaves already-committed candidates untouched.
python scripts/benchmark/harvest_wpt_prs.py \
  --since 2024-12-13 --until <boundary> --max-prs 400 --skip-existing

# Refresh a known set (e.g. after a harvester change) without re-crawling:
python scripts/benchmark/harvest_wpt_prs.py --pr 47302,46734
```

**Every harvest is a logged step.** Before running, confirm `--until` is at or
before the current boundary in the [model-cutoff table](#model--training-cutoff);
after running, append a row to the [harvest log](#harvest-log). The `--until`
guardrail is what keeps a crawl from reaching into the holdout window.

Each candidate records, per reviewed commit: the commented test file's bytes
**at the review commit** (base64), and each comment's author, path, line, and
`html_url`. The commit is GitHub's `original_commit_id` — the state the
reviewer actually saw — so the stored bytes and the comment line numbers
describe the same file. 

> **Vendor exports are filtered out.** `chromium-export`, `webkit-export`,
> `gecko-sync`, etc. dominate the merge feed and carry no in-repo review — the
> harvester drops them, along with bot authors and non-test files.

### 2. Annotate (map comments → rule ids)

A candidate is raw review comments; the answer key needs each comment resolved
to the evaluator's rule vocabulary. Follow [`ANNOTATION.md`](ANNOTATION.md) — it
is a skill an LLM can run — to produce `annotated/<pr>.yaml`: for each comment,
a `rule_id` from `rules.yaml` (semantic-layer rules only) **or** `no-rule` when
the feedback falls outside the distilled rules.

`no-rule` is common and correct — much real review feedback (naming, coverage,
housekeeping) isn't a distilled rule, and a wrong `rule_id` silently poisons
the key. When uncertain, use `no-rule` and note a candidate mapping in a
comment rather than guessing.

### 3. Verify (human)

**The LLM's annotation is a draft, not the answer key.** A human reads each
mapped label against the actual comment and confirms the `rule_id` fits — or
downgrades it to `no-rule`. This is the step that makes the set trustworthy;
it is not optional. Spot-check that each label's `commit_id` and line still
point at the code the comment was about (they should, by construction).

### 4. Score

Golden is a first-class entry type in the benchmark harness — no separate mode.
The loader pairs each `candidates/<pr>.json` with its `annotated/<pr>.yaml`,
stages the test at its review commit, runs the evaluator, and scores findings
against the gold labels.

```bash
# Fast smoke — one or two PRs with a catchable finding, one repeat:
python scripts/benchmark/run_benchmark.py \
  --golden-set smoke --filter role=golden --repeats 1

# The full mapped dev set:
python scripts/benchmark/run_benchmark.py \
  --golden-set mapped --filter role=golden

# Ad-hoc subset, no manifest edit:
python scripts/benchmark/run_benchmark.py \
  --golden-prs 43400,47302 --filter role=golden
```

Named sets (`smoke`, `mapped`, …) live under `golden_sets:` in
`benchmarks/manifest.yaml` — membership only; the commit, bytes, and labels
still come from the on-disk artifacts. `--filter role=golden` restricts the run
to golden entries (otherwise seeds and corpus run too). Scoring is
**recall-focused**: a predicted finding with no matching gold label is *not*
charged as a false positive — it may be a valid finding the human missed (the
input to a future "exceeds-human" measure), so it's reported as an unmatched
prediction, not held against precision.

---

## Dev window vs. holdout — and why annotations are the sensitive part

The value of this set depends on the models under test not having *memorized*
the answers. Two different exposures matter, and they need different defenses.

**The snapshots (`candidates/`) are public by nature.** The PRs, diffs, and
review comments already live on GitHub and get crawled whether or not we mirror
them. Committing them here adds near-zero marginal exposure. Secrecy is not the
defense for these — the **time split** is.

**The annotations (`annotated/`) are the answer key, and they are new
information that exists nowhere else.** This is what should be protected.

So golden PRs fall into two windows by merge date, relative to the earliest
training cutoff among the models under test:

- **Dev window** — PRs merged *before* the cutoff. The models may have seen the
  merged result during training, so there is less to protect by
  hiding the answer key. **These annotations are safe to commit here** — the current
  set (Jul–Dec 2024) is the dev window.
- **Holdout window** — PRs merged *after* the cutoff. The models could not have
  trained on these, so recall here is the honest signal — *provided the answer
  key stays private*. **Holdout annotations must not be committed to this
  public repo.** As a window ages past the next cutoff, it rotates into the dev
  set and its annotations can then be published.

This PR ships only the **dev window**, so everything here is safe to commit.
How maintainers should *store and share* holdout annotations privately is
deliberately left open — that's a policy decision for maintainers to settle
once the overall approach is agreed. The only firm rule is the boundary:
holdout answer keys do not land in this repo.

## The boundary is a decision, not a date — model cutoffs & harvest log

The dev/holdout boundary is **the earliest training cutoff among the models
under test** (`wpt-gen.yml`). It is *not* a fixed date and *not* the newest
model's cutoff — it moves only as far forward as the **oldest** model allows.

**Standing decision: cutoffs are deliberately staggered.** We keep at least one
older-cutoff model under test on purpose, to hold the boundary back and
preserve a large holdout window. Adding newer models is fine; the boundary does
not move as long as an older-cutoff model remains. This is worth doing while
there is no holdout-benchmark process yet — a large holdout is runway we cannot
yet spend, so we protect it.

**Consequence — treat the oldest model as load-bearing.** Removing it, or
bumping it to a later cutoff, moves the boundary forward and **permanently
contaminates** every holdout PR that crosses it (a model, once trained on a PR,
cannot un-see it). So changing the oldest model is a boundary decision logged
below, never a routine config edit.

### Model → training cutoff

Fill from each provider's authoritative documentation; do not guess. The
**minimum** of this column is the current boundary. (Dates are `YYYY-MM`.)

| provider  | model              | training cutoff |
| :-------- | :----------------- | :-------------- |
| gemini    | gemini-3.7-flash   | `TODO`          |
| anthropic | claude-opus-4-6    | `TODO`          |
| openai    | gpt-5.4            | `TODO`          |

**Current boundary (min cutoff): `TODO` — set from the table above.**

### Harvest log

One row per harvest run, appended. It records the boundary the run was
authorized under, so any committed candidate can be traced to the cutoff that
made it dev-window-safe. A run's `--until` must be `<=` the boundary in force.

| date run   | `--since` | `--until` | boundary at run | PRs added | notes                    |
| :--------- | :-------- | :-------- | :-------------- | :-------- | :----------------------- |
| 2024-??-?? | (initial) | (initial) | `TODO`          | 10        | initial dev set, Jul–Dec 2024 |

---

## To-do's

This is a **plumbing-grade** dev set — enough to build and exercise the pipeline
end to end, not yet a headline recall number. Much real review feedback maps to
`no-rule` (it falls outside the distilled rules), so the mapped-label
denominator is modest and some PRs contribute none. A recall-*measuring* set
needs a larger, mostly-holdout harvest.

The most important known limitation is the **multi-file test problem.** Many
WPT tests are split across files — a master entry point that imports a data
table, vectors, and helpers — and reviewers often comment on a *fragment* (the
data table) rather than the master. Staged in isolation, a fragment has no
harness and nothing to judge, so it scores 0 even when the review feedback is
real (#43400, WebCryptoAPI, is the canonical case). Fixing it means staging the
dependency closure and treating the *master* test as the run unit, not the
commented file. Deferred for follow-up work.
