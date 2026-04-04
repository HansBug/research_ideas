# 基于有人驾驶数据挖掘的无人重型履带车辆远程换挡控制方法 / An Efficient Remote Driving Shift Control Method of Unmanned Heavy Tracked Vehicles Based on Manned Data Mining

## 基本信息

- **标题**：An Efficient Remote Driving Shift Control Method of Unmanned Heavy Tracked Vehicles Based on Manned Data Mining
- **中文标题**：基于有人驾驶数据挖掘的无人重型履带车辆远程换挡控制方法
- **作者**：Weijian Jia，Yao Zhao，Haiwen Zheng，Penglei Hu，Yufei Gao
- **单位**：
  - Zhengzhou Campus, Army Artillery and Air Defense Forces Defense Academy
- **发表**：Scientific Reports，2025
- **DOI**：10.1038/s41598-025-28676-1
- **链接**：https://doi.org/10.1038/s41598-025-28676-1

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文写明车辆控制程序基于 `C++` 与 `QT`，核心处理器为 `STM32F103`，但未公开源码。
- 原文给出了上层/下层 HFSM、各换挡子状态、故障子状态、时间阈值与回原挡策略，足以作为 source paper 直接使用。

### 数据集/案例获取方式

- 原文未提供独立数据集下载，但说明使用了 `2160` 段有人驾驶换挡过程片段训练 shift timing decision model。
- 论文给出了 bench test 与实车测试中的完整换挡监督控制链，可直接作为单案例控制系统论文收纳。

## 简报

这篇论文解决的是**无人化改造后的重型履带车辆在远程驾驶时如何平顺、可靠地完成换挡并在失败时自动回退或停车**的问题。输入是远程换挡命令、发动机转速、油门开度、离合器位移、当前挡位、目标挡位和各子状态执行时长，方法是用一个带上层异常处理与下层换挡流程的层次有限状态机来调度 shift timing decision、离合器、空挡和挂挡执行，输出是 `S41 -> S42 -> S43 -> S44 -> S45 -> S46` 主链以及 `S61/S62/S63` 异常处理链。

- **输入**：`flagc_g`、`flagd_g`、`gear_cur`、`gear_exp`、`x_clh`、`n_e`、`β_t`、`t_s`、`tth_g`、`tth_s`。
- **方法**：SVM shift timing decision + HFSM-based integrated power-transmission shift control。
- **输出**：正常换挡六子状态、第一次挂挡失败回原挡、异常时分离离合/入空挡/制动停车的完整监督控制流程。
- **一句话评价**：这是高质量的 `HSM + T1` 工程车辆控制样本，层次结构、状态表和故障回退链都非常完整。

## 控制系统与状态机证据

### 控制对象

论文对象是无人重型履带车辆的远程驾驶换挡监督控制器。它负责在接收到远程换挡指令后，判断时机、调节发动机转速、执行离合器分离与结合、完成入空挡和挂目标挡，并在超时或同步器顶齿时触发回退和异常处理。

### 状态机组织方式

原文把该控制器明确写成 `hierarchical finite state machine`。上层包含：

1. `S4` 远程驾驶动力传动一体化换挡控制状态
2. `S6` 换挡异常处理状态

其中 `S4` 下又分为六个换挡子状态：

1. `S41` on-gear control
2. `S42` shift timing auxiliary decision
3. `S43` clutch separation
4. `S44` off-gear control / neutral
5. `S45` gear shift
6. `S46` clutch engagement

`S6` 下再分为：

1. `S61` clutch separation in fault
2. `S62` neutral gear in fault
3. `S63` braking stop

### 关键控制链

论文把正常链和故障链都写得很明确：

- 收到远程换挡命令后，从 `S41` 进入 `S42`，由 shift timing decision model 根据 `n_e` 与 `β_t` 判断何时允许换挡。
- 满足时机后转入 `S43` 分离离合器，`x_clh >= 48 mm` 后进入 `S44` 脱挡到空挡。
- `gear_cur = 0` 后进入 `S45` 挂目标挡；若 `ts < 4 s` 且 `gear_cur = gear_exp`，则进入 `S46` 结合离合器并返回 `S41`。
- 若 `S45` 中 `ts >= tth_g` 或各子状态 `ts >= tth_s`，系统按 `S45 -> S44` 回原挡或进入 `S61/S62/S63` 异常处理链，最终执行制动停车或熄火。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实无人车辆动力传动监督控制器**，不是宽泛的无人驾驶行为决策论文。
- 原文同时保留了上层/下层状态结构、变量、阈值、进入/退出动作和 fault handling 逻辑，特别适合提取高质量自然语言状态机样本。
- 对“工业/军用车辆执行器控制 + 超时异常回退链”这一类复杂控制样本非常有价值。

### 可直接借鉴之处

- 可以直接借鉴上层 `remote driving` 与 `exception handling` 的层次分解方式。
- 可以直接借鉴 `shift timing decision -> clutch separation -> neutral -> gear shift -> clutch engagement` 的换挡模板。
- 可以直接借鉴以 `ts`, `tth_g`, `tth_s` 为核心的超时回退与故障处理写法。

### 局限性

- 论文前半部分有较多 SVM 辅助决策内容，需要与 HFSM 主控制链区分阅读。
- 车辆底层动力学与液压机构细节较多，整理时需聚焦监督控制主链。
- 状态命名以工程代号为主，转写时需要补足中文语义说明。

## 文献分类总结

- **文献类型**：真实无人车辆换挡监督控制案例论文
- **控制对象**：无人重型履带车辆的远程换挡与异常处理监督控制器
- **状态机画像**：`HSM + T1`
- **证据强度**：上层/下层状态图、状态转移规则、时间阈值和 fault handling 都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充复杂执行器控制、超时回退和层次状态机样本
