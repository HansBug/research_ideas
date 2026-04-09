# Autonomous Firefighting Inside Buildings by an Unmanned Aerial Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把室外接近建筑、寻找窗户、穿窗进入、室内探索、火源定位、灭火和返航都并入一套 `FlexBE` 层次状态机，任务主链和异常回退链都足够完整。

## 备注

- 当前 `paper_content.txt` 中含少量 `NUL` 字节，但正文关键段落与状态机说明可正常读取；本次提取以可追溯文字证据为准，未把这些噪声硬改写成正文内容。

## 条目 1: Building-interior firefighting mission supervisor

- 控制对象：航空航天与飞行/空管控制领域的室内灭火无人机室外-室内任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个运行在 `MAV` 上的高层任务监督器，用层次状态机串联起飞前检查、室外绕楼搜窗、穿窗进入、室内探索找火、灭火、从原窗离开以及返航降落。
- 判断：算。对象是实际消防无人机任务控制器而不是单一感知算法；原文明确说明整套系统由 `hierarchical state machine` 互连，且逐段展开了 `outdoor phase`、`window flythrough`、`indoor phase` 与 `return home` 逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 10 页，`F. High-Level Behavior Control`，`paper_content.txt` 第 905-939 行
> The complete behavior structure of the proposed system is constructed as a hierarchical state machine, which is used for interconnecting all the subsystems.
>
> The hierarchical state machine is implemented using the Flexbe library, and it is fully integrated into the designed ROS framework.
>
> The diagram of the main state machine ... In the first step, the correct performance of all key parts of the system is checked. When every component is verified to be operational, an automatic takeoff is called. Once the MAV is in the air, the mission commences.
>
> The mission is divided into two parts: the outdoor phase and the indoor phase ... At the end of the mission ... the MAV flies back to the home position and lands.

#### 摘录 B

- 出处：第 10-11 页，`Outdoor phase`，`paper_content.txt` 第 960-984 行
> After it reaches a safe position near the building, the MAV starts flying alongside the building at a predefined distance with a heading towards the building, and begins the window detection mechanism.
>
> Whenever a window is located, the MAV stops flying alongside the building and flies in front of the window to distance of 2 m from its center.
>
> Once this position is reached, the localization of the MAV is switched to indoor flying mode ... and an attempt is made to fly through the window.
>
> If the attempt is successful, the MAV is inside the building and the outdoor phase is considered successfully finished ... The attempts can be repeated until the maximum allowed flight time is reached. After reaching this time, the MAV automatically lands.

#### 摘录 C

- 出处：第 11-12 页，`Window flythrough`，`paper_content.txt` 第 985-1009 行
> First, the MAV flies to a position in front of the window while continuously facing the center of the window.
>
> The MAV then hovers in front of the center of the window to stabilize itself before the actual flythrough.
>
> The flythrough maneuver is then initialized and the state machine waits for an up-to-date window estimate corrected by new detections.
>
> After the window estimate has been updated, the MAV flies through the center of the window to a goal position at a predefined distance behind the window while maintaining a constant altitude.
>
> If the window estimate is lost while the flythrough is in progress and the MAV is still outside the building, the state machine switches to the Escaping state and the MAV returns to its original hovering position in front of the window.

#### 摘录 D

- 出处：第 12 页，`Indoor phase`，`paper_content.txt` 第 1010-1028 行
> The indoor phase contains the final parts - localization and extinguishing of the fire.
>
> Once the fire is detected, the MAV flies in front of it and begins extinguishing.
>
> If the fire target is not lost, the MAV depletes all the water that it is carrying during the extinguishing maneuver ... In the case that the fire is lost, the MAV starts exploring again.
>
> After depleting the extinguishing agent, the MAV flies back in front of the window that it entered through and tries to fly back outside the building.
>
> When the MAV is outside, the localization of the MAV is switched to outdoor flying again and MAV flies back to land on the starting position.

### 2. 基于原文整理后的自然语言描述

The paper exposes a hierarchical mission supervisor for an indoor-firefighting UAV, implemented in `FlexBE`, that interconnects takeoff checks, outdoor building approach, window entry, indoor search, extinguishing, exit, and return-home landing. At the main level, the controller starts with system verification and takeoff, then splits the mission into `outdoor phase` and `indoor phase`, and ends by flying back to the home position and landing. During the outdoor phase, the MAV wall-follows the building, searches for an open window, moves to a point `2 m` in front of the detected window, switches localization to indoor mode, and repeatedly retries the entry attempt until either the vehicle is inside or the maximum flight time is exceeded and an automatic landing is triggered. The flythrough itself is a nested submachine: the UAV first hovers in front of the window to stabilize, waits for an updated window estimate, then flies through the center of the window to a goal point behind it, while an `Escaping` branch returns the vehicle to the original hover point if the estimate is lost before the vehicle has entered the building. Inside the building, the supervisor alternates among exploration, fire detection, flying in front of the detected fire, and extinguishing; if the target is lost it resumes exploration, and once the extinguishing agent is depleted it exits through the same window, switches back to outdoor localization, and returns to the start position. The result is a richly structured UAV mission HSM with both nominal and recovery paths clearly exposed.

### 3. 逐句溯源

1. 句子 1：The paper exposes a hierarchical mission supervisor for an indoor-firefighting UAV, implemented in `FlexBE`, that interconnects takeoff checks, outdoor building approach, window entry, indoor search, extinguishing, exit, and return-home landing.
   对应摘录：A
2. 句子 2：At the main level, the controller starts with system verification and takeoff, then splits the mission into `outdoor phase` and `indoor phase`, and ends by flying back to the home position and landing.
   对应摘录：A
3. 句子 3：During the outdoor phase, the MAV wall-follows the building, searches for an open window, moves to a point `2 m` in front of the detected window, switches localization to indoor mode, and repeatedly retries the entry attempt until either the vehicle is inside or the maximum flight time is exceeded and an automatic landing is triggered.
   对应摘录：B
4. 句子 4：The flythrough itself is a nested submachine: the UAV first hovers in front of the window to stabilize, waits for an updated window estimate, then flies through the center of the window to a goal point behind it, while an `Escaping` branch returns the vehicle to the original hover point if the estimate is lost before the vehicle has entered the building.
   对应摘录：C
5. 句子 5：Inside the building, the supervisor alternates among exploration, fire detection, flying in front of the detected fire, and extinguishing; if the target is lost it resumes exploration, and once the extinguishing agent is depleted it exits through the same window, switches back to outdoor localization, and returns to the start position.
   对应摘录：D
6. 句子 6：The result is a richly structured UAV mission HSM with both nominal and recovery paths clearly exposed.
   对应摘录：A, B, C, D
