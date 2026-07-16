# Source-level issue definition v0

## 1. 定义目标

本文件只定义 paper1 当前 source-level issue lifecycle 的 v0 合同。它的作用是给 Discover root assessment、Repair eligibility、Confirm issue-chain 处置和 C closure audit 提供共同迁移对象，而不是定义最终实验指标或 baseline；动态 subPR 路线以 [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100) 为准。

## 2. 核心术语

| 术语 | v0 定义 | repair eligibility |
|---|---|---|
| `candidate_only` | 有可疑信号，但尚不能确认是 raw/source 层行为问题。 | false |
| `confirmed` | 已确认是 source-level behavioral issue，且可作为 repair target。 | true |
| `rejected_conversion_artifact` | 问题来自 conversion / lowering / normalization，而非 raw/source STM。 | false |
| `rejected_other` | 已知不是本方法应修复的 source-level issue，但不属于 conversion artifact。 | false |
| `out_of_scope` | 问题可能重要，但超出当前 paper1 headline scope。 | false |
| `insufficient_evidence` | NL、source 或 behavior evidence 不足，不能确认。 | false |

## 3. 两条 confirmed path

### 3.1 `nl_grounded_behavioral_issue`

这是默认 confirmed path。必须同时具备：

1. `NL evidence`：需求文本中能支撑该行为约束的片段或引用；v0 schema 要求至少一条 `nl_requirement` evidence。
2. `raw/source STM evidence`：源状态机中的状态、迁移、事件、guard、action/effect 或层次结构证据；v0 schema 要求至少一条 `source_stm_fragment` evidence。
3. `typed behavior evidence`：probe、simulation trace、verification counterexample、inspect diagnostic 或等价可引用证据，说明该问题具有行为后果；v0 schema 要求至少一条 `inspect_diagnostic` / `simulation_trace` / `probe_result` / `verification_counterexample`，`human_annotation`、`other_reference` 或 `conversion_report` 只能作为补充，不能单独支撑该 path。

### 3.2 `raw_internal_inconsistency`

这是用户在 `PR-issue-ledger` 计划阶段确认允许的第二条 confirmed path。它覆盖 raw/source STM 自身内部已经矛盾、但未必能直接绑定明确 NL 句子的情况。

最低要求：

1. `source STM evidence`：指出 raw/source artifact 中互相冲突的元素；v0 schema 要求 `source_element_refs` 与 `source_stm_evidence` 至少各有两个条目，用来表达冲突双方。
2. `source_internal_consistency_check` 或等价 typed behavior evidence：说明冲突如何成立；v0 schema 要求 `behavior_evidence` 中至少包含一个 `source_internal_consistency_check`。
3. `confirmation_rationale`：解释为什么此处不需要明确 NL evidence；当前 schema 要求 `nl_evidence` 为空，且 rationale 明确包含 `NL evidence is not required` 语义。
4. `attribution_boundary`：明确排除 conversion / lowering / normalization artifact。

限制：

- 该路径是 v0 合同，不是 final issue taxonomy。
- 后续必须结合真实 raw NL 例子、真实 discovery 能力和 pilot 输出复核。
- 不允许用该路径把 folded event / ugly expression 自动 confirmed。

## 4. folded event / expression debt

类似下面的 raw/source 表达：

```text
Idle --> Alarm : Event("temperature > 80")
```

默认只能作为 `candidate_only`。只有在后续证据证明 raw/source 层行为语义确实错，而不是表达介质受限或命名丑，才允许升级为 confirmed。

## 5. conversion artifact

如果问题来自：

- raw/source 到 canonical JSON 的 conversion；
- canonical 到 `.fcstm` 的 lowering；
- normalization / recovery / parser workaround；

则必须标为 `rejected_conversion_artifact` 或在 attribution boundary 中排除，不得作为 method discovered source-level issue。

## 6. timed / hybrid scope

当前 paper1 headline 不覆盖 timed / hybrid automata 主张。timed-like requirement 可以记录为 `out_of_scope` fixture 或风险，但不得进入主 repair/evaluation 分母，除非后续 protocol 明确扩展 scope。

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 09:52:31 | 初始化 candidate / confirmed / rejected / out-of-scope / insufficient evidence 定义，并加入 `raw_internal_inconsistency` 第二确认路径。 |
