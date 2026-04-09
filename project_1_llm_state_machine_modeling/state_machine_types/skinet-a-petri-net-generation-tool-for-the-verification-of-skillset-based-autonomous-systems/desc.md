# SkiNet：面向 Skillset 型自主系统的 Petri 网生成与验证工具 / SkiNet, A Petri Net Generation Tool for the Verification of Skillset-based Autonomous Systems

## 基本信息

- 标题：SkiNet, A Petri Net Generation Tool for the Verification of Skillset-based Autonomous Systems
- 中文标题：SkiNet：面向 Skillset 型自主系统的 Petri 网生成与验证工具
- 作者：Baptiste Pelletier，Charles Lesire，David Doose，Karen Godary-Dejean，Charles Dramé-Maigné
- 发表：*Electronic Proceedings in Theoretical Computer Science*，371:120-138，2022
- DOI：`10.4204/EPTCS.371.9`
- 链接：https://doi.org/10.4204/EPTCS.371.9
- 形式主义：`Skillset / Petri Net / SkiNet / Tina toolbox`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准 / 基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`Skillset -> Petri net -> Tina` 的技能架构验证工具前端
- 工具/实现获取方式：原文明确给出 `SkiNet` 公开入口 `https://gitlab.com/onera-robot-skills/skinet-release`，并说明其与 skillset 控制代码生成链协同工作。
- 标准/格式获取方式：输入是 skillset specification（resources / skills / guards / effects）；中间承载是生成的 `Petri net` 与 Kripke structure；分析侧使用 `Tina` 工具箱的 `Selt`、`Muse` 和 `PathTo`。

## 简报

这篇论文补的不是新的 Petri 网理论，而是一层很务实的验证基础设施：把 skill-based robotics architecture 自动翻成普通 `Petri net`，让不直接操作 LTL/CTL 或 Petri 建模的系统设计者也能做 deadlock、transition liveness、skill liveness 这类检查。它的价值在于把“机器人技能架构的高层规格”和“现成 Petri 工具箱的成熟分析能力”接到了一起。

- 形式主义定位：面向 skillset 架构的 `Petri net` 生成、验证与解释基础设施。
- 构造方式简述：`skillset(resources / skills / guards / effects) -> Petri net -> Kripke structure -> Tina LTL / CTL checks`。
- 基础设施与场景简述：依托 `SkiNet`、`Tina`、`Selt`、`Muse`、`PathTo` 与代码生成链，服务 autonomous systems / robotics 的前期验证。

```text
skillset specification -> generated Petri net -> Kripke structure -> LTL / CTL checks -> skill-level feedback
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. skillset architecture。
2. resources / skills / guards / effects / skillset transitions。
3. 带 priority relation 的 Petri net。
4. 由生成网导出的 Kripke structure。
5. `Tina` 工具链上的 LTL / CTL 检查。

### 核心抽象

论文给出的网模型是：

$$
\langle N, m_0 \rangle,\qquad N = (P, T, F)
$$

并扩展成：

$$
N = (P, T, F, \chi)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 places 集合。
2. `$T$` 是 transitions 集合。
3. `$F$` 是有向弧集合。
4. `$m_0$` 是初始 marking。
5. `$\chi$` 是 transition priority relation；若 `$t_1 \chi t_2$` 且二者同时 enabled，则只有 `$t_1$` 可 fire。

skillset 本体被整理成：

$$
S = (R, V, S)
$$

上式中的符号逐项解释如下：

1. `$R$` 是 resources 集合。
2. `$V$` 是 events 集合。
3. 最后的 `$S$` 是 skills 集合。
4. 这里沿用原文记号，虽然集合名与整体对象名同为 `$S$`，上下文可区分。

单个 skillset transition 写成：

$$
t = (f, E, s)
$$

上式中的符号逐项解释如下：

1. `$f$` 是 resource guard。
2. `$E$` 是 effects 集合。
3. `$s=(state_1,state_2)$` 是 skill state change。

论文最重要的正确性约束是资源与技能状态 place invariants：

$$
\forall r \in R,\ \sum_{S_i^r \in S_r} m_n[p_i^r] = 1
$$

$$
\forall s \in Skills,\ m_n[p_e^s] + m_n[p_i^s] + \sum_k m_n[p_{x,k}^s] = 1
$$

它们共同推出 1-safeness：

$$
\forall m \in M,\ \forall p \in P,\ m[p] \in \{0,1\}
$$

### 一个最小例子与通俗解释

论文用 Spot 机器人 skillset 中的 `go_to` 技能举例：

1. start transition 需要 `lease_status == AutoMode`、`control_mode == Idle`、`power_status == PowerOn`。
2. 生成的 Petri transition 会把技能 place 从 idle 推到 running，同时把 `control_mode` 从 `Idle` 推到 `Busy`。
3. success transition 则在满足 invariant 时把 token 从 running 推到某个 exit place，并把 `control_mode` 复位到 `Idle`。

通俗地说，SkiNet 并不是让用户自己画网，而是把“资源状态机 + 技能状态机 + 前置条件 / 不变量 / 失败效果”自动编成一张 Petri 网，再替用户跑一遍“会不会卡死、有没有永远激活不了的技能、有没有死 transition”。

### 运行 / 接受 / 转移语义

资源与技能在运行时都被建成 place invariants：

1. 每个 resource 在任一时刻恰有一个 state place 持有 token。
2. 每个 skill 在任一时刻也只能处于 `idle / running / exit` 中的一个状态。

start / success / failure / reset 等语义通过自动生成的 transitions 落到网里。典型 start transition 形如：

$$
t_{go\_to,start} = (f, E, (e_{go\_to}, i_{go\_to}))
$$

而 success transition 则会把 token 从 running place 推到对应 exit place。作者随后用数学归纳证明：所有自动生成 transition 都保持资源和技能状态机的单 token 语义。

### 语义边界

1. 论文关注的是 skill-based architecture，不是一般机器人控制程序。
2. 资源状态空间必须有限，否则无法生成可检查 Petri 网。
3. 当前正确性证明首先保证“生成网保持资源 / 技能状态机语义”，但运行时语义与执行代码的完全等价仍被列为后续工作。
4. 状态空间爆炸是作者明确承认的现实瓶颈。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 网骨架 | `$\langle N,m_0 \rangle,\ N=(P,T,F,\chi)$` | 生成的 Petri 后端模型。 |
| skillset 骨架 | `$S=(R,V,S)$` | 高层自主系统规格。 |
| 单条 skillset transition | `$t=(f,E,s)$` | guard / effect / state change 的统一单位。 |
| 资源 invariant | `$\forall r,\sum m_n[p_i^r]=1$` | 每个 resource 只能在一个状态。 |
| 技能 invariant | `$m_n[p_e^s]+m_n[p_i^s]+\sum_k m_n[p_{x,k}^s]=1$` | 每个 skill 只能处于一个阶段。 |
| 技能可激活性 | `$AGEF\ p_i^s$` | 是否总能再次激活某技能。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | resources 与 skills 都显式编码成状态 places。 |
| 事件 / 触发 | 很强 | events / start / success / failure / reset 都入网。 |
| 守卫 / 数据 | 中等支持 | 通过 guards、solutions 与资源状态组合表达。 |
| 层次 | 弱支持 | 主体是 flat Petri net，不是层次网。 |
| 并发 / 同步 | 很强 | 资源竞争、技能并发和互斥都是主线。 |
| 时间约束 | 不支持 | 本文不是 timed Petri 工具。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | 自动生成网后即可接 `Tina` 做检查。 |

### 形式化问题与性质

1. 这篇论文补的是自主系统 skill architecture 的“自动验证前端”，而不是新的 Petri theory。
2. 它最重要的价值是把用户真正写的 skillset specification 和成熟的 Petri / temporal-logic 工具链接起来。
3. 对 `state_machine_types` 来说，这类条目不长主树，但非常适合补 `Petri net` 在 autonomous-system architecture verification 上的基础设施支线。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 写 skillset specification。
2. 声明 resources、guards、effects、events 和 skills。
3. SkiNet 自动生成 Petri net。
4. 进一步导出 Kripke structure，送到 `Tina` 的 `Selt / Muse / PathTo`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. skillset 文本规格。
2. 生成的 `Petri net`。
3. Kripke structure。
4. `LTL / CTL / \mu`-calculus 性质。

### 交换与互操作

1. skillset 本身和控制代码生成链是上游。
2. SkiNet 负责把高层规格翻成普通 Petri net，而不是 colored net，从而接入更广泛的验证工具。
3. 验证时依托 `Tina` 工具箱，而不是自建专用 model checker。

## 配套基础设施

- 建模/编辑工具：skillset specification 与其代码生成工具链。
- 解析/交换/元模型支持：SkiNet 的自动翻译与 Kripke structure 生成。
- 仿真/执行支持：论文提到未来的 `SkiNet Live` 将把 Petri firing 与真实系统执行同步显示。
- 验证/分析支持：`Tina`、`Selt`、`Muse`、`PathTo`、dead/live/safe/deadskill/deadset 检查。
- 代码生成/转换支持：skillset 侧已有 controller code generation，SkiNet 与其协同使用。
- 标准化或社区生态：依托 Petri-net 与 Tina 生态，同时服务机器人技能架构社区。

## 适用场景与需求前提

### 适用场景

适合 skill-based autonomous systems，尤其是机器人系统中已经把能力拆成 skills、resources 和 skill manager 的场景。

### 需求前提

1. 系统需要能写成有限资源状态和有限技能状态。
2. 技能执行逻辑应能抽成 guards / effects / state changes。
3. 团队接受把高层架构先翻成 Petri 网再做验证。
4. 若想让验证结果对应真实执行，必须同时维护好 skillset 与代码生成链的一致性。

### 不适用或高成本场景

若系统状态空间过大、技能和资源过多，生成网对应的 Kripke structure 会迅速膨胀，作者也明确把这点列为现实瓶颈。

## 与相邻形式主义的关系

它与手写 Petri net controller synthesis 路线不同，重点是“自动从现有 skill architecture 生成网”；相对 colored Petri net 路线，它主动退回普通 Petri net，以换取更多现成分析工具；相对 mission-specific verification，它又更贴近系统的实际执行骨架。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提示 `project_1`：若未来目标系统采用的是 skill / task / resource 这类高层状态机架构，完全可以把它们下压成 Petri family 做验证，而不必要求用户直接面向 Petri 网建模。

### 作为目标形式主义还是中间表示

对 `project_1` 来说，skillset 是前端应用架构表示，Petri net 是验证中间表示与分析后端。

### 对需求到模型生成的启发

1. 自动生成验证后端时，应先证明后端模型保持前端状态机的不变式。
2. 若目标用户不是形式化专家，工具应把公式和反例保留给高级用户，但默认只暴露有解释性的结果。
3. 把 colored / high-level 形式主义降到普通 Petri net，有时比坚持 richer notation 更实用。

### 现实限制

论文目前只完成了 skillset 到网的保持性证明，还没有彻底打通“运行时代码语义 = 生成网语义”的完整证明链。

## 重要的相关工作

1. 论文把已有基于 Behavior Tree、fault tree、colored Petri net 的自主系统验证路线作为对照。
2. `Tina` 在这里不是被动引用，而是 SkiNet 实际用来跑 LTL / CTL / deadlock / liveness 的核心后端。
3. 作者还规划了 `SkiNet Mission` 和 `SkiNet Live`，说明这条基础设施线还有继续扩展的空间。

## 文献分类总结

- 这篇论文应归入：📦 标准、交换格式、元模型与执行载体
- 这篇论文应归入：🏗️ 标准 / 基础设施
- 这篇论文应归入：🏭 并发过程 / 资源流
- 这篇论文应归入：🌡️ CPS / 物理系统建模
- 作为 `state_machine_types` 条目，它补的是 `Skillset -> Petri -> Tina` 的自主系统验证基础设施路线。
