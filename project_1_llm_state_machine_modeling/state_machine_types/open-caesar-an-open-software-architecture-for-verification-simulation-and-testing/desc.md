# OPEN/CÆSAR：面向验证、仿真与测试的开放式软件架构 / OPEN/CÆSAR: An Open Software Architecture for Verification, Simulation, and Testing

## 基本信息

- 标题：OPEN/CÆSAR: An Open Software Architecture for Verification, Simulation, and Testing
- 中文标题：OPEN/CÆSAR：面向验证、仿真与测试的开放式软件架构
- 作者：Hubert Garavel
- 发表：*INRIA Research Report RR-3352*，18 pages，1998
- DOI：原文未提供
- 链接：https://cadp.inria.fr/ftp/publications/cadp/Garavel-98.pdf
- 形式主义：`Open/Caesar / caesargraph.h / implicit LTS exploration`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：language-independent implicit-`LTS` API / verification-simulation-testing architecture
- 工具/实现获取方式：原文明确说明 `Open/Caesar` 作为 `CADP` 工具箱的一部分可免费获取，并给出 `CADP` 官方入口；当前 `paper.pdf` 即来自 `CADP` 官方站点。
- 标准/格式获取方式：核心承载对象是 `caesargraph.h` 图模块接口、state/label primitives、successor callback、`BCG` 等 `CADP` 生态格式；它是工具接口与运行时约定，不是中立交换标准。

## 简报

这篇论文补的是 `CADP` 生态真正的底座接口，而不是某个单点验证算法。`Open/Caesar` 的关键价值在于，把“语言相关的状态生成”与“语言无关的探索、仿真、验证、测试工具”明确拆开。只要某个前端语言能导出统一的 state/label 表示，并实现初始状态与 successor enumeration 接口，后面的 random execution、interactive simulation、on-the-fly verification、test generation 都可以复用。

- 形式主义定位：并发系统的隐式 `LTS` 探索接口与工具架构，而不是新的状态机母型。
- 构造方式简述：前端编译器负责生成 graph module，暴露 `caesargraph.h` 约定的状态、标签和后继枚举；library module 提供表、栈、transition-list 等通用数据结构；exploration module 只依赖统一 API 做分析。
- 基础设施与场景简述：依托 `CADP`、`BCG`、`Open/Caesar` graph/library/exploration 三层与 callback-based successor enumeration，服务多语言并发规格验证、仿真、诊断和测试生成。

```text
source language compiler -> graph module (states / labels / successors) -> Open/Caesar libraries -> simulator / verifier / tester
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. language-dependent graph module；
2. language-independent library module；
3. exploration module；
4. implicit labelled transition system；
5. `caesargraph.h` 统一接口。

### 核心抽象

从体系结构上，`Open/Caesar` 可以保守整理为：

$$
OC = (G, L, E)
$$

上式中的符号逐项解释如下：

1. `G` 是 graph module，负责封装语言相关的状态与转移生成。
2. `L` 是 library module，提供 transition lists、hash tables、stacks、bitmaps 等通用设施。
3. `E` 是 exploration module，负责 simulation、verification、testing 等具体分析流程。
4. 论文的重点正是通过清晰 API 把这三层解耦。

在语义层，graph module 暴露的是一个隐式 `LTS`：

$$
\mathcal G = (S, s_0, \Lambda, \rightarrow)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `s_0` 是初始状态。
3. `\Lambda` 是标签集合。
4. `\rightarrow \subseteq S \times \Lambda \times S` 是转移关系。
5. `Open/Caesar` 不要求一次性显式构造整张图，而是按需枚举 `\mathcal G` 的局部后继。

### 一个最小例子与通俗解释

最小直觉例子可以理解成：

1. 某个 `LOTOS` 或 `SDL` 编译器接收源模型。
2. 它不必直接生成整张可达图，而是只需要回答“初始状态是什么”和“这个状态的后继有哪些”。
3. `Executor` 可以据此随机走 trace，`Simulator` 可以逐步回放，`Evaluator` 可以在同一接口上做按需检查。
4. 因而 `Open/Caesar` 更像一块“验证插座板”，不同语言只要插头一致，就能共用后端工具。

通俗地说，`Open/Caesar` 不是在发明另一种并发模型，而是在发明“怎样把各种并发模型接到同一套验证工具上”的接口层。

### 运行 / 接受 / 转移语义

论文明确要求 graph module 至少提供初始状态函数：

$$
\mathrm{Init}() = s_0
$$

上式中的符号逐项解释如下：

1. `Init` 是 graph module 暴露的初始状态原语。
2. `s_0` 是待探索系统的初始配置。
3. exploration module 总是从它开始工作。

对某个状态 `s` 的后继，论文采用 callback 风格的枚举语义。可保守写成：

$$
\mathrm{Succ}(s) = \{ (\lambda, s') \mid s \xrightarrow{\lambda} s' \}
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态。
2. `\lambda` 是当前一步的标签。
3. `s'` 是后继状态。
4. graph module 的 successor enumeration function 会按某个编译器决定的顺序，把 `\mathrm{Succ}(s)` 中的元素逐个回调给 exploration module。

### 语义边界

1. `Open/Caesar` 本身不定义新的控制语义；它依赖前端语言给出状态与标签的真正含义。
2. 它的核心对象是 action-based implicit `LTS`，不擅长直接承载连续动力学或复杂数值优化。
3. 论文强调的是接口与工程解耦，而不是新的模型检查理论。
4. 它默认前端能够把状态向量和标签整理成可由 `C` 接口操纵的对象。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 三层架构 | `$OC = (G, L, E)$` | 语言相关生成、通用数据结构与探索算法彼此解耦。 |
| 隐式状态图 | `$\mathcal G = (S, s_0, \Lambda, \rightarrow)$` | 所有后端最终只依赖统一的状态-标签-转移语义。 |
| 初始接口 | `$\mathrm{Init}() = s_0$` | graph module 必须提供初始状态。 |
| 后继枚举 | `$\mathrm{Succ}(s) = \{ (\lambda, s') \mid s \xrightarrow{\lambda} s' \}$` | exploration module 通过 callback 获得当前状态的全部出边。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 整个接口都围绕 implicit state graph 展开。 |
| 事件 / 触发 | 很强 | 标签与转移是统一 API 的核心对象。 |
| 守卫 / 数据 | 弱支持 | 只通过前端状态向量间接暴露，不在接口层直接建模。 |
| 层次 | 不支持 | 不是层次状态图语言本体。 |
| 并发 / 同步 | 很强 | 面向协议、进程代数和并发系统工具共享。 |
| 时间约束 | 不支持 | 本文主体尚未把 quantitative time 纳入接口。 |
| 连续动态 / 随机性 | 不支持 | 不是 hybrid / stochastic 建模框架。 |
| 可执行 / 可验证性 | 很强 | random execution、simulation、verification、test generation 都是目标功能。 |

### 形式化问题与性质

1. 它真正解决的是“如何让不同语言共用同一套验证后端”。
2. callback-based successor enumeration 避免强制前端预生成整个状态图。
3. library module 说明在验证工具里，数据结构复用本身就是关键基础设施。

## 构造方式与承载格式

### 建模入口

原文中的建模入口是：

1. `LOTOS`、`SDL`、automata network、`BCG` 等前端形式；
2. 这些前端各自编译成符合 `caesargraph.h` 的 graph module；
3. exploration module 再对统一接口执行仿真、验证或测试。

### 机器可处理承载方式

机器可处理承载方式包括：

1. states / labels 的 `C` 级表示；
2. successor enumeration callbacks；
3. transition lists、tables、stacks、bitmaps 等内部 library structures；
4. `BCG` 等 `CADP` 生态格式。

### 交换与互操作

这篇论文的互操作重点在：

1. 不同前端语言共享同一 graph API；
2. 多个探索工具共享同一组 library data structures；
3. `CADP` 中的 simulation、verification、testing 工具都可直接复用已有 graph modules。

## 配套基础设施

- 建模/编辑工具：依托各前端语言自己的编译器与 `CADP` 生态。
- 解析/交换/元模型支持：`caesargraph.h`、states/labels primitives、`BCG` 等统一接口与格式。
- 仿真/执行支持：`Executor`、`Simulator`、`Xsimulator`。
- 验证/分析支持：`Terminator`、`Exhibitor`、`Evaluator`、`Projector` 等。
- 代码生成/转换支持：重点不是部署代码生成，而是 graph module 生成与工具复用。
- 标准化或社区生态：属于 `CADP` 的核心基础设施；原文未给独立标准组织。

## 适用场景与需求前提

### 适用场景

适合多语言并发规格、协议与分布式系统的统一验证平台建设，尤其适合想复用同一套隐式 `LTS` 后端工具的场景。

### 需求前提

1. 前端语言必须能够暴露有限或可枚举的状态向量与标签。
2. 系统语义最好可落成 action-based `LTS`。
3. 重点问题是探索、仿真、验证或测试，而不是数值优化或连续控制。
4. 团队愿意为每种前端实现统一 graph interface。

### 不适用或高成本场景

如果模型核心是连续动力学、复杂时钟算术或重数据求解，`Open/Caesar` 本身并不是直接的目标形式主义。

## 与相邻形式主义的关系

相对 [exp-open-20-a-flexible-tool-integrating-partial-order-compositional-and-on-the-fly-verification-methods/desc.md](../exp-open-20-a-flexible-tool-integrating-partial-order-compositional-and-on-the-fly-verification-methods/desc.md)，本文更底层，讲的是 `Open/Caesar` API 本身，而不是 concurrency front-end；相对 [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)，本文是更早的基础设施母线；相对 [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)，后者复用了 `Open/Caesar` / explorer 接口做测试，而本文解释的是被复用的底座。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明多种状态机/进程前端完全可以先统一到一层隐式图接口，再复用验证后端。
2. 对 `project_1` 而言，这比“为每种输出状态机各做一套专用验证桥”更有工程可维护性。
3. 它也提示：需求到模型闭环里，运行时接口和模型检查接口应当尽量统一。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Open/Caesar` 更像中间接口层与验证基础设施，而不是最终面向需求工程师的目标状态机语言。

### 对需求到模型生成的启发

1. 可以把“模型语义暴露接口”视为一等产物，而不只是附属实现细节。
2. 若未来支持多语言状态机输出，统一 successor-enumeration API 会比统一语法更现实。
3. graph module / exploration module 的分层思想适合迁移到“LLM 生成前端 + 统一验证后端”的闭环架构。

## 重要的相关工作

- [exp-open-20-a-flexible-tool-integrating-partial-order-compositional-and-on-the-fly-verification-methods/desc.md](../exp-open-20-a-flexible-tool-integrating-partial-order-compositional-and-on-the-fly-verification-methods/desc.md)：建立在 `Open/Caesar` 之上的并发组合前端。
- [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)：后续更完整的 `CADP` 工具箱总览。
- [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)：使用 explorer / `LTS` 接口进行在线测试生成的代表条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 结论：这是一篇典型的 language-independent verification infrastructure 条目，适合作为 `CADP/Open-Caesar` 母线、implicit-`LTS` API 与多前端工具复用架构的关键证据入账。
