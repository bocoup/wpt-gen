# Upstream provenance

In this variant (`wpt-eval-doc-inputs`), the evaluator reads the upstream
`web-platform-tests/wpt` documentation tree directly, rather than a
distilled `rules.yaml`. Findings cite the upstream doc path + line range
that prompted each flag.

## Source path convention

Findings cite sources as repo-root-relative paths whose first segment
names the originating repository:

- `wpt/...` — paths into upstream `web-platform-tests/wpt` (e.g.,
  `wpt/docs/writing-tests/general-guidelines.md:L82-L87`).
- `wpt-gen/...` — paths into this repository (reserved for future use if
  wpt-gen-specific guidance is layered on top of upstream).

A `:L<start>-L<end>` line anchor is appended where the source location is
stable.

## Pinned upstream commit

- Repository: https://github.com/web-platform-tests/wpt
- Commit: `255065af5cc7d18e891ff558024eca5623a0b6ac`
- Date: 2026-05-25

The local clone is expected at `../wpt/` (one level above this repo).

## Upstream source documents

The evaluator's curated reading lists in [`SKILL.md`](SKILL.md) refer to
the following upstream docs:

- `wpt/docs/writing-tests/general-guidelines.md`
- `wpt/docs/writing-tests/testharness.md`
- `wpt/docs/writing-tests/file-names.md`
- `wpt/docs/writing-tests/reftests.md`
- `wpt/docs/writing-tests/print-reftests.md`
- `wpt/docs/writing-tests/idlharness.md`
- `wpt/docs/writing-tests/manual.md`
- `wpt/docs/writing-tests/crashtest.md`
- `wpt/docs/writing-tests/visual.md`
- `wpt/docs/writing-tests/wdspec.md`
- `wpt/docs/writing-tests/testdriver.md`
- `wpt/docs/writing-tests/assumptions.md`
- `wpt/docs/writing-tests/rendering.md`
- `wpt/docs/writing-tests/server-features.md`
- `wpt/docs/writing-tests/css-metadata.md`
- `wpt/docs/reviewing-tests/checklist.md`

## Refresh procedure

When upgrading to a newer upstream commit:

1. `git -C ../wpt pull`
2. Skim the docs above for added, removed, or reworded normative
   statements. (No structured rules file needs syncing in this variant —
   the docs themselves are the source of truth.)
3. Update the pinned commit hash and date in this file.
4. Re-run any calibration regression suite and record changes in
   per-finding behavior.
