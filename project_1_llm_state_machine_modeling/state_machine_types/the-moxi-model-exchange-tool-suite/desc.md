# MoXI 模型交换工具套件 / The MoXI Model Exchange Tool Suite

## 基本信息

- 标题：The MoXI Model Exchange Tool Suite
- 中文标题：MoXI 模型交换工具套件
- 作者：Chris Johannsen，Karthik Nukala，Rohit Dureja，Ahmed Irfan，Natarajan Shankar，Cesare Tinelli，Moshe Y. Vardi，Kristin Yvonne Rozier
- 发表：*Computer Aided Verification*，pp. 203-218，2024
- DOI：`10.1007/978-3-031-65627-9_10`
- 链接：https://doi.org/10.1007/978-3-031-65627-9_10
- 形式主义：`MoXI / symbolic model-checking interlingua / tool suite`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：symbolic-model-checking intermediate language and translation suite
- 工具/实现获取方式：原文明确给出工具仓库 `https://github.com/ModelChecker/moxi-mc-flow`，并给出 benchmark 入口 `https://modelchecker.github.io/benchmarks`。
- 标准/格式获取方式：核心承载是 `MoXI` concrete syntax、`MoXI` JSON dialect、`SMV`、`Btor2` 与 witness 翻译链；它本身就是面向 symbolic model checking 的交换层候选。

## 简报

`MoXI` 补的是 symbolic model checking 世界里非常缺的一层“中间表示”。很多后端算法只吃低层硬件风格输入，很多前端高层模型语言又太丰富、太难直接比较。`MoXI` 的目标不是再造一个新的高层建模 DSL，而是做一个足够 expressive、又足够 machine-readable 的 interlingua，让前端语言与后端算法可以通过一套统一脚本和工具链互通。

- 形式主义定位：面向 symbolic model checking 的中间语言与翻译工具套件，而不是新的系统建模母语。
- 构造方式简述：把 `SMV` 等高层模型翻到 `MoXI`，再翻到 `Btor2` 或其他低层后端；模型检查完成后，再把 witness 映回 `MoXI` 或源语言。
- 基础设施与场景简述：依托 `SMT-LIB 2` 风格语法、`define-system / check-system` 命令、JSON dialect、translator suite 与 validator，服务 symbolic backends、benchmark reuse 与跨工具比较。

```text
SMV or other front-end -> MoXI interlingua -> Btor2 / backend checker -> witness / certificate -> back-translation
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. `MoXI` 中间语言；
2. state signature、initial condition、transition relation、invariants；
3. system composition 与 `check-system` queries；
4. witness / certificate representations；
5. translators 和 validators 组成的 tool suite。

### 核心抽象

原文说明每个 `define-system` 命令定义一个 transition system，可保守整理为：

$$
\mathcal{S} = (X_{in}, X_{out}, X_{loc}, Init(X), Trans(X,X'), Inv(X), Sub)
$$

上式中的符号逐项解释如下：

1. `X_{in}`、`X_{out}`、`X_{loc}` 分别是输入、输出和局部状态变量。
2. `Init(X)` 是初始状态条件。
3. `Trans(X,X')` 是转移关系，其中 `X'` 表示 next-state 变量。
4. `Inv(X)` 是系统不变式。
5. `Sub` 表示由其他系统做 synchronous composition 的子系统结构。
6. 这是根据 `define-system` 各字段做的保守整理，不是原文唯一官方元组。

论文明确指出 `MoXI` 语言基于 `SMT-LIB 2`：

$$
\text{MoXI logic} = \text{SMT-LIB 2} + \text{first-order temporal logic} + \text{system commands}
$$

上式中的符号逐项解释如下：

1. 基础逻辑是 many-sorted first-order logic with equality。
2. `MoXI` 在其上增加离散线性时间的 temporal layer。
3. 再进一步增加 `define-system`、`check-system` 等命令层。
4. 因而它既不像纯 SAT/SMT 输入那样太低层，也不像高层建模语言那样过重。

论文给出的 query 能力可保守压成：

$$
\mathcal{Q} = \{reachable,\ deadlock,\ fairness\text{-}conditioned\ checks,\ observer\text{-}based\ LTL\ encodings\}
$$

上式中的符号逐项解释如下：

1. `reachable` 覆盖 reachability checks。
2. `deadlock` 表示 deadlock checking。
3. `fairness-conditioned checks` 表示带环境假设与公平性条件的查询。
4. observer systems 让任意 `LTL` 规格可通过标准编码落入同一框架。

### 一个最小例子与通俗解释

论文里的最小例子是 three-bit counter：

1. 先定义 `Latch`，再定义 `OneBitCounter`，最后把三个 one-bit counter 组合成 `ThreeBitCounter`。
2. 每个系统都用 `define-system` 指定输入、输出、初始条件和转移公式。
3. 再用 `check-system` 询问“能否达到输出为 `2` 的状态”。
4. 返回结果不是只有 sat / unsat，还可以带具体 witness trace。

通俗地说，`MoXI` 像 symbolic model checking 的“中间装配线语言”。前端不用都直接对接每个后端，后端也不用分别支持每种高层语言。

### 运行 / 接受 / 转移语义

论文直接说明：

1. `MoXI` 使用离散、线性时间和 finite / infinite trace-based semantics。
2. `define-system` 用 `Init`、`Trans`、`Inv` 指定 transition system。
3. `check-system` 在已定义系统上表达 reachability / deadlock / assumption / fairness 条件下的 queries。
4. `check-system-response` 可返回 finite 或 lasso witness trace，也可返回 certificate。

这一点可保守压成：

$$
\mathcal{S} \models q
$$

其中 `q` 的结果可写成：

$$
result(q) \in \{sat,\ unsat\} \times \{trace,\ certificate\}
$$

上式中的符号逐项解释如下：

1. `q` 是一个 `check-system` query。
2. `sat` 时可返回 witness trace。
3. `unsat` 时可返回 proof certificate。
4. 这正是 back-translation 能把低层 counterexample 还原回高层模型的基础。

### 语义边界

1. `MoXI` 强调 machine-readability，因此不像 `SMV/TLA+/PROMELA/Simulink` 那样追求人类友好。
2. 当前版本重点仍在 finite-state symbolic model checking。
3. 论文明确说 asynchronous composition 计划后续支持，当前主线是 synchronous composition。
4. 它是 interlingua，不是端到端工业建模环境。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统骨架 | `$\mathcal{S} = (X_{in}, X_{out}, X_{loc}, Init(X), Trans(X,X'), Inv(X), Sub)$` | `MoXI` 里的系统由状态签名和逻辑公式定义。 |
| 逻辑层级 | `$\text{MoXI logic} = \text{SMT-LIB 2} + \text{temporal logic} + \text{system commands}$` | `MoXI` 在 SMT 层之上加时间与系统命令。 |
| 查询集合 | `$\mathcal{Q} = \{reachable,\ deadlock,\ fairness\text{-}conditioned\ checks,\ observer\text{-}based\ LTL\}$` | 支持 reachability / deadlock / fairness / observer-LTL。 |
| 结果接口 | `$result(q) \in \{sat,\ unsat\} \times \{trace,\ certificate\}$` | 可把结果统一回收为 witness 或 proof。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接承载 symbolic transition systems。 |
| 事件 / 触发 | 中等支持 | 取决于前端建模语言如何编码。 |
| 守卫 / 数据 | 很强 | 基于 `SMT-LIB` 的 typed variables 和 formulas。 |
| 层次 | 弱支持 | 不是层次状态机专用语言。 |
| 并发 / 同步 | 中等支持 | 当前明确支持 synchronous composition。 |
| 时间约束 | 弱支持 | 采用离散线性时间 trace semantics，不是 timed automata DSL。 |
| 连续动态 / 随机性 | 不支持 | 主体是 symbolic model checking 中间层。 |
| 可执行 / 可验证性 | 很强 | translators、validators、witness round-trip 都已给出。 |

### 形式化问题与性质

1. `MoXI` 的主要价值不是单个算法，而是让“新前端语言”和“新后端算法”都只需各写一次 translator。
2. 这使 benchmark reuse 与公平比较更现实。
3. 对 `project_1` 来说，它非常像“状态机生成后的统一验证 IR”。

## 构造方式与承载格式

### 建模入口

论文给出的主要入口包括：

1. `SMV` front-end；
2. `MoXI` concrete syntax；
3. `MoXI` JSON dialect；
4. `Btor2` back-end representation；
5. witness files。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `define-system` / `check-system` scripts；
2. state signatures 与 primed variables；
3. JSON schema；
4. `Btor2` model and witness；
5. translated `SMV` witness。

### 交换与互操作

这篇论文的互操作重点在：

1. `smv2moxi`：`SMV -> MoXI`；
2. `moxi2btor`：`MoXI -> Btor2`；
3. `btorwit2moxiwit`：`Btor2 witness -> MoXI witness`；
4. `moxiwit2smvwit`：`MoXI witness -> SMV witness`；
5. `validate`：对 `MoXI` concrete syntax 或 JSON dialect 做逻辑与 schema 检查。

## 配套基础设施

- 建模/编辑工具：并不追求独立 GUI，核心是 translator / validator suite。
- 解析/交换/元模型支持：`MoXI` concrete syntax、JSON dialect、`SMV` 与 `Btor2` 双向桥接。
- 仿真/执行支持：重点不是仿真，而是 symbolic checking 与 witness translation。
- 验证/分析支持：reachability、deadlock、assumptions、fairness 与 observer-`LTL` 编码。
- 代码生成/转换支持：重点是 model / witness translation，不是 deployment code generation。
- 标准化或社区生态：论文明确把 `MoXI` 设想成 international research-community standard 候选。

## 适用场景与需求前提

### 适用场景

适合需要在高层建模语言与低层 symbolic backends 之间稳定互通、希望比较不同 model-checking algorithms、或希望为新语言快速接通现有 backends 的场景。

### 需求前提

1. 源模型需能落成 finite- or infinite-state symbolic transition systems。
2. 用户愿意把高层语义压到 `MoXI` 可承载的状态签名和逻辑公式层。
3. 后端能接受 `Btor2` 或相邻 bit-precise symbolic encodings。
4. 若要做 `LTL`，最好愿意通过 observer encoding 进入 reachability framework。

### 不适用或高成本场景

如果团队首要诉求是人类友好建模、图形编辑或工业级 domain-specific abstractions，`MoXI` 不是前台建模工具。

## 与相邻形式主义的关系

相对 [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)，`JANI` 是 quantitative-modeling 交换格式，而 `MoXI` 面向 symbolic model checking；相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md) 与 [the-extended-hoa-format-for-synthesis/desc.md](../the-extended-hoa-format-for-synthesis/desc.md)，`HOA` 系列交换的是 automata / games，`MoXI` 交换的是 transition-system + query + witness 全链路；相对 [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)，`LTSmin` 用 `PINS` 做 backend abstraction，而 `MoXI` 更像公开的 textual interlingua。

## 与本研究的关系

### 对 Project 1 的价值

1. 它很适合被看成“状态机生成之后的统一验证 IR”候选思路。
2. 若未来 `project_1` 产出多种状态机或 DSL，统一先降到一层中间语义，再接多个验证后端，会比为每个目标后端单独写翻译更稳。
3. `witness` 与 `counterexample` 可回译这一点，对后续 repair 闭环尤其关键。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它明显更像中间表示，而不是最终用户直接编写的目标状态机语言。

### 对需求到模型生成的启发

1. 模型生成和后端验证应解耦。
2. 中间层不一定要“最漂亮”，但必须语义稳定、可回译。
3. witness round-trip 对“生成-验证-修复”闭环很重要。

## 重要的相关工作

- [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：quantitative 方向的中立交换层。
- [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：自动机交换层的代表标准。
- [the-extended-hoa-format-for-synthesis/desc.md](../the-extended-hoa-format-for-synthesis/desc.md)：综合方向的 automata/game 交换层扩展。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这是一篇非常典型的 symbolic model-checking 基础设施条目，适合作为“统一中间表示、translator suite 与 witness 回译链”证据正式入账。
