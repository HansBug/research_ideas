# 多目标搜索与近距检查无人机任务框架 / A Framework for Multiple Ground Target Finding and Inspection Using a Multirotor UAS

## 论文在讲什么

这篇论文围绕一个多旋翼 UAS 的视觉引导 ground-target finding and inspection 任务展开，目标是在较大搜索区域里自动发现多个地面目标，飞到目标附近，下探到较低高度完成检查动作，然后继续转向下一个目标。论文整体采用 OODA 作为高层决策框架，并把目标检测、内部地图、投票过滤、导航与控制封装成 ROS 上的模块化系统，用两个 test case 去验证这套框架在误检、定位误差和外部扰动下仍能工作。

对 `sources/` 来说，最有价值的不是它有多少视觉算法细节，而是作者把主模块直接实现成了一套显式 FSM。原文不仅列出了 `search`、`move to target`、`re-estimate target position`、`descend`、`adjust`、`climb`、`confirm target`、`action` 这些状态，还写清了内部地图和 vote 变量如何影响目标选择，以及 false positive 在 `confirm target` 中如何被移出 internal map。

## 控制系统在文中的位置

这里的控制系统描述是整篇论文的主骨架之一。目标检测、位姿估计和 autopilot driver 都是重要子模块，但真正决定无人机什么时候搜索、什么时候接近、什么时候下探、什么时候放弃误检并转向下一个目标的，是 `3.5 Main module` 里的有限状态机。换句话说，其他模块提供感知与执行能力，FSM 则负责把这些能力组织成可以连续完成多目标任务的离散监督器。

这点很关键，因为很多无人机论文虽然也会说“高层决策”或“mission planning”，但最终只给框架图或者脚本描述。这篇则明确把状态、状态作用、控制量和目标变量写出来。尤其 `adjust` 里的比例控制、`confirm target` 的验证逻辑，以及 `Vi > H` 的候选筛选条件，使得这条控制链不仅可概括，而且可以直接回溯到原文中的具体变量。

## 对我们为什么有用

这篇论文补的是 `✈️` 方向里很实用的一类任务级 `EFSM` 样本。仓库里已经有一些 UAV 任务管理、降落或 mission planner 条目，但这篇的独特价值在于它同时保住了“多目标内部地图”“票数过滤误检”“逐目标循环访问”三件事，所以不像单目标 landing 或单次 search 行为那样容易退化成简单的单链控制。

它对后续数据集也有很好的示范作用：不是飞控连续环，不是纯感知算法，而是“高层状态机如何调度感知和动作模块完成一连串 inspection/search tasks”。这种写法很贴近真实工程里的 mission-level supervisor，适合训练模型从自然语言恢复带变量、带回退分支的任务控制器。

## 如果需要人工细读，建议怎么读

人工重读时，建议先直接看第 `7-8` 页附近的 `3.4 Internal map` 与 `3.5 Main module`。这几页能最快重建控制器骨架：先锁定 internal map 保存了什么，再看 Figure `6` 和状态说明，确认每个状态负责什么动作、谁决定目标是否有效、什么时候会落回 landing 终止。随后再读实验部分，尤其 test case 的轨迹说明和 `Table 2`，用来核对这套 FSM 在真实飞行中怎样循环访问多个目标，以及 action failure / false detection 是怎样出现的。

目标检测、blob size、颜色分割和相机参数这些内容可以第二轮再看。它们对整个系统当然重要，但如果目的是重建状态机样本，第一轮只需要把主 FSM、内部地图和 vote-based filtering 读稳即可。这样即使以后 `STM.md` 需要重做，也能直接顺着这条阅读路线把离散控制链重新抽出来。
