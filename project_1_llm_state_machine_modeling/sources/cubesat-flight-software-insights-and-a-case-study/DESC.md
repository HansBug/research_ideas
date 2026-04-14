# PHI-Demo 脚本引擎与在轨任务排程 / CubeSat Flight Software: Insights and a Case Study

## 论文在讲什么

这篇论文前半部分是 CubeSat flight software 综述，后半部分则给出一个相当具体的 PHI-Demo 12U CubeSat case study。真正对 `sources/` 有价值的并不是综述部分，而是 case study 里那套 app-based flight software：命令行接口、脚本引擎、bootloader，以及围绕它们组织的在轨任务执行方式。

当前最值得抽取的核心对象是脚本引擎。它不是简单的“命令解释器”，而是一个显式状态机驱动的 orbit-operations controller，用来把 LEOP、载荷控制、推进操作和后续多轨任务编成可上传脚本，并在卫星脱离地面接触后仍按预定时序自动执行。这让它成为一个非常典型、而且文本证据很完整的 CubeSat 任务执行监督样本。

## 控制系统在文中的位置

这套控制系统描述在文中属于主案例载体。作者虽然先做了大篇幅文献综述，但后面的 PHI-Demo 案例不是点缀，而是用来证明他们提出的 flight software 框架如何真正落地的核心部分。脚本引擎、bootloader 和 CLI 共同构成了这套 flight software 的关键运行机制。

对我们来说，最关键的是作者把脚本引擎写成了明确的 `Idle / Armed / Running / Finished / Aborted` 状态机，并说明了 LEOP 启动脚本、ground arming、脚本链式执行和延时命令释放的逻辑。这种“带状态图、带运行条件、带连续脚本拼接”的叙述，非常适合转成自然语言状态机数据，而不是停在框架级概述。

## 对我们为什么有用

这篇论文补的是航空航天方向里一种比较少见的样本类型：不是姿态控制律，也不是传统 safe-mode 图，而是“基于脚本和命令行的在轨任务监督器”。它能让数据集覆盖到 CubeSat 里另一类很真实的控制对象，即把一串命令和载荷操作组织成可跨多轨执行的任务控制软件。

此外，这篇论文的 case study 还同时给出 bootloader 的镜像槽位、watchdog 和 crash counter 机制。即便当前 `STM.md` 主条目只聚焦脚本引擎，这些附加内容也说明这篇论文对“在轨执行 + 更新 + 恢复”这类航空航天离散控制语义是有系统覆盖的。后续如果要扩展到 fault recovery 或 in-mission update 子样本，这篇文章也很适合作为回看入口。

## 如果需要人工细读，建议怎么读

如果后续要人工细读，建议直接从第 29-32 页的 case study 深处读起，而不是先顺着综述部分从头读。第 29-30 页先抓脚本引擎的 `armed -> running -> finished/aborted` 主链、LEOP 自动脚本和脚本链式执行；第 31-32 页再看 bootloader 的四槽位镜像组织、watchdog 超时和 crash counter 回退逻辑，用来补足这套 flight software 的恢复侧语义。

第 1-28 页的综述可以放到第二轮再看，它更适合帮助理解 CubeSat FSW 的背景缺口、已有框架和设计争议，而不是直接决定当前这条 `STM` 样本的主链。如果只是为了重做状态机条目，优先保住的仍然是脚本引擎状态图、arming 规则、脚本延时执行、LEOP 启动脚本以及多脚本链式任务调度。
