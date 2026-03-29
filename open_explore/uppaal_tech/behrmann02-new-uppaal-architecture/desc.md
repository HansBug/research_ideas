# New UPPAAL Architecture

- 问题一句话：旧版 `UPPAAL` 引擎在功能不断叠加后，代码结构、状态存储和层次化扩展能力都开始成为瓶颈。
- 方法一句话：用 filter/buffer pipeline 重构引擎，统一 `Passed` 与 `Waiting` 为 `PWList`，并通过 zone union 与共享存储压缩状态表示。
- 解决点一句话：把 `UPPAAL` 引擎从“功能堆叠的实现”推进成可扩展、可组合、可支撑 hierarchy 的新架构。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `🛠️ 工程/工具链` 条目，是 `UPPAAL` 技术线里非常关键的一篇**引擎架构重构论文**。如果说 [llpy97-compact-data-structure](../llpy97-compact-data-structure/) 解决的是“单个 `DBM` 和状态存储怎么更省”，那么这篇解决的是：

> 当优化选项越来越多、实验性特性越来越多、未来还想支持 hierarchy 时，整个 `UPPAAL` 引擎应该怎样重构？

它前接 [amnell01-uppaal-now-next-future](../amnell01-uppaal-now-next-future/) 中对未来方向的官方盘点，后面则会继续通向 [behrmann02-uppaal-implementation-secrets](../behrmann02-uppaal-implementation-secrets/) 和更系统的数据结构条目。

## 立足问题

这篇论文面对的问题很工程化，但一点也不次要。作者在引言里非常坦白地说：timed automata 的基本算法和局部优化技术虽然都已有了，但**它们如何在一个统一、灵活、仍然高效的实现中拼起来**，并没有被讲清楚。

旧实现的问题主要有三类：

1. **核心循环越来越复杂**
   - 新 feature 不断往 exploration loop 里加条件判断。
   - 代码可维护性和实验可替换性持续变差。
2. **状态空间存储成本高**
   - `Waiting` 和 `Passed` 分离导致重复 lookup 和内存浪费。
   - 同一离散状态下的多个 zones 也缺少更统一的组织。
3. **未来 hierarchy 支持需要动态作用域**
   - 层次化 timed automata 会导致 clocks、variables 和并发层级动态增减。
   - 传统“状态结构固定”的实现很难平滑支持这种变化。

所以这篇论文立足的问题不是抽象的“架构不好看”，而是：**如果不重构，引擎很难继续承接 `UPPAAL` 平台化演进。**

## 核心方法

这篇论文的方法主线很清楚：**用分层 pipeline 改造控制流，用 `PWList` 改造探索数据结构，用共享存储改造状态表示，并预先为 hierarchy 留出动态作用域接口。**

### 1. 用 layered architecture 把 checker 组织成 pipeline

论文首先把 `UPPAAL` 的内部组件重新划成几层：

1. system representation / query parser
2. state representation / state manipulation
3. state space representation
4. reachability / liveness / leads-to 等 checkers
5. command line / GUI interface

其中最重要的是中间两层不再直接被某个 monolithic exploration loop 调用，而是通过统一接口拼成 pipeline。作者把组件抽象成两类：

1. **buffers**
   - 负责存储对象，提供 `put` / `get` 等操作；
2. **filters**
   - 接收输入后做某一步变换，再把结果送到下游。

于是 reachability checker 不再是一个大函数，而是一串可插拔的过滤器链，例如：

1. `Transition`
2. `Successor`
3. `Delay`
4. `Normalisation`
5. `PWList`
6. `TraceStore`
7. `Progress`
8. `ActiveClockReduction`

这一步的意义很大：

1. 某个优化若关闭，可以直接绕开对应 filter，而不是在核心循环里插 if。
2. 同一个 `Successor` filter 可以被 reachability、deadlock、trace generation 等多个 checker 复用。
3. 实验不同算法组合时，不需要 fork 整个代码库。

作者也承认 virtual call 会带来大约 `5%` 左右的开销，但认为这点代价远小于统一架构带来的可组合性收益。

### 2. 把 `Passed` 与 `Waiting` 合并成统一的 `PWList`

这是全文最核心的具体改动之一。传统 reachability 里：

1. `Waiting` 存未展开状态；
2. `Passed` 存已展开状态。

但这会带来两个问题：

1. 插入新状态时，往往要分别检查 waiting 和 passed；
2. 某些 waiting states 其实已经被别的状态覆盖，却要到更晚的时候才意识到，浪费内存。

论文于是定义统一结构：

$$
PWList = (P, W)
$$

并把 `put / get` 统一起来。其语义上仍能表达 passed/waiting 的区别，但实现上：

1. 统一使用一张 hash table 记录已见状态；
2. waiting queue 只保存对这张表项的引用；
3. 于是 discrete lookup 不必做两遍。

作者给出的新算法里，核心逻辑也更简洁：从 `Q` 中弹状态后直接展开，只有 successor 插入时才做 inclusion check。这样一来：

1. 内存重复降低；
2. 离散状态判重只做一次；
3. exploration order 仍然与存储结构正交。

### 3. 把同一离散部分下的符号状态表示成 zone union

在 reference implementation 中，每个 hash entry 以 discrete part 为键，即：

1. location vector
2. integer variables

而连续部分则不再是一条单独 zone，而是一个 zone union。也就是说，同一离散控制配置下的多个连续约束被系统地挂到一起，而不是散落成多个完全独立状态项。

这种表示的好处是：

1. discrete duplicates 被天然消灭；
2. inclusion check 可先按离散部分哈希定位，再在该 union 内检查 zones；
3. 后续若要换成 `CDD` 表示 union，也有清晰接口可接。

这一点其实是把 earlier compact-state 结果进一步“架构化”了。

### 4. 用 specialised allocator 与 shared storage 压缩内存

论文接着往下做的，是更底层的 storage redesign。它把 location vectors、integer variable vectors、DBM data 等都交给 storage layer 管理，并在其下使用专门 allocator：

1. 以大块分配；
2. 面向少数几种固定尺寸对象；
3. 减少大量小对象分配的管理开销。

在 storage 上，作者实现了两个版本：

1. **simple copy**
2. **shared storage**

shared storage 的核心思想是：

1. 对 location vectors、variable vectors、DBM data 都做哈希；
2. 若已有相同数据则复用；
3. 利用实际 reachable state space 中极高的结构共享率节省内存。

论文通过 instrumentation 发现：

1. 不同模型里 location / variable / DBM 的共享度都相当可观；
2. 大模型共享更高；
3. 因而共享存储在 `UPPAAL` 这种状态空间搜索器里是值得的。

这使得“状态”不再被看成一个大对象，而是被拆解成多个可共享子结构。

### 5. 预先把 hierarchy 支持翻译成“动态作用域上的状态操作”

这篇论文另一大价值是：它不只是重构当下代码，而是明确把 hierarchy 当作未来需求来设计接口。

hierarchical timed automata 的难点在于：

1. clocks scope 会变；
2. variables scope 会变；
3. 并发层数会随进入/退出层次结构而变化。

这意味着 successor computation 不再能假定状态有固定维度。论文的方案是：

1. 先复制 discrete part；
2. 根据 transition 和新 scope 判断哪些 clocks 需要保留、哪些新增、哪些删除；
3. 再对 symbolic part 执行 add/remove clocks、delay、reset、assignment、invariant evaluation。

也就是说，hierarchy 在实现层被归结为：**状态维度与作用域是动态的，但 pipeline 仍能逐步完成 successor construction。**

这一步很关键，因为它把“支持 hierarchy”从语法问题转成了存储与状态变换问题。

## 解决了什么问题

这篇论文真正解决的是 `UPPAAL` 内核的三类瓶颈。

### 1. 它把引擎从“功能堆叠实现”改成了可组合架构

新 feature 不再需要不断侵入同一个 exploration loop，而可以通过增加、替换或跳过某个 filter 完成。

### 2. 它显著降低了状态存储成本

论文实验给出的结果很直接：

1. 单是新架构 copy 版就比旧版更快；
2. shared storage 版在某些 benchmark 上把内存压到原来的很小一部分；
3. time 和 space 都出现明显改进，文中摘要总结为大约 `80%` 的提升量级。

### 3. 它为 hierarchy 和更多未来优化留出了稳定接口

没有这层重构，很多后续工作只能通过局部 hack 接入；有了这层重构，不同 zone representation、hierarchical successor computation、更多 state-space representations 都有了清晰挂载点。

### 4. 它也保留了真实代价与边界

论文没有把 pipeline 吹成零成本，也承认：

1. virtual interface 有调用开销；
2. shared storage 并非所有数据都完全回收；
3. hierarchy 真正高效还需要后续工作继续实现。

这种工程上的诚实非常重要。

## 与 UPPAAL 技术线的关系

这篇论文是 `UPPAAL` 工程内核演进里的一个转折点。

### 它接在谁之后

它直接接在：

1. [llpy97-compact-data-structure](../llpy97-compact-data-structure/)
   - 已经提出局部和全局空间削减。
2. [amnell01-uppaal-now-next-future](../amnell01-uppaal-now-next-future/)
   - 已经把 hierarchy、CDD、distributed exploration 等列为下一步方向。

### 它往后影响了谁

它往后最直接影响的是：

1. [behrmann02-uppaal-implementation-secrets](../behrmann02-uppaal-implementation-secrets/)
2. [behrmann03-real-time-data-structures](../behrmann03-real-time-data-structures/)
3. `UPPAAL 4` 及更后续版本的内核工程线。

### 它更靠近哪条主线

它最靠近的是：

1. 引擎架构；
2. 状态空间存储；
3. hierarchy-ready implementation；
4. modular checker infrastructure。

## 实现与材料

1. **内容详细程度**
   - 当前总账给它记为 `🟨 中等`，我认为这个口径偏保守但合理。
   - 原因是论文把核心结构和实现意图讲得很清楚，也有实验，但很多接口与实现细节仍停留在架构层，不像 thesis 那样细到每个子模块都可直接复刻。
2. **实现可获取程度**
   - 当前总账记为 `🟨 部分实现源码可得`，合理。
   - 因为论文讨论的许多底层主题今天可以沿 `UDBM`、`utap`、`uppaal-libs` 等公开组件继续追实现线。
3. **材料质量**
   - `paper_content.txt` 足以支撑重建架构层和数据结构层的主线。
   - 若后续要继续细抠 `PWList` 某个变体或 hierarchy successor implementation，仍建议联读后续 implementation 论文。

## 对本研究的启发

这篇论文对当前博士研究的启发很强，因为它提醒我们：**一条闭环研究线若想长期扩展，架构设计本身就是研究对象。**

至少有四点值得直接借鉴：

1. 后续若要把 LLM 建模、验证、诊断、修复做成平台，必须有清晰的 pipeline 与可插拔组件，而不能把所有逻辑塞进一个主循环。
2. 中间状态表示要尽量拆成可共享子结构，否则闭环一扩规模就会先死在内存上。
3. 搜索顺序、状态存储与后处理信息记录应尽量正交，便于后续替换与实验。
4. 若未来要支持层次状态机、局部变量或不同抽象粒度，现在就需要为“动态作用域”预留接口，而不是等功能加上来再返工。
