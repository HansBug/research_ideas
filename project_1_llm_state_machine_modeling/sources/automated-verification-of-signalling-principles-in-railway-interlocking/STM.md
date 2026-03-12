# Automated Verification of Signalling Principles in Railway Interlocking Systems - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：联锁控制循环和对象互斥条件明确，但更多体现为 ladder logic 的周期执行与状态约束。

## 条目 1: Periodic execution logic of a railway interlocking controller
- 控制对象：铁路联锁系统的 ladder-logic 控制器

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 ladder-logic interlocking controller，用于在周期扫描中更新信号、道岔和传感输入，并维持铁路站场的安全约束。
- 判断：算，但属于控制器执行循环与互斥约束样本。对象是实际联锁控制器，原文明确给出了扫描循环、输入输出更新以及信号/道岔状态互斥条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Page 3，对 continuous while loop 的描述，行 79-89
> Initialise;
> while(true)foutput(); input(); x1:='1;xn:='n;g
> In the initialisation phase some variables are set to initial values, others remain
> unde
> ned. Then a continuous while loop is entered in which: the values of the
> output variables are sent to the signals, points, etc; the input variables are set
> to the inputs (states of buttons from the control panel, sensors from the track
> segments, sensors from the points, etc.); and then the ladder is executed. Note that,
> while executing the assignments, the real world output variables are not modi
> ed,
> therefore correctness is only required at the end of each execution of the ladder.

#### 摘录 B
- 出处：第 3 页，Page 4，对 physically possible states 与 invariant 的说明，行 127-141
> 1) Not all choices of input variables correspond to physically possible states. An
> example is a 3-way switch which has 3 positions A,B,C(e.g. \control from central
> panel", \control by local station" and \control by emergency panel"). The output
> of such a switch would then be represented by 3 variables, one indicating whether
> Awas chosen, one for Band one for C. At any time at least one of A,B,Cis
> chosen, but if the button is malfunctioning (e.g. staples falling into the button) it
> might be that both AandBorBandCare chosen.
> 2) Some combinations of variables are unreachable. When looking carefully at
> false positives, it was usually found that some variables were in a state which should
> not be reachable, typically when two variables are related to each other (e.g. if the
> green signal is activated the red one is not activated). When such a possible invariant
>
> --- Page 4 ---
>  Invwas discovered (e.g. signal iisred$:signal iisgreen) we 
> rst tried to prove

#### 摘录 C
- 出处：第 4 页，Page 4，对 signalling principle 的例子，行 152-158
> In order to make it easier to write down safety conditions, we formulated them
>
> rst in 
> rst order logic using general predicates. An example would be \points in
> a rail yard should not be set to the normal and reverse positions simultaneously" :
> 8pt2Points ::[normal (pt)^reverse (pt)] (normal andreverse are the two possible
> positions of points). We used Prolog terms to construct a topological model of

### 2. 基于原文整理后的自然语言描述

In each execution cycle, the interlocking controller sends output values to the signals and points, reads the current inputs from the control panel, track sensors and point sensors, and then executes the ladder logic. The controller must exclude physically impossible combinations, such as contradictory switch positions or a green signal being active together with the corresponding red signal. One of the signalling principles is that a point must not be set to the normal and reverse positions simultaneously.

### 3. 逐句溯源

1. 句子 1：In each execution cycle, the interlocking controller sends output values to the signals and points, reads the current inputs from the control panel, track sensors and point sensors, and then executes the ladder logic.
   对应摘录：A
2. 句子 2：The controller must exclude physically impossible combinations, such as contradictory switch positions or a green signal being active together with the corresponding red signal.
   对应摘录：B
3. 句子 3：One of the signalling principles is that a point must not be set to the normal and reverse positions simultaneously.
   对应摘录：C
