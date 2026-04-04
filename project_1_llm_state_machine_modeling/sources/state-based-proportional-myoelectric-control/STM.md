# A state-based, proportional myoelectric control method: online validation and comparison with the clinical state-of-the-art - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多自由度上肢肌电假肢的功能切换明确写成“每个功能一个状态”的状态式控制框架，并给出 `40 ms` 检测窗、`240 ms` 分类窗、`100-300 ms` 比例估计窗与 detection threshold 逻辑，可直接作为高质量 `EFSM + T1` 样本。

## 条目 1: State-based EMG function-switch controller for hand open/close and wrist rotation
- 控制对象：多自由度上肢肌电假肢的 hand open/close 与 wrist rotation 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向多自由度肌电假肢的状态式功能切换控制器，用检测与分类替代传统 co-contraction 模式切换，并对当前激活功能输出连续比例控制。
- 判断：算。对象是实际假肢控制器，不是单纯分类算法；原文明确给出“每个功能一个状态”的框架、状态转移检测逻辑、分类窗口、比例输出窗口，以及与临床开合手/腕旋控制任务的对应关系。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Methods / Algorithm，行 70-88
> In this study, we present a state-based algorithm for myoelectric control that aimed at improving the user performance with respect to the myoelectric control systems implemented in commercial devices, when controlling the same functions of these devices (two DoFs).
>
> Rather than using muscle co-contraction to switch between DoFs, as in classic commercial prostheses, the proposed approach implemented a more natural control for the switch between functions, and an adaptive proportional control of the activated functions.
>
> The control algorithm used a state-based paradigm. In this framework, a "state" was assigned to each of the desired functions. The transitions among the different states were realized by detection and classification. For each state, proportional control was implemented.

#### 摘录 B
- 出处：第 2 页，Methods / Detection step，行 89-135
> The detection of transitions between motions was based on the average increase in variance across the surface EMG channels.
>
> The data were analyzed based on non-overlapping windows of 40 ms. Consecutive windows were used to form an analysis segment, whose length was variable.
>
> The reference buffer stored the last 1500 ms data, or all available data from the last positive detection, whichever was shorter.
>
> As the intended transition by the subject is usually short, the function ft(L) was introduced to reflect two scenarios: 1) the steady increase of the reliability with an impending motion transition when L is shorter than 300 ms; 2) the sharp decrease in reliability after 300 ms, in the event of a likely inadvertent action.
>
> The current RMT was then compared to a detection threshold (DT, see Results). When RMT > DT (positive detection) or RMT < 20% (no detection), the analysis segment would be reset. Otherwise, the next 40 ms of incoming data would be added to the analysis segment.

#### 摘录 C
- 出处：第 2-3 页，Methods / Classification step and Proportional estimation，行 136-163
> Once a positive detection was triggered, the classification step would take place.
>
> The Hudgins time domain features (TD), i.e. mean absolute value, zero crossing, slope sign change and wave length, were used, and principal component analysis (PCA) was used to reduce the dimensionality of the feature space (components accounted 95% were kept). A linear discriminant analysis (LDA) was used as the classifier.
>
> In the event of positive detection of motion transition, the most recent 240 ms of data prior to detection were used for classification of the next motion.
>
> The proportionality was calculated from the most recent data with variable window length (between 100 ms and 300 ms, adapted for subject's comfort of use).
>
> Motion-specific normalization of the mean absolute value (MAV) was applied to the whitened channels, providing instantaneous estimations of the intended proportional activation level.

#### 摘录 D
- 出处：第 6 页，Comparison with the clinical state-of-the-art，行 311-328
> The industrial SOA utilized the one-site-one-function approach with two-control sites.
>
> An activation threshold was set for each channel. When the threshold of the channels was exceeded, the corresponding function would be selected (e.g., supination or pronation). When the two thresholds were simultaneously exceeded, a mode switch would take place (e.g. from rotation mode to open/close mode).
>
> Individual thresholds of the two channels were chosen through the standard procedure in prosthetic fitting, such that occurrences of un-intended mode switches were minimal while intended activation commands could be easily articulated.

### 2. 基于原文整理后的自然语言描述

The controller models a multi-DoF myoelectric prosthesis as an extended state machine in which each desired function is a state, and transitions between functions are not triggered by co-contraction but by a dedicated detection-and-classification pipeline. Transition detection monitors variance growth across EMG channels in non-overlapping `40 ms` windows, keeps a `1500 ms` reference buffer, and uses an RMT score with a `300 ms` intended-transition profile plus a detection threshold to decide whether a function switch is real or inadvertent. Once a positive transition is detected, the next function is classified from the most recent `240 ms` of EMG using TD features, PCA and LDA, and the active state's command magnitude is then produced from a `100-300 ms` proportional-estimation window using whitened MAV features. The target actuation space is the same hand open/close and wrist rotation space used by clinical two-site prostheses, but the switching logic is encoded explicitly as state transitions instead of simultaneous-threshold co-contraction, which makes the sample a detailed `EFSM + T1` control case rather than a pure pattern-recognition paper.

### 3. 逐句溯源

1. 句子 1：The controller models a multi-DoF myoelectric prosthesis as an extended state machine in which each desired function is a state, and transitions between functions are not triggered by co-contraction but by a dedicated detection-and-classification pipeline.
   对应摘录：A
2. 句子 2：Transition detection monitors variance growth across EMG channels in non-overlapping `40 ms` windows, keeps a `1500 ms` reference buffer, and uses an RMT score with a `300 ms` intended-transition profile plus a detection threshold to decide whether a function switch is real or inadvertent.
   对应摘录：B
3. 句子 3：Once a positive transition is detected, the next function is classified from the most recent `240 ms` of EMG using TD features, PCA and LDA, and the active state's command magnitude is then produced from a `100-300 ms` proportional-estimation window using whitened MAV features.
   对应摘录：C
4. 句子 4：The target actuation space is the same hand open/close and wrist rotation space used by clinical two-site prostheses, but the switching logic is encoded explicitly as state transitions instead of simultaneous-threshold co-contraction, which makes the sample a detailed `EFSM + T1` control case rather than a pure pattern-recognition paper.
   对应摘录：A, D
