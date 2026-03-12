# Design of Elevator Control System Based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文用工作流形式描述了电梯的初始楼层、呼叫响应、开门/关门、行程开关反馈、自动/手动切换与异常呼叫，足以形成完整的上层模式控制描述。

## 条目 1: PLC elevator workflow with automatic and manual operation
- 控制对象：PLC 电梯系统的工作流与模式控制

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电与电梯控制领域的电梯上层工作流控制器，用于处理呼梯按钮、车门开闭、行程开关反馈、自动控制与手动安全操作。
- 判断：算。对象是实际电梯控制系统，工作流描述对应的是轿厢运行与门控行为，不是开发流程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，`3.2 PLC control system workflow`，行 100-126
> The working flow of PLC in the elevator control system is as follows: (1) When the PLC is
> connected to the elevator control system, the elevator is located on the first floor of the building,
> and can receive the information of each call button in the control system to facilitate the
> corresponding response.(2) When the elevator stops at any floor, the upper and lower call buttons of
> the floor can send the door opening information to the control system to control the movement of
> the elevator and the opening of the door, which will form a certain delay operation to effectively
> ensure the safety of the elevator. In addition, the elevator control system can receive another
> operation at the same time when performing one operation, that is, the above instructions will be
> repeatedly executed according to the system structure programming during operation.(3) The key in
> the elevator control system, as the information input device of the control system, will light up the
> corresponding call light after receiving the instruction, and form the execution command feedback
> to turn off the light after completing the corresponding operation.(4) A travel controller will be
> provided in the shaft of each floor of the elevator. When the car reaches the floor, it will touch the
> switch of the travel controller, and then let the system perceive that it has reached the command
> specified area, and form the corresponding output operation.(5) In addition to the automatic control
> according to the button call instruction command, the switch function of the elevator is also
> provided with a manual operation button to ensure the safety of the elevator operation, and the
> self-locking function cannot be opened or closed during the elevator operation.(6) During the
> operation of the elevator, each floor to which the car travels will display the corresponding floor
> indication number in the prompt area to achieve information feedback on the operation process.(7)
> In order to ensure the safety of the elevator in operation, the car is equipped with an emergency call
> button. The button has a communication function, which can be used to contact the elevator control
> system center or the property when the elevator operation is abnormal, and conduct real-time

### 2. 基于原文整理后的自然语言描述

When the PLC elevator controller is initialized, the car starts from the first floor and waits for call-button information. If the elevator stops at a floor, the call buttons on that floor can trigger door-opening information, and the controller inserts a delay to keep the operation safe before continuing with movement. As the car travels, the corresponding call light is turned on and then cleared after the requested operation is completed, and a travel-controller switch at each floor confirms that the car has reached the commanded area. The system supports automatic execution of button-call commands together with a manual operation function for safety, keeps the door self-locking function unavailable during car movement, displays the current floor during operation, and provides an emergency call button for abnormal situations.

### 3. 逐句溯源

1. 句子 1：When the PLC elevator controller is initialized, the car starts from the first floor and waits for call-button information.
   对应摘录：A
2. 句子 2：If the elevator stops at a floor, the call buttons on that floor can trigger door-opening information, and the controller inserts a delay to keep the operation safe before continuing with movement.
   对应摘录：A
3. 句子 3：As the car travels, the corresponding call light is turned on and then cleared after the requested operation is completed, and a travel-controller switch at each floor confirms that the car has reached the commanded area.
   对应摘录：A
4. 句子 4：The system supports automatic execution of button-call commands together with a manual operation function for safety, keeps the door self-locking function unavailable during car movement, displays the current floor during operation, and provides an emergency call button for abnormal situations.
   对应摘录：A
