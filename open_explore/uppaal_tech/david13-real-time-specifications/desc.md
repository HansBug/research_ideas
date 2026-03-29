# Real-Time Specifications

- 问题一句话：实时接口设计需要一套在语义、算子和工具算法上都更成熟的完整规格理论。
- 方法一句话：以 `TIOTS/TIOA` 为双层语义，系统统一 specification、implementation、satisfaction、refinement、consistency、conjunction、composition 与 quotient，并给出 `Ecdar` 的符号算法化路径。
- 解决点一句话：把 `TIOA` 实时规格理论整理成成熟的期刊级总成版本，成为 `ECDAR` 支线的核心理论底座。

## 论文定位

这篇论文在 `uppaal_tech/` 里属于 `⚡ 改进与扩展`，但更准确地说，它是 `UPPAAL / ECDAR` 中 `TIOA specification theory` 分支的一篇**成熟化总论文**。相较 [david10-timed-io-automata-complete-specification-theory](./../david10-timed-io-automata-complete-specification-theory/)，它不是简单重复，而是把那条理论线连同 `Ecdar` 中的工具算法、实现/规格分层、局部一致性、剪枝和 quotient 细节做了更全面的系统整理。

它的位置有点像：

1. `2010` 的 HSCC/CAV 论文给出核心理论与方法；
2. `2012` 的 `Ecdar` 论文给出工具工作流与案例；
3. 本文把整条线收束成一篇更完整、更统一的实时规格理论总成。

因此，若把 `UPPAAL` 技术演进当作时间线，这篇文章并不是开创新分支，而是把 `TIOA/ECDAR` 分支从“若干关键论文”整合成“成熟规范体系”。

## 立足问题

这篇论文立足的问题，不是“能否为实时组件写接口自动机”，而是“如何形成一套真正完整、可执行、彼此协调的实时规格理论”。这意味着它要同时解决几件事情，而不仅是定义一个模型：

1. 规格和实现如何区分。
2. 一个规格何时可实现，也就是 consistency。
3. 两个规格之间何时可替换，也就是 refinement。
4. 多个需求视角如何合并，也就是 conjunction。
5. 多个组件如何安全组合，也就是 composition。
6. 如何从全局需求与局部已有部件中反推出剩余部件规格，也就是 quotient。

论文强调，如果这些操作之间没有统一的语义基础，那么所谓“接口理论”就很容易退化成一组拼凑功能：某些算子能算，但没有模型集意义；某些操作可写，但和实现语义不一致；某些工具能跑，但只是一种 ad hoc 工程技巧。

因此，这篇论文真正盯住的是一个更高层问题：**实时接口规格理论要怎样同时满足语义完整性、组合设计需求、实现判定需求以及符号算法可行性。**

## 核心方法

这篇论文的方法是完整规格理论的全景展开。其核心可以拆成六层。

### 1. 双层语义：用 `TIOTS` 定义语义，用 `TIOA` 做有限表示

作者首先仍坚持双层建模：

1. 语义层是 `Timed I/O Transition Systems`

$$
S = (St, s_0, \Sigma, \to)
$$

2. 语法层是 `Timed I/O Automata`

$$
A = (Loc, q_0, Clk, E, Act, Inv)
$$

这么做的意义在于：

1. 理论定义不被某一种语法表示绑死。
2. 工具实现仍可回落到 `UPPAAL` 风格的时钟自动机符号表示。

这使得“理论正确性”和“工具可执行性”能同时保持。

### 2. 规格与实现分层：继续用 input-enabledness、output urgency、independent progress 划界

本文保留并系统展开了 `specification` 与 `implementation` 的核心区分。

规格要求：

1. input-enabled

实现要求在规格之上再满足：

1. output urgency
2. independent progress

这两条尤其关键。output urgency 表示可发出的输出不能被故意拖延，independent progress 则禁止实现陷入“必须等环境输入才推进”的卡死状态。用更抽象的形式写，就是：

$$
\mathrm{Implementation} \subseteq \mathrm{Specification}.
$$

但这个包含不是语法上的，而是语义条件诱导出来的。

### 3. refinement 与 model inclusion：让可替换性和实现集合包含对齐

这篇论文继续使用 timed alternating simulation 风格的 refinement，但比早期会议文更完整地把其性质讲清楚。核心目标不是单纯定义一个 preorder，而是证明：

$$
S \le T \iff Mod(S) \subseteq Mod(T).
$$

这里 `Mod(S)` 表示满足 `S` 的实现集合。这个等价非常关键，因为它保证 refinement 确实对应“更强规格的实现集合更小”，也因此能支撑 substitutability 与 compositional reasoning。

### 4. consistency / local consistency / pruning：把 realizability 做成可计算对象

本文比简短会议文更充分地展开了 consistency 问题。作者区分：

1. **consistency**
   - 是否存在至少一个实现满足该规格。
2. **local consistency**
   - 每个状态是否都满足实现所需的独立推进条件。

这一区分很重要，因为规格可能整体可实现，但局部包含坏状态或死区；这就需要通过游戏求解与 pruning 清掉不可实现部分。

其核心仍然是基于 predecessor/fixpoint 的博弈分析。也就是说，consistency 不是纯语法健全性检查，而是“环境与组件对抗下，是否存在避免错误的输出策略”。

### 5. 完整运算集：conjunction、composition、quotient 各司其职

#### 5.1 Conjunction

把同一组件的多份需求规格合并成一个共同规格。其关键性质是 implementation set 的交：

$$
Mod(S \wedge T) = Mod(S) \cap Mod(T).
$$

并在结果不局部一致时通过 pruning 进行裁剪。

#### 5.2 Composition

parallel composition 处理的是两个独立组件如何安全共同工作。这里关注的不是单个组件内部如何避免坏状态，而是环境是否存在方式使组合系统保持 useful / compatible。

#### 5.3 Quotient

这是实时规格理论“完整性”最强的标志之一。给定总规格 `T` 和已有部件 `S`，quotient 返回最宽松的缺失部件规格。直觉上满足：

$$
S \parallel X \le T.
$$

而且 `X` 在 refinement 意义下尽量宽松。本文对 pre-quotient、universal state、inconsistent state 和后续 pruning 的关系讲得比早期会议文更细。

### 6. 符号算法层：把理论算子还原成 `Ecdar` 可执行算法

这篇文章不只是讲语义，还比较明确地描述了如何在 `Ecdar` 中落地：

1. refinement 转成 game-based symbolic checking。
2. consistency / compatibility 用 timed game 与 predecessor fixpoint 处理。
3. conjunction / composition / quotient 通过产品构造再配合 pruning 实现。

这意味着本文的核心方法并非“理论与工具两张皮”，而是：

$$
\mathrm{theory} \to \mathrm{symbolic\ construction} \to \mathrm{game\ solving} \to \mathrm{pruned\ specification}.
$$

工具算法之所以可信，是因为都被放回同一套 `TIOTS/TIOA` 语义框架中解释。

## 解决了什么问题

这篇论文解决的，是 `TIOA` 实时规格理论从若干核心成果走向稳定、成熟、可复用体系的问题。

第一，它把 specification、implementation、satisfaction、refinement、consistency、conjunction、composition、quotient 全部放进一个统一框架里，而不是让这些概念各自游离。

第二，它把 refinement 和 implementation inclusion 正式对齐，从而保证“规格强弱”“可替换性”“实现集合包含”三者说的是同一件事。

第三，它把 consistency / local consistency / pruning 做成了规格理论中的核心一环，而不仅仅把它当成工具附带检查。这使 `Ecdar` 风格的规格裁剪有了坚实理论基础。

第四，它让 quotient 真正进入可操作体系。很多接口理论止步于 composition 和 refinement，而 quotient 恰恰是支持模块分解、需求反推和 assume/guarantee 合成的关键。

第五，它为 `Ecdar` 的实现奠定了稳定理论版本，使工具不再只是若干会议论文结果的拼接。

## 与 UPPAAL 技术线的关系

这篇论文和 `UPPAAL` 技术线的关系可以概括成一句话：它是 `TIOA / ECDAR` 支线的“规范化总纲”。

向前，它继承：

1. `timed automata` 与 `UPPAAL` 的时钟自动机传统。
2. `UPPAAL-TIGA` 的 timed game 求解基础。
3. [david10-timed-io-automata-complete-specification-theory](./../david10-timed-io-automata-complete-specification-theory/) 的核心理论骨架。

向后，它支撑：

1. [david12-compositional-verification-ecdar](./../david12-compositional-verification-ecdar/) 的工具化使用与案例分析。
2. [goorden23-timed-io-automata-never-too-late](./../goorden23-timed-io-automata-never-too-late/) 等后续 `TIOA` 线延伸。
3. 后续关于 randomized refinement、robustness 等工作在这条分支上的继续发展。

从分类上看，它最靠近：

1. `TIOA / specification theory`
2. `ECDAR`
3. `assume-guarantee / quotient-based design`

## 实现与材料

这篇论文的材料很扎实，而且比早期会议版明显更适合作为文库中的核心理论条目。

从内容详细程度看：

1. 定义和性质相当完整。
2. 工具算法与语义联系也讲得更明确。
3. 还讨论了 related work、工具化和未来 robustness 等方向。

它已经达到了“读者可较完整重建整套理论框架”的程度。虽然不等于把所有证明逐行展开，但对于技术线梳理来说，密度和完整性都很高。

从实现可获取角度看，论文明确以 `Ecdar` 为实现落点。工具存在、算法存在、工作流存在都很清楚；若要完整获取源码级实现细节，则仍需配合工具代码仓与前后相关论文。

## 对本研究的启发

对当前博士研究，这篇论文的价值主要体现在“规格理论层面的清晰分工”。

第一，它提醒我们：在自动状态机建模里，必须严格区分 specification 与 implementation。很多 LLM 自动产物一开始更接近 specification，如果不先承认这一点，就很容易把验证和修复目标搞混。

第二，它展示了 consistency、refinement、composition、quotient 这几种关系各有分工。对我们的“生成-验证-修复”闭环来说，这意味着不同错误类型需要不同判定关系，而不能只靠单一可达性或单一性质检查。

第三，它的 pruning 思路很适合启发自动修复。很多时候错误不是某条边局部不满足，而是某片状态区域整体已经不可实现；若能把这种坏区显式裁掉或定位出来，对后续 LLM 纠错会更有帮助。
