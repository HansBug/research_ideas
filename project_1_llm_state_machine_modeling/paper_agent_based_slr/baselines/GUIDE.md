# baselines/GUIDE.md：LLM-based SLR 近邻 baseline 维护规则

## 1. 目标与边界

本目录用于支撑第二篇 agent-based SLR 论文的 Related Work、novelty matrix、claim-evidence map 和评测设计。它不是普通“文献堆放处”，而是一个面向 CCF A 类论文写作的 **claim-evidence baseline 审计库**：每条强判断都必须能回到 PDF、`paper_content.txt`、BibTeX 或官方元数据。

新增或重写条目时，必须判断它是否会威胁本文如下候选贡献：

1. 将 SLR / SMS 的检索、筛选、抽取、编码、综合、报告组织为 agent 工作流。
2. 为每个阶段保存可审计证据链和 run record。
3. 把报告级 主张绑定到论文来源、筛选决策、抽取记录和编码决策。
4. 通过 人工审计 gate 控制幻觉、unsupported claim 和错误证据定位。
5. 在软件工程 / LLM4SE / MDE 语境中评价该工作流。

本目录可以先保存 title / abstract 粗筛，但只要 PDF 已获取，`review.md` 必须逐步升级为全文核验稿。正式写 paper 的 Related Work / novelty 对比时，不能引用粗筛结论替代全文证据。

## 2. 纳入范围

优先纳入：

1. LLM-based systematic literature review / systematic mapping。
2. LLM-assisted screening、corpus filtration、data extraction、coding、evidence synthesis、review composition。
3. agentic / multi-agent literature review、survey 生成、scientific knowledge synthesis。
4. human-in-the-loop evidence synthesis、provenance-aware extraction、claim-to-source traceability。
5. 软件工程、LLM4SE、MDE、empirical SE 中与 SLR/SMS 自动化直接相关的论文。
6. 虽不直接自动化 SLR，但会影响本文 evaluation design、survey quality evaluation、citation grounding、LLM variability、false negative 风险或 SE community positioning 的论文。

暂不纳入或降为 P2：

1. 只做普通摘要、问答、RAG 写作，没有 SLR / SMS 任务语境的工作。
2. 只研究 LLM4SE 任务本身、没有文献综述自动化流程的工作。
3. 只有宣传网页、无论文 / DOI / arXiv / 官方仓库的工具。
4. 与本文 novelty 无关的通用 survey 生成 工作；除非其 agent / evaluation / citation 机制强到足以影响本文报告生成 claim。

## 3. 分层口径

| 分层 | 含义 | 处理规则 |
|---|---|---|
| P0 | 强 baseline / 直接 novelty 威胁 | 必须建立单篇目录；`review.md` 必须全文核验；Related Work 与 novelty matrix 必须逐段对比。 |
| P1 | 高度关注 / 局部强 baseline | 原则上建立单篇目录并全文核验；至少说明威胁筛选、抽取、综合、审计、评价或报告生成中的哪一环。 |
| P2 | 背景相关 / 方法参照 | 若 PDF 可自动获取且会影响 story/evaluation，应建立单篇目录；否则可只留检索表。 |
| PX | 排除 | 只在检索日志保留必要排除理由，不进入总表。 |

## 4. 七维评分标准

emoji 列在正式表格中只写 emoji；中文解释集中写在本节。每篇候选必须独立给出 D1-D7，不能只给一个总等级。

| 维度 | 🟢 强 | 🟡 中 | 🟠 弱 | ⚪ 无 / 背景 |
|---|---|---|---|---|
| D1 主题贴合度 | 直接研究 LLM / agent 执行 SLR、SMS、literature review 或 evidence synthesis | 研究 LLM 辅助筛选、抽取、编码、综述写作中的关键环节 | 只讨论 LLM4SE / research automation，和 SLR 关系间接 | 与 SLR / 文献综述自动化基本无关 |
| D2 SLR/SMS 流程覆盖度 | 覆盖检索、筛选、抽取、编码、综合、报告中的四个及以上环节 | 覆盖两个到三个核心环节 | 只覆盖一个环节或泛泛讨论 | 不覆盖可识别 SLR/SMS 环节 |
| D3 LLM/agent 自动化深度 | 使用 LLM / agent 执行多阶段工作流并有明确输入输出链 | 使用 LLM 辅助单阶段或少数阶段，流程较清楚 | 只做 prompt / chatbot 演示或概念性讨论 | 没有 LLM / agent 自动化实质内容 |
| D4 人工审计与可追踪性 | 明确提供 human-in-the-loop audit、claim-to-source trace、决策日志、per-cell provenance 或可复核证据包 | 有人工复核或 provenance，但链条不完整 | 只提到人工检查或引用来源，缺少可执行审计设计 | 无人工审计或可追踪性机制 |
| D5 评价严谨性 | 有真实数据集、多案例、金标或人工标注、误差分类、对照基线或可复现实验 | 有实验或案例，但样本、指标或复现性有限 | 只有小例子、用户研究片段或定性讨论 | 无实证评价 |
| D6 SE / CCF 相关性 | 发表在 CCF A/B/C SE/AI4SE/MDE 强相关 venue 或直接面向软件工程 SLR | 非 CCF 但与 SE / LLM4SE / MDE 强相关 | 泛 AI / 医学 / 社科综述自动化，可提供方法背景 | 与本仓库主题或目标 venue 关联弱 |
| D7 对本文 novelty 的威胁强度 | 已经覆盖 agent-based + SLR 多阶段 + audit/traceability/evaluation 的核心组合 | 覆盖其中多个关键点，需要本文明确差异化 | 只覆盖局部点，可作为 related work 背景 | 不构成 novelty 威胁 |

### 4.1 全文核验评分规则

1. `粗筛评分` 可以来自 title / abstract；`全文评分` 必须来自 `paper_content.txt` 或 PDF 的方法、实验、系统描述、结论等正文证据。
2. 若全文没有支持某个维度的证据，应降级评分，而不是沿用粗筛推测。
3. 若 PDF 文本提取缺页、乱码或图表缺失，应在该维度写“证据不足 / 待 PDF 核对”，不能脑补。
4. D7 必须和本文 paper2 的具体 主张绑定：威胁的是 agent 工作流、人工审计、claim-to-source、SE setting、evaluation protocol，还是报告生成。
5. 对 arXiv 论文，D6 不能写成 CCF/peer-reviewed；若后续发现正式版本，必须补充 venue 和核验日期。

### 4.2 paper2 主张 ID 与威胁类型

按 `$ai-research-writing-skill` 的 claim-evidence 口径，baseline 不是只判断“相关 / 不相关”，而是要回答它影响 paper2 哪一条可写 claim。每篇 `review.md` 与 [SUMMARY.md](./SUMMARY.md) 至少应使用下列 主张 ID；若后续 story 调整，可新增 ID，但不得复用旧 ID 表示新语义。

| 主张 ID | 当前含义 | baseline 审查时要问的问题 |
|---|---|---|
| C1 | agent 化多阶段 SLR/SMS 工作流 | 该论文是否已经覆盖检索、筛选、抽取、编码、综合、报告中的多个阶段，并以 agent / workflow 形式组织？ |
| C2 | 人工审计 gate / human-in-the-loop | 该论文的人类角色是标注、运行中裁决、事后评价，还是只在论文实验里做 human reference？ |
| C3 | claim-to-source / provenance 证据链 | 该论文是否能把输出 claim、表格单元、引用或筛选决策追溯到源文献位置、页面、段落、表格或运行记录？ |
| C4 | SE / LLM4SE / MDE 场景定位 | 该论文是否直接发生在软件工程、LLM4SE、MDE 或目标 venue 语境中？ |
| C5 | 阶段化评价协议与指标 | 该论文是否提供可复用的筛选、抽取、编码、报告、引用质量、unsupported claim、成本或人工负担指标？ |
| C6 | 报告生成 / survey writing 可靠性 | 该论文是否已经覆盖自动 survey / review composition、citation validity、veracity 或 LLM-as-Judge 评价？ |
| C7 | 可复现 LLM workflow / run record | 该论文是否记录模型、prompt、温度、seed、重复运行、成本、代码、数据、版本和日志，足以支撑复现或公平 baseline？ |

`威胁类型` 必须使用受控口径之一：

| 威胁类型 | 含义 | 写作影响 |
|---|---|---|
| 直接覆盖 | baseline 已覆盖 paper2 某条候选 claim 的核心组合 | 该 claim 必须降级、重写或增加强差异化证据。 |
| 局部覆盖 | baseline 覆盖某个阶段、模块或评价维度 | paper2 可保留组合贡献，但必须在 Related Work 中承认局部近邻。 |
| 负面证据 | baseline 暴露 LLM/agent 在该环节的失败、变异或不可靠性 | paper2 可把它转化为方法动机或实验指标，但不能忽略风险。 |
| 评价协议约束 | baseline 提供了 reviewer 会期待的指标、gold、人工评审或成本口径 | paper2 实验应对齐或解释为什么不可比。 |
| 禁用 claim 证据 | baseline 直接证明某个宽泛 claim 不能写 | 对应 claim 应进入 claims-to-avoid。 |
| 背景定位 | baseline 只提供领域背景或弱近邻 | 可用于 Related Work，但不能作为主 novelty 对手。 |

## 5. 检索策略

### 5.1 CCF A/B/C venue 粗筛

1. 范围以 [../../../ccf_venues/01-venue-scope.md](../../../ccf_venues/01-venue-scope.md) 和 [../../../ccf_venues/SUMMARY.md](../../../ccf_venues/SUMMARY.md) 当前 venue 为基线。
2. 优先级：年度 README 已维护 paper list → 官方 accepted/program/proceedings → publisher TOC → DBLP 年度页 → 搜索线索。
3. 多数 CCF venue 不提供可批量获取 abstract；若只有标题，必须写成 title-level discovery，不能写成 abstract screening。
4. 遇到 429、403、WAF、尚未出版、DBLP 未归档，应写入 [search/ccf-venue-coverage-gaps.md](./search/ccf-venue-coverage-gaps.md)，不得解释为“无相关论文”。
5. 每个 venue-year 的最低审计字段为：入口 URL、检查日期、coverage emoji、是否拿到 title list、命中 title 数、排除理由或 gap 原因；能自动扫描的原始命中应保留到 [search/ccf-dblp-title-scan-raw.md](./search/ccf-dblp-title-scan-raw.md)。
6. 若发现 CCF-adjacent workshop / companion 命中，必须标注 track / source，不得冒充 main track。

### 5.2 arXiv 粗筛

1. 保留 query、检索时间、原始记录、去重数量、纳入数量。
2. 初始 query 至少覆盖：`LLM + systematic literature review`、`LLM + screening/extraction/synthesis`、`agentic literature review`、`automated literature review`、`evidence synthesis`、`survey 生成`。
3. 原始 arXiv query 快照写入 [search/arxiv-query-raw-snapshot.jsonl](./search/arxiv-query-raw-snapshot.jsonl)，2024--2026 去重候选池写入 [search/arxiv-dedup-candidate-pool.jsonl](./search/arxiv-dedup-candidate-pool.jsonl)。
4. 正式纳入候选元数据写入 [search/arxiv-query-results.jsonl](./search/arxiv-query-results.jsonl)，粗筛总表写入 [search/arxiv-2024-2026-title-abstract-screening.md](./search/arxiv-2024-2026-title-abstract-screening.md)。
5. 每条未纳入候选至少保留 `screening_decision=excluded` 与中文排除理由；否则不能把 291→34 这类筛选链条写成可审计。

## 6. 单篇目录规则

每个入库目录至少包含：

```text
papers/<slug>/
├── paper.pdf
├── paper_content.txt
├── bibtex.bib
└── review.md
```

要求：

1. `paper.pdf`：优先使用 arXiv / official open PDF；若 publisher 受限，不强行绕过。
2. `paper_content.txt`：必须用仓库工具生成：
   ```bash
   source venv/bin/activate
   python -m tools.pdf_extractor -i papers/<slug>/paper.pdf -o papers/<slug>/paper_content.txt -m text
   ```
   若文字模式严重异常，再记录 OCR 或人工复查。
3. `bibtex.bib`：至少含 title、author、year、url/eprint；正式引用前再补 DOI / venue。
4. `review.md`：必须按 §6.1 的全文 review 模板维护。逐维判定理由不能只写模板句；每个维度至少要有一个 `paper_content.txt` 页码/章节/表格/实验证据锚点。
5. 单篇 `review.md` 可以使用少量原文短语，但不要复制长段英文；默认用中文转述并给出 PDF / `paper_content.txt` 链接。

### 6.1 `review.md` 全文核验模板

每篇 review 必须显式区分“是否读过原文”。这是证据管理字段，不是措辞装饰。允许的 `阅读状态` 至少包括：

| 阅读状态 | 含义 | 可写结论边界 |
|---|---|---|
| `未读原文-仅题摘粗筛` | 只读 title / abstract / 元数据 | 只能写候选相关性和待核验假设，不得写方法细节或实验结论为事实 |
| `已读全文文本-paper_content核验` | 已阅读 `paper_content.txt` 的摘要、引言、方法、实验、结论等关键部分 | 可写全文级方法/实验/结果总结，但图表和公式若提取不完整需标注 |
| `已回PDF核对图表` | 在文本阅读之外，已打开 PDF 核对关键图表、表格、公式或版式 | 可写图表/表格级证据，并标注页码或表号 |
| `全文不可得-待人工下载` | 合法 PDF 未获取 | 只能保留元数据、下载尝试和为什么值得补全文 |

`阅读状态` 只说明“读到哪里”；`证据等级` 说明“能支撑多强的 paper claim”。快速结论卡片必须同时包含这两个字段，避免把题摘粗筛、全文文本核验和 PDF 图表核对混成同一证据层级。受控 `证据等级` 如下：

| 证据等级 | 适用条件 | 写作边界 |
|---|---|---|
| `题摘级` | 只读题名、摘要、元数据 | 只能写候选相关性，不能支撑方法/实验强对比 |
| `全文文本级；图表待人工核对` | 已读 `paper_content.txt` 关键正文，但未逐页看 PDF 图表 | 可写方法、实验、结果的文本级总结；涉及表格/图形具体数值时须标注待核对 |
| `PDF图表级` | 已人工打开 PDF 核对关键图表、表格、公式或版式 | 可支撑图表/表格级细节，但仍需记录核对日期和位置 |
| `全文不可得` | PDF 未获取或无法合法访问 | 只能保留下载需求和题摘级判断 |

如果一篇论文只是粗略 review，必须在快速结论卡片和 SUMMARY 中如实标注；如果已经全文阅读，也必须写清楚阅读入口和范围，避免后续把不同证据等级混在一起。

快速结论卡片的字段必须按 `$ai-research-writing-skill` 的 claim-evidence 口径维护。最低字段分为七组：

1. **元信息与证据状态**：标题、作者、年份、venue / arXiv / DOI / peer-reviewed 状态、SUMMARY 事实分层 P0/P1/P2、阅读状态、证据等级、核验入口、核验日期或待 PDF 图表核对状态。
2. **任务边界与方法事实**：研究脉络、引用角色、研究任务、输入、输出、覆盖 SLR/SMS 阶段、不覆盖阶段、方法/系统形态、LLM/agent 角色、人类角色与 human-in-the-loop 位置。
3. **审计与 provenance**：人工审计机制、人类角色、审计发生时机、证据溯源粒度、主张追踪状态、决策日志状态、冲突处理机制、审计记录是否可导出。
4. **评价与结果**：RQ 或评价问题、数据集/案例/领域、gold/reference/human label、baselines/comparators、metrics 与方向、主要结果数字、关键结果锚点、数值使用许可、failure/error analysis。若原文未给某项，必须写“原文未给出”，不能省略后让读者误以为已核验。
5. **LLM workflow 与可复现资产**：模型/API 设置、模型角色、提示词状态、温度/重复/随机种子、token/成本、代码状态、数据状态、许可状态、artifact URL / 本地路径、运行可行性。若只是看到论文声称有代码或数据，但未打开核验，应写“给出 URL；本轮未打开核验”或“论文声称但无 URL”，不能写成已可复现；若只是正文出现 `code` / `dataset` 字样但不是本研究制品入口，应写“未提及源码入口”或“方法内部代码描述；非 artifact 入口”。
6. **paper2 claim-evidence 影响**：受影响主张 ID、威胁类型、威胁的 paper2 主张、支持的 paper2 主张、paper2 应避免的主张、差异化要求、对 paper2 evaluation design 的启发、对比方式 / baseline 可用性。
7. **写作与待复核**：可用于 Related Work 的引用角度、可支持的写作强度、局限与可复现性、代码/数据/prompt/license/artifact 状态、按优先级排序的待复核清单。

`分层` 字段只写 SUMMARY 事实分层 P0/P1/P2，不写“全文建议 P0/P1”这类和总账冲突的判断。若单篇作者认为该论文虽被归入 P2 但对某个模块威胁很强，应另设 `近邻强度备注`，并在 SUMMARY 的 claim / 可用性表中解释降级理由。

若目标是支撑 CCF A 类论文写作或 rebuttal，快速结论卡片还应显式覆盖以下扩展字段；本轮如果尚未逐项核验，必须写“待 artifact audit / 待 PDF 图表核对 / 原文未给出”，而不是省略：

| 字段组 | 必填字段 | 目的 |
|---|---|---|
| 来源与审稿状态 | `source_type`、`peer_review_status`、`venue_rank_or_scope`、`doi_or_proceedings_status` | 区分 arXiv、workshop、main track、journal、CCF 与非 CCF，避免把预印本写成同行评审事实。 |
| 方法假设与可比性 | `method_assumptions`、`input_availability_assumption`、`human_expertise_assumption`、`model_access_assumption`、`domain_generalization_boundary`、`comparability_to_paper2` | 回答 baseline 是否要求专家标签、完整 PDF、商业 API、固定领域 taxonomy 或特殊人工裁决，防止不公平比较。 |
| 负面证据与失败模式 | `negative_evidence`、`reported_failure_modes`、`metric_limitations`、`residual_risk`、`paper2_evaluation_implication` | 把 prior work 暴露的问题转成 paper2 的评价指标和失败分析，而不是只摘取正面结果。 |
| 人类研究与数据伦理 | `human_subjects_involved`、`IRB_or_ethics_status`、`consent_compensation_status`、`data_sensitivity`、`data_license_or_terms`、`copyright_redistribution_risk` | 对专家评审、用户研究、clinical / biomedical data、人工标注和 PDF 全文版权风险做条件性核验。 |
| 可复现制品状态 | `artifact_claim_status`、`artifact_url_status`、`artifact_local_status`、`license_status`、`baseline_readiness`、`artifact_evidence_anchor` | 把“论文说有”“URL 可访问”“本地已 clone”“license 可复用”“能 smoke”拆开，防止把文本线索升级为可运行 baseline。 |
| claim-to-source 锚点 | `paper2_claim_id`、`claim_strength`、`source_anchor`、`number_anchor`、`number_use_status` | 每个可能进入论文正文的主张都必须绑定证据强度和位置；含数字时必须标出是否已 PDF 图表核对。 |

每篇全文 review 至少包含以下章节，顺序保持稳定，便于后续汇总脚本和人工阅读：

1. **快速结论卡片**：用一个紧凑表格给出上述七组最低字段；字段名应尽量稳定，便于后续汇总脚本抽取。
2. **D1-D7 全文核验评分**：emoji 单值列 + 每维中文理由 + 证据锚点；明确哪些评分相对粗筛发生变化。
3. **论文解决的问题与背景**：说明原文为什么认为该问题重要，以及与 SLR/SMS/evidence synthesis 的关系。
4. **方法 / 系统拆解**：必须写清输入、输出、阶段、LLM/agent 角色、prompt/RAG/检索/抽取/编码/生成模块、人机交互与异常处理。
5. **实验 / 评价设计**：整理 RQ、数据集或案例、baseline、指标、设置、人工标注/专家评审、统计方式；若没有实验，要明确写出。
6. **主要结果与结论**：只写原文能支持的结果；数字必须来自正文、表格或图，不确定时写“原文未给出明确数值”。
7. **局限与可复现性**：记录代码/数据/提示词是否可得、样本规模、领域限制、模型漂移、人工标注风险、arXiv 未审稿风险。
8. **对 paper2 的具体影响**：指出它威胁或支撑 paper2 的哪类 claim，以及 paper2 必须如何差异化。
9. **可用于写作的引用角度**：给出 2--4 条中文 Related Work 句子草稿或定位语，但不能写 unsupported novelty。
10. **待复核清单**：列出仍需人工看 PDF 图表、补 DOI/venue、下载代码、复核实验数字等事项。

### 6.2 证据锚点写法

推荐格式：

- `paper_content.txt §Abstract / Page 1`：中文转述证据。
- `paper_content.txt §Method / Page 3--5`：中文转述系统阶段。
- `paper_content.txt Table 1 / Page 6`：中文转述指标或结果。

如果 `paper_content.txt` 没有保留章节名或页码，就写关键词定位，例如：`paper_content.txt 中 “Evaluation” 附近段落`。不要把无法定位的记忆写成事实。

## 7. SUMMARY 回填规则

更新 [SUMMARY.md](./SUMMARY.md) 时必须同步：

1. 当前候选总数、本地建库数、P0/P1/P2 数量、全文核验数量、PDF 图表级核对数量、人工下载数量。
2. **主表不能只有 D1-D7**。主表必须同时包含描述性维度，让读者不打开单篇 `review.md` 也能直观看到每篇论文状况。
3. 主表最低字段：年份、分层、标题、venue/状态、peer-reviewed/预印本状态、阅读状态、证据等级、PDF 图表核对状态、研究脉络 / 引用角色、输入、输出、覆盖阶段、方法/系统形态、LLM/agent 角色、人审/审计机制、证据溯源粒度、实验对象/数据集、gold/reference、baselines/metrics/main result、代码/数据/prompt/artifact 可用性、D1-D7、威胁的 paper2 主张、支持的 paper2 主张、paper2 应避免的主张、差异化要求 / paper2 action item、未解决阻塞项、本地链接。
4. `baseline 可用性` 必须使用受控口径之一：`可运行baseline待复现`、`协议/指标baseline`、`定性强baseline`、`仅related-work背景`、`全文不可得待补`。若代码、数据或 prompt 未核验，应写入 可用性或阻塞项，而不是留空。
5. 若 GitHub 单张表过宽，可拆成“主表 A：方法事实与证据等级”“主表 B：D1-D7 与 claim 影响”“主表 C：claim-evidence / 可复现性可用性”。三张表必须覆盖同一批本地条目，并都保留标题到单篇 `review.md` 的相对链接。
6. 以下字段缺失应按 I 级学术风险处理：阅读状态 / 证据等级、venue/状态、peer-reviewed/预印本状态、输入、输出、覆盖阶段、方法/系统形态、LLM/agent 角色、人审/审计机制、证据溯源粒度或其缺失说明、实验对象/指标、主要发现、D1-D7、威胁的 paper2 主张、支持的 paper2 主张、paper2 应避免的主张、差异化要求、baseline 可用性、本地证据入口。
7. 分组总结必须覆盖：多 agent / agent 式 SLR 工作流、人工审计 / provenance、screening / corpus filtration、survey 生成 / review composition、SE 场景近邻、evaluation benchmark / prompt reproducibility。
8. P2 若已建本地目录，应进入主表或背景表，并说明为什么不是 P0/P1；如果 D7=🟢 但仍归 P2，必须在 `差异化要求 / 阻塞项` 中解释它威胁的是 survey 生成 / evaluation 等局部 claim，而非 SLR/SMS evidence workflow 主线。
9. CCF coverage / gap 与人工下载入口必须保留，不能把 coverage gap 写成负证据。
10. `SUMMARY.md` 应给出总体定调结论：哪些 claim 必须禁用，哪些 claim 可以保守保留，后续实验必须补哪些证据。

### 7.1 CCF-A 级字段补强口径

若本 baseline 文库要支撑 CCF A 类标准的 Related Work、novelty matrix、实验设计或 rebuttal 预案，`SUMMARY.md` 不应只复述单篇 quick card，而应额外维护下列 reviewer 会直接追问的字段。字段可拆成主表 D / E，避免把主表 A/B/C 扩到不可读。

1. **主张绑定字段**：`受影响主张 ID`、`威胁类型`、`对比方式`、`paper2 必须采取的动作`。这四项用于把 baseline 结论接到 paper story 和 claim-evidence map，避免“相关但不知道威胁什么”。
2. **阶段边界字段**：`覆盖阶段` 与 `不覆盖阶段` 必须分开；只有写清 baseline 不覆盖什么，才能支撑 paper2 的保守 gap claim。
3. **审计/provenance 字段**：至少拆出 `人类角色`、`审计时机`、`主张追踪状态`、`决策日志状态`、`冲突处理机制`。不能把 expert label、human evaluation、运行中人工裁决和 claim-level provenance 混在一列。
4. **LLM 设置字段**：至少记录 `模型/API 设置`、`提示词状态`、`温度/重复/随机种子`、`成本/token`；若原文未给出，写“原文未给出”。这类缺失本身就是 paper2 可复现性设计的动机。
5. **资产可复现字段**：至少记录 `代码状态`、`数据状态`、`许可状态`、`制品入口`、`运行可行性`。不要用一句“代码/数据/prompt 待复核”覆盖所有论文；它无法支持是否能作为 executable baseline 的决策。
6. **数字证据字段**：凡 `SUMMARY.md` 写入 AUC、F1、accuracy、cost、win-rate、time saving 等数字，必须同时写 `关键结果锚点` 与 `数值使用许可`。当前没有人工 PDF 图表级核对时，默认写“仅文本级引用；正式写作前需 PDF 图表核对”。
7. **方法假设与可比性字段**：至少记录 `关键假设 / 不可比原因`，必要时拆到单篇 `method_assumptions`、`input_availability_assumption`、`human_expertise_assumption`、`model_access_assumption`、`domain_generalization_boundary` 和 `comparability_to_paper2`。这类字段用于判断是否能作为公平 baseline，而不是只判断“主题相关”。
8. **负面证据字段**：至少记录 `主要负证据 / 对 paper2 指标的要求`。若 prior work 报告 false negative、模型变异、citation hallucination、低一致性、人工成本或跨域失败，应回写为 paper2 的评价指标或风险，而不是只在长文里散落描述。
9. **伦理/数据/版权字段**：涉及 human participants、专家评审、clinical/biomedical data、私有全文 PDF、人工标注或用户研究时，必须标注 `ethics/data/license flag`；未核验 IRB、consent、compensation、data terms 或版权再分发时写“待核验”，不能沉默。

推荐受控口径：

| 字段 | 允许值 / 写法 |
|---|---|
| `代码状态` | `未提及` / `声称有；未核验` / `URL已核验` / `已clone未运行` / `已smoke运行` |
| `数据状态` | `未提及` / `公开；未核验license` / `公开且license已核验` / `需申请` / `部分公开` / `不可得` |
| `artifact_claim_status` | `未提及` / `论文声称但无URL` / `给出URL待打开` / `补充材料提供` / `需申请` / `不可得` |
| `artifact_url_status` | `未检查` / `可访问` / `404` / `403/WAF` / `需登录` / `重定向异常` |
| `artifact_local_status` | `未下载` / `已保存metadata` / `已clone未运行` / `已smoke通过` / `smoke失败` |
| `license_status` | `未提及` / `未核验` / `已核验可复用` / `仅学术使用` / `不可再分发` / `需人工许可` |
| `baseline_readiness` | `executable-baseline` / `needs-adaptation` / `protocol-metric-only` / `qualitative-only` / `not-baseline` |
| `提示词状态` | `未给出` / `附录片段` / `repo提供` / `完整可复用` / `版本未定` |
| `运行可行性` | `可运行baseline待复现` / `可复现需改造` / `协议/指标baseline` / `定性强baseline` / `仅related-work背景` |
| `人类角色` | `无` / `标注者` / `运行中审查者` / `冲突裁决者` / `事后评价者` / `领域专家gold` / `用户反馈` |
| `审计时机` | `无` / `运行前` / `运行中` / `运行后` / `仅评价阶段` |
| `主张追踪状态` | `无` / `引用级` / `段落级` / `source-span级` / `页面/表格/单元格级` / `报告级claim链` |
| `决策日志状态` | `无` / `per-record` / `per-stage` / `full run record` / `仅论文叙述` |
| `数值使用许可` | `可直接引用` / `仅文本级引用` / `需PDF图表核对` / `原文未给明确数值` |

其中 `代码状态` / `数据状态` 只能来自原文中的明确制品入口或数据可用性声明。仅因正文出现 “code generation”“dataset construction”“GitHub Copilot”“benchmark dataset”等普通词，不得写“声称有代码/数据”。若未打开外部 URL，最多写“给出 URL；本轮未打开核验”；若原文写 “upon request” 或 “will be added upon publication”，必须分别写成“需申请”或“占位承诺；未发布”。

### 7.2 字段命名风险

1. 避免在主表使用单列 `初步判断` 承载所有信息；它会混淆题摘粗筛与全文结论。应拆为 `主要发现`、`对 paper2 的作用`、`差异化要求`。
2. 避免只写 `核验阶段`；应写成 `阅读状态` + `证据等级`。
3. D6 的正式含义是 `SE / 目标 venue 相关性`，不能把 arXiv 或非同行评审工作写成 CCF / peer-reviewed 事实。
4. P0/P1/P2 表示 novelty 威胁强度，不等同“可复现实验 baseline”或“正式发表等级”。
5. 避免把 `分层` 写成“全文建议 P0/P1”这类自由文本；事实分层与近邻强度备注应分列，便于 SUMMARY 数量闭合。
6. 避免把 `可复现性` 只写在长文末尾；快速结论卡片和 SUMMARY 必须有 代码/数据/prompt/artifact 可用性 或 阻塞项。

### 7.3 字段分层 checklist

为避免字段一次性膨胀到不可维护，后续维护按三层执行：

| 层级 | 进入条件 | 必填字段组 | 验收方式 |
|---|---|---|---|
| L0：全文 review 最低层 | 论文已保存 `paper.pdf` 与 `paper_content.txt` | 元信息、阅读状态、证据等级、输入、输出、覆盖/不覆盖阶段、方法形态、LLM/agent 角色、人审/审计机制、实验对象/指标、主要发现、D1-D7、paper2 主张影响、初步代码/数据/许可状态 | 当前 PR-B0 必须满足；缺失按 I 级处理。 |
| L1：artifact audit 层 | 准备把某篇 work 当作可运行 baseline 或复现实验对象 | artifact claim、URL 状态、本地 clone/download 状态、commit/version、license、prompt/data/code 可复用条件、smoke 命令与结果 | 只有 URL 打开、license 记录、smoke 或阻塞原因写入后，才能把 `运行可行性` 升级。 |
| L2：CCF-A 写作 / rebuttal 层 | 某个 claim 要进入 paper 正文、novelty matrix 或 rebuttal | 方法假设、可比性边界、负面证据、failure modes、metric limitations、伦理/IRB/data/copyright flag、claim strength、source/number anchor | 每个强 claim 都能从 SUMMARY 跳到单篇 `review.md` 和 `paper_content.txt` / PDF 位置；缺证据时降级为 careful/background/avoid。 |

当前 PR-B0 已完成 L0，并对 L1 的代码/数据/许可线索做文本级识别；L1 URL/commit/license/smoke 与 L2 claim-level 写作锚点仍是后续 artifact audit / PDF 图表核对任务，不能提前写成已完成。

## 8. 验证与验收

每轮提交前至少运行：

```bash
source venv/bin/activate
python - <<'PY'
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/papers')
missing = []
for d in sorted(p for p in base.iterdir() if p.is_dir()):
    for name in ['paper.pdf', 'paper_content.txt', 'bibtex.bib', 'review.md']:
        if not (d / name).exists():
            missing.append(f'{d}/{name}')
print('missing=', missing)
raise SystemExit(1 if missing else 0)
PY

git diff --check
```

全文强化 PR 还必须检查：

1. `review.md` 是否包含快速结论卡片、D1-D7、方法、实验、结果、局限、paper2 影响。
2. `SUMMARY.md` 主表是否包含输入、输出、方法、阶段、审计、实验、发现等描述性列。
3. 是否仍有“粗筛”“待全文核验”字样残留在已全文阅读的核心 P0/P1 条目里；若有，必须解释原因。
4. 是否存在“首次性 / 完整覆盖 / PRISMA 合规”等未经证据支撑的强 claim。

如果 reviewer 要求 dry-run，至少选 1 个 P0、1 个 P1、1 个 P2 场景，检查是否能从 README → GUIDE → SUMMARY → search → paper dir 找到证据链。

## 9. 写作禁令

- 不得写“本文是首次自动化 SLR / 首次 agentic SLR”。
- 不得把 PRISMA 风格 / PRISMA 启发式提示写成 PRISMA 合规。
- 不得把 title-level CCF 未命中写成完整负证据。
- 不得把 arXiv 论文写成 peer-reviewed / CCF 事实。
- 不得把粗筛 `review.md` 当成最终 Related Work；正式写作必须回到 PDF / `paper_content.txt` 核验。
- 不得为了让 story 显得强而降低 baseline 的相关性；强近邻必须正面承认并差异化。
