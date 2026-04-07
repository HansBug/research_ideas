# Robot excavation and manipulation of geometrically cohesive granular media - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把机器人在 excavation zone 与 deposition zone 之间的挖掘、运输、寻堆、沉积和返回循环写成了由光源、RGB、ArduCAM、antenna 和 jaws 感知驱动的完整 `FSM`。

## 条目 1: Excavation-Transport-Deposit Robot FSM

- 控制对象：几何黏聚颗粒物挖掘机器人的循环任务监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是通用控制与机器人施工领域的 excavation robot supervisor，用固定光源、RGB 颜色检测、ArduCAM pile search、antenna sensing 和 jaws 状态在 excavate、transport、deposit、return 各阶段间切换。
- 判断：算。对象是实际机器人任务控制器，原文明确给出了 FSM 目标、阶段循环、关键触发和感知驱动的转移条件，不是只在图中暗示“有状态机”。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`arena and FSM overview`，`paper_content.txt` 第 167-180 行
> The robot operates within a constructed “arena” and uses lights to coordinate movement between an “excavation zone” and “deposition zone”.
>
> The robotic agent's microcontroller executes a finite state machine (FSM) ... The FSM embodies the different behaviors needed for the robotic agent to excavate material, transport it to the deposition site, and finally return to the excavation site to repeat the process.
>
> The transitions between behaviors are governed by environmental signals in the form of fixed light sources and object proximity information, which are detected via onboard sensors.

#### 摘录 B

- 出处：第 9 页，`Appendix C: finite state machine`，`paper_content.txt` 第 595-617 行
> The robotic agent is equipped with a finite state machine (FSM) ... The robot follows instructions encoded by the FSM, in order to excavate material, transport it to the deposition site, locate an existing deposit, and return to the excavation site to repeat the process.
>
> Turning is initiated after successful excavation or deposition and is only stopped once the RGB sensor detects a local maximum in the desired color value. Once the robot is moving towards the excavation site (blue), it will begin the excavation procedure until it detects that material has remained within its jaws.
>
> While the robot is moving to deposit, it takes a picture using the ArduCAM and searches for a pile by counting the number of “dark” pixels ... The robot then chooses the largest group of connected columns within an image.

#### 摘录 C

- 出处：第 10 页，`FSM final state / deposit`，`paper_content.txt` 第 675-679 行
> and transitions to the final state of the FSM. Here, it will search with its antenna and deposit its material either at the existing pile or at the wall and then begin turning towards the excavation site, thus completing one cycle of material excavation and deposition.

### 2. 基于原文整理后的自然语言描述

The robot controller is an arena-level finite-state machine that cycles through excavation, transport, pile-location, deposition, and return behaviors while moving between a blue excavation zone and a red deposition zone. After a successful excavation or deposition, the robot enters a turning behavior and keeps turning until the RGB sensor detects a local maximum of the target color, which determines when it has aligned with the next zone. When moving toward the excavation site, the controller stays in the excavation procedure until the robot detects that material remains inside its jaws, and when moving toward the deposition site it uses the ArduCAM to search for a pile by detecting dark-pixel shadows framed by bright LED-strip regions. In the final state, the robot uses its antenna to decide whether to deposit on an existing pile or at the wall, then starts turning back toward the excavation site and thereby closes one full excavation-deposition cycle.

### 3. 逐句溯源

1. 句子 1：The robot controller is an arena-level finite-state machine that cycles through excavation, transport, pile-location, deposition, and return behaviors while moving between a blue excavation zone and a red deposition zone.
   对应摘录：A, B
2. 句子 2：After a successful excavation or deposition, the robot enters a turning behavior and keeps turning until the RGB sensor detects a local maximum of the target color, which determines when it has aligned with the next zone.
   对应摘录：B
3. 句子 3：When moving toward the excavation site, the controller stays in the excavation procedure until the robot detects that material remains inside its jaws, and when moving toward the deposition site it uses the ArduCAM to search for a pile by detecting dark-pixel shadows framed by bright LED-strip regions.
   对应摘录：B
4. 句子 4：In the final state, the robot uses its antenna to decide whether to deposit on an existing pile or at the wall, then starts turning back toward the excavation site and thereby closes one full excavation-deposition cycle.
   对应摘录：C
