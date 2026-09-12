#!/usr/bin/env python3
"""Render the publication report from the canonical manual summary only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable


def load(path: Path) -> dict[str, Any]:
    """Load a JSON object used as a canonical report input."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def metric(value: dict[str, Any]) -> str:
    """Render a numerator/denominator/percentage metric without dropping its base."""

    percentage = value.get("percentage")
    rendered = "n/a" if percentage is None else f"{percentage * 100:.2f}%"
    return f"{value['numerator']}/{value['denominator']} = {rendered}"


def delta(left: dict[str, Any], right: dict[str, Any]) -> str:
    """Render a v60-minus-baseline absolute and percentage-point delta."""

    left_percentage = left.get("percentage")
    right_percentage = right.get("percentage")
    pp = "n/a" if left_percentage is None or right_percentage is None else f"{(left_percentage - right_percentage) * 100:+.2f} pp"
    return f"{left['numerator'] - right['numerator']:+d}; {pp}"


def row(label: str, getter: Callable[[dict[str, Any]], dict[str, Any]], sides: dict[str, Any]) -> str:
    """Create one paired metric row."""

    current = getter(sides["v60_current"])
    baseline = getter(sides["x1v2_baseline"])
    return f"| {label} | `{metric(current)}` | `{metric(baseline)}` | `{delta(current, baseline)}` |"


def count_row(label: str, getter: Callable[[dict[str, Any]], int], sides: dict[str, Any]) -> str:
    """Create a paired categorical count row with an explicit report denominator."""

    current = sides["v60_current"]
    baseline = sides["x1v2_baseline"]
    current_n = getter(current)
    baseline_n = getter(baseline)
    return f"| {label} | `{current_n}/{current['report_count']} = {current_n / current['report_count'] * 100:.2f}%` | `{baseline_n}/{baseline['report_count']} = {baseline_n / baseline['report_count'] * 100:.2f}%` | `{current_n - baseline_n:+d}; {(current_n / current['report_count'] - baseline_n / baseline['report_count']) * 100:+.2f} pp` |"


def paired_count_row(label: str, current_n: int, baseline_n: int, current_denominator: int, baseline_denominator: int) -> str:
    """Render paired categorical counts with their own denominators and delta."""

    current_ratio = current_n / current_denominator if current_denominator else None
    baseline_ratio = baseline_n / baseline_denominator if baseline_denominator else None
    current_text = f"{current_n}/{current_denominator} = {current_ratio * 100:.2f}%" if current_ratio is not None else "n/a"
    baseline_text = f"{baseline_n}/{baseline_denominator} = {baseline_ratio * 100:.2f}%" if baseline_ratio is not None else "n/a"
    pp = "n/a" if current_ratio is None or baseline_ratio is None else f"{(current_ratio - baseline_ratio) * 100:+.2f} pp"
    return f"| {label} | `{current_text}` | `{baseline_text}` | `{current_n - baseline_n:+d}; {pp}` |"


def main() -> None:
    """Render the final Chinese report without hand-entered result numbers."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve()
    summary = load(directory / "summary.json")
    calibration = load(directory / "calibration_report.json")
    predicate = load(directory / "predicate_witness_audit.json")
    inventory = load(directory / "inventory.json")
    sides = summary["sides"]
    current = sides["v60_current"]
    baseline = sides["x1v2_baseline"]
    calibration_targeted = calibration["targeted_re_review_closure"]
    report_lines = [
        "# v60/current 与 X1v2 baseline 的最终人工监督评测",
        "",
        "> 本报告的主结果只来自 `derived/manual_adjudication_v2/` 的最终人工监督裁定；旧 Judge v3.2、reviews/11、reviews/12 和旧 witness audit 只作为 calibration/proposal 或历史诊断，不作为本次论文真值。",
        "",
        "## 口径与范围",
        "",
        "协议版本为 `issue-189-195-manual-evidence-v2`，按 issue #189 的 D/A 事实与义务审查、issue #195 的 expected relation 与 validity 轴执行。先判断作者 NL/PlantUML 上的承重事实，再判 `D2/D1/D0/A0`，逐条对 145 个 expected 给出 `FULL_MATCH/PARTIAL_MATCH/NO_MATCH`，最后由后端确定性闭合 `VALID_KNOWN/VALID_NOVEL/INVALID` 与 `K/N/I`。`D0/A0 -> INVALID -> I`；`D2/D1` 且存在正关系为 `VALID_KNOWN -> K`，全部 `NO_MATCH` 才是 `VALID_NOVEL -> N`。",
        "",
        "A0 只有 `FALSE_POSITIVE` 和 current-only 的 `NOT_A_DEFECT_CLAIM`；X1v2 不使用后者。W 是独立证据轴：W2 必须同时有原始 executable object、typed input、精确 artifact hash、terminal true/false 和 receipt；缺一项退为 W1/W0。W、L、predicate usage 和方法自报标签不参与 validity、relation、hit 或 FP。",
        "",
        "raw-first reviewer 输入使用双方共同 allowlist：两侧 report 均映射为 claim/reason，`location_text` 固定为空；双方都附对应 pair 的 NL、PlantUML 和 source SHA-256。raw target pointer/hash、producer-specific location、predicate、receipt、W、旧 Judge 标签和最终语义标签不进入盲审投影；精确 raw identity/hash 只在 proposal 提交后通过 sealed unblind mapping 进入主 session 的回读与仲裁。字段缺失按 schema 差异保留，不填零。完整 field-level mapping 见 [semantic Judge protocol](../../../discover_matrix/docs/protocol/semantic_judge_protocol.md#双侧-reviewer-输入映射)。",
        "",
        f"raw inventory 从冻结归档重新枚举：v60/current `{inventory['reports']['v60_current']}` reports、X1v2 `{inventory['reports']['x1v2_baseline']}` findings，双方各 `{inventory['cells']['v60_current']}` method cells；expected ledger `{summary['expected_count']}` 条，dense relation 为 `{(current['report_count'] + baseline['report_count']) * summary['expected_count']}` 行。详情见 [inventory](../derived/manual_adjudication_v2/inventory.json) 和 [protocol](../derived/manual_adjudication_v2/protocol_freeze_v2.md)。",
        "",
        "## 主结果",
        "",
        "表中 delta 均为 v60/current 减 X1v2 baseline；分号前为 numerator 差，后为百分点差。结构化来源是 [summary.json](../derived/manual_adjudication_v2/summary.json)，每个 report 的稳定审计键是 `report_id`。",
        "",
        "| 指标 | v60/current | X1v2 baseline | delta (n; pp) |",
        "|---|---:|---:|---:|",
        row("overall hit@1 / FULL", lambda s: s["hit_at_1_full"], sides),
        row("L2 hit@1 / FULL", lambda s: s["l2_hit_at_1_full"], sides),
        row("hit@3", lambda s: s["hit_at_3_full"], sides),
        row("hit@all", lambda s: s["hit_at_all_full"], sides),
        row("L2 hit@3", lambda s: s["l2_hit_at_3_full"], sides),
        row("L2 hit@all", lambda s: s["l2_hit_at_all_full"], sides),
        row("supported coverage, round units", lambda s: s["supported_coverage_round_units"], sides),
        row("supported coverage, unique expected", lambda s: s["supported_coverage_unique_expected"], sides),
        row("report-based precision", lambda s: s["report_based_precision"], sides),
        row("report-based FP rate", lambda s: s["report_based_fp_rate"], sides),
        row("partial_only_known_report", lambda s: s["partial_only_known_report"], sides),
        row("partial_only_known_expected", lambda s: s["partial_only_known_expected"], sides),
        row("ledger K_hit", lambda s: s["ledger_based"]["K_hit"], sides),
        row("ledger N_group composition", lambda s: s["ledger_based"]["N_group"], sides),
        row("ledger I_group composition", lambda s: s["ledger_based"]["I_group"], sides),
        row("ledger-based precision", lambda s: s["ledger_based"]["precision"], sides),
        row("ledger-based FP rate", lambda s: s["ledger_based"]["fp_rate"], sides),
        row("FULL-hit max W2", lambda s: s["hit_max_witness"]["W2"], sides),
        row("FULL-hit max W1", lambda s: s["hit_max_witness"]["W1"], sides),
        row("FULL-hit max W0", lambda s: s["hit_max_witness"]["W0"], sides),
        row("W2 / all expected", lambda s: s["w2_all_expected"], sides),
        "",
        "`K_hit` 是三轮中至少一次 FULL 的 unique expected issue；N/I 是同一 side、同一 pair 内按人工确认的 substantive property、author-source locus、repair obligation 和 cause 合并的操作性 group。当前 N/I group counts 为 `" + str(current["ledger_based"]["N_group_count"]) + "`/`" + str(current["ledger_based"]["I_group_count"]) + "`，baseline 为 `" + str(baseline["ledger_based"]["N_group_count"]) + "`/`" + str(baseline["ledger_based"]["I_group_count"]) + "`；不跨 side、pair，也不按文本相似度合并。L2 ledger precision/FP 为 `not_applicable`，因为 N/I group 没有自然的 L2 expected 归属。",
        "",
        "## D/A、K/N/I 与关系",
        "",
        "以下表格使用 report 分母；relation 表使用 dense `(report, expected)` 分母。完整逐条记录见 [v60 decisions](../derived/manual_adjudication_v2/v60_report_decisions.json)、[baseline decisions](../derived/manual_adjudication_v2/x1v2_report_decisions.json) 和 [dense relations](../derived/manual_adjudication_v2/relation_decisions.json)。",
        "",
        "| 类别 | v60/current | X1v2 baseline | delta (n; pp) |",
        "|---|---:|---:|---:|",
    ]
    for key in ("D2", "D1", "D0", "A0"):
        report_lines.append(paired_count_row(key, current["decision_counts"].get(key, 0), baseline["decision_counts"].get(key, 0), current["report_count"], baseline["report_count"]))
    for key in ("K", "N", "I"):
        report_lines.append(paired_count_row(key, current["kni_counts"].get(key, 0), baseline["kni_counts"].get(key, 0), current["report_count"], baseline["report_count"]))
    for key in ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH"):
        report_lines.append(paired_count_row(key, current["relation_counts"].get(key, 0), baseline["relation_counts"].get(key, 0), current["report_count"] * summary["expected_count"], baseline["report_count"] * summary["expected_count"]))
    report_lines += [
        "",
        "`PARTIAL_MATCH` 提供 supported coverage，但不计主 hit，也不计 FP。只有最终 `INVALID` 计 report-based FP；`VALID_NOVEL` 不是 FP。hit@1 的分母是 435 个 expected-round 单元，hit@3/all 的分母是 145 个 unique expected；L2 对应 117/39。",
        "",
        "## W 与 predicate",
        "",
        "| W 轴 | v60/current | X1v2 baseline |",
        "|---|---:|---:|",
        f"| finding-level W0/W1/W2 | `{current['witness_counts'].get('W0', 0)}/{current['witness_counts'].get('W1', 0)}/{current['witness_counts'].get('W2', 0)}` / `{current['report_count']}` | `{baseline['witness_counts'].get('W0', 0)}/{baseline['witness_counts'].get('W1', 0)}/{baseline['witness_counts'].get('W2', 0)}` / `{baseline['report_count']}` |",
        f"| FULL-hit max W2/W1/W0 | `{current['hit_max_witness']['W2']['numerator']}/{current['hit_max_witness']['W1']['numerator']}/{current['hit_max_witness']['W0']['numerator']}` / `{current['hit_at_1_full']['numerator']}` | `{baseline['hit_max_witness']['W2']['numerator']}/{baseline['hit_max_witness']['W1']['numerator']}/{baseline['hit_max_witness']['W0']['numerator']}` / `{baseline['hit_at_1_full']['numerator']}` |",
        f"| W2/all-expected | `{metric(current['w2_all_expected'])}` | `{metric(baseline['w2_all_expected'])}` |",
        "",
        "W-on-hits 的分母是有 FULL 的 expected-round hit 单元；W2/all-expected 的分母固定为全部 435 个 expected-round 单元，二者不能互换。",
        "",
        "current 的 predicate usage 只统计 frozen 19-registry 中的合法 precise binding。冻结 evaluator 的 planned scope（`planned_scope`，当前 15 个 ID）与逐报告观察到的 `report_bound_plan_count` 分开；每行另记录 route、precise binding、receipt present、terminal true/false、全部 usage 的 W0/W1/W2 以及 FULL-hit supporting usage。receipt 缺失或失败仍留在 usage 分母。baseline 没有同构 predicate schema，predicate usage 明确为 `not_applicable`，不填 0。详见 [predicate_witness_audit.json](../derived/manual_adjudication_v2/predicate_witness_audit.json) 和 [predicate_source_provenance.json](../derived/manual_adjudication_v2/predicate_source_provenance.json)。",
        "",
        "| predicate | frozen scope / report-bound plan | routed / precise | receipt | terminal true / false | all usage W0/W1/W2 | FULL-hit usage W0/W1/W2 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in predicate["sides"]["v60_current"]["predicate_rows"]:
        report_lines.append(
            f"| `{item['predicate_id']}` | `{('yes' if item.get('planned_in_frozen_scope') else 'no')}/{item.get('report_bound_plan_count', 0)}` | `{item.get('route_count', 0)}/{item.get('precise_binding_count', 0)}` | `{item.get('receipt_present_count', 0)}` | `{item.get('terminal_true_count', 0)}/{item.get('terminal_false_count', 0)}` | `{item['all_usage_w0']}/{item['all_usage_w1']}/{item['all_usage_w2']}` / `{item['all_usage_denominator']}` | `{item['full_hit_supporting_w0']}/{item['full_hit_supporting_w1']}/{item['full_hit_supporting_w2']}` / `{item['full_hit_supporting_usage_denominator']}` |"
        )
    report_lines += [
        "",
        "## Calibration 与审查",
        "",
        f"444 条 frozen N 与 106 条 frozen I 共 550 条 calibration/reference rows。raw-first blind calibration 的 strict D/A agreement 为 `{metric(calibration['agreement']['strict_da_and_a0_type'])}`，dense relation agreement 为 `{metric(calibration['agreement']['dense_relation'])}`；mismatch `{calibration_targeted['mismatch_count']}` 条，[targeted reread](../derived/manual_adjudication_v2/pane5_targeted_re_review.json) 对 mismatch 的闭合为 `{calibration_targeted['matched_mismatch_count']}/{calibration_targeted['mismatch_count']}`，总 targeted reread 记录为 `{calibration_targeted['total_targeted_re_review_count']}` 条，closure=`{calibration_targeted['all_mismatches_targeted']}`，sentinel 为 `{all(calibration['sentinels'].values())}`，calibration status 为 `{calibration['status']}`。reference 同单位聚合见 [reference_ledger_aggregate.json](../derived/manual_adjudication_v2/reference_ledger_aggregate.json)。",
        "",
        "主 session 是用户授权的 pane5 人类监督 adjudication session。每条最终记录都有 `human_confirmation=true`、`human_supervised_session=true`、primary/final `human:pane5-supervised-adjudicator`；independent reviewer 如实记录为 `subagent:raw-first-independent-proposal`，先 raw-first blind，再解盲比较，未冒充真人。逐条 evidence-read、授权消息/时间、attestation 和 closure 见 [pane5_evidence_reads.json](../derived/manual_adjudication_v2/pane5_evidence_reads.json)、[pane5_adjudications.json](../derived/manual_adjudication_v2/pane5_adjudications.json)、[human_supervised_authorization.json](../derived/manual_adjudication_v2/human_supervised_authorization.json) 与 [review_log.json](../derived/manual_adjudication_v2/review_log.json)。",
        "",
        "## 成本与限制",
        "",
        "| 阶段 | v60/current | X1v2 baseline |",
        "|---|---:|---:|",
        f"| method cost | `${current['cost'].get('method_usd'):.8f}`; eligible={current['cost'].get('method_cost_eligible')} | `${baseline['cost'].get('method_usd'):.8f}`; eligible={baseline['cost'].get('method_cost_eligible')} |",
        f"| Judge cost | `${current['cost'].get('judge_recorded_usd'):.8f}`; eligible={current['cost'].get('judge_cost_eligible')} | `${baseline['cost'].get('judge_recorded_usd'):.8f}`; eligible={baseline['cost'].get('judge_cost_eligible')} |",
        f"| Judge logical calls | `{current['cost'].get('judge_logical_call_count')}` | `{baseline['cost'].get('judge_logical_call_count', 'not recorded')}` |",
        "",
        "台账不是完整缺陷宇宙；人工归并是本协议下的 operational group，不宣称本体论上的唯一缺陷数。L2 的语义边界、baseline schema 差异、baseline 缺少原始 predicate receipt、v60 Judge 成本中未定价调用，以及观察性比较不能推出因果，都是限制。v27/v46 和旧 v3.2 headline 只保留在 archive/history，不混入本报告主分母。",
        "",
        "## 复算入口",
        "",
        "```bash",
        "PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_manual_adjudication.py --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2",
        "PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_manual_adjudication.py --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2",
        "```",
        "",
        "上述命令只读取冻结 raw/reference 和 canonical decisions，不调用 provider，不重跑 method/Judge，也不修改 raw。MANIFEST 绑定所有 canonical JSON/TSV、过程审计、输入 hash 和 supporting artifact。",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(report_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
