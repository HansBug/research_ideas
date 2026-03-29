# Online On-the-Fly Testing of Real-time Systems

- 问题一句话：离线生成完整测试集对实时系统往往太贵，而且还难以处理 dense-time、非确定性和长时间运行的黑盒实现。
- 方法一句话：论文把 `UPPAAL` 的 symbolic reachability 引擎改造成在线测试引擎，基于 timed trace inclusion 维护当前 reachable symbolic state-set，并一边生成下一步测试动作一边执行。
- 解决点一句话：它为 `UPPAAL` 打开了实时在线测试分支，证明无需预先展开整张状态图，也能对带时间约束的系统做可执行、可判 verdict 的 conformance testing。

## 论文定位

这篇论文在 `uppaal_tech/` 中应归入 `🛠️ 工程/工具链` 与 `🧪 扩展方向` 的交界位置，更准确地说，它是 `UPPAAL` **testing 分支的起点级条目**。

它与普通 `UPPAAL` verification 论文的最大差别在于：目标不再是证明一个模型满足某性质，而是拿一个形式化规格去**在线测试真实实现**。因此它引入的是一整套新的问题设置：

1. 有一个黑盒 `IUT`；
2. 观察的是 input / output 与时间延迟组成的 timed trace；
3. 工具不能预先知道实现处于哪个具体状态，只能维护当前可能状态集；
4. verdict 不是简单 true / false，而是 `pass / fail / inconclusive`。

如果把技术线往后看，这篇显然直接通向：

1. [larsen04-online-testing-real-time-systems-using-uppaal](../larsen04-online-testing-real-time-systems-using-uppaal/)
2. [larsen04-online-testing-status-future-work](../larsen04-online-testing-status-future-work/)
3. [mikucionis10-online-testing-real-time-systems](../mikucionis10-online-testing-real-time-systems/)

因此，它的历史角色非常清楚：这是测试线真正起步的那篇。

## 立足问题

这篇论文面对的问题是：**实时系统测试太依赖人工、太 ad-hoc，而传统 offline test generation 在实时场景下又常常过重。**

作者在引言里把问题说得很明白：

1. 嵌入式与实时系统测试占项目资源很大比例；
2. 但很多测试流程仍靠经验和手工；
3. 时序正确性不仅看“发生了什么事件”，还看“什么时候发生”；
4. 若采用离线测试生成，完整测试场景与 verdict 必须事先算好，这很容易遇到 state-space explosion；
5. timed automata 规格还常常含非确定性，进一步增加离线生成难度。

因此作者押注在线测试：边执行、边生成下一步测试动作，而不是先把整棵测试树离线算完。

这背后的关键判断有三条：

1. **长时间测试需要 online**
   - 一个测试 run 可能持续很久，没必要也不现实把全程测试脚本预计算出来。
2. **dense-time 需要 symbolic**
   - 实时时钟取值是连续的，不能显式枚举。
3. **黑盒实现需要 state estimation**
   - 工具看不到实现内部状态，只能根据已观察 trace 维护一个可能状态集合。

所以这篇论文真正立足的问题，不只是“如何从 timed automata 生成测试”，而是：

> 如何把 `UPPAAL` 的 symbolic model-checking 技术改造成一个在线、实时、基于状态集估计的 testing engine。

## 核心方法

这篇论文的方法主线非常清楚，可以拆成五步。

### 1. 先把测试问题组织成 `IUT + Environment + Adapter + Testing Engine`

论文先给出完整 testing framework。测试场景不是“规格对实现”的抽象二元关系，而是四个部件共同作用：

1. `IUT`
   - 被测实现。
2. `Environment`
   - 外部环境模型，决定哪些输入何时可能发生。
3. `Adapter`
   - 在抽象动作与真实实现接口之间做转换。
4. `Testing Engine`
   - 负责选择测试动作、更新当前状态估计并给出 verdict。

这一步很重要，因为它告诉我们：测试不是把 model checker 直接拿去看代码输出，而是需要把环境假设、动作映射和执行控制都建模出来。

### 2. 用 timed trace inclusion 定义 conformance

接着论文定义 conformance relation。它没有直接照搬非实时领域常见的 `ioco`，而是采用 timed trace inclusion：

$$
\text{Traces}(IUT) \subseteq \text{Traces}(Spec)
$$

这里的关键含义是：

1. 实现不能产生规范未允许的 observable behavior；
2. 不仅动作序列要合法，动作发生的时间点也要合法；
3. “安静一段时间”只有在规范允许对应时间推移且无输出时才算合法。

作者特别强调，这提供了一种 real-time 下的 `time-bounded quiescence` 观念，而不是非实时 `ioco` 式的永恒静默。

基于这个 conformance relation，论文定义三种 verdict：

1. `fail`
   - 观察到规范不允许的输出或不允许的 delay。
2. `inconclusive`
   - 观察到的行为不是实现模型明确禁止，但偏离了当前环境模型/测试目标，导致本次测试目标失效。
3. `pass`
   - 观察到的输出和时间行为都被规范允许。

这一步的价值在于：它把“实时测试的正确性判定”压成了一条很明确的 trace inclusion 关系。

### 3. 在线算法维护当前 reachable symbolic state-set

论文的核心算法是维护当前状态估计集合 $Z$。它表示：

> 在目前为止已经观察到的 timed trace 下，测试规格可能处于哪些 symbolic states。

算法流程很直接：

1. 初始时，$Z$ 只含初始 symbolic state；
2. 测试引擎反复在两种动作间选择：
   - 给 `IUT` 发送一个输入；
   - 等待一段时间看输出是否出现；
3. 每次观察到动作或 delay 后，都更新 $Z$；
4. 若更新后得到空集，说明观察 trace 不在规范中，对应 `fail`。

作者给出的主算法中，当前版本的 `ChooseAction` 与 `ChooseDelay` 还是随机选择，这很重要：论文的重点不是某个特别强的 test purpose heuristic，而是把在线状态估计与 verdict 机制先搭起来。

### 4. 用 `After` 与闭包运算实现状态集更新

真正让在线测试可行的，是 `UPPAAL` 风格的 symbolic state-set computation。

论文把核心更新运算写成：

$$
After(Z, a)
$$

和

$$
After(Z, \delta)
$$

它们分别表示：

1. 在当前状态集 $Z$ 下执行一个可观察动作 $a$ 后能到达的状态集；
2. 在等待 $\delta$ 时间后能到达的状态集。

为了支持 timed semantics，作者引入了：

1. `Closure_tau(Z)`
   - 零时间内所有 internal transitions 的闭包。
2. `Closure_tau^delta(Z, d)`
   - 在 `0..d` 范围内允许时间流逝并夹杂内部动作后的闭包。

实现上还引入一个辅助时钟 `t`：

1. 每当发生 observable action，就把 `t` 置零；
2. 等待操作时用 `t <= d` 限制 delay closure；
3. 达到目标 delay 后再通过 `t == d` 截取对应 symbolic states。

这一步非常漂亮，因为它把“在线测试时只关心从现在开始的相对时间”直接翻译成了一个额外时钟变量。

### 5. 用 `T-UPPAAL` 原型与 train controller 做实验

论文最后把算法实现成 `T-UPPAAL` prototype，并用 train controller 规格与一组 mutants 做实验。

实验分两部分：

1. **错误检测能力**
   - 测试若干 mutant 是否会被发现。
2. **状态集计算性能**
   - 测量 `After(delay)` 与 `After(action)` 的状态集大小和计算时间。

从文中结果看，核心观察包括：

1. 大部分测试中 symbolic state-set 很小，很多时候只有 `2-3` 个 symbolic states；
2. `After(delay)` 是更重的操作，但平均仍在毫秒量级；
3. 工具能较快发现多种典型错误；
4. 正确实现上的少数异常结果，作者坦率地归因为 prototype bug 或同步问题，而不是掩盖掉。

这说明方法在原型层已经可运行，而且 symbolic online tracking 并没有因为 dense-time 而立刻失控。

## 解决了什么问题

这篇论文真正解决了 testing 分支里的几个基础问题。

### 1. 它把 `UPPAAL` 从 verifier 扩成了 online tester

此前 `UPPAAL` 的主身份是 model checker；这篇工作证明，其 symbolic engine 也可以改造为一个一边执行、一边估计状态集、一边判断 verdict 的测试引擎。

### 2. 它把 real-time conformance testing 的核心对象明确化了

通过 timed trace inclusion 与 `pass/fail/inconclusive`，论文给出了一个对实时系统足够自然的判定基础。

### 3. 它证明了 online symbolic testing 在实践上并不离谱

实验结果说明：

1. 不需要把整张状态图离线算出来；
2. 当前状态集通常不大；
3. `After` 运算的代价可接受；
4. 非 trivial 的 train controller 场景也能跑。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线里是一个明显的分叉点：它不再主要沿着“更快的验证引擎”这条线走，而是把同一 symbolic 核心迁移到 testing。

### 它接在谁之后

它建立在：

1. 早期 `UPPAAL` symbolic reachability 内核；
2. [behrmann02-new-uppaal-architecture](../behrmann02-new-uppaal-architecture/)
   - 让引擎更模块化、可扩展；
3. [david03-unification-sharing-timed-automata-verification](../david03-unification-sharing-timed-automata-verification/)
   - 继续提升核心状态空间管理性能。

### 它往后影响了谁

它明显往后通向：

1. [larsen04-online-testing-real-time-systems-using-uppaal](../larsen04-online-testing-real-time-systems-using-uppaal/)
2. [larsen04-online-testing-status-future-work](../larsen04-online-testing-status-future-work/)
3. [hessel08-testing-real-time-systems-using-uppaal](../hessel08-testing-real-time-systems-using-uppaal/)
4. [mikucionis10-online-testing-real-time-systems](../mikucionis10-online-testing-real-time-systems/)

### 它更靠近哪条主线

它最靠近的是：

1. online testing；
2. timed I/O semantics；
3. state-set estimation；
4. `UPPAAL` 核心 symbolic engine 的测试化改造。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟨 中等偏上`。
   - 框架、conformance、主算法、`After` 更新和实验都讲得比较清楚，但 prototype 仍较早，很多策略层与工程层细节没有完全展开。
2. **实现可获取程度**
   - 适合评为 `🟥 源码未见明确公开`。
   - 论文明确实现了 `T-UPPAAL` prototype，但当前材料中没有看到清晰、可直接取得的源码入口；这与公开可下载可执行工具不同，不能算“实现可获取”。
3. **材料质量**
   - `paper_content.txt` 足以支撑重建 testing framework 和算法主线。
   - 若后续要继续把 testing 线扩得更完整，应继续联读 `2004` 和 `2010` 的后续条目。

## 对本研究的启发

这篇论文对当前博士研究尤其有启发，因为它展示了一个非常接近“生成-验证-执行-反馈闭环”的原型。

可以直接借鉴的点包括：

1. 若将来要把 `LLM` 生成的形式模型拿去接触真实系统，不应只做离线验证，还应考虑在线状态估计与运行时测试。
2. `pass/fail/inconclusive` 这种多值 verdict 很适合不完全可观测、带环境假设的闭环场景。
3. 在黑盒场景里，维护“可能状态集”比追求唯一内部状态更现实。
4. `UPPAAL` 的 symbolic 技术不只适用于证明，也适用于和真实执行过程持续交互，这一点对后续研究路线很重要。
