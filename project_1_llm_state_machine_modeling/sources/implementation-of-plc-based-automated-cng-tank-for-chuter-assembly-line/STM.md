# Implementation of PLC Based Automated CNG Tank for Chuter Assembly Line - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `master on 延时 -> 传感检测 CNG 罐 -> loading pusher 推送 -> stopper 站间阻挡 -> 手动/自动两种运行` 这条滚筒线控制链写得比较完整，双 A 可成立。

## 条目 1: Loading-pusher and stopper-controlled CNG tank transfer line

- 控制对象：离散制造领域的 CNG 罐滚筒线推送与站间止挡控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 CodeSys 梯形图的 CNG 罐 chuter 装配线控制系统，用接近传感器、loading station pusher、stopper、lifter 和手动/自动模式管理滚筒线转运。
- 判断：算。对象是实际装配线控制器，原文明确写出了输入输出地址、5 秒启动延时、站间推送/止挡逻辑和手动/自动两种运行方式。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5-6 页，`PLC And Chuter Assembly Line`，`paper_content.txt` 第 185-218 行
> Realizing the CNG tank's sensing was the first task. In order to do this, proximity sensors have been utilised ... While starting the program in CodeSys software some address has given for input / output modules. ... physical input address has been given to the input modules such as air on, master on, loading station pusher, lifter 1 and 2 ... output modules address given, such as tower lamps, loading station lamp, unloading station lamp. ... Timer has been used in this process so that when master is ON the machine should take a delay in the start for about 5 seconds ...
>
> In the next task, placing of the CNG tank at the loading station in a systematic manner. Following with that the sensor senses the CNG tank placed on the roller conveyor and with that the pusher ... pushes the CNG tank to move forward to station and with that there is other drive ... called as stopper. At each stations there is a stopper provided. If there is other component in the next station the stopper stops the CNG tank to slide to next station.

#### 摘录 B

- 出处：第 6 页，`PLC And Chuter Assembly Line`，`paper_content.txt` 第 219-229 行
> First, both a manual and automatic alternative was developed. In addition to that TOF timer, a TON timer was also utilised. This operates so that pressing the button rings the bell, which must be held ringing for five seconds before the programme can begin. And the process begins when the button is released. ... A test panel is built in the software itself for testing purposes so that we can see how it works visually. With the PLC ladder logic diagram the test is completed successful.

### 2. 基于原文整理后的自然语言描述

The chuter-line controller begins from a master-enabled idle condition and enforces a five-second start delay before the automated sequence is allowed to run. Once the line is active, proximity sensing detects the arrival of a CNG tank at the loading station, and the loading pusher moves that tank forward from the roller conveyor into the next station. Each downstream station is guarded by a stopper, so the PLC permits transfer only when the next position is free and blocks the tank when the following station is still occupied. The line logic also coordinates auxiliary devices such as lifters, indicator lamps, and pushbuttons through mapped input and output addresses. In addition to the automatic sequence, the program supports a manual alternative, so the operator can switch between two operating styles while preserving the same sensor-and-actuator chain.

### 3. 逐句溯源

1. 句子 1：The chuter-line controller begins from a master-enabled idle condition and enforces a five-second start delay before the automated sequence is allowed to run.
   对应摘录：A, B
2. 句子 2：Once the line is active, proximity sensing detects the arrival of a CNG tank at the loading station, and the loading pusher moves that tank forward from the roller conveyor into the next station.
   对应摘录：A
3. 句子 3：Each downstream station is guarded by a stopper, so the PLC permits transfer only when the next position is free and blocks the tank when the following station is still occupied.
   对应摘录：A
4. 句子 4：The line logic also coordinates auxiliary devices such as lifters, indicator lamps, and pushbuttons through mapped input and output addresses.
   对应摘录：A
5. 句子 5：In addition to the automatic sequence, the program supports a manual alternative, so the operator can switch between two operating styles while preserving the same sensor-and-actuator chain.
   对应摘录：B
