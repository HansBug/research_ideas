# 使用有色 Petri 网形式化并发 UML 状态机 / Formalising Concurrent UML State Machines Using Coloured Petri Nets

## 基本信息

- 标题：Formalising Concurrent UML State Machines Using Coloured Petri Nets
- 中文标题：使用有色 Petri 网形式化并发 UML 状态机
- 作者：Étienne André, Mohamed Mahdi Benmoussa, Christine Choppy
- 发表：*Knowledge and Systems Engineering*, pp. 473-486, 2015
- DOI：`10.1007/978-3-319-11680-8_38`
- 链接：https://doi.org/10.1007/978-3-319-11680-8_38
- 形式主义：`UML State Machine / Coloured Petri Net translation`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：并发 `UML` 状态机到 `Coloured Petri Net` 的形式化与验证桥接方法
- 工具/实现获取方式：论文明确依赖 `CPN Tools` 一类支持 global variables 的 `CPN` 工具做测试和检查；正文重点是翻译算法，本身未给出独立公开仓库。
- 标准/格式获取方式：输入承载是 `UML` state machine diagram (`SMD`)；输出承载是 `Coloured Petri Net`；两者都是图形模型，论文没有把桥接固定成中立 `XMI` 标准，而是固定翻译规则与生成网结构。

## 简报

这篇论文补的是 `UML State Machine` 非常关键的一块基础问题：并发、层次、entry/exit/do、fork/join、共享变量这些工程上常用的语法特性，如果只停留在非形式化 `UML` 语义层，很难直接做可靠验证。作者选择的路线不是发明新的专用验证器，而是把并发 `UML SMD` 翻译到 `Coloured Petri Net`，借助 `CPN` 的图形结构、token 语义和现成工具链，把 `UML` 行为图接到可分析后端。

- 形式主义定位：并发 `UML State Machine` 的形式化与验证桥，而不是新的 `UML` 子语言。
- 构造方式简述：`UML SMD -> states/behaviors/transition translation algorithms -> CPN places/transitions/tokens -> CPN analysis tools`。
- 基础设施与场景简述：依托 `UML` 行为图、`CPN` 图形语义、global variables 和 `CPN Tools`，适合需要保留 hierarchy 与 concurrency 的软件行为验证。

```text
concurrent UML SMD -> translation algorithms -> coloured Petri net -> simulation / state-space analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML` state machine diagram 中的 simple/composite states、orthogonal regions、fork/join、history、entry/exit/do behaviors。
2. 含 global variables 的 `Coloured Petri Nets`。
3. 由 states/behaviors translation 和 transitions translation 组成的两类核心算法。
4. 用 level state 和 hierarchy-traversal 规则保持原始 `UML` 层次结构。

### 核心抽象

论文把并发 `UML SMD` 中的一条 transition 写成：

$$
t = (S_1, e, g, (b,f), sLevel, S_2)
$$

上式中的符号逐项解释如下：

1. `$S_1$` 是源状态集合。
2. `$S_2$` 是目标状态集合。
3. `$e$` 是触发该 transition 的事件。
4. `$g$` 是 guard。
5. `$(b,f)$` 是 firing 该 transition 时需要执行的 behavior。
6. `$sLevel$` 是包含该 transition 的 level state，即包住这条 transition 的最内层层次状态。

这个 `$sLevel$` 概念是论文的一大关键，因为 fork/join、跨层 transition 和复合状态退出顺序，都要靠它来恢复 `UML` 层次语义，而不是简单 flatten 掉结构。

对应的翻译函数可保守整理为：

$$
\mathcal{T}_{uc} : SMD \to CPN
$$

上式中的符号逐项解释如下：

1. `$SMD$` 是输入的并发 `UML State Machine Diagram`。
2. `$CPN$` 是输出的 `Coloured Petri Net`。
3. `$\mathcal{T}_{uc}$` 表示整篇论文的桥接翻译。
4. 该翻译不是单条规则，而是由 `Algorithm 1` 和 `Algorithm 2` 等多步构造组成。

论文对 `CPN` 的核心运行对象强调的是 marking。可保守压成：

$$
M : P \to Multiset(Token)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 `CPN` 的 place 集合。
2. `$Token$` 是 place 上允许的带颜色 token 值。
3. `$M$` 给出当前每个 place 上有哪些 token。
4. firing transition 会消费源 place token 并在目标 place 生成新 token。

为了表达共享变量，论文允许使用 `CPN` global variables；若工具不原生支持，则可用“单 token 全局 place”模拟。这个思路可以保守写成：

$$
v \in Var,\quad pv \in P,\quad M(pv)=\{ value(v) \}
$$

上式中的符号逐项解释如下：

1. `$v$` 是共享变量。
2. `$pv$` 是编码该变量值的全局 place。
3. `$M(pv)$` 中唯一 token 保存当前变量值。
4. 读取 guard 时 token 会被读出再放回，更新时则生成新值 token。

### 一个最小例子与通俗解释

论文最想解决的不是普通顺序状态机，而是更难的并发 `UML`：

1. 一个 composite state 内可以有多个 orthogonal regions。
2. 某条 fork transition 可以同时激活多个 region。
3. join transition 要等待多个 region 都到位。
4. 这些状态还可能带 entry/exit/do behaviors，并读写共享变量。

通俗地说，作者把 `UML` 图里的“现在有哪些子状态同时活着、哪些入口出口动作要执行、哪个共享变量当前是什么值”，都转成 `CPN` 中的 token 分布和 firing 条件。这样原本口头描述的并发层次行为，就变成了可以让 `CPN Tools` 跑起来和检查起来的网模型。

### 运行 / 接受 / 转移语义

论文的桥接语义可保守写成：

$$
SMD \xrightarrow{\mathcal{T}_{uc}} CPN \xrightarrow{\mathrm{fire}} M_0 \to M_1 \to \cdots
$$

上式中的符号逐项解释如下：

1. `$SMD$` 是源 `UML` 状态机。
2. `$\mathcal{T}_{uc}$` 是翻译函数。
3. `$CPN$` 是生成的有色网。
4. `$M_0,M_1,\ldots$` 是 firing 过程中产生的 marking 序列。

状态和行为翻译的主要职责是生成对应的 places、entry/exit/do 行为结点和 history 结构；transition 翻译则负责把事件、guard、共享变量读写、fork/join 和跨层同步连接起来。

### 语义边界

1. 论文主线是 `UML SMD -> CPN` 形式化，不是完整 `UML` 语义标准化。
2. 它显式覆盖 concurrency、hierarchy 和 shared variables，但不追求对象动态创建/销毁等更广义 `UML` 行为语义。
3. 方法依赖 `CPN` 作为中间验证对象，因此保真度和可验证性都与生成网规模相关。
4. 作者强调相较于 flatten 路线，本方法保留 hierarchy；但这也意味着翻译算法更复杂。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `UML` transition 骨架 | `$t=(S_1,e,g,(b,f),sLevel,S_2)$` | 保留并发、层次和行为的核心对象。 |
| 总翻译函数 | `$\mathcal{T}_{uc}: SMD \to CPN$` | 把并发 `UML` 状态机桥接到 `CPN`。 |
| marking 语义 | `$M:P\to Multiset(Token)$` | `CPN` 当前状态由 token 分布决定。 |
| 全局变量编码 | `$M(pv)=\{value(v)\}$` | 共享变量可由单 token 全局 place 表示。 |
| 结构保持 | `level state` | 避免 flatten 掉 hierarchy 带来的语义损失。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | simple/composite state、history 和层次结构都是主体。 |
| 事件 / 触发 | 很强 | transition 直接以事件驱动。 |
| 守卫 / 数据 | 很强 | shared variables 和 guards 是翻译核心之一。 |
| 层次 | 很强 | `level state` 和多层 composite state 是论文重点。 |
| 并发 / 同步 | 很强 | orthogonal regions、fork/join 是主要贡献。 |
| 时间约束 | 不支持 | 本文不是 timed UML 或 timed CPN 路线。 |
| 连续动态 / 随机性 | 不支持 | 不在语义范围内。 |
| 可执行 / 可验证性 | 很强 | 生成 `CPN` 后可用 `CPN Tools` 等现成基础设施分析。 |

### 形式化问题与性质

1. 这篇论文真正补的是“如何把并发 `UML` 的复杂语义稳定落到现成形式化后端”。
2. `CPN` 被选中，不只是因为它能验证，还因为它保留图形化承载，便于和 `UML` 图做结构对应。
3. 对 `project_1` 来说，这说明 `UML` 状态机如果要进入验证链，shared variables、fork/join 和 hierarchy 不能模糊生成。

## 构造方式与承载格式

### 建模入口

建模入口是带并发 region、fork/join、entry/exit/do behaviors 和共享变量的 `UML State Machine Diagram`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UML SMD` 图形模型。
2. level-state 与 hierarchy traversal 辅助结构。
3. 生成的 `CPN` places、transitions、arc expressions 和 colored tokens。
4. global variables 或等价的全局 place 编码。

### 交换与互操作

论文的互操作重点在 `UML -> CPN`。它没有定义开放交换标准，而是固定了一条能接 `CPN` 工具的翻译路线；相比只翻到文本型 model checker 输入，`CPN` 还能保留更接近原图的图形结构。

## 配套基础设施

- 建模/编辑工具：任意能表达目标子集的 `UML` 建模工具。
- 解析/交换/元模型支持：论文重点是翻译算法本身，未给独立 `XMI` 交换层规范。
- 仿真/执行支持：生成的 `CPN` 可由 `CPN Tools` 等网工具仿真。
- 验证/分析支持：`CPN` state-space exploration 与相关分析功能。
- 代码生成/转换支持：核心就是 `UML SMD -> CPN` 的结构化翻译。
- 标准化或社区生态：依托 `UML` 和 `Coloured Petri Net` 两条成熟图形建模生态。

## 适用场景与需求前提

### 适用场景

适合软件行为建模、并发控制逻辑和层次交互流程已经使用 `UML State Machine` 表达，但又需要正式验证支撑的场景。

### 需求前提

1. 需求已经能落成明确的状态、事件、guard 和共享变量。
2. 并发结构主要是 orthogonal regions、fork/join 这类 `UML SMD` 语义。
3. 团队接受通过 `CPN` 做中间验证模型。
4. 不要求完整对象动态语义，只要求论文覆盖的 `UML SMD` 子集。

### 不适用或高成本场景

若需求更偏 dense time、连续物理过程、概率行为或复杂对象生命周期管理，这条 `UML -> CPN` 路线就需要额外扩展。

## 与相邻形式主义的关系

相对 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，两者都是 `UML -> formal backend` 桥，但那篇接 `PAT/CSP#`，这里接 `CPN` 并更强调图形并发结构；相对 [a-metamodel-based-execution-framework-for-uml-state-machines/desc.md](../a-metamodel-based-execution-framework-for-uml-state-machines/desc.md)，`BlueState` 更偏执行与代码生成，本文更偏形式化验证桥；相对 [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)，后者更偏运行时实现和验证混合路线，本文更强调用 `CPN` 承接并发语义。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 `UML State Machine` 并不是只能当图形前端，也可以被稳定地翻进并发验证后端。
2. 对 LLM 自动建模来说，若目标是 `UML`，就必须把 fork/join、region、共享变量和 entry/exit/do 行为生成得足够明确。
3. 它为后续“模型元素级验证场景生成”提供了一个结构保持的并发后端。

### 作为目标形式主义还是中间表示

更适合作为 `UML` 目标形式主义的验证中间表示路线，而不是最终替代 `UML` 的新语言。

### 对需求到模型生成的启发

1. 并发 `UML` 需求应显式指出哪些状态可并行、哪些点需要 join。
2. 共享变量若要可验证，就必须提前约束其读写位置和作用。
3. 为了桥到形式后端，层次结构不能只靠视觉缩进表达，必须能恢复成可遍历对象。

### 现实限制

它主要解决的是 `UML SMD` 的并发形式化桥接，不直接解决 `UML` 全标准的全部语义歧义。

## 重要的相关工作

### 奠基或前身工作

- `UML State Machine` 的非形式化工业语义母线。
- `Coloured Petri Nets` 图形化并发建模基础设施。

### 同类型或同家族工作

- [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：`UML -> PAT/CSP#` 路线。
- [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)：`UML` 状态机的执行与验证桥。

### 标准 / 格式 / 工具链工作

- `CPN Tools` 与 global-variable `CPN` 工作流。
- [a-metamodel-based-execution-framework-for-uml-state-machines/desc.md](../a-metamodel-based-execution-framework-for-uml-state-machines/desc.md)：`UML` 执行载体一侧的相邻基础设施。

### 与本研究关系最紧的工作

- `UML` 行为图自动化生成后，需要稳定接到形式验证后端时，这篇提供了保留 concurrency 与 hierarchy 的桥接模板。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machine / Coloured Petri Net translation`
- 论文角色：并发 `UML` 状态机到 `CPN` 的形式化与验证桥接方法
- 核心功能：把带 hierarchy、fork/join 和 shared variables 的并发 `UML SMD` 形式化翻译成 `Coloured Petri Net` 并接入现成验证工具。
- 关键特性：orthogonal regions、fork/join、entry/exit/do、history、level state、global variables、`CPN Tools`。
- 构造方式：`UML SMD -> translation algorithms -> CPN places/transitions/tokens -> CPN analysis`。
- 基础设施：`UML` 图形建模、`CPN` 图形语义、global variables、`CPN Tools`。
- 适用场景：并发软件行为、层次控制逻辑和需要正式验证的 `UML` 状态机。
- 需求前提：需求需能明确写成 `UML` 状态、事件、guard、region 和共享变量，并接受 `CPN` 作为验证中间层。
- 状态：🟢 直接可用
