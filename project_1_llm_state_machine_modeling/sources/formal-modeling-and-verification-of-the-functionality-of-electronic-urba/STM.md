# Formal Modeling and Verification of the Functionality of Electronic Urban Railway Control Systems Through a Case Study - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：电车平交口保护序列和检测点状态机都给出了可追溯的离散行为。

## 条目 1: Tram-road level crossing protection sequence
- 控制对象：电车平交口保护系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

In the initial state of the system, the road signals show flashing yellow and the tram indicator is blank. When a tram arrives at detection point D1, the road signals change to continuous yellow for 4 to 10 seconds and then to red so that road traffic must stop. After that the indicator shows yellow, which tells the tram driver that road traffic has been stopped successfully and that the tram may cross the intersection at the maximum speed allowed by national rules. When the tram leaves the system at detection point D2, the equipment returns to the initial state.

### 3. 逐句溯源

1. 句子 1：In the initial state of the system, the road signals show flashing yellow and the tram indicator is blank.
   对应摘录：A
2. 句子 2：When a tram arrives at detection point D1, the road signals change to continuous yellow for 4 to 10 seconds and then to red so that road traffic must stop.
   对应摘录：A
3. 句子 3：After that the indicator shows yellow, which tells the tram driver that road traffic has been stopped successfully and that the tram may cross the intersection at the maximum speed allowed by national rules.
   对应摘录：A
4. 句子 4：When the tram leaves the system at detection point D2, the equipment returns to the initial state.
   对应摘录：A

## 条目 2: Detection-point parameter and antagonism handling
- 控制对象：平交口检测点的输入处理状态机
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 C
- 出处：第 14-15 页，State machines，对 `presencehandling` / `releasepermission` 的说明，行 771-790, 803-811
> the PTomin parameter for the duration while both presence
> inputs were in the free state (with PFault true).
> If the presence time To has an upper bound (PTomaxE is
> true), then the state machine can also enter to state over-
> ﬂowed_PTomax. The PTomax value means that thedetection point was occupied for an incredibly long time.
> Such a long occupancy by a tram cannot occur in practice.
> For the DP this means that the value of the To timer wasmore than the PTomax parameter for the duration while
> both presence inputs were in the free state (with PFault
> true).
> Finally, if the DP has correctly detected the occupancy
> according to the conﬁguration (PTomaxE can be also true
> or false), the tram presence will remain in the state
> non_overﬂowed_PTomax. The DP can enter from this stateto the free state without failure (i.e., with false PFault).
> The condition for release is that the DP must
> be neither faulty nor in occupied states for a speciﬁed
> period of time (PTr). The release time is measured by thetimer Tr. The state machine ‘‘releasepermission’’ uses
> outputs of the ‘‘presencehandling’’ (OOccupancy) and
> ‘‘faulthandling’’ (OFailure). Based on these inputs, deter-mine its own output (RPermit) as a function of time Tr.

### 2. 基于原文整理后的自然语言描述

The detection-point logic is decomposed into `paramcheck`, `antagonismcheck`, `presencehandling`, `faulthandling`, `releasepermission`, and `outputsetting` functions. In `paramcheck`, the machine stays in `config_ok` unless a configuration failure occurs, in which case it moves to `config_failure` and reports `CFault`. In `antagonismcheck`, contradictory `in_presence_p` and `in_presence_n` inputs move the component from `non_antagonism` to `antagonism`, start timer `Topn`, keep `AFault` false while `Topn <= PTopn`, and set `AFault` true once `Topn > PTopn`, with the fault value staying true if `Topn` reaches `CInt8Max`; if the contradiction disappears, the machine returns to `non_antagonism` and resets `Topn`. In `presencehandling`, the main states are `free` and `occupied`, the occupancy timer `To` is checked against `PTomin`, `PTomax`, and `PTomaxE` to distinguish short occupancy, overflown `PTomax`, and non-overflown occupancy cases, and `releasepermission` uses timer `Tr` with parameter `PTr` so that the detection point can be released only after it is neither faulty nor occupied for the required release-preparation time.

### 3. 逐句溯源

1. 句子 1：The detection-point logic is decomposed into `paramcheck`, `antagonismcheck`, `presencehandling`, `faulthandling`, `releasepermission`, and `outputsetting` functions.
   对应摘录：B, C
2. 句子 2：In `paramcheck`, the machine stays in `config_ok` unless a configuration failure occurs, in which case it moves to `config_failure` and reports `CFault`.
   对应摘录：A
3. 句子 3：In `antagonismcheck`, contradictory `in_presence_p` and `in_presence_n` inputs move the component from `non_antagonism` to `antagonism`, start timer `Topn`, keep `AFault` false while `Topn <= PTopn`, and set `AFault` true once `Topn > PTopn`, with the fault value staying true if `Topn` reaches `CInt8Max`; if the contradiction disappears, the machine returns to `non_antagonism` and resets `Topn`.
   对应摘录：B
4. 句子 4：In `presencehandling`, the main states are `free` and `occupied`, the occupancy timer `To` is checked against `PTomin`, `PTomax`, and `PTomaxE` to distinguish short occupancy, overflown `PTomax`, and non-overflown occupancy cases, and `releasepermission` uses timer `Tr` with parameter `PTr` so that the detection point can be released only after it is neither faulty nor occupied for the required release-preparation time.
   对应摘录：C
