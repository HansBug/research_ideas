# Safety analysis integration in a SysML-based complex system design process - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：轮刹系统的容错供压逻辑和相应安全要求可以直接成段。

## 条目 1: Wheel brake system fault-tolerant mode automaton
- 控制对象：飞机轮刹系统的容错供压逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空机载制动领域的飞机轮刹供压控制系统，用于在正常、备用和应急供压之间切换以持续维持制动能力。
- 判断：算。对象是实际飞机轮刹系统的容错控制逻辑，供压路径和失效后的退化方式都具有明确模式结构。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6-7 页，wheel brake system four modes and safety requirements，行 479-526
> To model this behavior, we consider four modes or states
> of the system that are:
> •Normal: when the Normal line is operated;
> •Alternate: activated when the Normal line fails and this
> failure is noted as failNormal ;
> •Emergency: activated when Alternate mode also fails
> (failAlternate ). The accumulator provides power source
> in this mode;
> •Fail: when all systems are in failure. The failure of the
> accumulator is noted as failEmergency .
> These modes and the corresponding transitions are modeled
> in an automata describing the dynamic behavior of the system
> including fault effects given by a SysML State Machine
> Diagram (see Fig.2).
> To satisfy the safety requirement SR, the wheel brake
> system shall be fault tolerant, i.e. it shall be able to brake
> the system even in presence of a certain number of failures.
> This can be translated, for instance, into the two safety
> requirements. These requirements are linked to corresponding
> test cases in a SysML Requirements Diagram (Fig.3).
> •SR1-WBS: When output is not supplied by Normal
> Fig. 2. Dynamic Behavior Including Faults Automata
> Line and there is no failure accounted in Alternate line,
> pressure shall be supplied from Alternate line;
> •SR2-WBS: When both Normal line and Alternate line
> are not producing output, as long as there is no failure
> accounted along the emergency line, the system shall not
> fail.
> Fig. 3. Safety Requirements in SysML
> Formal veriﬁcation is chosen to verify these requirements.
> For this the automata describing the dynamic behavior of
> the system in Fig.2 together with the requirements to be
> veriﬁed shall be translated into a NuSMV program. The
> safety requirements SR1-WBS and SR2-WBS are respectively
> speciﬁed by temporal formulas F1-WBS and F2-WBS:
> •F1-WBS: SPEC AG (( Normal.output = False AND Al-
> ternate.failAlternate = False)
> →
> Alternate.output =True).
> •F2-WBS: SPEC AG (( Normal.output = False) AND ( Al-
> ternate.output = False) AND ( Accumulator.failEmergency
> = False)
> →
> 5
> 
> --- Page 7 ---
> !(systemMode = Fail))
> Running the NuSMV program, these two properties are

### 2. 基于原文整理后的自然语言描述

The wheel brake system is modeled by four explicit modes: Normal, Alternate, Emergency, and Fail. The system stays in Normal while the normal hydraulic line operates, switches to Alternate when failNormal is detected, switches to Emergency when failAlternate is also detected so that the accumulator becomes the pressure source, and reaches Fail only when failEmergency occurs as well. These modes and transitions are the dynamic behavior that the authors encode in a SysML State Machine Diagram and then translate into a NuSMV model for formal verification. The linked safety requirements make the transition conditions operational: SR1-WBS requires Alternate.output = True whenever Normal.output = False and Alternate.failAlternate = False, and SR2-WBS requires !(systemMode = Fail) whenever both Normal and Alternate produce no output but Accumulator.failEmergency = False.

### 3. 逐句溯源

1. 句子 1：The wheel brake system is modeled by four explicit modes: Normal, Alternate, Emergency, and Fail.
   对应摘录：A
2. 句子 2：The system stays in Normal while the normal hydraulic line operates, switches to Alternate when failNormal is detected, switches to Emergency when failAlternate is also detected so that the accumulator becomes the pressure source, and reaches Fail only when failEmergency occurs as well.
   对应摘录：A
3. 句子 3：These modes and transitions are the dynamic behavior that the authors encode in a SysML State Machine Diagram and then translate into a NuSMV model for formal verification.
   对应摘录：A
4. 句子 4：The linked safety requirements make the transition conditions operational: SR1-WBS requires Alternate.output = True whenever Normal.output = False and Alternate.failAlternate = False, and SR2-WBS requires !(systemMode = Fail) whenever both Normal and Alternate produce no output but Accumulator.failEmergency = False.
   对应摘录：A
