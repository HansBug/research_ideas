# 双向无限词的可识别集合 / Ensembles Reconnaissables de Mots Biinfinis

## 基本信息

- 标题：Ensembles Reconnaissables de Mots Biinfinis
- 中文标题：双向无限词的可识别集合
- 作者：Maurice Nivat, Dominique Perrin
- 发表：*Canadian Journal of Mathematics*, 38(3):513-537, 1986
- DOI：`10.4153/CJM-1986-025-6`
- 链接：https://doi.org/10.4153/CJM-1986-025-6
- 形式主义：`Bi-Infinite Word Automata / Biautomata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 bi-infinite words、biautomata 与 bilateral envelope。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是左右两侧 deterministic automata、连接关系 `\Lambda` 和双向无限词上的识别语义。

## 简报

这篇论文把 `Büchi / McNaughton` 的 one-sided `\omega`-word 理论推广到了 `\mathbb Z` 上索引的 bi-infinite words。它引入的关键对象不是普通 `\omega`-automaton，而是把“左侧无限过去”和“右侧无限未来”分开处理、再通过接口关系连接起来的 `biautomate / automate bilatère`。对当前文库来说，它正好补出 `Infinite-Object Automata / \omega-Automata` 下长期缺失的 `Bi-Infinite Word Automata` 节点。

- 形式主义定位：`\omega`-word 主干向双向无限词扩展的经典分支。
- 构造方式简述：用一个处理左上下文的 deterministic automaton、一个处理右上下文的 deterministic automaton，再用联接关系 `\Lambda` 组成 biautomaton。
- 基础设施与场景简述：原文是纯理论工作，但给出了双向无限词、bilateral envelope、deterministic biautomata 与 Boolean closure 这组非常稳定的谱系骨架。

```text
one-sided infinite words -> bi-infinite words indexed by Z -> biautomata / bilateral automata -> Boolean closure of deterministic classes
```

## 形式主义定义与核心对象

### 定义对象

论文把 bi-infinite word 定义成从整数集 `\mathbb Z` 到字母表 `A` 的映射，也就是：

$$
w : \mathbb Z \to A
$$

它和 ordinary `\omega`-word 的区别在于：读头既有“无限未来”，也有“无限过去”。

### 核心抽象

原文为此引入 `biautomate`。其核心骨架可写成：

$$
\mathcal B = (\mathcal A_-, \mathcal A_+, \Lambda)
$$

其中：

$$
\mathcal A_- = (Q_-, I_-, T_-), \qquad \mathcal A_+ = (Q_+, I_+, T_+)
$$

上式中的符号逐项解释如下：

1. `\mathcal A_-` 是处理左侧无限部分的 deterministic automaton。
2. `\mathcal A_+` 是处理右侧无限部分的 deterministic automaton。
3. `Q_-`、`Q_+` 分别是左右自动机的状态集。
4. `I_-`、`I_+` 是左右自动机的初始状态家族。
5. `T_-`、`T_+` 是左右自动机的终止 / 接受状态家族。
6. `\Lambda \subseteq I_- \times I_+` 是把左右两半拼接成同一个 bi-infinite word 的联接关系。

若 `w=[u,v]` 表示由左无限词 `u` 和右无限词 `v` 拼成的 bi-infinite word，则原文的 bi-infinite behavior 可压成：

$$
w \in |\mathcal B|_{\mathbb Z}
\iff
\exists (i_-,i_+) \in \Lambda,\ 
u \in |(Q_-,i_-,T_-)|^{\mathbb N},\
v \in |(Q_+,i_+,T_+)|^{\mathbb N}
$$

### 一个最小例子与通俗解释

原文给出的典型例子是形如 `{}^\omega a\, b^\omega` 的界面词及其所有平移。直观上，这类 bi-infinite word 在某个位置左边最终全是 `a`，右边最终全是 `b`。一个 biautomaton 可以让左自动机检查“往左看时一直像 `a^*`”，右自动机检查“往右看时一直像 `b^*`”，然后由 `\Lambda` 把这两个检查在同一个切分点上对齐。

通俗地说，biautomaton 像两台背靠背的 deterministic automata：一台负责读“过去”，一台负责读“未来”，中间再有一个接口说明哪对左右状态可以合法拼成同一个双向无限词。

### 运行 / 接受 / 转移语义

论文第 3 节同时定义了“bilateral envelope”。若 `X \subseteq A^*` 是有限词语言，则其 bilateral envelope `\overline X` 收集那些可以由一串越来越长的双侧有限窗逼近出来的 bi-infinite words。

原文 Proposition 3.3 的核心结论可以压成：

$$
W \text{ is the bi-infinite behavior of a bilateral automaton }
\iff
W = \overline X \text{ for some recognizable } X \subseteq A^*
$$

这说明：bi-infinite recognition 仍然可以回到 finite-word recognizable sets，只是要通过 bilateral envelope 把“有限窗逼近”提升到 `\mathbb Z`-indexed 对象。

### 语义边界

相对 ordinary `\omega`-words，这个模型要处理的是“左右都无限延伸”的对象，因此语言必须天然对平移稳定。原文也明确指出，recognizable sets of bi-infinite words 按定义就是 translation-closed 的。

### 关键性质与判定边界

这篇论文最核心的结构结论是：

$$
\mathrm{Rec}(A^{\mathbb Z}) = [\mathrm{Det}(A^{\mathbb Z})]_B
$$

也就是说，所有可识别的 bi-infinite word 语言，恰好是 deterministic bi-infinite classes 的 Boolean closure。这正是 bi-infinite 版本的 `McNaughton` 型结论。

原文还给出：

$$
W \in \mathrm{Det}(A^{\mathbb Z})
\Rightarrow
W \in \mathrm{Rec}(A^{\mathbb Z})
$$

以及“recognizable simple sets” 的分解，这些都在证明上支撑了上面的主定理。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍然是有限状态骨架，只是拆成左右两侧 automata。 |
| 事件 / 触发 | 强支持 | 输入对象仍是离散符号序列。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般变量守卫。 |
| 层次 | 不支持 | 对象是双向线性序列，不是树。 |
| 并发 / 同步 | 部分支持 | 左右 automata 不是并发进程，但要通过 `\Lambda` 同步对齐。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 automata-theoretic 模型。 |
| 可执行 / 可验证性 | 强理论支持 | bilateral envelope、deterministic characterization 和 Boolean closure 都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| bi-infinite word | `$w:\mathbb Z\to A$` | 双向无限词的对象定义。 |
| biautomaton | `$\mathcal B=(\mathcal A_-,\mathcal A_+,\Lambda)$` | 左右两侧 deterministic automata 的连接骨架。 |
| bi-infinite behavior | `$w\in|\mathcal B|_{\mathbb Z}$` | 左右两半在 `\Lambda` 下可拼接时接受。 |
| bilateral envelope | `$W=\overline X$` | 从有限词语言提升到 bi-infinite language。 |
| 主定理 | `$\mathrm{Rec}(A^{\mathbb Z})=[\mathrm{Det}(A^{\mathbb Z})]_B$` | bi-infinite 版 McNaughton 定理。 |

## 构造方式与承载格式

### 建模入口

1. 先明确对象是否真的是 `\mathbb Z`-indexed bi-infinite word。
2. 分别为左侧和右侧构造 deterministic automata。
3. 用 `\Lambda` 说明哪些左右状态对可以在同一个切分点上匹配。
4. 必要时通过 bilateral envelope 把 finite-word recognizable sets 提升成双向无限语言。

### 机器可处理承载方式

机器可处理承载方式是左右 automata 加关系 `\Lambda`，而不是工程 DSL。

### 交换与互操作

它直接连接：

1. `Büchi / McNaughton` 的 one-sided `\omega`-word 理论。
2. recognizable finite-word languages。
3. later `biautomata`、双向逻辑和 symbolic dynamics 相关方向。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 biautomaton 和 bilateral envelope，而不是交换文件。
- 仿真/执行支持：可按左右两侧 deterministic automata 分别推进。
- 验证/分析支持：deterministic characterization、Boolean closure 和 translation-closure 是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `\omega`-automata 向双向无限词扩展的经典理论分支。

## 适用场景与需求前提

### 适用场景

适合表达“既依赖无限过去又依赖无限未来”的序列语言，如 bi-infinite symbolic sequences、shift-like behaviors 和双向轨迹语言。

### 需求前提

1. 对象必须天然是 `\mathbb Z`-indexed 而不是只向未来展开。
2. 语言应当对平移稳定。
3. 可以接受把左右语义拆成两台 deterministic automata 再做接口联接。

### 不适用或高成本场景

若对象只是 ordinary `\omega`-word 或有限 trace，这类 bilateral 语义就会显得过重。

## 与相邻形式主义的关系

相对 [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)，它把“infinite objects” 里的双向无限词分支做成了明确的独立理论节点；相对 `Büchi / McNaughton` 的 one-sided `\omega`-word 线，它把索引域从 `\mathbb N` 推广到 `\mathbb Z`；相对 [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)，这篇走的是双向线性对象，而不是分支树对象。

## 与本研究的关系

### 对 Project 1 的价值

它为 `Infinite-Object Automata / \omega-Automata` 主干补出了 `Bi-Infinite Word Automata` 这一经典而长期缺失的分支。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和语言类中间表示，不是控制系统需求建模的默认终点。

### 对需求到模型生成的启发

如果某类需求同时依赖“无限历史 + 无限未来”的对称结构，one-sided `\omega`-automata 可能不够，模型生成阶段应明确是否需要 bilateral semantics。

### 现实限制

没有工程化工具或标准格式；在控制系统主线里更多承担谱系地图作用。

## 重要的相关工作

### 奠基或前身工作

- `Büchi` 与 `McNaughton` 关于 one-sided infinite words 的经典工作。

### 同类型或同家族工作

- [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合挂成 `Infinite-Object Automata / \omega-Automata -> Bi-Infinite Word Automata` 的代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Bi-Infinite Word Automata / Biautomata`
- 论文角色：模型提出
- 核心功能：把 `\omega`-word 识别理论推广到 `\mathbb Z` 上的 bi-infinite words，并用 biautomata 给出 deterministic characterization。
- 关键特性：双向无限词、左右 deterministic automata、联接关系 `\Lambda`、bilateral envelope、Boolean closure of deterministic classes。
- 构造方式：`\mathcal B=(\mathcal A_-,\mathcal A_+,\Lambda)` + bilateral envelope。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：bi-infinite symbolic sequences、shift-like language classes 和双向轨迹语义。
- 需求前提：对象是 `\mathbb Z`-indexed bi-infinite words，且语言对平移稳定。
- 状态：🟢
