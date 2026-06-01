# SD-8 FixPlan

## 目标

把 selected feedback 转成结构化 FixPlan 或 RevisedFixPlan；inspect suggested_fix 仅作为参考，不允许无脑执行。

## 输入

- `selected_feedback`: parse/semantic/design/sim/model_review/rejection。
- `grounding_map`: preserve 与 target hints。
- `policy_profile`: 修复策略与 edit scope。

## 输出

- `fix_plan`: target/severity/evidence/suggested_fix_hints/recommended_strategy/forbidden_edits。
- `revised_fix_plan`: 可选，保留 original target 并追加 rejection evidence。

## 函数名或 prompt generator 名

- `run_sd8_fix_plan(...)`

## 最小示例

见 [`../fixtures/SD-8.json`](../fixtures/SD-8.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
