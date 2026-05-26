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

