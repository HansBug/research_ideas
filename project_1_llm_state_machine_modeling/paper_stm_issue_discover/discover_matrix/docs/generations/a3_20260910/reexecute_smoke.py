"""Re-execute saved real A3 generations after an exact identity adapter fix."""

import argparse
import hashlib
import json
from pathlib import Path
import uuid

from paper_stm_method.inputs import load_pair
from paper_stm_method.orchestration import runner
from paper_stm_method.orchestration.direct_report import DirectReportResponse
from utils.artifact_io import write_json
from utils.structured_runtime import StructuredCallOutcome


class SavedGeneration:
    def __init__(self, cell):
        self.cell = cell
        self.calls = 0

    def call(self, **kwargs):
        assert self.calls == 0 and kwargs["kind"] == "direct_report"
        assert runner._hash_json(kwargs["prompt"]) == self.cell["prompt_hash"]
        self.calls += 1
        outcome = StructuredCallOutcome[DirectReportResponse].model_validate(self.cell["llm_calls"][0])
        assert outcome.real_llm and outcome.succeeded
        return outcome


def reexecute(source, output):
    assert not output.exists(), "original and derived artifacts must never be overwritten"
    provenance = runner._source_provenance()
    assert not provenance["source_dirty"]
    run_id = uuid.uuid4().hex
    originals = sorted(source.glob("method/*/round-1.json"))
    assert len(originals) == 3
    manifest = {"schema": "a3.saved-generation-reexecution.v1", "run_id": run_id,
                "source_provenance": provenance, "source_root": str(source),
                "prompt_schema_hash": runner._prompt_schema_hash("direct-report"),
                "reason": "Exact state identity adapter repair; zero new provider calls, original generations retained.",
                "sources": {str(p.relative_to(source)): "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest() for p in originals}}
    identity = {"ablation": "direct-report", "run_id": run_id,
                "source_provenance": provenance, "run_contract_hash": runner._hash_json(manifest)}
    write_json(output / "run_manifest.json", {**manifest, "run_contract_hash": identity["run_contract_hash"]})
    for path in originals:
        original = json.loads(path.read_text())
        nl = next(a for a in original["context_manifest"]["artifacts"] if a["role"] == "natural_language")
        pair = load_pair(Path(nl["path"]).parent)
        cell = runner._method_cell(pair=pair, round_index=1, runtime=SavedGeneration(original), output_root=output, run_identity=identity)
        assert cell["model_output"] == original["model_output"]
        runner._finalize_w2_audit_links(output_root=output, pair_id=pair.pair_id, rounds_data=[cell])
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    reexecute(args.source.resolve(), args.output.resolve())
