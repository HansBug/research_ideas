# BeSpaceD 中的空间与时间算子 / Operators for Space and Time in BeSpaceD

## 基本信息

- 标题：Operators for Space and Time in BeSpaceD
- 中文标题：BeSpaceD 中的空间与时间算子
- 作者：Jan Olaf Blech，Keith Foster
- 发表：*CoRR*，`abs/1602.08809`，2016
- DOI：`10.48550/ARXIV.1602.08809`
- 链接：https://arxiv.org/abs/1602.08809
- 形式主义：`BeSpaceD invariants / filtering / folding / normalization`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：operator layer for BeSpaceD spatio-temporal invariants
- 工具/实现获取方式：论文明确说明该实现基于 `Scala`、运行在 `Java` 环境中，并使用 `ScalaTest` 进行测试，同时可接 `z3` 等外部工具。
- 标准/格式获取方式：核心承载方式仍是 `BeSpaceD` 的 `Invariant` AST；本文新增的是 `filter`、`foldTime`、`foldSpace`、`normalize` 等可复用操作符层。

## 简报

这篇论文补的不是新的时空语言，而是 `BeSpaceD` 已有 invariant 语言之上的“算子层”。如果说前一篇 `BeSpaceD` 基础论文解决的是“如何把时空行为落成 invariant 并生成验证条件”，那这篇解决的就是“已有 invariant 之后，怎么做筛选、聚合、归一化和可比较化处理”。

- 形式主义定位：`BeSpaceD` 的 operator infrastructure，不是新的状态机族。
- 构造方式简述：在已有 invariant AST 上增加 filtering、time/space folding、normalization 等高阶操作，使时空规约能够被聚合、简化和重写。
- 基础设施与场景简述：依托 `Scala` case classes、pattern matching、函数式聚合和测试基础设施，服务工厂自动化、覆盖分析、工业机器人等场景中的时空数据处理。

```text
BeSpaceD invariant -> filter / foldTime / foldSpace / normalize -> comparable or aggregated invariant/result -> downstream analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `BeSpaceD` 的 `Invariant` 抽象语法树；
2. 时间与空间上的 filtering；
3. 面向累积计算的 `foldTime` 与 `foldSpace`；
4. 由多个 processor 组成的 normalization pipeline；
5. `Scala` 实现与测试支撑。

### 核心抽象

本文沿用 `BeSpaceD` 的 invariant 基础语法。可直接写为：

$$
I ::= TRUE \mid FALSE \mid AND(I,I) \mid OR(I,I) \mid IMPLIES(I,I) \mid TimePoint(t) \mid TimeInterval(t_1,t_2) \mid Owner(o) \mid OccupyBox(\cdots)
$$

上式中的符号逐项解释如下：

1. `I` 是 `BeSpaceD` invariant。
2. `TimePoint`、`TimeInterval` 表示时间对象。
3. `Owner` 表示某语义拥有者，例如 cloud 或 mountain。
4. `OccupyBox` 表示空间占用盒。
5. 这是论文在实现章节给出的 `Scala` case-class 片段的直接整理。

论文给出了时间折叠的泛型签名：

$$
\mathrm{foldTime}: Invariant \times A \times T \times T \times \Delta T \times (A \times Invariant \to A) \to A
$$

上式中的符号逐项解释如下：

1. `Invariant` 是被扫描的时空规约对象。
2. `A` 是累加器类型。
3. 前两个 `T` 分别是 start time 和 stop time。
4. `\Delta T` 是时间步长。
5. `(A \times Invariant \to A)` 是聚合函数。
6. 这正对应论文给出的 generalized signature 和其 `Scala` 实现签名。

空间折叠则可整理为：

$$
\mathrm{foldSpace}: Invariant \times A \times B \times B \times \Delta B \times (A \times Invariant \to A) \to A
$$

上式中的符号逐项解释如下：

1. `B` 表示空间区域对象，在实现里具体化为 `OccupyBox`。
2. 两个 `B` 分别表示 start area 和 stop area。
3. `\Delta B` 表示空间平移步长或 translation。
4. 其余部分与 `foldTime` 相同，只是扫描维度从时间换成空间。

对于归一化，论文直接给出了 processor 链：

$$
normalize = flatten \circ order \circ deduplicate \circ simplify
$$

以及更专门的：

$$
normalizeOwnerOccupied = mergeOwners \circ normalize
$$

上式中的符号逐项解释如下：

1. `flatten` 把嵌套 conjunction / disjunction 拉平。
2. `order` 给项排序。
3. `deduplicate` 去重。
4. `simplify` 做局部重写，如 `IMPLIES(TRUE,t_2)\mapsto t_2`。
5. `mergeOwners` 把相同 premise 下的 ownership-conclusion 合并。

### 一个最小例子与通俗解释

论文给了一个很直观的时间折叠例子。三个时间点上的 box invariant 写成：

$$
IMPLIES(TimePoint(t_1), b_1),\quad IMPLIES(TimePoint(t_2), b_2),\quad IMPLIES(TimePoint(t_3), b_3)
$$

上式中的符号逐项解释如下：

1. `t_1,t_2,t_3` 是三个时间点。
2. `b_1,b_2,b_3` 是对应的占用 box。
3. 每个 `IMPLIES` 都表示“在该时间点，空间对象占据该 box”。

把面积函数作为累加器后，论文的 `foldTime` 会把三个 box 的面积 `100 + 121 + 121` 聚合成 `342`。通俗地说，这就像把一串时空逻辑项当成可遍历的数据结构，不再只把它当“给 solver 的公式”，而是也当成“可以像列表那样 fold/filter/normalize 的结构化程序对象”。

### 运行 / 接受 / 转移语义

本文不是定义 automaton run，而是定义 invariant AST 上的变换语义。最核心的是 filtering 和 normalization：

$$
filter: Invariant \times Cond \to Invariant
$$

和

$$
normalize: Invariant \to Invariant
$$

上式中的符号逐项解释如下：

1. `Cond` 可以是时间窗口、空间区域或其他筛选条件。
2. `filter` 选出和该条件相关的 invariant 子树。
3. `normalize` 通过若干 processor 反复重写直到到达稳定形式。
4. 这两者共同把 “时空逻辑项” 变成“可比较、可聚合的数据对象”。

论文还展示了 filtering 的一条典型重写：

$$
IMPLIES(FALSE, t_2) \mapsto TRUE
$$

上式中的符号逐项解释如下：

1. `IMPLIES(FALSE,t_2)` 表示前提恒假。
2. 在逻辑上它可直接化简为 `TRUE`。
3. 该类 rewrite 会在 filtering / normalization 过程中截断不相关分支。

### 语义边界

1. 论文主线是 invariant operator layer，不是新的时空规约本体。
2. `foldTime`、`foldSpace` 的示例实现依赖比较强的输入格式假设，作者自己也明确指出部分示例是 naive 的。
3. operator 的价值主要在数据处理和规约后处理，不直接替代 solver 或前端建模语言。
4. normalization 策略不是唯一的，论文明确主张按 use case 选不同 processor 链。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| invariant 骨架 | `$I ::= TRUE \mid FALSE \mid AND(I,I) \mid \cdots$` | 算子层直接运行在 `BeSpaceD` invariant AST 上。 |
| 时间折叠 | `$\mathrm{foldTime}: Invariant \times A \times T \times T \times \Delta T \times (A \times Invariant \to A) \to A$` | 把时序 invariant 扫描成聚合结果。 |
| 空间折叠 | `$\mathrm{foldSpace}: Invariant \times A \times B \times B \times \Delta B \times (A \times Invariant \to A) \to A$` | 把空间规约按步扫描成聚合结果。 |
| 归一化链 | `$normalize = flatten \circ order \circ deduplicate \circ simplify$` | 通过 processor pipeline 生成可比较 normal form。 |
| ownership 特化 | `$normalizeOwnerOccupied = mergeOwners \circ normalize$` | 把 ownership-aware 数据做额外归并。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 间接支持 | 依赖底层 `BeSpaceD` invariant，不单独定义新的状态机。 |
| 事件 / 触发 | 中等支持 | 可在 invariant 里筛选 `Event` 与时间条件。 |
| 守卫 / 数据 | 中等支持 | 通过 ownership、geometry 和条件重写处理，不主打复杂离散数据分析。 |
| 层次 | 条件支持 | 体现在 AST 组合和 processor 链，不是显式层次状态图。 |
| 并发 / 同步 | 间接支持 | 主要对并发系统生成后的 invariant 做处理，而非直接处理同步语义。 |
| 时间约束 | 很强 | `filterTime`、`foldTime`、`TimePoint/Interval` 是本文主线之一。 |
| 连续动态 / 随机性 | 不直接支持 | 依托底层空间对象与外部语义，本篇主线只是 operator layer。 |
| 可执行 / 可验证性 | 很强 | 论文提供 `Scala` 实现、测试用例和 open-source 说明。 |

### 形式化问题与性质

1. 本文把 `BeSpaceD` 从“可描述”推进到“可重写、可聚合、可归一化”。
2. 时间折叠和空间折叠的价值在于把时空规约转成数值、统计或摘要对象，便于后续分析。
3. normalization 的重点不是唯一语义，而是为比较、去重和 ownership-aware merge 提供稳定表示。

## 构造方式与承载格式

### 建模入口

本文默认建模入口已经是 `BeSpaceD` invariant。新增的是：

1. filtering operators；
2. time folding；
3. space folding；
4. normalization pipelines。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Invariant` AST；
2. `Scala` higher-order functions；
3. `foldTime` / `foldSpace` 聚合函数；
4. `InvariantProcessor` 组合链。

### 交换与互操作

1. 本文不引入新的交换文件格式。
2. 它的互操作重点是让同一份 `BeSpaceD` invariant 同时服务于 solver、分析器和 operator pipeline。
3. 相比只把 invariants 交给外部求解器，这篇补的是“框架内部的数据后处理能力”。

## 配套基础设施

- 建模/编辑工具：`Scala` case classes、模式匹配和函数组合。
- 解析/交换/元模型支持：仍沿用 `BeSpaceD` invariant AST，不新增 XML/JSON 交换层。
- 仿真/执行支持：非重点；主要处理由其他环节产生的 invariant 数据。
- 验证/分析支持：filtering、time/space folding、normalization、ownership-aware merge。
- 代码生成/转换支持：不主打代码生成，重点是 AST-to-AST 的规约重写和聚合。
- 标准化或社区生态：论文说明实现是 open source，并有 `ScalaTest` 测试基础设施。

## 适用场景与需求前提

### 适用场景

适合已经采用 `BeSpaceD` 描述时空行为、并且需要从大量 invariants 中筛选窗口、做聚合统计或生成稳定比较形式的场景。

### 需求前提

1. 系统已经有 `BeSpaceD` invariant 表示。
2. 时空分析任务需要 aggregation、sub-selection 或 normalization，而不只是一次性求解。
3. 团队接受以 `Scala` 函数式方式扩展 operator pipeline。

### 不适用或高成本场景

1. 如果系统根本不使用 `BeSpaceD`，这篇单独价值有限。
2. 如果目标是前端建模语言或 solver 算法创新，而不是 invariant 后处理，这篇不是主入口。
3. 若输入 invariants 结构很不规范，文中某些 naive fold 示例会比较脆弱。

## 与相邻形式主义的关系

1. 相对 [bespaced-towards-a-tool-framework-and-methodology-for-the-specification-and-verification-of-spatial-behavior-of-distributed-software-component-systems/desc.md](../bespaced-towards-a-tool-framework-and-methodology-for-the-specification-and-verification-of-spatial-behavior-of-distributed-software-component-systems/desc.md)，前者是框架底座，本文是算子层加固。
2. 相对 [towards-verifying-safety-properties-of-real-time-probabilistic-systems/desc.md](../towards-verifying-safety-properties-of-real-time-probabilistic-systems/desc.md)，那篇把 `BeSpaceD` 接到概率实时 CPS 验证流程，这篇补 `BeSpaceD` 内部 invariants 的可处理性。
3. 相对一般 `SMT` 求解器论文，本文不是后端求解技术，而是 solver 之前的规约重写和聚合基础设施。

## 与本研究的关系

### 对 Project 1 的价值

它告诉 `project_1` 一个很实际的点：即便 LLM 已经把需求落成状态机或时空规约，后续闭环仍需要“筛选哪些时间窗口、哪些空间片段、怎样规范化比较”的 operator layer。否则大量自动生成模型会很难进入稳定的验证流水线。

### 作为目标形式主义还是中间表示

更像中间层基础设施，是规约处理和验证编排的工具化层。

### 对需求到模型生成的启发

1. 生成模型时最好考虑后续是否需要局部 window filtering 和 fold 聚合。
2. ownership、空间对象和时间对象若从一开始就结构化，后续 normalization 会更稳。
3. “可验证”不仅是能下发给 solver，也包括能做稳定的 compare / deduplicate / aggregate。

### 现实限制

1. 贡献更多在算子工程，不在形式主义母线定义。
2. 部分示例代码带明显 research prototype 特征。
3. 性能与适用性仍依赖具体 invariant 结构和 processor 设计。

## 重要的相关工作

### 奠基或前身工作

1. [bespaced-towards-a-tool-framework-and-methodology-for-the-specification-and-verification-of-spatial-behavior-of-distributed-software-component-systems/desc.md](../bespaced-towards-a-tool-framework-and-methodology-for-the-specification-and-verification-of-spatial-behavior-of-distributed-software-component-systems/desc.md)：`BeSpaceD` 框架底座。

### 同类型或同家族工作

1. 论文自己明确把 filtering、folding、normalization 视为从函数式语言迁移到时空 invariant 处理的操作层。

### 与本研究关系最紧的工作

1. 对 `project_1` 来说，这篇是“状态机/时空规约生成后如何被程序化整理”的直接侧证，和 foundation paper 必须成对看。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`BeSpaceD invariants / filtering / folding / normalization`
- 论文角色：operator layer for BeSpaceD spatio-temporal invariants
- 核心功能：为 `BeSpaceD` invariant 提供 filtering、time/space folding 与 normalization 基础设施
- 关键特性：higher-order operators、ownership-aware merge、normal-form pipeline、`Scala` 测试实现
- 构造方式：`BeSpaceD invariant -> filter/fold/normalize -> aggregated or comparable result`
- 基础设施：`Scala` case classes、pattern matching、`ScalaTest`、open-source 实现
- 适用场景：已有时空 invariants 的聚合统计、窗口筛选、结果归一化与比较
- 需求前提：系统已采用 `BeSpaceD` invariant 表示，且需要程序化后处理
- 状态：🟢 直接可用
