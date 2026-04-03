# 动态 Web 服务组合监控的灵活架构 / A Flexible Architecture to Monitor Dynamic Web Services Composition

## 基本信息

- 标题：A Flexible Architecture to Monitor Dynamic Web Services Composition
- 中文标题：动态 Web 服务组合监控的灵活架构
- 作者：Flavio Corradini, Francesco De Angelis, Daniele Fani', Andrea Polini
- 发表：*Proceedings of the 11th International Conference on Web Information Systems and Technologies (WEBIST 2015)*, pp. 64-72, 2015
- DOI：`10.5220/0005444800640072`
- 链接：https://doi.org/10.5220/0005444800640072
- 形式主义：`Interface Automata (IA) + Cassandra choreography failure prediction architecture`
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：动态 Web 服务组合监控架构 / `IA` 驱动的 choreography 运行时预测验证
- 工具/实现获取方式：原文给出基于 `Apache ServiceMix`、`Apache Camel`、`Cassandra` verification service 与 `SCXML` 行为规约的实现思路，但未提供独立公开仓库。
- 标准/格式获取方式：承载方式是 `Interface Automata`、`SCXML` 行为模型、ESB 路由配置与 choreography role-bundle；原文未给统一交换标准。

## 简报

这篇论文的重点不是重新定义一类新的接口自动机，而是回答一个更工程化的问题：当 Web 服务组合是动态 choreography、参与者可能在运行时加入、退出或替换时，怎样把 `Interface Automata` 的兼容性分析真正接到可运行的中间件架构上。作者给出的答案是把服务真实流量经由 ESB 外挂出来，再把每个服务的公开行为模型交给 `Cassandra` 做近未来失败预测。

- 形式主义定位：这是 `Interface Automata` 在动态服务组合与 choreography 运行时验证场景中的应用型条目，主体仍然围绕接口行为兼容与 illegal-state 预测展开。
- 构造方式简述：先为参与服务准备 `IA/SCXML` 行为模型，再通过 `Apache ServiceMix + Camel` 承接消息路由，最后让 `Cassandra` 基于当前执行状态向前展开 `k` 步预测。
- 基础设施与场景简述：依托 `ESB`、role-bundle、observer、`Cassandra`、`SCXML` 和 file-sharing choreography 示例，服务动态 Web service composition 与运行时失效预警。

```text
服务角色 + IA/SCXML 行为模型 -> ESB role-bundle 路由 -> observer 提交运行时状态 -> Cassandra 向前预测 -> illegal states / failure warning
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 每个服务公开的接口行为 `IA`。
2. choreography 中的角色与 role-bundle。
3. 共享动作同步下的 `IA` product。
4. product 上的 illegal states。
5. `Cassandra` 的当前状态识别与 `k` 步前瞻预测。
6. `ESB` 上承接真实消息流与监控流的 observer 机制。

### 核心抽象

论文沿用标准 `Interface Automata` 作为行为骨架：

$$
P = \langle V_P, V_P^{init}, A_P^I, A_P^O, A_P^H, T_P \rangle
$$

上式中的符号逐项解释如下：

1. `V_P` 是接口自动机状态集合。
2. `V_P^{init}` 是初始状态集合，原文要求至多一个初始状态。
3. `A_P^I`、`A_P^O`、`A_P^H` 分别是输入、输出和内部动作集合。
4. `T_P \subseteq V_P \times A_P \times V_P` 是带动作标记的迁移集合。
5. `A_P = A_P^I \cup A_P^O \cup A_P^H` 是全部动作集合。

两个 `IA` 的可组合条件是：

$$
\mathrm{shared}(P,Q) = A_P \cap A_Q = (A_P^I \cap A_Q^O) \cup (A_Q^I \cap A_P^O)
$$

上式中的符号逐项解释如下：

1. `\mathrm{shared}(P,Q)` 是两边真正需要同步的共享动作集合。
2. 原文要求两个自动机只共享 input/output 动作，不共享 internal 动作。
3. 因而共享集合只由一边输入、另一边输出的动作组成。

组合后的 illegal states 定义为：

$$
(v,u)\ \text{illegal} \iff \exists a \in \mathrm{shared}(P,Q),\ a \in A_P^O(v)\setminus A_Q^I(u)\ \lor\ a \in A_Q^O(u)\setminus A_P^I(v)
$$

上式中的符号逐项解释如下：

1. `(v,u)` 是 product automaton 的组合状态。
2. `A_P^O(v)` 表示在状态 `v` 可发出的输出动作。
3. `A_Q^I(u)` 表示在状态 `u` 可接受的输入动作。
4. 若一方能发而另一方不能收，该组合状态就是 illegal。

论文中的 `Cassandra` 预测并未再给出单独形式化元组；根据原文对“从当前状态向前展开 `k` 步预测树并着色 illegal states”的描述，可保守整理为：

$$
\mathrm{Pred}_k(s_{cur}) = \mathrm{Reach}_{\le k}(P \otimes Q, s_{cur}) \cap \mathrm{Illegal}(P,Q)
$$

这里是根据原文算法描述做的保守归纳，其中：

1. `s_{cur}` 是由 observer 上报的当前运行时组合状态。
2. `P \otimes Q` 表示参与 choreography 的行为 product。
3. `\mathrm{Reach}_{\le k}` 是向前不超过 `k` 步的可达状态集合。
4. 与 illegal 集合相交后即可得到“近未来可能发生的失败状态”。

### 一个最小例子与通俗解释

论文用一个文件共享 choreography 来解释 failure prediction：

1. 服务 `C` 需要向服务 `D` 发送 `msg1`，并随后触发写文件或读文件动作。
2. 设计时看，两个服务的接口自动机可组合，所以 choreography 可以先接受它们进入系统。
3. 运行时如果 `D` 已下线、角色被替换或当前状态不再接受该消息，`observer` 会把实时状态发给 `Cassandra`。
4. `Cassandra` 在当前状态上往前展开几步，一旦看到会落到 illegal state，就在消息真正送出前发出 warning。

通俗地说，这个体系像“把接口自动机分析外挂到总线旁边”，不是等故障真的发生再报错，而是让监控器提前看到“下一两步会撞车”。

### 运行 / 接受 / 转移语义

单个 `IA` 的运行由状态和动作交替序列组成：

$$
v_0, a_0, v_1, a_1, \dots, v_n
$$

上式中的符号逐项解释如下：

1. `v_i` 是某一步的接口状态。
2. `a_i` 是该步触发的动作。
3. 每一对 `(v_i, a_i, v_{i+1})` 都必须属于迁移集合 `T_P`。

运行时 product 的核心语义是：

1. 对共享动作做同步。
2. 对非共享动作做异步交错。
3. 一旦达到 illegal state，就说明该当前组合在接口层不可安全继续。
4. `Cassandra` 不是离线穷尽全局状态空间，而是从当前实际状态出发有限步预测。

### 语义边界

这篇论文的边界很明确：

1. 它主要处理离散接口行为，不显式建模时间、概率或连续动力学。
2. 服务真实内部逻辑仍被当作黑盒，论文只依赖公开行为模型。
3. `Cassandra` 预测依赖服务提供的行为规约与当前状态通知；若规约失真，预测也会偏差。
4. 主体是 choreography 运行时兼容与 failure prediction，不是一般 QoS 优化或服务编排综合。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `IA` 骨架 | `$P = \langle V_P, V_P^{init}, A_P^I, A_P^O, A_P^H, T_P \rangle$` | 单个服务的公开接口行为模型。 |
| 共享动作 | `$\mathrm{shared}(P,Q)$` | 决定哪些服务动作必须同步。 |
| illegal state | `$(v,u)\ \text{illegal}$` | 预测失败的直接判据。 |
| product 语义 | `$P \otimes Q$` | choreography 行为分析的基础。 |
| 近未来预测 | `$\mathrm{Pred}_k(s_{cur})$` | 运行时只向前看有限步，适应动态服务替换。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个参与服务都有显式接口状态。 |
| 事件 / 触发 | 强支持 | choreography 消息就是动作同步的核心。 |
| 守卫 / 数据 | 弱支持 | 主体不是复杂数据守卫，而是接口可接收性。 |
| 层次 | 弱支持 | 结构重点在 role-bundle 和 ESB，不在层次状态机。 |
| 并发 / 同步 | 强支持 | 共享动作同步与消息交错是主体。 |
| 时间约束 | 不支持 | 原文不以 clocks / deadlines 为核心。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散接口与消息交互问题。 |
| 可执行 / 可验证性 | 强执行、强验证 | 可以在 ESB 上运行，并做在线预测验证。 |

### 形式化问题与性质

1. 论文要解决的问题不是“静态能否组合”，而是“动态替换后还能否安全继续执行”。
2. `IA` 提供兼容骨架，`Cassandra` 提供在线前瞻能力，`ESB` 提供与真实运行时对接的承载层。
3. 它因此不是单纯理论条目，也不是单纯中间件实现条目，而是接口/组合主干与运行时基础设施之间的一条桥接线。

## 构造方式与承载格式

### 建模入口

建模入口通常是：

1. 为每个 choreography participant 准备一个接口行为模型。
2. 把该服务绑定到某个 role-bundle。
3. 在 `ESB` 上为角色之间的消息交换配置静态/动态路由。
4. 让 observer 把真实消息和运行时角色变更同步给 `Cassandra`。

### 机器可处理承载方式

原文直接给出的机器可处理承载方式包括：

1. `Interface Automata` 行为图。
2. 服务行为的 `SCXML` 规约。
3. `ServiceMix/Camel` 路由定义。
4. `Cassandra` 接收的 add/remove/state notification 消息。

### 交换与互操作

互操作重点在：

1. 角色替换时如何更新对应服务 endpoint。
2. observer 如何在不改业务逻辑的前提下观察消息流。
3. `Cassandra` 如何把当前状态与服务规约拼成预测树。

## 配套基础设施

- 建模/编辑工具：原文基于 `Apache ServiceMix`、`Apache Camel`、`SCXML` 与自定义 verification service 搭建。
- 解析/交换/元模型支持：有 `SCXML` 行为规约与 ESB 消息承载，但无单独统一元模型标准。
- 仿真/执行支持：真实运行依托 `ESB` 路由与 role-bundle。
- 验证/分析支持：`Cassandra` 支持运行时监控、当前状态识别与 `k` 步 failure prediction。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托 `SOA`、`Web Services`、`Interface Automata` 与 `SCXML` 生态。

## 适用场景与需求前提

### 适用场景

适合服务会动态加入、退出、替换，且系统不能接受“等故障发生后再发现”的 choreography、SOA 与 Future Internet 应用。

### 需求前提

1. 参与服务能够提供可信的接口行为模型。
2. 消息流可以被 ESB 或等价中间件截获。
3. choreography 角色与当前绑定关系可以被运行时感知。
4. 目标主要是接口层 failure prediction，而不是数值优化。

### 不适用或高成本场景

如果系统主要依赖隐式共享内存、复杂数据语义、概率故障或连续控制，仅靠本文这套 `IA + ESB + prediction` 框架表达会比较吃力。

## 与相邻形式主义的关系

相对 [Interface Automata](../interface-automata/desc.md)，本文没有扩展新的接口理论骨架，而是把 `IA` 真正接进动态服务组合的运行时体系；相对 [Towards Formal Interfaces for Web Services with Transactions](../towards-formal-interfaces-for-web-services-with-transactions/desc.md)，本文更强调 choreography 运行时监控与近未来预测，而不是补偿事务接口；相对 [A Runtime Environment for Contract Automata](../a-runtime-environment-for-contract-automata/desc.md)，这里的行为蓝本仍是 `IA`，且重点是 ESB 下的 failure prediction。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：接口/组合模型不是只能做离线兼容性证明，它还可以成为运行时观察、预测和修复闭环的行为层基础。

### 作为目标形式主义还是中间表示

对服务组合与 choreography 分析，它可以直接作为目标接口形式主义；对更大的控制软件，它更适合作为“交互层中间表示”。

### 对需求到模型生成的启发

1. 需求里关于“谁和谁交互、什么消息必须被接收”的约束，应优先抽成接口动作而不是纯文本说明。
2. 如果目标系统允许动态替换，生成模型时就不能只关注静态可组合性，还要保留当前状态与未来风险预测入口。
3. `SCXML` 一类可执行行为规约很适合作为接口模型落地载体。

## 重要的相关工作

- [Interface Automata](../interface-automata/desc.md)：本文所有运行时分析都建立在标准 `IA` product 与 illegal-state 语义之上。
- [Towards Formal Interfaces for Web Services with Transactions](../towards-formal-interfaces-for-web-services-with-transactions/desc.md)：同样面向 Web services 接口组合，但更偏长事务与补偿链。
- [An Introduction to Pervasive Interface Automata](../an-introduction-to-pervasive-interface-automata/desc.md)：同样关心动态替换与环境约束，但不直接提供本文这种 ESB 运行时架构。

## 文献分类总结

- 这是一篇 `🔌` 类应用型条目，核心价值是把 `Interface Automata` 从静态组合检查推进到动态 choreography 的运行时预测验证。
- 它的描述客体是服务角色与消息交互，因此记为 `🤝`；论文语境面向 Web services 与动态组合，因此记为 `🌐`。
- 对 `project_1` 来说，它证明了接口/组合模型可以自然进入“监控 - 预测 - 修复”的闭环，而不只是需求建模后的离线产物。
