# llm4se-systematic-review：A1 S1--S8 round3 单篇维度抽取审计

## 0. 审计边界与阅读状态

- **处理对象**：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/llm4se-systematic-review`。
- **本轮角色**：A1 survey-of-surveys 单篇维度抽取 subagent；未开启 sub-subagent；只处理本篇。
- **输出边界**：本文件只写入 round3 独立审计结果，不修改 `review.md`、`evidence_chain.md`、`SUMMARY.md` 或其他文件。
- **纪律声明**：本文件是 **A1 文本级审计证据**，不是 Paper2 的 final quantitative finding；本文内部的 LLM4SE 数字、比例、任务分布和 roadmap 只能作为 schema seed / 后续 A2a 候选，不得直接写成目标领域最终经验结论。
- **总体判定**：该文是 Kitchenham-style LLM4SE SLR，主样本单位是一篇被纳入的 LLM4SE research paper，最终集合 N=395；原生结构应复原为“检索/纳排元数据 + RQ1--RQ4 四棵编码树”的维度森林。它是后续主统计池候选，但当前仍需 A2a 精核页码、表图、ACM final 与 replication package。

| 材料 | 阅读状态 | 依据 |
|---|---|---|
| `bibtex.bib` | 已读全文 | 13 行；确认正式元数据为 TOSEM 33(8), 2024, DOI `10.1145/3695988`。 |
| `metadata.json` | 已读全文 | 35 行；确认 `review_type=SLR`、样本 395、`eligible_for_statistical_synthesis=true`；同时发现 artifact URL 与正文不同。 |
| `paper_content.txt` | 已读全文 | 4152 行；覆盖摘要、§1--§9、References 与 Appendix A--E。关键锚点包括 RQ1--RQ4、Fig. 1、Table 5、Table 8、Table 10、Appendix Tables 13--17。 |
| `review.md` | 已读全文 | 435 行；重点复核“维度树复原”与 “survey_of_surveys 自身 schema 抽取”。 |
| `evidence_chain.md` | 已读全文 | 47 行；A.1--A.4 均已读，重点核对 `ev-llm4se-systematic-review-*` 与 `clm-llm4se-systematic-review-*`。 |
| `paper.pdf` | 已做必要核对，但未逐页视觉精核 | `pdfinfo` 显示 79 页；用 `pdftotext -layout` 核对 Fig. 1、Table 8、Table 10 的关键分母/表格布局；未人工逐页视觉核验所有图表。 |

## 1. 全文阅读依据与关键证据

### 1.1 核心事实锚点

| 锚点 | 原文位置 / 本地依据 | 对本轮审计的作用 |
|---|---|---|
| 研究对象与样本 | 摘要行 15--28：系统综述 LLM4SE，选择并分析 395 篇，回答 4 个 RQ；artifact URL 为 `xinyi-hou/LLM4SE_SLR`。 | 支撑 S1、S3、S6；确认样本不是本仓库目标领域样本。 |
| 贡献与范围 | 行 122--143：声明 395 篇、LLM 分类、数据处理、优化/评价、85 个 SE task、challenges/research directions。 | 支撑原生森林的顶层边界。 |
| RQ1--RQ4 | 行 158--185：RQ1 模型、RQ2 数据、RQ3 优化/评价、RQ4 SE 任务。 | 作为原生维度森林的 4 个 RQ 根。 |
| 方法学 | 行 149--157：遵循 Kitchenham et al. SLR 方法，planning / conducting / analyzing 三步。 | 支撑 S1=强、S2=强。 |
| QGS 与检索流程 | 行 186--228 与 PDF layout Fig. 1：manual search、automated search、snowballing 与分母链。 | 支撑 S2；也是分母冲突的主要来源。 |
| 纳排与 QAC | 行 262--277、306--368：Inclusion 3 条、Exclusion 9 条、QAC1--QAC10、80% 阈值。 | 支撑 S2、S8；也产生 QAC3 secondary-study caveat。 |
| Snowballing | 行 369--381：382 初始、forward 3,964、backward 9,610、去重 5,152、补入 13。 | 支撑分母链；与 Fig. 1 的 9,601 冲突。 |
| Table 5 data items | 行 386--395：8 项抽取字段绑定 RQ。 | 支撑 S3/S4；是本篇最重要的字段合同。 |
| RQ1 分类 | 行 449--455、Table 6 行 465--475、RQ1 summary 行 605--615。 | 支撑模型/架构子树。 |
| RQ2 数据字段 | 行 631--663、690--725、873--947、RQ2 summary 行 955--966。 | 支撑数据来源、数据类型、预处理、input form 子树。 |
| RQ3 优化/评价字段 | 行 967--1187、Table 9 行 1142--1163、Appendix C/D。 | 支撑调优、prompt、metric 子树。 |
| RQ4 任务字段 | 行 1192--1280、Table 10；Appendix E 行 4014--4151。 | 支撑 SDLC/task/problem type 子树；必须区分 task-instance 分母。 |
| Threats | 行 1934--1975：search omission、selection bias、empirical knowledge bias；两名 reviewers secondary review；replication package。 | 支撑 S8=中/强之间的裁决；字段级 coder agreement 不足。 |
| Challenges / roadmap | 行 1976--2248：challenges、opportunities、roadmap、SE4LLM。 | 支撑 S7；只迁移 finding 形成模式，不迁移领域结论。 |
| Appendix A--E | 行 3715--4151：Table 13--17 以字段取值回链 primary-study reference IDs。 | 支撑 S4 字段级证据和 source-anchor 模式。 |

### 1.2 分母与表格语义专项审计

| 项 | 文本级事实 | 冲突 / 限制 | 本轮裁决 |
|---|---|---|---|
| 主样本 | 摘要与 §2.5 均为 N=395；质量评估后 382，加 snowballing 13。 | 无主分母冲突。 | N=395 可作为本篇 SLR 主样本单位，但 A2a 前仍只作候选统计池入口。 |
| Automated search | 正文 §2.2.2：IEEE 1,192 + ACM 10,445 + ScienceDirect 62,290 + WoS 42,166 + Springer 85,671 + arXiv 9,966 + DBLP 4,035。 | 这些数相加为 215,765，不是正文/图中 218,765；Fig. 1/PDF layout 列 ScienceDirect 为 65,290，合计才是 218,765。 | 必须把 **62,290（正文）/65,290（Fig. 1）** 标为待 A2a 核验；不得在 SUMMARY 定量链中无说明地择一。 |
| Snowballing | 正文 §2.4：forward 3,964 + backward 9,610；去重后 5,152，补 13。 | Fig. 1/PDF layout：forward 3,964 + backward 9,601，且图中总 snowballing 13,565 = 3,964+9,601；正文 9,610 会得到 13,574。 | 必须把 **9,601（Fig. 1）/9,610（正文）** 严格区分；当前仅可写“存在冲突，待 PDF/ACM final/replication package 核验”。 |
| Table 5 | 8 个 data items：SE task category、LLM category、LLM characteristics/applicability、data handling techniques、weight training algorithms/optimizer、evaluation metrics、SE activity、developed strategies/solutions。 | 无明显字段冲突；但它是字段合同，不是最终 finding。 | 强证据；应作为原生维度森林的 RQ-field 关系边。 |
| Table 8 | Table 8 总分母为 355 个显式说明 input form 的 papers；总类为 token 347、tree/graph 5、pixel 1、hybrid 2。 | 文中又写 tree/graph “seven studies”，与 Table 8/Appendix B 的 5 不一致；token 子项 150+118+78=346，而表中 token total=347。 | Table 8 只能按 **input-form-explicit 子分母 N=355** 使用；tree/graph 与 token 子项需 A2a 精核，不得混入 N=395。 |
| Table 10 / Fig. 10 | Table 10 活动 total：17+4+247+66+99+3=436；Fig. 10a 百分比与 436 对应。 | 这些不是 395 篇 unique paper 的占比；RQ4 summary 又称 software development “229 papers”，与 Table 10 total 247 不同。 | Table 10/Fig. 10a 应写为 **task-study assignments / task reports 分母 436**；不得说成 N=395 论文分布。 |
| Appendix A--E | Tables 13--17 给每个字段取值附 reference IDs。 | Appendix 表多为字段实例/取值-论文映射，不同表分母不同。 | 可作为 source-anchor 模式；所有定量汇总必须保留对应表分母。 |

## 2. S1--S8 五分栏抽取

> 等级含义沿用 GUIDE §6.4：强/中/弱/不适用只表示对 `survey_of_surveys` 二级 schema 的可用程度，不等于论文质量，也不等于可直接进入最终统计。统计池资格单独列出。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| **S1 综述任务设定：强** | 摘要说明系统综述 LLM4SE，395 篇，RQ1--RQ4；§2 声明 follows Kitchenham et al. methodology；§2.1 给出四个 RQ。 | 顶层对象是“LLM4SE SLR”；原生根可复原为 RQ1 模型、RQ2 数据、RQ3 优化/评价、RQ4 SE 任务，并辅以 challenges/roadmap。 | 可作为 SLR task/RQ-field contract 的统计池候选；不作为 LLM4STM / 控制系统状态机领域 evidence pool。 | 核对 ACM final 与本地 arXiv v6 的 RQ 文本、页码、出版日期和 DOI 占位差异。 |
| **S2 语料收集与筛选：强但分母链有 I 级待核** | QGS：6 个顶级 SE venue、4,618 手工集合、51 QGS；7 数据库 automated search；Inclusion/Exclusion；QAC；snowballing；最终 382+13=395。 | 可复原为完整分母链树：manual search → QGS → automated search → filtering → QAC → snowballing。样本单位为 LLM4SE research paper。 | 可进入后续主统计池候选；但中间分母冲突未消解前只可作为 `schema_seed`。 | 必须核验 62,290/65,290、9,601/9,610；核验 5,078 与 4,341 的图中关系；核验 replication package 是否给出最终 CSV。 |
| **S3 原生维度树 / 样本编码对象：强** | Table 5 将 8 个 extracted data items 绑定 RQ；§3--§6 和 Appendix A--E 按模型、数据、优化/评价、任务组织 395 篇。QAC3 明确“not a secondary study”，但正文又称 systematic views/survey/review papers retained to QA。 | 原生结构是维度森林：检索/纳排元数据树 + RQ1 模型树 + RQ2 数据树 + RQ3 优化/评价树 + RQ4 任务树；编码对象为 primary/research paper，而不是 secondary study。 | 合格候选；secondary-study 边界必须带 caveat。 | 核验最终 395 是否仍含 survey/review；若 replication package 有 study type 字段，应补充 `primary-study intended` / `secondary retained?` 状态。 |
| **S4 字段级证据：强** | Table 5 定义字段合同；Appendix A--E / Tables 13--17 为 data type、input form、prompt、metric、SE task 提供 reference IDs；正文给 replication package。 | 字段证据链：RQ → data item → classification / count table → appendix reference list → artifact。 | 可作为 source-anchor / appendix-as-evidence 模式样本；字段级数字 A2a 前不作最终统计。 | 核验 artifact URL：正文为 `xinyi-hou/LLM4SE_SLR`，metadata 为 `security-pride/LLM4SE_SLR`；核验文件结构、license、与 ACM final 一致性。 |
| **S5 维度模式演化：中** | Threats 中称 RQ 形成参考 DL4SE 等前序综述；每个 RQ 前先读相关文献预定义 categories；full-text review 抽取 Table 5 字段。 | 可复原为“前序综述/领域知识预定义分类 + full-text extraction”的维度形成模式。原文未暴露 open coding、schema revision history、coder agreement、冲突解决日志。 | 可统计“是否报告分类来源/演化”的候选字段；不能统计为完整 audit-first coding process。 | 查 replication package 是否含 codebook 版本、字段定义、双人编码、冲突裁决或审计日志。 |
| **S6 统计分析：强但必须多分母** | N=395 主集合；N=374 显式说明 dataset；N=355 显式说明 input form；Table 9 metric instances；Table 10 task-study assignments；Fig. 2--10 和 Tables 6--17 给出趋势/频次/比例。 | 可复原为多张可计数字段表：architecture、data source/type/input form、prompt、metric_by_problem_type、SDLC phase、specific task、problem type。 | 合格候选；当前仅作为模式池与后续 A2a 统计入口，不可外推到目标领域。 | 精核所有分母：Table 8 N=355、Table 10 分母 436、Table 9 metric instances、Table 7 data-type instances、N=374 dataset-explicit。 |
| **S7 候选 finding：强（模式强，领域结论降级）** | RQ summaries 与 §8 challenges/opportunities/roadmap 将统计观察提升为 gap、challenge、opportunity：工业数据缺口、under-explored phases、评价不足、SE4LLM 等。 | 可复原为“field statistics → challenge/opportunity → roadmap”的 finding 生成链。迁移的是 finding 形成模式，不是 LLM4SE 具体结论。 | 方法模式可入候选池；LLM4SE 领域 finding 不得进入 Paper2 final finding。 | 核验 §8 每个 challenge 是否由前文字段统计支撑；避免 roadmap prose 被直接升级为经验结论。 |
| **S8 研究者 / 作者质疑与裁决：中** | §7 报告 search omission、study selection bias、empirical knowledge bias；two experienced reviewers secondary review；QAC 与 replication package 缓解。 | 质量控制树包括 QGS、纳排、QAC、secondary review、replication package、threat mitigation；缺字段级 coder agreement 和 conflict log。 | 可统计“是否有 QA/threat/replication package”；不能统计为强审计型 study。 | 核验 reviewer 是否独立、是否有 inter-rater agreement、字段抽取是否双人完成、replication package 是否含裁决记录。 |

## 3. 原生维度树 / 维度森林复原

### 3.1 树型与样本单位

- **树型**：维度森林。
- **主样本单位**：一篇被纳入的 LLM4SE research paper / study；最终 N=395。
- **统计池资格**：后续主统计池候选；当前 A1 round3 只冻结文本级 schema 与风险，不生成 final quantitative finding。
- **根对象**：LLM4SE SLR 的 primary-study 编码结果，而不是“LLM4SE 领域真相”的最终证据。

```text
[根] LLM4SE research paper / study（N=395；A2a 前为候选统计池）
├── [M0] 检索与样本元数据树
│   ├── 手工检索源：ICSE / ESEC-FSE / ASE / ISSTA / TOSEM / TSE
│   ├── QGS：4,618 手工 venue papers → 51 relevant papers
│   ├── 自动检索库：IEEE / ACM DL / ScienceDirect / WoS / Springer / arXiv / DBLP
│   │   ├── 初始合计：218,765（但 ScienceDirect 正文 62,290 vs Fig.1 65,290）
│   │   └── 阶段分母：80,611 → 5,078 → 1,172 → 810 → 594 → 382
│   ├── QAC：QAC1--QAC10；published 21 分阈值 16.8；arXiv 18 分阈值 14.4
│   ├── Snowballing：forward 3,964 + backward 9,601/9,610 → 5,152 → +13
│   └── 发表状态：154 peer-reviewed + 241 arXiv
│
├── [RQ1] LLM 使用与模型类型树
│   ├── LLM 架构：encoder-only / encoder-decoder / decoder-only
│   ├── 模型族与实例：BERT, CodeBERT, T5, CodeT5, GPT 系列, ChatGPT, Codex, LLaMA, StarCoder, Claude 等 70+
│   ├── 参数规模：reported numeric / not declared
│   ├── 架构—任务适配：understanding / generation / understanding+generation
│   └── 年份 × 架构趋势：Fig. 5；注意是实例/论文混合统计，需 A2a 精核
│
├── [RQ2] 数据集收集、预处理与输入形式树
│   ├── 数据来源：open-source / collected / constructed / industrial；N=374 dataset-explicit 子分母
│   ├── 数据类型：text-based / code-based / graph-based / software-repository-based / combined；Appendix A 回链 references
│   ├── 文本预处理流程：extraction → segmentation → deletion → preprocessing → deduplication → tokenization → split
│   ├── 代码预处理流程：extraction → deletion → deduplication → compilation → uncompilable deletion → code representation → split
│   └── 输入形式：token / tree-graph / pixel / hybrid；N=355 input-form-explicit 子分母，Table 8 有局部数字冲突
│
├── [RQ3] 优化与评价树
│   ├── 调优技术：full fine-tuning, ICL, PEFT.LoRA, prompt tuning, prefix tuning, adapter tuning, RL, SFT, syntax fine-tuning, knowledge-preservation fine-tuning, task-oriented fine-tuning
│   ├── Prompt 工程：few-shot, zero-shot, CoT, APE, CoC, Auto-CoT, MoT, SCoT, Others
│   └── 评价指标 × 问题类型：regression / classification / recommendation / generation → metric set；Table 9 / Appendix D
│
└── [RQ4] SE 任务与问题类型树
    ├── SDLC 活动：requirements engineering / software design / software development / software quality assurance / software maintenance / software management
    ├── 具体任务：85 个 specific SE tasks；Appendix E 给 reference IDs
    ├── 问题类型：generation / classification / recommendation / regression
    └── 领域缺口候选：RE、design、management、verification、specification formalization 等低覆盖项只能作 LLM4SE 内部候选观察
```

### 3.2 核心叶子维度与取值空间

| 叶子 | 父节点 | 取值空间 | 分母 / 缺失值语义 | 迁移边界 |
|---|---|---|---|---|
| `leaf.search_database_count` | M0 | IEEE 1,192；ACM 10,445；ScienceDirect 62,290/65,290；WoS 42,166；Springer 85,671；arXiv 9,966；DBLP 4,035 | 分母冲突未消解；A2a 前不得择一。 | 只迁移“数据库分母链必须可审计”的模式。 |
| `leaf.snowballing_count` | M0 | forward 3,964；backward 9,601/9,610；dedup 5,152；additional 13 | Fig.1 与正文冲突；A2a 前不得写成强统计。 | 只迁移“snowballing 单独分母”的模式。 |
| `leaf.table5_data_item` | RQ-field contract | 8 项 data items：SE task category、LLM category、LLM characteristics/applicability、data handling techniques、weight training algorithms/optimizer、evaluation metrics、SE activity、developed strategies/solutions | 完整字段合同；缺失值语义需 replication package。 | 高价值 schema seed；不能当作目标领域字段终稿。 |
| `leaf.llm_architecture` | RQ1 | encoder-only / encoder-decoder / decoder-only | 多模型论文为多值；未声明为 unknown。 | 可迁移为 LLM 类研究通用字段。 |
| `leaf.data_source` | RQ2 | open-source / collected / constructed / industrial | N=374 explicitly state dataset；未声明 dataset 不进入该比例。 | 工业数据缺口是 LLM4SE 内部 finding，不外推。 |
| `leaf.data_type` | RQ2 | text / code / graph / software repository / combined + 子类型 | Table 7 / Appendix A 多为 data-type instances。 | STM/形式化任务需扩展 trace、spec、automaton、model-checking artifact 等类型。 |
| `leaf.input_form` | RQ2 | token / tree-graph / pixel / hybrid | N=355 explicitly state input form；Table 8 tree/graph 与 token 子项需核。 | 只迁移“输入形式需单独子分母”的规则。 |
| `leaf.prompt_technique` | RQ3 | few-shot / zero-shot / CoT / APE / CoC / Auto-CoT / MoT / SCoT / Others | 取值可多选；Others=76 说明分类仍有长尾。 | Prompt 技术时间漂移强。 |
| `leaf.metric_by_problem_type` | RQ3 | regression: MAE；classification: Precision/Recall/F1/Accuracy/...；recommendation: MRR/Precision@k/...；generation: BLEU/Pass@k/CodeBLEU/... | Table 9/16 是 metric instances，不是 unique paper 主分母。 | STM/verification 评价指标必须重新定义。 |
| `leaf.sdlc_phase` | RQ4 | RE / design / development / QA / maintenance / management | Table 10/Fig.10a 分母为 task-study assignments total 436，而非 N=395。 | 只能迁移 SDLC 分层模式。 |
| `leaf.specific_se_task` | RQ4 | 85 个任务；含 specification formalization(1)、verification(5)、traceability automation(1) | 多任务论文可多值；Table 10 与 RQ summary 中 229/247 语义需核。 | 低频项不能证明目标领域已充分或不足研究，只能提示扩库方向。 |
| `leaf.problem_type` | RQ4/RQ3 | generation / classification / recommendation / regression | Fig.10b；应视为 task/problem assignment 分布。 | 可迁移为 metric schema 的上层字段。 |

### 3.3 关系边审计

| 关系边 | 源 → 目标 | 原文依据 | 缺失值 / 风险 | 用途 |
|---|---|---|---|---|
| `edge.rq_to_field` | RQ1--RQ4 → Table 5 data items | Table 5 | 无明显冲突。 | 字段合同：每个字段必须服务至少一个 RQ。 |
| `edge.field_to_appendix_anchor` | data/input/prompt/metric/task 取值 → reference IDs | Appendix A--E / Tables 13--17 | 需核验 reference ID 与 replication package 一致性。 | source-anchor 模式。 |
| `edge.architecture_to_task_type` | architecture → understanding/generation/task examples | Table 6 | 是适配关系，不是因果。 | 模型类别与任务类型关系。 |
| `edge.data_type_to_preprocess` | text/code data type → preprocessing pipeline | Fig. 7 / Fig. 8 | graph/repo/combined 未给同等完整流水线。 | 数据类型与预处理绑定。 |
| `edge.problem_type_to_metrics` | problem type → metric set | Table 9 / Appendix D | metric instances 与 paper count 不同。 | 评价指标 schema。 |
| `edge.task_to_sdlc_phase` | specific task → SDLC phase | Table 10 / Appendix E | 多任务论文导致 total=436，不是 395。 | 覆盖度/under-explored phase 分析。 |
| `edge.statistic_to_candidate_finding` | 字段统计 → challenge/opportunity/roadmap | RQ summaries + §8 | roadmap prose 不一定逐条有定量反证。 | Finding 生成模式候选。 |
| `edge.qa_to_eligibility` | QAC / secondary review / threats → inclusion confidence | §2.3.2 + §7 | 缺 coder agreement / conflict log。 | 研究者裁决字段候选。 |

## 4. 对 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 清单

| 等级 | 文件 | 问题 | 影响 | 建议 |
|---|---|---|---|---|
| C | -- | 未发现必须立即阻断 A1 的 critical 问题。 | 当前 `review.md` 已正确将本篇定位为 LLM4SE SLR / schema seed，并多处提示 A2a 待核。 | -- |
| I | `review.md` / `SUMMARY.md` | Table 10 / Fig.10a 的 SDLC 百分比容易被写成 N=395 paper distribution；实际上 Table 10 totals 为 436 task-study assignments，且 RQ4 summary 另有 “229 papers” 表述。 | 若不区分 395 papers、436 task assignments、229 papers，将污染后续 S6 统计池和 under-explored phase finding。 | 在 S6、维度树、SUMMARY S6 中显式写“Table 10/Fig.10a 分母=436 task-study assignments；不是 N=395 unique papers”。 |
| I | `review.md` / `evidence_chain.md` / `SUMMARY.md` | Automated search 中 ScienceDirect 分母存在 **62,290（正文）/65,290（Fig.1/PDF layout）** 冲突；当前 evidence_chain 没有单独记录该冲突。 | 分母链是 S2 的核心证据；若无冲突标注，后续检索分母复现会失真。 | 在 A2a 或 evidence_chain 追加 denominator-conflict evidence；SUMMARY 不要只写“218,765”而不记录 ScienceDirect 差异。 |
| I | `review.md` / `evidence_chain.md` / `SUMMARY.md` | Snowballing backward 分母存在 **9,601（Fig.1）/9,610（正文）** 冲突；Fig.1 总数 13,565 支持 9,601。 | snowballing 分母会影响 S2 语料链可信度。 | 明确写成“Fig.1=9,601；正文=9,610；待 ACM final / replication package 核验”，不得择一升级。 |
| I | `SUMMARY.md` | S1--S8 覆盖矩阵中 S6 “N=395 主分母、数据源/输入形式子分母、SDLC 阶段分布”表述过于压缩，未显式区分 Table 8 N=355、Table 10 N=436、Table 9 metric instances。 | 后续读者可能把所有比例视为 395 篇论文比例。 | 在该行补“多分母：N=374 dataset-explicit，N=355 input-form-explicit，Table10=436 task assignments，Table9=metric instances”。 |
| I | `evidence_chain.md` | A.2 当前只给 `ev-llm4se-systematic-review-denom` 一个高层证据，未拆出 Table 5、Table 8、Table 10、Appendix A--E 与冲突分母的独立证据条目。 | 不足以支持 A2a 后升级为 statistical_synthesis；也不利于审计冲突分母。 | A2a 时将分母冲突、Table5、Table8、Table10、Appendix A--E 分别建证据标识，并保留 `not_verified` 状态直到 PDF/artifact 核验完成。 |
| I | `review.md` / `SUMMARY.md` | S7 可以写“模式强”，但任何 LLM4SE 领域观察（如 verification=5、specification formalization=1、industrial datasets=6）都必须保持 LLM4SE-only。当前 review 已有边界声明，但 SUMMARY 压缩行仍可能被摘录成目标领域 finding。 | 可能违反“严禁把 A1 文本级结果写成 final quantitative finding”。 | SUMMARY 中相关跨论文结论旁增加“LLM4SE-only / schema_seed / not final quantitative finding”。 |
| M | `review.md` | `维度树复原` 中 `leaf.input_form` 写 token=347、tree/graph=5，但未显式提到 Table 8 子项和正文 “seven studies” 的局部冲突。 | 不影响当前 A1 大方向，但会影响后续精确统计。 | 在 A2a 待核项中补 Table 8 子项 sum 与 tree/graph “5 vs seven” 核验。 |
| M | `review.md` | QAC3 secondary-study caveat 已写，但“样本单位=原始研究”仍可能被误读为最终 395 必然全为 primary study。 | 轻微边界风险。 | 改为“primary-study intended research paper；QAC3 应排除 secondary study，但 retained survey/review 阶段性表述待核”。 |
| M | `evidence_chain.md` | A.2 多条证据强度为 `not_verified` 是正确的；`ev-llm4se-systematic-review-pool` 使用 `adjudicated` 作为证据强度，若未来脚本只接受枚举值可能不兼容。 | 工程兼容风险，不影响当前学术判断。 | 可改为 `not_verified; adjudicated eligibility` 或在脚本/指南中允许该值。 |
| M | `review.md` / `evidence_chain.md` | Artifact URL 差异已在 review 中提示，但 evidence_chain A.1 没有单独把两个 URL 作为待核外部来源列出。 | 不影响文本级审计，但影响 replication package 复验。 | A2a 新增 `src-...-artifact-xinyi` 与 `src-...-artifact-security-pride`，核验访问性、fork/owner 关系与 license。 |

## 5. 审计结论

本篇是 19 篇中最强的现代 LLM4SE SLR schema seed 之一：它提供了明确 RQ、系统检索/纳排、QAC、Table 5 字段合同、Appendix A--E source anchors，以及从统计观察到 challenges/opportunities/roadmap 的 finding 形成模式。当前应采纳其 **原生维度森林结构** 与 **RQ-field-source-anchor 方法模式**。

但本轮必须保留三条硬边界：

1. **多分母边界**：N=395、N=374、N=355、Table10=436、Table9 metric instances 不得混用。
2. **冲突分母边界**：62,290/65,290 与 9,601/9,610 必须进入 A2a 核验，不得在 A1 直接裁决。
3. **目标领域边界**：LLM4SE 的模型、任务、比例、低覆盖阶段和 roadmap 只能作为 schema seed / candidate heuristic，不能写成 LLM4STM、控制系统状态机或 formal verification × LLM 的 final quantitative finding。
