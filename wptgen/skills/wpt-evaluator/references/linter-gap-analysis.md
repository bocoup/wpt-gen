# Deterministic rules: linter gap analysis

Every rule in [`rules.yaml`](rules.yaml) carries a `layer` field:

- `deterministic` — decidable from a file's bytes, structure, or path
  (regex/AST checkable).
- `semantic` — requires rendering or human-style judgment.

The `deterministic` rules split further by whether upstream `wpt lint`
already enforces them. This document records that split so contributors
know which rules are checked where, and so the split can be re-verified
on each upstream refresh.

This analysis was performed against upstream's rule inventory at
`wpt/tools/lint/rules.py` (plus the detection logic in
`wpt/tools/lint/lint.py`) as of the commit pinned in
[`UPSTREAM.md`](../UPSTREAM.md). **Both the corpus and the upstream linter
change independently, so this mapping is not permanent — re-check it on
every refresh** (see the refresh procedure in `UPSTREAM.md`).

## Covered by upstream `wpt lint` — not reimplemented

The evaluator skips these to avoid double-flagging (see `SKILL.md`, "skip
anything covered by `wpt lint`"). wpt-gen does not re-check them.

| rules.yaml | upstream lint rule |
| ---------- | ------------------ |
| FMT-002    | `MISSING-TESTHARNESSREPORT` / `MULTIPLE-TESTHARNESS` |
| FMT-003    | `TESTHARNESS-PATH` / `TESTHARNESS-IN-OTHER-TYPE` / `EARLY-TESTHARNESSREPORT` |
| NAME-001   | `PATH LENGTH` |
| NAME-003   | `DUPLICATE-BASENAME-PATH` / `DUPLICATE-CASE-INSENSITIVE-PATH` |
| NAME-010 / NAME-013 | `CONTENT-MANUAL` / `CONTENT-VISUAL` |
| META-004   | `VARIANT-MISSING` / `MALFORMED-VARIANT` |
| META-005   | `MISSING-LINK` |
| API-006    | `MISSING-TESTDRIVER-VENDOR` / `MULTIPLE-TESTDRIVER` / `TESTDRIVER-PATH` |
| STRUCT-007 | `MISSING-REFTESTWAIT` |
| STRUCT-001 (partial) | `NON-EXISTENT-REF` / `SAME-FILE-REF` / `ABSOLUTE-URL-REF` |
| PORT-006 (partial)   | `W3C-TEST.ORG` / `WEB-PLATFORM.TEST` (hardcoded-host strings only) |

## Gap rules — implemented in the linter extension

Deterministic rules upstream lint does **not** cover, **and** which have a
clean, low-false-positive check. These are the subject of
[`wptgen/lint_ext.py`](../../../lint_ext.py), where each check is named
with its `rules.yaml` id so the linter and the LLM evaluator share one
identifier space.

| rules.yaml | severity | check |
| ---------- | -------- | ----- |
| FMT-004    | error | `.worker.js` must `importScripts` testharness.js + call `done()` (content, gated on `.worker.js`) |
| NAME-004   | error | `-manual` must be the last `-` element before the extension (filename) |
| NAME-006   | warn | `.window`/`.worker`/`.any` must be immediately before the final `.js` (filename) |
| NAME-011   | error | `-crash` must be immediately before the extension, unless under `crashtests/` (filename) |
| NAME-012   | error | `-print` must be immediately before the extension, unless under `print/` (filename) |
| META-008   | warn | `<meta name=flags>` uses a deprecated CSS token (line) |
| API-005    | error | manual testharness `setup()` lacks `{explicit_timeout: true}` (line, gated on `-manual`) |
| REV-003    | warn | commented-out code (line, conservative regex) |

## Not implemented — left to the LLM judge

Reclassified to `layer: semantic` in `rules.yaml`. Two reasons a rule
lands here:

**Requires rendering or intent judgment** — not decidable from bytes:

- **STRUCT-004** — "render within 800×600" (requires rendering)
- **STRUCT-006** — reftest match/mismatch pass semantics (runtime)
- **REV-007** — "fixed, static page with no animation" (requires rendering)
- **PORT-003** — Ahem when "a known font is needed" (intent judgment)
- **NAME-007** — whether a test *requires* HTTPS is semantic; no fixed API
  list decides it, and scanning full content for that proxy is slow and
  incomplete.

**No clean deterministic signal** — checkable in principle, but a byte-level
check would be too noisy or false-positive-prone to be worth it:

- **NAME-005** — feature-flag vs. type-flag ordering: real filenames mix `-`
  and `.` delimited tokens (e.g. `foo-visual.manual.html`), so violations
  are not cleanly expressible.
- **STRUCT-008 / META-009** — `fuzzy` / `reftest-pages` well-formedness: real
  content uses positional `range;range` forms and template placeholders that
  a strict validator would false-positive on.
- **META-001 / META-002 / META-003** — recommend `// META: title/script/timeout`:
  flagging the *absence* of an optional-but-recommended directive is high-noise
  and closer to a judgment call.
- **API-002 / API-008 / API-009** — conditional includes ("to use X, include
  Y"): only apply *if* the test uses that API, which is itself a content/intent
  judgment.
- **PORT-008** — the `.headers` sibling-file convention describes how to set
  headers; there is no clear violation to detect.
- **REV-006** — "one blank line between tests" is a `nit` requiring
  test-block boundary parsing for marginal value.

## Why the split falls where it does

Upstream `wpt lint` checks structural/syntactic *presence* (does a manual
test's filename end in `-manual`? are there multiple timeouts? is a
metadata key valid?). It does not enforce the authoring *recommendations*
that many deterministic rules encode. The gap set is that
deterministic-but-unlinted remainder.
