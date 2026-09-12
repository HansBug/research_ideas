# SD-3 SemanticFeedback

## 目标

将 parse-ok DSL 构建为 pyfcstm model，并把 AST/model 放入 `StageContext` 供 SD-4/SD-6 复用。

## 输入

- `parse_ok_dsl`: parse 已通过 DSL。
- `dsl_hash`: DSL hash。

## 输出

- `semantic_feedback`: missing states/dangling transitions/type mismatches。
- `stage_context_update`: ast/model/model_summary。

## 函数名或 prompt generator 名

- `run_sd3_semantic(...)`

## 最小示例

见 [`../fixtures/SD-3.json`](../fixtures/SD-3.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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

## PR-1A 工具入口与 handoff

```python
from archive.agent_loop_method.schema import StageContext
from archive.agent_loop_method.stages.sd_tools import run_sd3_semantic

context = StageContext(nl=nl)
feedback, meta, build = run_sd3_semantic(parse_ok_dsl, context)
assert context.model is build.model
```

`run_sd3_semantic` 复用 `archive.agent_loop_method.feedback.semantic.check_semantic`，并通过 `archive.agent_loop_method.stages.sd_context.build_model_from_dsl()` 走 canonical parse/build path，把 AST/model 显式写入 `StageContext` 供 SD-4/SD-6 复用。
