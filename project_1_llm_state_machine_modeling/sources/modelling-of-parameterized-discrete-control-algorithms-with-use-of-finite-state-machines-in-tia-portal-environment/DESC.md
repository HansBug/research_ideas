# 在 TIA Portal 环境中利用有限状态机建模参数化离散控制算法 / Modelling of Parameterized Discrete Control Algorithms With Use of Finite State Machines in TIA Portal Environment

## 基本信息

- **标题**：Modelling of Parameterized Discrete Control Algorithms With Use of Finite State Machines in TIA Portal Environment
- **中文标题**：在 TIA Portal 环境中利用有限状态机建模参数化离散控制算法
- **作者**：Grzegorz Andrzejewski，Wojciech Zając
- **单位**：The Jacob of Paradies University, Gorzów Wielkopolski, Poland
- **发表**：International Journal of Electronics and Telecommunications, 2018, 64(2): 249-254
- **DOI**：10.24425/119584
- **链接**：https://doi.org/10.24425/119584

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文直接展示了 FSM 图、状态输出表和 LAD 实现步骤，已足够复原 PLC 控制程序的高层逻辑。

### 数据集/案例获取方式

- 原文未提供外部数据集下载链接。
- 十字路口交通灯控制对象、状态相位、定时值和 PLC 实现均在正文中给出，可直接作为单案例来源。

## 简报

这篇论文解决的是**如何用 FSM 在 TIA Portal 中建模并实现带参数化时间变量的离散控制算法**的问题。作者选择了一个双向十字路口交通灯作为控制对象，把它建成七状态 FSM，再在 Siemens PLC 的 LAD 程序中实现。

- **输入**：`Start`、`OE` 以及 `T1-T6` 六个 timing pulse。
- **方法**：Moore 型 `FSM` + 状态输出表 + LAD 定时器链。
- **输出**：七状态交通灯控制器及其在 TIA Portal 上的 PLC 实现。
- **一句话评价**：这是非常干净的 `FSM + T1` 工程样本，状态和定时脉冲都足够明确，适合作为基础离散控制模板。

## 控制系统与状态机证据

### 控制对象

作者选择的是一个十字路口双向交通灯控制器。对象非常典型，但与很多只给流程图的论文不同，这篇把状态图、状态-输出对应关系和 PLC 实现过程同时给出来了。

### 状态机组织方式

控制器共有 `s1-s7` 七个状态，其中：

- `s1-s6` 对应正常灯序循环
- `s7` 对应关闭/复位状态

每个状态都有唯一的灯色组合，例如 `Green A / Red B`、`Yellow A / Red B`、`Red A / Green B` 等，因此属于标准 Moore 型 FSM 结构。

### 时间与参数语义

论文的核心价值在于它不是只说“有状态变化”，而是把时间条件明确写成：

- `T1 = 5 s`
- `T2 = 2 s`
- `T3 = 2 s`
- `T4 = 5 s`
- `T5 = 2 s`
- `T6 = 2 s`

并说明每个下一状态是由前一个状态计时器 `Q` 输出的负边沿触发。因此它天然就是 `T1` 级别的工程定时状态机。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它提供了一个非常标准、规整、低歧义的 PLC 相位控制样本。
- 它的状态、输出和定时条件几乎可以直接转成自然语言-状态机对。
- 它对训练基础离散控制与时间相位控制尤其有用。

### 可直接借鉴之处

- 可以直接借鉴 `state/output table + timer-driven transitions` 的表达方式。
- 可以直接借鉴把 `OE` 作为统一停机/清零守卫的写法。
- 可以直接借鉴用 LAD 程序中负边沿触发器表达状态切换。

### 局限性

- 对象比较基础，系统复杂度有限。
- 论文更偏建模与实现演示，没有太多复杂异常分支。
- 时间语义主要是局部 phase timer，不涉及更高阶任务调度或复杂层次。

## 文献分类总结

- **文献类型**：真实 PLC 控制案例论文
- **控制对象**：十字路口交通灯控制器
- **状态机画像**：`FSM + T1 + 显式时钟`
- **证据强度**：状态、输出、时长和实现过程都清晰，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，用于补齐基础相位控制与定时驱动 PLC 样本
