## Input scope

| File                                                  |    Bytes |
| ----------------------------------------------------- | -------: |
| wptgen/skills/wpt-evaluator/SKILL.md                  |    4,612 |
| wpt/docs/writing-tests/general-guidelines.md          |    9,253 |
| wpt/docs/writing-tests/file-names.md                  |    2,628 |
| wpt/docs/writing-tests/assumptions.md                 |    1,949 |
| wpt/docs/writing-tests/server-features.md             |    6,141 |
| wpt/docs/reviewing-tests/checklist.md                 |    4,767 |
| wpt/docs/writing-tests/reftests.md                    |    7,639 |
| wpt/docs/writing-tests/rendering.md                   |    3,405 |
| wpt/docs/writing-tests/css-metadata.md                |    5,407 |
| wpt/css/css-flexbox/align-content_center.html         |      968 |
| **Total**                                             | **46,769** |

Approach: doc-inputs
Approximate input tokens: ~11,692
Total session tokens: 57.8k

## Test classification

- Kind: **reftest** (has `<link rel="match">`) + **css** (lives under `css/css-flexbox/`)
- Reading lists applied: all-kinds baseline, reftest, css

## Findings

### 1. Filename uses underscore and lacks numeric suffix

- **Severity**: nit
- **Line reference**: filename `align-content_center.html`
- **Evidence**: `align-content_center.html`
- **Source citation**: `wpt/docs/writing-tests/general-guidelines.md:L16-L23`
- **Summary**: The documented common filename format is `test-topic-NNN.html` (hyphen-separated, three-digit suffix); this file uses an underscore between `align-content` and `center` and omits a numeric suffix.

### 2. Title duplicates the filename

- **Severity**: nit
- **Line reference**: L4
- **Evidence**: `<title>CSS Flexible Box Test: align-content_center</title>`
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L73-L75`
- **Summary**: The reviewer checklist flags titles that are not descriptive but instead wordy or mechanical; this title pastes the raw filename rather than describing what is being tested.

### 3. Self-describing statement relies on a red rectangle the markup does not visibly produce

- **Severity**: warn
- **Line reference**: L21-L23
- **Evidence**: `Test passes if:<br>\n    1. the rectangle 1, 2, 3 show up in a vertical column in a red rectangle and no gap between them.<br>\n    2. the rectangle 1, 2, 3 appear in middle left of red rectangle.`
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L99-L104`
- **Summary**: The reftest self-describing statement should be accurate, precise, simple, and self-explanatory so a non-technical reader can decide pass/fail in seconds; this statement references a "red rectangle" whose existence depends on `support/test-style.css` (not visible in the test file) and uses awkward phrasing ("the rectangle 1, 2, 3").

### 4. Pass description and visible content depend on a font for rendered digits, which the platform does not guarantee

- **Severity**: warn
- **Line reference**: L24
- **Evidence**: `<div id=test><div id=test01>1</div><div id=test02>2</div><div id=test03>3</div></div>`
- **Source citation**: `wpt/docs/writing-tests/general-guidelines.md:L154-L157`
- **Summary**: Tests cannot rely on fonts being installed or having specific metrics; when a known font is needed, Ahem (loaded as a web font) should be used. This reftest renders numeric glyphs whose box size and position will vary across platforms, putting pixel-perfect matching at risk.

### 5. Reftest must render pixel-perfect identically across platforms — text-based content is fragile

- **Severity**: warn
- **Line reference**: L24
- **Evidence**: `<div id=test01>1</div><div id=test02>2</div><div id=test03>3</div>`
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L80-L83`
- **Summary**: Reftest reviewer checklist requires the reference render pixel-perfect identically to the test on all platforms; rendering rasterized digits without a controlled font (e.g., Ahem) and without `<meta name=fuzzy>` makes platform-identical rendering unlikely.

### 6. Test sizing (200×80) places content well within 800×600 but no scrollbar control is exercised

- **Severity**: info
- **Line reference**: L11-L17
- **Evidence**: `#test{\n\theight: 200px;\n        width: 80px;\n        display: flex;`
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L90-L93`
- **Summary**: Test and reference must render within an 800×600 viewport without scrollbars unless scrolling is under test; this test satisfies that constraint (dimensions 200×80) — flagged only as confirmation, not a violation.

### 7. Indicator color choice (red as the failure indicator) is conventionally correct but the test file does not establish the red itself

- **Severity**: info
- **Line reference**: L8, L21-L23
- **Evidence**: `<link rel="stylesheet" href="support/test-style.css">` … `red rectangle`
- **Source citation**: `wpt/docs/writing-tests/rendering.md:L46-L51`
- **Summary**: Rendering guidance recommends using red so that a rendering off by a few pixels exposes red on the page; the test relies on `support/test-style.css` (not opened during this evaluation) to provide that red. Evaluator did not open the support stylesheet, so cannot confirm whether the red layer is set up as a failure-revealing background behind the flex items.

### 8. `<meta name=assert>` phrasing is generic

- **Severity**: nit
- **Line reference**: L9
- **Evidence**: `<meta name="assert" content="Check if the web engine can identify the align-content value center." />`
- **Source citation**: `wpt/docs/writing-tests/css-metadata.md:L150-L188`
- **Summary**: css-metadata recommends a detailed assertion describing what the test specifically proves (examples like "This test checks that a background image with no intrinsic size covers the entire padding box."); "identify the … value" describes parsing rather than the layout behavior the reftest actually exercises.

### 9. Mixed tabs and spaces for indentation inside `<style>`

- **Severity**: (skipped — enforced by `wpt lint`)
- **Line reference**: L12, L15, L16, L17
- **Evidence**: `\theight: 200px;` (tab) vs. `        width: 80px;` (spaces)
- **Source citation**: `wpt/docs/writing-tests/general-guidelines.md:L183-L186`
- **Summary**: Style rules say use spaces for indentation; flagging here only as a note — `wpt lint` already enforces this.

## Notes on rubric / evaluator design

- The reference file `support/test-style.css` and `reference/align-content_center-ref.html` were intentionally *not* opened — INVOKE.md scopes evaluation to the single test file. Several findings (cross-platform pixel-match, red-failure-indicator setup, reference using a different technique) cannot be fully resolved without them. A future revision might either widen the scope to "the reftest pair plus its support files" or explicitly cap findings about cross-file properties at `info`.
- The `<link rel="help">` URL uses `http://www.w3.org/...`. Neither css-metadata.md nor general-guidelines.md mandates `https`, so this was not flagged.
- The test contains no `<meta charset>`, but the bytes are pure ASCII; general-guidelines.md:L82-L87 permits this, so no finding.
- Severity calibration: nothing in the loaded docs uses RFC-2119 MUST language for the issues found; the strongest term applied is "must render pixel-perfect identically" in the reviewer checklist (treated as `warn` rather than `error` because the checklist itself is framed as a guideline, per its own header).
