# 独立光伏混合储能功率调度状态机 / Power dispatching techniques as a finite state machine for a standalone photovoltaic system with a hybrid energy storage

## 论文在讲什么

这篇论文研究的是独立光伏系统中电池和超级电容混合储能单元如何分担负载，并通过状态机方式管理可用性、负载分配和底层 PWM 控制。作者的重点不是单纯做控制器参数整定，而是把功率调度明确拆成 `WMC`、`PFC` 和 `SWC` 等层次，让不同层分别负责模式选择、功率份额计算和开关控制。

论文的技术主体带有不少连续控制和功率电子公式，但对 `sources/` 来说真正有价值的是第 `6-9` 页对层次状态机的写法。它把 `Hybrid / Battery only / Disconnected` 三个工作模式以及 `Fully dispatchable / Limited / Disconnected` 等子状态直接和 `SOC`、负载需求、功率上限联系起来。

## 控制系统在文中的位置

这里的控制系统描述是文章的中心结构，而不是实验配角。作者明确说 power management strategy 是“hierarchical architecture as an event driven finite state machine”，而且后续章节就是按层来解释这台控制器如何选择能源、如何在超限时降级、以及如何把离散决策传给 DC-DC 和 DC-AC 变换器。

与很多只给几个 mode 名称的能量管理论文不同，这篇在 `WMC` 和 `PFC` 两层都给了状态与转移逻辑，因此更像一个真正可抽取的 supervisor。即便底层仍有 PID 和滤波计算，上层离散部分的边界也相当清楚。

## 对我们为什么有用

这篇论文补的是 `🌡️` 方向里相对稀缺、而且结构很鲜明的 `HSM + T0` 能量管理样本。库里已经有一些微电网和混合能源系统条目，但不少论文只写 mode 名称和阈值，离状态机自然语言描述还差一步。这篇则把模式层和子状态层都讲清楚了。

它的另一个价值是“层次状态机与连续变量强耦合”这个画像很突出。对后续建模研究来说，这类样本可以帮助区分纯离散工程顺序控制和依赖 `SOC / Pmax / load demand` 这类连续量触发的 supervisor 写法。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `6-9` 页，也就是 `2.4 Control system overview`、`3.1 WMC` 和 `3.2 PFC`。先把顶层 `Hybrid / Battery only / Disconnected`、二层 `Fully dispatchable / Limited / Connected / Disconnected` 读出来，再看这些状态分别依赖哪些 `SOC`、负载和功率上限条件切换。这样最容易重建状态机骨架。

随后再回看第 `1` 页摘要和第 `3-5` 页系统拓扑，确认电池、超级电容、DC bus 和逆变器各自在控制链里处于什么位置。大量电池/超级电容模型方程和 PWM 细节可以放到最后看，因为它们主要解释连续行为，不是先还原层次监督器所必需的部分。
