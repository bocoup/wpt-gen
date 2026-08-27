# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for shared reftest reference resolution."""

from __future__ import annotations

import pytest

from benchmark.golden_references import reference_hrefs, resolve_reference


def test_reference_hrefs_finds_match_and_mismatch() -> None:
    html = (
        '<link rel="match" href="a-ref.html">\n'
        "<link rel=mismatch href='b-ref.html'>\n"
        '<link rel="help" href="ignore.html">'
    )
    assert reference_hrefs(html) == ["a-ref.html", "b-ref.html"]


def test_reference_hrefs_none_when_no_reftest_link() -> None:
    assert reference_hrefs("<div>plain testharness</div>") == []


@pytest.mark.parametrize(
    ("test_path", "href", "expected"),
    [
        # Relative -> resolved against the test's directory.
        ("css/t.html", "reference/t-ref.html", "css/reference/t-ref.html"),
        ("css/t.html", "../ref/x.html", "ref/x.html"),
        # Root-relative -> wpt-root path.
        ("css/deep/t.html", "/css/common-ref.html", "css/common-ref.html"),
        # Fragment / query stripped.
        ("css/t.html", "t-ref.html#frag", "css/t-ref.html"),
    ],
)
def test_resolve_reference_paths(
    test_path: str, href: str, expected: str
) -> None:
    assert resolve_reference(test_path, href) == expected


@pytest.mark.parametrize(
    "href",
    ["https://example.com/r.html", "//cdn/r.html", "data:text/html,x", ""],
)
def test_resolve_reference_external_is_none(href: str) -> None:
    assert resolve_reference("css/t.html", href) is None
