# 齿轮控制器的形式化设计与分析：一个使用 UPPAAL 的工业案例 / Formal Design and Analysis of a Gear Controller: An Industrial Case Study Using UPPAAL

## 基本信息

- 标题：Formal Design and Analysis of a Gear Controller: An Industrial Case Study Using UPPAAL
- 中文标题：齿轮控制器的形式化设计与分析：一个使用 UPPAAL 的工业案例
- 作者：Magnus Lindahl, Paul Pettersson, Wang Yi
- 发表：*TACAS 1998*, LNCS 1384, pp. 281-297, 1998
- DOI：`10.1007/BFb0054178`
- 链接：https://doi.org/10.1007/BFb0054178
- 形式主义：`Timed Automata / Gear-Controller Network`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：车辆换挡控制 / 定时自动机应用建模
- 工具/实现获取方式：原文把 `GearControl`、`Interface`、`Clutch`、`Engine`、`GearBox` 建成 `UPPAAL` 网络，并通过手工装饰模型验证 `46` 条逻辑公式；论文未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、共享时钟/变量与查询公式；不是独立行业交换标准。

## 简报

这篇论文关注的是“换挡控制器到底能不能在真实时间约束下安全完成一次 gear shift”。作者没有只对某个局部控制环节做分析，而是把换挡控制器、接口、离合器、发动机和变速箱一起压成一个 `UPPAAL` 定时自动机网络，并把工业方给出的非形式化要求整理成 `46` 条可检查性质。

- 形式主义定位：这是 `Timed Automata` 主干上的工业控制应用条目，重点不在提出新的自动机家族，而在展示怎样把工业换挡需求压成可验证的 clocks/guards/invariants。
- 构造方式简述：用 `GearControl || Interface || Clutch || Engine || GearBox` 组成网络，借助 `GCTimer/GBTimer/CTimer/ETimer` 和 `FromGear/ToGear` 表达 gear-shift 过程、异常检测与恢复。
- 基础设施与场景简述：依托 `UPPAAL` 的 reachability 分析与作者给出的 bounded-response-time 装饰方法，服务汽车/车辆传动系统中的实时控制逻辑验证。

```text
换挡需求与时间窗口 -> GearControl/Interface/Environment timed automata -> UPPAAL reachability queries -> 换挡性能 / 可预测性 / 错误检测验证
```

## 形式主义定义与核心对象

### 定义对象

论文里的关键对象包括：

1. 控制器 automaton `GearControl (GC)`，负责发起零扭矩、摘挡、同步转速、挂新挡和恢复扭矩。
2. `Interface (I)`，负责把 `FromGear` 和 `ToGear` 写入共享变量并发起 gear-change 请求。
3. 环境 automata：`Clutch (C)`、`Engine (E)`、`GearBox (GB)`。
4. 四个时钟：`GCTimer`、`GBTimer`、`CTimer`、`ETimer`。
5. 两个共享整数：`FromGear`、`ToGear`。
6. 两个装饰变量：`ErrStat` 用于 unrecoverable errors，`UseCase` 用于 recoverable engine cases。

### 核心抽象

论文底层仍然采用经典 timed automata 组合语义，可保守整理为：

$$
\mathcal{G} = GC \parallel I \parallel C \parallel E \parallel GB
$$

上式中的符号逐项解释如下：

1. `$GC$` 是齿轮控制器 automaton。
2. `$I$` 是接口 automaton，负责发起换挡请求。
3. `$C$`、`$E$`、`$GB$` 分别是离合器、发动机和变速箱环境模型。
4. `$\parallel$` 表示通过同步信道和共享变量组成的 timed automata network。

论文中与建模最直接相关的状态量可进一步压成：

$$
X = \{GCTimer, GBTimer, CTimer, ETimer, FromGear, ToGear, ErrStat, UseCase\}
$$

上式中的符号逐项解释如下：

1. `$GCTimer$` 用来测量控制器等待环境响应的时间。
2. `$GBTimer$`、`$CTimer$`、`$ETimer$` 分别对应变速箱、离合器和发动机内部服务时间。
3. `$FromGear$` 与 `$ToGear$` 表示当前挡位和目标挡位。
4. `$ErrStat$` 记录 unrecoverable error 类型。
5. `$UseCase$` 记录发动机零扭矩或同步转速失败等 recoverable case。

论文最有辨识度的形式化对象其实不是系统元组，而是作者为 `UPPAAL` reachability 检查设计的 bounded-response 表示。文中与案例直接相关的一条性质可以写成：

$$
GC@Initiate \ ;\leq 1500 \ ((ErrStat = 0) \rightarrow GC@GearChanged)
$$

上式中的符号逐项解释如下：

1. `GC@Initiate` 表示控制器进入一次换挡过程的起始位置。
2. `;\leq 1500` 表示“从前件发生起，后件必须在 `1500ms` 内成立”。
3. `ErrStat = 0` 表示期间没有进入 unrecoverable error。
4. `GC@GearChanged` 表示换挡完成位置。
5. 这条式子对应工业方提出的“gear shift 最迟 `1.5s` 完成”的性能要求。

### 一个最小例子与通俗解释

最小例子可以看成一次 `2 -> 3` 升挡：

1. `Interface` 把 `FromGear = 2`、`ToGear = 3` 写入共享变量，并发出 `ReqNewGear`。
2. `GearControl` 先请求发动机进入 `zero torque`。
3. 零扭矩达成后，请求变速箱释放当前挡位，再请求发动机对齐同步转速。
4. 同步转速完成后，请求变速箱设置新挡位，最后恢复扭矩并结束换挡。

通俗地说，这像“让五个小状态机协商完成一次换挡”。普通 `FSM` 只能表达先后步骤，而 timed automata 还能表达“离合器多久没打开算故障”“发动机多久没找到同步转速必须走恢复路径”“整次换挡多久内必须完成”。

### 运行 / 接受 / 转移语义

论文中最核心的控制语义是按阶段串接环境服务，并对每个阶段加时间窗。例如在正常条件下，作者从模型里推导出一次 gear shift 的紧上界：

$$
100 + 150 + 100 + 150 + 100 + 300 = 900
$$

上式中的符号逐项解释如下：

1. 前两个项是发动机达成零扭矩和变速箱摘挡的最坏等待。
2. 中间两个项是同步转速与新挡设置前后的协调时间。
3. 末尾两个项对应离合器与变速箱的最坏服务时间。
4. 这就是论文中“正常工况下应在 `1s` 内完成换挡”的模型侧解释，具体推导得到 `900ms`。

文中还把 bounded-response 语义规约成 invariant 检查。抽象地说，可写成：

$$
\mathcal{G}' \models A[]\ (v_1 \rightarrow c \leq T)
$$

上式中的符号逐项解释如下：

1. `$\mathcal{G}'$` 是对原模型做过装饰后的系统。
2. `$v_1$` 是“前件已经发生但后件尚未兑现”的标志。
3. `$c$` 是额外引入的监测时钟。
4. `$T$` 是目标 response bound。
5. 这说明作者把“在 `T` 内响应”转成了 `UPPAAL` 能直接处理的 reachability / invariant 问题。

### 语义边界

这篇论文的边界主要有：

1. 环境是抽象后的服务模型，不是完整车辆动力学模型。
2. 发动机只保留与零扭矩、同步转速相关的时间行为，不建模精细连续转速曲线。
3. 论文强调的是 prototype gear controller，而不是量产 ECU 全栈实现。
4. 方法依赖“需求里的关键时间窗口、错误类型和 gear-change phase 可显式结构化”这一前提。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统组合 | `$\mathcal{G} = GC \parallel I \parallel C \parallel E \parallel GB$` | 把控制器、接口与环境压成统一 timed automata network。 |
| 状态量集合 | `$X = \{GCTimer, GBTimer, CTimer, ETimer, FromGear, ToGear, ErrStat, UseCase\}$` | 控制换挡顺序、时间监视与错误分类的核心变量。 |
| gear shift 性能上界 | `$GC@Initiate \ ;\leq 1500 \ ((ErrStat = 0) \rightarrow GC@GearChanged)$` | 若无 unrecoverable error，则一次换挡最迟 `1500ms` 完成。 |
| 正常工况换挡时间 | `$100 + 150 + 100 + 150 + 100 + 300 = 900$` | 说明“正常条件下 `1s` 内完成”有模型级时间依据。 |
| bounded-response 到 invariant 的规约 | `$\mathcal{G}' \models A[]\ (v_1 \rightarrow c \leq T)$` | 把 `UPPAAL` 的 reachability 能力扩展到响应时间验证。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `Initiate`、`CheckTorque`、`CheckSyncSpeed`、`GearChanged`、错误态等都很明确。 |
| 事件 / 触发 | 强支持 | `ReqSet`、`ReqNeu`、`OpenClutch`、`CloseClutch`、`ReqSpeed` 等请求/响应通道是控制骨架。 |
| 守卫 / 数据 | 强支持 | `FromGear/ToGear`、`ErrStat/UseCase` 和多个 timer guard 共同决定转移。 |
| 层次 | 弱支持 | 不是层次状态机，但用“控制器 + 接口 + 环境”分层组织。 |
| 并发 / 同步 | 强支持 | 五个 automata 通过信道和共享变量并行同步。 |
| 时间约束 | 强支持 | 离合器、变速箱、发动机和整次换挡都带显式上界。 |
| 连续动态 / 随机性 | 不支持 | 只保留离散 phase 与时间窗口，不做连续动力学。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` 直接验证 `46` 条工业需求派生性质。 |

### 形式化问题与性质

1. 论文的关键价值不是“又一个汽车控制案例”，而是把一份工业需求文档压成可运行、可检查的 `UPPAAL` 模型。
2. `ErrStat` 与 `UseCase` 的分离很重要，因为它把 recoverable 和 unrecoverable error 分开编码。
3. bounded-response 的装饰法说明，很多工程“多久内必须完成”的要求可以在旧版 `UPPAAL` reachability 能力下落地。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先把工业方的换挡步骤和时间要求整理成环境服务接口。
2. 再把 `GearControl` 写成串接这些服务的 timed automaton。
3. 用 `ErrStat` / `UseCase` 区分错误分支与恢复分支。
4. 最后对性能/预测性要求做装饰，转成 `UPPAAL` 可检的 reachability / invariant 性质。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` 图形 automata。
2. 同步信道，如 `ReqSet`、`ReqNeu`、`ReqSpeed`、`NewGear`。
3. 共享变量和 clocks。
4. 经装饰后的 bounded-response 查询。

### 交换与互操作

互操作重点在：

1. `Interface` 和 `GearControl` 通过 `FromGear/ToGear` 共享挡位语义。
2. `GearControl` 与环境通过 request/response channel 对接。
3. `UPPAAL` 的 reachability 内核与作者的逻辑装饰方法组合，形成需求检查链路。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` 图形编辑与模拟环境。
- 解析/交换/元模型支持：无独立交换标准；模型直接承载在 `UPPAAL` automata/network 里。
- 仿真/执行支持：可用 `UPPAAL` 仿真换挡过程和错误恢复路径。
- 验证/分析支持：支持 `46` 条逻辑公式、deadlock 检查和 bounded-response 规约验证。
- 代码生成/转换支持：原文未提供自动代码生成链。
- 标准化或社区生态：依托 `UPPAAL` 和 timed automata 社区，而不是独立行业标准。

## 适用场景与需求前提

### 适用场景

适合那些由离散 phase 驱动、且对各 phase 响应时限极其敏感的汽车/车辆嵌入式控制器，例如换挡、联锁、执行器协调等任务。

### 需求前提

1. 需求必须能分解成有限个阶段和同步事件。
2. 每个外部服务都要有明确的成功/失败和时间窗口。
3. 关键正确性要求主要是安全性、可预测性和 bounded response，而不是复杂连续动力学。

### 不适用或高成本场景

如果系统核心难点在高维连续动力学、非线性轮胎模型或概率故障传播，仅靠这里的 timed automata 抽象会过粗。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是标准 `Timed Automata` 在工业车辆控制上的直接落地；相对 [formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md](../formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md)，它从通信协议转向执行器协调控制；相对 [testing-automotive-reactive-systems-using-timed-automata/desc.md](../testing-automotive-reactive-systems-using-timed-automata/desc.md)，本文重点是设计验证而不是测试驱动。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：只要需求里已经有“步骤顺序 + 每步时限 + 错误恢复”三件事，就很适合生成 timed automata，而不必先退化成无时间的普通状态机。

### 作为目标形式主义还是中间表示

对实时控制器验证，它可以直接作为目标形式主义；对更大系统，它也适合做从需求到验证模型的中间表示。

### 对需求到模型生成的启发

1. 应把 environment service 先形式化，再生成 controller。
2. 需要显式区分 recoverable 与 unrecoverable error。
3. 性能要求最好直接生成为 bounded-response 公式，而不是后写成散乱注释。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文依赖的 timed automata 理论底座。
- [formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md](../formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md)：同样是 `UPPAAL` 工业实时控制案例，但对象是电源协议。
- [testing-automotive-reactive-systems-using-timed-automata/desc.md](../testing-automotive-reactive-systems-using-timed-automata/desc.md)：同属车辆相关 timed automata 条目，但重心是 HIL 测试。

## 文献分类总结

- 形式主义：`Timed Automata / Gear-Controller Network`
- 成熟度：`UPPAAL` 建模与验证链完整，需求到公式的映射也很清楚。
- 条目价值：这是一篇 `⏱️` 类工业控制应用条目，核心价值在于展示 timed automata 如何承接真实换挡需求与 bounded-response 验证。
