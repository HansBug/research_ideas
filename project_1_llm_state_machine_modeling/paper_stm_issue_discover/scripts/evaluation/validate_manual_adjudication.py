"""Fail-closed provider-free validator for manual adjudication v2 artifacts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from collections import Counter
from pathlib import Path

from paper_stm_evaluation.manual_adjudication import (
    GroupDecisionSet,
    Pane5ManualInput,
    RawInventory,
    RelationAuditSet,
    ReportDecisionSet,
    validate_group_decisions,
    validate_decision_set,
    validate_tsv_mirror,
)
from build_reviewer_projection import (
    FORBIDDEN_KEYS,
    SEMANTIC_FORBIDDEN_KEYS,
    canonical_bytes,
    sha256_file as projection_sha256_file,
)


REQUIRED_FILES = (
    "v60_report_decisions.json",
    "v60_report_decisions.tsv",
    "x1v2_report_decisions.json",
    "x1v2_report_decisions.tsv",
    "relation_decisions.json",
    "hit_max_witness.json",
    "group_decisions.json",
    "summary.json",
    "reference_ledger_aggregate.json",
    "predicate_witness_audit.json",
    "review_log.json",
    "pane5_evidence_reads.json",
    "pane5_adjudications.json",
    "human_supervised_authorization.json",
    "predicate_source_provenance.json",
    "reviewer_projection_audit.json",
    "reviewer_input_projection.jsonl",
    "reviewer_unblind_mapping.json",
    "schema.md",
    "README.md",
    "MANIFEST",
)

STRUCTURED_FILE_SHAPES = {
    "hit_max_witness.json": ("schema", "witnesses"),
    "summary.json": ("schema", "sides"),
    "reference_ledger_aggregate.json": ("schema", "aggregates"),
    "predicate_witness_audit.json": ("schema", "sides"),
    "review_log.json": ("schema", "entries"),
}

EXPECTED_CELLS = {"v60_current": 162, "x1v2_baseline": 162}
EXPECTED_REPORTS = {"v60_current": 1271, "x1v2_baseline": 512}
EXPECTED_BY_ROUND = {
    "v60_current": {"1": 415, "2": 446, "3": 410},
    "x1v2_baseline": {"1": 173, "2": 163, "3": 176},
}


def load_object(path: Path) -> dict:
    """Load one JSON object from the versioned audit directory."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    """Hash one archive file for immutable closure checks."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def resolve_json_pointer(document: object, pointer: str) -> object:
    """Resolve an RFC 6901 JSON Pointer without using text heuristics."""

    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON Pointer: {pointer}")
    value = document
    for raw_token in pointer.split("/")[1:]:
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            if token not in value:
                raise ValueError(f"JSON Pointer target is missing: {pointer}")
            value = value[token]
        elif isinstance(value, list):
            try:
                value = value[int(token)]
            except (ValueError, IndexError) as exc:
                raise ValueError(f"JSON Pointer list target is missing: {pointer}") from exc
        else:
            raise ValueError(f"JSON Pointer traverses a scalar: {pointer}")
    return value


def build_inventory_from_archive(archive: Path) -> RawInventory:
    """Rebuild inventory through the provider-free inventory generator."""

    source = Path(__file__).with_name("build_manual_inventory.py")
    spec = importlib.util.spec_from_file_location("paper1_manual_inventory_validator", source)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load inventory generator: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_inventory(archive)


def validate_raw_inventory(directory: Path, inventory: RawInventory) -> None:
    """Re-enumerate the archive and validate every inventory pointer and hash."""

    archive = directory.parent.parent
    rebuilt = build_inventory_from_archive(archive)
    stored = inventory.model_dump(mode="json")
    current = rebuilt.model_dump(mode="json")
    stored.pop("generated_at_utc", None)
    current.pop("generated_at_utc", None)
    if stored != current:
        raise ValueError("inventory does not equal a fresh enumeration of the frozen archive")
    if inventory.cells != EXPECTED_CELLS or inventory.reports != EXPECTED_REPORTS or inventory.by_round != EXPECTED_BY_ROUND:
        raise ValueError("raw inventory does not close over the frozen cell/report/round universe")
    file_hash_cache: dict[Path, str] = {}
    document_cache: dict[Path, dict] = {}

    def cached_hash(path: Path) -> str:
        """Hash each archive file once while checking many report pointers."""

        if path not in file_hash_cache:
            file_hash_cache[path] = sha256_file(path)
        return file_hash_cache[path]

    def cached_document(path: Path) -> dict:
        """Parse each JSON raw artifact once while checking many reports."""

        if path not in document_cache:
            document_cache[path] = load_object(path)
        return document_cache[path]

    for relative_path, expected_hash in inventory.source_manifests.items():
        manifest_path = (archive / relative_path).resolve()
        if not manifest_path.is_file() or cached_hash(manifest_path) != expected_hash:
            raise ValueError(f"source manifest hash mismatch: {relative_path}")

    x1v2_witness_ids = {
        str(record.get("work_item", {}).get("original_report_id"))
        for record in load_object(archive / "derived" / "x1v2_witness_level_audit.json").get("records", [])
    }
    for item in inventory.items:
        raw_path = (archive / item.raw_method_path).resolve()
        try:
            raw_path.relative_to(archive.resolve())
        except ValueError as exc:
            raise ValueError(f"raw path escapes archive: {item.raw_method_path}") from exc
        if not raw_path.is_file():
            raise ValueError(f"raw file is missing: {item.raw_method_path}")
        if cached_hash(raw_path) != item.raw_sha256:
            raise ValueError(f"raw SHA-256 mismatch: {item.report_id}")
        document = cached_document(raw_path)
        target = resolve_json_pointer(document, item.raw_json_pointer)
        resolve_json_pointer(document, item.claim_pointer)
        resolve_json_pointer(document, item.where_pointer)
        if not isinstance(target, dict):
            raise ValueError(f"raw report target is not an object: {item.report_id}")
        pair_key = "pair_id" if item.side.value == "v60_current" else "case"
        if str(document.get(pair_key)) != item.pair_id or int(document.get("round", -1)) != item.round:
            raise ValueError(f"raw side/pair/round mismatch: {item.report_id}")
        if item.side.value == "v60_current" and str(target.get("issue_id")) != item.report_id:
            raise ValueError(f"raw v60 report ID mismatch: {item.report_id}")
        if item.side.value == "x1v2_baseline" and item.report_id not in x1v2_witness_ids:
            raise ValueError(f"raw X1v2 report ID is not present in witness provenance: {item.report_id}")


def validate_w2_witnesses(archive: Path, decisions: list) -> None:
    """Validate W2 receipt bytes and the exact terminal receipt object."""

    for decision in decisions:
        if decision.witness.level.value != "W2":
            continue
        receipt = decision.witness.receipt
        executable = decision.witness.executable_object
        assert receipt is not None and executable is not None
        if receipt.artifact_sha256 != executable.artifact_sha256:
            raise ValueError(f"W2 artifact hash mismatch: {decision.report_id}")
        receipt_path = (archive / receipt.repository_path).resolve()
        try:
            receipt_path.relative_to(archive.resolve())
        except ValueError as exc:
            raise ValueError(f"W2 receipt path escapes archive: {decision.report_id}") from exc
        if not receipt_path.is_file() or sha256_file(receipt_path) != receipt.receipt_sha256:
            raise ValueError(f"W2 receipt file hash mismatch: {decision.report_id}")
        receipt_document = load_object(receipt_path)
        receipt_object = resolve_json_pointer(receipt_document, receipt.json_pointer)
        if not isinstance(receipt_object, dict):
            raise ValueError(f"W2 receipt pointer does not target an object: {decision.report_id}")
        # The canonical contract calls this value ``terminal_result`` while
        # the frozen method receipt calls it ``verdict``.  Validate the
        # explicit field mapping; do not infer execution success from prose.
        receipt_fields = (
            ("receipt_id", receipt.receipt_id, "receipt_id"),
            ("terminal_result", receipt.terminal_result, "verdict"),
        )
        for canonical_name, expected, raw_name in receipt_fields:
            if raw_name not in receipt_object or str(receipt_object[raw_name]) != expected:
                raise ValueError(f"W2 receipt field mismatch ({canonical_name}/{raw_name}): {decision.report_id}")
        artifact_path = (archive / receipt.artifact_repository_path).resolve()
        try:
            artifact_path.relative_to(archive.resolve())
        except ValueError as exc:
            raise ValueError(f"W2 artifact path escapes archive: {decision.report_id}") from exc
        if not artifact_path.is_file() or sha256_file(artifact_path) != receipt.artifact_sha256:
            raise ValueError(f"W2 evaluated artifact hash mismatch: {decision.report_id}")


def validate_source_refs(archive: Path, decisions: list, groups: list | None = None) -> None:
    """Resolve every source reference to an archive file and optional JSON pointer."""

    refs = [ref for decision in decisions for ref in decision.source_refs]
    refs.extend(
        ref
        for decision in decisions
        for relation in decision.relations
        for ref in relation.source_refs
    )
    if groups:
        refs.extend(ref for group in groups for ref in group.source_refs)
    file_cache: dict[Path, dict] = {}
    hash_cache: dict[Path, str] = {}
    for ref in refs:
        path = (archive / ref.repository_path).resolve()
        try:
            path.relative_to(archive.resolve())
        except ValueError as exc:
            raise ValueError(f"source ref escapes archive: {ref.repository_path}") from exc
        if not path.is_file():
            raise ValueError(f"source ref file is missing: {ref.repository_path}")
        if path not in hash_cache:
            hash_cache[path] = sha256_file(path)
        if hash_cache[path] != ref.sha256:
            raise ValueError(f"source ref hash mismatch: {ref.repository_path}")
        if ref.json_pointer is not None:
            if path not in file_cache:
                file_cache[path] = load_object(path)
            resolve_json_pointer(file_cache[path], ref.json_pointer)
        if ref.line is not None:
            line_count = path.read_text(encoding="utf-8").count("\n") + 1
            if ref.line > line_count:
                raise ValueError(f"source ref line is outside file: {ref.repository_path}:{ref.line}")


def validate_structured_supporting_files(
    directory: Path,
    decisions: list,
    expected_ids: tuple[str, ...],
) -> dict[str, dict]:
    """Validate aggregate content against the canonical report decisions."""

    loaded: dict[str, dict] = {}
    for name, fields in STRUCTURED_FILE_SHAPES.items():
        value = load_object(directory / name)
        if not value.get("schema") or any(field not in value for field in fields[1:]):
            raise ValueError(f"{name} lacks its required schema envelope: {fields}")
        loaded[name] = value

    by_side = {
        side: [decision for decision in decisions if decision.side.value == side]
        for side in ("v60_current", "x1v2_baseline")
    }
    summary_sides = loaded["summary.json"]["sides"]
    if set(summary_sides) != set(by_side):
        raise ValueError("summary sides do not match the two decision sets")
    for side, side_decisions in by_side.items():
        summary = summary_sides[side]
        expected_counts = {
            "report_count": len(side_decisions),
            "decision_counts": dict(Counter(decision.strict_da.value for decision in side_decisions)),
            "validity_counts": dict(Counter(decision.validity.value for decision in side_decisions)),
            "kni_counts": dict(Counter(decision.corrected_kni for decision in side_decisions)),
            "witness_counts": dict(Counter(decision.witness.level.value for decision in side_decisions)),
            "relation_counts": dict(Counter(
                relation.relation.value
                for decision in side_decisions
                for relation in decision.relations
            )),
        }
        for field_name, expected_value in expected_counts.items():
            if summary.get(field_name) != expected_value:
                raise ValueError(f"summary {side}.{field_name} does not match canonical decisions")

    report_by_id = {decision.report_id: decision for decision in decisions}
    witnesses = loaded["hit_max_witness.json"]["witnesses"]
    witness_keys = {(row.get("side"), row.get("expected_id"), row.get("round")) for row in witnesses}
    expected_witness_keys = {
        (side, expected_id, round_no)
        for side in by_side
        for expected_id in expected_ids
        for round_no in (1, 2, 3)
    }
    if len(witnesses) != len(witness_keys) or witness_keys != expected_witness_keys:
        raise ValueError("hit_max_witness.json is not a dense side/expected/round projection")
    for witness in witnesses:
        support_ids = witness.get("supporting_report_ids")
        if not isinstance(support_ids, list):
            raise ValueError("hit witness supporting_report_ids must be a list")
        if len(support_ids) != len(set(support_ids)):
            raise ValueError("hit witness repeats a supporting report")
        expected_max = None
        for report_id in support_ids:
            decision = report_by_id.get(report_id)
            if decision is None:
                raise ValueError(f"hit witness references unknown report: {report_id}")
            if decision.side.value != witness["side"] or decision.round != witness["round"]:
                raise ValueError(f"hit witness crosses side or round: {report_id}")
            if not any(
                row.expected_id == witness["expected_id"] and row.relation.value == "FULL_MATCH"
                for row in decision.relations
            ) or decision.validity.value != "VALID_KNOWN":
                raise ValueError(f"hit witness is not backed by VALID_KNOWN + FULL: {report_id}")
            witness_level = decision.witness.level.value
            if expected_max is None or {"W0": 0, "W1": 1, "W2": 2}[witness_level] > {"W0": 0, "W1": 1, "W2": 2}[expected_max]:
                expected_max = witness_level
        if witness.get("max_witness_level") != expected_max:
            raise ValueError("hit witness has an invalid max_witness_level")

    review_entries = loaded["review_log.json"]["entries"]
    review_ids = {entry.get("report_id") for entry in review_entries if isinstance(entry, dict)}
    if review_ids != set(report_by_id) or len(review_entries) != len(review_ids):
        raise ValueError("review_log.json does not contain exactly one entry per report decision")
    required_review_fields = {
        "primary_reviewer_id", "independent_reviewer_id", "final_adjudicator_id",
        "human_confirmation", "human_supervised_session", "review_status", "submission_hash",
        "confirmed_at", "confirmation_basis", "independent_submission_at",
        "primary_submission_at", "blind_event_sequence", "attestation",
        "human_supervised_authorization",
    }
    for entry in review_entries:
        if not required_review_fields.issubset(entry):
            raise ValueError("review_log entry lacks human/blind review attestation fields")
        if entry["human_confirmation"] is not True or entry["review_status"] not in {"ARBITRATED", "FINAL"}:
            raise ValueError("review_log contains a non-final human attestation")
        if entry["human_supervised_session"] is not True or not entry["confirmed_at"] or not entry["confirmation_basis"]:
            raise ValueError("review_log lacks per-report human confirmation evidence")
        if not entry["independent_submission_at"] or not entry["primary_submission_at"]:
            raise ValueError("review_log lacks blind submission timestamps")
        if not isinstance(entry["blind_event_sequence"], list) or len(entry["blind_event_sequence"]) < 3:
            raise ValueError("review_log lacks the blind event sequence")
        if not entry["attestation"] or not entry["human_supervised_authorization"]:
            raise ValueError("review_log lacks authorization or attestation")
        decision = report_by_id[entry["report_id"]]
        review = decision.review
        for field_name in (
            "primary_reviewer_id", "independent_reviewer_id", "final_adjudicator_id",
            "human_confirmation", "review_status", "submission_hash",
            "confirmed_at", "confirmation_basis", "independent_submission_at",
            "primary_submission_at", "blind_event_sequence",
        ):
            expected = getattr(review, field_name)
            if hasattr(expected, "value"):
                expected = expected.value
            if isinstance(expected, tuple):
                expected = list(expected)
            if entry[field_name] != expected:
                raise ValueError(f"review_log differs from decision review: {entry['report_id']}/{field_name}")

    predicate_sides = loaded["predicate_witness_audit.json"]["sides"]
    baseline_predicates = predicate_sides.get("x1v2_baseline")
    if not isinstance(baseline_predicates, dict) or baseline_predicates.get("status") != "not_applicable":
        raise ValueError("X1v2 predicate witness audit must be explicitly not_applicable")
    registry = load_object(directory.parent.parent / "reference" / "predicate_registry.json")
    registry_ids = {
        predicate["id"]
        for family in registry.get("families", [])
        for predicate in family.get("predicates", [])
    }
    current_predicates = predicate_sides.get("v60_current", {})
    predicate_rows = current_predicates.get("predicate_rows")
    if not isinstance(predicate_rows, list):
        raise ValueError("current predicate audit must contain predicate_rows")
    predicate_ids = {row.get("predicate_id") for row in predicate_rows if isinstance(row, dict)}
    if len(predicate_rows) != len(predicate_ids) or predicate_ids != registry_ids:
        raise ValueError("current predicate audit does not cover the frozen 19-predicate registry")
    planned_scope = current_predicates.get("planned_scope")
    if not isinstance(planned_scope, dict):
        raise ValueError("current predicate audit must separate frozen planned scope from report-bound usage")
    planned_ids = planned_scope.get("predicate_ids")
    if (
        not isinstance(planned_ids, list)
        or not all(isinstance(item, str) for item in planned_ids)
        or planned_scope.get("count") != len(planned_ids)
        or planned_scope.get("count") != len(set(planned_ids))
        or not set(planned_ids).issubset(registry_ids)
        or not isinstance(planned_scope.get("scope_id"), str)
        or not planned_scope.get("source_path")
        or not isinstance(planned_scope.get("source_sha256"), str)
    ):
        raise ValueError("frozen planned predicate scope is malformed")
    planned_source = directory.parent.parent / planned_scope["source_path"]
    if not planned_source.is_file() or sha256_file(planned_source) != planned_scope["source_sha256"]:
        raise ValueError("frozen planned predicate scope source hash mismatch")
    row_by_predicate = {row["predicate_id"]: row for row in predicate_rows}
    for predicate_id in registry_ids:
        row = row_by_predicate[predicate_id]
        if not isinstance(row.get("planned_in_frozen_scope"), bool):
            raise ValueError(f"predicate row lacks frozen scope membership: {predicate_id}")
        if row["planned_in_frozen_scope"] != (predicate_id in planned_ids):
            raise ValueError(f"predicate row planned scope membership mismatch: {predicate_id}")
        if not isinstance(row.get("report_bound_plan_count"), int) or row["report_bound_plan_count"] < 0:
            raise ValueError(f"predicate row lacks report-bound plan count: {predicate_id}")
    return loaded


def validate_reviewer_projection(directory: Path, inventory: RawInventory) -> None:
    """Verify redaction, uniform shape, and pair/round slot symmetry."""

    audit = load_object(directory / "reviewer_projection_audit.json")
    unblind = load_object(directory / "reviewer_unblind_mapping.json")
    projection_path = directory / "reviewer_input_projection.jsonl"
    if audit.get("projection_path") != str(projection_path.relative_to(directory.parent.parent)):
        raise ValueError("reviewer projection path is not archive-relative")
    if audit.get("projection_sha256") != projection_sha256_file(projection_path):
        raise ValueError("reviewer projection hash mismatch")
    if audit.get("projected_report_count") != len(inventory.items) or audit.get("provider_calls") != 0:
        raise ValueError("reviewer projection does not close over inventory or is not provider-free")
    all_forbidden_keys = FORBIDDEN_KEYS | SEMANTIC_FORBIDDEN_KEYS
    if set(audit.get("forbidden_keys", [])) != set(all_forbidden_keys):
        raise ValueError("reviewer projection forbidden-key contract changed")
    rows = []
    with projection_path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError("reviewer projection contains a non-object row")
            rows.append(row)
    if audit.get("row_count") != len(rows):
        raise ValueError("reviewer projection row count mismatch")
    seen = set()
    expected_row_keys = {
        "schema", "review_key", "arm_token", "pair_token", "round", "slot",
        "report_evidence",
        "author_source", "redactions_applied", "projection_sha256",
    }
    expected_report_keys = {"claim_text", "reason_text", "location_text"}
    expected_author_keys = {"nl", "plantuml", "nl_sha256", "plantuml_sha256"}

    def scan(value: object) -> None:
        if isinstance(value, dict):
            if set(value) & all_forbidden_keys:
                raise ValueError("reviewer projection contains a sealed provider/model/prompt/semantic key")
            for child in value.values():
                scan(child)
        elif isinstance(value, list):
            for child in value:
                scan(child)

    arm_slot_keys: dict[str, set[tuple[str, int, int]]] = {"arm-a": set(), "arm-b": set()}
    padded = 0
    source_by_slot: dict[tuple[str, int, int], dict] = {}
    for row in rows:
        if set(row) != expected_row_keys:
            raise ValueError("reviewer projection row shape is not side-neutral")
        if set(row["report_evidence"]) != expected_report_keys:
            raise ValueError("reviewer projection report evidence shape is not side-neutral")
        if row["report_evidence"]["location_text"] != "":
            raise ValueError("reviewer projection exposes a producer-specific location")
        if any(
            "llms_emp_feedback_final_" in row["report_evidence"][field]
            for field in ("claim_text", "reason_text")
        ):
            raise ValueError("reviewer projection exposes a producer-specific claim or reason")
        if set(row["author_source"]) != expected_author_keys:
            raise ValueError("reviewer projection author-source shape is not side-neutral")
        if row["redactions_applied"] is not True:
            raise ValueError("reviewer projection must declare uniform redaction")
        if row.get("arm_token") not in arm_slot_keys or not isinstance(row.get("slot"), int) or row["slot"] < 0:
            raise ValueError("reviewer projection has an invalid arm or slot")
        key = row.get("review_key")
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError("reviewer projection has duplicate or missing review key")
        seen.add(key)
        slot_key = (row["pair_token"], row["round"], row["slot"])
        arm_slot_keys[row["arm_token"]].add(slot_key)
        prior_source = source_by_slot.setdefault(slot_key, row["author_source"])
        if prior_source != row["author_source"]:
            raise ValueError("reviewer projection source closure differs across sealed arms")
        stored_hash = row.get("projection_sha256")
        unsigned = dict(row)
        unsigned.pop("projection_sha256", None)
        if stored_hash != "sha256:" + hashlib.sha256(canonical_bytes(unsigned)).hexdigest():
            raise ValueError("reviewer projection row hash mismatch")
        scan(row)
    if arm_slot_keys["arm-a"] != arm_slot_keys["arm-b"]:
        raise ValueError("reviewer projection pair/round slot universe differs across sealed arms")
    if unblind.get("schema") != "paper1.manual-adjudication.reviewer-unblind-map.v1" or unblind.get("raw_first_visible") is not False:
        raise ValueError("reviewer unblind mapping is missing its sealed-audit contract")
    if set(unblind.get("arm_tokens", {})) != {"v60_current", "x1v2_baseline"}:
        raise ValueError("reviewer unblind mapping arm closure is malformed")
    mapping_rows = unblind.get("rows")
    if not isinstance(mapping_rows, list) or len(mapping_rows) != len(rows):
        raise ValueError("reviewer unblind mapping does not close over projection rows")
    mapping_by_key = {row.get("review_key"): row for row in mapping_rows if isinstance(row, dict)}
    if len(mapping_by_key) != len(mapping_rows) or set(mapping_by_key) != seen:
        raise ValueError("reviewer unblind mapping review-key closure failed")
    projection_by_key = {row["review_key"]: row for row in rows}
    inventory_by_id = {item.report_id: item for item in inventory.items}
    seen_reports: set[str] = set()
    padded = 0
    for review_key, row in mapping_by_key.items():
        projection = projection_by_key[review_key]
        if row.get("padded") is True:
            padded += 1
            if row.get("report_id") is not None or row.get("raw_target_sha256") is not None:
                raise ValueError("reviewer unblind padding carries a raw report")
            if any(projection["report_evidence"].values()):
                raise ValueError("reviewer projection padded slot contains report evidence")
            continue
        report_id = row.get("report_id")
        item = inventory_by_id.get(report_id)
        if item is None or report_id in seen_reports:
            raise ValueError("reviewer unblind mapping report closure failed")
        seen_reports.add(report_id)
        expected = (item.side.value, item.pair_id, item.round)
        if (row.get("side"), row.get("pair_id"), row.get("round")) != expected:
            raise ValueError("reviewer unblind mapping changes an inventory identity")
        if projection["arm_token"] != unblind["arm_tokens"].get(item.side.value):
            raise ValueError("reviewer projection arm token disagrees with the sealed mapping")
        if projection["pair_token"] != unblind.get("pair_tokens", {}).get(item.pair_id):
            raise ValueError("reviewer projection pair token disagrees with the sealed mapping")
        if projection["round"] != item.round or projection["slot"] != row.get("slot"):
            raise ValueError("reviewer projection location disagrees with the sealed mapping")
        raw_path = directory.parent.parent / item.raw_method_path
        raw = load_object(raw_path)
        target = resolve_json_pointer(raw, item.raw_json_pointer)
        if row.get("raw_target_sha256") != canonical_json_sha256(target):
            raise ValueError("reviewer unblind mapping target hash mismatch")
    if seen_reports != set(inventory_by_id):
        raise ValueError("reviewer unblind mapping does not close over all reports")
    if audit.get("padded_slot_count") != padded:
        raise ValueError("reviewer projection padded-slot count mismatch")


def canonical_json_sha256(value: object) -> str:
    """Hash a JSON value using the evidence recorder's canonical encoding."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def validate_human_process_files(
    directory: Path,
    inventory: RawInventory,
    decisions: list,
    expected_ids: tuple[str, ...],
) -> None:
    """Close every final row over the pane5 evidence-read and authorization ledgers."""

    archive = directory.parent.parent
    decision_by_id = {decision.report_id: decision for decision in decisions}
    evidence_document = load_object(directory / "pane5_evidence_reads.json")
    evidence_rows = evidence_document.get("rows")
    if evidence_document.get("schema") != "paper1.manual-adjudication.evidence-read.v1" or not isinstance(evidence_rows, list):
        raise ValueError("pane5_evidence_reads.json has an invalid schema or rows field")
    evidence_by_id = {str(row.get("report_id")): row for row in evidence_rows if isinstance(row, dict)}
    if len(evidence_rows) != len(evidence_by_id) or set(evidence_by_id) != set(decision_by_id):
        raise ValueError("pane5_evidence_reads.json does not close exactly over final decisions")

    raw_cache: dict[Path, dict] = {}
    ledger = load_object(archive / "reference" / "ledger.json")
    expected_digest_rows = [
        {
            "expected_id": expected_id,
            "pair": str(ledger["items"][expected_id].get("pair", "")),
            "summary_sha256": canonical_json_sha256({
                "summary": ledger["items"][expected_id].get("summary"),
                "D": ledger["items"][expected_id].get("D"),
                "L": ledger["items"][expected_id].get("L"),
            }),
        }
        for expected_id in sorted(expected_ids)
    ]
    expected_digest = canonical_json_sha256(expected_digest_rows)
    ledger_hash = sha256_file(archive / "reference" / "ledger.json")
    for report_id, decision in decision_by_id.items():
        row = evidence_by_id[report_id]
        if row.get("raw_read") is not True or row.get("author_source_read") is not True:
            raise ValueError(f"pane5 evidence read flags are incomplete: {report_id}")
        for field_name, expected in (
            ("side", decision.side.value), ("pair_id", decision.pair_id), ("round", decision.round),
            ("raw_method_path", decision.raw_method_path), ("raw_json_pointer", decision.raw_json_pointer),
            ("raw_sha256", decision.raw_sha256), ("claim_pointer", decision.claim_pointer),
            ("where_pointer", decision.where_pointer), ("expected_count", len(expected_ids)),
            ("expected_digest", expected_digest), ("ledger_sha256", ledger_hash),
        ):
            if row.get(field_name) != expected:
                raise ValueError(f"pane5 evidence closure mismatch: {report_id}/{field_name}")
        raw_path = archive / decision.raw_method_path
        if raw_path not in raw_cache:
            raw_cache[raw_path] = load_object(raw_path)
        target = resolve_json_pointer(raw_cache[raw_path], decision.raw_json_pointer)
        if row.get("raw_target_sha256") != canonical_json_sha256(target):
            raise ValueError(f"pane5 target digest mismatch: {report_id}")
        author_source = row.get("author_source")
        if not isinstance(author_source, dict):
            raise ValueError(f"pane5 author source evidence is missing: {report_id}")
        for path_field, hash_field in (("nl_path", "nl_sha256"), ("plantuml_path", "plantuml_sha256")):
            source_path = archive / str(author_source.get(path_field, ""))
            if not source_path.is_file() or sha256_file(source_path) != author_source.get(hash_field):
                raise ValueError(f"pane5 author source hash mismatch: {report_id}/{path_field}")
        digest_payload = deepcopy(row)
        evidence_digest = digest_payload.pop("evidence_digest", None)
        if evidence_digest != canonical_json_sha256(digest_payload):
            raise ValueError(f"pane5 evidence digest is not reproducible: {report_id}")

    pane5_document = load_object(directory / "pane5_adjudications.json")
    pane5_rows = pane5_document.get("rows")
    if pane5_document.get("schema") != "paper1.manual-adjudication.pane5-manual-input.v2" or not isinstance(pane5_rows, list):
        raise ValueError("pane5_adjudications.json has an invalid schema or rows field")
    pane5_models = [Pane5ManualInput.model_validate(row) for row in pane5_rows]
    pane5_by_id = {row.report_id: row for row in pane5_models}
    if len(pane5_rows) != len(pane5_by_id) or set(pane5_by_id) != set(decision_by_id):
        raise ValueError("pane5_adjudications.json does not close exactly over final decisions")
    for report_id, decision in decision_by_id.items():
        row = pane5_by_id[report_id]
        evidence = evidence_by_id[report_id]
        if not row.human_confirmation or not row.human_supervised_session:
            raise ValueError(f"pane5 adjudication is not human-supervised: {report_id}")
        if row.reviewer_id != decision.review.final_adjudicator_id:
            raise ValueError(f"pane5 adjudicator mismatch: {report_id}")
        if row.evidence_digest != evidence["evidence_digest"]:
            raise ValueError(f"pane5 adjudication evidence mismatch: {report_id}")
        if row.strict_da.value != decision.strict_da.value or row.witness.level.value != decision.witness.level.value:
            raise ValueError(f"pane5 adjudication D/A or W mismatch: {report_id}")
        if [item.model_dump(mode="json") for item in row.relation_rows] != [item.model_dump(mode="json") for item in decision.relations]:
            raise ValueError(f"pane5 adjudication relation mismatch: {report_id}")
        if row.reason != decision.reason or row.basis != decision.basis:
            raise ValueError(f"pane5 adjudication reason/basis mismatch: {report_id}")
        if row.reference_visible is not False or row.primary_visible is not False:
            raise ValueError(f"pane5 adjudication was not blind before unblinding: {report_id}")
        review = decision.review
        for field_name in ("confirmed_at", "independent_submission_at", "primary_submission_at", "unblinded_at", "blind_event_sequence"):
            if getattr(row, field_name) != getattr(review, field_name):
                raise ValueError(f"pane5 blind event closure mismatch: {report_id}/{field_name}")

    authorization_path = directory / "human_supervised_authorization.json"
    authorization = load_object(authorization_path)
    stored_authorization_hash = authorization.get("authorization_file_sha256")
    unsigned_authorization = dict(authorization)
    unsigned_authorization.pop("authorization_file_sha256", None)
    if stored_authorization_hash != canonical_json_sha256(unsigned_authorization):
        raise ValueError("human authorization file hash is not reproducible")
    authorization_hash = canonical_json_sha256(authorization)
    for decision in decisions:
        review = decision.review
        if review.authorization_message_sha256 != authorization_hash:
            raise ValueError(f"decision authorization hash mismatch: {decision.report_id}")
        if review.authorization_reference != authorization.get("authorization_reference"):
            raise ValueError(f"decision authorization reference mismatch: {decision.report_id}")



def validate_manifest(directory: Path, inventory: RawInventory) -> None:
    """Validate the machine-readable manifest's listed file hashes."""

    from paper_stm_evaluation.manual_adjudication import ManualAdjudicationManifest

    manifest = ManualAdjudicationManifest.model_validate(load_object(directory / "MANIFEST"))
    if manifest.report_counts != inventory.reports:
        raise ValueError("manual manifest report counts do not match raw inventory")
    for relative_path, expected_hash in inventory.source_manifests.items():
        if manifest.raw_input_hashes.get(relative_path) != expected_hash:
            raise ValueError(f"MANIFEST omits or changes source manifest hash: {relative_path}")
        source_path = (directory.parent.parent / relative_path).resolve()
        if not source_path.is_file() or sha256_file(source_path) != expected_hash:
            raise ValueError(f"MANIFEST source input hash mismatch: {relative_path}")
    required_canonical = set(REQUIRED_FILES) - {"MANIFEST"}
    if not required_canonical.issubset(manifest.canonical_files):
        missing = sorted(required_canonical - set(manifest.canonical_files))
        raise ValueError(f"MANIFEST omits canonical files: {missing}")
    for relative_path, expected_hash in manifest.canonical_files.items():
        path = (directory / relative_path).resolve()
        try:
            path.relative_to(directory.resolve())
        except ValueError as exc:
            raise ValueError(f"MANIFEST path escapes audit directory: {relative_path}") from exc
        if not path.is_file() or sha256_file(path) != expected_hash:
            raise ValueError(f"MANIFEST hash mismatch: {relative_path}")


def validate_directory(directory: Path) -> dict[str, int]:
    """Validate complete human finality and exact raw/report closure."""

    inventory = RawInventory.model_validate(load_object(directory / "inventory.json"))
    expected_counts = {"v60_current": 1271, "x1v2_baseline": 512}
    if inventory.reports != expected_counts:
        raise ValueError(f"raw inventory counts do not match the declared frozen universe: {inventory.reports}")
    validate_raw_inventory(directory, inventory)
    raw_index = {
        item.report_id: item.model_dump(mode="json")
        for item in inventory.items
    }
    ledger = load_object(directory.parent.parent / "reference" / "ledger.json")
    ledger_items = ledger.get("items")
    if not isinstance(ledger_items, dict) or not ledger_items:
        raise ValueError("reference ledger items are missing")
    expected_ids = tuple(sorted(str(key) for key in ledger_items))
    missing = [name for name in REQUIRED_FILES if not (directory / name).is_file()]
    if missing:
        raise ValueError(
            "manual adjudication is incomplete; missing canonical files: "
            + ", ".join(missing)
            + ". No human final labels may be inferred from legacy Judge output."
        )
    sets: dict[str, ReportDecisionSet] = {}
    for name, side in (("v60_report_decisions.json", "v60_current"), ("x1v2_report_decisions.json", "x1v2_baseline")):
        decision_set = ReportDecisionSet.model_validate(load_object(directory / name))
        if decision_set.side.value != side:
            raise ValueError(f"wrong side in {name}")
        side_index = {key: value for key, value in raw_index.items() if value["side"] == side}
        validate_decision_set(decision_set.decisions, expected_ids=expected_ids, raw_report_index=side_index)
        validate_tsv_mirror(directory / ("v60_report_decisions.tsv" if side == "v60_current" else "x1v2_report_decisions.tsv"), decision_set.decisions)
        validate_w2_witnesses(directory.parent.parent, list(decision_set.decisions))
        sets[side] = decision_set
    all_decisions = list(sets["v60_current"].decisions) + list(sets["x1v2_baseline"].decisions)
    validate_human_process_files(directory, inventory, all_decisions, expected_ids)
    validate_structured_supporting_files(directory, all_decisions, expected_ids)
    groups = GroupDecisionSet.model_validate(load_object(directory / "group_decisions.json"))
    validate_group_decisions(groups.groups, all_decisions)
    validate_source_refs(directory.parent.parent, all_decisions, list(groups.groups))
    relations = RelationAuditSet.model_validate(load_object(directory / "relation_decisions.json"))
    decision_by_id = {
        decision.report_id: decision
        for decision_set in sets.values()
        for decision in decision_set.decisions
    }
    nested_relations = {
        (decision.report_id, relation.expected_id): relation
        for decision_set in sets.values()
        for decision in decision_set.decisions
        for relation in decision.relations
    }
    relation_keys = {(row.report_id, row.expected_id) for row in relations.rows}
    if len(relations.rows) != len(relation_keys) or relation_keys != set(nested_relations):
        raise ValueError("relation_decisions.json is not a complete dense relation projection")
    for row in relations.rows:
        nested = nested_relations.get((row.report_id, row.expected_id))
        decision = decision_by_id.get(row.report_id)
        if (
            nested is None
            or decision is None
            or row.side != decision.side
            or row.pair_id != decision.pair_id
            or row.round != decision.round
            or row.relation != nested.relation
            or row.reason != nested.reason
            or row.basis != nested.basis
            or row.source_refs != nested.source_refs
            or row.report_owned_field_refs != nested.report_owned_field_refs
        ):
            raise ValueError(f"relation projection differs from report decision: {row.report_id}/{row.expected_id}")
    validate_manifest(directory, inventory)
    return {side: len(value.decisions) for side, value in sets.items()}


def main() -> None:
    """Run validation for a completed manual adjudication directory."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    counts = validate_directory(args.directory.resolve())
    print(json.dumps({"status": "PASS", "decision_counts": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
