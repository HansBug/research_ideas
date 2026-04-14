# 基于 UPPAAL 的唇音同步算法自动验证 / Automatic Verification of a Lip-Synchronisation Algorithm Using UPPAAL

## 基本信息

- 标题：Automatic Verification of a Lip-Synchronisation Algorithm Using UPPAAL
- 中文标题：基于 UPPAAL 的唇音同步算法自动验证
- 作者：Howard Bowman, Giorgio P. Faconti, Joost-Pieter Katoen, Diego Latella, Mieke Massink
- 发表：*FMICS'98* extended version, CWI, pp. 97-124, 1998；期刊版本见 *Formal Aspects of Computing* 10(5-6), 1998
- DOI：`10.1007/S001650050032`（期刊版本）
- 链接：https://kar.kent.ac.uk/21658/1/Automatic_Verification_of_a_Lip-Synchronisation_Algorithm_Using_UPPAAL_-_Extended_Version.pdf
- 形式主义：`Timed Automata / Lip-Synchronisation Controller Network`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：多媒体同步算法验证 / 定时自动机应用建模
- 工具/实现获取方式：原文把 `SoundMgr`、`VideoMgr`、`SoundWdg`、`VideoWdg`、`SoundSynch`、`VideoSynch`、`SoundClock`、`Synch`、`UrgMon` 与输入流 automata 一起写成 `UPPAAL` 网络；论文未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata、urgent channels、watchdog timeout 构件和 reachability 查询；不是独立标准格式。

## 简报

这篇论文研究的是一个很典型、也很难“只靠直觉”讲清楚的实时同步问题：音频每 `30ms` 一包、视频理想情况下每 `40ms` 一帧，但允许 jitter 和 skew，控制器该怎样安排呈现时机，才能既不乱序，也不让唇音脱节。作者把 lip-sync 算法翻译成 timed automata network，用 `UPPAAL` 自动检查 jitter / skew 性质，结果发现原算法并不总能优雅报错，而是会在某些流模式下直接 timelock。

- 形式主义定位：这是 `Timed Automata` 在多媒体同步控制上的应用条目，重点是 watchdog、precise/ bounded timeout 与跨流 skew 约束。
- 构造方式简述：用 stream automata 产生 `savail/vavail`，由 manager 报告 `sready/vready`，再由 synchroniser 决定何时发出 `sok/vok` 让 presentation device 播放。
- 基础设施与场景简述：依托 `UPPAAL` 的 reachability 检查和 urgent-channel 机制，服务实时多媒体流同步算法的形式验证。

```text
audio/video arrival streams -> managers + watchdogs + synchroniser timed automata -> UPPAAL reachability -> jitter/skew correctness and timelock analysis
```

## 形式主义定义与核心对象

### 定义对象

论文里的关键对象包括：

1. `SoundMgr` 与 `VideoMgr`，负责在 item 到达时通知同步器，并在允许时触发呈现。
2. `SoundWdg` 与 `VideoWdg`，负责检查各自流的 inter-packet timing。
3. `SoundSynch` 与 `VideoSynch`，负责核心 lip-sync 决策。
4. `SoundClock`，负责给视频帧计算相对音频的 skew。
5. `Synch` 与 `UrgMon`，分别负责初始同步和 precise-timeout 相关辅助逻辑。
6. 输入流 automata `SoundStr` 与 `VideoStr`。

### 核心抽象

系统网络可整理为：

$$
\mathcal{N}_{lip} = SoundStr \parallel VideoStr \parallel SoundMgr \parallel VideoMgr \parallel SoundWdg \parallel VideoWdg \parallel SoundSynch \parallel VideoSynch \parallel SoundClock \parallel Synch \parallel UrgMon
$$

上式中的符号逐项解释如下：

1. `SoundStr` 和 `VideoStr` 生成输入流到达事件。
2. `SoundMgr/VideoMgr` 管理单流 item 的就绪与播放。
3. `SoundWdg/VideoWdg` 监视单流时间约束。
4. `SoundSynch/VideoSynch/SoundClock/Synch/UrgMon` 共同实现跨流同步和 timeout 机制。
5. `$\parallel$` 表示由同步信道组合的 timed automata network。

论文中的关键同步量是视频相对音频的 skew 变量 `vmins`。可保守写成：

$$
-150 \leq vmins \leq 15
$$

上式中的符号逐项解释如下：

1. `$vmins$` 记录视频相对于音频的时间偏移。
2. 下界 `-150` 表示视频最多比音频晚 `150ms`。
3. 上界 `15` 表示视频最多比音频早 `15ms`。
4. 这是论文采用的跨流同步容差。

单流 timing 约束同样被写得很明确。例如视频的 non-anchored jitter 要求是：

$$
35 \leq \Delta_v \leq 45
$$

上式中的符号逐项解释如下：

1. `$\Delta_v$` 表示相邻两次视频呈现之间的时间差。
2. 下界 `35ms` 和上界 `45ms` 给出了允许的 jitter 窗口。
3. 这一定义允许 drift 累积，因此与 anchored jitter 明显不同。

### 一个最小例子与通俗解释

最小例子可以想成：

1. 第一个 sound frame 到达后，`SoundMgr` 立刻发 `sready`，并在被允许时触发 `sok`。
2. `SoundClock` 开始每 `1ms` 递进一次，同时更新 `vmins`。
3. 当某个 video frame 到达时，`VideoSynch` 先检查当前 `vmins` 是否在 `[-150, 15]` 内。
4. 如果视频太早，就延迟一小步后重新检查；如果太晚，就直接进入 `vsynch_error`。

通俗地说，这像“音频是节拍器，视频要追着它但不能追太慢，也不能抢太早”。timed automata 的优势在于：它不光能说“最终是否同步”，还能精确判断“在哪个 watchdog 先爆掉”“什么时候只是 early frame、什么时候已经构成不可恢复 skew”。

### 运行 / 接受 / 转移语义

论文对错误的验证主要采用 reachability 公式，形式大致为：

$$
E<> A:l \land \neg(B_1:l_1 \lor \cdots \lor B_n:l_n)
$$

上式中的符号逐项解释如下：

1. `$E<>$` 表示存在一条路径最终到达某状态。
2. `$A:l$` 是目标 error location。
3. `$\neg(B_1:l_1 \lor \cdots \lor B_n:l_n)$` 用于排除“先进入别的错误态导致的假阳性”。
4. 作者用它分别检查 initial sound/video sync error、video sync error、video late 和 sound late。

视频 watchdog 的约束可直接写成：

$$
35 \leq t_4 \leq 45
$$

上式中的符号逐项解释如下：

1. `$t_4$` 是 `VideoWdg` 中记录相邻视频帧间隔的时钟。
2. `t_4 \geq 35` 表示不能过早播放下一帧。
3. `t_4 \leq 45` 表示不能过晚播放下一帧。
4. 超过上界时进入 `vlate` 相关错误。

Sound watchdog 的“精确 `30ms`”行为则依赖更强的 timeout 结构，可压成：

$$
t_3 = 30 \Rightarrow ums,\qquad t_3 = 31 \Rightarrow slate
$$

上式中的符号逐项解释如下：

1. `$t_3$` 是 sound watchdog 计时器。
2. `ums` 用于在恰好 `30ms` 时触发紧急同步机制。
3. 若此时没有可播放的 sound frame，则在 `31ms` 时报 `slate`。
4. 这说明 sound stream 被建模为无 jitter 的理想节拍。

### 语义边界

这篇论文的边界主要有：

1. sound stream 被假定为理想流，几乎不讨论音频端的 jitter。
2. 原算法不含 buffering，因此只能靠 immediate scheduling 修正误差。
3. 论文使用 dense time，而原问题背景更接近 discrete time；两者差异正是 timelock 暴露的来源之一。
4. 很多错误不是传统 bad state，而是“无法继续推进时间”的 timelock。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统组合 | `$\mathcal{N}_{lip} = SoundStr \parallel VideoStr \parallel \cdots \parallel UrgMon$` | 把输入流、manager、watchdog 和 synchroniser 全部放进一个 timed automata network。 |
| 跨流 skew 约束 | `$-150 \leq vmins \leq 15$` | 视频最多晚音频 `150ms`、最多早音频 `15ms`。 |
| 视频 jitter 约束 | `$35 \leq \Delta_v \leq 45$` | 相邻视频帧的 non-anchored jitter 窗口。 |
| error 可达性检查 | `$E<> A:l \land \neg(B_1:l_1 \lor \cdots \lor B_n:l_n)$` | 分别检查不同错误是否可独立触发。 |
| sound precise timeout | `$t_3 = 30 \Rightarrow ums,\ t_3 = 31 \Rightarrow slate$` | 声音必须严格按 `30ms` 节拍推进。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | managers、watchdogs、synchronisers 都有明确 phase。 |
| 事件 / 触发 | 强支持 | `savail/vavail`、`sready/vready`、`sok/vok`、`slate/vlate` 是模型骨架。 |
| 守卫 / 数据 | 强支持 | `vmins` 和 `t1..t7` 共同决定播放、等待或报错。 |
| 层次 | 弱支持 | 不是层次状态机，但通过组件分工形成结构化网络。 |
| 并发 / 同步 | 强支持 | 多个 automata 通过 urgent / normal channel 协同。 |
| 时间约束 | 强支持 | `30ms` sound、`35..45ms` video 和 `[-150,15]ms` skew 都是显式约束。 |
| 连续动态 / 随机性 | 不支持 | 没有连续媒体信号动力学，只保留离散到达/播放时间。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` 自动发现 timelock 和短期 skew failure。 |

### 形式化问题与性质

1. 论文最重要的发现是：原算法即使在“该报错时就报错”的直觉下，也可能先 timelock。
2. non-anchored jitter 会积累 drift，这解释了为什么它在约 `1031ms` 左右就能把系统推到出错边界。
3. timeout 在 `UPPAAL` 里需要手工搭建，这本身就暴露了高层时间操作符和低层 timed automata 之间的落差。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先把 sound/video arrival streams 建成输入 automata。
2. 再把 manager、watchdog 和 synchroniser 的职责拆开。
3. 用 `vmins` 和 watchdog clocks 编码 jitter / skew 规则。
4. 通过 error-location reachability 查询分别检查各类同步失败。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata。
2. urgent channels，如 `sok`。
3. 全局 clocks `t1..t7` 与整数变量 `vmins`。
4. error-location reachability 查询。

### 交换与互操作

互操作重点在：

1. streams 只通过 `savail/vavail` 与 managers 接口。
2. managers 与 synchronisers 通过 `ready/ok/present` 三层动作分离“到达”“批准”“播放”。
3. watchdog 与 synchroniser 通过 `sokk/vokk` 和 `ums/ume` 等动作协同 precise timeout。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：无独立交换标准；模型直接承载在 timed automata 网络中。
- 仿真/执行支持：可利用 `UPPAAL` simulator 观察 timelock 形成路径。
- 验证/分析支持：支持 error-state reachability、timelock 观察和多种视频流假设下的对比验证。
- 代码生成/转换支持：原文未提供。
- 标准化或社区生态：依托 timed automata / timed process algebra 与多媒体同步研究路线。

## 适用场景与需求前提

### 适用场景

适合需要在设计阶段验证多媒体流同步算法、watchdog 逻辑和跨流 skew 策略的系统。

### 需求前提

1. 音视频流到达可抽成离散事件流。
2. 可接受的 jitter / skew 边界必须明确。
3. 同步控制主要由逻辑和时钟主导，而不是由复杂缓冲/自适应滤波主导。

### 不适用或高成本场景

如果系统依赖大容量缓冲、统计 QoS、自适应码率和网络概率延迟，仅用这里的 timed automata 抽象会过于粗糙。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是 timed automata 在多媒体同步领域的应用条目；相对 [formal-modeling-and-analysis-of-an-audio-video-protocol-an-industrial-case-study-using-uppaal/desc.md](../formal-modeling-and-analysis-of-an-audio-video-protocol-an-industrial-case-study-using-uppaal/desc.md)，两者都面向音视频系统，但一个验证 bus protocol，一个验证 presentation synchronisation algorithm；相对 [formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md](../formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md)，本文更突出 watchdog 和跨流时序容差。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求中包含“两个流之间的相对时间差必须落在窗口内”时，timed automata 非常适合做早期时序需求建模和漏洞暴露。

### 作为目标形式主义还是中间表示

对同步算法验证，它可以直接作为目标形式主义；对更大系统，它也可以作为从 QoS 需求到形式模型的中间层。

### 对需求到模型生成的启发

1. 应把单流约束和跨流约束拆开建模。
2. `watchdog` 与 `synchroniser` 分层是非常有价值的结构化建模习惯。
3. 自然语言里含糊的“立刻”“恰好”“最晚”在模型里必须分清 bounded timeout 还是 precise timeout。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文依赖的 timed automata 理论基础。
- [formal-modeling-and-analysis-of-an-audio-video-protocol-an-industrial-case-study-using-uppaal/desc.md](../formal-modeling-and-analysis-of-an-audio-video-protocol-an-industrial-case-study-using-uppaal/desc.md)：同属音视频领域 `UPPAAL` 经典案例，但对象是 bus 协议。
- [formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md](../formal-verification-of-a-power-controller-using-the-real-time-model-checker-uppaal/desc.md)：同样展示 `UPPAAL` 如何承接严格时间窗口与工业/系统级需求。

## 文献分类总结

- 形式主义：`Timed Automata / Lip-Synchronisation Controller Network`
- 成熟度：时钟、watchdog 和 reachability 查询链条完整，但也暴露出 `UPPAAL` 在高层 timeout 表达上的一些工程成本。
- 条目价值：这是一篇 `⏱️` 类同步算法应用条目，核心价值在于用 timed automata 自动揭示了 lip-sync 算法的真实边界与 timelock 风险。
