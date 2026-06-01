# SD-4 DesignFeedback

## 目标

消费 `StageContext.model` 与 `inspect_model().diagnostics`，按 policy profile 分类 E/W/I 与 warning budget。

## 输入

- `model_summary`: SD-3 构建模型摘要。
- `inspect_json`: pyfcstm Layer1/2 diagnostics。
- `policy_profile`: generated_candidate / signed_ref 等策略。
- `warning_budget_state`: per diagnostic instance budget。

## 输出

- `design_feedback`: blocking/advisory/info items。
- `budget_decisions`: budgeted_repair / exhausted / advisory。
- `inspect_summary`: 给 SL-5/SL-7/SL-9 使用的摘要。

## 函数名或 prompt generator 名

- `run_sd4_design(...)`

## 最小示例

见 [`../fixtures/SD-4.json`](../fixtures/SD-4.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
