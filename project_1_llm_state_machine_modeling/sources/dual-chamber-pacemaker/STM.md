# Modeling and Verification of a Dual Chamber Implantable Pacemaker - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：基础起搏逻辑和 DDD/VDI 切换逻辑都能从原文连续化。

## 条目 1: Basic DDD pacemaker timing control
- 控制对象：双腔起搏器 DDD 模式基本控制逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是植入式心脏节律管理领域的双腔起搏器控制系统，用于协调心房与心室的感知和起搏时序。
- 判断：算。对象是典型安全关键医疗控制系统，核心行为就是依据感知事件和定时约束推进不同节律阶段。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section 3.2-3.3 开头，行 138-157
> The function of a pacemaker is to manage the timing relationship between the
> atrial and ventricular events. Thus Timed Automata is suitable for modeling
> boththe deterministicbehaviorofapacemakerandthenon-deterministicbehav-
> ior of the heart. The overview of the closed-loop system is showed in Fig. 2(a).
> The heart and the pacemaker communica te with each other using broadcast
> channels. The heart generates Aget!and Vget!actions, representing atrial and
> ventricular events that the pacemaker take as inputs. The pacemaker processes
> the signals and generates pacing actions AP!and VP!to the corresponding
> components in the heart.
> 3.3 Basic DDD Pacemaker Modeling
> The DDD pacemaker has 5 basic timing cycles triggered by events, as shown
> in Fig. 2(b). We decomposed our pacemaker model into 5 components which
> correspond to the 5 counters. These com ponents communicate with each other
> using broadcast channels and shared variables (as shown in Fig. 3).
> Lower Rate Interval (LRI): This component keeps the heart rate above a
> minimumvalue.InDDDmode,theLRIcomponentmodelsthebasictimingcycle
> which deﬁnes the longest interval betw een two ventricular events. The clock is
> reset when a ventricular event (VS, VP) is received. If no atrial event has been
> sensed (AS), the component will deliver atrial pacing (AP) after TLRI-TAVI.
> The UPPAAL design of LRI component is shown in Fig. 3(a).

#### 摘录 B
- 出处：第 5-6 页，AVI/URI/PVARP/VRP 描述，行 192-215
> Atrio-Ventricular Interval (AVI) and Upper Rate Interval (URI): The
> function of the AVI component is to maintain the appropriatedelay between the
> atrial activation and the ventricular activation. It deﬁnes the longest interval
> between an atrial event and a ventricular event. If no ventricular event has been
> sensed (VS) within TAVI after an atrial event (AS, AP), the component will
> deliver ventricular pacing (VP). In orde r to prevent the pacemaker from pacing
> the ventricle too fast, a URI component uses a global clock clkto track the time
> after a ventricular event (VS, VP). The URI limits the ventricular pacing rate
> by enforcing a lower bound on the times between consecutive ventricle events.If the global clock value is less than TURI when the AVI component is about to
> deliver VP, AVI will hold VP and deliver it after the global clock reaches TURI.
> The UPPAAL design of AVI and URI component is shown in Fig. 3(b) and (c).
> Post Ventricular Atrial Refractory Period (PVARP) and Post Ventric-
> ular Atrial Blanking (PVAB): Not all atrial events ( Aget!) are recognized
> as Atrial Sense ( AS!). After each ventricular event, there is a blanking period
> (PVAB) followed by a refractory period (PVARP) for the atrial events in orderto ﬁlter noise. Atrial events during PVAB are ignored and atrial events dur-
> ing PVARP trigger AR!event which can be used in some advanced diagnostic
> algorithms. The UPPAAL design of PVARP component is shown in Fig. 3(d).
> 
> --- Page 6 ---
> Modeling and Veriﬁcation of a Dual Chamber Implantable Pacemaker 193
> Ventricular Refractory Period (VRP): Correspondingly, the VRP follows
> each ventricular event (VP, VS) to ﬁlter no ise and early events in the ventricular
> channel which could otherwise cause undesired pacemaker behavior. Fig. 3(e)
> shows the UPPAAL design of VRP component.

#### 摘录 C
- 出处：第 6 页，Parameter Selection，行 216-221
> Parameter Selection: Each timing parameter of the pacemaker has a feasible
> range. However, after those parameters are programmed, they are ﬁxed during
> pacemaker operation. Consider all possible combinations of feasible parameter
> valuesisinfeasible.In thiswork,weonlyverifyoneinstanceofaDDD pacemaker
> with nominal values in clinical settings [8]. The values we choose are TAVI=150,
> TLRI=1000, TPVARP=100, TVRP=150, TURI=400, TPVAB=50.

### 2. 基于原文整理后的自然语言描述

The DDD pacemaker is decomposed into five event-triggered timing components that communicate through broadcast channels and shared variables while sensing Aget!/Vget! events from the heart and issuing AP!/VP! pacing actions. The LRI component is reset by each ventricular event (VS or VP) and, if no atrial sense occurs, delivers AP after TLRI-TAVI so that the ventricular interval never exceeds the lower-rate limit. After an atrial event (AS or AP), the AVI component waits up to TAVI for a ventricular sense and delivers VP if none arrives, while the URI component uses the global clock clk after each ventricular event and holds that VP until the lower bound TURI is satisfied. After every ventricular event, PVAB first blanks atrial events, then PVARP continues the refractory window so that atrial events in that interval become AR rather than AS, and VRP separately filters noise and early ventricular events on the ventricular channel. In the verified clinical instance, the nominal timing parameters are TAVI = 150, TLRI = 1000, TPVARP = 100, TVRP = 150, TURI = 400, and TPVAB = 50.

### 3. 逐句溯源

1. 句子 1：The DDD pacemaker is decomposed into five event-triggered timing components that communicate through broadcast channels and shared variables while sensing Aget!/Vget! events from the heart and issuing AP!/VP! pacing actions.
   对应摘录：A
2. 句子 2：The LRI component is reset by each ventricular event (VS or VP) and, if no atrial sense occurs, delivers AP after TLRI-TAVI so that the ventricular interval never exceeds the lower-rate limit.
   对应摘录：A
3. 句子 3：After an atrial event (AS or AP), the AVI component waits up to TAVI for a ventricular sense and delivers VP if none arrives, while the URI component uses the global clock clk after each ventricular event and holds that VP until the lower bound TURI is satisfied.
   对应摘录：B
4. 句子 4：After every ventricular event, PVAB first blanks atrial events, then PVARP continues the refractory window so that atrial events in that interval become AR rather than AS, and VRP separately filters noise and early ventricular events on the ventricular channel.
   对应摘录：B
5. 句子 5：In the verified clinical instance, the nominal timing parameters are TAVI = 150, TLRI = 1000, TPVARP = 100, TVRP = 150, TURI = 400, and TPVAB = 50.
   对应摘录：C

## 条目 2: Mode-switch algorithm between DDD and VDI
- 控制对象：双腔起搏器的模式切换控制
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是植入式心脏起搏领域的模式切换控制器，用于在快速房性节律出现时把起搏器从双腔模式切到单腔后备模式并在恢复后切回。
- 判断：算。它描述的是实际医疗设备的模式管理逻辑，进入、维持和退出条件都可直接追溯到原文。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9-10 页，Section 5.2 “Mode-Switch Algorithm”，行 360-414
> Mode-Switch Algorithm: Intuitively, the mode-switch algorithmﬁrst detects
> SVT. After conﬁrmed detection, it switch es the pacemaker from a dual-chamber
> mode to a single-chamber mode. During the single-chamber mode, the A-V syn-
> chrony function of the pacemaker is deactivated thus the ventricular rate is
> decoupled from the fast atrial rate. After the algorithm determines the end of
> SVT, it will switch the pacemaker back to the dual chamber mode.
> The mode-switch algorithm speciﬁcation we use is the same as the one used
> in Boston Scientiﬁc pacemakers [8]. The algorithm ﬁrst measures the interval
> between atrial events outside the blanking period (AS, AR). The interval is
> considered as fastif it is above a threshold ( Trigger Rate )a n d slowotherwise
> (see Fig. 8 (1)). A counter increments for fastevents and decrement for slow
> events (see Fig. 8 (2)). After the counter value reaches the Entry Count ,t h e
> algorithm will start a Duration which is a time interval used to conﬁrm the
> detection of SVT (see Fig. 8 (3)). In the Duration , the counter keeps counting. If
> the counter value is still positive after the Duration , the pacemaker will switch
> to the VDI mode ( Fallback mode ). In the VDI mode, the pacemaker only senses
> and paces the ventricle. At any time if the counter reaches zero, the Duration
> will terminate and the pacemaker is switched back to DDD mode.
> In our UPPAAL model of the mode-switch algorithm, we use nominal param-
> eter values from the clinical setting. We deﬁne trigger rate at 170bpm (350ms),
> entry count at 8, duration for 8 ventricular events and fallback mode as VDI.
> In orderto modelbothDDD andVDI modesandtheswitchingbetweenthem,
> we made modiﬁcations to the AVI and LRI components. In each component
> Counter
> Fast?
> C
> CSlow?
> du_end?
> DDD!
> VDI!
> du_beg!
> Duration
> VS?
> D
> D
> VP?
> du_beg?
> du_end!
> Interval
> AS?
> AR?
> AP?
> Fast!
> Slow! 1 
> 2 
> 3 
> Fig. 8.Mode-Switch algorithm
> 
> --- Page 10 ---
> Modeling and Veriﬁcation of a Dual Chamber Implantable Pacemaker 197
> two copies for both modes are modeled, and switch between each other when
> switchingevents(DDD, VDI) arereceived.During VDI mode, VPisdeliveredby
> the LRI component instead of the AVI co mponent. The clock values are shared
> between both copies in order to preserve esse ntial intervals even after switching.
> The modiﬁed AVI and LRI components are shown in Fig. 9.

### 2. 基于原文整理后的自然语言描述

When sustained fast atrial activity is confirmed, the mode-switch algorithm changes the device from dual-chamber operation to the single-chamber fallback mode VDI so that ventricular timing is no longer driven by the fast atrial rate. To make that decision, it measures intervals between atrial events outside the blanking period (AS, AR), classifies each interval as fast or slow against the Trigger Rate threshold, increments the counter for fast intervals, decrements it for slow intervals, and starts a Duration confirmation window once the counter reaches the Entry Count. In the verified UPPAAL instance, the trigger rate is 170 bpm (350 ms), the entry count is 8, the duration spans 8 ventricular events, and fallback mode is VDI. If the counter is still positive after Duration, the pacemaker switches to VDI; if the counter reaches zero at any time, Duration terminates and the pacemaker switches back to DDD. In the model, AVI and LRI each have duplicated DDD and VDI copies that switch on DDD!/VDI! events, VP is delivered by LRI rather than AVI in VDI mode, and shared clocks preserve essential timing intervals across the mode change.

### 3. 逐句溯源

1. 句子 1：When sustained fast atrial activity is confirmed, the mode-switch algorithm changes the device from dual-chamber operation to the single-chamber fallback mode VDI so that ventricular timing is no longer driven by the fast atrial rate.
   对应摘录：A
2. 句子 2：To make that decision, it measures intervals between atrial events outside the blanking period (AS, AR), classifies each interval as fast or slow against the Trigger Rate threshold, increments the counter for fast intervals, decrements it for slow intervals, and starts a Duration confirmation window once the counter reaches the Entry Count.
   对应摘录：A
3. 句子 3：In the verified UPPAAL instance, the trigger rate is 170 bpm (350 ms), the entry count is 8, the duration spans 8 ventricular events, and fallback mode is VDI.
   对应摘录：A
4. 句子 4：If the counter is still positive after Duration, the pacemaker switches to VDI; if the counter reaches zero at any time, Duration terminates and the pacemaker switches back to DDD.
   对应摘录：A
5. 句子 5：In the model, AVI and LRI each have duplicated DDD and VDI copies that switch on DDD!/VDI! events, VP is delivered by LRI rather than AVI in VDI mode, and shared clocks preserve essential timing intervals across the mode change.
   对应摘录：A
