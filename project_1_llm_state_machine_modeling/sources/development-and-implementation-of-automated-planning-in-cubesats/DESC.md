# MOCI 任务模式调度与执行 / Development and Implementation of Automated Planning in CubeSats

## 论文在讲什么

这篇论文围绕 UGA 小卫星实验室为 MOCI CubeSat 构建的 `MASS` 自动计划系统展开。它表面上是在讲 ground-based automated planning pipeline，但真正有价值的不是泛泛的规划框图，而是作者把 MOCI 任务操作拆成了可直接执行的 mission modes，并明确写出这些模式需要满足哪些电量、通信窗口、目标窗口和任务完成条件。也就是说，这不是单纯的“调度算法论文”，而是一篇把 CubeSat 任务模式和执行规则写进正文的工程 case paper。

从 `sources/` 的角度看，最关键的是第 8-10 页的 MOCI integration 部分。作者先定义了 `Cruise / Power Generation / Scan / Data Processing / Data Downlink / Safe` 六个模式，再给出这套模式在地面 `MASS` 与机载 flight software 之间是如何衔接的：哪些切换来自人工命令、哪些来自排程命令、哪些由任务完成自动触发、哪些会因为异常自动转入 `Safe`。这让它非常接近一个可直接做状态机建模的数据集样本。

## 控制系统在文中的位置

这套控制系统描述在文中属于案例主体，而不是背景说明。论文前半部分虽谈了 MASS 的总体开发与仿真能力，但到了 MOCI integration 章节，作者已经不再只讲“如何排程”，而是在讲卫星到底有哪些运行模式、每种模式什么时候允许进入、什么时候必须退出，以及这些条件怎样落到机载调度器和 timed interrupts 上。

对我们来说，这一点尤其重要，因为它把“地面自动排程”与“机载模式执行”接成了一条完整控制链。换句话说，MASS 不是悬空给出一张推荐时间表，而是生成带参数的 mode sequence；机载软件收到这些配置后，会在定时中断触发时检查进入条件，再正式启动对应任务。这个结构比很多只讲 planner 或 mission concept 的航天论文更适合抽成明确的状态机自然语言描述。

## 对我们为什么有用

这篇论文补的是航天方向里很缺的一类样本：它既不是连续姿轨控本体，也不是抽象 autonomy framework，而是一个围绕 mission mode execution 写得比较实的 CubeSat 调度与执行链。我们能从中稳定抽出模式集合、触发事件、battery/storage guard、ground-station elevation 条件，以及 `50 minutes / 75 minutes / 60 minutes` 这类工程定时约束。

这类样本对 `project_1` 很有意义，因为它把很多后续建模真正需要的元素放在同一条文本主链里了：控制对象明确，状态/模式清晰，进入和退出条件可追溯，还保留了 scheduler queue、timed interrupts、safe-mode fallback 这些真实工程里常见但在论文中并不总能写清楚的控制语义。它也能和仓库里已有的 CubeSat mode-management 条目形成互补，不再只覆盖 `LEOP / safe mode` 这一类经典模式切换样本。

## 如果需要人工细读，建议怎么读

如果后续要人工细读，建议直接从第 8-10 页的 `Introduction to MOCI`、`Introduction to Operational Rules`、`Table 3-7` 和 `MASS to MOCI Pipeline` 开始，而不是从前面的 related work 顺读。第一轮先把 6 个模式、四类切换触发条件，以及 `Scan / Data Processing / Data Downlink` 的进入与退出规则读稳；这一步就足够支撑重写 `STM.md` 的主条目。

之后再回看第 2-7 页关于 phantom satellite、future event prediction、power/data/link budgets 的描述，用来理解这些 mode rules 为什么会形成现在这样的 guard 组合。若只是为了重做状态机样本，优先保住的仍然是模式名、切换触发、`75%` 电量阈值、`50 / 75 / 60 minutes` 时间限制、`20 degrees` 下传门限，以及 timed interrupt 如何把排程真正落到机载任务执行上。
