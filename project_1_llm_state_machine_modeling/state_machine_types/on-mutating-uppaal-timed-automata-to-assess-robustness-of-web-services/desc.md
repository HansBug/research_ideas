# 通过变异 UPPAAL 定时自动机评估 Web 服务鲁棒性 / On Mutating UPPAAL Timed Automata to Assess Robustness of Web Services

## 基本信息

- 标题：On Mutating UPPAAL Timed Automata to Assess Robustness of Web Services
- 中文标题：通过变异 UPPAAL 定时自动机评估 Web 服务鲁棒性
- 作者：Faezeh Siavashi, Dragos Truscan, Jüri Vain
- 发表：*Proceedings of the 11th International Joint Conference on Software Technologies*, pp. 15-26, 2016
- DOI：`10.5220/0005970800150026`
- 链接：https://doi.org/10.5220/0005970800150026
- 形式主义：`UPPAAL Timed Automata / TRON Mutation Testing Model`
- 主类：⏱️
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：Web 服务鲁棒性测试 / 定时自动机应用建模
- 工具/实现获取方式：原文使用 `UPPAAL`、`UPPAAL TRON` 和自写 mutation generator，对 web service composition 的 `UTA` 模型生成、验证并执行在线测试；论文未公开独立仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata XML、HTTP 请求适配器和在线测试配置；无独立行业交换标准。

## 简报

这篇论文不是在讲“怎样再建一个 Web services 组合模型”，而是在讲：既然组合已经被写成 `UPPAAL` timed automata，那么能不能直接在模型层做 mutation，再用 `UPPAAL TRON` 在线打到真实实现上，专门查那些普通 conformance testing 没打出来的 robustness 问题？作者的答案是可以。它把 Booking System 的组合服务写成 4 个 automata，然后只对核心的 Booking service 做变异，先用 reachability / deadlock 检查筛掉无效 mutant，再把剩余 mutant 当成在线测试机去驱动真实服务。

- 形式主义定位：这是 `Timed Automata` 主干在 web-service robustness testing 上的应用条目，重点不是提出新的时间自动机分支，而是把 `UTA + mutation + online testing` 串成一条工程化测试链。
- 构造方式简述：先把 Web service composition 写成 `UPPAAL` timed automata，再对可观察动作的 transition / sync / input 等元素应用 mutation operators，之后由 `UPPAAL TRON` 在线执行。
- 基础设施与场景简述：工具链是 `UPPAAL + mutation generator + UPPAAL TRON + HTTP adapter`；场景是 Booking System 一类服务组合鲁棒性测试。

```text
web-service composition -> UPPAAL timed automata -> mutation operators + verification rules -> valid mutants -> TRON online testing -> robustness faults
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `UPPAAL timed automata (UTA)` 模型。
2. `UPPAAL TRON` 在线测试引擎。
3. 针对 transition / channel / input 的 mutation operators，如 `CT`、`CS`、`CNI`。
4. Hotel Booking System (`HBS`) 的 Booking / Card / Hotel / Environment 四个 automata。
5. 由 mutation generator 自动插入的可达性验证规则。

### 核心抽象

论文把被测系统写成 `UTA`，可保守记为：

$$
M = \langle L, l_0, C, \Sigma, E, I \rangle
$$

上式中的符号逐项解释如下：

1. `$L$` 是位置集合。
2. `$l_0$` 是初始位置。
3. `$C$` 是时钟集合。
4. `$\Sigma$` 是可观察与内部动作集合。
5. `$E$` 是带 guards / resets 的边集合。
6. `$I$` 是位置不变式。

在实验中，Booking service 模型包含 `33` 个 locations、`39` 个 actions、`4` 个 guards 和 `4` 个 clock invariants。基于原模型，变异模型可保守整理为：

$$
M' = \mu_{op}(M)
$$

上式中的符号逐项解释如下：

1. `$M$` 是原始 `UTA` 模型。
2. `$\mu_{op}$` 是某个 mutation operator，例如 `CT`、`CS` 或 `CNI`。
3. `$M'$` 是只包含一阶语法改动的 mutant。

论文还给出两个关键评价公式：

$$
ME_i = \frac{A_i}{V_i}
$$

$$
MFD_i = \frac{NE_i}{T_i - E_i}
$$

上式中的符号逐项解释如下：

1. `$A_i$` 是第 `$i$` 个 operator 产生的 alive mutants 数量。
2. `$V_i$` 是 valid mutants 数量。
3. `$NE_i$` 是能揭示真实隐藏错误的 non-equivalent mutants 数量。
4. `$T_i$` 是该 operator 生成的总 mutants 数量。
5. `$E_i$` 是 equivalent mutants 数量。

### 一个最小例子与通俗解释

最小例子可以理解成 Booking service 的一个错误转移：

1. 原模型要求“同一 booking 只能确认一次 hotel confirmation”。
2. 对某个 transition 应用 `CT` 或 `CS` 之后，mutant 允许重复走到某个本不该重复进入的确认分支。
3. `UPPAAL TRON` 会用这个 mutant 在线生成输入，向真实服务发送 HTTP 请求。
4. 如果真实系统接受了这个本不该接受的输入序列，就暴露出 robustness fault。

通俗地说，这像“先把服务组合写成带秒表的状态机，再故意把图上的边改错一点点，看真实系统会不会跟着犯错”。这比只跑正常 happy path 更擅长把重复确认、重复支付、异常退款之类的问题逼出来。

### 运行 / 接受 / 转移语义

论文中的一个关键思想是：不是所有 mutant 都适合在线测试，所以先用 `UPPAAL` 验证可达性和 deadlock freedom，再把 valid mutants 交给 `TRON`。其 reachability rule 可保守写成：

$$
E\Diamond l_{mut}
$$

上式中的符号逐项解释如下：

1. `$l_{mut}$` 是 mutation 实际影响到的目标位置。
2. `$E\Diamond$` 表示存在路径最终到达该位置。
3. 若 mutation 永远不可达，就不值得进入在线测试阶段。

Mutation testing 的判定大致分为：

1. `killed`：mutant 生成的输入能让实现暴露不一致。
2. `alive`：在给定测试预算内没有暴露错误。
3. `equivalent`：虽然 alive，但与原模型等价。
4. `non-equivalent alive`：说明实现接受了未被规范允许的输入。

论文最终结果中，`1346` 个生成 mutant 里有 `393` 个 valid mutants；其中 `40` 个 mutant 暴露出 `3` 个此前未发现的实现错误。作者计算得：

$$
ME_{CT} = 22.9\%, \qquad ME_{CS} = 84.2\%
$$

以及

$$
MFD_{CT} = 62.5\%, \qquad MFD_{CS} = 8.3\%
$$

说明 `CS` 更容易保留下 alive mutants，而 `CT` 更擅长真正揭示 fault。

### 语义边界

这篇论文的边界主要有：

1. 它的核心是 robustness testing，不是服务组合语义本体的新定义。
2. 论文只做一阶 mutation，并重点限制在可观察动作上。
3. `TRON` 在线测试假设模型和实现之间能通过 adapter 对接。
4. equivalent mutant 识别仍需要人工分析。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 原始模型骨架 | `$M = \langle L, l_0, C, \Sigma, E, I \rangle$` | 被测 web-service composition 的 `UTA` 结构。 |
| 变异模型 | `$M' = \mu_{op}(M)$` | 用某个 operator 对原模型做一阶改写。 |
| 变异可达性 | `$E\Diamond l_{mut}$` | 只有可达 mutation 才值得执行在线测试。 |
| 变异效率 | `$ME_i = A_i / V_i$` | 该 operator 产生 alive mutants 的比例。 |
| 变异找错能力 | `$MFD_i = NE_i / (T_i - E_i)$` | 去掉 equivalent mutants 后，该 operator 真正揭错的能力。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | Booking / Card / Hotel / Environment 都是显式 automata。 |
| 事件 / 触发 | 强支持 | HTTP 请求、服务确认、拒绝、超时等动作都显式可变异。 |
| 守卫 / 数据 | 部分支持 | 核心仍是 control-flow mutation，复杂业务数据语义不是主体。 |
| 层次 | 不支持 | 模型是平铺 UTA network，不是层次状态机。 |
| 并发 / 同步 | 支持 | 多服务和环境用同步动作交互。 |
| 时间约束 | 中等支持 | Booking 流程含 `24h` 之类约束，但主创新在 mutation/testing。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散服务交互与在线测试。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` 验证 + `TRON` 在线测试直接闭环。 |

### 形式化问题与性质

1. 论文补出的关键不是“又一个 web-service timed automata 模型”，而是“如何利用 timed automata mutant 去打真实实现”。
2. 它证明正常 conformance testing 之外，mutation-based online testing 可以额外暴露重复确认、重复支付、退款路径等隐藏错误。
3. 这对 `project_1` 很有价值，因为未来“生成-验证-修复”闭环里，mutation line 可以直接接在形式模型之后。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 把参与组合的 web services 和 environment 写成 `UPPAAL` timed automata。
2. 选择要变异的核心 automaton，这里是 Booking service。
3. 应用 `CT / CS / CNI` 等 mutation operators。
4. 为每个 mutant 加入 reachability / deadlock freedom 规则，筛出 valid mutants。
5. 用 adapter 把 model-level input 映射为 HTTP 请求，再交给 `TRON` 在线执行。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata XML。
2. mutation generator 产生的 mutant models。
3. `UPPAAL TRON` 在线测试配置。
4. HTTP 级请求适配器。

### 交换与互操作

互操作链路非常清楚：

1. 原始模型和 mutants 都先在 `UPPAAL` 中检查。
2. `TRON` 从 valid mutants 中逐步生成输入。
3. adapter 把模型输入翻译成对真实 web services 的 HTTP 调用。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：`UPPAAL` XML 模型与 mutation generator；无独立行业标准。
- 仿真/执行支持：`UPPAAL TRON` 支持在线测试生成与执行。
- 验证/分析支持：可达性、deadlock freedom、mutation efficiency 与 fault detection 分析。
- 代码生成/转换支持：不是代码生成链，而是 model-to-request adapter。
- 标准化或社区生态：依托 `UPPAAL/TRON` 与 web-service testing 研究生态。

## 适用场景与需求前提

### 适用场景

适合那些已有 timed automata 规格、又需要检查真实服务实现是否会接受非规范输入序列的 web-service composition。

### 需求前提

1. 系统行为已经被形式化成 `UPPAAL` timed automata。
2. 实现侧能通过 adapter 暴露成可测试接口。
3. 关注点在 robustness，而不只是正常路径 conformance。

### 不适用或高成本场景

如果系统只有非结构化接口文档、没有稳定模型，或者输入输出无法映射到自动机动作，那么这条路线很难落地。

## 与相邻形式主义的关系

相对 [web-service-composition-automation-based-on-timed-automata/desc.md](../web-service-composition-automation-based-on-timed-automata/desc.md)，本文更关注测试而不是组合自动生成；相对 [a-flexible-architecture-to-monitor-dynamic-web-services-composition/desc.md](../a-flexible-architecture-to-monitor-dynamic-web-services-composition/desc.md)，它不是运行时监控架构，而是基于 mutant 的 online testing；相对 [contract-automata/desc.md](../contract-automata/desc.md)，这里的主形式主义仍是 timed automata，而不是 request/offer 契约本体。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当 LLM 已经生成了某个 timed automata 模型后，可以进一步沿 mutation 路线生成“反例式测试刺激”，而不必停留在静态模型检查。

### 作为目标形式主义还是中间表示

对 web-service testing，它更像模型后的验证中间表示；但如果项目本身就以 `UPPAAL` timed automata 为规范核心，它也可以直接作为目标形式主义。

### 对需求到模型生成的启发

1. 如果模型要进入后续 testing 闭环，就应优先保留可观察动作而不是只保留抽象状态。
2. robustness 缺陷常常来自流程图边界条件，mutation line 值得作为闭环中的常设步骤。
3. 模型层验证规则可以先过滤掉大量无效 mutant，减少后续测试成本。

## 重要的相关工作

- [web-service-composition-automation-based-on-timed-automata/desc.md](../web-service-composition-automation-based-on-timed-automata/desc.md)：同样以 timed automata 处理 Web services，但重点是组合构造而非 mutation testing。
- [a-flexible-architecture-to-monitor-dynamic-web-services-composition/desc.md](../a-flexible-architecture-to-monitor-dynamic-web-services-composition/desc.md)：同样面向动态服务组合，但采用运行时监控而非 mutant 驱动。
- [contract-automata/desc.md](../contract-automata/desc.md)：服务组合的另一条本体路线，强调契约匹配而非 timed automata mutation。

## 文献分类总结

- 形式主义：`UPPAAL Timed Automata / TRON Mutation Testing Model`
- 成熟度：`UPPAAL + TRON + adapter` 闭环明确，属于很适合进入“生成后验证”链路的工程化条目。
- 条目价值：这是一篇 `⏱️` 类高价值应用条目，核心贡献是把 timed automata 直接推进到在线 robustness testing。
