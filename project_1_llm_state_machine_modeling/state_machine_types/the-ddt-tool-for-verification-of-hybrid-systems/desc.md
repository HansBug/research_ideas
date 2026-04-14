# d/dt：混成系统验证工具 / The d/dt Tool for Verification of Hybrid Systems

## 基本信息

- 标题：The d/dt Tool for Verification of Hybrid Systems
- 中文标题：d/dt：混成系统验证工具
- 作者：Eugene Asarin，Thao Dang，Oded Maler
- 发表：*Computer Aided Verification*，pp. 365-370，2002
- DOI：`10.1007/3-540-45657-0_30`
- 链接：https://link.springer.com/content/pdf/10.1007/3-540-45657-0_30.pdf
- 形式主义：`Hybrid Automata / d/dt`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：hybrid reachability verifier / switching-controller synthesizer
- 工具/实现获取方式：原文详细说明实现依赖 `cdd`、`Qhull`、`Cubes` 与 `Geomview`，但没有给出独立公开下载入口。
- 标准/格式获取方式：输入承载是带线性 staying conditions、guards 与 affine resets 的 `Hybrid Automata`；原文未给中立交换标准。

## 简报

这篇论文的重点，是把混成系统 reachability 从 `HyTech` 的线性混成自动机继续往前推到“线性连续动力学 + uncertain input”的可验证工具链。`d/dt` 不只做 safety checking，还显式支持 switching-controller synthesis；它通过 step-by-step over-approximation、convex polyhedra 与 orthogonal polyhedra，把连续可达集压成可计算对象。

- 形式主义定位：面向 `Hybrid Automata` 的 reachability verification / controller synthesis 工具，而不是新的混成自动机本体。
- 构造方式简述：输入离散 modes、线性连续动力学、invariants、guards 与 resets，工具内部围绕 convex/orthogonal polyhedra、time-successor 与 predecessor 计算。
- 基础设施与场景简述：依托 `cdd`、`Qhull`、`Cubes`、`Geomview` 与 step-based reachability，服务 platoon longitudinal control、biped leg、bacterial quorum-sensing 等混成安全分析。

```text
hybrid model -> convex polyhedral reachability step -> orthogonal over-approximation -> safety check / switching-controller synthesis
```

## 形式主义定义与核心对象

### 定义对象

论文把 `d/dt` 的工作对象固定为一类 `Hybrid Automata`：

1. 离散状态 `q`。
2. 连续状态向量 `x \in \mathbb{R}^n`。
3. 线性连续动力学与 uncertain input。
4. 线性 invariant 与 transition guard。
5. affine set-valued reset。

### 核心抽象

论文明确假设连续动力学为：

$$
\dot{x} = Ax + Bu, \quad u \in U
$$

上式中的符号逐项解释如下：

1. `x` 是连续状态向量。
2. `A` 是线性系统矩阵。
3. `B` 是输入矩阵。
4. `u` 是不确定输入。
5. `U` 是凸多面体形式的有界输入集合。

离散跳转的 reset 则写成：

$$
R(x) = Dx + J
$$

上式中的符号逐项解释如下：

1. `D` 是 affine reset 的线性部分。
2. `J` 是凸多面体形式的偏移集合。
3. `R(x)` 因而是 set-valued affine map。

论文把 symbolic states 写成 `(q,F)`，其中 `q` 是离散 location，`F \subseteq \mathbb{R}^n` 是连续状态区域。对每个 time step `r`，工具按区间 `[kr,(k+1)r]` 迭代，计算这一时间段内的 over-approximation。

### 一个最小例子与通俗解释

可以把论文的方法直观理解成这样：

1. 某个 location 里，系统按 `\dot{x} = Ax + Bu` 连续演化。
2. 因为 `u` 不是单值，而是落在集合 `U` 中，所以真正可达集是一整片区域，不是一条轨迹。
3. `d/dt` 先算出一步时间内这片区域的 convex over-approximation，再把结果塞进更便于累积存储的 orthogonal polyhedra。
4. 如果这片区域碰到 bad set，就说明安全性可能被破坏；如果要做 controller synthesis，就反过来找还能保证永远不出界的 states。

通俗地说，`d/dt` 像“拿几何块去包住混成系统未来所有可能走向”的工具。它关心的是“整片可能区域会不会撞线”，而不是某条仿真轨迹。

### 运行 / 接受 / 转移语义

论文首先把 reachability 看成 hybrid configuration 的集合演化：全局配置是 `(q,x)`，符号状态是 `(q,F)`。对纯线性系统 `\dot{x}=Ax`，给定初始多面体 `F`，时刻 `r` 的可达集记为 `F_r`，并先构造：

$$
C = \mathrm{conv}(F \cup F_r)
$$

上式中的符号逐项解释如下：

1. `F` 是初始 convex polyhedron。
2. `F_r` 是经过时间 `r` 后的连续后继集合。
3. `\mathrm{conv}` 表示凸包。
4. `C` 是一步连续演化的中间 over-approximation。

控制器综合依赖 one-step predecessor operator，可保守写成：

$$
W_{k+1} = W_k \cap \pi(W_k)
$$

上式中的符号逐项解释如下：

1. `W_k` 是第 `k` 轮仍被认为安全的状态集合。
2. `\pi(W_k)` 是一步之内还能保持在 `W_k` 中的前驱状态。
3. 迭代删去不再安全的 states，最后得到 maximal invariant set 的 under-approximation。

### 语义边界

这篇论文的边界很明确：

1. 主体面向 linear continuous dynamics with uncertain input。
2. invariant 与 guards 都默认是线性不等式的合取。
3. reset 需要是 affine set-valued map。
4. 对一般非线性动力学，本文只说已有更一般方法，当前工具实现重点仍是线性类。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 连续动力学 | `$\dot{x} = Ax + Bu,\ u \in U$` | `d/dt` 的核心连续模型。 |
| affine reset | `$R(x) = Dx + J$` | 离散跳转后的集合更新。 |
| 一步凸包近似 | `$C = \mathrm{conv}(F \cup F_r)$` | 连续可达集 over-approximation 的骨架。 |
| 安全集迭代 | `$W_{k+1} = W_k \cap \pi(W_k)$` | switching-controller synthesis 的核心思路。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `Hybrid Automata` 的离散 location 是主骨架。 |
| 事件 / 触发 | 强支持 | 离散 transitions、guards 与 resets 明确存在。 |
| 守卫 / 数据 | 很强 | 线性不等式与 affine reset 是一等对象。 |
| 层次 | 不支持 | 论文不讨论 hierarchy。 |
| 并发 / 同步 | 弱支持 | 主体是单 automaton reachability，不在并发接口语义。 |
| 时间约束 | 很强 | 连续时间演化是核心。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 支持 uncertain input，但不是概率模型。 |
| 可执行 / 可验证性 | 很强 | safety verification 与 controller synthesis 都直接实现。 |

### 形式化问题与性质

1. `d/dt` 的独特点不是单纯 over-approx reachability，而是把 controller synthesis 一起纳入同一工具骨架。
2. 论文刻意用 orthogonal polyhedra 存储 reachable sets，是为了避免一般 polyhedra union 在高维下过于难管。
3. 对 uncertain input 的处理依赖 Maximum Principle 来推动 faces，而不是只做点采样。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 写 discrete states 与连续变量。
2. 为每个 mode 指定线性连续动力学。
3. 写线性 staying conditions 与 transition guards。
4. 为离散跳转补 affine reset。
5. 设定 time step 与 orthogonal approximation granularity。

### 机器可处理承载方式

机器可处理承载方式包括：

1. hybrid automaton 输入。
2. convex polyhedra。
3. orthogonal polyhedra。
4. 用户可调的 approximation parameters。

### 交换与互操作

这篇论文的互操作重点不在开放标准，而在实现层拼装：

1. `cdd` / `Qhull` 负责常规 convex polyhedra 操作。
2. `Cubes` 负责 orthogonal polyhedra。
3. `Geomview` 用于运行时三维可视化。

## 配套基础设施

- 建模/编辑工具：原文未描述独立 GUI，主体是 reachability / synthesis tool 本体。
- 解析/交换/元模型支持：输入是 hybrid automaton；无中立交换标准。
- 仿真/执行支持：更偏 reachable-set evolution，而非高保真数值仿真器。
- 验证/分析支持：reachability、safety checking、switching-controller synthesis。
- 代码生成/转换支持：原文未涉及代码生成。
- 标准化或社区生态：`cdd`、`Qhull`、`Cubes` 与 `Geomview` 是文中明确给出的实现依赖。

## 适用场景与需求前提

### 适用场景

适合线性或可线性化的混成控制对象，尤其是需要 safety verification 或 mode-switching controller synthesis 的场景。

### 需求前提

1. 连续动力学最好能写成 `Ax+Bu`。
2. 不确定性主要体现在凸多面体输入集合，而不是复杂概率分布。
3. invariants、guards 与 resets 需可结构化成线性/affine 约束。
4. 团队能接受 reachable set 是 over-approximation，而不是精确轨迹。

### 不适用或高成本场景

若系统核心是强非线性连续动力学、黑盒仿真器或复杂层次并发交互，`d/dt` 并不是自然入口。

## 与相邻形式主义的关系

相对 [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)，`d/dt` 继续往“线性连续动力学 + uncertain input”方向推进；相对 [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)，它更强调 orthogonal polyhedra 与 controller synthesis；相对 [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)，它还没有转向 support functions / scalable flowpipe 平台路线。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续 `project_1` 需要把需求映射到混成验证后端，那么“把需求先收束成线性混成骨架”是一条现实可行的工程路径。

### 作为目标形式主义还是中间表示

更适合作为验证后端，而不是直接给人阅读的最终交付形式。

### 对需求到模型生成的启发

1. 生成阶段必须显式产出 discrete modes、continuous variables、guards、invariants 与 resets。
2. 连续动力学能否被线性化，直接决定 `d/dt` 这类工具是否可接。
3. 修复阶段不仅可能改 guards，也可能需要把连续模型压回更易分析的线性子类。

### 现实限制

`d/dt` 证明了 reachability + synthesis 可以打通，但它对输入模型结构有很强要求，不能替代一般黑盒仿真。

## 重要的相关工作

- [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)：更早的混成自动机验证器母线。
- [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)：后续更成熟的 polyhedral hybrid verifier。
- [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)：强调 scalability 的 hybrid verification platform。
- [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)：面向 non-linear flowpipe 的后续路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Hybrid Automata / d/dt`
- 论文角色：hybrid reachability verifier / switching-controller synthesizer
