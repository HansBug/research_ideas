from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def write_markdown_summary(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Evidence-Discovery Run Audit",
        "",
        f"- run id: `{summary.get('run_id')}`",
        f"- run contract: `{summary.get('run_contract_hash')}`",
        f"- status: `{summary.get('status')}`",
        f"- scope: `{summary.get('scope')}`",
        f"- profile: `{summary.get('profile')}`",
        f"- source commit: `{summary.get('source_commit')}`",
        f"- source branch: `{summary.get('source_branch')}`",
        f"- registry: `{summary.get('registry_version')}`",
        f"- pair count: `{summary.get('pair_count')}`",
        f"- method cells: `{summary.get('method_cell_count')}`",
        f"- judge pairs: `{summary.get('judge_pair_count')}`",
        f"- method cost USD: `{summary.get('method_cost_usd')}`",
        f"- judge cost USD: `{summary.get('judge_cost_usd')}`",
        "",
        "## Overall",
        "",
    ]
    overall = summary.get("metrics", {}).get("overall", {})
    for key, value in overall.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Pair Status", "", "| pair | method cells | eligible | judge | errors | method USD | judge USD |", "|---|---:|---:|---|---:|---:|---:|"])
    for pair_id, row in sorted(summary.get("per_pair", {}).items()):
        lines.append(
            f"| {pair_id} | {row.get('method_cells')} | {row.get('eligible_method_cells')} | "
            f"{row.get('judge_status')} | {row.get('errors')} | "
            f"{row.get('method_cost_usd')} | {row.get('judge_cost_usd')} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
