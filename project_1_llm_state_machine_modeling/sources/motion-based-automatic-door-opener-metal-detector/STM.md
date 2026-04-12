# Design and Construction of a Motion-Based Automatic Door Opener with Metal Detector - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然控制对象不复杂，但把 `PIR + metal detector + PIC + servo + buzzer + LCD` 的 guard、输出和回闭过程都写得很明确，足以形成高质量自动门控制样本。

## 条目 1: PIR-and-metal-gated automatic door controller

- 控制对象：楼宇机电与电梯控制领域的基于 `PIR` 与金属检测的自动门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个由 `PIC16F877A` 控制的自动门系统，依据人体感应与金属探测结果决定开门、关门、报警和状态显示。
- 判断：算。对象是真实门控控制器，原文给出了输入组合、输出动作、开闭方向、报警分支和程序代码，不是只有硬件介绍的薄链稿。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This project work presents a motion-based automatic door opener with a metal detector. ... This work is designed to provide easy access through doorways and prevent entry with metals which may be harmful. This is achieved using a passive infrared (PIR) sensor which is used to sense the presence of a human being through the person’s body heat. The information from the PIR sensor is fed to a microcontroller which gives an output to the servo motor to rotate and move the door open and close. The programming of the microcontroller is done in such a way that the door opens only when the PIR sensor is ‘high’ indicating human detected and the metal detector is ‘low’ indicating no metal detected and as such entry with metal is prevented automatically.

#### 摘录 B

- 出处：第 3 页，Theoretical Framework / Conceptual Framework
> The microcontroller waits until it receives a message from the metal detector indicating that no metal is detected before it sends a message to the servo motor which moves through 180 degrees to open the door.
>
> The microcontroller analyses the input from the PIR sensor and metal detector and gives an output to the servomotor which rotates to indicate door opening and door closing. An LCD screen is used as an output device to display the door status (Door Opened or Door Closed) appropriately. When the input from the metal detector is high, indicating the presence of a metal approaching the door; the microcontroller sends a signal to a buzzer for security alert.

#### 摘录 C

- 出处：第 14-15 页，Programming / Simulation results
> When the port carrying the PIR and the metal detector circuit are both high, then the door will not open and it sounds an alarm indicating that it has sensed a metal but if the PIR is high and the metal detector is low. It implies that no metal is detected so it swings the servo motor arm to 1800 and waits till the PIR port is low before it swings back to 00 to close the door.
>
> When the PIR sensor and metal detector is ‘high’, the servo motor swings to -90o and closes the door.
>
> When the PIR sensor is ‘low’ and the metal detector is ‘high’, the servo motor turns to -90o and the door remains closed.

#### 摘录 D

- 出处：第 19 页，Program listing
> if(PORTB.B1==0 && PORTB.B0==0) //check if human with metal is present
> {
>   PORTB.RB5=1; // sound alarm
>   close_door();
>   lcd_Out(2,5,"CLOSED");
> }
>
> if(PORTB.B1==0 && PORTB.B0==1) // Check if human is present
> {
>   do
>   {
>     PORTB.RB5=0;
>     open_door();
>     lcd_Out(2,5,"OPENED");
>   } while(PORTB.B1==0);
> }
> delay_ms(1000);
> close_door();
> lcd_Out(2,5,"CLOSED");

#### 摘录 E

- 出处：第 17 页，Results
> The result shows that the circuit works as expected for the door opens only when a person without a metal is around the PIR sensor range and the LCD outputs the door status ‘Door Opened’. For other conditions when a person is within sensor range and with a metal, the LCD outputs the door status ‘Door Closed’. The door status remains closed until when the PIR sensor is ‘high’ and the Metal Detector ‘low’.

### 2. 基于原文整理后的自然语言描述

The controller combines a `PIR` sensor, a metal detector, a `PIC16F877A`, a servo motor, an LCD, and a buzzer to supervise a single automatic door. Motion detection alone is not enough: the microcontroller only opens the door when the `PIR` input indicates a person and the metal-detector input stays low, which it represents by rotating the servo from `0°` to `180°` and showing `OPENED` on the LCD. If a person is detected together with metal, or if no person is present, the controller keeps the door closed, drives the buzzer alarm in the metal-detected branch, and reports `CLOSED` on the display. Once the permitted entrant leaves the sensing region and the `PIR` input returns low, the program closes the door again by swinging the servo back to `0°`. The simulation, code listing, and breadboard test all confirm the same input-output guard table, making this a compact but explicit guard-driven door-access EFSM.

### 3. 逐句溯源

1. 句子 1：The controller combines a `PIR` sensor, a metal detector, a `PIC16F877A`, a servo motor, an LCD, and a buzzer to supervise a single automatic door.
   对应摘录：A, B
2. 句子 2：Motion detection alone is not enough: the microcontroller only opens the door when the `PIR` input indicates a person and the metal-detector input stays low, which it represents by rotating the servo from `0°` to `180°` and showing `OPENED` on the LCD.
   对应摘录：A, B, C, D
3. 句子 3：If a person is detected together with metal, or if no person is present, the controller keeps the door closed, drives the buzzer alarm in the metal-detected branch, and reports `CLOSED` on the display.
   对应摘录：B, C, D, E
4. 句子 4：Once the permitted entrant leaves the sensing region and the `PIR` input returns low, the program closes the door again by swinging the servo back to `0°`.
   对应摘录：C, D
5. 句子 5：The simulation, code listing, and breadboard test all confirm the same input-output guard table, making this a compact but explicit guard-driven door-access EFSM.
   对应摘录：C, D, E
