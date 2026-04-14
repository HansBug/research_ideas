# Development of an Automatic Door Controller for a Smart Building - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把人感 + 距离门控条件、开门/关门输出、引脚映射和结果表都写得完整，可直接整理成门控 EFSM。

## 条目 1: PIR-and-ultrasonic sliding-door controller
- 控制对象：基于 PIR 与超声波传感器的智能楼宇自动滑门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的 automatic sliding-door controller，用人体运动检测和距离测量联合决定门是打开还是保持/回到关闭状态。
- 判断：算。对象是实际自动门控制系统，原文给出了传感输入、门控 guard、开关门输出、程序逻辑、引脚分配和结果表。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract 与 Introduction，对输入条件与输出动作的说明，行 17-27、81-93
> The work uses a microcontroller ATmega 328P to design an automatic door controller.
> The design employs a passive infrared sensor to sense the approaching human towards the door.
> It incorporates an ultrasonic sensor to calculate the distance between it and the body.
> As the distance is between 10cm and 60cm, a control signal is initiated from FMOTOR (pin8) ...
> A close door signal from RMOTOR (pin9) also closes the sliding door if the conditions are not met.
> ...
> the two situations are ANDed by using C programming language.
> The result is the opening of the door ... with the sounding of a tone for a second while operational status is displayed on a 16 × 2 liquid crystal display.

#### 摘录 B
- 出处：第 2-5 页，Materials and Method 与 Programming，对逻辑与引脚的说明，行 95-114、233-277
> Passive infrared and ultrasonic sensors are used as intelligent sensors that sense human presence and determine his or her proximity to the door.
> Coding is achieved using C programming language ... using IF, AND, OR and relational functions to produce a HIGH of +5V when true.
> ...
> Motor forward and reverse control signals are obtained from pins 8 and 9 respectively.
> A HIGH (+5V) signal after human detection is obtained at HpirSensor realized with pin2.
> The logical expression used to operate the door is an IF, else statement:
> if((distance>=60||distance<=10)&&(vald=LOW)),
> the door should remain closed else it should be opened.
> ...
> #define FMOTOR 8
> #define RMOTOR 9
> #define HpirSensor 2

#### 摘录 C
- 出处：第 7-8 页，Results and Discussion 与 Conclusion，行 334-345、369-375
> any distance outside the 10cm to 60cm range, the door remains closed while targets within the range allow the door to open.
> ...
> It is of note that the door will only open if there is human movement and the distance of the sensed person is within 10cm to 60cm.

#### 摘录 D
- 出处：第 7 页，Table 1，对门状态结果的说明，行 347-360
> Distance (cm)  Q1 Input  Q2 Input  Q1 Collector  Q2 Collector  Door
> 5 ... Closed
> 10 ... Opened
> 20 ... Opened
> 30 ... Opened
> 40 ... Opened
> 50 ... Opened
> 60 ... Opened
> 70 ... Closed
> 80 ... Closed
> 90 ... Closed
> 100 ... Closed

### 2. 基于原文整理后的自然语言描述

The smart-building door controller combines a PIR sensor with an ultrasonic sensor so that the system reacts only when a person is both detected and located within the permitted approach range. The ultrasonic measurement and human-motion signal are combined in software, and if the sensed person is within `10 cm` to `60 cm`, the controller drives `FMOTOR` to operate the relay and open the sliding door; otherwise `RMOTOR` is driven so that the door stays closed or moves back to the closed direction. The implementation maps the motion signal to `HpirSensor` on pin `2`, the forward motor signal to pin `8`, and the reverse motor signal to pin `9`, and expresses the decision as an `if` / `else` condition over distance and motion. The results table confirms that distances `10-60 cm` map to the opened state while distances outside that interval map to the closed state. The conclusion restates the same guard: the door opens only when human movement is present and the sensed person is within the `10-60 cm` range.

### 3. 逐句溯源

1. 句子 1：The smart-building door controller combines a PIR sensor with an ultrasonic sensor so that the system reacts only when a person is both detected and located within the permitted approach range.
   对应摘录：A, B
2. 句子 2：The ultrasonic measurement and human-motion signal are combined in software, and if the sensed person is within `10 cm` to `60 cm`, the controller drives `FMOTOR` to operate the relay and open the sliding door; otherwise `RMOTOR` is driven so that the door stays closed or moves back to the closed direction.
   对应摘录：A, B, C
3. 句子 3：The implementation maps the motion signal to `HpirSensor` on pin `2`, the forward motor signal to pin `8`, and the reverse motor signal to pin `9`, and expresses the decision as an `if` / `else` condition over distance and motion.
   对应摘录：B
4. 句子 4：The results table confirms that distances `10-60 cm` map to the opened state while distances outside that interval map to the closed state.
   对应摘录：C, D
5. 句子 5：The conclusion restates the same guard: the door opens only when human movement is present and the sensed person is within the `10-60 cm` range.
   对应摘录：C
