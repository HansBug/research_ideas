# Paper1 结果处置清单

本清单只处置 v60/current 与 X1v2 baseline v3 的既有 canonical 指标。每个 `included_in_main` 或 `included_in_appendix` 指标已在唯一大纲的相应段落解释；本清单不复制结果表，也不形成第二个结果真源。除另有注明外，公平比较指标的 canonical pointer 为 `final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json`。

| 指标组与冻结数值 | disposition | canonical source | 论文处理与限制 |
| --- | --- | --- | --- |
| 数据结构：9 个在用自然语言簇、每簇 6 个制品、54 pair、145 条 source-backed expected issues、3 rounds、435 round-level units | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json`；`derived/fair_comparison_v4/protocol_freeze_v4_fair_comparison.md` | Table 4 和第 8 节说明 54 不是独立需求数，435 是 145 条问题的三轮重复观测。 |
| overall FULL `hit@1`：current `310/435=71.26%`，baseline `227/435=52.18%` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | Table 5 和 RQ1 主回答；只作本案例研究的描述性比较。 |
| L2 FULL `hit@1`：current `105/117=89.74%`，baseline `50/117=42.74%` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | Table 5 的分层结果；117 是 L2 round-level units，不和 435 混用。 |
| overall FULL `hit@3`：current `119/145=82.07%`，baseline `106/145=73.10%` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | Figure 3/Table 6 的 coverage 曲线端点；分母是 unique expected issues。 |
| overall FULL `hit@all`：current `86/145=59.31%`，baseline `46/145=31.72%` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | RQ1 的深度覆盖补充，不能解释成每轮独立成功率。 |
| L2 FULL `hit@3`：current `37/39=94.87%`，baseline `26/39=66.67%`；`hit@all`：`33/39=84.62%` 对 `8/39=20.51%` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | 第 9.1 节直接解释；39 是 L2 unique expected issues。 |
| supported coverage：round units current `337/435=77.47%`、baseline `264/435=60.69%`；unique IDs `128/145=88.28%`、`119/145=82.07%` | `included_in_appendix` | `derived/fair_comparison_v4/combined_summary_v4.json` | 附录完整分层表；正文仅用于说明它不替代 PRIMARY FULL hit。 |
| reports：current `1271`，baseline `512` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | 与 precision 同列，显示 coverage 增加伴随更多报告。 |
| report validity precision：current `980/1271=77.10%`，baseline `417/512=81.45%`，差 `-4.34 pp` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | Figure 3/Table 6 报告 coverage--precision 权衡；这是 report-level validity，不是状态机语义真值率。 |
| FULL hits 的最大 W：current W0/W1/W2=`0/113/197`（分母 310），baseline=`0/227/0`（分母 227） | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json`；`related_work/provenance/predicate_provenance.md` | Table 7 报告冻结 runtime witness 分布；baseline 没有同构 receipt schema。G2 的 2 条、V4 的 88 条和 source-authority 未闭合的 125 条历史 false W2 不得按更强的发表命题解释。 |
| receipt/binding 使用：terminal-receipt predicate IDs `12/19`，report-bound predicate IDs `8/19` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | Table 7；这是 distinct-ID usage，不是 defect coverage、边际贡献或 baseline 的等价零值。 |
| K/N/I：current `749/231/291`，baseline `312/105/95` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | RQ3 说明机器在既有人工字段上闭合的记账类别，不能把 K/N/I 当作缺陷类型。 |
| D2/D1/D0/A0：current `721/259/120/171`，baseline `342/75/85/10` | `included_in_main` | `derived/fair_comparison_v4/combined_summary_v4.json` | RQ3 的人工裁定组成；不暗示独立双人标注或一致性统计。 |
| current I 组成：D0 `120`、ordinary source-level FP `53`、NADC `118` | `included_in_main` | `derived/conversion_attribution_v1/i_attribution_summary_v1.json` | Table 8 分开 source-artifact issue 与方法边界；三类只在 current 侧有完整诊断。 |
| NADC overlay：compiler-owned `38`、projection/trace boundary `24`、runtime/evidence closure `48`、attribution-indeterminate `8`；confirmed lowering-only=`0` | `included_in_main` | `derived/conversion_attribution_v1/i_attribution_summary_v1.json` | Table 8；不将 NADC 当作 baseline 的零值，也不将 conversion 写成 precision gap 的主因。 |
| N reports：current `231`、baseline `105`；D2/D1 composition：`38/193`、`50/55`；conservative substantive N groups：`121`、`98` | `included_in_appendix` | `derived/fair_comparison_v4/combined_summary_v4.json`；baseline `derived/manual_adjudication_v3_baseline_ni/baseline_n_groups_v3.json` | 附录解释 N 的异质性；grouping 不是主 precision 分母。 |
| report-bound binding rows `825/1271=64.91%`；其中 legacy coverage markers `303/825=36.73%` | `included_in_appendix` | `derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json` | 附录诊断 binding surface；不推 predicate coverage 或因果贡献。 |
| current method cost `$7.18277320` 完整；baseline `$0.22523328` 为不完整小计 | `included_in_main` | `derived/final_talk_cost_section7_v1/cost_summary_v1.json` | Table 9 逐项标明 eligibility；缺失 billable schema-retry usage receipt，故不计算成本倍率。 |
| G2 publication exclusion：`0020:r3:i1:receipt`、`0020:r3:i5:receipt` 共 2 条历史 W2；V4 exclusion：82 条 terminal-false 加 6 条 terminal-true，共 88 条；source-authority exclusion：125 条历史 false W2 | `included_in_appendix` | `related_work/provenance/current_source_catalog.json`；`related_work/provenance/predicate_provenance.md` | 附录 soundness table 只收窄论文级极性解释。125 条仅排除“source-bound mechanical counterexample”这一更强解释；三类均绝不改 canonical W、report 或 headline metric。 |
| 19 条谓词来源库存历史数 `313/310/454/361` | `excluded_with_reason` | `related_work/provenance/archive/legacy_20260821/SUMMARY.md` | 它们是来源库存/筛选规模，不是 prevalence 分母或本案例研究效果。 |
| 显著性、总体效应和 population-level confidence interval | `excluded_with_reason` | 冻结设计与上述 canonical summary | 435 单元嵌套于 54 artifacts/9 NL clusters，且当前论文只报告描述性比较；不能按 IID 作推断。 |
| C1 inspect on/off 的 paired causal gain | `excluded_with_reason` | 冻结端到端比较与 `story/experiment_dependent_gates.json` | conversion 与 inspect/C2 耦合；没有保持 conversion 不变的 paired switch 实验，不能从端到端差异识别 C1 单独效应。 |
| 跨状态机语言效果、审查工时、生产率、安全认证或部署结果 | `excluded_with_reason` | `story/model_scope.md`；冻结 PlantUML 案例研究 | 本研究只实现并评测 PlantUML adapter，未运行跨语言或 human-outcome study。 |
