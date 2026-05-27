# WPT Evaluation: svg/sniffing-content-type.html

## Input scope

| File                                              |    Bytes | Role  |
| ------------------------------------------------- | -------: | ----- |
| wptgen/skills/wpt-evaluator/SKILL.md              |    9,276 | skill |
| wptgen/skills/wpt-evaluator/references/rules.yaml |   50,132 | rules |
| svg/sniffing-content-type.html                    |    1,090 | test  |
| **Total**                                         | **60,498** |       |

Declared dependencies (not read): /resources/testharness.js, /resources/testharnessreport.js
Approach: distilled-yaml
Approximate input tokens: ~15,124

---

## Test kind

`testharness` · `html`

---

## Findings

### FMT-001 — info · line 1
**No `<meta charset=utf-8>` present.**

The file contains a `<svg … xmlns="…">` string and a `http://www.w3.org/2000/svg` URI that are pure ASCII, and the file appears to be ASCII-clean. However, the HTML spec requires that HTML documents served without an explicit charset declaration in the HTTP header carry `<meta charset=utf-8>` (or equivalent) inside `<head>`. The file has a `<head>` but omits the charset declaration. If the server does not set `Content-Type: text/html; charset=utf-8`, a browser could mis-interpret the encoding.

```
<head>
    <title>SVG Content Sniffing Test</title>
    <script src="/resources/testharness.js"></script>
```

Citation: `wpt/docs/writing-tests/general-guidelines.md#L82-L87`

---

### ASSERT-001 — warn · line 24
**`assert_false(Boolean(...))` is less specific than needed.**

The assertion wraps the value in `Boolean()` before passing it to `assert_false`. The value `window.exploitRan` is `undefined` (falsy) when the test passes and `true` when it fails. Using `assert_false(Boolean(window.exploitRan), …)` is equivalent to `assert_false(!!(window.exploitRan), …)`. The simpler and more idiomatic form is `assert_equals(window.exploitRan, undefined, …)` or at minimum `assert_false(window.exploitRan, …)`, both of which produce clearer failure messages (e.g., "expected false but got true" vs. "expected undefined but got true"). The `Boolean()` wrapper obscures the actual value on failure.

```
assert_false(Boolean(window.exploitRan), "The SVG content was incorrectly executed.");
```

Citation: `wpt/docs/reviewing-tests/checklist.md#L126-L130`

---

### ASYNC-001 — warn · line 10
**Synchronous `test()` with a side effect (appending a live element to the document) may race with the browser's load pipeline.**

The test appends an `<svg><use href="blob:...#x">` element synchronously inside `test()`. Whether the `use` element resolves its `href` and fires `onerror` synchronously or asynchronously is implementation-defined. If the browser resolves the blob URL asynchronously, `window.exploitRan` will still be `undefined` at assertion time regardless of whether the attack succeeded, producing a false pass. The test should use an async harness pattern — a `promise_test` or an `async_test` — that waits for a microtask/task turn (e.g., `Promise.resolve()` or a `load`/`error` event on the injected element) before asserting, so the assertion is evaluated after any asynchronous side effects can have fired.

```
test(() => {
    ...
    document.body.appendChild(svg);
    assert_false(Boolean(window.exploitRan), "The SVG content was incorrectly executed.");
}, "SVG should not be executed when the content type is not valid");
```

Citation: `wpt/docs/reviewing-tests/checklist.md#L116-L123`

---

### INDEP-001 — warn · line 9
**Mutable global state (`window.exploitRan`) is not cleaned up after the test.**

The test sets `window.exploitRan = true` on the global object (via an `onerror` handler) if the exploit fires. If this test is run as part of a multi-test file in the future, or if the test is retried, the global will still be `true` from the previous run, potentially masking failures in subsequent assertions or tests. A `t.add_cleanup(() => { delete window.exploitRan; })` call (for `async_test`) or equivalent cleanup at the end of `test()` should be added.

Additionally, the blob URL created with `URL.createObjectURL(blob)` is never revoked. While this does not affect correctness, `URL.revokeObjectURL(url)` should be called in a cleanup step.

```
const blob = new Blob([text], { type: 'application/octet-stream' });
const url = URL.createObjectURL(blob);
...
document.body.appendChild(svg);
assert_false(Boolean(window.exploitRan), ...);
```

Citation: `wpt/docs/reviewing-tests/checklist.md#L109-L114`

---

### PORT-001 / REV-001 — error · line 11
**Blob URL created from inline content functions as an internal resource, not an external one — no violation.**

`URL.createObjectURL` creates a `blob:` URL that is same-origin and local to the browser session. This does not constitute an external network resource. No violation of PORT-001 or REV-001.

*(No finding — recorded here to document the evaluation.)*

---

### FOCUS-003 — warn · line 25
**The test name is partially self-describing but the failure message is not actionable.**

The test title `"SVG should not be executed when the content type is not valid"` does not indicate *which* mechanism is being tested (SVG content sniffing via `<use href="blob:...">` referencing an `application/octet-stream` Blob). A reader seeing this test name in a results dashboard cannot identify the failure mechanism without reading the source.

The assert message `"The SVG content was incorrectly executed."` similarly does not distinguish this failure from other SVG execution failures.

Suggested title: `"SVG blob: URL with application/octet-stream content-type should not be executed via <use href>"`.

Citation: `wpt/docs/writing-tests/general-guidelines.md#L170-L174`

---

### REV-005 — nit · line 4
**Title matches the filename in being generic.**

`<title>SVG Content Sniffing Test</title>` is descriptive at a high level but does not indicate what specific behavior is being asserted. See FOCUS-003 above.

```
<title>SVG Content Sniffing Test</title>
```

Citation: `wpt/docs/reviewing-tests/checklist.md#L73-L75`

---

### NAME-002 — nit · file path
**Filename `sniffing-content-type.html` is reasonably descriptive** and follows the kebab-case convention. It does not include a numeric suffix, which is acceptable for a single test. No violation.

---

## Summary

| ID         | Severity | Category       | Short description                                                          |
| ---------- | -------- | -------------- | -------------------------------------------------------------------------- |
| FMT-001    | info     | file-format    | Missing `<meta charset=utf-8>` in `<head>`                                 |
| ASSERT-001 | warn     | assertions     | `assert_false(Boolean(...))` — use `assert_equals` or bare `assert_false`  |
| ASYNC-001  | warn     | async-timing   | Synchronous assertion may race with async blob URL resolution              |
| INDEP-001  | warn     | independence   | Global `window.exploitRan` not cleaned up; blob URL never revoked          |
| FOCUS-003  | warn     | focus          | Test title and assert message don't identify the specific mechanism tested |
| REV-005    | nit      | review         | Title is generic; does not describe the specific assertion                 |

The most significant concern is **ASYNC-001**: the test as written may produce a false pass on browsers that resolve `<use href="blob:...">` asynchronously, which is common. Converting to `promise_test` with an appropriate await (e.g., a settled `Promise.resolve()` after the DOM insertion) would make the test reliable. **INDEP-001** (cleanup) should be addressed in the same pass.
