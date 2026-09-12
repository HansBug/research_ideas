# SD-6 SimFeedback

## 目标

用 frozen ScenarioSet 运行 SimulationRuntime，记录每步 actual state/vars/mismatches。

## 输入

- `current_dsl`: 当前 DSL。
- `scenario_set`: SC-5F 冻结的 oracle。

## 输出

- `sim_feedback`: pass/fail/error、scenario_results、setup_error。
- `prompt_ready_summary`: 面向 repair 的失败摘要。

## 函数名或 prompt generator 名

- `run_sd6_sim(...)`

## 最小示例

见 [`../fixtures/SD-6.json`](../fixtures/SD-6.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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

## PR-1A 工具入口

```python
from archive.agent_loop_method.stages.sd_tools import run_sd6_sim

sim_feedback, meta = run_sd6_sim(current_dsl, frozen_scenario_set, context)
```

输入必须是 `ScenarioSet`；缺失时返回显式 `SimFeedback(ok=False, setup_error=...)` 与 `StageStatus.ERROR`，不得静默跳过 enabled sim。
