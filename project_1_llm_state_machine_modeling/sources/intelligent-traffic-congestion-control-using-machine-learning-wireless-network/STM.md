# Intelligent Traffic Congestion Control System using Machine Learning and Wireless Network - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `视觉检测 -> 服务器判决 -> 当前路口放行 -> 相邻路口联动` 和 `救护车优先 / 超过 10 辆车的拥堵优先` 两类规则写得足够完整，能稳定形成双 A 样本。

## 条目 1: Camera-count threshold traffic-light preemption controller

- 控制对象：道路交通信号控制领域的摄像头车流计数、救护车优先与相邻路口联动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `camera + server + ESP32 + wireless network` 的交通灯控制系统，用视觉检测识别车流密度和救护车，再由控制器决定当前路口与相邻路口的绿灯放行。
- 判断：算。对象是实际交通灯控制器，原文明确给出了服务器、微控制器和相邻路口之间的控制分工，以及“救护车优先”和“某一方向超过 10 辆车时优先放行”两条决策规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 32-44 行
> In this paper, we propose an intelligent, low cost, and efficient microcontroller circuit-based system for controlling cars in traffic light. This system can manage car traffics smarter than traditional approaches, it is capable to dynamically adjust timings of traffic signal. ... The system uses machine learning technique (i.e.,Yolov3 model and OpenCV) for decision depending on existence of emergency cars and number of cars.

#### 摘录 B

- 出处：第 3-4 页，`System Hardware / Proposed Model`，`paper_content.txt` 第 185-198、221-224、292-305 行
> ESP32 Nodemcu ... has been used to control the traffic light based on the data received from the server (i.e., number of cars and detecting ambulance). Moreover, it is used to communicate with next traffic light through wireless communication.
>
> Received data then send to microcontroller to make decision to open the lane or no.
>
> The proposed system mainly works based on relation between a server computer and ESP32 Nodemcu open-source microcontroller. The server receives car videos through attached cameras, to be used for car identification and counting car numbers in each lane at the same time. The microcontroller side controls all the operations of the electronic circuits connected to its digital input and output pins.

#### 摘录 C

- 出处：第 5 页，`Proposed Model`，`paper_content.txt` 第 299-318 行
> Video cameras are used for inputting real-time video to the server ... detecting ambulance car. The microcontroller, in turn, reacts depending on emergency car existence on the road sides by changing light sign to green and send command to next neighbor traffic light via wireless communication to change it to green sign.
>
> The decision will be trigger in two cases: First, in case, if ambulance is detected on a side, the system automatically decides to open this side (i.e., change the light from red to green) to let it pass the traffic light soon and it communicates with next traffic light through wireless network to change the light to green too. Second, also in case, if the amount of waiting cars in one side exceeded 10 cars and other sides are empty automatically change this side light to green.

#### 摘录 D

- 出处：第 5-8 页，`System Algorithm / Conclusion`，`paper_content.txt` 第 320-334、387-401 行
> First step, the model sets its parameters. Then, continually images sent to the server through attached camera and image processing in the server side will start. Later, image detection begins by distinguishing emergency car from normal car, if received image was for emergency car (i.e., ambulance) or number of cars at a lane reached 10 then the server notifies the microcontroller to change the traffic light to green. In the same time, it communicates with next traffic light to change light to green to let the emergency car pass overall interactions. Otherwise, the system continues in a loop and gets new images.
>
> The system can recognize two types of car information, one of them is car type and the other is number of cars. Car type is used for distinguishing emergency car from normal car and number of cars is used for comparison among cars in each lane. In both cases, the system uses gathered information and gives priority to emergency cars over normal car and crowded lane to empty lane. Another feature of this system is that the traffic lights communicate together through wireless medium to gives priority to emergency car.

### 2. 基于原文整理后的自然语言描述

The intelligent traffic-light controller is organized as a server-and-microcontroller loop in which cameras continuously send live road images to a server, and the server uses `Yolov3` plus `OpenCV` to classify emergency vehicles and count normal cars in each lane. The server then notifies the `ESP32 Nodemcu` controller, which directly drives the current traffic-light hardware and also communicates with the next traffic light through the wireless network. The first decision branch is emergency preemption: if an ambulance is detected on one side, the controller changes that side from red to green and simultaneously commands the next neighbor traffic light to green so the emergency vehicle can pass across successive intersections. The second branch is congestion relief: if one side has more than `10` waiting cars while the other sides are empty, that crowded side is switched to green automatically. If neither condition is satisfied, the system keeps looping, acquiring new images and preserving the ordinary traffic-light operation until one of the two rule conditions becomes true.

### 3. 逐句溯源

1. 句子 1：The intelligent traffic-light controller is organized as a server-and-microcontroller loop in which cameras continuously send live road images to a server, and the server uses `Yolov3` plus `OpenCV` to classify emergency vehicles and count normal cars in each lane.
   对应摘录：A, B, D
2. 句子 2：The server then notifies the `ESP32 Nodemcu` controller, which directly drives the current traffic-light hardware and also communicates with the next traffic light through the wireless network.
   对应摘录：B, C, D
3. 句子 3：The first decision branch is emergency preemption: if an ambulance is detected on one side, the controller changes that side from red to green and simultaneously commands the next neighbor traffic light to green so the emergency vehicle can pass across successive intersections.
   对应摘录：C, D
4. 句子 4：The second branch is congestion relief: if one side has more than `10` waiting cars while the other sides are empty, that crowded side is switched to green automatically.
   对应摘录：C, D
5. 句子 5：If neither condition is satisfied, the system keeps looping, acquiring new images and preserving the ordinary traffic-light operation until one of the two rule conditions becomes true.
   对应摘录：D
