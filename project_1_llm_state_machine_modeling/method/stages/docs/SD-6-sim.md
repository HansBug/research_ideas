# SD-6 SimFeedback

## 目标

冻结 `SD-6` 的 PR-0 最小 stage contract，供后续 PR-1A/PR-1B 向后兼容扩展。

## 输入

- `stage_id`: `SD-6`
- `stage_kind`: `deterministic`
- `input`: 最小 JSON fixture 中的 `input` 对象。

## 输出

- `output`: 最小 JSON fixture 中的 `output` 对象。
- `meta`: `StageResultMeta`，enabled stage 缺失输出不得静默视为 ok。

## 函数名或 prompt generator 名

PR-0 仅冻结名称槽位；具体实现由 PR-1A / PR-1B 向后兼容补齐。

## 最小示例

见 [`../fixtures/SD-6.json`](../fixtures/SD-6.json)。

## 依赖关系

由 `method.stages.ids.ALL_STAGE_SPECS` 统一登记，禁止在 PR-1A/PR-1B 重新定义 stage id。

## 失败语义

- `skipped` 必须给出 `skipped_reason`。
- `error` 必须给出 `stage_error` 或 `output_validation_error`。
- `advisory` 不阻塞，但必须进入 trace / run record。

## 常见失败模式

- enabled stage 未产出 `StageResultMeta`。
- output schema 与 fixture 不兼容。
- prompt-ready summary 字段缺失。
