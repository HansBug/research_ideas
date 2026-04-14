# mcpta：面向概率定时自动机的 Modest-PRISM 检查路线 / A Modest Approach to Checking Probabilistic Timed Automata

## 基本信息

- 标题：A Modest Approach to Checking Probabilistic Timed Automata
- 中文标题：mcpta：面向概率定时自动机的 Modest-PRISM 检查路线
- 作者：Arnd Hartmanns，Holger Hermanns
- 发表：*2009 Sixth International Conference on the Quantitative Evaluation of Systems*，pp. 187-196，2009
- DOI：`10.1109/QEST.2009.41`
- 链接：https://doi.org/10.1109/QEST.2009.41
- 形式主义：`Probabilistic Timed Automata / Modest / mcpta`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`Modest` 到 `PRISM` 的 `PTA` 自动模型检查路线
- 工具/实现获取方式：原文把 `mcpta` 描述为依托 `Modest` 与 `PRISM` 的自动工具路线，并给出 `http://www.modestchecker.net/` 作为相关获取入口；正文未单列独立仓库。
- 标准/格式获取方式：输入承载是 `Modest` 进程描述，内部落到 `VPTA/PTA`，输出承载是 `PRISM` guarded-command modules 与 property files。

## 简报

这篇论文的核心贡献，不是再定义一个新的 `PTA` 变体，而是把“高层 `Modest` 建模 + `PTA` 语义 + `PRISM` 后端”真正串成一条自动化检查链。`mcpta` 允许用户在 `Modest` 中写带异常处理、有限递归和受限动态并行的模型，再通过 digital-clocks 语义把它翻译成 `PRISM` 可以求解的同步概率自动机集合。

- 形式主义定位：`PTA` 的自动模型检查方法与工具链，不是新的状态机本体。
- 构造方式简述：`Modest` 过程先按操作语义落成 `STA/VPTA`，再经 integral-time / digital-clocks 约化与模块化翻译生成 `PRISM` modules。
- 基础设施与场景简述：依托 `Modest` 前端、`mcpta` 翻译器与 `PRISM` 后端，服务概率实时协议、调度和嵌入式控制分析。

```text
Modest processes -> STA / VPTA -> closed diagonal-free PTA fragment -> PRISM modules + property file -> probabilistic / expected reachability
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 概率定时自动机 `PTA`。
2. `Modest` 高层组合式建模语言。
3. `STA/VPTA` 作为 `Modest` 操作语义中间层。
4. digital-clocks / integral-time 语义。
5. `PRISM` guarded-command modules 与 reachability checking。

### 核心抽象

论文直接采用的 `PTA` 语法可整理为：

$$
A = (L, l_0, X, \Sigma, inv, prob)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `l_0` 是初始 location。
3. `X` 是有限时钟集合。
4. `\Sigma` 是动作集合。
5. `inv : L \to CC(X)` 给每个 location 一个 invariant。
6. `prob \subseteq L \times CC(X) \times \Sigma \times Dist(2^X \times L)` 是概率边关系。

其中论文对边关系给出的关键部分可以直接写成：

$$
prob \subseteq L \times CC(X) \times \Sigma \times Dist(2^X \times L)
$$

上式中的符号逐项解释如下：

1. `CC(X)` 是时钟约束集合。
2. `Dist(2^X \times L)` 是“要重置的时钟集合 + 目标 location”上的离散概率分布。
3. 一条边不仅包含 guard 和 action，还包含概率化的 reset/跳转目标。

论文还明确给出离散概率分布的记号：

$$
\mu : Q \to [0,1], \quad \sum_{q \in Q} \mu(q) = 1
$$

上式中的符号逐项解释如下：

1. `Q` 是某个可数状态集。
2. `\mu(q)` 是元素 `q` 的概率。
3. 求和为 `1` 表示它是合法的离散概率分布。

从工具链角度，可把 `mcpta` 的核心路线保守整理为：

$$
\mathrm{mcpta} = (\mathcal{L}_{Modest}, \mathcal{T}_{STA/VPTA}, \mathcal{D}_{clk}, \mathcal{B}_{PRISM})
$$

上式中的符号逐项解释如下：

1. `\mathcal{L}_{Modest}` 是输入建模语言层。
2. `\mathcal{T}_{STA/VPTA}` 是 `Modest` 的中间语义层。
3. `\mathcal{D}_{clk}` 是 digital-clocks / integral-time 离散化层。
4. `\mathcal{B}_{PRISM}` 是 `PRISM` 后端。
5. 这是根据论文工具流程做的保守归纳，不是原文显式统一元组。

### 一个最小例子与通俗解释

论文第一页给了一个很典型的通信小例子：`SEND / WAIT / DONE / FAIL` 四个 location 用一个时钟 `c` 描述重传场景。

1. 系统先发送消息并进入等待状态。
2. 传输延迟在 `1` 到 `3` 个时间单位之间。
3. 通道以 `1/100` 的概率丢消息，以 `99/100` 的概率成功传送。
4. 超时后可以重试，最终要么成功，要么进入失败状态。

通俗地说，普通 `TA` 只能表达“什么时候允许等、什么时候必须跳”；`PTA` 进一步表达“跳过去以后哪种结果出现的概率是多少”。`mcpta` 做的事，就是把这种带时间和概率的模型，用 `Modest` 写出来，再自动变成 `PRISM` 吃得下的形式。

### 运行 / 接受 / 转移语义

论文把 `PTA` 的运行语义放到 probabilistic timed structure 上。对一条边 `(l,g,a,\mu)` 来说：

1. 当前 location 必须是 `l`。
2. 当前时钟赋值必须满足 guard `g`。
3. 触发 action `a` 后，按分布 `\mu` 选择目标 location 和 reset 集。
4. 目标 location 的 invariant 必须在跳转后仍成立。

从工具角度，关键不是直接做 zone-based symbolic checking，而是采用 digital clocks 语义，把连续时钟改写成有界整数变量，从而让 `PRISM` 直接做后端求解。

### 语义边界

这条路线的边界在论文中写得很清楚：

1. digital-clocks 方法只覆盖 closed、diagonal-free 的 `PTA` 片段。
2. `Modest` 的连续分布不在本工具支持范围内。
3. 递归和动态并行只支持有限、受限的形式。
4. 重点性质是 probabilistic reachability 和 expected reachability，不是完整 `PTCTL`。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PTA` 元组 | `$A = (L, l_0, X, \Sigma, inv, prob)$` | 工具面向的核心模型对象。 |
| 概率边 | `$prob \subseteq L \times CC(X) \times \Sigma \times Dist(2^X \times L)$` | 每条边同时携带 guard、action、reset 与概率目标。 |
| 分布定义 | `$\mu : Q \to [0,1],\ \sum_{q \in Q}\mu(q)=1$` | 离散概率选择的基本语义。 |
| 工具路线 | `$\mathrm{mcpta} = (\mathcal{L}_{Modest}, \mathcal{T}_{STA/VPTA}, \mathcal{D}_{clk}, \mathcal{B}_{PRISM})$` | `Modest -> PTA-like semantics -> PRISM` 的自动链路。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 以 location-based `PTA` 为核心。 |
| 事件 / 触发 | 中等支持 | 动作标签和同步动作明确，但主体仍是验证路线。 |
| 守卫 / 数据 | 强支持 | 时钟约束、离散变量和有限分布都可进入模型。 |
| 层次 | 弱支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 中等到强 | `Modest` 组合与 `PRISM` 静态并行都可表达并发。 |
| 时间约束 | 很强 | 核心就是概率 + 实时时钟。 |
| 连续动态 / 随机性 | 随机性强，连续动态不支持 | 支持离散概率，不支持混成连续动力学。 |
| 可执行 / 可验证性 | 很强 | 目标就是自动 reachability checking。 |

### 形式化问题与性质

1. 论文的主问题是：怎样把 `Modest` 的高层描述自动压到 `PRISM` 可接受的 `PTA` 数字时钟表示。
2. 相比理论论文，它最关键的价值在于“自动化”和“前端表达力”。
3. 相比纯工具平台论文，它又明显带有方法论色彩，因为 digital-clocks 约化和模块翻译是核心内容。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. 用 `Modest` 写 process、loop、parallel composition、受限递归和异常处理。
2. 由操作语义先得到 `STA`。
3. 再约束到 `VPTA/PTA` 片段。
4. 最终生成 `PRISM` guarded-command modules。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Modest` 文本模型。
2. `STA/VPTA` 语义中间层。
3. digital-clocks 下的 bounded integer variables。
4. `PRISM` modules 与 properties 文件。

### 交换与互操作

互操作重点在于：

1. `Modest` 前端与 `PRISM` 后端之间的自动翻译。
2. `PRISM` 的模块同步机制与 `Modest` 并发构造的对应。
3. 原有 `PRISM` 生态可直接复用到 `PTA` 片段。

## 配套基础设施

- 建模/编辑工具：`Modest` 语言与其建模环境。
- 解析/交换/元模型支持：`mcpta` 把 `Modest` 自动翻译为 `PRISM` modules。
- 仿真/执行支持：论文主线不是运行时仿真，而是 `PRISM` 后端分析。
- 验证/分析支持：`PRISM` 负责 probabilistic / expected reachability checking。
- 代码生成/转换支持：核心是 `Modest -> PRISM` 翻译，不是部署代码生成。
- 标准化或社区生态：依托 `Modest` 与 `PRISM`，并与后来的 `Modest Toolset` quantitative 生态直接相连。

## 适用场景与需求前提

### 适用场景

适合带概率超时、重传、调度和实时约束的协议与嵌入式系统分析，尤其适合已经在 `Modest` 或类似高层组合语言中描述系统，但又希望落到自动模型检查后端上的场景。

### 需求前提

1. 模型能被收束到 closed、diagonal-free `PTA` 片段。
2. 时间约束可接受 digital-clocks 的整数化表达。
3. 随机性主要是离散概率，而不是连续分布或混成噪声。
4. 关心的性质主要是 reachability 概率或期望代价。

### 不适用或高成本场景

如果模型 heavily 依赖连续概率分布、一般递归或复杂动态并行，这条路线就会超出论文支持边界。

## 与相邻形式主义的关系

相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，它不是直接扩展 `PRISM` 输入语言，而是给 `PRISM` 增加一个更高层的 `Modest` 前端；相对 [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)，它更早、更聚焦在 `PTA` 与 digital clocks；相对 [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)，它走的是离散化后端精确求解路线，而不是统计模型检查。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果未来状态机输出需要进入概率实时验证链，LLM 不一定要直接生成低层 `PRISM`，也可以先生成更接近工程建模的高层文本，再经自动翻译进入求解器。

### 作为目标形式主义还是中间表示

更像中间表示与验证桥接路线，而不是最终交付给工程团队的统一状态机格式。

### 对需求到模型生成的启发

1. “高层可写 + 后端可证”之间需要明确的翻译层。
2. 时间、概率与并发一旦同时出现，直接把最终求解格式暴露给用户并不友好。
3. 如果后续要做生成-验证闭环，`Modest` 这样的前端比直接手写 `PRISM` 更适合自动生成。

### 现实限制

它依赖受限的 `PTA` 片段和 digital-clocks 假设，因此不应被误读成“所有概率实时模型都能自动平移到 `PRISM`”。

## 重要的相关工作

1. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：概率实时模型检查平台主线。
2. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：`Modest` 后续整合工作台。
3. [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)：另一条概率实时分析路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Probabilistic Timed Automata / Modest / mcpta`
- 归类理由：主贡献是 `Modest -> PTA -> PRISM` 的自动模型检查方法与工具链，不是新的状态机本体。
