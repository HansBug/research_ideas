# FPGA IMPLEMENTATION FOR EFFICIENT LIFT CONTROL SYSTEM - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把八层电梯的请求楼层比较、方向输出、到层停机、超时开门告警和超重停机三类控制情形写成了完整的请求驱动电梯逻辑，但与现有电梯门控簇相似度较高。

## 条目 1: Eight-Floor Lift Request and Alert Controller
- 控制对象：楼宇机电领域的 FPGA 八层电梯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G4 同向优先电梯调度与门控）

### 0. 条目识别与判定
- 一句话说明：这是一个 FPGA 八层电梯控制器，依据请求楼层与当前楼层比较决定上行、下行或停靠，并在超时开门和超重时进入告警停机分支。
- 判断：算。对象是实际楼宇电梯控制系统，原文直接给出了输入输出编码、请求/当前楼层比较规则、三分钟门超时和超重两条异常链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，`ABSTRACT / 1. INTRODUCTION / 4. PROPOSED WORK`，`paper_content.txt` 第 19-25 行、第 31-38 行、第 91-104 行
> With predetermined information inputs and outputs, the FPGA may run across any number of floors while controlling utilisation. By simply altering a control variable in the HDL code, this controller can be utilised for a lift with the needed number of floors.
>
> The goal of an integrated circuit is to create an eight -floor elevator controller ... The elevator determines where to take passengers by comparing the current floor with the desired floor and providing instructions. subject to the conditions that the weight be less than 4500 lbs. and the door close in three minutes. If the weight goes over that limit, the elevator will alert you right away. When the door has been open for more than three minutes, the Door Alert signal ... becomes louder.
>
> we add two new input pins to the code called Over time and Over weight. ... When the controller receives a signal from a weight alert or door alert, the elevator won't move while it's on the Out Current Floor. ... When an elevator is working properly, it compares the Request Floor and Out Current Floor to determine which way to move; however, it activates the Door Alert if a door is left open for longer than three minutes, and it activates the Weight Alert if it is transporting obese passengers.

#### 摘录 B
- 出处：第 2-3 页，`5. BLOCK DIAGRAM / 6. OUTPUTS`，`paper_content.txt` 第 109-117 行、第 133-140 行
> Define Request Floor as an input variable of type 8 -bit. The numbers from 00000001 to 10000000 correspond to the first through eighth floors. ... For In Current _Floor, add a definition for an 8- bit input variable. ... Make Over Time an input variable. The number "1" in the Verilog code denotes that the waiting duration exceeds three minutes. ... Over Weight should be used as the definition of the input variable. In Verilog code, the number "1" denotes an elevator overload.
>
> Provide the name Direction to the output variable. The numbers "1" and "0" in Verilog code represent upward and downward motion, respectively. Provide the value Complete to the output variable. The elevator that enters the designated floor is represented by the number "1" ... In cases when the Over Time or Weight Warning is enabled, it can also be used in place of stopping (remain stationary at the Out Current Floor). It is necessary to set a Door Alert output variable ... Choose Weight Alert as the desired output parameter.

#### 摘录 C
- 出处：第 3 页，`7. THREE CASES OF ELEVATOR`，`paper_content.txt` 第 141-153 行
> Case I- An example of how the elevator usually operates. The elevator will move up if the Request Floor is higher than the R Out Current Floor. If the Request Floor is below the R Out Current Floor, the elevator will depressurize. If the Request Floor equals the R Out Current Floor (it reaches the Request Floor), the R Complete is on, and the elevator stops travelling.
>
> Case II - About three minutes had passed since I last shut the door. Both the R Door Alert and R Complete are set to ON when the Reset is disabled but Over Time is enabled. Off is an option for both the R Weight Alert and R Direction. Information is maintained there by the R Out Current Floor. The elevator will halt (or pause) ...
>
> Case III- Almost 4500 pounds of weight may be supported by the elevator. The R Weight Alert and R Complete are set to be ON if Over Weight is enabled but Reset is disabled. R Door Alert and R Direction are ineffective. To R Out Current Floor, the R Out Current Floor keeps its data. As a result, if an elevator is too full, the weight alert ring will ring and it will stop (or pause) moving.

### 2. 基于原文整理后的自然语言描述

The FPGA lift controller compares `Request Floor` with `Out Current Floor` to drive an eight-floor elevator upward or downward until the requested floor is reached, while floor-encoded sensor inputs and outputs such as `Direction`, `Complete`, `Door Alert`, `Weight Alert`, and `Out Current Floor` expose the controller state to the rest of the device. In normal service, a higher requested floor triggers upward movement, a lower requested floor triggers downward movement, and equality between request and current floor turns `Complete` on and stops travel at the destination. The controller also monitors `Over Time` and `Over Weight` inputs: if the door remains open for more than three minutes or the cabin exceeds the weight limit, it keeps the current-floor value unchanged, suppresses direction changes, and raises the corresponding alert while pausing motion. These normal, door-timeout, and overweight cases together define a request-driven EFSM with two explicit abnormal branches instead of only a single move-to-floor rule.

### 3. 逐句溯源

1. 句子 1：The FPGA lift controller compares `Request Floor` with `Out Current Floor` to drive an eight-floor elevator upward or downward until the requested floor is reached, while floor-encoded sensor inputs and outputs such as `Direction`, `Complete`, `Door Alert`, `Weight Alert`, and `Out Current Floor` expose the controller state to the rest of the device.
   对应摘录：A, B
2. 句子 2：In normal service, a higher requested floor triggers upward movement, a lower requested floor triggers downward movement, and equality between request and current floor turns `Complete` on and stops travel at the destination.
   对应摘录：B, C
3. 句子 3：The controller also monitors `Over Time` and `Over Weight` inputs: if the door remains open for more than three minutes or the cabin exceeds the weight limit, it keeps the current-floor value unchanged, suppresses direction changes, and raises the corresponding alert while pausing motion.
   对应摘录：A, B, C
4. 句子 4：These normal, door-timeout, and overweight cases together define a request-driven EFSM with two explicit abnormal branches instead of only a single move-to-floor rule.
   对应摘录：A, C
