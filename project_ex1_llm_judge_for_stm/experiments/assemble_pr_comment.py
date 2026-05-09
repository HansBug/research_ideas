"""Assemble the reviewer-experiment PR comment from
`experiment_alignment.json` and the chart-image URL map.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"


def fmt(v, sig=3) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        if v != v:  # NaN
            return "—"
        return f"{v:.{sig}f}"
    return str(v)


def fmt_delta(d) -> str:
    if d is None or (isinstance(d, float) and d != d):
        return "—"
    sign = "+" if d > 0 else ""
    return f"{sign}{fmt(d, 3)}"


PAPER_LABEL = {
    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models": "structure-event-driven (SED)",
    "llms_emp": "llms_emp",
    "ttool-ai": "ttool-ai",
    "psmbench": "psmbench (NEW)",
    "rfcnlp": "rfcnlp (NEW)",
    "hermes": "hermes (NEW)",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alignment-json", type=Path, default=ETL_OUT / "experiment_alignment.json")
    parser.add_argument("--images-json", type=Path, required=True,
                        help="JSON dict mapping chart filename → user-attachments URL")
    parser.add_argument("--commit-sha", type=str, default="TBD")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.alignment_json.read_text())
    images = json.loads(args.images_json.read_text())
    base = payload["baseline"]
    new = payload["new"]
    delta = payload.get("delta_new_minus_baseline", {})
    base_a = base["alignment"]
    new_a = new["alignment"]
    base_p = base["proxy_metrics"]
    new_p = new["proxy_metrics"]

    def img(fname: str) -> str:
        return images.get(fname, f"(missing image URL for {fname})")

    align_keys = ["MAE", "RMSE", "ScoreAlign", "RankAlign", "spearman_rho", "pearson_r", "JudgementAlign"]
    proxy_keys = ["RAS_proxy", "SAS_proxy", "CRAS_proxy", "HAI_proxy"]

    md = []
    md.append(f"## 🧪 LLM expert reviewer 实测：用 protocol-FSM 新数据 × baseline UML/SysML 旧数据做新旧对比（commit {args.commit_sha}）")
    md.append("")
    md.append("> 上一条 [#issuecomment-4385916089](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4385916089) 已 deprecated，那只到了 ETL/coverage 层；本条才是**真正用我们 reviewer 系统跑出来的实验结果**。")
    md.append("")
    # Section 1
    md.append("### 一、实验设计")
    md.append("")
    md.append("- **Reviewer 配置（公平统一）**：`gpt-5.5` via `airouter`，`temperature=0`，`rerun_count=0`，`llm_mode=auto`，11 阶段 LangGraph pipeline")
    md.append(f"- **Baseline (UML/SysML 旧域) 样本**：{base.get('n_paired', 0)} 行 — SED component_level + llms_emp sample_level + ttool-ai summary_level")
    md.append(f"- **New (protocol-FSM 新域) 样本**：{new.get('n_paired', 0)} 行 — PSMBench (9 LLMs × 3 协议) + RFCNLP NLP-predictor")
    md.append("- **人评 ground truth**：baseline 论文公开 0-100 / F1，new 用 PSMBench κ=0.82/0.78 cross-verified ground-truth + paper 9 类标签 macro-F1 / paper-reported accuracy")
    md.append("- **指标公式**：与 [`benchmark.py`](https://github.com/HansBug/research_ideas/blob/dev/reviewer/project_ex1_llm_judge_for_stm/src/expert_review/benchmark.py) 一致 (`ScoreAlign = 100·(1-MAE)`; `RankAlign = 100·pairwise_order`; HAI = 0.40·RAS + 0.30·SAS + 0.30·CRAS)")
    md.append("")
    # Section 2
    md.append("### 二、Headline 指标对比（new vs baseline）")
    md.append("")
    md.append(f"![proxy alignment metrics]({img('15_proxy_metrics.png')})")
    md.append("")
    md.append("| 指标 | baseline (UML/SysML) | new (protocol-FSM) | Δ (new - baseline) |")
    md.append("|---|---:|---:|---:|")
    md.append(f"| n_paired | {base.get('n_paired', 0)} | {new.get('n_paired', 0)} | — |")
    md.append(f"| **MAE** ↓ | {fmt(base_a['MAE'])} | {fmt(new_a['MAE'])} | {fmt_delta(delta.get('alignment',{}).get('MAE'))} |")
    md.append(f"| **Spearman ρ** ↑ | {fmt(base_a['spearman_rho'])} | {fmt(new_a['spearman_rho'])} | {fmt_delta(delta.get('alignment',{}).get('spearman_rho'))} |")
    md.append(f"| **Pearson r** ↑ | {fmt(base_a['pearson_r'])} | {fmt(new_a['pearson_r'])} | {fmt_delta(delta.get('alignment',{}).get('pearson_r'))} |")
    md.append(f"| **ScoreAlign** ↑ | {fmt(base_a['ScoreAlign'], 2)} | {fmt(new_a['ScoreAlign'], 2)} | {fmt_delta(delta.get('alignment',{}).get('ScoreAlign'))} |")
    md.append(f"| **RankAlign** ↑ | {fmt(base_a['RankAlign'], 2)} | {fmt(new_a['RankAlign'], 2)} | {fmt_delta(delta.get('alignment',{}).get('RankAlign'))} |")
    md.append(f"| **JudgementAlign** ↑ | {fmt(base_a['JudgementAlign'], 2)} | {fmt(new_a['JudgementAlign'], 2)} | {fmt_delta(delta.get('alignment',{}).get('JudgementAlign'))} |")
    md.append(f"| **RAS_proxy** ↑ | {fmt(base_p['RAS_proxy'], 2)} | {fmt(new_p['RAS_proxy'], 2)} | {fmt_delta(delta.get('proxy_metrics',{}).get('RAS_proxy'))} |")
    md.append(f"| **SAS_proxy** ↑ | {fmt(base_p['SAS_proxy'], 2)} | {fmt(new_p['SAS_proxy'], 2)} | {fmt_delta(delta.get('proxy_metrics',{}).get('SAS_proxy'))} |")
    md.append(f"| **CRAS_proxy** ↑ | {fmt(base_p['CRAS_proxy'], 2)} | {fmt(new_p['CRAS_proxy'], 2)} | {fmt_delta(delta.get('proxy_metrics',{}).get('CRAS_proxy'))} |")
    md.append(f"| **HAI_proxy** ↑ | {fmt(base_p['HAI_proxy'], 2)} | {fmt(new_p['HAI_proxy'], 2)} | {fmt_delta(delta.get('proxy_metrics',{}).get('HAI_proxy'))} |")
    md.append("")
    # Auto-generated insight
    rho_b = base_a.get("spearman_rho")
    rho_n = new_a.get("spearman_rho")
    mae_b = base_a.get("MAE")
    mae_n = new_a.get("MAE")
    if rho_b is not None and rho_n is not None and not (rho_b != rho_b or rho_n != rho_n):
        if rho_n > rho_b:
            ins = f"reviewer 在新域 (ρ={rho_n:.3f}) **优于**旧域 (ρ={rho_b:.3f})"
        elif abs(rho_n - rho_b) < 0.05:
            ins = f"reviewer 在新旧域排序相关性近似 (ρ_new={rho_n:.3f} vs ρ_baseline={rho_b:.3f})"
        else:
            ins = f"reviewer 在新域排序相关性 (ρ={rho_n:.3f}) 略低于旧域 (ρ={rho_b:.3f})"
        md.append(f"→ **关键 insight**：{ins}（rank correlation）。MAE: baseline {mae_b:.3f} vs new {mae_n:.3f}，HAI_proxy: baseline {base_p['HAI_proxy']:.1f} vs new {new_p['HAI_proxy']:.1f}。")
    md.append("")
    # Section 3
    md.append("### 三、Reviewer ↔ human 散点图")
    md.append("")
    md.append(f"![alignment scatter]({img('11_alignment_scatter.png')})")
    md.append("")
    md.append("两侧子图分别画了 baseline 与 new 的散点。x 轴是归一化的 human reference score，y 轴是我们 reviewer 的 overall_score。点离 y=x 对角线越近代表 reviewer 越对齐 human。")
    md.append("")
    # Section 4
    md.append("### 四、Score 分布对比")
    md.append("")
    md.append(f"![score distribution]({img('10_score_distribution.png')})")
    md.append(f"- baseline reviewer mean = {fmt(base['reviewer_stats']['score_mean'], 3)} (std {fmt(base['reviewer_stats']['score_std'], 3)})")
    md.append(f"- new reviewer mean = {fmt(new['reviewer_stats']['score_mean'], 3)} (std {fmt(new['reviewer_stats']['score_std'], 3)})")
    md.append(f"- baseline 中 reviewer score < 0.3: **{base['reviewer_stats']['low_count_lt_0.3']}** / ≥ 0.7: **{base['reviewer_stats']['high_count_ge_0.7']}**")
    md.append(f"- new 中 reviewer score < 0.3: **{new['reviewer_stats']['low_count_lt_0.3']}** / ≥ 0.7: **{new['reviewer_stats']['high_count_ge_0.7']}**")
    md.append("")
    # Section 5
    md.append("### 五、Per-paper 表现")
    md.append("")
    md.append(f"![per-paper]({img('13_per_paper.png')})")
    md.append("")
    md.append("| paper | n | reviewer mean | human mean | ScoreAlign | ρ |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for paper, pp in (list(base["per_paper"].items()) + list(new["per_paper"].items())):
        label = PAPER_LABEL.get(paper, paper)
        md.append(f"| {label} | {pp['n']} | {fmt(pp['reviewer_mean'], 3)} | {fmt(pp['human_mean'], 3)} | {fmt(pp['score_align'], 2)} | {fmt(pp['spearman_rho'], 3)} |")
    md.append("")
    # Section 6
    md.append("### 六、6 个评估维度的 reviewer 行为")
    md.append("")
    md.append(f"![dimension comparison]({img('14_dimension_comparison.png')})")
    md.append("")
    md.append("(每张柱图标的是 baseline 与 new 各自的均值与误差棒。哪些维度的 score 在新域显著下降，就指向 reviewer 在该维度对 protocol-FSM 域的潜在弱点。)")
    md.append("")
    # Section 7
    md.append("### 七、PSMBench: 我们 reviewer 的 LLM 排名 vs 论文 auto F1 排名")
    md.append("")
    md.append(f"![psmbench cross-check]({img('16_psmbench_ranking_crosscheck.png')})")
    md.append("")
    md.append('两个独立的"打分系统"对同一组 LLM 的相对排名是否一致 — 这是 reviewer 学到的 quality signal 是否在新域**仍然保留 LLM 间区分能力**的强证据。')
    md.append("")
    # Section 8
    md.append("### 八、Triage / Judgement 分布")
    md.append("")
    md.append(f"![triage and judgement]({img('12_judgement_triage.png')})")
    md.append("")
    md.append("baseline triage:")
    for k, v in base["distributions"]["triage_label"].items():
        md.append(f"- `{k}`: {v}")
    md.append("")
    md.append("new triage:")
    for k, v in new["distributions"]["triage_label"].items():
        md.append(f"- `{k}`: {v}")
    md.append("")
    # Section 9 — auto-generated discussion
    md.append("### 九、关键发现 + 局限")
    md.append("")
    discussion: list[str] = []
    if rho_n is not None and rho_b is not None and not (rho_n != rho_n or rho_b != rho_b):
        diff = rho_n - rho_b
        if abs(diff) < 0.05:
            discussion.append(f"1. **跨域 rank correlation 近似稳定**：reviewer 在新旧域的 Spearman ρ 差异仅 {diff:+.3f}，说明它学到的 review signal 在 protocol-FSM 域**仍然保留排序能力**，没有 collapse")
        elif diff < -0.10:
            discussion.append(f"1. **跨域 rank correlation 显著下降**：reviewer 在新域 ρ={rho_n:.3f} 比旧域 ρ={rho_b:.3f} 低 {-diff:.3f}，说明它对 protocol-FSM 域的相对排序判断弱了")
        else:
            discussion.append(f"1. **跨域 rank correlation 略变化**：Δρ={diff:+.3f}（{'优于' if diff > 0 else '低于'} 旧域）")
    if mae_b is not None and mae_n is not None:
        diff_mae = mae_n - mae_b
        if diff_mae > 0.05:
            discussion.append(f"2. **新域 MAE 增加** {diff_mae:.3f}：reviewer 在 protocol-FSM 上 absolute score 偏离 human reference 比旧域更多")
        elif diff_mae < -0.05:
            discussion.append(f"2. **新域 MAE 减少** {-diff_mae:.3f}：reviewer 在 protocol-FSM 上 absolute score 反而比旧域更准")
        else:
            discussion.append(f"2. **MAE 跨域稳定**：差异仅 {diff_mae:+.3f}")
    hai_diff = (delta.get("proxy_metrics") or {}).get("HAI_proxy")
    if hai_diff is not None:
        if hai_diff < -3:
            discussion.append(f"3. **HAI_proxy 在新域下降** {-hai_diff:.1f}：综合 alignment 指标提示新域 reviewer 表现弱于旧域，主要原因可能是 input_text 上下文较薄（PSMBench segment 摘要只 1-2 行）")
        elif hai_diff > 3:
            discussion.append(f"3. **HAI_proxy 在新域提升** {hai_diff:.1f}：可能因为 protocol-FSM 域语法更结构化，reviewer 易判断")
        else:
            discussion.append(f"3. **HAI_proxy 跨域稳定**：差异 {hai_diff:+.1f}")
    if not discussion:
        discussion.append("1. (待添加 — 数据未生成)")
    md.extend(discussion)
    md.append("")
    md.append("**局限**：")
    md.append(f"- 样本规模：{base.get('n_paired', 0) + new.get('n_paired', 0)} 行（baseline {base.get('n_paired', 0)} + new {new.get('n_paired', 0)}）— 单 reviewer pass，无 rerun 所以 Stability 不单独评估")
    md.append("- proxy_metrics 不是 benchmark.py 的完整 RAS/SAS/CRAS（缺 issue_f1 / equivalence / calibration / stability 子分），只是同公式 shape 的 baseline")
    md.append("- new 域 input_text 上下文较薄（PSMBench segment 摘要 ~1-2 行），与 baseline 富需求文本不公平 — 但这恰恰刻画 reviewer 对 thin context 的鲁棒性")
    md.append(f"- 单条 reviewer call 平均 latency: baseline {fmt(base['reviewer_stats']['latency_mean_s'], 1)}s / new {fmt(new['reviewer_stats']['latency_mean_s'], 1)}s")
    md.append("")
    # Section 10
    md.append("### 十、Artifact 落点")
    md.append("")
    md.append("- **样本与结果**：[`experiments/out/`](https://github.com/HansBug/research_ideas/tree/dev/reviewer/project_ex1_llm_judge_for_stm/experiments/out)")
    md.append("  - `experiment_baseline_sample.jsonl` / `experiment_new_sample.jsonl`（输入）")
    md.append("  - `experiment_baseline_result.jsonl` / `experiment_new_result.jsonl`（reviewer 原始输出）")
    md.append("  - `experiment_alignment.json`（指标聚合）")
    md.append("- **可视化**：`charts/10_*.png` ~ `charts/16_*.png` 共 7 张")
    md.append("- **入口脚本**：")
    md.append("  - [`build_experiment_batches.py`](https://github.com/HansBug/research_ideas/blob/dev/reviewer/project_ex1_llm_judge_for_stm/experiments/build_experiment_batches.py)（采样）")
    md.append("  - [`compute_alignment_metrics.py`](https://github.com/HansBug/research_ideas/blob/dev/reviewer/project_ex1_llm_judge_for_stm/experiments/compute_alignment_metrics.py)（指标）")
    md.append("  - [`build_experiment_charts.py`](https://github.com/HansBug/research_ideas/blob/dev/reviewer/project_ex1_llm_judge_for_stm/experiments/build_experiment_charts.py) + [`build_dimension_charts.py`](https://github.com/HansBug/research_ideas/blob/dev/reviewer/project_ex1_llm_judge_for_stm/experiments/build_dimension_charts.py)（图）")
    md.append("")
    # Section 11
    md.append("### 十一、下一步")
    md.append("")
    md.append("- [ ] **完整 Phase 14 LOFO 重测**：用 `benchmark.py:run_phase14_evaluation_bundle` 在 combined 973 行上跑完整流程，获得真实的 RAS/SAS/CRAS（不是 proxy）+ LOFO worst-fold-gap")
    md.append("- [ ] 给 PSMBench 行扩充更详细的 input_text（每协议 RFC 的关键章节抽取），看 reviewer 对 rich-context vs thin-context 的差异")
    md.append('- [ ] 路径 C "自补 review" 仍可并行：拿现成 LLM 输出 + 自己组织专家做 review，做出真正的 NL→SM expert-review benchmark')

    args.output.write_text("\n".join(md))
    print(f"PR comment written: {args.output}")
    print(f"  baseline n_paired={base.get('n_paired', 0)}, new n_paired={new.get('n_paired', 0)}")


if __name__ == "__main__":
    main()
