问题一句话：本文验证的是形式化已分析的人机交互场景如何进一步映射成可运行的机器人部署系统，核心问题是设计期 `SHA + SMC` 得到的结果在 `ROS` 中间件和模拟/真实环境里能否保持可比的一致性。
方法一句话：作者在原有 HRI 设计期模型上加入 deployment features，提出从 `SHA` 子集到 `ROS` 发布订阅部署单元的 model-to-code 映射，并通过 `UPPAAL SMC + CoppeliaSim` 对设计期与运行期结果做对照。
验证收获一句话：论文显示设计期成功率区间与 `100` 次左右模拟部署结果基本一致，例如某实验在 `70 s` 内的设计期成功率为 `[0.90186,1]`，运行期统计成功率则达到 `96.1%` 或 `94.5%`，说明形式模型确实能支撑部署前评估。

## 基本信息

- 标题：A Deployment Framework for Formally Verified Human-Robot Interactions
- 中文标题：面向形式化已验证人机交互的部署框架
- 作者：Livia Lestingi、Mehrnoosh Askarpour、Marcello M. Bersani、Matteo Rossi
- 单位：Politecnico di Milano；McMaster University
- 发表：IEEE Access，2021
- DOI：`10.1109/ACCESS.2021.3117852`
- 链接：[DOI](https://doi.org/10.1109/ACCESS.2021.3117852)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🏥 医疗与健康
- 被验证系统：面向医疗服务机器人场景的形式模型到 `ROS` 部署框架
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：论文给出 `HRI Deployment` 仓库，当前可访问：[GitHub](https://github.com/LesLivia/hri_deployment)。
- 案例/数据获取方式：案例来自医疗场景仿真；论文还给出 demo 链接，但此处优先使用仓库入口。

## 简报

这篇论文解决的是一个经常被忽略的问题：即便设计期的 `UPPAAL SMC` 模型给出了很好的成功率，真正把场景部署到机器人中间件后，结果还是否可信。作者因此提出一套从 `SHA` 子集到 `ROS` 部署单元的映射规则，把 orchestrator、human、robot、battery 和 publisher queue 一一对应到运行期结构。

- 系统：形式化 HRI 模型的部署框架，而不是单个静态场景。
- 特点：`SHA -> ROS` model-to-code、CoppeliaSim 仿真、设计期/运行期双验证。
- 规模：代表性实验使用 `100` 次左右模拟运行，并比较多个 mission configuration。
- 模型：扩展后的 stochastic hybrid automata 加上 `ROS` publisher queue 模型。
- 性质：任务成功率、任务完成时间、疲劳峰值、电量残值及其与设计期估计的一致性。
- 方法：设计期先做 `SMC`，通过后再自动映射成 `ROS` 部署单元并在虚拟环境中反复运行。
- 结果：设计期和部署期指标高度接近，能有效暴露需要二次建模或调参的人类延迟行为。

`设计期 HRI 模型 -> SHA/SMC 分析 -> model-to-code 映射 -> ROS/CoppeliaSim 部署 -> 与设计期结果对照`

## 论文定位

本文属于 `🧩 + 🏥`。它真正关注的是软件框架与工作流的正确落地，而不是某个单点控制器或协议，因此适合作为软件服务/业务流程类案例。

## 验证对象与问题背景

### 系统与场景

场景仍然来自 assistive robotics，尤其是医疗服务机器人环境；但论文重点已经从“场景成功率”扩展为“如何把形式模型变成可运行部署”。

### 系统组成与运行机制

框架包含三层：

1. **设计期**
   - 用 `SHA` 建模人、机器人、电池和 orchestrator；
2. **映射层**
   - 把 automata 元素映射成部署单元、脚本与 `ROS` topic；
3. **运行期**
   - 在真实或虚拟环境中执行，其中论文主要用 `ROS + CoppeliaSim` 仿真。

### 验证边界

论文验证的是**形式模型与 `ROS` 部署层之间的一致性**，而非底层 SLAM、路径规划或真实医院环境全部细节。

### 核心问题

1. 设计期概率结果是否能在运行期被观测到；
2. `ROS` publisher queue、通信延迟和用户输入是否会破坏设计期假设；
3. 当运行期出现人类延迟、轨迹偏差时，能否反向指导模型修订。

### 研究动机

作者认为，形式方法要真正服务机器人应用，不能停在 design-time，必须贯通到 deployment-time。

## 模型与形式化建模

### 扩展 formal model

在原有 HRI 场景模型基础上，作者加入 deployment-related features，特别是：

1. `ROS` publisher queue 的 timed/stochastic 模型；
2. 传感器读数和 topic 交互；
3. SHA 到部署单元的映射函数。

### model-to-code 映射

论文定义了从 automata 到 deployment unit 的映射关系：

1. automaton 对应部署单元；
2. discrete transition 对应脚本逻辑；
3. synchronization channel 对应 `ROS` topic 消息；
4. 物理变量对应真实或模拟环境中的可观测量。

### 关键抽象

1. 仅对一类可映射的 `SHA` 子集做代码生成；
2. 人类的不确定行为在运行期由真实用户输入或模拟行为“接管”；
3. 运行期重点比较 success rate、duration、fatigue、charge，而不是逐状态强双模拟。

## 验证目标与性质

### 待验证问题

论文希望回答两类问题：

1. 设计期 `SMC` 预测的任务成功率是否可靠；
2. 若运行期出现明显偏差，是否意味着模型或参数需要修订。

### 性质类型

1. 统计成功概率；
2. 设计期/部署期一致性比较；
3. 物理变量近似一致性；
4. human-in-the-loop 异常行为下的失败分析。

### 性质分组与实际含义

1. **Mission success within `\tau`**
   - 任务是否在给定时间界内完成；
2. **Metric consistency**
   - fatigue 峰值、电量残值、任务时长是否与 `UPPAAL` 估计接近；
3. **Counter-example driven refinement**
   - 运行期异常是否指向参数或模型需要修订。

### 查询表达

论文仍以 `P_\tau(<>scs)` 类型查询为主，再把运行期成功率定义为“在 `\tau` 内成功的运行次数 / 总运行次数”，用于与 `SMC` 区间比较。

## 核心方法与验证流程

1. 先在设计期用 `UPPAAL SMC` 评估候选场景；
2. 若结果足够好，再把 automata 通过映射规则转成 `ROS` 节点与脚本；
3. 在 `CoppeliaSim` 中重复运行场景，真实用户通过输入驱动 human 行为；
4. 收集 success rate、mission duration、fatigue、charge 等日志；
5. 将运行期结果与设计期估计对照，必要时回到设计期重调参数。

这里比 2020 年两篇论文更进一步的，是它开始真正处理“模型到实现”的跨层一致性问题。

## 案例与结果

### 案例规模

1. 主要实验在模拟医疗走廊环境中完成；
2. 运行期实验对每个场景执行约 `100` 次模拟；
3. 使用 `ROS Melodic` 与 `CoppeliaSim`。

### 主要验证任务

1. 比较设计期与运行期的成功率；
2. 比较 mission duration、fatigue 和 charge；
3. 通过异常运行轨迹识别模型偏差。

### 主要结果

1. 实验 `1a` 中，设计期在 `70 s` 内的成功率区间是 `[0.90186, 1]`，运行期统计成功率为 `96.1%`；
2. 实验 `1b` 改用更高初始电量后，运行期在 `70 s` 内成功率为 `94.5%`；
3. 实验 `2` 中，`80 s` 时间界下运行期成功率达到 `100%`，并与设计期结果一致；
4. 论文还展示了因第二位人类延迟启动而导致机器人电量耗尽的失败轨迹，说明部署阶段能发现 design-time 没覆盖到的人类行为边界。

### 结果解释

作者并不把单次仿真当成形式验证替代品，而是把它当成 design-time 结果的现实校验器；两者相互补充，而不是互相替代。

## 与本研究的关系

### 相关性分析

这篇论文非常适合博士研究中的“验证结果如何反馈到系统实现与修模”的那一环。

### 可借鉴之处

1. 给出状态机到运行期实体的系统映射；
2. 用运行期日志验证设计期结论；
3. 把异常人类行为当成修模触发器。

### 存在的不足与改进空间

1. 当前主要是在虚拟环境验证；
2. 只覆盖一类 `SHA` 子集；
3. 设计期和部署期的比较仍是统计指标级，而非严格行为等价。

### 对本研究的启发

它提示本研究中的“验证-修复”闭环不能只在形式模型内部打转，还应该考虑如何把实现期观测反哺到模型侧。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：论文给出的 `HRI Deployment` 仓库当前可访问。
- 获取方式/链接：[DOI](https://doi.org/10.1109/ACCESS.2021.3117852)；[GitHub](https://github.com/LesLivia/hri_deployment)
- 对后续复用的现实影响：这是少见公开了 deployment 框架的人机交互案例，适合复用其 `SHA -> ROS` 映射思路与设计期/运行期对照流程。
