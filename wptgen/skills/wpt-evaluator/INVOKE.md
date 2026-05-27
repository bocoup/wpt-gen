# Invoking the WPT Evaluator as a skill-call

This file documents how to drive the evaluator manually from a conversation
with an agent. The intended use is **rubric validation** — running the
evaluator against real WPT test files to discover where the upstream
guidance is unclear, ambiguous, or missing — before any CLI or workflow
integration is built.

This branch (`wpt-eval-doc-inputs`) is the **doc-inputs variant**: the
evaluator reads upstream WPT documentation directly, rather than a
distilled `rules.yaml`. Findings cite the source doc + line range that
prompted the flag.

The expected output format and reading lists come from
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
specific guidance.

## Invocation protocol

In a fresh conversation, paste a prompt of the following shape. Replace
`<path>` with the file under evaluation.

```
Evaluate the WPT test file at <path> using the wpt-evaluator skill
(doc-inputs variant).

1. Read wptgen/skills/wpt-evaluator/SKILL.md to load the rubric, the
   curated reading lists, and the dependency-reading rules.
2. Read the test file at <path>.
3. Detect the test kind from the filename and contents (testharness,
   reftest, print-reftest, crashtest, manual, visual, idl, wdspec, css).
4. Load every doc on the curated reading list for that test kind
   (including the baseline "all kinds" list).
5. Detect declared dependencies in the test file (script src, link
   href, // META: script, etc.). List them, classify each as
   framework/external/local, and read local dependencies ONLY when
   SKILL.md's "When to read a local dependency" criteria apply.
6. Identify normative statements in the loaded docs and evaluate the
   test file against each one. Skip statements already enforced by
   `wpt lint`.
7. Produce findings in the format specified by SKILL.md:
   - Severity, line reference in the test file, evidence quote,
     source citation (upstream doc path + line range), one-sentence
     summary of the guidance.
   - No composite score. No proposed fixes. No synthetic rule IDs.
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
compare the corpus weight of different evaluator designs.

Use this template, replacing the example numbers with actual `wc -c`
output. Sum the bytes column at the bottom.

```markdown
## Input scope

| File                                                  |    Bytes | Role         |
| ----------------------------------------------------- | -------: | ------------ |
| wptgen/skills/wpt-evaluator/SKILL.md                  |    5,234 | skill        |
| wpt/docs/writing-tests/general-guidelines.md          |   10,841 | reading-list |
| wpt/docs/writing-tests/file-names.md                  |    3,012 | reading-list |
| ...                                                   |      ... |              |
| <path to test file under evaluation>                  |    3,128 | test         |
| <path to dependency that was read>                    |      812 | dependency   |
| **Total**                                             | **NN,NNN** |              |

Declared dependencies (not read): /resources/testharness.js,
/resources/testharnessreport.js, https://example.org/foo.js
Approach: doc-inputs              # use one of: distilled-yaml, doc-inputs
Approximate input tokens: ~NN,NNN # bytes ÷ 4
```

The `Role` column distinguishes the skill, curated reading-list docs,
the test file, and any dependencies that were actually read. List
dependencies that were detected but NOT read (framework + external)
on the line below the table so the cost of "considered but skipped"
is also visible.

The "Approach" tag lets A/B comparisons group reports by evaluator
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
   the test file and a specific upstream doc location. If the agent writes
   "this test is poorly structured" without a doc citation and a test line,
   the rubric prompted too loosely.
2. **Are findings accurate?** Does the doc citation actually back the
   finding, or did the evaluator over-interpret the prose? With the
   doc-inputs approach, this risk is higher than with the YAML approach
   because the source is less constrained.
3. **Are there obvious issues the evaluator missed?** Tests have
   anti-patterns the upstream docs don't cover. Note them — they are
   candidates for future work (either upstreaming guidance, or
   reintroducing a thin wpt-gen-side rules layer).
4. **Is the severity calibrated?** An `error` finding should reflect
   something a maintainer would block on. A `nit` should be ignorable.
   Verify that the inferred severity matches the upstream RFC 2119 keyword.
5. **Is the output readable?** If a human reviewer would have to wade
   through noise to find signal, the format needs work.

Record discoveries from each invocation in
`.wpt-evaluator-tmp/outputs/<filename>.md` alongside the findings, or in
a separate notes file. These become the input for the next rubric pass.

## When to graduate beyond skill-call

After running this protocol against several diverse tests, and once one
of the evaluator designs is producing consistent useful output, the next
step is a CLI command. The CLI is a thin wrapper around exactly this
protocol:

```
wpt-gen evaluate <path-to-test-file>
```

Same skill, same docs (or rules), same output format — just automated
invocation instead of manual prompting.
