# Formal specification and analysis of take-off procedure using VDM-SL - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文对地面控制、塔台控制和起飞队列流转给出了较清楚的阶段化描述，可直接整理为机场地面起飞流程样本。

## 条目 1: Queue-governed airport take-off flow
- 控制对象：机场地面空管中的起飞流程控制

### 0. 条目识别与判定

- 一句话说明：这是航空交通控制领域的 airport surface take-off control procedure，用于在 ground controller 与 local controller 的协同下，把飞机从滑行道权限阶段推进到跑道与起飞阶段。
- 判断：算。对象是实际机场起飞流程控制，原文给出了 controller 分工、队列流转顺序以及“进入队列后必须最终离开”的推进约束。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5-6 页，Methods，对 ground/local control 与队列推进约束的说明，行 199-217
> It is supposed that ground control monitors aircrafts moving from gate to taxiway. The local control is responsible for taxiing to runway and take-off. After reaching the runway, aircraft is put into the queue and then takes-off after the final permission.
>
> The objective is to find and assign optimal routes with minimum delays meeting the real safety standards by defining a set of queues and sequence of operations. Once an aircraft is inserted into a queue, it should eventually be removed from the queue after the next queue becomes available. In other words, the formal system does not allow any situation where an aircraft is inserted into a queue, and never removed from that queue.

#### 摘录 B
- 出处：第 6 页，Table 1 Aircrafts Queues Management，行 231-240
> 1 Taxiway permission taxiwayPermission –
> 2 Taxiway assigned taxiwaysAssigned taxiwayPermission
> 3 Taxiing Taxiing taxiwaysAssigned
> 4 Runway permission runwayPermission Taxiing
> 5 Runway assign runwaysAssigned runwayPermission
> 6 On runway Onrunway runwaysAssigned
> 7 Take-off – Onrunway

#### 摘录 C
- 出处：第 11-12 页，Ground control / local controller definitions，行 328-351
> Ground control is used for monitoring and guiding aircrafts moving from gate to enter taxiway. The ground controller consists of aircrafts, taxiways, taxiwayPermission, taxiwaysAssigned and taxiing.
>
> The local controller consists of aircrafts, runways, taxiing, runwayPermission, runwaysAssigned and onrunway. The runwayPermission is used to represent aircrafts in the queue which have permission for take-off. The runwaysAssigned is a mapping from aircraft identifier to runway identifier to represent aircrafts which are assigned the runways. The onrunway is a mapping from aircraft on the runways.

### 2. 基于原文整理后的自然语言描述

Ground control monitors aircraft moving from the gate to the taxiway, while local control is responsible for taxiing to the runway and for take-off. After an aircraft reaches the runway, it is placed into a take-off queue and departs only after the final permission is granted. The procedure advances aircraft through the staged flow of taxiway permission, taxiway assignment, taxiing, runway permission, runway assignment, on-runway, and take-off, and the model requires that any aircraft inserted into a queue must eventually be removed once the next queue becomes available.

### 3. 逐句溯源

1. 句子 1：Ground control monitors aircraft moving from the gate to the taxiway, while local control is responsible for taxiing to the runway and for take-off.
   对应摘录：A, C
2. 句子 2：After an aircraft reaches the runway, it is placed into a take-off queue and departs only after the final permission is granted.
   对应摘录：A, C
3. 句子 3：The procedure advances aircraft through the staged flow of taxiway permission, taxiway assignment, taxiing, runway permission, runway assignment, on-runway, and take-off, and the model requires that any aircraft inserted into a queue must eventually be removed once the next queue becomes available.
   对应摘录：A, B
