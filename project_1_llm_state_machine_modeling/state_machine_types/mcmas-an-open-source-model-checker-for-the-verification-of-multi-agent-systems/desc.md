# MCMAS：多智能体系统开源模型检查器 / MCMAS: an open-source model checker for the verification of multi-agent systems

## 基本信息

- 标题：MCMAS: an open-source model checker for the verification of multi-agent systems
- 中文标题：MCMAS：多智能体系统开源模型检查器
- 作者：Alessio Lomuscio，Hongyang Qu，Franco Raimondi
- 发表：*International Journal on Software Tools for Technology Transfer*，19(1): 9-30，2017
- DOI：`10.1007/s10009-015-0378-x`
- 链接：https://doi.org/10.1007/s10009-015-0378-x
- 形式主义：`Interpreted Systems / ISPL / ATLK / MCMAS`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：symbolic multi-agent model checker for temporal, epistemic and strategic properties
- 工具/实现获取方式：原文明确给出 `MCMAS` 官网入口 `http://vas.doc.ic.ac.uk/software/mcmas/`，并说明其为开源工具。
- 标准/格式获取方式：主承载是 `ISPL`（Interpreted Systems Programming Language）模型、`ATLK` 公式、fairness 条件和 witness/counterexample 输出；它不是行业交换标准，而是多智能体验证工具链载体。

## 简报

这篇论文补的是多智能体系统验证里的经典平台线。`MCMAS` 的核心不是发明新的 agent 状态机母型，而是把 interpreted systems、`ATLK`、`OBDD` 和 `ISPL` 真正做成一个能处理知识、群知识、战略能力、公平性和反例/证据的统一检查器。

- 形式主义定位：多智能体系统的 symbolic verification infrastructure，而不是新的 agent-statechart 语法家族。
- 构造方式简述：用 `ISPL` 显式声明 agent 的 local states、actions、protocols、evolution，再把全局系统解释成 interpreted system，并在其上检查 `ATLK` 公式。
- 基础设施与场景简述：依托 `OBDD`、`ISPL`、fairness、uniform strategies、counterexample/witness generation 和 Eclipse 插件，服务协议分析、安全协议、协同决策与分布式交互系统验证。

```text
agents + local protocols + local evolutions -> ISPL model -> interpreted system / induced model -> ATLK checking + fairness + witness/counterexample
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. interpreted systems；
2. `ISPL` 建模语言；
3. `ATLK` 公式，包括 temporal、epistemic 和 strategic operators；
4. `OBDD`-based symbolic model checking；
5. fairness、uniform strategies、counterexamples 与 witnesses。

### 核心抽象

论文直接给出 interpreted system 的骨架：

$$
IS = (\{L_i, Act_i, P_i, \tau_i\}_{i \in Ag}, I, h)
$$

上式中的符号逐项解释如下：

1. `$Ag$` 是 agent 集合，论文默认包含环境 agent `$Ag_0$`。
2. `$L_i$` 是 agent `$i$` 的局部状态集合。
3. `$Act_i$` 是 agent `$i$` 的可选动作集合。
4. `$P_i : L_i \to 2^{Act_i} \setminus \{\emptyset\}$` 是 protocol function，描述某局部状态下允许哪些动作。
5. `$\tau_i$` 是 local transition function，输入当前局部状态和 joint action，返回下一局部状态。
6. `$I$` 是初始全局状态集合。
7. `$h$` 是原子命题标注关系。

论文随后定义其诱导模型：

$$
M_{IS} = (Ag, ACT, S, T, \{\sim_i\}_{i \in Ag \setminus \{Ag_0\}}, h)
$$

上式中的符号逐项解释如下：

1. `$ACT$` 是 joint actions 集合。
2. `$S$` 是从 `$I$` 可达的全局状态集合。
3. `$T \subseteq S \times ACT \times S$` 是全局转移关系。
4. `$\sim_i$` 是 agent `$i$` 的 epistemic indistinguishability relation。
5. `$h$` 继续表示原子命题标注。

agent 的知识关系由局部状态相等诱导：

$$
s \sim_i s' \iff l_i(s) = l_i(s')
$$

上式中的符号逐项解释如下：

1. `$s,s'$` 是两个全局状态。
2. `$l_i(s)$` 表示 agent `$i$` 在全局状态 `$s$` 中看到的局部状态。
3. 若两个全局状态对 agent `$i$` 来说局部观察一致，则其无法区分这两个状态。

论文给出 `ATLK` satisfaction，其中一个代表性 strategic operator 可保守写成：

$$
(M,s) \models \langle\langle \Gamma \rangle\rangle X \varphi \iff \exists a_\Gamma \in \sigma_\Gamma(s_\Gamma)\ \forall s'.\ s \xrightarrow{a} s' \Rightarrow (M,s') \models \varphi
$$

上式中的符号逐项解释如下：

1. `$\Gamma$` 是 agent group。
2. `$\sigma_\Gamma$` 是群体策略。
3. `$s_\Gamma$` 是状态 `$s$` 在群体 `$\Gamma$` 上的投影。
4. `$a_\Gamma$` 是该群体在当前观察下选取的 joint action。
5. `$a$` 表示对 `$a_\Gamma$` 的任一 completion。
6. 该公式表达“群体 `$\Gamma$` 可以保证下一步满足 `$\varphi$`”。

### 一个最小例子与通俗解释

论文用 bit transmission protocol 演示 `ISPL` 建模：

1. `Sender` 有待发送 bit 和确认状态。
2. `Receiver` 根据是否收到消息决定是否确认。
3. `Environment` 决定消息是否传达、何时交付。
4. 由此可以检查“某 agent 是否知道 bit 已被成功接收”或“某群体是否能确保最终达成确认”。

通俗地说，`MCMAS` 不是把系统看成“一个大状态机”，而是看成“多个 agent 的局部状态机同步组成的联合系统”。每个 agent 只看到自己那部分局部状态，因此“能不能知道”“能不能联合保证”都能在模型里被形式化区分出来。

### 运行 / 接受 / 转移语义

全局转移由各局部转移组合得到：

$$
(s, a, s') \in T \iff \forall i \in Ag.\ \tau_i(l_i(s), a) = l_i(s')
$$

上式中的符号逐项解释如下：

1. `$s$` 是当前全局状态。
2. `$a$` 是 joint action。
3. `$s'$` 是下一全局状态。
4. 每个 agent 都按自己的 local transition function 参与该 joint step。

群知识相关算子也由关系组合得到，例如：

$$
(M,s) \models D_\Gamma \varphi \iff \forall s'.\ s\left(\bigcap_{i \in \Gamma}\sim_i\right)s' \Rightarrow (M,s') \models \varphi
$$

上式中的符号逐项解释如下：

1. `$D_\Gamma$` 是 distributed knowledge。
2. `$\bigcap_{i \in \Gamma}\sim_i$` 表示群体共享各自信息后仍无法区分的状态关系。
3. 若在所有这些状态里 `$\varphi$` 都成立，则群体对 `$\varphi$` 具有 distributed knowledge。

common knowledge 则通过传递闭包定义：

$$
(M,s) \models C_\Gamma \varphi \iff \forall s'.\ s\left(\bigcup_{i \in \Gamma}\sim_i\right)^+ s' \Rightarrow (M,s') \models \varphi
$$

上式中的符号逐项解释如下：

1. `$C_\Gamma$` 是 common knowledge。
2. `$\left(\bigcup_{i \in \Gamma}\sim_i\right)^+$` 是“大家都知道、大家都知道大家知道……”所对应的传递闭包。

### 语义边界

1. 论文采用 observational semantics，不是 perfect recall semantics。
2. 策略主要是 memoryless、incomplete-information 风格；这保证了工程上的可计算性。
3. `ISPL` 适合显式 agent、local state、joint action 和 protocol 的系统，不适合连续动力学或大规模数值混成语义。
4. `MCMAS` 的价值重点在 symbolic model checking infrastructure，而非更丰富的建模前端体验。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| interpreted system 骨架 | `$IS = (\{L_i, Act_i, P_i, \tau_i\}_{i \in Ag}, I, h)$` | `MCMAS` 的建模核心对象。 |
| 诱导模型 | `$M_{IS} = (Ag, ACT, S, T, \{\sim_i\}, h)$` | 检查 `ATLK` 的语义载体。 |
| 知识关系 | `$s \sim_i s' \iff l_i(s)=l_i(s')$` | epistemic operators 的基础。 |
| strategic next operator | `$(M,s)\models \langle\langle \Gamma \rangle\rangle X \varphi$` | 群体是否能保证下一步性质成立。 |
| distributed knowledge | `$(M,s)\models D_\Gamma \varphi$` | 群体聚合信息后的知识能力。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 本体就是多个 agent 的局部状态组合。 |
| 事件 / 触发 | 很强 | 通过 joint action 和 protocol 显式给出。 |
| 守卫 / 数据 | 中等支持 | 主要通过 protocol/evolution 条件表达，不主打富数值约束。 |
| 层次 | 不支持 | 不是层次状态图语言。 |
| 并发 / 同步 | 很强 | 多 agent 通过 joint action 同步演化。 |
| 时间约束 | 弱支持 | 主线不是 real-time semantics。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / probabilistic line。 |
| 可执行 / 可验证性 | 很强 | `ISPL`、`OBDD`、fairness、witness/counterexample 都已工程化。 |

### 形式化问题与性质

1. `MCMAS` 的核心贡献，是把 interpreted systems 和 `ATLK` 做成可复用的 symbolic checker。
2. `ISPL` 不是通用中立标准，而是围绕 interpreted systems 量身定制的 executable modeling carrier。
3. 论文同时覆盖知识算子、群体策略和公平性，这让它在 MAS 验证平台中比纯 `CTL/LTL` 后端更有辨识度。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Agent` declarations；
2. local variables / actions / protocol / evolution sections；
3. `InitStates`、`Groups`、`Fairness`、`Formulae` 等全局段落；
4. 以 `ATLK` 编写的 temporal-epistemic-strategic properties。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `ISPL` 文本模型；
2. interpreted-system style local-state structures；
3. `OBDD`-encoded state sets 和 transition relations；
4. fairness constraints；
5. witnesses / counterexamples / strategies。

### 交换与互操作

互操作重点不在行业交换标准，而在验证链路：

1. `ISPL` 把 MAS 语义显式化为本工具可消费的模型。
2. Eclipse 插件提供编辑、语法支持和项目组织。
3. witness/counterexample 输出让其可与上层调试、协议分析流程结合。

## 配套基础设施

- 建模/编辑工具：原文说明提供 Eclipse-based `ISPL` editor。
- 解析/交换/元模型支持：`ISPL` parser、formula parser、fairness 约束与 group declarations。
- 仿真/执行支持：重点是 symbolic verification，不是 runtime execution platform。
- 验证/分析支持：`ATLK` checking、knowledge operators、uniform strategies、fairness、counterexamples 和 witnesses。
- 代码生成/转换支持：主线不是代码生成；更强调 symbolic encodings 和 state-space construction。
- 标准化或社区生态：公开源码、`ISPL` 建模语言、Eclipse 插件与 MAS verification 社群构成其生态。

## 适用场景与需求前提

### 适用场景

适合安全协议、分布式协商、投票 / 协议知识分析、多智能体协调和需要显式推理“谁知道什么、谁能保证什么”的系统。

### 需求前提

1. 系统能拆成有限个 agent 的局部状态和 joint actions。
2. 协议规则适合写成 local protocol 和 local evolution。
3. 性质关注点确实包括 knowledge、group knowledge 或 strategic ability，而不只是 plain temporal logic。
4. 团队愿意接受文本化 `ISPL` 工作流。

### 不适用或高成本场景

如果系统核心是连续物理过程、密集数值优化或纯层次状态图语法体验，`MCMAS` 就不是最自然的建模前端。

## 与相邻形式主义的关系

相对 [epmc-gets-knowledge-in-multi-agent-systems/desc.md](../epmc-gets-knowledge-in-multi-agent-systems/desc.md)，`ePMC` 是 plugin-based quantitative platform，而 `MCMAS` 是 interpreted-systems 导向的 epistemic/strategic checker；相对 [the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md](../the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md)，`mCRL2` 更偏 action-based process algebra，而 `MCMAS` 更偏 agent-local observation semantics；相对 [fdr3-a-modern-refinement-checker-for-csp/desc.md](../fdr3-a-modern-refinement-checker-for-csp/desc.md)，`FDR3` 主打 refinement，而 `MCMAS` 主打 knowledge 和 strategy reasoning。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒我们：并非所有“状态机建模”都该直接压成单一全局 `FSM`，多 agent 需求有时更适合先保留 local-state + protocol 结构。
2. `ISPL` 给出了“非形式化协作规则 -> 可验证局部协议模型”的一条稳定路径，可为后续 LLM 建模提供结构目标。
3. `knowledge / strategy / fairness` 三类性质也为 `project_2` 和 `project_3` 的性质生成、验证 profile 设计提供了可借鉴语义层。

### 作为目标形式主义还是中间表示

更像偏验证侧的目标形式主义与工具载体，不是面向一般控制软件的一线状态机前端。

### 对需求到模型生成的启发

1. 若需求天然按角色分配，就应优先抽取 agent、局部观测、局部动作和协议约束。
2. 需求文本中的“知道”“看见”“通知后再决定”等说法，不应被粗暴压扁成普通 guard。
3. 多主体协作需求若后续要验证 knowledge 或 strategic ability，建模阶段必须保留 local-state granularity。

### 现实限制

`MCMAS` 很强于 epistemic / strategic reasoning，但不直接覆盖 timed / hybrid 控制状态机主线，因此它更适合作为分布式交互与 MAS 侧证，而非统一终点形式主义。

## 重要的相关工作

1. [epmc-gets-knowledge-in-multi-agent-systems/desc.md](../epmc-gets-knowledge-in-multi-agent-systems/desc.md)：概率模型检查平台中对知识算子的扩展条目。
2. [the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md](../the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md)：并发系统另一条 action-based verification platform 路线。
3. [fdr3-a-modern-refinement-checker-for-csp/desc.md](../fdr3-a-modern-refinement-checker-for-csp/desc.md)：process algebra 方向的现代 refinement-checking 基础设施。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`Interpreted Systems / ISPL / ATLK / MCMAS`
- 归类理由：主贡献是把 interpreted systems、`ISPL` 和 `ATLK` 做成一套成熟的 MAS symbolic verification infrastructure，而不是提出新的状态机本体。
