"""Capture a provider-free, machine-readable baseline before a release refactor.

The command reads tracked source and frozen archive files, collects the declared
pytest nodes, and writes one atomic JSON manifest.  It never imports the method
or Judge packages and never initializes a provider client.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HashedFile(BaseModel):
    """One repository-relative file and its immutable SHA-256 digest."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str = Field(description="Repository-relative POSIX path to the file.")
    bytes: int = Field(ge=0, description="Exact byte length at capture time.")
    sha256: str = Field(description="SHA-256 digest prefixed with sha256:.")


class TestBaseline(BaseModel):
    """The exact provider-free pytest collection used as the migration baseline."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    command: tuple[str, ...] = Field(
        description="Exact command tokens used to collect the baseline node IDs."
    )
    pythonpath: str = Field(
        description="PYTHONPATH passed to pytest collection without provider setup."
    )
    node_ids: tuple[str, ...] = Field(
        description="Complete, sorted pytest node IDs that must remain collectable."
    )
    node_ids_sha256: str = Field(
        description="Digest of newline-joined node IDs in their stored order."
    )


class ExternalDependency(BaseModel):
    """One external runtime dependency needed for release reconstruction."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(description="Stable dependency name.")
    value: str = Field(description="Pinned version, commit, or explicit availability value.")
    basis: str = Field(description="How the value was obtained without provider access.")


class ReleaseRefactorBaseline(BaseModel):
    """Complete immutable baseline for a structure-only paper1 release refactor."""

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    schema_id: Literal["paper1.release-refactor-baseline.v1"] = Field(
        alias="schema",
        description="Stable schema identifier for this pre-migration manifest.",
    )
    generated_at_utc: str = Field(description="UTC creation timestamp for audit chronology.")
    repository_head: str = Field(description="Git commit at the start of the refactor.")
    paper_root: str = Field(description="Repository-relative root of the paper1 workspace.")
    known_frozen_anchors: dict[str, str] = Field(
        description="Declared experimental commits, run IDs, and frozen semantic hashes."
    )
    test_baseline: TestBaseline = Field(
        description="Provider-free pytest node universe preserved across migration."
    )
    production_files: tuple[HashedFile, ...] = Field(
        description="Tracked current method, Judge, reporting, and shared-runtime files."
    )
    frozen_archive_files: tuple[HashedFile, ...] = Field(
        description="Every pre-existing final-results file, retained without modification."
    )
    external_dependencies: tuple[ExternalDependency, ...] = Field(
        description="External versions or commits required for later clean-install verification."
    )
    reason: str = Field(description="Why this manifest is sufficient for structural equivalence review.")
    basis: str = Field(description="Commands and source sets used to capture this offline baseline.")


PAPER_ROOT_RELATIVE = Path(
    "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
)
FROZEN_ANCHORS = {
    "v60_method_commit": "66b5d71aecd73f6eeddac082037f7c34e04da057",
    "semantic_judge_commit": "05cf0da6f7d9fcf1de26c349b586fc71c268f1c5",
    "v60_method_run_id": "915d56e45a634c27aa03866f03818c6d",
    "registry_hash": "sha256:38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca",
    "prompt_schema_hash": "sha256:daddf099896d47092b83f08fba907fd1c3f84a3e699bccf890e120d2a286d861",
    "input_hash": "sha256:c89b1aca38bf6104c94de4735d0b682165c01d6092cf2a595fb826a36210fc10",
    "run_contract_hash": "sha256:4375f6071b04d230c7998368c42a36f5d784ae8938085646f0a297239e50cd3d",
    "judge_protocol": "github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2",
    "judge_protocol_sha256": "d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210",
}


def _sha256(path: Path) -> str:
    """Return the exact byte-level SHA-256 of one regular file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_files(repository_root: Path, roots: tuple[Path, ...]) -> tuple[HashedFile, ...]:
    """Hash only tracked regular files, excluding caches and user-owned run outputs."""

    tracked = frozenset(
        line
        for line in _git(repository_root, "ls-files", "-z").split("\0")
        if line
    )
    files: list[HashedFile] = []
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            relative = path.relative_to(repository_root).as_posix()
            if relative not in tracked:
                continue
            files.append(
                HashedFile(
                    path=relative,
                    bytes=path.stat().st_size,
                    sha256=_sha256(path),
                )
            )
    return tuple(files)


def _git(repository_root: Path, *args: str) -> str:
    """Read one Git value without changing repository state."""

    return subprocess.check_output(("git", *args), cwd=repository_root, text=True).strip()


def _collect_nodes(
    repository_root: Path,
    python: Path,
    paper_root: Path,
) -> TestBaseline:
    """Collect the declared method-and-Judge tests without importing a provider config."""

    targets = (
        paper_root / "pipeline" / "evidence_discovery" / "tests",
        paper_root / "pipeline" / "semantic_judge" / "tests",
    )
    command = (
        str(python),
        "-m",
        "pytest",
        *(str(target.relative_to(repository_root)) for target in targets),
        "--collect-only",
        "-q",
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(paper_root.relative_to(repository_root))
    output = subprocess.check_output(
        command, cwd=repository_root, text=True, env=environment, stderr=subprocess.STDOUT
    )
    node_ids = tuple(sorted(line.strip() for line in output.splitlines() if "::" in line))
    if not node_ids:
        raise RuntimeError("pytest collection produced no node IDs")
    payload = "\n".join(node_ids).encode("utf-8")
    return TestBaseline(
        command=command,
        pythonpath=environment["PYTHONPATH"],
        node_ids=node_ids,
        node_ids_sha256="sha256:" + hashlib.sha256(payload).hexdigest(),
    )


def _dependency_rows(repository_root: Path) -> tuple[ExternalDependency, ...]:
    """Capture only public dependency identities needed for offline release checks."""

    pyfcstm = repository_root / "pyfcstm"
    pyfcstm_commit = _git(repository_root, "-C", str(pyfcstm), "rev-parse", "HEAD")
    return (
        ExternalDependency(
            name="python",
            value=sys.version.split()[0],
            basis="running interpreter version",
        ),
        ExternalDependency(
            name="pyfcstm",
            value=pyfcstm_commit,
            basis="git submodule HEAD",
        ),
        ExternalDependency(
            name="pydantic",
            value=__import__("pydantic").__version__,
            basis="installed package version",
        ),
        ExternalDependency(
            name="httpx",
            value=__import__("httpx").__version__,
            basis="installed package version",
        ),
    )


def capture(repository_root: Path, paper_root: Path, python: Path) -> ReleaseRefactorBaseline:
    """Build the complete baseline object before any source relocation begins."""

    production_roots = (
        paper_root / "pipeline" / "evidence_discovery",
        paper_root / "pipeline" / "semantic_judge",
        repository_root / "utils",
    )
    frozen_archive = paper_root / "final_results" / "v60_current_vs_x1v2_baseline"
    return ReleaseRefactorBaseline(
        schema_id="paper1.release-refactor-baseline.v1",
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        repository_head=_git(repository_root, "rev-parse", "HEAD"),
        paper_root=paper_root.relative_to(repository_root).as_posix(),
        known_frozen_anchors=FROZEN_ANCHORS,
        test_baseline=_collect_nodes(repository_root, python, paper_root),
        production_files=_hash_files(repository_root, production_roots),
        frozen_archive_files=_hash_files(repository_root, (frozen_archive,)),
        external_dependencies=_dependency_rows(repository_root),
        reason="Preserves source, test, dependency, and frozen-result identities before a structure-only migration.",
        basis="Git, byte-level SHA-256, provider-free pytest collection, and installed dependency versions.",
    )


def _write_json(path: Path, value: BaseModel) -> None:
    """Atomically write stable JSON without changing any frozen experiment artifact."""

    payload = value.model_dump_json(indent=2, by_alias=True).encode("utf-8") + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    """Run the offline baseline capture command."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    manifest = capture(
        arguments.repository_root.resolve(),
        arguments.paper_root.resolve(),
        arguments.python,
    )
    _write_json(arguments.output.resolve(), manifest)
    print(arguments.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
