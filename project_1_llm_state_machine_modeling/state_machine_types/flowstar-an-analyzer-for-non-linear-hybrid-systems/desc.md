# Flow*：非线性混成系统分析器 / Flow*: An Analyzer for Non-linear Hybrid Systems

## 基本信息

- 标题：Flow*: An Analyzer for Non-linear Hybrid Systems
- 中文标题：Flow*：非线性混成系统分析器
- 作者：Xin Chen，Erika Abraham，Sriram Sankaranarayanan
- 发表：*Computer Aided Verification*，pp. 258-263，2013
- DOI：`10.1007/978-3-642-39799-8_18`
- 链接：https://home.cs.colorado.edu/~srirams/papers/cav2013-flowstar.pdf
- 形式主义：`Non-linear Hybrid Systems / Taylor-Model Flow*`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：non-linear flowpipe verification tool
- 工具/实现获取方式：原文明确给出在线发布页，包含 `Flow*` source code 与本文 benchmark。
- 标准/格式获取方式：承载方式是 hybrid system model file 与 specification file，输出 `TM` flowpipes、plotting files 与 safety results；原文未给中立交换标准。

## 简报

这篇论文的核心价值，是把非线性混成系统的验证从“少量数学原型”推进成可复用工具链。`Flow*` 不再局限于线性 hybrid systems，而是用 Taylor models 做连续演化的 guaranteed approximation，再通过 domain contraction、range over-approximation、adaptive steps / orders 与 template directions 处理 guards、transitions 和 unsafe-set checking。

- 形式主义定位：面向 non-linear hybrid systems 的 flowpipe-based verification 路线，而不是新的状态机语言。
- 构造方式简述：输入 hybrid model file 与 specification file，生成 `TM` flowpipes，并在给定时间界 `[0,T]` 与最大 jump 深度 `J` 下检查 unsafe intersection。
- 基础设施与场景简述：依托 model parser、`TM` integrator、TM arithmetic、image computation、TM analyzer 与 plotting chain，服务非线性 ODE / hybrid benchmark 的安全验证。

```text
non-linear hybrid model -> Taylor-model flowpipes -> guard/image computation -> unsafe-set checking -> safe / unsafe / plot
```

## 形式主义定义与核心对象

### 定义对象

论文把 `Flow*` 的工作对象固定成：

1. 具有多个 modes 的 non-linear hybrid systems。
2. 每个 mode 上的 polynomial / non-linear dynamics。
3. discrete transitions 与 guard sets。
4. unsafe set specification。
5. 给定时间界 `[0,T]` 与最大 jump 深度 `J` 的 bounded verification 问题。

### 核心抽象

原文没有重新教科书式给出完整 hybrid-automaton 元组，但根据 paper 明确列出的输入文件结构，可保守整理为：

$$
H = (Loc, X, Flow, Inv, E, Guard, Reset, \Theta)
$$

上式中的符号逐项解释如下：

1. `Loc` 是 modes / locations 集合。
2. `X` 是连续变量集合。
3. `Flow` 为每个 mode 指派 non-linear dynamics。
4. `Inv` 是 mode invariants。
5. `E` 是 discrete transitions 集合。
6. `Guard` 是 transition guard sets。
7. `Reset` 是 transition image / reset 规则。
8. `\Theta` 是初始状态集合。

`Flow*` 真正操作的核心对象不是普通 polyhedron，而是 Taylor-model flowpipe。论文用 bounded problem 直接刻画：

$$
Reach_H([0,T], J)
$$

上式中的符号逐项解释如下：

1. `H` 是输入 hybrid system。
2. `[0,T]` 是给定时间范围。
3. `J` 是允许的最大 jump 深度。
4. 工具返回的是这个 bounded reachable set 的 over-approximation。

安全检查则可保守写成：

$$
\left(\bigcup_{i=0}^{k} F_i\right) \cap U = \emptyset
$$

上式中的符号逐项解释如下：

1. `F_i` 是第 `i` 段 Taylor-model flowpipe segment。
2. `U` 是 unsafe set。
3. 若并集与 `U` 无交，则在给定 `[0,T], J` 下证明安全。

### 一个最小例子与通俗解释

论文里既有连续系统 benchmark，也有 navigation 与 artificial pancreas 一类 hybrid benchmark。把最小直觉压缩一下：

1. 某个 mode 里，连续变量按非线性 ODE 演化。
2. `Flow*` 不直接做数值点采样，而是把一整段轨迹近似成一个 Taylor-model “流管”。
3. 当流管可能撞到 guard 时，工具用 domain contraction 与 range over-approximation 来算 jump image。
4. 最终只要整根流管都不碰 unsafe set，就能在给定时间界内证明安全。

通俗地说，`Flow*` 像“给非线性混成系统套上一层带误差证明的流形外壳”。你关心的不是某条仿真曲线，而是整束可能轨迹有没有触碰危险区域。

### 运行 / 接受 / 转移语义

论文的连续部分围绕 Taylor models 与 flowpipe construction 展开。其核心语义可保守整理为：

$$
Reach_H([0,T], J) \subseteq \bigcup_{i=0}^{k} F_i
$$

上式中的符号逐项解释如下：

1. `F_i` 是由 `TM` integrator 产生的第 `i` 段 flowpipe。
2. `k` 由 step-size、time horizon 与 jump splitting 共同决定。
3. 整个并集 over-approximates bounded reachable states。

对于离散跳转，论文强调两类关键操作：

$$
\text{Image} = \text{DomainContraction} \circ \text{RangeOverApprox}
$$

上式中的符号逐项解释如下：

1. `DomainContraction` 通过收缩初始条件与时间区间来逼近 guard intersection。
2. `RangeOverApprox` 把 Taylor model 转成 template polyhedron 或 zonotope 等更容易做 guard 计算的表示。
3. 两者结合后再把结果转回 Taylor model，供下一段 flowpipe 继续传播。

### 语义边界

这篇论文的边界也很明确：

1. 它主打 bounded-time safety，而不是一般无界时域性质。
2. 连续动力学虽然允许 non-linear，但实现上重点落在 polynomial / Taylor-model friendly systems。
3. 输出是 over-approximate flowpipes，不是 exact reachable set。
4. 如果模型主要是纯离散协议或简单线性时钟系统，`SpaceEx / UPPAAL` 一类工具会更自然。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| bounded reachable set | `$Reach_H([0,T], J)$` | 工具明确只求时间界与 jump 深度界下的可达集。 |
| flowpipe 覆盖 | `$Reach_H([0,T], J) \subseteq \bigcup_i F_i$` | `Flow*` 输出的是 sound over-approximation。 |
| safety check | `$\left(\bigcup_i F_i\right)\cap U = \emptyset$` | unsafe-set intersection 是工具主问题。 |
| image computation | `$\text{Image} = \text{DomainContraction} \circ \text{RangeOverApprox}$` | guard / transition 处理的核心路线。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | modes 与 jumps 组成 hybrid 骨架。 |
| 事件 / 触发 | 强支持 | guards / transitions 明确建模。 |
| 守卫 / 数据 | 很强 | guard intersection 与 unsafe set checking 是第一等对象。 |
| 层次 | 弱支持 | 主体不是层次状态机。 |
| 并发 / 同步 | 弱到中 | 重点不在协议交互，而在连续/混成演化。 |
| 时间约束 | 很强 | bounded horizon 与 step-size control 是核心。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 主打 non-linear ODE 的 sound approximation。 |
| 可执行 / 可验证性 | 很强 | model parser、TM integrator、image computation、plotting chain 完整。 |

### 形式化问题与性质

1. `Flow*` 的核心不在“又一个 hybrid parser”，而在 Taylor-model flowpipe 这条 method line。
2. adaptive step sizes、adaptive TM orders 与 preconditioning 反映出 non-linear integration 的脆弱性和工具化收束策略。
3. domain contraction + range over-approximation 的组合，解释了它为什么能比单一技巧更稳地处理 guard intersections。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 写 hybrid system model file，描述 modes、dynamics 与 transitions。
2. 写 specification file，包含 state-space / unsafe-set 信息。
3. 运行 `Flow*`，指定 `[0,T]` 与 jump depth `J`。
4. 查看 `TM` flowpipes、图形输出与 safety result。

### 机器可处理承载方式

机器可处理承载方式包括：

1. model file。
2. specification file。
3. `TM` flowpipe files。
4. plotting files 与 result files。

### 交换与互操作

这篇论文的互操作重点不在开放标准，而在工具链复用：

1. `TM` output 可以被 `Flow*` 自己再次读取，支持增量性质检查。
2. range over-approximation 会暂时转入 template polyhedra 或 zonotopes 等表示。
3. 这种“内部多表示切换”比静态文件交换更重要。

## 配套基础设施

- 建模/编辑工具：以 `Flow*` parser 与文本模型为主。
- 解析/交换/元模型支持：model/specification files + `TM` intermediate outputs；无中立交换标准。
- 仿真/执行支持：`TM` integrator 提供 guaranteed integration。
- 验证/分析支持：Taylor-model flowpipe construction、domain contraction、range over-approximation、unsafe checking。
- 代码生成/转换支持：不强调代码生成；重点是 flowpipe/analysis pipeline。
- 标准化或社区生态：原文明确给出 source code 与 benchmark 发布页。

## 适用场景与需求前提

### 适用场景

适合非线性 continuous / hybrid systems 的 bounded-time safety verification，例如 navigation、artificial pancreas 与其他 polynomial ODE 主导的 CPS。

### 需求前提

1. 动力学最好可由 Taylor-model 方法稳定近似。
2. 需要显式给出 unsafe set 与 bounded time horizon。
3. 允许接受 sound over-approximation，而不是 exact reachability。
4. 若含跳转，guards 与 reset 需要可结构化处理。

### 不适用或高成本场景

若系统主体是纯离散状态机、纯接口协议或特别高阶的非解析连续动力学，`Flow*` 并不是最经济的路线。

## 与相邻形式主义的关系

相对 [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)，`Flow*` 把 focus 从 affine reachability 推到 non-linear flowpipe；相对 [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)，它不再坚持 polyhedral exactness，而是接受 Taylor-model over-approximation；相对 [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)，它更靠近通用 hybrid system 后端，而不是 `Stateflow` 专用入口。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果 `project_1` 未来生成的模型必须覆盖非线性连续动力学，那验证后端不能只考虑 `HyTech / PHAVer / SpaceEx` 一类线性工具，还要预留 Taylor-model route。

### 作为目标形式主义还是中间表示

更像非线性验证后端的方法路线，而不是面向用户的中立状态机表示。

### 对需求到模型生成的启发

1. 若要接 `Flow*`，自然语言需求最终必须转成 mode、ODE、guards、unsafe set 与 time horizon。
2. 生成模型时要尽量把连续部分写得“Taylor-model friendly”，不要把关键语义藏在黑盒函数里。
3. bounded-time safety 需要在生成阶段就一起结构化，而不是验证时再临时补。

### 现实限制

`Flow*` 很适合非线性安全边界，但如果需求超出 bounded-time safety 或需要更强 compositional semantics，它并不提供万能答案。

## 重要的相关工作

- [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)：更偏 affine / scalable reachability 的平台路线。
- [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)：更偏 polyhedral symbolic verification 的前一代路线。
- [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)：混成验证工具母线起点。
- [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)：工业 `Stateflow` 到 hybrid verification 的另一条 method line。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Non-linear Hybrid Systems / Taylor-Model Flow*`
- 论文角色：non-linear flowpipe verification tool
