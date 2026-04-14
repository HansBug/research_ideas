# Development of an Automatic Door Controller for a Smart Building - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接给出 `PIR + ultrasonic + IF/else` 的门控逻辑、`FMOTOR/RMOTOR` 输出和开闭结果表，可以稳定恢复成带数值 guard 的自动门控制链。

## 条目 1: PIR-and-Ultrasonic Sliding-Door Controller

- 控制对象：楼宇机电与门控领域的滑动自动门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个智能楼宇滑动门控制器，用 `PIR` 检测人员接近、用超声测距判断人与门之间的距离，并据此驱动继电器与 `DC` 电机执行开门或关门。
- 判断：算。对象是实际门控系统而不是感知演示，原文明确给出输入传感器、数值 guard、输出引脚、继电器方向和结果表，足以形成高质量 `EFSM + T0` 样本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 17-27 行
> Smart building and Building automation systems (BAS) have gained popularity in recent times. An automatic system furnishes comfort and saves time. The paper discusses a smart system applied to a building. The work uses a microcontroller ATmega 328P to design an automatic door controller. The design employs a passive infrared sensor to sense the approaching human towards the door. It incorporates an ultrasonic sensor to calculate the distance between it and the body. As the distance is between 10cm and 60cm, a control signal is initiated from FMOTOR (pin8) to drive an electronic switch having a relay as load. A close door signal from RMOTOR (pin9) also closes the sliding door if the conditions are not met. Both switches have relays as their loads and their contact sets control a geared 12V DC motor in forward (Door open) and reverse (Door Close) rotational directions.

#### 摘录 B

- 出处：第 2 页，`Materials and Method`，`paper_content.txt` 第 95-118 行
> The heart of the system is a microcontroller implemented with an 8-bit ATmega 328P (Figure 1). Passive infrared and ultrasonic sensors are used as intelligent sensors that sense human presence and determine his or her proximity to the door. Coding is achieved using C programming language (Akinwole, 2020), the code using IF, AND, OR and relational functions to produce a HIGH of +5V when true. The latter is used to drive an electronic switch achieved with NPN bipolar transistor 2N2222 having a 12V relay as load ... An untrue state drives another electronic switch. The relay’s contact sets are wired in series with a DC motor that provides a rotational motion for the door mechanism. A switch provides forward rotation while the other furnishes a reverse motion, an action that depends on which one receives signals from the microcontroller.

#### 摘录 C

- 出处：第 5 页，`Programming`，`paper_content.txt` 第 233-250, 262-267 行
> With the aid of flowchart in figure 5 which diagrammatically represent the order of activities used to design the system ... Ultrasonic pins are Trig and Echo pins ... Motor forward and reverse control signals are obtained from pins 8 and 9 respectively. A HIGH (+5V) signal after human detection is obtained at HpirSensor realized with pin2. The logical expression used to operate the door is an IF, else statement:
>
> if((distance>=60||distance<=10)&&(vald=LOW)),
>
> the door should remain closed else it should be opened.

#### 摘录 D

- 出处：第 7-8 页，`Results and Discussion / Conclusions`，`paper_content.txt` 第 334-357, 369-375 行
> The result of the design is as summarized in Table 1 below, any distance outside the 10cm to 60cm range, the door remains closed while targets within the range allow the door to open.
>
> Distance (cm)  Q1 Input  Q2 Input  Q1 Collector  Q2 Collector  Door
> 5 Low High High Low Closed
> 10 High Low Low High Opened
> 20 High Low Low High Opened
> 30 High Low Low High Opened
> 40 High Low Low High Opened
> 50 High Low Low High Opened
> 60 High Low Low High Opened
> 70 Low High High Low Closed
> 80 Low High High Low Closed
> 90 Low High High Low Closed
> 100 Low High High Low Closed
>
> The work has been able to systematically explain the development of an automatic door controller for a smart building. It is of note that the door will only open if there is human movement and the distance of the sensed person is within 10cm to 60cm.

### 2. 基于原文整理后的自然语言描述

The smart-building door controller is implemented on an `ATmega 328P` and combines a `PIR` human-presence detector with an ultrasonic distance sensor to decide whether the sliding door should open or remain closed. Its control logic is guard-driven rather than purely sequential: the program evaluates human detection together with the measured distance, and only when the sensed person is within the admitted `10 cm` to `60 cm` range does the controller assert `FMOTOR` on pin `8` to energize the relay path for door opening. When those conditions are not met, the complementary `RMOTOR` signal on pin `9` drives the reverse relay path so that the geared `12 V DC` motor closes the door instead. The same controller therefore maps sensor conditions to two mutually exclusive motor directions, with forward rotation denoting `Door open` and reverse rotation denoting `Door close`. The published result table confirms that distances `10/20/30/40/50/60 cm` produce the open branch while `5/70/80/90/100 cm` stay on the closed branch, and the conclusion reiterates that opening also requires human movement rather than distance alone.

### 3. 逐句溯源

1. 句子 1：The smart-building door controller is implemented on an `ATmega 328P` and combines a `PIR` human-presence detector with an ultrasonic distance sensor to decide whether the sliding door should open or remain closed.
   对应摘录：A, B
2. 句子 2：Its control logic is guard-driven rather than purely sequential: the program evaluates human detection together with the measured distance, and only when the sensed person is within the admitted `10 cm` to `60 cm` range does the controller assert `FMOTOR` on pin `8` to energize the relay path for door opening.
   对应摘录：A, C, D
3. 句子 3：When those conditions are not met, the complementary `RMOTOR` signal on pin `9` drives the reverse relay path so that the geared `12 V DC` motor closes the door instead.
   对应摘录：A, C
4. 句子 4：The same controller therefore maps sensor conditions to two mutually exclusive motor directions, with forward rotation denoting `Door open` and reverse rotation denoting `Door close`.
   对应摘录：A, B
5. 句子 5：The published result table confirms that distances `10/20/30/40/50/60 cm` produce the open branch while `5/70/80/90/100 cm` stay on the closed branch, and the conclusion reiterates that opening also requires human movement rather than distance alone.
   对应摘录：D
