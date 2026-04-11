# An Unmanned Aerial Carrier and Anchoring Mechanism for Transporting Companion UAVs - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把空中载机的软件架构明确组织成 `RC control / Transportation / Anchor operation` 三态 FSM，并把各状态与 MPC 位置控制、稳定悬停和锚定执行链直接接通。

## 条目 1: Three-state aerial transport-and-anchor supervisor

- 控制对象：航空航天与飞行控制领域的空中载机运输与锚定监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个负责空中载机起降、运输悬停和伴随 UAV 锚定/释放的三态监督器，外层 FSM 调度飞行控制与锚定执行机构。
- 判断：算。对象是真实空中平台控制系统；原文不仅说明有 MPC 位置控制和锚定机构，还明确写出 FSM 的三种状态、进入条件、应急回退路径以及锚定动作完成后的返回逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 14-24 行
> This paper demonstrates an unmanned aerial carrier as well as a new anchoring mechanism for connecting and transporting companion unmanned aerial vehicles (UAVs). ... A nonlinear position model predictive controller cascaded with a DJI attitude controller is implemented for the flight control. ... Real-world experiments results suggest that the transportation system is a viable approach to transport the companion UAV, and that the proposed anchoring mechanism allows for reliable operation.

#### 摘录 B

- 出处：第 5 页，Section `3.1 Software Overview`，`paper_content.txt` 第 297-316 行
> Figure 4 provides an overview of system software modules and architecture implemented on the aerial carrier for stable position flight control, map formation, and the control of the anchoring mechanism. ... For stable flight control e.g., during transportation, a position controller for the aerial carrier has been developed ... For reliable anchoring of the companion UAV, a software has been designed and implemented that allows automatic anchoring. As shown in Figure 4, all software modules are managed by a finite state machine (FSM) to accomplish the transport and anchoring tasks effectively.

#### 摘录 C

- 出处：第 5 页，Section `3.5 Finite State Machine`，`paper_content.txt` 第 415-433 行
> The behavior of the aerial platform is determined by a finite state machine (FSM) consisting of three states: `RC control` ... initial state for the aerial platform taking off, normal landing or emergency landing ... transitions to the `Transportation` state. `Transportation` ... When it reaches the hover position and hovers stably, the state switches to `Anchor operation`. In case of emergency, the state switches to `RC control` ... `Anchor operation` ... the anchor is starting to work for locking or releasing the companion UAV with a RC switch triggering. When the action is done, the FSM transitions to the `Transportation` state or it transitions to `RC control` if an emergency is triggered.

### 2. 基于原文整理后的自然语言描述

The aerial carrier is supervised by a three-state FSM that coordinates flight, transport, and anchoring rather than leaving the carrier behavior as an unstructured set of ROS services. The software architecture couples positioning, mapping, a nonlinear MPC position controller, the DJI attitude controller, and the anchoring mechanism under this FSM so that transport and docking remain part of one control chain. The initial state `RC control` covers takeoff, normal landing, and emergency landing, and after the carrier finishes takeoff and hovers stably it transitions into `Transportation`. In `Transportation`, the platform flies under RC-commanded transport behavior until it reaches a stable hover position, where it switches into `Anchor operation` to lock or release the companion UAV through the anchor mechanism. Once the anchor action is complete, the supervisor returns to `Transportation`, while any emergency in either transport or anchoring sends the platform back to `RC control` for emergency landing.

### 3. 逐句溯源

1. 句子 1：The aerial carrier is supervised by a three-state FSM that coordinates flight, transport, and anchoring rather than leaving the carrier behavior as an unstructured set of ROS services.
   对应摘录：B, C
2. 句子 2：The software architecture couples positioning, mapping, a nonlinear MPC position controller, the DJI attitude controller, and the anchoring mechanism under this FSM so that transport and docking remain part of one control chain.
   对应摘录：A, B
3. 句子 3：The initial state `RC control` covers takeoff, normal landing, and emergency landing, and after the carrier finishes takeoff and hovers stably it transitions into `Transportation`.
   对应摘录：C
4. 句子 4：In `Transportation`, the platform flies under RC-commanded transport behavior until it reaches a stable hover position, where it switches into `Anchor operation` to lock or release the companion UAV through the anchor mechanism.
   对应摘录：C
5. 句子 5：Once the anchor action is complete, the supervisor returns to `Transportation`, while any emergency in either transport or anchoring sends the platform back to `RC control` for emergency landing.
   对应摘录：C
