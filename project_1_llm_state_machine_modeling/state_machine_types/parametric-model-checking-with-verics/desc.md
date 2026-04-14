# 基于 VerICS 的参数化模型检查 / Parametric Model Checking with VerICS

## 基本信息

- 标题：Parametric Model Checking with VerICS
- 中文标题：基于 VerICS 的参数化模型检查
- 作者：Michał Knapik，Artur Niewiadomski，Wojciech Penczek，Agata Półrola，Maciej Szreter，Andrzej Zbrzezny
- 发表：*Transactions on Petri Nets and Other Models of Concurrency IV*，pp. 98-120，2010
- DOI：`10.1007/978-3-642-18222-8_5`
- 链接：https://doi.org/10.1007/978-3-642-18222-8_5
- 形式主义：`VerICS / parametric BMC / ENS / distributed TPN / UML subset / PRTECTL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：多形式主义参数化 `SAT-BMC` 验证路线与 `VerICS` 模块扩展
- 工具/实现获取方式：原文明确给出 `VerICS` 架构，并说明新增 `BMC4EPN`、`BMC4TPN`、`BMC4UML` 三个模块；正文未给稳定公开仓库链接。
- 标准/格式获取方式：输入形式包括 `ENS`、distributed `TPN` 与受限 `UML`，性质用 `PRTECTL` 或参数化 reachability 公式表示；承载对象是 `VerICS` 的符号路径编码与 `SAT` 工作流，而不是中立交换标准。

## 简报

这篇论文的重点不是再引入一种新状态机，而是把 `VerICS` 从“能做普通模型检查”推进到“能在多个输入形式上做参数化验证”。它最有代表性的地方在于：同一套 `SAT`-based bounded model checking 思路，被同时接到了 `Elementary Net Systems`、distributed `Time Petri Nets` 和受限 `UML` 状态机子集上，并且不只问“某性质是否成立”，还问“最小多大参数或时间上界才成立”。

- 形式主义定位：多形式主义参数化验证方法路线，围绕 `VerICS` 的 `SAT-BMC` 基础设施展开。
- 构造方式简述：把系统在深度 `$k$` 上展开成符号路径，编码成命题公式，再把 `PRTECTL` 或参数化 reachability 一并编码给 `SAT` 求解器。
- 基础设施与场景简述：依托 `BMC4EPN`、`BMC4TPN`、`BMC4UML`、`MiniSAT/RSat`、symbolic path encoding 与参数化 reachability，服务实时协议、并发 Petri 网和 `UML` 设计模型。

```text
ENS / distributed TPN / UML subset -> symbolic k-path encoding -> SAT-based BMC -> parameter synthesis / minimal bound search
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Elementary Net Systems (ENS)`；
2. distributed `Time Petri Nets (TPN)`；
3. 受限 `UML` 类图 + 对象图 + 状态机；
4. `PRTECTL` 参数化时序逻辑；
5. `SAT`-based bounded model checking。

### 核心抽象

对 `ENS`，论文直接使用：

$$
EN = (P,T,F,m_0)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 places 集合。
2. `$T$` 是 transitions 集合。
3. `$F$` 是 flow relation。
4. `$m_0$` 是初始 marking。

对 `Time Petri Nets`，论文给出：

$$
N = (P,T,F,m_0,Eft,Lft)
$$

上式中的符号逐项解释如下：

1. 前四项与 `ENS` 相同。
2. `$Eft:T\to\mathbb N$` 是 earliest firing time。
3. `$Lft:T\to\mathbb N\cup\{\infty\}$` 是 latest firing time。
4. 论文主体实际处理的是 distributed、1-safe、sequential `TPN` 子类。

在验证层，整条方法的统一骨架是符号 `$k$`-路径：

$$
path_k(w_0,\ldots,w_k)=I(w_0)\land\bigwedge_{i=0}^{k-1}T(w_i,w_{i+1})
$$

上式中的符号逐项解释如下：

1. `$w_i$` 是第 `$i$` 个 symbolic state 的命题变量向量。
2. `$I(w_0)$` 编码初始状态。
3. `$T(w_i,w_{i+1})$` 编码从第 `$i$` 步到第 `$i+1$` 步的转移关系。
4. 这一定义是三类输入形式共享的 `BMC` 母式。

论文对参数化逻辑给出的代表例子包括：

$$
EG^{\le 3}p
$$

以及

$$
\forall \Theta_1 \le 1 \ \exists \Theta_2 \le 2 \ EF^{\le \Theta_1+\Theta_2}p
$$

上式中的符号逐项解释如下：

1. `$\Theta_1,\Theta_2$` 是自然数参数。
2. 带上标的 `$\le c$` 表示路径长度约束。
3. 论文把这类 `PRTECTL` 公式通过展开量词，归约成命题公式的合取 / 析取组合。

参数化模型检查的一个复杂度锚点被写成：

$$
O(|M|^{k+1}\cdot |\varphi|)
$$

上式中的符号逐项解释如下：

1. `$M$` 是 Kripke 模型。
2. `$k$` 是公式中的参数个数。
3. `$\varphi$` 是待检性质。
4. 这个复杂度结果解释了为什么论文强调只对“有限深度局部片段”做 `BMC` 编码。

### 一个最小例子与通俗解释

一个最容易理解的例子是论文处理的“最小时间到达”问题：

1. 先用普通 `BMC` 找到一条到达目标命题 `$p$` 的 witness。
2. 从 witness 中读出实际用时 `$x$`。
3. 再在模型中加入一个控制计时过程或额外 clock，反复检验 `EF^{\le c}p` 是否仍成立。
4. 由此逼出满足性质的最小整数时间界。

通俗地说，这条路线像是把“模型检查”改造成“参数试探机”。它不只告诉你某模型会不会出错，还会帮你问：最小要多少时间、多少参数裕量，系统才会满足要求。

### 运行 / 接受 / 转移语义

对 `ENS`，论文直接把 transition relation 编码为命题公式：

$$
T(w,v)=\bigvee_{t\in T} \mathrm{Enc}_t(w,v)
$$

这里的含义是：

1. 每个 `$\mathrm{Enc}_t(w,v)$` 精确编码某个变迁 `$t$` 的启用与 firing 结果。
2. 整个系统的一步行为由所有候选变迁编码的析取构成。

对参数化 reachability，论文给出的代表目标是：

$$
\min \{ c \in \mathbb N \mid EF^{\le c}p \}
$$

上式中的符号逐项解释如下：

1. `$p$` 是目标状态谓词。
2. `$EF^{\le c}p$` 表示在不超过 `$c$` 的路径长度或时间界内可达。
3. 论文分别为 `TPN` 与 `UML` 给出最小界搜索算法。

### 语义边界

1. `ENS` 路线支持 `PRTECTL`，但 `TPN/UML` 路线在本文中主要做到参数化 reachability。
2. `TPN` 只处理 distributed、1-safe、sequential 子类。
3. `UML` 只覆盖受限子集，不支持动态对象创建与终止。
4. 优势来自有限深度 `BMC`，并不意味着对大深度展开仍然轻松。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `ENS` 骨架 | `$EN=(P,T,F,m_0)$` | 并发 Petri 网输入的最小单位。 |
| `TPN` 骨架 | `$N=(P,T,F,m_0,Eft,Lft)$` | 实时网模型加入 firing-time 区间。 |
| 符号 `$k$`-路径 | `$path_k(w_0,\ldots,w_k)$` | 三类输入统一共享的 `BMC` 编码母式。 |
| 参数化逻辑 | `$EG^{\le 3}p$`、`$\forall \Theta_1 \exists \Theta_2 EF^{\le \Theta_1+\Theta_2}p$` | `PRTECTL` 的代表性表达能力。 |
| 复杂度锚点 | `$O(|M|^{k+1}\cdot |\varphi|)$` | 参数化逻辑为何需要结合 `BMC` 做局部化处理。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `ENS`、`TPN`、`UML` 状态机都能落到统一编码框架。 |
| 事件 / 触发 | 很强 | 变迁、事件队列、触发条件在编码里都是一等对象。 |
| 守卫 / 数据 | 中等支持 | `UML` 路线支持 guards、queues 与变量，但不是富数据求解器。 |
| 层次 | 中等支持 | `UML` 子集含 composite states 和 regions。 |
| 并发 / 同步 | 很强 | `ENS/TPN/UML` 都服务并发系统验证。 |
| 时间约束 | 很强 | `TPN` firing interval、参数化时间界和有界路径长度是中心内容。 |
| 连续动态 / 随机性 | 不支持 | 本文不处理混成或概率动力学。 |
| 可执行 / 可验证性 | 很强 | 已实现到 `VerICS`，并给出多个 benchmark 结果。 |

### 形式化问题与性质

1. `VerICS` 在这里的代表性，不是“又一个模型检查器”，而是同一套参数化 `SAT-BMC` 内核被证明能跨多输入形式复用。
2. 论文同时覆盖了 Petri 网、时间网和 UML，这对文库里的“多前端接一后端”路线很关键。
3. 参数化 reachability 把“是否可达”推进成“多大参数才可达/不可达”，更接近工程调参问题。

## 构造方式与承载格式

### 建模入口

原文中的入口包括：

1. `ENS`；
2. distributed `TPN`；
3. class / object / state machine 组成的 `UML` 子集；
4. `PRTECTL` 或参数化 reachability 公式。

### 机器可处理承载方式

机器可处理承载方式包括：

1. state-variable vectors；
2. propositional encoding of transition relations；
3. symbolic `$k$`-paths；
4. `SAT` solver 输入子句集合。

### 交换与互操作

1. 多前端都被压到统一的 propositional encoding 层。
2. `TPN` 通过离散化 extended region graph 进入 `BMC`。
3. `UML` 不是先翻译成另一个中间自动机，而是直接编码到命题逻辑。

## 配套基础设施

- 建模/编辑工具：`VerICS` 前端支持多语言输入，含 `TPN`、`UML` 等。
- 解析/交换/元模型支持：`BMC4EPN`、`BMC4TPN`、`BMC4UML` 三个新增模块是论文核心。
- 仿真/执行支持：重点不在仿真，而在 witness 搜索与参数界分析。
- 验证/分析支持：`PRTECTL`、reachability、参数化最小界搜索、`SAT`-based `BMC`。
- 代码生成/转换支持：主要是到 propositional formula 的逻辑编码，不主打部署代码生成。
- 标准化或社区生态：依托 `VerICS` 与 `MiniSAT/RSat` 生态，延续 SAT-based verification 路线。

## 适用场景与需求前提

### 适用场景

适合那些已经有 `Petri Net / UML / timed` 形式模型，但真正关心的是“参数或时间界取多少才安全”的实时与嵌入式系统分析场景。

### 需求前提

1. 系统可落到论文支持的 `ENS`、distributed `TPN` 或 `UML` 子集。
2. 目标性质能收束到 `PRTECTL` 或 reachability 类问题。
3. 团队接受 `SAT` 求解和有界展开式工作流。
4. 若是 `TPN`，最好满足 1-safe、distributed、sequential 约束。

### 不适用或高成本场景

若需要完整 `CTL/LTL` across all frontends、无界深度证明、连续动力学或概率模型，这条 2010 年的 `VerICS` 参数化路线就不是直接答案。

## 与相邻形式主义的关系

相对 [romeo-a-tool-for-analyzing-time-petri-nets/desc.md](../romeo-a-tool-for-analyzing-time-petri-nets/desc.md) 与 [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)，`VerICS` 更强调参数化 `SAT-BMC` 而不是 state-class/zone 风格分析；相对 [model-checking-timed-uml-state-machines-and-collaborations/desc.md](../model-checking-timed-uml-state-machines-and-collaborations/desc.md) 与 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，它同样处理 `UML`，但重点是直接符号编码和参数化 reachability；相对 [configurable-verification-of-timed-automata-with-discrete-variables/desc.md](../configurable-verification-of-timed-automata-with-discrete-variables/desc.md)，后者面向 `TA + discrete variables` 抽象域组合，而本文更像多前端统一到 `SAT-BMC` 的早期平台路线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒我们，前端形式主义可以很多，但验证后端未必需要各自独立。
2. 若 `project_1` 以后需要面向不同建模对象生成不同中间模型，`VerICS` 这种“多前端 -> 单一符号后端”的组织方式很有借鉴价值。
3. 参数化 reachability 也很适合作为修复迭代中的量化目标，例如“最小延迟/最小安全裕量”。

### 作为目标形式主义还是中间表示

更像统一验证后端与方法路线，而不是前端建模语言。

### 对需求到模型生成的启发

1. 若需求中存在显式阈值或时间界，不妨把“求界值”本身当成验证任务。
2. 生成模型时要提前考虑后端是否容易被统一编码，而不只是追求前端表达好看。
3. 多形式主义共用后端时，模型元素抽象最好尽量保持同构。

## 重要的相关工作

1. [romeo-a-tool-for-analyzing-time-petri-nets/desc.md](../romeo-a-tool-for-analyzing-time-petri-nets/desc.md)：`TPN` 工具线对照。
2. [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：`UML -> PAT` 路线。
3. [configurable-verification-of-timed-automata-with-discrete-variables/desc.md](../configurable-verification-of-timed-automata-with-discrete-variables/desc.md)：更晚期的 timed/discrete unified verification 框架。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
