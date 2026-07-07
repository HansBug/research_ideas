# task_boundary.md — source-level issue lifecycle 的方法范围

## 1. 任务定义

本文任务不是 `<NL, STM_0> -> better STM` 的偏好判断，而是：

```text
Input:  <NL, raw/source STM_0>
Output: <confirmed issue ledger, repair/change ledger, raw/source patch bundle or final raw/source STM_k, closure/regression ledger>
```

方法目标是在已有状态机制品中发现、确认、修复并闭合 source-level behavioral issues。

## 2. 输入

| 输入 | 说明 | 纪律 |
|---|---|---|
| `NL` | 控制系统自然语言需求或需求片段。 | 是 issue confirmation 的依据之一。 |
| raw/source `STM_0` | 原始或源层状态机制品，如 PlantUML-like / SysML-like / extracted STM artifact。 | 是最终评价和解释的落点。 |
| source provenance | 来源、hash、文件路径、转换记录等。 | 必须支持后续 trace 和 audit。 |
| intermediate representation | 从 raw/source 得到的可执行语义表示。 | 只作工具反馈介质，不作贡献归因。 |

## 3. 输出

| 输出 | 说明 | 不能做什么 |
|---|---|---|
| candidate issue ledger | 记录工具 / LLM /人工提示的可疑行为问题。 | 不能直接作为 confirmed issue 或 success。 |
| confirmed issue ledger | 记录经 `NL + raw/source element + behavior evidence` 确认的问题。 | 不能由 folded event / diagnostic alone 自动生成。 |
| repair/change ledger | 记录每个 `issue_id` 对应的修复计划、候选修改、失败或 unsupported 情形。 | 不能泛泛重写整个模型。 |
| raw/source patch bundle or final raw/source `STM_k` | 回到源层的补丁、diff、解释或完整候选模型。 | 无法投影的中间修改不能算 closure。 |
| closure/regression ledger | 记录 closed / partially closed / not closed / over-repaired / regression-introduced / unjudgeable。 | 不得静默删除未闭合或新引入的问题。 |

## 4. 方法内外边界

### 方法内

1. raw/source 资产读取与 source trace。
2. 中间可执行语义表示构造。
3. diagnostics / inspect / simulation / verification feedback 消费。
4. candidate issue discovery。
5. strict source-level confirmation。
6. issue-grounded repair。
7. raw/source patch/projection。
8. closure / regression audit。

### 方法外

1. 一轮式 `NL -> STM` 初始生成。
2. 完整 PlantUML / SysML round-trip converter。
3. 证明 `fcstm` 是更好建模语言。
4. timed / hybrid automata headline claim。
5. final evaluation rubric / baseline contract 的提前冻结。
6. constructed `STM_k` adjudication 作为方法效果。

## 5. 人类角色

| 阶段 | 人类角色 |
|---|---|
| 任务和范围设定 | 冻结 paper story、scope、claim boundary。 |
| reference issue / pilot 后 rubric | 可参与人工复核和 ambiguity 标注。 |
| 方法运行 | 不应在 run 中手工替换 `STM_0` 或私自修补输出。 |
| 失败处理 | 标注 unsupported / untraceable / unjudgeable，而不是隐性删除失败。 |

## 6. 失败状态

| 状态 | 含义 |
|---|---|
| `unsupported` | 当前中间表示或工具无法承载该源层行为。 |
| `untraceable` | 中间元素无法可靠映射回 raw/source 元素。 |
| `unconfirmed` | candidate issue 无法经 `NL + source + behavior evidence` 确认。 |
| `partial_repair` | 修改只解决 issue 的一部分。 |
| `not_closed` | 修复后原 issue 仍存在。 |
| `over_repaired` | 修复改变了超出 issue 所需的行为。 |
| `regression_introduced` | 引入新的 source-level behavioral issue。 |
| `unjudgeable` | 证据不足，不能可靠判定。 |

## 7. 不跑实验纪律

本文件只定义任务边界，不运行四例 / selected examples / repair-loop pilot，不产生 run record 或实验结果。
