# 自底向上的数据树自动机 / Bottom-up automata on data trees and vertical XPath

## 基本信息

- 标题：Bottom-up automata on data trees and vertical XPath
- 中文标题：数据树上的自底向上自动机与垂直 XPath
- 作者：Diego Figueira, Luc Segoufin
- 发表：*28th International Symposium on Theoretical Aspects of Computer Science (STACS 2011)*, LIPIcs 9:93-104, 2011
- DOI：`10.4230/LIPIcs.STACS.2011.93`
- 链接：https://doi.org/10.4230/LIPIcs.STACS.2011.93
- 形式主义：`Bottom-Up Data Automata (BUDA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 逻辑-自动机桥接
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `A=(A,B,Q,q_0,\delta_\epsilon,\delta_{up},S,h)`、thread configuration `C\subseteq Q\times D`、semigroup path test 与到 `WSTS` 的 emptiness proof。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 unranked data tree、internal labeling、vertical `regXPath` 与 bottom-up run semantics。

## 简报

这篇论文的关键价值，是把 data-tree family 里一条此前比较散的路线稳定命名成 `BUDA`。它不是普通 unranked tree automata 的小修补，而是一个真正能挂到演化树上的模型节点：自底向上、交替、单寄存器，而且允许沿正则路径检查“子树里是否存在与当前寄存器 datum 相同或不同的后代值”。靠这个组合，它精确抓住了 vertical `XPath`，同时又保住 emptiness decidability。

- 形式主义定位：`Tree Automata` 主干下的 `Data / Infinite-Alphabet Tree` 分支，可视为“树对象上的 one-register alternating bottom-up family”。
- 构造方式简述：每个线程由一个状态和一个寄存器 datum 组成；自动机在节点上先做 `\epsilon`-tests 和线程分裂，再把各子树线程自底向上合并到父节点。
- 基础设施与场景简述：原文纯理论，但给出与 vertical `regXPath(V,=)` 的双向桥接，并用 `WSTS` 证明 emptiness decidable。

```text
data tree -> bottom-up alternating threads + one register -> vertical path/data tests -> WSTS emptiness / XPath satisfiability
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是有限、有序、非定阶的 data tree。每个节点既有有限标签，也有来自无限域的 datum。与 data word 不同，这里核心对象是树，因此模型天然支持 parent/child/ancestor/descendant 方向，但不打算覆盖 sibling 上的复杂水平约束。

### 核心抽象

原文把 `BUDA` 写成：

$$
A=(A,B,Q,q_0,\delta_\epsilon,\delta_{up},S,h)
$$

上式中的符号逐项解释如下：

1. `A` 是输入树的有限标签字母表。
2. `B` 是自动机内部猜测的有限辅助标签字母表。
3. `Q` 是有限状态集。
4. `q_0` 是初始状态。
5. `\delta_\epsilon` 是节点内的局部 `\epsilon`-transition 函数。
6. `\delta_{up}` 是把线程从子节点向父节点推进的 `up`-transition 函数。
7. `S` 是有限半群，用来编码正则路径性质。
8. `h:(A\times B)^+\to S` 是把节点路径映到半群元素的同态。

一个运行配置是线程集合：

$$
C\subseteq Q\times D
$$

上式中的符号逐项解释如下：

1. 每个线程是一个二元组 `(q,d)`。
2. `q` 是线程状态。
3. `d` 是该线程寄存器中当前保存的 datum。

`BUDA` 最有辨识度的地方，是 `\delta_\epsilon` 里的原子动作和测试。原文允许的典型原子包括：

$$
p,\ \mathrm{guess}(p),\ \mathrm{univ}(p),\ \mathrm{store}(p),\ eq,\ \overline{eq},\ \langle\mu\rangle^{=},\ \langle\mu\rangle^{\neq}
$$

上式中的符号逐项解释如下：

1. `p` 表示进入新状态 `p` 并保留寄存器 datum。
2. `\mathrm{store}(p)` 表示把当前节点 datum 写入寄存器后进入 `p`。
3. `\mathrm{guess}(p)` 表示任意猜一个 datum 进寄存器后进入 `p`。
4. `\mathrm{univ}(p)` 表示对子树中每个 datum 都生成一个处于状态 `p` 的线程。
5. `eq` / `\overline{eq}` 分别测试“当前节点 datum 是否等于寄存器 datum”。
6. `\langle\mu\rangle^{=}` / `\langle\mu\rangle^{\neq}` 测试“是否存在一条满足半群值 `\mu` 的向下路径，其终点 datum 与寄存器 datum 相等 / 不等”。

### 一个最小例子与通俗解释

一个很直观的例子是：判断“当前节点的 datum 是否在某个后代 `b` 节点上再次出现”。`BUDA` 可以这样做：

1. 在当前节点执行 `store(p)`，把当前 datum 记进寄存器。
2. 再在状态 `p` 上测试某个对应 `↓^*[b]` 的路径条件 `\langle \mu_b\rangle^{=}`。
3. 如果测试成功，就说明当前 datum 在某个 `b`-后代中重现。

通俗地说，`BUDA` 像“自底向上汇总子树证据的树自动机，但每条线程手里还拿着一张 datum 便签”。它不是在整棵树上自由乱跳，而是在 bottom-up 汇总过程中，把与 datum 相关的局部义务一层层带到父节点。

### 运行 / 接受 / 转移语义

设 `t=a\otimes b\otimes d` 是带输入标签、内部标签和 datum 的树。`BUDA` 的 run 是函数 `\rho`，给每个节点 `x` 分配一个配置 `\rho(x)`。

叶子处的初始配置满足：

$$
\rho(x)=\{(q_0,d(x))\}
$$

上式中的符号逐项解释如下：

1. 每个叶子先产生一条线程。
2. 该线程初始状态是 `q_0`。
3. 该线程初始寄存器 datum 就是该叶子的 datum。

若 `x` 是内部节点，子节点是 `x\cdot 1,\ldots,x\cdot n`，则原文要求各子树先做 `\epsilon`-closure 和 `up`-transition，再把它们并起来：

$$
\rho(x)=\bigcup_{i\in[n]} C_i'
$$

上式中的符号逐项解释如下：

1. 每个 `C_i'` 是第 `i` 个孩子子树在向上推进后的线程集合。
2. 并集表示所有子树线程在父节点处汇合。
3. 因为模型是 alternating 的，线程集合本身就承载并行义务。

整棵树接受，当且仅当根节点的 `\epsilon`-closure 里能到达空配置：

$$
\emptyset
$$

这表示所有线程义务都被满足并消解掉。

### 语义边界

这个 family 的设计边界非常清晰：

1. 它强调 bottom-up。
2. 它强调 vertical navigation。
3. 它强调 datum equality，而不是 datum order。
4. 它不支持 sibling 方向上的任意水平性质。

原文还明确指出，这个模型**不对补集闭包**，因为 `guess` 和 `univ` 不是对偶操作；如果把它们的对偶也加进来，会直接把模型推向不可判定。

### 关键性质与判定边界

原文最重要的结果可压成：

$$
\forall \eta\in \mathrm{regXPath}(V,=),\ \exists A\in \mathrm{BUDA}\ \text{such that}\ t\in L(A)\iff \llbracket \eta \rrbracket_t\neq\emptyset
$$

$$
\mathrm{emptiness}(\mathrm{BUDA})\ \text{decidable}
$$

$$
(\wp_{<\infty}(AC),\Rightarrow)\ \text{is }N\text{-downward compatible, where }N=2(|S||Q|)^2+1
$$

上面几式中的符号逐项解释如下：

1. 第一式表示 `BUDA` 至少足够强，能覆盖 vertical `XPath`。
2. 第二式表示它虽然树上带 data，又有 alternation，但 emptiness 仍可判定。
3. `AC` 是抽象配置集合。
4. `\wp_{<\infty}(AC)` 是有限抽象配置集的集合。
5. `\Rightarrow` 是 `WSTS` 上的抽象迁移。
6. 第三式是判定性的核心技术支点。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保留有限状态树自动机骨架。 |
| 事件 / 触发 | 强支持 | 在树节点处触发局部测试与向上合并。 |
| 守卫 / 数据 | 强支持 | 单寄存器 + descendant-path datum equality 是核心。 |
| 层次 | 强支持 | 对象天然是树。 |
| 并发 / 同步 | 强支持 | alternating thread-set 语义表达并行义务。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树模型。 |
| 可执行 / 可验证性 | 强理论支持 | emptiness 可判定，并可承载 vertical XPath satisfiability。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(A,B,Q,q_0,\delta_\epsilon,\delta_{up},S,h)$` | `BUDA` 的标准骨架。 |
| 线程配置 | `$C\subseteq Q\times D$` | 每条线程既有状态也有寄存器 datum。 |
| descendant-path test | `$\langle\mu\rangle^{=},\langle\mu\rangle^{\neq}$` | 把正则路径和 data test 绑到一起。 |
| 逻辑桥接 | `$\eta\in\mathrm{regXPath}(V,=)\Rightarrow \exists A\in\mathrm{BUDA}$` | 捕获 vertical XPath。 |
| 判定技术 | `$\wp_{<\infty}(AC)$` 上的 `WSTS` | emptiness decidable 的核心抽象。 |

## 构造方式与承载格式

### 建模入口

1. 先确认对象真的是 data tree，而不是 data word。
2. 再确认需求主要发生在 ancestor/descendant 这类 vertical 方向，而不是 sibling 横向关系。
3. 把树上需要检查的数据路径模式压成 semigroup 路径性质。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `A\times D` 标注的数据树；
2. 内部辅助标签树 `B`；
3. `BUDA` 元组；
4. 抽象配置与 `WSTS`。

原文没有 XML schema、JSON 或专门 DSL 级别的机读标准。

### 交换与互操作

它和 vertical `regXPath(V,=)` 的互操作最强，因为模型正是为这条逻辑路线提供 automata basis；与一般 unranked tree automata 的关系，则体现在“保留 tree skeleton，但额外给了一个寄存器和路径-data tests”。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 semigroup path tests、thread configurations 与 `WSTS` 抽象。
- 仿真/执行支持：可按 node-wise bottom-up thread-set semantics 解释。
- 验证/分析支持：vertical `XPath` 翻译、`WSTS` emptiness、normal-form reduction。
- 代码生成/转换支持：原文不讨论工程代码生成。
- 标准化或社区生态：是 data-tree / XPath decidability 交叉地带的经典理论节点。

## 适用场景与需求前提

### 适用场景

适合以下类型的树对象需求：

1. XML / 半结构化文档上的 vertical data constraints。
2. 只关心 ancestor/descendant，而不关心水平兄弟次序的 data-tree 性质。
3. 需要在树节点上比较“某个 datum 是否在满足特定路径性质的后代中再次出现”。

### 需求前提

1. 输入对象必须天然是树。
2. 数据关系主要是 datum equality。
3. 路径约束最好能压成 downward regular property。
4. 横向 sibling 约束不是核心。

### 不适用或高成本场景

若需求需要 full XPath、复杂 sibling counting、datum order 或补集闭包，这个 family 就不够，应转向别的 data-tree 模型。

## 与相邻形式主义的关系

相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它不是 top-down `guess/spread` 样式，而是 bottom-up tree family；相对 [regular-tree-languages-over-non-ranked-alphabets/desc.md](../regular-tree-languages-over-non-ranked-alphabets/desc.md)，它把数据值和单寄存器带进了 unranked tree skeleton；相对 [an-automata-model-for-trees-with-ordered-data-values/desc.md](../an-automata-model-for-trees-with-ordered-data-values/desc.md)，它只处理 equality、偏 vertical `XPath`，而后者进一步把 datum order 纳入模型。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata` 主干正式补出一条 `Data / Infinite-Alphabet Tree` 子枝，使演化树不再只在 word 上讨论 infinite alphabet。

### 作为目标形式主义还是中间表示

更适合作为理论节点或文献谱系骨架，而不是控制系统最终输出的工程建模语言。

### 对需求到模型生成的启发

当需求文本天然描述“树状对象 + 祖先/后代方向 + datum equality”时，LLM 不应误落到 word 自动机或纯 XML schema，而应识别为 data-tree automata 家族问题。

### 现实限制

没有成熟工程标准和运行时；其价值主要在树模型本体、逻辑桥接和 decidability boundary。

## 重要的相关工作

### 奠基或前身工作

- [regular-tree-languages-over-non-ranked-alphabets/desc.md](../regular-tree-languages-over-non-ranked-alphabets/desc.md)
- [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)

### 同类型或同家族工作

- [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)
- [hedge-automata-a-formal-model-for-xml-schemata/desc.md](../hedge-automata-a-formal-model-for-xml-schemata/desc.md)
- [an-automata-model-for-trees-with-ordered-data-values/desc.md](../an-automata-model-for-trees-with-ordered-data-values/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具。

### 与本研究关系最紧的工作

- 它最适合补到 `Tree Automata -> Data / Infinite-Alphabet Tree` 主枝，作为 equality-only、vertical-navigation-oriented 的经典节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Bottom-Up Data Automata (BUDA)`
- 论文角色：模型提出 / 逻辑-自动机桥接
- 核心功能：在 unranked data trees 上用 bottom-up one-register alternating 语义表达 vertical data-tree properties，并捕获 vertical XPath。
- 关键特性：bottom-up、single register、semigroup path tests、alternation、`WSTS` emptiness。
- 构造方式：`A=(A,B,Q,q_0,\delta_\epsilon,\delta_{up},S,h)` + thread-set configurations + bottom-up run semantics。
- 基础设施：纯理论模型，无工程标准/工具；核心分析设施是 `WSTS` 和 logic-to-automata translation。
- 适用场景：vertical data-tree constraints、XML-like document reasoning、ancestor/descendant equality patterns。
- 需求前提：对象必须是树，数据关系以 equality 为主，且横向 sibling 性质不是核心。
- 状态：🟢
