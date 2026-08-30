# v60/current 与 X1v2 baseline 最终人工评测归档

本目录是 Paper1 当前 v60/current 与 X1v2 baseline v3 评测的稳定入口。当前 headline 来自
`derived/fair_comparison_v4/`：current 使用 `derived/manual_adjudication_v4_current_reaudit/`，
baseline 使用冻结的 `derived/manual_adjudication_v3_baseline_ni/`。旧 Judge、旧 witness
audit 和 superseded reviews 只由 archive/provenance 入口保留，不混入当前人工真值。
current/v60 v4 是对既有 pane5 source-first 确认的逐条 raw/source/hash/relation
再验证；baseline v3 只对原非 K 逐条读 raw/source/ledger 后确认，原 K 是冻结副本。

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

## 当前主结果

完整的并列表格和论文口径只见[正式 v4 中文报告](./report/v60_current_vs_x1v2_baseline_v4_cn.md)。报告是当前唯一的纸面 headline 入口；current v4、baseline v3 和 fair comparison 的 JSON/TSV 是可审计事实源。旧 v2 summary、旧 report 和旧 Judge 只作为历史 provenance，不再构成当前并列结果。

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
`issue-189-195-baseline-ni-v3`。两者都先核事实，再判 D/A，再逐条判
`FULL_MATCH/PARTIAL_MATCH/NO_MATCH`，最后由后端派生 validity 与 K/N/I。`D0/A0 -> I`；
`D2/D1 + positive relation -> K`；`D2/D1 + all NO_MATCH -> N`。A0 只允许
`FALSE_POSITIVE` 与 current-only `NOT_A_DEFECT_CLAIM`。W0/W1/W2 是独立证据轴，W2
必须有原始 executable object、typed input、精确 artifact hash、terminal true/false 和
receipt；baseline 没有同构 predicate receipt，predicate usage 显式为 `not_applicable`，
但 baseline W 仍按相同证据等级人工审计。I 不建立实质性 defect group；任何 I cluster
只作附录诊断，不能替代 report-based precision。

冻结 raw 中保留的 provider/model/prompt provenance 未被改写；这些历史元数据不进入
canonical semantic label，也不作为任一侧能力证据。历史 raw-first review 使用已去除这些字段的
[reviewer projection](./derived/manual_adjudication_v2/reviewer_projection_audit.json)，
两侧保留稳定 arm/pair/round token 和 source hash。X1v2 缺少同构 method commit、v60 Judge
仍有未定价 usage；这两项按 manifest 和报告披露为数据缺口，未用推算补齐。predicate planned
scope 与逐报告 report-bound usage 在 predicate audit 中分开保存。台账不完整、
人工归并粒度、L2 边界、baseline schema 差异以及观察性比较不能推出因果，均是当前限制。

raw-first 输入按同一字段 allowlist 投影：两侧 report 都映射到统一的 claim/reason，固定的
`location_text` 对两侧均为空；双方都附 pair 对应的 NL、PlantUML 和 source hash。projection
去除 `report_index`、raw JSON pointer、raw target hash、`element_refs` 和 baseline `where`，并为
每个 pair/round 提供两臂相同的 slot universe；无原始报告的 padding slot 为空，不是 finding，
也不进入审计或统计分母。精确 pointer/hash 只在 inventory、canonical decision 和提交后解盲的
`reviewer_unblind_mapping.json` 中保存。current 独有的 predicate、
receipt、W 或旧 Judge 字段，以及 baseline 不具备的字段，都不进入 reviewer 投影。完整
field-level mapping 见 [semantic Judge protocol](../../discover_matrix/docs/protocol/semantic_judge_protocol.md#双侧-reviewer-输入映射)。

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
