from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

from paper_stm_repair_loop.config import PAIRS_JSONL

FORMAL_CASE_COUNT = 60
PROVENANCE_KEYS = (
    "research_commit",
    "pairs_sha256",
    "artifact_set_sha256",
    "implementation_tree_sha256",
    "working_contract_set_sha256",
)


def _bounds(value: str) -> tuple[int, ...]:
    values = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not values or any(item <= 0 for item in values):
        raise argparse.ArgumentTypeError("bounds must be positive comma-separated integers")
    return values


def _read_pair_ids(path: Path) -> tuple[list[str], list[str]]:
    ids: list[str] = []
    reasons: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [], [f"pairs_manifest_missing: {path}"]
    except Exception as exc:
        return [], [f"pairs_manifest_unreadable: {path}: {type(exc).__name__}: {exc}"]

    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            reasons.append(f"pairs_manifest_invalid_json: line {line_no}: {exc.msg}")
            continue
        pair_id = row.get("pair_id")
        if not isinstance(pair_id, str) or not pair_id:
            reasons.append(f"pairs_manifest_missing_pair_id: line {line_no}")
            continue
        ids.append(pair_id)
    duplicate_ids = sorted({pair_id for pair_id in ids if ids.count(pair_id) > 1})
    if duplicate_ids:
        reasons.append(f"pairs_manifest_duplicate_pair_ids: {duplicate_ids}")
    return sorted(ids), reasons


def _fcstm_files(fcstm_dir: Path) -> tuple[dict[str, Path], list[str]]:
    if not fcstm_dir.exists():
        return {}, [f"fcstm_dir_missing: {fcstm_dir}"]
    if not fcstm_dir.is_dir():
        return {}, [f"fcstm_dir_not_directory: {fcstm_dir}"]
    files = sorted(fcstm_dir.glob("*.fcstm"))
    by_stem: dict[str, Path] = {}
    reasons: list[str] = []
    for file in files:
        if file.stem in by_stem:
            reasons.append(f"fcstm_duplicate_stem: {file.stem}")
        by_stem[file.stem] = file
    return by_stem, reasons


def _load_report_provenance(fcstm_dir: Path) -> tuple[dict[str, Any], list[str]]:
    manifest_path = fcstm_dir.parent / "manifest.json"
    if not manifest_path.exists():
        return {}, [f"report_manifest_missing: {manifest_path}"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"report_manifest_invalid_json: {manifest_path}: {exc.msg}"]
    except Exception as exc:
        return {}, [f"report_manifest_unreadable: {manifest_path}: {type(exc).__name__}: {exc}"]

    provenance = {
        "report_manifest_path": str(manifest_path),
        **{key: manifest.get(key) for key in PROVENANCE_KEYS if key in manifest},
    }
    missing_required = [
        key
        for key in ("research_commit", "pairs_sha256", "artifact_set_sha256")
        if not provenance.get(key)
    ]
    reasons = [f"report_manifest_missing_provenance_keys: {missing_required}"] if missing_required else []
    return provenance, reasons


def _preflight_assets(
    *, pairs_path: Path, fcstm_dir: Path, formal_60_case: bool
) -> tuple[list[str], dict[str, Path], dict[str, Any], list[str]]:
    pair_ids, reasons = _read_pair_ids(pairs_path)
    fcstm_by_stem, fcstm_reasons = _fcstm_files(fcstm_dir)
    provenance, provenance_reasons = _load_report_provenance(fcstm_dir)
    reasons.extend(fcstm_reasons)
    reasons.extend(provenance_reasons)

    if formal_60_case:
        if len(pair_ids) != FORMAL_CASE_COUNT:
            reasons.append(
                f"pairs_manifest_count_mismatch: expected {FORMAL_CASE_COUNT}, got {len(pair_ids)}"
            )
        if len(fcstm_by_stem) != FORMAL_CASE_COUNT:
            reasons.append(
                f"fcstm_file_count_mismatch: expected {FORMAL_CASE_COUNT}, got {len(fcstm_by_stem)}"
            )
        fcstm_stems = sorted(fcstm_by_stem)
        if pair_ids != fcstm_stems:
            missing_fcstm = sorted(set(pair_ids) - set(fcstm_stems))
            extra_fcstm = sorted(set(fcstm_stems) - set(pair_ids))
            reasons.append(
                "pair_fcstm_id_mismatch: "
                f"missing_fcstm_for_pair_ids={missing_fcstm}; extra_fcstm_stems={extra_fcstm}"
            )
    return pair_ids, fcstm_by_stem, provenance, reasons


def _failure(reason: str, details: list[str]) -> dict[str, Any]:
    return {
        "status": "input_asset_preflight_failed",
        "failure_reason": reason,
        "reasons": details,
    }


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _row(
    pair_id: str,
    fcstm_file: Path,
    bound: int,
    wall_seconds: float | None,
    input_provenance: dict[str, Any],
    probe_contract: dict[str, Any],
) -> dict[str, Any]:
    from paper_stm_repair_loop.eval_env.fbmcq import FBMCQAPI
    from paper_stm_repair_loop.pyfcstm_adapter import check_fcstm

    fcstm = fcstm_file.read_text(encoding="utf-8")
    checked = check_fcstm(fcstm, str(fcstm_file))
    inspect = checked.get("inspect") or {}
    query = f"init cold;\ncheck invariant <= {bound}: !terminated();"
    started = time.monotonic()
    base = {
        "pair_id": pair_id,
        "bound": bound,
        "property_kind": "invariant",
        "query": query,
        "model_sha256": _sha256_text(fcstm),
        "fcstm_path": str(fcstm_file),
        "state_count": len(inspect.get("states") or []),
        "transition_count": len(inspect.get("transitions") or []),
        "process_wall_seconds": wall_seconds,
        "input_provenance": input_provenance,
        "probe_contract": probe_contract,
    }
    try:
        observation = FBMCQAPI(
            fcstm,
            process_wall_seconds=wall_seconds,
        ).fbmcq(query)
        raw_report = observation.raw.to_json()["data"]
        return {
            **base,
            "status": "completed",
            "elapsed_seconds": time.monotonic() - started,
            "holds": observation.holds,
            "solver_status": observation.status,
            "replay_status": observation.replay_status,
            "process_isolation": observation.process_isolation,
            "timings": raw_report.get("timings", {}),
        }
    except Exception as exc:
        return {
            **base,
            "status": "inconclusive",
            "elapsed_seconds": time.monotonic() - started,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "metadata": getattr(exc, "metadata", None),
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Opt-in Issue #165 FBMCQ performance probe over frozen pairs."
    )
    parser.add_argument("--pairs", type=Path, default=PAIRS_JSONL)
    parser.add_argument("--fcstm-dir", type=Path, required=True)
    parser.add_argument("--bounds", type=_bounds, default=(5, 20, 50))
    parser.add_argument("--wall-seconds", type=float)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.wall_seconds is not None and args.wall_seconds <= 0:
        parser.error("--wall-seconds must be positive")
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be positive")
    if args.output.exists():
        parser.error("--output must not already exist")

    formal_60_case = args.limit is None
    pair_ids, fcstm_by_stem, input_provenance, reasons = _preflight_assets(
        pairs_path=args.pairs,
        fcstm_dir=args.fcstm_dir,
        formal_60_case=formal_60_case,
    )
    if reasons:
        print(
            json.dumps(
                _failure("input_asset_preflight_failed", reasons),
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2

    if args.limit is not None:
        pair_ids = pair_ids[: args.limit]
        missing_smoke_fcstm = sorted(set(pair_ids) - set(fcstm_by_stem))
        if missing_smoke_fcstm:
            print(
                json.dumps(
                    _failure(
                        "input_asset_preflight_failed",
                        [f"fcstm_file_missing_for_smoke_pair_ids: {missing_smoke_fcstm}"],
                    ),
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return 2
    probe_contract = {
        "issue": "165",
        "formal_case_count": FORMAL_CASE_COUNT,
        "case_count_mode": "formal_60_case" if formal_60_case else "opt_in_smoke_limit",
        "limit": args.limit,
        "smoke_only": not formal_60_case,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        for pair_id in pair_ids:
            fcstm_file = fcstm_by_stem.get(pair_id)
            if fcstm_file is None:
                row = _failure(
                    "input_asset_preflight_failed",
                    [f"fcstm_file_missing_for_pair_id: {pair_id}"],
                )
                row.update(
                    {
                        "pair_id": pair_id,
                        "input_provenance": input_provenance,
                        "probe_contract": probe_contract,
                    }
                )
            else:
                for bound in args.bounds:
                    row = _row(
                        pair_id,
                        fcstm_file,
                        bound,
                        args.wall_seconds,
                        input_provenance,
                        probe_contract,
                    )
                    stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
                    stream.flush()
                    print(json.dumps(row, ensure_ascii=False, sort_keys=True))
                continue
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            stream.flush()
            print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
