# baseline candidate matrix：R1 候选资产矩阵

## 1. 字段口径

- `R2预演`：是否适合作为四例预演候选。
- `主实验`：是否可能进入主实验样本或对照。
- `对照资格`：`runnable` / `near-approximate` / `evidence-only` / `related-work-only` / `skip`。
- `对照角色`：seed、NL-regeneration、no-structured-feedback、repair-refinement、conversion-aware、related-work 等。

## 2. 五绿 direct baseline 深审矩阵

| slug | 输出格式 | 公开 NL / 输入 | 代码 / artifact | R2预演 | 主实验 | 对照资格 | 对照角色 | 主要风险 |
|---|---|---|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | CSV DFSM / Mealy | 合成英文 DFSM 描述 | [nl2fsm](https://github.com/Paul3246/nl2fsm)，无 release/license/依赖锁 | yes | possible | near-approximate | repair-refinement / conversion-aware | 合成数据、无真实控制系统、需清理依赖与 API drift。 |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | UML state machine / reference PNG / F1 workbook | 8 个 reactive-system descriptions | [4open artifact](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) + ZIP / workbook | yes | possible | near-approximate | seed / NL-regeneration / conversion-aware | 匿名 artifact 无 DOI/release/license；需本地冻结副本。 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | protocol FSM / rulebook | RFC 文档公开，GT 未公开 | [FlowFSM](https://github.com/YoussefMaklad/FlowFSM) 当前仓库壳 | no | unlikely | evidence-only | related-work | 源码、rulebook、GT、逐转移结果未公开。 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | NAS / NGAP / PFCP protocol FSM | 3GPP 输入规格公开，GT 未公开 | 未发现公开仓库 | no | unlikely | evidence-only | related-work | 需锁 Release 17；作者 GT 未公开。 |
| `req` | Mermaid.js statechart | Volvo / Car Weaver 内部需求 | 无公开代码 / 数据 | no | no | related-work-only | related-work | 工业私有数据，不可复跑。 |
| `umple` | Umple state machine code | Umple 示例可近似重建，thesis bundle 未公开 | Umple 工具链公开，论文 pipeline 未公开 | possible | possible | near-approximate | seed / conversion-aware | benchmark bundle、RAG 语料和输出未公开；需人工映射示例。 |
| `llms_emp` | PlantUML SysML STM / ACT / SD | 公开 Drive + 本地 parquet | 结果数据强，生成 pipeline 未公开 | yes | possible | near-approximate | seed / no-structured-feedback / conversion-aware | Drive 可能漂移；需区分 STM 子集与 ACT/SD。 |
| `pushing-the-generative-envelope-mbse-artifacts` | SysML v2 state machine diagrams | 2 个小样本题项 | 无独立数据包 / 输出包 | no | no | evidence-only | related-work | 样本太少，无可下载生成结果。 |
| `ttool-ai` | SysML block/internal/state machine + TTool XML | platooning / spacebasedsystem / AutomatedBraking 等 | [zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) + `results.ods` | yes | possible | near-approximate | seed / repair-refinement / conversion-aware | 需安装 TTool；provider drift；repo 是 artifact 不是完整工具源码。 |

## 3. 强近邻与补充资产

| slug / 入口 | 输出格式 | R1 角色 | 对照资格 | 备注 |
|---|---|---|---|---|
| `pat-agent-autoformalization-model-checking` | PAT/CSP# model + assertions + verification traces | 形式化 feedback / repair 近邻 | evidence-only | 有 GitHub；输出非 STM，但对 feedback loop 叙事重要。 |
| `event-b-agent` | Event-B machines / proofs | autoformalization 近邻 | evidence-only | 可借鉴证明/反例式反馈，不作为 STM seed。 |
| `llm-aided-security-protocol-verification` | SAPIC+ / Tamarin / ProVerif / DeepSec | 协议形式模型近邻 | evidence-only | 输出非控制系统 STM。 |
| `modeling-like-peeling-an-onion` | PlantUML activity diagrams | LLM4MDE 行为建模近邻 | related-work-only | 当前四件套已补齐，但输出是 activity diagram。 |
| `chatgpt-uml-state-diagrams-to-rebeca` | Rebeca formal model | 模型转换 / verification 近邻 | evidence-only | 输入是 PlantUML state diagrams，不是 NL seed。 |
| `llm-business-process-modeling-benchmark` | POWL / BPMN / Petri net | benchmark / self-improvement 近邻 | related-work-only | 流程模型非 STM；有 GitHub 线索。 |
| `ai-driven-consistency-sysml-diagrams` | UCD/BD inconsistency reports | 一致性修复近邻 | related-work-only | 非状态机输出，可用于 repair feedback 风险讨论。 |

## 4. 初步 R2 候选建议

R2 不应直接从本表机械抽样。若只选四例预演，建议覆盖：

1. 一个真实控制系统 seed：来自 `sources/`，用弱 prompt / 旧模型 / 人工 seed 构造 `STM_0`。
2. 一个可下载 reference 的 external baseline seed：优先 `structure-and-event-driven...`。
3. 一个本地 parquet 数据 seed：优先 `llms_emp` STM 子集。
4. 一个工具 / XML / SysML seed：优先 `ttool-ai` 或 `umple`，视转换成本决定。

上述只是 R1 handoff，不是 R2 冻结结论。
