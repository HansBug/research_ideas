# Conformance Testing in UPPAAL: A diabolic approach

- 问题一句话：`UPPAAL` 验证引擎很强，但 model-based mutation testing 仍主要依赖 `Ecdar` 或 `MoMuT::TA`，缺少一条直接在 `UPPAAL` 里完成 conformance testing 的路径。
- 方法一句话：论文提出 diabolic completion，在规格上加入 kill state，把“mutant 不符合规格”改写成 reachability 问题，并配合 angelic/demonic completion、chain transformation、I/O flip 与 `Yggdrasil` 自动产出测试代码。
- 解决点一句话：它把 `UPPAAL` 的普通 reachability engine 重新解释成 conformance checker 和 test-case generator，并在 car alarm case 上获得显著速度优势。

## 论文定位

这篇论文在 `uppaal_tech/` 中应归为 `🛠️ 工程/工具链`。它不是去发展新的 timed I/O specification theory，而是问一个很务实的问题：如果已经有一个高效、成熟、广泛使用的 `UPPAAL` verifier，为什么 conformance testing 还必须依赖别的专门工具。

它与 [gundersen18-effortless-fault-localisation-ecdar](../gundersen18-effortless-fault-localisation-ecdar/) 形成鲜明对照：

1. `gundersen18` 走的是 `ECDAR` refinement / IDE 一体化路线；
2. 本文则希望把事情直接压回 `UPPAAL` verifier；
3. 其关键不是 refinement game，而是一个新的模型变换：diabolic completion。

因此它更像一篇“如何复用 `UPPAAL` 核心引擎做 testing”的工程型方法论文。

## 立足问题

model-based mutation testing 在 timed automata 上并不新鲜，但此前主流工具大体有两类：

1. `MoMuT::TA`
   - 依赖 SMT / bounded conformance checking；
2. `Ecdar`
   - 依赖 timed I/O automata refinement checking。

这两条线各有优点，但若从 `UPPAAL` 用户角度看，仍存在一个明显落差：

1. 很多用户已经习惯在 `UPPAAL` 里建模；
2. `UPPAAL` 支持的语言特性比部分 testing 工具更丰富；
3. `UPPAAL` verifier 本身高度优化；
4. 但 conformance testing 却没有被直接做进这条主工具线。

因此作者真正盯住的问题是：**能否把 mutant 与 specification 的不符合性，改写成一个 `UPPAAL` verifier 已经非常擅长处理的 reachability 问题。**

一旦能做到这点，就有可能同时得到：

1. 更广的语言支持；
2. 更快的验证性能；
3. 更低的工具切换成本。

## 核心方法

整篇论文的方法就是围绕这条改写展开：先对模型做 input-enabled completion，再在规格上做 diabolic completion，随后把 non-conformance 检查变成 `kill state` 的 reachability，最后借 `Yggdrasil` 生测试代码。

### 1. 继续从 timed automata 和 `MBMT` 出发

论文仍然站在 timed automata / mutation testing 的熟悉框架上：

1. 从规格 `S` 出发；
2. 用 mutation operators 生成 mutants `M`；
3. 若某个 mutant 引入可观察 fault，就应存在一条 trace 能把它和规格区分开；
4. 再由这条 trace 生成 test case。

所以它不是改 testing 的高层框架，而是改 conformance checking 的底层求解方式。

### 2. 先做 angelic / demonic completion，让两侧 input-enabled

为了使后续比较过程稳定，论文先定义两种 completion。

对 mutants 用 **angelic completion**：

1. 在缺少某输入的状态上加 self-loop；
2. 含义是“面对意外输入时忽略它”，而不是直接报错。

对 specification 用 **demonic completion**：

1. 对未规定输入加边到 sink location；
2. 到了 sink 后任何输入输出都可接受。

这样做的逻辑是：

1. 规格只刻画关心的行为，未建模输入不应自动判错；
2. mutant 则不应因为没写某个输入边就人为缩小行为。

这一步和 `ECDAR` testing 线的 completion 思想是一致的，但本文是为下一步 `diabolic completion` 做铺垫。

### 3. 核心创新：在规格上做 diabolic completion

真正的新东西是 **diabolic completion**。它的目标是在规格中加入一个新的 `kill state`，只要 mutant 产生了规格不允许的输出，就把规格送进 `kill`。

直觉上，kill state 表示：“mutant 在这一时刻表现出了 specification 不接受的输出行为”。这种不接受可能有两类：

1. 输出动作本身在该 location 根本不存在；
2. 动作名字对，但 timing guard 不满足，也就是在错误时间发了本应允许的输出。

因此 diabolic completion 的关键不是对输入做处理，而是把**所有不被规格接受的输出空间**显式补成指向 `kill` 的边。

### 4. `resolve` / inverse guard / inverse output 让“补所有错误输出”可机械构造

为了让 diabolic completion 可算法化，论文定义了若干辅助函数：

1. `f_in`
   - 找某位置上没被显式列出的输入；
2. `f_guard`
   - 取 guard 的补；
3. `resolve`
   - 针对同一动作，把所有已有 guard 的否定合成新的 kill-edge guard；
4. `f_out`
   - 找某位置上根本不存在的输出动作。

于是对某个位置 `l`，最终会补两类 kill transitions：

1. 对“动作存在，但当前 guard 不允许”的输出，用 `resolve` 生成 guarded kill edge；
2. 对“动作根本不存在”的输出，直接补一条到 kill 的未约束边。

这一步的本质就是把“规格不接受的输出”显式完成出来。

### 5. 用 reachability 代替完整 conformance checking

一旦 specification 完成了 demonic + diabolic completion，mutant 完成了 angelic completion，就可以把两者并行组成 network。此时只要规格里的 `kill` 可达，就说明 mutant 存在一条行为：

1. 能在 mutant 中发生；
2. 却不属于 specification。

也就是说，non-conformance 被压成了一个普通 reachability 查询：

$$ E \Diamond \texttt{Spec.KillState} $$

这是整篇论文最核心的工程转化。它把原本复杂的 conformance 问题改写成 `UPPAAL` 验证器最擅长的一类查询。

论文还给出定理，说明：

$$ S'(\sigma) = (\texttt{kill}, C) \iff \sigma \in M \land \sigma \notin S $$

这里 `S'` 是 diabolically completed specification。也就是说，kill 可达与“mutant 出现了规格外 trace”是等价的。

### 6. 为了适配 `UPPAAL` 语法限制，再做 chain transformation 与 I/O flip

工程上还有两步很关键。

第一是 **chain transformation**。因为 `UPPAAL` guard 不允许一般形式的析取，而 diabolic completion 产生的 negated guards 可能带 disjunction。作者通过把复合 guard 拆成带 committed locations 的链式结构，保持 reachability 等价，同时绕过语法限制。

第二是 **flip input/output**。为了让 mutant 和 specification 在 `UPPAAL` network 中以同步通道方式通信，mutant 侧还要把输入翻成输出、输出翻成输入，使两者能通过 channel 对接。

这些都说明本文不是只给一个数学想法，而是真的把它做成 `UPPAAL` 可执行模型转换。

### 7. 用 `Yggdrasil` 从 witness trace 生成测试代码

当 `UPPAAL` 给出通向 kill 的最短 witness trace 后，论文继续利用 `UPPAAL` 的 `Yggdrasil` 功能，把 trace 经过的 transition 上附着的 test code 拼起来，自动导出测试文件。

也就是说，这条线最终形成了：

1. mutant generation
2. model transformation
3. reachability witness
4. test-code generation

完整闭环。

## 解决了什么问题

这篇论文最关键的推进，是让 `UPPAAL` 自己就能承担 mutation-based conformance testing 的核心求解任务。

第一，它通过 diabolic completion 把 conformance 问题成功压成 reachability。这样一来，`UPPAAL` 验证引擎多年积累的性能优化都能直接被 testing 复用。

第二，它提供了比部分既有工具更宽的建模兼容性，因为方法建立在 `UPPAAL` 本身的模型语言之上。

第三，它借 `Yggdrasil` 打通了从 witness trace 到测试代码的自动化路径，而不是只给一个理论反例。

第四，在 case study 中它相对 `MoMuT::TA` 和 `Ecdar 2.2` 都表现出速度优势，说明这种“reachability 化”的想法不只是概念漂亮，工程上也确实有收益。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [hessel04-time-optimal-real-time-test-case-generation-uppaal](../hessel04-time-optimal-real-time-test-case-generation-uppaal/)
2. [david08-game-theoretic-approach-real-time-system-testing](../david08-game-theoretic-approach-real-time-system-testing/)
3. `UPPAAL` 既有 verifier / witness / `Yggdrasil` 功能线

但它的方法论与 `ECDAR` testing 线也有强交叉。

### 它往后影响了谁

它对后续最大的价值在于示范了一种路径：

1. 不一定非要为 testing 单独造全新引擎；
2. 也可以通过模型变换，把 testing 还原成主验证器已经能做的问题。

这种思路对后续任何想复用 `UPPAAL` 核心引擎的扩展都很有启发。

### 它更靠近哪条主线

它最靠近：

1. `UPPAAL`-native conformance testing
2. mutation testing
3. witness-to-test-code workflow

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - angelic / demonic / diabolic completion、reachability 定理、chain transformation 和 test generation workflow 都讲得比较实。
2. **实现可获取程度**
   - 更适合评为 `🟥 暂未获取实现源码`。
   - 论文说明实现是基于 `UPPAAL` Java library 写的，但当前没有找到该 diabolic-completion 工具本体的公开源码仓库。
3. **材料价值**
   - 它非常适合拿来理解“如何通过模型变换复用现成 verifier”，这对 `UPPAAL` 技术线非常有代表性。

## 对本研究的启发

对当前博士研究，这篇论文最重要的启发是：**很多看似需要新求解器的问题，其实可以通过合适的模型变换，重写成已有求解器擅长的问题。**

第一，这对你的“验证失败 -> 修复建议”闭环很关键。很多诊断问题未必需要重新设计推理器，可能只要把“错误条件”显式编码进模型，就能复用现有 verifier。

第二，本文把工具语法限制也纳入了方法设计，例如 chain transformation 处理 guard 析取。这说明真正工程化时，形式化思想必须愿意向目标工具的实际语法和执行模型妥协。

第三，`witness trace -> test code` 这条链同样值得借鉴。对未来做自动修复或自动验证脚本生成，这种“从引擎输出直接生成工程制品”的思路很有价值。
