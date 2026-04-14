# Towards Safe Autonomous Driving: Model Checking a Behavior Planner during Development - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然以模型检查流程为主，但对工业行为规划器里的 `LCfast` 离散决策链、gap 输入结构、一步一秒的执行节拍和“开灯后等待两步再并线”的换道相位给出了足够强的原文锚点。

## 条目 1: Gap-based LCfast lane-change decision with indicator wait

- 控制对象：高速自动驾驶行为规划器的 `LCfast` 换道决策器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业高速自动驾驶软件栈里的 tactical behavior planner 片段，用 `gap` 结构判断是否发起 `LCfast` 换道，并按离散 planning step 推进指示灯、等待和实际并线阶段。
- 判断：算。对象是实际自动驾驶行为规划器的战术换道逻辑，原文直接给出了 tactical BP 的职责、symbolic transition system 语义、`gap` 输入接口、`LCfast` 输出语义，以及“两步等待后再启动换道”的离散阶段链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，`2 Background`，`paper_content.txt` 第 199-205, 227-229 行
> The plan part can be divided into three steps ... Then, the tactical BP decides between available maneuvers, e.g., lane following or lane change. Finally, the trajectory planner calculates a desired trajectory ...
>
> We focus on the tactical BP ...
>
> A symbolic transition system S = <X, I, T> is a tuple, where X is a set of state variables, I(X) is a formula representing the initial states, and T(X, X') is a formula representing the transitions ...

#### 摘录 B

- 出处：第 8-9 页，`3.2 Environment model / 3.3 The Original and Mock BPs`，`paper_content.txt` 第 446-468, 488-504 行
> The ego vehicle tracks objects in its proximity via so-called gaps ... there can be up to three gaps, one is always in the ego lane, the other two can be in the left or right lane next to ego ... For each car in the gaps, information such as relative distance to ego, velocity and acceleration are stored which can be used by the BP for decision making.
>
> ... the code considered for the actual BP is an excerpt ... containing the logic for a lane change decision towards the “fast” lane (LCfast) ... The interface ... uses the gap structure as input and returns as output the decision whether or not to initiate a lane change towards the fast lane.

#### 摘录 C

- 出处：第 11 页，`Double Merge`，`paper_content.txt` 第 709-775 行
> ... the actual problematic decision already occurs in step 2 where ego decides to change the lane towards the middle, as displayed by the indicators turned on. At this point, ego waits for two steps before actually starting the lane change. During this whole period, the middle lane appears to be free ... When ego actually does the lane change, car 1 happens to finish its own and ends up colliding with ego.
>
> ... Having a more flexible cancellation mechanism, or including cars between a neighboring lane and the one next to that into the gaps, could ... easily avoid this type of issues.
>
> ... the issue is caused by ego not looking further than one lane to the left when deciding to change a lane, and delaying the actual lane change after the decision for 2 steps.

### 2. 基于原文整理后的自然语言描述

The paper targets the industrial tactical behavior planner, the module that sits between strategic routing and trajectory planning and chooses maneuvers such as lane following or lane change from a discrete symbolic transition-system model. In the published case, the analyzed control fragment is the `LCfast` logic, whose input is a `gap` structure covering the ego lane and the available neighbouring lanes; each gap stores the nearest front and rear vehicles together with their relative distance, velocity, and acceleration, and the planner's output is the yes/no decision whether to initiate a lane change toward the fast lane. The decision sequence is not instantaneous: once the planner decides to change lane, the indicators are turned on first, the vehicle waits for two planning steps, and only then does the actual merge start. Because the decision is based only on the neighbouring-lane gap abstraction, the planner can miss a vehicle that merges from two lanes away, which is why the paper explicitly points to a wider gap model or a more flexible cancellation mechanism as the recovery path. Taken together, the published `LCfast` excerpt can be read as an EFSM whose state variables are the gap-derived traffic features and whose discrete phases are `keep lane`, `decision to initiate lane change`, `indicator-on waiting`, `actual merge`, and `cancel / retry` under the one-step-per-second planning rhythm used by the model.

### 3. 逐句溯源

1. 句子 1：The paper targets the industrial tactical behavior planner, the module that sits between strategic routing and trajectory planning and chooses maneuvers such as lane following or lane change from a discrete symbolic transition-system model.
   对应摘录：A
2. 句子 2：In the published case, the analyzed control fragment is the `LCfast` logic, whose input is a `gap` structure covering the ego lane and the available neighbouring lanes; each gap stores the nearest front and rear vehicles together with their relative distance, velocity, and acceleration, and the planner's output is the yes/no decision whether to initiate a lane change toward the fast lane.
   对应摘录：B
3. 句子 3：The decision sequence is not instantaneous: once the planner decides to change lane, the indicators are turned on first, the vehicle waits for two planning steps, and only then does the actual merge start.
   对应摘录：C
4. 句子 4：Because the decision is based only on the neighbouring-lane gap abstraction, the planner can miss a vehicle that merges from two lanes away, which is why the paper explicitly points to a wider gap model or a more flexible cancellation mechanism as the recovery path.
   对应摘录：C
5. 句子 5：Taken together, the published `LCfast` excerpt can be read as an EFSM whose state variables are the gap-derived traffic features and whose discrete phases are `keep lane`, `decision to initiate lane change`, `indicator-on waiting`, `actual merge`, and `cancel / retry` under the one-step-per-second planning rhythm used by the model.
   对应摘录：A, B, C
