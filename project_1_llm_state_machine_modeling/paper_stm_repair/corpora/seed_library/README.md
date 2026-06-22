# seed_library — 上游 `NL -> STM_0` seed 方法 / 来源文库

## 0. 定位

本目录是第一篇论文 `paper_stm_repair` 的 seed library，服务于 `<NL, STM_0> -> STM_k / Better STM` 任务。它记录能说明 `STM_0` 从自然语言需求、用例、场景、系统描述或文本规格生成 / 派生 / 人工构造而来的上游方法与来源。

**核心边界**：seed library 不是本论文的 repair baseline，也不是 R2 四例样本集合本身。旧 `NL -> STM` generation baseline 在这里作为上游 seed 方法集合、转换压力、相关工作 和 R2 候选来源入账；本论文主贡献仍是后续的无人化反馈驱动修正循环。

三类文库交叉入口：[../repair_baselines/](../repair_baselines/) 记录 `STM_0 -> STM_k / Better STM` 的 repair / feedback 近邻；[../nl_datasets/](../nl_datasets/) 记录只有 NL、尚未闭合 `STM_0` 生成关系的数据源。若同一对象跨库出现，必须在各自 `SUMMARY.md` 中按 seed / repair / NL 角色切片并互链。

## 1. 阅读顺序

1. 先读本 [README.md](./README.md) 理解文库边界。
2. 再读 [GUIDE.md](./GUIDE.md) 理解收录、分级、更新和验收规则。
3. 重点读 [SUMMARY.md](./SUMMARY.md)：这是研究结论与统计摘要入口。
4. 需要逐条资源明细时读 [REGISTRY.md](./REGISTRY.md)：它是一手 `NL + generated STM_0` 资源明细主表，包含每个 seed 的一手入口、pair 统计、blocker、assets 链接和 R2 选择建议。
5. 进入单条目目录时，默认读取 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> seed_desc.md -> artifacts.md`；artifact-only 条目按 `seed_desc.md -> artifacts.md -> 原始 metadata / package` 顺序。
6. 需要旧 R1.5--R1.7 ledger / raw search 时，进入 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)；archive 只作审计，不是当前事实真源。

## 1.5 结论速览

目前的横向结论是：**严格种子 3 条、条件种子 / 方法证据 6 条、边界 / 相关工作 6 条、仅元数据 1 条**。

| 结论级别 | 代表条目 | 一句话判断 | 详情 |
|---|---|---|---|
| 严格种子（3） | `sefm-llm-state-machine`、`llms-emp-stm-subset`、`maritaca-use-case-behavior-models` | 真实 `NL -> STM` 关系清楚，且 STM family 在 T0 内 | 以 [SUMMARY.md](./SUMMARY.md) §16 为准 |
| 条件种子 / 方法证据（6） | `automated-transition-use-cases-uml-sm`、`designing-fsm-gpt4`、`unified-uml-multimodal-validation`、`dependable-product-families-usecases-state-machines`、`statechart-use-case-validation-event-driven`、`rscharter-statechart-elements` | 关系成立但带合成、可变性、验证导向或中间层边界；不等于当前 R2 全部可计 | 以 [SUMMARY.md](./SUMMARY.md) §16 为准 |
| 边界 / 相关工作（6） | `execution-nl-req-bt-sm`、`semi-auto-efsm-standard-docs`、`nl-standard-docs-state-machines`、`most-states-modes`、`web-tool-goal-statechart-derivation`、`requirements-analysis-prototyping-scenarios-statecharts` | 可做方法证据或边界证据，但不作为主 seed | 以 [SUMMARY.md](./SUMMARY.md) §16 为准 |
| 仅元数据（1） | `executable-use-cases-domain-machine-specifications` | 目前只补到 BibTeX，PDF 仍待人工下载 | 见 [manual_download_queue.bib](./manual_download_queue.bib) |


## 1.6 核心文献 + 资源结论表

本表用于快速回答“这个 seed 的 NL 到底是什么、STM 到底是什么、能否直接给 R2 用”。它不是逐条资源明细事实源；资源可用性、pair 统计和 blocker 以 [REGISTRY.md](./REGISTRY.md) 为准。时间特性只按当前全文 / 制品证据判断：`未见显式时钟` 表示未发现 timed automata clock、连续时间或 hybrid dynamics；不代表原系统现实中没有时间约束。资源获取方式只记录论文正文 / 脚注 / Data Availability、作者官方制品页、出版商页、数据集页或论文明确指向的作者仓库等一手入口；当前 repo 已缓存的 parquet、代码、PDF、ZIP、hash 或 agent 复现副本只作本地审计证据，不计入资源可获取性。

| ID | 文献结论 | R2用途 | NL输入是什么 | STM输出是什么 | STM关键特性 | STM谱系 | 时间特性等级 | 生成方式 | 资源获取方式 |
|---|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 严格种子 | 强主候选；需冻结 | 非结构化 reactive-system 系统描述 / 行为需求 | UML state machine | 显式 state / transition / guard / action；评估层次、并发、history 等元素 | UML statechart / HSM-capable | T0-结构化离散；未见显式时钟 / 连续动力学 | LLM 单轮、结构驱动、事件驱动、混合策略 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip)；许可 / 哈希待冻结 |
| `llms-emp-stm-subset` | 严格种子 | 强主候选；只冻结初始/指定 `STM_0` | SysML 行为模型的自然语言 requirements descriptions | SysML / PlantUML STM | State、Region、Pseudostate、Transition 等 SysML STM 子集；仅冻结初始/指定输出 | SysML state machine / UML statechart | T0-结构化离散；未见 timed / hybrid 目标模型 | LLM prompt；只取 STM 子集初始/指定输出 | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文给出的数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；流水线代码未公开 |
| `maritaca-use-case-behavior-models` | 严格种子 | 文献种子；不计当前四例 | 半结构化 textual use case descriptions | UML state machine / behavior model | use-case step 到状态/迁移的模板化行为模型；需人工特征选择 | UML state machine / 用例行为模型 | T0-离散事件；未见显式时钟 | 半自动 NLP + template / 规则 + 人工特征选择 | 论文 [IEEE DOI](https://doi.org/10.1109/DSN-W.2017.33)；论文引用作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 但当前按 403/受阻处理；论文例子可重建 |
| `automated-transition-use-cases-uml-sm` | 条件种子 / 方法证据 | 不计当前四例；后续重建冻结后再裁决 | RUCM textual use case specifications，受限自然语言用例 | UML State Machine | 从 RUCM flow / transition 信息生成 state-based testing 用状态机；附录可重建局部 pair | UML state machine / state-based testing | T0-离散事件；未见显式时钟 | RUCM + aToucan / rule-based transformation | 论文 [Springer DOI](https://doi.org/10.1007/978-3-642-21470-7_9)；论文附录/示例可重建局部 pair；未见论文一手原生 pair 包、完整代码、许可或版本哈希 |
| `designing-fsm-gpt4` | 条件种子 | 条件主候选；只取初始生成 | 模板合成的英文 DFSM / Mealy 自然语言描述 | CSV DFSM / Mealy machine | 字段为 State、Input、Output、Next_State；确定性、平坦、输入/输出驱动 | 平坦 FSM / Mealy | T0-平坦离散；未见显式时钟 / 时间变量 | GPT-4 / GPT-4o 初始生成，排除 oracle / repair 环节 | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；论文内 Listing 1.1/1.2 可重建初始 NL/CSV；论文未给一手代码/数据链接，论文外 GitHub 只作线索不计入资源列 |
| `unified-uml-multimodal-validation` | 条件种子 | 条件主候选；需许可与合成边界 | LLaMA 生成的 synthetic user-focused requirements / feature descriptions | PlantUML StateDiagram / UMLCode_StateDiagram | PlantUML 状态图文本；需抽检非状态图污染和合成数据泄漏 | UML state diagram / PlantUML statechart | T0-离散；未见显式时钟，需抽检 PlantUML 污染 | 多模型流水线：requirements -> PlantUML | 论文 [TechScience HTML](https://www.techscience.com/CMES/v146n1/65740/html)；论文 Data Availability 给 [HF datasets](https://huggingface.co/nguyenvanviet/datasets)，StateDiagram 子集 [UMLCode_StateDiagram](https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram) |
| `dependable-product-families-usecases-state-machines` | 条件种子 / 方法证据 | 文献种子；不计当前四例 | 受限格式 use cases，含 variability、exception handling、traceability matrix | product-specific state machine / EFSM | 处理 product-line variability、exception 和 traceability；需切片为具体产品 seed | EFSM / product-line state machine | T0-数据/守卫级；variability 需切片，未见显式时钟 | 半自动 NLP / 规则，含 product-family variability | 论文 [IEEE DOI](https://doi.org/10.1109/LADC.2016.28)；论文引用作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 但按受阻处理；论文例子可重建，原生代码/数据/许可未公开 |
| `statechart-use-case-validation-event-driven` | 条件种子 / 方法证据 | 文献种子；不计当前四例 | 结构化 use case 模板，含 pre/postconditions、events、main flow | 单 use-case UML Statechart 与 combined Statechart | 事件驱动；支持将多个 use-case statechart 合并用于 validation | UML Statechart / validation-oriented | T0-离散事件；未见显式时钟 | use case 文档 -> statechart -> combined statechart | 论文 [ACM DOI](https://doi.org/10.1145/2245276.2231947)；案例来源 [RealState](http://openseminar.org/se/)；论文图示可重建，完整代码/数据/许可未公开 |
| `rscharter-statechart-elements` | 条件种子 / 方法证据 | 文献种子；不计当前四例 | PuRE dataset 中 RUPP/EARS 风格 SRS / NL requirements | statechart diagram elements / state diagram，经 FOPL 中间层 | 主要抽取状态图元素并经 FOPL 桥接；完整图与 pair 需另行冻结 | statechart elements + FOPL bridge | T0-元素级待核；未冻结完整状态图时间语义 | NLP / 规则 -> FOPL -> State Diagram Generator | 论文 [SSRN](https://papers.ssrn.com/abstract=4964857)；输入来源 PuRE 数据集 [Zenodo DOI](https://doi.org/10.5281/zenodo.1414117)；RSCharter 增强 pair/code 未公开 |

详情以 [SUMMARY.md](./SUMMARY.md) §16 为准，本表只作入口速览。


## 1.7 一手资源 registry 入口

- [REGISTRY.md](./REGISTRY.md) 是逐条一手资源明细主表。
- [SUMMARY.md](./SUMMARY.md) 只保留研究结论与统计摘要；若 `REGISTRY.md` 与 `SUMMARY.md` 细节冲突，以 `REGISTRY.md` 的逐条资源明细和单条目 `seed_resource_registry.json` 为准。
- [GUIDE.md](./GUIDE.md) §3.5 规定 `assets/` 一手来源纪律、trace validator 与 `storage_mode` 分级。
- 每个重点条目的 `assets/README.md` 必须中文说明 raw / extracted 映射、Python 加载方法和审计不变量。

## 2. 收录范围

| 类别 | 收录口径 |
|---|---|
| 主 seed 方法 | `NL -> T0 FSM/HSM/EFSM/statechart` generation / derivation / extraction-from-NL / human modeling。 |
| 条件 seed 方法 | T0 边界、artifact、synthetic NL、license 或 leakage 需要 R2 再裁决，但生成关系清楚。 |
| 方法层证据 | paper-only、private-only、protocol-domain、pipeline-output-missing 等不能计四例但能解释上游 `STM_0` 来源的方法。 |
| 负例哨兵 | completion-only、protocol FSM、sequence/formal scenario、process/non-STM、co-exist-only 等防误收证据。 |

## 3. 单条目目录

每个条目目录至少应尽量包含：

```text
<slug>/
├── paper.pdf（artifact-only 可无）
├── paper_content.txt（artifact-only 可无）
├── bibtex.bib
├── seed_desc.md
└── artifacts.md
```

当前 36 个目录全部具备 `seed_desc.md` 与 `artifacts.md`；`fsm-bench-20` 是 artifact-only / pipeline fallback，缺 `paper.pdf` 与 `paper_content.txt` 属预期 caveat。

## 4. 更新纪律

- 横向事实只更新 [SUMMARY.md](./SUMMARY.md)，不得新增根层 `candidate_matrix.md`、`screening_ledger.md`、`manual_queue.md`、`crosswalk.md` 等第二事实源。
- 新增 / 修改条目必须同步更新 `SUMMARY.md` 的候选表、资产表、manual queue / negative evidence / 更新日志中相关部分。
- 涉及 PR 执行计划、review 状态、ready gate、commit / push / merge 进度的信息只写 GitHub PR / issue body/comment，不写入本目录。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-16 23:08:00 | PR-R1.8-E 补充三类文库交叉入口，明确 repair_baselines 与 nl_datasets 不能替代 seed 事实源。 |
| 2026-06-15 14:23:39 | PR-R1.8-B：补强 README 核心表，显式列出每个核心 seed 的 NL 输入对象、STM 输出对象、STM 关键特性、STM 谱系和时间特性等级。 |
| 2026-06-14 23:40:00 | PR-R1.8-B：补入 Yue 2011 的本地全文章节后，`automated-transition-use-cases-uml-sm` 升级为条件种子；`manual_download_queue.bib` 只保留 Jørgensen 2004。 |
| 2026-06-14 21:30:00 | PR-R1.8-B：同步 36 个目录口径、README 结论速览和 manual queue 外链；详情以 SUMMARY §16 为准。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 将旧 `seed_corpus/` 重构为 `corpora/seed_library/`，建立 README/GUIDE/SUMMARY 三件套，旧横向 ledger 与 raw search 归档。 |
