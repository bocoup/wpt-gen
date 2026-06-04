"""Tests for adk_evaluator.py."""

import pytest

pytest.importorskip("google.adk")

from wptgen.agents.adk_evaluator import _EVALUATOR_TOOL_ALLOWLIST


def test_evaluator_tool_allowlist_is_pinned() -> None:
    assert _EVALUATOR_TOOL_ALLOWLIST == frozenset(
        {
            "read_file",
            "list_directory",
            "search_files",
            "search_file_contents",
            "run_wpt_lint",
        }
    )
