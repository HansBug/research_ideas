# Time-Complemented Event-Driven Architecture for Distributed Automation Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：Sorter1 的控制流非常适合作为分布式自动化状态/转移样本。

## 条目 1: Sorter1 control flow in a TCED sorting machine
- 控制对象：分布式分拣机系统中的 Sorter1 控制模块
- 整理后的英文描述：The sorting machine control is organized as hierarchical modules. After an item is scanned, the main controller analyzes the scan result and dispatches a time-stamped module command to the target sorter. In Sorter1, the local EDPM receives the command, updates the action schedule, and then the diverter and labeler modules actuate their extend/retract and labeling actions at synchronized times.
- 要素 1：控制流起点是 item scanned，对应 Petri net transition `T1`。
- 要素 2：主控制器分析扫描结果后，把命令下发给目标 sorter。
- 要素 3：Sorter1 的 EDPM 更新 action schedule，然后 TDCM 依据时钟触发 agent。
- 要素 4：extend/retract agents 的 actuations 与物体运动同步。
- 要素 5：这是一个明确的“状态/转移/动作”控制流，只是形式化符号采用 Petri net/TCED module。
- 定位 1：`paper_content.txt` 第 3-4 页，Section IV.A，sorting machine overall concept 与 Thread A/B，行 216-225。
- 定位 2：`paper_content.txt` 第 5 页，Section IV.B / Figure 6-7，行 337-381。
- 证据 1：`The control flow is initiated after an item is scanned (T1)`
- 证据 2：`the item is assigned to Sorter1 (T3)`
- 证据 3：`the sorter TDCM decides when to actuate the extend and retract agents`
- 证据 4：`actuations ... are synchronized to the item’s movement`
