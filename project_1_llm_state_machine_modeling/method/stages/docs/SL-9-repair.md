# SL-9 修复

## 目标

基于 NL、FixRequestBatch、完整 FixLog 与 selected diagnostics，对每个 request 做 accept/reject 决策，并在至少 accept 一个 request 时生成 candidate repaired DSL。

## 输入

- `nl`: 原始需求。
- `current_dsl`: 修复前 DSL。
- `fix_request_batch`: SD-8 输出的 request batch。
- `fix_log`: 跨 iteration repair ledger。
- `grammar_digest`: pyfcstm DSL 约束。
- `preserve_list`: required grounded elements。

### LLM 输入

- NL + current_dsl + FixRequestBatch + 完整 FixLog + selected diagnostics + grammar + preserve list + scenario summary。

## 输出

- `decisions`: 每个 request 的 accept/reject、理由、waiver/rework_locked 信息。
- `candidate_dsl`: 至少 accept 一个 request 时的候选修复 DSL。
- `repair_rationale`: LLM 声明的修改点与原因。

### LLM 输出

- JSON：`decisions` + `candidate_dsl` + `repair_rationale` + `diff_summary`；legacy DSL-only 仅作为兼容 fallback。

## 函数名或 prompt generator 名

- `build_sl9_repair_prompt(...)`

## 最小示例

见 [`../fixtures/SL-9.json`](../fixtures/SL-9.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

Repair prompt 必须明确：`suggested_fix` / `suggested_fix_hints` 只是 hint, not a command；优先最小编辑、保护 NL-grounded required elements，并保持 passing scenarios 不回退。若 `SL-10` 标记 rework_locked，SL-9 必须继续修复，不得再次 reject 同一返工 request。

## 依赖关系

- stage id 由 `method.stages.ids.ALL_STAGE_SPECS` 统一登记，禁止在 PR-1A/PR-1B 重新定义。
- prompt generator 位于 `method/stages/`，只返回 message pack / markdown prompt，不调用 LLM provider。
- 若由 `method/agents/*` wrapper 使用，wrapper 必须复用本 stage 的 prompt generator，避免 prompt drift。

## 失败语义

- `skipped` 必须给出 `skipped_reason`。
- `error` 必须给出 `stage_error` 或 `output_validation_error`。
- `fail` 表示 stage 正常执行但发现阻塞问题，必须使对应 feedback 非 ok。
- `advisory` 不阻塞 `all_ok`，但必须进入 trace / run record。
- enabled stage 缺失 `StageResultMeta` 不得静默视为 ok。

## 常见失败模式

- prompt generator 直接调用 LLM provider、读取 `.env` 或绑定特定 provider。
- output schema 与 fixture / fake response parser 不兼容。
- prompt 缺少输入、输出 JSON/DSL schema、约束或禁止事项。
- 内部 agent wrapper 与 stage prompt generator 维护两套不一致 prompt。
