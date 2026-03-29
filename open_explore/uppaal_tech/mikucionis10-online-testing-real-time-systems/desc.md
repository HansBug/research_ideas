# Online Testing of Real-time Systems

- 问题一句话：实时系统的 online testing 需要同时解决 timed conformance、在线决策、物理时间戳和测试适配层四个层面的问题，单靠离线 test generation 或纯理论框架都不够。
- 方法一句话：围绕 `rtioco`、符号在线测试算法、显式 adapter 建模和 virtual time 框架，构造一条从理论到 `UPPAAL Tron` 落地的 thesis 级闭环。
- 解决点一句话：把 `UPPAAL` 的 testing 支线从“几篇论文点子”推进成可执行、可诊断、可工业接入的完整技术体系。

## 论文定位

这篇博士论文是 `uppaal_tech/` 里 `🛠️ 工程/工具链` 支线最重要的核心条目之一。它不是一篇只讲某个新公式的 theory paper，也不是单独介绍一个工具按钮的 tool demo，而是把 `UPPAAL Tron` 这一整条 online testing 路线完整铺开：

1. 前面 [mikucionis03-online-on-the-fly-testing-real-time-systems](../mikucionis03-online-on-the-fly-testing-real-time-systems/) 和 [larsen04-online-testing-real-time-systems-using-uppaal](../larsen04-online-testing-real-time-systems-using-uppaal/) 已经奠定了“在线测试可以和 timed automata / UPPAAL 结合”的方向。
2. 这篇 thesis 把方向扩成了完整栈：形式化关系、符号算法、实现结构、adapter 框架、实验、工业案例、附录手册。
3. 后面 [behrmann11-developing-uppaal-over-15-years](../behrmann11-developing-uppaal-over-15-years/) 会从工具工程史角度重新回看 `Tron` 这条分支，但真正把 testing 线讲透的仍然是这篇 thesis。

因此，在整个 `UPPAAL` 技术线里，它承担的是“testing 分支总入口”的角色。只要后续要研究 `UPPAAL` 如何从模型检查走向在线执行、在线观测和 verdict 生成，这篇就是绕不开的基础文献。

## 立足问题

这篇论文立足的问题非常具体，而且是纯理论 timed testing 文献里经常被淡化的那些“最难真正落地”的部分。

### 1. 传统 `ioco`/`tioco` 框架很强，但离真实测试环境还有距离

经典 conformance testing 框架擅长回答“实现是否符合规格”，但实时系统里真正跑测试时，会立刻碰到几个现实问题：

1. tester 和 IUT 是两个独立实体，不共享同一个物理时钟。
2. 输入输出信号通过 adapter/通信通道传输，会产生延迟、排队、交错。
3. 测试不只是离线生成一棵 test tree，而是要在执行过程中根据观察到的输出实时更新下一步动作。
4. 环境行为不是任意的，测试者通常希望只探索“部署时现实可能出现”的轨迹。

因此，这篇 thesis 不满足于沿用一个抽象的 timed conformance 关系，而是要给出一个**能和真实执行环境对接**的 timed online testing 框架。

### 2. `UPPAAL` 模型天然是 closed system，但 online testing 天然是 decoupled setup

`UPPAAL` 模型习惯把系统、环境和通信都写进一个封闭的 timed automata 网络里。但在线测试时，tester 只控制环境那一侧，IUT 在另一侧运行，双方之间隔着 adapter 和物理时间。

换句话说，模型世界和执行世界之间存在一道鸿沟：

1. 模型里同步是理想化的。
2. 现实里输入输出可能异步交错。
3. 模型里 clock 是语义对象。
4. 现实里时间只能靠本地时钟观测和时间戳近似恢复。

这篇 thesis 的核心难题，就是如何把这两层重新接起来。

### 3. 仅靠离线 test generation 不足以处理 timed non-determinism

论文明确强调，timed specifications、black-box IUT 和真实执行平台天然引入了大量非确定性：

1. 并发进程的调度次序不确定。
2. 内部转移触发时机不确定。
3. 执行时间和通信延迟有抖动。
4. 抽象模型本身也可能保留多种可接受行为。

所以测试不可能只靠“先生成完整测试树，再照着跑”。更可行的路线是：在当前估计状态集之上在线选择下一步输入和等待动作。也正因为如此，这篇论文的主战场是 online algorithm，而不是 offline test-suite generation。

## 核心方法

这篇 thesis 的方法可以概括成四个彼此扣合的层次：`conformance relation -> symbolic online algorithm -> adapter/virtual-time framework -> tool and empirical validation`。

### 1. 用 `rtioco` 把环境假设显式纳入实时符合关系

论文最重要的理论动作之一，是提出 relativized timed input/output conformance，也就是 `rtioco`。其核心对象有三个：

1. `p`：implementation under test。
2. `s`：requirements specification。
3. `e`：environment assumptions。

作者不再假设 tester 会去挑战一切理论上可能的输入轨迹，而是明确把环境模型 `e` 放进关系里。它的定义可以压成：

$$
p \mathrel{\mathrm{rtioco}_e} s \iff \forall \sigma \in \mathrm{TTr}(e).\ \mathrm{Out}(\langle e,p\rangle \text{ after } \sigma) \subseteq \mathrm{Out}(\langle e,s\rangle \text{ after } \sigma)
$$

这个定义非常关键，因为它把“测试应该覆盖什么输入时序”从一个隐含假设，提升成了规格的一部分。这样得到几个直接好处：

1. 测试者只探索现实环境允许的轨迹，不再把资源浪费在不现实的路径上。
2. 当测试中断、输入被拒绝或环境本身不再允许继续时，可以给出更合理的 inconclusive 解释。
3. 规格不仅描述系统要求，也描述系统将面对什么环境。

论文进一步证明，在输入使能前提下，`rtioco` 可以化为带环境约束的 timed trace inclusion：

$$
p \mathrel{\mathrm{rtioco}_e} s \iff \mathrm{TTr}(p) \cap \mathrm{TTr}(e) \subseteq \mathrm{TTr}(s) \cap \mathrm{TTr}(e)
$$

这说明 `rtioco` 不是凭空定义的新关系，而是把 timed trace inclusion 用更适合 testing 的方式重新组织了一遍。

### 2. 定义 observable composition，把 tester 视角下的交互留在语义里

为配合 `rtioco`，论文还引入了 observable composition。这里最重要的观念是：虽然 `environment` 和 `implementation` 组合后形成的是封闭系统，但它们之间的输入输出交互对 tester 来说仍然是可观察的。

这一步的作用在于：

1. 语义上仍保留“系统与环境之间是谁给谁发了什么”的结构。
2. 后续定义 `Out(after σ)` 时，可以精确对着 tester 能看到的交互轨迹说话。
3. 为 online algorithm 提供自然的“当前环境轨迹下可能发生什么”语义基础。

如果没有这一层，后面的在线测试算法就很难把“模型闭包”与“测试观测”统一起来。

### 3. 设计抽象 online testing 算法：实时维护状态集估计

论文随后给出抽象 online testing 算法，核心思想非常清楚：测试过程中不维护一个确定状态，而是维护一个**当前可能状态集合**。

因为 tester 对事件发生时刻只能得到区间估计，所以每次观测到一个动作时，都会把它写成带时间区间的事件，再把当前状态集做一次 `after` 更新：

$$
Z := Z \text{ after } ([t_{\min}, t_{\max}])a
$$

在此基础上，算法每轮都做三件事：

1. 先消费输出缓冲区，把已经观察到的输出作用到当前状态集。
2. 再计算接下来允许的输入事件和可延迟区间。
3. 在输入或延迟之间在线选择下一步测试原语。

论文把这两类关键计算都形式化了：

1. `Events(Z, A)`：从符号状态集 `Z` 中求给定动作集合里哪些事件可能发生，以及它们可发生的时间区间。
2. `MaxDelay(Z, f)`：在未来时界 `f` 内，系统最多还能合法延迟多久。

这里最重要的方法特征是：**online testing 被组织成“状态集估计 + 在线选择”的循环**，而不是“事先铺开一棵巨大的测试树”。这对于 timed non-determinism 和大模型来说尤其重要。

### 4. 用时间戳区间把现实物理时间映射回模型时间

这是整篇 thesis 最有工程味、也最难做干净的部分。tester 观察到某个输入或输出时，并不知道它在模型语义里发生在一个精确实数时刻，只知道：

1. 自己本地时钟在某两个读数之间观察到了这个事件。
2. 这个事件可能还穿过了 adapter 和通信缓冲区。

论文因此采用区间时间戳而不是点时间戳。也就是说，tester 并不声称“事件发生在 `t`”，而是保守地说“事件发生在 `[t_1, t_2]` 之间”。这使得状态估计变成 over-approximation。

作者很明确地指出，这种 over-approximation 的代价是：

1. 可能让一些实际上没发生的模型行为也被认为可能。
2. 因而可能出现 false pass。
3. 但不会产生 false fail。

也就是说，这套映射是按 testing 工具最重要的保守性要求设计的：宁可不够敏感，也不能把正确实现误判为错误。

### 5. 用符号技术复用 `UPPAAL` 内核，而不是重造一套 testing engine

论文的另一个非常关键的工程决策，是不重新发明一套在线测试求解器，而是直接复用 `UPPAAL` 的符号底层。

这里复用的核心包括：

1. timed automata 网络表示。
2. zone/DBM 操作。
3. reachability 风格的状态空间操作。
4. pipeline 风格的 engine 组件。

在实现层，`Tron` 增加了一组新的 symbolic state filters，用来支持：

1. delay closure。
2. action transition。
3. 可用输入动作计算。
4. verdict 所需的 allowed transitions 追踪。

因此 `Tron` 不是平地起楼，而是把 online testing 算法嵌进了 `UPPAAL` 已有的符号分析管线。这也解释了为什么 testing 支线最后没有和主工具完全脱钩。

### 6. 显式建模 adapter，而不是假设共享全局时钟

第四章是整篇 thesis 最值得认真看的工程部分之一。作者不接受“tester 和 IUT 共享一个理想参考时钟”这种太强的假设，而是明确提出：

1. adapter 必须作为模型的一部分显式表示。
2. tester 只用自己本地时钟打时间戳。
3. 输入输出在 adapter 中的排队、延迟和交错，都需要进入规格模型。

论文给出的 partitioning 很清楚：

1. `Environment assumptions`
2. `Adapter communication`
3. `Implementation requirements`

`Uppaal Tron` 只把 `inp_t` 和 `out_r` 这种 tester 侧可观察接口当作真正的观测点。这样做的意义在于：

1. IUT 不需要暴露内部时钟机制。
2. 输入输出交错由 adapter 模型显式承担。
3. tester 与 IUT 的时间观感不一致，也能通过模型解释。

这实际上把“测试工具如何接入真实系统”从工程细节提升成了形式化对象。

### 7. 用 virtual time 框架控制执行平台噪声

为了验证 online testing 思路本身，而不是让操作系统调度和物理通信噪声淹没结论，论文又提出了 virtual time framework。

它的核心思路是：

1. 劫持 IUT 和 tester 里的 timed system calls。
2. 用一个共享的 virtual clock 协商时间推进。
3. 只有当所有参与线程都同意等待时，虚拟时间才往前走。

这样做带来两个效果：

1. 可以在“实验室条件”下更干净地验证 online testing 算法本身。
2. 可以重放和复现实验过程，更容易定位 timing bugs。

对这篇 thesis 而言，这一步非常重要，因为它证明作者不是只想写一个“理论上可行”的 testing 框架，而是认真考虑了执行平台噪声如何影响实验可信度。

### 8. 用工业案例和 mutation/coverage 实验验证整条链

论文并没有停在算法与工具说明，而是给了大量实验：

1. 基础功能测试。
2. 时间精度和反应时间基准。
3. code coverage 实验。
4. mutation 实验。
5. Danfoss EKC 制冷控制器案例。

其中几个点尤其值得注意：

1. `Tron` 在标准 PC 上的即时反应时间可以做到亚毫秒级量级，文中测得最好大约在 `0.1ms` 到 `0.5ms` 范围。
2. mutation study 不只是为了“报个数字”，而是用来检验 online tests 是否真能发现实现中的时间/并发类问题。
3. Danfoss 案例说明这条路线并不只适合学术 toy example，而是能接到工业控制器。

所以从“问题定义 -> 算法 -> 工具 -> 工业实验”这个完整度上看，这篇 thesis 在整个 `UPPAAL` 文库里都属于非常高完成度的条目。

## 解决了什么问题

这篇论文解决的是一个长链条问题，而不是某个单独局部问题。

### 1. 理论上，它把 timed conformance 从“抽象 relation”推进到“带环境假设的 testing relation”

`rtioco` 的提出，解决了“现实测试并不会穷举所有不现实环境”的问题。它让 testing relation 更贴近部署条件，也更适合作为 online testing 的基础。

### 2. 算法上，它给了真正可执行的 symbolic online testing loop

也就是：

1. 基于时间戳区间更新状态集。
2. 基于状态集在线计算输入和延迟选择。
3. 持续输出 verdict 与诊断信息。

这让 testing 不再停留在离线 test-case generation。

### 3. 工程上，它把 adapter、时间戳和执行环境噪声这些最难的现实问题放进了模型

这一步对真实落地尤其关键。很多 testing 论文默认略过 adapter；这篇 thesis 则反过来把 adapter 明确当作形式化对象建模。

### 4. 工具上，它把 `UPPAAL` testing 支线做成了一套完整平台

不仅有引擎，还有手册、接口、实验和工业案例。就“把一条研究线真正做成可运行工具”这一点而言，这篇 thesis 的完成度非常高。

## 与 UPPAAL 技术线的关系

这篇 thesis 在 `UPPAAL` 时间线里的作用可以概括成：它让 `UPPAAL` 从“验证模型”进一步走到“在线接实现、边测边判”。

更具体地说，它和其他支线有三层关系：

1. **与 timed automata / symbolic engine 主线的关系**
   - 它大量复用了 `UPPAAL` 的 zone/DBM/engine 机制。
   - 所以 testing 不是平行宇宙，而是主引擎的一个新用法。
2. **与 specification theory 支线的关系**
   - 它使用 TIOTS、timed traces、conformance 这些对象。
   - 后续 `Ecdar` 那条更偏接口/规约的线，会把这些对象系统化得更彻底。
3. **与工程/工业落地主线的关系**
   - 它是 `UPPAAL` 诸分支里最重视“如何接真实系统接口”的条目之一。

如果要理解 `UPPAAL` 为什么不只是学术验证器，而是能往 testing / synthesis / control 方向继续生长，这篇 thesis 是非常重要的证据。

## 实现与材料

- 内容详细程度：`🟢 复现级`。这是 thesis 级材料，包含理论、算法、实现、实验和附录手册，足够支持后续做深度复现和对照。
- 实现可获取程度：`🟧 仅可执行/可使用版本可得`。论文和手册能直接支撑理解 `Tron` 的工作方式，但从当前材料不能确认完整源码公开可得。
- 关键材料线索：
  - thesis 主文档本身。
  - 附录 `Uppaal Tron Manual`。
  - 相关 conference papers 作为更短版本入口。
- 复现注意点：
  - 真正复现时必须同时看主文档和附录手册。
  - adapter/virtual-time 部分不能只读理论章节，否则会低估落地难度。

## 对本研究的启发

这篇 thesis 对当前博士研究的启发非常直接，尤其适合你现在这条“生成-验证-修复”路线。

1. **要把环境假设显式建模**
   - LLM 生成状态机后，如果验证与测试不把环境假设写进模型，很容易做出脱离实际部署的分析。
2. **要把在线观测误差当作一等问题**
   - 真实系统里的日志、传感器、接口时间戳都不精确。
   - 这篇 thesis 提醒我们：如果后续要把模型接到真实运行数据，必须把“不精确观测”显式放进语义和算法。
3. **要允许“先粗测找错，再深证确认”**
   - `Tron` 的工作方式本质上是围绕当前状态集持续收缩和判定。
   - 这很适合和 LLM 生成的候选模型形成闭环：先在线刺激/找错，再回到模型修复。
4. **要重视 adapter 层**
   - 在控制系统场景里，需求、模型、实现之间往往隔着协议、接口和信号转换层。
   - thesis 里对 adapter 的处理方式，对后续做模型到实现的映射尤其值得借鉴。

总的来说，这篇论文最重要的价值不只是“UPPAAL 也能做在线测试”，而是它给出了一条完整路径：怎样把形式化 timed 模型真正接到现实执行过程中去。
