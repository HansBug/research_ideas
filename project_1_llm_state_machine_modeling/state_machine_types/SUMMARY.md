# Project 1 State Machine Types Summary

本文件是 `project_1_llm_state_machine_modeling/state_machine_types/` 的总账，用于记录当前已经正式入账的状态机类型论文、综述类论文、统一分类口径、关键词簇和更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 若任务涉及普通条目，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 若任务涉及综述条目，再读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
5. 最后使用本文件查看统计、双表总账、关键词簇和待补方向。

## 当前收录统计

- 已收录普通类型论文：**0** 篇
- 已收录综述类论文：**0** 篇
- 本轮新增论文：**0** 篇
- 已完成 `desc.md`：**0** 篇
- 已完成 `survey.md`：**0** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮工作：建立 `state_machine_types/` 文库骨架，固定普通论文 `desc.md`、综述论文 `survey.md` 以及双表总账口径

## 形式主义主类口径

| Emoji | 主类 | 范围 |
|---|---|---|
| 🧩 | 经典离散状态机 | `FSM`、`EFSM`、`Statechart`、`UML State Machine`、`SCXML` 等 |
| ⏱️ | 时间/时钟自动机 | `Timed Automata`、`Timed Statecharts`、`TIOA` 等 |
| 🌊 | 混成/随机扩展 | `Hybrid Automata`、概率/随机自动机、随机混成扩展等 |
| 🕸️ | Petri 网与并发网模型 | `P/T Net`、`Colored Petri Net`、`Timed Petri Net`、高层网等 |
| 🔌 | 接口/组合/契约模型 | `I/O Automata`、`Interface Automata`、`Contract Automata`、组合行为模型等 |
| 📦 | 标准、交换格式与执行载体 | `SCXML`、`PNML`、`UML/XMI`、专用 DSL、元模型、交换标准等 |

## 状态口径

| Emoji | 含义 |
|---|---|
| 🟢 | 直接可用 |
| 🟡 | 可整理 |
| ⚪ | 未收获 |
| ⏳ | 尚未提取 |

## 检索关键词簇

### 当前推荐关键词簇

- `finite state machine / extended finite state machine / statechart / UML state machine / SCXML`
- `timed automata / timed statecharts / timed transition systems / timed I-O automata`
- `hybrid automata / probabilistic automata / stochastic automata / stochastic hybrid automata`
- `petri net / colored petri net / timed petri net / PNML / hierarchical petri net`
- `interface automata / I-O automata / contract automata / reactive modules`
- `survey / review / tutorial / taxonomy / mapping study` + 上述形式主义关键词

### 已观察到的高命中特征

- 当前仍处于文库骨架初始化阶段，尚无足够正式入账样本，本节暂不下正式结论

### 已观察到的低命中特征

- 当前仍处于文库骨架初始化阶段，尚无足够正式入账样本，本节暂不下正式结论

### 检索倾向调整

- 首轮优先补 `Statechart/UML/SCXML`、`Timed Automata`、`Petri Nets`、`Hybrid Automata`、`Interface Automata` 五条主线
- survey/review 与 definition/tutorial/tool 论文并行收录，不只盯奠基论文
- 只有当标准、格式或工具论文能解释“如何构造和承载该形式主义”时，才正式入账

## 状态机类型论文总表

说明：

1. `主类` 与 `状态` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
2. `主类` 的中文释义见上方“形式主义主类口径”，`状态` 的中文释义见上方“状态口径”。
3. 除非另有说明，本表正式入账后默认按 `年份升序` 排列。

| # | 主类 | 形式主义 | 论文角色 | 标题 | 年份 | 核心功能 | 关键特性 | 构造方式 | 基础设施 | 适用场景 | 需求前提 | 状态 | 目录 |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|
| - | - | - | - | 暂无 | - | - | - | - | - | - | - | - | - |

## 综述类论文总表

说明：

1. `状态` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
2. survey 正式入账后，应继续把其引出的代表原始文献回填到下一节的追踪表。
3. 除非另有说明，本表正式入账后默认按 `年份升序` 排列。

| # | 综述主题 | 标题 | 年份 | 覆盖主类 | 覆盖的形式主义 | 是否覆盖构造方式/基础设施 | 主要价值 | 状态 | 目录 |
|---|---|---|---:|---|---|---|---|---|---|
| - | - | 暂无 | - | - | - | - | - | - | - |

## 由综述引出的待跟进原始文献

说明：

1. 本表用于把 survey/review 条目转成下一轮可执行的补库入口。
2. `优先级` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。

| # | 来源综述 | 形式主义 / 方向 | 应追踪的原始文献或标准 | 推荐原因 | 后续动作 | 优先级 |
|---|---|---|---|---|---|---|
| - | - | 暂无 | - | - | - | - |

## 待优先补入方向

1. `Harel Statecharts / UML State Machine / SCXML` 这一条“经典状态机 -> 标准化执行载体”主线。
2. `Timed Automata` 及其基础语义、主流工具承载方式和时间约束表达入口。
3. `Petri Nets` 及 `Colored/Timed Petri Nets` 的并发建模与 `PNML` 交换线。
4. `Hybrid Automata` 及其连续动态表达、分析工具和需求前提。
5. `I/O / Interface / Contract` 这条组合与接口语义主线。
6. 一篇能横向比较 `Statechart / Timed Automata / Petri Nets / Hybrid Automata` 的综述型条目。

## 更新日志

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-04-01 11:58:00 | 建立 `state_machine_types/` 文库骨架 | 新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)、[SURVEY_GUIDE.md](./SURVEY_GUIDE.md)，并固定普通论文/综述论文双表口径 |

## 失败与阻塞记录

- 当前无正式失败记录。
