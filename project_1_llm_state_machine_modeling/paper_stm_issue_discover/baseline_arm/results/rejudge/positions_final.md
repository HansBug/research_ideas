# 逐位判定结果（105 位）

口径：`original` = 主臂 v46 原判定；`regroup` = 本次判定组输出；`final` = 主 session 裁定后。⭐ 裁定只在收紧方向发生。

| # | 位 | 样本 | 谓词 | 组 | original | regroup | carrier | form | final | 变化 |
| --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | `EIS-0000-02|run1/0000-claude` | miss(60) | `stays_in` | R5 | miss | miss |  |  | miss | — |
| 2 | `EIS-0000-02|run2/0000-claude` | miss(60) | `stays_in` | R5 | miss | miss |  |  | miss | — |
| 3 | `EIS-0002-02|run2/0002-claude` | miss(60) | `reaches` | R6 | miss | hit | assertion | 合取项之一 | miss | — |
| 4 | `EIS-0004-01|run1/0004-claude` | miss(60) | `state_declared` | R4 | miss | miss |  |  | miss | — |
| 5 | `EIS-0004-01|run1/0004-gpt` | miss(60) | `state_declared` | R4 | miss | miss |  |  | miss | — |
| 6 | `EIS-0004-01|run3/0004-claude` | miss(60) | `state_declared` | R4 | miss | miss |  |  | miss | — |
| 7 | `EIS-0005-01|run1/0005-gpt` | miss(60) | `edge_declared` | R6 | miss | hit | assertion | 直接对应 | miss | — |
| 8 | `EIS-0005-01|run2/0005-claude` | miss(60) | `edge_declared` | R6 | miss | hit | assertion | 直接对应 | miss | — |
| 9 | `EIS-0005-02|run1/0005-gpt` | miss(60) | `containment` | R6 | miss | miss |  |  | miss | — |
| 10 | `EIS-0007-01|run1/0007-gpt` | miss(60) | `reaches` | R1 | miss | miss |  |  | miss | — |
| 11 | `EIS-0007-02|run2/0007-claude` | miss(60) | `occupancy_after` | R1 | miss | miss |  |  | miss | — |
| 12 | `EIS-0007-02|run3/0007-gpt` | miss(60) | `occupancy_after` | R1 | miss | miss |  |  | miss | — |
| 13 | `EIS-0009-01|run1/0009-claude` | miss(60) | `edge_declared` | R4 | miss | miss |  |  | miss | — |
| 14 | `EIS-0009-01|run3/0009-claude` | miss(60) | `edge_declared` | R4 | miss | miss |  |  | miss | — |
| 15 | `EIS-0009-01|run3/0009-gpt` | miss(60) | `edge_declared` | R4 | miss | miss |  |  | miss | — |
| 16 | `EIS-0010-05|run1/0010-gpt` | miss(60) | `event_consumed` | R5 | miss | hit | issue | 合取项之一 | hit | ⭐ miss→hit |
| 17 | `EIS-0010-05|run3/0010-gpt` | miss(60) | `event_consumed` | R5 | miss | hit | issue | 直接对应 | hit | ⭐ miss→hit |
| 18 | `EIS-0014-03|run2/0014-gpt` | miss(60) | `state_declared` | R7 | miss | hit | issue | 合取项之一 | hit | ⭐ miss→hit |
| 19 | `EIS-0014-04|run1/0014-gpt` | miss(60) | `action_declared` | R7 | miss | hit | issue | 直接对应 | hit | ⭐ miss→hit |
| 20 | `EIS-0016-02|run1/0016-claude` | miss(60) | `initial_target` | R6 | miss | miss |  |  | miss | — |
| 21 | `EIS-0019-01|run3/0019-claude` | miss(60) | `guard_distinguishable` | R8 | miss | miss |  |  | miss | — |
| 22 | `EIS-0024-01|run3/0024-gpt` | miss(60) | `action_declared` | R6 | miss | miss |  |  | miss | — |
| 23 | `EIS-0024-03|run1/0024-gpt` | miss(60) | `persists_until` | R6 | miss | miss |  |  | miss | — |
| 24 | `EIS-0025-01|run1/0025-gpt` | miss(60) | `NONE` | R2 | miss | miss |  |  | miss | — |
| 25 | `EIS-0025-01|run3/0025-claude` | miss(60) | `NONE` | R2 | miss | miss |  |  | miss | — |
| 26 | `EIS-0026-01|run2/0026-claude` | miss(60) | `cardinality` | R3 | miss | miss |  |  | miss | — |
| 27 | `EIS-0026-01|run2/0026-gpt` | miss(60) | `cardinality` | R3 | miss | miss |  |  | miss | — |
| 28 | `EIS-0026-03|run1/0026-claude` | miss(60) | `reaches` | R3 | miss | miss |  |  | miss | — |
| 29 | `EIS-0026-03|run3/0026-claude` | miss(60) | `reaches` | R3 | miss | miss |  |  | miss | — |
| 30 | `EIS-0027-01|run2/0027-gpt` | miss(60) | `reaches` | R3 | miss | miss |  |  | miss | — |
| 31 | `EIS-0027-01|run3/0027-claude` | miss(60) | `reaches` | R3 | miss | miss |  |  | miss | — |
| 32 | `EIS-0029-01|run2/0029-claude` | miss(60) | `containment` | R3 | miss | miss |  |  | miss | — |
| 33 | `EIS-0032-01|run2/0032-gpt` | miss(60) | `initial_target` | R5 | miss | miss |  |  | miss | — |
| 34 | `EIS-0033-02|run2/0033-gpt` | miss(60) | `NONE` | R7 | miss | hit | issue | 蕴含更根本的原因 | miss | — |
| 35 | `EIS-0034-03|run1/0034-claude` | miss(60) | `action_declared` | R8 | miss | miss |  |  | miss | — |
| 36 | `EIS-0034-03|run2/0034-claude` | miss(60) | `action_declared` | R8 | miss | miss |  |  | miss | — |
| 37 | `EIS-0034-05|run2/0034-claude` | miss(60) | `NONE` | R8 | miss | miss |  |  | miss | — |
| 38 | `EIS-0035-03|run1/0035-gpt` | miss(60) | `NONE` | R5 | miss | hit | assertion | 蕴含更根本的原因 | miss | — |
| 39 | `EIS-0035-03|run3/0035-gpt` | miss(60) | `NONE` | R5 | miss | miss |  |  | miss | — |
| 40 | `EIS-0036-01|run2/0036-gpt` | miss(60) | `reaches` | R7 | miss | miss |  |  | miss | — |
| 41 | `EIS-0036-01|run3/0036-gpt` | miss(60) | `reaches` | R7 | miss | miss |  |  | miss | — |
| 42 | `EIS-0036-02|run3/0036-gpt` | miss(60) | `terminates` | R7 | miss | miss |  |  | miss | — |
| 43 | `EIS-0039-01|run3/0039-gpt` | miss(60) | `edge_declared` | R2 | miss | miss |  |  | miss | — |
| 44 | `EIS-0039-02|run2/0039-claude` | miss(60) | `guard_distinguishable` | R2 | miss | miss |  |  | miss | — |
| 45 | `EIS-0039-02|run2/0039-gpt` | miss(60) | `guard_distinguishable` | R2 | miss | miss |  |  | miss | — |
| 46 | `EIS-0040-01|run2/0040-claude` | miss(60) | `event_consumed` | R4 | miss | miss |  |  | miss | — |
| 47 | `EIS-0042-01|run1/0042-claude` | miss(60) | `occupancy_after` | R4 | miss | miss |  |  | miss | — |
| 48 | `EIS-0046-01|run1/0046-claude` | miss(60) | `initial_target` | R7 | miss | miss |  |  | miss | — |
| 49 | `EIS-0046-01|run2/0046-claude` | miss(60) | `initial_target` | R7 | miss | miss |  |  | miss | — |
| 50 | `EIS-0046-03|run1/0046-gpt` | miss(60) | `initial_target` | R7 | miss | miss |  |  | miss | — |
| 51 | `EIS-0046-03|run3/0046-gpt` | miss(60) | `initial_target` | R7 | miss | miss |  |  | miss | — |
| 52 | `EIS-0047-03|run2/0047-gpt` | miss(60) | `edge_declared` | R2 | miss | miss |  |  | miss | — |
| 53 | `EIS-0049-01|run1/0049-gpt` | miss(60) | `edge_declared` | R1 | miss | miss |  |  | miss | — |
| 54 | `EIS-0049-02|run3/0049-claude` | miss(60) | `containment` | R1 | miss | miss |  |  | miss | — |
| 55 | `EIS-0049-03|run3/0049-gpt` | miss(60) | `guard_distinguishable` | R1 | miss | miss |  |  | miss | — |
| 56 | `EIS-0050-01|run2/0050-claude` | miss(60) | `state_declared` | R3 | miss | miss |  |  | miss | — |
| 57 | `EIS-0055-01|run1/0055-claude` | miss(60) | `NONE` | R8 | miss | miss |  |  | miss | — |
| 58 | `EIS-0055-01|run2/0055-claude` | miss(60) | `NONE` | R8 | miss | miss |  |  | miss | — |
| 59 | `EIS-0056-01|run1/0056-gpt` | miss(60) | `guard_distinguishable` | R8 | miss | miss |  |  | miss | — |
| 60 | `EIS-0057-01|run3/0057-claude` | miss(60) | `initial_target` | R2 | miss | miss |  |  | miss | — |
| 61 | `EIS-0002-03|run3/0002-gpt` | hit(s1) | `cardinality` | R6 | hit | hit | issue | 直接对应 | hit | — |
| 62 | `EIS-0005-03|run2/0005-claude` | hit(s1) | `NONE` | R6 | hit | hit | issue | 蕴含更根本的原因 | hit | — |
| 63 | `EIS-0005-03|run3/0005-gpt` | hit(s1) | `NONE` | R6 | hit | hit | issue | 直接对应 | hit | — |
| 64 | `EIS-0006-01|run1/0006-gpt` | hit(s2) | `cardinality` | S2 | hit | hit | issue | 直接对应 | hit | — |
| 65 | `EIS-0006-01|run3/0006-claude` | hit(s2) | `cardinality` | S2 | hit | hit | issue | 直接对应 | hit | — |
| 66 | `EIS-0006-02|run2/0006-gpt` | hit(s2) | `effect_declared` | S2 | hit | hit | issue | 蕴含更根本的原因 | hit | — |
| 67 | `EIS-0006-03|run3/0006-gpt` | hit(s2) | `terminates` | S2 | hit | hit | issue | 合取项之一 | hit | — |
| 68 | `EIS-0007-01|run2/0007-claude` | hit(s2) | `reaches` | S4 | hit | hit | issue | 合取项之一 | hit | — |
| 69 | `EIS-0007-03|run1/0007-claude` | hit(s2) | `NONE` | S4 | hit | miss |  |  | miss | ⛔ hit→miss |
| 70 | `EIS-0009-02|run2/0009-claude` | hit(s2) | `state_declared` | S4 | hit | hit | issue | 合取项之一 | hit | — |
| 71 | `EIS-0010-02|run1/0010-gpt` | hit(s1) | `state_declared` | R5 | hit | hit | issue | 直接对应 | hit | — |
| 72 | `EIS-0010-03|run1/0010-claude` | hit(s1) | `terminates` | R5 | hit | hit | issue | 直接对应 | hit | — |
| 73 | `EIS-0010-04|run3/0010-gpt` | hit(s1) | `reaches` | R5 | hit | hit | issue | 直接对应 | hit | — |
| 74 | `EIS-0012-01|run2/0012-gpt` | hit(s1) | `persists_until` | R5 | hit | hit | issue | 直接对应 | hit | — |
| 75 | `EIS-0014-01|run1/0014-gpt` | hit(s1) | `initial_target` | R7 | hit | hit | issue | 直接对应 | hit | — |
| 76 | `EIS-0014-04|run1/0014-claude` | hit(s1) | `action_declared` | R7 | hit | hit | issue | 直接对应 | hit | — |
| 77 | `EIS-0015-01|run1/0015-gpt` | hit(s2) | `NONE` | S3 | hit | hit | issue | 蕴含更根本的原因 | hit | — |
| 78 | `EIS-0015-01|run2/0015-claude` | hit(s2) | `NONE` | S3 | hit | hit | issue | 合取项之一 | hit | — |
| 79 | `EIS-0016-01|run1/0016-gpt` | hit(s1) | `containment` | R6 | hit | hit | issue | 直接对应 | hit | — |
| 80 | `EIS-0019-01|run3/0019-gpt` | hit(s2) | `guard_distinguishable` | S5 | hit | hit | issue | 直接对应 | hit | — |
| 81 | `EIS-0019-02|run1/0019-claude` | hit(s1) | `initial_target` | R8 | hit | hit | issue | 直接对应 | hit | — |
| 82 | `EIS-0020-01|run1/0020-claude` | hit(s1) | `event_declared` | R7 | hit | hit | issue | 直接对应 | hit | — |
| 83 | `EIS-0020-02|run1/0020-gpt` | hit(s2) | `event_declared` | S2 | hit | hit | issue | 合取项之一 | hit | — |
| 84 | `EIS-0020-02|run3/0020-claude` | hit(s2) | `event_declared` | S2 | hit | hit | issue | 合取项之一 | hit | — |
| 85 | `EIS-0024-01|run1/0024-gpt` | hit(s2) | `action_declared` | S5 | hit | hit | issue | 直接对应 | hit | — |
| 86 | `EIS-0024-03|run2/0024-claude` | hit(s2) | `persists_until` | S5 | hit | hit | issue | 直接对应 | hit | — |
| 87 | `EIS-0029-02|run3/0029-claude` | hit(s1) | `guard_distinguishable` | R3 | hit | hit | issue | 直接对应 | hit | — |
| 88 | `EIS-0029-03|run1/0029-gpt` | hit(s2) | `edge_declared` | S1 | hit | hit | issue | 直接对应 | hit | — |
| 89 | `EIS-0029-03|run3/0029-gpt` | hit(s1) | `edge_declared` | R3 | hit | hit | issue | 直接对应 | hit | — |
| 90 | `EIS-0030-01|run1/0030-gpt` | hit(s2) | `state_declared` | S5 | hit | hit | issue | 直接对应 | hit | — |
| 91 | `EIS-0030-02|run1/0030-gpt` | hit(s1) | `event_consumed` | R1 | hit | miss |  |  | miss | ⛔ hit→miss |
| 92 | `EIS-0032-02|run1/0032-claude` | hit(s2) | `containment` | S1 | hit | hit | issue | 合取项之一 | hit | — |
| 93 | `EIS-0032-02|run2/0032-gpt` | hit(s1) | `containment` | R5 | hit | hit | issue | 直接对应 | hit | — |
| 94 | `EIS-0032-02|run3/0032-claude` | hit(s2) | `containment` | S1 | hit | hit | issue | 合取项之一 | hit | — |
| 95 | `EIS-0034-01|run3/0034-gpt` | hit(s1) | `containment` | R8 | hit | hit | issue | 直接对应 | hit | — |
| 96 | `EIS-0040-03|run1/0040-claude` | hit(s1) | `occupancy_after` | R4 | hit | miss |  |  | miss | ⛔ hit→miss |
| 97 | `EIS-0040-03|run2/0040-claude` | hit(s2) | `occupancy_after` | S3 | hit | miss |  |  | miss | ⛔ hit→miss |
| 98 | `EIS-0042-01|run2/0042-gpt` | hit(s2) | `occupancy_after` | S2 | hit | miss |  |  | miss | ⛔ hit→miss |
| 99 | `EIS-0044-01|run2/0044-claude` | hit(s2) | `initial_target` | S1 | hit | hit | issue | 直接对应 | hit | — |
| 100 | `EIS-0047-02|run2/0047-claude` | hit(s1) | `initial_target` | R2 | hit | hit | issue | 直接对应 | hit | — |
| 101 | `EIS-0049-02|run3/0049-gpt` | hit(s2) | `containment` | S3 | hit | hit | issue | 直接对应 | hit | — |
| 102 | `EIS-0053-01|run1/0053-claude` | hit(s2) | `initial_target` | S4 | hit | hit | issue | 直接对应 | hit | — |
| 103 | `EIS-0053-01|run3/0053-claude` | hit(s2) | `initial_target` | S4 | hit | hit | issue | 直接对应 | hit | — |
| 104 | `EIS-0053-01|run3/0053-gpt` | hit(s2) | `initial_target` | S4 | hit | hit | issue | 直接对应 | hit | — |
| 105 | `EIS-0056-02|run3/0056-gpt` | hit(s1) | `effect_declared` | R8 | hit | hit | issue | 蕴含更根本的原因 | hit | — |

## 发生变化的 9 位（论证全文）

其余各位的 `argument` 见 [positions_final.json](./positions_final.json)。

### `EIS-0010-05|run1/0010-gpt`（miss→hit，组 R5）

台账命题是合取式『AutonomousIdle 且 AutonomousActive 且 AutonomousFinal 三个自动驾驶态都不消费 Power Off，自动驾驶期间无法关机』。本格 issue [10]（ISSUE-REQ-014-015-power-off-only-on-human-driving）证明其中 AutonomousFinal 这一合取项成立（AST-REQ-015-1 terminates(AutonomousFinal, Power_Off)=False），并同时证明 Autonomous 亦然（AST-REQ-014-1=False），其 rationale 逐字给出同一根因：『模型只声明了从 HumanDriving 发出的 Power_Off 边』。这与台账指向作者源同一处遗漏——全文只有 `HumanDriving --> AutonomousFinal : Power Off` 一条 Power Off 边。

### `EIS-0010-05|run3/0010-gpt`（miss→hit，组 R5）

台账记『AutonomousIdle / AutonomousActive / AutonomousFinal 三个自动驾驶态都不消费 Power Off』。本格 issue [7]（ISSUE-PowerOffAutonomousIdleNotTerminating）、issue [8]（ISSUE-PowerOffAutonomousActiveNotTerminating）、issue [9]（ISSUE-PowerOffAutonomousFinalNotTerminating）逐一覆盖台账点名的这三个状态，对应 AST-REQ-014B-1 / AST-REQ-014C-1 / AST-REQ-014D-1 全为 False，另加 issue [6] 覆盖 Autonomous。命题与台账逐条对应，指向作者源同一处遗漏（自动驾驶侧无任何 Power Off 出边）。

### `EIS-0014-03|run2/0014-gpt`（miss→hit，组 R7）

已发布 issue [4] `ISSUE-REQ-006-entry-action`（AST-REQ-006-1，action_declared:EmergencyStopping:entry 判 False）主张 EmergencyStopping 自身未声明 entry 动作以承载 Emergency Stop。台账 EIS-0014-03 的命题是「作者源第 49 行 `Entry: Emergency Stop` 不是动作语法，于是 Emergency Stop 动作被降级成虚假子状态，结果 EmergencyStopping 既没有动作、又变成复合状态」——这是一个合取，产出证明了其中「EmergencyStopping 没有 Emergency Stop 入场动作」这一合取项为真（即动作缺失）。两者指向的是作者源同一条语句，元素同为 EmergencyStopping，缺陷事实同为 NL 第 3 句要求的 Emergency Stop 动作未被建为该状态的 entry 动作。

### `EIS-0014-04|run1/0014-gpt`（miss→hit，组 R7）

已发布 issue [5] `ISSUE-REQ-026-approaching-during-action`（AST-REQ-026-1 判 False）主张 InMotion.Approaching 未声明 during 动作、因此不能承载在 Approaching 中发送 Send 信号的义务；已发布 issue [6] `ISSUE-REQ-027-send-event-missing`（AST-REQ-027-1，event_declared:Send 判 False）进一步主张 Send 在模型中根本未被声明。台账 EIS-0014-04 说的是「Send 动作在全模型任何相位、任何迁移上都不存在」。两者指向作者源同一处（Approaching 块只写了两行描述文本、未承载 Send），元素与缺陷事实完全一致。

### `EIS-0007-03|run1/0007-claude`（hit→miss，组 S4）

台账 EIS-0007-03 主张的是 OperationalControls 整棵子树（FeedbackControl/SystemCheck/CommunicationControl）为 NL 未提及的臆造内容、无任何入边、且在同一非正交区内放了三条初始迁移。本格 2 条 issue 无一指向此处：issue [1](ISSUE-REQ-001-root-region-count) 虽因 cardinality=3 为 False 而枚举到 OperationalControls，但它明确把多出的那个判为 InitialState（『多出的 InitialState 与前三个作为区域的复合状态并列』），即把 OperationalControls 当作合法区域之一——与台账主张相反，属纪律 2 点名禁止的按相似度对齐；issue [2](ISSUE-REQ-003-005-007-activation-routing) 关于 CollisionDetection→CollisionAvoidance 的激活路径。断言表中为 False 的 AST-REQ-001-1/003-1/005-1/007-1 分别关于根区域计数与三次碰撞事件后的 CollisionAvoidance 占据，无一以 OperationalControls 或其三个子状态为对象，也无任何关于死代码入边缺失或非确定初始迁移的主张。

### `EIS-0030-02|run1/0030-gpt`（hit→miss，组 R1）

台账 EIS-0030-02 的命题是断电义务只覆盖一半作用域：作者源只有 `HumanDriving --> [*] : Power Off`，缺 Autonomous 侧的 power off 终止边，故自动驾驶激活期间无法断电。本格 6 条已发布 issue（ISSUE-front_distance_missing、ISSUE-auto_final_joint_edge_missing、ISSUE-human_steering_cmd_missing、ISSUE-brake_pressed_missing、ISSUE-auto_final_state_missing、ISSUE-auto_final_containment_missing）分别关于 front_distance 变量、auto final 状态与其包含关系、human steering cmd / brake pressed 的独立与联合事件声明，无一涉及 Power Off 的作用域。断言表里为 False 的 AST-REQ-007-1、010-1、010-2、010-4、011-1、012-1、013-1、013B-1、013B-2 同样全部落在上述对象上。唯一与断电有关的 AST-REQ-014-1 `terminates:HumanDriving:Power_Off` 结果为 True——它只检查了 HumanDriving 一侧且判为通过，按 §3.1 不承载命中，且恰恰说明本格没有去问 Autonomous 侧是否也能断电。

### `EIS-0040-03|run1/0040-claude`（hit→miss，组 R4）

台账 EIS-0040-03 指向作者源 `[*] --> AutoInitial : Enter Autonomous Mode` 这一行：复合状态 Autonomous 的初始迁移带触发事件，导致进入 Autonomous 后无任何子状态被激活。本格 3 条 issue 分别是 front_distance 变量缺失与守卫被抽象成事件（[1]）、human_steering_cmd 未独立声明（[2]）、brake_pressed 未独立声明（[3]），锚定的是 `HumanDriving --> Autonomous : front_distance > 10` 与 `Autonomous --> HumanDriving : ...` 这两行，与台账那一行不是同一条作者编辑，全文未出现 Enter Autonomous Mode、初始伪态带触发或子状态未激活的任何主张。issue [1] 引用的 AST-REQ-004b-1 `occupancy_after:HumanDriving:front_distance_10:Autonomous` 虽为 False，但本格自陈的因果是「无 front_distance 变量、无守卫化边故无法正确到达 Autonomous」，其命题是「进不了 Autonomous」，与台账「已进入 Autonomous 但内部无激活子状态」在可达性方向上相反，正落在纪律第 2 条点名禁止的按相似度对齐情形；蕴含链说不清，依 §四判 false。

### `EIS-0040-03|run2/0040-claude`（hit→miss，组 S3）

台账 EIS-0040-03 指向作者源里唯一那一行 `[*] --> AutoInitial : Enter Autonomous Mode`——复合状态 Autonomous 的初始迁移带了触发事件，导致进入 Autonomous 后无任何子状态激活。本格 3 条已发布 issue 无一触及该行：issue [1] 关于 front_distance 变量缺失与外层边 HumanDriving --> Autonomous 把数值守卫编成事件名，issue [2]/[3] 关于 human_steering_cmd 与 brake_pressed 未独立声明。`AutoInitial` 与 `Enter Autonomous Mode` 在全部 issue、rationale 与断言表中一次都未出现。断言表里为 False 的条目（AST-REQ-004-1、AST-REQ-006-1、AST-REQ-007-1、AST-REQ-008-0/1、AST-REQ-009-0/1）分别关于变量与事件声明，同样不指向初始迁移。唯一形似的是 AST-REQ-005-1（occupancy_after:HumanDriving:front_distance_10:Autonomous 为 False），但承载它的 issue [1] 明确把该 False 归因于「触发是事件而不是守卫、且无 front_distance 变量可评估比较」，并提出「声明 front_distance 并把该外层边改为带守卫的过渡」即可消除两个 False——这条修法完全不动初始迁移，其命题也不蕴含台账所述「子状态不激活」；把它对齐过去只能靠猜测模拟器按叶配置计 occupancy，蕴含链说不清，按 §四 反自利纪律判 false。AST-REQ-010-1（reaches:AutoFinal:HumanDriving）结果为 True，按 §3.1 不承载命中。另两条被结构门丢弃的排除项按 §3.1 亦不承载。

### `EIS-0042-01|run2/0042-gpt`（hit→miss，组 S2）

本格唯一一条已发布 issue [1]（ISSUE-REQ-001-root-initial-target，AST-REQ-001-1，initial_target:root:Operate = False）主张的是「根状态首次进入应直接落到 Operate，而模型落到 Off」，说的是初始迁移的**目标**；台账 EIS-0042-01 说的是同一行 `[*] --> Off : keyOff` 上的**触发**——初始伪态出边带事件为 UML 所禁、致冷启动路径不可达，且把本属关机的 keyOff 误挂到上电边。二者虽同锚一行，但缺陷事实不同，且台账本身把「上电→Off→start→Operate」视为应当可达的正确路径，即认为 Off 作为初始目标并无问题，故本格主张与台账主张不仅不等价、方向相反（§三纪律 2）。issue 全文未提触发、未提可达性、未提 keyOff 误挂。本格其余为 False 的断言只有 AST-REQ-014-2（Operate.Idle 的 keyOff 退出承载，属被证据角色制度静默的观察，且未被任何已发布 issue 引用），不承载命中。

## 被主 session 收紧掉的 5 位

| 位 | 判定组 | 裁定 |
| :-- | :-- | :-- |
| `EIS-0002-02|run2/0002-claude` | R6 判 hit（carrier=assertion） | 载体 AST-REQ-009-1/010-1 在 excluded_findings 内且无已发布 issue 引用；主臂 A 层与 X1 规则都不许它承载命中 |
| `EIS-0005-01|run1/0005-gpt` | R6 判 hit（carrier=assertion） | 载体 AST-REQ-002-1 在 excluded_findings 内且无已发布 issue 引用 |
| `EIS-0005-01|run2/0005-claude` | R6 判 hit（carrier=assertion） | 载体 AST-REQ-002-1 在 excluded_findings 内且无已发布 issue 引用 |
| `EIS-0033-02|run2/0033-gpt` | R7 判 hit（carrier=issue） | 所援引 issue 逐字对应 EIS-0033-01，且该记录在同格已计命中（6/6）；再认领 -02 属一果两记 |
| `EIS-0035-03|run1/0035-gpt` | R5 判 hit（carrier=assertion） | 载体 AST-REQ-019-2 在 excluded_findings 内且无已发布 issue 引用 |
