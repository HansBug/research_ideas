# seed_library — 上游 `NL -> STM_0` seed 方法 / 来源文库

## 0. 定位

本目录是第一篇论文 `paper_stm_repair` 的 seed library，服务于 `<NL, STM_0> -> STM_k / Better STM` 任务。它记录能说明 `STM_0` 从自然语言需求、用例、场景、系统描述或文本规格生成 / 派生 / 人工构造而来的上游方法与来源。

**核心边界**：seed library 不是本论文的 repair baseline，也不是 R2 四例样本集合本身。旧 `NL -> STM` generation baseline 在这里作为上游 seed 方法集合、转换压力、相关工作 和 R2 候选来源入账；本论文主贡献仍是后续的无人化反馈驱动修正循环。

三类文库交叉入口：[../repair_baselines/](../repair_baselines/) 记录 `STM_0 -> STM_k / Better STM` 的 repair / feedback 近邻；[../nl_datasets/](../nl_datasets/) 记录只有 NL、尚未闭合 `STM_0` 生成关系的数据源。若同一对象跨库出现，必须在各自 `SUMMARY.md` 中按 seed / repair / NL 角色切片并互链。

## 1. 阅读顺序

1. 先读本 [README.md](./README.md) 理解文库边界。
2. 再读 [GUIDE.md](./GUIDE.md) 理解收录、分级、更新和验收规则。
3. 重点读 [SUMMARY.md](./SUMMARY.md)：这是研究结论与统计摘要入口。
4. 需要逐条资源明细时读 [REGISTRY.md](./REGISTRY.md)：它是一手 `NL + generated STM_0` 资源明细主表，包含每个 seed 的一手入口、NL 数量、pair 统计、caveat、assets 链接和 R2 选择建议。
5. 进入单条目目录时，默认读取 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> seed_desc.md -> artifacts.md`；artifact-only 条目按 `seed_desc.md -> artifacts.md -> 原始 metadata / package` 顺序。
6. 需要旧 R1.5--R1.7 ledger / raw search 时，进入 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)；archive 只作审计，不是当前事实真源。

## 1.5 结论速览

从 R2.0 起，本 README 只给入口级速览；**逐条一手资源事实以 [REGISTRY.md](./REGISTRY.md) 为准**。旧 R1.8 的“严格种子 / 条件种子”只表示文献层 `NL -> STM_0` 方法关系，不能等同于当前可直接入池的一手 `NL + generated STM_0` pair。

当前一手 registry 结论：**🟢 final_pool_ready = 3；🟡 conditional_final_pool = 0；🟠 pipeline_only = 1；⚪ paper_reconstructable = 10；🔴 related_only = 1**。本轮不再把公开学术资源的许可 / 再分发写作升绿 blocker；后续论文规范引用原作即可。🟢 只表示一手 `NL + generated STM_0` 可回溯复验，不表示没有 synthetic、非控制系统、样本少或泄漏隔离等学术 caveat。

| 一手 registry 角色 | 代表条目 | 一句话判断 | 详情 |
|---|---|---|---|
| 🟢 `final_pool_ready` | `llms-emp-stm-subset`、`sefm-llm-state-machine`、`unified-uml-multimodal-validation` | 一手 raw 已 committed，`NL + generated STM_0` 可由 validator 回溯；仍需按备注保留 synthetic / 非控制系统 / 单例 / 泄漏隔离 caveat | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |
| 🟡 `conditional_final_pool` | 暂无 | 保留给一手入口明确但缺关键 raw、locator、generated 输出、泄漏隔离或质量审计的条目 | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |
| 🟠 `pipeline_only` | `fsm-bench-20` | 有 NL / prompt / schema / code，但作者未公开 generated `STM_0` | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |
| ⚪ `paper_reconstructable` | 多数传统 use-case / statechart 工作 | 只有论文图示、附录或示例可重建，不计现成 seed | 以 [REGISTRY.md](./REGISTRY.md) §2 与 §4 为准 |
| 🔴 `related_only` | `designing-fsm-gpt4` | 当前无稳定一手 pair，不能进入 final pool | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |


## 1.6 核心文献 + 资源结论表

本表用于快速回答“这个 seed 的 NL 到底是什么、STM 到底是什么、R2.0 一手资源角色是什么”。它不是逐条资源明细事实源；资源可用性、NL 数、pair 统计和 caveat 以 [REGISTRY.md](./REGISTRY.md) 为准。时间特性只按当前全文 / 制品证据判断：`未见显式时钟` 表示未发现 timed automata clock、连续时间或 hybrid dynamics；不代表原系统现实中没有时间约束。资源获取方式只记录论文正文 / 脚注 / Data Availability、作者官方制品页、出版商页、数据集页或论文明确指向的作者仓库等一手入口；当前 repo 已缓存的 parquet、代码、PDF、ZIP、hash 或 agent 复现副本只作本地审计证据，不计入资源可获取性。

| ID | 一手角色 | R2.0 资源用途 | NL输入是什么 | STM输出是什么 | STM关键特性 | STM谱系 | 时间特性等级 | 生成方式 | 一手入口 / blocker |
|---|---|---|---|---|---|---|---|---|---|
| `unified-uml-multimodal-validation` | 🟢 `final_pool_ready` | 可直接复验；HF parquet 999 行全量 trace verified，其中 989 行有效 PlantUML 可计，10 行生成失败已排除；989 个 eligible NL 均唯一，适合作 synthetic smoke/stress | LLaMA-3.2-1B-Instruct 生成的 synthetic user-focused feature descriptions | PlantUML StateDiagram / UMLCode_StateDiagram | PlantUML 状态图文本；需抽检非状态图污染和合成数据泄漏 | UML state diagram / PlantUML statechart | T0-离散；未见显式时钟，需抽检 PlantUML 污染 | 多模型流水线：requirements -> PlantUML | 论文 [TechScience HTML](https://www.techscience.com/CMES/v146n1/65740/html)；论文 Data Availability 给 [HF datasets](https://huggingface.co/nguyenvanviet/datasets)，StateDiagram 子集 [UMLCode_StateDiagram](https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram)；本地一手资源见 [assets/README.md](./unified-uml-multimodal-validation/assets/README.md)；caveat: synthetic / non-control-domain quality audit；不是控制系统真实需求 |
| `llms-emp-stm-subset` | 🟢 `final_pool_ready` | 强相关一手入口；Google Drive workbook 已下载并 trace verified 60 条 generated PlantUML；10 个唯一 NL × 6 个 LLM 输出，需保持 reference/checking 列隔离 | SysML 行为模型的自然语言 requirements descriptions | SysML / PlantUML STM | State、Region、Pseudostate、Transition 等 SysML STM 子集；只取初始 `Generation PlantUML`，排除 reference 与 checking outputs | SysML state machine / UML statechart | T0-结构化离散；未见 timed / hybrid 目标模型 | LLM prompt；6 个 LLM 各 10 条 generated PlantUML | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文给出的数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；本地一手资源见 [assets/README.md](./llms-emp-stm-subset/assets/README.md)；caveat: reference / checking columns 必须隔离 |
| `sefm-llm-state-machine` | 🟢 `final_pool_ready` | 强相关一手入口；已 committed 4open ZIP 并 trace verified 1 组 SSC7 generated pair；ZIP 另含 8 个 NL-only descriptions 与 8 个 reference solutions | 非结构化 reactive-system 系统描述 / 行为需求（SSC7 自助结账系统描述） | UML state machine / Umple 输出（Claude Sonnet 3.5 single-prompt generated `SSC7_single_prompt_*.txt`） | 显式 state / transition / guard / action；含 Ready、WeighingItem、SecurityCheck、Payment、Override、Timeout 等状态；评估层次、并发、history 等元素 | UML statechart / HSM-capable / Umple | T0-结构化离散；generated 输出含 `after(60)` 类 Umple timer-like transition，后续转换需标注但不是 timed automata / hybrid model | LLM 单轮、结构驱动、事件驱动、混合策略；当前 extracted pair 只取 Claude Sonnet 3.5 single prompt 原始输出 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip)；本地一手资源见 [assets/README.md](./sefm-llm-state-machine/assets/README.md)；caveat: 当前只有 SSC7 有 generated text output，其他 NL 只能作 NL-only / reference 资产 |
| `fsm-bench-20` | 🟠 `pipeline_only` | 不计现成 seed；后续可由本项目复跑构造 `STM_0` 并另建 run record | 控制系统需求 / prompt / schema | 目标 FSM JSON schema；公开包缺作者 generated `STM_0` outputs | 平坦 FSM schema、prompt、benchmark gold / systems | FSM JSON / T0 | T0-离散；未见显式时钟 | 作者 benchmark pipeline；需本项目 rerun | [Zenodo](https://doi.org/10.5281/zenodo.20517969) / GitHub release；blocker: no published generated `STM_0` |
| `maritaca-use-case-behavior-models` | ⚪ `paper_reconstructable` | 传统方法证据；不计现成 seed | 半结构化 textual use case descriptions | UML state machine / behavior model | use-case step 到状态/迁移的模板化行为模型；需人工特征选择 | UML state machine / 用例行为模型 | T0-离散事件；未见显式时钟 | 半自动 NLP + template / 规则 + 人工特征选择 | 论文 [IEEE DOI](https://doi.org/10.1109/DSN-W.2017.33)；作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 当前按 403/受阻处理；blocker: no machine-readable native pair |
| `designing-fsm-gpt4` | 🔴 `related_only` | 只作 related / toy-line 证据；当前不进 final pool | 模板合成的英文 DFSM / Mealy 自然语言描述 | CSV DFSM / Mealy machine | 字段为 State、Input、Output、Next_State；确定性、平坦、输入/输出驱动 | 平坦 FSM / Mealy | T0-平坦离散；未见显式时钟 / 时间变量 | GPT-4 / GPT-4o 初始生成，论文还含 oracle / repair 环节 | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；只有 Listing 可重建线索，未给稳定一手代码/数据 release；blocker: no stable first-source pair |

详情以 [REGISTRY.md](./REGISTRY.md) 为准；本表只作入口速览。


## 1.7 一手资源 registry 入口

- [REGISTRY.md](./REGISTRY.md) 是逐条一手资源明细主表。
- [SUMMARY.md](./SUMMARY.md) 只保留研究结论与统计摘要；若 `REGISTRY.md` 与 `SUMMARY.md` 细节冲突，以 `REGISTRY.md` 的逐条资源明细和单条目 `seed_resource_registry.json` 为准。
- [GUIDE.md](./GUIDE.md) §3.5 规定 `assets/` 一手来源纪律、trace validator 与 `storage_mode` 分级。
- 每个重点条目的 `assets/README.md` 必须中文说明 raw / extracted 映射、Python 加载方法和审计不变量。

## 2. 收录范围

| 类别 | 收录口径 |
|---|---|
| 上游 seed 方法证据 | `NL -> T0 FSM/HSM/EFSM/statechart` generation / derivation / extraction-from-NL / human modeling；是否进入 R2 以 [REGISTRY.md](./REGISTRY.md) `recommended_role` 为准。 |
| 条件方法证据 | T0 边界、artifact、synthetic NL、leakage 或质量审计需要 R2 再裁决，但生成关系清楚；默认不等于一手 eligible seed。 |
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

当前 36 个历史条目目录全部具备 `seed_desc.md` 与 `artifacts.md`；其中 15 个重点条目已补 `seed_resource_registry.json`，4 个条目已补 `assets/` 一手审计链。未建 registry 的既有目录按 [REGISTRY.md](./REGISTRY.md) §4 统一视为 `paper_reconstructable` / `related_only`，不能直接进入 R2。`fsm-bench-20` 是 artifact-only / pipeline fallback，缺 `paper.pdf` 与 `paper_content.txt` 属预期 caveat。

## 4. 更新纪律

- 一手资源 / pair / blocker 事实必须优先更新 [REGISTRY.md](./REGISTRY.md) 与单条目 `seed_resource_registry.json`；[SUMMARY.md](./SUMMARY.md) / [README.md](./README.md) 只保留研究摘要和入口速览，不得新增根层 `candidate_matrix.md`、`screening_ledger.md`、`manual_queue.md`、`crosswalk.md` 等第二事实源。
- 新增 / 修改条目必须同步更新 `SUMMARY.md` 的候选表、资产表、manual queue / negative evidence / 更新日志中相关部分。
- 涉及 PR 执行计划、review 状态、ready gate、commit / push / merge 进度的信息只写 GitHub PR / issue body/comment，不写入本目录。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-22 19:40:00 | PR-R2.0：修正 unified 不应按 3 行计数的口径，全量抽取 HF parquet 999 行并计 989 条有效 PlantUML；用 gdown 下载 llms-emp Google Drive workbook 并抽取 60 条 generated PlantUML。 |
| 2026-06-22 18:55:00 | PR-R2.0：补齐 `sefm-llm-state-machine` 4open ZIP raw、1 组 SSC7 `NL + generated STM_0` trace verified pair，以及 assets README 真实示例输出；已改按公开学术资源引用原作口径处理，当前该 pair 为 `final_pool_ready`。 |
| 2026-06-22 18:30:00 | PR-R2.0：初始化一手 registry 口径，明确未建 registry 目录默认不可入池，并补强 validator 的 raw locator / 文本 hash 回溯校验；后续本轮已更新为 `final_pool_ready=3`。 |
| 2026-06-16 23:08:00 | PR-R1.8-E 补充三类文库交叉入口，明确 repair_baselines 与 nl_datasets 不能替代 seed 事实源。 |
| 2026-06-15 14:23:39 | PR-R1.8-B：补强 README 核心表，显式列出每个核心 seed 的 NL 输入对象、STM 输出对象、STM 关键特性、STM 谱系和时间特性等级。 |
| 2026-06-14 23:40:00 | PR-R1.8-B：补入 Yue 2011 的本地全文章节后，`automated-transition-use-cases-uml-sm` 升级为条件种子；`manual_download_queue.bib` 只保留 Jørgensen 2004。 |
| 2026-06-14 21:30:00 | PR-R1.8-B：同步 36 个目录口径、README 结论速览和 manual queue 外链；详情以 SUMMARY §16 为准。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 将旧 `seed_corpus/` 重构为 `corpora/seed_library/`，建立 README/GUIDE/SUMMARY 三件套，旧横向 ledger 与 raw search 归档。 |
