# Invoking the WPT Evaluator as a skill-call

This file documents how to drive the evaluator manually from a conversation
with an agent. The intended use is **rubric validation** — running the
evaluator against real WPT test files to discover where rules are unclear,
miscalibrated, or missing — before any CLI or workflow integration is built.

The expected output format and rubric come from
[`SKILL.md`](SKILL.md). This file only describes the invocation protocol.

## Scratch directory layout

Place inputs and outputs in the repo-root scratch directory:

```
.wpt-evaluator-tmp/
├── inputs/      # test files to evaluate (one per file)
└── outputs/     # findings reports, named to match inputs
```

`.wpt-evaluator-tmp/` is gitignored. Test inputs can be copies of files from
`../wpt/`, files produced by wpt-gen, or hand-crafted cases for probing
specific rules.

## Invocation protocol

In a fresh conversation, paste a prompt of the following shape. Replace
`<path>` with the file under evaluation.

```
Evaluate the WPT test file at <path> using the wpt-evaluator skill.

1. Read wptgen/skills/wpt-evaluator/SKILL.md to load the rubric and the
   dependency-reading rules.
2. Read the test file at <path>.
3. Detect the test kind from the filename and contents (testharness,
   reftest, manual, crashtest, visual, idl, wdspec, etc.).
4. Load rules from wptgen/skills/wpt-evaluator/references/rules.yaml,
   filtering to those whose `applies_to` includes the detected kind
   (plus matching `html`/`js`/`css` etc. based on file content).
5. Detect declared dependencies in the test file (script src, link
   href, // META: script, etc.). List them, classify each as
   framework/external/local, and read local dependencies ONLY when
   SKILL.md's "When to read a local dependency" criteria apply.
6. Evaluate the test file against each applicable rule.
7. Produce findings in the format specified by SKILL.md:
   - Rule ID, severity, line reference, evidence quote, source citation.
   - No composite score. No proposed fixes.
8. As you work, track every file you read in service of the evaluation.
   For each file: its path and its byte size (use `wc -c <path>` or
   equivalent). Do NOT count files you only touched to navigate (e.g.,
   directory listings, this INVOKE.md, files referenced but not opened).
9. Write the findings to .wpt-evaluator-tmp/outputs/<filename>.md, where
   <filename> matches the input filename with `.md` appended. Prepend
   an "Input scope" section to the report (format below).
```

If the file path is relative to a directory you've cloned alongside (e.g.,
`../wpt/css/css-flexbox/flex-direction-001.html`), pass that path as-is —
the agent has read access to sibling directories.

## Input scope section format

The findings report must begin with an Input scope section recording what
was loaded into context during the evaluation. This makes it possible to
compare the corpus weight of different evaluator designs (e.g., distilled
YAML vs. tagged upstream docs).

Use this template, replacing the example numbers with actual `wc -c`
output. Sum the bytes column at the bottom.

```markdown
## Input scope

| File                                              |    Bytes | Role         |
| ------------------------------------------------- | -------: | ------------ |
| wptgen/skills/wpt-evaluator/SKILL.md              |    4,002 | skill        |
| wptgen/skills/wpt-evaluator/references/rules.yaml |   26,341 | rules        |
| <path to test file under evaluation>              |    3,128 | test         |
| <path to dependency that was read>                |      812 | dependency   |
| **Total**                                         | **NN,NNN** |              |

Declared dependencies (not read): /resources/testharness.js,
/resources/testharnessreport.js, https://example.org/foo.js
Approach: distilled-yaml          # or tagged-docs, prose-direct, etc.
Approximate input tokens: ~NN,NNN # bytes ÷ 4
```

The `Role` column distinguishes the skill, the rules corpus, the test
file, and any dependencies that were actually read. List dependencies
that were detected but NOT read (framework + external) on the line
below the table so the cost of "considered but skipped" is also
visible.

The "Approach" tag lets later A/B comparisons group reports by evaluator
design. Use a short stable label per approach.

After the Input scope section, continue with the findings as specified
by SKILL.md.

## What Input scope can and can't tell you

It captures: the corpus the evaluator chose to load.

It does NOT capture: system prompt, tool-call overhead, the agent's
internal reasoning, or anything the harness loaded outside the agent's
control. Treat the byte total as a **lower bound** on real input tokens,
and as a **directly comparable** signal between approaches that both
under-count by the same overhead.

For the conversation-wide actual token count, use Claude Code's
`/cost` command at the end of the session.

## What to look for during validation

When reviewing the output, the rubric-design questions to keep in mind:

1. **Are findings grounded?** Each finding should cite a specific line in
   the test file and a specific rule ID. If the agent writes
   "this test is poorly structured" without a rule ID and line, the
   rubric prompted too loosely.
2. **Are the `layer` labels accurate?** A rule marked `deterministic`
   should be flagged via straightforward pattern matching, not subjective
   judgment. If the agent had to reason heavily to apply it, the rule
   should probably be `semantic` (or rewritten).
3. **Are there obvious issues the evaluator missed?** Tests have
   anti-patterns the rule set doesn't cover. Note them — they are
   candidates for new rules.
4. **Is the severity calibrated?** An `error` finding should reflect
   something a maintainer would block on. A `nit` should be ignorable.
   Mismatches indicate the severity field needs tuning.
5. **Is the output readable?** If a human reviewer would have to wade
   through noise to find signal, the format needs work.

Record discoveries from each invocation in
`.wpt-evaluator-tmp/outputs/<filename>.md` alongside the findings, or in
a separate notes file. These become the input for the next rubric pass.

## When to graduate beyond skill-call

After running this protocol against several diverse tests (testharness,
reftest, manual, crashtest, ideally tests of varying quality), and once
the rubric is producing consistent useful output, the next step is a CLI
command. The CLI is a thin wrapper around exactly this protocol:

```
wpt-gen evaluate <path-to-test-file>
```

Same skill, same rules, same output format — just automated invocation
instead of manual prompting.
