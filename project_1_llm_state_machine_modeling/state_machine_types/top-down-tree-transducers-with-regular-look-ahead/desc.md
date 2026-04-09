# 带正则前瞻的自顶向下树变换器 / Top-down tree transducers with regular look-ahead

## 基本信息

- 标题：Top-down tree transducers with regular look-ahead
- 中文标题：带正则前瞻的自顶向下树变换器
- 作者：Joost Engelfriet
- 发表：DAIMI Report Series, 4(49):1-34, 1975
- DOI：`10.7146/dpb.v4i49.6468`
- 链接：https://tidsskrift.dk/daimipb/article/download/6468/5587/21815
- 形式主义：Top-down Tree Transducers with Regular Look-Ahead
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文只给出模型与分解定理；无独立实现。机器可处理入口是树变换规则和 recognizable look-ahead 约束。
- 标准/格式获取方式：原文没有 XML/JSON 标准，承载方式是 top-down tree transducer 规则加每个变量位置的 recognizable-language 条件。

## 简报

这篇报告补上的不是一般“树自动机相关论文”，而是树对象主干里非常关键的一条 `tree transducer` 支线。它把普通 top-down tree transducer 无法先检查子树再决定是否删除/改写的弱点，用 `regular look-ahead` 明确补齐，从而把 top-down tree transformation 的闭包和分解性质稳定下来。

- 形式主义定位：经典 top-down tree transducer 的可检查子树版本，是 tree transducer 族中非常稳定的命名节点。
- 构造方式简述：规则仍然是自顶向下展开，但每个变量位置都可以附带“该子树必须属于某个 recognizable tree language”的前瞻条件。
- 基础设施与场景简述：原文完全是理论工作，没有工程标准；但它给出了与 bottom-up relabeling 和 ordinary top-down transducer 的清晰分解关系。

```text
输入树 -> recognizable look-ahead -> top-down rewrite -> output tree / surface set
```

## 形式主义定义与核心对象

### 定义对象

原文的核心改动很直接：保留 ordinary top-down fst 的重写骨架，但让规则中的每个变量都带一个 recognizable tree-language 约束，这样机器在处理父节点前，就能“先看一眼”各个子树是否满足某种正则性质。

### 核心抽象

按原文 Definition 2.1 的保守整理，带 regular look-ahead 的 top-down tree transducer 可写成：

$$
T = \langle \Sigma, \Delta, Q, Q_d, R \rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是输入 ranked alphabet。
2. `\Delta` 是输出 ranked alphabet。
3. `Q` 是有限状态集。
4. `Q_d` 是 distinguished initial states。
5. `R` 是有限规则集。

原文把每条规则写成“ordinary top-down rule + look-ahead mapping”的二元组：

$$
\langle t_1 \to t_2, D \rangle
$$

其中 `D` 给出每个变量位置的前瞻约束：

$$
D(x_i) \in \mathrm{RECOG}
$$

上式中的符号逐项解释如下：

1. `t_1 \to t_2` 是普通 top-down tree transducer 规则。
2. `x_i` 是规则左侧出现的变量，代表某个待处理子树。
3. `D(x_i)` 是该子树必须满足的 recognizable tree language。
4. `\mathrm{RECOG}` 表示 recognizable tree languages 类。

因此，这个模型的关键不是“增加更多状态”，而是在规则应用前，把对子树的正则可识别性质检查变成显式语义的一部分。

### 一个最小例子与通俗解释

一个最小例子是：只有当某个右子树属于某个 recognizable tree language `$U$` 时，才允许删除左子树并把右子树提升为结果。普通 top-down tree transducer 做不到这一点，因为它必须在没看过右子树内容前就决定是否删左子树；而带 regular look-ahead 的版本可以先用 `D(x_2)=U` 检查右子树，再决定规则是否可用。

通俗地说，这个模型像“会先验一下孩子节点，再从根往下改写”的树编辑器。它仍然是自顶向下的，但不再是盲写，而是带一个有限状态 tree-automaton 级别的前瞻过滤器。

### 运行 / 接受 / 转移语义

其运行语义仍然是 tree transformation，而不是 accept/reject。对某个输入树 `t`，只有在当前规则中每个变量绑定到的子树都满足对应 `D(x_i)` 时，该规则才能被应用。于是某条规则的可用性条件可保守写成：

$$
\forall x_i \in \mathrm{Var}(t_1), \quad s_i \in D(x_i)
$$

上式中的符号逐项解释如下：

1. `\mathrm{Var}(t_1)` 是左侧模式中出现的变量集合。
2. `s_i` 是当前输入树中与变量 `x_i` 匹配的实际子树。
3. `D(x_i)` 是该变量位置的 recognizable look-ahead 条件。

在满足这些条件后，才按 ordinary top-down transducer 的方式，把 `$t_1$` 重写成 `$t_2$`。

### 语义边界

相对普通 top-down tree transducer，它多了“删除或替换子树前先检查子树正则性质”的能力；相对 bottom-up tree transducer，它仍然以 top-down rewrite 为主，而不是自底向上综合状态。

### 关键性质与判定边界

原文最重要的结果不是某个具体算法，而是分解与组合。核心分解定理可压缩成：

$$
T^R\text{-FST} \subseteq DBQREL \circ T\text{-FST}
$$

上式中的符号逐项解释如下：

1. `T^R\text{-FST}` 表示带 regular look-ahead 的 top-down finite-state tree transformation 类。
2. `DBQREL` 是 deterministic bottom-up finite-state relabeling。
3. `T\text{-FST}` 是 ordinary top-down finite-state tree transformation。
4. `\circ` 表示先做 bottom-up relabeling，再做 ordinary top-down transformation。

这条式子非常关键，因为它说明：regular look-ahead 不是“玄学增强”，而是可以被分解成一个先计算可识别属性的 bottom-up relabeling，再接一个标准 top-down transducer。

原文还把它用于 closure properties 和 surface sets，说明这条支线在树变换理论中是稳定可组合的。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态 top-down control 仍是核心。 |
| 事件 / 触发 | 不适用 | 输入对象是树节点而非事件流。 |
| 守卫 / 数据 | 部分支持 | 不支持数值变量，但支持 recognizable look-ahead 条件。 |
| 层次 | 强支持 | 直接面向树结构。 |
| 并发 / 同步 | 不支持 | 不是并发模型。 |
| 时间约束 | 不支持 | 无时钟与延迟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树对象变换。 |
| 可执行 / 可验证性 | 强支持 | 有清晰分解、组合与 closure 理论。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$T=\langle \Sigma,\Delta,Q,Q_d,R \rangle$` | 带 regular look-ahead 的 top-down tree transducer 骨架。 |
| 规则增强 | `$\langle t_1 \to t_2, D \rangle$` | ordinary rule 外加子树可识别前瞻条件。 |
| 变量约束 | `$D(x_i) \in \mathrm{RECOG}$` | look-ahead 只允许 recognizable tree-language 级别。 |
| 分解定理 | `$T^R\text{-FST} \subseteq DBQREL \circ T\text{-FST}$` | 先自底向上标注，再普通自顶向下改写。 |
| 理论收益 | `closure of surface sets / composition` | 修补普通 top-down tree transducer 的闭包缺陷。 |

## 构造方式与承载格式

### 建模入口

建模需要：

1. 定义输入与输出 ranked alphabet。
2. 定义 top-down control states。
3. 编写树重写规则。
4. 给每个变量位置附上 recognizable look-ahead 条件。

### 机器可处理承载方式

其机器可处理承载方式是：

1. rule-based tree transformation；
2. recognizable tree-language constraints；
3. 可选的 deterministic bottom-up relabeling 分解。

### 交换与互操作

它和 `Tree Automata`、bottom-up relabeling、surface sets 以及 tree transformation languages 直接互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：通过规则与 recognizable language 指定，不是工程交换标准。
- 仿真/执行支持：理论上可执行为“先判 look-ahead，再做 top-down rewrite”。
- 验证/分析支持：composition、decomposition 和 closure properties 是原文重点。
- 代码生成/转换支持：原文未讨论代码生成。
- 标准化或社区生态：是后续 tree transducer / XML tree transformation 理论的重要前身节点。

## 适用场景与需求前提

### 适用场景

适合任何“输出树如何生成取决于输入子树是否属于某个正则树语言”的变换场景，例如结构化过滤、条件性子树删除与可识别形状驱动的树改写。

### 需求前提

1. 输入与输出对象都应天然是树。
2. 需要先看子树的 recognizable property 再决定是否改写。
3. 前瞻必须能压成有限 tree automaton 级别的正则性质，而不是任意语义谓词。

### 不适用或高成本场景

若需求只需普通 top-down rewrite，不需要子树检查，则 regular look-ahead 是多余成本；若条件超出 recognizable tree languages，则该模型仍不够强。

## 与相邻形式主义的关系

相对 [tree-automata/desc.md](../tree-automata/desc.md)，它从“识别树语言”转向“变换树”；相对普通 top-down tree transducer，它增加 recognizable look-ahead；相对 [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)，它不是单遍线性化 streaming 模型，而是更经典的 rule-based tree transformation 分支。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata` 节点下缺失已久的 `Tree Transducer` 支线正式命名化，有助于后续继续把现代 `STT`、XML transformation 或 macro-tree 路线挂到同一父节点下。

### 作为目标形式主义还是中间表示

更适合作为理论母型或中间谱系节点，而不是控制系统主线的最终交付形式主义。

### 对需求到模型生成的启发

如果未来需求转向树状配置、AST 或 XML-like 结构，单纯识别模型不够，必须考虑树变换模型；而“look-ahead 是否只需正则树性质”是很好的选型分界线。

### 现实限制

缺少直接工程标准与主流开发者工具，主要价值仍在谱系与表达力边界。

## 重要的相关工作

### 奠基或前身工作

- [tree-automata/desc.md](../tree-automata/desc.md)
- ordinary top-down / bottom-up finite-state tree transducer 路线

### 同类型或同家族工作

- [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合补当前演化树里的 `Tree Automata -> Tree Transducer` 经典支线。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Top-down Tree Transducers with Regular Look-Ahead
- 论文角色：模型提出
- 核心功能：在 top-down tree transducer 中引入 recognizable subtree look-ahead，使规则应用前可检查子树正则性质。
- 关键特性：regular look-ahead、tree rewrite、分解成 bottom-up relabeling + ordinary top-down transducer、closure properties 改善。
- 构造方式：`T=\langle \Sigma,\Delta,Q,Q_d,R \rangle` 加规则级 look-ahead 映射 `D(x_i) \in RECOG`。
- 基础设施：纯理论模型，无工程标准与工具。
- 适用场景：树结构条件改写、surface sets、tree transformation language 理论主干。
- 需求前提：条件性改写必须可压成 recognizable tree-language 级别的前瞻判断。
- 状态：🟢
