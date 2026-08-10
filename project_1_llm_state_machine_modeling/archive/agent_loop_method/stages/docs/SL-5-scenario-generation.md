# SL-5 场景生成

## 目标

在 parse+semantic+design pass 后生成 TestScenario 候选；ScenarioSet 冻结前可按 coverage gap 重试。

## 输入

- `nl`: 原始需求。
- `current_dsl`: 当前 DSL。
- `inspect_summary`: SD-4 摘要。
- `grounding_map`: NL/model 元素映射。

### LLM 输入

- NL + current_dsl + inspect JSON + design 摘要 + GroundingMap。

## 输出

- `scenario_candidates`: TestScenario 列表。
- `scenario_rationale`: 每个 scenario 覆盖的行为/元素。

### LLM 输出

- TestScenario 列表候选。

## 函数名或 prompt generator 名

- `build_sl5_scenario_generation_prompt(...)`

## 最小示例

见 [`../fixtures/SL-5.json`](../fixtures/SL-5.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

## 依赖关系

- stage id 由 `archive.agent_loop_method.stages.ids.ALL_STAGE_SPECS` 统一登记，禁止在 PR-1A/PR-1B 重新定义。
- prompt generator 位于 `archive/agent_loop_method/stages/`，只返回 message pack / markdown prompt，不调用 LLM provider。
- 若由 `archive/agent_loop_method/agents/*` wrapper 使用，wrapper 必须复用本 stage 的 prompt generator，避免 prompt drift。

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
