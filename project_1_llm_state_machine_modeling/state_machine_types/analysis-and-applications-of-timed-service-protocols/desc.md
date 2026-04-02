# 定时服务协议的分析与应用 / Analysis and Applications of Timed Service Protocols

## 基本信息

- 标题：Analysis and Applications of Timed Service Protocols
- 中文标题：定时服务协议的分析与应用
- 作者：Julien Ponge，Boualem Benatallah，Fabio Casati，Farouk Toumani
- 发表：*ACM Transactions on Software Engineering and Methodology*，19(4):1-38，2010
- DOI：`10.1145/1734229.1734230`
- 链接：https://doi.org/10.1145/1734229.1734230
- 形式主义：`Timed Service Protocols / Protocol Timed Automata (PTA)`
- 主类：🔌
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：定时服务协议建模与兼容/可替换性分析 / 服务协议到 `PTA` 的语义保持映射
- 工具/实现获取方式：原文说明相关分析能力被实现到 `ServiceMosaic` 原型中，并支持从 `BPEL` 过程抽取 timed protocol；原文未提供独立公开仓库。
- 标准/格式获取方式：承载方式包括 timed business protocol tuple、`BPEL` 流程、`WSDL` 接口、`PTA` 与 timed automata 运算；原文未给统一交换标准。

## 简报

这篇论文处理的是“服务能不能交互”这个老问题在真实 Web service 场景里的时间化版本。作者不是只看消息名是否能对上，而是把登录超时、报价失效、告警定时器、会话 deadline 这类业务时序约束直接纳入协议模型，形成 timed service protocol，再把它语义保持地映射成一类带 `ε` 迁移和 reset 的 `Protocol Timed Automata`，最后在这个层面做兼容、替换、差集和交集分析。

- 形式主义定位：这是接口/组合/契约主干上的应用型条目，核心价值是把服务协议的“消息极性 + 定时约束 + 兼容/替换分析”连成完整链路。
- 构造方式简述：先用 timed business protocol 描述状态、消息、时钟变量和 `C-Invoke / M-Invoke` 约束，再构造 timed traces / conversations / interaction traces，最后映射到 `PTA` 并做算子运算。
- 基础设施与场景简述：依托 `BPEL`、`WSDL`、timed automata 理论和 `ServiceMosaic` 原型，服务于 Web service 绑定、运行时替换、协议适配器分析和 BPEL 伙伴服务选择。

```text
service interaction requirements + deadlines -> timed service protocol -> PTA / timed-automata operators -> compatibility / replaceability analysis -> service binding or adaptation
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 以状态机方式描述服务会话的 timed business protocol。
2. 作为显式时间约束的 `C-Invoke` 与 `M-Invoke`。
3. 记录每条迁移最近一次触发时刻的时钟变量集合 `X`。
4. 执行层的 timed trace、timed conversation 与 timed interaction trace。
5. 面向算子运算的 `PTA`，以及兼容/替换分析中的交集、差集、投影等协议算子。

### 核心抽象

论文给出的 timed business protocol 定义是：

$$
P = (S, s_0, F, M, X, C, R)
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集合，描述服务在会话中的阶段。
2. `s_0 \in S` 是初始状态。
3. `F \subseteq S` 是终止状态集合。
4. `M = M_e \cup \{\epsilon\}` 是消息集合，除普通消息外还允许空消息 `\epsilon`。
5. `X` 是按 transition 标识符建立的时钟变量集合，记录各迁移最近一次触发时间。
6. `C` 是定义在 `X` 上的时间约束集合。
7. `R \subseteq S^2 \times M \times C` 是迁移集合，元素 `(s, s', m, c)` 表示带消息 `m` 和约束 `c` 的协议迁移。

论文还把两类时间约束分开建模。`C-Invoke` 用于普通消息迁移，`M-Invoke` 用于隐式超时迁移：

$$
\mathrm{C\text{-}Invoke}(c), \quad c ::= x \ \mathrm{op}\ k \mid x - x' \ \mathrm{op}\ k \mid c \land c \mid c \lor c
$$

$$
\mathrm{M\text{-}Invoke}(c), \quad c ::= (x = k) \land c' \mid c \land c \mid c \lor c
$$

上式中的符号逐项解释如下：

1. `x, x' \in X` 是时钟变量。
2. `k \in \mathbb{Q} \cup \{\bot\}` 是常数，`\bot` 表示“从未触发过”。
3. `\mathrm{op} \in \{=,\neq,<,>,\le,\ge\}` 是比较关系。
4. `C-Invoke` 用来约束显式消息在什么时间窗口内可发送。
5. `M-Invoke` 用来表达超时类隐式跳转，典型地对应 deadline 到点后的状态转移。

协议执行语义通过变量赋值函数给出。对执行

$$
\sigma = s_0 \cdot (m_0,t_0) \cdot s_1 \cdots s_{n-1} \cdot (m_{n-1}, t_{n-1}) \cdot s_n
$$

论文定义时钟 `T_i` 在时刻 `t_j` 的赋值为：

$$
V_{t_j}(T_i)=
\begin{cases}
V_{t_{j-1}}(T_i) + (t_j - t_{j-1}) & \text{若对应迁移未在该步触发} \\
0 & \text{若对应迁移在该步被触发}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `V_{t_j}(T_i)` 是时刻 `t_j` 对时钟变量 `T_i` 的赋值。
2. 若当前步没有触发与 `T_i` 对应的迁移，则该时钟继续累加流逝时间。
3. 若该迁移当前被触发，则 `T_i` 被复位为 `0`。
4. 这样协议就能表达“某动作距离上次发生已经过去多久”。

协议算子层面，交集与差集直接建立在 conversation 集合上：

$$
\mathrm{Tr}(P) = \mathrm{Tr}(P_1) \cap \mathrm{Tr}(P_2)
$$

$$
\mathrm{Tr}(P) = \mathrm{Tr}(P_1) \setminus \mathrm{Tr}(P_2)
$$

上式中的符号逐项解释如下：

1. `\mathrm{Tr}(P)` 表示协议 `P` 允许的 timed conversations 集合。
2. 第一式对应协议交集，表示两协议都允许的会话。
3. 第二式对应协议差集，表示 `P_1` 允许而 `P_2` 不允许的会话。
4. 这些算子是兼容性与可替换性分析的基础。

### 一个最小例子与通俗解释

论文最直观的例子是在线融资服务：

1. 服务最初在 `Start` 状态，请求方先发 `login(+)` 才能进入 `Logged`。
2. 随后可以发送 `preApproval(+)`，服务再返回 `approved(-)` 等消息。
3. 某些状态带有超时语义，例如信用批准在一段时间后若未继续处理，会自动走到 `CreditExpired`。
4. 这种“显式消息 + 隐式超时”的组合，就是 `C-Invoke` 与 `M-Invoke` 同时生效的效果。

通俗地说，这个模型像“给普通服务协议图每条边都挂上计时器和超时器”。普通接口状态机只会问“下一条消息能不能发”，而 timed service protocol 还会问“必须多久内发、拖到什么时候就失效、两个协议是不是在时间上也匹配”。

### 运行 / 接受 / 转移语义

论文把一个正确执行定义为满足以下条件的有限序列：

$$
\sigma = s_0 \cdot (m_0,t_0) \cdot s_1 \cdots s_{n-1} \cdot (m_{n-1}, t_{n-1}) \cdot s_n
$$

其中要求：

$$
t_0 \le t_1 \le \cdots \le t_n,\quad s_n \in F,\quad V_{j-1} \models c_{j-1}
$$

上式中的符号逐项解释如下：

1. 时间戳必须单调不减。
2. 最终状态 `s_n` 必须属于终止状态集合 `F`。
3. 每一步迁移都必须满足其绑定的时间约束 `c_{j-1}`。
4. 这一定义保证了协议既是可达的，也是时间上合法的。

论文还定义了 timed interaction trace。若两个协议 `P` 与 `P'` 的观测会话在消息极性上互为反转，则去掉极性后得到的无极性 trace 就是它们的可交互证据。也就是说，兼容分析不是只看字面消息名，而是要看双方在同一时间轴上的输入/输出极性是否能对齐。

### 语义边界

这篇论文的边界主要在于：

1. 它关注的是服务交互协议与时间约束，不处理复杂数据变换和内部算法。
2. 时间语义是“相对某次迁移触发后的约束”，更接近交互 deadline，而不是连续物理动力学。
3. 协议要求是确定性的，作者对同一状态下同消息多守卫重叠做了约束。
4. 它很适合 Web services / BPEL 场景，但不直接覆盖高维控制回路。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed protocol 定义 | `$P = (S, s_0, F, M, X, C, R)$` | 用状态、消息、时钟和约束定义定时服务协议。 |
| 时间约束语法 | `$\mathrm{C\text{-}Invoke}(c),\ \mathrm{M\text{-}Invoke}(c)$` | 区分显式消息约束与隐式超时约束。 |
| 时钟更新 | `$V_{t_j}(T_i)$` 的累加 / 复位规则 | 记录每条迁移距上次触发已过去的时间。 |
| 正确执行 | `$t_0 \le \cdots \le t_n,\ s_n \in F,\ V_{j-1} \models c_{j-1}$` | 给出 timed conversation 的合法性标准。 |
| 协议交集 | `$\mathrm{Tr}(P) = \mathrm{Tr}(P_1) \cap \mathrm{Tr}(P_2)$` | 识别双方共同支持的 timed conversations。 |
| 协议差集 | `$\mathrm{Tr}(P) = \mathrm{Tr}(P_1) \setminus \mathrm{Tr}(P_2)$` | 找出兼容缺口与替换缺口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 状态表示会话阶段，终止状态决定 conversation 是否接受。 |
| 事件 / 触发 | 强支持 | 消息发送/接收与 `\epsilon` 超时迁移都是一等事件。 |
| 守卫 / 数据 | 部分支持 | 支持时钟守卫与消息极性，不强调复杂业务数据。 |
| 层次 | 不支持 | 主体是平铺协议状态机，而非层次状态机。 |
| 并发 / 同步 | 部分支持 | 通过 interaction trace 和协议算子做交互分析，但不是显式并发控制网。 |
| 时间约束 | 强支持 | `C-Invoke`、`M-Invoke`、时钟赋值和 `PTA` 映射是核心。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散时序服务交互。 |
| 可执行 / 可验证性 | 强验证 | 可落到 `PTA`/timed automata 运算，并支撑兼容与替换分析。 |

### 形式化问题与性质

1. 作者证明了 timed protocol 可通过语义保持映射落到 `PTA`，从而把交集、补集、差集等运算转成可判定问题。
2. `PTA` 允许带 clock reset 的 `\epsilon` 迁移，这使它比普通无声迁移 timed automata 更贴近协议超时语义。
3. 兼容与可替换性不再只是“有没有共同 trace”，而是“共同 trace 是否在时间上也成立”。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先明确服务的消息集合和输入/输出极性。
2. 把会话阶段写成状态，把消息交互写成迁移。
3. 对显式消息加 `C-Invoke` 约束，对隐式超时加 `M-Invoke` 约束。
4. 生成 timed traces / conversations / interaction traces。
5. 再映射到 `PTA`，以便做协议算子运算和自动分析。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. timed business protocol tuple。
2. `BPEL` 过程与其抽取出的多方 protocol。
3. `PTA` / timed automata 结构。
4. 兼容、差集、投影等算子运算结果。

### 交换与互操作

互操作重点在：

1. `WSDL/BPEL` 中的消息交互如何抽到 protocol。
2. protocol 如何映射到 `PTA` 并保持会话语义。
3. 差集结果如何反向解释为“不兼容 conversation”。

## 配套基础设施

- 建模/编辑工具：原文围绕 `ServiceMosaic` 原型组织协议分析和生命周期管理。
- 解析/交换/元模型支持：支持从 `BPEL` 抽取 timed protocol，但未定义统一元模型标准。
- 仿真/执行支持：主体不强调执行引擎，而强调分析链路。
- 验证/分析支持：支持 compatibility、replaceability、intersection、difference、projection 等协议分析。
- 代码生成/转换支持：支持从 `BPEL` 过程抽取 timed protocols，并映射为 `PTA`。
- 标准化或社区生态：依托 `BPEL`、`WSDL` 和 timed automata 理论生态。

## 适用场景与需求前提

### 适用场景

适合需要做服务绑定、伙伴替换、协议适配或超时交互审计的 Web service / service-oriented composition 场景。

### 需求前提

1. 交互必须能抽成显式消息和有限状态阶段。
2. 时间需求主要表现为 deadline、超时、相对触发时间窗口。
3. 关注点在协议可对接性，而不是内部功能正确性。
4. 若要接 `BPEL`，流程结构必须可稳定抽取成消息 choreography。

### 不适用或高成本场景

如果系统主要依赖高维数据转换、连续控制律或概率性能指标，仅靠 timed protocol + `PTA` 抽象会明显过粗。

## 与相邻形式主义的关系

相对 [Towards Formal Interfaces for Web Services with Transactions](../towards-formal-interfaces-for-web-services-with-transactions/desc.md)，本文更强调时间约束和可替换性算子，而不是事务语义；相对 [Specification and Verification of Context-dependent Services](../specification-and-verification-of-context-dependent-services/desc.md)，这里的重点是 timed protocol 分析与 `PTA` 映射，而不是上下文服务组合；相对 [Towards Verifying Contract Regulated Service Composition](../towards-verifying-contract-regulated-service-composition/desc.md)，本文更靠近“服务接口协议 + 时间 + 算子分析”的底座，而不是把契约义务编译到 `ISPL`。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求中出现“某消息必须在多久内发送、超过多久就作废、某流程换服务时是否仍兼容”这类约束时，目标模型就不应只保留接口顺序，还要显式保留时间窗口和极性。

### 作为目标形式主义还是中间表示

对服务交互需求，它可以直接作为目标形式主义；对更广义控制系统需求，它更像交互协议子系统的中间表示。

### 对需求到模型生成的启发

1. 时间相关需求可以自然落成 `C-Invoke / M-Invoke` 两类约束。
2. 兼容性与可替换性最好在建模阶段就生成对应算子，而不是事后人工推断。
3. 若原始系统只有 `BPEL` 之类流程表示，也可以先抽取 protocol 再进入形式分析。

## 重要的相关工作

- [Specification and Verification of Context-dependent Services](../specification-and-verification-of-context-dependent-services/desc.md)：同样面向服务组合，但更偏上下文与配置约束。
- [Towards Formal Interfaces for Web Services with Transactions](../towards-formal-interfaces-for-web-services-with-transactions/desc.md)：强调事务语义接口，而不是 timed protocol 算子。
- [Towards Verifying Contract Regulated Service Composition](../towards-verifying-contract-regulated-service-composition/desc.md)：强调 contract-regulated composition 的设计时验证。
- [Contract Automata](../contract-automata/desc.md)：后续更系统地把 request/offer agreement 抽成独立 automata 家族。

## 文献分类总结

- 这是一篇 `🔌` 类应用型条目，核心价值是把服务协议的时间语义、兼容性和可替换性分析连成可操作的 formal chain。
- 它描述的是服务接口与交互 conversation，因此记为 `🤝`；论文语境属于服务组合和协议互操作，因此记为 `🌐`。
- 对 `project_1` 来说，它特别重要的启发是：需求里的 deadline、超时和接口可替换性，可以直接转成状态机约束与算子，而不是只能留在自然语言层。
