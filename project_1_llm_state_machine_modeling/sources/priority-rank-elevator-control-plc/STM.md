# The Realization of a Control Algorithm and its PLC Based Program Able to Authorize Four Different Ranks of Priority to Elevator Users - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `Normal / Rank1 / Rank2 / Rank3` 四级特权电梯调度写成统一 PLC 程序，并明确了模式切换、同级集体运行和高优先级抢占规则。

## 条目 1: Four-rank privileged elevator service supervisor

- 控制对象：楼宇机电与电梯控制领域的四级权限电梯调度监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向医院和公共建筑 privileged-use 场景的电梯服务监督器，用四种授权等级动态切换普通调度和 VIP 抢占调度。
- 判断：算。对象是实际电梯控制系统，原文明确给出了四个模式的服务规则、模式间切换条件、同级集体运行逻辑和最高优先级抢占行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 16-28 行
> In this project, authorization rankings were assigned and special usage privileges given. Thus, in cases where VIP usage is needed, the elevator temporarily cancels out either totally or partially all other calls according to VIP ranking, resulting in the efficient use of elevators by preventing them from being inactive when there is no ongoing VIP usage. This project utilizes a model encompassing a four rank authorization system (three VIP, and one normal).

#### 摘录 B

- 出处：第 1-2 页，Introduction，对四种模式的总说明，`paper_content.txt` 第 74-112 行
> four different algorithms created for four differently ranked priority groups (rank1, rank2, rank3, normal) ... the elevator, in case of VIP usage, temporarily cancels out either totally or partially all other calls and sends the elevator according to VIP ranking of the caller.
>
> Rank1 Mode: ... All calls before and after are canceled until caller has reached destination.
>
> Rank2 Mode: ... It answers cabin calls made before Rank2 call until Rank2 is reached, and answers Rank1 calls made afterwards, and Rank2 and Rank3 calls which are en route.
>
> Rank3 Mode: ... Calls made before Rank3 call are answered until Rank3 user is reached. Afterwards normal calls are not answered.
>
> Normal Mode: ... elevator calls matching elevator direction are answered with accordance to en route closeness, while calls in the opposite direction are answered after elevator course changes again accordingly with en route closeness.

#### 摘录 C

- 出处：第 2 页，`2.2.1 Normal Mode` 与 `2.2.2 Privileged Modes`，`paper_content.txt` 第 159-204 行
> Collective operation answers same direction calls according to proximity and stores to memory opposite direction calls to be answered after direction change.
>
> The transition conditions from normal mode to privileged mode, and from any privileged mode to another rank have been set. When in privileged mode, the collective operation will be used for other calls on the same rank. For example, when in Rank2, another Rank2 call will be accepted if on the way, if not it will be left for later.

#### 摘录 D

- 出处：第 2 页，`2.2.2.1 Rank1`，`paper_content.txt` 第 205-213 行
> When in either Rank2, Rank3 or Normal mode, in order to respond to the Rank1 call, the elevator stops on the nearest floor and an announcement is made for the passengers to evacuate the elevator. Then, the elevator goes directly to the Rank1 user and performs the cabin call for Rank1 users. No calls other than another Rank1 call are accepted. ... After the Rank1 call has been fulfilled, the elevator returns to Normal mode if there are no other Rank1 calls.

### 2. 基于原文整理后的自然语言描述

The PLC elevator controller is organized around four authorization modes rather than around a single dispatch rule: `Normal`, `Rank1`, `Rank2`, and `Rank3`. In `Normal` mode, it applies collective-operation logic, serving same-direction calls by proximity and storing opposite-direction calls until the travel direction reverses. When a privileged request appears, the supervisor switches from `Normal` or a lower rank into the corresponding privileged mode, and each privileged mode preserves a different service envelope: `Rank1` clears all other calls and serves only rank-1 traffic until the user reaches the destination, `Rank2` continues cabin calls already made before the request and still admits later `Rank1` calls plus en-route `Rank2` and `Rank3` calls, and `Rank3` finishes older calls until the rank-3 user is reached and then suppresses normal calls. Calls of the same rank inside a privileged mode still reuse collective-operation logic, so the overall design is a hierarchical elevator supervisor with a shared dispatch policy nested inside rank-specific override modes.

### 3. 逐句溯源

1. 句子 1：The PLC elevator controller is organized around four authorization modes rather than around a single dispatch rule: `Normal`, `Rank1`, `Rank2`, and `Rank3`.
   对应摘录：A, B
2. 句子 2：In `Normal` mode, it applies collective-operation logic, serving same-direction calls by proximity and storing opposite-direction calls until the travel direction reverses.
   对应摘录：B, C
3. 句子 3：When a privileged request appears, the supervisor switches from `Normal` or a lower rank into the corresponding privileged mode, and each privileged mode preserves a different service envelope: `Rank1` clears all other calls and serves only rank-1 traffic until the user reaches the destination, `Rank2` continues cabin calls already made before the request and still admits later `Rank1` calls plus en-route `Rank2` and `Rank3` calls, and `Rank3` finishes older calls until the rank-3 user is reached and then suppresses normal calls.
   对应摘录：B, D
4. 句子 4：Calls of the same rank inside a privileged mode still reuse collective-operation logic, so the overall design is a hierarchical elevator supervisor with a shared dispatch policy nested inside rank-specific override modes.
   对应摘录：C
