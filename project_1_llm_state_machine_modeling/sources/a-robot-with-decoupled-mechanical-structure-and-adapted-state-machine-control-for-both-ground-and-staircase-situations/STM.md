# A Robot with Decoupled Mechanical Structure and Adapted State Machine Control for Both Ground and Staircase Situations - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 stair-climbing robot 的状态机、传感器输入、`SC1-SC7` 转移条件和上楼操作步骤都写得很清楚，可直接作为机器人顺序控制样本。

## 条目 1: Stair-climbing mode manager for the decoupled delivery robot
- 控制对象：解耦机械结构送货机器人的楼梯切换与攀爬控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个 stair-climbing robot 的高层状态机，用于根据轮组、支腿和台阶距离传感器，在地面模式、姿态调整和不同 climbing cases 之间切换。
- 判断：算。对象是实际 stair-climbing delivery robot 的运动控制器；原文明确给出了 sensor set、`SC1-SC7` 守卫条件、上楼状态机和返回 ground mode 的逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 8-9 页，Section 4 `State Machine for the Robot`
> Based on the basic actions designed in Section 3, a state machine is further proposed to manage the robot's movement in this section.
>
> Each state in the state machine can be defined as a class with a property (the data of the corresponding sensors) and method (basic actions).
>
> Laser ranging sensors ... are used as the trigger conditions for the stair-climbing actions.

#### 摘录 B
- 出处：第 9-10 页，Table 4 `The conditions of the transition of the states`
> SC1 No stairs detected  Mode on the ground
>
> SC2 Stairs and ...  Posture adjustment: case 1
>
> SC4 d1L < Δdup and d1R < Δdup  Stair-climbing: case I
>
> SC5 ... Stair-climbing: case II
>
> SC6 d2L < Δdup and d2R < Δdup  Stair-climbing: case IV
>
> SC7 SC4 || SC5 || SC6  Stair-climbing: case III

#### 摘录 C
- 出处：第 10 页，Section 4.2 `State Machine Design`
> When the robot gets the start signal, it firstly operates in the ground mode.
>
> When the SC2 is met, the state machine goes to Case 1; thus, the robot adjusts its pose.
>
> Once SC7 is triggered, the state machine goes to Case III and begins to climb the stair.
>
> Specifically, after Case I is finished, SC3 is used to check the posture of the robot.
>
> If the state machine is in Case IV ... Once SC1 is triggered, the state machine turns to ground mode.

### 2. 基于原文整理后的自然语言描述

The stair-climbing robot is governed by a finite state machine whose states are parameterized by sensor readings from wheel encoders, leg encoders, and laser range sensors placed near the front wheels, wheel-legs, and robot ends. At startup the controller remains in `ground mode`, where ordinary path planning and obstacle avoidance are enabled, and it only leaves this mode when stair-detection condition `SC2` becomes true. Once `SC2` is satisfied, the machine enters `Case 1` for posture adjustment so that the front wheels approach the step and the tetrapod can land in preparation for climbing. When one of the climb-trigger conditions in `SC4 / SC5 / SC6` holds, `SC7` routes execution into `Case III`, after which the controller selects `Case I`, `Case II`, or `Case IV` according to the measured front-wheel and wheel-leg distances and reuses `SC3` to decide when posture correction is needed. After the robot reaches the final stage and `SC1` indicates that no stair remains, the controller returns to `ground mode`, completing the stair-climbing sequence and preventing shutdown while the robot is still on a step.

### 3. 逐句溯源

1. 句子 1：The stair-climbing robot is governed by a finite state machine whose states are parameterized by sensor readings from wheel encoders, leg encoders, and laser range sensors placed near the front wheels, wheel-legs, and robot ends.
   对应摘录：A
2. 句子 2：At startup the controller remains in `ground mode`, where ordinary path planning and obstacle avoidance are enabled, and it only leaves this mode when stair-detection condition `SC2` becomes true.
   对应摘录：B, C
3. 句子 3：Once `SC2` is satisfied, the machine enters `Case 1` for posture adjustment so that the front wheels approach the step and the tetrapod can land in preparation for climbing.
   对应摘录：B, C
4. 句子 4：When one of the climb-trigger conditions in `SC4 / SC5 / SC6` holds, `SC7` routes execution into `Case III`, after which the controller selects `Case I`, `Case II`, or `Case IV` according to the measured front-wheel and wheel-leg distances and reuses `SC3` to decide when posture correction is needed.
   对应摘录：B, C
5. 句子 5：After the robot reaches the final stage and `SC1` indicates that no stair remains, the controller returns to `ground mode`, completing the stair-climbing sequence and preventing shutdown while the robot is still on a step.
   对应摘录：B, C
