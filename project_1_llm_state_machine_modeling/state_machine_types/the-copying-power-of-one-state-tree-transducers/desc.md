# 单状态树变换器的复制能力 / The Copying Power of One-State Tree Transducers

## 基本信息

- 标题：The Copying Power of One-State Tree Transducers
- 中文标题：单状态树变换器的复制能力
- 作者：Joost Engelfriet, Sven Skyum
- 发表：Journal of Computer and System Sciences, 25(3):418-435, 1982
- DOI：`10.1016/0022-0000(82)90019-8`
- 链接：https://ris.utwente.nl/ws/files/6738048/Engelfriet82copying.pdf
- 形式主义：Tree Homomorphisms / One-State Deterministic Top-Down Tree Transducers
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：能力边界
- 工具/实现获取方式：原文只给出 tree homomorphism、copying operation 与语言闭包分析；无独立实现。
- 标准/格式获取方式：原文没有工程标准，机器可处理入口是 ranked alphabet 上的 homomorphism 映射族 `H_k`。

## 简报

这篇论文的重要性在于，它把 `one-state deterministic top-down tree transducer` 与 `tree homomorphism` 直接等同起来，并用“prime copying 不可实现”这条非常硬的能力边界，把 `Tree Transducer` 主枝里的一个经典弱模型节点稳定下来。对演化树来说，它非常适合挂成 `Top-Down Tree Transducer` 下的 `Tree Homomorphisms / One-State Tree Transducers`。

- 形式主义定位：最经典、最受限的一类 top-down tree transducer，只保留一个状态和固定的树同态替换能力。
- 构造方式简述：每个输入符号 `\sigma \in \Sigma_k` 预先指定一个输出模板 `H_k(\sigma) \in T_{\Delta}[X_k]`，运行时把各子树翻译结果代回模板。
- 基础设施与场景简述：原文完全是理论工作，但给出了 tree homomorphism 的复制能力上界，尤其澄清了它能做什么、绝对做不了什么。

```text
输入树 -> 符号级同态模板 H_k -> 递归替换子树翻译结果 -> 输出树 / 输出串
```

## 形式主义定义与核心对象

### 定义对象

`tree homomorphism` 是树对象上的最基础变换器之一。它没有多状态控制，也没有看上下文后的条件分支；每个输入符号的翻译形式在模型定义时就已经固定。

### 核心抽象

原文把 tree homomorphism 定义成一个由映射族决定的翻译：

$$
H = \{H_k : \Sigma_k \to T_{\Delta}[X_k] \mid k \ge 0\}
$$

上式中的符号逐项解释如下：

1. `\Sigma_k` 是输入 ranked alphabet 中秩为 `k` 的符号集合。
2. `\Delta` 是输出 ranked alphabet。
3. `X_k = \{x_1,\ldots,x_k\}` 是子树位置变量。
4. `T_{\Delta}[X_k]` 是由输出符号和变量组成的输出模板树。

其递归语义写成：

$$
H(\sigma(t_1,\ldots,t_k)) = H_k(\sigma)[H(t_1),\ldots,H(t_k)]
$$

上式中的符号逐项解释如下：

1. `\sigma(t_1,\ldots,t_k)` 是输入树的一个节点及其子树。
2. `H_k(\sigma)` 是该输入符号对应的固定输出模板。
3. 方括号表示把各子树的翻译结果替换到模板变量位置中。

论文强调这一模型等价于 one-state deterministic top-down tree transducer，因此可把它看成“只有一个状态的 top-down tree transducer”。

### 一个最小例子与通俗解释

一个最小例子是：定义 `H_2(\sigma)=g(x_1,x_1,x_2)`。那么输入树 `\sigma(t_1,t_2)` 会被翻译成 `g(H(t_1),H(t_1),H(t_2))`。这说明模型能做固定倍数的复制，例如把左子树复制两次。

通俗地说，tree homomorphism 像一个“静态树模板替换器”。它不会根据运行中的状态改变策略，只会按每个输入符号预先写好的模板机械展开。

### 运行 / 接受 / 转移语义

论文把某个子树 `s` 在大树 `t` 中被翻译后复制多少次，定义成 translation number `\mathrm{trn}_H(s,t)`。其核心结论是：对固定 `H`，所有这样的复制次数都只能由一组有限小整数相乘得到。可写成：

$$
\mathrm{trn}_H(s,t) \in D_{\{n \mid 0 < n < N\}}
$$

上式中的符号逐项解释如下：

1. `\mathrm{trn}_H(s,t)` 表示子树 `s` 在 `H(t)` 中对应翻译结果出现的次数。
2. `N` 是由同态 `H` 决定的常数上界。
3. `D_A` 表示集合 `A` 中元素乘积所形成的集合。

这条式子就是后面“不能做 prime copying”的基础。

### 语义边界

它能做固定模板复制，也能做某些纯指数型复制，但不能根据输入长度实现具有任意大素因子的复制次数；这比多状态 top-down transducer 和更强的 tree transducer 弱得多。

### 关键性质与判定边界

论文定义的 copying operation 形如：

$$
c_f(L) = \{\$(w\$)^{f(n)} \mid f(n) > 1,\ w \in L\}
$$

并证明 deterministic one-state top-down tree transducers 不能处理 prime copying。可保守概括为：

$$
\mathrm{HOM} \text{ is not closed under prime copying}
$$

上面两式中的符号逐项解释如下：

1. `f` 是整数函数，决定复制次数。
2. `c_f` 把字符串按 `f(n)` 次进行包裹式复制。
3. “prime copying” 指 `f` 的值域中包含具有任意大素因子的数。
4. `\mathrm{HOM}` 表示 tree homomorphism 类。

这正是它作为独立节点的原因：它不是一般 top-down transducer，而是明确更弱的一层。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 极弱支持 | 只对应单状态 deterministic top-down 行为。 |
| 事件 / 触发 | 不适用 | 输入是树节点，不是事件流。 |
| 守卫 / 数据 | 不支持 | 无额外条件或变量。 |
| 层次 | 强支持 | 直接面向树递归结构。 |
| 并发 / 同步 | 不支持 | 不是并发模型。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树对象变换。 |
| 可执行 / 可验证性 | 强支持 | 同态模板、复制上界和闭包边界都非常清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 同态族定义 | `$H=\{H_k:\Sigma_k\to T_{\Delta}[X_k]\}$` | 每个输入符号对应一个固定输出模板。 |
| 递归语义 | `$H(\sigma(t_1,\ldots,t_k))=H_k(\sigma)[H(t_1),\ldots,H(t_k)]$` | 输出由模板替换递归构成。 |
| 复制次数上界 | `$\mathrm{trn}_H(s,t)\in D_{\{n\mid 0<n<N\}}$` | 子树翻译被复制的次数只含有限小素因子。 |
| copying 操作 | `$c_f(L)=\{\$(w\$)^{f(n)}\mid f(n)>1,\ w\in L\}$` | 用于刻画模型能否实现某类复制。 |
| 能力边界 | `$\mathrm{HOM}$ not closed under prime copying` | one-state tree transducer 不能实现 prime copying。 |

## 构造方式与承载格式

### 建模入口

建模时只需：

1. 选定输入与输出 ranked alphabet。
2. 对每个输入符号给出一个输出模板。
3. 决定模板中哪些变量被保留、删除或固定次复制。

### 机器可处理承载方式

机器可处理承载方式就是符号到模板的映射表 `H_k`，没有单独状态机控制表。

### 交换与互操作

它与 top-down tree transducers、syntax-directed translation、restricted parallel level languages 以及后续 macro / streaming transducer 理论直接互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：原文只有数学同态定义。
- 仿真/执行支持：递归模板替换即可执行。
- 验证/分析支持：复制能力边界和语言闭包分析非常强。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是 tree transducer hierarchy 中的基础弱模型节点。

## 适用场景与需求前提

### 适用场景

适合表达“结构固定、上下文无状态”的树到树或树到串翻译，例如语法树的静态模板映射和有限固定倍数复制。

### 需求前提

1. 输入对象必须是树。
2. 每个输入符号的翻译模式必须可预先固定。
3. 不依赖运行中状态、上下文参数或任意增长的复制次数。

### 不适用或高成本场景

若需要上下文参数、条件性 look-ahead、任意增长复制或复杂状态依赖，就必须升级到更强的 tree transducer。

## 与相邻形式主义的关系

它是 [bottom-up-and-top-down-tree-transformations-a-comparison/desc.md](../bottom-up-and-top-down-tree-transformations-a-comparison/desc.md) 中 top-down 路线的一个极简弱化节点；相对 [top-down-tree-transducers-with-regular-look-ahead/desc.md](../top-down-tree-transducers-with-regular-look-ahead/desc.md)，它没有前瞻；相对 [macro-tree-transducers/desc.md](../macro-tree-transducers/desc.md)，它没有参数和上下文。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Tree Transducer` 主枝中的“最弱同态层”明确挂出来，避免后续把所有树变换模型都混成一层。

### 作为目标形式主义还是中间表示

更适合作为理论参照点和表达力下界，而不是最终建模语言。

### 对需求到模型生成的启发

如果需求只是静态结构重写，就不需要更强模型；但一旦涉及任意复制或上下文传播，tree homomorphism 明显不够。

### 现实限制

表达力很受限，几乎不可能直接承担复杂控制系统建模。

## 重要的相关工作

### 奠基或前身工作

- [bottom-up-and-top-down-tree-transformations-a-comparison/desc.md](../bottom-up-and-top-down-tree-transformations-a-comparison/desc.md)

### 同类型或同家族工作

- [top-down-tree-transducers-with-regular-look-ahead/desc.md](../top-down-tree-transducers-with-regular-look-ahead/desc.md)
- [macro-tree-transducers/desc.md](../macro-tree-transducers/desc.md)
- [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合作为当前演化树中 `Top-Down Tree Transducer` 下的弱模型节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Tree Homomorphisms / One-State Deterministic Top-Down Tree Transducers
- 论文角色：能力边界
- 核心功能：把 one-state deterministic top-down tree transducer 解释为 tree homomorphism，并给出复制能力上界。
- 关键特性：符号到模板的固定映射、translation number、有界素因子复制、prime copying 不可实现。
- 构造方式：映射族 `H_k` + 递归模板替换。
- 配套基础设施：以理论定义和闭包边界为主，无工程标准。
- 适用场景：静态结构映射、有限固定倍复制的树变换与形式语言分析。

