# Automated Verification of Signalling Principles in Railway Interlocking Systems - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：联锁控制循环和对象互斥条件明确，但条目核心仍偏控制器周期执行与 invariant 约束。

## 条目 1: Periodic execution logic of a railway interlocking controller
- 控制对象：铁路联锁系统的 ladder-logic 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 ladder-logic interlocking controller，用于在周期扫描中更新信号、道岔和传感输入，并维持铁路站场的安全约束。
- 判断：算，但属于控制器执行循环与互斥约束样本。对象是实际联锁控制器，原文明确给出了扫描循环、输入输出更新以及信号/道岔状态互斥条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，对 continuous while loop 与 correctness point 的描述，行 76-102
> Initialise;
> while(true){output(); input(); x1:='1; ... xn:='n;}
> ...
> Then a continuous while loop is entered in which: the values of the
> output variables are sent to the signals, points, etc; the input variables are set
> to the inputs ...; and then the ladder is executed. Note that,
> while executing the assignments, the real world output variables are not modiﬁed,
> therefore correctness is only required at the end of each execution of the ladder.
> ...
> we show that  holds after initialisation and one execution of the ladder;
> and that, if  holds before the execution of the ladder, it holds afterwards as well.

#### 摘录 B
- 出处：第 3-4 页，对 impossible/unreachable combinations 与 invariant 的说明，行 109-145
> Not all choices of input variables correspond to physically possible states.
> ...
> Some combinations of variables are unreachable.
> ...
> when two variables are related to each other (e.g. if the
> green signal is activated the red one is not activated).
> ...
> An example would be "points in
> a rail yard should not be set to the normal and reverse positions simultaneously":
> 8pt2Points ::[normal (pt)^reverse (pt)]

### 2. 基于原文整理后的自然语言描述

The interlocking controller initializes its variables and then repeatedly executes the cycle `output(); input(); ladder`. In each cycle it first sends the current output values to physical objects such as signals and points, then reads the latest control-panel, track-segment, and point-sensor inputs, and only after that executes the ladder logic. Because the real-world outputs are not changed while the ladder assignments are being evaluated, safety is required at the end of each ladder execution cycle rather than in the middle of the scan. The controller is also constrained by invariants that exclude physically impossible or unreachable combinations, such as contradictory switch positions or a green signal together with the corresponding red signal. One explicit signalling principle is that a point must never be in the normal and reverse positions simultaneously.

### 3. 逐句溯源

1. 句子 1：The interlocking controller initializes its variables and then repeatedly executes the cycle `output(); input(); ladder`.
   对应摘录：A
2. 句子 2：In each cycle it first sends the current output values to physical objects such as signals and points, then reads the latest control-panel, track-segment, and point-sensor inputs, and only after that executes the ladder logic.
   对应摘录：A
3. 句子 3：Because the real-world outputs are not changed while the ladder assignments are being evaluated, safety is required at the end of each ladder execution cycle rather than in the middle of the scan.
   对应摘录：A
4. 句子 4：The controller is also constrained by invariants that exclude physically impossible or unreachable combinations, such as contradictory switch positions or a green signal together with the corresponding red signal.
   对应摘录：B
5. 句子 5：One explicit signalling principle is that a point must never be in the normal and reverse positions simultaneously.
   对应摘录：B
