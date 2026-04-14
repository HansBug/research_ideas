# Automatic Bottle Filling and Capping Machine using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了一条明确的 `start -> 停带灌装 -> 前送挂盖 -> 停位压盖 -> 送往下一工位` 算法链，并补上了 PLC 运行说明和传感器/执行器配置，双 A 条件成立。

## 条目 1: Conveyor-stop timed fill and cap-piston sequence controller

- 控制对象：工业自动化与离散制造领域的输送带瓶装灌装与压盖顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `SELEC PLC` 的瓶装灌装封盖控制器，用输送带、填充位传感器、阀门、旋转盘、挂盖机构和压盖活塞完成连续生产循环。
- 判断：算。对象是实际制造顺序控制系统，原文直接给出九步过程算法和 PLC 实际执行说明，不是泛泛的设备介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Introduction`，`paper_content.txt` 第 9-29、41-50 行
> The filling of the bottle is controlled by using a controller known as PLC. ... Different sensors have been utilized to identify the position of the bottle. ... Our task having three areas includes the sensing the bottle on the conveyor belt then dispensing the required amount of liquid into the bottle by the solenoid valve. Then it will move the bottle over the conveyor belt. Capping system is accomplished by utilizing dc gear engine and sensors. ... The whole system operation is controlled by SELEC PLC.

#### 摘录 B

- 出处：第 1 页，`III. PROCESS ALGORITHM`，`paper_content.txt` 第 56-72 行
> 1) STEP 1: Press the “START” Push Button.
>
> 2) STEP 2: Motor starts and conveyor is moving forward.
>
> 3) STEP 3: If sensor detects empty bottle in filling section, conveyor will stop.
>
> 4) STEP 4: After some delay the valve will turn “ON” and the bottle will get filled with liquid.
>
> 5) STEP 5: After the bottle is filled, conveyor will move forward.
>
> 6) STEP 6: As the bottle is moving forward, the cap will be placed by cap hopper automatically.
>
> 7) STEP 7: After the cap is placed the bottle will move further and the bottle will stop below the capping piston.
>
> 8) STEP 8: After some delay the capping piston will come down and the cap will be placed tightly.
>
> 9) STEP9: After the cap is placed the bottle will go further process.

#### 摘录 C

- 出处：第 2-3 页，`Hardware Description / Software Used and Programming`，`paper_content.txt` 第 93-116、117-127、176-193 行
> Hardware part of the system consists of PLC ... photo electric sensor (2), metal proximity sensor(4), ... conveyor, rotating metal disc, 12V 30 RPM dc gear motor(4) ...
>
> The PLC controls the input and output depending on program given. ... The PLC checks the input status and it scans the input by user defined programming. Next the process is executed and finally it checks the output status.
>
> ... When the photo electric sensor detect the bottle in filling section, conveyor immediately stop. Then PLC will on solenoid valve to fill water in particular time ... After the timing is expired the conveyor will move again forward ... metal proximity sensor send the signal to controller to start motor2 ... When it comes to capping position rotating disc motor stop. Then two dc gear motor start and perform capping operation. After capping is finished motor will rotate and lift bottle to conveyor 2 ...

### 2. 基于原文整理后的自然语言描述

The PLC bottle machine starts from a pushbutton-triggered transport state in which the conveyor runs forward until a bottle reaches the filling section. When the filling sensor detects that bottle, the controller stops the conveyor, waits for the programmed delay, and turns on the solenoid valve so the bottle is filled while it remains stationary. After the timed fill completes, the conveyor restarts and the bottle advances to the cap hopper, where a cap is placed automatically before the bottle moves on to the capping position. At that second stop point, the rotating-disc motor halts, the capping piston comes down after another delay, and the DC gear motors tighten the cap. Once capping is finished, the machine rotates and transfers the bottle to the continuously running second conveyor so it can leave for the next process stage.

### 3. 逐句溯源

1. 句子 1：The PLC bottle machine starts from a pushbutton-triggered transport state in which the conveyor runs forward until a bottle reaches the filling section.
   对应摘录：A, B
2. 句子 2：When the filling sensor detects that bottle, the controller stops the conveyor, waits for the programmed delay, and turns on the solenoid valve so the bottle is filled while it remains stationary.
   对应摘录：B, C
3. 句子 3：After the timed fill completes, the conveyor restarts and the bottle advances to the cap hopper, where a cap is placed automatically before the bottle moves on to the capping position.
   对应摘录：B, C
4. 句子 4：At that second stop point, the rotating-disc motor halts, the capping piston comes down after another delay, and the DC gear motors tighten the cap.
   对应摘录：B, C
5. 句子 5：Once capping is finished, the machine rotates and transfers the bottle to the continuously running second conveyor so it can leave for the next process stage.
   对应摘录：B, C
