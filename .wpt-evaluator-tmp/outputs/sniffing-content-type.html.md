## Input scope

| File                                                          |    Bytes | Role         |
| ------------------------------------------------------------- | -------: | ------------ |
| wptgen/skills/wpt-evaluator/SKILL.md                          |    9,221 | skill        |
| wpt/docs/writing-tests/general-guidelines.md                  |    9,253 | reading-list |
| wpt/docs/writing-tests/file-names.md                          |    2,628 | reading-list |
| wpt/docs/writing-tests/assumptions.md                         |    1,949 | reading-list |
| wpt/docs/writing-tests/server-features.md                     |    6,141 | reading-list |
| wpt/docs/writing-tests/testharness.md                         |   12,178 | reading-list |
| wpt/docs/reviewing-tests/checklist.md                         |    4,767 | reading-list |
| wpt/svg/sniffing-content-type.html                            |    1,090 | test         |
| **Total**                                                     | **47,227** |              |

Declared dependencies (not read): /resources/testharness.js, /resources/testharnessreport.js
Approach: doc-inputs
Approximate input tokens: ~11,807

---

## Findings

### 1. Missing `<meta charset=utf-8>` declaration

**Severity**: `error`
**Line reference**: Line 2 (`<html>`)
**Evidence**: The `<head>` element contains no `<meta charset>` declaration.
**Source citation**: `wpt/docs/writing-tests/general-guidelines.md:L84-L87`
**Summary**: HTML files that are not pure ASCII must contain `<meta charset=utf-8>` (or equivalent metadata) to declare their encoding; the test omits this required declaration.

---

### 2. Missing `<link rel="help">` spec reference

**Severity**: `warn`
**Line reference**: Lines 3–7 (`<head>` block)
**Evidence**: No `<link rel="help" href="...">` element is present.
**Source citation**: `wpt/docs/writing-tests/general-guidelines.md:L172-L175` (Be Self-Describing section); `wpt/docs/reviewing-tests/checklist.md:L34-L36`
**Summary**: Tests should make it obvious what specification behavior they verify; a `<link rel="help">` pointing to the relevant spec section is the standard way to express this and is expected by reviewers.

---

### 3. Synchronous assertion on an asynchronous side-effect — likely false-passing test

**Severity**: `error`
**Line reference**: Lines 10–25 (the `test()` callback)
**Evidence**: `document.body.appendChild(svg)` followed immediately by `assert_false(Boolean(window.exploitRan), ...)` in the same synchronous microtask.
**Source citation**: `wpt/docs/reviewing-tests/checklist.md:L32-L35` ("The test fails when it's supposed to fail." / "The test is testing what it thinks it's testing.")
**Summary**: The `onerror` event on an SVG `<image>` element fires asynchronously after layout/load; asserting `window.exploitRan === false` synchronously before the event loop yields will always pass regardless of whether the browser actually blocks execution, making the test incapable of detecting the failure it intends to catch. The test should use `async_test` or `promise_test` with an event listener (or a short `step_timeout`) to give the browser time to fire the error event before asserting.

---

### 4. Over-wrapped assertion — `assert_false(Boolean(...))` instead of `assert_false(...)`

**Severity**: `nit`
**Line reference**: Line 24
**Evidence**: `assert_false(Boolean(window.exploitRan), ...)`
**Source citation**: `wpt/docs/reviewing-tests/checklist.md:L127-L129`
**Summary**: Reviewers expect tests to use the most specific assertion available; wrapping the value in `Boolean()` before passing it to `assert_false` is redundant since `assert_false` already performs a boolean coercion check, and the extra wrapper obscures what is actually being tested (`window.exploitRan` itself is the meaningful value).

---

### 5. `<!DOCTYPE html>` capitalization — not lowercase

**Severity**: `nit`
**Line reference**: Line 1
**Evidence**: `<!DOCTYPE html>` (uppercase DOCTYPE keyword)
**Source citation**: `wpt/docs/writing-tests/testharness.md:L63` (example boilerplate uses `<!doctype html>`)
**Summary**: WPT boilerplate examples consistently use `<!doctype html>` (lowercase); while browsers accept either, WPT style convention follows the lowercase form seen throughout the testharness documentation and existing tests.
