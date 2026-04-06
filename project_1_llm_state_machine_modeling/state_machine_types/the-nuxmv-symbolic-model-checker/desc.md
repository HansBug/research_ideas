# nuXmv：符号模型检查器 / The nuXmv Symbolic Model Checker

## 基本信息

- 标题：The nuXmv Symbolic Model Checker
- 中文标题：nuXmv：符号模型检查器
- 作者：Roberto Cavada，Alessandro Cimatti，Michele Dorigatti，Alberto Griggio，Alessandro Mariotti，Andrea Micheli，Sergio Mover，Marco Roveri，Stefano Tonetta
- 发表：*Computer Aided Verification (CAV 2014)*，pp. 334-342，2014
- DOI：`10.1007/978-3-319-08867-9_22`
- 链接：https://doi.org/10.1007/978-3-319-08867-9_22
- 形式主义：`Synchronous Transition Systems / nuXmv`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：finite / infinite-state symbolic model checker and `SMT`-enabled verification backend
- 工具/实现获取方式：原文明确说明 `NUXMV` 可从 `https://nuxmv.fbk.eu` 下载。
- 标准/格式获取方式：原文说明 `nuXmv` 延续 `NuSMV` 语言，同时新增 `Reals`、unbounded `Integers`、`AIGER` 输入，以及 `XMI` 显式状态导出；它是工具链承载，不是独立标准。

## 简报

这篇论文的重点，是把传统 `NuSMV` 从“主要面向有限布尔状态的 BDD/SAT 模型检查器”推进成“既能处理有限状态，也能处理带整数与实数的无限状态同步转移系统”的统一平台。`nuXmv` 的工程核心有两条：一条是继续补强 finite-state 侧的 `BDD/SAT/IC3` 验证能力，另一条是用 `SMT`、interpolation、`k`-induction、IC3 和 abstraction-refinement 把 infinite-state checking 真的接进主工具链。

- 形式主义定位：同步转移系统的符号验证平台，而不是新的状态机母型。
- 构造方式简述：系统继续用 `NuSMV` 风格变量、`INIT / TRANS / next` 语法描述，再由 `BDD/SAT/SMT` 后端做 invariants、`LTL`、BMC、IC3 与 abstraction-refinement。
- 基础设施与场景简述：依托 `CUDD`、`MiniSAT`、`MathSAT5`、`AIGER`、`XMI` 和 monitor-based property translation，服务硬件、软件、需求分析和各种把同步状态逻辑压成 transition system 的验证场景。

```text
NuSMV-style synchronous model -> Boolean / SMT encodings -> BMC / k-induction / IC3 / interpolation / abstraction-refinement -> proof or counterexample
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. finite- and infinite-state synchronous transition systems；
2. `NuSMV` 语言及其 `INIT / TRANS / next` 骨架；
3. `BDD / SAT / SMT` verification engines；
4. `AIGER` 与 `XMI` 等承载格式；
5. invariant、`LTL`、IC3、CEGAR 与 interpolation-based checking。

### 核心抽象

对 `nuXmv` 可保守写成一个公平同步转移系统：

$$ M = (V, I(V), T(V,V'), F) $$

上式中的符号逐项解释如下：

1. `V` 是状态变量集合，可含布尔、标量、整数和实数。
2. `I(V)` 是初始条件。
3. `T(V,V')` 是从当前状态到下一状态的同步转移关系。
4. `F` 是公平性约束集合。
5. 论文开头明确把 `nuXmv` 定位为 “finite- and infinite-state synchronous transition systems” 的符号模型检查器。

当系统含输入变量和下一状态更新时，单步执行可保守写成：

$$ s' \models T(s,s') $$

上式中的符号逐项解释如下：

1. `s` 是当前状态赋值。
2. `s'` 是下一状态赋值。
3. `T` 由 `TRANS` 与 `next(x)` 这类语句共同定义。
4. 因为系统是同步的，所以一个时钟步里所有变量一起更新。

对有界模型检查，论文继续沿用标准路径编码，可整理为：

$$ I(s_0) \land \bigwedge_{0 \le i < k} T(s_i,s_{i+1}) \land \neg \varphi_k $$

上式中的符号逐项解释如下：

1. `s_0,\ldots,s_k` 是长度为 `k` 的路径。
2. `I(s_0)` 要求路径从初始状态出发。
3. `T(s_i,s_{i+1})` 约束每一步都满足系统转移关系。
4. `\varphi_k` 是在第 `k` 步检查的性质实例。
5. 论文说明 `nuXmv` 把 `SBMC`、interpolation、`k`-induction 与 IC3 都扩到了 `SMT` 场景。

### 一个最小例子与通俗解释

论文第一页就给了一个最小例子：

1. 离散状态变量 `state` 在 `s0`、`s1` 之间切换。
2. 连续变量 `res` 是非负实数。
3. 在 `s0` 中每步增加 `d`，且 `0 \le d \le 0.01`；在 `s1` 中每步增加 `d`，且 `0 \le d \le 0.02`。
4. 性质写成 `INVARSPEC res <= 0.3`。

通俗地说，这个例子展示了 `nuXmv` 的关键扩展：以前只能把系统压成有限布尔机，现在可以直接把“离散模式 + 实数/整数变量 + 约束更新”一起交给同一套模型检查工具。

### 运行 / 接受 / 转移语义

若采用论文中的 monitor-based `LTL` 处理，可保守整理为：

$$ M \models \varphi \iff M \parallel Mon(\neg \varphi) \models \text{no-bad-state} $$

上式中的符号逐项解释如下：

1. `M` 是原系统。
2. `\varphi` 是待验证的 `LTL` 性质。
3. `Mon(\neg \varphi)` 是把性质否定转成监视器后的附加同步组件。
4. “no-bad-state” 表示坏状态不可达。
5. 论文明确说对含 input / next 的性质，内部是通过增加 monitor 来复用既有验证引擎。

对 invariant checking，则可直接写成：

$$ Reach(M) \subseteq \{\, s \mid p(s) \,\} $$

上式中的符号逐项解释如下：

1. `Reach(M)` 是系统所有可达状态集合。
2. `p(s)` 是状态 `s` 上的 invariant predicate。
3. 若可达状态全集都满足 `p`，则 invariant 成立。
4. 论文中的 `INVARSPEC res <= 0.3` 就是这种最小例子。

### 语义边界

1. `nuXmv` 处理的是同步转移系统，不是层次状态机语言本体。
2. `SMT` 扩展使它能处理无限状态，但很多方法在一般情形下并非总是完备。
3. 原文确实提到 hybrid-system extensions，但本文主对象仍是 symbolic model checker 本体。
4. 它提供 `XMI` 导出与 `AIGER` 导入，但这不是通用模型交换标准，而是围绕验证任务的工程承载。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 同步转移系统 | `$M = (V, I(V), T(V,V'), F)$` | `nuXmv` 的核心对象是 finite / infinite-state synchronous transition systems。 |
| 单步语义 | `$s' \models T(s,s')$` | `TRANS / next` 语句定义同步更新。 |
| BMC 路径编码 | `$I(s_0) \land \bigwedge_{i<k} T(s_i,s_{i+1}) \land \neg \varphi_k$` | `SAT/SMT` 后端的基础工作形态。 |
| monitor 化性质检查 | `$M \models \varphi \iff M \parallel Mon(\neg \varphi) \models \text{no-bad-state}$` | 原文对 input / next references 的处理方式。 |
| invariant 检查 | `$Reach(M) \subseteq \{s \mid p(s)\}$` | `INVARSPEC` 的本质。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 明确面向同步 transition systems。 |
| 事件 / 触发 | 中等支持 | 更偏同步状态更新而非显式消息端口。 |
| 守卫 / 数据 | 很强 | 支持布尔、标量、整数、实数以及 `SMT` 推理。 |
| 层次 | 不支持 | 不是层次状态图工具。 |
| 并发 / 同步 | 强 | 同步更新语义天然适合硬件和同步控制逻辑。 |
| 时间约束 | 间接支持 | 可借 `Reals/Integers` 编码部分时序，但不是专用 timed-automata 平台。 |
| 连续动态 / 随机性 | 弱支持 | 主线不是一般连续动力学或概率语义。 |
| 可执行 / 可验证性 | 很强 | `BDD/SAT/SMT/IC3/CEGAR` 都已工程化。 |

### 形式化问题与性质

1. `nuXmv` 的核心突破，是把有限状态 symbolic model checking 与 infinite-state `SMT` checking 放进同一代码基。
2. 它并不重定义“状态机是什么”，而是重构“同一状态机怎样被 `BDD/SAT/SMT` 多路消费”。
3. `AIGER`、`XMI`、monitor translation 和 model transformations 一起说明它是典型的验证型基础设施条目。

## 构造方式与承载格式

### 建模入口

原文给出的主要入口有：

1. `NuSMV` 语言本体；
2. `AIGER` 输入；
3. 通过输入 / next references 扩展的性质描述；
4. 对外部 IC3 executable 与 `SMT` solvers 的接口。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `INIT / TRANS / next` 风格同步状态机描述；
2. `BDD` / `SAT` / `SMT` 内部编码；
3. `AIGER`；
4. 投影后导出的 `XMI` 显式状态表示。

### 交换与互操作

互操作重点不在中立标准，而在验证桥：

1. `AIGER` 允许与硬件 model-checking competition 生态对接。
2. `XMI` 导出允许用 `UML` viewer 看显式状态表示。
3. `MathSAT5` 等 `SMT` interface 让 infinite-state 算法真正落地。

## 配套基础设施

- 建模/编辑工具：主体沿用 `NuSMV` 文本建模方式，不是图形前端。
- 解析/交换/元模型支持：`NuSMV` parser、`AIGER` import、`XMI` export。
- 仿真/执行支持：核心是验证，不是运行时执行平台。
- 验证/分析支持：`BDD`-based checking、`SAT`-based BMC、`SMT`-based invariant / `LTL` checking、IC3、interpolation、`k`-induction、CEGAR。
- 代码生成/转换支持：支持模型 transformation、monitor insertion、AIGER trace 回转。
- 标准化或社区生态：`nuXmv` 站点、`CUDD`、`MiniSAT`、`MathSAT5`、`AIGER` 共同构成符号验证生态。

## 适用场景与需求前提

### 适用场景

适合硬件、嵌入式软件、同步控制逻辑、需求监视器和一般可以压成同步 transition systems 的验证场景，尤其适合既要 finite-state symbolic checking，又要 infinite-state `SMT` reasoning 的任务。

### 需求前提

1. 系统最好能写成同步更新的 transition relation。
2. 若使用无限状态能力，性质与模型需要适配 `SMT` 背景理论。
3. 团队愿意接受文本化模型与符号验证工作流。
4. 关注点主要是 invariants、`LTL`、安全性、可达性与抽象精化。

### 不适用或高成本场景

如果需求主要是 timed-automata clocks、层次状态图可视化或连续微分方程语义，`nuXmv` 就不是最直接的主入口。

## 与相邻形式主义的关系

相对 [pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md](../pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md)，`PAT 3` 更偏多领域插件式架构，而 `nuXmv` 更偏单一 symbolic core 的极致扩展；相对 [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)，后者是 `xUML` 到外部后端的桥，而本文是后端本体；相对 [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)，`PRISM` 主打概率模型，而 `nuXmv` 主打同步符号转移系统。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明如果后续 `project_1` 要选一种“广谱验证后端”，同步 transition-system 语义仍然极具工程价值。
2. `nuXmv` 提醒我们：对富数据需求，不一定非得先降到纯有限状态，也可以保留整数/实数并直接走 `SMT` 验证。
3. 对“生成-验证-修复”闭环来说，`monitor translation`、abstraction-refinement 和 counterexample 机制都很值得借鉴。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像后端验证平台，而不是最终面向用户的状态机表达语言。

## 重要的相关工作

- [pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md](../pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md)：可对照多领域模型检查器架构。
- [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)：另一类主流 symbolic verification platform。
- [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)：可执行状态机经翻译接验证后端的现有条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这是一篇典型的 symbolic verification infrastructure 条目，适合作为 `NuSMV -> nuXmv` 演化、finite/infinite-state 同平台验证与 `SMT`-enabled transition-system checking 的基础设施证据入账。
