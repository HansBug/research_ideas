# A New State Machine Behaviour Model for Procedural Control Entities in Industrial Process Control Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文在真实工业气力输送案例中明确给出 `Stopped / Starting / Running / Stopping` 顶层状态、`Running` 与 `Emptying` 的嵌套层次，以及 filling/emptying durative sequence 的处理方式，可直接作为 `HSM + T1` 样本。

## 条目 1: Hierarchical pneumatic-transport procedural controller with durable filling/emptying sequences

- 控制对象：工业气力输送过程控制实体的分层状态机
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向慢响应工业气力输送过程的 procedural controller，用顶层运行态和 `Running` 内部的层次化 filling/venting/emptying 子状态共同组织 ore transport 操作。
- 判断：算。对象是真实工业过程控制器，不是单纯建模方法流程；原文不仅给出层次状态集，还明确说明 filling/emptying 动作序列具有持续时间并需要按子序列推进。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 21-33 行
> State machines are a popular way of modelling the behaviour of systems, including process control systems. ... This paper presents a new state machine behaviour model for procedural control entities in industrial process control systems. The main feature of the new concept of state machine processing is the durability of all action sequences ... The new concept is demonstrated and validated by means of a case study, which addresses a control problem from a real industrial project.

#### 摘录 B

- 出处：第 8-9 页，Section `4.2. Use of the New State Machine Model`，`paper_content.txt` 第 1296-1315 行
> The state machine of the pneumatic transport operation according to the new model is shown in Figure 8. The state machine has typical states of a continuous operation, namely Stopped, Starting, Running, and Stopping. The state Running is a superstate, which is composed of three states, namely elementary states Venting and Filling, and a superstate Emptying ... The Emptying superstate is composed of two states ... Emptying starting and a superstate Emptying running, which is composed of three elementary states, namely Not finished, Wait for finished, and Blowing the chamber.

#### 摘录 C

- 出处：第 10 页，Section `4.4. Comparison of Both State Machine Models`，`paper_content.txt` 第 1394-1404 行
> The first difference is the state Filling (see Figure 8). This state's processing is composed of three parts, each of them having duration. The first part includes the filling starting sequence ... The second part includes waiting for the filling of the chamber to be completed ... Finally, the third part, including the filling stopping sequence, also has a duration ...

### 2. 基于原文整理后的自然语言描述

The case study models a pneumatic-transport controller for moving ground ore from a storage silo into a dosing silo, and its top-level machine uses `Stopped`, `Starting`, `Running`, and `Stopping` as the main operating states. Inside `Running`, the controller is explicitly hierarchical: it decomposes into `Venting`, `Filling`, and an `Emptying` superstate, and `Emptying` further decomposes into `Emptying starting` and `Emptying running`, with the latter split into `Not finished`, `Wait for finished`, and `Blowing the chamber`. Unlike a flat instantaneous state machine, this behavior model is designed for slow industrial processes, so action sequences are durative rather than atomic. Even a state such as `Filling` contains a start sequence, a waiting interval for chamber completion, and a stopping sequence that each take time and must complete before the next part proceeds. The sample is therefore a true process-control `HSM`, because the control semantics depend simultaneously on nested superstates and on the timed completion of physical filling and emptying procedures.

### 3. 逐句溯源

1. 句子 1：The case study models a pneumatic-transport controller for moving ground ore from a storage silo into a dosing silo, and its top-level machine uses `Stopped`, `Starting`, `Running`, and `Stopping` as the main operating states.
   对应摘录：A, B
2. 句子 2：Inside `Running`, the controller is explicitly hierarchical: it decomposes into `Venting`, `Filling`, and an `Emptying` superstate, and `Emptying` further decomposes into `Emptying starting` and `Emptying running`, with the latter split into `Not finished`, `Wait for finished`, and `Blowing the chamber`.
   对应摘录：B
3. 句子 3：Unlike a flat instantaneous state machine, this behavior model is designed for slow industrial processes, so action sequences are durative rather than atomic.
   对应摘录：A, C
4. 句子 4：Even a state such as `Filling` contains a start sequence, a waiting interval for chamber completion, and a stopping sequence that each take time and must complete before the next part proceeds.
   对应摘录：C
5. 句子 5：The sample is therefore a true process-control `HSM`, because the control semantics depend simultaneously on nested superstates and on the timed completion of physical filling and emptying procedures.
   对应摘录：A, B, C
