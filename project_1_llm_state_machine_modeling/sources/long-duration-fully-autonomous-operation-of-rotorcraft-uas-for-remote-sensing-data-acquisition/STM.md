# Long-Duration Fully Autonomous Operation of Rotorcraft UAS for Remote-Sensing Data Acquisition - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把长时自主旋翼无人机的 autonomy engine 明确写成 master/slave 层次状态机，并给出了 `takeoff / mission / landing / emergency landing` 主状态以及起飞前电机检查、返航、视觉搜索和原地紧急降落等具体控制链。

## 条目 1: Master-and-Autopilot Mission Cycle for Autonomous Rotorcraft UAS
- 控制对象：长时自主旋翼无人机的数据采集与回充任务控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个真实四旋翼平台的高层任务控制器，用 master state machine 调度 `takeoff / mission / landing / emergency landing` 四类 autopilot，并在低电量、着陆点丢失或电机异常时切换到不同回退路径。
- 判断：算。对象是长期户外自主运行的真实 UAS 与充电站系统，不是纯方法论文；原文不仅明确给出层次状态机，还把主状态、子 autopilot 行为、起飞前检查、视觉着陆搜索和紧急降落条件都写到了可直接复原控制链的程度。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页 Abstract；第 10 页 Section 3.3 `Mission Architecture`
> We propose a fully autonomous rotorcraft UAS that is capable of performing repeated flights for long-term observation missions without any human intervention.
>
> High-level autonomous decision making is implemented as a hierarchy of master and slave state machines.
>
> Before each take-off, the system initializes the on-board state estimator and passes a series of pre-flight checks that include testing for an adequate battery voltage level and motor nominal performance.

#### 摘录 B
- 出处：第 20-21 页 Section 7.2 `Autonomy Engine` / Section 7.3 `Takeoff Autopilot`
> The master state machine coordinates calls to the phase-specific autopilots.
>
> In the takeoff, mission, landing and emergency landing states the master state machine activates the appropriate autopilot and waits for it to complete.
>
> The master can also abort each autopilot in order to execute robust behaviors for cases like low battery charge in flight or abnormal motor performance before takeoff.
>
> Ten attempts to pass this check are allowed before the takeoff is aborted.

#### 摘录 C
- 出处：第 21-23 页 Section 7.5 `Landing Autopilot` / Section 7.6 `Emergency Lander`
> The first action is to check if the landing pad is visible in the downfacing navigation camera image.
>
> If not, the UAS executes the spiral grid search trajectory until the landing bundle becomes visible.
>
> The vehicle then performs a constant velocity descent until touchdown is detected based on 0.3 m height and 0.1 m/s velocity thresholds.
>
> The emergency lander brings the UAS to a soft touchdown at its current location and is triggered in response to a critically low battery voltage.

### 2. 基于原文整理后的自然语言描述

The rotorcraft autonomy engine is organized as a hierarchical controller in which a master state machine selects one of four phase-specific autopilots: `takeoff`, `mission`, `landing`, or `emergency landing`. The `takeoff` autopilot first validates battery and motor health, reinitializes the state estimator after charging, memorizes the launch location, and then commands a velocity-controlled climb to a safe hover altitude; takeoff is aborted if the motor nominal-performance check cannot be passed within ten attempts. Once airborne, the `mission` autopilot flies the waypoint-and-hover data acquisition route until the plan finishes or a low-battery event requests return to the charging pad. The `landing` autopilot checks whether the AprilTag bundle on the charging station is visible, falls back to a spiral grid search if it is not, then aligns over the pad and performs a constant-velocity descent until touchdown is detected using combined height and vertical-velocity thresholds. If battery charge becomes critically low during flight, the master aborts the nominal task and switches to the `emergency landing` autopilot, which performs an in-place soft touchdown instead of attempting return-to-home.

### 3. 逐句溯源

1. 句子 1：The rotorcraft autonomy engine is organized as a hierarchical controller in which a master state machine selects one of four phase-specific autopilots: `takeoff`, `mission`, `landing`, or `emergency landing`.
   对应摘录：A, B
2. 句子 2：The `takeoff` autopilot first validates battery and motor health, reinitializes the state estimator after charging, memorizes the launch location, and then commands a velocity-controlled climb to a safe hover altitude; takeoff is aborted if the motor nominal-performance check cannot be passed within ten attempts.
   对应摘录：A, B
3. 句子 3：Once airborne, the `mission` autopilot flies the waypoint-and-hover data acquisition route until the plan finishes or a low-battery event requests return to the charging pad.
   对应摘录：B
4. 句子 4：The `landing` autopilot checks whether the AprilTag bundle on the charging station is visible, falls back to a spiral grid search if it is not, then aligns over the pad and performs a constant-velocity descent until touchdown is detected using combined height and vertical-velocity thresholds.
   对应摘录：C
5. 句子 5：If battery charge becomes critically low during flight, the master aborts the nominal task and switches to the `emergency landing` autopilot, which performs an in-place soft touchdown instead of attempting return-to-home.
   对应摘录：B, C
