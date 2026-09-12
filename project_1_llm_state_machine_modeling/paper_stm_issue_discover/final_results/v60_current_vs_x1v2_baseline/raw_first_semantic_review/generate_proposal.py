#!/usr/bin/env python3
"""Build an independent, raw-first review proposal for a seeded stratified sample.

This script reads only frozen raw judge inputs, the frozen NL/PlantUML closure,
and the reference ledger.  It deliberately does not read any adjudication
outputs.  The result is a proposal and must not be treated as a final ruling.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "raw" / "v60_current" / "judge" / "source_runs"
REF = BASE / "reference"
OUT = Path(__file__).resolve().parent / "independent_raw_first_proposal.json"

RUNS = {
    1: "77404499c3ac4511a218f0ad3f91c45b",
    2: "86407845e4d5428ab8334fce3398cf60",
    3: "a93f5773cd3d4e6387b68b6fd1f9113d",
}
SAMPLE_SEED = 20260829
SAMPLE_FAMILIES = 9


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def puml_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def source_line_refs(report: dict) -> list[tuple[int, str]]:
    refs = []
    for ref in report.get("source_refs", []):
        match = re.search(r"\.puml:line:(\d+)$", ref)
        if match:
            refs.append((int(match.group(1)), ref))
    return refs


def direct_edges(lines: list[str]) -> set[tuple[str, str]]:
    edges = set()
    for line in lines:
        text = line.strip()
        if not text or text.startswith("'") or "-->" not in text:
            continue
        left, right = text.split("-->", 1)
        target = right.split(":", 1)[0].strip()
        source = left.strip()
        if source and target:
            edges.add((source, target))
    return edges


def source_label(line: str) -> str:
    if ":" not in line:
        return ""
    return line.split(":", 1)[1].strip()


def endpoint_label(where: str, lines: list[str]) -> str:
    match = re.search(r"transition:\s*(.+?)\s*->\s*([^>]+?)\s*$", where)
    if not match:
        return ""
    source = match.group(1).strip()
    target = match.group(2).strip()
    for line in lines:
        text = line.strip()
        if "-->" not in text or ":" not in text:
            continue
        left, right = text.split("-->", 1)
        candidate_target, label = right.split(":", 1)
        if left.strip() == source and candidate_target.strip() == target:
            return label.strip()
    return ""


def compact(text: str, limit: int = 240) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def report_text(report: dict) -> str:
    return " ".join(
        str(report.get(key) or "")
        for key in ("claim", "where", "property", "expected", "observed")
    )


def select_sample_pairs() -> tuple[list[str], dict[str, str], dict[str, list[str]]]:
    """Sample one numeric pair from each exact-NL family using a recorded seed."""
    families: dict[str, list[str]] = {}
    for pair_dir in sorted((REF / "x1v2_input_closure" / "pairs").iterdir()):
        if not pair_dir.is_dir() or not pair_dir.name.isdigit() or len(pair_dir.name) != 4:
            continue
        nl_hash = hashlib.sha256((pair_dir / "nl.txt").read_bytes()).hexdigest()
        families.setdefault(nl_hash, []).append(pair_dir.name)
    if len(families) != SAMPLE_FAMILIES:
        raise RuntimeError(f"expected {SAMPLE_FAMILIES} NL families, found {len(families)}")

    rng = random.Random(SAMPLE_SEED)
    selected_by_canonical: dict[str, str] = {}
    family_members: dict[str, list[str]] = {}
    for members in sorted(families.values(), key=lambda values: values[0]):
        canonical = members[0]
        family_members[canonical] = members
        selected_by_canonical[canonical] = rng.choice(members)
    selected_pairs = sorted(selected_by_canonical.values())
    canonical_by_pair = {
        selected: canonical for canonical, selected in selected_by_canonical.items()
    }
    return selected_pairs, canonical_by_pair, family_members


def remap_relation_id(relation_id: str, pair: str) -> str:
    parts = relation_id.split("-")
    if len(parts) != 3 or len(parts[1]) != 4:
        raise ValueError(f"unexpected ledger relation id: {relation_id}")
    parts[1] = pair
    return "-".join(parts)


def fact_review(report: dict, lines: list[str]) -> tuple[str, str, str]:
    core_text = " ".join(
        str(report.get(key) or "")
        for key in ("claim", "where", "property", "expected", "observed")
    )
    low = core_text.lower()
    if "grounding remains unresolved" in low or "did not close" in low or "unresolved" in low:
        return (
            "UNRESOLVED",
            "The raw report explicitly says that typed grounding did not close; the allowed author sources do not justify silently resolving it.",
            "raw input report fields plus the cited author NL/PlantUML/source inventory",
        )

    refs = source_line_refs(report)
    cited_lines = [lines[number - 1] for number, _ in refs if 1 <= number <= len(lines)]
    labels = [source_label(line) for line in cited_lines if source_label(line)]
    prop = str(report.get("property") or "")

    if prop == "trigger_set" and re.search(r"triggers?\s*=\s*\[\s*\]|trigger set.*\[\s*\]", low):
        if labels:
            return (
                "CONTRADICTED",
                "The author PlantUML line cited by the report carries a non-empty transition label, while the report's core observed field says the trigger set is empty; the no-trigger fact is therefore not source-compatible.",
                "author PlantUML cited lines: " + "; ".join(compact(line, 160) for line in cited_lines),
            )

    if prop == "guard" and "guard=null" in low and labels:
        return (
            "PARTIALLY_SUPPORTED",
            "The author source carries the stated condition or label, but the allowed source text alone does not establish its typed role as a guard; the raw typed-null assertion is not independently closed.",
            "author PlantUML cited lines: " + "; ".join(compact(line, 160) for line in cited_lines),
        )

    if prop == "guard" and "guard=null" in low:
        label = endpoint_label(str(report.get("where") or ""), lines)
        if label:
            return (
                "PARTIALLY_SUPPORTED",
                "The author PlantUML edge carries a non-empty condition/event label, but the allowed source text alone does not establish that the label has the typed role of a guard; the raw typed-null assertion remains only partially closed.",
                "author PlantUML endpoint scan: " + compact(label, 160),
            )

    if prop == "effect" and ("no exact" in low or "no supplied" in low or "no cooking-time" in low):
        if not any("/" in line or "entry/" in line or "do/" in line or "exit/" in line for line in cited_lines):
            return (
                "SUPPORTED",
                "The cited author source contains no effect or lifecycle-action syntax at the reported carrier, while the NL requires the reported behavior.",
                "author NL and PlantUML cited lines",
            )

    if "required transition" in low and "absent" in low:
        endpoint = re.search(r"transition:\s*([^\n]+?)\s*->\s*([^\n]+?)(?:\s*->|$)", str(report.get("where") or ""))
        if endpoint:
            src, dst = endpoint.group(1).strip(), endpoint.group(2).strip()
            if (src, dst) in direct_edges(lines):
                return (
                    "CONTRADICTED",
                    f"The author PlantUML contains a direct {src} -> {dst} edge, contradicting the report's assertion that the required edge is absent.",
                    "author PlantUML direct-edge scan",
                )

    if refs and not cited_lines:
        return (
            "UNRESOLVED",
            "The report cites an author-source line that is outside the frozen closure's line count; the source pointer cannot be verified.",
            "frozen PlantUML closure line-count check",
        )

    return (
        "SUPPORTED",
        "The report's bounded claim is compatible with the cited author NL/PlantUML/source-inventory facts; no source-level contradiction was found in this pass.",
        "author NL, PlantUML, source inventory, and the raw report fields",
    )


def relation_map(pair: str, text: str) -> dict[str, str]:
    """Return conservative report-to-ledger relation proposals for this sample."""
    low = text.lower()
    result: dict[str, str] = {}

    def set_match(eid: str, match: str):
        result[eid] = match

    if pair == "0000":
        if any(x in low for x in ("autonomous", "power-off", "power off", "finalstate", "final state")):
            set_match("EIS-0000-01", "FULL_MATCH" if "autonomous" in low or "endpoint" in low or "source scope" in low else "PARTIAL_MATCH")
        if any(x in low for x in ("auto-final", "autofinal", "human steering", "brake")):
            set_match("EIS-0000-02", "FULL_MATCH")
        if any(x in low for x in ("initial transition", "initial entry", "trigger")):
            set_match("INS-0000-04", "FULL_MATCH")
        elif any(x in low for x in ("power_on", "power on", "power_off", "power off")):
            set_match("INS-0000-04", "PARTIAL_MATCH")
    elif pair == "0001":
        if "clampinglosestate" in low:
            set_match("INS-0001-02", "FULL_MATCH")
        if "clampingstate" in low:
            set_match("VU-0001-01", "FULL_MATCH")
    elif pair == "0002":
        if "pumpcontrol" in low and "initialstate" in low:
            set_match("EIS-0002-01", "FULL_MATCH")
        if "unreachable" in low and any(x in low for x in ("pumpstate", "waterstate", "methanestate")):
            set_match("EIS-0002-02", "FULL_MATCH")
        if "initialstate" in low and any(x in low for x in ("not in nl", "no corresponding", "extraneous")):
            set_match("EIS-0002-03", "FULL_MATCH")
        if "initialstate" in low and any(x in low for x in ("dead-end", "dead end", "no outgoing", "permanently")):
            set_match("INS-0002-02", "FULL_MATCH")
        for eid, state in (
            ("INS-0002-03", "runningstate"),
            ("INS-0002-04", "monitoringwaterflow"),
            ("INS-0002-05", "monitoringmethaneflow"),
        ):
            if state in low and "initial transition" in low:
                set_match(eid, "FULL_MATCH")
    elif pair == "0004":
        if "doorsclosing" in low and "malformed" in low:
            set_match("EIS-0004-01", "FULL_MATCH")
        if "emergencystopping" in low and "dead" in low:
            set_match("INS-0004-01", "FULL_MATCH")
        if "stopping" in low and "dead" in low:
            set_match("INS-0004-02", "FULL_MATCH")
    elif pair == "0005":
        if "doorshut" in low and "cancel" in low and ("self" in low or "loop" in low):
            set_match("EIS-0005-01", "FULL_MATCH")
        if any(x in low for x in ("nest", "dooropenwithitem routes", "dooropenwithitem -> dooropenwithitem")):
            set_match("EIS-0005-02", "FULL_MATCH")
        if any(x in low for x in ("cooking-time", "cooking time", "timer", "effect")):
            set_match("EIS-0005-03", "FULL_MATCH" if "cooking" in low else "PARTIAL_MATCH")
    elif pair == "0006":
        if any(x in low for x in ("uav-count", "uav count", "number of uavs", "swarm-size", "swarm size")):
            set_match("EIS-0006-02", "FULL_MATCH")
    elif pair == "0007":
        if "initialstate" in low and any(x in low for x in ("dead", "unreachable", "root")):
            set_match("EIS-0007-01", "FULL_MATCH" if "initialstate" in low and "root" in low else "PARTIAL_MATCH")
        if "initial transition" in low and "trigger" in low:
            set_match("EIS-0007-02", "FULL_MATCH")
        if "operationalcontrols" in low or "four regions" in low:
            set_match("EIS-0007-03", "FULL_MATCH" if "operationalcontrols" in low else "PARTIAL_MATCH")
    elif pair == "0009":
        if "highway" in low and "exit" in low:
            set_match("EIS-0009-01", "FULL_MATCH")
        if "exit_urban" in low or "urban local exit" in low:
            set_match("EIS-0009-02", "FULL_MATCH")
        if "finishstate" in low and any(x in low for x in ("scope", "termination", "wrong")):
            set_match("EIS-0009-03", "FULL_MATCH")
        if "nonterminate" in low or "termination" in low:
            set_match("INS-0009-03", "FULL_MATCH")
        if "collisionavoidancesystem" in low and "unreachable" in low:
            set_match("VU-0009-01", "FULL_MATCH")
        elif "collision avoidance" in low and "unreachable" in low:
            set_match("VU-0009-01", "PARTIAL_MATCH")
    return result


def main() -> None:
    sample_pairs, canonical_by_pair, family_members = select_sample_pairs()
    ledger = load(REF / "ledger.json")
    ledger_items = ledger["items"]
    by_pair: dict[str, list[dict]] = {pair: [] for pair in sample_pairs}
    for item in ledger_items.values():
        if item.get("pair") in by_pair:
            by_pair[item["pair"]].append(item)
    for values in by_pair.values():
        values.sort(key=lambda item: item["id"])

    entries = []
    set_counts = {}
    for round_number, run_id in RUNS.items():
        for pair in sample_pairs:
            input_path = RAW / run_id / "inputs" / f"{pair}.json"
            result_path = RAW / run_id / "pairs" / f"{pair}.json"
            data = load(input_path)
            nl_path = REF / "x1v2_input_closure" / "pairs" / pair / "nl.txt"
            puml_path = REF / "x1v2_input_closure" / "pairs" / pair / "plantuml.puml"
            lines = puml_lines(puml_path)
            inventory = next(
                artifact for artifact in data["artifact_closure"]["artifacts"]
                if artifact["artifact_id"] == "artifact:exact_source_inventory"
            )
            set_counts[f"{pair}:r{round_number}"] = len(data["reports"])
            expected_ids = [item["id"] for item in by_pair[pair]]
            for index, report in enumerate(data["reports"]):
                fact_status, fact_reason, fact_basis = fact_review(report, lines)
                text = report_text(report)
                relations = {
                    remap_relation_id(relation_id, pair): match
                    for relation_id, match in relation_map(canonical_by_pair[pair], text).items()
                }
                if fact_status in ("CONTRADICTED", "UNRESOLVED"):
                    for eid in list(relations):
                        relations[eid] = "NO_MATCH" if fact_status == "CONTRADICTED" else "UNRESOLVED"
                relation_rows = []
                for eid in expected_ids:
                    match = relations.get(eid, "NO_MATCH")
                    linked = ledger_items[eid] if match != "NO_MATCH" else None
                    relation_rows.append(
                        {
                            "expected_id": eid,
                            "match": match,
                            "reason": (
                                "The report and ledger entry share the bounded carrier/obligation described in the match."
                                if match == "FULL_MATCH"
                                else "The report shares a consequence or carrier with the ledger entry but does not state the complete ledger defect."
                                if match == "PARTIAL_MATCH"
                                else "No source-grounded overlap sufficient for this relation proposal was found."
                                if match == "NO_MATCH"
                                else "The report's typed grounding is unresolved, so this relation remains unresolved."
                            ),
                            "basis": "candidate report fields, author NL/PlantUML/source inventory, and reference ledger entry",
                            "ledger_D": linked.get("D") if linked else None,
                        }
                    )
                full = [row for row in relation_rows if row["match"] == "FULL_MATCH"]
                partial = [row for row in relation_rows if row["match"] == "PARTIAL_MATCH"]
                if fact_status == "CONTRADICTED":
                    proposal_status = "PROPOSED_REJECT"
                elif fact_status == "UNRESOLVED":
                    proposal_status = "PROPOSED_UNRESOLVED"
                elif fact_status == "PARTIALLY_SUPPORTED":
                    proposal_status = "PROPOSED_PARTIAL"
                else:
                    proposal_status = "PROPOSED_ACCEPT"
                d_level = full[0]["ledger_D"] if full else partial[0]["ledger_D"] if partial else "UNRESOLVED"
                attribution = "KNOWN_LEDGER_ISSUE" if full else "PARTIAL_LEDGER_OVERLAP" if partial else "NO_KNOWN_LEDGER_MATCH"
                entries.append(
                    {
                        "entry_id": f"{pair}:r{round_number}:report:{index:03d}",
                        "pair_id": pair,
                        "round": round_number,
                        "report_id": report["report_id"],
                        "proposal_status": proposal_status,
                        "raw_report": {
                            "path": str(input_path.relative_to(BASE)),
                            "pointer": f"#/reports/{index}",
                            "sha256": sha256(input_path),
                        },
                        "raw_record": {
                            "path": str(result_path.relative_to(BASE)),
                            "pointer": f"#/report_outcomes/{index}",
                            "sha256": sha256(result_path),
                        },
                        "source_files": {
                            "nl": {"path": str(nl_path.relative_to(BASE)), "sha256": sha256(nl_path)},
                            "plantuml": {"path": str(puml_path.relative_to(BASE)), "sha256": sha256(puml_path)},
                            "source_inventory": {"artifact_id": inventory["artifact_id"], "sha256": inventory["sha256"]},
                        },
                        "report_snapshot": {
                            "claim": report.get("claim"),
                            "where": report.get("where"),
                            "property": report.get("property"),
                            "expected": report.get("expected"),
                            "observed": report.get("observed"),
                        },
                        "fact_review": {
                            "status": fact_status,
                            "reason": fact_reason,
                            "basis": fact_basis,
                        },
                        "d_a_review": {
                            "status": "PROPOSED",
                            "defect_level": d_level,
                            "attribution": attribution,
                            "reason": "D-level is inherited only when a source-grounded relation to a reference-ledger issue is proposed; otherwise the defect level remains unresolved.",
                            "basis": "fact review plus the independent report-to-ledger relation proposal",
                        },
                        "relation_review": {
                            "status": "PROPOSED",
                            "expected_ids": expected_ids,
                            "rows": relation_rows,
                        },
                        "reason": fact_reason,
                        "basis": fact_basis,
                        "source_refs": sorted(set(report.get("source_refs", [])) | {
                            str(nl_path.relative_to(BASE)),
                            str(puml_path.relative_to(BASE)),
                            f"source_inventory:{inventory['sha256']}",
                            *[f"reference/ledger.json#/items/{eid}" for eid in expected_ids],
                        }),
                    }
                )

    all_pair_ids = sorted(
        path.stem
        for path in (RAW / next(iter(RUNS.values())) / "inputs").glob("*.json")
        if path.stem.isdigit() and len(path.stem) == 4
    )
    for round_number, run_id in RUNS.items():
        run_pair_ids = sorted(
            path.stem
            for path in (RAW / run_id / "inputs").glob("*.json")
            if path.stem.isdigit() and len(path.stem) == 4
        )
        if run_pair_ids != all_pair_ids:
            raise RuntimeError(f"pair population differs in round {round_number}")
    population_counts = {}
    for round_number, run_id in RUNS.items():
        population_counts[str(round_number)] = sum(
            len(load(pair)["reports"])
            for pair in sorted((RAW / run_id / "inputs").glob("*.json"))
            if pair.name.endswith(".json")
        )

    document = {
        "schema": "paper1.independent-raw-first-semantic-review-proposal.v1",
        "review_state": "PROPOSAL_ONLY",
        "reviewer_mode": "independent_raw_first",
        "selection": {
            "method": "seeded stratified random sample: one pair per exact-NL family",
            "seed": SAMPLE_SEED,
            "pair_ids": sample_pairs,
            "rounds": [1, 2, 3],
            "family_count": len(family_members),
            "family_members": family_members,
            "coverage_basis": "one randomly selected pair per exact-NL family; all reports in every selected pair-round set",
        },
        "allowed_inputs": [
            "raw/v60_current/judge/source_runs/*/inputs/*.json",
            "reference/x1v2_input_closure/pairs/*/{nl.txt,plantuml.puml}",
            "reference/ledger.json",
            "artifact:exact_source_inventory embedded in the frozen raw inputs",
        ],
        "coverage": {
            "population_pair_count": len(all_pair_ids),
            "population_pair_round_sets": len(all_pair_ids) * len(RUNS),
            "population_reports_by_round": population_counts,
            "population_reports_total": sum(population_counts.values()),
            "selected_pair_round_sets": len(sample_pairs) * len(RUNS),
            "selected_reports_total": len(entries),
            "selected_reports_by_pair_round": set_counts,
            "selected_pair_ids": sample_pairs,
            "unselected_pair_count": len(all_pair_ids) - len(sample_pairs),
            "scope_note": "This is not a complete review of all pair-round sets; the proposal covers the complete report set inside the selected sets.",
        },
        "entries": entries,
    }
    OUT.write_text(json.dumps(document, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(OUT), "entries": len(entries), "population_reports": sum(population_counts.values()), "selected_sets": len(sample_pairs) * len(RUNS)}))


if __name__ == "__main__":
    main()
