# 加权自动机算法 / Weighted Automata Algorithms

## 基本信息

- 标题：Weighted Automata Algorithms
- 中文标题：加权自动机算法
- 作者：Mehryar Mohri
- 发表：in Handbook of Weighted Automata, pp. 213-254, 2009
- DOI：原文未提供
- 链接：http://www.cs.nyu.edu/~mohri/postscript/hwa.pdf
- 形式主义：Weighted Automata
- 主类：🧩
- 描述客体：📝
- 所属领域：🧮
- 论文角色：手册章节
- 工具/实现获取方式：原文章节给出算法与图表示，不附带统一代码下载入口。
- 标准/格式获取方式：原文以图与 semiring 定义给出模型，不规定 XML/JSON/DSL 标准。

## 简报

这章虽然标题强调算法，但开头先把 `Weighted Automata / Weighted Transducers` 的本体定义讲得非常清楚：有限状态结构不再只判断接受/拒绝，而是沿路径组合权值，并在多个路径之间按 semiring 运算聚合结果。对想把“代价 / 概率 / 分数”并入自动机的人来说，这是一条非常标准的本体入口。

- 形式主义定位：在有限状态自动机或转导器上附加 semiring 权值的定量自动机。
- 构造方式简述：图结构 + 标签 + 权值 + semiring 运算；加权自动机可看作输入输出标签相同的加权转导器。
- 基础设施与场景简述：算法体系成熟，适合概率、代价、评分和最短路类分析，但原文不提供统一交换标准。

```text
字符串 / trace -> Weighted Automata -> 路径权值组合 -> 概率 / 代价 / 评分分析
```

## 形式主义定义与核心对象

### 定义对象

加权自动机面向的仍然是字符串或输入输出串对，但不再只做布尔接受，而是给每条迁移、每条路径以及每个串赋予可组合的权值。

### 核心抽象

原文先定义 semiring：

$$
(S, \oplus, \otimes, 0, 1)
$$

再定义 weighted transducer：

$$
T = (\Sigma, \Delta, Q, I, F, E, \lambda, \rho)
$$

其中迁移和初末状态都可携带权值。文中随后说明 weighted automaton 可视为“输入输出标签相同的 weighted transducer”，因此仍保留有限状态骨架，但把布尔语义提升到了 semiring 语义。

### 语义边界

相对普通 `Finite Automata`，它多了路径权值和路径间聚合；相对 `Probabilistic Automata`，它更一般，因为 semiring 不限于概率；相对 `Weighted Logics`，它偏自动机和图算法本体。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 基础仍是有限状态图。 |
| 事件 / 触发 | 支持 | 输入符号依然驱动迁移。 |
| 守卫 / 数据 | 不支持 | 原始模型核心是权值，不是变量守卫。 |
| 层次 | 不支持 | 不是层次状态图。 |
| 并发 / 同步 | 不支持 | 不是并发网模型。 |
| 时间约束 | 部分支持 | 可表达代价/延迟类权值，但不是显式时钟自动机。 |
| 连续动态 / 随机性 | 部分支持 | 可承载概率和其他数值权，但不是混成连续语义。 |
| 可执行 / 可验证性 | 强支持 | shortest-distance、composition、determinization、minimization 是本文核心。 |

## 构造方式与承载格式

### 建模入口

建模时要先确定三件事：

1. 有限状态结构本身。
2. 权值所在的 semiring。
3. 权值如何沿路径组合与聚合。

### 机器可处理承载方式

原文明显偏向图表示和算法伪代码。机器可处理对象通常是图结构、标签和权值表，而不是标准文档格式。

### 交换与互操作

原文没有规定统一交换标准。互操作更多依赖“图 + semiring”这一抽象接口，而不是公共 XML/JSON 语法。

## 配套基础设施

- 建模/编辑工具：原文未绑定具体工具。
- 解析/交换/元模型支持：原文以图和 semiring 语义为主，不给统一元模型文件标准。
- 仿真/执行支持：可按路径权值执行或计算最优/总权结果。
- 验证/分析支持：最短距离、epsilon-removal、composition、determinization、minimization 是成熟主线。
- 代码生成/转换支持：原文关注 automata/transducer 算法，不讨论代码生成。
- 标准化或社区生态：算法和应用生态很强，特别适合语音、NLP、OCR、机器学习等定量有限状态任务。

## 适用场景与需求前提

### 适用场景

适用于需要在有限状态结构上附加概率、代价、得分或其他可组合数值的场景，如 speech/NLP 中的加权识别与转导。

### 需求前提

1. 核心对象仍然可表达为有限状态图。
2. 每条迁移或路径都需要可组合权值。
3. 权值组合规律能够被某个 semiring 统一描述。

### 不适用或高成本场景

如果系统需要变量守卫、层次状态、实时时钟或连续物理流，仅靠加权自动机不够。

## 与相邻形式主义的关系

相对 `Finite Automata`，它把布尔接受提升为 semiring 语义；相对 `Probabilistic Automata`，它更一般；相对 `Weighted Logics`，它提供的是更直接的自动机承载；相对 `Transducers`，它可以统一处理 acceptor 与 transducer 两类对象。

## 与本研究的关系

### 对 Project 1 的价值

它不是控制系统状态机的主流目标形式，但在需要把“不确定性 / 成本 / 偏好”并入状态机时很有启发。

### 作为目标形式主义还是中间表示

更适合作为扩展型中间表示，而不是默认最终输出对象。

### 对需求到模型生成的启发

如果需求不仅在问“能不能发生”，还在问“代价多大、优先级如何、概率多高”，布尔状态机可能就不够了。

### 现实限制

原文重点是模型与算法，没有给出现代交换标准，因此落地时仍需补具体工具和格式线。

## 重要的相关工作

### 奠基或前身工作

- rational power series。
- unweighted finite automata / transducer 算法。

### 同类型或同家族工作

- weighted logics。
- probabilistic / tropical / log semiring 自动机。

### 标准 / 格式 / 工具链工作

- 原文不定义交换标准，但明确以 graph + semiring 为接口。

### 与本研究关系最紧的工作

- 对状态机引入代价、偏好或置信度的扩展方向。

## 文献分类总结

- 主类：🧩
- 描述客体：📝
- 所属领域：🧮
- 形式主义：Weighted Automata
- 论文角色：手册章节
- 核心功能：在有限状态自动机/转导器上引入 semiring 权值并支持定量分析。
- 关键特性：semiring、weighted transducer、path weight、determinization、minimization。
- 构造方式：图结构 + 标签 + 权值 + semiring 运算。
- 基础设施：算法体系成熟，但原文不提供统一交换标准。
- 适用场景：概率/代价/评分型字符串与转导建模。
- 需求前提：需求必须仍能压成有限状态图，并且权值满足统一组合语义。
- 状态：🟢
