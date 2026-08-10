# SC-5F 冻结 ScenarioSet

## 目标

冻结 scenario oracle，记录 source_dsl_hash / inspect_hash / coverage_report；repair iteration 默认不自动换 oracle。

## 输入

- `scenario_candidates`: 已通过或达到预算上限的 scenarios。
- `source_dsl_hash`: 冻结时 DSL hash。
- `coverage_report`: SD-5A 报告。

## 输出

- `scenario_set`: frozen ScenarioSet。
- `scenario_epoch`: 初始 epoch。

## 函数名或 prompt generator 名

- `freeze_scenario_set(...)`

## 最小示例

见 [`../fixtures/SC-5F.json`](../fixtures/SC-5F.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

## 依赖关系

由 `archive.agent_loop_method.stages.ids.ALL_STAGE_SPECS` 统一登记，禁止在 PR-1A/PR-1B 重新定义 stage id。

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
