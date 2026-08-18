"""Aggregate the Luna full-matrix run without lexical semantic shortcuts."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from utils.llm import LLMPricing, estimate_usage_cost_usd, load_llm_registry


CELLS = (
    "method_run1",
    "method_run2",
    "method_run3",
    "baseline_run1",
    "baseline_run2",
    "baseline_run3",
)
METHOD_CELLS = CELLS[:3]
BASELINE_CELLS = CELLS[3:]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def failure_class(observations: list[dict[str, Any]]) -> str:
    phases: list[str] = []
    for observation in observations:
        for attempt in observation.get("attempts", []):
            phase = attempt.get("failure_phase")
            if isinstance(phase, str) and phase != "none":
                phases.append(phase)
    if phases and all(phase in {"provider_response", "transport"} for phase in phases):
        return "provider_failure"
    if phases and all(phase.startswith("structured_") for phase in phases):
        return "schema_invalid"
    if phases:
        return "mixed_failure"
    return "unknown_failure"


def usage_cost(usage: dict[str, Any], pricing: LLMPricing) -> float:
    result = estimate_usage_cost_usd(usage, pricing)
    return float(result["total_usd"] or 0.0)


def attempt_cost(attempt: dict[str, Any], pricing: LLMPricing) -> float:
    if attempt.get("billing_disposition") == "provider_error_retry_exempt":
        return 0.0
    return usage_cost(attempt.get("usage") or {}, pricing)


def method_cost(pair_dir: Path, pricing: LLMPricing) -> tuple[float, int, int, int]:
    final_path = pair_dir / "record.json"
    final = read_json(final_path) if final_path.exists() else {}
    observations = final.get("llm_observations", [])
    observation_sources = [final_path] if observations else []
    if not observations:
        observation_sources.extend(sorted((pair_dir / "stages").glob("*/record.json")))
    seen_calls: set[str] = set()
    total = 0.0
    calls = 0
    attempts = 0
    provider_exempt = 0
    for source in observation_sources:
        payload = read_json(source)
        for observation in payload.get("llm_observations", []):
            call_id = observation.get("llm_call_id")
            if isinstance(call_id, str) and call_id in seen_calls:
                continue
            if isinstance(call_id, str):
                seen_calls.add(call_id)
            calls += 1
            for attempt in observation.get("attempts", []):
                attempts += 1
                if attempt.get("billing_disposition") == "provider_error_retry_exempt":
                    provider_exempt += 1
                total += attempt_cost(attempt, pricing)
    if final.get("status") == "failed" and final.get("failure"):
        category = final["failure"].get("class")
        if category == "provider_or_schema":
            category = failure_class(observations)
        failure = {"class": category or failure_class(observations)}
    else:
        failure = None
    return total, calls, attempts, provider_exempt


def record_failure_category(record: dict[str, Any], pair_dir: Path | None = None) -> str:
    failure = record.get("failure") or {}
    category = failure.get("class")
    if category != "provider_or_schema":
        return str(category or failure_class(record.get("llm_observations") or []))
    observations = record.get("llm_observations") or []
    if pair_dir is not None and not observations:
        for source in sorted((pair_dir / "stages").glob("*/record.json")):
            payload = read_json(source)
            observations.extend(payload.get("llm_observations") or [])
    return failure_class(observations)


def baseline_cost(record: dict[str, Any], pricing: LLMPricing) -> float:
    usage = record.get("usage") or {}
    return usage_cost(usage, pricing)


def judge_cost(judge_root: Path, pricing: LLMPricing) -> dict[str, Any]:
    """Sum judge attempts from per-pair manifests without reading prompt text."""

    total = 0.0
    calls = 0
    attempts = 0
    provider_exempt = 0
    manifests: list[str] = []
    seen_calls: set[str] = set()
    for manifest_path in sorted(judge_root.glob("**/manifest.json")):
        manifest = read_json(manifest_path)
        manifests.append(str(manifest_path))
        for row in manifest.get("pairs", []):
            for observation in row.get("observations", []):
                call_id = observation.get("llm_call_id")
                if isinstance(call_id, str) and call_id in seen_calls:
                    continue
                if isinstance(call_id, str):
                    seen_calls.add(call_id)
                calls += 1
                for attempt in observation.get("attempts", []):
                    attempts += 1
                    if attempt.get("billing_disposition") == "provider_error_retry_exempt":
                        provider_exempt += 1
                    total += attempt_cost(attempt, pricing)
    return {
        "cost_usd": total,
        "llm_calls": calls,
        "attempts": attempts,
        "provider_retry_exempt_attempts": provider_exempt,
        "manifest_paths": manifests,
    }


def cell_status(root: Path, arm: str, pair: str, run: int) -> tuple[str, dict[str, Any]]:
    path = root / f"run{run}" / f"{pair}-luna" / "record.json"
    if not path.exists():
        return "missing", {}
    record = read_json(path)
    return str(record.get("status") or "ok"), record


def load_judgements(judge_root: Path, pairs: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for pair in pairs:
        candidates = [path for path in judge_root.glob(f"**/{pair}.json") if path.is_file()]
        if candidates:
            result[pair] = read_json(max(candidates, key=lambda path: path.stat().st_mtime_ns))
    return result


def ledger_metrics(
    pair: str,
    ledger: list[dict[str, Any]],
    judgement: dict[str, Any] | None,
    statuses: dict[str, str],
) -> dict[str, Any]:
    assessments = {
        row["ledger_id"]: row for row in (judgement or {}).get("judgement", {}).get("ledger_assessments", [])
    }
    per_cell: dict[str, list[bool]] = {cell: [] for cell in CELLS}
    per_entry: list[dict[str, Any]] = []
    for entry in ledger:
        assessment = assessments.get(entry["id"])
        row: dict[str, Any] = {"ledger_id": entry["id"], "D": entry["D"], "L": entry["L"]}
        for cell in CELLS:
            hit = False
            if assessment is not None and statuses.get(cell) == "ok":
                hit = bool(getattr_dict(assessment, cell).get("hit", False))
            row[cell] = hit
            per_cell[cell].append(hit)
        per_entry.append(row)
    return {"per_entry": per_entry, "per_cell": per_cell}


def getattr_dict(value: dict[str, Any], key: str) -> dict[str, Any]:
    data = value.get(key, {})
    return data if isinstance(data, dict) else {}


def summarize_hits(rows: list[dict[str, Any]], cells: tuple[str, ...], subset: set[str] | None = None) -> dict[str, Any]:
    selected = [row for row in rows if subset is None or row["ledger_id"] in subset]
    denominator = len(selected) * len(cells)
    per_position = sum(sum(bool(row[cell]) for cell in cells) for row in selected)
    any_count = sum(any(bool(row[cell]) for cell in cells) for row in selected)
    all_count = sum(all(bool(row[cell]) for cell in cells) for row in selected)
    return {
        "entries": len(selected),
        "positions": denominator,
        "hit_at_1": per_position,
        "hit_at_1_rate": per_position / denominator if denominator else None,
        "hit_at_3": any_count,
        "hit_at_3_rate": any_count / len(selected) if selected else None,
        "hit_at_all": all_count,
        "hit_at_all_rate": all_count / len(selected) if selected else None,
    }


def emission_metrics(judgements: dict[str, dict[str, Any]]) -> dict[str, Any]:
    counts = Counter()
    for result in judgements.values():
        for row in result.get("judgement", {}).get("emission_assessments", []):
            arm = str(row.get("cell", "")).split("_", 1)[0]
            counts[f"{arm}_emitted"] += 1
            if row.get("false_positive") is True:
                counts[f"{arm}_false_positive"] += 1
    output: dict[str, Any] = {}
    for arm in ("method", "baseline"):
        emitted = counts[f"{arm}_emitted"]
        false_positive = counts[f"{arm}_false_positive"]
        output[arm] = {
            "emitted": emitted,
            "false_positive": false_positive,
            "precision": (emitted - false_positive) / emitted if emitted else None,
        }
    return output


def method_quality(method_root: Path, pairs: list[str], pricing: LLMPricing) -> dict[str, Any]:
    counters = Counter()
    costs = 0.0
    calls = attempts = provider_exempt = 0
    per_pair: dict[str, Any] = {}
    for pair in pairs:
        path = method_root / "run1" / f"{pair}-luna" / "record.json"
        records = []
        for run in (1, 2, 3):
            p = method_root / f"run{run}" / f"{pair}-luna" / "record.json"
            if p.exists():
                records.append(read_json(p))
        pair_cost = 0.0
        pair_calls = pair_attempts = pair_exempt = 0
        for run in (1, 2, 3):
            pdir = method_root / f"run{run}" / f"{pair}-luna"
            if (pdir / "record.json").exists():
                c, n, a, e = method_cost(pdir, pricing)
                pair_cost += c
                pair_calls += n
                pair_attempts += a
                pair_exempt += e
        costs += pair_cost
        calls += pair_calls
        attempts += pair_attempts
        provider_exempt += pair_exempt
        for run, record in enumerate(records, start=1):
            if record.get("status") == "failed":
                pdir = method_root / f"run{run}" / f"{pair}-luna"
                counters[f"failure:{record_failure_category(record, pdir)}"] += 1
                continue
            for finding in record.get("finding_records", []):
                counters[f"W:{finding.get('witness_level', 'unknown')}"] += 1
                counters[f"D:{(finding.get('d_decision') or {}).get('d_level', 'unknown')}"] += 1
                counters[f"L:{finding.get('l_level', 'unknown')}"] += 1
            counters["accepted"] += len(record.get("accepted_report_issues", []))
            counters["confirmed"] += len(record.get("confirmed_report_issues", []))
        per_pair[pair] = {
            "cost_usd": pair_cost,
            "llm_calls": pair_calls,
            "attempts": pair_attempts,
            "provider_retry_exempt_attempts": pair_exempt,
        }
    return {
        "counts": dict(counters),
        "cost_usd": costs,
        "llm_calls": calls,
        "attempts": attempts,
        "provider_retry_exempt_attempts": provider_exempt,
        "per_pair": per_pair,
    }


def baseline_quality(baseline_root: Path, pairs: list[str], pricing: LLMPricing) -> dict[str, Any]:
    total = 0.0
    per_pair: dict[str, Any] = {}
    failures = Counter()
    for pair in pairs:
        pair_cost = 0.0
        for run in (1, 2, 3):
            path = baseline_root / f"run{run}" / f"{pair}-luna" / "record.json"
            if not path.exists():
                failures["missing"] += 1
                continue
            record = read_json(path)
            pair_cost += baseline_cost(record, pricing)
            if record.get("status") != "ok":
                failures[str(record.get("failure_class") or "failed")] += 1
        total += pair_cost
        per_pair[pair] = {"cost_usd": pair_cost}
    return {"cost_usd": total, "failures": dict(failures), "per_pair": per_pair}


def markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def build_report(metrics: dict[str, Any]) -> str:
    overall = metrics["coverage"]
    method = overall["method"]
    baseline = overall["baseline"]
    lines = [
        "# Luna 全量 x3 语义审计报告",
        "",
        "本报告比较 gpt-5.6-luna 下的新方法 v26-dnorm 与 X1v2 baseline，运行矩阵为 54 个非 NL04 pair、每臂每 pair 三轮；命中由独立语义评审依据同一位置与同一性质判定，不使用关键词、字符串包含、编辑距离、embedding 或其他词法捷径。",
        "",
        "## 方法侧覆盖",
        "",
        markdown_table(
            [
                ["整体", str(method["overall"]["entries"]), f"{method['overall']['hit_at_1']}/{method['overall']['positions']}", f"{method['overall']['hit_at_3']}/{method['overall']['entries']}", f"{method['overall']['hit_at_all']}/{method['overall']['entries']}"],
                ["L2", str(method["L2"]["entries"]), f"{method['L2']['hit_at_1']}/{method['L2']['positions']}", f"{method['L2']['hit_at_3']}/{method['L2']['entries']}", f"{method['L2']['hit_at_all']}/{method['L2']['entries']}"],
                ["D2×L2", str(method["D2xL2"]["entries"]), f"{method['D2xL2']['hit_at_1']}/{method['D2xL2']['positions']}", f"{method['D2xL2']['hit_at_3']}/{method['D2xL2']['entries']}", f"{method['D2xL2']['hit_at_all']}/{method['D2xL2']['entries']}"],
            ],
            ["子集", "条目数", "hit@1", "hit@3", "hit@all"],
        ),
        "",
        "## X1v2 baseline 覆盖",
        "",
        markdown_table(
            [
                ["整体", str(baseline["overall"]["entries"]), f"{baseline['overall']['hit_at_1']}/{baseline['overall']['positions']}", f"{baseline['overall']['hit_at_3']}/{baseline['overall']['entries']}", f"{baseline['overall']['hit_at_all']}/{baseline['overall']['entries']}"],
                ["L2", str(baseline["L2"]["entries"]), f"{baseline['L2']['hit_at_1']}/{baseline['L2']['positions']}", f"{baseline['L2']['hit_at_3']}/{baseline['L2']['entries']}", f"{baseline['L2']['hit_at_all']}/{baseline['L2']['entries']}"],
                ["D2×L2", str(baseline["D2xL2"]["entries"]), f"{baseline['D2xL2']['hit_at_1']}/{baseline['D2xL2']['positions']}", f"{baseline['D2xL2']['hit_at_3']}/{baseline['D2xL2']['entries']}", f"{baseline['D2xL2']['hit_at_all']}/{baseline['D2xL2']['entries']}"],
            ],
            ["子集", "条目数", "hit@1", "hit@3", "hit@all"],
        ),
        "",
        "## 质量、错误与成本",
        "",
        f"方法侧 finding 的 W/D/L 分布、accepted/confirmed 数、schema/provider/local failure 数以及每次 attempt 的计费明细见 `metrics.json`；provider retry exemption 只统计 `billing_disposition=provider_error_retry_exempt`，所有其他 attempt 都计费。方法总成本为 `${metrics['cost']['method_usd']:.6f}`，baseline 总成本为 `${metrics['cost']['baseline_usd']:.6f}`，倍率为 `{metrics['cost']['multiplier']:.2f}x`。",
        "",
        "## 逐条台账对照",
        "",
        "方法与 baseline 的逐条台账表物理分开，分别见 `ledger_method.md` 与 `ledger_baseline.md`；每个单元格是三轮中该轮的语义命中结果，失败格按保守规则记为 `❌`。",
        "",
        "## 可复现边界",
        "",
        "原始完整运行目录位于本机 `runs/paper1/luna-full-x3-20260819-v1/`，本目录的 `audit_index.json` 保存每个 raw record 的 SHA-256、状态、失败分类和紧凑审计摘要路径；原始 raw prompt/response 体积过大且包含重复中间阶段，不复制进 git。",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-root", type=Path, required=True)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--judge-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--profile", default="gpt-5.6-luna")
    args = parser.parse_args()
    profile = load_llm_registry().require(args.profile)
    if profile.pricing is None:
        raise ValueError(f"profile {args.profile!r} has no configured pricing")
    pricing = profile.pricing
    ledger_data = read_json(args.ledger)["items"]
    pairs = sorted(
        p.name[:4]
        for p in (args.method_root / "run1").glob("[0-9][0-9][0-9][0-9]-luna")
        if not p.name.endswith("8")
    )
    ledger_by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in ledger_data.values():
        ledger_by_pair[str(item["pair"])].append(item)
    for pair in pairs:
        ledger_by_pair.setdefault(pair, [])
    pairs = sorted(set(pairs) | set(ledger_by_pair))
    judgements = load_judgements(args.judge_root, pairs)
    coverage_rows: dict[str, list[dict[str, Any]]] = {"method": [], "baseline": []}
    audit_index: list[dict[str, Any]] = []
    for pair in pairs:
        statuses: dict[str, str] = {}
        for arm, root in (("method", args.method_root), ("baseline", args.baseline_root)):
            for run in (1, 2, 3):
                status, _ = cell_status(root, arm, pair, run)
                statuses[f"{arm}_run{run}"] = status
                raw = root / f"run{run}" / f"{pair}-luna" / "record.json"
                if raw.exists():
                    audit_index.append({"arm": arm, "run": run, "pair": pair, "status": status, "raw_record": str(raw), "raw_sha256": sha256(raw)})
        pair_metrics = ledger_metrics(pair, ledger_by_pair[pair], judgements.get(pair), statuses)
        for arm, cells in (("method", METHOD_CELLS), ("baseline", BASELINE_CELLS)):
            rows = []
            for row in pair_metrics["per_entry"]:
                rows.append({"ledger_id": row["ledger_id"], "D": row["D"], "L": row["L"], **{cell: row[cell] for cell in cells}})
            coverage_rows[arm].extend(rows)
    ledger_rows = {"method": [], "baseline": []}
    for arm, cells in (("method", METHOD_CELLS), ("baseline", BASELINE_CELLS)):
        for row in coverage_rows[arm]:
            marks = ["✅" if row[cell] else "❌" for cell in cells]
            ledger_rows[arm].append([row["ledger_id"], row["D"], row["L"], *marks])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "ledger_method.md").write_text(markdown_table(ledger_rows["method"], ["台账", "D", "L", "run1", "run2", "run3"]) + "\n", encoding="utf-8")
    (args.output_dir / "ledger_baseline.md").write_text(markdown_table(ledger_rows["baseline"], ["台账", "D", "L", "run1", "run2", "run3"]) + "\n", encoding="utf-8")
    method_quality_data = method_quality(args.method_root, pairs, pricing)
    baseline_quality_data = baseline_quality(args.baseline_root, pairs, pricing)
    judge_quality_data = judge_cost(args.judge_root, pricing)
    method_rows = coverage_rows["method"]
    baseline_rows = coverage_rows["baseline"]
    method_ids = {row["ledger_id"] for row in method_rows}
    baseline_ids = {row["ledger_id"] for row in baseline_rows}
    method_ledger = {item["id"]: item for item in ledger_data.values()}
    coverage = {
        "method": {
            "overall": summarize_hits(method_rows, METHOD_CELLS),
            "L2": summarize_hits(method_rows, METHOD_CELLS, {key for key, value in method_ledger.items() if value["L"] == "L2"}),
            "D2xL2": summarize_hits(method_rows, METHOD_CELLS, {key for key, value in method_ledger.items() if value["D"] == "D2" and value["L"] == "L2"}),
        },
        "baseline": {
            "overall": summarize_hits(baseline_rows, BASELINE_CELLS),
            "L2": summarize_hits(baseline_rows, BASELINE_CELLS, {key for key, value in method_ledger.items() if value["L"] == "L2"}),
            "D2xL2": summarize_hits(baseline_rows, BASELINE_CELLS, {key for key, value in method_ledger.items() if value["D"] == "D2" and value["L"] == "L2"}),
        },
    }
    metrics = {
        "schema": "paper1.luna_full_x3_semantic_audit.v1",
        "pairs": pairs,
        "ledger_entries": len(ledger_data),
        "coverage": coverage,
        "emissions": emission_metrics(judgements),
        "method_quality": method_quality_data,
        "baseline_quality": baseline_quality_data,
        "judge_quality": judge_quality_data,
        "cost": {
            "method_usd": method_quality_data["cost_usd"],
            "baseline_usd": baseline_quality_data["cost_usd"],
            "judge_usd": judge_quality_data["cost_usd"],
            "method_plus_judge_usd": method_quality_data["cost_usd"] + judge_quality_data["cost_usd"],
            "research_total_usd": method_quality_data["cost_usd"] + baseline_quality_data["cost_usd"] + judge_quality_data["cost_usd"],
            "multiplier": method_quality_data["cost_usd"] / baseline_quality_data["cost_usd"] if baseline_quality_data["cost_usd"] else None,
            "profile": args.profile,
            "rate_card": pricing.model_dump(mode="json"),
        },
        "judgement_status": {pair: result.get("status") for pair, result in judgements.items()},
        "audit_index": audit_index,
    }
    (args.output_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "REPORT.md").write_text(build_report(metrics), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
