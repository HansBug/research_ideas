# 火星样本返回捕获-封装-返回系统机器人控制软件的初步设计 / A Preliminary Design of the Robotic Control Software for Mars Sample Return - Capture, Containment, and Return System

## 基本信息

- **标题**：A Preliminary Design of the Robotic Control Software for Mars Sample Return - Capture, Containment, and Return System
- **中文标题**：火星样本返回捕获-封装-返回系统机器人控制软件的初步设计
- **作者**：Jacob T. Cassady，Ashok K. Prajapati，Elizabeth J. Geist，Bradley C. Tse，Benjamin L. Osborne，Jeffrey A. Angielski，Joseph B. Lattisaw，Francis B. Hallahan
- **单位**：
  - NASA Langley Research Center
  - NASA Goddard Space Flight Center
  - Microtel LLC.
  - HII Mission Technology Corporation
  - Embedded Flight Systems Inc.
- **发表**：AIAA SCITECH 2025 Forum, 2025
- **DOI**：10.2514/6.2025-2514
- **链接**：https://doi.org/10.2514/6.2025-2514

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文正文给出了 `RSW` 主任务、FSM、Worker Task 协作方式、命令处理和 `RSCE` 交互逻辑，可直接作为控制器设计依据。

### 数据集/案例获取方式

- 原文未提供外部数据集下载链接。
- 论文围绕 `CCRS` 真实任务背景，给出了 motion primitives、behaviors、硬件/软件架构和主控状态机，可直接作为单案例 source paper 使用。

## 简报

这篇论文解决的是**火星样本返回任务中，机器人传送装置如何通过 flight software 安全执行抓取/传送动作**的问题。输入是 motion primitive 命令、`RSCE` telemetry、Worker Task 检查结果和 stop/fault 事件，方法是设计一个显式主 FSM 管理配置、预检查、运动执行和后检查，输出是 `RSW` 的机器人控制软件结构。

- **输入**：motion primitive commands、`RSCE` telemetry、Worker Task result、stop command、fault condition。
- **方法**：`Step / StateExit / StateEntry / StateRun` 调度的机器人控制 FSM。
- **输出**：机器人运动原语执行控制链、异常处理逻辑和 `RSW` 软件架构。
- **一句话评价**：这是很典型的航天机器人 `EFSM + T0` 样本，状态表和转移链都已经足够细，不需要额外猜测。

## 控制系统与状态机证据

### 控制对象

论文对象是 `Mars Sample Return` 任务 `CCRS` 中的 `Robot Software (RSW)`。它负责 command and monitor 控制机器人机构的 avionics，使系统能够执行 sterilize、install、pick-and-place 等与样本转运相关的动作。

### 状态机组织方式

`RSW` 主状态机明确包括：

1. `UNKNOWN`
2. `INITIALIZED`
3. `RSCE_ON`
4. `READY_ON`
5. `CONFIGURE`
6. `PRE_MOTION_CHECK`
7. `IN_MOTION`
8. `POST_MOTION_CHECK`
9. `FAULT`

同时，原文还给出 `current state` 与 `requested state` 的双变量设计，以及 `Step -> StateExit -> StateEntry -> StateRun` 的调度顺序，因此它不是只列状态名，而是完整的软件控制骨架。

### 关键控制链

论文把 nominal path 写得非常明确：

- 启动后从 `UNKNOWN` 进入 `INITIALIZED`
- 等待 telemetry 后进入 `RSCE_ON`
- 完成初始配置后进入 `READY_ON`
- 收到 motion primitive command 后进入 `CONFIGURE`
- 配置完成后进入 `PRE_MOTION_CHECK`
- 预检通过后进入 `IN_MOTION`
- 运动结束后进入 `POST_MOTION_CHECK`
- 检查完成后回到 `READY_ON`

同时也写清楚了异常路径：

- 任意状态都允许进入 `FAULT`
- `CONFIGURE / PRE_MOTION_CHECK / IN_MOTION / POST_MOTION_CHECK` 中收到 stop command 会直接回 `READY_ON`

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它是**真实航天任务软件**中的离散控制链，不是泛化的机器人方法描述。
- 它能提供“命令-配置-预检-执行-后检-异常回退”这种非常规整的工程控制模板。
- 论文正文足以支撑 `STM.md` 达到 `🟢 A`，适合直接进入主数据集候选池。

### 可直接借鉴之处

- 可以直接借鉴 `current/requested state` 这种工程化状态管理写法。
- 可以直接借鉴 `StateExit / StateEntry / StateRun` 的控制器文本组织结构。
- 可以直接借鉴 stop/fault 作为统一回退接口的建模方式。

### 局限性

- 论文是 preliminary design，某些底层 motion primitive 细节还没完全展开。
- 低层机器人运动学和硬件细节较多，不应全部混入高层状态机文本。
- 时间语义主要依赖软件循环和任务进度，不是显式 timer 驱动。

## 文献分类总结

- **文献类型**：真实航天机器人控制案例论文
- **控制对象**：`CCRS` 机器人软件 `RSW`
- **状态机画像**：`EFSM + T0`
- **证据强度**：状态表、执行链和 fault/stop 回退都完整，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，用于补齐机器人运动原语执行与异常恢复类航天控制样本
