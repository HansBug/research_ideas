# baseline candidate matrix：R1 候选资产矩阵

## 1. 字段口径

- `R2预演`：是否适合作为四例预演候选。
- `主实验`：是否可能进入主实验样本或对照。
- `对照资格`：`runnable` / `near-approximate` / `evidence-only` / `related-work-only` / `skip`。
- `对照角色`：seed、NL-regeneration、no-structured-feedback、repair-refinement、conversion-aware、related-work 等。
- `strict seed`：比五绿 direct baseline 更窄；必须满足 [strict_seed_literature_survey.md](./strict_seed_literature_survey.md) 的 `P1_NL_INPUT / P2_T0_STM_FAMILY / P3_GENERATION_RELATION / P4_EVIDENCE_POINTER` 四谓词。
- `本地事实源`：本表优先引用当前 `baselines/` 下的四件套、`ASSETS.md` 和 `DESC.md`；外部 URL 的可用性沿用这些文件中已经记录的核验结论，R1 本轮不重新联网复跑。

## 2. 五绿 direct baseline 候选级证据闭合

### 2.1 元数据、材料状态与可获取性

| slug | 论文 / 年份 / venue | 本地事实源 | 材料状态 | 代码 / artifact / access 风险 |
|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | *Designing FSMs Specifications from Requirements with GPT 4.0*；2026；arXiv | [ASSETS](../../baselines/designing-fsm-specifications-from-requirements-gpt4/ASSETS.md) / [DESC](../../baselines/designing-fsm-specifications-from-requirements-gpt4/DESC.md) / [bibtex](../../baselines/designing-fsm-specifications-from-requirements-gpt4/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在。 | 本地 ASSETS 记录 [nl2fsm](https://github.com/Paul3246/nl2fsm) 可作为起点；无 release、license、依赖锁，数据为合成 DFSM，可能需要 OpenAI API，正式使用前需审计仓库配置与 `.env` 风险。 |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | *Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models*；2026；arXiv | [ASSETS](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/ASSETS.md) / [DESC](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) / [bibtex](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在。 | 本地 ASSETS 记录 4open artifact、ZIP、F1 workbook、8 个 reference solutions 可用；匿名 artifact 无 DOI / release / license，正式实验前必须冻结本地副本、文件清单和 hash。 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | *An Agentic Flow for Finite State Machine Extraction using Prompt Chaining*；2025；arXiv | [ASSETS](../../baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/ASSETS.md) / [DESC](../../baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/DESC.md) / [bibtex](../../baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在。 | 本地 ASSETS 记录 GitHub 入口目前是仓库壳，源码、rulebook、ground truth 和逐转移结果未公开；RTSP 版本未锁，不能写成可复跑 baseline。 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | *Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles*；2025；arXiv | [ASSETS](../../baselines/automated-extraction-protocol-state-machines-3gpp-specifications/ASSETS.md) / [DESC](../../baselines/automated-extraction-protocol-state-machines-3gpp-specifications/DESC.md) / [bibtex](../../baselines/automated-extraction-protocol-state-machines-3gpp-specifications/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在。 | 公开输入规格可定位，但 SpecGPT 源码、GT、逐转移结果未公开；3GPP dynareport 是活入口，正式引用需锁定 release / 版本。 |
| `req` | *Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering*；2025；Master’s thesis | [ASSETS](../../baselines/req/ASSETS.md) / [DESC](../../baselines/req/DESC.md) / [bibtex](../../baselines/req/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在。 | 论文公开，但 Volvo / Car Weaver 原始需求、人工 statecharts、代码和专家评分原表未公开；工业私有数据无稳定申请入口。 |
| `umple` | *Exploring How Well Llama3 can Generate State Machines Represented in Umple*；2025；Master’s thesis | [ASSETS](../../baselines/umple/ASSETS.md) / [DESC](../../baselines/umple/DESC.md) / [bibtex](../../baselines/umple/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在；另有本地 toolchain reproduction 线索。 | Umple 工具链公开，但论文 benchmark bundle、RAG 语料、生成输出和 pipeline 未公开；本地 reproduction 只能证明工具链可装，不等于论文 artifact 可复跑。 |
| `llms_emp` | *Generating SysML Behavior Models via Large Language Models: an Empirical Study*；2025；Internetware 2025 | [ASSETS](../../baselines/llms_emp/ASSETS.md) / [DESC](../../baselines/llms_emp/DESC.md) / [bibtex](../../baselines/llms_emp/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在；本地已有 parquet 冻结。 | 公开数据和结果强，生成 / 修复 pipeline 未公开；Drive 可能漂移，license 待核验；必须区分 STM、ACT、SD，不能把三类行为模型混作同一 STM 样本。 |
| `pushing-the-generative-envelope-mbse-artifacts` | *Pushing the (Generative) Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts*；2025；RANLP | [ASSETS](../../baselines/pushing-the-generative-envelope-mbse-artifacts/ASSETS.md) / [DESC](../../baselines/pushing-the-generative-envelope-mbse-artifacts/DESC.md) / [bibtex](../../baselines/pushing-the-generative-envelope-mbse-artifacts/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在。 | 只有论文和正文表格；未发现公开代码、supplement、数据包或生成输出包；样本只有 air purifier / vacuum 两个题项。 |
| `ttool-ai` | *System Architects Are not Alone Anymore: Automatic System Modeling with AI*；2024；MODELSWARD | [ASSETS](../../baselines/ttool-ai/ASSETS.md) / [DESC](../../baselines/ttool-ai/DESC.md) / [bibtex](../../baselines/ttool-ai/bibtex.bib) | `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md` 已存在。 | 本地 ASSETS 记录 `zebradile/ttool-ai` artifact repo、规范、XML 与 `results.ods`；但 repo 不是完整 TTool 源码，复跑依赖 TTool、OpenAI key 和 provider drift，license 仍需正式实验前核验。 |

### 2.2 输入、输出、转换风险与实验角色

| slug | 输入材料 | 输出产物 | 转换风险 | R2预演 | 主实验 | 对照资格 | 对照角色 |
|---|---|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | 合成英文 DFSM / Mealy 需求描述。 | CSV DFSM / Mealy machine；含 oracle 比较和修复结果。 | 中：CSV 可转迁移表，但缺少真实控制系统语义、层次结构、时间约束；需定义 output / action 映射。 | yes | possible | near-approximate | repair-refinement / conversion-aware |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | 8 个非结构化 reactive-system descriptions。 | UML state machine；reference `.txt/.png`；F1 workbook；部分策略输出 Umple / HTML tables。 | 中：任务最贴近，但需从文本、图片、Umple 或表格抽取统一 STM；license 与长期可获取性待 R2/R3 核验。 | yes | possible | near-approximate | seed / NL-regeneration / conversion-aware |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | RFC 协议文档，FTP / RTSP。 | protocol FSM / command rulebook。 | 高：无可下载输出与 GT；协议 FSM 与控制系统 STM 外部效度差异大。 | no | unlikely | evidence-only | related-work |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | 3GPP NAS / NGAP / PFCP Release 17 规格。 | protocol FSM，含状态、条件、动作、转移。 | 高：需重建文档切分、prompt、ensemble 与 GT；不适合作当前可复跑主对照。 | no | unlikely | evidence-only | related-work |
| `req` | Volvo Cars / Car Weaver 产品功能需求；另有合成扩充数据描述。 | Mermaid.js statechart。 | 高：无原始工业数据；Mermaid 到内部 STM 需另做语义映射，只能作为任务边界和 related-work 证据。 | no | no | related-work-only | related-work |
| `umple` | 5 个 Umple 示例系统的自然语言需求，需人工重建论文 bundle。 | Umple state machine code。 | 中：Umple 可解析 / 编译，但样本和 RAG 语料缺失；适合作转换压力，不宜声称复现原实验。 | possible | possible | near-approximate | seed / conversion-aware |
| `llms_emp` | 107 个 SysML 行为模型需求；本地 parquet 含样本和 human review。 | PlantUML SysML 行为模型：STM / ACT / SD。 | 中：可抽 STM 子集，但需排除 ACT/SD 干扰，并定义 PlantUML / SysML 到内部 STM 的信息保留规则。 | yes | possible | near-approximate | seed / no-structured-feedback / conversion-aware |
| `pushing-the-generative-envelope-mbse-artifacts` | air purifier、vacuum 两个简短系统题项。 | SysML v2 requirements list + state machine diagrams。 | 高：无可下载逐次输出，样本极小；只适合作 prompt / temperature / local LLM 敏感性背景。 | no | no | evidence-only | related-work |
| `ttool-ai` | platooning、spacebasedsystem、AutomatedBraking 等自然语言系统规范。 | SysML BDD / IBD / state machine；TTool XML；结果表。 | 中-高：需解析 TTool XML，分离结构图与状态机，并对齐 TTool 语义与内部 STM 语义。 | yes | possible | near-approximate | seed / repair-refinement / conversion-aware |


### 2.3 strict seed 资格初判

本节不替代后续 PR-R2 的 seed registry，只防止把宽口径 direct baseline 全部误写成 strict seed。`SS-A/SS-B/ES-C/NN-D` 口径见 [strict_seed_literature_survey.md](./strict_seed_literature_survey.md)。

| slug | strict 初判 | 必须保留的限制 | R2/R3 使用建议 |
|---|---|---|---|
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | `SS-A?` 待 R2 复核 | 需冻结 4open artifact、reference、license 与 hash。 | 优先作 external same-sample strict seed 候选。 |
| `llms_emp` | STM 子集 `SS-A?` 待 R2 复核 | 只取 `diagram_type=stm`；ACT/SD 不得混入 STM seed。 | 作 STM 子集 seed / judge 校准。 |
| `ttool-ai` | SMD 部分 `SS-B/ES-C` | 只取 state-machine panel；BD/IBD/UCD/properties 不算 strict seed。 | 作工具格式和 XML 转换压力。 |
| `umple` | `SS-B/ES-C` | NL->Umple 方向贴近，但 benchmark bundle / pipeline 不完整。 | 作可重建 seed 或 adapter 压力。 |
| `designing-fsm-specifications-from-requirements-gpt4` | `SS-B/ES-C` | 只能用 NL->DFSM/Mealy 初始生成链路；repair/refinement 输出不能作为主 seed。 | 作 CSV/DFSM 近似 seed 与 repair 近邻。 |
| `req` | `SS-B` | 任务贴合但原始工业数据、人工 statechart、评分私有。 | related work / task boundary，不作可复验主样本。 |
| `pushing-the-generative-envelope-mbse-artifacts` | `SS-B/ES-C` | 只有 2 个题项和论文表格，无逐次输出包。 | 方法背景 / 小样本 evidence。 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | `NN-D` | RFC -> protocol FSM，触发 `X_PROTOCOL`。 | protocol related work，不进主 strict seed。 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | `NN-D` | 3GPP -> protocol FSM，触发 `X_PROTOCOL`。 | protocol related work，不进主 strict seed。 |

## 3. 强近邻与补充资产

强近邻表只做 R1 层面的 related-work / feedback evidence / boundary 记录，不做候选级深审；除非后续 PR 重新开深审，否则不进入 PR-R2 四例预演，也不进入 PR-R6 near-approximate comparison。

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

## 5. 阶段性边界与后续回填

R1 的资产表天然会显得比后续实验设计更“薄”，因为当前只回答“有哪些可用资产、能不能成为 seed / converter pressure / limited comparison 线索”，还没有回答“真实转换后损失多少、修正 loop 是否真的改善、评价门是否足够区分好坏”。因此：

1. R1 结论只能作为候选池和风险台账，不能直接写成论文最终 claim。
2. PR-R2 冻结四例样本后，应回填每个候选为何入选 / 未入选，并更新本表的 R2 / 主实验字段。
3. PR-R3 实现转换器后，应把“可转换性评估”替换为实际 conversion fixture、信息损失和失败原因。
4. PR-R4--R6 跑出诊断、场景和端到端结果后，允许在不突破导师定调的前提下局部调整 story 链路、RQ 侧重和 comparison 角色。
