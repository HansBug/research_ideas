# Model Checking Timed Automata with Priorities Using DBM Subtraction

- 问题一句话：一旦 `UPPAAL` 要支持 priorities、urgent guards 或 timed games，一步 symbolic successor 就可能变成非凸集合，而标准 `DBM` 只擅长凸 zones。
- 方法一句话：论文把 priorities 正式加入 timed automata 语义，并围绕 `D - E = D \land \neg E` 这一关键 `DBM` subtraction 问题，提出最小约束、disjoint splitting、约束重排和 facet-intersection 等一组高效启发式。
- 解决点一句话：它把 `DBM` subtraction 这个长期缺位的底层操作真正做进了 `UPPAAL` 工具线，从而为 priorities、urgent guards 和 timed games 等扩展铺平了路。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于非常典型的 `🧱 核心算法/数据结构` 条目，同时又是 `🛠️ 工程/工具链` 的关键支撑条目。它的主问题不是“priority 语义本身复杂”，而是：

> 一旦低优先级 transition 的可达 valuation 要扣掉所有高优先级 transition 已覆盖的部分，结果就天然变成非凸；而 `UPPAAL` 的核心数据结构 `DBM` 恰恰只直接表示凸 zone。

因此，这篇论文在技术线里的意义远超“给 `UPPAAL` 加一个小功能”。它实际上解决的是 `DBM` 世界里少数最棘手、最缺基础设施的操作之一：subtraction。

## 立足问题

这篇论文面对的问题有两层。

第一层是建模层。真实实时系统大量使用优先级：

1. 任务优先级；
2. 中断优先级；
3. 通信总线或共享资源访问优先级；

如果工具不直接支持 priorities，用户就只能手工把优先关系编码进 guards 和额外边中，这既繁琐又容易错。

第二层是算法层。即便 priority semantics 本身并不难写，真正难的是 symbolic semantics。文中开头的例子很直观：若边 `a` 优先于边 `b`，那么 `b` 真正可走的 valuation 集合必须是：

1. 原 guard 允许的 valuation；
2. 再减去所有让更高优先级边 `a` enabled 的 valuation。

这类集合通常是非凸的，因此不能再由一个单独的 `DBM` 表示。

换句话说，论文真正立足的问题是：

1. 如何给 timed automata 加 priorities；
2. 更关键地，如何在 `DBM` 世界里高效做 subtraction，避免 zone splitting 爆炸。

## 核心方法

这篇论文的方法主线很清楚：**先定义 priorities 的 symbolic semantics，再把真正的难点收缩为 `DBM subtraction`，然后围绕 subtraction 设计一套越来越聪明的算法。**

### 1. 先把 priorities 作为 timed automata 的一等语义对象

作者首先引入带 priorities 的 network timed automata。优先级可以定义在两个层面：

1. actions 上；
2. automata 上。

并且优先级允许是 partial order，而不强制 total order。之后再通过动作优先级与 automata 优先级推导 transition 级的 blocking 关系。

语义直觉是：

1. 某 transition 若 enabled；
2. 且存在更高优先级 transition 同时 enabled；
3. 则前者被 block。

这使得普通 symbolic successor 计算发生根本变化：对某个低优先级 transition，不是只算 guard 交 invariant，而是还要减去被高优先级 transition 抢占掉的那部分 valuation。

### 2. 识别 subtraction 是真正的核心操作

作者非常明确地把问题压成：

$$
D - E = D \land \neg E
$$

其中 `D` 和 `E` 是 canonical `DBM`。

这个操作难的地方在于：

1. `D` 和 `E` 各自都是凸的；
2. 但 `D - E` 往往不是凸的；
3. 因此结果必须表示成一个 federation，也就是一组 `DBM`。

作者还指出 subtraction 不只对 priorities 有用，它还会在以下场景出现：

1. urgent transitions with clock guards；
2. deadlock checking；
3. timed games；
4. backward TCTL model-checking；
5. scheduling / controller synthesis。

因此，这篇论文的贡献并不是局部为 priorities 打补丁，而是补上了一块很多扩展都会用到的底层积木。

### 3. 从 basic subtraction 出发，承认它正确但太粗糙

最直接的 subtraction 做法，是把 `E` 的每个约束逐个取反，再用这些 negated constraints 去切 `D`，最终得到若干 `DBM` 的并。

优点是：

1. 很直观；
2. 正确；
3. 总复杂度可控制在 $O(n^4)$。

缺点则很明显：

1. 产生的 `DBM` 数量往往偏多；
2. 彼此还可能重叠；
3. 这些重叠会在后续 symbolic search 中重复制造工作。

所以 basic subtraction 只是一条 correctness baseline。

### 4. 用 minimal constraints 和 disjoint subtraction 先砍掉明显冗余

论文接下来做的第一类改进，是把 `E` 先缩成 minimal constraints form。因为若某些约束在 `E` 里本来就是冗余的，用它们来切 `D` 只会制造无意义 split。

第二类改进是把结果强制做成 disjoint union。作者引入 remainder `R` 概念，按某个顺序连续切分：

1. 每次从当前 remainder 里切出一块结果；
2. 剩余部分继续往后切；
3. 最终得到互不重叠的 `DBM` 集合。

这一步很重要，因为：

1. overlapping DBMs 会让后续 inclusion / exploration 成本重复叠加；
2. disjoint result 虽不一定总在每一步都最优，但更利于后续处理。

论文还给出 soundness / completeness 证明，说明这种 disjoint subtraction 语义上仍然是同一个 `D - E`。

### 5. 发现 split ordering 是决定质量的关键

作者进一步指出，一个 subtle 但极其关键的问题：**切分顺序很重要。**

即便最终 `DBM` 数量一样，不同顺序也可能得到：

1. 不同形状的 pieces；
2. 不同的 future inclusion behavior；
3. 不同的后续 splitting 成本。

因此，“最少当前 pieces”不一定代表“对 reachability 最优”。这也是论文批评已有工作“只说 optimal subtraction 但没说顺序”的地方。

### 6. 提出两层 heuristic：重排与 facet-intersection

这篇论文的真正算法亮点，在于两层启发式。

#### 6.1 基本重排启发式

作者定义度量：

$$
|e_{ij}| - |d_{ij}|
$$

并优先选择使该值最小的约束去切。直觉上，这是在优先选择那些“facet 更深入 `D` 内部”的约束，让早期 split 尽可能切出大块，从而减少未来 split 需求。

更巧妙的是，作者不是一次全排序，而是在每次 split 后重新计算，因为 `DBM` 已经变了，旧排序失去意义。

#### 6.2 Facet-intersection 启发式

更进一步，作者尝试忽略那些虽然属于 `E`，但其 corresponding facet 实际并不与 `D` 相交的约束。若某 facet 根本不碰当前 `D`，拿它来 split 就是在做无意义工作。

为此作者构造 `H'`，在检测某 facet 不相交时直接给出 `\infty`，从而把这类约束排除。实现上又用了两个小技巧：

1. 通过 tightening 与 specialized Floyd 变体高效构造 facet 检查；
2. 只看必要的少量约束，而不重算整个几何对象。

这条线很典型地体现了 `UPPAAL` 团队的风格：不是追求一个高大上的全局最优定理，而是做出一个在 reachability 实践里真正好用的 heuristic。

### 7. 用 priorities、timed games 与 job-shop 实验检验 subtraction

实验部分有两层。

#### 7.1 Priority 实验

用带 priority 的 Fischer protocol 比较：

1. 原模型；
2. 带原生 priorities 的模型；
3. 手工编码 priorities 的模型。

结论是：

1. 原生 priority 支持开销不大；
2. 与手工编码相比表现可比；
3. 但原生语义显然更好建模。

#### 7.2 重 splitting 实验

在 timed games 与 job-shop 这类 subtraction 更频繁、更重的原型上，作者比较：

1. basic；
2. reorder；
3. disjoint；
4. expensive heuristic；
5. efficient heuristic；

结果显示：

1. naive reorder 并不总是好；
2. disjoint 有时会对 inclusion 产生副作用；
3. expensive heuristic 性价比一般；
4. efficient heuristic 是整体最优折中。

这说明作者真的在用实际 symbolic engine 的行为来评价 subtraction，而不是只看单次运算结果长什么样。

## 解决了什么问题

这篇论文解决了 `UPPAAL` 技术线里一个长期基础设施缺口。

### 1. 它让 priorities 成为工具内建特性而非手工编码技巧

这直接提升了建模自然性，也减少了用户手工构造 disjunctive guards 的负担。

### 2. 它把 `DBM subtraction` 做成了可用操作

这点影响远超 priorities，本质上是给 `DBM` 家族补上了一个处理非凸差集的关键操作。

### 3. 它让后续涉及 federation reduction、timed games、urgent guards 的工作有了可复用底座

尤其是 timed games 分支，会直接受益于 subtraction quality。

## 与 UPPAAL 技术线的关系

这篇论文是多个分支的公共支撑点。

### 它接在谁之后

它建立在：

1. [bengtsson02-clocks-dbms-states](../bengtsson02-clocks-dbms-states/)
   - `DBM` 包与操作体系；
2. [bblp04-zone-based-abstractions](../bblp04-zone-based-abstractions/)
   - 对 `DBM` 外推与 canonicalization 的进一步优化。

### 它往后影响了谁

它往后直接影响：

1. [behrmann06-uppaal-4](../behrmann06-uppaal-4/)
   - priorities 成为官方工具特性。
2. [behrmann07-uppaal-tiga](../behrmann07-uppaal-tiga/)
   - timed games 工具实现受益于 subtraction / federation 改进。
3. 后续任何依赖 federation reduction 的 `UPPAAL` 扩展。

### 它更靠近哪条主线

它最靠近：

1. `DBM` 操作；
2. non-convex symbolic set handling；
3. priorities；
4. timed games 与 urgent guards 的基础设施。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - priorities 语义、subtraction 算法、heuristics、实验都讲得比较透，足以重建其方法主线。
2. **实现可获取程度**
   - 适合评为 `🟨 部分实现源码可得`。
   - 论文明确是在 `UPPAAL` 扩展版与实验原型中实现，后续不少思想进入官方 `UPPAAL 4` 与相关库，但历史原型未必独立可得。
3. **材料质量**
   - `paper_content.txt` 很适合后续深挖 federation / subtraction 主题，是一篇非常值钱的底层算法论文。

## 对本研究的启发

这篇论文对当前博士研究的启发很具体：**一旦系统要表达排他、优先、覆盖剔除或“被更强行为抢占”的逻辑，底层表示往往立刻从凸变成非凸。**

可直接借鉴的点包括：

1. 若未来闭环修复或控制建议要做“候选行为减去已知不可行/已被更高优先级占用部分”，底层差集表示会成为关键问题。
2. 一个基础数据结构真正成熟，往往取决于是否补齐了它最难但最常被需要的几个操作。
3. heuristic 的目标不应只看单步最优，还要看对后续搜索的长期影响。
