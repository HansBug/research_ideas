# WUPPAAL: Computation of Worst-Case Execution-Time for Binary Programs with UPPAAL

- 问题一句话：二进制程序的 `WCET` 既受输入路径影响，又受 pipeline/cache 等复杂硬件时序影响，传统分析链难以既精确又通用。
- 方法一句话：论文把程序运行抽象成可生成的带注释执行树，再用扩展版 `UPPAAL` 对“程序树 + 硬件 timed automata”做最长时间路径搜索。
- 解决点一句话：它把早先偏 ARM/专用建模的 `UPPAAL` 式 `WCET` 分析推广成面向任意二进制语言和硬件的模块化框架，并以 `WUPPAAL` 工具链落地。

## 论文定位

这篇论文属于 `🛠️ 工程/工具链` 条目，但它和普通工具介绍文不同，它实际上位于 `UPPAAL` 技术线和 `WCET / hardware timing analysis` 之间的一条很硬的交叉支线。它延续了作者更早用 timed automata 计算执行时间的工作，但这次重点不再是手工把某种 CPU/ISA 写死进模型，而是把整条分析链**抽象成可替换的模块接口**。

在 `uppaal_tech/` 的时间线上，它更像：

1. 承接早期 `UPPAAL` 作为 timed-game / scheduling / cost analysis 引擎的工程传统；
2. 把 `UPPAAL` 再拉向静态分析、binary semantics 与 hardware timing 交叉的方向；
3. 同时为后续把 `UPPAAL` 当作通用 timed-analysis back-end 的工程思路提供了一个很强的例子。

它的特殊性在于：虽然结果是 `WCET`，但论文主体其实主要在讨论**如何把二进制程序与硬件时序抽象成适合 `UPPAAL` 处理的形式**，而不是把 `UPPAAL` 只当黑箱求解器。

## 立足问题

论文面对的核心问题是：`WCET` 不是单纯的软件路径问题，也不是单纯的硬件建模问题，而是二者耦合出的时序极值问题。

从软件侧看，程序的最坏执行时间依赖输入。若只做仿真，只能得到 lower bound，因为你永远不敢保证已经试到最坏输入。  
从硬件侧看，现代处理器包含 pipeline、cache、memory hierarchy，这些部件本身就是带并发和时序约束的系统。于是“执行多少周期”不再是给每条指令贴个常数就能完事的。

作者把这个问题正式写成：

$$ \mathrm{WCET}(P, H) = \sup_{d \in D} Xtime(P, d, H). $$

这里：

1. $P$ 是二进制程序；
2. $H$ 是硬件；
3. $d$ 是输入数据；
4. $Xtime(P,d,H)$ 是该输入下程序在该硬件上的执行时间。

这一定义马上暴露出两个技术瓶颈：

1. 输入域 $D$ 很大，无法靠枚举数据仿真得到安全上界；
2. 硬件是并行、带缓存和争用的 timed concurrent system，很难直接压成简单成本模型。

作者对已有 `METAMOC` 路线的批评也很具体：尽管 timed automata + `UPPAAL` 很适合表达 pipeline/cache 同步，但原方案仍有若干限制：

1. CFG 生成和 value analysis 容易卡死或不收敛；
2. 某些寄存器间接跳转程序难处理；
3. 需要手工 loop bound 注释；
4. 程序语义与 cache 状态被整个塞进 `UPPAAL` 的离散状态里，导致状态空间过大。

所以这篇论文真正要解决的是：**保留 “`UPPAAL` 处理 timed hardware behavior” 的优点，同时把程序语义和缓存细节尽量从 `UPPAAL` 模型里外包出去。**

## 核心方法

这篇论文的方法主线非常清楚：把“程序 + 硬件”的 `WCET` 问题拆成**注释程序运行生成器**与**硬件 timed automata 求值器**两个模块，再通过扩展版 `UPPAAL` 把它们拼起来。

### 1. 先把二进制程序执行抽象成注释运行语言

作者首先把程序可能的执行抽象成运行集合 $L_H(P)$，再进一步构造带时序相关注释的运行语言 $L_H^a(P)$。  
这里的核心想法不是在 `UPPAAL` 里完整解释每条二进制指令，而是只保留**求执行时间真正需要的信息**，比如：

1. 某条指令在流水线执行级要花多少 cycles；
2. 当前访存是 instruction-cache hit 还是 miss；
3. 哪些寄存器依赖会引发 pipeline stall；
4. 程序路径与循环展开后还剩哪些可行运行。

于是最终硬件分析不再吃“原始程序”，而是吃一个已经注释过的 trace 语言：

$$ \sigma \in L_H^a(P). $$

这一步非常关键，因为它把“语义解释”和“时序评估”分开了。后者只需要知道某条运行上发生了哪些 timed-relevant 事件，不需要再自己模拟整个 ISA 语义。

### 2. 用 timed automaton transducer 表示硬件时间评估

在这套分工下，硬件抽象成一个 timed automaton transducer `Aut(H)`，它把一条注释运行映射成执行时间：

$$ \mathrm{WCET}(P, H) = \max_{\sigma \in L_H^a(P)} Aut(H)(\sigma). $$

这里的方法重点在于，`Aut(H)` 只需要模拟：

1. 流水线各级如何并行推进；
2. 哪些地方会因寄存器/流水线约束 stall；
3. cache/main memory 访问何时是 hit、何时是 miss；
4. 最终总时间如何累计。

作者明确指出，这里的硬件 timed model 不必包含完整 concrete hardware state。因为求执行时间时，并不需要真的在 `UPPAAL` 内部保存所有寄存器值、cache line 内容和内存状态；只要外部已经告诉它“这一运行上的 cache 结果与执行阶段耗时是什么”，硬件 automata 就能只做 timed coordination。

这就是这篇论文相对早期方案的最本质变化：**`UPPAAL` 从“既解释程序又模拟硬件”的重模型，变成“主要负责 timed hardware orchestration”的轻模型。**

### 3. 把程序可能运行组织成可查询的执行树

论文第三部分提出 `WUPPAAL` 的 generic framework。作者假设已经能得到一个有限的程序计算树 `Tree_H^a(P)`，并为它定义一个 tree-API，最关键的操作包括：

1. `getinit()`：取根节点；
2. `getnext(n)`：给出节点 `n` 的后继；
3. `hitins(n)`：该节点对应取指是否 cache hit；
4. `getexec(n)`：该节点所对应指令在执行级的耗时。

这意味着程序侧的“所有可能运行”不再作为一个写死的 `UPPAAL` automaton 编码，而是作为外部库可查询的数据结构提供给 `UPPAAL`。论文甚至把这套接口明确实现进 `libgdb2uppaal`。

这一步是工程设计的关键。因为：

1. 对程序路径空间的枚举，留给外部工具和运行时库；
2. 对硬件 timing composition 的分析，留给 `UPPAAL`；
3. 两者通过简单 tree-API 交互。

### 4. 用 `qemu + gdb + libgdb2uppaal` 把程序语义外包掉

论文的工具链是它最有工程含量的部分：

1. `pre-analysis`
   - 从二进制构造切片程序、CFG 和必要注释；
2. `qemu`
   - 模拟硬件执行，计算单步指令效果；
3. `gdb`
   - 检查 `qemu` 中程序状态；
4. `libgdb2uppaal`
   - 实现前面说的 tree-API，把程序状态映射为 `UPPAAL` 可调用的整数标识；
5. `HW.xml`
   - 用 timed automata 写出的硬件模型；
6. `Uppaal`
   - 在这些接口基础上探索全部运行并求最坏执行时间。

这意味着作者真正做成的不是一篇“再建一个 NTA 模型”，而是一条外部语义工具和 `UPPAAL` 引擎协同工作的 analysis pipeline。尤其 `qemu` 的作用很关键：它避免了把完整二进制指令语义手写翻译进 `UPPAAL` 的 C-like 受限语言里，从而减少了翻译错误和状态爆炸。

### 5. pipeline 与 cache 在 `UPPAAL` 里只保留 timed skeleton

论文给出 ARM920T 5-stage pipeline 的 timed automata 模板：

1. `F`：fetch
2. `D`：decode
3. `E`：execute
4. `M`：memory
5. `W`：writeback

每级模板只关心：

1. 当前是否有指令 token；
2. 什么时候能 push 到下一阶段；
3. 当前阶段耗时多少；
4. 是否要等待 cache / main memory / hazard 清除。

instruction cache 与 main memory 也分别给出 TA 模板，但不再在 `UPPAAL` 内部精细重建完整 cache 内容，而是依赖外部注释决定 hit/miss。  
这一步说明作者并不是放弃 `UPPAAL` 的 hardware model，而是**把它收缩成专门负责 timed scheduling 的骨架模型**。

### 6. 用 `UPPAAL` 搜索 witness trace 与逐步 refinement

论文最后还指出，这套方法一个很实用的优势是能得到 producing `WCET` 的 witness trace，而不只是一个数字上界。并且因为程序路径与 cache behavior 都能被单独 refinement，它天然适合做：

1. 程序可行性 refinement；
2. cache 行为 refinement；
3. 逐轮缩紧上界。

这使得 `WUPPAAL` 不只是一次性分析器，而是可迭代改进的分析框架。

## 解决了什么问题

这篇论文解决的核心问题，是如何让 `UPPAAL` 在 `WCET` 场景里真正变成一个**通用 timed analysis back-end**。

第一，它把早先对特定 ISA/硬件紧耦合的方案推广成 generic framework。二进制语言、硬件 timed model、外部仿真器都被拆成独立模块。

第二，它显著减轻了 `UPPAAL` 内部离散状态负担。程序语义、寄存器值、cache 具体内容不再全塞进 `UPPAAL` 状态里，而是由 `qemu/gdb/libgdb2uppaal` 在外部维护。

第三，它保留了 timed automata 方法在 pipeline/cache 分析上的优势：与纯 ILP 或纯 abstract interpretation 路线相比，硬件并发和同步关系仍能自然建模。

第四，它给出了真正可运行的工具链 `WUPPAAL`，并在标准 benchmark 上展示了可行性。这说明这不是“理论上也许能用 `UPPAAL` 做 `WCET`”，而是已经被做成了实践路径。

## 与 `UPPAAL` 技术线的关系

这篇论文和 `UPPAAL` 主线的关系，可以理解为“把 timed automata 引擎外溢到 binary timing analysis”。它不是 `UPPAAL` 官方主分支里的通用功能，但却体现了 `UPPAAL` 技术线一个很重要的面向：**只要问题能压成 timed symbolic exploration，就能把 `UPPAAL` 当作后端求解器。**

它和文库中的其他条目关系如下：

1. 它继承了早期 `UPPAAL` 在 timed games、cost-optimal scheduling、SMC 等方向形成的“用同一引擎处理不同 timed objective”的思路。
2. 它与 [behrmann05-optimal-scheduling-priced-timed-automata](./../behrmann05-optimal-scheduling-priced-timed-automata/) 一样，都不是在改核心语义，而是在把引擎能力迁移到新的 timed objective 上。
3. 它同时又展示了很强的工程化倾向：`UPPAAL` 不必独占整条分析链，而可以通过接口和外部工具协同。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。原因是：

1. 问题定义、`WCET` 形式化、tree-API、工具链、硬件模板和实验都讲得比较清楚；
2. 但若真要完整复刻 `pre-analysis + qemu/gdb bridge + libgdb2uppaal + HW.xml`，还需要阅读作者的前序工作和实际工具实现。

从实现可获取程度看，更适合标 `🟥 暂未获取实现源码`：

1. 论文明确说实现了 `WUPPAAL`；
2. 也提到 benchmark/模型包；
3. 但当前没有看到稳定公开的完整源码仓库可直接获取这条工具链。

如果按更宽松口径，可以说有 `qemu/gdb` 与 `UPPAAL` 等外部可得底座；但在本库的严格“源码级实现”标准下，这仍不算论文实现源码可得。

## 对本研究的启发

对当前博士研究，这篇论文有两层启发。

第一，复杂验证工作流不一定要把全部语义硬塞进一个 formal tool 里。作者把“程序语义解释”交给 `qemu/gdb`，把“timed coordination”留给 `UPPAAL`，这种**职责拆分**很值得借鉴。

第二，若后续你的研究涉及从自然语言需求生成模型，再做验证与修复，这篇论文说明：可以把 LLM 更擅长的高层结构生成，与形式工具更擅长的时序求解分离，而不是期待单一工具包办一切。

第三，它还提醒了一点：只要接口设计得好，`UPPAAL` 并不只是一个封闭的 model checker，而可以成为更大验证管线中的 timed reasoning kernel。
