# EVALUATION_GATE.md — R4 评价门规则总表

## 0. 定位与边界

本文件是 `paper_stm_repair/pipeline/evaluation/` 的核心规则文档，合并维护 R4 原先分散在 diagnostic taxonomy、scenario schema、Better STM checklist、eligibility policy、human rubric 和 metrics table plan 中的长期规则。

R4 的任务不是生成或修正状态机，而是在 R5/R6 真实修正预演之前，把“什么样的样例能评价、什么样的问题要记录、什么样的场景能作为回归门、什么样的修正结果才允许称为 Better STM”落成可审计的评价门。

R4 可以声称：本目录定义并用四个静态样例 dry-run 了诊断、场景、准入与 Better STM 判定规则。R4 不能声称：修正循环已经有效、正式实验 protocol 已冻结、四例 dry-run 是最终实验集合、转换 / 规范化 recovery 是 repair 收益。

## 1. 证据优先级

| 等级 | 证据 | R4 用法 |
|---|---|---|
| A | [../conversion/reports/selected_seed_examples_conversion_report.json](../conversion/reports/selected_seed_examples_conversion_report.json)、规范化中间表示 JSON、loss ledger | R3 status / loss / 规范化中间表示事实真源。 |
| A | [../../selected_seed_examples/](../../selected_seed_examples/) 中 `nl.txt`、`stm0.*`、`source_meta.json` | 四例 dry-run 输入事实真源。 |
| A | [../../experiment_design/better_stm_definition.md](../../experiment_design/better_stm_definition.md) | Better STM 五条件定义真源。 |
| B | R3/R3.1 summary Markdown | 便于阅读的摘要；数字仍应回到 JSON / ledger 复核。 |
| C | PR comment / review comment | 施工与审查线索；长期规则需抽象进仓库文档后才可作为仓库事实。 |

## 2. Eligibility policy：R3 输出如何进入 R4/R5

Eligibility policy 决定 R3 输出能否进入 R4/R5/R6 的不同层级 dry-run。它只处理开发、冒烟与 protocol 草案，不冻结 R7 主实验最终纳入规则。

| R3 状态 / 来源 | R4 decision | 允许事项 | 禁止事项 |
|---|---|---|---|
| `converted` + 官方 SCXML/XML 规范化中间表示 | `complete` | 完整 diagnostic / scenario / checklist dry-run；可进入 R5 确定性 smoke。 | 不得声称已有修正收益。 |
| `partial` + 规范化中间表示可用 | `focused` | limited diagnostic / scenario dry-run；必须携带 loss caveat。 | 不得无 caveat 进入模型级 Better STM。 |
| `partial` + inventory-only 规范化中间表示 | `focused` 或 `supplementary` | inventory-level diagnostic、边界说明。 | 不得冒充纯 T0 状态机。 |
| `partial` + no 规范化中间表示 conversion | `blocked` | blocked / diagnostic-only / toolchain-boundary analysis。 | 不得做模型级 evaluation 或 repair proposal。 |
| `blocked / unsupported` | `blocked` | 记录原因、风险和后续修复建议。 | 不进入 R5/R6 model-level smoke。 |

### 2.1 R4 dry-run decision 枚举

| 值 | 含义 | 进入后续 |
|---|---|---|
| `complete` | 规范化中间表示可用且 R3 无已知 loss；可完整填 diagnostic / scenario / checklist。 | 可进入 R5 确定性 smoke。 |
| `focused` | 部分规范化中间表示或 inventory 可用，但必须携带 loss / caveat；只验证特定评价门能力。 | 只进入 limited smoke 或 supplementary。 |
| `blocked` | 规范化中间表示缺失或工具链边界阻塞；不能做模型级 evaluation。 | 只记录 blocked / diagnostic-only。 |
| `supplementary` | 有研究说明价值但不适合主评价集合。 | 仅补充分析。 |

### 2.2 R3.1 recovery 规则

R3.1 `main_eligibility_included=466` 表示 PlantUML 转换前 normalization/recovery 后的主 eligibility 线索。它可用于 R7/R8 扩大候选池，但不能在 R4/R5/R6 中被写成 Better STM 修正收益。

每个 dry-run 样例必须有 `eligibility_decision.json`，至少说明 R3 `status` 与 `status_reason_code`、规范化中间表示是否存在、`r4_dry_run_decision`、diagnostic / scenario / model-level / repair-loop smoke 是否允许、required caveats 与 evidence locators。Schema 见 [schemas/eligibility_decision.schema.json](./schemas/eligibility_decision.schema.json)。

## 3. Diagnostic taxonomy：问题如何分类

R4 diagnostic taxonomy 用于统一记录状态机问题、证据来源、严重级别和与 Better STM 五条件的关系。它不是最终缺陷分类论文贡献，而是修正循环前的评价门草案。

### 3.1 顶层 code family

| code 前缀 | 类别 | 典型来源 |
|---|---|---|
| `R4.DIAG.r3_conversion.*` | R3 转换 / 工具链 / loss 映射 | R3 report、规范化中间表示 JSON、loss ledger。 |
| `R4.DIAG.syntax.*` | 语法或解析问题 | 官方工具链、parser、schema validation。 |
| `R4.DIAG.semantic.*` | 状态 / 迁移 / guard / action 语义问题 | 规范化中间表示、NL 对照、人工裁决。 |
| `R4.DIAG.scenario.*` | 场景 / 回归 oracle 问题 | scenario suite dry-run。 |
| `R4.DIAG.traceability.*` | 证据链 / locator 缺失 | 文件路径、hash、raw locator。 |
| `R4.DIAG.boundary.*` | 超出 T0 / no-规范化中间表示 / inventory-only 边界 | partial / blocked 样例。 |

### 3.2 source_stage 枚举

| 值 | 含义 |
|---|---|
| `r3_conversion` | 来自 R3 转换报告、规范化中间表示 JSON 或 loss ledger。 |
| `static_semantic` | 来自静态结构检查。 |
| `design_rule` | 来自设计规则或表示纪律。 |
| `scenario` | 来自场景 / 回归 suite。 |
| `human_review` | 来自人工 rubric 或裁决。 |
| `unknown` | 暂无可靠来源；不得支撑 Better STM 主张。 |

### 3.3 severity 枚举

| severity | 阻塞含义 | 默认处理 |
|---|---|---|
| `blocking` | 阻止模型级 evaluation 或 Better STM 主张。 | 必须修复或降级为 blocked / supplementary。 |
| `high` | 显著影响语义、结构或实验纳入。 | R7 前必须裁决。 |
| `medium` | 影响局部维度或需要人工 caveat。 | 可进入 focused dry-run。 |
| `low` | 轻微问题或记录性 caveat。 | 不单独阻塞。 |
| `info` | 事实记录。 | 不阻塞。 |

### 3.4 repair_relevance 枚举

| 值 | 含义 |
|---|---|
| `must_fix` | 若进入修正循环，必须被修复或显式拒绝。 |
| `should_fix` | 建议修复；未修复需说明风险。 |
| `monitor` | 用于回归监控，不一定作为 repair 目标。 |
| `not_repair_target` | 不是 修正循环目标，例如 conversion-only loss 或工具链边界。 |

### 3.5 R3 到 R4 映射

| R3 code / 状态 | R4 diagnostic 建议 | 说明 |
|---|---|---|
| `R3.STATUS.converted` | `R4.DIAG.r3_conversion.converted` | 可作为完整 dry-run 前提，但不是 Better STM 改善证据。 |
| `R3.LOSS.timing.medium` | `R4.DIAG.r3_conversion.timing_loss` | 不得把 timing loss 自动当作 修正收益机会。 |
| `R3.LOSS.structure.high` | `R4.DIAG.r3_conversion.structure_loss` | 对 TTool inventory-only 样例阻止模型级 Better STM。 |
| `R3.LOSS.tooling.high` | `R4.DIAG.boundary.no_canonical_conversion` | no-canonical 样例只能 blocked / diagnostic-only。 |
| R3.1 `main_eligibility_included` | `R4.DIAG.r3_conversion.eligibility_recovered` | 只表示 conversion eligibility 线索，不表示 repair 收益。 |

Machine-readable diagnostic bundle 由 [schemas/diagnostic.schema.json](./schemas/diagnostic.schema.json) 约束。每条 diagnostic 至少要包含 code、source stage、severity、repair relevance、Better STM 条件链接和 evidence locator。

## 4. Scenario / regression suite：场景如何定义

R4 scenario schema 只定义后续 R5/R6/R7 可复用的最小场景结构。它不承诺本 PR 已具备完整仿真能力，也不把 dry-run 场景写成正式主实验。

### 4.1 最小字段

| 字段 | 说明 |
|---|---|
| `scenario_id` | 稳定 ID，例如 `R4.SCENARIO.llms_hldcs_mode_switch`。 |
| `source_nl_ref` | 指向 `selected_seed_examples/<id>/nl.txt`。 |
| `source_stm_ref` | 指向 `stm0.*` 或 R3 规范化中间表示。 |
| `initial_state` | 初始状态；未知时可为 `null`，但必须说明原因。 |
| `event_sequence` | 事件 / 条件序列；R4 可为空数组表示 blocked / placeholder。 |
| `expected_observation` | 期望状态、迁移或人工断言。 |
| `oracle_type` | oracle 类型，见下表。 |
| `is_regression_gate` | 是否可作为回归门。placeholder 不得为 true。 |
| `blocking_on_failure` | 失败是否阻塞后续 Better STM 主张。 |
| `evidence_locator` | 指向 NL、STM、规范化中间表示、R3 report 或 loss ledger。 |

### 4.2 oracle_type 枚举

| 值 | 含义 | 可作为 regression gate |
|---|---|---:|
| `reachability` | 检查某状态可达。 | 是，若 evidence 明确。 |
| `transition_presence` | 检查某迁移存在。 | 是，若 source/target/event 明确。 |
| `forbidden_transition` | 检查不应存在的迁移。 | 是，若 NL 明确禁止。 |
| `trace_prefix` | 检查 trace 前缀或事件序列。 | 是，若语义明确。 |
| `human_assertion` | 人工裁决断言。 | 可作为辅助，不宜单独作自动门。 |
| `placeholder` | 字段占位或设计讨论。 | 否。 |

### 4.3 partial / blocked 规则

1. `partial` 样例可有 focused scenario，但必须在 `limitations` 中列出 R3 loss。
2. `blocked` 样例可以有 `placeholder` scenario 来记录为何不能构造回归门。
3. no-canonical 样例不得伪造 initial state、transition 或 trace。
4. 若 scenario 使用 `placeholder` 或关键 `unknown`，对应 Better STM checklist 不能 pass。

场景 suite 由 [schemas/scenario.schema.json](./schemas/scenario.schema.json) 约束。

## 5. Better STM checklist：什么时候可以说变好了

本 checklist 直接操作化 [../../experiment_design/better_stm_definition.md](../../experiment_design/better_stm_definition.md) 中的定义：$Better(STM_k, STM_0 \mid NL, S, D, R)$。

R4 没有 `STM_k`，因此本目录中的 checklist 是评价门 dry-run：验证字段、证据与聚合逻辑可执行，而不是声称任何样例已经 Better。

### 5.1 五条件

| 字段 | 条件 | R4 判定要点 |
|---|---|---|
| `no_new_blocking_diagnostics` | `STM_k` 不得引入新的 blocking diagnostics。 | R4 无 `STM_k` 时通常 `not_applicable`；若 R3 已 no-规范化中间表示，可记为 `fail` 支撑 blocked。 |
| `no_critical_regression_on_frozen_scenarios` | 冻结场景 / 回归不退化。 | placeholder / unknown oracle 不能 pass。 |
| `improves_at_least_one_preregistered_dimension` | 至少一个预注册维度改善。 | R4 无 repair candidate，不能 pass。 |
| `no_nl_semantic_degradation` | 基于 NL 的裁决不退化。 | partial / no-规范化中间表示 通常 `unknown` 或 `not_applicable`。 |
| `conversion_gain_separated_from_repair_gain` | 转换 / 规范化 gain 与 修正收益 分离。 | R4 应明确 `pass`，并把 R3/R3.1 gain 标为不可计入 repair。 |

### 5.2 condition status 枚举

| 值 | 含义 | 是否支持 Better STM |
|---|---|---:|
| `pass` | 该条件已有明确证据满足。 | 是，但必须五条件同时满足。 |
| `fail` | 条件失败。 | 否。 |
| `not_applicable` | R4 无 `STM_k` 或该样例不进入模型级评价。 | 否。 |
| `unknown` | 证据不足。 | 否。 |

### 5.3 聚合规则

1. 只有五条件全部为 `pass` 时，`can_claim_better_stm=true`。
2. 任一条件 `fail`，整体为 `not_better` 或 `not_evaluable`。
3. 任一关键条件 `unknown`，整体不得为 Better STM。
4. `not_applicable` 不能当作 `pass`；R4 dry-run 默认 `can_claim_better_stm=false`。
5. R3/R3.1 转换 / 规范化 改善只能进入 转换归因，不得进入 修正收益。
6. `can_claim_better_stm=true` 时，`gain_归因` 必须为 `repair_loop`。

Checklist fixture 由 [schemas/better_stm_checklist.schema.json](./schemas/better_stm_checklist.schema.json) 约束。

## 6. Human rubric：人工裁决只用于评价

Human rubric v0 是 R4 对后续 R7/R8 人工裁决的草案化定义。它用于检查评价维度是否足以覆盖 NL fidelity、diagnostic closure、regression safety 与 semantic drift，不在 R4 执行正式人工评测。

| 维度 | 问题 | 建议评分 |
|---|---|---|
| NL fidelity / requirement coverage | `STM_k` 是否覆盖 `NL` 中关键状态、事件、约束和禁止行为？ | `improved / unchanged / degraded / unknown` |
| Diagnostic closure | 预注册 diagnostics 是否被关闭，是否引入新 blocking issue？ | `closed / partially_closed / not_closed / regressed / unknown` |
| Regression safety | 冻结场景 / 回归是否保持不退化？ | `pass / fail / unknown` |
| Guard/action/state semantics preservation | guard、action、状态层级是否保持需求语义？ | `preserved / changed_with_reason / drifted / unknown` |
| Traceability and auditability | 每项判断是否能追到 NL、STM、scenario、diagnostic 或人工 note？ | `complete / partial / missing` |
| Semantic drift / overfitting risk | 是否为通过测试删除需求行为或过拟合场景？ | `low / medium / high / unknown` |
| Confidence and adjudication notes | 裁决者置信度与冲突说明。 | `high / medium / low` + free text |

人类可参与评价构造、reference / adjudication 与最终审计；修正循环 运行内部不能把人工临时干预写成无人化方法贡献。Rubric 结构由 [schemas/human_rubric.schema.json](./schemas/human_rubric.schema.json) 约束；当前 machine-readable 草案见 [human_rubric_v0.json](./human_rubric_v0.json)。

## 7. Metrics table plan：后续结果如何报告

本节预注册 R7/R8 结果表的字段骨架，避免后续根据 repair 结果临时挑选指标。R4 只冻结表头与解释，不填主实验数字。

### 7.1 Table A：eligibility / 转换归因

| 字段 | 含义 |
|---|---|
| `seed_id` / `example_id` | 样例来源。 |
| `raw_format` | PlantUML / Umple / TTool XML 等。 |
| `r3_status` | `converted / partial / blocked / unsupported`。 |
| `conversion_losses` | R3 loss code 计数。 |
| `conversion_gain_counted_as_repair` | 必须为 `false`，除非单独实验条件。 |
| `r4_decision` | `complete / focused / blocked / supplementary`。 |

### 7.2 Table B：diagnostic closure

| 字段 | 含义 |
|---|---|
| `run_id` | repair run 标识。 |
| `diagnostics_before_repair` | 转换后 `STM_0` 诊断计数。 |
| `diagnostics_after_repair` | `STM_k` 诊断计数。 |
| `new_blocking_diagnostics` | 新增 blocking 数量。 |
| `closed_must_fix` | `must_fix` 关闭数量。 |

### 7.3 Table C：scenario / regression

| 字段 | 含义 |
|---|---|
| `scenario_count` | 冻结场景数量。 |
| `regression_gate_count` | 可作为回归门的场景数量。 |
| `pass_before` / `pass_after` | 修正前后通过数。 |
| `critical_regression_count` | 关键回归数量。 |
| `placeholder_or_unknown_count` | 不得计入主通过率的占位 / unknown 数。 |

### 7.4 Table D：Better STM five-condition ledger

| 字段 | 含义 |
|---|---|
| `no_new_blocking_diagnostics` | pass/fail/unknown/not_applicable。 |
| `no_critical_regression_on_frozen_scenarios` | pass/fail/unknown/not_applicable。 |
| `improves_at_least_one_preregistered_dimension` | pass/fail/unknown/not_applicable。 |
| `no_nl_semantic_degradation` | pass/fail/unknown/not_applicable。 |
| `conversion_gain_separated_from_repair_gain` | pass/fail/unknown/not_applicable。 |
| `can_claim_better_stm` | 只有五项全 pass 才为 true。 |

### 7.5 报告原则

1. 失败、回滚、不收敛、blocked 不能被静默删除。
2. 四例冒烟结果只能作为开发证据，不进入主结果统计。
3. partial / inventory-only / no-canonical 样例必须单独分层报告。
4. 没有 Codecov 时不得虚构 coverage，只能说明本地测试与 GitHub 冒烟的局限。
