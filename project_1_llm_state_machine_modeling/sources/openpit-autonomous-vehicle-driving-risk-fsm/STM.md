# Driving risk assessment and prevention strategies for autonomous vehicle in open-pits - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把露天矿区无人驾驶矿卡的碰撞风险防控写成七态有限状态机，并把风险等级、速度阈值、状态持续时间与制动踏板开度控制都落到了正文里，足以形成强细节的 `EFSM + T1` 样本。

## 条目 1: Open-Pit Collision-Risk Braking Decision FSM

- 控制对象：通用控制与矿区无人运输领域的露天矿区无人驾驶矿卡风险等级、制动与退出监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是露天矿区无人驾驶矿卡在遇到前方障碍物时，根据风险等级、相对距离、预碰撞时间和车辆速度切换制动策略并最终把控制权交回无人驾驶系统的监督控制器。
- 判断：算。对象是实际矿卡的风险防控决策系统，不是单纯风险评估算法；原文明确给出状态集合、guard、优先级、状态内制动动作和 `0.5 s / 1 s / 2 s` 级局部定时。

### 1. 原文摘录

#### 摘录 A

- 出处：第 8-9 页，`4.1 考虑行车风险等级的安全防控决策`，`paper_content.txt` 第 639-689 行
> “正常行驶状态”
>
> “RiskLevelA”
>
> “QuitStateTwo”

#### 摘录 B

- 出处：第 8-9 页，图 14 状态转移标注，`paper_content.txt` 第 656-679 行
> “障碍物持续消失 1 s”
>
> “持续时间 > 2 s”

#### 摘录 C

- 出处：第 9 页，`4.2 紧急制动控制策略`，`paper_content.txt` 第 744-777 行
> “t0+0.5”
>
> “1 s内”

### 2. 基于原文整理后的自然语言描述

The open-pit driving-security model uses a seven-state decision machine with `Normal Driving`, `RiskLevelA`, `RiskLevelB`, `StopToEnd`, `QuitStateOne`, `QuitStateTwo`, and `Parking` to supervise obstacle-response braking. The transitions depend on explicit continuous variables such as the minimum braking distance ratio `dr <= 1.2 ds`, the pre-collision-time thresholds `Tr <= Tth` and `Tr <= 0.5 Tth`, and low-speed guards such as `vh < 5 km/h` and `vh < 0.3 km/h`, so the machine is not only a plain mode list but an extended guard-driven controller. Once the controller enters `RiskLevelB`, it computes a progressive brake opening from the remaining distance; `RiskLevelA` immediately commands full braking; and `StopToEnd` ramps the brake command to full within `0.5 s` to avoid oscillatory stop-go behavior at low speed. After the obstacle disappears, the supervisor does not hand control back immediately: `QuitStateOne` holds full braking while checking complete stop, whereas `QuitStateTwo` releases the brake to zero within `1 s` and only exits after the state has been active for more than `2 s`. This gives the paper a full decision chain from risk detection to braking, parking, and authority hand-back.

### 3. 逐句溯源

1. 句子 1：The open-pit driving-security model uses a seven-state decision machine with `Normal Driving`, `RiskLevelA`, `RiskLevelB`, `StopToEnd`, `QuitStateOne`, `QuitStateTwo`, and `Parking` to supervise obstacle-response braking.
   对应摘录：A；`paper_content.txt` 第 639-646, 656-679 行。
2. 句子 2：The transitions depend on explicit continuous variables such as the minimum braking distance ratio `dr <= 1.2 ds`, the pre-collision-time thresholds `Tr <= Tth` and `Tr <= 0.5 Tth`, and low-speed guards such as `vh < 5 km/h` and `vh < 0.3 km/h`, so the machine is not only a plain mode list but an extended guard-driven controller.
   对应摘录：A, B；`paper_content.txt` 第 668-677, 683-689 行。
3. 句子 3：Once the controller enters `RiskLevelB`, it computes a progressive brake opening from the remaining distance; `RiskLevelA` immediately commands full braking; and `StopToEnd` ramps the brake command to full within `0.5 s` to avoid oscillatory stop-go behavior at low speed.
   对应摘录：C；`paper_content.txt` 第 694-759 行。
4. 句子 4：After the obstacle disappears, the supervisor does not hand control back immediately: `QuitStateOne` holds full braking while checking complete stop, whereas `QuitStateTwo` releases the brake to zero within `1 s` and only exits after the state has been active for more than `2 s`.
   对应摘录：B, C；`paper_content.txt` 第 675-677, 764-777 行。
5. 句子 5：This gives the paper a full decision chain from risk detection to braking, parking, and authority hand-back.
   对应摘录：A, B, C；`paper_content.txt` 第 639-689, 744-777 行。
