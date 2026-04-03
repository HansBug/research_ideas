# 基于定时自动机的无线传感器网络 DoS 攻击建模与验证 / Timed Automata Based Modeling and Verification of Denial of Service Attacks in Wireless Sensor Networks

## 基本信息

- 标题：Timed Automata Based Modeling and Verification of Denial of Service Attacks in Wireless Sensor Networks
- 中文标题：基于定时自动机的无线传感器网络拒绝服务攻击建模与验证
- 作者：Youcef Hammal, Quentin Monnet, Lynda Mokdad, Jalel Ben-Othman, Abdelkarim Abdelli
- 发表：*Studia Informatica Universalis*, 12(1):1-46, 2014
- DOI：原文未提供
- 链接：https://www.qmo.fr/publications/timed-automata-based-modeling-and-verification-of-denial-of-service-attacks-in-wireless-sensor-networks/
- 形式主义：`Timed Automata / UPPAAL WSN Defense Network`
- 主类：⏱️
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：`WSN` DoS 防御建模 / 定时自动机应用建模
- 工具/实现获取方式：原文用 `UPPAAL` 建立 cluster head、medium、node、`cNode`、`vNode` 和 compromised node 的 timed automata，并用 `ns-3` 做能耗对照仿真；论文未给公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata templates、广播/同步 channel、整型数组和 CTL 风格查询；不是行业标准交换格式。

## 简报

这篇论文处理的是一个很具体的 `WSN` 安全问题：如果集群里有若干监测节点 `cNode` 负责监听流量并报告异常，那么这些 `cNode` 自己该怎么选，才能既考虑剩余能量，又不让恶意节点长期霸占监督角色？作者的做法是把 cluster head、medium、普通 sensing node、`cNode`、`vNode` 以及 compromised node 都压成 communicating timed automata，再用 `UPPAAL` 检查“节点会不会被覆盖”“能量耗尽后是否会断开”“`cNode` / `vNode` 是否会出现不该出现的组合”等性质。

- 形式主义定位：这是 `Timed Automata` 在安全感知型 `WSN` 协议/监督机制上的应用条目，重点是“带 clocks 的集群节点角色演化与防御逻辑”。
- 构造方式简述：先定义 residual energy、sleep / awaken 周期、`cNode/vNode` 选举与 claim 机制，再把 cluster head、region medium 和 node 模板化成 `UPPAAL` timed automata network。
- 基础设施与场景简述：依托 `UPPAAL` 做 reachability / safety / leads-to 检查，再用 `ns-3` 对能耗和负载均衡做应用侧评估。

```text
clustered WSN attack-defense rules -> CH / medium / node / cNode / vNode timed automata -> UPPAAL CTL queries -> role-election / suspicion / energy / liveness validation
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. cluster head (`CH`)。
2. 普通 sensing node、`cNode` 和 `vNode` 三种主要角色。
3. compromised node 的恶意行为。
4. region medium 与广播/同步 channel。
5. residual energy、sleep / awaken 周期、election 周期等 clocks 和整数变量。
6. `UPPAAL` 查询语言中的 reachability / safety / liveness 性质。

### 核心抽象

论文先给出 untimed automaton：

$$
A = \langle Q, \Sigma, \to, q_0 \rangle
$$

上式中的符号逐项解释如下：

1. `$Q$` 是位置集合。
2. `$\Sigma$` 是交互事件集合。
3. `$\to \subseteq Q \times \Sigma \times Q$` 是边集合。
4. `$q_0$` 是初始位置。

随后将其扩展为 timed automaton：

$$
A_T = \langle A, \Chi, I, G, Z \rangle
$$

上式中的符号逐项解释如下：

1. `$A$` 是上一式中的 untimed automaton 骨架。
2. `$\Chi$` 是时钟集合。
3. `$I$` 把 invariant 赋给位置。
4. `$G$` 把 timing guard 赋给边。
5. `$Z$` 为边指定需要复位的 clocks。

论文在 `UPPAAL` 中进一步把整网写成模板化 timed automata network，可保守整理为：

$$
\mathcal{N}_{wsn} = A_{CH} \parallel A_{M,1} \parallel \cdots \parallel A_{M,r} \parallel A_{N,1} \parallel \cdots \parallel A_{N,n}
$$

上式中的符号逐项解释如下：

1. `$A_{CH}$` 是 cluster head automaton。
2. `$A_{M,i}$` 是第 `$i$` 个 region medium。
3. `$A_{N,j}$` 是第 `$j$` 个 node automaton。
4. node automaton 会在 sensing / `cNode` / `vNode` 模式间切换。
5. `$\parallel$` 表示按同步 channel 和共享变量组合的 timed automata network。

### 一个最小例子与通俗解释

最小例子可以理解成一个 cluster 中的三步循环：

1. cluster head 收集所有节点 residual energy，并选出若干 `cNode`。
2. 被选中的 `cNode` 在一个周期内持续监听周边节点流量；若某节点发包异常，就沿 `claimSuspected` 向 `CH` 报告。
3. 与此同时，邻居中的 `vNode` 会周期性询问 `cNode` 的 residual energy，并把本地观察与理论能耗模型对比；若不一致，也向 `CH` 报告。

通俗地说，这像“让一群带秒表的状态机互相监督”。普通 `FSM` 只能表达“谁在什么角色”，而 timed automata 还能表达“多久醒一次”“多久发一次能量请求”“在一个 election cycle 内会不会发生不该发生的角色组合”。

### 运行 / 接受 / 转移语义

论文中的 timed semantics 写成：

$$
(q,v) \xrightarrow{a} (q', v[Z(e):=0]), \qquad (q,v) \xrightarrow{\delta} (q, v+\delta)
$$

上式中的符号逐项解释如下：

1. `$q,q'$` 是当前位置与目标位置。
2. `$v$` 是当前 clock valuation。
3. `$a$` 是离散动作，如选举、发送 claim、请求 residual energy。
4. `$Z(e)$` 是在边 `$e$` 上被复位的 clocks 集合。
5. `$\delta$` 表示时间流逝。

论文给出的一个典型 safety 查询是：

$$
A[]\big(CH:Enquiring \Rightarrow CH:i == NBR\_REGIONS\big)
$$

上式中的符号逐项解释如下：

1. `CH:Enquiring` 表示 cluster head 正在进入选举相关询问阶段。
2. `CH:i == NBR_REGIONS` 要求它此时已经拿到了所有 region medium。
3. 这条性质保证选举不会在 region 信息不全时启动。

典型的 liveness / leads-to 性质则是：

$$
node0:residualEnergy \le 0 \;\rightsquigarrow\; node0:Disconnected
$$

以及

$$
CH:Asleep \;\rightsquigarrow\; CH:Awaken
$$

上式中的符号逐项解释如下：

1. `$\rightsquigarrow$` 对应 `UPPAAL` 中的 leads-to 语义。
2. 第一条性质要求电量耗尽的节点最终断开。
3. 第二条性质要求睡眠状态最终能回到唤醒状态。

论文还用 reachability 查询检查：

$$
E\Diamond node0:Idle\_CNode
$$

表示存在一条执行路径使 `node0` 在某个未来周期内成为 `cNode`。

### 语义边界

这篇论文的边界主要有：

1. 它的核心是 role election 与 defense logic，不是低层无线信道物理层精确建模。
2. 论文用集群结构和 region medium 缩小状态空间，因此并不面向任意开放拓扑。
3. `vNode` 的能耗模型是离散近似，而不是连续功耗方程。
4. 实验部分用 `ns-3` 评估能耗，但形式语义主线仍在 `UPPAAL` timed automata。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| untimed automaton 骨架 | `$A = \langle Q, \Sigma, \to, q_0 \rangle$` | 节点/部件的离散角色流转基础。 |
| timed automaton 扩展 | `$A_T = \langle A, \Chi, I, G, Z \rangle$` | 在角色流转上加入时钟、不变式和复位。 |
| 全网组合 | `$\mathcal{N}_{wsn} = A_{CH} \parallel A_{M,1} \parallel \cdots \parallel A_{N,n}$` | 把 CH、medium 和 nodes 组合成可检网络。 |
| 选举安全性 | `$A[](CH:Enquiring \Rightarrow CH:i == NBR\_REGIONS)$` | 只有掌握所有 region 时才允许启动选举。 |
| `cNode` 可达性 | `$E\Diamond node0:Idle\_CNode$` | 某节点有机会在未来被选为 `cNode`。 |
| 电量耗尽响应 | `$node0:residualEnergy \le 0 \rightsquigarrow node0:Disconnected$` | 电量耗尽后最终要断开。 |
| 睡眠唤醒活性 | `$CH:Asleep \rightsquigarrow CH:Awaken$` | 系统不能永远卡在睡眠状态。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | sensing、`cNode`、`vNode`、compromised 等模式都显式建模。 |
| 事件 / 触发 | 强支持 | 选举、请求能量、发送 claim、sleep / wake 都是显式动作。 |
| 守卫 / 数据 | 强支持 | residual energy、claim 计数、node list、region coverage 都进入 guard / update。 |
| 层次 | 弱支持 | 不是层次状态机，但通过 CH / medium / node 模板化分工组织系统。 |
| 并发 / 同步 | 强支持 | 所有节点、medium 和 CH 并行运行并用 channel 同步。 |
| 时间约束 | 强支持 | sleep / awaken 周期、选举周期和请求周期是模型主体。 |
| 连续动态 / 随机性 | 不支持 | `ns-3` 仿真在外部，形式模型主体仍是离散 timed automata。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 查询和 `ns-3` 对照让结构和应用两侧都可检。 |

### 形式化问题与性质

1. 这篇论文最值得保留的是“安全监督角色本身也需要被形式化监督”这一点。
2. `cNode/vNode` 的双重角色机制使它不是简单的“节点监听器”应用，而是一个稳定的 timed role-evolution 模型。
3. 对 `project_1` 而言，它展示了如何把安全策略、周期行为和节点角色一起压成可检查的 timed automata。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 明确 cluster、region、node 与 role-election 规则。
2. 用 `UPPAAL` 模板化 CH、medium 和 node。
3. 用 broadcast / binary channel 表达选举、请求与 claim。
4. 用整型数组保存 residual energy、`setOfCNodes`、`nbrClaims` 等全局状态。
5. 写 reachability / safety / liveness 查询验证结构正确性。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata templates。
2. clock / integer / channel arrays。
3. `UPPAAL` 查询公式。
4. `ns-3` 仿真配置参数。

### 交换与互操作

互操作重点在：

1. CH 如何与所有 region medium 协调选举。
2. `cNode` / `vNode` 如何通过请求/报告 channel 同步。
3. `UPPAAL` 负责形式验证，`ns-3` 负责应用层能耗对照。

## 配套基础设施

- 建模/编辑工具：原文直接基于 `UPPAAL` 编辑器和查询语言建模。
- 解析/交换/元模型支持：无统一外部元模型；主要承载为 `UPPAAL` 网络模板与数组变量。
- 仿真/执行支持：`UPPAAL` 做形式执行，`ns-3` 做能耗与负载均衡仿真。
- 验证/分析支持：支持 reachability、safety、leads-to 和 deadlock 检查。
- 代码生成/转换支持：原文未提供部署级代码生成。
- 标准化或社区生态：依托 `UPPAAL`、`ns-3` 与 `WSN` 安全研究生态。

## 适用场景与需求前提

### 适用场景

适合 clustered WSN、需要在能量约束下持续运行监测节点并防止恶意节点长期占据监督角色的场景。

### 需求前提

1. 网络可按 cluster / region 有限化。
2. 节点角色和攻击相关行为可离散为有限状态。
3. 关键防御问题集中在角色选举、监督与报错，而不是完整无线物理层。

### 不适用或高成本场景

如果系统需要精确模拟无线信号衰减、复杂概率攻击分布或大规模动态拓扑变化，仅靠这里的 `UPPAAL` 角色网络会过于粗粒度。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是典型 `WSN` 安全应用；相对 [timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md](../timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md)，这里不是日志攻击检测，而是节点角色与选举机制建模；相对 [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，这里关注的是安全监督与能耗角色，而不是中间件 callback 时序。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果需求中包含“周期唤醒、角色切换、剩余能量、监督者再监督”这类条件，生成状态机时应该显式保留 clocks、claim channel 和 role set，而不是只输出高层防御流程。

### 作为目标形式主义还是中间表示

对 `WSN` 安全监督，它可以直接作为目标形式主义；对更一般的控制需求，也适合作为角色/周期层的中间表示。

### 对需求到模型生成的启发

1. 安全机制中的“监督者”角色本身也要进模型。
2. residual energy、周期唤醒和选举窗口适合直接映射为时钟与整型变量。
3. 防御逻辑的很多自然语言条件都能转成 leads-to 或 safety 查询。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：本文所有应用建模的时间语义母体。
- [timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md](../timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md)：同样是安全场景中的 timed automata network 应用。
- [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：展示 timed automata 如何继续推广到通信与控制运行时验证。

## 文献分类总结

- 形式主义：`Timed Automata / UPPAAL WSN Defense Network`
- 成熟度：`UPPAAL + ns-3` 双链路明确，属于结构验证与应用评估都比较完整的条目。
- 条目价值：这是一篇 `⏱️` 类高价值应用条目，核心贡献是把 `cNode/vNode` 监督机制压成可检查的 timed automata network。
