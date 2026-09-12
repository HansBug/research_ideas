# SC-0 启动入口

## 目标

初始化一次 agent-loop 的 `StageContext`、配置快照与 stage graph。

## 输入

- `nl`: 原始自然语言需求。
- `config`: loop condition、enabled stages、policy profile、dataset provenance。

## 输出

- `stage_context_summary`: 初始 DSL/hash 为空，budget 与 stage_records 初始化。
- `run_record_seed`: run_id、created_at、schema_version。

## 函数名或 prompt generator 名

- `init_stage_context(...)`

## 最小示例

见 [`../fixtures/SC-0.json`](../fixtures/SC-0.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
