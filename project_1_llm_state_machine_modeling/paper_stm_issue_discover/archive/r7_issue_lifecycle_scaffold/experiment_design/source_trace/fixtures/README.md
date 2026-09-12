# source_trace fixtures 说明

本目录是 source trace synthetic contract fixtures 的人类可读说明入口。机器 JSON 位于 [../../../pipeline/evaluation/fixtures/source_trace/](../../../../../pipeline/evaluation/fixtures/source_trace/)。

## fixture 列表

| fixture | JSON | 说明 |
|---|---|---|
| [exact_transition_trace/README.md](./exact_transition_trace/README.md) | [exact_transition_trace.json](../../../../../pipeline/evaluation/fixtures/source_trace/exact_transition_trace.json) | 一一对应 trace。 |
| [normalized_guard_trace/README.md](./normalized_guard_trace/README.md) | [normalized_guard_trace.json](../../../../../pipeline/evaluation/fixtures/source_trace/normalized_guard_trace.json) | 语义保持 guard normalization。 |
| [split_transition_trace/README.md](./split_transition_trace/README.md) | [split_transition_trace.json](../../../../../pipeline/evaluation/fixtures/source_trace/split_transition_trace.json) | transition 拆分与 partial projection。 |
| [ambiguous_trace/README.md](./ambiguous_trace/README.md) | [ambiguous_trace.json](../../../../../pipeline/evaluation/fixtures/source_trace/ambiguous_trace.json) | 多个 source origin，不能 closure claim。 |
| [untraceable_element/README.md](./untraceable_element/README.md) | [untraceable_element.json](../../../../../pipeline/evaluation/fixtures/source_trace/untraceable_element.json) | 中间元素无 source origin。 |
| [conversion_artifact_trace/README.md](./conversion_artifact_trace/README.md) | [conversion_artifact_trace.json](../../../../../pipeline/evaluation/fixtures/source_trace/conversion_artifact_trace.json) | conversion artifact trace，不是 source-level repair gain。 |

这些 fixture 均为 synthetic contract fixture，不对应真实实验样例，不运行 LLM，不生成真实 `STM_final`。

## 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 14:03:59 | 初始化六类 source trace fixture 说明入口。 |
