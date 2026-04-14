# A Microcontroller Operated LASER based Railway Gate and Signal Controlling System with Efficient Accident Prevention Strategy via IP-Webcam related Video-Surveillancing - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `激光到车检测 -> 倒计时 -> 关门 -> 通过后开门` 主链和 `PIR` 障碍停车分支一起写成了 8 步算法，原文与描述都足以维持双 A。

## 条目 1: Laser-countdown railway gate with PIR-triggered train stop

- 控制对象：轨道交通与铁路控制领域的激光触发道口关门、倒计时提示与 PIR 障碍停车控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个铁路道口门控与事故预防系统，用激光模块检测列车到来、LCD 倒计时和摄像头显示列车位置，并用 `PIR` 传感器在有人闯入轨道时触发减速停车。
- 判断：算。对象是实际铁路道口控制器，原文不只写装置组成，还明确给出了从发车、检测、倒计时、关门到列车通过后复位的 8 步顺序，以及障碍物分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`Abstract`，`paper_content.txt` 第 20-31 行
> The objective of our proposed work is to provide an automatic railway gate at a level crossing replacing the gates operated by the gatekeeper. ... the arrival of the train is detected by the laser light module placed near to the gate and people can aware the position of the train by cctv feature using Arducam mini camera. Hence, the time for which it is closed is less compared to the manually operated gates and also reduces the human labour. ... if a person suddenly comes in front of a running train, train detects the presence of the person by using passive infrared sensor (PIR sensor) ... and it reduces its motion and finally stops.

#### 摘录 B

- 出处：第 2-3 页，`Introduction / Our Proposed Work`，`paper_content.txt` 第 42-47、64-71 行
> In this project we detect the arrival of train and warn the road users about the arrival of train by timer in the LCD screen.
>
> In our proposed work we use laser light module (transmitter and receiver) for the arrival of train ... count down process and message printing on a lcd screen make our project more fruitful ... the timer on the lcd screen will prevent the sudden fall down of the railway gate on the vehicle or car or human beings. Prevention of an accident can be solved in such a way that when the train detects the presence of people in front of the train using PIR sensor the speed of the train gradually decreases and the speed controller will help to reduce the speed and finally the train will stop.

#### 摘录 C

- 出处：第 7 页，`Proposed Algorithm For Our Proposed System`，`paper_content.txt` 第 268-284 行
> Step 1: At first the signal of train is red and after some time the train starts its journey and at that moment the railway gate lifts up.
>
> Step 2: When the train cuts the laser light module the buzzer sounds on and the signal of the train becomes green from red.
>
> Step 3: After that count down starts on lcd screen and the position of the train from the gate is displayed on screen using arducam mini camera.
>
> Step 4: After finishing of the count down a message “the train is coming” is printed on the lcd screen and if any human being comes in front of the train then go to step 5 otherwise go to step 6.
>
> Step 5: The speed of the train decreases gradually and the buzzer sounds on and red led light becomes on and train stops.
>
> Step 6: Next the railway gate pulls down and a message is printed on the lcd screen “the train has passed”.
>
> Step 7: After passing of train to the railway gate, the gate lifts up and buzzer sounds off.
>
> Step 8: The signal of the train becomes red from green.

#### 摘录 D

- 出处：第 7-8 页，`Experiment and Results / Conclusion`，`paper_content.txt` 第 288-294、309-314 行
> People can aware the position of the train by cctv features using Arducam mini camera and the timer in the lcd screen will help them to get the minimum time to cross the railway gate. In our project if any human being come infront of the running train then PIR sensor will detect it and the speed of the train will decrease gradually and finally the train will stop. Now if the train has stopped suddenly then the train will not control its speed and the coaches of the train will be derailed from the track. So here we use speed controller to control the speed of the train.
>
> The circuit was able to control the railway gate precisely. The circuit was tested in both direction and worked perfectly. By using laser module we were able to achieve a fast response.

### 2. 基于原文整理后的自然语言描述

The railway controller starts from a state where the train signal is red and the gate is up, and it waits for the approaching train to break the laser transmitter-receiver path near the crossing. Once the laser path is cut, the controller turns the train signal green, activates the buzzer, starts an LCD countdown, and shows the train position through the `Arducam` video feed so road users can see the incoming train. After the countdown finishes, the system checks the hazard branch: if the `PIR` sensor detects a person in front of the moving train, the controller turns on the red LED, keeps the buzzer active, and gradually reduces the train speed until it stops. Otherwise the controller pulls the railway gate down and announces the train passage on the LCD. After the train has crossed the gate, the barrier lifts again, the buzzer is switched off, and the train signal returns from green to red.

### 3. 逐句溯源

1. 句子 1：The railway controller starts from a state where the train signal is red and the gate is up, and it waits for the approaching train to break the laser transmitter-receiver path near the crossing.
   对应摘录：A, C
2. 句子 2：Once the laser path is cut, the controller turns the train signal green, activates the buzzer, starts an LCD countdown, and shows the train position through the `Arducam` video feed so road users can see the incoming train.
   对应摘录：A, B, C
3. 句子 3：After the countdown finishes, the system checks the hazard branch: if the `PIR` sensor detects a person in front of the moving train, the controller turns on the red LED, keeps the buzzer active, and gradually reduces the train speed until it stops.
   对应摘录：A, B, C, D
4. 句子 4：Otherwise the controller pulls the railway gate down and announces the train passage on the LCD.
   对应摘录：B, C
5. 句子 5：After the train has crossed the gate, the barrier lifts again, the buzzer is switched off, and the train signal returns from green to red.
   对应摘录：C, D
