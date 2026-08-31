"""Replay every final predicate-gold false/control receipt provider-free.

Each saved command is redirected to a temporary receipt root. The replay never
overwrites canonical evidence and compares only deterministic semantic fields,
not timestamps or output-file byte hashes.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    PredicateGoldDataset,
    canonical_sha256,
    sha256_path,
    write_json,
)


def _replace_option(command: list[str], option: str, value: str) -> None:
    """Replace one required argv option without changing the saved query."""

    try:
        index = command.index(option)
    except ValueError as error:
        raise ValueError(f"saved command lacks {option}") from error
    if index + 1 >= len(command):
        raise ValueError(f"saved command has no value for {option}")
    command[index + 1] = value


def _semantic_projection(receipt: dict[str, Any]) -> dict[str, Any]:
    """Project deterministic fields that establish Boolean execution closure."""

    projected = {
        key: receipt.get(key)
        for key in (
            "schema_version",
            "request_id",
            "request_sha256",
            "artifact_role",
            "artifact_path",
            "artifact_sha256",
            "state",
            "verdict",
            "acceptance_match",
            "backend",
            "oracle_id",
        )
    }
    constituents = receipt.get("constituents")
    if constituents is not None:
        projected["constituents"] = [
            {
                key: item.get(key)
                for key in (
                    "constituent_id",
                    "request_id",
                    "state",
                    "verdict",
                    "acceptance_match",
                )
            }
            for item in constituents
        ]
    return projected


def _replay_one(
    *,
    repo_root: Path,
    paper_root: Path,
    saved_root: Path,
    temporary_root: Path,
) -> dict[str, Any]:
    """Replay one saved receipt command into a temporary directory."""

    saved_path = saved_root / "receipt.json"
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    command = list(saved["command"])
    command[0] = sys.executable
    _replace_option(command, "--receipt-root", str(temporary_root))
    python_paths = [
        str(paper_root / "evaluation" / "src"),
        str(paper_root / "method" / "src"),
        str(repo_root),
    ]
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH")
    if existing:
        python_paths.append(existing)
    environment["PYTHONPATH"] = os.pathsep.join(python_paths)
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    observed_path = temporary_root / "receipt.json"
    if completed.returncode != 0 or not observed_path.is_file():
        raise ValueError(
            f"replay failed for {saved_root}: returncode={completed.returncode}; "
            f"stderr={completed.stderr[-1000:]}"
        )
    observed = json.loads(observed_path.read_text(encoding="utf-8"))
    expected_projection = _semantic_projection(saved)
    observed_projection = _semantic_projection(observed)
    if observed_projection != expected_projection:
        raise ValueError(
            f"semantic replay mismatch for {saved_root}: "
            f"expected={expected_projection!r}, observed={observed_projection!r}"
        )
    return {
        "saved_receipt": saved_path.relative_to(repo_root).as_posix(),
        "ledger_id": saved_root.parent.name,
        "artifact_role": saved["artifact_role"],
        "state": observed["state"],
        "verdict": observed["verdict"],
        "request_sha256": observed["request_sha256"],
        "constituent_count": len(observed.get("constituents") or []),
        "result": "PASS",
    }


def replay_all(
    *,
    repo_root: Path,
    canonical_path: Path,
    output_path: Path,
    replayed_at: str,
) -> dict[str, Any]:
    """Replay all final exact/proxy defective and true-control receipts."""

    dataset = PredicateGoldDataset.model_validate_json(
        canonical_path.read_text(encoding="utf-8")
    )
    gold_root = canonical_path.parent
    paper_root = repo_root / "project_1_llm_state_machine_modeling" / "paper_stm_issue_discover"
    executable_ids = sorted(
        item.ledger_id
        for item in dataset.items.values()
        if item.execution is not None or item.proxy_execution is not None
    )
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(
        prefix=".predicate-gold-replay-", dir=repo_root
    ) as directory:
        temporary = Path(directory)
        for ledger_id in executable_ids:
            for role in ("defective", "positive_control"):
                rows.append(
                    _replay_one(
                        repo_root=repo_root,
                        paper_root=paper_root,
                        saved_root=gold_root / "receipts" / ledger_id / role,
                        temporary_root=temporary / ledger_id / role,
                    )
                )
    unsigned = {
        "schema_version": "paper1.predicate-gold.full-replay.v1",
        "replayed_at": replayed_at,
        "canonical_path": canonical_path.relative_to(gold_root).as_posix(),
        "canonical_sha256": sha256_path(canonical_path),
        "executable_issue_count": len(executable_ids),
        "receipt_replay_count": len(rows),
        "blocked_execution_count": 0,
        "provider_experiment_calls": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
        "full_experiment_reruns": 0,
        "rows": rows,
        "result": "PASS",
    }
    report = {**unsigned, "report_sha256": canonical_sha256(unsigned)}
    write_json(output_path, report)
    return report


def main(argv: list[str] | None = None) -> int:
    """Run the full provider-free replay audit."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replayed-at", required=True)
    args = parser.parse_args(argv)
    report = replay_all(
        repo_root=args.repo_root.resolve(),
        canonical_path=args.canonical.resolve(),
        output_path=args.output.resolve(),
        replayed_at=args.replayed_at,
    )
    print(
        f"PASS executable={report['executable_issue_count']} "
        f"receipts={report['receipt_replay_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
