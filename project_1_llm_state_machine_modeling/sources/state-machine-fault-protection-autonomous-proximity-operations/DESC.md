# 自主近距离接近任务的状态机容错保护 / STATE MACHINE FAULT PROTECTION FOR AUTONOMOUS PROXIMITY OPERATIONS

## 论文在讲什么

这篇论文讨论的是航天器在自主近距离接近和捕获任务中，如何把 fault protection 从传统 rule-based limit checking 升级成 state-machine-based supervisor。作者把应用背景放在 Mars Sample Return：服务航天器在接近 orbiting sample canister 时，必须在没有地面实时介入的情况下完成 terminal rendezvous、捕获和故障恢复，因此仅靠简单阈值告警已经不够。

文章先用 fault tree 分析故障模式，再把它们映射到一个 mission-phase state machine。最重要的不是“验证方法”本身，而是作者把接近过程明确拆成 `Passive Standby`、`Passive Miss Region`、`Active Abort Region`、`Unavoidable Intercept Region`、`Locate OS` 等离散阶段，并给出各阶段的风险含义、转移条件和 abort 处理方式。这样一来，fault protection 不再只是“某个量超限就报错”，而是与当前任务状态和风险区间强绑定。

## 控制系统在文中的位置

控制系统描述是这篇论文的主角之一。虽然论文也讲了 fault tree、generic modular architecture 和未来 autocoding，但真正支撑全文的是 rendezvous and capture process 本身的状态化建模。没有这条状态链，后面的 fault protection response、zone-sensitive risk calibration 和 nominal/off-nominal 切换都无从谈起。

从 `sources/` 角度看，它也不是一般的“航天故障管理框架稿”。这里研究的对象是一个真实 mission supervisor：状态与任务阶段直接对应，abort 是否可行受当前 region 决定，capture 是否成功又决定是否进入 `Locate OS`。这种把任务阶段、风险等级和恢复路径统一到一个离散监督器里的写法，对后续状态机建模数据集非常有价值。

## 对我们为什么有用

它对 `✈️` 方向的价值，在于补进了一个和常见起落架、UAV mission manager、CubeSat safe mode 都不太一样的“自主近距操作 + 容错保护”样本。这里的控制对象不是普通飞行姿态控制，而是 mission-critical proximity operations fault protection，重点是接近区间划分、abort 时机和 capture failure recovery。

这篇材料也非常适合作为 `FSM + T1` 的双 A 样本。它有稳定的状态名，有明确的 nominal/off-nominal 分支，有 `30-45 min / 5 min / 2 min` 这种局部时间窗口，还有 `Locate OS` 这样的恢复状态。对训练自然语言到状态机的任务来说，这种“任务阶段驱动的恢复链”比单纯的控制律或连续动力学更直接、更稀缺。

## 如果需要人工细读，建议怎么读

人工重读时，建议先直接看第 `9-10` 页的 zones of criticality 和 Figure `10` 所在部分，把 `Passive Miss / Active Abort / Unavoidable Intercept / Locate OS` 的职责和转移关系先读清楚。这一段已经足够恢复主状态链、风险窗口和 abort 边界，是最关键的样本证据。

随后再回到前面的 case-study 说明与 fault tree 分析部分，确认为什么这些状态被这样划分、哪些故障模式会触发哪些 response。更前面关于 generic architecture、industry adoption 和 broader fault-protection process 的讨论可以后读，因为那部分更偏方法背景，而不是先恢复近距离接近 supervisor 的必要材料。
