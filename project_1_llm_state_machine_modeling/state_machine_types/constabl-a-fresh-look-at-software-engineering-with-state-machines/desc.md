# ConStaBL：重新审视以状态机为核心的软件工程 / ConStaBL - A Fresh Look at Software Engineering with State Machines

## 基本信息

- 标题：ConStaBL - A Fresh Look at Software Engineering with State Machines
- 中文标题：ConStaBL：重新审视以状态机为核心的软件工程
- 作者：Karthika Venkatesan，Sujit Kumar Chakrabarti
- 发表：*CoRR / arXiv*，2023
- DOI：`10.48550/arXiv.2307.03790`
- 链接：https://doi.org/10.48550/arXiv.2307.03790
- 形式主义：`ConStaBL / concurrent statecharts with local variables`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：executable-statechart semantics / simulator / fuzz-testing route
- 工具/实现获取方式：原文说明作者实现了 `ConStaBL` simulator，并给出 fuzzing workflow 与配套仓库引用，但正文没有提供稳定的软件发布页；可直接依据论文语义和文中引用的代码仓库线索继续追踪。
- 标准/格式获取方式：原文给出 `ConStaBL` 的抽象语法、状态/迁移元组、结构语义和可执行仿真算法，但未定义独立 XML / JSON 交换标准。

## 简报

这篇论文的重要性不在于再讲一次一般 statecharts，而在于把“带局部变量、允许并发区域、又不依赖外部优先级打补丁”的状态图语义收得更紧，并把语义直接写成可执行 simulation algorithm。它一方面把 `Statecharts` 的本体语义落到更清楚的代码级并发解释上，另一方面又把 simulator 直接接到 fuzz testing，使状态图不只是设计文档，而是可执行、可测、可找 bug 的工程载体。

- 形式主义定位：一种带 local variables 的 concurrent statechart 变体，以及围绕它的可执行语义和测试方法。
- 构造方式简述：先定义状态、迁移、配置树、source/destination code tree，再把 enabled transitions 的代码组合成顺序/并发混合结构，由 simulator 逐语句交错执行。
- 基础设施与场景简述：依托抽象语法、CFG、code containment tree、simulator 和 `Jazzer` fuzzing，适合把复杂反应式逻辑先建成可执行状态图，再做早期缺陷暴露。

```text
reactive requirements -> ConStaBL statechart + local variables -> executable simulation semantics -> trace / conflict detection / fuzz testing
```

## 形式主义定义与核心对象

### 定义对象

论文把 `ConStaBL` 明确组织成三类核心对象：

1. 状态集合 `S`。
2. 迁移集合 `T`。
3. 事件集合 `E`。

在此基础上，再通过配置树、状态包含树、代码树和控制流图来定义一轮 simulation step 内应执行的代码。

### 核心抽象

原文直接给出状态元组与迁移元组。单个状态可写为：

$$
s = (p, I, V_l, V_p, V_s, a_N, a_X, \tau)
$$

上式中的符号逐项解释如下：

1. `p` 是父状态。
2. `I` 是默认或初始子状态集合。
3. `V_l` 是 local variables。
4. `V_p` 是 parameter variables。
5. `V_s` 是 static variables。
6. `a_N` 是 entry action。
7. `a_X` 是 exit action。
8. `\tau \in \{\mathrm{statechart}, \mathrm{atomic}, \mathrm{composite}, \mathrm{shell}\}` 是状态类型。

迁移被定义为：

$$
t = (p, s, d, e, g, a)
$$

上式中的符号逐项解释如下：

1. `p` 是迁移所在父状态。
2. `s` 是源状态。
3. `d` 是目标状态。
4. `e` 是触发事件。
5. `g` 是 guard。
6. `a` 是迁移动作代码。

在给定配置 `C` 和事件 `e` 时，论文把 enabled transition 的条件压成三条：

$$
t \text{ is enabled in } (C,e) \iff t.s \in CST(C)\ \land\ t.e=e\ \land\ \sigma \vdash t.g \Downarrow \mathrm{true}
$$

上式中的符号逐项解释如下：

1. `CST(C)` 是配置 `C` 的 configuration state tree 中出现的状态集合。
2. `\sigma` 是当前变量值环境。
3. `\vdash t.g \Downarrow \mathrm{true}` 表示 guard 在当前环境下求值为真。

论文进一步把一组已启用迁移的执行代码写成并发组合。对某个迁移 `t`，其执行代码写为：

$$
\mathrm{Code}(t,C)=\mathrm{Seq}([\mathrm{C_s}(t,C),\ \mathrm{cfg}(t.a),\ \mathrm{C_d}(t,C)])
$$

上式中的符号逐项解释如下：

1. `\mathrm{C_s}(t,C)` 是源侧 exit code tree 展开的顺序代码。
2. `\mathrm{cfg}(t.a)` 是迁移动作 `a` 的控制流图。
3. `\mathrm{C_d}(t,C)` 是目标侧 entry / initialization code tree 展开的代码。
4. `\mathrm{Seq}` 表示顺序组合。

若当前启用迁移集合是 `T=\{t_1,\ldots,t_n\}`，则整轮执行代码为：

$$
\mathrm{C}(T) = [\mathrm{C}(t_1,C)\ |\ \mathrm{C}(t_2,C)\ |\ \cdots\ |\ \mathrm{C}(t_n,C)]
$$

上式中的符号逐项解释如下：

1. `[\cdot|\cdot]` 表示并发组合。
2. 每个分支对应一条 enabled transition 的源侧代码、动作代码和目标侧代码。
3. simulator 在并发组合内部允许语句级任意交错，但单条指令仍原子执行。

### 一个最小例子与通俗解释

论文在示例图里给了一个最小并发场景：当前配置是 `{A,C}`，事件 `e1` 到来后，`tAB` 和 `tCD` 同时可触发。

1. `tAB` 需要退出 `A`，执行 `tAB.a`，再进入 `B`。
2. `tCD` 需要退出 `C`，执行 `tCD.a`，再进入 `D`。
3. simulator 先为两条迁移分别构造代码树，再把两棵树并发组合。
4. 随后代码不是按固定 region 顺序执行，而是允许指令级交错。

通俗地说，`ConStaBL` 像“把 statechart 一次跳转时到底要执行哪些 exit / transition / entry 代码，拆开后放到一个可并发调度的小执行机里”。它比普通状态机多出来的，不只是 hierarchy 和并发区域，而是明确规定了并发代码如何交错、什么时候算冲突、什么时候一轮仿真是合法的。

### 运行 / 接受 / 转移语义

这篇论文的语义重点不是语言接受，而是 simulation step 的构造与合法性。原文显式定义了冲突：

$$
\mathrm{conflict}(t_1,t_2)=\mathrm{true}\ \text{if}\ \mathrm{C}(t_1,C)\cap \mathrm{C}(t_2,C)\neq \varnothing
$$

上式中的符号逐项解释如下：

1. `\mathrm{C}(t_1,C)` 和 `\mathrm{C}(t_2,C)` 是两条迁移在配置 `C` 下对应的代码块集合。
2. 若两条迁移会导致某些代码块重复执行，则它们冲突。
3. 这里的交集是“代码块集合”的交集，而不是字符串文本相同。

基于此，论文给出有效仿真的核心约束：

$$
\text{valid simulation step} \Rightarrow \text{each code block executes at most once}
$$

上式中的符号逐项解释如下：

1. “valid simulation step” 指当前事件下允许真正执行的一轮状态图仿真。
2. 它禁止靠额外优先级规则悄悄解决冲突。
3. 若某代码块会被重复执行，则该组 enabled transitions 不能同时作为合法执行集。

### 语义边界

1. 论文聚焦的是 `ConStaBL` 这一路 statechart 语义，不等于覆盖所有 `UML / SCXML / Yakindu / Stateflow` 变体。
2. 它刻意拒绝通过外部优先级规则隐式解决 ancestor-descendant 或 orthogonal-region 冲突。
3. 并发代码只允许语句级任意交错，不继续细化到表达式级或内存模型级竞争。
4. 价值重点在 executable semantics、simulator 和 fuzz testing，不是工业代码生成。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 状态元组 | `$s = (p, I, V_l, V_p, V_s, a_N, a_X, \tau)$` | 固定了带局部变量和 entry/exit 动作的状态骨架。 |
| 迁移元组 | `$t = (p, s, d, e, g, a)$` | 固定了事件、guard 和动作级转移对象。 |
| 启用条件 | `$t.s \in CST(C) \land t.e=e \land \sigma \vdash t.g \Downarrow true$` | 说明 transition fire 由配置、事件和 guard 共同决定。 |
| 转移代码 | `$\mathrm{Code}(t,C)=\mathrm{Seq}([\mathrm{C_s}(t,C),\mathrm{cfg}(t.a),\mathrm{C_d}(t,C)])$` | 把一次跳转拆成 exit / action / entry 代码三段。 |
| 并发组合 | `$\mathrm{C}(T)=[\mathrm{C}(t_1,C)|\cdots|\mathrm{C}(t_n,C)]$` | enabled transitions 可以并发进入统一执行器。 |
| 冲突判定 | `$\mathrm{C}(t_1,C)\cap\mathrm{C}(t_2,C)\neq\varnothing$` | 是否会重复执行代码块。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心就是带 hierarchy 的 statechart。 |
| 事件 / 触发 | 很强 | enabledness 直接由事件触发和 guard 共同决定。 |
| 守卫 / 数据 | 很强 | local / parameter / static variables 都是一等对象。 |
| 层次 | 很强 | 明确区分 `atomic/composite/shell/statechart`。 |
| 并发 / 同步 | 很强 | 重点就在 orthogonal 并发和任意交错执行。 |
| 时间约束 | 不支持 | 本文不是 timed statechart 语义。 |
| 连续动态 / 随机性 | 不支持 | 不涉及混成或随机机制。 |
| 可执行 / 可验证性 | 很强 | 语义直接落成 simulator，并接上 fuzz testing。 |

### 形式化问题与性质

1. `ConStaBL` 的核心贡献是把 statechart 语义真正落到“代码如何执行”的层面，而不是只停在图形结构。
2. 它对冲突保持保守态度，宁可显式报冲突，也不接受隐藏优先级。
3. 通过 simulator + fuzzing，这篇论文把 statechart 从“规格图”推进到“可被测试工具消费的执行工件”。

## 构造方式与承载格式

### 建模入口

原文中的构造顺序大致是：

1. 写 `ConStaBL` 状态图结构。
2. 为状态声明 `local/parameter/static` 变量。
3. 给状态填 entry / exit code。
4. 给迁移填事件、guard 和动作。
5. 由 simulator 构造 configuration tree、state tree、code tree 和 CFG 后执行。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. 抽象语法层的状态和迁移元组。
2. 状态包含树与初始子树。
3. source / destination code tree。
4. CFG 与 code containment tree。
5. simulator 生成的 trace。

### 交换与互操作

1. 原文没有给出 `XML/XMI/JSON` 一类独立交换格式。
2. 互操作重点不在跨工具交换，而在“statechart -> executable simulator -> fuzzing engine”。
3. 与外部工具最明确的耦合是把 simulator 输出交给 fuzzing workflow，而不是标准化导入导出。

## 配套基础设施

- 建模/编辑工具：原文主要描述语言与 simulator，没有成熟图形化建模 IDE 的稳定发布说明。
- 解析/交换/元模型支持：抽象语法、结构语义、配置树和 CFG 规则就是它的核心元模型承载。
- 仿真/执行支持：论文明确给出 `ConStaBL` simulator，并以 operational semantics 形式解释其执行。
- 验证/分析支持：冲突检测、valid simulation 判定和 trace 生成是直接能力；进一步分析通过 fuzz testing 接入。
- 代码生成/转换支持：原文不把代码生成作为主线。
- 标准化或社区生态：目前更像研究型语言和工具原型，生态远弱于 `SCXML/Yakindu/Stateflow`。

## 适用场景与需求前提

### 适用场景

适合需要用 statechart 表达较复杂并发控制逻辑，同时又希望把模型直接执行起来并做早期缺陷检测的场景，尤其是软件行为建模、设计期验证和测试驱动建模。

### 需求前提

1. 需求本身要能清晰拆成有限状态和事件驱动转移。
2. 数据层面需要局部变量、guard 和动作代码，而不是纯无记忆 `FSM`。
3. 并发是关键复杂度来源，且团队关心并发语义到底如何落到代码执行。
4. 时间和连续动力学不是核心问题，否则应转向 timed / hybrid 家族。

### 不适用或高成本场景

1. 若主要问题是 deadline、时钟约束或物理动力学，这条路线不够。
2. 若团队只需要画图而不需要可执行语义、trace 或 testing，则 `ConStaBL` 的收益会下降。
3. 若系统最终必须对齐工业级 `SCXML/Yakindu/UML` 标准，这个研究型方言会带来映射成本。

## 与相邻形式主义的关系

1. 相比普通 `FSM`，`ConStaBL` 增加了 hierarchy、并发区域、局部变量和 entry/exit/action 代码。
2. 相比广义 `Statecharts`，它更强调 executable semantics 和代码交错规则，而不是语义留白或工具私有规则。
3. 相比 `SCXML/Yakindu/Stateflow` 这类成熟载体，它的优势是语义更显式，劣势是标准化和生态弱。
4. 它与 `Petri Net` 一样重视并发，但仍保持 statechart 的状态分层和事件驱动视角，不转成 token-flow 模型。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的直接价值在于：它说明“面向需求自动建模”时，若目标是可执行 statechart，不能只生结构图，还必须明确 entry/exit/action 代码、冲突判定和并发执行规则。

### 作为目标形式主义还是中间表示

它更适合作为目标形式主义的语义参照或中间执行语义，而不是当前文库里最优的最终工业输出对象。因为它足够清楚地说明了怎样执行，却缺少广泛通用的标准交换格式。

### 对需求到模型生成的启发

1. 生成状态图时应同时生成变量作用域信息。
2. 并发区域不能只画出来，必须同时生成冲突约束。
3. 若要后续自动测试，模型动作代码和 trace 观测点应在建模阶段就保留。

### 现实限制

1. 工具生态仍偏研究型。
2. 语义依赖本文定义的 simulator，不是行业默认。
3. 缺少稳定标准格式会增加和其他后端互通的成本。

## 重要的相关工作

### 奠基或前身工作

1. Harel 的 `Statecharts` 是总母线。
2. 论文把早期 `StaBL` 扩展到带并发的 `ConStaBL`。

### 同类型或同家族工作

1. `SCXML`、`Yakindu`、`Stateflow`、`Rhapsody`、`Sismic` 都属于 statechart 执行语义或工具家族。
2. 这些工具大多依赖固定优先级、document order 或工具私有规则来解并发冲突。

### 标准 / 格式 / 工具链工作

1. 原文明确讨论了 `SCXML`、`Yakindu`、`Stateflow`、`Sismic` 等现有实现。
2. `ConStaBL` 的 simulator 和 fuzz-testing setup 则是它自己的工具链特色。

### 与本研究关系最紧的工作

1. `Sismic` 与本文最接近，因为都把 executable statecharts 接到测试。
2. 各类 `Yakindu/UML/Stateflow -> verification` bridge 说明 statechart 若要进入高可信流程，语义收束是前提。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`ConStaBL / concurrent statecharts with local variables`
- 论文角色：executable-statechart semantics / simulator / fuzz-testing route
- 核心功能：把带局部变量和并发区域的 statechart 落成可执行 simulator，并显式定义冲突与合法仿真。
- 关键特性：局部变量、hierarchy、并发语义、代码级交错、冲突显式报错、可接 fuzz testing。
- 构造方式：状态/迁移元组 + state tree / code tree / CFG + simulator。
- 基础设施：研究型 simulator、CFG/code containment tree、fuzz-testing workflow。
- 适用场景：需要 executable statechart、并发语义清晰、早期 bug 暴露和测试驱动建模的反应式软件。
- 需求前提：需求能拆成有限状态、事件、变量和动作，且主要复杂度来自离散并发而不是时间或连续动力学。
- 状态：🟢 直接可用
