# Formal specification and analysis of take-off procedure using VDM-SL - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互、资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出地面控制、塔台控制和起飞队列流转，还写清了 priority、clear-state 资源分配和双控制器共享/移交流程，可直接整理为机场地面起飞流程样本。

## 条目 1: Queue-governed airport take-off flow
- 控制对象：机场地面空管中的起飞流程控制
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥、协议交互
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空交通控制领域的 airport surface take-off control procedure，用于在 ground controller 与 local controller 的协同下，把飞机从滑行道权限阶段推进到跑道与起飞阶段。
- 判断：算。对象是实际机场起飞流程控制，原文给出了 controller 分工、队列流转顺序以及“进入队列后必须最终离开”的推进约束。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Methods / Table 1，`paper_content.txt` 第 210-217, 231-240 行
> The airport surface is divided into blocks which are nodes of the graph relation. ... The objective is to find and assign optimal routes with minimum delays meeting the real safety standards by defining a set of queues and sequence of operations. Once an aircraft is inserted into a queue, it should eventually be removed from the queue after the next queue becomes available. In other words, the formal system does not allow any situation where an aircraft is inserted into a queue, and never removed from that queue.
>
> 1 Taxiway permission taxiwayPermission –
> 2 Taxiway assigned taxiwaysAssigned taxiwayPermission
> 3 Taxiing Taxiing taxiwaysAssigned
> 4 Runway permission runwayPermission Taxiing
> 5 Runway assign runwaysAssigned runwayPermission
> 6 On runway Onrunway runwaysAssigned
> 7 Take-off – Onrunway

#### 摘录 B
- 出处：第 11-18 页，Ground/Local controller 和动态操作，`paper_content.txt` 第 330-365, 377-450 行
> The ground controller consists of aircrafts, taxiways, taxiwayPermission, taxiwaysAssigned and taxiing. ... The total number of aircrafts in the permission queue should not be greater than the permissible limit ... The intersection of elements of queue having permission and which are assigned taxiways is empty ... The intersection of taxiing aircrafts and aircrafts which are assigned taxiways is empty.
>
> The local controller consists of aircrafts, runways, taxiing, runwayPermission, runwaysAssigned and onrunway. ... The runwayPermission is used to represent aircrafts in the queue which have permission for take-off. ... The set of aircrafts which are on runways is subset of the aircrafts assigned the runways. ... The intersection of aircrafts on runways and aircrafts having permission is empty.
>
> For every queue, it is checked if the size of next queue is less than its maximum bound and previous queue is not empty then the first aircraft in the previous is moved to the next queue. In this way, starvation is avoided and efficiency is achieved.
>
> Post-conditions ... If priority of the aircraft is high, an optimal taxiway with clear state is assigned. If priority is low, a suboptimal taxiway with clear state is assigned. ... If aircraft priority is high ... an optimal runway is assigned. If priority is low ... a suboptimal runway is assigned.

#### 摘录 C
- 出处：第 15-17 页，Ground/local operations，`paper_content.txt` 第 398-440 行
> Pre-conditions ... An aircraft is provided the permission if size of the queue having permission is less than the maximum permissible limit. Post-conditions List of aircrafts having permission for taxiing is updated by sequence concatenation operator by adding the aircraft aid at the end of list.
>
> After having permission, taxiway is assigned to the aircraft. The ground controller checks various conditions such as priority, availability of taxiway, size of current queue and then assigns the taxiway to the aircraft using the TaxiwayAssign operation.
>
> An aircraft sends a request to the ground controller for taxiing. If state of the assigned taxiway is clear then the aircraft is allowed for taxiing. ... The aircraft is added in the list of aircrafts under local controller. This is because taxiing aircraft must be in the record of both the ground and local controllers.
>
> The runwayPermission is used to represent aircrafts in the queue which have permission for take-off. ... The aircraft is removed from the taxiing aircrafts under both the ground and local controllers. ... Runway assigning procedure is described below. It is noted that after leaving taxiway, the aircraft is only under the local controller.

### 2. 基于原文整理后的自然语言描述

The airport surface is modeled as graph blocks and edges, and taxiways or runways are treated as priority-sensitive resources with clear or occupied states. Ground control owns the queues `taxiwayPermission`, `taxiwaysAssigned`, and `taxiing`, while local control owns `runwayPermission`, `runwaysAssigned`, and `onrunway`; taxiing aircraft are recorded by both controllers until runway permission is granted, after which the aircraft stays only under local control. The take-off procedure advances each aircraft through the seven-stage flow of taxiway permission, taxiway assignment, taxiing, runway permission, runway assignment, on-runway, and take-off, always moving the first aircraft from the previous queue when the next queue has space so starvation is avoided. Taxiway and runway assignment check aircraft identity, queue bounds, resource availability, and clear-state conditions, assigning optimal resources to high-priority aircraft and suboptimal ones to low-priority aircraft.

### 3. 逐句溯源

1. 句子 1：The airport surface is modeled as graph blocks and edges, and taxiways or runways are treated as priority-sensitive resources with clear or occupied states.
   对应摘录：A, B
2. 句子 2：Ground control owns the queues `taxiwayPermission`, `taxiwaysAssigned`, and `taxiing`, while local control owns `runwayPermission`, `runwaysAssigned`, and `onrunway`; taxiing aircraft are recorded by both controllers until runway permission is granted, after which the aircraft stays only under local control.
   对应摘录：B, C
3. 句子 3：The take-off procedure advances each aircraft through the seven-stage flow of taxiway permission, taxiway assignment, taxiing, runway permission, runway assignment, on-runway, and take-off, always moving the first aircraft from the previous queue when the next queue has space so starvation is avoided.
   对应摘录：A, B
4. 句子 4：Taxiway and runway assignment check aircraft identity, queue bounds, resource availability, and clear-state conditions, assigning optimal resources to high-priority aircraft and suboptimal ones to low-priority aircraft.
   对应摘录：B, C
