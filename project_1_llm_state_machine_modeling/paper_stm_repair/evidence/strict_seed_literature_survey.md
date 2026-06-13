# strict seed literature survey：大规模 seed 文献调研口径与执行方案

## 1. 目的与边界

本文件补充 PR-R1 的新增口径：第一篇论文的 seed 资产盘点不能只局限于历史九个 direct baseline，也不能把所有 `<NL, STM>` 共现材料都视为可用 seed。后续 PR-R2 需要在更大文献空间中寻找可作为 `<NL, STM_0>` 输入的 seed，因此 R1 先冻结 **strict seed** 的定义、排除规则、多维编码指标、分级标准和调研执行方案。

本文件只建立调研合同和初始事实台账，不声称 strict seed 文献版图已经穷尽，不冻结四例样本，不实现转换器，也不证明 repair loop 有效。最终进入主实验的 seed 必须等待 PR-R2 样本登记、PR-R3 转换器合同和 PR-R6 评价协议闭合。

## 2. strict seed 的硬定义

一篇论文、artifact 或样本只有同时满足以下四个谓词，才可标为 strict seed：

| 谓词 | 必要条件 | 不满足时的处理 |
|---|---|---|
| `P1_NL_INPUT` | 输入主源是自然语言需求、用例、场景、系统描述、文本规格或等价非形式化文本。 | 形式规格、源码、已有图模型或纯表格输入不得标 strict。 |
| `P2_T0_STM_FAMILY` | 输出目标属于 `T0（无关键时间语义）` 的 `FSM / HSM / EFSM / statechart` 家族，可包含 UML/SysML/PlantUML/Mermaid/Umple 的状态机方言。 | `T1+`、Hybrid、Protocol、Resource-flow、BPMN、Petri、CSP、Event-B、TLA+、LTL/STL 等不得标 strict。 |
| `P3_GENERATION_RELATION` | STM 必须在 generation / synthesis / derivation 环节由 `P1` 所定义的非形式化 `NL` 生成或派生；若使用 extraction，抽取源也必须是自然语言需求 / 场景 / 描述而非 protocol spec、形式规格或已有图模型。方法可以是 LLM、规则、传统 NLP、受控模板 / 中间结构归一或人工，但必须存在可追踪的 `NL -> STM` 关系；图模型 / 形式模型之间的转换不能单独满足本谓词。 | 只有 NL 与 STM 同时存在、已有 STM repair/refinement、protocol / formal-spec extraction、或 diagram/formal-model conversion 不得标 strict。 |
| `P4_EVIDENCE_POINTER` | 至少有论文段落、本地 `DESC/ASSETS/STM`、artifact、结果文件或可追踪 URL 证明输入、输出和生成关系。 | 证据不足只能标 candidate / pending，不计入 strict 数量。 |

> 术语说明：这里的 `T0` 指 [sources/STM_GUIDE.md](../../sources/STM_GUIDE.md) 中的“无关键时间语义”，不是初始模型 `STM_0`。`STM_0` 是修正任务的输入模型，可能来自 strict seed、extended seed 或人工 / 弱模型构造。

## 3. 硬排除码

**判定顺序**：先应用硬排除码，再评估四个谓词。也就是说，即使某个 protocol 或形式规格任务表面上满足“文本输入 -> 状态机输出”，只要触发 `X_PROTOCOL`、`X_FORMAL_SPEC`、`X_PROCESS` 等排除码，就不得标为 strict seed。

| 排除码 | 排除对象 | strict seed 处理 | 可保留用途 |
|---|---|---|---|
| `X_PROTOCOL` | RFC / 3GPP / cellular / network protocol FSM。 | 不计入主 strict seed。 | out-of-domain、reviewer 泛化、related work。 |
| `X_RESOURCE_FLOW` | 资源流、互斥资源生命周期、调度资源图。 | 不计入主 strict seed。 | converter boundary、错误类型背景。 |
| `X_PROCESS` | BPMN、POWL、process model、business process。 | 不计入主 strict seed。 | benchmark 近邻、self-improvement 背景。 |
| `X_SEQUENCE_CLASS` | sequence diagram、class diagram、goal model、domain model。 | 不计入主 strict seed。 | LLM4MDE 近邻。 |
| `X_FORMAL_SPEC` | Petri net、CSP/PAT、Rebeca、Event-B、TLA+、LTL/STL、SAPIC+ 等形式规格。 | 不计入主 strict seed。 | verification / feedback related work。 |
| `X_T1_PLUS` | 关键时间语义为 `T1/T2/T3` 或强实时 / 显式时钟窗口。 | 不计入 strict；可进入 extended / stress seed。 | 转换压力、扩展分析。 |
| `X_HYBRID` | hybrid automata、连续耦合控制主导。 | 不计入 strict。 | 边界与局限性。 |
| `X_NO_GEN_REL` | 只有 `<NL, STM>` 共现，但无 `NL -> STM` 生成 / 派生证据。 | 不计入 strict。 | source pool 或 related work。 |
| `X_REPAIR_ONLY` | 输入是已有 STM，任务是补全、修复、refinement 或验证。 | 不计入 strict seed。 | repair baseline / feedback taxonomy。 |
| `X_ARTIFACT_UNCLEAR` | 论文可能满足 strict，但无法定位输入 / 输出 / 生成关系证据。 | 暂不计入 strict 数量。 | pending candidate。 |

## 4. 多维编码指标

每篇候选至少按下表编码。该表是 PR-R2 建立 `seed_registry` 和 PR-R6 分层报告的最低字段，不要求 R1 逐篇完成全部外部文献筛查。

| 维度 | 推荐取值 | 判定作用 | 证据要求 |
|---|---|---|---|
| `candidate_id` | 稳定 slug / DOI slug | 去重与跨 PR 追踪。 | DOI > 标准化标题 > 作者年份 > slug。 |
| `source_batch` | baseline / sources / reproduction / reviewer-corpus / external-search | 区分既有资产与新增检索。 | 本地路径或 URL。 |
| `screening_depth` | title / abstract / fulltext / artifact | 防止摘要级判断冒充全文核验。 | 至少记录最后核验层级。 |
| `input_type` | requirement / use case / scenario / system description / protocol spec / formal spec / diagram / code | `P1_NL_INPUT` gate。 | 原文段落或 artifact 文件。 |
| `output_family` | FSM / HSM / EFSM / statechart / UML-SM / SysML-SM / PlantUML / Mermaid / Umple / non-STM | `P2_T0_STM_FAMILY` gate。 | 输出样例、图、表、代码或结果文件。 |
| `time_tier` | T0 / T1 / T2 / T3 / hybrid / N/A | strict 与 extended seed 分界。 | 按 [sources/STM_GUIDE.md](../../sources/STM_GUIDE.md) 口径判定。 |
| `generation_relation` | explicit NL->STM / implicit NL->STM / co-exist only / repair-only / unknown | `P3_GENERATION_RELATION` gate。 | 方法章节、实验设置或 artifact pipeline。 |
| `generation_actor` | LLM / rule-based NLP / controlled template or intermediate normalization / human / mixed / unknown | 解释 seed 来源，不作为 strict 必要条件。 | 方法说明。 |
| `control_relevance` | control-system / synthetic-FSM / MBSE-toy / protocol-only / non-control | 决定外部效度与主实验优先级。 | 任务或领域描述。 |
| `artifact_usability` | SA-1 / SA-2 / SA-3 / SA-4 / SA-5 | 决定能否进 R2 可复验样本。 | 文件、commit、hash、license、下载入口。 |
| `conversion_readiness` | deterministic / semi-automatic / manual / not-convertible | 交给 PR-R3 定转换合同。 | 格式样例与字段映射风险。 |
| `gt_leakage_risk` | low / medium / high / unknown | 防止构造 `STM_0` 时偷看 reference。 | seed 构造流程与 reference 隔离记录。 |
| `strict_seed_grade` | SS-A / SS-B / ES-C / NN-D / EX-E / pending | literature eligibility 分级。 | 四个谓词与排除码。 |
| `downstream_role` | R2 seed / extended seed / converter pressure / limited comparison / related work / exclude | 后续使用方式。 | R1/R2 decision。 |
| `evidence_pointer` | 文件路径 + 小节 / 行号 / URL | 可审计性。 | 必填；否则不能标 SS-A/SS-B。 |

## 5. 分级标准

### 5.1 strict seed literature eligibility

| 等级 | 名称 | 判定标准 | 是否计入 strict seed | 后续用途 |
|---|---|---|---|---|
| `SS-A` | strict literature confirmed | 同时满足四个谓词，且未触发任何硬排除码；已有足够证据证明该文献/样本确为 `NL -> T0 STM-family`。artifact 是否可冻结另由 `SA-*` 轴判断。 | 是 | 文献证据；若同时为 `SA-1/SA-2`，再进入 PR-R2 主 seed 候选。 |
| `SS-B` | strict literature candidate | 任务方向看起来满足 strict，但 fulltext / artifact 证据仍不足，或生成关系 / T0 边界需二次核验。artifact 是否可冻结另由 `SA-*` 轴判断。 | 暂不计入 strict 数量 | R2 风险候选 / 待复核。 |
| `ES-C` | extended seed | 存在 NL->状态机关系，但含 `T1+`、非主格式、强转换或外部效度弱。 | 否 | converter pressure、扩展 / stress 分析。 |
| `NN-D` | near neighbor | protocol FSM、process model、formal spec、repair / verification 近邻。 | 否 | related work、feedback taxonomy、boundary。 |
| `EX-E` | excluded | 明确非 NL、非 STM、无生成关系或证据不足。 | 否 | 排除记录。 |
| `pending` | 待筛查 | 尚未完成 fulltext / artifact 核验。 | 否 | R2 / 后续外部检索。 |

### 5.2 seed artifact usability

`SA-*` 只回答“能否进入可复验实验样本”，不改变 `SS-*` 的文献资格判断。最终 R2 样本应优先选择 `SS-A + SA-1/SA-2`；`SS-A + SA-3/SA-4` 只能作为文献证据或 related work。

| 等级 | 名称 | 判定标准 | 是否可进 R2 样本 |
|---|---|---|---|
| `SA-1` | directly usable pair | NL 输入、STM 输出或 reference、license / commit / hash 可冻结。 | 可候选。 |
| `SA-2` | reconstructable | 可从论文或公开材料近似重建，但需记录人工步骤和信息损失。 | 谨慎候选。 |
| `SA-3` | paper-only | 只有论文描述或聚合表，缺少可复验 pair。 | 不进主样本。 |
| `SA-4` | private / access-limited | 原始数据、GT 或逐次输出私有。 | 不进主样本。 |
| `SA-5` | unknown | 尚未核验。 | 不进主样本。 |

## 6. 初始事实台账

### 6.1 `sources/` 宽池与 strict-source 子池

[sources/SUMMARY.md](../../sources/SUMMARY.md) 当前记录 `787` 篇论文、`746` 条正例案例。按案例级字段重新筛选，满足 `状态机类型 ∈ {FSM, EFSM, HSM}` 且 `时间级别 = T0（无关键时间语义）` 的案例为 `337` 条，其中 `EFSM=177`、`HSM=91`、`FSM=69`；当前未出现 `T0 + statechart` 的单独桶，因此 `statechart` 只保留在定义层作为后续外部检索可能命中的状态机家族，不计入本轮 `sources/` 子池数字。

质量与角色分布如下：`💎 核心保留=320`，`🧰 清洗后保留=7`，`🪫 降采样保留=10`；`原文=🟢 A` 且 `描述=🟢 A` 的案例为 `319` 条，其中同时为 `💎 核心保留` 的为 `308` 条；`原文/描述 >= 🟡 B` 的为 `334` 条。换言之，337 条 T0-family 子池中，双 A 占 319 条，约 `94.7%`；双 A 且核心保留为 308 条；B 级以上为 334 条，约 `99.1%`。


#### 6.1.1 `sources/` 数字重算口径

上述 `337 / 177 / 91 / 69 / 319 / 308 / 334` 数字来自 [sources/SUMMARY.md](../../sources/SUMMARY.md) 的“案例总账（按新口径维护）”案例级表，而不是论文级状态表。复算时按如下列过滤：`状态机类型`、`时间级别`、`数据集角色`、`原文细节`、`描述细节`；其中 strict-source 子池条件为 `状态机类型 ∈ {FSM, EFSM, HSM}` 且 `时间级别 = T0`。

这些数字只说明 `sources/` 中存在大量 **T0 + FSM/HSM/EFSM 控制系统 NL 描述源池**。它们不自动等同于外部文献已有的 paired strict seed；若 PR-R2 用弱 prompt、旧模型或人工方式从这些 NL 描述构造 `STM_0`，必须把构造流程、是否偷看 reference、转换损失和 eligibility 单独登记。

### 6.2 九个 direct baseline 的 strict seed 初判

| slug | strict 初判 | artifact 可用性 | 关键限制 | R1 后续角色 |
|---|---|---|---|---|
| `structure-and-event-driven-frameworks...` | `SS-A` 候选 | `SA-1` 候选 | 8 个 reactive-system descriptions 与 UML state machine/reference artifact 最贴近 strict；正式实验前冻结 4open 副本、license 与 hash。 | R2 主 seed / near comparison 优先候选。 |
| `llms_emp` | STM 子集 `SS-A` 候选；ACT/SD 排除 | `SA-1/SA-2` | [reproduction parquet](../../reproduction/results/llms_emp/predictions.parquet) 中 `diagram_type=stm` 为 `38` 行；不能把 ACT/SD 混入 STM seed。 | STM 子集 seed、judge 校准、conversion-aware。 |
| `ttool-ai` | SMD/state-machine 部分 `SS-B/ES-C` | `SA-1/SA-2` | NL 系统规范到 SysML 联合模型；只能取 state-machine panel，不取 BD/IBD/UCD/properties。 | 工具格式 seed / converter pressure。 |
| `umple` | `SS-B/ES-C` | `SA-2/SA-3` | NL->Umple state machine 方向贴近，但论文 bundle / pipeline 不完整。 | 转换压力、人工重建候选。 |
| `designing-fsm...` | `SS-B/ES-C` | `SA-2` | NL->DFSM/Mealy CSV；可用初始生成链路，不得把其 repair/refinement 输出当主 seed；合成数据外部效度弱。 | repair-refinement 近邻、CSV adapter 压力。 |
| `req` | `SS-B` | `SA-4` | NL->Mermaid statechart 任务贴合，但 Volvo/Car Weaver 原始数据、人工 statechart 与评分表私有。 | task-boundary / related work。 |
| `pushing-the-generative-envelope...` | `SS-B/ES-C` | `SA-3` | 只有论文表格和 2 个题项，无逐次输出包。 | prompt / temperature 背景。 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | `NN-D` | `SA-3/SA-5` | RFC -> protocol FSM，触发 `X_PROTOCOL`。 | protocol related work，不进主 strict seed。 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | `NN-D` | `SA-3/SA-5` | 3GPP -> protocol FSM，触发 `X_PROTOCOL`。 | protocol related work，不进主 strict seed。 |

### 6.3 reproduction / review corpus 可复用事实

本地 `reproduction/results/` 是结果产物，不是 seed registry，但可帮助 R2/R3 判断哪些候选有可解析样例：

| 入口 | 本地事实 | strict 使用限制 |
|---|---|---|
| [structure_event/predictions.parquet](../../reproduction/results/structure_event/predictions.parquet) | `32` 行，即 `8` 个 case × `4` 个 strategy。 | strict-like；仍需 R2 选取 seed 与 reference，R3 冻结解析路径。 |
| [llms_emp/predictions.parquet](../../reproduction/results/llms_emp/predictions.parquet) | `98` 行，其中 `diagram_type=stm` 为 `38`，`act=21`，`sd=39`。 | 只允许 STM 子集进 strict 讨论。 |
| [ttool/predictions.parquet](../../reproduction/results/ttool/predictions.parquet) | `6` 行，来自 `3` 个 scenario × `2` 个 strategy。 | 只能剥离 state-machine/SMD 部分；联合模型整体不等于 strict seed。 |
| [nimbus/predictions.parquet](../../reproduction/results/nimbus/predictions.parquet) | `4` 行 structured fragment 结果。 | 更适合作 RSML-e / 负面边界，不作为主 strict seed；仅 4 行，不能声称可泛化到 RSML-e 全族。 |

[project_ex1 reviewer corpus](../../../project_ex1_llm_judge_for_stm/state_machine_review_corpus/SUMMARY.md) 当前可消费 `973` 行 reviewer records，其中 baseline `820` 行、新增 protocol `153` 行。该 corpus 是 reviewer 数据资产，不是 seed 总账：`structure-event-driven`、`llms_emp` STM 子集和 `ttool-ai` SMD 子集可作为 strict-compatible review 证据；`psmbench`、`rfcnlp`、`hermes` 的 protocol FSM 只能作 out-of-domain / robustness 资产，不得并入主 strict seed 统计。

## 7. 大规模 seed 文献调研执行方案

| 阶段 | 动作 | 产物 | 验收门 |
|---|---|---|---|
| Survey-0 | 从 `baselines/`、`sources/`、`reproduction/`、review corpus 和 PR #73/#82/#92/#94 统一建立候选入口。 | 初始 `candidate_id` 与 dedup key。 | 不把旧 direct baseline 当封闭全集。 |
| Survey-1 | 扩展外部学术检索：`natural language requirements state machine`、`use case statechart generation`、`scenario to state machine`、`textual requirements UML state machine`、`LLM state machine modeling` 等关键词簇。 | 外部候选清单与检索日期。 | 每条候选记录来源链接、筛查层级与去重结果。 |
| Survey-2 | Title / abstract / fulltext / artifact 四级筛查。 | `screening_depth`、`strict_seed_grade`、`exclusion_code`。 | 没有 fulltext/artifact 证据不得标 `SS-A`。 |
| Survey-3 | 对 `SS-A/SS-B/ES-C` 候选补输入、输出、生成关系和 artifact 可用性。 | 可进入 PR-R2 的 seed registry 候选池。 | 每个 strict 行必须有 `P1/P2/P3/P4` 证据指针。 |
| Survey-4 | 负例 sentinel 复查：protocol、BPMN/process、formal spec、T1+、co-exist only、repair-only 各抽至少 1 例。 | 排除门自检记录。 | sentinel 不得误入 strict。 |
| Survey-5 | 与 PR-R2/R3/R6 交接。 | R2 seed 候选、R3 converter pressure、R6 related-work / comparison 分层。 | 不从 R1 直接推出实验效果 claim。 |

## 8. Review gate

PR #104 重新 ready 前，reviewer 至少检查以下事项：

1. 是否明确写出 strict seed 四谓词与 `T0（无关键时间语义）` 定义。
2. 是否把 `sources/` 的 `337` 条 T0-family 案例写成 **source pool / strict-source 子池**，而不是已闭合 paired strict seed。
3. 是否把 9 个 direct baseline 全部误写成 strict seed；尤其 FlowFSM / SpecGPT 必须触发 `X_PROTOCOL`。
4. 是否把 `llms_emp` 的 ACT/SD、`ttool-ai` 的 BD/IBD/UCD/properties、review corpus 的 protocol 153 行混入主 strict seed。
5. 是否区分 literature eligibility、artifact usability、conversion readiness 和 downstream role。
6. 是否承认大规模外部文献调研尚未闭合，只交付筛选协议和初始台账。
7. 是否避免“已证明可泛化 / 已完成全面 seed census / baseline 覆盖全部空间”等过强 claim。
