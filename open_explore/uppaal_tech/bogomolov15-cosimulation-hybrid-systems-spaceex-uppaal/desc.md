# Co-Simulation of Hybrid Systems with SpaceEx and Uppaal

- 问题一句话：`UPPAAL` 与 `SpaceEx` 各自擅长不同混成系统子问题，但原生语言和仿真内核彼此不兼容，难以在一个统一工作流里联合运行。
- 方法一句话：论文把两边模型自动导出为 `FMI` 的 `FMU`，再用满足 determinacy 的 co-simulation master algorithm 在宿主环境中按步协同推进。
- 解决点一句话：它把 `UPPAAL` 拉进了标准化异构协同仿真链路，并验证了用小步长协同时可以逼近单工具整体建模的轨迹结果。

## 论文定位

这篇论文属于 `🛠️ 工程/工具链` 条目，位置上接在 `UPPAAL-SMC` 初步具备混成系统统计分析能力之后，但它关注的不是继续扩查询语言或验证算法，而是**把 `UPPAAL` 变成异构 co-simulation 工具链中的一个可组合组件**。它和 [david11-statistical-model-checking-real-time](./../david11-statistical-model-checking-real-time/) 、[bulychev12-uppaal-smc-priced-timed-automata](./../bulychev12-uppaal-smc-priced-timed-automata/) 共享一条“`UPPAAL` 不只做 classical timed automata，也要接更广义 CPS 仿真/分析”的主线；再往后它又和 [nyman17-integrating-tools-cosimulation-fmi-fmu](./../nyman17-integrating-tools-cosimulation-fmi-fmu/) 形成很清晰的连续工程演进：前者先打通 `SpaceEx + UPPAAL + FMI`，后者再把 `FMU` 直接内化进 `UPPAAL SMC` 自己的执行语义里。

它的特殊价值在于：论文讨论的核心对象已经不是单一 timed automaton，而是**标准化的仿真组件接口**。这意味着作者真正回答的问题是，`UPPAAL` 如何在不丢掉自身仿真/验证语义的前提下，作为一个 `FMU` 参与多工具协作。

## 立足问题

论文面对的技术瓶颈很具体：现代 CPS 通常由多个领域模型组成，例如控制器更适合用 `UPPAAL` 这种离散/实时形式工具表达，而物理 plant 更适合用 `SpaceEx` 之类混成系统工具表达。问题在于这两边虽然都能“模拟”某些混成行为，但：

1. 建模语言不同，直接互译会丢语义。
2. 仿真引擎不同，不能天然共享时间推进和变量交换机制。
3. 若强行全部改写进单一工具，常常只能保留两边能力的交集，而不是各自最擅长的部分。

作者明确点出，单纯走“把一种语言翻译成另一种语言”的路线并不理想。因为 `UPPAAL` 的 committed locations、C-like update code、urgent behavior 等语义，并不能被 `SpaceEx` 原样承载；反过来，`SpaceEx` 擅长的 ODE/hybrid dynamics 也不是 `UPPAAL` 原生语言的强项。也就是说，这篇论文立足的问题不是“如何证明两个模型都能模拟”，而是：

1. 如何让 `UPPAAL` 和 `SpaceEx` 保留各自 native semantics；
2. 如何让二者在一个共同时间轴上交换值并协同前进；
3. 如何保证这种协同的结果不是任意的宿主执行顺序产物，而是有稳定语义的。

这个最后一点尤其关键。若 master algorithm 只是随便按某个 FMU 创建顺序调度，那么同一个系统图可能会因组件排列不同而得出不同轨迹，工程上就不可靠了。

## 核心方法

这篇论文的方法核心不是某个 reachability algorithm，而是一套**从 `UPPAAL/SpaceEx` 模型到 `FMU` 再到确定型协同推进**的工程语义链。

### 1. 把 `FMU` 视为带接口的定时状态机

作者首先采用 `Broman et al.` 的抽象，把一个 `FMU` 看成带输入、输出和内部状态的 timed state machine。对本文最关键的接口是：

$$ \mathrm{doStep}: S \times \mathbb{R}_{\ge 0} \to S \times \mathbb{R}_{\ge 0}. $$

这意味着 master algorithm 给出一个候选步长 $h$，而 `FMU` 可以：

1. 接受它，返回新的内部状态和同样的步长；
2. 或拒绝这个步长，只承认一个更小的 $h' < h$。

论文随后把 `set/get/doStep`、静态 I/O 依赖和输入输出端口都解释成协同仿真的语义契约。这里真正重要的不是 API 名字本身，而是作者明确要求 `FMU` 满足：

1. 输入输出关系静态可知；
2. 组合起来的全局 I/O dependency graph 无环；
3. 单个 `FMU` 的行为是 deterministic 的。

没有这几条，后续的 determinacy 就站不住。

### 2. 采用带回滚的两阶段步长协商

论文使用 `Broman et al. (2013)` 的 co-simulation algorithm，而不是随便设计一个 host scheduler。其关键机制是：

1. 宿主先提议一个最大步长 $h_{max}$。
2. 保存每个 `FMU` 当前状态。
3. 对所有 `FMU` 调用 `doStep(s_i, h_{max})`。
4. 若都接受，则本轮结束。
5. 若有人拒绝，则取所有返回值中的最小者：

$$ h_{min} = \min \{ h'_1, \ldots, h'_n \}. $$

6. 回滚所有 `FMU` 到保存状态，再用 $h_{min}$ 重试。

这套机制背后的关键假设是单调性：若一个 `FMU` 能接受某个较小步长，那么也能接受更小的步长。于是第二次尝试必成功，单轮协同最多两次。论文看似只是在引用已有算法，但真正的方法贡献在于：**它把 `UPPAAL` 和 `SpaceEx` 导出的 `FMU` 精确嵌进了这套带 determinacy 的推进语义里**。

### 3. 为 `UPPAAL` 和 `SpaceEx` 分别设计 `FMU` 翻译约定

两边不是简单导出“黑箱函数”，而是各自有一套针对原工具语义的映射。

对 `UPPAAL`：

1. continuous part 主要落在 clocks 与 `SMC` 扩展的 ODE 变量上；
2. discrete transitions 被分成 internal / input / output 三类；
3. 原生 channel synchronization 通过专门的离散端口变量编码成 `FMU` 输入输出；
4. 为避免语义歧义，每次至多执行一个离散动作，让 master algorithm 能细粒度控制。

对 `SpaceEx`：

1. 连续变量直接映射为 `FMU` ports；
2. 原来的同步标签没有 `input/output` 方向，于是作者人为用命名约定补出方向；
3. 为保证 determinism，采用 must-semantics 和 transition priority，强制在可走时立即走。

换句话说，方法上并不是“把两个工具都包成二进制组件”那么简单，而是**在导出层就先把原工具里容易导致 nondeterminism 或同步歧义的部分规范化**。

### 4. 明确比较 `UPPAAL` 原生并发语义与 FMI 协同语义的差异

论文很诚实地讨论了一个很重要的问题：`UPPAAL` 原生 timed automata 的并发执行采用 interleaving semantics，而 `FMI` master algorithm 在多个 `FMU` 之间会显式做值传播和同步调度。两者不是一回事。

作者用四个 timed automata 链式同步的例子说明：

1. 在原生 `UPPAAL` 里，不同 urgent/discrete 动作的 interleaving 可能给出多种零时刻顺序；
2. 在 `FMI` 框架里，master algorithm 会按依赖图推进，选出一个特定顺序；
3. 因此 `FMI` 协同语义只覆盖原语义中的一部分行为，并可能在一次协调步中实现“并行”的多点传播。

这其实是本文方法里最重要的边界说明：它不是 trying to preserve every interleaving of original NTA，而是要得到一个**工程上稳定且可重复的协同仿真语义**。

### 5. 用案例验证 co-simulation 的轨迹逼近与统计潜力

论文方法最终落在两个案例上。

第一个案例是 room heating：

1. plant 用 `SpaceEx` 建模；
2. bang-bang controller 用 `UPPAAL` 建模；
3. 然后分别导出 `FMU` 并协同仿真。

作者比较：

1. 全部在单一工具里建模/仿真的轨迹；
2. 拆成 `UPPAAL + SpaceEx` 两个 `FMU` 后的协同轨迹。

结果显示，小步长下 co-simulation 轨迹能逼近单工具整体模型；大步长下则出现 overshoot，这正是 master algorithm 只能在离散步边界感知 guard crossing 的结果。

第二个案例则更关键：作者把 stochastic controller 放在 `UPPAAL` 一侧，让 `SpaceEx` 继续提供房间动力学，然后通过大量 `FMI` simulations 做简单统计比较。这里的含义是：一旦 `UPPAAL` 可被放进 `FMI` 协同回路，它的 `SMC` 能力也就有可能被拿来服务异构组合模型。

## 解决了什么问题

这篇论文解决的不是“`UPPAAL` 单独又多支持了一种语法”，而是更偏平台级的问题。

第一，它证明 `UPPAAL` 可以作为 `FMU` 参与标准化 CPS 协同仿真，而不用把整个系统都重写进 `UPPAAL` 或 `SpaceEx`。

第二，它给出了一套明确的语义约束，保证：

1. `FMU` 的 I/O 依赖静态可分析；
2. 宿主调度满足 determinacy；
3. 不同组件排列或创建顺序不会导致任意差异。

第三，它识别并解释了 co-simulation 相对原生 timed-automata 语义的偏差来源，尤其是 interleaving 与同步传播的差异，因此这不是“黑箱集成”，而是**带边界说明的语义集成**。

第四，它把 `UPPAAL` 的统计仿真潜力带进了异构模型组合环境，为后续直接在 `UPPAAL SMC` 中内置 `FMU` 能力埋下了非常直接的技术前奏。

## 与 `UPPAAL` 技术线的关系

这篇论文和 `UPPAAL` 主线的关系主要体现在两点。

1. 它承接了 `UPPAAL-SMC` 已经不只处理纯离散 timed automata，而开始关心 ODE / hybrid / stochastic behavior 的阶段。
2. 它又明显预示了后续 [nyman17-integrating-tools-cosimulation-fmi-fmu](./../nyman17-integrating-tools-cosimulation-fmi-fmu/) 那条线：从“`UPPAAL` 能导出 `FMU`”进一步走向“`UPPAAL` 自己把 `FMU` 当作外部函数/组件吃进去”。

因此它在技术演进线上更像一个桥梁：

1. 前面连接 `UPPAAL-SMC` 的混成/统计能力；
2. 后面连接 `FMI-FMU`、外部库调用、异构控制器分析；
3. 横向上则把 `UPPAAL` 拉向更标准的 CPS 工具互操作生态。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。它把：

1. `FMU` 语义接口；
2. master algorithm；
3. `UPPAAL` 和 `SpaceEx` 的翻译约定；
4. 案例与误差来源；

都讲清楚了，但并没有把每个导出器内部实现、每个语义 corner case 都展开到可直接复刻全部工程代码的程度。

从实现可获取程度看，更适合标 `🟧 仅可执行/可使用版本可得`：

1. 论文提到 `UPPAAL`、`SpaceEx`、`Ptolemy` 三边工具与 benchmark package；
2. 也提供了案例包下载入口；
3. 但看不到这篇论文对应的完整导出器和宿主集成源码公开仓库。

因此它更像“工程能力与案例包可追”，而不是“源码级实现直达”。

## 对本研究的启发

对当前博士研究，这篇论文的启发很直接。

第一，不同形式化/仿真工具之间的协同，不一定要靠语言统一，也可以靠**语义明确的接口层**来拼接。对你后续若要把状态机验证、环境仿真、LLM 生成模块串起来，这种接口思路非常有借鉴价值。

第二，作者没有回避“组合后语义会变”这个问题，而是把差异明说并量化。对你的研究同样重要：自动生成模型、自动补场景、自动修复模型时，都应该明确“新工作流与原始语义相比偏差在哪里”。

第三，这篇论文说明 `UPPAAL` 技术线并不只是在做纯 verification kernel，也在持续向可组合 CPS 工具链扩展。若你后续要把博士课题和 `UPPAAL` 生态更紧地挂钩，这类论文是非常好的工程化切入口。
