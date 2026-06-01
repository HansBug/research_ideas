# SL-7 轻量模型评审

## 目标

轻量 LLM-as-reviewer，补充 NL fidelity / holistic drift 风险，不替代 deterministic checks。

## 输入

- `nl`: 原始需求。
- `current_dsl`: 当前 DSL。
- `inspect_summary`: SD-4 摘要。
- `sim_summary`: SD-6 摘要。
- `grounding_map`: NL/model 元素映射。

### LLM 输入

- NL + current_dsl + inspect diagnostics + sim summary + GroundingMap。

## 输出

- `model_review_feedback`: decision/findings/risk/blocking_findings，并内嵌 `review_meta`。
- `model_review_feedback.review_meta`: provider/model/prompt hash/schema validation/cache key，以及 `decision_threshold`、`failure_policy`、`replay_key`。

### LLM 输出

- schema-valid ReviewDecision + findings + risk level。

## 函数名或 prompt generator 名

- `build_sl7_model_review_prompt(...)`

## 最小示例

见 [`../fixtures/SL-7.json`](../fixtures/SL-7.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

## 依赖关系

由 `method.stages.ids.ALL_STAGE_SPECS` 统一登记，禁止在 PR-1A/PR-1B 重新定义 stage id。

## 失败语义

- `skipped` 必须给出 `skipped_reason`。
- `error` 必须给出 `stage_error` 或 `output_validation_error`。
- `fail` 表示 stage 正常执行但发现阻塞问题，必须使对应 feedback 非 ok。
- `advisory` 不阻塞 `all_ok`，但必须进入 trace / run record。
- enabled stage 缺失 `StageResultMeta` 不得静默视为 ok。

## 常见失败模式

- enabled stage 未产出 `StageResultMeta`。
- output schema 与 fixture 不兼容。
- prompt-ready summary、hash、provenance 或 review meta 字段缺失。
