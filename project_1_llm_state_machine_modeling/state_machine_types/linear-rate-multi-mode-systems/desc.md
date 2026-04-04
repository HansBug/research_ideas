# 线性速率多模态系统最优调度 / Optimal Scheduling for Linear-Rate Multi-Mode Systems

## 基本信息

- 标题：Optimal Scheduling for Linear-Rate Multi-Mode Systems
- 中文标题：线性速率多模态系统最优调度
- 作者：Dominik Wojtczak
- 发表：*Formal Modeling and Analysis of Timed Systems*, pp. 258-273, 2013
- DOI：`10.1007/978-3-642-40229-6_18`
- 链接：https://arxiv.org/pdf/1302.4406.pdf
- 形式主义：`Linear-Rate Multi-Mode Systems (LRMMS)`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立工具；机器可处理入口是 `H=(M,N,A,B)` 元组、safe controller 语义、implementable frequency vector 与 peak/average/weighted cost optimization。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 per-mode 线性微分方程、hyperrectangular safe set 和 periodic controller construction。

## 简报

这篇论文把 `multi-mode hybrid` 从“常速率平移”推进到了“线性收敛动力学”。在 `LRMMS` 中，每个 mode 不再只给一个 constant rate vector，而是给一组线性微分方程系数；系统在该 mode 内会朝某个 equilibrium 指数式靠近。这样一来，它既保留了 `multi-mode switching` 的结构，又比 `CMS` 更贴近实际温控和资源调节系统。

- 形式主义定位：`Hybrid Automata` 下的线性速率 multi-mode 子类，是 `CMS` 的相邻 sibling 而非简单子类。
- 构造方式简述：给每个 mode 配置一组独立坐标上的一阶线性方程，再寻找保证安全的非 Zeno controller。
- 基础设施与场景简述：核心基础设施是 implementable frequency vectors、periodic safe controllers，以及 peak/average/weighted cost optimization。

```text
multi-mode hybrid control -> per-mode linear ODE -> safe controller synthesis -> LRMMS -> optimal control over safe switching
```

## 形式主义定义与核心对象

### 定义对象

`LRMMS` 面向的是这样一类系统：每个 mode 内连续变量都按“朝某个平衡点衰减或逼近”的规律演化，而不是简单匀速漂移。相比 `CMS`，这一步显著增强了物理拟合能力；相比一般 `HA`，它又依然保留了足够规整的 per-mode dynamics。

### 核心抽象

原文 Definition 1 把模型写成：

$$
H = (M,N,A,B)
$$

上式中的符号逐项解释如下：

1. `M` 是有限非空的 mode 集合。
2. `N` 是连续变量个数。
3. `A : M \to \mathbb R_{>0}^N` 给每个 mode 提供衰减系数向量。
4. `B : M \to \mathbb R^N` 给每个 mode 提供驱动常数项。

由原文微分方程可整理出，在 controller 令系统停留于 mode `m` 时：

$$
\dot{x}(t)=B(m)-\mathrm{diag}(A(m))x(t)
$$

上式中的符号逐项解释如下：

1. `x(t)\in\mathbb R^N` 是连续状态。
2. `\mathrm{diag}(A(m))` 是由 `A(m)` 形成的对角矩阵。
3. 每个坐标都独立地朝 `b_i^m/a_i^m` 这个平衡值收敛。

### 一个最小例子与通俗解释

一个直觉例子是“两间房 + 一个只能在不同送风配置之间切换的温控系统”：

1. 在 mode `m_1` 下，房间 1 被加热、房间 2 缓慢回到室外温度；
2. 在 mode `m_2` 下，角色对换；
3. 若一直停在单一 mode，每个房间会指数式收敛到该 mode 的 equilibrium；
4. 只有不断在这些 mode 之间切换，系统才可能始终停在 comfort box 内。

通俗地说，`LRMMS` 像“每个 mode 都带一个自己的温度吸引点”，而 controller 的任务是不断切换这些吸引点，让整体轨迹始终被困在安全盒子里。

### 运行 / 接受 / 转移语义

原文给出：若系统在 mode `m` 中持续 `t` 时间，则每个变量满足闭式解

$$
x_i(t_0+t)=\frac{b_i^m}{a_i^m}+\left(x_i(t_0)-\frac{b_i^m}{a_i^m}\right)e^{-a_i^m t}
$$

上式中的符号逐项解释如下：

1. `a_i^m` 和 `b_i^m` 分别是 mode `m` 下第 `i` 个变量的线性系数和常数项。
2. `b_i^m/a_i^m` 是该 mode 的 equilibrium。
3. 指数项说明状态会单调地朝 equilibrium 逼近。

原文把 controller 定义为 timed actions 序列：

$$
s=\langle (m_1,t_1),(m_2,t_2),\ldots\rangle
$$

并要求它至少是 non-Zeno；若最小 dwell time 为正，则称为 feasible。

### 语义边界

`LRMMS` 和 `CMS` 的关系不是简单“更强 / 更弱”单调链。原文明确指出：`CMS` 是“每个变量在 mode 内按常速率平移”，而 `LRMMS` 是“每个变量在 mode 内按线性方程向 equilibrium 收敛”，两者是不同的 modeling axis。它们共享 multi-mode skeleton，但连续动力学语义不同。

### 关键性质与判定边界

原文的核心决策问题可写成：

$$
\text{Given } H,S,x_0,\ \text{decide whether there exists a feasible } S\text{-safe controller}
$$

作者证明：

$$
\text{If a safe controller exists, then a periodic safe controller exists}
$$

并进一步给出多项式时间算法来构造 safe controller，以及在加入 per-mode costs 后求解 peak cost、average cost 与 weighted cost 最优控制。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限 modes 是模型骨架。 |
| 事件 / 触发 | 弱支持 | 切换由 controller 选定，不依赖外部事件逻辑。 |
| 守卫 / 数据 | 不支持显式 guard | tractable family 聚焦 mode 选择，不引入一般 hybrid guards。 |
| 层次 | 不支持 | 原始模型是平坦 multi-mode system。 |
| 并发 / 同步 | 不支持显式并发 | 多变量共享 mode，但各坐标的流是独立线性方程。 |
| 时间约束 | 强支持 | dwell time 与最小 dwell time 是核心。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 每个 mode 内是线性稳定 ODE。 |
| 可执行 / 可验证性 | 强理论支持 | safe controllability 与多种 optimal control 问题都有算法。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$H=(M,N,A,B)$` | 把每个 mode 的线性动力学参数显式化。 |
| mode 动力学 | `$\dot{x}(t)=B(m)-\mathrm{diag}(A(m))x(t)$` | 每个 mode 都对应一个稳定线性系统。 |
| 闭式解 | `$x_i(t_0+t)=\frac{b_i^m}{a_i^m}+\left(x_i(t_0)-\frac{b_i^m}{a_i^m}\right)e^{-a_i^m t}$` | 解释了为何 hyperrectangle safety 可被 controller 利用。 |
| 可行控制 | `$\exists$ feasible $S$-safe controller` | 核心判定问题。 |
| 优化目标 | peak / average / weighted cost | 说明这条 family 不只可判，还便于最优控制。 |

## 构造方式与承载格式

### 建模入口

建模时通常先决定：

1. mode 集合有哪些；
2. 每个 mode 对每个变量的线性系数 `a_i^m,b_i^m`；
3. safe set 是否能压成 hyperrectangle；
4. 目标是只求安全，还是还要最优 cost。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. `H=(M,N,A,B)` 元组；
2. timed controller 序列；
3. hyperrectangular safe set；
4. implementable frequency vectors 与 cost LP。

### 交换与互操作

它与以下条目关系最紧：

1. [optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md](../optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md)
2. [safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md](../safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md)
3. 一般 `switched linear systems` 与 `Hybrid Automata`

其中 `CMS` 关注 constant-rate translation，`LRMMS` 则关注线性收敛 dynamics。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 implementable frequency vector、periodic controller 与 cost minimization framework。
- 仿真/执行支持：按每个 mode 的闭式解直接数值执行即可。
- 验证/分析支持：safe controllability、minimum peak cost、minimum average cost、weighted optimization。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 switched linear / hybrid optimal control 与 multi-mode scheduling 的理论分支。

## 适用场景与需求前提

### 适用场景

适合那些：

1. 每个 mode 内连续量会稳定地朝某个 equilibrium 演化；
2. 系统主控接口是切换 mode 而不是连续反馈律；
3. 安全约束可以压成 hyperrectangle。

### 需求前提

1. 每个坐标在固定 mode 内应近似 obey 一阶线性动力学。
2. 起始点最好位于 safe set 内部。
3. 需要的是 mode-level safe controller，而不是一般非线性 hybrid policy。

### 不适用或高成本场景

若动力学存在强耦合、非线性项、guard/reset 依赖或不确定 rate sets，则应改用一般 `HA` 或 `BMS` 一类模型。

## 与相邻形式主义的关系

相对 `CMS`，它不是常速率平移，而是线性收敛；相对 `BMS`，它强调确定线性 dynamics 而不是对抗不确定速率；相对一般 `Hybrid Automata`，它显著更弱，但更适合直接做 safe/optimal mode scheduling。

## 与本研究的关系

### 对 Project 1 的价值

它让 `Hybrid Automata` 分支下的 `multi-mode` 方向不再只有 constant-rate family，还长出了一条线性收敛 sibling，有助于后续把控制需求按动力学复杂度分层。

### 作为目标形式主义还是中间表示

对温控、资源分配、负载切换这类系统，它既可以做理论目标形式主义，也可以作为从自然语言需求走向更一般 hybrid 模型前的结构化中间表示。

### 对需求到模型生成的启发

当需求隐含“每种模式下系统会朝固定平衡态回归”的语义时，LLM 生成 `LRMMS` 往往比生成一般 `HA` 更稳，也比强行套成 `CMS` 更真实。

## 重要的相关工作

### 奠基或前身工作

- 一般 `Hybrid Automata`
- switched linear systems

### 同类型或同家族工作

- [optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md](../optimal-scheduling-for-constant-rate-multi-mode-systems/desc.md)
- [safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md](../safe-schedulability-of-bounded-rate-multi-mode-systems/desc.md)

### 标准 / 格式 / 工具链工作

- 原文没有工程标准；最重要的基础设施是 frequency-vector reasoning 和 cost optimization pipeline。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Hybrid Automata -> Linear-Rate Multi-Mode Systems`，并与 `Constant-Rate Multi-Mode Systems` 保持 sibling 关系。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
