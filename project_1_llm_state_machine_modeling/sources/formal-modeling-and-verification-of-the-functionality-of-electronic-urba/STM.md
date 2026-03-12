# Formal Modeling and Verification of the Functionality of Electronic Urban Railway Control Systems Through a Case Study - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：电车平交口保护序列和检测点状态机都给出了可追溯的离散行为。

## 条目 1: Tram-road level crossing protection sequence
- 控制对象：电车平交口保护系统

### 0. 条目识别与判定

- 一句话说明：这是城市轨道交通控制领域的 tram-road level crossing protection system，用于在有电车接近时切换道路信号和电车指示器以保护平交口。
- 判断：算。对象是实际平交口控制系统，原文给出了无车、检测到电车、道路禁止通行、电车获准通过以及恢复初始状态的连续控制步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 11 页，Case study，对 initial state 与 tram arrival 的描述，行 601-608
> In the initial state of the system (no tram in the scope of
> the system), road signals show ﬂashing yellow, and the
> indicator is blank. When a tram arrives at detection point
> D1, the road signals change to continuous yellow. Thisstate lasts for a well-deﬁned, short period (from 4 to 10
> seconds) of time. After that, the road signals change to a
> red aspect, and road trafﬁc must stop. Then the yellowaspect appears on the indicator. To the tram driver, this
> means that road trafﬁc has been stopped successfully. Thus,
> the tram can cross the intersection at the maximum speedallowed by national rules. When the tram has left the

### 2. 基于原文整理后的自然语言描述

In the initial state of the system, the road signals show flashing yellow and the tram indicator is blank. When a tram arrives at detection point D1, the road signals change to continuous yellow for a short period and then to red so that road traffic must stop. After that the tram indicator shows yellow to permit the tram to cross, and when the tram has left the protected area the road signals return to flashing yellow.

### 3. 逐句溯源

1. 句子 1：In the initial state of the system, the road signals show flashing yellow and the tram indicator is blank.
   对应摘录：A
2. 句子 2：When a tram arrives at detection point D1, the road signals change to continuous yellow for a short period and then to red so that road traffic must stop.
   对应摘录：A
3. 句子 3：After that the tram indicator shows yellow to permit the tram to cross, and when the tram has left the protected area the road signals return to flashing yellow.
   对应摘录：A

## 条目 2: Detection-point parameter and antagonism handling
- 控制对象：平交口检测点的输入处理状态机

### 0. 条目识别与判定

- 一句话说明：这是城市轨道交通平交口系统中的 detection-point input handling logic，用于检查参数配置并处理 presence/negated presence 输入矛盾。
- 判断：算。虽然是构件级样本，但对象是平交口控制系统中的实际输入处理部件，原文明确给出了 configuration ok/failure 与 antagonism 的处理路径。

### 1. 原文摘录

#### 摘录 A
- 出处：第 14 页，State machines，对 paramcheck state machine 的说明，行 733-737
> ‘‘paramcheck’’ state machine is trivial: when there is a
> conﬁguration failure in the system, it remains in the con-
> ﬁg_failure state. If a conﬁguration fault occurs duringsystem operation (e.g., the ‘‘parameter store’’ is damaged),
> the state machine will transit to the conﬁg_failure state
> from the conﬁg_ok state. The ‘‘paramcheck’’ state machinegives failure at its output when it is in the conﬁg_failure

#### 摘录 B
- 出处：第 14 页，State machines，对 antagonism / presencehandling 的说明，行 742-754
> (in_presence_p) and negated presence (in_presence_n)inputs are not in contradiction (non_antagonism state). In
> the non_antagonism state, the Topn timer does not run, and
> the AFault output of this function is false (i.e., there is noantagonism between presence inputs of DP). If the DP
> detects a discrepancy between the presence inputs, it enters
> the state antagonism. In the antagonism state the Topntimer runs. If the antagonism disappears, the state machine
> returns to the non_antagonism state and resets the Topn
> timer. If timer Topn is less than or equal to PTopn, therewill be no antagonism failure at output AFault (AFault is
> false). If timer Topn is greater than PTopn and less than
> CInt8Max, there will be antagonism failure at outputAFault (AFault is true). If timer Topn reaches value
> CInt8Max, it will still be a true value at output AFault.
> Until Topn reaches CInt8Max, the DP component would beable to provide accurate information to the diagnostics
> about how long the antagonism fault has occurred.
> The ‘‘presencehandling’’ state machine (see Fig. 9

### 2. 基于原文整理后的自然语言描述

The parameter-checking logic stays in a configuration-ok condition and moves to configuration-failure when a parameter check fails. It also checks whether the presence and negated presence inputs contradict each other, and when the contradiction appears the logic enters an antagonism condition. The logic leaves that condition only after the antagonism disappears or the timeout handling has completed.

### 3. 逐句溯源

1. 句子 1：The parameter-checking logic stays in a configuration-ok condition and moves to configuration-failure when a parameter check fails.
   对应摘录：A
2. 句子 2：It also checks whether the presence and negated presence inputs contradict each other, and when the contradiction appears the logic enters an antagonism condition.
   对应摘录：B
3. 句子 3：The logic leaves that condition only after the antagonism disappears or the timeout handling has completed.
   对应摘录：B
