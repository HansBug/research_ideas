# Automated Contingency Management in Unmanned Aircraft Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文提出的安全监视器把多类飞行异常统一组织成 `7` 状态中央监视状态机，并通过 `C2` 失链仿真给出进入 `Autonomous operation` 与恢复 `Nominal operation` 的实际运行轨迹，是航空方向质量较高的任务安全管理样本。

## 条目 1: Centralized Safety Monitor FSM

- 控制对象：航空航天与飞行/空管控制领域的无人机自动应急管理安全监视器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于 `UAS` 自动应急管理的中央安全监视器，用统一状态机诊断 `C2` 失链、导航退化、控制退化、失去间隔和越界等异常，并决定是交给 contingency manager 还是直接触发 flight termination。
- 判断：算。对象是实际无人机任务管理架构中的安全关键控制子系统，不是单纯验证模型；原文明确给出状态集、进入条件、恢复条件、终止状态语义以及 `C2` 失链时的仿真运行结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 97-98 页，`4.3 Safe Mission Manager architecture design`，`paper_content.txt` 第 3084-3104 行
> Accordingly, we advocate separating ACM functions into two separate software components, named the Safety Monitor and Contingency Manager ... The role of the Safety Monitor is to check system behavior for unsafe states; and when an unsafe state is detected, to take the critical decision of whether a contingency management option is feasible, or whether the flight termination action is required instead ... When the contingency threshold is exceeded ... the resolution of this state will be delegated to the Contingency Manager. But if the contingency option fails and the emergency threshold is surpassed ... the Safety Monitor will command the FTS ...

#### 摘录 B

- 出处：第 254 页，`A.2 Specification of the Safety Monitor model`，`paper_content.txt` 第 8132-8160 行
> In short, the proposed contingencies or fault hypothesis include: 1. C2 link loss 2. GNSS loss of performance 3. Loss of control in-flight 4. Loss of separation 5. Mission boundary limits violation ... the Safety Monitor must diagnose each of the previous events and decide whether the resulting state is to be handled by the Contingency Manager or by the Flight Termination System ... one single contingency results in an abnormal state ... any combination of nested contingencies or the occurrence of an emergency event results in an emergency state ...
>
> The proposed FSM has seven states: the nominal state (S1), five abnormal states (S2 to S6, one per contingency under study) and one emergency state (S7, representing all possible out of control conditions). Autonomous operation (S2) is entered after the C2 link loss; Degraded navigation (S3) ... Degraded control (S4) ... Traffic alert (S5) ... Out of mission volume (S6) ...

#### 摘录 C

- 出处：第 255 页，`Figure A.1` 与 model requirements，`paper_content.txt` 第 8167-8202 行
> S2: Autonomous operation ... S1: Nominal operation ... S4: Degraded control ... S3: Degraded navigation ... S5: Traffic alert ... S6: Out of mission volume ... S7: Out of control ...
>
> By contrast, the emergency state is an unrecoverable state: when this state is entered, no transition can make the system to evolve to a different state.
>
> SM1 There should always be a transition for reaching the out of control state in one step ... SM2 The out of control state shall be a final state ... SM3 A contingency state shall not be reachable from another contingency state in one step ...

#### 摘录 D

- 出处：第 222-224 页，`7.3.3 Contingency scenario CS2`，`paper_content.txt` 第 7220-7236、7250-7252、7285-7290 行
> Once the contingency is injected, the Safety Monitor receives the corresponding contingency signal and enters the “Autonomous operation” state ...
>
> Figure 7.37: ... Safety Monitor state [Nominal operation, Autonomous operation, Degraded navigation, Degraded control, Traffic alert, Out of boundary, Out of control]
>
> the “regain signal” is effective at recovering the C2 link ... the Safety Monitor returns to the “Nominal operation” state ...

### 2. 基于原文整理后的自然语言描述

The proposed Safety Monitor is the strategic safety gatekeeper of the UAS contingency-management architecture: it continuously checks whether the aircraft has entered an unsafe condition and decides whether the situation may still be delegated to the contingency manager or must instead go directly to the flight-termination system. Its centralized FSM contains seven named states, namely `S1 Nominal operation`, five abnormal states `S2 Autonomous operation`, `S3 Degraded navigation`, `S4 Degraded control`, `S5 Traffic alert`, `S6 Out of mission volume`, and one emergency state `S7 Out of control`. Each single contingency maps to one abnormal state, but nested contingencies or emergency events escalate the monitor into `S7`, which is explicitly specified as a final unrecoverable state that must remain reachable in one step from the other states to preserve the ability to trigger flight termination. In the validated `C2 link loss` scenario, the monitor leaves `Nominal operation` and enters `Autonomous operation` when the link is lost, then returns to `Nominal operation` after the regain-signal procedure succeeds and the `C2` link is restored.

### 3. 逐句溯源

1. 句子 1：The proposed Safety Monitor is the strategic safety gatekeeper of the UAS contingency-management architecture: it continuously checks whether the aircraft has entered an unsafe condition and decides whether the situation may still be delegated to the contingency manager or must instead go directly to the flight-termination system.
   对应摘录：A, B
2. 句子 2：Its centralized FSM contains seven named states, namely `S1 Nominal operation`, five abnormal states `S2 Autonomous operation`, `S3 Degraded navigation`, `S4 Degraded control`, `S5 Traffic alert`, `S6 Out of mission volume`, and one emergency state `S7 Out of control`.
   对应摘录：B, C
3. 句子 3：Each single contingency maps to one abnormal state, but nested contingencies or emergency events escalate the monitor into `S7`, which is explicitly specified as a final unrecoverable state that must remain reachable in one step from the other states to preserve the ability to trigger flight termination.
   对应摘录：A, B, C
4. 句子 4：In the validated `C2 link loss` scenario, the monitor leaves `Nominal operation` and enters `Autonomous operation` when the link is lost, then returns to `Nominal operation` after the regain-signal procedure succeeds and the `C2` link is restored.
   对应摘录：D
