# 使用 TimeNET 4.1 的随机 Petri 网建模与评估 / Modeling and Evaluation of Stochastic Petri Nets With TimeNET 4.1

## 基本信息

- 标题：Modeling and Evaluation of Stochastic Petri Nets With TimeNET 4.1
- 中文标题：使用 TimeNET 4.1 的随机 Petri 网建模与评估
- 作者：Armin Zimmermann
- 发表：*Proceedings of the 6th International Conference on Performance Evaluation Methodologies and Tools*，2012
- DOI：`10.4108/valuetools.2012.250263`
- 链接：https://doi.org/10.4108/valuetools.2012.250263
- 形式主义：`eDSPN / SCPN / TimeNET`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：stochastic Petri-net modeling and performance-evaluation environment
- 工具/实现获取方式：原文明确给出 `http://www.tu-ilmenau.de/sse/timenet/` 作为工具、用户手册和更新入口，且说明非商业用途可免费获取。
- 标准/格式获取方式：核心承载包括 TimeNET 自身 XML 模型格式，以及 `eDSPN` 的 `PNML` import/export；对 `SCPN` 仍以工具自有建模环境为主。

## 简报

这篇论文补的是随机 Petri 网工具链里很实用的一支：`TimeNET 4.1`。它既支持标准与彩色随机 Petri 网，又把 steady-state、transient、simulation、rare-event simulation、结构检查、图形界面和 `PNML` 交换格式接到了一起。相比只做某一类 `GSPN` 的求解器，它更像一个长期演进的 stochastic-PN 工作环境。

- 形式主义定位：随机 Petri 网建模与性能评估基础设施，而不是新的网类本体。
- 构造方式简述：先在图形界面中构造 `eDSPN` 或 `SCPN`，再按模型类和延迟分布选择数值分析或仿真模块。
- 基础设施与场景简述：依托 Java GUI、`eDSPN/SCPN` 分析器、simulation modules 与 `PNML`，服务制造、通信和一般离散事件系统的性能评估。

```text
stochastic Petri-net model -> structural checks / simulation / numerical analysis -> transient or stationary measures
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `eDSPN`：extended deterministic and stochastic Petri nets。
2. `SCPN`：colored stochastic Petri nets。
3. `TimeNET` 图形建模与分析环境。
4. steady-state / transient 数值分析与 simulation modules。
5. `PNML` import/export 与工具私有 XML 格式。

### 核心抽象

论文明确给出 TimeNET 当前支持的主要网类，可压成：

$$
\mathcal{C}_{TimeNET} = \{eDSPN,\ SCPN,\ \text{stochastic UML statecharts(proto)}\}
$$

上式中的符号逐项解释如下：

1. `eDSPN` 是扩展确定/随机 Petri 网。
2. `SCPN` 是彩色随机 Petri 网。
3. `stochastic UML statecharts` 在文中仍处于 prototype 状态。

对 `eDSPN`，论文明确列出允许的 firing-delay 类别，可保守写成：

$$
\delta(t) \in \{0,\ \exp,\ det,\ expolynomial\}
$$

上式中的符号逐项解释如下：

1. `0` 表示 immediate transitions。
2. `\exp` 表示指数分布延迟。
3. `det` 表示确定性延迟。
4. `expolynomial` 是论文强调的一类分段指数多项式有限支撑分布。
5. `\delta(t)` 表示 transition `t` 的 firing-delay 类型。

论文还给出 `eDSPN` 数值分析的重要前提，可压成：

$$
\forall m,\ \left|\{t \in enabled(m)\mid \delta(t)\ \text{non-Markovian}\}\right| \le 1 \Rightarrow \text{stationary numerical analysis}
$$

$$
\forall m,\ \left|\{t \in enabled(m)\mid \delta(t)\ \text{deterministic}\}\right| \le 1 \Rightarrow \text{transient numerical analysis}
$$

上式中的符号逐项解释如下：

1. `enabled(m)` 是 marking `m` 下可发射的变迁集合。
2. 第一条表示若同一 marking 下非指数延迟变迁互斥，则可做稳态数值分析。
3. 第二条表示若进一步收束为确定性延迟互斥，则还能做瞬态数值分析。
4. 这两条正是论文正文对数值分析前提的概括。

### 一个最小例子与通俗解释

论文用 manufacturing system application 说明新功能：

1. 原始系统可用一般随机 Petri 网表示。
2. 用 `SCPN` 后，颜色与对象化 token 能显著压缩模型规模。
3. 工具再用 simulation 和数值分析得到性能指标。

通俗地说，`TimeNET` 的意义是“先把复杂并发资源流系统压进网里，再把性能数字算出来”，而不是只停在可视化画网阶段。

### 运行 / 接受 / 转移语义

论文的分析语义主要围绕 marking 演化与 firing delays。可保守写成：

$$
(N, M) \xrightarrow{t,\tau} (N, M')
$$

其中：

1. `N` 是当前 Petri 网模型。
2. `M` 和 `M'` 是 firing 前后的 marking。
3. `t` 是被触发的 transition。
4. `\tau` 是由 `\delta(t)` 决定的延迟样本或确定时间。
5. 这条记法是对论文“stochastic/distributed firing delay + marking evolution”的保守整理。

### 语义边界

论文边界包括：

1. `TimeNET` 重点是 stochastic Petri nets，而不是一般状态机全家桶。
2. 不同网类和分布假设对应不同分析模块，不是所有模型都能直接做数值分析。
3. `stochastic UML state charts` 仍只是原型状态。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 支持网类 | `$\mathcal{C}_{TimeNET} = \{eDSPN,\ SCPN,\ \text{stochastic UML statecharts(proto)}\}$` | 论文明确列出的当前能力范围。 |
| 延迟类别 | `$\delta(t) \in \{0,\ \exp,\ det,\ expolynomial\}$` | `eDSPN` 可接受的 firing-delay 类型。 |
| 稳态前提 | `$\forall m,\ |\{t\in enabled(m)\mid \delta(t)\ \text{non-Markovian}\}| \le 1$` | 非指数延迟互斥时可做稳态数值分析。 |
| 瞬态前提 | `$\forall m,\ |\{t\in enabled(m)\mid \delta(t)\ \text{deterministic}\}| \le 1$` | 确定性延迟互斥时可做瞬态数值分析。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 以 marking 演化为核心，而非状态机 mode。 |
| 事件 / 触发 | 中等支持 | 通过 transition enabling/firing 表达。 |
| 守卫 / 数据 | 强支持 | `SCPN` 允许颜色与对象化 token。 |
| 层次 | 弱支持 | 主体不是层次网或层次状态机。 |
| 并发 / 同步 | 很强 | Petri 网的并发、资源竞争与同步是核心。 |
| 时间约束 | 很强 | 随机延迟、确定性延迟、瞬态/稳态分析都是主线。 |
| 连续动态 / 随机性 | 强随机 / 弱连续 | 概率与时间分布是核心，连续动力学不在主线。 |
| 可执行 / 可验证性 | 很强 | 支持结构检查、仿真、数值分析与 rare-event simulation。 |

### 形式化问题与性质

1. 这篇论文不是提出新网类，而是把 `stochastic PN` 的建模、可视化和性能分析打通。
2. `SCPN` 与非指数延迟支持，是它相对只做 `GSPN` 的工具的重要补点。
3. `PNML` 的接入，使它不只是私有 GUI 工具，而是开始具备交换能力。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 在 GUI 中构造 `eDSPN` 或 `SCPN`。
2. 执行结构检查、token game 或 simulation。
3. 根据网类和分布前提选择 steady-state / transient 数值分析。
4. 需要交换时使用 `PNML` import/export。

### 机器可处理承载方式

机器可处理承载方式包括：

1. TimeNET 自身 XML 模型格式。
2. `eDSPN` 和 `SCPN` 图形模型。
3. `PNML` 交换文件。
4. 分析结果图和 transient 曲线。

### 交换与互操作

这篇论文的互操作重点在于：

1. `PNML` import/export。
2. 工具自有 XML 作为主要内部承载。
3. 在 stochastic-PN 工具链里兼顾图形输入、分析结果展示与模型交换。

## 配套基础设施

- 建模/编辑工具：TimeNET Java 图形界面。
- 解析/交换/元模型支持：工具自有 XML、`PNML` import/export。
- 仿真/执行支持：steady-state / transient simulation、rare-event simulation、token game。
- 验证/分析支持：结构检查、稳态与瞬态数值分析、colored 模型仿真。
- 代码生成/转换支持：重点不是部署代码生成，而是模型导入导出与分析。
- 标准化或社区生态：TimeNET 网站、用户手册与 stochastic-PN 学术生态。

## 适用场景与需求前提

### 适用场景

适合制造系统、通信系统、资源受限并发系统和一般 stochastic discrete-event system 的性能评估。

### 需求前提

1. 系统更自然地用 places / transitions / tokens 表示，而不是状态机式控制流。
2. 关注点包括吞吐、队长、延迟、稳态或瞬态性能指标。
3. 若要做某些数值分析，需要满足论文列出的非指数/确定性延迟互斥前提。

### 不适用或高成本场景

如果目标是复杂连续物理动力学或纯接口契约分析，`TimeNET` 不是合适入口。

## 与相邻形式主义的关系

相对 [the-greatspn-tool-recent-enhancements/desc.md](../the-greatspn-tool-recent-enhancements/desc.md)，两者都做 stochastic PN 性能分析，但 `TimeNET` 更强调非指数分布和 `SCPN`；相对 [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)，`TAPAAL` 偏 timed-arc verification，而 `TimeNET` 偏 stochastic performance evaluation；相对 [quickly-prototyping-petri-nets-tools-with-snakes/desc.md](../quickly-prototyping-petri-nets-tools-with-snakes/desc.md)，`SNAKES` 偏原型化库，`TimeNET` 偏成熟分析环境。

## 与本研究的关系

### 对 Project 1 的价值

它说明若未来 `project_1` 需要把某些控制/调度/资源流需求转到 Petri 网侧做性能评估，仅有标准或单点求解器还不够，成熟 GUI + analysis environment 也很关键。

### 作为目标形式主义还是中间表示

更像 Petri 网支线的分析环境与执行载体，而不是最终理论本体。

### 对需求到模型生成的启发

1. 资源流和并发约束若天然对应 token 语义，Petri 网比状态机更合适。
2. 时间和概率需求往往要求同时考虑“模型紧凑性”和“分析可行性”，`SCPN` 正是这种折中。
3. 交换格式支持对后续自动化流程很重要，哪怕主工具仍有私有 XML。

### 现实限制

数值分析能力依赖网类和分布假设，不能把所有随机网都一概而论。

## 重要的相关工作

1. [the-greatspn-tool-recent-enhancements/desc.md](../the-greatspn-tool-recent-enhancements/desc.md)：另一条 stochastic Petri net 工具主线。
2. [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)：更偏 timed-arc verification 的 Petri 网 IDE。
3. [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)：Petri 网交换格式与 `PNML` 基础。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 归类理由：主贡献是 stochastic Petri-net 的建模与性能分析环境，而不是新网类本体。
