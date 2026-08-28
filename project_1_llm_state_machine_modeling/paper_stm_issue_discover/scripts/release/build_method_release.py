"""Build a deterministic, allowlisted method release without rewriting source.

Input: a clean repository checkout and ``method/release_allowlist.json``.
Output: a new release directory containing only allowlisted method and neutral
utility files plus a generated per-file SHA-256 manifest. This command never
calls a provider and never writes into the source checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReleaseEntry(BaseModel):
    """One immutable source-to-destination rule in the release allowlist."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    source: str = Field(min_length=1, description="Repository-relative source file or directory allowed into the release.")
    destination: str = Field(min_length=1, description="Release-relative destination path for the exact source bytes.")
    purpose: str = Field(min_length=1, description="Auditable reason this entry is needed by the standalone method release.")
    recursive: bool = Field(default=False, description="Whether the source is a directory copied recursively under suffix restrictions.")
    allowed_suffixes: tuple[str, ...] = Field(default_factory=tuple, description="Allowed file suffixes for a recursive source, or empty for one exact file.")


class ReleaseAllowlist(BaseModel):
    """Validated machine-readable policy for the minimal method release tree."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["paper1.method-release-allowlist.v1"] = Field(description="Versioned release allowlist schema identifier.")
    package_name: str = Field(min_length=1, description="Published distribution name represented by this allowlist.")
    source_commit_requirement: str = Field(min_length=1, description="Required source-tree provenance condition before a release build.")
    entries: tuple[ReleaseEntry, ...] = Field(min_length=1, description="Complete, ordered set of permitted source copy rules.")
    excluded_categories: tuple[str, ...] = Field(min_length=1, description="Classes of data intentionally excluded from the method release.")


class ReleaseFile(BaseModel):
    """Hash and provenance of one byte-identical released file."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    source: str = Field(min_length=1, description="Repository-relative allowlisted source path.")
    destination: str = Field(min_length=1, description="Release-relative copied path.")
    sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the copied bytes, equal to the source bytes.")
    byte_count: int = Field(ge=0, description="Exact byte count of the copied file.")
    purpose: str = Field(min_length=1, description="Allowlist purpose inherited from the source entry.")


class ReleaseManifest(BaseModel):
    """Deterministic generated manifest for one method release build."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["paper1.method-release-manifest.v1"] = Field(description="Versioned generated release manifest schema identifier.")
    source_commit: str = Field(pattern=r"^[0-9a-f]{40}$", description="Clean Git commit supplying every copied release byte.")
    allowlist_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the exact allowlist JSON bytes.")
    files: tuple[ReleaseFile, ...] = Field(min_length=1, description="Sorted exhaustive list of files copied into the release tree.")
    file_count: int = Field(ge=1, description="Number of released payload files excluding this generated manifest.")
    total_bytes: int = Field(ge=0, description="Total size of released payload files excluding this generated manifest.")
    provider_call_count: Literal[0] = Field(description="Provider calls made while building the release; always zero.")
    billable_call_count: Literal[0] = Field(description="Billable provider calls made while building the release; always zero.")
    reason: str = Field(min_length=1, description="Statement of the build's byte-copy-only boundary.")
    basis: str = Field(min_length=1, description="Allowlist, clean Git commit, and per-file SHA-256 provenance basis.")


def _sha256(path: Path) -> str:
    """Return the SHA-256 identity of one file without interpreting its content."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _repository_root() -> Path:
    """Resolve the Git root rather than assuming a caller working directory."""

    return Path(
        subprocess.check_output(
            ("git", "rev-parse", "--show-toplevel"), text=True
        ).strip()
    )


def _clean_commit(root: Path) -> str:
    """Require a clean tracked checkout so a release maps to one immutable commit."""

    status = subprocess.check_output(
        ("git", "status", "--porcelain", "--untracked-files=no"),
        cwd=root,
        text=True,
    )
    if status.strip():
        raise RuntimeError("build-method-release requires a clean tracked Git tree")
    return subprocess.check_output(("git", "rev-parse", "HEAD"), cwd=root, text=True).strip()


def _safe_relative(value: str) -> Path:
    """Validate a release-relative path cannot escape the release tree."""

    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"release path must be a safe relative path: {value}")
    return path


def _entry_files(root: Path, entry: ReleaseEntry) -> tuple[tuple[Path, Path], ...]:
    """Expand one allowlist entry into deterministic source/destination files."""

    source_relative = _safe_relative(entry.source)
    destination_relative = _safe_relative(entry.destination)
    source = root / source_relative
    if entry.recursive:
        if not source.is_dir() or not entry.allowed_suffixes:
            raise ValueError(f"recursive allowlist entry is invalid: {entry.source}")
        files = tuple(
            path
            for path in sorted(source.rglob("*"))
            if path.is_file() and path.suffix in entry.allowed_suffixes
        )
        if not files:
            raise ValueError(f"recursive allowlist entry matched no files: {entry.source}")
        return tuple(
            (path, destination_relative / path.relative_to(source)) for path in files
        )
    if not source.is_file():
        raise FileNotFoundError(source)
    return ((source, destination_relative),)


def _reject_leaks(repository: Path, files: tuple[ReleaseFile, ...]) -> None:
    """Reject released paths that would disclose evaluation or machine-local data."""

    forbidden_path_parts = {
        "judge", "evaluation", "baseline", "final_results", "runs", "archive", "legacy",
    }
    secret_pattern = re.compile(
        rb"(?:sk-[A-Za-z0-9_-]{20,}|authorization:\s*bearer\s+[A-Za-z0-9._-]{20,})",
        re.IGNORECASE,
    )
    violations: list[str] = []
    for item in files:
        destination = Path(item.destination)
        if forbidden_path_parts.intersection(destination.parts):
            violations.append(f"forbidden release path: {item.destination}")
        content = (repository / item.source).read_bytes()
        if secret_pattern.search(content):
            violations.append(f"probable credential in release content: {item.destination}")
    if violations:
        raise RuntimeError("method release leakage check failed: " + "; ".join(violations))


def build(*, output: Path, root: Path | None = None) -> ReleaseManifest:
    """Copy exactly allowlisted bytes into an empty output directory and manifest them."""

    repository = root or _repository_root()
    commit = _clean_commit(repository)
    allowlist_path = repository / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/release_allowlist.json"
    allowlist_bytes = allowlist_path.read_bytes()
    allowlist = ReleaseAllowlist.model_validate_json(allowlist_bytes)
    output = output.expanduser().resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"release output must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    files: list[ReleaseFile] = []
    destinations: set[Path] = set()
    for entry in allowlist.entries:
        for source, destination in _entry_files(repository, entry):
            if destination in destinations:
                raise ValueError(f"duplicate release destination: {destination}")
            destinations.add(destination)
            target = output / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            source_hash = _sha256(source)
            if _sha256(target) != source_hash:
                raise RuntimeError(f"byte mismatch after copy: {source}")
            files.append(
                ReleaseFile(
                    source=source.relative_to(repository).as_posix(),
                    destination=destination.as_posix(),
                    sha256=source_hash,
                    byte_count=source.stat().st_size,
                    purpose=entry.purpose,
                )
            )
    ordered = tuple(sorted(files, key=lambda item: item.destination))
    _reject_leaks(repository, ordered)
    manifest = ReleaseManifest(
        source_commit=commit,
        allowlist_sha256="sha256:" + hashlib.sha256(allowlist_bytes).hexdigest(),
        files=ordered,
        file_count=len(ordered),
        total_bytes=sum(item.byte_count for item in ordered),
        provider_call_count=0,
        billable_call_count=0,
        reason="The release was created by byte-for-byte allowlisted copies only; no source rewrite or provider call occurred.",
        basis="Clean Git commit, release_allowlist.json, and SHA-256 for every copied file.",
    )
    manifest_path = output / "release_manifest.json"
    manifest_path.write_bytes(
        manifest.model_dump_json(indent=2).encode("utf-8") + b"\n"
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    """Run the provider-free deterministic method-release builder."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build(output=args.output)
    print(manifest.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
