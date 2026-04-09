# 面向人工胰腺患者在环监测的混成自动机方法 / A Hybrid Automata Approach for Monitoring the Patient in the Loop in Artificial Pancreas Systems

## 基本信息

- 标题：A Hybrid Automata Approach for Monitoring the Patient in the Loop in Artificial Pancreas Systems
- 中文标题：面向人工胰腺患者在环监测的混成自动机方法
- 作者：Aleix Beneyto, Vicen\c{c} Puig, B. Wayne Bequette, Josep Vehi
- 发表：*Sensors*, 21(21):7117, 2021
- DOI：`10.3390/s21217117`
- 链接：https://doi.org/10.3390/s21217117
- 形式主义：`Patient-Mode Hybrid Automaton + LPV/Zonotopic Observer Bank`
- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：人工胰腺患者在环故障监测 / 混成自动机应用
- 工具/实现获取方式：原文明确使用 reduced `Hovorka` model、polytopic Kalman filters、zonotopic observers、`Matlab R2019a` 与 `UVA/Padova` simulator；未提供单独代码仓库。
- 标准/格式获取方式：承载方式是 `HA_k`、fault signature matrix、LPV state-space model 与 observer bank；原文未提供独立交换格式。

## 简报

这篇论文的关键价值，在于把“患者是被控对象，同时又是控制环操作员”这件事显式压成混成自动机。作者不是只做一个 glucose predictor，而是把正常模式、故障模式、患者输入事件、残差一致性和 observer bank 统一进一套 mode-based diagnosis 结构里。对人工胰腺来说，这比单一连续模型更贴近真实风险来源。

- 形式主义定位：面向 patient-in-the-loop fault monitoring 的 `Hybrid Automata` 应用模型，而不是一般医学数据分类器。
- 构造方式简述：先用 reduced `Hovorka` nonlinear model 构造 `LPV` 多面体模型和 observer bank，再以 residual consistency + patient input 触发 `HA` 模式切换。
- 基础设施与场景简述：依托 `eSCAPE` multivariable hybrid AP、`Matlab`、`UVA/Padova` simulator、Kalman/zonotope observers 与 residual-based diagnoser，服务 meal/exercise/CHO fault 监测。

```text
glucose-insulin dynamics + patient actions -> LPV / zonotopic observers -> residual signatures -> hybrid automaton mode diagnosis -> AP fault monitoring / controller reconfiguration
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 患者 operational modes，例如 meal/postprandial、altered insulin sensitivity、resting/fasting。
2. faulty modes，例如 meal fault、exercise fault、faulty rescue CHO。
3. 连续 glucose-insulin dynamics。
4. patient input events，如 meal/exercise announcement。
5. 由 observer residuals 驱动的 hybrid diagnosis。

### 核心抽象

原文直接给出了混成自动机骨架：

$$
HA_k = \langle Q, X, U, Y, F, G, H, S, T \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是模式集合，包含 nominal 与 faulty patient modes。
2. `X` 是连续状态空间。
3. `U` 是连续输入空间，这里包括 insulin、meal 和 rescue `CHO`。
4. `Y` 是输出空间，这里主要是 `CGM` 测量。
5. `F` 是故障集合。
6. `G` 是离散时间状态函数集合。
7. `H` 是离散时间输出函数集合。
8. `S` 是事件集合。
9. `T : Q \times S \to Q` 是模式转移函数。

论文还明确把模式集合拆成：

$$
Q = Q_N \cup Q_F
$$

上式中的符号逐项解释如下：

1. `Q_N` 是正常模式集合。
2. `Q_F` 是故障模式集合。
3. 原文实例里共有 `3` 个正常模式和 `3` 个故障模式。

事件集合又进一步拆分为：

$$
S = S_S \cup S_C \cup S_F
$$

上式中的符号逐项解释如下：

1. `S_S` 是 spontaneous switching events，例如系统未观测到的患者行为。
2. `S_C` 是可观测输入事件，例如 meal/exercise announcement。
3. `S_F` 是 fault events，由 residual consistency 检查触发。

### 一个最小例子与通俗解释

论文里最直观的例子是“患者宣布进餐，但餐量估计错误”的路径：

1. 系统本来在 resting/fasting 模式 `q_3`。
2. 患者宣布进餐后，自动机转到 meal/postprandial 模式 `q_1`。
3. observer bank 持续检查 meal observer 的残差是否还能解释当前 `CGM` 变化。
4. 若 15 分钟内 meal observer 不再一致，就触发 fault transition，进入 faulty meal mode `q_6`。

通俗地说，这个模型像“给人工胰腺装上一位会记笔记的模式监督员”：它一边看患者说了什么，一边看血糖变化是不是和这句话对得上；如果对不上，就把系统切换到相应故障模式。

### 运行 / 接受 / 转移语义

模式切换由事件函数驱动：

$$
T : Q \times S \to Q
$$

其中：

1. 当前模式是 `q_i \in Q`。
2. 事件 `s \in S` 可以来自患者输入，也可以来自 residual-based diagnosis。
3. 输出模式 `q_j = T(q_i, s)` 表示系统认定的下一运行模式。

论文用 fault signature matrix 来决定哪些残差模式可触发哪些转移：

$$
FSM =
\begin{bmatrix}
f_{1,1} & f_{1,2} & \cdots & f_{1,n_m} \\
f_{2,1} & f_{2,2} & \cdots & f_{2,n_m} \\
\vdots & \vdots & \ddots & \vdots \\
f_{n_s,1} & f_{n_s,2} & \cdots & f_{n_s,n_m}
\end{bmatrix}
$$

上式中的符号逐项解释如下：

1. `n_s` 是事件 / 转移候选数。
2. `n_m` 是 automaton 模式数。
3. 每一行描述一种可接受的 residual signature。

单个二值残差信号由 interval residual 是否包含 `0` 决定。原文可压缩为：

$$
f_i =
\begin{cases}
1, & \text{if } \sum_{M_i=1}^{M} (t_{r_i}^{l} < 0 \lor t_{r_i}^{u} > 0) = 1 \\
0, & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `f_i` 是第 `i` 个二值残差信号。
2. `t_{r_i}^{l}` 与 `t_{r_i}^{u}` 分别是 interval residual 的下界和上界。
3. 直觉上，如果 observer 预测区间已经不能解释真实行为，就触发对应 fault symptom。

### 语义边界

这篇论文的语义边界也很明确：

1. 它处理的是“连续代谢动力学 + 离散患者模式切换”的混成诊断问题，不是一般控制综合。
2. 连续部分依赖 reduced `Hovorka` model 与 `LPV` 近似，不追求完整生理真实性。
3. 模式切换 heavily 依赖 observer residuals 和患者输入，输入缺失时诊断能力会下降。
4. 论文重点是 mode/fault detection，而不是完整 closed-loop proof。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 混成自动机 | `$HA_k = \langle Q, X, U, Y, F, G, H, S, T \rangle$` | 把患者模式、连续状态、输入输出和故障统一到一套结构。 |
| 正常/故障模式 | `$Q = Q_N \cup Q_F$` | 把运行模式与 fault modes 分离。 |
| 事件类型 | `$S = S_S \cup S_C \cup S_F$` | 区分 spontaneous、患者输入和 fault-triggered events。 |
| 转移函数 | `$T : Q \times S \to Q$` | 模式切换由事件驱动。 |
| 残差签名矩阵 | `$FSM$` | 用可接受的 symptom pattern 决定允许的 mode transitions。 |
| 二值残差 | `$f_i \in \{0,1\}$` | 通过 residual consistency 判定 observer 是否失配。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 明确区分 meal、exercise、rest 与多种 faulty modes。 |
| 事件 / 触发 | 强支持 | 患者输入、残差违例和自发切换共同驱动状态迁移。 |
| 守卫 / 数据 | 强支持 | `CGM`、meal/CHO 输入与 residual consistency 都参与守卫。 |
| 层次 | 弱支持 | 主要是单层 mode automaton，而非层次状态机。 |
| 并发 / 同步 | 弱支持 | 重点不是并发，而是 mode diagnosis。 |
| 时间约束 | 部分支持 | 使用采样时刻和 15 分钟窗口，但不是 clock automata 风格显式时钟。 |
| 连续动态 / 随机性 | 强连续、弱随机 | 连续代谢动力学是一等对象；不确定性主要通过 zonotope bounds 处理。 |
| 可执行 / 可验证性 | 强分析 | 可在线诊断并支持控制重构，但形式证明深度有限。 |

### 形式化问题与性质

1. 本文最大的增量，是把 patient-in-the-loop fault 变成显式 mixed discrete/continuous diagnosis 问题。
2. observer bank 不是附属工具，而是 `HA` 模式切换的感知前端。
3. 这条路线很适合“有连续 plant、又有人为离散事件输入”的控制系统。
4. 对混成主干来说，它提供了比纯机器人模式切换更典型的 medical CPS 证据。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 用 reduced `Hovorka` model 描述 glucose-insulin dynamics。
2. 将其转成 `LPV` / polytopic state-space 形式。
3. 设计 zonotopic Kalman observer bank。
4. 依据 residual signatures 和 patient inputs 构建 `HA_k`。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `HA_k` 模式图。
2. `FSM` 签名矩阵。
3. `LPV` state-space 模型。
4. zonotopic interval observers。

### 交换与互操作

互操作重点不在开放标准，而在：

1. 连续病理模型到 observer bank 的转换。
2. observer residual 到 hybrid diagnosis 的连接。
3. diagnosis 结果到 controller reconfiguration 的反馈。

## 配套基础设施

- 建模/编辑工具：原文未给专用图形编辑器，建模主要基于数值模型与 `HA` 结构。
- 解析/交换/元模型支持：有 `LPV`、observer bank 和 `HA` 结构，但无统一交换文件。
- 仿真/执行支持：`Matlab R2019a`、`UVA/Padova T1D Simulator v3.2`、`eSCAPE` AP control setup。
- 验证/分析支持：residual consistency analysis、fault-mode diagnosis、population simulations。
- 代码生成/转换支持：原文未提供。
- 标准化或社区生态：依托 artificial pancreas、medical CPS 与 hybrid diagnosis 研究生态。

## 适用场景与需求前提

### 适用场景

适合存在显式运行模式、连续生理或物理动力学、并且模式切换受人类操作行为影响的 medical CPS / human-in-the-loop 控制系统。

### 需求前提

1. 系统存在可辨识的正常/故障模式。
2. 连续 plant 可由可观测的 state-space / LPV 模型近似。
3. 有稳定的 observer 或 residual generation 机制。
4. 外部人类输入对控制闭环有显著影响。

### 不适用或高成本场景

如果系统缺乏可解释模式、无法建立可靠 observer，或人类输入完全不可观测，则这种混成诊断链条会明显变弱。

## 与相邻形式主义的关系

相对 [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)，本文是典型 medical CPS 应用；相对 [formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md](../formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md)，它更强调 observer-based diagnosis 而非 reachability；相对 [a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md](../a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md)，它更聚焦 patient-in-the-loop 故障模式。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求同时包含连续 plant、离散模式切换和人类输入故障时，普通 `FSM` 很难覆盖，混成自动机更自然。

### 作为目标形式主义还是中间表示

对 medical CPS 监测器，它可以直接作为目标形式主义；对一般控制系统，也很适合作为“连续对象 + 模式监督层”的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把 nominal modes、fault modes 和 human-triggered events 明确分开。
2. LLM 若要生成混成监测模型，不能只写模式图，还要补 residual/observer 证据链。
3. 对患者在环、操作员在环这类系统，“人是执行器还是传感器”本身就是高价值需求特征。

## 重要的相关工作

- [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)：混成自动机的基础理论。
- [formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md](../formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md)：另一条应用型混成分析路线。
- [a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md](../a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md)：模式切换驱动的机器人混成架构。

## 文献分类总结

- 这是一篇 `🌊` 类高价值应用条目，核心贡献是把人工胰腺中的 patient-in-the-loop 监测压成 `Hybrid Automata + observer bank` 结构。
- 其描述客体是连续生理系统及其模式监督，因此记为 `🌡️`；论文语境落在 medical CPS，因此记为 `🌡️`。
- 对 `project_1` 来说，它补足了“连续对象 + 人为离散输入 + 故障监测”这类需求的形式主义证据。
