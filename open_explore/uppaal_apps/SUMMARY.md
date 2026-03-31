# UPPAAL 应用验证文库总账

本文件是 `open_explore/uppaal_apps/` 论文集的总账，用于记录当前已经正式入账的 `UPPAAL` 应用验证论文、分类口径、公开性盘点、更新进展和失败/阻塞历史。

## 文档定位与使用方式

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，了解本论文集定位和与 [uppaal_tech/README.md](../uppaal_tech/README.md) 的边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选、分流、回填和一致性检查规范。
3. 若任务涉及单篇 `desc.md`，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 最后使用本文件查看当前统计、统一论文表、公开性清单和失败记录。

## 当前关注边界

1. 这里只收录 `UPPAAL` 被用于**形式化验证具体模型或系统**的应用论文。
2. 主贡献是 `UPPAAL` 本体技术的论文，不在这里入账，应进入 [uppaal_tech/README.md](../uppaal_tech/README.md)。
3. 只是在正文中顺带提一下 `UPPAAL` 的条目，不应正式入账。
4. 主要目标是调度、优化、测试或控制合成，但没有清晰验证任务、性质或结论的论文，当前不作为优先收录对象。

## 检索关键词簇

### 当前推荐关键词簇

- `UPPAAL + formal verification/model checking + protocol/controller/embedded system/medical device/SCADA`
- `UPPAAL + schedulability/deadlock/reachability/response time/consistency/attack detection + case study`
- `UPPAAL SMC + schedulability + satellite/embedded software`
- `UPPAAL + AODV/pacemaker/radiation therapy/RapidIO/PLC/web service + verification`

### 已观察到的高命中特征

- 题目或摘要直接写清被验证系统名、验证任务词和 `case study`
- 正文明确说明系统组成、验证边界、性质簇和结果，而不是只写“应用了 `UPPAAL`”
- `2020` 年后，`UPPAAL Stratego / SMC` 与“具名应用场景 + 量化结果”联动出现得更频繁
- 官方模型仓库、作者 `GitHub/Zenodo`、公开数据页仍是高价值反向入口

### 已观察到的低命中特征

- 教程、综述或方法展示文，没有稳定具体系统边界
- 只讲 optimization/testing/scheduling，却没有清晰验证问题、查询或验证边界
- 只搜泛 timed automata 或泛 industry 词，没有具名系统名或性质词
- 历史案例页常能找到论文，但很多旧工件链接已经失效

### 检索倾向调整

- 当前高价值方向已扩展到：`Stratego` 铁路/交通控制、`SMC` 能量/疫情场景、医疗设备与网络协议、业务流程系统
- 只要用户没有明确豁免，正式入账时仍默认同步补齐 `desc.md`
- 公开性继续单独维护为“案例/模型/数据公开性清单”，不再回退到 `详度/实现`
- 对 `2020` 年后条目，优先选择能把“系统是什么、验证哪一层、规模多大、材料能否拿到”讲清楚的论文

## 当前收录统计

| 统计项 | 数值 | 年份信息 |
|---|---:|---|
| 已收录顶层条目 | 30 | 覆盖 `1996-2024` |
| 本轮新增条目 | 10 | 本轮新增均位于 `2020-2024` |
| 其中已补 `desc.md` | 30 | `1996-2024` 均已完成整理 |
| 当前 `🟢 直接可用` | 23 | 主体已扩展到协议、控制器、医疗、交通、公共健康与业务流程案例 |
| 当前 `🟡 可整理` | 7 | 主要是框架展示型、材料偏薄或验证边界偏窄的案例 |
| 当前 `⏳ 尚未提取` | 0 | 无 |
| 公开性分布 | `🟢 10 / 🟠 17 / 🔒 3` | 新增批次里可直接复跑的公开案例明显增多，但整体仍以论文重建为主 |
| 最早年份 | 1996 | 首批收录始于经典协议冲突案例 |
| 最晚年份 | 2024 | 已扩展到电子考试流程与可信设计案例 |
| 当前失败/阻塞记录 | 2 | 记录见“失败与阻塞记录” |

## 按年份分布统计

| 年份 | 条目数 | 已补 `desc.md` | 备注 |
|---|---:|---:|---|
| 1996 | 1 | 1 | Philips 音频协议总线冲突案例 |
| 1997 | 3 | 3 | 收录重传协议、TDMA 启动与 B&O 工业协议 |
| 1998 | 2 | 2 | 覆盖 lip sync 与车辆换挡控制 |
| 1999 | 1 | 1 | B&O 电源控制器验证 |
| 2000 | 1 | 1 | ABB `AF100` field bus 工业案例 |
| 2003 | 1 | 1 | multimedia `QoS` 验证案例 |
| 2010 | 4 | 4 | 扩展到 RapidIO、卫星调度、工业 PLC 与 `WS-AT` |
| 2011 | 2 | 2 | 覆盖医疗放疗控制与 `WS-BA` 协议 |
| 2012 | 2 | 2 | 覆盖 `UPPAAL SMC` 调度与 AODV 路由协议 |
| 2013 | 1 | 1 | 健康监测驾驶辅助系统框架案例 |
| 2019 | 2 | 2 | 扩展到 pacemaker 与 SCADA 攻击检测 |
| 2020 | 3 | 3 | 扩展到疫情流体模型、moving block 铁路与 WSN 攻击分析 |
| 2021 | 4 | 4 | 覆盖能量驱动计算、`5G` 切片、`TSN` 与城市交通灯控制 |
| 2022 | 1 | 1 | 扩展到在线针导航与医疗避障控制 |
| 2023 | 1 | 1 | 扩展到机械呼吸机控制验证 |
| 2024 | 1 | 1 | 扩展到电子考试流程可信设计 |

## 双轴分类口径

### 主轴分类

| Emoji | 主轴分类 | 含义 | 当前正式条目数 |
|---|---|---|---:|
| 🛰️ | 协议与通信机制 | 论文真正验证的是协议状态机、通信规则、消息协调或转发/同步机制 | 10 |
| 🎛️ | 控制器与设备控制 | 论文真正验证的是控制器、设备行为、执行逻辑或闭环控制结构 | 10 |
| ⏱️ | 调度、资源与性能分析 | 论文真正验证的是可调度性、资源竞争、时延、`QoS`、能量或其他性能边界 | 6 |
| 🧩 | 软件服务与业务流程 | 论文真正验证的是软件服务编排、角色协作、业务流程规则或工作流状态机 | 2 |
| 📊 | 场景行为与监测分析 | 论文真正验证的是日志模式、群体场景、策略评估或监测判定模型 | 2 |

### 次轴场景

| Emoji | 次轴场景 | 含义 | 当前正式条目数 |
|---|---|---|---:|
| 🌐 | 网络与分布式服务 | 网络协议、Web 服务、无线网络、`5G` 编排等 | 7 |
| 🎵 | 多媒体与消费电子 | 音视频协议、多媒体同步、消费电子组件等 | 5 |
| 🏭 | 工业与基础设施 | 工业自动化、现场总线、`SCADA`、工业网络等 | 5 |
| 🚦 | 交通、车载与铁路 | 交通灯、铁路、车辆控制、驾驶辅助等 | 4 |
| 🏥 | 医疗与健康 | 医疗设备、治疗系统、植入式设备、临床导航等 | 4 |
| 🚀 | 航天 | 卫星、航天任务软件与空间任务调度等 | 2 |
| 🦠 | 公共健康与疫情策略 | 传染病传播、接触追踪与公共卫生决策支持 | 1 |
| 🔋 | 能源与采能计算 | 采能系统、电池 sizing、能量迁移计算等 | 1 |
| 🎓 | 教育与考试流程 | 电子考试、教学流程与教育规则系统等 | 1 |

说明：

1. 本论文集不再把“验证对象类型”和“现实应用场景”压成单一 `领域`，而是统一维护 `主轴分类 + 次轴场景` 两列。
2. `主轴分类` 优先回答“这篇论文主要在验证什么”；`次轴场景` 再回答“它服务于什么现实对象或行业”。
3. 上述双轴只是当前版本的分类骨架，不是封闭不变的固定枚举。
4. 若后续实际收录中出现新的稳定对象簇或应用簇，或现有类别已经过宽，应按实际情况动态扩充、拆分或合并对应轴的类型。
5. 一旦发生动态调整，必须同步更新本节统计口径以及统一论文总表中的 `主轴` 与 `次轴` 字段。

## 状态与公开性口径

### 条目状态

| 状态 | 含义 |
|---|---|
| 🟢 | 直接可用：已有较完整单篇 `desc.md`，能直接服务博士研究比较或案例提炼 |
| 🟡 | 可整理：有价值，但案例规模、结构细节或复用度仍略弱于主代表案例 |
| ⚪ | 未收获：不满足目标，或无法形成可靠、可追溯的产物 |
| ⏳ | 尚未提取：论文已入库，但 `desc.md` 尚未完成 |

### 案例/模型/数据可获取性

| Emoji | 含义 |
|---|---|
| 🟢 | 可直接获取：存在当前可访问的公开下载链接、仓库、补充材料页或官方案例入口，能直接拿到相应材料 |
| 🟡 | 需联系申请：原文明确说明需要联系作者、团队或项目方申请 |
| 🟠 | 信息不清：原文或官网提到材料存在，但没有稳定、清晰、当前可用的公开路径，或历史链接已失效 |
| 🔒 | 难以取得：案例强依赖企业内部资产、工业实现、受限规格或现实上难以公开的材料 |

### `UPPAAL线` 口径

| 取值 | 含义 |
|---|---|
| `UPPAAL` | 主线工具或经典 `UPPAAL` 验证 |
| `UPPAAL SMC` | 统计模型检查应用 |
| `UPPAAL Tiga` | timed game / controller synthesis 相关应用 |
| `UPPAAL CORA` | cost-optimal / priced timed automata 相关应用 |
| `UPPAAL Stratego` | 策略综合、学习或规划相关应用 |
| `UPPAAL PORT` | 组件化、本地时间或 `PORT` 线应用 |
| `ECDAR` | timed I/O specification / compositional verification 相关应用 |
| `其他 UPPAAL 谱系变体` | 其他明确属于 `UPPAAL` 谱系的变体 |

## 统一论文总表

统一字段固定为：

`主轴 | 次轴 | 年份 | Key | 标题 | 关键词 | 被验证系统 | 系统特点 | 系统规模 | UPPAAL线 | 验证任务 | 性质类型 | 状态 | 一句话简介 | 链接`

维护规则：

1. `年份` 为必填字段；虽然当前表格把 `主轴` 与 `次轴` 放在最前两列，但全表仍必须按年份从低到高排列，同年按 `Key` 字典序稳定排序。
2. `主轴` 与 `次轴` 两列只保留 emoji，不再附加文字解释。

| 主轴 | 次轴 | 年份 | Key | 标题 | 关键词 | 被验证系统 | 系统特点 | 系统规模 | UPPAAL线 | 验证任务 | 性质类型 | 状态 | 一句话简介 | 链接 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 🛰️ | 🎵 | 1996 | `bengtsson96` | Verification of an Audio Protocol with Bus Collision Using UPPAAL | 音频协议, 总线冲突, 广播通信 | Philips 音频控制协议（双发送端冲突版本） | 单总线、广播/碰撞检测、工业背景 | `6` 个 automata；状态空间约为单发送端版的 `10^3` 倍 | `UPPAAL` | 协议碰撞处理与时序容错验证 | 安全、有界活性、时序容错 | 🟢 | 用 timed automata 验证双发送端冲突协议，并确定 `5%/6%` 容错边界。 | [paper](./bengtsson96-audio-protocol-bus-collision/) |
| 🛰️ | 🌐 | 1997 | `dargenio97` | The Bounded Retransmission Protocol Must Be on Time! | 文件传输, 有界重传, 超时 | BRP 有界重传文件传输协议 | 分块传输、丢包信道、超时/中止 | 发送端/接收端 + `T1/T2` 定时器；原文未给统一状态规模 | `UPPAAL` | 服务符合性与超时参数验证 | 安全、服务符合性、时序约束 | 🟢 | 通过 timed/untimed 对照说明 BRP 正确性依赖真实超时结构。 | [paper](./dargenio97-bounded-retransmission-time/) |
| 🛰️ | 🎵 | 1997 | `havelund97` | Formal Modelling and Analysis of an Audio/Video Protocol: An Industrial Case Study Using UPPAAL | 工业协议, 音视频总线, 碰撞检测 | Bang & Olufsen 音视频控制协议 | 单总线、`2800` 行汇编、工业真实协议 | `9` 个 automata；`5` 次主要迭代、约 `3` 个月；错误轨迹近 `2000` 步 | `UPPAAL` | 协议建模、错误定位与修复验证 | 安全、有界活性、一致性 | 🟢 | 通过自动诊断轨迹定位并修复 B&O 工业协议中的时序错误。 | [paper](./havelund97-audio-video-protocol/) |
| 🛰️ | 🌐 | 1997 | `lonn97` | Formal Verification of a TDMA Protocol Start-Up Mechanism | `TDMA`, 启动同步, 时钟漂移 | DACAPO `TDMA` 启动机制 | 多主站、启动同步、时钟漂移 | `4` 个站点 + 总线；时钟漂移 `±10^-3` | `UPPAAL` | 启动同步与截止时间验证 | 安全、有界响应、时序约束 | 🟢 | 证明四站 TDMA 系统能在漂移条件下于有界时间内完成同步。 | [paper](./lonn97-tdma-startup-mechanism/) |
| ⏱️ | 🎵 | 1998 | `bowman98` | Automatic Verification of a Lip Synchronisation Algorithm Using UPPAAL | lip sync, multimedia, `QoS` | lip synchronization 算法 | 音视频双流同步、jitter/skew、watchdog | 音频 `30 ms`/包、视频 `40 ms`/帧；non-anchored jitter 下约 `1031 ms` | `UPPAAL` | 同步边界、timelock 与 `QoS` 验证 | `QoS` 时序、timelock/deadlock | 🟢 | 自动分析 lip sync 算法，发现它会在部分场景下先 timelock 而非正常报错。 | [paper](./bowman98-lip-synchronisation-algorithm/) |
| 🎛️ | 🚦 | 1998 | `lindahl98` | Formal Design and Analysis of a Gear Controller | 换挡控制, 车辆控制, 有界响应 | 车辆 prototype gear controller | 控制 clutch/engine/gearbox，安全关键 | `46` 条公式；完整换挡 `<=1.5 s`；验证约 `2.99 s` | `UPPAAL` | 控制器设计验证与响应时间检查 | 安全、有界响应 | 🟢 | 在工业环境假设下验证换挡控制器，并把 bounded response 转成可达性分析。 | [paper](./lindahl98-gear-controller/) |
| 🎛️ | 🎵 | 1999 | `havelund99` | Formal Verification of a Power Controller Using the Real-Time Model Checker UPPAAL | 电源控制, 中断处理, 音视频组件 | 音视频组件 power controller | 多任务优先级、中断无丢失、上下电 | `15` 条性质；发现并修正 `3` 个设计错误 | `UPPAAL` | 电源控制逻辑与中断安全验证 | 安全、有界响应、时序约束 | 🟢 | 验证多任务电源控制器，修正设计错误并发现中断频率上界需求。 | [paper](./havelund99-power-controller/) |
| 🛰️ | 🏭 | 2000 | `david00` | Modelling and Analysis of a Commercial Field Bus Protocol | field bus, `AF100`, 工业调试 | ABB `AF100` bus coupler / data link layer | 商业 field bus、超时/重传/信号量 | 面向 `80` 站；数百页规格 + 数千行源码；`82/35` 条性质 | `UPPAAL` | 大型工业协议错误定位 | 安全、同步正确性、时序约束 | 🟢 | 通过抽象模型快速定位 AF100 工业协议中的同步与超时错误源。 | [paper](./david00-commercial-field-bus-protocol/) |
| ⏱️ | 🎵 | 2003 | `bordbar03` | Verification of Timeliness QoS Properties in Multimedia Systems | `QoS`, throughput, latency | distributed multimedia video player 示例 | ODP/QoS 契约、QTA/test automata | video player 示例；原文未给统一 benchmark 规模 | `UPPAAL` | Timeliness `QoS` 属性构造与验证 | throughput、jitter、latency | 🟡 | 通过 QTA 把多媒体 `QoS` 属性规约为 `UPPAAL` 可达性问题。 | [paper](./bordbar03-timeliness-qos-multimedia/) |
| 🎛️ | 🏭 | 2010 | `belmokadem10` | Verification of a Timed Multitask System with Uppaal | PLC, 多任务控制, 反应时间 | Bosch MSS station 2 多任务 PLC 控制程序 | PLC 周期扫描、事件中断、TON 定时块、机械环境联动 | 全局模型约 `30 x 10^6` 状态；比较单任务与多任务两种方案 | `UPPAAL` | 工业控制反应时间与 observer 度量验证 | 可达性、有界响应、时序约束 | 🟢 | 用 observer 自动机验证多任务 PLC 站点的停机反应时间，并证明 `<10` 但不满足 `<=5`。 | [paper](./belmokadem10-timed-multitask-system/) |
| ⏱️ | 🚀 | 2010 | `mikucionis10` | Schedulability Analysis Using Uppaal: Herschel-Planck Case Study | 可调度性, 卫星软件, 资源竞争 | Herschel-Planck 卫星单处理器控制软件任务集 | 固定优先级抢占、资源共享、任务挂起、工业航天软件 | `32` 个任务、`6` 类共享资源、`4` 个运行实例 | `UPPAAL` | 任务可调度性、WCRT 与 CPU 利用率分析 | 安全、有界响应、调度性质 | 🟢 | 证明卫星任务集可调度，并给出比传统 RTA 更紧的关键任务响应时间上界。 | [paper](./mikucionis10-herschel-planck-case-study/) |
| 🛰️ | 🌐 | 2010 | `ravn10` | A Formal Analysis of the Web Services Atomic Transaction Protocol with UPPAAL | web services, distributed transaction, consistency | `WS-AT` 分布式事务协议 | coordinator + participants、2PC/3-phase、TLA+ 对照 | 可验证至 `5` 个参与者 | `UPPAAL` | 协议一致性与工具对照验证 | 安全、一致性、可达性 | 🟡 | 把 WS-AT 从 TLA+ 转写为 `UPPAAL` 模型，并比较两类工具链的性能与扩展性。 | [paper](./ravn10-web-services-atomic-transaction/) |
| ⏱️ | 🏭 | 2010 | `xing10` | UPPAAL in Practice: Quantitative Verification of a RapidIO Network | RapidIO, 工业网络, 最坏时延 | 基于 RapidIO 的多处理器运动控制平台互连网络 | 周期控制流量、交换网络、最坏包时延、与 POOSL 对照 | `5` 个 blade、`10` 个交换机、`40` 个端点；全系统约 `2500` 个活动 | `UPPAAL` | 工业互连网络最坏时延分析 | 定量时序、最坏情况分析 | 🟢 | 把 RapidIO 工业性能模型转为 `UPPAAL`，用启发式分析高负载场景下的最坏时延。 | [paper](./xing10-rapidio-network/) |
| 🎛️ | 🏥 | 2011 | `lee11` | Modeling and Analysis of Radiation Therapy System with Respiratory Compensation Using Uppaal | 放疗控制, 呼吸补偿, 医疗设备 | 带呼吸补偿的放疗定位/跟踪控制系统 | HexaPOD、相机、控制器、缓冲区、医疗安全关键 | 至少 `4` 个核心组件；HexaPOD 具备 `6` 自由度 | `UPPAAL` | 控制器完成性、目标位姿可达性与死锁检查 | 可达性、死锁安全、控制完成性 | 🟡 | 用简化离散模型验证放疗控制链条无基本逻辑错误，但连续运动细节仍未纳入。 | [paper](./lee11-radiation-therapy-system/) |
| 🛰️ | 🌐 | 2011 | `ravn11` | Modelling and Verification of Web Services Business Activity Protocol | `WS-BA`, 长事务, 通信介质语义 | `WS-Business Activity` 中的 `BAwCC` 协议 | coordinator/participant、消息乱序/丢失/重复、协议修补 | `1` 个 coordinator + `1` 个 participant；模型含 `600+` 行 C 代码 | `UPPAAL` | 协议安全性、终止性与介质敏感性验证 | 安全、终止性、一致性 | 🟢 | 证明原 `BAwCC` 除完美 FIFO 外都会出错，并验证增强协议可在弱化介质下恢复正确性。 | [paper](./ravn11-web-services-business-activity/) |
| ⏱️ | 🚀 | 2012 | `david12` | Schedulability of Herschel-Planck Revisited Using Statistical Model Checking | `UPPAAL SMC`, 可调度性, 执行时间区间 | Herschel-Planck 卫星单处理器控制软件任务集（带执行时间区间） | 不确定 `BCET/WCET`、停表、符号 MC + SMC 组合 | 沿用 `32` 任务单 CPU 模型，并把执行时间推广为区间 | `UPPAAL SMC` | 可调度边界、deadline miss 反例与概率评估 | 安全、统计性质、调度性质 | 🟢 | 用符号 MC 和 `UPPAAL SMC` 共同分析带执行时间区间的卫星任务集可调度边界。 | [paper](./david12-herschel-planck-smc/) |
| 🛰️ | 🌐 | 2012 | `fehnker12` | Automated Analysis of AODV Using UPPAAL | AODV, 无线 mesh, 路由发现 | 无线 mesh / MANET 中的 AODV 路由协议 | 按需建路、动态拓扑、反例驱动协议修补 | 穷举 `<=5` 节点；`444` 静态拓扑、`1978` 加链路对、`1978` 删链路对 | `UPPAAL` | 路由发现、最优路与修补收益验证 | 安全、可达性、协议正确性 | 🟢 | 穷举小规模拓扑定位 AODV 缺陷，并量化三类修补对最优路保证的提升。 | [paper](./fehnker12-aodv-uppaal/) |
| 🎛️ | 🚦 | 2013 | `gruhn13` | Design and Verification of a Health-Monitoring Driver Assistance System | 驾驶辅助, 健康监测, 服务化网络 | 面向心脏病高风险驾驶员的健康监测驾驶辅助系统 | 多源传感、动态入网/离网、应急制动、分层验证 | ECG、呼吸带、相机、控制器、紧急制动系统、便携脉搏计等 `8` 类部件 | `UPPAAL` | 控制器时间/功能验证与动态网络分层验证 | 时序约束、功能正确性、通信可达性 | 🟡 | 提出医疗驾驶辅助系统的分层验证框架，其中控制器部分由 `UPPAAL` 承担。 | [paper](./gruhn13-health-monitoring-driver-assistance/) |
| 🎛️ | 🏥 | 2019 | `alur19` | Continuous-Time Models for System Design and Analysis | pacemaker, hybrid automata, 医疗 `CPS` | 双腔植入式心脏起搏器及其心脏环境模型 | `DDD/VDI` 模式、离散控制器 + 连续心脏、抽象证明 | `8` 个 pacemaker 过程 + `5` 个心脏抽象部件；基础 `DDD` 与 `DDD-VDI` 两种配置 | `UPPAAL` | 上/下速率限制与心跳传播要求验证 | 安全、时序约束、监视器性质 | 🟢 | 先用 `SpaceEx` 证明心脏抽象，再在 `UPPAAL` 中验证 pacemaker 的上下速率限制。 | [paper](./alur19-pacemaker-continuous-time/) |
| 📊 | 🏭 | 2019 | `martinelli19` | Timed Automata Networks for SCADA Attacks Real-Time Mitigation | SCADA, 攻击检测, 燃气管网 | SCADA 燃气管网日志驱动的攻击检测模型 | 日志转自动机、双特征同步、`DoS/MI` 攻击公式 | `269,228` 条测量；`100 ms` 窗口生成 `2,692` 个模型；`1346` 正常 + `1346` 攻击 | `UPPAAL` | 攻击模式可达性判定与检测评估 | 可达性、时序模式、工业安全 | 🟢 | 把 SCADA 日志转成 timed automata 网络，并用 `UPPAAL` 公式检测 `DoS` 与恶意注入攻击。 | [paper](./martinelli19-scada-attack-mitigation/) |
| 🎛️ | 🚦 | 2020 | `basile20` | Strategy Synthesis for Autonomous Driving in a Moving Block Railway System with Uppaal Stratego | railway, moving block, autonomous driving, strategy synthesis | ERTMS Level 3 moving block 信号与自主驾驶抽象系统 | 单列车/单 `RBC`、随机通信延迟、`MA` 安全边界 | `1` train + `1` `RBC` + `1` `OBU` + `1` `LU`；默认 `ma=5`、`arrive=20` | `UPPAAL Stratego` | 安全驾驶策略合成与到达时间优化 | 安全、可达性、统计性质、定量优化 | 🟢 | 用 `Stratego` 合成永不越 `MA` 的驾驶策略，并在安全前提下优化到达时间。 | [paper](./basile20-moving-block-railway-driving/) |
| 🛰️ | 🌐 | 2020 | `bernardeschi20` | Analysis of Security Attacks in Wireless Sensor Networks: From UPPAAL to Castalia | WSN, flooding, drop/tamper, Castalia | 无线传感器网络应用层 flooding 协议 | 源节点 + 中继节点、链路冗余、单次攻击注入 | `1` source + `4` relay；攻击在随机时刻执行 `1` 次 | `UPPAAL` | 协议正确转发与攻击影响分析 | 安全、可达性、攻击场景正确性 | 🟡 | 先在 `UPPAAL` 证明 flooding 性质，再自动转到 Castalia 分析 drop/tamper 攻击后果。 | [paper](./bernardeschi20-wsn-security-castalia/) |
| 📊 | 🦠 | 2020 | `jensen20` | Fluid Model-Checking in UPPAAL for Covid-19 | Covid-19, SEIHR, fluid model checking, contact tracing | 丹麦 `Covid-19` SEIHR 疫情与场景模型 | 多抽象层级、隔离阶段/家庭作息/超级传播/追踪 app | `10,000` 人基础模型；`30+9,970` fluid；哥本哈根+`5` 场所+`3` 成员；`1,000` 人 tracing | `UPPAAL SMC` | 住院容量、暴露概率、超级传播与追踪策略评估 | 统计性质、概率估计、容量界 | 🟢 | 用 `UPPAAL SMC` 在群体和个体双层场景中分析疫情传播、暴露风险与接触追踪效果。 | [paper](./jensen20-covid19-fluid-model-checking/) |
| ⏱️ | 🔋 | 2021 | `gamatie21` | Modeling and Analysis for Energy-Driven Computing using Statistical Model-Checking | energy harvesting, energy-neutrality, batteries, distributed systems | 带采能与能量迁移的分布式实时计算系统 | 任务/资源/太阳能板/电池/控制器联动，支持节点间能量共享 | `11` 个任务、`5` 个基础节点，扩展到 `6/8` 节点；`2` 天 Girona 场景 | `UPPAAL SMC` | deadline/energy-neutrality 验证与电池 sizing | 统计性质、deadline 安全、资源定量 | 🟢 | 用 `UPPAAL SMC` 评估最小电池容量，并说明能量共享可显著降低总储能需求。 | [paper](./gamatie21-energy-driven-computing/) |
| 🛰️ | 🏭 | 2021 | `guo21` | A Formal Method for Evaluating the Performance of TSN Traffic Shapers using UPPAAL | TSN, TAS, preemption, latency | `TSN` 交换节点中的流量整形器 | `ST/BE` 双类流量、window automata、抢占机制对比 | `100 Mbps`；`ST 128B/200μs`、`BE 256B/125μs`；`TAS` 周期 `500μs` | `UPPAAL` | shaping 规则与低时延性质验证 | 安全、活性、时延、可达性 | 🟢 | 证明不带抢占的 `TAS/PS` 难以满足低时延要求，而抢占能同时改善时延和利用率。 | [paper](./guo21-tsn-traffic-shapers/) |
| 🧩 | 🌐 | 2021 | `kunnappilly21` | From UML Modeling to UPPAAL Model Checking of 5G Dynamic Service Orchestration | 5G slicing, UML, service orchestration, VNF | `5G` 动态服务编排与 network slicing 场景 | 共享 `VNF`、动态请求、`UML` 到 `UPPAAL` 的自动翻译 | `3` 个 health `UE` + `2` 个 video `UE`；`4` hosts；health `v1-v2`、video `v1-v3-v4-v5` | `UPPAAL` | SLA/时延与最终服务性验证 | 可达性、leads-to、不变式 | 🟡 | 把 `UML` 状态图翻译成 `UPPAAL` 模型，验证关键切片请求的时限与最终服务性。 | [paper](./kunnappilly21-5g-service-orchestration/) |
| 🎛️ | 🚦 | 2021 | `thamilselvam21` | Scalable Coordinated Intelligent Traffic Light Controller for Heterogeneous Traffic Scenarios Using UPPAAL Stratego | traffic lights, hierarchical control, Stratego, heterogeneous traffic | Ahmedabad `23` 路口交通灯协调系统 | `ILTAN + ALTAN` 双层控制、`4` 类车辆、`SUMO` 在线闭环 | `23` 个交叉口、`4` 相位、`1200s` 仿真、`4` 类车辆 | `UPPAAL Stratego` | 相位控制综合与延迟/排放评估 | 定量优化、吞吐、排放、延迟 | 🟢 | 在城市级路网中合成双层交通灯策略，显著降低等待时间与排放。 | [paper](./thamilselvam21-traffic-light-controller/) |
| 🎛️ | 🏥 | 2022 | `lehmann22` | Modeling R^3 Needle Steering in Uppaal | needle steering, medical CPS, obstacle avoidance, online strategy synthesis | 软组织中的 steerable needle 在线导航系统 | `TR/CR/DR` 区域建模、在线重综合、`R^3 -> Z^3` 抽象 | `5` 类环境；虚拟针 `50` 次/设置、真实针 `5-7` 次/设置；`120s` 超时 | `UPPAAL Stratego` | 安全到靶与在线重规划验证 | 安全、可达性、性能 | 🟢 | 用 `Stratego` 进行针导航在线策略综合，在真实针实验中保持 `0%` 关键区命中。 | [paper](./lehmann22-r3-needle-steering/) |
| 🎛️ | 🏥 | 2023 | `cuartas23` | Formal Verification of a Mechanical Ventilator using UPPAAL | ventilator, medical device, valve control, flow | 机械呼吸机控制架构 | `Setup/Control/Injector/ExpValve` 四自动机、简化流体模型、符号 + `SMC` 混合验证 | `4` 个 automata；流量 `10-50 L/min`；`FiO2 10-100%`；时序 `100-300 cs` | `UPPAAL` | 阀门协调、时序与流量行为验证 | 安全、可达性、统计性质、定量分析 | 🟢 | 验证呼吸机控制与阀门互锁逻辑，并用模型分析更优采样周期。 | [paper](./cuartas23-mechanical-ventilator/) |
| 🧩 | 🎓 | 2024 | `zhou24` | Ensuring Reliability in Electronic Examinations Through UPPAAL-Based Trustworthy Design | electronic examination, workflow, cheating detection, trustworthy design | 电子考试流程系统 | 四角色协作、操作队列、答案相似度防作弊 | 示例为 `2` 名考生、`3` 道题、`12` 条性质；`MaxT=1000` | `UPPAAL` | 流程可靠性与规则一致性验证 | 安全、完整性、活性、防作弊 | 🟡 | 用 `UPPAAL` 模型检查电子考试中的注册、提交、阅卷、通知与作弊检测规则。 | [paper](./zhou24-electronic-examinations/) |

## 案例/模型/数据公开性清单

| 论文 | 状态 | 案例/模型/数据 | 来源类型 | 制作/来源方式 | 可获取性 | 获取方式/链接 | 简述 |
|---|---|---|---|---|---|---|---|
| [bengtsson96](./bengtsson96-audio-protocol-bus-collision/desc.md) | 🟢 | Philips 音频协议 timed automata 案例 | 工业协议案例（历史 benchmark 入口） | 论文正文 + 官方 benchmark 历史条目 `philaudio` | 🟠 | [DOI](https://doi.org/10.1007/3-540-61474-5_73)；[UPPAAL Benchmarks](https://uppaal.org/benchmarks/) | benchmark 页仍可见案例名，但当前公开直链已失效 |
| [dargenio97](./dargenio97-bounded-retransmission-time/desc.md) | 🟢 | BRP 协议模型 | 协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1007/BFb0035403) | 原文未提供独立模型包或仓库 |
| [lonn97](./lonn97-tdma-startup-mechanism/desc.md) | 🟢 | DACAPO 启动同步模型 | 协议案例 | 论文正文重建 | 🟠 | [论文 PDF](https://uppaal.org/texts/lp-prfts97.pdf) | 论文可得，但无独立模型入口 |
| [havelund97](./havelund97-audio-video-protocol/desc.md) | 🟢 | B&O 音视频协议工业案例 | 工业实现案例 | 工业实现 + 论文描述 + 官网案例页 | 🔒 | [DOI](https://doi.org/10.1109/REAL.1997.641264)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 真实资产来自工业实现，论文未公开完整模型与原始协议资产 |
| [bowman98](./bowman98-lip-synchronisation-algorithm/desc.md) | 🟢 | lip sync 算法模型 | 学术算法案例 | 论文正文重建 | 🟠 | [论文 PDF](https://uppaal.org/texts/bfklm-fimcs98.pdf) | 无独立模型/输入流数据包 |
| [lindahl98](./lindahl98-gear-controller/desc.md) | 🟢 | gear controller 与环境模型 | 工业控制案例 | 工业合作需求 + 论文描述 | 🔒 | [DOI](https://doi.org/10.1007/BFb0054178) | 控制器需求与环境资产来自工业项目，难以直接公开取得 |
| [havelund99](./havelund99-power-controller/desc.md) | 🟢 | power controller 历史模型 `bopdp` / `bopdpFIXED` | 工业控制案例（历史 benchmark 入口） | 论文正文 + 官方 benchmark 历史条目 | 🟠 | [DOI](https://doi.org/10.7146/BRICS.V6I8.20065)；[UPPAAL Benchmarks](https://uppaal.org/benchmarks/) | benchmark 页仍记有模型名，但当前公开直链已失效 |
| [david00](./david00-commercial-field-bus-protocol/desc.md) | 🟢 | AF100 bus coupler 案例 | 工业协议案例 | ABB 工业规格/实现 + 论文抽象 | 🔒 | [DOI](https://doi.org/10.1109/EMRTS.2000.854004) | 案例依赖商业协议规格与实现资产，原文未公开模型包 |
| [bordbar03](./bordbar03-timeliness-qos-multimedia/desc.md) | 🟡 | video player + QTA 示例 | 方法示例案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1007/978-3-540-39893-6_30) | 方法公开，但无独立 QTA 工具实现或示例模型包 |
| [ravn10](./ravn10-web-services-atomic-transaction/desc.md) | 🟡 | WS-AT `UPPAAL` 模型（历史 `rvs10.zip`） | 软件协议案例（历史 case-study 入口） | 论文正文 + 官网案例页历史链接 | 🟠 | [DOI](https://doi.org/10.1007/978-3-642-16558-0_47)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 官网仍提历史压缩包，但当前公开链接返回 `404` |
| [xing10](./xing10-rapidio-network/desc.md) | 🟢 | RapidIO 工业网络性能模型 | 工业嵌入式通信案例 | POOSL 性能模型 + 论文描述 | 🟠 | [UTwente PDF](https://ris.utwente.nl/ws/portalfiles/portal/5301883/uppaal_in_practice_ISOLA2010.pdf) | 论文公开，但未提供独立 `UPPAAL` 模型包或流量工件 |
| [mikucionis10](./mikucionis10-herschel-planck-case-study/desc.md) | 🟢 | Herschel-Planck 调度模型 | 航天调度案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [模型目录](https://github.com/DEIS-Tools/uppaal-models/tree/main/CaseStudies/HerschelPlanck2010)；[HerschelEvents2.xml](https://raw.githubusercontent.com/DEIS-Tools/uppaal-models/main/CaseStudies/HerschelPlanck2010/HerschelEvents2.xml) | 当前可直接获取论文、模型和查询 |
| [belmokadem10](./belmokadem10-timed-multitask-system/desc.md) | 🟢 | Bosch MSS station 2 PLC 案例 | 工业 PLC 案例 | 论文正文 + HAL 版本 | 🟠 | [HAL 页面](https://hal.science/hal-00527736) | 论文可获取，但站点模型、PLC 源程序和 `UPPAAL` 工程未公开 |
| [ravn11](./ravn11-web-services-business-activity/desc.md) | 🟢 | `BAwCC` 协议模型（历史 `rsv-tacas11.zip`） | 软件协议案例（历史 case-study 入口） | 论文正文 + 官网历史链接 | 🟠 | [论文 PDF](https://uppaal.org/texts/rsv-tacas11.pdf)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 论文可得，但历史模型压缩包当前返回 `404` |
| [lee11](./lee11-radiation-therapy-system/desc.md) | 🟡 | 放疗补偿控制系统模型 | 医疗控制案例 | 论文结构描述重建 | 🟠 | [论文 PDF](http://www.kevin-lee.co.uk/work/research/KLMKrilaviciusEtAl_ISPA2011.pdf) | 仅论文公开，无独立模型或数据包 |
| [david12](./david12-herschel-planck-smc/desc.md) | 🟢 | Herschel-Planck `SMC` 调度模型 | 航天调度案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [Herschel-SMC2.xml](https://github.com/DEIS-Tools/uppaal-models/blob/main/CaseStudies/HerschelPlanck2012/Herschel-SMC2.xml) | 当前可直接拿到 `UPPAAL SMC` 案例模型 |
| [fehnker12](./fehnker12-aodv-uppaal/desc.md) | 🟢 | AODV `UPPAAL` 协议模型 | 协议案例 | RFC + AWN 形式化规范 + 论文描述 | 🟠 | [DOI](https://doi.org/10.1007/978-3-642-28756-5_13) | 论文公开，但稳定模型下载入口未确认，历史 AWN 报告入口当前不可达 |
| [gruhn13](./gruhn13-health-monitoring-driver-assistance/desc.md) | 🟡 | 健康监测驾驶辅助系统验证框架 | 医疗车载 `CPS` 案例 | 论文框架描述 | 🟠 | [DOI](https://doi.org/10.4108/icst.pervasivehealth.2013.252091) | 无公开 `UPPAAL` 模型、`π`-演算规范或案例数据 |
| [alur19](./alur19-pacemaker-continuous-time/desc.md) | 🟢 | pacemaker `UPPAAL` 模型 | 医疗设备案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [pacemaker.xml](https://github.com/DEIS-Tools/uppaal-models/blob/main/CaseStudies/Pacemaker2019/pacemaker.xml) | 当前可直接获取模型文件，适合复跑与二次分析 |
| [martinelli19](./martinelli19-scada-attack-mitigation/desc.md) | 🟢 | SCADA 燃气管网日志数据集 + 攻击公式 | 工业安全数据案例 | UAH ICS 公开数据集 + 论文公式构造 | 🟢 | [数据集页面](https://sites.google.com/a/uah.edu/tommy-morris-uah/ics-data-sets)；[Raw Data Gas Pipeline](http://www.ece.uah.edu/~thm0009/icsdatasets/gas_final.arff)；[数据缺陷报告](http://www.ece.uah.edu/~thm0009/icsdatasets/MSU_SCADA_Final_Report.pdf) | 数据可直接获取，但源页已明确说明该批数据存在已知缺陷 |
| [basile20](./basile20-moving-block-railway-driving/desc.md) | 🟢 | moving block 铁路 `Stratego` 模型与实验 | 铁路控制案例（作者仓库） | 论文 + 作者 `GitHub` 仓库 | 🟢 | [FORTE2020 仓库](https://github.com/davidebasile/FORTE2020) | 当前可直接获取模型与实验脚本，是较少见的公开 `Stratego` 铁路案例 |
| [bernardeschi20](./bernardeschi20-wsn-security-castalia/desc.md) | 🟡 | WSN flooding 协议模型与 `UPPAAL->Castalia` 原型 | 协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.5220/0009380508150824)；[论文 PDF](https://www.scitepress.org/Papers/2020/93805/93805.pdf) | 论文公开，但无稳定模型仓库或桥接脚本下载入口 |
| [jensen20](./jensen20-covid19-fluid-model-checking/desc.md) | 🟢 | `Covid-19` 流体/随机/追踪模型 | 公共健康场景（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [Covid-19 模型目录](https://github.com/DEIS-Tools/uppaal-models/tree/main/CaseStudies/Covid-19) | 当前可直接获取疫情场景模型，是少数公开的 `UPPAAL SMC` 公共健康案例 |
| [gamatie21](./gamatie21-energy-driven-computing/desc.md) | 🟢 | energy-driven computing 模型模板 | 采能计算案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [EnergyNeutrality 目录](https://github.com/DEIS-Tools/uppaal-models/tree/main/CaseStudies/EnergyNeutrality) | 可直接获取能量中和案例模型，适合复跑电池 sizing 流程 |
| [guo21](./guo21-tsn-traffic-shapers/desc.md) | 🟢 | `TSN` shaper 形式模型 | 协议/网络案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1109/LCN52139.2021.9524955)；[论文 PDF](https://zhehou.github.io/papers/A-Formal-Method-for-Evaluating-the-Performance-of-TSN-Traffic-Shapers-using-UPPAAL.pdf) | 论文与参数公开，但未提供独立模型工件 |
| [kunnappilly21](./kunnappilly21-5g-service-orchestration/desc.md) | 🟡 | `5G-SO` `UML`/`UPPAAL` 模式与 `G5` 工作流 | 架构建模案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1145/3459960.3459965)；[论文 PDF](https://www.es.mdu.se/pdf_publications/6189.pdf) | 自动验证思路公开，但未确认稳定仓库或工具下载入口 |
| [thamilselvam21](./thamilselvam21-traffic-light-controller/desc.md) | 🟢 | `SUMO + Stratego` 交通灯协同控制源码 | 城市交通案例（作者仓库） | 论文 + 作者 `GitHub` 仓库 | 🟢 | [GitHub 仓库](https://github.com/ThamilselvamB/Intelligent-Traffic-Light-Controller-using-Uppaal-Stratego) | 可直接获取城市交通灯控制代码与仿真脚本 |
| [lehmann22](./lehmann22-r3-needle-steering/desc.md) | 🟢 | 三维针导航 `Uppaal` 模型细节 | 医疗导航案例 | 论文附录与正文重建 | 🟠 | [DOI](https://doi.org/10.4204/EPTCS.355.4)；[arXiv PDF](https://arxiv.org/pdf/2203.09884) | 正文和附录给出大量模型细节，但未提供独立仓库 |
| [cuartas23](./cuartas23-mechanical-ventilator/desc.md) | 🟢 | 呼吸机 `ventilator.xml` 与 `SCADE` 模型 | 医疗设备案例（作者仓库） | 论文 + `ventynet` 仓库 | 🟢 | [ventilator.xml](https://github.com/ventynet/ventynet/blob/master/ventilator.xml)；[ventynet-SCADE](https://github.com/ventynet/ventynet-SCADE) | 当前可直接获取 `UPPAAL` 模型文件与相关原型材料 |
| [zhou24](./zhou24-electronic-examinations/desc.md) | 🟡 | 电子考试 `UPPAAL` 模型 | 业务流程案例（GitHub + Zenodo） | 论文 + 作者仓库 + 归档 | 🟢 | [GitHub 仓库](https://github.com/TURTING-BO/An-Electronic-Examination-Model-Based-on-UPPAAL)；[Zenodo](https://doi.org/10.5281/zenodo.12787513) | 模型可直接获取，是当前文库里公开度最高的业务流程类案例之一 |

## 初步归类与当前观察

1. 文库扩展到 `2024` 后，`UPPAAL` 应用主线已从早期协议/控制器进一步延伸到疫情策略评估、`5G` 服务编排、`TSN`、城市交通灯、针导航、呼吸机和电子考试流程。
2. `2020` 年后的代表性案例里，`UPPAAL Stratego` 与 `UPPAAL SMC` 的占比明显提高，说明“策略综合/统计分析 + 具体应用对象”的组合已成为新主线。
3. 新批次里真正可直接获取的工件明显增多，主要来自作者 `GitHub/Zenodo` 与官方 `uppaal-models` 仓库，而非历史 benchmark 页面。
4. 现有条目已经证明，单列 `领域` 会把“验证对象类型”和“现实应用场景”混在一起；改成 `主轴分类 + 次轴场景` 后，像工业协议、医疗车载系统和业务流程规则这类交叉案例的边界更稳定。
5. 新条目再次证明必须明确写清“验证的是哪一层”：例如有的论文验证控制策略，有的只验证协议层，有的只验证日志模式或业务流程规则。
6. 医疗设备/交通控制/资源系统仍然最贴近博士研究主线，但业务流程与公共健康案例也提供了“多角色规则如何转成状态机性质”的额外启发。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化 `open_explore/uppaal_apps/`，建立 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 三个核心文件 | 先把应用文库与 `uppaal_tech/` 拆开，固定边界与总账骨架 | 先解决结构拆分，后续再正式扩充应用条目 |
| 2026-03-31 | 重写 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)，并新增 [DESC_GUIDE.md](./DESC_GUIDE.md) | 将文库主线收紧到“使用 `UPPAAL` 对具体对象进行形式化验证”的应用论文，补齐大规模扩库所需的字段、状态和单篇规范 | 为后续批量抓取控制系统、嵌入式系统、工业 `CPS` 与协议验证文献做准备 |
| 2026-03-31 | 将分类口径从单列 `领域` 重构为 `主轴分类 + 次轴场景`，并把统一总表前两列改为纯 emoji | 用“验证对象类型”和“现实应用场景”拆分原有混合口径，同时同步回写 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 与 [DESC_GUIDE.md](./DESC_GUIDE.md) | 为后续稳定维护跨行业、跨对象类型的应用案例统计做准备 |
| 2026-03-31 | 首批纳入 `10` 篇 `2010` 年及以前的 `UPPAAL` 应用论文，补齐每篇的 `paper.pdf + paper_content.txt + bibtex.bib` | 基于官网 `Case Studies` 与 `Documentation` 反向筛查 `20+` 个候选，优先选择 PDF 可稳定获取且验证主线清晰的协议、控制器、工业和软件案例 | 建立 `1996-2010` 的早期应用主线骨架 |
| 2026-03-31 | 为首批 `10` 篇论文全部补齐 `desc.md`，并把总账字段改为“被验证系统 / 系统特点 / 系统规模 + 公开性清单” | 取消 `详度/实现` 两列，改为维护单篇 `desc.md`、统一论文表和“案例/模型/数据公开性清单”；同时把“默认必须写 `desc.md`”落进 [README.md](./README.md) 与 [GUIDE.md](./GUIDE.md) | 让 `uppaal_apps/` 的维护方式对齐 `baselines` 的公开性思路，并固定今后入账口径 |
| 2026-03-31 | 新增 `10` 篇 `2010-2019` 应用论文，覆盖 RapidIO、卫星调度、工业 PLC、`WS-BA`、医疗设备、AODV、SCADA 安全等方向，并全部补齐 `desc.md` | 继续按“系统边界明确 + 性质清晰 + 规模可描述 + 公开性可追溯”的口径扩库，同时核验可公开模型/数据链接是否当前可访问 | 把文库上界从 `2010` 推进到 `2019`，并补上少量当前可直接获取的模型/数据案例 |
| 2026-03-31 | 新增 `10` 篇 `2020-2024` 应用论文，覆盖疫情流体模型、moving block 铁路、WSN 安全、能量驱动计算、`5G` 切片、`TSN`、城市交通灯、针导航、机械呼吸机与电子考试，并全部补齐 `desc.md` | 优先选择系统边界、性质簇、规模与公开性都能写清的后 `2020` 案例，同时补核 `GitHub/Zenodo` 或官方模型仓库链接 | 把文库时间上界推进到 `2024`，并建立 `Stratego/SMC` 后期应用主线 |

## 失败与阻塞记录

| 时间 | 候选条目/对象 | 问题 | 当前处理 |
|---|---|---|---|
| 2026-03-31 | Model-Checking Real-Time Control Programs | 官网旧链接 `https://homes.cs.aau.dk/~paupet/papers/ikllmmpt-ecrts00.pdf` 与对应 `.bib.txt` 返回 `404`，无法稳定取得三件套 | 本轮未正式入账；已以 [bordbar03-timeliness-qos-multimedia/](./bordbar03-timeliness-qos-multimedia/) 补足名额，超过 `5` 天后若找到可用公开版本再重试 |
| 2026-03-31 | `philaudio.ta` / `bopdp.xml` / `rvs10.zip` / `rsv-tacas11.zip` 等历史工件链接 | 官网 benchmark/case-study 页仍提到历史模型入口，但当前公开直链已失效或返回 `404` | 在公开性清单中统一按 `🟠 信息不清` 处理，不误记为“模型可直接获取” |
