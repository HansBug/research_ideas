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

- `UPPAAL + CAN/clock synchronization/802.11i/RTPS + protocol verification`
- `UPPAAL + DIMA/ARINC-653/AFDX/multiprocessor schedulability + analysis`
- `UPPAAL + tramway/autonomous positioning/ERTMS/lift system + case study`
- `UPPAAL + edge persistence/NetBill/service protocol + model checking`

### 已观察到的高命中特征

- 题目中直接出现系统名、协议名、标准名或中间件名，仍比泛化 `application/system` 检索更稳定
- 正文若同时给出组件分解、性质簇、参数表和验证结论，后续写 `desc.md` 与统一总表最省返工
- 作者主页、机构仓储、开放期刊 PDF、中文期刊官网、Springer `content/pdf` 和 `GitHub/Zenodo` 工件仍是稳定主入口
- `CAN`、`802.11i`、`RTPS`、`DIMA`、tramway `APS` 与 edge persistence 这类“对象名很具体”的方向，本轮命中率明显高于泛化检索

### 已观察到的低命中特征

- 只剩出版社摘要页、目录页、聚合页或 `ResearchGate` 镜像，但没有稳定 PDF 的候选
- 主要讲工具、翻译框架或方法对照，但应用对象只是一笔带过的论文
- 只有“做了验证”结论，却没有清晰系统边界、性质或结果表格的候选
- 历史页面会写 `models available`，但若没有稳定工件直链，仍不适合在公开性里高估

### 检索倾向调整

- 继续优先使用具体系统词和标准词，如 `CAN`、`802.11i`、`RTPS`、`DIMA`、`ARINC-653`、`AFDX`、tramway `APS`
- 正式入账时仍要求 `paper.pdf + paper_content.txt + bibtex.bib + desc.md` 四件套同时完成
- 公开性继续单独维护为“案例/模型/数据公开性清单”，没有稳定工件入口时统一如实记为 `🟠`
- 老论文优先追作者主页/机构镜像与会议 PDF，新论文优先追开放期刊、`GitHub/Zenodo` 与文中明确给出的模型页面

## 当前收录统计

| 统计项 | 数值 | 年份信息 |
|---|---:|---|
| 已收录顶层条目 | 80 | 覆盖 `1996-2026` |
| 本轮新增条目 | 10 | 本轮补入 `2003-2021` 的分布式 lift、`CAN` 时钟同步、多处理器可调度性、`802.11i`、`RTPS`、edge persistence、tramway `APS`、`DIMA` 与 `NetBill` 场景 |
| 其中已补 `desc.md` | 80 | 全部正式条目均已完成整理 |
| 当前 `🟢 直接可用` | 49 | tramway hazard、`RTPS` 与 `DIMA` 等高价值样本继续补厚，可直接横向比较的条目更多 |
| 当前 `🟡 可整理` | 31 | 主要是方法色彩偏强、工件未公开或边界仍需按论文重建的案例 |
| 当前 `⏳ 尚未提取` | 0 | 无 |
| 公开性分布 | `🟢 20 / 🟠 56 / 🔒 4` | 本轮新增了 tramway `APS` 的公开模型仓库，但多数协议、调度与服务案例仍需按论文重建 |
| 最早年份 | 1996 | 现已同时覆盖两篇 `1996` 早期协议案例 |
| 最晚年份 | 2026 | 已扩展到 `CARE` 运行时形式化分析与模型驱动测试案例 |
| 当前失败/阻塞记录 | 4 | 记录见“失败与阻塞记录” |

## 按年份分布统计

| 年份 | 条目数 | 已补 `desc.md` | 备注 |
|---|---:|---:|---|
| 1996 | 2 | 2 | 覆盖 Philips 音频协议与 Ethernet-like 冲突避免协议 |
| 1997 | 3 | 3 | 收录重传协议、TDMA 启动与 B&O 工业协议 |
| 1998 | 2 | 2 | 覆盖 lip sync 与车辆换挡控制 |
| 1999 | 2 | 2 | 扩展到 B&O 电源控制器与 LEGO 分拣控制程序 |
| 2000 | 2 | 2 | 覆盖 ABB `AF100` field bus 与 `SIDMAR` batch plant 综合案例 |
| 2003 | 2 | 2 | 新增分布式 lift 重设计案例，并保留 multimedia `QoS` 主线 |
| 2005 | 1 | 1 | 新增 `CAN` 时钟同步协议验证案例 |
| 2006 | 2 | 2 | 覆盖 Zeroconf 地址配置与 BMP 物理层通信协议 |
| 2007 | 2 | 2 | 新增 `SHIM6` 协议草案验证，并保留 pig stable 气候控制 `Tiga` 合成案例 |
| 2008 | 3 | 3 | 新增 `FlexRay` membership 与 `EUV` 工业案例，并保留 COMDES-II turntable 控制系统验证 |
| 2009 | 1 | 1 | 新增 Océ 打印 pipeline 自适应调度案例 |
| 2010 | 4 | 4 | 扩展到 RapidIO、卫星调度、工业 PLC 与 `WS-AT` |
| 2011 | 2 | 2 | 覆盖医疗放疗控制与 `WS-BA` 协议 |
| 2012 | 4 | 4 | 扩展到 pacemaker，并继续保留 `Bluetooth` 发现、`UPPAAL SMC` 调度与 AODV 路由主线 |
| 2013 | 3 | 3 | 扩展到嵌入式传感器接口分析、`ICCP` checker 与健康监测驾驶辅助 |
| 2014 | 2 | 2 | 新增循线机器人几何验证案例，并保留 laser tracheotomy 在线 `SMC` 案例 |
| 2015 | 1 | 1 | 新增多处理器实时系统可调度性模板案例 |
| 2016 | 1 | 1 | 补入数据流应用能耗控制综合案例 |
| 2017 | 3 | 3 | 扩展到 `ROS` 机器人应用，并继续保留 `CAN` database 与 TCP/SCTP 握手主线 |
| 2018 | 5 | 5 | 新增 `DIMA`、`802.11i` 与 `NetBill` 场景，并保留多车道变道控制器活性修复案例 |
| 2019 | 4 | 4 | 扩展到 cooperative automotive timing 与 `SIP/ZRTP`，并继续保留 pacemaker 和 SCADA 主线 |
| 2020 | 6 | 6 | 新增 `RTPS` 双模型验证案例，并继续保留投票协议、疫情流体模型、moving block 铁路、`WBAN` 与 WSN 攻击分析 |
| 2021 | 12 | 12 | 新增 edge persistence 与 tramway `APS` hazard 分析，并继续保留铁路接口、rerouting、能量、`5G`、`CKB` 与交通灯主线 |
| 2022 | 3 | 3 | 新增 `ERTMS` full moving block 与 quarry 多代理策略综合，并保留在线针导航案例 |
| 2023 | 3 | 3 | 扩展到机械呼吸机、`Sigfox` 节点寿命与 smart home `IoT` 案例 |
| 2024 | 1 | 1 | 扩展到电子考试流程可信设计 |
| 2025 | 3 | 3 | 新增 research reactor 备件优化，并保留 `ROS`/`ROS 2` 反应时间与 pattern-based verification 案例 |
| 2026 | 1 | 1 | 新增 `CARE` 运行时形式化分析与模型驱动测试案例 |

## 双轴分类口径

### 主轴分类

| Emoji | 主轴分类 | 含义 | 当前正式条目数 |
|---|---|---|---:|
| 🛰️ | 协议与通信机制 | 论文真正验证的是协议状态机、通信规则、消息协调或转发/同步机制 | 27 |
| 🎛️ | 控制器与设备控制 | 论文真正验证的是控制器、设备行为、执行逻辑或闭环控制结构 | 26 |
| ⏱️ | 调度、资源与性能分析 | 论文真正验证的是可调度性、资源竞争、时延、`QoS`、能量或其他性能边界 | 17 |
| 🧩 | 软件服务与业务流程 | 论文真正验证的是软件服务编排、角色协作、业务流程规则或工作流状态机 | 6 |
| 📊 | 场景行为与监测分析 | 论文真正验证的是日志模式、群体场景、策略评估或监测判定模型 | 4 |

### 次轴场景

| Emoji | 次轴场景 | 含义 | 当前正式条目数 |
|---|---|---|---:|
| 🌐 | 网络与分布式服务 | 网络协议、Web 服务、无线网络、`5G` 编排等 | 22 |
| 🎵 | 多媒体与消费电子 | 音视频协议、多媒体同步、消费电子组件等 | 6 |
| 🏭 | 工业与基础设施 | 工业自动化、现场总线、`SCADA`、工业网络等 | 16 |
| 🚦 | 交通、车载与铁路 | 交通灯、铁路、车辆控制、驾驶辅助等 | 14 |
| 🏥 | 医疗与健康 | 医疗设备、治疗系统、植入式设备、临床导航等 | 7 |
| 🚀 | 航天 | 卫星、航天任务软件与空间任务调度等 | 4 |
| 🦠 | 公共健康与疫情策略 | 传染病传播、接触追踪与公共卫生决策支持 | 1 |
| 🔋 | 能源与采能计算 | 采能系统、电池 sizing、能量迁移计算等 | 2 |
| 🎓 | 教育与考试流程 | 电子考试、教学流程与教育规则系统等 | 1 |
| 🤖 | 机器人与自主系统 | LEGO 机电平台、RoboCup、多智能体机器人与自主决策等 | 7 |

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
| 🛰️ | 🌐 | 1996 | `jensen96` | Modelling and Analysis of a Collision Avoidance Protocol using SPIN and `UPPAAL` | 冲突避免协议, 轮询, 广播介质 | 运行在类 Ethernet 广播介质上的冲突避免轮询协议 | master 轮询、介质延迟/丢包、slave 异步回复 | `1` 个 master + `1` 个 medium + `N` 个 slave；有界活性示例采用 `3` 用户/从站场景 | `UPPAAL` | 无冲突、消息送达与 round-trip 时间界验证 | 安全、有界活性、有界响应 | 🟢 | 用 master/medium/slave 自动机验证冲突避免协议，并给出 timeout 与 round-trip 的时间界。 | [paper](./jensen96-collision-avoidance-protocol/) |
| 🛰️ | 🌐 | 1997 | `dargenio97` | The Bounded Retransmission Protocol Must Be on Time! | 文件传输, 有界重传, 超时 | BRP 有界重传文件传输协议 | 分块传输、丢包信道、超时/中止 | 发送端/接收端 + `T1/T2` 定时器；原文未给统一状态规模 | `UPPAAL` | 服务符合性与超时参数验证 | 安全、服务符合性、时序约束 | 🟢 | 通过 timed/untimed 对照说明 BRP 正确性依赖真实超时结构。 | [paper](./dargenio97-bounded-retransmission-time/) |
| 🛰️ | 🎵 | 1997 | `havelund97` | Formal Modelling and Analysis of an Audio/Video Protocol: An Industrial Case Study Using UPPAAL | 工业协议, 音视频总线, 碰撞检测 | Bang & Olufsen 音视频控制协议 | 单总线、`2800` 行汇编、工业真实协议 | `9` 个 automata；`5` 次主要迭代、约 `3` 个月；错误轨迹近 `2000` 步 | `UPPAAL` | 协议建模、错误定位与修复验证 | 安全、有界活性、一致性 | 🟢 | 通过自动诊断轨迹定位并修复 B&O 工业协议中的时序错误。 | [paper](./havelund97-audio-video-protocol/) |
| 🛰️ | 🌐 | 1997 | `lonn97` | Formal Verification of a TDMA Protocol Start-Up Mechanism | `TDMA`, 启动同步, 时钟漂移 | DACAPO `TDMA` 启动机制 | 多主站、启动同步、时钟漂移 | `4` 个站点 + 总线；时钟漂移 `±10^-3` | `UPPAAL` | 启动同步与截止时间验证 | 安全、有界响应、时序约束 | 🟢 | 证明四站 TDMA 系统能在漂移条件下于有界时间内完成同步。 | [paper](./lonn97-tdma-startup-mechanism/) |
| ⏱️ | 🎵 | 1998 | `bowman98` | Automatic Verification of a Lip Synchronisation Algorithm Using UPPAAL | lip sync, multimedia, `QoS` | lip synchronization 算法 | 音视频双流同步、jitter/skew、watchdog | 音频 `30 ms`/包、视频 `40 ms`/帧；non-anchored jitter 下约 `1031 ms` | `UPPAAL` | 同步边界、timelock 与 `QoS` 验证 | `QoS` 时序、timelock/deadlock | 🟢 | 自动分析 lip sync 算法，发现它会在部分场景下先 timelock 而非正常报错。 | [paper](./bowman98-lip-synchronisation-algorithm/) |
| 🎛️ | 🚦 | 1998 | `lindahl98` | Formal Design and Analysis of a Gear Controller | 换挡控制, 车辆控制, 有界响应 | 车辆 prototype gear controller | 控制 clutch/engine/gearbox，安全关键 | `46` 条公式；完整换挡 `<=1.5 s`；验证约 `2.99 s` | `UPPAAL` | 控制器设计验证与响应时间检查 | 安全、有界响应 | 🟢 | 在工业环境假设下验证换挡控制器，并把 bounded response 转成可达性分析。 | [paper](./lindahl98-gear-controller/) |
| 🎛️ | 🎵 | 1999 | `havelund99` | Formal Verification of a Power Controller Using the Real-Time Model Checker UPPAAL | 电源控制, 中断处理, 音视频组件 | 音视频组件 power controller | 多任务优先级、中断无丢失、上下电 | `15` 条性质；发现并修正 `3` 个设计错误 | `UPPAAL` | 电源控制逻辑与中断安全验证 | 安全、有界响应、时序约束 | 🟢 | 验证多任务电源控制器，修正设计错误并发现中断频率上界需求。 | [paper](./havelund99-power-controller/) |
| 🎛️ | 🤖 | 1999 | `iversen99` | Model-Checking Real-Time Control Programs. Verifying LEGO Mindstorms Systems Using UPPAAL | LEGO Mindstorms, 实时控制程序, 颜色分拣 | 基于 LEGO `RCX` 的颜色分拣控制程序与分拣机械装置 | round-robin 调度、真实执行时间、传感器与 kick arm 环境联动 | `RCX` 平台最多 `10` 个任务与 `32` 个整型变量；案例核心为 `2` 个任务 + 砖块/机械臂环境 | `UPPAAL` | 分拣正确性与执行机构安全验证 | 安全、可达性、设备安全 | 🟢 | 把 `RCX` 控制程序自动翻译为 timed automata，并在三黑砖场景中定位真实分拣缺陷。 | [paper](./iversen99-lego-mindstorms-systems/) |
| 🛰️ | 🏭 | 2000 | `david00` | Modelling and Analysis of a Commercial Field Bus Protocol | field bus, `AF100`, 工业调试 | ABB `AF100` bus coupler / data link layer | 商业 field bus、超时/重传/信号量 | 面向 `80` 站；数百页规格 + 数千行源码；`82/35` 条性质 | `UPPAAL` | 大型工业协议错误定位 | 安全、同步正确性、时序约束 | 🟢 | 通过抽象模型快速定位 AF100 工业协议中的同步与超时错误源。 | [paper](./david00-commercial-field-bus-protocol/) |
| 🎛️ | 🏭 | 2000 | `hune00` | Guided Synthesis of Control Programs for a Batch Plant using `UPPAAL` | batch plant, 调度综合, 工业控制 | `SIDMAR` 钢铁 batch plant 调度与控制程序综合流程 | 多 batch、共享设备与吊车、trace 可投影为控制程序 | 最大 `125` 个 automata、`183` 个 clocks；引导后可处理 `60` 个 batch | `UPPAAL` | 批处理调度可达性与控制程序综合 | 可达性、安全、时间约束 | 🟢 | 用引导式搜索把 batch plant 可综合规模从 `2` 个 batch 提升到 `60` 个，并在 `LEGO` plant 上执行生成程序。 | [paper](./hune00-batch-plant-control-synthesis/) |
| ⏱️ | 🎵 | 2003 | `bordbar03` | Verification of Timeliness QoS Properties in Multimedia Systems | `QoS`, throughput, latency | distributed multimedia video player 示例 | ODP/QoS 契约、QTA/test automata | video player 示例；原文未给统一 benchmark 规模 | `UPPAAL` | Timeliness `QoS` 属性构造与验证 | throughput、jitter、latency | 🟡 | 通过 QTA 把多媒体 `QoS` 属性规约为 `UPPAAL` 可达性问题。 | [paper](./bordbar03-timeliness-qos-multimedia/) |
| 🎛️ | 🏭 | 2003 | `pang03` | Analyzing the Redesign of a Distributed Lift System in UPPAAL | distributed lift system, `CAN`, startup, synchronous movement | 真实分布式举升系统中的多 lift / station 协同控制 | 启动阶段分配编号、正常阶段轮转广播状态、`sync` 消息触发全体同步运动 | `1` 个 `Bus` + 每个 lift 的 `Station/Interface` + `Timer`；lift 数量参数化 | `UPPAAL` | 死锁、按钮响应活性与同步运动安全验证 | 死锁安全、活性、同步安全 | 🟢 | 用 test automata 证明开发者重设计仍有漏洞，并给出满足五条需求的修复方案。 | [paper](./pang03-distributed-lift-system-redesign/) |
| 🛰️ | 🚦 | 2005 | `rodrigueznavas05` | Using UPPAAL to Model and Verify a Clock Synchronization Protocol for the Controller Area Network | `CAN`, clock synchronization, drift, fault tolerance | 面向 `CAN` 网络的容错时钟同步协议 | 主从同步、优先级仲裁、在线时间戳、显式时钟漂移/校正 | 每个 master 含 `Master` + `Clkctrl`；另有 `Chanctrl`/`Roundctrl`；master 数量参数化 | `UPPAAL` | 同步轮次、漂移校正与故障主节点替换分析 | 时序约束、容错正确性、同步一致性 | 🟡 | 在 `UPPAAL` 中给出可变漂移时钟的建模方案，并据此开始验证 `CAN` 同步协议的关键机制。 | [paper](./rodrigueznavas05-can-clock-synchronization/) |
| 🛰️ | 🌐 | 2006 | `gebremichael06` | Analysis of the Zeroconf Protocol Using UPPAAL | Zeroconf, RFC 3927, link-local address | RFC 3927 Zeroconf IPv4 链路本地地址配置协议 | 从 RFC 文本逐段建模，保留 probe/announce/defend 关键阶段 | 每个 host 由 `3` 个 timed automata 组成；`3` host 实例可完整探索，并对一般规模给出手工证明 | `UPPAAL` | 地址互斥、死锁与规范歧义验证 | 安全、死锁安全、规范一致性 | 🟢 | 从 RFC 出发建模 Zeroconf，并同时产出 mutual exclusion 证明、歧义清单和公开工件。 | [paper](./gebremichael06-zeroconf-link-local-addresses/) |
| 🛰️ | 🌐 | 2006 | `vaandrager06` | Analysis of a Biphase Mark Protocol with Uppaal and PVS | 物理层协议, BMP, 参数化验证 | 面向物理层串行通信的 biphase mark protocol (`BMP`) | 同时考虑 drift、jitter、edge distortion，并联合 `PVS` 做参数化证明 | 围绕 coder/wire/sampler/decoder `4` 个核心部件展开；验证多个参数实例并给出参数化约束 | `UPPAAL` | 协议正确性与可支持位率分析 | 安全、参数正确性、定量优化 | 🟢 | 结合 `UPPAAL` 与 `PVS` 重新分析 BMP 参数，提出更快且仍具容错能力的实现方案。 | [paper](./vaandrager06-biphase-mark-protocol/) |
| 🎛️ | 🏭 | 2007 | `jessen07` | Guided Controller Synthesis for Climate Controller Using Uppaal Tiga | pig stable, 气候控制, 策略综合 | 多分区猪舍气候控制系统 | 温湿度耦合环境、timed game 合成、`Simulink` 闭环评估 | 结果章节给出 `3` 区温湿度控制比较；策略进一步送入 `Simulink` 生成 `S-function` | `UPPAAL Tiga` | 控制策略综合与目标函数优化 | 安全、不变式、定量优化 | 🟢 | 用 `Tiga` 合成猪舍气候控制策略，并在连续仿真中比较能耗与收敛速度权衡。 | [paper](./jessen07-climate-controller-tiga/) |
| 🛰️ | 🌐 | 2007 | `mekking07` | Formalizing SHIM6, a Proposed Internet Standard in UPPAAL | SHIM6, IPv6 multihoming, Internet standard | `SHIM6` 多宿主主机 shim 层握手与 locator 切换流程 | `I2/I2bis` 可选重传、payload 接收与 responder nonce 语义是主要难点 | `2` 页短文；原文未给 automata 数与状态空间规模 | `UPPAAL` | 协议握手、重传与草案歧义验证 | 死锁安全、消息一致性、语义歧义 | 🟡 | 用 `UPPAAL` 直接暴露 `SHIM6` 草案中 `I2/I2bis` 与 responder nonce 的关键歧义。 | [paper](./mekking07-shim6-internet-standard/) |
| 🎛️ | 🏭 | 2008 | `braspenning08` | Model-based system analysis using Chi and Uppaal: An industrial case study | `Chi`, industrial case study, vacuum control | ASML `EUV` wafer scanner 中 vacuum/source 协同控制子系统 | `vented/pre-vacuum/exposure/active` latch 互锁、支持中断与错误恢复 | 环境/真空/光源 `3` 模块；原始状态空间约 `20510`，修复后约 `9961` | `UPPAAL` | 工业控制 sequence、互锁与时间上界验证 | 安全、死锁安全、有界时序 | 🟢 | 用 `Chi->UPPAAL` 在 ASML `EUV` 案例中发现 `5` 个错误并提前约 `20` 周暴露集成问题。 | [paper](./braspenning08-chi-industrial-case-study/) |
| 🛰️ | 🚦 | 2008 | `mudaliar08` | Verification of FlexRay Membership Protocol Using UPPAAL | FlexRay, membership protocol, fault tolerance | 车载 `FlexRay` 网络中的 membership protocol | 混合时触发/事件触发通信、成员一致性、故障移除与 join request | `Bus/Global Clock/DTask/Node/Scheduler` `5` 类核心组件；实验比较 `10` processes 映射到 `4-8` nodes | `UPPAAL` | 成员一致性、故障处理与响应时间验证 | 安全、活性、有界响应 | 🟢 | 验证 `FlexRay` membership 行为成立，并给出 `10` 个 process 采用 `5` 个 nodes 的工程折中结论。 | [paper](./mudaliar08-flexray-membership-protocol/) |
| 🎛️ | 🏭 | 2008 | `xu08` | Verification of COMDES-II Systems Using UPPAAL with Model Transformation | COMDES-II, turntable, 模型转换 | 基于 COMDES-II 设计的 Turntable Control System | 显式保留 actor、scheduler、state machine FB 的控制语义 | 案例模型含 `6` 个 actor tasks；代表性查询约 `7s` 完成，内存约 `18220 KB` | `UPPAAL` | 调度与反应行为验证 | 安全、调度性质、反应语义 | 🟡 | 通过语义锚定把 COMDES-II 控制模型转到 `UPPAAL`，并在 turntable 案例上证明其可验证。 | [paper](./xu08-comdes-ii-systems/) |
| ⏱️ | 🏭 | 2009 | `alattili09` | Adaptive Scheduling of Data Paths using Uppaal Tiga | printer/copier pipeline, scheduling, trade-off | Océ 打印/复印系统的 image-processing pipeline 与资源调度 | 多 datapath 共享 `Scanner/IP/USB/memory`，作业到达时间不可预测 | 基础案例围绕 `DirectCopy` 与 `PrintWithProcessing`；扩展模型还分析 `10` 个 `ScanToEmail` jobs | `UPPAAL Tiga` | 工业数据通路调度与 Pareto trade-off 综合 | 有界响应、调度性能、赢策略 | 🟢 | 为 Océ pipeline 综合出 `6` 个 Pareto-optimal 自适应调度策略，并指出自动规则难直接部署。 | [paper](./alattili09-adaptive-scheduling-data-paths/) |
| 🎛️ | 🏭 | 2010 | `belmokadem10` | Verification of a Timed Multitask System with Uppaal | PLC, 多任务控制, 反应时间 | Bosch MSS station 2 多任务 PLC 控制程序 | PLC 周期扫描、事件中断、TON 定时块、机械环境联动 | 全局模型约 `30 x 10^6` 状态；比较单任务与多任务两种方案 | `UPPAAL` | 工业控制反应时间与 observer 度量验证 | 可达性、有界响应、时序约束 | 🟢 | 用 observer 自动机验证多任务 PLC 站点的停机反应时间，并证明 `<10` 但不满足 `<=5`。 | [paper](./belmokadem10-timed-multitask-system/) |
| ⏱️ | 🚀 | 2010 | `mikucionis10` | Schedulability Analysis Using Uppaal: Herschel-Planck Case Study | 可调度性, 卫星软件, 资源竞争 | Herschel-Planck 卫星单处理器控制软件任务集 | 固定优先级抢占、资源共享、任务挂起、工业航天软件 | `32` 个任务、`6` 类共享资源、`4` 个运行实例 | `UPPAAL` | 任务可调度性、WCRT 与 CPU 利用率分析 | 安全、有界响应、调度性质 | 🟢 | 证明卫星任务集可调度，并给出比传统 RTA 更紧的关键任务响应时间上界。 | [paper](./mikucionis10-herschel-planck-case-study/) |
| 🛰️ | 🌐 | 2010 | `ravn10` | A Formal Analysis of the Web Services Atomic Transaction Protocol with UPPAAL | web services, distributed transaction, consistency | `WS-AT` 分布式事务协议 | coordinator + participants、2PC/3-phase、TLA+ 对照 | 可验证至 `5` 个参与者 | `UPPAAL` | 协议一致性与工具对照验证 | 安全、一致性、可达性 | 🟡 | 把 WS-AT 从 TLA+ 转写为 `UPPAAL` 模型，并比较两类工具链的性能与扩展性。 | [paper](./ravn10-web-services-atomic-transaction/) |
| ⏱️ | 🏭 | 2010 | `xing10` | UPPAAL in Practice: Quantitative Verification of a RapidIO Network | RapidIO, 工业网络, 最坏时延 | 基于 RapidIO 的多处理器运动控制平台互连网络 | 周期控制流量、交换网络、最坏包时延、与 POOSL 对照 | `5` 个 blade、`10` 个交换机、`40` 个端点；全系统约 `2500` 个活动 | `UPPAAL` | 工业互连网络最坏时延分析 | 定量时序、最坏情况分析 | 🟢 | 把 RapidIO 工业性能模型转为 `UPPAAL`，用启发式分析高负载场景下的最坏时延。 | [paper](./xing10-rapidio-network/) |
| 🎛️ | 🏥 | 2011 | `lee11` | Modeling and Analysis of Radiation Therapy System with Respiratory Compensation Using Uppaal | 放疗控制, 呼吸补偿, 医疗设备 | 带呼吸补偿的放疗定位/跟踪控制系统 | HexaPOD、相机、控制器、缓冲区、医疗安全关键 | 至少 `4` 个核心组件；HexaPOD 具备 `6` 自由度 | `UPPAAL` | 控制器完成性、目标位姿可达性与死锁检查 | 可达性、死锁安全、控制完成性 | 🟡 | 用简化离散模型验证放疗控制链条无基本逻辑错误，但连续运动细节仍未纳入。 | [paper](./lee11-radiation-therapy-system/) |
| 🛰️ | 🌐 | 2011 | `ravn11` | Modelling and Verification of Web Services Business Activity Protocol | `WS-BA`, 长事务, 通信介质语义 | `WS-Business Activity` 中的 `BAwCC` 协议 | coordinator/participant、消息乱序/丢失/重复、协议修补 | `1` 个 coordinator + `1` 个 participant；模型含 `600+` 行 C 代码 | `UPPAAL` | 协议安全性、终止性与介质敏感性验证 | 安全、终止性、一致性 | 🟢 | 证明原 `BAwCC` 除完美 FIFO 外都会出错，并验证增强协议可在弱化介质下恢复正确性。 | [paper](./ravn11-web-services-business-activity/) |
| 🛰️ | 🌐 | 2012 | `arry12` | Formal Verification of Device Discovery Mechanism using UPPAAL | Bluetooth, device discovery, frequency hopping | Bluetooth ad hoc 网络中的 device discovery 过程 | sender/receiver 频率跳变、双节点连接、轻量级能量变量 | `2` 个设备节点 + `1` 个接收频率模板；代表性查询使用 `30000` 时间单位上界 | `UPPAAL` | 发现成功率与数据接收验证 | 概率可达性、时间界、能量约束 | 🟡 | 用简化 Bluetooth discovery 模型检查回复与接收数据的概率边界。 | [paper](./arry12-device-discovery-mechanism/) |
| ⏱️ | 🚀 | 2012 | `david12` | Schedulability of Herschel-Planck Revisited Using Statistical Model Checking | `UPPAAL SMC`, 可调度性, 执行时间区间 | Herschel-Planck 卫星单处理器控制软件任务集（带执行时间区间） | 不确定 `BCET/WCET`、停表、符号 MC + SMC 组合 | 沿用 `32` 任务单 CPU 模型，并把执行时间推广为区间 | `UPPAAL SMC` | 可调度边界、deadline miss 反例与概率评估 | 安全、统计性质、调度性质 | 🟢 | 用符号 MC 和 `UPPAAL SMC` 共同分析带执行时间区间的卫星任务集可调度边界。 | [paper](./david12-herschel-planck-smc/) |
| 🛰️ | 🌐 | 2012 | `fehnker12` | Automated Analysis of AODV Using UPPAAL | AODV, 无线 mesh, 路由发现 | 无线 mesh / MANET 中的 AODV 路由协议 | 按需建路、动态拓扑、反例驱动协议修补 | 穷举 `<=5` 节点；`444` 静态拓扑、`1978` 加链路对、`1978` 删链路对 | `UPPAAL` | 路由发现、最优路与修补收益验证 | 安全、可达性、协议正确性 | 🟢 | 穷举小规模拓扑定位 AODV 缺陷，并量化三类修补对最优路保证的提升。 | [paper](./fehnker12-aodv-uppaal/) |
| 🎛️ | 🏥 | 2012 | `jiang12` | Modeling and Verification of a Dual Chamber Implantable Pacemaker | pacemaker, medical device, DDD, PMT | 双腔植入式心脏起搏器及其闭环心脏环境 | `LRI/AVI/URI/PVARP/VRP` 五定时部件、心房/心室事件、`PMT` 风险 | `5` 个 pacemaker 定时部件 + 随机心脏模型；名义参数含 `TLRI=1000`、`TAVI=150`、`TURI=400` | `UPPAAL` | 上下速率限制、`PMT` 场景与纠正算法验证 | 安全、时序约束、异常场景 | 🟢 | 用闭环心脏-起搏器模型验证基本速率要求，并定位 mode-switch 抗 `PMT` 策略的边界问题。 | [paper](./jiang12-dual-chamber-pacemaker/) |
| 🎛️ | 🏭 | 2013 | `bourke13` | Analyzing an Embedded Sensor with Timed Automata in `Uppaal` | 嵌入式传感器, timing diagram, 汇编驱动 | `Sharp GP2D02` 红外传感器及其汇编驱动接口 | datasheet 时序图、driver/sensor 分离、汇编级验证 | tester `13` locations / `98` transitions；transmission correctness 探索 `851713` states | `UPPAAL` | 接口时序一致性与传输正确性验证 | 精化、一致性、安全 | 🟢 | 通过 timed trace inclusion 把 datasheet 级时序规范一路验证到汇编驱动实现。 | [paper](./bourke13-embedded-sensor/) |
| 🎛️ | 🚦 | 2013 | `gruhn13` | Design and Verification of a Health-Monitoring Driver Assistance System | 驾驶辅助, 健康监测, 服务化网络 | 面向心脏病高风险驾驶员的健康监测驾驶辅助系统 | 多源传感、动态入网/离网、应急制动、分层验证 | ECG、呼吸带、相机、控制器、紧急制动系统、便携脉搏计等 `8` 类部件 | `UPPAAL` | 控制器时间/功能验证与动态网络分层验证 | 时序约束、功能正确性、通信可达性 | 🟡 | 提出医疗驾驶辅助系统的分层验证框架，其中控制器部分由 `UPPAAL` 承担。 | [paper](./gruhn13-health-monitoring-driver-assistance/) |
| 🛰️ | 🏭 | 2013 | `malik13` | Formal Design of Communication Checkers for `ICCP` using `UPPAAL` | ICCP, smart grid, starvation, checker | 电网控制中心间 `ICCP` 通信与安全检查机制 | 不改协议基座、反例驱动细化 checker、关注资源耗尽攻击 | client/server/device/observer/attacker/checker 六类角色；原文未给统一状态规模 | `UPPAAL` | 协议弱点发现与 checker 设计验证 | 安全、活性、检测性质 | 🟡 | 用 generic attacker 与反例追踪设计 `ICCP` checker，并定位 `device control block starvation` 风险。 | [paper](./malik13-iccp-communication-checkers/) |
| 🎛️ | 🏥 | 2014 | `ma14` | Evaluating On-line Model Checking in `UPPAAL-SMC` using a Laser Tracheotomy Case Study | 在线模型检查, laser tracheotomy, patient-in-the-loop | 激光气管切开 patient-in-the-loop 在线安全监测系统 | 病人轨迹回写模型、每 `3s` 在线适配、面向手术安全 | `6` 条 patient traces、`60` 次实验、每次 `600s`；平均检查时间 `0.047s` | `UPPAAL SMC` | 在线安全性质检查与短时预测评估 | 安全、统计性质、预测误差 | 🟡 | 在医疗闭环中验证在线 `SMC` 的可行性，并把 `SpO2` 相对预测误差控制在约 `2%`。 | [paper](./ma14-laser-tracheotomy-case-study/) |
| 🎛️ | 🤖 | 2014 | `nakatani14` | 2D Geometric Modeling and Verification of Line Tracing Robot Using UPPAAL Model Checker | line tracing robot, geometric modeling, direction constraints | 带光传感器的 line-tracing robot 及其轨道跟随控制 | `10x10` 离散轨道、位置/朝向状态机、禁区与方向约束 | 轨道数组 `10x10`；核心状态为 `pos_x/pos_y/angle` | `UPPAAL` | 轨道区域与前进方向正确性验证 | 安全、轨迹约束、反例可达性 | 🟡 | 用二维离散几何模型证明窄缺口 `C` 型轨道可行，而 `2` 格缺口会让机器人在 `(9,6)` 离轨。 | [paper](./nakatani14-line-tracing-robot/) |
| ⏱️ | 🌐 | 2015 | `dai15` | Schedulability Analysis Model for Multiprocessor Real-Time Systems Using UPPAAL | multiprocessor real-time, schedulability, dependency, stopwatch | 带任务依赖和总线通信的多处理器实时任务系统 | 固定处理器划分、依赖矩阵、总线消息、不确定执行时间和抢占 | `4` 个处理器上的 `21` 任务 `GSM` 实例；扩展到 `103` 任务 `GSM+MP3` | `UPPAAL SMC` | deadline、不可调度概率与响应时间/利用率分析 | 安全、统计性质、性能分析 | 🟡 | 把多处理器可调度性模板化到 `UPPAAL`，既能证明 `21` 任务系统可调度，也能用 `SMC` 快速判定 `103` 任务系统不可调度。 | [paper](./dai15-multiprocessor-realtime-schedulability/) |
| ⏱️ | 🔋 | 2016 | `ahmad16` | Synthesizing Energy-Optimal Controllers for Multiprocessor Dataflow Applications with `Uppaal Stratego` | dataflow, DVFS, DPM, 能耗优化 | `MPEG-4` 数据流应用的多处理器能量控制策略 | throughput 约束下联合调频、关停与任务映射 | `Exynos 4210` 风格平台；目标 `67 fps` / `15 ms`；比较 `1-5` 处理器配置 | `UPPAAL Stratego` | 吞吐约束下的 near-optimal 能耗控制综合 | 定量优化、性能约束、统计比较 | 🟡 | 用 `Stratego` 在满足吞吐的前提下优化能耗，并证明结果与 `CORA` 最优值最多约 `10%` 偏差。 | [paper](./ahmad16-energy-optimal-dataflow-controllers/) |
| 🛰️ | 🚦 | 2017 | `cho17` | `CAN` Database Verification Framework Using `UPPAAL` | CAN, DBC, response time, automotive | 车载 `CAN` database 与消息调度时限验证框架 | `DBC` 自动转模型、总线仲裁、低负载下也可能超时 | `1` 个 Bus + 多个 ECU；deadline 统一 `1 ms`；jitter `100 μs`；位时间抽象 `25 μs` | `UPPAAL` | `DBC` 级消息时限验证与超时定位 | 时间约束、逻辑正确性 | 🟡 | 通过自动建模发现 `0x106/0x109/0x10E` 三条消息虽在 `28.5%` 负载下仍超出 deadline。 | [paper](./cho17-can-database-verification/) |
| ⏱️ | 🤖 | 2017 | `halder17` | Formal Verification of ROS-Based Robotic Applications Using Timed-Automata | ROS, Kobuki, queue overflow, callback timeout | `Kobuki` 机器人中的 `SafetyController` / `Multiplexer` 通信与调度逻辑 | publisher-subscriber 队列、callback queue、`callAvailable()` timeout、优先级仲裁 | wheel / bumper / cliff `3` 类传感器队列 + `SafetyController` 与 `Multiplexer` 核心模块 | `UPPAAL` | 队列溢出、消息可达性与参数敏感性验证 | 安全、活性、资源/时序 | 🟢 | 用 timed automata 穷举 `ROS` 队列与 timeout 参数，发现 `Kobuki` 中的传感器消息丢失和控制饥饿条件。 | [paper](./halder17-ros-robotic-applications/) |
| 🛰️ | 🌐 | 2017 | `saini17` | Evaluating the Stream Control Transmission Protocol Using Uppaal | TCP, SCTP, SYN flooding | TCP 三次握手与 SCTP 四次握手关联建立机制 | 合法/非法客户端、服务器与 `TCB` 联合建模，显式比较 cookie 机制 | 两个协议都建模合法客户端、非法客户端、服务器和连接状态块；重点覆盖握手阶段 | `UPPAAL` | half-open connection 与资源占用安全验证 | 安全、攻击相关性质、资源占用 | 🟢 | 用对照建模证明 TCP 会留下 half-open connection，而 SCTP 的 cookie 机制能避免资源劫持。 | [paper](./saini17-sctp-uppaal/) |
| ⏱️ | 🚀 | 2018 | `han18mars` | A Modeling Framework for Schedulability Analysis of Distributed Avionics Systems | `DIMA`, `ARINC-653`, `AFDX`, schedulability | 由 `ARINC-653` 模块和 `AFDX` 网络组成的 `DIMA` 航电系统 | 两级调度、sampling/queuing port 约束、计算与通信联合分析 | `5` 个 partitions、`18` 个 periodic + `4` 个 sporadic tasks、`4` 条 `VL` | `UPPAAL SMC` | deadline、sampling port refresh 与 queue overflow 验证 | 安全、统计 falsification、通信时序约束 | 🟢 | 通过 `SMC + MC` 联合分析发现原分区表因 `Msg2` 刷新周期违例不可调度，并用时间片交换修复配置。 | [paper](./han18-dima-schedulability-framework/) |
| ⏱️ | 🚀 | 2018 | `han18metrid` | A Compositional Approach for Schedulability Analysis of Distributed Avionics Systems | `DIMA`, assume-guarantee, message interface, `AFDX` | 同一类 `DIMA` 航电分区系统的组合式可调度性分析 | 用 message interface 抽象通信环境，逐分区验证再合成全局结论 | 同样面向 `5` partitions 与 `4` 条 `VL` 的案例；全局模型约 `51` 个 processes | `UPPAAL` | 分区局部 `A[] not perror[i]` 与全局可调度推导 | 安全、组合式验证、通信时序约束 | 🟡 | 用 assume-guarantee 和 message interface 把原本难以直接验证的航电系统拆成多个可独立证明的分区问题。 | [paper](./han18-dima-schedulability-compositional/) |
| 🛰️ | 🌐 | 2018 | `lu18` | Modeling and Verification of IEEE 802.11i Security Protocol for Internet of Things | IEEE 802.11i, 802.1X, 4-way handshake, DoS | `IEEE 802.11i` 的 `802.1X` 认证与密钥握手流程 | 端口控制、重认证、攻击者注入假消息、关注 `MIC/PTK/GTK` | supplicant/authenticator/server/hacker 多自动机场景；攻击次数阈值实验约 `100` 次 | `UPPAAL` | 端口开闭、死锁自由与握手/组播密钥建立验证 | 安全、活性、攻击相关性质 | 🟡 | 证明 `802.11i` 核心流程在理想条件下无死锁，并揭示 `4-way handshake` 对 `DoS` 和错误 `ANonce` 的脆弱性。 | [paper](./lu18-ieee80211i-security-protocol/) |
| 🧩 | 🌐 | 2018 | `nigro18` | Model Checking Knowledge And Commitments In Multi-Agent Systems Using Actors And UPPAAL | NetBill, commitments, knowledge, actors | `NetBill` 电子交易协议中的 customer/merchant 承诺与知识状态 | actor 归约、异步/定时消息、显式 `PAY/DELIVER` 承诺知识 | 穷尽验证可处理到 `4` agents；更大规模转 `SMC` | `UPPAAL SMC` | 无死锁、承诺履行与双方认知一致性验证 | 安全、活性、知识相关时序性质 | 🟡 | 将 `NetBill` 的承诺与知识状态归约到 `UPPAAL`，证明支付/交付承诺最终会被双方共同知晓并回到初始闭环。 | [paper](./nigro18-netbill-knowledge-commitments/) |
| 🎛️ | 🚦 | 2018 | `schwammberger18` | Introducing Liveness into Multi-lane Spatial Logic lane change controllers using UPPAAL | lane change, MLSL, liveness | 多车道高速公路上的 lane change controller | claim/reserve 机制、潜在碰撞检测、通过等待状态修复 livelock | 核心场景为 `3` 车 `4` 车道；扩到 `4` 车时强活性验证升至约 `1025s` | `UPPAAL` | 变道控制器 safety/liveness 联合验证 | 安全、活性、时序约束 | 🟢 | 用 observer 证明原变道控制器虽安全但不活，随后通过 `q_wait` 修补并回归验证。 | [paper](./schwammberger18-lane-change-controllers/) |
| 🎛️ | 🏥 | 2019 | `alur19` | Continuous-Time Models for System Design and Analysis | pacemaker, hybrid automata, 医疗 `CPS` | 双腔植入式心脏起搏器及其心脏环境模型 | `DDD/VDI` 模式、离散控制器 + 连续心脏、抽象证明 | `8` 个 pacemaker 过程 + `5` 个心脏抽象部件；基础 `DDD` 与 `DDD-VDI` 两种配置 | `UPPAAL` | 上/下速率限制与心跳传播要求验证 | 安全、时序约束、监视器性质 | 🟢 | 先用 `SpaceEx` 证明心脏抽象，再在 `UPPAAL` 中验证 pacemaker 的上下速率限制。 | [paper](./alur19-pacemaker-continuous-time/) |
| ⏱️ | 🚦 | 2019 | `huang19` | Formal Verification of Safety & Security Related Timing Constraints for a Cooperative Automotive System | cooperative automotive, VANET, safety/security timing, PrCcsl | 三车一 `RSU` 的协同汽车系统 | `Raise` 协议、攻击模型、安全与安全性时序耦合 | `3` 辆车 + `1` 个 `RSU`；`R1-R11` 共 `11` 条要求 | `UPPAAL SMC` | 攻击感知的安全/安全性时序约束验证 | 统计性质、安全、真实性/完整性/新鲜度 | 🟡 | 在重放、伪造与欺骗攻击下联合验证 `R1-R11`，展示通信安全失效如何传导成车辆行为风险。 | [paper](./huang19-cooperative-automotive-timing/) |
| 📊 | 🏭 | 2019 | `martinelli19` | Timed Automata Networks for SCADA Attacks Real-Time Mitigation | SCADA, 攻击检测, 燃气管网 | SCADA 燃气管网日志驱动的攻击检测模型 | 日志转自动机、双特征同步、`DoS/MI` 攻击公式 | `269,228` 条测量；`100 ms` 窗口生成 `2,692` 个模型；`1346` 正常 + `1346` 攻击 | `UPPAAL` | 攻击模式可达性判定与检测评估 | 可达性、时序模式、工业安全 | 🟢 | 把 SCADA 日志转成 timed automata 网络，并用 `UPPAAL` 公式检测 `DoS` 与恶意注入攻击。 | [paper](./martinelli19-scada-attack-mitigation/) |
| 🛰️ | 🌐 | 2019 | `raghavan19` | Simulation and Formal Verification of SIP/ZRTP Protocol using UPPAAL | SIP, ZRTP, VoIP, MITM | `SIP/ZRTP` 语音会话建立与密钥协商协议 | `SIP` 预握手、`ZRTP` 发现/确认、`DH` 与 `SAS` 认证 | `Caller` + `SIPServer` + `Callee` `3` 模板，覆盖多类 mismatch 与 `MITM` 断开路径 | `UPPAAL` | 握手正确性与异常断开路径验证 | 安全、活性、可达性 | 🟡 | 用三角色自动机验证 `SIP/ZRTP` 正常握手与多类 mismatch / `MITM` 异常断开行为。 | [paper](./raghavan19-sip-zrtp-protocol/) |
| 🎛️ | 🚦 | 2020 | `basile20` | Strategy Synthesis for Autonomous Driving in a Moving Block Railway System with Uppaal Stratego | railway, moving block, autonomous driving, strategy synthesis | ERTMS Level 3 moving block 信号与自主驾驶抽象系统 | 单列车/单 `RBC`、随机通信延迟、`MA` 安全边界 | `1` train + `1` `RBC` + `1` `OBU` + `1` `LU`；默认 `ma=5`、`arrive=20` | `UPPAAL Stratego` | 安全驾驶策略合成与到达时间优化 | 安全、可达性、统计性质、定量优化 | 🟢 | 用 `Stratego` 合成永不越 `MA` 的驾驶策略，并在安全前提下优化到达时间。 | [paper](./basile20-moving-block-railway-driving/) |
| 🛰️ | 🌐 | 2020 | `bernardeschi20` | Analysis of Security Attacks in Wireless Sensor Networks: From UPPAAL to Castalia | WSN, flooding, drop/tamper, Castalia | 无线传感器网络应用层 flooding 协议 | 源节点 + 中继节点、链路冗余、单次攻击注入 | `1` source + `4` relay；攻击在随机时刻执行 `1` 次 | `UPPAAL` | 协议正确转发与攻击影响分析 | 安全、可达性、攻击场景正确性 | 🟡 | 先在 `UPPAAL` 证明 flooding 性质，再自动转到 Castalia 分析 drop/tamper 攻击后果。 | [paper](./bernardeschi20-wsn-security-castalia/) |
| 🧩 | 🌐 | 2020 | `jamroga20` | Model Checkers Are Cool: How to Model Check Voting Protocols in Uppaal | e-voting, Prêt à Voter, receipt-freeness, coercion | `Prêt à Voter` 电子投票协议 | 多角色协作、知识性质、mix teller 审计与 `OOM` 边界显式可见 | `1-5` 个 voters + coercer / mix tellers / decryption tellers / auditor；`5` voters 已出现 `OOM` | `UPPAAL` | 投票流程与弱 receipt-freeness 验证 | 可达性、知识相关时序性质、审计性质 | 🟡 | 用 `UPPAAL` 建模 `Prêt à Voter` 并通过模型/公式重构近似检查弱 receipt-freeness，同时暴露状态空间边界。 | [paper](./jamroga20-voting-protocols/) |
| 📊 | 🦠 | 2020 | `jensen20` | Fluid Model-Checking in UPPAAL for Covid-19 | Covid-19, SEIHR, fluid model checking, contact tracing | 丹麦 `Covid-19` SEIHR 疫情与场景模型 | 多抽象层级、隔离阶段/家庭作息/超级传播/追踪 app | `10,000` 人基础模型；`30+9,970` fluid；哥本哈根+`5` 场所+`3` 成员；`1,000` 人 tracing | `UPPAAL SMC` | 住院容量、暴露概率、超级传播与追踪策略评估 | 统计性质、概率估计、容量界 | 🟢 | 用 `UPPAAL SMC` 在群体和个体双层场景中分析疫情传播、暴露风险与接触追踪效果。 | [paper](./jensen20-covid19-fluid-model-checking/) |
| 🛰️ | 🌐 | 2020 | `lin20` | Modelling and Verification of Real-Time Publish and Subscribe Protocol Using Uppaal and Simulink/Stateflow | `RTPS`, `DDS`, heartbeat, `ACKNACK` | `DDS/RTPS` writer-reader 发布订阅协议 | 双模型（`Stateflow + UPPAAL`）、不可靠信道、cache 一致性与重传机制 | writer + 多 readers + `WHC/RHC`；代表性样本数组 `[100,200,300,400,500]` | `UPPAAL SMC` | 顺序一致性、heartbeat/repair 正确性与限时传输概率评估 | 安全、统计性能、一致性 | 🟢 | 用 `TCTL` 证明 `RTPS` 一致性与确认机制正确，并用 `SMC` 量化通过率和响应延迟对成功传输概率的影响。 | [paper](./lin20-rtps-simulink-stateflow/) |
| 🛰️ | 🏥 | 2020 | `touijer20` | Scalability Validation of the Posting Access Method through UPPAAL-SMC Model-Checker | `WBAN`, IEEE 802.15.6, posting access method | `IEEE 802.15.6 MAC` 中 hub 侧 posting access method | `poll/post/ack` 交互、随机业务到达、比较 `4/16/64` 节点规模下的伸缩性 | `4/16/64` nodes；`T1/T2/T3=3600/7200/10800`；每组 `10000` 次仿真 | `UPPAAL SMC` | 时隙分配、能耗与吞吐量可扩展性验证 | 统计性能、吞吐、资源消耗 | 🟡 | 用 `UPPAAL SMC` 证明 `WBAN` posting access method 在节点数扩大时仍维持稳定 allocation、energy 与 throughput。 | [paper](./touijer20-posting-access-method/) |
| 🧩 | 🌐 | 2021 | `bakhshi21` | Using UPPAAL to Verify Recovery in a Fault-tolerant Mechanism Providing Persistent State at the Edge | edge computing, persistent state, `RAFT`, recovery | 边缘/雾容器平台中的有状态应用恢复与复制存储机制 | 存储容器、复制数据结构、应用故障和节点故障双层恢复 | 多个 `App/SC` 自动机 + `Node Failure` 自动机 + replicated arrays | `UPPAAL` | 应用恢复、节点恢复、数据可用性与最终一致性验证 | 安全、活性、一致性 | 🟡 | 验证边缘有状态容器机制在应用和节点故障后仍能恢复执行，并保持复制状态最终一致。 | [paper](./bakhshi21-edge-persistent-state-recovery/) |
| 🛰️ | 🚦 | 2021 | `basile21` | Formal Analysis of the `UNISIG` Safety Application Intermediate Sub-layer | railway interface, UNISIG, SAI, handover | 铁路 `RBC/RBC` 接口中的 `SAI` 安全应用中间子层 | 官方标准接口、故障注入、关注安全与互操作性 | initiator/responder 各含 `SAI User`、`SAI`、`Euroradio SL`；附 `Fault Injector` | `UPPAAL SMC` | 标准接口防护逻辑与歧义定位 | 安全、互操作性、统计分析 | 🟢 | 对 `Subset-098` 接口建模并发现自然语言标准中的安全与互操作性缺口，同时公开模型仓库。 | [paper](./basile21-unisig-safety-application-intermediate-sublayer/) |
| 🎛️ | 🚦 | 2021 | `basile21tram` | Analysing an autonomous tramway positioning system with the Uppaal Statistical Model Checker | tramway, `APS`, hazard analysis, railway | 用自主定位系统替代 track circuits 的 tramway 定位与联锁系统 | 位置不确定性、保护级、虚拟标签/轨道电路、degraded mode | 代表性场景含 `1` 个 `OCC`、`1` 个 `IXL`、`2` 辆 tram、`3` 个 `TCV`；共 `27` 条 hazard 性质 | `UPPAAL SMC` | hazard 概率评估与新需求/新风险发现 | 统计风险分析、安全、监督超时 | 🟢 | 用 `UPPAAL SMC` 系统化评估 `27` 个 tramway hazards，并发现自主定位替代传统传感器后引入的新 corner case。 | [paper](./basile21-autonomous-tramway-positioning/) |
| 📊 | 🚦 | 2021 | `bilgram21` | Online and Proactive Vehicle Rerouting with `Uppaal Stratego` | rerouting, SUMO, lemming effect, traffic | 城市路网中的在线集体 rerouting 推荐系统 | 实时交通快照、驾驶员接受概率、`Stratego + SUMO` 闭环 | `25` 个 intersections；horizon `40 s`；接受概率 `0.9`；共 `1000` 组实验 | `UPPAAL Stratego` | 网络级 rerouting 策略学习与效果评估 | 定量优化、统计比较、场景评估 | 🟡 | 用 `Stratego` 为城市路网学习集体分流策略，在无封路和封路场景下分别取得最高约 `31%` 和 `70%` 改善。 | [paper](./bilgram21-online-vehicle-rerouting/) |
| 🛰️ | 🏭 | 2021 | `bujosa20` | CSRP: An Enhanced Protocol for Consistent Reservation of Resources in AVB/TSN | SRP, TSN, AVB, termination, consistency | `AVB/TSN` 网络中的分布式 `SRP/CSRP` 资源预留协议 | talker / listener / bridge 分布式预留、termination 与 consistency 为核心 | `1` 个 talker + `3` 个 bridges + `3` 个 listeners 的 `UPPAAL` 模型 | `UPPAAL` | 协议 termination / consistency 与修补验证 | 终止性、一致性、资源正确性 | 🟢 | 证明标准分布式 `SRP` 在无故障下仍可能等待和浪费资源，并验证改进版 `CSRP` 可恢复 termination 与 consistency。 | [paper](./bujosa20-csrp-avb-tsn/) |
| 🛰️ | 🌐 | 2021 | `feng21` | Modeling and Verification of CKB Consensus Protocol in UPPAAL | CKB, blockchain, two-step confirmation, block propagation | Nervos `CKB` 共识协议 | proposal / commitment 双阶段、miner / full node 分工、缺失交易追问 | `TwoStep` + `MiningNode` + `FullNode` + `BlockPropagation` `4` 自动机；`7` 条性质 | `UPPAAL` | 两步确认与缺失交易处理验证 | 安全、可达性、死锁安全 | 🟡 | 用四自动机验证 `CKB` 两步确认的 proposal / commitment 前置条件，以及缺失交易下的矿工拉黑逻辑。 | [paper](./feng21-ckb-consensus-protocol/) |
| ⏱️ | 🔋 | 2021 | `gamatie21` | Modeling and Analysis for Energy-Driven Computing using Statistical Model-Checking | energy harvesting, energy-neutrality, batteries, distributed systems | 带采能与能量迁移的分布式实时计算系统 | 任务/资源/太阳能板/电池/控制器联动，支持节点间能量共享 | `11` 个任务、`5` 个基础节点，扩展到 `6/8` 节点；`2` 天 Girona 场景 | `UPPAAL SMC` | deadline/energy-neutrality 验证与电池 sizing | 统计性质、deadline 安全、资源定量 | 🟢 | 用 `UPPAAL SMC` 评估最小电池容量，并说明能量共享可显著降低总储能需求。 | [paper](./gamatie21-energy-driven-computing/) |
| 🛰️ | 🏭 | 2021 | `guo21` | A Formal Method for Evaluating the Performance of TSN Traffic Shapers using UPPAAL | TSN, TAS, preemption, latency | `TSN` 交换节点中的流量整形器 | `ST/BE` 双类流量、window automata、抢占机制对比 | `100 Mbps`；`ST 128B/200μs`、`BE 256B/125μs`；`TAS` 周期 `500μs` | `UPPAAL` | shaping 规则与低时延性质验证 | 安全、活性、时延、可达性 | 🟢 | 证明不带抢占的 `TAS/PS` 难以满足低时延要求，而抢占能同时改善时延和利用率。 | [paper](./guo21-tsn-traffic-shapers/) |
| 🎛️ | 🤖 | 2021 | `holler21` | Strategising RoboCup in Real Time with Uppaal Stratego | RoboCup, 实时策略生成, 多智能体 | RoboCup 2D 足球仿真中的多智能体实时策略生成系统 | `100ms` tick、部分可观测、在线预测与离线查表混合 | `4` 个局部策略模型；包含 `100` 次攻门实验与 `40` 场完整比赛评估 | `UPPAAL Stratego` | 实时策略生成与收益评估 | 定量优化、统计比较、实时可用性 | 🟡 | 用 `Stratego` 在 RoboCup `100ms` 决策窗口内生成局部策略，并在守门和体力管理上取得统计改进。 | [paper](./holler21-robocup-stratego/) |
| 🧩 | 🌐 | 2021 | `kunnappilly21` | From UML Modeling to UPPAAL Model Checking of 5G Dynamic Service Orchestration | 5G slicing, UML, service orchestration, VNF | `5G` 动态服务编排与 network slicing 场景 | 共享 `VNF`、动态请求、`UML` 到 `UPPAAL` 的自动翻译 | `3` 个 health `UE` + `2` 个 video `UE`；`4` hosts；health `v1-v2`、video `v1-v3-v4-v5` | `UPPAAL` | SLA/时延与最终服务性验证 | 可达性、leads-to、不变式 | 🟡 | 把 `UML` 状态图翻译成 `UPPAAL` 模型，验证关键切片请求的时限与最终服务性。 | [paper](./kunnappilly21-5g-service-orchestration/) |
| 📊 | 🚦 | 2021 | `meng21` | Analysis of ATO System Operation Scenarios Based on UPPAAL and the Operational Design Domain | ATO, ODD, scenario analysis, platform door | 高铁 `ATO` 车门与站台门联动控制场景 | `ODD` 驱动、接口映射、需求抽取导向 | `ATP` + train + onboard `ATO` + `TSRS` `4` 模块；表 4 / 5 对应验证与需求参数 | `UPPAAL` | 场景验证与需求参数抽取 | 场景一致性、有界响应、接口正确性 | 🟡 | 用 `ODD` 和 `UPPAAL` 验证车门 / 站台门联动场景，并把通过的场景模型回写为车载 `ATO` 需求参数。 | [paper](./meng21-ato-operation-scenarios/) |
| 🎛️ | 🚦 | 2021 | `thamilselvam21` | Scalable Coordinated Intelligent Traffic Light Controller for Heterogeneous Traffic Scenarios Using UPPAAL Stratego | traffic lights, hierarchical control, Stratego, heterogeneous traffic | Ahmedabad `23` 路口交通灯协调系统 | `ILTAN + ALTAN` 双层控制、`4` 类车辆、`SUMO` 在线闭环 | `23` 个交叉口、`4` 相位、`1200s` 仿真、`4` 类车辆 | `UPPAAL Stratego` | 相位控制综合与延迟/排放评估 | 定量优化、吞吐、排放、延迟 | 🟢 | 在城市级路网中合成双层交通灯策略，显著降低等待时间与排放。 | [paper](./thamilselvam21-traffic-light-controller/) |
| 🎛️ | 🚦 | 2022 | `basile22` | Exploring the ERTMS/ETCS full moving block specification: An experience with formal methods | `ERTMS/ETCS`, moving block, `RBC`, formal methods | `ERTMS/ETCS Level 3` full moving block 中的 train/`OBU`/`RBC` 协同控制 | 多列车共享 `RBC`、动态 `MA` 计算、通信延迟与并发共享状态 | 参数化 train/`RBC`/`OBU`/`LU` 模型；重点分析 `1-3` 列车场景 | `UPPAAL SMC` | freshness、message loss、`MA` 正确性与越权风险验证 | 安全、不变式、统计风险分析 | 🟢 | 在多列车 `RBC` 模型中发现 freshness、message-loss 与 `MA` 过期问题，并验证默认参数下约 `1` 分钟 headway 安全。 | [paper](./basile22-ertms-full-moving-block/) |
| 🎛️ | 🤖 | 2022 | `gu22` | Verifiable strategy synthesis for multiple autonomous agents: A scalable approach | autonomous agents, mission planning, quarry, reinforcement learning | autonomous quarry 中多代理路径规划与任务调度系统 | timed games + `RL` + post-verification；代理数增大时状态空间急剧膨胀 | 重点比较 `3-6` agents；另有 `2` agents 下 `5/8/10` milestones/tasks 实验 | `UPPAAL Stratego` | mission plan 综合与学习后策略验证 | 安全、有界活性、顺序约束 | 🟡 | 将 `RL` 与模型检查结合到 quarry 多代理 mission planning，把可处理规模从 `5` 个代理推进到 `6` 个。 | [paper](./gu22-multi-agent-strategy-synthesis/) |
| 🎛️ | 🏥 | 2022 | `lehmann22` | Modeling R^3 Needle Steering in Uppaal | needle steering, medical CPS, obstacle avoidance, online strategy synthesis | 软组织中的 steerable needle 在线导航系统 | `TR/CR/DR` 区域建模、在线重综合、`R^3 -> Z^3` 抽象 | `5` 类环境；虚拟针 `50` 次/设置、真实针 `5-7` 次/设置；`120s` 超时 | `UPPAAL Stratego` | 安全到靶与在线重规划验证 | 安全、可达性、性能 | 🟢 | 用 `Stratego` 进行针导航在线策略综合，在真实针实验中保持 `0%` 关键区命中。 | [paper](./lehmann22-r3-needle-steering/) |
| 🎛️ | 🎵 | 2023 | `chen23` | `IoT` Modeling and Verification: From the `CaIT` Calculus to `UPPAAL` | IoT, CaIT, smart home, broadcast | 基于 `CaIT` 描述的 smart home `IoT` 系统 | 先有过程演算规范，再翻译到 timed automata；支持 mobility 与 broadcast | entrance/patio/lounge 三位置；`2` lights、`2` windows、`1` boiler、`1` phone | `UPPAAL` | `IoT` 控制规则验证与形式语言桥接 | 安全、时序性质、并发一致性 | 🟡 | 把扩展 `CaIT` smart home 规范映射到 `UPPAAL`，并验证 boiler、lights、windows 的 `6` 条性质。 | [paper](./chen23-cait-iot-uppaal/) |
| 🎛️ | 🏥 | 2023 | `cuartas23` | Formal Verification of a Mechanical Ventilator using UPPAAL | ventilator, medical device, valve control, flow | 机械呼吸机控制架构 | `Setup/Control/Injector/ExpValve` 四自动机、简化流体模型、符号 + `SMC` 混合验证 | `4` 个 automata；流量 `10-50 L/min`；`FiO2 10-100%`；时序 `100-300 cs` | `UPPAAL` | 阀门协调、时序与流量行为验证 | 安全、可达性、统计性质、定量分析 | 🟢 | 验证呼吸机控制与阀门互锁逻辑，并用模型分析更优采样周期。 | [paper](./cuartas23-mechanical-ventilator/) |
| ⏱️ | 🏭 | 2023 | `muhammad23` | Modelling and Analysis of a Sigfox-Based `IoT` Network Using `UPPAAL SMC` | Sigfox, IoT, battery lifetime, water monitoring | 排水管网水位监测用 `Sigfox` 节点与网络寿命分析模型 | 真实硬件测量校准、部署点难维护、比较多种上传策略 | 代表性电池 `10000 mAh`；寿命从 `202` 天到 `2.71` 年 | `UPPAAL SMC` | 节点寿命评估与能耗瓶颈分析 | 统计性质、资源定量、策略比较 | 🟢 | 用 `UPPAAL SMC` 量化不同传输策略对节点寿命的影响，并发现测量链路最多可占约 `57%` 能耗。 | [paper](./muhammad23-sigfox-iot-network/) |
| 🧩 | 🎓 | 2024 | `zhou24` | Ensuring Reliability in Electronic Examinations Through UPPAAL-Based Trustworthy Design | electronic examination, workflow, cheating detection, trustworthy design | 电子考试流程系统 | 四角色协作、操作队列、答案相似度防作弊 | 示例为 `2` 名考生、`3` 道题、`12` 条性质；`MaxT=1000` | `UPPAAL` | 流程可靠性与规则一致性验证 | 安全、完整性、活性、防作弊 | 🟡 | 用 `UPPAAL` 模型检查电子考试中的注册、提交、阅卷、通知与作弊检测规则。 | [paper](./zhou24-electronic-examinations/) |
| ⏱️ | 🤖 | 2025 | `backeman25` | Verifying ROS-Based Applications Using Timed and Stochastic Timed Automata | ROS 2, reaction time, stochastic timed automata, industrial robots | 相机引导工业机器人任务链 | probabilistic load、端到端 reaction time、timer/subscription fusion 比较 | cameras + object detection + fusion + actuation；表 4 给出 `Camera/Object Detection/Fusion/Actuation` 参数 | `UPPAAL SMC` | 最大 reaction time 与 deadline 风险分析 | 有界响应、统计性质、性能分析 | 🟢 | 用 timed / stochastic timed automata 量化 camera 数和负载对工业 `ROS` 任务链 `850` deadline 的影响。 | [paper](./backeman25-ros-timed-stochastic/) |
| ⏱️ | 🤖 | 2025 | `dust25` | Pattern-based verification of ROS 2 applications using UPPAAL | ROS 2, executor, callback latency, buffer overflow | `ROS 2` executor / callback 处理链与通信缓冲行为 | pattern-based 模板、`ExV1/ExV2`、holistic / individual 双建模方式 | `SC1-SC3` 三场景；三类 callback 模板 + executor / topic 模板 | `UPPAAL` | callback latency 与输入/输出缓冲溢出验证 | 有界响应、overflow 安全、调度正确性 | 🟢 | 用 pattern-based 模板验证 `ROS 2` callback latency 与缓冲溢出，并指出 `ExV2` 下的 timer instance miss 与“低延迟假象”。 | [paper](./dust25-pattern-based-ros2-applications/) |
| ⏱️ | 🏭 | 2025 | `soltani25` | Optimal spare management via statistical model checking: A case study in research reactors | spare management, research reactor, fault tree, cost optimization | 研究反应堆 emergency shutdown system 的备件库存决策 | `fault tree -> SPTGA`，rare events 对最优策略影响显著 | 单组件最优 `6` 个 spares；双组件最优 `6 + 140`；寿命周期 `40` 年 | `UPPAAL Stratego` | 最优备件数、availability 与 downtime 风险分析 | 策略综合、统计成本、rare-event 概率 | 🟢 | 将备件管理转为 `Stratego` 优化问题，并求得单组件 `6` 与双组件 `6+140` 的最优配置。 | [paper](./soltani25-spare-management-research-reactors/) |
| 🧩 | 🌐 | 2026 | `basile26` | Formal Analysis of the Contract Automata Runtime Environment with Uppaal: Modelling, Verification and Testing | contract automata, middleware, sockets, model-based testing | `CARE` 分布式中间件的 orchestrator/services 运行时交互 | 抽象模型直接连到源码、`Yggdrasil` 测试生成、关注缓冲与超时语义 | orchestrator + 多 services + timeout automata；源码约 `770` 行且与模型可追踪对照 | `UPPAAL` | termination、deadlock、orphan message 与 compatibility 验证 | 安全、活性、模型驱动测试 | 🟢 | 把 `CARE` 从模型检查延伸到 `JUnit` 级测试，并借此发现和修复 non-blocking socket 假设引入的死锁问题。 | [paper](./basile26-contract-automata-runtime-environment/) |

## 案例/模型/数据公开性清单

| 论文 | 状态 | 案例/模型/数据 | 来源类型 | 制作/来源方式 | 可获取性 | 获取方式/链接 | 简述 |
|---|---|---|---|---|---|---|---|
| [bengtsson96](./bengtsson96-audio-protocol-bus-collision/desc.md) | 🟢 | Philips 音频协议 timed automata 案例 | 工业协议案例（历史 benchmark 入口） | 论文正文 + 官方 benchmark 历史条目 `philaudio` | 🟠 | [DOI](https://doi.org/10.1007/3-540-61474-5_73)；[UPPAAL Benchmarks](https://uppaal.org/benchmarks/) | benchmark 页仍可见案例名，但当前公开直链已失效 |
| [jensen96](./jensen96-collision-avoidance-protocol/desc.md) | 🟢 | 冲突避免轮询协议模型 | 协议案例 | BRICS 报告正文重建 | 🟠 | [DOI](https://doi.org/10.7146/brics.v3i24.20005)；[BRICS PDF](https://tidsskrift.dk/brics/article/download/20005/17638) | 论文公开，但无独立 `UPPAAL` 模型包 |
| [dargenio97](./dargenio97-bounded-retransmission-time/desc.md) | 🟢 | BRP 协议模型 | 协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1007/BFb0035403) | 原文未提供独立模型包或仓库 |
| [lonn97](./lonn97-tdma-startup-mechanism/desc.md) | 🟢 | DACAPO 启动同步模型 | 协议案例 | 论文正文重建 | 🟠 | [论文 PDF](https://uppaal.org/texts/lp-prfts97.pdf) | 论文可得，但无独立模型入口 |
| [havelund97](./havelund97-audio-video-protocol/desc.md) | 🟢 | B&O 音视频协议工业案例 | 工业实现案例 | 工业实现 + 论文描述 + 官网案例页 | 🔒 | [DOI](https://doi.org/10.1109/REAL.1997.641264)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 真实资产来自工业实现，论文未公开完整模型与原始协议资产 |
| [bowman98](./bowman98-lip-synchronisation-algorithm/desc.md) | 🟢 | lip sync 算法模型 | 学术算法案例 | 论文正文重建 | 🟠 | [论文 PDF](https://uppaal.org/texts/bfklm-fimcs98.pdf) | 无独立模型/输入流数据包 |
| [lindahl98](./lindahl98-gear-controller/desc.md) | 🟢 | gear controller 与环境模型 | 工业控制案例 | 工业合作需求 + 论文描述 | 🔒 | [DOI](https://doi.org/10.1007/BFb0054178) | 控制器需求与环境资产来自工业项目，难以直接公开取得 |
| [havelund99](./havelund99-power-controller/desc.md) | 🟢 | power controller 历史模型 `bopdp` / `bopdpFIXED` | 工业控制案例（历史 benchmark 入口） | 论文正文 + 官方 benchmark 历史条目 | 🟠 | [DOI](https://doi.org/10.7146/BRICS.V6I8.20065)；[UPPAAL Benchmarks](https://uppaal.org/benchmarks/) | benchmark 页仍记有模型名，但当前公开直链已失效 |
| [iversen99](./iversen99-lego-mindstorms-systems/desc.md) | 🟢 | LEGO `RCX` 颜色分拣控制程序模型 | 机器人控制案例 | BRICS 报告正文 + 程序语义重建 | 🟠 | [DOI](https://doi.org/10.7146/brics.v6i53.20123)；[BRICS PDF](https://tidsskrift.dk/brics/article/download/20123/17745) | 论文公开，但 `rcx2uppaal` 与案例模型未独立发布 |
| [david00](./david00-commercial-field-bus-protocol/desc.md) | 🟢 | AF100 bus coupler 案例 | 工业协议案例 | ABB 工业规格/实现 + 论文抽象 | 🔒 | [DOI](https://doi.org/10.1109/EMRTS.2000.854004) | 案例依赖商业协议规格与实现资产，原文未公开模型包 |
| [hune00](./hune00-batch-plant-control-synthesis/desc.md) | 🟢 | `SIDMAR` batch plant 模型与 `LEGO` 验证平台流程 | 工业控制综合案例 | BRICS 报告正文 + 物理 plant 描述重建 | 🟠 | [DOI](https://doi.org/10.7146/brics.v7i37.20203)；[BRICS PDF](https://tidsskrift.dk/brics/article/download/20203/17817) | 论文可得，但未公开独立 `UPPAAL` 模型、综合脚本或 `LEGO` 控制程序 |
| [bordbar03](./bordbar03-timeliness-qos-multimedia/desc.md) | 🟡 | video player + QTA 示例 | 方法示例案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1007/978-3-540-39893-6_30) | 方法公开，但无独立 QTA 工具实现或示例模型包 |
| [pang03](./pang03-distributed-lift-system-redesign/desc.md) | 🟢 | distributed lift system 协同控制案例 | 工业控制案例 | 论文正文 + 真实工业案例描述重建 | 🟠 | [DOI](https://doi.org/10.1007/978-3-540-39893-6_29)；[公开 PDF](https://www.cs.vu.nl/~wanf/pubs/redesign.pdf) | 论文可得，但未提供独立 `UPPAAL` 模型、查询文件或工业案例资产下载入口 |
| [rodrigueznavas05](./rodrigueznavas05-can-clock-synchronization/desc.md) | 🟡 | `CAN` 时钟同步协议模型 | 车载通信协议案例 | 论文正文 + 协议机制描述重建 | 🟠 | [DOI](https://doi.org/10.1109/ETFA.2005.1612717)；[公开 PDF](https://fileadmin.cs.lth.se/ai/Proceedings/etfa2005/html/articles/CF-002899.pdf) | 论文可公开获取，但未附独立 `UPPAAL` 模型包或稳定工件入口 |
| [gebremichael06](./gebremichael06-zeroconf-link-local-addresses/desc.md) | 🟢 | Zeroconf 完整模型、抽象模型与查询文件 | 协议案例（作者专题页） | 论文 + 作者专题页工件 | 🟢 | [专题页面](https://sws.cs.ru.nl/publications/papers/fvaan/zeroconf/)；[完整模型](https://sws.cs.ru.nl/publications/papers/fvaan/zeroconf/zeroconffull.xml)；[查询文件](https://sws.cs.ru.nl/publications/papers/fvaan/zeroconf/zeroconf.q) | 论文、模型、抽象版与查询均可直接获取，是高公开度经典协议案例 |
| [vaandrager06](./vaandrager06-biphase-mark-protocol/desc.md) | 🟢 | BMP 参数化协议模型说明 | 协议案例 | 技术报告 PDF + 作者专题页 | 🟠 | [DOI](https://doi.org/10.1007/s00165-006-0008-1)；[BMP 页面](https://sws.cs.ru.nl/publications/papers/fvaan/BMP.html)；[报告 PDF](https://sws.cs.ru.nl/publications/papers/fvaan/BMP/paper.pdf) | 论文和案例说明公开，但未找到独立 `UPPAAL` 模型下载入口 |
| [jessen07](./jessen07-climate-controller-tiga/desc.md) | 🟢 | pig stable 气候控制 `Tiga` 案例 | 工业控制综合案例 | 论文 + `Tiga` 项目页 | 🔒 | [论文 PDF](https://homes.cs.aau.dk/~adavid/publications/30-casestudy.pdf)；[Tiga 项目页](https://homes.cs.aau.dk/~adavid/tiga/) | 论文与工具页公开，但工业 pig stable 模型和真实数据未单独公开 |
| [mekking07](./mekking07-shim6-internet-standard/desc.md) | 🟡 | `SHIM6` 握手与重传模型 | Internet 协议草案案例（历史作者页） | IETF 草案文本 + symposium 短文 + 历史模型页 | 🟠 | [Handle](https://hdl.handle.net/2066/34748)；历史模型页 `https://sws.cs.ru.nl/publications/papers/fvaan/SHIM6/UPPAAL` | 论文可得，但历史模型入口当前返回 `404`，更适合作为草案歧义验证样本 |
| [braspenning08](./braspenning08-chi-industrial-case-study/desc.md) | 🟢 | `Chi/UPPAAL` 工业协同控制案例 | 工业设备控制案例 | ASML 设计文档 + 论文正文 + TU/e 开放 PDF | 🟠 | [DOI](https://doi.org/10.1016/j.compind.2007.06.002)；[TU/e PDF](https://pure.tue.nl/ws/files/3336674/642387.pdf) | 论文与开放版本可得，但未见独立 `Chi`/`UPPAAL` 模型包 |
| [mudaliar08](./mudaliar08-flexray-membership-protocol/desc.md) | 🟢 | `FlexRay` membership 协议模型 | 车载协议案例 | 学位论文正文重建 | 🟠 | [K-State 页面](https://krex.k-state.edu/items/701856ac-59b2-4108-b517-d3d4b2a953e8) | 学位论文可公开获取，但未提供独立 `UPPAAL` 工程文件 |
| [xu08](./xu08-comdes-ii-systems/desc.md) | 🟡 | COMDES-II turntable 转换验证案例 | 组件化控制案例 | 开放版 PDF + 论文描述重建 | 🟠 | [DOI](https://doi.org/10.1109/RTCSA.2008.32)；[SDU PDF](https://findresearcher.sdu.dk/ws/portalfiles/portal/3637/Verification_of_COMDES-II_Systems_Using_UPPAAL_with_Model_Transformation_normalsize.pdf) | 转换思路公开，但未见 turntable 模型或工具链下载入口 |
| [alattili09](./alattili09-adaptive-scheduling-data-paths/desc.md) | 🟢 | Océ pipeline `Tiga` 模型与扩展包 | 工业调度案例（作者模型页） | 论文 + `TigaOce` 项目页工件 | 🟢 | [模型页](https://mbsd.cs.ru.nl/publications/papers/fvaan/TigaOce/)；[基础模型](https://mbsd.cs.ru.nl/publications/papers/fvaan/TigaOce/new_model.xml)；[扩展模型](https://mbsd.cs.ru.nl/publications/papers/fvaan/TigaOce/ExtendedModel.zip) | 当前可直接获取基础与扩展模型，是高公开度工业调度案例 |
| [ravn10](./ravn10-web-services-atomic-transaction/desc.md) | 🟡 | WS-AT `UPPAAL` 模型（历史 `rvs10.zip`） | 软件协议案例（历史 case-study 入口） | 论文正文 + 官网案例页历史链接 | 🟠 | [DOI](https://doi.org/10.1007/978-3-642-16558-0_47)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 官网仍提历史压缩包，但当前公开链接返回 `404` |
| [xing10](./xing10-rapidio-network/desc.md) | 🟢 | RapidIO 工业网络性能模型 | 工业嵌入式通信案例 | POOSL 性能模型 + 论文描述 | 🟠 | [UTwente PDF](https://ris.utwente.nl/ws/portalfiles/portal/5301883/uppaal_in_practice_ISOLA2010.pdf) | 论文公开，但未提供独立 `UPPAAL` 模型包或流量工件 |
| [mikucionis10](./mikucionis10-herschel-planck-case-study/desc.md) | 🟢 | Herschel-Planck 调度模型 | 航天调度案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [模型目录](https://github.com/DEIS-Tools/uppaal-models/tree/main/CaseStudies/HerschelPlanck2010)；[HerschelEvents2.xml](https://raw.githubusercontent.com/DEIS-Tools/uppaal-models/main/CaseStudies/HerschelPlanck2010/HerschelEvents2.xml) | 当前可直接获取论文、模型和查询 |
| [belmokadem10](./belmokadem10-timed-multitask-system/desc.md) | 🟢 | Bosch MSS station 2 PLC 案例 | 工业 PLC 案例 | 论文正文 + HAL 版本 | 🟠 | [HAL 页面](https://hal.science/hal-00527736) | 论文可获取，但站点模型、PLC 源程序和 `UPPAAL` 工程未公开 |
| [ravn11](./ravn11-web-services-business-activity/desc.md) | 🟢 | `BAwCC` 协议模型（历史 `rsv-tacas11.zip`） | 软件协议案例（历史 case-study 入口） | 论文正文 + 官网历史链接 | 🟠 | [论文 PDF](https://uppaal.org/texts/rsv-tacas11.pdf)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 论文可得，但历史模型压缩包当前返回 `404` |
| [lee11](./lee11-radiation-therapy-system/desc.md) | 🟡 | 放疗补偿控制系统模型 | 医疗控制案例 | 论文结构描述重建 | 🟠 | [论文 PDF](http://www.kevin-lee.co.uk/work/research/KLMKrilaviciusEtAl_ISPA2011.pdf) | 仅论文公开，无独立模型或数据包 |
| [arry12](./arry12-device-discovery-mechanism/desc.md) | 🟡 | Bluetooth discovery 双节点模型 | 通信发现机制案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.5120/9392-3816)；[论文 PDF](https://research.ijcaonline.org/volume58/number19/pxc3883816.pdf) | 论文可得，但未提供独立模型工程或实验脚本 |
| [david12](./david12-herschel-planck-smc/desc.md) | 🟢 | Herschel-Planck `SMC` 调度模型 | 航天调度案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [Herschel-SMC2.xml](https://github.com/DEIS-Tools/uppaal-models/blob/main/CaseStudies/HerschelPlanck2012/Herschel-SMC2.xml) | 当前可直接拿到 `UPPAAL SMC` 案例模型 |
| [fehnker12](./fehnker12-aodv-uppaal/desc.md) | 🟢 | AODV `UPPAAL` 协议模型 | 协议案例 | RFC + AWN 形式化规范 + 论文描述 | 🟠 | [DOI](https://doi.org/10.1007/978-3-642-28756-5_13) | 论文公开，但稳定模型下载入口未确认，历史 AWN 报告入口当前不可达 |
| [jiang12](./jiang12-dual-chamber-pacemaker/desc.md) | 🟢 | pacemaker 闭环模型（历史 `PM_verify.zip` 入口） | 医疗设备案例（历史作者链接） | 论文 + 规格描述 + 历史 `UPenn` 链接 | 🟠 | [DOI](https://doi.org/10.1007/978-3-642-28756-5_14)；[历史模型链接](https://www.seas.upenn.edu/~zhihaoj/VHM/PM_verify.zip) | 论文可得，但文中给出的历史模型压缩包当前返回 `404` |
| [bourke13](./bourke13-embedded-sensor/desc.md) | 🟢 | `GP2D02` 传感器 timing diagram、split model 与汇编驱动案例 | 嵌入式设备案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1145/2539036.2539040)；[HAL PDF](https://inria.hal.science/hal-00909062/document) | 论文公开，但未提供独立模型、tester 自动机或汇编程序仓库 |
| [gruhn13](./gruhn13-health-monitoring-driver-assistance/desc.md) | 🟡 | 健康监测驾驶辅助系统验证框架 | 医疗车载 `CPS` 案例 | 论文框架描述 | 🟠 | [DOI](https://doi.org/10.4108/icst.pervasivehealth.2013.252091) | 无公开 `UPPAAL` 模型、`π`-演算规范或案例数据 |
| [malik13](./malik13-iccp-communication-checkers/desc.md) | 🟡 | `ICCP` checker 设计案例 | 关键基础设施协议安全案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1109/SMARTGRIDCOMM.2013.6688005)；[论文 PDF](https://www.perform.illinois.edu/Papers/USAN_papers/13MAL02.pdf) | 论文公开，但未提供 `UPPAAL` 模型、checker 规则文件或流量数据 |
| [ma14](./ma14-laser-tracheotomy-case-study/desc.md) | 🟡 | laser tracheotomy 在线 `SMC` 模型与 patient trace 实验 | 医疗在线验证案例 | 论文正文 + `PhysioNet` trace 描述 | 🟠 | [DOI](https://doi.org/10.4230/OASIcs.MCPS.2014.100)；[Dagstuhl PDF](https://drops.dagstuhl.de/storage/01oasics/oasics-vol036-medcps2014/OASIcs.MCPS.2014.100/OASIcs.MCPS.2014.100.pdf) | 论文公开，但未提供完整 `UPPAAL SMC` 模型和在线适配脚本 |
| [nakatani14](./nakatani14-line-tracing-robot/desc.md) | 🟡 | 循线机器人二维离散轨道模型 | 机器人运动案例 | 论文正文与轨道数组定义重建 | 🟠 | [Atlantis Press PDF](https://www.atlantis-press.com/article/13628.pdf) | 论文可得，但未提供独立 `UPPAAL` 模型或轨道脚本仓库 |
| [dai15](./dai15-multiprocessor-realtime-schedulability/desc.md) | 🟡 | 多处理器实时任务系统可调度性模板 | 调度分析案例 | 论文正文 + `GSM/GSM+MP3` 任务集参数重建 | 🟠 | [论文页面](http://www.jos.org.cn/1000-9825/4781.htm)；[PDF](https://www.jos.org.cn/josen/article/pdf/4781) | 论文与网页可公开获取，但未给出 `UPPAAL` 模型、任务配置文件或查询文件下载入口 |
| [ahmad16](./ahmad16-energy-optimal-dataflow-controllers/desc.md) | 🟡 | `MPEG-4` 数据流能耗控制案例 | 资源优化案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1007/978-3-319-47166-2_7)；[UTwente PDF](https://ris.utwente.nl/ws/files/515556506/Main.pdf) | 论文公开，但未提供稳定模型仓库或实验脚本 |
| [cho17](./cho17-can-database-verification/desc.md) | 🟡 | `CAN` database 自动验证案例 | 车载通信配置案例 | `DBC` 文件到模型的论文级转换流程 | 🟠 | [DOI](https://doi.org/10.7763/IJCTE.2017.V9.1182)；[论文 PDF](https://www.ijcte.org/vol9/1182-AE009.pdf) | 论文公开，但 `DBC2XML` 工具和示例 `DBC` 未见稳定仓库 |
| [halder17](./halder17-ros-robotic-applications/desc.md) | 🟢 | `Kobuki` `ROS` 通信/调度案例 | 机器人中间件案例 | 论文正文 + `Kobuki` 代码结构描述 | 🟠 | [DOI](https://doi.org/10.1109/FORMALISE.2017.9)；[公开 PDF](https://repositorium.sdum.uminho.pt/bitstreams/c15d9b06-0fba-4f8b-bf80-8f16f7454ebf/download) | 论文公开，但未给独立 `UPPAAL` 模型或实验配置包 |
| [saini17](./saini17-sctp-uppaal/desc.md) | 🟢 | TCP/SCTP 握手安全模型 | 协议安全案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.4204/EPTCS.244.1)；[arXiv PDF](https://arxiv.org/pdf/1703.06568) | 论文公开，但未见独立 `UPPAAL` 模型仓库 |
| [han18mars](./han18-dima-schedulability-framework/desc.md) | 🟢 | `DIMA` 航电系统可调度性框架 | 航电调度案例 | 论文正文 + `ARINC-653/AFDX` 参数表重建 | 🟠 | [DOI](https://doi.org/10.4204/EPTCS.268.5)；[PDF](https://arxiv.org/pdf/1803.11050.pdf) | 论文公开，但脚注中的模型入口并未形成稳定、清晰的公开工件下载链路 |
| [han18metrid](./han18-dima-schedulability-compositional/desc.md) | 🟡 | 组合式 `DIMA` 分区可调度性模型 | 航电调度案例 | 论文正文 + message interface 抽象重建 | 🟠 | [DOI](https://doi.org/10.4204/EPTCS.272.4)；[PDF](https://cgi.cse.unsw.edu.au/~eptcs/paper.cgi?MeTRiD2018.4.pdf) | 论文公开，但未给出稳定公开的消息接口模板或完整模型工程 |
| [lu18](./lu18-ieee80211i-security-protocol/desc.md) | 🟡 | `IEEE 802.11i` 认证与握手模型 | 无线安全协议案例 | 论文正文 + 标准流程与攻击场景重建 | 🟠 | [DOI](https://doi.org/10.1142/S021819401840020X)；[会议 PDF](https://ksiresearch.org/seke/seke18paper/seke18paper_60.pdf) | 论文公开，但未提供 `UPPAAL` 模型或攻击场景工程下载入口 |
| [nigro18](./nigro18-netbill-knowledge-commitments/desc.md) | 🟡 | `NetBill` actor 承诺/知识模型 | 业务协议案例 | 论文正文 + actor 语义与承诺状态重建 | 🟠 | [DOI](https://doi.org/10.7148/2018-0136)；[会议 PDF](https://www.scs-europe.net/dlib/2018/ecms2018acceptedpapers/0136_is_ecms2018_0856.pdf) | 论文公开，但未见 actor 模型、`UPPAAL` 工程或查询文件公开仓库 |
| [schwammberger18](./schwammberger18-lane-change-controllers/desc.md) | 🟢 | 多车道变道控制器与 observer | 交通控制案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.4204/EPTCS.269.3)；[arXiv PDF](https://arxiv.org/pdf/1804.04346) | 论文公开，但未提供稳定模型仓库；复跑仍需按文中定义重建 |
| [alur19](./alur19-pacemaker-continuous-time/desc.md) | 🟢 | pacemaker `UPPAAL` 模型 | 医疗设备案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [pacemaker.xml](https://github.com/DEIS-Tools/uppaal-models/blob/main/CaseStudies/Pacemaker2019/pacemaker.xml) | 当前可直接获取模型文件，适合复跑与二次分析 |
| [huang19](./huang19-cooperative-automotive-timing/desc.md) | 🟡 | cooperative automotive timing 约束模型与 `ProTL` 入口 | 车联网时序/安全性案例 | 论文 + `ProTL` 工具页 | 🟠 | [DOI](https://doi.org/10.1007/978-3-030-16722-6_12)；[ProTL 页面](https://sites.google.com/view/protl) | 工具页可访问，但完整 `CAS` 案例模型仓库未确认 |
| [martinelli19](./martinelli19-scada-attack-mitigation/desc.md) | 🟢 | SCADA 燃气管网日志数据集 + 攻击公式 | 工业安全数据案例 | UAH ICS 公开数据集 + 论文公式构造 | 🟢 | [数据集页面](https://sites.google.com/a/uah.edu/tommy-morris-uah/ics-data-sets)；[Raw Data Gas Pipeline](http://www.ece.uah.edu/~thm0009/icsdatasets/gas_final.arff)；[数据缺陷报告](http://www.ece.uah.edu/~thm0009/icsdatasets/MSU_SCADA_Final_Report.pdf) | 数据可直接获取，但源页已明确说明该批数据存在已知缺陷 |
| [raghavan19](./raghavan19-sip-zrtp-protocol/desc.md) | 🟡 | `SIP/ZRTP` 三角色协议模型 | `VoIP` 协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.35940/IJRTE.B1029.0982S1119)；[论文 PDF](https://www.ijrte.org/wp-content/uploads/papers/v8i2S11/B10290982S1119.pdf) | 论文公开，但未见独立 `UPPAAL` 模型仓库 |
| [basile20](./basile20-moving-block-railway-driving/desc.md) | 🟢 | moving block 铁路 `Stratego` 模型与实验 | 铁路控制案例（作者仓库） | 论文 + 作者 `GitHub` 仓库 | 🟢 | [FORTE2020 仓库](https://github.com/davidebasile/FORTE2020) | 当前可直接获取模型与实验脚本，是较少见的公开 `Stratego` 铁路案例 |
| [bernardeschi20](./bernardeschi20-wsn-security-castalia/desc.md) | 🟡 | WSN flooding 协议模型与 `UPPAAL->Castalia` 原型 | 协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.5220/0009380508150824)；[论文 PDF](https://www.scitepress.org/Papers/2020/93805/93805.pdf) | 论文公开，但无稳定模型仓库或桥接脚本下载入口 |
| [jamroga20](./jamroga20-voting-protocols/desc.md) | 🟡 | `Prêt à Voter` 多角色投票模型 | 投票流程案例 | arXiv 论文正文重建 | 🟠 | [DOI](https://doi.org/10.48550/arXiv.2007.12412)；[arXiv PDF](https://arxiv.org/pdf/2007.12412) | 论文公开，但未确认独立 `UPPAAL` 模型工件 |
| [jensen20](./jensen20-covid19-fluid-model-checking/desc.md) | 🟢 | `Covid-19` 流体/随机/追踪模型 | 公共健康场景（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [Covid-19 模型目录](https://github.com/DEIS-Tools/uppaal-models/tree/main/CaseStudies/Covid-19) | 当前可直接获取疫情场景模型，是少数公开的 `UPPAAL SMC` 公共健康案例 |
| [lin20](./lin20-rtps-simulink-stateflow/desc.md) | 🟢 | `RTPS` 协议的 `UPPAAL/Stateflow` 双模型 | 发布订阅协议案例 | 论文正文 + 扩展版模型描述重建 | 🟠 | [DOI](https://doi.org/10.1007/S11390-020-0537-8)；[扩展 PDF](https://lcs.ios.ac.cn/~bzhan/jcst20extended.pdf) | 论文和扩展版 PDF 可公开获取，但未见稳定模型仓库、`Stateflow` 工程或生成代码下载入口 |
| [touijer20](./touijer20-posting-access-method/desc.md) | 🟡 | `WBAN` posting access method `UPPAAL-SMC` 模型 | 医疗网络协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.14569/IJACSA.2020.0110887) | 论文可得，但未提供独立模型与查询文件；更适合复用统计查询模板 |
| [bakhshi21](./bakhshi21-edge-persistent-state-recovery/desc.md) | 🟡 | edge persistent-state 恢复机制模型 | 边缘服务容错案例 | 论文正文 + 容器化 fog 存储方案描述重建 | 🟠 | [DOI](https://doi.org/10.1109/ETFA45728.2021.9613178)；[预印本 PDF](https://www.es.mdu.se/pdf_publications/6316.pdf) | 论文与预印本可公开获取，但未给出稳定公开的 `UPPAAL` 模型包或实验脚本 |
| [basile21](./basile21-unisig-safety-application-intermediate-sublayer/desc.md) | 🟢 | `UNISIG SAI` 模型与性质集 | 铁路标准接口案例（公开仓库） | 论文 + 作者 `GitHub` 仓库 | 🟢 | [DOI](https://doi.org/10.1007/978-3-030-85248-1_11)；[GitHub 仓库](https://github.com/IreneRosadi/UppaalModels) | 模型与性质当前可直接获取，是公开度很高的铁路接口案例 |
| [basile21tram](./basile21-autonomous-tramway-positioning/desc.md) | 🟢 | tramway `APS` hazard 分析模型与实验日志 | 铁路定位控制案例（公开仓库） | 论文 + 作者 `GitHub` 仓库 + 预印本 | 🟢 | [DOI](https://doi.org/10.1007/S00165-021-00556-1)；[预印本 PDF](https://openportal.isti.cnr.it/data/2021/456085/2021_456085.preprint.pdf)；[模型仓库](https://github.com/davidebasile/faoc2020) | 论文明确给出模型与实验日志公开仓库，是公开度很高的 tramway hazard 案例 |
| [bilgram21](./bilgram21-online-vehicle-rerouting/desc.md) | 🟡 | `Stratego + SUMO` rerouting 源码与场景 | 城市交通 rerouting 案例（公开仓库） | 论文 + 作者 `GitHub` 仓库 | 🟢 | [DOI](https://doi.org/10.1177/03611981211000348)；[GitHub 仓库](https://github.com/Marglib/AAUP7) | 当前可直接获取源码和场景，是公开度较高的 `Stratego` 交通案例 |
| [bujosa20](./bujosa20-csrp-avb-tsn/desc.md) | 🟢 | `SRP/CSRP` 资源预留协议模型 | 工业 `TSN` 协议案例 | 论文 + 开放预印本 | 🟠 | [DOI](https://doi.org/10.1109/TII.2020.3015926)；[开放预印本 PDF](https://www.es.mdu.se/pdf_publications/5988.pdf) | 论文与预印本可得，但未确认独立模型与查询文件入口 |
| [feng21](./feng21-ckb-consensus-protocol/desc.md) | 🟡 | `CKB` two-step confirmation 模型 | 区块链协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.18293/SEKE2021-072)；[会议 PDF](https://ksiresearch.org/seke/seke21paper/paper072.pdf) | 论文公开，但未提供独立 `UPPAAL` 模型仓库 |
| [gamatie21](./gamatie21-energy-driven-computing/desc.md) | 🟢 | energy-driven computing 模型模板 | 采能计算案例（官方模型仓库） | 论文 + 官方 `uppaal-models` 仓库 | 🟢 | [EnergyNeutrality 目录](https://github.com/DEIS-Tools/uppaal-models/tree/main/CaseStudies/EnergyNeutrality) | 可直接获取能量中和案例模型，适合复跑电池 sizing 流程 |
| [guo21](./guo21-tsn-traffic-shapers/desc.md) | 🟢 | `TSN` shaper 形式模型 | 协议/网络案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1109/LCN52139.2021.9524955)；[论文 PDF](https://zhehou.github.io/papers/A-Formal-Method-for-Evaluating-the-Performance-of-TSN-Traffic-Shapers-using-UPPAAL.pdf) | 论文与参数公开，但未提供独立模型工件 |
| [holler21](./holler21-robocup-stratego/desc.md) | 🟡 | RoboCup 实时策略生成模型 | 机器人策略案例 | 论文正文 + 会议 PDF | 🟠 | [DOI](https://doi.org/10.5220/0010239602730280)；[会议 PDF](https://www.scitepress.org/Papers/2021/102396/102396.pdf) | 论文公开，但文中提及的项目入口未能确认稳定可访问仓库 |
| [kunnappilly21](./kunnappilly21-5g-service-orchestration/desc.md) | 🟡 | `5G-SO` `UML`/`UPPAAL` 模式与 `G5` 工作流 | 架构建模案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1145/3459960.3459965)；[论文 PDF](https://www.es.mdu.se/pdf_publications/6189.pdf) | 自动验证思路公开，但未确认稳定仓库或工具下载入口 |
| [meng21](./meng21-ato-operation-scenarios/desc.md) | 🟡 | 高铁 `ATO` 车门 / 站台门联动场景模型 | 铁路场景需求案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.3390/electronics10040503)；[论文页面](https://www.mdpi.com/2079-9292/10/4/503) | 论文公开，但未给独立 `UPPAAL` 场景模型下载入口 |
| [thamilselvam21](./thamilselvam21-traffic-light-controller/desc.md) | 🟢 | `SUMO + Stratego` 交通灯协同控制源码 | 城市交通案例（作者仓库） | 论文 + 作者 `GitHub` 仓库 | 🟢 | [GitHub 仓库](https://github.com/ThamilselvamB/Intelligent-Traffic-Light-Controller-using-Uppaal-Stratego) | 可直接获取城市交通灯控制代码与仿真脚本 |
| [basile22](./basile22-ertms-full-moving-block/desc.md) | 🟢 | `ERTMS` full moving block 模型 | 铁路控制案例（作者仓库） | 论文 + `ASTRail` 公开模型仓库 | 🟢 | [DOI](https://doi.org/10.1007/s10009-022-00653-3)；[模型仓库](https://github.com/davidebasile/ASTRail/tree/master/STTT2021) | 模型当前可直接获取，是高公开度铁路 `RBC/OBU/LU` 案例 |
| [gu22](./gu22-multi-agent-strategy-synthesis/desc.md) | 🟡 | `MALTA` 多代理 mission-planning 工具链 | 自主系统规划案例 | 论文 + 工具仓库 | 🟠 | [DOI](https://doi.org/10.1007/s10009-022-00657-z)；[MALTA 仓库](https://github.com/rgu01/MALTA) | 工具链可得，但 quarry benchmark 不是独立标准工件包 |
| [lehmann22](./lehmann22-r3-needle-steering/desc.md) | 🟢 | 三维针导航 `Uppaal` 模型细节 | 医疗导航案例 | 论文附录与正文重建 | 🟠 | [DOI](https://doi.org/10.4204/EPTCS.355.4)；[arXiv PDF](https://arxiv.org/pdf/2203.09884) | 正文和附录给出大量模型细节，但未提供独立仓库 |
| [chen23](./chen23-cait-iot-uppaal/desc.md) | 🟡 | `CaIT` 到 `UPPAAL` 的 smart home 示例 | `IoT` 形式语言桥接案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1587/transinf.2022EDP7223)；[J-STAGE PDF](https://www.jstage.jst.go.jp/article/transinf/E106.D/9/E106.D_2022EDP7223/_pdf) | 论文公开，但未提供独立 `UPPAAL` 模型或 `CaIT` 示例仓库 |
| [cuartas23](./cuartas23-mechanical-ventilator/desc.md) | 🟢 | 呼吸机 `ventilator.xml` 与 `SCADE` 模型 | 医疗设备案例（作者仓库） | 论文 + `ventynet` 仓库 | 🟢 | [ventilator.xml](https://github.com/ventynet/ventynet/blob/master/ventilator.xml)；[ventynet-SCADE](https://github.com/ventynet/ventynet-SCADE) | 当前可直接获取 `UPPAAL` 模型文件与相关原型材料 |
| [muhammad23](./muhammad23-sigfox-iot-network/desc.md) | 🟢 | `Sigfox` 水位监测节点寿命分析模型 | 工业 `IoT` 节点案例 | 论文正文 + 硬件测量描述 | 🟠 | [DOI](https://doi.org/10.1109/JSEN.2023.3261667)；[AAU VBN PDF](https://vbn.aau.dk/ws/files/755949882/Journal_Muhammad_IEEE_Sensors.pdf) | 论文公开，但未提供完整 `UPPAAL SMC` 模型和测量数据仓库 |
| [zhou24](./zhou24-electronic-examinations/desc.md) | 🟡 | 电子考试 `UPPAAL` 模型 | 业务流程案例（GitHub + Zenodo） | 论文 + 作者仓库 + 归档 | 🟢 | [GitHub 仓库](https://github.com/TURTING-BO/An-Electronic-Examination-Model-Based-on-UPPAAL)；[Zenodo](https://doi.org/10.5281/zenodo.12787513) | 模型可直接获取，是当前文库里公开度最高的业务流程类案例之一 |
| [backeman25](./backeman25-ros-timed-stochastic/desc.md) | 🟢 | `ROS` reaction-time 模型与工业案例代码 | 机器人性能案例（公开仓库） | 论文 + 作者 `GitHub` 仓库 | 🟢 | [DOI](https://doi.org/10.1007/978-3-031-85134-6_13)；[GitHub 仓库](https://github.com/ptrbman/ros2-modeling/) | 模型代码可直接获取，是高公开度 `ROS` 反应时间案例 |
| [dust25](./dust25-pattern-based-ros2-applications/desc.md) | 🟢 | `ROS 2` pattern-based 模板与场景模型 | 机器人中间件案例（完整模型页） | 论文 + 完整模型页面 | 🟢 | [DOI](https://doi.org/10.1007/s10009-025-00802-4)；[完整模型页面](https://sites.google.com/view/pbvros2nodes) | 模型模板可直接访问，是高公开度 `ROS 2` 执行语义案例 |
| [soltani25](./soltani25-spare-management-research-reactors/desc.md) | 🟢 | research reactor spare-management `SPTGA` 模型与查询 | 工业可靠性案例（Zenodo 工件） | 论文 + `Zenodo` artefact | 🟢 | [DOI](https://doi.org/10.1007/s10009-025-00791-4)；[Zenodo 工件](https://doi.org/10.5281/zenodo.7970835) | 工件当前可直接获取，是少见的 `Stratego` 备件优化公开案例 |
| [basile26](./basile26-contract-automata-runtime-environment/desc.md) | 🟢 | `CARE` 模型、测试与补充材料 | 开源中间件案例（GitHub + Zenodo） | 论文 + `CARE` release + 补充材料 | 🟢 | [DOI](https://doi.org/10.46298/lmcs-22(1:8)2026)；[CARE Release](https://github.com/contractautomataproject/CARE/releases/tag/v1.0.1)；[补充材料](https://doi.org/10.5281/zenodo.14671729) | 模型、源码与测试工件均可获取，是高公开度运行时验证案例 |

## 初步归类与当前观察

1. 文库扩展到 `80` 篇后，`1996-2026` 主线已经连续，且 `2003`、`2005`、`2015`、`2018`、`2020`、`2021` 六个年份簇被明显补厚，早中期应用面更平衡。
2. 本轮把 distributed lift、`CAN` 时钟同步、多处理器实时调度、`DIMA`、`802.11i`、`RTPS`、edge persistence、tramway `APS` 与 `NetBill` 放进同一账本，进一步坐实了 `UPPAAL` 在协议、控制、调度和服务四条主轴上的互补性。
3. 协议线不再只集中在 Internet/车联网常见案例，还覆盖了 `CAN`、`802.11i`、`RTPS` 和 `NetBill` 这类更贴近实现边界的对象，适合后续抽取握手、安全、同步、缓存一致性与知识承诺等性质簇。
4. 控制与铁路线新增 distributed lift 和 tramway `APS`，配合既有 `moving block`、`RBC/OBU/LU` 与 `UNISIG SAI`，已经形成从设备级协同控制到系统级 hazard 分析的对照链。
5. 调度分析线新增多处理器实时系统和 `DIMA` 航电两类案例，进一步补足了 `deadline`、refresh、queue overflow 与不可调度概率这类性能-安全混合性质。
6. 具体系统名、标准名和中间件名仍明显优于泛化关键词；公开性仍是主要短板，除 tramway 案例外，本轮多数条目仍需按论文重建模型。

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
| 2026-04-01 | 通过网络检索新增 `10` 篇应用论文，补入 `1996-2021` 的协议、控制器与机器人案例，并同步回写 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)、[SUMMARY.md](./SUMMARY.md) | 先筛查 `20+` 个候选，只保留能稳定拿到 PDF 且可完成 `paper.pdf + paper_content.txt + bibtex.bib + desc.md` 四件套的条目；再统一核对双轴分类、状态与公开性 | 补厚早中期应用主线，新增 `🤖` 次轴，并强化“作者主页/机构镜像优先”的检索经验 |
| 2026-04-01 | 再新增 `10` 篇 `2000-2023` 应用论文，覆盖 batch plant 综合、嵌入式传感器、`ICCP`、激光气管切开、`CAN` database、`UNISIG SAI`、城市 rerouting、`Sigfox` 节点寿命与 smart home `IoT`，并全部补齐 `desc.md` | 基于网络检索继续筛查 `20+` 个候选，只正式收录已拿到论文且可补齐 `paper.pdf + paper_content.txt + bibtex.bib + desc.md` 四件套的条目；同步复核仓库可达性与公开性口径 | 把正式入账总量推进到 `50` 篇，并补厚工业/嵌入式/交通/IoT 应用面 |
| 2026-04-01 | 再新增 `10` 篇 `2012-2025` 应用论文，覆盖 pacemaker、`ROS/Kobuki`、cooperative automotive timing、`SIP/ZRTP`、`TSN/CSRP`、投票协议、高铁 `ATO`、`CKB` 共识与 `ROS 2` pattern-based verification，并全部补齐 `desc.md` | 先接续仓库中断留下的 `paper.pdf + paper_content.txt` 半成品，再补齐 `bibtex.bib + desc.md`，随后统一回填统计、双轴分类和公开性清单 | 把正式入账总量推进到 `60` 篇，并把文库时间上界推进到 `2025`，显著补厚医疗与 `ROS/ROS 2` 应用线 |
| 2026-04-01 | 再新增 `10` 篇 `2007-2026` 应用论文，覆盖 `SHIM6`、`FlexRay`、`EUV`、Océ pipeline、line-tracing robot、`WBAN` posting、`ERTMS` full moving block、quarry 多代理、research reactor 与 `CARE`，并全部补齐 `desc.md` | 继续按“先筛查候选、拿到稳定 PDF、生成 `paper_content.txt`、补 `bibtex.bib + desc.md`、最后统一回填总表与公开性清单”的顺序执行；同时清理未正式入账的失败候选空目录 | 把正式入账总量推进到 `70` 篇，并补厚铁路、工业控制、网络协议与开源中间件应用线 |
| 2026-04-01 | 再通过网络检索新增 `10` 篇 `2003-2021` 应用论文，覆盖 distributed lift、`CAN` 时钟同步、多处理器实时调度、`DIMA`、`802.11i`、`RTPS`、edge persistence、tramway `APS` 与 `NetBill`，并全部补齐四件套 | 先检查仓库状态并接续中断任务，只正式入账已拿到稳定 PDF 且可完成 `paper.pdf + paper_content.txt + bibtex.bib + desc.md` 四件套的条目；随后统一回填公开性清单、年份分布与双轴统计 | 把正式入账总量推进到 `80` 篇，并显著补厚早中期协议、调度、铁路与边缘服务应用线 |

## 失败与阻塞记录

| 时间 | 候选条目/对象 | 问题 | 当前处理 |
|---|---|---|---|
| 2026-03-31 | Model-Checking Real-Time Control Programs | 官网旧链接 `https://homes.cs.aau.dk/~paupet/papers/ikllmmpt-ecrts00.pdf` 与对应 `.bib.txt` 返回 `404`，无法稳定取得三件套 | 本轮未正式入账；已以 [bordbar03-timeliness-qos-multimedia/](./bordbar03-timeliness-qos-multimedia/) 补足名额，超过 `5` 天后若找到可用公开版本再重试 |
| 2026-03-31 | `philaudio.ta` / `bopdp.xml` / `rvs10.zip` / `rsv-tacas11.zip` 等历史工件链接 | 官网 benchmark/case-study 页仍提到历史模型入口，但当前公开直链已失效或返回 `404` | 在公开性清单中统一按 `🟠 信息不清` 处理，不误记为“模型可直接获取” |
| 2026-04-01 | 本轮若干 `RTnet/OLSR` 等历史候选 | 仅能取得 `Cloudflare/403/ResearchGate` 或失效镜像，无法稳定拿到正式 PDF，因此不能完成四件套 | 本轮未正式入账；超过 `5` 天后若找到稳定公开 PDF 再重试 |
| 2026-04-01 | `arfi23` / `hasrat23` / `alzamil24` / `wang17` 等本轮候选 | 仅拿到 `403`、站点拦截或不稳定镜像，无法稳定取得正式 PDF，因此不能完成四件套；已删除本地空目录以避免与总账不一致 | 本轮未正式入账；超过 `5` 天后若找到稳定公开 PDF 再重试 |
