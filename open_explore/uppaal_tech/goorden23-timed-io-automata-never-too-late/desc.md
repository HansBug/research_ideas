# Timed I/O Automata: It is never too late to complete your timed specification theory

- 问题一句话：早期 timed interface / `TIOA` 工作已经给出不少核心想法，但在“实现是什么、何时一致、怎样做 conjunction/composition/quotient、这些操作如何和 refinement 严格配合”上仍缺一套完整、可证明、可工具化的统一理论。
- 方法一句话：以 `TIOTS/TIOA` 为统一语义与语法层，重新定义实现、refinement、consistency、conjunction、composition、quotient 及两类 pruning，并给出全套定理和 `ECDAR` 实现指向。
- 解决点一句话：把 timed specification theory 从“部分可用的研究片段”补成一套真正完整的组件规约理论。

## 论文定位

这篇论文是 `uppaal_tech/` 文库里 `🧱 核心算法/数据结构` 与 `⚡ 改进与扩展` 的交叉核心条目。它之所以关键，不是因为它又提出了一个新 operator，而是因为它把 timed specification theory 需要的几乎全部结构一次性补齐了：

1. 规格是什么。
2. 实现是什么。
3. refinement 如何定义。
4. consistency 怎样判。
5. conjunction 和 composition 怎样定义且如何配合。
6. quotient 作为 composition 的对偶怎样成立。

而且这次不是只给会议短文版的主张，而是把证明、边界条件、修正过的定义和工具实现关系都彻底铺开。对 `ECDAR` 线来说，这篇文章相当于“正式教科书版本”。

## 立足问题

文章开头就把问题讲得很清楚：如果想让组件化 timed system 的设计真正可组合，就必须有一套完整 specification theory。

这类理论至少需要回答四件事：

1. `refinement`
   - 一个规格能否替代另一个规格。
2. `conjunction`
   - 两个规格的要求能否同时满足。
3. `composition`
   - 两个组件规约合起来意味着什么。
4. `quotient`
   - 如果系统总规格 `T` 已知，而已有部件 `S` 已实现，那么“剩下那个部件”应该满足什么规格。

过去已有 timed interface / TIOA 工作，但论文明确指出它们各有缺口：

1. 有的只定义了 composition，没有实现与 refinement。
2. 有的有 refinement，却没有 quotient。
3. 有的给出原型工具，但理论不完整或不支持连续时间。
4. 早期版本对 pruning、quotient、严格不良状态等定义也存在需要修正的地方。

因此这篇文章不是“另起炉灶”，而是在原有 timed I/O 自动机与接口理论基础上做一轮系统补完。

## 核心方法

这篇论文的核心方法就是把 specification theory 的每个基础构件重新钉牢，而且这些构件之间严格互相配合。下面按对象与逻辑顺序拆开。

### 1. 用 `TIOTS` 做语义层，用 `TIOA` 做有限表示层

论文首先区分：

1. **Timed I/O Transition Systems (`TIOTS`)**
   - 真正的语义对象。
   - 通常状态无限。
2. **Timed I/O Automata (`TIOA`)**
   - 作为 `TIOTS` 的有限符号表示。

这一步很重要，因为后文很多定义先在 `TIOTS` 上给出，再说明如何在 `TIOA` 上实现。也就是说，理论不是绑死在 automaton syntax 上，而是先有语义，再谈具体实现。

同时，论文坚持 deterministic setting，并要求输入输出动作集合显式区分，这为后续 refinement 与 composition 的“责任归属”提供基础。

### 2. 明确区分 specification 与 implementation

这是整篇论文一个非常重要的决断。很多早期 timed interface 工作没有把“规格”和“实现”严格区分开，而这篇论文明确认为：

1. **规格**
   - 必须 input-enabled。
   - 因为环境输入不应被系统阻止，只能被显式建模为各种可接受/不可接受后续行为。
2. **实现**
   - 是规格的一个子类。
   - 必须满足 output urgency 与 independent progress。

其中 implementation 的两个关键条件最值得记：

#### 2.1 Output urgency

如果某个输出已经可以发生，那么实现不能无限拖延它。形式直觉是：

1. 若存在输出 `o!`
2. 同时还能做正延迟 `d > 0`
3. 那就不算实现语义下的“确定可执行行为”

这保证实现的输出时机是可预测的。

#### 2.2 Independent progress

实现不能卡在“除非环境先发输入，否则自己连时间都不往前走”的状态里。论文要求：

1. 要么实现可以无限延迟。
2. 要么存在某个延迟后，它能自己发出输出推动系统前进。

这条条件非常关键，因为它把“被动等环境拯救”的状态排除出了实现集合。也正因此，implementation 成了“真正能落地执行的系统”，而不只是另一个 underspecified automaton。

### 3. 用 alternating timed simulation 风格定义 refinement

有了 specification / implementation 区分后，论文给出 refinement `S \le T`。它的本质是 alternating timed simulation：左右两边对输入、输出和 delay 承担不同义务。

其规则可以概括成五条：

1. 右边能接收的共享输入，左边也必须能接。
2. 若输入只在右边字母表中出现，则左边可以原地保持关系。
3. 左边发出的共享输出，右边必须能匹配。
4. 若输出只在左边出现，则关系要跟着左边输出后的状态继续。
5. 左边能延迟多少，右边都必须能匹配相同延迟。

这种定义把 input/output 的责任清晰区分开：

1. 输入代表环境施加给系统的压力。
2. 输出与 delay 代表系统自己对外许诺的行为。

因此 refinement 不是简单 trace inclusion，而是交互责任意义下的替换关系。

### 4. 证明 refinement 与实现集合包含对应

论文的第一个大结果之一，是在局部一致且动作集相同的条件下：

$$
S \le T \iff \llbracket S \rrbracket_{\mathrm{mod}} \subseteq \llbracket T \rrbracket_{\mathrm{mod}}
$$

这极其重要，因为它说明 refinement 不是“看起来像包含”，而是真的和实现集合的包含精确对应。对 specification theory 来说，这是 refinement 合理性的核心保证之一。

### 5. 把一致性问题转成可控避免 error state 的游戏

论文并不把 consistency 只定义成“局部结构上看没毛病”，而是区分了：

1. `local consistency`
   - 每个状态本地看起来都允许独立进展。
2. `consistency`
   - 存在至少一个 implementation 满足该 specification。

为此，作者引入：

1. `imerr`
   - immediate error states
2. `err(X)`
   - 在给定坏状态集合 `X` 下，哪些状态会因输出/时间前进责任而成为 error
3. `incons`
   - 由 controllable predecessor / fixed-point 反推出的全体不一致状态

这里的核心思想是：一个状态即便现在还能动，只要所有能走的输出最终都会落入坏状态，而且它又不能无限安全延迟，那么这个状态仍应被视为不一致。

于是 consistency 最终被组织成一个安全游戏：

1. 若环境能强迫系统走到 error，则该规格不一致。
2. 若存在输出方策略总能避开 error，则规格一致。

### 6. 引入 adversarial pruning，把一致规格化成局部一致规格

论文随后定义 adversarial pruning `S^\Delta`：把所有 inconsistent states 以及相关迁移砍掉，只保留 `cons` 中的部分。

它的重要性质是：

1. 剪完之后得到 locally consistent specification。
2. 不改变实现集合。

这一步特别关键，因为它把“理论上有实现，但内部夹杂坏状态”的规格，转成了更干净的、可继续参与后续 operator 的规格。

作者后来又明确区分出 `cooperative pruning`，就是因为 adversarial pruning 并不总和 composition 可交换。这是本文相对早期版本的一个重要修正点。

### 7. 定义 conjunction，并证明它是 shared refinement

论文的 conjunction 不是简单交集，而是：

1. 先做类似积构造。
2. 再通过 adversarial pruning 去掉引入的不一致状态。

得到的结果满足：

1. `S ∧ T` 同时细化到 `S` 和 `T`。
2. 任何同时细化到 `S` 与 `T` 的规格，也会细化到 `S ∧ T`。

也就是说 conjunction 真正成为 refinement 格上的 greatest lower bound。

这一点对组合式设计很关键，因为它使“合并需求”这件事在 timed setting 下也有了严格语义。

### 8. 定义 optimistic composition，并引入 cooperative pruning

composition 是另一块关键内容。它延续 interface automata 的乐观语义：

1. 两个接口可以组合，
2. 只要存在某个环境让它们安全交互。

但 timed 场景里最麻烦的就是 pruning。论文明确指出：

1. adversarial pruning 不分配到 composition 上。
2. 因而不能像旧直觉那样，每次组合完马上做 adversarial pruning 就万事大吉。

为解决这一点，作者提出 cooperative pruning，用来描述“在组件协作场景下，哪些状态仍值得保留”。这也是这篇长文相对早期会议版最重要的理论修补之一。

最后，论文证明：

1. composition 是结合的。
2. refinement 是 composition 的 precongruence。

这保证了组合式推理能稳定进行。

### 9. 定义 quotient，使其真正成为 composition 的对偶

论文后半段最重的部分就是 quotient。直觉上，若我们知道整体规格 `T` 和现有部件 `S`，则 `T \\ S` 应该给出“剩下那部分部件应满足什么规格”。

作者强调 quotient 应满足的核心性质是：

$$
S \parallel X \le T \iff X \le T \setminus\!\setminus S
$$

这才是真正的“composition 的对偶”。

而这一步恰恰是旧版本理论最容易出错的地方：定义稍有不慎，就会破坏 duality、alphabet 条件或 error handling。本文花了大量篇幅修正 quotient 的细节，并给出完整证明。

### 10. 给出完整工具落地：`ECDAR`

最后，文章明确把理论对接到 `ECDAR`：

1. consistency checking
2. refinement
3. conjunction
4. composition
5. quotient

这些都被纳入了新的开源实现路线。这一点很重要，因为这篇论文不只是“理论补完”，而是“理论补完 + 工具主线收束”。

## 解决了什么问题

这篇论文解决的是一个结构性问题：以前 timed specification theory 的很多零件都有了，但拼不成一台完整机器；本文把它们装配成了一整套。

### 1. 它真正补齐了 complete specification theory

不是只有 refinement，也不是只有 composition，而是把 specification theory 需要的全套 operator 都补齐，并且证明它们相互匹配。

### 2. 它澄清了 implementation 的语义

output urgency 与 independent progress 的引入，让 implementation 不再只是“更具体一点的规格”，而是确实代表可执行的系统对象。

### 3. 它修正了 pruning 和 quotient 上的老问题

这些修正不是小打小闹，而是决定理论是否自洽的关键。特别是 adversarial/cooperative pruning 的区分，直接关系到 composition 的正确理解。

## 与 UPPAAL 技术线的关系

这篇文章标志着 `UPPAAL` 生态中 `ECDAR/TIOA` 那条 specification theory 支线彻底成熟。

它和整体时间线的关系大致是：

1. 早期 `UPPAAL` 主线解决单系统 timed verification。
2. 2010 年前后逐渐出现 timed I/O / Ecdar 支线，关注组件规约与接口组合。
3. 本文把该支线正式收束成完整理论。

因此它的重要性和 `timed automata` 奠基文献不同，但在“组件化形式化方法”这个维度上同样是底座级条目。

## 实现与材料

- 内容详细程度：`🟢 复现级`。这是长篇完整论文，定义、例子、定理、附录证明、工具实现关系都很全。
- 实现可获取程度：`🟢 论文对应实现源码直达`。论文明确对接开源 `ECDAR` 工具链，后续做实现核验有直接入口。
- 关键材料线索：
  - [ECDAR](https://github.com/Ecdar/ECDAR)
  - [Reveaal](https://github.com/Ecdar/Reveaal)
  - [j-Ecdar](https://github.com/Ecdar/j-Ecdar)
- 复现注意点：
  - 这篇论文比会议短文版有多处定义修正。
  - 做 quotient / pruning 相关工作时，必须以后期长文定义为准。

## 对本研究的启发

这篇论文对当前博士研究的启发非常直接。

1. **复杂系统验证不能只盯整机模型**
   - 还要把接口责任、环境输入、组件替换关系显式建模。
2. **“实现”必须有可执行语义**
   - 不能只说“更具体一点”，而要像本文这样用 progress/urgency 约束把实现对象钉牢。
3. **组合式 operator 必须成体系**
   - refinement、conjunction、composition、quotient 如果各自零散定义，闭环式设计很难成立。
4. **理论修补要和工具实现同步**
   - 本文最值得学的不只是定理，而是它把修正过的定义真正对到开源实现里。

如果你后续要把状态机建模、验证画像和局部修复做成“可分组件逐步设计”的体系，这篇论文是最值得反复参考的条目之一。
