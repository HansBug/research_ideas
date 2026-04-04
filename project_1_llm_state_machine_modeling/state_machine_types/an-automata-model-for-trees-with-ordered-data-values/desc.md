# 有序数据值树自动机 / An Automata Model for Trees with Ordered Data Values

## 基本信息

- 标题：An Automata Model for Trees with Ordered Data Values
- 中文标题：有序数据值树自动机模型
- 作者：Tony Tan
- 发表：*2012 27th Annual IEEE Symposium on Logic in Computer Science (LICS 2012)*, 586-595, 2012
- DOI：`10.1109/LICS.2012.69`
- 链接：https://doi.org/10.1109/LICS.2012.69
- 形式主义：`Ordered-Data Tree Automata (ODTA / weak ODTA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 逻辑-自动机桥接
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `S=\langle T,M,\Gamma_0\rangle`、`Profile(t)`、按数据值排序的字符串表示 `V_\Gamma(t)` 与 emptiness decision procedure。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 ordered-data tree、profile tree、letter-to-letter transducer 与 string automaton。

## 简报

这篇论文把 data-tree family 从“只能测 datum equality”继续推到了“datum 还带线性顺序”的版本。它的关键收获，不是多给 tree automata 加一个比较符号，而是提出了一个很特别的组合骨架：先用 tree transducer 在结构层面标注节点，再把整棵树按 datum 从小到大压成一个 `2^\Gamma` 字符串，最后交给普通字符串自动机。这个架构就是 `ODTA`。它既把 ordered-data trees 稳定命名出来，又给出逻辑刻画和 emptiness decidability。

- 形式主义定位：`Tree Automata` 主干下 `Data / Infinite-Alphabet Tree` 子枝里进一步引入 datum order 的经典节点，可视为 equality-only data-tree family 的 ordered extension。
- 构造方式简述：`T` 先读取 `Profile(t)` 并输出标记树 `t'`；`M` 再读取按数据值升序形成的字符串 `V_\Gamma(t')`；最后由 `\Gamma_0` 统一施加“某些标签必须 pairwise data-distinct”的全局约束。
- 基础设施与场景简述：原文纯理论，但给出与 `FO^2(E_\downarrow,E_\rightarrow,\sim)` 加 `FO(\sim,\prec,\prec_{suc})` 组合逻辑的精确桥接；并进一步提出 `weak ODTA`，把 emptiness 复杂度从 `3`-`NEXPTIME` 降到 `NP`。

```text
ordered-data tree -> profile tree -> transducer output tree -> data-value string representation -> finite automaton + distinctness side condition
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 ordered-data tree。每个节点既有有限标签，也有一个来自线性有序无限域的 datum。除了树关系 `E_\downarrow`、`E_\rightarrow` 之外，模型还允许使用：

1. 数据相等关系 `\sim`；
2. 数据大小关系 `\prec`；
3. 数据后继关系 `\prec_{suc}`。

为了让 transducer 能看到局部相等信息，论文先定义节点 profile。对每个节点 `u`，其 profile 是三元组：

$$
(l,p,r)\in\{\top,\bot,*\}^3
$$

上式中的符号逐项解释如下：

1. `l` 表示它与左兄弟 datum 是否相等；若没有左兄弟则为 `*`。
2. `p` 表示它与父节点 datum 是否相等；若没有父节点则为 `*`。
3. `r` 表示它与右兄弟 datum 是否相等；若没有右兄弟则为 `*`。

于是整棵树被提升成 `Profile(t)`，其字母表是 `\Sigma\times\{\top,\bot,*\}^3`。

### 核心抽象

原文把 `ODTA` 定义为：

$$
S=\langle T,M,\Gamma_0\rangle
$$

上式中的符号逐项解释如下：

1. `T` 是从 `\Sigma\times\{\top,\bot,*\}^3` 到输出字母表 `\Gamma` 的 letter-to-letter tree transducer。
2. `M` 是一个在字母表 `2^\Gamma` 上运行的有限字符串自动机。
3. `\Gamma_0\subseteq\Gamma` 是一组需要满足 data-distinctness 的标签。

`ODTA` 最特别的地方，是它不直接在树上做最终接受，而是先构造“数据值字符串表示”。若 `d_1<\cdots<d_m` 是树中出现过的所有 datum，则定义：

$$
V_\Gamma(t)=S_1S_2\cdots S_m
$$

其中每个 `S_i\subseteq\Gamma` 表示“哪些输出标签在 datum `d_i` 上出现过”。

上式中的符号逐项解释如下：

1. `d_1<\cdots<d_m` 是按 datum 大小排序后的所有不同数据值。
2. `S_i` 收集所有落在 datum `d_i` 上的输出标签。
3. 因此，树上关于 datum order 的问题被转成了一个普通字符串上的顺序问题。

### 一个最小例子与通俗解释

一个最容易理解的例子是“所有 `a`-节点的数据值都互不相同”。`ODTA` 可以这样写：

1. `T` 把每个 `a`-节点标记成 `\alpha`，其余节点标记成 `\beta`。
2. `M` 对 `V_\Gamma(t')` 不施加复杂顺序条件，接受任意字符串。
3. 令 `\Gamma_0=\{\alpha\}`，于是接受条件自动要求所有 `\alpha`-节点 pairwise data-distinct。

通俗地说，`ODTA` 不是“在树上直接跑一个超级复杂的 data automaton”，而是先把树结构和数据顺序拆开处理：结构部分交给 transducer，顺序部分交给字符串自动机，全局 distinctness 再单独收束。

### 运行 / 接受 / 转移语义

设 `t` 是输入 ordered-data tree。`ODTA` 接受 `t`，当且仅当存在输出树 `t'` 满足：

$$
t\in L_{data}(S)
$$

当且仅当：

$$
\exists t'\ \Bigl(
T(\mathrm{Profile}(t))=t'
\land
V_\Gamma(t')\in L(M)
\land
\forall a\in\Gamma_0,\ \text{all }a\text{-nodes in }t' \text{ have different data values}
\Bigr)
$$

上式中的符号逐项解释如下：

1. `T(\mathrm{Profile}(t))=t'` 表示 `T` 在 profile tree 上输出标记树 `t'`。
2. `V_\Gamma(t')` 是按 datum 排序后的标签集合字符串。
3. `V_\Gamma(t')\in L(M)` 表示字符串自动机负责所有与 datum 顺序相关的 regular 条件。
4. 最后一项是 `\Gamma_0` 驱动的全局 distinctness side condition。

### 语义边界

这个模型的边界与 `BUDA` 很不同：

1. 它显式支持 datum order，而不只是 datum equality。
2. 它把“树结构”和“datum 顺序”拆成 transducer + string automaton 两段。
3. 它对 negation 不闭包。
4. 它还有一个更弱的 sibling-equality-free 版本 `weak ODTA`。

### 关键性质与判定边界

原文最关键的结论可压成：

$$
L\ \text{accepted by ODTA}\iff
\exists X_1\cdots\exists X_m\ \varphi\land\psi
$$

其中

$$
\varphi\in FO^2(E_\downarrow,E_\rightarrow,\sim),\qquad
\psi\in FO(\sim,\prec,\prec_{suc})
$$

并且：

$$
\mathrm{emptiness}(\mathrm{ODTA})\ \text{decidable in }3\text{-NEXPTIME}
$$

$$
\mathrm{emptiness}(\mathrm{weak\ ODTA})\in NP
$$

上面几式中的符号逐项解释如下：

1. 第一组公式是 `ODTA` 的核心逻辑刻画。
2. `\varphi` 负责树结构与局部 equality。
3. `\psi` 负责纯 datum-order 相关的约束。
4. `weak ODTA` 去掉了相邻节点 datum equality 测试，因此复杂度显著下降。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 结构层由 tree transducer 和 string automaton 共同承担。 |
| 事件 / 触发 | 强支持 | 可表达树结构、局部 profile 与 datum 顺序条件。 |
| 守卫 / 数据 | 强支持 | 同时支持 `=`、`<` 与 data-successor。 |
| 层次 | 强支持 | 对象天然是有序非定阶树。 |
| 并发 / 同步 | 不强调 | 重点不是 alternation，而是结构-顺序分解。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | `ODTA` emptiness decidable，`weak ODTA` 更便宜。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$S=\langle T,M,\Gamma_0\rangle$` | `ODTA` 的标准骨架。 |
| 数据值字符串 | `$V_\Gamma(t)=S_1\cdots S_m$` | 把 datum order 压到普通字符串上。 |
| 接受语义 | `$T(Profile(t))=t'$` and `$V_\Gamma(t')\in L(M)$` | 结构处理与顺序处理分层进行。 |
| 逻辑刻画 | `$\exists X_1\cdots\exists X_m\ \varphi\land\psi$` | 精确对应 tree + data-order 逻辑。 |
| 复杂度 | `$\mathrm{emptiness}(\mathrm{ODTA})$ decidable, `$\mathrm{weak\ ODTA}\in NP$` | ordered-data tree family 仍保持可判定。 |

## 构造方式与承载格式

### 建模入口

1. 先确认对象确实是树，且 datum 带线性顺序。
2. 再确认需求既有树结构部分，也有按 datum 排序后的全局顺序部分。
3. 用 `T` 解决结构标注，用 `M` 解决 datum-order regular condition，用 `\Gamma_0` 解决 distinctness。

### 机器可处理承载方式

机器可处理承载方式包括：

1. ordered-data tree；
2. `Profile(t)`；
3. `T` 输出树；
4. datum-order string `V_\Gamma(t)`；
5. string automaton `M`。

原文没有工程层面的 XML / JSON / DSL 标准。

### 交换与互操作

它与 `FO^2(E_\downarrow,E_\rightarrow,\sim)` 加 `FO(\sim,\prec,\prec_{suc})` 的互操作最直接；与 `weak ODTA` 的关系则提供了一条复杂度更低但功能更窄的 sibling-free 子线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 profile tree、data-value string representation 与 transducer/automaton 组合。
- 仿真/执行支持：可按 transducer 输出后再在字符串上运行 `M` 的两阶段语义解释。
- 验证/分析支持：逻辑刻画、emptiness decision procedure、`weak ODTA` 复杂度下降。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 ordered-data tree 理论中的关键母节点。

## 适用场景与需求前提

### 适用场景

适合以下类型问题：

1. 树结构对象上同时依赖 datum equality 和 datum order 的约束。
2. XML / 文档 / 结构化验证里需要比较“哪个 data value 更大、谁是下一个 data value”。
3. 希望把树结构逻辑和数据顺序逻辑拆开分析。

### 需求前提

1. 输入对象必须是树。
2. 数据域需具备线性顺序。
3. 需求能被分解成“结构局部条件 + 数据值全局顺序条件”。

### 不适用或高成本场景

若只需要 datum equality 且更关心 vertical `XPath`，`BUDA` 这类 equality-only 模型往往更直接；若还需要 full negation、加法或更强 order arithmetic，则 `ODTA` 也会失守。

## 与相邻形式主义的关系

相对 [bottom-up-automata-on-data-trees/desc.md](../bottom-up-automata-on-data-trees/desc.md)，它不走 one-register bottom-up + `WSTS` 路线，而是走 transducer + string-automaton 分解路线，并且显式支持 datum order；相对 [regular-tree-languages-over-non-ranked-alphabets/desc.md](../regular-tree-languages-over-non-ranked-alphabets/desc.md)，它把普通 unranked tree automata 继续推进到 ordered-data 场景；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它的重点已不再是 register alternation，而是 order-aware data-tree representation。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata` 主干上的 `Data / Infinite-Alphabet Tree` 支线继续推进到“ordered data”层次，是演化树上非常关键的补洞节点。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和复杂树需求的中间抽象，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

当需求文本里的数据关系不只是“相等/不等”，还出现“更早/更晚”“更大/更小”“下一个数据值”这类 order-style 条件时，LLM 应识别“这已经越过 equality-only data-tree family，进入 `ODTA` 一类 ordered-data 模型”。

### 现实限制

没有成熟工程标准和现成运行时；它的主要价值在 ordered-data tree family 的定义、逻辑刻画和判定边界。

## 重要的相关工作

### 奠基或前身工作

- [regular-tree-languages-over-non-ranked-alphabets/desc.md](../regular-tree-languages-over-non-ranked-alphabets/desc.md)
- [bottom-up-automata-on-data-trees/desc.md](../bottom-up-automata-on-data-trees/desc.md)

### 同类型或同家族工作

- [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)
- [hedge-automata-a-formal-model-for-xml-schemata/desc.md](../hedge-automata-a-formal-model-for-xml-schemata/desc.md)
- [deterministic-automata-on-unranked-trees/desc.md](../deterministic-automata-on-unranked-trees/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具。

### 与本研究关系最紧的工作

- 它最适合补到 `Tree Automata -> Data / Infinite-Alphabet Tree` 主枝中，作为 ordered-data 版本的经典节点；`weak ODTA` 则是该节点向可判定低复杂度子类收束的一条旁支。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Ordered-Data Tree Automata (ODTA / weak ODTA)`
- 论文角色：模型提出 / 逻辑-自动机桥接
- 核心功能：在 ordered-data trees 上把结构逻辑与 datum-order logic 分解到 transducer + string automaton 框架中，并保持 emptiness decidable。
- 关键特性：profile tree、datum-order string representation、`FO^2 + FO(\prec)` 刻画、`weak ODTA` 子类。
- 构造方式：`S=\langle T,M,\Gamma_0\rangle` + `Profile(t)` + `V_\Gamma(t)` + distinctness side condition。
- 基础设施：纯理论模型，无工程标准/工具；核心分析设施是 transducer decomposition 与 emptiness decision procedure。
- 适用场景：ordered-data trees、文档结构上的 equality/order 混合约束、树结构与数据顺序联合分析。
- 需求前提：对象必须是树，数据域具备线性顺序，需求可拆成结构局部条件与数据顺序条件。
- 状态：🟢
