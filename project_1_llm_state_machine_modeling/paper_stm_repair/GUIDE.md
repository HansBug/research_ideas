# paper_stm_repair/GUIDE.md

## 0. 定位

本文件是 `paper_stm_repair/` 的论文级工作规范，服务于第一篇论文的新主线：给定控制系统自然语言需求与初始状态机 `<NL, STM_0>`，通过无人化反馈驱动的检查、诊断、场景、仿真与修正循环得到候选 `STM_k` / Better STM。

本路径下的 `corpora/` 只承担论文级资产选用、裁决、实验角色和风险总账，不替代 project_1 已有长期文库，也不把旧 `NL -> STM` generation baseline 改名为本论文 repair baseline。

## 1. 最高优先级边界

1. **主贡献边界**：本论文主贡献是 `<NL, STM_0> -> STM_k / Better STM` 的反馈驱动状态机修正任务与无人化循环；`NL -> STM_0` 只作为 seed construction / 上游输入来源 / related work 背景。
2. **表示边界**：语义增强、可机检、可执行的状态机表示是 feedback 的必要载体；`fcstm` / `pyfcstm` / DSL 不进入标题、摘要或贡献位。
3. **文库边界**：`seed library`、`repair baselines`、`NL datasets` 是三类不同资产，不得混名、混表或共用同一统计口径。
4. **事实保全边界**：R1--R1.7 已核验事实不得静默删除、覆盖或改写；迁移必须保留旧路径、旧 ID、新路径 / 新章节、迁移理由和影响范围。
5. **smoke 样例边界**：[selected_seed_examples/](./selected_seed_examples/) 只保存后续转换器 / 诊断器 / 修正循环做最小连通性自检的静态输入样例；它不是最终实验集合、不是主结果样本上限，也不是 seed registry 的一手事实主表。
6. **四例运行边界**：R1.8-A/B/C/D/E 均为文档和文库结构 PR，不跑四例真实运行，不调用真实 LLM，不读取 `.env`；后续若用 [selected_seed_examples/](./selected_seed_examples/) 真正执行 smoke，应另建 run record。
7. **流程信息边界**：PR / issue 的执行计划、review 状态、ready gate、commit / push 汇报与 merge 进度只维护在 GitHub body / comment；本路径只保留长期结构纪律、事实总账和论文材料，不新增 `progress.md`、`task-packets/` 或跨 PR `agent_provenance.md` 作为动态流程真源。
8. **R3.1 PlantUML 恢复边界**：PlantUML normalization / recovery 只回答转换器 eligibility，不能写成 Better STM repair 效果；normalization 必须发生在官方 PlantUML `-tscxml` 前，不修改一手 raw assets，canonical STM 只能来自官方 SCXML；高基数 raw / normalized `.puml` 与官方 `.scxml` 必须压缩进 [conversion/artifacts/](./conversion/artifacts/) 下的 archive，不得提交根目录 `runs/` 散文件；主 eligibility 必须通过 source-level semantic preservation gate，高风险 action / guard / hierarchy / concurrency / pseudo-state 降级样本只能作 supplementary evidence。

## 2. 阅读顺序

1. 先读 [README.md](./README.md)：理解当前论文主线与路径总入口。
2. 再读本文件：确认文库分工、root 三件套纪律、fact-union 与长期验收口径。
3. 再读 [corpora/README.md](./corpora/README.md)：确认三类文库入口与 project-level 文库边界。
4. 需要 story / RQ / Better STM 口径时，转入 [story/](./story/) 与 [experiment_design/](./experiment_design/)。
5. 需要理解 seed 当前事实时，优先读 [corpora/seed_library/README.md](./corpora/seed_library/README.md)、[corpora/seed_library/GUIDE.md](./corpora/seed_library/GUIDE.md)、[corpora/seed_library/SUMMARY.md](./corpora/seed_library/SUMMARY.md)；后续 R2 seed 冻结以该 SUMMARY 为当前入口。
6. 需要查看 smoke 用静态样例时，读 [selected_seed_examples/README.md](./selected_seed_examples/README.md)；该目录只保存少量可读 `<NL, STM_0>` 输入和来源元数据，不能替代 [corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md)，也不能被写成最终实验集合。
7. 需要运行或审计 R3 converter v0 时，读 [conversion/README.md](./conversion/README.md)、[conversion/GUIDE.md](./conversion/GUIDE.md) 与 [conversion/toolchain_survey.md](./conversion/toolchain_survey.md)；若审计 R3.1 PlantUML recovery / normalization，还必须继续读 [conversion/normalization/README.md](./conversion/normalization/README.md)、[conversion/normalization/GUIDE.md](./conversion/normalization/GUIDE.md)、[conversion/reports/plantuml_recovery_summary.md](./conversion/reports/plantuml_recovery_summary.md) 和 [conversion/artifacts/plantuml_recovery/r3_1_committed/README.md](./conversion/artifacts/plantuml_recovery/r3_1_committed/README.md)。该层只服务四例 smoke / R4-R5 dry-run 和 conversion eligibility audit，不是 R7/R8 正式实验级转换器。
8. 需要运行或审计 R4 诊断 / 场景 / Better STM 评价门时，读 [evaluation/README.md](./evaluation/README.md)、[evaluation/EVALUATION_GATE.md](./evaluation/EVALUATION_GATE.md)、[evaluation/DRY_RUNS.md](./evaluation/DRY_RUNS.md) 与 [evaluation/GUIDE.md](./evaluation/GUIDE.md)。该层只做 gate dry-run 与 schema contract，不调用真实 LLM、不执行 repair loop、不把四例写成主实验结果。
9. 需要理解 repair baseline / 近邻当前事实时，读 [corpora/repair_baselines/README.md](./corpora/repair_baselines/README.md)、[corpora/repair_baselines/GUIDE.md](./corpora/repair_baselines/GUIDE.md)、[corpora/repair_baselines/SUMMARY.md](./corpora/repair_baselines/SUMMARY.md)；它不提供 R2 seed。
10. 需要理解纯 NL 数据源当前入口时，读 [corpora/nl_datasets/README.md](./corpora/nl_datasets/README.md)、[corpora/nl_datasets/GUIDE.md](./corpora/nl_datasets/GUIDE.md)、[corpora/nl_datasets/SUMMARY.md](./corpora/nl_datasets/SUMMARY.md)；只有生成并记录 `STM_0` 后才 crosslink 到 seed。
11. 需要追溯 PR-R1 generation-era 资产审计时，读 [evidence/README.md](./evidence/README.md)；这些旧台账不替代当前三类 corpora 总账。
12. 需要追溯 R1.5--R1.7 旧 ledger / raw search 时，读 [archive/r1_5_to_r1_7_seed_corpus_snapshot/](./archive/r1_5_to_r1_7_seed_corpus_snapshot/)；旧 [seed_corpus/](./seed_corpus/) 只保留 redirect。
13. 需要确认当前 PR / 子 PR 计划、review 状态或 ready gate 时，回到 GitHub PR / issue body 与 comment；不要在仓库文件中寻找动态施工状态.

## 3. 三类文库分工

### 3.1 seed library：上游 `NL -> STM_0` seed 方法 / 来源文库

**定义**：收集能支撑 `<NL, STM_0>` 输入构造的上游工作、论文、artifact 或人工生成来源。核心判定不是方法强弱，而是能否证明 `STM_0` 确实由 `NL` 生成、派生或人工构造得到。

| 维度 | 口径 |
|---|---|
| 收什么 | `NL -> T0 FSM/HSM/EFSM/statechart` generation / derivation / extraction-from-NL / human modeling 工作；generation actor 可以是 LLM、传统 NLP、规则 / 模板、人类、学生或混合流程。 |
| 不收什么 | 只有 `<NL, STM>` 共现但没有生成关系证据的材料；纯 repair-only；纯 protocol FSM；BPMN/process；Petri/CSP/Event-B/TLA+/LTL/STL 等非目标形式主义；关键 timed/hybrid 行为不可隔离的对象。 |
| 主要用途 | 为 R2 冻结 `<NL, STM_0>` 样本、为转换器压力分析提供输入格式、为 related work 提供上游 seed construction 背景。 |
| 不是 | 不是本论文的 STM repair baseline；不是 R2 四例 selection 本身；不是旧 `NL -> STM` generation 论文主贡献。 |

### 3.2 repair baselines：本论文修正任务 baseline / 近邻文库

**定义**：收集与 `STM_0 -> STM_k`、模型修正、模型补全、模型 refinement、诊断反馈修复、verification-guided repair、simulation-guided repair、LLM self-repair / agentic repair 相关的 prior work。

| 维度 | 口径 |
|---|---|
| 收什么 | 状态机 / UML / SysML / model artifact 的 repair、completion、refinement、consistency fixing、counterexample-guided repair、simulation / verification feedback repair、LLM-as-repair loop 等。 |
| 可兼收的边界项 | `NL -> STM` generation pipeline 中若存在 check / feedback / repair 环节，应记录“做到了什么程度”：是否自动、是否无人化、是否结构化反馈、是否可执行 / 可机检、是否有回滚 / regression。 |
| 不收什么 | 只提供初始 `NL -> STM` seed、没有修正环节的工作；纯数据集；纯 NL requirement corpus；纯 program repair、test repair、NL requirement refinement；未声称适用于 state machine / UML / SysML model artifact 的 formal-spec repair。 |
| 主要用途 | 设计本论文对照、消融、related work positioning 与 novelty boundary。 |
| 与 seed library 的关系 | 同一篇论文可以双重登记：若既有 `NL -> STM` seed 又有 repair loop，则在 seed library 记录 seed 关系，在 repair baselines 记录 repair / feedback 能力，并用 crosslink 连接。 |

### 3.3 NL datasets：控制系统纯 NL 数据集文库

**定义**：收集控制系统自然语言需求、用例、场景、系统描述、标准片段、教学案例等纯 NL 或以 NL 为主的实验输入来源。

| 维度 | 口径 |
|---|---|
| 收什么 | 控制系统 NL 需求集、公开 requirements corpus、案例系统描述、旧 Path-1 纯 NL 候选、来自 [../../CLAUDE.md](../../CLAUDE.md) § 数据集信息的 9 系统 / 101 功能安全需求、可授权学生建模的教学 / 工程文本。 |
| 不收什么 | 原始只有 NL 的对象仍归 NL datasets，不因未来可能生成 STM 而提前算 seed；只有在后续通过明确流程生成并记录 `STM_0` 后，生成后的 `<NL, STM_0>` 条目才可 crosslink 到 seed library。 |
| 主要用途 | 后续用弱模型 / 弱 prompt / 旧模型 / 学生人工生成 `STM_0`，形成 project-constructed seed；为主实验或 fallback 数据提供 NL 入口。 |
| 与 seed library 的关系 | 当某个 NL dataset 通过明确流程生成了 `STM_0`，并保留生成配置 / 人工记录 / 输出时，生成后的 `<NL, STM_0>` 可以进入 seed registry；原始 NL 数据源仍留在 NL datasets。 |

## 4. `corpora/` 根目录纪律

1. `corpora/` 是三类文库的论文级入口，不做事实总账，不维护跨条目统计；smoke 用静态样例放在同级根路径 [selected_seed_examples/](./selected_seed_examples/)，不得放入 `seed_library/` 根层造成 registry 文库职责混淆。
2. `corpora/seed_library/`、`corpora/repair_baselines/`、`corpora/nl_datasets/` 的根层横向 Markdown 文件只允许：`README.md`、`GUIDE.md`、`SUMMARY.md`。
3. 单论文、单 baseline、单 dataset 子目录可以存在，但只能承载该条目的原文、全文、BibTeX、单篇分析、artifact / dataset card，不得承载跨条目总账。单篇 seed / baseline 默认“五件套”指 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、对应 `seed_desc.md` / `baseline_desc.md`、`artifacts.md`；dataset 条目可用 `dataset_card.md`、`source_refs.md` 与可追溯样本目录替代。
4. 候选矩阵、排除记录、manual queue、crosswalk、统计结论、风险、handoff、更新日志等跨条目信息，必须进入对应 `SUMMARY.md`，不得拆成根层 `candidate_matrix.md`、`screening_ledger.md`、`dataset_queue.md` 等第二事实源。
5. `search_rounds/`、`search_results/` 等过程性证据不得作为当前文库根事实源；若仍需留痕，应整体迁入 `archive/` 或 `runs/` 并在 `SUMMARY.md` 写明过程证据入口。
6. `SUMMARY.md` 必须做到：读完后几乎能掌握文库现状，包括数量、分级、候选 / 排除、manual blocker、negative evidence、实验角色、风险和待办。

## 5. SUMMARY-first 最低字段

### 5.1 seed library / `SUMMARY.md`

| 字段组 | 最低字段 |
|---|---|
| 元数据 | `seed_id`、标题 / 来源名、年份、venue / source、DOI / URL、本地路径、来源批次。 |
| NL 输入 | NL 类型、领域、真实 / synthetic、是否公开、是否唯一输入、需求数量或案例数量。 |
| STM 输出 | FSM/HSM/EFSM/statechart 类型、T0 状态、格式、是否机器可读、是否含 timed / hybrid / protocol / process caveat。 |
| 生成关系 | 是否明确 `NL -> STM`、generation actor、方法类型、是否人工、是否 LLM、是否存在 oracle / repair / reference 泄漏。 |
| 资产可用性 | PDF、全文、BibTeX、代码、数据、raw output、license、hash / release、人工下载状态。 |
| 实验角色 | seed 方法集合角色、R2 四例可计资格、converter pressure、fallback、negative sentinel、related work。 |
| 分级与风险 | SS/SA、优先级、排除码、leakage、转换风险、事实置信度。 |
| 证据指针 | 页码 / 小节 / 本地文件 / URL；不得只写“见论文”。 |

### 5.2 repair baselines / `SUMMARY.md`

| 字段组 | 最低字段 |
|---|---|
| 元数据 | `baseline_id`、标题、年份、venue、DOI / URL、本地路径。 |
| 任务关系 | repair / completion / refinement / consistency / counterexample-guided / simulation-guided / self-repair 类型。 |
| 输入输出 | 输入模型类型、是否含 NL、输出模型类型、是否适配 FSM/HSM/EFSM/statechart。 |
| 反馈机制 | 是否有 check / verification / simulation / diagnostic feedback；反馈是否结构化；是否无人化；是否支持回滚 / regression。 |
| 可运行性 | 代码、artifact、license、依赖、是否可复跑、是否可对接 R2 样本。 |
| 对照角色 | 主 baseline、近似 baseline、消融参考、related work only、不可运行 negative evidence。 |
| 学术风险 | 与本任务不匹配处、公平性限制、数据私有、形式主义不一致、需要人工干预。 |
| 证据指针 | 页码 / 小节 / 本地文件 / URL。 |

### 5.3 NL datasets / `SUMMARY.md`

| 字段组 | 最低字段 |
|---|---|
| 元数据 | `dataset_id`、名称、来源、年份、URL、本地路径。 |
| NL 内容 | 需求 / 用例 / 场景 / 系统描述类型、控制系统领域、语言、规模、粒度。 |
| 公开与许可 | 可下载性、license、引用要求、敏感性、是否可发布派生产物。 |
| seed 构造潜力 | 是否适合弱模型 / 弱 prompt / 学生人工建模、预期缺陷类型、是否需要人工清洗。 |
| 与已有 STM 关系 | 是否已有 STM；若有，是否能证明 STM 由 NL 生成；不能证明时仍只算 dataset，不算 seed。 |
| 实验角色 | 主实验 NL 来源、fallback、教学人工 seed、负例或仅 related data。 |
| 证据指针 | 数据说明、样例文件、论文页码、URL。 |

## 6. fact-union 与迁移哨兵

后续 R1.8-B/C/D/E 必须能从新三类 `SUMMARY.md` 和迁移记录复算或解释以下当前结构哨兵；其中 seed 证据目录以 post-R1.8-B 的 `36 dirs` 为准，R1.5--R1.7 旧口径只作为 archive 审计背景：

| 哨兵 | 口径 | 不通过含义 |
|---|---|---|
| `47/47` | seed candidate matrix 与 screening ledger 对齐。 | 候选或筛选事实在迁移中丢失 / 重复 / 口径漂移。 |
| `36 dirs` | post-R1.8-B 当前 [corpora/seed_library/](./corpora/seed_library/) 下 36 个单条目证据目录已在 [SUMMARY.md](./corpora/seed_library/SUMMARY.md) 资产表和迁移表中有去向；旧 `seed_corpus/` 只保留 redirect。 | 单篇证据容器丢失、旧路径被误当当前事实源，或 24/36 口径漂移。 |
| `9/9 crosswalk` | 旧九个 direct generation baseline 的 seed-method 入账关系保留。 | 旧 generation baseline 被误删、误归 repair baseline 或 crosswalk 丢失。 |
| `R2 handoff` | `seed_selection_candidates.md` 作为 R2 四例候选 handoff 保留，但不得被误读为 seed 方法全集。 | R2 样本冻结前置信息被误读。 |
| project-level 回链 | paper1 条目保留到 project_1 `baselines/`、`sources/`、`data/`、`reproduction/` 的来源指针和核验日期。 | paper1 制造第二事实源或整体搬迁长期文库。 |

若迁移后无法复算上述哨兵，必须在对应 PR 中按 C/I 问题修复，不得以“只是文档整理”放行。

## 7. 与 project_1 既有文库的边界

| 既有入口 | 当前角色 | R1.8 处理纪律 |
|---|---|---|
| [../baselines/](../baselines/) | 项目级 generation / LLM4Modeling baseline 与历史候选文库。 | 不整体迁入、不改写为 repair baseline；paper1 只在 `seed_library` 或 `repair_baselines` 中登记被本论文实际使用 / 复核的子集，并保留回链。 |
| [../sources/](../sources/) | 项目级论文 / 系统来源池，含可能的 NL 与 STM 线索。 | 不整体迁入；`nl_datasets` 只登记被 paper1 选用或候选使用的控制系统 NL 数据源；若由 sources 构造 `<NL, STM_0>`，生成后的 seed 条目再 crosslink 到 `seed_library`。 |
| [../data/](../data/) | 项目级数据与 9 系统 / 101 需求等实验数据入口。 | 不复制敏感或大体量数据；`nl_datasets/SUMMARY.md` 记录 dataset card、规模、许可和本地路径指针。 |
| [../reproduction/](../reproduction/) | 复现实验或旧 pipeline 入口。 | 仅作为可复跑 / artifact 线索；若用于 paper1 对照或 seed 构造，必须在对应 SUMMARY 中登记版本、命令、风险和证据指针。 |

原则：project-level 文库继续作为长期事实源；paper1 `corpora/` 是论文级选用、裁决、实验角色与风险总账。不得让两边同时维护同一统计口径；paper1 若引用 project-level 条目，应以可点击路径和核验日期追踪，而不是复制成未标来源的第二事实。

## 8. R1.8 结构阶段边界与四例运行要求

下表只记录长期结构阶段的研究边界和四例运行要求；具体 PR 编号、review gate、执行进度和 ready 状态以 GitHub PR / issue body 与 comment 为准，不在仓库文件中维护。

| 阶段 | 目标 | 四例真实运行 | 长期验收口径 |
|---|---|---|---|
| R1.8-A | 冻结结构纪律、root 三件套、SUMMARY-first、fact-union 和 project-level 边界。 | 否 | 本文件与 [corpora/README.md](./corpora/README.md) 能指导后续三类文库重整，且不引入动态流程真源。 |
| R1.8-B | seed library 实际重构与旧 `seed_corpus/` 归档 / 迁移。 | 否 | seed `SUMMARY.md` 可复算 `47/47`、`36 dirs`、旧九 crosswalk seed 部分。 |
| R1.8-C | repair baselines 文库初始化。 | 否 | 不把旧 generation baseline 误当 repair baseline；只按实际 repair / feedback 能力登记。 |
| R1.8-D | NL-datasets 文库初始化。 | 否 | 纯 NL 数据源与 seed 生成关系分离；不把只有 NL 的对象提前计为 seed。 |
| R1.8-E | 三类文库总账一致性与上游同步。 | 否 | 三类 SUMMARY 一致、链接可用、#100 / 后续 R2 入口同步，所有哨兵可复算。 |

### 8.1 R1.8-E 一致性闭合门

R1.8-E 的长期验收不是新增文献或冻结四例，而是确保后续 R2 / R3 / R4 不再被旧路径误导：

1. **R2 seed 入口唯一化**：后续 R2 默认从 [corpora/seed_library/SUMMARY.md](./corpora/seed_library/SUMMARY.md) 读取 seed 候选、R2=4 handoff、资源 caveat 和旧九 crosswalk；不得直接从旧 [seed_corpus/](./seed_corpus/) 或 `evidence/baseline_*` 冻结样本。
2. **repair baseline 降级清楚**：[corpora/repair_baselines/SUMMARY.md](./corpora/repair_baselines/SUMMARY.md) 只提供修正任务 baseline / 近邻 / negative evidence，不提供 R2 seed；严格 baseline = 0 与 `completion-sysml-gwt` 的 P0 近邻身份必须保持可追踪。
3. **纯 NL 数据源不提前计 seed**：[corpora/nl_datasets/SUMMARY.md](./corpora/nl_datasets/SUMMARY.md) 只提供控制系统 NL 来源；只有生成并记录 `STM_0` 后，生成后的 `<NL, STM_0>` 才能 crosslink 到 seed。
4. **旧入口只作审计**：[seed_corpus/](./seed_corpus/) 是 redirect，[evidence/](./evidence/) 是 PR-R1 generation-era 历史审计入口，[archive/](./archive/) 是旧 ledger / raw search 快照；这些路径不得作为当前横向事实真源。
5. **上游 GitHub 同步**：相关 GitHub PR body/comment 应在对应流程中同步到 A/B/C/D/E 闭合状态和 R2 读取新 seed library 的口径；未完成前不得在上游写成完成事实。

## 9. 后续审查口径

后续维护三类文库或执行结构迁移时，审查者应重点检查：

1. 是否和 2026-06-12 导师定调、PR #100 新主线、PR #109 结构合同一致。
2. 是否把 seed、repair baselines、NL datasets 三类文库分清。
3. 是否把旧 generation baseline 当作 seed / 历史资产，而不是直接改名为 repair baseline。
4. 是否保留 R1.7 事实哨兵、manual blocker、negative evidence 与 R2 handoff。
5. 是否维护 project-level 回链，而不是制造第二事实源。
6. 是否明确四例真实运行不属于 R1.8-A/B/C/D/E。
7. 是否把 PR / issue 的执行状态留在 GitHub body / comment，而不是写入仓库正文。

## 10. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-27 01:20:00 | 增加 [representation/](./representation/) R4.5 读取链路与边界：R4.5 只负责 canonical STM JSON -> `.fcstm` / pyfcstm inspect report 的表示桥，loss ledger 全部归因到 representation/conversion，不计 repair gain。 |
| 2026-06-26 12:35:00 | 增加 [evaluation/](./evaluation/) R4 读取链路与边界：R4 只冻结 diagnostic / scenario / Better STM checklist / eligibility / human rubric v0，并用四例做 gate dry-run；没有 `STM_k` 时不得 claim Better。 |
| 2026-06-25 23:55:00 | 增加 R3.1 PlantUML normalization / recovery 读取链路与边界：它只服务 conversion eligibility audit；高基数制品必须以 [conversion/artifacts/](./conversion/artifacts/) archive 归档，主 eligibility 必须通过 source-level semantic preservation gate。 |
| 2026-06-24 17:45:00 | 增加 [conversion/](./conversion/) 读取链路与 R3 converter v0 边界：只服务四例 smoke / R4-R5 dry-run，不是 R7/R8 正式实验级转换器。 |
| 2026-06-24 10:25:00 | 增加 [selected_seed_examples/](./selected_seed_examples/) 根路径纪律：该目录只服务 smoke / 连通性自检，不是 seed registry 事实源或最终实验集合。 |
| 2026-06-16 23:08:00 | PR-R1.8-E 收敛总账一致性门：R2 当前入口统一为 [corpora/seed_library/SUMMARY.md](./corpora/seed_library/SUMMARY.md)，旧 `seed_corpus/` / `evidence/` / `archive/` 降级为 redirect 或历史审计入口，并将 seed 哨兵统一为 `36 dirs`。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 更新 seed 当前入口为 [corpora/seed_library/](./corpora/seed_library/)，旧 `seed_corpus/` 降级为 redirect，旧 ledger / raw search 迁入 archive。 |
| 2026-06-14 13:34:18 | PR-R1.8-A 新增 paper1 路径级 GUIDE，冻结三类文库、SUMMARY-first、fact-union 哨兵与 project-level 边界。 |
