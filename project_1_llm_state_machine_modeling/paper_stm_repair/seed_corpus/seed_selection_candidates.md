# PR-R2 seed selection handoff

本文件是 PR-R1.6 向 PR-R2 交接的候选池。它不冻结最终四例，只把当前 bounded snapshot 下可裁决的主候选、条件主候选、fallback 与排除边界集中列出，避免 PR-R2 从 `candidate_matrix.md` 的 36 行中重新摸索。

## 1. 可交接主 / 条件主候选

| 优先级 | ID | SS | SA | 是否可计入四例候选 | 为什么可考虑 | PR-R2 必做裁决 |
|---:|---|---|---|---|---|---|
| 1 | `sefm-llm-state-machine` | `SS-A` | `SA-2` | 是 | 非结构化系统描述到 UML state machine，artifact 有代码/参考解/结果；最贴近任务。 | 冻结 1--2 个 case 的 NL、reference、generated STM、hash、license / anonymous artifact caveat。 |
| 2 | `llms-emp-stm-subset` | `SS-A` | `SA-2` | 是 | 公开数据 / 结果中可隔离 `diagram_type=stm`；自然语言需求到 SysML/PlantUML STM。 | 只取 STM subset，排除 ACT/SD；冻结 parquet row、prompt / output、license caveat。 |
| 3 | `designing-fsm-gpt4` | `SS-B` | `SA-2` | 条件是 | 初始 `NL -> DFSM/Mealy CSV` 链路清楚，代码/样例线索存在。 | 必须 initial-generation-only；剔除 oracle、repair、fault model、checking sequence，防止 GT 泄漏。 |
| 4 | `unified-uml-multimodal-validation` | `SS-B` | `SA-2` | 条件是 | HF `UMLCode_StateDiagram` 公开 999 rows，PlantUML state subset 可机器读取；生成关系清楚。 | 明确 synthetic requirements；冻结 row index / parquet hash / HF sha；抽检 PlantUML parse/render；记录 license 不清。 |

## 2. fallback 候选

| ID | 当前等级 | 为什么暂不计数 | 何时可升级 |
|---|---|---|---|
| `fsm-bench-20` | `SS-A / SA-2`（pipeline-only） | 公开包有 dataset / prompt / schema / code / MIT，但 generated FSM outputs / gold 没有冻结；`SA-2` 只指 pipeline artifact 可冻结。 | PR-R2 按 v1.0.0 tag + prompt + model digest 复跑并保存 raw/cleaned outputs、manifest、hash 后，可作为 project-rerun seed。 |
| `ttool-ai-smd-subset` | `ES-C / SA-2` | 含 `after (5, 5)`、signal、guard/action 等 timed-SMD 语义；不满足 T0 hard gate。 | PR-R3 若冻结 timing abstraction / case-level T0 isolation，可重新裁决。 |
| `fsm-gen-iec-61499` | `SS-B / SA-4` | 控制系统相关性强，但 fbAssistant、数据、状态机输出和 IEC 61499 代码未公开。 | 作者公开 artifact 或本项目另行构造 comparable seed；不能直接复用原文私有输出。 |
| `sources-*` | `pending-source` | 本项目真实控制系统描述池，不是文献 strict seed；R1.6 不构造 `STM_0`。 | R2/R3 若构造 `STM_0`，需单独记录 provenance、leakage control 和人工/低配 prompt 生成过程。 |

## 3. 不应计入四例的代表项

| ID | 原因 |
|---|---|
| `ijisrt-uml-state-diagrams-llm` | `SS-A` 但 `SA-3`，paper-only，无 raw outputs / dataset。 |
| `umple-nl-state-machine` | `SS-A` 但 `SA-3`，paper/thesis-only。 |
| `req-mermaid-statechart` | `SS-B` 但 `SA-4`，核心汽车数据私有。 |
| `from-use-cases-to-statecharts` / `beyond-scenarios-state-models` / `executable-state-machines-structured-text` | classic paper-only，可 related work / manual reconstruction，不计 automated seed。 |
| `completion-sysml-gwt` | `X_REPAIR_ONLY`，partial SysML model completion，不是 `NL -> STM_0`。 |
| `generating-statechart-designs-from-scenarios` / `synthesis-revisited-scenario-based` | scenario / LSC / sequence-style formal input，不是 NL requirements。 |
| protocol / standard sentinel | protocol FSM 或 standard extraction risk，不满足控制系统 T0 seed 主线。 |

## 4. PR-R2 最小动作建议

1. 先冻结 `sefm-llm-state-machine` 与 `llms-emp-stm-subset` 两个强候选。
2. 对 `designing-fsm-gpt4` 与 `unified-uml-multimodal-validation` 分别做 leakage / synthetic / license 裁决；若通过，则四例候选数满足。
3. 若任一条件候选失败，启动 `fsm-bench-20` 小规模复跑冻结，或转入 `sources/` 构造 fallback。
4. 所有正式四例都必须落到同一 case-level manifest：`seed_id`、NL 输入、原始 STM / output、转换后 STM、证据 URL、本地 hash、license、排除信息、eligibility。
