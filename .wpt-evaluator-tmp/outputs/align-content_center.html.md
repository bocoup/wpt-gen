# Evaluation: css/css-flexbox/align-content_center.html

## Input scope

| File                                                                              |     Bytes | Role        |
| --------------------------------------------------------------------------------- | --------: | ----------- |
| wptgen/skills/wpt-evaluator/SKILL.md                                              |     7,475 | skill       |
| wptgen/skills/wpt-evaluator/references/rules.yaml                                 |    50,132 | rules       |
| ../wpt/css/css-flexbox/align-content_center.html                                  |       968 | test        |
| ../wpt/css/css-flexbox/reference/align-content_center-ref.html                    |       580 | dependency  |
| ../wpt/css/css-flexbox/support/test-style.css                                     |       342 | dependency  |
| **Total**                                                                         | **59,497** |             |

Declared dependencies (not read): none classified as framework or external. The
only external-style URLs are `<link rel="author" href="http://www.intel.com">`
and `<link rel="help" href="http://www.w3.org/TR/css-flexbox-1/#align-content-property">`
which are metadata URLs, not loaded resources.

Local dependencies read:
- `reference/align-content_center-ref.html` — read to evaluate STRUCT-002 and
  STRUCT-003 (whether the reference uses the technology under test and whether
  it uses a different technique).
- `support/test-style.css` — read to evaluate STRUCT-013/STRUCT-014 (the test's
  prose mentions a "red rectangle" with no red declared in the test file
  itself, so the shared stylesheet had to be inspected to confirm whether the
  rendering convention is met).

Approach: distilled-yaml
Approximate input tokens: ~14,874
Total session usage: 61.2k

## Detected test kind

- `reftest` (has `<link rel="match" href="reference/align-content_center-ref.html">`)
- `css` (lives under `css/css-flexbox/`)
- `html`

Not testharness, not manual, not crashtest, not visual, not idl, not wdspec.

## Findings

### STRUCT-002 — warn — reference uses the technology under test (partially)

- Line: [reference/align-content_center-ref.html:7-15](../../../wpt/css/css-flexbox/reference/align-content_center-ref.html#L7-L15)
- Evidence (reference file, lines 7-15):
  ```
  #test {
    height: 200px;
    width: 80px;
  }
  #spacer {
    width: 50px;
    height: 25px;
  }
  ```
- The reference avoids `display: flex` / `align-content` (good — the technology
  under test is not used). However the reference depends on the shared
  stylesheet `support/test-style.css`, which sets `width: 50px; height: 50px`
  on `#test01..#test03` — three 50px boxes inside an 80px-wide container will
  visually stack in normal block flow only because each box's width is less
  than the container width. The reference's vertical centering is produced by
  a 25px-tall `#spacer` block above the three 50px boxes (25 + 150 = 175, with
  25px slack below) — this is a legitimate non-flexbox technique. The rule is
  largely satisfied, but flagged as a soft warn because the reference's
  correctness depends on shared stylesheet rules that are also consumed by the
  test, making the reference less robust than one that re-declared its own
  styles inline.
- Source: `wpt/docs/writing-tests/reftests.md#L32-L35`

### STRUCT-003 — info — reference uses a different technique

- Line: [reference/align-content_center-ref.html:21](../../../wpt/css/css-flexbox/reference/align-content_center-ref.html#L21)
- Evidence: reference uses normal block layout with a 25px `#spacer` div to
  push the three 50px boxes downward, achieving centering without flexbox.
  The test uses `display: flex; flex-wrap: wrap; align-content: center`.
- This is reported as an `info`-level satisfaction rather than a violation —
  the different-technique requirement is met.
- Source: `wpt/docs/reviewing-tests/checklist.md#L85-L88`

### STRUCT-009 — nit — self-describing statement is imprecise

- Line: [align-content_center.html:21-23](../../../wpt/css/css-flexbox/align-content_center.html#L21-L23)
- Evidence:
  ```
  <p>Test passes if:<br>
  1. the rectangle 1, 2, 3 show up in a vertical column in a red rectangle and no gap between them.<br>
  2. the rectangle 1, 2, 3 appear in middle left of red rectangle.</p>
  ```
- "middle left of red rectangle" is vague — a reviewer cannot tell from this
  text alone what the exact pass condition is without knowing the dimensions
  of the red rectangle. "Vertical column" plus "middle left" is also
  redundant for an 80px container holding 50px boxes. The statement is
  understandable but not precise; "the three rectangles are vertically
  centered within the red rectangle" would be clearer.
- Source: `wpt/docs/reviewing-tests/checklist.md#L95-L104`

### STRUCT-013 — warn — rendering does not use the canonical green-square / red-fail convention

- Line: [align-content_center.html:11-17](../../../wpt/css/css-flexbox/align-content_center.html#L11-L17) and shared stylesheet `support/test-style.css`
- Evidence: the three test boxes are colored chartreuse (`#7FFF00`), cyan
  (`#00FFFF`), and royal blue (`#4169E1`) on a red (`#ff0000`) container. The
  rendering test guideline recommends using green to indicate pass and red to
  expose failures.
- This is a reftest, so pass/fail is determined by image comparison rather
  than by color convention; the rule is a soft guideline for tests where
  visual readability matters. Reported as `warn` because the test deviates
  from the convention but is still functional.
- Source: `wpt/docs/writing-tests/rendering.md#L8-L24`

### FOCUS-003 / STRUCT-009 — warn — instructions describe a pass condition for a manual viewer, not for reftest comparison

- Line: [align-content_center.html:21-23](../../../wpt/css/css-flexbox/align-content_center.html#L21-L23)
- Evidence: the test contains step-by-step pass instructions ("Test passes
  if: 1. ... 2. ...") that look like manual-test instructions. The same text
  also appears in the reference file (lines 18-20 of the reference). For a
  reftest, the pass condition is "test image matches reference image", so
  these instructions are decorative — they are not consulted by the reftest
  runner. They are not incorrect, but their presence in a reftest is
  unusual and can confuse a reader into thinking the test is manual.
- Source: `wpt/docs/writing-tests/general-guidelines.md#L170-L174`

### META-007 — info — `<meta name="assert">` content overlaps with title

- Line: [align-content_center.html:4](../../../wpt/css/css-flexbox/align-content_center.html#L4) and [align-content_center.html:9](../../../wpt/css/css-flexbox/align-content_center.html#L9)
- Evidence:
  - Title (line 4): `CSS Flexible Box Test: align-content_center`
  - Assert (line 9): `Check if the web engine can identify the align-content value center.`
- The assert text is not literally a copy of the title, but is a near-paraphrase
  ("align-content_center" ↔ "align-content value center"). It does not add
  significant information beyond the title.
- Source: `wpt/docs/writing-tests/css-metadata.md#L156-L168`

### FMT-001 — info — no `<meta charset>` declared (file is pure ASCII, so compliant)

- Line: [align-content_center.html:1-19](../../../wpt/css/css-flexbox/align-content_center.html#L1-L19)
- Evidence: the file declares no `<meta charset="utf-8">`. The file contains
  only ASCII characters, so the rule's "or be pure ASCII" clause is satisfied.
  Listed as `info` for traceability, not a violation.
- Source: `wpt/docs/writing-tests/general-guidelines.md#L82-L87`

### META-005 — info — satisfied

- Line: [align-content_center.html:6](../../../wpt/css/css-flexbox/align-content_center.html#L6)
- Evidence: `<link rel="help" href="http://www.w3.org/TR/css-flexbox-1/#align-content-property" />`
- The CSS-test requirement of at least one `<link rel="help">` is met.
- Source: `wpt/docs/writing-tests/css-metadata.md#L5-L12`

### STRUCT-001 — info — satisfied

- Line: [align-content_center.html:7](../../../wpt/css/css-flexbox/align-content_center.html#L7)
- Evidence: `<link rel="match" href="reference/align-content_center-ref.html">`
- Reftest link element is present and points to an existing reference file.
- Source: `wpt/docs/writing-tests/reftests.md#L25-L29`

### STRUCT-005 — info — reference naming follows convention

- Line: [align-content_center.html:7](../../../wpt/css/css-flexbox/align-content_center.html#L7)
- Evidence: reference path is `reference/align-content_center-ref.html`. The
  test is `align-content_center.html`, and the reference uses a `-ref` suffix
  and lives in a `reference/` directory. The recommendation says single-test
  references use the test name plus `-ref`. Convention satisfied.
- Source: `wpt/docs/writing-tests/reftests.md#L46-L55`

### NAME-002 — nit — filename uses underscore separator inconsistent with WPT convention

- Line: filename
- Evidence: `align-content_center.html`. WPT's filename convention prefers
  hyphenated descriptive names (e.g., `align-content-center.html` or
  `align-content-center-001.html`). Mixing a hyphen and an underscore in the
  same name is unusual and inconsistent with the documented
  `test-topic-001.html` pattern.
- Source: `wpt/docs/writing-tests/general-guidelines.md#L15-L22`

### PORT-004 — info — viewport assumption met implicitly

- Test fits well within an 800x600 viewport (container is 200x80). Satisfied.
- Source: `wpt/docs/writing-tests/assumptions.md#L6-L8`

## Rules considered but not flagged

The following applicable rules were evaluated and produced no finding:

- FMT-001 (file format / encoding) — listed above as info.
- META-005, META-006 (help link presence and ordering) — single help link
  present; ordering is trivially satisfied.
- STRUCT-004 (800x600 viewport) — satisfied; test is 80x200.
- STRUCT-006 (multiple-references semantics) — only one reference declared.
- STRUCT-007 (`reftest-wait`) — no DOM manipulation needed; not applicable.
- STRUCT-008 (`fuzzy`) — not declared; only needed when anti-aliasing differs.
- API-006..API-009 (testdriver) — testdriver not used.
- PORT-001 / REV-001 (external resources) — only the `<link rel="help">` and
  `<link rel="author">` URLs are external; these are metadata, not loaded.
- PORT-003 (fonts) — no custom fonts; only plain digit glyphs in the test boxes.
- PORT-006 (hostnames/ports) — no server URLs hardcoded.
- REV-002 (proprietary features) — none used.
- REV-003 (commented-out code) — none.
- FOCUS-001 (shortness) — test is short and minimal.
- FOCUS-004 (passes when implemented correctly, fails otherwise) — the test
  is constructed such that `align-content: center` produces the centered
  layout that matches the reference; a UA without flexbox support, or one
  that does not implement `align-content: center`, will produce a different
  layout and fail the image comparison. Satisfied.

## Notes on rubric calibration

Issues worth tracking for future rubric refinement:

1. **STRUCT-002 borderline**: The current rule text says the reference
   "should not use the technology under test". The reference here doesn't —
   but it depends on a shared stylesheet that is also used by the test. The
   rubric may want a sub-rule about whether dependency sharing between test
   and reference is acceptable, or whether references should re-declare their
   own styles to remain robust if the test stylesheet changes.

2. **Reftest vs. manual-style prose**: The "Test passes if:" instructions in
   both test and reference are leftover from a manual-test style of writing,
   even though this is a reftest. The rubric currently has no rule that
   specifically calls out "reftest contains manual-test instructions" — it
   gets flagged here under FOCUS-003 / STRUCT-009 but is really a distinct
   anti-pattern worth its own rule.

3. **NAME-002 specificity**: The rule discourages "very generic names like
   `001.html`" and mentions a `test-topic-001.html` format, but does not
   explicitly forbid underscore-vs-hyphen mixing. The filename
   `align-content_center.html` is descriptive (so the rule's primary
   concern is met), and the underscore-vs-hyphen objection is a stylistic
   inference. Worth tightening if WPT enforces hyphens-only.

4. **No rule for "self-test of UA capability"**: The test relies on the UA
   actually implementing flexbox to fail correctly. If a UA renders
   `display: flex` as `display: block`, the three 50px boxes will still
   stack vertically (because they exceed the 80px container width) but
   will not be vertically centered — so the test would still fail in that
   case. The test passes when implemented correctly and fails otherwise,
   which satisfies FOCUS-004, but the analysis to confirm this is
   non-trivial. A rule prompting reviewers to verify the failure mode
   explicitly might be useful.
