# SL-9 修复

## 目标

基于 NL、FixPlan/RevisedFixPlan 与 selected diagnostics 生成 candidate repaired DSL。

## 输入

- `nl`: 原始需求。
- `current_dsl`: 修复前 DSL。
- `fix_plan_or_revised`: SD-8 输出。
- `grammar_digest`: pyfcstm DSL 约束。
- `preserve_list`: required grounded elements。

### LLM 输入

- NL + current_dsl + FixPlan/RevisedFixPlan + selected diagnostics + grammar + preserve list。

## 输出

- `candidate_dsl`: 候选修复 DSL。
- `repair_summary`: LLM 声明的修改点与原因。

### LLM 输出

- candidate repaired DSL + repair summary。

## 函数名或 prompt generator 名

- `build_sl9_repair_prompt(...)`

## 最小示例

见 [`../fixtures/SL-9.json`](../fixtures/SL-9.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
