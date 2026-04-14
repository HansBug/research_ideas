# 高速公路超车/跟车一体 FSM 机动选择器 / A Sliding Mode Control Architecture for Autonomous Driving in Highway Scenarios Based on Quadratic Artificial Potential Fields

## 论文在讲什么

这篇论文提出的是一套高速公路自动驾驶控制架构，整体上由 APF 路径规划、滑模控制跟踪和一个高层 behavioral logic 组成。虽然标题强调 sliding mode control 和 quadratic artificial potential fields，但真正让它进入 `sources/` 的关键，不是连续控制器本身，而是文中那个明确负责选择机动任务的 finite state machine。

作者把问题放在典型 highway 场景里：车辆需要在保持车道、超车、跟车和目标速度跟踪之间切换。论文不是只说“系统能自主超车”，而是把当前车道编号、慢车检测、目标车道安全距离、固定机动时间和 ACC 介入条件写进 FSM 逻辑里，再由低层控制器去跟踪高层选出来的参考轨迹和参考速度。

## 控制系统在文中的位置

这里的控制系统描述并不是附属配角。第 3-4 页的 `Behavioral Logic` 直接把 FSM 写成高层决策核心，说明它输出的就是 `(X_target, Y_target)` 与纵向参考速度，而低层 SMC/APF 只是去执行这些参考量。因此，从 `sources/` 的视角看，这篇论文实际提供的是“离散机动选择 + 连续轨迹执行”的耦合型控制样本。

值得注意的是，这篇稿件虽然篇幅只有 6 页，但并不空泛。它明确列出了 possible tasks、lane-change feasibility guard、`d0 + t_H v_x` 安全距离、固定 `t_LC` 机动时间，以及一个包含慢车、超车、重新并回右车道的完整仿真序列。对于短篇 letters 来说，这已经足以支撑高质量单条 STM。

## 对我们为什么有用

这篇论文补的是汽车方向一个非常有代表性的控制图像：同一个高层 FSM 不只是决定“换不换道”，还要在超车过程中临时切到 ACC，再在安全条件满足后回到原车道。这种带有机动阶段切换和安全 guard 的 highway behavior logic，对后续做自动驾驶状态机抽取和生成都很有参考价值。

它还提供了一个清晰的边界案例，帮助我们区分“可入样本的离散监督器”和“只属于连续控制实现细节的部分”。后续如果 LLM 要从论文中抽状态机，这篇论文就是一个很好的例子：真正应被抽出的不是 APF 数学细节，而是 behavioral FSM 的任务集合、guard 条件和切换顺序。

## 如果需要人工细读，建议怎么读

如果要人工重读，建议先跳到第 3-4 页 `B. Behavioral Logic`，不要被前言里大量 APF/SMC 背景带偏。这里先把 `lane keeping / left-right lane change / target velocity tracking / ACC` 这些任务抄出来，再把 `d0 + t_H v_x`、目标车道可用性和 `t_LC` 固定机动时间记下来。这一部分已经基本决定了 `STM.md` 的主干。

然后再读第 5-6 页仿真结果，用 `18 s` 进入 `state 1 (moving left)`、`29 s` 完成 ACC 段、`73 s` 并回右车道这几个时间点，核对状态切换链是否闭合。至于前面大段关于 APF 构造、势场形式和滑模控制设计的推导，可以放到第二轮再看；它们对理解低层实现有帮助，但不是重建高层 FSM 的第一优先级。
