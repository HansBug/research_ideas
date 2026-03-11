# Teaching Finite State Machines (FSMs) as Part of a PLC Course - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：三步 box-fill 过程和外层 auto/standby 控制都可直接写成自然语言流程。

## 条目 1: Three-state box fill FSM
- 控制对象：PLC 控制的 box fill 子过程

### 0. 条目识别与判定

- 一句话说明：这是离散制造与 PLC 顺序控制领域的箱体灌装子过程，用于驱动输送机与填充装置完成找箱、灌装和移走满箱。
- 判断：算。虽然它是教学型小规模案例，但对象仍是实际设备子过程控制，顺序阶段和切换条件都很清楚。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5-6 页，Figure 3 前后的 box fill 状态说明，行 151-177
> A state machine diagram is given in Figure 3.  Ther e are three states.  The author’s practice is to nu mber 
> the states by tens to allow for modifications.  In state 10 the conveyor is running and we are looking  for 
> an empty box as indicated by the proximity switch.  In state 20 the box is filled until the level swit ch is 
> made.  In state 30 the conveyor runs until the prox imity switch clears indicating the full box is gone .  The 
> transition from standby is made to state 30 so that  if there is a box on the conveyor it is removed be fore 
> the fill operation begins.   
>  
> 
> 
> --- Page 6 ---
>  
> Figure 3 A state diagram for a three state FSM for a box fill operation 
>  
> The system can be in auto or standby, and for safet y includes a Normally Open (NO) contact from an 
> external estop relay.  The auto standby circuit is operated by an NO Pushbutton (PB) for auto start, a nd a 
> Normally Closed (NC) PB for stop.  This two state a uto/standby FSM is shown in rung one of Figure 4.  
> Note that rung one is a two state FSM and rungs two  through four are a separate three state FSM.  The 
> outputs on rungs five and six are combinational log ic.   
>  
> Coil C101 is a state because it is dependent on the  previous value of C101, C102, and C103.  Coil C102  is 
> a state because it depends on the previous scan val ue of C102, and C103.  In Rung four the new values 
> from the current scan are available for C101, and C 102, but the previous scan value for C103 is used 
> making C103 a state. 
>  
> One might argue that because coils C101, C102, and C103 are states that the outputs Y001, and Y002 are  
> also states.  This is not the case.  The outputs ar e dependent on the values of the state coils comput ed 
> on the current cycle, not on the previous cycle.  T hus the outputs are combinational, not states.   

#### 摘录 B
- 出处：第 9 页，state 20/30 与输出说明，行 219-245
> The state is exited when a new state is activated.  A NC contact for each exit state is placed in seri es with 
> the permissive and the seal in.  There is one NC ex it contact for each outgoing arrow in the state 
> diagram.   
> An FSM can have entry chores, exit chores, state ch ores, etc.  In Figure 4 the state chores are the 
> outputs Y001, and Y002.  There are no entry or exit  chores but if there were they could be activated 
> using transitional contacts.  The generic form of F igure 5 may not cover every aspects of a traditiona l 
> FSM but it does cover all of the items necessary fo r a PLC sequence. 
> A complete description of states 20, 30, and the ou tputs in Figure 4 follows.  State 20 is the box fil l state.  
> If the box is loading and the proximity switch is a ctivated the state 20 coil, C102 energizes.  This d rops 
> out the C101 coil, and C102 seals in the fill state .  The fill state is complete when state 30 is ener gized. 
> In state 30 there are two entry conditions.  The fi rst condition has no from-state, but it does have e ntry 
> logic.  If the system is in auto and there is no ac tive state coil C103 is energized, and seals in.  T hus on 
> the transition to auto the conveyor starts and runs  until the proximity clears.  The second path into state 
> 30 is from-state 20.  When in state 20 and the leve l switch activates the box is full and the FSM move s to 
> state 30.  The exit condition for state 30 is state  20. 
> Finally the outputs Y001 conveyor run in auto, and Y002 box fill are functions of the states.  The 
> conveyor runs in state 10 load box, and state 30 re move box.  The box fill output Y002 is energized wh en 
> in state 20.  The logic for the outputs is combinat ional. 
> The logic of Figure 4 represents a sub-process.  A typical PLC application might consists of dozens of  
> small sub-processes like this.  When combined they can control a complete process or multiple process.   
> Each sub-process consists of three components, entr y logic which is combinational, the FSM, and the 
> output logic which is also combinational.  This for mat promotes robust design, programming, and 
> maintenance of the PLC system. 
> For a sub-process the entry logic might consist of combinations of permissive, input devices, and 
> contacts from other sub-processes.  The FSM contain s the state logic.  The output logic is combination al 
> and generates internal coils which go to other sub- processes, and external coils which go to solenoid 
> valves, motor starters, and other external devices.  

### 2. 基于原文整理后的自然语言描述

During automatic box filling, the conveyor first looks for an empty box, then keeps the box in place while it is filled, and then runs again until the full box clears the proximity switch. The sequence begins by moving into the remove-box portion when coming out of standby so that any box already on the conveyor is cleared before filling starts. When the level switch indicates that the box is full, the process advances to the remove-box portion, and the conveyor-run and box-fill outputs follow whichever part of the sequence is active.

### 3. 逐句溯源

1. 句子 1：During automatic box filling, the conveyor first looks for an empty box, then keeps the box in place while it is filled, and then runs again until the full box clears the proximity switch.
   对应摘录：A, B
2. 句子 2：The sequence begins by moving into the remove-box portion when coming out of standby so that any box already on the conveyor is cleared before filling starts.
   对应摘录：A
3. 句子 3：When the level switch indicates that the box is full, the process advances to the remove-box portion, and the conveyor-run and box-fill outputs follow whichever part of the sequence is active.
   对应摘录：B

## 条目 2: Auto/standby permissive around the sequence
- 控制对象：PLC 子过程外层的 auto/standby 控制

### 0. 条目识别与判定

- 一句话说明：这是离散制造与 PLC 顺序控制领域的上层运行许可回路，用于在 auto 和 standby 之间切换并决定箱体灌装子过程是否允许运行。
- 判断：算。它管理的是设备子过程的运行模式和安全许可，本质上就是上层模式控制逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，对 auto/standby circuit 的描述，行 164-168
> The system can be in auto or standby, and for safet y includes a Normally Open (NO) contact from an 
> external estop relay.  The auto standby circuit is operated by an NO Pushbutton (PB) for auto start, a nd a 
> Normally Closed (NC) PB for stop.  This two state a uto/standby FSM is shown in rung one of Figure 4.  
> Note that rung one is a two state FSM and rungs two  through four are a separate three state FSM.  The 
> outputs on rungs five and six are combinational log ic.   

### 2. 基于原文整理后的自然语言描述

The outer permissive for this sub-process lets the system be either in auto or in standby and includes the estop contact for safety. The auto/standby circuit is operated by an auto-start pushbutton and a stop pushbutton, and it encloses the separate three-step box-fill sequence.

### 3. 逐句溯源

1. 句子 1：The outer permissive for this sub-process lets the system be either in auto or in standby and includes the estop contact for safety.
   对应摘录：A
2. 句子 2：The auto/standby circuit is operated by an auto-start pushbutton and a stop pushbutton, and it encloses the separate three-step box-fill sequence.
   对应摘录：A
