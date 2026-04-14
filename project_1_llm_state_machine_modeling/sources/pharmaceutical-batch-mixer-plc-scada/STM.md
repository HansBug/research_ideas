# Automation of a Pharmaceutical Batch Mixer Using Programmable Logic Controller (PLC) and Supervisory Control and Data Acquisition System (SCADA) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把药剂批混过程拆成带名义时长与温度阈值的八步顺序链，并进一步补上 PLC/SCADA 监控界面，原文细节已经达到双 A。

## 条目 1: Eight-Step Temperature-Controlled Pharmaceutical Batch Mixer

- 控制对象：工业自动化与过程制造领域的药用批混 PLC-SCADA 控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向药剂批量混合生产的 PLC-SCADA 顺序控制器，负责准备、投料、反应、混合、排放、转储与冷却整条工艺链。
- 判断：算。对象是真实工业批处理系统，原文以步骤清单形式给出阶段顺序、名义持续时间、温度阈值、按钮触发和各执行元件动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，Section `2.1.1 Process Description`，`paper_content.txt` 第 174-180 行
> "10 mins"

- 证据说明：原文从准备阶段开始，逐步列出每个阶段的名义时长，并以 `START PB` 作为进入投料阶段的启动事件。

#### 摘录 B

- 出处：第 3-4 页，Section `2.1.1 Process Description`，`paper_content.txt` 第 183-209 行
> "75 °C"

- 证据说明：反应与混合阶段都绑定到目标温度，之后又以 `40 °C` 作为进入排放阶段的触发条件，同时协调冷却水阀、搅拌器、泵和阀门。

#### 摘录 C

- 出处：第 16-17 页，Section `3.1.3 SCADA HMI Design and Implementation`，`paper_content.txt` 第 496-518、555-566 行
> "real-time"

- 证据说明：SCADA 层继续把批次阶段、温度、搅拌速度、原料液位、阀位和报警做成分层监控界面，说明该顺序控制链确实被用于在线监测与操作。

### 2. 基于原文整理后的自然语言描述

The pharmaceutical batch mixer is organized as an eight-step PLC-controlled process whose transitions depend on both event triggers and engineering timing constraints. After a `10-minute` preparation phase, the operator presses `START PB`, sugar crystals are charged into the heating vessel for `3 minutes`, and the reaction stage begins with the temperature controller in manual mode, heating to `75 °C`, then enabling cooling water and holding the stirrer on until the drain stage starts. The next phases continue as an ordered sequence: blend additives for `60 minutes`, wait until the temperature falls to `40 °C`, drain the heating vessel for `45 minutes` while turning on the filter, pump, and mixing-vessel stirrer, then blend preservatives and distilled water for another `60 minutes`. After that, the system transfers the syrup to storage for `20 minutes`, keeps the relevant stirrers active until the source vessel is empty, and finally cools the product to room temperature so it is ready for bottling. The SCADA layer mirrors this state progression with real-time displays of batch phase, temperature, mixer speed, ingredient level, valve position, and alarms, which shows that the sequence is not just a conceptual list but an implemented supervisory control workflow.

### 3. 逐句溯源

1. 句子 1：The pharmaceutical batch mixer is organized as an eight-step PLC-controlled process whose transitions depend on both event triggers and engineering timing constraints.
   对应摘录：A, B
2. 句子 2：After a `10-minute` preparation phase, the operator presses `START PB`, sugar crystals are charged into the heating vessel for `3 minutes`, and the reaction stage begins with the temperature controller in manual mode, heating to `75 °C`, then enabling cooling water and holding the stirrer on until the drain stage starts.
   对应摘录：A, B
3. 句子 3：The next phases continue as an ordered sequence: blend additives for `60 minutes`, wait until the temperature falls to `40 °C`, drain the heating vessel for `45 minutes` while turning on the filter, pump, and mixing-vessel stirrer, then blend preservatives and distilled water for another `60 minutes`.
   对应摘录：B
4. 句子 4：After that, the system transfers the syrup to storage for `20 minutes`, keeps the relevant stirrers active until the source vessel is empty, and finally cools the product to room temperature so it is ready for bottling.
   对应摘录：B
5. 句子 5：The SCADA layer mirrors this state progression with real-time displays of batch phase, temperature, mixer speed, ingredient level, valve position, and alarms, which shows that the sequence is not just a conceptual list but an implemented supervisory control workflow.
   对应摘录：C
