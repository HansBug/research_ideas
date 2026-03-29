# Bounded DBM-based clock state construction for timed automata in Uppaal

- 问题一句话：在线模型检查或仿真恢复时，`Uppaal` 只能通过有限种 `DBM` 操作重建 clock state，直接回放历史轨迹会让恢复序列越跑越长。
- 方法一句话：把目标重建拆成 overapproximation 的 `O-phase` 与 constraining 的 `C-phase`，并证明总序列长度只依赖时钟数而不依赖原始轨迹长度。
- 解决点一句话：给 `Uppaal` 补上一套有严格上界的 clock-state reconstruction 方案，使在线恢复从“回放整段历史”变成“按时钟数有界重建”。

## 论文定位

这篇论文最适合归到 `🧱 核心算法/数据结构`。它讨论的不是通常意义上的 reachability 或 abstraction，而是一个更底层、但对 online verification 很关键的问题：**怎样在 `Uppaal` 支持的 `DBM` 操作集合内，把系统恢复到某个目标 clock state**。

它在文库里的位置比较特殊：

1. 它和传统 `DBM/zone` 工作同属底层状态表示线；
2. 但关注点不是“怎么验证更快”，而是“怎么构造指定的 symbolic clock state”；
3. 它直接服务于 online model checking / simulator restoration 这类增量运行场景。

因此，这篇工作很像 `UPPAAL` 技术线里的一个“底层辅助能力”：不是核心模型检查算法本体，但没有它，在线恢复和增量验证很难做稳。

## 立足问题

作者从一个非常实际的场景出发：若系统已经运行了一段时间，想继续从某个中间时刻做仿真或验证，那么必须先把模型恢复到那个时刻对应的状态。

location 和离散变量通常容易设置，但 clock state 不行。因为在 `Uppaal` 里，时钟状态不是直接赋值，而是由 `DBM` 表示的一组差值约束，且工具支持的操作集很有限：

1. reset 某些 clocks；
2. 施加约束；
3. 时间推进；
4. close / extrapolation 一类 `DBM` 操作。

问题就在于：**你并不能直接写一条“把 `DBM[i,j]` 设成某值”的赋值语句**。如果只是回放原始历史轨迹，当然总能重建目标状态，但这样做有两个问题：

1. 轨迹越长，恢复序列越长；
2. 若模型已发生变化，历史轨迹未必还合法。

于是作者盯住的核心问题是：能否只用 `Uppaal` 允许的 `DBM` 操作，构造一条长度**有严格上界**的恢复序列，而且这个上界只依赖 clocks 数量，而不依赖原始轨迹长度。

## 核心方法

论文的方法主线非常明确：把重建问题拆成 `O-phase` 和 `C-phase` 两段，先造一个包含目标的 overapproximation，再逐步把它压到目标 `DBM`。这种分阶段设计是整篇工作的关键。

### 1. 把 state construction 拆成 O-phase 与 C-phase

作者把整体任务写成：

1. `O-phase`
   - 从初始 `DBM_init` 出发，构造一个 `DBM_approx`，满足它覆盖目标。
2. `C-phase`
   - 从 `DBM_approx` 出发，添加约束直到精确得到 `DBM_target`。

核心关系可以压成：

$$
DBM_{approx} \supseteq DBM_{target}
$$

直觉上，这种分解很自然：

1. 如果你不能直接把目标 `DBM` 写出来，那就先想办法到一个“足够大、把目标包住”的 zone；
2. 再用约束把多余部分裁掉。

这比试图一步到位构造精确 `DBM_target` 要容易得多，也让有界性证明有了抓手。

### 2. O-phase：只保留真正让 zone 变大的操作

对 `O-phase`，作者考虑两种情况：

1. 已知一条历史参考序列 `S_ref`，把它压缩成更短的 overapproximation sequence；
2. 不知道参考序列，只从目标 `DBM` 反推 overapproximation 序列。

对第一种情况，关键观察是：

1. `Constraint` 与 `Close` 这类操作只会把 `DBM` 变小，形成 subzone；
2. 真正把 zone 放大的主要是 `DelayFuture` 与 `Reset`。

因此，作者证明：

1. 可以不断从 `S_ref` 中删除所有 `Constraint/Close`，结果一定仍然 overapproximate 目标；
2. 然后再删除冗余或已被覆盖的 `Reset/DF`，最终把 `O-phase` 的序列压到只和 clocks 数量相关。

这一步的思路很漂亮，因为它不是“重新合成一条新序列”，而是先用单调性证明把历史序列里“收缩区间”的动作统统删掉，只保留那些真正制造上界空间的动作。

### 3. C-phase：从 overapproximation 出发，系统地补约束

`C-phase` 的任务是从 `DBM_approx` 精确收缩到 `DBM_target`。作者给出三种策略：

1. `FCS`
   - full constraint system
2. `MCS`
   - minimal constraint system
3. `RCS`
   - reduced constraint sequence

这些方法的共同思路是：不要盲目把所有约束一股脑加回去，而是找出**足以唯一确定目标 `DBM` 的最小或更短的约束集**。

也就是说，`C-phase` 不是简单执行“把目标 DBM 的每个条目都重新施加一次约束”，而是分析哪些差值约束是冗余的、哪些其实可由其他约束推得，从而压缩 constraining sequence。

### 4. 得到总长度上界：只和 clocks 数量有关

整篇论文最核心的结果，是给出总体构造序列长度的显式上界：

$$
|S| \le 1 + 2|T| + |T|(|T| + 1)
$$

这里 `|T|` 是系统 clocks 数量。注意这个结论的力度非常强：它说无论原始执行轨迹有多长，重建序列长度都不再随时间增长，只由 clocks 数量决定。

这正是作者反复强调“bounded”而不是“通常更短”的原因。本文要解决的不是平均表现，而是在线场景里必须满足的硬界限问题。

### 5. 把抽象 `DBM` 操作序列重新编码成可执行 `Uppaal` 模型片段

仅在 `DBM` 层构造操作还不够，作者还进一步说明如何把这些操作落回具体 `Uppaal` 模型：

1. 通过插入人工 location / edge 承载构造序列；
2. 让最后一条边回到原模型应处于活动状态的位置；
3. 对离散变量直接赋值；
4. 对 clock state 则通过边上的 resets、guards、delay 等组合间接构造。

这一步很关键，因为它说明本文不是抽象算法，而是能真正修改 `Uppaal` 模型，使其在初始化后先走一小段“恢复通道”，再回到原系统运行区。

### 6. 给出完整实现，并比较 trivial / Rinast / OC approach

论文不仅证明理论上界，还把 trivial replay、Rinast graph-based shortcut approach 和自己的 `OC` approach 放在一起比较。

作者实现了：

1. `Uppyyl` simulator
2. state constructor
3. experiment suite

并用多个 `Uppaal` demo models 与随机序列做实验，验证：

1. trivial 序列会线性增长；
2. graph-based shortcut 在有些模型上仍无法保证有界；
3. `OC` approach 始终保持与 clocks 数量相关的固定上界。

## 解决了什么问题

这篇论文解决的是 `UPPAAL` 在 online / incremental 场景下的一个关键缺口：如何在不支持直接 clock-state assignment 的前提下，仍然有界地恢复任意目标 `DBM` 状态。

第一，它把恢复问题从“回放整段历史”转成“构造一个只依赖 clocks 数的 bounded sequence”。

第二，它给出了清晰的两阶段结构，使得 overapproximation 与 exact reconstruction 被分开处理，各自有独立的正确性与界限论证。

第三，它不仅停在理论，还实现了工具和模型改写方法，因此可以直接嵌入 `Uppaal` 相关在线验证工作流。

第四，它还明确说明了相较于 trivial 与 graph-based shortcut approaches 的优势边界：前者必然增长，后者只有在某些反复 reset 所有 clocks 的场景下才可能变短，而 `OC` 是一般性的 bounded 方案。

## 与 UPPAAL 技术线的关系

这篇论文与 `UPPAAL` 技术线的关系集中在底层 `DBM` 操作能力：

1. 它建立在 `DBM` 作为 symbolic clock-state 表示的传统之上；
2. 但关注的是“如何构造状态”，而非“如何搜索状态”；
3. 它与 online model checking、simulator state restoration、增量验证接口紧密相关。

可把它看成 `DBM / symbolic state` 这条线在 2020s 的一个实用扩展：不是再压缩状态空间，而是让状态本身能被可控地重建。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟢 复现级`。因为：

1. 问题建模完整；
2. `O-phase/C-phase` 结构明确；
3. 上界定理和实现细节都给出；
4. 还提供了代码与实验仓库。

从实现可获取程度看，适合标 `🟢 论文对应实现源码直达`。论文明确写到：

1. 项目实现开源；
2. `Uppyyl simulator`
3. `uppyyl-state-constructor`
4. 实验仓库

都给了 GitHub 入口。因此这是少数“论文方法源码确实可直接追到”的条目。

## 对本研究的启发

对当前博士研究，这篇论文最值得迁移的是：**很多验证工作流的难点不在判定本身，而在怎样让模型快速进入你真正关心的局部状态**。

具体启发有三点：

1. 若将来你的闭环方法需要反复从“已知局部上下文”继续验证，那么状态恢复本身值得单列成能力，而不是默认总从初态重跑。
2. 把复杂问题分成“先包住目标，再精确收缩”的两阶段设计，非常适合迁移到模型修复或场景生成里。
3. 明确的长度上界比平均更短更重要，尤其当系统要进入在线、频繁、自动化执行时。
