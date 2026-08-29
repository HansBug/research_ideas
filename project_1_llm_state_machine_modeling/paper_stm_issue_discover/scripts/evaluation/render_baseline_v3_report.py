#!/usr/bin/env python3
"""Render the paired publication report using current v2 and baseline v3 JSON."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    """Load one canonical JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(path)
    return value


def show(metric: dict[str, Any]) -> str:
    """Render n/N and percentage, preserving not-applicable metrics."""
    if metric.get("status") == "not_applicable":
        return "not_applicable"
    percentage = metric.get("percentage")
    return f"{metric['numerator']}/{metric['denominator']} = {percentage * 100:.2f}%" if percentage is not None else "n/a"


def difference(left: dict[str, Any], right: dict[str, Any]) -> str:
    """Render current-minus-baseline numerator and percentage-point delta."""
    lp, rp = left.get("percentage"), right.get("percentage")
    pp = "n/a" if lp is None or rp is None else f"{(lp-rp)*100:+.2f} pp"
    return f"{left['numerator']-right['numerator']:+d}; {pp}"


def metric_row(label: str, current: dict[str, Any], baseline: dict[str, Any]) -> str:
    """Build one paired metric row."""
    d = difference(current, baseline) if "numerator" in current and "numerator" in baseline else "n/a"
    return f"| {label} | `{show(current)}` | `{show(baseline)}` | `{d}` |"


def report_count_row(label: str, current_n: int, baseline_n: int, current_d: int, baseline_d: int) -> str:
    """Build one paired count row."""
    c = {"numerator": current_n, "denominator": current_d, "percentage": current_n/current_d if current_d else None}
    b = {"numerator": baseline_n, "denominator": baseline_d, "percentage": baseline_n/baseline_d if baseline_d else None}
    return metric_row(label, c, b)


def main() -> None:
    """Render all primary report numbers from canonical summaries."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    old_summary = load(archive / "derived/manual_adjudication_v2/summary.json")
    current = old_summary["sides"]["v60_current"]
    baseline_summary = load(archive / "derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json")
    baseline = baseline_summary["metrics"]
    decisions = load(archive / "derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json")["decisions"]
    predicate_audit = load(archive / "derived/manual_adjudication_v2/predicate_witness_audit.json")["sides"]["v60_current"]
    review_log = load(archive / "derived/manual_adjudication_v3_baseline_ni/review_log_v3.json")
    arbitration_log = load(archive / "derived/manual_adjudication_v3_baseline_ni/reviews/arbitration_log_v3.json")
    # The ledger cardinality is read from the canonical inventory/reference, not a result target.
    ledger = load(archive / "reference/ledger.json")["items"]
    expected = len(ledger)

    def current_ledger(name: str) -> dict[str, Any]:
        ledger_based = current["ledger_based"]
        if name == "precision":
            numerator = ledger_based["K_hit"]["numerator"] + ledger_based["N_group"]["numerator"]
            denominator = ledger_based["composition_denominator"]
            return {"numerator": numerator, "denominator": denominator, "percentage": numerator / denominator}
        if name == "fp_rate":
            numerator = ledger_based["I_group"]["numerator"]
            denominator = ledger_based["composition_denominator"]
            return {"numerator": numerator, "denominator": denominator, "percentage": numerator / denominator}
        return ledger_based[name]

    def baseline_ledger(name: str) -> dict[str, Any]:
        mapping = {"precision": "ledger_group_based_precision", "fp_rate": "ledger_group_based_fp_rate"}
        return baseline[mapping[name]]

    lines = [
        "# v60/current 与 X1v2 baseline 的最终人工监督评测",
        "",
        "> 主结果使用 v60/current 的既有最终人工监督裁定与 X1v2 baseline v3 对全部非 K 报告的逐条人工重审。v2 是历史输入；v3 不覆盖或修改 frozen K、raw、current、method 或 Judge 制品。",
        "",
        "## 口径与范围",
        "",
        "协议版本为 `issue-189-195-baseline-ni-v3`，按 issue #189/#195 的事实、D/A、expected relation 和机械 K/N/I 闭合执行。顺序固定为：作者源事实 -> D2/D1/D0/A0 -> validity -> 全部 145 个 expected relation -> K/N/I。",
        "",
        "v3 只重审 baseline 原非 K 的 233 条；279 条已有 K 从 v2 按字节内容/字段快照冻结复制。D0/A0 均为 I，A0 仅使用 `FALSE_POSITIVE`；W、predicate、Judge 输出和 ledger 缺失不能决定 validity。",
        "",
        f"raw inventory 与 ledger 均由归档重新读取：current `{current['report_count']}` 条、baseline `{baseline['report_count']}` 条、expected `{expected}` 条。结构化来源是 [current v2 summary](../derived/manual_adjudication_v2/summary.json)、[baseline v3 summary](../derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json) 和 [v3 manifest](../derived/manual_adjudication_v3_baseline_ni/publication_manifest_v3_baseline_ni.json)。",
        "",
        "## 主结果",
        "",
        "delta 为 v60/current 减 X1v2 baseline；分号前是 numerator 差，分号后是百分点差。hit@1 的分母是 145 个 expected × 3 个 round，即 435 个 expected-round units；不是单轮的 145。",
        "",
        "| 指标 | v60/current | X1v2 baseline | delta (n; pp) |",
        "|---|---:|---:|---:|",
        metric_row("overall hit@1 / FULL", current["hit_at_1_full"], baseline["hit_at_1_full"]),
        metric_row("L2 hit@1 / FULL", current["l2_hit_at_1_full"], baseline["l2_hit_at_1_full"]),
        metric_row("hit@3", current["hit_at_3_full"], baseline["hit_at_3_full"]),
        metric_row("hit@all", current["hit_at_all_full"], baseline["hit_at_all_full"]),
        metric_row("L2 hit@3", current["l2_hit_at_3_full"], baseline["l2_hit_at_3_full"]),
        metric_row("L2 hit@all", current["l2_hit_at_all_full"], baseline["l2_hit_at_all_full"]),
        metric_row("supported coverage, round units", current["supported_coverage_round_units"], baseline["supported_coverage_round_units"]),
        metric_row("supported coverage, unique expected", current["supported_coverage_unique_expected"], baseline["supported_coverage_unique_expected"]),
        metric_row("report-based precision", current["report_based_precision"], baseline["report_based_precision"]),
        metric_row("report-based FP rate", current["report_based_fp_rate"], baseline["report_based_fp_rate"]),
        metric_row("partial_only_known_report", current["partial_only_known_report"], baseline["partial_only_known_report"]),
        metric_row("partial_only_known_expected", current["partial_only_known_expected"], baseline["partial_only_known_expected"]),
        metric_row("ledger K_hit", current_ledger("K_hit"), {"numerator": baseline["ledger_group_composition"]["K_hit"], "denominator": expected, "percentage": baseline["ledger_group_composition"]["K_hit"]/expected}),
        metric_row("ledger/group precision", current_ledger("precision"), baseline_ledger("precision")),
        metric_row("ledger/group FP rate", current_ledger("fp_rate"), baseline_ledger("fp_rate")),
        metric_row("FULL-hit max W2", current["hit_max_witness"]["W2"], baseline["hit_max_witness"]["W1"] if False else baseline["hit_max_witness"]["W2"]),
        metric_row("FULL-hit max W1", current["hit_max_witness"]["W1"], baseline["hit_max_witness"]["W1"]),
        metric_row("FULL-hit max W0", current["hit_max_witness"]["W0"], baseline["hit_max_witness"]["W0"]),
        metric_row("W2 / all expected", current["w2_all_expected"], baseline["w2_all_expected"]),
        "",
        f"baseline ledger/group composition 为 `K_hit={baseline['ledger_group_composition']['K_hit']}`、`N_group={baseline['ledger_group_composition']['N_group']}`、`I_group={baseline['ledger_group_composition']['I_group']}`，分母为三者之和；I group 仅为 invalid diagnostic cluster，不是真实缺陷。L2 ledger precision 与 baseline predicate usage 均为 `not_applicable`，并保留 reason。",
        "",
        "## D/A 与 K/N/I",
        "",
        "| 类别 | v60/current | X1v2 baseline | delta (n; pp) |",
        "|---|---:|---:|---:|",
    ]
    for key in ("D2", "D1", "D0", "A0"):
        lines.append(report_count_row(key, current["decision_counts"].get(key, 0), baseline["decision_counts"].get(key, 0), current["report_count"], baseline["report_count"]))
    for key in ("K", "N", "I"):
        lines.append(report_count_row(key, current["kni_counts"].get(key, 0), baseline["kni_counts"].get(key, 0), current["report_count"], baseline["report_count"]))
    for key in ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH"):
        # The frozen v2 summary stores relation counts as integers; v3 stores
        # the same counts as Metric objects. Normalize only at this renderer
        # boundary so neither canonical input is rewritten.
        current_relation_count = current["relation_counts"][key]
        baseline_relation_count = baseline["relation_counts"][key]
        if isinstance(current_relation_count, dict):
            current_relation_count = current_relation_count["numerator"]
        if isinstance(baseline_relation_count, dict):
            baseline_relation_count = baseline_relation_count["numerator"]
        lines.append(report_count_row(key, current_relation_count, baseline_relation_count, current["report_count"] * expected, baseline["report_count"] * expected))
    lines += [
        "",
        "`PARTIAL_MATCH` 进入 supported coverage，不进入主 FULL hit；只有 INVALID/I 进入 report-based FP。K hit 在 expected ID 层去重，N 以 substantive group 展示，I cluster 独立命名。",
        "",
        "## W 与 predicate",
        "",
        "W0/W1/W2 是独立证据轴，不参与 validity、relation、hit 或 FP。W2 只接受报告自带 executable object、typed input、精确 artifact hash、terminal result 和原始 receipt；后验 Judge 不能升级 baseline W。",
        "",
        "| finding-level W | v60/current | X1v2 baseline |",
        "|---|---:|---:|",
    ]
    for level in ("W0", "W1", "W2"):
        lines.append(f"| {level} | `{current['witness_counts'].get(level, 0)}/{current['report_count']}` | `{baseline['witness_counts'].get(level, 0)}/{baseline['report_count']}` |")
    lines += [
        "",
        "| FULL-hit witness | v60/current | X1v2 baseline |",
        "|---|---:|---:|",
    ]
    for level in ("W2", "W1", "W0"):
        lines.append(f"| maximum {level} | `{show(current['hit_max_witness'][level])}` | `{show(baseline['hit_max_witness'][level])}` |")
    lines += [
        "",
        f"W-on-hits 的分母分别是 current `{current['hit_at_1_full']['numerator']}` 与 baseline `{baseline['hit_at_1_full']['numerator']}` 个 FULL expected-round units；W2/all-expected 的分母固定为 `{baseline['w2_all_expected']['denominator']}`，不能互换。",
        "",
        f"current predicate usage 见 [predicate_witness_audit.json](../derived/manual_adjudication_v2/predicate_witness_audit.json)，planned scope 为 `{predicate_audit['planned_scope']['scope_id']}`、`{predicate_audit['planned_scope']['count']}` 个 ID。全部 usage 与 FULL-hit supporting usage 分母分开，receipt 缺失/失败仍留在 usage 分母；baseline predicate usage 为 `not_applicable`，不是零。",
        "",
        "| predicate | planned | report-bound | precise | receipt | all usage W0/W1/W2 | FULL-hit usage W0/W1/W2 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in predicate_audit["predicate_rows"]:
        all_w = f"{row['all_usage_w0']}/{row['all_usage_w1']}/{row['all_usage_w2']} / {row['all_usage_denominator']}"
        hit_w = f"{row['full_hit_supporting_w0']}/{row['full_hit_supporting_w1']}/{row['full_hit_supporting_w2']} / {row['full_hit_supporting_usage_denominator']}"
        planned = "yes" if row["planned_in_frozen_scope"] else "no"
        lines.append(f"| `{row['predicate_id']}` | `{planned}` | `{row['report_bound_plan_count']}` | `{row['precise_binding_count']}` | `{row['receipt_present_count']}` | `{all_w}` | `{hit_w}` |")
    lines += [
        "",
        "## 成本",
        "",
        "成本只报告冻结 run record 中已有的金额和 eligibility；本 v3 重审没有新增 provider、method 或 Judge 调用。",
        "",
        "| 阶段 | v60/current | X1v2 baseline |",
        "|---|---:|---:|",
        f"| method | `${current['cost']['method_usd']:.8f}`; eligible=`{current['cost']['method_cost_eligible']}` | `${baseline['cost']['method_usd']:.8f}`; eligible=`{baseline['cost']['method_cost_eligible']}` |",
        f"| Judge | `${current['cost']['judge_recorded_usd']:.8f}`; eligible=`{current['cost']['judge_cost_eligible']}` | `${baseline['cost']['judge_recorded_usd']:.8f}`; eligible=`{baseline['cost']['judge_cost_eligible']}` |",
        "",
        "## Baseline round/pair 分布",
        "",
        "下表只展示 baseline v3；完整 pair-level JSON 位于 [recomputed summary](../derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json)。",
        "",
        "| round | reports | K | N | I | D2 | D1 | D0 | A0 |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for round_no in sorted(baseline_summary["by_round"], key=int):
        value = baseline_summary["by_round"][round_no]
        kni = value["kni"]
        d_a = value["d_a"]
        lines.append(f"| {round_no} | {value['report_count']} | {kni.get('K', 0)} | {kni.get('N', 0)} | {kni.get('I', 0)} | {d_a.get('D2', 0)} | {d_a.get('D1', 0)} | {d_a.get('D0', 0)} | {d_a.get('A0', 0)} |")
    lines += [
        "",
        "| pair | reports | K | N | I | D2 | D1 | D0 | A0 |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for pair_id in sorted(baseline_summary["by_pair"]):
        value = baseline_summary["by_pair"][pair_id]
        kni = value["kni"]
        d_a = value["d_a"]
        lines.append(f"| {pair_id} | {value['report_count']} | {kni.get('K', 0)} | {kni.get('N', 0)} | {kni.get('I', 0)} | {d_a.get('D2', 0)} | {d_a.get('D1', 0)} | {d_a.get('D0', 0)} | {d_a.get('A0', 0)} |")
    lines += [
        "",
        "## 非 K 迁移与分组",
        "",
        f"v3 non-K 迁移计数来自 [summary_v3.json](../derived/manual_adjudication_v3_baseline_ni/summary_v3.json)：`{json.dumps(baseline_summary['non_k_migrations']['counts'], ensure_ascii=False, sort_keys=True)}`。新增 K 的完整 report/expected 映射见 summary 的 `non_k_migrations.rows`。",
        "",
        "| migration | count |",
        "|---|---:|",
    ]
    for migration, count in baseline_summary["non_k_migrations"]["counts"].items():
        lines.append(f"| `{migration}` | `{count}` |")
    new_k_rows = [row for row in baseline_summary["non_k_migrations"]["rows"] if row["to"] == "K"]
    lines += [
        "",
        f"新增 K 共 `{len(new_k_rows)}` 条非 K report，全部标记为 `reclassified_from_non_k=true`；下面保留其 report 到 ledger relation 的可追溯映射，完整字段仍以 summary JSON 为准。",
        "",
        "| report_id | FULL ledger IDs | PARTIAL ledger IDs |",
        "|---|---|---|",
    ]
    for row in new_k_rows:
        lines.append(f"| `{row['report_id']}` | `{', '.join(row['full_ledger_ids']) or '-'}` | `{', '.join(row['partial_ledger_ids']) or '-'}` |")
    n_d = Counter(row["d_tier"] for row in decisions if row["corrected_kni"] == "N")
    old_counts = baseline_summary["old_v2_comparison"]["old_v2_counts"]
    new_counts = baseline_summary["old_v2_comparison"]["new_counts"]
    lines += [
        "",
        f"N report/group 视图：原始非 K N `{baseline_summary['n_grouping']['original_non_k_n_reports']}`，corrected N `{baseline_summary['n_grouping']['corrected_n_reports']}`，substantive N group `{baseline_summary['n_grouping']['substantive_n_groups']}`，root-cause group `{baseline_summary['n_grouping']['root_cause_group_count']}`；N 的 D2/D1 为 `{n_d.get('D2', 0)}/{n_d.get('D1', 0)}`，group size distribution 为 `{json.dumps(baseline_summary['n_grouping']['group_size_distribution'], sort_keys=True)}`。",
        f"I 构成见 `a0_subtypes`：`{json.dumps(baseline_summary['a0_subtypes'], ensure_ascii=False, sort_keys=True)}`；I 不被表述为 novel defect。",
        "",
        "| historical comparison | K | N | I |",
        "|---|---:|---:|---:|",
        f"| v2 frozen scope | `{old_counts['K']}` | `{old_counts['N']}` | `{old_counts['I']}` |",
        f"| v3 combined | `{new_counts['K']}` | `{new_counts['N']}` | `{new_counts['I']}` |",
        "",
        f"未合并 I 的敏感性为 `{baseline['ledger_group_sensitivity_unmerged_I']['numerator']}/{baseline['ledger_group_sensitivity_unmerged_I']['denominator']} = {baseline['ledger_group_sensitivity_unmerged_I']['percentage'] * 100:.2f}%`；主结果使用 `{baseline['ledger_group_based_precision']['numerator']}/{baseline['ledger_group_based_precision']['denominator']}`，因为 I 只作为诊断 cluster，不是真实缺陷实体。",
        "",
        "## 审计与限制",
        "",
        f"每条 v3 非 K 记录保留 raw/source refs、hash、145 relations、两份独立 proposal 和 pane5 confirmation；当前 review log 记录 `{review_log['independent_reviewer_count']}` 个独立 reviewer、`{review_log['coverage']['decisions']}/{baseline_summary['reviewed_non_k_count']}` 决策覆盖、`{arbitration_log['disagreement_count']}` 条分歧和 `{arbitration_log['entry_count']}` 条 pane5 仲裁。Track B proposal 是 blind proposal，不是最终人工裁定。旧 v2/Judge 只作冻结 scope、历史 provenance 或工具诊断，不倒灌 v3 标签。",
        "",
        "审计限制包括：台账不保证覆盖完整缺陷宇宙；人工归并是 operationalization；L2 对 N/I 无自然归属；baseline 没有 current-side predicate schema；观察性比较不推出因果。legacy/probe proposal 保留但被 v3 manifest 明确排除。",
        "",
        "## 离线复算",
        "",
        "```bash",
        "PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_manual_adjudication_v3_baseline_ni.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni",
        "python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_baseline_n_groups_v3.py --decisions project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_n_groups_v3.json",
        "python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_baseline_v3_summary.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json",
        "python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_baseline_v3.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline",
        "python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_baseline_v3_manifest.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline",
        "```",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
