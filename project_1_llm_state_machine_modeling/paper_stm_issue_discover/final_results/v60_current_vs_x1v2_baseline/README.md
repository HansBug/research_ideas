# v60/current 与 X1v2 baseline 最终人工评测归档

本目录是 Paper1 当前 v60/current 与 X1v2 baseline 评测的稳定入口。current/v60 的主结果
来自 `derived/manual_adjudication_v2/`，X1v2 baseline 的本次非 K 重审来自
`derived/manual_adjudication_v3_baseline_ni/`；两层共同组成当前并列发布结果。旧 Judge v3.2、
旧 witness audit 和 superseded reviews 只作为历史资料，不混入当前人工真值。

版本边界：冻结 raw 中的 `v3.2` 是历史 Judge 输入/输出身份；`v3.3` 是后续
evaluator/protocol implementation 版本。两者都不是本次论文人工真值，不能被重命名为
人工标签；current/v60 真值只来自 `manual_adjudication_v2` 的逐条 pane5 监督确认和确定性
派生；baseline v3 只对原非 K 逐条读 raw/source/ledger 后确认，原 K 是 v2 冻结副本。

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
和 [review log](./derived/manual_adjudication_v2/review_log.json)。baseline v3 的入口见
[v3 README](./derived/manual_adjudication_v3_baseline_ni/README.md)、[v3 decisions](./derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json)、
[v3 summary](./derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json) 和
[v3 reviews](./derived/manual_adjudication_v3_baseline_ni/reviews/)。

## 当前主结果

完整的并列表格和论文口径见[正式中文报告](./report/v60_current_vs_x1v2_baseline_cn.md)。报告是当前发布面的唯一 headline 入口；current/v2 和 baseline/v3 的逐侧 canonical JSON 是可审计事实源，不能把旧的 v2 baseline summary 当成 v3 并列结果。
下列仅列入口，不另建第二事实源：

- current/v60 的逐条裁定：[v60 decisions](./derived/manual_adjudication_v2/v60_report_decisions.json) 与 [current summary](./derived/manual_adjudication_v2/summary.json)；
- X1v2 baseline v3 的逐条非 K 重审：[baseline v3 decisions](./derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json) 与 [baseline v3 summary](./derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json)。`derived/manual_adjudication_v2/x1v2_report_decisions.json` 仅作为 v3 冻结 K 的历史 provenance，不是当前 baseline headline 的事实源。

- v60/current：`D2/D1/D0/A0 = 721/259/120/171`；`K/N/I = 749/231/291`；ledger `K_hit/N_group/I_group = 119/121/189`。
- X1v2 baseline v3：`D2/D1/D0/A0 = 342/75/85/10`；`K/N/I = 312/105/95`；ledger `K_hit/N_group/I_group = 106/98/95`。
- v60/current 与 X1v2 baseline v3 的 report-based precision 分别为 `980/1271 = 77.10%` 与 `417/512 = 81.45%`；按各自有效单位公式得到的 ledger/group 诊断比值 `240/429 = 55.94%` 与 `204/299 = 68.23%` 只作诊断，不是论文主 precision。

这些数字的单位不同。论文主结果只使用逐条 report-based precision：
`(K reports + N reports) / all reports`。ledger/group 数值使用台账 `K_hit` 与同 side、同
pair、跨 round 的 N substantive groups；I 只能保留为 invalid diagnostic cluster，不能被
当作实质缺陷 group，因此该数值不用于主 precision。PARTIAL 只进入 supported coverage，
不进入主 hit 或 FP。L2 ledger precision/FP 为 `not_applicable`，因为 N/I 没有自然的 L2
expected 归属。

### 数据源优先级与版本边界

报告中的 current headline 来自 `derived/manual_adjudication_v2`，baseline headline 来自
`derived/manual_adjudication_v3_baseline_ni`。如果旧的独立派生文件仍出现
`306/435`、`118/145` 或 `84/145` 等历史数字，它们只能作为历史复算记录，不能和当前报告
混用。更新任何 headline 后，必须重新运行 provider-free recompute、校验 manifest hash，
并使报告、README、SCHEMA 与逐侧 summary 一致。

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
