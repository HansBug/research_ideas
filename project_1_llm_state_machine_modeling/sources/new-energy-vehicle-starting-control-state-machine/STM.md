# Research on Starting Control Method of New-Energy Vehicle Based on State Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把新能源车起步过程拆成 `default / preload / anti-rollback / pedal / PI creep` 五个状态，并给出显式 guard、速度阈值、踏板阈值与 `0.5 s` 预加载时长，足以稳定形成双 A 样本。

## 条目 1: Five-state starting supervisor for slope launch and creep

- 控制对象：新能源汽车起步阶段的扭矩仲裁与防溜坡监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于挡位、车速、坡度、制动踏板和加速踏板状态切换 `preload / anti-rollback / pedal / creep` 的车辆起步控制器。
- 判断：算。对象是真实车辆起步控制主链，不是单独的 PI 子模块或仿真流程；原文给出了五个状态、逐条转移条件和状态内扭矩计算方式。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The method of vehicle starting control is designed, which includes five control states: default state control, torque pre-loading control, anti-rollback control, pedal control and PI (Proportion-Intergral) creep control.
>
> In terms of flat road and light slope, the vehicle travels below 3 km /h according to the driver's intention, the speed is stable at 8 km /h during the creeping control phase.

#### 摘录 B

- 出处：第 6-8 页，Section `2.4 Starting Control Strategy / 2.4.2 Conversion Criteria`
> Based on the state machine, each control state can be switched, as shown in Figure 6.
>
> If it is currently in the default mode, it will convert to preload mode when the following conditions are met: (a) shifting gear to D /R; (b) brake pedal aperture greater than 95%; (c) no accelerator pedal action; (d) the vehicle speed is lower than 0.2 km /h; (e) the motor speed is lower than 20 rpm.
>
> If it is currently in the anti-rollback mode or default mode, it will convert to pedal control mode when the following condition are met: (a) gear position is in D /R; (b) the brake pedal aperture is lower than 70%; (c) no accelerator pedal action; (d) the vehicle speed is lower than 3 km /h.
>
> If it is currently in the pedal control mode or default mode, it will convert to PI control mode when the following conditions are met: (a) gear position is in D /R; (b) the brake pedal aperture is zero; (c) the accelerator pedal aperture is zero; (d) the vehicle speed is lower than 9 km /h.

#### 摘录 C

- 出处：第 8-10 页，Section `2.4.3 Torque Calculation`
> The preload torque of the drive motor is 0.5 N·m and returns to zero after 0.5 s.
>
> The anti-rollback torque T1 is determined according to Formula (9).
>
> At this state, the vehicle can launch smoothly without rollback at the stage of the pedal control according to the calibration parameters.
>
> In PI control mode, the torque T5 is determined by Formula (13).
>
> each time the creep phase is entered, the I-value will be reset to depress overshoot, and the integral term will be frozen when the slope is steep.

### 2. 基于原文整理后的自然语言描述

The new-energy vehicle starting controller is activated when the vehicle is in `D/R`, the speed stays at or below `8 km/h`, and the driver is not requesting acceleration, after which the FSM begins from the `default` state and arbitrates the launch torque. From `default`, the controller enters `preload` when the brake aperture is above `95%`, the vehicle speed is below `0.2 km/h`, and the motor speed is below `20 rpm`; this state injects a `0.5 N·m` preload torque for `0.5 s` and then returns to zero. If the vehicle is on a grade and the brake is still above `70%`, the supervisor instead uses `anti-rollback` to hold the car, and once the brake aperture drops below `70%` with speed still below `3 km/h`, it transfers to `pedal control`, where the output torque depends on brake aperture and actual speed so the vehicle can launch without rollback. When the brake and accelerator are both released and the speed is below `9 km/h`, the FSM moves into `PI creep`, which resets the integral term at every entry, freezes it on steep slopes, and regulates the target creeping speed around `8 km/h`. The controller returns to `default` when the brake is reapplied or the speed exceeds `9 km/h`, and the whole starting mode exits when the gear leaves `D/R`, the vehicle speed exceeds `10 km/h`, or the accelerator torque request dominates the starting request.

### 3. 逐句溯源

1. 句子 1：The new-energy vehicle starting controller is activated when the vehicle is in `D/R`, the speed stays at or below `8 km/h`, and the driver is not requesting acceleration, after which the FSM begins from the `default` state and arbitrates the launch torque.
   对应摘录：A, B
2. 句子 2：From `default`, the controller enters `preload` when the brake aperture is above `95%`, the vehicle speed is below `0.2 km/h`, and the motor speed is below `20 rpm`; this state injects a `0.5 N·m` preload torque for `0.5 s` and then returns to zero.
   对应摘录：B, C
3. 句子 3：If the vehicle is on a grade and the brake is still above `70%`, the supervisor instead uses `anti-rollback` to hold the car, and once the brake aperture drops below `70%` with speed still below `3 km/h`, it transfers to `pedal control`, where the output torque depends on brake aperture and actual speed so the vehicle can launch without rollback.
   对应摘录：B, C
4. 句子 4：When the brake and accelerator are both released and the speed is below `9 km/h`, the FSM moves into `PI creep`, which resets the integral term at every entry, freezes it on steep slopes, and regulates the target creeping speed around `8 km/h`.
   对应摘录：A, B, C
5. 句子 5：The controller returns to `default` when the brake is reapplied or the speed exceeds `9 km/h`, and the whole starting mode exits when the gear leaves `D/R`, the vehicle speed exceeds `10 km/h`, or the accelerator torque request dominates the starting request.
   对应摘录：B
