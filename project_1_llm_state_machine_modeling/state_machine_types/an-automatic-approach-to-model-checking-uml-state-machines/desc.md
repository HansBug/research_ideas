# UML 状态机的自动模型检查方法 / An Automatic Approach to Model Checking UML State Machines

## 基本信息

- 标题：An Automatic Approach to Model Checking UML State Machines
- 中文标题：UML 状态机的自动模型检查方法
- 作者：Shao Jie Zhang，Yang Liu
- 发表：*2010 Fourth International Conference on Secure Software Integration and Reliability Improvement Companion*，pp. 1-6，2010
- DOI：`10.1109/ssiri-c.2010.11`
- 链接：https://doi.org/10.1109/ssiri-c.2010.11
- 形式主义：`UML State Machine / PAT / XMI-to-CSP#`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`UML` 状态机到 `PAT/CSP#` 的自动验证桥接方法
- 工具/实现获取方式：原文直接给出 `PAT` 入口 `http://www.patroot.com`，并说明实现成了 `PAT` 框架下的原型工具。
- 标准/格式获取方式：输入承载是 `XMI`，中间目标语言是 `CSP#`，前端对象是 `UML` state machine。

## 简报

这篇论文补的是 `UML State Machine` 在 `PAT` 生态里的自动验证桥。它把 UML 状态机自动翻译到 `CSP#`，从而接入 `PAT` 的 simulation、deadlock、reachability、`LTL`、fairness 和 trace refinement 能力，同时重点补齐了 fork、join、history、submachine、entry/exit point 这些很多早期方案常规避或弱处理的细节。

- 形式主义定位：`UML` 状态机的自动验证路线，而不是新的 UML 语言本体。
- 构造方式简述：从 `XMI` 读取 UML 模型，按状态/事件到 process/event 的映射规则翻译成 `CSP#`，再交给 `PAT` 验证。
- 基础设施与场景简述：依托 `XMI`、`PAT`、`CSP#` 和自动翻译规则，适合软件设计早期的 UML 动态行为验证。

```text
UML state machine (XMI) -> translation rules -> CSP# model -> PAT simulation / verification / refinement checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. UML state、transition 和 pseudo states。
2. `CSP#` process、event、channel 和 shared variable。
3. 自动翻译函数 `f: UML -> CSP#`。
4. fork/join/history/submachine 的专门翻译规则。
5. `PAT` 的 simulation / model checking / refinement checking 能力。

### 核心抽象

论文显式给出总翻译函数：

$$
f:\mathrm{UML} \to \mathrm{CSP\#}
$$

上式中的符号逐项解释如下：

1. `\mathrm{UML}` 表示输入的 UML 状态机模型。
2. `\mathrm{CSP\#}` 表示输出的 `PAT` 输入语言。
3. `f` 是整篇论文的中心对象，即自动翻译过程。

论文在基础翻译规则表中给出系统级组合骨架，可压成：

$$
f(system) = f(sm_1)\ |||\ f(sm_2)\ |||\ \cdots\ |||\ f(sm_n)
$$

上式中的符号逐项解释如下：

1. `sm_1,\ldots,sm_n` 是系统中的多个状态机。
2. `|||` 表示 `CSP#` 的 interleaving composition。
3. 该规则说明多个 UML state machines 会被翻成并行过程。

论文对 fork 的翻译给出一个非常具体的模板：

$$
P_S(i,j,k) = enter\_a\_state \to ((P_{r1}(i) ||| P_{r2}(j)) ||| P_{r3}(k))
$$

上式中的符号逐项解释如下：

1. `P_S(i,j,k)` 是复合状态 `S` 的参数化 `CSP#` 过程。
2. `i,j,k` 记录各 region 即将激活的目标状态。
3. `P_{r1}, P_{r2}, P_{r3}` 是不同 region 对应的子过程。
4. 该模板体现了 fork 会把控制同时分发到多个 region。
5. 这是论文正文直接给出的翻译样式。

submachine 的同步调用则被压成通道通信，例如：

$$
P_{S1}=e_1 \to ch!0 \to Skip,\quad P_{SM2}=ch?0 \to starting \to P_{S4}
$$

上式中的符号逐项解释如下：

1. `ch!0` 表示向被调用子状态机发送进入入口点的同步消息。
2. `ch?0` 表示被调用子状态机接收该消息并开始执行。
3. 这说明 submachine 在翻译后更像带同步通道的“子程序调用”。

### 一个最小例子与通俗解释

论文用 CD player 例子说明得很清楚：

1. `NONPLAYING` 里有 `CLOSED` 和 `OPEN` 等子状态。
2. 按下 `play`、`load` 等事件会触发不同转移。
3. 若存在 history state，就用一个共享变量记住上次活跃子状态。
4. 翻译后，原本图里的状态和事件都变成了 `CSP#` 的 process 与 event。

通俗地说，这条路线是把 UML 图“剥皮”成一个更适合模型检查器处理的过程代数模型，同时尽量不要求用户自己去学 `PAT` 语法。

### 运行 / 接受 / 转移语义

论文遵循的翻译直觉是：

1. 一个 UML state 对应一个 `CSP#` process。
2. 一个 event occurrence 对应一个 `CSP#` event。
3. composite state 会变成并行过程组合。
4. join 通过公共事件强制多个源状态同步退出。
5. history 用共享变量记录最近一次活跃子状态。

### 语义边界

边界同样明确：

1. 重点是自动验证路线，不是 UML 语义标准化母文。
2. 支持的是“较完整子集”，不是完整 UML 全语法。
3. 优势主要来自 `PAT` 后端，因此能力边界也受 `PAT/CSP#` 建模方式约束。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总翻译函数 | `$f:\mathrm{UML} \to \mathrm{CSP\#}$` | 自动把 UML 状态机送到 `PAT` 可处理的模型。 |
| 系统组合 | `$f(system)=f(sm_1) ||| \cdots ||| f(sm_n)$` | 多状态机被翻成并行过程。 |
| fork 模板 | `$P_S(i,j,k)=enter\_a\_state \to ((P_{r1}(i) ||| P_{r2}(j)) ||| P_{r3}(k))$` | fork 会并发激活多个 region。 |
| submachine 模板 | `$P_{S1}=e_1 \to ch!0 \to Skip$` | submachine 用同步通道表达“进入/返回”控制传递。 |
| 可验证性质 | safety / liveness / fairness / trace refinement | 翻译的意义是复用 `PAT` 的多类验证能力。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 主体就是 UML 状态机。 |
| 事件 / 触发 | 很强 | UML event 直接映射为 `CSP#` event。 |
| 守卫 / 数据 | 中等支持 | 通过 `CSP#` guard 和共享变量承载。 |
| 层次 | 很强 | composite、submachine、entry/exit point 都是重点。 |
| 并发 / 同步 | 很强 | fork/join、多 state machines 并行是核心亮点。 |
| 时间约束 | 弱支持 | 这篇不主打 timed UML。 |
| 连续动态 / 随机性 | 不支持 | 不在本文范围。 |
| 可执行 / 可验证性 | 很强 | `PAT` 提供 simulation、`LTL`、fairness 和 refinement checking。 |

### 形式化问题与性质

1. 论文的主问题是“如何自动、透明地把 UML 状态机送进成熟模型检查器”。
2. 相比许多更早方案，它强调减少显式辅助变量，从而缓解状态爆炸。
3. fork/join/history/submachine 的支持，使它在 `UML -> model checker` 路线里更接近工程图纸的真实复杂度。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 从 UML 工具导出 `XMI`。
2. 由原型读取 `XMI` 并解析 state machine。
3. 按翻译规则生成 `CSP#`。
4. 交给 `PAT` 做 simulation 和 verification。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `XMI`；
2. `CSP#` 过程代数模型；
3. `PAT` 的性质输入与验证结果。

### 交换与互操作

这篇论文的互操作重点在于：

1. 输入层不绑定具体 UML 建模器，而是绑定 `XMI`。
2. 语义桥接层是 `UML -> CSP#`。
3. 后端层复用 `PAT`，而不是重新实现模型检查器。

## 配套基础设施

- 建模/编辑工具：任意可导出 `XMI` 的 UML 工具。
- 解析/交换/元模型支持：`XMI` 作为输入交换格式。
- 仿真/执行支持：`PAT` simulator 支持 complete-state generation、random / interactive simulation 和 trace replay。
- 验证/分析支持：deadlock、reachability、trace refinement、`LTL` with fairness。
- 代码生成/转换支持：核心是 `XMI -> CSP#` 翻译。
- 标准化或社区生态：依附 UML `XMI` 与 `PAT` 工具生态。

## 适用场景与需求前提

### 适用场景

适合软件设计早期、对象行为建模、希望直接从 UML 图进入 formal verification 的场景。

### 需求前提

1. 行为逻辑已落成 UML state machines。
2. 模型位于论文支持的 UML 子集之内。
3. 团队接受通过 `PAT/CSP#` 做后端验证，而不要求保留纯 UML 前端语义的黑盒执行。

### 不适用或高成本场景

若需求高度依赖完整 UML 元模型、复杂对象结构或连续/概率扩展，这条路线就需要更多补充桥接。

## 与相邻形式主义的关系

相对 [a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md](../a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md)，那篇更偏 UML 直接语义完备化，而这里更偏自动翻译和工具接入；相对 [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)，两者都是验证桥，但一个接 `PAT/CSP#`，一个接 `mCRL2`；相对 [model-checking-timed-uml-state-machines-and-collaborations/desc.md](../model-checking-timed-uml-state-machines-and-collaborations/desc.md)，这里更强调一般 UML 行为特性而不是 timed collaboration。

## 与本研究的关系

### 对 Project 1 的价值

它说明 UML 状态机并不是只能停在图形前端；只要翻译链够稳，就能接到成熟 formal backend，并让复杂控制特性继续可检验。

### 作为目标形式主义还是中间表示

更像方法路线和验证桥，而不是最终目标形式主义。

### 对需求到模型生成的启发

1. 若未来 LLM 直接生成 UML 状态机，`XMI` 是很现实的机器交换入口。
2. 复杂 pseudo states 不能只停留在“画出来”，还要想清楚后端映射。
3. trace refinement 和 fairness 检查说明生成模型的验证需求可以比 safety 更丰富。

### 现实限制

这条路线证明了桥接可行，但并没有一次性解决完整 UML 的所有语义歧义。

## 重要的相关工作

1. [a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md](../a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md)：更完整的 UML 状态机直接语义化路线。
2. [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)：另一条 `UML -> formal backend` 桥接路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML 形式化与自动验证的综述总览。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 归类理由：主贡献是 `XMI -> CSP# -> PAT` 的自动验证桥接方法，以及对 fork/join/history/submachine 等复杂特性的翻译规则，而不是新的 UML 状态机本体。
