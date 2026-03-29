# Model-Checking for Real-Time Systems

- 问题一句话：real-time reachability 穷举验证代价过高。
- 方法一句话：用符号约束求解与 compositional quotient 结合 region 技术。
- 解决点一句话：立起早期 `UPPAAL` 验证核心。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `🧱 核心算法/数据结构` 条目，也是当前文库里第一篇明确把“**这些技术就是 `Uppaal` 的基础**”写在摘要里的条目。它位于 `1995` 年，正好卡在 [ad90-timed-automata](../ad90-timed-automata/) 与 [llpy97-compact-data-structure](../llpy97-compact-data-structure/) 之间：前者给出 timed automata 语义与 region 可判定性骨架，后者开始解决 `DBM` 压缩与状态空间削减问题，而这篇论文正是把它们拉成一个真正的 verification workflow。

它的历史位置非常明确：

1. 从理论上，它继承了 timed automata / region technique。
2. 从方法上，它开始系统攻击两类爆炸：
   - **control-node explosion**
   - **region-space explosion**
3. 从工具上，它第一次把这套方法明确指向一个新工具：`Uppaal`。

所以，这篇论文不是一般意义上的“早期工具介绍”，而是 `UPPAAL` 最早那批真正把“实时模型检查如何才能跑起来”说清楚的奠基条目。

## 立足问题

这篇论文面对的问题非常具体：即使 timed automata 的 model checking 已经被证明可判定，真正落到并行系统时，实际代价还是会被两种爆炸拖垮。

作者在摘要和引言里把问题直接点明了：

1. **control-node explosion**
   - 多个 timed automata 并行组合后，离散控制节点的乘积空间会迅速膨胀。
2. **region-space explosion**
   - region technique 是 decidability 的基础，但 region 划分是按常数上界静态生成的，极其细、极其大。

如果只停在 region graph 层面，问题虽然“理论上可算”，但并不意味着工程上可用。作者真正盯住的是：**怎样在不丢掉 timed semantics 的前提下，把 region-based model checking 变成真正可执行、可扩展、可对比其他工具的验证器。**

这里面其实有三个更深的技术瓶颈：

1. **region 是 property-independent 的**
   - 它只依赖 automaton 中出现的常数，而不考虑当前要验证的公式。
   - 这导致分区往往远比真正需要的细。
2. **并行组合太早做全局乘积会直接炸**
   - 如果先把所有 automata 乘起来，再去 model check，control nodes 先爆掉。
3. **逻辑表达力和求解代价之间有张力**
   - 如果坚持用很强的 timed logic，符号分区和实现复杂度都会急剧上升。

因此，这篇论文真正的问题意识不是“发明一个更强的逻辑”，而是：**在够用的表达力下，把 timed verification 的语义对象、逻辑对象和工具对象一起改造到足够高效。**

## 核心方法

这篇论文的方法主线很清晰，可以拆成四块：**统一 timed automata / network 语义、引入适合效率的逻辑片段、用 clock constraints 做 symbolic model checking、再用 quotient 做 compositional model checking。**

### 1. 用 timed transition systems 和 timed automata / networks 固定语义底盘

论文先把 timed automata 的语义落成 timed transition systems。系统状态是：

$$
(l, u),
$$

其中 $l$ 是控制节点，$u$ 是当前 clock assignment。网络语义则通过同步函数定义并行组合，不直接把所有成分一上来就化成一个静态整体。

这一层的重要性在于：作者没有直接跳到算法，而是先把 **单 automaton、network、parallel composition、clock constraints** 全部放到同一语义框架里。这样后面的 symbolic search 和 quotient 才有统一目标对象。

论文中的 timed automaton 已经具备后来 `UPPAAL` 的基本骨架：

1. clocks；
2. invariants；
3. guards；
4. resets；
5. network composition。

换句话说，`UPPAAL` 不是先有工具再慢慢补语义，而是这篇论文里语义、逻辑和算法三层已经同时成形。

### 2. 不直接追求最强逻辑，而是设计 `L_\nu` 与更实用的 `L_s`

作者没有只用已有 TCTL / timed $\mu$-calculus，而是先给出带 clocks 和 recursion 的 `L_\nu`，再从中抽出一个更适合工具实现的片段 `L_s`，专门服务于 safety 和 bounded liveness。

这一步的策略非常值得注意：

1. **不是先追求最强表达力。**
2. **而是先确定实践中常用性质能否表达。**
3. **再以此换取更高效的 symbolic procedure。**

这和很多理论论文的方向正相反。作者清楚知道：若逻辑太强，symbolic partition 还是会过细、实现也更复杂；而对工业验证来说，很多关键问题其实就是：

1. invariant；
2. deadlock-freedom；
3. bounded response；
4. bounded liveness。

所以，这篇论文的方法性贡献不仅是“选了某个逻辑”，而是**把逻辑设计本身当作可扩展性优化的一部分**。

### 3. 用 clock constraints 取代过细的静态 regions，做 symbolic model checking

这是全文最关键的一步。region technique 的问题在于它是 property-independent 的，于是分区太细。作者提出的改造方式是：不再坚持显式 region graph，而是直接用 clock constraints 来符号化表示一批赋值。

论文中 symbolic state 写成：

$$
[l, D],
$$

意思是：对所有满足约束系统 $D$ 的 clock assignments，都在同一个控制位置 $l$ 上一起处理。

作者为此定义了一组核心运算：

1. $D^\uparrow$
   - 延时闭包，对应“让时间流逝后仍可能到达的赋值集合”。
2. $D^\downarrow$
   - 文中写作 `D#`，对应某种反向时间可达。
3. $r(D)$
   - reset 某组 clocks。
4. $D \land D'$
   - 交。

这些对象不是纯口头比喻，而是直接作为 model-checking rewrite system 的输入输出。作者要检查的也不再是单个扩展状态，而是：

$$
[l, D] \models \varphi,
$$

即：凡是满足 $D$ 的赋值，在位置 $l$ 上都满足公式 $\varphi$。

这一步有两个本质变化：

1. **把 region 的固定划分，换成与性质相关的 constraint partition。**
2. **把 checking 问题转成 constraint solving / rewrite tree。**

作者还给出符号化 satisfaction 规则。例如对于时间算子和动作算子，会把公式递归地改写成新的 symbolic problems；循环则可利用最大不动点语义终止。由此，模型检查不再需要先完整展开 region graph，而是按性质需求、按当前约束状态逐步推进。

这一改造正是后来 `UPPAAL`“用 symbolic zones 而不是显式 regions 工作”的核心精神前身。虽然这里的术语还是 clock constraints，不是后来的成熟 zone/DBM 工程化表达，但主思路已经完全到位。

### 4. 用 quotient construction 攻击 control-node explosion

只做 symbolic clock constraints 还不够，因为 control-node explosion 依然存在。于是作者再引入 compositional quotient construction，把系统成分逐个从并行系统里“搬进公式”。

其目标关系写得非常直接：

$$
A \parallel_f B \models \varphi \iff A \models \varphi /_f B.
$$

如果网络是 $A_1 \parallel \cdots \parallel A_n$，那么就可以不断 quotient：

$$
A_1 \parallel \cdots \parallel A_n \models \varphi \iff \mathbf{1} \models \varphi / A_n / A_{n-1} / \cdots / A_1.
$$

这背后的方法重点不是简单“做组合验证”，而是：

1. 通过 quotient 避免一次性构造完整 product control space。
2. 每 quotient 一步，就把一个组件行为吸收到公式中。
3. quotient 之后立即做 minimization，而不是任由公式无限膨胀。

作者还专门设计了三类化简机制：

1. **constraint propagation**
2. **region propagation**
3. **equivalence reduction**

这说明 quotient 不是一个抽象存在定理，而是一个必须和化简联动的工程化过程。不然节点空间没爆，公式空间会先爆。

### 5. 用实现与实验把“方法真的可用”落地

论文最后不是只给复杂度，而是直接实现成 `Uppaal` 并和 HyTech、Kronos、Epsilon 做对比。实验选择 Fischer protocol 这种可扩规模的 benchmark，目的非常明确：证明这套 symbolic + compositional 组合拳不是理论演示，而是确实比其他实时验证工具更快、能撑更大规模。

这一步很关键，因为它把整篇论文的方法闭环补齐了：

1. 语义对象：timed automata / networks。
2. 逻辑对象：`L_\nu` / `L_s`。
3. 算法对象：constraint-solving symbolic model checking。
4. 组合对象：quotient + minimization。
5. 工具对象：`Uppaal` 实现和 benchmark。

## 解决了什么问题

这篇论文真正解决的，是早期实时模型检查从“可判定理论”走向“可用工具”的第一道大门槛。

### 1. 它把 region-based decidability 推进成 property-sensitive symbolic verification

此前 timed model checking 虽然可判定，但 region 太细。作者的 symbolic technique 让分区开始依赖待验证性质，而不是一律按 automaton 常数静态切分。这直接缓解了 region-space explosion。

### 2. 它第一次系统处理了 control-node explosion

通过 quotient，作者把“并行组合后节点空间过大”这件事从建模层就开始拆解，而不是等全局 product 构完再亡羊补牢。这让实时组合验证第一次真正走向可扩展。

### 3. 它奠定了 `UPPAAL` 的方法学骨架

如果把 `UPPAAL` 后来的风格压成一句话，大概就是：

1. timed automata network；
2. symbolic clock constraints；
3. 面向常用安全/有界活性性质；
4. on-the-fly 风格；
5. 强调实际性能。

而这些点，在这篇论文里已经几乎全部出现。

### 4. 它也明确保留了边界

作者没有声称所有 timed logics 都能同样高效处理。相反，他们清楚承认：

1. `L_s` 的表达力弱于完整 timed $\mu$-calculus。
2. 当前工具的实际瓶颈更偏空间复杂度。
3. 未来还需要更省空间的 clock-constraint 表示、更好的诊断信息和更强的 minimization heuristics。

这说明这篇论文不是终点，而是一个非常清晰的“第一代 `UPPAAL` 核心路线图”。

## 与 UPPAAL 技术线的关系

这篇论文和 `UPPAAL` 的关系不是“相关工作”级别，而是**起点级别**。

### 它接在谁之后

它直接接在：

1. [ad90-timed-automata](../ad90-timed-automata/)
   - 提供 timed automata 与 region decidability 的理论地基。
2. [dill89-timing-assumptions](../dill89-timing-assumptions/)
   - 提供 continuous-time constraints 与 difference-style region 表示的前史味道。

### 它往后影响了谁

在当前文库里，它往后最直接影响的是：

1. [llpy97-compact-data-structure](../llpy97-compact-data-structure/)
   - 继续解决 clock constraints / DBM 的内存问题。
2. [lpy97-uppaal-nutshell](../lpy97-uppaal-nutshell/)
   - 把这篇论文里的方法骨架转成更系统的工具说明。
3. [behrmann02-new-uppaal-architecture](../behrmann02-new-uppaal-architecture/)
   - 进一步把工具骨架模块化。
4. 后续 `Tiga / SMC / Stratego`
   - 虽然目标不同，但都继承了“先有可执行 symbolic engine，再扩分析能力”的路线。

### 它更靠近哪条主线

它最靠近的是：

1. `symbolic verification`
2. `constraint solving`
3. `compositional quotient`
4. 早期 `UPPAAL` 工具内核

相比之下，它离后来的 `SMC / ECDAR / Coshy` 还很远。

## 实现与材料

1. **内容详细程度**
   - 当前总账给它记为 `🟩 较完整`，我认为合理。
   - 原因是论文不仅有问题陈述，还有明确的 symbolic operations、quotient construction、化简规则和 benchmark；已经不是一般概览。
2. **实现可获取程度**
   - 目前仍应记为 `🟧 仅可执行/可使用版本可得`。
   - 论文明确指向 `Uppaal`，但当前没有拿到与 `1995` 这篇论文直接对应的公开核心源码快照。
3. **材料质量**
   - `paper_content.txt` 足够支持问题、方法和技术线定位的重建。
   - 但如果后续要继续抠公式规则和具体 rewrite semantics，仍建议回到 PDF 表格与图示。

## 对本研究的启发

这篇论文对当前博士研究有三点非常直接的启发。

### 1. 性质语言必须为验证效率服务

不是性质语言越强越好。若想让 LLM 生成的状态机真的进工具链，往往需要先确定一类足够实用、且能高效验证的性质子语言。

### 2. 符号表示必须和待验证问题绑定

作者之所以能比纯 region 法更有效，是因为 partition 不再完全 property-independent。这对本仓库很重要：如果未来要做验证剖面，剖面本身就应影响状态抽象和搜索方式，而不是验证时一视同仁。

### 3. 组合问题不要一开始就做全局乘积

这对复杂状态机系统尤其关键。若未来要把多个组件模型、场景模型和修复候选一起验证，必须尽早考虑 compositional decomposition，而不是默认先建一个大而全的统一模型。
