# 有界速率多模态系统的安全可调度性 / Safe Schedulability of Bounded-Rate Multi-Mode Systems

## 基本信息

- 标题：Safe Schedulability of Bounded-Rate Multi-Mode Systems
- 中文标题：有界速率多模态系统的安全可调度性
- 作者：Rajeev Alur、Vojtěch Forejt、Salar Moarref、Ashutosh Trivedi
- 发表：*Proceedings of the 16th ACM International Conference on Hybrid Systems: Computation and Control*, pp. 243-252, 2013
- DOI：`10.1145/2461328.2461366`
- 链接：https://www.cis.upenn.edu/~alur/Hscc13.pdf
- 形式主义：`Bounded-Rate Multi-Mode Systems (BMS)`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立实现；机器可处理入口是 `H=(M,n,R)` 元组、scheduler/environment 双人博弈语义、extreme-rate reduction 和 `H-closed polytope` 判定框架。
- 标准/格式获取方式：原文没有 DSL / 交换标准，核心承载方式是 convex rate sets、safe polytope 和 strategy semantics。

## 简报

`BMS` 是对 `CMS` 的自然但关键的推广：在 `CMS` 里，一个 mode 只有一个固定 rate vector；在 `BMS` 里，一个 mode 只给出一个有界 rate-set，而真正的 rate vector 由环境在运行时选。于是问题不再是“是否存在安全 schedule”，而变成“scheduler 是否有 winning strategy，能对抗任何允许的环境扰动”。这一步把 `multi-mode hybrid scheduling` 从确定模型推进到了博弈式鲁棒模型。

- 形式主义定位：`CMS` 的不确定速率 / 对抗环境推广。
- 构造方式简述：scheduler 先选 `(mode, time)`，environment 再从该 mode 的 convex rate polytope 中选具体 `\vec r`。
- 基础设施与场景简述：核心基础设施是 game semantics、extreme-rate characterization、`H-closed polytope` 和 complexity split。

```text
constant-rate MMS -> uncertain rate-set per mode -> scheduler vs environment game -> BMS -> robust schedulability
```

## 形式主义定义与核心对象

### 定义对象

`BMS` 关心的不是单条连续轨迹，而是“在每一步 mode 切换后，环境还会怎么选具体速率”。因此它的核心对象是一个两层结构：

1. mode 切换权在 scheduler；
2. mode 内具体速率选择权在 environment。

这种建模把 uncertainty 明确外显成 game，而不是藏进“扰动项”或最坏情况注释里。

### 核心抽象

原文 Definition 1 先给出一般 multi-mode system：

$$
H=(M,n,R)
$$

上式中的符号逐项解释如下：

1. `M` 是有限非空的 mode 集合。
2. `n` 是连续变量个数。
3. `R : M \to 2^{\mathbb R^n}` 给每个 mode 赋一个 rate set。

`BMS` 则是其中每个 `R(m)` 都是 convex polytope 的特殊情况。对一次有限运行：

$$
\rho=\langle x_0,(m_1,t_1,\vec r_1),x_1,\ldots,(m_k,t_k,\vec r_k),x_k\rangle
$$

状态更新满足：

$$
x_i = x_{i-1} + t_i \cdot \vec r_i,\qquad \vec r_i \in R(m_i)
$$

### 一个最小例子与通俗解释

还是 HVAC 直觉，但这次每个 mode 的“升温 / 降温速度”不再固定：

1. scheduler 决定“现在开冷却模式并维持 5 秒”；
2. environment 决定“这 5 秒里真实降温速度是这个 mode 允许区间中的哪一个向量”；
3. 如果 scheduler 不管环境怎样选，都能把状态保持在 safe set 内，那么它就赢了。

通俗地说，`BMS` 像“mode switch 由控制器选，但每个 mode 的实际动力学由对手在允许范围内挑”。它把鲁棒安全控制直接压成了一个 mode-level game。

### 运行 / 接受 / 转移语义

原文把 `BMS` 的语义正式写成一个 turn-based two-player game。scheduler 的策略是：

$$
\sigma : FRuns \to M \times \mathbb R_{\ge 0}
$$

environment 的策略是：

$$
\pi : FRuns \times (M \times \mathbb R_{\ge 0}) \to \mathbb R^n
$$

上式中的符号逐项解释如下：

1. `FRuns` 是当前历史运行前缀集合。
2. `\sigma` 根据历史给出下一步 `(mode,time)`。
3. `\pi` 在看到 scheduler 的选择后，返回该 mode 中允许的具体速率向量。

因此，从起始状态 `x_0` 出发的结果 run 记为：

$$
Run(x_0,\sigma,\pi)
$$

而 safe schedulability 问题就是问：

$$
\exists \sigma\ \forall \pi,\ Run(x_0,\sigma,\pi)\in W^{S}_{Safe}
$$

### 语义边界

相对 `CMS`，这里新增的不只是 uncertainty，而是“对手选择 uncertainty”的 game semantics。原文还区分了：

1. static scheduler strategy：不观察 environment 之前的选项；
2. dynamic scheduler strategy：可根据历史观察结果自适应。

作者明确给出反例说明：在 `BMS` 里 static strategy 可能不够，而 dynamic strategy 可以赢。

### 关键性质与判定边界

原文的代表性结论包括：

$$
\text{Schedulability games on BMS are determined}
$$

以及复杂度边界：

$$
\text{Schedulability(BMS) is coNP-complete}
$$

并且在二维变量情形下进一步收紧到：

$$
n=2 \Rightarrow \text{schedulability is in PTIME}
$$

如果再要求 scheduler 只能在离散 clock period 的整数倍时刻切换，则问题升到 `EXPTIME`-complete。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 modes 仍是模型骨架。 |
| 事件 / 触发 | 弱支持 | 切换由 scheduler 决策，不依赖外部离散事件语义。 |
| 守卫 / 数据 | 不支持显式 guard | 原始 family 的关键在 rate uncertainty，而不是 transition guards。 |
| 层次 | 不支持 | 原始模型是平坦 game graph。 |
| 并发 / 同步 | 不支持显式并发 | 多变量通过共享 mode 与 rate set 共同演化。 |
| 时间约束 | 强支持 | time duration 是 scheduler 动作的一部分。 |
| 连续动态 / 随机性 | 强支持连续、无概率 | 是对抗性不确定速率，不是随机过程。 |
| 可执行 / 可验证性 | 强理论支持 | game determinacy、coNP / PTIME / EXPTIME 边界都明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$H=(M,n,R)$` | 在每个 mode 中保留一个 rate polytope。 |
| 状态更新 | `$x_i=x_{i-1}+t_i\vec r_i$` | 具体速率由 environment 选取。 |
| scheduler 策略 | `$\sigma:FRuns\to M\times\mathbb R_{\ge 0}$` | 控制器先选 mode 和 dwell time。 |
| environment 策略 | `$\pi:FRuns\times(M\times\mathbb R_{\ge 0})\to\mathbb R^n$` | 对手再选具体速率。 |
| 复杂度 | `coNP-complete`, `PTIME` for 2 vars | 给鲁棒 multi-mode branch 一个稳定复杂度定位。 |

## 构造方式与承载格式

### 建模入口

建模时通常先决定：

1. mode 集合有哪些；
2. 每个 mode 的可允许速率集合是否能压成 convex polytope；
3. 安全集是否可写成 convex polytope；
4. scheduler 能否观察环境历史。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. rate-set polytopes；
2. two-player strategy semantics；
3. extreme-rate reduction；
4. `H-closed polytope` 判断和离散 period 变体。

### 交换与互操作

它与以下 family 的关系最直接：

1. [optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md](../optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md) 的确定型母类；
2. `multi-rate multi-mode systems (MMS)`；
3. 需要鲁棒保障的 green scheduling / uncertain hybrid control 场景。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 convex polytope、extreme-rate enumeration 和 strategy semantics。
- 仿真/执行支持：可以直接按 scheduler / environment 交替动作执行。
- 验证/分析支持：determinacy、coNP characterization、二维特例、离散 period 变体。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 robust multi-mode hybrid scheduling 的理论母型。

## 适用场景与需求前提

### 适用场景

适合那些：

1. 模式切换是主控制接口；
2. 每个 mode 的动力学存在确定有界的不确定性；
3. 需要回答“在最坏环境下还能否保证安全”。

### 需求前提

1. 不确定性最好能压成每个 mode 的 convex rate polytope。
2. 安全集最好可压成 convex polytope。
3. 问题更像鲁棒调度 / 安全控制，而不是一般 hybrid reachability。

### 不适用或高成本场景

若 uncertainty 不是 mode-local bounded rate，而是复杂非线性扰动、随机噪声或必须配合 guard/reset 结构，则 `BMS` 会过于简化。

## 与相邻形式主义的关系

相对 `CMS`，`BMS` 把单个 rate vector 放宽成 rate set 并引入 adversarial semantics；相对一般 hybrid games，它又保留了足够规整的几何结构，使 schedulability 还能被精确分析；相对 `LRMMS`，它强调的是不确定 constant rate，而不是指数式线性收敛。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Hybrid Automata` 分支进一步从“确定 multi-mode”推进到“鲁棒 multi-mode”节点，使演化树能清楚地区分 deterministic 与 adversarial 两类可调度 family。

### 作为目标形式主义还是中间表示

更适合作为鲁棒控制 / 最坏情况验证的中间表示或目标理论模型，而不是直接面向工程师的执行规范。

### 对需求到模型生成的启发

当需求里反复出现“环境扰动”“速率区间”“无论外界怎样变化都必须安全”时，LLM 应倾向于生成 `BMS` 一类 scheduler-vs-environment 模型，而不是普通 `CMS`。

## 重要的相关工作

### 奠基或前身工作

- [optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md](../optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md)

### 同类型或同家族工作

- `Multi-rate Multi-Mode Systems`
- [linear-rate-multi-mode-systems/desc.md](../linear-rate-multi-mode-systems/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准；最重要的基础设施是 `H-closed polytope` 和 extreme-rate reasoning。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Hybrid Automata -> Singular / Constant-Rate Hybrid 支线 -> Constant-Rate Multi-Mode Systems -> Bounded-Rate Multi-Mode Systems`。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
