# MINIATUR 2 LIFT 5 LANTAI MENGGUNAKAN KONTROLLER 2 PLC OMRON CPM1A DENGAN ONE TO ONE PC LINK CONNECTION MENGGUNAKAN KABEL RS232 - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了双梯组控中的主从调度层、单梯执行层和异常恢复行为，任务分配依据、并行关系与测试场景都比较完整，可直接作为楼宇机电方向的双 A `HSM + T0` 样本。

## 条目 1: Duplex-Collective Five-Floor Elevator Dispatcher with Master-Slave PLC Link

- 控制对象：楼宇机电领域的双梯五层主从式组控电梯控制系统
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 `PLC master + PLC slave` 组成的双梯组控系统，主控负责楼层呼叫任务分配，两个单梯控制器并行执行各自的上下行、停靠、过载告警和断电恢复逻辑。
- 判断：算。对象是实际电梯群控子系统，原文不仅说明了两台电梯如何协作，还给出了分层主从结构、任务比较逻辑、位置分组规则、过载告警和掉电后 first cycle 恢复行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`Metode Duplex-Collective / Perangkat Keras`，`paper_content.txt` 第 72-80 行、第 104-124 行
> "duplex-collective"
>
> "PLC master"
>
> "PLC slave"

论文先把系统定义成两台并列电梯的 `duplex-collective` 协同模式，再补充单梯的限位、层站按钮、上/下行按钮、过载开关、LED 指示和蜂鸣器等执行部件。

#### 摘录 B

- 出处：第 3-5 页，`Komunikasi / Program PLC Master`，`paper_content.txt` 第 144-154 行、第 250-279 行、第 333-398 行
> "jumlah tugas"
>
> "push button naik / turun"

主控层通过 `RS232` 接收从梯的位置、方向和任务数，再按楼层相对位置、当前上/下行方向和双方任务数量来决定哪台电梯接管某个厅外呼叫。

#### 摘录 C

- 出处：第 5-6 页，`Kontrol Motor / Program PLC Slave`，`paper_content.txt` 第 402-423 行、第 435-456 行
> "first cycle"
>
> "timer"

单梯执行层负责根据 latch 任务、楼层限位、上下优先级和电机互锁来驱动上行或下行，并使用 stop timer 模拟每层停靠；从梯只是不再承担顶层调度决策。

#### 摘录 D

- 出处：第 6-7 页，`Pengujian Sistem Secara Keseluruhan / Kesimpulan`，`paper_content.txt` 第 541-549 行、第 620-716 行
> "buzzer"
>
> "Supply dimatikan"

系统级测试不仅覆盖多名乘客并发呼叫和任务优先级，还明确覆盖了过载触发蜂鸣器、供电中断后停在层间、重新上电后回到最近下方楼层并要求重新下达任务的恢复流程。

### 2. 基于原文整理后的自然语言描述

The five-floor twin-elevator controller is organized hierarchically: a master PLC plays the role of group dispatcher, while two elevator executors in parallel handle the physical motion of car 1 and car 2. At the dispatch layer, the master receives the slave car's LED-based position and direction state together with its current task count, then compares both elevators by floor grouping, current up/down movement, and `jumlah tugas` before assigning an external hall call to one side. Inside each car controller, accepted hall calls or cabin-floor requests are latched into per-floor tasks, and the motor logic uses floor limit switches, direction priority, and interlocked up/down relays to carry the car until the matching floor switch clears the task; a stop timer is used to emulate the door-stop phase at intermediate floors. The same model also includes non-nominal branches: overload closes the normal transport path and raises a buzzer alarm, while a sudden power loss freezes both cars between floors and a fresh `first cycle` on restart drives each car down to the nearest lower floor before any remaining demand can be served again.

### 3. 逐句溯源

1. 句子 1：The five-floor twin-elevator controller is organized hierarchically: a master PLC plays the role of group dispatcher, while two elevator executors in parallel handle the physical motion of car 1 and car 2.
   对应摘录：A, B, C
2. 句子 2：At the dispatch layer, the master receives the slave car's LED-based position and direction state together with its current task count, then compares both elevators by floor grouping, current up/down movement, and `jumlah tugas` before assigning an external hall call to one side.
   对应摘录：B
3. 句子 3：Inside each car controller, accepted hall calls or cabin-floor requests are latched into per-floor tasks, and the motor logic uses floor limit switches, direction priority, and interlocked up/down relays to carry the car until the matching floor switch clears the task; a stop timer is used to emulate the door-stop phase at intermediate floors.
   对应摘录：A, C
4. 句子 4：The same model also includes non-nominal branches: overload closes the normal transport path and raises a buzzer alarm, while a sudden power loss freezes both cars between floors and a fresh `first cycle` on restart drives each car down to the nearest lower floor before any remaining demand can be served again.
   对应摘录：C, D
