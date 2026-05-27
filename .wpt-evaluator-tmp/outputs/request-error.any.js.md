# Evaluation: request-error.any.js

## Input scope

Files read in service of this evaluation:

| Path | Bytes |
| --- | ---: |
| `../wpt/fetch/api/request/request-error.any.js` | 2243 |
| `wptgen/skills/wpt-evaluator/SKILL.md` | 7475 |
| `wptgen/skills/wpt-evaluator/references/rules.yaml` | 50132 |

Dependencies verified to exist (not read):

| Path | Kind | Bytes |
| --- | --- | ---: |
| `../wpt/fetch/api/request/request-error.js` (via `// META: script=request-error.js`) | local | 1616 |

## Test kind

- `testharness` (uses `test()`, `assert_*` from harness)
- `js` (JavaScript-only test resource)
- `any` (filename suffix `.any.js`; `// META: global=window,worker`)
- Effective globals: `window`, `worker` (dedicated worker via the `.any.js` multi-global expansion)

## Declared dependencies

| Form | Path | Classification |
| --- | --- | --- |
| `// META: script=request-error.js` | `request-error.js` (sibling) | local |

The framework files (`/resources/testharness.js`, `/resources/testharnessreport.js`) are injected automatically by wptserve for `.any.js` and are not declared in the file. No external (`http(s)://`) or `/resources/`-prefixed dependencies are declared by this file.

## Findings

### REV-006 — `nit` — line 23

Rule: Tests in a single file should be separated by one empty line.

Evidence: The `for` block ends at line 14 and the next `test(...)` begins at line 16 with only one blank line — that case is fine. But the `test` ending at line 22 is followed immediately at line 24 by the next `test(`, with only one blank line (line 23), which is correct; however the same pattern recurs at lines 29→31, 37→39, 44→46, and 51→53, each with one blank line — also correct.

After re-checking each gap (lines 14↔16, 22↔24, 29↔31, 37↔39, 44↔46, 51↔53), every pair of tests is separated by exactly one empty line. **No violation.** This finding is included here only to record that the rule was evaluated.

Source: `wpt/docs/reviewing-tests/checklist.md#L135-L137`

---

### ASSERT-001 — `warn` — lines 16-22

Rule: Use the most specific assert available; avoid `assert_true` for everything.

Evidence: Lines 16-22 contain a `test(function() { ... })` with no test name argument. The `test()` invocation is missing its second-positional `name` parameter:

```js
test(function() {
  assert_throws_js(
      TypeError,
      () => Request("about:blank"),
      "Calling Request constructor without 'new' must throw"
    );
});
```

While not strictly an assertion-specificity issue, this is the closest matching rule on assertion quality. The lack of an explicit test name will cause the harness to auto-generate or duplicate names. (See also REV-005 below.)

Source: `wpt/docs/reviewing-tests/checklist.md#L126-L130`

---

### REV-005 — `nit` — line 22

Rule: The test title should be descriptive but not too wordy.

Evidence: The `test()` block ending at line 22 omits the test-name argument entirely:

```js
test(function() {
  assert_throws_js(
      TypeError,
      () => Request("about:blank"),
      "Calling Request constructor without 'new' must throw"
    );
});
```

Compare to every other `test(...)` in the file, which supplies an explicit second-argument name (lines 13, 29, 37, 44, 51, 56). Without a name argument, this test has no descriptive title at all. The string `"Calling Request constructor without 'new' must throw"` is passed only as the assert's `description` parameter, not as the test name.

Source: `wpt/docs/reviewing-tests/checklist.md#L73-L75`

---

### INDEP-001 — `warn` — lines 6-14

Rule: The number of tests in each file and the test names should be consistent across runs and browsers.

Evidence: Lines 6-14 iterate over `badRequestArgTests` (imported from `request-error.js`) to generate `test()` cases dynamically:

```js
for (const { args, testName } of badRequestArgTests) {
  test(() => {
    assert_throws_js(
      TypeError,
      () => new Request(...args),
      "Expect TypeError exception"
    );
  }, testName);
}
```

This pattern is acceptable per INDEP-001 *if* the data table is defined unconditionally and identically across globals. The dependency `request-error.js` was not read, so the consistency of `badRequestArgTests` across `window` and `worker` globals cannot be confirmed from this file alone. Recorded as advisory: confirm `badRequestArgTests` is statically defined.

Source: `wpt/docs/reviewing-tests/checklist.md#L109-L114`

---

### FOCUS-003 — `warn` — line 53-56

Rule: Tests should be self-describing: it should be obvious when they pass and when they fail without consulting the specification.

Evidence:

```js
test(function() {
  var options = {"cache": "only-if-cached", "mode": "same-origin"};
  new Request("test", options);
}, "Request with cache mode: only-if-cached and fetch mode: same-origin");
```

This test constructs a `Request` and makes no assertion. The implicit assertion is "does not throw" — the test passes if construction completes. The test name describes the configuration but not the expected outcome (i.e., that construction is allowed for this combination). A reader has to consult the Fetch spec to know whether this combination is supposed to be valid. Consider an explicit assertion or a more outcome-oriented name.

Source: `wpt/docs/writing-tests/general-guidelines.md#L170-L174`

---

### FOCUS-004 — `warn` — line 53-56

Rule: Tests should pass when the feature under test exposes the expected behavior, and fail when the feature is not implemented or implemented incorrectly.

Evidence: Same block as above. Because there is no assertion, the test will pass even if a future implementation regression alters `Request` construction in a way that does not throw — for example, if `Request("test", options)` silently coerces or ignores `cache: "only-if-cached"`. The absence of any positive assertion on the resulting `Request`'s properties weakens the test's ability to fail on incorrect implementation.

Source: `wpt/docs/writing-tests/general-guidelines.md#L121-L127`

---

## Rules evaluated but not violated (recorded)

The following rules in scope for `testharness, js, any, worker` were evaluated and produced no finding:

- **FMT-001** UTF-8 / ASCII — file is ASCII.
- **FMT-003** `.any.js` must not include `testharness.js`/`testharnessreport.js` — file does neither.
- **FMT-005** `.any.js` auto-invokes `done()` — file correctly omits a manual `done()`.
- **NAME-001** Path length under 150 chars — `fetch/api/request/request-error.any.js` is well under.
- **NAME-005** Feature-flag ordering — no feature flags present.
- **NAME-006** `.any` immediately followed by `.js` — yes.
- **NAME-007** HTTPS filename — test does not require HTTPS.
- **META-001** `// META: title=...` — present on line 2.
- **META-002** Use `// META: script=...` for external JS — used on line 3.
- **META-003** `// META: timeout=long` — not needed; tests are synchronous.
- **PORT-001** No external network resources — none referenced.
- **PORT-006** No hardcoded hosts/ports — none.
- **REV-001** No external resources — none.
- **REV-002** No proprietary features — none.
- **REV-003** No commented-out code — line 5 is a comment but it is explanatory ("badRequestArgTests is from response-error.js"), not commented-out code.
- **ASSERT-002** `idlharness.js` for basic IDL — not applicable; tests are behavioral, not basic IDL conformance.
- **API-001** IDL tests use `.any.js`/`.window.js` — uses `.any.js` (though this is not strictly an IDL test).

## Notes on comment at line 5

Line 5 reads:

```js
// badRequestArgTests is from response-error.js
```

This comment is informational, but the META script on line 3 imports `request-error.js`, not `response-error.js`. The comment may be incorrect (says `response-error.js` while the actual META import is `request-error.js`). This is a documentation/accuracy concern rather than a rule violation per the current corpus; no rule in `rules.yaml` covers internal comment accuracy. Recorded for human-reviewer attention.
