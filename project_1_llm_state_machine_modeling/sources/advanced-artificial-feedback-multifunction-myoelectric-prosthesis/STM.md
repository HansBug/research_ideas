# The clinical relevance of advanced artificial feedback in the control of a multi-functional myoelectric prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确记录 Michelangelo 多功能假手的可配置 state machine、`100 Hz` 采样、`3%` 接触阈值、`200/250/1500 ms` 触觉 burst 时序，以及 `palmar / lateral / rotation` 三功能切换和 force-range 编码，可直接作为 `EFSM + T1` 样本。

## 条目 1: Trigger-switch Michelangelo controller with state-coded vibrotactile feedback
- 控制对象：Michelangelo 多功能肌电假手的 sequential/proportional controller 与状态反馈接口
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 Michelangelo 多功能假手的可配置状态式控制器，用 trigger-based EMG bursts 在 `palmar grip / lateral grip / wrist rotation` 三个 DoF 之间切换，并用离散/连续混合的 vibrotactile code 回传接触、功能切换和抓握力区间。
- 判断：算。对象是真实多功能假手控制器；虽然论文研究重点是反馈，但正文完整保住了控制状态集合、切换事件、采样率、传感输入、力阈值和 burst 时序，足以支持状态机级建模。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Experimental setup and feedback coding，行 254-273
> The internal controller of the Michelangelo prosthesis provided commercial state-of-the-art two-channel sequential and proportional myoelectric control, with trigger-based (i.e., single- or two-channel bursts of EMG activity) switching between three available functions (DoFs): palmar grip, lateral grip, and wrist rotation.
>
> The state machine operating the prosthesis, including the trigger type and the switching order between the DoFs, was configured for each subject individually, based on his/her preferences, and the configuration was not changed throughout the experiment.
>
> The prosthesis was instrumented with three position encoders (thumb, fingers, and wrist) and a single force transducer ... measuring the hand aperture, hand rotation and grasping force, respectively.
>
> The embedded prosthesis controller samples the sensor data and the processed EMG signals at the frequency of 100 Hz. The maximum prosthesis grip force was 70 N in palmar grip.

#### 摘录 B
- 出处：第 4 页，Experimental setup and feedback coding，行 290-309
> To transmit the full state of a multi DOF prosthesis, the VFS integrated multiple feedback variables of which some were discrete in nature (contact event, DOF switching) and some continuous (grasping force).
>
> The feedback communicated the following information to the subjects: ‘Touch’ events, ‘DoF-switching’ events, and the prosthesis force.
>
> The ‘Touch’ was detected when the prosthesis grasping force crossed the threshold of 3% of maximum force (rising edge), and this was indicated to the user by delivering a single 250-ms long vibration burst at 50% of the maximum amplitude at all four stimulation sites simultaneously.

#### 摘录 C
- 出处：第 5 页，DoF-switch and force coding，行 324-350
> The ‘DoF-Switch’ feedback comprised three discrete events, namely, switching into the lateral or palmar grasp and switching from grasping to wrist rotation control.
>
> These events were encoded by two short vibration bursts (two times 200 ms, with 100 ms of no vibration in between) at the maximal amplitude delivered through different tactor pairs, depending on the selected function.
>
> The ‘Force’ feedback communicated five ranges of the grasping force.
>
> When the subject felt only the ‘Touch’ feedback, he/she knew that the grasping force was between 3 and 10%. The remaining ranges were represented ... in the ranges 11–24%, 25–39%, 40–59% and ≥60% of the maximum force.
>
> The tactor pairs were activated sequentially from ventral to medial side ... and the vibration amplitude was simultaneously increased (55%, 70%, 85% and 100%, respectively).

#### 摘录 D
- 出处：第 5 页，Force burst delivery，行 348-353
> In order to prevent habituation, the force range was communicated as a single 1500-ms long vibration burst.
>
> The burst was delivered only if EMG activity was detected, indicating that the subject intended to operate the prosthesis, or if the force level had changed.

### 2. 基于原文整理后的自然语言描述

The Michelangelo hand is controlled as a configurable extended state machine whose primary functional states are `palmar grip`, `lateral grip`, and `wrist rotation`, and switching between them is driven by trigger-like single- or dual-channel EMG bursts rather than by continuous proportional blending across all DoFs. The embedded controller closes the loop over thumb, finger, and wrist encoders plus a thumb-base force transducer, and it samples both sensor data and processed EMG at `100 Hz`, with palmar-grip output reaching up to `70 N`. On top of that state machine, the interface encodes state and contact semantics explicitly: crossing `3%` of maximum force triggers a `250 ms` full-site touch burst, and DoF-switch events are signaled by two `200 ms` bursts separated by `100 ms` to denote entry into lateral grip, palmar grip, or wrist rotation. Grasp force is discretized into `3-10%`, `11-24%`, `25-39%`, `40-59%`, and `>=60%` bands, mapped to ordered tactor locations and amplitudes `55% / 70% / 85% / 100%`, and delivered as a `1500 ms` burst only when EMG intent is present or the force band changes. This preserves both the internal discrete control logic and the external state-feedback contract, making the sample a detailed `EFSM + T1` prosthesis-control case rather than only a sensory-feedback study.

### 3. 逐句溯源

1. 句子 1：The Michelangelo hand is controlled as a configurable extended state machine whose primary functional states are `palmar grip`, `lateral grip`, and `wrist rotation`, and switching between them is driven by trigger-like single- or dual-channel EMG bursts rather than by continuous proportional blending across all DoFs.
   对应摘录：A
2. 句子 2：The embedded controller closes the loop over thumb, finger, and wrist encoders plus a thumb-base force transducer, and it samples both sensor data and processed EMG at `100 Hz`, with palmar-grip output reaching up to `70 N`.
   对应摘录：A
3. 句子 3：On top of that state machine, the interface encodes state and contact semantics explicitly: crossing `3%` of maximum force triggers a `250 ms` full-site touch burst, and DoF-switch events are signaled by two `200 ms` bursts separated by `100 ms` to denote entry into lateral grip, palmar grip, or wrist rotation.
   对应摘录：B, C
4. 句子 4：Grasp force is discretized into `3-10%`, `11-24%`, `25-39%`, `40-59%`, and `>=60%` bands, mapped to ordered tactor locations and amplitudes `55% / 70% / 85% / 100%`, and delivered as a `1500 ms` burst only when EMG intent is present or the force band changes.
   对应摘录：C, D
5. 句子 5：This preserves both the internal discrete control logic and the external state-feedback contract, making the sample a detailed `EFSM + T1` prosthesis-control case rather than only a sensory-feedback study.
   对应摘录：A, B, C, D
