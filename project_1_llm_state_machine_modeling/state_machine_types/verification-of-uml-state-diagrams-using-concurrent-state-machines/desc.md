# 使用并发状态机验证 UML 状态图 / Verification of UML State Diagrams Using Concurrent State Machines

## 基本信息

- 标题：Verification of UML State Diagrams Using Concurrent State Machines
- 中文标题：使用并发状态机验证 UML 状态图
- 作者：Jerzy Mieścicki
- 发表：*Software Engineering Techniques: Design for Quality*，pp. 261-271，2007
- DOI：`10.1007/978-0-387-39388-9_25`
- 链接：https://doi.org/10.1007/978-0-387-39388-9_25
- 形式主义：`UML State Diagrams / Concurrent State Machines / COSMA`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`UML -> CSM / COSMA` 转换与多阶段模型检查路线
- 工具/实现获取方式：原文明确给出 `COSMA` 项目入口，并提到 `TempoRG`、`ECSM` 等同一环境下的分析模块。
- 标准/格式获取方式：输入是 `UML` state diagrams（计划从 `XMI` 自动转换）；中间承载是 `Concurrent State Machines`；性质检查使用 `QsCTL` 与 `COSMA` reachability / compression 链。

## 简报

这篇论文的主线不是发明新的 UML 语法，而是给 UML state diagrams 找一条适合并发通信系统的模型检查后端：`Concurrent State Machines (CSM)`。它的特别之处在于，不像很多路线把 UML 直接塞进 `Promela/SPIN`，这里作者强调的是 broadcast-style communication、同时事件发生、同时组件动作、以及 product graph 的多阶段压缩。

- 形式主义定位：`UML state diagrams -> CSM/COSMA` 的验证桥接与压缩分析路线。
- 构造方式简述：`UML state diagrams -> component CSMs -> CSM product -> multi-phase reduction -> QsCTL / counterexample`。
- 基础设施与场景简述：依托 `COSMA`、`TempoRG`、`ECSM` 与 stepwise product compression，适合 control-dominated、并发通信型 UML 行为模型。

```text
UML state diagrams -> concurrent state machines -> compressed product graph -> temporal-property check
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML state diagrams`。
2. `Concurrent State Machines (CSM)`。
3. CSM product。
4. multi-phase product compression。
5. `COSMA` 环境中的 `QsCTL` 性质检查。

### 核心抽象

论文直接给出 `CSM` 的核心元组：

$$
m = \langle N, edges, form, out, n_0 \rangle
$$

上式中的符号逐项解释如下：

1. `$N$` 是有限状态集合。
2. `$edges \subseteq N \times N$` 是有向边集合。
3. `$form$` 给边标注布尔公式。
4. `$out$` 给状态标注当前为真的原子命题集合。
5. `$n_0$` 是初始状态。

论文强调 CSM 的边不是用单个事件标签，而是用布尔公式标注，因此它天然支持“同时收到多种广播信号”的情形。机器必须 complete，也就是每个状态所有外出边公式的布尔和为 `1`。

整系统的组合则通过 product 给出。ATM-Bank 例子里，论文直接写出：

$$
System = User \otimes ATM \otimes BankMain \otimes VerC \otimes VerPIN
$$

而为了缓解爆炸，它又引入多阶段 product：

$$
Bank = BankMain \otimes VerC \otimes VerPIN
$$

$$
ATMandBank = ATM \otimes Bank
$$

$$
System = User \otimes ATMandBank
$$

这些等式的意义是：先算局部 product，再依据当前待验证性质只保留相关通信符号，压缩无关状态后再进入下一阶段组合。

### 一个最小例子与通俗解释

论文用 ATM-Bank 系统说明这条路线：

1. `ATM`、`BankMain`、`VerC`、`VerPIN` 都先被写成独立的 CSM。
2. 每个状态显式输出当前广播信号，例如 `VerifyPIN`、`PINVerified`、`Abort`。
3. 这些 CSM 再做 product，得到整个系统的并发行为图。
4. 若当前只关心“插卡后最终会取卡”或“插卡后最终会出钞”这类性质，就先把无关信号隐藏，再压缩图。

通俗地说，这条路线不是“把 UML 状态图直接扔给一个现成 model checker”，而是先把每个 UML 组件翻成一种更适合并发通信的状态机，再做按性质裁剪的 product 和压缩。

### 运行 / 接受 / 转移语义

论文的运行语义有两个关键点：

1. 输出附着在状态上，类似 Moore 风格，而不是 UML transition 上的 Mealy 风格。
2. 多个组件通过广播式原子命题通信，不预设单一输入字母或固定交错顺序。

因此，UML 到 CSM 的转换时需要：

1. 把某些 transition output 变成额外中间状态。
2. 为 composite states 拆出子 CSM，并用技术性同步符号在外层未激活时冻结它们。
3. 对 fork/join、junction、branch 等伪状态引入额外同步逻辑。

### 语义边界

1. 论文明确说 CSM 更适合 control-dominated systems。
2. 无限缓冲、动态对象创建 / 销毁与复杂数据都会破坏 finite-state 假设。
3. 文中主体还是基本 CSM，不是带富代码语义的 `ECSM`。
4. timed CSM 只被作为未来工作提到，本条目本身不是 timed verification 论文。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| CSM 骨架 | `$m=\langle N,edges,form,out,n_0\rangle$` | UML 行为后端对象。 |
| 广播并发组合 | `$System = User \otimes ATM \otimes BankMain \otimes VerC \otimes VerPIN$` | 全系统 product。 |
| 多阶段 product | `$Bank = BankMain \otimes VerC \otimes VerPIN$` 等 | 先局部组合再压缩。 |
| 逻辑检查 | `QsCTL` | 大图由 `COSMA` 模块做时序性质检查。 |
| 反例解释 | counterexample path | 若性质不成立，能回溯导致失败的路径。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕状态图与状态输出组织。 |
| 事件 / 触发 | 很强 | 原子命题广播与触发公式是主线。 |
| 守卫 / 数据 | 弱支持 | 简单数据可加，但富数据会放大 product。 |
| 层次 | 中等支持 | composite states 需拆成多个 CSM 并配技术同步。 |
| 并发 / 同步 | 很强 | CSM 的卖点就是并发组件和广播同步。 |
| 时间约束 | 弱支持 | 本文主体仍是 untimed CSM。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | `COSMA` + compression + `QsCTL` 全链路可用。 |

### 形式化问题与性质

1. 论文的关键贡献是说明 `UML -> CSM` 之后，product 不是只能一口气算完，还能按待验证性质分阶段压缩。
2. `COSMA` 路线强调“并发组件 + 广播符号 + 控制流 skeleton”的可检验性。
3. 对 `state_machine_types` 而言，它补的是 UML-state-diagram 向另一类 finite-state backend 的桥接，而不是再补一个 UML 语言本体节点。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 先有 `UML state diagrams`。
2. 再把每个 diagram 或 nested subdiagram 翻成独立 `CSM`。
3. 按需要构造局部 / 全局 product。
4. 最后在 `COSMA` 中做性质检查。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UML state diagrams`。
2. `CSM` labeled graphs。
3. partial / full product graphs。
4. `QsCTL` 性质与 counterexample traces。

### 交换与互操作

1. 论文明确提到目标是从 `XMI` 自动转换到 `CSM`。
2. `COSMA` 负责 product、compression 与性质检查。
3. `TempoRG` 用于时序模型检查，`ECSM` 则承担更接近执行级的扩展语义。

## 配套基础设施

- 建模/编辑工具：标准 UML CASE 工具。
- 解析/交换/元模型支持：计划中的 `XMI -> CSM` 转换模块。
- 仿真/执行支持：`COSMA` 的 product / graph exploration。
- 验证/分析支持：`QsCTL`、counterexample、multi-phase compression。
- 代码生成/转换支持：论文提到 MDA 背景，但本文主体是验证而非代码生成。
- 标准化或社区生态：`COSMA`、`TempoRG`、`ECSM` 与 UML/XMI 共同构成工具生态。

## 适用场景与需求前提

### 适用场景

适合并发通信型、控制流主导的 UML 行为模型，尤其是组件数较多、但关键性质只涉及少量通信符号的场景。

### 需求前提

1. 系统核心必须能有限状态化。
2. 组件交互要能表达成广播式或布尔公式约束。
3. 团队接受将 UML 输出语义改写为 state-output 风格的 `CSM`。
4. 对无限缓冲和动态进程创建没有刚性依赖。

### 不适用或高成本场景

若系统高度依赖富数据、动态对象生命周期或复杂真实时间约束，这条 untimed CSM 路线会变重甚至不适用。

## 与相邻形式主义的关系

它与常见的 `UML -> Promela/SPIN` 路线不同，更强调 broadcast-style concurrency 和 product compression。相对 `UML -> UPPAAL` 路线，它不是 timed backend；相对 `ECSM`，本文又停留在可 model-check 的控制流 skeleton 层。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提醒 `project_1`：UML 状态图并不只有一种“经典后端”，不同并发语义假设会把它导向不同 finite-state family。

### 作为目标形式主义还是中间表示

对 `project_1` 来说，`CSM` 更像某类 UML 并发语义的验证中间表示，而不是最终交付建模语言。

### 对需求到模型生成的启发

1. 若需求本身强调并发组件与广播交互，直接压成普通交错 `FSM` 可能损失结构信息。
2. “按性质裁剪 product 再继续组合”是应对大模型爆炸的实用思路。
3. UML 到后端的转换细节里，state-output / transition-output 差异不能忽略。

### 现实限制

论文自己也指出自动转换出来的 CSM 往往不够人类可读，因此这更像“形式后端”而不是新的人工建模前端。

## 重要的相关工作

1. 论文把 `vUML`、`Hugo` 等 UML verification 路线作为主要对照。
2. `COSMA` 的独特性在于 `CSM`、`TempoRG` 和 multi-phase compression 组合起来的并发控制流分析能力。
3. 文中还提到 `Timed CSM` 是后续方向，说明这条线未来有潜力继续接到 timed-family 上。

## 文献分类总结

- 这篇论文应归入：📦 标准、交换格式、元模型与执行载体
- 这篇论文应归入：🛠️ 方法路线
- 这篇论文应归入：🎛️ 控制 / 反应式逻辑
- 这篇论文应归入：💻 软件建模与程序行为
- 作为 `state_machine_types` 条目，它补的是 `UML state diagram -> CSM / COSMA` 的并发验证桥与多阶段压缩分析路线。
