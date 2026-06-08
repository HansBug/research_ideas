# SD-8 FixRequestBatch

## 目标

把 selected feedback 转成结构化 repair request。底层工具仍产出 legacy `FixPlan` / `RevisedFixPlan`，PR-E1 runtime 会提升为 `FixRequestBatch = list[FixRequest]`；inspect suggested_fix 仅作为参考，不允许无脑执行。

## 输入

- `selected_feedback`: parse/semantic/design/sim/model_review/rejection。
- `grounding_map`: preserve 与 target hints。
- `policy_profile`: 修复策略与 edit scope。

## 输出

- `fix_request_batch`: batch id、source stage、target、severity、problem summary、evidence、hard_block / waiver_allowed。
- `legacy_fix_plan`: 兼容字段，包含 target/severity/evidence/suggested_fix_hints/recommended_strategy/forbidden_edits。

## 函数名或 prompt generator 名

- `run_sd8_fix_plan(...)`

## 最小示例

见 [`../fixtures/SD-8.json`](../fixtures/SD-8.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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

## PR-1A 工具入口

```python
from method.stages.sd_tools import run_sd8_fix_plan

fix_plan, meta = run_sd8_fix_plan(
    selected_feedback,
    source="design",
    grounding_map=grounding_map,
    before_dsl=current_dsl,
)
```

当 `SL-10` 要求 rework 时，rework 指令必须写入 FixLog 并回到 `SL-9`，返工 request 不允许再次 reject；不再通过改写 `FixPlan.target=repair_review` 表达返工。
