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
- `2010` 年后，安全关键嵌入式/医疗/工业安全方向的命中率明显提高
- 官方模型仓库、历史 case-study 页和公开数据集页仍是高价值反向入口

### 已观察到的低命中特征

- 教程、综述或方法展示文，没有稳定具体系统边界
- 只讲 optimization/testing/scheduling，却没有清晰验证问题和查询
- 只搜泛 timed automata 或泛 industry 词，没有具名系统名或性质词
- 历史案例页常能找到论文，但很多旧工件链接已经失效

### 检索倾向调整

- 当前高价值方向已扩展到：航天调度、医疗设备、工业 PLC、无线路由、SCADA 安全与服务事务协议
- 只要用户没有明确豁免，正式入账时仍默认同步补齐 `desc.md`
- 公开性继续单独维护为“案例/模型/数据公开性清单”，不再回退到 `详度/实现`
- 对 `2010-2020` 条目，优先选择能把“系统是什么、验证哪一层、规模多大、材料能否拿到”讲清楚的论文

## 当前收录统计

| 统计项 | 数值 | 年份信息 |
|---|---:|---|
| 已收录顶层条目 | 20 | 覆盖 `1996-2019` |
| 本轮新增条目 | 10 | 本轮新增均位于 `2010-2019` |
| 其中已补 `desc.md` | 20 | `1996-2019` 均已完成整理 |
| 当前 `🟢 直接可用` | 16 | 主体已扩展到协议、控制器、医疗与工业安全案例 |
| 当前 `🟡 可整理` | 4 | 主要是材料较薄或更偏框架展示的案例 |
| 当前 `⏳ 尚未提取` | 0 | 无 |
| 公开性分布 | `🟢 4 / 🟠 13 / 🔒 3` | 公开模型/数据仍然稀缺，但已出现可直接获取案例 |
| 最早年份 | 1996 | 首批收录始于经典协议冲突案例 |
| 最晚年份 | 2019 | 已扩展到 pacemaker 与 SCADA 安全案例 |
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

## 应用分类口径

| 一级领域 | 说明 | 当前正式条目数 |
|---|---|---:|
| 🛰️ 协议与通信系统 | 网络协议、通信协议、分布式交互等 | 5 |
| 🎛️ 控制器与嵌入式系统 | 控制逻辑、嵌入式控制器、实时控制软件等 | 8 |
| 🏭 工业系统与 `CPS` | 制造、工业控制、混合系统、工程案例等 | 3 |
| 🚦 交通、调度与资源系统 | 交通控制、调度、实时资源系统等 | 0 |
| 🧩 软件、架构与组件系统 | 软件组件、并发软件、软件架构等 | 4 |

说明：

1. 上表是当前版本的领域骨架，不是封闭不变的固定枚举。
2. 若后续实际收录中出现新的稳定应用簇，或现有类别已经过宽，应按实际情况动态扩充、拆分或合并领域类型。
3. 一旦发生动态调整，必须同步更新本节统计口径以及统一论文总表中的 `领域` 字段。

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

`领域 | 年份 | Key | 标题 | 关键词 | 被验证系统 | 系统特点 | 系统规模 | UPPAAL线 | 验证任务 | 性质类型 | 状态 | 一句话简介 | 链接`

维护规则：

1. `年份` 为必填字段；虽然当前表格把 `领域` 放在第一列，但全表仍必须按年份从低到高排列，同年按 `Key` 字典序稳定排序。
2. `领域` 列只保留 emoji，不再附加文字解释。

| 领域 | 年份 | Key | 标题 | 关键词 | 被验证系统 | 系统特点 | 系统规模 | UPPAAL线 | 验证任务 | 性质类型 | 状态 | 一句话简介 | 链接 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 🛰️ | 1996 | `bengtsson96` | Verification of an Audio Protocol with Bus Collision Using UPPAAL | 音频协议, 总线冲突, 广播通信 | Philips 音频控制协议（双发送端冲突版本） | 单总线、广播/碰撞检测、工业背景 | `6` 个 automata；状态空间约为单发送端版的 `10^3` 倍 | `UPPAAL` | 协议碰撞处理与时序容错验证 | 安全、有界活性、时序容错 | 🟢 | 用 timed automata 验证双发送端冲突协议，并确定 `5%/6%` 容错边界。 | [paper](./bengtsson96-audio-protocol-bus-collision/) |
| 🛰️ | 1997 | `dargenio97` | The Bounded Retransmission Protocol Must Be on Time! | 文件传输, 有界重传, 超时 | BRP 有界重传文件传输协议 | 分块传输、丢包信道、超时/中止 | 发送端/接收端 + `T1/T2` 定时器；原文未给统一状态规模 | `UPPAAL` | 服务符合性与超时参数验证 | 安全、服务符合性、时序约束 | 🟢 | 通过 timed/untimed 对照说明 BRP 正确性依赖真实超时结构。 | [paper](./dargenio97-bounded-retransmission-time/) |
| 🛰️ | 1997 | `havelund97` | Formal Modelling and Analysis of an Audio/Video Protocol: An Industrial Case Study Using UPPAAL | 工业协议, 音视频总线, 碰撞检测 | Bang & Olufsen 音视频控制协议 | 单总线、`2800` 行汇编、工业真实协议 | `9` 个 automata；`5` 次主要迭代、约 `3` 个月；错误轨迹近 `2000` 步 | `UPPAAL` | 协议建模、错误定位与修复验证 | 安全、有界活性、一致性 | 🟢 | 通过自动诊断轨迹定位并修复 B&O 工业协议中的时序错误。 | [paper](./havelund97-audio-video-protocol/) |
| 🛰️ | 1997 | `lonn97` | Formal Verification of a TDMA Protocol Start-Up Mechanism | `TDMA`, 启动同步, 时钟漂移 | DACAPO `TDMA` 启动机制 | 多主站、启动同步、时钟漂移 | `4` 个站点 + 总线；时钟漂移 `±10^-3` | `UPPAAL` | 启动同步与截止时间验证 | 安全、有界响应、时序约束 | 🟢 | 证明四站 TDMA 系统能在漂移条件下于有界时间内完成同步。 | [paper](./lonn97-tdma-startup-mechanism/) |
| 🧩 | 1998 | `bowman98` | Automatic Verification of a Lip Synchronisation Algorithm Using UPPAAL | lip sync, multimedia, `QoS` | lip synchronization 算法 | 音视频双流同步、jitter/skew、watchdog | 音频 `30 ms`/包、视频 `40 ms`/帧；non-anchored jitter 下约 `1031 ms` | `UPPAAL` | 同步边界、timelock 与 `QoS` 验证 | `QoS` 时序、timelock/deadlock | 🟢 | 自动分析 lip sync 算法，发现它会在部分场景下先 timelock 而非正常报错。 | [paper](./bowman98-lip-synchronisation-algorithm/) |
| 🎛️ | 1998 | `lindahl98` | Formal Design and Analysis of a Gear Controller | 换挡控制, 车辆控制, 有界响应 | 车辆 prototype gear controller | 控制 clutch/engine/gearbox，安全关键 | `46` 条公式；完整换挡 `<=1.5 s`；验证约 `2.99 s` | `UPPAAL` | 控制器设计验证与响应时间检查 | 安全、有界响应 | 🟢 | 在工业环境假设下验证换挡控制器，并把 bounded response 转成可达性分析。 | [paper](./lindahl98-gear-controller/) |
| 🎛️ | 1999 | `havelund99` | Formal Verification of a Power Controller Using the Real-Time Model Checker UPPAAL | 电源控制, 中断处理, 音视频组件 | 音视频组件 power controller | 多任务优先级、中断无丢失、上下电 | `15` 条性质；发现并修正 `3` 个设计错误 | `UPPAAL` | 电源控制逻辑与中断安全验证 | 安全、有界响应、时序约束 | 🟢 | 验证多任务电源控制器，修正设计错误并发现中断频率上界需求。 | [paper](./havelund99-power-controller/) |
| 🏭 | 2000 | `david00` | Modelling and Analysis of a Commercial Field Bus Protocol | field bus, `AF100`, 工业调试 | ABB `AF100` bus coupler / data link layer | 商业 field bus、超时/重传/信号量 | 面向 `80` 站；数百页规格 + 数千行源码；`82/35` 条性质 | `UPPAAL` | 大型工业协议错误定位 | 安全、同步正确性、时序约束 | 🟢 | 通过抽象模型快速定位 AF100 工业协议中的同步与超时错误源。 | [paper](./david00-commercial-field-bus-protocol/) |
| 🧩 | 2003 | `bordbar03` | Verification of Timeliness QoS Properties in Multimedia Systems | `QoS`, throughput, latency | distributed multimedia video player 示例 | ODP/QoS 契约、QTA/test automata | video player 示例；原文未给统一 benchmark 规模 | `UPPAAL` | Timeliness `QoS` 属性构造与验证 | throughput、jitter、latency | 🟡 | 通过 QTA 把多媒体 `QoS` 属性规约为 `UPPAAL` 可达性问题。 | [paper](./bordbar03-timeliness-qos-multimedia/) |
| 🏭 | 2010 | `belmokadem10` | Verification of a Timed Multitask System with Uppaal | PLC, 多任务控制, 反应时间 | Bosch MSS station 2 多任务 PLC 控制程序 | PLC 周期扫描、事件中断、TON 定时块、机械环境联动 | 全局模型约 `30 x 10^6` 状态；比较单任务与多任务两种方案 | `UPPAAL` | 工业控制反应时间与 observer 度量验证 | 可达性、有界响应、时序约束 | 🟢 | 用 observer 自动机验证多任务 PLC 站点的停机反应时间，并证明 `<10` 但不满足 `<=5`。 | [paper](./belmokadem10-timed-multitask-system/) |
| 🎛️ | 2010 | `mikucionis10` | Schedulability Analysis Using Uppaal: Herschel-Planck Case Study | 可调度性, 卫星软件, 资源竞争 | Herschel-Planck 卫星单处理器控制软件任务集 | 固定优先级抢占、资源共享、任务挂起、工业航天软件 | `32` 个任务、`6` 类共享资源、`4` 个运行实例 | `UPPAAL` | 任务可调度性、WCRT 与 CPU 利用率分析 | 安全、有界响应、调度性质 | 🟢 | 证明卫星任务集可调度，并给出比传统 RTA 更紧的关键任务响应时间上界。 | [paper](./mikucionis10-herschel-planck-case-study/) |
| 🧩 | 2010 | `ravn10` | A Formal Analysis of the Web Services Atomic Transaction Protocol with UPPAAL | web services, distributed transaction, consistency | `WS-AT` 分布式事务协议 | coordinator + participants、2PC/3-phase、TLA+ 对照 | 可验证至 `5` 个参与者 | `UPPAAL` | 协议一致性与工具对照验证 | 安全、一致性、可达性 | 🟡 | 把 WS-AT 从 TLA+ 转写为 `UPPAAL` 模型，并比较两类工具链的性能与扩展性。 | [paper](./ravn10-web-services-atomic-transaction/) |
| 🎛️ | 2010 | `xing10` | UPPAAL in Practice: Quantitative Verification of a RapidIO Network | RapidIO, 工业网络, 最坏时延 | 基于 RapidIO 的多处理器运动控制平台互连网络 | 周期控制流量、交换网络、最坏包时延、与 POOSL 对照 | `5` 个 blade、`10` 个交换机、`40` 个端点；全系统约 `2500` 个活动 | `UPPAAL` | 工业互连网络最坏时延分析 | 定量时序、最坏情况分析 | 🟢 | 把 RapidIO 工业性能模型转为 `UPPAAL`，用启发式分析高负载场景下的最坏时延。 | [paper](./xing10-rapidio-network/) |
| 🎛️ | 2011 | `lee11` | Modeling and Analysis of Radiation Therapy System with Respiratory Compensation Using Uppaal | 放疗控制, 呼吸补偿, 医疗设备 | 带呼吸补偿的放疗定位/跟踪控制系统 | HexaPOD、相机、控制器、缓冲区、医疗安全关键 | 至少 `4` 个核心组件；HexaPOD 具备 `6` 自由度 | `UPPAAL` | 控制器完成性、目标位姿可达性与死锁检查 | 可达性、死锁安全、控制完成性 | 🟡 | 用简化离散模型验证放疗控制链条无基本逻辑错误，但连续运动细节仍未纳入。 | [paper](./lee11-radiation-therapy-system/) |
| 🧩 | 2011 | `ravn11` | Modelling and Verification of Web Services Business Activity Protocol | `WS-BA`, 长事务, 通信介质语义 | `WS-Business Activity` 中的 `BAwCC` 协议 | coordinator/participant、消息乱序/丢失/重复、协议修补 | `1` 个 coordinator + `1` 个 participant；模型含 `600+` 行 C 代码 | `UPPAAL` | 协议安全性、终止性与介质敏感性验证 | 安全、终止性、一致性 | 🟢 | 证明原 `BAwCC` 除完美 FIFO 外都会出错，并验证增强协议可在弱化介质下恢复正确性。 | [paper](./ravn11-web-services-business-activity/) |
| 🎛️ | 2012 | `david12` | Schedulability of Herschel-Planck Revisited Using Statistical Model Checking | `UPPAAL SMC`, 可调度性, 执行时间区间 | Herschel-Planck 卫星单处理器控制软件任务集（带执行时间区间） | 不确定 `BCET/WCET`、停表、符号 MC + SMC 组合 | 沿用 `32` 任务单 CPU 模型，并把执行时间推广为区间 | `UPPAAL SMC` | 可调度边界、deadline miss 反例与概率评估 | 安全、统计性质、调度性质 | 🟢 | 用符号 MC 和 `UPPAAL SMC` 共同分析带执行时间区间的卫星任务集可调度边界。 | [paper](./david12-herschel-planck-smc/) |
| 🛰️ | 2012 | `fehnker12` | Automated Analysis of AODV Using UPPAAL | AODV, 无线 mesh, 路由发现 | 无线 mesh / MANET 中的 AODV 路由协议 | 按需建路、动态拓扑、反例驱动协议修补 | 穷举 `<=5` 节点；`444` 静态拓扑、`1978` 加链路对、`1978` 删链路对 | `UPPAAL` | 路由发现、最优路与修补收益验证 | 安全、可达性、协议正确性 | 🟢 | 穷举小规模拓扑定位 AODV 缺陷，并量化三类修补对最优路保证的提升。 | [paper](./fehnker12-aodv-uppaal/) |
| 🎛️ | 2013 | `gruhn13` | Design and Verification of a Health-Monitoring Driver Assistance System | 驾驶辅助, 健康监测, 服务化网络 | 面向心脏病高风险驾驶员的健康监测驾驶辅助系统 | 多源传感、动态入网/离网、应急制动、分层验证 | ECG、呼吸带、相机、控制器、紧急制动系统、便携脉搏计等 `8` 类部件 | `UPPAAL` | 控制器时间/功能验证与动态网络分层验证 | 时序约束、功能正确性、通信可达性 | 🟡 | 提出医疗驾驶辅助系统的分层验证框架，其中控制器部分由 `UPPAAL` 承担。 | [paper](./gruhn13-health-monitoring-driver-assistance/) |
| 🎛️ | 2019 | `alur19` | Continuous-Time Models for System Design and Analysis | pacemaker, hybrid automata, 医疗 `CPS` | 双腔植入式心脏起搏器及其心脏环境模型 | `DDD/VDI` 模式、离散控制器 + 连续心脏、抽象证明 | `8` 个 pacemaker 过程 + `5` 个心脏抽象部件；基础 `DDD` 与 `DDD-VDI` 两种配置 | `UPPAAL` | 上/下速率限制与心跳传播要求验证 | 安全、时序约束、监视器性质 | 🟢 | 先用 `SpaceEx` 证明心脏抽象，再在 `UPPAAL` 中验证 pacemaker 的上下速率限制。 | [paper](./alur19-pacemaker-continuous-time/) |
| 🏭 | 2019 | `martinelli19` | Timed Automata Networks for SCADA Attacks Real-Time Mitigation | SCADA, 攻击检测, 燃气管网 | SCADA 燃气管网日志驱动的攻击检测模型 | 日志转自动机、双特征同步、`DoS/MI` 攻击公式 | `269,228` 条测量；`100 ms` 窗口生成 `2,692` 个模型；`1346` 正常 + `1346` 攻击 | `UPPAAL` | 攻击模式可达性判定与检测评估 | 可达性、时序模式、工业安全 | 🟢 | 把 SCADA 日志转成 timed automata 网络，并用 `UPPAAL` 公式检测 `DoS` 与恶意注入攻击。 | [paper](./martinelli19-scada-attack-mitigation/) |

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

## 初步归类与当前观察

1. 文库扩展到 `2019` 后，`UPPAAL` 应用主线已不再局限于早期协议和控制器，而是明显延伸到航天调度、医疗设备、工业安全和日志驱动检测。
2. `2010` 年后的高质量条目更强调“被验证系统是哪一层边界”，不少论文只验证子机制、抽象环境或日志模型，不能含糊写成“验证了整个系统”。
3. 当前真正可直接复用的公开材料仍然不多，主要集中在官方 `uppaal-models` 仓库和公开数据集页，而不是论文附录本身。
4. 控制器与嵌入式系统类条目已成为当前最大簇，说明后续继续向调度、医疗控制和工业嵌入式扩库会更贴近博士研究主线。
5. SCADA、driver assistance 这类案例提醒后续整理时要明确区分“验证控制逻辑”“验证网络结构”“验证日志模式”三种不同对象。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化 `open_explore/uppaal_apps/`，建立 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 三个核心文件 | 先把应用文库与 `uppaal_tech/` 拆开，固定边界与总账骨架 | 先解决结构拆分，后续再正式扩充应用条目 |
| 2026-03-31 | 重写 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)，并新增 [DESC_GUIDE.md](./DESC_GUIDE.md) | 将文库主线收紧到“使用 `UPPAAL` 对具体对象进行形式化验证”的应用论文，补齐大规模扩库所需的字段、状态和单篇规范 | 为后续批量抓取控制系统、嵌入式系统、工业 `CPS` 与协议验证文献做准备 |
| 2026-03-31 | 补充领域类型动态扩充规则，并将统计区改为显式含年份的表格 | 把领域分类从固定枚举调整为“当前骨架 + 按实际收录动态扩充”，同时强化时间维度统计与排序口径 | 为后续按年份维护大规模文献总表做准备 |
| 2026-03-31 | 首批纳入 `10` 篇 `2010` 年及以前的 `UPPAAL` 应用论文，补齐每篇的 `paper.pdf + paper_content.txt + bibtex.bib` | 基于官网 `Case Studies` 与 `Documentation` 反向筛查 `20+` 个候选，优先选择 PDF 可稳定获取且验证主线清晰的协议、控制器、工业和软件案例 | 建立 `1996-2010` 的早期应用主线骨架 |
| 2026-03-31 | 为首批 `10` 篇论文全部补齐 `desc.md`，并把总账字段改为“被验证系统 / 系统特点 / 系统规模 + 公开性清单” | 取消 `详度/实现` 两列，改为维护单篇 `desc.md`、统一论文表和“案例/模型/数据公开性清单”；同时把“默认必须写 `desc.md`”落进 [README.md](./README.md) 与 [GUIDE.md](./GUIDE.md) | 让 `uppaal_apps/` 的维护方式对齐 `baselines` 的公开性思路，并固定今后入账口径 |
| 2026-03-31 | 新增 `10` 篇 `2010-2019` 应用论文，覆盖 RapidIO、卫星调度、工业 PLC、`WS-BA`、医疗设备、AODV、SCADA 安全等方向，并全部补齐 `desc.md` | 继续按“系统边界明确 + 性质清晰 + 规模可描述 + 公开性可追溯”的口径扩库，同时核验可公开模型/数据链接是否当前可访问 | 把文库上界从 `2010` 推进到 `2019`，并补上少量当前可直接获取的模型/数据案例 |

## 失败与阻塞记录

| 时间 | 候选条目/对象 | 问题 | 当前处理 |
|---|---|---|---|
| 2026-03-31 | Model-Checking Real-Time Control Programs | 官网旧链接 `https://homes.cs.aau.dk/~paupet/papers/ikllmmpt-ecrts00.pdf` 与对应 `.bib.txt` 返回 `404`，无法稳定取得三件套 | 本轮未正式入账；已以 [bordbar03-timeliness-qos-multimedia/](./bordbar03-timeliness-qos-multimedia/) 补足名额，超过 `5` 天后若找到可用公开版本再重试 |
| 2026-03-31 | `philaudio.ta` / `bopdp.xml` / `rvs10.zip` / `rsv-tacas11.zip` 等历史工件链接 | 官网 benchmark/case-study 页仍提到历史模型入口，但当前公开直链已失效或返回 `404` | 在公开性清单中统一按 `🟠 信息不清` 处理，不误记为“模型可直接获取” |
