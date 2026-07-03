# repair_target_adjudication/ — R5.7.4 静态裁决 dry-run

本目录保存 R5.7.4 的 **修复目标静态裁决与客观指标 dry-run**。它的作用是把 R5.7.1 的评价逻辑链、R5.7.2 的 Better STM / repair target 合同、R5.7.3 的客观代理指标框架，放到真实 `llms-emp` 样例上做可执行性检查。

> 关键边界：本目录不运行 repair loop，不调用真实 LLM，不读取 `.env`，不生成 `STM_k`，不报告 Better STM 成功率，也不把 `.fcstm` / `pyfcstm` / converter 写成论文贡献。

## 1. 阅读顺序

1. 先读上游规则：
   - [../evaluation_logic.md](../evaluation_logic.md)：R5.7.1 评价逻辑链、claim boundary、分母纪律。
   - [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md)：R5.7.2 G0--G6 gate、三层输出模型。
   - [../quality_model/repair_target_taxonomy.md](../quality_model/repair_target_taxonomy.md)：R5.7.2 repair target taxonomy、五级 `repair_action_allowed`。
   - [../metrics/objective_metric_framework.md](../metrics/objective_metric_framework.md)：R5.7.3 五级 `metric_permission` 与指标证据层。
2. 再读本 README，理解四个 dry-run 样例分别覆盖什么。
3. 最后进入单个样例文件；若需要 paper-facing 汇总，读 [../../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](../../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md)。

## 2. 四个样例

| 样例 | 角色 | 文件 | 裁决用途 |
|---|---|---|---|
| `llms_emp_stm_results_0000` | T0 / HSM / partial / condition-like | [2026-07-03-23-44-12-llms-emp-0000-hldcs-gpt4o.md](./2026-07-03-23-44-12-llms-emp-0000-hldcs-gpt4o.md) | 验证 `condition_like_label_lowered_as_event` 能否回到 `NL + raw STM_0` 被裁决为后续 guard target，同时保留 composite/source lifting 的 representation caveat。 |
| `llms_emp_stm_results_0001` | T0 / FSM / converted / low-noise | [2026-07-03-23-44-12-llms-emp-0001-hstbs-gpt4o.md](./2026-07-03-23-44-12-llms-emp-0001-hstbs-gpt4o.md) | 验证 taxonomy 不会在无 loss、无明确缺陷的样例上强行制造 repair target。 |
| `llms_emp_stm_results_0045` | T0.5 / Microwave / timer-like caveat | [2026-07-03-23-44-12-llms-emp-0045-microwave-deepseek.md](./2026-07-03-23-44-12-llms-emp-0045-microwave-deepseek.md) | 验证 timer / zero-time / normalization replay 只能进入 caveat / monitor，不进入 T0 headline 或 repair gain。 |
| `llms_emp_stm_results_0018` | T1 / Digital Camera / supplementary stress | [2026-07-03-23-44-12-llms-emp-0018-digital-camera-gpt4.md](./2026-07-03-23-44-12-llms-emp-0018-digital-camera-gpt4.md) | 验证 T1 timing、fork/choice、cross-scope 等复杂状态图只能作 stress / limitation，不进入 Better 主比较。 |

## 3. 统一裁决纪律

每个样例都同时记录两层状态：

| 字段 | 含义 | 本轮允许写法 |
|---|---|---|
| `static_dry_run_preflight` | 当前证据是否足够支撑静态 dry-run。 | 四例均可写 `pass`，但只表示输入证据足够。 |
| `run_validity_status` | R5.7.2 canonical enum：正式 Better STM run 是否具备 `STM_k`、change ledger、run record 等最低证据。 | 本轮必须写 `protocol_or_provenance_invalid`。 |
| `run_validity_reason` | 对 canonical `run_validity_status` 的阶段性解释。 | 本轮写 `static_dry_run_without_stmk_change_ledger_or_run_record`，不得把该原因拼进 enum 值。 |
| `better_adjudication_outcome` | R5.7.2 canonical enum：正式 Better STM 裁决输出。 | 本轮必须写 `unknown`；不得写 `better`。 |
| `better_outcome_reason` | 对 canonical `better_adjudication_outcome` 的阶段性解释。 | 本轮写 `not_evaluated_in_static_dry_run`，不得把该原因拼进 enum 值。 |
| `dry_run_taxonomy_finding` | 静态规则检查发现。 | 可写 target confirmed / monitor / not target / stress / caveat，但不得把它写成 repair effectiveness。 |

## 4. 必须保留的证据链

每个样例必须至少回到以下事实源：

| 证据层 | 事实源 | 用途 |
|---|---|---|
| `NL` 与 raw `STM_0` | [../../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl](../../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl) | 判断候选问题是否有需求和 raw source 证据。 |
| case matrix | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | 读取 time level、结构族、conversion status、parse / inspect 状态和 loss codes。 |
| partial attribution ledger | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | 区分 candidate-only、pipeline artifact、conversion artifact 和 source defect。 |
| record archive | [../../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip](../../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip) | 复核 record 级 hash、canonical / parse / inspect、loss reason codes。 |
| selected smoke `.fcstm` | [../../selected_seed_examples/](../../selected_seed_examples/) | 仅对 0000 / 0045 有 standalone snapshot；0001 / 0018 目前只有 hash / status，没有 standalone `.fcstm` 文件。 |

## 5. R6 / R7 handoff 纪律

1. R6 若消费这些样例，必须先物化 canonical baseline 与 candidate `STM_k` 的可追溯 evidence bundle。
2. R7 若把某个 dry-run target 写入正式指标，必须有 target-instance ledger、change ledger、scenario / trace / semantic gate 证据。
3. 0001 / 0018 当前只有 seed-sweep hash 与 parse / inspect status，没有 standalone `.fcstm` 文本，这是 R6/R7 执行前必须物化的 baseline evidence bundle 缺口。
4. 0000 / 0045 已有 selected smoke standalone `.fcstm`；其 selected hash 与 seed-sweep hash 不同属于不同转换运行的预期差异，不是缺失，但 R6/R7 必须明确 authoritative baseline hash，并把 seed-sweep hash 保留为 audit trail。
5. 后续修改 taxonomy 或指标框架时，必须引用本目录或正式 R7 run 的真实 finding；不得空口改规则。
