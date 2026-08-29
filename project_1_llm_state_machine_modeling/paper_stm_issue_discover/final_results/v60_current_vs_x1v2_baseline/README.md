# v60/current 与 X1v2 baseline 最终人工评测归档

本目录是 Paper1 当前 v60/current 与 X1v2 baseline 评测的稳定入口。论文主结果只使用
`derived/manual_adjudication_v2/` 的最终人工监督逐条裁定；旧 Judge v3.2、旧 witness
audit、`reviews/11` 和 `reviews/12` 只作为显式标记的 calibration/proposal 或历史资料，
不混入主结果。

版本边界：冻结 raw 中的 `v3.2` 是历史 Judge 输入/输出身份；`v3.3` 是后续
evaluator/protocol implementation 版本。两者都不是本次论文人工真值，不能被重命名为
人工标签；当前真值只来自 `manual_adjudication_v2` 的逐条 pane5 监督确认和确定性派生。

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
[manual adjudication v2](./derived/manual_adjudication_v2/README.md)、[v60 decisions](./derived/manual_adjudication_v2/v60_report_decisions.json)、
[X1v2 decisions](./derived/manual_adjudication_v2/x1v2_report_decisions.json)、[summary](./derived/manual_adjudication_v2/summary.json)
和 [review log](./derived/manual_adjudication_v2/review_log.json)。

## 当前主结果

数值从 canonical JSON 离线重算，完整并列表格见[正式中文报告](./report/v60_current_vs_x1v2_baseline_cn.md)。
下列仅列入口，不另建第二事实源：

- v60/current：`D2/D1/D0/A0 = 721/259/120/171`；`K/N/I = 749/231/291`；ledger `K_hit/N_group/I_group = 119/121/189`。
- X1v2 baseline：`D2/D1/D0/A0 = 408/3/2/99`；`K/N/I = 279/132/101`；ledger `K_hit/N_group/I_group = 104/132/101`。
- v60/current 与 X1v2 的 report-based precision 分别为 `980/1271 = 77.10%` 与 `411/512 = 80.27%`；ledger-based precision 分别为 `119/429 = 27.74%` 与 `104/337 = 30.86%`。

这些数字的单位不同：report precision 使用逐条 validity；ledger precision 使用台账
`K_hit` 与同 side、同 pair 的跨 round N/I substantive groups。PARTIAL 只进入 supported
coverage，不进入主 hit 或 FP。L2 ledger precision/FP 为 `not_applicable`，因为 N/I
group 没有自然的 L2 expected 归属。

## 协议与边界

评测协议为 `issue-189-195-manual-evidence-v2`：先核事实，再判 D/A，再逐条判
`FULL_MATCH/PARTIAL_MATCH/NO_MATCH`，最后由后端派生 validity 与 K/N/I。`D0/A0 -> I`；
`D2/D1 + positive relation -> K`；`D2/D1 + all NO_MATCH -> N`。A0 只允许
`FALSE_POSITIVE` 与 current-only `NOT_A_DEFECT_CLAIM`。W0/W1/W2 是独立证据轴，W2
必须有原始 executable object、typed input、精确 artifact hash、terminal true/false 和
receipt；baseline 没有同构 predicate receipt，predicate usage 显式为 `not_applicable`，
但 baseline W 仍按相同证据等级人工审计。

冻结 raw 中保留的 provider/model/prompt provenance 未被改写；这些历史元数据不进入
canonical semantic label，也不作为任一侧能力证据。raw-first reviewer 使用去除这些字段
的 [reviewer projection](./derived/manual_adjudication_v2/reviewer_projection_audit.json)，
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
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_manual_adjudication.py \
  --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_manual_adjudication.py \
  --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

归档和发布面的文件清单分别见 [archive_manifest.json](./archive_manifest.json) 和
[publication_manifest.json](./publication_manifest.json)。
