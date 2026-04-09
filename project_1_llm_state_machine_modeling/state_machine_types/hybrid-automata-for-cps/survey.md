# 面向网络物理系统形式化建模与验证的混成自动机综述 / Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems

## 基本信息

- 标题：Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems
- 中文标题：面向网络物理系统形式化建模与验证的混成自动机综述
- 作者：Shankara Narayanan Krishna，Ashutosh Trivedi
- 发表：`Journal of the Indian Institute of Science`, 93(3), 2013
- DOI：原文未提供
- 链接：https://journal.iisc.ac.in/index.php/iisc/article/view/2204
- 综述主题：`Hybrid Automata` 在 CPS 中的建模意义、LTL 验证框架与可判定子类边界
- 对象类型：🧱
- 覆盖时间范围：以 1990s 早期 hybrid/timed automata 经典工作为起点，主体覆盖至 2013 年前后的关键结果
- 覆盖主类：🌊 ⏱️
- 补充材料/数据获取方式：原文无单独数据集，但给出大量定理、工具和子类文献线索
- 原文是否给出系统比较表：原文未用单一汇总表，但按“通用模型 -> 可判定子类 -> 工具/案例”结构清晰展开

## 综述范围与结论

该文把 `Hybrid Automata` 放在 `CPS` 语境下讨论：离散控制与连续物理环境耦合时，为什么传统有限状态机不够、为什么 `Timed Automata` 仍然不够，以及 `Hybrid Automata` 在何处获得表达力、又在何处失去可判定性。原文的主结论非常明确：一般 `Hybrid Automata` 的验证问题很快就会走向不可判定，真正可落地的关键在于限制动力学并选择合适子类。

- 覆盖范围：一般 `Hybrid Automata`、`Timed Automata`、`Multi-rate / Rectangular Hybrid Automata`、`Piecewise-Constant Derivative systems`
- 主要比较轴：离散/连续耦合方式、动力学类型、LTL 可判定性边界、有限双模拟 quotient、工具支持
- 对本 collection 的直接价值：它能帮助 `project_1` 判断何时需要从离散状态机升级到混成模型，以及升级后的代价是什么

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| 🌊 | General Hybrid Automata | 重点 | 定义对象 | 连续变量 + 离散模式切换的总框架 |
| ⏱️ | Timed Automata | 重点 | 对比对象 | 作为最早的可判定子类和基准 |
| 🌊 | Multi-rate Hybrid Automata | 重点 | 子类对象 | 不同变量可有不同常数速率 |
| 🌊 | Initialized Rectangular Hybrid Automata | 重点 | 子类对象 | 通过初始化约束恢复可判定性 |
| 🌊 | Piecewise-Constant Derivative Systems | 重点 | 子类对象 | 展示“看似简单也会高度不可判定”的边界案例 |

## 分类轴与比较框架

原文主要沿以下逻辑组织：

1. 动力学维度：离散系统、连续系统、混成系统。
2. 变量流动维度：统一常速率、分模式常速率、矩形区间速率、分片常导数。
3. 逻辑与验证维度：以 `LTL model checking` 为主线。
4. 可判定性维度：是否存在 finite bisimulation quotient，是否可规约到 `Timed Automata`。
5. 扩展维度：原文明确点出但不展开 `game-theoretic`、`probabilistic`、`priced` 扩展。

因此它不是“混成自动机百科全书”，而是一篇很强的问题导向综述：什么能验证，为什么能验证。整篇文章的比较也不是简单按名字列模型，而是按“**动力学复杂度增加之后，验证会在什么点失控**”来组织。

| 形式主义/子类 | 连续动力学能力 | 是否有有限双模拟/有限抽象主线 | `LTL`/可达性结论 | 原文强调的关键原因 | 对本 collection 的意义 |
|---|---|---|---|---|---|
| General Hybrid Automata | 最强，可含一般连续动力学 | 通常没有 | 原文明确视为一般情形不可判定 | 连续变量与离散切换耦合过强 | 说明混成模型不是默认输出目标，而是高门槛上位模型 |
| Timed Automata | 连续部分退化为统一时钟流动 | 有，典型是 region equivalence | 可判定，是最早成熟子类 | 所有 clocks 以统一速率流动，结构最受控 | 是从离散状态机升级到“时间”而非“通用连续动力学”的首选 |
| Multi-rate Hybrid Automata | 每个变量可有不同常速率 | 一般不足以保证 | 原文指出一般 multi-rate 仍不可判定 | 速率一旦按变量或模式区分，复杂度迅速上升 | 表达力明显增强，但很快超出稳健验证边界 |
| Initialized Rectangular Hybrid Automata | 允许矩形速率区间，但加入初始化限制 | 有，希望通过约束恢复 | 可判定 | 初始化/reset 约束把系统重新拉回可分析区域 | 是“怎样给混成模型加约束才能重新可验证”的典型教材 |
| PCD systems | 分片常导数，局部看似简单 | 很弱 | 三维及以上高度不可判定，二维才有正结果 | “简单连续动力学”并不自动等于“好验证” | 能提醒后续不要被直觉误导，以为简单分片就足够安全 |

| 维度 | Timed Automata | Initialized Rectangular / Restricted HA | General Hybrid Automata |
|---|---|---|---|
| 需求需要补充的信息 | clocks、guard、reset、invariant | 还要给出每模式速率范围与初始化约束 | 还要给出更一般的流动方程与切换约束 |
| 可验证性 | 高 | 中，取决于限制是否满足 | 低 |
| 工具成熟度 | 高 | 中 | 中但依赖强假设 |
| 对 `project_1` 的现实可用性 | 强 | 条件可用 | 适合做特例目标，不适合默认目标 |

## 构造方式与表示格式版图

| 形式主义 | 图形表示 | 文本/数学承载 | 机器可处理承载 | 标准/交换格式 | 原文体现出的主要限制 |
|---|---|---|---|---|---|
| General Hybrid Automata | 是 | 守卫、reset、微分/flow 约束需要文本或公式表达 | 多依赖专用工具输入或数学定义 | 原文未给统一标准 | 真正难点不在“画状态”，而在精确定义连续动力学 |
| Timed Automata | 是 | clocks、guards、invariants、resets 可被工具 DSL 稳定承载 | 工具私有 DSL 最常见 | 无统一标准，但工具承载成熟 | 交换格式弱，但工具生态强，足以支撑工程使用 |
| Multi-rate / Rectangular Hybrid Automata | 是 | 常数速率或矩形速率谓词 | 更偏理论与工具受限输入 | 无 | 需要严格满足子类限制，否则很快滑向不可判定 |
| Initialized Rectangular Hybrid Automata | 是 | 还要显式写出 initialization/reset 规则 | 与 rectangular/multi-rate 工具输入强相关 | 无 | 语法负担比 timed automata 大得多 |
| PCD systems | 弱 | 主要靠区域划分与分片常导数公式 | 几乎不体现为统一工程承载 | 无 | 更像理论边界对象，不像通用工程交换对象 |

原文几乎不讨论统一交换格式，这也意味着：混成自动机当前更像“验证理论和专用工具对象”，而不是“已有稳定标准承载的交换对象”。

| 路线/子类 | 自动生成最难的输入项 | 为什么难 |
|---|---|---|
| Timed Automata | clocks、上界/下界、reset 点 | 这些信息还能从需求里相对稳定抽取 |
| Restricted HA | 每模式速率范围、初始化条件 | 需要需求或控制设计文档显式给出连续动力学假设 |
| General HA | 一般流动方程与切换条件 | 对输入需求质量和物理建模知识要求极高 |

## 基础设施与生态版图

| 工具/谱系 | 主要支持对象 | 支持能力 | 成熟度 | 原文体现出的前提或限制 |
|---|---|---|---|---|
| `UPPAAL`、`Kronos`、`RED` | `Timed Automata` | 可达性、模型检验、实时分析 | 高 | 依赖 clocks 语义，不处理一般连续动力学 |
| `HyTech` | 受限混成/线性混成子类 | reachability、symbolic analysis | 中高 | 更适合受限流动与线性约束 |
| `PHA Ver` / `Phaver` | 多面体/受限混成系统 | 混成可达性分析 | 中高 | 子类限制和数值近似前提明显 |
| 数值仿真工具（如文中提及 `Matlab` 背景） | 连续动力学部分 | 仿真与近似分析 | 高 | 更像数值实验，不直接等价于形式验证 |

| 维度 | Timed Automata 工具线 | Restricted Hybrid 工具线 | General Hybrid |
|---|---|---|---|
| 工具数量与成熟度 | 高 | 中 | 中但可用范围窄 |
| 典型分析对象 | 实时逻辑与时钟约束 | 受限连续动力学 | 理论上最强，实践上最难 |
| 对需求建模的反馈价值 | 强 | 中 | 弱到中 |

与时间自动机相比，混成自动机的工具生态更依赖子类限制和建模假设，工程门槛明显更高。

## 适用场景与需求映射

| 形式主义 | 适用场景 | 需求前提 | 为什么适合 | 不适合的情况 |
|---|---|---|---|---|
| General Hybrid Automata | 离散控制与连续物理过程紧耦合的 CPS | 需求里必须保留连续状态演化与切换条件 | 能同时表达模式切换与连续演化 | 只需离散事件或简单时钟约束时 |
| Timed Automata | 强时间约束但物理演化可抽为 clocks | 连续部分可忽略或离散化，时限能写成 guards/invariants | 可判定性和工具链最好 | 需要真实微分方程和连续守卫时 |
| Initialized Rectangular Hybrid Automata | 连续速率受限且可通过 reset/初始化保持分析性 | 能接受初始化限制并提供速率范围 | 在表达力与可验证性之间取得折中 | 速率切换频繁且不愿 reset 时 |
| PCD systems | 理论边界分析、特定低维连续系统 | 更关注 decidability 边界而非统一工程实现 | 有助于理解“多维连续分片系统”的难点 | 需要通用工程建模与统一工具链时 |

| 需求里出现的信号 | 更适合的形式主义 | 原因 |
|---|---|---|
| 只有状态、事件和时间上界/下界 | `Timed Automata` | 不必引入更重的连续动力学 machinery |
| 出现模式切换下的不同常速率/受限连续区间 | restricted `Hybrid Automata` | 可以显式建模流动，但仍有机会保住可验证性 |
| 出现一般 ODE、真实物理过程闭环耦合 | general `Hybrid Automata` | 只有这类模型才足够表达，但验证成本会显著上升 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

对于大多数软件需求建模任务，`Hybrid Automata` 不应成为默认输出，因为它要求的输入前提比普通状态机高得多：不仅要识别状态和事件，还要识别连续变量、流动方程和切换守卫。更现实的策略是把它视为高阶目标或验证补充目标。

### 对中间表示设计的启发

如果未来需求中包含物理量演化、采样控制、连续约束，中间表示必须能区分三层信息：

1. 离散控制状态。
2. 连续变量与流动规律。
3. 切换 guard/reset 与可判定子类约束。

否则模型容易落入“表达得出，但验证不了”的区域。

### 对后续扩库方向的启发

后续应优先沿以下方向补单篇条目：

1. 一般 `Hybrid Automata` 奠基定义。
2. `Timed Automata` 作为可判定子类的衔接文献。
3. `Initialized Rectangular Hybrid Automata` / `What’s Decidable...` 这一判定边界线。
4. `HyTech`、`PHA Ver` 这类工具线。

### 原文未覆盖但本研究仍需补的空白

原文明确排除了博弈、概率和 priced 扩展的详细讨论；若 `project_1` 未来涉及资源、能耗、不确定性或控制合成，这些方向需要额外补库。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1993 | General Hybrid Automata | Alur, Courcoubetis, Henzinger, Ho, `Hybrid Automata: An Algorithmic Approach to the Specification and Verification of Hybrid Systems` | 一般混成自动机的经典起点 | 优先补单篇 `desc.md` | 🔴 |
| 1994 | Timed Automata | Alur, Dill, `A Theory of Timed Automata` | 原文把它作为最关键的可判定子类基准 | 优先补单篇 `desc.md` | 🔴 |
| 1995 | PCD systems | Asarin, Maler, Pnueli, `Reachability Analysis of Dynamical Systems Having Piecewise-Constant Derivatives` | 典型边界案例，帮助理解“简单动力学也会不可判定” | 先找原文并评估是否入库 | 🟡 |
| 1998 | Decidability boundary | Henzinger et al., `What’s Decidable About Hybrid Automata?` | 判定边界最关键的参考之一 | 优先补单篇 `desc.md` | 🔴 |
| 1997 | Tool line | Henzinger et al., `HyTech` tool paper | 混成系统工具主线入口 | 优先补工具条目 | 🟠 |
| 2005 | Tool line | Frehse, `Phaver: Algorithmic Verification of Hybrid Systems Past HyTech` | 补足 `PHA Ver` / `Phaver` 工具谱系 | 先找原文并补 `desc.md` | 🟡 |

## 文献分类总结

- 综述主题：混成自动机在 CPS 中的建模与验证
- 对象类型：🧱
- 覆盖主类：🌊 ⏱️
- 覆盖的形式主义：一般 `Hybrid Automata`、`Timed Automata`、`Multi-rate/Rectangular`、`PCD`
- 是否覆盖构造方式/基础设施：部分覆盖，偏建模结构与工具，不涉及统一交换格式
- 主要价值：把“为什么需要混成自动机”以及“什么情况下还能验证”讲得非常清楚
- 状态：🟢
