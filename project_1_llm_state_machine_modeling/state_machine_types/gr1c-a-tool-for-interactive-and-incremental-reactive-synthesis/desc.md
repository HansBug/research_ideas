# gr1c：交互式与增量式反应式综合工具 / gr1c: a tool for interactive and incremental reactive synthesis

## 基本信息

- 标题：gr1c: a tool for interactive and incremental reactive synthesis
- 中文标题：gr1c：交互式与增量式反应式综合工具
- 作者：Scott C. Livingston
- 发表：Caltech Library / CaltechAUTHORS，2024
- DOI：`10.7907/5M62H-A4204`
- 链接：https://authors.library.caltech.edu/doi/10.7907/5m62h-a4204
- 形式主义：`GR(1) reactive synthesis / strategy automaton / gr1c`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`GR(1)` 综合、交互式 winning-set 查询、增量式策略修补与 `Promela/JSON` 输出工具条目
- 工具/实现获取方式：原文明确给出开源仓库 `https://github.com/tulip-control/gr1c`，并说明 `gr1c` 由 `C` 实现、依赖 `CUDD` 作为主要 `BDD` 后端，可与 `TuLiP` 集成。
- 标准/格式获取方式：输入是 `gr1c` plaintext `GR(1)` 规格与 edge-set-change file；输出支持图形/文本策略、`JSON` 与 `Promela`，不是独立行业标准。

## 简报

这篇论文补的是 `GR(1)` synthesis 工具链的一条工程化分支。相对只做一次性求解的综合器，`gr1c` 更强调两件事：第一，用户可以在 winning-set 固定点计算之后交互式查询 sublevel sets、系统下一步可选动作和中间 `BDD` 值；第二，既有策略可以在目标或安全转移发生局部变化后被增量修补，而不必每次从零重新综合。

- 形式主义定位：`GR(1)` reactive synthesis 的交互式 / 增量式求解路线，而不是新的状态机母型。
- 构造方式简述：`GR(1)` plaintext spec -> `BDD` fixed-point winning set -> sublevel-set strategy construction -> interactive query / incremental patch / `JSON` 或 `Promela` 输出。
- 基础设施与场景简述：依托 `CUDD`、`TuLiP` wrapper、`gr1c patch`、edge-set-change file 和 `Spin/Promela` 后验检查，服务机器人任务规划与离散化 reactive controller synthesis。

```text
GR(1) assumptions/guarantees -> gr1c BDD fixed point -> strategy automaton -> interactive query / incremental patch / Promela checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `GR(1)` 规格与 synthesis game。
2. `BDD` 表示的状态集合、winning set 与 sublevel sets。
3. 从 sublevel sets 构造出的 finite strategy automaton。
4. `gr1c` 交互式命令与 `gr1c patch` 增量修补接口。
5. `JSON` / `Promela` 等机器可读输出。

### 核心抽象

根据论文对 initial states、feasible transitions 与 environment/system goals 的说明，可把 `gr1c` 处理的 `GR(1)` 游戏骨架保守整理为：

$$
G = (X, Y, \Theta_e, \Theta_s, \rho_e, \rho_s, \{\psi^{env}_j\}_{j=1}^{m}, \{\psi^{sys}_i\}_{i=1}^{n})
$$

上式中的符号逐项解释如下：

1. `$X$` 是 environment-controlled variables。
2. `$Y$` 是 system-controlled variables。
3. `$\Theta_e,\Theta_s$` 分别约束环境和系统的初始状态。
4. `$\rho_e,\rho_s$` 分别约束环境和系统的可行转移。
5. `$\psi^{env}_j$` 是第 `$j$` 个环境活性目标。
6. `$\psi^{sys}_i$` 是第 `$i$` 个系统活性目标。
7. 该元组是依据论文描述做的保守整理，原文显式给出的是下列 `GR(1)` 活性公式。

论文给出的 `GR(1)` 活性规格是：

$$
\bigwedge_{j=1}^{m} \Box\Diamond \psi^{env}_j \Rightarrow \bigwedge_{i=1}^{n} \Box\Diamond \psi^{sys}_i
$$

上式中的符号逐项解释如下：

1. `$\Box\Diamond$` 表示“总是最终会再次达到”。
2. 左侧是环境反复满足其目标的假设。
3. 右侧是系统策略必须反复满足其目标的保证。
4. 论文同时说明 initial states 与 feasible transitions 可作为安全要求加入该综合问题。

### 一个最小例子与通俗解释

论文给出的最小规格使用两个布尔变量 `x` 与 `y`：

1. `x` 是环境变量，环境假设它会在相邻步之间反复切换。
2. `y` 是系统变量，初始为真。
3. 系统目标包括反复达到 `y & x`，也反复达到 `!y`。
4. 交互命令 `sysnext` 可以在某个当前状态和目标编号下，返回哪些系统后继能继续朝对应 sublevel set 前进。

通俗地说，`gr1c` 不只是“按规格吐出一个控制器”，还像一个可检查内部计算过程的 `GR(1)` 工作台：你可以问它为什么某个状态可赢、下一步有哪些可选动作、规格改动后原策略能不能局部修补。

### 运行 / 接受 / 转移语义

论文说明 winning set 通过 `\mu`-calculus 固定点迭代得到，并用 sublevel sets 构造策略。可把进度语义保守整理为：

$$
\mathrm{rank}_i(s') < \mathrm{rank}_i(s)
$$

上式中的符号逐项解释如下：

1. `$i$` 是当前系统活性目标编号。
2. `$s$` 是当前游戏状态。
3. `$s'$` 是候选下一状态。
4. `$\mathrm{rank}_i$` 表示相对第 `$i$` 个系统目标的 sublevel-set 层级。
5. 该式表示一次可接受的系统动作应使策略在 winning-set 层级上向目标推进；这是根据论文对 sublevel sets 与 `sysnext` 的解释做的保守表达。

增量修补接口可保守写成：

$$
S' = \mathrm{patch}(S, \Delta)
$$

上式中的符号逐项解释如下：

1. `$S$` 是已有策略。
2. `$\Delta$` 是目标追加、目标删除或 edge-set-change file 给出的转移变化。
3. `$S'$` 是 `gr1c patch` 尝试得到的修补后策略。
4. 原文明确给出 `gr1c patch -f PHI`、`gr1c patch -r i` 以及 `restrict/relax/blocksys` 类 edge-set-change 命令。

### 语义边界

1. 主体仍是有限离散变量上的 `GR(1)`，连续系统需要先通过离散抽象进入该框架。
2. 整数变量在实现中编码为 bitvectors，本体语义仍落回有限布尔 `BDD` 游戏。
3. 增量修补围绕 goals 和 game graph 的局部变化，不等价于任意 `LTL` 规格重写。
4. `Promela` 输出主要用于对综合结果做后验模型检查，不改变 synthesis 本身的语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `GR(1)` 活性规格 | `$\bigwedge_j \Box\Diamond \psi^{env}_j \Rightarrow \bigwedge_i \Box\Diamond \psi^{sys}_i$` | 工具的核心输入片段。 |
| 游戏骨架 | `$G = (X,Y,\Theta_e,\Theta_s,\rho_e,\rho_s,\ldots)$` | 依据原文描述整理出的 synthesis game 对象。 |
| sublevel 进度 | `$\mathrm{rank}_i(s') < \mathrm{rank}_i(s)$` | 解释 `sysnext` 为什么返回某些系统后继。 |
| 增量修补 | `$S' = \mathrm{patch}(S,\Delta)$` | 对目标或 edge set 变化复用既有策略。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 输出策略本质上是 finite strategy automaton。 |
| 事件 / 触发 | 很强 | 输入/输出变量和交替博弈步进是主对象。 |
| 守卫 / 数据 | 中等支持 | 支持有限整数域变量，但通过 bitvector 编码到布尔 `BDD`。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 间接支持 | 通过环境/系统交互建模，不提供并发组件代数。 |
| 时间约束 | 不支持 | 稠密时间需要先离散抽象。 |
| 连续动态 / 随机性 | 不支持 | 原文只把 hybrid systems 作为可通过离散抽象接入的上游场景。 |
| 可执行 / 可验证性 | 很强 | 支持交互查询、策略输出、`JSON` 集成和 `Promela` 后验检查。 |

### 形式化问题与性质

1. `gr1c` 的核心价值不在于重新定义 `GR(1)`，而在于把求解器内部状态开放成可查询对象。
2. 对需求到状态机建模而言，交互式 fixed-point 查询可作为 LLM 生成规格后的调试入口。
3. 增量修补对反复修改目标的机器人任务规划很关键，因为它避免了每次从头综合。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `ENV/SYS` 变量声明。
2. `ENVINIT/SYSINIT` 初始约束。
3. `ENVTRANS/SYSTRANS` 转移约束。
4. `ENVGOAL/SYSGOAL` 活性目标。
5. edge-set-change file 中的 `restrict`、`relax`、`blocksys` 修补命令。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `gr1c` plaintext 规格文件。
2. `BDD/CUDD` 内部状态集合。
3. explicit strategy graph。
4. `JSON` 输出。
5. `Promela` 输出。

### 交换与互操作

1. `TuLiP` 可把自身的 hybrid / temporal-logic planning 问题部分交给 `gr1c`。
2. `Promela` 输出让 `Spin` 可复核综合策略。
3. `JSON` 输出允许下游工具消费策略结构，而不依赖人读图。

## 配套基础设施

- 建模/编辑工具：命令行 `gr1c` 与 plaintext specification。
- 解析/交换/元模型支持：`ENV/SYS` 分块语法、edge-set-change file、`JSON` strategy output。
- 仿真/执行支持：支持显式策略输出和交互式查询，但不主打嵌入式 runtime。
- 验证/分析支持：realizability、winning-set fixed point、sublevel-set strategy construction、`Promela/Spin` 后验检查。
- 代码生成/转换支持：输出 `Promela`，并可生成可供其他工具使用的标准数据格式。
- 标准化或社区生态：开源仓库、`CUDD`、`TuLiP` 生态与 robotics temporal-logic planning 研究线。

## 适用场景与需求前提

### 适用场景

适合 `GR(1)` 反应式控制器综合、机器人任务目标热替换、需求规格调试、以及需要把 fixed-point 中间结果暴露给研究人员的工具链实验。

### 需求前提

1. 需求应能压成环境假设与系统保证的 `GR(1)` 结构。
2. 输入输出变量最好是布尔或有限整数域。
3. 若系统来自连续物理世界，需要先有可靠离散抽象。
4. 若使用增量修补，规格变化最好局限在 liveness goals 或局部转移集变化上。

### 不适用或高成本场景

如果需求本身需要一般 `LTL`、定量 payoff、稠密时间博弈或大规模无限数据域，`gr1c` 不能直接承载，需要换更丰富的 synthesis backend 或先做抽象。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`gr1c` 更强调交互式 fixed-point 查询、`Promela/JSON` 输出和增量 patch；相对 [tulip-a-software-toolbox-for-receding-horizon-temporal-logic-planning/desc.md](../tulip-a-software-toolbox-for-receding-horizon-temporal-logic-planning/desc.md)，`TuLiP` 是上游规划工具箱，`gr1c` 是其中可被调用的 `GR(1)` 求解器；相对 [a-high-level-ltl-synthesis-format-tlsf-v11/desc.md](../a-high-level-ltl-synthesis-format-tlsf-v11/desc.md)，`TLSF` 是规格格式标准，`gr1c` 是具体求解与策略修补基础设施。

## 与本研究的关系

### 对 Project 1 的价值

`gr1c` 对“需求到状态机自动建模”的价值在于提供了一条可验证的后端链路：如果 LLM 能把需求压成 `GR(1)` 假设/保证，那么后端不仅能生成策略自动机，还能暴露 sublevel sets 供调试、修复和解释。

### 可复用启发

1. LLM 生成规格后，交互式查询可以帮助定位“为什么不可实现”或“为什么策略这样走”。
2. 增量修补适合迭代式需求变更，与本仓库的生成-验证-修复闭环高度契合。
3. `Promela` 输出提供了把 synthesis 结果再交给 model checking 复核的工程模式。

## 重要的相关工作

1. `Slugs`：同属 `GR(1)` 综合工具线。
2. `TuLiP`：上游 temporal-logic planning 工具箱。
3. `CUDD`：`BDD` fixed-point 求解的核心后端。
4. `Spin/Promela`：策略输出后的后验模型检查链路。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 关键特性：`GR(1)`、`BDD` fixed point、interactive query、incremental patch、`JSON/Promela` 输出。
- 构造方式：`GR(1)` spec -> winning-set computation -> sublevel-set strategy -> interactive / incremental / checked output。
- 基础设施：`gr1c`、`CUDD`、`TuLiP` wrapper、`Spin/Promela`。
- 对状态机族演化树而言，它是 `GR(1)` / finite strategy automaton 的工具链侧证，不单独形成新的家族节点。
