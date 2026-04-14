# ObsSlice：一种基于观察者的定时自动机切片器 / ObsSlice: A Timed Automata Slicer Based on Observers

## 基本信息

- 标题：ObsSlice: A Timed Automata Slicer Based on Observers
- 中文标题：ObsSlice：一种基于观察者的定时自动机切片器
- 作者：Víctor Braberman，Diego Garbervetsky，Alfredo Olivero
- 发表：*Computer Aided Verification*，pp. 470-474，2004
- DOI：`10.1007/978-3-540-27813-9_39`
- 链接：https://doi.org/10.1007/978-3-540-27813-9_39
- 形式主义：`Timed Automata / observer-based slicing / OpenKronos / Uppaal`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：observer-guided exact slicing for timed-automata verification
- 工具/实现获取方式：论文直接给出 `ObsSlice` 原型与原始项目页，并说明输出可交给 `Kronos`、`OpenKronos`、`Uppaal` 使用。
- 标准/格式获取方式：输入模型是与 `Kronos/OpenKronos` 兼容的 timed automata network 与 I/O label classification；输出是可被 `Kronos/OpenKronos/Uppaal` 检查的变换后网络。

## 简报

这篇论文的重点，不是定义一种新的 timed automata 家族，而是解决一个非常工程化的问题：当性质由 observer 表达时，网络里到底哪些 automata 和 clocks 真正与当前 observer 位置相关。`ObsSlice` 用 influence information 和 sojourn-set 近似先做静态判断，再生成一个对 observer 上 `TCTL` 性质保持精确的切片模型。

- 形式主义定位：timed-automata verification preprocessing method，而不是新的 timed language。
- 构造方式简述：把系统 under analysis 与 observer 合成，按 observer 位置估计相关 automata / clocks，再生成带 sleep locations 或 committed disabling chains 的精简网络。
- 基础设施与场景简述：依托 `Kronos / OpenKronos / Uppaal`，服务 observer-based real-time verification，目标是减小状态空间、缩短反例并降低内存压力。

```text
timed-automata network + observer -> influence / sojourn analysis -> location-wise relevance sets -> sliced network -> Kronos / OpenKronos / Uppaal verification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. system under analysis (`SUA`) 的 timed automata network。
2. 以 virtual component 方式并行组合的 observer。
3. observer location 对应的 relevance information。
4. pair-wise influence analysis。
5. transformed / sliced timed automata network。

### 核心抽象

根据论文描述，可以把输入对象保守整理为：

$$
\mathcal N = A_1 \parallel A_2 \parallel \cdots \parallel A_n \parallel O
$$

上式中的符号逐项解释如下：

1. `A_1,\ldots,A_n` 是被分析系统的 timed automata 组件。
2. `O` 是 observer automaton 或 observer network。
3. `\parallel` 表示并行组合。
4. 整个方法都是围绕“observer 在不同位置时哪些元素可忽略”展开。

论文真正的核心产物是针对 observer 位置的 relevance sets，可保守写成：

$$
R(\ell_O) \subseteq \{A_1,\ldots,A_n\} \cup C
$$

上式中的符号逐项解释如下：

1. `\ell_O` 是 observer 的某个位置。
2. `C` 是模型中的 clocks 集合。
3. `R(\ell_O)` 表示在 observer 位于 `\ell_O` 时，不可安全忽略的 automata 与时钟。
4. 不在 `R(\ell_O)` 中的元素可以被暂时 disable，从而缩小验证状态空间。

论文强调该变换对 observer 上的 branching-time 分析是 exact 的，可压成：

$$
\mathcal N \models \varphi \iff \mathrm{Slice}(\mathcal N, O) \models \varphi
$$

其中：

1. `\varphi` 是 stated over the observer 的 `TCTL` 性质。
2. `\mathrm{Slice}(\mathcal N, O)` 是 `ObsSlice` 变换后的网络。
3. “exact” 的含义是：不会因为切片而改变 observer 性质的真值。

### 一个最小例子与通俗解释

论文中的 token-ring、pipeline 和 remote-bridge 例子都说明了同一个直觉：

1. observer 只关心某个 end-to-end timing scenario。
2. 在 observer 当前所处位置，系统中很多 automata 和 clocks 实际不会影响这个 scenario 是否成立。
3. `ObsSlice` 先把这些不相关活动“睡眠化”，再交给 `Kronos` 或 `Uppaal`。

通俗地说，它像一个“按性质裁剪 timed model 的预处理器”。不是整个系统都一股脑送进模型检查器，而是先问：“为了这条 observer 性质，我现在到底需要看哪些局部行为？”

### 运行 / 接受 / 转移语义

论文的方法本身不是重新定义 timed automata 运行语义，而是在其之上做保持性质的模型变换。可保守写成：

$$
\mathrm{ObsSlice} = (\mathrm{RelevanceCalc}, \mathrm{InfluenceCalc}, \mathrm{SojournCalc}, \mathrm{Translator})
$$

上式中的符号逐项解释如下：

1. `RelevanceCalc` 负责按 observer 位置估计相关元素。
2. `InfluenceCalc` 负责做 pair-wise influence 判断。
3. `SojournCalc` 给出在某 observer 位置下各组件可能停留的 location over-approximation。
4. `Translator` 负责输出对应目标工具方言下的 sliced network。

### 语义边界

方法边界包括：

1. 它主要适用于 observer-based timed verification。
2. 切片保持的是 observer 上 `TCTL` 分析的 exactness，而不是任意性质。
3. 输入方言以 `Kronos/OpenKronos` 兼容网络为主。
4. I/O classification 若写错，不会让结果变成不安全，但会削弱切片精度。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 输入模型 | `$\mathcal N = A_1 \parallel \cdots \parallel A_n \parallel O$` | 系统网络与 observer 的基本对象。 |
| relevance set | `$R(\ell_O) \subseteq \{A_1,\ldots,A_n\} \cup C$` | 在 observer 某位置下，哪些 automata / clocks 不能被忽略。 |
| exact slicing | `$\mathcal N \models \varphi \iff \mathrm{Slice}(\mathcal N, O) \models \varphi$` | 对 observer 上 `TCTL` 性质保持精确。 |
| 工具骨架 | `$\mathrm{ObsSlice} = (\mathrm{RelevanceCalc}, \mathrm{InfluenceCalc}, \mathrm{SojournCalc}, \mathrm{Translator})$` | 论文图 1 给出的模块化架构。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 面向 timed automata network 的 location-level 分析。 |
| 事件 / 触发 | 中等支持 | 通过 I/O label classification 参与 influence 判断。 |
| 守卫 / 数据 | 中等支持 | 影响分析会考虑 predicates、assignments 与 communication。 |
| 层次 | 不适用 | 主线不是层次状态机。 |
| 并发 / 同步 | 很强 | 针对多组件并发 timed activity 与 observer 并行组合。 |
| 时间约束 | 很强 | 核心对象就是 clocks 与 observer-based timing properties。 |
| 连续动态 / 随机性 | 不支持 | 主线完全在 timed automata。 |
| 可执行 / 可验证性 | 很强 | 直接面向 `Kronos / OpenKronos / Uppaal` 验证前处理。 |

### 形式化问题与性质

1. 这条路线不是近似抽象，而是 observer-property preserving 的 exact slicing。
2. 它把“哪些部分与当前时序性质无关”变成了静态可计算问题。
3. 对 timed automata 实务非常有价值，因为它直接缓解状态爆炸与超长 counterexample。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. `Kronos/OpenKronos` 兼容 timed automata network。
2. 以虚拟 observer 表达 safety / liveness 场景。
3. 每个 automaton 的 I/O action classification。
4. 可选的 synchronous subsystem directives。

### 机器可处理承载方式

机器可处理承载方式包括：

1. timed automata network；
2. observer locations；
3. activity tables / relevance tables；
4. sleep locations 或 committed chains 形式的 transformed automata。

### 交换与互操作

这篇论文的互操作重点在 timed-verification 工具链内部：

1. 输入兼容 `Kronos / OpenKronos`。
2. 输出可给 `Kronos / OpenKronos / Uppaal`。
3. translator 会按目标方言选择不同的 disabling 方式。

## 配套基础设施

- 建模/编辑工具：外部 timed automata 建模器；原文未自带图形 editor。
- 解析/交换/元模型支持：`Kronos/OpenKronos` 兼容输入，`Uppaal` 兼容输出。
- 仿真/执行支持：不是执行器，核心是 verification preprocessing。
- 验证/分析支持：observer-guided slicing、pair-wise influence、sojourn-set 估计、counterexample 缩短。
- 代码生成/转换支持：`Automata Translator` 负责生成对应工具方言的 sliced model。
- 标准化或社区生态：与 `Kronos / OpenKronos / Uppaal` 的 timed-automata toolchain 直接耦合。

## 适用场景与需求前提

### 适用场景

适合 observer-based real-time verification，尤其适合网络较大、组件较多、而性质只关注某条局部 timing scenario 的场景。

### 需求前提

1. 系统能稳定建模为 timed automata network。
2. 性质能写成 observer 上的 `TCTL` 或 branching-time 观察条件。
3. 组件通信、赋值与 predicates 足够清晰，便于 influence analysis。
4. 团队愿意接受一个前处理切片步骤，而不是直接把原模型送进 model checker。

### 不适用或高成本场景

如果性质不是 observer-based，或者模型已强依赖超出 timed automata 方言的大量数据与外部语义，`ObsSlice` 的收益会显著下降。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，这篇论文不是 timed automata 平台综述，而是其前处理优化；相对 [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)，`Kronos` 是检查器本体，`ObsSlice` 是送检前的切片器；相对 [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md)，`Synthia` 更偏开放 timed game 的验证/综合，而这里更偏 observer-guided reduction。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的启发是：当 LLM 生成的状态机足够大时，后续验证不一定只能靠“更强的模型检查器”，也可以靠“更聪明的 property-aware slicing”。如果未来自动生成 observer 或待验证性质，类似 `ObsSlice` 的思路很适合接到闭环中。

### 作为目标形式主义还是中间表示

它不是目标形式主义，而是 timed automata 生态中的 verification method / preprocessing bridge。

### 对需求到模型生成的启发

1. observer 设计会直接决定验证成本，不只是决定验证结论。
2. 生成模型时若能保留组件边界和 I/O 分类，后续切片与组合分析会更有效。
3. “与当前性质无关的局部行为”应被视为验证前可裁剪资产。

### 现实限制

它依赖 observer-based timed verification 语境，不能泛化成所有状态机家族的通用压缩器。

## 重要的相关工作

1. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：经典 timed automata 工具链总入口。
2. [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)：早期 `Timed Automata` 核心检查器。
3. [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md)：另一条 timed-automata verification / synthesis 工具线。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / observer-based slicing / OpenKronos / Uppaal`
- 论文角色：observer-guided exact slicing for timed-automata verification
- 归类理由：论文主体是围绕 timed automata observer verification 的切片方法和工具链，而不是新的模型本体或标准格式。
