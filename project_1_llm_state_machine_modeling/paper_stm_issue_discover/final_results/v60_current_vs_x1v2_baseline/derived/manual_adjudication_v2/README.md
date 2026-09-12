# 人工评测 v2（最终人工监督裁定）

本目录保存 issue #189/#195 对齐的最终人工监督评测。JSON 是 canonical source，TSV
是由 JSON 逐字段生成的固定列镜像。`v60_report_decisions.json` 的 `1271/1271` 条和
`x1v2_report_decisions.json` 的 `512/512` 条均已由用户授权的 pane5 主 session 逐条读取
冻结 raw、作者 NL/PlantUML 和必要的 ledger/artifact 证据后确认；subagent/LLM 只保留在
`proposals/` 和 review provenance 中，不能替代最终裁定。

评测顺序固定为：

`事实是否成立 -> D2/D1/D0/A0 -> report validity -> expected relation -> K/N/I -> hit/FP 派生`

## 文件状态

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `inventory.json` | FINAL | 从冻结 raw 重新枚举的双侧身份、路径、pointer 和 hash 闭合。 |
| `protocol_freeze_v2.md` | FINAL | D/A、relation、K/N/I、W、grouping 和分母规则。 |
| `v60_report_decisions.json` | FINAL | 1271 条逐条人工监督裁定，唯一一条 raw report 对应一条 decision。 |
| `x1v2_report_decisions.json` | FINAL | 512 条逐条人工监督裁定，唯一一条 baseline finding 对应一条 decision。 |
| `relation_decisions.json` | FINAL | `1783 * 145 = 258535` 条 dense relation。 |
| `hit_max_witness.json` | FINAL | 仅从最终 `VALID_KNOWN + FULL_MATCH` supporting report 派生。 |
| `group_decisions.json` | FINAL | 仅同 side、同 pair 的人工同质 N/I group。 |
| `summary.json` | FINAL | 由 canonical decisions 确定性重算的完整指标。 |
| `reference_ledger_aggregate.json` | FINAL | 从 frozen reference relation 重算的同单位 calibration aggregate。 |
| `predicate_witness_audit.json` | FINAL | current 的冻结 planned scope 与 report-bound 19-predicate usage/W 交叉表；baseline 明确 `not_applicable`。 |
| `review_log.json` | FINAL | 每条 report 的 raw-first blind chronology、pane5 attestation、仲裁和 blocker closure。 |
| `MANIFEST` | FINAL | canonical 文件、输入 hash 和 supporting artifact 的 SHA-256 清单。 |

## 最终确认边界

最终记录具有 `review_status=FINAL`、`human_confirmation=true`、
`human_supervised_session=true`、`final_adjudicator_id=human:pane5-supervised-adjudicator`。
`independent_reviewer_id=subagent:raw-first-independent-proposal` 明确是 subagent proposal，
不是第二位真人。每条记录的专属 `reason`、`basis`、`source_refs`、raw/source digest、
盲审事件和用户授权 attestation 均保存在 decision/review/evidence-read 文件中。

`D0/A0 -> INVALID -> I`；`D2/D1` 且存在 `FULL_MATCH/PARTIAL_MATCH` 为 `K`，全部
`NO_MATCH` 为 `N`。`PARTIAL_MATCH` 不计主 hit、不计 FP。W0/W1/W2 是独立证据轴；W2
必须有原始 executable object、typed input、精确 artifact hash、terminal true/false 和
receipt，缺一项按证据降为 W1/W0。group 不跨 side/pair，也不按文本相似度、状态名或
expected ID 自动合并。

predicate audit 将冻结 evaluator 的 planned scope 与逐报告 binding usage 分开：
`planned_scope`/`planned_in_frozen_scope` 表示冻结计划，`report_bound_plan_count` 表示本次
报告投影观察到的计划字段；两者都不改变人工 D/A、relation、hit、FP 或 W 规则。

## 输入与复算

本目录只读取归档 `raw/`、`reference/` 和版本化协议材料；不调用 provider、不重跑
method/Judge、不修改冻结 raw。`generate_manual_adjudication.py` 只生成 proposal，
`confirm_manual_adjudication.py` 只有在显式 pane5 输入与逐条 raw/source evidence digest
闭合后才可生成 FINAL；`recompute_manual_adjudication.py` 只做确定性派生。

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_manual_adjudication.py \
  --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_manual_adjudication.py \
  --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

reviewer-visible projection 的规则和 hash 见 `reviewer_projection_audit.json`：`location_text`
在两臂均固定为空，raw target hash/identity 仅在独立 proposal 提交后使用
`reviewer_unblind_mapping.json` 解盲。冻结 raw 中
保留的 provider/model/prompt provenance 是不可变历史字段；它们不进入 canonical semantic
decision，也不作为 baseline/current 的能力证据。缺失的作者/出版物元数据和未定价的旧
Judge usage 只作为显式 evidence gap/成本限制，不能补造。
