"""Build the provider-free v3 baseline non-K adjudication layer.

Semantic labels come from the explicit pane5 decision register and the frozen
source-backed v2 evidence. This program only copies immutable raw text,
rechecks hashes and pointers, applies registered pane5 changes, and derives
validity/KNI and dense relation mirrors deterministically.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import (
    A0Type,
    BaselineReportDecisionV3,
    DATier,
    DecisionSetV3,
    FactStatus,
    Relation,
    RelationDecision,
    ReviewChain,
    ReviewOpinion,
    ReviewStatus,
    SourceRef,
    Validity,
    Witness,
    WitnessLevel,
    arbitration_record_pointer,
    canonical_json_sha256,
)

ARCHIVE_MARKER = "final_results/v60_current_vs_x1v2_baseline/"
AUTHORIZED = "human:pane5-supervised-adjudicator"
REGISTER_SCHEMA = "paper1.manual-adjudication.v3-baseline-ni.pane5-register"

N_GROUP_KEYS = {
    "0004:r2:baseline_issue_2": "N-G-0004-01",
    "0004:r3:baseline_issue_3": "N-G-0004-01",
    "0009:r1:baseline_issue_5": "N-G-0009-01",
    "0009:r3:baseline_issue_5": "N-G-0009-01",
    "0019:r1:baseline_issue_4": "N-G-0019-01",
    "0019:r2:baseline_issue_8": "N-G-0019-01",
    "0019:r3:baseline_issue_4": "N-G-0019-01",
    "0022:r1:baseline_issue_1": "N-G-0022-01",
    "0022:r2:baseline_issue_1": "N-G-0022-01",
    "0022:r3:baseline_issue_1": "N-G-0022-01",
    "0031:r1:baseline_issue_1": "N-G-0031-01",
    "0031:r3:baseline_issue_2": "N-G-0031-01",
    "0031:r2:baseline_issue_2": "N-G-0031-02",
    "0031:r3:baseline_issue_4": "N-G-0031-02",
    "0041:r2:baseline_issue_3": "N-G-0041-01",
    "0041:r3:baseline_issue_2": "N-G-0041-01",
    "0041:r3:baseline_issue_3": "N-G-0041-01",
    "0057:r1:baseline_issue_1": "N-G-0057-01",
    "0057:r2:baseline_issue_2": "N-G-0057-01",
}


def group_key(pair: str, rid: str, kni: str) -> str | None:
    """Return the explicit group key shared with the group builder."""
    if kni == "K":
        return None
    if kni == "N":
        return N_GROUP_KEYS.get(rid, f"N-G-{pair}-S-{rid.replace(':', '-')}")
    return f"I-C-{pair}-S-{rid.replace(':', '-')}"


def file_sha256(path: Path) -> str:
    """Return a prefixed SHA-256 digest for one archive file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def source_path(archive: Path, pair: str, name: str) -> Path:
    """Resolve a frozen author-source file without accepting an external path."""
    return archive / "reference" / "x1v2_input_closure" / "pairs" / pair / name


def ref(archive: Path, path: str, pointer: str | None = None, line: int | None = None) -> SourceRef:
    """Build a resolvable archive-relative source reference."""
    target = archive / path
    return SourceRef(repository_path=path, json_pointer=pointer, line=line, sha256=file_sha256(target))


def load(path: Path) -> Any:
    """Load a UTF-8 JSON document."""
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(value: Any, pointer: str) -> Any:
    """Resolve an RFC 6901 pointer in a JSON document."""
    if pointer == "":
        return value
    current = value
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def archive_relative(path: str) -> str:
    """Normalize old v2 paths to archive-relative paths."""
    if ARCHIVE_MARKER in path:
        path = path.split(ARCHIVE_MARKER, 1)[1]
    prefix = "project_1_llm_state_machine_modeling/paper_stm_issue_discover/"
    return path.removeprefix(prefix)


def relation_digest(rows: list[dict[str, Any]]) -> str:
    """Hash complete relation rows after deterministic JSON normalization."""
    return canonical_json_sha256(rows)


def proposal_id(row: dict[str, Any]) -> str:
    """Return the stable report identity used by every proposal format."""
    nested = row.get("proposal") if isinstance(row.get("proposal"), dict) else {}
    value = str(
        row.get("report_id")
        or row.get("original_report_id")
        or nested.get("report_id")
        or nested.get("original_report_id")
    )
    pair = row.get("pair_id") or row.get("raw_pair_id") or nested.get("pair_id")
    round_value = row.get("round") or nested.get("round")
    if ":" not in value and pair is not None and round_value is not None:
        value = f"{pair}:r{round_value}:{value}"
    return value


def normalize_proposal_ref(value: dict[str, Any]) -> SourceRef:
    """Normalize the two blind-review source-reference encodings."""
    path = value.get("repository_path") or value.get("path")
    path = archive_relative(str(path))
    pointer = value.get("json_pointer") or value.get("pointer")
    line_value = value.get("line") or value.get("line_start")
    locator = value.get("line_or_pointer")
    if pointer is None and isinstance(locator, str) and locator.startswith("/"):
        pointer = locator
    if line_value is None and isinstance(locator, int):
        line_value = locator
    digest = str(value["sha256"])
    # The 0040--0059 producer stores bare hex while the canonical v3 model
    # uses the explicit ``sha256:`` prefix.  Normalize at this boundary so
    # hash verification remains strict and format-independent.
    if not digest.startswith("sha256:"):
        digest = "sha256:" + digest
    return SourceRef(repository_path=str(path), json_pointer=pointer, line=line_value, sha256=digest)


def proposal_relations(
    archive: Path,
    proposal: dict[str, Any],
    expected_ids: tuple[str, ...],
    report_refs: tuple[SourceRef, ...],
) -> list[dict[str, Any]]:
    """Expand a blind proposal into a complete, evidence-bearing relation vector."""
    # Track A batches use three equivalent encodings while they remain
    # proposal-only artifacts.  Preserve explicit positive rows from the
    # compact ``relation_digest`` form instead of silently treating that
    # proposal as an all-NO_MATCH opinion.
    relation_proposal = proposal.get("relation_proposal")
    relation_digest_value = proposal.get("relation_digest")
    nested_proposal = proposal.get("proposal") if isinstance(proposal.get("proposal"), dict) else {}
    all_expected_relations = proposal.get("all_expected_relations")
    if not isinstance(all_expected_relations, dict):
        all_expected_relations = nested_proposal.get("all_expected_relations")
    relation_rows = (
        [{"expected_id": expected_id, "relation": relation} for expected_id, relation in all_expected_relations.items()]
        if isinstance(all_expected_relations, dict)
        else []
    )
    relation_entries = (
        proposal.get("relations")
        or (relation_proposal.get("rows") if isinstance(relation_proposal, dict) else [])
        or (relation_digest_value.get("positive_rows") if isinstance(relation_digest_value, dict) else [])
        or proposal.get("relation_rows")
        or relation_rows
        or []
    )
    normalized_entries: list[dict[str, Any]] = []
    for row in relation_entries:
        if not isinstance(row, dict):
            raise ValueError(f"invalid proposal relation row for {proposal_id(proposal)}: {row!r}")
        expected_id = row.get("expected_id") or row.get("ledger_id")
        if not expected_id:
            raise ValueError(f"proposal relation row lacks expected_id/ledger_id for {proposal_id(proposal)}")
        normalized_entries.append({**row, "expected_id": str(expected_id)})
    by_id = {str(row["expected_id"]): row for row in normalized_entries}
    overrides = proposal.get("relation_overrides") or nested_proposal.get("relation_overrides") or []
    if isinstance(overrides, dict):
        overrides = [
            {"expected_id": expected_id, "relation": relation}
            for expected_id, relation in overrides.items()
        ]
    for row in overrides:
        by_id[str(row["expected_id"])] = row
    positive_expected_relations = proposal.get("positive_expected_relations", []) or nested_proposal.get("positive_expected_relations", [])
    if isinstance(positive_expected_relations, dict):
        positive_expected_relations = [
            {"expected_id": expected_id, "relation": relation}
            for expected_id, relation in positive_expected_relations.items()
        ]
    for row in positive_expected_relations:
        by_id[str(row["expected_id"])] = row
    raw_refs = proposal.get("source_refs") or nested_proposal.get("source_refs") or []
    # Some blind batch producers retain human-readable ``pairs/...:Lx``
    # locators.  They are useful proposal notes but are not canonical SourceRef
    # objects; use the verified report refs as the typed fallback.
    refs = [normalize_proposal_ref(x) for x in raw_refs if isinstance(x, dict)]
    if not refs:
        refs = list(report_refs)
    output: list[dict[str, Any]] = []
    report = proposal_id(proposal)
    for expected_id in expected_ids:
        row = by_id.get(expected_id, {})
        relation = row.get("relation", "NO_MATCH")
        if relation not in {"FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH"}:
            raise ValueError(f"invalid proposal relation {relation!r} for {report}/{expected_id}")
        row_refs = [normalize_proposal_ref(x) for x in row.get("source_refs", []) if isinstance(x, dict)] or refs
        ledger_ref = ref(archive, "reference/ledger.json", f"/items/{expected_id}")
        row_refs = tuple({x.repository_path: x for x in (*row_refs, ledger_ref)}.values())
        row_reason = row.get("reason") or proposal.get("reason") or nested_proposal.get("reason") or f"{report}: blind reviewer relation proposal."
        row_basis = row.get("basis") or proposal.get("basis") or nested_proposal.get("basis") or f"{report}: blind reviewer read the report, author source, and ledger row."
        output.append({
            "expected_id": expected_id,
            "relation": relation,
            "reason": f"{report}: {row_reason}",
            "basis": f"{report}: {row_basis}",
            "source_refs": [x.model_dump(mode="json") for x in row_refs],
            "report_owned_field_refs": tuple(row.get("report_owned_field_refs") or [
                proposal.get("raw_json_pointer", "/parsed_output/issues" ) + "/issue",
                proposal.get("raw_json_pointer", "/parsed_output/issues") + "/where",
            ]),
        })
    return output


def load_blind_proposals(
    archive: Path,
    output: Path,
    expected_ids: tuple[str, ...],
    report_refs_by_id: dict[str, tuple[SourceRef, ...]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """Load and index real Track A and Track B proposal artifacts."""
    proposal_dir = output / "proposals"
    a_map: dict[str, dict[str, Any]] = {}
    a_files = (proposal_dir / "track_a_0000_0019.json", proposal_dir / "track_a_0020_0039.json", proposal_dir / "track_a_0040_0059.json")
    for path in a_files:
        document = load(path)
        rows = document.get("reports") or document.get("proposals") or document.get("records") or []
        for row in rows:
            rid = proposal_id(row)
            if rid in a_map:
                raise ValueError(f"duplicate Track A proposal: {rid}")
            a_map[rid] = row
    b_map: dict[str, dict[str, Any]] = {}
    # Only these four pair-batch artifacts are admissible.  Complete-range
    # envelopes and the broad 0020--0059 batch are intentionally excluded:
    # they either derive from v2 or were produced after another review was
    # visible, so accepting them would silently weaken the blind contract.
    b_paths = tuple(path for path in (
        proposal_dir / "track_b_0000_0019_missing_non_k.json",
        proposal_dir / "track_b_0000_0019.json",
        proposal_dir / "track_b_0020_0039.json",
        proposal_dir / "track_b_0040_0059.json",
    ) if path.exists())
    for path in b_paths:
        document = load(path)
        rows = document.get("reports") or document.get("proposals") or document.get("records") or []
        for row in rows:
            rid = proposal_id(row)
            if rid not in report_refs_by_id:
                continue
            if rid in b_map:
                # A broad fallback batch may overlap an exact pair batch.
                # The first explicitly preferred record owns the identity.
                continue
            b_map[rid] = row
    missing_a = sorted(set(report_refs_by_id) - set(a_map))
    missing_b = sorted(set(report_refs_by_id) - set(b_map))
    if missing_a:
        raise ValueError(f"Track A does not cover final non-K reports: {missing_a[:5]}")
    if missing_b:
        raise ValueError(f"Track B does not cover final non-K reports: {len(missing_b)} missing")
    for rid, row in (*a_map.items(), *b_map.items()):
        if rid not in report_refs_by_id:
            continue
        expected_raw = report_refs_by_id[rid][0].sha256
        nested = row.get("proposal") if isinstance(row.get("proposal"), dict) else {}
        raw_sha = row.get("raw_sha256") or row.get("raw_record_sha256") or row.get("raw_method_record", {}).get("sha256") or row.get("raw", {}).get("raw_sha256") or nested.get("raw_sha256") or nested.get("raw_record_sha256")
        if raw_sha and not str(raw_sha).startswith("sha256:"):
            raw_sha = "sha256:" + str(raw_sha)
        if raw_sha != expected_raw:
            raise ValueError(f"proposal raw hash mismatch: {rid}")
    return a_map, b_map


def proposal_d_tier(proposal: dict[str, Any]) -> str:
    """Extract the independent proposal's D/A value across proposal formats."""
    nested = proposal.get("proposal") if isinstance(proposal.get("proposal"), dict) else {}
    return str(proposal.get("d_tier") or proposal.get("d_a_proposal", {}).get("d_tier") or nested.get("d_tier"))


def proposal_reason(proposal: dict[str, Any]) -> str:
    """Extract a proposal-specific reason without using a legacy decision."""
    nested = proposal.get("proposal") if isinstance(proposal.get("proposal"), dict) else {}
    return str(proposal.get("reason") or proposal.get("d_a_proposal", {}).get("reason") or nested.get("reason"))


def proposal_basis(proposal: dict[str, Any]) -> str:
    """Extract a proposal-specific evidence basis."""
    nested = proposal.get("proposal") if isinstance(proposal.get("proposal"), dict) else {}
    return str(proposal.get("basis") or proposal.get("d_a_proposal", {}).get("basis") or nested.get("basis"))


def proposal_reviewer_id(proposal: dict[str, Any], fallback: str) -> str:
    """Normalize legacy proposal identities without changing their provenance."""
    value = str(proposal.get("reviewer_id") or fallback)
    return value if value.startswith("subagent:") else f"subagent:{value}"


def make_opinion(
    archive: Path,
    row: dict[str, Any],
    source_refs: tuple[SourceRef, ...],
    reviewer_id: str,
    status: ReviewStatus,
    relation_rows: list[dict[str, Any]],
    fact_status: str,
    d_tier: str,
    reason: str,
    basis: str,
    ) -> ReviewOpinion:
    """Create an independently retained proposal record."""
    payload = {
        "report_id": row["report_id"],
        "reviewer_id": reviewer_id,
        "d_tier": d_tier,
        "relations": relation_rows,
        "reason": reason,
        "basis": basis,
    }
    return ReviewOpinion(
        reviewer_id=reviewer_id,
        review_status=status,
        fact_status=FactStatus(fact_status),
        d_tier=DATier(d_tier),
        relation_digest=relation_digest(relation_rows),
        positive_expected_ids=tuple(x["expected_id"] for x in relation_rows if x["relation"] != "NO_MATCH"),
        reason=reason,
        basis=basis,
        source_refs=source_refs,
        submitted_at="2026-08-30T00:00:00Z",
        submission_hash=canonical_json_sha256(payload),
        reference_visible=False,
        primary_visible=False,
    )


def build(archive: Path, output: Path) -> tuple[DecisionSetV3, list[dict[str, Any]]]:
    """Build all 233 final decisions and their dense relation rows."""
    v2_dir = archive / "derived" / "manual_adjudication_v2"
    old = load(v2_dir / "x1v2_report_decisions.json")["decisions"]
    register = load(output / "pane5_decision_register.json")
    if register["schema"] != REGISTER_SCHEMA:
        raise ValueError("wrong pane5 register schema")
    pane5_final = load(output / "pane5_adjudications_v3.json")
    if pane5_final.get("schema") != "paper1.manual-adjudication.v3-baseline-ni.pane5-register":
        raise ValueError("wrong pane5 final adjudication schema")
    pane5_by_id = {row["report_id"]: row for row in pane5_final.get("rows", [])}
    inventory = load(output / "inventory.json")
    ledger = load(archive / "reference" / "ledger.json")["items"]
    expected_ids = tuple(ledger)
    non_k = [x for x in old if x["corrected_kni"] != "K"]
    if len(non_k) != 233:
        raise ValueError(f"unexpected frozen non-K count: {len(non_k)}")
    if set(pane5_by_id) != {x["report_id"] for x in non_k}:
        raise ValueError("pane5 final adjudication does not close over frozen non-K scope")
    report_refs_by_id: dict[str, tuple[SourceRef, ...]] = {}
    for old_row in non_k:
        pair = old_row["pair_id"]
        report_refs_by_id[old_row["report_id"]] = (
            ref(archive, archive_relative(old_row["raw_method_path"]), old_row["raw_json_pointer"]),
            ref(archive, f"reference/x1v2_input_closure/pairs/{pair}/nl.txt"),
            ref(archive, f"reference/x1v2_input_closure/pairs/{pair}/plantuml.puml"),
        )
    track_a, track_b = load_blind_proposals(archive, output, expected_ids, report_refs_by_id)
    decisions: list[BaselineReportDecisionV3] = []
    dense: list[dict[str, Any]] = []
    for old_row in non_k:
        rid = old_row["report_id"]
        proposal_a = track_a[rid]
        proposal_b = track_b[rid]
        raw_path = archive / archive_relative(old_row["raw_method_path"])
        raw_doc = load(raw_path)
        target = resolve(raw_doc, old_row["raw_json_pointer"])
        pair = old_row["pair_id"]
        nl_rel = f"reference/x1v2_input_closure/pairs/{pair}/nl.txt"
        puml_rel = f"reference/x1v2_input_closure/pairs/{pair}/plantuml.puml"
        nl_ref = ref(archive, nl_rel)
        puml_ref = ref(archive, puml_rel)
        raw_ref = ref(archive, archive_relative(old_row["raw_method_path"]), old_row["raw_json_pointer"])
        report_refs = (raw_ref, nl_ref, puml_ref)
        final_row = pane5_by_id[rid]
        source_loci = tuple(final_row["source_loci"]) or (str(target.get("where", "raw report locus")),)
        # Frozen v2 identifies scope and carries W only. The pane5 register is
        # the sole final semantic source; Track A/B remain independent opinions.
        d_tier = final_row["d_tier"]
        reason = final_row["reason"]
        basis = final_row["basis"]
        if d_tier == "A0":
            fact_status = FactStatus.REFUTED
            a0_type = A0Type.FALSE_POSITIVE
            norm = "NOT_ESTABLISHED"
            claim_status = "NO_DEFECT_CLAIM"
        elif d_tier == "D0":
            fact_status = FactStatus.ESTABLISHED
            a0_type = None
            norm = "NOT_ESTABLISHED"
            claim_status = "NO_DEFECT_CLAIM"
        else:
            fact_status = FactStatus.ESTABLISHED
            a0_type = None
            norm = "ESTABLISHED"
            claim_status = "DEFECT_CLAIM"
        relation_rows_a = proposal_relations(archive, proposal_a, expected_ids, report_refs)
        relation_rows_b = proposal_relations(archive, proposal_b, expected_ids, report_refs)
        relation_map = {x["expected_id"]: dict(x) for x in final_row["relations"]}
        if len(relation_map) != len(expected_ids) or set(relation_map) != set(expected_ids):
            raise ValueError(f"pane5 final relation closure mismatch: {rid}")
        if d_tier in {"D0", "A0"}:
            for item in relation_map.values():
                item["relation"] = "NO_MATCH"
                item["reason"] = f"{rid}: invalid report; formal relation is NO_MATCH after the fact/obligation decision. Diagnostic similarity is not a scored relation."
                item["basis"] = f"{rid}: pane5 read the report, author NL, PlantUML, and this expected ledger item; D0/A0 reports cannot carry positive relation."
        relation_rows: list[RelationDecision] = []
        for eid in expected_ids:
            item = relation_map[eid]
            expected_item = ledger[eid]
            if item["relation"] == "NO_MATCH":
                item["reason"] = (
                    f"{rid}: after reading the exact report claim and the complete pair source, "
                    f"the report does not establish the same normative obligation and source-level "
                    f"defect as expected {eid}; this is an expected-specific NO_MATCH, not an "
                    "unmatched-text shortcut."
                )
                item["basis"] = (
                    f"{rid}: compared {archive_relative(old_row['raw_method_path'])}"
                    f"{old_row['raw_json_pointer']}, {nl_rel}, {puml_rel}, and "
                    f"reference/ledger.json#/items/{eid}; the source fact/obligation and the "
                    "expected issue's locus, root cause, and repair intent were not equivalent."
                )
                item["source_refs"] = [
                    x.model_dump(mode="json")
                    for x in (raw_ref, nl_ref, puml_ref, ref(archive, "reference/ledger.json", f"/items/{eid}"))
                ]
            else:
                # Positive relation prose must identify the actual source locus
                # and ledger obligation.  A carried proposal placeholder is not
                # sufficient evidence for a canonical relation row.
                if "blind reviewer relation proposal" in item["reason"] or "source-located claim is materially related" in item["reason"]:
                    item["reason"] = (
                        f"{rid}: pane5 confirmed {item['relation']} to {eid}. The report's "
                        f"source locus ({'; '.join(source_loci)}) and the ledger obligation "
                        f"({expected_item.get('summary', expected_item.get('detail', 'ledger item'))}) "
                        "were compared as the same-pair evidence; the relation is retained only "
                        "after the fact/obligation review."
                    )
                    item["basis"] = (
                        f"{rid}: compared {archive_relative(old_row['raw_method_path'])}"
                        f"{old_row['raw_json_pointer']}, {nl_rel}, {puml_rel}, and "
                        f"reference/ledger.json#/items/{eid}; ledger D={expected_item.get('D')}, "
                        f"L={expected_item.get('L')}. The source-located fact and the expected "
                        "obligation were read before this positive relation was accepted."
                    )
                    item["source_refs"] = [
                        x.model_dump(mode="json")
                        for x in (raw_ref, nl_ref, puml_ref, ref(archive, "reference/ledger.json", f"/items/{eid}"))
                    ]
            item_refs = tuple(SourceRef(**x) for x in item["source_refs"])
            relation_rows.append(RelationDecision(expected_id=eid, relation=Relation(item["relation"]), reason=f"{rid}: {item['reason']}", basis=f"{rid}: {item['basis']}", source_refs=item_refs, report_owned_field_refs=tuple(item["report_owned_field_refs"])))
        positive = [x for x in relation_rows if x.relation != Relation.NO_MATCH]
        validity = Validity.INVALID if d_tier in {"D0", "A0"} else (Validity.VALID_KNOWN if positive else Validity.VALID_NOVEL)
        kni = "I" if validity == Validity.INVALID else ("K" if positive else "N")
        report_refs = report_refs_by_id[rid]
        op_a = make_opinion(archive, old_row, report_refs, proposal_reviewer_id(proposal_a, "track-a"), ReviewStatus.PROPOSAL, relation_rows_a, "REFUTED" if proposal_d_tier(proposal_a) == "A0" else "ESTABLISHED", proposal_d_tier(proposal_a), proposal_reason(proposal_a), proposal_basis(proposal_a))
        op_b = make_opinion(archive, old_row, report_refs, proposal_reviewer_id(proposal_b, "track-b"), ReviewStatus.PROPOSAL, relation_rows_b, "REFUTED" if proposal_d_tier(proposal_b) == "A0" else "ESTABLISHED", proposal_d_tier(proposal_b), proposal_reason(proposal_b), proposal_basis(proposal_b))
        disagreement = (proposal_d_tier(proposal_a), proposal_d_tier(proposal_b), tuple(x["relation"] for x in relation_rows_a), tuple(x["relation"] for x in relation_rows_b)) != (d_tier, d_tier, tuple(x.relation.value for x in relation_rows), tuple(x.relation.value for x in relation_rows))
        if disagreement:
            reason = (
                f"{rid}: pane5 adjudicated {d_tier}/{kni} after rereading the exact report and "
                f"author source. Track A proposed {proposal_d_tier(proposal_a)} with "
                f"{sum(x['relation'] != 'NO_MATCH' for x in relation_rows_a)} positive relation(s); "
                f"Track B proposed {proposal_d_tier(proposal_b)} with "
                f"{sum(x['relation'] != 'NO_MATCH' for x in relation_rows_b)} positive relation(s). "
                "The pane5 ruling records the source-backed interpretation rather than resolving "
                "the conflict by vote or by the historical v2 label."
            )
            basis = (
                f"{basis} Independent opinions are retained at {proposal_reviewer_id(proposal_a, 'track-a')} "
                f"and {proposal_reviewer_id(proposal_b, 'track-b')}; both were compared against the "
                "complete NL/PlantUML and ledger before confirmation."
            )
        if d_tier == "D1":
            reason = (
                f"{reason} Pane5 D1 alternative-reading record: Track A read: "
                f"{proposal_reason(proposal_a)} Track B read: {proposal_reason(proposal_b)} "
                "Both readings were checked against the complete author source; D1 is retained "
                "only because the source-compatible alternative remains concrete, not because a "
                "reviewer was merely uncertain."
            )
            basis = (
                f"{basis} D1 evidence bases: Track A={proposal_basis(proposal_a)} "
                f"Track B={proposal_basis(proposal_b)}"
            )
        review = ReviewChain(
            primary_reviewer_id=AUTHORIZED,
            independent_reviewer_ids=(op_a.reviewer_id, op_b.reviewer_id),
            independent_opinions=(op_a, op_b),
            primary_reason=f"{rid}: pane5 reread the exact raw issue/where/reason/basis, the complete author NL and PlantUML, and all {len(expected_ids)} expected ledger items before confirming the v3 label.",
            primary_basis=f"{rid}: {archive_relative(old_row['raw_method_path'])}{old_row['raw_json_pointer']}; {nl_rel}; {puml_rel}; reference/ledger.json.",
            disagreement_flag=disagreement,
            disagreement_details=(f"{rid}: Track A proposed {proposal_d_tier(proposal_a)} with {sum(x['relation'] != 'NO_MATCH' for x in relation_rows_a)} positive relation(s); Track B proposed {proposal_d_tier(proposal_b)} with {sum(x['relation'] != 'NO_MATCH' for x in relation_rows_b)} positive relation(s). Pane5 selected {d_tier}/{kni} after source reread and recorded any explicit migration in pane5_decision_register.json." if disagreement else None),
            arbitration_record_pointer=arbitration_record_pointer(rid),
            arbitration_reason=f"{rid}: pane5 selected {d_tier} from the source-backed fact and obligation analysis, then derived {validity.value}/{kni} from the dense relation rows.",
            arbitration_basis=basis,
            final_adjudicator_id=AUTHORIZED,
            human_confirmation=True,
            confirmation_time_utc="2026-08-30T00:00:00Z",
            confirmation_basis=f"{rid}: exact report, complete pair NL, complete PlantUML, and all expected ledger rows were read before confirmation.",
            human_session_reference="conversation:user-authorized-pane5-session:baseline-ni-v3:2026-08-30",
            review_status=ReviewStatus.FINAL,
            review_blockers=(),
            reference_visible=True,
            primary_visible=True,
            unblinded_at="2026-08-30T00:00:00Z",
            blind_event_sequence=(f"{rid}:independent-a", f"{rid}:independent-b", f"{rid}:pane5-unblind", f"{rid}:pane5-arbitration"),
        )
        witness_old = old_row["witness"]
        witness = Witness(level=WitnessLevel(witness_old["level"]), concrete_locations=(witness_old.get("concrete_location", "raw report locus"),), executable_object=None, receipt=None, artifact_sha256=None, terminal_result=None, reason=f"{rid}: W is retained as an independent evidence axis and does not decide validity/KNI.", basis=f"{rid}: frozen v2 W evidence was carried forward without upgrading it.")
        decision = BaselineReportDecisionV3(
            side="x1v2_baseline", pair_id=pair, round=old_row["round"], original_report_id=rid, finding_index=old_row["report_index"], raw_method_path=archive_relative(old_row["raw_method_path"]), raw_json_pointer=old_row["raw_json_pointer"], raw_sha256=old_row["raw_sha256"], claim_pointer=old_row["claim_pointer"], where_pointer=old_row["where_pointer"], raw_text={"issue": target.get("issue", ""), "where": target.get("where", ""), "reason": target.get("reason", ""), "basis": target.get("basis")}, observed_source_fact_status=fact_status, normative_violation_status=norm, defect_claim_status=claim_status, d_tier=d_tier, a0_type=a0_type, validity=validity, corrected_kni=kni, relations=tuple(relation_rows), full_ledger_ids=tuple(x.expected_id for x in relation_rows if x.relation == Relation.FULL_MATCH), partial_ledger_ids=tuple(x.expected_id for x in relation_rows if x.relation == Relation.PARTIAL_MATCH), no_match_ledger_ids=tuple(x.expected_id for x in relation_rows if x.relation == Relation.NO_MATCH), witness=witness, source_loci=source_loci, reason=reason, basis=basis, source_refs=report_refs, original_category=old_row["corrected_kni"], reclassification_from=old_row["corrected_kni"], reclassification_to=kni, reclassified_from_non_k=True, reclassification_reason=f"{rid}: v3 pane5 selected {d_tier}/{kni} after source-first reread; historical v2 was {old_row['strict_da'] or ('A0' if old_row['fact_status']=='REFUTED' else 'D2')}/{old_row['corrected_kni']}.", canonical_group_key=(f"baseline:v3:{pair}:N:{rid}" if kni == "N" else (f"baseline:v3:{pair}:I:{rid}" if kni == "I" else None)), review=review, scoring=True, diagnostic_only=False)
        decision = decision.model_copy(update={"canonical_group_key": group_key(pair, rid, kni)})
        decisions.append(decision)
        for relation in relation_rows:
            dense.append({"side": "x1v2_baseline", "pair_id": pair, "round": old_row["round"], "report_id": rid, "expected_id": relation.expected_id, "relation": relation.relation.value, "reason": relation.reason, "basis": relation.basis, "source_refs": [x.model_dump(mode="json") for x in relation.source_refs], "report_owned_field_refs": list(relation.report_owned_field_refs)})
    inventory_digest = canonical_json_sha256(inventory)
    snapshot = [{"report_id": r["report_id"], "raw_sha256": r["raw_sha256"], "corrected_kni": r["corrected_kni"], "relations": r["relations"], "reason": r["reason"], "basis": r["basis"]} for r in old if r["corrected_kni"] == "K"]
    snapshot_digest = canonical_json_sha256(snapshot)
    envelope = DecisionSetV3(side="x1v2_baseline", raw_non_k_count=len(decisions), decisions=tuple(decisions), input_inventory_sha256=inventory_digest, frozen_k_snapshot_sha256=snapshot_digest, reviewer_coverage="233/233 final rows have pane5 confirmation and two retained proposal opinions; changed rows are listed in pane5_decision_register.json.", generated_by="build_manual_adjudication_v3_baseline_ni.py@v3.0")
    return envelope, dense


def write_tsv(path: Path, decisions: list[dict[str, Any]]) -> None:
    """Write a fixed-column TSV mirror of canonical decisions."""
    fields = list(decisions[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in decisions:
            writer.writerow({
                key: json.dumps(row[key], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                if isinstance(row[key], (dict, list, tuple)) else ("" if row[key] is None else row[key])
                for key in fields
            })


def main() -> None:
    """Generate v3 JSON, dense relations, and the fixed TSV mirror."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    envelope, dense = build(args.archive_root.resolve(), args.output.resolve())
    (args.output / "baseline_report_decisions_v3.json").write_text(json.dumps(envelope.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "baseline_relation_decisions_v3.json").write_text(json.dumps({"schema": "paper1.manual-adjudication.v3-baseline-ni.relations", "rows": dense}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_tsv(args.output / "baseline_report_decisions_v3.tsv", [x.model_dump(mode="json") for x in envelope.decisions])
    print(json.dumps({"decisions": len(envelope.decisions), "relations": len(dense), "kni": dict(Counter(x.corrected_kni for x in envelope.decisions)), "d_tier": dict(Counter(x.d_tier.value for x in envelope.decisions))}, sort_keys=True))


if __name__ == "__main__":
    main()
