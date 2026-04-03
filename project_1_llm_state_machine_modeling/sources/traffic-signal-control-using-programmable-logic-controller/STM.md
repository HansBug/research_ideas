# Traffic Signal Control Using Programmable Logic Controller (PLC) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对车辆优先、行人计数触发 all-red、同发冲突时的近端优先和红绿灯联动栏杆控制都有明确文字说明，适合直接收录。

## 备注
- 原文对 zebra crossing 的行人阈值出现了 `10 people` 与 `fifty people` 两种写法；当前条目保守按“存在计数阈值触发 all-red 行人放行”整理，不臆测唯一数值。

## 条目 1: Vehicle and Pedestrian Aware Signal-and-Barrier Control
- 控制对象：路口交通灯与自动栏杆联动控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的 PLC 联动控制系统，用于依据车辆和行人传感输入控制信号灯与栏杆的开闭。
- 判断：算。对象是实际交通控制系统，原文给出了传感输入、红绿灯响应和栏杆联动逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Methodology，`paper_content.txt` 第 116-160 行
> The surface of the sheet was designed like an intersection of 4 way road and each road has two lanes ... At each road 3 eddy current displacement sensors were used. Their distance was different in the entire road. This sensor is used to sense vehicles.
>
> For zebra crossing eddy current displacement sensor which senses the human was used in every road. After sensing 10 people all signals was red as this people can cross the road. At each road automatic barrier was used. When the signal was red the barrier was closed that means no vehicle can break the traffic rules and when the signal was green the barrier was open.
>
> Timers, counters, shift registers, math functions are included in ladder logic to perform an operation ... The program is written on real time basis.

#### 摘录 B
- 出处：第 3-5 页，Methodology / Results and Discussion，`paper_content.txt` 第 185-207, 232-273 行
> Eddy current displacement sensor which senses human was using for zebra crossing in each road. It counted the people. Ladder logic with an up counter was programmed. Zebra crossing is opened when any of the sensor counts fifty people. To detect the vehicles eddy current displacement sensors were used and these sensors were placed at different position. In one road the sensor was 5 m distance from the intersection. In second road the distance was 7 m, in third road the distance was 9m and in forth road the distance was 11m. 4 automatic barriers were used to open and close the roads. It was connected with the green signal.
>
> The response time of the sensor was .01 sec. And the range of the sensors was 2 to 5 mm. ... The green or red signal depends on which sensor senses first.
>
> When the sensor in road A sensed first then the signal in that road was green and the automatic barrier was opened in that roads and the signal were red and the automatic barrier were closed in B, C and D roads. When two sensors in two roads sensed at same time then the sensor which was closed to the intersection was green and the signal of the other road was red and the other roads signal were also red. When the sensor in the road B sensed first, then road B was opened.

### 2. 基于原文整理后的自然语言描述

The PLC-controlled four-way intersection uses eddy-current vehicle sensors and proportionate signaling to decide which road receives green, while automatic barriers are tied to the signal state and stay closed on red and open on green. A zebra-crossing sensor counts pedestrians and, once its configured count threshold is reached, forces all traffic signals to red so the crossing can open. Vehicle sensors are placed at different distances from the intersection, and the road whose sensor fires first is opened while the other three roads remain red; if two roads are detected at the same time, the road with the sensor closer to the intersection wins and the other roads stay red. The sensor response time is about `0.01 s`, and the design maps separate green/red outputs to roads A, B, C, and D.

### 3. 逐句溯源

1. 句子 1：The PLC-controlled four-way intersection uses eddy-current vehicle sensors and proportionate signaling to decide which road receives green, while automatic barriers are tied to the signal state and stay closed on red and open on green.
   对应摘录：A, B
2. 句子 2：A zebra-crossing sensor counts pedestrians and, once its configured count threshold is reached, forces all traffic signals to red so the crossing can open.
   对应摘录：A, B
3. 句子 3：Vehicle sensors are placed at different distances from the intersection, and the road whose sensor fires first is opened while the other three roads remain red; if two roads are detected at the same time, the road with the sensor closer to the intersection wins and the other roads stay red.
   对应摘录：B
4. 句子 4：The sensor response time is about `0.01 s`, and the design maps separate green/red outputs to roads A, B, C, and D.
   对应摘录：B
