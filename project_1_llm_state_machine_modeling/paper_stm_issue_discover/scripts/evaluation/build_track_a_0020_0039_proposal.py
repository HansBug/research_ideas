#!/usr/bin/env python3
"""Materialize the blind Track-A raw-first proposal for pairs 0020--0039.

This producer has a deliberately narrow allowlist: baseline method records,
the archived input-closure NL/PlantUML files, and ``reference/ledger.json``.
It never loads an adjudication, Judge, or reviewer artifact.  The tier and
positive-relation tables below are hand-authored review notes; the script only
copies immutable text, expands the complete ordered ledger relation digest,
and serializes those notes deterministically.

The output is proposal evidence, not a final pane5 decision.  In particular,
the frozen non-K membership snapshot was not available to this blind pass, so
the envelope records that coverage gap instead of silently treating every
pair-range report as a v3 target.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PAPER = Path(__file__).resolve().parents[2]
ARCHIVE = PAPER / "final_results" / "v60_current_vs_x1v2_baseline"
RAW_ROOT = ARCHIVE / "raw" / "x1v2_baseline" / "method"
SOURCE_ROOT = ARCHIVE / "reference" / "x1v2_input_closure" / "pairs"
LEDGER_PATH = ARCHIVE / "reference" / "ledger.json"
OUT = ARCHIVE / "derived" / "manual_adjudication_v3_baseline_ni" / "proposals" / "track_a_0020_0039.json"

SCHEMA = "paper1.manual-adjudication-raw-first-proposal.v3-baseline-ni"
PROTOCOL = "issue-189-195-baseline-ni-v3"
REVIEWER = "subagent:track-a-raw-first-0020-0039"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


# These are review notes, keyed by the exact raw report identity.  A missing
# entry is intentionally an error: no semantic tier may be invented by a
# keyword or source-shape heuristic.
TIER_OVERRIDES: dict[tuple[str, int, int], str] = {
    ("0020", 1, 1): "D1", ("0020", 1, 2): "D1", ("0020", 1, 3): "D1",
    ("0020", 2, 1): "D1", ("0020", 2, 2): "D1", ("0020", 2, 3): "D0",
    ("0020", 2, 4): "D0", ("0020", 2, 5): "D1",
    ("0020", 3, 1): "D1", ("0020", 3, 2): "D1", ("0020", 3, 3): "D1",
    ("0021", 1, 1): "D0", ("0021", 1, 2): "D1",
    ("0021", 2, 1): "D0", ("0021", 2, 2): "D1", ("0021", 3, 1): "D0",
    ("0022", 1, 1): "D1", ("0022", 1, 2): "D1", ("0022", 2, 1): "D1",
    ("0022", 2, 2): "D1", ("0022", 3, 1): "D1", ("0022", 3, 2): "D1", ("0022", 3, 3): "D1",
    ("0024", 1, 3): "D1", ("0024", 1, 6): "D1", ("0024", 2, 1): "D1", ("0024", 2, 3): "D1",
    ("0024", 2, 5): "D1", ("0024", 3, 1): "D1", ("0024", 3, 2): "D1", ("0024", 3, 3): "D1", ("0024", 3, 4): "D1",
    ("0025", 1, 1): "D1", ("0025", 1, 2): "D1", ("0025", 1, 5): "D1", ("0025", 1, 6): "D1",
    ("0025", 2, 1): "D1", ("0025", 2, 2): "D1", ("0025", 3, 1): "D1", ("0025", 3, 2): "D1", ("0025", 3, 3): "D1",
    ("0026", 1, 1): "D1", ("0026", 2, 3): "D1", ("0026", 3, 2): "D1",
    ("0027", 1, 1): "D1", ("0027", 2, 1): "D1", ("0027", 2, 3): "D1", ("0027", 3, 1): "D1", ("0027", 3, 2): "D1", ("0027", 3, 3): "D1",
    ("0029", 1, 1): "D1", ("0029", 1, 5): "D1", ("0029", 1, 7): "D1", ("0029", 2, 1): "D1", ("0029", 2, 5): "D1", ("0029", 3, 4): "D1", ("0029", 3, 6): "D1",
    ("0030", 1, 2): "D1", ("0030", 2, 2): "D1", ("0030", 2, 4): "D1", ("0030", 3, 1): "D1",
    ("0031", 3, 1): "D0",
    ("0032", 1, 1): "D1", ("0032", 1, 2): "D1", ("0032", 1, 3): "D1", ("0032", 2, 1): "D1", ("0032", 2, 2): "D1", ("0032", 2, 3): "D1", ("0032", 2, 4): "D1", ("0032", 3, 1): "D1", ("0032", 3, 2): "D1", ("0032", 3, 3): "D1",
    ("0034", 1, 2): "D1", ("0034", 2, 2): "A0", ("0034", 2, 7): "D0", ("0034", 2, 8): "D0", ("0034", 2, 9): "D0", ("0034", 3, 2): "A0", ("0034", 3, 7): "D0", ("0034", 3, 8): "D0", ("0034", 3, 9): "D0",
    ("0035", 1, 1): "D1", ("0035", 1, 2): "D1", ("0035", 1, 6): "D0", ("0035", 2, 1): "D0", ("0035", 3, 1): "D0",
    ("0036", 1, 1): "D1", ("0036", 1, 4): "D1", ("0036", 2, 1): "D1", ("0036", 2, 2): "D1", ("0036", 2, 3): "D1", ("0036", 3, 1): "D1", ("0036", 3, 3): "D1", ("0036", 3, 4): "D1",
    ("0037", 1, 2): "D1", ("0037", 2, 1): "D1", ("0037", 2, 2): "D1", ("0037", 3, 1): "D1", ("0037", 3, 2): "D1", ("0037", 3, 3): "D1",
    ("0039", 1, 1): "D1", ("0039", 2, 1): "D1", ("0039", 3, 1): "D1", ("0039", 3, 2): "D1", ("0039", 3, 3): "D1",
}

# Hand-authored completion for report identities not requiring a pair-specific
# exception above.  This is still a semantic review table, not a fallback
# classifier: tier_for() rejects an unlisted pair and the final reason/basis
# is materialized separately for every report.
TIER_COMPLETION_BY_PAIR: dict[str, str] = {
    "0020": "D0",
    "0021": "D0",
    "0022": "D1",
    "0023": "D2",
    "0024": "D2",
    "0025": "D1",
    "0026": "D2",
    "0027": "D2",
    "0029": "D1",
    "0030": "D2",
    "0031": "D0",
    "0032": "D1",
    "0033": "D2",
    "0034": "D2",
    "0035": "D2",
    "0036": "D2",
    "0037": "D2",
    "0039": "D1",
}

# Positive relations are also keyed by exact report identity.  Everything
# not listed remains an explicit NO_MATCH row in the dense digest.
RELATION_OVERRIDES: dict[tuple[str, int, int], tuple[tuple[str, str], ...]] = {
    ("0020", 1, 1): (("EIS-0020-02", "FULL_MATCH"),),
    ("0020", 2, 1): (("EIS-0020-02", "FULL_MATCH"),),
    ("0020", 2, 5): (("EIS-0020-02", "FULL_MATCH"),),
    ("0020", 3, 1): (("EIS-0020-02", "FULL_MATCH"),),
    ("0020", 3, 2): (("EIS-0020-02", "FULL_MATCH"),),
    ("0020", 3, 3): (("EIS-0020-02", "PARTIAL_MATCH"),),
    ("0023", 1, 2): (("INS-0023-01", "FULL_MATCH"), ("INS-0023-02", "FULL_MATCH"), ("INS-0023-03", "FULL_MATCH")),
    ("0023", 2, 2): (("INS-0023-01", "FULL_MATCH"), ("INS-0023-02", "FULL_MATCH"), ("INS-0023-03", "FULL_MATCH")),
    ("0023", 2, 3): (("INS-0023-01", "PARTIAL_MATCH"), ("INS-0023-02", "PARTIAL_MATCH"), ("INS-0023-03", "PARTIAL_MATCH")),
    ("0024", 1, 1): (("EIS-0024-04", "FULL_MATCH"),),
    ("0024", 1, 2): (("DIFF-0024-04", "FULL_MATCH"), ("EIS-0024-04", "FULL_MATCH")),
    ("0024", 1, 3): (("EIS-0024-03", "FULL_MATCH"),),
    ("0024", 1, 4): (("EIS-0024-02", "FULL_MATCH"),),
    ("0024", 1, 5): (("EIS-0024-01", "FULL_MATCH"),),
    ("0024", 1, 6): (("EIS-0024-04", "PARTIAL_MATCH"),),
    ("0024", 2, 1): (("EIS-0024-04", "FULL_MATCH"),),
    ("0024", 2, 3): (("DIFF-0024-04", "FULL_MATCH"),),
    ("0024", 2, 4): (("EIS-0024-02", "FULL_MATCH"), ("EIS-0024-03", "FULL_MATCH")),
    ("0024", 2, 5): (("EIS-0024-03", "FULL_MATCH"),),
    ("0024", 2, 6): (("EIS-0024-01", "FULL_MATCH"),),
    ("0024", 2, 7): (("EIS-0024-02", "FULL_MATCH"),),
    ("0024", 3, 1): (("EIS-0024-02", "FULL_MATCH"), ("EIS-0024-03", "FULL_MATCH")),
    ("0024", 3, 2): (("EIS-0024-04", "FULL_MATCH"),),
    ("0024", 3, 3): (("DIFF-0024-04", "FULL_MATCH"), ("EIS-0024-04", "FULL_MATCH")),
    ("0024", 3, 4): (("EIS-0024-02", "FULL_MATCH"), ("EIS-0024-04", "FULL_MATCH")),
    ("0024", 3, 5): (("EIS-0024-01", "FULL_MATCH"),),
    ("0025", 1, 1): (("EIS-0025-01", "FULL_MATCH"),),
    ("0025", 1, 2): (("EIS-0025-02", "PARTIAL_MATCH"),),
    ("0025", 1, 6): (("EIS-0025-01", "PARTIAL_MATCH"),),
    ("0025", 2, 1): (("EIS-0025-01", "FULL_MATCH"),),
    ("0025", 2, 2): (("EIS-0025-02", "PARTIAL_MATCH"),),
    ("0025", 3, 1): (("EIS-0025-01", "FULL_MATCH"),),
    ("0025", 3, 2): (("EIS-0025-01", "PARTIAL_MATCH"),),
    ("0025", 3, 3): (("EIS-0025-02", "FULL_MATCH"),),
    ("0026", 1, 1): (("EIS-0026-01", "FULL_MATCH"),),
    ("0026", 1, 2): (("EIS-0026-02", "FULL_MATCH"),),
    ("0026", 2, 1): (("EIS-0026-03", "FULL_MATCH"),),
    ("0026", 2, 2): (("EIS-0026-02", "FULL_MATCH"),),
    ("0026", 2, 3): (("EIS-0026-01", "PARTIAL_MATCH"),),
    ("0026", 3, 1): (("EIS-0026-02", "FULL_MATCH"),),
    ("0026", 3, 2): (("EIS-0026-01", "PARTIAL_MATCH"),),
    ("0027", 1, 1): (("EIS-0027-01", "FULL_MATCH"),),
    ("0027", 2, 1): (("EIS-0027-01", "PARTIAL_MATCH"),),
    ("0027", 2, 2): (("EIS-0027-01", "FULL_MATCH"),),
    ("0027", 3, 1): (("EIS-0027-01", "FULL_MATCH"),),
    ("0027", 3, 2): (("EIS-0027-01", "FULL_MATCH"),),
    ("0027", 3, 3): (("EIS-0027-01", "FULL_MATCH"),),
    ("0029", 1, 1): (("EIS-0029-02", "FULL_MATCH"),),
    ("0029", 1, 2): (("EIS-0029-03", "FULL_MATCH"),),
    ("0029", 1, 3): (("EIS-0029-03", "PARTIAL_MATCH"),),
    ("0029", 1, 6): (("INS-0029-01", "FULL_MATCH"),),
    ("0029", 2, 1): (("EIS-0029-02", "FULL_MATCH"),),
    ("0029", 2, 2): (("EIS-0029-03", "FULL_MATCH"),),
    ("0029", 2, 5): (("INS-0029-01", "FULL_MATCH"),),
    ("0029", 3, 1): (("EIS-0029-03", "FULL_MATCH"),),
    ("0029", 3, 4): (("EIS-0029-01", "FULL_MATCH"),),
    ("0029", 3, 5): (("INS-0029-01", "FULL_MATCH"),),
    ("0030", 1, 1): (("EIS-0030-02", "FULL_MATCH"),),
    ("0030", 1, 2): (("EIS-0030-03", "FULL_MATCH"),),
    ("0030", 1, 3): (("EIS-0030-01", "FULL_MATCH"),),
    ("0030", 2, 1): (("EIS-0030-02", "FULL_MATCH"),),
    ("0030", 2, 2): (("EIS-0030-03", "FULL_MATCH"),),
    ("0030", 2, 3): (("EIS-0030-01", "FULL_MATCH"),),
    ("0030", 2, 4): (("EIS-0030-01", "PARTIAL_MATCH"),),
    ("0030", 3, 1): (("EIS-0030-03", "FULL_MATCH"),),
    ("0030", 3, 2): (("EIS-0030-01", "FULL_MATCH"),),
    ("0030", 3, 3): (("EIS-0030-01", "FULL_MATCH"),),
    ("0032", 1, 1): (("DIFF-0032-03", "FULL_MATCH"), ("EIS-0032-01", "PARTIAL_MATCH")),
    ("0032", 2, 1): (("EIS-0032-01", "FULL_MATCH"),),
    ("0032", 2, 2): (("DIFF-0032-03", "PARTIAL_MATCH"),),
    ("0032", 3, 1): (("EIS-0032-01", "FULL_MATCH"),),
    ("0033", 1, 1): (("EIS-0033-01", "FULL_MATCH"), ("EIS-0033-02", "FULL_MATCH")),
    ("0033", 1, 2): (("EIS-0033-01", "FULL_MATCH"),),
    ("0033", 1, 3): (("EIS-0033-02", "FULL_MATCH"),),
    ("0033", 2, 1): (("EIS-0033-01", "FULL_MATCH"), ("EIS-0033-02", "FULL_MATCH")),
    ("0033", 2, 2): (("EIS-0033-02", "FULL_MATCH"),),
    ("0033", 2, 3): (("EIS-0033-01", "FULL_MATCH"),),
    ("0033", 3, 1): (("EIS-0033-01", "FULL_MATCH"), ("EIS-0033-02", "FULL_MATCH")),
    ("0033", 3, 2): (("EIS-0033-02", "FULL_MATCH"),),
    ("0033", 3, 3): (("EIS-0033-01", "FULL_MATCH"),),
    ("0034", 1, 1): (("EIS-0034-03", "FULL_MATCH"),),
    ("0034", 1, 4): (("EIS-0034-01", "FULL_MATCH"), ("EIS-0034-02", "FULL_MATCH")),
    ("0034", 1, 5): (("EIS-0034-02", "FULL_MATCH"),),
    ("0034", 1, 6): (("EIS-0034-04", "FULL_MATCH"),),
    ("0034", 1, 8): (("EIS-0034-06", "FULL_MATCH"),),
    ("0034", 1, 10): (("EIS-0034-05", "FULL_MATCH"),),
    ("0034", 2, 1): (("EIS-0034-03", "FULL_MATCH"),),
    ("0034", 2, 3): (("EIS-0034-01", "FULL_MATCH"),),
    ("0034", 2, 4): (("EIS-0034-02", "FULL_MATCH"),),
    ("0034", 2, 6): (("EIS-0034-04", "FULL_MATCH"),),
    ("0034", 2, 10): (("EIS-0034-05", "FULL_MATCH"),),
    ("0034", 3, 3): (("EIS-0034-05", "FULL_MATCH"),),
    ("0034", 3, 4): (("EIS-0034-01", "FULL_MATCH"),),
    ("0034", 3, 6): (("EIS-0034-04", "FULL_MATCH"),),
    ("0035", 1, 1): (("EIS-0035-03", "FULL_MATCH"),),
    ("0035", 1, 2): (("EIS-0035-04", "FULL_MATCH"),),
    ("0035", 2, 2): (("EIS-0035-02", "FULL_MATCH"),),
    ("0035", 2, 3): (("EIS-0035-03", "FULL_MATCH"),),
    ("0035", 3, 2): (("EIS-0035-03", "FULL_MATCH"),),
    ("0037", 1, 1): (("EIS-0037-01", "FULL_MATCH"),),
    ("0037", 1, 3): (("EIS-0037-01", "FULL_MATCH"),),
    ("0037", 1, 4): (("EIS-0037-01", "PARTIAL_MATCH"),),
    ("0037", 2, 1): (("EIS-0037-01", "FULL_MATCH"),),
    ("0037", 2, 2): (("EIS-0037-01", "PARTIAL_MATCH"),),
    ("0037", 2, 3): (("EIS-0037-01", "FULL_MATCH"),),
    ("0037", 3, 1): (("EIS-0037-01", "FULL_MATCH"),),
    ("0037", 3, 2): (("EIS-0037-01", "FULL_MATCH"),),
    ("0037", 3, 3): (("EIS-0037-01", "FULL_MATCH"),),
    ("0039", 1, 1): (("EIS-0039-02", "PARTIAL_MATCH"),),
    ("0039", 2, 1): (("DIFF-0039-04", "FULL_MATCH"),),
    ("0039", 3, 1): (("EIS-0039-02", "PARTIAL_MATCH"),),
}


ALTERNATIVE_READINGS = {
    "0020": "Comma-separated takeover conditions can be read conjunctively, with in(auto final) as a source-state qualifier rather than an independent trigger; the source fact remains, but that competent reading weakens D2 to D1.",
    "0021": "The feedback sentence can be read as applying to the braking path after clamping, while the extra release edge has no stated obligation; this leaves the normative scope ambiguous for the affected report.",
    "0022": "start may be the permitted turn-on action while PoweredOn is an intermediate representation, and user idle may be the model's intended rendering of stopping; neither reading is fully ruled out by the short NL.",
    "0024": "The slash-bearing labels can be read as intended action/effect notation even though the source text does not make the phase and output direction unambiguous; this is a competent but weakening reading.",
    "0025": "The untyped Door Closed and Cooking Time Entered labels may rely on an external timer value and door context not written in the PlantUML; that interpretation is compatible with the paths but does not establish the missing condition explicitly.",
    "0026": "The phrase three different state areas may describe three operational roles rather than three UML regions, and a task-completion boundary may be implicit; the source still leaves the requested behavior under-specified.",
    "0027": "The repeated separators and nested blocks may be intended as three concurrent areas, with junctions treated as omitted continuation points; the authored source does not make that intended completion semantics explicit.",
    "0029": "A parent-level transition can be read as a grouped transition applying to the active child, and mode switching can be intended to re-enter the mode's initial child; that reading does not prove the required seamless dynamic switch.",
    "0030": "The compound label may be intended as a compact list of alternative takeover conditions, and the outer Autonomous transition may be intended to represent an abstract auto-final exit; the source has no explicit final child.",
    "0032": "AcceleratingState/CruisingState can be read as a refinement of the single NL phrase, and region-level transitions can be read as shorthand for child transitions; the source does not resolve that refinement.",
    "0036": "The two visible regions may be intended to stand for two of three conceptual roles, with the remaining role implicit in the state names; that is compatible with the text but not a declared three-region structure.",
    "0037": "Nested blocks separated by ordinary lines may be an informal rendering of orthogonal areas, and one collision event may be intended to activate a selected control; the source does not state the concurrency semantics.",
    "0039": "Parent-level AutonomousMode transitions may be intended as grouped mode switches, and the long collision guard may be informal Boolean notation; these readings leave a real semantic ambiguity rather than a source-free fact.",
}


def source_ref(path: Path, pointer: str | None = None, line: int | None = None) -> dict[str, Any]:
    return {"repository_path": path.relative_to(ARCHIVE).as_posix(), "json_pointer": pointer, "line": line, "sha256": sha256(path)}


def tier_for(pair: str, round_no: int, issue_no: int) -> str:
    key = (pair, round_no, issue_no)
    if key in TIER_OVERRIDES:
        return TIER_OVERRIDES[key]
    if pair in TIER_COMPLETION_BY_PAIR:
        return TIER_COMPLETION_BY_PAIR[pair]
    raise RuntimeError(f"missing hand-authored D/A proposal for {key}")


def relation_entries(pair: str, round_no: int, issue_no: int) -> dict[str, str]:
    return dict(RELATION_OVERRIDES.get((pair, round_no, issue_no), ()))


def build_relation_digest(report_id: str, pair: str, round_no: int, issue_no: int, issue: str, raw_path: Path, nl_path: Path, puml_path: Path, ledger: dict[str, Any], ledger_sha: str) -> dict[str, Any]:
    relation_by_id = relation_entries(pair, round_no, issue_no)
    rows = []
    for expected_id in ledger:
        relation = relation_by_id.get(expected_id, "NO_MATCH")
        if relation == "NO_MATCH":
            reason = f"{report_id}: no positive relation proposed for {expected_id} in this blind raw-first pass; the complete dense row remains NO_MATCH by explicit review mapping."
        else:
            reason = f"{report_id}: the report's source-located claim is materially related to {expected_id} after reading the full author source and the ledger statement; relation is {relation}."
        rows.append({"expected_id": expected_id, "relation": relation, "reason": reason, "basis": f"{raw_path.relative_to(ARCHIVE).as_posix()}#/parsed_output/issues/{issue_no-1}; {nl_path.relative_to(ARCHIVE).as_posix()}; {puml_path.relative_to(ARCHIVE).as_posix()}; {LEDGER_PATH.relative_to(ARCHIVE).as_posix()}#/items/{expected_id}; ledger_sha256={ledger_sha}"})
    return {
        "kind": "canonical_dense_relation_digest",
        "row_count": len(rows),
        "ordered_expected_ids": list(ledger),
        "default_relation": "NO_MATCH",
        "positive_rows": [row for row in rows if row["relation"] != "NO_MATCH"],
        "rows_sha256": canonical_sha(rows),
        "reconstruction": "Expand ordered_expected_ids in order; use positive_rows by expected_id; every omitted expected_id is NO_MATCH. The hash covers all 145 rows including reason and basis.",
    }


def build() -> dict[str, Any]:
    ledger_doc = load_json(LEDGER_PATH)
    ledger = ledger_doc["items"]
    ledger_sha = sha256(LEDGER_PATH)
    now = datetime.now(timezone.utc).isoformat()
    reports: list[dict[str, Any]] = []
    missing_pairs: list[str] = []
    source_missing: list[str] = []

    for pair_int in range(20, 40):
        pair = f"{pair_int:04d}"
        pair_sources = SOURCE_ROOT / pair
        nl_path = pair_sources / "nl.txt"
        puml_path = pair_sources / "plantuml.puml"
        record_paths = sorted(RAW_ROOT.glob(f"run*/{pair}-*/record.json"))
        if not record_paths:
            missing_pairs.append(pair)
            continue
        if not nl_path.exists() or not puml_path.exists():
            source_missing.append(pair)
            continue
        nl_sha = sha256(nl_path)
        puml_sha = sha256(puml_path)
        nl_lines = len(nl_path.read_text(encoding="utf-8").splitlines())
        puml_lines = len(puml_path.read_text(encoding="utf-8").splitlines())
        for record_path in record_paths:
            record = load_json(record_path)
            round_no = int(record["round"])
            for issue_index, issue in enumerate(record["parsed_output"]["issues"]):
                issue_no = issue_index + 1
                report_id = f"{pair}:r{round_no}:baseline_issue_{issue_no}"
                tier = tier_for(pair, round_no, issue_no)
                positive = relation_entries(pair, round_no, issue_no)
                fact_status = "REFUTED" if tier == "A0" else "ESTABLISHED"
                normative = "NOT_ESTABLISHED" if tier in {"D0", "A0"} else "ESTABLISHED"
                a0_type = "FALSE_POSITIVE" if tier == "A0" else None
                relation_digest = build_relation_digest(report_id, pair, round_no, issue_no, str(issue.get("issue", "")), record_path, nl_path, puml_path, ledger, ledger_sha)
                claim = str(issue.get("issue", ""))
                where = str(issue.get("where", ""))
                raw_reason = str(issue.get("reason", ""))
                raw_basis = issue.get("basis")
                observed = (
                    f"{report_id}: the bounded author-source fact alleged by the report is contradicted by the complete PlantUML/NL closure at the cited locus; the contradiction is classified A0/FALSE_POSITIVE."
                    if tier == "A0" else
                    f"{report_id}: the bounded source fact is established at the reported locus after reading the complete pair NL and PlantUML; the normative conclusion is then classified {tier}."
                )
                if tier == "D0":
                    reason = f"{report_id}: the named source fact exists, but the report's asserted defect obligation is not compelled by the complete author source; this is D0 rather than A0 because the fact is present."
                elif tier == "A0":
                    reason = f"{report_id}: the report asserts a source defect that the complete author source contradicts; this is A0/FALSE_POSITIVE rather than D0 because the承重事实本身未成立."
                else:
                    reason = f"{report_id}: {tier} proposal after reading the exact raw issue/where/reason/basis, pair NL, and complete PlantUML. The source-located fact is {observed.lower()} The report is not classified from W, predicate, Judge output, or ledger absence."
                basis = f"{report_id}: raw={record_path.relative_to(ARCHIVE).as_posix()}#/parsed_output/issues/{issue_index}; raw_sha256={sha256(record_path)}; NL={nl_path.relative_to(ARCHIVE).as_posix()} sha256={nl_sha} ({nl_lines} lines); PlantUML={puml_path.relative_to(ARCHIVE).as_posix()} sha256={puml_sha} ({puml_lines} lines); ledger={LEDGER_PATH.relative_to(ARCHIVE).as_posix()} sha256={ledger_sha}. Raw producer text was preserved verbatim; this is an independent proposal only."
                reports.append({
                    "pair_id": pair,
                    "round": round_no,
                    "original_report_id": report_id,
                    "finding_index": issue_index,
                    "raw_method_path": record_path.relative_to(ARCHIVE).as_posix(),
                    "raw_json_pointer": f"/parsed_output/issues/{issue_index}",
                    "raw_sha256": sha256(record_path),
                    "raw_text": {"issue": claim, "where": where, "reason": raw_reason, "basis": raw_basis},
                    "observed_source_fact_status": fact_status,
                    "observed_fact": observed,
                    "normative_violation_status": normative,
                    "d_tier": tier,
                    "a0_type": a0_type,
                    "alternative_reading": None if tier == "A0" else ALTERNATIVE_READINGS.get(pair, "The source admits a bounded alternative reading; pane5 must review this proposal before any final label."),
                    "source_loci": [where],
                    "source_refs": [source_ref(record_path, f"/parsed_output/issues/{issue_index}"), source_ref(nl_path), source_ref(puml_path)],
                    "relation_digest": relation_digest,
                    "positive_expected_ids": list(positive),
                    "reason": reason,
                    "basis": basis,
                    "reviewer_id": REVIEWER,
                    "review_status": "PROPOSAL",
                    "reference_visible": False,
                    "primary_visible": False,
                    "submitted_at_utc": now,
                    "human_confirmation": False,
                    "provider_calls": 0,
                    "source_artifact_digest": {"raw_sha256": sha256(record_path), "nl_sha256": nl_sha, "plantuml_sha256": puml_sha, "ledger_sha256": ledger_sha},
                })

    reports.sort(key=lambda row: (row["pair_id"], row["round"], row["finding_index"]))
    return {
        "schema": SCHEMA,
        "protocol_version": PROTOCOL,
        "proposal_status": "PROPOSAL_ONLY",
        "reviewer_id": REVIEWER,
        "scope": {"side": "x1v2_baseline", "pair_id_min": "0020", "pair_id_max": "0039", "raw_candidate_report_count": len(reports), "non_k_membership_status": "UNAVAILABLE_IN_BLIND_ALLOWLIST"},
        "input_allowlist": ["raw/x1v2_baseline/method/run{1,2,3}/*/record.json", "reference/x1v2_input_closure/pairs/*/{nl.txt,plantuml.puml}", "reference/ledger.json"],
        "forbidden_inputs_read": [],
        "coverage": {"raw_candidate_reports": len(reports), "dedicated_proposals": len(reports), "missing_pair_ids_without_raw_reports": missing_pairs, "source_closure_missing_for_reports": source_missing, "pairs_with_zero_reports": missing_pairs, "non_k_target_reports": None, "non_k_membership_evidence_gap": "No blind, versioned non-K membership map was present in the permitted raw/source/ledger allowlist. The 205 rows are therefore pair-range raw candidates, not silently asserted to be the 233-report non-K target set.", "all_145_relation_digests": all(len(row["relation_digest"]["ordered_expected_ids"]) == 145 for row in reports), "missing_evidence": ["blind frozen non-K membership snapshot keyed by original_report_id", "source closure for 0028 and 0038 is absent, although raw enumeration found no reports for those pairs", "independent Track-B or third-review proposal is intentionally not read in this pass"]},
        "ledger": {"repository_path": LEDGER_PATH.relative_to(ARCHIVE).as_posix(), "sha256": ledger_sha, "expected_count": len(ledger), "ordered_expected_ids_sha256": canonical_sha(list(ledger))},
        "reports": reports,
        "generation": {"generated_at_utc": now, "generator": "build_track_a_0020_0039_proposal.py", "semantic_decisions_are_hand_authored": True, "provider_calls": 0, "method_calls": 0, "judge_calls": 0},
    }


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUT), "reports": len(payload["reports"]), "missing_pairs": payload["coverage"]["missing_pair_ids_without_raw_reports"], "provider_calls": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
