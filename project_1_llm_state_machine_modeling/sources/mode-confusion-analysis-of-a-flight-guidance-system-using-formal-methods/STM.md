# Mode confusion analysis of a flight guidance system using formal methods - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文直接描述了 flight guidance system 的 lateral/vertical 模式、armed/active/capture/track 子状态及其约束，非常适合作为飞行控制模式逻辑样本。

## 条目 1: Armed-active-capture-track logic in a flight guidance system
- 控制对象：飞机飞行引导系统（FGS）模式逻辑

### 0. 条目识别与判定

- 一句话说明：这是航空飞行控制领域的 flight guidance system mode logic，用于决定飞机横向与纵向引导模式何时被选择、预位、激活以及从捕获转入跟踪。
- 判断：算。对象是实际 avionics flight guidance subsystem，原文明确给出了 mode 的层级状态、典型 lateral/vertical modes，以及 mode sequencing 约束。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，The Flight Guidance System Mode Logic，行 123-160
> The mode logic determines which lateral and vertical modes of operation are active and armed at any given time. These in turn determine which flight control laws are active and armed.
>
> A mode is said to be selected if it has been manually requested by the flight crew or if it has been automatically requested by a subsystem such as the FMS. The simplest modes have only two states, cleared and selected. Some modes can be armed to become active when a criterion is met. In such modes, the two states armed and active are sub-states of the selected state. Some modes also distinguish between capturing and tracking of the target reference or navigation source. Once in the active state, such a mode's flight control law first captures the target by maneuvering the aircraft to align it with the navigation source or reference. Once correctly aligned, the mode transitions to the tracking state that holds the aircraft on the target.

#### 摘录 B
- 出处：第 2-3 页，The Flight Guidance System Mode Logic，对 lateral/vertical mode families 与 sequencing constraints 的说明，行 163-184
> The mode logic consists of all the available modes and the rules for transitioning between them.
>
> For example, in Figure 2, there are lateral modes of Roll Hold, Heading Hold, Navigation, Lateral Approach, and Lateral Go Around. These control the guidance about the longitudinal, or roll, axis. Guidance about the vertical, or pitch, axis is controlled by the vertical modes of Pitch, Vertical Speed, Altitude Hold, Altitude Select, Vertical Approach, and Vertical Go Around. Each of these modes are associated with one or more control laws. In order to provide effective guidance of the aircraft, these modes are tightly synchronized. Constraints enforce sequencing of modes that are dictated by the characteristics of the aircraft and the airspace. The mode logic is responsible for enforcing these constraints.

### 2. 基于原文整理后的自然语言描述

The flight guidance system mode logic determines which lateral and vertical modes are active and armed at any given time, and these mode decisions determine the flight control laws that are in effect. A mode may be selected by the crew or by another subsystem, then move through armed and active sub-states, and some active modes further progress from a capture state to a tracking state once the aircraft has aligned with the target reference. The mode logic coordinates lateral modes such as Roll Hold, Heading Hold, Navigation, Lateral Approach, and Lateral Go Around with vertical modes such as Pitch, Vertical Speed, Altitude Hold, Altitude Select, Vertical Approach, and Vertical Go Around, and it enforces the sequencing constraints required by the aircraft and the airspace.

### 3. 逐句溯源

1. 句子 1：The flight guidance system mode logic determines which lateral and vertical modes are active and armed at any given time, and these mode decisions determine the flight control laws that are in effect.
   对应摘录：A
2. 句子 2：A mode may be selected by the crew or by another subsystem, then move through armed and active sub-states, and some active modes further progress from a capture state to a tracking state once the aircraft has aligned with the target reference.
   对应摘录：A
3. 句子 3：The mode logic coordinates lateral modes such as Roll Hold, Heading Hold, Navigation, Lateral Approach, and Lateral Go Around with vertical modes such as Pitch, Vertical Speed, Altitude Hold, Altitude Select, Vertical Approach, and Vertical Go Around, and it enforces the sequencing constraints required by the aircraft and the airspace.
   对应摘录：B
