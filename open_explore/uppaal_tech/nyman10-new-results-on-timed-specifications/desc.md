# New Results on Timed Specifications

- 问题一句话：原有 `TIOA/ECDAR` 规格理论主要解决 safety 风格问题，但对 liveness、Büchi 目标和 non-Zeno 保证还不够。
- 方法一句话：把 `UPPAAL-TIGA` 的 zone-based `SOTFTR` reachability 算法推广成 Büchi timed-game 求解，并用 sink/monitor 技术把 safety 与 Büchi 合并到 `ECDAR`。
- 解决点一句话：让 `ECDAR` 不再只会检查“能否安全实现”，还能够表达“能否无限次完成某类好行为且不落入坏状态”。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，它不是重新定义整套 `TIOA` 理论，而是在已有完整规格理论之上，补上此前相对薄弱的一段：**liveness/Büchi objectives 在 timed interface theory 里怎么做、怎么高效做、怎么做进工具**。它和 [david10-timed-io-automata-complete-specification-theory](./../david10-timed-io-automata-complete-specification-theory/) 的关系很像“理论主文 + 后续增强版”：前者把 refinement、consistency、conjunction、composition、quotient 这些 safety 主体搭起来，本文则继续回答“如果我还想约束系统无限次发生某类好行为怎么办”。

它在线路上的位置也很明确：

1. 前面已经有 `UPPAAL-TIGA` 的 on-the-fly timed-game reachability 算法；
2. 前面也已有 `ECDAR` 的 timed specification theory；
3. 本文则把 **Büchi / safety+Büchi / non-Zeno strategy** 接到这条线上。

因此，它是 `ECDAR` 从“只会 safety 风格 contract”走向“开始能说 liveness”的关键增强条目。

## 立足问题

作者面对的问题很具体。已有的 timed specification theory 已经可以讨论：

1. satisfaction
2. consistency
3. refinement
4. composition / conjunction / quotient

而这些检查大多都可以归约成 timed game 上的 safety 或 reachability 问题。但如果一个规格除了“别出错”之外，还要求：

1. 某类好状态要被无限次访问；
2. 系统不能靠 Zeno 行为假装一直满足目标；
3. 一边避开坏状态，一边持续让时间前进；

那么只靠原有 safety machinery 就不够了。

换句话说，原来的 `ECDAR` 更擅长回答：

1. 这个接口是否可实现；
2. 这个实现是否 refinement 于该规格；
3. 两个接口是否能安全组合；

但对于下面这类问题还缺少直接支持：

1. 输出玩家能否保证无限次回到某个“服务完成”状态；
2. 这种保证是否仍然成立，同时又不经过坏状态；
3. 这种“无限次成功”是不是通过 Zeno trick 假装出来的。

这使得 timed specifications 在方法上仍偏 safety-heavy，而对真实 reactive interface 来说，liveness 约束同样关键。

## 核心方法

论文的方法主干非常清楚：从现有的 zone-based reachability game 求解器 `SOTFTR` 出发，构造一个 Büchi timed-game 算法，再进一步把 safety 与 Büchi 目标合并，并落进 `ECDAR`。

### 1. 继续沿用 `TIOTS/TIOA` 双层结构

作者没有换底层对象，仍沿用：

1. 语义层 `TIOTS`
2. 语法层 `TIOA`

一个 `TIOA` 仍写成：

$$
A = (Loc, q_0, Clk, E, Act, Inv)
$$

其展开后的状态是 location 与 clock valuation 的二元对，再加上输入/输出划分与 strategy 语义。也就是说，本文不是换模型，而是在**同一个接口模型上增加更强的目标类型**。

### 2. 先回顾 `SOTFTR`：reachability timed game 的 zone 算法

`UPPAAL-TIGA` 里已有一个重要底座：`SOTFTR`。它解决的是 reachability objective，也就是玩家是否能最终强制到达一组 goal states。

该算法的关键不是普通 backward fixpoint 本身，而是它在连续时间上使用了 zones 而不是 regions。为此，作者先定义：

1. action predecessor `Pred_a(X)`
2. input predecessor `iPred(X)`
3. output predecessor `oPred(X)`
4. safe timed predecessor `cPred_t(X, Y)`

其中 `cPred_t(X, Y)` 表示：存在一个 delay 能把状态送入 `X`，且在这段 delay 过程中不会碰到 `Y`。这正是 timed game 里“既要等时间，又不能让对手趁机把你拖去坏区域”的关键操作。

然后 reachability 中真正起作用的 winning predecessor 算子写成：

$$
\pi_i(H) = cPred_t(iPred(H), oPred(States \setminus H))
$$

直观上，它表示：输入玩家能否通过一次输入或延时，把系统推进到 `H`，并同时避免输出玩家把系统引到 `H` 外。

### 3. 从 reachability 闭包提升到 Büchi 目标

有了 `SOTFTR` 之后，作者观察到：Büchi objective 本质上不是完全另一种问题，而是“找到一组真正可反复回访的好状态，然后再求可达它们的状态”。

设 `Goal` 是应被无限次访问的好状态，作者把 Büchi timed game 写成一个双层不动点：

1. 外层维护当前还可能是“真好状态”的集合 `W_j`；
2. 内层用 reachability 风格闭包，找出能再次强制到达 `Goal ∩ \pi_i(W_j)` 的状态。

最终得到的 symbolic timed Büchi 算法 `STB` 可以压成：

$$
W_{j+1} = \mathrm{SOTFTR}(Goal \cap \pi_i(W_j))
$$

这一步的高明之处在于：作者没有为 Büchi 另起一套全新 symbolic engine，而是最大程度复用了现有的 zone operations。也就是说，`STB` 仍然活在 `SOTFTR` 那套 zone 算子里，只是把 goal 的更新方式从“一次 reachability”升级成“反复可达的 goal subset”。

### 4. 把 Büchi 与 safety 合并

仅有“无限次访问 Goal”还不够，因为很多接口问题天然还带坏状态 `Bad`。作者因此定义 combined objective：既要避免 `Bad`，又要无限次访问 `Goal`。

做法很实用：把所有 `Bad` 状态通过额外输出动作 `err` 接到一个 sink location `B`，并令 `B` 不属于 `Goal`。这样一来，只要轨迹进入坏状态，对手就能走 `err` 把你送进必输 sink，于是 “Büchi + safety” 就被规约回普通 Büchi game。

从方法角度看，这一步其实是在做：

1. safety 约束不再单独维护一套算法；
2. 而是通过模型变换把它吸收到 Büchi 目标里。

这使工具实现保持统一，也让 `ECDAR` 端只需支持一套核心求解机制。

### 5. 用 monitor 处理 non-Zeno 策略

作者进一步注意到，一个看似“无限次访问好状态”的策略，可能实际上通过 Zeno 行为作弊，即在有限时间内做无限多次离散动作。对此，论文给出一个小 monitor 自动机 `Z`，引入 `NonZeno` 状态，并要求其被无限次访问。

核心思想是：

1. monitor 只有在至少过去一段真实时间后才能回到 `NonZeno`；
2. 因而“无限次回到 `NonZeno`”就意味着时间确实无限推进。

这相当于把“时间是否真的前进”也转成一个 Büchi 条件，再与原有目标一起求解。于是 `ECDAR` 不只知道某个接口“理论上可能一直成功”，还知道它是不是依赖不现实的 Zeno 行为。

### 6. 在 `ECDAR` 中实现，并用传感器案例验证

论文不是只给算法，还把这些增强落进 `ECDAR`，并用红外传感器与驱动器的接口模型做案例。

这个案例很适合说明方法价值，因为它并非单纯安全约束，而是既关心：

1. 时序协议是否满足；
2. 接口是否 consistent；
3. 某些交互是否能持续完成；
4. 是否可能因 Zeno 或 environment assumption 问题出错。

作者还展示了如何通过 conjunction 把更局部的约束（例如某些信号必须交替）与主体模型拼起来。这说明本文的 Büchi 增强并不是孤立功能，而是直接嵌回了整个 `ECDAR` 工作流。

## 解决了什么问题

这篇论文真正解决的是：`ECDAR` 之前主要是一个 safety-heavy 的 timed interface 工具，而本文让它开始能稳定处理 liveness 风格规格。

第一，它给 timed I/O specification theory 补上了 Büchi timed-game 求解能力。这样一来，接口不只可以说“别进入坏状态”，还可以说“某种好行为要一直发生”。

第二，它把 Büchi 与 safety 组合成可执行算法，因此实际建模时不必在“只表达 liveness”与“只表达 safety”之间二选一。

第三，它提供了 non-Zeno strategy 的处理方式。这一点很重要，因为在实时系统里，“无限次成功”如果不排除 Zeno，很多结果在工程上并不可信。

第四，它通过 `ECDAR` 实现与案例说明，证明这不是纯理论补丁，而是可直接用到 interface design and analysis 里的增强功能。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线上扮演的是一个“把 game-solving 能力往 liveness 再推一步”的角色。

向前，它接着：

1. `UPPAAL-TIGA` 的 reachability timed games；
2. `TIOA` 完整规格理论；
3. `ECDAR` 工具环境。

向后，它影响：

1. 后续 `real-time specifications` 线对 operators 与语义的更系统整理；
2. `ECDAR` 在 interface design 中对 liveness 的表达能力；
3. 将安全、进展、非 Zeno 等需求放到同一 contract 语境中。

如果按文库里的主线分类，它明显属于：

1. `TIOA / specification theory`
2. `ECDAR`
3. `timed games / liveness`

## 实现与材料

从内容详细程度看，这篇论文可标 `🟩 较完整`。原因是：

1. 问题定义很清楚；
2. `SOTFTR -> STB -> safety+Büchi` 的算法迁移讲得较实；
3. 还给了传感器案例和 `ECDAR` 实装；
4. 但若要完全复现所有 fixpoint 细节和证明，仍需结合前序 `SOTFTR` 与主规格理论论文一起读。

从实现可获取程度看，可标 `🟩 核心实现源码线直达`。原因是：

1. 论文明确说这些想法已经实现进 `ECDAR`；
2. 文中还给出了案例实现包；
3. `ECDAR` 这条源码线后续是可追的。

但也要注意，本文依赖的另一部分底座是 `UPPAAL-TIGA` 游戏引擎，而这部分并不是像 `UDBM` 那样单独直接暴露完整核心源码，所以“源码线直达”主要成立在 `ECDAR` 这一侧。

## 对本研究的启发

对当前博士研究，这篇论文的启发很直接：如果你的目标是把需求、模型和验证闭环组织起来，那么只会处理 safety 远远不够。

值得迁移的点主要有三条：

1. **进展目标也要显式建模**
   - 很多状态机需求并不是“别错”，而是“最终要发生、且会反复发生”。
2. **把复杂目标规约回已有求解器**
   - 本文没有重写一整套引擎，而是复用 `SOTFTR`。这对你后续若想在现有 verification profile 上扩目标类型，非常值得借鉴。
3. **对 Zeno/伪进展保持警惕**
   - 在自动化生成与修复状态机时，模型可能“看上去满足性质”，但实际上依赖不现实的无限快切换。本文的 monitor 思路很适合拿来防这种假阳性。
