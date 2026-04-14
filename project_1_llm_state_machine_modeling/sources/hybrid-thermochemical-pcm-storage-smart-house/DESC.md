# 智能住宅混合热化学-PCM 储能集成控制 / Integrated Control of Hybrid Thermochemical-PCM Storage for Renewable Heating and Cooling Systems in a Smart House

## 论文在讲什么

这篇论文研究的是一个部署在 `MiniStor smart house` 上的混合热储能系统如何被统一控制。系统里同时存在 `TCM reactor`、`PCM` 储罐、`heat pump`、太阳能回路、阀门、压缩机和若干液位/压力/温度传感器，作者关心的不是单个部件的局部控制，而是整套供热/制冷储能系统在不同工况下该进入什么模式、何时切换、各执行器在每个模式里该怎么配合。

文章把这套逻辑写成了一个分层的 `finite-state machine`。上层 supervisory layer 负责决定 `standby`、`pressurization/pre-heat`、`charging`、`depressurization`、`discharging`、`safety` 等主模式；下层 local control layer 负责在这些模式下驱动泵、阀、压缩机和 `EEV`。文中不仅有模式名，还有 `2.5 bar`、`PR > 5.5`、`PNH3 - PTCM > 0.2 bar`、液位 `90% / 5%`、延时与 hysteresis 这些明确的切换条件。

## 控制系统在文中的位置

控制系统描述是论文的核心内容之一。作者在 `2.3 Control of the Systems (Software)` 中明确说明所有子模块状态信号都会汇入一个总状态机，再由这个状态机决定系统运行模式，并强调它是 hierarchical、rule-based 的 `finite-state machine`。这说明这里的状态机不是辅助示意图，而是整个 smart house 储能系统运行策略的组织骨架。

同时，这篇论文也不是只停留在流程图层面。它把控制逻辑和后面的 commissioning、Grafana 观测、人工/自动/半自动模式都连在了一起，因此能让人看清这套监督器怎样真正支撑 demonstrator 的运行。这种“控制逻辑直接嵌在真实装置软件里”的材料，对 `sources/` 来说比纯 HVAC 策略综述更有保留价值。

## 对我们为什么有用

它对文库最重要的价值，是补了 `🏢` 方向里少见的“建筑能源系统 HSM 样本”，而且不是普通电梯或门控那类经典离散序列，而是带热储能、压力比、液位与天气条件的复杂楼宇能源 supervisor。对于后续做状态机生成和验证数据集，这类样本能把“楼宇机电控制”从传统机电流程扩展到建筑能源管理。

它还提供了一个很好的 `HSM + T1` 例子。文中显式提到 `time delays`、`hysteresis bands` 和 `minimum dwell constraints`，并把这些时间/阈值条件嵌进模式切换，这使它不只是一个泛化的“模式切换说明”，而是很适合抽成带局部工程时序的层次状态机自然语言样本。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `10-13` 页的 `2.3 Control of the Systems (Software)` 以及 Figure `9/10`，先把 `Standby -> Pressurization -> Charging -> Depressurization -> Discharging` 这条主链和 `Safety` 旁支读出来，再按文中阈值把关键 guard 记下来。随后继续看第 `22-23` 页的 `4.2 Pressurization and Charging Phase`，确认这套模式切换在实验和调试阶段是怎样被反复触发与回跳的。

第二轮再去看 HMI、Grafana、REST API 和前端页面部分，这些内容有助于理解系统怎样被监测和人工介入，但并不是先恢复状态机控制链的关键入口。若只想重做 `STM.md`，应优先盯住软件控制章节、充放热 flowchart 和 commissioning 里对模式阈值的解释。
