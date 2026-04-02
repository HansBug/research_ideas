# 基于接口自动机与 UML 构件模型的构件组装 / Assembly of Components Based on Interface Automata and UML Component Model

## 基本信息

- 标题：Assembly of Components Based on Interface Automata and UML Component Model
- 中文标题：基于接口自动机与 UML 构件模型的构件组装
- 作者：Samir Chouali, Sebti Mouelhi, Hassan Mountassir
- 发表：*4e Conf{\'e}rence francophone sur les Architectures Logicielles, CAL 2010, Pau, France, 9--11 mars 2010*, pp. 66-78, 2010
- DOI：原文未给出
- 链接：https://editions-rnti.fr/?inprocid=1000897
- 形式主义：`Improved Interface Automata + UML Architecture Graph`
- 主类：🔌
- 描述客体：🤝
- 所属领域：💻
- 论文角色：构件组装 / 接口兼容性验证
- 工具/实现获取方式：原文给出 `UML 2.0` 构件结构 + interface automata 的组合算法，但未提供公开分析器或代码仓库。
- 标准/格式获取方式：承载方式是 `UML` 构件图、graph representation 与 improved interface automata；原文未提供 `XMI` 或其他独立交换格式。

## 简报

这篇论文的价值，不在于再次复述 `Interface Automata` 的二元兼容性，而在于把它扩到“有层次的 UML 构件系统组装”上。标准 `Interface Automata` 更擅长验证两个接口之间的协议级兼容，但面对 composite component、subcomponent 连接和整套架构图时就不够了。本文用一个 `UML` 构件结构图提供架构上下文，再把每个 primitive component 的接口写成 automaton，并沿着图上的邻接关系逐步组装。

- 形式主义定位：面向组件组装与互操作验证的接口/组合模型，不是执行型状态机 DSL。
- 构造方式简述：先为 primitive component 写 `IA`，再把 `UML` 架构写成图 `G_M`，最后按邻接关系迭代做 improved product 与 compatibility 检查。
- 基础设施与场景简述：依托 `UML 2.0` 组件模型、illegal/bad states 分析和逐步组装算法，服务软件构件与嵌套组件架构的协议兼容验证。

```text
UML component architecture -> per-component interface automata -> graph-guided synchronized product -> illegal/bad-state pruning -> compatible composite interface
```

## 形式主义定义与核心对象

### 定义对象

论文处理的对象有两层：

1. 单个 primitive component 的接口行为，用 `Interface Automaton` 描述。
2. 整个 `UML` 构件系统的架构关系，用 graph representation 描述。
3. component 之间的邻接关系与 composite-subcomponent 层次关系。
4. 逐步组合得到的 composite interface automaton。

### 核心抽象

原文先复用了标准 interface automaton：

$$
A = \langle S_A, I_A, \Sigma_A^I, \Sigma_A^O, \Sigma_A^H, \delta_A \rangle
$$

上式中的符号逐项解释如下：

1. `S_A` 是状态集合。
2. `I_A` 是初始状态集合。
3. `\Sigma_A^I` 是输入动作集合。
4. `\Sigma_A^O` 是输出动作集合。
5. `\Sigma_A^H` 是内部动作集合。
6. `\delta_A` 是带动作标记的转移关系。

论文随后把 `UML` 架构显式写成图：

$$
G_M = \langle N_{G_M}, C^p_{G_M}, C^n_{G_M} \rangle
$$

上式中的符号逐项解释如下：

1. `N_{G_M}` 是节点集合，对应系统中的组件。
2. `C^p_{G_M}` 是 composite 与 subcomponent 的层次边。
3. `C^n_{G_M}` 是同一 composite 内部 subcomponent 之间的连接边。

为了让 automata 真正感知架构上下文，原文定义了 improved interface automaton：

$$
A = \langle S_A, I_A, \Sigma_A^I, \Sigma_A^O, \Sigma_A^H, \delta_A, U_A \rangle
$$

上式中的符号逐项解释如下：

1. 前六个分量与标准 `IA` 一致。
2. `U_A` 是与组件 `C_A` 相连的邻居组件集合，由 `UML` 架构图推导得到。

### 一个最小例子与通俗解释

最容易理解的场景是：某个 composite controller 下有两个 subcomponent，`SensorProxy` 和 `ActuatorProxy`。

1. `SensorProxy` 在某状态会发出共享输出动作 `dataReady!`。
2. `ActuatorProxy` 只有在某些状态才接受 `dataReady?`。
3. 若两者被 `UML` 连接图声明为相邻组件，则可以进行同步 product。
4. 如果 product 中出现 `(s_1, s_2)` 这样的组合状态，使得一侧输出共享动作而另一侧当前并不接受，该状态就是 illegal state。

通俗地说，标准 `IA` 像“检查两个接口能不能对话”，而本文的方法像“先看整套接线图，再按接线关系逐块装配，并在装配过程中随时检查谁在说对方没准备接的话”。

### 运行 / 接受 / 转移语义

原文复用了 interface automata 的 synchronized product。若 `A_1` 与 `A_2` 可组合，则其共享动作集是：

$$
\mathrm{Shared}(A_1, A_2) = (\Sigma_{A_1}^I \cap \Sigma_{A_2}^O) \cup (\Sigma_{A_2}^I \cap \Sigma_{A_1}^O)
$$

上式中的符号逐项解释如下：

1. 第一项表示 `A_2` 的输出被 `A_1` 当作输入接收。
2. 第二项表示 `A_1` 的输出被 `A_2` 当作输入接收。
3. 这两类共享动作在 product 中同步发生。

illegal state 的定义可压缩成：

$$
\mathrm{Illegal}(A_1, A_2) = \{(s_1, s_2) \mid \exists a \in \mathrm{Shared}(A_1, A_2),\ (a \in \Sigma_{A_1}^O(s_1) \land a \notin \Sigma_{A_2}^I(s_2)) \lor (a \in \Sigma_{A_2}^O(s_2) \land a \notin \Sigma_{A_1}^I(s_1))\}
$$

上式中的符号逐项解释如下：

1. `(s_1, s_2)` 是 product automaton 中的组合状态。
2. `\Sigma_{A_i}^O(s_i)` 表示在状态 `s_i` 可发出的共享输出。
3. `\Sigma_{A_i}^I(s_i)` 表示在状态 `s_i` 可接收的共享输入。
4. 若一侧发得出而另一侧此刻接不了，就形成 illegal state。

兼容组合后的接口可写成：

$$
A_1 \parallel A_2 = \langle \mathrm{Comp}(A_1, A_2), I_{A_1 \times A_2} \cap \mathrm{Comp}(A_1, A_2), \Sigma_{A_1 \times A_2}, \delta' \rangle
$$

上式中的符号逐项解释如下：

1. `\mathrm{Comp}(A_1, A_2)` 是环境可避免落入 illegal states 的兼容状态集合。
2. `I_{A_1 \times A_2}` 是 product automaton 的初始状态集合。
3. `\delta'` 是在兼容状态上保留下来的转移关系。

对于 improved product，邻接集合还要更新为：

$$
U_{A_1 \times A_2} = (U_{A_1} \cup U_{A_2}) \setminus \{C_{A_1}, C_{A_2}\}
$$

这表示：合成后的复合组件继承两侧的外部邻居，但不再把被合并的两个组件自己当作外邻居。

### 语义边界

这篇论文的边界很清楚：

1. 它仍是离散协议兼容模型，不引入时间、概率或连续动态。
2. `UML` 在这里只承担架构上下文角色，不提供新的执行语义。
3. 重点是 protocol-level interoperability，而不是数据语义、QoS 或代码生成。
4. 它改进的是“如何在整套架构上做组装与验证”，不是重写 `Interface Automata` 基础理论。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 标准接口自动机 | `$A = \langle S_A, I_A, \Sigma_A^I, \Sigma_A^O, \Sigma_A^H, \delta_A \rangle$` | 单个组件的接口协议骨架。 |
| 架构图 | `$G_M = \langle N_{G_M}, C^p_{G_M}, C^n_{G_M} \rangle$` | 显式表示 composite-subcomponent 和连接关系。 |
| 改进接口自动机 | `$A = \langle S_A, I_A, \Sigma_A^I, \Sigma_A^O, \Sigma_A^H, \delta_A, U_A \rangle$` | 把架构邻居集合并入 automaton。 |
| 共享动作 | `$\mathrm{Shared}(A_1, A_2)$` | 判断两接口能否同步。 |
| illegal states | `$\mathrm{Illegal}(A_1, A_2)$` | 输出动作无人接收时的冲突状态。 |
| 合成接口 | `$A_1 \parallel A_2$` | 通过剪掉 illegal/bad/unreachable states 得到兼容组合。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个接口都由显式状态和动作驱动。 |
| 事件 / 触发 | 强支持 | 输入、输出、内部动作是一等对象。 |
| 守卫 / 数据 | 弱支持 | 重点在协议动作，不在复杂数据守卫。 |
| 层次 | 部分支持 | 通过 `UML` composite/subcomponent 图处理层次结构。 |
| 并发 / 同步 | 强支持 | 共享输入/输出动作通过 synchronized product 同步。 |
| 时间约束 | 不支持 | 没有时钟或 deadline。 |
| 连续动态 / 随机性 | 不支持 | 纯离散接口交互。 |
| 可执行 / 可验证性 | 强验证 | 可计算 composability、illegal states、compatibility 与 composite interface。 |

### 形式化问题与性质

1. 论文的增量不是“又一个组件图”，而是把架构邻接信息压进接口组合过程。
2. 相比只做 pairwise composition，它更适合真实组件架构的渐进式组装。
3. compatibility 在这里是“存在帮助环境使非法状态可避开”，不是简单的动作名匹配。
4. 邻居集合 `U_A` 让 composite interface 的构造可沿架构图持续推进。

## 构造方式与承载格式

### 建模入口

建模入口遵循两条线并行：

1. 对每个 primitive component 建一个 interface automaton。
2. 对整个系统建一张 `UML 2.0` component architecture graph。
3. 由图提取每个组件的邻居集合 `U_A`。
4. 按图遍历顺序做 improved product 和 compatibility 检查。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `IA` 元组。
2. `UML` 架构图 `G_M`。
3. 邻居集合 `U_A`。
4. product / illegal / compatibility 计算过程。

### 交换与互操作

互操作重点不是 `UML` 文件交换，而是：

1. 在架构图层面确定哪些组件允许被尝试组装。
2. 在 automata 层面检查共享动作是否真的兼容。
3. 在 composite 层面递归构造系统级接口。

## 配套基础设施

- 建模/编辑工具：原文依赖 `UML 2.0` component model 作为架构入口，但未绑定具体建模器。
- 解析/交换/元模型支持：有 `UML` 图结构和 improved `IA` 元组，但未提供公开元模型或交换 schema。
- 仿真/执行支持：重点不在执行器，而在接口兼容分析。
- 验证/分析支持：composability 检查、illegal states、bad states、compatibility、composite interface 构造。
- 代码生成/转换支持：原文未提供。
- 标准化或社区生态：依托 `UML` 与 interface automata 研究生态，工程工具链需要自行补齐。

## 适用场景与需求前提

### 适用场景

适合组件化软件系统、嵌套组件架构、服务模块组装和协议兼容性分析，尤其适合“接口行为重要，且系统已有显式架构图”的场景。

### 需求前提

1. 组件接口可抽成有限动作和离散协议状态。
2. 系统架构能明确写成 composite/subcomponent + connector 图。
3. 关注点是组件组装正确性，而非数值计算或时间性能。
4. 环境行为可被保守地理解为“帮助避免 illegal states”的输入提供者。

### 不适用或高成本场景

如果系统核心困难在实时调度、复杂数据约束、概率失效或连续物理过程，这套 improved interface automata 就不够，需要转向 timed / hybrid / probabilistic 路线。

## 与相邻形式主义的关系

相对 [an-introduction-to-input-output-automata/desc.md](../an-introduction-to-input-output-automata/desc.md)，本文更强调非 input-enabled 的接口兼容和 illegal states；相对 [towards-formal-interfaces-for-web-services-with-transactions/desc.md](../towards-formal-interfaces-for-web-services-with-transactions/desc.md)，它不讨论事务与补偿，而更关心组件架构组装；相对 [specification-and-verification-of-context-dependent-services/desc.md](../specification-and-verification-of-context-dependent-services/desc.md)，它不建上下文契约，而是把 `UML` 架构信息并入接口组合。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，当需求最终要落到“多组件交互系统”时，仅生成局部状态机还不够，还要显式抽出组件连接关系和可组合性约束。

### 作为目标形式主义还是中间表示

对接口兼容分析任务，它可以直接作为目标形式主义；对一般控制系统，它更适合作为组件交互层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把“组件是谁、谁和谁相连”与“各自接口协议是什么”分层建模。
2. LLM 生成接口模型后，应追加一轮 illegal/bad-state 检查，而不是只看动作名是否匹配。
3. composite system 的模型最好沿架构图递归生成，而不是一次性扁平展开。

## 重要的相关工作

- [an-introduction-to-input-output-automata/desc.md](../an-introduction-to-input-output-automata/desc.md)：`I/O Automata` 的理论蓝本。
- [towards-formal-interfaces-for-web-services-with-transactions/desc.md](../towards-formal-interfaces-for-web-services-with-transactions/desc.md)：展示 interface 主干在 Web services 方向的事务扩展。
- [specification-and-verification-of-context-dependent-services/desc.md](../specification-and-verification-of-context-dependent-services/desc.md)：展示接口/契约模型如何接上下文与服务组合。

## 文献分类总结

- 这是一篇 `🔌` 类高价值应用条目，核心贡献是把 `Interface Automata` 从 pairwise compatibility 扩到带层次架构信息的组件组装。
- 其描述客体是组件接口与交互关系，因此记为 `🤝`；论文语境更偏组件软件工程与组装验证，因此记为 `💻`。
- 对 `project_1` 来说，它补的是“需求中出现多组件交互时，状态机之外还需要哪一层结构信息”的关键证据。
