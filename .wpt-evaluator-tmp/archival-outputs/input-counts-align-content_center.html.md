## Input scope

| File                                              |    Bytes |
| ------------------------------------------------- | -------: |
| wptgen/skills/wpt-evaluator/SKILL.md              |    4,002 |
| wptgen/skills/wpt-evaluator/references/rules.yaml |   50,132 |
| ../wpt/css/css-flexbox/align-content_center.html  |      968 |
| **Total**                                         | **55,102** |

Approach: distilled-yaml
Approximate input tokens: ~13,776
Total session tokens: 58.4k

## Test classification

- **Kind**: reftest (has `<link rel="match">`)
- **Format**: HTML
- **Category**: CSS (under `css/css-flexbox/`)
- **Applies-to filters**: `reftest`, `html`, `css`

## Findings

### FMT-001 — file-format — error (deterministic)
- **Line**: 1–3 (head region)
- **Evidence**: No `<meta charset="utf-8">` declared in the file.
- **Rule**: Files must be encoded in UTF-8. In HTML, where UTF-8 is not the default encoding, files must contain `<meta charset=utf-8>` or be pure ASCII.
- **Source**: wpt/docs/writing-tests/general-guidelines.md#L82-L87
- **Note**: The file appears to be pure ASCII (no non-ASCII characters present), so this may be compliant by the ASCII clause. However, explicit `<meta charset>` is the safer convention.

### STRUCT-001 — structure — error (deterministic) — PASS
- **Line**: 7
- **Evidence**: `<link rel="match" href="reference/align-content_center-ref.html">`
- **Rule**: A reftest file must contain a `<link rel="match"|"mismatch">` with an `href`.
- **Source**: wpt/docs/writing-tests/reftests.md#L25-L29
- **Status**: Satisfied. (Listed for completeness; no issue.)

### STRUCT-005 — structure — warn (semantic)
- **Line**: 7
- **Evidence**: `<link rel="match" href="reference/align-content_center-ref.html">`
- **Rule**: Single-test references should use the test name with a `-ref` suffix, in the same directory; shared references go in a `references` directory.
- **Source**: wpt/docs/writing-tests/reftests.md#L46-L55
- **Issue**: The reference is placed in a sibling `reference/` (singular) directory rather than the conventional `references/` (plural) shared directory, *or* alongside the test as `align-content_center-ref.html`. The filename suffix convention (`-ref`) is respected, but the directory name (`reference/`) does not match either documented pattern.

### STRUCT-009 — structure — nit (semantic)
- **Line**: 21–23
- **Evidence**: `Test passes if: 1. the rectangle 1, 2, 3 show up in a vertical column in a red rectangle and no gap between them. 2. the rectangle 1, 2, 3 appear in middle left of red rectangle.`
- **Rule**: Reftests should include a self-describing statement that is accurate, precise, simple, and self-explanatory.
- **Source**: wpt/docs/reviewing-tests/checklist.md#L95-L104
- **Issue**: A self-describing statement is present, but for a reftest the harness compares to a reference image — the human-readable pass criteria is supplementary. The phrasing is acceptable but somewhat awkward ("the rectangle 1, 2, 3 show up", "middle left of red rectangle"). Grammar (singular/plural) and color reference ("red rectangle" — no red is established in this file's CSS) reduce clarity.

### STRUCT-013 — structure — warn (semantic)
- **Line**: 10–18 (style), 20–25 (body)
- **Evidence**: The test uses no green/red color convention. The flex container has only `height: 200px; width: 80px; display: flex; flex-wrap: wrap; align-content: center;` with no background color, and items have no styling visible in this file (presumably from `support/test-style.css`).
- **Rule**: Rendering tests should indicate success with a recognizable visual pattern — typically a green paragraph or green square, often over red so misalignment exposes red.
- **Source**: wpt/docs/writing-tests/rendering.md#L8-L24
- **Issue**: The instruction text refers to a "red rectangle" but the test file itself defines no red background. Color cues (if any) come from the external `support/test-style.css` stylesheet, making the rendering convention non-obvious from the test file alone. For a reftest, the convention is less critical than for a visual test (since comparison is automated), but the rendering-test guidelines still apply.

### STRUCT-014 — structure — warn (semantic)
- **Line**: 10–18
- **Evidence**: Test CSS does not encode failure as a visually obvious pattern (e.g., red exposed, "FAIL" text, overlapping text).
- **Rule**: Rendering tests should be designed so failures are visually obvious.
- **Source**: wpt/docs/writing-tests/rendering.md#L37-L59
- **Issue**: Same as STRUCT-013 — without seeing `support/test-style.css`, this file alone gives no failure-exposing visual design. For an automated reftest this is mitigated by the reference comparison, but the instruction text refers to a red rectangle that isn't established in this file.

### META-005 — metadata — error (deterministic) — PASS
- **Line**: 6
- **Evidence**: `<link rel="help" href="http://www.w3.org/TR/css-flexbox-1/#align-content-property" />`
- **Rule**: CSS tests REQUIRE at least one `<link rel="help" href="...">`.
- **Source**: wpt/docs/writing-tests/css-metadata.md#L5-L12
- **Status**: Satisfied.

### META-006 — metadata — warn (semantic) — PASS
- **Line**: 6
- **Evidence**: `<link rel="help" href="http://www.w3.org/TR/css-flexbox-1/#align-content-property" />`
- **Rule**: Spec links should target relevant sections; primary section first.
- **Source**: wpt/docs/writing-tests/css-metadata.md#L16-L25
- **Status**: Single link to a fragment-anchored, specific section. Satisfied.

### META-007 — metadata — warn (semantic)
- **Line**: 9
- **Evidence**: `<meta name="assert" content="Check if the web engine can identify the align-content value center." />`
- **Rule**: `<meta name="assert">` must not duplicate the title, the verification instructions, the suite, or a spec line.
- **Source**: wpt/docs/writing-tests/css-metadata.md#L156-L168
- **Issue**: The assertion is weakly phrased ("Check if the web engine can identify...") — it describes a meta-action rather than the property/value behavior under test. While not a literal duplicate of the title, it conveys roughly the same information as the title (`align-content_center`) with little added specificity. A stronger assertion would describe the expected layout effect (e.g., "When `align-content: center` is applied to a multi-line flex container, the flex lines are centered along the cross axis").

### PORT-003 — portability — warn (deterministic)
- **Line**: 24
- **Evidence**: `<div id=test><div id=test01>1</div><div id=test02>2</div><div id=test03>3</div></div>` — renders digits "1", "2", "3" using the UA's default font.
- **Rule**: Fonts cannot be relied on to be installed or to have specific metrics. When a known font is needed, use Ahem loaded as a web font.
- **Source**: wpt/docs/writing-tests/general-guidelines.md#L154-L157
- **Issue**: The test displays text ("1", "2", "3") in flex items without specifying a font. If the reference also uses a default font, the comparison may be acceptable, but cross-platform font-metric variation could affect layout (item baseline, item height with `flex-wrap: wrap`). Using Ahem would make the comparison robust.

### PORT-005 — portability — warn (semantic) — informational
- **Line**: N/A
- **Evidence**: Test relies on default `color: black` text on default canvas background.
- **Rule**: Tests may assume `medium` font-size = 16px, canvas background white, initial color black, empty user stylesheet.
- **Source**: wpt/docs/writing-tests/assumptions.md#L9-L12
- **Status**: Within the assumed envelope. No finding.

### FOCUS-001 — focus — warn (semantic)
- **Line**: 21–23, 24
- **Evidence**: The visible page content is the multi-line instruction paragraph plus the 80×200 flex container with digits 1/2/3.
- **Rule**: Tests should be as short as possible; extraneous page elements should be avoided so it is clear what is part of the test.
- **Source**: wpt/docs/writing-tests/general-guidelines.md#L99-L106
- **Issue**: For a reftest, the human-readable instruction paragraph (`<p>Test passes if: ...</p>`) appears in the test viewport and will be part of the screenshot compared against the reference. If the reference also renders this paragraph, that's fine; if not, the instruction text contributes to the rendering area. Reftests typically rely on the rendered output alone — long instruction text on the test page is uncommon and risks pushing the actual test region or affecting layout.

### FOCUS-003 — focus — warn (semantic)
- **Line**: 21–23
- **Evidence**: `Test passes if: 1. the rectangle 1, 2, 3 show up in a vertical column in a red rectangle and no gap between them. 2. the rectangle 1, 2, 3 appear in middle left of red rectangle.`
- **Rule**: Tests should be self-describing; obvious when they pass/fail without consulting the spec.
- **Source**: wpt/docs/writing-tests/general-guidelines.md#L170-L174
- **Issue**: The self-describing text mentions a "red rectangle" but no red is defined in this file. The reader must inspect `support/test-style.css` or the rendered output to understand the pass condition. The phrasing also has grammatical issues ("the rectangle 1, 2, 3 show up", "appear in middle left of red rectangle").

### REV-001 — review — error (deterministic) — PASS
- **Line**: 5, 6, 7, 8
- **Evidence**: References are to `http://www.intel.com` (author link only, not loaded), the W3C spec (`rel="help"`, not loaded), and local `reference/` and `support/` paths.
- **Rule**: Test must not use external resources.
- **Source**: wpt/docs/reviewing-tests/checklist.md#L42-L45
- **Status**: The `rel="author"` and `rel="help"` URLs are metadata, not loaded resources. Stylesheet and reference are local. Satisfied.

### NAME-002 — filename — nit (semantic)
- **Line**: filename
- **Evidence**: `align-content_center.html`
- **Rule**: File names should be descriptive; common format is `test-topic-001.html` (hyphen-separated, padded integer).
- **Source**: wpt/docs/writing-tests/general-guidelines.md#L15-L22
- **Issue**: The filename is descriptive but mixes hyphens and underscores (`align-content_center` instead of `align-content-center`). Not strictly required, but the convention favors hyphens throughout.

### NAME-001 — filename — error (deterministic) — PASS
- **Evidence**: Path `css/css-flexbox/align-content_center.html` (38 chars relative to test root).
- **Rule**: < 150 characters.
- **Status**: Satisfied.

## Indentation / formatting observation (not a rule violation)

- **Lines 12–17**: The style block mixes tabs and spaces for indentation (tabs on lines 12, 15, 16, 17; spaces on 13, 14). Cosmetic; no rule covers this.

## Files read in service of the evaluation

| File                                              | Bytes  |
| ------------------------------------------------- | -----: |
| wptgen/skills/wpt-evaluator/SKILL.md              |  4,002 |
| wptgen/skills/wpt-evaluator/references/rules.yaml | 50,132 |
| ../wpt/css/css-flexbox/align-content_center.html  |    968 |
| **Total**                                         | **55,102** |

Note: `support/test-style.css` and `reference/align-content_center-ref.html` were referenced by the test file but not opened — their existence was verified by directory listing only. Several findings (STRUCT-013, STRUCT-014, FOCUS-001) would benefit from inspecting those files but were issued based on what the test file alone discloses.
