# Research on Longitudinal Active Collision Avoidance of Autonomous Emergency Braking Pedestrian System (AEB-P) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：层次、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：AEB-P 的三级风险判定、TTC/制动安全距离阈值、off/ready/active 工作区与上下层控制链都较清楚，可作为非趋同混成样本。

## 条目 1: Warning and braking handoff in the AEB-P system
- 控制对象：行人自动紧急制动系统（AEB-P）
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：层次、连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车主动安全控制领域的 AEB-P system，用于依据碰撞时间和制动安全距离先发出预警，再在必要时接管制动。
- 判断：算，但属于功能链路型样本。对象是实际 AEB 控制系统，原文给出了 warning model、automatic braking intervention 以及上下层控制模块之间的职责分配。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，对 warning model 与上下层控制器的说明，行 15-24
> By studying relevant theoretical systems, such as TTC (time to collision) and braking safety distance, an AEB-P
> warning model was established, and the tra c safety level and work area of the AEB-P warning system
> were deﬁned. The upper-layer fuzzy neural network controller of the AEB-P system was designed,
> and the BP (backpropagation) neural network was trained by collected pedestrian longitudinal
> anti-collision braking operation data of experienced drivers. Also, the fuzzy neural network model
> was optimized by introducing the genetic algorithm. The lower-layer controller of the AEB-P system
> was designed based on the PID (proportional integral derivative controller) theory, which realizes the
> conversion of the expected speed reduction to the pressure of a vehicle braking pipeline.

#### 摘录 B
- 出处：第 5-7 页，Section 2 / 3.3，对 five modules 与 early warning system 的说明，行 233-239, 325-335
> This system consisted of ﬁve modules, namely, sensing system, early warning system, self-learning
> system, control system, and execution system.
> The AEB-P early warning system established in this study had
> three main modules, vehicle and driving environment information collection module, risk assessment
> module, and early warning and brake signal transmitting module.
> The risk assessment module was responsible for determining the risk level based on the obtained
> information and security status judgment; the warning and braking signal transmitting module was
> responsible for issuing the corresponding control signals to the controlled object according to the
> risk assessment level; the controlled object was the AEB-P system.

#### 摘录 C
- 出处：第 9 页，Section 3.3.3，对三级安全等级及输出信号的说明，行 523-537
> The established AEB-P early warning system uses a hierarchical early warning algorithm to
> classify the security levels at di erent driving states. Di erent security levels correspond to di erent
> TTC values. According to the degree of danger, the security levels are divided into three levels; the ﬁrst
> level is the driving safety level, the second level is the collision warning level, and the third level is the
> collision danger level. The ﬁrst level indicates the current driving safety without potential danger,
> and in that case, the AEB-P warning system sends a signal value of 0. The second level indicates that
> the pedestrian has been detected, and there is a potential collision risk, so a driver needs to take the
> corresponding braking measures, and the AEB-P warning system sends a signal value of one. The
> third level denotes an impending pedestrian collision, and the AEB-P warning system sends a brake
> signal value of two.

#### 摘录 D
- 出处：第 11-12 页，Section 3.3.3，对 1.5 s warning window、`t0TTC` 阈值与 level III latch 的说明，行 611-641
> The warning time of the AEB-P early warning system should fully consider the driver’s reaction
> time and brake action time [ 29]. The complexity and danger-level of pedestrian test conditions were
> considered in the study. The warning time of the AEB-P system was set to 1.5 s.
> where t0TTCdenotes the brake safety threshold. When TTCt0TTC, the risk assessment model will
> issue a brake control signal; when t0TTCTTCt0TTC+1.5, the risk assessment model will issue an
> early warning control signal; lastly, when TTCt0TTC+1.5, representing the driving safety, the risk
> assessment model will not issue a control signal.
> In addition, when the vehicle enters the third level, due to frequent changes in vehicle deceleration,
> the computational burden of the risk assessment model will increase, and false alarms are likely to
> occur. Therefore, after entering the third level, the warning system will continue to issue the brake
> signal, and the TTC value will not be calculated.

#### 摘录 E
- 出处：第 12-13 页，Section 3.4，对 off / ready / active operating area 的说明，行 645-658
> When a self-car is close enough to a pedestrian (the
> TTC division in Table 2 is used as a standard), the AEB-P system may be in o , ready to work, or active
> state, which is mainly based on the pedestrian status as a reference indicator. If the pedestrian is in the
> BCG or EFH area (refer to Figure 8), and v1,0orv2,0, the AEB-P system will be in a ready working
> state. In this case, the risk assessment model will not issue any control signals, and the system will
> prompt a driver to pay attention to pedestrian safety in the form of an image. If a pedestrian is in the
> AECGH area, the AEB-P system will be activated regardless of the sporting state of a pedestrian. In this
> case, the risk assessment model will issue a pedestrian collision warning or an automatic emergency
> braking signal.

### 2. 基于原文整理后的自然语言描述

The AEB-P system is organized as sensing, early warning, self-learning, control, and execution modules, with an upper fuzzy-neural-network controller that outputs the desired deceleration and a lower controller that converts that command into brake-line pressure for the vehicle. Its early-warning subsystem collects vehicle and pedestrian information, uses the risk-assessment module as the highest decision-making layer, and issues control signals according to three safety levels: level I sends signal 0 for safe driving, level II sends signal 1 for collision warning, and level III sends brake signal 2 for impending collision. The warning duration of the second level is set to 1.5 s, and the integrated TTC/braking-safety-distance rule issues a brake control signal when TTC <= t0TTC, an early-warning signal when t0TTC <= TTC <= t0TTC + 1.5, and no control signal when TTC >= t0TTC + 1.5. After the vehicle enters level III, the warning system keeps issuing the brake signal without recalculating TTC, and the operating-area logic further distinguishes off, ready-to-work, and active states according to the pedestrian area and movement status.

### 3. 逐句溯源

1. 句子 1：The AEB-P system is organized as sensing, early warning, self-learning, control, and execution modules, with an upper fuzzy-neural-network controller that outputs the desired deceleration and a lower controller that converts that command into brake-line pressure for the vehicle.
   对应摘录：A, B
2. 句子 2：Its early-warning subsystem collects vehicle and pedestrian information, uses the risk-assessment module as the highest decision-making layer, and issues control signals according to three safety levels: level I sends signal 0 for safe driving, level II sends signal 1 for collision warning, and level III sends brake signal 2 for impending collision.
   对应摘录：B, C
3. 句子 3：The warning duration of the second level is set to 1.5 s, and the integrated TTC/braking-safety-distance rule issues a brake control signal when TTC <= t0TTC, an early-warning signal when t0TTC <= TTC <= t0TTC + 1.5, and no control signal when TTC >= t0TTC + 1.5.
   对应摘录：D
4. 句子 4：After the vehicle enters level III, the warning system keeps issuing the brake signal without recalculating TTC, and the operating-area logic further distinguishes off, ready-to-work, and active states according to the pedestrian area and movement status.
   对应摘录：D, E
