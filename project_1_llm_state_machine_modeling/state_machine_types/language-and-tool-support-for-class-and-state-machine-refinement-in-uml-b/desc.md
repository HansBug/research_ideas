# UML-B 中类与状态机细化的语言与工具支持 / Language and Tool Support for Class and State Machine Refinement in UML-B

## 基本信息

- 标题：Language and Tool Support for Class and State Machine Refinement in UML-B
- 中文标题：UML-B 中类与状态机细化的语言与工具支持
- 作者：Mar Yah Said，Michael J. Butler，Colin F. Snook
- 发表：*FM 2009: Formal Methods*，pp. 579-595，2009
- DOI：`10.1007/978-3-642-05089-3_37`
- 链接：https://doi.org/10.1007/978-3-642-05089-3_37
- 形式主义：`UML-B / Event-B class and state-machine refinement`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：UML-like graphical front end / refinement notation / Event-B translator extension
- 工具/实现获取方式：原文明确说明 `UML-B tool` 是 `Rodin` Event-B 验证环境的 plug-in，并用它生成对应 `Event-B` 模型；正文未单列独立仓库地址。
- 标准/格式获取方式：承载方式是 `UML-B` package/class/state-machine diagrams 与生成的 `Event-B` machines/contexts；相关规范背景来自 `UML` 与 `Event-B`。

## 简报

这篇论文补的不是“UML 也能做细化”这种抽象口号，而是把 `UML-B` 真正补成一个可做类细化、状态机细化和事件移动的图形前端。它把 `Event-B` 的 refinement discipline 向上抬到 `UML-like` 类图和状态机图，使工程人员既能保留图形化建模体验，又不丢掉 `Rodin/Event-B` 的 proof-obligation 语义。

- 形式主义定位：`UML-B` 这条图形化 formal front-end 的 refinement 与 translator 基础设施。
- 构造方式简述：用 class diagrams 与 state machines 表达结构和行为，再由 `UML-B tool` 翻译成 `Event-B` contexts/machines，并在 `Rodin` 中 discharge POs。
- 基础设施与场景简述：依托 `UML-B` drawing tool、`Event-B` translator 与 `Rodin`，服务需要可视 refinement 的软件/控制系统开发。

```text
UML-B classes + state machines -> refined classes / refined states / event movement -> generated Event-B -> Rodin proof obligations
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML-B` 的 class diagrams 与 state machine diagrams。
2. `Event-B` 的 contexts、machines、variables、events 与 refinement 关系。
3. refined classes、inherited attributes、refined state machines、refined states。
4. event movement 与 witness 机制。
5. `UML-B tool -> Event-B translator -> Rodin` 的工具链。

### 核心抽象

结合论文的图形前端与生成后端，可把一个 `UML-B` machine 保守整理为：

$$
U = (C, A, R, SM, E)
$$

上式中的符号逐项解释如下：

1. `C` 是类集合。
2. `A` 是 attributes / associations 集合。
3. `R` 是 refinement 关系集合。
4. `SM` 是状态机集合。
5. `E` 是 class events 与 transition events 集合。
6. 这组元组是根据论文的 `class + state machine + Event-B machine` 结构做的保守归纳。

论文明确说明生成的 `Event-B` 语义采用“类、属性、状态都变变量”的方式。典型生成约束可写成：

$$
CA \subseteq CASET,\quad x \in CA \to \mathbb{N},\quad ab \in CA \to CB
$$

上式中的符号逐项解释如下：

1. `CASET`、`CBSET` 是类对应的 carrier sets。
2. `CA`、`CB` 是当前存在的实例集合。
3. `x` 是类 `CA` 上的属性。
4. `ab` 是从 `CA` 到 `CB` 的 association。
5. `CA \to \mathbb{N}` 与 `CA \to CB` 对应论文里生成的类型不变式。

对状态机细化，论文给出的核心关系可压成：

$$
A = A_1 \cup A_2 \cup A_3,\quad A_i \subseteq A,\quad A_i \cap A_j = \varnothing \ (i \ne j)
$$

上式中的符号逐项解释如下：

1. `A` 是 refined super-state。
2. `A_1,A_2,A_3` 是其 sub-states。
3. `A = A_1 \cup A_2 \cup A_3` 表示 sub-states 构成 refined state。
4. 两两不交约束保证状态划分清晰。

事件移动时，论文引入 witness 关系：

$$
ca = self
$$

上式中的符号逐项解释如下：

1. `self` 是抽象层类事件中的默认 self-name 参数。
2. `ca` 是细化层中新引入的参数。
3. witness 说明细化层参数如何对应抽象层参数。

### 一个最小例子与通俗解释

论文给了一个很直观的 ATM 细化例子：

1. 抽象层先有 `Account`、`ATM` 等类及基础状态机。
2. 下一层把 `ATM` 的 `active_atm` 细化成带多个 sub-state 的 nested state machine。
3. 抽象 transition `t2` 可以被 `t2a`、`t2b` 多条细化 transition 替代。
4. 原来挂在某个类上的事件，还可以被移动成另一类状态机中的 transition，并用 witness 保持 refinement 对应。

通俗地说，这篇论文做的事，就是让“图上的类和状态图”不再只是画法，而是真正带着 `Event-B` 细化纪律往下走。你可以把大状态拆小、把一个抽象事件拆成几条更具体的转移，同时还保留可证明的 refinement 关系。

### 运行 / 接受 / 转移语义

论文的核心语义不是运行时解释器，而是翻译到 `Event-B` 的静态-证明语义：

1. 类、属性、association 生成 `Event-B` variables 与 invariants。
2. state machine states 生成表示活动实例集合的变量。
3. transitions 生成 `Event-B` events。
4. refinement 通过新的 invariants、细化事件与 witness 约束体现。

对状态机细化，论文的结构约束可概括为：

1. 每条抽象 transition 可被一条或多条具体 transition 替换。
2. 一个抽象 state 可被 nested state machine 展开。
3. self-loop transition 可被 sub-states 间 transition 精细化。

### 语义边界

边界同样明确：

1. 主线是 safety-preserving refinement，不处理 liveness。
2. 这是 `UML-B` 前端及其 `Event-B` 映射，不是完整 UML 全语法。
3. 细化主要服务类图与状态机，不是 sequence diagram 或完整对象交互语义。
4. 证明能力最终仍取决于生成后的 `Event-B/Rodin` 证明。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 前端骨架 | `$U = (C, A, R, SM, E)$` | `UML-B` machine 把类、状态机与 refinement 绑定到同一图形前端。 |
| 类/属性生成 | `$CA \subseteq CASET,\ x \in CA \to \mathbb{N}$` | 类图元素被翻成 `Event-B` 变量与不变式。 |
| refined state 组成 | `$A = A_1 \cup A_2 \cup A_3$` | super-state 可被 sub-states 展开。 |
| disjointness | `$A_i \cap A_j = \varnothing$` | refined state 的子状态要两两不交。 |
| witness | `$ca = self$` | 事件移动后仍保留抽象层参数对应。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 显式支持类内 state machines 与 refined states。 |
| 事件 / 触发 | 很强 | class events 与 transition events 都可细化。 |
| 守卫 / 数据 | 强支持 | class attributes、associations、guards 都映射进 `Event-B`。 |
| 层次 | 中等到强 | 通过 nested state machines 支持 refinement hierarchy。 |
| 并发 / 同步 | 中等支持 | 多类、多状态机可共存于同一 machine，但主体不是并发语义优化。 |
| 时间约束 | 不支持 | 本文不是 timed UML / timed Event-B 路线。 |
| 连续动态 / 随机性 | 不支持 | 不在范围内。 |
| 可执行 / 可验证性 | 很强 | `UML-B tool` 与 `Rodin` 构成完整可验证链。 |

### 形式化问题与性质

1. 论文的核心不是提出新的状态机本体，而是把 `Event-B` refinement discipline 安到 `UML-B` 图形前端上。
2. refined state machine 与 event movement 两个机制，使前端能承载更真实的渐进式设计过程。
3. 这条路线对“图形化可接受性”和“形式化可证明性”的平衡做得很典型。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 先画 package、context、class、state machine diagrams。
2. 在 refinement 层中标注 refined classes / states / transitions。
3. 由 `UML-B tool` 自动生成 `Event-B` context 与 machine。
4. 在 `Rodin` 中生成并证明 POs。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UML-B` 图形模型。
2. 生成的 `Event-B` contexts / machines。
3. 类、状态、transition 对应的变量与事件。
4. refinement witness 与 invariants。

### 交换与互操作

这条线的互操作重点在于：

1. `UML-like` 图形前端到 `Event-B` 后端的稳定翻译。
2. `Rodin` proof obligations 对图形建模结果的承接。
3. 类图与状态图在同一 refinement 体系内协同演进。

## 配套基础设施

- 建模/编辑工具：`UML-B tool`。
- 解析/交换/元模型支持：`UML-B` diagrams 到 `Event-B` contexts/machines 的 translator。
- 仿真/执行支持：论文重点不在执行器，而在 `Event-B` 证明链。
- 验证/分析支持：`Rodin` provers 与生成的 proof obligations。
- 代码生成/转换支持：主线是 `UML-B -> Event-B` 翻译，不是部署代码生成。
- 标准化或社区生态：依托 `UML-B`、`Event-B` 与 `Rodin` 社区生态。

## 适用场景与需求前提

### 适用场景

适合需要图形化 refinement、对象结构与状态机协同建模、并希望最终落到 `Event-B/Rodin` 证明链的软件与控制系统。

### 需求前提

1. 团队接受 `Event-B` 的 invariants / events / refinement 心智模型。
2. 需要用 class diagram + state machine 共同表达系统。
3. 设计过程确实存在多层 refinement，而不是一次性细化到最终实现。
4. 目标性质以 safety 与结构一致性为主。

### 不适用或高成本场景

若需求主要是 run-time execution、代码生成或 timed/continuous behavior，这条路线就不如专门的 execution DSL 或 timed formalism 自然。

## 与相邻形式主义的关系

相对 [uml-251-specification/desc.md](../uml-251-specification/desc.md)，它不是通用 `UML` 标准，而是面向 `Event-B` 的 restricted graphical front end；相对 [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)，它更强调 refinement 与 proof，而不是翻译到 process algebra 做模型检查；相对 [turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md](../turtle-a-real-time-uml-profile-supported-by-a-formal-validation-toolkit/desc.md)，它不引入 timed profile，而是把类与状态机细化纪律接到 `Event-B`。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续希望让 LLM 输出“图形化可接受、但仍可证明”的状态机工件，`UML-B` 这种受限前端值得关注。

### 作为目标形式主义还是中间表示

更适合作为图形前端与形式证明后端之间的桥，而不是最终执行载体。

### 对需求到模型生成的启发

1. refinement 层级应成为生成任务的一等对象，而不是只生成最终状态图。
2. 类、关联和状态机的细化往往要联动进行。
3. 事件移动与 witness 对应机制对“修复后保持可追溯”很有启发。

### 现实限制

它非常适合 safety-oriented formal development，但不等价于完整 UML 生态，也不直接解决执行部署问题。

## 重要的相关工作

1. [uml-251-specification/desc.md](../uml-251-specification/desc.md)：通用 `UML State Machine` 规范入口。
2. [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)：另一条 `UML -> formal backend` 桥接路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML 状态机形式化与自动验证综述。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 归类理由：论文主体是 `UML-B` 这门图形前端语言及其 `Event-B/Rodin` 工具支撑，不只是一般验证算法，因此按 `🔣/🏗️` 更合适。
