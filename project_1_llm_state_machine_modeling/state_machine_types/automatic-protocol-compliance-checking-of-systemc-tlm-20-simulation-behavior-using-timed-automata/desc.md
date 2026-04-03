# 基于定时自动机的 SystemC TLM-2.0 协议合规检查 / Automatic Protocol Compliance Checking of SystemC TLM-2.0 Simulation Behavior Using Timed Automata

## 基本信息

- 标题：Automatic Protocol Compliance Checking of SystemC TLM-2.0 Simulation Behavior Using Timed Automata
- 中文标题：基于定时自动机的 SystemC TLM-2.0 仿真行为协议合规检查
- 作者：Mehran Goli, Jannis Stoppe, Rolf Drechsler
- 发表：*2017 IEEE International Conference on Computer Design (ICCD)*, pp. 377-384, 2017
- DOI：`10.1109/ICCD.2017.65`
- 链接：https://doi.org/10.1109/ICCD.2017.65
- 形式主义：`Timed Automata / SystemC TLM Protocol-Compliance Model`
- 主类：⏱️
- 描述客体：🤝
- 所属领域：💻
- 论文角色：`SystemC/TLM` 协议合规检查 / 定时自动机应用建模
- 工具/实现获取方式：原文用 `GDB` 非侵入式提取 `SystemC TLM-2.0` 运行日志，再自动生成 timed automata 和 `UPPAAL` 查询完成协议检查；论文未公开独立仓库。
- 标准/格式获取方式：承载方式是 `GDB` 运行时日志、作者定义的 transaction lifetime 结构、`UPPAAL` timed automata 与 TCTL 风格查询；无统一交换标准。

## 简报

这篇论文解决的是一个很实际的问题：`SystemC TLM-2.0` 标准里有一百多条规则，但编译器和库本身并不会在运行时告诉你模型是不是违反了这些协议语义。作者的方案不是直接去形式化整个 `SystemC` 语言，而是先用 `GDB` 抓仿真时的 transaction lifetime，再把这些 lifetime 自动翻成 timed automata，最后用 `UPPAAL` 检查它是否遵守 `TLM-2.0` 的 dynamic rules。

- 形式主义定位：这是 `Timed Automata` 在电子系统级建模协议检查上的应用条目，重点是“仿真行为抽取 -> timed automata -> protocol queries”。
- 构造方式简述：通过 `GDB` 提取 transaction ID、phase、delay、return status 和 involved modules，再把每个 transaction lifetime 编译成 timed automaton。
- 基础设施与场景简述：依托 `SystemC/TLM-2.0`、`GDB`、transaction log translation 和 `UPPAAL`，服务 `ESL` 参考模型与协议合规检查场景。

```text
SystemC TLM simulation -> GDB transaction log -> transaction lifetime -> timed automata + temporal properties -> UPPAAL protocol compliance checking
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `SystemC TLM-2.0` 模型及其 transaction lifetime。
2. 通过 `GDB` 提取的运行时日志。
3. 对应单个 transaction 的 timed automaton。
4. 由 `TLM-2.0` dynamic rules 转写而来的 temporal properties。
5. `UPPAAL` 中的 query-based 协议检查。

### 核心抽象

论文直接给出了 timed automaton 定义：

$$
TA = (L, l_0, C, A, E, I)
$$

上式中的符号逐项解释如下：

1. `$L$` 是位置集合，对应 transaction lifetime 中的各个 timing step。
2. `$l_0 \in L$` 是初始位置。
3. `$C$` 是 clock 集合。
4. `$A$` 是动作集合。
5. `$E \subseteq L \times A \times B(C) \times 2^C \times L$` 是边集合。
6. `$I : L \to B(C)$` 把 invariants 绑定到位置。

论文进一步给出了 timed automaton 的语义转移系统：

$$
(S, s_0, \to), \qquad S \subseteq L \times \mathbb{R}_{\ge 0}^{|C|}
$$

以及离散转移：

$$
(l,u) \xrightarrow{a} (l',u') \iff l \xrightarrow{(a,g,r)} l' \land u \in g \land u' = [r \mapsto 0]u \land u' \in I(l')
$$

上式中的符号逐项解释如下：

1. `$u$` 是当前 clock valuation。
2. `$g$` 是 guard。
3. `$r$` 是在边上需要复位的时钟集合。
4. `$u' = [r \mapsto 0]u$` 表示对应 clocks 在转移后归零。
5. `$I(l')$` 保证新状态仍满足目标位置不变式。

论文里一个具体 transaction lifetime 会被翻成如下形式：

$$
TA_{tx} = (L_{tx}, l_0, \{clk\}, \varnothing, E_{tx}, I_{tx})
$$

其中 `clk` 用来保证每个 transaction step 在规定时间点离开。作者给出的例子里，`AT_typeA_initiator -> AT_interconnect -> AT_typeE_target -> ...` 会被压成一条有限路径型 automaton。

### 一个最小例子与通俗解释

论文里的最小直觉例子就是一个 `AT-example` transaction：

1. initiator 创建事务并进入 `BEGIN_REQ`。
2. interconnect 转发它。
3. target 接收后返回 `TLM_COMPLETED`。
4. 作者把这个 lifetime 中的每个步骤变成一个 location，并用 `clk==0,1,2,3` 等 guard 约束步骤次序。

通俗地说，这像“先把一次事务执行录像下来，再把录像逐帧翻成带秒表的状态机”。这样就不用去完整形式化所有 `SystemC` 语法，而是直接检查一次真实仿真是否违背了 `TLM` 协议。

### 运行 / 接受 / 转移语义

论文中的关键不是识别某个语言，而是检查 transaction semantics 和 communication semantics 是否满足协议规则。比如 transaction response status 的默认值要求被写成：

$$
(l_i \land transact.tstatus = 0) \leadsto (l_{i+1} \land transact.tstatus = 0)
$$

上式中的符号逐项解释如下：

1. `transact.tstatus = 0` 表示 response status 仍为 `TLM_INCOMPLETE_RESPONSE`。
2. `$l_i, l_{i+1}$` 是 transaction lifetime 中相邻两步。
3. 这条规则对应标准中“默认 response status 必须保持为 `TLM_INCOMPLETE_RESPONSE`”。

另一条 communication semantics 规则则要求：

$$
(l_i \land tlm\_return\_status \neq 2 \land transact.tphase = p) \leadsto (l_{i+1} \land transact.tphase = p)
$$

上式中的符号逐项解释如下：

1. `tlm_return_status = 2` 在文中对应 `TLM_UPDATED`。
2. 若没有返回 `TLM_UPDATED`，就不允许 phase transition 合法发生。
3. `p` 表示某个特定 transaction phase。

这些规则最终都被编进 `UPPAAL` 查询数据库，作者提到一共定义了 `40` 个 template properties，其中 `15` 条检查 transaction semantics，`25` 条检查 communication semantics。

### 语义边界

这篇论文的边界主要有：

1. 它验证的是一次仿真行为的协议合规性，而不是所有可能 `SystemC` 程序的完整语义。
2. 方法依赖可用的 debug information 与 `GDB` 兼容执行环境。
3. 所有 timing annotations 在进入 `UPPAAL` 时都要离散成整数。
4. 它更像“运行时轨迹后验形式化”，不是直接从源码静态综合整套 timed automata。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton 骨架 | `$TA = (L, l_0, C, A, E, I)$` | 单个 transaction lifetime 的标准表示。 |
| 语义转移系统 | `$(S, s_0, \to)$` | 给出 automaton 的形式语义。 |
| 离散转移规则 | `$(l,u) \xrightarrow{a} (l',u')$` | 用 guards / resets 承接 transaction step。 |
| response status 规则 | `$(l_i \land transact.tstatus = 0) \leadsto (l_{i+1} \land transact.tstatus = 0)$` | 默认 response status 不能被非法改写。 |
| phase transition 规则 | `$(l_i \land tlm\_return\_status \neq 2 \land transact.tphase = p) \leadsto (l_{i+1} \land transact.tphase = p)$` | 未返回 `TLM_UPDATED` 时不应发生 phase transition。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个 transaction lifetime step 都被显式建成 location。 |
| 事件 / 触发 | 强支持 | `BEGIN_REQ`、`TLM_COMPLETED`、return status 等都是一等对象。 |
| 守卫 / 数据 | 强支持 | transaction attributes、phase、delay、return value 都进入 guards / updates。 |
| 层次 | 不支持 | 模型是平铺 transaction automata，不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 重点在单 transaction lifetime，但不同 modules 的交互被编码进轨迹。 |
| 时间约束 | 强支持 | delay annotations 和 `clk` 直接约束 phase sequence。 |
| 连续动态 / 随机性 | 不支持 | 纯离散协议行为。 |
| 可执行 / 可验证性 | 很强 | `GDB` 抽取 + `UPPAAL` 检查构成稳定闭环。 |

### 形式化问题与性质

1. 论文真正补的是“怎样把一次仿真行为自动形式化到 timed automata”，而不是一般 `TLM` 文本规范。
2. 这条路线把传统 simulation-based verification 和 formal verification 接到了一起。
3. 对 `project_1` 很有启发：当原始系统语义难以直接建模时，可以先抓运行轨迹，再反推形式模型。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 用 `GDB` 记录 transaction ID、phase、timing、return status 和 involved modules。
2. 把日志整理成 transaction lifetime。
3. 为每个 lifetime 生成 timed automaton。
4. 把 `TLM-2.0` dynamic rules 转成 temporal properties。
5. 在 `UPPAAL` 里把 automata 和 queries 一起求证。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `GDB` 运行时日志。
2. transaction lifetime 结构化表示。
3. `UPPAAL` timed automata。
4. query templates。

### 交换与互操作

互操作链路非常明确：

1. `SystemC` 运行时通过 `GDB` 暴露行为。
2. 提取器将行为翻译成 timed automata。
3. 规则模板库将标准规则翻译成 `UPPAAL` 查询。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：`GDB` 抽取器 + 作者定义的 lifetime translator；无统一外部元模型。
- 仿真/执行支持：以 `SystemC/TLM` 仿真作为数据源。
- 验证/分析支持：`UPPAAL 4.1` 检查 protocol compliance。
- 代码生成/转换支持：支持从运行日志自动生成 timed automata，但不生成部署代码。
- 标准化或社区生态：依托 `SystemC TLM-2.0` 标准与 `UPPAAL` 生态。

## 适用场景与需求前提

### 适用场景

适合已有 `SystemC TLM-2.0` 可执行模型、希望检查 transaction 是否违反标准协议规则的电子系统级设计流程。

### 需求前提

1. 模型可在 `GDB` 下运行并暴露调试信息。
2. 关键正确性问题集中在 transaction / protocol semantics，而不是连续物理模型。
3. timing annotations 和 phase 语义可离散成有限步骤。

### 不适用或高成本场景

如果设计没有可调试执行环境、行为依赖大量不可观测外设，或要求完整源级语义证明，这条方法会受到明显限制。

## 与相邻形式主义的关系

相对 [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)，本文不是直接从协议规范手工建模，而是从仿真行为自动反推 timed automata；相对 [automatic-verification-of-component-based-real-time-corba-applications/desc.md](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)，两者都面向组件/中间件时序，但这里更偏 transaction protocol compliance；相对 [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，这里关注的是 `ESL/TLM` 协议层，而不是机器人中间件通信。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当目标系统本体过于复杂，无法直接从需求一步生成干净模型时，可以先抓关键运行行为，再将其规范化成 timed automata 做合规检查。

### 作为目标形式主义还是中间表示

对 `TLM` 协议检查，它更像运行时到形式验证之间的中间表示；但对特定 transaction semantics，它也可以成为直接验证对象。

### 对需求到模型生成的启发

1. 日志/轨迹可以是形式模型生成的输入，不一定非要从自然语言直接到模型。
2. 复杂标准中的规则库适合先模板化，再绑定到自动机查询。
3. 对“协议合规”类需求，应优先保留 phase、return status 和 timing annotations。

## 重要的相关工作

- [automatic-verification-of-component-based-real-time-corba-applications/desc.md](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)：同样处理组件/中间件时序验证，但建模入口不同。
- [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)：展示从协议语义直接手工建模的另一条 timed automata 路线。
- [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：说明 timed automata 可继续推广到其他运行时通信框架。

## 文献分类总结

- 形式主义：`Timed Automata / SystemC TLM Protocol-Compliance Model`
- 成熟度：`GDB -> timed automata -> UPPAAL` 的非侵入式链路很清楚，适合作为复杂运行时系统的形式化桥接样板。
- 条目价值：这是一篇 `⏱️` 类高价值应用条目，核心贡献是把 `SystemC TLM-2.0` 仿真行为自动翻成 timed automata 做协议合规检查。
