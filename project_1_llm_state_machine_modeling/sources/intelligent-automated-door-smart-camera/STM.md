# An Intelligent Automated Door Control System Based on a Smart Camera - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把智能门禁系统明确写成“开门/关门”两态门控逻辑，并给出了 `Paccess > thPT`、红外防夹闭门条件以及 `2 s / 3 s` 响应与误拒率分析，足以形成双 A 的门控 EFSM 样本。

## 备注

- 当前目录中的 `paper.pdf` 使用 PMC 可打印页面导出的 PDF 版本；相比直接 `pdf` 下载链，这一版本的图文和 `paper_content.txt` 提取质量更稳定，适合做状态机证据回溯。

## 条目 1: Smart-camera door intention and safety loop

- 控制对象：楼宇机电与门控领域的基于智能相机的人体意图识别自动门门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向自动门的门控控制器，用相机检测人体与轨迹意图来决定何时开门，再用红外扫描确认通道清空后闭门。
- 判断：算。对象是实际自动门控制系统而不是纯视觉算法模块，原文明确给出了门的开闭状态、由 `Paccess` 与阈值 `thPT` 驱动的开门条件、由红外安全检测驱动的闭门条件，以及 `2 s / 3 s` 级别的响应性能。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，`2.1. State Transition`，行 74-80
> The state diagram of the proposed accessing control system, which includes opening and closing actions, is depicted in Figure 2. The door open process identifies the detect targets as human by face/contour detection, and calculate the door access intention probability, called Paccess, by analyzing the corresponding trajectory. Once the Paccess is greater than a threshold thPT, the door is opened accordingly. On the other hand, an infrared sensor is added to make sure that nobody is passing or stayed before door closing, and then activate close action when the entrance/exit is clear for safety.

#### 摘录 B

- 出处：第 10-11 页，`2.3. Accessing Intention Estimation`，行 205-218
> access the door Paccess using Equation (4): Paccess=1/T * sum P(xci, yci). If the face stays long enough during the time interval T, the value of Paccess will be high. An average value μPT of the joint pdf is adopted as the threshold μPT ... Therefore, μPT is used, in this paper, as the threshold thPT to determine whether one has intention to go through the entrance or not. That is, if Paccess is greater than μPT, the “opening” command is activated.

#### 摘录 C

- 出处：第 12-13 页，`2.4. System Performance Evaluation` 与 `3. Experiment Results and Discussion`，行 245-260
> where P(thPT) denotes the ratio of area whose value is greater than thPT over the total area of PT ... The theoretical estimation show that if T = 2 s, FRR will be close to 2.4 × 10−5, but if T = 3 s, FRR will be 3.9 × 10−8 and lower. ... The infrared signal scanning in ROI is indicated by the red area, as shown in Figure 5(d).

#### 摘录 D

- 出处：第 19-20 页，`3. Experiment Results and Discussion`，行 347-356
> Total 253 1 99.6% ... The collected data, in 253 trials at five different locations, shows that the correct opening rate within the default 2 s is 0.996 (252/253) while the incorrect action number is only 1. It is noted that although the FAR (0.004) is slightly higher than the theoretically predicted number, for the only one failure case, however, the door is still opened but just delayed for a short time (the response time is 4 s).

### 2. 基于原文整理后的自然语言描述

The proposed automatic-door controller is an intention-gated two-state door loop in which the opening transition is enabled only after the system identifies a human target and computes a trajectory-based access probability `Paccess`. The key guard of the opening action is `Paccess > thPT`, where the threshold is concretely instantiated as the average value `μPT` of the learned probability field over the passage region. Closing is guarded by a different safety condition: an infrared sensor must confirm that nobody is still passing or staying in the entrance or exit area before the close action is activated. The paper also keeps the controller at engineering detail level by quantifying the decision horizon and quality, showing how `T = 2 s` versus `T = 3 s` changes the false rejection rate and reporting `253` field trials with a `99.6%` correct opening rate and one delayed-but-correct recovery case.

### 3. 逐句溯源

1. 句子 1：The proposed automatic-door controller is an intention-gated two-state door loop in which the opening transition is enabled only after the system identifies a human target and computes a trajectory-based access probability `Paccess`.
   对应摘录：A
2. 句子 2：The key guard of the opening action is `Paccess > thPT`, where the threshold is concretely instantiated as the average value `μPT` of the learned probability field over the passage region.
   对应摘录：A, B
3. 句子 3：Closing is guarded by a different safety condition: an infrared sensor must confirm that nobody is still passing or staying in the entrance or exit area before the close action is activated.
   对应摘录：A, C
4. 句子 4：The paper also keeps the controller at engineering detail level by quantifying the decision horizon and quality, showing how `T = 2 s` versus `T = 3 s` changes the false rejection rate and reporting `253` field trials with a `99.6%` correct opening rate and one delayed-but-correct recovery case.
   对应摘录：C, D
