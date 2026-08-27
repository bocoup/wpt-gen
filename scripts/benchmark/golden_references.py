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
"""Reftest reference resolution, shared by the harvester and the harness.

A reftest links its reference with ``<link rel=match>`` / ``rel=mismatch>``.
The golden candidate only captures a PR's *commented* test files, not the
reference files they point at, so a reftest staged without its reference is
mis-flagged for a spurious "reference does not exist" (REFTESTS-001).

The harvester (``harvest_wpt_prs.py``) uses these helpers to capture the
reference bytes *at the test's own commit*, alongside the test, so the pair is
commit-coupled by construction. The harness then stages whatever the candidate
captured, with no checkout lookup.
"""

from __future__ import annotations

import posixpath
import re

_LINK_TAG_RE = re.compile(r"<link\b[^>]*>", re.IGNORECASE)
_MATCH_REL_RE = re.compile(
    r"""rel\s*=\s*["']?\s*(?:mis)?match\b""", re.IGNORECASE
)
_HREF_RE = re.compile(
    r"""href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.IGNORECASE
)


def reference_hrefs(html: str) -> list[str]:
    """The href of every ``<link rel=match|mismatch>`` in an HTML string."""
    hrefs: list[str] = []
    for tag in _LINK_TAG_RE.findall(html):
        if _MATCH_REL_RE.search(tag):
            m = _HREF_RE.search(tag)
            if m:
                hrefs.append(m.group(1) or m.group(2) or m.group(3))
    return hrefs


def resolve_reference(test_rel_path: str, href: str) -> str | None:
    """Resolves a reftest href to a wpt-root-relative path, or None if external.

    Relative hrefs resolve against the test's directory; a leading ``/`` is
    wpt-root-relative. External (``http(s)://``, ``//``, ``data:``) and empty
    hrefs return None.
    """
    href = href.split("#", 1)[0].split("?", 1)[0].strip()
    if not href or href.startswith(("http://", "https://", "//", "data:")):
        return None
    if href.startswith("/"):
        return href.lstrip("/")
    base = posixpath.dirname(test_rel_path)
    return posixpath.normpath(posixpath.join(base, href))
