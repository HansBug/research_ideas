# 自动滑门层次化运动控制 / Mechatronic Control System on a Finite-State Machine

## 论文在讲什么

这篇论文讨论的是一个以自动滑门为对象的 mechatronic 控制系统设计。作者的核心主张不是再讲一套抽象软件工程原则，而是把自动门的控制逻辑明确组织成 `state-transition` 风格的软件结构，并用实际的 `DSP + Matlab/Simulink/StateFlow` 实现来展示这种组织方式如何落到工程控制器上。

论文真正有价值的部分在于，它没有停留在“用了 FSM”这种空泛表述，而是把控制对象、输入输出、状态层级和故障恢复都写进了一个具体系统。文中既给出 door control system 对传感器与执行器的基本关系，也给出 motion-generator FSM 的主状态、子状态和阻塞恢复策略，所以读者能从中看到一条完整的自动门运行链，而不是只看到一个状态图壳子。

## 控制系统在文中的位置

这里的控制系统就是论文主体。作者虽然也谈到了 hybrid systems、motion method、DSP rapid prototyping 和控制回路参数，但这些内容都是为了说明自动滑门控制器应如何被分层、编码和调试，而不是把自动门当成附带示例。

更具体地说，文中最值得关注的是两个层面。第一个层面是 door management 与 motion generator 之间的任务分工，说明谁负责下达运动命令、谁负责输出位置/速度/加速度参考。第二个层面是 motion FSM 的内部层级：主状态是 `init / positive / negative / stop`，正负向运动再展开为更细的 motion-profile sector 子状态，最后还有 obstacle interruption 触发的 blockade detection 和三次失败后的 error stop。也就是说，这篇论文的控制对象、状态骨架和异常恢复链都是正文正面展开的内容。

## 对我们为什么有用

对 `sources/` 来说，这篇论文最有价值的地方是补进了一个楼宇机电方向的层次化门控样本。仓库里虽然已经有不少电梯和门控类控制器，但自动滑门的表达方式与常见电梯调度不同，它更强调“门管理层 -> 运动生成层 -> 子运动扇区层”这种逐层细化结构，因此能为后续 `HSM + T0` 的自然语言样本补一个较干净的工程实例。

另外，这篇论文还补上了一个很有代表性的恢复链模板：运行中遇到 obstacle 或 movement prevention 后，不是立即终止，而是进入 blockade detection，尝试改向或恢复，直到三次失败才落到 error indication。对于后续做状态机建模、验证或修复研究的人来说，这种“正常链 + 异常链 + 重试上限”的自然语言结构非常有启发性，且比只给主流程的轻量门控稿更适合进入训练或分析母体。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `2` 页 `SYSTEM DESCRIPTION`，先确认这套 automatic door controller 的输入、输出和“new state depends on previous state and input conditions”这个总框架。接着直接跳到第 `6-8` 页 `MOTION BASED ON FSM`，优先把 `PROMACHINE_IN`、五个输出、主状态 `init / positive / negative / stop`、八个 sector 子状态和 `S20` 这类二级状态一并抄出来，因为这些内容决定了后续到底该把它抽成平面 FSM 还是层次状态机。

如果是为了补强异常分支，再跳到第 `10` 页附近看 blockade detection 那一段，把 obstacle collision、direction change、three subsequent attempts、error indicator 这些词与前面的主状态链对齐。至于前文更偏 hybrid systems 背景、控制回路参数、摩擦补偿和实验曲线的部分，可以放到第二轮再看；它们对理解工程实现有帮助，但对重做 `STM.md` 来说，优先级明显低于“状态层级是什么、谁给谁下命令、阻塞后如何恢复”这些主控制事实。
