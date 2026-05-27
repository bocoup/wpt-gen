# Invoking the WPT Evaluator

A paste-able prompt for running the evaluator as a skill-call. All
behavior is defined in [`SKILL.md`](SKILL.md) — this file is only the
entry point.

Use a fresh conversation so prior context doesn't leak into the
evaluation. Replace `<path>` with the test file under evaluation.

```
Evaluate the WPT test file at <path> using the wpt-evaluator skill at
wptgen/skills/wpt-evaluator/. Read SKILL.md and follow its procedure.

Write the report to .wpt-evaluator-tmp/outputs/<filename>.md (where
<filename> matches the input filename with `.md` appended).
```
