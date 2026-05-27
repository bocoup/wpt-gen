# WPT Evaluator findings — `fetch/api/request/request-error.any.js`

## Input scope

Test file under evaluation:

| Path | Bytes |
| --- | --- |
| `wpt/fetch/api/request/request-error.any.js` | 2243 |

Curated reading list (testharness, all-kinds baseline + testharness-only):

| Path | Bytes |
| --- | --- |
| `wpt/docs/writing-tests/general-guidelines.md` | 9253 |
| `wpt/docs/writing-tests/file-names.md` | 2628 |
| `wpt/docs/writing-tests/assumptions.md` | 1949 |
| `wpt/docs/writing-tests/server-features.md` | 6141 |
| `wpt/docs/reviewing-tests/checklist.md` | 4767 |
| `wpt/docs/writing-tests/testharness.md` | 12178 |

Declared dependencies:

| Dependency | Form | Classification | Read? |
| --- | --- | --- | --- |
| `request-error.js` | `// META: script=request-error.js` | local | yes — to evaluate the on-file comment claiming `badRequestArgTests` is "from response-error.js", and to confirm META-script existence per SKILL.md |

Local dependency read:

| Path | Bytes |
| --- | --- |
| `wpt/fetch/api/request/request-error.js` | 1616 |

## Findings

### Finding 1

- **Severity**: warn
- **Line reference**: [request-error.any.js:5](../../../wpt/fetch/api/request/request-error.any.js#L5)
- **Evidence**: `// badRequestArgTests is from response-error.js`
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L18-L21` ("It is obvious what the test is trying to test.")
- **Summary**: The inline comment misattributes `badRequestArgTests` to `response-error.js`, but the META-declared dependency (and only file in this directory that defines it) is `request-error.js`; this obscures rather than clarifies what the test is testing.

### Finding 2

- **Severity**: warn
- **Line reference**: [request-error.any.js:16-22](../../../wpt/fetch/api/request/request-error.any.js#L16-L22)
- **Evidence**: `test(function() { assert_throws_js(... () => Request("about:blank"), "Calling Request constructor without 'new' must throw" ); });`
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L18-L21` ("It is obvious what the test is trying to test.")
- **Summary**: This `test(...)` call omits the test-name (second) argument, so the harness will auto-generate a name; the intended description lives only inside the `assert_throws_js` message, making the test less self-describing than the named tests around it.

### Finding 3

- **Severity**: warn
- **Line reference**: [request-error.any.js:53-56](../../../wpt/fetch/api/request/request-error.any.js#L53-L56)
- **Evidence**: `test(function() { var options = {"cache": "only-if-cached", "mode": "same-origin"}; new Request("test", options); }, "Request with cache mode: only-if-cached and fetch mode: same-origin");`
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L126-L130` ("The test uses the most specific asserts possible (e.g. doesn't use `assert_true` for everything).")
- **Summary**: The test body contains no assertion — it only constructs a `Request` and relies on the absence of a thrown exception to count as a pass; an explicit positive assertion (e.g., `assert_equals(request.cache, "only-if-cached")`) would make the intent and the pass/fail criterion explicit.

### Finding 4

- **Severity**: info
- **Line reference**: [request-error.any.js:16-22](../../../wpt/fetch/api/request/request-error.any.js#L16-L22), [request-error.any.js:53-56](../../../wpt/fetch/api/request/request-error.any.js#L53-L56)
- **Evidence**: `test(function() { ... });` (and same form at line 53)
- **Source citation**: `wpt/docs/reviewing-tests/checklist.md:L109-L114` ("The number of tests in each file and the test names are consistent across runs and browsers.")
- **Summary**: Auto-generated test names (when the second arg to `test()` is omitted) are derived from the function source, which can shift if the file is reformatted, weakening cross-run/cross-browser name stability versus the surrounding explicitly-named tests.

### Finding 5

- **Severity**: nit
- **Line reference**: [request-error.any.js:7-13](../../../wpt/fetch/api/request/request-error.any.js#L7-L13), [request-error.any.js:16-22](../../../wpt/fetch/api/request/request-error.any.js#L16-L22), [request-error.any.js:24-29](../../../wpt/fetch/api/request/request-error.any.js#L24-L29)
- **Evidence**: mix of `test(() => { ... }, name)` and `test(function() { ... }, name)` inside one file
- **Source citation**: `wpt/docs/writing-tests/general-guidelines.md:L178-L186` (Style Rules — "Any of these rules may be broken if the test demands it" and the file-level consistency expectation implied by the rest of the section)
- **Summary**: Tests within a single file mix arrow-function and `function()` callbacks for `test()`; consistent style within a single file is preferable.
