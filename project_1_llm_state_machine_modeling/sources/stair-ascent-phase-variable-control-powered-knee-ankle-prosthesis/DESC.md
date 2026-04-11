# 主动膝踝假肢楼梯上行相位变量控制 / Stair Ascent Phase-Variable Control of a Powered Knee-Ankle Prosthesis

## 论文在讲什么

这篇 ICRA 论文把已有的 phase-variable walking control 扩展到主动膝踝假肢的 step-over stair ascent。核心问题是：楼梯上行时 maximum hip flexion 不再和 heel strike 接近，如果仍按平地步行的 gait-cycle 定义，会让相位变量饱和，进而影响膝踝轨迹同步。

作者的解决方案是把 gait cycle 改为从 `MHF` 开始和结束，并配套修改控制相位 FSM。该 FSM 使用 `S1-S4` 四个状态在 descending 和 ascending thigh-angle phase definitions 之间切换，再用 Fourier-series virtual constraints 生成 knee/ankle desired angles，最后由低层位置控制器驱动关节执行。

## 控制系统在文中的位置

文中的状态机是相位估计和关节控制的关键骨架，而不是仅用于插图说明。`S1-S4` 决定当前 phase variable 的定义，`FC`、push-off onset、`MHE`、`MHF` 等事件决定转移，状态输出间接决定假肢膝踝关节的目标轨迹。

它与文库里既有 powered knee-ankle prosthesis 样本高度相关，因此本轮标成降采样保留更合适。即便如此，它的原文细节足够支撑双 A：状态定义、转移条件、相位公式、virtual constraints、实验验证都能在正文或图题中追溯。

## 对我们为什么有用

它补充的是“楼梯上行专用 phase-variable supervisor”这一更窄的医疗设备控制样本。相较于普通 stance/swing 或多相 impedance FSM，它强调由于任务运动学不同而重新定义 gait cycle，并把这个定义变化落实为状态机转移规则。

后续做数据集时，建议把它放入膝踝假肢步态相位簇，用于训练模型识别同一硬件对象在不同任务中的状态机变体。抽样时不应无限重复这类假肢样本，但保留一两个清楚例子对比 level walking、stair ascent、stair descent 仍然有价值。

## 如果需要人工细读，建议怎么读

人工复核时，先看摘要和 Introduction 理解为什么 stair ascent 需要重新定义 phase variable，再重点读 Section II-A 和 Fig. 3，抽出 `S1-S4`、`FC`、`MHF`、push-off onset、`MHE` 与相位不能下降的规则。然后读 Section II-B/II-C 确认状态输出怎样进入 virtual constraints 和低层位置控制。

如果只是校正 `STM.md`，实验结果可以放在第二轮，只需用它确认控制器确实在 powered knee-ankle prosthesis 或 bypass adapter 上验证过。数学细节里最重要的是 phase definition 与 state transition 的关系，不必把每个 Fourier coefficient 写进样本。
