# Water Tank Level Controller by using PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：上下阈值触发泵/阀动作的控制序列明确，适合直接当成简单控制需求样本。

## 条目 1: Threshold-based refill logic for a two-tank PLC system
- 控制对象：PLC 水箱液位控制系统

### 0. 条目识别与判定

- 一句话说明：这是过程控制领域的 PLC-based water tank level controller，用于依据上下液位阈值控制泵和阀门，从而维持两个水箱的液位。
- 判断：算。对象是实际液位控制系统，原文给出了 lower threshold / higher threshold 触发的泵启停和阀门开关逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Introduction，对 lower/higher threshold control 的说明，行 28-30
> The project “Water Tank Level Controller by using PLC” is designed to monitor and control the level of liquid in the tank. Th e 
> system has associate automatic pumping system hooked up thereto thus on refill the tank once the liq uid gets to the lower threshold, 
> while offing the pump once the liquid gets to the higher threshold. Sustainability of available wate r resources in many reaso ns of the

#### 摘录 B
- 出处：第 3 页，Operation description，对 two-tank sequence 的说明，行 86-103
> When we switch ON the power supply, pump will start pumping the water in tank 2 through tank 1 and c ontrol valve (CV). When 
> upper threshold of tank 2 is achieved then sensor 2 will sense the water level of tank 2. S2 will se nd the signal to the PLC about 
> upper threshold of tank 2. Now, PLC will send the analog signal to the control valve (CV) to interrup t the liquid flow. Then w ater 
> will fill the tank 1. When upper threshold of tank 1 is achieved then sensor 1 will sense the water level of tank 1. S1 will send the 
> signal to the PLC about upper threshold of tank 1. PLC will send the analog signal to the pump. Pump  will stop pumping water to 
> tank. When water from tank 2 is drained out sensor 2 will sense the lower threshold of water level i n tank 2. S2 will se nd the signal 
>
>
> --- Page 4 ---
> International Journal for Research in Applied Science & Engineering Technology (IJRASET ) 
>                                                                                            ISSN: 2321 -9653; IC Value: 45.98; SJ Impact Factor: 7.177  
>                                                                                                                 Volume 7 Issue V, May 2019 - Available at www.ijraset.com  
>      
> ©IJRASET: All Rights are Reserved  
>  2106  to the PLC about lower threshold of tank 2. PLC will send the analog signal to the control valve (CV ) to let the liquid from tank 1 
> flow in tank 2. When lower threshold of tank 1 is achieved then sensor 1 will sense the water level of tank 1.  S1 will send the signal 
> to the PLC about lower threshold of tank 1. PLC will send the analog signal to the pump. Pump will s tart pumping water to tan k. 
> This operation will take place continuously and required result is obtained .

### 2. 基于原文整理后的自然语言描述

The water-tank controller monitors the liquid level and automatically refills the tank when the lower threshold is reached, while switching the pump off when the higher threshold is reached. In the described two-tank sequence, reaching the upper threshold of tank 2 causes the control valve to interrupt the flow, reaching the upper threshold of tank 1 stops the pump, and later lower-threshold events reopen the valve or restart the pump. This operation continues automatically to maintain the required water levels.

### 3. 逐句溯源

1. 句子 1：The water-tank controller monitors the liquid level and automatically refills the tank when the lower threshold is reached, while switching the pump off when the higher threshold is reached.
   对应摘录：A
2. 句子 2：In the described two-tank sequence, reaching the upper threshold of tank 2 causes the control valve to interrupt the flow, reaching the upper threshold of tank 1 stops the pump, and later lower-threshold events reopen the valve or restart the pump.
   对应摘录：B
3. 句子 3：This operation continues automatically to maintain the required water levels.
   对应摘录：B
