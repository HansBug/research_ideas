# 基于 Institution 的简单 UML 状态机在 CASL/SPASS 中的编码与验证 / Institution-Based Encoding and Verification of Simple UML State Machines in CASL/SPASS

## 基本信息

- 标题：Institution-Based Encoding and Verification of Simple UML State Machines in CASL/SPASS
- 中文标题：基于 Institution 的简单 UML 状态机在 CASL/SPASS 中的编码与验证
- 作者：Tobias Rosenberger，Saddek Bensalem，Alexander Knapp，Markus Roggenbach
- 发表：*Recent Trends in Algebraic Development Techniques*，pp. 120-141，2021
- DOI：`10.1007/978-3-030-73785-6_7`
- 链接：https://doi.org/10.1007/978-3-030-73785-6_7
- 形式主义：`Simple UML State Machines / M#_D / CASL-SPASS`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：把 simple UML state machines 机构化成 `M#_D` 逻辑框架，再经 `CASL` 与 `SPASS` 提供符号证明路线
- 工具/实现获取方式：原文明确说明实现已集成到 `Hets` 的一个 fork 中，入口为 `https://github.com/spechub/hets`；证明后端使用自动定理证明器 `SPASS`。
- 标准/格式获取方式：输入承载是接近 `PlantUML` 风格的 `UMLSM` 文本语法；中间承载是逻辑框架 `M#_D`；后端承载是 `CASL` 规范与 `SPASS` 可处理的一阶证明义务。

## 简报

这篇论文补的不是“UML 也可以翻成逻辑”这种泛泛说法，而是一条机构论驱动的严整链路：先把 simple UML state machines 的事件、数据、控制状态和输入完备语义固定成一套模型类，再把它们放进新的混合模态逻辑 `M#_D`，最后通过 theoroidal institution comorphism 映到 `CASL`，交由 `SPASS` 做符号证明。

- 形式主义定位：受限 UML 状态机子语言的 institution-based verification 路线，不是通用 UML 工具平台。
- 构造方式简述：`UMLSM` 文本规范先翻成 simple UML state machine，再自动生成 `M#_D` 句子，最后经 comorphism 落到 `CASL`。
- 基础设施与场景简述：依托 `Hets`、`M#_D`、`CASL` 与 `SPASS`，服务带数据、守卫和输入完备语义的 UML 状态机符号验证。

```text
simple UML state machine -> event/data signature + transition specs -> M#_D sentence -> theoroidal comorphism -> CASL specification -> SPASS proof obligations
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. simple UML state machines 的事件、属性、控制状态与转移规格。
2. event/data signatures、data states 与 transition predicates。
3. event/data structures 这一语义模型类。
4. 用于描述这些结构的混合模态逻辑 `M#_D`。
5. `M#_D -> CASL` 的 theoroidal institution comorphism。
6. `Hets` 中从 `UMLSM` 到 `CASL/SPASS` 的自动翻译链。

### 核心抽象

论文对事件和数据接口的基础对象定义得很清楚，可直接整理为：

$$
\Sigma = (E(\Sigma), A(\Sigma))
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是 event/data signature。
2. `E(\Sigma)` 是事件签名，给出事件名及其参数变量。
3. `A(\Sigma)` 是数据签名，给出属性集合。

simple UML state machine 本体则可写成：

$$
U = (\Sigma(U), C(U), T(U), c_0(U), \varphi_0(U))
$$

上式中的符号逐项解释如下：

1. `\Sigma(U)` 是机器使用的 event/data signature。
2. `C(U)` 是有限控制状态集合。
3. `T(U)` 是有限转移规格集合。
4. `c_0(U)` 是初始控制状态。
5. `\varphi_0(U)` 是初始数据状态谓词。

一条转移规格的形状是：

$$
(c,\varphi,e(X),\psi,c')
$$

上式中的符号逐项解释如下：

1. `c` 是源控制状态。
2. `\varphi` 是数据状态守卫。
3. `e(X)` 是带参数变量集合 `X` 的事件。
4. `\psi` 是数据转移谓词，也就是 eﬀect。
5. `c'` 是目标控制状态。

论文对语义结构也给出明确骨架，可整理为：

$$
M = (\Gamma, R, \Gamma_0, \omega)
$$

上式中的符号逐项解释如下：

1. `\Gamma` 是配置集合，每个配置包含控制状态和某个数据名。
2. `R` 是按事件及其实例化参数划分的转移关系族。
3. `\Gamma_0` 是初始配置集合。
4. `\omega` 是把数据名解释成实际数据状态的标注函数。

### 一个最小例子与通俗解释

论文用一个 bounded, resettable counter 作为 running example：

1. 机器有两个控制状态 `s_1` 与 `s_2`。
2. 属性只有 `cnt`，初值为 `0`。
3. 事件 `inc(x)` 在不同 guard 下既可让状态停在 `s_1`，也可在计数到 `4` 时切到 `s_2`。
4. `reset` 会把计数重置为 `0` 并回到 `s_1`。
5. 未显式处理的输入会按 UML 输入完备语义被“静默丢弃”，等价为不改数据的自环。

通俗地说，这条路线不是去运行 UML 状态机，而是把“什么输入允许发生、发生后数据怎么变、哪些迁移必须存在、哪些迁移必须不存在”都翻成逻辑句子。于是验证器不再只做状态遍历，而是可以做真正的符号证明。

### 运行 / 接受 / 转移语义

论文最关键的语义点，是 simple UML state machine 的模型必须同时满足“显式迁移存在”和“未指定行为不得乱跑”。这在文中体现在 event/data structures 的模型条件上。

其核心可保守压成：

$$
M \models U
$$

当且仅当：

1. 对于 `T(U)` 中每条 `(c,\varphi,e(X),\psi,c')`，只要当前配置满足 guard `\varphi`，就必须存在一个 `e(X)` 转移到某个满足 effect `\psi` 的后继配置。
2. 对于结构中任何实际出现的 `e(X)` 转移，它要么来自某条显式转移规格，要么就是“没有任何 guard 可用时”的输入完备自环。

论文给出的输入完备 completion 也可以直接整理为：

$$
\{(c,\neg \bigvee_{(c,\varphi,e(X),\psi,c') \in T(U)} \varphi,\ e(X),\ 1_{A(\Sigma(U))},\ c)\mid c \in C(U),\ e(X)\in E(\Sigma(U))\}
$$

上式中的符号逐项解释如下：

1. `c` 是某个控制状态。
2. `e(X)` 是某个事件。
3. `\neg \bigvee ... \varphi` 表示当前没有任何显式转移 guard 被满足。
4. `1_{A(\Sigma(U))}` 表示数据保持不变的恒等 eﬀect。
5. 这一组自环把 simple UML state machine 补成 input-enabled。

对 `M#_D`，论文的直觉可保守概括为“既能表达必须存在的转移，也能表达禁止出现的转移”。其机构化关系可写成：

$$
(SM^\#_D,\ Str^\#_D,\ Sen^\#_D,\models_{M^\#_D})
$$

上式中的符号逐项解释如下：

1. `SM^\#_D` 是 `M#_D` 的签名范畴。
2. `Str^\#_D` 是 `M#_D` 的结构范畴。
3. `Sen^\#_D` 是 `M#_D` 的句子构造。
4. `\models_{M^\#_D}` 是满足关系。
5. 论文正式证明这四元组构成一个 institution。

### 语义边界

边界非常清楚：

1. 只处理 simple UML state machines。
2. 当前不覆盖 hierarchical states、compound transitions、defer 和状态机间事件通信。
3. 重点是数据、状态、guarded transitions 与输入完备语义。
4. 主线是 symbolic verification，不是执行仿真或代码生成。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 事件/数据接口 | `$\Sigma = (E(\Sigma), A(\Sigma))$` | 机器接口同时由事件签名和属性签名组成。 |
| simple UML 状态机元组 | `$U = (\Sigma(U), C(U), T(U), c_0(U), \varphi_0(U))$` | 机器本体由接口、控制状态、转移、初始状态与初始谓词组成。 |
| 转移规格 | `$(c,\varphi,e(X),\psi,c')$` | 一条迁移同时约束源状态、guard、事件、effect 和目标状态。 |
| 语义结构 | `$M = (\Gamma, R, \Gamma_0, \omega)$` | 语义模型是带可达性约束的 event/data transition system。 |
| 输入完备 completion | `$\{(c,\neg \bigvee ...,\ e(X),\ 1_{A(\Sigma(U))},\ c)\}$` | 未显式处理的输入被补成不改数据的自环。 |
| 机构论后端 | `$\nu : M^\#_D \to \mathrm{CASL}$` | `M#_D` 可通过 theoroidal comorphism 映到 `CASL`。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 UML control states。 |
| 事件 / 触发 | 很强 | 事件签名与参数化事件是核心。 |
| 守卫 / 数据 | 很强 | guard 与 effect 都被显式逻辑化。 |
| 层次 | 不支持 | simple UML 子集故意排除了 hierarchical states。 |
| 并发 / 同步 | 弱支持 | 当前不处理状态机间事件通信。 |
| 时间约束 | 不支持 | 不在本文范围。 |
| 连续动态 / 随机性 | 不支持 | 不在本文范围。 |
| 可执行 / 可验证性 | 强验证、弱执行 | 主线是符号证明，不是运行执行。 |

### 形式化问题与性质

1. 论文真正解决的是“怎样把 UML 状态机放进 institution theory，同时保住 satisfaction condition 和工具独立性”。
2. `M#_D` 的价值在于它比直接把 UML 各部件各自机构化更贴近状态机领域对象。
3. `CASL/SPASS` 只是一个后端实例；更重要的是先在 institution 层面把语义和翻译固定下来。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 用 `UMLSM` 文本语法写 simple UML state machine。
2. 明确事件、参数、属性、控制状态与转移效果。
3. 在 `Hets` 中自动翻译成 `M#_D` 句子。
4. 再翻译成 `CASL` 规范并交给 `SPASS` 证明。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 接近 `PlantUML` 风格的 `UMLSM` 文本。
2. `M#_D` 逻辑句子。
3. `CASL` 规范与 frame。
4. `SPASS` 消费的证明义务。

### 交换与互操作

这条路线的互操作重点在于：

1. `UMLSM -> M#_D` 的自动翻译。
2. `M#_D -> CASL` 的 theoroidal institution comorphism。
3. `Hets` 把前端 UML 状态机桥接到多个逻辑与证明后端的能力。

## 配套基础设施

- 建模/编辑工具：`Hets` 扩展了 `UMLSM` 输入语言与 parser。
- 解析/交换/元模型支持：`UMLSM` 文本语法、`M#_D` 逻辑表示与 `CASL` 规范共同构成承载链。
- 仿真/执行支持：不是本文重点，主线是逻辑翻译与证明。
- 验证/分析支持：`SPASS` 做自动定理证明；`CASL` 规格承载证明义务。
- 代码生成/转换支持：有稳定的自动翻译链，但目标是逻辑证明，不是部署代码。
- 标准化或社区生态：依托 `CASL`、`Hets` 和 institution theory 社区生态。

## 适用场景与需求前提

### 适用场景

适合需要对带数据和 guard 的 UML 状态机做严格、可追溯、符号化验证的场景，尤其是希望把受限 UML 前端接入 algebraic specification / theorem proving 生态的研究型或高可信设计流程。

### 需求前提

1. 行为模型能落入 simple UML 子集。
2. 属性与 eﬀect 能写成明确的数据谓词和转移谓词。
3. 验证任务更偏 invariants、可达性和结构性约束，而不是复杂运行时仿真。
4. 团队能接受 `CASL/SPASS` 这类逻辑证明工作流。

### 不适用或高成本场景

如果需求高度依赖完整 UML 交互语义、层次状态、复杂通信或执行部署，这条 institution-based symbolic 路线就会显得过重或不够贴近工程执行。

## 与相邻形式主义的关系

相对 [language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md](../language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md)，这篇更偏 institution-based logical encoding，而不是 `Event-B` refinement 前端；相对 [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)，它走 theorem-proving / algebraic-specification 路线，不走显式状态空间模型检查；相对 [a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md](../a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md)，它覆盖的 UML 面更窄，但换来了更清晰的 institution 语义与符号证明闭环。

## 与本研究的关系

### 对 Project 1 的价值

它说明若后续 LLM 生成的是受限但结构清晰的 UML 状态机，那么完全可以把事件、属性和 guard/effect 直接送入逻辑框架，而不必先退化成更弱的无数据有限状态机。

### 作为目标形式主义还是中间表示

更像中间验证表示和验证路线，而不是最终交付格式。

### 对需求到模型生成的启发

1. 需求抽取时最好把事件接口、属性签名和初始条件单独结构化。
2. guard 与 effect 若能写成清晰谓词，后续可直接进入 theorem-proving 流程。
3. “未处理输入如何定义”必须在建模阶段决定，否则 satisfaction condition 很难稳定。

### 现实限制

这篇论文证明的是一条受限 UML 状态机的机构化符号验证路径，不是完整 UML 全生态的统一解法。

## 重要的相关工作

1. [language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md](../language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md)：图形前端接 `Event-B/Rodin` 的另一条 UML 形式化路线。
2. [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)：把 executable UML 接到 `mCRL2/LTSmin` 的模型检查路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML 状态机形式化与自动验证的综述总览。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Simple UML State Machines / M#_D / CASL-SPASS`
- 归类理由：论文主体是把受限 UML 状态机机构化并接到 `CASL/SPASS` 的方法路线，核心贡献在翻译、语义与证明链，而不是单独的运行时基础设施。
