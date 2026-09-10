"""Repair exact identity serialization using saved generations, without providers."""

import argparse
from pathlib import Path
import uuid

from paper_stm_method.inputs import load_pair
from paper_stm_method.orchestration import runner
from paper_stm_method.orchestration.direct_report import execution_candidate
from paper_stm_method.semantics.obligations import CandidateIssue
from paper_stm_judge.artifacts import adapt_evidence_discovery_release
from reexecute_smoke import SavedGeneration
from utils.artifact_io import write_json
from verify_sources import read, digest


def reexecute(analysis, root):
    provenance = runner._source_provenance()
    assert not provenance["source_dirty"]
    for model, arm in read(analysis)["models"].items():
        directory = root / model / "binding-corrected"
        assert not directory.exists()
        changes = []
        identity = {"ablation": "direct-report", "run_id": uuid.uuid4().hex,
                    "source_provenance": provenance,
                    "run_contract_hash": runner._hash_json({"source_index": digest(analysis), "source_provenance": provenance, "model": model})}
        for row in arm["a3"]["cells"]:
            path = Path(row["source"])
            original = read(path)
            assert original["eligible"]
            nl = next(a for a in original["context_manifest"]["artifacts"] if a["role"] == "natural_language")
            pair = load_pair(Path(nl["path"]).parent)
            affected = []
            for record in original["evidence_records"]:
                if not record.get("adapted_candidate"):
                    continue
                candidate = CandidateIssue.model_validate(record["adapted_candidate"])
                if execution_candidate(candidate, pair).predicate_inputs != candidate.predicate_inputs:
                    affected.append(record["generation_index"])
            if not affected:
                continue
            cell = runner._method_cell(pair=pair, round_index=original["round"], runtime=SavedGeneration(original), output_root=directory, run_identity=identity)
            assert cell["model_output"] == original["model_output"]
            runner._finalize_w2_audit_links(output_root=directory, pair_id=pair.pair_id, rounds_data=[cell])
            new_path = directory / "method" / pair.pair_id / f"round-{original['round']}.json"
            before, _, _, _ = adapt_evidence_discovery_release(path, ())
            after, _, _, _ = adapt_evidence_discovery_release(new_path, ())
            before_projection = [r.model_dump(mode="json") for r in before]
            after_projection = [r.model_dump(mode="json") for r in after]
            changes.append({"pair_id": pair.pair_id, "round": original["round"], "source": str(path), "source_hash": digest(path),
                            "corrected_source": str(new_path), "corrected_hash": digest(new_path), "affected_generation_indices": affected,
                            "generated_output_unchanged": True, "published_before": len(before), "published_after": len(after),
                            "judge_projection_unchanged": before_projection == after_projection,
                            "before_projection_hash": runner._hash_json(before_projection), "after_projection_hash": runner._hash_json(after_projection)})
        manifest = {"schema": "a3.exact-identity-reexecution.v1", **identity, "source_index": str(analysis), "source_index_hash": digest(analysis),
                    "new_provider_calls": 0, "reason": "Complete exact state/event identity binding across registered input slots; unchanged saved generations.", "cells": changes}
        write_json(directory / "run_manifest.json", manifest)
        print({"model": model, "corrected_cells": len(changes), "projection_changed": [f"{c['pair_id']}/r{c['round']}" for c in changes if not c["judge_projection_unchanged"]]}, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    reexecute(args.analysis.resolve(), args.root.resolve())
