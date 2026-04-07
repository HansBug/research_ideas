# The automatic and manual railroad door systems based on IoT - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路道口栏门的自动/手动两种控制模式、红外触发、Web 服务器联动、手机端 override 和响应时延测试写得很完整，可稳定支撑双 A 样本。

## 条目 1: Infrared-Automatic and Smartphone-Manual Crossing-Gate Controller

- 控制对象：轨道交通与铁路控制领域的 IoT 道口栏门自动/手动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个铁路道口栏门控制系统，用红外传感器负责自动开闭闸，Web 服务器和 Android 手机负责人工远程 override，CCTV 提供实时监控。
- 判断：算。对象是真实铁路道口门控系统，原文明确区分了 automatic / manual 两种控制模式，并给出了输入组件、执行输出、网络联动链和红外/视频响应时延。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 21-36 行
> The automatic and manual IoT-based rail door ... is a door bar designed to be able to close and open automatically and manually. The automatic system works based on sensors that detect the presence of trains and system manual works based on the open and Close button on the smartphone. The components to be used are ATmega328 microcontrollers, Infrared sensors, power supply, CCTV and android applications. Infrared sensor will detect the presence of the train and the gate will close automatically. Then the doorway will open when the train has crossed the automatic door bar. By the manual way, rail door control can be open and closed with android smartphones in real-time with graphical display provided by CCTV.

#### 摘录 B

- 出处：第 2 页，`2.1 Block diagram`，`paper_content.txt` 第 81-95 行
> The diagram block of the system is found in Figure 1. ... Broadly, the system is divided into three parts: input, process data/program, and output. The input section consists of Infrared and CCTV Camera. Meanwhile, the output consists of servo Motor as the Mobilizer and Buzzer. As for the process of using an ATmega microcontroller 328 combined with the W5100 Ethernet module, it is used as the main control for processing data programs. Switch Hub and Router are used as Monitoring and control globally with the Internet. ... If the data is valid, the microcontroller will provide an execution order to the servo motor to open the train door bar. As for the manual way, CCTV will display the train door crossbar in real-time in mobile Android where the settings buttons open close the train door manually and can be moved automatically.

#### 摘录 C

- 出处：第 4-5 页，`3. RESULTS AND DISCUSSION`，`paper_content.txt` 第 183-199 行
> Automated process, infrared is placed in the section before the train door as a detector or reader when the train passes. When Infrared detects a car, the door of the train will close and open the door, Infrared will send data to the controller to be identified. When the data is valid, the controller will emit output to keep the door closed and open using the servo motor. Manual process, the controller will send IP statically to the global server in order to access via global network or internet and will be displayed with Android Smartphone media in the form of CCTV camera and servo motor drive button or the railway door.
>
> Infrared is used as a media detector where doors will open or close ... Servo Motor as an automatic gate drive ... Web Server as a global network to manually control the door of the train and also display it via CCTV.

#### 摘录 D

- 出处：第 5-7 页，`3.1 Transmitting data test / 3.2 Infrared test / 3.3 CCTV test`，`paper_content.txt` 第 241-255 行、第 262-300 行、第 309-346 行
> The result of the Table 1 shows that data transmission is very consistent and fixed i.e. every 1 second per data. The Web Server responds less than 1 second to any data transmission done in the table above.
>
> Infrared 1 gives the signal to the servo to close the gate ... average train takes time ... 0.687 /second. On Infrared 1, the System program does not use the delay at all. On Infrared 2 gives the signal to the servo to open the gate ... 3.449 / second. On Infrared 2, program on the system using the delay 1.5 second.
>
> CCTV displays realtime graphics on the average rail door takes time ... 0.857 /second.

### 2. 基于原文整理后的自然语言描述

The railroad-door controller has two top-level operating paths: an automatic path driven by infrared train detection and a manual path driven by smartphone commands through an Internet-connected web server. Its input chain combines infrared sensors and CCTV, the processing layer uses an `ATmega328` plus `W5100` Ethernet module, and the output layer drives a servo barrier together with buzzer-based warnings. In the automatic path, a valid infrared detection event is sent to the controller so the servo closes the gate for an approaching train and reopens it after the train has crossed, whereas in the manual path the controller exposes open and close commands together with live CCTV monitoring to an Android client. The implementation also reports timing evidence for the control cycle: server communication responds in less than `1` second, the first infrared path closes the gate with an average response of about `0.687 s`, and the second infrared path reopens the gate with an average response of about `3.449 s` because that branch includes a programmed `1.5 s` delay.

### 3. 逐句溯源

1. 句子 1：The railroad-door controller has two top-level operating paths: an automatic path driven by infrared train detection and a manual path driven by smartphone commands through an Internet-connected web server.
   对应摘录：A, B
2. 句子 2：Its input chain combines infrared sensors and CCTV, the processing layer uses an `ATmega328` plus `W5100` Ethernet module, and the output layer drives a servo barrier together with buzzer-based warnings.
   对应摘录：A, B
3. 句子 3：In the automatic path, a valid infrared detection event is sent to the controller so the servo closes the gate for an approaching train and reopens it after the train has crossed, whereas in the manual path the controller exposes open and close commands together with live CCTV monitoring to an Android client.
   对应摘录：A, B, C
4. 句子 4：The implementation also reports timing evidence for the control cycle: server communication responds in less than `1` second, the first infrared path closes the gate with an average response of about `0.687 s`, and the second infrared path reopens the gate with an average response of about `3.449 s` because that branch includes a programmed `1.5 s` delay.
   对应摘录：D
