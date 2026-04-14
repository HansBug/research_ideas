# A Reconfigurable Control Mechanism for Smart Traffic Management for Highly Congested Route - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把主路/支路交通灯控制写成 Mealy `FSM` 与 Verilog 状态转移代码，默认优先、传感器触发和可配置延时都很完整。

## 备注

- `paper_content.txt` 中状态表受 OCR 影响把最后一行打成了 `S5 R Y`，但同页 Verilog `state definition` 与后续 `case` 语句都明确最后一态是 `S4`；下文按代码口径整理。

## 条目 1: Highway-Priority Mealy Traffic Controller

- 控制对象：道路交通信号控制领域的主路优先/支路请求交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用于主干道与乡村支路交叉口的 Mealy 交通灯控制器，默认保持主路绿灯，并在检测到支路来车时通过黄灯/全红/放行/回切序列切换。
- 判断：算。对象是实际路口信号控制器，原文同时给出控制规格、状态表、延时常量和完整 Verilog 状态转移代码。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract 与 Introduction，`paper_content.txt` 第 9-18、49-60 行
> This paper consists of an efficient design of a reconfigurable Traffic Control System ... designed in VLSI using Finite State Machines
> ...
> The basis of the traffic light controller is the FSM which stands for Finite State Machines.
> ...
> In this paper, we have developed a real traffic control system using Mealy state machines. The design is implemented in Verilog HDL

#### 摘录 B

- 出处：第 3 页，Section 2.1 `Design`，`paper_content.txt` 第 100-114 行
> The traffic signal for the main highway/line gets highest priority because cars are continuously present on the main highway. Thus, the main highway signal remains green by default.
> Occasionally or in emergency, cars from the country road arrive at the traffic signal. The traffic signal for the country road must turn green only long enough to let the cars on the country road go.
> As soon as there are no cars on the country road, the country road traffic signal turns yellow and then red and simultaneously highway traffic signal glows green.
> There is a sensor to detect cars waiting on the country road. The sensor sends a signal X as input to the controller. X=1, then there are cars on the country road; otherwise X=0.
> There are delays on transition from S1 to S2, S2 to S3, S3 to S4 and S4 to S0

#### 摘录 C

- 出处：第 5-7 页，`Program for Traffic Light/Signal Control`，`paper_content.txt` 第 163-172、199-255 行
> `defineS03'd0  //GREENRED
> `defineS13'd1  //YELLOWRED
> `defineS23'd2  //REDRED
> `defineS33'd3  //REDGREEN
> `defineS43'd4  //REDYELLOW
> ...
> `define Y2RDELAY 3
> `define R2GDELAY 2
> ...
> `S0: if( X) next_state = `S1; else next_state=`S0;
> `S1 : begin repeat(`Y2RDELAY) @ (posedge clock); next_state =`S2; end
> `S2: begin repeat (`R2GDELAY) @ (posedge clock); next_state=`S3; end
> `S3: if( X) next_state=`S3; else next_state=`S4;
> `S4: begin repeat (`Y2RDELAY) @(posedge clock); next_state = `S0; end

### 2. 基于原文整理后的自然语言描述

The controller manages a junction between a main highway and a country road, and its default condition is to keep the highway green while the country road stays red. When sensor `X` reports that cars are waiting on the country road, the FSM leaves `S0` and enters `S1`, where the highway turns yellow while the country road remains red, and after `Y2RDELAY` it advances to `S2`, the all-red transition state. After `R2GDELAY`, the controller reaches `S3`, where the country road gets green and continues to hold that state as long as `X` remains true. Once the country-road demand disappears, the machine goes to `S4`, which turns the country road yellow for another `Y2RDELAY`, and then it returns to `S0` to restore highway priority. Because the design is implemented as a Mealy controller with explicit delay constants and clocked `repeat(...)` waits, both phase ordering and phase dwell are directly encoded in the state transition logic.

### 3. 逐句溯源

1. 句子 1：The controller manages a junction between a main highway and a country road, and its default condition is to keep the highway green while the country road stays red.
   对应摘录：A, B, C
2. 句子 2：When sensor `X` reports that cars are waiting on the country road, the FSM leaves `S0` and enters `S1`, where the highway turns yellow while the country road remains red, and after `Y2RDELAY` it advances to `S2`, the all-red transition state.
   对应摘录：B, C
3. 句子 3：After `R2GDELAY`, the controller reaches `S3`, where the country road gets green and continues to hold that state as long as `X` remains true.
   对应摘录：B, C
4. 句子 4：Once the country-road demand disappears, the machine goes to `S4`, which turns the country road yellow for another `Y2RDELAY`, and then it returns to `S0` to restore highway priority.
   对应摘录：B, C
5. 句子 5：Because the design is implemented as a Mealy controller with explicit delay constants and clocked `repeat(...)` waits, both phase ordering and phase dwell are directly encoded in the state transition logic.
   对应摘录：A, C
