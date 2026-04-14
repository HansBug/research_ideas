# 基于定时自动机的 Web 服务组合自动化 / Web Service Composition Automation based on Timed Automata

## 基本信息

- 标题：Web Service Composition Automation based on Timed Automata
- 中文标题：基于定时自动机的 Web 服务组合自动化
- 作者：Hu Jingjing, Zhu Wei, Zhao Xing, Zhu Dongfeng
- 发表：*Applied Mathematics & Information Sciences*, Vol. 8, No. 4, pp. 2017-2024, 2014
- DOI：`10.12785/AMIS/080460`
- 链接：https://doi.org/10.12785/AMIS/080460
- 形式主义：`Timed Automata for Web Service Composition (TAC)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：Web 服务组合自动化 / 定时自动机应用建模
- 工具/实现获取方式：原文实现了 `WSIL` 语义解析、`TAC/NTA` 生成和 `UPPAAL 4.0` 仿真验证流程，但未给出公开代码仓库。
- 标准/格式获取方式：承载方式是 `WSIL` 上的接口描述、由算法生成的 `TAW/TAC` 与 `UPPAAL` 可读取的 `NTA`；不是行业标准文件。

## 简报

这篇论文把 timed automata 直接用到了“自动拼 Web services”这件事上。作者先为每个原子服务构造 `TAW`，再根据接口参数等价关系把多个 `TAW` 合成全局 `TAC`，并用一个 global clock 记录组合路径代价；工程实现上又定义了 `WSIL`，用语法/语义解析把服务接口自动编译成 `NTA`，最后交给 `UPPAAL` 仿真与评估。

- 形式主义定位：属于 `Timed Automata` 在 Web service composition 上的应用条目，重点是“带时间代价的服务组合模型 + 自动化构造”。
- 构造方式简述：`WSIL` 接口描述先转成 equivalent graph/tree，再由 `A-TAW` 生成单服务 timed automata，由 `A-TAC` 合并成组合 automaton。
- 基础设施与场景简述：工具链是 `WSIL parser + NTA generator + UPPAAL 4.0`；场景是自动把独立服务拼成满足参数等价和代价约束的复合服务。

```text
WSIL service interfaces -> equivalent graph / equivalent tree -> TAW -> TAC / NTA -> UPPAAL simulation -> automated WSC result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. 原子 Web service 的输入/输出参数与参数等价关系。
2. 单服务 `TAW`。
3. 组合服务 `TAC`。
4. `WSIL` 接口描述语言。
5. `UPPAAL` 可读取的 `NTA` 目标模型。

### 核心抽象

原文直接采用 timed automaton 四元组定义：

$$
TA = \langle N, l_0, E, I \rangle,\qquad E \subseteq N \times \beta(C) \times \Sigma \times 2^C \times N
$$

上式中的符号逐项解释如下：

1. `$N$` 是有限位置集合。
2. `$l_0 \in N$` 是初始位置。
3. `$\beta(C)$` 是时钟约束集合，`$C$` 是时钟变量集。
4. `$\Sigma$` 是动作集合。
5. `$2^C$` 表示可复位的时钟集合。
6. `$I : N \to \beta(C)$` 为每个位置赋不变式。

单个原子服务被建成 `TAW`，其结构仍是：

$$
TAW = \langle N, l_0, E, I \rangle
$$

上式中的符号逐项解释如下：

1. `$N$` 是服务调用状态集合。
2. `$E$` 表示服务状态迁移。
3. `$I$` 把调用约束绑定到 clock constraints。
4. 时钟值在这里代表当前迁移路径上的 cost。

对组合模型 `TAC`，原文强调它由多个 `TAW` 集成得到，并插入 head model、去掉冗余 clock constraints、重置 global clock。按该构造流程可保守整理为：

$$
TAC = \langle H, \{TAW_i\}_{i=1}^n, c_g, B \rangle
$$

上式中的符号逐项解释如下：

1. `$H$` 是组合起始的 head model。
2. `$\{TAW_i\}_{i=1}^n$` 是参与组合的原子服务自动机集合。
3. `$c_g$` 是记录总 cost 的 global clock。
4. `$B$` 表示由 branch/end tags 和参数等价关系诱导出的连接约束。
5. 这个四元组是根据 `A-TAC` 流程做的保守归纳，不是原文逐字给出的独立数学定义。

### 一个最小例子与通俗解释

可以把论文方法理解成一个最小两服务组合：

1. 服务 `S_1` 输出参数 `p`，服务 `S_2` 输入参数也需要 `p`。
2. `WSIL` 先把两个接口描述出来，并标出这两个参数等价。
3. 语义解析生成 equivalent graph，再变成无环 equivalent tree。
4. `A-TAW` 为每个服务参数生成带 guard/reset 的分支图，`A-TAC` 把这些分支拼成全局 `TAC`。
5. `UPPAAL` 最终跑出一条满足接口连接且 global clock 代价较小的组合路径。

通俗地说，这个模型像“把服务候选空间变成一张带计时器的拼装自动机图”，自动机跑通哪条路径，就代表哪组服务能被拼成一个复合服务。

### 运行 / 接受 / 转移语义

原文对单条 timed transition 的记法是：

$$
l \xrightarrow{g,a,r} l'
$$

其中 `$\langle l, g, a, r, l' \rangle \in E$`。符号解释如下：

1. `$l,l'$` 是源/目标位置。
2. `$g \in \beta(C)$` 是时钟守卫。
3. `$a \in \Sigma$` 是动作标签。
4. `$r \subseteq C$` 是要复位的时钟集合。

`A-TAW` 构造单服务分支时，active/passive parameter 的核心语义可保守概括为：

$$
\text{active parameter} \Rightarrow \text{guard} = \text{clock constraints},\ \text{reset} = \text{local clocks}
$$

$$
\text{passive parameter} \Rightarrow \text{guard} = \text{clock constraints} \land \text{active-branch tag}
$$

上式中的符号逐项解释如下：

1. `guard` 是该分支能否被选择的时间/标签条件。
2. `reset` 控制局部时钟在转移时清零。
3. `active-branch tag` 把被动参数绑定到已经选中的主动分支。

在组合层，`global clock` 记录组合总代价，原文据此选择更优组合路径。可保守写成：

$$
c_g(\pi) = \sum_{e \in \pi} cost(e),\qquad \pi^* = \arg\min_{\pi \in \Pi_{TAC}} c_g(\pi)
$$

上式中的符号逐项解释如下：

1. `$\pi$` 是 `TAC` 上一条可行组合路径。
2. `$cost(e)$` 是边 `$e$` 对应的局部代价/时钟消耗。
3. `$\Pi_{TAC}$` 是所有满足接口连接约束的候选路径集合。
4. 该式是根据论文“global clock stores total cost / path with clock value becomes the best solution”的语义做的保守整理。

### 语义边界

这篇论文的边界主要有：

1. 它重点解决接口参数连接和组合代价，不是事务补偿或复杂协议合规。
2. 时钟语义主要承担 cost/latency 约束，不是高精度实时控制分析。
3. 论文用整数时钟和 zone automata 缓解状态爆炸，但 clocks 数量上升时仍会受限。
4. 更适合接口结构和候选服务集合已知的组合问题，不适合完全开放的语义发现。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 定时自动机骨架 | `$TA = \langle N, l_0, E, I \rangle$` | 组合模型直接建立在标准 timed automata 上。 |
| 单服务模型 | `$TAW = \langle N, l_0, E, I \rangle$` | 原子服务接口可独立编译成 timed automaton。 |
| 组合模型 | `$TAC = \langle H, \{TAW_i\}, c_g, B \rangle$` | 全局复合服务由多个 `TAW` 与全局时钟拼接得到。 |
| 转移语义 | `$l \xrightarrow{g,a,r} l'$` | 分支可选性由 guard 与 clock reset 决定。 |
| 最优路径语义 | `$\pi^* = \arg\min c_g(\pi)$` | global clock 可用于选择代价较低的组合方案。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 服务调用状态与组合路径都是显式位置。 |
| 事件 / 触发 | 强支持 | 接口动作和分支标签直接成为转移标签。 |
| 守卫 / 数据 | 强支持 | 参数等价、branch tags 和 clock constraints 都进入 guard。 |
| 层次 | 部分支持 | `TAW -> TAC -> NTA` 是弱层次，不是深层 mode hierarchy。 |
| 并发 / 同步 | 支持 | 多个服务自动机通过分支标签和同步结构组合。 |
| 时间约束 | 强支持 | clock constraints、global clock 和 zone semantics 是主体。 |
| 连续动态 / 随机性 | 不支持 | 不建模连续 ODE 或概率行为。 |
| 可执行 / 可验证性 | 强验证、部分自动生成 | 可自动生成 `NTA` 并交给 `UPPAAL`。 |

### 形式化问题与性质

1. 论文最有价值的点是把“服务接口描述 -> timed automata -> 组合结果”做成一条自动化编译链。
2. `WSIL` 在这里是辅助输入语言，主形式主义仍然是 `Timed Automata`。
3. `global clock` 把组合可行性和代价优化压进同一个自动机搜索问题。
4. 对 `project_1` 来说，这种“从接口字段到自动机分支”的构造法值得借鉴。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 用 `WSIL` 写原子服务接口。
2. 语义解析生成 equivalent graph。
3. 广度优先生成 equivalent tree。
4. 按 `A-TAW` 构造每个节点的单服务 automaton。
5. 按 `A-TAC` 合成组合模型，再按 `A-NTA` 输出 `UPPAAL` 输入。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `WSIL` 上的接口定义。
2. equivalent graph / tree。
3. `TAW/TAC`。
4. `NTA` 与 `UPPAAL` 模型。

### 交换与互操作

互操作链路非常明确：

1. `WSIL` 是前端接口输入。
2. `NTA` 是后端工具可直接读取的模型输出。
3. `UPPAAL` 负责仿真和性质检查。

## 配套基础设施

- 建模/编辑工具：`WSIL` 接口描述 + CFG/语义解析器。
- 解析/交换/元模型支持：原文用 context-free grammar、Lex/YACC 风格工具和 syntax-tree traversal 实现解析；未给出独立元模型标准。
- 仿真/执行支持：`UPPAAL 4.0` 作为 service composition simulator。
- 验证/分析支持：`UPPAAL`、zone automata、整数时钟/实值时钟对比实验。
- 代码生成/转换支持：从 `WSIL` 自动生成 `TAW/TAC/NTA`。
- 标准化或社区生态：主要依托 `Timed Automata` 与 `UPPAAL` 生态，`WSIL` 是论文自定义语言。

## 适用场景与需求前提

### 适用场景

适合候选服务接口已知、参数连接关系明确、且组合目标需要同时考虑逻辑连通性和时间/代价约束的 Web service composition。

### 需求前提

1. 服务接口和参数结构要能用 `WSIL` 表达。
2. 参数等价关系要能离散化成 equivalent graph。
3. 组合目标可通过路径代价和时钟约束表达。
4. 候选组合空间不能大到让 clocks/reset 引发不可控爆炸。

### 不适用或高成本场景

如果服务语义主要依赖复杂自然语言说明、动态在线发现或非结构化 QoS 学习，这种自动机构造法会缺少稳定输入。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文不是理论奠基，而是 Web service composition 应用建模；相对 [analysis-and-applications-of-timed-service-protocols/desc.md](../analysis-and-applications-of-timed-service-protocols/desc.md)，本文更强调从接口语言自动生成组合模型，而不是协议兼容/可替换运算；相对 [an-interface-theory-based-approach-to-verification-of-web-services/desc.md](../an-interface-theory-based-approach-to-verification-of-web-services/desc.md)，本文把主形式主义明确放在 `Timed Automata`，而不是事务接口三层本体。

## 与本研究的关系

### 对 Project 1 的价值

它说明：如果需求中已经有“服务输入输出参数 + 时间/代价约束”，LLM 生成状态机时可以直接走“接口结构 -> timed automata 分支 -> 工具后端”的路线，而不必只输出自然语言流程图。

### 作为目标形式主义还是中间表示

对带时间/代价的服务组合，它可以直接作为目标形式主义；对更一般的系统需求，它也可以作为接口层和调度层之间的中间表示。

### 对需求到模型生成的启发

1. 参数连接关系应显式抽成图结构，再映射到自动机拼接。
2. 时间/代价变量可以先作为 clock-like 成本容器进入模型。
3. 若要自动接 `UPPAAL`，前端语言与模型生成算法应一起设计。

### 现实限制

论文自定义的 `WSIL` 和 branch-tag 机制偏工程原型，若迁移到通用场景，可能需要重新设计接口抽象和类型系统。

## 重要的相关工作

### 奠基或前身工作

1. `Timed Automata` 理论和 `UPPAAL` 工具是本文的直接基础。
2. 论文也延续了 Web service composition 与 AI planning / workflow composition 的应用背景。

### 同类型或同家族工作

1. [analysis-and-applications-of-timed-service-protocols/desc.md](../analysis-and-applications-of-timed-service-protocols/desc.md) 是更偏时间协议语义与兼容分析的一条 timed service 路线。
2. [business-process-verification-the-application-of-model-checking-and-timed-automata/desc.md](../business-process-verification-the-application-of-model-checking-and-timed-automata/desc.md) 说明 `Timed Automata` 也可落到业务流程验证，而本文更偏自动组合生成。

### 标准 / 格式 / 工具链工作

1. `UPPAAL` 与 `NTA` 是本文后端工具线。
2. `WSIL` 是前端输入语言，但不是外部标准。

### 与本研究关系最紧的工作

1. 它为“需求/接口文本如何结构化成 timed automata 构造输入”提供了可复用样板。
2. 对 `project_1` 来说，`equivalent graph -> TAW/TAC` 这条构造链尤其值得借鉴。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`Timed Automata for Web Service Composition (TAC)`
- 论文角色：Web 服务组合自动化 / 定时自动机应用建模
- 核心功能：把原子服务接口自动编译成可由 `UPPAAL` 仿真的组合 timed automata
- 关键特性：`TAW/TAC`、clock guards/reset、global clock cost、`WSIL`、`NTA` 输出
- 构造方式：`WSIL -> equivalent graph/tree -> TAW -> TAC -> NTA`
- 基础设施：`UPPAAL 4.0`、CFG parser、Lex/YACC 风格语义解析
- 适用场景：带时间/代价约束的 Web service composition 自动化
- 需求前提：接口参数和等价关系需可结构化枚举
- 状态：🟢
