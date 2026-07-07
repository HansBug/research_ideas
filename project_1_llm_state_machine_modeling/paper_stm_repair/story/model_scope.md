# model_scope.md — paper1 模型范围与行为表达边界

## 1. 研究对象

本文研究对象是 existing raw/source state-machine artifacts，而不是某个特定 DSL 本身。`fcstm` / `pyfcstm` 只是在当前实现中承载中间可执行语义表示的工具介质。

## 2. Headline 范围

| 范围 | 当前角色 | 说明 |
|---|---|---|
| discrete FSM | headline | 状态、事件、迁移是基础对象。 |
| hierarchical state machine | headline | 允许 composite / nested state，但必须可 trace。 |
| discrete UML/SysML-like statechart subset | headline | 作为 source artifact 形态进入；不声称覆盖 arbitrary UML/SysML。 |
| EFSM-lite cues | careful / annotated | 变量、guard-like condition、action/effect 可作为 issue evidence，但需严格 source-level confirmation。 |
| timer-like textual cue | caveat | 可作为 annotation 或 risk，不进入 timed automata headline。 |
| timed / hybrid automata | out-of-scope headline | 当前 paper1 不主打 timed/hybrid 语义完整验证。 |

## 3. 可处理的行为表达

| 表达 | 可进入 issue lifecycle 的条件 |
|---|---|
| state / initial / final | raw/source 可定位，且与 NL 或行为路径有关。 |
| transition | source element 可追踪，且有事件 / guard / action / target 语义影响。 |
| event | 作为触发条件或外部输入；若 folded 了 guard/action，需要进一步确认是否为 issue。 |
| guard-like condition | 需要与 NL、变量、路径或 source 语义对齐；不能因名字像 condition 就自动确认。 |
| variable / data condition | 可作为 EFSM-lite evidence；需记录当前工具支持边界。 |
| action / effect | 可作为行为结果或 side effect evidence；文本 action 需标注不确定性。 |
| hierarchy | 可作为 scope / containment / transition semantics evidence；需 source trace。 |
| annotation / comment | 只能辅助确认，不单独成为 confirmed issue。 |

## 4. confirmed issue 的最低要求

一个 confirmed source-level behavioral issue 至少需要：

1. 对应 raw/source element 或明确缺失的 source-level behavior；
2. 与 `NL` 或 raw/source 内部行为一致性之间的冲突、遗漏或不可闭合证据；
3. 可审计的 evidence bundle，例如 diagnostics、simulation/probe、verification/check hint、trace、人工裁决说明；
4. 明确说明它不是单纯 expression debt、conversion artifact 或中间表示 artifact。

## 5. 与历史 Better STM 框架的关系

Better STM 主框架已经 superseded。旧框架中的 no-regression、attribution boundary、anti-gaming 等纪律若后续有价值，必须从 archive / asset map 中显式迁移到 issue lifecycle 语境，不能自动保留为 active evaluation framework。

## 6. 禁止外推

- 不外推到 arbitrary UML / SysML 全语义。
- 不外推到 timed automata / hybrid automata。
- 不把 `fcstm` 支持的语法范围等同于 paper1 的研究对象范围。
- 不把 model runnable 等同于 model behavior correct。
- 不把 scenario / property pass 等同于 issue closure，除非 source-level issue 与 evidence 链完整。
