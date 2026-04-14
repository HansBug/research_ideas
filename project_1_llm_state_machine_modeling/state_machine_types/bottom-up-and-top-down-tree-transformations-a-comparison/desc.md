# 自底向上与自顶向下树变换的比较 / Bottom-up and Top-down Tree Transformations---a Comparison

## 基本信息

- 标题：Bottom-up and Top-down Tree Transformations---a Comparison
- 中文标题：自底向上与自顶向下树变换的比较
- 作者：Joost Engelfriet
- 发表：Mathematical Systems Theory, 9(2):198-231, 1975
- DOI：`10.1007/BF01704020`
- 链接：https://ris.utwente.nl/ws/files/6529681/Engelfriet75bottom.pdf
- 形式主义：Bottom-Up / Top-Down Tree Transducers / Generalized Finite State Transformations
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文只给出 ranked-tree rewrite 规则、有限状态与组合分解结果；无独立实现。
- 标准/格式获取方式：原文没有工程化标准，机器可处理入口是 ranked alphabet、状态集与 top-down / bottom-up / generalized `fst` 规则。

## 简报

这篇论文对当前文库的重要性，不只是“又有一篇树变换论文”，而是它把经典 `Tree Transducer` 主枝的两个母型稳定并列出来：`top-down` 和 `bottom-up`，并进一步给出同时覆盖两者的 `generalized fst`。对于演化树来说，它正好适合作为 `Tree Automata -> Tree Transducer` 下的早期主干节点。

- 形式主义定位：经典 rule-based tree transformation 母线，回答“树是先向下复制改写，还是先向上归并判断”。
- 构造方式简述：输入输出都用 ranked trees 表达，规则以有限状态和变量占位描述树到树的逐步改写。
- 基础设施与场景简述：原文完全是理论工作，但把 top-down、bottom-up 与 generalized 版本的表达差异、分解方式和闭包性质讲得很清楚。

```text
输入树 -> top-down / bottom-up finite-state rules -> 输出树
      \-> generalized fst -> 统一解释复制、删除、重标记与组合
```

## 形式主义定义与核心对象

### 定义对象

原文把 tree transducer 写成有限状态树重写系统，输入对象不是线性词，而是 ranked tree。模型核心问题是：有限状态在树上到底是“先看父后看子”还是“先看子后归并”，以及这两种策略对复制、删除和组合能力的影响。

### 核心抽象

原文把树变换器写成统一的五元组：

$$
M = (\Sigma, \Delta, Q, Q_d, R)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是输入 ranked alphabet。
2. `\Delta` 是输出 ranked alphabet。
3. `Q` 是有限状态集。
4. `Q_d` 是 designated states；在 top-down 与 bottom-up 语义中分别扮演初始或终止角色。
5. `R` 是规则集。

对 top-down finite state transformation，规则形如：

$$
q(\sigma(x_1,\ldots,x_k)) \to t
$$

对 bottom-up finite state transformation，规则形如：

$$
\sigma(q_1(x_1),\ldots,q_k(x_k)) \to q(t)
$$

上面两式中的符号逐项解释如下：

1. `\sigma \in \Sigma_k` 是输入树上的 `k` 元节点符号。
2. `q,q_1,\ldots,q_k \in Q` 是有限状态。
3. `x_1,\ldots,x_k` 是对子树位置的变量占位。
4. `t` 是由输出字母表、状态调用和变量构成的输出模板。

论文进一步引入 generalized finite state transformation，其规则可写成：

$$
(q, k, m, \sigma \to t, \varphi)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `k` 是当前输入节点 `\sigma` 的分支数。
3. `m` 是输出模板中待回填的中间结果个数。
4. `t \in T_{\Delta}[X_m]` 是输出模板。
5. `\varphi : X_m \to Q(X_k)` 指定每个输出孔位需要从哪一个子树取得、且以哪个状态计算的翻译结果。

### 一个最小例子与通俗解释

一个最小例子是：输入树根为 `\sigma(t_1,t_2)`。如果使用 top-down 规则，机器可以在没真正看过 `t_1,t_2` 之前，先决定复制哪个子树、先生成什么输出骨架；如果使用 bottom-up 规则，则必须先分别求出两个子树的状态化结果，再在父节点上合并。

通俗地说，top-down 像“先画蓝图再递归填子模块”，bottom-up 像“先把每个零件算清楚，再在父节点统一装配”。`generalized fst` 则把“哪些子树结果需要被拿来拼、拼几次、是否只作为可行性前提”都显式写进一条规则。

### 运行 / 接受 / 转移语义

top-down 情况下，树变换关系可写成：

$$
M = \{(t,s) \mid q(t) \Rightarrow^* s \text{ for some } q \in Q_d\}
$$

bottom-up 情况下，树变换关系可写成：

$$
M = \{(t,s) \mid t \Rightarrow^* q(s) \text{ for some } q \in Q_d\}
$$

上式中的符号逐项解释如下：

1. `t` 是输入树。
2. `s` 是输出树。
3. `\Rightarrow^*` 是由规则集 `R` 诱导的零步或多步改写关系。
4. 两式差别正好体现了“状态包住输入开始往下改写”与“状态包住输出结果往上归并”的方向差异。

对 generalized `fst`，论文给出的状态化语义可保守整理为：

$$
M_q(\sigma(t_1,\ldots,t_k)) = \{\, t[s_1,\ldots,s_m] \mid (q,k,m,\sigma \to t,\varphi)\in R \land s_i \in M_p(t_j) \text{ if } \varphi(x_i)=p(x_j) \,\}
$$

这条式子说明：一条 generalized 规则会先按 `\varphi` 指定的“状态 + 子树位置”取得若干中间翻译结果，再把它们填回输出模板 `t`。

### 语义边界

top-down 擅长“先复制再分别处理”，但删除子树前无法先检查子树内容；bottom-up 擅长“先判子树再决定是否保留”，但难以做无约束复制。论文的 generalized `fst` 正是围绕这条边界线建立的。

### 关键性质与判定边界

论文最关键的结构性结论之一是：

$$
GFST = HOM \circ RELAB \circ FTA \circ HOM
$$

上式中的符号逐项解释如下：

1. `GFST` 是 generalized finite state transformations 类。
2. `HOM` 是 tree homomorphisms。
3. `RELAB` 是 relabeling。
4. `FTA` 是 finite tree automata 级别的树语言过滤。
5. `\circ` 表示关系复合。

这条结果很重要，因为它说明 generalized `fst` 既不是黑盒“更强模型”，也不是杂糅定义，而是可被分解成 homomorphism、重标记和树自动机过滤这几种经典部件。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态是全部模型的核心控制骨架。 |
| 事件 / 触发 | 不适用 | 输入对象是树节点，不是事件流。 |
| 守卫 / 数据 | 不支持 | 没有数值变量；判断主要靠树结构与状态。 |
| 层次 | 强支持 | 直接面向 ranked tree。 |
| 并发 / 同步 | 不支持 | 不是并发行为模型。 |
| 时间约束 | 不支持 | 无时钟、deadline 或延迟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树对象变换。 |
| 可执行 / 可验证性 | 强支持 | 规则、分解、闭包与组合关系都非常清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 统一模型元组 | `$M=(\Sigma,\Delta,Q,Q_d,R)$` | top-down / bottom-up tree transducer 的公共骨架。 |
| top-down 规则 | `$q(\sigma(x_1,\ldots,x_k)) \to t$` | 先在父节点决定输出骨架，再递归处理子树。 |
| bottom-up 规则 | `$\sigma(q_1(x_1),\ldots,q_k(x_k)) \to q(t)$` | 先获得子树状态化结果，再在父节点合并。 |
| generalized 规则 | `$(q,k,m,\sigma \to t,\varphi)$` | 用模板和子树映射统一 top-down / bottom-up 能力。 |
| 分解结论 | `$GFST = HOM \circ RELAB \circ FTA \circ HOM$` | generalized `fst` 可被分解成经典树理论部件。 |

## 构造方式与承载格式

### 建模入口

建模时需要：

1. 选定输入与输出 ranked alphabet。
2. 定义有限状态集合与 designated states。
3. 选择 top-down、bottom-up 或 generalized 规则形式。
4. 为每个输入节点符号编写相应的树模板重写规则。

### 机器可处理承载方式

机器可处理承载方式就是数学规则表：

1. `t-fst` 的父节点驱动规则；
2. `b-fst` 的子树归并规则；
3. generalized `fst` 的模板 `t` 与映射 `\varphi`。

### 交换与互操作

它与 tree homomorphisms、finite tree automata、relabeling 和后续 look-ahead / macro / streaming transducer 路线都直接互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：原文只提供理论规则形式，无工程化文件格式。
- 仿真/执行支持：按树重写关系可直接执行。
- 验证/分析支持：模型比较、分解、组合与闭包性质是全文重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是后续 tree transducer 理论、语法树翻译与 XML/tree transformation 的母线之一。

## 适用场景与需求前提

### 适用场景

适合语法树、项、AST 与结构化文档的有限状态树变换，尤其适合解释“树翻译为什么需要 top-down 还是 bottom-up”的选型场景。

### 需求前提

1. 输入和输出都应自然地表示成 ranked tree。
2. 需求的核心是结构变换，而不是数值计算或连续动态。
3. 若需要复制与删除子树，应先判断是“先复制后处理”还是“先检查后归并”。

### 不适用或高成本场景

若对象本质上是线性词、时钟系统、随机系统或带复杂数据约束的控制逻辑，这组模型就不是最佳入口。

## 与相邻形式主义的关系

它位于 [tree-automata/desc.md](../tree-automata/desc.md) 的“识别树”之后，是“变换树”的经典母线；相对 [top-down-tree-transducers-with-regular-look-ahead/desc.md](../top-down-tree-transducers-with-regular-look-ahead/desc.md)，这里先把普通 top-down / bottom-up 主枝立起来；相对 [macro-tree-transducers/desc.md](../macro-tree-transducers/desc.md) 和 [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)，它是更早的 rule-based tree transformation 蓝本。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文能把演化树里的 `Tree Transducer` 支线从原先“只有 look-ahead 和 STT 两个点”补成有母节点的经典主干。

### 作为目标形式主义还是中间表示

更适合作为谱系母型和理论中间表示，而不是控制系统主线的最终交付语言。

### 对需求到模型生成的启发

当未来需求涉及 AST、配置树或结构化文档转换时，首先要问的不是“要不要树模型”，而是“复制与删除发生在看子树之前还是之后”；这正是 top-down / bottom-up 的分界。

### 现实限制

它主要提供理论骨架，缺少工程 DSL、标准和主流执行环境。

## 重要的相关工作

### 奠基或前身工作

- [tree-automata/desc.md](../tree-automata/desc.md)

### 同类型或同家族工作

- [top-down-tree-transducers-with-regular-look-ahead/desc.md](../top-down-tree-transducers-with-regular-look-ahead/desc.md)
- [the-copying-power-of-one-state-tree-transducers/desc.md](../the-copying-power-of-one-state-tree-transducers/desc.md)
- [macro-tree-transducers/desc.md](../macro-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合充当当前演化树里 `Tree Automata -> Tree Transducer` 的经典母节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Bottom-Up / Top-Down Tree Transducers / Generalized Finite State Transformations
- 论文角色：分支整理
- 核心功能：系统比较自顶向下与自底向上的树变换骨架，并引入 generalized `fst` 统一两者。
- 关键特性：树结构、有限状态、复制/删除顺序差异、`GFST` 分解。
- 构造方式：ranked alphabet + 有限状态 + tree rewrite rules / template mapping。
- 配套基础设施：以理论规则和分解定理为主，无工程标准。
- 适用场景：语法树、AST、结构化文档与形式语言中的树到树翻译。

