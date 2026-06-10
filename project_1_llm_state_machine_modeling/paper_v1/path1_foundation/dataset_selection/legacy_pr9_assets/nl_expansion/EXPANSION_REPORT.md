# Path 1 候选 + 备选 NL 扩充报告（严格溯源）

> **任务定位**：把 SELECTION_REPORT 的 15 候选 + 15 备选 sample 的 STM.md §2 原 NL 描述扩充为 150-300 词的可追溯版本，作为 sprint 实验 A0_strong / A_full_ours 共同输入。
> **评测框架**：4 主维度 H/G/A/F + 2 综合 bd/ft = 6 axis_coverage 字段，对准 PATH1 selection 评分体系（[selection_screening/SELECTION_REPORT.md](../selection_screening/SELECTION_REPORT.md)）。
> **硬约束**：每条事实带 inline `[En]` marker + 1:1 配对的 provenance 数组；codex 严格读 paper.pdf + STM.md 后输出，禁止无中生有。

## 总览统计

- 30 个 sample（15 candidate + 15 backup）全部完成 ✅，0 失败、0 marker mismatch
- 词数：mean=266.3，min=234，max=289（范围 150-300）
- 平均 inline markers：17.4 / provenance entries：17.4（完美 1:1）
- marker mismatch（缺漏或孤立 provenance）：0/30

### 评测轴覆盖率（codex 自报『原文支持』比例，越高越好）

| 轴 | 支持 | 不支持 | 支持率 | 说明 |
|---|---:|---:|---:|---|
| H 层次 | 25 | 5 | 83% | 层次结构 hook（mode / sub-phase / 嵌套） |
| G 守卫算术 | 24 | 6 | 80% | 多变量算术 guard hook |
| A 动作 | 30 | 0 | 100% | 非平凡 action hook（变量赋值 / I/O / cross-cutting 监控） |
| F 故障恢复 | 22 | 8 | 73% | 全局应急 / safe-state / fail-safe hook |
| bd baseline-trap | 29 | 1 | 96% | baseline 失败模式综合（cross-section / implicit-domain / multivar / composite-internal / global） |
| ft fcstm-fit | 17 | 13 | 56% | pyfcstm 独占优势综合（深复合 init / SMT guard / forced+aspect / abstract action） |

### 桶 / 领域分布

- candidate / backup：15 / 15
- 桶（STM 类型）：{'HSM': 22, 'EFSM': 5, 'FSM': 3}
- 领域：{'⚙️': 6, '✈️': 10, '🌡️': 3, '🏭': 4, '🩺': 1, '🅿️': 2, '🚆': 1, '🚗': 2, '🏢': 1}

## 候选 Top 15

### #1 ⚙️ `amazing-race-robot-edition__01` (HSM)

- **case**: Ask-for-Directions Hierarchical Navigation Supervisor
- **统计**：265 词 / 11 markers / 11 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The supervisor controls a room-finding robot in an unknown single-floor building with no prior map or goal-location knowledge [E1]; it seeks a person, obtains spoken directions, follows them to the target hallway, and inspects door tags [E2]. The top-level FSM starts in WANDER, explores while detecting people, requests and interprets directions through speech synthesis and recognition, and enters FOLLOW DIRECTIONS only after dialogue yields a complete instruction set [E3]. Within WANDER, entry begins at MAKE DECISION, which checks registered-intersection context and available qualitative directions; when none are available, a recovery phase spins in place 360 degrees to update the quantitative and qualitative maps [E4]. Its exploration logic records hallway-trajectory visitation times, prefers unvisited trajectories, otherwise chooses the oldest visited one, and updates the selected trajectory before moving on [E5]. FOLLOW DIRECTIONS has a step counter initialized to the first plan step; forward actions drive until the specified intersection is detected, and left, right, or turn-around actions rotate 90 degrees, -90 degrees, or 180 degrees [E6]. For a forward-through-intersection action, the robot remains in motion until the intersection type changes and it has traveled at least 2 m from the rotation point; then the motion substate increments the step counter before returning to decision making [E7]. Failure recovery returns control to WANDER: top-level states have failure conditions that return to the initial state, and FOLLOW DIRECTIONS also returns to WANDER when a hallway-end 360-degree check still cannot find the specified intersection [E8]. The implementation uses a Husky platform with IMU, LiDAR, an Axis camera, ROS, speech I/O, and OCR over Axis-camera door-tag images [E9] [E10] [E11].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴由 [E4] 和 [E6] 覆盖：WANDER 进入后默认从 MAKE DECISION 开始并含 recovery phase，FOLLOW DIRECTIONS 以 step counter 初始化到第一 plan step 后进入 forward/rotate 等内部 phase。
- **G 守卫算术**：G 轴由 [E7] 覆盖：具名变量为 intersection type 与 distance from rotation point，自然语言复合条件是 intersection type changes AND distance >= 2 m；未额外发明其他阈值。
- **A 动作**：A 轴由 [E4]-[E7] 和 [E11] 覆盖：进入 recovery 时 360-degree spin，forward/rotate motion 执行，visitation time 更新，step counter increment，以及语音/OCR 等硬件相关动作。
- **F 故障恢复**：F 轴由 [E8] 覆盖：顶层状态有 failure conditions 返回 initial state，FOLLOW DIRECTIONS 在 hallway-end 360-degree check 后仍未找到指定 intersection 时返回 WANDER。
- **bd baseline-trap**：expanded_nl 命中 composite-internal（WANDER/FOLLOW DIRECTIONS 内部 phase，[E4][E6]）、implicit-domain（registered intersection/qualitative directions/hallway trajectories，[E4][E5]）和 multivar-guard（intersection type + 2 m，[E7]）等 baseline 失败模式。
- **ft fcstm-fit**：pyfcstm 适配点主要是 [E4]/[E6] 的复合 init 链、[E7] 的可转 SMT 复合守卫和 [E8] 的 forced-reset 风格回到 WANDER；abstract action 只在 [E9]-[E11] 的硬件 grounding 上有有限支撑。

</details>

<details><summary>provenance (11条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Introduction | paper_content.txt 行 59-65
    - quote: "we place the robot in an unknown environment, without a map... finding a door with a specified number on a single floor"
    - supports: unknown single-floor building, no prior map, specified door-number goal
- `[E2]` STM §1 摘录 A | paper.pdf p.1 Introduction | paper_content.txt 行 64-71
    - quote: "it must seek a person for assistance... follow these directions to reach the hallway... search for doors and read their door tags"
    - supports: seek a person, obtain directions, follow to hallway, inspect door tags
- `[E3]` STM §1 摘录 B | paper.pdf p.2 §II.B Architecture | paper_content.txt 行 163-183
    - quote: "the initial state is WANDER... detect and track people... speech synthesis and speech recognition... complete set of directions"
    - supports: top-level WANDER start, people detection, dialogue I/O, transition after complete directions
- `[E4]` STM §1 摘录 C | paper.pdf p.5 §III.A WANDER | paper_content.txt 行 443-453
    - quote: "WANDER enters the MAKE DECISION substate first... spin in place 360°. This substate helps to update the quantitative and qualitative maps"
    - supports: WANDER composite default substate and 360-degree recovery action
- `[E5]` STM §1 摘录 C | paper.pdf p.5 §III.A WANDER | paper_content.txt 行 471-482
    - quote: "maintain a visitation time... selects the oldest one... randomly selects one... updates the visitation time of the selected hallway trajectory"
    - supports: visitation-time variable, trajectory selection policy, visitation-time update
- `[E6]` STM §1 摘录 D | paper.pdf p.11-12 §III.D FOLLOW DIRECTIONS | paper_content.txt 行 1061-1090
    - quote: "maintains a step counter... initializing the step counter to the first step... left → 90°, right → −90°, and turn-around → 180°"
    - supports: FOLLOW DIRECTIONS internal counter, default plan step, forward and rotation actions
- `[E7]` STM §1 摘录 D | paper.pdf p.12 §III.D FOLLOW DIRECTIONS | paper_content.txt 行 1091-1099
    - quote: "requires that the intersection type change and the robot travel at least 2 m... they increment the step counter accordingly"
    - supports: compound numeric guard and step-counter transition action
- `[E8]` STM §1 摘录 B/D | paper.pdf p.2 §II.B and p.12 §III.D | paper_content.txt 行 165-168, 1149-1155
    - quote: "failure conditions which result in a transition to the initial state... indicates failure to carry out the plan and will return to the WANDER state"
    - supports: failure recovery to initial WANDER behavior
- `[E9]` paper.pdf p.2 §II.A Hardware and Software | paper_content.txt 行 135-141
    - quote: "Clearpath Husky A200 UGV equipped with an Open IMU UM7, Velodyne VLP-16 3D LiDAR, Axis M5525-E PTZ Camera"
    - supports: Husky platform, IMU, LiDAR, Axis camera hardware
- `[E10]` paper.pdf p.2 §II.A Hardware and Software | paper_content.txt 行 142-146
    - quote: "using ROS Kinetic as the communication framework... SLAM from data from the IMU and 3D LiDAR"
    - supports: ROS communication and IMU/LiDAR SLAM grounding
- `[E11]` paper.pdf p.2 §II.A Hardware and Software | paper_content.txt 行 147-157
    - quote: "record speech with the Blue Yeti microphone... synthesize speech through the laptop speaker... door tags taken with the Axis camera"
    - supports: speech input/output and OCR over Axis-camera door-tag images

</details>

- **intentional omissions**：未加入 emergency stop、safe-state 或任意子状态强制中止，因为原文只支持失败返回 initial/WANDER。未加入具体阀门/电机编号、人物检测置信度或额外传感器阈值，因为原文没有给这些控制模型事实。

### #2 ✈️ `autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle__01` (HSM)

- **case**: Building-interior firefighting mission supervisor
- **统计**：278 词 / 18 markers / 18 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The mission supervisor is a FlexBE hierarchical state machine in ROS that interconnects MAV subsystems and contains nested lower-level state machines [E1] [E2] [E3]. It first verifies key parts, calls automatic takeoff only after every component is operational, then runs outdoor and indoor phases before returning home and landing [E4] [E5]. In outdoor phase, 2D LIDAR scans form a virtual bumper against plans closer than a predefined safe distance, and the MAV flies along the building at a predefined distance and heading while searching for windows [E6] [E7]. When a window is located, it stops wall-following, moves to 2 m from the window center, switches to indoor flying localization, and retries flythrough until success or maximum allowed flight time triggers automatic landing [E8] [E9]. The flythrough submachine faces the window, hovers to stabilize, waits for an updated window estimate, then flies through the center to a goal behind the window at constant altitude [E10]. If that estimate is lost during flythrough while the MAV remains outside, Escaping returns it to the original hover point [E11]. Any state outcome meaning the MAV cannot continue also calls a landing event [E12]. Indoors, exploration and fire detection send the MAV to a validated fire position 1.5 m in front of the target before extinguishing [E13]. Its effector is a water bag and pump driving water through a front nozzle; spraying is active only in the drifting state and disabled outside the outer range [E14] [E15]. If the fire is lost, exploration resumes [E16]; otherwise the MAV depletes its water, treats all-water-depleted as completion [E17], exits through the same window, switches back to outdoor localization, and lands at the start position [E18].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用 FlexBE HSM、nested lower-level state machines、outdoor/indoor phase 和 flythrough submachine 暴露层次结构，并用主流程先 verification、flythrough 先 hover/wait 作为原文支持的 init 线索 [E1][E2][E3][E4][E5][E10]。
- **G 守卫算术**：G 钩子集中在 predefined safe distance、2 m window-center distance、maximum allowed flight time、estimate lost 且仍在室外、1.5 m fire standoff、outer range spraying-disable 这些具名变量/自然复合条件 [E6][E8][E9][E11][E13][E15]。
- **A 动作**：A 钩子包括 verify 后 automatic takeoff、localization mode switch、hover/wait/flythrough、pump/nozzle spraying、water depletion completion、exit and land 等非平凡动作 [E4][E8][E10][E14][E15][E17][E18]。
- **F 故障恢复**：F 钩子包括 window estimate 丢失时进入 Escaping 回到原 hover 点、最大飞行时间自动 landing、以及任何 state 不能继续时的全局 landing event [E9][E11][E12]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain（MAV/FlexBE/GNSS/LIDAR）、implicit-action-prose（动作散落叙述）、multivar-guard（estimate lost AND still outside）、composite-internal（flythrough submachine）和 global-cross-cutting（any-state landing）等 baseline 失败模式 [E1][E6][E10][E11][E12]。
- **ft fcstm-fit**：pyfcstm 适配点主要是深复合 HSM 与子机初始行为、数值/复合守卫、forced/global landing 语义，以及 pump/nozzle/water-spraying 这类 effector-agnostic abstract action；未强行加入 per-tick aspect [E1][E3][E6][E8][E11][E12][E14][E15]。

</details>

<details><summary>provenance (18条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.10 §F High-Level Behavior Control | paper_content.txt 行 905-908
    - quote: "constructed as a hierarchical state machine, which is used for interconnecting all the subsystems"
    - supports: hierarchical state machine; interconnects MAV subsystems
- `[E2]` STM §1 摘录 A | paper.pdf p.10 §F High-Level Behavior Control | paper_content.txt 行 910-912
    - quote: "The hierarchical state machine is implemented using the Flexbe library [40], and it is fully integrated into the designed ROS framework."
    - supports: FlexBE implementation and ROS integration
- `[E3]` STM §1 摘录 A | paper.pdf p.10 §F High-Level Behavior Control | paper_content.txt 行 913-916
    - quote: "the nested lower-level state machines are visualized as double-outline rectangles"
    - supports: nested lower-level state machines
- `[E4]` STM §1 摘录 A | paper.pdf p.10 §F High-Level Behavior Control | paper_content.txt 行 928-932
    - quote: "In the first step, the correct performance of all key parts of the system is checked. When every component is verified to be operational, an automatic takeoff is called."
    - supports: verify key parts; automatic takeoff only after components are operational
- `[E5]` STM §1 摘录 A | paper.pdf p.10 §F High-Level Behavior Control | paper_content.txt 行 932-939
    - quote: "The mission is divided into two parts: the outdoor phase and the indoor phase... the MAV flies back to the home position and lands."
    - supports: outdoor/indoor phases; return-home landing
- `[E6]` paper.pdf p.10 §F Outdoor phase | paper_content.txt 行 949-956
    - quote: "These scans... are used in a virtual bumper... prevents the MAV from following a plan... closer than the predefined safe distance."
    - supports: 2D LIDAR virtual bumper and predefined safe-distance guard
- `[E7]` STM §1 摘录 B | paper.pdf p.10 §F Outdoor phase | paper_content.txt 行 960-963
    - quote: "the MAV starts flying alongside the building at a predefined distance with a heading towards the building, and begins the window detection mechanism."
    - supports: wall-following at predefined distance and heading while detecting windows
- `[E8]` STM §1 摘录 B | paper.pdf p.10-11 §F Outdoor phase | paper_content.txt 行 963-973
    - quote: "the MAV stops flying alongside the building... flies in front of the window to distance of 2 m... localization... switched to indoor flying mode"
    - supports: stop wall-following; move 2 m from window center; switch to indoor localization
- `[E9]` STM §1 摘录 B | paper.pdf p.11 §F Outdoor phase | paper_content.txt 行 974-984
    - quote: "The attempts can be repeated until the maximum allowed flight time is reached. After reaching this time, the MAV automatically lands."
    - supports: retry flythrough until maximum flight time; automatic landing
- `[E10]` STM §1 摘录 C | paper.pdf p.11-12 §F Window flythrough | paper_content.txt 行 985-1005
    - quote: "hovers in front of the center of the window to stabilize itself... waits for an up-to-date window estimate... maintaining a constant altitude"
    - supports: flythrough submachine sequence: hover, wait for updated estimate, fly through at constant altitude
- `[E11]` STM §1 摘录 C | paper.pdf p.12 §F Window flythrough | paper_content.txt 行 1004-1009
    - quote: "If the window estimate is lost... the state machine switches to the Escaping state and the MAV returns to its original hovering position"
    - supports: estimate-lost-and-still-outside recovery through Escaping
- `[E12]` paper.pdf p.10 §F High-Level Behavior Control | paper_content.txt 行 920-922
    - quote: "A landing event is called whenever any state produces an outcome that means that the MAV cannot continue its mission."
    - supports: global landing event from any state that cannot continue
- `[E13]` paper.pdf p.9 §E Fire Extinguishing | paper_content.txt 行 856-863
    - quote: "Upon obtaining the first validated fire detection state... the MAV is sent to a position... 1.5 m in front... handed over to the fire-extinguishing subsystem."
    - supports: validated fire detection leads to a 1.5 m target position before extinguishing
- `[E14]` paper.pdf p.13 Platform Description | paper_content.txt 行 1143-1151
    - quote: "To extinguish fires, the MAV is equipped with a water bag and a pump... The pump drives the water through a nozzle"
    - supports: water bag, pump, and front-nozzle effector
- `[E15]` paper.pdf p.10 §E Fire Extinguishing | paper_content.txt 行 887-904
    - quote: "Water spraying is only activated when the MAV is in this drifting state... outside the outer ranges... water spraying is disabled."
    - supports: spraying active only in drifting state and disabled outside outer range
- `[E16]` STM §1 摘录 D | paper.pdf p.12 §F Indoor phase | paper_content.txt 行 1020-1021
    - quote: "In the case that the fire is lost, the MAV starts exploring again."
    - supports: fire lost causes exploration to resume
- `[E17]` STM §1 摘录 D | paper.pdf p.12 §F Indoor phase | paper_content.txt 行 1015-1020
    - quote: "If the fire target is not lost, the MAV depletes all the water... extinguishing is therefore declared completed once all the water is depleted."
    - supports: not-lost fire target; water depletion as completion
- `[E18]` STM §1 摘录 D | paper.pdf p.12 §F Indoor phase | paper_content.txt 行 1021-1028
    - quote: "the MAV flies back in front of the window that it entered through... localization... switched to outdoor flying again and MAV flies back to land"
    - supports: exit through same window; switch outdoor localization; land at start position

</details>

- **intentional omissions**：没有加入阀门编号、紧急停止按钮、传感器型号、显式最大飞行时间数值或额外 safe-state 名称，因为 STM §1 与相关 PDF 段落没有支撑。也没有把“灭火是否成功”写成反馈 guard，因为原文明说 MAV 无法识别喷洒液体是否足以灭火。

### #3 ⚙️ `autonomous-navigation-framework-holonomic-mobile-robots-agriculture__01` (HSM)

- **case**: Greenhouse row-inspection navigation supervisor
- **统计**：250 词 / 19 markers / 19 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The greenhouse navigation supervisor coordinates a mobile robot that uses heating-system rails inside crop rows, a single stereo camera for perception, LiDAR for distance measurements, and an FSM to automate the sequence of inspection actions [E1] [E2]. At the top level it starts in WAIT_FOR_GOAL, where initialization acquires the occupancy grid map and the mission instructions that name the rows to inspect, then configures localization and the action sequence for the mission [E3] [E4] [E5]. When a mission is provided, the controller enters the PLAN_EXEC block and uses the TEB local planner for headland planning, while a real-time local costmap updated from laser-scanner input supports collision-free trajectories [E6] [E7]. After PLAN_EXEC succeeds, VISUAL_SERVOING starts the in-row process with TARGET_ALIGNMENT before any forward rail traversal; this phase combines semantic segmentation with stereo depth and computes optical velocity and steering commands for rail alignment [E8] [E9] [E10] [E11]. TARGET_ALIGNMENT continues until the robot’s angular, lateral, and longitudinal divergence from the selected rail midpoint are all approximately zero [E12] [E13]. Once on the rails, in-row motion is constrained to forward/backward linear-x commands, and other velocity instructions are disregarded [E14] [E15]. The robot then iterates through forward traversal, inspection, and backward traversal until row targets are completed; negative linear velocity commands return it toward the row start, and semantic detection of row endpoints terminates rail navigation [E9] [E16] [E17]. Completion returns the FSM to WAIT_FOR_GOAL, while any failure anywhere in the operation enters a common invalid/aborted/failure outcome and then returns to initialization [E18] [E19].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用 WAIT_FOR_GOAL、PLAN_EXEC、VISUAL_SERVOING 和进入 VISUAL_SERVOING 后先执行 TARGET_ALIGNMENT 暴露了顶层 mode 与子相位 init 关系，主要依据 [E3] [E6] [E8] [E9]。
- **G 守卫算术**：G 钩子来自 TARGET_ALIGNMENT 中 dθ、dy、dx 三个变量全部约为零的复合自然语言守卫，另有 row endpoints 触发 rail-navigation 终止；原文未给具体数值阈值，依据 [E12] [E13] [E17]。
- **A 动作**：A 钩子体现在 TEB/costmap 生成导航轨迹、alignment 计算 velocity/steering commands、rail navigation 丢弃非 linear-x 命令并用 negative linear velocity 回退，依据 [E7] [E10] [E11] [E15] [E16]。
- **F 故障恢复**：F 钩子明确存在：任何 operation 中的 failure 都进入 common invalid/aborted/failure outcome 并回初始化，正常完成则回 WAIT_FOR_GOAL，依据 [E18] [E19]。
- **bd baseline-trap**：expanded_nl 同时命中 composite-internal（VISUAL_SERVOING 内 TARGET_ALIGNMENT 与迭代子状态）、multivar-guard（dθ/dy/dx 近零）、implicit-action-prose（速度与规划动作散写）和 global-cross-cutting（any failure），依据 [E8] [E9] [E12] [E13] [E19]。
- **ft fcstm-fit**：pyfcstm 适配点中等偏强：有复合 init/子相位链 [E8] [E9]、多变量 SMT 风格 guard [E12] [E13]、全局 failure reset [E19]，以及可抽象为平台无关 action 的 velocity/steering command [E11]；但原文不支持 per-tick aspect 或具名硬件 actuator。

</details>

<details><summary>provenance (19条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 50-52
    - quote: "utilizes the heating system rails to navigate through the crop rows using a single stereo camera for perception and a LiDAR sensor for accurate distance measurements."
    - supports: heating-system rails, crop rows, stereo camera, and LiDAR distance measurements
- `[E2]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 52-53
    - quote: "A finite state machine orchestrates the sequence of required actions, enabling fully automated task execution."
    - supports: FSM automates the sequence of inspection actions
- `[E3]` STM §1 摘录 C | paper.pdf p.10 §3.4 / Figure 8 | paper_content.txt 行 421-422
    - quote: "The robot initialization is equivalent to the WAIT_FOR_GOAL state."
    - supports: top-level start in WAIT_FOR_GOAL
- `[E4]` STM §1 摘录 B | paper.pdf p.9 §3.4 | paper_content.txt 行 395-397
    - quote: "acquisition of both the greenhouse occupancy grid map and the user’s mission instructions, which specify the rows to be inspected."
    - supports: initialization acquires occupancy grid and row mission
- `[E5]` paper.pdf p.9 §3.4 | paper_content.txt 行 397-399
    - quote: "configuration of crucial operational components such as localization and the determination of the action sequence required to complete the designated mission."
    - supports: initialization configures localization and action sequence
- `[E6]` STM §1 摘录 C | paper.pdf p.10 §3.4 / Figure 8 | paper_content.txt 行 421-423
    - quote: "there is a transition to the PLAN_EXEC block, which contains the headland planning that is performed by the Timed Elastic Band (TEB) Local Planner."
    - supports: mission transition to PLAN_EXEC and TEB headland planning
- `[E7]` paper.pdf p.11 §3.5 | paper_content.txt 行 446-449
    - quote: "The local planner operates on a local costmap that updates in real-time with the input from the laser scanners and provides accurate, collision-free trajectories."
    - supports: real-time costmap, laser-scanner input, collision-free trajectories
- `[E8]` STM §1 摘录 C | paper.pdf p.10 §3.4 / Figure 8 | paper_content.txt 行 424-425
    - quote: "When that block finishes successfully, there is a transition to the VISUAL_SERVOING block, which is responsible for the in-row processes."
    - supports: PLAN_EXEC success leads to VISUAL_SERVOING
- `[E9]` STM §1 摘录 D | paper.pdf p.10 §3.4 / Figure 8 | paper_content.txt 行 425-427
    - quote: "the robot performs the TARGET_ALIGNMENT phase once, followed by an iterative process between the states TRAVERSE_FORWARD, INSPECT and TRAVERSE_BACKWARD."
    - supports: TARGET_ALIGNMENT as first in-row phase and later forward/inspect/backward iteration
- `[E10]` paper.pdf p.11 §3.6 | paper_content.txt 行 461-465
    - quote: "integration of the outcomes of semantic segmentation with the depth data obtained from the stereo camera system."
    - supports: semantic segmentation combined with stereo depth
- `[E11]` paper.pdf p.11 §3.6 | paper_content.txt 行 458-460
    - quote: "to calculate the optical velocity and steering commands that will align the robot precisely with the rails."
    - supports: computed optical velocity and steering commands for rail alignment
- `[E12]` paper.pdf p.12 §3.6 | paper_content.txt 行 519-523
    - quote: "At each timestep the robot calculates its divergence from pmiddle, which is expressed as dθ, dy and dx."
    - supports: angular, lateral, and longitudinal divergence variables
- `[E13]` paper.pdf p.12-p.13 §3.6 Equation (6) | paper_content.txt 行 525-529
    - quote: "dθ ≈ 0; dy ≈ 0; dx ≈ 0."
    - supports: compound approximately-zero alignment guard
- `[E14]` paper.pdf p.13 §3.7 | paper_content.txt 行 549-552
    - quote: "the mobility of the robot is constrained to only two directions: forward and backward."
    - supports: in-row motion constrained to forward/backward
- `[E15]` paper.pdf p.13 §3.7 | paper_content.txt 行 551-554
    - quote: "velocity that do not belong to the linear x-axis are deemed inconsequential and swiftly disregarded."
    - supports: non-linear-x velocity instructions are disregarded
- `[E16]` paper.pdf p.13 §3.7 | paper_content.txt 行 559-562
    - quote: "The provision of negative linear velocity commands to the robot controller serves the purpose of directing the robot towards the initial point of the row."
    - supports: negative linear velocity returns robot toward row start
- `[E17]` paper.pdf p.13 §3.7 | paper_content.txt 行 563-565
    - quote: "termination of backward movement, and rail navigation in general, is triggered when the robot’s field of view encompasses the endpoints of the rows."
    - supports: row endpoint detection terminates rail navigation
- `[E18]` STM §1 摘录 D | paper.pdf p.10 §3.4 / Figure 8 | paper_content.txt 行 427-428
    - quote: "When the in-row task is completed, the FSM returns to the WAIT_FOR_GOAL state again."
    - supports: normal completion returns to WAIT_FOR_GOAL
- `[E19]` STM §1 摘录 D | paper.pdf p.10 §3.4 / Figure 8 | paper_content.txt 行 428-430
    - quote: "any failure that may occur throughout the entire operation returns to a common state, which is reported as invalid, aborted, or a failure, and then to the initialization state."
    - supports: global failure path through common outcome back to initialization

</details>

- **intentional omissions**：未加入具体阈值、速度大小、motor/valve 编号、emergency-stop safe mode 或 watchdog/aspect，因为原文没有这些事实支撑。也没有展开全部 state name、projection equations 或完整传感器表，避免把 NL 变成伪代码或 state 枚举。

### #4 🌡️ `control-system-design-of-water-filter-test-bench__01` (HSM)

- **case**: Water-filter test-bench main-state and valve supervisor
- **统计**：269 词 / 24 markers / 24 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The water-filter test-bench controller is modelled with UML state machines, and its main states decide which HMI actuations and sensor/state data are available [E1] [E2]. At the top level, Normal is the basic state, the selectable modes are ISO 16689 ΔP measurement, ISO 3968 multi-pass measurement, and manual control, and power-up puts components in their initial states [E3] [E4] [E5]. Stop route E.1 is global: it triggers when parameters leave allowed limits or emergency stop is pressed, and it can be entered from every state [E6] [E7]. In ΔP measurement, entering Lobby1 sets valves to ΔP initial positions and enables B.PM.2, B.TV.1/B.TV2, B.V.12 cleaning, and test-filter bypass controls [E8] [E9]. In multi-pass measurement, entering the mode activates Lobby2 and initial multi-pass valve positions; the test starts only when A.PM.1, B.PM.1, B.PM.3, and A.PM.2 are on, sensor pumps are off, A.V.2 is right, B.V.12 is left, and bypass is active, then sensor pumps and needed counters start and gather data [E10] [E11] [E12]. The test stops on completion, stop2, automatic stop1, or safety stop2; those stop cases halt every pump and measuring event, route the system to Lobby3 for diagnosis, safety stop2 forbids pump use, and reset leaves stop states only after parameters or pressure normalize and emergency stop is not pressed [E13] [E14] [E15] [E16] [E17] [E18] [E19]. A.V.1 starts left and can turn right in Lobby3 only when reservoir B.W.1 is not full and the A.V.1 button is pressed, or when the multi-pass start guard holds [E20] [E21]. Bypass supervision keeps B.V.10 and B.V.11 synchronous, using combined valve/pump guards and delay guards before redirecting flow [E22] [E23] [E24].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用 Normal 顶层主状态、ISO 16689/ISO 3968/manual control 模式、Lobby1/Lobby2 进入语义和 power-up 初始状态暴露层次与 init 线索，见 [E3] [E4] [E5] [E8] [E10]。
- **G 守卫算术**：G 钩子主要是 allowed-limit/critical-limit 型阈值守卫和多变量复合守卫：E.1 的参数越界或急停 [E6]、multi-pass 的泵/阀/旁路组合条件 [E11]、A.V.1 的 B.W.1 未满且按钮按下 [E20]、B.V.10/B.V.11 的阀泵组合守卫 [E23]；原文未给具体数字阈值。
- **A 动作**：A 钩子包括 power-up 设置初始状态 [E5]、进入 Lobby1/Lobby2 设置阀门初始位置 [E8] [E10]、multi-pass 启动传感泵和计数器 [E12]、stop 停全部泵和测量事件 [E14]、旁路延迟守卫引导执行顺序 [E24]。
- **F 故障恢复**：F 钩子由 E.1 从任意状态进入的全局 stop [E6] [E7]、automatic stop1/safety stop2 的停泵与 Lobby3 诊断路径 [E13] [E14] [E15] [E16] [E17]、以及 reset 恢复条件 [E18] [E19] 支撑。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拆段、implicit-domain 工业术语、multivar-guard 和 global-cross-cutting：主状态在 §4.5.2、阀监督在 §4.5.3、stop/recovery 在 §4.5.5，关键点见 [E6] [E7] [E11] [E20] [E23] [E24]。
- **ft fcstm-fit**：pyfcstm 适配主要落在复合模式/init 线索 [E3] [E5] [E8] [E10]、多变量 SMT 风格守卫 [E11] [E20] [E23]、forced/global stop [E6] [E7]，以及阀/泵/计数器等 abstract action effector 解耦 [E9] [E12] [E14] [E22]；原文没有每 tick aspect，未强行补写。

</details>

<details><summary>provenance (24条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 45-50
    - quote: "The control system was modelled in Unified Modelling Language’s state machine diagrams"
    - supports: controller is modelled with UML state machines
- `[E2]` STM §1 摘录 A | paper.pdf p.1-2 Abstract | paper_content.txt 行 53-62
    - quote: "These states defined which of the components could be actuated during each state and which sensor/state data would be shown to the user"
    - supports: main states decide HMI actuations and sensor/state data
- `[E3]` STM §1 摘录 B | paper.pdf p.34 §4.5.2 | paper_content.txt 行 1080-1082
    - quote: "Normal state is the basic state of the system."
    - supports: Normal is the basic top-level state
- `[E4]` STM §1 摘录 B | paper.pdf p.34 §4.5.2 | paper_content.txt 行 1081-1084
    - quote: "Options are two different measuring states ISO 16689 and ISO 3968 and a manual control state."
    - supports: selectable modes are ISO 16689, ISO 3968, and manual control
- `[E5]` STM §1 摘录 B | paper.pdf p.34 §4.5.2 | paper_content.txt 行 1090-1091
    - quote: "When the power is turned on to the system the components are set into their initial states"
    - supports: power-up puts components in initial states
- `[E6]` STM §1 摘录 B | paper.pdf p.34 §4.5.2 | paper_content.txt 行 1092-1094
    - quote: "triggers when system parameters are over or under their allowed limits or when the emergency stop is pressed"
    - supports: E.1 trigger conditions
- `[E7]` STM §1 摘录 B | paper.pdf p.34 §4.5.2 | paper_content.txt 行 1094-1095
    - quote: "E.1 can be entered from every state of the system."
    - supports: global stop route from every state
- `[E8]` STM §1 摘录 B | paper.pdf p.35 §4.5.2 | paper_content.txt 行 1104-1106
    - quote: "When the state is entered, valves are set into initial states suited for the ΔP measurement."
    - supports: Lobby1 entry sets ΔP valve initials
- `[E9]` STM §1 摘录 B | paper.pdf p.35 §4.5.2 | paper_content.txt 行 1106-1108
    - quote: "In lobby1 a user can control pump B.PM.2, Throttle valves B.TV.1 and B.TV2, valve B.V.12 for cleaning the system and test filter bypass."
    - supports: Lobby1 available controls
- `[E10]` STM §1 摘录 B | paper.pdf p.36 §4.5.2 | paper_content.txt 行 1119-1122
    - quote: "When the state is entered, a lobby2 state becomes active and systems valves are set into their initial multi-pass states."
    - supports: multi-pass entry activates Lobby2 and initializes valves
- `[E11]` STM §1 摘录 B | paper.pdf p.36 §4.5.2 | paper_content.txt 行 1126-1128
    - quote: "pumps A.PM.1, B.PM.1, B.PM.3 and A.PM.2 has to be on, sensor pumps must be off, valve A.V.2 must be right, valve B.V.12 must be left and bypass must be active"
    - supports: multi-pass start compound guard
- `[E12]` paper.pdf p.36 §4.5.2 | paper_content.txt 行 1132-1134
    - quote: "sensor pumps are turned on and all the needed counters for the multi-pass test are turned on and their data are being gathered"
    - supports: multi-pass start actions for sensor pumps and counters
- `[E13]` paper.pdf p.36 §4.5.2 | paper_content.txt 行 1137-1138
    - quote: "The test ends when the test is finished, when stop2 is pressed or when automatic stop1 state or safety stop2 becomes active."
    - supports: test stop triggers
- `[E14]` paper.pdf p.36 §4.5.2 | paper_content.txt 行 1138-1139
    - quote: "Last three of the four options mentioned will stop every pump of the system and also ends the measuring event."
    - supports: stop cases halt pumps and measuring
- `[E15]` STM §1 摘录 B | paper.pdf p.36 §4.5.2 | paper_content.txt 行 1147-1151
    - quote: "lobby3 is also entered when automatic stop1 or safety stop2 state becomes active."
    - supports: stop cases route to Lobby3
- `[E16]` paper.pdf p.36-37 §4.5.2 | paper_content.txt 行 1151-1158
    - quote: "by entering the manual control state, the user can identify the problem"
    - supports: manual-control diagnosis purpose
- `[E17]` STM §1 摘录 B | paper.pdf p.37 §4.5.2 | paper_content.txt 行 1163-1164
    - quote: "when safety stop2 is active, pumps cannot be used because system’s pressure is dangerously high or emergency stop is pressed."
    - supports: safety stop2 forbids pump use
- `[E18]` paper.pdf p.59 §4.5.5 | paper_content.txt 行 1577-1582
    - quote: "This automatic stop state can be left when system parameters are back to normal and reset is pressed."
    - supports: automatic stop recovery by reset after parameters normalize
- `[E19]` paper.pdf p.60 §4.5.5 | paper_content.txt 行 1591-1596
    - quote: "reset must be pressed while the system’s pressure is normalized and emergency stop is not pressed."
    - supports: safety stop recovery by reset after pressure normalizes and emergency stop clears
- `[E20]` STM §1 摘录 C | paper.pdf p.38 §4.5.3 | paper_content.txt 行 1200-1202
    - quote: "Its initial state is left. It can be turned to right in manual control lobby3 if reservoir B.W.1 is not full and a button A.V.1 is pressed."
    - supports: A.V.1 initial state and manual-control guard
- `[E21]` STM §1 摘录 C | paper.pdf p.38 §4.5.3 | paper_content.txt 行 1202-1203
    - quote: "It will be turned right when the multi-pass test is started, note that the guards here must be the same as to start the multi-pass test."
    - supports: A.V.1 uses the multi-pass start guard
- `[E22]` paper.pdf p.47 §4.5.3 | paper_content.txt 行 1337-1340
    - quote: "it is critical to ensure that valves change their positions synchronously."
    - supports: B.V.10 and B.V.11 synchronous bypass supervision
- `[E23]` paper.pdf p.47 §4.5.3 | paper_content.txt 行 1342-1345
    - quote: "when valve B.V.11 is open or when it is closed and pumps B.PM.1 and B.PM.2 are not on."
    - supports: combined valve and pump guard for bypass control
- `[E24]` paper.pdf p.47 §4.5.3 | paper_content.txt 行 1345-1347
    - quote: "there is a delay added before the turn left command. This is to ensure that the valve B.V.11 will have enough time to open"
    - supports: delay guard before redirecting bypass flow

</details>

- **intentional omissions**：刻意没有补具体阈值数字、延时长度和完整阀泵状态表；原文公开版没有给出这些数值，很多 limit 只以 allowed 或 critical allowed limits 表述。也没有新增未出现的传感器型号、PLC I/O 信号表或未被原文支持的恢复路径。

### #5 🏭 `fault-handling-plc-industry4__02` (HSM)

- **case**: Abort-reset-start return path
- **统计**：248 词 / 16 markers / 16 provenance entries
- **轴覆盖**：✅ H 层次 / ⚪ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The controller manages a packaging-machine PLC whose mechanical layout has one facility module and six main application modules [E1]; each application module can contain subroutines such as parameterization or axis movement, with additional application and basic modules beneath it [E2]. The application conforms mostly to ISA-S88 and implements an OMAC state-machine model [E3], while the return-path behavior uses machine modes such as execute, aborting, aborted, resetting, and starting [E4]. In automatic mode, the module executes until an error aborts it into the failure state aborted, and that state requires human intervention [E5]. Fault detection is hierarchical: basic modules detect hardware or technical-process faults such as a pneumatic cylinder not reaching its end position [E6], then the next higher level assigns the error ID [E7] and chooses the reaction according to severity [E8]. Error-management functions collect all errors and implement the reaction [E9], can escalate several individually reportable errors into a shutdown reaction [E10], and a lower-priority task sends alarms to the HMI [E11]. Recovery follows a standardized return path: resetting switches to manual mode to resolve process errors [E12], then automatic recalibration in starting is required before returning to automatic mode [E13]. After a shutdown-causing error, restart is permitted only if calibration has not been impaired and material is not entangled [E14]; then the operator may acknowledge the error and restart with the implemented function [E15]. Because the facility module and each application module possess these modes, the same return-path modes appear as sub-states in the machine [E16].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用 facility/application/basic module 层次和 sub-states in the machine 暴露了层次结构 [E1][E2][E16]；原文未给具体默认初始子状态，因此未写 default init。
- **G 守卫算术**：原文无数值算术守卫，未提供 G 轴的 arithmetic 覆盖；expanded_nl 只保留 calibration not impaired AND material not entangled 的复合布尔重启条件 [E14]。
- **A 动作**：A 钩子在错误 ID 分配、按严重度选择反应、收集错误、发送 HMI alarm、manual reset 和 starting recalibration 等动作 [E7][E8][E9][E11][E12][E13]。
- **F 故障恢复**：F 钩子体现在 automatic 中错误导致 aborted 且需人工介入、严重错误可 shutdown、满足校准/物料条件后 acknowledge and restart [E5][E10][E14][E15]；原文未支持 from any state 全局 escape。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息融合、implicit-domain 术语和 hierarchical error handling 中的 implicit-action-prose，但没有数值 multivar-guard [E1][E3][E7][E9][E14]。
- **ft fcstm-fit**：pyfcstm 适配点主要是复合层次与 sub-state 组织、抽象化的 HMI/alarm/error reaction 动作，以及复合布尔 restart guard [E1][E2][E9][E11][E14][E16]；forced+aspect 和多变量 SMT 算术覆盖弱。

</details>

<details><summary>provenance (16条)</summary>

- `[E1]` paper.pdf p.9 Case study B | paper_content.txt 行 405-413
    - quote: "The mechanical layout consists of one facility module and six main application modules"
    - supports: packaging-machine PLC has one facility module and six main application modules
- `[E2]` paper.pdf p.9 Case study B | paper_content.txt 行 411-414
    - quote: "Each application module includes similar subroutines, such as parameterization or axis movement, which are implemented differently and mostly include additional application and basic modules."
    - supports: application modules contain parameterization or axis-movement subroutines and additional application/basic modules
- `[E3]` paper.pdf p.9 Case study B | paper_content.txt 行 414-416
    - quote: "The application conforms mostly to the ISA-S88 and implements the OMAC state machine model."
    - supports: ISA-S88 conformance and OMAC state-machine model
- `[E4]` STM §1 摘录 A | paper.pdf p.9 | paper_content.txt 行 398-404
    - quote: "“execute”, “aborting”, “aborted”, “resetting” and “starting”."
    - supports: return-path mode names execute, aborting, aborted, resetting, and starting
- `[E5]` STM §1 摘录 A | paper.pdf p.9 | paper_content.txt 行 398-400
    - quote: "In automatic mode, the module is executed and aborted in case of errors resulting in a failure state (“aborted”) which requires human interaction."
    - supports: automatic execution, error-driven abort to aborted, and required human intervention
- `[E6]` STM §1 摘录 B | paper.pdf p.9 Case study B | paper_content.txt 行 416-421
    - quote: "a pneumatic cylinder not reaching its end position, should be identified by the basic module pneumatic cylinder."
    - supports: basic modules detect hardware/process faults such as a pneumatic cylinder not reaching end position
- `[E7]` STM §1 摘录 B | paper.pdf p.9 Case study B | paper_content.txt 行 421-424
    - quote: "the error ID is assigned on the next higher level along with the decision on how the identified error should be handled"
    - supports: higher level assigns error ID
- `[E8]` STM §1 摘录 B | paper.pdf p.9 Case study B | paper_content.txt 行 423-425
    - quote: "related to the severity of the error in rising order: only a warning is issued, the machine is immediately shut down"
    - supports: reaction is chosen according to error severity
- `[E9]` STM §1 摘录 B | paper.pdf p.9 Case study B | paper_content.txt 行 430-433
    - quote: "The functions collect all errors and implement the error reaction."
    - supports: error-management functions collect errors and implement the reaction
- `[E10]` STM §1 摘录 B | paper.pdf p.9 Case study B | paper_content.txt 行 433-435
    - quote: "If several errors arrive, which individually would only be reported, the error reaction of shutting down may for example be set."
    - supports: multiple individually reportable errors can be escalated into shutdown
- `[E11]` paper.pdf p.9 Case study B | paper_content.txt 行 435-437
    - quote: "The task with the lower priority executes functions related to the HMI (sending the alarms)."
    - supports: lower-priority task sends alarms to the HMI
- `[E12]` STM §1 摘录 A | paper.pdf p.9 | paper_content.txt 行 399-401
    - quote: "The resetting is done by switching to manual mode, used to resolve process errors"
    - supports: resetting switches to manual mode to resolve process errors
- `[E13]` STM §1 摘录 A | paper.pdf p.9 | paper_content.txt 行 400-402
    - quote: "followed by an automatic recalibration of the machine (“starting”), which is a prerequisite for returning back to automatic mode."
    - supports: automatic recalibration in starting before returning to automatic mode
- `[E14]` STM §1 摘录 B | paper.pdf p.9 Case study B | paper_content.txt 行 435-437
    - quote: "If the calibration has not been impaired by the shutdown and the material is not entangled somewhere in the machine"
    - supports: restart guard: calibration not impaired and material not entangled
- `[E15]` STM §1 摘录 B | paper.pdf p.9 Case study B | paper_content.txt 行 435-437
    - quote: "the operator can decide to acknowledge the error and restart using the implemented function."
    - supports: operator acknowledgement and restart using the implemented function
- `[E16]` STM §1 摘录 A | paper.pdf p.9 | paper_content.txt 行 401-402
    - quote: "each application module possesses these different operation modes, allowing for sub-states in the machine."
    - supports: return-path modes appear as sub-states in the machine hierarchy

</details>

- **intentional omissions**：原文本条没有给出阀门编号、传感器型号、数值阈值或任意状态强制跳转，所以未加入这些内容；也没有枚举全部 OMAC states。

### #6 ⚙️ `finite-state-automaton-control-system-walking-machines__01` (HSM)

- **case**: Hierarchical Navigation-and-Gait Supervisor for a Walking Machine
- **统计**：276 词 / 29 markers / 29 provenance entries
- **轴覆盖**：✅ H 层次 / ⚪ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The walking-machine controller is a top-down hierarchy of smaller subsystems, each process is treated as its own finite-state automaton, and the highest process sends task demands down to the middle level [E1][E2][E3]. At the top, global navigation starts in SinitSystem to set up data repositories and check the robot, then handles route generation, target waypoints, mission monitoring, heading error, and position error through the shared repositories [E4][E5][E6][E7][E8]. The middle local-navigation automaton starts in SloadTarget, requests a new target, then moves toward forward motion after a waypoint is loaded while using proximity sensors for collision-free path planning and inclinometers for gait selection [E9][E10][E11][E12]. Local motion behaviour is refined by a lower gait FSM: the lower layer chooses a tripod gait on relatively flat terrain and a wave gait when surface inclination is detected [E13][E14][E15]. During execution, every state section first reads the whiteboard and makes local copies of recent variables; OnEntry sets state variables, Internal runs cyclic actions, and OnExit performs clean-up [E16][E17][E18]. In the left-sidewalk behaviour, entering resumes the sideways-walk gait submachine and exiting suspends it before switching to rightward motion [E19][E20][E21]. The simulated hexapod uses GPS, compass, inclinometers, and six proximity sensors as feedback while local navigation sends body-trajectory demand to the actuation subsystem that generates motor commands [E22][E23]. The named guards are whiteboard-derived conditions: non-normal status makes ffault transfer the left-sidewalk state to Sstop, and if at least one of fleftobs or foutofcorridor is valid, the controller switches to right-side walking [E24][E25][E26]. For abnormal cases, Sstop stops the robot and returns it to its initial configuration, while an unreachable blocked path notifies the user and waits for further instructions or a modified mission [E27][E28][E29].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 通过 top-down hierarchy、global/local/lower gait FSM 三层，以及 SinitSystem 与 SloadTarget 的初始进入语义暴露 H 轴；下层 gait 只写原文支持的 tripod/wave 选择，未补默认初始 gait [E1][E2][E4][E9][E13][E14][E15]。
- **G 守卫算术**：原文未提供显式数值阈值或算术比较，G 轴只覆盖白板派生的复合布尔守卫：ffault 与 fleftobs/foutofcorridor 至少一个有效触发迁移 [E24][E25][E26]。
- **A 动作**：A 钩子在 OnEntry/Internal/OnExit 动作、left-sidewalk 子机 resume/suspend、以及 actuation subsystem 生成 motor commands 中体现 [E16][E17][E18][E19][E20][E21][E23]。
- **F 故障恢复**：原文支持故障/异常处理但不支持任意状态全局强制 emergency；expanded_nl 暴露 ffault 到 Sstop、Sstop 返回初始配置、blocked path 通知用户并等待/修改 mission 的恢复路径 [E25][E27][E28][E29]。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拆段、implicit-domain 术语、implicit-action-prose 和 composite guard：层次结构、gait/whiteboard/corridor 术语、OnEntry/Internal/OnExit 动作与 fleftobs/foutofcorridor 守卫分散在不同原文章节 [E1][E13][E16][E17][E24][E26]。
- **ft fcstm-fit**：pyfcstm fit 主要体现在深复合 + 非平凡 init 链、state action 阶段和硬件边界抽象；原文未给多变量数值 SMT guard 或全局 forced/aspect 规则，因此这些独占优势覆盖弱 [E1][E4][E9][E13][E16][E17][E18][E22][E23]。

</details>

<details><summary>provenance (29条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.3 Control system structure | paper_content.txt 行 233-235
    - quote: "The developed control structure divides the overall system into smaller subsystems which are arranged in a hierarchical (top-down) structure."
    - supports: top-down hierarchy of smaller subsystems
- `[E2]` STM §1 摘录 A | paper.pdf p.3 Control system structure | paper_content.txt 行 254-255
    - quote: "Each process in the control structure is treated as a separate finite state automaton."
    - supports: each process is treated as its own finite-state automaton
- `[E3]` STM §1 摘录 A | paper.pdf p.3 Control system structure | paper_content.txt 行 244-247
    - quote: "the highest level process sends the task demand to the level below (middle level), which in turn sends its demand to the level below it."
    - supports: highest process sends task demands down to the middle level
- `[E4]` STM §1 摘录 B | paper.pdf p.4 Global navigation FSM | paper_content.txt 行 281-284
    - quote: "This is the initial state of the automaton. It sets up the data repositories and performs a check that the robot system is working properly."
    - supports: global navigation starts in SinitSystem to set up repositories and check the robot
- `[E5]` STM §1 摘录 B | paper.pdf p.4 Global navigation FSM | paper_content.txt 行 268-270
    - quote: "The global navigation automaton is the highest level subsystem in the control structure and is responsible for route generation."
    - supports: global navigation handles route generation
- `[E6]` STM §1 摘录 B | paper.pdf p.4 Global navigation FSM | paper_content.txt 行 270-272
    - quote: "receiving target waypoints and requesting further instructions in case of a locked path."
    - supports: target waypoints
- `[E7]` STM §1 摘录 B | paper.pdf p.4 Global navigation FSM | paper_content.txt 行 272-274
    - quote: "the global navigation process monitors the mission, calculating the heading error and evaluating the position errors."
    - supports: mission monitoring, heading error, and position error
- `[E8]` STM §1 摘录 B | paper.pdf p.4 Global navigation FSM | paper_content.txt 行 274-276
    - quote: "This information is deposited on the status repository which is subsequently used by the local navigation subsystem."
    - supports: shared repositories used across global and local navigation
- `[E9]` STM §1 摘录 C | paper.pdf p.4 Local navigation FSM | paper_content.txt 行 324-328
    - quote: "This is the initial state of the automaton. It sends a request to the global navigation automaton"
    - supports: local navigation starts in SloadTarget and requests a new target
- `[E10]` STM §1 摘录 C | paper.pdf p.4 Local navigation FSM | paper_content.txt 行 328-331
    - quote: "When a target waypoint has been loaded, it transitions to the SmoveFwd state."
    - supports: moves toward forward motion after a waypoint is loaded
- `[E11]` STM §1 摘录 C | paper.pdf p.4 Local navigation FSM | paper_content.txt 行 310-312
    - quote: "It uses information from the proximity sensors to produce a collision free path for the robot"
    - supports: proximity sensors for collision-free path planning
- `[E12]` STM §1 摘录 C | paper.pdf p.4 Local navigation FSM | paper_content.txt 行 313-314
    - quote: "The information from the inclinometers is used to define the type of gait motion."
    - supports: inclinometers for gait selection
- `[E13]` STM §1 摘录 D | paper.pdf p.5 gait sub-behaviour | paper_content.txt 行 383-387
    - quote: "The lower layer governs which type of gait to use. This two-tier description follows the concept of hierarchical FSMs."
    - supports: lower gait FSM refines local motion behaviour
- `[E14]` STM §1 摘录 D | paper.pdf p.5 gait sub-behaviour | paper_content.txt 行 398-401
    - quote: "This state generates the tripod gait. The FSM transitions to this state when the motion surface is relatively flat."
    - supports: tripod gait on relatively flat terrain
- `[E15]` STM §1 摘录 D | paper.pdf p.5 gait sub-behaviour | paper_content.txt 行 402-405
    - quote: "The wave gait is implemented in this state. Since this is the most stable gait, the FSM transitions to this state when a surface inclination is detected."
    - supports: wave gait when surface inclination is detected
- `[E16]` paper.pdf p.8 Real-time implementation | paper_content.txt 行 656-659
    - quote: "Whenever a section of the current state executes, it first reads the whiteboard and makes local copies of the whiteboard variables."
    - supports: state sections read the whiteboard and copy recent variables
- `[E17]` paper.pdf p.8 Real-time implementation | paper_content.txt 行 661-664
    - quote: "The OnEntry section associated with each state was used to setup the state variables. The OnExit section was used for the clean-up code."
    - supports: OnEntry sets state variables and OnExit performs clean-up
- `[E18]` paper.pdf p.8 Real-time implementation | paper_content.txt 行 664-665
    - quote: "All the cyclic actions were implemented in the Internal section."
    - supports: Internal runs cyclic actions
- `[E19]` paper.pdf p.8 Real-time implementation | paper_content.txt 行 673-678
    - quote: "When the FSM enters SmoveLeft, its OnEntry section is executed first, that is, it resumes the activities of the submachine related to sideways walk towards left."
    - supports: entering left-sidewalk resumes the gait submachine
- `[E20]` paper.pdf p.8 Real-time implementation | paper_content.txt 行 683-685
    - quote: "first the OnExit section of SmoveLeft is executed, that is, the activities of the submachine are suspended."
    - supports: exiting left-sidewalk suspends the submachine
- `[E21]` paper.pdf p.8 Real-time implementation | paper_content.txt 行 685-687
    - quote: "After that the FSM transitions to SmoveRight."
    - supports: switching to rightward motion
- `[E22]` paper.pdf p.9 Simulation | paper_content.txt 行 750-755
    - quote: "GPS, compass and inclinometers were attached to the robot model to provide robot pose as feedback to the control system. Six proximity sensors were also attached to the hexapod"
    - supports: GPS, compass, inclinometers, and six proximity sensors as feedback
- `[E23]` STM §1 摘录 C | paper.pdf p.4 Local navigation FSM | paper_content.txt 行 315-318
    - quote: "This demand is sent to the lowest level in the hierarchy, that is, actuation control subsystem which generates the motor commands."
    - supports: actuation subsystem generates motor commands
- `[E24]` STM §1 摘录 E | paper.pdf p.6 transition guard | paper_content.txt 行 451-453
    - quote: "OnEntry and OnExit conditions (denoted by fc) are produced within the states using the whiteboard readings"
    - supports: named guards are whiteboard-derived conditions
- `[E25]` STM §1 摘录 E | paper.pdf p.6 transition guard | paper_content.txt 行 457-459
    - quote: "If the status is different from normal, then the ffault as the OnExit condition becomes valid and the state transfers to Sstop."
    - supports: non-normal status makes ffault transfer to Sstop
- `[E26]` STM §1 摘录 E | paper.pdf p.6 transition guard | paper_content.txt 行 468-473
    - quote: "If at least one of fleftobs and foutofcorridor is valid, the state SmoveLeft transfers to SmoveRight producing the side walk to the right side."
    - supports: fleftobs or foutofcorridor switches to right-side walking
- `[E27]` STM §1 摘录 C | paper.pdf p.5 Local navigation FSM | paper_content.txt 行 372-376
    - quote: "This state ensures the robot has stopped and returns the robot to its initial configuration."
    - supports: Sstop stops the robot and returns it to its initial configuration
- `[E28]` paper.pdf p.9 Simulation | paper_content.txt 行 769-772
    - quote: "in case no path exists within the robot workspace constraints, then a signal is generated and the situation is communicated to the user, while the robot awaits further instructions."
    - supports: blocked path notifies the user and waits for further instructions
- `[E29]` paper.pdf p.11 Simulation | paper_content.txt 行 865-870
    - quote: "Once the user initiates the modified mission, fmission modified becomes valid and transition to SinitMotion is performed. The robot continues its motion based on the modified mission."
    - supports: modified mission recovery path

</details>

- **intentional omissions**：没有添加具体 valve/motor 编号、数值阈值、emergency stop 或任意状态 forced safe-state，因为原文只支持 generic motor commands、fault flags 和局部/任务级异常处理。也没有写 lower gait FSM 的默认初始 gait，因为文本只说明按 terrain/inclination 在 tripod 与 wave 间选择。

### #7 🩺 `cara-infusion-pump-formal-spec__01` (EFSM)

- **case**: Pump manual/autocontrol modes
- **统计**：254 词 / 17 markers / 17 provenance entries
- **轴覆盖**：✅ H 层次 / ⚪ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access [E1] [E2] [E3]. The pump has manual and autocontrol modes [E4]. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source [E5] [E6] [E7]. The Algorithm component controls infusion rate and records infusion-related data in log files [E8]; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate [E9]. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages [E10] [E11]. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit [E12] [E13]. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications [E14]. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control [E15] [E16]. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target [E17].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 通过 Mode_Control_Algorithm 中的 Ask_StartAC submode、setpoint 修改和 StartAC 进入 AutocontrolInit 暴露了层次结构 [E12] [E13]；原文未给进入该 mode 的默认初始子状态，因此未声称默认 init。
- **G 守卫算术**：原文不支持数值阈值或算术守卫；expanded_nl 只保留了无 pump-operation complications 的定性条件 [E14] 和 backManual 多源布尔触发 [E17]，未提供 G 轴算术覆盖。
- **A 动作**：A 钩子集中在 manual switch/default flow、external control voltage、log files、error messages、alarm activation 和 release control 等非平凡动作 [E5] [E6] [E7] [E8] [E10] [E11] [E15] [E16]。
- **F 故障恢复**：F 钩子是 complications/fault 时释放 CARA 控制并回到 Manual 的恢复路径，以及四个 backManual 触发源共享的 Manual recovery target [E14] [E16] [E17]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain 医疗输液术语、implicit-action-prose 散叙述动作，以及 multivar-guard/global-cross-cutting 的四源 backManual 规则 [E7] [E8] [E15] [E16] [E17]。
- **ft fcstm-fit**：pyfcstm 适配主要体现在 abstract action/effector 解耦的泵速、显示、日志、报警动作，以及 forced fallback 风格的 backManual 横切回退；深复合 init 和多变量 SMT 算术守卫覆盖弱 [E5] [E7] [E8] [E11] [E15] [E17]。

</details>

<details><summary>provenance (17条)</summary>

- `[E1]` STM §1 摘录 B | paper.pdf p.7 §3.1 | paper_content.txt 行 367-368
    - quote: "The components include Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors."
    - supports: CARA coordinates the named interface, monitor, algorithm, and pump-monitor components
- `[E2]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 247
    - quote: "The infusion pump is the device which moves fluid into the patient."
    - supports: infusion pump that moves fluid into the patient
- `[E3]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 241-243
    - quote: "all data from the sensor is assumed to be stored in a shared buffer"
    - supports: sensor readings are stored in a shared buffer for software access
- `[E4]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 249
    - quote: "The pump has two modes, manual and autocontrol."
    - supports: pump has manual and autocontrol modes
- `[E5]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 249-250
    - quote: "In manual mode, the pump speed is set with a switch built into the pump."
    - supports: manual mode pump speed is set with the built-in switch
- `[E6]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 256-259
    - quote: "sets a default flow rate directly on the pump for use by the pump when it is operating in manual mode"
    - supports: caregiver sets a default flow rate directly on the pump for manual operation
- `[E7]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 250-251
    - quote: "In autocontrol mode, the pumping speed is set by a control voltage from an external source."
    - supports: autocontrol mode pump speed is set by external control voltage
- `[E8]` STM §1 摘录 B | paper.pdf p.7 §3.1 | paper_content.txt 行 370-371
    - quote: "The purpose of the Algorithm component is to control the infusion rate of the pump and keep track of infusion related data in log files."
    - supports: Algorithm controls infusion rate and records infusion-related data in log files
- `[E9]` STM §1 摘录 B | paper.pdf p.7 §3.1 | paper_content.txt 行 371-373
    - quote: "A patient’s blood pressure is used to compute the rate at which the pump will be infusing"
    - supports: patient blood pressure is used to compute the infusion rate
- `[E10]` STM §1 摘录 B | paper.pdf p.7 §3.1 | paper_content.txt 行 377-380
    - quote: "It allows the caregiver to modify infusion parameters such as the target blood pressure, and also initiate and terminate the algorithm’s control of the pump."
    - supports: caregiver modifies target blood pressure and starts or terminates algorithmic pump control
- `[E11]` STM §1 摘录 B | paper.pdf p.7 §3.1 | paper_content.txt 行 380-382
    - quote: "Second, it displays and sounds error messages."
    - supports: Caregiver Interface displays and sounds error messages
- `[E12]` STM §1 摘录 C | paper.pdf p.19 Figure 11 text | paper_content.txt 行 1303-1311
    - quote: "we specify the four states of CARA - wait, manual, autocontrol init, and autocontrol — and the Ask_StartAC submode."
    - supports: Mode_Control_Algorithm hierarchy has mode-control states plus Ask_StartAC submode
- `[E13]` STM §1 摘录 C | paper.pdf p.19 Figure 11 text | paper_content.txt 行 1322-1323
    - quote: "In the Ask_StartAC submode, the setpoint value can be changed and AutocontrolInit may be entered by pushing the StartAC button."
    - supports: Ask_StartAC allows setpoint change and StartAC enters AutocontrolInit
- `[E14]` STM §1 摘录 B | paper.pdf p.7 §3.1 | paper_content.txt 行 373-375
    - quote: "The CARA algorithm controls the flow rate as long as there are no complications in the pump’s operation."
    - supports: normal autocontrol continues only while there are no pump-operation complications
- `[E15]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 230-232
    - quote: "Whenever a pump fault occurs (e.g., occlusion in the fluid tubing), appropriate alarm signals are activated."
    - supports: pump fault such as fluid-tubing occlusion activates alarm signals
- `[E16]` STM §1 摘录 A | paper.pdf p.5 | paper_content.txt 行 232-234
    - quote: "The caregiver is responsible for removing the pump’s faults, and if they happen when the pump is being controlled by CARA, the software releases its control."
    - supports: caregiver removes pump faults and software releases control when CARA was controlling the pump
- `[E17]` STM §1 摘录 B | paper.pdf p.7 §3.1 | paper_content.txt 行 536-539
    - quote: "CA_backManual OR CB_backManual OR CP_backManual OR CC-backManual — CA-mode = Manual"
    - supports: any listed back-to-manual flag causes CA_mode to become Manual

</details>

- **intentional omissions**：未加入血压阈值、3 分钟超时、cuff 采样频率或有效区间，因为这些属于后续 Cuff Handler 条目或本 case §1 未支撑。未补 valve 编号、传感器型号、默认初始子状态或 per-tick aspect，因为原文没有给出。

### #8 🅿️ `lift-control-automatic-car-parking-using-plc__01` (EFSM)

- **case**: Multi-Level Parking Lift Auto/Manual Positioning Controller
- **统计**：278 词 / 19 markers / 19 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The controller belongs to an automatic car-parking lift system used to take cars into and out of the system for parking [E1], in which a single Beckhoff PLC controls the parking system and a VFD drives the lift [E2], using speed control for acceleration, deceleration, and accurate stopping [E3], while pallet position, lift-level alignment, and safety interlocks are sensed by dedicated sensors [E4]. It organizes lift behavior into manual and auto mode sequences [E5]: manual mode is an inching maintenance mode with spring-action up/down buttons [E6], fixed slow speed, and actions from the HMI or teach pendant [E7], whereas auto mode initially waits for a command [E8] expressed as direction and number of levels to move [E9]. In auto mode, the PLC derives movement from destination level no minus source level no: a negative result means upward travel and initializes the level counter, while a positive result means downward travel for the counted levels [E10][E11]. The VFD interface receives forward, backward, slow-speed, high-speed, and reset commands from the PLC [E12]; during travel, the controller reduces speed when the fork slow sensor is sensed and stops when the fork stop sensor is sensed [E13]. After stopping, level-position sensors are checked for correct stopping [E14], and slat-confirmation sensing confirms that correct position makes pallet transfer safe [E15]; if a level difference remains, the confirmation sensor is not sensed and an error is given [E16]. Safety handling cuts and stops lift operation when Height/AntiLift sensors detect improper pallet engagement during up/down movement [E17], over-travel sensors alarm when the lift goes above safe limits [E18], and whenever an alarm occurs the whole lift goes into an emergency case requiring operator acknowledgement [E19].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：原文仅支持弱层次结构：expanded_nl 暴露了 manual/auto 两类 mode sequence，并说明 auto mode 的默认进入相位是等待 command [E5][E8]；原文未给更深嵌套或显式 initial pseudo。
- **G 守卫算术**：G 钩子集中在 destination level no minus source level no 的算术守卫：负值上行并初始化 counter，正值下行指定层数 [E10][E11]；另有 fork sensor 与 level-confirmation sensor 的布尔/传感器守卫 [E13][E16]。
- **A 动作**：A 钩子包括 manual inching 与 HMI/teach-pendant 动作 [E6][E7]、PLC 到 VFD 的 forward/backward/slow/high/reset 命令 [E12]，以及 fork sensor 触发的减速和停止动作 [E13]。
- **F 故障恢复**：F 钩子由安全与报警处理支撑：Height/AntiLift cut-and-stop、over-travel alarm，以及 alarm 后 whole lift 进入 emergency case 并需要 operator acknowledgement [E17][E18][E19]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain（Beckhoff PLC、VFD、fork sensor、Height/AntiLift）、implicit-action-prose（减速、停止、VFD 命令）与 multivar-guard（destination/source level 算术）等 baseline 失败模式，并且证据跨 Abstract、Operation、VFD、Conclusion 多节 [E2][E10][E12][E13][E19]。
- **ft fcstm-fit**：pyfcstm 适配点为弱复合 init 链（manual/auto，auto 先等待 command）[E5][E8]、destination-source 算术守卫 [E10][E11]、VFD/传感器/报警的 abstract action 候选 [E12][E13][E17]，以及 alarm emergency 的 forced-like 横切片段 [E19]；但无 per-tick aspect 或深复合层次。

</details>

<details><summary>provenance (19条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 15-17
    - quote: "lift control is proposed in fully automatic Level Car Parking System which used to take cars in/out of system & park the cars."
    - supports: automatic car-parking lift system used to take cars into/out of the system for parking
- `[E2]` STM §1 摘录 A | paper.pdf p.1 INTRODUCTION | paper_content.txt 行 58-63
    - quote: "A single PLC (BECKHOFF PLC) is used to control the entire parking system. For accurate speed control lift is operated with VFD."
    - supports: single Beckhoff PLC controls the parking system; VFD drives the lift
- `[E3]` STM §1 摘录 A | paper.pdf p.1 INTRODUCTION | paper_content.txt 行 63-64
    - quote: "Speed control is required for acceleration/ deceleration & proper stopping accuracy."
    - supports: speed control for acceleration, deceleration, and accurate stopping
- `[E4]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 17-20
    - quote: "The pallet position on lift, accurate positioning between lift-level & safety interlocks are sensed from dedicated sensor."
    - supports: pallet position, lift-level alignment, and safety interlocks sensed by dedicated sensors
- `[E5]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 145-147
    - quote: "There are two types of sequences manual mode sequence and auto mode sequence."
    - supports: manual and auto mode sequences
- `[E6]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 149-151
    - quote: "The lift manual mode operation is inching. b) The lift inched with spring action button in up or down direction for maintenance work."
    - supports: manual inching maintenance mode with spring-action up/down buttons
- `[E7]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 151-154
    - quote: "The speed in the manual/maintenance mode is slow speed. e) All manual mode actions are done from the HMI or from teach pendant."
    - supports: manual fixed slow speed and HMI/teach-pendant actions
- `[E8]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 159-160
    - quote: "lift is always waiting for command in auto mode"
    - supports: auto mode initially waits for a command
- `[E9]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 160-162
    - quote: "The command given to the lift is in terms of direction and number of levels to move."
    - supports: auto command expressed as direction and number of levels to move
- `[E10]` STM §1 摘录 C | paper.pdf p.3 Example | paper_content.txt 行 177-180
    - quote: "Number of levels to move = destination level no – source level no = 1 – 2 = -1. I.e. Counter value=1."
    - supports: destination-source arithmetic, negative result, upward travel, counter initialization
- `[E11]` STM §1 摘录 C | paper.pdf p.3 Example | paper_content.txt 行 185-189
    - quote: "Here no of levels is positive, it means that lift has given down command & two levels to move."
    - supports: positive result means downward travel for counted levels
- `[E12]` STM §1 摘录 B | paper.pdf p.2 §3 ELECTRICAL WIRING DIAGRAM OF VFD | paper_content.txt 行 118-120
    - quote: "The control signals received from the PLC to VFD are Commands as Forward, Backward, slow speed, high speed, & reset."
    - supports: VFD forward/backward/slow/high/reset commands from PLC
- `[E13]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 163-165
    - quote: "Once slow sensor(fork sensor) is sensed the speed of the VFD is made slow. e) As soon as the stop sensor(fork sensor) is sensed the lift stops."
    - supports: fork slow sensor reduces speed; fork stop sensor stops lift
- `[E14]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 165-167
    - quote: "The level position sensors are checked to ensure that the lift is stopped correctly."
    - supports: level-position sensors checked for correct stopping
- `[E15]` STM §1 摘录 B | paper.pdf p.1 §2 OVERVIEW DIAGRAM OF LIFT | paper_content.txt 行 85-88
    - quote: "This sensor are be used to confirm that the lift has reached the correct position and the transfer of pallet to be done is safe."
    - supports: slat confirmation checks correct position and safe pallet transfer
- `[E16]` STM §1 摘录 C | paper.pdf p.3 §4 OPERATIONAL SEQUENCE | paper_content.txt 行 167-169
    - quote: "If there is a level difference, then the level confirmation sensor will not be sensed and error will be given."
    - supports: level difference causes missing confirmation and error
- `[E17]` STM §1 摘录 B | paper.pdf p.2 §2 OVERVIEW DIAGRAM OF LIFT | paper_content.txt 行 100-102
    - quote: "If the lift pallet not engaged properly during up/down movements, then Height/AntiLift sensors cut and stop the operation of Lift."
    - supports: Height/AntiLift safety cut/stop on improper pallet engagement
- `[E18]` STM §1 摘录 B | paper.pdf p.2 §2 OVERVIEW DIAGRAM OF LIFT | paper_content.txt 行 102-104
    - quote: "The over travel sensors used to alarm the system that lift is going above the safe position limits."
    - supports: over-travel alarm above safe position limits
- `[E19]` paper.pdf p.5 §6 CONCLUSION | paper_content.txt 行 284-288
    - quote: "Whenever an alarm occurs whole lift goes into emergency case where the operator needs to acknowledge alarm to avoid major accidents at parking."
    - supports: alarm sends whole lift to emergency case requiring operator acknowledgement

</details>

- **intentional omissions**：未加入 valve 编号、传感器型号、具体时间阈值、数学函数或 watchdog/per-tick 逻辑，因为原文没有这些信息。也没有把安全报警强写成 from any state forced reset，只保留原文支持的 whenever alarm emergency/acknowledgement 语义。

### #9 🏭 `plc-scada-liquid-filling-automation-ejosat__01` (EFSM)

- **case**: HMI-Configured Cup Filling, Capping, and Labeling Line
- **统计**：268 词 / 17 markers / 17 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ⚪ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The filling line is organized as main processes with helper processes [E1], and the cycle starts from HMI user entries for composition, gram values, and quantity [E2]. When product quantity is more than one, the HMI selects automatic production [E3]; that automatic screen can choose four products and assign gram amounts to one or more of them [E4], while the maximum production count is tied to cup capacity and defaults to 10 cups [E5]. The HMI macro checks whether the entered content is conforming [E6], and cups leave storage according to the desired filling number [E7]. During filling, a level-control helper process measures each tank with pressure transmitters, and the PLC opens pneumatic valves only when the desired liquid level is present and the filling signal arrives [E8]. As the cup weight rises, load-cell feedback drives the stop condition: when the requested weight is reached, the valve is closed [E9]. Inside capping, the default sequence begins with a filled cup arriving [E10], then uses the cap store, vacuum pickup, a rodless pneumatic cylinder, and a 50 mm vertical capping motion [E11], and returns the cylinder and vacuum to initial positions [E12]. If any capping step fails, the whole capping process restarts from the beginning [E13]; if liquid, cups, or lids run out, production stops and an alarm is raised [E14], and an operator clears the alarm after replenishment [E15]. Labeling then prints a mixed label for multiple selected products and a pure label for a single selected product [E16], while conveyor transport is monitored by comparing the step-motor command with encoder feedback so movement failures are detected [E17].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：原文支持弱层次：expanded_nl 用 [E1] 暴露主过程/辅助过程嵌套，用 [E10]-[E12] 暴露 capping 内部默认从 cup arrival 开始的顺序；但原文没有严格 STM 式深层 mode + init pseudo。
- **G 守卫算术**：G 钩子在 [E3]-[E5] 的 product quantity > 1 与默认 10 cups 限制，以及 [E8]-[E9] 的 tank level AND filling signal、requested cup weight 条件。
- **A 动作**：A 钩子集中在 [E8]-[E17]：PLC 开/关 pneumatic valves，vacuum/cylinder 执行封盖，alarm/label/encoder monitoring 都是非平凡 I/O action。
- **F 故障恢复**：F 轴只有局部恢复：capping step failure 后重启 capping [E13]，物料耗尽后 stop + alarm + replenish-clear [E14]-[E15]；原文不支持任意状态 global emergency safe-state。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain 与 implicit-action-prose（HMI、loadcell、pressure transmitter、vacuum、encoder 分散在 [E2]-[E17]），并有 multivar-guard/composite-internal 钩子 [E8]-[E12]；global-cross-cutting 覆盖弱。
- **ft fcstm-fit**：pyfcstm fit 主要来自多变量 SMT guard [E3]-[E5][E8]-[E9]、capping composite init 弱钩子 [E10]-[E12]、以及 effector-agnostic abstract action 解耦 [E8]-[E17]；forced+aspect 横切原文不支持。

</details>

<details><summary>provenance (17条)</summary>

- `[E1]` paper.pdf p.5 §2.2 Sistem Bileşenleri | paper_content.txt 行 373-377
    - quote: "Sistem içerisinde ana dört adet proses kullanılmaktadır. Ana proseslerin içerisinde ana proses işleminin tamamlanması için birçok yardımcı proses bulunmaktadır."
    - supports: main processes with helper processes
- `[E2]` paper.pdf p.4 | paper_content.txt 行 320-325
    - quote: "Bu ürünlerden biri veya birkaçı seçilerek gramajları belirlenir. Ürün özelliklerinin belirlenmesiyle kaç adet üretileceği girilir."
    - supports: HMI entries for composition, gram values, and quantity
- `[E3]` paper.pdf p.4 | paper_content.txt 行 313-317
    - quote: "Sıvı dolumu yapılacak ürün miktarı 1’den fazla ise HMI paneldeki ilgili ekrandan otomatik buton seçimi yapılır."
    - supports: product quantity more than one selects automatic production
- `[E4]` paper.pdf p.4 | paper_content.txt 行 320-323
    - quote: "Fazla adette sıvı dolumu için kullanılan otomatik üretim ekranı içerisinde seçilebilecek 4 adet farklı ürün bulunmaktadır. Bu ürünlerden biri veya birkaçı seçilerek gramajları belirlenir."
    - supports: four selectable products and gram assignment
- `[E5]` paper.pdf p.4 | paper_content.txt 行 323-325
    - quote: "Maksimum üretim adedi maksimum bardak kapasitesi ile doğru orantılıdır ve varsayılan olarak 10 adet ile sınırlandırılmıştır."
    - supports: maximum production count tied to cup capacity and default limit 10
- `[E6]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 57-59
    - quote: "The conformity of the contents entered by the user is determined according to the macro code written into the HMI panel."
    - supports: HMI macro checks entered content
- `[E7]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 59-60
    - quote: "Depending on the desired filling number, the glasses leave the glass storage and arrive at the liquid filling stations."
    - supports: cups leave storage according to desired filling number
- `[E8]` STM §1 摘录 B | paper.pdf p.5 §2.2.1 | paper_content.txt 行 385-401
    - quote: "tankların seviyelerinin ölçümü için basınç transmitleri kullanılmaktadır. Sıvı seviye ölçümünün istenilen düzeyde olması ve dolum sinyalinin gelmesi ile pnömatik vanalar açılır."
    - supports: pressure-transmitter level measurement and valve opening guard
- `[E9]` paper.pdf p.6 §2.2.1 | paper_content.txt 行 412-416
    - quote: "Bardak istenen ağırlığa geldiğinde vananın kapatılması için ağırlık ölçüm prosesi çalıştırılır. Gerçek zamanlı olarak gerçekleşen bu işlemler yük hücresi (loadcell) adı verilen sensör ölçümü ile ağırl"
    - supports: load-cell weight feedback and valve closing at requested weight
- `[E10]` STM §1 摘录 C | paper.pdf p.6 §2.2.2 | paper_content.txt 行 451-453
    - quote: "1. Adım: Kapak takma istasyonuna bardak gelir."
    - supports: capping sequence begins with cup arrival
- `[E11]` paper.pdf p.6 §2.2.2 | paper_content.txt 行 446-456
    - quote: "Kapak deposundan kapak vakum yöntemi ile alınır ... pnömatik milsiz silinir ile gerçekleştirilir ... 50 milimetrelik dikey eksen hareketiyle kapak takılır."
    - supports: cap store, vacuum pickup, rodless pneumatic cylinder, and 50 mm capping motion
- `[E12]` STM §1 摘录 C | paper.pdf p.6 §2.2.2 | paper_content.txt 行 457
    - quote: "5. Adım: Milsiz silindir ve vakum başlangıç konumuna döner."
    - supports: cylinder and vacuum return to initial positions
- `[E13]` STM §1 摘录 C | paper.pdf p.6 §2.2.2 | paper_content.txt 行 458-460
    - quote: "Kapak takma işlemi esnasında işlem adımlarının biri veya birkaçında hata olması halinde prosesin tüm işlemleri baştan başlar."
    - supports: capping failure restarts the whole capping process
- `[E14]` paper.pdf p.5 | paper_content.txt 行 356-360
    - quote: "sıvı, bardak ve kapak gibi harcanan ürünler bitebilmektedir. Sistem içerisinde herhangi bir ürün bittiğinde üretim durur ve sistem alarm verir."
    - supports: liquid, cups, or lids running out stops production and raises alarm
- `[E15]` paper.pdf p.5 | paper_content.txt 行 360-363
    - quote: "Ürünlerin tamamlaması ardından yönetici veya operatör Şekil 8‘deki ekrandan alarm kaldırma işlemini yapar."
    - supports: operator clears alarm after replenishment
- `[E16]` STM §1 摘录 C | paper.pdf p.6 §2.2.3 | paper_content.txt 行 469-472
    - quote: "Birden fazla ürün seçilip istenilen oranlarda karıştırılmasıyla ... karışık etiketi basılır. Tek ürün seçimi yapılması durumda ... sade etiketi basılmaktadır."
    - supports: mixed label for multiple products and pure label for single product
- `[E17]` STM §1 摘录 C | paper.pdf p.7 §2.2.4 | paper_content.txt 行 505-529
    - quote: "Kapalı çevrim kontrolde çıkış sinyali ile giriş sinyali karşılaştırılır ... enkoder bilgi sinyali ile hatalar tespit edilir."
    - supports: closed-loop conveyor comparison and encoder-based movement failure detection

</details>

- **intentional omissions**：没有补写 valve 编号、精确目标重量、具体传感器型号编号、emergency stop 强制 safe-state 或 conveyor 自动恢复路径，因为原文没有给出这些行为细节。SCADA emergency button 只在原文中作为界面元素出现，未被扩展成全局故障转移。

### #10 🚆 `railway-generic-electronic-interlocking-software-engineering-methods__01` (EFSM)

- **case**: Route-3 request-call-occupation interlocking supervisor
- **统计**：258 词 / 8 markers / 8 provenance entries
- **轴覆盖**：✅ H 层次 / ⚪ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The Route 3 interlocking supervisor belongs to a railway electronic interlocking model expressed with Boolean interlocking functions and UML statecharts [E1]. Route R3 enters a composite Route Request phase whose internal path first checks S3, then the required track and point elements, and later continues through set, call, and occupation phases when availability decisions succeed [E2]. A route is available only when no conflicting route is already set, the relevant signals are red and unused, the required track sections are unoccupied, and all required elements are free and available [E3]. During this request path, point w1 is position-checked; if it is not in the correct position, the interlocking instructs the point to change before continuing [E4]. When Route 3 is set, s3, s5, Tb, Tc, Ty, and w1 are expected to move from free configurations to yellow reserved indications, and the test reports that Route 3 is set [E5]. The call phase turns the route elements green and clears the start signal to green, meaning the route is called and ready for train occupation [E6]. During occupation, the train proceeds section by section, occupied sections and the start signal turn red, and after the train stops before the destination signal the reserved overlap, route, and required elements are cleared; the Route 3 test records the cleared elements as grey [E7]. If Tc is faulted, the route request cannot be issued; unrequested point-machine switching or faulty sensors turn all Route 3 elements red and cancel the route, while incorrect train detection during occupation turns all signalling elements red [E8].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 通过 Route R3 进入 composite Route Request、内部先检查 S3 并继续到 set/call/occupation phase 的表述暴露了 Route R3 → Route Request → 内部检查的层次和默认入口，见 [E2]。
- **G 守卫算术**：原文无数值阈值或算术守卫，未提供 G-arithmetic 覆盖；expanded_nl 仅忠实暴露 no conflicting route、signals red/unused、track sections unoccupied、elements free/available、point position 这类布尔复合 guard，见 [E3][E4]。
- **A 动作**：A 钩子主要在 point corrective instruction、yellow/green/red/grey element indication changes、start signal clearing、route clearing 等非平凡动作，见 [E4][E5][E6][E7]。
- **F 故障恢复**：F 钩子在 Tc fault 阻止 route request，以及 set/call/occupation 场景中的 safety-critical event 使元素转 red、取消 route 或占用化的 fail-safe 响应，见 [E8]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain 术语（Route R3、S3、Tc、point machine）、composite-internal 结构、布尔 multivar-guard 和 implicit-action-prose 的颜色/锁闭动作，且 [E8] 暴露接近 global-cross-cutting 的安全响应。
- **ft fcstm-fit**：pyfcstm fit 中等：有复合 init/phase 链 [E2]、effector-agnostic abstract action 候选（signal/track/point indication 与 point instruction）[E4]-[E7]、forced-style fail-safe 响应 [E8]；但无数值 SMT 守卫或 per-tick aspect。

</details>

<details><summary>provenance (8条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 80-84
    - quote: "The interlocking system is modelled using Boolean interlocking functions and UML (Unified Modelling Language) statecharts."
    - supports: railway electronic interlocking model expressed with Boolean interlocking functions and UML statecharts
- `[E2]` paper.pdf p.106 (document p.84) Figure B.11 | paper_content.txt 行 3291-3293
    - quote: "Route R3; ROUTE REQUEST; Availability of S3; SET ROUTE; Route Call; Train Occupation"
    - supports: Route R3 default entry into Route Request and the route request/set/call/occupation phase structure
- `[E3]` STM §1 摘录 B | paper.pdf p.67-68 §4.5.2.1 | paper_content.txt 行 2198-2214
    - quote: "no conflicting routes ... signals are currently displaying a red aspect ... track sections are unoccupied ... required elements are free and available"
    - supports: compound availability guard over conflicting routes, signal state/use, track occupancy, and element availability
- `[E4]` paper.pdf p.70 §4.5.2.2 | paper_content.txt 行 2304-2309; paper.pdf p.106 Figure B.11
    - quote: "If not, an instruction is sent to the interlocking to change it into the correct required position"
    - supports: point w1 position check and corrective point-changing action before continuing
- `[E5]` STM §1 摘录 C | paper.pdf p.128 (document p.106) Table E.17 | paper_content.txt 行 3801-3809
    - quote: "s3 = Yellow ... s5 = Yellow ... Tb = Yellow ... Tc = Yellow ... Ty = Yellow ... w1 = Yellow ... Route 3 is set."
    - supports: Route 3 set action changes listed elements to yellow reserved indications
- `[E6]` STM §1 摘录 B/C | paper.pdf p.68-69 §4.5.2.1 and p.129 Table E.18 | paper_content.txt 行 2255-2262, 3825-3833
    - quote: "track sections sequentially turn green ... start signal clears to green ... route is ready for occupation"
    - supports: route call turns elements green and clears the start signal for occupation
- `[E7]` STM §1 摘录 B/C | paper.pdf p.69 §4.5.2.1 and p.129 Table E.19 | paper_content.txt 行 2270-2279, 3835-3844
    - quote: "track section ... turns red ... start signal then turns red ... reserved overlap, the route and required elements are cleared"
    - supports: occupation progression, red occupied indications, clearing behavior, and grey cleared Route 3 test result
- `[E8]` STM §1 摘录 C | paper.pdf p.130-131 (document p.108-109) Tables E.21-E.24 | paper_content.txt 行 3862-3926
    - quote: "Fault triggered for element Tc ... Route request is not issued ... All elements turn red ... Train detection operating incorrectly ... All signalling elements turn red."
    - supports: Tc fault prevents request, and safety-critical events force red/cancel or red occupied response

</details>

- **intentional omissions**：没有加入时间阈值、算术区间、传感器型号、阀门/继电器编号或额外恢复路径，因为原文只支持布尔可用性、颜色/占用状态和 Route 3 元素名。也没有写成 from any state 的全局跳转，因为原文只在 set/call/occupation 测试场景中验证 safety-critical response。

### #11 ✈️ `reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01` (EFSM)

- **case**: Closed-mode CONOPS and safe-mode fallback in Masat-1
- **统计**：274 词 / 26 markers / 26 provenance entries
- **轴覆盖**：⚪ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> Masat-1 flight-control software uses a closed-mode CONOPS: an application-layer finite state machine rules spacecraft operating modes, and in closed mode the main-bus subsystems follow the spacecraft operating mode [E1] [E2] [E3]. On launch or restart the controller enters INIT at the power-ON pseudo-state, updates the boot counter, delays antenna deployment 45 min, retries deployment up to three times before reboot if failure persists, then enters SAFE [E4] [E5] [E6] [E7] [E8] [E9]. Transitions are driven by ground telecommand, completion of initialization or tasks, battery charge below nominal, or FDIR reconfiguration after detected anomalies; procedures inside modes react to low battery, sun eclipse, ground visibility, and errors [E10] [E11] [E12]. In SAFE, the satellite remains commandable during sun-visible contact, the payload is off, only vital subsystems stay operational, beaconing is reduced from 60 to 120 s, and the receiver is always on for ground-station commands [E13] [E14] [E15]. When battery charge is under 86%, a critical low-power configuration powers off the payload, switches EPS, OBC, COM, and ADCS to low power, reduces the beacon to 120 s, and returns to idle only after batteries recharge to nominal level [E16] [E17] [E18]. Sun-visible operation assumes battery charge above 90%, keeps the receiver waiting for a valid ground command, and leaves the camera on standby; communication operation checks pointing error below 5 degrees and periodically rechecks battery level, falling back to the critical configuration if charge falls under 86% [E19] [E20] [E21] [E22] [E23]. For subsystem or system failures, the safety monitor raises event/action decisions to the flight planner, which switches the spacecraft to SAFE and keeps it there until the next ground contact [E24] [E25] [E26].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：原文无显式层次化状态机/嵌套 mode，expanded_nl 仅保留 application-layer FSM、closed-mode subsystem coupling 与 INIT 的 power-ON pseudo-state [E2][E3][E4]，因此 H 轴覆盖弱而非完整层次结构。
- **G 守卫算术**：G 钩子集中在 battery_charge under 86%、battery_charge above 90%、pointing_error below 5 degrees、antenna retry count up to three attempts 等自然语言数值守卫 [E8][E16][E19][E22][E23]。
- **A 动作**：A 钩子包括 INIT 更新 boot counter/延迟天线部署、SAFE 关闭 payload/降 beacon/保持 receiver ON、critical 配置切换 EPS/OBC/COM/ADCS 低功耗等非平凡动作 [E6][E7][E14][E15][E17][E18]。
- **F 故障恢复**：F 钩子为 subsystem/system failure 经 safety monitor 与 flight planner 切入 SAFE 并保持到下一次 ground contact，另有天线部署失败后重试三次再 reboot 的局部恢复 [E8][E24][E25][E26]。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拼接、implicit-domain 术语、implicit-action-prose 与 global-cross-cutting safe fallback：CONOPS、FDIR、EPS/OBC/COM/ADCS、beacon/receiver/payload 动作和 safety monitor→SAFE 分散在多处证据中 [E1][E12][E14][E17][E24][E25]。
- **ft fcstm-fit**：pyfcstm 适配点主要是 Expr-IR 数值守卫与 abstract action/effector 解耦，以及接近 forced safe fallback 的故障横切语义 [E16][E19][E22][E23][E14][E17][E25]；深复合 init 链因原文无显式嵌套结构而覆盖弱。

</details>

<details><summary>provenance (26条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.18 §6 | paper_content.txt 行 1084-1086
    - quote: "We decided to adopt a closed mode of concepts to ensure the deterministic behavior of the spacecraft."
    - supports: closed-mode CONOPS
- `[E2]` STM §1 摘录 D | paper.pdf p.27 Conclusions | paper_content.txt 行 1511-1513
    - quote: "control logic of the spacecraft is based on a finite state machine implemented at the application layer."
    - supports: application-layer finite state machine
- `[E3]` paper.pdf p.18 §6 | paper_content.txt 行 1073-1076
    - quote: "all main bus subsystems are driven by the spacecraft’s operating mode."
    - supports: main-bus subsystems follow spacecraft operating mode
- `[E4]` STM §1 摘录 B | paper.pdf p.18 §6 | paper_content.txt 行 1099-1102
    - quote: "enters the INIT mode at the power ON pseudo-state"
    - supports: controller enters INIT at the power-ON pseudo-state
- `[E5]` STM §1 摘录 B | paper.pdf p.18 §6 | paper_content.txt 行 1101-1103
    - quote: "starting point for any satellite restart due to power blackouts, failures, ground commands or watchdog resets."
    - supports: launch or restart entry context
- `[E6]` STM §1 摘录 B | paper.pdf p.18 §6 | paper_content.txt 行 1102-1103
    - quote: "The boot counter is then updated to keep track of the satellite reboot count."
    - supports: updates the boot counter
- `[E7]` STM §1 摘录 B | paper.pdf p.18 §6 | paper_content.txt 行 1103-1105
    - quote: "The antenna system deployment mechanism is designed to be executed 45 min after launch."
    - supports: delays antenna deployment 45 min
- `[E8]` STM §1 摘录 B | paper.pdf p.19 §6 | paper_content.txt 行 1110-1111
    - quote: "three attempts to redeploy the antenna were planned after which the satellite was rebooted"
    - supports: retries deployment up to three times before reboot
- `[E9]` STM §1 摘录 B | paper.pdf p.19 §6 | paper_content.txt 行 1114-1115
    - quote: "Thereafter, the Masat-1 shall enter safe mode"
    - supports: then enters SAFE
- `[E10]` STM §1 摘录 A/B | paper.pdf p.18 §6 | paper_content.txt 行 1090-1092
    - quote: "ground telecommand received; (ii) automatic onboard transition when a task or satellite initialization is completed"
    - supports: ground telecommand and task/initialization completion transition triggers
- `[E11]` STM §1 摘录 A/B | paper.pdf p.18 §6 | paper_content.txt 行 1091-1093
    - quote: "the battery charge is under the nominal level; or (iv) an automatic FDIR reconfiguration order upon some anomalies detected"
    - supports: battery-below-nominal and FDIR-anomaly transition triggers
- `[E12]` STM §1 摘录 A | paper.pdf p.18 §6 | paper_content.txt 行 1085-1088
    - quote: "occurring events, such as the low battery level, sun eclipse, ground visibility or errors."
    - supports: procedures inside modes react to low battery, eclipse, visibility, and errors
- `[E13]` STM §1 摘录 B/C | paper.pdf p.20 §6 | paper_content.txt 行 1135-1137
    - quote: "the satellite is fully commandable from the ground when a contact opportunity presents itself during sun visibility."
    - supports: SAFE remains commandable during sun-visible contact
- `[E14]` STM §1 摘录 C | paper.pdf p.20 §6 | paper_content.txt 行 1137-1139
    - quote: "the payload is turned off, only vital subsystems are operational, and the beaconing rate is reduced from 60 to 120 s"
    - supports: SAFE payload-off, vital-only, and beacon-rate actions
- `[E15]` STM §1 摘录 C | paper.pdf p.20 §6 | paper_content.txt 行 1141-1142
    - quote: "the satellite receiver shall be always ON waiting for GS command"
    - supports: SAFE keeps receiver always on for ground-station commands
- `[E16]` STM §1 摘录 B/C | paper.pdf p.20 §6 | paper_content.txt 行 1145-1146
    - quote: "Critical mode is entered when the battery charge level is under 86%."
    - supports: critical low-power configuration guard battery charge under 86%
- `[E17]` STM §1 摘录 C | paper.pdf p.20 §6 | paper_content.txt 行 1145-1147
    - quote: "the payload is powered off; the EPS, OBC and COM and ADCS are switched to low power mode."
    - supports: critical low-power effector actions
- `[E18]` STM §1 摘录 C | paper.pdf p.20 §6 | paper_content.txt 行 1147-1149
    - quote: "beacon rate is reduced from 60 to 120 s. After recharging batteries to a nominal level, we shall revert back to IDLE mode."
    - supports: critical beacon reduction and return after nominal recharge
- `[E19]` STM §1 摘录 B/C | paper.pdf p.20 §6 | paper_content.txt 行 1158-1160
    - quote: "The battery charging level in this mode is nominal—higher than 90%."
    - supports: sun-visible operation assumes battery charge above 90%
- `[E20]` STM §1 摘录 B/C | paper.pdf p.20 §6 | paper_content.txt 行 1160-1161
    - quote: "The receiver is ON, waiting for a valid direct command from the ground."
    - supports: receiver waits for valid ground command
- `[E21]` STM §1 摘录 B/C | paper.pdf p.20 §6 | paper_content.txt 行 1161-1163
    - quote: "The camera is on standby mode and the ADCS is ensuring nadir pointing attitude."
    - supports: camera standby in sun-visible operation
- `[E22]` paper.pdf p.20 §6 | paper_content.txt 行 1173-1175
    - quote: "monitor the satellite attitude in this mode to ensure less than a 5◦ pointing error"
    - supports: communication operation checks pointing error below 5 degrees
- `[E23]` STM §1 摘录 B | paper.pdf p.20 §6 | paper_content.txt 行 1175-1177
    - quote: "battery level check periodically, and it will switch the spacecraft to critical mode if the battery level falls under 86%."
    - supports: communication operation periodically checks battery and falls back to critical under 86%
- `[E24]` STM §1 摘录 D | paper.pdf p.25 §7.4 | paper_content.txt 行 1417-1419
    - quote: "events are raised and are handled through a decision matrix (event/action correlation)"
    - supports: safety monitor raises event/action decisions
- `[E25]` STM §1 摘录 D | paper.pdf p.25 §7.4 | paper_content.txt 行 1417-1420
    - quote: "For failures at the subsystem or system level, the safety monitor sends signals to the flight planner to switch to safe mode."
    - supports: subsystem/system failures switch spacecraft to SAFE via flight planner
- `[E26]` STM §1 摘录 D | paper.pdf p.25 §7.4 | paper_content.txt 行 1420-1422
    - quote: "it will remain in this state until next contact with the ground segment."
    - supports: SAFE remains until next ground contact

</details>

- **intentional omissions**：未加入原文没有的 valve/pump 编号、具体传感器型号、任意状态 forced transition 或新的恢复路径。也没有枚举全部 mode name；仅保留 INIT、SAFE 与少量关键配置，以避免把生成任务退化为状态清单复述。

### #12 ⚙️ `finite-state-machine-accommodating-unexpected-large-ground-height-variations-bipedal-robot-walking__01` (FSM)

- **case**: Blind terrain-transition FSM for the MABEL biped
- **统计**：279 词 / 10 markers / 10 provenance entries
- **轴覆盖**：⚪ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The controller supervises MABEL, a kneed planar biped with 1 m-long legs, over terrain whose height-change location and size are not given in advance [E1]. It uses a finite-state supervisor to switch among flat-ground walking, step-down, step-up, and trip-reflex controllers, with the top-level stance phases RW, SD, SU, and TR [E2]. Each transition decision combines front and end contact-switch readings with walking-surface height computed at impact from leg lengths and joint angles [E3]. When ground impact occurs close to the end of the gait, the swing-toe height guard keeps RW if the magnitude is below Delta H, selects SD if the height is below -Delta H, and selects SU if it is above Delta H [E4]. If the swing leg hits an obstacle or touches ground prematurely, the supervisor enters TR and checks late-trip or early-trip switching conditions [E5]. Inside TR, a separate reflex FSM routes tripping-start toward rapid lowering, rapid elevation, or recovery [E6]. A late trip requires shin obstacle contact, gait phase close to the end, and sufficient absolute swing-leg advance; the thresholds are searly = 0.66 and qearly = 190 deg [E7]. In that case, the current controller is left unchanged until swing-foot ground contact, then the ensuing step applies recovery [E8]. An early trip occurs before or during mid-gait, or with insufficient swing-leg advance, and rapidly bends the swing knee by repositioning the swing leg-shape motor so the leg can clear a 10 cm obstacle [E9]. If elevation fails, recovery is applied at the next step after checking swing-foot height and horizontal advance; a stuck foot is identified by near-zero horizontal advance and height within Delta H, with Delta H set to 0.05 m [E10].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用「top-level stance phases RW/SD/SU/TR」和「Inside TR, a separate reflex FSM routes tripping-start...」暴露了弱层次结构，但原文只支持 TR 内部 reflex FSM 与 tripping-start 图示，不支持更强的完整默认 init 链 [E2][E6]。
- **G 守卫算术**：G 钩子集中在 gait phase、swing-toe height、absolute swing-leg angle、horizontal advance、Delta H 等具名变量的复合阈值条件，尤其是 RW/SD/SU、late trip 与 failed elevation 判断 [E4][E7][E10]。
- **A 动作**：A 钩子体现在 late trip 保持当前控制器直到触地后切 recovery，以及 early trip 通过 repositioning swing leg-shape motor 快速弯膝清障 [E8][E9]。
- **F 故障恢复**：原文支持局部绊倒恢复路径，即 TR 内 rapid-lowering/rapid-elevation 失败后进入 recovery；但不支持从任意状态进入全局 emergency safe-state 的横切故障恢复 [E6][E8][E10]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain、multivar-guard、implicit-action-prose 和 composite-internal 几类 baseline 失败模式：机器人步态术语、复合数值守卫、散叙述动作和 TR 内部 FSM 分布在多句中 [E4][E6][E7][E9]。
- **ft fcstm-fit**：pyfcstm 适配点主要是 Expr-IR/SMT 风格的多变量数值守卫和 effector-agnostic abstract action；forced+aspect 全局横切优势覆盖弱，因为原文没有全局 emergency 或 per-tick aspect [E4][E7][E9][E10]。

</details>

<details><summary>provenance (10条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Abstract | paper_content.txt 行 5-10
    - quote: "allows MABEL, a kneed planar bipedal robot with 1 m-long legs"
    - supports: MABEL 机器人对象、1 m 腿长、未知地形高度变化输入
- `[E2]` STM §1 摘录 B | paper.pdf p.9 Section V | paper_content.txt 行 924-935
    - quote: "regular-walking phase (RW), step-down phase (SD), step-up phase (SU), and tripping phase (TR)"
    - supports: 顶层 FSM 的四个控制相位和控制器切换
- `[E3]` STM §1 摘录 C | paper.pdf p.9 Section V | paper_content.txt 行 936-955
    - quote: "values of the contact switches at the front and end of each leg"
    - supports: 转移决策使用腿部前端/末端接触开关和冲击时高度估计
- `[E4]` STM §1 摘录 C | paper.pdf p.9 Section V | paper_content.txt 行 956-965
    - quote: "being less than -Delta H, or larger than Delta H, respectively"
    - supports: RW/SD/SU 的 Delta H、-Delta H、+Delta H 数值守卫方向
- `[E5]` STM §1 摘录 C | paper.pdf p.9 Section V | paper_content.txt 行 966-968
    - quote: "transition to TR arises when the swing leg trips over obstacles or touches the ground prematurely"
    - supports: 障碍绊倒或过早触地触发 TR
- `[E6]` paper.pdf p.6 Figure 5 and caption | paper_content.txt 行 532-538, 609-613
    - quote: "Fig. 5: Finite-state machine of tripping-reflex controller"
    - supports: TR 内部存在单独的 tripping-reflex FSM，含 tripping-start、rapid-lowering、rapid-elevation、recovery
- `[E7]` paper.pdf p.5-6 Section IV-B3 | paper_content.txt 行 522-540
    - quote: "searly and qearly are set to 0.66 and 190 deg"
    - supports: late tripping 的复合条件和两个阈值
- `[E8]` STM §1 摘录 D | paper.pdf p.6 Section IV-B3 | paper_content.txt 行 541-548
    - quote: "The controller is not changed until the swing foot touches the ground"
    - supports: late tripping 的动作：保持控制器直到触地，然后下一步 recovery
- `[E9]` STM §1 摘录 D | paper.pdf p.6 Section IV-B3 | paper_content.txt 行 556-578
    - quote: "Rapid-elevation of the swing leg is accomplished by rapidly bending the swing knee"
    - supports: early tripping 的动作、腿形电机重定位和 10 cm obstacle clearance
- `[E10]` paper.pdf p.6 Section IV-B3 | paper_content.txt 行 579-608
    - quote: "Delta H in R is a scalar threshold value, which is set to 0.05m"
    - supports: rapid-elevation 失败后的 recovery 条件、水平前进近零、Delta H=0.05 m

</details>

- **intentional omissions**：未写全局 emergency stop、safe shutdown、从任意状态强制恢复等 F 轴横切路径，因为原文只给 TR 内部 recovery 而没有全局故障转移。也未扩展全部 Figure 10 转移边和所有控制器参数，避免把图表枚举和优化细节注入为需求。

### #13 🌡️ `optimization-control-energy-management-system-microgrids__01` (FSM)

- **case**: Five-mode microgrid EMS switch-breaker supervisor
- **统计**：261 词 / 19 markers / 19 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> An EMS finite-state controller governs a grid-connected residential microgrid through five main operating modes over configuration states defined by the utility-grid transfer switch, EMS breaker, and grid-power indicator [E1][E2]. The modes are higher-level groupings of lower-level switch states; the two switches use Closed, Fault-opening, and Manual-opening values, while the grid indicator records stable power versus off or unstable power [E3][E4][E5]. In grid-connected operation, the high-level EMS controller commands the low-level inverter to charge or discharge the battery at the desired power [E6]. If the battery or EMS inverter malfunctions or is under service, Grid-only behavior opens the breaker connecting EMS to the microgrid [E7]. When utility-grid power is down or unstable, Islanding opens the grid transfer switch, isolates the microgrid, and uses the EMS inverter as a voltage-source inverter to maintain bus voltage, frequency, and power balance [E8][E9]. Synchronization permits return from islanded operation only after the microgrid and grid match in magnitude, frequency, and phase [E10]. Outage applies when both the utility grid and EMS battery packs lack power; the control unit stays active on reserved power and prepares to switch to the correct mode when power returns [E11][E12]. The relay-level guards sense grid current and voltage, trip the transfer switch from Closed to Fault-opening on outage or voltage instability, and allow EMS-directed reclosure from Fault-opening to Closed after a cleared fault, but not from Manual-opening to Closed [E13][E14][E15]. In the grid-failure simulation, grid voltage falls to about 10% nominal, the converter switches to islanding, and after grid recovery the EMS synchronizes the microgrid before reconnecting without current surge [E16][E17][E18][E19].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用“modes are higher-level groupings of lower-level switch states”暴露了 red-circle mode 对 blue-box configuration states 的分组层次 [E5]，但原文未给进入某 mode 后的默认 init 子状态，所以 H 只有分组层次覆盖。
- **G 守卫算术**：G 钩子集中在 relay-level guards：grid current/voltage sensing、outage or voltage instability 触发 C→F、fault cleared 后 F→C 且 M→C 禁止，以及 grid voltage about 10% nominal 的仿真条件 [E13][E14][E15][E16]。
- **A 动作**：A 钩子包括 inverter charge/discharge command、Grid-only opening EMS breaker、Islanding opening transfer switch/isolation/VSI voltage-frequency-power-balance control [E6][E7][E8][E9]。
- **F 故障恢复**：原文支持 fault recovery 路径：Outage 保留控制单元监控并等待电源恢复，grid failure 后切 islanding、grid recovery 后同步并无冲击重连 [E11][E12][E17][E18][E19]；但无显式 from-any-state global escape。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拼接（§5.5 mode controller + §5.6.3 grid-failure simulation）、implicit-action-prose（open breaker/switch、charge/discharge、sync/reconnect）和 multivar-guard（current/voltage、magnitude/frequency/phase）[E6][E8][E10][E13][E18]。
- **ft fcstm-fit**：pyfcstm 适配点主要是 composite mode grouping、离散 switch-state guard 与 voltage threshold、以及 breaker/transfer-switch/inverter 这类可抽象为硬件解耦 action 的 effector [E2][E5][E13][E14][E16]；forced+aspect 横切优势覆盖弱，因为原文没有任意状态强制转移。

</details>

<details><summary>provenance (19条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf PDF p.107 (thesis p.90) §5.5.1 | paper_content.txt 行 2122-2124
    - quote: "the operation of a grid-connected microgrid with EMS is classified into five main operating modes"
    - supports: five main operating modes
- `[E2]` STM §1 摘录 C | paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2171-2173
    - quote: "The state variables are the state of utility grid transfer switch, EMS breaker and grid power indicator."
    - supports: configuration states defined by the utility-grid transfer switch, EMS breaker, and grid-power indicator
- `[E3]` STM §1 摘录 C | paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2174-2175
    - quote: "Utility grid transfer switch has three states, Closed(C), Fault opening(F), and Manual opening(M)."
    - supports: switch values Closed, Fault-opening, and Manual-opening
- `[E4]` STM §1 摘录 C | paper.pdf PDF p.110 (thesis p.93) §5.5.1 | paper_content.txt 行 2184-2185
    - quote: "Grid power indicator has two values: Grid has power and stable(Y), grid is power off or unstable(N)."
    - supports: grid indicator records stable power versus off or unstable power
- `[E5]` STM §1 摘录 D | paper.pdf PDF p.110 (thesis p.93) §5.5.1 | paper_content.txt 行 2186-2191
    - quote: "The red circles represent the modes of the system, which include groups of states with similar meaning."
    - supports: modes are higher-level groupings of lower-level switch states
- `[E6]` paper.pdf PDF p.108 (thesis p.91) §5.5.1 | paper_content.txt 行 2143-2144
    - quote: "command the low-level EMS inverter to either charge or discharge the battery to achieve the desired charge/discharge power."
    - supports: high-level EMS controller commands the low-level inverter to charge or discharge the battery
- `[E7]` STM §1 摘录 A | paper.pdf PDF p.108 (thesis p.91) §5.5.1 | paper_content.txt 行 2145-2148
    - quote: "the controller would open the breaker connecting the EMS to the microgrid, and enters a Grid-only operation mode."
    - supports: Grid-only behavior opens the breaker connecting EMS to the microgrid
- `[E8]` STM §1 摘录 A | paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2155-2156
    - quote: "open the grid transfer switch. The microgrid is isolated from the utility grid and operates in islanding mode."
    - supports: Islanding opens the grid transfer switch and isolates the microgrid
- `[E9]` paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2156-2160
    - quote: "The main function of EMS in this mode is to maintain the microgrid voltage and frequency, and power balance between generation and consumption."
    - supports: uses the EMS inverter as a voltage-source inverter to maintain bus voltage, frequency, and power balance
- `[E10]` STM §1 摘录 B | paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2161-2165
    - quote: "EMS would ensure that the magnitude, frequency and phase of the microgrid and grid are the same."
    - supports: Synchronization permits return only after magnitude, frequency, and phase match
- `[E11]` STM §1 摘录 B | paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2166-2167
    - quote: "This system enters this mode when both utility grid and EMS battery packs are out of power."
    - supports: Outage applies when both utility grid and EMS battery packs lack power
- `[E12]` STM §1 摘录 B | paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2167-2170
    - quote: "the EMS control unit is still active and monitors the system with reserved power, preparing for switching to the correct mode when power comes back"
    - supports: control unit stays active on reserved power and prepares to switch when power returns
- `[E13]` paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2174-2176
    - quote: "The transfer switch has build-in relay which senses utility grid current and voltage."
    - supports: relay-level guards sense grid current and voltage
- `[E14]` paper.pdf PDF p.109 (thesis p.92) §5.5.1 | paper_content.txt 行 2176-2177
    - quote: "In case of grid power outage and voltage instability, the transfer switch would trip from C to F."
    - supports: trip the transfer switch from Closed to Fault-opening on outage or voltage instability
- `[E15]` paper.pdf PDF p.110 (thesis p.93) §5.5.1 | paper_content.txt 行 2182-2183
    - quote: "The EMS could direct the transfer switch to reclose from F to C when a fault is cleared, but not from M to C."
    - supports: EMS-directed reclosure from Fault-opening to Closed after a cleared fault, but not from Manual-opening to Closed
- `[E16]` paper.pdf PDF p.116 (thesis p.99) §5.6.3 | paper_content.txt 行 2244-2247
    - quote: "a grid failure occurs which drops its voltage to about 10% of nominal voltage."
    - supports: grid voltage falls to about 10% nominal
- `[E17]` paper.pdf PDF p.116 (thesis p.99) §5.6.3 | paper_content.txt 行 2248-2251
    - quote: "the controller of the EMS converter is switched to islanding mode."
    - supports: the converter switches to islanding
- `[E18]` paper.pdf PDF p.116 (thesis p.99) §5.6.3 | paper_content.txt 行 2253-2257
    - quote: "When EMS detects the recovery of utility grid, it starts to synchronize the microgrid voltage to that of the utility grid."
    - supports: after grid recovery the EMS synchronizes the microgrid
- `[E19]` paper.pdf PDF p.116 (thesis p.99) §5.6.3 | paper_content.txt 行 2257-2258
    - quote: "No current surge is observed at the moment of reconnection"
    - supports: reconnecting without current surge

</details>

- **intentional omissions**：未加入原文没有的默认初始子状态、全局 emergency stop/forced safe-state、具体阀门编号或传感器型号。仿真中的部分精确时间点没有全部写入 expanded_nl，避免把单次仿真参数误写成控制器硬阈值。

### #14 ✈️ `automated-contingency-management-in-unmanned-aircraft-systems__01` (FSM)

- **case**: Centralized Safety Monitor FSM
- **统计**：274 词 / 17 markers / 17 provenance entries
- **轴覆盖**：⚪ H 层次 / ⚪ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The centralized Safety Monitor is the strategic safety gatekeeper in the UAS automatic contingency-management architecture: during the mission it checks for unsafe states and decides whether the resulting condition can be handled by the Contingency Manager or must instead trigger the Flight Termination System [E1]. Its FSM has one nominal mode, five abnormal contingency modes, and one emergency mode named Out of control [E2]; a single contingency is abnormal [E3], while nested contingencies or any emergency event enter the emergency state and require instant flight termination [E4]. The abnormal entry conditions are event-style guards over domain signals: C2 link loss enters Autonomous operation [E5], and the other listed contingencies include GNSS performance loss, in-flight control loss, separation loss, and mission-boundary violation [E6]. Recovery is modeled only from abnormal modes back to Nominal operation [E7], whereas Out of control is unrecoverable and has no outgoing transition [E8]. A global escape rule is required: from any non-emergency monitor state, there must always be a one-step transition to Out of control, preserving the ability to trigger flight termination [E9]. In the CS2 trace, the C2 link-loss signal is injected at t=1,864 s and the monitor receives that contingency signal before entering Autonomous operation [E10] [E11]. After that abnormal classification, the SMMS disengages the nominal goal and switches to the remote-pilot-approved C2 link-loss policy [E12]; the later procedure is a climb maneuver trying to regain the C2 link signal with a 10 min time slot [E13] [E14]. When the regain signal restores the C2 link before that time limit [E15], the contingency signal is deactivated at t=2,733 s [E16] and the Safety Monitor returns to Nominal operation [E17].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：原文无显式层次结构、复合状态或默认 init 语义；expanded_nl 只保留 nominal / abnormal / emergency 的平铺分类 [E2]，未提供 H 轴覆盖。
- **G 守卫算术**：原文不支持具体多变量算术守卫；expanded_nl 仅暴露事件/阈值式条件，如 C2 link-loss signal、single vs nested contingency/emergency event、10 min time slot before regain [E3][E4][E5][E14][E15]，G 轴覆盖较弱。
- **A 动作**：A 钩子体现在 Safety Monitor 对 Contingency Manager / Flight Termination System 的系统级决策动作 [E1][E9]，以及 SMMS disengages nominal goal 并 switches to C2 link-loss policy 的非平凡任务动作 [E12]。
- **F 故障恢复**：F 钩子较强：异常状态可 recovery 回 Nominal operation [E7]，任意非应急状态保留一步到 Out of control 的全局逃逸用于 flight termination [E9]，CS2 中 regain signal 后返回 Nominal operation [E15][E17]。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拼合（架构、模型要求、仿真轨迹）[E1][E9][E10]、implicit-domain 术语（C2/GNSS/FTS/SMMS）[E5][E6][E12]、global-cross-cutting 逃逸规则 [E9] 和 implicit-action-prose [E12]。
- **ft fcstm-fit**：pyfcstm 独占优势主要落在 forced transition / global escape 到 Out of control [E9] 与 effector-agnostic abstract action 风格的 FTS/SMMS 系统级动作 [E1][E12]；原文无深复合 init 链和多变量 SMT 守卫。

</details>

<details><summary>provenance (17条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf pp.97-98 §4.3 | paper_content.txt 行 3084-3104
    - quote: "whether a contingency management option is feasible, or whether the flight termination action is required instead"
    - supports: Safety Monitor decides between Contingency Manager handling and Flight Termination System action
- `[E2]` STM §1 摘录 B | paper.pdf p.254 §A.2 | paper_content.txt 行 8152-8155
    - quote: "The proposed FSM has seven states: the nominal state (S1), five abnormal states (S2 to S6, one per contingency under study) and one emergency state"
    - supports: one nominal mode, five abnormal contingency modes, and one emergency mode
- `[E3]` STM §1 摘录 B | paper.pdf p.254 §A.2 | paper_content.txt 行 8147-8149
    - quote: "one single contingency results in an abnormal state"
    - supports: single contingency is abnormal
- `[E4]` STM §1 摘录 B | paper.pdf p.254 §A.2 | paper_content.txt 行 8149-8151
    - quote: "any combination of nested contingencies or the occurrence of an emergency event results in an emergency state; emergency states require instant flight termination."
    - supports: nested contingencies or emergency events enter emergency state and require flight termination
- `[E5]` STM §1 摘录 B | paper.pdf p.254 §A.2 | paper_content.txt 行 8155-8157
    - quote: "Autonomous operation (S2) is entered after the C2 link loss"
    - supports: C2 link loss enters Autonomous operation
- `[E6]` STM §1 摘录 B | paper.pdf p.254 §A.2 | paper_content.txt 行 8135-8140
    - quote: "GNSS loss of performance 3. Loss of control in-flight 4. Loss of separation 5. Mission boundary limits violation"
    - supports: other listed contingency signals
- `[E7]` paper.pdf p.255 §A.2 | paper_content.txt 行 8161-8163、8189-8190
    - quote: "transitions where i > j represent recovery events: events that make the system to evolve from an abnormal state to the nominal state."
    - supports: recovery from abnormal modes back to Nominal operation
- `[E8]` STM §1 摘录 C | paper.pdf p.255 §A.2 | paper_content.txt 行 8189-8192
    - quote: "when this state is entered, no transition can make the system to evolve to a different state."
    - supports: Out of control is unrecoverable with no outgoing transition
- `[E9]` STM §1 摘录 C | paper.pdf p.255 SM1 | paper_content.txt 行 8195-8197
    - quote: "in one step. In other words, the Safety Monitor should always be able to trigger the flight termination action."
    - supports: global one-step escape to Out of control for flight termination
- `[E10]` STM §1 摘录 D | paper.pdf p.222 §7.3.3 | paper_content.txt 行 7220-7224
    - quote: "the C2 link loss signal is injected at time t = 1 864 s"
    - supports: CS2 C2 link-loss injection time
- `[E11]` STM §1 摘录 D | paper.pdf p.222 §7.3.3 | paper_content.txt 行 7222-7224
    - quote: "receives the corresponding contingency signal and enters the “Autonomous operation” state"
    - supports: monitor receives contingency signal and enters Autonomous operation
- `[E12]` paper.pdf p.222 §7.3.3 | paper_content.txt 行 7232-7235
    - quote: "the SMMS disengages the nominal goal and switches to the C2 link loss policy approved by the remote pilot"
    - supports: SMMS disengages nominal goal and switches to approved C2 link-loss policy
- `[E13]` paper.pdf p.223 §7.3.3 | paper_content.txt 行 7259-7263
    - quote: "a climb maneuver trying to regain the C2 link signal"
    - supports: climb maneuver to regain the C2 link signal
- `[E14]` paper.pdf p.224 §7.3.3 | paper_content.txt 行 7283-7284
    - quote: "the time slot allowed to try to regain the signal is 10 min in this case"
    - supports: 10 min time slot
- `[E15]` paper.pdf p.224 §7.3.3 | paper_content.txt 行 7285-7287
    - quote: "the “regain signal” is effective at recovering the C2 link before the time limit occurs"
    - supports: regain signal restores C2 link before the time limit
- `[E16]` paper.pdf p.224 §7.3.3 | paper_content.txt 行 7287-7288
    - quote: "the contingency injection signal is deactivated at time t = 2, 733 s"
    - supports: contingency signal deactivated at t=2,733 s
- `[E17]` STM §1 摘录 D | paper.pdf p.224 §7.3.3 | paper_content.txt 行 7288-7290
    - quote: "the Safety Monitor returns to the “Nominal operation” state"
    - supports: Safety Monitor returns to Nominal operation

</details>

- **intentional omissions**：没有加入层次 mode、默认子状态 init、阀门/传感器编号、具体硬件执行器或多变量算术 guard，因为原文不支持这些内容。也没有逐个枚举全部 7 个 state name，只保留关键 mode 和状态类别，避免把任务退化为 state list 复述。

### #15 🚗 `full-automated-drive-urban-environments-gomentum-station__01` (HSM)

- **case**: Urban automated-driving event supervisor for traffic lights, intersections, pedestrians, and roadwork
- **统计**：278 词 / 18 markers / 18 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The urban automated-driving event supervisor is a hierarchical state machine that reasons over events from the Event Handler and uses top-level modes such as `GO` and `STOP`, where `GO` instructs the Trajectory Planner to proceed in the current lane at a suitable speed and `STOP` means the car must come to a stop [E1][E2][E3]. Each received event is assessed for a `MUST STOP` flag: `PEDESTRIAN`, `TFL RED`, and `INT` events all switch the supervisor into `STOP`, and the latest events of those three types are stored as stop requirements [E4]. In `STOP`, a traffic-light requirement waits for `TFL GREEN`, a pedestrian requirement waits for `PED CLEAR`, and an intersection requirement waits until the lowest cross-traffic TTC exceeds a threshold for a number of consecutive iterations; TTC is calculated from closing distance and closing velocity [E5][E6]. The hierarchy also includes a communication sub-state machine: `BUSY` means a connection request has been sent and a response is expected, `IDLE` is reached after response or timeout, and failure or timeout events provide feedback for error recovery [E7][E8][E9]. Periodic messages serve as heartbeats so the state machine monitors process health, while unhandled errors send the vehicle to `ERROR` and disengage automated driving [E10][E11]. In demonstrated scenarios, cameras detect signalized traffic lights and resume `GO` on green; LiDAR recognizes construction pylons and, if a feasible solution exists, the vehicle moves laterally around them; vision-LiDAR pedestrian detection issues `PEDESTRIAN` and keeps the vehicle in `STOP` until `PED CLEAR` [E12][E13][E14][E15][E16][E17]. At the control layer, a proprietary controller calculates steering, throttle, and braking commands from trajectory points, while the state-machine layer handles the event and requirement logic that decides when `GO` or `STOP` is active [E18][E4].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴部分覆盖：expanded_nl 通过顶层 `GO`/`STOP` 与 `BUSY`/`IDLE` 通信子状态机暴露层次结构，但原文没有说明默认 init 子状态，因此未写 init 链 [E1][E7][E8]。
- **G 守卫算术**：G 轴覆盖在 `STOP` 的 intersection requirement：具名变量 TTC 必须超过阈值并持续若干次迭代，且 TTC 由 closing distance/velocity 计算 [E5][E6]。
- **A 动作**：A 轴覆盖包括 `GO` 中指令 Trajectory Planner、`STOP` 中存储 requirement、施工区 lateral maneuver，以及底层 steering/throttle/braking command [E2][E4][E15][E18]。
- **F 故障恢复**：F 轴部分覆盖：failure/timeout events 提供 error recovery 反馈，heartbeat 监控 process health，unhandled errors 进入 `ERROR` 并 disengage AD；原文不支持任意状态 emergency forced transition [E9][E10][E11]。
- **bd baseline-trap**：bd 命中 implicit-domain 事件术语、multivar/threshold TTC guard、composite-internal 通信子状态机与 heartbeat 横切监控等 baseline 易失误点 [E4][E5][E7][E10]。
- **ft fcstm-fit**：ft 主要落在 TTC 的 Expr-IR/SMT 数值守卫、heartbeat 的 per-tick aspect 风格监控、steering/throttle/braking 的 abstract action effector 解耦；深复合 init 与 forced reset 证据不足 [E5][E6][E10][E18]。

</details>

<details><summary>provenance (18条)</summary>

- `[E1]` STM §1 摘录 B | paper.pdf p.5 §V.A State Machine | paper_content.txt 行 465
    - quote: "We use a hierarchical state machine for level reasoning, from events that are generated by the Event Handler."
    - supports: hierarchical state machine reasoning over Event Handler events
- `[E2]` paper.pdf p.5 §V.A State Machine | paper_content.txt 行 468-470
    - quote: "In GO state, the Trajectory Planner is instructed to go in the current lane with suitable speed."
    - supports: `GO` mode action instructing the trajectory planner
- `[E3]` STM §1 摘录 B | paper.pdf p.5 §V.A State Machine
    - quote: "STOP: State when the car has to come to a stop"
    - supports: `STOP` mode meaning that the car must stop
- `[E4]` STM §1 摘录 C | paper.pdf p.5 §V.A State Machine | paper_content.txt 行 470-475
    - quote: "PEDESTRIAN, TFL RED or INT (intersection) events all trigger the switch to STOP. The latest events from these three event types are stored in memory"
    - supports: `MUST STOP` event classes, transition to `STOP`, and stored stop requirements
- `[E5]` STM §1 摘录 E | paper.pdf p.6 §V.C Behavior Planning | paper_content.txt 行 554-563
    - quote: "If the TTC exceeds a threshold for a number of consecutive iterations, then the INT OK event is issued."
    - supports: intersection guard using lowest TTC threshold over consecutive iterations
- `[E6]` paper.pdf p.6 §V.C Behavior Planning | paper_content.txt 行 563-568
    - quote: "Then the TTC is calculated as dclosing /vclosing, where dclosing is the lateral distance in the left-right direction."
    - supports: TTC calculation from closing distance and closing velocity
- `[E7]` STM §1 摘录 D | paper.pdf p.5 §V.A State Machine | paper_content.txt 行 497-500
    - quote: "BUSY sub-state means a request for connection has been sent for that state and a response is expected."
    - supports: `BUSY` communication sub-state semantics
- `[E8]` paper.pdf p.5 §V.A State Machine | paper_content.txt 行 500-502
    - quote: "Sub-state machines goes into IDLE when a response is received or a timeout occurs."
    - supports: `IDLE` after response or timeout
- `[E9]` paper.pdf p.5 §V.A State Machine | paper_content.txt 行 502-505
    - quote: "These situations raise either failure or timeout events, which gives the state machine feedback for error recovery."
    - supports: failure/timeout events as feedback for error recovery
- `[E10]` paper.pdf p.5 §V.A State Machine | paper_content.txt 行 506-508
    - quote: "The processes send periodic messages that also serves as a heartbeat message, so that the state machine monitors the health of the processes"
    - supports: heartbeat monitoring of process health
- `[E11]` paper.pdf p.5 §V.A State Machine | paper_content.txt 行 481-485
    - quote: "Errors that are not handled by the state machine cause the vehicle to go to ERROR state, and leads to disengagement from AD."
    - supports: unhandled errors lead to `ERROR` and AD disengagement
- `[E12]` paper.pdf p.7 §VI.A Scenario 1 | paper_content.txt 行 675-678
    - quote: "On-board cameras detect the traffic light state, which is initially green on approach to the intersection."
    - supports: camera-detected signalized traffic lights
- `[E13]` paper.pdf p.7 §VI.A Scenario 1 | paper_content.txt 行 685-687
    - quote: "Once the green light is detected, the TFL GREEN event is sent and the vehicle resumes to the GO state."
    - supports: green light clears traffic-light requirement and resumes `GO`
- `[E14]` paper.pdf p.7 §VI.C Scenario 3 | paper_content.txt 行 704-706
    - quote: "Pylons on the road are recognized using LiDAR, and determines that it is neither a pedestrian nor a vehicle."
    - supports: LiDAR recognition of construction pylons
- `[E15]` paper.pdf p.7 §VI.C Scenario 3 | paper_content.txt 行 713-718
    - quote: "If a feasible solution is found, the vehicle smoothly moves laterally from the lane center to avoid the pylons"
    - supports: construction-zone trajectory action around pylons
- `[E16]` paper.pdf p.8 §VI.D Scenario 4 | paper_content.txt 行 727-732
    - quote: "Using the vision-LiDAR sensing modality, the vehicle detects a pedestrian near the roadway and issues a PEDESTRIAN event"
    - supports: vision-LiDAR pedestrian detection issuing `PEDESTRIAN`
- `[E17]` paper.pdf p.8 Fig. 8 / §VI.D Scenario 4 | paper_content.txt 行 721-724
    - quote: "vehicle remains in STOP state until the pedestrian is cleared."
    - supports: pedestrian handling keeps vehicle in `STOP` until cleared
- `[E18]` paper.pdf p.6 §V.E Vehicle Control | paper_content.txt 行 635-638
    - quote: "We use a propriety controller for calculation of the steering/throttle and braking commands on the vehicle."
    - supports: physical control effectors: steering, throttle, and braking commands

</details>

- **intentional omissions**：未补写具体 TTC 阈值、连续迭代次数、传感器型号或执行器编号，因为原文没有给出这些参数。也未写“任意状态 emergency stop 强制进入 Safe mode”或默认 init 子状态链，因为原文只支持 ERROR/disengagement、failure/timeout recovery 和 heartbeat 监控。

## 备选 Backup 15

### #1 ✈️ `long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition__01` (HSM)

- **case**: Master-and-Autopilot Mission Cycle for Autonomous Rotorcraft UAS
- **统计**：273 词 / 14 markers / 14 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The autonomy engine controls a rotorcraft UAS for repeated observation flights without human intervention, with high-level decisions implemented as a hierarchy of master and slave state machines [E1][E2]. The master coordinates the takeoff, mission, landing, and emergency-landing states by activating the phase-specific autopilot and waiting for it to complete [E3], and it can abort an autopilot when robust behavior is needed [E4]. The takeoff autopilot starts from a motors-off vehicle on the charging pad [E5]; before climb it validates battery voltage and motor performance [E6], reinitializes the state estimator after charging, saves the launch location in permanent memory [E7], and commands velocity-controlled climb to the target altitude [E8]. Its motor check spins the motors at low RPM, requires measured speed within 400 RPM of nominal, and aborts takeoff after ten failed attempts [E9]. The mission autopilot flies user-defined waypoints and hover times through the guidance subsystem until the route completes or low battery requests return to the charging pad [E10]. The landing autopilot checks the downfacing navigation camera for any AprilTag in the pad bundle and performs a spiral grid search when the bundle is not visible [E11], then aligns yaw and lateral position over the pad center and descends until height is below 0.3 m and vertical speed is below 0.1 m/s [E12]. If battery voltage becomes critically low, mission or landing can be aborted and the emergency lander performs an in-place soft touchdown with a 0.3 m/s descent and 0.1 m/s velocity threshold [E13]. During mission execution, a health observer monitors critical components and issues fail-safe emergency messages such as return-to-home or emergency landing on low battery or state-estimation failure [E14].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 在 [E1][E2][E3] 暴露 master/slave state machines 与 phase-specific autopilot 调度关系，[E5] 给出 takeoff autopilot 的进入起点，形成 H 轴覆盖。
- **G 守卫算术**：G 钩子主要在 [E9] 的 400 RPM 偏差与 ten attempts abort，以及 [E12][E13] 的高度/速度 touchdown 阈值；均以具名物理量自然语言表达。
- **A 动作**：A 钩子包括 [E3][E4] 的 activate/wait/abort，[E7][E8] 的 estimator reinit、memory save、velocity climb，以及 [E11][E12] 的 camera search、alignment、descent。
- **F 故障恢复**：F 钩子在 [E4][E13][E14]：master 可 abort autopilot，critically low battery 触发 emergency lander，health observer 发出 fail-safe emergency messages。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain、implicit-action-prose、multivar-guard 与 global-cross-cutting 失败模式，集中体现在 rotorcraft/AprilTag 术语、散叙述动作、touchdown 复合阈值和健康监控/abort 规则 [E7]-[E14]。
- **ft fcstm-fit**：pyfcstm fit 较强：层次 master/slave 与 autopilot 进入点适配深复合 init [E2][E3][E5]，数值守卫适配 Expr-IR/SMT [E9][E12][E13]，abort/emergency 语义适配 forced recovery [E4][E13][E14]；原文不支持每 tick aspect。

</details>

<details><summary>provenance (14条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Abstract
    - quote: "performing repeated flights for long-term observation missions without any human intervention"
    - supports: UAS performs repeated observation flights without human intervention
- `[E2]` STM §1 摘录 A | paper.pdf p.1 Abstract
    - quote: "High-level autonomous decision making is implemented as a hierarchy of master and slave state machines."
    - supports: high-level decisions are hierarchical master/slave state machines
- `[E3]` STM §1 摘录 B | paper.pdf p.20 §7.2
    - quote: "activates the appropriate autopilot and waits for it to complete"
    - supports: master activates phase-specific autopilot and waits
- `[E4]` STM §1 摘录 B | paper.pdf p.20 §7.2
    - quote: "abort each autopilot in order to execute robust behaviors"
    - supports: master can abort an autopilot for robust behavior
- `[E5]` STM §1 摘录 B | paper.pdf p.20 §7.3
    - quote: "from a motors-off state on the charging pad to a hover"
    - supports: takeoff starts from motors-off vehicle on charging pad
- `[E6]` STM §1 摘录 A | paper.pdf p.10 §3.3
    - quote: "adequate battery voltage level and motor nominal performance"
    - supports: pre-takeoff battery-voltage and motor-performance validation
- `[E7]` STM §1 摘录 B | paper.pdf p.20 §7.3
    - quote: "re-initializing the state estimator after the prolonged charging phase and memorizing the current horizontal location in permanent memory"
    - supports: state-estimator reinitialization and launch-location memory action
- `[E8]` STM §1 摘录 B | paper.pdf p.20 §7.3
    - quote: "commands a velocity-controlled takeoff that takes it from the initial position on the charging pad to a target altitude."
    - supports: velocity-controlled climb to target altitude
- `[E9]` STM §1 摘录 B | paper.pdf p.20 §7.3
    - quote: "verified to rotate within 400 RPM of the nominal value. Ten attempts to pass this check are allowed"
    - supports: RPM deviation guard and ten-attempt abort condition
- `[E10]` paper.pdf p.21 §7.4 | paper_content.txt 行 518-520
    - quote: "individual waypoints and hover times; low battery charge requests the UAS to return to the charging pad"
    - supports: mission waypoints/hover-times and low-battery return request
- `[E11]` STM §1 摘录 C | paper.pdf p.21 §7.5
    - quote: "if any AprilTag in the bundle is detected. If not, the UAS executes the spiral grid search trajectory"
    - supports: camera AprilTag check and spiral-grid-search fallback
- `[E12]` STM §1 摘录 C | paper.pdf p.23 §7.5
    - quote: "align the vehicle’s lateral position over the center of the charging pad; 0.3 m height and 0.1 m/s velocity thresholds"
    - supports: alignment over pad center and conjunctive touchdown thresholds
- `[E13]` STM §1 摘录 C | paper.pdf p.23 §7.6
    - quote: "triggered in response to a critically low battery voltage; mild vertical velocity of 0.3 m/s; 0.1 m/s velocity threshold"
    - supports: critical-battery emergency landing and descent/touchdown thresholds
- `[E14]` paper.pdf p.10 §3.3
    - quote: "system health observer monitors all critical components of the UAS and issues emergency messages"
    - supports: health observer monitors components and issues fail-safe emergency messages

</details>

- **intentional omissions**：未加入原文没有明确支持的 per-cycle watchdog/aspect、forced reset、额外传感器型号或执行器编号。也未逐个枚举 Figure 17/18 的全部 state/flowchart node，以避免把任务退化为状态清单复述。

### #2 ✈️ `methodology-to-develop-a-discrete-event-supervisory-controller-for-an-autonomous-helicopter-flight__01` (HSM)

- **case**: Takeoff-on-route-landing supervisory flow for Bell 412 autonomy
- **统计**：281 词 / 22 markers / 22 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The Bell 412 autonomy supervisor is a state-based, event-driven controller for the autonomous mission from takeoff to landing; it uses inputs from the FCC, mission manager, pilot, aircraft, and LIDAR landing-zone evaluation so the mission avoids unacceptable outcomes such as landing on an obstacle when no suitable landing point is found [E1] [E2] [E3] [E4] [E5]. Its top-level behavior is decomposed into Takeoff, On Route, and Landing: Takeoff initializes the mission and verifies autonomy status, On Route forwards reached waypoints to the FCC, and Landing governs the final segment until touchdown or pilot handover [E6] [E7] [E8] [E9]. For the landing behavior, the Landing Point Manager starts in IDLE and, when start_mission arrives, enters the waiting phase for landing [E10]. If the planned landing point is achieved on plp_ach before any landing point is received, the manager requests aircraft state, asks the helicopter to stabilize so the landing zone can be evaluated, and begins the scan; at START_LZE_SCAN it emits an FCC orbit command and updates the mission planning software, autonomy guidance, and mission-monitor status [E11] [E12] [E13]. If a landing point arrives before the PLP or during the scan, the manager requests aircraft state, starts the LP_APPROACH acceptance timer, publishes a new LP only when it is far enough from the previous LP, and rejects further LP updates once the timer expires [E14] [E15] [E16]. If no suitable landing point is found, it hands aircraft control to the pilot, and pilot takeover via pilot_takeover is allowed from any state [E17] [E18]. The supervisor expresses its external actions through output ports such as FCC command ports, LP update or expiry ports, mission-manager/mission-planning/autonomy-guidance update ports, and pilot notification [E19] [E20] [E21] [E22].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 通过 Takeoff / On Route / Landing 顶层分解，以及 Landing Point Manager 从 IDLE 等待 start_mission 后进入 landing waiting phase 的默认 init 线索暴露层次结构，[E6] [E7] [E8] [E9] [E10]。
- **G 守卫算术**：原文没有给具体数值阈值，expanded_nl 只保留 plp_ach / lp_recv 事件顺序、pilot_takeover 与 LP far enough from previous LP 的距离型自然守卫，G 轴算术覆盖较弱，[E11] [E14] [E15] [E18]。
- **A 动作**：A 钩子集中在 request_aircraft_state、stabilize、START_LZE_SCAN 输出 fcc_command_orbit/update_gcs/update_boss/set_mission_monitor_status、LP_new/LP_expired 等非平凡输出动作，[E11] [E12] [E13] [E14] [E15] [E16] [E19] [E20] [E21] [E22]。
- **F 故障恢复**：F 钩子为找不到 suitable LP 时 hand over control to the pilot，以及 pilot_takeover from any state 的全局接管路径，[E17] [E18]。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拆段、implicit-domain 航空/PLP/LP 术语、implicit-action-prose 散叙述输出动作与 global-cross-cutting pilot_takeover 这些 baseline 失败模式，[E3] [E5] [E11] [E13] [E17] [E18]。
- **ft fcstm-fit**：expanded_nl 暴露深复合 + init 链和 abstract action / effector 解耦，forced-like 全局逃逸由 pilot_takeover 支持；但原文缺少具体数值 SMT 守卫和 per-tick aspect，[E6] [E10] [E13] [E18] [E19] [E20] [E21] [E22]。

</details>

<details><summary>provenance (22条)</summary>

- `[E1]` paper.pdf Abstract | paper_content.txt 行 39-44
    - quote: "state-based, event-driven supervisory controller for autonomous rotorcraft"
    - supports: state-based, event-driven controller
- `[E2]` STM §1 摘录 C | paper_content.txt 行 360-363
    - quote: "We developed a supervisory controller for the entire autonomous mission, from take-off to landing."
    - supports: autonomous mission from takeoff to landing
- `[E3]` STM §1 摘录 C | paper_content.txt 行 367-369
    - quote: "LIDAR-based landing zone evaluation system will identify Landing Points (LPs) within the PLP radius"
    - supports: LIDAR landing-zone evaluation
- `[E4]` STM §1 摘录 C | paper_content.txt 行 371-373
    - quote: "receive inputs from the FCC, mission manager, pilot, and aircraft"
    - supports: uses inputs from the FCC, mission manager, pilot, and aircraft
- `[E5]` STM §1 摘录 B | paper_content.txt 行 132-135
    - quote: "landing on an obstacle if a suitable landing location is not found"
    - supports: avoids unacceptable outcomes when no suitable landing point is found
- `[E6]` STM §1 摘录 C | paper_content.txt 行 382-384
    - quote: "decomposed into 3 sub-components Takeoff, On Route, and Landing"
    - supports: top-level behavior is decomposed into Takeoff, On Route, and Landing
- `[E7]` STM §1 摘录 C | paper_content.txt 行 385-386
    - quote: "initialize the mission, verify the status of the autonomy system prior to takeoff"
    - supports: Takeoff initializes the mission and verifies autonomy status
- `[E8]` STM §1 摘录 C | paper_content.txt 行 387-388
    - quote: "forwarding of mission items (e.g., waypoints) to the flight control computer"
    - supports: On Route forwards reached waypoints to the FCC
- `[E9]` STM §1 摘录 C | paper_content.txt 行 389-390
    - quote: "until the helicopter has landed or handed control to the pilot"
    - supports: Landing governs the final segment until touchdown or pilot handover
- `[E10]` STM §1 摘录 D | paper_content.txt 行 462-463
    - quote: "The model is initialized in the IDLE state. It remains IDLE state until the start_mission is received"
    - supports: Landing Point Manager starts in IDLE and waits for start_mission
- `[E11]` STM §1 摘录 D | paper_content.txt 行 464-466
    - quote: "After the PLP is achieved the Landing Point Manager will request the aircraft state"
    - supports: on plp_ach before LP, requests aircraft state
- `[E12]` STM §1 摘录 D | paper_content.txt 行 466-468
    - quote: "the model requests for the helicopter to be stabilized, so the landing zone can be evaluated"
    - supports: asks the helicopter to stabilize for landing-zone evaluation
- `[E13]` paper.pdf p.10 Figure 6 | rendered figure check
    - quote: "fcc_command_orbit! update_gcs! update_boss! set_mission_monitor_status!"
    - supports: START_LZE_SCAN emits FCC orbit and update outputs
- `[E14]` STM §1 摘录 D | paper_content.txt 行 471-474
    - quote: "After an LP is received, the model then requests the aircraft state and starts the LP_APPROACH timer."
    - supports: LP arrival path requests aircraft state and starts LP_APPROACH timer
- `[E15]` STM §1 摘录 D | paper_content.txt 行 474-476
    - quote: "valid (located far enough from the previous LP), the model sends a new LP output"
    - supports: publishes new LP only when far enough from previous LP
- `[E16]` STM §1 摘录 D | paper_content.txt 行 476-477
    - quote: "will not allow any further updates to the LP"
    - supports: rejects further LP updates once the timer expires
- `[E17]` STM §1 摘录 D | paper_content.txt 行 468-469
    - quote: "hand over control of the aircraft to the pilot"
    - supports: no suitable LP found leads to pilot handover
- `[E18]` STM §1 摘录 D | paper_content.txt 行 477-479
    - quote: "pilot can take control of the helicopter at any state"
    - supports: pilot_takeover is allowed from any state
- `[E19]` paper.pdf p.13 §5.1 | paper_content.txt 行 566-568
    - quote: "message bags were constructed and sent to the output ports"
    - supports: external actions are expressed through output ports
- `[E20]` paper.pdf p.9 Table 2 | paper_content.txt 行 419-423
    - quote: "fcc_command_hover Sends hover command to the FCC; fcc_command_land Sends land command; fcc_command_orbit Sends orbit command"
    - supports: FCC command ports
- `[E21]` paper.pdf p.9 Table 2 | paper_content.txt 行 424-426
    - quote: "lp_expired Sends notification that the LP accept timer has expired; lp_new Sends new valid landing point"
    - supports: LP update or expiry ports
- `[E22]` paper.pdf p.10 Table 2 | paper_content.txt 行 432-441
    - quote: "notify_pilot Notifies the pilot; update_boss Sends updates to autonomy guidance; update_gcs Sends updates to the mission planning software"
    - supports: pilot notification and mission-planning/autonomy-guidance update ports

</details>

- **intentional omissions**：原文没有给 LP 距离阈值、LP_APPROACH 具体时长或 DEFAULT_ORBIT_RADIUS/VELOCITY 等数值，因此未写具体数值 guard。原文没有命名低层舵机、阀门等直接执行器，也没有 emergency stop / reset fault path，因此只保留 FCC 输出端口、pilot handover/takeover 与相关监督动作。

### #3 🚗 `odin-team-victortango-darpa-urban-challenge__01` (HSM)

- **case**: Winner-Takes-All Driving Behaviors with Parking and Replan Interrupts
- **统计**：280 词 / 21 markers / 21 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> Odin Driving Behaviors is a hierarchical FSM: a top-level classifier distinguishes normal-road, intersection, and parking-lot situations, with each behavior treated as a lower-level nested state machine [E1] [E2]. Its Behavior Integrator uses modified Winner-Takes-All arbitration and selects one winner per driver category [E3]; categories include target-point, speed, and lane drivers [E4]. Driving Behaviors outputs a behavior profile to Motion Planning with six target points, desired maximum speed, travel lane, and direction [E5], plus optional stop flag and desired heading [E6]; Vehicle Interface turns motion profiles into throttle, brake, steering, and shifting actions [E7], and can actuate lights, turn signals, and horn [E8]. On normal roads, passing monitors nearby vehicles and decides whether a safe legal pass is needed [E9], while route following can overrule a pass too close to an exit or intersection [E10]. The Blockage Driver maintains available lanes [E11] and removes lanes blocked by static obstacles or disabled vehicles [E12]; if all RNDF lanes are removed and at least one is oncoming, it commands dynamic replan [E13], then updates the Route Planner and resets all behaviors during new-route generation [E14]. At intersections, precedence, merge, and left-turn handling operate across approach/stop/exit situations [E15], while their drivers monitor vehicle-prediction areas [E16]; merge speed control waits until precedence says it is Odin's turn or a traffic jam has been detected [E17]. In parking zones, guided Dijkstra selects control points [E18], and a blocked segment lets the Zone Driver disconnect that graph segment and choose different control points [E19]. Parking enables the stop flag and desired heading on the checkpoint [E20], and backing out constrains direction to reverse only while placing a target point for the next spot or zone exit [E21].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 在 [E1] [E2] 暴露了 normal-road/intersection/parking-lot 顶层分类与 lower-level nested behavior FSM；原文未给进入某 mode 的默认初始子状态，因此未写 default init。
- **G 守卫算术**：G 轴只有复合逻辑 guard 而非算术阈值：[E13] 写出 all RNDF lanes removed AND at least one oncoming lane 触发 dynamic replan；原文没有数值或算术 guard。
- **A 动作**：A 轴由 [E5] [E6] 的 behavior profile 输出、[E7] [E8] 的 Vehicle Interface/灯光喇叭执行器、[E20] [E21] 的 parking stop flag/heading/reverse-only target point 暴露。
- **F 故障恢复**：[E13] [E14] 暴露 blocked-road recovery path：满足 lane-list guard 后触发 dynamic replan、更新 Route Planner 并 reset all behaviors；原文未支持 from-any-state emergency safe-state。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拆段 [E5]-[E8]、implicit-action-prose 动作散叙述 [E13] [E14] [E20] [E21]、multivar-guard 复合守卫 [E13]，并有 hierarchy/nested domain terms [E1] [E2]。
- **ft fcstm-fit**：pyfcstm fit 主要在层次嵌套 [E1] [E2]、复合布尔 guard + reset effect [E13] [E14]、behavior profile 到 Vehicle Interface 的 abstract action/effector 解耦 [E5]-[E8]；原文未支持 per-tick aspect 或全局 forced transition。

</details>

<details><summary>provenance (21条)</summary>

- `[E1]` STM §1 摘录 B | paper.pdf p.16 §2.3.2 Action-Selection Mechanism | paper_content.txt 行 598-600
    - quote: "Such a system allows Driving Behaviors to distinguish between intersection, parking lot, and normal road scenarios."
    - supports: top-level classifier distinguishes normal-road, intersection, and parking-lot situations
- `[E2]` STM §1 摘录 B | paper.pdf p.16 §2.3.2 Action-Selection Mechanism | paper_content.txt 行 603-605
    - quote: "A finite state machine is used to classify the situation, and each individual behavior can be viewed as a lower-level, nested state machine."
    - supports: each behavior is treated as a lower-level nested state machine
- `[E3]` STM §1 摘录 B | paper.pdf p.16 §2.3.2 and p.17 Figure 11 | paper_content.txt 行 597, 619-620
    - quote: "Therefore, a modified Winner-Takes-All (Maes, 1989) mechanism was chosen. Behavior Integrator ensures there is one winner from each driver category."
    - supports: modified Winner-Takes-All arbitration and one winner per driver category
- `[E4]` STM §1 摘录 B | paper.pdf p.16 §2.3.2 | paper_content.txt 行 607-609
    - quote: "Target Point Drivers, Speed Drivers, and Lane Drivers."
    - supports: target-point, speed, and lane driver categories
- `[E5]` paper.pdf p.15 §2.3.2 Driving Behaviors | paper_content.txt 行 559-560
    - quote: "The behavior profile sent to Motion Planning comprises six target points, a desired maximum speed, travel lane, and direction"
    - supports: behavior profile fields: six target points, desired maximum speed, travel lane, and direction
- `[E6]` paper.pdf p.15 §2.3.2 Driving Behaviors | paper_content.txt 行 561-563
    - quote: "Target points can also contain optional fields such as a stop flag and a desired heading."
    - supports: optional stop flag and desired heading
- `[E7]` paper.pdf p.22 §2.3.4 Vehicle Interface | paper_content.txt 行 812-815
    - quote: "output vehicle-specific throttle, brake, steering, and shifting signals."
    - supports: Vehicle Interface output actions for throttle, brake, steering, and shifting
- `[E8]` paper.pdf p.22 §2.3.4 Vehicle Interface | paper_content.txt 行 823-824
    - quote: "actuate other vehicle systems such as lights, turn signals, and the horn."
    - supports: Vehicle Interface can actuate lights, turn signals, and horn
- `[E9]` STM §1 摘录 C | paper.pdf p.17 Passing and Blocked Roads | paper_content.txt 行 628-630
    - quote: "monitoring other vehicles in the near vicinity, deciding if a pass is necessary, and executing this pass in a safe and legal manner."
    - supports: passing monitors nearby vehicles and decides whether a safe legal pass is needed
- `[E10]` STM §1 摘录 C | paper.pdf p.17 Passing and Blocked Roads | paper_content.txt 行 633-636
    - quote: "it is the responsibility of the Route Driver to overrule the Passing Driver if a pass is initiated too close to an exit or intersection."
    - supports: route following can overrule a pass too close to an exit or intersection
- `[E11]` STM §1 摘录 C | paper.pdf p.17 Passing and Blocked Roads | paper_content.txt 行 637
    - quote: "the Blockage Driver maintains a current list of available lanes."
    - supports: Blockage Driver maintains available lanes
- `[E12]` STM §1 摘录 C | paper.pdf p.17 Passing and Blocked Roads | paper_content.txt 行 637-639
    - quote: "If static obstacles in the road or a disabled vehicle cause a lane to be blocked, the Blockage Driver removes this lane from the available list."
    - supports: blocked lanes are removed when static obstacles or disabled vehicles block them
- `[E13]` STM §1 摘录 C | paper.pdf p.17 Passing and Blocked Roads | paper_content.txt 行 639-641
    - quote: "If all RNDF defined lanes are removed from the list and at least one of these lanes is an oncoming lane, then the Blockage Driver commands a dynamic replan."
    - supports: compound guard for dynamic replan: all RNDF lanes removed and at least one oncoming lane
- `[E14]` STM §1 摘录 C | paper.pdf p.17 Passing and Blocked Roads | paper_content.txt 行 641-643
    - quote: "the Route Planner is first updated with the appropriate blockage information and all behaviors are reset while a new route is generated."
    - supports: Route Planner update and reset of all behaviors during new-route generation
- `[E15]` STM §1 摘录 D | paper.pdf p.18 Intersections | paper_content.txt 行 652-654
    - quote: "To handle intersections, Odin uses three drivers (Precedence, Merge, and Left Turn) in the Approaching Stop, Stop, Approaching Exit, and Exit situations."
    - supports: intersection handling across approach/stop/exit situations
- `[E16]` STM §1 摘录 D | paper.pdf p.18 Intersections | paper_content.txt 行 654-656
    - quote: "all three drivers operate by monitoring areas where vehicles (or their predictions) may be"
    - supports: intersection drivers monitor vehicle-prediction areas
- `[E17]` STM §1 摘录 D | paper.pdf p.18 Intersections | paper_content.txt 行 663-668
    - quote: "the Merge Driver cannot adjust the speed until the Precedence Driver has indicated it is Odin’s turn or a traffic jam has been detected."
    - supports: merge speed control waits for precedence turn or detected traffic jam
- `[E18]` STM §1 摘录 E | paper.pdf p.18-19 Parking Lot Navigation | paper_content.txt 行 685-687
    - quote: "Odin performs a guided Dijkstra search to select control points for navigating toward the parking spot and reversing out of the spot."
    - supports: guided Dijkstra selects parking-zone control points
- `[E19]` STM §1 摘录 E | paper.pdf p.18-19 Parking Lot Navigation | paper_content.txt 行 687-689
    - quote: "If the path is blocked, the Zone Driver can disconnect a segment of the graph and choose a different set of control points."
    - supports: blocked parking path segment triggers graph disconnection and alternate control points
- `[E20]` STM §1 摘录 E | paper.pdf p.18-19 Parking Lot Navigation | paper_content.txt 行 689-691
    - quote: "The parking maneuver is signaled to Motion Planning by enabling the stop flag and providing a desired heading on the parking checkpoint."
    - supports: parking enables stop flag and desired heading on the checkpoint
- `[E21]` STM §1 摘录 E | paper.pdf p.18-19 Parking Lot Navigation | paper_content.txt 行 691-693
    - quote: "the direction is constrained to be only in reverse, and a target point is placed in order to position Odin for the next parking spot or zone exit."
    - supports: backing out uses reverse-only direction and a target point for next spot or exit

</details>

- **intentional omissions**：未补写默认初始子状态、全局 emergency stop/safe-state、数值阈值/计时器、具体传感器型号，因为 STM §1 与 PDF 相关段落没有支持。也没有完整枚举所有 driver/state 名，避免把任务退化为状态名复述。

### #4 ✈️ `onboard-mission-management-vtol-uav-sequence-supervisory-control__01` (HSM)

- **case**: Mission-Mode / Command-Mode VTOL UAV Supervisor
- **统计**：279 词 / 26 markers / 26 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The VTOL UAV mission manager [E1] contains a Sequence Control System [E2] modeled as a UML 1.2 State Chart [E3] with two hierarchical levels [E4]; top-level composite states Mission Mode and Command Mode separate mission-plan processing from direct command execution [E5]. Inside Mission Mode, the controller keeps only one behavior active at a time [E6], and finished behaviors return to Parse Command [E7], which grabs commands from the loaded mission plan and issues the event for the appropriate behavior [E8]. Command Mode can be entered from every state inside Mission Mode for payload-directed flight [E9], while runtime plausibility checks decide valid payload/operator command combinations and validate mission sequences with EBNF semantic checks for height parameters, maximum velocity or flight-height restrictions, and movement start/end consistency [E10][E11][E12][E13]. Its hardware-facing output is command generation: every cycle the mission manager commands the flight controller [E14], using vehicle state estimates such as position, velocity, acceleration, and sensor states such as ground distance as inputs [E15]. Interruption handling is cross-cutting: every top-level state can go to Mission Controller Off on manual control [E16], every auto-mode state can execute an operator stop [E17], Slow Down smooths the changeover into Stand By [E18], and Stand By holds hover at the current position or on the ground [E19]. The Supervisory Control System runs before the sequence layer at every instant [E20], reacts to data-link loss [E21], can modify missions [E22], and may issue operator-like commands to the sequence layer [E23]. Its deliberate objectives include Fly Home, which returns the vehicle autonomously to the mission start point [E24], and Search and Track, which finds and tracks a moving ground object using payload-directed detection and the a-priori mission plan [E25][E26].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴由 [E2]-[E5] 暴露：Sequence Control System 是 UML State Chart，具有 two hierarchical levels，并用 Mission Mode / Command Mode 两个 composite state 区分任务计划处理与直接命令执行；原文未给 Mission/Command 内部默认 init，故未写入默认子相位。
- **G 守卫算术**：G 轴由 [E10]-[E13] 暴露：payload/operator 组合、height parameter、maximum velocity / flight-height restriction、movement start/end consistency 作为自然语言合法性检查呈现；原文没有给具体数值阈值。
- **A 动作**：A 轴由 [E7]-[E8] 与 [E14]-[E15] 暴露：Parse Command 抓取任务命令并发出事件，Mission Manager 每周期向 flight controller 输出命令并使用 position / velocity / acceleration / ground-distance 输入。
- **F 故障恢复**：F 轴由 [E16]-[E21] 暴露：manual control 到 Mission Controller Off、auto-mode stop、Slow Down / Stand By 以及 data-link loss 反应构成横切中断/安全处置；原文未提供 emergency stop 或明确故障恢复目标状态。
- **bd baseline-trap**：bd 命中 composite-internal（[E5]-[E8]）、multivar-guard / semantic-check（[E10]-[E13]）、implicit-action-prose（[E14]-[E15]）和 global-cross-cutting（[E16]-[E21]）等 baseline 易错模式。
- **ft fcstm-fit**：ft 中等偏强：层次复合结构（[E2]-[E5]）、多约束合法性检查（[E10]-[E13]）、forced/aspect 风格横切中断和每周期命令输出（[E14]-[E19]）适合 pyfcstm，但原文不支持深 init 链或具体 abstract handler 名。

</details>

<details><summary>provenance (26条)</summary>

- `[E1]` paper.pdf p.1 title | paper_content.txt 行7-8
    - quote: "Onboard Mission Management for a VTOL UAV"
    - supports: VTOL UAV mission manager
- `[E2]` paper.pdf p.3 §4 | paper_content.txt 行214-218
    - quote: "yields two main system components: The Sequence Control System and the Supervisory Control System."
    - supports: mission manager contains a Sequence Control System
- `[E3]` STM §1 摘录 A | paper.pdf p.6 §4.3 | paper_content.txt 行370-371
    - quote: "Thus, the Sequence Control System is modelled as UML 1.2 State Charts."
    - supports: modeled as a UML 1.2 State Chart
- `[E4]` STM §1 摘录 A | paper.pdf p.6 §4.3 | paper_content.txt 行381-382
    - quote: "It has two hierarchical levels where the top level models the procedural flow for a safe operation."
    - supports: two hierarchical levels
- `[E5]` STM §1 摘录 A | paper.pdf p.6 §4.3 | paper_content.txt 行381-385
    - quote: "The two composite states, ”Mission Mode” and ”Command Mode”, model mission plan processing and direct command execution respectively."
    - supports: Mission Mode and Command Mode separate mission-plan processing from direct command execution
- `[E6]` STM §1 摘录 A | paper.pdf p.7 §4.3 | paper_content.txt 行466-468
    - quote: "There are no transitions among behaviors assuring that only one can be active at a time."
    - supports: only one behavior active at a time
- `[E7]` STM §1 摘录 A | paper.pdf p.7 §4.3 | paper_content.txt 行468-470
    - quote: "For each behavior there exists a termination condition, which transits into the command parser ”Parse Command”."
    - supports: finished behaviors return to Parse Command
- `[E8]` STM §1 摘录 A | paper.pdf p.7 §4.3 | paper_content.txt 行470-471
    - quote: "this state grabs behavior commands from an existing mission plan (Figure 4). It issues an event for traversing into the appropriate state."
    - supports: Parse Command grabs commands and issues the event
- `[E9]` STM §1 摘录 A | paper.pdf p.7 §4.3 | paper_content.txt 行472-474
    - quote: "the composite state ”Command Mode” can be entered from every state inside “Mission Mode”."
    - supports: Command Mode can be entered from every state inside Mission Mode
- `[E10]` paper.pdf p.10 §4.6 | paper_content.txt 行622-624
    - quote: "It checks valid combinations for payload directed flight and manual interruption of missions by the operator."
    - supports: valid payload/operator command combinations
- `[E11]` paper.pdf p.10 §4.6 | paper_content.txt 行631-633
    - quote: "using attribute features (e.g. semantic checks of a height parameter), the attributed EBNF shown in Figure 8 has been implemented"
    - supports: EBNF semantic checks for height parameters
- `[E12]` paper.pdf p.11 §4.6 | paper_content.txt 行709-710
    - quote: "For example, it checks against an allowed maximum velocity of a movement behavior or maximum flight height restrictions."
    - supports: maximum velocity or flight-height restrictions
- `[E13]` paper.pdf p.11 §4.6 | paper_content.txt 行710-712
    - quote: "A start position of a behavior must always match the expected end position of a previous behavior."
    - supports: movement start/end consistency
- `[E14]` paper.pdf p.13 §5 | paper_content.txt 行728-730
    - quote: "The Mission Manager is integrated onboard the flight control computer as a component commanding directly and every cycle to the flight controller."
    - supports: every cycle the mission manager commands the flight controller
- `[E15]` paper.pdf p.13 §5 | paper_content.txt 行729-731
    - quote: "The vehicle state estimates (e.g. position, velocities, acceleration) and further sensor states (e.g. ground distance sensor) are the main input"
    - supports: position, velocity, acceleration, and ground-distance sensor inputs
- `[E16]` STM §1 摘录 A | paper.pdf p.6 §4.3 | paper_content.txt 行384-386
    - quote: "Every state of the top level has a transition to the ”Mission Controller Off” to handle a manual control event"
    - supports: every top-level state can go to Mission Controller Off on manual control
- `[E17]` STM §1 摘录 A | paper.pdf p.7 §4.3 | paper_content.txt 行461-462
    - quote: "In case the operator commands the UAV to stop, a transition from every auto mode state assures that the command is executed."
    - supports: every auto-mode state can execute an operator stop
- `[E18]` STM §1 摘录 A | paper.pdf p.7 §4.3 | paper_content.txt 行459-460
    - quote: "The state ”Slow Down” is necessary to assure a smooth changeover into ”Stand By” regardless of the flight maneuver being executed."
    - supports: Slow Down smooths the changeover into Stand By
- `[E19]` STM §1 摘录 A | paper.pdf p.7 §4.3 | paper_content.txt 行457-459
    - quote: "another idle state ”Stand By” lets the UAV hover at its current position when the state was entered; including a position on the ground."
    - supports: Stand By holds hover at the current position or on the ground
- `[E20]` STM §1 摘录 B | paper.pdf p.7 §4.4 | paper_content.txt 行477-480
    - quote: "It is executed before the Sequence Control System at every instant of time."
    - supports: Supervisor runs before the sequence layer at every instant
- `[E21]` STM §1 摘录 B | paper.pdf p.7 §4.4 | paper_content.txt 行477-480
    - quote: "as well as reacting to a loss of the data link."
    - supports: reacts to data-link loss
- `[E22]` STM §1 摘录 B | paper.pdf p.7 §4.4 | paper_content.txt 行480-482
    - quote: "This allows the Supervisory Control System to modify a mission when conditions are recognized to imply a necessity of modification."
    - supports: can modify missions
- `[E23]` STM §1 摘录 B | paper.pdf p.7 §4.4 | paper_content.txt 行483-485
    - quote: "It can command the Sequence Control System via the same type of commands that a remote operator can send to the Sequence Control System"
    - supports: may issue operator-like commands to the sequence layer
- `[E24]` STM §1 摘录 C | paper.pdf p.8 §4.4 | paper_content.txt 行500-502
    - quote: "The Fly Home behavior provides the vehicle with the capability of returning autonomously to the starting point of a given mission."
    - supports: Fly Home returns autonomously to the mission start point
- `[E25]` STM §1 摘录 C | paper.pdf p.8 §4.4 | paper_content.txt 行503-504
    - quote: "The Search and Track behavior can be used to find and track a moving object on the ground."
    - supports: Search and Track finds and tracks a moving ground object
- `[E26]` STM §1 摘录 C | paper.pdf p.8 §4.4 | paper_content.txt 行504-506
    - quote: "Once spotted (e.g. using payload directed object detection) it is desirable to track it. Similar to the Fly Home behavior, it seizes information in the a-priori mission plan"
    - supports: payload-directed detection and use of the a-priori mission plan

</details>

- **intentional omissions**：有意省略具体数值阈值、阀门/电机/传感器型号、GPS/GCS 恢复路径和 EmergencyStop，因为原文没有给出这些细节。也没有枚举 Fig. 3 / Fig. 4 的全部状态和事件名，以免把生成任务退化成抄图。

### #5 ✈️ `robust-accurate-drone-landing-moving-targets__01` (HSM)

- **case**: Three-stage visual-sliding-landing mission supervisor
- **统计**：250 词 / 12 markers / 12 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The VSL mission supervisor is organized as a three-stage drone state machine with a separate Fail-safe branch [E1]. The ordered Stage 1 flow begins from the unarmed ground condition and then arms the drone [E2], climbs to a predefined altitude such as 1 m, and runs a waypoint mission [E3]. In Stage 2, the drone searches for a known target such as a QR code [E4], keeps the helipad centered in the gimbal-camera field of view using yaw, roll, and throttle [E5], and reaches an approach funnel at a certain distance and angle [E6]. After the guiding target is detected, the controller maintains a leash and centering around that smaller sloped target [E7]. During terminal landing, the gimbal changes from about -45 degrees toward 0 degrees while the drone hovers relative to the target [E8], then the controller holds a 1.5 m leash, closes to 1 m, and changes the gimbal to 20 degrees before vertical descent [E9]. The safe-landing envelope also checks numeric operational limits, including max helipad slope of 20 degrees, drone-to-ArUco velocity rate below 1 m/s, marker-tracking confidence, and a 95% credibility factor [E10]. On touchdown, the drone shuts down the motors, reports landing, and returns to the armed ready-to-fly stage [E11]. If abnormality or risk is detected, the Fail-safe policy handles loss of sight or communication loss by staying in place for less than 10 frames and going back to a safe-stage after more than 10 frames, while hardware malfunction sends control to manual mode [E12].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 通过三段 Stage 1/2/3 与独立 Fail-safe 分支暴露阶段化层次结构，并用 Stage 1 从 unarmed ground condition 开始的顺序给出弱 init 线索；原文未支持更深嵌套默认子状态语义，[E1][E2]。
- **G 守卫算术**：G 钩子集中在 gimbal -45→0→20 degrees、1.5 m/1 m 距离链，以及 max helipad slope=20 degrees、velocity rate<1 m/s、credibility factor=95% 的自然语言数值条件，[E8][E9][E10]。
- **A 动作**：A 钩子包括 yaw/roll/throttle 执行 centering、gimbal 角度调整，以及 Touchdown 时 shut down motors、report landing、return to arm 的非平凡动作，[E5][E8][E9][E11]。
- **F 故障恢复**：F 钩子是独立 Fail-safe policy：loss of sight/communication loss 按 10 frames 阈值 stay/safe-stage，hardware malfunction 转 manual control；原文未明确支持 from-any-state forced 语义，[E1][E12]。
- **bd baseline-trap**：bd 中等偏强：expanded_nl 命中 composite-internal 阶段行为、implicit-action-prose 的执行器散叙述、多变量数值守卫，以及弱 global-cross-cutting Fail-safe 分支，[E1][E5][E8][E10][E12]。
- **ft fcstm-fit**：ft 中等：多变量数值约束适合 Expr-IR/SMT，yaw/roll/throttle、gimbal、motors 等动作适合 effector-agnostic abstract action；深复合 init 与 forced/aspect 只得到弱覆盖，[E1][E5][E8][E10][E11][E12]。

</details>

<details><summary>provenance (12条)</summary>

- `[E1]` paper.pdf p.10 Figure 12 | STM §1 摘录 B
    - quote: "Stage 1 ... Stage 2 ... Stage 3 ... Fail-safe"
    - supports: three-stage drone state machine with a separate Fail-safe branch
- `[E2]` paper.pdf p.10 §4.3 | paper_content.txt 行 372-373 | STM §1 摘录 B
    - quote: "Disarmed: The drone is on the ground not armed. Arm: The drone is on the ground armed"
    - supports: Stage 1 begins from the unarmed ground condition and then arms the drone
- `[E3]` paper.pdf p.10 §4.3 | paper_content.txt 行 374-376 | STM §1 摘录 B
    - quote: "Take Off: ... reaches a predefined altitude (e.g., 1 m). Mission: ... composed of several waypoints."
    - supports: climbs to 1 m and runs a waypoint mission
- `[E4]` paper.pdf p.10 §4.3 | paper_content.txt 行 377 | STM §1 摘录 B
    - quote: "Search Target: The drone is looking for a known target (e.g., QR code)"
    - supports: searches for a known target such as a QR code
- `[E5]` paper.pdf p.9-10 §4.2-4.3 | paper_content.txt 行 356-357, 381-383 | STM §1 摘录 A/B
    - quote: "maintaining it in the center of the camera’s FoV... achieved by using yaw roll and throttle"
    - supports: keeps the helipad centered in the gimbal-camera field of view using yaw, roll, and throttle
- `[E6]` paper.pdf p.10 §4.3 | paper_content.txt 行 384-386 | STM §1 摘录 B
    - quote: "the drone reaches a certain distance and angle to the helipad (i.e., approach funnel)"
    - supports: reaches an approach funnel at a certain distance and angle
- `[E7]` paper.pdf p.10 §4.2-4.3 | paper_content.txt 行 362-363, 387-389 | STM §1 摘录 A/B
    - quote: "guiding target (which is smaller than the helipad and is oriented in a slope)... maintains “leash” and executes a centering process"
    - supports: after guiding target detection, maintains leash and centering around the smaller sloped target
- `[E8]` paper.pdf p.12 Figure 15/18 | paper_content.txt 行 443-445 | STM §1 摘录 C
    - quote: "closing distance while changing gimbal angle from -45° to 0°, and hovering in relation to the target"
    - supports: gimbal changes from -45 degrees toward 0 degrees while hovering relative to the target
- `[E9]` paper.pdf p.10 §4.2 + p.11 Hover and Landing | paper_content.txt 行 362-365, 411-414 | STM §1 摘录 A/C
    - quote: "keep a "leash" of 1.5m... close the distance to 1m and change the gimbal angle to 20°. ... descends on the helipad vertically"
    - supports: holds 1.5 m leash, closes to 1 m, changes gimbal to 20 degrees, then descends vertically
- `[E10]` paper.pdf p.12 §4.5 + p.13 Figure 16 | paper_content.txt 行 466-479
    - quote: "marker tracking confidence... Max Helipad Slope 20°... Velocity Rate... <1 m/s... credibility factor 95%"
    - supports: safe-landing numeric checks: slope, relative velocity, marker confidence, credibility factor
- `[E11]` paper.pdf p.11 §4.3 | paper_content.txt 行 398-399 | STM §1 摘录 B
    - quote: "Touchdown: On touching the helipad, the drone shuts down the motors, reports 'landing', and moves to 'arm'"
    - supports: touchdown actions: shut down motors, report landing, return to armed stage
- `[E12]` paper.pdf p.11 §4.3 + p.13 Figure 17 | paper_content.txt 行 400-402 | STM §1 摘录 B
    - quote: "Fail-safe: The drone detects some kind of abnormality or risk... less than 10 frames Stay on Place... Hardware malfunction Take manual control"
    - supports: Fail-safe recovery for abnormality/risk, loss of sight or communication loss, and hardware malfunction

</details>

- **intentional omissions**：没有写具体 safe-stage 名称、任意状态强制跳转、传感器型号或阀门/电机编号，因为原文没有给出这些状态机级细节。也没有枚举全部 state name，避免把输入退化为逐状态抄表。

### #6 🏭 `safety4-dynamic-fsm-multilayer-operation-modes__01` (HSM)

- **case**: Multilayer HRI operation-mode safety FSM
- **统计**：273 词 / 17 markers / 17 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The safety supervisor is a multilayer FSM: the level planner classifies the HRI interaction [E1], the selected operation-mode cluster combines the modes needed for the task [E2], and each collaborative operation mode becomes one machine state [E3]. In the level-1 SRMS cluster, S3 is treated as the start state; in the richer SRMS+SSM cluster, S10 AutoMode can be the start mode before the robot enters collaborative modes such as SSM or SRMS [E4] [E5]. Transitions are guarded by bundles of safety functions: SRMS moves to Stop1 when danger-field entry is active together with SS1, SBC and STO, and Stop1 returns to SRMS only after the danger field is clear and MAR confirms manual restart [E6] [E7]. From AutoMode, SSM starts when a collaborative-field entry such as CFE1 through CFEX is active and SLS, SSM, SSR and SDI are also active [E8]; if danger-field entry occurs [E9] or a safe-motion function is not active, for example when actuator speed exceeds the maximum speed limit, the robot goes to Stop1 [E10]. The Stop1 transfer couples guards with physical safety effects: SS1 maintains actuator position, STO disables actuator torque, and SBC drives an external brake output [E11]. In the case study, a Kuka KR-180 robot and an EMAG VMC 300 MT CNC cell handle a car-engine part [E12]; machining takes 10 min [E13], then the machine opens its safety door and the robot grabs the item [E14]. The robot uses SRMS while picking, transporting, and waiting for machining [E15], switches to HandGuiding when the quality process starts [E16], and later uses SSM for transport to maintenance or SRMS to return a good item to storage [E17].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴由 level planner → operation-mode cluster → collaborative mode as machine state 的多层结构，以及 S3/S10 AutoMode 的 start-state 入口暴露，见 [E1]-[E5]；原文没有更深的 UML-style nested init pseudo。
- **G 守卫算术**：G 钩子在 [E6]-[E10]，用 DFE/MAR/CFE1-CFEX/SLS/SSM/SSR/SDI 等具名安全函数表达复合 AND/OR guard，并只保留 actuator speed exceeds maximum speed limit 这一原文支持的阈值关系；原文没有具体数值阈值。
- **A 动作**：A 钩子在 [E11]-[E14]，Stop1 transfer 绑定 SS1 维持 actuator position、STO torque off、SBC external brake output，并在案例流程中包含 CNC safety door 与 robot grab 动作。
- **F 故障恢复**：F 钩子在 [E6]-[E7] 与 [E9]-[E10]，SRMS/SSM/AutoMode 相关 cluster 可因 danger-field 或 safe-motion violation 进入 Stop1，并在 DFE clear + MAR 后恢复；原文不支持无条件 any-state global escape。
- **bd baseline-trap**：bd 主要命中 cross-section 信息拆段（方法层、状态图、案例流程分别来自 [E1]-[E3]、[E6]-[E10]、[E12]-[E17]）、multivar-guard（[E6]-[E10]）和 implicit-action-prose（[E11]-[E14]）。
- **ft fcstm-fit**：ft 主要暴露 pyfcstm 的多层 cluster/start-mode 建模优势（[E1]-[E5]）、复合 safety-function guard（[E6]-[E10]）和 effector-agnostic abstract action 映射（[E11]-[E14]）；forced+aspect 横切优势覆盖有限。

</details>

<details><summary>provenance (17条)</summary>

- `[E1]` paper.pdf p.4 §3 | paper_content.txt 行 257-263
    - quote: "The first layer “Level-Planner”, facilitates the classification of the proposed application according to the interaction level"
    - supports: level planner classifies the HRI interaction
- `[E2]` paper.pdf p.4 §3 | paper_content.txt 行 261-264
    - quote: "The second layer presents a combination of possible clustered operation modes to fulfill the described task in the level-planner."
    - supports: selected operation-mode cluster combines the modes needed for the task
- `[E3]` STM §1 摘录 A | paper.pdf p.6 §3.2 | paper_content.txt 行 349-352
    - quote: "every collaborative operation mode will represent one machine state"
    - supports: each collaborative operation mode becomes one machine state
- `[E4]` paper.pdf p.8 §3.4 | paper_content.txt 行 416-421
    - quote: "By supposing that S3 is the start state"
    - supports: level-1 SRMS cluster treats S3 as the start state
- `[E5]` STM §1 摘录 C | paper.pdf p.8 §3.4 | paper_content.txt 行 446-448
    - quote: "S10 (AutoMode) represents the automation mode which can be the start mode."
    - supports: S10 AutoMode can be the start mode
- `[E6]` STM §1 摘录 B | paper.pdf p.8 §3.4 | paper_content.txt 行 427-437
    - quote: "T3_1 -> (DFE ∧ SS1 ∧ SBC ∧ STO)"
    - supports: SRMS moves to Stop1 when DFE, SS1, SBC and STO are active
- `[E7]` STM §1 摘录 B | paper.pdf p.8 §3.4 | paper_content.txt 行 438-445
    - quote: "DFE is deactivated, and the human has left the danger area. Besides that, a user confirmation through MAR"
    - supports: Stop1 returns to SRMS after danger field is clear and MAR confirms restart
- `[E8]` STM §1 摘录 C | paper.pdf p.8 §3.4 | paper_content.txt 行 452-458
    - quote: "T10_4 -> ((CFE1 ∨ CFE2 ... CFEX) ∧ SLS ∧ SSM ∧ SSR ∧ SDI)"
    - supports: AutoMode enters SSM under CFE and safe-motion function bundle
- `[E9]` paper.pdf p.8 §3.4 | paper_content.txt 行 459-463
    - quote: "The transitions T4_1 and T3_1 from S4 and S3 states to the S1-state happen when the DFE is activated"
    - supports: danger-field entry sends SSM/SRMS states to Stop1
- `[E10]` paper.pdf p.8 §3.4 | paper_content.txt 行 464-467
    - quote: "if one of the safe motion functions is not active (e.g. the actuator speed exceeds the maximum speed limit), the robot goes to S1-state"
    - supports: safe-motion violation or actuator speed over limit sends robot to Stop1
- `[E11]` paper.pdf p.8 §3.4 | paper_content.txt 行 430-432
    - quote: "SS1 for maintaining the position of the actuator, STO for disabling the torque in the actuator, and SBC for supplying a safe output signal to drive an external brake system"
    - supports: Stop1 transfer includes actuator position hold, torque off, and external brake output
- `[E12]` paper.pdf p.9 §4 | paper_content.txt 行 513-516
    - quote: "using a CNC machine EMAG VMC 300 MT integrated with a heavy-duty robot Kuka KR-180 Prime 2,900"
    - supports: case-study hardware: Kuka KR-180 robot and EMAG VMC 300 MT CNC cell
- `[E13]` paper.pdf p.9 §4 | paper_content.txt 行 528-529
    - quote: "it takes 10 min for each item"
    - supports: machining takes 10 min
- `[E14]` paper.pdf p.9 §4 | paper_content.txt 行 530-531
    - quote: "the machine opens the safety door while robots move toward the machine. The robot grabs the item from the machine."
    - supports: machine opens safety door and robot grabs the item
- `[E15]` STM §1 摘录 D | paper.pdf p.9 §4 | paper_content.txt 行 549-551
    - quote: "the robot can work under SRMS operation mode while picking the item from storage, transporting it to the CNC, and waiting for the machining process"
    - supports: SRMS covers picking, transport to CNC, and waiting for machining
- `[E16]` STM §1 摘录 D | paper.pdf p.9 §4 | paper_content.txt 行 551-552
    - quote: "When the quality process starts, the robot can switch to the HandGuiding operation mode."
    - supports: robot switches to HandGuiding when quality process starts
- `[E17]` STM §1 摘录 D | paper.pdf p.9 §4 | paper_content.txt 行 552-554
    - quote: "the robot can work under SSM while transporting the item to the maintenance station or under SRMS"
    - supports: final process uses SSM for maintenance transport or SRMS for returning good item to storage

</details>

- **intentional omissions**：未加入阀门编号、传感器型号、额外 mode 名、具体速度阈值、watchdog/per-tick aspect 或任意状态 emergency jump，因为原文没有支撑。也刻意没有枚举全部 state name，以避免把任务退化成直接抄状态表。

### #7 🅿️ `scale-model-parking-garage-integrating-automation-in-parking-facilities__01` (HSM)

- **case**: Circular Parking Garage Auto/Manual Supervisor
- **统计**：256 词 / 20 markers / 20 provenance entries
- **轴覆盖**：⚪ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The controller uses Beckhoff TwinCAT 3 logic for a scale-model circular parking garage [E1]: MAIN coordinates the program blocks, the automatic branch handles parking/retrieval [E2], and the manual branch supports troubleshooting, testing, or calibration [E3]. Its cyclic task runs the main logic at a fixed interval [E4] and handles checking safety signals and sending motor commands [E5]. Through the HMI, the operator selects automatic or manual operation [E6], and PLC interlocking permits only one active mode [E7]. In automatic operation, the operator enters a desired slot number [E8] and uses Entry or Exit command buttons [E9]; the PLC then manages slot positioning, platform rotation, and vehicle movement automatically [E10]. The PLC evaluates the selected slot number: configured slot ranges select the vertical target position, and the same slot choice selects reverse, skip, or forward platform rotation [E11] [E12]. In manual operation, push buttons command vertical motion, horizontal or rotational motion, and door control [E13], with a select option enabling only the intended motion [E14]. The motion layer uses stepper and servo function blocks to control motor direction, speed, motion commands, and encoder feedback [E15]. When emergency stop is pressed, all motor drives are deactivated and operation halts [E16]; motion commands are overridden, motor-enable signals are deactivated, and the system enters a safe state [E17]. The PLC continuously checks drive faults such as overload, communication errors, and overcurrent [E18]; on a fault it disables further commands, stops the affected motor [E19], and permits system restart only after the fault is cleared and safety conditions are restored [E20].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用 MAIN 协调程序块、automatic/manual 两个互斥运行分支暴露层次组织与模式互斥 [E2] [E3] [E7]；但原文未给出进入某 mode 的默认 init 子状态，因此未提供 default-init 钩子。
- **G 守卫算术**：expanded_nl 的 G 钩子是 selected slot number：PLC 按 slot ranges 选择垂直目标位置，并按 slot 选择 reverse/skip/forward rotation [E11] [E12]；原文没有具体数值阈值，未补造数字。
- **A 动作**：expanded_nl 暴露了周期任务检查安全信号并发送电机命令、自动序列管理定位/旋转/车辆移动、手动按钮驱动多类机械动作以及 stepper/servo FB 控制电机反馈 [E4] [E5] [E10] [E13] [E15]。
- **F 故障恢复**：expanded_nl 的 F 钩子是 emergency stop 与 drive fault：急停覆盖命令并进入 safe state，故障停止受影响电机，系统只有在 fault cleared 与 safety restored 后才允许 restart [E16] [E17] [E19] [E20]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain 的停车槽位/楼层/旋转术语、implicit-action-prose 的散叙述电机与 HMI 动作、composite-internal 的 auto/manual 内部行为，以及 global-cross-cutting 的急停/故障安全逻辑 [E8] [E10] [E11] [E13] [E16] [E19]。
- **ft fcstm-fit**：expanded_nl 对 pyfcstm 的适配主要在 slot-range 决策可转成 Expr/SMT 守卫、cyclic task 可转成 per-tick aspect、急停/故障可转成 forced/safe-state 规则、stepper/servo/HMI 可转成 abstract action；但原文不支持深复合 init 链 [E4] [E11] [E12] [E15] [E16] [E20]。

</details>

<details><summary>provenance (20条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.22 §5.1 | paper_content.txt 行 527-529
    - quote: "In the scale model circular parking garage system, the Beckhoff TwinCAT 3 software is used to develop logic sequences."
    - supports: Beckhoff TwinCAT 3 logic for a scale-model circular parking garage
- `[E2]` STM §1 摘录 A | paper.pdf p.22-23 §5.1 | paper_content.txt 行 530-540
    - quote: "MAIN (PRG): Runs the overall system logic and coordinates communication between all program blocks. AUTO_MODE (PRG): Controls the automatic parking and retrieval sequence."
    - supports: MAIN coordinates program blocks; automatic branch handles parking/retrieval
- `[E3]` STM §1 摘录 A | paper.pdf p.23 §5.1 | paper_content.txt 行 541-542
    - quote: "MAN_MODE (PRG): Allows manual operation for troubleshooting, testing, or calibration."
    - supports: manual branch supports troubleshooting, testing, or calibration
- `[E4]` STM §1 摘录 A | paper.pdf p.23 §5.1 | paper_content.txt 行 551-552
    - quote: "The PLC program uses a cyclic task that runs the main logic at a fixed interval"
    - supports: cyclic task runs main logic at a fixed interval
- `[E5]` STM §1 摘录 A | paper.pdf p.23 §5.1 | paper_content.txt 行 551-553
    - quote: "This task handles important actions such as checking safety signals and sending motor commands."
    - supports: checking safety signals and sending motor commands
- `[E6]` STM §1 摘录 B | paper.pdf p.29-30 §6.2.3 | paper_content.txt 行 695-697
    - quote: "A dedicated ‘Mode Selection’ button allows the operator to switch between 'Automatic' and 'Manual' modes."
    - supports: operator selects automatic or manual operation through the HMI
- `[E7]` STM §1 摘录 B | paper.pdf p.29-30 §6.2.3 | paper_content.txt 行 697-699
    - quote: "Interlocking logic plays a vital role within the PLC to confirm that only one mode can be active at a time."
    - supports: PLC interlocking permits only one active mode
- `[E8]` STM §1 摘录 B | paper.pdf p.29 §6.2.2 | paper_content.txt 行 685-689
    - quote: "A numeric input field for entering the desired parking slot number"
    - supports: operator enters a desired slot number
- `[E9]` STM §1 摘录 B | paper.pdf p.29 §6.2.2 | paper_content.txt 行 688-690
    - quote: "Entry and Exit command buttons to initiate parking or retrieval sequences"
    - supports: Entry or Exit command buttons initiate automatic operation
- `[E10]` STM §1 摘录 B | paper.pdf p.29 §6.2.2 | paper_content.txt 行 691-692
    - quote: "the PLC executes a predefined control sequence that manages parking slot positioning, rotation and the vehicle movement automatically."
    - supports: PLC manages slot positioning, platform rotation, and vehicle movement automatically
- `[E11]` STM §1 摘录 C | paper.pdf p.34 §8.4 | paper_content.txt 行 816-820
    - quote: "Slots are grouped into ranges. Each range corresponds to predefined vertical target position"
    - supports: configured slot ranges select the vertical target position
- `[E12]` STM §1 摘录 C | paper.pdf p.34 §8.4 | paper_content.txt 行 822-824
    - quote: "Specific slots are activated by reverse rotation or skip rotation command and remaining slots are activated by forward rotation."
    - supports: selected slot determines reverse, skip, or forward platform rotation
- `[E13]` STM §1 摘录 B | paper.pdf p.29 §6.2.1 | paper_content.txt 行 674-679
    - quote: "The Manual Mode section allows individual mechanical movements ... vertical movement, horizontal or rotational movement, door control"
    - supports: manual push buttons command vertical, horizontal/rotational, and door movements
- `[E14]` STM §1 摘录 B | paper.pdf p.29 §6.2.1 | paper_content.txt 行 680-682
    - quote: "The ‘select’ option refers to manual commands that are enabled and ensures that only the intended motion is activated."
    - supports: select option enables only the intended motion
- `[E15]` STM §1 摘录 A | paper.pdf p.23 §5.1 | paper_content.txt 行 543-547
    - quote: "Function blocks that control the stepper motors, including direction and speed monitoring. servo (FB): Controls the servo motor and motion commands and handles encoder feedback."
    - supports: stepper and servo function blocks control direction, speed, commands, and encoder feedback
- `[E16]` STM §1 摘录 C | paper.pdf p.31 §7.1 | paper_content.txt 行 730-733
    - quote: "When the emergency stop button is pressed, it immediately deactivates all drives of the motors and halts system operation."
    - supports: emergency stop deactivates motor drives and halts operation
- `[E17]` STM §1 摘录 C | paper.pdf p.31 §7.1 | paper_content.txt 行 734-736
    - quote: "motion commands are overridden due to the emergency stop signal indication. The system into a safe state and all motors enable signals are deactivated."
    - supports: motion commands are overridden, motor-enable signals are deactivated, and the system enters safe state
- `[E18]` STM §1 摘录 C | paper.pdf p.31 §7.2 | paper_content.txt 行 740-744
    - quote: "Fault signals from motor drives such as overload, communication errors, or overcurrent are communicated to PLC input channels. The PLC continuously checks the fault signals during system operation."
    - supports: PLC continuously checks drive fault signals such as overload, communication errors, and overcurrent
- `[E19]` STM §1 摘录 C | paper.pdf p.31 §7.2 | paper_content.txt 行 744-746
    - quote: "If any fault detects during operation the system disables further motion commands and immediately stops the affected motor."
    - supports: on a fault, the PLC disables further commands and stops the affected motor
- `[E20]` STM §1 摘录 C | paper.pdf p.35 §8.5 | paper_content.txt 行 854-855
    - quote: "the whole system restarts only possible after the fault is cleared and safety conditions are restored."
    - supports: system restart is permitted only after fault clearance and safety restoration

</details>

- **intentional omissions**：未写具体 slot range 边界、楼层编号、速度数值或全部 state name，因为原文只给出范围/方向规则与 POU 组织，没有给出可溯源的完整枚举。也未发明进入 AUTO_MODE 或 MAN_MODE 后的默认初始子相位，因为 PDF 与 STM §1 摘录都没有明确 default init。

### #8 ✈️ `sequence-supervisory-control-onboard-uav-mission-management__01` (HSM)

- **case**: Mission-mode / command-mode UAV sequence supervisor
- **统计**：279 词 / 19 markers / 19 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The onboard mission manager combines a Sequence Control System with a Supervisory Control System so events and commands from a remote operator or onboard components can enter the system while only permitted commands pass event handling [E1] [E2] [E3]. The Sequence Control System follows a default transition into ControllerOn and then uses a two-level UML state chart whose top level separates Mission Mode for mission-plan processing from Command Mode for direct command execution [E4] [E5]. When a safety pilot switches between manual and computer-aided flight control, the controller stops producing actuator commands and resets onboard components into a defined stand-by condition [E6]. In autonomous flight, stop and manual-control events are cross-cutting: every top-level state can fall back for manual control, and every auto-mode state has a stop transition [E7] [E8]. Inside Mission Mode, the behavior library allows at most one behavior to be active; each behavior terminates by returning to the command parser, which reads the next behavior command from the mission plan and issues the event for the appropriate behavior [E9] [E10]. Direct commands are admitted only when a static truth table accepts the incoming GCS, vision-computer, or FLARM channel values, including boolean or numeric position, joystick, pattern-position, stereo-avoidance, and FLARM-avoidance data [E11] [E12]. Mission plans are checked as EBNF behavior-command sequences: the root mission must start with take-off and end with land, hover-and-wait uses a nonnegative waiting-time parameter, and forward-flight planning requires at least three behavior commands [E13] [E14] [E15]. The safety envelope remains global, because the operator may overrule autonomous actions anytime, stand-by also serves as an error fall-back state, malformed mission plans are rejected, and minimum ground-distance shortfall is never allowed [E16] [E17] [E18] [E19].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴由 [E4] [E5] 覆盖：expanded_nl 写出 DefaultTransition→ControllerOn，以及两层 UML State Chart 中 Mission Mode / Command Mode 两个复合状态；原文未明示这两个复合状态内部的默认子态。
- **G 守卫算术**：G 轴由 [E11] [E12] [E13] [E14] [E15] 覆盖：direct command 需要 GCS / vision / FLARM 通道的 boolean 或 numeric 数据组合通过 truth table，mission grammar 还包含 start/end、waiting time 非负、forward flight 至少三个 behavior commands 等自然语言算术/组合条件。
- **A 动作**：A 轴由 [E6] [E10] 覆盖：manual/computer-aided 切换时停止 actuator commands 并 reset onboard components，Mission Mode 的 command parser 读取下一个 behavior command 并发出进入对应 behavior 的 event。
- **F 故障恢复**：F 轴由 [E7] [E8] [E16] [E17] [E18] [E19] 覆盖：manual overrule、top-level/manual fallback、auto-mode stop transition、Stand By error fallback、malformed mission rejection 与 minimum-ground-distance 全局安全约束共同构成横切恢复/安全路径。
- **bd baseline-trap**：bd 覆盖较强：expanded_nl 把 state chart 层次、truth-table/grammar 守卫和 safety conclusion 跨章节合并，并含 GCS/FLARM 等隐式领域术语、散文式动作与多源 numeric/boolean guard，主要落在 cross-section、implicit-domain、implicit-action-prose、multivar-guard [E5] [E6] [E11] [E12] [E13] [E14] [E15]。
- **ft fcstm-fit**：ft 覆盖中等偏强：expanded_nl 暴露了 DefaultTransition→ControllerOn 的 init 链、复合 mode 边界、truth-table/grammar 型多变量 SMT 守卫，以及 manual/stop/fallback 的 forced/global 安全语义；但缺少具体每 tick aspect 与硬件编号级 abstract action [E4] [E5] [E7] [E8] [E11] [E12] [E13] [E14] [E15] [E16] [E17]。

</details>

<details><summary>provenance (19条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.1 Overview | paper_content.txt 行 7-13
    - quote: "Two main components, a Sequence Control System and a Supervisory Control System, form the Mission Management System"
    - supports: Sequence Control System 与 Supervisory Control System 共同构成 onboard mission manager
- `[E2]` STM §1 摘录 A | paper.pdf p.1 Overview | paper_content.txt 行 8-13
    - quote: "Events and commands sent by a remote operator or an onboard component can be integrated into the system"
    - supports: remote operator / onboard component 的 events and commands can enter the system
- `[E3]` STM §1 摘录 A | paper.pdf p.1 Overview | paper_content.txt 行 8-13
    - quote: "only permitted commands are accepted by the event handling"
    - supports: only permitted commands pass event handling
- `[E4]` paper.pdf p.4 Figure 3
    - quote: "DefaultTransition; ControllerOn"
    - supports: state chart follows a default transition into ControllerOn
- `[E5]` STM §1 摘录 B | paper.pdf p.5 §4.2 | paper_content.txt 行 227-229
    - quote: "It has two hierarchical levels where the top level models the procedural flow for a safe operation. The two composite states, ”Mission Mode” and ”Command Mode”"
    - supports: two-level UML state chart and Mission Mode / Command Mode composite-state separation
- `[E6]` paper.pdf p.4 §4.1 | paper_content.txt 行 176-180
    - quote: "stop producing actuator commands and reset its onboard components into a defined stand-by state"
    - supports: manual/computer-aided flight-control switch triggers actuator-command stop and reset to stand-by
- `[E7]` STM §1 摘录 B | paper.pdf p.5 §4.2 | paper_content.txt 行 229-233
    - quote: "Every state of the top level has a transition to the ”Mission Controller Off”"
    - supports: manual-control event is available from every top-level state
- `[E8]` STM §1 摘录 B | paper.pdf p.5 §4.2 | paper_content.txt 行 230-233
    - quote: "a transition from every auto mode state assures that the command is executed"
    - supports: stop command has a transition from every auto-mode state
- `[E9]` paper.pdf p.5 §4.2 | paper_content.txt 行 234-236
    - quote: "not more than one behavior can be active at a time"
    - supports: Mission Mode behavior library allows at most one active behavior
- `[E10]` STM §1 摘录 B | paper.pdf p.5 §4.2 | paper_content.txt 行 236-237
    - quote: "this state grabs behavior commands from an existing mission plan. It issues an event"
    - supports: command parser reads the next mission-plan behavior command and issues the traversal event
- `[E11]` paper.pdf p.5 §4.2 | paper_content.txt 行 243-246
    - quote: "direct input data channels for the GCS, vision computer and FLARM"
    - supports: direct-command admission depends on GCS, vision-computer, and FLARM channels
- `[E12]` paper.pdf p.5 §4.2 | paper_content.txt 行 245-246
    - quote: "data values, either boolean or numeric, for position, joystick, pattern position"
    - supports: truth-table guard uses boolean or numeric data values such as position, joystick, and pattern position
- `[E13]` STM §1 摘录 B | paper.pdf p.5 §4.2 | paper_content.txt 行 248-249
    - quote: "start with a take-off behavior and end with a land"
    - supports: EBNF root mission start/end constraint
- `[E14]` paper.pdf p.5 §4.2 | paper_content.txt 行 249-250
    - quote: "waiting time must not be a negative number"
    - supports: hover-and-wait nonnegative waiting-time parameter check
- `[E15]` paper.pdf p.5 §4.2 | paper_content.txt 行 249-250
    - quote: "forward flight needs at least three of its behavior commands"
    - supports: forward-flight planning requires at least three behavior commands
- `[E16]` STM §1 摘录 C | paper.pdf p.7 Conclusion | paper_content.txt 行 288-291
    - quote: "operator can overrule autonomous actions anytime"
    - supports: operator can globally overrule autonomous actions
- `[E17]` STM §1 摘录 C | paper.pdf p.7 Conclusion | paper_content.txt 行 288-291
    - quote: "stand by state which also serves as a fall-back state"
    - supports: stand-by is an error fall-back state
- `[E18]` paper.pdf p.7 Conclusion | paper_content.txt 行 288-291
    - quote: "rejects a malformed mission plan"
    - supports: malformed mission plans are rejected
- `[E19]` paper.pdf p.7 Conclusion | paper_content.txt 行 288-291
    - quote: "allows no shortfall of a minimum ground distance"
    - supports: minimum ground-distance shortfall is never allowed

</details>

- **intentional omissions**：原文没有提供阀门、传感器型号、执行器编号或具体数值阈值，因此没有编造硬件 I/O 名称和精确 threshold。Mission Mode / Command Mode 内部的默认初始子态也未由正文明确说明，所以只保留 Figure 3 可见的顶层 DefaultTransition→ControllerOn。

### #9 ⚙️ `autonomous-robotic-manipulation-exploratory-interactions__01` (HSM)

- **case**: Four-State Exploratory Manipulation Supervisor with Fault-Detection Substates
- **统计**：237 词 / 9 markers / 9 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ⚪ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The controller is a finite-state supervisor for autonomous robotic material manipulation: it manages framework phases, consumes visual-perception data, and activates self-tuning impedance when interaction is expected [E1][E2]. Its top-level sequence begins in Workspace definition, where polygon vertices from Materials localization are stored, then enters Exploration to identify stiffness kst for each material [E3]. In Exploration, the end-effector grasps a stick-like tool, reaches the leftmost material compliantly, dunks into it, sets Im and If true, moves toward the polygon center, stores kst, and repeats the identification for all materials [E4]. An Exploration Fault Detection sub-unit monitors external forces projected along the motion vector; when the sampled linear-regression slope m exceeds mfault, the robot stops the current motion and returns to homing [E5]. Materials distribution associates vision-derived peak points with materials, and Task uses those peaks as scooping starts to scoop and pour material into a pot held by another robot [E6]. In the reported Task execution, the robotic hand grasps a scooping tool, Task is subdivided into four scheduled material substates starting with soil, and stiffness adapts along the current motion direction inside the interaction expectancy area [E7]. During Task, kst is bounded by the exploration stiffness multiplied by one plus a percentage p constrained to the range from 0 to 0.5; if kst exceeds that maximum, Task fault detection halts execution and returns the robot to its homing position or initial configuration in a compliant way [E8][E9].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 在 [E5] 写出 Exploration 内部 Fault Detection sub-unit，在 [E7] 写出 Task subdivided into four scheduled material substates starting with soil；原文支持层次/子状态，但未给完整通用 init 链。
- **G 守卫算术**：G 钩子在 [E5][E8][E9]：外力回归斜率 m 超过 mfault，以及 Task 中 kst 相对 exploration stiffness 和 p∈[0,0.5] 计算的上界，均用自然语言条件表达。
- **A 动作**：A 钩子在 [E2][E4][E6][E7]：控制器激活 impedance，end-effector grasp/dunk/store kst，Materials distribution associates peaks，Task grasp/scoop/pour/adapt stiffness。
- **F 故障恢复**：F 钩子在 [E5][E9]：Exploration 和 Task 内的 Fault Detection 在阈值越界时中止当前 motion/execution 并回到 homing/initial configuration；原文未支持全局任意状态 escape。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain terms（kst、Im/If、mfault）、implicit-action-prose（grasp/dunk/store/scoop/pour）和 multivar-guard/composite-internal（Task bound、Fault Detection sub-unit、Task substates）[E4][E5][E7][E8][E9]。
- **ft fcstm-fit**：pyfcstm 适配点主要是复合状态/子状态与局部 recovery [E5][E7][E9]、Expr-IR 可表达的阈值/乘法上界 [E8]、以及 effector-agnostic grasp/scoop/pour/adapt 动作 [E4][E6][E7]；forced/aspect 全局横切覆盖弱。

</details>

<details><summary>provenance (9条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.7 §2.5 | paper_content.txt 行 419-421
    - quote: "responsible of managing the transitions between the different phases of the framework"
    - supports: finite-state supervisor; manages framework phases
- `[E2]` paper.pdf p.7 §2.5 | paper_content.txt 行 422-427
    - quote: "gets as input the data sent by the Visual perception module / activate the Self-tuning impedance unit"
    - supports: consumes visual-perception data; activates self-tuning impedance when interaction is expected
- `[E3]` STM §1 摘录 A | paper.pdf p.7 §2.5 | paper_content.txt 行 428-435
    - quote: "gets as input the vertices of the polygons / switches to the “Exploration” state / identify the kst parameter for every material"
    - supports: Workspace definition stores polygon vertices; transition into Exploration; identify kst per material
- `[E4]` STM §1 摘录 A | paper.pdf p.7 §2.5 | paper_content.txt 行 435-446
    - quote: "the robot end-effector grasps a stick-like tool / both the boolean value Im and If have been set to True / stores the resulting kst / repeated for all the materials"
    - supports: Exploration actions: grasp, dunk/contact expectation, set Im and If, store kst, repeat
- `[E5]` STM §1 摘录 B | paper.pdf p.7 §2.5 | paper_content.txt 行 457-465
    - quote: "linear regression slope m goes beyond a threshold set to mfault, the fault is triggered / ends its motion and goes back to its homing position"
    - supports: Exploration Fault Detection guard and recovery
- `[E6]` STM §1 摘录 B | paper.pdf p.7 §2.5 | paper_content.txt 行 466-483
    - quote: "the vision unit detects the highest point / the robot needs to scoop some material and pour it in a pot"
    - supports: Materials distribution peak association; Task scooping and pouring
- `[E7]` paper.pdf p.9 §4 | paper_content.txt 行 587-606
    - quote: "robotic hand grasps a scooping tool / Task state, subdivided in four substates / following this sequence: soil (a) / kst is adapted along the direction of the motion"
    - supports: Task hardware action, four substates, first scheduled material, stiffness adaptation
- `[E8]` STM §1 摘录 C | paper.pdf p.8 §2.5 | paper_content.txt 行 495-501
    - quote: "kst_max,m = kst_exploration,m ∗ (1 + p) 0 ≤ p ≤ 0.5 ∀m"
    - supports: Task stiffness bound using exploration stiffness and p in range 0 to 0.5
- `[E9]` STM §1 摘录 C | paper.pdf p.8 §2.5; paper.pdf p.11 Fig.11 | paper_content.txt 行 501-503, 676-693
    - quote: "the robot goes back to its homing position / execution halts and the robot goes back to its initial configuration in a compliant way"
    - supports: Task fault detection halts execution and returns to homing or initial configuration

</details>

- **intentional omissions**：没有补造全局 any-state emergency stop、Valve/PLC 编号、计时器/复位计数器或 ROS topic 名。实验段虽有材料坐标、α、kmin、通信频率等数字，但多数是实验设置而非该 STM 的通用控制规则，因此未写入 expanded_nl。

### #10 🏢 `mechatronic-control-system-finite-state-machine__01` (HSM)

- **case**: Hierarchical Sliding-Door Motion FSM with Blockade Recovery
- **统计**：234 词 / 18 markers / 18 provenance entries
- **轴覆盖**：✅ H 层次 / ⚪ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The controller is an automatic sliding-door FSM in which the control system reads application inputs and produces outputs that affect the door, and the continuous space exchanges data with door sensors and actuators [E1][E2]. A door-management FSM commands the motion-generator through PROMACHINE_IN, and the motion-generator has fourteen inputs and five outputs that supply acceleration, velocity, and position reference data to the control system, plus diagnostic state-toggle and status information for door management [E3][E4][E5][E6]. On power-on, the door enters an initiation cycle, searches the end position at a constant slow speed, saves the maximum motor current as the door-opening interval, and later generates reference motion values within motor capacity for the given door weight [E7][E8][E9]. The main motion generator is hierarchical: high-level modes include init, positive, negative, and stop, and these modes are refined into sub-levels rather than flattened [E10]. Within positive motion, the first sub-level switches across sectors I to VIII, and the second sub-level concludes the motion-calculation equations; one lower state, S20, covers first-sector motion calculation [E11][E12][E13]. Transitions are driven by input or function conditions; the examples combine door_closed with person_detected, or command_open with person_detected, and sub-level states remain conditioned by events and actions from the main level [E14][E15][E16]. During normal operation, if motion is forcefully interrupted by obstacle collision or another movement-prevention condition, the door enters blockade detection, changes movement direction, and stops with an error indicator after three subsequent attempts [E17][E18].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 通过 main motion generator 的 `init / positive / negative / stop` 主模式、`positive` 内 sectors I-VIII 子层、second sub-level 与 S20 计算层暴露层次结构；power-on initiation cycle 只支持顶层初始进入线索，原文未给出 positive 内默认子状态，因此未补写 [E7][E10][E11][E12][E13]。
- **G 守卫算术**：原文没有给可量化阈值或算术 transition guard；expanded_nl 仅暴露 input/function condition、`door_closed` + `person_detected`、`command_open` 或 `person_detected` 等布尔复合 guard，以及主层事件/action 对子层的条件约束，G 轴覆盖弱 [E14][E15][E16]。
- **A 动作**：A 钩子在 motion-generator 输出 reference acceleration/velocity/position、diagnostic/status，power-on 保存 maximum motor current，并在 blockade 中 change direction 或 error stop，均为非平凡动作/输出语义 [E5][E6][E7][E8][E9][E18]。
- **F 故障恢复**：F 钩子是 normal operation 下 forceful interruption 进入 blockade detection，并在恢复失败后 change direction 或三次后 error stop；原文不支持 from any state 的全局 emergency escape，因此未写全局强制路径 [E17][E18]。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拆段、implicit-domain 机电术语、implicit-action-prose 动作散叙述和 composite-internal 子层条件等 baseline 失败模式，但 multivar-guard 与 global-cross-cutting 证据不足 [E3][E6][E10][E16][E17][E18]。
- **ft fcstm-fit**：pyfcstm 适配点主要是深复合层次结构与 effector-agnostic 的 reference/status/diagnostic 输出动作；原文缺少明确 SMT 数值守卫、per-tick aspect 和任意状态 forced reset，因此独占优势覆盖为中等偏窄 [E2][E5][E6][E10][E11][E12][E13]。

</details>

<details><summary>provenance (18条)</summary>

- `[E1]` STM §1 摘录 B | paper.pdf p.2 §2 SYSTEM DESCRIPTION | paper_content.txt 行 123-127
    - quote: "The control system receives certain information (inputs) from the application, and generates actions (outputs) that affect it."
    - supports: control system reads application inputs and produces outputs that affect the door
- `[E2]` paper.pdf pp.2-3 §2 SYSTEM DESCRIPTION | paper_content.txt 行 144-152
    - quote: "The continuous space contains a continuous data stream both from and to the sensors and actuators that are used on the automatic doors."
    - supports: continuous space exchanges data with door sensors and actuators
- `[E3]` STM §1 摘录 C | paper.pdf p.6 §4 MOTION BASED ON FSM | paper_content.txt 行 348
    - quote: "The FSM motion-generator has 14 different inputs."
    - supports: motion-generator has fourteen inputs
- `[E4]` STM §1 摘录 C | paper.pdf p.6 §4 MOTION BASED ON FSM | paper_content.txt 行 349-351
    - quote: "The input PROMACHINE_IN is connected to the door management FSM, which gives commands to the FSM motion-generator."
    - supports: door-management FSM commands the motion-generator through PROMACHINE_IN
- `[E5]` STM §1 摘录 C | paper.pdf p.6 §4 MOTION BASED ON FSM | paper_content.txt 行 356-359
    - quote: "The FSM motion-generator with 5 outputs represents 3 pieces of reference data (acceleration, velocity, and position)."
    - supports: five outputs supply acceleration, velocity, and position reference data
- `[E6]` STM §1 摘录 C | paper.pdf p.6 §4 MOTION BASED ON FSM | paper_content.txt 行 362-365
    - quote: "FSM motion-generator diagnostic – states toggle information. The status output is connected to the door management FSM"
    - supports: diagnostic state-toggle and status information for door management
- `[E7]` paper.pdf p.10 §5 SELF-TUNNING ALGORITHM FOR MOTION GENERATOR | paper_content.txt 行 486-488
    - quote: "The doors have an initiation cycle at the beginning (power on). The doors go into end-position search at a constant slow speed."
    - supports: power-on initiation cycle and end-position search at constant slow speed
- `[E8]` paper.pdf p.10 §5 SELF-TUNNING ALGORITHM FOR MOTION GENERATOR | paper_content.txt 行 488-491
    - quote: "The maximum motor current value is saved in the memory as the door-opening interval."
    - supports: saves maximum motor current as the door-opening interval
- `[E9]` paper.pdf p.10 §5 SELF-TUNNING ALGORITHM FOR MOTION GENERATOR | paper_content.txt 行 497-498
    - quote: "The door-motion FSM will generate reference motion values within the motor-capacity using a given door weight."
    - supports: generates reference motion values within motor capacity for the given door weight
- `[E10]` STM §1 摘录 C | paper.pdf p.6 §4 MOTION BASED ON FSM | paper_content.txt 行 379-383
    - quote: "The states (init., positive, negative, and stop) have two sub-levels."
    - supports: high-level modes include init, positive, negative, and stop, refined into sub-levels
- `[E11]` STM §1 摘录 C | paper.pdf p.6 §4 MOTION BASED ON FSM | paper_content.txt 行 383-386
    - quote: "The first sub-level contains positive motion profile sector-switching (sectors I to VIII – see Fig. 8)."
    - supports: positive motion first sub-level switches across sectors I to VIII
- `[E12]` STM §1 摘录 C | paper.pdf p.7 §4 MOTION BASED ON FSM | paper_content.txt 行 400-402
    - quote: "The second sub-level finally concludes the equations for motion calculations (1, 2, and 3)."
    - supports: second sub-level concludes motion-calculation equations
- `[E13]` STM §1 摘录 C | paper.pdf p.7 §4 MOTION BASED ON FSM | paper_content.txt 行 407-408
    - quote: "S20 (Fig. 12) includes the states for the first sector motion calculation"
    - supports: S20 covers first-sector motion calculation
- `[E14]` paper.pdf p.3 §2 SYSTEM DESCRIPTION | paper_content.txt 行 153-156
    - quote: "The event occurs when a specific input or function condition is met."
    - supports: transitions are driven by input or function conditions
- `[E15]` STM §1 摘录 B | paper.pdf p.2 §2 SYSTEM DESCRIPTION | paper_content.txt 行 129-134
    - quote: "door_closed AND person_detected command_open OR person_detected"
    - supports: examples combine door_closed with person_detected, or command_open with person_detected
- `[E16]` STM §1 摘录 C | paper.pdf p.7 §4 MOTION BASED ON FSM | paper_content.txt 行 397-399
    - quote: "The transition table’s blue fields represent the events and actions from the main level. Each state in the sub-level is also conditioned from the main level."
    - supports: sub-level states remain conditioned by events and actions from the main level
- `[E17]` STM §1 摘录 D | paper.pdf p.10 §5 SELF-TUNNING ALGORITHM FOR MOTION GENERATOR | paper_content.txt 行 501-503
    - quote: "The door during normal operation goes into blockade detection when the motion is forcefully interrupted (obstacle collision or any other movement prevention)."
    - supports: forceful interruption leads to blockade detection
- `[E18]` STM §1 摘录 D | paper.pdf p.10 §5 SELF-TUNNING ALGORITHM FOR MOTION GENERATOR | paper_content.txt 行 504-505
    - quote: "In this case the door changes movement direction or stops with an error indicator after three subsequent attempts."
    - supports: changes movement direction and stops with error indicator after three attempts

</details>

- **intentional omissions**：未加入 valve 编号、具体传感器型号、数值阈值、任意状态急停或 forced reset，因为 paper.pdf 与 STM §1 均无这些原文支撑。也未写 positive mode 的默认内部初始子相位，因为原文只说明 sector 子层和 S20 示例，没有给进入 positive 后默认落点。

### #11 🏭 `prefabricated-board-transfer-palletizer-s7-1500-plc__01` (HSM)

- **case**: Manual-Maintenance-Auto Palletizer Supervisor
- **统计**：289 词 / 9 markers / 9 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ⚪ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The S7-1500 PLC controls a prefabricated-board transfer palletizer whose hardware includes transverse movement, lifting, bracket, pushing, positioning, and door-lifting mechanisms [E1]. The operator interface provides HMI instructions and monitoring, while the outer mode manager separates manual, maintenance, and automatic operation [E2]. Manual mode supports protected single-step execution, maintenance mode supports debugging and device-exception work by clicking, and automatic mode performs normal production according to HMI-issued instructions [E3]. Within automatic mode, the controller selects operational phases such as board storage, board retrieval, frame transverse movement, platform lifting, combined transverse-plus-lifting, board taking, or board sending, then starts the selected predefined sequence when the automatic start button is pressed [E4]. Target selection uses the kiln number as the named variable: a number at most 20 selects kiln A, a number from 21 to 41 selects kiln B, a number above 41 is invalid and is reset to 0, and MOD/DIV calculations derive the target column and layer [E5]. A storage cycle moves the board from the roller conveyor line through transverse movement, lifting, door opening, conveying, pushing, and door closing, while retrieval opens the door, hooks, closes the door, conveys, lifts, traverses, and returns the board to the roller conveyor line [E6]. Motion and IO subroutines drive motors, positioning devices, door-lifting claws, push/hook hardware, frequency converters, hydraulic cylinders, and indicator lights while reading sensors, station buttons, converter status, and motor status [E7]. After failure, restart, or work completion, initialization resets startup parameters, working mode, motor-protection and emergency-stop faults, and the palletizer initial state at A1-1 [E8]. During operation, the alarm interface presents frequency-converter faults, motor malfunctions, limit triggers, and sensor failures for operator verification, and the stop button halts all operations before clear resets indicators, operation modes, and the kiln-template number [E9].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：expanded_nl 用 outer manual/maintenance/automatic mode 加 automatic 内部 operational phases 暴露层次结构，但原文只支持 automatic start 后进入所选预定义序列，未给出更深的默认 init 子状态；对应 [E2][E4]。
- **G 守卫算术**：G 钩子来自 kiln number 变量的区间判定：≤20 为 kiln A、21-41 为 kiln B、>41 为无效并置 0，再用 MOD/DIV 计算 column/layer；对应 [E5]。
- **A 动作**：A 钩子来自 storage/retrieval 的多步动作链和 motion/IO 子程序对电机、定位装置、门爪、push/hook、变频器、液压缸、指示灯等执行器的控制；对应 [E6][E7]。
- **F 故障恢复**：F 轴只弱覆盖：原文支持 initialization reset motor-protection/emergency-stop faults、HMI alarm verification、stop/clear reset，但不支持任意状态强制进入 Safe mode；对应 [E8][E9]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain、implicit-action-prose 和 multivar-guard 三类 baseline-trap：PLC/HMI/变频器等领域术语、跨句动作链、kiln number 区间与 MOD/DIV 计算；对应 [E5][E6][E7]。
- **ft fcstm-fit**：pyfcstm 适配主要体现在层次 mode-to-phase 表达、kiln number 的可 SMT 化算术守卫、以及硬件执行器与传感器读写可抽象成 action handler；对应 [E2][E4][E5][E7]，forced+aspect 横切覆盖较弱。

</details>

<details><summary>provenance (9条)</summary>

- `[E1]` paper.pdf p.1 §2 | paper_content.txt 行 22-24
    - quote: "consisting primarily of a transverse movement system, a lifting system, a bracket, a pushing mechanism, transverse movement positioning devices, lifting positioning devices"
    - supports: hardware includes transverse movement, lifting, bracket, pushing, positioning, and door-lifting mechanisms
- `[E2]` STM §1 摘录 B | paper.pdf p.5 §4.2 | paper_content.txt 行 215-222
    - quote: "The control mode of the palletizer is divided into manual mode, maintenance mode, and automatic mode."
    - supports: outer mode manager separates manual, maintenance, and automatic operation
- `[E3]` STM §1 摘录 B | paper.pdf p.5 §4.2 | paper_content.txt 行 216-222
    - quote: "Manual mode is primarily utilized for scenarios requiring single-step execution"
    - supports: manual single-step, maintenance debugging/exception work, automatic HMI-commanded production
- `[E4]` STM §1 摘录 C | paper.pdf p.6 §4.3 | paper_content.txt 行 236-241
    - quote: "Upon pressing the automatic start button, the palletizer executes its tasks automatically in accordance with a predefined sequence of actions."
    - supports: automatic operational phases and predefined sequence after automatic start
- `[E5]` paper.pdf p.5 §4.1 | paper_content.txt 行 208-212
    - quote: "If the kiln number is less than or equal to 20, it is classified as kiln A"
    - supports: kiln-number guard ranges, invalid reset to 0, and MOD/DIV column/layer calculation
- `[E6]` STM §1 摘录 A | paper.pdf p.2 §3.1 | paper_content.txt 行 62-70
    - quote: "through a series of movements, including transverse movement, lifting, opening the door, conveying, pushing, and closing the door"
    - supports: storage and retrieval action sequences
- `[E7]` paper.pdf p.6 §4.3 | paper_content.txt 行 242-260
    - quote: "gathering input signals from sensors, operation station buttons, frequency converter operating status, motor operating status"
    - supports: IO and motion subroutines reading inputs and driving equipment
- `[E8]` STM §1 摘录 C | paper.pdf p.6 §4.3 | paper_content.txt 行 230-235
    - quote: "resetting working mode, motor protection and emergency stop faults, as well as controlling the reset of the palletizer’s initial state"
    - supports: initialization reset after failure/restart/completion and reset to initial state
- `[E9]` paper.pdf p.7-p.8 §4.4-§5 | paper_content.txt 行 276-279, 337-339
    - quote: "Press the “stop” button while the palletizer is in operation to halt all operations."
    - supports: alarm presentation, stop halt, and clear reset behavior

</details>

- **intentional omissions**：没有编造任意状态 emergency forced transition、safe-state 名称、阈值时间、传感器型号或具体阀门编号。原文虽有报警与 stop/clear，但未明确给出全局故障恢复路径，因此只写弱恢复语义。

### #12 ⚙️ `state-machine-based-hybrid-position-force-control-waste-mobile-robot__01` (HSM)

- **case**: Pick-and-drop supervisor for the waste-selection manipulator
- **统计**：251 词 / 10 markers / 10 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The pick-and-drop controller for the 5DOF waste-selection manipulator is a state-machine supervisor organized around the main machine plus homing, position-control, and force-control sub-sections [E1]. At startup, each motor/DOF is initialized and homed [E2]; when homing completes, the controller enters stable state Si3, the starting point for later control sequences [E3]. A new task provides object type, target coordinates, and Z-axis rotation [E4]; the supervisor first drives the XOY positioning joints and then starts vertical motion and gripper orientation [E5]. The physical effectors behind those actions include the Festo EXCM planar gantry for horizontal XOY motion, the Festo EGSK electrical slide for OZ displacement, the Festo ERMO rotary motor for orientation, and the Festo HGPLE gripper jaws [E6]. During the task sequence, the Z-axis position error ΔPz is compared with the allowed error εPz, and the top-position move is issued before gripper opening and force computation steps [E7]. Once vertical position and orientation are ready, the supervisor changes the gripper DOF from position control to force control by updating the S-matrix, closes the jaws, and applies the reference force Fjaws to grip the target [E8]. While the gripper force remains within the force-error tolerance ΔFjaws ≤ εFjaws, the other four DOFs lift the object, rotate and move above the waste tray, then the supervisor switches back to position control and opens the jaws to drop it [E9]. The loop runs only while emergency stop ES is false, and the state list assigns SES to the emergency-stop case under the position/force-control diagrams [E10].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 覆盖明确：[E1] 暴露 main + homing/position-control/force-control 子段结构，[E2][E3] 暴露启动后经 homing 落到 Si3 作为后续控制序列起点。
- **G 守卫算术**：G 钩子在 [E7][E9]：ΔPz 与 εPz 的 Z 轴误差比较、ΔFjaws ≤ εFjaws 的力误差容差条件均以自然语言表达，未写伪代码。
- **A 动作**：A 钩子在 [E6][E8][E9]：具体硬件执行器、S-matrix 更新、位置/力控切换、闭合/打开 gripper jaws 都是非平凡动作。
- **F 故障恢复**：F 覆盖较弱但存在：[E10] 只支持 emergency stop 条件 ES 和 SES 急停状态；原文未给出急停后的自动恢复路径。
- **bd baseline-trap**：expanded_nl 命中 cross-section、implicit-domain、implicit-action-prose 和 multivar-guard：状态层次来自 [E1]-[E3]，S-matrix/DOF/误差容差来自 [E7]-[E9]，硬件动作散落在 [E6]-[E9]。
- **ft fcstm-fit**：pyfcstm fit 中等偏强：[E1]-[E3] 适合复合状态与 init 链，[E7][E9] 适合 Expr-IR 数值守卫，[E6][E8][E9] 适合 abstract action 与 effector 解耦；forced+aspect 横切语义只由 [E10] 弱支持。

</details>

<details><summary>provenance (10条)</summary>

- `[E1]` STM §1 摘录 C | paper.pdf p.6 Figure 4 / Section 3 | paper_content.txt 行 227-235
    - quote: "These are the homing state machine, the position control state machine, and the force control state machine."
    - supports: main machine plus homing, position-control, and force-control sub-sections
- `[E2]` paper.pdf p.16 §6 | paper_content.txt 行 563-568
    - quote: "initialize the motors and start the homing process for each motor"
    - supports: startup initialization and homing of each motor/DOF
- `[E3]` STM §1 摘录 C | paper.pdf p.6 Section 3 | paper_content.txt 行 236-239
    - quote: "transitions to the stable state Si3. This state is the starting point"
    - supports: controller enters Si3 as the starting point for later control sequences
- `[E4]` STM §1 摘录 D | paper.pdf p.7 Algorithm 1 | paper_content.txt 行 261-262
    - quote: "get (ObjType, Txyz, Rz)"
    - supports: new task provides object type, target coordinates, and Z-axis rotation
- `[E5]` STM §1 摘录 D | paper.pdf p.6 Section 3 | paper_content.txt 行 239-242
    - quote: "starting with the first two translation joints for positioning on XOY plane. Then, the vertical motion and orientation begin"
    - supports: first XOY positioning, then vertical motion and gripper orientation
- `[E6]` paper.pdf p.4 §2 | paper_content.txt 行 177-186
    - quote: "Festo planar surface gantry EXCM / Festo electrical slide EGSK / Festo rotary motor ERMO / Festo HGPLE gripper"
    - supports: named physical effectors for XOY motion, OZ displacement, orientation, and gripper jaws
- `[E7]` STM §1 摘录 D | paper.pdf p.7 Algorithm 1 | paper_content.txt 行 262-266, 290-291
    - quote: "if (∆P + z > εPz) GripperMove (Ttop) ... Jaws (open) Compute (Fjaws)"
    - supports: Z-axis position-error guard and top-position move before opening and force computation
- `[E8]` STM §1 摘录 D | paper.pdf p.6 Section 3 / p.7 Algorithm 1 | paper_content.txt 行 241-244, 270-272, 289
    - quote: "changing the control type ... within the S-matrix / using the reference force"
    - supports: switch from position to force control, update S-matrix, close jaws, and apply Fjaws
- `[E9]` STM §1 摘录 D | paper.pdf p.6-7 Section 3 / Algorithm 1 | paper_content.txt 行 245-248, 273-279, 292-293
    - quote: "while (∆Fjaws ≤ εFjaws) GripperMove (Ttop) GripperRotate (Rtray) GripperMove (Ttray) / Jaws (open)"
    - supports: force-error tolerance, lift/rotate/move above tray, switch back, and open jaws
- `[E10]` STM §1 摘录 B/D | paper.pdf p.5 Table 1, p.6-7 Algorithm 1 | paper_content.txt 行 220-221, 255, 280-282
    - quote: "while (!ES &&New Task) / SES Position Control/Force Control Emergency stop"
    - supports: loop conditioned on ES being false and SES emergency-stop state under position/force control

</details>

- **intentional omissions**：没有加入原文未给出的阀门编号、传感器型号、超时阈值、从任意状态强制跳转到 Safe 的恢复路径。急停只写到 ES/SES，不扩展成自动恢复或全局 forced transition。

### #13 🌡️ `virtual-commissioning-wick-soilless-cultivations__01` (HSM)

- **case**: Hierarchical nutrient-solution management supervisor
- **统计**：255 词 / 20 markers / 20 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The NSM supervisor controls a wick-soilless cultivation test-bench module responsible for preparing nutrient solutions with established pH and EC values [E1]. In the filtration phase, tap water enters T110 through the V110 solenoid valve and P110 sends it through the F110 inverse-osmosis filter [E2], then filtered water accumulates in T120 and reaches recipe preparation through P120 [E3], and digital level sensors trigger filling and emptying operations [E4]. The state-machine behaviour first fills T110 and T120 and sends filtered water to T240 [E5]; for each plant sample it assigns specific target EC and pH values [E6]. During recipe preparation, C200 agitates T220/T230 [E7] and supplies air to T240 [E8], while P210/P220/P230 deliver acid and nutrients for pH/EC control [E9], and Q240/I240 sense pH/EC while A240 continuously senses liquid height [E10]. The PLC model is hierarchical: region, state, and substate variables implement three layers [E11], the working composite contains nested states selected by CASE logic [E12], and entry to nutrient solution generation sets the initial nested substate [E13]. Common actions are attached to composite behaviour, so C200 works throughout all preparation steps [E14] and is on when nutrient solution generation is active [E15]; the waiting state executes an exit behaviour selecting the production-line tank to refill [E16]. Outside the nominal chain, an alarm state automatically stops the system in case of malfunctioning [E17], and its transition fires when the HMI alarm interrupter is pressed [E18], when mixing-tank liquid volume exceeds the high threshold limit value [E19], or when the acid or concentrated nutrient tanks need refilling [E20].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴由三层 region/state/substate、working 复合状态的 nested states，以及 nutrient solution generation 的 entry 初始子状态设置暴露；关键 mode/子相位为 working、waiting、nutrient solution generation，对应 [E11][E12][E13]。
- **G 守卫算术**：G 轴由 plant sample 决定 EC/pH target 与 alarm transition 的复合自然语言条件暴露，具名变量包括 mixing-tank liquid volume、acid stock、concentrated nutrient tanks；原文只给 high threshold limit value 而无具体数值，对应 [E6][E18][E19][E20]。
- **A 动作**：A 轴由 V110/P110/P120 过滤动作、C200/P210/P220/P230/Q240/I240/A240 硬件动作与传感、nutrient solution generation entry init、waiting exit tank selection、C200 state-active action 暴露，对应 [E2][E3][E7][E8][E9][E10][E13][E14][E15][E16]。
- **F 故障恢复**：F 轴由 alarm state 自动停止 malfunction 及三类触发条件暴露，但原文未说明 from any state 的全局 forced transition 或 alarm 后恢复路径，因此只保守写 safe-stop 分支，对应 [E17][E18][E19][E20]。
- **bd baseline-trap**：expanded_nl 命中 implicit-domain（NSM、pH/EC、T/P/Q/I/A 编号）、implicit-action-prose（过滤、配液、entry/exit 行为散叙述）、multivar-guard 与 composite-internal（working/nutrient solution generation 嵌套和 alarm 三条件），对应 [E1][E2][E3][E7][E8][E9][E10][E11][E12][E13][E17][E18][E19][E20]。
- **ft fcstm-fit**：expanded_nl 暴露深复合 init 链 [E11][E12][E13]、多条件守卫 [E18][E19][E20]、以及可抽象为 effector-agnostic actions 的执行器/传感器动作 [E2][E3][E7][E8][E9][E10][E14][E15][E16]；forced+aspect 覆盖较弱，仅 C200 common action 有 aspect-like 线索。

</details>

<details><summary>provenance (20条)</summary>

- `[E1]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 348-349
    - quote: "The Nutrient Solution Module (NSM) is responsible for preparing nutrient solutions with an established value of pH and EC"
    - supports: NSM prepares nutrient solutions with established pH and EC values
- `[E2]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 350-352
    - quote: "Tap water is collected into the T110 tank through the activation of the V110 solenoid valve. Then, the P110 pump supplies the water into the F110 inverse osmosis filter"
    - supports: V110 admits tap water into T110 and P110 sends it through F110
- `[E3]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 352-354
    - quote: "the filtered water is accumulated into the T120 tank connected to the recipe preparation unit through the P120 pump"
    - supports: filtered water accumulates in T120 and reaches recipe preparation through P120
- `[E4]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 354-355
    - quote: "Two digital level sensors are placed into the two tanks for triggering the filling and emptying operations"
    - supports: digital level sensors trigger filling and emptying operations
- `[E5]` STM §1 摘录 B | paper.pdf p.11 §5 | paper_content.txt 行 456-459
    - quote: "A sequential behaviour is implemented by first filling tanks T110 and T120, and then sending the filtered water to the T240 mixing tank"
    - supports: state-machine sequence fills T110/T120 and sends filtered water to T240
- `[E6]` STM §1 摘录 B | paper.pdf p.11 §5 | paper_content.txt 行 459-460
    - quote: "a specific target value of EC and pH is assigned based on the considered sample of plants"
    - supports: plant sample determines target EC and pH values
- `[E7]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 356-357
    - quote: "C200 air compressor agitates the fertilizer tanks T220 and T230 to prevent the concentrated nutrients from settling down"
    - supports: C200 agitates T220/T230
- `[E8]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 358-359
    - quote: "Air is also delivered to the T240 mixing tank for mixing the nutrients during the preparation of the solution"
    - supports: C200 supplies air to T240 for mixing during preparation
- `[E9]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 362-363
    - quote: "Peristatic pumps P210, P220 and P230 delivers acid and nutrients for the control of the pH and EC of the solution"
    - supports: P210/P220/P230 deliver acid and nutrients for pH/EC control
- `[E10]` STM §1 摘录 A | paper.pdf p.8 §4.1 | paper_content.txt 行 363-365
    - quote: "The actual value of the pH and EC is respectively sensed with the Q240 and I240 meters. The A240 analogue level sensor continuously senses the liquid height within the tank"
    - supports: Q240/I240 sense pH/EC and A240 senses liquid height
- `[E11]` STM §1 摘录 C | paper.pdf p.11 §5 | paper_content.txt 行 483-485
    - quote: "The NSM state machine has three hierarchical layers (i.e., composite behaviours) that are implemented with the region, state and substate scalar variables"
    - supports: region/state/substate variables implement three hierarchical layers
- `[E12]` STM §1 摘录 C | paper.pdf p.12 §5 | paper_content.txt 行 494-496
    - quote: "The CASE construct selects the active state among the nested states of the ‘working’ composite state"
    - supports: working composite contains nested states selected by CASE logic
- `[E13]` STM §1 摘录 C | paper.pdf p.12 §5 | paper_content.txt 行 498-499
    - quote: "the ‘nutrient solution generation’ composite state executes an entry behaviour to set the initial state among its nested substates"
    - supports: entry to nutrient solution generation sets its initial nested substate
- `[E14]` STM §1 摘录 B | paper.pdf p.11 §5 | paper_content.txt 行 461-464
    - quote: "the C200 air compressor must work throughout all the steps of preparation of the nutrient solution"
    - supports: C200 works throughout all preparation steps as a common composite action
- `[E15]` STM §1 摘录 C | paper.pdf p.12 §5 | paper_content.txt 行 502-506
    - quote: "the C200 air compressor when the ‘nutrient solution generation’ state is active"
    - supports: C200 is on when nutrient solution generation is active
- `[E16]` STM §1 摘录 C | paper.pdf p.12 §5 | paper_content.txt 行 496-497
    - quote: "The ‘waiting’ state implements an exit behaviour for selecting the tank of the ‘production line’ that must be refilled"
    - supports: waiting exit behaviour selects the production-line tank to refill
- `[E17]` STM §1 摘录 B | paper.pdf p.11 §5 | paper_content.txt 行 464-465
    - quote: "an ‘alarm’ state is implemented for automatically stopping the system in case of malfunctioning"
    - supports: alarm state automatically stops the system in malfunction cases
- `[E18]` STM §1 摘录 B | paper.pdf p.11 §5 | paper_content.txt 行 466-467
    - quote: "the operator presses the ‘alarm’ interrupter on the HMI"
    - supports: alarm transition fires on HMI alarm interrupter press
- `[E19]` STM §1 摘录 B | paper.pdf p.11 §5 | paper_content.txt 行 467-468
    - quote: "the liquid volume within the mixing tank is above a ‘high threshold limit value’"
    - supports: alarm transition fires when mixing-tank liquid volume exceeds the high threshold
- `[E20]` STM §1 摘录 B | paper.pdf p.11 §5 | paper_content.txt 行 468
    - quote: "the acid or the concentrated nutrient tanks must be refilled"
    - supports: alarm transition fires when acid or concentrated nutrient tanks need refilling

</details>

- **intentional omissions**：未补充具体 pH/EC 数值阈值、液位数值、全部状态名、alarm 后恢复路径或 from any state 的强制跳转，因为原文没有给出这些信息。也未从 Fig. 8 图内状态机臆测额外 valve 编号或恢复路径。

### #14 ✈️ `autonomous-uav-multimodal-mapping-underground-mines__01` (HSM)

- **case**: Mission supervisor for mine exploration and pillar inspection
- **统计**：269 词 / 18 markers / 18 provenance entries
- **轴覆盖**：⚪ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The underground-mine UAV mission supervisor starts from a data-recording initial state, then selects manual flight, reactive exploration, or supervised autonomous pillar inspection; each mode has its own FSM for flight-phase transitions, safety, and data integrity [E1][E2]. In the manual branch, the operator keeps attitude and thrust authority through the RC transmitter, while the flight controller handles state estimation and stability and the onboard computer stores robot and payload data [E3][E4]. Data recording is independent of flight status, so the operator can fly to a region of interest and engage high-bandwidth LiDAR and camera recording only when necessary [E5][E6]. In reactive exploration, the controller takes off to a safe altitude, finds the most open space, adjusts attitude toward it, and moves with commanded velocity; the mode uses LiDAR sensing to identify the largest-range sector and heading error toward the open area [E7][E8][E9]. A PD controller stops the drone if it gets too close to a pillar, and because the mode is supervised, the operator can take control or land the UAV at any moment [E10][E11]. In supervised pillar inspection, the operator positions the drone before the pillar; the mission maintains fixed distance and velocity, performs horizontal back-and-forth passes at incremental altitudes, and uses three forward LiDARs for corners plus one upward LiDAR for ceiling distance [E12][E13][E14][E15]. During this scan, the ceiling-distance guard compares dceil with tolerance tol: dceil greater than tol returns the inspection through altitude adjustment, while dceil at or below tol branches toward landing [E16]. Across operation, the system supports RC recovery during emergencies, manual fallback on autonomy failure, and a hardware kill switch for emergency shutdown [E17][E18].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴由第一句暴露：data-recording 初始状态、manual/reactive/pillar 三个顶层 mission mode，以及每个 mode 自有 FSM 管理 flight phases [E1][E2]；原文未提供更深的完整嵌套 init 链。
- **G 守卫算术**：G 轴主要来自 ceiling-distance guard：具名变量 dceil 与 tol 形成自然语言阈值分支，dceil > tol 回到 altitude adjustment，dceil ≤ tol 进入 landing 分支 [E16]；原文未给 tol 数值。
- **A 动作**：A 轴覆盖 RC 控制、flight controller 稳定、onboard storage、LiDAR/camera recording、V_cmd/attitude command、PD stop、pillar sweeping 与 LiDAR corner/ceiling sensing 等非平凡动作 [E3]-[E15]。
- **F 故障恢复**：F 轴由 supervised takeover/landing、RC emergency recovery、autonomy failure manual fallback 与 hardware kill switch 支撑 [E11][E17][E18]；原文没有细化到任意状态强制跳转到某个具体 safe state。
- **bd baseline-trap**：expanded_nl 命中 cross-section 信息拆段、implicit-domain UAV/LiDAR 术语、implicit-action-prose 散叙述动作，以及带应急语义的 global-cross-cutting fallback 片段 [E1][E7][E10][E17][E18]。
- **ft fcstm-fit**：pyfcstm fit 主要来自层次 mode+per-mode FSM [E1][E2]、dceil/tol 数值守卫 [E16]、以及 RC/flight-controller/onboard-computer/LiDAR/camera 这类可抽象为 effector-agnostic action 的硬件交互 [E3]-[E6][E15]；多变量 SMT 守卫和完整 forced reset 链覆盖较弱。

</details>

<details><summary>provenance (18条)</summary>

- `[E1]` STM §1 摘录 B | paper.pdf p.13 Figure 6 | paper_content.txt 行 721-725
    - quote: "initial state to record data, and three different options: manual flight (mission 1), reactive exploration (mission 2), and supervised autonomous inspection (mission 3)."
    - supports: data-recording initial state and three selectable mission modes
- `[E2]` STM §1 摘录 A | paper.pdf p.12 §3.5 | paper_content.txt 行 668-670
    - quote: "Each mode is governed by its own FSM, which manages transitions between flight phases, ensuring safety and data integrity."
    - supports: each mode has its own FSM for flight-phase transitions, safety, and data integrity
- `[E3]` paper.pdf p.13 §3.5.1 | paper_content.txt 行 727-729
    - quote: "the operator maintains control over the vehicle’s attitude and thrust via a standard RC transmitter."
    - supports: manual branch RC attitude and thrust authority
- `[E4]` paper.pdf p.13 §3.5.1 | paper_content.txt 行 729-731
    - quote: "the flight controller handles state estimation and stability, while the onboard computer stores sensor data recorded by the robot and the payload."
    - supports: flight controller and onboard computer actions
- `[E5]` STM §1 摘录 C | paper.pdf p.13 §3.5.1 | paper_content.txt 行 731-733
    - quote: "A dedicated “Data recording” mission can be started independently of the flight status"
    - supports: data recording independent of flight status
- `[E6]` STM §1 摘录 C | paper.pdf p.13 §3.5.1 | paper_content.txt 行 733-734
    - quote: "engage the high-bandwidth recording (LiDAR and cameras) only when necessary."
    - supports: high-bandwidth LiDAR and camera recording action
- `[E7]` STM §1 摘录 B | paper.pdf p.13 Figure 6 | paper_content.txt 行 721-725
    - quote: "takes off to a safe altitude, finds the most open space, adjusts its attitude towards it and move with the commanded velocity toward it."
    - supports: reactive exploration takeoff, attitude adjustment, and commanded velocity
- `[E8]` paper.pdf p.13 §3.5.2 | paper_content.txt 行 736-738
    - quote: "This mode relies on an 8-point LiDAR tower mounted on the second version of the drone or on the Livox LiDAR"
    - supports: LiDAR sensing used in reactive exploration
- `[E9]` paper.pdf p.13 §3.5.2 | paper_content.txt 行 739-740
    - quote: "identifies the sector with the largest range and calculates the angular error"
    - supports: largest-range sector and heading-error computation
- `[E10]` paper.pdf p.14 §3.5.2 | paper_content.txt 行 777-778
    - quote: "A PD controller is implemented to guarantee that the drone stops if it gets too close to a pillar."
    - supports: PD controller stop action near a pillar
- `[E11]` paper.pdf p.14 §3.5.2 | paper_content.txt 行 778-779
    - quote: "the operator can take control or land the UAV at any moment."
    - supports: supervised takeover or landing escape
- `[E12]` paper.pdf p.14 §3.5.3 | paper_content.txt 行 790-791
    - quote: "The operator positions the drone in front of the target pillar and initiates the mission."
    - supports: operator positions the drone before pillar inspection
- `[E13]` paper.pdf p.14 §3.5.3 | paper_content.txt 行 784-786
    - quote: "maintaining a fixed distance and velocity relative to the structure."
    - supports: fixed distance and velocity during pillar inspection
- `[E14]` STM §1 摘录 D | paper.pdf p.14 §3.5.3 | paper_content.txt 行 786-789
    - quote: "horizontal back-and-forth (sweeping) pattern."
    - supports: back-and-forth sweeping passes
- `[E15]` STM §1 摘录 D | paper.pdf p.14 §3.5.3 | paper_content.txt 行 792-794
    - quote: "four LiDARs, with three pointing forward to identify corners and one pointing up to measure the distance to the ceiling."
    - supports: three forward LiDARs for corners and one upward LiDAR for ceiling distance
- `[E16]` paper.pdf p.13 Figure 6 | paper_content.txt 行 695-714
    - quote: "Update altitude; dceil > tol; dceil ≤ tol; Start landing"
    - supports: ceiling-distance tolerance guard and altitude-adjustment versus landing branch
- `[E17]` paper.pdf p.10 §3.4 | paper_content.txt 行 575-576
    - quote: "uses a remote controller (RC) for manual data logging or to recover the vehicle in an emergency while supervised autonomous missions run."
    - supports: RC recovery during emergencies
- `[E18]` paper.pdf p.7 Table 2 | paper_content.txt 行 370-374
    - quote: "Triggers manual control fallback during autonomy failure. Includes a hardware kill switch for emergency shutdown."
    - supports: manual fallback on autonomy failure and emergency kill switch

</details>

- **intentional omissions**：没有补写 safe altitude、commanded velocity、tol、exploration time 或 PD threshold 的具体数值，因为原文没有给出这些参数。也没有枚举 Figure 6 的全部 state name，且没有把 emergency fallback 硬写成任意状态到某个 safe-state 的精确 forced transition。

### #15 ✈️ `hybrid-autonomy-future-mars-science-helicopter__01` (HSM)

- **case**: Mission-Phase FSM-BT Supervisor for Mars Science Helicopter
- **统计**：274 词 / 19 markers / 19 provenance entries
- **轴覆盖**：✅ H 层次 / ✅ G 守卫算术 / ✅ A 动作 / ✅ F 故障恢复 / ✅ bd baseline-trap / ✅ ft fcstm-fit

<details><summary>扩充 NL（带 inline citation markers）</summary>

> The Mars science helicopter autonomy executes a mission plan of science and operational tasks at predefined waypoints [E1], and its FSM-BT Autonomy sends high-level commands to PX4 for navigation and task execution [E2]. At the top level, a deterministic FSM manages mission phases, while behavior trees supply reactive task execution within the active phase [E3]. The mission hierarchy is explicit: phases such as Takeoff and Land are separate state classes [E4], and the FSM activates the corresponding behavior tree for the selected phase [E5]. Events reach the FSM from behavior-tree status returns or external sources such as Healthguard [E6]; Success and Failure are required by all states [E7], undefined events self-transition [E8], and BatteryLow or BatteryCritical events are emitted when predefined thresholds are violated [E9]. Healthguard monitors battery levels, actuator status, and estimator confidence [E10], while broader monitoring of vehicle state, battery levels, and onboard anomalies can trigger adaptive mission reconfiguration or fail-safe actions [E11]. During Takeoff, the tree first checks vehicle health [E12], sets PX4 to Offboard, arms the vehicle [E13], and executes takeoff with lateral position control and vertical velocity control; the takeoff timeout is dynamically calculated from vehicle velocity and distance to the takeoff waypoint [E14]. If a takeoff leaf node fails, a fallback sequence executes Descend, Land, and Disarm [E15]; if that recovery also fails, the behavior tree returns Failure and the FSM transitions to EmergencyLand [E16]. In Land, after successful mission execution, the vehicle attempts the closest identified landing site [E17]; if no site is available, it flies a lower-altitude search pattern, targets the most confident site, and lands [E18], with landing fallback failure also leading to EmergencyLand [E19].

</details>

<details><summary>axis_coverage 详述</summary>

- **H 层次**：H 轴由 mission-level FSM + phase-local BT 层次覆盖，expanded_nl 写出 Takeoff/Land 作为 phase state 且 FSM 激活对应 BT [E3][E4][E5]；但原文未给出复合状态默认 init 子相位，因此未写默认 init。
- **G 守卫算术**：G 轴弱覆盖：expanded_nl 仅能忠实写出 BatteryLow/BatteryCritical 在 predefined thresholds 被违反时触发 [E9]，以及 takeoff timeout 由 velocity 和 distance 动态计算 [E14]；原文未给具体阈值数值或完整复合 guard。
- **A 动作**：A 轴由 Takeoff 与 fallback/Land 动作覆盖，包括 set PX4 Offboard、arm、takeoff 控制、Descend/Land/Disarm、选择 landing site 并 landing [E13][E14][E15][E17][E18]。
- **F 故障恢复**：F 轴由 Healthguard fail-safe 与 EmergencyLand 恢复链覆盖：健康异常可触发 fail-safe action，takeoff/landing fallback failure 会使 FSM 转入 EmergencyLand [E11][E16][E19]；但原文未支持 from-any-state forced transition 句式。
- **bd baseline-trap**：bd 命中 implicit-domain、implicit-action-prose 与 composite-internal：PX4/Healthguard/estimator confidence 等领域术语、散叙述硬件动作与 phase 内 BT 行为交织出现 [E2][E9][E10][E13][E15]。
- **ft fcstm-fit**：ft 主要暴露 abstract action effector 解耦与部分多变量 guard/timeout 表达：PX4 command、Offboard/arming/landing 动作适合抽象 action，velocity+distance 动态 timeout 适合 Expr-IR 表达 [E2][E13][E14][E15]；深复合 init 与 forced+aspect 原文支持不足。

</details>

<details><summary>provenance (19条)</summary>

- `[E1]` paper.pdf p.3 §III.A | paper_content.txt 行 243-250
    - quote: "specific science and operational tasks at predefined waypoints"
    - supports: mission plan contains science and operational tasks at predefined waypoints
- `[E2]` paper.pdf p.3 §III.A | paper_content.txt 行 251-254
    - quote: "sends high-level commands to the PX4 Autopilot"
    - supports: FSM-BT Autonomy sends high-level commands to PX4 for navigation/task execution
- `[E3]` STM §1 摘录 A | paper.pdf p.2 Introduction / Contributions | paper_content.txt 行 104-109
    - quote: "The FSM provides structured, deterministic state transitions, while BTs enable modular, reactive task execution"
    - supports: deterministic FSM plus reactive behavior trees
- `[E4]` STM §1 摘录 B | paper.pdf p.4 §III.B | paper_content.txt 行 315-320
    - quote: "Each state represents a mission phase"
    - supports: mission phases are state classes such as Takeoff and Land
- `[E5]` STM §1 摘录 B | paper.pdf p.4 §III.B | paper_content.txt 行 334-339
    - quote: "the FSM activates based on the mission phase"
    - supports: FSM activates the corresponding behavior tree for a selected phase
- `[E6]` STM §1 摘录 B | paper.pdf p.4 §III.B | paper_content.txt 行 321-325
    - quote: "may originate from behavior trees returned node status or external sources"
    - supports: events reach FSM from BT statuses and external sources
- `[E7]` paper.pdf p.4 §III.B | paper_content.txt 行 345-348
    - quote: "Success or Failure, which represent the BT status and are required by all states"
    - supports: Success and Failure events are required by all states
- `[E8]` STM §1 摘录 B | paper.pdf p.4 §III.B | paper_content.txt 行 327-329
    - quote: "it is treated as a self-transition to the current state"
    - supports: undefined events self-transition
- `[E9]` STM §1 摘录 B | paper.pdf p.4 §III.B | paper_content.txt 行 324-326
    - quote: "BatteryLow or BatteryCritical are emitted by the Healthguard when predefined thresholds are violated"
    - supports: BatteryLow/BatteryCritical threshold-triggered Healthguard events
- `[E10]` paper.pdf p.4 Figure 3 caption | paper_content.txt 行 303-308
    - quote: "detecting anomalies in actuator status, battery levels, and estimator confidence"
    - supports: Healthguard monitors battery, actuator status, and estimator confidence
- `[E11]` STM §1 摘录 A | paper.pdf p.2 Introduction / Contributions | paper_content.txt 行 116-118
    - quote: "vehicle state, battery levels, and onboard anomalies"
    - supports: monitoring can trigger adaptive reconfiguration or fail-safe actions
- `[E12]` paper.pdf p.4 §III.B Figure 4 text | paper_content.txt 行 386-392
    - quote: "the BT first checks the vehicle’s health status"
    - supports: Takeoff behavior tree begins with a vehicle-health check
- `[E13]` paper.pdf p.4 §III.B Figure 4 text | paper_content.txt 行 392-395
    - quote: "setting the PX4 mode to Offboard and then arming the vehicle"
    - supports: Takeoff actions set PX4 Offboard and arm the vehicle
- `[E14]` paper.pdf p.4 §III.B Figure 4 text | paper_content.txt 行 395-399
    - quote: "dynamically calculated based on the vehicle’s velocity and distance to the takeoff waypoint"
    - supports: takeoff timeout depends on velocity and distance to waypoint
- `[E15]` paper.pdf p.4 §III.B Figure 4 text | paper_content.txt 行 400-402
    - quote: "The Descend, Land, and Disarm actions are executed sequentially"
    - supports: fallback sequence actions after takeoff leaf failure
- `[E16]` STM §1 摘录 C | paper.pdf p.5 Figure 4 text | paper_content.txt 行 412-414
    - quote: "Failure status, causing a transition to the EmergencyLand state"
    - supports: failed recovery returns Failure and transitions to EmergencyLand
- `[E17]` paper.pdf p.5 Figure 4 text | paper_content.txt 行 414-416
    - quote: "the vehicle attempts to land at the closest identified landing site"
    - supports: Land phase targets closest identified landing site
- `[E18]` paper.pdf p.5 Figure 4 text | paper_content.txt 行 416-420
    - quote: "targets the most confident site and proceeds to land"
    - supports: lower-altitude search, confidence-based landing site choice, and landing
- `[E19]` STM §1 摘录 C | paper.pdf p.5 Figure 4 text | paper_content.txt 行 420-422
    - quote: "a transition to the EmergencyLand is executed"
    - supports: landing fallback failure transitions to EmergencyLand

</details>

- **intentional omissions**：没有加入具体电池阈值、速度/距离公式、传感器型号或全局 from-any-state EmergencyLand 规则，因为原文只说 predefined thresholds、动态计算 timeout 和若干失败路径。没有枚举全部 FSM state，也没有把 Figure 4 箭头补成完整转移表。

