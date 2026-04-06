# 船道桥体升降与道路交通联动控制 / Simulator Berbasis PLC untuk Pengaturan Lalu-lintas Jalan Raya pada Perlintasan Jalur Kapal

## 论文在讲什么

这篇论文研究的是一个基于 PLC 的船道桥梁通行控制原型。作者搭建了带液压桥体、道路栏杆、交通灯、photo sensor、proximity sensor 和 limit switch 的 miniature simulator，用 Mitsubishi PLC 和 ladder program 让桥体升降与道路放行、封路逻辑联动起来，从而模拟“船只经过时抬桥、车辆等待、船通过后落桥”的完整交通过程。

它不是那种只展示硬件接线的原型论文。文中既写了物理组成，也写了 auto/manual 两种运行方式、sensor #1 / #2 的触发顺序、栏杆下放前的 clear-area 检查、bridge up/down 的限位条件、单船与多船通行差异，以及多组秒级时序和 `26` 秒升降时差。控制链条比较完整，是真正可以抽成状态机文本的交通设施控制器。

## 控制系统在文中的位置

控制系统是论文主线。作者从摘要开始就强调 ladder syntax、input ports、output ports 和同步性能测量，正文后半段更直接按照“manual / auto 模式”“sensor 读取”“jembatan up/down”“traffic light 与 palang pintu 联动”来说明系统怎么运行。也就是说，论文不是把桥梁控制当作随手案例，而是把这套 crossing controller 当成研究目标本身。

对我们来说，最有价值的是它同时保留了**桥体机械链**和**道路信号链**。不少 railway/traffic 论文只写门杆或灯色切换，但这篇把桥体升降、液压动作、栏杆保护、道路灯色恢复和多船检测一并保住了，因此比单纯的 gate controller 更接近复杂一点的联动控制系统。

## 对我们为什么有用

这篇论文对 `🚦` 方向的补样意义很直接。当前交通信号类样本里，很多都集中在普通路口相位控制或应急车辆优先，而这篇提供的是“道路交通 + 通航桥体”的复合控制对象，结构上更像一种跨介质放行/封锁协调器，能明显拉开与常规 traffic light controller 的差异。

同时，它还是一个不错的 `EFSM + T1` 工程样本。文中不仅有灯色和栏杆动作，还有 selector switch、manual/auto 分支、photo sensor #1/#2、proximity clear-area 检查、上/下限位和多船计数条件，后续无论是做自然语言建模还是验证场景抽取，都会比只剩“红黄绿轮转”的薄稿更有用。

## 如果需要人工细读，建议怎么读

人工回读时，建议先抓第 `1-3` 页的系统边界：桥体、液压、栏杆、交通灯、sensor 布局和 ladder control 是什么关系。然后直接跳到第 `8` 页附近的运行说明，看 `manual / auto` 模式、photo sensor #1/#2、proximity sensor、limit switch、yellow 5-second phase 和 multi-ship condition 如何串起来，这里最接近最终控制链。

如果还需要补更多实现证据，再回头看中间几页的部件安装和 wiring 图，把 sensor 与 actuator 的物理对应关系补齐。至于前面大量 PLC 一般介绍和相关原型综述，可以放在最后，因为它们对重建主状态链帮助不如运行段直接。
