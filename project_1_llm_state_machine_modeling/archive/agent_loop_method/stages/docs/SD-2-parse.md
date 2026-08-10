# SD-2 ParseFeedback

## 目标

解析 current DSL，产出结构化 parse feedback。

## 输入

- `current_dsl`: 待解析 pyfcstm DSL。
- `dsl_hash`: DSL hash。

## 输出

- `parse_feedback`: line/col/expected/got/diagnostics。
- `prompt_ready_summary`: 面向修复 prompt 的错误摘要。

## 函数名或 prompt generator 名

- `run_sd2_parse(...)`

## 最小示例

见 [`../fixtures/SD-2.json`](../fixtures/SD-2.json)。该 fixture 必须包含 stage-specific `input` / `output` 字段，不能退化为通用 `summary` 占位。

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
from archive.agent_loop_method.stages.sd_tools import run_sd2_parse

feedback, meta = run_sd2_parse(current_dsl, context)
assert meta.stage_id == "SD-2"
```

`run_sd2_parse` 复用 `archive.agent_loop_method.feedback.parse.check_parse`，不调用 LLM、不读取 `.env`。
