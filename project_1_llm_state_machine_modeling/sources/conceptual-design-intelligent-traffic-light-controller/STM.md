# Conceptual Design of Intelligent Traffic Light Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把主干道/支路相位、左转跳过条件、Moore 机输出规则和 `12` 个状态编码都交代得较清楚，可以直接整理成交通灯相位状态机样本。

## 备注

- `Figure 1` 的状态图主体以图形方式给出，`paper_content.txt` 没有完整展开图内全部文字；当前条目以正文中对主/支路、左转检测、状态个数和各方向绿灯所在状态的文字说明为主，必要时可回 `paper.pdf` 对照状态图。

## 条目 1: Twelve-State Moore Traffic-Light Controller with Left-Turn Skip

- 控制对象：主干道/支路路口的智能交通灯相位控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的路口相位控制器，用主干道/支路分级、左转感应线圈和 `12` 个离散状态组织各方向绿灯输出。
- 判断：算。对象是实际交通灯控制系统，原文直接给出了主/支路设定、左转跳过规则、Moore 机判定、状态数以及若干方向灯在特定状态下点亮的条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`2. Traffic Light Model`，`paper_content.txt` 第 35-55 行
> We consider an intersection of two roads and a controllable traffic light system is in charge of the lights on all of the intersection corners. In Israel most of the major roads are North-South; therefore we consider the North-South road as the major road and the East-West road as a minor road. Accordingly, we gave the North-South road triple time period.
>
> ... we consider Inductive Detector Loops installed under of the left turn lanes pavement. If the detector does not indicate a vehicle in the turn left lane, the green light for this turn will be skipped in this iteration. The state machine for this traffic light is depicted in Figure 1.

#### 摘录 B

- 出处：第 2 页，`3. Controlling the Lights According to the States`，`paper_content.txt` 第 64-77 行
> The lights are decided only according to the states. The inputs from the Inductive Detector Loops have an effect only on the next state decision. This is actually the different of Mealy machines and Moore machines. ... our machine is a Moore machine.
>
> ... we have 12 states numbered from 0 to 11, so we need ⌈log2 12⌉ flip-flops to implement this state machine i.e., we need four flip-flops. We have denoted these flip-flops as A, B, C, D.

#### 摘录 C

- 出处：第 3-7 页，方向灯实现说明，`paper_content.txt` 第 112-115 行、第 182-200 行、第 245-248 行
> The traffic light of the East-South direction is much easier, because it has a green light only when the state is "1".
>
> The traffic light of the North-East direction ... has a green light only when the state is "5".
>
> The traffic light for the West-East direction is fairly similar to the traffic light of the East-West direction. They gives a green light in the same states, except of state "1" that was replaced by state "7" in the West-East direction.
>
> ... the traffic light of the West-North direction ... has a green light only when the state is "7".

### 2. 基于原文整理后的自然语言描述

The controller models a two-road intersection in which the North-South main road receives a longer service period than the East-West minor road. It is implemented as a `12`-state Moore FSM, so the lamp outputs are determined only by the current state while inductive-loop inputs in the left-turn lanes influence only which state is selected next. The state set encodes both straight-through and turning movements for the different approaches, with some signal heads becoming green only in designated states such as East-South in state `1`, North-East in state `5`, and West-North in state `7`. If no vehicle is detected in a left-turn lane, the controller skips that left-turn green state in the current iteration instead of serving it unconditionally.

### 3. 逐句溯源

1. 句子 1：The controller models a two-road intersection in which the North-South main road receives a longer service period than the East-West minor road.
   对应摘录：A
2. 句子 2：It is implemented as a `12`-state Moore FSM, so the lamp outputs are determined only by the current state while inductive-loop inputs in the left-turn lanes influence only which state is selected next.
   对应摘录：A, B
3. 句子 3：The state set encodes both straight-through and turning movements for the different approaches, with some signal heads becoming green only in designated states such as East-South in state `1`, North-East in state `5`, and West-North in state `7`.
   对应摘录：C
4. 句子 4：If no vehicle is detected in a left-turn lane, the controller skips that left-turn green state in the current iteration instead of serving it unconditionally.
   对应摘录：A
