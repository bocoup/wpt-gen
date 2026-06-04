"""Tests for adk_conformance_evaluator.py."""

import pytest

pytest.importorskip("google.adk")

from wptgen.agents.adk_conformance_evaluator import (  # noqa: E402
    _EVALUATOR_TOOL_ALLOWLIST as CONFORMANCE_ALLOWLIST,
)
from wptgen.agents.adk_evaluator import (  # noqa: E402
    _EVALUATOR_TOOL_ALLOWLIST as DOC_INPUTS_ALLOWLIST,
)


def test_conformance_evaluator_shares_doc_inputs_allowlist() -> None:
    """The two evaluator variants intentionally share one read-only allowlist.

    Both evaluators must remain read-only; sharing the allowlist means a
    change in one place is caught by both pin tests. If the conformance
    agent ever needs a different (still read-only) toolset, fork the
    allowlist deliberately and add a separate pin.
    """
    assert CONFORMANCE_ALLOWLIST is DOC_INPUTS_ALLOWLIST
