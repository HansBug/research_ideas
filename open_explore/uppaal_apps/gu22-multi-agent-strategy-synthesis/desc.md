问题一句话：本文验证的是多自主代理在工业采石场中的 mission planning 问题，核心挑战是在代理数量增加和动作持续时间不确定时，如何同时合成并验证路径规划与任务调度策略。
方法一句话：作者将代理的移动与任务执行建成 timed game，并把强化学习与 `UPPAAL Stratego` 结合成 `MCRL`，再用后验模型检查验证学习到的策略是否满足任务顺序、位置匹配和总时限要求。
验证收获一句话：论文证明 `MCRL` 在代理数变大时明显优于纯 `UPPAAL TIGA`，可把可处理规模从 `5` 个代理扩展到 `6` 个，同时仍通过后验验证保证策略完整且正确。

## 基本信息

- 标题：Verifiable strategy synthesis for multiple autonomous agents: A scalable approach
- 中文标题：面向多自主代理的可验证策略综合：一种可扩展方法
- 作者：Rong Gu、Peter G. Jensen、Danny B. Poulsen、Cristina Seceleanu、Eduard Enoiu、Kristina Lundqvist
- 单位：Mälardalen University；Aalborg University
- 发表：International Journal on Software Tools for Technology Transfer，2022
- DOI：`10.1007/s10009-022-00657-z`
- 链接：[DOI](https://doi.org/10.1007/s10009-022-00657-z)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🤖 机器人与自主系统
- 被验证系统：工业采石场中的多自主车辆/机械 mission-planning 系统
- UPPAAL线：`UPPAAL Stratego`
- 代码/模型/仓库获取方式：论文给出了 `MALTA` 工具仓库，可获取模型生成与任务调度工具；但文中 quarry 实验配置并非以独立 benchmark 包形式发布。
- 案例/数据获取方式：案例来自 autonomous quarry 场景和工具中的地图/任务配置；原文未单独提供标准化数据集。

## 简报

这篇论文讨论的不是单机器人控制器，而是多个 autonomous agents 在共享环境中如何同时做路径规划和任务调度。它关注的难点非常明确：如果只靠穷举式模型检查，代理数一上来状态空间就爆炸；如果只靠强化学习，又很难给出形式化正确性保证。作者于是把两者拼接起来，让学习先缩小搜索空间，再用 `UPPAAL Stratego` 对学到的策略做后验验证。

- 系统：autonomous quarry 中多代理的 mission planning。
- 特点：代理数量增长快、任务顺序受约束、移动与任务执行时间不确定、需要避免共享里程碑冲突。
- 规模：重点实验比较 `3/4/5/6` 个代理；另有 `2` 代理但 `5/8/10` 个 milestones/tasks 的复杂度实验。
- 模型：每个代理由 movement `TG` 与 task-execution `TG` 组成，策略综合在 `UPPAAL TIGA/Stratego` 中完成。
- 性质：里程碑匹配、任务顺序、在给定时间上界内完成全部任务。
- 方法：`MCRL = reinforcement learning + UPPAAL Stratego + post-verification`，并通过 `MALTA` 自动生成模型。
- 结果：`UPPAAL TIGA` 在 `6` 个代理时内存耗尽；`MCRL` 仍可在约 `7.9` 或 `14.8` 分钟内得到并验证完整策略。

`采石场地图/任务 -> MALTA 生成 timed games -> RL 学习候选策略 -> UPPAAL Stratego 后验验证 -> 得到可证明满足约束的 mission plan`

## 论文定位

它属于 `🤖` 场景下的策略综合与可验证规划案例，但论文真正验证的是代理行为控制与任务执行逻辑，因此放在 `🎛️ + 🤖` 更稳妥。它也属于非常典型的 `UPPAAL Stratego` 应用线：综合不是终点，验证才是闭环的最后一步。

## 验证对象与问题背景

### 系统与场景

论文的工业案例是 autonomous quarry：运输车辆和装载设备需要在一个带障碍物的采石环境中移动，到达指定里程碑并按顺序完成任务。

### 系统组成与运行机制

系统的关键对象包括：

1. map、milestones 和 forbidden areas；
2. 多个 autonomous agents；
3. 每个代理的 movement 行为；
4. 每个代理的 task execution 行为；
5. 全局任务顺序与时间限制。

代理必须：

1. 找到通往目标里程碑的路径；
2. 在正确位置执行正确任务；
3. 在有不确定持续时间的情况下仍完成整个任务链；
4. 避免与其他代理在共享位置和任务上发生冲突。

### 验证边界

论文主要验证的是 mission planning 层，不深入建模低层感知、连续控制或动态避障算法。动态避障被视为已由其他机制处理，本文聚焦静态 mission plans。

### 核心问题

作者希望同时解决：

1. 计划综合能否覆盖环境不确定性；
2. 代理数变大后是否仍能算得动；
3. 学习得到的策略能否像模型检查那样给出形式化保证。

## 模型与形式化建模

### 抽象对象

论文用两个 timed game 描述单个代理：

1. movement `TG`：在里程碑之间移动；
2. task execution `TG`：在指定里程碑上执行任务。

多个代理的全局模型则由这些局部游戏并置而成。

### 关键建模机制

1. 任务位置通过 `position[id][i]` 等布尔量绑定；
2. 任务完成状态通过二维数组 `tf[n][i]` 跟踪；
3. 时间约束由全局时钟 `x/gt` 等变量记录；
4. 环境中的不确定移动/执行时间由 game 结构和学习阶段共同处理。

### 工具链

`MALTA` 的结构包括：

1. `MMT` 图形配置界面；
2. path planner；
3. model generator；
4. task scheduler。

其中 task scheduler 会根据问题规模选择 `TAMAA`、`UPPAAL TIGA` 或 `UPPAAL Stratego/MCRL`。

## 验证目标与性质

### 待验证问题

论文将任务要求落实为三类核心查询：

1. 代理执行任务时是否确实位于该任务对应里程碑；
2. 任务顺序是否被遵守；
3. 所有代理是否都能在时间上界内完成任务。

### 性质类型

它们分别对应：

1. 安全/一致性性质；
2. 顺序约束性质；
3. 有界活性/时间达成性质。

### 查询表达

文中的代表性后验验证查询包括：

1. 里程碑匹配：
   `A[] (te_n.T_i imply move_n.P_i) under opt`
2. 任务顺序：
   `A[] (te_n.T_i imply tf[n][i-1] == true) under opt`
3. 时间要求：
   `A<> ((forall(i:int[0,N-1]) fin[i] >= M) imply x <= TL) under opt`

这些查询的关键点在于都加了 `under opt`，即在学习到的策略约束下再次做模型检查。

## 核心方法与验证流程

1. 用户通过 `MMT` 配置地图、里程碑、任务和代理。
2. path planner 先生成静态路径。
3. `MALTA` 自动生成 movement / task execution timed game。
4. 若规模较大，则采用 `MCRL`：
   - 用 simulation + Q-learning 学习候选策略；
   - 将候选策略重新送回 `UPPAAL Stratego`；
   - 通过后验模型检查证明其满足所有要求。
5. 最终输出可执行 mission plan。

## 案例与结果

### 代理数扩展实验

在 `3` 个 milestones 和 `3` 个 tasks 的环境中：

1. `UPPAAL TIGA` 处理 `3` 个代理只需约 `220 ms`，`4` 个代理约 `18.1 s`；
2. 到 `5` 个代理时，`UPPAAL TIGA` 已需约 `53.8 min`；
3. 到 `6` 个代理时，`UPPAAL TIGA` 直接 `Out of memory`；
4. 同一场景下，`MCRL` 仍能处理 `6` 个代理，内部 `Q-learning` 约 `7.9 min`，外部 `Q-learning` 约 `14.8 min`。

### 完整性与正确性

表 4 显示：

1. `4` 个代理时，内外部 `Q-learning` 都能用 `100` 条 sampled traces、`2000` 轮仿真得到 complete strategy；
2. `5` 个代理时，需要 `200` 条 traces，分别约 `10000/20000` 轮仿真；
3. `6` 个代理时，仍能得到 `True` 的 completeness。

这说明学习后的策略并非“看起来能跑”，而是经过模型检查确认可覆盖环境非确定性。

### milestones/tasks 扩展实验

论文也给出了一个反向结论：

1. 当代理数固定为 `2`，但 milestones/tasks 增至 `8` 或 `10` 时，`UPPAAL TIGA` 反而优于 `MCRL`；
2. 当 milestones/tasks 为 `10` 时，两种 `Q-learning` 生成 complete strategy 的成功率都低于 `10%`。

因此 `MCRL` 并非全域优于 `TIGA`，而是更适合“代理数大”的情况。

## 与本研究的关系

### 相关性分析

它和博士研究的联系在于：论文展示了如何把“学习 + 验证”真正闭环化。学习负责减轻状态空间爆炸，模型检查负责把策略重新拉回可证正确的轨道。

### 可借鉴之处

1. 先学后验，而不是把学习结果直接当真。
2. 用查询簇分别表达位置一致性、任务顺序和全局截止时间。
3. 通过自动模型生成工具减少人工建模负担。

### 存在的不足与改进空间

1. 动态避障和更复杂环境被抽象掉了。
2. 当 milestones/tasks 很大时，学习仍然会遇到稀有“好轨迹”不足的问题。
3. 原文公开了工具，但未把 quarry benchmark 做成一个独立标准数据包。

### 对本研究的启发

它说明“生成-验证-修复”闭环里，`LLM` 或学习模块并不一定直接输出最终可信模型，更现实的方式是输出候选策略，再交给形式验证阶段做兜底筛选。

## 重要的相关工作

### 1. `UPPAAL TIGA/Stratego` 自主系统主线

- 本文把 timed game synthesis、reinforcement learning 和 post-verification 合到一起，是自主系统应用中很典型的 `Stratego` 路线。

### 2. `MALTA` 工具链

- 文中 `MALTA` 负责从任务环境自动生成模型，这对后续把复杂现实场景压缩成可验证状态机非常有参考价值。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：`MALTA` 工具仓库可公开访问，但文中 quarry 具体实验环境与结果配置不是以独立 benchmark 形式单独发布。
- 获取方式/链接：[DOI](https://doi.org/10.1007/s10009-022-00657-z)；[MALTA 仓库](https://github.com/rgu01/MALTA)
- 对后续复用的现实影响：可直接参考模型生成和策略综合框架，但若想复现论文中的 quarry 结果，仍需按正文整理任务环境和参数。
