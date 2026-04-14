# Control System Design for Water Pump Activation in PLC-based Smart Hydroponic Design - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把光照触发、五点传感冗余、PLC OR 逻辑、自保持和手动互锁写成一条完整水泵启停控制链，并给出 `08:00 AM-04:00 PM` 的实际激活窗口。

## 条目 1: Sunlight-Sensed Pump Activation with Five-Sensor Redundancy

- 控制对象：智能水培系统中的 PLC 水泵启停控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个水培灌溉场景下的水泵启停控制器，用 LDR 传感器、继电器接口和 PLC 梯形图决定水泵是否在高蒸发条件下工作。
- 判断：算。对象是实际水培系统控制器，原文给出了传感器电路、5 路输入、OR 逻辑、自保持、手动互锁以及“至少 1 个传感器亮则泵继续运行”的明确控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract / I. INTRODUCTION`，`paper_content.txt` 第 63-75 行、第 149-164 行
> This study aims to design and test a PLC-based automation system for the purposes of setting the activation of a water pump in a hydroponic system based on the sunlight conditions in the hydroponic installation being built. By using a light sensor (LDR) to measure the intensity of sunlight in the hydroponic system being built, the activation of the pump motor can be controlled through the use of a PLC device that processes the information obtained from the sensor used. The results of the tests carried out provide information that the designed system has proven effective for use in hydroponic systems with pump water regulation time from 08:00 AM to 04:00 PM.
>
> Generally, practitioners engaged in hydroponics use a timer component to turn on and turn off the water pump ... the timer does not know other times to turn off or turn on the pump based on the surrounding environment.

#### 摘录 B

- 出处：第 4-6 页，`Sensor Design / Sensor and PLC Interface Design / PLC Control Design`，`paper_content.txt` 第 347-354 行、第 437-474 行
> The sensor circuit in Figure 6 works with the principle of activation based on the light intensity hitting the LDR component ... The PLC device uses this high logic as an input signal to be processed as an instruction that controls the activation of the water pump motor.
>
> The design of the control system in this study is to use a PLC device that is connected to five sensor outputs ... Since the control system in this study uses five sensors and the requirement condition for the pump motor to be activated is that one or more sensors detect the intensity of sunlight, thus the control program used on the PLC device (ladder diagram) is built using the OR logic gate principle ... The 100.00 coil in Figure 8 functions as Power Memory ... As a manual control feature ... the ladder diagram that is built is given an interlock circuit feature.

#### 摘录 C

- 出处：第 6-7 页，`IV. RESULTS AND DISCUSSION`，`paper_content.txt` 第 520-523 行、第 614-624 行
> it is known that the sensor circuit will be active when the sun is partially shining and shining brightly, namely from 08:00 AM to 4:00 PM as shown in the experimental results in Table 1.
>
> all sensors used are in active condition ... the output contacts for the pump motor to also become active ... the pump motor remains active even though there is only one active sensor. The pump motor will not activate when none of the sensors is active or when the Power Off switch is activated even though all sensors are active.

### 2. 基于原文整理后的自然语言描述

The hydroponic pump controller uses LDR-based sensor circuits to convert strong sunlight into high PLC input signals so the pump only runs under evaporation-relevant conditions rather than under a fixed all-day timer. Five sensor channels are deployed around the installation, and the PLC ladder keeps the pump output active whenever at least one sensor still reports sufficient light. The ladder also includes a `100.00` power-memory self-holding bit and a manual interlock, so the automation can stay latched during normal operation but can still be disabled deliberately when manual control is needed. In the reported tests, the control window aligns with sunny conditions around `08:00 AM` to `04:00 PM`, while the pump stays off if no sensor is active or if the `Power Off` branch is asserted.

### 3. 逐句溯源

1. 句子 1：The hydroponic pump controller uses LDR-based sensor circuits to convert strong sunlight into high PLC input signals so the pump only runs under evaporation-relevant conditions rather than under a fixed all-day timer.
   对应摘录：A, B
2. 句子 2：Five sensor channels are deployed around the installation, and the PLC ladder keeps the pump output active whenever at least one sensor still reports sufficient light.
   对应摘录：B, C
3. 句子 3：The ladder also includes a `100.00` power-memory self-holding bit and a manual interlock, so the automation can stay latched during normal operation but can still be disabled deliberately when manual control is needed.
   对应摘录：B
4. 句子 4：In the reported tests, the control window aligns with sunny conditions around `08:00 AM` to `04:00 PM`, while the pump stays off if no sensor is active or if the `Power Off` branch is asserted.
   对应摘录：A, C
