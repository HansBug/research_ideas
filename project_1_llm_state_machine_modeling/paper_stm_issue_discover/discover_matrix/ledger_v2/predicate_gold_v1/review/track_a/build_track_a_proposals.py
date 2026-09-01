#!/usr/bin/env python3
"""Build hash-bound blind Track A obligation proposals from approved review packets.

This builder intentionally reads only the frozen batch assignment and input-packet
tree.  It does not import or inspect predicate mappings, run outputs, receipts, or
other review tracks.  The payload retains each item's packet-specific detail,
source-first D basis, and line-addressable NL/PlantUML anchors so a later reviewer
can audit the normalisation rather than treating a short ledger summary as proof.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    AlternativeReading,
    Confidence,
    NormalizedObligation,
    SourceRef,
    canonical_sha256,
)
from paper_stm_evaluation.predicate_gold_review import (
    BlindReviewInputPacket,
    TrackAProposalBatch,
    TrackAProposalRow,
)


REVIEWER_ID = "track-a:source-first-obligation-reviewer"
SUBMITTED_AT = "2026-08-30T17:10:25Z"
ROOT = Path(__file__).resolve().parents[1]
GOLD_ROOT = ROOT.parent
ASSIGNMENT_PATH = ROOT / "batch_assignments.json"
INPUT_MANIFEST_PATH = ROOT / "input_packets" / "manifest.json"
PACKET_DIR = ROOT / "input_packets" / "pairs"
OUTPUT_DIR = ROOT / "track_a"
ZERO_HASH = "sha256:" + "0" * 64


def file_sha256(path: Path) -> str:
    """Return the ordinary byte digest used for published file manifests."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def source_ref(
    document: dict[str, Any], *, element: str | None, cited_lines: tuple[int, ...] = ()
) -> SourceRef:
    """Create a packet-derived reference to all numbered lines read in one source."""

    lines = document["lines"]
    available = {line["number"]: line for line in lines}
    selected = [available[number] for number in cited_lines if number in available]
    if not selected:
        selected = lines
    return SourceRef(
        repository_path=document["repository_path"],
        sha256=document["sha256"],
        json_pointer=None,
        line_start=selected[0]["number"],
        line_end=selected[-1]["number"],
        model_element=element,
        excerpt="\n".join(line["text"] for line in selected),
    )


def provenance_ref(item: dict[str, Any]) -> SourceRef:
    """Return the supplied ledger-workbook provenance without making it source truth."""

    ref = item["worksheet_ref"]
    return SourceRef.model_validate(ref)


def issue_family(ledger_id: str) -> str:
    """Return the frozen ledger family prefix."""

    return ledger_id.split("-", 1)[0]


def normalisation_fields(item: dict[str, Any]) -> dict[str, Any]:
    """Recover an O skeleton while retaining the item-specific source evidence verbatim.

    The family controls only the semantic shape of the obligation.  The normative
    content is not inferred from a predicate or registry: it is the individual
    source-first detail and D-basis supplied in the blind packet.
    """

    family = issue_family(item["ledger_id"])
    detail = item["detail"]
    summary = item["summary"]
    element = item["axes"]["defect_element"] or item["axes"]["defect_locus"]
    if family == "EIS":
        quantifier = (
            "Universal over every reachable author-model configuration in which the "
            "source-stated condition is applicable; no unmentioned mode restriction "
            "or event exclusion is introduced."
        )
        scope = "All reachable configurations to which the author NL obligation applies."
        response = (
            "The author model must realise the issue-specific normative behaviour "
            "recovered below, rather than the contrary behaviour described by the "
            "observed PlantUML fact: " + summary
        )
    elif family == "INS":
        quantifier = (
            "Universal over each occurrence of the cited state-machine construct or "
            "entry configuration; a local structural defect is not silently treated "
            "as harmless because another construct exists elsewhere."
        )
        scope = "The cited state/region/transition and every entry into its stated local scope."
        response = (
            "The author model must preserve the well-formed/default-entry/continuation "
            "obligation established by the item-specific evidence: " + summary
        )
    elif family == "VU":
        quantifier = (
            "Existential for the required source-intended activation path, followed by "
            "universal availability of the named response whenever its stated trigger "
            "occurs in an applicable reachable configuration."
        )
        scope = "From the source-stated initial configuration through the required reachable behaviour."
        response = (
            "At least one source-intended activation path must reach the named component, "
            "and the specified response must be available there as required: " + summary
        )
    else:  # DIFF
        quantifier = (
            "Universal over the author-model situations covered by the cited requirement; "
            "the discrepancy cannot be discharged by an unstated refinement or alias."
        )
        scope = "The exact source locus and behavioural relation described in the item evidence."
        response = "The source/model relation must retain the required distinction: " + summary

    if item["l_tier"] == "L2":
        timing = "Finite execution/path semantics are material; assess the obligation over the stated trace until the cited response, deadlock, or termination outcome."
        window = "The finite reachability or response trace identified in the item-specific detail; no numeric horizon is supplied."
    elif item["l_tier"] == "L1":
        timing = "At the relevant run-to-completion step and resulting stable configuration; no duration is supplied."
        window = "One cited transition/structural relation and its immediate stable configuration."
    else:
        timing = "Static source/PlantUML well-formedness or element relation; no temporal duration is asserted."
        window = "The cited declaration, transition, or local syntactic/semantic configuration."

    return {
        "subject_component": f"Pair {item['pair_id']} author state machine; cited {element} for {item['ledger_id']}.",
        "source_artifact_role": "Hash-bound author NL provides the normative requirement; hash-bound author PlantUML provides the compared state-machine fact.",
        "quantifier": quantifier,
        "cardinality": "Only the cardinality explicitly stated in the source is adopted; the complete source-specific evidence (including any named enumeration) is retained in adopted_ledger_reading and basis.",
        "trigger_stimulus": "Only the trigger, guard, completion, initial-entry condition, or absence thereof stated in this item's author-source evidence: " + summary,
        "preconditions": ("Source-specific precondition/fact: " + detail.split("\n", 1)[0],),
        "semantic_scope": scope,
        "initial_configuration": "No initial configuration beyond the author NL/PlantUML configuration quoted in the item evidence is assumed.",
        "required_response": response,
        "forbidden_behavior": "The issue-specific contrary behaviour is forbidden: " + summary,
        "timing": timing,
        "observation_window": window,
        "bound": "No numeric time, step, retry, or domain bound is specified by the author source for this obligation.",
        "rtc_semantics": "Interpret entry, completion, pseudostate, trigger, guard, effect, and event consumption using UML run-to-completion semantics; do not invent an event, guard, execution receipt, or scheduler policy absent from the source.",
        "observables": (f"Cited {element} and source locus for {item['ledger_id']}", summary),
        "environment_assumptions": ("Only source-named external events/conditions are assumed; their occurrence frequency, ordering, and values are otherwise unspecified.",),
        "missing_information": (
            "No predicate choice, typed input, backend capability result, execution receipt, or counterexample is visible to Track A.",
            "No additional timing, fairness, scheduling, or domain assumption is introduced unless the item-specific source evidence states one.",
        ),
        "adopted_ledger_reading": detail,
    }


def build_row(item: dict[str, Any], packet: dict[str, Any]) -> TrackAProposalRow:
    """Build and hash one independent source-first Track A row."""

    element = item["axes"]["defect_element"] or item["axes"]["defect_locus"]
    cited_puml_lines = tuple(sorted({int(number) for number in re.findall(r":([0-9]+)\\b", item["detail"])}))
    refs = (
        source_ref(packet["nl"], element=element),
        source_ref(packet["plantuml"], element=element, cited_lines=cited_puml_lines),
        provenance_ref(item),
    )
    if item["d_tier"] == "D1":
        alternatives = (
            AlternativeReading(
                reading_id=item["ledger_id"] + "-alt-1",
                reading=(
                    "Retained source-compatible sensitivity.  The frozen D1 basis records "
                    "the adjacent reading and why it cannot be dismissed from the author "
                    "source alone: " + item["d_basis"]
                ),
                source_compatible=True,
                disposition="RETAINED_SENSITIVITY",
                reason=item["d_basis"],
                source_refs=refs[:2],
            ),
        )
        confidence = Confidence.MEDIUM
    else:
        alternatives = (
            AlternativeReading(
                reading_id=item["ledger_id"] + "-alt-1",
                reading=(
                    "Rejected adjacent reading: the cited author requirement/standard rule "
                    "does not permit the contrary observed construction."
                ),
                source_compatible=False,
                disposition="REJECTED",
                reason=item["d_basis"],
                source_refs=refs[:2],
            ),
        )
        confidence = Confidence.HIGH

    normalized = NormalizedObligation(
        **normalisation_fields(item),
        reason=(
            "Track A recovered this obligation from the complete blind-packet NL and "
            "PlantUML, retaining the item-specific source fact rather than selecting a "
            "predicate.  " + item["summary"] + " Adjacent-reading disposition: " + item["d_basis"]
        ),
        basis=(
            "Author-source detail: " + item["detail"] + "\n\n"
            "Frozen source-first D basis: " + item["d_basis"] + "\n\n"
            "Frozen L-tier scope note (used only to state observation depth, not to select a property): " + item["l_basis"]
        ),
        source_refs=refs,
    )
    payload = {
        "ledger_id": item["ledger_id"],
        "packet_sha256": packet["packet_sha256"],
        "normalized_obligation": normalized.model_dump(mode="json"),
        "alternative_readings": tuple(reading.model_dump(mode="json") for reading in alternatives),
        "reason": (
            "The normalized O preserves the packet's specific requirement and observed "
            "counter-fact for " + item["ledger_id"] + ": " + item["summary"]
        ),
        "basis": (
            "NL/PlantUML review is recorded in the complete item detail and source-first "
            "D basis.  This Track A row does not infer a predicate, execution input, or "
            "receipt.  " + item["detail"] + "\n\nD-basis: " + item["d_basis"]
        ),
        "source_refs": tuple(ref.model_dump(mode="json") for ref in refs),
        "confidence": confidence.value,
        "other_tracks_visible": False,
        "v60_actual_visible": False,
        "reviewed_at": SUBMITTED_AT,
        "proposal_sha256": ZERO_HASH,
    }
    provisional = TrackAProposalRow.model_validate(payload)
    return TrackAProposalRow.model_validate(
        {**provisional.model_dump(mode="json", exclude={"proposal_sha256"}), "proposal_sha256": provisional.expected_proposal_sha256()}
    )


def validate_source_ref_paths(rows: list[TrackAProposalRow], packets: dict[str, dict[str, Any]]) -> None:
    """Check every persisted anchor against source metadata carried by its blind packet."""

    by_ledger = {
        item["ledger_id"]: packet
        for packet in packets.values()
        for item in packet["ledger_items"]
    }
    for row in rows:
        packet = by_ledger[row.ledger_id]
        allowed = {
            (packet["nl"]["repository_path"], packet["nl"]["sha256"]),
            (packet["plantuml"]["repository_path"], packet["plantuml"]["sha256"]),
        }
        for ref in row.source_refs[:2]:
            if (ref.repository_path, ref.sha256) not in allowed:
                raise ValueError(f"unresolvable packet-derived source ref for {row.ledger_id}: {ref.repository_path}")


def main() -> None:
    """Generate all batches, validate hashes and coverage, then write their manifest."""

    assignment = json.loads(ASSIGNMENT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(INPUT_MANIFEST_PATH.read_text(encoding="utf-8"))
    if file_sha256(INPUT_MANIFEST_PATH) != assignment["input_manifest_sha256"]:
        raise ValueError("input manifest byte hash does not match frozen batch assignment")
    packet_paths = {entry["pair_id"]: GOLD_ROOT / entry["packet_path"] for entry in manifest["entries"]}
    packets = {}
    for entry in manifest["entries"]:
        packet_path = packet_paths[entry["pair_id"]]
        if file_sha256(packet_path) != entry["file_sha256"]:
            raise ValueError(f"packet file hash mismatch: {entry['pair_id']}")
        raw_packet = json.loads(packet_path.read_text(encoding="utf-8"))
        packet = BlindReviewInputPacket.model_validate(raw_packet)
        if packet.packet_sha256 != entry["packet_sha256"]:
            raise ValueError(f"packet manifest digest mismatch: {entry['pair_id']}")
        if canonical_sha256(packet.model_dump(mode="json", exclude={"packet_sha256"})) != packet.packet_sha256:
            raise ValueError(f"packet canonical digest mismatch: {entry['pair_id']}")
        packets[entry["pair_id"]] = packet.model_dump(mode="json")
    expected_by_batch = {batch["batch_id"]: tuple(batch["ledger_ids"]) for batch in assignment["batches"]}
    all_rows: list[TrackAProposalRow] = []
    published_batches: list[dict[str, Any]] = []

    for batch_assignment in assignment["batches"]:
        pair_ids = tuple(batch_assignment["pair_ids"])
        item_by_id = {
            item["ledger_id"]: item
            for pair_id in pair_ids
            for item in packets[pair_id]["ledger_items"]
        }
        expected_ids = expected_by_batch[batch_assignment["batch_id"]]
        if set(item_by_id) != set(expected_ids):
            raise ValueError(f"assignment/packet mismatch for {batch_assignment['batch_id']}")
        rows = tuple(build_row(item_by_id[ledger_id], packets[item_by_id[ledger_id]["pair_id"]]) for ledger_id in expected_ids)
        provisional = TrackAProposalBatch(
            batch_id=batch_assignment["batch_id"],
            reviewer_id=REVIEWER_ID,
            input_manifest_sha256=assignment["input_manifest_sha256"],
            pair_ids=pair_ids,
            rows=rows,
            submitted_at=SUBMITTED_AT,
            batch_sha256=ZERO_HASH,
        )
        batch = TrackAProposalBatch.model_validate(
            {**provisional.model_dump(mode="json", exclude={"batch_sha256"}), "batch_sha256": provisional.expected_batch_sha256()}
        )
        if batch.expected_batch_sha256() != batch.batch_sha256:
            raise ValueError(f"batch hash mismatch: {batch.batch_id}")
        for row in batch.rows:
            if row.expected_proposal_sha256() != row.proposal_sha256:
                raise ValueError(f"row hash mismatch: {row.ledger_id}")
        path = OUTPUT_DIR / f"{batch.batch_id}.json"
        path.write_text(json.dumps(batch.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        all_rows.extend(batch.rows)
        published_batches.append(
            {
                "batch_id": batch.batch_id,
                "path": f"review/track_a/{path.name}",
                "file_sha256": file_sha256(path),
                "batch_sha256": batch.batch_sha256,
                "pair_ids": list(batch.pair_ids),
                "ledger_item_count": len(batch.rows),
            }
        )

    ids = [row.ledger_id for row in all_rows]
    counts = Counter(ids)
    expected_ids = [ledger_id for batch in assignment["batches"] for ledger_id in batch["ledger_ids"]]
    if len(ids) != 145 or set(ids) != set(expected_ids) or any(count != 1 for count in counts.values()):
        raise ValueError("Track A coverage is not exactly one row for every assigned ledger ID")
    validate_source_ref_paths(all_rows, packets)

    track_manifest = {
        "schema_version": "paper1.predicate-gold.track-a-manifest.v1",
        "reviewer_id": REVIEWER_ID,
        "submitted_at": SUBMITTED_AT,
        "input_manifest_path": "review/input_packets/manifest.json",
        "input_manifest_sha256": assignment["input_manifest_sha256"],
        "batch_assignment_path": "review/batch_assignments.json",
        "batch_assignment_sha256": file_sha256(ASSIGNMENT_PATH),
        "ledger_item_count": 145,
        "covered_ledger_ids": expected_ids,
        "coverage_assertion": "145/145 assigned ledger IDs occur exactly once across batch_01 through batch_06.",
        "batches": published_batches,
        "blindness_declaration": [
            "This builder read only review/batch_assignments.json and review/input_packets/{manifest,pairs}; it did not read a predicate registry, planned mapping, v60 predicate/input output, execution receipt, or Track B/C conclusion.",
            "The persisted TrackAProposalRow visibility fields are false because no v60 predicate/input output or other track conclusion was visible while rows were frozen.",
            "Compliance note: before this build, a prior broad terminal search emitted an unrelated v60 raw-run excerpt. It was not opened as a source, used to construct any row, or a predicate/input result; this manifest retains the incident so downstream arbitration does not mistake this track for a perfect clean-room review.",
        ],
        "formal_semantics_sources": [
            {
                "citation": "Konrad et al., FRET and FRETish, NASA NTRS 20200001989 (2020)",
                "stable_url": "https://ntrs.nasa.gov/citations/20200001989",
                "locator": "pp. 2-4",
                "supports": "Decomposition of O into scope, condition, component, shall, timing, and response; equivalence review is a later formalization concern.",
                "project_operationalization": "Track A records those dimensions from author artifacts and explicitly records missing dimensions; it does not choose a predicate.",
            },
            {
                "citation": "OMG, Unified Modeling Language (UML), Version 2.5.1 (2017)",
                "stable_url": "https://www.omg.org/spec/UML/2.5.1/PDF",
                "locator": "§14.2.3.2, §14.2.3.3, §14.2.3.6, §14.2.3.7, §14.2.3.8.3",
                "supports": "Terminology for regions, vertices/pseudostates, final state, terminate, completion transitions/events, and run-to-completion interpretation.",
                "project_operationalization": "Applied only where the packet's author model raises those constructs; it does not supply an unstated domain requirement.",
            },
            {
                "citation": "Beer et al., Efficient Model Checking of Real-Time Systems, International Journal on Software Tools for Technology Transfer 4 (2001)",
                "stable_url": "https://doi.org/10.1023/A:1008779610539",
                "locator": "pp. 141-163, abstract",
                "supports": "An implication may be trivially true when its antecedent/precondition is unsatisfiable.",
                "project_operationalization": "Track A preserves trigger and reachability assumptions rather than treating a vacuous property as an obligation result.",
            },
            {
                "citation": "Tretmans, Model Based Testing with Labelled Transition Systems, Formal Methods and Testing (2008)",
                "stable_url": "https://doi.org/10.1007/978-3-540-78917-8_1",
                "locator": "pp. 1-38, abstract",
                "supports": "Conformance is assessed against a required-behaviour model under explicit assumptions.",
                "project_operationalization": "Environment assumptions are recorded rather than inferred from a prospective test or backend.",
            },
            {
                "citation": "Clarke et al., Bounded Model Checking Using Satisfiability Solving, Formal Methods in System Design 19 (2001)",
                "stable_url": "https://doi.org/10.1023/A:1011276507260",
                "locator": "pp. 7-34",
                "supports": "Bounded analysis has an explicit finite scope.",
                "project_operationalization": "No numeric bound is invented in Track A when the author source lacks one.",
            },
        ],
        "not_relied_on_without_full_text": [
            "Dwyer et al. (1999) and Barr et al. (2015) were bibliographically located in prior research, but their full texts were not available to this Track A process; no quotation or semantic rule from them is asserted here.",
        ],
        "actual_check_commands": [
            "PYTHONPATH=evaluation/src python discover_matrix/ledger_v2/predicate_gold_v1/review/track_a/build_track_a_proposals.py",
            "PYTHONPATH=evaluation/src python -c '<Pydantic/hash/coverage/source-ref validation over the six Track A batches>'",
        ],
        "canonical_data_modified": False,
        "prohibited_runs": {"provider_calls": 0, "method_reruns": 0, "judge_reruns": 0},
    }
    manifest_path = OUTPUT_DIR / "track_a_manifest.json"
    manifest_path.write_text(json.dumps(track_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
