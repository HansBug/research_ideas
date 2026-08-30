"""Validate the provider-free invariants of the paper1 release refactor.

The validator reads the pre-refactor baseline manifest, the frozen archive,
and the relocated package tree.  It never imports a provider adapter, writes
an experiment artifact, or evaluates a model.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


PAPER_ROOT = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover")
ARCHIVE = PAPER_ROOT / "final_results" / "v60_current_vs_x1v2_baseline"
BASELINE = PAPER_ROOT / "release" / "baseline_manifest.json"
DOCUMENTATION_CHANGES = PAPER_ROOT / "release" / "documentation_audit" / "final_archive_documentation_changes.json"
TEST_UNIVERSE_CHANGES = PAPER_ROOT / "release" / "documentation_audit" / "test_universe_change.json"


class ValidationResult(BaseModel):
    """Machine-readable result of one offline release-structure validation."""

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    schema_id: Literal["paper1.release-structure-validation.v1"] = Field(
        alias="schema",
        description="Versioned schema identifier for this release validation."
    )
    frozen_archive_files_checked: int = Field(
        ge=0, description="Number of final-results files checked against the baseline or an approved documentation change."
    )
    documented_archive_change_paths: tuple[str, ...] = Field(
        description="Narrow set of non-data archive paths approved for this documentation-only update."
    )
    baseline_node_count: int = Field(
        ge=1, description="Number of historical pytest nodes required by the baseline."
    )
    current_node_count: int = Field(
        ge=1, description="Number of historical pytest nodes collected after relocation."
    )
    resource_hashes: dict[str, str] = Field(
        description="Named byte-identical resource SHA-256 values verified by this run."
    )
    boundary_violations: tuple[str, ...] = Field(
        description="Forbidden package import observations; must be empty for acceptance."
    )
    provider_call_count: Literal[0] = Field(
        description="Provider calls made by this validator; it is structurally zero."
    )
    billable_call_count: Literal[0] = Field(
        description="Billable calls made by this validator; it is structurally zero."
    )
    reason: str = Field(description="Human-readable validation conclusion.")
    basis: str = Field(description="Baseline, archive, resource, and AST evidence used.")


class DocumentedArchivePathChange(BaseModel):
    """One bounded final-results documentation path allowed to differ from the refactor baseline."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str = Field(description="Repository-relative path of the documented archive change.")
    baseline_bytes: int = Field(ge=0, description="Byte count recorded by the release-refactor baseline.")
    baseline_sha256: str = Field(description="Baseline SHA-256 prefixed with sha256:.")
    current_bytes: int = Field(ge=0, description="Expected byte count after the documentation-only update.")
    current_sha256: str = Field(description="Expected current SHA-256 prefixed with sha256:.")
    reason: str = Field(description="Why this path may change without changing experiment evidence.")
    basis: str = Field(description="Command or manifest basis for the approved change.")


class FinalArchiveDocumentationChanges(BaseModel):
    """Bounded exception record for current-facing archive documentation maintenance."""

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    schema_id: Literal["paper1.final-archive-documentation-changes.v1"] = Field(
        alias="schema", description="Versioned schema identifier for this exception record."
    )
    archive_root: str = Field(description="Repository-relative frozen archive root covered by this record.")
    baseline_manifest: str = Field(description="Release baseline manifest that supplies original file identities.")
    protected_prefixes: tuple[str, ...] = Field(
        description="Archive-relative evidence prefixes that no documentation exception may change."
    )
    protected_file_count: int = Field(
        ge=0, description="Number of raw, derived, and reference baseline files kept byte-identical."
    )
    allowed_changes: tuple[DocumentedArchivePathChange, ...] = Field(
        description="Exact non-data files and hashes permitted to differ from the release baseline."
    )
    provider_call_count: Literal[0] = Field(
        description="Provider calls made to produce this documentation record; structurally zero."
    )
    billable_call_count: Literal[0] = Field(
        description="Billable calls made to produce this documentation record; structurally zero."
    )
    reason: str = Field(description="Why the documentation update is compatible with frozen experiment evidence.")
    basis: str = Field(description="Baseline manifest, authoritative finalizer, and byte-level comparison basis.")


class ApprovedTestNodeAddition(BaseModel):
    """One explicitly reviewed pytest node added after the release baseline."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    node_id: str = Field(description="Exact repository-relative pytest node ID approved as an additive test.")
    source_path: str = Field(description="Repository-relative source file defining the approved node.")
    source_sha256: str = Field(description="SHA-256 of the complete source file containing the approved node.")
    introduced_by_commit: str = Field(description="Git commit that added the source file and approved nodes.")
    reason: str = Field(description="Why the node is a necessary provider-free release invariant test.")
    basis: str = Field(description="Source, commit, and collection evidence for the addition.")


class TestUniverseChange(BaseModel):
    """Hash-pinned exception for a known additive test change after baseline capture."""

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    schema_id: Literal["paper1.test-universe-change.v1"] = Field(
        alias="schema", description="Versioned schema identifier for this test-universe exception."
    )
    baseline_manifest: str = Field(description="Release baseline manifest supplying the original node universe.")
    baseline_node_count: int = Field(ge=1, description="Number of nodes in the immutable release baseline.")
    baseline_node_ids_sha256: str = Field(description="Digest of the baseline node IDs in stored order.")
    approved_added_nodes: tuple[ApprovedTestNodeAddition, ...] = Field(
        min_length=1,
        description="Complete set of explicitly approved additive nodes; no other node change is permitted.",
    )
    current_node_count: int = Field(ge=1, description="Expected current node count after the approved additions.")
    current_node_ids_sha256: str = Field(description="Digest of the expected current sorted node IDs.")
    provider_call_count: Literal[0] = Field(description="Provider calls used to establish this exception; structurally zero.")
    billable_call_count: Literal[0] = Field(description="Billable calls used to establish this exception; structurally zero.")
    reason: str = Field(description="Why the additive tests do not alter production or experiment evidence.")
    basis: str = Field(description="Baseline manifest, source hash, Git history, and provider-free collection evidence.")


def _hash(path: Path) -> str:
    """Return the exact SHA-256 of one file without normalizing its bytes."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _imports(path: Path) -> tuple[str, ...]:
    """Return explicit absolute imports from one Python source file."""

    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            values.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            values.append(node.module)
    return tuple(values)


def _scan_boundary(root: Path, forbidden: tuple[str, ...]) -> tuple[str, ...]:
    """Find imports crossing a declared one-way package boundary."""

    violations: list[str] = []
    for source in sorted(root.rglob("*.py")):
        for module in _imports(source):
            if any(module == value or module.startswith(value + ".") for value in forbidden):
                violations.append(f"{source.relative_to(root)} imports {module}")
    return tuple(violations)


def _collect_nodes(repository: Path, python: Path) -> tuple[str, ...]:
    """Collect the historical test universe without importing a provider client."""

    environment = dict(os.environ)
    sources = [
        repository / PAPER_ROOT / "method" / "src",
        repository / PAPER_ROOT / "judge" / "src",
        repository / PAPER_ROOT / "evaluation" / "src",
        repository / PAPER_ROOT,
    ]
    environment["PYTHONPATH"] = ":".join(str(path) for path in sources)
    targets = (
        PAPER_ROOT / "pipeline" / "evidence_discovery" / "tests",
        PAPER_ROOT / "pipeline" / "semantic_judge" / "tests",
    )
    output = subprocess.check_output(
        (str(python), "-m", "pytest", *(str(path) for path in targets), "--collect-only", "-q"),
        cwd=repository,
        text=True,
        env=environment,
        stderr=subprocess.STDOUT,
    )
    return tuple(sorted(line.strip() for line in output.splitlines() if "::" in line))


def _documentation_changes(repository: Path, baseline: dict[str, object]) -> dict[str, DocumentedArchivePathChange]:
    """Load a narrow, hash-pinned documentation exception without weakening data checks."""

    record = FinalArchiveDocumentationChanges.model_validate_json(
        (repository / DOCUMENTATION_CHANGES).read_text(encoding="utf-8")
    )
    if record.archive_root != ARCHIVE.as_posix() or record.baseline_manifest != BASELINE.as_posix():
        raise RuntimeError("documentation change record targets the wrong archive or baseline")
    if record.protected_prefixes != ("raw/", "derived/", "reference/"):
        raise RuntimeError("documentation change record weakens protected archive prefixes")
    baseline_files = {
        str(item["path"]): item
        for item in baseline["frozen_archive_files"]
        if isinstance(item, dict)
    }
    expected_protected_count = sum(
        path.startswith(str(ARCHIVE) + "/" + prefix)
        for path in baseline_files
        for prefix in record.protected_prefixes
    )
    if record.protected_file_count != expected_protected_count:
        raise RuntimeError("documentation change record has the wrong protected-file count")
    changes: dict[str, DocumentedArchivePathChange] = {}
    for change in record.allowed_changes:
        if change.path in changes or change.path not in baseline_files:
            raise RuntimeError("documentation change record contains duplicate or unknown path")
        if any(change.path == str(ARCHIVE / prefix.rstrip("/")) or change.path.startswith(str(ARCHIVE / prefix)) for prefix in record.protected_prefixes):
            raise RuntimeError("documentation change record cannot alter raw, derived, or reference evidence")
        original = baseline_files[change.path]
        if original.get("bytes") != change.baseline_bytes or original.get("sha256") != change.baseline_sha256:
            raise RuntimeError("documentation change record does not match the release baseline")
        changes[change.path] = change
    expected_paths = {
        str(ARCHIVE / "README.md"),
        str(ARCHIVE / "SCHEMA.md"),
        str(ARCHIVE / "archive_manifest.json"),
        str(ARCHIVE / "publication_manifest.json"),
        str(ARCHIVE / "report/v60_current_vs_x1v2_baseline_cn.md"),
        str(ARCHIVE / "reviews/01_numeric_recomputation_review.md"),
    }
    if set(changes) != expected_paths:
        raise RuntimeError("documentation change record must be limited to current-facing docs and root manifests")
    return changes


def _test_universe_change(repository: Path, baseline: dict[str, object]) -> TestUniverseChange:
    """Load and validate the exact, hash-pinned additive test exception."""

    record = TestUniverseChange.model_validate_json(
        (repository / TEST_UNIVERSE_CHANGES).read_text(encoding="utf-8")
    )
    if record.baseline_manifest != BASELINE.as_posix():
        raise RuntimeError("test-universe exception targets the wrong baseline manifest")
    expected_nodes = tuple(baseline["test_baseline"]["node_ids"])
    expected_hash = baseline["test_baseline"]["node_ids_sha256"]
    if record.baseline_node_count != len(expected_nodes) or record.baseline_node_ids_sha256 != expected_hash:
        raise RuntimeError("test-universe exception does not match the immutable baseline")
    node_ids = tuple(item.node_id for item in record.approved_added_nodes)
    if len(set(node_ids)) != len(node_ids) or any(node_id in expected_nodes for node_id in node_ids):
        raise RuntimeError("test-universe exception contains duplicate or historical nodes")
    source_paths = {item.source_path for item in record.approved_added_nodes}
    commits = {item.introduced_by_commit for item in record.approved_added_nodes}
    source_hashes = {item.source_sha256 for item in record.approved_added_nodes}
    if source_paths != {
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/evidence_discovery/tests/test_manual_adjudication_v2.py"
    } or commits != {"5f70a12b5797da19d1b5c963fcfd00683b477840"} or len(source_hashes) != 1:
        raise RuntimeError("test-universe exception has an unexpected source or introducing commit")
    source_path = repository / next(iter(source_paths))
    if _hash(source_path) != next(iter(source_hashes)):
        raise RuntimeError("approved additive test source hash changed")
    if subprocess.run(
        ("git", "merge-base", "--is-ancestor", next(iter(commits)), "HEAD"),
        cwd=repository,
        check=False,
    ).returncode != 0:
        raise RuntimeError("approved additive test commit is not an ancestor of HEAD")
    return record


def validate(repository: Path, python: Path) -> ValidationResult:
    """Validate frozen archive hashes, historical test nodes, resources, and imports."""

    baseline = json.loads((repository / BASELINE).read_text(encoding="utf-8"))
    changes = _documentation_changes(repository, baseline)
    test_universe_change = _test_universe_change(repository, baseline)
    missing_or_changed = [
        item["path"]
        for item in baseline["frozen_archive_files"]
        if not (repository / item["path"]).is_file()
        or (repository / item["path"]).stat().st_size
        != (changes[item["path"]].current_bytes if item["path"] in changes else item["bytes"])
        or _hash(repository / item["path"])
        != (changes[item["path"]].current_sha256 if item["path"] in changes else item["sha256"])
    ]
    if missing_or_changed:
        raise RuntimeError("frozen final-results hash mismatch: " + ", ".join(missing_or_changed[:5]))
    expected_nodes = tuple(baseline["test_baseline"]["node_ids"])
    current_nodes = _collect_nodes(repository, python)
    approved_nodes = tuple(sorted(item.node_id for item in test_universe_change.approved_added_nodes))
    expected_current_nodes = tuple(sorted((*expected_nodes, *approved_nodes)))
    if current_nodes != expected_current_nodes:
        added = sorted(set(current_nodes) - set(expected_nodes))
        missing = sorted(set(expected_current_nodes) - set(current_nodes))
        raise RuntimeError(
            "pytest node universe differs from baseline plus approved additions: "
            f"added={added[:5]}, missing={missing[:5]}"
        )
    if len(current_nodes) != test_universe_change.current_node_count:
        raise RuntimeError("test-universe exception has the wrong current node count")
    current_payload = "\n".join(current_nodes).encode("utf-8")
    if "sha256:" + hashlib.sha256(current_payload).hexdigest() != test_universe_change.current_node_ids_sha256:
        raise RuntimeError("test-universe exception has the wrong current node hash")
    resources = {
        "registry": _hash(repository / PAPER_ROOT / "method/src/paper_stm_method/resources/predicate_registry.json"),
        "source_catalog": _hash(repository / PAPER_ROOT / "method/src/paper_stm_method/resources/current_source_catalog.json"),
        "judge_protocol": _hash(repository / PAPER_ROOT / "judge/src/paper_stm_judge/resources/semantic_judge_issue_195.snapshot.md"),
    }
    anchors = baseline["known_frozen_anchors"]
    if resources["registry"] != anchors["registry_hash"]:
        raise RuntimeError("predicate registry hash changed")
    if resources["judge_protocol"].removeprefix("sha256:") != anchors["judge_protocol_sha256"]:
        raise RuntimeError("Judge protocol snapshot hash changed")
    package_roots = {
        "method": repository / PAPER_ROOT / "method/src/paper_stm_method",
        "judge": repository / PAPER_ROOT / "judge/src/paper_stm_judge",
        "evaluation": repository / PAPER_ROOT / "evaluation/src/paper_stm_evaluation",
        "utils": repository / "utils",
    }
    violations = (
        _scan_boundary(package_roots["method"], ("paper_stm_judge", "paper_stm_evaluation", "pipeline.semantic_judge", "discover_matrix"))
        + _scan_boundary(package_roots["judge"], ("paper_stm_method", "paper_stm_evaluation", "pipeline.evidence_discovery", "discover_matrix.ledger"))
        + _scan_boundary(package_roots["utils"], ("paper_stm_method", "paper_stm_judge", "paper_stm_evaluation", "pipeline.evidence_discovery", "pipeline.semantic_judge"))
    )
    return ValidationResult(
        schema_id="paper1.release-structure-validation.v1",
        frozen_archive_files_checked=len(baseline["frozen_archive_files"]),
        documented_archive_change_paths=tuple(sorted(changes)),
        baseline_node_count=len(expected_nodes),
        current_node_count=len(current_nodes),
        resource_hashes=resources,
        boundary_violations=violations,
        provider_call_count=0,
        billable_call_count=0,
        reason="Frozen data, bounded documentation changes, historical node IDs, resource hashes, and one-way import boundaries were checked without provider access.",
        basis="release/baseline_manifest.json, documentation exception hashes, byte-level SHA-256, pytest collection, and Python AST imports.",
    )


def main(argv: list[str] | None = None) -> int:
    """Execute the release validator and fail on any frozen or boundary violation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--python", type=Path, default=Path("venv/bin/python"))
    arguments = parser.parse_args(argv)
    # Do not resolve the interpreter path: resolving ``venv/bin/python`` can
    # dereference it to the base interpreter and discard the project venv.
    result = validate(arguments.repository_root.resolve(), arguments.python)
    if result.boundary_violations:
        raise RuntimeError("import boundary violation: " + "; ".join(result.boundary_violations))
    print(result.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
