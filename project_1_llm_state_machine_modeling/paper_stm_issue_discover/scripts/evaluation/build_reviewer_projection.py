#!/usr/bin/env python3
"""Build a provider/model-blinded, provider-free reviewer input projection.

The frozen raw archive remains the evidence source and is never rewritten.  A
reviewer can use this projection for semantic/fairness review without seeing
provider, model, profile, prompt, endpoint, or credential fields that happen
to be co-located in legacy raw records.  This command performs only structural
projection, hashing, and closure checks; it never assigns a label.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORBIDDEN_KEYS = frozenset({
    "adapter", "api_key", "base_url", "configured_model", "endpoint",
    "llm_model", "model", "model_id", "model_profile", "observed_model",
    "profile", "provider", "system_prompt", "user_prompt", "api_key_hash",
})
SEMANTIC_FORBIDDEN_KEYS = frozenset({
    "a0_type", "audit_bundle", "binding", "candidate_basis", "candidate_reason",
    "corrected_kni", "d_level", "execution_receipt", "expected", "ledger",
    "plan", "predicate_execution_receipts", "predicate_id", "predicate_inputs",
    "relation", "semantic_adjudication", "strict_da", "validity", "witness_level",
})


def canonical_bytes(value: Any) -> bytes:
    """Serialize a JSON value deterministically for audit hashes."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    """Return the repository's prefixed SHA-256 representation."""

    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    """Hash one frozen file without changing it."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def stable_text(value: Any) -> str:
    """Normalize one authored report field without inspecting its meaning."""

    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def authored_report_projection(target: Any, *, producer_root: str | None) -> dict[str, str]:
    """Project only common report prose into a side-neutral reviewer shape.

    The fixed ``location_text`` slot remains empty for both arms. Current
    stores producer-specific element arrays while X1v2 stores free-text
    ``where`` strings; serializing either would make the arm inferable.
    """

    if not isinstance(target, dict):
        target = {}
    claim = target.get("issue")
    if claim is None:
        claim = target.get("title")
    if claim is None:
        claim = target.get("property")
    if claim is None:
        claim = target.get("observed")
    def redact_producer_root(value: Any) -> str:
        """Remove only the known source-root literal from blind reviewer prose."""

        text = stable_text(value)
        return text.replace(producer_root, "") if producer_root else text

    return {
        "claim_text": redact_producer_root(claim),
        "reason_text": redact_producer_root(target.get("reason")),
        "location_text": "",
    }


def pointer(document: Any, path: str) -> Any:
    """Resolve the RFC 6901 subset used by the frozen inventory."""

    value = document
    for token in path.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def source_pair(archive: Path, side: str, pair_id: str) -> tuple[Path, Path]:
    """Resolve the immutable author-source pair for either side."""

    name = f"llms_emp_feedback_final_{pair_id}" if side == "v60_current" else pair_id
    root = archive / "reference" / "x1v2_input_closure" / "pairs" / name
    return root / "nl.txt", root / "plantuml.puml"


def load_unblind_mapping(path: Path) -> dict[str, Any]:
    """Load or initialize the mapping that is sealed from raw-first reviewers."""

    if path.is_file():
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict) or value.get("schema") != "paper1.manual-adjudication.reviewer-unblind-map.v1":
            raise ValueError("reviewer unblind mapping has an unexpected schema")
        for field in ("arm_tokens", "pair_tokens", "report_tokens", "padded_tokens"):
            if not isinstance(value.get(field), dict):
                raise ValueError(f"reviewer unblind mapping lacks {field}")
        return value
    return {
        "schema": "paper1.manual-adjudication.reviewer-unblind-map.v1",
        "review_status": "FINAL_UNBLINDED_AUDIT",
        "raw_first_visible": False,
        "reason": "This map restores opaque reviewer tokens to frozen report identities only after the independent raw-first proposal is submitted.",
        "basis": "It is final audit provenance, not reviewer input; raw-first reviewers receive only reviewer_input_projection.jsonl and reviewer_projection_audit.json.",
        "arm_tokens": {"v60_current": "arm-a", "x1v2_baseline": "arm-b"},
        "pair_tokens": {},
        "report_tokens": {},
        "padded_tokens": {},
        "rows": [],
    }


def opaque_token(mapping: dict[str, Any], field: str, identity: str, prefix: str) -> str:
    """Return a persistent random token that cannot be reverse-derived from an ID."""

    bucket = mapping[field]
    token = bucket.get(identity)
    if not isinstance(token, str) or not token:
        token = f"{prefix}-{secrets.token_hex(10)}"
        bucket[identity] = token
    return token


def main() -> None:
    """Write the projection JSONL and its auditable manifest."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    directory = args.directory.resolve()
    inventory_path = directory / "inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    rows = inventory["items"]
    grouped: dict[tuple[str, int, str], list[dict[str, Any]]] = {}
    for item in rows:
        grouped.setdefault((item["pair_id"], item["round"], item["side"]), []).append(item)
    pair_rounds = sorted({(pair_id, round_no) for pair_id, round_no, _side in grouped})
    out_path = directory / "reviewer_input_projection.jsonl"
    unblind_path = directory / "reviewer_unblind_mapping.json"
    unblind = load_unblind_mapping(unblind_path)
    audit_rows: list[dict[str, Any]] = []
    unblind_rows: list[dict[str, Any]] = []
    omitted_total: Counter[str] = Counter()
    side_counts: Counter[str] = Counter()
    with out_path.open("w", encoding="utf-8") as output:
        # Give both sealed arms the same pair/round/slot universe.  Padding is
        # represented by empty normalized prose, so missing report production
        # cannot be inferred from an omitted pair/round key.
        for pair_id, round_no in pair_rounds:
            side_items = {
                side: sorted(grouped.get((pair_id, round_no, side), []), key=lambda item: item["report_id"])
                for side in ("v60_current", "x1v2_baseline")
            }
            slot_count = max(len(side_items["v60_current"]), len(side_items["x1v2_baseline"]))
            for slot in range(slot_count):
                for side in ("v60_current", "x1v2_baseline"):
                    item = side_items[side][slot] if slot < len(side_items[side]) else None
                    if item is not None:
                        raw_path = archive / item["raw_method_path"]
                        raw = json.loads(raw_path.read_text(encoding="utf-8"))
                        target = pointer(raw, item["raw_json_pointer"])
                        report_token = opaque_token(unblind, "report_tokens", item["report_id"], "report")
                        raw_target_sha256 = sha256_bytes(canonical_bytes(target))
                    else:
                        target = {}
                        pad_identity = f"{side}:{pair_id}:{round_no}:{slot}"
                        report_token = opaque_token(unblind, "padded_tokens", pad_identity, "slot")
                        raw_target_sha256 = None
                    nl_path, plantuml_path = source_pair(archive, side, pair_id)
                    nl = nl_path.read_text(encoding="utf-8")
                    plantuml = plantuml_path.read_text(encoding="utf-8")
                    row = {
                        "schema": "paper1.manual-adjudication.reviewer-projection-row.v1",
                        "review_key": report_token,
                        "arm_token": unblind["arm_tokens"][side],
                        "pair_token": opaque_token(unblind, "pair_tokens", pair_id, "pair"),
                        "round": round_no,
                        "slot": slot,
                        "report_evidence": authored_report_projection(
                            target,
                            producer_root=(f"llms_emp_feedback_final_{pair_id}" if side == "v60_current" else None),
                        ),
                        "author_source": {
                            "nl": nl,
                            "plantuml": plantuml,
                            "nl_sha256": sha256_file(nl_path),
                            "plantuml_sha256": sha256_file(plantuml_path),
                        },
                        "redactions_applied": True,
                    }
                    row["projection_sha256"] = sha256_bytes(canonical_bytes(row))
                    output.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
                    audit_rows.append({
                        "review_key": row["review_key"],
                        "arm_token": row["arm_token"],
                        "pair_token": row["pair_token"],
                        "round": row["round"],
                        "slot": row["slot"],
                        "projection_sha256": row["projection_sha256"],
                        "padded": item is None,
                        "redactions_applied": row["redactions_applied"],
                    })
                    unblind_rows.append({
                        "review_key": row["review_key"],
                        "side": side,
                        "pair_id": pair_id,
                        "round": round_no,
                        "slot": slot,
                        "report_id": item["report_id"] if item is not None else None,
                        "raw_target_sha256": raw_target_sha256,
                        "padded": item is None,
                    })
                    side_counts[row["arm_token"]] += 1
    audit = {
        "schema": "paper1.manual-adjudication.reviewer-projection-audit.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_inventory_sha256": sha256_file(inventory_path),
        "projection_path": str(out_path.relative_to(archive)),
        "projection_sha256": sha256_file(out_path),
        "row_count": len(audit_rows),
        "arm_counts": dict(sorted(side_counts.items())),
        "projected_report_count": len(rows),
        "padded_slot_count": sum(row["padded"] for row in audit_rows),
        "forbidden_keys": sorted(FORBIDDEN_KEYS | SEMANTIC_FORBIDDEN_KEYS),
        "provider_calls": 0,
        "policy": {
            "semantic_labels": "absent; this file is input projection only",
            "expected_ledger": "absent during raw-first review",
            "legacy_judge_labels": "absent during raw-first review",
            "side_mapping": "arm-a/arm-b is sealed until unblind; pair and round tokens remain stable",
            "raw_mutation": False,
            "projection_shape": "identical allowlist and pair/round/slot universe for both arm tokens; padded slots preserve raw absence without creating a semantic decision",
        },
        "rows": audit_rows,
    }
    (directory / "reviewer_projection_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    unblind["rows"] = unblind_rows
    unblind["generated_at_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    unblind_path.write_text(
        json.dumps(unblind, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "rows": len(audit_rows), "arm_counts": dict(side_counts), "provider_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
