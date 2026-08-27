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

"""Tests for the benchmark provenance fingerprint."""

from __future__ import annotations

from pathlib import Path

import benchmark.provenance as provenance
from typing import Any

from benchmark.provenance import Provenance, compute_provenance


def _prov(manifest: Path, **kw: Any) -> Provenance:
    defaults: dict[str, Any] = {
        "model": "anthropic/claude-x",
        "wpt_commit": "abc123",
        "evaluator_version": "0.3.0",
    }
    defaults.update(kw)
    return compute_provenance(manifest_path=manifest, **defaults)


def test_fingerprint_is_stable_for_identical_inputs(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("version: 1\n", encoding="utf-8")
    assert _prov(manifest).fingerprint == _prov(manifest).fingerprint


def test_model_change_moves_fingerprint_not_subhashes(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("version: 1\n", encoding="utf-8")
    a = _prov(manifest, model="anthropic/claude-x")
    b = _prov(manifest, model="gemini/gemini-y")
    assert a.fingerprint != b.fingerprint
    # A model swap is result-affecting but touches no input file.
    assert a.rules_digest == b.rules_digest
    assert a.labels_digest == b.labels_digest


def test_wpt_commit_change_moves_fingerprint(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("version: 1\n", encoding="utf-8")
    a = _prov(manifest, wpt_commit="aaa")
    b = _prov(manifest, wpt_commit="bbb")
    assert a.fingerprint != b.fingerprint


def test_manifest_edit_moves_labels_and_fingerprint_only(
    tmp_path: Path, monkeypatch: Any
) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("version: 1\n", encoding="utf-8")
    # Pin the seed set empty so only the manifest bytes vary.
    monkeypatch.setattr(provenance, "_seed_files", lambda: [])
    before = _prov(manifest)
    manifest.write_text("version: 1  # edited\n", encoding="utf-8")
    after = _prov(manifest)
    assert after.labels_digest != before.labels_digest
    assert after.rules_digest == before.rules_digest
    assert after.fingerprint != before.fingerprint


def test_evaluator_version_is_carried_but_not_hashed(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("version: 1\n", encoding="utf-8")
    a = _prov(manifest, evaluator_version="0.3.0")
    b = _prov(manifest, evaluator_version="0.4.0")
    # The human-facing version is intent, recorded but not part of the truth
    # hash — so a bump with no input change leaves the fingerprint identical.
    assert a.evaluator_version == "0.3.0"
    assert b.evaluator_version == "0.4.0"
    assert a.fingerprint == b.fingerprint


def test_short_digests_have_expected_width(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("version: 1\n", encoding="utf-8")
    p = _prov(manifest)
    assert len(p.short) == 12
    assert len(p.rules_short) == 12
    assert len(p.labels_short) == 12
