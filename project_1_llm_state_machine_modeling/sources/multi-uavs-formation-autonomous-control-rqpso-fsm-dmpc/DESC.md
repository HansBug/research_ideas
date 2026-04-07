# 多无人机编队重构与威胁规避模式管理 / Multi-UAVs Formation Autonomous Control Method Based on RQPSO-FSM-DMPC

## 论文在讲什么

这篇论文研究的是多无人机编队在敌方威胁环境中的自主重构控制。作者把虚拟 leader 编队模型、DMPC 控制器和一个 finite state machine formation manager 结合起来，让编队在遇到预警雷达、防空雷达、禁飞区、协同干扰任务和解散命令时能够自动切换编队模式。

如果把连续优化部分先放一边，论文里对我们最重要的是那个 formation management unit。它负责先决定“当前编队应该处于哪种 mode”，再把 mode 交给 DMPC 去求具体控制量，所以它正好是一个很典型的“离散模式管理层 + 连续执行层”样本。

## 控制系统在文中的位置

FSM 在文中不是附属说明，而是整套方法的离散顶层。作者先给出多无人机模型和 threat constraint，然后专门开 Section `5` 讲 FSM formation manager，明确列出五个状态、九个 trigger event 和状态转移图，再说明该 manager 如何把 mode 传给 DMPC controller。

这意味着我们在这里抽取的不是纯数学 cost function，也不是单独的粒子群算法，而是“编队在什么条件下进入保持、重构、避障、协同任务或解散模式”的离散控制链。对 `sources/` 来说，这种 mode manager 比只写轨迹求解的 UAV 论文更直接地服务于状态机数据集。

## 对我们为什么有用

这篇最有用的地方是它把多无人机编队 supervisor 写得足够离散、足够清楚。状态名是明示的，触发事件也是明示的，而且 threat-driven transition 不是抽象的“环境变化”，而是预警雷达、防空雷达、禁飞区、加入/离队、协同攻击/干扰等非常具体的任务事件。

另外，它补的是 formation reconfiguration 这一类航空航天样本。库里虽然已有 mission supervisor、fault manager、landing controller 等 UAV 条目，但“编队在威胁环境下的 mode-level 重构”并不多，这篇能很好地补上 cooperative interference 和 formation avoidance 这两个语义位点。

## 如果需要人工细读，建议怎么读

如果后续要人工重做 `STM.md`，建议先读摘要，把“DMPC + FSM formation manager”这一层次关系先抓住；然后直接跳到 Section `5.1-5.2` 和 Figure `6-7`，把五个状态、九个触发事件以及状态图抄清；最后再回看 Section `3` 的 threat description，确认雷达、禁飞区和约束条件分别是怎样驱动状态切换的。

像后面的 RQPSO 推导、粒子群多样性公式、收敛分析和大段仿真曲线，可以放到第二轮再看。第一次人工复核最关键的是读稳“编队模式有哪些、由什么触发切换、切换后谁去干扰、其余无人机如何围绕 threat 和 reference trajectory 重新组织”。
