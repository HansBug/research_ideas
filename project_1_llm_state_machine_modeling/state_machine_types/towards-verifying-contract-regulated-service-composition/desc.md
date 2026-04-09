# 面向契约约束服务组合的验证 / Towards Verifying Contract Regulated Service Composition

## 基本信息

- 标题：Towards Verifying Contract Regulated Service Composition
- 中文标题：面向契约约束服务组合的验证
- 作者：Alessio Lomuscio, Hongyang Qu, Monika Solanki
- 发表：*2008 IEEE International Conference on Web Services (ICWS 2008)*, pp. 254-261, 2008
- DOI：`10.1109/ICWS.2008.115`
- 链接：https://doi.org/10.1109/ICWS.2008.115
- 形式主义：`Contract-Regulated Service Composition / WSBPEL-to-ISPL Contract Verification`
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：契约约束服务组合验证 / `WSBPEL` 行为到 `ISPL/MCMAS` 的自动编译
- 工具/实现获取方式：原文明确实现了把 `WSBPEL` 行为与契约编译到 `ISPL` 的 compiler，并调用 `MCMAS` 做验证；论文未提供独立公开仓库。
- 标准/格式获取方式：承载方式是 `WSBPEL`、生成的 `ISPL`、`MCMAS` 输入模型与 temporal-epistemic 公式；原文未给统一交换标准。

## 简报

这篇论文处理的是“服务编排不仅要满足流程正确性，还要满足合同义务、违约、补救和知识条件”这个更强的问题。作者的做法不是直接设计新的 contract automata 家族，而是把服务 party 和其 contractually correct behaviour 都写成 `WSBPEL`，再编译成 `ISPL` 中的 automata / agent model，最后交给 `MCMAS` 检查 green/red state 与契约违规性质。

- 形式主义定位：这是接口/组合/契约主干上的应用型条目，重点在 contract-regulated service composition 的可验证建模链路。
- 构造方式简述：先写 `BPEL-behaviour` 与 `BPEL-contract`，再把两者翻译成 behaviour automata / contract automata，随后标记 green/red states、生成原子命题与时序公式，并输出 `ISPL` 给 `MCMAS`。
- 基础设施与场景简述：依托 `WSBPEL`、`ISPL`、`MCMAS` 与 temporal-epistemic logic，服务多方软件供应、测试、保险和部署参与者组成的电子服务合同编排验证。

```text
contract-regulated WSBPEL parties -> behaviour / contract automata -> green / red state labeling -> ISPL agents + temporal-epistemic properties -> MCMAS verification
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 作为 contract parties 的 Web services。
2. 每个 party 的 `BPEL-behaviour` 与 `BPEL-contract`。
3. 由编译器生成的 behaviour automata 与 contract automata。
4. `ISPL` 中的 environment、agents、local states 与 actions。
5. 标记 contract compliance / violation 的 green / red states。
6. 用于检查合规与违约可达性的 temporal-epistemic 公式。

### 核心抽象

论文对 `MCMAS/ISPL` 中单个 agent 的核心骨架给出了直接说明。可按原文整理为：

$$
Agent_i = \langle L_i, Act_i, P_i, Ev_i \rangle
$$

上式中的符号逐项解释如下：

1. `L_i` 是 agent `i` 的局部状态集合。
2. `Act_i` 是局部动作集合。
3. `P_i : L_i \to 2^{Act_i}` 是 protocol function，给出各局部状态下允许的动作。
4. `Ev_i` 是局部演化函数，用于根据联合动作更新状态。
5. 这四元骨架是论文对 `ISPL` 语义的直接描述。

论文还把每个 agent 的局部状态按契约合规性切成：

$$
L_i = G_i \cup R_i,\quad G_i \cap R_i = \emptyset
$$

上式中的符号逐项解释如下：

1. `G_i` 是 green states，对应合规行为。
2. `R_i` 是 red states，对应违反契约的行为。
3. 论文用这两个集合把 correctness / violation 变成可验证的状态口径。

从 `WSBPEL` 到 automata 的编译链可保守整理为：

$$
\mathrm{Compile}(B^{beh}_p, B^{ctr}_p) \to (A^{beh}_p, A^{ctr}_p) \to ISPL_p
$$

这里是根据原文流程图与 5.1-5.3 节做的保守归纳，其中：

1. `B^{beh}_p` 是某个 process / party 的实际行为 `WSBPEL`。
2. `B^{ctr}_p` 是其契约允许的正确行为 `WSBPEL`。
3. `A^{beh}_p` 与 `A^{ctr}_p` 分别是 behaviour automaton 和 contract automaton。
4. `ISPL_p` 是最终输出给 `MCMAS` 的 agent 代码。

论文给出的两类基础性质如下：

$$
E(pgreen \ U \ pend)
$$

以及

$$
EF\ pred
$$

上式中的符号逐项解释如下：

1. `pgreen` 是“当前处于 green state”的原子命题。
2. `pend` 是流程结束状态上的原子命题。
3. `pred` 是某个 red / violation state 对应的原子命题。
4. 第一条性质表示：存在一条执行能始终保持合规直到正常结束。
5. 第二条性质表示：存在一条执行能到达某个违约状态。

### 一个最小例子与通俗解释

论文里的示例是一个多方软件交付合同：

1. `PSP` 和 `SP` 负责软件组件开发与集成，`C` 是客户，`T` 是测试机构，`I` 是保险方，`H` 是硬件提供者，`E` 是部署专家。
2. 合同规定 `PSP` / `SP` 必须两次更新进度，客户 `C` 必须在第二次更新前提出修改，否则属于违约并需支付罚金。
3. 编译器把这些 `WSBPEL` 活动翻译成 automata，并把“按时更新”“晚改需求”等阶段标成 green/red。
4. `MCMAS` 再检查：是否存在完全合规的一条执行？是否存在某个参与方会走到违约状态？

通俗地说，这套方法像“把合同文本变成服务交互流程图，再把流程图变成一台会标记‘守约/违约’的状态机”，然后让模型检查器穷尽看看系统会不会跑偏。

### 运行 / 接受 / 转移语义

论文中的运行语义有两层：

1. `WSBPEL` 层：
   - `receive/reply/assign/sequence/wait` 等活动构成服务执行流程。
   - 正常行为与 contractually correct behaviour 都可以用 `WSBPEL` 表达。
2. `ISPL/automata` 层：
   - 每个 transition 被映射为一个 action。
   - 若某 transition 源状态为 `s_1`、目标状态为 `s_2` 且 guard 为 `c`，则生成对应 evolution item。

论文直接给出的典型 evolution item 可整理为：

$$
state = s_2 \ \text{if}\ state = s_1 \land c \land Action = t
$$

上式中的符号逐项解释如下：

1. `state` 是 `ISPL` 中额外加入的枚举型状态变量。
2. `s_1` 与 `s_2` 是自动机中的源/目标状态。
3. `c` 是 guard 条件。
4. `Action = t` 表示当前执行的动作对应某条 automaton transition。
5. 若该 transition 与其他 agent 同步，还要把对方 action 一并加入条件。

### 语义边界

这篇论文的边界主要在于：

1. 主体关注 contract compliance / violation，而不是一般数据语义或 QoS 优化。
2. 服务行为需要先能以 `WSBPEL` 和有限状态方式表示。
3. 论文把 Web service 视作 MAS 中的 agents，因此更适合离散交互场景。
4. 合同知识与义务可以进入 temporal-epistemic 逻辑，但连续时间与概率不是主体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `ISPL` agent 骨架 | `$Agent_i = \langle L_i, Act_i, P_i, Ev_i \rangle$` | 每个 contract party 在模型检查器中的行为接口。 |
| 合规 / 违约划分 | `$L_i = G_i \cup R_i,\ G_i \cap R_i = \emptyset$` | 用 green/red 状态表达 contractual correctness。 |
| 编译链 | `$\mathrm{Compile}(B^{beh}_p, B^{ctr}_p) \to (A^{beh}_p, A^{ctr}_p) \to ISPL_p$` | 把 BPEL 行为与合同压成可检模型。 |
| 合规完成性 | `$E(pgreen \ U \ pend)$` | 是否存在一条完全合规直到结束的执行。 |
| 违约可达性 | `$EF\ pred$` | 是否存在违约路径。 |
| 演化规则 | `$state = s_2 \ \text{if}\ state = s_1 \land c \land Action = t$` | automata 迁移如何落到 `ISPL` 演化函数。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个服务 party 都有显式局部状态与 green/red 合规状态。 |
| 事件 / 触发 | 强支持 | `WSBPEL` 活动、消息与违约恢复动作是核心。 |
| 守卫 / 数据 | 部分支持 | `ISPL` 变量和 guard 支持离散条件，但不是复杂数据流分析。 |
| 层次 | 弱支持 | 重点是流程与 agent 组合，不是层次状态机。 |
| 并发 / 同步 | 强支持 | 多个 contract parties 并行、同步动作与服务组合是主体。 |
| 时间约束 | 弱支持 | 论文可表达“是否按时更新”这类流程约束，但不使用 clocks 作为主模型。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散契约交互。 |
| 可执行 / 可验证性 | 强验证 | `MCMAS` 可直接检查合规、违约与知识性质。 |

### 形式化问题与性质

1. 论文把“合同文本约束”转成了可穷尽检查的自动机与时序逻辑对象。
2. 它补出的不是一般接口兼容，而是“行为是否守约”这一层更强的 contract semantics。
3. green/red 标记使违约路径不再只是注释，而是显式模型状态。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 为每个 contract party 写 `WSBPEL` 行为。
2. 单独写出其 contractually correct `WSBPEL`。
3. 把两者翻译成 behaviour / contract automata。
4. 根据契约 automata 给 behaviour automata 标 green/red。
5. 生成 `ISPL` 与待验证公式，交给 `MCMAS`。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `WSBPEL` 过程。
2. behaviour automata 与 contract automata。
3. `ISPL` 代码。
4. `MCMAS` 验证公式。

### 交换与互操作

互操作重点在：

1. 服务 party 的 `WSBPEL` 结构如何映射成 automata。
2. contract automata 如何回标到 behaviour automata 的 green/red states。
3. 多 agent 动作同步如何落到 `ISPL` evolution items。

## 配套基础设施

- 建模/编辑工具：原文基于 `WSBPEL` 服务编排描述和自研 compiler。
- 解析/交换/元模型支持：有 `WSBPEL -> ISPL` 翻译链，但无独立元模型标准。
- 仿真/执行支持：论文主体不强调服务执行引擎，重点在验证链。
- 验证/分析支持：`MCMAS` 支持 `CTL`、epistemic、deontic/temporal-epistemic 性质验证。
- 代码生成/转换支持：支持从 `WSBPEL` 半自动生成 `ISPL`。
- 标准化或社区生态：依托 `WSBPEL` 与 `MCMAS` / MAS verification 生态。

## 适用场景与需求前提

### 适用场景

适合多方电子服务编排、供应链软件交付、存在违约/补救/罚金条件的服务合同组合。

### 需求前提

1. 服务行为能被 `WSBPEL` 或等价有限流程表示。
2. 合同中的义务、违规与补救条款可离散化成显式状态或条件。
3. 关注重点是“是否守约 / 何时违约”，而不是性能优化。
4. 参与方交互边界明确，允许按 agent 方式分解。

### 不适用或高成本场景

如果系统关键难点在高维数据处理、连续物理控制或概率服务质量，仅靠本文这条 `WSBPEL -> automata -> ISPL` 链会过于粗粒度。

## 与相邻形式主义的关系

相对 [Automata for Analysing Service Contracts](../contract-automata/desc.md)，本文不是提出 `Contract Automata` 家族，而是把契约约束服务组合接到 `WSBPEL/MCMAS` 验证链上；相对 [Specification and Verification of Context-dependent Services](../specification-and-verification-of-context-dependent-services/desc.md)，这里更强调多方合同义务与违约状态，而不是上下文敏感服务配置；相对 [A Flexible Architecture to Monitor Dynamic Web Services Composition](../a-flexible-architecture-to-monitor-dynamic-web-services-composition/desc.md)，这里偏设计时 / 离线验证，而非运行时 choreography failure prediction。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果需求里本来就有“义务、违规、罚则、恢复”这类合同语义，那么生成的状态机不该只保留控制流，还应显式保留 compliance / violation 层。

### 作为目标形式主义还是中间表示

对服务组合与合同分析，它可以直接作为目标形式主义；对更广的控制软件需求建模，它更适合作为交互契约层的中间表示。

### 对需求到模型生成的启发

1. 自然语言需求中的“必须 / 禁止 / 若违反则补救”可以直接转成 green/red state 口径。
2. 行为模型与合同模型可以分开生成，再做对齐标色，而不是混成一张图。
3. 时序逻辑性质最好跟模型同时生成，否则违约分析很难自动化。

## 重要的相关工作

- [Automata for Analysing Service Contracts](../contract-automata/desc.md)：后续更系统地把服务契约抽成 automata 家族。
- [Specification and Verification of Context-dependent Services](../specification-and-verification-of-context-dependent-services/desc.md)：同样面向服务契约验证，但更偏上下文与组合算子。
- [A Flexible Architecture to Monitor Dynamic Web Services Composition](../a-flexible-architecture-to-monitor-dynamic-web-services-composition/desc.md)：同样属于服务组合验证，但侧重运行时监控和未来故障预测。

## 文献分类总结

- 这是一篇 `🔌` 类应用型条目，核心价值是把契约约束服务组合从 `WSBPEL` 编排推进到 automata / `ISPL` / `MCMAS` 的可验证链路。
- 它描述的对象是多方服务与契约交互，因此记为 `🤝`；论文语境是服务组合与电子业务协作，因此记为 `🌐`。
- 对 `project_1` 来说，它提供了一个很直接的启发：需求里的合规性、违规和补救逻辑，其实天然就是状态机里的模式切换与性质生成素材。
