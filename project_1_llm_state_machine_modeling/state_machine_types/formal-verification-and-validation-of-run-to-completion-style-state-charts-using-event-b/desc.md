# 基于 Event-B 的 run-to-completion 状态图形式验证与确认 / Formal verification and validation of run-to-completion style state charts using Event-B

## 基本信息

- 标题：Formal verification and validation of run-to-completion style state charts using Event-B
- 中文标题：基于 Event-B 的 run-to-completion 状态图形式验证与确认
- 作者：K. Morris，C. Snook，T. S. Hoang，G. Hulette，R. Armstrong，M. Butler
- 发表：*Innovations in Systems and Software Engineering*，18(4):523-541，2022
- DOI：`10.1007/s11334-021-00416-4`
- 链接：https://doi.org/10.1007/s11334-021-00416-4
- 形式主义：`run-to-completion State charts / SCXML / UML-B / Event-B`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`SCXML/UML-B -> Event-B` 精化、动画与性质验证路线
- 工具/实现获取方式：论文明确说明存在自动 `SCXML -> UML-B` 翻译工具，基于 `EMF` 与 `Sirius`；后续依托 `Rodin`、`UML-B` translation、`ProB` 与 `Scenario Checker` 工作。
- 标准/格式获取方式：输入是 `SCXML` state chart；中间承载是 `UML-B` state machine 与 `Event-B` machine/context；验证侧使用 invariant proof、`LTL` model checking 与 scenario replay。

## 简报

这篇论文的关键价值不在于重新提出一种新的状态图语言，而在于把带 `run-to-completion` 语义的 state charts 真正接进 `Event-B` 的精化、证明和动画链。它解决的是一个很具体但也很难绕开的工程问题：`SCXML` 这类 reactive state chart 在执行上强调 trigger queue、macro-step、internal / external trigger 优先级，而 `Event-B` 天生是异步事件系统，直接映射会把很多精化和活性结论搞坏。

- 形式主义定位：`SCXML / state chart` 到 `Event-B` 的验证桥接与精化方法路线。
- 构造方式简述：`SCXML -> run-to-completion basis -> transition-combination events -> UML-B -> Event-B -> proof / scenario / LTL check`。
- 基础设施与场景简述：依托 `Rodin`、`UML-B`、`ProB`、`Scenario Checker` 与自动翻译器，服务安全关键 reactive controller 的分层验证。

```text
SCXML state chart -> run-to-completion basis -> UML-B state machine -> Event-B refinement -> proof / animation / model checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `run-to-completion` 风格的 state chart。
2. `SCXML` trigger queues 与 macro-step / micro-step 语义。
3. `UML-B` state machine。
4. `Event-B` machine/context 与 refinement proof obligations。
5. `Scenario Checker`、`ProB` 和 `LTL` model checking。

### 核心抽象

论文把 run-to-completion 抽象成一套基础状态变量，核心可保守压缩为：

$$
B = (iQ, eQ, dt, uc)
$$

上式中的符号逐项解释如下：

1. `$iQ$` 是 internal trigger queue。
2. `$eQ$` 是 external trigger queue。
3. `$dt$` 是当前 de-queued trigger。
4. `$uc$` 是 run-to-completion completion flag。

论文强调 trigger queue 不是集合，而是序列，因此基础上下文中需要：

$$
\mathrm{Seq}(SCXML\_TRIGGER)
$$

这表示全部可能 trigger 序列的集合。作者明确说明这一步是为了把 trigger consumption fairness 内建进模型，而不再像旧版本那样只靠额外 fairness 假设。

安全性质则被写成 Event-B invariant。对 state `S` 中应保持的性质 `P`，核心形态是：

$$
S = TRUE \Rightarrow P'
$$

其中 `$P'$` 是经过 run-to-completion 语义修正后的性质，即允许“触发反应已经在内部队列里或正在处理中，但退出动作还未完成”的瞬时过渡。

论文在活性部分给出终止内部反应的目标：

$$
GF(iQ=\emptyset \land uc=TRUE \land dt=\emptyset)
$$

上式中的符号逐项解释如下：

1. `$iQ=\emptyset$` 表示内部触发队列清空。
2. `$uc=TRUE$` 表示当前 macro-step 已完成。
3. `$dt=\emptyset$` 表示当前没有待消费 trigger。
4. 整体表示系统总能回到“ready to dequeue”状态。

### 一个最小例子与通俗解释

论文的 drone 例子最能说明这条路线：

1. 无人机在 `TAKEOFF` 或 `FLY` 时，电量监控并行 region 会持续判断 `BATTERYOK / BATTERYLOW`。
2. 当 charge 下降到阈值以下时，state chart 需要自动 raise 内部 trigger `toLand`。
3. 论文先在 `SCXML` 层给出该 run-to-completion 行为，再翻到 `UML-B / Event-B`。
4. 随后用 invariant 证明“低电量时不允许继续飞行”，再用 scenario replay 检查不同 refinement level 的期望响应。

通俗地说，这篇论文相当于给 state chart 加了一层“严肃数学地基”：trigger queue、完成标志、完成条件都变成了可证明、可回放、可检查的显式对象。

### 运行 / 接受 / 转移语义

论文区分了：

1. `micro-step`：单次 transition firing。
2. `macro-step`：从 dequeue 外部触发开始，到整个 run-to-completion 完成为止的完整反应过程。

基础机器中的关键操作包括：

1. `dequeueExternalTriggered`
2. `dequeueInternalTriggered`
3. `futureTriggeredTransitionSet`
4. `futureUntriggeredTransitionSet`
5. `noTriggeredTransitionsEnabled`
6. `noUntriggeredTransitionsEnabled`

这说明作者不是把 state chart 一步翻成一个普通状态机，而是先翻成一套“显式维护 trigger queue 与 completion 的事件系统基座”，然后再把具体模型精化上去。

### 语义边界

1. 论文主体关注的是 `run-to-completion` 风格的 state charts，而不是任意 UML / statechart 变体。
2. `SCXML` 精化依赖若干受控规则，不能任意交叉 containment boundary。
3. 活性部分仍需要 fairness / convergence reasoning，不是只靠 invariant preservation 自动得到。
4. 这条路线更像“state chart verification bridge”，不是工业部署运行时本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础运行时骨架 | `$B=(iQ,eQ,dt,uc)$` | 显式建模 run-to-completion 语义。 |
| trigger queue | `$\mathrm{Seq}(SCXML\_TRIGGER)$` | 把 trigger queue 建成序列而不是集合。 |
| 安全 invariant | `$S=TRUE \Rightarrow P'$` | 在 run-to-completion 稳定点上检查状态性质。 |
| 内部反应终止 | `$GF(iQ=\emptyset \land uc=TRUE \land dt=\emptyset)$` | 系统总能回到 ready-to-dequeue 状态。 |
| 外部 trigger 响应 | `$G([externalTrigger.t] \Rightarrow F([dequeueExternalTriggered.t]))$` | 外部触发最终会被取出处理。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 state charts / UML-B state machine 展开。 |
| 事件 / 触发 | 很强 | internal/external trigger queue 是核心对象。 |
| 守卫 / 数据 | 中等支持 | 通过 Event-B guards / invariants 表达。 |
| 层次 | 强支持 | refinement 与嵌套 state chart 都是主线。 |
| 并发 / 同步 | 中等支持 | 并行 region 会被组合成共同事件。 |
| 时间约束 | 弱支持 | 重点不是 clocks，而是 run-to-completion reactive semantics。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | proof、Scenario Checker、`LTL` model checking 都落地了。 |

### 形式化问题与性质

1. 论文补的是 `state chart -> proof-oriented formal method` 之间最缺的那层执行语义桥。
2. 它把“trigger queues、completion flag、future triggers”做成 refinement-safe 的 basis，因此能在抽象层先证明安全性质。
3. 对 `state_machine_types` 文库来说，这类论文不长主树新节点，但非常适合补 `SCXML / state chart -> Event-B` 的静态挂接口径。

## 构造方式与承载格式

### 建模入口

论文明确的输入链路是：

1. 写 `SCXML` 源模型。
2. 在模型中写 refinement annotations。
3. 自动生成 `UML-B` state machine。
4. 再调用标准 `UML-B` translator 生成 `Event-B`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `SCXML`。
2. `UML-B` state machine。
3. `Event-B` contexts / machines。
4. `LTL` properties 与 scenario traces。

### 交换与互操作

1. `SCXML -> UML-B -> Event-B` 是论文主干。
2. `ProB` 负责动画、约束求解与 model checking。
3. `Scenario Checker` 用于场景录制和回放，帮助在 refinement 过程中做行为确认。

## 配套基础设施

- 建模/编辑工具：`SCXML` 编辑环境、`EMF`、`Sirius`。
- 解析/交换/元模型支持：自动 `SCXML -> UML-B` translator 与标准 `UML-B -> Event-B` translation。
- 仿真/执行支持：`Scenario Checker`、`ProB` 动画。
- 验证/分析支持：`Rodin` theorem provers、invariant proof、`LTL` model checking。
- 代码生成/转换支持：主体不是代码生成，但保留了由高层模型到 formal backend 的稳定翻译链。
- 标准化或社区生态：依托 `SCXML`、`UML-B`、`Event-B` 与 `Rodin / ProB` 生态。

## 适用场景与需求前提

### 适用场景

适合安全关键 reactive controller，尤其是已经采用 `SCXML` / state chart 建模、同时又希望在抽象层做 proof-driven refinement 的团队。

### 需求前提

1. 模型必须是 `run-to-completion` 风格。
2. 团队需要接受 trigger queue、completion flag 等执行细节显式化。
3. 关键安全性质最好能写成 state invariants，行为要求则能转成 `LTL` 或 scenario。
4. refinement 结构要受论文规定的规则约束。

### 不适用或高成本场景

若团队只关心纯仿真、完全不做 refinement proof，或者模型依赖大量本文未覆盖的复杂 statechart 扩展，这条路线会显得过重。

## 与相邻形式主义的关系

它介于 `SCXML / state chart` 前端和 `Event-B` 证明后端之间。相对直接做 statechart model checking 的路线，它多了一层 refinement discipline；相对纯 `Event-B` 事件系统建模，它又保留了工程师更熟悉的 state chart 前端。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果 `project_1` 想把需求侧图形状态图接入形式证明链，不必一开始就抛弃 state chart 前端，而可以通过桥接把它们压到 `Event-B`。

### 作为目标形式主义还是中间表示

对 `project_1` 来说，`SCXML / state chart` 更像前端需求与设计表示，`Event-B` 更像验证中间表示与证明载体。

### 对需求到模型生成的启发

1. `run-to-completion` 的队列语义必须显式建模，否则后续 proof 会失真。
2. 生成 state chart 时最好同步生成 refinement annotations 与 future-trigger discipline，而不是事后再补。
3. 需求验证不应只靠动画，人机可读前端后面最好接 proof obligations。

### 现实限制

论文依赖专门的翻译链与建模纪律，因此不适合拿来当“任何 statechart 都能即插即用验证”的通用答案。

## 重要的相关工作

1. `UML-B`：为 `Event-B` 提供图形 state machine front-end，是本文桥接的重要基础。
2. `ProB` 与 `Scenario Checker`：把纯证明链补成了“可动画、可回放、可调试”的验证闭环。
3. 论文也明确承认 `SCXML` 自身没有 refinement 概念，因此真正的新意在“state chart 精化规则 + Event-B 承接”。

## 文献分类总结

- 这篇论文应归入：📦 标准、交换格式、元模型与执行载体
- 这篇论文应归入：🛠️ 方法路线
- 这篇论文应归入：🎛️ 控制 / 反应式逻辑
- 这篇论文应归入：💻 软件建模与程序行为
- 作为 `state_machine_types` 条目，它补的是 `SCXML / state chart -> Event-B` 的形式验证与场景确认桥接路线。
