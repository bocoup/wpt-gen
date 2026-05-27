# Findings: css/css-flexbox/align-content_center.html

## Input scope

| File                                                                  |     Bytes | Role         |
| --------------------------------------------------------------------- | --------: | ------------ |
| wptgen/skills/wpt-evaluator/SKILL.md                                  |     7,722 | skill        |
| wpt/docs/writing-tests/general-guidelines.md                          |     9,253 | reading-list |
| wpt/docs/writing-tests/file-names.md                                  |     2,628 | reading-list |
| wpt/docs/writing-tests/assumptions.md                                 |     1,949 | reading-list |
| wpt/docs/writing-tests/server-features.md                             |     6,141 | reading-list |
| wpt/docs/reviewing-tests/checklist.md                                 |     4,767 | reading-list |
| wpt/docs/writing-tests/reftests.md                                    |     7,639 | reading-list |
| wpt/docs/writing-tests/rendering.md                                   |     3,405 | reading-list |
| wpt/docs/writing-tests/css-metadata.md                                |     5,407 | reading-list |
| wpt/css/css-flexbox/align-content_center.html                         |       968 | test         |
| wpt/css/css-flexbox/reference/align-content_center-ref.html           |       580 | dependency   |
| wpt/css/css-flexbox/support/test-style.css                            |       342 | dependency   |
| **Total**                                                             | **50,801** |              |

Declared dependencies (not read): none classified as framework/external.
Local dependencies read:
- `reference/align-content_center-ref.html` — read to evaluate the
  reftest guidance that "the reference file should use a different
  technique that won't fail in the same way as the test"
  (reftests.md, checklist.md "Reftests Only").
- `support/test-style.css` — read because both test and reference
  include it; needed to determine whether the shared stylesheet
  carries any of the flex-layout logic that is under test.

Approach: doc-inputs
Approximate input tokens: ~12,700
Total session tokens: 58.8k

## Findings

### Finding 1 — missing character encoding declaration

- **Severity**: warn
- **Test line**: 1–4 (no `<meta charset>` anywhere in `<head>`)
- **Evidence**:
  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <title>CSS Flexible Box Test: align-content_center</title>
  ```
- **Source**: `wpt/docs/writing-tests/general-guidelines.md:L82-L87`
- **Summary**: Except when specifically testing encoding, files must
  be encoded in UTF-8, and in file formats where UTF-8 is not the
  default (HTML) they must contain metadata to mark them as such
  (e.g., `<meta charset=utf-8>`) or be pure ASCII. The file is ASCII
  today, so this does not break anything in practice, but the
  required marker is absent.

### Finding 2 — filename uses underscore instead of the recommended dash form

- **Severity**: nit
- **Test line**: n/a (filename: `align-content_center.html`)
- **Evidence**: filename `align-content_center.html`
- **Source**: `wpt/docs/writing-tests/general-guidelines.md:L15-L22`
- **Summary**: The recommended filename format is
  `test-topic-001.html` — a short hyphen-separated topic optionally
  followed by an incremental three-digit suffix. This file mixes
  hyphens (`align-content`) with an underscore (`_center`) instead of
  the documented hyphenated form (e.g., `align-content-center.html`
  or `align-content-001.html`).

### Finding 3 — self-describing statement is wordier than necessary

- **Severity**: nit
- **Test line**: 21–23
- **Evidence**:
  ```html
  <p>Test passes if:<br>
  1. the rectangle 1, 2, 3 show up in a vertical column in a red rectangle and no gap between them.<br>
  2. the rectangle 1, 2, 3 appear in middle left of red rectangle.</p>
  ```
- **Source**: `wpt/docs/reviewing-tests/checklist.md:L99-L104`
- **Summary**: The self-describing statement should be "accurate,
  precise, simple, and self-explanatory. Someone with no technical
  knowledge should be able to say whether the test passed or failed
  within a few seconds." The two-clause instruction here is parseable
  but mixes layout ordering and positioning into a single sentence
  per clause; a tighter statement would reduce the time a reviewer
  spends mapping the prose onto what they see.

### Finding 4 — title contains the filename verbatim rather than a descriptive phrase

- **Severity**: nit
- **Test line**: 4
- **Evidence**:
  ```html
  <title>CSS Flexible Box Test: align-content_center</title>
  ```
- **Source**: `wpt/docs/reviewing-tests/checklist.md:L73-L75`
- **Summary**: The checklist nit asks that the title be "descriptive
  but not too wordy." `align-content_center` is the filename
  verbatim (including the underscore), not a description of the
  property/value combination being tested (e.g., "align-content:
  center on a multi-line flex container").

## Notes for rubric validation

Items checked and found compliant (not raised as findings):

- **Reftest uses a different technique** (reftests.md:L32-L36,
  checklist.md:L86-L88): the test uses `display: flex` with
  `align-content: center`; the reference uses static block layout
  plus a fixed-height `#spacer` div to push the visible children to
  the vertical center. Different technique — good.
- **Shared support stylesheet** (`support/test-style.css`): used by
  both test and reference. The stylesheet only sets background
  colors and child box dimensions — it does not encode any of the
  flex layout under test — so sharing it does not cause the
  reference to "fail in the same way as the test."
- **Required `<link rel="help">` for CSS tests** present
  (css-metadata.md:L7-L13).
- **`<meta name="assert">`** present and non-trivial
  (css-metadata.md:L150-L188).
- **Viewport fits 800×600** (checklist.md:L91-L93,
  assumptions.md:L1-L6): test fixture is 80×200px.
- **No external network resources**, no proprietary features, no
  commented-out code (checklist.md:L43-L54).
- **Reference file exists** at the path declared by
  `<link rel="match">` (reftests.md "Reference existence").

Items deliberately not flagged because `wpt lint` already covers
them (per SKILL.md procedure step 4):

- Tab characters in the inline `<style>` on test lines 12, 15, 16,
  17 (mixed with space indentation on lines 13 and 14). Lint
  enforces "use spaces rather than tabs for indentation"
  (general-guidelines.md:L177-L185).
- Trailing whitespace / CR line endings (if any).

### Rubric observations

1. **Grounding**: each finding cites both a test line and an upstream
   doc location. Finding 3 (self-describing statement) is the most
   subjective — the upstream language is "simple and self-explanatory"
   rather than a hard rule, so a reviewer could reasonably disagree
   with the nit-level call.
2. **Coverage gap**: upstream docs do not give explicit guidance on
   filename punctuation beyond "hyphen-separated test-topic-NNN," so
   Finding 2 leans on the example rather than a normative MUST. A
   future thin rules layer could make this concrete.
3. **Coverage gap**: nothing in the curated reading list discusses
   sharing a support stylesheet between test and reference, even
   though that is a common reftest pattern with real failure modes
   (a bug in the support file would mask itself). Worth upstreaming.
