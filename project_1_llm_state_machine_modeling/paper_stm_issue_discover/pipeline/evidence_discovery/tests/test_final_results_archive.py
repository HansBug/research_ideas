from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.evidence_discovery.reporting.final_results_archive import (
    ARCHIVE_SCHEMA,
    PROVENANCE_SCHEMA,
    SUMMARY_SCHEMA,
    _validate_archive_metadata,
    _validate_markdown_links,
)


def _write_json(path: Path, value: object) -> None:
    """Write a minimal UTF-8 JSON fixture for archive metadata validation."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _metadata_fixture(tmp_path: Path) -> Path:
    """Create the smallest archive with valid schema declarations and mappings."""

    archive = tmp_path / "archive"
    for relative in (
        "archive_manifest.json",
        "raw/v60_current/archive_manifest.json",
        "raw/x1v2_baseline/archive_manifest.json",
    ):
        _write_json(archive / relative, {"schema": ARCHIVE_SCHEMA, "included_files": []})
    _write_json(archive / "derived/recomputed_summary.json", {"schema": SUMMARY_SCHEMA})
    (archive / "raw/v60_current/method").mkdir(parents=True)
    _write_json(
        archive / "provenance_path_mapping.json",
        {
            "schema": PROVENANCE_SCHEMA,
            "mappings": [{"archive_relative_path": "raw/v60_current/method"}],
        },
    )
    return archive


def test_archive_metadata_accepts_declared_schemas_and_existing_relative_mapping(tmp_path: Path) -> None:
    """Archive metadata is accepted only when schemas and provenance target are explicit."""

    _validate_archive_metadata(_metadata_fixture(tmp_path))


def test_archive_metadata_rejects_wrong_summary_schema(tmp_path: Path) -> None:
    """A stale or unsupported derived summary schema cannot pass final validation."""

    archive = _metadata_fixture(tmp_path)
    _write_json(archive / "derived/recomputed_summary.json", {"schema": "wrong-schema"})

    with pytest.raises(ValueError, match="unexpected summary schema"):
        _validate_archive_metadata(archive)


def test_archive_metadata_rejects_missing_or_escaping_provenance_target(tmp_path: Path) -> None:
    """Provenance maps must remain inside the archive and point to a real artifact."""

    archive = _metadata_fixture(tmp_path)
    _write_json(
        archive / "provenance_path_mapping.json",
        {"schema": PROVENANCE_SCHEMA, "mappings": [{"archive_relative_path": "../outside"}]},
    )

    with pytest.raises(ValueError, match="escapes its allowed root"):
        _validate_archive_metadata(archive)


def test_markdown_links_must_resolve_without_using_transient_runs(tmp_path: Path) -> None:
    """Final docs may use archive or repository paths but never the runs workspace."""

    repository = tmp_path / "repository"
    archive = repository / "final_results"
    archive.mkdir(parents=True)
    (archive / "target.json").write_text("{}", encoding="utf-8")
    (archive / "README.md").write_text("[ok](target.json)\n[located](target.json:7)\n", encoding="utf-8")

    _validate_markdown_links(archive, repository_root=repository)

    (archive / "README.md").write_text("[transient](../runs/result.json)\n", encoding="utf-8")
    with pytest.raises(ValueError, match="transient runs data"):
        _validate_markdown_links(archive, repository_root=repository)


def test_markdown_links_reject_missing_or_escaping_paths(tmp_path: Path) -> None:
    """Broken and out-of-repository local links are final-publication errors."""

    repository = tmp_path / "repository"
    archive = repository / "final_results"
    archive.mkdir(parents=True)
    readme = archive / "README.md"
    readme.write_text("[missing](missing.json)\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Markdown link is missing"):
        _validate_markdown_links(archive, repository_root=repository)

    readme.write_text("[escape](../../outside.json)\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Markdown link escapes repository"):
        _validate_markdown_links(archive, repository_root=repository)
