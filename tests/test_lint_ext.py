"""Tests for the deterministic linter extension (wptgen.lint_ext).

Each check is named with its rules.yaml id; these tests assert the gap-set
checks fire on violations and stay quiet on clean input.
"""

from wptgen.lint_ext import check_file


def _rule_ids(path: str, content: bytes) -> list[str]:
    return [err[0] for err in check_file(path, content)]


def test_clean_reftest_has_no_gap_findings() -> None:
    """A well-formed reftest triggers none of the gap checks."""
    content = (
        b"<!DOCTYPE html>\n<html>\n<head>\n"
        b'<link rel="match" href="ref.html">\n'
        b'<link rel="help" href="http://example.org/#x">\n'
        b"</head>\n<body>\n<p>Test passes if green.</p>\n</body>\n</html>\n"
    )
    assert _rule_ids("css/foo/align_center.html", content) == []


def test_name_004_flags_manual_suffix_not_last() -> None:
    assert "NAME-004" in _rule_ids("bar-manual-other.html", b"<!doctype html>")


def test_name_004_quiet_when_manual_is_last() -> None:
    assert "NAME-004" not in _rule_ids("bar-manual.html", b"<!doctype html>")


def test_rev_003_flags_commented_out_code() -> None:
    ids = _rule_ids("t.any.js", b"// doThing();\nassert_true(1);")
    assert "REV-003" in ids


def test_rev_003_quiet_on_prose_comment() -> None:
    ids = _rule_ids("t.any.js", b"// this is a prose comment\nassert_true(1);")
    assert "REV-003" not in ids


def test_api_005_flags_manual_setup_without_explicit_timeout() -> None:
    assert "API-005" in _rule_ids("m-manual.html", b"setup();\n")


def test_api_005_quiet_with_explicit_timeout() -> None:
    ids = _rule_ids("m-manual.html", b"setup({explicit_timeout: true});\n")
    assert "API-005" not in ids


def test_api_005_quiet_on_non_manual_test() -> None:
    """The gate: an ordinary (non-manual) test's setup() is not flagged."""
    assert "API-005" not in _rule_ids("m.html", b"setup();\n")
    assert "API-005" not in _rule_ids("m.any.js", b"setup();\n")


def test_name_011_flags_crash_suffix_not_last() -> None:
    assert "NAME-011" in _rule_ids("bar-crash-001.html", b"<!doctype html>")


def test_name_011_quiet_when_crash_is_last() -> None:
    assert "NAME-011" not in _rule_ids("bar-crash.html", b"<!doctype html>")


def test_name_011_quiet_under_crashtests_dir() -> None:
    ids = _rule_ids("css/crashtests/bar-crash-001.html", b"<!doctype html>")
    assert "NAME-011" not in ids


def test_name_012_flags_print_suffix_not_last() -> None:
    assert "NAME-012" in _rule_ids("bar-print-001.html", b"<!doctype html>")


def test_name_012_quiet_under_print_dir() -> None:
    assert "NAME-012" not in _rule_ids("css/print/bar-print-1.html", b"x")


def test_name_006_flags_token_not_before_js() -> None:
    assert "NAME-006" in _rule_ids("foo.any.bar.js", b"x")


def test_name_006_quiet_when_token_before_js() -> None:
    assert "NAME-006" not in _rule_ids("foo.any.js", b"x")


def test_meta_008_flags_deprecated_css_flag() -> None:
    content = b'<meta name=flags content="animated">'
    assert "META-008" in _rule_ids("t.html", content)


def test_meta_008_quiet_on_non_deprecated_flags() -> None:
    content = b'<meta name=flags content="dom">'
    assert "META-008" not in _rule_ids("t.html", content)


def test_fmt_004_flags_worker_missing_importscripts() -> None:
    ids = _rule_ids("t.worker.js", b"done();")
    assert "FMT-004" in ids


def test_fmt_004_flags_worker_missing_done() -> None:
    content = b'importScripts("/resources/testharness.js");'
    assert "FMT-004" in _rule_ids("t.worker.js", content)


def test_fmt_004_quiet_on_complete_worker() -> None:
    content = (
        b'importScripts("/resources/testharness.js");\n'
        b"test(() => {});\ndone();\n"
    )
    assert "FMT-004" not in _rule_ids("t.worker.js", content)


def test_fmt_004_only_applies_to_worker_js() -> None:
    """A non-worker file is never flagged for FMT-004 even if it lacks both."""
    assert "FMT-004" not in _rule_ids("t.any.js", b"assert_true(1);")


def test_check_file_reports_line_numbers_for_line_checks() -> None:
    """Line-pattern checks report a 1-indexed line number."""
    content = b"<!doctype html>\n// foo();\n"
    errors = check_file("t.any.js", content)
    rev = [e for e in errors if e[0] == "REV-003"]
    assert len(rev) == 1
    assert rev[0][3] == 2
