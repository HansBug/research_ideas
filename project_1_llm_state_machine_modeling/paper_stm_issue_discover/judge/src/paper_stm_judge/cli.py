"""CLI for unified rejudging of existing X1v2 or evidence-discovery reports."""

from __future__ import annotations

import argparse
import hashlib
from importlib import resources as package_resources
import json
import os
import re
import subprocess
import tempfile
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from utils.stm_artifacts import FROZEN_PAIR_IDS

from .artifacts import (
    adapt_evidence_discovery_release,
    adapt_legacy_report_clusters,
    adapt_x1v2_record,
    build_artifact_closure,
    build_artifact_consistency_preflight,
    build_unified_input,
    load_expected_issues,
)
from .execution import ProcessStructuredRuntime
from .metrics import aggregate_outcomes
from .models import (
    RunFailureSummary,
    RunManifest,
    RunPairFailure,
    RunPairReceipt,
    RunSummary,
)
from .protocol import (
    JUDGE_ALGORITHM_VERSION,
    PROTOCOL_SHA256,
    PROTOCOL_VERSION,
    verify_snapshot,
)
from .runner import MAX_REPORTS_PER_BATCH, judge_pair


def _sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _write_model(path: Path, value) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value.model_dump_json(indent=2).encode("utf-8") + b"\n"
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return _sha256_bytes(payload)


def _git_value(repository_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ("git", *args), cwd=repository_root, text=True
    ).strip()


def _require_clean_commit(repository_root: Path) -> str:
    status = _git_value(
        repository_root,
        "status",
        "--porcelain",
        "--untracked-files=no",
    )
    if status:
        raise RuntimeError(
            "live semantic Judge requires a clean tracked commit; commit or isolate changes first"
        )
    return _git_value(repository_root, "rev-parse", "HEAD")


def _source_repository_root() -> Path | None:
    """Find a source checkout enclosing the Judge package, if this is one."""

    return next(
        (parent for parent in Path(__file__).resolve().parents if (parent / ".git").exists()),
        None,
    )


def _release_manifest_file(destination: str):
    """Map a release manifest destination to an installed executable package resource."""

    prefix = "src/paper_stm_judge/"
    if destination.startswith(prefix):
        return package_resources.files("paper_stm_judge").joinpath(
            destination.removeprefix(prefix)
        )
    prefix = "src/utils/"
    if destination.startswith(prefix):
        return package_resources.files("utils").joinpath(destination.removeprefix(prefix))
    return None


def _release_source_commit() -> str | None:
    """Verify installed Judge bytes against the builder manifest and return its commit."""

    try:
        manifest = json.loads(
            package_resources.files("paper_stm_judge")
            .joinpath("release_manifest.json")
            .read_text(encoding="utf-8")
        )
        source_commit = str(manifest["source_commit"])
        files = manifest["files"]
        if (
            manifest.get("schema_version") != "paper-stm-judge.release-manifest.v1"
            or not re.fullmatch(r"[0-9a-f]{40}", source_commit)
            or not isinstance(files, list)
        ):
            return None
        checked_files = 0
        for item in files:
            if not isinstance(item, dict):
                return None
            destination = item.get("destination")
            expected_hash = item.get("sha256")
            if not isinstance(destination, str) or not isinstance(expected_hash, str):
                return None
            resource = _release_manifest_file(destination)
            if resource is None:
                continue
            actual_hash = "sha256:" + hashlib.sha256(resource.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                return None
            checked_files += 1
        if checked_files == 0:
            return None
    except (KeyError, OSError, TypeError, ValueError):
        return None
    return source_commit


def _code_commit() -> str:
    """Read clean Git provenance or a verified installed-release provenance manifest."""

    repository_root = _source_repository_root()
    if repository_root is not None:
        return _require_clean_commit(repository_root)
    source_commit = _release_source_commit()
    if source_commit is None:
        raise RuntimeError(
            "live semantic Judge requires a clean source checkout or a valid installed release manifest"
        )
    return source_commit


def _source_path(
    source_format: str,
    source_root: Path,
    pair_id: str,
    round_no: int,
) -> Path:
    if source_format == "evidence_discovery_release":
        path = source_root / "method" / pair_id / f"round-{round_no}.json"
        if not path.is_file():
            raise FileNotFoundError(path)
        return path
    if source_format == "legacy_report_clusters":
        candidates = tuple(
            sorted(source_root.glob(f"run{round_no}/{pair_id}-*/record.json"))
        )
        if len(candidates) != 1:
            raise FileNotFoundError(
                f"expected exactly one historical cluster record for pair {pair_id}, "
                f"round {round_no} under {source_root}; actual={candidates}"
            )
        return candidates[0]
    candidates = tuple(sorted(source_root.glob(f"{pair_id}-*/record.json")))
    if len(candidates) != 1:
        raise FileNotFoundError(
            f"expected exactly one X1v2 record for pair {pair_id} under {source_root}; actual={candidates}"
        )
    return candidates[0]


def _source_root_hash(paths: tuple[Path, ...], source_root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(str(path.relative_to(source_root)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


_ROUND_IN_ORIGINAL_ID = re.compile(r"^\d{4}:r(\d+):")


def load_report_filter(raw_bytes: bytes) -> dict[str, frozenset[str]]:
    """Parse a local ``{pair_id: [original_report_id, ...]}`` allowlist.

    The allowlist restricts which already-published reports are judged; it is
    provenance-only and never enters the provider payload.
    """

    payload = json.loads(raw_bytes.decode("utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("report filter must be a JSON object mapping pair_id to report IDs")
    result: dict[str, frozenset[str]] = {}
    for pair_id, values in payload.items():
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise ValueError(f"report filter[{pair_id}] must be a list of original report IDs")
        for value in values:
            match = _ROUND_IN_ORIGINAL_ID.match(value)
            if match is None or value[:4] != pair_id:
                raise ValueError(
                    f"report filter[{pair_id}] contains an ID without a matching pair/round prefix: {value}"
                )
        result[str(pair_id)] = frozenset(values)
    return result


def round_filter_ids(
    report_filter: Mapping[str, frozenset[str]], pair_id: str, round_no: int
) -> frozenset[str]:
    """Return the allowlisted original IDs of one pair that belong to ``round_no``."""

    return frozenset(
        value
        for value in report_filter.get(pair_id, frozenset())
        if int(_ROUND_IN_ORIGINAL_ID.match(value).group(1)) == round_no  # type: ignore[union-attr]
    )


def apply_report_filter(reports, adapter_audit, allowed: frozenset[str]):
    """Keep only allowlisted reports while preserving anonymous IDs and the ID map."""

    known = {row.original_id for row in adapter_audit.report_id_map}
    missing = sorted(allowed - known)
    if missing:
        raise ValueError(
            f"report filter names IDs absent from the adapted source: {missing}"
        )
    keep = frozenset(
        row.anonymous_id for row in adapter_audit.report_id_map if row.original_id in allowed
    )
    filtered_reports = tuple(report for report in reports if report.report_id in keep)
    filtered_audit = adapter_audit.model_copy(
        update={
            "report_id_map": tuple(
                row for row in adapter_audit.report_id_map if row.anonymous_id in keep
            ),
            "reason": (
                adapter_audit.reason
                + f" A local report allowlist restricted judging to {len(keep)} of "
                f"{len(adapter_audit.report_id_map)} adapted report(s); anonymous IDs are unchanged."
            ),
        }
    )
    return filtered_reports, filtered_audit


def _ledger_l2_ids(ledger_path: Path) -> frozenset[str]:
    raw = json.loads(ledger_path.read_text(encoding="utf-8"))
    return frozenset(
        str(item["id"])
        for item in raw["items"].values()
        if item.get("D") in {"D1", "D2"} and item.get("L") == "L2"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument(
        "--source-format",
        choices=(
            "x1v2_record",
            "evidence_discovery_release",
            "legacy_report_clusters",
        ),
        required=True,
    )
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--profile", default="gpt-5.6-luna")
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--pair-id", action="append", dest="pair_ids")
    parser.add_argument(
        "--workers",
        type=int,
        default=16,
        help="Independent pair processes (default: 16).",
    )
    parser.add_argument("--transport-retries", type=int, default=8)
    parser.add_argument(
        "--validity-readings",
        type=int,
        default=2,
        help="Independent validity readings per report (frozen protocol: 2).",
    )
    parser.add_argument(
        "--validity-aggregation",
        choices=("arbitration", "majority"),
        default="arbitration",
        help="Final-certificate selection; 'majority' needs at least 3 readings and is a calibration experiment.",
    )
    parser.add_argument(
        "--k-closure",
        choices=("validity_first", "relation_first"),
        default="validity_first",
        help="K/N/I closure: 'relation_first' admits D0 / NOT_A_DEFECT_CLAIM reports to relation judging and closes a positive ledger relation as KNOWN (calibration experiment).",
    )
    parser.add_argument(
        "--report-filter",
        type=Path,
        default=None,
        help=(
            "Optional local JSON allowlist {pair_id: [original_report_id, ...]}. Only listed "
            "reports of the selected round are judged; pairs without listed reports for the round are skipped."
        ),
    )
    parser.add_argument("--allow-live", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.allow_live:
        raise SystemExit("real Judge calls require explicit --allow-live")
    verify_snapshot()
    code_commit = _code_commit()
    report_root = args.report_root.expanduser().resolve()
    ledger_path = args.ledger.expanduser().resolve()
    source_root = args.source_root.expanduser().resolve()
    pair_ids = tuple(args.pair_ids or FROZEN_PAIR_IDS)
    invalid_pairs = sorted(set(pair_ids) - set(FROZEN_PAIR_IDS))
    if invalid_pairs:
        raise ValueError(f"pair IDs outside frozen protocol: {invalid_pairs}")
    report_filter: dict[str, frozenset[str]] | None = None
    report_filter_path: Path | None = None
    report_filter_hash: str | None = None
    if args.report_filter is not None:
        report_filter_path = args.report_filter.expanduser().resolve()
        filter_bytes = report_filter_path.read_bytes()
        report_filter = load_report_filter(filter_bytes)
        report_filter_hash = _sha256_bytes(filter_bytes)
        pair_ids = tuple(
            pair_id
            for pair_id in pair_ids
            if round_filter_ids(report_filter, pair_id, args.round)
        )
        if not pair_ids:
            raise ValueError(
                f"report filter selects no report for round {args.round}: {report_filter_path}"
            )
    source_paths = tuple(
        _source_path(args.source_format, source_root, pair_id, args.round)
        for pair_id in pair_ids
    )
    artifact_root = args.output_dir.expanduser().resolve() / args.run_id
    if artifact_root.exists() and any(artifact_root.iterdir()):
        raise FileExistsError(
            f"output run directory already exists and is non-empty: {artifact_root}"
        )
    artifact_root.mkdir(parents=True, exist_ok=True)
    manifest = RunManifest(
        run_id=args.run_id,
        source_format=args.source_format,
        source_root=str(source_root),
        source_root_hash=_source_root_hash(source_paths, source_root),
        report_root=str(report_root),
        ledger_path=str(ledger_path),
        ledger_hash=_sha256_bytes(ledger_path.read_bytes()),
        protocol_version=PROTOCOL_VERSION,
        protocol_sha256=PROTOCOL_SHA256,
        judge_algorithm_version=JUDGE_ALGORITHM_VERSION,
        judge_code_commit=code_commit,
        model_profile=args.profile,
        selected_pair_ids=pair_ids,
        selected_rounds=(args.round,),
        workers=args.workers,
        max_reports_per_batch=MAX_REPORTS_PER_BATCH,
        transport_retries=args.transport_retries,
        validity_readings=args.validity_readings,
        validity_aggregation=args.validity_aggregation,
        k_closure=args.k_closure,
        report_filter_path=(
            str(report_filter_path) if report_filter_path is not None else None
        ),
        report_filter_hash=report_filter_hash,
        reason="Existing published reports are rejudged without regeneration through the single arm-neutral issue #195 entry point.",
        basis="Frozen CLI selection, source bytes, issue #195 snapshot, clean Judge commit, and one utils.llm profile.",
    )
    manifest_path = artifact_root / "run_manifest.json"
    manifest_hash = _write_model(manifest_path, manifest)
    runtime = ProcessStructuredRuntime(
        args.profile,
        artifact_root / "llm",
        workers=args.workers,
        transport_retries=args.transport_retries,
        streaming=True,
    )

    def run_one(pair_id: str, source_path: Path):
        expected, expected_map = load_expected_issues(ledger_path, pair_id)
        if args.source_format == "x1v2_record":
            reports, adapter_audit, round_no, adapted_pair_id = adapt_x1v2_record(
                source_path, expected_map
            )
        elif args.source_format == "evidence_discovery_release":
            reports, adapter_audit, round_no, adapted_pair_id = (
                adapt_evidence_discovery_release(source_path, expected_map)
            )
        else:
            reports, adapter_audit, round_no, adapted_pair_id = (
                adapt_legacy_report_clusters(source_path, expected_map)
            )
        if adapted_pair_id != pair_id or round_no != args.round:
            raise ValueError(
                f"source identity mismatch for {source_path}: expected pair={pair_id},round={args.round}; "
                f"actual pair={adapted_pair_id},round={round_no}"
            )
        if report_filter is not None:
            reports, adapter_audit = apply_report_filter(
                reports,
                adapter_audit,
                round_filter_ids(report_filter, pair_id, round_no),
            )
        preflight = build_artifact_consistency_preflight(report_root, pair_id)
        _write_model(
            artifact_root / "artifact_preflights" / f"{pair_id}.json",
            preflight,
        )
        if preflight.status.value != "PASS":
            raise RuntimeError(preflight.reason)
        closure = build_artifact_closure(report_root, pair_id, preflight=preflight)
        judge_input = build_unified_input(
            reports=reports,
            expected_issues=expected,
            artifact_closure=closure,
        )
        input_path = artifact_root / "inputs" / f"{pair_id}.json"
        _write_model(input_path, judge_input)
        _write_model(
            artifact_root / "adapter_audits" / f"{pair_id}.json",
            adapter_audit,
        )
        result = judge_pair(
            run_id=args.run_id,
            round_no=round_no,
            judge_input=judge_input,
            adapter_audit=adapter_audit,
            runtime=runtime,
            judge_code_commit=code_commit,
            validity_readings=args.validity_readings,
            validity_aggregation=args.validity_aggregation,
            k_closure=args.k_closure,
        )
        result_path = artifact_root / "pairs" / f"{pair_id}.json"
        result_hash = _write_model(result_path, result)
        receipt = RunPairReceipt(
            pair_id=pair_id,
            round=round_no,
            result_path=str(result_path),
            result_hash=result_hash,
            artifact_closure_hash=result.artifact_closure_hash,
            report_count=result.metrics.report_count,
            expected_count=result.metrics.expected_count,
        )
        return result, receipt

    results = []
    receipts = []
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_one, pair_id, path): (pair_id, path)
            for pair_id, path in zip(pair_ids, source_paths, strict=True)
        }
        for future in as_completed(futures):
            pair_id, source_path = futures[future]
            try:
                result, receipt = future.result()
            except Exception as exc:  # noqa: BLE001 - run boundary persists typed failures
                input_path = artifact_root / "inputs" / f"{pair_id}.json"
                adapter_path = artifact_root / "adapter_audits" / f"{pair_id}.json"
                call_receipts = tuple(getattr(exc, "call_receipts", ()))
                failure = RunPairFailure(
                    pair_id=pair_id,
                    round=args.round,
                    source_path=str(source_path),
                    input_path=str(input_path) if input_path.is_file() else None,
                    adapter_audit_path=(
                        str(adapter_path) if adapter_path.is_file() else None
                    ),
                    llm_artifact_path=str(artifact_root / "llm" / pair_id),
                    error_type=type(exc).__name__,
                    error_message=str(exc) or repr(exc),
                    call_receipts=call_receipts,
                    total_judge_cost_usd=sum(call.cost_usd for call in call_receipts),
                    cost_eligible=all(call.cost_eligible for call in call_receipts),
                    reason="The pair did not complete two validated readings and any required arbitration, so it is excluded from aggregation.",
                    basis="Captured worker exception plus preserved unified input, adapter audit, and public runtime artifacts when available.",
                )
                _write_model(artifact_root / "failures" / f"{pair_id}.json", failure)
                failures.append(failure)
                print(
                    json.dumps(
                        {
                            "pair_id": pair_id,
                            "status": "failed",
                            "error_type": failure.error_type,
                            "error_message": failure.error_message,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                continue
            results.append(result)
            receipts.append(receipt)
            print(
                json.dumps(
                    {
                        "pair_id": pair_id,
                        "hit": result.metrics.full_hit_count,
                        "expected": result.metrics.expected_count,
                        "K": result.metrics.valid_known_count,
                        "N": result.metrics.valid_novel_count,
                        "I": result.metrics.invalid_count,
                        "conflicts": len(result.conflicts),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    runtime.close()
    if failures:
        receipts.sort(key=lambda item: item.pair_id)
        failures.sort(key=lambda item: item.pair_id)
        failure_summary = RunFailureSummary(
            run_id=args.run_id,
            manifest_hash=manifest_hash,
            completed_pair_receipts=tuple(receipts),
            failures=tuple(failures),
            total_judge_cost_usd=(
                sum(
                    call.cost_usd for result in results for call in result.call_receipts
                )
                + sum(failure.total_judge_cost_usd for failure in failures)
            ),
            cost_eligible=(
                all(
                    call.cost_eligible
                    for result in results
                    for call in result.call_receipts
                )
                and all(failure.cost_eligible for failure in failures)
            ),
            reason=f"{len(failures)} selected pair(s) failed; no completed summary or partial score was emitted.",
            basis=f"{PROTOCOL_VERSION}; {JUDGE_ALGORITHM_VERSION}; typed pair failures and no-partial-summary policy",
        )
        _write_model(artifact_root / "failure_summary.json", failure_summary)
        print(failure_summary.model_dump_json(indent=2), flush=True)
        return 1
    results.sort(key=lambda item: item.pair_id)
    receipts.sort(key=lambda item: item.pair_id)
    overall = aggregate_outcomes(
        (
            (result.pair_id, report)
            for result in results
            for report in result.report_outcomes
        ),
        (
            (result.pair_id, expected)
            for result in results
            for expected in result.expected_outcomes
        ),
    )
    l2_ids = _ledger_l2_ids(ledger_path)
    l2_outcomes = [
        expected
        for result in results
        for expected in result.expected_outcomes
        if expected.ledger_id in l2_ids
    ]
    total_cost = sum(
        call.cost_usd for result in results for call in result.call_receipts
    )
    summary = RunSummary(
        run_id=args.run_id,
        manifest_hash=manifest_hash,
        pair_receipts=tuple(receipts),
        overall=overall,
        l2_expected_count=len(l2_outcomes),
        l2_full_hit_count=sum(item.hit for item in l2_outcomes),
        l2_hit_rate=(
            sum(item.hit for item in l2_outcomes) / len(l2_outcomes)
            if l2_outcomes
            else 0.0
        ),
        total_judge_cost_usd=total_cost,
        cost_eligible=all(
            call.cost_eligible for result in results for call in result.call_receipts
        ),
        reason="Every selected report and expected issue was judged twice, conflicts were arbitrated, and final metrics were deterministically recomputed.",
        basis=f"{PROTOCOL_VERSION}; {JUDGE_ALGORITHM_VERSION}; {len(results)} complete PairJudgeResult artifacts",
    )
    _write_model(artifact_root / "summary.json", summary)
    print(summary.model_dump_json(indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
