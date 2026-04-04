# An Efficient Remote Driving Shift Control Method of Unmanned Heavy Tracked Vehicles Based on Manned Data Mining - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟, 层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把无人重型履带车辆的远程换挡控制明确组织成上层正常/异常双状态与下层多子状态 HFSM，并给出 `ts`、`tth_g`、`tth_s` 等定时阈值和回原挡逻辑，可直接形成高质量控制状态机描述。

## 条目 1: HFSM-based remote shift supervisor for an unmanned heavy tracked vehicle
- 控制对象：无人重型履带车辆的远程驾驶换挡与异常处理监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟, 层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把远程换挡主链与故障处理链分层组织起来的车辆动力传动监督控制器，用于协调 shift timing decision、离合器、空挡、挂挡和停车处理。
- 判断：算。对象是真实无人履带车辆控制器，不是数据挖掘流程；原文给出了 HFSM 结构、状态转移条件、变量 guard 和超时回退链，完全属于本研究关注的状态机属性控制系统。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7 页，Section `Integrated shift control strategy ... based on HFSM`
> To ensure that the vehicle controller can control each shift actuator to complete the shift process successfully and improve the smoothness of the vehicle shift, this study uses a hierarchical finite state machine to design the vehicle shift control system.
>
> The upper control system state mainly divides the driving control state of a tracked vehicle into the remote driving power transmission integrated shift control state, denoted by `S4`, and the shift exception handling state, denoted by `S6`.

#### 摘录 B
- 出处：第 8 页，Section `Design of shift control state machine based on shift timing auxiliary decision`
> Referring to a driver's shift operation process, the remote driving integrated shift control state `S4` is divided into six sub-states: the on-gear control state (`S41`), the shift timing auxiliary decision state (`S42`), the clutch separation state (`S43`), the off-gear control state (`S44`), the gear shift state (`S45`), and the clutch engagement state (`S46`).
>
> `F(S41, CS41→S42)=S42 ... F(S46, CS46→S41)=S41`.

#### 摘录 C
- 出处：第 9 页，Section `Design of shift control state machine based on shift timing auxiliary decision`
> The `S42` state is an auxiliary decision state of shift timing ... the shift timing auxiliary decision model monitors the values of engine speed `ne` and throttle opening `βt` in real time. When the model determines that the shift timing is reasonable, the vehicle enters the `S43` state ...
>
> In the `S45` state ... `ts` is used to calculate the gearing duration, and `tth_g` is the gearing time threshold. When `ts ≥ tth_g`, the system determines the abnormal shift operation ... returned to the original gear.

#### 摘录 D
- 出处：第 10 页，Section `Design of shift fault handling state machine based on fixed time threshold method`
> Figure 9 depicts the schematic diagram of the shift exception handling sub-state transition process.
>
> the shift exception handling state is divided into three sub-states: a clutch separation state (`S61`), a neutral gear state (`S62`), and a braking stop state (`S63`).
>
> The time threshold of each shift sub-state and the corresponding abnormal flags and shift exception handling measures are displayed in Table 4.

### 2. 基于原文整理后的自然语言描述

The unmanned heavy tracked vehicle uses a hierarchical finite state machine to supervise remote gear shifting and abnormal-shift recovery in its power-transmission system. At the upper level, the controller separates normal remote driving shift control `S4` from shift exception handling `S6`; inside `S4`, the normal shift chain progresses through `S41 on-gear control`, `S42 shift timing auxiliary decision`, `S43 clutch separation`, `S44 off-gear/neutral control`, `S45 gear shift`, and `S46 clutch engagement`. After a remote shift command is received, the controller remains in `S42` until the auxiliary model judges the current `ne` and `βt` combination to be a reasonable shift moment, then it separates the clutch, moves through neutral, and attempts to engage the expected gear. During `S45`, the controller compares the elapsed gearing time `ts` with the threshold `tth_g`; if the target gear is not achieved before timeout, it falls back to neutral and returns to the original gear instead of continuing the failed engagement. If any sub-state exceeds its preset execution threshold or the shift becomes abnormal, control escalates into `S61`, `S62`, and `S63`, where clutch separation, neutralization, braking stop, and if necessary engine shutdown are carried out as the fault-handling chain.

### 3. 逐句溯源

1. 句子 1：The unmanned heavy tracked vehicle uses a hierarchical finite state machine to supervise remote gear shifting and abnormal-shift recovery in its power-transmission system.
   对应摘录：A
2. 句子 2：At the upper level, the controller separates normal remote driving shift control `S4` from shift exception handling `S6`; inside `S4`, the normal shift chain progresses through `S41 on-gear control`, `S42 shift timing auxiliary decision`, `S43 clutch separation`, `S44 off-gear/neutral control`, `S45 gear shift`, and `S46 clutch engagement`.
   对应摘录：A, B
3. 句子 3：After a remote shift command is received, the controller remains in `S42` until the auxiliary model judges the current `ne` and `βt` combination to be a reasonable shift moment, then it separates the clutch, moves through neutral, and attempts to engage the expected gear.
   对应摘录：B, C
4. 句子 4：During `S45`, the controller compares the elapsed gearing time `ts` with the threshold `tth_g`; if the target gear is not achieved before timeout, it falls back to neutral and returns to the original gear instead of continuing the failed engagement.
   对应摘录：C
5. 句子 5：If any sub-state exceeds its preset execution threshold or the shift becomes abnormal, control escalates into `S61`, `S62`, and `S63`, where clutch separation, neutralization, braking stop, and if necessary engine shutdown are carried out as the fault-handling chain.
   对应摘录：D
