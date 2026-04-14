# Design and Simulation of Small Space Parallel Parking Fuzzy Controller - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出了“先检测车位，再按 Ackerman 反向模型执行泊车”的流程，还补出了三输入一输出的模糊控制器、18 条规则和起始点约束对结果的影响。

## 条目 1: Parking-Space Detection and Reverse Parking Control
- 控制对象：智慧停车领域的并联泊车控制器
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个并联泊车控制器，用于先检测附近车位，再根据车辆反向运动学模型和模糊控制器完成倒车入位。
- 判断：算，但属于模型控制级样本。对象是实际泊车控制器，不过显式状态更多体现在检测和倒车两个阶段。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Section 2.1, 行 49-54
> Before the car automatically stopping into the parking spaces, it must be detected around the parking spaces. The image sensor or ultrasonic sensor is installed around car to detect the parking spaces. ... If the parking space is large enough, the parking spaces will be the parking space of smart car.

#### 摘录 B
- 出处：第 2-3 页，Section 2.2.2, 行 117-124
> Car reversing model under the simplified model. Two wheels of car were controlled with two motors and two control chips respectively in the paper, and wheels rotational angle were determined by the Ackerman angle. ... Automatic parallel parking algorithm is based on kinematic model of the car. In building kinematic model of the car, first of all model parameters need to be determined.

#### 摘录 C
- 出处：第 4-8 页，`3.3 The fuzzy Controller Design / 6. Simulation Analysis / 7. Conclusion`，行 210-235, 376-389
> Fuzzy controller has three inputs x, y, and θ in the process of reversing; and a output θ̇ equal to the rotation angle of wheels approximately. This three-dimensional fuzzy controller ... have a total of 18 rules. ... Mamdani control rules were used, and membership functions use Gaussian function.
> ...
> If x is S, and y is S, it means that the car has been reversed into the parking ... when θ is Z ... then reversing the process of the car ends.
> ...
> Figure 15 based on the fuzzy control simulation results show that cars can be safe stop into the parking space.
> ...
> selecting a starting point is also essential to success parking, so that only two part must cooperate to make car into parking spaces safely.

### 2. 基于原文整理后的自然语言描述

The controller first detects candidate parking spaces around the vehicle by using image or ultrasonic sensors and accepts a space only when it is large enough for the smart car. After a feasible space has been identified, the reverse maneuver is generated from a simplified kinematic model in which the two driven wheels are controlled through the Ackerman steering angle relation. The fuzzy parking controller then uses the vehicle coordinates `(x, y)` and direction angle `θ` as inputs and outputs the steering-rate command `θ̇`, with a three-dimensional Mamdani rule base of 18 rules implemented by Gaussian membership functions. Within these rules, states close to the final parking pose can terminate the reversing process, and the simulation study shows that successful parking also depends on choosing a suitable starting point before the fuzzy controller executes the maneuver.

### 3. 逐句溯源

1. 句子 1：The controller first detects candidate parking spaces around the vehicle by using image or ultrasonic sensors and accepts a space only when it is large enough for the smart car.
   对应摘录：A
2. 句子 2：After a feasible space has been identified, the reverse maneuver is generated from a simplified kinematic model in which the two driven wheels are controlled through the Ackerman steering angle relation.
   对应摘录：B
3. 句子 3：The fuzzy parking controller then uses the vehicle coordinates `(x, y)` and direction angle `θ` as inputs and outputs the steering-rate command `θ̇`, with a three-dimensional Mamdani rule base of 18 rules implemented by Gaussian membership functions.
   对应摘录：C
4. 句子 4：Within these rules, states close to the final parking pose can terminate the reversing process, and the simulation study shows that successful parking also depends on choosing a suitable starting point before the fuzzy controller executes the maneuver.
   对应摘录：C
