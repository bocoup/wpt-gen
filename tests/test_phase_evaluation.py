"""Tests for the evaluation phase: dataclasses, payload conversion, the
report renderer, and run_evaluation."""

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from wptgen.config import Config
from wptgen.phases.evaluation import (
    EvaluationReportRenderer,
    Finding,
    InputScope,
    InputScopeFile,
    _payload_to_findings,
    _payload_to_input_scope,
    run_evaluation,
)


# ---------------------------------------------------------------------------
# InputScope dataclass properties
# ---------------------------------------------------------------------------


def test_input_scope_total_bytes_sums_files() -> None:
    scope = InputScope(
        files=[
            InputScopeFile(path="a.md", bytes=100, role="skill"),
            InputScopeFile(path="b.md", bytes=250, role="reading-list"),
            InputScopeFile(path="c.html", bytes=50, role="test"),
        ],
    )
    assert scope.total_bytes == 400


def test_input_scope_token_estimate_is_bytes_over_four() -> None:
    scope = InputScope(
        files=[InputScopeFile(path="a.md", bytes=4000, role="skill")],
    )
    assert scope.approximate_input_tokens == 1000


def test_input_scope_empty_files_zeroes() -> None:
    scope = InputScope()
    assert scope.total_bytes == 0
    assert scope.approximate_input_tokens == 0


# ---------------------------------------------------------------------------
# Payload conversion
# ---------------------------------------------------------------------------


def test_payload_to_findings_roundtrips_all_fields() -> None:
    payload = [
        {
            "title": "missing charset",
            "severity": "warn",
            "test_line": "Lines 1-4",
            "evidence": "<head>...",
            "source": "wpt/docs/writing-tests/general-guidelines.md:L82-L87",
            "summary": "HTML files must declare encoding.",
        }
    ]
    findings = _payload_to_findings(payload)
    assert len(findings) == 1
    f = findings[0]
    assert f.title == "missing charset"
    assert f.severity == "warn"
    assert f.test_line == "Lines 1-4"
    assert f.evidence == "<head>..."
    assert f.source == "wpt/docs/writing-tests/general-guidelines.md:L82-L87"
    assert f.summary == "HTML files must declare encoding."


def test_payload_to_findings_tolerates_missing_fields() -> None:
    findings = _payload_to_findings([{}])
    assert len(findings) == 1
    f = findings[0]
    assert f.title == ""
    assert f.severity == ""
    assert f.test_line == ""
    assert f.evidence == ""
    assert f.source == ""
    assert f.summary == ""


def test_payload_to_findings_empty_list() -> None:
    assert _payload_to_findings([]) == []


def test_payload_to_input_scope_full() -> None:
    payload = {
        "files": [
            {"path": "skill.md", "bytes": 100, "role": "skill"},
            {"path": "test.html", "bytes": 50, "role": "test"},
        ],
        "dependencies_not_read": [
            "/resources/testharness.js",
            "http://example.com",
        ],
        "approach": "doc-inputs",
    }
    scope = _payload_to_input_scope(payload)
    assert len(scope.files) == 2
    assert scope.files[0].path == "skill.md"
    assert scope.files[0].bytes == 100
    assert scope.files[0].role == "skill"
    assert scope.dependencies_not_read == [
        "/resources/testharness.js",
        "http://example.com",
    ]
    assert scope.approach == "doc-inputs"


def test_payload_to_input_scope_tolerates_empty_payload() -> None:
    scope = _payload_to_input_scope({})
    assert scope.files == []
    assert scope.dependencies_not_read == []
    assert scope.approach == "doc-inputs"  # default


def test_payload_to_input_scope_handles_none_lists() -> None:
    # Agents might serialize empty fields as null/None — the conversion
    # should not crash.
    scope = _payload_to_input_scope(
        {"files": None, "dependencies_not_read": None}
    )
    assert scope.files == []
    assert scope.dependencies_not_read == []


# ---------------------------------------------------------------------------
# Report renderer
# ---------------------------------------------------------------------------


def _sample_finding(**overrides: Any) -> Finding:
    defaults: dict[str, Any] = {
        "title": "missing character encoding declaration",
        "severity": "warn",
        "test_line": "Lines 1-4",
        "evidence": "<!DOCTYPE html>",
        "source": "wpt/docs/writing-tests/general-guidelines.md:L82-L87",
        "summary": "HTML must declare encoding.",
    }
    defaults.update(overrides)
    return Finding(**defaults)


def _sample_scope(**overrides: Any) -> InputScope:
    defaults: dict[str, Any] = {
        "files": [
            InputScopeFile(
                path="wptgen/skills/wpt-evaluator/SKILL.md",
                bytes=7_500,
                role="skill",
            ),
            InputScopeFile(
                path="wpt/css/css-flexbox/align-content_center.html",
                bytes=968,
                role="test",
            ),
        ],
        "dependencies_not_read": [],
        "approach": "doc-inputs",
    }
    defaults.update(overrides)
    return InputScope(**defaults)


def test_render_basic_finding() -> None:
    """A single finding renders with all expected fields."""
    renderer = EvaluationReportRenderer()
    report = renderer.render(
        test_path="wpt/css/css-flexbox/align-content_center.html",
        findings=[_sample_finding()],
        input_scope=_sample_scope(),
    )

    # Top-level header
    assert (
        "# Findings: wpt/css/css-flexbox/align-content_center.html" in report
    )

    # Finding section + fields
    assert "### Finding 1 — missing character encoding declaration" in report
    assert "**Severity**: warn" in report
    assert "**Test line**: Lines 1-4" in report
    assert (
        "**Source**: `wpt/docs/writing-tests/general-guidelines.md:L82-L87`"
        in report
    )
    assert "**Summary**: HTML must declare encoding." in report

    # Evidence is code-fenced
    assert "```\n  <!DOCTYPE html>\n  ```" in report


def test_render_multiline_evidence_stays_inside_code_fence() -> None:
    """Multi-line evidence renders within a single fenced block."""
    renderer = EvaluationReportRenderer()
    evidence = "<head>\n  <title>foo</title>\n  <meta>"
    report = renderer.render(
        test_path="wpt/foo/bar.html",
        findings=[_sample_finding(evidence=evidence)],
        input_scope=_sample_scope(),
    )

    # Verify each line of the evidence is inside the fence (indented).
    assert "  <head>" in report
    assert "  <title>foo</title>" in report
    assert "  <meta>" in report

    # Verify the fenced block is well-formed: opening fence, content,
    # closing fence — and that we have exactly two fence markers for
    # this finding's evidence.
    fence_lines = [
        line for line in report.splitlines() if line.strip() == "```"
    ]
    assert len(fence_lines) == 2


def test_render_empty_findings_shows_fallback() -> None:
    renderer = EvaluationReportRenderer()
    report = renderer.render(
        test_path="wpt/foo/bar.html",
        findings=[],
        input_scope=_sample_scope(),
    )
    assert "No findings raised." in report
    # Input scope still renders.
    assert "## Input scope" in report


def test_render_input_scope_table_format() -> None:
    """The Input scope table uses comma-formatted bytes and a Total row."""
    renderer = EvaluationReportRenderer()
    scope = InputScope(
        files=[
            InputScopeFile(path="a.md", bytes=1_500, role="skill"),
            InputScopeFile(path="b.md", bytes=12_345, role="reading-list"),
            InputScopeFile(path="c.html", bytes=968, role="test"),
        ],
        approach="doc-inputs",
    )
    report = renderer.render(
        test_path="wpt/c.html", findings=[], input_scope=scope
    )

    # Each row shows comma-formatted bytes.
    assert "| a.md | 1,500 | skill |" in report
    assert "| b.md | 12,345 | reading-list |" in report
    assert "| c.html | 968 | test |" in report
    # Total row matches total_bytes (1500 + 12345 + 968 = 14813).
    assert "**Total** | **14,813**" in report
    # Token estimate is total_bytes // 4 = 3703.
    assert "Approximate input tokens: ~3,703" in report


def test_render_no_dependencies_says_none() -> None:
    renderer = EvaluationReportRenderer()
    report = renderer.render(
        test_path="wpt/foo/bar.html",
        findings=[],
        input_scope=_sample_scope(dependencies_not_read=[]),
    )
    assert "Declared dependencies (not read): none" in report


def test_render_dependencies_comma_separated() -> None:
    renderer = EvaluationReportRenderer()
    deps = ["/resources/testharness.js", "http://example.com/foo.js"]
    report = renderer.render(
        test_path="wpt/foo/bar.html",
        findings=[],
        input_scope=_sample_scope(dependencies_not_read=deps),
    )
    assert (
        "Declared dependencies (not read): "
        "/resources/testharness.js, http://example.com/foo.js"
    ) in report


def test_render_approach_label_appears() -> None:
    """The approach label flows through to the rendered Markdown."""
    renderer = EvaluationReportRenderer()
    scope = _sample_scope(approach="some-other-variant")
    report = renderer.render(
        test_path="wpt/foo/bar.html",
        findings=[],
        input_scope=scope,
    )
    assert "Approach: some-other-variant" in report


# ---------------------------------------------------------------------------
# run_evaluation integration (agent mocked)
# ---------------------------------------------------------------------------


@pytest.fixture
def wpt_root_with_test(tmp_path: Path) -> tuple[Path, Path]:
    """Creates a fake WPT root with a single test file inside it."""
    wpt = tmp_path / "wpt"
    wpt.mkdir()
    test = wpt / "foo.html"
    test.write_text("<!doctype html><title>hi</title>", encoding="utf-8")
    return wpt, test


@pytest.fixture
def evaluation_config(
    wpt_root_with_test: tuple[Path, Path], tmp_path: Path
) -> Config:
    wpt_root, _ = wpt_root_with_test
    return Config(
        provider="anthropic",
        default_model="test-model",
        api_key="test-key",
        wpt_path=str(wpt_root),
        cache_path=str(tmp_path / "cache"),
        categories={"lightweight": "fast", "reasoning": "smart"},
        phase_model_mapping={
            "requirements_extraction": "reasoning",
            "coverage_audit": "reasoning",
            "generation": "lightweight",
        },
    )


@pytest.mark.asyncio
async def test_run_evaluation_writes_report_when_agent_succeeds(
    wpt_root_with_test: tuple[Path, Path],
    evaluation_config: Config,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Happy path: agent returns a payload, report is rendered and written."""
    _, test_path = wpt_root_with_test
    output_dir = tmp_path / "out"

    agent_payload = {
        "findings": [
            {
                "title": "missing charset",
                "severity": "warn",
                "test_line": "Lines 1-4",
                "evidence": "<!doctype html>",
                "source": (
                    "wpt/docs/writing-tests/general-guidelines.md:L82-L87"
                ),
                "summary": "HTML must declare encoding.",
            }
        ],
        "input_scope": {
            "files": [{"path": "foo.html", "bytes": 30, "role": "test"}],
            "dependencies_not_read": [],
            "approach": "doc-inputs",
        },
    }

    mock_agent = AsyncMock(return_value=agent_payload)
    monkeypatch.setattr(
        "wptgen.phases.evaluation.evaluate_test_with_adk", mock_agent
    )

    report_path = await run_evaluation(
        test_path=test_path,
        output_dir=output_dir,
        config=evaluation_config,
        jinja_env=MagicMock(),
        ui=MagicMock(),
    )

    assert report_path is not None
    assert report_path.is_file()
    contents = report_path.read_text(encoding="utf-8")
    assert "# Findings:" in contents
    assert "### Finding 1 — missing charset" in contents
    assert "Approach: doc-inputs" in contents
    # The mocked agent was actually called.
    mock_agent.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_evaluation_returns_none_when_agent_returns_none(
    wpt_root_with_test: tuple[Path, Path],
    evaluation_config: Config,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Agent failure / empty response: no report file is written."""
    _, test_path = wpt_root_with_test
    output_dir = tmp_path / "out"

    monkeypatch.setattr(
        "wptgen.phases.evaluation.evaluate_test_with_adk",
        AsyncMock(return_value=None),
    )

    report_path = await run_evaluation(
        test_path=test_path,
        output_dir=output_dir,
        config=evaluation_config,
        jinja_env=MagicMock(),
        ui=MagicMock(),
    )

    assert report_path is None
    # The output directory should not have been populated with a report.
    assert not output_dir.exists() or not any(output_dir.iterdir())
