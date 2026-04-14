# 航空航天与飞行/空管控制 / State machine modeling of the Space Launch System Solid Rocket Boosters

## 论文在讲什么

这篇论文讨论的是 NASA 在 `Space Launch System` 项目里怎样用状态机去建模固体火箭助推器（`SRB`）的关键行为。它不是泛泛讲 SysML 或系统工程流程，而是把左右助推器及其 avionics、`FSS`、`SRM`、`TVC`、separation 等子系统放进一个可执行的 `Stateflow` 模型里，并围绕点火和分离两个 use case 做 nominal / off-nominal 状态分析。

如果只抓住对我们最有价值的部分，可以把它理解成“一个航天发射阶段的层次状态监督模型”。文中对 `SRM off / ignited / burnout`、点火命令序列、点火失败、左右点火时间差，以及 `t >= tHat`、`p <= pHat` 这些分离条件的写法都很集中，所以它并不是那种只有系统简介、没有控制链的航天论文。

## 控制系统在文中的位置

这里的控制系统描述是论文的主要分析对象。作者的目标就是把 `SLS` 的助推器系统状态抽象出来，借此支持系统工程、过程验证和故障管理，所以状态机本身不是附带案例，而是整篇文章的承载骨架。

更具体地说，本文并没有把连续动力学当作主轴，而是刻意把真正适合做状态分析的离散逻辑保留下来，例如 booster 顶层状态、substate 组织、点火命令顺序、点火异常和 separation guard。对 `sources/` 而言，这种样本的价值就在于：它把复杂航天系统切成了可以直接转成状态机自然语言描述的工程监督链。

## 对我们为什么有用

这篇论文补进的是文库里相对少见的“发射系统助推器层次监督控制”样本。它和常见的 UAV mission manager、飞行模式管理或 landing gear 顺序控制都不完全同构，因为这里关心的是发射前后的 booster ignition / separation 逻辑，而且还保住了 mission elapsed time 与 motor pressure 共同作为 transition guard 的组合条件。

另外，它对后续自动生成数据集也有实际意义：一方面，它提供了比较标准的 `顶层状态 -> 子系统子状态 -> use case 序列 -> off-nominal 分支` 组织方式；另一方面，它把 `tHat / pHat` 这种工程 guard 直接写在状态转移条件里，便于后续提取成更适合建模的自然语言模板，而不只是停留在“某系统会在某阶段分离”的泛描述。

## 如果需要人工细读，建议怎么读

如果后续要人工细读，建议先略读第 1-3 页，只确认 `SLS / SRB` 系统边界和作者为什么要做 state analysis；然后直接跳到第 7-10 页，把 `left/right SRBs as states`、`subsystems modeled as substates`、`SRM off / ignited / burnout`、点火异常情形和 `[(t >= tHat) && (p <= pHat)]` 这些关键语句重新标出来，这一段就是后续重做 `STM.md` 时最核心的证据区。

像前面的 FSM 基础理论和更广义的 systems engineering 背景，可以放到第二轮再看。第一次人工复核时，最重要的是先把“模型层次怎么分、点火链怎么走、分离 guard 是什么、作者分析了哪些 off-nominal 情况”四件事读稳；只要这四件事清楚，这篇论文就足够稳定地服务于状态机样本抽取。
