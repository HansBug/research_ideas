# 主动膝踝假肢可变坡度楼梯上下行相位控制 / Data-Driven Phase-Based Control of a Powered Knee-Ankle Prosthesis for Variable-Incline Stair Ascent and Descent

## 论文在讲什么

这篇 IEEE Transactions on Medical Robotics and Bionics 论文提出一个用于主动膝踝假肢 stair ascent/descent 的 data-driven phase-based HKIC 控制器。它面向不同 step height 和上下楼两类任务，用统一 phase variable 与数据驱动 impedance model 生成更接近 able-bodied 的膝踝运动学、动力学和功。

对文库最关键的是 Section III 中的 `S1-S5` 状态机。`S1-S3` 对应 stance，`S4-S5` 对应 swing；状态机在 `FS`、`MHE`、`TO`、`MHF`、大腿角和大腿速度阈值之间切换，并把状态选择的相位估计送入 stance impedance model 或 swing kinematic controller。

## 控制系统在文中的位置

状态机在文中承担 phase-variable definition manager 的角色，是 HKIC 控制器的高层离散骨架。没有这套 `S1-S5` 状态机，控制器无法决定什么时候用下降大腿角定义、什么时候用上升大腿角定义、什么时候进入 feed-forward swing，也无法在 foot strike 和 toe-off 处平滑切换 stance/swing 输出。

这篇论文同样属于膝踝假肢步态相位簇，因此本轮不把它标为核心新增主样本，而是作为降采样保留。它仍然满足双 A，因为正文和补充图明确给出了状态划分、guard、滤波窗口、低层输出和人体实验验证，足以支持可追溯 `STM.md`。

## 对我们为什么有用

它提供了一个更复杂的“同一假肢控制对象跨上楼/下楼/不同台阶高度”的状态机样本。相比只处理 stair ascent 的论文，它增加了 variable-incline 与 stance impedance model 的任务参数，并把 `S5` feed-forward swing 作为避免 premature saturation 的明确状态。

后续做训练集时，可以把它和 2019/2022 的相位变量控制论文放在同一簇里，用来观察模型是否能识别版本演进：从 forward/backward/non-rhythmic，到 stair ascent，再到 ascent/descent variable-height HKIC。抽样时需要控制数量，避免医疗假肢方向压过停车、铁路、电梯和交通灯等低位领域。

## 如果需要人工细读，建议怎么读

人工复核时，先看摘要明确 HKIC、variable stair height 和 ascent/descent 任务边界，再重点读 Section III 的 `Unified Stair Phase Variable`，逐项抽 `S1-S5`、`FS`、`MHE`、`TO`、`S4 -> S5` guard 与 `S5 -> S1` 回环。随后看 Section IV 的 stance impedance model 和 swing kinematic controller，确认状态输出如何落实成膝踝扭矩或轨迹。

若只是重写 `STM.md`，实验结果、统计图和模型拟合细节可放在第二轮；第一轮最重要的是把状态机、相位定义和低层输出接口读准。需要核对图示时，应回 PDF 看 Fig. S1 及周边文字，因为 `paper_content.txt` 对补充图的版式表达不如正文段落稳定。
