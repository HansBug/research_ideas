"""Audit A2 recorded calls and method cells without provider calls."""

import argparse
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re

from paper_stm_method.inputs import load_pair
from paper_stm_method.semantics.workflow import prompt_context_payload
from paper_stm_method.semantics.no_predicates import DISABLED_PREDICATE_STEPS
from paper_stm_judge.artifacts import adapt_evidence_discovery_release


MARKER = "Stage-scoped context projection and complete artifact manifest:\n"
MECHANISM = re.compile(r"predicate_id|predicate_inputs|frozen predicate|predicate registry|routing discipline|S4/S5")
FIELDS = {"predicate_id", "predicate_inputs"}
DECODER = json.JSONDecoder()


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def keys(value):
    if isinstance(value, dict):
        yield from value
        for item in value.values():
            yield from keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from keys(item)


def mask_role_instructions(payload):
    """The only allowed context differences are these fixed role descriptions."""
    value = deepcopy(payload)
    value["source_roles"].pop("fcstm_model", None)
    for section in value["context_manifest"]["sections"]:
        if section["section_id"] == "model-grounding":
            section.pop("purpose", None)
            section.pop("basis", None)
    for name in ("fcstm_model", "verify_facts"):
        if value.get(name):
            value[name].pop("reason", None)
    return value


def audit(root, reference_root, report_root, *, partial=False):
    manifest = read(root / "run_manifest.json")
    reference = read(reference_root / "run_manifest.json")
    assert manifest["ablation"] == "no-predicates"
    assert reference["ablation"] == "none"
    assert manifest["registry_hash"] == reference["registry_hash"]
    if manifest["profile"] == "aizzz-luna-eval":
        assert manifest["model_config_hash"] == "sha256:1b249a55de2f0b825c436305111743000d11077cd4fc3b8ac4ba215cc45305c6"
    else:
        assert manifest["model_config_hash"] == reference["model_config_hash"]
    for pair_id, value in manifest["pair_input_hashes"].items():
        assert reference["pair_input_hashes"][pair_id] == value, pair_id
    planned = {(p, r) for p in manifest["selected_pair_ids"] for r in range(1, manifest["rounds"] + 1)}
    rows, seen, hashes = [], set(), {}
    for path in sorted((root / "method").glob("*/round-*.json")):
        cell = read(path)
        key = (cell["pair_id"], cell["round"])
        assert key in planned and key not in seen
        seen.add(key)
        for field in ("run_id", "ablation", "run_contract_hash", "source_provenance"):
            assert cell[field] == manifest[field], (key, field)
        assert cell["pair_input_hash"] == manifest["pair_input_hashes"][key[0]]
        assert not cell["predicate_execution_receipts"]
        row = dict(pair_id=key[0], round=key[1], status=cell["status"], eligible=cell["eligible"],
                   errors=cell.get("errors", []), reports=len(cell["report_issue_clusters"]))
        if cell["eligible"]:
            assert cell["status"] in {"completed", "completed_with_diagnostics"}
            stage = cell["stage_outputs"]
            ablation = stage["ablation"]
            assert ablation["inspection_context"] == "enabled"
            assert ablation["predicate_execution"] == "disabled_by_ablation"
            assert {s["function"] for s in ablation["disabled_steps"]} == set(DISABLED_PREDICATE_STEPS)
            assert all(s["status"] == "disabled_by_ablation" for s in ablation["disabled_steps"])
            execute = stage["execute_batch"]
            assert execute["prepared_count"] == execute["candidate_count"]
            assert execute["execution_probe_count"] == execute["satisfied_count"] == 0
            assert not execute["primary_route_telemetry"] and not execute["predicate_execution_receipts"]
            for record in cell["evidence_records"]:
                assert record["plan"] is record["receipt"] is record["execution_receipt"] is None
                assert record["predicate_id"] is None and record["predicate_inputs"] == {}
                assert record["witness_level"] in {"W0", "W1"}
            for report in cell["report_issue_clusters"]:
                assert report["witness_level"] == "W1" and report["d_level"] in {"D1", "D2"}
            assert len(adapt_evidence_discovery_release(path, ())[0]) == row["reports"]
            assert all("predicate_registry" not in s["input_artifact_roles"] for s in cell["stage_receipts"])
            checks = execute["frontier_batch"]["checks"]
            row.update(
                report_W=dict(Counter(r["witness_level"] for r in cell["report_issue_clusters"])),
                evidence_W=stage["publish"]["w_distribution"], internal_D=stage["publish"]["d_distribution"],
                frontier_kinds=dict(Counter(c["kind"] for c in checks)),
                candidate_counts={name: execute[name] for name in ("candidate_count", "llm_candidate_count", "frontier_candidate_count", "domain_invariant_candidate_count", "exact_s2_scout_candidate_count")},
                publish=stage["publish"], d_unresolved=stage["validate_d"]["final_unresolved_ids"],
                schema_corrections=sum(len(c["schema_validation_failures"]) for c in cell["llm_calls"]),
                transport_events=[r for c in cell["llm_calls"] for a in c["attempts"] for r in a["retry_records"]],
                llm_calls=len(cell["llm_calls"]),
            )
        else:
            assert cell["status"] == "failed_with_receipt"
        rows.append(row)
    if not partial:
        assert seen == planned, ("missing terminal cells", sorted(planned - seen))

    @lru_cache(maxsize=None)
    def full_context(pair_id, stage):
        pair = load_pair(report_root / "pairs" / pair_id)
        assert pair.context_manifest.manifest_hash == manifest["pair_input_hashes"][pair_id]
        return mask_role_instructions(json.loads(json.dumps(prompt_context_payload(pair, stage=stage))))

    def check_text(text, pair_id):
        assert not MECHANISM.search(text), (pair_id, MECHANISM.search(text).group() if MECHANISM.search(text) else None)
        count = 0
        for part in text.split(MARKER)[1:]:
            payload, _ = DECODER.raw_decode(part)
            assert payload["source_roles"]["fcstm_model"] == "closed_model_semantic_binding"
            assert mask_role_instructions(payload) == full_context(pair_id, payload["stage"]), (pair_id, payload["stage"])
            count += 1
        return count

    traces, calls, contexts, schema_names, models, settings = 0, 0, 0, Counter(), set(), Counter()
    for path in sorted((root / "llm").rglob("audit.jsonl")):
        pair_id = path.relative_to(root / "llm" / "method").parts[0]
        for line in path.read_text().splitlines():
            event = json.loads(line)
            if "input_text" in event:
                traces += 1
                assert not FIELDS.intersection(keys(event["output_schema"]))
                schema_names[event["output_schema"]["title"]] += 1
                check_text(event["system_prompt"], pair_id)
                contexts += check_text(event["input_text"], pair_id)
                models.add(event["model"])
            if "rendered_input_projection" in event:
                calls += 1
                projection = event["rendered_input_projection"]
                assert not FIELDS.intersection(keys(projection["response_format"]))
                check_text(projection["system"], pair_id)
                contexts += sum(check_text(m, pair_id) for m in projection["messages"] if isinstance(m, str))
                settings[json.dumps(projection["model_settings"], sort_keys=True)] += 1
    if traces:
        assert models == {"gpt-5.6-luna"}
        assert calls and contexts >= traces
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix not in {".lock", ".part"}:
            hashes[str(path.relative_to(root))] = digest(path)
    return dict(schema="paper1.a2-run-audit.v1", partial=partial, run_id=manifest["run_id"],
                human_confirmations=0, planned_cells=len(planned), terminal_cells=len(seen),
                cells=rows, trace_headers=traces, rendered_calls=calls, checked_contexts=contexts,
                schema_names=dict(schema_names), model_settings=dict(settings), hashes=hashes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--reference-root", type=Path, required=True)
    parser.add_argument("--report-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--partial", action="store_true")
    args = parser.parse_args()
    result = audit(args.root, args.reference_root, args.report_root, partial=args.partial)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"hashes", "cells"}}, indent=2))
    print(json.dumps([{k: r.get(k) for k in ("pair_id", "round", "status", "reports", "internal_D", "schema_corrections")} for r in result["cells"]], indent=2))


if __name__ == "__main__":
    main()
