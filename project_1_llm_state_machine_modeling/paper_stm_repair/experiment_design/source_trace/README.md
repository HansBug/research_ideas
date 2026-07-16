# source_trace/ — raw/source ↔ intermediate trace 合同入口

## 1. 一句话定位

本目录定义 paper1 的最小 **source trace** 合同：把 `PR-issue-ledger` 已确认的 source-level behavioral issue，从 raw/source `STM_0` 元素追踪到中间可执行语义表示中的元素，并记录该对应关系是否能支持后续 raw/source patch projection 与 closure / regression 审计。

```text
confirmed issue
  -> raw/source element refs
  -> source trace ledger
  -> intermediate semantic elements
  -> later repair/change ledger
  -> raw/source patch bundle / closure evidence
```

source trace 是证据链和归因边界，不是 paper1 的 headline contribution；paper1 的贡献仍是 feedback-driven LLM refinement loop 与 diagnostics / simulation / formal-verification feedback integration。

## 2. 为什么需要 source trace

#150 已经定义 source issue ledger v0，但只回答“哪些 issue 可以被确认并进入 repair”。后续 loop 还需要回答：

1. 这个 issue 指向 raw/source STM 里的哪个 state / transition / guard / effect / variable？
2. 转换为中间表示后，对应哪个 transition / guard / effect？
3. 如果中间表示被修复，这个变化能不能回投为 raw/source patch？
4. 如果 trace 是 ambiguous / untraceable / conversion artifact，是否必须禁止它进入 source-level closure 主结论？

没有 source trace，后续很容易把 conversion / normalization / lowering 造成的变化误算成 repair gain，破坏论文证据链。

## 3. 当前 v0 范围

| 对象 | v0 决策 | 说明 |
|---|---|---|
| 支持的 trace relation | `exact` / `normalized` / `split` / `ambiguous` / `untraceable` / `conversion_artifact` | 不支持 `merged` / `inferred`，避免真实样例前引入弱归因关系。 |
| 与 issue ledger 的链接 | trace ledger 通过 `required_for_issue_ids[]` 指向 #150 issue id，并用 `issue_binding_policy` 声明绑定范围 | 本 PR 不修改 #150 issue ledger schema；consumer 构造确定性 reverse index 并检查 actual issue status。 |
| closure claim gate | `attribution_boundary.closure_claim_allowed` | `ambiguous` / `untraceable` / `conversion_artifact` 必须为 false。 |
| partial projection | `projection_status=partially_projectable` | v0 默认只能支撑 partial localization，不单独支撑 full closed。 |
| fixtures | synthetic contract fixtures | 不是真实实验、不是真实 repair-loop 输出、不跑四个 selected examples。 |

## 4. 文件说明

| 文件 / 路径 | 职责 |
|---|---|
| [GUIDE.md](./GUIDE.md) | 后续 agent 维护 source trace 合同时的操作规范。 |
| [source_trace_contract.md](./source_trace_contract.md) | v0 字段、relation、projection、attribution boundary 与 cross-ledger gate 的主合同。 |
| [fixtures/README.md](./fixtures/README.md) | 六个 synthetic contract fixture 的人类可读说明入口。 |
| [../../pipeline/evaluation/schemas/source_trace.schema.json](../../pipeline/evaluation/schemas/source_trace.schema.json) | machine-readable JSON Schema。 |
| [../../pipeline/evaluation/fixtures/source_trace/](../../pipeline/evaluation/fixtures/source_trace/) | source trace JSON fixtures。 |
| [../../pipeline/evaluation/tests/test_source_trace_schema.py](../../pipeline/evaluation/tests/test_source_trace_schema.py) | schema / fixture / cross-ledger pytest gate。 |

## 5. 推荐阅读顺序

1. 先读本文件，理解 source trace 为什么存在。
2. 再读 [source_trace_contract.md](./source_trace_contract.md)，确认字段与 gate。
3. 再读 [fixtures/README.md](./fixtures/README.md) 与六个 fixture 子目录。
4. 最后读 machine schema / fixtures / tests：
   - [../../pipeline/evaluation/schemas/source_trace.schema.json](../../pipeline/evaluation/schemas/source_trace.schema.json)
   - [../../pipeline/evaluation/fixtures/source_trace/](../../pipeline/evaluation/fixtures/source_trace/)
   - [../../pipeline/evaluation/tests/test_source_trace_schema.py](../../pipeline/evaluation/tests/test_source_trace_schema.py)

## 6. 禁止误读

- 不把 source trace success 写成 method effectiveness。
- 不把 `source_trace.schema.json`、trace ledger 或 audit bookkeeping 写成 paper contribution。
- 不把 `normalized` 造成的语法变化写成 repair gain。
- 不把 `split` 的 partial localization 写成 full issue closure。
- 不把 `ambiguous` / `untraceable` / `conversion_artifact` 用作 source-level closure 主证据。
- 不用本目录替代 Discover/Repair/Confirm runtime、最终 source export、C closure audit 或 pilot 后 evaluation rubric；动态施工顺序见 [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100)。

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-17 00:32:36 | 删除旧 loop-io 动态路由，改为稳定阶段能力与 #100 动态施工入口。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 初始化 source trace 合同入口、v0 relation 口径和 machine schema / fixture / tests 指针。 |
