# Formal Modeling and Verification of CTCS-2 Train Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 CTCS-2 车载设备的六模式转换、参与角色和若干安全侧性质集中写成了 UML 状态图与 NuSMV 验证对象，适合作为轨交模式管理样本。

## 条目 1: CTCS-2 On-Board Mode Conversion Manager
- 控制对象：轨道交通领域的 CTCS-2 车载设备模式转换控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个 CTCS-2 列控车载设备的模式管理器，用多角色事件交互和模式转换规则来保障车载设备在不同运行条件下切换到合适工作模式。
- 判断：算。对象是实际列控系统车载控制子系统，原文明确给出了六种工作模式、参与者之间的输入/输出事件、模式转换条件以及若干安全性质。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，`摘要 / Abstract`，`paper_content.txt` 第 16-19 行、第 24-30 行
> 由于CTCS-2级列控系统设计复杂，因此提出一种将统一建模语言(UML)与符号模型检验相结合的形式化建模与验证方法。分析CTCS-2级列控车载设备的模式转换场景，对其进行UML建模得到UML类图和状态图，制定转换规则对UML模型进行扩展和抽象，使其转化为NuSMV模型。将待验证的系统性质和转化后的检验程序输入符号模型检验系统进行验证，验证结果都为true，表明CTCS-2级列控车载设备的模式转化场景具有活性、可达性和安全性。
>
> It analyzes the mode conversion scene of CTCS-2 on-board equipment. The mode conversion scene of CTCS-2 on-board equipment is modeled by using the UML, and UML class diagrams and UML state diagrams are gotten as well ... The verified results are true, and it shows that mode conversion scene of CTCS-2 on-board equipment has activity, accessibility and security.

#### 摘录 B
- 出处：第 2 页，`3 列控车载设备的建模`，`paper_content.txt` 第 84-91 行
> 在CTCS-2级工作状态下，列控车载设备主要有6种工作模式，分别为待机模式SB、完全监控模式FS、部分监控模式PS、目视行车模式OS、调车监控模式SH、隔离模式IS。车载设备的工作模式是在一定条件下运用的，当条件发生改变时，工作模式也随之改变。

#### 摘录 C
- 出处：第 2-4 页，`UML 类图的建立 / 表1 / UML 状态转移图`，`paper_content.txt` 第 99-118 行、第 147-165 行
> DMI <<input>> VCMSG_AKEnterSH ... DMINotice_EnterSH ... Drive <<input>> DMINotice_EnterSH ... BNDOWN_ACKSH ... OnBoardEquipment ... mode:{sb,fs,ps,os,is,sh} ... Balise Train <<input>> EB TCC TCCMSG_SH ... STOPINSH ... External_Event OVERTIME ...
>
> 事件具体含义如表1所示。OVERTIME: 超时；TCCMSG_SH: 发送调车信息；VCMSG_AKEnterSH: 确认进入调车模式；BNDOWN_OpenDesk: 选择开启驾驶台；DMINotice_EnterSH: 显示进入调车模式；EnterVC_OpenDesk: 向车载报告驾驶台开启；BNDOWN_SH: 按压调车按钮；EB: 紧急制动；STOPINSH: 调车模式停车。
>
> 通过对模式转换的详细分析，模式转换的状态转移如图3所示，其中，C为司机操作命令；V为列车运行速度；T为轨道电路信息；B为应答器数据；Isolated为隔离；Normal为正常。图3中详细地描述了车载设备的模式转换过程，以及转换过程中的一些条件。列车启动后首先进入的是待机模式(SB)。其次根据条件，转换至不同的模式。

#### 摘录 D
- 出处：第 5 页，`模型验证结果分析`，`paper_content.txt` 第 195-210 行
> 表达式为 SPEC AG(in_FS)&(balise.Abnormal&(external_Event.env_TRAIN_STOP)&(!P1t1FS))->AX(in_PS))，表示当CTCS-2级列车运行控制系统的车载设备无法收到应答器信息时，车载系统的完全监控模式必须转化为部分监控模式。对此表达式进行验证，验证结果为 true，表明系统在此FS向PS模式转换过程中具有安全性。
>
> 验证程序中表达式为 SPEC AG(in_IS)，表示系统从任何一个模式都可进入隔离(IS)模式，将该表达式进行验证的结果为true，证明系统的IS模式具有活性。
>
> 表达式为 SPEC EF(State_i->State_j)，可达性验证的是系统在状态转移时是否存在不能到达的状态 ... 将该表达式进行验证，结果为 true，证明系统具有可达性。

### 2. 基于原文整理后的自然语言描述

The CTCS-2 on-board controller is modeled as a finite mode-conversion manager whose behavior is organized around the six working modes `SB`, `FS`, `PS`, `OS`, `SH`, and `IS`. It exchanges events with the driver, `DMI`, `TCC`, balise, train, and external environment, and the model explicitly includes interaction events such as `OVERTIME`, `EB`, `TCCMSG_SH`, `VCMSG_AKEnterSH`, `BNDOWN_OpenDesk`, and `STOPINSH` together with a mode variable on the on-board equipment object. Train startup first places the controller in standby mode `SB`, after which transitions are governed by driver command `C`, train speed `V`, track-circuit information `T`, balise data `B`, and normal or isolated operating conditions. The verified safety rules require, for example, that abnormal balise information under the `FS` supervision context forces a transition to `PS`, that any current mode can reach `IS`, and that the overall mode-conversion graph remains reachable, live, and safe.

### 3. 逐句溯源

1. 句子 1：The CTCS-2 on-board controller is modeled as a finite mode-conversion manager whose behavior is organized around the six working modes `SB`, `FS`, `PS`, `OS`, `SH`, and `IS`.
   对应摘录：A, B
2. 句子 2：It exchanges events with the driver, `DMI`, `TCC`, balise, train, and external environment, and the model explicitly includes interaction events such as `OVERTIME`, `EB`, `TCCMSG_SH`, `VCMSG_AKEnterSH`, `BNDOWN_OpenDesk`, and `STOPINSH` together with a mode variable on the on-board equipment object.
   对应摘录：C
3. 句子 3：Train startup first places the controller in standby mode `SB`, after which transitions are governed by driver command `C`, train speed `V`, track-circuit information `T`, balise data `B`, and normal or isolated operating conditions.
   对应摘录：C
4. 句子 4：The verified safety rules require, for example, that abnormal balise information under the `FS` supervision context forces a transition to `PS`, that any current mode can reach `IS`, and that the overall mode-conversion graph remains reachable, live, and safe.
   对应摘录：A, D
