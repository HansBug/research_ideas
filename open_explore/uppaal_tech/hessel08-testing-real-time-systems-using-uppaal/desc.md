# Testing Real-Time Systems Using UPPAAL

- 问题一句话：实时测试不仅要考虑动作，还要考虑何时刺激、何时响应、如何判 verdict，以及如何在离线与在线两类流程中复用 `UPPAAL` 的能力。
- 方法一句话：本章以 `UPPAAL` 为统一底座，同时系统展开 relativized real-time conformance、offline test generation、observer-based test purpose/coverage、以及 `TRON` 支持的 online testing。
- 解决点一句话：它把 testing 分支前几年的多篇工作汇成了一套完整方法学，形成 `UPPAAL` 测试线的章节级总论。

## 论文定位

这篇论文在 `uppaal_tech/` 中最适合归到 `🧪 扩展方向` 与 `🛠️ 工程/工具链` 的总论条目。它不是单个新算法论文，而是一篇**testing 线的汇总性章节**，把：

1. 实时 conformance 关系；
2. offline test generation；
3. observer-based coverage / test purposes；
4. online testing 与 `TRON`；

统一整理进一个框架。

和前面的 testing 论文相比：

1. [mikucionis03-online-on-the-fly-testing-real-time-systems](../mikucionis03-online-on-the-fly-testing-real-time-systems/)
   - 更像起步原型；
2. [larsen04-online-testing-real-time-systems-using-uppaal](../larsen04-online-testing-real-time-systems-using-uppaal/)
   - 更像正式 online 算法论文；
3. 本章则是把整个 testing 路线拉成一套体系。

## 立足问题

这篇章节立足的问题，是实时测试并不只是“把 model checker 拿来生成几个 traces”。

作者在开头就强调，real-time testing 会影响整个流程的每个环节：

1. 规格语言必须表达时间约束；
2. conformance 关系必须定义什么叫“时间上正确”；
3. test purposes / coverage 必须能形式化；
4. 生成算法必须足够快，能应对复杂规格；
5. 在线执行时测试器自己也成为一个实时系统。

因此，本章真正面对的是一个方法学问题：

> 若把 `UPPAAL` 当成 testing platform，而不只是 verifier，那么应该怎样组织 offline 与 online 两套流程，并让它们共享同一套语义与模型基础。

## 核心方法

这篇章节的核心方法，是以 `UPPAAL` timed automata 为共同语言，把 testing 分成两大分支并统一到同一个 conformance 框架下。

### 1. 用显式环境 + 系统模型作为统一规格入口

章节一开始就坚持环境与系统分离建模：

1. `E`
   - 环境模型；
2. `S`
   - 系统规格模型；
3. `IUT`
   - 被测实现。

这样做的意义不只是语义漂亮，而是 practical：

1. 可以只生成与环境相关的 realistic test scenarios；
2. 可以在不同环境假设下复用系统模型；
3. 可以把 environment emulation 与 system monitoring 分开思考。

这条思路贯穿 offline 与 online 两部分。

### 2. 继续采用 relativized timed input/output conformance

本章沿用并系统阐释 `rtioco` 路线。它强调：

1. 只在显式环境约束下谈实现是否 conform；
2. 核心直觉等价于 relativized timed trace inclusion；
3. 时间上的 quiescence 只能被看作有限时间范围内的安静，而不是 untimed `ioco` 式抽象永恒静默。

这一步使整章的 offline / online 方法都建立在同一 correctness notion 上，而不是各玩各的。

### 3. Offline testing：把 test purpose / coverage 编译成可验证目标

章节前半详细讲 offline test generation。其核心假设是：

1. 针对一类受限但很有用的规格；
2. 尤其是 deterministic、output urgent 的 timed automata；
3. 可把 test generation 编译成 model-checking 问题。

作者说明 `UPPAAL` 可生成：

1. some trace；
2. shortest trace；
3. fastest trace。

其中 fastest trace 使用一种变体的 `A*` 算法。也就是说，本章并不是只说“能离线生成”，而是明确把生成目标做成：

1. 最快满足 test purpose；
2. 最小化执行时间；
3. 或满足特定覆盖准则。

这对 real-time testing 很重要，因为测试时间本身就是成本。

### 4. 用 observers 把 coverage / test purposes 做成通用语言

本章最有方法价值的一块，是 observer automata。

作者指出，若对每种 coverage criterion 都靠手写模型注释或 reachability 公式，会很笨重也很不友好。因此他们提出用 observer 作为 coverage / test purpose 的统一表达语言：

1. observer 监控被测 timed automaton 的离散边、位置、变量使用等；
2. 一旦某 coverage item 被满足，observer 进入 accepting 状态；
3. observers 可参数化，从而表达一整类 coverage items。

章节里给出多种例子：

1. all-locations coverage；
2. all-edges coverage；
3. definition-use pairs；
4. all-definitions；
5. data-flow 风格 coverage；

更重要的是，observer 被定义成可以自动 superimpose 到原模型上，而不是要求用户手改模型本体。

这一步很强，因为它把 testing target specification 正式模块化了。

### 5. 用 bit-vector 扩展 reachability 算法来求最大 coverage

observer 有了以后，还需要更高效地求解“单条 trace 最多能覆盖多少 items”这类问题。章节因此给出一个扩展算法：

1. 在 symbolic reachability 基础上加入 bit-vector；
2. bit-vector 记录已经覆盖了哪些 observer accepting states；
3. 由此可在搜索过程中直接优化 maximum coverage。

这说明作者在 offline testing 部分不仅给出表达语言，还认真考虑了 coverage 求解效率。

### 6. Online testing：用 `TRON` 执行 sound & complete 算法

章节后半转入 online testing。它沿用此前 online line 的核心算法，并把它落实到 `TRON` 工具中。

`TRON` 的关键对象包括：

1. adapter；
2. environment model；
3. implementation model；
4. `UPPAAL` symbolic engine；

其中最值得注意的一点，是作者明确把 online testing 看成两个子任务：

1. **environment emulation**
2. **IUT monitoring**

这和 [larsen04-online-testing-status-future-work](../larsen04-online-testing-status-future-work/) 中的路线图是一致的。

也就是说，本章不只是复述算法，还把工具架构视角融进来了。

### 7. 把 offline / online 视为一个光谱，而不是对立选项

本章一个成熟的地方，在于作者并没有把 offline 与 online 写成互斥范式，而是明确说它们是一个 spectrum 的两端：

1. offline
   - 更适合提前求 time-optimal traces、coverage-guaranteed suites；
2. online
   - 更适合长时间运行、全非确定规格、持续交互。

两者都共享：

1. timed automata 规格；
2. relativized conformance；
3. `UPPAAL` symbolic engine。

这使整章真正有“平台方法学”味道。

## 解决了什么问题

这篇章节解决的是 testing 分支知识分散的问题。

### 1. 它把 `UPPAAL` testing 线的共同语义底座固定下来了

无论 offline 还是 online，都回到显式环境模型与 relativized conformance。

### 2. 它把 coverage / test purpose 从 ad hoc 技巧变成了 observer 语言

这让 test objective specification 有了可复用、可组合的正式表示。

### 3. 它把 `UPPAAL` testing platform 的两种主要工作流都讲清楚了

offline 与 online 各自的优劣势、适用场景与算法接口，都在本章里被明确区分。

## 与 UPPAAL 技术线的关系

这篇章节在 `UPPAAL` 技术线中相当于 testing 分支的“总账”。

### 它接在谁之后

它综合了：

1. [mikucionis03-online-on-the-fly-testing-real-time-systems](../mikucionis03-online-on-the-fly-testing-real-time-systems/)
2. [larsen04-online-testing-real-time-systems-using-uppaal](../larsen04-online-testing-real-time-systems-using-uppaal/)
3. [larsen04-online-testing-status-future-work](../larsen04-online-testing-status-future-work/)
4. 以及 offline coverage / observer 生成这条较少被单独记账的路线。

### 它往后影响了谁

它往后影响：

1. 更成熟的 `TRON` / online testing 实践；
2. observer-based offline test generation；
3. testing 分支与 coverage / diagnosis 进一步结合的工作。

### 它更靠近哪条主线

它最靠近：

1. model-based testing；
2. offline / online real-time testing；
3. observer-based coverage；
4. `TRON` 工具体系。

## 实现与材料

1. **内容详细程度**
   - 这篇章节适合评为 `🟩 较完整`。
   - 它覆盖范围极广，而且不只是概览，offline / online / observers / TRON 都给了较系统的说明。
2. **实现可获取程度**
   - 适合评为 `🟨 部分实现源码可得`。
   - 章节依托 `UPPAAL`、observer-based generator 和 `TRON` 等工具线，但各工具的源码与可执行可得性并不完全相同，不能一概写成“完整源码可得”。
3. **材料质量**
   - 这是 testing 分支非常关键的母条目，后续若要继续把 testing 线补成更细文库，应优先以它为中心组织。

## 对本研究的启发

这篇章节对当前博士研究的启发很直接，因为它展示了一条和你关心的“生成-验证-执行-反馈”非常接近的方法学路线。

具体可借鉴的点有：

1. 离线与在线并不矛盾，应被设计成共享同一模型与正确性关系的两种工作模式。
2. coverage / test purpose 最好有独立语言，而不是直接污染主模型。
3. 如果未来要把 `LLM` 生成的模型用于测试，observer 这类可叠加机制会非常有价值。
4. environment emulation 与 system monitoring 的分离，对任何真实运行时验证闭环都很关键。
