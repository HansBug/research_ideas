"""Provider-free before/after audit for soundness fragments and S2 scope."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

from paper_stm_method.backends.fcstm_native import all_transition_carriers, load_native_fcstm, resolve_state
from paper_stm_method.backends.source_static import _endpoint_matches, _scope_matches
from paper_stm_method.compiler.soundness import assess_soundness
from paper_stm_method.inputs.models import parse_fcstm


def _hash(payload: dict[str, Any]) -> str:
    """Return a stable audit hash without self-reference."""

    return "sha256:" + hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _model(cell: dict[str, Any]):
    """Reload the closed FCSTM referenced by one immutable method context."""

    artifacts = (cell.get("context_manifest") or {}).get("artifacts") or []
    paths = [item.get("path") for item in artifacts if item.get("role") == "fcstm_model"]
    if len(paths) != 1 or not isinstance(paths[0], str):
        raise ValueError("cell does not identify exactly one FCSTM input artifact")
    return parse_fcstm(Path(paths[0]).read_text(encoding="utf-8"))


def _s2_verdict(model: Any, inputs: dict[str, Any]) -> tuple[str, str]:
    """Re-evaluate S2 inventory semantics without calling a provider or Judge."""

    native = load_native_fcstm(model)
    scope = inputs.get("scope")
    source, target = inputs.get("source"), inputs.get("target")
    if not isinstance(scope, str) or not isinstance(source, str) or not isinstance(target, str):
        return "degraded", "S2 typed source/target/scope is not a unique string binding"
    if scope != "closed_fcstm" and resolve_state(native, scope) is None:
        return "degraded", "exact owner scope does not resolve to a native transition owner"
    found = any(_scope_matches(native, row, scope) and _endpoint_matches(native, row, source, target) for row in all_transition_carriers(native))
    return ("true" if found else "false"), ("global closed_fcstm inventory" if scope == "closed_fcstm" else "exact canonical owner inventory")


def build_shadow(method_root: str | Path) -> dict[str, Any]:
    """Produce a non-mutating shadow over every saved predicate receipt."""

    root = Path(method_root)
    records: list[dict[str, Any]] = []
    s2_records: list[dict[str, Any]] = []
    for path in sorted((root / "method").glob("*/round-*.json")):
        cell = json.loads(path.read_text(encoding="utf-8"))
        model = _model(cell)
        for receipt in cell.get("predicate_execution_receipts", []):
            predicate_id = receipt.get("predicate_id")
            if predicate_id is None:
                continue
            inputs = dict(receipt.get("typed_inputs") or {})
            assessment = assess_soundness(predicate_id, inputs, model=model, model_hash=inputs.get("model_hash"))
            old_w = receipt.get("witness_level")
            proposed_w = "W1" if old_w == "W2" and not assessment.satisfied else old_w
            records.append({
                "pair_id": cell["pair_id"], "round": cell["round"], "obligation_id": receipt["obligation_id"],
                "predicate_id": predicate_id, "old_w": old_w, "proposed_w": proposed_w,
                "old_execution_state": receipt.get("execution_state"), "soundness": assessment.model_dump(mode="json"),
                "reason": "Shadow changes only the W admission boundary; candidate/report/D/publication are immutable inputs.",
                "basis": receipt.get("receipt_hash", "immutable predicate receipt"),
            })
            if predicate_id == "S2":
                verdict, scope_basis = _s2_verdict(model, inputs)
                s2_records.append({
                    "pair_id": cell["pair_id"], "round": cell["round"], "obligation_id": receipt["obligation_id"],
                    "scope": inputs.get("scope"), "source": inputs.get("source"), "target": inputs.get("target"),
                    "old_verdict": receipt.get("predicate_verdict"), "proposed_verdict": verdict,
                    "exact_scout": bool("scout" in str(receipt.get("contract_id", "")).lower()),
                    "reason": "S2 scope shadow uses the same native global/owner-local inventory contract as the proposed backend.",
                    "basis": scope_basis,
                })
    transitions = Counter(f"{row['old_w']}->{row['proposed_w']}" for row in records)
    payload: dict[str, Any] = {
        "schema_version": "evidence-discovery.soundness-s2-shadow.v1",
        "method_root": str(root.resolve()), "record_count": len(records),
        "w_transition_matrix": dict(sorted(transitions.items())), "records": records,
        "s2_records": s2_records,
        "surface_invariant": {"candidate": "unchanged", "report": "unchanged", "D": "unchanged", "publication": "unchanged"},
        "reason": "Provider-free shadow of immutable method receipts; no method provider, Judge, ledger, or expected issue is read.",
        "basis": "saved typed inputs, pyfcstm native projection, and frozen backend contracts",
    }
    payload["artifact_hash"] = _hash(payload)
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    """Write one standalone immutable shadow artifact."""

    parser = argparse.ArgumentParser(description="Audit proposed predicate-soundness and S2 scope changes without LLM calls.")
    parser.add_argument("--method-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = build_shadow(args.method_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "artifact_hash": payload["artifact_hash"], "records": payload["record_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
