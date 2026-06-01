# SL-7 轻量模型评审

## 目标

轻量 LLM-as-reviewer，补充 NL fidelity / holistic drift 风险，不替代 deterministic checks。

## 输入

- `nl`: 原始需求。
- `current_dsl`: 当前 DSL。
- `inspect_summary`: SD-4 摘要。
- `sim_summary`: SD-6 摘要。
- `grounding_map`: NL/model 元素映射。
- `five_component_summary`: Path1/Path2 兼容的 5-component 摘要。
- `warning_budget_exhausted`: 已耗尽的 warning budget instance 列表。
- `review_policy`: fail-open / fail-closed / audit-only 等 ReviewPolicy。

### LLM 输入

- NL + current_dsl + inspect diagnostics + sim summary + GroundingMap + 5-component summary + warning budget exhausted + ReviewPolicy。

## 输出

- `model_review_feedback`: decision/findings/risk/blocking_findings，并内嵌 `review_meta`。
- findings category 必须映射到：`nl_fidelity`、`component_coverage`、`coverage_gap`、`over_simplification`、`unsafe_recovery`、`structure_smell`、`unjustified_warning_fix`、`path1_eval_risk`、`path2_grounding_risk`。
- `model_review_feedback.review_meta`: provider/model/prompt hash/schema validation/cache key，以及 `decision_threshold`、`failure_policy`、`replay_key`。

### LLM 输出

- schema-valid ReviewDecision + findings + risk level。

## 函数名或 prompt generator 名

- `build_sl7_model_review_prompt(...)`

## 最小示例

见 [`../fixtures/SL-7.json`](../fixtures/SL-7.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

## 依赖关系

- stage id 由 `method.stages.ids.ALL_STAGE_SPECS` 统一登记，禁止在 PR-1A/PR-1B 重新定义。
- prompt generator 位于 `method/stages/`，只返回 message pack / markdown prompt，不调用 LLM provider。
- 若由 `method/agents/*` wrapper 使用，wrapper 必须复用本 stage 的 prompt generator，避免 prompt drift。

## 失败语义

- `skipped` 必须给出 `skipped_reason`。
- `error` 必须给出 `stage_error` 或 `output_validation_error`。
- `fail` 表示 stage 正常执行但发现阻塞问题，必须使对应 feedback 非 ok。
- `advisory` 不阻塞 `all_ok`，但必须进入 trace / run record。
- enabled stage 缺失 `StageResultMeta` 不得静默视为 ok。

## 常见失败模式

- prompt generator 直接调用 LLM provider、读取 `.env` 或绑定特定 provider。
- output schema 与 fixture / fake response parser 不兼容。
- prompt 缺少输入、输出 JSON/DSL schema、约束或禁止事项。
- 内部 agent wrapper 与 stage prompt generator 维护两套不一致 prompt。
