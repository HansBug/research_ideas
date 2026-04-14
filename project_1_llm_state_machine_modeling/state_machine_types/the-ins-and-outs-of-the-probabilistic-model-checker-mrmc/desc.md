# MRMC：概率模型检查器的内外机制 / The Ins and Outs of the Probabilistic Model Checker MRMC

## 基本信息

- 标题：The Ins and Outs of the Probabilistic Model Checker MRMC
- 中文标题：MRMC：概率模型检查器的内外机制
- 作者：Joost-Pieter Katoen，Ivan S. Zapreev，Ernst Moritz Hahn，Holger Hermanns，David N. Jansen
- 发表：*2009 Sixth International Conference on the Quantitative Evaluation of Systems*，pp. 167-176，2009
- DOI：`10.1109/QEST.2009.11`
- 链接：https://doi.org/10.1109/QEST.2009.11
- 形式主义：`DTMC / CTMC / DMRM / CMRM / uCTMDP / MRMC`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：probabilistic reward model checker / explicit-state quantitative verification platform
- 工具/实现获取方式：原文明确说明 `MRMC` 以 `C` 实现，按 `GPL` 发布，并可从 `http://www.mrmc-tool.org/` 下载。
- 标准/格式获取方式：原文明确说明输入主要由 `.tra`、`.lab`、`.rew`、`.rewi` 和 `.ctmdp` 文件组成；它不是中立交换标准，而是面向显式状态概率模型的工具输入约定。

## 简报

这篇论文的重点，是把 `MRMC` 从“会算概率的程序”讲成一套完整的 quantitative verification 平台。它不仅支持 `DTMC/CTMC` 的 `PCTL/CSL`，还把 reward model、`uCTMDP`、property-driven bisimulation、精确的 on-the-fly steady-state detection 和 simulation-based `CSL` model checking 一并整合进去。

- 形式主义定位：显式状态概率/奖励模型检查平台，而不是新的概率状态机本体。
- 构造方式简述：用稀疏矩阵和标签/奖励文件描述 `DTMC / CTMC / MRM / uCTMDP`，再由 numerical engines、bisimulation engine 和 simulation engine 驱动性质验证。
- 基础设施与场景简述：依托 shell、input reader、common model-checking core、sparse-matrix backend、bisimulation minimization 和 DES simulation，服务性能、可靠性和 reward-bounded reachability 分析。

```text
explicit probabilistic model -> .tra/.lab/.rew/.rewi/.ctmdp -> numerical / bisimulation / simulation engines -> probability / reward / steady-state results
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `MRMC`：

1. `DTMC / CTMC`；
2. `DMRM / CMRM`；
3. `uCTMDP`；
4. `PCTL / CSL / PRCTL / CSRL`；
5. numerical、bisimulation 和 simulation 三套分析后端。

### 核心抽象

论文给出了工具支持的模型与逻辑对应关系。可把其覆盖模型集合写成：

$$
\mathcal{M} = \{ DTMC, CTMC, DMRM, CMRM, uCTMDP \}
$$

上式中的符号逐项解释如下：

1. `DTMC` 是离散时间 Markov 链。
2. `CTMC` 是连续时间 Markov 链。
3. `DMRM` 是离散时间 Markov reward model。
4. `CMRM` 是连续时间 Markov reward model。
5. `uCTMDP` 是 uniform continuous-time Markov decision process。

相应的性质语言集合可整理为：

$$
\mathcal{L} = \{ PCTL, CSL, PRCTL, CSRL \}
$$

上式中的符号逐项解释如下：

1. `PCTL` 对应离散时间概率性质。
2. `CSL` 对应连续时间概率性质。
3. `PRCTL` 是带 reward 的离散时间逻辑。
4. `CSRL` 是带 reward 的连续时间逻辑。
5. `MRMC` 用这四类逻辑覆盖概率与奖励分析主线。

论文特别强调 time-bounded 和 reward-bounded reachability。可保守写成：

$$
s \models P_{\le \lambda}(\Diamond^{\le t} \Phi)
$$

$$
s \models P_{\le \lambda}(\Diamond^{\le t}_{\le r} \Phi)
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态。
2. `\Phi` 是目标状态谓词。
3. `\Diamond^{\le t}` 表示在时间上界 `t` 内到达目标。
4. `\Diamond^{\le t}_{\le r}` 进一步要求累计 reward 不超过 `r`。
5. `\lambda` 是概率阈值。

### 一个最小例子与通俗解释

论文用一个简单骰子游戏的 `DMRM` 举例：

1. `game.tra` 描述状态转移和概率。
2. `game.lab` 描述状态标签。
3. `game.rew` 描述状态奖励。
4. 用户可以在 shell 里直接输入 `PRCTL` 公式，询问“在有限步数和奖励预算内拿到目标收益的概率是多少”。

通俗地说，`MRMC` 像“面向概率状态图的数值分析工作台”。它不先做复杂高层建模，而是假定你已经有一个显式状态概率模型，然后用很扎实的后端去算概率、代价和稳态。

### 运行 / 接受 / 转移语义

从工具架构角度，论文可保守整理为：

$$
MRMC = (Shell, Reader, Common, Bisim, Num, Sim)
$$

上式中的符号逐项解释如下：

1. `Shell` 是交互式命令行前端。
2. `Reader` 负责读取 `.tra/.lab/.rew/.rewi/.ctmdp` 等文件。
3. `Common` 是公共 model-checking 逻辑层。
4. `Bisim` 是 bisimulation minimization 引擎。
5. `Num` 是数值分析引擎。
6. `Sim` 是离散事件 simulation engine。

对稳态和瞬态分析，论文强调一条重要性质是精确的 on-the-fly steady-state detection。可保守写成：

$$
\Pr_{transient}(t) + \Pr_{goal}(t) + \Pr_{bad}(t) = 1
$$

上式中的符号逐项解释如下：

1. `\Pr_{transient}(t)` 是时间 `t` 时仍留在中性瞬态区的概率质量。
2. `\Pr_{goal}(t)` 是已进入目标吸收区的概率质量。
3. `\Pr_{bad}(t)` 是已进入非目标吸收区的概率质量。
4. 论文通过监测概率质量分布来避免过早 steady-state detection。

### 语义边界

这篇论文的边界主要有：

1. 它是显式状态平台，不是面向高层 DSL 的统一前端。
2. 更大规模 symbolic representation 不是 `MRMC` 的主线，这点和 `PRISM` 不同。
3. 支持的概率模型非常实用，但连续动力学或一般 hybrid semantics 不在覆盖面内。
4. `simulation-based CSL` 仍以已知图结构或既有状态空间信息为前提，不是完全无结构黑盒仿真。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 支持模型族 | `$\mathcal{M} = \{ DTMC, CTMC, DMRM, CMRM, uCTMDP \}$` | `MRMC` 覆盖的概率/奖励模型骨架。 |
| 支持逻辑族 | `$\mathcal{L} = \{ PCTL, CSL, PRCTL, CSRL \}$` | 工具支持的性质语言全集。 |
| 时间有界可达概率 | `$s \models P_{\le \lambda}(\Diamond^{\le t} \Phi)$` | `DTMC/CTMC` 主线查询。 |
| 时间+奖励有界可达概率 | `$s \models P_{\le \lambda}(\Diamond^{\le t}_{\le r} \Phi)$` | 论文强调的 reward-bounded reachability 能力。 |
| 工具架构 | `$MRMC = (Shell, Reader, Common, Bisim, Num, Sim)$` | shell、数值、缩减和仿真后端共同组成平台。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向显式状态概率模型。 |
| 事件 / 触发 | 中等支持 | 通过状态转移与标签文件表达。 |
| 守卫 / 数据 | 弱支持 | 不是高层 guarded-command 语言，主要消费已展开模型。 |
| 层次 | 不支持 | 主线是 flat explicit-state quantitative model checking。 |
| 并发 / 同步 | 间接支持 | 可分析并发系统生成的概率模型，但不直接提供并发建模 DSL。 |
| 时间约束 | 强支持 | `CTMC/uCTMDP` 与 `CSL/CSRL` 支持时间约束分析。 |
| 连续动态 / 随机性 | 随机性很强，连续动态不支持 | 概率/奖励是核心；连续 ODE 不在范围。 |
| 可执行 / 可验证性 | 很强 | numerical、bisimulation 和 simulation 三条分析线都成熟。 |

### 形式化问题与性质

1. `MRMC` 的价值不只是支持更多逻辑，而是把 reward-bounded reachability、bisimulation minimization 和 simulation-based `CSL` 变成同一个平台能力。
2. 它代表了 explicit-state quantitative verification 这一工程路线。
3. 对本文库而言，它补的是 `PRISM/VESTA/Storm` 之外另一条早期概率平台母线。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 先从外部工具或脚本得到显式状态概率模型。
2. 写入 `.tra` 转移文件。
3. 用 `.lab` 指定原子命题标签。
4. 需要 reward 时再写 `.rew/.rewi`。
5. 对 `uCTMDP` 则使用专门的 `.ctmdp` 描述。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `.tra`；
2. `.lab`；
3. `.rew`；
4. `.rewi`；
5. `.ctmdp`；
6. 稀疏矩阵与内部 bitset / splay tree 数据结构。

### 交换与互操作

这篇论文的互操作重点在显式状态后端接口：

1. `MRMC` 很适合作为其他建模工具的 back-end。
2. `PRISM` 等工具甚至可以导出 `MRMC` 输入格式。
3. 它把不同高层概率建模路线收束到共同的显式状态分析层。

## 配套基础设施

- 建模/编辑工具：主要依赖外部前端，`MRMC` 自身以 shell 为主。
- 解析/交换/元模型支持：`.tra/.lab/.rew/.rewi/.ctmdp` 输入协议与稀疏矩阵内部表示。
- 仿真/执行支持：离散事件 simulation engine 支持 `CSL` 仿真模型检查。
- 验证/分析支持：`PCTL/CSL/PRCTL/CSRL`、reward-bounded reachability、bisimulation minimization、steady-state detection。
- 代码生成/转换支持：不以代码生成见长，重点是 back-end quantitative analysis。
- 标准化或社区生态：`GPL` 发布、网站下载入口、与 `PRISM/VESTA/Ymer` 等工具形成对照生态。

## 适用场景与需求前提

### 适用场景

适合已经能构造显式状态概率模型，并且希望分析可达概率、稳态概率、reward/cost 或时间与奖励联合约束的场景。

### 需求前提

1. 系统可以落成 `DTMC / CTMC / MRM / uCTMDP` 之一。
2. 用户接受显式状态输入格式而不是更高层的 DSL。
3. 需求关心概率、稳态或 reward 指标，而不仅是布尔安全性。
4. 若使用 simulation engine，系统应适合离散事件抽样分析。

### 不适用或高成本场景

如果状态空间只能靠强符号压缩、或者对象本身是连续混成系统，`MRMC` 就不是最直接的入口。

## 与相邻形式主义的关系

相对 [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)，`PRISM` 更偏统一语言和 symbolic/numeric 平台，而 `MRMC` 更偏显式状态后端；相对 [vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md](../vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md)，`VESTA` 走统计抽样，`MRMC` 主线是数值 + 精确求解；相对 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)，`Storm` 更现代、更模块化，而 `MRMC` 是早期 reward-bounded explicit-state 平台代表。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明状态机文库里的 quantitative 后端不应只剩 `PRISM` 一条线，还应保留显式状态 reward-model checking 路线。
2. 如果后续需求涉及可靠性、资源消耗、累计代价或稳态风险，`MRMC` 这类平台提供了清晰的后端接口模板。
3. 对生成-验证闭环来说，`.tra/.lab/.rew` 这种薄格式也提示了一种“中间量化验证表示”的可能。

### 作为目标形式主义还是中间表示

它更像概率验证后端平台，而不是最终面向需求建模的前端状态机形式主义。

## 重要的相关工作

- [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)：概率模型检查统一语言平台的经典母线。
- [vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md](../vesta-a-statistical-model-checker-and-analyzer-for-probabilistic-systems/desc.md)：与 `MRMC` 的数值路线形成统计模型检查对照。
- [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：后续更现代的概率平台。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`DTMC / CTMC / DMRM / CMRM / uCTMDP / MRMC`
- 论文角色：probabilistic reward model checker / explicit-state quantitative verification platform
- 核心功能：统一显式状态概率/奖励模型的数值、缩减和仿真验证
- 关键特性：reward-bounded reachability、property-driven bisimulation、precise steady-state detection、simulation-based `CSL`
- 构造方式：explicit-state model -> `.tra/.lab/.rew/.rewi/.ctmdp` -> numerical / simulation analysis
- 基础设施：shell、reader、common checker、bisimulation engine、numerical engines、simulation engine
- 适用场景：性能、可靠性、资源消耗与 reward-bounded verification
- 需求前提：系统需能落成显式状态概率模型并关心 quantitative properties
