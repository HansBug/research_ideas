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


class ValidationResult(BaseModel):
    """Machine-readable result of one offline release-structure validation."""

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    schema_id: Literal["paper1.release-structure-validation.v1"] = Field(
        alias="schema",
        description="Versioned schema identifier for this release validation."
    )
    frozen_archive_files_checked: int = Field(
        ge=0, description="Number of immutable final-results files hash-checked."
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


def validate(repository: Path, python: Path) -> ValidationResult:
    """Validate frozen archive hashes, historical test nodes, resources, and imports."""

    baseline = json.loads((repository / BASELINE).read_text(encoding="utf-8"))
    missing_or_changed = [
        item["path"]
        for item in baseline["frozen_archive_files"]
        if not (repository / item["path"]).is_file()
        or _hash(repository / item["path"]) != item["sha256"]
    ]
    if missing_or_changed:
        raise RuntimeError("frozen final-results hash mismatch: " + ", ".join(missing_or_changed[:5]))
    expected_nodes = tuple(baseline["test_baseline"]["node_ids"])
    current_nodes = _collect_nodes(repository, python)
    if current_nodes != expected_nodes:
        raise RuntimeError("historical pytest node universe changed")
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
        baseline_node_count=len(expected_nodes),
        current_node_count=len(current_nodes),
        resource_hashes=resources,
        boundary_violations=violations,
        provider_call_count=0,
        billable_call_count=0,
        reason="Frozen artifacts, historical node IDs, resource hashes, and one-way import boundaries were checked without provider access.",
        basis="release/baseline_manifest.json, byte-level SHA-256, pytest collection, and Python AST imports.",
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
