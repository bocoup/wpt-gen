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
"""Provenance fingerprint for a benchmark run.

The evaluator carries one human-facing version (``evaluator_version`` in
``wpt-gen.yml``) that a maintainer bumps whenever anything that can change the
numbers changes: the skill/rules, the manifest or test files, the model
config, or the pinned wpt commit. That version is *intent* — "this is a new
version, re-run the release tier."

The fingerprint here is *truth*: a content hash of the actual inputs, computed
at run time, so a report records exactly what produced its numbers. If two
runs share an ``evaluator_version`` but differ in fingerprint, someone edited
an input and forgot to bump — the machine catches the drift a hand-maintained
version cannot.

The fingerprint is split into two sub-hashes so the report can say something
more specific than "an input changed":

* ``rules`` — ``rules.yaml`` + ``SKILL.md`` (the evaluator's judgment).
* ``labels`` — ``manifest.yaml`` + every seed file (the ground truth the
  ``expect`` labels are authored against).

A ``rules`` change with unchanged ``labels`` is exactly the case the old
``manifest.rules_version`` tripwire tried to flag by hand: the rules moved, so
the seed labels are due for re-review.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from benchmark.manifest import REPO_ROOT

_RULES_PATH = (
    REPO_ROOT
    / "wptgen"
    / "skills"
    / "wpt-evaluator"
    / "references"
    / "rules.yaml"
)
_SKILL_PATH = REPO_ROOT / "wptgen" / "skills" / "wpt-evaluator" / "SKILL.md"
_SEEDS_ROOT = REPO_ROOT / "benchmarks" / "seeds"

# Short-hash width shown in reports. Long enough to make a collision between
# two real input sets vanishingly unlikely, short enough to eyeball.
_SHORT = 12


@dataclass(frozen=True)
class Provenance:
    """The version stamp for one benchmark run."""

    evaluator_version: str  # human-facing semver from wpt-gen.yml
    fingerprint: str  # full hex digest over all inputs
    rules_digest: str  # sub-hash: rules.yaml + SKILL.md
    labels_digest: str  # sub-hash: manifest.yaml + seed files
    model: str  # resolved "provider/model", part of the fingerprint
    wpt_commit: str | None  # pinned upstream commit, part of the fingerprint

    @property
    def short(self) -> str:
        return self.fingerprint[:_SHORT]

    @property
    def rules_short(self) -> str:
        return self.rules_digest[:_SHORT]

    @property
    def labels_short(self) -> str:
        return self.labels_digest[:_SHORT]


def _hash_paths(paths: list[Path]) -> str:
    """SHA-256 over the contents of ``paths``, in the given order.

    Each file is folded in as ``<repo-relative-path>\\0<bytes>\\0`` so a rename
    changes the digest even when bytes are identical. Missing files fold in as
    empty, so a deleted input still moves the hash rather than being skipped.
    """
    h = hashlib.sha256()
    for path in paths:
        try:
            rel = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = path.as_posix()
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        try:
            h.update(path.read_bytes())
        except OSError:
            pass
        h.update(b"\0")
    return h.hexdigest()


def _seed_files() -> list[Path]:
    """All seed files under ``benchmarks/seeds/``, sorted for a stable hash."""
    if not _SEEDS_ROOT.is_dir():
        return []
    return sorted(p for p in _SEEDS_ROOT.rglob("*") if p.is_file())


def compute_provenance(
    manifest_path: Path,
    model: str,
    wpt_commit: str | None,
    evaluator_version: str,
) -> Provenance:
    """Computes the provenance stamp for a run.

    ``model`` is the resolved ``provider/model`` string, and ``wpt_commit`` the
    manifest's pinned upstream commit; both feed the top-level fingerprint (a
    model or pin change is a result-affecting change) but neither belongs to
    the file-content sub-hashes.
    """
    rules_digest = _hash_paths([_RULES_PATH, _SKILL_PATH])
    labels_digest = _hash_paths([manifest_path, *_seed_files()])

    combined = hashlib.sha256()
    combined.update(rules_digest.encode("ascii"))
    combined.update(labels_digest.encode("ascii"))
    combined.update((model or "").encode("utf-8"))
    combined.update((wpt_commit or "").encode("utf-8"))

    return Provenance(
        evaluator_version=evaluator_version,
        fingerprint=combined.hexdigest(),
        rules_digest=rules_digest,
        labels_digest=labels_digest,
        model=model,
        wpt_commit=wpt_commit,
    )
