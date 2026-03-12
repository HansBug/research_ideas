# PLC Controlled Elevator System using XC1 PLC through Ladder Programming - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文清楚描述了 PLC 记录呼叫、同向优先运行、到层减速与反向前延后处理的电梯调度逻辑。

## 条目 1: Intelligent Up-Then-Down Scheduling
- 控制对象：楼宇机电领域的 XC1 PLC 电梯控制系统

### 0. 条目识别与判定
- 一句话说明：这是一个电梯 PLC 调度控制器，用于采集楼层与轿厢按钮请求、判断轿厢位置，并按上行优先或下行优先策略组织停层顺序。
- 判断：算。对象是实际电梯控制系统，原文对呼叫登记、位置检测、减速停层和方向切换策略给出了明确描述。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section on elevator strategy, 行 125-146
> All the buttons in the elevator box and of each floor are wired to the PLC. When any one of these buttons is pressed, the XC1 PLC logs a request. There are different ways to find out the position of the elevator box. Generally, a light or magnetic sensor placed on the side of the box reads a series of holes on a long vertical tape in the shaft. The XC1 PLC knows exactly the position of the elevator box is in the shaft by counting the holes. The PLC can vary the motor speed so that the car slows down gently as it reaches each floor. This ensures a smooth ride for the passengers.
>
> In a multi-storeyed building, the PLC strategy is to keep the elevator box run efficiently. Traditionally, the strategy was to abstain from reversing the elevator's direction. That means, the elevator box will move up till there are people on the floors above that want to go up. It makes sure to only answer "down calls" after it has taken care of all the "up calls" (intelligent mode). But once it starts coming down, it won't pick up anybody who needs to go up until and unless there are no more down calls from the lower floors.

### 2. 基于原文整理后的自然语言描述

The PLC logs requests from both car buttons and floor buttons and determines the elevator position from sensors along the shaft. It slows the car as it approaches each floor, and its dispatching strategy avoids unnecessary reversals by serving all upward requests before responding to downward calls. Once the elevator begins descending, it continues clearing lower-floor down calls before accepting new upward requests.

### 3. 逐句溯源

1. 句子 1：The PLC logs requests from both car buttons and floor buttons and determines the elevator position from sensors along the shaft.
   对应摘录：A
2. 句子 2：It slows the car as it approaches each floor, and its dispatching strategy avoids unnecessary reversals by serving all upward requests before responding to downward calls.
   对应摘录：A
3. 句子 3：Once the elevator begins descending, it continues clearing lower-floor down calls before accepting new upward requests.
   对应摘录：A
