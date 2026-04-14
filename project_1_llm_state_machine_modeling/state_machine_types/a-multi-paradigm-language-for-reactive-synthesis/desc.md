# 面向反应式综合的多范式语言 / A Multi-paradigm Language for Reactive Synthesis

## 基本信息

- 标题：A Multi-paradigm Language for Reactive Synthesis
- 中文标题：面向反应式综合的多范式语言
- 作者：Ioannis Filippidis，Richard M. Murray，Gerard J. Holzmann
- 发表：*Electronic Proceedings in Theoretical Computer Science*，202:73-97，2016
- DOI：`10.4204/EPTCS.202.6`
- 链接：https://doi.org/10.4204/EPTCS.202.6
- 形式主义：`PROMELA-like reactive synthesis language / GR(1) / Slugs translation`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：reactive-synthesis front-end language integrating imperative processes, declarative constraints, and game semantics
- 工具/实现获取方式：原文明确说明实现以 `Python` 编写，并把该语言翻译为 `Slugs` synthesis input。
- 标准/格式获取方式：核心承载是基于 `PROMELA` 语法的 multiparadigm specification language、`env/sys/free` 变量声明、assumption/assertion 进程与 `Slugs` 后端输入；不是行业标准。

## 简报

这篇论文补的不是新的求解器，而是 reactive synthesis 最稀缺的一层：真正给人写规格的前端语言。作者的出发点很明确，单纯把所有需求都塞进 `LTL` 会导致公式冗长、顺序结构难写、已有组件模型也难复用，因此他们设计了一种混合 imperative 和 declarative 的语言，让 graph-like constraints、控制流和 `GR(1)` 目标能写在同一份 synthesis specification 中。

- 形式主义定位：面向 reactive synthesis 的输入语言与翻译基础设施，而不是新的自动机母型。
- 构造方式简述：用 `PROMELA` 风格语法描述 process / control flow，再用 `GR(1)` + past LTL 描述 assumptions / guarantees，最后翻译成 `Slugs` 可解输入。
- 基础设施与场景简述：依托 `Python` 编译器、`Slugs` 后端、`BDD` reordering 与 game semantics，服务协议、硬件接口、机器人和一般 open reactive systems。

```text
mixed imperative/declarative spec -> two-player game semantics -> GR(1) / past-LTL encoding -> Slugs synthesizer
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `PROMELA` 风格的 process / guarded commands。
2. 环境与系统两方玩家控制的变量集。
3. imperative 与 declarative 两类变量语义。
4. assumption / assertion 进程。
5. `GR(1)` synthesis problem 与 `Slugs` 翻译。

### 核心抽象

论文首先把问题定义为 open system synthesis。令 `$X$` 为环境变量集，`$Y$` 为系统变量集，则其核心 `GR(1)` 规格写成：

$$
\left(
\theta_e \land \Box \rho_e \land \bigwedge_{i=1}^{n} \Box \Diamond \psi^e_i
\right)
\mathbin{\mathrm{sr}\to}
\left(
\theta_s \land \Box \rho_s \land \bigwedge_{j=1}^{m} \Box \Diamond \psi^s_j
\right)
$$

上式中的符号逐项解释如下：

1. `$\theta_e$` 是环境初始条件。
2. `$\rho_e$` 是环境安全约束。
3. `$\psi^e_i$` 是环境 recurrence assumptions。
4. `$\theta_s$`、`$\rho_s$`、`$\psi^s_j$` 分别是系统的初始、安全和 recurrence assertions。
5. `$\mathrm{sr}\to` 表示论文采用的 strict realizability implication。

论文还区分 imperative 与 declarative 变量。可把全部变量写成：

$$
V = V_{free} \cup V_{imp}, \qquad V_{free} \cap V_{imp} = \emptyset
$$

上式中的符号逐项解释如下：

1. `$V_{free}$` 是用 `free` 关键字声明的 declarative variables，除非被约束，否则可自由变化。
2. `$V_{imp}$` 是 imperative variables，除非被显式赋值，否则保持原值。
3. 这种划分正是论文所谓“整合 imperative 和 declarative 两种范式”的关键。

论文把 process 解析成 program graph，并进一步解释为 turn-based game。一个 process 可以保守写成：

$$
Pr = (V_r, E_r, r)
$$

上式中的符号逐项解释如下：

1. `$V_r$` 是程序图节点集合。
2. `$E_r$` 是带语句标签的有向边集合。
3. `$r$` 是 root。
4. 程序计数器 `pcr` 决定当前控制流位置。

对应的诊断 / 求解对象则是交替博弈图。论文对玩家回合语义的解释可保守整理为：

$$
G = (S_0, S_1, T, Win)
$$

上式中的符号逐项解释如下：

1. `$S_0$` 是玩家 0 的位置集合。
2. `$S_1$` 是玩家 1 的位置集合。
3. `$T$` 是回合交替的转移关系。
4. `$Win$` 是由 `GR(1)` 公式定义的获胜条件。

### 一个最小例子与通俗解释

论文给了一个很适合直觉理解的 Bunny/Fox 追逐游戏：

1. 狐狸和兔子轮流移动。
2. 环境控制狐狸位置，系统控制兔子位置。
3. 兔子必须到达胡萝卜，同时避免经过狐狸所在格子。
4. 这种问题若纯写成逻辑公式会很绕；用进程语法写控制流和棋盘图，再用 `GR(1)` 写最终目标，就顺手得多。

通俗地说，这门语言像“给 reactive synthesis 加了程序骨架”。有些约束适合写成时序逻辑，有些适合写成进程和 guarded commands，作者做的就是把两者接到一个统一的游戏语义里。

### 运行 / 接受 / 转移语义

对 open system，执行由两方轮流赋值形成。若采用 Mealy game 语义，则每一轮可保守写成：

$$
(x_t, y_t) \xrightarrow{\text{env}} x_{t+1}
\xrightarrow{\text{sys}} y_{t+1}
$$

上式中的符号逐项解释如下：

1. `$x_t$` 是环境变量当前值。
2. `$y_t$` 是系统变量当前值。
3. 环境先选择下一步输入 `$x_{t+1}$`。
4. 系统在看见该输入后选择 `$y_{t+1}$`。

论文还说明了 assumption / assertion 进程与控制流、数据流的关系。若某个 process 的程序计数器由环境控制，而数据流约束系统变量，则：

$$
\text{env controls } pcr,\quad \text{sys satisfies selected statement}
$$

这意味着 process 本身就能表示一个小型 game，而不只是普通 transition system。

### 语义边界

1. 语言最终还是要翻译到 `GR(1)` / `Slugs` 后端，因此表达力受该后端 tractability 约束。
2. 它是 centralized synthesis with full information，不是分布式不完全信息综合。
3. 支持 imperative / declarative 混合，但不意味着支持任意 general-purpose programming feature。
4. 重点是前端可写性和可维护性，而不是重新发明新的求解算法。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `GR(1)` strict-realizability 骨架 | `$(\theta_e \land \Box \rho_e \land \bigwedge \Box \Diamond \psi^e) \mathbin{\mathrm{sr}\to} (\theta_s \land \Box \rho_s \land \bigwedge \Box \Diamond \psi^s)$` | 语言最终要落回可综合的游戏规格。 |
| imperative / declarative 划分 | `$V = V_{free} \cup V_{imp}$` | 允许两种语义在同一语言中共存。 |
| process graph | `$Pr = (V_r, E_r, r)$` | `PROMELA` 风格进程的核心结构。 |
| game graph | `$G = (S_0, S_1, T, Win)$` | 语言语义最终解释为 turn-based infinite game。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 进程图、程序计数器和 guarded commands 直接表达状态结构。 |
| 事件 / 触发 | 很强 | 选择、迭代、`goto`、可执行语句和玩家轮次共同驱动行为。 |
| 守卫 / 数据 | 很强 | 既支持布尔 / bitfield / ranged integer，也支持 declarative / imperative 混合数据语义。 |
| 层次 | 弱支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 支持多个 process，但主线仍是 centralized turn-based synthesis。 |
| 时间约束 | 弱支持 | 有时序逻辑和 past LTL，但没有显式 clocks。 |
| 连续动态 / 随机性 | 不支持 | 语言层不直接处理连续动力学。 |
| 可执行 / 可验证性 | 很强 | 可翻译到 `Slugs`，并由 game solver 求 realizability / strategy。 |

### 形式化问题与性质

1. 论文的核心创新是“给 synthesis 提供一个比裸 `LTL` 更结构化的输入层”。
2. imperative graph constraints 和 declarative temporal properties 可以按最自然的方式分别书写，而不是强迫全部公式化。
3. 对教育和工程实践而言，它显著降低了从程序语言思维切换到 synthesis 逻辑思维的门槛。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. `PROMELA` 风格 process / guarded commands。
2. `env` / `sys` / `free` 声明。
3. assumption / assertion 进程。
4. `GR(1)` 与 past-LTL 公式块。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 解析后的 program graph。
2. game-semantics intermediate representation。
3. `Slugs` backend input。
4. `BDD` variable reordering 所需的 bitfield / ranged integer 编码。

### 交换与互操作

1. 语言实现以 `Python` 编写，并明确翻译到 `Slugs`。
2. 整数范围通过 bitfield 编码进入 `BDD` 后端。
3. 语言既能表达 partial model，也能表达 assumptions / guarantees。
4. 其目标是 synthesis-exchange 层，而不是通用运行时序列化标准。

## 配套基础设施

- 建模/编辑工具：正文重点在语言与翻译器，本身未强调大型 IDE；实现为 `Python` translator。
- 解析/交换/元模型支持：`PROMELA`-like parser、program graph、game translation、`Slugs` bridge。
- 仿真/执行支持：论文重点不是运行时执行器，而是 synthesis input 层。
- 验证/分析支持：可由 `Slugs` 进行 realizability 与 strategy computation。
- 代码生成/转换支持：从 multiparadigm source 到 `Slugs` synthesis input 的自动翻译。
- 标准化或社区生态：与 `Slugs`、`PROMELA`、`BDD`-based synthesis 生态紧耦合。

## 适用场景与需求前提

### 适用场景

适合 reactive synthesis、协议与硬件控制器综合、带 graph constraints 的机器人任务、以及需要把已有部分模型和时序目标写在同一份规格中的开放系统。

### 需求前提

1. 问题需可表达为 centralized two-player game with full information。
2. 目标性质最好可落到 `GR(1)` / past-LTL 可处理片段。
3. 使用者愿意区分环境和系统变量所有权。
4. 若使用 ranged integers / bitfields，需要接受 `BDD`-driven symbolic backend 的建模约束。

### 不适用或高成本场景

1. 若需求本质上超出 `GR(1)` 片段，翻译后仍可能不可解或代价很高。
2. 若需要 dense-time 或连续动力学，语言层本身并不提供支持。
3. 若系统是分布式不完全信息综合，本文假设不足以覆盖。

## 与相邻形式主义的关系

相对 [spectra-a-specification-language-for-reactive-systems/desc.md](../spectra-a-specification-language-for-reactive-systems/desc.md)，`Spectra` 更像高层 reactive-spec DSL，而本文更强调 `PROMELA` 风格 control flow 与 partial model；相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 是后端综合器，这篇论文补的是其前端语言层；相对 [tulip-a-software-toolbox-for-receding-horizon-temporal-logic-planning/desc.md](../tulip-a-software-toolbox-for-receding-horizon-temporal-logic-planning/desc.md) 与 [ltlmop-experimenting-with-language-temporal-logic-and-robot-control/desc.md](../ltlmop-experimenting-with-language-temporal-logic-and-robot-control/desc.md)，这篇更偏 synthesis language infrastructure，而不是 planning / execution toolkit。

## 与本研究的关系

### 对 Project 1 的价值

1. 它非常接近“LLM 输出什么样的结构化语言最适合接后端综合器”这个核心问题。
2. imperative / declarative 混合的做法，对需求中“过程约束”和“时序目标”并存的场景尤其重要。
3. 如果未来要从需求文本自动生成 synthesis spec，这类语言比裸 `LTL` 更友好，也更利于修复。

### 作为目标形式主义还是中间表示

更适合作为 synthesis 前端中间表示，而不是最终交付给人类工程师长期维护的通用状态机标准。

### 对需求到模型生成的启发

1. 不同类型约束不必都映射到同一种语法层；图结构与时序目标应分层表达。
2. `env/sys/free` 这种所有权和更新语义标签，对自动生成规格尤其关键。
3. 若后端固定为 `GR(1)`，前端语言设计应主动帮助用户避开不可综合的表达习惯。

### 现实限制

它主要解决输入层可写性问题，不替代后端求解难度；复杂规格仍会在 `BDD` 和 `GR(1)` tractability 上遇到瓶颈。

## 重要的相关工作

1. `PROMELA`：提供其 imperative syntax 母线。
2. `Slugs`：本文实现所对接的 synthesis backend。
3. `GR(1)` 与 parity-game synthesis：提供其可解性基础。
4. `Spectra`、`TLSF` 等后续 synthesis 输入层工作，可视作同方向的相邻发展线。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`PROMELA-like reactive synthesis language / GR(1) / Slugs translation`
- 论文角色：reactive-synthesis front-end language integrating imperative and declarative constraints
- 核心功能：把 process / guarded commands / assumptions / guarantees 统一到可翻译的 synthesis 输入语言中
- 关键特性：`env/sys/free`、program graph、game semantics、past LTL、`Slugs` translation、bitfield / ranged integer encoding
