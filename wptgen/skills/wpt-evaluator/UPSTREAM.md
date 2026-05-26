# Upstream provenance

The rules in `references/rules.yaml` are currently derived from the `docs/`
tree of the upstream `web-platform-tests/wpt` repository. Rules from
wpt-gen's own style guides may be added in a later pass; provenance is
tracked per rule via the `source` field.

## Source path convention

The `source` field on each rule is a repo-root-relative path whose first
segment names the originating repository:

- `wpt/...` — paths into upstream `web-platform-tests/wpt` (e.g.,
  `wpt/docs/writing-tests/general-guidelines.md#L82-L87`).
- `wpt-gen/...` — paths into this repository (e.g.,
  `wpt-gen/wptgen/skills/wpt-generator/references/testharness_style_guide.md#L124`).

A `#L<start>-L<end>` line anchor is appended where the source location is
stable.

## Pinned upstream commit

- Repository: https://github.com/web-platform-tests/wpt
- Commit: `255065af5cc7d18e891ff558024eca5623a0b6ac`
- Date: 2026-05-25

## Upstream source documents

Rules currently draw from:

- `wpt/docs/writing-tests/general-guidelines.md`
- `wpt/docs/writing-tests/testharness.md`
- `wpt/docs/writing-tests/file-names.md`
- `wpt/docs/writing-tests/reftests.md`
- `wpt/docs/writing-tests/idlharness.md`
- `wpt/docs/writing-tests/manual.md`
- `wpt/docs/writing-tests/assumptions.md`
- `wpt/docs/reviewing-tests/checklist.md`

## Refresh procedure

When upgrading to a newer upstream commit:

1. `git -C ../wpt pull`
2. Re-read each source document listed above; check for added, removed, or
   reworded normative statements.
3. Update `references/rules.yaml`: add new rules, deprecate removed ones, and
   reword existing ones whose source language has changed. Bump the `source`
   line numbers if they have shifted.
4. Update the pinned commit hash and date in this file.
5. Re-run the calibration regression suite (see the RFC for details) and
   record any per-rule agreement changes.
