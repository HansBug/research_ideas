# 用带抽象的正则推断生成无限状态通信协议模型 / Generating Models of Infinite-State Communication Protocols Using Regular Inference with Abstraction

## 基本信息

- 标题：Generating Models of Infinite-State Communication Protocols Using Regular Inference with Abstraction
- 中文标题：用带抽象的正则推断生成无限状态通信协议模型
- 作者：Fides Aarts，Bengt Jonsson，Johan Uijen
- 发表：*Testing Software and Systems (ICTSS 2010)*，LNCS 6435，pp. 188-204，2010
- DOI：`10.1007/978-3-642-16573-3_14`
- 链接：https://doi.org/10.1007/978-3-642-16573-3_14
- 形式主义：`communication-protocol state machines / regular inference with abstraction / LearnLib + ns-2`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：abstraction-guided protocol-model inference route for infinite/dataful alphabets
- 工具/实现获取方式：原文明确说明实现把 `LearnLib` 与 `ns-2` 协议模拟器连接起来，用主动学习接口反复发查询并生成协议组件模型；正文未给独立公开仓库。
- 标准/格式获取方式：输入承载是 concrete message alphabet 与外部提供的 abstraction predicates / mapper，输出是 abstract finite-state protocol model；它不是固定交换标准。

## 简报

这篇论文要解决的，不是如何再定义一种新的通信自动机，而是如何在黑盒设置下，从带数据参数的通信协议实现中主动学习出仍然可验证、可测试的抽象状态机。它把 regular inference 和 predicate abstraction 结合起来：学习器继续在有限抽象字母表上工作，但抽象函数要由协议知识外部提供，从而能覆盖消息编号、会话标识等会把 concrete alphabet 拉成无限大的字段。

- 形式主义定位：协议状态机学习方法，而不是新的状态机母型。
- 构造方式简述：concrete messages 先经 abstraction mapper 映成抽象字母，再用 `LearnLib` 做 regular inference，必要时通过 counterexample 回到具体消息层重设抽象。
- 基础设施与场景简述：依托 `LearnLib`、主动 `MQ/EQ` 风格查询、外部 abstraction knowledge 与 `ns-2`，服务 `SIP` 一类带参数协议组件的模型恢复。

```text
concrete protocol messages -> abstraction predicates / mapper -> abstract learning alphabet -> active inference -> abstract protocol FSM -> validation / testing model
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. concrete message alphabet 与外部协议实现。
2. abstraction predicates 与 concrete-to-abstract mapper。
3. 基于 regular inference 的 finite-state hypothesis。
4. counterexample-guided abstraction adjustment。
5. `LearnLib + ns-2` 的学习闭环。

### 核心抽象

原文的关键不在新自动机定义，而在“学习对象如何被抽象成有限字母表”。可保守整理为：

$$
\alpha : \Sigma_c \to \Sigma_a
$$

上式中的符号逐项解释如下：

1. `\Sigma_c` 是 concrete message alphabet，其中消息可能带参数、编号或标识符。
2. `\Sigma_a` 是有限的 abstract alphabet。
3. `\alpha` 把具体消息映成抽象动作标签。
4. 论文强调：这个抽象不是自动学出来的，而是由对协议数据语义的外部知识给定。

学习得到的抽象协议模型可保守写成一个有限状态机：

$$
A = (Q, q_0, \Sigma_a, \delta)
$$

上式中的符号逐项解释如下：

1. `Q` 是抽象状态集合。
2. `q_0` 是初始状态。
3. `\Sigma_a` 是抽象字母表。
4. `\delta : Q \times \Sigma_a \to Q` 是在抽象消息上的转移函数。
5. 论文的目标不是学习 concrete infinite-state machine，而是学习一个足够精确的抽象有限模型。

把主动学习闭环压成一条方法路线，可写成：

$$
\mathcal{L} = (\alpha, MQ, EQ, H, CE)
$$

上式中的符号逐项解释如下：

1. `\alpha` 是抽象函数。
2. `MQ` 是 membership-style queries。
3. `EQ` 是 equivalence-style testing / checking step。
4. `H` 是当前 hypothesis automaton。
5. `CE` 是反例；若反例无法在当前抽象下解释，就需要改进抽象或 mapper。

### 一个最小例子与通俗解释

论文的直觉例子是 `SIP` 这类带参数的通信协议组件：

1. concrete message 里会出现 call-id、tag、branch 等参数。
2. 如果把每个不同编号都当成不同字母，alphabet 会无限膨胀。
3. 论文做法是先把消息按“是否同一会话、是否同一对话上下文”之类谓词抽象成有限标签。
4. 学习器在这个有限抽象字母表上恢复状态机。

通俗地说，这像“先决定消息里的哪些数字真的影响控制流，再把剩下的号码细节擦掉”。这样学出来的不是原始实现的逐比特复制品，而是更适合验证和测试的协议控制骨架。

### 运行 / 接受 / 转移语义

论文的学习语义不是传统接受语言语义，而是“抽象查询在被学习组件上如何被解释”。一次抽象执行可保守写成：

$$
q_{i+1} = \delta(q_i, \alpha(m_i))
$$

上式中的符号逐项解释如下：

1. `m_i` 是第 `i` 个 concrete message。
2. `\alpha(m_i)` 是对应抽象消息。
3. `q_i`、`q_{i+1}` 是 hypothesis 中的抽象状态。
4. 这说明学习器只观察抽象后的控制效应，而不是 concrete 参数的全部取值。

如果一个 concrete counterexample 在当前抽象下无法被现有 hypothesis 解释，则需要满足：

$$
\exists w \in \Sigma_c^*:\ \alpha(w) \text{ 与实现行为不一致}
$$

其中：

1. `w` 是一段 concrete message trace。
2. `\alpha(w)` 是其抽象化后的 trace。
3. 失配说明当前抽象太粗，或 hypothesis 仍需继续学习。

### 语义边界

1. 这篇论文不是 `RALib` 那种通用 register-automata tool paper，而是更早的 abstraction-guided protocol learning 路线。
2. 抽象知识必须外部提供；如果对数据字段缺少领域理解，方法收益会明显下降。
3. 输出仍是抽象有限状态模型，不保证恢复原始 infinite-state 实现的全部细节。
4. 重点场景是通信协议组件，而非一般算术密集型软件。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| concrete-to-abstract 映射 | `$\alpha : \Sigma_c \to \Sigma_a$` | 把无限/巨大的具体字母表压到有限抽象字母表。 |
| hypothesis 自动机 | `$A = (Q, q_0, \Sigma_a, \delta)$` | 学习输出的是 abstract finite-state protocol model。 |
| 学习闭环 | `$\mathcal{L} = (\alpha, MQ, EQ, H, CE)$` | regular inference 与 abstraction refinement 的组合骨架。 |
| 抽象执行 | `$q_{i+1} = \delta(q_i, \alpha(m_i))$` | 模型只观察抽象消息上的控制效果。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 最终输出是有限抽象状态机。 |
| 事件 / 触发 | 很强 | 消息/交互动作是主驱动对象。 |
| 守卫 / 数据 | 中等支持 | 数据通过 abstraction predicates 进入，而不是原样保留。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 中等支持 | 主体是协议交互，而非显式并发语义。 |
| 时间约束 | 不支持 | 不讨论 timed behaviour。 |
| 连续动态 / 随机性 | 不支持 | 纯离散协议学习。 |
| 可执行 / 可验证性 | 很强 | 输出模型直接服务测试、验证和协议理解。 |

### 形式化问题与性质

1. 论文的核心是“怎样在 infinite/dataful alphabet 上继续使用 finite-state regular inference”。
2. 把 predicate abstraction 放到主动学习前端，是它区别于纯 `RA/EFSM` 学习论文的关键。
3. 这条路线更偏 protocol abstraction + model recovery，而不是一般 automata theory。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. concrete communication messages。
2. 外部给定的 abstraction predicates / mapper。
3. `LearnLib` 学习器。
4. `ns-2` 协议模拟器或等价被学习系统。

### 机器可处理承载方式

机器可处理承载方式包括：

1. abstract alphabet。
2. finite-state hypothesis automaton。
3. concrete counterexample traces。
4. mapper / abstraction knowledge。

### 交换与互操作

1. 互操作重点在 `LearnLib` 与 `ns-2` 的联接。
2. 输入输出不是中立标准，而是“concrete trace + abstraction + hypothesis”三层。
3. 学到的抽象状态机可继续回送到验证或测试工具链。

## 配套基础设施

- 建模/编辑工具：不主打图形前端，核心是 `LearnLib` 学习框架与外部协议模拟器。
- 解析/交换/元模型支持：abstraction mapper、abstract alphabet 与 counterexample traces 是关键承载。
- 仿真/执行支持：由 `ns-2` 或等价 concrete system 回答学习查询。
- 验证/分析支持：输出模型服务后续 model-based validation / testing。
- 代码生成/转换支持：重点不是部署代码生成，而是 concrete message 到 abstract model 的转换。
- 标准化或社区生态：与 `LearnLib` 主动学习生态直接相连，也是后续 `RA/EFSM` 数据化学习线的早期方法前身。

## 适用场景与需求前提

### 适用场景

适合带会话标识、消息参数和大字母表的通信协议或接口组件，尤其适合系统本身难以直接形式化，但可以通过 active query 与 trace 观测恢复控制模型的场景。

### 需求前提

1. 系统必须可被查询或模拟。
2. 需要有人提供合理的 abstraction knowledge，说明哪些字段真正影响控制流。
3. 目标更偏协议控制骨架恢复，而不是 bit-accurate 实现重建。

### 不适用或高成本场景

如果系统的数据语义依赖复杂算术、全局历史或隐式 side effect，而又无法给出稳定抽象，这条路线会很难收敛。

## 与相邻形式主义的关系

相对 [learning-extended-finite-state-machines/desc.md](../learning-extended-finite-state-machines/desc.md) 与 [active-learning-for-extended-finite-state-machines/desc.md](../active-learning-for-extended-finite-state-machines/desc.md)，本文更早地把“协议数据字段如何先抽象再学习”说清楚；相对 [demonstrating-learning-of-register-automata/desc.md](../demonstrating-learning-of-register-automata/desc.md)，它更偏 protocol abstraction，而不是通用 `RA` 学习工作流；相对 [grey-box-learning-of-register-automata/desc.md](../grey-box-learning-of-register-automata/desc.md)，它不要求灰盒信息，而是依赖外部 abstraction knowledge。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明面对“需求里包含大量编号、标识符、消息参数”的系统时，不一定非要直接生成 `RA/EFSM`，也可以先做 predicate-style abstraction。
2. 对 `project_1` 的需求到状态机建模而言，这条路能帮忙回答“哪些数据应保留进模型，哪些应先抽象掉”。
3. 若未来要做从系统交互日志反推出中间模型，这篇论文是很好的方法侧证。

### 作为目标形式主义还是中间表示

更像一种“学习得到抽象协议状态机”的方法路线，适合作为中间建模与验证入口，而不是最终规范交付格式。

### 对需求到模型生成的启发

1. 数据参数并不总该直接进入状态机字母表。
2. 先做抽象再学习，往往比直接在 concrete alphabet 上硬学更稳。
3. 需求文本若显式区分“控制字段”和“载荷字段”，就很适合套这条路线。

### 现实限制

这篇论文强依赖抽象知识的质量；如果抽象过粗，学到的模型可能失真，过细又会让学习成本重新爆炸。

## 重要的相关工作

1. [demonstrating-learning-of-register-automata/desc.md](../demonstrating-learning-of-register-automata/desc.md)：面向协议与接口的 `RA` 学习 workflow。
2. [learning-extended-finite-state-machines/desc.md](../learning-extended-finite-state-machines/desc.md)：更系统的 `RA/EFSM` learning 方法论文。
3. [grey-box-learning-of-register-automata/desc.md](../grey-box-learning-of-register-automata/desc.md)：把 `RALib` 学习线推进到灰盒约束观测。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
