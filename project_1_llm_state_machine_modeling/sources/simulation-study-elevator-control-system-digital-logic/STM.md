# A Simulation Study of an Elevator Control System using Digital Logic - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把八层电梯的扫层控制写成“当前楼层 + 呼叫记忆 + 方向记忆 + 上下计数器 + 两级 MUX”的完整控制链，同时明确给出 `10 s` 楼层更新脉冲、`1 s` 比较脉冲和到层服务延迟，足以支撑双 A 的 `EFSM + T1` 样本。

## 条目 1: Call-Memory Eight-Floor Elevator Sweep Controller

- 控制对象：八层电梯的双向扫层与呼叫记忆控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电与电梯控制领域的八层 elevator supervisor，用呼叫记忆、方向选择、楼层比较器和定时脉冲组织“留在本层 / 上移一层 / 下移一层 / 到层服务 / 改变方向”的扫层控制逻辑。
- 判断：算。对象是实际八层电梯控制器，原文先给出 elevator flowchart，再把 `up counter / down counter / MUX / comparator / call memory / direction selector` 逐段实现出来，不是泛泛的数字电路教学背景。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 10-24 行
> This work presents a simulation study of elevator control of an eight storied building.
>
> The probable flow of events associated with movement of an elevator had been inspected and used to create a flow chart for the events. This flow chart had been used to create the logic to control the elevator and finally had been transformed into a digital electronic circuit.
>
> The proposed algorithm is easily scalable to “N” floor elevator system.

#### 摘录 B

- 出处：第 1 页，`II. PROBLEM DEFINITION` 与 `III. OPERATION PRINCIPLE`，`paper_content.txt` 第 51-99 行
> Let a call occurs at some i-th floor. As soon as the call occurs the lift will start upward counting 0-1-2-3-4-5-....-N till it reaches that i-th floor.
>
> ... If the lift has been going upward it will go on moving to i+j-th floor, serve the call, and then change its direction to come back at i-j-th floor to serve call.
>
> After all the calls had been served, if no more call occurs, the elevator will be waiting at its last served floor and will be searching both way (up/down) for new calls.
>
> ... the elevator should check if there is any call at current i-th floor ... depending on the ongoing movement direction ... search for calls in higher (i++) or lower (i--) floors. If no call is found in current movement direction it should change its moving direction and search for calls in opposite way.

#### 摘录 C

- 出处：第 4 页，`D. Shift Registers as Delay/Storage Elements`，`paper_content.txt` 第 276-286 行
> The first 74194 IC ... supplies this value as current i-th floor to the counters with 10 second pulse at clock.
>
> The second 74194 IC works as the supplier of floor number to comparator sub circuit ... Every second it passes on the present floor value ... to the comparators to help them compare and find if there is a new call at any floor.

#### 摘录 D

- 出处：第 4-5 页，`F. Call Memory/Directional Selector`，`paper_content.txt` 第 329-349 行
> This idea had been used to create the call memory and directional selector.
>
> Whenever there is a call for a floor the counter associated with that floor will have a HIGH pulse at clock and will make the LSB equal to 1. But as soon as the call is served a new HIGH pulse to the clock will be sent and LSB will become 0.
>
> Same thing happens for directional selector ... 0 means downward and 1 means upward movement.

#### 摘录 E

- 出处：第 5-6 页，`G. Interconnectors`，`paper_content.txt` 第 385-456 行
> Eight basic switches have been used to generate calls at a floor ... As soon as A=B happens ... XOR output will be 1 which will set 74190 clock input HIGH so the call will be cancelled.
>
> Delay components can be used in between XOR output and clock input so that the elevator gets sometime between reaching the floor with call and cancelling the call by flushing memory; which we could say the serving time.
>
> ... A>B OR’s output 1 means call in any above floor and A<B OR’s output 1 means call in any below floor ... If the AND output is 1 then there is call in either above or below floor so the new floor value that came from up/down counter must be chosen instead of staying at same floor.

### 2. 基于原文整理后的自然语言描述

The controller is an eight-floor elevator EFSM centered on three kinds of state information: the current floor value `i`, a per-floor call-memory bit, and a one-bit movement-direction memory. When a call is latched for some floor, the elevator first checks whether the current floor itself has a pending request; after serving that request and flushing its memory, it searches upward or downward according to the ongoing direction. If a higher or lower pending call exists, the controller uses the up/down counters to propose `i+1` or `i-1` and then lets a pair of multiplexers decide whether to stay on the current floor or move to the next one. The first multiplexer selects between upward and downward stepping according to the direction selector, while the second multiplexer selects between keeping `i` unchanged and committing the new floor according to whether any callable target still exists above or below. Each floor request is stored by a dedicated call-memory latch that is set when the floor switch is pressed and cleared automatically when the comparator reports `A=B`, so request persistence and request flushing are explicit parts of the controller state. The timing is also explicit rather than implicit: one shift-register path advances the floor value with a `10`-second clock pulse, another publishes the present floor to the comparators every second, and extra delay components can hold the elevator at a reached floor long enough to model passenger service time.

### 3. 逐句溯源

1. 句子 1：The controller is an eight-floor elevator EFSM centered on three kinds of state information: the current floor value `i`, a per-floor call-memory bit, and a one-bit movement-direction memory.
   对应摘录：B, D
2. 句子 2：When a call is latched for some floor, the elevator first checks whether the current floor itself has a pending request; after serving that request and flushing its memory, it searches upward or downward according to the ongoing direction.
   对应摘录：B, E
3. 句子 3：If a higher or lower pending call exists, the controller uses the up/down counters to propose `i+1` or `i-1` and then lets a pair of multiplexers decide whether to stay on the current floor or move to the next one.
   对应摘录：B, E
4. 句子 4：The first multiplexer selects between upward and downward stepping according to the direction selector, while the second multiplexer selects between keeping `i` unchanged and committing the new floor according to whether any callable target still exists above or below.
   对应摘录：E
5. 句子 5：Each floor request is stored by a dedicated call-memory latch that is set when the floor switch is pressed and cleared automatically when the comparator reports `A=B`, so request persistence and request flushing are explicit parts of the controller state.
   对应摘录：D, E
6. 句子 6：The timing is also explicit rather than implicit: one shift-register path advances the floor value with a `10`-second clock pulse, another publishes the present floor to the comparators every second, and extra delay components can hold the elevator at a reached floor long enough to model passenger service time.
   对应摘录：C, E
