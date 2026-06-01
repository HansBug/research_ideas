# SD-10 RepairReview

## 目标

对 candidate 执行本地复验、target resolved、regression、GroundingMap diff 与 drift risk。

## 输入

- `nl`: 原始需求。
- `grounding_map`: required elements。
- `old_dsl`: 修复前 DSL。
- `candidate_dsl`: 修复后 DSL。
- `fix_plan`: 原始目标。
- `scenario_set`: frozen oracle。

## 输出

- `repair_review_feedback`: target_resolved/regression_detected/drift_risk/local_rejection。
- `repair_rejection`: 若拒绝，给 SD-8R 形成 RevisedFixPlan。

## 函数名或 prompt generator 名

- `run_sd10_repair_review(...)`

## 最小示例

见 [`../fixtures/SD-10.json`](../fixtures/SD-10.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
