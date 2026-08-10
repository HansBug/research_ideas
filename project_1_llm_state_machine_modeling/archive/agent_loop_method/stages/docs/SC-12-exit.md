# SC-12 收敛退出

## 目标

当 feedback/review 均通过或达到终止条件时形成 final result。

## 输入

- `final_feedback`: 最后一轮 feedback bundle。
- `iter_traces`: 所有 iteration traces。
- `exit_policy`: converged/not_converged/error。

## 输出

- `agent_loop_result`: final_dsl/status/final_feedback/run_record_id。
- `final_verdict`: success/failed/rejected/budget_exhausted/error。

## 函数名或 prompt generator 名

- `finalize_agent_loop_result(...)`

## 最小示例

见 [`../fixtures/SC-12.json`](../fixtures/SC-12.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
