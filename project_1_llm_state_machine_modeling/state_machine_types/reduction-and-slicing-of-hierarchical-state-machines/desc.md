# 层次状态机的归约与切片 / Reduction and Slicing of Hierarchical State Machines

## 基本信息

- 标题：Reduction and Slicing of Hierarchical State Machines
- 中文标题：层次状态机的归约与切片
- 作者：Mats P. E. Heimdahl，Michael W. Whalen
- 发表：*Software Engineering --- ESEC/FSE '97*，pp. 450-467，1997
- DOI：`10.1007/3-540-63531-9_30`
- 链接：https://doi.org/10.1007/3-540-63531-9_30
- 形式主义：`RSML / hierarchical finite state machines / specification slicing`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`RSML` 层次状态机的 scenario-based reduction 与 slicing 方法
- 工具/实现获取方式：原文明确说明作者实现了一个 prototype slicing tool，并基于既有 `RSML` parser / analysis environment 运作；当前提取文本未见稳定公开下载地址。
- 标准/格式获取方式：承载方式是 `RSML` 图形状态机、AND/OR tables、scenario tables 与基于 AST marking 的 reduction/slicing 结果；无中立交换标准。

## 简报

这篇论文的重要性不在于定义新的状态机家族，而在于把“怎样看懂一个巨大的层次需求状态机”系统化了。作者面对 `TCAS II` 这样的大规格时，提出两级流程：先按 scenario 对 next-state relation 做域限制，得到 interpretation；再在 interpretation 上做 data-flow 与 control-flow slicing。这样一来，大型 `RSML` 规格不必一次平铺阅读，而可以围绕具体审查问题逐层压缩。

- 形式主义定位：围绕 `RSML` 层次需求状态机的解释、归约与切片方法。
- 构造方式简述：先用 reduction scenario 删去与场景矛盾的 table 列和 transition，再根据 guarding condition 与 trigger event 做依赖切片。
- 基础设施与场景简述：依托 `RSML` parser、AST marking、静态依赖图和 prototype slicer，服务 safety-critical embedded-control requirement review，尤其是 `TCAS II` 一类巨大规格。

```text
审查问题 -> reduction scenario -> interpretation of RSML spec -> data/control-flow slices -> 更小、更可读的规格视图
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `RSML` hierarchical state-machine specification；
2. next-state relation；
3. reduction scenario；
4. interpretation under scenario；
5. static data dependency graph；
6. control-flow slice built from trigger-event generation；
7. slice combination through set operations。

### 核心抽象

原文明确把 `RSML` 规格看成 next-state relation，可保守写成：

$$
F : C \to C
$$

上式中的符号逐项解释如下：

1. `$C$` 是状态与变量取值共同组成的配置集合。
2. `$F$` 是 `RSML` 规格定义的 mathematical next-state relation。
3. 原文指出 `$C \subseteq Config \times V$`，其中 `Config` 对应图形状态配置，`V` 对应输入输出变量。

给定 scenario `$s$` 后，论文定义的 interpretation 可写成：

$$
R = \{ (c, c') \in F \mid s(c) \}
$$

上式中的符号逐项解释如下：

1. `$s(c)$` 表示配置 `$c$` 满足 reduction scenario。
2. `$R$` 是把 `$F$` 的定义域收缩到该场景后的关系。
3. 这正对应原文“interpretation is a domain restriction of the next-state relation”。

数据依赖切片和控制流切片在文中是通过 AST marking 完成的。可把其骨架保守整理为：

$$
Slice = Slice_{data}(g) \cup Slice_{ctrl}(e)
$$

上式中的符号逐项解释如下：

1. `$g$` 是某个关注 transition 的 guarding condition。
2. `$e$` 是该 transition 的 trigger event。
3. `$Slice_{data}(g)$` 代表所有会影响 `$g$` 真值的实体。
4. `$Slice_{ctrl}(e)$` 代表所有能生成 `$e$` 的 transition 及相关实体。
5. 这一并集写法是对论文“data-flow slice + control-flow slice 可组合”的保守归纳。

### 一个最小例子与通俗解释

论文用 `TCAS II` 的 intruder classification 反复说明这一流程。以 “一个 intruder 停止报告高度” 为例：

1. 先定义 scenario `Not-Reporting-Altitude`。
2. 所有与该 scenario 矛盾的 AND/OR table 列被删去。
3. 一些 transition 因 guard 变得不可满足而直接从模型里消失。
4. 然后再围绕 “Potential-Threat 如何被降级” 做 data-flow 和 control-flow slicing。

通俗地说，这个方法像“给复杂需求状态机加了一个问题驱动的放大镜”。你先问“在这个场景下到底会发生什么”，系统先帮你把无关分支遮掉；再问“这条转移受什么影响、由什么触发”，系统继续把上下文缩到审查真正关心的一小块。

### 运行 / 接受 / 转移语义

论文的核心不是重新定义 `RSML` 执行语义，而是说明如何在既有 next-state relation 上做 scenario restriction。最关键的语义关系就是：

$$
c \xrightarrow{R} c' \iff (c, c') \in R
$$

上式中的符号逐项解释如下：

1. `$c$` 和 `$c'$` 是两个配置。
2. `$\xrightarrow{R}$` 表示在特定 scenario interpretation 下允许的一步状态变化。
3. 只有当 `$c$` 满足 scenario 时，这一步才会保留在 interpretation 中。

控制切片的可达性则可保守写成：

$$
t_0 \leadsto_e t_k
$$

上式中的符号逐项解释如下：

1. `$t_k$` 是当前关注的 transition。
2. `$e$` 是触发 `$t_k$` 的事件。
3. `$t_0 \leadsto_e t_k$` 表示 `$t_0$` 能在规格内部生成最终触发 `$t_k$` 的事件链。
4. 这是根据论文“沿能生成 trigger event 的 transitions 反向追踪，直到外部输入源”为止做的保守记法。

### 语义边界

1. 该工作依赖 `RSML` 的表格和状态配置结构，不是任意程序切片器。
2. 当前实现对 scenario predicates 的决策过程有边界，尤其不完全覆盖任意整数和实数表达式。
3. 它的目标是 readability / review support，不是直接替代模型检查器。
4. 切片后的结果保留的是对特定问题有用的视图，而不是新的独立语言。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| next-state relation | `$F : C \to C$` | `RSML` 规格被看作从配置到配置的关系。 |
| interpretation | `$R = \{ (c, c') \in F \mid s(c) \}$` | scenario 会把规格收缩成场景相关行为。 |
| interpretation step | `$c \xrightarrow{R} c' \iff (c, c') \in R$` | interpretation 上的执行只保留场景允许的转移。 |
| combined slice | `$Slice = Slice_{data}(g) \cup Slice_{ctrl}(e)$` | 数据依赖与事件生成依赖可组合。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 以 `RSML` 层次状态与配置为核心。 |
| 事件 / 触发 | 强 | control-flow slice 直接围绕 trigger events 展开。 |
| 守卫 / 数据 | 很强 | AND/OR tables 与 guarding conditions 是 reduction 主对象。 |
| 层次 | 强 | `RSML` 是层次状态机语言。 |
| 并发 / 同步 | 部分支持 | 原文指出 `RSML` 支持 parallelism，但本论文重心是 slicing。 |
| 时间约束 | 弱支持 | 不主打 clocks，主要是离散 requirements slicing。 |
| 连续动态 / 随机性 | 不支持 | 不涉及连续物理过程或概率。 |
| 可执行 / 可验证性 | 强 | 已实现 prototype tool，服务规格审查和分析。 |

### 形式化问题与性质

1. 作者把 specification slicing 从程序语句层，推进到了层次需求状态机和表格规格层。
2. scenario-based interpretation 非常适合做“验证 profile / review profile”。
3. 这条路线对于大型 requirement-state-machine 的可读性提升，比单纯 flatten 后再看模型检查结果更直接。

## 构造方式与承载格式

### 建模入口

1. 先有完整 `RSML` 规格。
2. 定义 reduction scenario。
3. 生成 interpretation。
4. 围绕具体 transition 或变量再做 data/control slicing。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `RSML` 图形状态机与 AND/OR tables；
2. reduction scenarios；
3. AST marking；
4. static dependency graph；
5. sliced specification views。

### 交换与互操作

论文的“互操作”不是跨工具标准，而是规格分析链路内部的结构互操作：

1. scenario 进入 AND/OR tables 进行列删减；
2. transition、变量、宏、函数和状态共享同一依赖图；
3. 多个 slices 可做并、交和补组合。

## 配套基础设施

- 建模/编辑工具：既有 `RSML` 规格编辑和分析环境。
- 解析/交换/元模型支持：作者扩展了 `RSML` parser 以支持 AST marking。
- 仿真/执行支持：论文主线不是仿真，而是 readability-oriented slicing。
- 验证/分析支持：prototype slicer、dependency analysis、scenario-based reduction。
- 代码生成/转换支持：无。
- 标准化或社区生态：依托 `RSML` / safety-critical requirements 社区，不是通用交换标准。

## 适用场景与需求前提

### 适用场景

适合大型 safety-critical embedded-control requirements 的人工审查、异常场景分析、verification-profile 预整理和 specification debugging。

### 需求前提

1. 规格本身已写成 `RSML` 或相近的层次状态机 + 表格逻辑。
2. 审查问题能表达成 scenario、guard 或 trigger-event 视角。
3. 团队愿意维护结构化场景条件，而不是只读平铺图。
4. 目标是缩小理解范围，而不是直接替代全部 formal verification。

### 不适用或高成本场景

如果模型主要是代码级控制流、连续动力学或高度数值化约束，直接套用该 `RSML` slicing 流程会较别扭。

## 与相邻形式主义的关系

相对 `Model Checking of Hierarchical State Machines` 这类理论型 `HSM` 条目，本文更偏实际需求规格分析；相对 `Model Checking RSML-e Requirements`，本文更关注“怎么把大规格看清楚”，而不是“怎么翻译到验证器”；相对 `SpecTRM-RL`，它展示了大型表格状态机在审查阶段需要额外的 slicing 支撑。

## 与本研究的关系

### 对 Project 1 的价值

1. 它非常接近“验证剖面”思想：scenario 本身就是一种面向问题的规格收缩器。
2. data-flow / control-flow slicing 对后续“根据模型元素生成验证场景与待验证性质”很有直接借鉴价值。
3. 如果未来 LLM 生成的状态机很大，这种 interpretation + slicing 路线可以显著改善人工复核成本。

### 作为目标形式主义还是中间表示

更适合作为 `RSML` 类需求状态机的分析方法与验证前处理，而不是独立目标形式主义。

### 对闭环生成-验证-修复的启发

它提示我们：修复并不一定要在全模型上进行，也可以先按场景切片，再局部定位真正影响某条性质的状态、表项和事件链。

## 重要的相关工作

- `RSML`
- `RSML-e`
- `SCR`
- `TCAS II`

## 文献分类总结

- 形式主义：`RSML / hierarchical finite state machines / specification slicing`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 关键词：`RSML`、scenario reduction、specification slicing、AND/OR tables、`TCAS II`
