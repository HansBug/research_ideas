# Ymer：统计模型检查器 / Ymer: A Statistical Model Checker

## 基本信息

- 标题：Ymer: A Statistical Model Checker
- 中文标题：Ymer：统计模型检查器
- 作者：Håkan L. S. Younes
- 发表：*Computer Aided Verification*，`LNCS 3576`，pp. 429-433，2005
- DOI：`10.1007/11513988_43`
- 链接：https://doi.org/10.1007/11513988_43
- 形式主义：`statistical model checking / CSL / PCTL / Ymer`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：statistical probabilistic model checker / distributed acceptance-sampling engine
- 工具/实现获取方式：原文明确说明 `Ymer` 以 `C` 和 `C++` 实现，部分 `CTMC` 数值分析代码来自 `PRISM`，并给出下载入口 `http://www.cs.cmu.edu/~lorens/ymer.html`。
- 标准/格式获取方式：原文明确说明 `Ymer` 当前支持使用 `PRISM` 输入语言扩展描述 time-homogeneous generalized semi-Markov processes，并直接支持 `PCTL/CSL` 性质。

## 简报

这篇论文的关键价值，在于把“概率模型检查不一定非要先构完状态空间”这条路线做成了工具。`Ymer` 以离散事件仿真和 acceptance sampling 为核心，对 `PCTL/CSL` transient properties 给出统计置信意义下的验证结论，并进一步支持 distributed sampling 与 nested probabilistic queries。

- 形式主义定位：概率/随机系统的统计模型检查路线，而不是新的随机状态机本体。
- 构造方式简述：把模型写成 `PRISM` 风格输入，再通过 discrete-event simulation 采样路径，用 acceptance sampling 或 mixed numeric/statistical 方法判断性质。
- 基础设施与场景简述：依托 `C/C++`、`PRISM` front-end、master/slave distributed sampling、`CUDD` 和 hybrid `CTMC` engine，服务大状态空间随机离散事件系统分析。

```text
stochastic model + CSL/PCTL property -> simulation paths -> acceptance sampling / mixed solving -> probabilistic verdict
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `Ymer`：

1. stochastic discrete event systems；
2. `PCTL` 与 `CSL` 性质；
3. discrete-event simulation；
4. acceptance sampling；
5. distributed master/slave architecture；
6. numerical/statistical mixed solving for nested properties。

### 核心抽象

论文直接使用的性质骨架是：

$$
P_{\ge \theta}[\varphi]
$$

上式中的符号逐项解释如下：

1. `$\varphi$` 是路径性质。
2. `$\theta$` 是概率阈值。
3. `$P_{\ge \theta}[\varphi]$` 表示满足 `$\varphi$` 的路径测度至少为 `$\theta$`。
4. 这是 `CSL/PCTL` 里最基本的概率判断骨架。

论文给出的示例之一是：

$$
\neg P_{\ge 0.01}[\top U_{[0,15.07]}\ faulty=n]
$$

上式中的符号逐项解释如下：

1. `$\top$` 表示真路径前缀。
2. `$U_{[0,15.07]}$` 是带时间区间的 until。
3. `faulty=n` 表示在 15.07 秒内达到 `n` 个 server 失效。
4. 外层否定表示该事件发生概率不应达到 0.01。

结合论文对工具流程的描述，可把 `Ymer` 的求解骨架保守整理为：

$$
\mathcal{Y} = (M, \Phi, Sim, AS, Num)
$$

上式中的符号逐项解释如下：

1. `$M$` 是随机系统模型。
2. `$\Phi$` 是待检验的 `PCTL/CSL` 性质。
3. `$Sim$` 是离散事件仿真器。
4. `$AS$` 是 acceptance sampling 程序。
5. `$Num$` 是针对 `CTMC` 或 nested operator 的数值求解组件。
6. 这是根据论文架构做的保守抽象，不是作者显式给出的工具元组。

### 一个最小例子与通俗解释

论文给了一个 polling system 例子，可压成：

$$
m_1 = 1 \to P_{\ge 0.5}[\top U_{[0,20]} poll_1]
$$

上式中的符号逐项解释如下：

1. `$m_1 = 1$` 表示站点 1 当前缓冲区为满。
2. `$poll_1$` 表示服务器轮询到站点 1。
3. 性质要求在 20 时间单位内轮询到站点 1 的概率至少为 0.5。

通俗地说，`Ymer` 像“用大量仿真样本做概率判案的法官”。它不是先把所有状态铺开再精确算，而是不断跑样本路径，看经验观察是否足以让某个概率命题在给定错误界内被接受或拒绝。

### 运行 / 接受 / 转移语义

论文明确把单次路径评估看成 Bernoulli trial。可保守写成：

$$
X_k = 1 \iff \pi_k \models \varphi
$$

上式中的符号逐项解释如下：

1. `$\pi_k$` 是第 `$k$` 条仿真路径。
2. `$X_k$` 是该路径对性质 `$\varphi$` 的观测结果。
3. 若满足性质则记为 1；否则取值为 0。
4. acceptance sampling 就建立在这组 Bernoulli observations 上。

论文还强调 master/slave distributed sampling。可保守写成：

$$
\hat p_N = \frac{1}{N}\sum_{k=1}^{N} X_k
$$

上式中的符号逐项解释如下：

1. `$N$` 是已经接收并按预定顺序处理的样本数。
2. `$\hat p_N$` 是基于样本的性质满足概率估计。
3. slave 只负责生成样本，master 负责汇总与采样判决。
4. 论文特别强调处理顺序必须预先固定，以避免快样本偏置。

### 语义边界

这篇论文的边界主要有：

1. 主线关注 transient probabilistic properties，而非全量 steady-state 体系。
2. 统计方法给的是置信意义下的正确性保证，不是精确穷举证明。
3. 原文的广义对象是 stochastic discrete event systems，但当前前端主要落在 `PRISM` 扩展输入语言。
4. nested probabilistic operator 需要 mixed 或 purely statistical special handling。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 概率性质骨架 | `$P_{\ge \theta}[\varphi]$` | `Ymer` 最核心的判定对象。 |
| 时间有界例子 | `$\neg P_{\ge 0.01}[\top U_{[0,15.07]}\ faulty=n]$` | 用于说明 `CSL` transient property 的典型形态。 |
| 采样观测 | `$X_k \in \{0,1\}$` | 每条仿真路径都会变成一次 Bernoulli observation。 |
| 概率估计 | `$\hat p_N = \frac{1}{N}\sum_{k=1}^{N} X_k$` | distributed acceptance sampling 的统计核心。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 面向随机离散事件系统与 `CTMC/GSMP`。 |
| 事件 / 触发 | 强支持 | 仿真路径由离散事件推进。 |
| 守卫 / 数据 | 条件支持 | 依赖前端模型语言，不是富数据 DSL。 |
| 层次 | 弱支持 | 论文主线不在层次状态机。 |
| 并发 / 同步 | 间接支持 | 只要系统能写成随机离散事件模型即可。 |
| 时间约束 | 强支持 | `CSL` time-bounded until 是核心对象。 |
| 连续动态 / 随机性 | 支持随机性，不支持连续动态 | 主线是随机离散事件系统。 |
| 可执行 / 可验证性 | 很强 | 仿真、distributed sampling、mixed numerical/statistical solving 已工具化。 |

### 形式化问题与性质

1. `Ymer` 的关键不是“再有一种概率逻辑”，而是“如何在状态空间过大时仍能做模型检查”。
2. 它把 acceptance sampling 明确收编进模型检查工具流。
3. 对本文库而言，它补的是统计概率模型检查的早期工具母线。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 使用 `PRISM` 输入语言扩展描述随机系统。
2. 编写 `PCTL/CSL` 性质。
3. 选择 statistical、mixed 或 numerical 解法。
4. 运行 `Ymer` 获取统计 verdict 或估计值。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PRISM`-style input language；
2. `PCTL/CSL` property strings；
3. 分布式 master/slave observation protocol；
4. `BDD/MTBDD` data structures for the hybrid engine。

### 交换与互操作

`Ymer` 的互操作重点不在中立交换标准，而在分析组件复用：

1. 前端沿用 `PRISM` 风格建模语法。
2. `CTMC` 数值求解部分直接复用 `PRISM` hybrid engine。
3. 分布式 sampling 则通过 master/slave 架构横向扩容。

## 配套基础设施

- 建模/编辑工具：`PRISM` 风格模型输入与 property 编写。
- 解析/交换/元模型支持：`PRISM` input extension、`PCTL/CSL` parser、`BDD/MTBDD` 支撑。
- 仿真/执行支持：discrete-event simulation、distributed slave workers。
- 验证/分析支持：acceptance sampling、sequential tests、mixed numerical/statistical nested checking。
- 代码生成/转换支持：不以代码生成为主，重点是模型分析。
- 标准化或社区生态：与 `PRISM`、`ETMCC`、后续 `VESTA/MRMC` 等工具形成早期概率验证对照生态。

## 适用场景与需求前提

### 适用场景

适合大状态空间随机系统、概率时间性质、抽样可行但精确穷举昂贵的研究和工程分析场景。

### 需求前提

1. 模型必须能被稳定仿真。
2. 性质能写成 `PCTL/CSL`。
3. 用户接受 statistical confidence，而不是精确全空间证明。
4. 若使用 distributed mode，需要可并行生成独立样本。

### 不适用或高成本场景

若任务要求严格稳态精确值、完全无误差判定，或模型根本不适合事件仿真，`Ymer` 就不是最佳入口。

## 与相邻形式主义的关系

相对 [vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md](../vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md)，`VESTA` 更强调后续 expected-value analysis 和 language-independent simulator interface，而 `Ymer` 是更早的统计模型检查工具母线；相对 [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)，`PRISM` 更偏精确数值/符号求解，而 `Ymer` 更偏 acceptance-sampling 驱动；相对 [the-ins-and-outs-of-the-probabilistic-model-checker-mrmc/desc.md](../the-ins-and-outs-of-the-probabilistic-model-checker-mrmc/desc.md)，`MRMC` 更偏显式状态数值与 reward 模型，`Ymer` 更偏 simulation-based statistical path analysis。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提示 `project_1`：当模型太大、环境太不确定时，验证后端可以考虑统计抽样而不是只押宝精确穷举。
2. 若未来某些状态机模型要接到随机环境仿真，`Ymer` 这类工具线说明“能仿真”本身就是一种重要基础设施能力。
3. 这也有助于后续“生成-验证-修复”闭环里引入概率置信反馈，而不是只有二值正确/错误。

### 作为目标形式主义还是中间表示

更像概率验证后端与方法路线，而不是最终交付的状态机本体。

## 重要的相关工作

1. [vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md](../vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md)：统计模型检查的后续工具线。
2. [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)：精确概率模型检查平台。
3. [the-ins-and-outs-of-the-probabilistic-model-checker-mrmc/desc.md](../the-ins-and-outs-of-the-probabilistic-model-checker-mrmc/desc.md)：显式状态 reward/probabilistic quantitative backend。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`statistical model checking / CSL / PCTL / Ymer`
- 论文角色：statistical probabilistic model checker / distributed acceptance-sampling engine
- 归类理由：论文主体是在随机状态机/随机事件系统上实现统计模型检查方法，核心贡献落在分析路线与工具实现，而不是新的模型本体。
