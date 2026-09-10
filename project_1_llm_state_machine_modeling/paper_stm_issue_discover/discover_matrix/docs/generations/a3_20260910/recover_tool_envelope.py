"""Recover the first complete report JSON from one malformed tool envelope."""

import argparse
import json
from pathlib import Path
import uuid

from paper_stm_method.inputs import load_pair
from paper_stm_method.orchestration import runner
from paper_stm_method.orchestration.direct_report import DirectReport, DirectReportResponse
from utils.artifact_io import write_json
from utils.structured_runtime import StructuredCallOutcome
from verify_sources import digest, read


def recover_arguments(arguments):
    if set(arguments) == {"reason", "basis", "issues"}:
        # Only the observed alternating, disjoint field blocks; no field inference.
        head = {"title", "requirement_quote", "source_quote", "source_refs"}
        tail = set(DirectReport.model_fields) - head
        fragments = arguments["issues"]
        assert isinstance(fragments, list) and fragments and len(fragments) % 2 == 0
        assert all(isinstance(row, dict) and set(row) == (head if i % 2 == 0 else tail)
                   for i, row in enumerate(fragments))
        return DirectReportResponse.model_validate({**arguments, "issues": [
            {**fragments[i], **fragments[i + 1]} for i in range(0, len(fragments), 2)]})
    assert set(arguments) == {"reason", "basis"}
    assert '</reason>\n<parameter name="issues">' in arguments["reason"]
    return DirectReportResponse.model_validate(arguments)


def recover(source, output):
    assert not output.exists()
    original = read(source)
    assert not original["eligible"] and len(original["llm_calls"]) == 1
    saved = original["llm_calls"][0]
    audit_path = Path(saved["attempts"][0]["audit_path"])
    records = [json.loads(line) for line in audit_path.read_text().splitlines()]
    first = next(row for row in records if isinstance(row.get("arguments"), dict))
    assert first["turn"] == 1
    response = recover_arguments(first["arguments"])
    recovery = {"schema": "a3.tool-envelope-recovery.v1", "source": str(source), "source_hash": digest(source),
                "audit_source": str(audit_path), "audit_hash": digest(audit_path), "turn": 1,
                "reason": ("The first generated report fields were split into alternating disjoint adjacent blocks; exact field-set matching restores each original report without changing field values."
                           if "issues" in first["arguments"] else
                           "The first generated complete issues JSON was embedded in reason by malformed tool-parameter serialization.") + " No new model call or report synthesis.",
                "original_failure_retained": True, "schema_validation_failures_retained": len(saved["schema_validation_failures"])}
    outcome = StructuredCallOutcome[DirectReportResponse].model_validate(saved).model_copy(update={
        "status": "success", "response": response,
        "result": {**saved["result"], "structured_recovery": recovery},
        "reason": recovery["reason"], "basis": "Exact first-turn structural recovery followed by the unchanged A3 schema; all original failures retained.",
    })

    class Saved:
        def call(self, **kwargs):
            assert runner._hash_json(kwargs["prompt"]) == original["prompt_hash"]
            return outcome

    nl = next(a for a in original["context_manifest"]["artifacts"] if a["role"] == "natural_language")
    pair = load_pair(Path(nl["path"]).parent)
    identity = {"ablation": "direct-report", "run_id": uuid.uuid4().hex,
                "source_provenance": runner._source_provenance(), "run_contract_hash": runner._hash_json(recovery)}
    write_json(output / "run_manifest.json", {**recovery, **identity})
    cell = runner._method_cell(pair=pair, round_index=original["round"], runtime=Saved(), output_root=output, run_identity=identity)
    runner._finalize_w2_audit_links(output_root=output, pair_id=pair.pair_id, rounds_data=[cell])
    print({"pair": pair.pair_id, "round": original["round"], "generated": len(response.issues), "published": len(cell["report_issue_clusters"]), "new_provider_calls": 0})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    recover(args.source.resolve(), args.output.resolve())
