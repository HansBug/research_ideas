# PATH2 候选样本 codex 全量评审报告

- 候选池大小：**239** 条（T0 严格 + 双 🟢A + 💎 + 纯结构标签）
- 已评审：**239** 条
- 候选（15）：HSM 6 + EFSM 6 + FSM 3
- 备选（15）：同分布

## 图例

**axis score**: 🟢 强 / 🟡 中 / 🟠 弱 / ⚪ 无

**verdict**: 💎 STRONG / ✨ GOOD / 🟢 OK / 🔘 WEAK

**bucket**: HSM(-layered) / EFSM(-interlock) / FSM(-basic)

**领域**（与 [sources/SUMMARY.md](../../../sources/SUMMARY.md) 同口径）：

- 🚗 汽车与道路车辆控制 · 🚆 轨道交通与铁路控制 · ✈️ 航空航天与飞行/空管控制 · 🩺 医疗设备与生命支持控制
- 🏭 工业自动化与离散制造 · 🏢 楼宇机电与电梯控制 · 🌡️ 过程与环境控制 · 🚦 道路交通信号控制
- 🅿️ 智慧停车与车位管理 · 🧩 建模方法与系统工程 · 🔐 安全/安保分析 · ⚙️ 通用控制与形式化工具

## 桶级统计

| 桶 | 数量 | 💎 | ✨ | 🟢 | 🔘 | C1≥🟢 | C2≥🟢 | C3≥🟢 | C4≥🟢 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HSM-layered | 57 | 42 | 3 | 11 | 1 | 47 | 29 | 15 | 35 |
| EFSM-interlock | 131 | 21 | 8 | 99 | 3 | 2 | 53 | 10 | 89 |
| FSM-basic | 51 | 7 | 2 | 26 | 16 | 1 | 18 | 3 | 21 |

## 🎯 候选池（15）

### 速查表

| 序 | id | 领域 | 桶 | C1 | C2 | C3 | C4 | verdict | scale (S/E/V/T) | 案例 | 系统简述 | 我们关注的特性 |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 138 | ⚙️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 14/18/10/34 | [Ask-for-Directions Hierarchical Navigation Supe…](../../../sources/amazing-race-robot-edition/STM.md) | 这是一个未知办公楼中的移动服务机器人高层导航监督器，使用 LiDAR、摄像头、麦克风/语音识别等感知人与门牌，并通过移动底盘、语音输出和 PTZ 摄像头执行找人问路、跟随方向、查找门牌的流程。 | 该样本对 PATH2 很有价值：C1 的层次化 FSM 结构清楚，C3 有从各阶段 failure 回到初始 WANDER 的统一恢复语义，C4 又有真实机器人硬件动作。NL 描述与原文图 1/图 5 对齐度高，适合作为 T0 中的 HSM-layered 样本。 |
| 2 | 009 | 🚗 | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 9/13/10/20 | [Two-Stage Mission-and-Control FSM for Urban Dri…](../../../sources/a-hierarchical-control-system-for-autonomous-driving-towards-urban-challenges/STM.md) | 这是城市自动驾驶车辆的高层决策控制器，用感知、ROS 节点状态和任务数据在 Ready、SAG、Change-Lane、E-stop、avoid obstacle 等任务间切换。决策结果驱动局部规划与纵横向控制器，最终作用到加速、制动和转向。 | 该样本同时覆盖层次化 mission/control FSM、跨模式 E-stop 恢复和真实车辆执行器输出，能很好支撑 C1、C3、C4 的 in-loop grounding。NL 条件表与 Figure 2 对应清楚，适合作为 PATH2 的 HSM-layered 样本。 |
| 3 | 118 | ⚙️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 10/12/8/17 | [Robotic Spacecraft Subsystem Lifecycle Supervisor](../../../sources/hirosco-high-level-robotic-spacecraft-controller/STM.md) | 这是 HIROSCO 中面向航天器/机器人子系统的生命周期监督器，用遥测、遥控、实时链路状态和错误事件驱动各子系统从 Offline 经 Software-Init、Hardware-Init、Pre-Operational、Safe-Operational 到 Operational。故障时 supervisor 按 severity 将子系统退回安全态… | 该样本对 PATH2 价值主要在 C1/C3/C4：它有分层 supervisor + 子系统生命周期 FSM + severity-based 跨子系统恢复，且硬件动作语义清楚，适合作为生成-验证-反馈循环中的 HSM 与 forced recovery grounding case。C2 只有阈值级数值 guard，不能作为 Z3 强样本。 |
| 4 | 169 | ⚙️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 8/12/7/15 | [Hierarchical mission-execution FSM for an auton…](../../../sources/pirate-precision-imaging-real-time-autonomous-tracker-explorer/STM.md) | 这是 PIRATE 自主水面艇的任务监督控制器，用 GNSS、声学接收器、ToF/TDoA 定位、视觉检测跟踪来协调 PX4、左右推进器和 Jetson/GPU 视觉硬件。典型流程是岸站下发任务后执行航迹导航或声学跟踪，完成三角定位后追击目标，接近后进入视觉/loiter，异常时全局切到 RTH。 | 该样本在 C1/C3/C4 上很强：真实 USV、层次 composite mode、any-state RTH 和异构硬件控制都能直接给 agent loop 提供 parse、semantic、sim grounding。NL 描述清楚，且属于自主海洋机器人任务监督，不容易与常见工业批处理或阀门样本同构。 |
| 5 | 207 | 🏭 | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 10/5/5/14 | [Hierarchical vine-pruning autonomy supervisor](../../../sources/bumblebee-autonomous-robotic-vine-pruning/STM.md) | 这是 Bumblebee 葡萄藤自主修剪机器人的高层监督控制器，协调地面机器人导航、双目相机/3D 建模感知、7-DoF 机械臂与剪切末端执行器。典型流程是驶向葡萄藤位置、停止扫描建模、定位剪切点、执行机械臂剪切，再前往下一株。 | 该样本对 PATH2 很有价值：C1/C3/C4 都有强 grounding，且来自真实田间农业机器人系统，不是玩具 FSM。NL 摘要清晰、流程闭环完整，能测试 agent loop 对层次状态、异常归并和硬件动作解耦的修复收益。 |
| 6 | 160 | ✈️ | HSM | 🟢 | 🟢 | 🟢 | 🟡 | 💎 | 10/20/8/24 | [Mission-Mode / Command-Mode VTOL UAV Supervisor](../../../sources/onboard-mission-management-vtol-uav-sequence-supervisory-control/STM.md) | 该 case 控制 VTOL 无人机机载任务管理器：监督层根据操作者、数据链路、payload/传感输入选择 Fly Home 或 Search and Track 等高层目标，序列层把 mission plan 解析成行为并向飞控输出轨迹/速度/位置类命令。典型流程是 Mission Mode 解析并执行任务行为，遇到直接命令、stop/manual、链… | 该样本对 PATH2 很有价值：C1/C3 都有清晰的层次状态和跨 mode 强制切换，C2 还有 mission/command plausibility 的数值语义检查，能支撑 parse + semantic + sim 的 in-loop feedback。它也是较真实的 UAV 工业控制对象，NL 描述边界清楚，和简单 takeoff/landi… |
| 7 | 142 | 🏭 | EFSM | 🟡 | 🟢 | 🟢 | 🟢 | 💎 | 13/18/11/21 | [HMI-Configured Cup Filling, Capping, and Labeli…](../../../sources/plc-scada-liquid-filling-automation-ejosat/STM.md) | 这是 PLC/SCADA 控制的杯装液体灌装线：操作者在 HMI 选择产品、克重和产量，PLC 依据液位、loadcell 重量与编码器反馈驱动阀门、输送带、真空/气缸封盖和贴标。典型流程是配方输入、重量闭环灌装、五步封盖、按单品/混合贴标并送至出口。 | 该样本对 PATH2 很有价值：C2 数值 guard、C3 报警恢复、C4 多执行器硬件解耦都很清楚，且是典型工业 PLC/SCADA 产线对象。NL 描述相对独立完整，能支撑 parse/semantic/sim 闭环反馈。 |
| 8 | 234 | 🅿️ | EFSM | 🟡 | 🟢 | 🟢 | 🟢 | 💎 | 11/13/8/20 | [Multi-level parking lift auto/manual positionin…](../../../sources/lift-control-automatic-car-parking-using-plc/STM.md) | 该 case 控制多层自动停车库的 PLC 升降机，用 VFD 驱动升降电机，并用叉形传感器、托盘位置传感器、停层确认传感器和安全互锁完成自动/手动定位。典型流程是自动接收目标层命令，计算层差和方向，快速运行、接近后降速、停层确认，异常时进入错误/急停路径。 | 该样本对 PATH2 很有价值：C2 的层差/计数器数值守卫清楚，C3/C4 又有全局报警急停和明确硬件执行器，可同时测试 symbolic guard feedback、forced fault recovery 和 abstract handler。NL 结构独立且工业控制对象典型。 |
| 9 | 114 | 🅿️ | EFSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 12/18/6/24 | [Slot-Selected Rotary Parking and Retrieval Cont…](../../../sources/vertical-rotary-car-parking-plc-outseal/STM.md) | 该 case 控制一个 8 车位垂直旋转停车库，PLC Outseal 读取 proximity/IR 传感器与 Android HMI 指令，驱动入口栏杆电机、旋转车库电机、继电器和 LED。典型流程是 Start 后检测进车、校验车辆位置、HMI 选车位并旋转停车，取车时选择车位、旋转到底部、人工确认 BENAR 后开闸放行。 | 该样本对 PATH2 有价值，主要强在 C2 的车位号/车辆数/移动 counter 数值 EFSM，以及 C4 的多硬件输出解耦；同时它是典型 PLC 工业控制对象，NL 流程从进车、停车、取车到 emergency/reset 都比较完整。 |
| 10 | 090 | ⚙️ | EFSM | 🟡 | 🟢 | 🟢 | 🟡 | 💎 | 14/12/12/40 | [Joey Pipe-Network Exploration Supervisor](../../../sources/autonomous-control-miniaturized-mobile-robots-unknown-pipe-networks/STM.md) | 这是 Joey 微型管网巡检机器人的高层探索监督器，使用三路 ToF 距离传感器、IMU 和轮腿编码器识别局部管网形态，并驱动左右轮腿电机完成直行、转弯、避障、死路掉头和回到入口。典型流程是在未知管网中按最右优先规则遍历岔路，遇 dead-end 180° 掉头，并持续监控翻倒和碰撞风险。 | 该样本对 PATH2 的价值主要在 C2 和 C3：数值传感 guard 很丰富，且有贯穿所有运行阶段的碰撞/翻倒安全监控，适合展示 parse + semantic + sim 反馈的收益。它是真实机器人控制对象，NL 描述和原文动作表都较清晰，和常见家电/楼控样本不趋同。 |
| 11 | 181 | 🏢 | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 10/14/10/20 | [Priority-Scanned Smart-Home Utility and Access …](../../../sources/enhanced-smart-home-control-monitoring-system/STM.md) | 这是一个 AT89C51 智能家居监督控制器，用水位、温度、烟雾、运动/进出和 keypad 信号按优先级扫描不同子流程。典型流程是根据传感输入启动/停止水泵、空调、报警器、灯光、门禁与 GSM/LCD 通知。 | 该样本对 PATH2 的价值主要在 C2 与 C4：它把多个传感阈值、计数器和重试次数 guard 绑定到真实家居执行器，适合测试 symbolic guard feedback 与 abstract hardware handler。NL 独立清晰，且比单一门禁/灯控样本更综合。 |
| 12 | 008 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 12/12/13/12 | [Twelve-State EMS for LNG-Ship Hybrid Power Disp…](../../../sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/STM.md) | 该 case 控制 LNG 船混合供能 EMS，读取负载 PL、PV/WEC 输出 Ppv/Pw、三台机组容量和电池 SoC，并对 LNG、DG1、DG2、电池充放电与 spare power 发出功率调度。典型流程是 RES 优先，电池补缺，其后依次启用 LNG、DG1、DG2，极端过载落入非法 State 2_7。 | 该样本对 PATH2 的主要价值在 C2 和 C4：数值调度 guard 密集且真实工业控制对象清楚，硬件出口覆盖多类发电机与电池系统。NL 与 Table 1-3 对齐度高，适合检验 symbolic guard feedback 和 abstract hardware action grounding。 |
| 13 | 194 | 🌡️ | FSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 18/9/6/30 | [Five-mode microgrid EMS switch-breaker supervisor](../../../sources/optimization-control-energy-management-system-microgrids/STM.md) | 这是一个并网微电网 EMS 的模式切换监督器，用 EMS breaker、utility-grid transfer switch、grid power indicator 以及逆变器控制在 Grid-connected、Grid-only、Islanding、Synchronization、Outage 之间切换。典型流程是在电网故障时断开并网开关进入孤… | 该样本对 PATH2 有价值主要在 C2 和 C4：同步重连含清晰数值 guard，模式切换直接驱动物理开关和逆变器动作。它也是典型工业能源控制对象，NL 与图示状态编码都比较清楚。 |
| 14 | 018 | ✈️ | FSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 6/8/8/12 | [Low-altitude mission-task FSM for target approa…](../../../sources/autonomous-control-framework-unmanned-helicopter-low-altitude-flight/STM.md) | 该 case 控制无人直升机在山地低空任务中的高层飞行决策，利用机载相机/检测网络、Lidar/VFH 与可见性判断，在远程穿透、目标快速接近、严重威胁快速规避和小威胁迂回飞行之间切换。执行侧主要输出 yaw、altitude、longitude、lateral 等飞控通道命令。 | 该样本对 PATH2 有价值主要在 C2 和 C4：威胁等级阈值分支有清晰数值 grounding，飞控通道和 VFH/visual-servo 动作也能体现 abstract action 的硬件解耦收益。NL 独立且贴近真实无人直升机控制任务。 |
| 15 | 097 | ✈️ | FSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 6/6/5/10 | [Search-follow-catch mission controller](../../../sources/autonomous-aerial-robot-high-speed-search-intercept/STM.md) | 该 case 控制高速搜索与拦截任务中的 UAV 高层 mission controller，利用长距/短距视觉检测、球检测和夹爪内激光传感器触发状态切换。典型流程是起飞后搜索目标、长距跟随、短距接近、对准夹爪抓球，成功后降落。 | 该样本对 PATH2 的主要价值在 C2 与 C4：有清晰的连续帧计数型 guard，且状态动作直接连接 UAV 运动、云台和夹爪伺服等硬件出口。NL 描述和原文状态/事件表都较完整，适合作为真实机器人 T0 mission-control case。 |

### 详细卡片

#### HSM-layered （6 条）

##### 1. `[138]` ⚙️ Ask-for-Directions Hierarchical Navigation Supervisor (HSM-layered)

- **领域**: ⚙️
- **论文**: paper #485 [`amazing-race-robot-edition`](../../../sources/amazing-race-robot-edition/STM.md)
- **是什么**: 这是一个未知办公楼中的移动服务机器人高层导航监督器，使用 LiDAR、摄像头、麦克风/语音识别等感知人与门牌，并通过移动底盘、语音输出和 PTZ 摄像头执行找人问路、跟随方向、查找门牌的流程。
- **scale**: states=14 / events=18 / vars=10 / trans=34
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文 Figure 1 给出 WANDER、APPROACH_PERSON、HOLD_CONVERSATION、FOLLOW_DIRECTIONS、NAVIGATE_DOOR、ACHIEVE_GOAL 的顶层 FSM，且 WANDER 与 FOLLOW_DIRECTIONS 均明确有 five substates。
- **C2 数值守卫**: 🟡 — 原文 Figure 5/Section III 写到 DRIVE_THROUGH_INTERSECTION 需 intersection type changed 且 traveled more than 2 m，FOLLOW_DIRECTIONS maintains a step counter，WANDER 还维护 visitation times。
- **C3 forced fault**: 🟢 — 原文 Architecture 明确说系统 recovers from failure at any of those steps，且 each state 的 failure conditions result in a transition to the initial state。
- **C4 硬件解耦**: 🟢 — 原文 Hardware/Architecture 列出 Husky UGV、3D LiDAR、Axis PTZ Camera、microphone，并描述 robot drives towards the person、synthesizes speech、pans its camera to read door tag。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C1 的层次化 FSM 结构清楚，C3 有从各阶段 failure 回到初始 WANDER 的统一恢复语义，C4 又有真实机器人硬件动作。NL 描述与原文图 1/图 5 对齐度高，适合作为 T0 中的 HSM-layered 样本。
- **风险**: 数值 guard 多来自导航过程阈值和计数器，不是紧凑控制器中的强复合算术不变式，C2 不宜高估。

<details><summary><b>📝 扩充 NL（266 词 / 26 markers / 26 provenance entries）</b></summary>

**Expanded NL**:

> The robot operates in an unknown office and uses a finite-state-machine architecture [E1] [E2]. It starts in WANDER because it must find a person before obtaining directions [E3]. Its pipeline searches for an approachable person [E4], approaches and speaks to them [E5], asks for and interprets directions [E6], follows the plan [E7], then enters NAVIGATE DOOR to inspect door tags [E8]. Across the architecture, each state has a success condition that advances the pipeline and failure conditions that return control to the initial state [E9] [E10]. Inside WANDER, the exploration FSM enters MAKE DECISION first; if no qualitative directions are available, it enters a recovery rotation that spins 360 degrees to refresh the quantitative and qualitative maps [E11] [E12]. During exploration, WANDER drives forward while watching for registered intersections [E13]. A dead end is treated as a case with only a back drivable trajectory and no forward, left, or right trajectories [E14]; it may rotate 180 degrees before returning to forward driving [E15]. Inside FOLLOW DIRECTIONS, it enters MAKE DECISION first and initializes a step counter to the first plan step [E16]; it uses drive, rotate, and crossing phases, and the crossing phase returns only after more than 2 m of travel and an intersection-type change [E17] [E18]. If the goal action names the correct hallway, control moves to NAVIGATE DOOR [E19]; if it names another person waypoint, control returns to WANDER to ask again [E20] [E21]. The deployed Husky A200 uses an IMU, 3D LiDAR, PTZ camera, microphone, speech recognition, and speaker-based synthesis for mapping, door perception, and spoken dialogue [E22] [E23] [E24] [E25] [E26].

**Axis coverage**:

- **C1**: C1 由 WANDER 内部默认进入 MAKE DECISION、无 qualitative directions 时进入恢复子状态，以及 FOLLOW DIRECTIONS 内部 MAKE DECISION/drive/rotate/crossing phase 暴露，对应 [E11] [E12] [E16] [E17]。
- **C2**: C2 由 no qualitative directions、dead-end 的 back 且无 forward/left/right 复合守卫、step counter、2 m 与 intersection-type change 条件暴露，对应 [E12] [E14] [E16] [E18]。
- **C3**: C3 仅有原文支持的横切 failure-to-initial 语义：每个 state 都有 success/failure 条件，failure 回到 initial state，对应 [E9] [E10]；原文不支持 emergency-stop/forced-fault 按钮。
- **C4**: C4 由 Husky A200、IMU、3D LiDAR、PTZ camera、microphone、speech recognition、speaker synthesis 与 door perception 暴露，并由 drive/rotate 行为补充物理动作，对应 [E13] [E17] [E22] [E23] [E24] [E25] [E26]。

**Provenance** (26 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | paper.pdf p.1 Abstract | finding a room in an unknown and unmodified office environment | robot operates in an unknown office |
| [E2] | STM §1 摘录 B \| paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 163-164 | Our architecture is a finite-state machine illustrated in Figure 1. | uses a finite-state-machine architecture |
| [E3] | STM §1 摘录 B \| paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 168-170 | Given a goal description, the initial state is WANDER, as the robot needs to find a person to get… | starts in WANDER because it must find a person before obtaining directions |
| [E4] | STM §1 摘录 C \| paper.pdf p.5 §III.A WANDER \| paper_content.txt 行 436-438 | trying to detect and track people until it finds an approachable person. | pipeline searches for an approachable person |
| [E5] | STM §1 摘录 B \| paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 172-175 | it drives towards the person and synthesizes speech to grab their attention. | approaches and speaks to the person |
| [E6] | STM §1 摘录 B \| paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 176-179 | The robot uses speech synthesis and speech recognition to request directions to the desired goal … | asks for and interprets directions |
| [E7] | STM §1 摘录 B \| paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 182-185 | FOLLOW DIRECTIONS executes each direction in order by continuously mapping the environment | follows the plan |
| [E8] | STM §1 摘录 B \| paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 188-190 | NAVIGATE DOOR state which involves detecting doors and driving up to them to inspect their door t… | enters NAVIGATE DOOR to inspect door tags |
| [E9] | paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 165-167 | Each state has a success condition that leads to the next state in the pipeline | each state has a success condition that advances the pipeline |
| [E10] | paper.pdf p.2 §II.B Architecture \| paper_content.txt 行 167-168 | failure conditions which result in a transition to the initial state of the system. | failure conditions return control to the initial state |
| [E11] | STM §1 摘录 C \| paper.pdf p.5 §III.A WANDER \| paper_content.txt 行 443-448 | WANDER enters the MAKE DECISION substate first | WANDER exploration FSM enters MAKE DECISION first |
| [E12] | paper.pdf p.5 §III.A WANDER \| paper_content.txt 行 449-453 | If no qualitative directions are available (e.g., when it is first initialized), it enters the RO… | no qualitative directions triggers a 360-degree recovery rotation |
| [E13] | paper.pdf p.5 §III.A WANDER \| paper_content.txt 行 462-463 | the robot continuously drives forward while monitoring for registered intersections. | WANDER drives forward while watching for registered intersections |
| [E14] | paper.pdf p.6 §III.A WANDER \| paper_content.txt 行 504-507 | back qualitative drivable trajectory but no forward, left, or right qualitative drivable trajecto… | dead-end guard over available qualitative drivable trajectories |
| [E15] | paper.pdf p.6 §III.A WANDER \| paper_content.txt 行 513-515 | The robot would enter the ROTATE substate, rotate 180◦, and then return to the DRIVE FORWARD subs… | rotate 180 degrees before returning to forward driving |
| [E16] | STM §1 摘录 D \| paper.pdf p.11 §III.D FOLLOW DIRECTIONS \| paper_content.txt 行 1065-1068 | It enters the MAKE DECISION substate first, initializing the step counter to the first step in th… | FOLLOW DIRECTIONS enters MAKE DECISION first and initializes the step counter |
| [E17] | STM §1 摘录 D \| paper.pdf p.11 §III.D FOLLOW DIRECTIONS \| paper_content.txt 行 1061-1064 | DRIVE FORWARD, ROTATE, DRIVE THROUGH INTERSECTION | drive, rotate, and crossing phases |
| [E18] | paper.pdf p.12 §III.D FOLLOW DIRECTIONS \| paper_content.txt 行 1091-1095 | it requires that the intersection type change and the robot travel at least 2 m | crossing phase guard: more than 2 m and intersection-type change |
| [E19] | STM §1 摘录 D \| paper.pdf p.12 §III.D FOLLOW DIRECTIONS \| paper_content.txt 行 1104-1107 | the robot has reached the same hallway as the goal and must look for it. Thus the robot will tran… | goal hallway leads to NAVIGATE DOOR |
| [E20] | STM §1 摘录 D \| paper.pdf p.12 §III.D FOLLOW DIRECTIONS \| paper_content.txt 行 1107-1109 | When the goal action is person | another person waypoint condition |
| [E21] | STM §1 摘录 D \| paper.pdf p.12 §III.D FOLLOW DIRECTIONS \| paper_content.txt 行 1107-1110 | must now seek out a new person to ask for instructions. Thus the robot will transition to the WAN… | returns to WANDER to ask again |
| [E22] | paper.pdf p.2 §II.A Hardware and Software \| paper_content.txt 行 135-141 | Our robotic platform consists of a Clearpath Husky A200TM UGV equipped with an Open IMU UM7, Velo… | Husky A200 with IMU, 3D LiDAR, PTZ camera, and microphone |
| [E23] | paper.pdf p.2 §II.A Hardware and Software \| paper_content.txt 行 145-146 | perform simultaneous localization and mapping (SLAM) from data from the IMU and 3D LiDAR. | mapping from IMU and 3D LiDAR |
| [E24] | paper.pdf p.2 §II.A Hardware and Software \| paper_content.txt 行 147-148 | We record speech with the Blue Yeti microphone and convert it into text using the Google Speech-t… | microphone and speech recognition |
| [E25] | paper.pdf p.2 §II.A Hardware and Software \| paper_content.txt 行 149-150 | pyttsx3 library [7] to synthesize speech through the laptop speaker. | speaker-based synthesis and spoken dialogue |
| [E26] | paper.pdf p.12 §III.E NAVIGATE DOOR \| paper_content.txt 行 1168-1171 | To detect doors, doorways, and elevators, we rely on four standard pieces of sensor information f… | door perception |

**Intentional omissions**: 没有补造 valve 编号、emergency stop、forced fault path、周期性传感器采样或额外阈值。也没有列出全部顶层状态和全部子状态，只保留能触发层次与数值守卫的少量关键 mode/phase。

</details>


##### 2. `[009]` 🚗 Two-Stage Mission-and-Control FSM for Urban Driving (HSM-layered)

- **领域**: 🚗
- **论文**: paper #158 [`a-hierarchical-control-system-for-autonomous-driving-towards-urban-challenges`](../../../sources/a-hierarchical-control-system-for-autonomous-driving-towards-urban-challenges/STM.md)
- **是什么**: 这是城市自动驾驶车辆的高层决策控制器，用感知、ROS 节点状态和任务数据在 Ready、SAG、Change-Lane、E-stop、avoid obstacle 等任务间切换。决策结果驱动局部规划与纵横向控制器，最终作用到加速、制动和转向。
- **scale**: states=9 / events=13 / vars=10 / trans=20
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文明确说 M-FSM 分为 Ready、SAG、CL、E-stop、avoid obstacle 五类，且 “M-FSM consists of a C-FSM”，CL 内又有 lane-keeping 和 lane-changing 两个控制状态。
- **C2 数值守卫**: 🟡 — Table 1 的 condition 41 写明 “Un-complete obstacle avoiding mission, and the time for the mission is over”，可形成基于任务计时器的超时 guard，但其他条件多为符号事件。
- **C3 forced fault**: 🟢 — 原文写 “When urgent situations appear, the E-stop mode is activated”，Table 1 又列出 10/20/30/40 均为 perception informs emergency circumstances，且 E-stop priority 最高。
- **C4 硬件解耦**: 🟢 — Figure 6 将 Longitudinal controller 输出到 Acceleration/Break、Lateral controller 输出到 Steering，结论也写到 commanding throttle, brake, steering angle。
- **对 PATH2 的价值**: 该样本同时覆盖层次化 mission/control FSM、跨模式 E-stop 恢复和真实车辆执行器输出，能很好支撑 C1、C3、C4 的 in-loop grounding。NL 条件表与 Figure 2 对应清楚，适合作为 PATH2 的 HSM-layered 样本。
- **风险**: C2 数值守卫主要来自 obstacle-avoidance timeout，DMM 本体多数 guard 是 condition code，若只抽任务 FSM 而不带控制器变量，Z3 收益会偏弱。

<details><summary><b>📝 扩充 NL（256 词 / 17 markers / 17 provenance entries）</b></summary>

**Expanded NL**:

> The urban-driving controller is a decision-making mechanism for a self-driving car implemented as a two-stage FSM: the Mission FSM manages vehicle missions, and the Control FSM mimics the vehicle's status on the road [E1]. After observing surrounding-object trajectories and mission data, the two FSMs determine mission behavior and on-road control behavior, with mission choices including modes such as Change-Lane, E-stop, and obstacle avoidance [E2][E3]. Within the hierarchy, Change-Lane contains lane-keeping and lane-changing control states, and obstacle avoidance activates when obstacles are detected on the path [E4][E5]. Each FSM state requires a resource updated over time in ROS perception nodes, and the implemented vehicle's sensor set includes 3D LiDAR, Zed-camera, GPS, IMU, and encoders [E6][E7]. Normal progress uses condition 11 when ROS nodes are healthy and the vehicle is ready to go, and condition 23 when a path change is demanded [E8][E9]. Abnormal handling uses perception-driven emergency conditions 10, 20, 30, and 40, keeps working in emergency mode under condition 00, and can wake back to Ready under condition 01 when the case is non-dangerous [E10]. Obstacle recovery is captured by condition 41 when avoidance is incomplete and its time is over, condition 44 while the mission is being handled, and condition 42 when obstacle avoidance is completely performed [E11][E12]. State flags and priorities protect shared resources, with E-stop assigned the highest priority before obstacle avoidance, Change-Lane, and Stop-and-Go [E13][E14]. The downstream control layer follows the chosen trajectory through longitudinal and lateral controllers, using acceleration or braking for speed control and steering turn for lane tracking [E15][E16][E17].

**Axis coverage**:

- **C1**: expanded_nl 通过 two-stage FSM、Mission FSM / Control FSM、以及 Change-Lane 内部 lane-keeping / lane-changing 暴露层次结构 [E1][E4]；原文未明确进入 CL mode 时默认从哪个子态开始，因此未写默认初态。
- **C2**: 本条 DMM 原文只给 condition 11/23/41/42 等转移标签及语义，没有使命转移的物理数值阈值、区间或复合数值 guard；expanded_nl 只保留标签语义，不伪造阈值 [E8][E9][E11][E12]。
- **C3**: expanded_nl 通过 emergency conditions 10/20/30/40、condition 00、condition 01 和 E-stop 最高优先级暴露跨 mission 的异常/优先级语义 [E10][E14]；原文没有明确 any sub-state forced transition。
- **C4**: expanded_nl 暴露了 ROS perception resources、3D LiDAR/Zed-camera/GPS/IMU/encoders，以及下游 acceleration/braking/steering turn 控制动作 [E6][E7][E15][E16][E17]；原文没有 valve/pump 这类具名执行器编号。

**Provenance** (17 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 B \| paper.pdf p.4 §2.1 \| paper_content.txt 行 177-181 | The first DMM called the Mission FSM (M-FSM), which manages the vehicle’s missions. The second DM… | two-stage FSM; Mission FSM manages missions; Control FSM mirrors on-road status |
| [E2] | paper.pdf p.4 §2.1 \| paper_content.txt 行 181-183 | After observing the surrounding object’s trajectory from the perception and the missions data, M-… | uses surrounding-object trajectories and mission data to determine FSM behavior |
| [E3] | STM §1 摘录 B \| paper.pdf p.4 §2.1 \| paper_content.txt 行 183-184 | M-FSM is categorized into five classes: Ready, Stop-and-Go (SAG), Change-Lane(CL), E-stop, avoid … | mission choices include Change-Lane, E-stop, and obstacle avoidance |
| [E4] | STM §1 摘录 B \| paper.pdf p.4 §2.1 \| paper_content.txt 行 188-189 | The CL mode consists of two control states lane-keeping and lane-changing, which actuates when la… | Change-Lane contains lane-keeping and lane-changing control states |
| [E5] | STM §1 摘录 B \| paper.pdf p.4 §2.1 \| paper_content.txt 行 189-190 | The obstacle avoiding mode activates when the obstacles have been detected lying on the path. | obstacle avoidance activates when obstacles are detected on the path |
| [E6] | STM §1 摘录 C \| paper.pdf p.5 Figure 2说明 \| paper_content.txt 行 210-212 | Each state in FSM requires a resource that is updated over time in the ROS nodes of perception. | FSM state resources are updated over time in ROS perception nodes |
| [E7] | paper.pdf p.16 §3.1 \| paper_content.txt 行 829-830 | The sensors system consists of 3D Light Detection and Ranging (3D LiDAR), Zed-camera, GPS, IMU, a… | vehicle sensor set includes 3D LiDAR, Zed-camera, GPS, IMU, and encoders |
| [E8] | STM §1 摘录 B \| paper.pdf p.5 Table 1 \| paper_content.txt 行 199 | 11 All ROS nodes staying healthy, and the vehicle status is ready to go | condition 11 means ROS nodes are healthy and the vehicle is ready |
| [E9] | STM §1 摘录 B \| paper.pdf p.5 Table 1 \| paper_content.txt 行 205 | 23 Demanding to change the path | condition 23 means a path change is demanded |
| [E10] | STM §1 摘录 B \| paper.pdf p.5 Table 1 \| paper_content.txt 行 197-200 | 10, 20, 30, 40 The perception informs the emergency circumstances; 00 Continuously works in an em… | emergency conditions, emergency persistence, and recovery to Ready |
| [E11] | STM §1 摘录 B \| paper.pdf p.5 Table 1 \| paper_content.txt 行 201 | 41 Un-complete obstacle avoiding mission, and the time for the mission is over | condition 41 captures incomplete obstacle avoidance after mission time is over |
| [E12] | STM §1 摘录 B \| paper.pdf p.5 Table 1 \| paper_content.txt 行 203-207 | 44 Handling on the avoid obstacle mission; 32, 42 Completely performs the lane-changing and obsta… | condition 44 handles obstacle avoidance; condition 42 marks completed obstacl… |
| [E13] | STM §1 摘录 C \| paper.pdf p.5 Figure 2说明 \| paper_content.txt 行 211-212 | The use of priority and flag of each state is to prevent access to the same resources. | flags and priorities prevent shared-resource conflicts |
| [E14] | STM §1 摘录 C \| paper.pdf p.5 Figure 2说明 \| paper_content.txt 行 212-213 | The priority level of the E-stop mode is highest, following by the obstacle avoiding mode, the CL… | priority order among E-stop, obstacle avoidance, CL, and SAG |
| [E15] | paper.pdf p.4 §2 \| paper_content.txt 行 174-175 | the control commands the car to follow the trajectory by using the longitudinal and lateral contr… | downstream control follows trajectory through longitudinal and lateral contro… |
| [E16] | paper.pdf p.11 §2.3.1 \| paper_content.txt 行 630-632 | The controller must apply accelerating or braking to obtain the best control performance. | longitudinal speed control uses acceleration or braking |
| [E17] | paper.pdf p.10 §2.3 \| paper_content.txt 行 495-497 | the lateral controller manipulates the lane tracking by adjusting the steering turn. | lateral control uses steering turn for lane tracking |

**Intentional omissions**: 没有补写具体速度/距离阈值、车道变换默认子态、任意状态强制跳转或传感器触发阈值，因为本条 DMM 摘录和相关 PDF 段落没有给出这些事实。也未把控制算法中的 10 ms timer、look-ahead 公式等细节写成 DMM guard，以免把下游控制算法误当成该状态机的转移条件。

</details>


##### 3. `[118]` ⚙️ Robotic Spacecraft Subsystem Lifecycle Supervisor (HSM-layered)

- **领域**: ⚙️
- **论文**: paper #422 [`hirosco-high-level-robotic-spacecraft-controller`](../../../sources/hirosco-high-level-robotic-spacecraft-controller/STM.md)
- **是什么**: 这是 HIROSCO 中面向航天器/机器人子系统的生命周期监督器，用遥测、遥控、实时链路状态和错误事件驱动各子系统从 Offline 经 Software-Init、Hardware-Init、Pre-Operational、Safe-Operational 到 Operational。故障时 supervisor 按 severity 将子系统退回安全态或关闭实时网络，涉及硬件设备初始化、执行器使能/禁用、机械臂与力反馈摇杆等实体硬件。
- **scale**: states=10 / events=12 / vars=8 / trans=17
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文称 satellite runs in various modes 且各 mode 需要不同 subsystem operational，supervisor 位于 higher hierarchical level；Figure 4 又给出 ten separate states，并说明 each state can be subdivided into different phases。
- **C2 数值守卫**: 🟡 — 原文给出 temperature of a hardware device reaches a critical limit 和 exceed the torque limit of a joint 这两类阈值 guard，但没有复合算术或多变量合取。
- **C3 forced fault**: 🟢 — 原文明确有 global error handling，且 high severity errors 会 shut down all subsystems participating in the real-time network，medium severity 会把 subsystem 改到 safe-operational。
- **C4 硬件解耦**: 🟢 — 原文写 Hardware-Init 会 activate and initialize all hardware devices，Safe-Operational 禁用 actuators、Operational 启用 actuators，实测场景还有 manipulator、force-feedback joystick 和 real-time network shutdown。
- **对 PATH2 的价值**: 该样本对 PATH2 价值主要在 C1/C3/C4：它有分层 supervisor + 子系统生命周期 FSM + severity-based 跨子系统恢复，且硬件动作语义清楚，适合作为生成-验证-反馈循环中的 HSM 与 forced recovery grounding case。C2 只有阈值级数值 guard，不能作为 Z3 强样本。
- **风险**: 原文是体系结构论文而非完整控制需求，迁移触发和数值阈值多为概念性描述，部分 guard/action 需要从 Figure 4 和段落语义中保守补全。

<details><summary><b>📝 扩充 NL（279 词 / 21 markers / 21 provenance entries）</b></summary>

**Expanded NL**:

> HIROSCO treats satellite operation as mode-dependent subsystem coordination, e.g. telepresence or autonomous operation, where some subsystems are connected by real-time links [E1], and a supervisor logs telecommands and telemetry, monitors all subsystems, handles global errors, and manages inter-subsystem communication [E2]. Every subsystem implements the ten-state lifecycle machine for commissioning and coordination [E3]; it starts and stops in Offline [E4], and each state may be subdivided into phases if required [E5]. During commissioning, software data structures are published as parameters [E6], hardware devices are activated and initialized [E7], and the operator selects a configuration from the subsystem descriptor [E8]. The required real-time link is a guard for that move: Real-time Link Handling blocks Pre-Operational-to-Safe-Operational switching while the link is absent [E9], and the supervisor maintains a graph of all real-time links [E10]. In Safe-Operational, all control algorithms are active but hardware actuators remain disabled for verification [E11]; after verification, Operational enables the actuators and permits complete control [E12]. If a severe error occurs in this subsystem or another one, Error-Operational brings hardware devices to a defined state [E13], and a critical hardware-temperature limit is an example condition reported to the supervisor [E14]. Event Handling reacts to asynchronous error notifications with predefined recovery plans based on reason [E15] and the three PUS severity levels: low, medium, and high [E16]. A manipulator failure during grasping is a high-severity case [E17], and Event Handling must then shut down the affected real-time network [E18]; tests show that unplugging the joystick or robot immediately shuts down the joystick and manipulator subsystems [E19]. Medium-severity errors move the affected subsystem back to Safe-Operational [E20], while low-severity errors and progress information are only logged to the console [E21].

**Axis coverage**:

- **C1**: C1 暴露在 ten-state lifecycle、Offline 初始/停止语义以及 state 可细分为 phases 的描述中，对应 [E3][E4][E5]；原文只给通用 phase 可细分性，未给具体子 phase 名称。
- **C2**: 原文不支持具体数值阈值/区间/算术 guard，未提供强 C2 钩子；expanded_nl 只保留 required real-time link absent 和 critical hardware-temperature limit 这类定性 guard，对应 [E9][E14]。
- **C3**: C3 暴露在 supervisor 的全局监控/错误处理、high severity 关闭实时网络、medium/low severity 统一恢复策略中，对应 [E2][E18][E20][E21]。
- **C4**: C4 暴露在 hardware devices 激活初始化、actuators 禁用/启用、real-time network shutdown、joystick/manipulator shutdown 等硬件/外部效应中，对应 [E7][E11][E12][E18][E19]。

**Provenance** (21 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.3 subsystem coordination \| paper_content.txt 行181-184 | Each of these modes requires a different set of subsystems to be operational. Some of these subsy… | mode-dependent subsystems and real-time links |
| [E2] | STM §1 摘录 A \| paper.pdf p.3 subsystem coordination \| paper_content.txt 行187-190 | responsible for logging telecommands and telemetry data, monitoring all existing subsystems, glob… | supervisor duties |
| [E3] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行393-398 | This state machine consists of ten separate states. They were designed to ease the commissioning … | ten-state lifecycle machine for commissioning and coordination |
| [E4] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行402-403 | Each subsystem starts or stops in the state "Offline". | starts and stops in Offline |
| [E5] | paper.pdf p.5 §4.2 \| paper_content.txt 行455-458 | Each state can be subdivided into different phases if required. | state phases if required |
| [E6] | paper.pdf p.5 §4.2 \| paper_content.txt 行411-414 | all data structures that should be used by services of the component framework must be published … | software data structures published as parameters |
| [E7] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行416-419 | All hardware devices that belong to this subsystem are activated and initialized in this state. | hardware devices activated and initialized |
| [E8] | paper.pdf p.5 §4.2 \| paper_content.txt 行420-423 | the operator must select a configuration listed in the subsystem descriptor that should be applied. | operator selects configuration from subsystem descriptor |
| [E9] | paper.pdf p.6 §4.3 \| paper_content.txt 行489-492 | subsystems are not allowed to switch from "Pre-Operational" to "Safe-Operational" as long as a re… | real-time link guard for Pre-Operational-to-Safe-Operational switching |
| [E10] | paper.pdf p.6 §4.3 \| paper_content.txt 行492-494 | it maintains a graph of all real-time links so it is aware of all existing real-time networks at … | supervisor graph of real-time links |
| [E11] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行435-440 | all control algorithms implemented by the subsystem developer are active, but the actuators of th… | Safe-Operational algorithms active and actuators disabled |
| [E12] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行440-443 | The actuators are active and the subsystem can now be controlled completely. | Operational enables actuators and complete control |
| [E13] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行443-446 | The "Error-Operational" state secures that the hardware devices can reach a defined state after a… | Error-Operational brings hardware to defined state |
| [E14] | paper.pdf p.5 §4.2 \| paper_content.txt 行447-451 | if the temperature of a hardware device reaches a critical limit the subsystem has to notify the … | critical hardware-temperature condition reported to supervisor |
| [E15] | STM §1 摘录 C \| paper.pdf p.6 §4.3 \| paper_content.txt 行515-518 | may react to an error with predefined recovery plans based on severity and reason of the error. | Event Handling recovery plans based on reason |
| [E16] | STM §1 摘录 C \| paper.pdf p.6 §4.3 \| paper_content.txt 行518-520 | PUS defines three severity levels for error reporting: low, medium and high. | three PUS severity levels |
| [E17] | STM §1 摘录 C \| paper.pdf p.6 §4.3 \| paper_content.txt 行520-522 | if the manipulator failed during a grasp action and had to be shut down to avoid further damage, … | manipulator grasp failure as high severity |
| [E18] | STM §1 摘录 C \| paper.pdf p.6 §4.3 \| paper_content.txt 行523-524 | The "Event Handling" must then shut down the real-time network that includes the MCS | high-severity handling shuts down real-time network |
| [E19] | STM §1 摘录 C \| paper.pdf p.7 practical tests \| paper_content.txt 行599-604 | This was tested by unplugging the joystick or the robot from the real-time computer. This results… | unplugging joystick or robot immediately shuts down joystick and manipulator … |
| [E20] | STM §1 摘录 C \| paper.pdf p.7 practical tests \| paper_content.txt 行604-607 | Errors of medium severity cause the supervisor to change the state of a subsystem to safe-operati… | medium-severity errors move subsystem to Safe-Operational |
| [E21] | STM §1 摘录 C \| paper.pdf p.7 practical tests \| paper_content.txt 行607-609 | Errors of low severity and progress information are simply logged to the console without further … | low-severity errors and progress information logged only |

**Intentional omissions**: 没有添加阀门编号、传感器型号、具体温度或力矩阈值、恢复路径编号，因为原文没有给出这些细节。也没有把 2 kHz 采样率写成状态机 guard，因为它属于演示场景执行频率，不是生命周期状态机的转移条件。

</details>


##### 4. `[169]` ⚙️ Hierarchical mission-execution FSM for an autonomous marine tracker (HSM-layered)

- **领域**: ⚙️
- **论文**: paper #573 [`pirate-precision-imaging-real-time-autonomous-tracker-explorer`](../../../sources/pirate-precision-imaging-real-time-autonomous-tracker-explorer/STM.md)
- **是什么**: 这是 PIRATE 自主水面艇的任务监督控制器，用 GNSS、声学接收器、ToF/TDoA 定位、视觉检测跟踪来协调 PX4、左右推进器和 Jetson/GPU 视觉硬件。典型流程是岸站下发任务后执行航迹导航或声学跟踪，完成三角定位后追击目标，接近后进入视觉/loiter，异常时全局切到 RTH。
- **scale**: states=8 / events=12 / vars=7 / trans=15
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文明确写 mission execution is structured as an FSM，且 high-level operational states are organized hierarchically, with composite modes encapsulating navigation and perception substates。
- **C2 数值守卫**: 🟡 — 原文给出 target-vehicle range/range uncertainty 用于 enabling/disabling visual sensing 和 triggering re-localization，且 detection confidence exceeds a predefined threshold 才更新 tracking state，但未给出复合 guard 公式。
- **C3 forced fault**: 🟢 — 原文明确说 global interrupt mechanism allows immediate transition to the RTH state from any active mode，且 RTH 可由 communication timeout、mission end 或 various failure modes 触发。
- **C4 硬件解耦**: 🟢 — 原文写 Pi issues navigation and actuation commands to the PX4 flight controller，PX4 performs real-time motor control，并可触发 Jetson GPU 开停视觉检测跟踪和选择性激活 visual sensing。
- **对 PATH2 的价值**: 该样本在 C1/C3/C4 上很强：真实 USV、层次 composite mode、any-state RTH 和异构硬件控制都能直接给 agent loop 提供 parse、semantic、sim grounding。NL 描述清楚，且属于自主海洋机器人任务监督，不容易与常见工业批处理或阀门样本同构。
- **风险**: 数值条件多来自叙述性可配置阈值，Figure 3 的 guard 标签较粗，C2 建模时需要补齐变量和阈值口径。

<details><summary><b>📝 扩充 NL（217 词 / 11 markers / 11 provenance entries）</b></summary>

**Expanded NL**:

> PIRATE's mission supervisor is a hierarchical finite-state machine: its high-level modes are composite states with internal substates that coordinate navigation, visual perception, and acoustic sensing [E1]. Within the tracking behavior, each cycle begins with acoustic triangulation, where the vehicle follows a predefined tracking geometry, receives acoustic range measurements, and estimates target location onboard [E2]. After that estimate, PIRATE transitions into pursuit and navigates directly toward the estimated target position [E3]. When PIRATE determines that it is within an operationally viable range of the tracked target, it activates the visual perception pipeline; the Pi can trigger the Jetson GPU to begin or terminate detection/tracking, and detector outputs are accepted only when confidence exceeds a predefined threshold [E4] [E5] [E6]. In loiter near the estimated target, the vehicle keeps receiving acoustic transmissions, uses ToF range estimates to assess target-vehicle distance, and collects underwater visual data [E7]. If range uncertainty increases or sustained range deviations reveal displacement, the controller can re-enter localization, re-estimate the target, and resume pursuit without reset or operator intervention [E8] [E9]. Navigation and actuation are carried through the PX4 flight controller and two independently controlled stern-mounted thrusters using differential thrust [E10]. From any active mode, an interrupt-driven failsafe can force immediate RTH; RTH can also be triggered by communication timeout, mission end, or failure modes [E11].

**Axis coverage**:

- **C1**: C1 由 [E1] 的层次化 composite modes 和 [E2][E3] 的 tracking cycle 先 triangulation 后 pursuit 暴露；原文只支持该顺序，不支持更细的默认子状态表。
- **C2**: C2 由 [E6] 的 detection confidence predefined threshold、[E7][E8] 的 ToF target-vehicle range 与 range uncertainty/re-localization 条件暴露；原文未给具体阈值数字。
- **C3**: C3 由 [E11] 的 any active mode / any state interrupt-driven RTH failsafe 暴露横切强制恢复语义。
- **C4**: C4 由 [E5] 的 Pi/Jetson 视觉任务触发、[E7] 的 acoustic/visual sensing、[E10] 的 PX4 与 stern-mounted thrusters 暴露硬件动作和传感器/执行器。

**Provenance** (11 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 B \| paper.pdf p.9 §3.2 / Figure 3 \| paper_content.txt 行 407-418 | organized hierarchically | hierarchical FSM with composite modes and internal substates coordinating nav… |
| [E2] | STM §1 摘录 C \| paper.pdf p.18 §5.4 \| paper_content.txt 行 771-775 | acoustic triangulation phase | tracking cycle begins with acoustic triangulation, tracking geometry, acousti… |
| [E3] | STM §1 摘录 C \| paper.pdf p.18 §5.4 \| paper_content.txt 行 775-777 | transitioned into a pursuit phase | transition from target estimate to pursuit toward the estimated target position |
| [E4] | paper.pdf p.11 §3.5 \| paper_content.txt 行 481-483 | pipeline is activated | visual perception activates after PIRATE determines operationally viable range |
| [E5] | paper.pdf p.9 §3.2 \| paper_content.txt 行 397-400 | triggered by the Pi | Pi requests Jetson/GPU visual tasks to begin or terminate and receives results |
| [E6] | paper.pdf p.11 §3.5 \| paper_content.txt 行 507-513 | predefined threshold | detector outputs accepted only when detection confidence clears a threshold |
| [E7] | STM §1 摘录 C \| paper.pdf p.18 §5.4 \| paper_content.txt 行 778-782 | underwater visual data | loiter phase keeps acoustic reception, uses ToF range estimates, and collects… |
| [E8] | paper.pdf p.11 §3.4 \| paper_content.txt 行 475-480 | triggering re-localization | range estimate supports re-localization when range uncertainty increases |
| [E9] | paper.pdf p.25 §6.5 \| paper_content.txt 行 1010-1016 | without reset or operator intervention | after detecting displacement, PIRATE re-enters localization, re-estimates, an… |
| [E10] | paper.pdf p.6-9 §§2.2,3.2 \| paper_content.txt 行 283-292, 395-396 | stern-mounted thrusters | PX4 motor control and differential thrust through two independently controlle… |
| [E11] | STM §1 摘录 B \| paper.pdf p.9-10 §3.2 / Figure 3 \| paper_content.txt 行 413-430 | RTH from any state | interrupt-driven failsafe from any active mode and RTH triggers such as timeo… |

**Intentional omissions**: 没有补充具体 confidence 阈值、range 阈值、waypoint tolerance 数值或传感器型号，因为相关原文没有给出可直接用于该 FSM 的精确数值。也没有列出全部 top-level mode 或编造 forced fault/valve/recovery path，只保留原文明确支持的 RTH failsafe 与 re-localization。

</details>


##### 5. `[207]` 🏭 Hierarchical vine-pruning autonomy supervisor (HSM-layered)

- **领域**: 🏭
- **论文**: paper #708 [`bumblebee-autonomous-robotic-vine-pruning`](../../../sources/bumblebee-autonomous-robotic-vine-pruning/STM.md)
- **是什么**: 这是 Bumblebee 葡萄藤自主修剪机器人的高层监督控制器，协调地面机器人导航、双目相机/3D 建模感知、7-DoF 机械臂与剪切末端执行器。典型流程是驶向葡萄藤位置、停止扫描建模、定位剪切点、执行机械臂剪切，再前往下一株。
- **scale**: states=10 / events=5 / vars=5 / trans=14
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文写明 FSM 外层状态为 navigation、perception、manipulation、error，且每个状态有 sub-modules 与 internal error sub-states，并由 success/failure/done 推进。
- **C2 数值守卫**: 🟡 — 原文剪枝规则含 n=No. of buds to keep、budindex[n]/budindex[n+1]、0.9 similarity threshold 和 retain 4 buds per cane，但宏状态转移主要仍是 success/failure/done。
- **C3 forced fault**: 🟢 — 原文明确说 each of the sub-processes 都 equipped with internal error sub-states，用于 self-diagnose 并在 hardware or unknown issues 时 pause all operations for manual intervention。
- **C4 硬件解耦**: 🟢 — 原文列出 7 DoF robot arm、ground robot、cutting end-effector、dual stereo cameras，完整周期还包括 navigating、scanning、executing motion plans to physically removing canes。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C1/C3/C4 都有强 grounding，且来自真实田间农业机器人系统，不是玩具 FSM。NL 摘要清晰、流程闭环完整，能测试 agent loop 对层次状态、异常归并和硬件动作解耦的修复收益。
- **风险**: 主要风险是 C2 数值守卫主要来自感知/剪枝子流程，图 13 的宏状态机本身数值 guard 不强。

<details><summary><b>📝 扩充 NL（266 词 / 14 markers / 14 provenance entries）</b></summary>

**Expanded NL**:

> The Bumblebee vine-pruning robot uses a finite-state high-level supervisor: after START it enters navigation, and the same controller then coordinates perception, manipulation, and a separate error path for autonomous pruning [E1] [E2]. The model is hierarchical because each macro phase owns a sub-module; for example, the navigation sub-module contains GPS Waypoint Follow and an internal error state, while manipulation contains Approach Target/Homing and an internal error state [E3]. In navigation, the vehicle RTK-GPS receiver, wheel encoders, and onboard IMU are fused by an EKF so the ground robot can follow waypoints, enter the other aisle when needed, and stop at each selected vine position [E4] [E5]. Perception scans the vine using a top-bottom stereo camera system on a linear slide, builds a 3D model, detects buds, and localizes cut points [E6] [E7]. The pruning decision uses a simplified spur-pruning rule that retains four buds per cane, so bud count is an explicit numeric constraint for cut-point selection [E8]. During manipulation, the motion planner first positions the cutting end-effector 15cm ahead of the cut point, orients it perpendicular to the branch, inches toward the final pose, and closes then opens the blades to mark a successful cut [E9] [E10] [E11]. Mode changes follow sub-module outcomes such as success, failure, and done, and the predefined sequence repeats until all vines are pruned [E12]. For robustness, each sub-process has an internal error sub-state for software self-diagnosis, while hardware or unknown issues pause all operations for manual intervention [E13]. The integrated platform includes a 7 DoF robot arm, ground robot, cutting end-effector, dual stereo cameras, RTK-GPS, and on-board computers [E14].

**Axis coverage**:

- **C1**: expanded_nl 通过 “after START it enters navigation” 和 “each macro phase owns a sub-module” 暴露了层次结构与入口线索，对应 [E1] [E3]；未额外推断各子模块内部默认子状态。
- **C2**: expanded_nl 只使用原文支持的数值约束：retain four buds per cane 与 15cm ahead of the cut point，对应 [E8] [E9]；原文未给出复合数值 guard，因此未编造 AND/OR 条件。
- **C3**: expanded_nl 用 “each sub-process has an internal error sub-state” 和 “pause all operations for manual intervention” 暴露横切异常处理语义，对应 [E13]；原文不支持 emergency forced transition。
- **C4**: expanded_nl 点出 RTK-GPS、wheel encoders、IMU、top-bottom stereo、cutting end-effector/blades、7 DoF arm 与 ground robot 等硬件 IO/effector，对应 [E4] [E6] [E9] [E10] [E11] [E14]。

**Provenance** (14 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | paper.pdf p.18 Figure 13 | START ... NAVIGATION | after START it enters navigation |
| [E2] | STM §1 摘录 C \| paper.pdf p.18 §4.5.2 \| paper_content.txt 行 726-733 | The states in the FSM were navigation, perception, manipulation, and error. | coordinates perception, manipulation, and a separate error path |
| [E3] | paper.pdf p.18 Figure 13 \| STM §1 摘录 B | NAVIGATION SUB-MODULE: GPS Waypoint Follow ... Internal Error State; MANIPULATION SUB-MODULE: App… | hierarchical sub-modules and selected internal phases |
| [E4] | paper.pdf p.16 §4.4 \| paper_content.txt 行 672-675 | The RTK-GPS receiver mounted on the vehicle, wheel encoders, and the robot’s onboard IMU ... were… | RTK-GPS, wheel encoders, IMU, and EKF-localized navigation |
| [E5] | paper.pdf p.16 §4.4 \| paper_content.txt 行 675-681 | drive the robot down the aisles, accurately turn and enter the aisle on the other side ... stoppi… | follow waypoints, enter the other aisle, and stop at vine positions |
| [E6] | paper.pdf p.9 §4.2.1 \| paper_content.txt 行 381-386 | uses two of these cameras ... in a top-bottom stereo configuration and moved along the linear slide | top-bottom stereo camera system on a linear slide |
| [E7] | paper.pdf p.9 §4.2 \| paper_content.txt 行 369-372 | acquiring static images from fourteen view points, point cloud registration ... bud detection ...… | 3D modeling, bud detection, and cut-point localization |
| [E8] | paper.pdf p.19 §5.1 \| paper_content.txt 行 761-763 | the simplified spur pruning rule adopted in this study only required to retain 4 buds per cane. | four buds per cane as numeric pruning constraint |
| [E9] | paper.pdf p.15 §4.3.1 \| paper_content.txt 行 634-637 | positioning the tool 15cm ahead of that cut-point | 15cm initial end-effector offset |
| [E10] | paper.pdf p.15 §4.3.1 \| paper_content.txt 行 637-641 | the end-effector was commanded to orientate perpendicularly to the branch that contains the pruni… | perpendicular end-effector orientation and final approach setup |
| [E11] | paper.pdf p.15 §4.3.1 \| paper_content.txt 行 641-642 | Then the blades closed and opened to mark the end of a successful cut operation. | blade close/open effector action |
| [E12] | paper.pdf p.18 Figure 13 / §4.5.2 \| paper_content.txt 行 730-735 | SUCCESS FAILURE DONE; transitions between different states following a pre-defined sequence ... u… | success/failure/done outcomes and repeated predefined sequence |
| [E13] | STM §1 摘录 C \| paper.pdf p.18 §4.5.2 \| paper_content.txt 行 733-736 | internal error sub-states to self-diagnose software level issues and pause all operations for man… | cross-cutting internal error handling and manual-intervention pause |
| [E14] | paper.pdf p.18 Figure 12 / caption \| paper_content.txt 行 723-724 | RTK-GPS; Integrated robotic system with 7 DoF robot arm, ground robot, cutting end-effector, dual… | named physical platform, sensors, and effectors |

**Intentional omissions**: 未加入 valve 编号、emergency-stop、forced fault 恢复路径或复杂阈值 guard，因为原文只支持 internal error、pause operations 和 manual intervention。也未把几何角度或 MPC 公式改写成 DSL guard，以免引入原文未声明的控制判定条件。

</details>


##### 6. `[160]` ✈️ Mission-Mode / Command-Mode VTOL UAV Supervisor (HSM-layered)

- **领域**: ✈️
- **论文**: paper #543 [`onboard-mission-management-vtol-uav-sequence-supervisory-control`](../../../sources/onboard-mission-management-vtol-uav-sequence-supervisory-control/STM.md)
- **是什么**: 该 case 控制 VTOL 无人机机载任务管理器：监督层根据操作者、数据链路、payload/传感输入选择 Fly Home 或 Search and Track 等高层目标，序列层把 mission plan 解析成行为并向飞控输出轨迹/速度/位置类命令。典型流程是 Mission Mode 解析并执行任务行为，遇到直接命令、stop/manual、链路丢失或高层目标时切换到 Command Mode、Stand By、Slow Down、Mission Controller Off 或监督行为。
- **scale**: states=10 / events=20 / vars=8 / trans=24
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文明确说 Sequence Control System 有 “two hierarchical levels”，且 `Mission Mode` 与 `Command Mode` 是 composite states，并且 `Command Mode` 可从 `Mission Mode` 内 every state 进入。
- **C2 数值守卫**: 🟢 — 原文 runtime plausibility checks 包含 height parameter、allowed maximum velocity、maximum flight height restrictions，以及 movement behavior 的 end/start position spatial discrepancy。
- **C3 forced fault**: 🟢 — 原文写到 every state of the top level 都有到 `Mission Controller Off` 的 manual control transition，且 stop command 有 from every auto mode state 的 transition。
- **C4 硬件解耦**: 🟡 — 原文说行为生成 trajectory-based control commands fed into the flight controller，并在安全切换时 stop producing actuator commands，但未展开到多个具体电机/舵机级执行器。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C1/C3 都有清晰的层次状态和跨 mode 强制切换，C2 还有 mission/command plausibility 的数值语义检查，能支撑 parse + semantic + sim 的 in-loop feedback。它也是较真实的 UAV 工业控制对象，NL 描述边界清楚，和简单 takeoff/landing 三段式样本不完全同构。
- **风险**: 行为库内部状态没有全部展开，部分数值 guard 来自 runtime plausibility checks 而不是 Fig.3 顶层状态图本身。

<details><summary><b>📝 扩充 NL（279 词 / 24 markers / 24 provenance entries）</b></summary>

**Expanded NL**:

> The Sequence Control System is modeled as UML 1.2 state charts [E1], with exactly one state active at a time [E2]. It has two hierarchical levels whose top level models procedural flow [E3], and Mission Mode and Command Mode separate mission-plan processing from direct command execution [E4]. In auto mode, Stand By lets the UAV hover where it was entered [E5], while Slow Down gives a smooth changeover into Stand By regardless of the current flight maneuver [E6]. Mission Mode contains the behavior library, allows only one behavior to be active [E7], and returns each behavior through a termination condition to Parse Command, which reads behavior commands from the mission plan [E8]. Payload-directed flight can enter Command Mode from every state inside Mission Mode [E9], while a static truth table checks valid combinations for payload-directed flight and operator manual interruption [E10]. Mission-sequence plausibility is handled by grammar [E11] and attribute checks that constrain behavior parameters by expected degree ranges [E12], allowed maximum movement velocity and maximum flight height [E13], and consistency between consecutive movement start and end positions [E14]. Manual-control and stop events cut across the hierarchy: every top-level state can move to Mission Controller Off [E15], every auto-mode state can accept a stop command [E16], and switching to manual mode outranks stopping [E17]. The Supervisory Control System runs before the sequence layer at every instant [E18], reacts to data-link loss [E19], may modify missions [E20], and can command high-level objectives such as Fly Home [E21]. In ARTIS integration [E22], the Mission Manager runs on the flight-control computer and commands the flight controller every cycle [E23], and uses vehicle state estimates plus ground-distance sensor state as main inputs [E24].

**Axis coverage**:

- **C1**: 有 C1 钩子：[E3][E4] 暴露 two hierarchical levels 与 Mission Mode / Command Mode 复合状态，[E7][E8] 暴露 Mission Mode 内部行为库与 Parse Command 回跳；但原文未给进入复合状态的默认初始子状态。
- **C2**: 有弱 C2 钩子：[E11]-[E14] 暴露 grammar/attribute plausibility checks、degree range、maximum velocity、maximum flight height、start/end position consistency；原文没有给具体数值阈值。
- **C3**: 有 C3 钩子：[E15]-[E17] 暴露 every top-level state/manual off、every auto-mode state/stop command、manual-over-stop priority 这种横切/强制转移语义。
- **C4**: 有弱 C4 钩子：[E22]-[E24] 暴露 flight-control computer、每 cycle command flight controller、vehicle state estimates 与 ground-distance sensor；原文不支持具名阀/泵/电机等物理 effector。

**Provenance** (24 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | paper.pdf p.6 §4.3 \| paper_content.txt 行 370 | Thus, the Sequence Control System is modelled as UML 1.2 State Charts. | Sequence Control System is modeled as UML 1.2 state charts |
| [E2] | paper.pdf p.6 §4.3 \| paper_content.txt 行 371-372 | exactly one state is active at a time | exactly one state active at a time |
| [E3] | STM §1 摘录 A \| paper.pdf pp.6-7 Fig.3/§4.3 \| paper_content.txt 行 381-382 | It has two hierarchical levels where the top level models the procedural flow for a safe operation. | two hierarchical levels and top-level procedural flow |
| [E4] | STM §1 摘录 A \| paper.pdf pp.6-7 Fig.3/§4.3 \| paper_content.txt 行 383-384 | The two composite states, ”Mission Mode” and ”Command Mode”, model mission plan processing and di… | Mission Mode and Command Mode separate mission-plan processing from direct co… |
| [E5] | STM §1 摘录 A \| paper.pdf p.7 §4.3 \| paper_content.txt 行 386-388 | ”Stand By” lets the UAV hover at its current position when the state was entered | Stand By lets the UAV hover where it was entered |
| [E6] | STM §1 摘录 A \| paper.pdf p.7 §4.3 \| paper_content.txt 行 388-390 | The state ”Slow Down” is necessary to assure a smooth changeover into ”Stand By” regardless of th… | Slow Down gives a smooth changeover into Stand By regardless of maneuver |
| [E7] | STM §1 摘录 A \| paper.pdf p.7 §4.3 \| paper_content.txt 行 395-397 | The state mission mode contains the actual library of behaviors. There are no transitions among b… | Mission Mode behavior library and only one active behavior |
| [E8] | STM §1 摘录 A \| paper.pdf p.7 §4.3 \| paper_content.txt 行 397-400 | For each behavior there exists a termination condition, which transits into the command parser ”P… | termination to Parse Command and reading behavior commands from the mission plan |
| [E9] | STM §1 摘录 A \| paper.pdf p.7 §4.3 \| paper_content.txt 行 401-403 | the composite state ”Command Mode” can be entered from every state inside “Mission Mode”. | payload-directed flight can enter Command Mode from every Mission Mode state |
| [E10] | paper.pdf p.10 §4.6 \| paper_content.txt 行 622-624 | It checks valid combinations for payload directed flight and manual interruption of missions by t… | truth table checks valid payload-directed/operator interruption combinations |
| [E11] | paper.pdf p.10 §4.6 \| paper_content.txt 行 627-631 | it is possible to implement a plausibility check using a language grammar. | mission-sequence plausibility handled by grammar |
| [E12] | paper.pdf p.11 §4.6 \| paper_content.txt 行 648-653 | semantic actions are particularly important tools to check floating point values against their “m… | attribute checks and expected degree ranges |
| [E13] | paper.pdf p.11 §4.6 \| paper_content.txt 行 653-656 | it checks against an allowed maximum velocity of a movement behavior or maximum flight height res… | allowed maximum movement velocity and maximum flight height |
| [E14] | paper.pdf p.11 §4.6 \| paper_content.txt 行 656-658 | A start position of a behavior must always match the expected end position of a previous behavior. | consecutive movement start/end position consistency |
| [E15] | STM §1 摘录 A \| paper.pdf pp.6-7 §4.3 \| paper_content.txt 行 384-386 | Every state of the top level has a transition to the ”Mission Controller Oﬀ” to handle a manual c… | every top-level state can move to Mission Controller Off |
| [E16] | STM §1 摘录 A \| paper.pdf p.7 §4.3 \| paper_content.txt 行 390-391 | a transition from every auto mode state assures that the command is executed. | every auto-mode state can accept a stop command |
| [E17] | STM §1 摘录 A \| paper.pdf p.7 §4.3 \| paper_content.txt 行 391-394 | an event switching to manual mode is more important than a stop command | manual mode outranks stopping |
| [E18] | STM §1 摘录 B \| paper.pdf p.7 §4.4 \| paper_content.txt 行 409 | It is executed before the Sequence Control System at every instant of time. | Supervisor runs before the sequence layer every instant |
| [E19] | STM §1 摘录 B \| paper.pdf p.7 §4.4 \| paper_content.txt 行 407-409 | reacting to a loss of the data link. | reacts to data-link loss |
| [E20] | STM §1 摘录 B \| paper.pdf p.7 §4.4 \| paper_content.txt 行 410-411 | This allows the Supervisory Control System to modify a mission | may modify missions |
| [E21] | STM §1 摘录 B \| paper.pdf p.7 §4.4 \| paper_content.txt 行 416-417 | the Supervisor retains planning capabilities, and recognizes associated high-level mission object… | can command high-level objectives such as Fly Home |
| [E22] | paper.pdf p.12 §5 \| paper_content.txt 行 723-724 | The Mission Management system is integrated onboard the Autonomous Rotorcraft Testbed for Intelli… | ARTIS integration |
| [E23] | paper.pdf p.13 §5 \| paper_content.txt 行 766-767 | The Mission Manager is integrated onboard the flight control computer as a component commanding d… | flight-control computer and every-cycle commands to the flight controller |
| [E24] | paper.pdf p.13 §5 \| paper_content.txt 行 767-769 | The vehicle state estimates (e.g. position, velocities, acceleration) and further sensor states (… | vehicle state estimates and ground-distance sensor state as inputs |

**Intentional omissions**: 没有写具体数值阈值、阀门/电机/旋翼编号、传感器型号或 forced fault/recovery path，因为原文没有这些细节。也没有写进入 Mission Mode 或 Command Mode 时默认从哪个子状态开始，因为原文只支持层次结构与 Parse Command 回跳，不支持初始伪状态/默认相位。

</details>


#### EFSM-interlock （6 条）

##### 1. `[142]` 🏭 HMI-Configured Cup Filling, Capping, and Labeling Line (EFSM-interlock)

- **领域**: 🏭
- **论文**: paper #493 [`plc-scada-liquid-filling-automation-ejosat`](../../../sources/plc-scada-liquid-filling-automation-ejosat/STM.md)
- **是什么**: 这是 PLC/SCADA 控制的杯装液体灌装线：操作者在 HMI 选择产品、克重和产量，PLC 依据液位、loadcell 重量与编码器反馈驱动阀门、输送带、真空/气缸封盖和贴标。典型流程是配方输入、重量闭环灌装、五步封盖、按单品/混合贴标并送至出口。
- **scale**: states=13 / events=18 / vars=11 / trans=21
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文说系统有“ana dört adet proses”且主过程内有“birçok yardımcı proses”，封盖又有 5 个步骤并在步骤错误时“tüm işlemleri baştan başlar”，有阶段/子流程切换但不是显式层次状态机。
- **C2 数值守卫**: 🟢 — 原文给出产品“gramajları belirlenir”、产量默认“10 adet”上限、液位达到期望且收到灌装信号才开阀，以及“istenen ağırlığa geldiğinde”关闭阀门，另有步进电机脉冲与编码器比较。
- **C3 forced fault**: 🟢 — 原文写“herhangi bir ürün bittiğinde üretim durur ve sistem alarm verir”，并且主/辅助过程执行时“herhangi bir problem”会报警、修正后继续，适合抽成跨阶段 fault/recovery。
- **C4 硬件解耦**: 🟢 — 原文明确列出输出“motor, valf, alarm”，并具体包含 pnömatik vanalar、electropneumatic valves、step motor、vacuum、milsiz silindir 等物理执行器。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C2 数值 guard、C3 报警恢复、C4 多执行器硬件解耦都很清楚，且是典型工业 PLC/SCADA 产线对象。NL 描述相对独立完整，能支撑 parse/semantic/sim 闭环反馈。
- **风险**: C1 不是强层次状态机，原文主要是流程图和设备说明；建模时需主动结构化封盖五步、报警恢复和输送带闭环，否则可能退化成普通顺序流程。 

<details><summary><b>📝 扩充 NL（248 词 / 12 markers / 12 provenance entries）</b></summary>

**Expanded NL**:

> The controller manages a prototype PLC/SCADA liquid-filling line through an HMI panel [E1]. At setup, the HMI lets one or more of four products be selected, assigns gram values, and records the production count with a default maximum of 10 units [E1][E2]. Filling starts only when the tank level is at the desired level AND the filling signal arrives; then electropneumatic valves open, and loadcell weight feedback closes the valve when the cup reaches the desired weight [E3][E4]. Tank level comes from pressure transmitters with a 0-250 mBar range and 4-20 mA or 0-10 V analog output [E5]. Capping is a separate phase sequence that includes cup arrival, lid transfer by vacuum to the cup position, a 50 mm vertical attachment motion, and return of the rodless cylinder plus vacuum to the initial position [E6][E7]. If one or more capping steps fail, the whole capping process restarts; when completed correctly, labeling begins [E8]. Labeling uses the product-selection count: multiple selected products mixed at requested ratios get a mixed label, while a single selected product gets a pure label regardless of quantity [E9]. Conveyor movement uses step motor 86HS45 and M542 driver; PLC pulse counts determine motor turns and travel distance [E10]. Encoder feedback on the tension drum closes the loop, so if a move signal is sent but the motor or belt prevents movement, encoder information detects the error [E11]. Across main and auxiliary processes, any problem causes a warning; after correction, operation resumes where it stopped [E12].

**Axis coverage**:

- **C1**: 原文没有明确状态层级名，但 expanded_nl 将 capping 写成 separate phase sequence，并给出进入后从 cup arrival 开始、最后回到 initial position 的阶段边界，对应 [E6][E7]。
- **C2**: C2 钩子来自 production_count 默认最大 10、tank_level desired AND filling_signal 的复合守卫、0-250 mBar/4-20 mA/0-10 V 传感器范围和 desired_weight/loadcell 关阀条件，对应 [E2][E3][E4][E5]。
- **C3**: C3 钩子来自 capping step failure 整体重启，以及 main/auxiliary processes 中 any problem 触发 warning 后修正并续做的横切异常语义，对应 [E8][E12]。
- **C4**: C4 钩子来自 HMI、electropneumatic valves、pressure transmitters、loadcell、vacuum、rodless cylinder、step motor 86HS45、M542 driver 和 encoder 等具名硬件/IO，对应 [E1][E3][E4][E5][E6][E7][E10][E11]。

**Provenance** (12 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 54-57 | This study has been performed by programming PLC on the prototype liquid filling system... The SC… | prototype PLC/SCADA liquid-filling line; HMI panel control |
| [E2] | STM §1 摘录 B \| paper.pdf p.4 SCADA/HMI screen description \| paper_content.txt 行 320-325 | 4 adet farklı ürün bulunmaktadır. Bu ürünlerden biri veya birkaçı seçilerek gramajları belirlenir… | one or more of four products, gram values, production count, default maximum … |
| [E3] | STM §1 摘录 B \| paper.pdf pp.5-6 §2.2.1 \| paper_content.txt 行 400-411 | Sıvı seviye ölçümünün istenilen düzeyde olması ve dolum sinyalinin gelmesi ile pnömatik vanalar a… | compound filling guard and electropneumatic valve opening |
| [E4] | STM §1 摘录 B \| paper.pdf p.6 §2.2.1 \| paper_content.txt 行 412-425 | Bardak istenen ağırlığa geldiğinde vananın kapatılması... yük hücresi (loadcell) adı verilen sens… | loadcell weight feedback closes the valve at desired cup weight |
| [E5] | paper.pdf p.5 §2.2.1 \| paper_content.txt 行 385-389 | Basınç transmitteri 0-250 mBar basınç ölçüm aralığına sahiptir... 4-20 mA veya 0-10 V arasında an… | pressure transmitter range and analog output values |
| [E6] | STM §1 摘录 C \| paper.pdf p.6 §2.2.2 \| paper_content.txt 行 444-455 | Kapak takma istasyonuna bardak gelir. Kapak deposundan kapak taşıma yerine itilir... kapak vakum … | capping sequence begins with cup arrival, lid push, and vacuum transfer |
| [E7] | STM §1 摘录 C \| paper.pdf p.6 §2.2.2 \| paper_content.txt 行 456-457 | 50 milimetrelik dikey eksen hareketiyle kapak takılır. Milsiz silindir ve vakum başlangıç konumun… | 50 mm vertical attachment and return to initial position |
| [E8] | STM §1 摘录 C \| paper.pdf p.6 §2.2.2 \| paper_content.txt 行 458-462 | hata olması halinde prosesin tüm işlemleri baştan başlar... Kapak takma prosesinin tamamlanmasını… | capping failure restart and transition to labeling after successful completion |
| [E9] | STM §1 摘录 C \| paper.pdf p.6 §2.2.3 \| paper_content.txt 行 466-473 | Birden fazla ürün seçilip istenilen oranlarda karıştırılmasıyla... karışık etiketi basılır. Tek ü… | mixed label for multiple products and pure label for single product |
| [E10] | paper.pdf p.6 §2.2.4 \| paper_content.txt 行 478-488 | Konveyör bant bir step motor (86HS45) ile hareket ettirilmekte ve kontrolü için sürücü (M542) kul… | step motor 86HS45, M542 driver, and PLC pulse-count movement control |
| [E11] | STM §1 摘录 C \| paper.pdf p.7 §2.2.4 \| paper_content.txt 行 512-529 | enkoderin mili dairesel dönüş yapan gergi tamburuna bağlanır... hareket sağlanmazsa enkoder bilgi… | encoder on tension drum detects motor or conveyor movement failure |
| [E12] | paper.pdf p.6 §2.2.1 \| paper_content.txt 行 436-442 | herhangi bir problem oluşması halinde otomasyon sistemi uyarı verir... işlemlere kaldığı yerden d… | cross-process warning and resume-from-stopped-point recovery |

**Intentional omissions**: 没有写 valve 编号、具体 PLC I/O 地址、传感器 tag、超时阈值或 forced emergency-stop 路径，因为原文只说明存在急停按钮/报警/恢复，不支持更具体的全局强制迁移。也没有补充 sin/log/exp 等数学函数或完整状态名清单。

</details>


##### 2. `[234]` 🅿️ Multi-level parking lift auto/manual positioning controller (EFSM-interlock)

- **领域**: 🅿️
- **论文**: paper #775 [`lift-control-automatic-car-parking-using-plc`](../../../sources/lift-control-automatic-car-parking-using-plc/STM.md)
- **是什么**: 该 case 控制多层自动停车库的 PLC 升降机，用 VFD 驱动升降电机，并用叉形传感器、托盘位置传感器、停层确认传感器和安全互锁完成自动/手动定位。典型流程是自动接收目标层命令，计算层差和方向，快速运行、接近后降速、停层确认，异常时进入错误/急停路径。
- **scale**: states=11 / events=13 / vars=8 / trans=20
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文写明“There are two types of sequences manual mode sequence and auto mode sequence”，但流程主要是手动/自动两套扁平序列，没有明确层次化 composite/init/pseudo 语义。
- **C2 数值守卫**: 🟢 — 原文给出“Number of levels to move = destination level no - source level no”，并用层差正负决定上下行、用 counter 初始化和 Counter=0 判断运行结束。
- **C3 forced fault**: 🟢 — 原文结论写“Whenever an alarm occurs whole lift goes into emergency case”，且安全传感器在上下行时 cut and stop lift，适合抽成全局 fault/emergency transition。
- **C4 硬件解耦**: 🟢 — 原文列出 PLC 到 VFD 的 Forward、Backward、slow speed、high speed、reset 命令，并在 I/O testing 中提到 actuators like lamp, motor, buzzer。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C2 的层差/计数器数值守卫清楚，C3/C4 又有全局报警急停和明确硬件执行器，可同时测试 symbolic guard feedback、forced fault recovery 和 abstract handler。NL 结构独立且工业控制对象典型。
- **风险**: 与电梯/升降机类样本存在一定同构风险，且原文流程图较粗，部分状态边界需要从文本和图中保守重建。

<details><summary><b>📝 扩充 NL（269 词 / 21 markers / 21 provenance entries）</b></summary>

**Expanded NL**:

> The controller belongs to a fully automatic level car-parking lift system used to take cars in and out and park them [E1], and the described installation has two lifts, three level-transfer mechanisms, one Beckhoff PLC, and VFD speed control for acceleration, deceleration, and stopping accuracy [E2][E3]. Dedicated sensing covers pallet position, lift-level positioning, safety interlocks, fork sensing for speed reduction, and slat-position confirmation for checking correct position [E4][E5][E6]. The operational sequence is divided into manual and auto modes: manual mode is inching for maintenance through spring-action up/down commands from the HMI or teach pendant at slow speed [E7][E8][E9]. Auto mode starts from a waiting-for-command phase; the command states direction and number of levels, and the lift then moves in the commanded direction [E10][E11]. The movement decision uses the signed difference destination level minus source level: the formula is shown as destination level no minus source level no, a negative result selects upward travel and initializes the level counter to one, while a positive example gives a down command with two levels to move [E12][E13][E14]. During automatic travel, fork-sensor input reduces VFD speed, and the stop fork sensor stops the lift [E15]. After stopping, level-position and level-confirmation sensors are checked; if a level difference remains, the confirmation sensor is absent and an error is given [E16][E17]. Across both upward and downward movements, Height/AntiLift sensors cut and stop operation when pallet engagement is improper, while over-travel sensors alarm when the lift goes above safe position limits [E18][E19]. The PLC-to-VFD interface exposes Forward, Backward, slow-speed, high-speed, and reset commands, and the PLC receives Run and Fault status feedback from the VFD [E20][E21].

**Axis coverage**:

- **C1**: [E7]-[E10] 暴露了手动/自动 mode 边界，并把 auto mode 的进入起点写成 waiting-for-command phase；原文没有更深层层次结构，未编造子状态树。
- **C2**: [E11]-[E14] 暴露了 destination level、source level、signed difference、level counter 这些数值变量与 difference < 0 上行、positive 下行的自然语言 guard。
- **C3**: [E18][E19] 暴露了 up/down movement 范围内的横切安全语义：Height/AntiLift 可切断并停止运行，over-travel 可报警；原文不支持更强的 any-state emergency forced transition。
- **C4**: [E5][E15][E20][E21] 暴露了 fork sensor、stop fork sensor、VFD Forward/Backward/slow/high/reset 命令和 Run/Fault feedback 等物理 I/O 与 effector。

**Provenance** (21 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 15-17 | In this paper a novel approach for lift control is proposed in fully automatic Level Car Parking … | fully automatic level car-parking lift system used to take cars in and out an… |
| [E2] | STM §1 摘录 A \| paper.pdf p.1 §1 INTRODUCTION \| paper_content.txt 行 58-62 | The total system is having two lifts, three level transfer mechanisms. A single PLC (BECKHOFF PLC… | two lifts, three level-transfer mechanisms, one Beckhoff PLC |
| [E3] | STM §1 摘录 A \| paper.pdf p.1 §1 INTRODUCTION \| paper_content.txt 行 62-64 | For accurate speed control lift is operated with VFD. Speed control is required for acceleration/… | VFD speed control for acceleration, deceleration, and stopping accuracy |
| [E4] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 17-20 | The pallet position on lift, accurate positioning between lift-level & safety interlocks are sens… | dedicated sensing covers pallet position, lift-level positioning, and safety … |
| [E5] | STM §1 摘录 B \| paper.pdf p.1 §2 OVERVIEW DIAGRAM OF LIFT \| paper_content.txt 行 82-84 | Fork sensor. This sensor is fixed and the dogs are mounted at each slat location. When input from… | fork sensing for speed reduction |
| [E6] | STM §1 摘录 B \| paper.pdf p.1 §2 OVERVIEW DIAGRAM OF LIFT \| paper_content.txt 行 85-88 | Slat Position confirmation sensor: This is a retro-reflective sensor. This sensor are be used to … | slat-position confirmation for checking correct position |
| [E7] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 145-147 | There are two types of sequences manual mode sequence and auto mode sequence. | operational sequence is divided into manual and auto modes |
| [E8] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 149-151 | The lift manual mode operation is inching. The lift inched with spring action button in up or dow… | manual mode is inching for maintenance through spring-action up/down commands |
| [E9] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 151-154 | The speed in the manual/maintenance mode is slow speed. All manual mode actions are done from the… | HMI or teach pendant commands at slow speed |
| [E10] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 159-161 | lift is always waiting for command in auto mode. The command given to the lift is in terms of dir… | auto mode starts waiting for a command containing direction and number of levels |
| [E11] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 161-163 | depending upon the command direction lift starts to move respective direction | the lift moves in the commanded direction |
| [E12] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 171-178 | Number of levels to move = destination level no – source level no = 1 – 2 = -1. I.e. Counter valu… | destination level minus source level and signed negative example |
| [E13] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 178-180 | Since the number of levels to move < 0 so the direction is be up and the level counter is initial… | negative result selects upward travel and initializes the level counter to one |
| [E14] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 185-189 | Here no of levels is positive, it means that lift has given down command & two levels to move. | positive example gives a down command with two levels to move |
| [E15] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 163-165 | Once slow sensor(fork sensor) is sensed the speed of the VFD is made slow. As soon as the stop se… | fork-sensor input reduces VFD speed and stop fork sensor stops the lift |
| [E16] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 165-167 | The level position sensors are checked to ensure that the lift is stopped correctly. | after stopping, level-position sensors are checked |
| [E17] | STM §1 摘录 C \| paper.pdf p.3 §4 OPERATIONAL SEQUENCE \| paper_content.txt 行 167-169 | If there is a level difference, then the level confirmation sensor will not be sensed and error w… | missing level confirmation when a level difference remains and an error is given |
| [E18] | STM §1 摘录 B \| paper.pdf p.2 §2 OVERVIEW DIAGRAM OF LIFT \| paper_content.txt 行 100-102 | If the lift pallet not engaged properly during up/down movements, then Height/AntiLift sensors cu… | Height/AntiLift cut and stop operation during up/down movement when pallet en… |
| [E19] | STM §1 摘录 B \| paper.pdf p.2 §2 OVERVIEW DIAGRAM OF LIFT \| paper_content.txt 行 102-104 | The over travel sensors used to alarm the system that lift is going above the safe position limits. | over-travel sensors alarm when the lift goes above safe position limits |
| [E20] | STM §1 摘录 B \| paper.pdf p.2 §3 ELECTRICAL WIRING DIAGRAM OF VFD \| paper_content.txt 行 118-120 | The control signals received from the PLC to VFD are Commands as Forward, Backward, slow speed, h… | PLC-to-VFD Forward, Backward, slow-speed, high-speed, and reset commands |
| [E21] | STM §1 摘录 B \| paper.pdf p.2 §3 ELECTRICAL WIRING DIAGRAM OF VFD \| paper_content.txt 行 120-121 | PLC receives feedback from VFD in terms of Run & Fault status signals. | Run and Fault status feedback from the VFD |

**Intentional omissions**: 没有加入阀门编号、压力/温度阈值、传感器型号、任意状态急停、自动恢复路径或 sin/log/exp 等数学函数，因为原文没有支持。也没有列出完整 flowchart state name 或长 I/O 表，只保留 mode、level difference、fork/confirmation/safety sensors 与 VFD 命令。

</details>


##### 3. `[114]` 🅿️ Slot-Selected Rotary Parking and Retrieval Controller (EFSM-interlock)

- **领域**: 🅿️
- **论文**: paper #414 [`vertical-rotary-car-parking-plc-outseal`](../../../sources/vertical-rotary-car-parking-plc-outseal/STM.md)
- **是什么**: 该 case 控制一个 8 车位垂直旋转停车库，PLC Outseal 读取 proximity/IR 传感器与 Android HMI 指令，驱动入口栏杆电机、旋转车库电机、继电器和 LED。典型流程是 Start 后检测进车、校验车辆位置、HMI 选车位并旋转停车，取车时选择车位、旋转到底部、人工确认 BENAR 后开闸放行。
- **scale**: states=12 / events=18 / vars=6 / trans=24
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文 HMI 表把系统分成 Utama、Parkir Mobil、Ambil Mobil、Validasi Ambil Mobil、Darurat、Bagian Reset 等屏幕/模式，并有 Parkir/Ambil/SALAH 重试/急停分支，但未明确给出层次化 composite state 或 init/pseudo 语义。
- **C2 数值守卫**: 🟢 — 原文表 3 同时记录 “Jumlah Mobil di Area Parkir” 与 “Nomor Ruang Parkir”，并写到车辆进出会增加/减少数量、HMI 有 “Reset Jumlah” 和 “Reset Counter” 用于车数与车位移动计数，可形成 count<8、current_slot==selected_slot 等数值 guard。
- **C3 forced fault**: 🟡 — 原文把 “Keadaan darurat” 定义为流程不符合系统、用户取消停车/取车、车位移动计数错误或灾害等情况，并提供 “DARURAT ON/OFF”、CW/CCW、Palang Buka/Tutup，但没有明确说 from any state。
- **C4 硬件解耦**: 🟢 — 原文列出 “lampu led dan motor DC sebagai keluaran”，并说明继电器用于 motor DC CW/CCW 换向，另有入口 palang pintu 电机、rotary parking 电机和红/绿/黄 LED 输出。
- **对 PATH2 的价值**: 该样本对 PATH2 有价值，主要强在 C2 的车位号/车辆数/移动 counter 数值 EFSM，以及 C4 的多硬件输出解耦；同时它是典型 PLC 工业控制对象，NL 流程从进车、停车、取车到 emergency/reset 都比较完整。
- **风险**: 原文是实现与测试说明，不是形式化需求；C1 层次结构和 C3 任意状态故障切换需要从 HMI 模式与 emergency 描述归纳，不能按强层次/强 cross-cutting 样本处理。

<details><summary><b>📝 扩充 NL（267 词 / 24 markers / 24 provenance entries）</b></summary>

**Expanded NL**:

> The controller manages a prototype vertical rotary parking system with eight slots, PLC Outseal, Android HMI, proximity/infrared sensors, LEDs, and DC motors, including a rotary motor for moving parking spaces in and out [E1] [E2] [E3]. A relay protects the DC motor and reverses its rotation for CW/CCW movement [E4]. Operation starts with ON/Start and a green active LED; during entry, the proximity sensor opens the barrier when space is available, but the barrier motor remains closed with the red LED on when the lot is full [E5] [E6] [E7]. Infrared sensor 1 is the readiness guard: ON means the car is ready to park, while OFF means the position is wrong and the user must adjust it [E8] [E9]. For parking, the operator uses the HMI Parkir Mobil screen, chooses slot 1-8, presses OK, and the rotary motor runs until infrared sensor 2 detects a passing parking space, then stops [E10] [E11] [E12]. For retrieval, Ambil Mobil plus a slot number and OK makes the rotary motor move the car downward CW/CCW until the selected HMI slot is below, turning the yellow LED on and the rotary motor off [E13] [E14] [E15]. The validation step opens the barrier only after BENAR; SALAH sends the operator back to repeat Ambil Mobil [E16] [E17]. After exit, proximity detection closes the barrier again, turns the yellow LED off, and supports decrementing the parked-vehicle count [E18] [E19]. The HMI also exposes emergency and reset recovery: DARURAT ON/OFF, CW/CCW lowering, gate open/close, Reset Jumlah, and Reset Counter for cancelled parking/retrieval, parking-space movement counting errors, or disasters [E20] [E21] [E22] [E23] [E24].

**Axis coverage**:

- **C1**: 原文无正式层次状态或进入某 mode 的默认子状态，expanded_nl 只保留 HMI screen / phase 边界如 Parkir Mobil、Ambil Mobil、validation 与 emergency，见 [E10][E13][E16][E20]，不硬写严格 C1 钩子。
- **C2**: C2 只由原文支持的离散守卫暴露：slot 1-8、满位、IR1 ON/OFF、所选 HMI 槽位到底部，见 [E1][E7][E8][E9][E11][E15]；原文无连续阈值或时间约束。
- **C3**: 原文不支持 any-state forced transition 或每周期 aspect，只支持 emergency/recovery UI 用于取消、计数错误和灾害等情况，见 [E20][E21][E22][E23][E24]。
- **C4**: C4 明确支持，expanded_nl 写出 PLC/HMI、proximity/infrared sensors、LED、DC motor、relay、barrier、CW/CCW rotary motion 与 reset/gate controls，见 [E2][E3][E4][E6][E12][E14][E18][E21][E22][E23][E24]。

**Provenance** (24 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 36-38 | a prototype of a vertical rotating parking system with 8 parking spaces was made and controlled u… | prototype vertical rotary parking system with eight slots, PLC Outseal, Andro… |
| [E2] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 39-40 | The rotating parking lot uses a DC Motor that will rotate the vehicle parking lot to enter or exit. | rotary motor for moving parking spaces in and out |
| [E3] | STM §1 摘录 A \| paper.pdf p.3 Metodologi Penelitian \| paper_content.txt 行 103-105 | sensor proximity, sensor infrared dan push button sebagai masukan, lampu led dan motor DC sebagai… | proximity/infrared sensors, LEDs, and DC motors |
| [E4] | STM §1 摘录 A \| paper.pdf p.3 Metodologi Penelitian \| paper_content.txt 行 105-106 | Relay berfungsi untuk melindungi motor DC dari kelebihan tegangan dan sebagai pembalik arah putar… | relay protects the DC motor and reverses rotation for CW/CCW movement |
| [E5] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 134-136 | Untuk menjalankan sistem harus menekan tombol ON (Start) dan untuk mematikan sistem maka harus me… | ON/Start, OFF/Stop, and green active LED |
| [E6] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 138-140 | sensor proximity akan ON dan motor DC menggerakan palang pintu untuk terbuka | proximity sensor opens the barrier when space is available |
| [E7] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 140-142 | ruang parkir sudah penuh maka motor DC penggerak palang tetap tertutup kondisi led merah ON menan… | full lot guard, closed barrier motor, red LED on, green LED off |
| [E8] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 142-144 | jika sensor infrared 1 ON kondisi led hijau 2 ON menandakan bahwa kendaraan sudah siap parkir | infrared sensor 1 ON means ready to park |
| [E9] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 144-146 | jika sensor infrared 1 OFF menandakan bahwa kendaraan masih belum sesuai atau posisi mobil belum … | infrared sensor 1 OFF means wrong position and user adjustment |
| [E10] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 147-150 | operator menekan “Parkir Mobil” kemudian menekan “Nomor” ruang parkir mobilnya ditempatkan dan me… | Parkir Mobil, slot selection, OK command |
| [E11] | STM §1 摘录 C \| paper.pdf p.6 Table 1 \| paper_content.txt 行 238-244 | Tombol nomor ruang parkir 1 sampai ruang parkir 8 untuk parkir mobil | slot 1-8 selection for parking |
| [E12] | STM §1 摘录 B \| paper.pdf p.4 §3.1 \| paper_content.txt 行 158-160 | Ketika sensor infrared 2 mendeteksi ruang parkir yang lewat maka motor DC penggerak rotary parkir… | infrared sensor 2 detects passing parking space and stops rotary motor |
| [E13] | STM §1 摘录 B \| paper.pdf p.4 §3.1 \| paper_content.txt 行 163-166 | operator menekan “Ambil Mobil” kemudian menekan “Nomor” ruang parkir mobil ditempatkan dan meneka… | Ambil Mobil, stored slot selection, OK command |
| [E14] | STM §1 摘录 B \| paper.pdf p.4 §3.1 \| paper_content.txt 行 166-167 | motor DC penggerak rotary parkir ON mengarahkan mobil kebawah bergerak CW/CCW | rotary motor moves the car downward CW/CCW |
| [E15] | STM §1 摘录 B \| paper.pdf p.4 §3.1 \| paper_content.txt 行 167-168 | ruang parkir yang ditekan pada HMI Android sudah berada dibawah maka led kuning ON dan motor DC p… | selected HMI slot reaches bottom, yellow LED on, rotary motor off |
| [E16] | STM §1 摘录 B \| paper.pdf p.4 §3.1 \| paper_content.txt 行 169-170 | jika sudah benar maka tombol “BENAR” ditekan maka palang pintu akan terbuka | BENAR opens the barrier |
| [E17] | STM §1 摘录 B \| paper.pdf p.4 §3.1 \| paper_content.txt 行 171-172 | tombol “SALAH” maka operator harus mengulangi “Ambil Mobil”. | SALAH repeats Ambil Mobil |
| [E18] | STM §1 摘录 C \| paper.pdf p.5 §3.1 \| paper_content.txt 行 202-204 | sensor proximity ON kemudian palang pintu tertutup kembali dan kondisi led kuning OFF | exit proximity closes barrier and turns yellow LED off |
| [E19] | paper.pdf p.5 §3.1 \| paper_content.txt 行 204-206 | untuk mengurangi terdapat pada proses kendaraan keluar dimana proses ini stelah mobil keluar mela… | parked-vehicle count is reduced after exit through proximity sensor |
| [E20] | paper.pdf p.5 §3.1 \| paper_content.txt 行 207-210 | pengguna membatalkan untuk melakukan parkir atau mengeluarkan mobil dan keadaan yang tidak terdug… | cancelled parking/retrieval, movement-counting errors, and disasters as emerg… |
| [E21] | STM §1 摘录 C \| paper.pdf p.7 Table 1 \| paper_content.txt 行 274-277 | tombol “DARURAT ON” dan untuk mematikan sistem darurat adalah tombol “DARURAT OFF” | DARURAT ON/OFF controls |
| [E22] | STM §1 摘录 C \| paper.pdf p.7 Table 1 \| paper_content.txt 行 278-280 | Tombol dan indikator untuk menurunkan ruang parkir CW/CCW | emergency CW/CCW lowering controls |
| [E23] | STM §1 摘录 C \| paper.pdf p.7 Table 1 \| paper_content.txt 行 281 | Tombol untuk Palang Buka dan Palang Tutup | emergency gate open/close controls |
| [E24] | STM §1 摘录 C \| paper.pdf p.7 Table 1 \| paper_content.txt 行 286-289 | Tombol Reset Jumlah untuk mereset perhitungan jumlah mobil yang berada pada ruang parkir dan tomb… | Reset Jumlah and Reset Counter controls |

**Intentional omissions**: 没有加入 Bluetooth 0-10 米通信距离或 11 米失败，因为它属于通信测试结果，不是该 PATH2 case 的核心控制流程守卫。也没有硬编全局任意状态强制跳转、超时、连续数值阈值、传感器型号或额外恢复路径。

</details>


##### 4. `[090]` ⚙️ Joey Pipe-Network Exploration Supervisor (EFSM-interlock)

- **领域**: ⚙️
- **论文**: paper #350 [`autonomous-control-miniaturized-mobile-robots-unknown-pipe-networks`](../../../sources/autonomous-control-miniaturized-mobile-robots-unknown-pipe-networks/STM.md)
- **是什么**: 这是 Joey 微型管网巡检机器人的高层探索监督器，使用三路 ToF 距离传感器、IMU 和轮腿编码器识别局部管网形态，并驱动左右轮腿电机完成直行、转弯、避障、死路掉头和回到入口。典型流程是在未知管网中按最右优先规则遍历岔路，遇 dead-end 180° 掉头，并持续监控翻倒和碰撞风险。
- **scale**: states=14 / events=12 / vars=12 / trans=40
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文把机器人状态分成 turning right、turning left、going straight 三组，并区分 speed/position 两种闭环控制模式，但 Figure 3 本质上仍是扁平状态图而非层次化 composite state。
- **C2 数值守卫**: 🟢 — 状态估计含多个数值 guard，例如居中判断用 Rleft 与 Rright 的差比阈值，右分支判断用 Rr > Rr_expected + sigma 且 Rr/Rr_expected > epsilon。
- **C3 forced fault**: 🟢 — 原文写到 during all operations 持续监控 range、speed、acceleration 以避免 crash/obstacle/wall，且有 Crash left/right 与 Flip-risk 风险恢复状态。
- **C4 硬件解耦**: 🟡 — 控制动作主要落到左右 wheel-leg micro-motors，协议还允许短暂激活 camera 和 LED light sources，但核心执行出口仍以左右电机为主。
- **对 PATH2 的价值**: 该样本对 PATH2 的价值主要在 C2 和 C3：数值传感 guard 很丰富，且有贯穿所有运行阶段的碰撞/翻倒安全监控，适合展示 parse + semantic + sim 反馈的收益。它是真实机器人控制对象，NL 描述和原文动作表都较清晰，和常见家电/楼控样本不趋同。
- **风险**: 原文称 13 个状态，但 Figure 3 按 0-13 展开为 14 个叶状态；此外没有真正层次嵌套，C1 不能高估。

<details><summary><b>📝 扩充 NL（274 词 / 21 markers / 21 provenance entries）</b></summary>

**Expanded NL**:

> The Joey supervisor is a finite-state autonomous controller that recognizes 13 robot states from sensor readings, while avoiding SLAM, video, and acoustic control inputs [E1] [E2] [E3]. Each estimation cycle fuses histories from the three range sensors, IMU orientation values, wheel-leg rotation, and the previous state; when a new state appears the robot stops to re-assess, and it maneuvers only after state_confirm is larger than 1 [E4] [E5] [E6]. Its numeric guards include a straight-center test where the normalized difference between Rleft and Rright is at or below kc, and a Sided case where the front range is under Fs because the front is close to a wall or obstacle [E7] [E8]. Exploration follows two global directives: at junctions choose the furthest-right direction, and at a dead-end turn around toward the previous junction so the network is covered and the robot can return safely [E9] [E10] [E11]. States are grouped as turning-right, turning-left, or going-straight, while motor execution uses closed-loop speed control for straight pipes or a left branch and closed-loop position control for other fine maneuvers [E12] [E13] [E14]. The effectors are two micro-motors driving the left and right wheel-legs, with magnetic encoders on wheel-leg driveshafts used for odometry and motor control [E15] [E16]. Recovery actions include a 30° backward crash correction followed by re-evaluation, a 180° dead-end turn with re-centering, and slow forward or backward stepping from Flip risk according to pitch and roll [E17] [E18] [E19]. Across all high-level maneuvers and operations, the controller continuously monitors roll, pitch, acceleration, range, and speed values to avoid flipping, crashing, obstacles, and pipe walls; high-level maneuver monitoring is specified at 5 Hz [E20] [E21].

**Axis coverage**:

- **C1**: 原文仅支持状态分组和速度/位置两种闭环控制模式 [E12] [E13] [E14]，没有层次化 composite mode、子 phase 或进入 mode 的默认初始子状态；因此不把 expanded_nl 作为强 C1 钩子。
- **C2**: C2 钩子在 [E6] [E7] [E8]：state_confirm 大于 1、Rleft/Rright 归一化差比阈值 kc、front range 与 Fs 的阈值比较。
- **C3**: C3 钩子在 [E20] [E21]：all high-level maneuvers / all operations 的持续监控是横切 during/aspect 语义；原文不支持任意状态 forced fault transition。
- **C4**: C4 钩子在 [E15] [E16] [E20] [E21]：two micro-motors、left/right wheel-legs、magnetic encoders 与持续传感监控提供硬件/IO 解耦线索；C4 强度为中等，因为没有多个具名 actuator 编号。

**Provenance** (21 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.6 §3.1 \| paper_content.txt 行 306-313 | we propose a computationally cheap, autonomous control strategy based on a finite state machine | finite-state autonomous controller |
| [E2] | STM §1 摘录 A \| paper.pdf p.6 §3.1 \| paper_content.txt 行 308-313 | we defined 13 robot states. We assume that the robot can confirm its current state using its sens… | recognizes 13 robot states from sensor readings |
| [E3] | STM §1 摘录 B \| paper.pdf p.6 §3.1 \| paper_content.txt 行 353-356 | the control inputs do not involve any simultaneous localization and mapping (SLAM) or other video… | avoiding SLAM, video, and acoustic control inputs |
| [E4] | paper.pdf p.7 §3.2 \| paper_content.txt 行 384-386 | estimated by a fusion of historical data of distance values from three range sensors, orientation… | estimation cycle fuses range-sensor histories, IMU orientation, wheel-leg rot… |
| [E5] | paper.pdf p.7 §3.2 \| paper_content.txt 行 386-390 | If a new state (i.e., different to last state) is detected, the robot stops to re-assess its sens… | when a new state appears the robot stops to re-assess |
| [E6] | paper.pdf p.7 §3.2 \| paper_content.txt 行 391-394 | If a robot state is confirmed (i.e., state_confirm value is larger than 1), the robot carries out… | maneuver starts only after state_confirm is larger than 1 |
| [E7] | paper.pdf p.6 §3.1 Eq.1 \| paper_content.txt 行 315-323 | The definition of “close” is: Rleft − Rright / Rleft + Rright ≤ kc | straight-center numeric guard using normalized Rleft/Rright difference at or … |
| [E8] | paper.pdf p.6 §3.1 \| paper_content.txt 行 324-329 | Sided: This state is similar to straight sided except its front range value is under a defined li… | Sided guard where front range is under Fs because the front is close to a wal… |
| [E9] | STM §1 摘录 B \| paper.pdf p.6 §3.1 \| paper_content.txt 行 363-365 | Rule 1: At junctions, turn into the furthest right direction. | at junctions choose the furthest-right direction |
| [E10] | STM §1 摘录 B \| paper.pdf p.6 §3.1 \| paper_content.txt 行 365-366 | Rule 2: At dead-end, turn around to return to the previous junction. | at a dead-end turn around toward the previous junction |
| [E11] | STM §1 摘录 B \| paper.pdf p.6 §3.1 \| paper_content.txt 行 356-358 | The strategy is to exhaustively cover the given pipe network and return safely to the starting po… | network coverage and safe return |
| [E12] | paper.pdf p.6 §3.1 \| paper_content.txt 行 367-369 | robot states are divided into three groups which are the turning right group, turning left group,… | states are grouped as turning-right, turning-left, or going-straight |
| [E13] | STM §1 摘录 B \| paper.pdf p.6 §3.1 \| paper_content.txt 行 370-372 | In straight pipes or at a left branch, the robot uses closed-loop speed control | closed-loop speed control for straight pipes or a left branch |
| [E14] | STM §1 摘录 B \| paper.pdf p.6 §3.1 \| paper_content.txt 行 373-375 | Other robot states require fine robot maneuver; thus, the robot uses closed-loop position control | closed-loop position control for other fine maneuvers |
| [E15] | paper.pdf p.3 §2.1 \| paper_content.txt 行 162-164 | two micro-motors, each of which actuates all the wheel-legs on either the left or right side | two micro-motors driving the left and right wheel-legs |
| [E16] | paper.pdf p.3 §2.1 \| paper_content.txt 行 167-170 | a magnetic encoder (Pololu 4760) is mounted on the driveshaft of one wheel-leg on each side and u… | magnetic encoders on wheel-leg driveshafts used for odometry and motor control |
| [E17] | STM §1 摘录 C \| paper.pdf p.12 Table 1 \| paper_content.txt 行 596-598 | robot turns 30° backwards to previous turning direction, then re-evaluates its state and makes de… | 30° backward crash correction followed by re-evaluation |
| [E18] | STM §1 摘录 C \| paper.pdf p.12 Table 1 \| paper_content.txt 行 601-603 | robot turns around by 180° and adjusts its position to the center of pipe while maintaining its p… | 180° dead-end turn with re-centering |
| [E19] | STM §1 摘录 C \| paper.pdf p.12 Table 1 \| paper_content.txt 行 604-605 | robot steps slowly backwards or forwards depending on its pitch and roll value to escape the flip… | slow forward or backward stepping from Flip risk according to pitch and roll |
| [E20] | paper.pdf p.11 §3.3 \| paper_content.txt 行 563-566 | During all high-level maneuvers, the robot is continuously (5 Hz) monitoring its roll, pitch angl… | continuous high-level monitoring of roll, pitch, acceleration, and range at 5 Hz |
| [E21] | paper.pdf p.11 §3.3 \| paper_content.txt 行 570-572 | During all operations, the robot continuously monitors its range values, speed, and accelerations… | all-operation monitoring of range, speed, and acceleration to avoid crashing,… |

**Intentional omissions**: 没有写真正的层次化子 mode、init pseudo 或 forced emergency path，因为原文只给扁平状态分组与持续风险监控。也没有补充阈值具体数值、valve/relay 编号或 camera/LED 参与控制。

</details>


##### 5. `[181]` 🏢 Priority-Scanned Smart-Home Utility and Access Controller (EFSM-interlock)

- **领域**: 🏢
- **论文**: paper #602 [`enhanced-smart-home-control-monitoring-system`](../../../sources/enhanced-smart-home-control-monitoring-system/STM.md)
- **是什么**: 这是一个 AT89C51 智能家居监督控制器，用水位、温度、烟雾、运动/进出和 keypad 信号按优先级扫描不同子流程。典型流程是根据传感输入启动/停止水泵、空调、报警器、灯光、门禁与 GSM/LCD 通知。
- **scale**: states=10 / events=14 / vars=10 / trans=20
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文 Fig.4 给出 St0-St9 的 ASM chart，并在控制算法中写 Do forever 下 If (WLS) / Else if (TCS) / Else if (SKS) / Else if (MDS) / Else if (KPS)，有多分支过程切换但没有真正 composite/init/pseudo 层次语义。
- **C2 数值守卫**: 🟢 — 原文包含 If level is minimum/maximum、If temperature too high、Check if count is zero 后 Increment/Decrement count、allow “3” time check，以及 VTH = 0.13V 的 comparator threshold，数值 guard 和计数 effect 足够清楚。
- **C3 forced fault**: 🟠 — 原文只说明 AT commands 在 smoke detector 信号或 wrong keypad supplied three times 时激活，并有 Sound an alarm/Send message，没有写 any mode/from any state 的强制 ErrorHandler。
- **C4 硬件解耦**: 🟢 — 原文动作包括 Switch on/off pump、Switch on/off AC、Sound an alarm、Switch on/off light、Grant/Deny access、Send message 和 Display message/error (LCD)，物理执行器与硬件出口丰富。
- **对 PATH2 的价值**: 该样本对 PATH2 的价值主要在 C2 与 C4：它把多个传感阈值、计数器和重试次数 guard 绑定到真实家居执行器，适合测试 symbolic guard feedback 与 abstract hardware handler。NL 独立清晰，且比单一门禁/灯控样本更综合。
- **风险**: 结构本质上仍是扁平 priority-scanned ASM，C1 层次化风险和 C3 cross-cutting recovery 证据都有限。

<details><summary><b>📝 扩充 NL（274 词 / 15 markers / 15 provenance entries）</b></summary>

**Expanded NL**:

> The controller is an enhanced smart-home control and monitoring system built around an AT89C51 microcontroller [E1], and sensor outputs serve as inputs to the microcontroller that controls the monitored processes [E2]. It uses five input process variables—WLS for water level, TCS for temperature control, SKS for smoke, MDS for motion detection, and KPS for keypad input [E3], while the ASM/state-transition design records state, input, output, next-state, and output-function information [E4]. The control software initializes process variables and runs forever [E5]; within each pass, WLS is tested before TCS, then SKS, MDS, and KPS, so the first active signal selects the handled process [E6]. In the water branch, a minimum level switches the pump on, and reaching the maximum level displays “tank full” and switches the pump off [E7]. In the temperature branch, a too-high temperature switches on the AC, otherwise the AC is switched off [E8]. In the smoke branch, sensed smoke sounds an alarm and displays an LCD message, and the GSM AT-command path is activated by the smoke-detector hazard signal [E9][E10]. In the room-light branch, entrance handling tests room light intensity, switches on the light when the room is dark, and increments the count; exit handling checks whether the count is zero before decrementing it and switching off the light [E11][E12]. In the keypad branch, a correct code grants access, but an incorrect code after the allowed three checks denies access, sends a message, sounds an alarm, and displays an LCD error [E13]. The water-level input qualifier also exposes a numeric comparator guard: voltage above 0.13 V maps to zero output, while receiving 0.13 V turns the comparator output to one [E14][E15].

**Axis coverage**:

- **C1**: 原文无明确层次状态、sub-mode 或进入默认子状态，expanded_nl 只写扫描分支，未提供 C1 钩子。
- **C2**: C2 暴露在 keypad 的三次错误检查 [E13] 和水位比较器 0.13 V 阈值 [E14][E15]，均用自然语言阈值/次数表达。
- **C3**: C3 仅由 do-forever continuous scan / each pass 语义 [E5][E6] 支持；原文不支持 any-state emergency 或 forced fault path。
- **C4**: C4 暴露在 pump、AC、alarm、LCD、GSM、light/access 等执行器与 IO 行为 [E7][E8][E9][E10][E11][E12][E13]。

**Provenance** (15 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 23-24 | At the heart of the control is AT89C51 which is a low power, high performance cmos 8 -bit microco… | AT89C51 microcontroller as the control core |
| [E2] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 25-27 | The output from the sensors serves as input to the microcontroller which actually controls the en… | sensor outputs enter the controller and control monitored processes |
| [E3] | STM §1 摘录 B \| paper.pdf p.3 Design Specifications \| paper_content.txt 行 207-211 | WLS = Water Level Signal, TCS = Temperature Control Signal SKS = Smoke Signal, MDS = Motion Detec… | the five named input process variables |
| [E4] | STM §1 摘录 B \| paper.pdf p.3 The ASM Chart of the System \| paper_content.txt 行 215-221 | state, input, output, next state function and output function | ASM/state-transition design records state, input, output, next-state, and out… |
| [E5] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 514-515 | Begin (): Initialize Process variables Do forever | initialization and continuous scan loop |
| [E6] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 516-525 | If (WLS) then Process (Water); Else if (TCS) then Process (Temperature); Else if (SKS) then Proce… | ordered else-if scan over WLS, TCS, SKS, MDS, and KPS |
| [E7] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 528-535 | If level is minimum then Switch on pump Check for maximum level If level is maximum then Display … | water branch pump-on, tank-full display, and pump-off behavior |
| [E8] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 537-541 | If (temperature) too high then Switch on “AC” Else switch off “AC” | temperature branch AC switching behavior |
| [E9] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 543-547 | If (smoke sensed) then Sound an alarm Display message (LCD) | smoke branch alarm and LCD message |
| [E10] | STM §1 摘录 C \| paper.pdf p.5 GSM Modem \| paper_content.txt 行 586-588 | activated once the controller receives a signal from the hazard detector (smoke detector) | GSM AT-command activation by smoke-detector hazard signal |
| [E11] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 549-554 | Check room light intensity If room dark then Switch on light Increment count Else switch off light | entrance-side room-light intensity check, light switching, and count increment |
| [E12] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 555-559 | Else if exit then Check if count is “zero” If not zero then Decrement count Switch off light | exit-side count-zero check, decrement, and light-off behavior |
| [E13] | STM §1 摘录 C \| paper.pdf p.5 Next State Logic Design \| paper_content.txt 行 562-570 | If code correct then Grant access Else if allow “3” time check If code incorrect then Deny access… | keypad access grant and three-check wrong-code escalation |
| [E14] | paper.pdf p.5 Input Qualifier Threshold \| paper_content.txt 行 505-508 | any voltage above 0.13V will result in a negative value which is equal to zero. | voltage above 0.13 V maps to zero output |
| [E15] | paper.pdf p.5 Input Qualifier Threshold \| paper_content.txt 行 507-508 | once a voltage of o.13V is received, the comparator output will turn to one. | receiving 0.13 V turns the comparator output to one |

**Intentional omissions**: 没有补 valve 编号、具体门锁执行器、恢复到安全态或任意状态强制故障迁移，因为原文没有这些细节。也没有把 St0-St9 全部列成状态名，避免把 ASM 图机械转写成状态清单。

</details>


##### 6. `[008]` 🌡️ Twelve-State EMS for LNG-Ship Hybrid Power Dispatch (EFSM-interlock)

- **领域**: 🌡️
- **论文**: paper #157 [`state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`](../../../sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/STM.md)
- **是什么**: 该 case 控制 LNG 船混合供能 EMS，读取负载 PL、PV/WEC 输出 Ppv/Pw、三台机组容量和电池 SoC，并对 LNG、DG1、DG2、电池充放电与 spare power 发出功率调度。典型流程是 RES 优先，电池补缺，其后依次启用 LNG、DG1、DG2，极端过载落入非法 State 2_7。
- **scale**: states=12 / events=12 / vars=13 / trans=12
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文称 FSM changes from one state to another，并明确 We identified 12 finite states，存在 12 个运行模式切换，但未见 composite/init/pseudo 层次语义。
- **C2 数值守卫**: 🟢 — Table 3 给出 Ppv + Pw < PL、eng1_Pmax + eng3_Pmax > PL - Ppv - Pw、SoC < 0.5 等多变量复合数值 guard。
- **C3 forced fault**: 🟠 — 原文仅把 State 2_7 描述为 illegal and shall never occur 的极端过载状态，未给出 any mode/from any state 的强制 fault recovery 转移。
- **C4 硬件解耦**: 🟢 — 原文写 EMS controls PVs, WECs, LNG, DGs, Batteries 并 applies commands for cut-in and cut-out，Table 2 还列出 DG1/DG2/Gas Generator 与电池充放电功率请求。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：数值调度 guard 密集且真实工业控制对象清楚，硬件出口覆盖多类发电机与电池系统。NL 与 Table 1-3 对齐度高，适合检验 symbolic guard feedback 和 abstract hardware action grounding。
- **风险**: 结构本质是扁平优先级调度 EFSM，C1 不是 HSM 强样本，C3 也只有非法过载状态而非真正 cross-cutting fault handler。

<details><summary><b>📝 扩充 NL（261 词 / 15 markers / 15 provenance entries）</b></summary>

**Expanded NL**:

> The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads [E1]. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary [E2]. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power [E3]. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC [E4]. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95 [E5], or treats residual renewable power as spare once SoC is at least 0.95 [E6]. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first [E7], batteries when SoC is suitable [E8], LNG before diesel units [E9], and DG1/DG2 only as the last priority [E10]. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case [E11] and Pd1max/10 in later diesel-generator cases [E12]. When PL = 0, RES production is sent to battery charging [E13] or to spare power according to SoC thresholds [E14]. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice [E15].

**Axis coverage**:

- **C1**: 原文只给出平铺的 12 个有限状态和转移条件，没有层次 mode、sub-mode 或进入默认子状态，expanded_nl 未提供 C1 钩子。
- **C2**: C2 钩子在 [E3][E4][E5][E6][E11][E12][E13][E14]：PL、Ppv、Pw、SoC、eng3_Pmax 等数值变量，以及 0.95、PL = 0、Pgmax/5、Pd1max/10 等阈值或算术条件。
- **C3**: 原文无 any state、each cycle、global emergency 或 forced transition 等横切语义，未提供 C3 钩子。
- **C4**: C4 钩子在 [E1][E3][E7][E9][E10][E13][E14][E15]：PVs/WECs/DGs/LNG/batteries、cut-in/cut-out、battery charge/discharge、thermal unit activation 等物理执行动作。

**Provenance** (15 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 B \| paper.pdf p.8 §3.1 \| paper_content.txt 行 425-437 | PVs, WECs, LNG, DGs, Batteries, vs. time, applying commands for cut-in and cut-out | EMS 管理的电源模块以及 cut-in/cut-out 控制命令 |
| [E2] | paper.pdf p.5 §2 \| paper_content.txt 行 256-264 | switches dynamically and achieves a power balance vs. time | EMS 动态切换状态并维持功率平衡 |
| [E3] | STM §1 摘录 B \| paper.pdf p.8 Tables 1-2 \| paper_content.txt 行 438-456 | The EMS receives the input variables (Table 1), connects, or disconnects the generating units, an… | 输入变量、输出变量、发电单元连接/断开与请求功率 |
| [E4] | STM §1 摘录 B/C \| paper.pdf p.12 §3.3 \| paper_content.txt 行 667-675 | Transition between states happens according to defined logical conditions | 十二状态 FSM 使用逻辑条件选择状态转移 |
| [E5] | STM §1 摘录 C \| paper.pdf p.10 Table 3 \| paper_content.txt 行 533-538 | all ship power demands are covered from RES. Residual power from RES is directed for batteries ch… | Ppv + Pw 覆盖 PL 时由 RES 供电，并在 SoC < 0.95 时充电 |
| [E6] | STM §1 摘录 C \| paper.pdf p.10 Table 3 \| paper_content.txt 行 539-544 | Residual power from RES is considered to be spare (if batteries SoC ≥ 0.95). | SoC ≥ 0.95 时剩余 RES 作为 spare power |
| [E7] | paper.pdf p.12 §3.3 \| paper_content.txt 行 650-651 | RES units (PVs and WECs), as a first priority | 调度优先级中 RES 优先 |
| [E8] | paper.pdf p.12 §3.3 \| paper_content.txt 行 652-653 | remaining power demands towards batteries (if batteries preserve a suitable State of Charge SoC | SoC 合适时由电池承担剩余功率需求 |
| [E9] | paper.pdf p.12 §3.3 \| paper_content.txt 行 654-657 | primarily to the LNG | 热机调度中 LNG 先于 DG1/DG2 |
| [E10] | paper.pdf p.12 §3.3 \| paper_content.txt 行 658-660 | activation of DG1 and DG2 by the EMS is the last priority | DG1/DG2 是最后优先级 |
| [E11] | STM §1 摘录 C \| paper.pdf p.10 Table 3 \| paper_content.txt 行 552-561 | Pgmax /5 is requested | 低 SoC 的 LNG 分支请求 Pgmax/5 额外充电功率 |
| [E12] | STM §1 摘录 C \| paper.pdf p.11 Table 3 \| paper_content.txt 行 577-610 | Pd1max /10 is requested | 低 SoC 的柴油发电机相关分支请求 Pd1max/10 额外充电功率 |
| [E13] | STM §1 摘录 C \| paper.pdf p.11 Table 3 \| paper_content.txt 行 624-634 | Battery charges using Ppv + Pw | PL = 0 时 RES 功率用于电池充电 |
| [E14] | STM §1 摘录 C \| paper.pdf p.11 Table 3 \| paper_content.txt 行 635-639 | All residual power directs to Ps | PL = 0 且 SoC 足够高时剩余功率进入 spare power |
| [E15] | STM §1 摘录 C \| paper.pdf p.11 Table 3 \| paper_content.txt 行 611-623 | This state is illegal and shall never be occurred in practice. Lack of power is covered from batt… | 非法过载完成状态、热机资源不足与电池放电补缺 |

**Intentional omissions**: 未加入层次 mode、默认子状态、forced fault/emergency recovery、阀门编号或传感器型号，因为原文没有提供这些信息。也未逐个列出全部 12 个 state name 或完整 I/O 表，避免把 NL 输入退化为照抄表格。

</details>


#### FSM-basic （3 条）

##### 1. `[194]` 🌡️ Five-mode microgrid EMS switch-breaker supervisor (FSM-basic)

- **领域**: 🌡️
- **论文**: paper #648 [`optimization-control-energy-management-system-microgrids`](../../../sources/optimization-control-energy-management-system-microgrids/STM.md)
- **是什么**: 这是一个并网微电网 EMS 的模式切换监督器，用 EMS breaker、utility-grid transfer switch、grid power indicator 以及逆变器控制在 Grid-connected、Grid-only、Islanding、Synchronization、Outage 之间切换。典型流程是在电网故障时断开并网开关进入孤岛，电网恢复后先同步幅值、频率和相位，再重连。
- **scale**: states=18 / events=9 / vars=6 / trans=30
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文明确说系统分为 five main operating modes，且图中 red circles represent the modes、each blue box represents a state，但没有给出 init/pseudo 或真正层次嵌套语义。
- **C2 数值守卫**: 🟢 — Synchronization mode 要求切回并网前 EMS ensure that the magnitude, frequency and phase of the microgrid and grid are the same，前文还说明 error is smaller than a threshold value 后才 ready to switch。
- **C3 forced fault**: 🟡 — 原文写 battery or EMS inverter malfunction 时 controller opens the breaker，transfer switch 也会在 grid power outage and voltage instability 时 trip from C to F，属于多处 fault 切换但不是明确 any-state ErrorHandler。
- **C4 硬件解耦**: 🟢 — 物理执行器包括 EMS breaker、utility grid transfer switch、built-in relay、低层 EMS inverter 充放电控制，以及 transfer switch reclose 操作。
- **对 PATH2 的价值**: 该样本对 PATH2 有价值主要在 C2 和 C4：同步重连含清晰数值 guard，模式切换直接驱动物理开关和逆变器动作。它也是典型工业能源控制对象，NL 与图示状态编码都比较清楚。
- **风险**: 主要风险是箭头级迁移大量依赖图 5.12 视觉解析，文本没有逐条列出所有 transition，且 C1/C3 不具备强层次化或 any-state fault handler。

<details><summary><b>📝 扩充 NL（274 词 / 15 markers / 15 provenance entries）</b></summary>

**Expanded NL**:

> The EMS controller for a grid-connected microgrid classifies operation into five main modes and implements them as a finite state machine [E1] [E2]. In normal grid-connected operation, the utility grid determines bus voltage, the solar grid-tie inverter and battery pack act as current-source inverters, and the high-level EMS commands battery charge or discharge power [E3] [E4]. If the battery or EMS inverter malfunctions or is under service, the controller opens the breaker connecting the EMS to the microgrid [E5]. When the utility grid is down or voltage-unstable, the EMS detects the incident, opens the grid transfer switch, isolates the microgrid, and runs the EMS inverter as a voltage-source inverter to govern bus voltage, maintain voltage and frequency, and balance generation with consumption [E6] [E7]. Before reconnection from islanded operation, the EMS checks that microgrid and grid magnitude, frequency, and phase are the same [E8]. If both the utility grid and EMS battery packs are out of power, the EMS control unit stays active on reserved power and monitors for return of either source so it can switch to the correct mode [E9]. The FSM variables are the utility-grid transfer switch, EMS breaker, and grid-power indicator; both switches use Closed, Fault opening, and Manual opening, while the grid indicator separates stable power from off-or-unstable power [E10] [E11] [E12]. The transfer-switch relay senses grid current and voltage, trips from Closed to Fault opening on outage or instability, and can reclose from Fault opening to Closed after fault clearance, but not from Manual opening to Closed [E13] [E14]. Three-letter encoded microgrid states record EMS-breaker, transfer-switch, and grid-power-indicator values, and mode circles group states with similar meaning [E15].

**Axis coverage**:

- **C1**: expanded_nl 在 [E15] 暴露了 mode circles group encoded states 的弱层次/分组边界；原文没有进入 mode 的默认子状态，因此未写 init-substate 语义。
- **C2**: 原文不支持数值阈值/区间 C2 钩子；expanded_nl 只保留 C/F/M 与 Y/N 等离散变量和条件 [E10] [E11] [E12] [E13] [E14]。
- **C3**: 原文没有 each cycle、any state、forced fault 或全局 emergency 语义，未提供 C3 钩子；outage 与 relay trip 均按局部条件写 [E9] [E13] [E14]。
- **C4**: C4 由 breaker、transfer switch、relay、EMS inverter 等物理 effector/sensor 动作暴露，集中在 [E4] [E5] [E6] [E7] [E13] [E14]。

**Provenance** (15 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A; paper.pdf PDF p.107/thesis p.90 §5.5.1; paper_content.txt 行 2122-2124 | the operation of a grid-connected microgrid with EMS is classified into five main operating modes | classifies operation into five main modes |
| [E2] | STM §1 摘录 C; paper.pdf PDF p.109/thesis p.92 §5.5.1; paper_content.txt 行 2171-2173 | a finite state machine controller is designed | implements them as a finite state machine |
| [E3] | paper.pdf PDF p.107/thesis p.90 §5.5.1; paper_content.txt 行 2125-2129 | microgrid bus voltage is determined by the utility grid. The solar grid-tie inverter is a current… | utility grid determines bus voltage; solar inverter acts as CSI |
| [E4] | paper.pdf PDF pp.107-108/thesis pp.90-91 §5.5.1; paper_content.txt 行 2129-2144 | The battery pack is also controlled as CSI. The high-level controller of EMS would command the lo… | battery pack acts as CSI; high-level EMS commands charge or discharge power |
| [E5] | STM §1 摘录 A; paper.pdf PDF p.108/thesis p.91 §5.5.1; paper_content.txt 行 2145-2148 | In case the battery or EMS inverter has a malfunction or is under service, the controller would o… | battery/inverter malfunction or service causes EMS breaker opening |
| [E6] | STM §1 摘录 A; paper.pdf PDF pp.108-109/thesis pp.91-92 §5.5.1; paper_content.txt 行 2149-2156 | When the utility grid is down or suffering voltage instability, EMS could detect the incident and… | grid down or unstable triggers EMS detection and transfer-switch opening |
| [E7] | STM §1 摘录 A; paper.pdf PDF p.109/thesis p.92 §5.5.1; paper_content.txt 行 2155-2160 | microgrid bus voltage is governed by the EMS inverter ... maintain the microgrid voltage and freq… | isolated microgrid uses EMS inverter as VSI to govern voltage, frequency, and… |
| [E8] | STM §1 摘录 B; paper.pdf PDF p.109/thesis p.92 §5.5.1; paper_content.txt 行 2161-2165 | Before switching to grid connected mode, EMS would ensure that the magnitude, frequency and phase… | synchronization guard before reconnection |
| [E9] | STM §1 摘录 B; paper.pdf PDF p.109/thesis p.92 §5.5.1; paper_content.txt 行 2166-2170 | both utility grid and EMS battery packs are out of power ... monitors the system with reserved po… | outage condition and reserved-power monitoring/recovery |
| [E10] | STM §1 摘录 C; paper.pdf PDF p.109/thesis p.92 §5.5.1; paper_content.txt 行 2171-2173 | The state variables are the state of utility grid transfer switch, EMS breaker and grid power ind… | FSM variables |
| [E11] | STM §1 摘录 C; paper.pdf PDF pp.109-110/thesis pp.92-93 §5.5.1; paper_content.txt 行 2174-2184 | Utility grid transfer switch has three states, Closed(C), Fault opening(F), and Manual opening(M)… | switch state values for transfer switch and EMS breaker |
| [E12] | STM §1 摘录 C; paper.pdf PDF p.110/thesis p.93 §5.5.1; paper_content.txt 行 2184-2185 | Grid power indicator has two values: Grid has power and stable(Y), grid is power off or unstable(N). | grid-power indicator values |
| [E13] | paper.pdf PDF p.109/thesis p.92 §5.5.1; paper_content.txt 行 2174-2177 | senses utility grid current and voltage ... the transfer switch would trip from C to F | relay sensing and trip from Closed to Fault opening |
| [E14] | paper.pdf PDF p.110/thesis p.93 §5.5.1; paper_content.txt 行 2182-2183 | EMS could direct the transfer switch to reclose from F to C when a fault is cleared, but not from… | reclose allowed from fault state but not manual state |
| [E15] | STM §1 摘录 D; paper.pdf PDF p.110/thesis p.93 §5.5.1; paper_content.txt 行 2186-2191 | The three letters represent the state of EMS breaker, grid transfer switch and grid power indicat… | three-letter state encoding and mode grouping |

**Intentional omissions**: 没有写同步误差阈值、继电器电压/电流阈值或具体恢复优先级，因为原文只给出 same、unstable、fault cleared 这类定性条件。没有写 emergency stop、任意状态强制跳转或默认初始子状态，因为原文不支持。

</details>


##### 2. `[018]` ✈️ Low-altitude mission-task FSM for target approach and threat avoidance (FSM-basic)

- **领域**: ✈️
- **论文**: paper #173 [`autonomous-control-framework-unmanned-helicopter-low-altitude-flight`](../../../sources/autonomous-control-framework-unmanned-helicopter-low-altitude-flight/STM.md)
- **是什么**: 该 case 控制无人直升机在山地低空任务中的高层飞行决策，利用机载相机/检测网络、Lidar/VFH 与可见性判断，在远程穿透、目标快速接近、严重威胁快速规避和小威胁迂回飞行之间切换。执行侧主要输出 yaw、altitude、longitude、lateral 等飞控通道命令。
- **scale**: states=6 / events=8 / vars=8 / trans=12
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文第19页把 long-range penetration、fast approach、fast avoidance、circuitous flight 写成不同 flight tasks 的 state transitions，但没有 composite state/init/pseudo 语义。
- **C2 数值守卫**: 🟢 — 原文第18-19页给出 threat degree E = Sbox * xi_class，并用 E 与 ET 的比较区分 serious threat 和 small threat。
- **C3 forced fault**: 🟡 — 原文第18页说明 serious threat 的 fast avoidance 优先级高于 fast approach，且不管 target 是否在视野内都执行规避，但不是显式 any-state ErrorHandler。
- **C4 硬件解耦**: 🟢 — 原文第19页说明控制通道解耦，并通过 yaw channel、altitude channel、longitude channel、lateral channel 输出飞行控制命令。
- **对 PATH2 的价值**: 该样本对 PATH2 有价值主要在 C2 和 C4：威胁等级阈值分支有清晰数值 grounding，飞控通道和 VFH/visual-servo 动作也能体现 abstract action 的硬件解耦收益。NL 独立且贴近真实无人直升机控制任务。
- **风险**: FSM 是高层任务切换图，层次化 dead-end 与 fault recovery 语义不强，且 path re-planning/visibility judgement 是否建模为状态存在一定口径噪声。

<details><summary><b>📝 扩充 NL（265 词 / 16 markers / 16 provenance entries）</b></summary>

**Expanded NL**:

> The controller is a mission-task finite state machine for unmanned helicopter operations in low-altitude flight, and it forms a continuous operation process without human interference [E1]. In the normal destination-approach flow, the helicopter is given a distant destination, flies at low altitude, and runs a detection network for targets and threat facilities [E2]. When a target is detected, it heads to the target through visual servo control and revises the target position [E3]; it also estimates distance and yaw direction using airborne equipment [E4] and places target points along that direction for VFH path replanning [E5]. If the target is lost, the controller keeps flying toward the defined target points and returns to visual servo control when the target is rediscovered [E6]. For threats, the controller evaluates threat degree E using a class coefficient and Sbox distance [E7], and treats E higher than threshold ET as a serious threat [E8]. A serious threat has priority over fast approach and triggers fast avoidance regardless of target visibility [E9]; if several threats are present, the helicopter heads toward the one with the highest threat degree [E10]. During serious-threat handling, VFH target points are reset to history-path points [E11] and lateral maneuvers restore invisibility behind terrain cover [E12]. If E is lower than ET, the controller treats it as a small threat and executes circuitous flight [E13], with VFH target points reset to the helicopter side before the destination approach resumes when the threat is lost [E14]. The paper describes target/threat detections, airborne-equipment direction estimates, Lidar obstacle readings, and control commands of yaw, altitude, and linear-velocity channels [E2][E4][E15][E16].

**Axis coverage**:

- **C1**: 原文呈现的是任务级平铺 FSM 和 Figure 19 状态转换，没有 sub-mode/phase/default child，因此 expanded_nl 未暴露 C1 钩子。
- **C2**: C2 由 [E7][E8][E13] 暴露：threat degree E、Sbox distance、class coefficient 与 threshold ET 的高/低比较。
- **C3**: C3 有限支持由 [E9][E10] 暴露：fast avoidance 对 fast approach 的优先级和多威胁最高威胁度选择；原文不支持一般化的任意状态 forced fault path。
- **C4**: C4 部分支持由 [E2][E4][E15][E16] 暴露：detection network、airborne equipment、Lidar sensor 与 yaw/altitude/linear-velocity control channels；原文没有具名 physical actuator/effector。

**Provenance** (16 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.18-p.19 §4.2 | overall framework for unmanned helicopter operations in low-altitude flight ... continuous operat… | mission-task FSM for low-altitude unmanned helicopter operations and continuo… |
| [E2] | paper.pdf p.18 §4.2 | a helicopter is given a distant destination and required to approach the destination at low altit… | distant destination, low-altitude approach, and target/threat detection network |
| [E3] | STM §1 摘录 B \| paper.pdf p.18 §4.2 | Once the target is detected, the helicopter immediately heads to the target through visual servo … | target detection triggers visual servo heading and target-position revision |
| [E4] | paper.pdf p.18 §4.2 | it is able to estimate the distance and yaw direction using airborne equipment. | distance/yaw estimates using airborne equipment |
| [E5] | paper.pdf p.18 §4.2 | Several target points are placed along the target direction for path replanning of the VFH method. | target points along target direction for VFH path replanning |
| [E6] | STM §1 摘录 B \| paper.pdf p.18 §4.2 | In case the target is lost, the helicopter continues flying to the defined target points ... retu… | target-lost recovery through defined target points and visual-servo return on… |
| [E7] | paper.pdf p.18 §4.2 | ξclass is the coefficient for different classes of threats. Sbox implies the distance to the threat. | threat degree E uses class coefficient and Sbox distance |
| [E8] | STM §1 摘录 C \| paper.pdf p.18 §4.2 | a threat degree that higher than ET is considered as a serious threat. | E higher than threshold ET is serious |
| [E9] | STM §1 摘录 C \| paper.pdf p.18 §4.2 | higher priority to fast avoidance than to fast approach ... regardless of whether a target is det… | serious-threat fast avoidance overrides fast approach and target visibility |
| [E10] | paper.pdf p.18 §4.2 | If multiple threats are detected during the flight, the helicopter heads toward the threat with h… | highest-threat selection when multiple threats are detected |
| [E11] | paper.pdf p.18 §4.2 | The target points of the VFH method are reset as the points of the history path. | serious-threat handling resets VFH target points to history-path points |
| [E12] | paper.pdf p.18 §4.2 | the helicopter executes lateral maneuvers so as to quickly restore invisibility behind terrain co… | lateral maneuvers restore invisibility behind terrain cover |
| [E13] | STM §1 摘录 D \| paper.pdf p.19 §4.2 | If the threat degree is lower than ET, the detected threat is considered a small threat, and the … | E lower than ET leads to small-threat circuitous flight |
| [E14] | paper.pdf p.19 §4.2 | The target points of the VFH method are reset to the sides of the helicopter. When the threat is … | small-threat circuitous flight side target points and resumption after threat… |
| [E15] | paper.pdf p.17 visibility judgement paragraph | if the threat is lost from view and the Lidar sensor can detect obstacles ahead | Lidar obstacle readings used in visibility judgement |
| [E16] | paper.pdf p.19 §4.2 | The VFH method provides the control commands of the yaw channel and altitude channel ... u, v, an… | yaw, altitude, and linear-velocity control-command channels |

**Intentional omissions**: 没有加入层次化 mode、默认子状态或历史伪状态，因为原文只给任务级 FSM。没有加入具名 motor/valve、具体 ET 数值、emergency stop 或 forced fault recovery，因为 paper.pdf 与 STM §1 摘录均不支持这些细节。

</details>


##### 3. `[097]` ✈️ Search-follow-catch mission controller (FSM-basic)

- **领域**: ✈️
- **论文**: paper #372 [`autonomous-aerial-robot-high-speed-search-intercept`](../../../sources/autonomous-aerial-robot-high-speed-search-intercept/STM.md)
- **是什么**: 该 case 控制高速搜索与拦截任务中的 UAV 高层 mission controller，利用长距/短距视觉检测、球检测和夹爪内激光传感器触发状态切换。典型流程是起飞后搜索目标、长距跟随、短距接近、对准夹爪抓球，成功后降落。
- **scale**: states=6 / events=6 / vars=5 / trans=10
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文列出 START_STATE、SEARCH、FOLLOW_LONG_RANGE、FOLLOW_SHORT_RANGE、CATCH_BALL、LAND，并在 Figure 17 展示多状态切换，但也说明该 FSM 可用 small number of states and events 表示，未见层次化 composite state。
- **C2 数值守卫**: 🟢 — Table 1 明确给出 LONG_RANGE_UAV_DETECTED 为 5 连续帧中 3 次检测、SHORT_RANGE_UAV_DETECTED 为 4 连续帧中 2 次检测、DETECTION_LOST 为 5 连续帧无新检测。
- **C3 forced fault**: 🟡 — Table 1 将 DETECTION_LOST 定义为 No new detections in 5 consecutive frames，Figure 17 中 FOLLOW_LONG_RANGE、FOLLOW_SHORT_RANGE、CATCH_BALL 等状态都有回到 SEARCH 的 detection-lost 恢复迁移，但不是任意状态全局 fault。
- **C4 硬件解耦**: 🟢 — 原文说状态可 establish UAV speed 和 navigation goals，camera gimbal controller 按 LONG_RANGE_MODE/SHORT_RANGE_MODE 改变行为，且 gripper 由 Arduino Nano 控制 servomotor 开闭。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 与 C4：有清晰的连续帧计数型 guard，且状态动作直接连接 UAV 运动、云台和夹爪伺服等硬件出口。NL 描述和原文状态/事件表都较完整，适合作为真实机器人 T0 mission-control case。
- **风险**: Figure 17 只说明是 part of the transitions，完整迁移可能未全列，且结构本身是扁平 FSM，C1 层次化 dead-end grounding 不强。

<details><summary><b>📝 扩充 NL（279 词 / 18 markers / 18 provenance entries）</b></summary>

**Expanded NL**:

> The mission controller is a finite-state controller for a UAV mission that searches, follows, and grasps a moving object; initially the UAV is landed with GPS, RTK, and cameras initialized, and START_MISSION is the operator order to start [E1] [E2] [E3] [E4]. In SEARCH, the UAV flies a predefined semiellipse near the long-axis border and middle of that axis, at low altitude and very low speed and acceleration, so both UAV detectors stay active and can obtain sharp images against a uniform sky background [E5] [E6] [E7]. The controller changes from search to long-range following when the Long-Range Detector reaches three detections in five consecutive frames, and each new long-range detection commands fast UAV motion toward a point 5 m toward the detection in the XY plane [E8] [E9]. It then changes to short-range following when the Short-Range Detector reaches two detections in four consecutive frames, keeps about 4 m from the target, and disables the Long-Range UAV Detector so the short-range detector gets the computation power [E10] [E11]. When the ball is detected, the controller enters CATCH_BALL, commands motion toward the ball detection, aligns the ball with the gripper, and continues the planned trajectory after the ball leaves the camera field of view [E12] [E13] [E14]. If no new detections arrive for five consecutive frames, the FSM has a DETECTION_LOST transition event [E15]. A successful catch is declared only when the laser sensor inside the gripper detects the ball, after which the UAV lands at a given position and ends the mission [E16] [E17]. The gripper hardware includes a servomotor controlled through an Arduino Nano for closing and opening when high-level mission components require the catching maneuver [E18].

**Axis coverage**:

- **C1**: 原文将该控制器明确实现为普通 FSM，未给层次状态、子 mode 或进入复合 mode 的默认子状态；expanded_nl 未暴露 C1 钩子。
- **C2**: C2 钩子在 [E8] [E9] [E10] [E11] [E15]：3/5、2/4、5 m、4 m 和 5 consecutive frames 都是可转成数值守卫的原文变量/阈值。
- **C3**: 原文只支持 DETECTION_LOST 作为转移事件 [E15]，不支持 any-state/global forced transition 或 each-cycle aspect；expanded_nl 未编造全局 C3 语义。
- **C4**: C4 钩子在 [E3] [E7] [E11] [E13] [E16] [E18]：GPS/RTK/cameras、UAV detectors、trajectory/gripper、laser sensor 和 servo/Arduino 都是原文硬件或 I/O 依据。

**Provenance** (18 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | paper.pdf p.1 Abstract \| paper_content.txt 行 36-38 | autonomously search, follow, and grasp a moving object at 6 m/s | UAV mission searches, follows, and grasps a moving object |
| [E2] | STM §1 摘录 A \| paper.pdf p.19 §5.5 \| paper_content.txt 行 790-795 | a solution based on a FSM for the architecture designed for Challenge 1 has been implemented | finite-state controller |
| [E3] | paper.pdf p.19 §5.5 \| paper_content.txt 行 804-805 | START_STATE: The UAV is landed. In this state, the GPS, RTK, and cameras are initiated. | initially the UAV is landed with GPS, RTK, and cameras initialized |
| [E4] | STM §1 摘录 C \| paper.pdf p.20 Table 1 \| paper_content.txt 行 836-839 | START_MISSION The human operator gives the order to the UAV to start the mission | START_MISSION is the operator order to start |
| [E5] | paper.pdf p.19 §5.5 \| paper_content.txt 行 806-810 | The trajectory is in the form of a semiellipse, very close to the long axis border and in the mid… | SEARCH flies a predefined semiellipse near the long-axis border and middle |
| [E6] | paper.pdf p.19 §5.5 \| paper_content.txt 行 810-812 | the camera is pointing to the sky. This maximizes the accuracy of the detectors because the backg… | low altitude and uniform sky background for detector accuracy |
| [E7] | paper.pdf p.19 §5.5 \| paper_content.txt 行 812-814 | the maneuvers are at very low speed and acceleration order to get sharp images. In this state, bo… | very low speed and acceleration, sharp images, both detectors active |
| [E8] | STM §1 摘录 C \| paper.pdf p.20 Table 1 \| paper_content.txt 行 839-840 | There are 3 detections on 5 consecutive frames from the Long-Range Detector. | long-range threshold is three detections in five consecutive frames |
| [E9] | STM §1 摘录 B \| paper.pdf p.19 §5.5 \| paper_content.txt 行 815-817 | the UAV moves at a high speed to a point 5 m towards the detection in the XY plane | fast UAV motion toward a point 5 m toward the detection in the XY plane |
| [E10] | STM §1 摘录 C \| paper.pdf p.20 Table 1 \| paper_content.txt 行 841-842 | There are 2 detections on 4 consecutive frames from the Short-Range Detector. | short-range threshold is two detections in four consecutive frames |
| [E11] | STM §1 摘录 B \| paper.pdf p.19 §5.5 \| paper_content.txt 行 818-820 | maintaining 4 m from the target. In this state, the Long-Range UAV Detector is disabled so the Sh… | keeps about 4 m from target and disables long-range detector |
| [E12] | STM §1 摘录 C \| paper.pdf p.20 Table 1 \| paper_content.txt 行 843 | BALL_DETECTED The ball is detected. | ball detection triggers the catch phase |
| [E13] | STM §1 摘录 B \| paper.pdf p.19 §5.5 \| paper_content.txt 行 821-822 | CATCH_BALL: The UAV moves towards the ball detection trying to align the ball position with the g… | CATCH_BALL motion aligns the ball with the gripper |
| [E14] | STM §1 摘录 B \| paper.pdf p.19 §5.5 \| paper_content.txt 行 821-824 | Once the ball goes out of the camera field of view, it continues following the planned trajectory. | continues planned trajectory after ball leaves camera field of view |
| [E15] | STM §1 摘录 C \| paper.pdf p.20 Table 1 \| paper_content.txt 行 844 | DETECTION_LOST No new detections in 5 consecutive frames | DETECTION_LOST event after five frames without new detections |
| [E16] | STM §1 摘录 C \| paper.pdf p.20 Table 1 \| paper_content.txt 行 845 | SUCCESSFUL_CATCH Ball is detected by the laser sensor inside gripper. | successful catch requires laser sensor detection inside gripper |
| [E17] | STM §1 摘录 B \| paper.pdf p.19 §5.5 \| paper_content.txt 行 826 | LAND: The UAV lands in a given position and the mission ends. | UAV lands at a given position and ends the mission |
| [E18] | paper.pdf p.8 §3.2 \| paper_content.txt 行 350-352 | The stated servo is controlled trough an Arduino Nano, in charge of closing and opening the gripp… | gripper servomotor controlled through Arduino Nano for mission-required closi… |

**Intentional omissions**: 没有写层次化子状态、emergency stop、任意状态 forced fault、CATCH_BALL 进入时立即闭合 gripper 等，因为原文没有给这些控制语义。也没有编造 valve 编号、额外传感器型号或不受 Z3 支持的数学函数。

</details>



## 🛡️ 备选池（15）

### 速查表

| 序 | id | 领域 | 桶 | C1 | C2 | C3 | C4 | verdict | scale (S/E/V/T) | 案例 | 系统简述 | 我们关注的特性 |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 159 | 🌡️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 61/42/45/105 | [Water-filter test-bench main-state and valve su…](../../../sources/control-system-design-of-water-filter-test-bench/STM.md) | 该 case 建模水滤测试台的主模式监督器，以及阀门、泵、节流阀等执行器在 ΔP 测量、多通道测量、手动控制和 stop 路径下的允许操作。典型流程是从 Normal 进入 Lobby1/Lobby2/Lobby3，按传感器限值、泵阀状态和旁通状态守卫启动测试，异常时进入 automatic stop 或 safety stop 并限制泵使用。 | 该样本对 PATH2 很有价值：C1 的模式/层次结构、C3 的全局 stop 路径、C4 的大量物理执行器都能给 parse+semantic+sim feedback 提供 grounding。它是典型工业测试台控制对象，NL 与原文锚点清晰，和纯软件协议类样本差异明显。 |
| 2 | 010 | ✈️ | HSM | 🟢 | 🟢 | 🟢 | 🟡 | 💎 | 27/17/12/48 | [Master-and-Autopilot Mission Cycle for Autonomo…](../../../sources/long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition/STM.md) | 该 case 控制长时自主旋翼 UAS 在充电站、起飞、任务飞行、返航、精确着陆和紧急降落之间的任务循环；它使用电池/电机健康、GPS/状态估计、下视相机 AprilTag、触地高度与速度阈值等信息，驱动飞控、电机、返航和着陆动作。 | 该样本对 PATH2 很有价值：它同时有清晰 HSM 层次、跨 autopilot abort/紧急降落、复合数值 guard 和真实硬件动作，能覆盖 C1/C2/C3 的 grounding 需求。NL 描述独立、工业控制意味强，不只是 toy FSM。 |
| 3 | 015 | ⚙️ | HSM | 🟢 | 🟢 | 🟢 | 🟡 | 💎 | 7/8/6/14 | [Greenhouse row-inspection navigation supervisor](../../../sources/autonomous-navigation-framework-holonomic-mobile-robots-agriculture/STM.md) | 该 case 控制温室全向移动机器人在 headland 与作物行之间的导航巡检流程，利用 stereo camera、LiDAR、语义分割和 TEB/SMACH 导航栈调度 waypoint 导航、轨道对齐、行内前进巡检与后退返回。典型流程是 WAIT_FOR_GOAL 接收行巡检任务后进入 PLAN_EXEC，再进入 VISUAL_SERVOING 中… | 该样本对 PATH2 很有价值：它同时具备层次化 block、复合数值对齐 guard 和跨全流程 failure recovery，能直接支撑 C1/C2/C3 的 in-loop grounding。NL 描述清晰、对象是真实农业机器人导航监督控制器，且与常见纯软件协议样本差异明显。 |
| 4 | 179 | 🏢 | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 18/14/15/36 | [Robot Elevator Request-Floor-Estimation Recover…](../../../sources/secure-automated-elevator-management-pressure-sensor-floor-estimation/STM.md) | 该 case 控制室内移动机器人乘梯过程：AEMS 通过 Wi-Fi/ADAM 继电器呼梯与选层，压力传感器估计楼层，超声传感器识别门状态。典型流程是呼梯、进轿厢、按任务状态选择目标楼层、等楼层匹配且门打开后出梯，失败时进入内外两类错误恢复。 | 该样本对 PATH2 有价值，主要强在 C2 数值守卫和 C4 硬件动作解耦，同时具备较清晰的层次化乘梯/恢复结构。它是典型真实机器人-楼宇电梯控制对象，NL 描述较完整，和纯软件协议类样本不趋同。 |
| 5 | 012 | ⚙️ | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 14/22/9/34 | [Multi-modal drive-fly mission FSM for TURVTOL](../../../sources/terrestrial-unmanned-roving-vertical-take-off-and-landing-turvtol/STM.md) | 该 case 控制 TURVTOL 多模态自主 rover/drone 的任务监督 FSM，利用 SLAM、path planner、VIO、wheel encoders 和电池/地形安全信号在地面行驶、起飞、飞行、悬停、找降落点、降落、牵引恢复和休眠充电之间切换。执行侧涉及 differential-drive wheel motors、coaxial… | 该样本对 PATH2 很有价值：C1 层次结构非常明确，C2 有电池阈值、搜索半径、VIO/encoder 对比等可符号化守卫，C4 也有清晰硬件动作出口。NL 与原文表格/图对应关系清楚，且多模态 rover-drone 不容易与普通工业 FSM 趋同。 |
| 6 | 172 | ✈️ | HSM | 🟢 | 🟡 | 🟢 | 🟡 | 💎 | 17/15/8/31 | [Building-interior firefighting mission supervisor](../../../sources/autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle/STM.md) | 这是一个室内消防 MAV 的高层任务监督 HSM，使用 GNSS、2D LIDAR、立体相机和热相机进行定位/感知，控制飞行电机、定位模式切换与水泵喷射。典型流程是起飞检查、室外绕楼找窗、穿窗进入、室内探索找火、灭火、原窗退出并返航降落。 | 该样本对 PATH2 很有价值：C1 的层次化子状态机调用、失败回退和 nested exit 语义清楚，C3 又有 any-state landing event，可直接检验生成-验证-反馈循环对 HSM 病态与 forced recovery 的 grounding。它也是实体机器人消防控制对象，NL 描述独立且流程完整。 |
| 7 | 143 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 9/12/12/16 | [Auto-Manual WWTP Supervisor with Conductivity-F…](../../../sources/boiler-wastewater-treatment-control-monitoring-plc-hmi/STM.md) | 该 case 是锅炉废水处理厂的 PLC/HMI 监督控制器，在自动/手动模式下协调 equalization、coagulation、flocculation、clarifier、final tank 等处理单元。它用 pH、电导率/TDS、液位等传感器驱动泵、搅拌器、电磁阀和电动阀，最终按电导率反馈决定排放或回流到 equalization unit。 | 该样本对 PATH2 主要价值在 C2 与 C4：既有明确数值阈值/回流 guard，又有大量真实 PLC 执行器输出，适合展示 symbolic guard feedback 与 abstract hardware handler。Auto/manual mode 也提供中等 C1 模式切换风险，且工业控制对象清晰独立。 |
| 8 | 167 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 8/11/9/13 | [Flow-and-Water-Quality Feedback Dosing Controller](../../../sources/automatic-dosing-system-based-on-reclaimed-water-treatment/STM.md) | 这是再生水处理设备中的 PLC 自动加药控制器，根据进水流量、在线出水水质、液位和加药流量反馈计算投加量，并驱动电动阀、计量泵、变频器、搅拌器等完成稀释、阀门切换、配药和闭环投加。 | 该样本对 PATH2 的主要价值在 C2 和 C4：它有清晰的多变量乘法/比值控制公式、PID 闭环调节和真实水处理硬件执行链，适合检验数值 guard 反馈与 abstract action 硬件解耦收益。NL 描述独立清楚，是典型工业过程控制对象。 |
| 9 | 151 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 7/8/9/13 | [Flow-Interlocked Liquid Transfer and Pause-Reco…](../../../sources/liquid-level-monitoring-flow-liquid-distribution-plc-scada/STM.md) | 这是一个 PLC/SCADA 液体转运监督控制器：操作员选择目标罐并输入设定转运量后，系统根据液位、管线流量、阀门反馈和泵状态控制吸入/分配/目标电磁阀与泵。典型流程是预检联锁通过后开阀启泵，异常时暂停并关阀停泵，故障排除后重新 Start，流量累计达到设定量后完成。 | 该样本对 PATH2 的主要价值在 C2 和 C4：有典型工业 PLC/SCADA 对象、清晰的数值累计/阈值联锁，以及多路阀泵硬件动作，适合验证 EFSM 数值守卫和 abstract action 解耦收益。NL 流程也较完整，能形成可生成、可仿真、可反馈的 T0 case。 |
| 10 | 215 | 🏭 | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 8/10/8/11 | [Automatic Feeding, Tool Selection, Alignment, a…](../../../sources/control-system-automatic-bamboo-splitting-equipment-plc/STM.md) | 该 case 控制自动破竹机的 PLC 送料、刀盘选刀、竹筒对中夹持与切割流程；系统用传感器测量竹筒接触点和夹持压力，驱动输送带、电机、刀盘和夹持机构完成从送料到切割的顺序加工。 | 该样本对 PATH2 的主要价值在 C2 和 C4：它同时包含几何拟合、直径比较、压力阈值等数值守卫，以及多类真实工业执行器。NL 流程清楚，控制对象独立，适合作为 pyfcstm 数值反馈和 abstract handler grounding 的 T0 样本。 |
| 11 | 052 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 7/7/4/10 | [Four-Scenario Micro-Grid EMS with SOC-Governed …](../../../sources/energy-management-strategy-hybrid-micro-grid-renewable-energy/STM.md) | 这是一个混合微电网 EMS，用发电功率 PG、负载 PL、电池 SOC 和 utility grid availability 判断 PV/风电、电池、utility grid、柴油机之间的供能切换。典型流程是发电充足时供负载并给电池充电，SOC 满后送电网，发电不足时电池放电，SOC 到 20% 后切到电网或柴油机供电。 | 该样本对 PATH2 的主要价值在 C2 和 C4：数值守卫密集，且直接驱动物理能源设备 ON/OFF，适合检验 semantic/sim feedback 对 EFSM interlock 的修正收益。NL 描述清晰，工业控制对象典型，能作为 T0 中较强的微电网能量管理样本。 |
| 12 | 026 | 🩺 | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 4/6/6/7 | [Preset gait-phase stimulation supervisor for hy…](../../../sources/modular-neuroprosthesis-hybrid-fes-robot-assistance/STM.md) | 该 case 是一个步态相位监督器，用髋/膝/踝电角度计和 WR 状态识别 support、pre-swing、swing-up、swing-down，并驱动不同肌群的 FES 刺激及膝部机器人辅助。典型流程是按 HC/HO/TO/K1 等步态事件循环切换相位，在 standard mode 或 cross mode 下把刺激映射到 GM、Q、TFL、H、… | 该样本对 PATH2 的主要价值在 C2 和 C4：它有真实连续角度信号、adaptive threshold 相位判定和多肌群/机器人硬件输出，能体现 semantic/sim feedback 与 abstract hardware handler 的收益。C1 也有 standard/cross mode 变体，虽非强层次结构，但足以制造一定模式混淆… |
| 13 | 124 | ⚙️ | FSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 22/18/8/31 | [Excavation-Transport-Deposit Robot FSM](../../../sources/robot-excavation-geometrically-cohesive-granular-media/STM.md) | 该 case 控制一个几何黏聚颗粒物挖掘机器人在蓝色挖掘区与红色沉积区之间循环作业，依靠 RGB 光源检测、ArduCAM 视觉、antenna 触觉和 jaws 状态切换行为。典型流程是挖掘并夹取 pellet，转向并运输到沉积区，搜索已有料堆或墙面后卸料，再转回挖掘区。 | 该样本对 PATH2 的主要价值在 C2 和 C4：真实机器人 FSM 同时含视觉/触觉/颜色/计数阈值 guard 与多个物理执行器动作，能很好体现 symbolic guard feedback 和 abstract action 硬件解耦收益。C1 也有多阶段切换，适合测试 agent 是否能把图中阶段边界和叶子状态关系建对。 |
| 14 | 227 | 🏭 | FSM | 🟡 | 🟡 | 🟢 | 🟢 | 💎 | 9/9/8/22 | [Pause-resume segmented-panel assembly process c…](../../../sources/sensor-guided-assembly-segmented-structures-industrial-robots/STM.md) | 这是一个工业机器人分段复合板装配流程监督器，用相机定位与对准、F/T 传感器进行接触力控制，并驱动 ABB 机器人和真空吸盘夹爪完成拾取、运输、放置。典型流程是 Move Above Pickup Nest -> Approach Panel -> Pick Up -> Transport -> Place Panel -> Finish，中间可由操作员暂… | 该样本对 PATH2 的价值主要在 C3 与 C4：它是清晰、真实的工业装配流程控制器，暂停/恢复/异常接管语义跨越多个工艺阶段，同时绑定机器人、夹爪、视觉与力控硬件。NL 描述独立且图 4 给出明确状态结构，适合作为 T0 中制造控制类强样本。 |
| 15 | 061 | 🚗 | FSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 5/8/14/11 | [Five-Mode Benefit-Evaluated Driving Supervisor](../../../sources/autonomous-driving-benefit-evaluation-fsm/STM.md) | 这是自动驾驶车辆的高层驾驶行为决策 supervisor，基于交通信息、环境感知和车辆状态在自由行驶、跟车、换道、紧急制动、故障停车之间切换。原文实车平台使用 DGPS/IMU、Lidar、Mobileye Camera、ESR 感知，并把控制命令下发到转向、油门和制动执行器。 | 该样本对 PATH2 的主要价值在 C2 和 C4：收益评估、TTC、速度、合法性等变量能支撑 symbolic guard grounding，实车线控平台又给了明确 actuator 映射。它也是独立的自动驾驶控制样本，NL 描述较清晰，适合作为 T0 中等规模 case。 |

### 详细卡片

#### HSM-layered （6 条）

##### 1. `[159]` 🌡️ Water-filter test-bench main-state and valve supervisor (HSM-layered)

- **领域**: 🌡️
- **论文**: paper #540 [`control-system-design-of-water-filter-test-bench`](../../../sources/control-system-design-of-water-filter-test-bench/STM.md)
- **是什么**: 该 case 建模水滤测试台的主模式监督器，以及阀门、泵、节流阀等执行器在 ΔP 测量、多通道测量、手动控制和 stop 路径下的允许操作。典型流程是从 Normal 进入 Lobby1/Lobby2/Lobby3，按传感器限值、泵阀状态和旁通状态守卫启动测试，异常时进入 automatic stop 或 safety stop 并限制泵使用。
- **scale**: states=61 / events=42 / vars=45 / trans=105
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文写 'The system is divided into 4 main states'，且 ΔP/Multi-pass/Manual 各有 Lobby，Normal initial setup 和 E.1 stop route 形成明确的多模式层次监督结构。
- **C2 数值守卫**: 🟡 — 原文给出 pressure reading over the critical allowed limit、water level in reservoir B.W.3 above/below certain limit、pump frequency maximum/minimum condition 等阈值 guard，但具体 limit values 被写成 X。
- **C3 forced fault**: 🟢 — 原文明确写 Route E.1 'can be entered from every state of the system'，automatic stop1/safety stop2 会 stop every pump 并 interrupt measuring events。
- **C4 硬件解耦**: 🟢 — 原文控制设备表列出 A.V.1-A.V.3、B.V.1-B.V.14 阀门，B.TV.1/B.TV.2 节流阀，A.PM/B.PM/B.SP 多个泵，且阀门由 solenoid coils actuated。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C1 的模式/层次结构、C3 的全局 stop 路径、C4 的大量物理执行器都能给 parse+semantic+sim feedback 提供 grounding。它是典型工业测试台控制对象，NL 与原文锚点清晰，和纯软件协议类样本差异明显。
- **风险**: 数值 limit 多以 X 或 certain limit 表示，TEST2/counter/report 等子状态未完全展开，因此 C2 可用但不宜当作强 Z3 数值样本。

<details><summary><b>📝 扩充 NL（280 词 / 21 markers / 21 provenance entries）</b></summary>

**Expanded NL**:

> The water-filter test-bench controller uses main states to decide which components the HMI may actuate and which state or sensor data it shows [E1]. From normal state it can enter measuring or manual-control modes [E2]; on power-up components are put in initial states [E3]. The E.1 stop route is reachable from every state [E4] and triggers when parameters cross allowed limits or emergency stop is pressed [E5]. In ΔP Measurement, the single internal state Lobby1 [E6] sets valves for that measurement [E7] and exposes pump B.PM.2, throttle valves B.TV.1 and B.TV2, valve B.V.12, and bypass control [E8]. In Multi-pass Measurement, entry activates Lobby2 and sets valves to initial multi-pass states [E9]; the test may start only when pumps A.PM.1, B.PM.1, B.PM.3, and A.PM.2 are on, sensor pumps are off, A.V.2 is right, B.V.12 is left, and bypass is active [E10]. Starting it turns dirt feed into the filter test system and starts reservoir collection to keep volume constant [E11]. It also turns sensor pumps and multi-pass counters on and gathers their data [E12]. The test ends on finish, stop2, automatic stop1, or safety stop2 [E13], and the last three options stop every pump and end the measuring event [E14]. Manual-control Lobby3 is also entered when automatic stop1 or safety stop2 becomes active [E15], and it shows all available sensor and state data [E16]. A.V.1 starts left and may turn right in Lobby3 only when B.W.1 is not full and the A.V.1 button is pressed [E17], and returns left after measurement selection [E18], TEST2 finish, or a full B.W.1 sensor [E19]. Guard, act and event limits are not defined because system details are unknown [E20] and are represented as X [E21].

**Axis coverage**:

- **C1**: C1 由 [E6][E7][E9] 暴露：ΔP Measurement 内部只有 Lobby1，进入该 mode 时设置阀门初始状态；Multi-pass Measurement 进入时激活 Lobby2 并设置 multi-pass 初始阀门状态。
- **C2**: C2 由 [E10][E20][E21] 暴露：multi-pass 启动条件是泵、sensor pump、阀向与 bypass 的复合 guard；原文未给具体数值阈值，只说明 limit values 未定义并以 X 表示。
- **C3**: C3 由 [E4][E5][E13][E14][E15] 暴露：E.1 可从 every state 进入，stop2/automatic stop1/safety stop2 会停止所有泵并结束测量，stop 状态还会进入 Lobby3。
- **C4**: C4 由 [E8][E10][E11][E12][E17][E19] 暴露：具体物理对象包括 pump B.PM.2、A.PM.1/B.PM.1/B.PM.3/A.PM.2、sensor pumps、valves A.V.1/A.V.2/B.V.12、throttle valves 与 bypass。

**Provenance** (21 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A/B \| paper.pdf p.34 §4.5.2 \| paper_content.txt 行 1080-1086 | Purpose of main states are to define when and which components can be actuated from the HMI and w… | main states decide HMI actuation and displayed state/sensor data |
| [E2] | STM §1 摘录 B \| paper.pdf p.34 §4.5.2 \| paper_content.txt 行 1080-1084 | Options are two different measuring states ISO 16689 and ISO 3968 and a manual control state. | normal state can enter measuring or manual-control modes |
| [E3] | paper.pdf p.34 §4.5.2 \| paper_content.txt 行 1090-1091 | When the power is turned on to the system the components are set into their initial states | on power-up components are put in initial states |
| [E4] | STM §1 摘录 B \| paper.pdf p.34 §4.5.2 \| paper_content.txt 行 1092-1095 | E.1 can be entered from every state of the system. | E.1 stop route is reachable from every state |
| [E5] | STM §1 摘录 B \| paper.pdf p.34 §4.5.2 \| paper_content.txt 行 1092-1094 | Route E.1 is a stop feature, that triggers when system parameters are over or under their allowed… | E.1 trigger conditions |
| [E6] | STM §1 摘录 B \| paper.pdf p.35 §4.5.2 \| paper_content.txt 行 1104 | ΔP Measurement has only one state and it is called Lobby1 | ΔP Measurement contains the single internal state Lobby1 |
| [E7] | STM §1 摘录 B \| paper.pdf p.35 §4.5.2 \| paper_content.txt 行 1104-1106 | When the state is entered, valves are set into initial states suited for the ΔP measurement. | entering Lobby1 sets valves for ΔP measurement |
| [E8] | STM §1 摘录 B \| paper.pdf p.35 §4.5.2 \| paper_content.txt 行 1106-1108 | In lobby1 a user can control pump B.PM.2, Throttle valves B.TV.1 and B.TV2, valve B.V.12 for clea… | Lobby1 exposes named pump, throttle valves, valve B.V.12, and bypass control |
| [E9] | STM §1 摘录 B \| paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1119-1122 | When the state is entered, a lobby2 state becomes active and systems valves are set into their in… | Multi-pass entry activates Lobby2 and initial multi-pass valve states |
| [E10] | STM §1 摘录 B \| paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1126-1128 | pumps A.PM.1, B.PM.1, B.PM.3 and A.PM.2 has to be on, sensor pumps must be off, valve A.V.2 must … | multi-pass start compound guard |
| [E11] | paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1128-1132 | dirt feed is turned into the filter test system, extra water is being collected by the reservoir … | multi-pass start effects on dirt feed and reservoir collection |
| [E12] | paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1132-1134 | sensor pumps are turned on and all the needed counters for the multi-pass test are turned on and … | sensor pumps, counters, and data gathering start |
| [E13] | paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1137-1138 | The test ends when the test is finished, when stop2 is pressed or when automatic stop1 state or s… | multi-pass test end conditions |
| [E14] | paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1138-1139 | Last three of the four options mentioned will stop every pump of the system and also ends the mea… | stop2/automatic stop1/safety stop2 stop every pump and end measurement |
| [E15] | STM §1 摘录 B \| paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1147-1151 | lobby3 is also entered when automatic stop1 or safety stop2 state becomes active. | manual-control Lobby3 is entered on automatic stop1 or safety stop2 |
| [E16] | paper.pdf p.36 §4.5.2 \| paper_content.txt 行 1147-1149 | There, a user can control every control device of the system and see all the available sensor and… | Lobby3 shows available sensor and state data |
| [E17] | STM §1 摘录 C \| paper.pdf p.38 §4.5.3 \| paper_content.txt 行 1200-1203 | Its initial state is left. It can be turned to right in manual control lobby3 if reservoir B.W.1 … | A.V.1 initial-left state and guarded right transition |
| [E18] | STM §1 摘录 C \| paper.pdf p.38 §4.5.3 \| paper_content.txt 行 1205-1207 | Control valve is turned back to left when multi-pass measurement or ΔP measurement is pressed in … | A.V.1 returns left after measurement selection |
| [E19] | STM §1 摘录 C \| paper.pdf p.38 §4.5.3 \| paper_content.txt 行 1207-1208 | multi-pass test (TEST2) is finished or if reservoir of B.W.1 sensor is full. | A.V.1 returns left after TEST2 finish or full B.W.1 sensor |
| [E20] | paper.pdf p.33 \| paper_content.txt 行 1070-1072 | None of the limit values set as guards, acts and events in the state machine diagrams to come are… | guard, act and event limits are not defined because system details are unknown |
| [E21] | paper.pdf p.33 \| paper_content.txt 行 1070-1072 | therefore they’re presented as X. These values has to be set later. | undefined limits are represented as X |

**Intentional omissions**: 没有补写具体压力、流量或时间阈值，因为原文明确这些 limit values 尚未定义并以 X 表示。没有枚举全部阀门/泵状态机，也没有编造新的故障类型、传感器型号或恢复路径。

</details>


##### 2. `[010]` ✈️ Master-and-Autopilot Mission Cycle for Autonomous Rotorcraft UAS (HSM-layered)

- **领域**: ✈️
- **论文**: paper #160 [`long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition`](../../../sources/long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition/STM.md)
- **是什么**: 该 case 控制长时自主旋翼 UAS 在充电站、起飞、任务飞行、返航、精确着陆和紧急降落之间的任务循环；它使用电池/电机健康、GPS/状态估计、下视相机 AprilTag、触地高度与速度阈值等信息，驱动飞控、电机、返航和着陆动作。
- **scale**: states=27 / events=17 / vars=12 / trans=48
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文明确说 high-level decision making 是 “hierarchy of master and slave state machines”，且 master 在 takeoff / mission / landing / emergency landing 状态中激活对应 autopilot 并等待完成。
- **C2 数值守卫**: 🟢 — 原文给出 motor nominal performance 需在 nominal value 的 400 RPM 内、最多 ten attempts，并给出 touchdown guard：高度差 < 0.3 且垂直速度 |v| < 0.1。
- **C3 forced fault**: 🟢 — 原文说 master “can also abort each autopilot”，并举例 critical battery 时 mission 和 landing 可 mid-execution abort 以执行 emergency landing。
- **C4 硬件解耦**: 🟡 — 原文涉及 vertical velocity command to low-level velocity controller、motor RPM 检查、turn off motors、charging pad/data handling，但执行器类型主要集中在飞控/电机与充电接口。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：它同时有清晰 HSM 层次、跨 autopilot abort/紧急降落、复合数值 guard 和真实硬件动作，能覆盖 C1/C2/C3 的 grounding 需求。NL 描述独立、工业控制意味强，不只是 toy FSM。
- **风险**: 图 18 中不少流程框偏实现步骤，建模时需要避免把参数加载、数据库读写等非控制状态过度展开。

<details><summary><b>📝 扩充 NL（272 词 / 16 markers / 16 provenance entries）</b></summary>

**Expanded NL**:

> The system is a fully autonomous rotorcraft UAS for repeated long-term observation flights without human intervention, and its high-level decision logic is a hierarchy of master and slave state machines [E1] [E2]. The master has takeoff, mission, landing, and emergency landing states; in each state it activates the appropriate autopilot and waits for completion [E3]. During takeoff, the controller starts from a motors-off vehicle on the charging pad, validates motor nominal performance, reinitializes the state estimator after charging, stores the current horizontal location in permanent memory, and climbs to the target takeoff altitude [E4] [E5]. Before takeoff, motors are spun at low RPM, measured by zero-crossing detection, and accepted only when they rotate within 400 RPM of nominal; after ten failed attempts, takeoff is aborted [E6] [E7]. The mission autopilot executes the user-defined data-acquisition mission as waypoints with hover times, either once or continuously, until a low-battery event requests return to the charging pad [E8] [E9]. For landing, the autopilot begins from a hover near the pad, checks the downfacing navigation-camera image for any AprilTag in the bundle, and if none is detected commands a spiral grid search until the bundle is visible [E10] [E11] [E12]. It then uses the landing position estimate to align lateral position over the charging pad, descends at constant velocity, and declares touchdown when height is below 0.3 m AND vertical-speed magnitude is below 0.1 m/s [E13] [E14]. As a robustness path, the master can abort autopilots for low battery in flight or abnormal motor performance before takeoff, and critical battery voltage triggers an emergency lander that performs a soft touchdown at the current location [E15] [E16].

**Axis coverage**:

- **C1**: C1 由 hierarchy of master and slave state machines 以及 master 的 takeoff/mission/landing/emergency landing phase 边界暴露 [E2][E3]；原文未明确给出复合状态默认初始子状态，因此未硬写 init pseudo。
- **C2**: C2 由 motor within 400 RPM、ten attempts、touchdown height 0.3 m AND vertical speed 0.1 m/s 等数值守卫暴露 [E6][E7][E14]。
- **C3**: C3 只使用原文支持的跨 phase abort 语义：master 可 abort each autopilot，critical battery voltage 触发 emergency lander [E15][E16]；未扩写为任意状态强制跳转。
- **C4**: C4 由 motors、downfacing navigation camera、AprilTag bundle、charging pad 等物理执行器/传感器/外部对象暴露 [E6][E11][E13]。

**Provenance** (16 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 36-37 | fully autonomous rotorcraft UAS that is capable of performing repeated flights for long-term obse… | fully autonomous rotorcraft UAS for repeated long-term observation flights wi… |
| [E2] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 40-42 | High-level autonomous decision making is implemented as a hierarchy of master and slave state mac… | high-level decision logic is a hierarchy of master and slave state machines |
| [E3] | STM §1 摘录 B \| paper.pdf p.20 §7.2 \| paper_content.txt 行 490-493 | In the takeoff, mission, landing and emergency landing states the master state machine activates … | master states and autopilot activation/completion wait behavior |
| [E4] | paper.pdf p.20 §7.3 \| paper_content.txt 行 499-500 | takes the UAS from a motors-off state on the charging pad to a hover at a target takeoff altitude. | takeoff starts motors-off on charging pad and climbs to target takeoff altitude |
| [E5] | paper.pdf p.20 §7.3 \| paper_content.txt 行 500-502 | after successfully validating motor nominal performance, re-initializing the state estimator afte… | motor validation, state-estimator reinitialization, and storing horizontal lo… |
| [E6] | paper.pdf p.20 §7.3 \| paper_content.txt 行 504-506 | Motors are spun at a low RPM, which is measured via zero crossing detection, and are verified to … | motor RPM check, zero-crossing measurement, and 400 RPM threshold |
| [E7] | STM §1 摘录 B \| paper.pdf p.20 §7.3 \| paper_content.txt 行 506-507 | Ten attempts to pass this check are allowed before the takeoff is aborted. | ten failed attempts abort takeoff |
| [E8] | paper.pdf p.21 §7.4 \| paper_content.txt 行 517-518 | executing the actual data acquisition mission as defined by the user in the form of individual wa… | mission as user-defined waypoints with hover times |
| [E9] | paper.pdf p.21 §7.4 \| paper_content.txt 行 519-520 | The mission trajectory is performed either once or is re-flown continuously until an event such a… | mission once/continuous execution and low-battery return request |
| [E10] | paper.pdf p.21 §7.5 \| paper_content.txt 行 522-523 | The landing autopilot safely takes the UAS from a hovering state in the vicinity of the landing p… | landing begins from hover near the pad |
| [E11] | STM §1 摘录 C \| paper.pdf p.21 §7.5 \| paper_content.txt 行 523-525 | The first action is to check if the landing pad is visible in the downfacing navigation camera im… | downfacing camera and AprilTag bundle visibility check |
| [E12] | STM §1 摘录 C \| paper.pdf p.21 §7.5 \| paper_content.txt 行 525-526 | If not, the UAS executes the spiral grid search trajectory until the landing bundle becomes visible. | spiral grid search when the bundle is not visible |
| [E13] | paper.pdf p.23 §7.5 \| paper_content.txt 行 544-546 | the landing position estimate is used to align the vehicle's lateral position over the center of … | landing position estimate aligns lateral position over the charging pad |
| [E14] | STM §1 摘录 C \| paper.pdf p.23 §7.5 \| paper_content.txt 行 546-551 | The vehicle then performs a constant velocity descent until touchdown is detected based on 0.3 m … | constant velocity descent and touchdown thresholds |
| [E15] | STM §1 摘录 B \| paper.pdf p.20 §7.2 \| paper_content.txt 行 493-497 | the master can also abort each autopilot in order to execute robust behaviors for cases like low … | master aborts autopilots for low battery or abnormal motor performance |
| [E16] | STM §1 摘录 C \| paper.pdf p.23 §7.6 \| paper_content.txt 行 553-554 | The emergency lander brings the UAS to a soft touchdown at its current location and is triggered … | critical battery voltage triggers current-location soft touchdown |

**Intentional omissions**: 没有加入 valve 编号、具体传感器型号、额外 mode 名或恢复路径，因为原文没有这些细节。也没有把 state estimation failure 写成本条 emergency lander 的主路径，因为 §7.6 明确将其与 Figure 15 的 state-estimation-failure controller 区分开。

</details>


##### 3. `[015]` ⚙️ Greenhouse row-inspection navigation supervisor (HSM-layered)

- **领域**: ⚙️
- **论文**: paper #170 [`autonomous-navigation-framework-holonomic-mobile-robots-agriculture`](../../../sources/autonomous-navigation-framework-holonomic-mobile-robots-agriculture/STM.md)
- **是什么**: 该 case 控制温室全向移动机器人在 headland 与作物行之间的导航巡检流程，利用 stereo camera、LiDAR、语义分割和 TEB/SMACH 导航栈调度 waypoint 导航、轨道对齐、行内前进巡检与后退返回。典型流程是 WAIT_FOR_GOAL 接收行巡检任务后进入 PLAN_EXEC，再进入 VISUAL_SERVOING 中的 TARGET_ALIGNMENT 与 TRAVERSE_FORWARD/INSPECT/TRAVERSE_BACKWARD 循环。
- **scale**: states=7 / events=8 / vars=6 / trans=14
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文明确写到从 WAIT_FOR_GOAL 转入 PLAN_EXEC block，成功后转入 VISUAL_SERVOING block，后者包含 TARGET_ALIGNMENT 以及 TRAVERSE_FORWARD、INSPECT、TRAVERSE_BACKWARD 的迭代过程。
- **C2 数值守卫**: 🟢 — 原文轨道对齐部分给出 dθ≈0、dy≈0、dx≈0 三个持续检查条件，并说明全部满足时 alignment process completed，可作为复合数值 guard。
- **C3 forced fault**: 🟢 — 原文写明 any failure that may occur throughout the entire operation returns to a common state, reported as invalid, aborted, or a failure, and then to initialization state。
- **C4 硬件解耦**: 🟡 — 原文涉及物理移动底盘的 velocity vector/linear and angular velocity commands、metallic wheels 和 heating-pipe rails，但该 FSM 中明确控制的主要硬件出口仍集中在移动底盘导航。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：它同时具备层次化 block、复合数值对齐 guard 和跨全流程 failure recovery，能直接支撑 C1/C2/C3 的 in-loop grounding。NL 描述清晰、对象是真实农业机器人导航监督控制器，且与常见纯软件协议样本差异明显。
- **风险**: C4 不宜高估，UR10e、升降台和喷洒机构虽在平台描述中出现，但本 case 的 FSM 证据主要覆盖导航底盘而非多执行器工艺控制。

<details><summary><b>📝 扩充 NL（238 词 / 8 markers / 8 provenance entries）</b></summary>

**Expanded NL**:

> The navigation supervisor controls a holonomic greenhouse mobile robot whose finite state machine sequences automated row-inspection actions, while a single stereo camera supplies perception and a LiDAR sensor supplies distance measurements [E1]. It starts each mission in the initialization/WAIT_FOR_GOAL mode by acquiring the greenhouse occupancy grid map, reading the user's mission instructions that specify the rows to inspect, configuring localization, and deriving the action sequence for the mission [E2]. When a mission is available, the controller enters the headland-planning PLAN_EXEC block; the robot moves toward the pre-known target at the beginning of the selected corridor, and the TEB local planner uses laser-scanner costmap updates to produce collision-free trajectories that respect kinematics and obstacle distance [E3][E4]. After PLAN_EXEC finishes successfully, the controller enters VISUAL_SERVOING, whose default first phase is rail target alignment before the in-row process begins [E5]. During alignment, semantic segmentation and stereo depth provide rail geometry, and completion is guarded by the angular, lateral, and longitudinal divergences from the rail midpoint all being approximately zero [E6]. In the row, motion is limited to forward and backward x-axis movement; after a corridor has been traversed, negative linear velocity commands return the robot toward the row start, and rail navigation stops when row endpoints enter the robot's field of view [E7]. When the row task is complete, the FSM returns to WAIT_FOR_GOAL, but any failure anywhere in the operation is routed through a common invalid/aborted/failure outcome before reinitialization [E8].

**Axis coverage**:

- **C1**: C1 由 initialization/WAIT_FOR_GOAL、PLAN_EXEC、VISUAL_SERVOING 以及进入 VISUAL_SERVOING 后先执行 rail target alignment 暴露，对应 [E2][E3][E5]。
- **C2**: C2 由 alignment 完成条件暴露：角向、横向、纵向偏差 dθ/dy/dx 都近似为零才完成，对应 [E6]；原文没有给具体数值阈值。
- **C3**: C3 由「any failure anywhere in the operation」统一进入 common invalid/aborted/failure outcome 再初始化暴露，对应 [E8]；原文不支持每 cycle safety aspect。
- **C4**: C4 由 single stereo camera、LiDAR、laser scanners、robot velocity commands 暴露，对应 [E1][E4][E7]；原文未给具名 motor/valve 类 effector。

**Provenance** (8 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 49-53 | Our approach utilizes the heating system rails to navigate through the crop rows using a single s… | holonomic greenhouse robot, finite state machine orchestration, stereo-camera… |
| [E2] | STM §1 摘录 B/C \| paper.pdf p.9 §3.4 \| paper_content.txt 行 395-399, 421 | acquisition of both the greenhouse occupancy grid map and the user's mission instructions, which … | initialization/WAIT_FOR_GOAL acquires map, mission rows, localization setup, … |
| [E3] | STM §1 摘录 C \| paper.pdf p.10 §3.4 / Figure 8 \| paper_content.txt 行 421-424 | there is a transition to the PLAN_EXEC block, which contains the headland planning that is perfor… | mission-triggered transition into PLAN_EXEC and use of TEB for headland planning |
| [E4] | paper.pdf p.11 §3.5 \| paper_content.txt 行 443-449 | The local planner operates on a local costmap that updates in real-time with the input from the l… | laser-scanner costmap updates and collision-free trajectories respecting moti… |
| [E5] | STM §1 摘录 C/D \| paper.pdf p.10 §3.4 / Figure 8 \| paper_content.txt 行 424-427 | there is a transition to the VISUAL_SERVOING block, which is responsible for the in-row processes… | successful PLAN_EXEC leads to VISUAL_SERVOING and default first alignment phase |
| [E6] | paper.pdf p.12-13 §3.6 \| paper_content.txt 行 519-529, 545-547 | At each timestep the robot calculates its divergence from pmiddle, which is expressed as dθ, dy a… | alignment variables and composite approximately-zero completion guard |
| [E7] | paper.pdf p.13 §3.7 \| paper_content.txt 行 549-565 | the mobility of the robot is constrained to only two directions: forward and backward | in-row forward/backward x-axis motion, negative return velocity, and endpoint… |
| [E8] | STM §1 摘录 D \| paper.pdf p.10 §3.4 / Figure 8 \| paper_content.txt 行 428-430 | any failure that may occur throughout the entire operation returns to a common state, which is re… | cross-cutting failure route through common invalid/aborted/failure outcome an… |

**Intentional omissions**: 没有添加阀门、马达编号、传感器阈值、timeout 或 emergency-stop 路径，因为原文没有提供这些细节。也没有把 Figure 8 中所有状态名逐一列出，以避免把 NL 变成状态清单。

</details>


##### 4. `[179]` 🏢 Robot Elevator Request-Floor-Estimation Recovery Supervisor (HSM-layered)

- **领域**: 🏢
- **论文**: paper #600 [`secure-automated-elevator-management-pressure-sensor-floor-estimation`](../../../sources/secure-automated-elevator-management-pressure-sensor-floor-estimation/STM.md)
- **是什么**: 该 case 控制室内移动机器人乘梯过程：AEMS 通过 Wi-Fi/ADAM 继电器呼梯与选层，压力传感器估计楼层，超声传感器识别门状态。典型流程是呼梯、进轿厢、按任务状态选择目标楼层、等楼层匹配且门打开后出梯，失败时进入内外两类错误恢复。
- **scale**: states=18 / events=14 / vars=15 / trans=36
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — STM §2 明确称为“layered control chain”和“two nested recovery branches”，原文第4节又将 EHS 分成 outside/inside 两套 error handling flowchart。
- **C2 数值守卫**: 🟢 — Fig.8/9 含 `PE<=3`、`pE<=2`、`AEE<=3`、`Fault Counter=F.Max` 等计数阈值，floor reader 还用 `Height(p)` 与楼层范围比较。
- **C3 forced fault**: 🟡 — 原文按 `outside or inside elevator error handling` 分别处理故障，失败会 warning/stop/return to charge，但没有明确写 from any state 的全局强制迁移。
- **C4 硬件解耦**: 🟢 — 原文写 ADAM 有 relay outputs 并连接 elevator controller，Fig.8 还包含 robot kinematic arm 按钮操作和 forward/backward 底盘纠偏。
- **对 PATH2 的价值**: 该样本对 PATH2 有价值，主要强在 C2 数值守卫和 C4 硬件动作解耦，同时具备较清晰的层次化乘梯/恢复结构。它是典型真实机器人-楼宇电梯控制对象，NL 描述较完整，和纯软件协议类样本不趋同。
- **风险**: 原文更像流程图和工程控制策略，真正 HSM 的 composite/exit 语义需要从外部/内部错误处理流程中重构，C3 不宜高估为全局 fault aspect。

<details><summary><b>📝 扩充 NL（278 词 / 23 markers / 23 provenance entries）</b></summary>

**Expanded NL**:

> The elevator supervisor belongs to a four-control-layer management system [E1], and MFS integrates EHS to control elevator operation through two sub-systems [E2]: the computer-vision/kinematic-arm path and AEMS [E3]. When a task requires another floor, AEMS calls the elevator to the robot's current floor [E4]; after entry, the movement core selects the destination from grasp/place/charge task status [E5]. AEMS controls the automated elevator over Wi-Fi through an ADAM module [E6] and translates the required floor into hardware port and pin numbers [E7]. During in-elevator floor estimation, an LPS25HB pressure sensor and STM32F411 microcontroller provide the hardware platform [E8]; the microcontroller collects pressure data and applies a smoothing filter [E9], then sends data to the robot computer every 1 s [E10]. Before entry, adaptive calibration aligns sensor readings with the robot's current floor [E11], and the extracted height is compared with each floor's height range [E12]. The robot may leave only when the destination floor matches the estimated current floor AND the ultrasonic sensor recognizes the door as open [E13]. In the outside-error branch, EHS initializes counters [E14], retries position/orientation correction up to three times [E15], uses RGB-D button localization and the robot arm [E16], and falls back to AEMS over Wi-Fi if previous attempts fail [E17]. Inside-error handling continuously checks the current floor reader [E18], sends RRC warnings after specified floor or door failures [E19], returns to the elevator and reselects the destination after missing or wrong landmarks [E20], and sends an error message after maximum allowed attempts [E21]. Reconnection logic closes and reinitializes the Wi-Fi socket when elevator-status data is missing [E22] and closes and initializes the serial port when sensor-board messages are missing until updates resume [E23].

**Axis coverage**:

- **C1**: C1 由 [E1]-[E3] 的四层管理系统、MFS/EHS 边界与两个 EHS 子系统暴露，并由 [E14]/[E18] 分别给出 outside/inside error handling 的入口动作。
- **C2**: C2 由 [E13] 的 destination floor match AND door open 复合 guard、[E15] 的 three-times retry 阈值、[E10] 的 1 s 数据周期暴露；inside 的 specified/max attempts 原文未给具体数值。
- **C3**: C3 仅弱支持：原文支持 [E22]/[E23] 的通信/传感器数据缺失重连这种横切恢复逻辑，但没有任意状态 forced fault 钩子。
- **C4**: C4 由 [E6]-[E17] 的 ADAM/Wi-Fi、LPS25HB+STM32F411、ultrasonic sensor、RGB-D camera、robot arm、AEMS 等具名传感器/执行器暴露。

**Provenance** (23 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | paper.pdf p.3 §2 System Structure \| paper_content.txt 行 217-220 | This system has four control layers. | four-control-layer management system |
| [E2] | paper.pdf p.3 §2 System Structure \| paper_content.txt 行 236-238 | The MFS is integrated with the Elevator Handling System (EHS) to control elevator operation. | MFS integrates EHS to control elevator operation |
| [E3] | paper.pdf p.3 §2 System Structure \| paper_content.txt 行 238-241 | elevator handling based computer vision [23] with kinematic arm solution for pressing operation [… | computer-vision/kinematic-arm path and AEMS |
| [E4] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 302-304 | The AEMS calls the elevator to the robot’s current floor when the mobile robot needs the elevator… | AEMS calls the elevator to the robot's current floor |
| [E5] | STM §1 摘录 B \| paper.pdf p.3-4 §3.1 \| paper_content.txt 行 306-318 | the movement core depends on the transportation task status (Grasp Position Done, Place Position … | destination selected from grasp/place/charge task status |
| [E6] | STM §1 摘录 B \| paper.pdf p.3 §3.1 \| paper_content.txt 行 282-284 | This system controls the AE over Wi-Fi socket. The AE consists mainly of an ADAM module | AEMS controls the automated elevator over Wi-Fi through an ADAM module |
| [E7] | paper.pdf p.3 §3.1 \| paper_content.txt 行 296-298 | It translates the required elevator destination floor into a specific hardware port and pin numbers. | translates required floor into hardware port and pin numbers |
| [E8] | STM §1 摘录 A \| paper.pdf p.3-4 §2/§3.2 \| paper_content.txt 行 243-250, 363-365 | An LPS25HB pressure sensor and STM32F411 microcontroller are used in the current floor estimation… | LPS25HB pressure sensor and STM32F411 microcontroller provide the hardware pl… |
| [E9] | paper.pdf p.4 §3.2 \| paper_content.txt 行 399-402 | collecting the pressure sensor data, applying the smoothing filter to these data | microcontroller collects pressure data and applies smoothing filter |
| [E10] | paper.pdf p.4 §3.2 \| paper_content.txt 行 399-403 | finally sending it over USB to the robot computer every 1s. | sends data to the robot computer every 1 s |
| [E11] | paper.pdf p.4 §3.2 \| paper_content.txt 行 403-406 | calibrate the sensor readings to the robot’s current floor before entering the elevator | adaptive calibration before entry aligns readings with current floor |
| [E12] | paper.pdf p.5 §3.2 \| paper_content.txt 行 420-424 | extracted height is compared with the height range of each floor to identify the current robot’s … | extracted height compared with each floor's height range |
| [E13] | STM §1 摘录 C \| paper.pdf p.5 §3.2 \| paper_content.txt 行 450-454 | When the destination floor matches the estimated robot’s current floor and the elevator’s door st… | compound exit guard: destination floor match AND door open |
| [E14] | paper.pdf p.6 Figure 8 \| paper_content.txt 行 523-524 | Initialize the error Handling Counter (PE, PE, and AEE) | outside-error branch initializes counters |
| [E15] | STM §1 摘录 C \| paper.pdf p.5 §4 \| paper_content.txt 行 488-491 | tries to correct it three times | position/orientation correction retried up to three times |
| [E16] | paper.pdf p.5-6 §4/Figure 8 \| paper_content.txt 行 492-496, 529-534 | Button Detection and extraction the real word coordinates using the RGB-D camera | RGB-D button localization and robot arm button-pressing path |
| [E17] | STM §1 摘录 C \| paper.pdf p.5 §4 \| paper_content.txt 行 499-500 | If previous attempts have failed, the EHS selects the AEMS over the Wi-Fi socket to open the door. | fallback to AEMS over Wi-Fi after previous attempts fail |
| [E18] | STM §1 摘录 C \| paper.pdf p.5 §4 \| paper_content.txt 行 503-505 | starts by monitoring whether or not the destination floor has been reached by continuously checki… | inside-error handling continuously checks the current floor reader |
| [E19] | STM §1 摘录 C \| paper.pdf p.5 §4 \| paper_content.txt 行 506-509 | the MFS sends a warning alarm to the RRC | RRC warnings after specified floor or door failures |
| [E20] | STM §1 摘录 C \| paper.pdf p.5 §4 \| paper_content.txt 行 510-512 | If the landmark is missing or a wrong floor number landmark is read, the error handling system re… | return to elevator and reselect destination after missing or wrong landmarks |
| [E21] | STM §1 摘录 C \| paper.pdf p.5 §4 \| paper_content.txt 行 512-515 | after reaching the maximum allowed number of attempts, an error message is sent to the RRC | error message after maximum allowed attempts |
| [E22] | STM §1 摘录 B \| paper.pdf p.4 §3.1 \| paper_content.txt 行 333-340 | In case of missing data, the function closes the socket to AE and then initializes the connection… | Wi-Fi socket close/reinitialize on missing elevator-status data |
| [E23] | paper.pdf p.5 §3.2 \| paper_content.txt 行 424-427 | In the case of missing data, the serial port will close and initialize again till receiving the u… | serial port close/initialize on missing sensor-board messages |

**Intentional omissions**: 没有补写楼层高度阈值、I.Max/D.Max/F.Max 具体数值、门控时间或紧急停止 forced fault，因为原文没有给出明确数值或全局强制迁移语义。也没有展开 Figure 8/9 的全部计数器与状态名，避免把 flowchart 直接枚举成 DSL 提示。

</details>


##### 5. `[012]` ⚙️ Multi-modal drive-fly mission FSM for TURVTOL (HSM-layered)

- **领域**: ⚙️
- **论文**: paper #166 [`terrestrial-unmanned-roving-vertical-take-off-and-landing-turvtol`](../../../sources/terrestrial-unmanned-roving-vertical-take-off-and-landing-turvtol/STM.md)
- **是什么**: 该 case 控制 TURVTOL 多模态自主 rover/drone 的任务监督 FSM，利用 SLAM、path planner、VIO、wheel encoders 和电池/地形安全信号在地面行驶、起飞、飞行、悬停、找降落点、降落、牵引恢复和休眠充电之间切换。执行侧涉及 differential-drive wheel motors、coaxial rotors/flying motors 以及 Pixhawk/PX4/MAVROS 飞控命令。
- **scale**: states=14 / events=22 / vars=9 / trans=34
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文第34页明确写到 hierarchical design，顶层有 FLY_OPERATE 和 DRIVE_OPERATE，且 FLY_OPERATE contains a LANDING sub-machine，DRIVE_OPERATE contains TRACTION_LOSS 和 DORMANT sub-machine。
- **C2 数值守卫**: 🟢 — Table 5 给出 low_battery 是 battery level below threshold，return_to_safe 涉及 specified search radius，slipping/stuck 由 VIO moving more/less than encoders indicate 触发，属于多数值变量比较守卫。
- **C3 forced fault**: 🟡 — 原文有多处安全/异常路径，如 land 可由 battery low 或 no current destination 触发，TRACTION_LOSS 处理 stuck/slipping/flipped，但没有明确 from any state 或 any mode 的全局 fault transition。
- **C4 硬件解耦**: 🟢 — 原文控制段写 pwm signal gets sent to the motors，并且 MAVROS commands 初始化 mode changes、arming/disarming、takeoff/landing，autopilot 再 sends corresponding signals to the flying motors。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C1 层次结构非常明确，C2 有电池阈值、搜索半径、VIO/encoder 对比等可符号化守卫，C4 也有清晰硬件动作出口。NL 与原文表格/图对应关系清楚，且多模态 rover-drone 不容易与普通工业 FSM 趋同。
- **风险**: 主要风险是原文说明 FSM structure 已实现但 state methods 仍属 future work，部分 guard 语义偏自然语言而非完整公式。

<details><summary><b>📝 扩充 NL（269 词 / 27 markers / 27 provenance entries）</b></summary>

**Expanded NL**:

> The TURVTOL mission supervisor is a ROS SMACH hierarchical FSM with two top-level operating branches, FLY_OPERATE for airborne behavior and DRIVE_OPERATE for ground behavior [E1][E2][E3]. The flight branch contains LANDING for search, return, and landing protocols, while the drive branch contains TRACTION_LOSS and DORMANT behavior for stuck/slipping/flipped recovery plus charging and sleeping [E4][E5][E6]. In ground traversal, terrain that makes takeoff difficult moves the controller out of normal driving, telling the path planner not to consider flight paths until level terrain returns [E7][E8]. A takeoff transition depends on path-planner confirmation, and safe_takeoff combines suitable terrain with battery high enough for safe flight [E9][E10]. Once airborne, the FSM can continue flying on path-planner confirmation, wait for planner updates, or start landing when the planner confirms landing, battery is low, or no destination remains [E11][E12][E13]. During landing, it assesses terrain below, lands only after safe_landing is ensured, and returns to the known launch site when no safe landing can be made within the specified search radius [E14][E15][E16][E17]. Across the mission, transition signals come from what SLAM, the path planner, the control loop, and environmental factors detect or calculate, monitoring battery level, landing/takeoff safety, and flying conditions [E18][E19]. The safety loop compares VIO pose with wheel encoders; VIO-greater-than-encoder motion means slipping, the opposite case means stuck, and both cases trigger traction-regaining protocols [E20][E21][E22]. At the driving-control layer, distance error below 5 centimeters switches waypoints and sets linear velocity to zero [E23]. Motor-facing actions remain in the surrounding control stack: driving uses PWM signals to motors, while flight sends MAVROS/MAVLink mode-change, arming/disarming, and takeoff/landing messages to the autopilot, which signals the flying motors [E24][E25][E26][E27].

**Axis coverage**:

- **C1**: expanded_nl 前两句通过 [E1]-[E6] 暴露 ROS SMACH 层次 FSM、FLY_OPERATE/DRIVE_OPERATE 顶层分支以及 LANDING/TRACTION_LOSS/DORMANT 复合边界；原文未说明进入复合 mode 的默认初始子状态，因此未写默认入口。
- **C2**: expanded_nl 通过 [E9][E10] 暴露 safe_takeoff 的复合守卫 terrain suitable AND battery high enough，并通过 [E23] 暴露 distance error < 5 centimeters 的数值阈值；原文未给 battery threshold 或 search radius 的具体数值。
- **C3**: expanded_nl 通过 [E18]-[E22] 暴露跨任务 transition-signal 监控与 VIO/wheel-encoder 安全比较；原文支持连续安全监控，但不支持任何 forced emergency/global fault transition。
- **C4**: expanded_nl 通过 [E24]-[E27] 暴露 PWM-to-motors、MAVROS/MAVLink flight messages、autopilot-to-flying-motors 的硬件/外部控制接口；原文未把这些动作绑定为某个 mode 的 enter/exit action。

**Provenance** (27 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.34 §V.E.2 FSM Design | A finite state machine (FSM) has been designed and the general structure has been implemented usi… | ROS SMACH FSM |
| [E2] | STM §1 摘录 A \| paper.pdf p.34 §V.E.2 FSM Design | At a high level, the states are FLY_OPERATE and DRIVE_OPERATE. | two top-level operating branches |
| [E3] | paper.pdf p.34 §V.E.2 FSM Design | The FLY OPERATE state handles operations when the vehicle is in the air, and the DRIVE_OPERATE st… | airborne behavior and ground behavior |
| [E4] | STM §1 摘录 A \| paper.pdf p.34 §V.E.2 FSM Design | The FLY OPERATE sub-machine contains a LANDING sub-machine, which contains states for executing s… | LANDING branch for search, return, and landing protocols |
| [E5] | STM §1 摘录 A \| paper.pdf p.34 §V.E.2 FSM Design | The DRIVE_OPERATE sub-machine contains a TRACTION_LOSS sub-machine | TRACTION_LOSS behavior in the drive branch |
| [E6] | STM §1 摘录 A \| paper.pdf p.34 §V.E.2 FSM Design | DRIVE_OPERATE also contains the DORMANT sub-machine, which handles charging and sleeping states f… | DORMANT behavior for charging and sleeping |
| [E7] | STM §1 摘录 C \| paper.pdf p.33 §V.E.1 Design Criteria | when the vehicle is driving across terrain that would make it difficult for the vehicle to takeof… | terrain condition that changes ground traversal behavior |
| [E8] | STM §1 摘录 C \| paper.pdf p.33 §V.E.1 Design Criteria | inform the path planner to not even consider flight paths until the vehicle is back on level terr… | path planner avoiding flight paths until level terrain returns |
| [E9] | paper.pdf p.36 Table 5 | init_takeoff Path planner confirms takeoff | takeoff transition depends on path-planner confirmation |
| [E10] | paper.pdf p.36 Table 5 | safe_takeoff The current terrain is suitable for takeoff and vehicle’s battery is high enough to … | safe_takeoff guard combines terrain suitability and battery sufficiency |
| [E11] | STM §1 摘录 C \| paper.pdf p.36 Table 5 | continue_flight Path planner sends confirmation to continue flying (instead of landing) | continuing flight on path-planner confirmation |
| [E12] | STM §1 摘录 B \| paper.pdf p.34 Table 4 | HOVER Waiting for update from path planner | waiting for planner updates |
| [E13] | STM §1 摘录 C \| paper.pdf p.36 Table 5 | land Either path planner confirms landing or battery is low or there is no current destination | landing trigger conditions |
| [E14] | STM §1 摘录 B \| paper.pdf p.34 Table 4 | SEARCH_FOR_LANDING Assesses terrain below for safe landing location | landing branch assesses terrain below |
| [E15] | STM §1 摘录 C \| paper.pdf p.36 Table 5 | safe_landing Path planner confirms landing and safe landing has been ensured | landing only after safe_landing is ensured |
| [E16] | STM §1 摘录 B \| paper.pdf p.34 Table 4 | RETURN_TO_LAUNCH Cannot find safe landing location; return to known safe location (launch site) | return to known launch site |
| [E17] | STM §1 摘录 C \| paper.pdf p.36 Table 5 | return_to_safe Path planner confirms landing but a safe landing cannot be made within a specified… | specified search radius guard |
| [E18] | paper.pdf p.36 §V.E.2 FSM Design | transition signals that are assigned depending on what the SLAM algorithm, path planner, and cont… | transition signals from SLAM, path planner, and control loop |
| [E19] | paper.pdf p.36 §V.E.2 FSM Design | monitoring various parameters, such as battery level, safety of potential landings/takeoffs, and … | cross-mission monitoring parameters |
| [E20] | paper.pdf p.33 §V.D.5 Vehicle Safety | continuous comparisons of the vehicle’s pose as obtained through VIO and the wheel encoders | VIO and wheel encoder comparison |
| [E21] | paper.pdf p.33 §V.D.5 Vehicle Safety | the FSM will assume the vehicle is slipping and go into the SLIPPING state. If the opposite situa… | slipping and stuck interpretation |
| [E22] | paper.pdf p.33 §V.D.5 Vehicle Safety | In either case, the control loop will execute protocols to regain traction. | traction-regaining recovery |
| [E23] | paper.pdf p.31 §V.D.2 Control Loop Design | When the distance error is less than 5 centimeters, the control loop switches way points and sets… | 5-centimeter threshold and velocity effect |
| [E24] | paper.pdf p.30 §V.D.2 Control Loop Design | pwm is the signal that gets sent to the motors. | driving motor PWM output |
| [E25] | paper.pdf p.32 §V.D.4 Flying Control | forwarding the location information through the MAVLink protocol to the autopilot firmware using … | MAVLink/MAVROS flight command path |
| [E26] | paper.pdf p.32 §V.D.4 Flying Control | Additional messages are sent to initialize flight controller mode changes, arming/disarming and t… | mode-change, arming/disarming, and takeoff/landing messages |
| [E27] | paper.pdf p.32 §V.D.4 Flying Control | The autopilot interprets these messages and sends corresponding signals to the flying motors to e… | autopilot signaling flying motors |

**Intentional omissions**: 未补写电池阈值、搜索半径数值、风速阈值或具体恢复算法，因为原文只给出 threshold/radius 名称或说明恢复协议属未来工作。未写全局 emergency stop、forced fault path 或复合状态默认入口，因为 STM §1 与相关 PDF 页未提供这些语义。

</details>


##### 6. `[172]` ✈️ Building-interior firefighting mission supervisor (HSM-layered)

- **领域**: ✈️
- **论文**: paper #584 [`autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle`](../../../sources/autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle/STM.md)
- **是什么**: 这是一个室内消防 MAV 的高层任务监督 HSM，使用 GNSS、2D LIDAR、立体相机和热相机进行定位/感知，控制飞行电机、定位模式切换与水泵喷射。典型流程是起飞检查、室外绕楼找窗、穿窗进入、室内探索找火、灭火、原窗退出并返航降落。
- **scale**: states=17 / events=15 / vars=8 / trans=31
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟢 — 原文明确说整套行为结构是 hierarchical state machine，且 Figure 10 含 main、outdoor、indoor 和 flying-through-window 多个嵌套 state machine。
- **C2 数值守卫**: 🟡 — 原文给出纯阈值型条件，如飞到窗口中心前方 2 m、尝试可重复直到 maximum allowed flight time reached，但未形成复杂算术 guard。
- **C3 forced fault**: 🟢 — 原文写到 A landing event is called whenever any state produces an outcome that means the MAV cannot continue its mission，属于跨状态强制降落/恢复语义。
- **C4 硬件解耦**: 🟡 — 原文硬件动作包括 flight controller commands ESCs to drive brushless motors，以及 water bag、pump、nozzle 执行灭火喷射，但主要是电机和水泵两类执行器。
- **对 PATH2 的价值**: 该样本对 PATH2 很有价值：C1 的层次化子状态机调用、失败回退和 nested exit 语义清楚，C3 又有 any-state landing event，可直接检验生成-验证-反馈循环对 HSM 病态与 forced recovery 的 grounding。它也是实体机器人消防控制对象，NL 描述独立且流程完整。
- **风险**: 数值 guard 多为距离/时间阈值而非复杂符号算术，若只抽 mission supervisor 而不纳入灭火控制细节，C2 和 C4 的收益会偏中等。

<details><summary><b>📝 扩充 NL（273 词 / 28 markers / 28 provenance entries）</b></summary>

**Expanded NL**:

> The controller is a hierarchical state machine implemented with Flexbe that interconnects the UAV subsystems; after key-part verification it calls automatic takeoff, runs an outdoor phase then an indoor phase, and returns home to land [E1][E2][E3][E4][E5]. Entering the outdoor phase starts with flight to the known GNSS building position, while 2D LIDAR scans feed a virtual bumper that keeps planned motion outside the predefined safe distance from the building [E6][E7][E8]. At a safe position, the MAV flies along the building while detecting windows; when a window is located, it moves to 2 m from the window center, switches localization to indoor flying mode with LIDAR-based odometry feedback, and attempts the flythrough [E9][E10][E11]. The flythrough procedure hovers in front of the window, waits for an updated window estimate, then flies through the center to a goal behind it; if the estimate is lost while the MAV is still outside, Escaping returns it to the original hover point [E12][E13][E14][E15][E16]. Mission-wide landing behavior is present: any state outcome meaning the MAV cannot continue calls a landing event, and repeated window attempts also end in automatic landing after maximum allowed flight time [E17][E18]. In the indoor phase, the supervisor localizes fire, flies in front of it, extinguishes while the target is not lost, resumes exploration if it is lost, and exits through the entry window after all water is depleted [E19][E20][E21][E22]. For extinguishing, a validated fire target sends the MAV to 1.5 m in front of target q along normal nv; water spraying is enabled only inside the inner steering band, ±5° and ±0.075 m, and disabled once outside the outer band, ±10° and ±0.15 m [E23][E24][E25][E26][E27][E28].

**Axis coverage**:

- **C1**: C1 由层次状态机、outdoor/indoor phase，以及 entering outdoor phase starts with GNSS building-position flight 暴露；对应 [E1][E4][E6]，flythrough 内部顺序由 [E12]-[E16] 支撑。
- **C2**: C2 由 2 m window distance、1.5 m extinguishing distance、maximum allowed flight time，以及 ±5°/±0.075 m 与 ±10°/±0.15 m 内外 band 暴露；对应 [E10][E18][E24]-[E26]。
- **C3**: C3 由 any state outcome meaning the MAV cannot continue calls a landing event 这个横切/全局 landing 语义暴露；对应 [E17]，最大飞行时间自动降落由 [E18] 补充。
- **C4**: C4 由 LIDAR-based odometry 的 localization switch、automatic takeoff/landing、water spraying enable/disable 这些物理 IO/执行动作暴露；对应 [E3][E11][E17][E27][E28]。

**Provenance** (28 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.10 §II.F \| paper_content.txt 行 905-908 | constructed as a hierarchical state machine, which is used for interconnecting all the subsystems. | hierarchical state machine interconnecting UAV subsystems |
| [E2] | STM §1 摘录 A \| paper.pdf p.10 §II.F \| paper_content.txt 行 910-912 | The hierarchical state machine is implemented using the Flexbe library [40] | implemented with Flexbe |
| [E3] | STM §1 摘录 A \| paper.pdf p.10 §II.F \| paper_content.txt 行 928-932 | When every component is verified to be operational, an automatic takeoff is called. | key-part verification and automatic takeoff |
| [E4] | STM §1 摘录 A \| paper.pdf p.10 §II.F \| paper_content.txt 行 932-936 | The mission is divided into two parts: the outdoor phase and the indoor phase. | outdoor phase then indoor phase |
| [E5] | STM §1 摘录 A \| paper.pdf p.10 §II.F \| paper_content.txt 行 936-939 | the MAV flies back to the home position and lands. | return-home landing |
| [E6] | paper.pdf p.10 §II.F \| paper_content.txt 行 940-942 | The outdoor phase (Figure 10(c)) starts by flying to the known GNSS position of the building. | outdoor phase entry starts at known GNSS building position |
| [E7] | paper.pdf p.10 §II.F \| paper_content.txt 行 949-952 | the MAV uses scans provided by 2D LIDAR during the flight to facilitate navigation around the bui… | 2D LIDAR scans support navigation |
| [E8] | paper.pdf p.10 §II.F \| paper_content.txt 行 953-956 | prevents the MAV from following a plan that would lead it to go closer than the predefined safe d… | virtual bumper and predefined safe distance |
| [E9] | STM §1 摘录 B \| paper.pdf p.10 §II.F \| paper_content.txt 行 960-963 | starts flying alongside the building at a predefined distance with a heading towards the building | MAV flies along the building while detecting windows |
| [E10] | STM §1 摘录 B \| paper.pdf p.11 §II.F \| paper_content.txt 行 963-970 | flies in front of the window to distance of 2 m from its center. | 2 m from the window center |
| [E11] | STM §1 摘录 B \| paper.pdf p.11 §II.F \| paper_content.txt 行 970-973 | the localization of the MAV is switched to indoor flying mode (LIDAR-based odometry is used in th… | switch to indoor localization with LIDAR-based odometry |
| [E12] | STM §1 摘录 C \| paper.pdf p.11 §II.F \| paper_content.txt 行 985-991 | hovers in front of the center of the window to stabilize itself before the actual flythrough. | flythrough procedure begins with hover and stabilization |
| [E13] | STM §1 摘录 C \| paper.pdf p.11 §II.F \| paper_content.txt 行 991-993 | the state machine waits for an up-to-date window estimate corrected by new detections. | waits for an updated window estimate |
| [E14] | STM §1 摘录 C \| paper.pdf p.12 §II.F \| paper_content.txt 行 993-1005 | the MAV flies through the center of the window to a goal position at a predefined distance behind… | flies through window center to a goal behind it |
| [E15] | STM §1 摘录 C \| paper.pdf p.12 §II.F \| paper_content.txt 行 1005-1007 | If the window estimate is lost while the flythrough is in progress and the MAV is still outside t… | condition for Escaping branch |
| [E16] | STM §1 摘录 C \| paper.pdf p.12 §II.F \| paper_content.txt 行 1007-1009 | switches to the Escaping state and the MAV returns to its original hovering position | Escaping returns to original hover point |
| [E17] | paper.pdf p.10 §II.F \| paper_content.txt 行 920-922 | A landing event is called whenever any state produces an outcome that means that the MAV cannot c… | mission-wide landing behavior from any state outcome |
| [E18] | STM §1 摘录 B \| paper.pdf p.11 §II.F \| paper_content.txt 行 980-984 | The attempts can be repeated until the maximum allowed flight time is reached. After reaching thi… | repeated attempts end in automatic landing after maximum allowed flight time |
| [E19] | STM §1 摘录 D \| paper.pdf p.12 §II.F \| paper_content.txt 行 1010-1015 | Once the fire is detected, the MAV flies in front of it and begins extinguishing | fire localization, approach, and extinguishing start |
| [E20] | STM §1 摘录 D \| paper.pdf p.12 §II.F \| paper_content.txt 行 1015-1020 | the MAV depletes all the water that it is carrying during the extinguishing maneuver. | extinguishing while target is not lost and all water is depleted |
| [E21] | STM §1 摘录 D \| paper.pdf p.12 §II.F \| paper_content.txt 行 1020-1021 | In the case that the fire is lost, the MAV starts exploring again. | resumes exploration if fire is lost |
| [E22] | STM §1 摘录 D \| paper.pdf p.12 §II.F \| paper_content.txt 行 1021-1024 | the MAV flies back in front of the window that it entered through and tries to fly back outside t… | exits through the entry window |
| [E23] | paper.pdf p.9 §II.E \| paper_content.txt 行 855-857 | Upon obtaining the first validated fire detection state in the Kalman filter array | validated fire target |
| [E24] | paper.pdf p.9 §II.E \| paper_content.txt 行 856-863 | the MAV is sent to a position s 1.5 m in front of the given target q along the estimated normal nv. | 1.5 m in front of target q along normal nv |
| [E25] | paper.pdf p.10 §II.E \| paper_content.txt 行 878-884 | the inner range αi was set to ±5°, and the outer range αo was set to ±10°. | inner and outer angle bands |
| [E26] | paper.pdf p.10 §II.E \| paper_content.txt 行 884-887 | These were set to ±0.075 m for the inner range ri, and to ±0.15 m for the outer range ro. | inner and outer distance bands |
| [E27] | paper.pdf p.10 §II.E \| paper_content.txt 行 887-894 | Water spraying is only activated when the MAV is in this drifting state. | water spraying enabled in the inner steering condition |
| [E28] | paper.pdf p.10 §II.E \| paper_content.txt 行 901-904 | at which point water spraying is disabled. | water spraying disabled outside the outer band |

**Intentional omissions**: 原文没有提供阀门/泵编号、窗口编号、具体 maximum flight time 数值或 forced emergency-stop 事件，所以没有硬写这些内容。原文也没有给出灭火是否成功的传感反馈路径，因此只写 all water depleted 作为完成条件。

</details>


#### EFSM-interlock （6 条）

##### 1. `[143]` 🌡️ Auto-Manual WWTP Supervisor with Conductivity-Feedback Return Loop (EFSM-interlock)

- **领域**: 🌡️
- **论文**: paper #497 [`boiler-wastewater-treatment-control-monitoring-plc-hmi`](../../../sources/boiler-wastewater-treatment-control-monitoring-plc-hmi/STM.md)
- **是什么**: 该 case 是锅炉废水处理厂的 PLC/HMI 监督控制器，在自动/手动模式下协调 equalization、coagulation、flocculation、clarifier、final tank 等处理单元。它用 pH、电导率/TDS、液位等传感器驱动泵、搅拌器、电磁阀和电动阀，最终按电导率反馈决定排放或回流到 equalization unit。
- **scale**: states=9 / events=12 / vars=12 / trans=16
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文第5页写系统有 auto mode 与 manual mode 两种处理方法，HMI main control tab 可 activate/stop system 并 choose system mode，因此有模式切换但未见真正层次 init/pseudo 语义。
- **C2 数值守卫**: 🟢 — 原文第7页给出 pH 6-9、water channel <1500 ppm，并写 If water is > 1500 ppm, it will flow back，同时传感器读数用于决定 motorized control valve opening 和 solenoid valve bypass。
- **C3 forced fault**: 🟠 — 原文 Figure 4 只列 PAC Alarm、Polymer Alarm，且第7页说 abnormal circumstances 下用户可 take corrective actions quickly，未写 any mode/from any state 的强制 ErrorHandler。
- **C4 硬件解耦**: 🟢 — 原文 Figure 4 列出 intake/transfer/top-tank pump relay、agitator/mixer relay、PAC/polymer pump relay、motorized valves、blowdown/out solenoid valves 等多类物理执行器。
- **对 PATH2 的价值**: 该样本对 PATH2 主要价值在 C2 与 C4：既有明确数值阈值/回流 guard，又有大量真实 PLC 执行器输出，适合展示 symbolic guard feedback 与 abstract hardware handler。Auto/manual mode 也提供中等 C1 模式切换风险，且工业控制对象清晰独立。
- **风险**: 原文只给局部 ladder 截图和高层流程描述，完整迁移顺序需要从 I/O、流程单元和 NL 描述推断，且 C3 缺少真正 cross-cutting forced recovery。

<details><summary><b>📝 扩充 NL（205 词 / 17 markers / 17 provenance entries）</b></summary>

**Expanded NL**:

> The PLC supervises a boiler-wastewater treatment chain made up of equalization, coagulation, flocculation, clarifier, and final-tank units, with sensors and actuators added so the process can be controlled automatically and monitored through an HMI interface [E1][E2][E3]. Its PLC I/O design contains 16 inputs and 18 outputs, including pH and conductivity sensing, water-level sensing, motorized valves, pump and mixer relays, and blowdown or outlet solenoid valves [E4][E5][E6][E7][E8]. The controller has two operating methods: in auto mode, parameter setting and activation of supporting devices are performed by the program sequence using sensor, selector-switch, and pushbutton inputs, so the plant can run without operator manual input [E9]. In manual mode, the operator activates supporting devices and sets parameters manually, and the HMI main panel lets authorized users start or stop the system, choose mode, adjust motorized-valve openings, view active pump or solenoid-valve actuators, read analog values, and activate pumps or manual processes [E10][E11][E14]. The closed-loop return logic is centered on final-tank conductivity: the PLC converts conductivity readings to TDS, uses sensor readings to determine motorized control-valve opening and bypass-solenoid use, treats pH 6-9 and discharged-water TDS below 1500 ppm as quality targets, and sends water above 1500 ppm back to the equalization unit through the added pipeline [E12][E13][E15][E16][E17].

**Axis coverage**:

- **C1**: 原文只支持 Auto/Manual 顶层操作模式和处理链单元边界，expanded_nl 在 [E1][E9][E10] 暴露了弱 mode/process boundary；原文未给 mode 内默认初始子状态，因此未写强 C1 默认进入钩子。
- **C2**: C2 钩子在 [E12][E13][E15][E16][E17]：变量包括 conductivity/TDS 与 pH，阈值包括 pH 6-9、TDS <1500 ppm、TDS >1500 ppm，并有 motorized-valve/bypass-solenoid 决策。
- **C3**: 原文不支持 any-state emergency、forced fault、watchdog 或 each-cycle invariant，expanded_nl 未提供 C3 钩子。
- **C4**: C4 钩子在 [E2][E5][E6][E7][E8][E11][E13][E14]：原文支持 pH/conductivity/water-level sensors、motorized valves、pump/mixer relays、solenoid valves 与 HMI 读写/显示。

**Provenance** (17 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.2 Work Process Flowchart \| paper_content.txt 行166-172 | Wastewater treatment units consist of equalization units, coagulation units, flocculation units, … | treatment chain units |
| [E2] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行26-29 | control and monitor the process ... automatically ... adding sensors and actuators | automatic control and added sensors/actuators |
| [E3] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行29-31 | Display interface created using HMI (Human Machine Interface) software. | HMI interface monitoring |
| [E4] | STM §1 摘录 B \| paper.pdf p.4 Design of Control Devices \| paper_content.txt 行281-286 | The system uses 16 inputs and 18 outputs | PLC I/O count |
| [E5] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行301-304 | pH Sensor Conductivity Sensor | pH and conductivity sensing |
| [E6] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行321-324 | High Equalization Water Level Sensor | water-level sensing |
| [E7] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行302-303 | Motorized Valve PAC | motorized valves |
| [E8] | STM §1 摘录 B \| paper.pdf p.5 Figure 4 \| paper_content.txt 行305-317 | Intake Pump Relay Agitator Relay PAC Pump Relay Polymer Pump Relay Flocculation Unit Mixer Relay … | pump relays, mixer relays, and solenoid valves |
| [E9] | STM §1 摘录 D \| paper.pdf p.5-6 Flow chart \| paper_content.txt 行390-397 | auto mode ... sensors, selector switches, pushbuttons ... without manual input performed by the o… | auto-mode program sequence and no operator manual input |
| [E10] | STM §1 摘录 D \| paper.pdf p.5-6 Flow chart \| paper_content.txt 行397-407 | manual mode, the operator must activate the system supporting devices manually and set its parame… | manual-mode operator activation and parameter setting |
| [E11] | STM §1 摘录 D \| paper.pdf p.6 Interface Design \| paper_content.txt 行438-445 | main control tab that functions to activate and stop the system and choose the system mode | HMI start/stop and mode choice |
| [E12] | STM §1 摘录 D \| paper.pdf p.7 Quality of water \| paper_content.txt 行514-518 | conductivity values that are read can be converted to TDS values | conductivity-to-TDS conversion |
| [E13] | STM §1 摘录 D \| paper.pdf p.7 Quality of water \| paper_content.txt 行521-524 | determine the size of the motorized control valve opening and whether the solenoid valve bypass i… | sensor-based motorized-valve opening and bypass-solenoid use |
| [E14] | STM §1 摘录 D \| paper.pdf p.6 Interface Design \| paper_content.txt 行445-452 | actuator tab to display the actuator (pump, solenoid valve) ... analog value tab ... manual activ… | active actuator display, analog values, and manual pump/process activation |
| [E15] | STM §1 摘录 D \| paper.pdf p.7 Quality of water \| paper_content.txt 行531-534 | the value of process water is at pH 6-9 | pH 6-9 quality target |
| [E16] | STM §1 摘录 D \| paper.pdf p.7 Quality of water \| paper_content.txt 行535-536 | water discharged into the water channel < 1500 ppm | discharged-water TDS below 1500 ppm |
| [E17] | STM §1 摘录 D \| paper.pdf p.7 Quality of water \| paper_content.txt 行536-537 | If water is > 1500 ppm, it will flow back to the equalization unit. | return loop for water above 1500 ppm |

**Intentional omissions**: 没有加入阀门编号、泵编号、紧急停机、forced fault、任意状态强制跳转、watchdog/each-cycle 逻辑或 Auto 模式默认初始 phase，因为 paper.pdf 与 STM §1 都未提供这些事实；也没有把 pH 条件写成独立 discharge guard，只保留为质量目标。

</details>


##### 2. `[167]` 🌡️ Flow-and-Water-Quality Feedback Dosing Controller (EFSM-interlock)

- **领域**: 🌡️
- **论文**: paper #566 [`automatic-dosing-system-based-on-reclaimed-water-treatment`](../../../sources/automatic-dosing-system-based-on-reclaimed-water-treatment/STM.md)
- **是什么**: 这是再生水处理设备中的 PLC 自动加药控制器，根据进水流量、在线出水水质、液位和加药流量反馈计算投加量，并驱动电动阀、计量泵、变频器、搅拌器等完成稀释、阀门切换、配药和闭环投加。
- **scale**: states=8 / events=11 / vars=9 / trans=13
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文写明 The system has two modes: local control and PLC control，且 local control is the most priority control mode，同时可选择 flow proportional dosing 或 PID closed-loop control，但未见真正层次化 composite state。
- **C2 数值守卫**: 🟢 — 原文给出 Q = Q1 × P1 × P2 × P3，并定义 P2 为 actual detection value / set value、P3 为 empirical value / theoretical value，还要求比较 dosing flowmeter actual value 与 dosing set value 后经 PID 调频。
- **C3 forced fault**: 🟠 — 原文只写到 transmission equipment 有 fault 状态信号、flowmeter failure alarm、frequency converter protection functions，未明确 any mode/from any state 的统一故障恢复迁移。
- **C4 硬件解耦**: 🟢 — 原文明确 full-automatic control of dilution, valve switching and dosing of metering pump，并描述 electric ball valve、metering pump、frequency converter、agitator、ultrasonic level gauge 等现场硬件。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：它有清晰的多变量乘法/比值控制公式、PID 闭环调节和真实水处理硬件执行链，适合检验数值 guard 反馈与 abstract action 硬件解耦收益。NL 描述独立清楚，是典型工业过程控制对象。
- **风险**: 结构层次较浅，故障语义偏设备保护/报警而不是全局 forced recovery，C1/C3 的 grounding 收益有限。

<details><summary><b>📝 扩充 NL（270 词 / 22 markers / 22 provenance entries）</b></summary>

**Expanded NL**:

> The controller is an automatic dosing system for reclaimed-water treatment that replaces manual regulation [E1] by combining feedforward control, feedback control, dosing-ratio correction, PLC communication, and a control model [E2]. It is organized around dosing, dissolution/dilution, and regulation/control subsystems [E3], and the PLC controls the whole dilution and dosing process [E4] while parameters are adjusted according to wastewater flow and water quality [E5]. The system has local field-button control and PLC control, with local control as the priority mode [E6], while PLC control performs unattended dilution, valve switching, and metering-pump dosing [E7]. In PLC operation, the upper computer calculates the reagent dosing set value from front-end sewage flow and online water-quality data [E8], uses a correction dosing coefficient [E9], and sends the target through the PLC to the dosing diaphragm pump [E10]. The setpoint Q in m3/h is computed as Q1 x P1 x P2 x P3 [E11], with Q1 as inflow flow, P1 as dosing coefficient, P2 as water-quality feedback coefficient, and P3 as correction coefficient [E12]. In closed loop, the dosing-pipeline flowmeter returns the actual value in real time [E13]; the controller compares it with the set dosing value [E14] and drives the pump frequency converter through PID [E15]. The hardware path opens an electric medicine valve before delivery to the metering pump [E16], uses an electric valve to control water inlet time [E17], uses electric valves for start/stop control [E18], and uses ultrasonic liquid-level feedback to fill the tank [E19] and close the medicine inlet valve [E20]. If dosing stops, automatic flushing starts [E21]; if protected-system pressure exceeds set pressure, the safety valve opens to discharge [E22].

**Axis coverage**:

- **C1**: 原文只支持 local control / PLC control 两种控制模式与系统组成，不支持复合状态、子模式或默认进入子状态；[E6][E7] 仅保留模式事实，未提供 C1 层次钩子。
- **C2**: C2 钩子位于 [E11][E12][E13][E14][E22]：Q、Q1、P1、P2、P3、实际/设定流量比较，以及 pressure exceeds set pressure 的自然语言阈值守卫；未伪造具体数值。
- **C3**: 原文不支持任意状态 forced transition，也没有 each-cycle aspect；[E21][E22] 只是本地异常/设备保护行为，因此不写 C3 forced 钩子。
- **C4**: C4 钩子位于 [E10][E13][E15][E16][E17][E18][E19][E20][E22]：dosing diaphragm pump、flowmeter、frequency converter、electric medicine valve、electric valve、ultrasonic level gauge、safety valve 等物理 I/O 与执行器。

**Provenance** (22 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 7-15 | The automatic dosing system can replace the manual regulation mode. | automatic dosing system replaces manual regulation |
| [E2] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 12-15 | Fully combine feedforward control, feedback control, correction of dosing ratio and other control… | feedforward, feedback, dosing-ratio correction, PLC communication, and contro… |
| [E3] | STM §1 摘录 B \| paper.pdf p.2 §3.1 \| paper_content.txt 行 62-68 | The dosing system is mainly composed of dosing system, dissolution preparation and dilution syste… | subsystems: dosing, dissolution/dilution, regulation/control |
| [E4] | STM §1 摘录 B \| paper.pdf p.2 §3.1 \| paper_content.txt 行 74-75 | The automatic control of the whole process of dilution and dosing of the system reagent solution … | PLC controls the whole dilution and dosing process |
| [E5] | STM §1 摘录 B \| paper.pdf p.2 §3.1 \| paper_content.txt 行 75-76 | parameters can be automatically adjusted according to the waste water flow and water quality. | parameter adjustment depends on wastewater flow and water quality |
| [E6] | STM §1 摘录 D \| paper.pdf p.7 §4.3.1 \| paper_content.txt 行 275-277 | The system has two modes: local control (field button) and PLC control. Local control is the most… | local field-button control, PLC control, and local priority |
| [E7] | STM §1 摘录 D \| paper.pdf p.7 §4.3.1 \| paper_content.txt 行 278-280 | full-automatic control of dilution, valve switching and dosing of metering pump according to the … | PLC mode performs dilution, valve switching, and metering-pump dosing |
| [E8] | STM §1 摘录 B \| paper.pdf p.2-3 §3.2 \| paper_content.txt 行 82-88 | calculates the set value of reagent dosing by collecting and controlling the front-end sewage flo… | upper computer calculates set value from sewage flow and online water-quality… |
| [E9] | STM §1 摘录 B \| paper.pdf p.3 §3.2 \| paper_content.txt 行 88 | automatically or manually setting the correction dosing coefficient | correction dosing coefficient |
| [E10] | STM §1 摘录 B \| paper.pdf p.3 §3.2 \| paper_content.txt 行 88-89 | then feeds back to the dosing diaphragm pump through the PLC system. | target is sent through PLC to dosing diaphragm pump |
| [E11] | STM §1 摘录 C \| paper.pdf p.3 §3.2.4 \| paper_content.txt 行 121-124 | Q=Q1 × P1 × P2 × P3 | setpoint Q formula |
| [E12] | STM §1 摘录 C \| paper.pdf p.3 §3.2.4 \| paper_content.txt 行 125-127 | Q1 represents inflow flow (KM3 / h), P1 represents dosing amount and dosing coefficient, P2 repre… | definitions of Q1, P1, P2, and P3 |
| [E13] | STM §1 摘录 B \| paper.pdf p.3 §3.2 \| paper_content.txt 行 90-92 | The detection value of the flowmeter in the dosing pipeline is fed back to the PLC system in real… | dosing-pipeline flowmeter returns actual value in real time |
| [E14] | STM §1 摘录 B \| paper.pdf p.3 §3.2 \| paper_content.txt 行 92-93 | The central control system compares the actual value of the dosing flowmeter with the dosing set … | controller compares actual dosing flow with set value |
| [E15] | STM §1 摘录 B \| paper.pdf p.3 §3.2 \| paper_content.txt 行 93-94 | outputs the signal to the dosing pump frequency converter through the PID control system to adjus… | PID drives pump frequency converter |
| [E16] | paper.pdf p.4 §4.1 \| paper_content.txt 行 138-140 | Give a signal that the electric medicine valve is opened in place, open the valve and deliver it … | electric medicine valve opens before delivery to metering pump |
| [E17] | paper.pdf p.4 §4.1 \| paper_content.txt 行 140-141 | The water inlet pipe equipped with reagent solution is equipped with electric valve to control th… | electric valve controls water inlet time |
| [E18] | STM §1 摘录 D \| paper.pdf p.7 §4.3 \| paper_content.txt 行 260-264 | Then dilute with the designed water volume, and control the start and stop with electric valve. | electric valves control start/stop |
| [E19] | paper.pdf p.6 §4.2 \| paper_content.txt 行 219-225 | The reagent solution is sent to the liquid storage tank according to the requirements through the… | ultrasonic liquid-level feedback fills the tank |
| [E20] | paper.pdf p.6 §4.2 \| paper_content.txt 行 221-222 | a close in place signal is given to the electric ball valve to close the medicine inlet valve. | medicine inlet valve is closed by close-in-place signal |
| [E21] | paper.pdf p.4 §4.1 \| paper_content.txt 行 144-146 | If the dosing is stopped, it is necessary to start the automatic flushing procedure. | dosing stop triggers automatic flushing |
| [E22] | paper.pdf p.5 §4.1.1 \| paper_content.txt 行 169-172 | When the pressure of the protected system exceeds the set pressure, the safety valve opens to dis… | pressure guard opens safety valve |

**Intentional omissions**: 未写 valve 编号、传感器型号、具体压力阈值、默认子状态、全局急停或 forced fault，因为 paper.pdf 与 STM §1 均未提供支撑。也没有把变频器故障保护清单扩展成状态机恢复路径，因为原文只给设备保护功能，不给控制迁移语义。

</details>


##### 3. `[151]` 🌡️ Flow-Interlocked Liquid Transfer and Pause-Recovery Supervisor (EFSM-interlock)

- **领域**: 🌡️
- **论文**: paper #518 [`liquid-level-monitoring-flow-liquid-distribution-plc-scada`](../../../sources/liquid-level-monitoring-flow-liquid-distribution-plc-scada/STM.md)
- **是什么**: 这是一个 PLC/SCADA 液体转运监督控制器：操作员选择目标罐并输入设定转运量后，系统根据液位、管线流量、阀门反馈和泵状态控制吸入/分配/目标电磁阀与泵。典型流程是预检联锁通过后开阀启泵，异常时暂停并关阀停泵，故障排除后重新 Start，流量累计达到设定量后完成。
- **scale**: states=7 / events=8 / vars=9 / trans=13
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文有 Auto mode、confirmed、dispensing、paused、completed 等阶段，并写到“First keep the process in auto mode”和“process will be paused”，但没有真正层次化 composite state。
- **C2 数值守卫**: 🟢 — 原文明确用数值量作守卫：设定转运量、源罐液位可用量、管线流量和累计流量，例如“Entered set quantity ... should available in the selected source Tank”和“flow sensor totalizes the flow rate equivalent to the given set quantity”。
- **C3 forced fault**: 🟠 — 异常处理只限定在转运中，原文写“If any one of the following deviation occurs in the middle of the process then the process will be paused”，不是 any mode/from any state 的 cross-cutting fault。
- **C4 硬件解耦**: 🟢 — 原文列出明确硬件动作：“Destination, transferring, suction solenoid valves are opened followed by pump starts running”，完成或暂停时阀门关闭且泵停止。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：有典型工业 PLC/SCADA 对象、清晰的数值累计/阈值联锁，以及多路阀泵硬件动作，适合验证 EFSM 数值守卫和 abstract action 解耦收益。NL 流程也较完整，能形成可生成、可仿真、可反馈的 T0 case。
- **风险**: C1/C3 结构不强，暂停恢复是局部 dispensing 阶段逻辑，且与其他液体转运/阀泵联锁样本可能存在同构风险。

<details><summary><b>📝 扩充 NL（268 词 / 15 markers / 15 provenance entries）</b></summary>

**Expanded NL**:

> The supervisor starts a transfer from the SCADA screen in Auto mode: the operator selects the Transferring operation [E1], chooses the destination and enters the requested quantity [E2], confirms it, and clicks Start only after the interlocks are satisfied [E3]. Auto-mode operation is described as a sequence in which SCADA command selection and confirmation occur before the Start-triggered dispensing operation [E1][E2][E3]. When active transfer starts, the controller opens the destination, dispensing, and suction solenoid valves and then starts the pump to move liquid or solvent from the source tank to the selected destination [E4]. The transfer may continue only under a compound run condition: source-tank level is decreasing AND the line flow sensor senses liquid or solvent flow [E5]. If that condition is not maintained, the operation pauses automatically by closing all opened valves and stopping the pump [E6]. The same pause response applies to mid-process deviations with no change in storage-tank level and line flow [E7], pump dry run, trip, or failure [E8], missing dispensing-valve open feedback to the PLC [E9], a field override that opens another valve [E10], or low storage-tank level or level-switch indication [E11]. After an interlock is enabled, SCADA displays it and the operator must correct or troubleshoot the issue [E12], then click Start again to resume the process [E13]. While liquid is pumping, the flow sensor totalizes flow rate against the given set quantity; when the totalized flow is equivalent to that set quantity, the operation completes automatically, the pump turns off, and the corresponding valves close [E14]. A SCADA Stop control is also provided to stop transferring operations when necessary [E15].

**Axis coverage**:

- **C1**: 弱暴露：expanded_nl 只根据原文 Auto mode、Transferring、Confirm、Start 的顺序写出 Auto-mode 内的命令选择到 dispensing 序列 [E1][E2][E3]；原文不支持明确层次结构或默认子状态。
- **C2**: C2 钩子在源液位下降 AND line flow sensor senses flow 的复合守卫 [E5]，以及 flow totalizes flow rate equivalent to given set quantity 的变量阈值 [E14]。
- **C3**: C3 弱钩子在 mid-process deviation 触发统一 pause response [E7][E8][E9][E10][E11] 和 SCADA Stop [E15]；原文不支持 any-state forced transition 或 forced fault path。
- **C4**: C4 钩子在 destination/dispensing/suction solenoid valves、pump、flow sensor、SCADA 等物理 I/O，以及开阀启泵、关阀停泵动作 [E4][E6][E14]。

**Provenance** (15 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.3 Algorithm \| paper_content.txt 行 218-221 | Click on Auto button from SCADA screen to keep the system in Auto mode. Then select the Transferr… | Auto mode and selection of the Transferring operation from SCADA. |
| [E2] | STM §1 摘录 A \| paper.pdf p.3 Algorithm \| paper_content.txt 行 224-227 | Select the destination where liquid/solvent is to b transferred. Enter the set quantity | Destination selection and requested transfer quantity. |
| [E3] | STM §1 摘录 A \| paper.pdf p.3 Algorithm \| paper_content.txt 行 228-231 | If all the interlocks satisfied then operations will confirmed otherwise doesn’t confirmed. If op… | Confirmation depends on satisfied interlocks, and Start follows confirmed ope… |
| [E4] | STM §1 摘录 A \| paper.pdf p.3 Algorithm \| paper_content.txt 行 232-234 | Observe destination, dispensing, suction solenoid valves are opened followed by pump starts runni… | Valve opening, pump start, and transfer from source tank to destination. |
| [E5] | STM §1 摘录 B \| paper.pdf p.3 Algorithm \| paper_content.txt 行 235-237 | If Level in source tank decreases and flow sensor in line senses the liquid/solvent flow then ope… | Compound run condition using source-tank level decrease and line flow sensing. |
| [E6] | STM §1 摘录 B \| paper.pdf p.3 Algorithm \| paper_content.txt 行 237-239 | operation will be paused automatically. That means all the opened valves are closed and pump stops. | Automatic pause effect closes opened valves and stops the pump. |
| [E7] | STM §1 摘录 C \| paper.pdf p.7 Interlock enabled then pause screen \| paper_content.txt 行 446-448 | If there is no change in the storage tank level and if there is no change in the line flow. | Mid-process pause deviation for unchanged storage-tank level and line flow. |
| [E8] | STM §1 摘录 C \| paper.pdf p.8 Interlock enabled then pause screen \| paper_content.txt 行 456 | If pump dry run or tripped or failed. | Pause deviation for pump dry run, trip, or failure. |
| [E9] | STM §1 摘录 C \| paper.pdf p.8 Interlock enabled then pause screen \| paper_content.txt 行 457-458 | If any one of the dispensing valves open feedback is not received to PLC or valve fails. | Pause deviation for missing dispensing-valve open feedback to PLC. |
| [E10] | STM §1 摘录 C \| paper.pdf p.8 Interlock enabled then pause screen \| paper_content.txt 行 458-459 | During dispensing of the solvent if any one of other valve is opened manually from field (override). | Pause deviation for manual field override opening another valve. |
| [E11] | STM §1 摘录 C \| paper.pdf p.8 Interlock enabled then pause screen \| paper_content.txt 行 460 | If liquid level/Level switch in the storage tank goes low. | Pause deviation for low storage-tank level or level-switch indication. |
| [E12] | STM §1 摘录 C \| paper.pdf p.8 Interlock enabled then pause screen \| paper_content.txt 行 463-465 | The enabled interlock displayed on SCADA operating screen. It must be corrected or instrument nee… | SCADA displays the enabled interlock and requires correction or troubleshooting. |
| [E13] | STM §1 摘录 C \| paper.pdf p.8 Interlock enabled then pause screen \| paper_content.txt 行 465-466 | Then user comes back and process start again by click on start button. | Recovery resumes by clicking Start again. |
| [E14] | STM §1 摘录 B/C \| paper.pdf p.8 Liquid dispensing completed screen result \| paper_content.txt 行 467-470 | when flow sensor totalizes the flow rate equivalent to the given set quantity then operation Comp… | Completion guard using totalized flow versus set quantity, plus pump-off and … |
| [E15] | paper.pdf p.8 Liquid dispensing completed screen result \| paper_content.txt 行 471-472 | Stop is provided in SCADA screens, which stops transferring operations if necessarily. | SCADA Stop control for stopping transferring operations. |

**Intentional omissions**: 没有加入阀门编号、泵编号、具体容量数字、超时阈值、传感器型号或 any-state emergency forced path，因为 STM §1 和相关 PDF 页没有给出这些细节。没有把 flow transmitter 的 4-20 mA/0-200 LPM 标定写进 expanded_nl，因为它是通用监测块说明，不是该转运流程的必要 guard。

</details>


##### 4. `[215]` 🏭 Automatic Feeding, Tool Selection, Alignment, and Cutting (EFSM-interlock)

- **领域**: 🏭
- **论文**: paper #732 [`control-system-automatic-bamboo-splitting-equipment-plc`](../../../sources/control-system-automatic-bamboo-splitting-equipment-plc/STM.md)
- **是什么**: 该 case 控制自动破竹机的 PLC 送料、刀盘选刀、竹筒对中夹持与切割流程；系统用传感器测量竹筒接触点和夹持压力，驱动输送带、电机、刀盘和夹持机构完成从送料到切割的顺序加工。
- **scale**: states=8 / events=10 / vars=8 / trans=11
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文写系统分为 “bamboo tube feeding, blade choice, bamboo centering, bamboo cutting”，并有 “automatic and manual state switch”，有阶段/mode 切换但未见真正层次嵌套。
- **C2 数值守卫**: 🟢 — 原文写 4 个接触点的空间位置由传感器获得，经 fitting 得到直径并 “compared with 4 cutter diameter”，且对中后 “pressure sensor ... reaches the threshold” 才切割。
- **C3 forced fault**: 🟠 — 原文只在送料系统处说可实现 “fault alarm, status indication”，没有写 any mode/from any state 的全局 Error/Abort/Reset 恢复语义。
- **C4 硬件解耦**: 🟢 — 原文列出 conveyor belt、alternating current servo motor、motor、no finger cylinder、finger cylinder、relays、inverter 等硬件，并写 “Using PLC control motor speed and pause”。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：它同时包含几何拟合、直径比较、压力阈值等数值守卫，以及多类真实工业执行器。NL 流程清楚，控制对象独立，适合作为 pyfcstm 数值反馈和 abstract handler grounding 的 T0 样本。
- **风险**: 流程总体偏顺序型，自动/手动切换和 fault alarm 没有展开为跨状态恢复逻辑，C3 价值较弱。

<details><summary><b>📝 扩充 NL（263 词 / 16 markers / 16 provenance entries）</b></summary>

**Expanded NL**:

> The control system structures the automatic bamboo-splitting process as a sequence of bamboo-tube feeding, blade choice, bamboo centering, and bamboo cutting [E1]. The machine specification includes four tool dishes and 12 to 15 blades on the tool plate [E2], a processable bamboo diameter range of 60 to 120 mm [E3], and a gripping device for bamboo of 2 to 2.5 kg and 1500 to 2500 mm length [E4]. During feeding, a ladder-type conveyor sends bamboo to the cutting machine while the PLC controls motor speed and pause [E5]. The conveyor adapts speed according to the distance between two articles to prevent collisions [E6], supports fault alarm and status indication [E7], and can switch between automatic and manual states for maintenance [E8]. For blade selection, the controller replaces visual diameter estimation and manual tool-dish turning [E9] with automatic bamboo-diameter measurement and tool choice [E10]. The grasp tool obtains the spatial positions of four bamboo contact points through sensors [E11], then fits a circle for the irregular bamboo cross-section, uses the fitted diameter as a variable, and compares it with four cutter diameters on the cutter head to choose a suitable cutting tool [E12]. After the fitting circle is available, the clamping device performs automatic clamping under constant-speed movement [E13], and the grab tool together with the cutting-table position sensor aligns the bamboo center and blade center [E14]. The cut is permitted only after alignment is finished and the grab-tool pressure sensor reaches its threshold [E15]; then the cutting table and grasping tool feed the bamboo into the blade and automatic cutting is finished [E16].

**Axis coverage**:

- **C1**: 原文仅支持 bamboo feeding、blade choice、centering、cutting 四个顺序阶段，[E1] 暴露了阶段边界；原文无层次 mode 或进入复合 mode 的默认子状态，因此未提供严格 C1 钩子。
- **C2**: C2 钩子位于 [E2]-[E4]、[E11]-[E15]：包含 60-120 mm、2-2.5 kg、1500-2500 mm、4 contact points、4 cutter diameters 和 pressure sensor threshold，但原文未给压力阈值数值。
- **C3**: 原文只支持送料系统的 fault alarm、status indication 和 automatic/manual maintenance switch [E7][E8]，不支持 any-state emergency、forced fault transition 或明确恢复路径，因此无 C3 forced-transition 钩子。
- **C4**: C4 钩子位于 [E5]、[E11]、[E14]-[E16]：包含 ladder conveyor、PLC motor speed/pause、sensors、grab tool、position sensor、pressure sensor、cutting table 和 grasping tool 等物理 I/O 与执行部件。

**Provenance** (16 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.3 §2.1 \| paper_content.txt 行 95-99 | The control system is mainly divided into the following several parts: bamboo tube feeding, blade… | control process phases: feeding, blade choice, centering, cutting |
| [E2] | STM §1 摘录 A \| paper.pdf p.3 §2.1 \| paper_content.txt 行 105-106 | can be mounted to the rest of 4 tool dish, tool plate can be installed on the number of the blade… | four tool dishes and 12 to 15 blades |
| [E3] | STM §1 摘录 A \| paper.pdf p.3 §2.1 \| paper_content.txt 行 106-107 | Bamboo diameter that can be processed in the range of 60 ~ 120 mm. | processable bamboo diameter range of 60 to 120 mm |
| [E4] | STM §1 摘录 A \| paper.pdf p.3 §2.1 \| paper_content.txt 行 107-108 | The gripping device can grab the bamboo for 2 ~ 2.5 kg, the length of 1500 ~ 2500 mm | gripping device capacity and bamboo length range |
| [E5] | STM §1 摘录 B \| paper.pdf p.3-4 §2.2 \| paper_content.txt 行 109-112 | Bamboo tube feeding system performed by ladder type conveyor belt. Using PLC control motor speed … | ladder conveyor, PLC motor speed and pause control, feeding to cutting machine |
| [E6] | STM §1 摘录 B \| paper.pdf p.4 §2.2 \| paper_content.txt 行 119-120 | speed automatically according to the distance between the two items can transform to prevent coll… | speed adaptation based on inter-article distance to prevent collisions |
| [E7] | STM §1 摘录 B \| paper.pdf p.4 §2.2 \| paper_content.txt 行 120-122 | can realize fault alarm, status indication, the conveyor belt load soft start, etc. | fault alarm and status indication |
| [E8] | STM §1 摘录 B \| paper.pdf p.4 §2.2 \| paper_content.txt 行 121-122 | to realize automatic and manual state switch, convenient maintenance. | automatic/manual state switch for maintenance |
| [E9] | STM §1 摘录 C \| paper.pdf p.4 §2.3 \| paper_content.txt 行 133-136 | estimate its diameter by staff visual bamboo, artificially turn the tool dish, then cut bamboo. | manual visual diameter estimation and manual tool-dish turning being replaced |
| [E10] | STM §1 摘录 C \| paper.pdf p.4 §2.3 \| paper_content.txt 行 137-138 | This system adopted the control mode of automatic measurement of bamboo diameter and the choice o… | automatic bamboo-diameter measurement and tool choice |
| [E11] | STM §1 摘录 C \| paper.pdf p.4 §2.3 \| paper_content.txt 行 145-147 | there are 4 contact points between the bamboo grasp tool and bamboo, and the spatial position of … | four contact points and sensor-based spatial positions |
| [E12] | STM §1 摘录 C \| paper.pdf p.4 §2.3 \| paper_content.txt 行 147-149 | get the fitting the diameter of the circle, as the parameter compared with 4 cutter diameter of c… | fitted diameter compared with four cutter diameters to choose the suitable tool |
| [E13] | STM §1 摘录 D \| paper.pdf p.6 §2.4 \| paper_content.txt 行 212-214 | with constant speed movement principle of clamping device can realize automatic clamping action. | automatic clamping under constant-speed movement |
| [E14] | STM §1 摘录 D \| paper.pdf p.6 §2.4 \| paper_content.txt 行 214-216 | Using the grab tool and the position sensor of the cutting table, the center of the bamboo and th… | grab tool and cutting-table position sensor align bamboo and blade centers |
| [E15] | STM §1 摘录 D \| paper.pdf p.6 §2.4 \| paper_content.txt 行 215-216 | After the alignment is finished, the pressure sensor of the grab tool reaches the threshold. | cut permission guard based on completed alignment and pressure threshold |
| [E16] | STM §1 摘录 D \| paper.pdf p.6 §2.4 \| paper_content.txt 行 216-218 | the bamboo is fed into the blade by the cutting table and the grasping tool, and the automatic cu… | cutting table and grasping tool feed bamboo into blade and complete automatic… |

**Intentional omissions**: 没有加入 emergency stop、forced fault path、恢复流程、传感器型号、valve 编号或层次 mode 默认入口，因为原文没有这些支撑。原文虽提到 fault alarm 和自动/手动切换，但没有说明报警触发后的状态跳转或恢复逻辑。

</details>


##### 5. `[052]` 🌡️ Four-Scenario Micro-Grid EMS with SOC-Governed Battery Switching (EFSM-interlock)

- **领域**: 🌡️
- **论文**: paper #268 [`energy-management-strategy-hybrid-micro-grid-renewable-energy`](../../../sources/energy-management-strategy-hybrid-micro-grid-renewable-energy/STM.md)
- **是什么**: 这是一个混合微电网 EMS，用发电功率 PG、负载 PL、电池 SOC 和 utility grid availability 判断 PV/风电、电池、utility grid、柴油机之间的供能切换。典型流程是发电充足时供负载并给电池充电，SOC 满后送电网，发电不足时电池放电，SOC 到 20% 后切到电网或柴油机供电。
- **scale**: states=7 / events=7 / vars=4 / trans=10
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文写 EMS 供电逻辑“through four scenarios”，并用 Stateflow ON/OFF 表示各输出；有场景/模式切换，但未见层次化 composite、init/pseudo 或嵌套退出语义。
- **C2 数值守卫**: 🟢 — 原文给出多个数值 guard，如 `SOCmin < SOCbatt < SOCmax = 20% < SOCbatt < 100%`、`PG < PL = Battery Discharging`、`PPV + Pwind + Pbatt < PL`，并规定电池仅在可再生发电 `≥ 200 kW` 时充电。
- **C3 forced fault**: 🟠 — 原文只有局部退化处理：`when the utility grid was not available, then the diesel generator was switched on`，未见 any mode/from any state/all phases 的 cross-cutting fault 语义。
- **C4 硬件解耦**: 🟢 — Appendix action table 明确列出 `AC Load = ON`、`Battery = ON/OFF`、`Utility grid = ON`、`Diesel generator = ON`，对应负载供电、电池连接/断开、电网连接和柴油机开关等硬件出口。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：数值守卫密集，且直接驱动物理能源设备 ON/OFF，适合检验 semantic/sim feedback 对 EFSM interlock 的修正收益。NL 描述清晰，工业控制对象典型，能作为 T0 中较强的微电网能量管理样本。
- **风险**: C1 只有场景级模式切换而非真正层次状态机，C3 也只是 utility-grid unavailable 的局部 fallback，不适合作为 forced fault recovery 强样本。

<details><summary><b>📝 扩充 NL（248 词 / 9 markers / 9 provenance entries）</b></summary>

**Expanded NL**:

> The hybrid micro-grid energy management system controls energy flow between the hybrid micro-grid, the directly connected load, and the load connected to the utility grid [E1], and it also controls battery charging and discharging so that battery SOC remains within 20% to 100% [E2]. The EMS flow chart starts from measurements of PG, PL, SOC, fuel and electricity prices [E3], then supplies the load through four scenario branches using the battery, the diesel generator, and the utility grid [E4]. When PG equals PL, the load is supplied continuously by PV and wind power [E5]; when PG is greater than PL AND SOC is below 100%, the load remains supplied, the battery is connected for charging until maximum SOC, and excess production is supplied to the utility grid [E6]. When PG is less than PL AND the battery can supply the demand, the EMS checks the gap between renewable generation and load, measures SOC at the same time, and discharges the battery to support the load until SOC reaches the 20% minimum [E7]. At that minimum, the battery is disconnected; if the utility grid is available the controller connects it to supply the load, otherwise it switches on the diesel generator, and low-SOC charging is allowed only when available renewable power is at least 20% of total production [E8]. In the Stateflow implementation, components are represented by model blocks and the flow-chart output is logical: 1 means the system is operational ON and 0 means it is OFF [E9].

**Axis coverage**:

- **C1**: 原文只给出四个 scenario/flowchart 分支，没有层次化 mode、sub-mode 或进入 mode 的默认初始子状态；expanded_nl 未提供 C1 钩子。
- **C2**: C2 钩子在 [E5]-[E8]：使用 PG、PL、SOC、20%、100%、PG>PL、PG<PL、available power ≥20% of total production 等自然语言复合守卫。
- **C3**: 原文不支持 any-state emergency、forced fault、每 cycle aspect 或全局中止语义；expanded_nl 未提供 C3 钩子。
- **C4**: C4 钩子在 [E6]-[E9]：battery connected/disconnected、utility grid connected/supplies load、diesel generator switched on，以及 Stateflow ON/OFF 输出语义。

**Provenance** (9 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper_content.txt 行 19-21 | controls the flow of energy between the hybrid micro-grid system and the load connected directly … | EMS controls energy flow between the micro-grid, directly connected load, and… |
| [E2] | STM §1 摘录 A \| paper_content.txt 行 21-28 | control the charging and discharging of the battery ... (between 20 and 100%) | battery charging/discharging control and SOC admissible range of 20% to 100% |
| [E3] | paper.pdf p.8 Figure 4 | Measurements PG, PL, SoC, Fuel and Electricity prices | flow-chart measurement inputs PG, PL, SOC, fuel prices, and electricity prices |
| [E4] | STM §1 摘录 B \| paper_content.txt 行 279-288 | through four scenarios and with the help of the battery, a diesel generator, and the utility grid | four scenario branches and the three support resources |
| [E5] | paper.pdf p.9 §3 Case 1 \| paper_content.txt 行 290-292 | the load was continuously supplied by the power generated from wind power plant and PV power plan… | PG equals PL case supplies load from PV and wind power |
| [E6] | STM §1 摘录 B \| paper_content.txt 行 293-300, 315-316 | PG>PL=Charging ... maximum value, which was 100% ... excess of production was supplied to the uti… | PG > PL charging branch, SOC < 100% guard, battery charging, and grid export |
| [E7] | STM §1 摘录 B \| paper_content.txt 行 301-308, 317-322 | PG<PL= Battery Discharging ... measured the SOC of the battery at the same time ... reached the m… | PG < PL discharge branch, simultaneous SOC measurement, and discharge until m… |
| [E8] | STM §1 摘录 B/C \| paper_content.txt 行 309-333 \| paper.pdf p.8 Figure 4 | SOCbatt=20% = Battery Disconnected ... diesel generator was switched on ... available power was ≥… | 20% minimum disconnects battery, utility/diesel fallback, and low-SOC chargin… |
| [E9] | STM §1 摘录 C \| paper_content.txt 行 337-347 | represented by their respective model blocks ... either 0 or 1 ... operational (ON) ... OFF | Stateflow model blocks and logical ON/OFF output semantics |

**Intentional omissions**: 没有添加 sensor 型号、valve/contactor 编号、emergency stop、forced fault path 或层次化子模式，因为 paper.pdf 与 STM §1 都没有提供这些细节。也没有把 fuel/electricity prices扩展成优化策略，因为 Figure 4 只显示它们被测量，未给出基于价格的具体 guard。

</details>


##### 6. `[026]` 🩺 Preset gait-phase stimulation supervisor for hybrid FES-robot assistance (EFSM-interlock)

- **领域**: 🩺
- **论文**: paper #193 [`modular-neuroprosthesis-hybrid-fes-robot-assistance`](../../../sources/modular-neuroprosthesis-hybrid-fes-robot-assistance/STM.md)
- **是什么**: 该 case 是一个步态相位监督器，用髋/膝/踝电角度计和 WR 状态识别 support、pre-swing、swing-up、swing-down，并驱动不同肌群的 FES 刺激及膝部机器人辅助。典型流程是按 HC/HO/TO/K1 等步态事件循环切换相位，在 standard mode 或 cross mode 下把刺激映射到 GM、Q、TFL、H、GS、TA 等肌群。
- **scale**: states=4 / events=6 / vars=6 / trans=7
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文称该 FSM 有 `standard mode`，并集成 `cross mode` 变体，用 contralateral gait events 辅助 ipsilateral leg，但未给出真正层次化 composite/init/pseudo 语义。
- **C2 数值守卫**: 🟢 — 原文写明事件检测使用 hip、knee、ankle 的 angular trajectory 和 joint range of motion，并依赖 `adaptive thresholds` 将步态分成 support、pre-swing、swing-up、swing-down。
- **C3 forced fault**: 🟠 — 原文有 emergency button connected to each ES node，可在 any risk or need situation 下 immediately stop assistance，但未描述完整 ErrorHandler/recovery 状态机。
- **C4 硬件解耦**: 🟢 — 原文列出最多 4 个 stimulation nodes/多通道电极驱动 GM、Q、TFL、H、GS、TA，并在 hybrid 配置中还有 motorized knees 的 WR 辅助。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：它有真实连续角度信号、adaptive threshold 相位判定和多肌群/机器人硬件输出，能体现 semantic/sim feedback 与 abstract hardware handler 的收益。C1 也有 standard/cross mode 变体，虽非强层次结构，但足以制造一定模式混淆风险。
- **风险**: 原文未给出完整阈值公式，standard/cross 更像预设配置变体而非运行时层次切换，fault 也主要是 emergency stop 而非细化恢复逻辑。

<details><summary><b>📝 扩充 NL（223 词 / 14 markers / 14 provenance entries）</b></summary>

**Expanded NL**:

> The controller is a preset, one-sided finite-state-machine style supervisor for a modular neuroprosthesis adapted to gait, using electrogoniometer joint-angle data from the hip, knee, and ankle [E1][E2]. During operation, a gait-event detector uses adaptive thresholds on angular trajectories and range-of-motion data to segment gait into support, pre-swing, swing-up, and swing-down sub-phases [E3][E4]. The event boundaries are heel contact, heel off, toe off, and maximum knee flexion during swing, and the short sub-phases can be on the order of 10% of a 0.98-1.07 s adult gait cycle, about 100 ms [E5][E6]. In standard mode, the supervisor assists the ipsilateral musculature from ipsilateral hip, knee, and ankle angles, with configured stimulation-node channels mapped to identified muscle groups and delivered through transcutaneous electrodes [E7][E8][E9]. Its outputs are muscle-specific: gluteus maximus and quadriceps are stimulated in stance; hamstrings in swing-up; gastrocnemius in toe-off; and tibialis anterior and tensor fasciae latae in swing-related assistance [E10][E11]. When the corresponding event is detected, up-ramp stimulation is executed within the predefined assistance band, and when the end of stimulation is detected, down ramps are executed [E12]. A cross mode variant uses contralateral gait events to assist the ipsilateral leg; for gastrocnemius, contralateral heel contact starts assistance and ipsilateral toe-off stops it [E13]. An emergency button connected to each ES node can immediately stop assistance in any risk or need situation [E14].

**Axis coverage**:

- **C1**: expanded_nl 通过 [E4][E7][E13] 暴露 gait sub-phase 与 standard/cross mode 边界；但原文未给进入某 mode 默认从哪个 sub-phase 开始的初始化语义，因此未写 init pseudo 钩子。
- **C2**: expanded_nl 通过 [E3][E4][E6] 暴露 hip/knee/ankle 角度轨迹、ROM、自适应阈值以及 0.98-1.07 s/约 100 ms 时间量；原文未给具体数值阈值或复合 guard。
- **C3**: expanded_nl 通过 [E14] 仅暴露 emergency button 连接到各 ES node 并可立即停止 assistance 的横切安全语义；原文不支持 forced fault/recovery path。
- **C4**: expanded_nl 通过 [E1][E8][E9][E10][E11][E12] 暴露 electrogoniometers、stimulation-node channels、transcutaneous electrodes 与 ramped ES 输出这些硬件/effector 钩子。

**Provenance** (14 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | paper.pdf p.9 \| paper_content.txt 行 505-510 | up to 6 wireless electrogoniometers ... measure the angular motion | electrogoniometer joint-angle data |
| [E2] | STM §1 摘录 B \| paper.pdf p.9 \| paper_content.txt 行 567-570 | preset one-sided finite state machine type open-loop control algorithm | preset, one-sided finite-state-machine style supervisor |
| [E3] | paper.pdf p.9 \| paper_content.txt 行 539-542 | angular trajectory information of the hip, knee and ankle and the joint range of motion | angular trajectories and range-of-motion data |
| [E4] | STM §1 摘录 A \| paper.pdf p.9 \| paper_content.txt 行 552-553 | adaptive thresholds to segment the gait into support, pre-swing, swing-up and swing-down sub-phases | adaptive-threshold segmentation into the four gait sub-phases |
| [E5] | STM §1 摘录 A \| paper.pdf p.9 \| paper_content.txt 行 554-556 | heel contact, heel off, toe off and maximum knee flexion during swing | four event boundaries |
| [E6] | paper.pdf p.9 \| paper_content.txt 行 525-530 | up to 10% of the gait cycle ... between 0.98 and 1.07 s ... around 100 ms | short sub-phase timing context |
| [E7] | STM §1 摘录 B \| paper.pdf p.9 \| paper_content.txt 行 578-582 | standard mode ... ipsilaterally assists the musculature based on angular information | standard mode and ipsilateral angle-based assistance |
| [E8] | paper.pdf p.9 \| paper_content.txt 行 565-575 | muscle groups could be related to the configured channels | configured stimulation-node channels mapped to muscle groups |
| [E9] | paper.pdf p.6 \| paper_content.txt 行 380-382 | electrical stimulation directed to transcutaneous electrodes | delivery through transcutaneous electrodes |
| [E10] | STM §1 摘录 B \| paper.pdf p.9 \| paper_content.txt 行 582-594 | gluteus maximus and quadriceps are assisted during the stance phase ... Hamstrings ... swing-up .… | stance, swing-up, and toe-off muscle-output mapping |
| [E11] | STM §1 摘录 B \| paper.pdf p.9 \| paper_content.txt 行 585-597 | Tensor fasciae latae assistance was predefined during the swing ... tibialis anterior is assisted… | swing-related tensor fasciae latae and tibialis anterior assistance |
| [E12] | paper.pdf p.8 Fig.3 caption \| paper_content.txt 行 489-493 | down ramps are executed once the end of stimulation is detected ... up ramps ... corresponding ev… | event-triggered up ramps and end-triggered down ramps |
| [E13] | STM §1 摘录 C \| paper.pdf p.9-10 \| paper_content.txt 行 598-615 | contralateral heel contact was used to start the assistance and was stopped with ipsilateral toe-off | cross mode gastrocnemius start and stop events |
| [E14] | paper.pdf p.16 \| paper_content.txt 行 1107-1112 | connected to each ES node ... immediately stop the assistance ... any risk or need situation | emergency stop path |

**Intentional omissions**: 没有补写具体 adaptive threshold 数值、完整状态名枚举、阀门/泵/额外传感器编号或软件恢复路径；原文只支持 emergency stop，不支持 forced fault 或自动恢复流程。也没有把 knee-powered exoskeleton 的可配置参数扩写成本 case 的 guard，因为 STM §1 的目标是 NP gait-phase stimulation supervisor。

</details>


#### FSM-basic （3 条）

##### 1. `[124]` ⚙️ Excavation-Transport-Deposit Robot FSM (FSM-basic)

- **领域**: ⚙️
- **论文**: paper #449 [`robot-excavation-geometrically-cohesive-granular-media`](../../../sources/robot-excavation-geometrically-cohesive-granular-media/STM.md)
- **是什么**: 该 case 控制一个几何黏聚颗粒物挖掘机器人在蓝色挖掘区与红色沉积区之间循环作业，依靠 RGB 光源检测、ArduCAM 视觉、antenna 触觉和 jaws 状态切换行为。典型流程是挖掘并夹取 pellet，转向并运输到沉积区，搜索已有料堆或墙面后卸料，再转回挖掘区。
- **scale**: states=22 / events=18 / vars=8 / trans=31
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文 Fig.13 把 FSM 分成 Excavation、Turning、Visual Alignment to Deposit、Tactile Sensing & Deposition 四个阶段，并说明粗线表示这些阶段间的状态转移，但未给出真正层次化 init/exit 语义。
- **C2 数值守卫**: 🟢 — 原文第9页给出 RGB 颜色局部最大值、dark pixels below a threshold、bright regions/connected columns 等视觉判定，Fig.13 还含 Every 30 turns、Repeat 3x、close to wall 等计数/阈值 guard。
- **C3 forced fault**: 🟠 — Fig.13 只有 Forward motion obstructed 和 Obstructed jaws 这类局部异常分支，STM 摘录和 PDF 正文没有 from any state/any mode 的全局 Error、Abort 或 Reset 路径。
- **C4 硬件解耦**: 🟢 — 原文描述 five Dynamixel AX12A motors、front limbs/claws、rear whegs、jaw motor，Appendix A 还给出 antenna 与 ArduCAM 的独立电机，Fig.13 中对应 open/close jaws、whegs forward/reverse、sweep arm、antenna down 等硬件动作。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：真实机器人 FSM 同时含视觉/触觉/颜色/计数阈值 guard 与多个物理执行器动作，能很好体现 symbolic guard feedback 和 abstract action 硬件解耦收益。C1 也有多阶段切换，适合测试 agent 是否能把图中阶段边界和叶子状态关系建对。
- **风险**: 主要风险是 C3 较弱，没有明确 cross-cutting fault recovery；另外详细状态数依赖 Fig.13 图像标签，STM §2 NL 没有逐一列出全部叶子状态。

<details><summary><b>📝 扩充 NL（265 词 / 16 markers / 16 provenance entries）</b></summary>

**Expanded NL**:

> The robot controller is a microcontroller-executed FSM for a constructed arena, where blue and red lights mark excavation and deposition zones and behavior transitions are governed by fixed light sources and object-proximity information from onboard sensors [E1][E2][E3]. Its nominal cycle excavates material, transports it to the deposition site, locates an existing deposit, and returns to the excavation site to repeat the process [E4]. After successful excavation or deposition, turning begins and is stopped only when the RGB sensor detects a local maximum in the desired color value [E5]. Within excavation, interlocking jaws manipulate the material and are actuated by a single Dynamixel AX12A motor; initial material sensing and horizontal separation are followed by repeated vertical and horizontal tearing using the limbs and rear whegs [E6][E7][E8]. The transition out of excavation is not based on a fixed number of procedures; after backing away, material retention is indicated when the jaws cannot fully close and the Dynamixel encoder reports a jaw angle greater than about 30 degrees [E9][E10]. During transport toward deposit, the controller takes a 320x240 monochrome ArduCAM image and searches for a pile by counting dark pixels below a threshold in columns where two disconnected maximum-intensity bright regions are also present [E11][E12][E13]. For supported recovery behavior, the rangefinder can trigger reversing when an obstacle is in front, and the IMU can trigger a crutch maneuver when body pitching is impeded [E14][E15]. In the final deposit state, the robot searches with its antenna, deposits either at the existing pile or at the wall, and then begins turning toward the excavation site, completing one excavation-deposition cycle [E16].

**Axis coverage**:

- **C1**: 原文只支持平铺 FSM 流程和 excavation procedure 的内部动作顺序，没有显式层次 state/sub-mode 或进入复合 mode 的默认子状态；expanded_nl 未加入严格 C1 钩子。
- **C2**: C2 暴露在 [E5][E9][E10][E11][E12][E13]：RGB color value local maximum、jaw angle > ≈30°、320x240 image、dark pixels below threshold 与 bright regions maximum intensity，均用自然语言比较描述。
- **C3**: 原文不支持 any-state emergency、forced fault 或每 cycle aspect；expanded_nl 只保留 [E14][E15] 的局部传感恢复行为，没有硬编 C3 forced-transition 钩子。
- **C4**: C4 暴露在 [E6][E7][E8][E11][E12][E16]：Dynamixel jaws、limbs、rear whegs、ArduCAM、rangefinder、IMU 和 antenna 等物理执行器/传感器都作为动作载体出现。

**Provenance** (16 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.3 §2.1 \| paper_content.txt 行 170-173 | The robotic agent's microcontroller executes a finite state machine (FSM) | microcontroller-executed FSM |
| [E2] | paper.pdf p.9 Appendix B \| paper_content.txt 行 629-634 | The excavation and deposition areas are denoted with blue and red lights, respectively | blue and red lights mark excavation and deposition zones |
| [E3] | STM §1 摘录 A \| paper.pdf p.3 §2.1 \| paper_content.txt 行 176-180 | The transitions between behaviors are governed by environmental signals in the form of fixed ligh… | behavior transitions governed by fixed lights and object-proximity informatio… |
| [E4] | STM §1 摘录 B \| paper.pdf p.9 Appendix C \| paper_content.txt 行 597-604 | excavate material, transport it to the deposition site, locate an existing deposit, and return to… | nominal cycle sequence |
| [E5] | STM §1 摘录 B \| paper.pdf p.9 Appendix C \| paper_content.txt 行 605-607 | Turning is initiated after successful excavation or deposition and is only stopped once the RGB s… | turning start and RGB local-maximum stopping condition |
| [E6] | paper.pdf p.3 §2.2.1 \| paper_content.txt 行 190-194 | The robot manipulates geometrically cohesive material using a set of interlocking jaws | interlocking jaws manipulate the material |
| [E7] | paper.pdf p.3 §2.2.1 \| paper_content.txt 行 193-194 | These jaws are 3D printed and are actuated by a single Dynamixel AX12A motor. | jaws actuated by a Dynamixel AX12A motor |
| [E8] | paper.pdf p.3 §2.2.1 \| paper_content.txt 行 199-203 | a sequence of initial material sensing and horizontal separation, followed by repeated vertical a… | excavation internal action sequence using limbs and rear whegs |
| [E9] | paper.pdf p.4 §2.2.3 \| paper_content.txt 行 267-270 | the robot does not perform a fixed number of excavation procedures. Instead, the robot runs this … | transition out of excavation is not fixed-count and depends on jaw closure |
| [E10] | paper.pdf p.4 §2.2.3 \| paper_content.txt 行 271-273 | measured using the Dynamixel motor’s internal encoders, which indicate whether the jaw angle is g… | Dynamixel encoder jaw-angle threshold greater than about 30 degrees |
| [E11] | paper.pdf p.9 Appendix A sensing modalities \| paper_content.txt 行 620-623 | The ArduCAM provides long-range sensing in the form of 320x240 monochrome images | 320x240 monochrome ArduCAM image |
| [E12] | STM §1 摘录 B \| paper.pdf p.9 Appendix C \| paper_content.txt 行 611-612 | While the robot is moving to deposit, it takes a picture using the ArduCAM and searches for a pile | during transport toward deposit, controller takes an ArduCAM image and search… |
| [E13] | STM §1 摘录 B \| paper.pdf p.9 Appendix C \| paper_content.txt 行 612-615 | counting the number of “dark” pixels (below a threshold) that exist in a column, for which two di… | dark-pixel threshold and bright-region compound vision condition |
| [E14] | paper.pdf p.8 Appendix A Sensing modalities \| paper_content.txt 行 527-530 | The rangefinder indicates when an obstacle is in front of the robot, which triggers a reversing m… | obstacle-triggered reversing recovery behavior |
| [E15] | paper.pdf p.8 Appendix A Sensing modalities \| paper_content.txt 行 531-533 | The IMU is used to indicate when body motion (specifically, pitching) is impeded, which in turn t… | IMU-triggered crutch maneuver when pitching is impeded |
| [E16] | STM §1 摘录 C \| paper.pdf p.10 FSM final state \| paper_content.txt 行 675-679 | search with its antenna and deposit its material either at the existing pile or at the wall and t… | final deposit behavior and return turn |

**Intentional omissions**: 没有加入 emergency stop、any-state fault、timeout、forced recovery path、valve/pump 编号或显式层次 mode，因为原文没有支撑。没有逐一展开 Figure 13 的全部 state name，以避免违反任务中“禁止列出全部 state name”的限制。

</details>


##### 2. `[227]` 🏭 Pause-resume segmented-panel assembly process controller (FSM-basic)

- **领域**: 🏭
- **论文**: paper #764 [`sensor-guided-assembly-segmented-structures-industrial-robots`](../../../sources/sensor-guided-assembly-segmented-structures-industrial-robots/STM.md)
- **是什么**: 这是一个工业机器人分段复合板装配流程监督器，用相机定位与对准、F/T 传感器进行接触力控制，并驱动 ABB 机器人和真空吸盘夹爪完成拾取、运输、放置。典型流程是 Move Above Pickup Nest -> Approach Panel -> Pick Up -> Transport -> Place Panel -> Finish，中间可由操作员暂停、接管、回放或恢复。
- **scale**: states=9 / events=9 / vars=8 / trans=22
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文写到 state transition 在 safe teleoperation 或 autonomous mode 下执行，用户可 interrupt and take over，图 4 还有中心 Pause 与多状态的 pause/resume，但整体仍是扁平状态图而非层次化 composite state。
- **C2 数值守卫**: 🟡 — 原文明确把 excessive force in inadvertent contacts 作为 exception condition，并在拾取/放置中给出 force setpoint 250 N、specified 200 N，属于清楚的单类数值阈值 guard。
- **C3 forced fault**: 🟢 — 原文说 process may be interrupted at any time by the operator or under exception conditions，且 progression between states may be paused at any point 并 resume without restarting the whole process，具备跨阶段强制暂停/恢复语义。
- **C4 硬件解耦**: 🟢 — 原文硬件包括 ABB IRB-6640 robot、6-suction-cup vacuum gripper、F/T sensor、overhead/gripper cameras，且 controller sends joint angle commands and RAPID signals，six suction cups are then engaged。
- **对 PATH2 的价值**: 该样本对 PATH2 的价值主要在 C3 与 C4：它是清晰、真实的工业装配流程控制器，暂停/恢复/异常接管语义跨越多个工艺阶段，同时绑定机器人、夹爪、视觉与力控硬件。NL 描述独立且图 4 给出明确状态结构，适合作为 T0 中制造控制类强样本。
- **风险**: 主要风险是状态图偏扁平，数值 guard 多来自下层运动/力控上下文，不能把 QP 控制细节过度扩写成高层 FSM 迁移逻辑。

<details><summary><b>📝 扩充 NL（245 词 / 16 markers / 16 provenance entries）</b></summary>

**Expanded NL**:

> The controller supervises a robotic assembly process for large segmented composite structures, where an industrial robot repeatedly moves from locating and picking up a panel, through transport, to placement before returning to the next pickup when panels and nest space remain [E1] [E2] [E3]. The finite state machine governs process flow and the user interface, and its system state is represented by robot pose, sensor measurements, and end-effector conditions [E4] [E5]. In the pickup phase, an overhead camera estimates the panel position and orientation; once the gripper reaches the supported contact condition of 250 N, six suction cups are engaged to attach and lift the panel [E6] [E7]. During placement, wrist-mounted cameras guide alignment while force feedback regulates contact, with the placement force converging to the specified 200 N and the detected alignment error driven below 1 mm [E8] [E9] [E10]. State transitions may run autonomously with vision and force guidance or in safe teleoperation, and the operator may step through operations, interrupt, and take over in teleoperation [E11]. If the process is interrupted by the user or by an exception such as excessive inadvertent contact force, the FSM supports return to the previous known state [E12] [E13]. At any point, progression between states can be paused for intervention; the interrupted step can then be played back or resumed by replanning the trajectory without restarting the whole process, and the operator can manually continue by moving to a subsequent or previous step [E14] [E15] [E16].

**Axis coverage**:

- **C1**: 原文无层次结构，未提供 C1 钩子；expanded_nl 只在 [E2] [E11] 暴露三步流程与 autonomous/safe teleoperation 模式，没有构造 sub-mode 或默认入口。
- **C2**: C2 由 [E3] 的 panels/nest-space 条件、[E7] 的 250 N 接触条件、[E9] 的 200 N 放置力与 [E10] 的 1 mm 误差阈值暴露，未使用 Z3 不支持的数学函数。
- **C3**: C3 由 [E12] [E13] [E14] [E15] 的 user/exception interruption、任意点 pause、previous-known-state return 与 replay/resume/replan 暴露，属于横切于各流程步骤的恢复语义。
- **C4**: C4 由 [E6] [E7] [E8] [E9] 的 overhead camera、six suction cups、wrist-mounted cameras 与 placement force feedback 暴露，尤其是 250 N 后吸盘 engage 的物理 effector 动作。

**Provenance** (16 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 47-48 | large segmented composite structures | robotic assembly process for large segmented composite structures |
| [E2] | STM §1 摘录 B \| paper.pdf p.4 §3 \| paper_content.txt 行 183-188 | three major steps: panel localization and pick-up, panel transport, and panel placement | flow from locating and picking up a panel, through transport, to placement |
| [E3] | STM §1 摘录 B \| paper.pdf p.4 §3 \| paper_content.txt 行 188-190 | repeats indefinitely as long as there are panels available for pick-up and there is space in the … | returning to the next pickup when panels and nest space remain |
| [E4] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 52-53 | A ﬁnite state machine governs the process ﬂow and user interface. | finite state machine governs process flow and the user interface |
| [E5] | STM §1 摘录 D \| paper.pdf p.8 Figure 4 caption \| paper_content.txt 行 353-356 | robot pose, sensor measurements, and end effector conditions | system state represented by robot pose, sensor measurements, and end-effector… |
| [E6] | paper.pdf p.10 §6.1 Panel Pickup \| paper_content.txt 行 437-438 | With the calibrated overhead camera, the pick-up position and orientation of the panel are estimated | overhead camera estimates the panel position and orientation |
| [E7] | paper.pdf p.10 §6.1 Panel Pickup \| paper_content.txt 行 439-441 | force setpoint 250 N is reached. The six suction cups are then engaged | 250 N contact condition followed by suction-cup engagement |
| [E8] | paper.pdf p.5 §3 Solution Implementation \| paper_content.txt 行 206 | robot wrist mounted cameras for vision-guided alignment | wrist-mounted cameras guide placement alignment |
| [E9] | paper.pdf p.12 Figure 9 caption \| paper_content.txt 行 531-532 | Under force and vision feedback, the placement force converges to the specified 200 N | force feedback and placement force converging to the specified 200 N |
| [E10] | paper.pdf p.12 §6.3.2 \| paper_content.txt 行 495-497 | the detected error is smaller than 1 mm. | detected alignment error driven below 1 mm |
| [E11] | STM §1 摘录 C \| paper.pdf p.7 §4 Software Architecture \| paper_content.txt 行 329-334 | state transition is executed in either safe teleoperation or autonomous mode with vision and forc… | autonomous and safe teleoperation transition modes |
| [E12] | STM §1 摘录 B \| paper.pdf p.4 §3 \| paper_content.txt 行 190-192 | under exception conditions (e.g., excessive force in inadvertent contacts) | exception such as excessive inadvertent contact force |
| [E13] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 52-54 | return to the previous known state in case of error condition | FSM supports return to the previous known state |
| [E14] | STM §1 摘录 C \| paper.pdf p.7 §4 Software Architecture \| paper_content.txt 行 336-337 | The progression between states may be paused at any point if intervention is needed. | pause at any point for intervention |
| [E15] | STM §1 摘录 C \| paper.pdf p.7 §4 Software Architecture \| paper_content.txt 行 337-338 | played back or resumed by replanning the trajectory without restarting the whole process | playback or resume by replanning without restarting |
| [E16] | STM §1 摘录 B \| paper.pdf p.4 §3 \| paper_content.txt 行 192-193 | moving to the subsequent or previous steps | operator manually continues to a subsequent or previous step |

**Intentional omissions**: 没有加入 valve 编号、forced emergency-stop 目标状态或固定 reset 默认状态，因为原文只支持 pause/interruption/previous known state/resume，没有给出这些具体控制语义。没有把 FLIR/ATI/ABB EGM 等型号细节塞入 expanded_nl，因为它们虽在硬件章节出现，但会把输入变成硬件清单而非该 FSM 的核心需求。

</details>


##### 3. `[061]` 🚗 Five-Mode Benefit-Evaluated Driving Supervisor (FSM-basic)

- **领域**: 🚗
- **论文**: paper #290 [`autonomous-driving-benefit-evaluation-fsm`](../../../sources/autonomous-driving-benefit-evaluation-fsm/STM.md)
- **是什么**: 这是自动驾驶车辆的高层驾驶行为决策 supervisor，基于交通信息、环境感知和车辆状态在自由行驶、跟车、换道、紧急制动、故障停车之间切换。原文实车平台使用 DGPS/IMU、Lidar、Mobileye Camera、ESR 感知，并把控制命令下发到转向、油门和制动执行器。
- **scale**: states=5 / events=8 / vars=14 / trans=11
- **verdict**: 💎 STRONG
- **C1 多模式 dead-end**: 🟡 — 原文称“five basic driving behavior modes are constructed”，并给出 Figure 1 行为切换图，但没有 composite state、init/pseudo 或嵌套退出语义。
- **C2 数值守卫**: 🟢 — 原文把切换条件量化为 D=Max(Rc,Ra1…Ran)，并给出 Rspace 中 tttcif/tttcir 与阈值的合取比较、Refficiency=c3*vexp/vlaw 等数值公式。
- **C3 forced fault**: 🟠 — 原文只写“Failure parking mode: When automatic driving system encounters failure fault...”以及终止态可进入 failure parking，未明确说明 from any state 或 any mode 的 cross-cutting fault 切换。
- **C4 硬件解耦**: 🟢 — 原文写“control command is sent to each actuator”，实车平台能实现 steering wheel、throttle、brake 三类执行器自动化。
- **对 PATH2 的价值**: 该样本对 PATH2 的主要价值在 C2 和 C4：收益评估、TTC、速度、合法性等变量能支撑 symbolic guard grounding，实车线控平台又给了明确 actuator 映射。它也是独立的自动驾驶控制样本，NL 描述较清晰，适合作为 T0 中等规模 case。
- **风险**: 五模式本身是扁平 FSM，故障停车不是明确 any-mode forced transition，且 Figure 1 的检查节点和箭头需要在建模时规范化。

<details><summary><b>📝 扩充 NL（276 词 / 20 markers / 20 provenance entries）</b></summary>

**Expanded NL**:

> The autonomous-driving decision system is a finite-state framework for an autonomous-driving vehicle, with five basic behavior modes constructed from human-driver operation [E1]. When automatic driving is entered, the initial behavior is free driving and switches are triggered by external input events E [E2][E3]; termination occurs when the vehicle exits automatic driving or enters failure parking [E4]. The dynamic decision and planning module receives traffic and environment information from perception, generates an optimal behavior and path, and sends the control command to each actuator [E5]. For lane-change decisions, traffic information covers rules and road information, environment information gives real-time obstacle location and velocity [E6], and vehicular-state information describes the ego vehicle running state [E7]. Free driving is used when the current lane obeys driving rules and has no obstacles; when following a front vehicle, ego speed is adjusted in real time to maintain a safe distance [E8][E9]. If the current lane contains obstacles, has low driving efficiency, or does not conform to traffic rules, the ego vehicle needs to change lane; if that avoidance cannot be completed, the controller enters a braking response [E10][E11]. The lane-change model treats motivations as state-transition conditions and compares current benefit R_c with alternative benefits R_a_i over efficiency, space, safety, comfort, and negative effects [E12][E13][E14][E15]. A switching-cost constant H requires the behavior change to have higher benefit than the current behavior and avoids frequent switching [E16][E17]. When the automatic-driving system encounters a failure fault, failure parking pulls the vehicle into the rightmost lane and stops immediately [E18]. In the real-vehicle platform, steering wheel, throttle, and brake are automated, and actuator-control, sensor, and vehicular-state information are exchanged through MicroAutobox over CAN Bus [E19][E20].

**Axis coverage**:

- **C1**: 原文无层次结构，未提供 C1 钩子；expanded_nl 只保留扁平 FSM 与初始 free driving 信息 [E1][E2]。
- **C2**: C2 部分支持：expanded_nl 暴露外部事件 E、state-transition conditions、收益变量 R_c/R_a_i 与 H 的比较触发 [E3][E12][E13][E16]；原文未给具体数值阈值。
- **C3**: 原文不支持 any-state、each-cycle 或 forced-fault 横切语义；failure fault 只支持 failure parking 情形 [E18]，未写成全局强制迁移。
- **C4**: C4 部分支持：expanded_nl 写到 actuator command、steering wheel/throttle/brake 自动化与 MicroAutobox/CAN Bus 信息交换 [E5][E19][E20]；原文未给具体 actuator 编号或 enter/exit 动作。

**Provenance** (20 entries):

| marker | source | quote (≤30 词) | supports |
|---|---|---|---|
| [E1] | STM §1 摘录 A \| paper.pdf p.1 Abstract \| paper_content.txt 行 23-25 | five basic driving behavior modes are constructed, a driving behavior decision making framework f… | finite-state framework and five basic behavior modes |
| [E2] | STM §1 摘录 C \| paper.pdf p.6 §4 \| paper_content.txt 行 443-444 | The initial state of the vehicle entering automatic driving mode is free driving. | initial behavior is free driving |
| [E3] | STM §1 摘录 C \| paper.pdf p.6 §4 \| paper_content.txt 行 441-443 | the switching of driving behaviors is triggered by external input event set E. | switches are triggered by external input events E |
| [E4] | STM §1 摘录 C \| paper.pdf p.6 §4 \| paper_content.txt 行 444-446 | In termination state, the vehicle enters failure parking mode or exits automatic driving mode. | termination occurs by exiting automatic driving or entering failure parking |
| [E5] | paper.pdf p.4 §2 \| paper_content.txt 行 312-317 | This module obtains traffic and environment information from perception module. Based on the info… | dynamic decision/planning module input, optimal behavior/path generation, act… |
| [E6] | STM §1 摘录 D \| paper.pdf p.6 §3 \| paper_content.txt 行 405-408 | Traffic information reflects the traffic rules and road information; environment information extr… | traffic rules/road information and obstacle location/velocity inputs |
| [E7] | STM §1 摘录 D \| paper.pdf p.6 §3 \| paper_content.txt 行 408-409 | vehicular state information reflects the running state information of ego vehicle. | vehicular-state information describes ego running state |
| [E8] | STM §1 摘录 B \| paper.pdf p.4 §2 \| paper_content.txt 行 287-288 | Free driving mode: The current lane conforms driving rules and no obstacles in the lane. | free driving guard |
| [E9] | paper.pdf p.4 §2 \| paper_content.txt 行 289-292 | ego vehicle speed is real time adjusted to achieve safety car following distance. | front-vehicle following adjusts ego speed for safe distance |
| [E10] | STM §1 摘录 B \| paper.pdf p.4 §2 \| paper_content.txt 行 293-297 | In case of obstacles in current lane, low driving efficiency in current lane or the current lane … | lane-change trigger conditions |
| [E11] | STM §1 摘录 B \| paper.pdf p.4 §2 \| paper_content.txt 行 298-301 | For emergency scenario in which lane changing obstacle avoidance could not be completed, autonomo… | braking response when lane-change avoidance cannot be completed |
| [E12] | paper.pdf p.6-7 §5 \| paper_content.txt 行 459-465 | The motivations could be used as the conditions of state transition for decision making system ba… | motivations as state-transition conditions |
| [E13] | paper.pdf p.7 §5 \| paper_content.txt 行 496-500 | 𝑅𝑐 represents the benefit value of current driving behavior, 𝑅𝑎1……𝑅an represent the benefit value… | current benefit R_c and alternative benefits R_a_i |
| [E14] | paper.pdf p.7 §5 \| paper_content.txt 行 490-493 | Benefits of lane change behavior could be summarized as following aspects: driving efficiency, dr… | benefit factors efficiency, space, safety, comfort |
| [E15] | paper.pdf p.7 §5 \| paper_content.txt 行 493-494 | potential negative effects of lane change behavior should also be considered. | negative effects included in benefit evaluation |
| [E16] | paper.pdf p.7 §5 \| paper_content.txt 行 507-512 | H is regulates constant representing the execution cost of driving behavior switching, it regulat… | H as switching-cost trigger requiring higher benefit |
| [E17] | paper.pdf p.7 §5 \| paper_content.txt 行 512-513 | It avoids the potential effect of frequently switching of driving behavior. | avoid frequent switching |
| [E18] | STM §1 摘录 B \| paper.pdf p.4 §2 \| paper_content.txt 行 302-305 | When automatic driving system encounters failure fault, autonomous driving vehicle pulled into th… | failure parking response |
| [E19] | paper.pdf p.8 §6 \| paper_content.txt 行 641-644 | The system could realize the automation of steering wheel, throttle and brake. | automated steering wheel, throttle, and brake |
| [E20] | paper.pdf p.8 §6 \| paper_content.txt 行 645-647 | All actuator control information, sensor and vehicular state real time information are interacted… | actuator-control, sensor, and vehicular-state information over MicroAutobox/C… |

**Intentional omissions**: 没有补写具体传感器编号、执行器编号、阈值数字、enter/exit 硬件动作或 any-state forced fault path，因为原文没有这些粒度的控制规则。也没有把 TTC 分段公式完整塞进 NL，以避免把输入变成公式 dump。

</details>



## 📋 全量评审表（按桶）

### HSM-layered （57 条）

| id | 领域 | 桶 | C1 | C2 | C3 | C4 | verdict | states/events/vars/trans | 案例 |
|---|---|---|---|---|---|---|---|---|---|
| 009 | 🚗 | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 9 / 13 / 10 / 20 | [Two-Stage Mission-and-Control FSM for Urban Driving](../../../sources/a-hierarchical-control-system-for-autonomous-driving-towards-urban-challenges/STM.md)  🎯 |
| 118 | ⚙️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 10 / 12 / 8 / 17 | [Robotic Spacecraft Subsystem Lifecycle Supervisor](../../../sources/hirosco-high-level-robotic-spacecraft-controller/STM.md)  🎯 |
| 138 | ⚙️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 14 / 18 / 10 / 34 | [Ask-for-Directions Hierarchical Navigation Supervisor](../../../sources/amazing-race-robot-edition/STM.md)  🎯 |
| 169 | ⚙️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 8 / 12 / 7 / 15 | [Hierarchical mission-execution FSM for an autonomous mari...](../../../sources/pirate-precision-imaging-real-time-autonomous-tracker-explorer/STM.md)  🎯 |
| 207 | 🏭 | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 10 / 5 / 5 / 14 | [Hierarchical vine-pruning autonomy supervisor](../../../sources/bumblebee-autonomous-robotic-vine-pruning/STM.md)  🎯 |
| 160 | ✈️ | HSM | 🟢 | 🟢 | 🟢 | 🟡 | 💎 | 10 / 20 / 8 / 24 | [Mission-Mode / Command-Mode VTOL UAV Supervisor](../../../sources/onboard-mission-management-vtol-uav-sequence-supervisory-control/STM.md)  🎯 |
| 159 | 🌡️ | HSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 61 / 42 / 45 / 105 | [Water-filter test-bench main-state and valve supervisor](../../../sources/control-system-design-of-water-filter-test-bench/STM.md)  🛡️ |
| 010 | ✈️ | HSM | 🟢 | 🟢 | 🟢 | 🟡 | 💎 | 27 / 17 / 12 / 48 | [Master-and-Autopilot Mission Cycle for Autonomous Rotorcr...](../../../sources/long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition/STM.md)  🛡️ |
| 015 | ⚙️ | HSM | 🟢 | 🟢 | 🟢 | 🟡 | 💎 | 7 / 8 / 6 / 14 | [Greenhouse row-inspection navigation supervisor](../../../sources/autonomous-navigation-framework-holonomic-mobile-robots-agriculture/STM.md)  🛡️ |
| 012 | ⚙️ | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 14 / 22 / 9 / 34 | [Multi-modal drive-fly mission FSM for TURVTOL](../../../sources/terrestrial-unmanned-roving-vertical-take-off-and-landing-turvtol/STM.md)  🛡️ |
| 172 | ✈️ | HSM | 🟢 | 🟡 | 🟢 | 🟡 | 💎 | 17 / 15 / 8 / 31 | [Building-interior firefighting mission supervisor](../../../sources/autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle/STM.md)  🛡️ |
| 179 | 🏢 | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 18 / 14 / 15 / 36 | [Robot Elevator Request-Floor-Estimation Recovery Supervisor](../../../sources/secure-automated-elevator-management-pressure-sensor-floor-estimation/STM.md)  🛡️ |
| 016 | ⚙️ | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 12 / 11 / 14 / 18 | [Pick-and-drop supervisor for the waste-selection manipulator](../../../sources/state-machine-based-hybrid-position-force-control-waste-mobile-robot/STM.md)  |
| 019 | ✈️ | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 14 / 17 / 9 / 22 | [Mission supervisor for mine exploration and pillar inspec...](../../../sources/autonomous-uav-multimodal-mapping-underground-mines/STM.md)  |
| 105 | ✈️ | HSM | 🟢 | 🟡 | 🟢 | 🟡 | 💎 | 12 / 12 / 8 / 30 | [Mission-mode / command-mode UAV sequence supervisor](../../../sources/sequence-supervisory-control-onboard-uav-mission-management/STM.md)  |
| 200 | 🌡️ | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 9 / 12 / 17 / 15 | [Hierarchical nutrient-solution management supervisor](../../../sources/virtual-commissioning-wick-soilless-cultivations/STM.md)  |
| 204 | ⚙️ | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 15 / 11 / 10 / 24 | [Pallet Delivery Hierarchical Perception-Manipulation Supe...](../../../sources/pallet-manipulation-hierarchical-state-machine-experiment/STM.md)  |
| 239 | 🚗 | HSM | 🟢 | 🟢 | 🟡 | 🟢 | 💎 | 11 / 17 / 8 / 24 | [Urban automated-driving event supervisor for traffic ligh...](../../../sources/full-automated-drive-urban-environments-gomentum-station/STM.md)  |
| 102 | 🅿️ | HSM | 🟡 | 🟢 | 🟢 | 🟢 | 💎 | 14 / 18 / 14 / 24 | [Drop-off-to-pick-up autonomous parking supervisor](../../../sources/autonomous-parking-system-urban-mobility/STM.md)  |
| 176 | 🅿️ | HSM | 🟡 | 🟢 | 🟢 | 🟢 | 💎 | 11 / 10 / 9 / 18 | [Auto-Manual Lift Controller for Multilevel Parking](../../../sources/a-novel-approach-of-lift-control-in-automatic-car-parking-using-plc/STM.md)  |
| 069 | 🚗 | HSM | 🟢 | 🟡 | 🟡 | 🟢 | 💎 | 13 / 14 / 9 / 32 | [Urban Driving State-and-Exception Supervisor](../../../sources/junior-stanford-entry-urban-challenge/STM.md)  |
| 084 | 🚗 | HSM | 🟢 | 🟡 | 🟡 | 🟢 | 💎 | 13 / 18 / 14 / 24 | [Winner-Takes-All Driving Behaviors with Parking and Repla...](../../../sources/odin-team-victortango-darpa-urban-challenge/STM.md)  |
| 100 | 🏭 | HSM | 🟢 | 🟡 | 🟡 | 🟢 | 💎 | 10 / 7 / 11 / 6 | [Multilayer HRI operation-mode safety supervisor](../../../sources/safety4-dynamic-fsm-multilayer-operation-modes/STM.md)  |
| 104 | 🏢 | HSM | 🟢 | 🟡 | 🟡 | 🟢 | 💎 | 4 / 8 / 8 / 13 | [Four-rank privileged elevator service supervisor](../../../sources/priority-rank-elevator-control-plc/STM.md)  |
| 128 | ✈️ | HSM | 🟢 | 🟡 | 🟡 | 🟢 | 💎 | 8 / 8 / 6 / 14 | [Mission-Phase FSM-BT Supervisor for Mars Science Helicopter](../../../sources/hybrid-autonomy-future-mars-science-helicopter/STM.md)  |
| 116 | 🅿️ | HSM | 🟡 | 🟡 | 🟢 | 🟢 | 💎 | 14 / 16 / 12 / 24 | [Circular Parking Garage Auto/Manual Supervisor](../../../sources/scale-model-parking-garage-integrating-automation-in-parking-facilities/STM.md)  |
| 133 | 🏢 | HSM | 🟢 | 🟢 | 🟡 | 🟡 | 💎 | 13 / 17 / 19 / 25 | [Hierarchical Sliding-Door Motion FSM with Blockade Recovery](../../../sources/mechatronic-control-system-finite-state-machine/STM.md)  |
| 191 | ⚙️ | HSM | 🟢 | 🟢 | 🟡 | 🟡 | 💎 | 9 / 8 / 12 / 10 | [Four-State Exploratory Manipulation Supervisor with Fault...](../../../sources/autonomous-robotic-manipulation-exploratory-interactions/STM.md)  |
| 205 | 🏭 | HSM | 🟡 | 🟡 | 🟢 | 🟢 | 💎 | 14 / 12 / 10 / 22 | [Hierarchical packaging-machine supervisor](../../../sources/packaging-filling-machine-control-plc-logicon/STM.md)  |
| 174 | ⚙️ | HSM | 🟢 | 🟠 | 🟡 | 🟢 | 💎 | 56 / 56 / 17 / 56 | [Multitask Transmission-Line Maintenance Behavior Supervisor](../../../sources/self-evolution-mobile-robot-high-voltage-transmission-line/STM.md)  |
| 071 | ⚙️ | HSM | 🟢 | 🟡 | 🟡 | 🟡 | ✨ | 15 / 19 / 15 / 32 | [Hierarchical Navigation-and-Gait Supervisor for a Walking...](../../../sources/finite-state-automaton-control-system-walking-machines/STM.md)  |
| 074 | ⚙️ | HSM | 🟢 | 🟡 | 🟡 | 🟡 | ✨ | 3 / 4 / 12 / 6 | [Table-Tennis Ball-Collecting Robot Search-Collect-Avoid H...](../../../sources/communication-within-multi-fsm-based-robotic-systems/STM.md)  |
| 094 | 🏭 | HSM | 🟢 | 🟡 | 🟡 | 🟡 | ✨ | 13 / 10 / 10 / 24 | [Eye-Hand Instruction-and-Mapping Assembly Supervisor](../../../sources/human-robot-collaborative-assembly-eye-hand-fsm/STM.md)  |
| 111 | 🚗 | HSM | 🟢 | 🟢 | 🟠 | 🟢 | 💎 | 4 / 8 / 10 / 10 | [Four-state emergency driving hierarchical decision contro...](../../../sources/intelligent-decision-making-vehicle-emergency-fsm/STM.md)  |
| 127 | 🏭 | HSM | 🟢 | 🟢 | 🟠 | 🟢 | 💎 | 15 / 15 / 11 / 28 | [Manual-Maintenance-Auto Palletizer Supervisor](../../../sources/prefabricated-board-transfer-palletizer-s7-1500-plc/STM.md)  |
| 135 | ✈️ | HSM | 🟢 | 🟢 | 🟠 | 🟢 | 💎 | 18 / 14 / 15 / 24 | [Hierarchical FMS Command Sequencer for a Small-Scale UAV](../../../sources/autonomous-autopilot-control-system-small-scale-uavs/STM.md)  |
| 153 | 🏭 | HSM | 🟢 | 🟢 | 🟠 | 🟢 | 💎 | 15 / 18 / 14 / 28 | [Brick-load/unload mobile-manipulation challenge supervisor](../../../sources/autonomous-mobile-manipulation-wall-building-mbzirc-2020/STM.md)  |
| 231 | ✈️ | HSM | 🟢 | 🟢 | 🟠 | 🟢 | 💎 | 3 / 5 / 6 / 5 | [Hierarchical in-flight reconfiguration planner](../../../sources/beatle-self-reconfigurable-aerial-robot/STM.md)  |
| 043 | 🅿️ | HSM | 🟢 | 🟢 | 🟡 | 🟠 | 💎 | 10 / 12 / 14 / 24 | [Hierarchical AVP Mode and Behavior Supervisor](../../../sources/automated-valet-parking-decision-planning-finite-state-machine/STM.md)  |
| 209 | ✈️ | HSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 13 / 15 / 10 / 18 | [Three-stage visual-sliding-landing mission supervisor](../../../sources/robust-accurate-drone-landing-moving-targets/STM.md)  |
| 006 | ✈️ | HSM | 🟢 | 🟡 | 🟠 | 🟢 | 💎 | 6 / 9 / 5 / 14 | [Task activation and interruption logic for UAV mission ma...](../../../sources/behavior-trees-for-uav-mission-management/STM.md)  |
| 108 | 🏭 | HSM | 🟢 | 🟠 | 🟡 | 🟡 | 🟢 | 20 / 15 / 10 / 34 | [Teaching/teleoperation/playback multimodal programming su...](../../../sources/no-code-robotic-programming-agile-production/STM.md)  |
| 122 | ✈️ | HSM | 🟢 | 🟡 | 🟠 | 🟢 | 💎 | 19 / 14 / 18 / 27 | [Planner-Execution Mission-Agent Supervisor](../../../sources/software-architecture-autonomous-uav-mission-management-control/STM.md)  |
| 184 | 🅿️ | HSM | 🟢 | 🟡 | 🟠 | 🟢 | 💎 | 24 / 14 / 12 / 38 | [Priority-Buffered Garage Parking and Retrieval Supervisor](../../../sources/automatic-system-for-garage-control/STM.md)  |
| 107 | ⚙️ | HSM | 🟢 | 🟢 | 🟠 | 🟡 | 💎 | 3 / 6 / 8 / 8 | [Contact-transition whole-body humanoid controller](../../../sources/brain-machine-interface-humanoid-motion/STM.md)  |
| 213 | ⚙️ | HSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 8 / 8 / 5 / 12 | [Autonomous-manual fire-fighting mission supervisor](../../../sources/development-of-360-degrees-autonomus-and-manual-fire-fighting-robot/STM.md)  |
| 027 | 🩺 | HSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 9 / 9 / 8 / 11 | [Hierarchical gait-assistance supervisor for the ALLOR kne...](../../../sources/assistive-control-active-knee-orthosis-walker-post-stroke/STM.md)  |
| 033 | 🩺 | HSM | 🟢 | 🟢 | ⚪ | 🟡 | 🟢 | 7 / 7 / 4 / 7 | [Hierarchical walking-standing supervisor for the self-con...](../../../sources/preliminary-evaluations-of-a-self-contained-anthropomorphic-transfemoral-prosthesis/STM.md)  |
| 044 | 🚗 | HSM | 🟢 | 🟢 | ⚪ | 🟡 | 🟢 | 46 / 34 / 18 / 36 | [Three-Layer Straight-Lane Driving Supervisor](../../../sources/autonomous-vehicle-driving-behavior-hierarchical-state-machine/STM.md)  |
| 152 | ⚙️ | HSM | 🟢 | 🟢 | ⚪ | 🟡 | 🟢 | 19 / 13 / 12 / 28 | [Tactical-role hierarchical soccer-team coordinator](../../../sources/robot-soccer-strategy-hfsm-centralized-architectures/STM.md)  |
| 037 | 🩺 | HSM | 🟢 | 🟡 | ⚪ | 🟡 | 🟢 | 22 / 12 / 11 / 28 | [Ambulation-mode and gait-subphase supervisor for the open...](../../../sources/open-source-bionic-leg-clinical-implementation/STM.md)  |
| 070 | 🌡️ | HSM | 🟢 | 🟡 | ⚪ | 🟡 | 🟢 | 6 / 9 / 8 / 12 | [Two-Level Converter Signalling and Mode-Switch Controller](../../../sources/control-strategies-low-voltage-dc-microgrids/STM.md)  |
| 066 | 🚗 | HSM | 🟢 | 🟢 | ⚪ | 🟠 | 🟢 | 13 / 7 / 20 / 36 | [Three-Layer Scenario-to-Behavior Driving HSM](../../../sources/decision-making-framework-autonomous-vehicles-hierarchical-state-machine/STM.md)  |
| 232 | 🏭 | HSM | 🟡 | 🟢 | ⚪ | 🟢 | 🟢 | 4 / 4 / 4 / 11 | [Workflow-driven industrial exoskeleton support supervisor](../../../sources/exoskeleton-workflow-finite-state-machine-adaptivity/STM.md)  |
| 117 | 🚗 | HSM | 🟢 | 🟡 | ⚪ | 🟠 | 🟢 | 6 / 12 / 8 / 13 | [Two-Layer Bus Driving-Behavior Supervisor](../../../sources/driving-behavior-planning-trajectory-generation-autonomous-electric-bus/STM.md)  |
| 067 | 🚗 | HSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 23 / 25 / 25 / 247 | [Global-and-Local HFSM for 5G-V2X Driving Decisions](../../../sources/topsis-gra-autonomous-driving-decision-making-5g-v2x/STM.md)  |
| 036 | 🩺 | HSM | 🟡 | 🟠 | ⚪ | 🟡 | 🔘 | 5 / 8 / 7 / 5 | [Two-level insole-driven damping supervisor for an MR-damp...](../../../sources/affordable-insole-sensor-based-transfemoral-prosthesis/STM.md)  |

### EFSM-interlock （131 条）

| id | 领域 | 桶 | C1 | C2 | C3 | C4 | verdict | states/events/vars/trans | 案例 |
|---|---|---|---|---|---|---|---|---|---|
| 142 | 🏭 | EFSM | 🟡 | 🟢 | 🟢 | 🟢 | 💎 | 13 / 18 / 11 / 21 | [HMI-Configured Cup Filling, Capping, and Labeling Line](../../../sources/plc-scada-liquid-filling-automation-ejosat/STM.md)  🎯 |
| 234 | 🅿️ | EFSM | 🟡 | 🟢 | 🟢 | 🟢 | 💎 | 11 / 13 / 8 / 20 | [Multi-level parking lift auto/manual positioning controller](../../../sources/lift-control-automatic-car-parking-using-plc/STM.md)  🎯 |
| 114 | 🅿️ | EFSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 12 / 18 / 6 / 24 | [Slot-Selected Rotary Parking and Retrieval Controller](../../../sources/vertical-rotary-car-parking-plc-outseal/STM.md)  🎯 |
| 008 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 12 / 12 / 13 / 12 | [Twelve-State EMS for LNG-Ship Hybrid Power Dispatch](../../../sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/STM.md)  🎯 |
| 090 | ⚙️ | EFSM | 🟡 | 🟢 | 🟢 | 🟡 | 💎 | 14 / 12 / 12 / 40 | [Joey Pipe-Network Exploration Supervisor](../../../sources/autonomous-control-miniaturized-mobile-robots-unknown-pipe-networks/STM.md)  🎯 |
| 181 | 🏢 | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 10 / 14 / 10 / 20 | [Priority-Scanned Smart-Home Utility and Access Controller](../../../sources/enhanced-smart-home-control-monitoring-system/STM.md)  🎯 |
| 026 | 🩺 | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 4 / 6 / 6 / 7 | [Preset gait-phase stimulation supervisor for hybrid FES-r...](../../../sources/modular-neuroprosthesis-hybrid-fes-robot-assistance/STM.md)  🛡️ |
| 052 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 7 / 7 / 4 / 10 | [Four-Scenario Micro-Grid EMS with SOC-Governed Battery Sw...](../../../sources/energy-management-strategy-hybrid-micro-grid-renewable-energy/STM.md)  🛡️ |
| 143 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 9 / 12 / 12 / 16 | [Auto-Manual WWTP Supervisor with Conductivity-Feedback Re...](../../../sources/boiler-wastewater-treatment-control-monitoring-plc-hmi/STM.md)  🛡️ |
| 151 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 7 / 8 / 9 / 13 | [Flow-Interlocked Liquid Transfer and Pause-Recovery Super...](../../../sources/liquid-level-monitoring-flow-liquid-distribution-plc-scada/STM.md)  🛡️ |
| 167 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 8 / 11 / 9 / 13 | [Flow-and-Water-Quality Feedback Dosing Controller](../../../sources/automatic-dosing-system-based-on-reclaimed-water-treatment/STM.md)  🛡️ |
| 215 | 🏭 | EFSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 8 / 10 / 8 / 11 | [Automatic Feeding, Tool Selection, Alignment, and Cutting](../../../sources/control-system-automatic-bamboo-splitting-equipment-plc/STM.md)  🛡️ |
| 004 | 🏭 | EFSM | 🟠 | 🟢 | 🟠 | 🟢 | 💎 | 13 / 14 / 5 / 16 | [Six-Bottle Carton Packing and Quality Gate](../../../sources/development-of-automatic-packaging-system-using-plc-and-scada-for-industries/STM.md)  |
| 005 | ✈️ | EFSM | 🟢 | 🟡 | 🟢 | 🟢 | 💎 | 8 / 12 / 8 / 16 | [Closed-mode CONOPS and safe-mode fallback in Masat-1](../../../sources/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation/STM.md)  |
| 017 | ⚙️ | EFSM | 🟠 | 🟢 | 🟠 | 🟢 | 💎 | 6 / 7 / 7 / 7 | [Cotton-boll detection and harvesting supervisor](../../../sources/center-articulated-hydrostatic-cotton-harvesting-rover/STM.md)  |
| 198 | ⚙️ | EFSM | 🟠 | 🟢 | 🟠 | 🟢 | 💎 | 3 / 3 / 3 / 5 | [Voltage-current-temperature trip protection controller](../../../sources/protection-of-induction-motor-using-plc/STM.md)  |
| 011 | ✈️ | EFSM | 🟡 | 🟡 | 🟢 | 🟢 | 💎 | 9 / 11 / 6 / 15 | [RSW Motion-Primitive Execution FSM for CCRS RTAS](../../../sources/preliminary-design-of-robotic-control-software-for-mars-sample-return-capture-containment-and-return-system/STM.md)  |
| 020 | ✈️ | EFSM | 🟡 | 🟢 | 🟡 | 🟡 | ✨ | 4 / 5 / 8 / 5 | [Dynamic-platform landing supervisor for a quadrotor UAV](../../../sources/proactive-guidance-uav-landing-dynamic-platform/STM.md)  |
| 022 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟢 | 🟢 | 9 / 6 / 6 / 12 | [CoM-triggered gait-assistance supervisor for the MINDWALK...](../../../sources/design-and-control-of-the-mindwalker-exoskeleton/STM.md)  |
| 038 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟢 | 🟢 | 7 / 4 / 7 / 12 | [Seven-state posture-selection controller for the multigra...](../../../sources/control-of-multigrasp-myoelectric-prosthetic-hands/STM.md)  |
| 073 | 🌡️ | EFSM | 🟡 | 🟡 | 🟢 | 🟢 | 💎 | 10 / 14 / 4 / 26 | [F-CHP Central Controller Mode Manager](../../../sources/design-development-and-testing-of-flexible-combined-heat-and-power-fchp-system/STM.md)  |
| 082 | 🌡️ | EFSM | 🟡 | 🟢 | ⚪ | 🟢 | 🟢 | 15 / 6 / 5 / 15 | [Fifteen-State SOC-Segmented PV-PEMFC-Battery EMS](../../../sources/state-machine-control-multi-sources-pv-pemfc-batteries/STM.md)  |
| 203 | 🏢 | EFSM | 🟡 | 🟢 | ⚪ | 🟢 | 🟢 | 3 / 5 / 4 / 6 | [Rank-Based CAN-Distributed Elevator Controller](../../../sources/distributed-elevator-control-system-can/STM.md)  |
| 225 | 🚆 | EFSM | 🟡 | 🟢 | 🟡 | 🟡 | ✨ | 5 / 7 / 6 / 11 | [Four-mode network-degraded railway crossing controller](../../../sources/development-of-a-network-level-crossing-system/STM.md)  |
| 025 | 🩺 | EFSM | 🟢 | 🟢 | 🟠 | 🟡 | 💎 | 13 / 15 / 16 / 15 | [Phase-aware gait-and-squat controller for the gastrocnemi...](../../../sources/enhanced-gastrocnemius-mimicking-powered-exoskeleton/STM.md)  |
| 057 | 🏭 | EFSM | 🟠 | 🟢 | ⚪ | 🟢 | 🟢 | 6 / 8 / 5 / 7 | [Grafcet-Based 24-Can Packaging Sequence Controller](../../../sources/development-of-plc-based-automated-packaging-control-system-via-grafcet/STM.md)  |
| 068 | 🅿️ | EFSM | 🟠 | 🟢 | ⚪ | 🟢 | 🟢 | 5 / 6 / 4 / 8 | [Multi-Slot Password-Gated Parking Controller](../../../sources/verilog-multi-car-parking-fsm-urban-management/STM.md)  |
| 024 | ⚙️ | EFSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 6 / 7 / 4 / 7 | [Trailer-docking supervisor for an autonomous surface vehicle](../../../sources/vision-driven-trailer-loading-autonomous-surface-vehicles/STM.md)  |
| 075 | 🅿️ | EFSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 6 / 7 / 9 / 8 | [Five-Step Laser-Guided Parallel Parking Automaton](../../../sources/rule-based-controller-simulation-autonomous-parallel-parking-car-like-robot/STM.md)  |
| 087 | 🅿️ | EFSM | 🟡 | 🟡 | 🟡 | 🟢 | ✨ | 6 / 6 / 4 / 10 | [ON-OFF-EMERGENCY Parking Gate Supervisor](../../../sources/plc-based-automatic-intelligent-car-parking-system/STM.md)  |
| 093 | ✈️ | EFSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 12 / 11 / 10 / 16 | [Search-Move-Descend-Inspect Multi-Target Mission Controller](../../../sources/multiple-ground-target-finding-inspection-multirotor-uas/STM.md)  |
| 098 | ⚙️ | EFSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 5 / 6 / 10 / 100 | [Five-state maneuver-aware fuel-cell/battery EMS](../../../sources/fuel-cell-electric-robot-energy-management/STM.md)  |
| 120 | 🌡️ | EFSM | 🟡 | 🟡 | 🟡 | 🟢 | ✨ | 15 / 14 / 9 / 22 | [Manual-auto flue-gas ozone treatment supervisor](../../../sources/ozone-desulfurization-and-denitration-control-system-based-on-plc-and-kingview/STM.md)  |
| 162 | 🌡️ | EFSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 4 / 3 / 10 / 9 | [Inverter-count secondary supervisor for microgrid efficie...](../../../sources/enhanced-hierarchical-microgrids-thermal-management/STM.md)  |
| 185 | 🏢 | EFSM | 🟡 | 🟡 | 🟡 | 🟢 | ✨ | 8 / 12 / 8 / 20 | [Three-Floor Electro-Pneumatic Elevator PLC Supervisor](../../../sources/electro-pneumatic-prototype-elevator-plc/STM.md)  |
| 195 | 🅿️ | EFSM | 🟡 | 🟡 | 🟡 | 🟢 | ✨ | 13 / 11 / 9 / 27 | [Two-layer lift-sliding parking access controller](../../../sources/five-parking-lifting-stereo-garage-s7-200/STM.md)  |
| 201 | 🌡️ | EFSM | 🟡 | 🟡 | 🟡 | 🟢 | ✨ | 4 / 6 / 2 / 6 | [SOC-Hysteresis Four-Mode Microgrid Power-Flow Supervisor](../../../sources/microgrid-power-flow-control-integrated-battery-management/STM.md)  |
| 237 | 🏭 | EFSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 6 / 9 / 4 / 9 | [Wall-painting machine lift-traverse sequence controller](../../../sources/automatic-wall-painting-machine-plc-cp1e-na20dr-a/STM.md)  |
| 055 | 🅿️ | EFSM | 🟠 | 🟢 | 🟠 | 🟡 | 🟢 | 5 / 5 / 5 / 9 | [Password-Gated Four-Slot Parking Controller](../../../sources/verilog-based-solution-for-multi-vehicle-parking/STM.md)  |
| 077 | 🅿️ | EFSM | 🟠 | 🟢 | 🟠 | 🟡 | 🟢 | 12 / 8 / 6 / 13 | [Guided-Entry Secure-Exit Parking Controller](../../../sources/intelligent-car-parking-management-system-on-fpga/STM.md)  |
| 218 | 🚆 | EFSM | 🟠 | 🟢 | 🟠 | 🟡 | 🟢 | 4 / 5 / 4 / 8 | [Constant-Warning Railway Crossing Counting Logic](../../../sources/standardization-of-logic-for-a-constant-warning-time-control-at-automatic-level-crossings/STM.md)  |
| 230 | ✈️ | EFSM | 🟠 | 🟢 | 🟠 | 🟡 | 🟢 | 5 / 8 / 9 / 8 | [Wait-bid-won-deliver-return UAV delivery controller](../../../sources/uav-delivery-unknown-heterogeneous-energy-storage/STM.md)  |
| 014 | ⚙️ | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 7 / 2 / 4 / 13 | [Three-lane obstacle-avoidance lane-change controller for ...](../../../sources/design-and-implementation-of-an-asynchronous-finite-state-controller-for-wheeled-mobile-robots/STM.md)  |
| 028 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 4 / 6 / 4 | [Four-state biological-torque supervisor for the powered h...](../../../sources/biomechanical-comparison-emg-biological-torque-hip-exoskeleton/STM.md)  |
| 029 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 2 / 2 / 8 / 2 | [Two-state shared-neural supervisor for the robotic knee-a...](../../../sources/robotic-knee-ankle-prosthesis-shared-neural-control/STM.md)  |
| 030 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 9 / 5 / 8 / 9 | [Slope-adaptive gait-phase supervisor for a powered transf...](../../../sources/control-framework-for-sloped-walking-powered-transfemoral-prosthesis/STM.md)  |
| 031 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 5 / 6 / 7 / 6 | [Phase-dependent virtual-muscle supervisor for the robotic...](../../../sources/bio-inspired-control-robotic-foot-ankle-prosthesis-level-walking-stair-ascent/STM.md)  |
| 032 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 4 / 5 / 4 | [Four-phase impedance controller for the pneumatically act...](../../../sources/design-and-control-of-a-pneumatically-actuated-transtibial-prosthesis/STM.md)  |
| 034 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 4 / 4 / 4 | [Four-mode gait controller for the powered transfemoral pr...](../../../sources/design-and-control-of-a-powered-transfemoral-prosthesis/STM.md)  |
| 035 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 20 / 20 / 12 / 20 | [Four-state impedance FSM for the powered knee-ankle prost...](../../../sources/configuring-powered-knee-ankle-prosthesis-five-ambulation-modes/STM.md)  |
| 039 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 6 / 5 / 4 | [Four-state walking controller for the semi-powered SCSA knee](../../../sources/semi-powered-stance-control-swing-assist-transfemoral-prosthesis/STM.md)  |
| 040 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 2 / 2 / 9 / 2 | [Stance-swing adaptive supervisor for the powered knee-ank...](../../../sources/adaptive-ambulation-powered-knee-ankle-prosthesis/STM.md)  |
| 042 | 🩺 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 2 / 2 / 8 / 2 | [Two-state stair-ascent supervisor for the adaptive powere...](../../../sources/adaptive-stair-climbing-powered-knee-ankle-prosthesis/STM.md)  |
| 062 | 🏭 | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 6 / 7 / 5 / 10 | [Photoelectric Height-Sorting Conveyor PLC Supervisor](../../../sources/automatic-sorting-conveyor-belt-plc/STM.md)  |
| 096 | 🌡️ | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 3 / 1 / 5 / 6 | [Three-state thermal/SoC balancing supervisor](../../../sources/battery-balancing-fsm-flyback-converters/STM.md)  |
| 099 | 🌡️ | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 7 / 3 / 13 / 38 | [Seven-state smart-charging power supervisor](../../../sources/smart-charging-architecture-power-quality-distribution/STM.md)  |
| 106 | ✈️ | EFSM | 🟡 | 🟡 | 🟢 | 🟡 | ✨ | 7 / 11 / 4 / 16 | [Soft/hard contingency safe mission manager](../../../sources/safe-mission-manager-unmanned-aircraft-systems/STM.md)  |
| 115 | 🅿️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 11 / 10 / 7 / 15 | [Underground Lift-Rotate-Push Parking Controller](../../../sources/sistem-otomasi-mesin-tempat-parkir-mobil-bawah-tanah/STM.md)  |
| 123 | 🌡️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 11 / 11 / 7 / 12 | [Tank-Level and Booster-Pump Distribution Supervisor](../../../sources/water-distribution-control-system-using-plc/STM.md)  |
| 146 | 🌡️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 9 / 10 / 4 / 14 | [Semi-Automatic Dam Gate Level Supervisor with Hoist Up/Do...](../../../sources/semi-automatic-dam-gate-plc-mini-hoist/STM.md)  |
| 148 | 🌡️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 8 / 12 / 9 / 14 | [Eight-step mine drainage pump supervisor](../../../sources/automation-of-water-drainage-systems-using-a-programmable-logic-controller-in-mining/STM.md)  |
| 156 | 🚗 | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 6 / 5 / 6 / 8 | [Traffic-Light-Aware Expected-Velocity Switching](../../../sources/integrated-decision-and-control-at-multi-lane-intersections-with-mixed-traffic-flow/STM.md)  |
| 164 | 🅿️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 14 / 11 / 7 / 18 | [Queued slot allocation and retrieval controller](../../../sources/plc-control-system-for-translation-motion-stereo-garage/STM.md)  |
| 189 | 🅿️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 6 / 7 / 5 / 10 | [Front-Rear Sensor Gate and Forced-Breakthrough Spike-Barr...](../../../sources/parking-gate-spike-barrier-microcontroller/STM.md)  |
| 217 | 🌡️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 7 / 8 / 6 / 8 | [Temperature-Regulated Ship Water-Supply Start-Work-Stop C...](../../../sources/ship-water-supply-automatic-control-plc/STM.md)  |
| 219 | 🅿️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 10 / 9 / 8 / 12 | [RFID-Guided Empty-Slot Entry Pipeline](../../../sources/sistem-parkir-pintar-berbasis-plc-rfid/STM.md)  |
| 221 | 🌡️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 7 / 7 / 11 / 8 | [Three-Tank Fluid Level Pump-and-Valve Controller](../../../sources/automatic-fluid-level-control-using-programmable-logic-controller/STM.md)  |
| 222 | 🌡️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 8 / 12 / 4 / 14 | [Eight-Step PLC Water Level and Pump Starter Controller](../../../sources/simulation-of-automatic-water-level-control-system-using-plc/STM.md)  |
| 228 | 🅿️ | EFSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 12 / 10 / 10 / 30 | [Four-mode parking-mode selector and path-generation contr...](../../../sources/versatile-mode-parking-system-fpga/STM.md)  |
| 235 | 🌡️ | EFSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 7 / 8 / 5 / 12 | [Water-level threshold dam-gate auto/manual controller](../../../sources/embedded-dam-gate-control-system-c-visual-basic/STM.md)  |
| 021 | 🩺 | EFSM | 🟠 | 🟢 | ⚪ | 🟡 | 🟢 | 6 / 5 / 10 / 8 | [Weight-shift walking supervisor for the pediatric lower-l...](../../../sources/size-adjustable-pediatric-lower-limb-exoskeleton-weight-shift/STM.md)  |
| 041 | 🩺 | EFSM | 🟠 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 4 / 7 / 4 | [Four-state walking controller for coordinated knee swing ...](../../../sources/controlling-knee-swing-initiation-and-ankle-plantarflexion-active-prosthesis/STM.md)  |
| 054 | 🌡️ | EFSM | 🟠 | 🟡 | 🟠 | 🟢 | 🟢 | 3 / 4 / 4 / 6 | [ADC-Threshold Pump Relay and LED Water-Tank FSM](../../../sources/intelligent-water-tank-automation-system-using-fpga-for-efficient-water-management/STM.md)  |
| 065 | 🌡️ | EFSM | 🟠 | 🟡 | 🟢 | 🟡 | 🟢 | 2 / 3 / 4 / 5 | [Dry-Wet Threshold Irrigation Pump FSM](../../../sources/enhancing-sustainable-farming-practices-through-fpga-technology/STM.md)  |
| 079 | 🚆 | EFSM | 🟠 | 🟡 | 🟠 | 🟢 | 🟢 | 7 / 6 / 5 / 9 | [Crossing-Gate and Obstacle-Broadcast Protection Controller](../../../sources/implementation-of-automatic-gate-control-for-railroad-switch-and-anti-collision/STM.md)  |
| 154 | 🅿️ | EFSM | 🟠 | 🟡 | 🟠 | 🟢 | 🟢 | 10 / 9 / 7 / 14 | [RFID Access, Floor Allocation, and Lift Return Cycle](../../../sources/automated-multi-storied-car-parking-system-using-rfid/STM.md)  |
| 161 | 🅿️ | EFSM | 🟠 | 🟡 | 🟠 | 🟢 | 🟢 | 8 / 7 / 4 / 11 | [Password-Gated Parking Gate and Slot Monitor](../../../sources/parking-monitoring-system-security-system-features/STM.md)  |
| 180 | 🏢 | EFSM | 🟠 | 🟡 | 🟠 | 🟢 | 🟢 | 7 / 7 / 4 / 22 | [Priority-Ordered Door-Alarm-and-Climate Home Controller](../../../sources/home-automation-system-hardware-descriptive-tools/STM.md)  |
| 182 | 🏢 | EFSM | 🟠 | 🟡 | 🟠 | 🟢 | 🟢 | 10 / 5 / 5 / 20 | [Sensor-Qualified Home Automation Process Controller](../../../sources/asm-robot-cyber-physical-home-automation-controller/STM.md)  |
| 206 | 🏭 | EFSM | 🟠 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 5 / 4 / 7 | [HMI-configurable count-based filling controller](../../../sources/product-filling-packaging-hmi-omron-plc/STM.md)  |
| 002 | 🌡️ | EFSM | 🟡 | 🟡 | ⚪ | 🟢 | 🟢 | 6 / 7 / 6 / 7 | [Head-Tank Elevation Valve Control](../../../sources/perencanaan-control-valve-pada-head-tank-plta-tulungagung-menggunakan-plc/STM.md)  |
| 053 | 🅿️ | EFSM | 🟡 | 🟡 | ⚪ | 🟢 | 🟢 | 3 / 4 / 8 / 4 | [Idle-Entry-Exit Slot-Monitoring Parking Controller](../../../sources/fpga-based-smart-parking-management-system-with-real-time-slot-monitoring-and-entry-exit-detection/STM.md)  |
| 088 | 🅿️ | EFSM | 🟡 | 🟡 | ⚪ | 🟢 | 🟢 | 8 / 8 / 8 / 12 | [Vacancy-Sensed Dual-Gate Parking Supervisor](../../../sources/automated-parking-system-using-plc-technology/STM.md)  |
| 136 | 🅿️ | EFSM | 🟡 | 🟢 | 🟠 | 🟠 | 🟢 | 3 / 5 / 5 / 6 | [Backing-Out Warning Module FSM](../../../sources/vision-based-parking-assistance-system-for-leaving-perpendicular-angle-parking-lots/STM.md)  |
| 137 | 🚆 | EFSM | 🟡 | 🟠 | 🟢 | 🟢 | 💎 | 7 / 8 / 13 / 11 | [Obstacle-Aware Railway Crossing Gate Supervisor](../../../sources/automated-railway-crossing-system-using-multi-sensor-integration/STM.md)  |
| 147 | 🅿️ | EFSM | 🟡 | 🟡 | ⚪ | 🟢 | 🟢 | 10 / 8 / 6 / 12 | [Entry-Storage-Retrieval parking controller](../../../sources/automatic-car-parking-using-plc/STM.md)  |
| 150 | 🅿️ | EFSM | 🟡 | 🟡 | ⚪ | 🟢 | 🟢 | 5 / 6 / 4 / 9 | [Multi-Area Entry-Exit Barrier and Full-Lot Supervisor](../../../sources/scada-multi-area-parking-system-plc-m221/STM.md)  |
| 214 | 🅿️ | EFSM | 🟡 | 🟠 | 🟢 | 🟢 | 💎 | 21 / 18 / 16 / 32 | [Automatic Parking Sequence with Manual/Fault Fallback](../../../sources/controller-development-multi-layer-parking-equipment-stm32/STM.md)  |
| 063 | 🏢 | EFSM | 🟠 | 🟡 | ⚪ | 🟢 | 🟢 | 2 / 2 / 2 / 4 | [PIR-and-Ultrasonic Sliding-Door Controller](../../../sources/automatic-door-controller-smart-building/STM.md)  |
| 095 | 🅿️ | EFSM | 🟠 | 🟡 | ⚪ | 🟢 | 🟢 | 2 / 7 / 4 / 8 | [Six-slot vertical parking setpoint controller](../../../sources/low-vertical-car-parking-automatic-control-system-using-programmable-logic-control/STM.md)  |
| 141 | 🅿️ | EFSM | 🟠 | 🟡 | ⚪ | 🟢 | 🟢 | 8 / 6 / 4 / 11 | [RFID-Validated Entry/Exit and Occupancy Counter Parking C...](../../../sources/arduino-multi-tiered-car-parking-unilag/STM.md)  |
| 168 | 🏭 | EFSM | 🟠 | 🟡 | ⚪ | 🟢 | 🟢 | 7 / 5 / 4 / 8 | [Laser-Triggered Vision-Verified Liquid Filling Controller](../../../sources/automated-liquid-filling-system-interactive-design-approach/STM.md)  |
| 173 | 🏢 | EFSM | 🟠 | 🟡 | ⚪ | 🟢 | 🟢 | 2 / 2 / 2 / 4 | [PIR-and-Ultrasonic Sliding-Door Controller](../../../sources/development-of-an-automatic-door-controller-for-a-smart-building/STM.md)  |
| 197 | 🌡️ | EFSM | 🟠 | 🟡 | ⚪ | 🟢 | 🟢 | 6 / 8 / 6 / 10 | [Moisture-threshold zone-valve irrigation controller](../../../sources/plc-based-automated-irrigation-system/STM.md)  |
| 211 | 🅿️ | EFSM | 🟠 | 🟡 | ⚪ | 🟢 | 🟢 | 4 / 6 / 5 / 6 | [Entry-gated slot occupancy parking controller](../../../sources/smart-car-parking-system-using-plc/STM.md)  |
| 023 | 🩺 | EFSM | 🟡 | 🟡 | 🟠 | 🟡 | 🟢 | 5 / 4 / 6 / 5 | [Gait-phase supervisory controller for the P.REX pediatric...](../../../sources/pediatric-knee-exoskeleton-adaptive-control-overground-walking/STM.md)  |
| 050 | 🚆 | EFSM | 🟡 | 🟠 | 🟡 | 🟢 | 🟢 | 6 / 6 / 3 / 10 | [Bidirectional Railway-Gate and Road-Signal Cycle](../../../sources/plc-based-traffic-light-control-with-automatic-railway-gate-crossing/STM.md)  |
| 056 | 🚆 | EFSM | 🟡 | 🟡 | 🟠 | 🟡 | 🟢 | 7 / 7 / 4 / 7 | [Pressure-Sensed 45° Hold Railway Gate Controller](../../../sources/pressure-sensed-fast-response-anti-collision-system-railway-gate-control/STM.md)  |
| 113 | 🏢 | EFSM | 🟡 | 🟠 | 🟡 | 🟢 | 🟢 | 7 / 11 / 5 / 14 | [Three-Stop Electro-Pneumatic Elevator Call-and-Door Contr...](../../../sources/electro-pneumatic-prototype-elevator-controlled-by-plc/STM.md)  |
| 144 | 🅿️ | EFSM | 🟡 | 🟡 | 🟠 | 🟡 | 🟢 | 8 / 9 / 7 / 14 | [PIN-Gated Empty-Slot Search and Slot-Recall Parking Contr...](../../../sources/hanging-rotary-parking-system-plc-hmi/STM.md)  |
| 236 | 🚆 | EFSM | 🟡 | 🟡 | 🟠 | 🟡 | 🟢 | 8 / 7 / 6 / 11 | [Sliding-plug train door close-and-reopen trap controller](../../../sources/door-design-control-system-high-speed-train-kcmp/STM.md)  |
| 110 | 🅿️ | EFSM | 🟠 | 🟡 | 🟠 | 🟡 | 🔘 | 3 / 4 / 4 / 5 | [Idle-wait-password parking gate supervisor](../../../sources/automatic-car-parking-system-verilog-hdl/STM.md)  |
| 187 | 🅿️ | EFSM | 🟠 | 🟡 | 🟠 | 🟡 | 🔘 | 4 / 3 / 5 / 7 | [Credential-Gated Multi-Slot Parking Access Controller](../../../sources/verilog-design-for-multi-car-parking-management-system/STM.md)  |
| 193 | 🚆 | EFSM | 🟠 | 🟠 | 🟡 | 🟢 | 🟢 | 5 / 3 / 6 / 14 | [Five-state sensor-gate-whistle railway interlocking super...](../../../sources/formal-verification-dependable-state-machine-hardware-architecture-safety-critical-cps/STM.md)  |
| 119 | 🅿️ | EFSM | 🟡 | 🟠 | 🟠 | 🟢 | 🟢 | 8 / 7 / 4 / 8 | [Rotate-lift-drop multilevel parking controller](../../../sources/plc-based-multilevel-automatic-car-parking-system/STM.md)  |
| 145 | 🅿️ | EFSM | 🟡 | 🟠 | 🟠 | 🟢 | 🟢 | 19 / 14 / 12 / 30 | [RFID-Guided Slot Assignment and Plat-Shuttle Parking Cont...](../../../sources/smart-parking-system-plc-rfid/STM.md)  |
| 216 | 🏭 | EFSM | 🟡 | 🟠 | 🟠 | 🟢 | 🟢 | 14 / 12 / 9 / 20 | [Distributed PLC Car-Wash Sequence with Pause/Cancel and W...](../../../sources/automatic-intelligent-car-washing-machine-plc/STM.md)  |
| 058 | 🚆 | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 6 / 5 / 7 / 7 | [Train-Arrival Gate Closure and Road-Signal Recovery Cycle](../../../sources/design-and-simulation-of-plc-iot-railway-level-crossing-gate-control-track-monitoring-system/STM.md)  |
| 080 | 🚆 | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 6 / 5 / 5 / 8 | [IR-Guided Obstacle-Checked Railway Crossing Controller](../../../sources/prevention-of-accidents-using-automated-railway-crossing-system/STM.md)  |
| 089 | 🚆 | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 5 / 6 / 4 / 6 | [Two-Sensor Railway Gate Close-Open Controller](../../../sources/involuntary-railway-crossing-controller/STM.md)  |
| 166 | ⚙️ | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 7 / 6 / 5 / 8 | [Ship-Triggered Barrier and Bridge Opening Cycle](../../../sources/plc-based-automatic-drawbridge-model/STM.md)  |
| 178 | 🏭 | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 9 / 12 / 8 / 14 | [Three-Axis Warehouse Store-and-Retrieve Controller](../../../sources/automatic-control-three-dimensional-warehouse-based-on-plc/STM.md)  |
| 188 | 🅿️ | EFSM | 🟠 | 🟡 | ⚪ | 🟡 | 🔘 | 6 / 8 / 7 / 10 | [RFID-Authenticated Entry and Slot-Occupancy Parking Contr...](../../../sources/smart-car-parking-system-rfid-iot/STM.md)  |
| 190 | 🌡️ | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 4 / 5 / 2 / 5 | [Two-Float Dam Gate Sequential Open-Close Controller](../../../sources/plc-based-automatic-dam-shutter-control/STM.md)  |
| 196 | ⚙️ | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 6 / 6 / 6 / 8 | [Ship-triggered bridge and barrier control cycle](../../../sources/automatic-bridge-control-for-ships-using-plc/STM.md)  |
| 208 | 🚆 | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 3 / 3 / 3 / 3 | [Sensor-triggered crossing controller with obstacle-stop G...](../../../sources/microcontroller-railway-crossing-track-obstacle-monitoring/STM.md)  |
| 220 | 🅿️ | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 9 / 10 / 8 / 11 | [Semicircular Multistoried Parking Lift-Pallet Controller](../../../sources/plc-based-automatic-multistoried-car-parking-system/STM.md)  |
| 238 | 🏢 | EFSM | 🟠 | 🟠 | 🟠 | 🟢 | 🟢 | 3 / 4 / 5 / 6 | [PIR-and-metal-gated automatic door controller](../../../sources/motion-based-automatic-door-opener-metal-detector/STM.md)  |
| 081 | 🏢 | EFSM | 🟡 | 🟠 | ⚪ | 🟢 | 🟢 | 16 / 12 / 12 / 25 | [Priority-Based Four-Floor Telescopic Elevator PLC Controller](../../../sources/electro-hydraulic-telescopic-elevator-plc-control/STM.md)  |
| 125 | 🅿️ | EFSM | 🟡 | 🟠 | ⚪ | 🟢 | 🟢 | 22 / 16 / 5 / 25 | [Crane-Combs Parking and Retrieval Sequence Controller](../../../sources/design-of-automated-parking-system-using-plc/STM.md)  |
| 048 | 🅿️ | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 9 / 8 / 5 / 12 | [Availability-Identification-Slot-Allotment Parking FSM](../../../sources/design-and-implementation-of-car-parking-system-on-fpga/STM.md)  |
| 060 | 🚆 | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 4 / 4 / 3 / 4 | [Two-Sensor Railway Gate Open-Close Controller](../../../sources/automatic-railway-gate-crossing-control-sensors-microcontroller/STM.md)  |
| 083 | 🌡️ | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 5 / 4 / 5 / 8 | [Dual-Float Dam Shutter Open-Close Cycle](../../../sources/self-regulating-water-management-system-using-programmable-logic-controller/STM.md)  |
| 092 | 🚆 | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 4 / 3 / 3 / 4 | [Arrival-limit-departure railway crossing gate controller](../../../sources/design-and-construction-of-automatic-railway-crossing-gate-control-omron-cp1e-e30-sdra-plc/STM.md)  |
| 112 | 🚆 | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 5 / 4 / 6 / 5 | [PIC railway gate arrival-close / departure-open controller](../../../sources/fabrication-of-automatic-railway-gate-controller/STM.md)  |
| 121 | 🏢 | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 8 / 10 / 10 / 20 | [Ten-Input Seven-Output Elevator LUT Controller](../../../sources/elevator-controller-based-on-ram-fpga/STM.md)  |
| 132 | 🚆 | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 4 / 4 / 4 / 4 | [IR-Sensed Railway Gate Close-and-Reopen Controller](../../../sources/automatic-railway-gate-control-system-using-plc/STM.md)  |
| 165 | 🚆 | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 4 / 4 / 5 / 4 | [Train-Arrival Gate Closure and Road-Signal Recovery Cycle](../../../sources/smart-railway-gate-level-crossing-system/STM.md)  |
| 199 | 🅿️ | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 12 / 8 / 18 / 29 | [Priority-aware parking-slot allocation and bar-gate contr...](../../../sources/smart-parking-spot-allocation-priority-verilog-hdl/STM.md)  |
| 212 | ⚙️ | EFSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 6 / 5 / 6 / 7 | [Ship-detected drawbridge opening and barrier controller](../../../sources/automation-of-drawbridge-model-using-plc/STM.md)  |
| 003 | 🏭 | EFSM | ⚪ | ⚪ | ⚪ | 🟢 | 🟢 | 5 / 5 / 0 / 5 | [Bottle Cleaning-Filling-Capping Line](../../../sources/development-of-automatic-packaging-system-using-plc-and-scada-for-industries/STM.md)  |

### FSM-basic （51 条）

| id | 领域 | 桶 | C1 | C2 | C3 | C4 | verdict | states/events/vars/trans | 案例 |
|---|---|---|---|---|---|---|---|---|---|
| 018 | ✈️ | FSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 6 / 8 / 8 / 12 | [Low-altitude mission-task FSM for target approach and thr...](../../../sources/autonomous-control-framework-unmanned-helicopter-low-altitude-flight/STM.md)  🎯 |
| 097 | ✈️ | FSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 6 / 6 / 5 / 10 | [Search-follow-catch mission controller](../../../sources/autonomous-aerial-robot-high-speed-search-intercept/STM.md)  🎯 |
| 194 | 🌡️ | FSM | 🟡 | 🟢 | 🟡 | 🟢 | 💎 | 18 / 9 / 6 / 30 | [Five-mode microgrid EMS switch-breaker supervisor](../../../sources/optimization-control-energy-management-system-microgrids/STM.md)  🎯 |
| 061 | 🚗 | FSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 5 / 8 / 14 / 11 | [Five-Mode Benefit-Evaluated Driving Supervisor](../../../sources/autonomous-driving-benefit-evaluation-fsm/STM.md)  🛡️ |
| 124 | ⚙️ | FSM | 🟡 | 🟢 | 🟠 | 🟢 | 💎 | 22 / 18 / 8 / 31 | [Excavation-Transport-Deposit Robot FSM](../../../sources/robot-excavation-geometrically-cohesive-granular-media/STM.md)  🛡️ |
| 227 | 🏭 | FSM | 🟡 | 🟡 | 🟢 | 🟢 | 💎 | 9 / 9 / 8 / 22 | [Pause-resume segmented-panel assembly process controller](../../../sources/sensor-guided-assembly-segmented-structures-industrial-robots/STM.md)  🛡️ |
| 013 | ⚙️ | FSM | 🟡 | 🟢 | ⚪ | 🟢 | 🟢 | 8 / 9 / 6 / 12 | [Stair-climbing mode manager for the decoupled delivery robot](../../../sources/a-robot-with-decoupled-mechanical-structure-and-adapted-state-machine-control-for-both-ground-and-staircase-situations/STM.md)  |
| 007 | ⚙️ | FSM | 🟠 | 🟡 | 🟡 | 🟢 | 🟢 | 5 / 10 / 4 / 11 | [Five-state exploration and recovery FSM for an air-duct r...](../../../sources/design-of-mobile-robot-for-air-ducts-exploration/STM.md)  |
| 233 | ⚙️ | FSM | 🟡 | 🟡 | 🟠 | 🟢 | 🟢 | 7 / 10 / 6 / 10 | [Seven-task distillation-column inspection supervisor](../../../sources/safety-critical-autonomous-inspection-distillation-columns/STM.md)  |
| 202 | 🏭 | FSM | 🟡 | 🟠 | 🟡 | 🟢 | 🟢 | 91 / 59 / 0 / 143 | [Modular Floor-and-Elevator Manufacturing Supervisor](../../../sources/modular-supervisory-control-multi-floor-manufacturing/STM.md)  |
| 129 | ✈️ | FSM | 🟡 | 🟢 | 🟡 | 🟡 | ✨ | 5 / 9 / 12 / 15 | [Five-mode UAV formation manager](../../../sources/multi-uavs-formation-autonomous-control-rqpso-fsm-dmpc/STM.md)  |
| 170 | 🚗 | FSM | 🟡 | 🟢 | 🟡 | 🟡 | ✨ | 5 / 7 / 6 / 7 | [Parking-lot exploration and collision-aware parking super...](../../../sources/hybrid-verification-technique-decision-making-self-driving-vehicles/STM.md)  |
| 171 | 🩺 | FSM | 🟢 | 🟢 | 🟠 | 🟡 | 💎 | 5 / 8 / 8 / 10 | [Human-led error-recovery co-grasp controller](../../../sources/error-recovery-wearable-robotic-co-grasping/STM.md)  |
| 192 | 🏢 | FSM | 🟠 | 🟠 | 🟡 | 🟢 | 🟢 | 5 / 5 / 0 / 8 | [Tile-pickup and placement arm FSM](../../../sources/floor-tiling-robotic-system/STM.md)  |
| 059 | 🏢 | FSM | 🟡 | 🟠 | ⚪ | 🟢 | 🟢 | 6 / 5 / 8 / 9 | [Four-Storey Request-Serving Elevator FSM](../../../sources/designing-an-elevator-controller-using-vhdl/STM.md)  |
| 109 | 🅿️ | FSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 5 / 7 / 8 / 7 | [Sensor-driven valet parking search-align-park controller](../../../sources/handsfree-valet-technology-hfvt/STM.md)  |
| 210 | 🚆 | FSM | ⚪ | 🟡 | ⚪ | 🟢 | 🟢 | 6 / 6 / 5 / 6 | [Vibration-sensed six-state crossing gate supervisor](../../../sources/next-gen-railway-crossings-iot-safety-control/STM.md)  |
| 226 | 🚗 | FSM | 🟡 | 🟢 | 🟠 | 🟡 | 🟢 | 7 / 12 / 10 / 11 | [Seven-state park-driving decision supervisor](../../../sources/low-speed-autonomous-vehicles-park-fsm/STM.md)  |
| 045 | 🚆 | FSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 5 / 5 / 8 / 14 | [Sensor1-Sensor2 Railway Crossing Safety Cycle](../../../sources/dependable-state-machine-hardware-architecture-railway-interlocking/STM.md)  |
| 072 | 🏭 | FSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 6 / 10 / 0 / 12 | [Six-State Screwing Cell Sequence Controller](../../../sources/implementation-of-finite-state-automata-for-6-axis-robot-in-the-screwing-process/STM.md)  |
| 085 | 🅿️ | FSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 5 / 9 / 5 | [Four-State Vision-Based Parking FSM](../../../sources/multisensor-based-environment-modelling-and-control-applications-for-mobile-robots/STM.md)  |
| 101 | ⚙️ | FSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 5 / 5 / 9 / 6 | [Row-following-turning-realignment navigation supervisor](../../../sources/optimized-autonomous-navigation-field-robots/STM.md)  |
| 126 | 🚗 | FSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 4 / 6 / 6 / 6 | [Four-State Highway Behavior-Planning FSM](../../../sources/hierarchical-framework-decision-making-trajectory-tracking-autonomous-vehicles/STM.md)  |
| 134 | ⚙️ | FSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 4 / 6 / 2 / 7 | [Buffer-Constrained Three-Apparatus Mealy Supervisor](../../../sources/supervisory-control-systems-state-machines-outputs/STM.md)  |
| 139 | ✈️ | FSM | 🟡 | 🟢 | ⚪ | 🟡 | 🟢 | 36 / 3 / 7 / 36 | [Wind-Maneuver Adaptive Tracking Parameter FSM](../../../sources/development-of-a-finite-state-machine-for-a-small-unmanned-aircraft-system-using-experimental-design/STM.md)  |
| 157 | 🚆 | FSM | 🟠 | 🟠 | ⚪ | 🟢 | 🔘 | 5 / 3 / 6 / 14 | [Five-state interlocking gate and alarm controller](../../../sources/railway-interlocking-nusmv-hardware-architecture/STM.md)  |
| 158 | 🏭 | FSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 6 / 10 / 0 / 12 | [Six-state robot screwing Mealy controller](../../../sources/six-axis-robot-screwing-finite-state-automata/STM.md)  |
| 177 | 🚆 | FSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 4 / 4 / 4 / 6 | [Two-Sensor Railway Gate Open-Close Controller](../../../sources/automation-of-railway-gate-control-using-microcontroller/STM.md)  |
| 223 | 🩺 | FSM | 🟠 | 🟠 | ⚪ | 🟢 | 🟢 | 4 / 4 / 0 / 4 | [Wait-wander-grasp-give assistive humanoid controller](../../../sources/reaching-and-grasping-glass-of-water-bci-controlled-humanoid-robot/STM.md)  |
| 103 | 🏭 | FSM | 🟡 | 🟡 | 🟠 | 🟡 | 🟢 | 6 / 8 / 5 / 8 | [Palletizing-handover-recovery collaborative arm supervisor](../../../sources/human-robot-collaborative-manufacturing-cell-learning-based-interaction/STM.md)  |
| 155 | 🚆 | FSM | ⚪ | 🟠 | ⚪ | 🟢 | 🔘 | 9 / 4 / 2 / 9 | [RF-Packet Crossing Warning and Gate Cycle](../../../sources/fpga-based-soc-for-railway-level-crossing-management-system/STM.md)  |
| 163 | 🏭 | FSM | 🟠 | 🟢 | ⚪ | 🟡 | 🟢 | 6 / 7 / 5 / 8 | [Swarm safe-lift and collective-transport controller](../../../sources/collective-transport-robot-swarms/STM.md)  |
| 175 | ✈️ | FSM | 🟡 | 🟠 | 🟢 | 🟡 | 🟢 | 7 / 12 / 12 / 16 | [Centralized Safety Monitor FSM](../../../sources/automated-contingency-management-in-unmanned-aircraft-systems/STM.md)  |
| 049 | 🚆 | FSM | 🟠 | 🟡 | 🟠 | 🟡 | 🔘 | 9 / 7 / 1 / 7 | [DFA-Based Gate Closing and Reopening Cycle](../../../sources/controlling-railway-gates-using-automata-based-intelligent-controller/STM.md)  |
| 186 | 🌡️ | FSM | 🟠 | 🟡 | 🟠 | 🟡 | 🔘 | 3 / 3 / 3 / 4 | [Threshold-Based Water Tank Pump Controller](../../../sources/intelligent-water-tank-automation-fpga/STM.md)  |
| 001 | 🏭 | FSM | 🟠 | 🟠 | 🟡 | 🟡 | 🔘 | 3 / 4 / 3 / 4 | [Three-state box fill FSM](../../../sources/plc-course-fsm/STM.md)  |
| 051 | 🏢 | FSM | 🟠 | 🟠 | 🟡 | 🟡 | 🔘 | 7 / 7 / 9 / 9 | [Three-Floor Automatic Elevator Floor-Transition FSM](../../../sources/automatic-elevator-controller/STM.md)  |
| 091 | 🏭 | FSM | 🟡 | 🟠 | 🟠 | 🟡 | 🔘 | 3 / 3 / 3 / 3 | [Rotate-Move-Avoid Forklift Navigation FSM](../../../sources/autonomous-forklift-navigation-cluttered-logistics-factory/STM.md)  |
| 140 | ✈️ | FSM | 🟡 | 🟢 | 🟡 | 🟠 | 🟢 | 3 / 6 / 6 / 11 | [Three-State Heuristic Stand-off Tracking FSM](../../../sources/feasibility-of-onboard-processing-of-heuristic-path-planning-and-navigation-algorithms-within-suas-autopilot-computational-constraints/STM.md)  |
| 149 | 🅿️ | FSM | 🟠 | 🟡 | ⚪ | 🟡 | 🔘 | 9 / 12 / 8 / 11 | [Parallel-parking search-enter-align supervisor](../../../sources/seva3d-autonomous-vehicles-parking-simulator-three-dimensional-environment/STM.md)  |
| 183 | 🏢 | FSM | 🟠 | 🟠 | 🟠 | 🟡 | 🔘 | 4 / 5 / 3 / 7 | [Four-State Keypad Home Entry Code Lock](../../../sources/fpga-application-of-home-security-code-using-verilog/STM.md)  |
| 047 | 🚗 | FSM | 🟡 | 🟢 | ⚪ | 🟠 | 🟢 | 4 / 8 / 8 / 8 | [Go-Yield-Try-Aware Regulatory-Signal FSM](../../../sources/maneuver-planner-for-automated-vehicles-on-urban-scenarios/STM.md)  |
| 064 | 🏢 | FSM | 🟠 | 🟠 | ⚪ | 🟡 | 🔘 | 6 / 3 / 3 / 11 | [Six-State Moore Elevator Motion Controller](../../../sources/finite-state-machine-untuk-pengendali-elevator-berbasis-fpga/STM.md)  |
| 076 | ⚙️ | FSM | 🟡 | 🟡 | 🟡 | 🟠 | 🟢 | 5 / 4 / 4 / 10 | [Context-Aware Behavior Executor for Dynamic UGV Navigation](../../../sources/using-perception-cues-for-context-aware-navigation-in-dynamic-outdoor-environments/STM.md)  |
| 078 | 🏢 | FSM | 🟠 | 🟠 | ⚪ | 🟡 | 🔘 | 7 / 7 / 2 / 14 | [Seven-State Three-Level Elevator Controller](../../../sources/design-and-implementation-of-efficient-elevator-control-system-using-fpga/STM.md)  |
| 131 | 🚦 | FSM | 🟠 | 🟠 | ⚪ | 🟡 | 🔘 | 12 / 4 / 4 / 16 | [Twelve-State Moore Traffic-Light Controller with Left-Tur...](../../../sources/conceptual-design-intelligent-traffic-light-controller/STM.md)  |
| 086 | 🚗 | FSM | 🟡 | 🟠 | 🟢 | 🟠 | 🟢 | 8 / 5 / 2 / 22 | [Multi-Phase Driving Maneuver DFA](../../../sources/real-time-decision-making-for-autonomous-city-vehicles/STM.md)  |
| 224 | 🏭 | FSM | 🟠 | ⚪ | 🟠 | 🟡 | 🔘 | 3 / 4 / 0 / 4 | [Fault-aware rotating-table manufacturing-cell controller](../../../sources/modular-supervisory-control-coordination-manufacturing-cell-observable-faults/STM.md)  |
| 046 | 🏢 | FSM | 🟡 | 🟠 | 🟠 | 🟠 | 🔘 | 3 / 8 / 7 / 8 | [Three-Floor Mealy Elevator Transition Controller](../../../sources/vlsi-elevator-control-finite-state-machine/STM.md)  |
| 130 | 🚗 | FSM | 🟡 | 🟠 | 🟠 | 🟠 | 🔘 | 4 / 4 / 4 / 10 | [MLCA four-state lane-change decision controller](../../../sources/mlca-minimizing-lane-changes-autonomous-vehicles/STM.md)  |
| 229 | 🏭 | FSM | 🟡 | ⚪ | 🟡 | 🟠 | 🔘 | 3 / 3 / 0 / 5 | [Three-mode AGV operation supervisor](../../../sources/industrial-agv-supervisory-control/STM.md)  |

