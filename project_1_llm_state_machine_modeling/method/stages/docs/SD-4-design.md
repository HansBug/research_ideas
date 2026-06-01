# SD-4 DesignFeedback

## 目标

消费 `StageContext.model` 与 `inspect_model().diagnostics`，按 policy profile 分类 E/W/I 与 warning budget。

## 输入

- `model_summary`: SD-3 构建模型摘要。
- `inspect_json`: pyfcstm Layer1/2 diagnostics。
- `policy_profile`: generated_candidate / signed_ref 等策略。
- `warning_budget_state`: per diagnostic instance budget。

## 输出

- `design_feedback`: blocking/advisory/info items。
- `budget_decisions`: budgeted_repair / exhausted / advisory。
- `inspect_summary`: 给 SL-5/SL-7/SL-9 使用的摘要。

## 函数名或 prompt generator 名

- `run_sd4_design(...)`

## 最小示例

见 [`../fixtures/SD-4.json`](../fixtures/SD-4.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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

## PR-1A 工具入口与策略

```python
from method.stages.sd_tools import run_sd4_design, mark_warning_repair_attempt

design_feedback, meta = run_sd4_design(context, policy_profile="generated_candidate")
blocking_keys = [item.instance_key for item in design_feedback.blocking_items]
mark_warning_repair_attempt(context.warning_budget_state, blocking_keys)
```

PR-1A 实现的首批 `policy_profile`：

- `generated_candidate`：high-risk `W_*` 在预算内阻塞修复，advisory `W_*` 与 `I_*` 只入 trace。
- `signed_ref_model`：保持未知 warning 需分类的保守口径。
- `path_smoke` / `audit_only`：warning 不触发自动修复，只进入 advisory trace。

`suggested_fix_hints` 只作为 `FixPlan` 参考证据，不是必须执行的脚本。
