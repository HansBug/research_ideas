# PLC and SCADA Based Sewage Water Treatment Plant - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `tank 1 -> tank 2 -> tank 3` 的筛分、沉降、加药、氧化和按 pH 分流链写成了带延时和故障/紧急停机语义的 PLC/SCADA 顺序控制器，可稳定形成双 A 污水处理样本。

## 条目 1: Tank-Sequenced Sewage Treatment and pH-Routing Supervisor

- 控制对象：污水处理厂的筛分、沉降、加药、氧化与按 pH 分流监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是过程与环境控制领域的污水处理顺序控制器，沿 `tank 1 -> tank 2 -> tank 3` 推进筛分、沉降、加药、氧化和排出用途选择，并在 SCADA 上保留紧急停机和故障安全语义。
- 判断：算。对象是真实污水处理控制系统，原文明确说明了各 tank 的阶段职责、转移触发、延时、泵/搅拌器/电磁阀动作，以及 pH 条件下的最终分流。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`Treatment Techniques`，`paper_content.txt` 第 97-113 行
> Tank 1 contains wastewater ... After some time delay, a pipe transfers the sewage water from tank 1 to tank 2.
>
> As soon as sufficient water from tank 1 is taken in the tank 2, pipe closes. Here stirrer is used ...
>
> After a certain time delay pump 1 turns on and chlorine water goes into Tank 2.
>
> Water in tank 2 is kept stable until chlorination is completed ...
>
> As soon as alum and chlorine are added, stirrer in tank starts rotating ... Once the pump 2 is opened, Stirrer stops rotating. After certain amount of delay pump 2 is opened and water from tank 2 is transfer into tank 3.

#### 摘录 B

- 出处：第 2 页，`Oxidation`，`paper_content.txt` 第 115-119 行
> Tank 3 contains an AC pump operated with the help of relays to increase the amount of oxygen in the tank ...
>
> Sample of water is taken from tank 3 to measure the pH of water. Once the pH is considered suitable, Solenoid valve SV1 and SV2 are opened according to the purpose.

#### 摘录 C

- 出处：第 3-4 页，`SCADA Screen / Advantages and Limitations`，`paper_content.txt` 第 167-182、194-199 行
> The SCADA screen ... monitors and controls the overall process of sewage water treatment. With the help of this screen operator can give signals to all the ongoing field operations. One emergency stop key is provided on the screen which can be used in emergency situation.
>
> When operator receives pH data he puts pH value on screen and depending upon the pH value purified water will be distributed to either domestic or agricultural use.
>
> Fail-safe operation. Does not start automatically when power failure ...

### 2. 基于原文整理后的自然语言描述

The sewage-treatment supervisor organizes the plant as a tank-sequenced process that begins with screening and dwell time in `Tank 1`, then transfers wastewater into `Tank 2` for sedimentation and chemical dosing. Once enough water reaches `Tank 2`, the transfer pipe closes, solids settle, and after a delay `pump 1` introduces chlorine and alum while the stirrer runs to mix the tank. When chlorination is completed and another delay expires, `pump 2` opens, the stirrer stops, and the treated water is moved into `Tank 3`. In the final stage an AC pump raises oxygen concentration, a pH sample is taken from `Tank 3`, and the controller opens `SV1` or `SV2` to route the purified water according to its intended use. The SCADA layer supervises the whole sequence, provides an emergency-stop path, and the paper explicitly notes that the PLC is operated in a fail-safe way by not auto-restarting after power failure.

### 3. 逐句溯源

1. 句子 1：The sewage-treatment supervisor organizes the plant as a tank-sequenced process that begins with screening and dwell time in `Tank 1`, then transfers wastewater into `Tank 2` for sedimentation and chemical dosing.
   对应摘录：A
2. 句子 2：Once enough water reaches `Tank 2`, the transfer pipe closes, solids settle, and after a delay `pump 1` introduces chlorine and alum while the stirrer runs to mix the tank.
   对应摘录：A
3. 句子 3：When chlorination is completed and another delay expires, `pump 2` opens, the stirrer stops, and the treated water is moved into `Tank 3`.
   对应摘录：A
4. 句子 4：In the final stage an AC pump raises oxygen concentration, a pH sample is taken from `Tank 3`, and the controller opens `SV1` or `SV2` to route the purified water according to its intended use.
   对应摘录：B, C
5. 句子 5：The SCADA layer supervises the whole sequence, provides an emergency-stop path, and the paper explicitly notes that the PLC is operated in a fail-safe way by not auto-restarting after power failure.
   对应摘录：C
