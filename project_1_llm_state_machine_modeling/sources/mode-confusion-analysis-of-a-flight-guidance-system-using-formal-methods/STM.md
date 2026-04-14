# Mode confusion analysis of a flight guidance system using formal methods - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接描述了 FCP/PFD 交互、lateral/vertical 模式族、`selected/armed/active/capture/track` 层级和 annunciation 约束，非常适合作为飞行控制模式逻辑样本。

## 条目 1: Armed-active-capture-track logic in a flight guidance system
- 控制对象：飞机飞行引导系统（FGS）模式逻辑
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空飞行控制领域的 flight guidance system mode logic，用于决定飞机横向与纵向引导模式何时被选择、预位、激活以及从捕获转入跟踪。
- 判断：算。对象是实际 avionics flight guidance subsystem，原文明确给出了 mode 的层级状态、典型 lateral/vertical modes，以及 mode sequencing 约束。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，FGS / Mode Logic，`paper_content.txt` 第 115-184 行
> The flight crew interacts with the FGS primarily through the Flight Control Panel (FCP). The FCP includes switches for turning the Flight Director (FD) on and off, and switches for selecting the different flight modes. The FCP also supplies feedback to the crew, indicating selected modes by lighting lamps on either side of a selected mode's switch.
>
> The mode logic determines which lateral and vertical modes of operation are active and armed at any given time. These in turn determine which flight control laws are active and armed. These are annunciated, or displayed, on the Primary Flight Displays (PFD) ...
>
> A mode is said to be selected if it has been manually requested by the flight crew or if it has been automatically requested by a subsystem such as the FMS. The simplest modes have only two states, cleared and selected. Some modes can be armed to become active when a criterion is met. In such modes, the two states armed and active are sub-states of the selected state. Some modes also distinguish between capturing and tracking of the target reference or navigation source. Once in the active state, such a mode's flight control law first captures the target ... Once correctly aligned, the mode transitions to the tracking state ...

#### 摘录 B
- 出处：第 3, 9-11 页，Mode families / Hidden modes / Distinct annunciations，`paper_content.txt` 第 163-184, 700-717, 820-857 行
> The mode logic consists of all the available modes and the rules for transitioning between them.
>
> There are lateral modes of Roll Hold, Heading Hold, Navigation, Lateral Approach, and Lateral Go Around. ... Guidance about the vertical, or pitch, axis is controlled by the vertical modes of Pitch, Vertical Speed, Altitude Hold, Altitude Select, Vertical Approach, and Vertical Go Around. ... these modes are tightly synchronized. Constraints enforce sequencing of modes that are dictated by the characteristics of the aircraft and the airspace.
>
> The value of the mode annunciations are determined by values of the previous system state ... and the current inputs ... If the offside FD is not adequately visible to the pilot, there is no way for the pilot to predict whether the mode annunciations will turn off when pressing the FD switch. This is a hidden mode.
>
> Distinct_Mode_Annunciations : THEOREM ... if states `s1` and `s2` do not have the same modes, their mode annunciations must also be different.

### 2. 基于原文整理后的自然语言描述

The flight crew interacts with the flight-guidance system through the FCP, which selects modes and lights mode switches, while the active and armed modes are annunciated on the PFD together with the resulting guidance cues. The mode logic separates lateral, vertical, and auxiliary modes and treats each mode as `cleared/selected`, with some selected modes containing `armed` and `active` substates and some active modes further split into `capture` and `track`. It coordinates lateral modes such as Roll Hold, Heading Hold, Navigation, Lateral Approach, and Lateral Go Around with vertical modes such as Pitch, Vertical Speed, Altitude Hold, Altitude Select, Vertical Approach, and Vertical Go Around, and it keeps them tightly synchronized by sequencing constraints imposed by the aircraft and the airspace. The feedback logic also depends on previous mode annunciations, onside and offside FD status, autopilot engagement, and overspeed condition, so different mode configurations must produce distinct annunciations in order to avoid hidden modes.

### 3. 逐句溯源

1. 句子 1：The flight crew interacts with the flight-guidance system through the FCP, which selects modes and lights mode switches, while the active and armed modes are annunciated on the PFD together with the resulting guidance cues.
   对应摘录：A
2. 句子 2：The mode logic separates lateral, vertical, and auxiliary modes and treats each mode as `cleared/selected`, with some selected modes containing `armed` and `active` substates and some active modes further split into `capture` and `track`.
   对应摘录：A
3. 句子 3：It coordinates lateral modes such as Roll Hold, Heading Hold, Navigation, Lateral Approach, and Lateral Go Around with vertical modes such as Pitch, Vertical Speed, Altitude Hold, Altitude Select, Vertical Approach, and Vertical Go Around, and it keeps them tightly synchronized by sequencing constraints imposed by the aircraft and the airspace.
   对应摘录：B
4. 句子 4：The feedback logic also depends on previous mode annunciations, onside and offside FD status, autopilot engagement, and overspeed condition, so different mode configurations must produce distinct annunciations in order to avoid hidden modes.
   对应摘录：B
