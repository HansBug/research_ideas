# 基于行为混成自动机的医疗设备交互人机操作者模型 / A Human Operator Model for Medical Device Interaction Using Behavior-Based Hybrid Automata

## 基本信息

- 标题：A Human Operator Model for Medical Device Interaction Using Behavior-Based Hybrid Automata
- 中文标题：基于行为混成自动机的医疗设备交互人机操作者模型
- 作者：Gerrit Niezen, Parisa Eslambolchilar
- 发表：*IEEE Transactions on Human-Machine Systems*, 46(2):291-302, 2016
- DOI：`10.1109/THMS.2015.2487509`
- 链接：https://doi.org/10.1109/THMS.2015.2487509
- 形式主义：`Behavior-Based Hybrid Automata (BBHA) + ON-OFF Human Operator Model`
- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：医疗设备人机交互 / 行为混成自动机应用建模
- 工具/实现获取方式：原文明确使用 `PVS` / `PVSio-web` 模拟设备规格，并通过 `WebSocket` 将设备模型与人操作者模型闭环连接；未提供独立代码仓库。
- 标准/格式获取方式：承载方式是 behavior-based hybrid automaton、`ON-OFF` 控制模型与 `PVS` 设备规格；无独立交换标准。

## 简报

这篇论文的价值，在于它没有把“人”只当成外部假设，而是把操作者本身也建成一个混成控制模型。作者观察到，很多医疗设备上的 chevron-key 数值输入既包含离散按键，又包含连续按住后的加速变化，因此传统纯离散任务模型和传统纯连续控制模型都不够。为此，论文把 `ON-OFF` 控制理论和一个三态的 behavior-based hybrid automaton 结合起来，模拟 continuous、discrete、fine-tuning 三种操作行为。

- 形式主义定位：这是 `Hybrid Automata` 在线安全人机交互建模中的应用条目，重点是“人如何操作设备”，而不是设备本体控制律。
- 构造方式简述：先用 `ON-OFF` 控制模型给出按钮切换输出，再用 `BBHA` 切换连续、离散和精调三种行为模式，最后与 `PVS` 设备模型闭环联接。
- 基础设施与场景简述：依托 `PVSio-web`、chevron-key syringe pump 规格、操作者日志与实验对照，服务医疗设备数值输入的人机交互分析。

```text
目标数值 + 设备显示误差 -> ON-OFF control + BBHA -> 按键输入流 -> PVS 设备模型 -> 新显示值 -> 误差反馈
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象包括：

1. 参考值 `x_ref` 与显示输出 `y(t)`。
2. 误差信号 `e(t)` 与误差导数 `\dot e(t)`。
3. continuous、discrete、fine-tuning 三种用户行为模式。
4. chevron-key 四级离散输入。
5. 反应时延、观察噪声与控制噪声。
6. 与 `PVS` 设备规格联动的闭环仿真。

### 核心抽象

原文没有把 behavior-based hybrid automaton 写成一个统一元组，但根据其状态图与控制律，可保守整理为：

$$
H = (B, X, f, G, R, b_0)
$$

上式中的符号逐项解释如下：

1. `B = \{\mathrm{continuous}, \mathrm{discrete}, \mathrm{fine\text{-}tuning}\}` 是行为模式集合。
2. `X` 是连续变量集合，可包含 `e(t)`、`\dot e(t)`、`u(t)` 与 overshoot counter `c(t)`。
3. `f` 为各模式下的连续或脉冲化控制律。
4. `G` 是模式切换守卫，例如误差阈值和 overshoot 次数。
5. `R` 是切换时的重置或更新规则。
6. `b_0` 是初始行为模式。

误差信号是：

$$
e(t) = x_{ref} - y(t)
$$

其中：

1. `x_{ref}` 是用户想输入的目标值。
2. `y(t)` 是设备当前显示值。
3. 误差既驱动模式切换，也驱动按键选择。

论文把四级 chevron-key 切换函数写成：

$$
\beta_m = k_1 \mathrm{sgn}(e(t)) - k_2 \mathrm{sgn}(\dot e(t))
$$

并令：

$$
k_1 = \frac{11}{2},\quad k_2 = \frac{9}{2}
$$

上式中的符号逐项解释如下：

1. `\beta_m` 是四级离散控制输出。
2. `\mathrm{sgn}(e(t))` 决定当前误差方向。
3. `\mathrm{sgn}(\dot e(t))` 决定误差变化趋势。
4. 参数取值使四个离散等级正好映射到 `big down / small down / small up / big up`。

### 一个最小例子与通俗解释

论文讨论的是带四个 chevron 键的 syringe pump 数值输入。一个最小例子可以这样理解：

1. 当目标值和当前显示值相差很大时，操作者往往按住 `big up` 或 `big down`，表现为 continuous behavior。
2. 当误差降到某个阈值后，操作者改成短按，表现为 discrete behavior。
3. 如果多次越过目标值，操作者只会再用小步修正，进入 fine-tuning behavior。
4. 设备每更新一次显示值，误差又反馈回操作者模型，形成闭环。

通俗地说，这个模型像“把一个熟练护士输入泵速时的按键习惯，拆成三种会切换的控制模式”，而不只是把按键序列当作脚本重放。

### 运行 / 接受 / 转移语义

continuous behavior 下的控制律是：

$$
u(t) = k_p \left( k_1 \mathrm{sgn}(e(t)) - k_2 \mathrm{sgn}(\dot e(t)) \right)
$$

discrete behavior 则引入脉冲窗函数：

$$
u(t) = k_p \left( k_1 \mathrm{sgn}(e(t)) - k_2 \mathrm{sgn}(\dot e(t)) \right)\Pi(t-n\tau)
$$

fine-tuning behavior 只保留小步调整：

$$
u(t) = k_p (k_1-k_2)\mathrm{sgn}(e(t))\Pi(t-n\tau)
$$

上式中的符号逐项解释如下：

1. `u(t)` 是发给设备的控制输入。
2. `k_p` 是控制增益。
3. `\Pi(t-n\tau)` 是周期脉冲函数，用来模拟“按一下再松开”的离散按键。
4. `n\tau` 表示设备仿真步长与用户离散按压节拍。

模式切换条件也很明确。论文在 `t \bmod \tau = 0` 时检查：

$$
x_{ref} > 100 \land e(t) \le 100
\quad \lor \quad
x_{ref} \le 100 \land e(t) \le \alpha x_{ref}
$$

满足时从 continuous 切到 discrete。若 overshoot 次数足够多，则进入精调：

$$
c(t) > 2 \land e(t) < 1.0
$$

其中：

1. `\alpha` 是 switch sensitivity。
2. `c(t)` 是输出穿越目标值的次数。
3. 这套守卫恰好对应论文图中的三态混成切换逻辑。

### 语义边界

这篇论文的边界主要体现在：

1. 它建模的是 numeric entry interaction，不是一般认知任务规划。
2. 重点是 chevron-key 这种“离散按钮 + 按住连续变化”的接口。
3. 设备本体通过 `PVS` 规格接入，论文不重写设备控制软件本身。
4. 模型关注平均操作行为与相似性验证，不处理丰富心理状态。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 误差定义 | `$e(t) = x_{ref} - y(t)$` | 一切行为切换与控制输出都围绕输入误差。 |
| 四级切换函数 | `$\beta_m = k_1 \mathrm{sgn}(e(t)) - k_2 \mathrm{sgn}(\dot e(t))$` | 决定按大键还是小键、上键还是下键。 |
| 参数求解 | `$k_1 = 11/2,\ k_2 = 9/2$` | 使四级输出与 chevron keys 对应。 |
| continuous 控制律 | `$u(t)=k_p(k_1\mathrm{sgn}(e)-k_2\mathrm{sgn}(\dot e))$` | 模拟长按操作。 |
| discrete 控制律 | `$u(t)=k_p(k_1\mathrm{sgn}(e)-k_2\mathrm{sgn}(\dot e))\Pi(t-n\tau)$` | 模拟离散短按。 |
| fine-tuning 守卫 | `$c(t)>2 \land e(t)<1.0$` | 多次 overshoot 后改为小步精调。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 三种用户行为模式是模型主体。 |
| 事件 / 触发 | 强支持 | 误差阈值、overshoot 次数和仿真步点触发模式切换。 |
| 守卫 / 数据 | 强支持 | `e(t)`、`\dot e(t)`、`c(t)` 与 `x_ref` 共同决定转移。 |
| 层次 | 弱支持 | 重点是三态切换，不是层次控制图。 |
| 并发 / 同步 | 部分支持 | 人与设备构成闭环同步，但主体不是并发协议建模。 |
| 时间约束 | 部分支持 | 反应时延与离散按压周期是关键，但不是 timed automata 风格时钟约束。 |
| 连续动态 / 随机性 | 强连续、弱随机 | 误差控制是连续的，噪声以统计方式进入模型。 |
| 可执行 / 可验证性 | 强执行、强对比 | 可闭环仿真，并能与实验日志比较。 |

### 形式化问题与性质

1. 论文真正补的是“操作者本身”这一层，而不是单纯设备状态机。
2. `BBHA` 在这里把连续误差调节与离散按键策略统一起来了。
3. 它不是泛泛的 HCI 任务图，而是可直接接到设备形式规格上的闭环模型。
4. 因而对 `Hybrid Automata` 主干来说，这是很有代表性的人在环应用条目。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先确定设备接口和数值显示逻辑。
2. 再定义误差、误差导数和 overshoot 计数。
3. 用 `ON-OFF` 控制律构造不同按键层级输出。
4. 用 `BBHA` 组合三种用户行为模式，并与设备规格闭环。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. behavior-based hybrid automaton 状态图。
2. `ON-OFF` 控制方程与矩形脉冲函数。
3. `PVS` 设备规格。
4. `PVSio-web` 与 `WebSocket` 闭环仿真接口。

### 交换与互操作

互操作重点在：

1. 用户模型如何把 `u(t)` 映射为设备按键输入。
2. 设备模型如何把新显示值反馈成 `y(t)`。
3. 实验日志如何与仿真结果对比，验证模型是否贴近真实操作。

## 配套基础设施

- 建模/编辑工具：原文依托 `PVS` / `PVSio-web` 与数学仿真环境。
- 解析/交换/元模型支持：设备规格以 `PVS` 表示，无统一交换 schema。
- 仿真/执行支持：`PVSio-web` + `WebSocket` 提供闭环仿真。
- 验证/分析支持：通过实验日志与仿真对照评估模型有效性。
- 代码生成/转换支持：原文重点不在代码生成。
- 标准化或社区生态：依托混成系统、人机系统与医疗设备形式方法研究线。

## 适用场景与需求前提

### 适用场景

适合医疗设备、工业设备或任何使用离散数值输入且存在长按/短按混合行为的 HMI 分析任务。

### 需求前提

1. 用户输入目标可以抽成数值跟踪误差。
2. 设备输入是有限离散按钮集。
3. 设备显示更新可被形式规格或仿真模型接住。
4. 关注点主要是操作行为与交互安全，而不是复杂认知推理。

### 不适用或高成本场景

如果交互任务高度语义化、依赖复杂视觉搜索或需要完整认知架构，仅用这类控制导向 `BBHA` 会过于粗糙。

## 与相邻形式主义的关系

相对 [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)，本文是混成自动机在人机交互中的具体应用；相对 [A Hybrid Automata Approach for Monitoring the Patient in the Loop in Artificial Pancreas Systems](../a-hybrid-automata-approach-for-monitoring-the-patient-in-the-loop-in-artificial-pancreas-systems/desc.md)，它同样位于医疗场景，但前者建模患者/故障监测，本文建模操作者输入行为；相对纯任务分析或状态图式 HCI 模型，本文显式保留了连续误差调节语义。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提醒 `project_1`：需求到状态机建模并不总是只针对设备本体，人在环行为也可能需要被形式化成混成状态机。

### 作为目标形式主义还是中间表示

对人机交互输入行为建模，它可以直接作为目标形式主义；对更复杂系统，则很适合当“操作者层”中间模型。

### 对需求到模型生成的启发

1. 若需求同时包含离散按键和连续调整，普通 `FSM` 往往不够。
2. 人在环需求可以通过误差、阈值和 overshoot 这类可观测量进入模型。
3. 设备规格与用户模型的闭环联接，对验证实际可用性很关键。

## 重要的相关工作

- [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)：本文应用的上位理论蓝本。
- [A Hybrid Automata Approach for Monitoring the Patient in the Loop in Artificial Pancreas Systems](../a-hybrid-automata-approach-for-monitoring-the-patient-in-the-loop-in-artificial-pancreas-systems/desc.md)：同属医疗场景下的混成自动机应用。
- `PVSio-web` / `PVS`：论文设备侧闭环仿真的关键基础设施。

## 文献分类总结

- 这是一篇 `🌊` 类高价值应用条目，核心贡献是用 `BBHA + ON-OFF` 控制把人操作者输入行为形式化。
- 它的描述客体主要是人机交互控制行为，因此记为 `🎛️`；论文语境位于医疗设备与人在环系统，因此记为 `🌡️`。
- 对 `project_1` 来说，它为“混成状态机不只建模设备，也可建模人机操作层”提供了直接证据。
