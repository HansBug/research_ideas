# 土耳其铁路联锁进路与道岔超时控制 / The Application of Automation Theory to Railway Signaling Systems: The Turkish National Railway Signaling Project

## 论文在讲什么

这篇论文围绕土耳其国家铁路信号项目中的联锁软件开发展开，当前 `STM.md` 抽到的核心对象是“土耳其铁路联锁系统中的进路请求与道岔锁闭控制器”。如果只抓一句话理解它的主体，可以先把它看成：这是一个把 `TCC` 请求、进路表、信号灯色、道岔位置和 `7 s` 超时错误链放在同一处说明的铁路联锁样本。

从现有条目看，文中的离散控制链主要以 `EFSM（扩展状态机）` 的方式出现，时间语义属于 `T1（工程定时 / 局部定时）`。虽然论文大量使用 Petri net 建模，但它真正有价值的部分是把“何时允许 route reservation、道岔必须满足哪些 guard、多久不到位算 fault”这些联锁主链直接写出来了。

## 控制系统在文中的位置

它是论文的核心案例对象，而不是背景知识。作者讨论 SIL、架构和 Petri net 方法，最终都是为了说明这套铁路联锁软件怎样根据进路请求和现场设备状态做安全决策。

更具体地说，这篇论文里我们关心的控制系统描述，承担的是“把 interlocking principle 落成可执行 guard 链”的角色。对 `sources/` 而言，这比纯粹讲 railway standards 或 verification process 的文章更有用，因为这里能直接抽到 route / switch / signal / track-circuit 之间的离散约束。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补进的是一个 `铁路联锁 + 显式超时 guard` 的样本。库里已有不少铁路 `T0` 进路/资源互斥条目，而这篇的价值在于它把 `switch did not reach desired position in 7 sec -> error` 这种工程定时语义也公开写出来了，因此能补足 `🚆` 方向里更接近 `T1` 的联锁控制链。

做数据集时，第一轮最值得盯住的是 `TCC request -> route table guard -> switch position / signal color -> electronic lock -> timeout-to-error` 这条主链。Petri net 一般定义、SIL 论证和 safety case 讨论可以放到第二轮再看。

## 如果需要人工细读，建议怎么读

如果后续需要人工细读，建议先看第 2 页 `2.2 The Interlocking System` 到 `2.6 Level Crossing`，先把联锁对象、信号灯色语义、道岔 `normal/reverse` 和平交口门禁接口读稳；然后直接看第 4 页 interlocking table 说明，重点圈出 `001DT-2ST` 的具体 guard 组合；最后看第 4-5 页 field component models，确认“相交进路互斥、道岔锁闭、`7 s` 不到位转 `PE`、track circuit 单占用”这几个关键离散规则。

像第 1-3 页里更偏标准背景、SIL 判定和一般性建模说明的内容，可以放到第二轮再看。除非你是在追规范来源，否则第一次人工复核只需要先把 route / switch / signal 主链读稳；即使 `STM.md` 之后需要重做，这条阅读路线也足够支撑人工重新把案例抽出来。
