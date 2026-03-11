# Formal Specification and Verification of a Coordination Protocol for an Automated Air Traffic Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：AAC 中 AutoResolver/TSAFE/TCAS 的控制接管与返还条件非常明确。

## 条目 1: Layered control handoff in the Automated Airspace Concept
- 控制对象：自动空中交通控制系统中的冲突协调协议

### 0. 条目识别与判定

- 一句话说明：这是航空交通控制领域的 coordination protocol within an automated air traffic control system，用于在不同冲突时间窗下在 controller、TSAFE 和 TCAS 之间分配控制责任。
- 判断：算。对象是实际空中交通控制系统中的协调控制协议，原文清楚给出了冲突时间窗、审批、自动接管和控制返还逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section 3，对 AAC layered design 的描述，行 169-178
> ThecentraltaskoftheAACistomaintainsafeseparationandprovidecollision avoidanceinthe
> airspace. TheAACisabletodetectapotentiallossofseparation(LOS)inth efuture,referredto
> as aconﬂict, and resolve conﬂicts by generating resolution maneuvers for the aircra ft involved
> and sending these resolutions securely to pilot(s). Pilots are expected to ca rry out resolutions
> in a timely manner. To simplify communication and coordination, it is desirable to implemen t
> a single system capable of detecting and resolving all possible conﬂicts and collisions. How-
> ever, the complexity of this system would be formidable and satisfactory resp onse times are not
> achievable with currently available hardware. Thus, the AAC incorporate s a compositional de-
> sign,inwhichdifferentcomponentsareresponsibleforhandlingshort- ,andnear-termconﬂicts,
> andcollisionavoidance. Figure 1illustratestheinfrastructureof theAAC.

#### 摘录 B
- 出处：第 6 页，Figure 2 前后的 operational concept，行 216-230
> corresponding to time slot (1), and also provides resolutions accordingly to the controller. If
> approved by the controller, the resolutions from the AutoResolver will be tr ansmitted to the af-
> fected aircraft. TSAFE detects conﬂicts up to 3 minutes in the future. If the time to LOS is
> between 1 and 3 minutes, corresponding to time slot (2)in Figure 2, TSAFE will ﬁrst alert the
> controller and wait for approval. In this circumstance, the controller has th ree choices: approve
> the resolution from TSAFE and give control responsibility for the involved aircraft to TSAFE,
> resolve the conﬂict manually, or wait without resolving the conﬂict. In the latte r two cases, the
> controllermaintainsresponsibilityforcontrollingtheaircraftinvolvedintheco nﬂict. Ifthecon-
> troller transfers control to TSAFE, he should not give resolutions to the in volved aircraft until
> the conﬂict has been resolved. However, if the time to LOS falls below the TSA FEthreshold
> of 1 minute, as deﬁned in [ 13], TSAFE will take control of the aircraft involved in the conﬂict
> from the controller, without having to wait for controller approval, and se nd resolutions to these
> aircraft automatically. This case corresponds to time slot (3)in Figure 2. After the conﬂict is
> resolved, TSAFE will return control of the aircraft involved to the contro ller, as shown in time
> slot(4)in Figure 2. Without the help of ground-based systems, TCAS is able to detect possible

#### 摘录 C
- 出处：第 8 页，Figure 4，对 TSAFE_Alert variable values 的说明，行 315-316
> variable, there are three possible values for the variable TSAFE Alert: Non, AT and BT, corre-
> sponding to no LOS detected, LOS detected with time to LOS above and below the th reshold.

### 2. 基于原文整理后的自然语言描述

The Automated Airspace Concept allocates conflict handling across layered components, with AutoResolver addressing longer-term conflicts, TSAFE handling tactical conflicts, and TCAS providing the last layer of collision avoidance. When the time to loss of separation is between one and three minutes, TSAFE alerts the controller and waits for approval, and if the controller transfers control he should not issue further resolutions until the conflict has been resolved. When the time to loss of separation falls below one minute, TSAFE takes control automatically and returns control to the controller after the conflict is resolved.

### 3. 逐句溯源

1. 句子 1：The Automated Airspace Concept allocates conflict handling across layered components, with AutoResolver addressing longer-term conflicts, TSAFE handling tactical conflicts, and TCAS providing the last layer of collision avoidance.
   对应摘录：A
2. 句子 2：When the time to loss of separation is between one and three minutes, TSAFE alerts the controller and waits for approval, and if the controller transfers control he should not issue further resolutions until the conflict has been resolved.
   对应摘录：B
3. 句子 3：When the time to loss of separation falls below one minute, TSAFE takes control automatically and returns control to the controller after the conflict is resolved.
   对应摘录：B, C
