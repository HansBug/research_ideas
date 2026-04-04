# Design and implementation of smart traffic light controller using VHDL language - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口交通灯的模式集合、时序参数、九状态正常灯序、行人请求锁存和故障闪烁模式都写成了可直接恢复的控制链。

## 条目 1: Multi-Mode Traffic Signal and Walk-Request Controller
- 控制对象：道路交通信号领域的四路口交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个基于 FPGA 和 VHDL 的四路口交通灯控制器，负责管理主路、三条支路和行人过街灯的灯色序列、请求保持和定时参数切换。
- 判断：算。对象是实际路口信号控制系统，原文明确给出了模式集合、时间参数、状态序列、传感器 guard、行人请求触发和故障闪烁分支。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，`3. Traffic light controller system design / 3.1. Finite state machines (FSM)`，`paper_content.txt` 第 93-111 行
> Figure 1 illustrates the structure of the selected traffic light model for four road intersections ( one Main Street and three side streets). In general, Traffic Light Controller System consists of three lights (red, green and yellow) in each direction .The red light in dicates to Stop, green light indicates to allow the traffic and yellow light indicates the caution that the traffic is going to be stopped in few seconds. While, turning in yellow and red lights at the same time indicates the caution that the traffic is going to be moving in few seconds . The intersec- tion is fitted with a sensor for side stre et traffic and with walk request button.
>
> This traffic light controller also has provision for walk light ... The design is composed of fini te state ma- chine (FSM), data storage (D_RAM), timer, divider, and va rious synchronizers (latch, and synchronizer).
>
> Finite State Machines (FSM) is the heart of the traffic light controller system. This FSM controls the loading of static data  storage loca- tions with timing parameters, displaying these parameters by reading RAM locations, and the control of the actual traffic lights. There are four timing parameters in this system ... TBASE ... TEXT ... TYEL ... TBLINK. The FSM can execute four functions ... writing new timing pa rameters, reading old timing parameters, running traffic light in normal mode, and running the traffic light in bli nking mode ... the idle state of the FSM is called the reset state ... The system will stay in the reset state until the GO button is pressed.

#### 摘录 B
- 出处：第 3 页，`3.1. Finite state machines (FSM)`，`paper_content.txt` 第 124-135 行
> Using the writing function, the user can specify the any one of the four timing parameters ... For the reading operation, the user can use the same L1 and L0 switches to denote which of the four timing parameters to view on a set Hex -LEDs. In normal mode or blinking mode, the sy stem just cycles through the various traffic light states. The regular controller has been designed with nine states as presented in Table 3 without t aking the traffic sensors and walk request in the point view.
>
> In the normal mode ... the side street has a shorter green interval than the main street, but if there is traffic on the side street when the controller is about to cycle to turn that green light off, it will extend the green light by the sho rter (side street) green inter val. Thus the green light on the side street will stay on until traffic on the side street clears. Traffic sensor switch is u sed to simulate the effect waiting traffic on the side street, the system complies by keeping side street green until the traffic s ensor is switch off. The walk light comes on after the main street yellow interval, and then only if the walk request button has been pushed. Late at night or when something in the system is not working, the light goes into the blinking mode ...

#### 摘录 C
- 出处：第 4 页，`Table 3 / 3.3. Divider, sec_pulse, and timer / 3.4. Latch and sensors`，`paper_content.txt` 第 162-182 行
> Table 3: Operations of Traffic Light Controller System in Normal Mode without Using the Traffic Sensors and Walk Request
> Time Type  Main Street  Side 1 Street  Side 2 Street  Side 3 Street
> TBASE  Green  Red Red Red
> TEXT  Green  Red Red Red
> TYEL  Yellow  Yellow/Red  Red Red
> TBASE  Red Green  Red Red
> TYEL  Red Yellow  Yellow/Red  Red
> TBASE  Red Red Green  Red
> TYEL  Red Red Yellow  Yellow/Red
> TBASE  Red Red Red Green
> TYEL  Yellow/Red  Red Red Yellow
>
> Secpulse component is used to generate one second clock, which is used in the timin g of the traffic light. The timer is implemented as counter.
>
> Walk signal is latched so that when the user pushes the walk button once the signal is queued until the FSM need it. ... there are three traffic sensors which are synchronized by simply passing it through a flip flop.

### 2. 基于原文整理后的自然语言描述

The FPGA traffic controller manages a four-road intersection with one main street, three side streets, walk lights, and side-street sensors, and its control core is an FSM coupled with D_RAM, a timer, a divider, and request/sensor synchronizers. The controller exposes four operator-selectable modes, namely `read`, `write`, `normal`, and `blinking`, stores four timing parameters `TBASE`, `TEXT`, `TYEL`, and `TBLINK`, starts in a `reset` state with all lights off, and waits for the `GO` button before entering the working cycle. In `normal` mode it follows a nine-state signal sequence whose outputs are explicitly tabulated for the main street and three side streets, and when a side-street sensor remains active it extends the side-street green interval instead of immediately switching away. The walk request is latched until it is consumed after the main-street yellow interval, and when the system is put into `blinking` mode it alternates `main yellow + side red` and `main red + side yellow` under the one-second timing pulse rather than executing the normal cycle.

### 3. 逐句溯源

1. 句子 1：The FPGA traffic controller manages a four-road intersection with one main street, three side streets, walk lights, and side-street sensors, and its control core is an FSM coupled with D_RAM, a timer, a divider, and request/sensor synchronizers.
   对应摘录：A
2. 句子 2：The controller exposes four operator-selectable modes, namely `read`, `write`, `normal`, and `blinking`, stores four timing parameters `TBASE`, `TEXT`, `TYEL`, and `TBLINK`, starts in a `reset` state with all lights off, and waits for the `GO` button before entering the working cycle.
   对应摘录：A
3. 句子 3：In `normal` mode it follows a nine-state signal sequence whose outputs are explicitly tabulated for the main street and three side streets, and when a side-street sensor remains active it extends the side-street green interval instead of immediately switching away.
   对应摘录：B, C
4. 句子 4：The walk request is latched until it is consumed after the main-street yellow interval, and when the system is put into `blinking` mode it alternates `main yellow + side red` and `main red + side yellow` under the one-second timing pulse rather than executing the normal cycle.
   对应摘录：B, C
