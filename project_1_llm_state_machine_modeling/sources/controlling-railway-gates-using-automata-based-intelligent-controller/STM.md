# Controlling Railway Gates Using Automata Based Intelligent Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅说明了 GPS + UART 8051 的道口门控链，还把核心控制逻辑显式写成 DFA 的状态集、字母表和转移函数，原文可追溯性足够强。

## 条目 1: DFA-Based Gate Closing and Reopening Cycle

- 控制对象：铁路平交口自动栏杆门控控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向铁路道口的自动栏杆控制器，用 GPS、网关和 UART 8051 微控制器驱动红/绿信号与闸门开闭，并把主控制链显式建模成 DFA。
- 判断：算。对象是实际道口门控系统，原文既给出系统级输入输出流程，也给出有限状态机的状态集、字母表和具体转移链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`IV.A Procedure`，`paper_content.txt` 第 209-236 行
> Our proposed work deals with RGCS and automata. ... The GPS based embedded automata is installed in the train. The GPS tracks the location of the train in real time. ... The GPS receiver receives the signal and the GPS transmitter transmits the signal serially to the gateway controller by UART 8051 microcontroller. Hence, the UART 8051 receives the signal and red light is generated, which results in closing the gate. After the train crosses `500 m` away from the railway gate, green light is indicated and the gate opens for the vehicles and people passing by. This method will be carried on after each train passes.

#### 摘录 B

- 出处：第 4 页，`IV.C Sensor Calculation / Algorithm 1`，`paper_content.txt` 第 271-301 行
> Take `fn` as finite set of non-empty states that includes `sens`, `cont`, `circ`, `dist`, `clos`, `open`, `buzz`, `ligh`, `dead` ... Take `fi` as finite set of alphabets that includes `s`, `c`, `d`, `l`, `g`, `b`, `cl` ...
>
> `T` is the finite set of final state = `{clos, open}` ... `Trans : sens * s -> cont`; `Trans : cont * c -> dist`; `Trans : dist * d -> circ`; `Trans : circ * g -> open`; `Trans : circ * l -> ligh`; `Trans : ligh * cl -> clos`; `Trans : clos * cl -> clos`.

### 2. 基于原文整理后的自然语言描述

The railway gate controller automates a level-crossing barrier by combining train-side GPS, a gateway controller, and a UART `8051` microcontroller instead of relying on a manual gatekeeper. At system level, the GPS receiver and transmitter pass train-location information to the `8051`; when the train approaches the crossing, the controller raises a red signal and closes the gate, and once the train has moved `500 m` beyond the crossing it switches to green and reopens the gate. The core control logic is modeled as a DFA whose state set includes sensing, controller, distance, circuit, close, open, buzzer, light, and dead states, and whose final states are `clos` and `open`. Its transition chain advances from `sens` to `cont` to `dist` to `circ`, then branches to `open` on the safe-distance condition or through `ligh` into `clos` when gate closure is required, with `clos` remaining closed under repeated close input.

### 3. 逐句溯源

1. 句子 1：The railway gate controller automates a level-crossing barrier by combining train-side GPS, a gateway controller, and a UART `8051` microcontroller instead of relying on a manual gatekeeper.
   对应摘录：A
2. 句子 2：At system level, the GPS receiver and transmitter pass train-location information to the `8051`; when the train approaches the crossing, the controller raises a red signal and closes the gate, and once the train has moved `500 m` beyond the crossing it switches to green and reopens the gate.
   对应摘录：A
3. 句子 3：The core control logic is modeled as a DFA whose state set includes sensing, controller, distance, circuit, close, open, buzzer, light, and dead states, and whose final states are `clos` and `open`.
   对应摘录：B
4. 句子 4：Its transition chain advances from `sens` to `cont` to `dist` to `circ`, then branches to `open` on the safe-distance condition or through `ligh` into `clos` when gate closure is required, with `clos` remaining closed under repeated close input.
   对应摘录：B
