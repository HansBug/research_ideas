# llm4se-systematic-review · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude（claude reviewer 子代理；非 sub-subagent）。
- 是否读取 `$ai-research-writing-skill`：是（路径已确认存在 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` 及 references 目录）；本次以 SKILL.md / reviewer-guidelines / reviewer-self-review 的"reviewer 必须在源材料中给出可定位证据，C/I 必须说明对学术目标的影响"为审计纪律。
- 是否读取 `$research-planning`：是（`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 references/planning-prompts.md 路径已确认）；用于把"维度树是否服务后续 A2a / A2b 实证统计"作为评判标准。
- 是否读取 `$oh-my-codex:autoresearch`：是（`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` 路径已确认）；用于校验"从字段抽取到候选发现的证据链是否闭合"。
- 是否完整阅读 `paper_content.txt`：是。覆盖范围：Introduction（Section 1，含 Table 1 相关 surveys）、Approach（Section 2.1 RQ1--RQ4、2.2 QGS 检索流程、2.3 inclusion/exclusion + QAC 10 项、2.4 snowballing、2.5 数据抽取 Table 5）、RQ1（Section 3，含 Fig.4 LLM 三类架构树、Table 6 architecture↔task fit、Fig.5 趋势）、RQ2（Section 4，含 Fig.6 数据源四类、Table 7 数据类型、Fig.7/8 预处理流程、Table 8 输入形式四类）、RQ3（Section 5，含 PEFT 四技术 / 8 类 prompting / Table 9 metric × problem-type）、RQ4（Section 6，含 Fig.10 SDLC + problem-type 分布、Table 10 85 个 SE task）、Threats（Section 7 三类 + 缓解）、Challenges & Opportunities & Roadmap（Section 8）、Appendix A--E（字段↔primary-study 引用映射）。
- 是否核对 `paper.pdf`：否。本轮仅做文本级审计，无 PDF 视觉核对环境；review.md 自身亦将精确页码与图表版式列为 A2a 待办。Fig.4/Fig.5/Fig.6/Fig.10 等高密度图表的数值在 `paper_content.txt` 中已被 PDF 提取工具输出，可逐行核对，已使用文本中的数字（如 235 open-source、six industrial、355 input-form 分母、97.75% token-based、56.65% software development 等）作为代替证据。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

- 整体目标：在 2017-01--2024-01-31 区间内对 LLM4SE 做系统综述，覆盖 LLM 模型、数据、优化/评价、SE 任务四个维度，给出 state-of-the-art 综述 + gap + roadmap。
- 四个 RQ（Section 2.1）：
  - RQ1：What LLMs have been employed to date to solve SE tasks?
  - RQ2：How are SE-related datasets collected, preprocessed, and used in LLMs?
  - RQ3：What techniques are used to optimize and evaluate LLM4SE?
  - RQ4：What SE tasks have been effectively addressed to date using LLM4SE?
- 6 项核心贡献：首篇覆盖 2017--2024 的 395 篇 LLM4SE SLR；LLM 三类架构分类；data processing stages；optimizer/PEFT/prompt + 评价指标；85 个 SE task × 6 个 SDLC 阶段；challenges + future directions。

### 2.2 方法流程

- 方法基底：Kitchenham SLR guideline，分 plan / conduct / analyze 三步。
- 检索：Quasi-Gold Standard（QGS）三段式：
  1. Manual search：6 个 SE 顶会期刊（ICSE / ESEC/FSE / ASE / ISSTA / TOSEM / TSE）爬取 4,618 篇，人工筛 51 篇构成 QGS。
  2. Search string derivation：SE keywords（覆盖 software engineering / development / testing / requirements / code-X / mining 等 40+ 词）+ LLM keywords（LLM / PLM / Pre-trained / Transformer / BERT / Codex / GPT / T5 / ChatGPT / GPT-* 等）。
  3. Automated search：在 IEEE Xplore（1,192）/ ACM DL（10,445）/ ScienceDirect（62,290）/ WoS（42,166）/ Springer（85,671）/ arXiv（9,966）/ DBLP（4,035）共得 218,765 篇候选。
- 多阶段筛选（Fig.1）：218,765 → <8 页过滤 80,611 → 标题/摘要/关键词 5,078 → venue 过滤 1,172 → 去重 810 → 全文检查 594 → 质量评估 382；再做 forward（3,964）/ backward（9,610）snowballing → 去重 5,152 → 补 13 篇 → 最终 395。
- 纳排标准：Table 3 给出 3 条 inclusion + 9 条 exclusion（含 short paper / 重复 / 非 peer-review venue / tool demo / workshop / 非英文 / 仅提到 LLM 无技术描述 / SE 反向应用于 LLM 等）。
- 质量评估：Table 4 给出 10 项 QAC；QAC1--3 用 -1/0/1，QAC4--10 用 0/1/2/3；正式发表论文阈值 ≥ 16.8/21（80%），arXiv 论文阈值 ≥ 14.4/18（80%）。
- 数据抽取：Table 5 显式将 8 个数据项绑定到 RQ：SE task category（1,2,3,4）/ LLM category（1,2,3,4）/ LLM characteristics & applicability（1,4）/ data handling techniques（2）/ weight training algorithms & optimizer（3）/ evaluation metrics（3）/ SE activity（4）/ developed strategies & solutions（4）。
- finding 形成方式：每个 RQ 末尾有 "RQ#-Summary"；Section 8 把分布与 gap 转化为 challenges、opportunities、roadmap action point；Section 7 单独写 threats。

### 2.3 显式抽取 schema / taxonomy / coding scheme / figure / table

- LLM taxonomy（Fig.4 + Section 3.1）：三大架构 encoder-only / encoder-decoder / decoder-only；每类下列出全部模型实例并标注计数（如 BERT 50、CodeBERT 51、Codex 62、ChatGPT 72、GPT-4 53、StarCoder 25 等），共 70+ 模型；Table 6 给出 architecture → task fit 映射。
- 数据来源四分类（Fig.6 + Section 4.1）：open-source（235）/ collected（98）/ constructed（60）/ industrial（6）。
- 数据类型五分类（Table 7）：text-based（151，子类 22 项，从 programming tasks/problems 42 到 user reviews 1）/ code-based（103，子类 13 项）/ graph-based（1）/ software-repository-based（20）/ combined（55）。
- 数据预处理流程：text-based 7 步（Fig.7）；code-based 7 步（Fig.8）。
- 输入形式四分类（Table 8）：token-based（347，子类 3 项）/ tree-graph（5）/ pixel（1）/ hybrid（2），分母 355 篇。
- 优化技术分类（Section 5.1）：full fine-tuning（83）/ ICL / PEFT（LoRA 8、prompt tuning 3、prefix tuning 2、adapter tuning）/ RL / SFT / syntax / knowledge-preservation / task-oriented。
- Prompt engineering 八分类 + others（Fig.9）：few-shot 88 / zero-shot 79 / CoT 18 / APE / CoC / Auto-CoT / MoT 1 / SCoT 1 / 其他自定义 76。
- 评价指标 × problem-type（Table 9）：regression 1（MAE）/ classification 9 metrics（Precision 35、Recall 34、F1 33、Accuracy 23、AUC 9、ROC 4、FPR 4、FNR 3、MCC 2）/ recommendation 6 metrics / generation 19 metrics（BLEU 62、Pass@k 54、Accuracy 39、EM 36、CodeBLEU 29 等）。
- SE 任务分类（Fig.10 + Table 10）：6 SDLC 阶段（requirements engineering 3.9% / software design 0.92% / software development 56.65% / software QA 15.14% / software maintenance 22.71% / software management 0.69%）+ problem-type 四分类（generation 70.97% / classification 21.61% / recommendation 6.77% / regression 0.65%）+ 85 个具体 SE task；其中 software QA 下有 verification（5 篇）、requirements engineering 下有 specification formalization（1 篇）、traceability automation（1 篇）等。
- Appendix A--E：将数据类型 / 输入形式 / prompt engineering / 评价指标 / SE task 全量映射到具体 primary-study references；Replication package：`https://github.com/xinyi-hou/LLM4SE_SLR`（正文）vs `https://github.com/security-pride/LLM4SE_SLR`（abstract，待复核）。
- Threats（Section 7）：三类 paper search omission / study selection bias / empirical knowledge bias + 各自缓解。
- Challenges & Opportunities & Roadmap（Section 8）：把统计观察（如 industrial 数据稀缺、RE/design/management 低覆盖、benchmark 缺口、安全性、鲁棒性）转化为 challenge 与 future direction。

### 2.4 finding 形成路径

原文标准化路径：抽取字段（Table 5）→ 分布统计（Fig.2/5/6/10、Table 7/8/9/10）→ RQ-Summary 段中给出"现象 + 占比 + 含义"→ Section 8 challenges/opportunities/roadmap 把"低覆盖、不均衡、依赖、未充分评估"等模式提升为 candidate gap / recommendation。这条链路是 schema-driven + appendix-anchored，是 Paper2 A1-DT 应该完整复原的对象。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分通过 | `dim-llm4se-systematic-review-root` 标题取自论文题名，未直接绑定四个 RQ；根节点应明确写出"对象 = LLM4SE primary studies，单位 = 395 篇 peer / arXiv 论文，RQ1--RQ4 + Section 8 roadmap"。 | M |
| 主干分支是否覆盖原文 schema | **不通过** | 当前 b1--b5 五条主干为通用接口（范围 / 语料 / 分类 / 方法 / 评价+发现），未独立列出原文最关键的两条主干"LLM 架构-模型族（RQ1）"与"数据-预处理-输入形式（RQ2）"；Table 5 中 8 个 data item 与 RQ 的显式绑定关系在树中完全没有还原。"评价、统计与候选发现"被压成一条 b5，导致 evaluation metric × problem-type 与 finding / roadmap / threats 混在同一分支。 | **C** |
| 叶子维度是否足够具体 | **不通过** | review.md 自陈"六个 leaf-* 是跨论文通用接口层，不是原文叶子全集"；真正承担原文 schema 的"原文模式候选叶子映射（A1 种子）"只有 5 个极度抽象的占位项（se-task / llm-method / dataset-benchmark / metric / limitation-risk），远小于原文实际暴露的字段树（LLM 三类架构 × 70+ 模型族；数据四源 × 五类型 × 7 步预处理 × 四种输入形式；PEFT 四技术 + 8 类 prompt + 19 generation metrics；SDLC 6 阶段 × 4 problem-type × 85 具体任务；QGS / QAC10 / threats 三类）。这是典型的"把通用 6 leaf 接口当原文 schema"的过小化错误，正是本审计需要标出的核心问题。 | **C** |
| 取值空间是否可执行 | **不通过** | 6 个 leaf 的"取值空间"全是"自由文本 / 完整枚举 / 层级枚举 / 布尔 / 数值 / 链接状态"等元描述，并未把原文实际可枚举的有限集合（如 encoder-only/encoder-decoder/decoder-only、open-source/collected/constructed/industrial、token/tree/graph/pixel/hybrid、LoRA/prompt/prefix/adapter tuning、six SDLC phases、generation/classification/recommendation/regression）作为取值空间写下来。下游 A2a 无法据此做统计。 | **C** |
| 关系边是否缺失 | 不通过 | 仅给出两条关系边（method↔evidence、taxonomy↔finding）。原文真实关系至少包括：RQ↔data-item（Table 5）、architecture↔task-fit（Table 6）、problem-type↔metric（Table 9）、SDLC↔specific-task（Table 10）、threats↔mitigation（§7）。当前只保留 2 条会让 A2a 无法识别原文核心的交叉表。 | I |
| 统计用途 / 分母是否正确 | 不通过 | 评价用途表把整树统一标为"否（A1-DT 阶段仅作 schema seed）"，但 metadata.json 自身已声明 `eligible_for_statistical_synthesis: true`、`systematic_evidence_status: "systematic_review"`、`evidence_role: "slr_field_schema_pattern"`。当前两份事实源自相矛盾；A2a 接手时无明确分母（应至少标注 395 / 374 / 355 / 382 / 83 / 88 等分母语义）。 | I |
| 候选 finding 路径是否完整 | 不通过 | "统计观察与候选发现"叶子未把原文 Section 8 已经显式给出的 challenge / opportunity / roadmap 三栏作为子结构展开，也未给出原文已存在的具体候选发现锚（industrial-data gap、RE/design/management 低覆盖、token-input 主导、decoder-only 占优、verification 仅 5 篇、specification formalization 仅 1 篇等）。导致下游 A2a 要重新识别原文已经写好的 candidate finding。 | I |
| A.1--A.4 证据链是否足够 | **不通过** | A.2 表 5 行证据全部为 `not_verified`、原文短引"见释义"、原文页码全部留白；但 `paper_content.txt` 已可定位到具体页（QGS Fig.1 P5、QAC Table 4 P7、数据抽取 Table 5 P9、LLM 分类 Fig.4 P10/Table 6 P11、数据源 Fig.6 P15、数据类型 Table 7 P16、输入形式 Table 8 P19、prompt Fig.9 P23、metric Table 9 P25、SDLC Fig.10 P26、Table 10 P27、threats §7、roadmap §8）。证据强度被人为压低，与正文 §2 的密集复原不一致。 | **C** |
| 是否存在可能误导 A2a 的强主张 | 通过 | 一句话结论里反复加了"schema seed / 待 A2a 精核"降级语，对 A2a 不会形成虚假强主张；Section 6.2 风险栏对"不能作为目标领域 evidence pool / 工业占比低 / arXiv 占比高 / 时间漂移"已显式标出。 | 通过 |

## 4. 建议维度树骨架

根节点：`[dim-llm4se-systematic-review-root] LLM4SE SLR / 单位 = primary study（n=395，382 quality-assessed + 13 snowballed；其中 154 peer-reviewed，241 arXiv）` —— 绑定 RQ1--RQ4 + Section 8 roadmap。

主干（与 RQ 同构 + 1 个跨字段证据层 + 1 个 finding / threats 层）：

- **B1 综述协议与语料 corpus（来源：§2 + Fig.1 + Tables 2--4）**
  - leaf-scope-rq：四个 RQ 文本 + 6 项贡献声明；取值空间封闭。
  - leaf-search-strategy：seed venues = {ICSE, ESEC/FSE, ASE, ISSTA, TOSEM, TSE}；QGS size = 51；databases = 7 项命名集合；keyword families = {SE, LLM} 两族。
  - leaf-screening-funnel：分母链 218,765 → 80,611 → 5,078 → 1,172 → 810 → 594 → 382 → +13 → 395。
  - leaf-inclusion-exclusion：3 IC + 9 EC（Table 3）枚举值。
  - leaf-quality-assessment：QAC 10 项；阈值 16.8/21 与 14.4/18；QAC1--3 vs QAC4--10 评分制。
  - leaf-snowballing：forward 3,964 / backward 9,610 / 去重 5,152 / 入库 13。

- **B2 LLM 对象树（RQ1，来源：§3 + Fig.4 + Table 6 + Fig.5）**
  - leaf-architecture：{encoder-only, encoder-decoder, decoder-only}（封闭）。
  - leaf-model-family：70+ 模型族枚举（BERT 50、CodeBERT 51、CodeT5 46、Codex 62、ChatGPT 72、GPT-4 53、GPT-3.5 54、CodeGen 44、InCoder 29、CodeGPT 26 …）；带计数。
  - leaf-parameter-size-declared：布尔 + 数值（million / billion）。
  - leaf-architecture-task-fit：Table 6 三行映射 understanding / understanding+generation / generation。
  - leaf-temporal-trend：2020--2024 年份 × 架构计数矩阵（Fig.5）。

- **B3 数据对象树（RQ2，来源：§4 + Fig.6/7/8 + Tables 7--8 + Appendix A/B）**
  - leaf-source-category：{open-source 235, collected 98, constructed 60, industrial 6}（分母 = 374）。
  - leaf-data-type：text-based 151 / code-based 103 / graph 1 / repo 20 / combined 55；子类合计 50+ 具体 artifact。
  - leaf-preprocessing-step：text 7 步 / code 7 步两条流程（Fig.7/8）。
  - leaf-input-form：{token 347, tree/graph 5, pixel 1, hybrid 2}（分母 = 355；token-based ≈ 97.75%）。

- **B4 优化与评价（RQ3，来源：§5 + Fig.9 + Table 9 + Appendix C/D）**
  - leaf-tuning：{full fine-tuning 83, ICL, PEFT.LoRA 8, PEFT.prompt 3, PEFT.prefix 2, PEFT.adapter, RL, SFT, syntax FT, knowledge-preservation FT, task-oriented FT}。
  - leaf-prompt-engineering：{few-shot 88, zero-shot 79, CoT 18, APE, CoC, Auto-CoT, MoT 1, SCoT 1, custom-prompt 76}。
  - leaf-problem-type：{regression, classification, recommendation, generation}（封闭）。
  - leaf-eval-metric-by-problem-type：Table 9 完整矩阵；要求按 problem-type 绑定。

- **B5 SE 任务对象（RQ4，来源：§6 + Fig.10 + Table 10 + Appendix E）**
  - leaf-sdlc-activity：6 阶段封闭枚举 + 占比（RE 3.9 / design 0.92 / dev 56.65 / QA 15.14 / maint 22.71 / mgmt 0.69）。
  - leaf-specific-task：85 个具体任务 + 计数（含 verification 5、specification formalization 1、traceability automation 1 等对 Paper2 高相关项）。
  - leaf-problem-type-distribution：{generation 70.97, classification 21.61, recommendation 6.77, regression 0.65}。
  - leaf-input-output-artifact：把 specific-task → input/output artifact 类型连起来（与 B3 cross）。

- **B6 证据与制品层（来源：Appendix A--E + 论文 GitHub）**
  - leaf-table-figure-anchor：Fig.1--10 + Tables 2--11 枚举。
  - leaf-primary-study-reference-anchor：Appendix 字段↔[ref] 映射。
  - leaf-replication-package：GitHub URL（两条候选 URL，需核实）。
  - leaf-extraction-uncertainty：QAC 评分、coder agreement 缺失记录。

- **B7 Threats、Challenges 与 Roadmap（来源：§7 + §8）**
  - leaf-threat-category：{search omission, selection bias, empirical knowledge bias}（封闭）+ 各自 mitigation。
  - leaf-challenge-candidate：industrial-data gap / under-explored phase / benchmark gap / hallucination / robustness 等显式 candidate。
  - leaf-opportunity-roadmap：Section 8 future direction 子节列出的 action point。

关系边（最少集）：

- edge-rq-dataitem：B1.leaf-scope-rq → {B2.architecture, B3.source-category, B4.tuning, B4.prompt, B4.eval-metric, B5.sdlc, B5.specific-task, B5.problem-type}（来源：Table 5）。
- edge-arch-task：B2.architecture → B5.problem-type-distribution（Table 6）。
- edge-problemtype-metric：B5.problem-type → B4.eval-metric（Table 9）。
- edge-sdlc-task：B5.sdlc-activity → B5.specific-task（Table 10）。
- edge-funnel-quality：B1.screening-funnel → B1.quality-assessment（§2.3--2.4）。
- edge-threat-mitigation：B7.threat-category → B1.search-strategy / B1.quality-assessment（§7）。
- edge-finding-evidence：B7.challenge → 任一 B2--B5 分布 leaf + B6.primary-study-anchor。

为何当前 review 不足以保留：当前树只有 5 个 b 分支 + 6 个通用 leaf，把 RQ1（LLM 架构）与 RQ2（数据）合并进同一个 b3 "主题/对象分类"；评价 metric 与 finding/threats/roadmap 全部塞进 b5；导致原文 RQ↔字段的 1:1 schema 被压扁，A2a 无法据此做精细统计。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干分支重构为 RQ 同构 | review.md "维度树结构" | 把 b1--b5 替换为本审计 §4 给出的 B1--B7（语料协议 / LLM 对象 / 数据对象 / 优化评价 / SE 任务 / 证据制品 / Threats-Roadmap），以与 Table 5 的 8 个 data-item 直接对应。 | paper_content.txt L386--395 (Table 5)、L162--185 (RQ1--RQ4)、L605--615 (RQ1-Summary) | **C** |
| 把原文五分类 / 四分类 / 三分类的封闭取值空间写入叶子 | review.md "叶子维度表"或新建 B2--B5 子表 | 在 architecture / source-category / data-type / input-form / tuning / prompt-engineering / problem-type / sdlc-activity 等叶子明确列封闭枚举值与原文计数。 | paper_content.txt L433--438 (Fig.4 架构)、L632--660 (Fig.6 数据源)、L692--725 (Table 7)、L881--886 (Table 8)、L985--1029 (PEFT)、L1051--1113 (prompt 八类)、L1143--1162 (Table 9)、L1201--1280 (Table 10) | **C** |
| 候选 leaf 重新挂载到正确 RQ 分支 | review.md "原文模式候选叶子映射（A1 种子）" | 当前 orig-llm-method 挂在 b2 "语料收集与纳排"、orig-metric 挂在 b4 "方法/技术/干预"、orig-se-task 挂在 b1 "综述范围"，全部 RQ↔分支错位。修复时应：llm-method → B2(RQ1)、dataset-benchmark → B3(RQ2)、metric → B4(RQ3)、se-task → B5(RQ4)、limitation-risk → B7(§7)。 | paper_content.txt L162--185 (RQ 定义)、L386--395 (Table 5) | **C** |
| 把"统计用途 / 主统计池资格"与 metadata.json 对齐 | review.md "统计与候选发现链路"、"一句话结论"、Section 5 metadata | 当前表自陈"否（A1-DT 阶段仅作 schema seed）"，但 metadata.json `eligible_for_statistical_synthesis: true`、`systematic_evidence_status: "systematic_review"`。需在 review.md 内显式声明"本论文可进入主统计池"，并把降级语限定为"A1-DT 阶段的分母与字段冻结尚未完成"，而非"该论文不进入统计"。 | metadata.json L24--27 | I |
| A.2 证据账本升级（去 not_verified 化） | review.md A.2 表 | 至少 EV-002 / EV-003 / EV-005 应填入具体页码（Fig.1 P5、Table 4 P7、Table 5 P9、Fig.4/Table 6 P10--11、Fig.6 P15、Table 7 P16、Table 8 P19、Table 9 P25、Fig.10/Table 10 P26--27、§7、§8）与原文短引（如 "open-source（235）/ collected（98）/ constructed（60）/ industrial（6）"），证据强度可升至 medium。 | paper_content.txt 全文已可定位（行号见上） | **C** |
| 关系边补全 | review.md "关系边表" | 在现有 method↔evidence 与 taxonomy↔finding 两条之外，新增 rq↔dataitem、arch↔task-fit、problem-type↔metric、sdlc↔specific-task、threat↔mitigation、funnel↔quality 六条关系边。 | paper_content.txt Table 5/6/9/10、§7 | I |
| Threats 三分类与 Roadmap 显式分类 | review.md "维度树结构"新增 B7 节点 | 把 Section 7 的三类 threat（search omission / selection bias / empirical knowledge bias）与 Section 8 的 challenges / opportunities / roadmap 作为独立 leaf，而非压在 finding 通用层下。 | paper_content.txt §7 + §8 | I |
| 报告候选 finding 的原文锚 | review.md "统计与候选发现链路" 或新表 | 至少把 "industrial-data gap (6/374)"、"under-explored phases RE/design/mgmt (<5% 之和)"、"token-based 主导 (97.75%)"、"decoder-only 主导 (2023 70.7%)"、"verification 仅 5 篇 / specification formalization 仅 1 篇" 等原文已显式给出的候选 finding 写入 candidate ledger，标注分母与外推限制。 | paper_content.txt L673（六篇 industrial）、L919--947（97.75%）、L572--580（decoder-only 2023 70.7%）、L1254（verification 5 篇）、L1238（specification formalization 1 篇） | I |
| 文档级编号修复 | review.md §3 至 §7 | 当前 review.md 出现 §1 / §2 / §3 / §4 / §5（迁移）/ §6 / §7 / "维度树复原" / "审计附录"，但 §5 已被标记为历史草稿，导致后续 §6 / §7 编号不连续，且 §5 与"维度树复原"语义重叠。建议显式删除旧 §5 编号或重排为 §3 模式 / §4 启发 / §5 待复核 / §6 维度树复原 / §7 审计附录。 | review.md L171--237 | M |
| Replication package URL 二义性核实 | review.md §2.7 / metadata.json | metadata.json abstract 写 `security-pride/LLM4SE_SLR`；review.md §2.7 指出正文写 `xinyi-hou/LLM4SE_SLR`。建议在 A2a 之前最少做一次 git ls-remote 或 HEAD 探测以确认两个 URL 的关系（fork / 迁移 / 镜像），并在 review 中明确事实。 | metadata.json abstract、paper_content.txt L28 | M |

## 6. C/I/M 结论

- **C（4 项）**：
  1. 主干分支未与 RQ1--RQ4 + threats/roadmap 同构，把 LLM 对象、数据对象、评价、finding 全部压扁。直接影响 Paper2 A1-DT 复原原文 schema 的可信度，并使 A2a 无法据此做精确字段统计。
  2. 叶子层只有 6 个通用接口 + 5 个极度抽象 schema_seed，远小于原文实际暴露的字段集合（封闭枚举、计数、分母均已在原文给出）。会让后续维度树跨论文比较时把"本文有 / 本文未报告"混淆。
  3. 叶子取值空间未写封闭枚举，A2a 无法直接做"占比 / 分布 / 缺口"统计。
  4. A.2 证据账本将所有 EV 标为 not_verified，原文短引留空、页码留空，但 paper_content.txt 全文级证据已足够。这会让 A.2 在 PR-A1-DT 验收时无法通过"证据等级 vs 结论强度"的一致性检查，并对下游 A2a 的资料检索造成误导。
- **I（4 项）**：候选叶子挂错分支（RQ 错位）；统计池资格与 metadata.json 自相矛盾；关系边只有 2 条，缺 RQ↔dataitem 等关键交叉；Threats 与 Roadmap 未显式拆出，candidate finding 未沉淀。
- **M（2 项）**：章节编号断层；replication package URL 二义性未核实。
- 最终建议：**NEEDS FIX**。
  - 不阻塞本 PR 的"维度树复原已存在"声明，但若不修复 4 项 C，A2a 阶段会被迫返工重做原文 schema 复原；Paper2 a1-dimension-tree-inventory 的学术目标（把每篇综述的真实字段树作为后续证据合成与 finding 形成的基础）将不能由本篇承担。
  - 建议优先在本 PR 内补 §4 给出的 B1--B7 骨架与原文封闭取值空间，至少把 EV-002 / EV-003 升级为 verified；其余 I/M 可作为 follow-up。
