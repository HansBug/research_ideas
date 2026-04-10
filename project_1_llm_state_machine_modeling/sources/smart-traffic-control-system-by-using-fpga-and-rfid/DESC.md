# FPGA 与 RFID 智能交通控制 / Smart Traffic Control System by Using FPGA and RFID

## 论文在讲什么

这篇论文设计了一套四向路口智能交通灯控制系统，核心是用 FPGA Spartan 6 接收 RFID 与 IR 传感器输入，再驱动红、黄、绿 LED 信号灯。系统希望解决传统固定周期交通灯在拥堵和应急车辆通行场景下反应慢的问题。

控制思路分成三层：首先识别 RFID 标签中的应急车辆，并为其所在车道开启 green corridor；如果没有应急车辆，再用 IR 传感器估计各车道密度；如果应急和密度条件都不触发，就回到常规 FSM 交通灯序列。论文还给出红/绿灯 5 秒、黄灯 2 秒的局部延时，因此不是只有“自适应交通灯”口号。

## 控制系统在文中的位置

交通灯控制器是论文的主角。正文的 Proposed System、Flow Chart 和 Finite State Machine 三节直接描述输入、输出和 FSM 行为：RFID 用于识别 ambulance，IR 用于检测车流长度或密度，FPGA 根据程序选择 LED 输出。

从数据集角度看，这篇更适合作为应急车辆交通灯优先簇的降采样样本。它与库内已有 `RFID/RF emergency priority` 条目在控制目标上高度相近，但它同时保留了密度检测、常规序列、四种 FSM 操作状态和明确延时，细节充实度足以保留。

## 对我们为什么有用

它对 `sources/` 的主要价值在于给出一个工程化、文本可追溯的 `RFID priority + density-aware traffic FSM`。后续构造样本时，可以把输入拆成 `RFID_EV_detected`、`IR_density_high`、`all_lanes_equal` 等 guard，再把输出拆成 `green corridor`、`normal sequence`、`blink mode` 和 red/yellow/green delays。

同时它也提醒后续检索要控制趋同。交通灯应急优先方向已经有多个相似样本，因此这篇虽然达到双 A，不应与主代表同权重使用；更适合在需要表达差异或鲁棒性测试时从降采样池抽取。

## 如果需要人工细读，建议怎么读

建议先看第 2 页摘要，确认系统的三类要素：FPGA、IR sensors、RFID。然后跳到第 4 页 Proposed System 和 Flow Chart，把应急车辆优先、密度判断、空车道跳过、常规 FSM 序列四个分支读清楚。

第二轮再读第 5 页 Finite State Machine，重点核对 Moore FSM、四个 controller states、idle/reset 以及红绿灯 5 秒、黄灯 2 秒这些定时值。FPGA/Xilinx 背景和文献综述可以后看；如果要重写 `STM.md`，不要只依据摘要，应优先回到 Flow Chart 与 FSM 章节。
