# 通过广义状态合并扩展 AALpy 的被动学习能力 / Extending AALpy with Passive Learning: A Generalized State-Merging Approach

## 基本信息

- 标题：Extending AALpy with Passive Learning: A Generalized State-Merging Approach
- 中文标题：通过广义状态合并扩展 AALpy 的被动学习能力
- 作者：Benjamin von Berg, Bernhard K. Aichernig
- 发表：*Computer Aided Verification*, pp. 127-140, 2025
- DOI：`10.1007/978-3-031-98685-7_6`
- 链接：https://doi.org/10.1007/978-3-031-98685-7_6
- 形式主义：`AALpy / passive automata learning / generalized state-merging`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 论文角色：`AALpy` 被动学习与状态合并基础设施扩展
- 工具/实现获取方式：论文明确说明扩展直接并入开源 `AALpy`，并给出 GitHub 入口 `https://github.com/DES-Lab/AALpy`。
- 标准/格式获取方式：主承载是 `Python` API、`AALpy` 的通用内部自动机表示、prefix tree acceptor 与 `GeneralizedStateMerging` 配置接口；不是行业交换标准。

## 简报

这篇论文补的是 `AALpy` 从主动学习框架走向“主动 + 被动”统一基础设施的关键一步。作者不是只在库里硬塞几个 state-merging 算法，而是先抽出一个能覆盖多类 `IO` 自动机的通用内部表示，再把 red-blue framework 做成可配置骨架，使新算法的实现工作主要缩减成“定义兼容条件和评分函数”。

- 形式主义定位：自动机学习基础设施扩展，而不是新的自动机母型。
- 构造方式简述：`training data -> prefix tree / IO frequency automaton -> red-blue state merging -> extracted automaton`。
- 基础设施与场景简述：依托 `Python`、`AALpy`、通用 `IO automaton` 表示、`GeneralizedStateMerging` API 和多种兼容/评分策略，适合日志驱动模型推断与被动学习算法开发。

```text
logs / traces -> common IO automaton representation -> configurable red-blue merging -> learned automaton
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `AALpy` 现有主动学习基础设施。
2. 支持不同自动机类型的统一 `IO automaton` / `IO frequency automaton` 内部表示。
3. `red-blue` state-merging framework。
4. 兼容性检查、评分函数和 `GeneralizedStateMerging` API。

### 核心抽象

论文给出的基本 `IO automaton` 定义是：

$$
M = \langle Q, q_0, I, O, T \rangle
$$

上式中的符号逐项解释如下：

1. `$Q$` 是状态集合。
2. `$q_0$` 是唯一初始状态。
3. `$I$` 是输入符号集合。
4. `$O$` 是输出符号集合。
5. `$T \subseteq Q \times I \times O \times Q$` 是转移集合。

这一定义对应“带 `IO` 行为的自动机”统一骨架，可覆盖 deterministic、observably nondeterministic、Moore-style 等多类对象。

论文进一步定义带频次的内部表示：

$$
M_f = \langle Q, q_0, I, O, \delta, \nu \rangle
$$

上式中的符号逐项解释如下：

1. `$\delta$` 是 observably nondeterministic `IO automaton` 的转移函数视角。
2. `$\nu : Q \times I \times O \to \mathbb{N}$` 是频次函数。
3. `$\nu(q,i,o)=n$` 表示从状态 `$q$` 看到输入 `$i$` 并产生输出 `$o$` 的观测次数为 `$n$`。
4. 这就是论文所谓 `IO frequency automaton`，也是多类被动学习算法共享的内部载体。

red-blue state merging 的骨架可保守写成：

$$
(R,B,H_0) \Rightarrow H_1 \Rightarrow \cdots \Rightarrow H_k
$$

上式中的符号逐项解释如下：

1. `$H_0$` 是由日志构建出的 prefix tree acceptor 或频次自动机。
2. `$R$` 是当前 red states 集合。
3. `$B$` 是当前 blue frontier。
4. 每一步要么把某个 blue state 提升为 red，要么把某个 blue-red 对做 merge。
5. `$H_k$` 是最终学习出的自动机。

这条骨架在库层被封装成 `GeneralizedStateMerging`。其接口目标可以压成：

$$
\mathrm{GSM}(data,\ compat,\ score,\ constraints) \to \widehat{M}
$$

上式中的符号逐项解释如下：

1. `$data$` 是被动学习所用日志或样本。
2. `$compat$` 是兼容性判定。
3. `$score$` 是候选 merge 的评分函数。
4. `$constraints$` 表示额外结构约束，例如 deterministic / Moore 等。
5. `$\widehat{M}$` 是学习得到的假设自动机。

### 一个最小例子与通俗解释

最小例子可以按论文的 red-blue 直觉理解：

1. 先用训练日志构建一棵前缀树。
2. 根状态先标成 red，孩子状态作为 blue frontier。
3. 每次挑一个 blue 状态，看它能不能和某个 red 状态合并。
4. 如果不兼容，就把它升级成新的 red；如果兼容，就按评分函数选择最优 merge。

通俗地说，这像是在“把日志里过于细碎的行为树慢慢压缩成状态机”。论文真正做的不是某一个合并准则，而是把这个压缩过程本身做成通用、可复用的框架。

### 运行 / 接受 / 转移语义

论文的基础设施链可保守写成：

$$
data \xrightarrow{\mathrm{PTA/IOFA}} H_0 \xrightarrow{\mathrm{merge}} \widehat{M} \xrightarrow{\mathrm{export/use}} downstream
$$

上式中的符号逐项解释如下：

1. `$data$` 是训练日志。
2. `$H_0$` 是初始 prefix tree acceptor 或 `IOFA`。
3. `$\widehat{M}$` 是最终学习结果。
4. `downstream` 表示后续测试、验证或进一步学习工作流。

论文强调 `AALpy` 的目标不是把 passive learning 单独做成新包，而是让它和现有 active learning 生态共用自动机类型、输出对象和工程接口。

### 语义边界

1. 这篇论文不是被动学习理论综述，而是 `AALpy` 的工程化基础设施扩展。
2. 它主打的是 `IO` 行为自动机，而不是任意富数据或连续系统学习。
3. 能否学出好模型仍高度依赖日志质量、兼容性准则和结构先验。
4. 论文强调“易于实现新算法”，不等于所有任务都自动优于主动学习。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 统一 `IO` 自动机骨架 | `$M=\langle Q,q_0,I,O,T\rangle$` | 多类被动学习对象共享的最小内部表示。 |
| 频次自动机 | `$M_f=\langle Q,q_0,I,O,\delta,\nu\rangle$` | 用频次支撑 probabilistic / scoring-aware merging。 |
| red-blue 演化 | `$(R,B,H_0)\Rightarrow H_k$` | state-merging 的核心工作流。 |
| API 目标 | `$\mathrm{GSM}(data,\ compat,\ score,\ constraints)\to\widehat{M}$` | `GeneralizedStateMerging` 把算法变化压缩到少数可配置点。 |
| 工程收益 | “few lines of code” | 现有算法可用极少附加代码接入 `AALpy`。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 基础对象就是多类有限状态自动机。 |
| 事件 / 触发 | 很强 | 输入/输出交互是 `IO automaton` 定义核心。 |
| 守卫 / 数据 | 弱到中等支持 | 主体不是富守卫 DSL，但可通过 automaton type / constraints 承载有限结构差异。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 间接支持 | 可学习交互行为，但不是显式并发语义建模工具。 |
| 时间约束 | 不支持 | 论文主线不在 timed learning。 |
| 连续动态 / 随机性 | 支持概率频次，不支持连续动态 | `IOFA` 与 scoring 支持概率型观测；连续系统不在范围内。 |
| 可执行 / 可验证性 | 很强 | 直接并入 `AALpy`、`Python` API 清晰、可复现实验和快速原型实现。 |

### 形式化问题与性质

1. 论文真正补的是“被动学习算法怎样在同一库里复用工程骨架”。
2. 它把 automaton type 的差异尽量推迟到 `compatibility + scoring + constraints` 这几个可配置接口。
3. 这对文库中的学习类条目非常重要，因为它说明 `AALpy` 已不仅是主动学习工具，而是更广义的 automata-learning 平台。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 训练日志或 traces。
2. `AALpy` 中定义的 automaton type。
3. `GeneralizedStateMerging` 的配置参数。
4. 兼容性、评分和结构约束函数。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Python` API。
2. prefix tree acceptor / `IO frequency automaton`。
3. `GeneralizedStateMerging` 类。
4. 学习结果自动机对象。

### 交换与互操作

论文的互操作重点在库内统一表示：

1. 不同被动学习算法共享同一内部自动机表示。
2. 与现有 `AALpy` 主动学习对象保持兼容。
3. 输出模型可直接进入 `AALpy` 的既有分析和下游工作流。

## 配套基础设施

- 建模/编辑工具：不是图形建模器，而是 `Python` 库与示例脚本。
- 解析/交换/元模型支持：统一 `IO automaton / IOFA` 内部表示与状态合并 API。
- 仿真/执行支持：学习后的模型可直接在 `AALpy` 生态中执行和分析。
- 验证/分析支持：passive learning、state merging、兼容性检查和评分驱动 merge。
- 代码生成/转换支持：重点是日志到模型的推断，不是部署代码生成。
- 标准化或社区生态：开源 `AALpy`、GitHub、`Python` 和 automata-learning 社区构成其生态。

## 适用场景与需求前提

### 适用场景

适合接口协议推断、日志驱动行为建模、被动学习算法快速原型实现，以及需要在 `AALpy` 内统一比较多种 state-merging 方法的场景。

### 需求前提

1. 系统行为能被记录成输入/输出日志。
2. 目标模型更接近有限状态 `IO` 自动机而不是连续动力学。
3. 用户能够给出合理的 automaton type、兼容条件和评分逻辑。
4. 若要得到更好泛化效果，训练数据需覆盖关键交互模式。

### 不适用或高成本场景

如果对象是富数据 `RA/EFSM`、dense-time 系统或连续控制器，仅靠本文通用 state-merging 基础设施通常还不够。

## 与相邻形式主义的关系

相对 [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)，这篇不是重新介绍 `AALpy` 主库，而是把它扩展到被动学习和状态合并；相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md) 与 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，`LearnLib` 更偏主动学习 Java 生态，而本文强调 `Python` 下主动/被动统一基础设施；相对 [active-learning-for-extended-finite-state-machines/desc.md](../active-learning-for-extended-finite-state-machines/desc.md)，后者讲特定学习方法，本篇讲可复用平台骨架。

## 与本研究的关系

### 对 Project 1 的价值

1. 它为“从已有系统日志或交互行为反推状态机”提供了成熟基础设施锚点。
2. 对后续模型修复很有用，因为 LLM 生成模型可以拿实际日志再做被动对齐。
3. 它还说明自动建模不应只看“从需求生成”，也要看“从行为学习补模”。

### 作为目标形式主义还是中间表示

它是学习与对齐工作流的基础设施，不是最终要交付的状态机标准。

### 对需求到模型生成的启发

1. 若需求文本不够完备，行为日志可作为补充证据进入模型闭环。
2. 自动生成出的状态机可以通过 passive learning 结果做结构对照与修补。
3. 若想把这条路线自动化，日志采集和输入/输出字母表定义必须提前设计。

### 现实限制

它主要解决有限状态 `IO` 行为的被动学习基础设施问题，对 richer formalisms 仍需额外抽象层。

## 重要的相关工作

### 奠基或前身工作

- [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)：`AALpy` 主库与主动学习基础设施。
- red-blue state merging 传统路线，如 `RPNI`、`EDSM`、`IOAlergia`。

### 同类型或同家族工作

- [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：另一条主流学习框架生态。
- [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)：更晚的 active learning 框架盘点。

### 标准 / 格式 / 工具链工作

- `AALpy` GitHub 和 `Python` API。
- `GeneralizedStateMerging` 作为本论文新增的核心基础设施接口。

### 与本研究关系最紧的工作

- 在 LLM 自动建模闭环里，行为日志如何转成可比较的状态机，这篇给出了一条可直接落地的基础设施入口。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 形式主义：`AALpy / passive automata learning / generalized state-merging`
- 论文角色：`AALpy` 被动学习与状态合并基础设施扩展
- 核心功能：把 red-blue passive learning 和 generalized state merging 统一进 `AALpy` 可复用库接口。
- 关键特性：统一 `IO automaton / IOFA` 内部表示、`GeneralizedStateMerging`、兼容性与评分可配置、主动/被动学习共存。
- 构造方式：`logs -> PTA/IOFA -> generalized state merging -> learned automaton`。
- 基础设施：`AALpy`、`Python`、GitHub、通用自动机表示和状态合并 API。
- 适用场景：日志驱动行为建模、协议推断和被动学习算法开发。
- 需求前提：对象需近似有限状态 `IO` 行为，且能提供可用日志与输入/输出字母表。
- 状态：🟢 直接可用
