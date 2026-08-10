# SC-11 接受 candidate

## 目标

接受通过 `SL-10` repair review 的 candidate，更新 `current_dsl` 并进入下一轮 `SD-2` 完整重验；`SC-11` 不是 final success。

## 输入

- `candidate_dsl`: 已通过 `SL-10` 的 DSL。
- `sl10_repair_review`: `pass` 决策及 NL / FixLog / local evidence 依据。
- `fix_log`: request / decision / diff / review ledger。

## 输出

- `current_dsl`: 更新后的 DSL。
- `acceptance_record`: accepted_by=`SL-10`、hash、iteration、preserved scenario epoch。

## 函数名或 prompt generator 名

- `accept_repair_candidate(...)`

## 最小示例

见 [`../fixtures/SC-11.json`](../fixtures/SC-11.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
