# A Multi-Sensor Fusion Parking Barrier System with Lightweight Vision on Edge - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅写明了 `dist < 80 cm`、`tilt > 25°`、collision fallback 和 `Empty 5 s / Occ 10 s` 轮询，还在流程图中明确给出五个 parking-space state，原文与提取文本都足够支撑双 A。

## 条目 1: Infrared-Vision-Inertial Parking Barrier Supervisor
- 控制对象：智慧停车与车位管理领域的边缘侧停车位状态判定与上报控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个停车道闸边缘节点的多传感器状态机控制器，用红外触发视觉确认，并在碰撞或姿态异常下切到保守占位或异常状态。
- 判断：算。对象是真实停车控制节点，不是单纯识别算法；原文明确给出了触发阈值、状态集合、报警/睡眠策略和云端 state consistency 机制。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> At the decision level, an asymmetric infrared-vision-inertial fusion state machine is designed.
>
> single-frame inference latency is approximately `600-850 ms` ... meeting the polling requirements of `5 s` when idle and `10 s` when occupied.

#### 摘录 B
- 出处：第 4 页，Section 3.3
> Visual recognition is awakened when the infrared measured distance is less than `80 cm`.
>
> If infrared is triggered but visual confidence is insufficient and MPU6050 detects an impact, a conservative “collision-induced parking” decision is made.
>
> When the tilt angle exceeds `25°`, an abnormal tilt event is directly reported.

#### 摘录 C
- 出处：第 5 页，Fig. 3
> `State: OCCUPIED - Collision Matched`
>
> `State: ANOMALY - Other Object`
>
> `State: OCCUPIED - Normal Parking`
>
> `State: EMPTY - Normal Idle`
>
> `State: ANOMALY - Device Tilted`

#### 摘录 D
- 出处：第 5 页，Section 3.4 / 第 8 页，Section 5.5
> The cloud backend adopts an idempotent state-machine update strategy for repeated reports and prioritizes newer records with higher confidence.
>
> the system adopts a combined “event-triggered + periodic verification” strategy: detection runs every `5 s` in idle-space states and every `10 s` in occupied-space states.

### 2. 基于原文整理后的自然语言描述

The parking-barrier controller is an edge-side extended state machine that uses cheap infrared sensing as a trigger, lightweight vision as confirmation, and inertial sensing as an anomaly fallback. When the infrared distance falls below `80 cm`, the node wakes the camera and runs YOLO; a confident vehicle detection drives the space into `OCCUPIED - Normal Parking`. If infrared is triggered but visual confidence is insufficient, the controller checks inertial impact information and either conservatively assigns `OCCUPIED - Collision Matched` or classifies the scene as `ANOMALY - Other Object`. If no infrared trigger is present, the controller still checks tilt and directly reports `ANOMALY - Device Tilted` once the MPU tilt angle exceeds `25°`; otherwise it remains in `EMPTY - Normal Idle`. After a state change, heartbeat, or warning trigger, the node builds and sends a LoRa payload, and then enters the configured sleep schedule of `5 s` in empty mode or `10 s` in occupied mode, while the cloud side reconciles repeated reports through an idempotent state-update rule.

### 3. 逐句溯源

1. 句子 1：The parking-barrier controller is an edge-side extended state machine that uses cheap infrared sensing as a trigger, lightweight vision as confirmation, and inertial sensing as an anomaly fallback.
   对应摘录：A, B
2. 句子 2：When the infrared distance falls below `80 cm`, the node wakes the camera and runs YOLO; a confident vehicle detection drives the space into `OCCUPIED - Normal Parking`.
   对应摘录：B, C
3. 句子 3：If infrared is triggered but visual confidence is insufficient, the controller checks inertial impact information and either conservatively assigns `OCCUPIED - Collision Matched` or classifies the scene as `ANOMALY - Other Object`.
   对应摘录：B, C
4. 句子 4：If no infrared trigger is present, the controller still checks tilt and directly reports `ANOMALY - Device Tilted` once the MPU tilt angle exceeds `25°`; otherwise it remains in `EMPTY - Normal Idle`.
   对应摘录：B, C
5. 句子 5：After a state change, heartbeat, or warning trigger, the node builds and sends a LoRa payload, and then enters the configured sleep schedule of `5 s` in empty mode or `10 s` in occupied mode, while the cloud side reconciles repeated reports through an idempotent state-update rule.
   对应摘录：A, D
