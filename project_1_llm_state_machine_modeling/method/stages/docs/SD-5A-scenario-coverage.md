# SD-5A 场景覆盖自检

## 目标

用 M1-M6 probes 检查 scenario 对关键行为差异的敏感性，并给出 retry directive。

## 输入

- `current_dsl`: 当前 DSL。
- `scenario_candidates`: SL-5 输出。
- `mutation_plan`: M1-M6 coverage probes。

## 输出

- `coverage_report`: passed/failed probes 与 gap。
- `retry_directive`: 是否回到 SL-5。

## 函数名或 prompt generator 名

- `run_sd5a_scenario_coverage(...)`

## 最小示例

见 [`../fixtures/SD-5A.json`](../fixtures/SD-5A.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
