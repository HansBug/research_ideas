# Model-based control for exoskeletons with series elastic actuators evaluated on sit-to-stand movements - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `sit / stand / standing-up / sitting-down` 四主状态、`standing-up` 内部独立 assistance FSM、显式 event table，以及 `0.11 s` 与 `0.3 s` 的局部时序，可直接作为接触情境驱动的外骨骼监督控制样本。

## 条目 1: Contact-aware sit-to-stand supervisor with nested assistance FSM
- 控制对象：用于 `MIRAD` sit-to-stand 外骨骼的中层监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据 stool 接触情境和关节运动事件，在 `sit`、`standing-up`、`stand`、`sitting-down` 之间切换，并在起立过程中嵌套独立 assistance 子状态机的外骨骼监督控制器。
- 判断：算。对象是真实 sit-to-stand 外骨骼控制器，不是实验流程；原文明确给出了主状态、嵌套 assistance 逻辑、事件触发、守卫条件、异常入口和局部时间参数，能够恢复完整控制主链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 11 页，Section `Modelling Step 2: Determine contact situations`
> The two different contact situations are directly related to two discrete states, the sit state and the stand state, in the FSM of the mid-level controller in Fig. 8. The sit state and stand state are accompanied by two additional states for transition between the contact states: a standing-up state and a sitting-down state. ... A separate FSM in the standing-up state allows to independently start and stop the assistance. The transition between states is triggered by events, as shown by the arrows in Fig. 8.

#### 摘录 B
- 出处：第 12 页，Figure 8 caption
> The Finite State Machine of the sit-to-stand motion has four main states: sit, stand, standing-up and sitting-down. ... In the sit state only the inertial and Coriolis compensation of the exoskeleton is active. In the standing-up state, the gravity compensation is gradually turned on before the seat-off. ... When the event to start the assistance is detected, the assistance is switched to active. In the stand state the exoskeleton is completely compensated. In the sitting-down state, gravity compensation is gradually reduced to zero until the person sits back on the stool.

#### 摘录 C
- 出处：第 12 页，Table 3 `High-level controller: event detection/prediction`
> e_start_sit_to_stand qhip > 14.3 deg/s ... e_seatoff_detected ... e_detect_start_assistance tso - tcurrent < 0.11 s or ANN [54] ... e_assistance_done τas == 0 ... e_start_stand_to_sit qknee < -28.6 deg and q̇knee < -17.2 deg/s ... e_seatdown_detected qknee < -68.8 deg ... e_finish_stand_to_sit qknee < -77.3 deg and |q̇knee| < 5.7 deg/s ... e_error any encoder, controller or prediction error

#### 摘录 D
- 出处：第 12-13 页，Section `Modelling Step 4: Model the exoskeleton for each situation`
> The exoskeleton gravity compensation gain βg should not be turned on and off instantaneously. ... the reaction force on the stool decreases almost linearly, starting approximately 0.3 s before seat-off until seat-off. ... the exoskeleton gravity compensation gain βg needs to increase linearly from zero to one in approximately 0.3 s. This linearly increase of βg is implemented in the standing-up state in Fig. 8.

### 2. 基于原文整理后的自然语言描述

The sit-to-stand exoskeleton uses a mid-level hierarchical supervisor whose four main states are `sit`, `standing-up`, `stand`, and `sitting-down`, with a separate nested FSM inside `standing-up` to gate when assistance is turned on and off. State transitions are driven by event guards derived from joint kinematics and contact prediction, including `e_start_sit_to_stand` from hip angular velocity, predicted or detected seat-off, assistance-start detection, stand-to-sit detection, seat-down detection, completion events, and a global `e_error` branch. In `sit`, only inertial and Coriolis compensation is active, while in `standing-up` the controller gradually turns on gravity compensation and activates assistance once the predicted seat-off lead time falls below `0.11 s` or the ANN-based detector fires. The contact-model switch is explicitly time-shaped rather than instantaneous: the gain `βg` ramps from `0` to `1` over roughly `0.3 s` before seat-off according to the predicted time remaining until seat-off. After seat-off the machine reaches fully compensated `stand`, and during `sitting-down` the controller gradually reduces gravity compensation to zero until the stool contact is re-established.

### 3. 逐句溯源

1. 句子 1：The sit-to-stand exoskeleton uses a mid-level hierarchical supervisor whose four main states are `sit`, `standing-up`, `stand`, and `sitting-down`, with a separate nested FSM inside `standing-up` to gate when assistance is turned on and off.
   对应摘录：A, B
2. 句子 2：State transitions are driven by event guards derived from joint kinematics and contact prediction, including `e_start_sit_to_stand` from hip angular velocity, predicted or detected seat-off, assistance-start detection, stand-to-sit detection, seat-down detection, completion events, and a global `e_error` branch.
   对应摘录：A, C
3. 句子 3：In `sit`, only inertial and Coriolis compensation is active, while in `standing-up` the controller gradually turns on gravity compensation and activates assistance once the predicted seat-off lead time falls below `0.11 s` or the ANN-based detector fires.
   对应摘录：B, C
4. 句子 4：The contact-model switch is explicitly time-shaped rather than instantaneous: the gain `βg` ramps from `0` to `1` over roughly `0.3 s` before seat-off according to the predicted time remaining until seat-off.
   对应摘录：D
5. 句子 5：After seat-off the machine reaches fully compensated `stand`, and during `sitting-down` the controller gradually reduces gravity compensation to zero until the stool contact is re-established.
   对应摘录：B
