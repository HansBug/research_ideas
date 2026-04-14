# Intelligent Control of Battery Energy Storage for Multi-Agent Based Microgrid Energy Management - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把微电网 `BESS agent` 的充放电、待机、峰荷削减和 `EDR` 参与写成六状态监督控制链，并明确给出 `SOC / ON_PEAK / LOW_LOAD / EDR` 触发条件与仿真切换过程，足以支撑双 A。

## 条目 1: Battery-agent supervisory controller for peak shaving and EDR participation

- 控制对象：过程与环境控制领域的多智能体微电网电池储能系统代理及其充放电监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是微电网能量管理中的 `BESS agent`，负责在低负荷、峰负荷、过充和 `EDR` 事件之间切换电池储能的充放电策略。
- 判断：算。对象是真实微电网储能控制代理，不是抽象优化流程；原文明确给出了 `0-5` 六个状态、`SOC` 与负荷等级/`EDR` 信号、hysteresis dead-band，以及典型日/`EDR` 工况下的状态切换。

### 1. 原文摘录

#### 摘录 A

- 出处：第 11 页，`3.3 Battery Agent`，`paper_content.txt` 第 373-394 行
> In this paper, fuzzy-based artificial intelligence algorithms are applied to the BESS agent.
> The main operating algorithms of the BESS agent are programmed based on a state machine concept.
> State “0”: The BESS turns off. State “1”: The BESS turns the power on and stands by. State “2”: The BESS charges the battery according to a fuzzy logic. State “3”: The BESS discharges the battery according to a fuzzy logic during the peak loading condition. State “4”: When the battery is overcharged (>100%), the BESS discharges the battery at a constant rate. State “5”: In the EDR event, the battery is discharged at a constant rate.
> The state of the BESS agent changes according to the load level, EDR signal, and the SOC level of the battery ... hysteresis transition by including a small dead-band between states must be considered.

#### 摘录 B

- 出处：第 13 页，`Battery discharging rule / EDR`，`paper_content.txt` 第 443-467 行
> The discharging operation is defined by three states, “3”, “4”, and “5”, to consider peak load shaving, EDR participation, and battery SOC maintenance.
> In state “3”, the BESS discharges to support the power reserve of the main grid during the peak loading condition.
> State “4” defines the BESS discharging action to limit the battery SOC not to exceed 100% ... the BESS discharges by constantly controlling the discharging current at the speed of 1 C-rate until the SOC is equal to or less than 100%.
> When the EDR event occurs, the BESS also need to discharge power in constant current mode.

#### 摘录 C

- 出处：第 17-18 页，`4.1 Case 1 / 4.2 Case 2`，`paper_content.txt` 第 748-762、777-785 行
> In this case, the BESS operates to shave the loads during peak hours. Therefore, it charges during off-peak period and discharges during peak period ... it charges up to 100% by following the fuzzy logic of state “2” ... When the BESS discharges, it also follows the fuzzy logic of state “3”.
> After being fully charged, the battery agent is in state “1” before 11:00. At 11:00, the state of battery agent can be changed into state “3” ... During the low-load period after 20:00, the BESS agent will change into state “2”.
> After being fully charged, the BESS stops charging and waits for participating in the EDR event ... the BESS stays in standby mode until the EDR event occurs from 12:00 pm to 14:00 pm.

### 2. 基于原文整理后的自然语言描述

The `BESS agent` is modeled as a six-state EFSM with `0=off`, `1=standby`, `2=fuzzy charging`, `3=fuzzy discharging for peak-load shaving`, `4=constant-rate discharge for overcharge protection`, and `5=constant-rate discharge for `EDR` participation`. Its transition guards are not just symbolic events but combinations of `ON_PEAK / NORMAL / LOW_LOAD`, `EDR_ON / EDR_OFF`, and battery `SOC`, with a dead-band introduced to prevent chattering near boundary conditions. Inside the charging and peak-discharge states, the actual current reference is computed by fuzzy rules from load level and wind speed, while states `4` and `5` switch the controller to fixed-current safety or demand-response behavior. The case studies further show concrete execution traces: on a regular day the agent stays in `1`, enters `3` at peak time around `11:00`, and returns to `2` in the low-load period after `20:00`; under a scheduled `EDR` event it remains in `1` until the noon request arrives and then discharges through the event window.

### 3. 逐句溯源

1. 句子 1：The `BESS agent` is modeled as a six-state EFSM with `0=off`, `1=standby`, `2=fuzzy charging`, `3=fuzzy discharging for peak-load shaving`, `4=constant-rate discharge for overcharge protection`, and `5=constant-rate discharge for `EDR` participation`.
   对应摘录：A, B
2. 句子 2：Its transition guards are not just symbolic events but combinations of `ON_PEAK / NORMAL / LOW_LOAD`, `EDR_ON / EDR_OFF`, and battery `SOC`, with a dead-band introduced to prevent chattering near boundary conditions.
   对应摘录：A
3. 句子 3：Inside the charging and peak-discharge states, the actual current reference is computed by fuzzy rules from load level and wind speed, while states `4` and `5` switch the controller to fixed-current safety or demand-response behavior.
   对应摘录：B
4. 句子 4：The case studies further show concrete execution traces: on a regular day the agent stays in `1`, enters `3` at peak time around `11:00`, and returns to `2` in the low-load period after `20:00`; under a scheduled `EDR` event it remains in `1` until the noon request arrives and then discharges through the event window.
   对应摘录：C
