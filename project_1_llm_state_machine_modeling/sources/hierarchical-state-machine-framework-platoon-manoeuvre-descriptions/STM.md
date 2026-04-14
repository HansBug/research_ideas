# A Hierarchical State-Machine-Based Framework for Platoon Manoeuvre Descriptions - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然整体在讲机动描述框架，但 `JoinTail` 的角色机、层次 idle super-state、消息原语和 timeout-abort 稳定化链条都写得足够具体，可作为高质量车队协同样本。

## 备注

- `paper_content.txt` 中存在少量连字与 ligature 提取噪声，如 ``、``，但关键段落可读且不影响状态机主链判断。

## 条目 1: Join-Tail Hierarchical Manoeuvre with Timeout-Stable Abort

- 控制对象：汽车与道路车辆领域的 platoon `JoinTail` 机动协调器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向车辆编队的 `JoinTail` 分层机动描述与执行框架，用 leader / follower 角色状态、子机动、消息原语和 timeout-abort 规则来保证编队接入过程结束在稳定 idle state。
- 判断：算。虽然论文带有框架设计色彩，但原文给出的对象仍是实际 platooning manoeuvre controller，且 `JoinTail` 的状态、消息、层级组织、成功与中止流程都能直接整理成状态机自然语言样本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，JoinTail protocol example，行 214-230
> The JOIN TAIL-protocol describes the process of a free vehicle joining an existing platoon at its tail through two CFSM.
>
> When a vehicle (Vehicle A) decides to join a platoon, it sends a join request to the leader (Vehicle B) of the platoon (Transition 1, T1). B either rejects (T2) or acknowledges (T3) the request. In the case of rejection, both vehicles return to idle and the protocol terminates. If the request is acknowledged, A will wait for B to join the platoon. A moves to the tail of the platoon. Once arrived at the tail, A attaches to the platoon, starts following the preceding vehicle (i.e. switch into CACC mode), sends a message to B that the join is completed (T4), and transitions into the follower-Idle State. Upon receipt of the join-completion message, B updates the platoon information and returns to idle. The protocol execution is complete and terminates.

#### 摘录 B

- 出处：第 7-8 页，Framework overview，行 542-583
> Stability: To ensure stability of the system, each platooning manoeuvre has to end in a stable state for all involved vehicles, regardless of manoeuvre's success. We refer to these states as ``stable idle states'' ... Platoon Leader (PL), Platoon Follower (PF), or Free Vehicle (FV). ... unstable idle state would be WPL, WPF, and WFV. Additionally, we make use of the unstable idle state Temporary Platoon Leader (TPL) ...
>
> Communication ... These messages include Requests (REQ), orders (ORD), done-confirmation (DN), abort (ABT), and acceptance/rejection (ACK/NACK). ... If this cannot be ensured, then the sub-manoeuvres can be extended by adding respective time-out and abort transitions.
>
> Figure 5 provides an overview of the SEAD framework and illustrates its hierarchical structure according to the paradigm of hierarchical state machines.

#### 摘录 C

- 出处：第 8-10 页，Formulating sub-manoeuvres / manoeuvres / idle super-states，行 624-659, 690-698, 729-740, 776-790
> With the list of idle states and action primitives, we can now create sub-manoeuvres. A sub-manoeuvre encapsulates reusable behavioural patterns that involve two or more vehicles and transitions at least one of the participating vehicles from one idle state into another. For each participating vehicle, the behaviour is described through a sequence of primitives which constitute a sub-state machine. ... each sub-manoeuvre is split into two or more sub-state machines, one for each vehicle participating ... The sub-state machines are connected and synchronised through V2V messages.
>
> ... if one vehicle encounters a situation that will prevent the successful completion of the sub-manoeuvre and causes an abort-result, V2V communication (or time-outs) must cause all other sub-state machines to terminate at the same abort-result.
>
> ... if closing the gap is taking too long, a timeout in A aborts the sub-manoeuvre. The timeout causes A to send an ABT message to B ... Afterwards, the sub-manoeuvre concludes for A with an abort-result ... B receives the message and will initiate the sequence to split from the original platoon by transitioning into a PL ...
>
> The JOIN TAIL manoeuvre requires no additional actions in case of an abort and will conclude in a stable state achieved through the abort-architecture within the sub-manoeuvres.
>
> ... We combine the idle state and its associated sub-manoeuvres ... into an idle super-state ... This superstate can only be left through the successful or unsuccessful execution of sub-manoeuvres or when a time-out occurs.

### 2. 基于原文整理后的自然语言描述

The `JoinTail` controller describes how a free vehicle joins an existing platoon by sending a join request to the platoon leader, receiving either rejection or acknowledgement, moving to the tail, attaching to the platoon, switching into CACC-style following, and finally sending a join-completion message so that the leader can update platoon information and both vehicles return to idle. In the SEAD framework this behavior is not a flat protocol only: it is organized as a hierarchical state machine with stable idle states such as `PL`, `PF`, and `FV`, unstable idle states such as `WPL`, `WPF`, `WFV`, and `TPL`, and message primitives including `REQ`, `ORD`, `DN`, `ABT`, `ACK`, and `NACK` that synchronize the participating vehicles. Each reusable sub-manoeuvre is itself split into role-specific sub-state machines connected through V2V messages, and a full manoeuvre such as `JoinTail` is expressed as a chain of these sub-manoeuvres from the leader perspective while idle super-states collect the idle state and the sub-manoeuvres that may be executed from it. If a sub-manoeuvre cannot finish successfully, timeout or abort transitions force all involved vehicles to terminate in defined stable states instead of remaining in unstable waiting states, and the paper explicitly states that `JoinTail` relies on this abort architecture to finish safely even when the manoeuvre does not succeed.

### 3. 逐句溯源

1. 句子 1：The `JoinTail` controller describes how a free vehicle joins an existing platoon by sending a join request to the platoon leader, receiving either rejection or acknowledgement, moving to the tail, attaching to the platoon, switching into CACC-style following, and finally sending a join-completion message so that the leader can update platoon information and both vehicles return to idle.
   对应摘录：A
2. 句子 2：In the SEAD framework this behavior is not a flat protocol only: it is organized as a hierarchical state machine with stable idle states such as `PL`, `PF`, and `FV`, unstable idle states such as `WPL`, `WPF`, `WFV`, and `TPL`, and message primitives including `REQ`, `ORD`, `DN`, `ABT`, `ACK`, and `NACK` that synchronize the participating vehicles.
   对应摘录：B
3. 句子 3：Each reusable sub-manoeuvre is itself split into role-specific sub-state machines connected through V2V messages, and a full manoeuvre such as `JoinTail` is expressed as a chain of these sub-manoeuvres from the leader perspective while idle super-states collect the idle state and the sub-manoeuvres that may be executed from it.
   对应摘录：C
4. 句子 4：If a sub-manoeuvre cannot finish successfully, timeout or abort transitions force all involved vehicles to terminate in defined stable states instead of remaining in unstable waiting states, and the paper explicitly states that `JoinTail` relies on this abort architecture to finish safely even when the manoeuvre does not succeed.
   对应摘录：B, C
