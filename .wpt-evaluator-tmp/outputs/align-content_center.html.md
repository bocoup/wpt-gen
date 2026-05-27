# WPT Evaluator findings — `css/css-flexbox/align-content_center.html`

- **Test kind detected:** reftest (HTML, CSS) — contains `<link rel="match" href="reference/align-content_center-ref.html">`.
- **Applies-to filter used:** rules whose `applies_to` includes any of `reftest`, `html`, `css`, `any`.

Findings are listed by rule ID. Rules without findings are omitted.

---

## NAME-002 — `filename` / nit / semantic

- **Rule:** File names should be descriptive of what is being tested; a common format is `test-topic-001.html` using hyphens. Very generic numeric names are discouraged.
- **Line reference:** filename (path-level).
- **Evidence:** `align-content_center.html` uses an underscore between the property name and the value, rather than the conventional hyphen separator. There is also no `-NNN` ordinal even though sibling tests in this directory follow that pattern.
- **Source:** [wpt/docs/writing-tests/general-guidelines.md#L15-L22](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/general-guidelines.md#L15-L22)

## NAME-003 — `filename` / error / deterministic

- **Rule:** In the `css/` directory, file names must be unique within the whole `css/` directory.
- **Line reference:** filename (path-level).
- **Evidence:** Uniqueness within `css/` cannot be verified from this file alone; flagged for reviewer confirmation. The base name `align-content_center.html` is non-numeric and reasonably distinctive, lowering risk.
- **Source:** [wpt/docs/writing-tests/general-guidelines.md#L28-L30](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/general-guidelines.md#L28-L30)

## META-007 — `metadata` / warn / semantic

- **Rule:** `<meta name="assert">` content must not be a copy of the title, a copy of test verification instructions, a duplicate of another assertion in the suite, or a line from the spec (unless complete out of context).
- **Line reference:** line 9.
- **Evidence:** `<meta name="assert" content="Check if the web engine can identify the align-content value center." />` — this restates the title (`align-content_center`) and the property/value pair already named in the title and `<link rel="help">`, and reads as a phrasing of the title rather than a normative assertion about layout behavior.
- **Source:** [wpt/docs/writing-tests/css-metadata.md#L156-L168](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/css-metadata.md#L156-L168)

## STRUCT-009 — `structure` / nit / semantic

- **Rule:** Reftests should include a self-describing statement that is accurate, precise, simple, and self-explanatory; someone with no technical knowledge should determine pass/fail in seconds.
- **Line reference:** lines 21–23.
- **Evidence:**
  > Test passes if:<br>
  > 1. the rectangle 1, 2, 3 show up in a vertical column in a red rectangle and no gap between them.<br>
  > 2. the rectangle 1, 2, 3 appear in middle left of red rectangle.
  The statement references a "red rectangle" that is not visible in the test file's own rendering (the red background is presumably supplied by `support/test-style.css`). Phrasing such as "the rectangle 1, 2, 3" (singular noun, plural list) is awkward and "middle left" is ambiguous (vertical centering vs. left-aligned positioning).
- **Source:** [wpt/docs/reviewing-tests/checklist.md#L95-L104](https://github.com/web-platform-tests/wpt/blob/master/docs/reviewing-tests/checklist.md#L95-L104)

## STRUCT-013 — `structure` / warn / semantic

- **Rule:** Rendering tests should indicate success with a recognizable visual pattern — typically a green paragraph or a green square. The green square is often layered over a red square so misalignment exposes red.
- **Line reference:** lines 21–23 (and dependent on `support/test-style.css`, not inspected here).
- **Evidence:** The pass condition described is "rectangle 1, 2, 3 … in a red rectangle." Per WPT rendering conventions, red signals failure, not success. The intent here appears to be that red is the *container* background while the inner rectangles are the test subject, but the convention is to use green for the passing visual signature and red as a fail indicator. Reviewer should confirm what colors `test01`/`test02`/`test03` actually render as.
- **Source:** [wpt/docs/writing-tests/rendering.md#L8-L24](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/rendering.md#L8-L24)

## STRUCT-014 — `structure` / warn / semantic

- **Rule:** Rendering tests should be designed so that failures are visually obvious; red is the preferred color for exposing failures.
- **Line reference:** lines 21–24 (and dependent on `support/test-style.css`).
- **Evidence:** Because the test relies on a reftest comparison, visual failure exposure is enforced by the reference rather than by red-bleed within the test. However, the choice to use a "red rectangle" as the *container* (rather than as a fail-exposing underlay) inverts the usual convention. Worth a reviewer's eye to confirm the test isn't structured such that a misalignment failure would still look superficially correct.
- **Source:** [wpt/docs/writing-tests/rendering.md#L37-L59](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/rendering.md#L37-L59)

## STRUCT-002 — `structure` / warn / semantic

- **Rule:** The reference file should be as simple as possible and should not use the technology under test.
- **Line reference:** N/A (refers to `reference/align-content_center-ref.html`, not inspected by this evaluation).
- **Evidence:** Cannot be evaluated from the test file alone. Reviewer should confirm the reference does not also use `display: flex` to achieve the same layout.
- **Source:** [wpt/docs/writing-tests/reftests.md#L32-L35](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/reftests.md#L32-L35)

## STRUCT-003 — `structure` / warn / semantic

- **Rule:** The reference file should use a different technique from the test, so a shared bug doesn't cause both to fail the same way.
- **Line reference:** N/A (refers to reference file).
- **Evidence:** Cannot be evaluated from the test file alone. Reviewer should confirm the reference uses absolute/block positioning rather than flexbox.
- **Source:** [wpt/docs/reviewing-tests/checklist.md#L85-L88](https://github.com/web-platform-tests/wpt/blob/master/docs/reviewing-tests/checklist.md#L85-L88)

## STRUCT-004 — `structure` / warn / deterministic

- **Rule:** The test and reference must render within an 800x600 viewport, only displaying scrollbars if their presence is being tested.
- **Line reference:** lines 10–18, 24.
- **Evidence:** The test container is 80px × 200px — comfortably inside an 800×600 viewport. The descriptive paragraph (lines 21–23) is short and unlikely to cause scrollbars. Likely passes; flagged informationally because final rendering depends on `support/test-style.css`.
- **Source:** [wpt/docs/reviewing-tests/checklist.md#L90-L93](https://github.com/web-platform-tests/wpt/blob/master/docs/reviewing-tests/checklist.md#L90-L93)

## STRUCT-005 — `structure` / warn / semantic

- **Rule:** Place single-test references using the test name with a `-ref` suffix; shared references go in a `references` directory.
- **Line reference:** line 7.
- **Evidence:** `<link rel="match" href="reference/align-content_center-ref.html">` — the reference lives in a directory named `reference/` (singular), not the documented `references/` (plural). The `-ref` filename suffix convention is followed. Mismatched directory name is a minor convention deviation; many existing tests in `css/css-flexbox/` use the same `reference/` directory, so this is essay-level consistency rather than a hard violation.
- **Source:** [wpt/docs/writing-tests/reftests.md#L46-L55](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/reftests.md#L46-L55)

## FOCUS-001 — `focus` / warn / semantic

- **Rule:** Tests should be as short as possible; extraneous elements on the page should be avoided so it is clear what is part of the test.
- **Line reference:** lines 21–23.
- **Evidence:** The verbose self-describing paragraph ("Test passes if: 1. … 2. …") is itself rendered in the test viewport. For a reftest, the rendered output is what gets screenshot-compared against the reference, so any extra paragraph in the test must also be present in the reference. Reviewer should confirm the reference contains an identical paragraph; otherwise the comparison will fail purely due to the descriptive text.
- **Source:** [wpt/docs/writing-tests/general-guidelines.md#L99-L106](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/general-guidelines.md#L99-L106)

## FOCUS-003 — `focus` / warn / semantic

- **Rule:** Tests should be self-describing: it should be obvious when they pass and when they fail without consulting the specification.
- **Line reference:** lines 21–23.
- **Evidence:** The self-describing statement does identify pass criteria, but uses ambiguous spatial language ("middle left") and assumes a "red rectangle" the reader cannot verify exists from the test file in isolation (it is supplied by `support/test-style.css`). A human reader needs to load the stylesheet to fully evaluate pass/fail.
- **Source:** [wpt/docs/writing-tests/general-guidelines.md#L170-L174](https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/general-guidelines.md#L170-L174)

---

## Rules checked and not flagged (summary)

- **FMT-001** (UTF-8 / charset): file contains only ASCII; no charset declaration is required by the rule's "pure ASCII" allowance.
- **NAME-001** (≤150 chars from test root): well under the limit.
- **NAME-005, NAME-007, NAME-008, NAME-009, NAME-012**: no flag suffixes present (`.https`, `-print`, etc.); rule conditions not triggered.
- **META-005** (CSS `<link rel="help">`): present at line 6.
- **META-006** (help link specificity): the link targets `#align-content-property` — a section anchor, satisfying the "relevant section" requirement.
- **STRUCT-001** (reftest `<link rel="match">`): present at line 7.
- **STRUCT-006, STRUCT-007, STRUCT-008**: single match link, no DOM manipulation, no fuzziness declared — conditions not triggered.
- **PORT-001, PORT-006, PORT-007, REV-001**: no external network resources, no hardcoded hosts/ports, no cross-origin URLs.
- **PORT-002, PORT-003, PORT-004, PORT-005**: no platform-specific assumptions visible; no custom fonts.
- **REV-002** (proprietary features): none used.
- **REV-003** (commented-out code): none.
- **REV-005** (title length): `"CSS Flexible Box Test: align-content_center"` is descriptive and not overly wordy.
- **FOCUS-002, FOCUS-004**: no edge-case feature dependencies; test should pass when align-content is correctly implemented.

---

**Note:** This evaluation is based solely on the test file. Findings for STRUCT-002, STRUCT-003, STRUCT-013, STRUCT-014, FOCUS-001, and STRUCT-004 cannot be conclusively resolved without inspecting `reference/align-content_center-ref.html` and `support/test-style.css`; they are flagged for reviewer follow-up.
