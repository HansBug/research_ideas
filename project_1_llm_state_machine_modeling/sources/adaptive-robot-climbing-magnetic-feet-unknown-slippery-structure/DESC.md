# 磁足攀爬机器人相位切换与滑移恢复控制 / Adaptive Robot Climbing with Magnetic Feet in Unknown Slippery Structure

## 论文在讲什么

这篇论文研究的是磁足攀爬机器人在未知湿滑结构表面上的一步步攀爬控制。核心问题不是一般的轨迹跟踪，而是当接触面摩擦和磁吸附能力并不确定时，机器人如何在多接触攀爬过程中既保持动作推进，又能在滑移发生时及时恢复。

作者把整个 climbing controller 写成一个很清晰的相位状态机：`full-support`、`pre-swing transition`、`swing`、`post-swing transition`。这个状态机不是单纯的 gait naming，而是直接决定每一相使用什么样的 whole-body locomotion controller、接触维度、受力参数和 CoM 轨迹约束。

## 控制系统在文中的位置

这里的 state machine 是本文控制框架的骨架。作者先用它把一步攀爬的接触相序固定下来，再在此基础上叠加两个关键恢复机制：一是 slip detection 后的 CoM trajectory re-planning，二是基于 slip velocity 的 online weight adaptation。也就是说，状态机负责给出“当前处在哪个接触相位”，而扩展变量负责决定“在这个相位里遇到滑移时应该怎样修正”。

这也是为什么它更适合按 `EFSM + T1` 来理解，而不是普通 `FSM`。因为转移不仅依赖相位切换，还依赖滑移检测、摩擦系数估计、磁吸附估计和当前相位剩余时间；这些变量都会改变后续轨迹与接触力分配。

## 对我们为什么有用

对 `sources/` 来说，这篇论文的价值在于它提供了一个很少见但非常清晰的“相位状态机 + 故障/异常恢复”样本。很多机器人步态论文会给出接触相序，但不会把滑移恢复入口、何时重规划、何时改权重写得这么明确；这篇文章则把这些控制链条压得很实。

如果后续要把它用于 project1 的状态机数据集，最值得保住的是五类信息：四个 climbing 相位、滑移检测发生的相位窗口、重规划触发条件、CoM 重规划的目标、以及基于 slip velocity 的在线权重调节逻辑。这样可以把它和普通 gait scheduler、普通 MPC 轨迹优化样本区分开。

## 如果需要人工细读，建议怎么读

建议先读第 `6` 页的 `2.2.4 Phase-based state machine`，把四个 phase 的角色读稳；然后直接跳到第 `11` 页 `4.2 CoM re-planning for slip reflex`，确认滑移是在 `pre-swing / swing` 哪些窗口里触发以及触发后改什么；最后再看第 `15` 页 `6.3`，把 slip velocity 超阈值后怎样调权重、怎样重新分配接触力补齐。

如果只是为了抽状态机语料，不必先陷进大量动力学公式。先把“相位是什么、滑移什么时候被认定、认定后怎么修”的控制主链抓出来，会更高效。
