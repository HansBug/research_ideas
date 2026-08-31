#!/usr/bin/env python3
"""Generate the Track C provenance-only positive-control precursor audit.

This utility intentionally does not select predicates, construct queries, or
execute any property.  It establishes only that each current ledger item has a
hash-bound defective author artifact and a separately located, still
unvalidated reference-model candidate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Literal

from openpyxl import load_workbook
from pydantic import BaseModel, ConfigDict, Field, model_validator


SCHEMA_VERSION = "paper1.predicate-gold.track-c-artifact-positive-control-audit.v1"
CANDIDATE_INDEX_SCHEMA_VERSION = "paper1.predicate-gold.positive-control-candidates.v1"
REVIEWER_ID = "pane5:track-c-artifact-positive-control-audit"
SHA256_PATTERN = r"^sha256:[0-9a-f]{64}$"
UNVERIFIED_STATUS = "UNVERIFIED_CANDIDATE_REFERENCE"


class StrictModel(BaseModel):
    """Immutable audit record base that rejects undocumented fields."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class InputHash(StrictModel):
    """One hash-bound input read by the provenance-only audit."""

    role: str = Field(description="Semantic role of this immutable audit input.", min_length=1)
    repository_path: str = Field(description="Repository-relative path of the input file.", min_length=1)
    sha256: str = Field(description="SHA-256 of the complete input file bytes.", pattern=SHA256_PATTERN)


class SourceRef(StrictModel):
    """Stable location used to support a provenance or control-boundary claim."""

    role: str = Field(description="Evidence role, such as ledger, author source, metadata, or reference candidate.", min_length=1)
    repository_path: str = Field(description="Repository-relative evidence path.", min_length=1)
    sha256: str = Field(description="SHA-256 of the cited file bytes.", pattern=SHA256_PATTERN)
    json_pointer: str | None = Field(description="RFC 6901 pointer for JSON evidence, or null when not JSON-addressable.")
    line_number: int | None = Field(description="One-based line number for line-addressable evidence, or null otherwise.", ge=1)
    locator: str | None = Field(description="Workbook sheet/cell or other stable non-line locator, or null when not needed.")
    note: str = Field(description="Narrow explanation of what the cited location establishes.", min_length=1)


class ArtifactRef(StrictModel):
    """One author, derived, or reference artifact with exact byte identity."""

    role: str = Field(description="Artifact role; author source, derived execution input, or reference candidate.", min_length=1)
    repository_path: str | None = Field(description="Repository-relative materialized artifact path, or null when retained only in a workbook cell.")
    sha256: str = Field(description="SHA-256 of the artifact bytes or UTF-8 cell text.", pattern=SHA256_PATTERN)
    locator: str | None = Field(description="Stable workbook cell locator, or null for a materialized file.")
    author_source_authority: bool = Field(description="Whether this artifact may establish an author-source fact.")
    execution_eligibility: str = Field(description="Declared execution eligibility, not an inferred predicate result.", min_length=1)
    note: str = Field(description="Artifact-boundary explanation.", min_length=1)


class RepairedArtifactCheck(StrictModel):
    """Explicit absence record for an approved issue-specific repaired artifact."""

    exists: Literal[False] = Field(description="False because no approved issue-specific repaired artifact mapping is present in the checked ledger-gold scope.")
    checked_scope: tuple[str, ...] = Field(description="Repository scopes inspected for a canonical issue-specific control mapping.", min_length=1)
    checked_attribution_fields: tuple[str, ...] = Field(description="Canonical ledger and metadata fields checked for a repaired-control reference.", min_length=1)
    reason: str = Field(description="Why absence of a canonical mapping prevents an implicit repaired control.", min_length=1)


class ControlPrerequisite(StrictModel):
    """One concrete prerequisite before a candidate can become a true-side control."""

    prerequisite_id: Literal[
        "MATERIALIZE_REFERENCE_ARTIFACT",
        "SEMANTIC_EQUIVALENCE_REVIEW",
        "ATTRIBUTION_CLOSURE",
        "PRECOMMIT_PROPERTY_AND_INPUTS",
        "COMPLETED_TRUE_RECEIPT",
        "VACUITY_AND_CONTAMINATION_CHECK",
    ] = Field(description="Stable prerequisite category for promotion to an approved positive control.")
    status: Literal["MISSING"] = Field(description="This precursor records each promotion prerequisite as missing rather than assuming it holds.")
    required_evidence: str = Field(description="Specific evidence that must be added before this prerequisite can be closed.", min_length=1)
    reason: str = Field(description="Why this missing prerequisite matters for the candidate's truth-side evidentiary role.", min_length=1)


class AuditCheck(StrictModel):
    """One PASS/FAIL result with a bounded interpretation."""

    check_id: str = Field(description="Stable audit check identifier.", min_length=1)
    status: Literal["PASS", "FAIL"] = Field(description="PASS or FAIL for the stated check only; it is never a predicate or gold verdict.")
    reason: str = Field(description="Evidence-specific interpretation of this check outcome.", min_length=1)


class PositiveControlCandidateRecord(StrictModel):
    """Per-ledger reference candidate that remains unapproved until later Track C work."""

    ledger_id: str = Field(description="Current immutable ledger ID covered exactly once.", min_length=1)
    pair_id: str = Field(description="Four-digit source pair owning this ledger item.", pattern=r"^[0-9]{4}$")
    ledger_family: str = Field(description="Immutable ledger ID family prefix.", min_length=1)
    ledger_d_tier: Literal["D1", "D2"] = Field(description="Frozen ledger D tier; it is not re-adjudicated by this audit.")
    ledger_l_tier: Literal["L0", "L1", "L2"] = Field(description="Frozen ledger L tier; it is not re-adjudicated by this audit.")
    bad_author_plantuml: ArtifactRef = Field(description="Hash-bound defective author PlantUML source artifact.")
    bad_derived_fcstm: ArtifactRef = Field(description="Hash-bound derived FCSTM execution artifact with its declared limitations.")
    reference_candidate: ArtifactRef = Field(description="Workbook-backed reference PlantUML candidate; it is not an approved control.")
    candidate_status: Literal["UNVERIFIED_CANDIDATE_REFERENCE"] = Field(description="Mandatory unverified status; this record makes no true-control or predicate claim.")
    positive_control_approved: Literal[False] = Field(description="False until a later independent review closes every listed prerequisite.")
    cannot_default_to_true_reason: tuple[str, ...] = Field(description="Specific reasons a reference artifact cannot be treated as a completed true control.", min_length=1)
    issue_specific_repaired_artifact: RepairedArtifactCheck = Field(description="Explicit nonexistence record for a canonical repaired artifact mapped to this ledger ID.")
    remaining_prerequisites: tuple[ControlPrerequisite, ...] = Field(description="Required materialization, semantic, attribution, query, receipt, and vacuity work before approval.", min_length=1)
    provenance_check: AuditCheck = Field(description="PASS/FAIL for source/reference locator and hash closure.")
    control_approval_check: AuditCheck = Field(description="Expected FAIL until an independently executed true-side control exists.")
    source_refs: tuple[SourceRef, ...] = Field(description="Ledger, author artifact, metadata, workbook, and closure anchors actually read by Track C.", min_length=6)


class AuditCoverage(StrictModel):
    """Mechanically derived ledger coverage and unresolved-control totals."""

    ledger_item_count: int = Field(description="Number of current ledger IDs read by the audit.", ge=0)
    record_count: int = Field(description="Number of generated per-ledger audit records.", ge=0)
    unique_ledger_id_count: int = Field(description="Distinct generated ledger IDs.", ge=0)
    pair_count: int = Field(description="Distinct source pairs represented by the records.", ge=0)
    provenance_pass_count: int = Field(description="Records whose author/reference locator and hashes close.", ge=0)
    provenance_fail_count: int = Field(description="Records with a source/reference provenance failure.", ge=0)
    unverified_candidate_count: int = Field(description="Records deliberately retained as unverified reference candidates.", ge=0)
    approved_positive_control_count: Literal[0] = Field(description="Always zero in this precursor; no completed true control is asserted.")
    issue_specific_repaired_artifact_count: Literal[0] = Field(description="Always zero because no approved issue-specific repaired artifact mapping was found.")

    @model_validator(mode="after")
    def validate_counts(self) -> "AuditCoverage":
        """Keep coverage totals internally consistent."""

        if self.record_count != self.unique_ledger_id_count:
            raise ValueError("record_count must equal unique_ledger_id_count")
        if self.provenance_pass_count + self.provenance_fail_count != self.record_count:
            raise ValueError("provenance totals must equal record_count")
        if self.unverified_candidate_count != self.record_count:
            raise ValueError("every precursor record must remain unverified")
        return self


class TrackCArtifactPositiveControlAudit(StrictModel):
    """Complete provenance-only Track C audit covering every current ledger item."""

    schema_version: Literal[SCHEMA_VERSION] = Field(default=SCHEMA_VERSION, description="Versioned schema identifier for this precursor audit.")
    reviewer_id: Literal[REVIEWER_ID] = Field(default=REVIEWER_ID, description="Internal Track C reviewer identity; it is not an inter-rater study label.")
    reviewed_at: str = Field(description="UTC timestamp at which this immutable audit was generated.", min_length=1)
    source_commit: str = Field(description="Repository commit read by this audit.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="pyfcstm commit available when backend/control capability boundaries were reviewed.", pattern=r"^[0-9a-f]{40}$")
    input_hashes: tuple[InputHash, ...] = Field(description="Top-level frozen files read by the audit.", min_length=4)
    commands: tuple[str, ...] = Field(description="Actual provider-free commands used to generate and validate this audit.", min_length=1)
    execution_boundary: str = Field(description="Explicit statement that no predicate, method, Judge, provider, or v60 actual-output read occurred.", min_length=1)
    generic_fixture_exclusion: str = Field(description="Why generic pyfcstm fixtures are not ledger-specific positive controls.", min_length=1)
    checks: tuple[AuditCheck, ...] = Field(description="Top-level PASS/FAIL checks with no predicate semantics.", min_length=2)
    coverage: AuditCoverage = Field(description="Mechanically derived complete coverage and unverified-control counts.")
    records: tuple[PositiveControlCandidateRecord, ...] = Field(description="Exactly one explicit unverified candidate record for every ledger ID.", min_length=1)
    audit_sha256: str = Field(description="Canonical SHA-256 of this audit excluding audit_sha256.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_records(self) -> "TrackCArtifactPositiveControlAudit":
        """Require an exact once-only record set and no accidental approval."""

        ids = [record.ledger_id for record in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError("ledger IDs must be unique")
        if len(ids) != self.coverage.ledger_item_count:
            raise ValueError("record count must equal ledger coverage")
        if any(record.positive_control_approved for record in self.records):
            raise ValueError("precursor audit may not approve a positive control")
        return self


class CandidateIndexEntry(StrictModel):
    """Compact per-ledger index entry for later positive-control review batches."""

    ledger_id: str = Field(description="Current immutable ledger ID.", min_length=1)
    pair_id: str = Field(description="Four-digit source pair owning the candidate.", pattern=r"^[0-9]{4}$")
    candidate_status: Literal["UNVERIFIED_CANDIDATE_REFERENCE"] = Field(description="Candidate remains unverified and cannot count as a true control.")
    reference_locator: str = Field(description="Stable workbook sheet/cell locator for the candidate reference PlantUML.", min_length=1)
    reference_plantuml_sha256: str = Field(description="SHA-256 of the candidate reference PlantUML UTF-8 text.", pattern=SHA256_PATTERN)
    bad_author_plantuml_sha256: str = Field(description="SHA-256 of the defective author PlantUML source.", pattern=SHA256_PATTERN)
    bad_fcstm_sha256: str = Field(description="SHA-256 of the derived FCSTM artifact used only for future native binding.", pattern=SHA256_PATTERN)
    issue_specific_repaired_artifact_exists: Literal[False] = Field(description="No approved repaired artifact is mapped to this ledger issue.")
    approval_prerequisite_ids: tuple[str, ...] = Field(description="Stable prerequisite IDs that must all close before a true-control assertion.", min_length=1)
    audit_record_pointer: str = Field(description="RFC 6901 pointer to the full record in the Track C audit.", min_length=1)


class PositiveControlCandidateIndex(StrictModel):
    """Complete candidate index that deliberately exposes no property verdict or true receipt."""

    schema_version: Literal[CANDIDATE_INDEX_SCHEMA_VERSION] = Field(default=CANDIDATE_INDEX_SCHEMA_VERSION, description="Versioned schema identifier for the candidate index.")
    reviewer_id: Literal[REVIEWER_ID] = Field(default=REVIEWER_ID, description="Internal Track C reviewer identity producing this index.")
    generated_at: str = Field(description="UTC timestamp inherited from the provenance audit.", min_length=1)
    audit_path: str = Field(description="Gold-root-relative path of the full provenance audit.", min_length=1)
    audit_file_sha256: str = Field(description="SHA-256 of the persisted full audit file.", pattern=SHA256_PATTERN)
    no_positive_control_claim: Literal[True] = Field(description="Confirms that this index contains candidates only, never approved true controls.")
    entries: tuple[CandidateIndexEntry, ...] = Field(description="Exactly one unverified candidate entry for each current ledger ID.", min_length=1)
    index_sha256: str = Field(description="Canonical SHA-256 of this index excluding index_sha256.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_entries(self) -> "PositiveControlCandidateIndex":
        """Reject duplicates and any non-candidate status in the compact index."""

        ids = [entry.ledger_id for entry in self.entries]
        if len(ids) != len(set(ids)):
            raise ValueError("candidate index ledger IDs must be unique")
        return self


def sha256_path(path: Path) -> str:
    """Return a prefixed SHA-256 for complete file bytes."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(value: str) -> str:
    """Return a prefixed SHA-256 for exact UTF-8 text."""

    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    """Hash a canonical JSON value without relying on insertion order."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def repo_relative(repo_root: Path, path: Path) -> str:
    """Return a normalized repository-relative path for persisted evidence."""

    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def git_commit(path: Path) -> str:
    """Read a local git commit without changing repository state."""

    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def write_json(path: Path, value: StrictModel) -> None:
    """Persist one validated canonical JSON document with a trailing newline."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reference_prerequisites() -> tuple[ControlPrerequisite, ...]:
    """Return the uniform promotion requirements for every unverified candidate."""

    return (
        ControlPrerequisite(
            prerequisite_id="MATERIALIZE_REFERENCE_ARTIFACT",
            status="MISSING",
            required_evidence="Extract the cited workbook cell into a versioned per-pair PlantUML file and record its byte hash and extraction command.",
            reason="A cell locator and text hash locate the candidate but do not create a replayable control artifact.",
        ),
        ControlPrerequisite(
            prerequisite_id="SEMANTIC_EQUIVALENCE_REVIEW",
            status="MISSING",
            required_evidence="Independently show that the materialized reference satisfies this ledger issue's normalized obligation without narrowing quantifier, scope, timing, or assumptions.",
            reason="A reference-model label is not an issue-specific proof that the same obligation holds.",
        ),
        ControlPrerequisite(
            prerequisite_id="ATTRIBUTION_CLOSURE",
            status="MISSING",
            required_evidence="Bind workbook source cell, materialized PlantUML, any derived native artifact, and their hashes while documenting conversion exclusions.",
            reason="The available FCSTM is a conversion artifact with simulation ineligibility, so a true result cannot be attributed to author source by default.",
        ),
        ControlPrerequisite(
            prerequisite_id="PRECOMMIT_PROPERTY_AND_INPUTS",
            status="MISSING",
            required_evidence="Freeze an obligation-equivalent property, typed inputs, domains, bounds, and proposal hash before observing either artifact's result.",
            reason="Selecting an input after seeing a desired true result would invalidate the positive-control evidence.",
        ),
        ControlPrerequisite(
            prerequisite_id="COMPLETED_TRUE_RECEIPT",
            status="MISSING",
            required_evidence="Run the frozen query provider-free on the verified control artifact and retain a completed Boolean true receipt, trace/counterexample boundary, and replay result.",
            reason="No existing candidate record contains a completed true execution receipt.",
        ),
        ControlPrerequisite(
            prerequisite_id="VACUITY_AND_CONTAMINATION_CHECK",
            status="MISSING",
            required_evidence="Record an antecedent/domain/reachability vacuity check and show that the control was not selected or edited from the defective-result outcome.",
            reason="A true result without these checks can be vacuous or contaminated rather than discriminative.",
        ),
    )


def no_repaired_artifact_check(gold_root: Path) -> RepairedArtifactCheck:
    """Record absence of a canonical per-issue repaired-control mapping in scope."""

    control_catalog = gold_root / "positive_controls"
    repair_catalog = gold_root / "repaired_artifacts"
    if control_catalog.exists() or repair_catalog.exists():
        raise ValueError("a control catalog now exists; Track C must inspect it before asserting absence")
    return RepairedArtifactCheck(
        exists=False,
        checked_scope=(
            "discover_matrix/ledger_v2/ledger.json#/items/*",
            "discover_matrix/ledger_v2/predicate_gold_v1/positive_controls/",
            "discover_matrix/ledger_v2/predicate_gold_v1/repaired_artifacts/",
        ),
        checked_attribution_fields=(
            "ledger item fields (no repaired/control artifact field)",
            "source_meta.json source lineage fields",
            "fcstm_meta.json conversion and publication-seal fields",
        ),
        reason="No approved issue-specific repaired artifact catalog or per-ledger mapping exists in the current ledger-gold scope; generic examples and workbook reference cells cannot fill this role implicitly.",
    )


def build_audit(
    *,
    repo_root: Path,
    paper_root: Path,
    output_root: Path,
    reviewed_at: str,
    command: str,
) -> TrackCArtifactPositiveControlAudit:
    """Build a 145-row provenance audit without loading any actual predicate result."""

    ledger_path = paper_root / "discover_matrix" / "ledger_v2" / "ledger.json"
    gold_root = ledger_path.parent / "predicate_gold_v1"
    pairs_path = paper_root / "corpora" / "seed_library" / "llms-emp-stm-subset" / "assets" / "extracted" / "pairs.jsonl"
    workbook_path = paper_root / "corpora" / "seed_library" / "llms-emp-stm-subset" / "assets" / "raw" / "drive_download" / "Experiment Results.xlsx"
    closure_path = paper_root / "final_results" / "v60_current_vs_x1v2_baseline" / "reference" / "x1v2_input_closure" / "manifest.json"
    seed_registry_path = paper_root / "corpora" / "seed_library" / "llms-emp-stm-subset" / "seed_resource_registry.json"
    fixture_path = repo_root / "pyfcstm" / "docs" / "source" / "tutorials" / "bmc" / "first_check_fixed.fcstm"

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    closure = json.loads(closure_path.read_text(encoding="utf-8"))
    pair_rows: dict[str, tuple[int, dict[str, Any]]] = {}
    for line_number, line in enumerate(pairs_path.read_text(encoding="utf-8").splitlines(), start=1):
        row = json.loads(line)
        pair_rows[row["pair_id"].rsplit("_", 1)[-1]] = (line_number, row)

    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    worksheet = workbook["STM Results"]
    repair_check = no_repaired_artifact_check(gold_root)
    prerequisites = reference_prerequisites()
    records: list[PositiveControlCandidateRecord] = []
    provenance_failures: list[str] = []

    for ledger_id, item in sorted(ledger["items"].items()):
        pair_id = str(item["pair"]).zfill(4)
        pair_line, pair_row = pair_rows[pair_id]
        source_dir = paper_root / "selected_seed_examples" / f"llms_emp_feedback_final_{pair_id}"
        plantuml_path = (ledger_path.parent / item["pair_context"]["stm0_file"]).resolve()
        nl_path = (ledger_path.parent / item["pair_context"]["nl_file"]).resolve()
        fcstm_path = source_dir / "model.fcstm"
        source_meta_path = source_dir / "source_meta.json"
        fcstm_meta_path = source_dir / "fcstm_meta.json"
        source_meta = json.loads(source_meta_path.read_text(encoding="utf-8"))
        fcstm_meta = json.loads(fcstm_meta_path.read_text(encoding="utf-8"))
        reference_cell = source_meta["source_cells"]["reference_plantuml"]
        reference_text = worksheet[reference_cell].value
        if reference_text is None or not str(reference_text).strip():
            raise ValueError(f"{ledger_id}: reference PlantUML cell {reference_cell} is blank")
        reference_hash = sha256_text(str(reference_text))
        expected_reference_hash = "sha256:" + pair_row["reference_plantuml_sha256"]
        author_hash = sha256_path(plantuml_path)
        fcstm_hash = sha256_path(fcstm_path)
        source_hash_ok = (
            author_hash == "sha256:" + source_meta["stm0_sha256"]
            and author_hash == "sha256:" + source_meta["source_stm0_sha256"]
            and sha256_path(nl_path) == "sha256:" + source_meta["nl_sha256"]
            and fcstm_hash == "sha256:" + fcstm_meta["selected_fcstm_sha256"]
            and reference_hash == expected_reference_hash
            and "sha256:" + source_meta["source_sha256"] == sha256_path(workbook_path)
        )
        frozen_inputs = closure["inputs"].get(pair_id, [])
        frozen_hashes = {entry["sha256"] for entry in frozen_inputs}
        closure_ok = author_hash in frozen_hashes and sha256_path(nl_path) in frozen_hashes
        provenance_ok = source_hash_ok and closure_ok
        if not provenance_ok:
            provenance_failures.append(ledger_id)

        author_artifact = ArtifactRef(
            role="DEFECTIVE_AUTHOR_PLANTUML",
            repository_path=repo_relative(repo_root, plantuml_path),
            sha256=author_hash,
            locator=None,
            author_source_authority=True,
            execution_eligibility="AUTHOR_SOURCE_FACT_ONLY",
            note="This is the frozen author PlantUML against which ledger source facts must be checked.",
        )
        derived_artifact = ArtifactRef(
            role="DERIVED_FCSTM_EXECUTION_ARTIFACT",
            repository_path=repo_relative(repo_root, fcstm_path),
            sha256=fcstm_hash,
            locator=None,
            author_source_authority=False,
            execution_eligibility="SOURCE_STATIC_ELIGIBLE_WITH_EXCLUSIONS; SIMULATION_INELIGIBLE",
            note="The FCSTM artifact is a representation conversion. Its metadata prohibits whole-model behavior and simulation attribution by default.",
        )
        reference_artifact = ArtifactRef(
            role="WORKBOOK_REFERENCE_PLANTUML_CANDIDATE",
            repository_path=None,
            sha256=reference_hash,
            locator=f"Experiment Results.xlsx#STM Results!{reference_cell}",
            author_source_authority=False,
            execution_eligibility="UNVERIFIED_CANDIDATE_REFERENCE",
            note="The candidate remains in the source workbook cell and has no per-issue materialized, compiled, or executed true-control record.",
        )
        family = ledger_id.split("-", 1)[0]
        source_refs = (
            SourceRef(
                role="CURRENT_LEDGER_ITEM",
                repository_path=repo_relative(repo_root, ledger_path),
                sha256=sha256_path(ledger_path),
                json_pointer=f"/items/{ledger_id}",
                line_number=None,
                locator=None,
                note="Current ledger identity, D/L tier, source paths, and provenance worksheet.",
            ),
            SourceRef(
                role="AUTHOR_BAD_PLANTUML",
                repository_path=repo_relative(repo_root, plantuml_path),
                sha256=author_hash,
                json_pointer=None,
                line_number=None,
                locator=None,
                note="Frozen defective author PlantUML source for this pair.",
            ),
            SourceRef(
                role="DERIVED_FCSTM_METADATA",
                repository_path=repo_relative(repo_root, fcstm_meta_path),
                sha256=sha256_path(fcstm_meta_path),
                json_pointer="/",
                line_number=None,
                locator=None,
                note="Conversion status and source-static/simulation eligibility boundary.",
            ),
            SourceRef(
                role="AUTHOR_SOURCE_METADATA",
                repository_path=repo_relative(repo_root, source_meta_path),
                sha256=sha256_path(source_meta_path),
                json_pointer="/source_cells/reference_plantuml",
                line_number=None,
                locator=reference_cell,
                note="Workbook row and reference PlantUML cell used only as an unverified candidate locator.",
            ),
            SourceRef(
                role="REFERENCE_CANDIDATE_INDEX",
                repository_path=repo_relative(repo_root, pairs_path),
                sha256=sha256_path(pairs_path),
                json_pointer=None,
                line_number=pair_line,
                locator=reference_cell,
                note="Reference PlantUML text hash for the workbook candidate, not a predicate result.",
            ),
            SourceRef(
                role="REFERENCE_WORKBOOK",
                repository_path=repo_relative(repo_root, workbook_path),
                sha256=sha256_path(workbook_path),
                json_pointer=None,
                line_number=None,
                locator=f"STM Results!{reference_cell}",
                note="Committed source workbook containing the candidate reference text.",
            ),
            SourceRef(
                role="FROZEN_X1V2_INPUT_CLOSURE",
                repository_path=repo_relative(repo_root, closure_path),
                sha256=sha256_path(closure_path),
                json_pointer=f"/inputs/{pair_id}",
                line_number=None,
                locator=None,
                note="Independent frozen closure confirming the author NL and PlantUML byte identities.",
            ),
            SourceRef(
                role="REFERENCE_SET_BOUNDARY",
                repository_path=repo_relative(repo_root, seed_registry_path),
                sha256=sha256_path(seed_registry_path),
                json_pointer="/reference_sets/0",
                line_number=None,
                locator=None,
                note="Reference PlantUML is explicitly separated from generated STM_0 material.",
            ),
        )
        records.append(
            PositiveControlCandidateRecord(
                ledger_id=ledger_id,
                pair_id=pair_id,
                ledger_family=family,
                ledger_d_tier=item["D"],
                ledger_l_tier=item["L"],
                bad_author_plantuml=author_artifact,
                bad_derived_fcstm=derived_artifact,
                reference_candidate=reference_artifact,
                candidate_status=UNVERIFIED_STATUS,
                positive_control_approved=False,
                cannot_default_to_true_reason=(
                    "The workbook reference is an independent candidate, not a per-ledger proof that this normalized obligation holds.",
                    "No predicate/property, typed input, semantic-equivalence review, or completed Boolean true receipt has been bound to this ledger ID.",
                    "The candidate has not been materialized and attribution-closed through any required conversion; the available FCSTM is simulation-ineligible by metadata.",
                    "Generic pyfcstm fixed fixtures test library behavior only and have no issue-level mapping to this ledger entry.",
                ),
                issue_specific_repaired_artifact=repair_check,
                remaining_prerequisites=prerequisites,
                provenance_check=AuditCheck(
                    check_id="AUTHOR_REFERENCE_LOCATOR_AND_HASH_CLOSURE",
                    status="PASS" if provenance_ok else "FAIL",
                    reason="Author PlantUML, derived FCSTM, source metadata, workbook reference cell, pairs index, and frozen X1v2 source closure all match their recorded hashes." if provenance_ok else "At least one author/reference locator or hash did not close; see source references and regenerate only after resolving the input discrepancy.",
                ),
                control_approval_check=AuditCheck(
                    check_id="APPROVED_COMPLETED_TRUE_CONTROL_PRESENT",
                    status="FAIL",
                    reason="Expected precursor failure: no issue-specific repaired artifact, semantic-equivalence proof, precommitted query, completed true receipt, or vacuity/contamination check exists yet.",
                ),
                source_refs=source_refs,
            )
        )

    top_inputs = (
        InputHash(role="CURRENT_LEDGER", repository_path=repo_relative(repo_root, ledger_path), sha256=sha256_path(ledger_path)),
        InputHash(role="PAIR_REFERENCE_INDEX", repository_path=repo_relative(repo_root, pairs_path), sha256=sha256_path(pairs_path)),
        InputHash(role="SOURCE_WORKBOOK", repository_path=repo_relative(repo_root, workbook_path), sha256=sha256_path(workbook_path)),
        InputHash(role="FROZEN_X1V2_INPUT_CLOSURE", repository_path=repo_relative(repo_root, closure_path), sha256=sha256_path(closure_path)),
        InputHash(role="REFERENCE_SET_REGISTRY", repository_path=repo_relative(repo_root, seed_registry_path), sha256=sha256_path(seed_registry_path)),
        InputHash(role="GENERIC_PYFCSTM_FIXTURE_EXCLUSION", repository_path=repo_relative(repo_root, fixture_path), sha256=sha256_path(fixture_path)),
        InputHash(role="TRACK_C_AUDIT_GENERATOR", repository_path=repo_relative(repo_root, Path(__file__)), sha256=sha256_path(Path(__file__))),
    )
    coverage = AuditCoverage(
        ledger_item_count=len(ledger["items"]),
        record_count=len(records),
        unique_ledger_id_count=len({record.ledger_id for record in records}),
        pair_count=len({record.pair_id for record in records}),
        provenance_pass_count=len(records) - len(provenance_failures),
        provenance_fail_count=len(provenance_failures),
        unverified_candidate_count=len(records),
        approved_positive_control_count=0,
        issue_specific_repaired_artifact_count=0,
    )
    unsigned: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "reviewer_id": REVIEWER_ID,
        "reviewed_at": reviewed_at,
        "source_commit": git_commit(repo_root),
        "pyfcstm_commit": git_commit(repo_root / "pyfcstm"),
        "input_hashes": [item.model_dump(mode="json") for item in top_inputs],
        "commands": [command, f"python {repo_relative(repo_root, Path(__file__))} --repo-root {repo_root} --paper-root {paper_root} --output-root {output_root} --reviewed-at {reviewed_at} --validate-only"],
        "execution_boundary": "predicate_execution_count=0; v60_actual_predicate_artifacts_read=0; method_runs=0; judge_runs=0; provider_calls=0. This artifact audit assigns no predicate, typed input, exactness relation, gold status, or canonical verdict.",
        "generic_fixture_exclusion": "pyfcstm/docs/source/tutorials/bmc/first_check_fixed.fcstm is a generic library fixture. It is not an author/reference artifact for any ledger ID and is not accepted as a positive control.",
        "checks": [
            AuditCheck(check_id="LEDGER_COVERAGE", status="PASS" if len(records) == 145 else "FAIL", reason="Every current ledger item is represented once in the audit." if len(records) == 145 else "Generated record count differs from current ledger count.").model_dump(mode="json"),
            AuditCheck(check_id="PROVENANCE_CLOSURE", status="PASS" if not provenance_failures else "FAIL", reason="Every record's author and reference locator/hash closure passed." if not provenance_failures else f"Provenance failures: {', '.join(provenance_failures)}").model_dump(mode="json"),
            AuditCheck(check_id="TRUE_CONTROL_APPROVAL", status="FAIL", reason="Expected precursor failure: all entries are deliberately retained as unverified candidates and no true control is claimed.").model_dump(mode="json"),
        ],
        "coverage": coverage.model_dump(mode="json"),
        "records": [record.model_dump(mode="json") for record in records],
    }
    return TrackCArtifactPositiveControlAudit(**unsigned, audit_sha256=canonical_sha256(unsigned))


def build_candidate_index(
    *,
    audit: TrackCArtifactPositiveControlAudit,
    audit_path: Path,
    repo_root: Path,
) -> PositiveControlCandidateIndex:
    """Create a compact all-ledger candidate index from the full audit."""

    entries = tuple(
        CandidateIndexEntry(
            ledger_id=record.ledger_id,
            pair_id=record.pair_id,
            candidate_status=record.candidate_status,
            reference_locator=record.reference_candidate.locator or "missing",
            reference_plantuml_sha256=record.reference_candidate.sha256,
            bad_author_plantuml_sha256=record.bad_author_plantuml.sha256,
            bad_fcstm_sha256=record.bad_derived_fcstm.sha256,
            issue_specific_repaired_artifact_exists=False,
            approval_prerequisite_ids=tuple(item.prerequisite_id for item in record.remaining_prerequisites),
            audit_record_pointer=f"/records/{index}",
        )
        for index, record in enumerate(audit.records)
    )
    unsigned: dict[str, Any] = {
        "schema_version": CANDIDATE_INDEX_SCHEMA_VERSION,
        "reviewer_id": REVIEWER_ID,
        "generated_at": audit.reviewed_at,
        "audit_path": repo_relative(repo_root, audit_path),
        "audit_file_sha256": sha256_path(audit_path),
        "no_positive_control_claim": True,
        "entries": [entry.model_dump(mode="json") for entry in entries],
    }
    return PositiveControlCandidateIndex(**unsigned, index_sha256=canonical_sha256(unsigned))


def render_markdown(audit: TrackCArtifactPositiveControlAudit, index: PositiveControlCandidateIndex) -> str:
    """Render a human-readable companion without duplicating canonical truth fields."""

    by_pair: dict[str, list[PositiveControlCandidateRecord]] = {}
    for record in audit.records:
        by_pair.setdefault(record.pair_id, []).append(record)
    rows = [
        "# Track C Artifact and Positive-Control Precursor Audit",
        "",
        "This is provenance-only. It does not select a predicate, typed inputs, gold status, or semantic verdict, and it does not execute a predicate.",
        "",
        "## Result",
        "",
        f"- Reviewer: `{audit.reviewer_id}`",
        f"- Coverage: `{audit.coverage.record_count}/{audit.coverage.ledger_item_count}` ledger IDs across `{audit.coverage.pair_count}` pairs",
        f"- Provenance locator/hash closure: `{audit.coverage.provenance_pass_count}` PASS, `{audit.coverage.provenance_fail_count}` FAIL",
        f"- Candidate status: `{UNVERIFIED_STATUS}` for all `{audit.coverage.unverified_candidate_count}` entries",
        "- Approved positive controls: `0`; issue-specific repaired artifacts: `0`",
        "",
        "Every candidate still requires materialization, obligation-equivalence review, attribution closure, precommitted property/inputs, a completed Boolean true receipt, and vacuity/contamination checks.",
        "",
        "## Boundary",
        "",
        audit.execution_boundary,
        "",
        "The workbook reference and the generic `pyfcstm` fixed fixture are not positive controls in this audit. The canonical per-ledger records and hashes are in the adjacent JSON files.",
        "",
        "## Pair Coverage",
        "",
        "| Pair | Ledger IDs | Reference candidate locator | Reference SHA-256 |",
        "| --- | --- | --- | --- |",
    ]
    for pair_id, records in sorted(by_pair.items()):
        first = records[0]
        rows.append(
            f"| {pair_id} | {', '.join(record.ledger_id for record in records)} | {first.reference_candidate.locator} | `{first.reference_candidate.sha256}` |"
        )
    rows.extend(
        [
            "",
            "## Files",
            "",
            f"- Full audit canonical hash: `{audit.audit_sha256}`",
            f"- Candidate index canonical hash: `{index.index_sha256}`",
            f"- Candidate index audit-file hash: `{index.audit_file_sha256}`",
            "",
        ]
    )
    return "\n".join(rows)


def validate_outputs(*, audit_path: Path, index_path: Path, expected_ledger_ids: set[str]) -> None:
    """Validate persisted files, complete coverage, and the no-approval boundary."""

    audit_payload = json.loads(audit_path.read_text(encoding="utf-8"))
    stored_audit_hash = audit_payload.pop("audit_sha256")
    if stored_audit_hash != canonical_sha256(audit_payload):
        raise ValueError("persisted audit canonical hash does not match its payload")
    audit = TrackCArtifactPositiveControlAudit.model_validate({**audit_payload, "audit_sha256": stored_audit_hash})
    index_payload = json.loads(index_path.read_text(encoding="utf-8"))
    stored_index_hash = index_payload.pop("index_sha256")
    if stored_index_hash != canonical_sha256(index_payload):
        raise ValueError("persisted candidate-index canonical hash does not match its payload")
    index = PositiveControlCandidateIndex.model_validate({**index_payload, "index_sha256": stored_index_hash})
    audit_ids = {record.ledger_id for record in audit.records}
    index_ids = {entry.ledger_id for entry in index.entries}
    if audit_ids != expected_ledger_ids or index_ids != expected_ledger_ids:
        raise ValueError("persisted audit/index ledger IDs do not exactly match the current ledger")
    if any(record.candidate_status != UNVERIFIED_STATUS for record in audit.records):
        raise ValueError("audit contains a non-unverified candidate")
    if any(record.positive_control_approved for record in audit.records):
        raise ValueError("audit contains an approved positive control")
    if index.audit_file_sha256 != sha256_path(audit_path):
        raise ValueError("candidate index does not bind the persisted audit file hash")


def parse_args() -> argparse.Namespace:
    """Parse explicit filesystem paths for deterministic local generation."""

    parser = argparse.ArgumentParser(description="Generate Track C positive-control provenance audit without predicate execution.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--reviewed-at", required=True)
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Generate or validate the all-ledger Track C candidate records."""

    args = parse_args()
    audit_path = args.output_root / "review" / "precursor" / "track_c_artifact_positive_control_audit.json"
    index_path = args.output_root / "review" / "positive_control_candidates.json"
    markdown_path = args.output_root / "review" / "precursor" / "track_c_artifact_positive_control_audit.md"
    ledger_path = args.paper_root / "discover_matrix" / "ledger_v2" / "ledger.json"
    expected_ids = set(json.loads(ledger_path.read_text(encoding="utf-8"))["items"])
    if args.validate_only:
        validate_outputs(audit_path=audit_path, index_path=index_path, expected_ledger_ids=expected_ids)
        print(json.dumps({"status": "valid", "ledger_item_count": len(expected_ids)}, sort_keys=True))
        return 0
    command = " ".join(
        [
            "python",
            repo_relative(args.repo_root, Path(__file__)),
            "--repo-root",
            str(args.repo_root),
            "--paper-root",
            str(args.paper_root),
            "--output-root",
            str(args.output_root),
            "--reviewed-at",
            args.reviewed_at,
        ]
    )
    audit = build_audit(
        repo_root=args.repo_root,
        paper_root=args.paper_root,
        output_root=args.output_root,
        reviewed_at=args.reviewed_at,
        command=command,
    )
    write_json(audit_path, audit)
    index = build_candidate_index(audit=audit, audit_path=audit_path, repo_root=args.repo_root)
    write_json(index_path, index)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(render_markdown(audit, index), encoding="utf-8")
    validate_outputs(audit_path=audit_path, index_path=index_path, expected_ledger_ids=expected_ids)
    print(json.dumps({"status": "generated", "ledger_item_count": len(audit.records), "audit_path": str(audit_path), "index_path": str(index_path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
