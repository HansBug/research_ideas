# SC-13 Trace/Audit

## 目标

把一次完整 agent-loop 的流程、数据、日志、LLM interaction 与 final artifacts 写入单文件 run record。

## 输入

- `stage_records`: 全部 StageResultMeta。
- `iteration_records`: 每轮 DSL/feedback/repair/review。
- `llm_interactions`: prompt/response/replay meta。
- `environment`: git/pyfcstm/dependency/seed。

## 输出

- `agent_loop_run_record`: schema-valid JSON payload。
- `record_path`: `runs/<run_id>.agent_loop.json.gz`。
- `redaction_report`: secret 脱敏说明。

## 函数名或 prompt generator 名

- `write_agent_loop_run_record(...)`

## 最小示例

见 [`../fixtures/SC-13.json`](../fixtures/SC-13.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
