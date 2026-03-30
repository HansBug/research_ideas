# A Game-Theoretic Approach to Real-Time System Testing

- 问题一句话：早期 `UPPAAL` testing 方法大多要求 output urgency 和 isolated outputs，难以覆盖真正带 uncontrollable outputs 与时间不确定性的实时系统。
- 方法一句话：论文把规格建成 `Timed I/O Game Automata`，把 test purpose 写成 timed control query，再用 `UPPAAL-TIGA` 合成 winning strategy，并把该策略当成自适应 test case 执行。
- 解决点一句话：它把实时测试从“固定轨迹生成”推进到“博弈式策略生成”，显著放宽了可处理系统的行为假设。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `⚡ 改进与扩展`，而且是 testing 分支里的一个明显代际升级节点。与 [hessel04-time-optimal-real-time-test-case-generation-uppaal](../hessel04-time-optimal-real-time-test-case-generation-uppaal/) 相比，它不再主要追求“最快到达某个测试目标”，而是正面处理一个此前更麻烦的事实：很多系统的输出并不是 tester 能完全预测和强迫的。

它与 `TRON` 和早期 offline testing 的关系可以概括成：

1. 早期方法更像从规格里抽单条 test sequence；
2. 本文则把 testing 改写成 controller 与 plant 的 timed game；
3. 因而 test case 不再是固定 trace，而是能根据 SUT 运行时选择动态调整的 winning strategy。

所以它真正推进的是 testing 的**语义模型**，而不只是工具接口。

## 立足问题

论文开篇就点出早期 real-time testing 的一个关键局限：很多方法为了让测试生成变得干净，会对规格施加两个非常强的限制。

1. **output urgency**
   - 只要系统能发输出，就必须立即发。
2. **isolated outputs**
   - 若某个状态能发输出，就不能同时接受输入，也不能在多个输出之间摇摆。

这些限制在理论上确实很方便，因为 tester 可以把系统看成几乎“按脚本演”的对象。但现实系统并不总这样：

1. 某个输出可能由环境、调度器或内部竞争决定，tester 并不能控制；
2. 某个输出可能在一段时间窗口内发生，而不是固定时刻发生；
3. 一个状态下也可能同时允许继续等待、接受输入或在多个输出之间非确定选择。

于是早期 testing 流程就会失去覆盖面。很多更真实、更自然的 timed models 被迫先重写成更僵硬的形式，甚至因此丢掉原始时序结构。

因此，本文真正面对的问题不是“如何再快一点生成测试”，而是：

1. 如何让测试模型允许 uncontrollable outputs；
2. 如何容纳 outputs 的 timing uncertainty；
3. 在这两点成立时，test generation 还能否自动进行，并保持正确性。

作者给出的答案，是把 testing 重新理解成一个博弈问题：tester 是 controllable player，系统及其环境行为则体现在 uncontrollable player 一侧。

## 核心方法

方法主干可以拆成四步：先把规格从普通 TA 升级成 `TIOGA`，再用 `tioco` 固定正确性语义，然后把 test purpose 编成 timed-game control objective，最后把 `UPPAAL-TIGA` 输出的 winning strategy 直接当 test case。

### 1. 用 `Timed I/O Game Automata` 表示 tester 与 SUT 的对抗关系

论文引入的核心模型是 `Timed I/O Game Automata` (`TIOGA`)。它本质上是 timed game automata 的一个 I/O 化版本，把动作分成：

1. input actions
2. output actions

并把两类动作分别解释成：

1. tester 可控的输入；
2. 系统不可控的输出。

也就是说，`Act = Act_{in} \cup Act_{out}`，其中 controllable actions 对应输入，而 uncontrollable actions 对应输出。这样一来，规格不再是“只会按既定脚本走的对象”，而是一个允许环境/系统在关键分支上自己做决定的 timed game。

这一步直接解决了早期 testing 的两个痛点：

1. 不要求 output urgent；
2. 不要求 isolated outputs。

因此 timing uncertainty 和 output non-determinism 都能自然落入模型。

### 2. 用 `tioco` 作为 conformance 语义，而不是发明新的 pass/fail 标准

虽然模型换成了 game，论文并没有抛弃 testing 社区已有的 conformance 关系，而是继续使用 timed input-output conformance `tioco`。

其核心思想仍然是：对规格允许的所有 timed traces，实施系统在任意前缀之后给出的输出集合，不能超出规格允许的输出集合：

$$ I \;\mathrm{tioco}\; S \iff \forall \sigma \in TTr(S),\; Out(I \; after \; \sigma) \subseteq Out(S \; after \; \sigma) $$

这里很重要的一点是：在 timed setting 下，“delay” 也被视作一种可观察输出行为的一部分。于是测试时不只是看“发错了什么动作”，也看“是否等太久了”。

因此，本文不是另起炉灶，而是在 `tioco` 框架里重新设计 test generation 的机械过程。

### 3. 把 test purpose 翻译成 timed control objective

有了 `TIOGA` 之后，测试目标就可以被写成一个 timed control problem。论文的 test purpose 不再只是非正式描述，而是显式写成 `UPPAAL-TIGA` 能理解的 control query，例如某类 reachability 目标：

$$ \texttt{control: A<> K} $$

其中 `K` 是一组 goal states。含义是：tester 是否存在一个策略，使得无论系统的 uncontrollable outputs 如何发生，最终都能把运行导向 `K`。

这一步非常关键，因为它把 test generation 的核心问题从“从规格里抽一条测试轨迹”改写成：

1. 合成一个 controllable player 的 winning strategy；
2. 该策略要对所有系统端的可能响应都成立。

这就天然得到自适应测试，而不只是固定脚本测试。

### 4. 用 `UPPAAL-TIGA` 合成 winning strategy，并把它直接当 test case

论文真正借力的工具是 `UPPAAL-TIGA`。对于给定 `TIOGA` 和 goal set `K`，它会生成 state-based winning strategy `f`。文中把 supervised run 定义得比较清楚：若当前状态上策略建议某个 controllable action，就发该输入；若策略建议等待，就允许时间推进，直到需要进一步动作或系统自行输出。

于是 test case 不再是一条固定 alternating sequence，而是一个策略对象：

$$ f : S \to Act_c \cup \{\lambda\} $$

其中 `\lambda` 表示当前不主动出手、继续等待。

这意味着测试执行时，tester 可以根据 SUT 的实际输出和当前状态继续查询策略，而不是在第一处分支偏离后就只能给出 inconclusive。

### 5. 测试执行算法本质上是“规格 + 策略 + 黑盒实现”的联机对照

论文给出的执行算法很直接。输入包括：

1. 规格 `S`
2. 黑盒实现 `I`
3. 目标集合 `K`
4. winning strategy `f`

执行时不断维护当前已观察 trace `\sigma`，并循环做：

1. 若策略要求发输入，则发给实现；
2. 若策略允许等待，则等待某个时长；
3. 若在等待期间实现提前输出，则检查该输出在当前规格前缀下是否被允许。

若输出不在 `Out(S after \sigma)` 里，就判 `fail`；若最终顺利到达目标 `K`，则判 `pass`。

这说明本文的策略不是纯离线产物，而是测试执行时持续被 consult 的对象。

### 6. Soundness / partial completeness 建立了“策略式测试”的理论地基

论文没有止步于方法描述，而是还给出 soundness 和 partial completeness 论证。

直觉上：

1. 若存在失败测试运行，则实现确实不符合规格；
2. 对给定 test purpose，若实现相对该 purpose 不符合规格，则存在某条失败运行可被该方法抓到。

这非常重要，因为一旦 test case 从固定 trace 升级成 strategy，很多人会担心 pass/fail 语义是否还稳。本文正是在说明：博弈式 testing 仍然能落回经典 conformance 理论。

## 解决了什么问题

这篇论文最重要的推进，是把实时测试从“脚本生成”推进到了“策略生成”。

第一，它放松了 output urgency 与 isolated outputs 这两个非常限制建模表达力的假设。很多此前需要强行重写的系统，现在可以更自然地直接建模。

第二，它让 test case 变成 adaptive winning strategy。对存在不可控输出和时间不确定性的系统，这一点非常关键，因为 tester 终于能在运行时根据 SUT 的分支选择调整动作。

第三，它把 `UPPAAL-TIGA` 这条 timed games 工具线直接接到了 testing 上。也就是说，controller synthesis 不只用于“合控制器”，也能用于“合测试器”。

第四，它清楚说明了 testing 与 game solving 的关系：test purpose 本质上就是一个 reachability / control objective，而 winning strategy 就是最自然的 test artifact。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [hessel04-time-optimal-real-time-test-case-generation-uppaal](../hessel04-time-optimal-real-time-test-case-generation-uppaal/)
   - 已经能做基于 reachability 的 offline testing，但仍受强假设限制。
2. [cassez05-analysis-of-timed-games](../cassez05-analysis-of-timed-games/)
3. [behrmann07-uppaal-tiga](../behrmann07-uppaal-tiga/)
   - 提供 timed game solving 与 strategy synthesis 工具底座。

### 它往后影响了谁

它明显影响：

1. [hessel08-testing-real-time-systems-using-uppaal](../hessel08-testing-real-time-systems-using-uppaal/)
   - 后续 testing 综述对这条 game-based 方法线的整理。
2. `TIOA / ECDAR / mutation-based testing` 分支
3. 更复杂的 adaptive testing / strategy-based testing 工作

### 它更靠近哪条主线

它最靠近：

1. timed games
2. adaptive testing
3. `tioco`-based real-time conformance

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - `TIOGA`、`tioco`、winning strategy 与执行算法都讲得比较清楚，但它更偏 conference paper，很多底层 game-solving 细节仍引用 `UPPAAL-TIGA` 前作。
2. **实现可获取程度**
   - 更适合评为 `🟧 仅可执行/可使用版本可得`。
   - 论文明确依托 `UPPAAL-TIGA`，说明工具链可运行，但 testing workflow 本身没有以完整独立源码包的形式直接给出。
3. **材料价值**
   - 这篇条目非常适合当作“从 timed game synthesis 走向 testing”的关键桥梁来读。

## 对本研究的启发

对当前博士研究，这篇论文的启发很直接。

第一，**测试 / 验证场景可以被表达成策略，而不只是静态脚本**。这对你后续若要让 LLM 生成更鲁棒的验证场景，非常重要。

第二，它说明一类很有价值的迁移路径：把 verification / synthesis 工具已经会做的事情，重新解释成 testing artifact。对“验证失败后生成修复建议”同样可以采用这种迁移思路。

第三，论文把“不可控行为”正面留在模型里，而不是预处理掉。这一点值得借鉴，因为真实控制系统需求往往也带着环境不确定性，过早把不确定性抹平，最终会让自动建模和验证链条失真。
