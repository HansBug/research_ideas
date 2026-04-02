# 基于 Petri 网的港口运输系统防碰撞监督器设计 / Petri Net Approach of Collision Prevention Supervisor Design in Port Transport System

## 基本信息

- 标题：Petri Net Approach of Collision Prevention Supervisor Design in Port Transport System
- 中文标题：基于 Petri 网的港口运输系统防碰撞监督器设计
- 作者：Danko Kezić、Igor Vujović、Anita Gudelj
- 发表：*Promet - Traffic&Transportation*, 19(5): 269-275, 2007
- DOI：原文未提供
- 链接：https://traffic2.fpz.hr/index.php/PROMTT/article/view/2234
- 形式主义：`Ordinary Petri Net + P-Invariant Supervisor`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🏭
- 论文角色：港口 AGV / HOV 混行防碰撞监督控制
- 工具/实现获取方式：原文给出普通 `Petri Net` 建模、`P-invariant` 监督器计算步骤和仿真验证思路，但未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 ordinary `Petri Nets`、control places 和 `P-invariant` 计算；原文未给出独立交换标准。

## 简报

这篇论文处理的是一个很典型但也很容易被忽略的场景：港口里并不只有全自动 `AGV`，还会有人工驾驶的 `HOV` 与它们共用交叉区。作者把港口局部运输系统分成多个危险区，把车辆进入/离开这些区看成离散事件，再用普通 `Petri Net` 与 `P-invariant` 方法计算 control places，综合出一个只在“即将发生碰撞”时才阻塞动作的监督器。

- 形式主义定位：这是 ordinary `Petri Net` 在港口运输并发监督控制中的应用条目，重点是 `P-invariant` 约束综合。
- 构造方式简述：先分别建模 `AGV` 循环路径与 `HOV` 的 command-response 行为，再针对 zones 和共享 crane 定义 forbidden constraints，最后生成 control places。
- 基础设施与场景简述：依托视频检测、离散事件 supervisor 与 `Petri Net` 结构分析，适合港口运输、混合人机交通和交叉区避碰。

```text
port transport zones + AGV/HOV events -> process Petri net -> forbidden-state constraints -> P-invariant control places -> collision prevention supervisor
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. 港口局部运输系统中的 `AGV`、`HOV` 和 cranes。
2. 以路径 sections 和危险 zones 表示的离散状态。
3. 用普通 `Petri Net` 描述的 process net。
4. 以 `P-invariant` 为基础计算的 control places。
5. 视频系统检测到的 zone-level discrete events。

### 核心抽象

原文把 `P-T Petri Net` 写成：

$$
Q = (P, T, I, O, \Phi, m_0)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 places 集合。
2. `$T$` 是 transitions 集合。
3. `$I$` 是输入函数。
4. `$O$` 是输出函数。
5. `$\Phi$` 是弧权函数。
6. `$m_0$` 是初始 marking。

状态变化由经典状态方程给出：

$$
m' = m + A q
$$

上式中的符号逐项解释如下：

1. `$m$` 和 `$m'$` 是 firing 前后的 marking。
2. `$A$` 是 incidence matrix。
3. `$q$` 是 firing vector。
4. 这条方程表达了 transition firing 对 token 分布的更新。

监督控制部分，论文把 process net 约束写成：

$$
L \cdot m_p + m_e = b
$$

$$
A_e = L \cdot A_p,\quad m_{e0} = b - L \cdot m_{p0}
$$

上式中的符号逐项解释如下：

1. `$m_p$` 是 process net 的 marking。
2. `$m_e$` 是 supervisor net 的 marking。
3. `$L$` 是 constraints matrix。
4. `$b$` 是约束上界向量。
5. `$A_p$` 是 process incidence matrix，`$A_e$` 是 supervisor incidence matrix。
6. `$m_{e0}$` 是 supervisor 的初始 marking。

### 一个最小例子与通俗解释

最小例子是“两个车道靠近或交叉时，最多只允许一台车处在危险区”：

1. `AGV1` 和 `AGV2` 的相邻 lane 太近，被定义为 zone 1。
2. `AGV2`、`MAN1`、`MAN2` 在其他交叉区形成 zone 2-4。
3. 一旦视频系统检测到某区已有车辆进入，supervisor 就会禁止另一个冲突车辆继续触发进入 transition。
4. 等该区车辆离开后，相关 transition 再重新开放。

通俗地说，这套方法像“给每个危险区配一个令牌门禁”。谁先拿到令牌谁先过，别的车必须等。

### 运行 / 接受 / 转移语义

论文直接把港口危险区约束写成 marking inequality。例如 zone 1：

$$
m(p_3) + m(p_4) \le 1
$$

对其他交叉区，同样有：

$$
m(p_5) + m(p_6) + m(p_7) + m(p_8) \le 1
$$

上式中的符号逐项解释如下：

1. `$m(p_i)$` 表示 place `$p_i$` 中的 token 数。
2. 每个相关 place 都对应某个危险区中的车辆状态。
3. 右侧上界 `1` 表示该 zone 内最多只允许一辆车占用。

论文还处理了共享 crane 的互斥：

$$
q_1 + q_2 \le 1
$$

并把它转换成基于输入 places 的等价约束：

$$
m(p_1) + m(p_2) \le 1
$$

上式中的符号逐项解释如下：

1. `$q_1,q_2$` 分别对应两个争用 crane 的 transition firing。
2. 转换后变成 marking 约束，便于并入 `P-invariant` 监督控制框架。

### 语义边界

这篇论文的边界比较清楚：

1. 它主要处理 zone-level collision prevention，不讨论精细轨迹规划。
2. 人类驾驶行为被抽象成 command-response，不是连续驾驶学模型。
3. 强项是紧凑离散监督控制，不是高保真港口交通仿真。
4. 依赖视频/传感系统能把车辆进入危险区准确离散化。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 普通 `Petri Net` | `$Q = (P, T, I, O, \Phi, m_0)$` | 给出 process net 的基本结构。 |
| 状态方程 | `$m' = m + A q$` | transition firing 后 marking 如何更新。 |
| 监督约束 | `$L \cdot m_p + m_e = b$` | 把 forbidden-state 约束写成可综合的线性形式。 |
| supervisor 计算 | `$A_e = L \cdot A_p,\ m_{e0} = b - L \cdot m_{p0}$` | 由约束直接求 control places。 |
| zone 约束 | `$m(p_3)+m(p_4)\le 1$` | 危险区内最多只允许一辆车。 |
| crane 互斥 | `$q_1 + q_2 \le 1$` | 共享装卸资源不能被同时占用。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 车辆所在路段、危险区和装卸位都由 places 显式表示。 |
| 事件 / 触发 | 强支持 | 进入/离开路径 section 和 crane 操作都是 transition。 |
| 守卫 / 数据 | 部分支持 | 重点在占用约束，不在复杂业务数据。 |
| 层次 | 部分支持 | process net 与 supervisor net 构成两层。 |
| 并发 / 同步 | 强支持 | 多车并发与共享区互斥是主体。 |
| 时间约束 | 不适用 | 本文不处理定时 firing 或 deadline。 |
| 连续动态 / 随机性 | 不适用 | 采用纯离散事件抽象。 |
| 可执行 / 可验证性 | 强分析 | `P-invariant` 直接生成 maximally permissive supervisor。 |

### 形式化问题与性质

1. 论文的关键不是“港口有碰撞风险”这个常识，而是“如何用 control places 自动合成只阻塞危险动作的 supervisor”。
2. `P-invariant` 方法避免了纯 automata 状态爆炸的缺点。
3. 把人类驾驶车辆也纳入同一离散监督框架，是这篇应用条目的一个亮点。
4. 对 `Petri Net` 主干来说，它提供了非常清晰的混合人机交通监督控制证据。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 把 `AGV` 路径分成若干 sections，形成循环 `Petri Net`。
2. 把 `HOV` 行为按 command-response 方式展开成可控/不可控 transition。
3. 定义危险 zones 与共享资源的线性约束。
4. 再由 `P-invariant` 方法生成 control places。

### 机器可处理承载方式

原文涉及的机器可处理承载方式包括：

1. process `Petri Net` 的 incidence matrix。
2. constraints matrix `$L$`。
3. supervisor incidence matrix `$A_e$` 与初始标记 `$m_{e0}$`。
4. 视频系统产生的 discrete event feedback。

### 交换与互操作

论文没有定义开放交换标准，但给出了清楚的控制接口：

1. 视频系统检测车辆 movement events。
2. supervisor 接收这些事件并发出 allow / disallow 命令。
3. `AGV` 与 `HOV` 共同遵守 control places 给出的互斥约束。

## 配套基础设施

- 建模/编辑工具：原文未指定专用工具，重点是 `Petri Net` 数学建模。
- 解析/交换/元模型支持：无独立交换格式。
- 仿真/执行支持：原文说明用 computer simulation 验证 supervisor。
- 验证/分析支持：`P-invariant` 计算与 composite `Petri Net` 分析。
- 代码生成/转换支持：原文没有自动代码生成，但给出完整 supervisor 计算流程。
- 标准化或社区生态：建立在 ordinary `Petri Nets` 与离散事件监督控制传统上。

## 适用场景与需求前提

### 适用场景

适合港口运输、AGV 与人工车辆共用通道、交叉区互斥与共享装卸资源控制等场景。

### 需求前提

1. 车辆运动可离散成 sections 或 zones。
2. 危险区进入/离开能被传感器或视频系统可靠检测。
3. 关注点主要是碰撞避免和共享资源互斥。
4. 驾驶员行为可以接受 command-response 抽象。

### 不适用或高成本场景

若系统核心在连续轨迹优化、细粒度人因建模或不确定交通流，本文的离散 zone abstraction 会显得过粗。

## 与相邻形式主义的关系

相对 [petri-nets-properties-analysis-and-applications/desc.md](../petri-nets-properties-analysis-and-applications/desc.md)，本文是典型的应用侧监督控制实例；相对 [a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)，它更强调 AGV 与人类驾驶车辆混行的安全门控；相对 [towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md](../towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md)，它更早也更纯粹地展示了 `P-invariant` 式 control-place 合成。

## 与本研究的关系

### 对 Project 1 的价值

它说明只要需求里有“共享危险区、互斥通过、人机混行”，`Petri Net` 就往往比普通状态机更自然，因为 token 和 control places 可以直接承担 supervisor 语义。

### 作为目标形式主义还是中间表示

对港口交通和并发资源场景，它完全可以作为目标形式主义；对更一般控制系统，它也适合作为并发/互斥层的中间表示。

### 对需求到模型生成的启发

1. 需求中应显式抽取危险区、共享资源和可控/不可控事件。
2. forbidden-state 约束可以直接转成 `Petri Net` 监督控制约束。
3. 对人机协同系统，离散事件抽象常常足以支撑第一层安全监督。

### 现实限制

本文模型对时间与连续空间的刻画较粗，因此更适合做高层安全门控，而不是低层导航控制。

## 重要的相关工作

- [petri-nets-properties-analysis-and-applications/desc.md](../petri-nets-properties-analysis-and-applications/desc.md)：普通 `Petri Net` 性质与分析主线。
- [a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)：多机器人协调的 `Petri Net` 在线控制器。
- [towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md](../towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md)：更现代的人机协作安全 `Petri` 条目。

## 文献分类总结

- 这是一篇 `🕸️` 类应用条目，核心贡献是把港口混合人机运输系统压成 ordinary `Petri Net`，并用 `P-invariant` 方法综合 collision prevention supervisor。
- 其对象是并发车辆与共享区资源流，因此记为 `🏭`；场景属于工业运输与自动化监督控制，因此领域记为 `🏭`。
- 对状态机族演化树而言，它补强的是 `Petri Nets` 主干在港口交通与人机混行监督控制上的应用证据，不单独生成新节点。
