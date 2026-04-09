# TEMPEST：概率环境中的反应式系统与 Shield 综合工具 / TEMPEST - Synthesis Tool for Reactive Systems and Shields in Probabilistic Environments

## 基本信息

- 标题：TEMPEST - Synthesis Tool for Reactive Systems and Shields in Probabilistic Environments
- 中文标题：TEMPEST：概率环境中的反应式系统与 Shield 综合工具
- 作者：Stefan Pranger，Bettina Konighofer，Lukas Posch，Roderick Bloem
- 发表：*Automated Technology for Verification and Analysis*，pp. 222-228，2021
- DOI：`10.1007/978-3-030-88885-5_15`
- 链接：https://doi.org/10.1007/978-3-030-88885-5_15
- 形式主义：`stochastic multi-player games / shielding / rPATL / Tempest`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：reactive-system and shield synthesis platform for probabilistic environments
- 工具/实现获取方式：原文明确给出工具主页 `http://www.tempest-shielding.xyz`，并说明提供源代码、Docker image 与 examples。
- 标准/格式获取方式：建模入口采用 `PRISM-games` 语言，性质语言基于 `rPATL` 并扩展 `PreSafety / PostSafety / Optimal` shield syntax；它不是独立交换标准。

## 简报

`TEMPEST` 补的是 reactive synthesis 里一条更偏运行时保障和概率环境的路线。它既能从 stochastic game 综合 reactive system，也能综合 shield。这里的 shield 不是离线证明器，而是一个运行时 enforcement module：在环境不确定、系统可能犯错的情况下，要么限制系统动作，要么直接覆盖系统输出，并尽量少干预。

- 形式主义定位：以 stochastic multi-player games 为语义内核的 reactive synthesis / shielding 工具链，而不是新的状态机语言。
- 构造方式简述：先用 `PRISM-games` 建模 turn-based stochastic game，再用 `rPATL` 或扩展 shield syntax 指定 qualitative / quantitative objective，最后输出 memoryless deterministic strategy 作为 controller 或 shield。
- 基础设施与场景简述：依托 `Storm` code base、`PRISM-games` modeling language、value iteration 和 strategy export，服务机器人规划、交通控制、安全强化学习与 runtime enforcement。

```text
probabilistic environment model -> stochastic game -> rPATL / shield objective -> strategy synthesis -> controller or pre/post-shield
```

## 形式主义定义与核心对象

### 定义对象

论文聚焦以下对象：

1. turn-based stochastic multi-player games；
2. player coalitions 与 strategy；
3. `rPATL` qualitative / quantitative properties；
4. pre-safety / post-safety / optimal shields；
5. `Tempest` 输出的 memoryless deterministic strategy。

### 核心抽象

原文没有把 `SMG` 写成统一数学元组，但根据其 `PRISM-games` 建模说明，可保守整理为：

$$
G = (S, S_1, S_2, S_P, Act, P)
$$

上式中的符号逐项解释如下：

1. `S` 是游戏状态集合。
2. `S_1` 与 `S_2` 分别是两个对抗 coalition 控制的状态子集。
3. `S_P` 是概率分支状态集合。
4. `Act` 是可选动作集合。
5. `P` 给出动作选择后的概率转移。
6. 这是基于原文对 turn-based stochastic multi-player games 的描述做的保守整理，不是原文逐字元组。

原文直接给出反应式系统综合性质示例：

$$
\langle\!\langle 1,2 \rangle\!\rangle P_{\max = ?}[F\ target]
$$

以及

$$
\langle\!\langle 1,2 \rangle\!\rangle R^r_{\max = ?}[S]
$$

上式中的符号逐项解释如下：

1. `\langle\!\langle 1,2 \rangle\!\rangle` 表示同一 coalition 内协作的玩家集合。
2. `P_{\max = ?}[F\ target]` 表示最大化最终到达 `target` 的概率。
3. `R^r_{\max = ?}[S]` 表示最大化 long-run average reward `r`。
4. 这两类公式对应 controller synthesis 的 qualitative / quantitative 目标。

对于 shielding，原文给出扩展语法：

$$
\langle PreSafety,\gamma = 0.9 \rangle \langle\!\langle shield \rangle\!\rangle P_{\max = ?}[G^{\le 14}\ \neg crash]
$$

$$
\langle PostSafety,\lambda = 0.95 \rangle \langle\!\langle shield \rangle\!\rangle P_{\max = ?}[G^{\le 14}\ \neg crash]
$$

以及

$$
\langle Optimal \rangle \langle\!\langle shield \rangle\!\rangle R^r_{\min = ?}[S]
$$

上式中的符号逐项解释如下：

1. `PreSafety` 表示 pre-shield，在系统之前限制可选动作。
2. `PostSafety` 表示 post-shield，在系统之后覆盖输出。
3. `\gamma` 是绝对阈值，`\lambda` 是相对阈值。
4. `Optimal` 表示以 long-run reward 为目标的最优 shield。

### 一个最小例子与通俗解释

论文里的直觉例子是 warehouse robot：

1. 机器人在仓库里要取货送货，环境里还存在其他机器人与阻塞走廊。
2. controller synthesis 负责找“长期平均路径代价更好”的控制策略。
3. safety-shield 负责在有限 horizon 内强制避免碰撞。
4. optimal-shield 则是在“尽量少干预”和“不要让系统表现太差”之间找平衡。

通俗地说，`TEMPEST` 像是把“规划器”“安全员”“运行时拦截器”三件事合成到同一个 stochastic-game backend 上：同一套模型既可出 controller，也可出 shield。

### 运行 / 接受 / 转移语义

原文明确说：

1. 在每个状态，恰有一个 player 选择一个可用的 probabilistic transition。
2. strategy 决定 player 如何选边。
3. 工具输出的是 memoryless deterministic strategy。
4. 该 strategy 既可以实现 reactive system，也可以实现 shield。

对 shield，原文用 safety-value 描述动作是否应被阻塞。可保守写成：

$$
sv_k(s,a) = \max \Pr_s(G^{\le k}\ safe \mid a)
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态。
2. `a` 是候选动作。
3. `sv_k(s,a)` 表示在未来 `k` 步内保持安全的最大概率。
4. 这是根据原文“safety-value of an action”含义做的保守整理，不是逐字公式。

由此可把 shield 决策规则压成：

$$
sv_k(s,a) \ge \gamma \quad \text{or} \quad sv_k(s,a) \ge \lambda \cdot \max_b sv_k(s,b)
$$

上式中的符号逐项解释如下：

1. `\gamma` 是绝对阈值。
2. `\lambda` 是相对阈值。
3. 第一种规则对应 absolute comparison。
4. 第二种规则对应 relative comparison。

### 语义边界

1. 论文当前支持 perfect-information 的 stochastic games。
2. 目标是 turn-based setting，不是一般并发博弈模型。
3. 输出策略是 memoryless deterministic 的，不覆盖更广的 finite-memory / stochastic update 策略。
4. 作者也明确把 partial information 留作 future work。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 控制器综合目标 | `$\langle\!\langle 1,2 \rangle\!\rangle P_{\max=?}[F\ target]$` | 求 coalition 的最大到达概率策略。 |
| 长期奖励目标 | `$\langle\!\langle 1,2 \rangle\!\rangle R^r_{\max=?}[S]$` | 求最大 long-run average reward 策略。 |
| safety shield | `$\langle PreSafety,\gamma \rangle \langle\!\langle shield \rangle\!\rangle P_{\max=?}[G^{\le k}\ safe]$` | pre-shield 根据绝对阈值阻塞动作。 |
| optimal shield | `$\langle Optimal \rangle \langle\!\langle shield \rangle\!\rangle R^r_{\min=?}[S]$` | 用 reward 最小化综合最优干预策略。 |
| safety-value 规则 | `$sv_k(s,a) \ge \gamma$` 或 `$sv_k(s,a) \ge \lambda \max_b sv_k(s,b)$` | shield 以概率阈值为依据允许或覆盖动作。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 底层是可综合的 stochastic game。 |
| 事件 / 触发 | 很强 | 输入输出动作是 shield/controller synthesis 的核心。 |
| 守卫 / 数据 | 中等支持 | 通过 `PRISM-games` 模型表达，而非富数据 DSL。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 主要依赖 `PRISM-games` 的模块同步与 game semantics。 |
| 时间约束 | 弱支持 | 不是 timed-game 主线，重点是 probabilistic environments。 |
| 连续动态 / 随机性 | 很强 | 环境随机性与 quantitative objective 是核心。 |
| 可执行 / 可验证性 | 很强 | 直接导出策略并可作为 shield 或 controller 使用。 |

### 形式化问题与性质

1. `TEMPEST` 的独特之处在于同一 backend 同时服务 controller synthesis 与 shield synthesis。
2. 与一般 reactive synthesis 工具相比，它把 stochastic environments 作为一等对象。
3. 对 `project_1` 而言，它为“生成后如何加 shield / runtime enforcement”提供了非常直接的工具证据。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `PRISM-games` 模型；
2. coalition 指定；
3. `rPATL` 性质；
4. `PreSafety / PostSafety / Optimal` shield 性质扩展。

### 机器可处理承载方式

机器可处理承载方式包括：

1. turn-based stochastic multi-player games；
2. reward structures；
3. strategy tables；
4. pre-shield allowed-action lists；
5. post-shield forwarded-action mappings。

### 交换与互操作

这篇论文的互操作重点在：

1. 直接复用 `PRISM-games` modeling language；
2. 构建在 `Storm` code base 之上；
3. 输出的 strategy 可以直接作为 synthesized system 或 shield 的实现骨架。

## 配套基础设施

- 建模/编辑工具：依赖 `PRISM-games` 文本建模，不主打独立图形编辑器。
- 解析/交换/元模型支持：支持 `PRISM-games` 模型与扩展性质语法。
- 仿真/执行支持：重点是 strategy synthesis，不是单独 simulator。
- 验证/分析支持：qualitative objectives、mean-payoff objectives、shield synthesis、strategy extraction。
- 代码生成/转换支持：输出策略本身就是部署前的实现骨架。
- 标准化或社区生态：与 `Storm`、`PRISM-games`、shielding 和 stochastic-game synthesis 社区直接相连。

## 适用场景与需求前提

### 适用场景

适合存在不确定环境、需要 correct-by-construction controller、或希望在运行时对系统行为做最小必要干预的场景。

### 需求前提

1. 系统与环境交互必须能抽成 turn-based stochastic game。
2. 性质最好能写成 `rPATL`、safety horizon 或 mean-payoff reward 目标。
3. 若做 shield，需要明确定义哪些动作可拦截、哪些输出可覆盖。
4. 当前更适合 perfect-information setting。

### 不适用或高成本场景

如果任务依赖连续动力学主导、强部分可观测性或复杂有限记忆策略，当前 `TEMPEST` 不是最自然入口。

## 与相邻形式主义的关系

相对 [prism-games-a-model-checker-for-stochastic-multi-player-games/desc.md](../prism-games-a-model-checker-for-stochastic-multi-player-games/desc.md)，`PRISM-games` 更偏 verification / game solving backend，而 `TEMPEST` 更强调 synthesis 与 shield 输出；相对 [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)，`UPPAAL-Tiga` 是 timed games，`TEMPEST` 是 stochastic games；相对 [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)、[slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md) 和 [spectra-a-specification-language-for-reactive-systems/desc.md](../spectra-a-specification-language-for-reactive-systems/desc.md)，这些条目聚焦离散 `LTL/GR(1)` reactive synthesis，而 `TEMPEST` 引入了概率环境与 shielding。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明自动生成的状态机模型不仅可做离线 verification，还可进一步综合成 runtime shield。
2. 对后续 repair 研究，它提供了“先保证不违规，再最小干预”的一个工程锚点。
3. 对控制系统需求建模，这类 shield objective 很适合作为安全性质的更细化 operationalization。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像 synthesis / enforcement backend，而不是前端状态机语言。

### 对需求到模型生成的启发

1. 需求可先拆为 qualitative safety 与 quantitative performance 两层。
2. 生成的模型未来可以直接接入 shield synthesis，而不是只停在“能验证”。
3. 概率环境建模让“理想假设下正确”升级为“随机扰动下仍有保障”。

## 重要的相关工作

- [prism-games-a-model-checker-for-stochastic-multi-player-games/desc.md](../prism-games-a-model-checker-for-stochastic-multi-player-games/desc.md)：stochastic-game verification backend 的重要近邻。
- [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)：timed-game synthesis 的经典工具条目。
- [spectra-a-specification-language-for-reactive-systems/desc.md](../spectra-a-specification-language-for-reactive-systems/desc.md)：偏离散 reactive-synthesis 前端的代表条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 结论：这是一篇非常典型的 stochastic reactive synthesis / shielding 方法条目，适合作为概率环境下 controller synthesis 与 runtime enforcement 路线的关键工具证据入账。
