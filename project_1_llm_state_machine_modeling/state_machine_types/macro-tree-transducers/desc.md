# 宏树变换器 / Macro Tree Transducers

## 基本信息

- 标题：Macro Tree Transducers
- 中文标题：宏树变换器
- 作者：Joost Engelfriet, Heiko Vogler
- 发表：Journal of Computer and System Sciences, 31(1):71-146, 1985
- DOI：`10.1016/0022-0000(85)90066-2`
- 链接：https://ris.utwente.nl/ws/files/6562639/Engelfriet85macro.pdf
- 形式主义：Macro Tree Transducers
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文给出 `MT`、`IO/OI` 派生语义、regular look-ahead 与组合分解结论；无独立实现。
- 标准/格式获取方式：原文没有工程标准，机器可处理入口是 ranked alphabets、带参数的状态和宏规则集 `R`。

## 简报

`Macro Tree Transducer` 是 tree transducer 主枝里非常关键的一层：它把普通 top-down tree transducer 的“只会往下传结构”推进到“还能显式携带上下文参数”。这使它既像树上的递归过程系统，又像 syntax-directed semantics 的形式化骨架，因此非常适合作为 `Tree Transducer` 支线中的主节点。

- 形式主义定位：带上下文参数的 top-down tree transducer，是 tree translation 中处理 context information 的经典母型。
- 构造方式简述：规则左侧是 `q(\sigma(x_1,\ldots,x_m),y_1,\ldots,y_n)`，右侧可递归调用其他状态并传递参数。
- 基础设施与场景简述：原文是理论工作，但系统讨论了 `IO/OI` 语义、regular look-ahead、组合与分解、domain/range 等核心问题。

```text
输入树 + 上下文参数 -> macro rule expansion -> 输出树 / 输出串
```

## 形式主义定义与核心对象

### 定义对象

`Macro tree transducer` 的核心动机是：普通 top-down tree transducer 能递归处理子树，但很难把“已经积累的上下文”显式带给后续翻译；macro 版本通过参数把这种上下文传递写成模型本体的一部分。

### 核心抽象

原文把 macro tree transducer 定义成：

$$
M = (Q, \Sigma, \Delta, q^{in}, R)
$$

上式中的符号逐项解释如下：

1. `Q` 是 ranked states，每个状态至少 rank 为 `1`。
2. `\Sigma` 是 ranked input alphabet。
3. `\Delta` 是 ranked output alphabet。
4. `q^{in}` 是初始状态，rank 为 `1`。
5. `R` 是规则集。

规则的标准形态是：

$$
q(\sigma(x_1,\ldots,x_m), y_1,\ldots,y_n) \to t
$$

其中：

$$
t \in RHS(Q,\Delta,m,n)
$$

上面两式中的符号逐项解释如下：

1. `x_1,\ldots,x_m` 是输入子树变量。
2. `y_1,\ldots,y_n` 是上下文参数。
3. `RHS(Q,\Delta,m,n)` 是允许由输出符号、参数和带参数的状态调用嵌套构成的右侧项集合。

若把所有状态 rank 都限制为 `1`，就退化回普通 top-down tree transducer。

### 一个最小例子与通俗解释

一个最小例子是：当翻译某个语法树节点 `\sigma(t_1,t_2)` 时，状态 `q` 不仅处理 `t_1,t_2`，还额外收到参数 `y`，表示“当前上下文里已经构造好的前缀”。规则右侧可以把 `y` 传给某个子调用，也可以先用输出符号包裹后再传递。

通俗地说，macro tree transducer 像“在树上递归运行的一组带参数过程”。普通 tree transducer 只会递归下钻，而 macro 版本会在下钻时顺手把上下文一起带下去。

### 运行 / 接受 / 转移语义

其核心运行单位是带参数的状态调用：

$$
q(s, y_1,\ldots,y_n)
$$

其中 `s` 是当前输入子树，`y_1,\ldots,y_n` 是当前上下文对象。对 deterministic 情况，论文强调 total deterministic `MT` 在 `IO` 和 `OI` 两种求值方式下给出同一映射。可保守写成：

$$
\tau_{IO}(M) = \tau_{OI}(M) \quad \text{for total deterministic } M
$$

上式中的符号逐项解释如下：

1. `\tau_{IO}` 表示 outside-in / call-by-value 风格语义。
2. `\tau_{OI}` 表示 inside-out / call-by-name 风格语义。
3. 等式表示 total deterministic 情况下两种求值顺序不改变最终翻译。

### 语义边界

相对普通 top-down tree transducer，它多了参数化上下文；相对 attribute grammar 或 denotational semantics，它保留的是有限状态树翻译骨架，而不是完整语义工程环境。

### 关键性质与判定边界

论文的重要结论之一是：regular look-ahead 不增加 macro tree transducer 的变换能力。可保守写成：

$$
MT = MT^{R}
$$

同时，论文把它与 top-down tree transducer 和 context-free tree grammar 的关系固定下来，可概括为：

$$
T \subseteq MT
$$

上面两式中的符号逐项解释如下：

1. `MT` 是 macro tree transducer 类。
2. `MT^R` 是带 regular look-ahead 的 macro tree transducer。
3. `T` 是普通 top-down tree transducer。

这些结论说明：macro 版本是“显式上下文参数”的经典树变换母型，而不是零散技巧拼接。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 带 rank 的状态负责选择递归翻译过程。 |
| 事件 / 触发 | 不适用 | 输入对象是树节点。 |
| 守卫 / 数据 | 部分支持 | 无一般数值变量，但有显式上下文参数。 |
| 层次 | 强支持 | 直接递归处理树。 |
| 并发 / 同步 | 不支持 | 不是并发模型。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树对象变换。 |
| 可执行 / 可验证性 | 强支持 | `IO/OI` 语义、组合分解和 domain/range 分析都较成熟。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$M=(Q,\Sigma,\Delta,q^{in},R)$` | macro tree transducer 的标准骨架。 |
| 规则形式 | `$q(\sigma(x_1,\ldots,x_m),y_1,\ldots,y_n)\to t$` | 子树变量和上下文参数同时进入规则。 |
| 右侧集合 | `$t\in RHS(Q,\Delta,m,n)$` | 右侧允许嵌套状态调用和参数传播。 |
| 求值一致性 | `$\tau_{IO}(M)=\tau_{OI}(M)$` | total deterministic 情况下 `IO/OI` 结果一致。 |
| look-ahead 边界 | `$MT = MT^{R}$` | regular look-ahead 不增加其变换能力。 |

## 构造方式与承载格式

### 建模入口

建模时需要：

1. 选定输入树和输出树字母表。
2. 设计带 rank 的状态集。
3. 明确哪些信息作为上下文参数传递。
4. 编写 macro 规则并决定 `IO/OI` 求值口径。

### 机器可处理承载方式

机器可处理承载方式是带参数的宏规则系统：

1. 输入子树变量；
2. 上下文参数；
3. 输出模板；
4. 嵌套状态调用。

### 交换与互操作

它与 top-down tree transducer、context-free tree grammar、syntax-directed translation、attribute grammar 与 pushdown/indexed machine 路线都直接互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：无工程化交换标准。
- 仿真/执行支持：`IO/OI` 导出语义明确，可直接执行。
- 验证/分析支持：composition、decomposition、domain、range、regular look-ahead 是全文重点。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是树翻译和 syntax-directed semantics 理论中的核心模型。

## 适用场景与需求前提

### 适用场景

适合语法树、AST 与结构化语义对象的上下文敏感翻译，例如编译中的语义传递、树到树/树到串的参数化转换。

### 需求前提

1. 输入对象必须是树。
2. 变换过程需要显式携带上下文信息。
3. 上下文应能通过有限个参数递归传播，而非依赖任意外部存储。

### 不适用或高成本场景

若需求主要是纯树识别、无上下文模板替换或工程化标准建模语言，macro 级别会显得偏重。

## 与相邻形式主义的关系

它是 [bottom-up-and-top-down-tree-transformations-a-comparison/desc.md](../bottom-up-and-top-down-tree-transformations-a-comparison/desc.md) 中 top-down 路线的增强版；相对 [the-copying-power-of-one-state-tree-transducers/desc.md](../the-copying-power-of-one-state-tree-transducers/desc.md)，它从无状态模板提升到带参数递归；相对 [pushdown-machines-for-the-macro-tree-transducer/desc.md](../pushdown-machines-for-the-macro-tree-transducer/desc.md)，后者进一步把它重新解释成 indexed / pushdown machine。

## 与本研究的关系

### 对 Project 1 的价值

它能把当前演化树中的 `Tree Transducer` 主枝往“上下文敏感树变换”方向稳定地长出一层经典节点。

### 作为目标形式主义还是中间表示

更适合作为理论母型和中间谱系节点，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

当需求文本里出现“上下文继承”“父环境影响子翻译”“需要把已经构造的语义对象继续往下传”时，普通 top-down tree transducer 不够，macro 级别才是合理候选。

### 现实限制

虽然理论很强，但工程侧仍缺统一标准和主流建模工具。

## 重要的相关工作

### 奠基或前身工作

- [bottom-up-and-top-down-tree-transformations-a-comparison/desc.md](../bottom-up-and-top-down-tree-transformations-a-comparison/desc.md)
- [top-down-tree-transducers-with-regular-look-ahead/desc.md](../top-down-tree-transducers-with-regular-look-ahead/desc.md)

### 同类型或同家族工作

- [the-copying-power-of-one-state-tree-transducers/desc.md](../the-copying-power-of-one-state-tree-transducers/desc.md)
- [pushdown-machines-for-the-macro-tree-transducer/desc.md](../pushdown-machines-for-the-macro-tree-transducer/desc.md)
- [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合充当当前演化树里 `Tree Transducer` 主枝向“显式上下文参数”分化的经典节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Macro Tree Transducers
- 论文角色：模型提出
- 核心功能：把上下文参数显式引入 top-down tree translation，形成带参数递归的树变换模型。
- 关键特性：参数传递、`IO/OI` 语义、regular look-ahead、composition/decomposition、domain/range。
- 构造方式：带 rank 的状态 + 输入子树变量 + 参数 + macro 规则。
- 配套基础设施：以理论定义和分解结果为主，无工程标准。
- 适用场景：上下文敏感语法树翻译、syntax-directed semantics、参数化树变换。

