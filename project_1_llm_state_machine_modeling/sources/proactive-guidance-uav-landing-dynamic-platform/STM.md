# Proactive Guidance for Accurate UAV Landing on a Dynamic Platform: A Visual–Inertial Approach - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把动态平台降落 supervisor 明确写成四阶段 FSM，并给出视觉接管域、回退条件和 `<5 cm` shutdown 触发，可直接作为高质量降落控制样本入账。

## 条目 1: Dynamic-platform landing supervisor for a quadrotor UAV
- 控制对象：四旋翼 UAV 面向动态平台回收的高层自主降落监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向动态 UGV/船载平台回收任务的 UAV landing FSM，用于协调 GPS 跟随、视觉接管、无地效接近和最终关机着陆。
- 判断：算。对象是真实 UAV 着陆控制器，不是视觉流程；原文给出了阶段状态、空间 guard、回退条件和关机条件，能够恢复成完整的高层控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> In this study ... a finite state machine is designed to track and control the landing process, as shown in Figure 2.
>
> This state machine includes four stages, which are Stage 1—GPS following, Stage 2—vision position following, Stage 3—ground-effect free trajectory, and Stage 4—shutdown.

#### 摘录 B
- 出处：第 7-8 页，Section 2.3 `Finite State Machine`
> In this first stage, the UAV is commanded to follow the landing platform at a pre-programmed distance and height difference ... Whenever the positioning estimation module starts to provide a reasonable reading of the position, it triggers the state machine to switch to the next stage.
>
> The goal of this stage is to ensure the stability of position controlling and to wait for the landing platform to be ready for approaching.

#### 摘录 C
- 出处：第 8 页，Section 2.3.2 `Second Stage—Vision Position Following`
> When the position difference between the landing platform and the UAV is in the desired domain, the stage then proceeds to the following motion.
>
> Note that the desired domain is defined as a sphere with a radius of 0.1 m. The center of this sphere is 1.1 m behind the landing pad in the horizontal direction and 0.7 m above.

#### 摘录 D
- 出处：第 8-9 页，Section 2.3.3-2.3.4
> If any of these criteria are out of bounds, the state machine immediately switches back to the previous stage and rapidly separates the UAV from the landing platform to maintain a safe distance.
>
> When the UAV moves toward the landing platform within a reasonable distance (<5 cm in this study) above the landing pad, the FSM commands the UAV to drastically reduce the throttles of the motors until the motors are all shut down.

### 2. 基于原文整理后的自然语言描述

The quadrotor landing controller is organized as a four-stage finite state machine that supervises recovery onto a moving platform. It begins in `GPS following`, where the UAV tracks the platform at a pre-programmed offset until the visual-inertial localization pipeline provides a reliable position estimate, then switches to `vision position following` for non-GPS relative control. When the relative pose enters the desired domain, defined as a sphere of radius `0.1 m` centered `1.1 m` behind and `0.7 m` above the landing pad, the supervisor advances to `ground-effect free trajectory following` to execute the smooth final approach. During this approach phase, any excessive trajectory divergence, insufficient remaining altitude, or overshoot with respect to the landing platform immediately pushes the controller back to the previous stage so that safe separation is restored. Once the UAV reaches the landing position and is within `5 cm` above the pad, the FSM enters `shutdown` and rapidly cuts motor throttle to complete the landing on the moving platform.

### 3. 逐句溯源

1. 句子 1：The quadrotor landing controller is organized as a four-stage finite state machine that supervises recovery onto a moving platform.
   对应摘录：A
2. 句子 2：It begins in `GPS following`, where the UAV tracks the platform at a pre-programmed offset until the visual-inertial localization pipeline provides a reliable position estimate, then switches to `vision position following` for non-GPS relative control.
   对应摘录：A, B
3. 句子 3：When the relative pose enters the desired domain, defined as a sphere of radius `0.1 m` centered `1.1 m` behind and `0.7 m` above the landing pad, the supervisor advances to `ground-effect free trajectory following` to execute the smooth final approach.
   对应摘录：C
4. 句子 4：During this approach phase, any excessive trajectory divergence, insufficient remaining altitude, or overshoot with respect to the landing platform immediately pushes the controller back to the previous stage so that safe separation is restored.
   对应摘录：D
5. 句子 5：Once the UAV reaches the landing position and is within `5 cm` above the pad, the FSM enters `shutdown` and rapidly cuts motor throttle to complete the landing on the moving platform.
   对应摘录：D
