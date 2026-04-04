# User-centered design and development of TWIN-Acta: A novel control suite of the TWIN lower limb exoskeleton for the rehabilitation of persons post-stroke - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 `state classifier -> FSM -> torque control unit` 的层次链、`10 cm` aligned-feet 阈值、可配置 transition time，以及 support/swing 相位下的 joint-specific assistive torque，足以直接作为 `HSM + T1` 样本。

## 条目 1: Inter-feet-distance gait-phase supervisor for the TWIN-Acta exoskeleton
- 控制对象：TWIN lower limb exoskeleton 的 gait-phase assist-as-needed controller
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 post-stroke 下肢外骨骼的层次 gait-phase 控制器，用 encoders 提取 inter-feet distance、由 background state classifier 判定实时 gait phase，再由 `FSM` 与 torque unit 为 support leg / swing leg 分配 hip、knee 与 trunk assistance。
- 判断：算。对象是真实 lower limb exoskeleton 控制套件；原文直接给出 phase classifier、阈值、transition time、assistive torque 构成和 `FSM` 架构，而不是单纯 rehabilitation protocol。

### 1. 原文摘录

#### 摘录 A
- 出处：第 8 页，Section `Computing the gait phases`，行 664-683
> TWIN-Acta identifies gait phases thanks to the encoders integrated into the structure of the exoskeleton, without relying on specific external sensors. In particular, the gait phases are determined by the detection of the inter-feet distance in the sagittal plane. Three possible conditions are thus possible: right foot forward, aligned feet, left foot forward.
>
> The various phases of the walking cycle are handled by a Finite State Machine (FSM), which generates the signals to be sent to the active joints to provide the assistive torque. ... a “state classifier” continuously runs in the background during movements and identifies the kinematic status of the exoskeleton. The FSM, therefore, transmits the torque amplitude to be delivered to the various joints to a torque control unit ...

#### 摘录 B
- 出处：第 9 页，Section `Computing the gait phases`，行 723-748
> TWIN-Acta classifies which foot has advanced the other by a certain distance, named the relative foot distance threshold. This parameter allows the identification of the condition of aligned feet, which we identified when the feet are displaced `10 cm` or less along the sagittal plane.
>
> We introduced the transition time parameter, which indicates the time taken by the user to move their weight from one leg to the other. Conveniently, this time can be configured, based on the user’s walking speed. Once this transition time has elapsed, it is possible to assume that the foot in the rear position is that belonging to the previously supporting leg ... becoming the swinging leg.

#### 摘录 C
- 出处：第 9 页，Section `The assist-as-needed control of TWIN-Acta`，行 751-788
> Each joint provides a different contribution, i.e., an assistive torque, for each phase of the walk. ... a single joint can deliver an assistive torque to accomplish more than one function, such as the joint at the hip, which is used to extend/flex the hip to perform the walk, but also to maintain the upper body of the patient in an upright position both during quiet standing and walking.
>
> These issues were addressed by providing specific assistance throughout the entire gait cycle ... in particular:
> `tKNEE,ext`: knee extension of the supporting leg;
> `tHIP,ext`: hip extension of the supporting leg;
> `tTRUNK`: trunk extension during the support phase;
> `tHIP,flex`: hip flexion of the swinging leg;
> `tKNEE,flex`: knee flexion of the swinging leg;

#### 摘录 D
- 出处：第 10-11 页，Figure `4` 与 Figure `5`，行 798-844
> Gait cycle phases and the timing profiles of the assistance provided at articular joints at T1.4. `tHIP,flex` and `tKNEE,flex` are the assistive torque ... during the toe-off phase of the non-paretic leg; `tTRUNK` is the pelvic tilt dumping during stance phase; `tKNEE,ext` provides stabilization of the knee joint of the support leg; `tHIP,ext` helps the extension of the paretic leg during stance phase.
>
> Figure 5 | Architecture of TWIN-Acta. Following parameters configuration (`c`), the FSM identifies the state of the TWIN exoskeleton `[s = m(q)]` ... recognizes the state of the plegic leg among the four possible ... and provides the reference torque which is a function of time, exoskeleton state, position, and configuration parameters `[t_ref(t,s,q,c)]`. The torque control unit provides the assistance ... to TWIN joints.

### 2. 基于原文整理后的自然语言描述

TWIN-Acta is structured as a hierarchical gait-phase controller in which encoders first measure inter-feet distance in the sagittal plane, a continuously running state classifier converts that kinematic relation into the real-time gait phase, and an FSM then routes assistive torques to the exoskeleton joints through a torque control unit. The phase detector distinguishes `right foot forward`, `aligned feet`, and `left foot forward`, defines `aligned feet` as an inter-feet displacement of at most `10 cm`, and introduces a configurable `transition time` so the controller delays the support-to-swing handoff until body weight has plausibly shifted to the new supporting leg. On top of that phase logic, the controller distributes joint-specific assistance across the gait cycle, combining `tKNEE,ext` and `tHIP,ext` for the supporting leg with `tTRUNK` for upright posture and `tHIP,flex / tKNEE,flex` for the swinging leg. The timing profiles in `T1.4` make these torques phase-local rather than global background compensation: hip and knee flexion assistance are tied to toe-off, trunk assistance is active during stance, and knee stabilization plus hip extension are applied while the paretic leg supports the body. At the architectural level, the FSM recognizes one of four plegic-leg states and outputs a reference torque function `t_ref(t,s,q,c)`, so the system preserves both a discrete gait-state backbone and a parameterized assist-as-needed control surface.

### 3. 逐句溯源

1. 句子 1：TWIN-Acta is structured as a hierarchical gait-phase controller in which encoders first measure inter-feet distance in the sagittal plane, a continuously running state classifier converts that kinematic relation into the real-time gait phase, and an FSM then routes assistive torques to the exoskeleton joints through a torque control unit.
   对应摘录：A
2. 句子 2：The phase detector distinguishes `right foot forward`, `aligned feet`, and `left foot forward`, defines `aligned feet` as an inter-feet displacement of at most `10 cm`, and introduces a configurable `transition time` so the controller delays the support-to-swing handoff until body weight has plausibly shifted to the new supporting leg.
   对应摘录：B
3. 句子 3：On top of that phase logic, the controller distributes joint-specific assistance across the gait cycle, combining `tKNEE,ext` and `tHIP,ext` for the supporting leg with `tTRUNK` for upright posture and `tHIP,flex / tKNEE,flex` for the swinging leg.
   对应摘录：C
4. 句子 4：The timing profiles in `T1.4` make these torques phase-local rather than global background compensation: hip and knee flexion assistance are tied to toe-off, trunk assistance is active during stance, and knee stabilization plus hip extension are applied while the paretic leg supports the body.
   对应摘录：D
5. 句子 5：At the architectural level, the FSM recognizes one of four plegic-leg states and outputs a reference torque function `t_ref(t,s,q,c)`, so the system preserves both a discrete gait-state backbone and a parameterized assist-as-needed control surface.
   对应摘录：D
