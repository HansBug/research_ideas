# Fault Handling in PLC-Based Industry 4.0 Automated Production Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：PackML/OMAC 模式与故障后恢复流程都能直接引用。

## 条目 1: Standardized machine-part operation modes
- 控制对象：PLC 机器部件的标准化 operation modes

### 0. 条目识别与判定

- 一句话说明：这是包装机械与工业自动化领域的机器部件控制模块，用于管理自动、设定、手动、半自动、初始化、关停和安全停机等运行方式。
- 判断：算。虽然它偏通用运行模式框架，但对象仍是机器部件的实际运行控制，原文也明确给出了有效模式和模式切换约束。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section 2.2，operation modes 与 OMAC/PackML，行 232-250
>  5 According  to Güttel  et al. [12] the main  operations  of function  blocks  include:  
>  Automatic  mode : defines  the behavior  of a machine part in automatic  mode.  
>  Setup  mode : defines  the behavior  of a machine part in setup  mode.  In this mode,  the drive  of a machine part 
> moves  as long as the manual  input  is active.  In this mode,  no interlocks  are active.  
>  Manual  mode:  defines  the behavior  in manual  mode.  In this mode,  the interlocks  are active.  
>  Semi -automatic  mode:  defines  the behavior  of a machine part in semi-automatic  mode.  
>  Initialize : defines  the behavior  during  the initialization  of the machine part. 
>  Shut  down : defines  the behavior  during  shutdown.  
>  Save  stop: defines  the actions  which  are necessary  to reach  a safe state.  
> The different  operation  modes  need  to be implemented,  which  may be realized  as additional  automata  or dif-
> ferent  branches  with the other  automata  according  to Fantuzzi  et al. [13].  In food & beverage  a more  sophist i-
> cated  standard  is used,  i.e. the OMAC  standard  or in Germany  the Weihenstephan  Standard  [14]. 
> The OMAC  State  Machine  [15] (cp. Figure  2) is part of the widespread  PackML  standard,  which  pursues  the 
> objective  to bring  operational  consistency  to a packaging  line, especially  if it consists  of packaging machines  
> from  different  vendors.  The PackML  standard defines  the OMAC  State  machine with 17 states  consisting  of 
> acting  and waiting  states  in which  acting  states  represent  activities  like starting  and waiting  states  identify  the 
> reaching  of a set of conditions  e.g. Held . The OMAC  State  Machine  is responsible  for identifying  valid  state 
> transitions  depending on the actual  OMAC  state and specified  state transition  conditions.  If a state change oc-
> curs,  a suitable  function  is called,  that is implemented  by the machine vendor  or integrator.  

### 2. 基于原文整理后的自然语言描述

The control software of a machine part is expected to cover automatic, setup, manual, semi-automatic, initialize, shutdown, and safe-stop operation. These operation modes may be implemented as separate automata or as branches inside other automata. In packaging applications, the OMAC state machine is used to keep operational consistency by identifying which state changes are valid and by calling the appropriate function when a change occurs.

### 3. 逐句溯源

1. 句子 1：The control software of a machine part is expected to cover automatic, setup, manual, semi-automatic, initialize, shutdown, and safe-stop operation.
   对应摘录：A
2. 句子 2：These operation modes may be implemented as separate automata or as branches inside other automata.
   对应摘录：A
3. 句子 3：In packaging applications, the OMAC state machine is used to keep operational consistency by identifying which state changes are valid and by calling the appropriate function when a change occurs.
   对应摘录：A

## 条目 2: Abort-reset-start return path
- 控制对象：包装机械模块在故障后的恢复控制过程

### 0. 条目识别与判定

- 一句话说明：这是包装机械与工业自动化领域的设备模块故障恢复控制流程，用于在故障停机后经人工处理、复位和重新启动把模块带回自动运行。
- 判断：算。它针对的是实际机器模块的故障后恢复控制，不是维护流程文档，且恢复路径由明确的模式序列组织起来。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9 页，标准化 mode switching 描述，行 398-404
>  9 “execute”,  “aborting”,  “aborted”,  “resetting”  and “starting”.  In automatic  mode,  the module  is executed  and ab-
> orted  in case of errors  resulting  in a failure  state (“aborted”)  which  requires  human interaction.  The resetting  is 
> done  by switching  to manual  mode,  used to resolve  process  errors,  followed  by an automatic  recalibration  of the 
> machine (“starting”),  which  is a prerequisite  for returning back  to automatic  mode.  Besides  the facility  module,  
> each application  module  possesses  these  different  operation  modes,  allowing  for sub-states  in the machine.  
> While  the OMAC  state machine is not used,  this procedure  of switching  between  machine operation  modes  and 
> thus states  is standardized  within  this company.  

#### 摘录 B
- 出处：第 9 页，Case study B 中的模块/错误/重启描述，行 405-437
> Case  study  B—Machinery  for Packaging  Industry  
> The example  in case study  B consists  of three  tasks  which  invoke  three  PRGs.  The task with the second  high-
> est priority  and its corresponding program  realize and call the main  functions  controlling  the technical  process  
> and are strongly  related  to the mechanical  layout  of the machine.  The mechanical  layout  consists  of one facility  
> module  and six main  application  modules,  which  is directly  reflected  within  the PLC control  software  archite c-
> ture (with  the exception  of several  additional  software  modules  being  used for facility -wide  functions,  e.g., for 
> error  management).  Each  application  module  includes  similar  subroutines,  such as parameterization  or axis 
> movement,  which  are implemented  differently  and mostly  include  additional  application  and basic  modules.  
> Furthermore,  encapsulated  FBs and functions  are used which  stem from  a supplier  delivering  and supporting 
> axes in particular.  The application  conforms  mostly  to the ISA-S88 and implements  the OMAC  state machine  
> model.   
> Fault  and alarm  handling may be considered  as being handled in a hierarchical  manner  (cp. Figure  3). On the 
> basic  module  level  the main  part of fault/error  detection  of hardware  and faults  stemming  from  the technical  
> process  is happening.  This is only logical  as, e.g., a pneumatic  cylinder  not reaching  its end position,  should  be 
> identified  by the basic  module  pneumatic  cylinder.  It allows  for easier  reuse,  as the mechanical  representation  
> has a direct  software  implementation.  However,  the error  ID is assigned  on the next higher  level  along with the 
> decision  on how the identified  error  should  be handled  (related  to the severity  of the error  in rising  order: only a 
> warning  is issued,  the machine is immediately  shut down).  The advantage  in this kind of setup  is that errors  are 
> assigned  to the correct  application  module  (e.g.,  which  pneumatic  cylinder  in which  module  is erroneous),  mak-
> ing error  identification  easier.  Furthermore,  if more  than one error  occurs  within  one application  module,  but 
> from  different  basic  or sub-application  modules,  an analysis  can be done  and group errors,  hinting  more  specif i-
> cally  at the cause of an error,  may be identified.  Group  errors  lead,  depending  on their severity,  to the shutdown 
> of the entire  machine group as they often  hint at specific  problems  in the specified  group  (area  of a machine).  In 
> the next step the errors  are analyzed  by separate functions,  apart  from  the application  modules  when  considering  
> the mechanical  layout.  The functions  collect  all errors  and implement  the error reaction.  If several  errors  arrive,  
> which  individually  would only be reported,  the error  reaction  of shutting  down  may for example be set. This 
> kind of setup  allows  for easy maintenance,  as the overall  error  management  functions  have  been  standardized  as 
> libraries  and can be reused  within  every  machine.  The error  detection  and error  reactions  are carried  out mainly  
> within  the second  task. The task with the lower  priority  executes  functions  related  to the HMI  (sending  the 
> alarms).  
> After  an error  that leads  to a shutdown has occurred  a function  for restarting  is available.  If the calibration  has 
> not been  impaired  by the shutdown and the material  is not entangled  somewhere  in the machine,  the operator  
> can decide  to acknowledge  the error  and restart  using  the implemented  function.  

### 2. 基于原文整理后的自然语言描述

In automatic operation, a module executes its process until an error aborts the module and places it in a failure condition that requires human intervention. Recovery is performed by switching to manual mode to resolve the process error, then recalibrating the machine in starting, and only afterwards returning to automatic mode. These standardized operation modes also exist on the application modules, so the machine behavior can be organized into sub-states that match the PLC control software architecture. After a shutdown-inducing error, a dedicated restart function can acknowledge the error and resume operation when calibration and material conditions allow it.

### 3. 逐句溯源

1. 句子 1：In automatic operation, a module executes its process until an error aborts the module and places it in a failure condition that requires human intervention.
   对应摘录：A
2. 句子 2：Recovery is performed by switching to manual mode to resolve the process error, then recalibrating the machine in starting, and only afterwards returning to automatic mode.
   对应摘录：A
3. 句子 3：These standardized operation modes also exist on the application modules, so the machine behavior can be organized into sub-states that match the PLC control software architecture.
   对应摘录：A, B
4. 句子 4：After a shutdown-inducing error, a dedicated restart function can acknowledge the error and resume operation when calibration and material conditions allow it.
   对应摘录：B
