# Unification & Sharing in Timed Automata Verification

- 问题一句话：`UPPAAL` 的 symbolic reachability 已经能跑，但 `waiting/passed` 双结构和整状态重复存储仍然浪费大量时间与内存。
- 方法一句话：论文把 `passed` 和 `waiting` 合并成统一列表，并对 `location vector / variable vector / zone` 三类子结构做共享存储。
- 解决点一句话：它用很少的结构改动，显著减少无谓 waiting states 与重复数据，在实验中拿到了最高约 `60%` 提速和 `80%` 内存节省。

## 论文定位

这篇论文在 `uppaal_tech/` 中最适合归为 `🛠️ 工程/工具链`，但它又非常贴近 `🧱 数据结构`，因为它改造的不是表层界面，而是 reachability 引擎最核心的状态空间数据结构。

它与 [behrmann02-new-uppaal-architecture](../behrmann02-new-uppaal-architecture/) 和 [behrmann02-uppaal-implementation-secrets](../behrmann02-uppaal-implementation-secrets/) 的关系非常直接：

1. 新架构论文已经提出 `PWList` 与 shared storage 的思路；
2. implementation secrets 里已经把它们列为关键优化；
3. 这篇则把“统一 + 共享”单独抽出来，聚焦讲清楚对象、插入规则和实验收益。

所以它的定位很明确：这是 `UPPAAL` 新架构落地后，对一项关键内核优化的专题展开。

## 立足问题

这篇论文面对的问题相当具体，而且非常有工程价值。

在 timed automata 的 symbolic reachability 中，一个符号状态通常写成：

$$
(l, \nu, Z)
$$

其中：

1. $l$ 是 location vector；
2. $\nu$ 是 bounded integer variables；
3. $Z$ 是 zone。

经典实现里通常要维护两类集合：

1. `waiting`
   - 尚未展开的 symbolic states；
2. `passed`
   - 已经展开过的 symbolic states。

问题在于，这个经典做法在实践里会产生两种浪费。

第一种浪费是 **等待区里堆着很多早就没有意义的状态**。  
如果某个新状态已经被一个更大的状态覆盖，它仍可能先被放进 `waiting`，直到将来被弹出来时才意识到自己没必要展开。

第二种浪费是 **状态对象本身有大量重复子结构**。  
真实 reachable state-space 里，经常很多状态共享：

1. 相同的 location vectors；
2. 相同的 variable vectors；
3. 甚至相同的 zones。

如果每次都整状态拷贝，就会在内存中制造大量重复对象。

因此论文要解决的不是抽象的“性能不够好”，而是这两个非常直接的内核问题：

1. 插入状态时，能不能更早地去掉注定无用的 waiting states。
2. 存储状态时，能不能避免反复拷贝相同部件。

## 核心方法

这篇论文的方法其实很干净，主线就两条：

1. **uniﬁcation**
2. **sharing**

### 1. 先把覆盖关系当作插入规则的核心

作者先重新强调 symbolic states 的包含关系。对于同一离散部分下的两个符号状态，

$$
(l, \nu, Z) \subseteq (l, \nu, Z') \iff Z \subseteq Z'
$$

也就是说，若离散控制位置与离散变量相同，真正决定谁覆盖谁的是 zone inclusion。

基于这个关系，论文明确提出三条操作原则：

1. 新状态 `s` 若被已有状态覆盖，则不必加入。
2. 新状态 `s` 若加入成功，则它覆盖的旧状态应被移除。
3. 判重不该只看 identical states，而要看 covering states。

这一步非常关键，因为它把状态空间管理从“精确相等去重”升级成“语义覆盖管理”。

### 2. 把 `passed` 与 `waiting` 合并成 unified list

接下来论文的第一项核心改动，就是把两张表改成一张 unified list。

传统方案的问题在于：

1. 插入时要分别看 `waiting` 和 `passed`；
2. 被覆盖的 waiting states 可能长期滞留；
3. 同一状态往往在两处都被维护。

新的 unified list 规则是：

1. 插入状态时，先跟现有状态比较覆盖关系；
2. 若新状态被覆盖，则直接丢弃；
3. 若新状态不被覆盖，则删去所有被它覆盖的旧状态；
4. 再把新状态加入统一结构；
5. 结构内部仍记录“是否已展开”，但不再需要显式复制出一份 `passed` 和一份 `waiting`。

实现上，论文给出的结构非常清楚：

1. 一个 hash table 按离散部分定位；
2. 同一离散部分下维护一条 zones 的 linked list，也就是 zone union；
3. 另有一个 waiting queue，但队列里只存对 state entry 的引用。

这实际上等于把“状态是否待展开”从**状态存储本体**里剥离出来，变成一种元信息。

### 3. 用离散部分做主键，把连续部分做成 zone union

论文中 unified list 的另一个关键点，是把离散部分作为 hash key：

1. location vector
2. variable vector

这样做的好处是：

1. inclusion check 不需要全局乱找；
2. 只需先定位到同一离散部分下的候选列表；
3. 再在这些 zones 上检查覆盖关系。

换句话说，结构被设计成：

$$
\text{discrete part} \rightarrow \text{zone union}
$$

这比把整状态扔进统一哈希表更符合 timed symbolic search 的本质，因为 inclusion 只在离散部分相同的状态之间有意义。

### 4. 再对状态子结构做 sharing

仅仅统一列表还只解决“队列里少放废状态”的问题，并不能降低单状态内存开销。因此论文又叠加第二个正交优化：对子结构共享。

共享对象包括：

1. location vectors；
2. variable vectors；
3. zones。

实现上就是再维护若干 hash tables，把这些对象单独 intern 化。于是 unified list 中的状态项不再内嵌整个对象，而是只保留对共享对象的 key / reference。

这一点本质上就是把 symbolic state 拆成了可共享的结构化组件，而不是把它看成一个不可分割的胖对象。

### 5. 让 unified list 和 sharing 互相配合

这篇论文很重要的一点在于，作者明确说明 unified list 与 sharing 是**正交**的：

1. unified list 主要减少无谓 waiting states、减少查找与覆盖维护成本；
2. sharing 主要减少 location/variable/zone 的重复存储成本。

二者叠加后，收益并不冲突，反而相互增强：

1. unified list 让需要存下来的状态更少；
2. sharing 让剩下的状态也更便宜。

这就是为什么实验里 memory saving 非常明显。

## 解决了什么问题

这篇论文解决的问题看起来“只是数据结构改造”，但实际影响非常大。

### 1. 它显著减少了无谓 waiting states

统一之后，状态一旦插入就立刻参与全局覆盖判断，被已有状态覆盖的候选不会在等待区里长期滞留。

### 2. 它显著减少了重复对象

location vector、variable vector、zone 这些对象在大模型里重复率很高。论文给出的统计已经显示，某些例子中唯一对象比例很低，这正说明共享空间很大。

### 3. 它在真实模型上拿到了非常可观的收益

论文实验结论很直接：

1. 最高约 `60%` speedup；
2. 最高约 `80%` memory saving；
3. 大模型收益最明显，例如 `Plant` 一类模型从原先会爆内存的边缘状态被大幅压缩。

这说明这不是“对小 benchmark 有点帮助”的局部 tweak，而是确实能改变模型能不能跑下来的那种优化。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线里可以看作早期新架构的一次关键落地。

### 它接在谁之后

它直接接在：

1. [behrmann02-new-uppaal-architecture](../behrmann02-new-uppaal-architecture/)
   - 提出了 `PWList` 与共享式状态表示的总体方向。
2. [behrmann02-uppaal-implementation-secrets](../behrmann02-uppaal-implementation-secrets/)
   - 把 `PWL` 与 `State` 作为重要优化项列入总账。

### 它往后影响了谁

它往后影响：

1. [behrmann06-uppaal-4](../behrmann06-uppaal-4/)
   - 新一代版本中的整体引擎实现。
2. 后续 testing / `SMC` / `ECDAR` 等所有复用核心 symbolic engine 的分支
   - 因为它们都受益于统一后的状态空间存储基础设施。

### 它更靠近哪条主线

它最靠近：

1. symbolic state-space representation；
2. `PWList`；
3. shared storage；
4. `UPPAAL` 内核性能工程。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 原因是它把对象、数据结构、插入规则和实验结果都讲得很清楚，已经能较直接指导复现 unified list / sharing 的核心思路。
2. **实现可获取程度**
   - 适合评为 `🟨 部分实现源码可得`。
   - 论文明确说实验基于 `UPPAAL` development version `3.3.24`，但这一特定历史快照未必完整可得；不过相关思想显然进入了后续公开工具代码与生态。
3. **材料质量**
   - `paper_content.txt` 足够支撑方法级重建。
   - 若后续要补得更细，可以继续联读新架构论文与 `implementation secrets` 中对应章节。

## 对本研究的启发

这篇论文对当前博士研究很有启发，因为它证明了一件常被忽略的事：**闭环系统的可扩展性，往往不是先死在大算法上，而是先死在中间状态管理上。**

可直接借鉴的点包括：

1. 对 `LLM` 驱动的生成-验证-修复闭环，也应尽量把“是否待处理”和“对象本体存储”分离开。
2. 若中间对象可拆成多个子结构，就应优先考虑共享存储，而不是整对象重复复制。
3. 去重规则最好用“语义覆盖”而不是“字节级相等”，否则很难真正压缩状态空间。
4. 小而精准的数据结构改造，可能比引入一个新分析大模块更能决定平台能否扩起来。
