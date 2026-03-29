# UPPAAL - Now, Next, and Future

- 问题一句话：`UPPAAL` 在 2001 年前后已经分化出多条能力线，但整体技术版图、下一步方向和工程重点还缺少一次官方盘点。
- 方法一句话：先总结 `Uppaal2k` 的当前语言、验证器和优化，再系统枚举 cost-optimal、parametric、stopwatch、probabilistic、hierarchical、executable、animation 与新数据结构方向。
- 解决点一句话：把 `UPPAAL` 从单一实时验证工具明确推进成一个正在分叉演进的平台型技术路线图。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `🛠️ 工程/工具链` 条目，但它更准确的角色是 **官方技术路线盘点与议程文献**。如果说 [lpy97-uppaal-nutshell](../lpy97-uppaal-nutshell/) 负责把早期 `UPPAAL` 讲成一个完整工具箱，那么这篇则负责回答：**这个工具箱接下来要往哪些方向长、为什么要长、哪些方向已经有雏形。**

它所处的时间点非常关键：

1. 早期 `UPPAAL` 核心 reachability 工具已经稳定。
2. `Uppaal2k` 已经完成了界面和架构层面的重要升级。
3. 团队内部同时在推进 cost optimality、parametric timed automata、stopwatches、probabilistic timed automata、hierarchy、distributed exploration、CDD 等多条分支。

所以这篇论文不是单点贡献，而是一次对 `UPPAAL` 技术生态的“官方截面照”。

## 立足问题

这篇论文面对的问题，不是某一个算法卡住了，而是 `UPPAAL` 已经开始从单核工具变成多分支平台之后，**整体脉络、优先问题和未来增量方向不再容易从单篇论文中看清**。

具体说，有三类现实需求在推动它出现：

1. **现状需要统一说明**
   - `Uppaal2k` 已经不是 `1997` 那个版本了。
   - 模板、局部变量、Java GUI、socket client/server、更多查询和优化选项都已经出现。
2. **未来方向需要被组织起来**
   - 团队并行推进多条研究线，如果没有统一盘点，外部读者很难理解各分支与主引擎的关系。
3. **平台身份需要被明确**
   - `UPPAAL` 不再只是“验证 timed automata 是否可达”，而是在向 optimization、hybrid、probabilistic、testing、distributed 等方向扩展。

因此，这篇论文真正要解决的是：**给 `UPPAAL` 一张面向研究者和工程用户都可读的技术地图**。这也是它为什么采用“Current Version / New Directions / Recent Developments / Case Studies”这种结构。

## 核心方法

这篇论文不是算法论文，因此它的方法性贡献主要体现在“如何组织整条技术线”。从内容组织上看，它做了三件非常重要的事。

### 1. 先把 `Uppaal2k` 的当前能力重新定义清楚

论文首先回顾当前版本，不是简单重复早期介绍，而是明确说明 `Uppaal2k` 已经发生了哪些关键变化。

第一层是**产品结构升级**：

1. GUI 改为 Java。
2. 核心 verification engine 继续使用 C++。
3. 整个系统变成 socket-based client/server。

这意味着 `UPPAAL` 的工程边界已经变化：

1. GUI 和 verifier 可以分离部署。
2. 一个 server 可以服务多个 clients。
3. 系统的可维护性、可移植性和界面集成能力明显增强。

第二层是**建模语言升级**：

1. 支持 process templates。
2. 支持局部 clocks、局部 variables、局部 constants。
3. 支持更丰富的 bounded data structures，如 arrays。

这使得系统描述从“写一堆并行 automata”进一步演化成“模板化、可复用的实时组件建模语言”。也就是说，`UPPAAL` 在这一阶段已经开始主动靠近更真实的软件建模工作流。

第三层是**验证能力与优化选项的整理**：

1. 当前查询支持 `E<>`、`A[]`、`E[]`、`A<>` 和 `-->`。
2. 引擎仍以 forward symbolic exploration 为核心。
3. 但已叠加 bit-state hashing、convex-hull approximation、active/inactive clock reduction 等优化选项。

这一步的意义在于：论文先把“现在能做什么”讲清楚，再往后谈未来扩展。没有这一层，后面的 roadmap 就会悬空。

### 2. 用“新方向矩阵”把多条未来支线逐一展开

这篇论文最重要的方法动作，就是把未来分支不是列成一个清单，而是逐条写出它们**为什么需要、打算怎样做、与原 `UPPAAL` 的接口在哪里**。

#### 2.1 `COUppaal`: cost-optimal search

论文先介绍 `UPPAAL` 如何从“找到可行 trace”进一步走向“找到最优 trace”。其核心对象是：

1. `UPTA`
2. `LPTA`
3. priced zones

也就是说，未来代价不再只是“用时最短”，而是把 location / transition prices 一并纳入。这里明确说明了从 scheduling problems 到 optimal traces 的演化方向，也把 [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/) 这条线纳入官方 roadmap。

#### 2.2 `Parametric-Uppaal`

这里论文讲得相当具体：它不是口头说“支持参数”，而是把核心对象写成：

1. guards 中允许线性参数表达式；
2. 把 `DBM` 推成 `PDBM`；
3. symbolic state 变成“location vector + PDBM + constraint set”。

也就是说，参数化 reachability 的处理方式，是把未知参数的比较分支显式积累进 constraint set，而不是黑箱调用搜索器。这非常像把 timed model checking 继续向 symbolic synthesis 推一步。

#### 2.3 `Stopwatch-Uppaal`

这条线针对 hybrid systems 里的表达能力不足。论文并没有直接跳到一般线性混杂自动机，而是采取一个很 `UPPAAL` 风格的折中：

1. 允许 stopwatches，也就是偶尔停止的 clocks；
2. 用它去近似更一般的 linear hybrid automata；
3. 继续尽量复用现有高效数据结构与 reachability 算法。

方法重点在于：不是立刻引入一般 polyhedra 工具链，而是寻找“最小表达力增量”以保持 `UPPAAL` 的算法优势。

#### 2.4 `PrUppaal`

论文把 probabilistic timed automata 作为下一条核心扩展。它不只是说“边上加概率”，还点出了关键难题：

1. 现有 region-based 解法太容易状态爆炸；
2. 直接修改 forward reachability 又不能一般性地决定简单可达性质；
3. 因而计划结合稳定的 probabilistic zone graphs、CDD 和 dynamic partitioning。

这一步非常重要，因为它显示 `UPPAAL` 团队已经意识到：概率扩展不是单独再加一个语义，而会反过来要求新的 symbolic representation。

#### 2.5 `HUppaal`

hierarchical timed automata 在文中被视为下一代建模层扩展。这里论文强调的不是语法糖，而是：

1. hierarchy 可以服务于抽象层次化建模；
2. 可以帮助表达模板复用与结构对称；
3. 有希望支持 compositional verification 与 refinement；
4. 但 timed setting 下因为全局时间同步，真正高效利用 hierarchy 并不容易。

换句话说，这里已经把 hierarchy 同时定位为“建模可读性增强”和“潜在分析优化入口”，而不是单纯画图方便。

#### 2.6 `ExUppaal`

这是一个很值得注意的方向：论文把 timed automata 明确地看成可执行软件的抽象，并尝试把 location 和任务队列绑定。

其核心对象包括：

1. 节点上挂 periodic / sporadic tasks；
2. 任务实例进入 scheduling queue；
3. 语义状态扩成“location + clock valuation + task queue”；
4. 调度正确性用 schedulability analysis 来判定。

这说明团队在这一阶段已经不满足于“验证模型”，而在尝试把 timed automata 往 program execution / code synthesis 方向推进。

#### 2.7 Hybrid automata animation

这一方向同样很有工程意味。论文不是想把整个 `UPPAAL` 变成 hybrid model checker，而是要在 animator 一侧接入 ODE-based environment visualization：

1. system 仍主要用 timed automata；
2. environment / animation 可用更 expressive hybrid automata；
3. 数值求解用 `CVODE`；
4. 动画由变量值、location 和 signals 驱动。

这个想法说明团队很早就意识到：**模型验证和模型可视化并不是一回事**，很多情况下需要更丰富的外部环境表达来帮助人理解模型。

### 3. 把“近期效率研发”明确成数据结构与分布式两大方向

除未来应用线外，论文还专门整理了“提升引擎能力”的内部研究。

#### 3.1 `CDD`

论文把 CDD 介绍成对 `DBM` 的关键补充，因为 `DBM` 不封闭于 union，而 symbolic exploration 又不断需要做 set union。CDD 的核心思想是：

1. 用 clock-difference decision tree 表示约束；
2. 一条 root-to-true path 表示一组差分约束合取；
3. 整个 CDD 表示所有这些路径对应集合的并。

于是它天然支持 non-convex unions，并能通过 sharing common substructure 省空间。论文还给出实验结论：有些场景下空间可省到 `99%`，但 canonical-form 相关运算会更复杂，运行时间可能上升。

#### 3.2 compact state representation

论文还介绍了两套更紧凑的状态打包方案：

1. 把离散部分编码成数字；
2. 进一步压缩 `DBM` 的存储；
3. 在空间和 inclusion-check 代价之间做不同权衡。

这表明 `UPPAAL` 团队当时已经非常明确地把“单状态存储格式”当成一等研究对象。

#### 3.3 distributed exploration

这部分也讲得很实。分布式版本不是随便把任务并行化，而是：

1. 用 hash-based distribution 把 symbolic states 分配到节点；
2. 每个节点维护自己的 `Waiting` / `Passed` 片段；
3. 为保证 inclusion 判断正确，分发只依赖 symbolic state 的 discrete part；
4. 搜索顺序尽量逼近 breadth-first，以减少多余 explored states。

可以看出，团队已经清楚意识到：在 timed symbolic verification 里，“并行化”首先是一个**状态分发和搜索顺序问题**，不是纯算力堆叠问题。

#### 3.4 dynamic partitioning

这条线把 abstract interpretation 引进来，目标是自动调整抽象精度。方法重点是：

1. 从很粗的 partition 开始；
2. 若当前精度不足以证明 safety property，就继续 refine；
3. 直到足够证明，或 refinement 已不值得继续。

这其实是在回答 `UPPAAL` 长期面临的一个老问题：如何在 precision 和 efficiency 之间自动找到合适位置。

## 解决了什么问题

这篇论文解决的，不是某一个验证算子，而是 `UPPAAL` 技术线在 2001 年时“如何被整体理解”的问题。

### 1. 它把 `UPPAAL` 从单工具重新定位成平台

在这篇文章里，`UPPAAL` 已经不再只是 timed reachability checker，而是一个可以向 optimization、parameter synthesis、hybrid approximation、probabilistic verification、hierarchy、distributed exploration 等方向延展的平台。

### 2. 它把不同分支和主引擎的关系说清楚了

很多平台会不断长新能力，但各分支之间关系模糊。这篇论文的好处在于：它明确告诉你哪些方向是在扩**语义模型**，哪些是在扩**分析任务**，哪些是在改**底层数据结构**，哪些是在改**用户交互层**。

### 3. 它让后续检索与扩库有了稳定骨架

从今天回看，这篇论文几乎是一份 `UPPAAL` 早期研究地图。后续检索作者、关键词和论文簇时，它可以直接拿来当分类索引。

### 4. 它也诚实保留了大量“未完成态”

论文里许多方向还只是 prototype、planned 或正在尝试。也正因为如此，它非常适合帮助我们区分：

1. 当时已经成熟上线的能力；
2. 当时只是正在探索、后来才真正长成的能力。

## 与 UPPAAL 技术线的关系

这篇论文和 `UPPAAL` 技术线的关系，更像一个“官方分叉说明书”。

### 它接在谁之后

它直接接在：

1. [lpy97-uppaal-nutshell](../lpy97-uppaal-nutshell/)
   - 先把早期 `UPPAAL` 的完整工具箱形态讲清楚。
2. [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/)
   - 其中一条未来分支已经开始具象化。
3. [hune01-guided-synthesis-control-programs-uppaal](../hune01-guided-synthesis-control-programs-uppaal/)
   - 也被它吸纳进 recent case study / roadmap 叙事里。

### 它往后影响了谁

它往后几乎影响了整个文库的后续分支：

1. `priced / optimization`
2. `parametric`
3. `hybrid / stopwatch`
4. `probabilistic / SMC`
5. `hierarchy`
6. `distributed verification`
7. `CDD / compact states`

### 它更靠近哪条主线

它最靠近的是：

1. `UPPAAL` 官方路线图；
2. 工程能力分叉；
3. 研究平台化演进。

## 实现与材料

1. **内容详细程度**
   - 当前总账记为 `🟧 概览级`，我认为合理。
   - 原因是它覆盖非常广，但对各支线多以“问题 + 核心对象 + 当前进展”的层级讲述，不是每条线都给到可直接复现的算法细节。
2. **实现可获取程度**
   - 当前总账记为 `🟨 部分实现源码可得`，这个判断也合理。
   - 因为文中涉及的许多方向后来能沿官方 `UDBM`、`utap`、`uppaal-libs`、文档站与下载页追到部分实现线索，但论文中的很多 prototype 并没有统一开源快照。
3. **材料质量**
   - `paper_content.txt` 足够支撑我们重建每条方向的意图和技术定位。
   - 若后续要深挖某一条分支，仍必须回到该分支自己的主论文。

## 对本研究的启发

这篇论文对当前博士研究最直接的启发，是它展示了一个成熟技术平台如何管理自己的演进：**不是把所有增量都塞进同一个核心，而是清楚地区分主引擎、语义扩展、工程工作流和实验性分支。**

具体来说，有四点值得吸收：

1. 后续若要把 LLM 状态机建模、性质生成、验证剖面和修复做成平台，也必须明确哪些是主闭环、哪些是支线能力。
2. 一条研究线若想长期可扩张，就需要像这篇论文一样定期做“当前能力 + 下一步方向”的结构化盘点。
3. 数据结构与工作流改造，常常和新语义扩展同样重要，不能只盯理论表达力。
4. 对我们整理 `UPPAAL` 文库而言，这篇论文本身就是后续扩库的一级导航图。
