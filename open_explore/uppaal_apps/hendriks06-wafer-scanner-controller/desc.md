问题一句话：本文验证的是半导体 `EUV` wafer scanner 的资源分配与调度控制，核心问题是如何在避免 deadlock 的同时让曝光子系统达到最优吞吐。
方法一句话：作者先用 `SMV` 在抽象有限状态模型上求出最小约束的 deadlock avoidance policy，再用与之 stuttering bisimulation 对齐的 `UPPAAL` 时序模型搜索最优吞吐 schedule。
验证收获一句话：结果表明可以把 deadlock avoidance policy 压缩成一个很短的布尔谓词，并在细化 `UPPAAL` 模型中找到以 `EXPOSE + SWAP` 为周期上界的最优稳定吞吐调度；相反，先验限制 wafer 单向流会明显拉低吞吐。

## 基本信息

- 标题：Model Checker Aided Design of a Controller for a Wafer Scanner
- 中文标题：借助模型检查器设计晶圆扫描机控制器
- 作者：Martijn Hendriks、Barend van den Nieuwelaar、Frits Vaandrager
- 单位：Radboud University Nijmegen；Eindhoven University of Technology；工业背景为 `ASML`
- 发表：*International Journal on Software Tools for Technology Transfer*，`8(6)`，2006
- DOI：`10.1007/s10009-006-0025-7`
- 链接：[DOI](https://doi.org/10.1007/s10009-006-0025-7)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🏭 工业与基础设施
- 被验证系统：`ASML` `EUV` wafer scanner 中 locks / internal robots / chucks 组成的 wafer flow 调度系统
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文作者主页当前仍提供 `SMV/UPPAAL` 模型压缩包。
- 案例/数据获取方式：案例来自 `ASML` `EUV` wafer scanner 设计；论文正文详述 wafer flow、资源结构和时间操作。

## 简报

这篇论文验证的不是控制器代码细节，而是一个典型的工业资源分配问题：晶圆在 locks、双臂 internal robots 与双 chuck 之间如何流动，既不能互相堵死，又要让最昂贵的曝光镜头尽量一直工作。

- 系统：`EUV` wafer scanner 的 wafer flow 与资源调度控制。
- 特点：`4` 个 locks、`2` 个 internal robots（各 `2` arms）、`2` 个 chucks，存在交叉物流路径和 deadlock 风险。
- 规模：抽象 `SMV` 模型有 `10` 个位置变量、`22` 个异步 process 和 `57116` 个 reachable states。
- 模型：`SMV` 负责 deadlock avoidance，`UPPAAL` 负责带时间延迟的调度优化。
- 性质：最小约束 deadlock avoidance、稳定吞吐最优、不同设计方案的 throughput 对比。
- 方法：先抽象后细化，并通过 stuttering bisimulation 让两层模型保持逻辑一致。
- 结果：找到 exact deadlock avoidance policy，并在 `UPPAAL` 中求得稳定吞吐达到 `mins = EXPOSE + SWAP` 的 schedule；若强行把进出 wafer 分成单向 locks，吞吐会降到 `1.61 * mins`。

`EUV wafer flow -> SMV 抽象资源分配模型 -> exact DAP -> UPPAAL 时序细化模型 -> observer 搜索最优 schedule -> 比较备选设计吞吐`

## 论文定位

这是 `uppaal_apps/` 里很强的一篇工业调度案例。它证明 `UPPAAL` 不只是“检查时序错误”，还可以与另一层抽象模型协作，解决工业设备的资源分配和吞吐优化问题。

## 验证对象与问题背景

### 系统与场景

对象是 `ASML` 正在开发的 `EUV` wafer scanner。由于 `EUV` 光在空气中会被吸收，设备内部处于真空环境，wafer 需要在 locks、internal robots 和 chucks 之间移动完成测量、曝光和出舱。

### 系统组成与运行机制

一片 wafer 的路径固定为：

`lock -> internal robot -> chuck -> internal robot -> lock`

系统核心资源包括：

1. `4` 个 locks；
2. `2` 个 internal robots；
3. 每个 robot 有 `2` 个 arms；
4. `2` 个 chucks。

wafer 先进入 lock，减压后由 robot 取走，送至处于 measure position 的 chuck，经过测量、chuck swap 和曝光后，再由 robot 送回 lock，最后被外部 track robot 取出。

### 验证边界

论文关注的是 wafer 流动、资源占用、deadlock avoidance 和 throughput，不深入真实控制软件细节，也不展开所有物理过程。

### 核心问题

1. 多条交叉物流路径很容易形成 deadlock；
2. 简单地把进出路径做成单向虽然能防死锁，但会降低吞吐；
3. 需要找出既最不保守又能保证无死锁的控制策略。

## 模型与形式化建模

### 抽象对象

`SMV` 模型用 `10` 个位置变量表示 `4` 个 locks、`4` 个 robot arms 和 `2` 个 chucks。每个位置只有三种状态：

1. `e`
   - empty；
2. `r`
   - 持有未曝光 wafer；
3. `g`
   - 持有已曝光 wafer。

### 建模形式

1. **`SMV`**
   - 抽象掉机器人转向、chuck swap 和测量细节，只保留资源占用与 wafer 颜色变化；
2. **`UPPAAL`**
   - 细化加入时间延迟、转向动作、observer process 和启发式剪枝。

### 关键抽象与取舍

1. `SMV` 模型足够小，便于穷尽地求 safe states；
2. `UPPAAL` 模型更细，但无法直接完整求 CTL 层面的最小约束 DAP；
3. 两者通过 stuttering bisimulation 建立形式关联，从而把 `SMV` 中求得的 DAP 可靠带入 `UPPAAL`。

## 验证目标与性质

### 待验证问题

论文处理两大问题：

1. **Deadlock avoidance**
   - 找到 least restrictive deadlock avoidance policy；
2. **Throughput optimization**
   - 在死锁避免前提下寻找稳定期最优 schedule。

### 性质类型

这些性质覆盖：

1. 死锁安全；
2. 可达性 / 安全状态表征；
3. 吞吐优化；
4. 设计替代方案比较。

### 查询表达

`UPPAAL` 中通过 observer 验证如下形态的性质：

`EG ((observer.LO and observer.x < H) and (observer.L1 and observer.x < S))`

含义是：第一次 unload 在 `H` 内发生，之后相邻 unload 间隔始终不超过 `S`。

## 核心方法与验证流程

1. 在 `SMV` 中建立资源占用抽象模型；
2. 形式化 deadlock，并计算全部 safe states；
3. 将 safe-state 表征压缩成一个很短的布尔 deadlock avoidance policy；
4. 在 `UPPAAL` 中建立带时间的细化模型，并加入 observer；
5. 用来自 `SMV` 的 DAP 约束 `UPPAAL`，再结合若干启发式剪枝搜索稳定吞吐最优 schedule；
6. 最后比较两种替代设计：单向锁流和更小资源配置。

## 案例与结果

### Deadlock avoidance

`SMV` 模型有 `57116` 个 reachable states，接近理论总数 `3^10 = 59049`。作者成功求出了 exact deadlock avoidance policy，并指出该策略可以直接实现为控制器中的简短布尔判断。

### Throughput optimization

在 `UPPAAL` 中，作者证明：

1. 最优稳定吞吐对应的相邻 unload 间隔可达到 `mins = EXPOSE + SWAP`；
2. 第一次 unload 时间只比理论下界 `minH` 高约 `5%`；
3. 这意味着曝光镜头几乎只被必要的 chuck swap 打断，处于非常高的利用率。

### 设计对比

如果把输入 wafer 固定走上方 locks、输出 wafer 固定走下方 locks，以避免 deadlock：

1. 虽然不会死锁；
2. 但吞吐下降到 `1.61 * mins`；
3. 说明先验强约束会显著牺牲性能。

若进一步把系统缩成 `2` 个 locks 和 `1` 个 internal robot，则只能找到约 `1.82 * mins` 的 schedule。

## 与本研究的关系

### 相关性分析

这篇论文非常适合作为博士研究第三部分“验证剖面”和第四部分“修复/优化”之间的桥梁案例，因为它展示了如何从安全控制策略进一步走向性能优化。

### 可借鉴之处

1. 用粗模型求精确安全边界，再把结果投射到细模型。
2. 将不同抽象层模型通过形式关系连接，而不是靠经验“感觉相近”。
3. 用 observer 过程把吞吐优化问题转写成 `UPPAAL` 可处理的时序性质。

### 存在的不足与改进空间

1. `UPPAAL` 侧仍依赖若干启发式剪枝，可能丢掉更好 schedule。
2. 论文更关注资源流和吞吐，对更细的软件控制逻辑展开不多。
3. 该方法在更大规模资源系统上仍会遇到状态空间问题。

### 对本研究的启发

它直接说明：在复杂控制/生产系统中，应该允许“不同层次模型各司其职”。一个模型负责求安全边界，另一个模型负责求时序性能，然后通过形式关系把结论接起来。这对博士研究中“生成-验证-修复”的闭环组织很有参考价值。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 直接可用
- 判断依据：作者主页当前仍提供该论文相关模型压缩包。
- 获取方式/链接：[DOI](https://doi.org/10.1007/s10009-006-0025-7)；[作者主页](https://sws.cs.ru.nl/publications/papers/martijnh/)；[模型压缩包](https://sws.cs.ru.nl/publications/papers/martijnh/MAD-04/Models.zip)
- 对后续复用的现实影响：这是公开度很高的工业调度案例，适合直接复跑 deadlock avoidance 和 throughput 优化流程。
