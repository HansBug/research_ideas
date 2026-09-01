# v60/current 与 X1v2 baseline 最终人工评测归档

本目录是 Paper1 当前 v60/current 与 X1v2 baseline v3 评测的稳定入口。当前 headline 来自
`derived/fair_comparison_v4/`：current 使用 `derived/manual_adjudication_v4_current_reaudit/`，
baseline 使用冻结的 `derived/manual_adjudication_v3_baseline_ni/`。旧人工裁定记录、旧 witness
audit 和 superseded reviews 只由 archive/provenance 入口保留，不混入当前人工真值。
current/v60 v4 是对既有 pane5 source-first 确认的逐条 raw/source/hash/relation
再验证；baseline v3 只对原非 K 逐条读 raw/source/ledger 后确认，原 K 是冻结副本。
两侧的 validity、relation、D/A、K/N/I 及成分分析均由人工完成；机器只读取这些已完成
制品，执行确定性校验、闭合和算术复算。内部 reviewer/subagent 记录仅是质量审阅与
provenance，不构成独立的人类 inter-rater 研究，也不替代人工裁定。

## 数据闭合

| 项目 | 数量 |
| --- | ---: |
| v60/current method cells / reports | `162 / 1271` |
| X1v2 baseline method cells / findings | `162 / 512` |
| expected issue / round-level expected | `145 / 435` |
| dense relation rows | `258535` |

每条 report/finding 恰有一条 FINAL decision；每条 decision 包含 raw path/pointer/hash、
作者 NL/PlantUML source refs、专属 reason/basis、W 证据、逐 expected relation，以及
pane5 人工监督确认、独立 subagent proposal、解盲和仲裁记录。结构化入口是
[fair comparison v4](./derived/fair_comparison_v4/README.md)、[current v4](./derived/manual_adjudication_v4_current_reaudit/README.md)、
[current v4 decisions](./derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json)、
[combined summary](./derived/fair_comparison_v4/combined_summary_v4.json)。baseline v3 的入口见
[v3 README](./derived/manual_adjudication_v3_baseline_ni/README.md)、[v3 decisions](./derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json)、
[v3 summary](./derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json) 和
[v3 reviews](./derived/manual_adjudication_v3_baseline_ni/reviews/)。

### Paper-facing predicate summary

v60 使用冻结的 19 个谓词 registry，分为 Structure (6)、Topology (4)、Trajectory
simulation (4) 和 Bounded verification (5) 四族。method summary 中有 12/19 个
distinct predicate IDs 产生过 terminal receipt；current v4 canonical decisions
中有 8/19 个 distinct predicate IDs 至少绑定到一条 report-bound finding。两者都是
ID 级指标，不是 finding、W2 或 hit 的覆盖率。X1v2 没有同构
predicate binding/receipt schema，因此 predicate usage 为 N/A，不是零。825/1271
和 303/825 仍保存在 fair-comparison summary 中，作为行级审计诊断，不替代 12/19
与 8/19。详细后端能力审计只属于内部 evaluation-only 目录。

## 当前主结果

完整的并列表格和论文口径只见[正式 v4 中文报告](./report/v60_current_vs_x1v2_baseline_v4_cn.md)。报告是当前唯一的纸面 headline 入口；current v4、baseline v3 和 fair comparison 的 JSON/TSV 是可审计事实源。旧 v2 summary、旧 report 和旧人工裁定记录只作为历史 provenance，不再构成当前并列结果。

本次 provider-free evaluation-only 归因见 [conversion attribution v1 overlay](./derived/conversion_attribution_v1/README.md)。它覆盖全部 291 条 current I（其中 118 条 NADC），确认 110 条方法内部机制、8 条 indeterminate，严格 confirmed lowering-only 为 0；不修改 canonical decisions、主 precision 或 headline。重跑 gate 的唯一结论为 `NO_RERUN`。

### Method-cost provenance

[final-talk cost audit v1](./derived/final_talk_cost_section7_v1/README.md) 是两侧 method generation provider cost 的当前入口。它只读取同一 `54 x 3 = 162` cell scope 中保存的 usage receipt，排除 evaluator、人工审核、CPU、存储和开发成本。ours 的完整 receipt closure 为 `$7.18277320`；baseline 只有 `$0.22523328` 的 known recorded subtotal，因为一条 billable schema-error attempt 没有保存 usage。故 baseline `method_cost_eligible=false`，完整成本和精确成本倍率均不发布。`raw/x1v2_baseline/method/corrected_cost_audit.json` 中的 `$6.77501040` 已标记为旧 current/evidence-discovery run 的 misbound historical provenance，不能作为 baseline 成本。

结构化入口如下：

- current/v60：[v4 decisions](./derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json)、[v4 TSV](./derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.tsv)、[v4 summary](./derived/manual_adjudication_v4_current_reaudit/summary_v4.json)。
- X1v2 baseline v3：[decisions](./derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json)、[TSV](./derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.tsv)、[summary](./derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json)。
- 统一比较层：[fair comparison README](./derived/fair_comparison_v4/README.md)、[combined summary](./derived/fair_comparison_v4/combined_summary_v4.json)、[manifest](./derived/fair_comparison_v4/fair_comparison_manifest_v4.json)。

### 数据源优先级与版本边界

报告中的 current headline 来自 `derived/manual_adjudication_v4_current_reaudit`，baseline
headline 来自 `derived/manual_adjudication_v3_baseline_ni`，统一指标来自
`derived/fair_comparison_v4`。旧数字不进入本报告；更新 headline 后必须重新运行
provider-free recompute、校验 manifest hash，并使报告、README、schema 与逐侧 summary 一致。

## 协议与边界

current/v60 评测协议为 `issue-189-195-manual-evidence-v2`；baseline 非 K v3 使用
`issue-189-195-baseline-ni-v3`。两者都先核事实，再由人工判 D/A，再逐条人工判
`FULL_MATCH/PARTIAL_MATCH/NO_MATCH`，并由人工确认 validity 与 K/N/I；机器只对已完成
裁定做确定性闭合和复算。`D0/A0 -> I`；人工确认有效的 `D2/D1 + positive relation -> K`；人工确认有效的 `D2/D1 + all NO_MATCH -> N`。D2/D1 本身仍可能在有效性复核后进入 I。A0 只允许
`FALSE_POSITIVE` 与 current-only `NOT_A_DEFECT_CLAIM`。W0/W1/W2 是独立证据轴，W2
必须有原始 executable object、typed input、精确 artifact hash、terminal true/false 和
receipt；baseline 没有同构 predicate receipt，predicate usage 显式为 `not_applicable`，
但 baseline W 仍按相同证据等级人工审计。I 不建立实质性 defect group；任何 I cluster
只作附录诊断，不能替代 report-based precision。

冻结 raw 中保留的 provider/model/prompt provenance 未被改写；这些历史元数据不进入
canonical classification，也不作为任一侧能力证据。历史 raw-first review 使用已去除这些字段的
[reviewer projection](./derived/manual_adjudication_v2/reviewer_projection_audit.json)，
两侧保留稳定 arm/pair/round token 和 source hash。X1v2 缺少同构 method commit、v60 人工裁定
仍有未定价 usage；这两项按 manifest 和报告披露为数据缺口，未用推算补齐。predicate planned
scope 与逐报告 report-bound usage 在 predicate audit 中分开保存。台账不完整、
人工归并粒度、L2 边界、baseline schema 差异以及观察性比较不能推出因果，均是当前限制。

raw-first 输入按同一字段 allowlist 投影：两侧 report 都映射到统一的 claim/reason，固定的
`location_text` 对两侧均为空；双方都附 pair 对应的 NL、PlantUML 和 source hash。projection
去除 `report_index`、raw JSON pointer、raw target hash、`element_refs` 和 baseline `where`，并为
每个 pair/round 提供两臂相同的 slot universe；无原始报告的 padding slot 为空，不是 finding，
也不进入审计或统计分母。精确 pointer/hash 只在 inventory、canonical decision 和提交后解盲的
`reviewer_unblind_mapping.json` 中保存。current 独有的 predicate、
receipt、W 或旧裁定字段，以及 baseline 不具备的字段，都不进入 reviewer 投影。完整
field-level mapping 见 [issue #195 冻结协议](https://github.com/HansBug/research_ideas/issues/195)。

## 离线复算

从仓库根执行：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_current_reaudit_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_baseline_v3.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_fair_comparison_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only
```

归档和发布面的文件清单分别见 [archive_manifest.json](./archive_manifest.json) 和
[publication_manifest.json](./publication_manifest.json)。publication manifest 只绑定 v4 report、
current v4、baseline v3、fair v4 和本轮 review；raw、v2 及其他历史层只由 archive manifest 保留。
