# 系统之系统接口契约行为建模 / Modelling System of Systems Interface Contract Behaviour

## 基本信息

- 标题：Modelling System of Systems Interface Contract Behaviour
- 中文标题：系统之系统接口契约行为建模
- 作者：Oldrich Faldik, Richard Payne, John Fitzgerald, Barbora Buhnova
- 发表：*Electronic Proceedings in Theoretical Computer Science*, 245:1-15, 2017
- DOI：`10.4204/eptcs.245.1`
- 链接：https://doi.org/10.4204/eptcs.245.1
- 形式主义：`Extended Interface Automata for Contract + SysML/OCL Contract Pattern`
- 主类：🔌
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：`SoS` 契约兼容性建模 / 音视频系统案例
- 工具/实现获取方式：原文依托 `SysML`、`OCL` 和 contract pattern；提出可作为 `Symphony` 外挂自动验证的方向，但未提供现成公开工具。
- 标准/格式获取方式：承载方式是 `SysML` views、`OCL` notes 与 extended interface automata；无独立交换格式。

## 简报

这篇论文的价值，在于把 `SoS` 合同工程和接口自动机真的接起来。作者并不满足于“在 `SysML` 里写合同”，而是进一步把 contract variables、pre/post conditions 和 protocol states 翻译成可组合、可判 illegal states 的 extended interface automata。它因此同时解决了两个问题：一是把 `CML` 改成更贴近 `SysML` 生态的 `OCL`，二是让 constituent systems 之间的 contract compatibility 有了更直接的接口级验证骨架。

- 形式主义定位：面向 `SoS` constituent contracts 与交互兼容性的接口/组合模型，不是一般组件 DSL。
- 构造方式简述：先在 Contract Pattern 中用 `SysML + OCL` 描述 contract definition / protocol，再翻译成 extended interface automata 做 composition 与 illegal-state 分析。
- 基础设施与场景简述：依托 `SysML`、`OCL`、contract pattern、extended `IA` 和 `LE Device / Transport Layer` 案例，服务音视频 `SoS` 的 contract conformance 与 compatibility。

```text
SoS contract views -> SysML/OCL constraints -> extended interface automata -> synchronized product / illegal states -> contract compatibility analysis
```

## 形式主义定义与核心对象

### 定义对象

论文处理的对象有四层：

1. `SoS` 中 constituent system 的 contract definition。
2. contract protocol states 与操作可见性。
3. contract variables 及其 `OCL` pre/post 约束。
4. 由多个 contract interface 组成的同步 product 与 illegal states。

### 核心抽象

原文把 contract 的扩展接口自动机定义为：

$$
A(C) = \langle S_A, I_A, S_A^I, S_A^O, S_A^H, V_A, Pre_A, Post_A, d_A \rangle
$$

上式中的符号逐项解释如下：

1. `S_A` 是 contract protocol 的状态集合。
2. `I_A` 是初始状态集合。
3. `S_A^I`、`S_A^O`、`S_A^H` 分别是输入、输出和隐藏动作集合。
4. `V_A` 是 contract variables 集合。
5. `Pre_A` 是动作前置条件集合，由 `OCL` 表达。
6. `Post_A` 是动作后置条件集合，由 `OCL` 表达。
7. `d_A` 是带语义约束的迁移集合。

两个 contract interface 的共享动作仍由输入/输出交集决定：

$$
\mathrm{Shared}(A_1, A_2) = (S_1^I \cap S_2^O) \cup (S_2^I \cap S_1^O)
$$

上式中的符号逐项解释如下：

1. `S_i^I` 是第 `i` 个 contract automaton 的输入动作集合。
2. `S_i^O` 是第 `i` 个 contract automaton 的输出动作集合。
3. 共享动作是两个 contract 能同步通信的唯一入口。

同步 product 则被写成：

$$
A_1 \otimes A_2 = \langle S_1 \times S_2, I_1 \times I_2, S^I, S^O, S^H, V_1 \cup V_2, Pre, Post, d \rangle
$$

上式中的符号逐项解释如下：

1. `S_1 \times S_2` 是组合后的状态空间。
2. `S^I`、`S^O`、`S^H` 是组合后的输入、输出与隐藏动作集合。
3. `V_1 \cup V_2` 是双方 contract variables 的并集。
4. `Pre` 与 `Post` 会在共享动作同步时做合取组合。

### 一个最小例子与通俗解释

论文里的最小直觉例子是 `LE Device` 与 `Transport Layer`：

1. `LE Device` 会输出 `sendMessages`。
2. `Transport Layer` 必须把 `sendMessages` 作为输入接收。
3. 如果 `Transport Layer` 当前状态下没有这个输入，或者对应 `OCL` 前后置条件为假，就形成 illegal state。
4. 只有在协议状态与 `OCL` 语义都匹配时，这两个 contract 才能被视为可组合。

通俗地说，这个模型像是在问：“两个系统之间不仅接口名对不对，而且在当前合同状态下，这次调用到底被不被允许、调用后承诺的变量更新到底对不对。”

### 运行 / 接受 / 转移语义

共享动作同步时，原文把前后置条件做合取：

$$
pre = pre_1 \land pre_2 \qquad post = post_1 \land post_2
$$

上式中的符号逐项解释如下：

1. `pre_i` 是第 `i` 个接口上该共享动作的前置条件。
2. `post_i` 是第 `i` 个接口上该共享动作的后置条件。
3. 组合接口只有同时满足两侧约束时，才允许该同步动作。

illegal state 的核心判定可压缩为：

$$
(s_1, s_2) \in \mathrm{Illegal}(A_1, A_2)
$$

当且仅当发生以下两类冲突之一：

1. 一侧要求的共享功能没有被另一侧提供。
2. 所有可用同步迁移的 `pre` 或 `post` 最终化简为 `false`。

### 语义边界

这篇论文的边界主要有三点：

1. 它处理的是 `SoS` 合同兼容，不是一般控制器执行语义。
2. 时间、概率和连续动力学并不是核心对象，重点在 contract protocol 与 `OCL` 约束。
3. 论文主要完成了形式化映射与 case study，自动化工具链仍停留在未来工作层面。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| contract 扩展接口自动机 | `$A(C) = \langle S_A, I_A, S_A^I, S_A^O, S_A^H, V_A, Pre_A, Post_A, d_A \rangle$` | 把 contract states、variables 与 `OCL` 约束统一进自动机。 |
| 共享动作 | `$\mathrm{Shared}(A_1, A_2)$` | 判断两个 contract 的同步通信入口。 |
| 同步 product | `$A_1 \otimes A_2$` | 构造组合后的 contract interface。 |
| 组合语义 | `$pre = pre_1 \land pre_2,\ post = post_1 \land post_2$` | 同步动作必须同时满足两侧约束。 |
| illegal states | `$(s_1,s_2)\in \mathrm{Illegal}(A_1,A_2)$` | 缺失服务或 `OCL` 语义不满足都会导致非法。 |
| compatibility | `$I_{A_1 \otimes A_2} \cap \mathrm{Comp}(A_1,A_2) \neq \emptyset$` | 组合后仍存在合法初始兼容状态时，contract 才可组合。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | contract protocol states 是显式对象。 |
| 事件 / 触发 | 强支持 | 输入、输出、隐藏操作都被分类建模。 |
| 守卫 / 数据 | 强支持 | `OCL` 前置、后置与变量约束是一等对象。 |
| 层次 | 弱支持 | 重点不在层次状态结构。 |
| 并发 / 同步 | 强支持 | 通过 shared actions 与 product 建模 constituent interaction。 |
| 时间约束 | 弱支持 | 可表达 timing-related contracts，但本体不是时钟自动机。 |
| 连续动态 / 随机性 | 不支持 | 不处理连续物理过程。 |
| 可执行 / 可验证性 | 中强验证 | 兼容性分析骨架清晰，但自动工具仍需额外实现。 |

### 形式化问题与性质

1. 论文的关键不是“把 `SysML` 翻译成别的语言”，而是让 contract behavior 真正能落到自动机级组合分析。
2. `OCL` 在这里承担了 contract semantics 的角色，而不是只是注释。
3. illegal states 的定义把“接口没接上”和“约束虽接上但语义为假”统一起来了。
4. 它是从 `SoS` 合同工程走向可验证接口模型的一条稳定路线。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下顺序：

1. 用 Contract Pattern 确定 constituent systems 与 contracts。
2. 在 Contract Definition View 中写 invariants 以及 `OCL` pre/post。
3. 在 Contract Protocol View 中写 states 与 guarded transitions。
4. 将 input/output/hidden 操作分类后翻译成 extended interface automata。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `SysML` contract views。
2. `OCL` notes 形式的 invariants / preconditions / postconditions。
3. extended interface automata 元组。
4. synchronized product 与 illegal-state 集合。

### 交换与互操作

互操作重点不在 XML 或 schema，而在：

1. 合同操作是否按 input/output/hidden 正确分类。
2. 协议状态是否允许该交互发生。
3. `OCL` 约束组合后是否仍然可满足。

## 配套基础设施

- 建模/编辑工具：原文依赖 `SysML` 建模环境和 `OCL` 约束书写方式。
- 解析/交换/元模型支持：以 Contract Pattern 视图和 extended `IA` 为主，未给公开 exchange schema。
- 仿真/执行支持：重点不在执行器，而在 contract composition analysis。
- 验证/分析支持：可检查 composability、synchronized product 与 illegal states。
- 代码生成/转换支持：原文未提供自动生成代码链路。
- 标准化或社区生态：依托 `SysML`、`OCL`、`SoS` contract pattern 与 interface automata 社区。

## 适用场景与需求前提

### 适用场景

适合 `SoS`、服务型系统、音视频网络、分布式协作系统等“每个 constituent system 都相对独立，但必须在合同边界上保持好公民行为”的场景。

### 需求前提

1. constituent systems 的交互接口必须能显式枚举。
2. 协议行为需要可写成有限状态。
3. 关键约束能够用 `OCL` 或等价布尔表达式描述。
4. 分析目标是 contract compatibility，而不是连续控制精度。

### 不适用或高成本场景

如果系统的关键难点是复杂实时调度、连续物理闭环或大规模概率失效，单靠这套 contract automata 骨架并不够。

## 与相邻形式主义的关系

相对 [refinement-of-interface-automata-strengthened-by-action-semantics/desc.md](../refinement-of-interface-automata-strengthened-by-action-semantics/desc.md)，本文把 `pre/post` 语义接口模型接入了 `SysML/OCL` 合同工程；相对 [a-runtime-environment-for-contract-automata/desc.md](../a-runtime-environment-for-contract-automata/desc.md)，它更偏前端建模与 contract composition，而不是运行时编排引擎；相对 [specification-and-verification-of-context-dependent-services/desc.md](../specification-and-verification-of-context-dependent-services/desc.md)，它更强调 constituent contracts 在 `SoS` 语境下的协议可组合性。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果未来要让 LLM 从系统级需求直接产出“可验证的交互层模型”，那么 contract variables、协议状态和 `pre/post` 约束必须一起抽。

### 作为目标形式主义还是中间表示

对 `SoS` 合同兼容分析，它可以直接作为目标形式主义；对一般控制系统，它更适合作为“接口与协议约束层”的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把 constituent roles、接口可见性和协议状态同时建模。
2. `OCL` 这类约束语言很适合承接从自然语言中抽出的 contract clauses。
3. LLM 生成交互模型时，不能只画状态图，还要明确哪些变量与操作构成合同。

## 重要的相关工作

- [interface-automata/desc.md](../interface-automata/desc.md)：接口自动机的原始理论蓝本。
- [refinement-of-interface-automata-strengthened-by-action-semantics/desc.md](../refinement-of-interface-automata-strengthened-by-action-semantics/desc.md)：把动作语义引入 refinement 的关键前序工作。
- [a-runtime-environment-for-contract-automata/desc.md](../a-runtime-environment-for-contract-automata/desc.md)：展示契约模型进一步落到运行时编排的路线。

## 文献分类总结

- 这是一篇 `🔌` 类高价值条目，核心贡献是把 `SoS` contract pattern、`OCL` 约束和 extended interface automata 串成同一条 compatibility 线。
- 其描述客体是 constituent interfaces 与 contracts，因此记为 `🤝`；论文语境聚焦 `SoS` 与网络化交互，因此记为 `🌐`。
- 对 `project_1` 来说，它补足了“系统级合同如何转成可验证交互自动机”这一层关键桥梁。
