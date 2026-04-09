# MTSA：模态迁移系统 Eclipse 工作台 / MTSA: Eclipse support for Modal Transition Systems construction, analysis and elaboration

## 基本信息

- 标题：MTSA: Eclipse support for Modal Transition Systems construction, analysis and elaboration
- 中文标题：MTSA：模态迁移系统 Eclipse 工作台
- 作者：Nicolas D'Ippolito，Dario Fishbein，Howard Foster，Sebastian Uchitel
- 发表：*Proceedings of the 2007 OOPSLA Workshop on Eclipse Technology eXchange*，pp. 6-10，2007
- DOI：`10.1145/1328279.1328281`
- 链接：https://www.cs.mcgill.ca/~martin/etx2007/papers/2.pdf
- 形式主义：`Modal Transition Systems / MTSA`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 论文角色：Eclipse workbench / partial-behavior synthesis and analysis plugin
- 工具/实现获取方式：原文明确说明 `MTSA-Eclipse` 插件可公开获取于 `http://lafhis.dc.uba.ar/suchitel/MTSA.html`。
- 标准/格式获取方式：承载方式是扩展 `FSP` 文本语言、Eclipse editor / outline / draw / animator views；原文未给独立于工具的中立交换标准。

## 简报

这篇论文的核心价值，不是再定义一遍 `MTS`，而是把“部分行为规格”真正落成工程工作台。`MTSA` 允许用户用扩展 `FSP` 写 `Modal Transition Systems`，再在 Eclipse 里做并行组合、merge、从 `FLTL` 约束或场景合成模型、三值 model checking 与动画验证。对 `project_1` 来说，这条线很重要，因为它说明需求在早期不完整时，不一定非要先压成完全确定的 `FSM`；可以先保留 `may / required` 区分，再逐步精化。

- 形式主义定位：面向 `Modal Transition Systems` 的 Eclipse 工程工作台，而不是新的状态机本体。
- 构造方式简述：用扩展 `FSP` 写 partial behavior，再在 workbench 中做 composition、merge、property/scenario synthesis、model checking 和 animation。
- 基础设施与场景简述：依托 `FSP Editor`、`Outline View`、`MTS Draw View`、`Animator View` 和 `LTSA` core，服务软件需求精化、部分规格验证和场景驱动建模。

```text
partial requirements -> MTS in extended FSP -> synthesis / merge / refinement-oriented elaboration -> 3-valued checking / animation
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象是 `Modal Transition Systems (MTS)` 与其 Eclipse 载体：

1. states 与初始状态。
2. required transitions。
3. maybe transitions。
4. refinement 与 implementation 关系。
5. 从 `FLTL` 约束和 scenarios 合成得到的 partial models。

### 核心抽象

结合论文对 `MTS` 的描述，可保守整理成：

$$
M = (S, Act, \to_{req}, \to_{may}, s_0)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `Act` 是动作集合。
3. `\to_{req}` 是 required transition relation。
4. `\to_{may}` 是 maybe transition relation。
5. `s_0` 是初始状态。

`MTS` 的基本一致性条件可写成：

$$
\to_{req} \subseteq \to_{may}
$$

上式中的符号逐项解释如下：

1. 每条 required 行为也必须是允许出现的行为。
2. `maybe` 表示“当前尚未决定最终必须支持还是最终禁止”。

论文还反复强调 refinement 的直觉：精化就是把 `maybe` 行为删掉，或者把它升级成 `required`。可保守写成：

$$
M_1 \preceq M_2
$$

其含义是：

1. `M_1` 比 `M_2` 更具体、更少未定行为。
2. 通过 refinement 得到的最终“没有 maybe transitions 的模型”就是某个 implementation。

### 一个最小例子与通俗解释

论文一开始就给了一个 light switch 示例：

1. 开关一定会在 `on` 与 `off` 两种稳定模式之间交替。
2. 但当灯已经亮着时，是否允许再次 `on`，或灯已经灭时是否允许再次 `off`，可以先不定。
3. 在扩展 `FSP` 里，带 `?` 的动作用来表示这类 `maybe` 行为。
4. 之后随着需求变清晰，这些 `maybe` 行为可以被删掉，或者提升成 required。

通俗地说，`MTS` 像“给状态机多加了一层承诺等级”。普通 `FSM` 只能说“有这条边”或“没这条边”，而 `MTS` 还能说“这条边现在先保留为待定”。`MTSA` 则把这种待定行为的编写、合成和检查做成了真正可操作的插件。

### 运行 / 接受 / 转移语义

论文对 `MTS` model checking 给出三值结果。可保守写成：

$$
\mathrm{MC}(M,\varphi) \in \{\mathrm{true}, \mathrm{maybe}, \mathrm{false}\}
$$

上式中的符号逐项解释如下：

1. `M` 是待检查的 `MTS`。
2. `\varphi` 是待验证的 `FLTL` 性质。
3. `true` 表示所有 deadlock-free implementations 都满足该性质。
4. `false` 表示所有 implementations 都不满足该性质。
5. `maybe` 表示不同 implementations 的结果不一致。

论文还说明 `MTSA` 的 model checking 实现方式本质上是把 `MTS` 派生成两个 `LTS` 再调用 `LTSA` 核心去做检查。对部分行为合成，论文中有两类典型来源：

$$
\text{properties} \Rightarrow \text{upper bound MTS}
$$

$$
\text{scenarios} \Rightarrow \text{lower bound MTS}
$$

上式中的符号逐项解释如下：

1. 从 `FLTL` 约束合成得到的 `MTS` 提供行为上界，即不违反性质的所有候选行为。
2. 从 scenarios 合成得到的 `MTS` 提供行为下界，即至少应保留的示例行为。
3. 两者再通过 merge 组合，形成更接近真实系统的 partial model。

### 语义边界

这篇论文的边界也很清楚：

1. 它关注的是离散 partial behavior，而不是时间、连续变量或概率语义。
2. `MTS` 的价值在于早期不完整规格；如果需求已经完全定型，普通 `LTS/FSM` 就足够。
3. 工程载体主要是 Eclipse + `LTSA` core，而不是开放交换标准。
4. 其 synthesis 和 checking 都围绕软件行为规格，不涉及物理系统动力学。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `MTS` 骨架 | `$M = (S, Act, \to_{req}, \to_{may}, s_0)$` | 用 required / maybe 区分已定与未定行为。 |
| 一致性条件 | `$\to_{req} \subseteq \to_{may}$` | required 行为必须也是允许行为。 |
| refinement | `$M_1 \preceq M_2$` | 通过删减 `maybe` 或提升为 required 让模型更具体。 |
| 三值检查 | `$\mathrm{MC}(M,\varphi) \in \{\mathrm{true}, \mathrm{maybe}, \mathrm{false}\}$` | 针对 partial behavior 给出保守验证结论。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `MTS` 仍以离散状态为骨架。 |
| 事件 / 触发 | 很强 | 动作标签驱动状态转移。 |
| 守卫 / 数据 | 弱支持 | 主体在 partial behavior，不在复杂数据守卫。 |
| 层次 | 不支持 | 论文主线不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 支持 `CSP` 风格并行组合。 |
| 时间约束 | 不支持 | 不涉及 clock / delay。 |
| 连续动态 / 随机性 | 不支持 | 纯离散规格工作台。 |
| 可执行 / 可验证性 | 很强 | synthesis、merge、三值 checking 与 animation 都直接集成。 |

### 形式化问题与性质

1. `MTSA` 的关键优势不是单一算法，而是把 partial behavior 的多种操作集中到同一工作台。
2. 它把 `properties -> upper bound` 与 `scenarios -> lower bound` 这两条建模路径放在一起，再用 merge 汇合。
3. 对需求工程而言，三值结论比强行二值化更诚实，也更适合增量式精化。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 在 `FSP Editor` 中写扩展 `FSP`。
2. 用 `?` 标出待定动作。
3. 通过 toolbar 或 outline 编译得到 `MTS`。
4. 在 `Draw View`、`Animator View` 或 model-checking 输出中验证模型。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 扩展 `FSP` 文本模型。
2. `MTS Draw View` 中的图形表示。
3. scenarios 自动生成的 FSP/MTS。
4. `LTSA` core 接受的 `LTS` 派生表示。

### 交换与互操作

这篇论文的互操作重点不在中立标准，而在 Eclipse 内部协同：

1. `MTSA` 作为 Eclipse plug-in 与其他插件联动。
2. `LTSA` 核心类被复用到 checking 与 analysis。
3. `plugin.xml` 和多视图结构支持后续扩展新的 synthesis / analysis 功能。

## 配套基础设施

- 建模/编辑工具：`FSP Editor`、`Outline View`、`MTS Draw View`、`Animator View`。
- 解析/交换/元模型支持：扩展 `FSP` 文本解析与 Eclipse 插件视图；原文未给中立交换格式。
- 仿真/执行支持：`Animator View` 支持交互式行为走查。
- 验证/分析支持：三值 `FLTL` model checking、deadlock-freedom checking、merge、parallel composition、scenario/property synthesis。
- 代码生成/转换支持：原文未强调代码生成，重点是部分规格建模与验证。
- 标准化或社区生态：Eclipse PDE、`LTSA` core 与公开插件下载入口构成主要工程生态。

## 适用场景与需求前提

### 适用场景

适合需求早期尚不完整的软件行为规格、场景驱动建模、增量 refinement 和部分协议/组件行为分析。

### 需求前提

1. 需求主体仍是离散事件行为，而不是连续控制。
2. 团队愿意显式区分“已确定必须支持”和“暂时未定”的行为。
3. 可接受 `FSP` 风格的文本建模入口。
4. 需要在场景、性质和 partial models 之间反复迭代。

### 不适用或高成本场景

如果系统重点是 dense time、物理连续动力学或复杂数值守卫，这条 `MTS` 工具线就不是自然入口。

## 与相邻形式主义的关系

相对 [interface-automata/desc.md](../interface-automata/desc.md)，`MTS` 更强调 partial behavior 与 `may / required` 分层，而不是输入输出兼容本身；相对 [on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md](../on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md)，它更早、更偏 partial behavior synthesis，而 `MIO Workbench` 更聚焦 modal interface theory；相对 [ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md](../ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md)，它没有时间语义和 timed game machinery。

## 与本研究的关系

### 对 Project 1 的价值

它说明“需求到状态机”的过程中不一定要一步到位产出完全确定模型，中间可以保留 `may` 行为作为待定空间。

### 作为目标形式主义还是中间表示

更适合作为中间表示或需求侧精化工件，而不是最终交付给控制实现端的目标模型。

### 对需求到模型生成的启发

1. LLM 生成阶段可以先输出 partial behavior，而不是被迫对未说明行为拍脑袋补全。
2. 约束与场景可以分别给出行为上界和下界，再做 merge。
3. 修复阶段可以把“删掉某个 maybe”或“提升为 required”作为显式编辑动作。

### 现实限制

它主要解决的是离散软件规格的不完整性，不直接覆盖控制系统里常见的时钟、连续变量和混成语义。

## 重要的相关工作

- [interface-automata/desc.md](../interface-automata/desc.md)：更强调 I/O 兼容与替换性的接口自动机母线。
- [on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md](../on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md)：modal interface theory 的后续工程工作台。
- [ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md](../ecdar-an-environment-for-compositional-design-and-analysis-of-real-time-systems/desc.md)：把 timed interface theory 推到 dense-time game-based tool。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
