# 面向 AutoFocus 工具链的已验证系统开发 / Verified System Development with the AutoFocus Tool Chain

## 基本信息

- 标题：Verified System Development with the AutoFocus Tool Chain
- 中文标题：面向 AutoFocus 工具链的已验证系统开发
- 作者：Maria Spichkova，Florian Hölzl，David Trachtenherz
- 发表：*2nd Workshop on Formal Methods in the Development of Software 2012 (WS-FMDS 2012)*，*Electronic Proceedings in Theoretical Computer Science* 86:17-24，2012
- DOI：`10.4204/EPTCS.86.3`
- 链接：https://doi.org/10.4204/EPTCS.86.3
- 形式主义：`Focus / AutoFocus 3 / Isabelle-HOL / C0 verified development tool chain`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：verified-development methodology and transformation chain over `AutoFocus 3`, `FOCUS`, `Isabelle/HOL`, and `C0`
- 工具/实现获取方式：原文明确给出 `AutoFocus 3` 工具链入口 `http://af3.fortiss.org`，并说明存在 `AutoFocus 3 -> Isabelle/HOL` translator 与 `AutoFocus 3 -> C0` code generator。
- 标准/格式获取方式：核心承载是 informal / semiformal requirements、`MSC`、`FOCUS` requirements and architecture specifications、`AutoFocus 3` model、`Isabelle/HOL` theories 与 `C0` code；不是中立行业交换标准。

## 简报

这篇论文的关键价值，不是再提出一种新的状态机或 DSL，而是把“从需求到形式化模型，再到证明辅助器和受限 `C` 代码”的整条 verified-development pipeline 讲清楚。它补的是 `AutoFocus 3` 这条 component-automata workbench 如何被放进真正可追溯、可验证、可生成代码的方法路线中。

- 形式主义定位：围绕 `AutoFocus 3` 的端到端 verified-development 方法路线，而不是新的状态机母型。
- 构造方式简述：先把 informal requirements 结构化成 semiformal text / `MSC`，再转成 `FOCUS` requirements and architecture，随后落到 `AutoFocus 3` 模型，并继续生成 `Isabelle/HOL` 理论与 `C0` 代码。
- 基础设施与场景简述：依托 `FOCUS`、`AutoFocus 3`、temporal logic、model checking、`Isabelle/HOL` translator、`C0` generator 与 paper-and-pencil equivalence argument，服务 safety-critical embedded software。

```text
informal requirements -> semiformal text / MSC -> FOCUS requirements + architecture -> AutoFocus 3 model -> Isabelle/HOL theories / C0 code
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. informal requirements 与其 semiformal textual patterns。
2. `MSC` 表示。
3. `FOCUS` requirements / architecture specifications。
4. `AutoFocus 3` executable model。
5. `Isabelle/HOL` translator 与 `C0` code generator。

### 核心抽象

论文最核心的形式化对象不是单个 automaton，而是分层开发链。可把该方法保守整理为：

$$
\mathcal D = (R_i, R_s, M, S_r, S_a, A, H, C_0)
$$

上式中的符号逐项解释如下：

1. `$R_i$` 是 informal requirements specification。
2. `$R_s$` 是 semiformal requirements specification。
3. `$M$` 是 `MSC` specification。
4. `$S_r$` 是 `FOCUS` requirements specification。
5. `$S_a$` 是 `FOCUS` architecture specification。
6. `$A$` 是 `AutoFocus 3` model。
7. `$H$` 是由 translator 生成的 `Isabelle/HOL` theory set。
8. `$C_0$` 是 `C0` implementation。

正文对方法链的图示可进一步压成一个有向变换序列：

$$
R_i \rightarrow R_s \rightarrow M \rightarrow (S_r, S_a) \rightarrow A \rightarrow (H, C_0)
$$

上式中的符号逐项解释如下：

1. 前三步对应从自由文本到结构化文本与 `MSC` 的 requirements clarification。
2. `$(S_r,S_a)$` 表示在 `FOCUS` 层同时保留 requirements view 与 architecture view。
3. `$A$` 是可执行、可仿真的 `AutoFocus 3` 模型。
4. `$(H,C_0)$` 表示同一模型继续通向 theorem proving artifact 与 executable implementation。

论文还明确强调了语义保持的自动生成器。对 `AutoFocus 3 -> Isabelle/HOL` 与 `AutoFocus 3 -> C0` 两条链，可保守整理为：

$$
\llbracket A \rrbracket_{AF3} = \llbracket \mathrm{Gen}_{HOL}(A) \rrbracket
$$

$$
\llbracket \mathrm{Gen}_{C0}(A) \rrbracket \preceq \llbracket A \rrbracket_{AF3}
$$

上式中的符号逐项解释如下：

1. `$\llbracket \cdot \rrbracket$` 表示相应工件的行为语义。
2. `$\mathrm{Gen}_{HOL}$` 是 `AutoFocus 3 -> Isabelle/HOL` translator。
3. `$\mathrm{Gen}_{C0}$` 是 `AutoFocus 3 -> C0` code generator。
4. 第一式对应原文关于 translator 与 `AutoFocus` 模型行为等价的说明。
5. 第二式用保守写法表达“生成代码是模型的 admissible simulation / behavior-preserving implementation route”。

### 一个最小例子与通俗解释

论文用 automotive case study 解释这条链最直观。可以把它简化成一个 cruise-control 例子：

1. 需求首先以自然语言写出，例如“如果驾驶员按下加速按钮，且没有关停条件出现，则系统在下一时间单位内加速车辆”。
2. 这些句子先按 `WHILE / IF / THEN / ELSE` 模式重写成 semiformal requirements。
3. 然后转成 `MSC` 和 `FOCUS` requirements / architecture。
4. 再把 architecture 落成 `AutoFocus 3` 的 component model 与 automata behavior。
5. 之后可以一边导出 `Isabelle/HOL` 做证明，一边生成 `C0` 代码。

通俗地说，这篇论文像是在回答：“状态机和组件模型不是最后一张图，而是中间那个能把需求、证明和实现串起来的枢纽。” 它把 `AutoFocus 3` 放在 verified-development pipeline 的中央位置。

### 运行 / 接受 / 转移语义

论文在 `AutoFocus 3` 层依然采用 time-synchronous reactive semantics。对模型逐步执行，可保守写成：

$$
A(t+1) = F(A(t), I(t))
$$

上式中的符号逐项解释如下：

1. `$A(t)$` 是时刻 `$t$` 的全局模型状态。
2. `$I(t)$` 是该 tick 的输入观测。
3. `$F$` 是由 component structure、ports、behavior specifications 共同决定的同步更新函数。
4. 这对应原文所说 `AutoFocus 3` 建模语言基于 restricted `FOCUS` semantics 和 time-synchronous frame。

在 requirements clarification 层，论文给了固定文本骨架：

$$
\texttt{WHILE } p \quad \texttt{IF } e \quad \texttt{THEN } q \quad \texttt{ELSE } r
$$

上式中的符号逐项解释如下：

1. `$p$` 是一段持续状态条件。
2. `$e$` 是事件或状态变化触发。
3. `$q$` 是触发后应发生的结果。
4. `$r$` 是否则分支的结果。
5. 这不是逻辑公理，而是原文给出的 semiformal requirement pattern。

### 语义边界

1. 这篇论文的中心是 development methodology 与 transformation chain，不是新的 automata theory。
2. 其时间观建立在离散、同步、reactive embedded-system modeling 上，不是 dense-time timed automata。
3. 从 `FOCUS` 到 `AutoFocus 3` 的映射在文中仍以 formal / schematic transformation 为主，完全自动化被明确标为 ongoing work。
4. 它非常适合安全关键 embedded software，但对高度连续、强非线性物理控制对象并不是直接建模母型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 开发链元组 | `$\mathcal D = (R_i, R_s, M, S_r, S_a, A, H, C_0)$` | 把 paper 的全过程工件压成统一对象。 |
| 工件变换链 | `$R_i \rightarrow R_s \rightarrow M \rightarrow (S_r,S_a) \rightarrow A \rightarrow (H,C_0)$` | 论文图 1 的核心 pipeline。 |
| `AutoFocus -> HOL` 保持 | `$\llbracket A \rrbracket_{AF3} = \llbracket \mathrm{Gen}_{HOL}(A) \rrbracket$` | translator 的行为等价目标。 |
| `AutoFocus -> C0` 保守实现 | `$\llbracket \mathrm{Gen}_{C0}(A) \rrbracket \preceq \llbracket A \rrbracket_{AF3}$` | code generator 需要是模型的 admissible simulation / behavior-preserving implementation。 |
| requirements pattern | `$\texttt{WHILE } p\ \texttt{IF } e\ \texttt{THEN } q\ \texttt{ELSE } r$` | 从 informal text 向 semiformal specification 收束的固定骨架。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `AutoFocus 3` 层以 component behavior、I/O automata 与 state variables 表达离散控制逻辑。 |
| 事件 / 触发 | 强 | requirements pattern、ports 与 message flow 都以事件 / 状态变化驱动。 |
| 守卫 / 数据 | 中等支持 | `AutoFocus 3` 包含 data dictionary、typed ports 与 transition pre/postconditions。 |
| 层次 | 强 | 从 requirements decomposition 到 component hierarchy 都是层次化组织。 |
| 并发 / 同步 | 强 | 组件网络按 global synchronized time frame 运行。 |
| 时间约束 | 中等支持 | 明确关注 embedded timing aspects，但主线是 time-synchronous reactive semantics，不是 clocks。 |
| 连续动态 / 随机性 | 不支持 | 不是论文主体。 |
| 可执行 / 可验证性 | 很强 | `FOCUS`、model checking、`Isabelle/HOL`、`C0` code generation 被串进同一闭环。 |

### 形式化问题与性质

1. 论文的主创新不在单点验证算法，而在把 requirements structuring、formal modeling、theorem proving 和 code generation 拉成一条连续链。
2. `AutoFocus 3` 在这条链里不是孤立建模器，而是连接 formal specification 与 implementation 的执行性中枢。
3. 对本论文集而言，它是非常典型的“方法路线为主，但同时强烈依赖状态机 / component-automata 基础设施”的条目。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. informal requirements text。
2. semiformal requirement patterns。
3. `MSC`。
4. `FOCUS` requirements / architecture specifications。
5. `AutoFocus 3` data type、system structure 和 component behavior views。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `FOCUS` formal specifications。
2. `AutoFocus 3` component models。
3. temporal-logic specifications for model checking。
4. generated `Isabelle/HOL` theories。
5. generated `C0` code。

### 交换与互操作

1. `FOCUS` requirements 和 architecture 可转向 `Isabelle/HOL` 与 `AutoFocus 3`。
2. `AutoFocus 3` 可继续导出 theorem-prover theories 与 `C0` implementation。
3. 论文还明确提出未来补 deployment model 与 distributed execution environment description。
4. 这是一条工程化 transformation chain，而不是中立 interchange standard。

## 配套基础设施

- 建模/编辑工具：`AutoFocus 3` graphical modeling environment，支持 data types、system structure 与 component behavior。
- 解析/交换/元模型支持：semiformal textual patterns、`MSC`、`FOCUS` specifications、`AutoFocus 3` translators。
- 仿真/执行支持：`AutoFocus 3` simulator 可用于 executable-model validation。
- 验证/分析支持：requirements 到 temporal logic 的 model-checking route，以及 `FOCUS on Isabelle` / `AutoFocus 3 -> Isabelle/HOL` theorem-proving route。
- 代码生成/转换支持：`AutoFocus 3 -> C0` code generator，且原文强调其语义保持与 translation validation 角色。
- 标准化或社区生态：`FOCUS`、`AutoFocus 3`、`Isabelle/HOL`、`C0` 与 automotive case-study chain 共同构成方法生态；原文未给行业中立标准。

## 适用场景与需求前提

### 适用场景

适合 safety-critical embedded software、automotive application software、需要把 requirements clarification、formal verification 与 generated implementation 放进同一开发链的场景。

### 需求前提

1. 需求需要能够先被结构化成 semiformal textual patterns，再提升到 `MSC` / `FOCUS`。
2. 系统应可抽成 distributed, timed, reactive component architecture。
3. 团队接受 time-synchronous modeling discipline 与逐层 refinement。
4. 若要真正吃到工具链收益，必须愿意同时维护 requirements、architecture、proof 与 generator assumptions 的一致性。

### 不适用或高成本场景

1. 若项目并不需要 theorem proving 或 semantics-preserving code generation，这条链会显得过重。
2. 若系统高度依赖连续控制、优化或概率行为，而不能自然落成 `AutoFocus 3` component model，建模成本会很高。
3. 若 requirements 本身过于松散，连 semiformal patterns 都无法稳定收束，后续 formal transformation 会卡住。

## 与相邻形式主义的关系

相对 [autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md](../autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md)，本文不是平台本体，而是把 `AutoFocus 3` 放进 verified-development pipeline；相对 [user-friendly-model-checking-integration-in-model-based-development/desc.md](../user-friendly-model-checking-integration-in-model-based-development/desc.md)，后者只补 model-checking integration，本文则把 `FOCUS`、`Isabelle/HOL` 和 `C0` 全链路贯通；相对 `BIP` 一类 rigorous design flow 条目，本文更强调从 requirements 开始的 seamless formal development，而不只是组件组合与死锁验证。

## 与本研究的关系

### 对 Project 1 的价值

1. 它直接说明：若未来让 LLM 从需求生成状态机，真正有价值的不只是生成图，还要把 requirements structuring、formal transformation 和 verification evidence 一起组织起来。
2. 对 `project_1` 的“生成-验证-修复”闭环，这篇论文提供了一个很强的工程参照物，即模型必须位于可证明、可生成、可追溯的中间层。
3. 其 `WHILE / IF / THEN / ELSE` 式 semiformal pattern 也非常适合作为需求到状态机抽取的前置规整模板。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像“高可信状态机工程化落地方式”的方法路线与基础设施锚点，而不是最终要比较的独立状态机母型。

## 重要的相关工作

- [autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md](../autofocus-3-a-scientific-tool-prototype-for-model-based-development-of-component-based-reactive-distributed-systems/desc.md)：`AutoFocus 3` 平台本体条目。
- [user-friendly-model-checking-integration-in-model-based-development/desc.md](../user-friendly-model-checking-integration-in-model-based-development/desc.md)：`AutoFocus 3` 上的 property-oriented model-checking integration。
- [rigorous-component-based-system-design-using-the-bip-framework/desc.md](../rigorous-component-based-system-design-using-the-bip-framework/desc.md)：另一条把组件模型、验证和实现串成工程流程的对照路线。

## 文献分类总结

- 这篇论文在本论文集中的主类是 `📦 标准、交换格式、元模型与执行载体`，因为它的核心贡献是 verified-development tool chain 和 transformation chain，而不是新的状态机语言本体。
- 其对象类型归为 `🛠️ 方法路线`，因为论文主体围绕“如何把 `AutoFocus 3` 放进 requirements -> proof -> code 的方法链”展开。
- 描述客体归为 `🎛️ 控制 / 反应式逻辑`，因为其建模与验证对象是 reactive embedded application software 的组件化行为逻辑。
- 所属领域归为 `⏱️ 实时与嵌入式系统`，因为全文语境和 case study 都集中在 safety-critical embedded / automotive systems。
