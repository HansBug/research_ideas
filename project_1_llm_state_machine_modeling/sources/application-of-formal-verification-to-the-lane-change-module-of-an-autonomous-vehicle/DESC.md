# 七位置换道横向状态管理器 / Application of Formal Verification to the Lane Change Module of an Autonomous Vehicle

## 论文在讲什么

这篇论文围绕自动驾驶换道模块的形式化验证展开，当前 `STM.md` 抽到的核心对象是“自动驾驶车辆换道模块的横向状态管理器”。如果只抓一句话理解它的主体，可以先把它看成：这是汽车与道路车辆控制领域里一个真正落到代码实现的换道主状态机，负责在高频 planner 更新下记住“当前换道走到哪一步了”。

从现有条目看，文中的离散控制链主要以 `EFSM（扩展状态机）` 的方式出现，时间语义属于 `T1（工程定时 / 局部定时）`。它最有价值的地方不在于“有一个 lane change 状态图”，而在于把 `updateState / duringUpdate / enterUpdate` 这套实际执行节拍、当前 location 变量以及 `timer1/2/3` 的单周期更新约束一起讲清楚了。

## 控制系统在文中的位置

它是论文的主控制对象，不是验证背景。作者做形式化验证的前提，就是先把这套换道逻辑从 MATLAB 代码翻译成 EFSM，再围绕它写 specification 和 non-blocking 检查。

更具体地说，文中我们关心的不是 Supremica 工具本身，而是 `Planner` 里的 `Lateral State Manager`。这使得它对 `sources/` 很有价值，因为这里抽到的是“真实代码里的主状态机如何按 update 周期运转”，而不是只给几条高层 maneuver 名称。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补进的是一个很好的 `自动驾驶换道 + 主状态机实现节拍` 样本。后续如果要训练或比较“状态机自然语言是否保住 entry / during / timer / request-side consistency”这几类细件，这篇会比只给状态集合的车道变换论文更有区分度。

做数据集时，第一轮最值得盯住的是 `NoRequest -> 请求后中间状态 -> Finished -> 回到 NoRequest` 这条主链，以及每次 planner update 如何只触发一次状态推进、timer 如何按 update 计数、direction 如何持续和 request 对齐。工具链、非阻塞验证算法和状态空间爆炸讨论可以放到第二轮再看。

## 如果需要人工细读，建议怎么读

如果后续需要人工细读，建议先看第 4 页 `A. Planner` 和 `B. Lateral state manager`，把 `Planner` 的职责、`LSM` 的七位置集合和初始/完成态读稳；然后读第 5 页 `C. Implementation`，重点圈出 `updateState / duringUpdate / enterUpdate` 三类方法的调度关系，以及 7-valued location variable、75 个 location、123 条 transition 这些实现级信息；最后再看第 5-6 页 `Specifications`，确认 `direction` 一致性和 `timer1/2/3` 的单周期增量约束。

像第 2-3 页里更偏 EFSM 形式化定义和一般性预备知识的内容，可以放到第二轮再看。除非你是在追某个验证公式，否则第一次人工复核只需要先把主状态机与 update 节拍读稳；即使 `STM.md` 之后需要重做，这条阅读路线也足够支撑人工重新把案例抽出来。
