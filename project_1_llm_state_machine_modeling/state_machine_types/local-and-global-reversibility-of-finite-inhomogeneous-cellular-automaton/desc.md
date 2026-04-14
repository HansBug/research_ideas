# 有限非均匀细胞自动机的局部与全局可逆性 / Local and global reversibility of finite inhomogeneous cellular automaton

## 基本信息

- 标题：Local and global reversibility of finite inhomogeneous cellular automaton
- 中文标题：有限非均匀细胞自动机的局部与全局可逆性
- 作者：Endre Katona
- 发表：*Acta Cybernetica*, 3(4):287-292, 1977
- DOI：原文未提供
- 链接：https://cyber.bibl.u-szeged.hu/index.php/actcybern/article/download/3154/3139
- 形式主义：`Finite Inhomogeneous Cellular Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🖼️ 网格 / 图案对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供软件实现；机器可处理入口是有限细胞集、非均匀邻域函数、局部映射族和由此诱导的全局映射。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `CA=(C,A,N,\Phi)` 元组、全局映射 `F` 与 ICT 逆构造表。

## 简报

这篇论文的重要性在于，它不是泛泛讨论 `CA` 动力学，而是把“有限、非均匀、任意拓扑”的 cellular automaton 明确定义出来，并把 reversibility 写成“是否存在一组新的局部函数，使全局映射正好成为原映射的逆”。对当前文库来说，这恰好把 `Cellular Automata` 主干从“大型同质格点系统”往更贴近 automata-theoretic family 的方向细化出 `Finite Inhomogeneous Cellular Automata` 节点。

- 形式主义定位：`Cellular Automata` 主干下的有限、非均匀、拓扑可变分支。
- 构造方式简述：显式给出有限细胞集、每个细胞自己的邻域、每个细胞自己的局部更新函数，再由这些局部函数拼出全局映射。
- 基础设施与场景简述：原文是纯理论工作，但给出了平衡局部映射、garden-of-eden 配置、ICT 逆构造表和一维二值情形的结构定理，足以让该节点独立挂树。

```text
有限细胞集 + 非均匀邻域 + 每格独立局部映射 -> 全局配置映射 F -> 局部/全局可逆性分析
```

## 形式主义定义与核心对象

### 定义对象

论文第 1 节把 inhomogeneous cellular automaton 明确定义为一个四元组，不再要求无限格点或全局同质局部规则。

### 核心抽象

原文定义可写成：

$$
\mathcal{A} = (C, A, N, \Phi)
$$

上式中的符号逐项解释如下：

1. `C=\{c_1,\ldots,c_m\}` 是有限细胞集合。
2. `A=\{0,1,\ldots,s-1\}` 是单元状态集合。
3. `N` 是邻域函数，为每个细胞指定其邻居元组。
4. `\Phi` 是局部函数系统，为每个细胞指定一个局部映射 `f_i`。

配置是一个映射：

$$
\alpha : C \to A
$$

全局映射 `F` 则由各局部映射拼成：

$$
F : \mathcal{S} \to \mathcal{S}
$$

并满足：

$$
F(\alpha)=\beta \iff \forall i,\ f_i(a_{i1},\ldots,a_{in_i})=\beta(c_i)
$$

上式中的符号逐项解释如下：

1. `\mathcal{S}` 是全部配置集合。
2. `(a_{i1},\ldots,a_{in_i})` 是配置 `\alpha` 在细胞 `c_i` 邻域上的状态元组。
3. `\beta(c_i)` 是更新后细胞 `c_i` 的状态。

### 一个最小例子与通俗解释

一个非常直观的可逆例子，是一维环形拓扑上的“左移”函数系统。设每个细胞只有 `0/1` 两种状态，并令每个细胞的新状态直接等于左邻居旧状态：

$$
F(\alpha)(c_i) = \alpha(c_{i-1})
$$

这样一步更新就是整条环形配置整体左移一格。它的逆映射显然是：

$$
F^{-1}(\alpha)(c_i) = \alpha(c_{i+1})
$$

也就是整体右移一格。

通俗地说，这类模型把普通同质 `CA` 里的“每个格子都执行同一条规则”放宽成“不同格子可以有不同邻域和不同规则”。而论文关心的是：这种局部差异会不会破坏全局可逆性，以及能否仅靠新的局部规则把整个系统倒过来。

### 运行 / 接受 / 转移语义

论文不是语言接受模型，而是配置演化模型。其核心语义是配置在全局映射 `F` 下的一步演化：

$$
\alpha \mapsto F(\alpha)
$$

论文采用的 reversibility 定义比“单纯双射”更强，可写成：

$$
\mathcal{A}=(C,A,N,\Phi)\ \text{is reversible} \iff \exists \Phi' \text{ such that } (C,A,N,\Phi') \text{ generates } F^{-1}
$$

上式中的符号逐项解释如下：

1. `\Phi'` 是新的局部函数系统。
2. `F^{-1}` 是原全局映射的逆映射。
3. 这意味着逆系统也必须保持“同一套细胞集与邻域函数 + 局部映射拼装”的形式。

### 语义边界

论文强调的不是一般 `CA` 双射，而是“强可逆性”：

1. 不仅要求 `F` 双射。
2. 还要求逆映射本身也能再次分解成同一邻域结构上的局部函数系统。

这让 `Finite Inhomogeneous Cellular Automata` 成为一个更像自动机 family 的节点，而不是泛泛的动力系统对象。

### 关键性质与判定边界

论文先引入 balanced local map。若某个局部映射 `f` 的各输出值对应的局部邻域数不均衡，则可推出全局会出现 garden-of-eden 配置。原文核心估计可压成：

$$
f \text{ is } q\text{-unbalanced} \Rightarrow \text{at least } q \cdot s^{m-n} \text{ garden-of-eden configurations}
$$

上式中的符号逐项解释如下：

1. `q` 衡量局部映射偏离 balanced 的程度。
2. `s` 是单元状态数。
3. `m` 是细胞数。
4. `n` 是相关细胞的邻域大小。

由此得到必要条件：

$$
F \text{ bijective } \Rightarrow \text{ all local maps are balanced}
$$

随后，论文给出 reversibility 的判定准则：每个细胞的 inverse-constructing table 必须满足“若 `t+1` 时刻的邻域状态相同，则 `t` 时刻该细胞的状态也必须相同”。

对一维二值环形 `CA`，论文最后得到非常强的结构结论：

$$
\text{reversible} \Rightarrow
\begin{cases}
\text{each cell belongs to an isolated section of at most three cells},\\
\text{or }\Phi\text{ is a shift function-system}
\end{cases}
$$

这说明在经典一维二值场景里，可逆的非均匀 `CA` 家族其实非常瘦。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个细胞取有限离散状态。 |
| 事件 / 触发 | 不适用 | 由同步离散步推进，而非事件触发。 |
| 守卫 / 数据 | 不支持 | 无一般变量守卫。 |
| 层次 | 不支持 | 不是层次状态图。 |
| 并发 / 同步 | 强支持 | 所有细胞同步更新。 |
| 时间约束 | 部分支持 | 只有离散时步，无显式时钟约束。 |
| 连续动态 / 随机性 | 不支持 | 纯离散确定性。 |
| 可执行 / 可验证性 | 强理论支持 | 平衡性、eden 配置和 reversibility 判定准则都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$\mathcal A=(C,A,N,\Phi)$` | 有限非均匀 `CA` 的本体。 |
| 全局映射 | `$F:\mathcal S \to \mathcal S$` | 由局部映射族诱导出的整体演化。 |
| 强可逆性 | `$\exists \Phi' \text{ s.t. } (C,A,N,\Phi') \text{ generates } F^{-1}$` | “逆映射也必须局部化”。 |
| 平衡必要条件 | `all local maps balanced` | 排除 garden-of-eden 的基本前提。 |
| 一维二值结构定理 | `isolated sections` or `shift function-system` | 说明该子类在经典情形下非常受限。 |

## 构造方式与承载格式

### 建模入口

建模时首先要确定：

1. 细胞集合 `C` 是否有限。
2. 每个细胞的邻域是否允许不同。
3. 每个细胞是否有独立的局部映射 `f_i`。

### 机器可处理承载方式

原文的机器可处理承载方式是细胞集、邻域函数、局部函数系统和 ICT 表，而不是某种统一交换文件。

### 交换与互操作

它最自然地互操作到：

1. classical `CA` 可逆性理论。
2. finite / inhomogeneous `CA` 建模。
3. reversible `CA` 与 shift-like 系统分析。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `CA` 元组和 inverse-constructing table。
- 仿真/执行支持：可直接按全局映射执行。
- 验证/分析支持：balanced local map、eden 配置计数和 reversibility criterion 是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `CA` 理论和 reversible `CA` 早期分支。

## 适用场景与需求前提

### 适用场景

适用于需要分析有限格点系统、拓扑非均匀局部更新、以及局部规则能否支撑全局可逆性的场景。

### 需求前提

1. 对象必须天然是格点 / 细胞结构。
2. 系统关注的是同步全局演化，而不是单个读头式识别。
3. 需要允许不同细胞拥有不同邻域或不同局部映射。

### 不适用或高成本场景

如果目标只是普通 homogeneous `CA`、字符串自动机或工程控制流程图，这个 family 会显得过专。

## 与相邻形式主义的关系

相对 [cellular-automata/desc.md](../cellular-automata/desc.md)，它把 `CA` 从无限、同质的常见叙述收紧为有限、非均匀、可逆性可判的 family；相对 [a-simple-construction-method-of-a-reversible-finite-automaton-out-of-fredkin-gates-and-its-related-problem/desc.md](../a-simple-construction-method-of-a-reversible-finite-automaton-out-of-fredkin-gates-and-its-related-problem/desc.md)，这篇讨论的是整体格点系统的局部 / 全局可逆性，而不是单个有限自动机单元；相对二维 tape automata，它的并行更新语义更接近动力系统而不是移动读头。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了 `Cellular Automata` 下的 `Finite / Inhomogeneous` 分支，使该主线不再只停留在同质格点系统总论。

### 作为目标形式主义还是中间表示

更适合作为谱系节点与理论参照，而不是控制系统需求建模的默认终态。

### 对需求到模型生成的启发

如果需求天然是“由许多局部单元同步更新”而且局部规则不完全一致，那么模型生成阶段可以明确区分 homogeneous 与 inhomogeneous `CA`，并进一步检查是否需要 reversibility。

### 现实限制

它没有工程标准和现成交换格式，且面向格点系统；对常规控制状态图需求并不直接友好。

## 重要的相关工作

### 奠基或前身工作

- [cellular-automata/desc.md](../cellular-automata/desc.md)
- reversible cellular automata / garden-of-eden 主线

### 同类型或同家族工作

- finite homogeneous cellular automata
- reversible cellular automata
- shift function systems

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合作为 `CA` 主干向“有限、非均匀、可逆”细化时的经典节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🖼️ 网格 / 图案对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Finite Inhomogeneous Cellular Automata`
- 论文角色：模型提出
- 核心功能：定义有限非均匀 `CA` 并给出局部/全局可逆性的必要条件、判定准则和一维二值结构定理。
- 关键特性：有限细胞集、异构邻域、局部函数系统、ICT、balanced local maps、强可逆性。
- 构造方式：`(C,A,N,\Phi)` 元组 + 全局映射 `F`。
- 基础设施：纯理论承载，无工程标准，但 reversibility 判据清晰。

