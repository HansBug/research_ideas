# `EFSM/HSM + T0 + 双A` 候选审核 Guide

本文档用于约束 `project_1_llm_state_machine_modeling/sources/` 下 `EFSM/HSM + T0 + 原文A + 描述A` 候选样本的二次人工审核口径。它服务于后续 `60-100` 条实验数据集的受控抽样，因此重点不是“再判一次能不能收录”，而是补齐更细的**采样治理字段**。

后续使用 `codex exec` 对候选做人工式逐条审核时，必须先阅读本文，再阅读目标论文目录下的 `STM.md`、`DESC.md`，必要时回 `paper_content.txt`。执行上允许用“小批量 prompt 承载多个 case”，但每个 case 仍必须独立阅读、独立判定、独立给出结论。禁止把本文当成关键词匹配模板使用；它只提供**边界清晰的定义**和**few-shot 示例**。

## 1. 适用范围

本文仅面向以下候选池：

1. `状态机类型 ∈ {EFSM, HSM}`
2. `时间级别 = T0`
3. `原文细节充实度 = 🟢 A`
4. `描述细节充实度 = 🟢 A`
5. `数据集角色 = 💎 核心保留`

它不直接用于：

1. `T1/T2/T3` 条目；
2. `Hybrid / Protocol / Resource-flow` 条目；
3. `🧰 / 🪫 / ⛔` 条目；
4. 论文级总账状态判断。

## 2. 六个新增指标

### 2.1 `cluster_key`

用途：概括“控制图像簇”，用于后续防止把大量近同构样本同时抽入实验集。

填写要求：

1. 使用**稳定、可复用、与具体系统名解耦**的英文短横线 slug。
2. 优先描述“控制模式”，不要直接抄论文标题或系统名。
3. 粒度要够抽象，能让不同论文里的近同构样本复用同一个 key。

正例：

1. `two-tank-threshold-refill-controller`
2. `urban-driving-mission-supervisor`
3. `uav-mission-task-manager`
4. `robot-motion-primitive-execution-fsm`

反例：

1. `masat-1-fsm`
2. `paper-158-case-117`
3. `autoplant-top-level`

### 2.2 `scope_level`

用途：区分样本控制边界，避免把整机级、子系统级、构件级样本混成一锅。

可选值：

1. `整机`
2. `子系统`
3. `构件`

判定规则：

1. `整机`
   - 该控制器位于整个设备/平台的最上层，直接协调主要任务阶段或主要功能链。
   - 去掉它后，整机行为主线就不成立。
2. `子系统`
   - 该控制器服务于整机内一个主要功能层或决策层。
   - 它通常管理一大块功能，但不是整个平台唯一的顶层主控。
3. `构件`
   - 该对象更像局部功能块、动作执行器、模块控制器或某一专门功能流程。
   - 它一般挂在更大的 supervisor / planner / platform controller 之下。

边界提醒：

1. 不要因为论文写成 “top-level” 就自动判 `整机`；要看它是否真是整个平台主控。
2. 不要因为对象很“重要”就判 `子系统`；局部 lane-change controller、motion-primitive executor 往往仍是 `构件`。

### 2.3 `complexity_bin`

用途：控制实验集里的难度层次，避免全是小流程或全是大 HSM。

可选值：

1. `小`
2. `中`
3. `大`

判定规则：

1. `小`
   - 通常是单层 `EFSM/FSM`；
   - 主状态数大致在 `3-5` 个；
   - 只有一条主循环和少量分支；
   - 外部变量/结果位很少。
2. `中`
   - 可能是较厚的 `EFSM`，也可能是较轻量的 `HSM`；
   - 主状态数大致在 `5-10` 个，或者虽少于 `5` 个但每个状态内部职责较重；
   - 有较明显的 guard 组合、阶段切换、异常分支，但还没有大规模层次/并行。
3. `大`
   - 多层次 `HSM`、并行/多 autopilot/多 action-client 协调，或语义上存在明显的多阶段大链条；
   - 常伴随 superstate、submachine、任务族、fallback family、全局 fault 入口等；
   - 不要求机械数状态，但整体恢复成本明显高于普通顺序链。

边界提醒：

1. `大` 不是“论文篇幅大”，而是“控制结构大”。
2. 有层次不等于自动判 `大`；若只是薄层包装，仍可判 `中`。

### 2.4 `evidence_compactness`

用途：反映“从原文恢复当前状态机样本”到底有多费劲。

可选值：

1. `直述`
2. `整合`
3. `重构`

判定规则：

1. `直述`
   - 单个局部证据块已经足够恢复主控制链；
   - 常见形态是“某一节 + 邻近表/图”直接给出模式、guard、动作和顺序；
   - 整理时主要是把原文压成更顺的自然语言，不需要改写控制语义。
2. `整合`
   - 需要把 `2-3` 个证据块拼起来；
   - 这些证据块通常还在同一章节或邻近章节里；
   - 主链仍然稳定，但 guard、异常链、内部变量等分散在几处。
3. `重构`
   - 需要跨多处图表/表格/实现语义做较强重建；
   - 或者原文主要形式根本不是“状态机自然语言”，而是行为树、动作客户端、流程函数、接口语义；
   - 当前 `STM.md` 的状态机自然语言明显比原文更抽象了一层。

边界提醒：

1. 有图表不等于 `重构`；如果图表就在局部证据块里配合正文直说，仍可判 `直述`。
2. `重构` 不是“信息差”，而是“恢复过程需要语义转换”。

### 2.5 `hidden_time_risk`

用途：在当前总账仍记作 `T0` 的前提下，额外标记该样本未来是否可能因为回原文更细读而上浮到 `T1+`。

可选值：

1. `低`
2. `中`
3. `高`

判定规则：

1. `低`
   - 主控制链几乎完全由事件、阈值、模式结果、资源占用或离散 guard 决定；
   - 没有明显的 delay、periodic、timeout、驻留、重试窗口、速率约束等时间影子。
2. `中`
   - 当前仍可按 `T0` 用，但原文出现了 mission complete、周期 tick、循环检查、任务时限、重试次数、阶段持续等轻度时间影子；
   - 时间还不是主语义，但后续精读可能让人考虑升到 `T1`。
3. `高`
   - 原文已经明确出现了数值化 delay、period、周期监测、固定 beacon rate、超时/超窗、重试窗口或 duration-triggered 行为；
   - 只是当前总账还没把它重新定级；
   - 这类样本进入本轮纯 `T0` 主数据集前应优先谨慎。

边界提醒：

1. `hidden_time_risk` 不是重新判时间级别；它是在现有 `T0` 标签之外，加一个“稳定性”提醒。
2. 一旦原文里出现明确数值时间条件，默认至少认真考虑 `高`，不要因为当前总账写着 `T0` 就自动判 `低`。

### 2.6 `pyfcstm_fit`

用途：判断样本离 `pyfcstm` 目标表达形式还有多远。

可选值：

1. `直接`
2. `轻归一`
3. `重归一`

判定规则：

1. `直接`
   - 状态、guard、动作、异常边基本都已显式；
   - 稍做转写就能落到 `pyfcstm` 风格；
   - 不需要额外发明新的中间状态或新层级。
2. `轻归一`
   - 原文本身已经是状态机式控制链；
   - 但还需要统一命名、拆 guard/action、补初态、展开编号条件、显化父子层关系等；
   - 本质上是“规范化”，不是“改模型”。
3. `重归一`
   - 原文语义与 `pyfcstm` 之间仍隔着一层明显的建模转换；
   - 常见原因包括：行为树语义、并行 action-client 框架、任务返回码驱动、多种执行 hook、非状态机原生 formalism；
   - 需要重组控制边界、重切状态粒度或改写结构。

边界提醒：

1. `重归一` 不等于样本差；很多高价值样本反而会因为结构太丰富而落到这一档。
2. `轻归一` 与 `重归一` 的分界，不看工作量绝对值，而看“是否需要改变原控制表达的组织方式”。

## 3. Few-Shot 审核样例

下面这些样例用于给后续单条审核提供边界感。它们不是“关键词模板”，而是**判定参照物**。

### 样例 A：简单阈值控制的 `直述 + 低风险 + 直接`

- 案例：`Threshold-based refill logic for a two-tank PLC system`
- 文件：[water-tank-level-controller-by-using-plc/STM.md](../water-tank-level-controller-by-using-plc/STM.md)
- 推荐判定：
  - `cluster_key = two-tank-threshold-refill-controller`
  - `scope_level = 整机`
  - `complexity_bin = 小`
  - `evidence_compactness = 直述`
  - `hidden_time_risk = 低`
  - `pyfcstm_fit = 直接`
- 说明：
  - 原文在一段 operation description 里几乎直接写出了 `上阈值关泵/关阀` 与 `下阈值开阀/开泵` 主链；
  - 这是整套 PLC 水箱控制系统主逻辑，不是某个局部子模块；
  - 控制图像很干净，几乎可以直接转成 `pyfcstm`。

### 样例 B：局部执行控制器的 `构件 + 中等复杂度 + 直接`

- 案例：`Three-lane obstacle-avoidance lane-change controller for a WMR`
- 文件：[design-and-implementation-of-an-asynchronous-finite-state-controller-for-wheeled-mobile-robots/STM.md](../design-and-implementation-of-an-asynchronous-finite-state-controller-for-wheeled-mobile-robots/STM.md)
- 推荐判定：
  - `cluster_key = obstacle-lane-change-controller`
  - `scope_level = 构件`
  - `complexity_bin = 中`
  - `evidence_compactness = 直述`
  - `hidden_time_risk = 低`
  - `pyfcstm_fit = 直接`
- 说明：
  - 这是 WMR 内部的 lane-change / obstacle-avoidance controller，而不是整个平台 supervisor；
  - 原文直接给出 follow/check/stop 链与 `0.5m` 障碍阈值、orientation guard、PWM 输出；
  - 结构较清楚，归一化成本低。

### 样例 C：典型层次 supervisor 的 `子系统 + 中档 + 轻归一`

- 案例：`Two-Stage Mission-and-Control FSM for Urban Driving`
- 文件：[a-hierarchical-control-system-for-autonomous-driving-towards-urban-challenges/STM.md](../a-hierarchical-control-system-for-autonomous-driving-towards-urban-challenges/STM.md)
- 推荐判定：
  - `cluster_key = urban-driving-mission-supervisor`
  - `scope_level = 子系统`
  - `complexity_bin = 中`
  - `evidence_compactness = 直述`
  - `hidden_time_risk = 中`
  - `pyfcstm_fit = 轻归一`
- 说明：
  - 它是自动驾驶决策层控制器，不是整车唯一的总控，因此判 `子系统`；
  - `Mission FSM + Control FSM` 层次直接写出，局部证据块已经足够恢复主链；
  - 但 `condition 10/20/30/40/41/42` 这类编号 guard 仍需归一化，且 `mission is over` 暗示存在轻度时间边界上浮风险。

### 样例 D：证据分散但结构仍稳的 `整合 + 高隐时风险`

- 案例：`Closed-mode CONOPS and safe-mode fallback in Masat-1`
- 文件：[reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation/STM.md](../reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation/STM.md)
- 推荐判定：
  - `cluster_key = satellite-mode-fdir-controller`
  - `scope_level = 子系统`
  - `complexity_bin = 大`
  - `evidence_compactness = 整合`
  - `hidden_time_risk = 高`
  - `pyfcstm_fit = 轻归一`
- 说明：
  - 主链需要把 `CONOPS`、mode 说明和 FDIR 实现几块证据拼起来，不是单段直出；
  - 它主要覆盖飞控软件中的任务/故障管理层，更像大子系统而非整机；
  - 原文明确出现 `45 min`、`60 s`、`120 s`、periodic battery check 等时间语义，因此虽然当前总账仍标 `T0`，也应判 `高` 风险。

### 样例 E：行为树重写成状态机的 `重构 + 重归一`

- 案例：`Task activation and interruption logic for UAV mission management`
- 文件：[behavior-trees-for-uav-mission-management/STM.md](../behavior-trees-for-uav-mission-management/STM.md)
- 推荐判定：
  - `cluster_key = uav-mission-task-manager`
  - `scope_level = 构件`
  - `complexity_bin = 大`
  - `evidence_compactness = 重构`
  - `hidden_time_risk = 中`
  - `pyfcstm_fit = 重归一`
- 说明：
  - 原文主表达形式是 `Behavior Tree`，不是原生状态机；
  - 要得到当前 `STM.md` 的状态机式自然语言，必须把 transient / non-transient、tick、activation/deactivation、internal status 等运行语义重写成状态控制逻辑；
  - 它是 mission management module，而不是 UAV 整机总控，因此判 `构件`。

### 样例 F：顶层作业监督器的 `整机 + 大 + 重归一`

- 案例：`Top-level mission supervisor for the AutoPlant reforestation machine`
- 文件：[autonomous-reforestation-machine-control-system-fsm/STM.md](../autonomous-reforestation-machine-control-system-fsm/STM.md)
- 推荐判定：
  - `cluster_key = robot-mission-action-client-supervisor`
  - `scope_level = 整机`
  - `complexity_bin = 大`
  - `evidence_compactness = 整合`
  - `hidden_time_risk = 低`
  - `pyfcstm_fit = 重归一`
- 说明：
  - 它位于整机控制链顶层，协调 move / transfer / planner / planter 等主要 action clients；
  - 主链依赖顶层状态图、returned outcomes 和 status variables 共同支撑，因此是 `整合`；
  - 并行执行、superstate 和 action-client outcome 驱动让它落到 `pyfcstm` 时需要较强结构重组。

### 样例 G：大层次平台控制器的 `整机 + 大 + 轻归一`

- 案例：`Master-and-Autopilot Mission Cycle for Autonomous Rotorcraft UAS`
- 文件：[long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition/STM.md](../long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition/STM.md)
- 推荐判定：
  - `cluster_key = rotorcraft-mission-autopilot-hsm`
  - `scope_level = 整机`
  - `complexity_bin = 大`
  - `evidence_compactness = 整合`
  - `hidden_time_risk = 中`
  - `pyfcstm_fit = 轻归一`
- 说明：
  - 这是平台级 autonomy engine，直接调度 `takeoff / mission / landing / emergency landing` 四类 autopilot；
  - 证据需要把 mission architecture、autonomy engine 和 landing/emergency lander 说明合起来；
  - 虽然主链仍可按 `T0` 使用，但 `ten attempts`、mission cycle、touchdown thresholds 等让它比纯事件驱动样本更接近 `中` 风险。

### 样例 H：显式执行态表的 `构件 + 中等复杂度 + 直接`

- 案例：`RSW Motion-Primitive Execution FSM for CCRS RTAS`
- 文件：[preliminary-design-of-robotic-control-software-for-mars-sample-return-capture-containment-and-return-system/STM.md](../preliminary-design-of-robotic-control-software-for-mars-sample-return-capture-containment-and-return-system/STM.md)
- 推荐判定：
  - `cluster_key = robot-motion-primitive-execution-fsm`
  - `scope_level = 构件`
  - `complexity_bin = 中`
  - `evidence_compactness = 直述`
  - `hidden_time_risk = 低`
  - `pyfcstm_fit = 直接`
- 说明：
  - 原文直接给出状态表、`StateExit / StateEntry / StateRun / Step` 调度和全局 `FAULT` 入口；
  - 这是 `CCRS` 软件栈里的主控构件，不是整个平台任务调度层；
  - 结构已经非常接近可执行状态机。

## 4. 审核 prompt 的使用要求

后续单条或小批量审核 prompt 必须满足：

1. 先要求模型阅读本文，再阅读目标 `STM.md`、`DESC.md`，必要时回 `paper_content.txt`。
2. 输出字段固定为：
   - `cluster_key`
   - `scope_level`
   - `complexity_bin`
   - `evidence_compactness`
   - `hidden_time_risk`
   - `pyfcstm_fit`
   - `rationale`
3. `rationale` 必须简要说明：
   - 为什么判这个 `scope_level`
   - 为什么判这个 `evidence_compactness`
   - 为什么判这个 `hidden_time_risk`
   - 为什么判这个 `pyfcstm_fit`
4. 禁止只凭标题、已有 `状态机类型/时间级别` 标签或案例名猜测。
5. 若目标条目明显与本文口径冲突，应在 `rationale` 里明确指出，而不是硬套到最近的 few-shot 例子上。
6. 若一次审核多个 case，默认控制在 `2-5` 条/批，并要求：
   - 每条都输出独立 `case_id`
   - 每条都给出独立 `rationale`
   - 不允许把多个 case 合并成一条总判断
