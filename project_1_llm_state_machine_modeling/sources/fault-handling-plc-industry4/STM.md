# Fault Handling in PLC-Based Industry 4.0 Automated Production Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：PackML/OMAC 模式与故障后恢复流程都能直接引用，其中恢复链明显更适合作为主样本。

## 条目 1: Standardized machine-part operation modes
- 控制对象：PLC 机器部件的标准化 operation modes
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是包装机械与工业自动化领域的机器部件控制模块，用于管理 automatic、setup、manual、semi-automatic、initialize、shutdown 和 safe-stop 等运行方式。
- 判断：算。虽然它偏通用运行模式框架，但对象仍是机器部件的实际运行控制，原文明确给出了有效模式集合、层次实现方式和状态转换职责。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section 2.2，operation modes 与 OMAC/PackML，行 232-250
> According  to Güttel  et al. [12] the main  operations  of function  blocks  include:
> Automatic  mode : defines  the behavior  of a machine part in automatic  mode.
> Setup  mode : defines  the behavior  of a machine part in setup  mode.  In this mode,  the drive  of a machine part
> moves  as long as the manual  input  is active.  In this mode,  no interlocks  are active.
> Manual  mode:  defines  the behavior  in manual  mode.  In this mode,  the interlocks  are active.
> Semi -automatic  mode:  defines  the behavior  of a machine part in semi-automatic  mode.
> Initialize : defines  the behavior  during  the initialization  of the machine part.
> Shut  down : defines  the behavior  during  shutdown.
> Save  stop: defines  the actions  which  are necessary  to reach  a safe state.
> The different  operation  modes  need  to be implemented,  which  may be realized  as additional  automata  or dif-
> ferent  branches  with the other  automata  according  to Fantuzzi  et al. [13].
> ...
> The PackML  standard defines  the OMAC  State  machine with 17 states  consisting  of
> acting  and waiting  states  in which  acting  states  represent  activities  like starting  and waiting  states  identify  the
> reaching  of a set of conditions  e.g. Held . The OMAC  State  Machine  is responsible  for identifying  valid  state
> transitions  depending on the actual  OMAC  state and specified  state transition  conditions.  If a state change oc-
> curs,  a suitable  function  is called,  that is implemented  by the machine vendor  or integrator.

### 2. 基于原文整理后的自然语言描述

The control software of a machine part is expected to cover `automatic`, `setup`, `manual`, `semi-automatic`, `initialize`, `shutdown`, and `safe-stop` operation, and these modes imply different interlock policies such as setup motion under manual input without interlocks versus manual mode with interlocks active. The different operation modes may be implemented either as separate automata or as separate branches inside other automata. In packaging lines, PackML adopts the OMAC state machine with 17 states split into acting and waiting states, where acting states perform activities such as starting and waiting states denote that a condition such as `Held` has been reached. The OMAC state machine determines which transitions are valid from the current state under the specified transition conditions and calls the appropriate vendor-implemented function whenever a state change occurs.

### 3. 逐句溯源

1. 句子 1：The control software of a machine part is expected to cover `automatic`, `setup`, `manual`, `semi-automatic`, `initialize`, `shutdown`, and `safe-stop` operation, and these modes imply different interlock policies such as setup motion under manual input without interlocks versus manual mode with interlocks active.
   对应摘录：A
2. 句子 2：The different operation modes may be implemented either as separate automata or as separate branches inside other automata.
   对应摘录：A
3. 句子 3：In packaging lines, PackML adopts the OMAC state machine with 17 states split into acting and waiting states, where acting states perform activities such as starting and waiting states denote that a condition such as `Held` has been reached.
   对应摘录：A
4. 句子 4：The OMAC state machine determines which transitions are valid from the current state under the specified transition conditions and calls the appropriate vendor-implemented function whenever a state change occurs.
   对应摘录：A

## 条目 2: Abort-reset-start return path
- 控制对象：包装机械模块在故障后的恢复控制过程
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是包装机械与工业自动化领域的设备模块故障恢复控制流程，用于在故障停机后经人工处理、复位和重新启动把模块带回自动运行。
- 判断：算。它针对的是实际机器模块的故障后恢复控制，不是维护流程文档，且恢复路径由明确的模式序列和层次化错误处理组织起来。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9 页，标准化 mode switching 描述，行 398-404
> “execute”,  “aborting”,  “aborted”,  “resetting”  and “starting”.  In automatic  mode,  the module  is executed  and ab-
> orted  in case of errors  resulting  in a failure  state (“aborted”)  which  requires  human interaction.  The resetting  is
> done  by switching  to manual  mode,  used to resolve  process  errors,  followed  by an automatic  recalibration  of the
> machine (“starting”),  which  is a prerequisite  for returning back  to automatic  mode.  Besides  the facility  module,
> each application  module  possesses  these  different  operation  modes,  allowing  for sub-states  in the machine.

#### 摘录 B
- 出处：第 9 页，Case study B 中的模块/错误/重启描述，行 405-437
> Fault  and alarm  handling may be considered  as being handled in a hierarchical  manner.
> On the basic  module  level  the main  part of fault/error  detection  of hardware  and faults  stemming  from  the technical
> process  is happening.
> ...
> the error  ID is assigned  on the next higher  level  along with the
> decision  on how the identified  error  should  be handled  (related  to the severity  of the error  in rising  order: only a
> warning  is issued,  the machine is immediately  shut down).
> ...
> Group  errors  lead,  depending  on their severity,  to the shutdown
> of the entire  machine group.
> ...
> The functions  collect  all errors  and implement  the error reaction.
> ...
> After  an error  that leads  to a shutdown has occurred  a function  for restarting  is available.  If the calibration  has
> not been  impaired  by the shutdown and the material  is not entangled  somewhere  in the machine,  the operator
> can decide  to acknowledge  the error  and restart  using  the implemented  function.

### 2. 基于原文整理后的自然语言描述

In automatic mode, the module runs in `execute` until an error forces the sequence `execute -> aborting -> aborted`, and the `aborted` condition requires human intervention. Recovery is standardized as a return path through manual mode to resolve the process error, followed by automatic recalibration in `starting`, after which the module may go back to automatic operation. These operation modes also exist on each application module, so the machine behavior is organized as sub-states that mirror the PLC control software hierarchy. Fault and alarm handling is hierarchical: basic modules detect hardware/process faults, higher levels assign error IDs and decide whether to issue warnings or shut down a machine group, and separate error-management functions collect multiple errors to determine the final reaction. After a shutdown-causing error, a restart function may acknowledge the error and resume operation only if calibration is still valid and material has not become entangled in the machine.

### 3. 逐句溯源

1. 句子 1：In automatic mode, the module runs in `execute` until an error forces the sequence `execute -> aborting -> aborted`, and the `aborted` condition requires human intervention.
   对应摘录：A
2. 句子 2：Recovery is standardized as a return path through manual mode to resolve the process error, followed by automatic recalibration in `starting`, after which the module may go back to automatic operation.
   对应摘录：A
3. 句子 3：These operation modes also exist on each application module, so the machine behavior is organized as sub-states that mirror the PLC control software hierarchy.
   对应摘录：A
4. 句子 4：Fault and alarm handling is hierarchical: basic modules detect hardware/process faults, higher levels assign error IDs and decide whether to issue warnings or shut down a machine group, and separate error-management functions collect multiple errors to determine the final reaction.
   对应摘录：B
5. 句子 5：After a shutdown-causing error, a restart function may acknowledge the error and resume operation only if calibration is still valid and material has not become entangled in the machine.
   对应摘录：B
