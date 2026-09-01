#!/usr/bin/env python3
"""Build the traceable current-v4 invalid-claim diagnostic cluster index.

This provider-free projection reuses only the historical pane5-confirmed I
membership. It does not create substantive defect groups, change a semantic
decision, or run method, Judge, or provider code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceReference(BaseModel):
    """Repository-relative source reference carried by one diagnostic cluster."""

    model_config = ConfigDict(extra="forbid")

    repository_path: str = Field(min_length=1, description="Repository-relative evidence path; not nullable and not a prompt field.")
    json_pointer: str | None = Field(default=None, description="RFC 6901 pointer into the evidence file; nullable and not a prompt field.")
    line: int | None = Field(default=None, ge=1, description="One-based source line when applicable; nullable and not a prompt field.")
    sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the evidence file; not nullable and not a prompt field.")


class InvalidDiagnosticCluster(BaseModel):
    """One same-pair cluster of invalid reports used only for diagnostic sensitivity."""

    model_config = ConfigDict(extra="forbid")

    cluster_id: str = Field(min_length=1, description="Stable current-v4 diagnostic cluster ID; not nullable and not a defect identity.")
    side: Literal["v60_current"] = Field(description="Evaluation side owning every member; fixed and not nullable.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Author/source pair owning every member; not nullable and not a prompt field.")
    member_report_ids: tuple[str, ...] = Field(min_length=1, description="Invalid report IDs assigned exactly once to this diagnostic cluster; not nullable.")
    diagnostic_key: str = Field(min_length=1, description="Historical pane5 diagnostic key retained for provenance; not nullable and not a defect identity.")
    reason: str = Field(min_length=1, description="Why the reports share a diagnostic invalid-claim pattern; not nullable and not a substantive-defect claim.")
    basis: str = Field(min_length=1, description="Source and historical membership evidence for this diagnostic projection; not nullable.")
    source_refs: tuple[SourceReference, ...] = Field(min_length=1, description="Resolvable source evidence for the cluster membership; not nullable.")
    substantive_defect: Literal[False] = Field(description="Structurally false because invalid diagnostic clusters are not defects.")
    grouped_precision_unit: Literal[False] = Field(description="Structurally false because this cluster cannot enter substantive grouped precision.")


class DiagnosticAssertions(BaseModel):
    """Machine-checkable boundaries for the current invalid-cluster projection."""

    model_config = ConfigDict(extra="forbid")

    every_current_i_report_exactly_once: Literal[True] = Field(description="Whether every current I report has exactly one diagnostic ID; structurally true.")
    no_cross_pair: Literal[True] = Field(description="Whether every cluster stays within one pair; structurally true.")
    no_cross_side: Literal[True] = Field(description="Whether every cluster stays on current; structurally true.")
    diagnostic_only: Literal[True] = Field(description="Whether all cluster IDs are diagnostic and not defect entities; structurally true.")
    excluded_from_grouped_precision: Literal[True] = Field(description="Whether the projection is excluded from substantive grouped precision; structurally true.")


class InvalidDiagnosticClusterDocument(BaseModel):
    """Versioned current-v4 diagnostic cluster document with complete membership."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    schema_version: Literal["paper1.current-reaudit.i-diagnostic-clusters.v4"] = Field(alias="schema", description="Versioned schema identifier serialized as schema; fixed and not nullable.")
    side: Literal["v60_current"] = Field(description="Evaluation side covered by the document; fixed and not nullable.")
    source_group_decisions_path: str = Field(min_length=1, description="Repository-relative historical membership source; not nullable.")
    source_group_decisions_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the historical membership source; not nullable.")
    report_count: int = Field(ge=0, description="Number of current invalid reports covered; not nullable.")
    diagnostic_cluster_count: int = Field(ge=0, description="Number of invalid-claim diagnostic clusters; not nullable and not a defect count.")
    clusters: tuple[InvalidDiagnosticCluster, ...] = Field(description="Complete diagnostic cluster records; not nullable.")
    report_to_cluster: dict[str, str] = Field(description="One-to-one invalid report to diagnostic cluster map; not nullable.")
    assertions: DiagnosticAssertions = Field(description="Machine-checkable non-substantive grouping boundaries; not nullable.")


def load(path: Path) -> Any:
    """Load one UTF-8 JSON document."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Return an archive-style SHA-256 digest."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def dump(path: Path, value: BaseModel | dict[str, Any]) -> None:
    """Write deterministic JSON for a validated model or manifest object."""

    payload = value.model_dump(mode="json", by_alias=True) if isinstance(value, BaseModel) else value
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build(archive: Path) -> Path:
    """Create and validate the diagnostic index without touching decisions."""

    current_root = archive / "derived/manual_adjudication_v4_current_reaudit"
    source_path = archive / "derived/manual_adjudication_v2/group_decisions.json"
    decisions_path = current_root / "current_report_decisions_v4.json"
    output_path = current_root / "current_i_diagnostic_clusters_v4.json"

    decisions = load(decisions_path)["decisions"]
    current_i = {
        str(row["original_report_id"]): str(row["pair_id"])
        for row in decisions
        if row["canonical_class"] == "I"
    }
    source_groups = [
        row
        for row in load(source_path)["groups"]
        if row.get("side") == "v60_current" and row.get("group_verdict") == "I"
    ]
    clusters: list[InvalidDiagnosticCluster] = []
    mapping: dict[str, str] = {}
    for row in sorted(source_groups, key=lambda item: (str(item["pair_id"]), str(item["canonical_group_key"]))):
        pair_id = str(row["pair_id"])
        members = tuple(sorted(str(report_id) for report_id in row["report_ids"]))
        if any(report_id not in current_i or current_i[report_id] != pair_id for report_id in members):
            raise ValueError(f"diagnostic cluster crosses the current I/pair boundary: {row['canonical_group_key']}")
        cluster_id = "current-i-diagnostic::" + str(row["canonical_group_key"])
        for report_id in members:
            if report_id in mapping:
                raise ValueError(f"current I report appears in two diagnostic clusters: {report_id}")
            mapping[report_id] = cluster_id
        clusters.append(InvalidDiagnosticCluster(
            cluster_id=cluster_id,
            side="v60_current",
            pair_id=pair_id,
            member_report_ids=members,
            diagnostic_key=str(row["canonical_group_key"]),
            reason=(
                "These invalid reports retain one historical same-pair invalid-claim diagnostic key; "
                "the shared ID describes repeated attribution/interpretation symptoms and does not assert a defect."
            ),
            basis=str(row["basis"]),
            source_refs=tuple(SourceReference.model_validate(ref) for ref in row["source_refs"]),
            substantive_defect=False,
            grouped_precision_unit=False,
        ))
    if set(mapping) != set(current_i):
        missing = sorted(set(current_i) - set(mapping))
        extra = sorted(set(mapping) - set(current_i))
        raise ValueError(f"current I diagnostic membership is not closed: missing={missing[:5]}, extra={extra[:5]}")
    document = InvalidDiagnosticClusterDocument(
        schema_version="paper1.current-reaudit.i-diagnostic-clusters.v4",
        side="v60_current",
        source_group_decisions_path="derived/manual_adjudication_v2/group_decisions.json",
        source_group_decisions_sha256=sha256(source_path),
        report_count=len(current_i),
        diagnostic_cluster_count=len(clusters),
        clusters=tuple(clusters),
        report_to_cluster=mapping,
        assertions=DiagnosticAssertions(
            every_current_i_report_exactly_once=True,
            no_cross_pair=True,
            no_cross_side=True,
            diagnostic_only=True,
            excluded_from_grouped_precision=True,
        ),
    )
    dump(output_path, document)

    manifest_path = current_root / "manifest_v4.json"
    manifest = load(manifest_path)
    manifest.setdefault("outputs", {})[output_path.name] = sha256(output_path)
    dump(manifest_path, manifest)
    print(json.dumps({
        "status": "PASS",
        "current_i_reports": document.report_count,
        "diagnostic_clusters": document.diagnostic_cluster_count,
        "output": str(output_path),
    }, sort_keys=True))
    return output_path


def validate(archive: Path) -> None:
    """Validate a saved index against current decisions and its source hash."""

    current_root = archive / "derived/manual_adjudication_v4_current_reaudit"
    output_path = current_root / "current_i_diagnostic_clusters_v4.json"
    document = InvalidDiagnosticClusterDocument.model_validate(load(output_path))
    source_path = archive / document.source_group_decisions_path
    if sha256(source_path) != document.source_group_decisions_sha256:
        raise ValueError("current I diagnostic source hash changed")
    current_i = {
        str(row["original_report_id"])
        for row in load(current_root / "current_report_decisions_v4.json")["decisions"]
        if row["canonical_class"] == "I"
    }
    members = [report_id for cluster in document.clusters for report_id in cluster.member_report_ids]
    if set(members) != current_i or len(members) != len(set(members)) or document.report_to_cluster.keys() != current_i:
        raise ValueError("current I diagnostic index does not cover each invalid report exactly once")
    if document.report_count != len(current_i) or document.diagnostic_cluster_count != len(document.clusters):
        raise ValueError("current I diagnostic counts are stale")
    manifest = load(current_root / "manifest_v4.json")
    if manifest.get("outputs", {}).get(output_path.name) != sha256(output_path):
        raise ValueError("current I diagnostic output is absent or stale in manifest_v4.json")
    print(json.dumps({"status": "PASS", "current_i_reports": len(current_i), "diagnostic_clusters": len(document.clusters)}, sort_keys=True))


def main() -> None:
    """Build or validate the current invalid diagnostic index."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    if args.validate_only:
        validate(archive)
    else:
        build(archive)


if __name__ == "__main__":
    main()
