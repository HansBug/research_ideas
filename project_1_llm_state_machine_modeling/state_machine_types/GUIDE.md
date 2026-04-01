# `state_machine_types/` 操作规范

本文档用于固定 `project_1_llm_state_machine_modeling/state_machine_types/` 与 [SUMMARY.md](./SUMMARY.md) 的后续维护方式，作为 `project_1` 中“状态机类型谱系文库”的统一操作规范。

## 0. 文档关系与使用顺序

`state_machine_types/` 下几个核心文档的职责如下：

1. [README.md](./README.md)
   - 解释论文集定位、收录边界、单论文目录约束和推荐阅读顺序。
2. [GUIDE.md](./GUIDE.md)
   - 规定检索、筛选、目录维护、`SUMMARY.md` 回填和一致性检查的操作规范。
3. [SUMMARY.md](./SUMMARY.md)
   - 是当前论文集的总账，记录普通类型论文表、综述论文表、统计、关键词簇和更新日志。
4. [DESC_GUIDE.md](./DESC_GUIDE.md)
   - 负责单篇 `desc.md` 的结构与写法。
5. [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)
   - 负责单篇 `survey.md` 的结构与写法。

默认推荐顺序如下：

1. 先读 [README.md](./README.md)，确认本论文集为什么存在、收什么、不收什么。
2. 再读 [GUIDE.md](./GUIDE.md)，确认本轮工作流程、字段口径和回填要求。
3. 再读 [SUMMARY.md](./SUMMARY.md)，确认当前缺口、统计和失败历史。
4. 若任务涉及普通条目，读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
5. 若任务涉及综述条目，读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
6. 最后进入具体论文目录，按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> desc.md/survey.md` 的顺序工作。

## 1. 目标与任务边界

`state_machine_types/` 不是应用案例库，也不是 LLM baseline 库，而是为 `project_1` 建设“状态机类型地图”的专题文库。它主要服务以下任务：

1. 理清主流状态机族形式主义的定义、表达能力和边界。
2. 固定不同形式主义的构造方式、文件载体、元模型或标准化形态。
3. 盘点各类形式主义的基础设施成熟度，包括编辑、执行、验证、交换与代码生成。
4. 建立“需求特征 -> 适合的形式主义类型”之间的映射。
5. 为 `project_1` 选择目标形式主义和中间表示提供依据。

以下工作不属于本论文集的主任务，应避免混入：

1. `baselines/` 中那类“LLM 生成状态机”方法对比。
2. `sources/` 中那类“真实控制系统样本与 `STM.md` 抽取”。
3. 纯应用验证案例论文，若正文不解释形式主义本身。
4. 只谈求解器或验证算法，却几乎不交代形式主义对象、结构和构造方式的论文。

## 2. 分类口径

### 2.1 形式主义主类 Emoji 口径

后续在 [SUMMARY.md](./SUMMARY.md) 中，默认按以下主类维护：

| Emoji | 主类 | 范围 |
|---|---|---|
| 🧩 | 经典离散状态机 | `FSM`、`EFSM`、`Statechart`、`UML State Machine`、`SCXML` 等 |
| ⏱️ | 时间/时钟自动机 | `Timed Automata`、`Timed Transition Systems`、`Timed Statecharts`、`TIOA` 等 |
| 🌊 | 混成/随机扩展 | `Hybrid Automata`、概率/随机自动机、随机混成扩展等 |
| 🕸️ | Petri 网与并发网模型 | `P/T Net`、`Colored Petri Net`、`Timed Petri Net`、层次/高层网等 |
| 🔌 | 接口/组合/契约模型 | `I/O Automata`、`Interface Automata`、`Contract Automata`、组合行为模型等 |
| 📦 | 标准、交换格式与执行载体 | `SCXML`、`PNML`、`UML/XMI`、专用 DSL、元模型、交换标准等 |

若后续遇到稳定且高频的新主类，可以扩展，但必须在同一轮内同步更新：

1. [README.md](./README.md)
2. [GUIDE.md](./GUIDE.md)
3. [SUMMARY.md](./SUMMARY.md)
4. [DESC_GUIDE.md](./DESC_GUIDE.md)
5. [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)

### 2.2 单篇状态口径

本论文集默认使用以下状态口径：

| 状态 | 含义 |
|---|---|
| 🟢 直接可用 | 已能稳定提炼该形式主义的功能、特性、构造方式、基础设施、场景和需求前提 |
| 🟡 可整理 | 有价值，但证据还不够完整，后续需要补工具链、格式或场景信息 |
| ⚪ 未收获 | 论文与目标形式主义关联弱，或不能形成可靠产物 |
| ⏳ 尚未提取 | 论文已收录，但 `desc.md` 或 `survey.md` 尚未完成 |

### 2.3 表格中的 emoji 列口径

本论文集在正式总表中若使用 `主类`、`状态`、`评估` 等 emoji 列，默认遵循以下规则：

1. emoji 列的单元格只放 emoji，不写中文说明。
2. `主类` 列若使用 emoji，则单元格只写 `🧩 / ⏱️ / 🌊 / 🕸️ / 🔌 / 📦` 之一。
3. `状态` 列若使用 emoji，则单元格只写 `🟢 / 🟡 / ⚪ / ⏳` 之一。
4. 中文释义统一放在口径表中，不在正式总表的单元格里重复展开。

## 3. 检索策略

### 3.1 主线关键词簇

后续扩库时，优先围绕以下关键词簇进行：

1. `finite state machine / extended finite state machine / statechart / UML state machine / SCXML`
2. `timed automata / timed statecharts / timed transition system / timed I-O automata`
3. `hybrid automata / probabilistic automata / stochastic automata / stochastic hybrid automata`
4. `petri net / colored petri net / timed petri net / hierarchical petri net / PNML`
5. `interface automata / I-O automata / contract automata / reactive modules / behavior composition`
6. `survey / review / tutorial / taxonomy / mapping study / state of the art` + 上述形式主义关键词
7. `syntax / metamodel / XML / JSON / DSL / interchange format / semantics / tool support` + 上述形式主义关键词

### 3.2 检索方向优先级

优先级按以下顺序执行：

1. 经典定义型或代表型论文。
2. 直接解释语义、结构或构造方式的教程型论文。
3. 直接规定交换格式、执行语义或工具接口的标准/工具论文。
4. 综述/调查/系统映射论文。
5. 单一变体扩展论文，只有当它能补关键演化分支时才进入正式总账。

### 3.3 去偏与跳过规则

为避免把时间浪费在低命中方向，后续应主动降权以下候选：

1. 论文标题有 `state machine`，但正文主要讨论工作流编排、聊天机器人流程、agent orchestration。
2. 纯应用案例或工业系统论文，几乎不解释所用形式主义。
3. 只讲验证算法或求解器优化，不交代建模对象和构造方式。
4. 只有某种 niche 变体，却没有工具、标准或稳定引用链。

### 3.4 批量规模

本论文集当前采用以下 override：

1. 每轮实际筛查的候选论文尽量不少于 `15` 篇。
2. 每轮最终正式入账尽量不少于 `5` 篇。
3. 若因资料稀缺、开放获取限制或综述型条目不足导致未达到该规模，需要在 [SUMMARY.md](./SUMMARY.md) 更新日志中说明原因。

## 4. 筛选标准

### 4.1 收录条件

一篇论文进入 `state_machine_types/`，至少应满足以下条件之一：

1. 直接定义或系统说明某一主流状态机族形式主义。
2. 直接阐明某一形式主义的语义、结构、表示格式或建模/执行基础设施。
3. 作为 survey/review/tutorial/mapping study，对多个状态机族形式主义进行系统比较。
4. 作为标准、规范或工具核心文档，能明确回答“如何构造该形式主义”或“如何以机器可处理方式承载该形式主义”。

### 4.2 降优先级条件

以下论文可暂存为候选，但不应优先入库：

1. 只在更大框架中附带介绍一种形式主义。
2. 工具论文只关注某个局部算法优化，未清楚交代对象语义。
3. 综述范围很宽，但状态机族内容只占很小比例。

### 4.3 排除条件

以下论文原则上不纳入：

1. 与状态机族形式主义本体无稳定关联。
2. 无法获得合法可用 PDF。
3. 即使拿到 PDF，也无法生成可用 `paper_content.txt`。
4. 与已收录条目完全重复，且没有新增视角。

### 4.4 去重规则

1. 先按 DOI 去重。
2. DOI 缺失时按标准化标题去重。
3. 标题存在轻微差异时，再结合作者、年份和会议/期刊综合判断。
4. 同一形式主义允许保留多篇论文，但前提是它们在“论文角色”上确有差异，例如：
   - 奠基定义
   - 教程/语义说明
   - 标准/交换格式
   - 工具/基础设施
   - survey/review

## 5. 目录与文件规范

`state_machine_types/` 下每篇论文必须独占一个子目录。目录名应保持简洁、稳定、可读，通常采用标题关键词 slug。

每个单论文目录至少应包含：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`
4. `desc.md` 或 `survey.md`

这里额外固定以下 collection 级硬约束：

1. 本 collection 统一使用小写 `desc.md` 和 `survey.md`。
2. 普通条目默认补 `desc.md`；综述类条目默认补 `survey.md`。
3. survey 条目默认不再额外补 `desc.md`；若需要记录该 survey 覆盖的具体形式主义，应写入 `survey.md`。

## 6. 内容整理策略

### 6.1 普通类型论文需要提取什么

每篇 `desc.md` 至少应抽取以下信息：

1. 该形式主义的核心功能。
2. 关键特性，例如层次、并发、时间、数据、随机性、连续动态、组合性。
3. 构造方式与承载格式，例如图形符号、文本 DSL、XML/JSON、元模型、交换标准。
4. 配套基础设施，例如编辑器、执行器、验证器、转换器、代码生成、标准生态。
5. 适用场景与需求前提。
6. 与 `project_1` 的关系。

### 6.2 综述论文需要提取什么

每篇 `survey.md` 至少应抽取以下信息：

1. 综述覆盖的形式主义范围与时间边界。
2. 论文采用的分类轴和比较维度。
3. 各类形式主义在构造方式、基础设施和应用场景上的共性与差异。
4. 综述指出的缺口、开放问题和代表性原始文献。
5. 哪些条目值得进一步拆成单篇 `desc.md`。
6. 一份可直接指导下一轮扩库的跟进清单，而不是只给概括性结论。

这里额外固定一条硬约束：

1. 若某篇 survey 没有抽出“后续要追的原始文献/标准/工具线”，则该 `survey.md` 不算完成态。

### 6.3 必须进入总表的字段

[SUMMARY.md](./SUMMARY.md) 中必须维护两张正式表。

普通类型论文总表至少包含以下列：

1. `主类`
2. `形式主义`
3. `论文角色`
4. `标题`
5. `年份`
6. `核心功能`
7. `关键特性`
8. `构造方式`
9. `基础设施`
10. `适用场景`
11. `需求前提`
12. `状态`
13. `目录`

综述论文总表至少包含以下列：

1. `综述主题`
2. `标题`
3. `年份`
4. `覆盖主类`
5. `覆盖的形式主义`
6. `是否覆盖构造方式/基础设施`
7. `主要价值`
8. `状态`
9. `目录`

此外，[SUMMARY.md](./SUMMARY.md) 还必须维护一张由综述驱动的追踪表，至少包含以下列：

1. `来源综述`
2. `形式主义 / 方向`
3. `应追踪的原始文献或标准`
4. `推荐原因`
5. `后续动作`
6. `优先级`

字段补充规则如下：

1. 普通类型论文总表中的 `主类` 与 `状态` 若采用 emoji 口径，单元格只写一个 emoji。
2. 综述论文总表中的 `状态` 若采用 emoji 口径，单元格只写一个 emoji。
3. 中文释义在口径表中统一解释，不在正式总表中重复写。
4. 普通类型论文总表与综述论文总表都必须保留 `年份` 列，不得省略。
5. 除非本 collection 明确写出其他排序规则，否则这两张正式文献表默认按 `年份升序` 排列。

### 6.4 哪些内容进入 `desc.md` 或 `survey.md`

应进入单篇文件的内容：

1. 单篇论文可追溯的事实、分类和分析。
2. 后续论文写作时需要直接回查的形式主义定义、特性、格式和工具链信息。
3. 原文支持的比较与结论。

不应塞进单篇文件的内容：

1. collection 级检索日志。
2. 大量尚未核实的候选论文名单。
3. 只在全局尺度上有意义的宏观统计。

这些内容应统一写入 [SUMMARY.md](./SUMMARY.md)。

## 7. `SUMMARY.md` 撰写规范

[SUMMARY.md](./SUMMARY.md) 必须持续维护以下章节：

1. 当前收录统计
2. 形式主义主类口径
3. 状态口径
4. 检索关键词簇
5. 状态机类型论文总表
6. 综述类论文总表
7. 由综述引出的待跟进原始文献
8. 待优先补入方向
9. 更新日志
10. 失败与阻塞记录

其中：

1. 普通条目和综述条目必须分表维护，不得混在一张总表里。
2. 统计数字必须与两张正式表和当前目录真实内容一致。
3. 关键词簇相关章节必须采用“压缩式整合更新”，不能写成无限增长的检索流水账。
4. 若当前阶段尚未形成足够样本，则应明确写“暂不下正式结论”，不要伪造高/低命中特征。
5. 综述条目一旦正式入账，原则上必须同步把其引出的代表原始文献和后续动作回写到“由综述引出的待跟进原始文献”章节。
6. 两张正式文献表默认按 `年份升序` 排列；若因专题需要改用其他排序，必须在本文件中显式说明。

## 8. 工作流程

后续一轮完整工作默认按以下顺序执行：

1. 先读 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
2. 判断当前缺口是“普通类型条目”还是“综述条目”。
3. 先补历史欠账，再扩新条目。
4. 为新条目创建目录并补齐 `paper.pdf / paper_content.txt / bibtex.bib`。
5. 若是普通类型论文，按 [DESC_GUIDE.md](./DESC_GUIDE.md) 编写 `desc.md`。
6. 若是综述论文，按 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md) 编写 `survey.md`。
7. 若本轮处理的是综述论文，还必须把其引出的待跟进原始文献同步回填到 [SUMMARY.md](./SUMMARY.md)。
8. 最后统一回填 [SUMMARY.md](./SUMMARY.md)。
9. 一轮结束时复核统计、状态口径、分类口径与链接完整性。

## 9. 质量与可追溯性要求

1. 任何关于功能、特性、格式、工具和场景的结论都必须有原文依据。
2. 若原文没有明确给出 `XML/JSON/DSL` 等承载方式，不得主观补写。
3. 若工具生态并非论文直接给出，而是来自标准或官方站点，必须在文中显式区分“原文给出”和“外部补证”。
4. 如果证据不足，必须在 `desc.md`、`survey.md` 和 [SUMMARY.md](./SUMMARY.md) 中如实标明，而不是臆测补齐。

## 10. 与专项 GUIDE 的关系

本文件只负责 collection 级组织和总账逻辑；单篇文件的具体结构由专项 GUIDE 约束。

1. 只要任务涉及普通条目的 `desc.md`，默认必须先读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
2. 只要任务涉及综述条目的 `survey.md`，默认必须先读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
3. 若冲突涉及单篇文件结构和字段展开，以对应专项 GUIDE 为准。
4. 若冲突涉及收录边界、总表字段和统计口径，以 [README.md](./README.md) + [GUIDE.md](./GUIDE.md) 为准。
