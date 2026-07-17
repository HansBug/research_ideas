from __future__ import annotations

import json
from typing import Any, Mapping

from .records import RecordStore, canonical_json, sha256_file, sha256_json


TASK_FIELDS = ("stage", "loop_no", "model", "targets", "current_records", "readable_history")
REFERENCE_MARKERS = (
    "known_issue_seed",
    "evaluation_reference",
    "gold_issue",
    "gold_binding",
    "gold_repair",
    "gold_stm",
    "expected_issue_id",
)


def validate_reference_blind(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered = str(key).lower()
            if any(marker in lowered for marker in REFERENCE_MARKERS):
                raise ValueError(f"reference_content_forbidden:{path}.{key}")
            validate_reference_blind(item, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            validate_reference_blind(item, path=f"{path}[{index}]")


def freeze_task_snapshot(
    *,
    model_text: str,
    model_sha256: str,
    normalized_inspect: Mapping[str, Any],
    current_records: Mapping[str, Any],
) -> dict[str, Any]:
    snapshot = {
        "stage": "B-discover",
        "loop_no": 0,
        "model": {
            "model_id": "STM_0",
            "content": model_text,
            "sha256": model_sha256,
            "model_sha256": model_sha256,
            "normalized_inspect": dict(normalized_inspect),
        },
        "targets": [],
        "current_records": dict(current_records),
        "readable_history": [],
    }
    if tuple(snapshot) != TASK_FIELDS:
        raise AssertionError("read_task field order drifted")
    validate_reference_blind(snapshot)
    return snapshot


def publish_context(
    store: RecordStore,
    *,
    attempt_id: str,
    system_prompt: str,
    snapshot: Mapping[str, Any],
    content_language: str,
) -> dict[str, Any]:
    validate_reference_blind(snapshot)
    if set(snapshot) != set(TASK_FIELDS):
        raise ValueError("read_task must contain exactly six top-level fields")
    directory = store.outdir / "contexts" / attempt_id
    if directory.exists():
        raise FileExistsError(directory)
    directory.mkdir(parents=True)
    prompt_path = directory / "prompt.md"
    context_json_path = directory / "context.json"
    context_md_path = directory / "context.md"
    prompt_path.write_text(system_prompt.rstrip() + "\n", encoding="utf-8")
    context_json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    context_md_path.write_text(
        "# Frozen B-discover context\n\n"
        f"- language: `{content_language}`\n"
        f"- snapshot sha256: `{sha256_json(snapshot)}`\n\n"
        "```json\n"
        + json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n```\n",
        encoding="utf-8",
    )
    manifest = {
        "schema_version": "paper1.context_manifest.v1",
        "attempt_id": attempt_id,
        "context_snapshot_head": sha256_json(snapshot),
        "task_fields": list(TASK_FIELDS),
        "content_language": content_language,
        "files": {
            "prompt.md": sha256_file(prompt_path),
            "context.json": sha256_file(context_json_path),
            "context.md": sha256_file(context_md_path),
        },
        "reference_content_sentinel_hits": 0,
    }
    manifest_path = directory / "context_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {**manifest, "context_manifest_path": str(manifest_path.relative_to(store.outdir))}


def verify_frozen_snapshot(snapshot: Mapping[str, Any], manifest: Mapping[str, Any]) -> None:
    if sha256_json(snapshot) != manifest.get("context_snapshot_head"):
        raise ValueError("read_task snapshot drift")
    if canonical_json(list(snapshot)) != canonical_json(list(TASK_FIELDS)):
        raise ValueError("read_task field order drift")
