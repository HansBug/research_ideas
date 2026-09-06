> **Cold archive / deprecated historical snapshot.** 本文件已经脱离当前 R5.5+ 主线，只用于追溯 R1.5--R1.7 旧 seed_corpus 的历史证据链；不得作为当前 seed、baseline、eligibility 或主实验事实源。当前事实请回到 `paper_stm_repair/corpora/`、`paper_stm_repair/reports/` 与 `paper_stm_repair/pipeline/` 的对应入口。

## 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/seed_selection_candidates.md` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-seed-selection-candidates.md` |
| 时间前缀 / 内容冻结依据 | `d3758f2bd5a780274ff1a249b40c7184a4230242` — 2026-06-14 11:18:35 +0800 — fix(paper1-r1.7): 补齐旧baseline seed方法入账 |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| 当前事实源替代入口 | [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)、[../../../corpora/repair_baselines/SUMMARY.md](../../../corpora/repair_baselines/SUMMARY.md)、[../../../corpora/nl_datasets/SUMMARY.md](../../../corpora/nl_datasets/SUMMARY.md)、[../../../reports/SUMMARY.md](../../../reports/SUMMARY.md) |

# PR-R2 seed selection handoff

本文件**只是 PR-R2 四例样本 selection handoff**，不是 seed 方法全集。seed 方法 / 来源全集以 [candidate_matrix.md](./2026-06-14-11-18-35-candidate-matrix.md) 与 [baseline_seed_method_crosswalk.md](./2026-06-14-11-18-35-baseline-seed-method-crosswalk.md) 为准；本文件只把当前 bounded snapshot v4 下可裁决的主候选、条件主候选、fallback、paper-only evidence、hard exclusion 与 manual blocker 集中列出，避免 PR-R2 从候选矩阵中重新摸索。

## 1. 可交接主 / 条件主候选

按 PR #108 §1.3 公式，只有 `SS-A/SS-B + SA-1/SA-2` 且 [candidate_matrix.md](./2026-06-14-11-18-35-candidate-matrix.md) 中 `计数资格` 为 `yes-main` / `yes-conditional` 的条目，才进入当前主 / 条件主候选；`SA-3/SA-4/SA-5`、pipeline-only/output-missing、project-constructed/source fallback 均不计数。注意：不计数只表示不能作为当前四例样本，并不表示不属于 seed 方法集合。

| 优先级 | ID | SS | SA | 是否可计入四例候选 | 为什么可考虑 | PR-R2 必做裁决 |
|---:|---|---|---|---|---|---|
| 1 | `sefm-llm-state-machine` | `SS-A` | `SA-2` | 是 | 非结构化系统描述到 UML state machine，artifact 有代码/参考解/结果；最贴近任务。 | 冻结 1--2 个 case 的 NL、reference、generated STM、hash、license / anonymous artifact caveat。 |
| 2 | `llms-emp-stm-subset` | `SS-A` | `SA-2` | 是 | 公开数据 / 结果中可隔离 `diagram_type=stm`；自然语言需求到 SysML/PlantUML STM。 | 只取 STM subset，排除 ACT/SD；冻结 parquet row、prompt / output、license caveat。 |
| 3 | `designing-fsm-gpt4` | `SS-B` | `SA-2` | 条件是 | 初始 `NL -> DFSM/Mealy CSV` 链路清楚，代码/样例线索存在。 | 必须 initial-generation-only；剔除 oracle、repair、fault model、checking sequence，防止 GT 泄漏。 |
| 4 | `unified-uml-multimodal-validation` | `SS-B` | `SA-2` | 条件是 | HF `UMLCode_StateDiagram` 公开 999 rows，PlantUML state subset 可机器读取；生成关系清楚。 | 明确 synthetic requirements；冻结 row index / parquet hash / HF sha；抽检 PlantUML parse/render；记录 license 不清。 |

## 2. R1.7 可计数不足的 negative evidence

R1.7 新增/重判 11 条正式候选，并新增 9 个单篇目录；同时补齐旧九个 direct baseline 方法层 crosswalk。但新增 strict-like 文献均为 paper-only / manual / boundary，**没有新增 `计数资格=yes-main/yes-conditional` 主 / 条件主候选**。

| 证据类别 | R1.7 发现 | 对 PR-R2 的含义 |
|---|---|---|
| classic / LLM paper-only strict/conditional evidence | `nlp-req-formalization-testcase-generation`、`statistical-usage-testing-uml`、`unified-use-case-statecharts`、`statechart-codesign-usecases`、`object-models-uml-embedded`、`pushing-generative-envelope-mbse` | 可作 related work / manual reconstruction / prompt-temperature seed 方法证据，但 `SA-3` 不计四例。 |
| manual / paywall strong title | `MARITACA`、`Automated Transition`、`Dependable Product-Families`、`Rscharter` | 值得人工下载，但未发现公开 artifact；不应等待其闭合后再启动 R2。 |
| boundary / protocol-domain sentinel | `protocol-flowfsm-sentinel`、`3gpp-protocol-sentinel`、`towards-automatic-model-completion`、`integrating-graphical-nl-specifications`、`specification-based-verification-usecase-sm`、`ucgen-usecase-descriptions`、`web-tool-goal-statechart-derivation` | FlowFSM / SpecGPT 保留为 protocol-domain seed 方法证据但不计控制系统四例；其他条目防止把 completion、co-exist、testbench、non-STM output、goal-model input 误收。 |
| broad API search | OpenAlex/Crossref/arXiv/DBLP + Semantic Scholar blocker | 支撑 bounded negative evidence：广域 query 未发现新的公开可复验 `NL -> T0 STM` pair。 |

因此，若 PR-R2 需要 `>=4` 四例，建议优先裁决 §1 四条；若任一条件候选被拒绝，按 §4 fallback 启动。

## 3. fallback 候选

| ID | 当前等级 | 为什么暂不计数 | 何时可升级 |
|---|---|---|---|
| `fsm-bench-20` | `SS-A / SA-2`（pipeline-only；`计数资格=no-pipeline-output-missing`） | 公开包有 dataset / prompt / schema / code / MIT，但 generated FSM outputs / gold 没有冻结；`SA-2` 只指 pipeline artifact 可冻结，不代表已有 `STM_0` 可直接冻结。 | PR-R2 按 v1.0.0 tag + prompt + model digest 复跑并保存 raw/cleaned outputs、manifest、hash 后，可作为 project-rerun seed。 |
| `ttool-ai-smd-subset` | `ES-C / SA-2` | 含 `after (5, 5)`、signal、guard/action 等 timed-SMD 语义；不满足 T0 hard gate。 | PR-R3 若冻结 timing abstraction / case-level T0 isolation，可重新裁决。 |
| `fsm-gen-iec-61499` | `SS-B / SA-4` | 控制系统相关性强，但 fbAssistant、数据、状态机输出和 IEC 61499 代码未公开。 | 作者公开 artifact 或本项目另行构造 comparable seed；不能直接复用原文私有输出。 |
| `sources-*` | `pending-source` | 本项目真实控制系统描述池，不是文献 strict seed；R1.7 不构造 `STM_0`。 | R2/R3 若构造 `STM_0`，需单独记录 provenance、leakage control 和人工/低配 prompt 生成过程。 |
| `pushing-generative-envelope-mbse` | `SS-B / SA-3` | 两个自然语言 MBSE 题项能说明上游 prompt/temperature 生成方法，但没有公开 raw outputs / code / package。 | 仅作为 paper-only seed 方法证据，不计 PR-R2 四例。 |
| `protocol-flowfsm-sentinel` / `3gpp-protocol-sentinel` | `NN-D / SA-3~5` | 保留为 protocol-domain seed 方法证据，但触发 `X_PROTOCOL`，不默认进入控制系统四例。 | 不计 PR-R2 四例；如后续要做协议域子线，可单独再裁决。 |

## 4. 不应计入四例的代表项

| ID | 原因 |
|---|---|
| `nlp-req-formalization-testcase-generation` | `SS-B / SA-3`，IRDL/sequence intermediate + paper-only，无 public output。 |
| `statistical-usage-testing-uml` | `SS-B / SA-3`，依赖 structured refinement/domain class model，paper-only。 |
| `unified-use-case-statecharts` / `statechart-codesign-usecases` / `object-models-uml-embedded` | use-case -> statechart 证据有价值，但人工/方法论 + paper-only。 |
| `ijisrt-uml-state-diagrams-llm` | `SS-A` 但 `SA-3`，paper-only，无 raw outputs / dataset。 |
| `umple-nl-state-machine` | `SS-A` 但 `SA-3`，paper/thesis-only。 |
| `req-mermaid-statechart` | `SS-B` 但 `SA-4`，核心汽车数据私有。 |
| `pushing-generative-envelope-mbse` | `SS-B / SA-3`，paper-only seed 方法证据，不能提供作者原装 `<NL, STM>` 输出包。 |
| `from-use-cases-to-statecharts` / `beyond-scenarios-state-models` / `executable-state-machines-structured-text` | classic paper-only，可 related work / manual reconstruction，不计 automated seed。 |
| `towards-automatic-model-completion` / `completion-sysml-gwt` | `X_REPAIR_ONLY`，partial SysML model completion，不是 `NL -> STM_0`。 |
| `integrating-graphical-nl-specifications` / `specification-based-verification-usecase-sm` | statechart/verification state machine 不是 NL 生成的目标 STM。 |
| `protocol-flowfsm-sentinel` / `3gpp-protocol-sentinel` | protocol-domain seed 方法证据，不计控制系统四例；不能从 seed 方法集合中删除。 |

## 5. PR-R2 最小动作建议

1. 先冻结 `sefm-llm-state-machine` 与 `llms-emp-stm-subset` 两个强候选。
2. 对 `designing-fsm-gpt4` 与 `unified-uml-multimodal-validation` 分别做 leakage / synthetic / license 裁决；若通过，则四例候选数满足。
3. 若任一条件候选失败，启动 `fsm-bench-20` 小规模复跑冻结，或转入 `sources/` / 低配 prompt / 学生人工构造 fallback。
4. 所有正式四例都必须落到同一 case-level manifest：`seed_id`、NL 输入、原始 STM / output、转换后 STM、证据 URL、本地 hash、license、排除信息、eligibility。
5. R1.7 paper-only / private / protocol-domain 文献可作为 related work、方法层证据与手工重建灵感，但不应作为主实验可复验 seed；PR-R2 需要在 case-level manifest 中记录“为什么不选”。
