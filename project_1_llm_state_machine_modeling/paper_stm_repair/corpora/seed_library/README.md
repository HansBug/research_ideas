# seed_library — 上游 `NL -> STM_0` seed 方法 / 来源文库

## 0. 定位

本目录是第一篇论文 `paper_stm_repair` 的 seed library，服务于 `<NL, STM_0> -> STM_k / Better STM` 任务。它记录能说明 `STM_0` 从自然语言需求、用例、场景、系统描述或文本规格生成 / 派生 / 人工构造而来的上游方法与来源。

**核心边界**：seed library 不是本论文的 repair baseline，也不是四个代表性样例集合本身。旧 `NL -> STM` generation baseline 在这里作为上游 seed 方法集合、转换压力、相关工作和种子候选来源入账；本论文主贡献仍是后续的无人化反馈驱动修正循环。

三类文库交叉入口：[../repair_baselines/](../repair_baselines/) 记录 `STM_0 -> STM_k / Better STM` 的 repair / feedback 近邻；[../nl_datasets/](../nl_datasets/) 记录只有 NL、尚未闭合 `STM_0` 生成关系的数据源。若同一对象跨库出现，必须在各自 `SUMMARY.md` 中按 seed / repair / NL 角色切片并互链。

## 1. 阅读顺序

1. 先读本 [README.md](./README.md) 理解文库边界。
2. 再读 [GUIDE.md](./GUIDE.md) 理解收录、分级、更新和验收规则。
3. 重点读 [SUMMARY.md](./SUMMARY.md)：这是研究结论与统计摘要入口。
4. 需要逐条资源明细时读 [REGISTRY.md](./REGISTRY.md)：它是一手 `NL + generated STM_0` 资源明细主表，包含每个 seed 的一手入口、NL 数量、pair 统计、caveat、assets 链接和使用建议。
5. 需要查看 smoke 用代表性静态样例时读上级 [selected_seed_examples/README.md](../../selected_seed_examples/README.md)；它不属于本 seed registry 文库内部事实总账。
6. 进入单条目目录时，默认读取 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> seed_desc.md -> artifacts.md`；artifact-only 条目按 `seed_desc.md -> artifacts.md -> 原始 metadata / package` 顺序。
7. 需要早期 ledger / raw search 时，进入 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)；archive 只作审计，不是当前事实真源。

## 1.5 结论速览

从一手 registry 起，本 README 只给入口级速览；**逐条一手资源事实以 [REGISTRY.md](./REGISTRY.md) 为准**。早期文献层“严格种子 / 条件种子”只表示文献层 `NL -> STM_0` 方法关系，不能等同于当前可直接入池的一手 `NL + generated STM_0` pair。

当前一手 registry 结论：**🟢 final_pool_ready = 3；🟡 conditional_final_pool = 1；🟠 pipeline_only = 2；⚪ paper_reconstructable = 10；🔴 related_only = 0**。本轮不再把公开学术资源的许可 / 再分发写作升绿 blocker；后续论文规范引用原作即可。🟢 只表示一手 `NL + generated STM_0` 可回溯复验，不表示没有 synthetic、非控制系统、样本少或泄漏隔离等学术 caveat。

| 一手 registry 角色 | 代表条目 | 一句话判断 | 详情 |
|---|---|---|---|
| 🟢 `final_pool_ready` | `llms-emp-stm-subset`、`sefm-llm-state-machine`、`unified-uml-multimodal-validation` | 一手 raw 已 committed，`NL + generated STM_0` 可由 validator 回溯；仍需按备注保留 synthetic / 非控制系统 / 单例 / 泄漏隔离 caveat | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |
| 🟡 `conditional_final_pool` | `ttool-ai-smd-subset` | 一手 `NL + generated TTool XML` 已可回溯，但仍需 SMD/T0 切片、时间/信号/guard/action 规范化与 incoherency 泄漏隔离；不计现成 final pool | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |
| 🟠 `pipeline_only` | `fsm-bench-20`、`designing-fsm-gpt4` | 有 NL / prompt / schema / code，但作者未公开可回溯 `<NL, generated STM_0>` pair；若源码含未配对 run artifacts，也只作审计线索；属于 `NL+源码可复跑`，复跑输出必须另建 run record | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |
| ⚪ `paper_reconstructable` | 多数传统 use-case / statechart 工作 | 只有论文图示、附录或示例可重建，不计现成 seed | 以 [REGISTRY.md](./REGISTRY.md) §2 与 §4 为准 |
| 🔴 `related_only` | 暂无 | 当前主表无 related-only 登记条目；不满足条件者仍可在未登记表或相关文献中保留 | 以 [REGISTRY.md](./REGISTRY.md) §2 为准 |


## 1.6 核心文献 + 资源结论表

本表用于快速回答“这个 seed 的 NL 到底是什么、STM 到底是什么、一手 registry 一手资源角色是什么”。它不是逐条资源明细事实源；资源可用性、NL 数、pair 统计和 caveat 以 [REGISTRY.md](./REGISTRY.md) 为准。时间特性只按当前全文 / 制品证据判断：`未见显式时钟` 表示未发现 timed automata clock、连续时间或 hybrid dynamics；不代表原系统现实中没有时间约束。资源获取方式只记录论文正文 / 脚注 / Data Availability、作者官方制品页、出版商页、数据集页或可核验的作者官方仓库等一手入口；当前 repo 已缓存的 parquet、代码、PDF、ZIP、hash 或 agent 复现副本只作本地审计证据，不计入资源可获取性。

| ID | 一手角色 | 资源类别 | 源码 | 论文LLM | 复跑 | 一手 registry 资源用途 | NL输入是什么 | STM输出是什么 | STM关键特性 | STM谱系 | 时间特性等级 | 生成方式 | 一手入口 / blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `unified-uml-multimodal-validation` | 🟢 `final_pool_ready` | NL+STM一手 | 🔴未公开 | 🟢开权重可用 | ⚪不适用 | 可直接复验；HF parquet 999 行全量 trace verified，其中 989 行有效 PlantUML 可计，10 行生成失败已排除；989 个 eligible NL 均唯一，适合作 synthetic stress | LLaMA-3.2-1B-Instruct 生成的 synthetic user-focused feature descriptions | PlantUML StateDiagram / UMLCode_StateDiagram | PlantUML 状态图文本；需抽检非状态图污染和合成数据泄漏 | UML state diagram / PlantUML statechart | T0-离散；未见显式时钟，需抽检 PlantUML 污染 | 多模型流水线：requirements -> PlantUML | 论文 [TechScience HTML](https://www.techscience.com/CMES/v146n1/65740/html)；论文 Data Availability 给 [HF datasets](https://huggingface.co/nguyenvanviet/datasets)，StateDiagram 子集 [UMLCode_StateDiagram](https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram)；本地一手资源见 [assets/README.md](./unified-uml-multimodal-validation/assets/README.md)；caveat: synthetic / non-control-domain quality audit；不是控制系统真实需求 |
| `llms-emp-stm-subset` | 🟢 `final_pool_ready` | NL+STM一手 | 🔴未公开 | 🟡混合 | ⚪不适用 | 强相关一手入口；Google Drive workbook 已下载并 trace verified 60 条 generated PlantUML；10 个唯一 NL × 6 个 LLM 输出，需保持 reference/checking 列隔离 | SysML 行为模型的自然语言 requirements descriptions | SysML / PlantUML STM | State、Region、Pseudostate、Transition 等 SysML STM 子集；只取初始 `Generation PlantUML`，排除 reference 与 checking outputs | SysML state machine / UML statechart | R5.5 复核为 mixed：8 个 T0、Microwave 为 T0.5 timer-like caveat、Digital Camera 为 T1 supplementary stress | LLM prompt；6 个 LLM 各 10 条 generated PlantUML | 论文 [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)；论文给出的数据 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；本地一手资源见 [assets/README.md](./llms-emp-stm-subset/assets/README.md)；caveat: reference / checking columns 必须隔离；reference 按 canonical case 为 10，exact unique reference PlantUML 文本为 11（1 个需求存在 reference 文本变体） |
| `sefm-llm-state-machine` | 🟢 `final_pool_ready` | NL+STM一手 | 🟢固定源码 | 🟡混合 | ⚪不适用 | 强相关一手入口；已 committed 4open ZIP 并 trace verified 1 组 SSC7 generated pair；ZIP 另含 8 个无 generated 输出的 NL（7 个 reference-only + 1 个 ATAS 纯 NL-only）与 8 个 reference solutions | 非结构化 reactive-system 系统描述 / 行为需求（SSC7 自助结账系统描述） | UML state machine / Umple 输出（Claude Sonnet 3.5 single-prompt generated `SSC7_single_prompt_*.txt`） | 显式 state / transition / guard / action；含 Ready、WeighingItem、SecurityCheck、Payment、Override、Timeout 等状态；评估层次、并发、history 等元素 | UML statechart / HSM-capable / Umple | T0-结构化离散；generated 输出含 `after(60)` 类 Umple timer-like transition，后续转换需标注但不是 timed automata / hybrid model | LLM 单轮、结构驱动、事件驱动、混合策略；当前 extracted pair 只取 Claude Sonnet 3.5 single prompt 原始输出 | 论文 [arXiv](https://arxiv.org/abs/2604.00275)；作者制品 [4open](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip)；本地一手资源见 [assets/README.md](./sefm-llm-state-machine/assets/README.md)；caveat: 当前只有 SSC7 有 generated text output，其他 8 个无 generated 输出的 NL 中 7 个是 reference-only、1 个 ATAS 是纯 NL-only |
| `ttool-ai-smd-subset` | 🟡 `conditional_final_pool` | NL+STM一手 | 🟠片段/部分 | 🟡混合 | ⚪未尝试 | 条件候选 / 转换器压力；6 组 `NL + generated TTool XML` 已 trace verified，但不计现成 final pool | 作者 GitHub 工件中的系统规格（4 个唯一 NL / 6 条 raw，其中主案例与 `incoherencies/` 变体分开） | TTool/SysML/AVATAR XML 工件，需后续切出 state-machine diagram / T0 子集 | 完整 TTool XML，可能含 BD/UCD、attributes、signals、guards/actions、`after` 时间语义与 incoherency correction 上下文 | SysML/TTool state-machine diagram subset / XML | T1-含时间/信号语义线索；需转换器明确降级或保留 | TTool + ChatGPT 3.5 生成；公开仓库不是完整 TTool-AI 源码 | 论文 [HAL](https://telecom-paris.hal.science/hal-04483279) / [DOI](https://doi.org/10.5220/0012320100003645)；作者仓库 [zebradile/ttool-ai](https://github.com/zebradile/ttool-ai)；本地一手资源见 [assets/README.md](./ttool-ai-smd-subset/assets/README.md)；caveat: 必须冻结 SMD/T0 切片与 incoherency 泄漏边界 |
| `fsm-bench-20` | 🟠 `pipeline_only` | NL+源码可复跑 | 🟢固定源码 | 🟡本地/代理可用 | 🟢单系统连通 | 不计现成 seed；后续可由本项目复跑构造 `STM_0` 并另建 run record | 控制系统需求 / prompt / schema | 目标 FSM JSON schema；公开包缺作者 generated `STM_0` outputs | 平坦 FSM schema、prompt、benchmark gold / systems | FSM JSON / T0 | T0-离散；未见显式时钟 | 作者 benchmark pipeline；需本项目 rerun | [Zenodo](https://doi.org/10.5281/zenodo.20517969) / GitHub release；blocker: no published generated `STM_0` |
| `maritaca-use-case-behavior-models` | ⚪ `paper_reconstructable` | 论文可重建 | ❓受阻 | ⚪不适用 | ⚪不适用 | 传统方法证据；不计现成 seed | 半结构化 textual use case descriptions | UML state machine / behavior model | use-case step 到状态/迁移的模板化行为模型；需人工特征选择 | UML state machine / 用例行为模型 | T0-离散事件；未见显式时钟 | 半自动 NLP + template / 规则 + 人工特征选择 | 论文 [IEEE DOI](https://doi.org/10.1109/DSN-W.2017.33)；作者站点 [MARITACA](http://www.students.ic.unicamp.br/~ra161251/) 当前按 403/受阻处理；blocker: no machine-readable native pair |
| `designing-fsm-gpt4` | 🟠 `pipeline_only` | NL+源码可复跑 | 🟢固定源码 | 🟠需代理/替代 | 🟢初始连通 | 只作 NL+code 复跑线索；当前不进 final pool | 模板合成的英文 DFSM / Mealy 自然语言描述 | CSV DFSM / Mealy machine | 字段为 State、Input、Output、Next_State；确定性、平坦、输入/输出驱动 | 平坦 FSM / Mealy | T0-平坦离散；未见显式时钟 / 时间变量 | GPT-4 / GPT-4o 初始生成，论文还含 oracle / repair 环节 | 论文 [arXiv](https://arxiv.org/abs/2603.29140)；作者代码 [GitHub](https://github.com/Paul3246/nl2fsm)，本地一手源码与连通性检查记录见 [assets/README.md](./designing-fsm-gpt4/assets/README.md)；blocker: no author-published traceable `<NL, STM_0>` pair；源码未配对 run artifacts 不计，复跑输出必须另建 run record |

详情以 [REGISTRY.md](./REGISTRY.md) 为准；本表只作入口速览。


## 1.7 一手资源 registry 入口

- [REGISTRY.md](./REGISTRY.md) 是逐条一手资源明细主表。
- [SUMMARY.md](./SUMMARY.md) 只保留研究结论与统计摘要；若 `REGISTRY.md` 与 `SUMMARY.md` 细节冲突，以 `REGISTRY.md` 的逐条资源明细和单条目 `seed_resource_registry.json` 为准。
- [GUIDE.md](./GUIDE.md) §3.5 规定 `assets/` 一手来源纪律、trace validator 与 `storage_mode` 分级。
- 每个重点条目的 `assets/README.md` 必须中文说明 raw / extracted 映射、Python 加载方法和审计不变量。

## 1.8 smoke 用代表性样例入口

上级 [selected_seed_examples/](../../selected_seed_examples/) 是当前固定维护的 smoke 用代表性种子样例迷你文库。它故意放在 `paper_stm_repair/` 根路径下，而不是放在本 `seed_library/` 内：本目录继续作为上游 seed 方法 / 来源事实总账，`selected_seed_examples/` 只把少量已核验的一手 `<NL, STM_0>` pair 展开成可直接读取的 `nl.txt` 与 `stm0.*` 源文件，服务后续转换器、诊断器、修正循环和评价协议的最小连通性自检。当前样例不是最终实验集合，也不是主结果样本规模上限。

| 分组 | 条目 | 作用 |
|---|---|---|
| 现成一手种子来源 | `llms-emp-stm-subset`、`sefm-llm-state-machine`、`unified-uml-multimodal-validation` | 当前可用的一手 `NL + NL-generated STM_0` 来源。 |
| 条件 XML 样例 | `ttool-ai-smd-subset` | TTool XML / SMD/T0 切片压力源；不计现成 final pool。 |
| 仅复跑线索补充 | `fsm-bench-20`、`designing-fsm-gpt4` | 后续可复跑构造 seed，但复跑前不计 author first-source pair。 |

当前 smoke 用代表性样例为 [llms-emp-deepseek-microwave](../../selected_seed_examples/llms-emp-deepseek-microwave/)、[llms-emp-gpt4o-hldcs](../../selected_seed_examples/llms-emp-gpt4o-hldcs/)、[llms-emp-kimi-autonomous-collision](../../selected_seed_examples/llms-emp-kimi-autonomous-collision/) 和 [sefm-ssc7-umple](../../selected_seed_examples/sefm-ssc7-umple/)。其中 `ttool-automatedbraking-xml` 与 `unified-uml-synthetic-0000` 已从当前四例 selected smoke 移除，只保留在 registry / evidence 中作为未来 TTool XML / SMD 切片或 synthetic probe 专项线索；当前四例均来自一手 `NL + generated STM_0` pair。

## 2. 收录范围

| 类别 | 收录口径 |
|---|---|
| 上游 seed 方法证据 | `NL -> T0 FSM/HSM/EFSM/statechart` generation / derivation / extraction-from-NL / human modeling；是否进入当前可用种子池以 [REGISTRY.md](./REGISTRY.md) `recommended_role` 为准。 |
| 条件方法证据 | T0 边界、artifact、synthetic NL、leakage 或质量审计需要进一步裁决，但生成关系清楚；默认不等于一手 eligible seed。 |
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

当前 36 个历史条目目录全部具备 `seed_desc.md` 与 `artifacts.md`；其中 16 个重点条目已补 `seed_resource_registry.json`，6 个条目已补 `assets/` 一手审计链。未建 registry 的既有目录按 [REGISTRY.md](./REGISTRY.md) §4 统一视为 `paper_reconstructable` / `related_only`，不能直接进入当前可用种子池。`fsm-bench-20` 是 artifact-only / pipeline fallback，缺 `paper.pdf` 与 `paper_content.txt` 属预期 caveat；`designing-fsm-gpt4` 与 `ttool-ai-smd-subset` 已补 `assets/`，但分别是 pipeline-only 复跑线索和 conditional XML 切片线索。

## 4. 更新纪律

- 一手资源 / pair / blocker 事实必须优先更新 [REGISTRY.md](./REGISTRY.md) 与单条目 `seed_resource_registry.json`；[SUMMARY.md](./SUMMARY.md) / [README.md](./README.md) 只保留研究摘要和入口速览，不得新增根层 `candidate_matrix.md`、`screening_ledger.md`、`manual_queue.md`、`crosswalk.md` 等第二事实源。
- 新增 / 修改条目必须同步更新 `SUMMARY.md` 的候选表、资产表、manual queue / negative evidence / 更新日志中相关部分。
- 涉及 PR 执行计划、review 状态、ready gate、commit / push / merge 进度的信息只写 GitHub PR / issue body/comment，不写入本目录。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-24 00:30:00 | 新增上级 [selected_seed_examples/README.md](../../selected_seed_examples/README.md) 入口，把四个 smoke 用代表性种子样例整理为根路径迷你文库。 |
| 2026-06-23 21:20:00 | 一手 registry：核心表与 REGISTRY 增加 `复跑` 可见列，明确 `designing-fsm-gpt4` 只完成初始生成连通性检查、`fsm-bench-20` 完成单系统连通性检查，二者仍是 pipeline-only / NL+源码可复跑而非作者一手 pair。 |
| 2026-06-23 19:45:00 | 一手 registry：核心表新增资源类别、源码与论文 LLM 可用性口径，`designing-fsm-gpt4` 调整为 NL+源码可复跑 / pipeline-only，`fsm-bench-20` 增加 OpenAI-compatible proxy 连通性记录，`ttool-ai-smd-subset` 以条件一手 `NL+TTool XML` 纳入 registry。 |
| 2026-06-22 21:30:00 | 一手 registry：补强 REGISTRY/JSON 机器字段，所有登记条目都记录 NL raw/unique/NL-only、数据构造说明与质量抽检状态；SEFM / unified / llms-emp / fsm-bench 的一手资源真实状况和 NL 计数已再次核对。 |
| 2026-06-22 19:40:00 | 一手 registry：修正 unified 不应按 3 行计数的口径，全量抽取 HF parquet 999 行并计 989 条有效 PlantUML；用 gdown 下载 llms-emp Google Drive workbook 并抽取 60 条 generated PlantUML。 |
| 2026-06-22 18:55:00 | 一手 registry：补齐 `sefm-llm-state-machine` 4open ZIP raw、1 组 SSC7 `NL + generated STM_0` trace verified pair，以及 assets README 真实示例输出；已改按公开学术资源引用原作口径处理，当前该 pair 为 `final_pool_ready`。 |
| 2026-06-22 18:30:00 | 一手 registry：初始化一手 registry 口径，明确未建 registry 目录默认不可入池，并补强 validator 的 raw locator / 文本 hash 回溯校验；后续本轮已更新为 `final_pool_ready=3`。 |
| 2026-06-16 23:08:00 | 补充三类文库交叉入口，明确 repair_baselines 与 nl_datasets 不能替代 seed 事实源。 |
| 2026-06-15 14:23:39 | 补强 README 核心表，显式列出每个核心 seed 的 NL 输入对象、STM 输出对象、STM 关键特性、STM 谱系和时间特性等级。 |
| 2026-06-14 23:40:00 | 补入 Yue 2011 的本地全文章节后，`automated-transition-use-cases-uml-sm` 升级为条件种子；`manual_download_queue.bib` 只保留 Jørgensen 2004。 |
| 2026-06-14 21:30:00 | 同步 36 个目录口径、README 结论速览和 manual queue 外链；详情以 SUMMARY §16 为准。 |
| 2026-06-14 17:55:00 | 将旧 `seed_corpus/` 重构为 `corpora/seed_library/`，建立 README/GUIDE/SUMMARY 三件套，旧横向 ledger 与 raw search 归档。 |
