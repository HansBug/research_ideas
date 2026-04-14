# VIEshunt: towards a ventricular intelligent and electromechanical shunt for hydrocephalus therapy - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `upright / undefined / supine` 三状态智能分流器 `FSM`、姿态角区间、predefined-time 转移和 `pressure / flow` 双模式输出，可直接作为高质量医疗设备监督控制样本。

## 条目 1: Posture-aware smart-shunt supervisor for VIEshunt
- 控制对象：`VIEshunt` 智能脑脊液分流器的姿态感知高层监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据患者躯干姿态在 `upright / undefined / supine` 三个模式之间切换，并分别输出 `ICP` 或 `CSF` 流量参考值的智能分流器监督控制器。
- 判断：算。对象是真实植入式医疗控制装置，不是实验流程；原文明确给出状态集合、姿态 guard、预设驻留时间、控制模式切换以及各状态输出参考值，能够恢复为完整离散控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section `Controller design`
> Here, a finite state machine (FSM) is used to switch between pressure-based and flow-based control. In pressure-based control mode ... a 30 s averaging window is applied to ICPmeas ... The inner PI controller ... apply U ... at a rate of 1 Hz.

#### 摘录 B
- 出处：第 4 页，Section `Controller design`
> The supine and upright position refer to torso inclination angles of 0 ± 10◦ and 90 ± 10◦ ... If the measured torso inclination angles ... leave the range that corresponds to the current state ... for a predefined time, then the respective up or down input ... causes a state transition.

#### 摘录 C
- 出处：第 4 页，Figure 2 / Figure 3
> State: upright / Mode: pressure control / Pressure reference: ICP upright
>
> State: undefined / Mode: flow control / Flow reference: CSF baseline
>
> State: supine / Mode: pressure control / Pressure reference: ICP supine

#### 摘录 D
- 出处：第 8 页，Section `In vitro testing`
> Using the torso inclination as an input, the FSM detected the posture changes and adjusted its current state ... In both upright and supine positions, the ICP could be controlled to ... —3 mmHg (upright) and 12 mmHg (supine) ... In the undefined posture state ... the shunt controller successfully regulated the CSF drainage rate to ... 100 µL/min.

### 2. 基于原文整理后的自然语言描述

The VIEshunt smart shunt is supervised by a three-state posture-aware FSM with `upright`, `undefined`, and `supine` states driven by the patient torso inclination measured by the integrated `IMU`. The machine uses explicit inclination guards, treating `0 ± 10°` as `supine`, `90 ± 10°` as `upright`, and all intermediate postures as `undefined`, and it only fires `up` or `down` transitions after the current posture band has been left for a predefined time. In `upright` and `supine`, the FSM places the shunt in pressure-control mode, where a posture-specific `ICPref` is compared against a `30 s` averaged `ICPmeas` and the outer `PI` loop computes the drainage reference for the inner `1 Hz` flow controller. In `undefined`, the pressure loop is deactivated and the state machine directly outputs a baseline `CSF` drainage reference so the pump regulates flow rather than chasing a pressure target during walking or intermediate postures. The reported test bench results show that the supervisor tracks posture changes and automatically switches the reference set to `-3 mmHg`, `12 mmHg`, or `100 µL/min` according to the active state.

### 3. 逐句溯源

1. 句子 1：The VIEshunt smart shunt is supervised by a three-state posture-aware FSM with `upright`, `undefined`, and `supine` states driven by the patient torso inclination measured by the integrated `IMU`.
   对应摘录：B, C
2. 句子 2：The machine uses explicit inclination guards, treating `0 ± 10°` as `supine`, `90 ± 10°` as `upright`, and all intermediate postures as `undefined`, and it only fires `up` or `down` transitions after the current posture band has been left for a predefined time.
   对应摘录：B
3. 句子 3：In `upright` and `supine`, the FSM places the shunt in pressure-control mode, where a posture-specific `ICPref` is compared against a `30 s` averaged `ICPmeas` and the outer `PI` loop computes the drainage reference for the inner `1 Hz` flow controller.
   对应摘录：A, C
4. 句子 4：In `undefined`, the pressure loop is deactivated and the state machine directly outputs a baseline `CSF` drainage reference so the pump regulates flow rather than chasing a pressure target during walking or intermediate postures.
   对应摘录：A, B, C
5. 句子 5：The reported test bench results show that the supervisor tracks posture changes and automatically switches the reference set to `-3 mmHg`, `12 mmHg`, or `100 µL/min` according to the active state.
   对应摘录：D
