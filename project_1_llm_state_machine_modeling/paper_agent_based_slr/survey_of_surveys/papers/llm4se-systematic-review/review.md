# Large Language Models for Software Engineering: A Systematic Literature Review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Large Language Models for Software Engineering: A Systematic Literature Review |
| 作者 | Xinyi Hou; Yanjie Zhao; Yue Liu; Zhou Yang; Kailong Wang; Li Li; Xiapu Luo; David Lo; John Grundy; Haoyu Wang |
| 年份 / 出版日期 | 2024 / 2024-09-20；本地 PDF 为 arXiv v6 文本，页眉显示 2024-04-10 |
| DOI | <https://doi.org/10.1145/3695988> |
| 类型 | SLR |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [TOSEM](https://dl.acm.org/journal/tosem)；开放全文来自 arXiv PDF |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | A |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 阅读状态 | 已读 `bibtex.bib`、`metadata.json`、`paper_content.txt`；未逐页人工核对 `paper.pdf` 图表 |
| 证据等级 | 全文文本级；图表/表格精确数值、artifact 内容与最终 ACM 版本差异待复核 |
| 语料范围 | 2017 年 1 月至 2024 年 1 月；论文收集截止日为 2024-01-31，最终纳入 395 篇 LLM4SE 研究论文 |
| A1 角色 | 高相关 CCF-A LLM4SE SLR，用来抽取 SE SLR/SMS 的 field schema、artifacts、证据呈现与 threat pattern。 |
| 是否目标领域 evidence pool | 否。它只作为“软件工程二次研究如何建字段树和制品链”的模式样本，不能支撑 Paper2 目标领域 finding。 |
| 一句话结论 | 该文的核心价值不是某个 LLM4SE 结论，而是把 LLM4SE 拆成“模型类型—数据—优化/评价—SE 任务—挑战/路线图”的可审计字段树，并用 appendices/replication package 连接每个字段与 原始研究。 |

## 2. 全文内容详读

### 2.1 背景 / 问题设定

论文指出，已有 LLM4SE 相关综述要么只覆盖单一 SE 子任务（例如 testing、NL2Code、program repair），要么仍停留在 ML/DL for SE，不足以覆盖 ChatGPT、GPT-4、LLaMA 等新近 LLM 在 SE 中的扩散。作者因此按 Kitchenham 系统综述方法组织一篇覆盖 LLM、数据、优化/评价和 SE 应用任务的 SLR。

对 A1 来说，它最重要的 methodological signal 是：作者没有把 SLR 写成“论文列表”，而是预先定义了四个 RQ，每个 RQ 都对应一组可抽取字段，最后再把统计观察提升为 challenges、opportunities 和 roadmap。这正是 Paper2 的 A1-M0--M6 证据工程链条可借鉴的结构。

### 2.2 RQ1--RQ4

| RQ | 原文问题 | 抽取出的元维度 | 对 A1 的意义 |
|---|---|---|---|
| RQ1 | What LLMs have been employed to date to solve SE tasks? | LLM architecture、model family、parameter size、task fit、usage trend | 把“模型”从泛称拆成 encoder-only / encoder-decoder / decoder-only，并关联 SE 任务类型。 |
| RQ2 | How are SE-related datasets collected, preprocessed, and used in LLMs? | data source、data type、preprocessing、input representation | 把数据证据拆成 source/type/process/representation 四层，适合迁移为 Paper2 的字段树。 |
| RQ3 | What techniques are used to optimize and evaluate LLM4SE? | tuning、PEFT、prompt engineering、problem type、metrics | 同时抽取“优化策略”和“评价策略”，避免只统计模型性能。 |
| RQ4 | What SE tasks have been effectively addressed to date using LLM4SE? | SDLC activity、specific SE task、problem type、solution strategy | 用 SDLC 六阶段组织任务分布，并进一步按 generation/classification/recommendation/regression 分类。 |

### 2.3 语料范围：2017--2024

作者把检索起点设为 2017 年，理由是 Transformer 架构论文发表于 2017 年，是后续 LLM 的关键基础。论文收集截止日为 2024-01-31；正文也将时间窗概括为 January 2017--January 2024。最终语料为 395 篇：质量评估后得到 382 篇，再经 forward/backward snowballing 补充 13 篇。

关键边界：该语料是 LLM4SE，而不是 SLR automation、agentic review、formal methods 或 LLM4STM。它可以作为“现代 SE SLR 如何构造分类轴”的样本，不能直接作为本仓库目标主题的证据池。

### 2.4 检索 / 筛选流程

作者使用 Quasi-Gold Standard（QGS）策略：

1. **Manual search**：选择 6 个顶级 SE venue：ICSE、ESEC/FSE、ASE、ISSTA、TOSEM、TSE；爬取 4,618 篇论文，人工确认 51 篇相关论文作为 QGS。
2. **Search string derivation**：从 QGS 和领域知识构造两组关键词：SE task keywords 与 LLM keywords。SE 关键词覆盖 code generation/search/completion/summarization、bug detection/localization、program repair、requirement extraction/traceability/validation、mining GitHub/SO/app 等；LLM 关键词覆盖 LLM、PLM、pre-trained、Transformer、BERT、Codex、GPT、T5、ChatGPT 等。
3. **Automated search**：在 IEEE Xplore、ACM Digital Library、ScienceDirect、Web of Science、Springer、arXiv、DBLP 七个数据库检索，初始获得 218,765 条候选。
4. **Filtering**：按少于 8 页、题名/摘要/关键词、venue 信息、去重、全文检查、workshop/doctoral symposium/灰色文献（grey literature） 等条件逐级筛选。
5. **Quality assessment**：设置 10 个 QAC，覆盖 SE task relevance、LLM usage、是否二次研究、高声誉 venue、动机、技术描述、实验设置/数据、finding、贡献/限制、学术或工业贡献。正式出版论文按 21 分满分，arXiv 按 18 分满分，阈值均为 80%。
6. **Snowballing**：对 382 篇初始集合做 backward/forward snowballing，获得 3,964 + 9,610（正文文本；Fig.1/合计疑似 9,601，待 A2a 核验）条线索，去重后 5,152 条，再筛选补入 13 篇。

可迁移点：QGS 不只是检索技巧，也是一种 A1-M1 脚手架构造方式——先由高置信 venue 构造关键词与候选 schema，再扩展到数据库与 snowballing。

待注意：正文对 QAC3 “not a 二次研究” 与“retained systematic views/survey/review papers for assessment”的表述存在潜在歧义；正式引用其筛选规则前应回 PDF/replication package 核对。

### 2.5 数据抽取

Table 5 将抽取字段直接绑定到 RQ：

- SE task category。
- LLM category。
- LLM characteristics and applicability。
- data handling techniques。
- weight training algorithms and optimizer。
- evaluation metrics。
- SE activity。
- developed strategies and solutions。

这是本文最适合 Paper2 复用的做法：每个字段都要说明服务哪个 RQ，而不是为“信息完整”机械抽取。

### 2.6 分类维度与主要结果

#### RQ1：LLM 类型与趋势

作者采用 encoder-only、encoder-decoder、decoder-only 三分法。encoder-only 主要服务理解类任务，如 code understanding、bug localization、vulnerability detection；encoder-decoder 同时服务理解与生成，如 code summarization、code translation、program repair；decoder-only 更适合生成类任务，如 code generation、code completion、test case generation。

主要发现：395 篇中出现 70+ 种 LLM；decoder-only 成为最常用架构。2020 年研究主要集中于 encoder-only；2021--2022 开始多样化；2023 年 decoder-only 显著占优；2024 年 1 月样本中 decoder-only 仍是中心，但 encoder-decoder 和 encoder-only 仍有探索空间。

#### RQ2：数据来源、类型、预处理与输入形式

作者把数据来源分成四类：

1. open-source datasets。
2. collected datasets。
3. constructed datasets。
4. industrial datasets。

其中 open-source datasets 最常见；显式说明 dataset 的 374 篇中约 62.83% 使用开源数据。industrial datasets 只有 6 篇，作者据此指出学术数据与工业真实场景之间可能错位。

数据类型分成五类：text-based、code-based、graph-based、software repository-based、组合更新。Table 7/Appendix A 进一步细到 programming tasks/problems、prompts、Stack Overflow posts、bug reports、requirements 文档、source code、buggy code、patches、test suites/cases、code repository、issues/commits、pull requests 等。

预处理方面，文本数据流程包括 data extraction、initial segmentation、unqualified data deletion、text preprocessing、duplicated instance deletion、tokenization、segmentation；代码数据流程包括 extraction、unqualified deletion、duplicate deletion、compilation、uncompilable deletion、code representation、segmentation。

输入形式分为 token-based、tree/graph-based、pixel-based、hybrid。token-based 占绝对多数：在 355 篇明确 input form 的研究中约 97.75% 使用 token-based input；tree/graph、pixel、hybrid 仍很少。

#### RQ3：优化与评价

优化策略包括 全量微调（full fine-tuning）、ICL、PEFT、prompt engineering 等。PEFT 进一步包括 LoRA、prompt tuning、prefix tuning、adapter tuning；此外还有 RL、SFT、syntax fine-tuning、knowledge preservation fine-tuning、task-oriented fine-tuning。

Prompt engineering 被整理为八类：少样本、零样本、思维链、自动提示工程、代码链、自动思维链、模块化思维链、结构化思维链（原英文术语保留于审计附录）。另有 76 篇研究虽未落入上述名称，但仍进行了 提示策略 / 提示设计。

评价指标按 problem type 组织：

- regression：MAE。
- classification：Precision、Recall、F1、Accuracy、AUC、ROC、FPR、FNR、MCC。
- recommendation：MRR、Precision@k、MAP@k、F-score@k、Recall@k、Accuracy。
- generation：BLEU、Pass@k、Accuracy@k、Exact Match、CodeBLEU、ROUGE、METEOR、Edit Similarity 等。

这里的可迁移点是：评价字段不应直接绑定具体任务，而应先绑定 problem type，再允许 task-specific metric。

#### RQ4：SE 任务分布

作者按 SDLC 将 SE 任务分为六类：requirements engineering、software design、software development、software quality assurance、software maintenance、software management。研究分布高度不均：software development 约 56.65%，software maintenance 约 22.71%，software quality assurance 约 15.14%，requirements engineering 约 3.90%，software design 约 0.92%，software management 约 0.69%。按问题类型看，generation 约 70.97%，classification 约 21.61%，recommendation 约 6.77%，regression 约 0.65%。

Table 10/Appendix E 总结了 85 个具体 SE task。高频任务包括 code generation、program repair、code completion、code summarization、test generation、vulnerability detection 等；requirements engineering 中有 anaphoric ambiguity treatment、requirements classification、requirement analysis/evaluation、specification generation、traceability automation、specification formalization、use case generation；software quality assurance 中出现 verification，但数量很少。

对本仓库特别重要的观察：需求、设计、形式化规格、验证等与控制系统状态机建模更接近的环节，在这篇 LLM4SE SLR 中属于低占比区域。因此它可以支持“field schema 需要覆盖 under-explored phases”的模式判断，但不能支持“LLM4STM 已被充分研究”的结论。

### 2.7 Artifacts 做法

论文多次声明 replication package / artifacts 公开可得，并在正文给出 GitHub 链接。`paper_content.txt` 中摘要和 threats footnote 指向 `https://github.com/xinyi-hou/LLM4SE_SLR`；`metadata.json` 的 abstract 则记录 `https://github.com/security-pride/LLM4SE_SLR`。该 URL 差异需要后续联网核对。

就文本内容看，artifact 至少承载以下类型：

1. selected 原始研究 list。
2. 每篇研究使用的 LLM 与参数规模。
3. Appendix A--E 的字段到 primary-study references 映射：data types、input forms、prompt engineering、evaluation metrics、SE tasks。
4. 支撑复核的 replication package。

对 Paper2 的启发：appendix 不只是补充材料，而是 field schema 的 source-anchor 层。后续我们自己的字段树也应能从 summary table 跳到单篇论文和原文锚点。

### 2.8 Threats

作者报告三类 threats：

1. **Paper search omission**：关键词不完备可能遗漏相关论文；缓解方式是 manual search + automated search + backward/forward snowballing。
2. **Study selection bias**：BibTeX/metadata 不完整、自动筛选误判、人工判断主观性；缓解方式包括保留无法确定排除的论文进入人工阶段、邀请两名 SE/LLM 领域 reviewers 做 secondary review，并提供 replication package。
3. **Empirical knowledge bias**：395 篇论文需要人工理解和归类，作者经验可能影响 RQ 与分类；缓解方式是参考 DL4SE 等前序综述，并在回答每个 RQ 前先读相关文献预定义分类。

A1 额外风险判断：其 threat 报告比普通 survey 更规范，但仍没有完全暴露每个字段的 coder agreement、冲突解决日志、schema revision history。Paper2 若主打 audit-first，应在这些过程证据上比它更强。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 四个 RQ 按“对象模型—数据—优化/评价—应用任务”展开，形成完整 field schema。 | Section 2.1；RQ1--RQ4。 | 可迁移为 Paper2 的 A1-M0 综述元模型设计范式。 | RQ 内容是 LLM4SE 特有，不能迁移为目标领域结论。 |
| dimension pattern | 核心维度包括 LLM architecture、dataset source/type/preprocessing/input form、tuning/prompt/eval metric、SDLC activity、problem type、specific task。 | Table 5；Sections 3--6；Appendix A--E。 | 高度可迁移为字段树。 | 取值空间偏 code-centric，对状态机/形式化方法需重新扩展。 |
| finding pattern | 从频次与趋势推导出 decoder-only 占优、industrial data 缺口、token input 主导、RE/design/management 低覆盖、evaluation limitations。 | RQ summaries；Section 8。 | 可迁移为“统计观察 -> gap/challenge/opportunity”的 finding 生成方式。 | 这些 finding 属于 LLM4SE，不是 Paper2 目标领域 finding。 |
| evidence presentation pattern | 使用 QGS 流程图、筛选分母、QAC 表、RQ-field 表、分布图、分类表、appendix reference lists、replication package。 | Fig. 1--10；Table 2--17；Appendix A--E。 | 非常适合迁移为审计优先证据呈现模板。 | 本轮未 PDF 核对图表版式；精确数值引用需复核。 |
| validity / threat pattern | threats 分为 search omission、selection bias、empirical knowledge bias，并逐项写缓解措施。 | Section 7。 | 可迁移为 Paper2 的 threat skeleton。 | 对 coder agreement、schema drift、artifact rot 的显式处理不足。 |
| report structure pattern | Introduction / Approach / RQ1--RQ4 / Threats / Challenges & Opportunities / Roadmap / Conclusion；每个 RQ 末尾都有 summary。 | 全文目录与章节。 | 可迁移为“方法--RQ结果--威胁--路线图”的 SLR 报告结构。 | Paper2 是方法论文，不能照搬为纯领域 SLR 结构。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式 | 说明 |
|---|---|---|
| A1-M0 主题与综述元模型设定 | 用 RQ 明确综述对象、数据、优化/评价和任务边界。 | 证明高质量 SE SLR 会先设定可执行元模型，而不是边读边自由摘要。 |
| A1-M1 脚手架挖掘与种子探测 | QGS：顶级 venue manual search -> 51 篇种子 -> search strings。 | 可作为“从高置信种子构造初始 schema/keyword”的脚手架策略。 |
| A1-M2 维度模式准备与批准 | Table 5 将 data items 绑定到 RQ。 | 可迁移为字段合同：每个字段必须服务某个 RQ，并定义最低证据。 |
| A1-M3 论文收集与概览 | 218,765 初始候选 -> 多阶段筛选 -> 382 + 13 -> 395。 | 可迁移为检索分母、排除原因、全文状态、质量阈值的概览卡。 |
| A1-M4 字段级证据抽取与模式演化 | Appendix A--E 把字段取值与 primary-study references 连接。 | 可迁移为 source-anchor 表；但原文未充分暴露 schema revision trail。 |
| A1-M5 统计分析 | 按年份、venue、architecture、dataset、input form、prompt、metric、SE activity 做分布分析。 | 可迁移为字段表上的频次/趋势/交叉统计，而非直接生成结论。 |
| A1-M6 候选发现形成 | Section 8 将统计缺口组织成 challenges、opportunities、roadmap。 | 可迁移为 候选发现 ledger：统计观察先变成候选发现，再由研究者裁决。 |

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **字段树优先于摘要生成**：该文最强的做法是 Table 5 + Appendix A--E，把综述问题、抽取字段、取值表和 primary-study anchors 连成一条链。
2. **QGS 可作为 A1-M1 scaffold pattern**：先用高置信 venue 形成 QGS，再派生 query strings，比直接在数据库中堆关键词更适合审计。
3. **field schema 应服务 RQ**：每个字段都应解释它支撑哪个 RQ；Paper2 可用这一点约束 agent 不做无目的摘录。
4. **结果章节可按 RQ 分段，每段末尾保留 summary**：这有利于从统计观察过渡到候选 finding。
5. **appendix 是证据链，不是剩余材料**：后续 Paper2 的字段证据表、source anchors、artifact links 应像该文 appendices 一样成为可审计资产。
6. **under-explored phase 是重要 finding 类型**：本文通过 SDLC 分布识别 RE/design/management 低覆盖；Paper2 可借鉴这种“覆盖不均 -> 研究缺口”的候选发现模式。
7. **roadmap 要从统计缺口推出**：Section 8 的 challenges/opportunities/roadmap 可作为 A1-M6 候选发现 的写法样本。

### 6.2 风险

1. **不能把它当目标领域 evidence pool**：它是 LLM4SE SLR，不是 LLM4STM、控制系统状态机、formal verification 或 agentic SLR 目标语料。
2. **时间漂移很强**：论文收集截止日为 2024-01-31，且 LLM4SE 之后发展极快；任何“当前最新模型/任务格局”都必须重新核验。
3. **arXiv 占比高**：395 篇中大量是 arXiv，虽有质量评估，但不能简单等价为 peer-reviewed evidence。
4. **工业数据覆盖弱**：industrial datasets 仅少量出现，工业/安全关键系统外推需要降级。
5. **字段审计过程不足**：文章公开了 replication package，但正文未充分展示每个字段的双人编码、一致性、冲突解决和 schema drift 记录；Paper2 若主打 audit-first，应补强这部分。
6. **代码中心偏置**：分类轴高度围绕 code generation/repair/testing，对 requirements formalization、system design、state machine modeling、formal verification 的取值空间不足。
7. **artifact URL 有差异**：本地 metadata 与 paper text 的 GitHub 链接不同，不能在正式写作中不核验就引用。

## 7. 待复核

1. 人工打开 `paper.pdf` 核对 Fig. 1、Table 2--17、Appendix A--E 的版式和精确数值，尤其是数据库分项命中数与 task count 语义。
2. 核对 ACM final version 与 arXiv v6 的差异：本地 PDF 页眉 DOI 仍显示占位格式，但 `bibtex.bib` / `metadata.json` 已有正式 DOI。
3. 联网核验 replication package 的真实 URL、可访问性、license、文件结构，以及 `xinyi-hou/LLM4SE_SLR` 与 `security-pride/LLM4SE_SLR` 的关系。
4. 复核 QAC3 与二次研究纳排规则是否存在版本/表述歧义。
5. 若要在 Paper2 正文引用精确比例，应回到 PDF 或 artifact 表格确认分母：例如 374 篇显式说明 dataset、355 篇显式说明 input form、software development 的 paper count 与 task-instance count 差异。
6. A2a 若把该文纳入 `survey_of_surveys` 总账，应同步回填 `target_se_subfield=LLM4SE`、`challenge_action_pattern`、`artifact_anchor_pattern`，但不得改写为目标领域 finding。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__codex.md](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__codex.md)、[../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__claude.md](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__claude.md)、[../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__deepseek.md](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/llm4se-systematic-review.md](../../audits/a1dt-v2-19x3/adjudications/llm4se-systematic-review.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `llm4se-systematic-review` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是。按页码顺序逐段通读 §1 INTRODUCTION → §2 APPROACH（含 Table 2/3/4/5、Fig. 1）→ §3 RQ1（Fig. 4/5、Table 6）→ §4 RQ2（Fig. 6/7/8、Table 7/8）→ §5 RQ3（Fig. 9、Table 9）→ §6 RQ4（Fig. 10、Table 10/11/12）→ §7 Threats → §8 Challenges/Opportunities/Roadmap → §9 Conclusion → References 起始页 → Appendix A--E（Table 13/14/15/16/17）。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是，两文件均逐字段读完。 |
| 是否打开或核对 `paper.pdf` | 否。本轮仅基于 `paper_content.txt` 的页眉、Fig./Table 标号与正文交叉核验；复杂版面（如 Fig. 4 的 LLM 树状图细节）未做 PDF 视觉级核验，仍记为待复核。 |
| 原文类型 | SLR（Kitchenham-style；明确声明遵循 Kitchenham et al. [197,198] 方法学，§2 首段） |
| 被编码样本单位 | 原始研究（一篇被纳入的 LLM4SE research paper），最终 N=395。 |
| 样本数量 / 分母 | 主分母 N=395。子分母：N=374（显式说明 数据集）；N=355（显式说明 input form）；N=154（peer-reviewed）+ 241（arXiv）；按年 7/13/56/273/46（2020–2024.01）。 |
| 原生树类型 | 维度森林。根为 4 个 RQ，每个 RQ 各自展开一棵编码树（RQ1 模型、RQ2 数据、RQ3 优化与评价、RQ4 任务），通过 Table 5 的 8 项 data items 串联。 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | v2 已返修完成：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

---

### 1. 原文证据阅读说明

#### 1.1 已读文件与覆盖
- `bibtex.bib`：完整 13 行，含 DOI `10.1145/3695988`、journal=TOSEM、vol 33 no 8、pages 1--79、year 2024。
- `metadata.json`：完整 36 行；注意其 abstract 字段引用 artifact URL 为 `https://github.com/security-pride/LLM4SE_SLR`，与正文 §3.1 与 §7 footnote 6 的 `https://github.com/xinyi-hou/LLM4SE_SLR` **不一致**——这是 review.md 已点出的待核验事实，本轮再次确认。
- `review.md`：现有 440 行均已通读，含 A1-DT v2 维度树复原节；证据链已迁至 evidence_chain.md。
- `paper_content.txt`：4152 行全部已读，覆盖 79 页正文 + 5 个附录。

#### 1.2 仍需 PDF 版面核验
- Fig. 4 的层级树（70+ LLM 模型按 仅编码器（encoder-only） / 编码器-解码器（encoder-decoder） / 仅解码器（decoder-only） 三栏 + 年份纵轴的具体节点数）；
- Fig. 1 研究 identification 流程图各节点数（4618、51、218765、80611、5078、1172、810、594、382、5152、+13）的箭头连接（与正文叙述存在 5078 → 1172 vs 5078 → 594 等中间路径，需图形核验）；
- Table 11 / 12 的 baseline 列表与日期；
- Appendix Table 13--17 中 reference ID 是否与正文一致（其中 RQ2 §4.2 提到“Code 仓库 (9)”而 Table 7 写“Code 仓库 (9)”，但正文 §4.2 又写“Code 仓库 (3)”——这是叙述 vs Appendix 表格分母不一致，须 PDF 核对）。

#### 1.3 关键原文证据锚点（5–12 个）

| # | 锚点 | 位置 | 简要释义 |
|---|---|---|---|
| E1 | §1 Contributions 列表 + Table 1 | p.1:3 | 自我定位：第一个覆盖通用 LLM4SE 的 SLR；与 8 个先前 surveys 在 SE scope / 模型 scope / SLR 标记 / time frame / # papers 五维度比较。 |
| E2 | §2.1 RQ1--RQ4 段 | p.1:4 | 四个 RQ 的精确措辞与目标维度；Section 3--6 与 RQ 一一对应。 |
| E3 | §2.2 + Fig. 1 + Table 2/3 | p.1:4--6 | QGS 检索：6 venues（ICSE/ESEC-FSE/ASE/ISSTA/TOSEM/TSE）→ 4618 → 51 QGS；7 DB（IEEE/ACM/SD/WoS/Springer/arXiv/DBLP）→ 218,765；Inclusion 3 条 / Exclusion 9 条。 |
| E4 | §2.3.2 Table 4 + QAC scoring | p.1:7 | 10 QAC；QAC1--3 `-1/0/1`，QAC4--10 `0/1/2/3`；published 阈值 16.8/21（80%），arXiv 阈值 14.4/18（80%）。 |
| E5 | §2.4 Snowballing | p.1:8 | 382 初始 → forward 3,964 + backward 9,610（正文文本；Fig.1/合计疑似 9,601，待 A2a 核验）→ 去重 5,152 → +13 → 395。 |
| E6 | §2.5 Table 5 | p.1:9 | 8 项 extracted data items 各自绑定 RQ（1,2,3,4 / 1,2,3,4 / 1,4 / 2 / 3 / 3 / 4 / 4）。 |
| E7 | §3.1 + Fig. 4 + Table 6 | p.1:10--11 | 仅编码器（encoder-only） / 编码器-解码器（encoder-decoder） / 仅解码器（decoder-only） 三分法及对应典型 SE task。 |
| E8 | §3.2 Fig. 5 + 各年统计 | p.1:12--13 | 2020：8 篇 仅编码器（encoder-only）；2021：47.37% 仅解码器（decoder-only）；2022 涌现；2023：70.7% 仅解码器（decoder-only）；2024.01：64.17% 仅解码器（decoder-only）。 |
| E9 | §4.1 Fig. 6 + RQ2 Summary (1) | p.1:14--15, 20 | 数据源 4 类，分子分母明确：open-source 235、收集（收集） 98、构造（构造） 60、工业（industrial） 6；374 papers 显式声明 数据集 时 open-source 占 62.83%。 |
| E10 | §4.2 Table 7 + §4.4 Table 8 | p.1:16--19 | 数据类型 5 类（text 151 / code 103 / graph 1 / software-repo 20 / 组合类（组合类） 55）；input form 4 类（token 347/树-graph 5/pixel 1/混合（混合） 2），N=355 显式声明者中 token-based 97.75%。 |
| E11 | §5 + Fig. 9 + Table 9 | p.1:21--25 | tuning 类型清单 + 8 prompt techniques 频次 + 4 problem types × 指标 总表（生成（Generation） 338 instances, 分类 147, Recommendation 39, Regression 1）。 |
| E12 | §6.1 Fig. 10 + Table 10 + §6.2--§6.7 | p.1:26--40 | 6 SDLC 活动 × 85 specific SE tasks；problem type 分布（Gen 70.97%、Cls 21.61%、Rec 6.77%、Reg 0.65%）。 |
| E13 | §7 Threats | p.1:40--41 | 3 类 威胁（search omission、selection bias、经验研究（empirical） knowledge bias）及缓解。 |
| E14 | §8 Challenges & Opportunities & Roadmap | p.1:41--46 | applicability / generalizability / 评价 / interpretability 四类 挑战；opportunities 与 路线图 8 个方向（含 SE4LLM）。 |
| E15 | Appendix A--E Table 13--17 | p.1:72--79 | 字段 → primary-研究 reference 的完整 anchor 表，是该 SLR 的“证据账本”实体。 |

---

### 2. 样本单位与字段来源判定

1. **被纳入和逐项描述的对象**：单篇 LLM4SE 研究论文（原始研究，原始研究）。N=395，其中 154 来自 peer-reviewed venues，241 来自 arXiv 但经过同一 QAC 流程评估。
2. **是否存在系统检索 / 纳排 / 数据抽取 / 编码**：是。所有四项均显式：QGS-based 检索；§2.3.1 Inclusion 3 条 + Exclusion 9 条；§2.3.2 10 QAC + 80% 阈值；§2.5 Table 5 抽取表绑定 RQ。
3. **字段来源**：
   - 一级骨架：4 RQ（§2.1）；
   - 字段合同：Table 5 的 8 项 data items；
   - 分类法：RQ1 三分架构 [326]、RQ2 数据源四分法 + 数据类型五分法 + 输入形式四分法、RQ3 优化八分法 + 评价四问题类型、RQ4 SDLC 六阶段 + 85 specific task；
   - 源锚定：Appendix A--E（Table 13--17）把每一字段取值映射到 paper ID。
4. **RQ 与样本单位的关系**：RQ 是 模式 顶层分支（既是问题，也是字段族 — 一个 paper 在每个 RQ 下都被多维编码），不是“结果组织方式”。Table 5 把字段与 RQ 显式绑定（“服务 RQ1,2,3,4 的 SE task category” 等）。
5. **是否需要降级**：不按路线图 / 提案降级。该文是真正的系统综述，是后续主统计池候选；但当前证据链仍把多数证据标为 `not_verified`，A1 仅作 `schema_seed`，A2a 需要补精确页码、Fig./Table 号后再按证据等级裁决，才能进入最终定量统计。

---

### 3. 原生样本编码维度树（维度森林）

样本单位 = `primary_study`（1 个 paper = 1 个编码样本），下挂 4 个 RQ 子树 + 1 个 bibliographic / search-and-selection 元数据子树。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[根节点] 原始研究（原始研究；首次术语；N=395）
├── [meta-A] 书目信息元数据
│   ├── 发表源短名（原文缩写保留）：{ICSE, ESEC/FSE, ASE, ISSTA, TOSEM, TSE, SANER, ICSME, EMNLP, ICML, ICPC, NeurIPS, arXiv, 其他（Others）}（Fig. 2a）
│   ├── 发表年份：2020 | 2021 | 2022 | 2023 | 2024（Fig. 2b: 7/13/56/273/46）
│   ├── 是否同行评审：布尔值；154 peer-reviewed vs 241 arXiv
│   └── 质量评分：published 取值 0..21，arXiv 取值 0..18；阈值 80%
├── [meta-B] 检索与筛选来源链
│   ├── 手工检索发表源：6 个 SE 顶级发表源 → 4618 → 51 QGS
│   ├── 自动检索数据库（原文库名保留）：IEEE Xplore / ACM DL / ScienceDirect / WoS / Springer / arXiv / DBLP → 218,765
│   ├── 纳排阶段：阶段 1..6 filter 计数 = 80,611 → 5,078 → 1,172 → 810 → 594 → 382
│   └── 滚雪球来源：{initial, forward, backward, +13}
├── [RQ1] 使用的 LLM（原标识：llm_employed）
│   ├── 架构：{仅编码器（encoder-only）、编码器-解码器（encoder-decoder）、仅解码器（decoder-only）}；Fig. 4 / Table 6
│   ├── 模型族：70+ 命名实例，每个实例附使用论文计数；高频例包括 ChatGPT 72、Codex 62、GPT-4 53、GPT-3.5 54、BERT 50、CodeBERT 51、CodeT5 46、CodeGen 44、T5 20
│   ├── 参数规模是否声明：数值或 未声明（not declared）
│   ├── 任务适配：{理解（理解）、生成（生成）、理解 + 生成（理解 + 生成）}；Table 6
│   └── 年份 × 架构实例计数：见 Fig. 5
├── [RQ2] 数据集处理（数据集 handling）
│   ├── 数据来源：{开源（开源）235、收集（收集）98、构造（构造）60、工业（industrial）6}；Fig. 6
│   ├── 数据类型：文本类（文本类）151、代码类（代码类）103、图类（图类）1、软件仓库类（软件仓库类）20、组合类（组合类）55；Table 7 / Appendix A
│   ├── 文本预处理流水线：抽取（抽取）→ 初始分段（初始分段）→ 删除不合格项（删除不合格项）→ 文本预处理（文本预处理）→ 删除重复项（删除重复项）→ 分词（分词）→ 分段（分段）；Fig. 7
│   ├── 代码预处理流水线：抽取（抽取）→ 删除不合格项（删除不合格项）→ 删除重复项（删除重复项）→ 编译（编译）→ 删除不可编译项（删除不可编译项）→ 代码表示（代码表示）→ 分段（分段）；Fig. 8
│   └── 输入形式：基于词元（基于词元）347、基于树 / 图（树 / 图类）5、基于像素（pixel based）1、混合（混合）2；分母 = 355 个显式说明者，Table 8 / Appendix B
├── [RQ3] 优化与评价（optimization and 评价）
│   ├── 调优技术：全量微调（full_fine_tuning）83、上下文学习（ICL）、PEFT.LoRA 8、PEFT 提示调优（prompt tuning） 3、PEFT 前缀调优（prefix tuning） 2、PEFT 适配器调优（adapter tuning）、强化学习（RL）、监督微调（SFT）等
│   ├── 提示工程：少样本（few_shot）88、零样本（zero_shot）79、思维链（CoT）18、自动提示工程（APE）2、代码链（CoC）2、自动思维链（Auto_CoT）1、MoT 1、SCoT 1、其他（Others）76；Fig. 9 / Appendix C
│   └── 评价指标按问题类型分组：回归（回归）1 项；分类（分类）9 项共 147 个实例；推荐（推荐）6 项共 39 个实例；生成（生成）19 项共 338 个实例；Table 9 / Appendix D
└── [RQ4] 软件工程任务（se_task）
    ├── 软件生命周期活动：需求工程（requirements engineering）17、软件设计（software design）4、软件开发（software development）247、软件质量保障（software quality assurance）66、软件维护（software maintenance）99、软件管理（software management）3；Fig. 10a / Table 10 / Appendix E
    ├── 具体 SE 任务：85 个开放命名；低频但本仓库相关项包括规约形式化（specification formalization）、验证（verification）、追踪自动化（traceability automation）等
    └── 问题类型：{生成（生成）、分类（分类）、推荐（推荐）、回归（回归）}；Fig. 10b
```

**取值空间类型标注**：详见 §4 叶子维度表的“取值空间类型”列。

> 说明：A1-M0--M6 的“通用六叶”（scope/语料/分类法/方法/证据/发现）是 Paper2 跨论文投影接口，与上面的原生森林**不是同一层**；当前复原应优先保留本文自己的细粒度森林，并把通用六叶降为附属投影。

---

### 4. 叶子维度表（聚焦原文叶子，按 RQ 分组）

只挑取值空间封闭或可量化的核心叶子；自由文本叶子从略以保篇幅。表头按任务要求。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf.architecture | LLM 架构 | RQ1 | Table 5 (item 2 "category of LLM") + §3.1 + Table 6 | 论文中使用的 LLM 的 Transformer 骨架类别 | {仅编码器（encoder-only）、编码器-解码器（encoder-decoder）、仅解码器（decoder-only）} | 完整枚举 | 不区分 → `unspecified` | architecture × year × task 交叉表 | 架构选择漂移、生成-task–decoder 亲和 | E7, E8, Fig. 4/5, Table 6 | 仅 LLM4SE 取值空间；迁移到 LLM4STM 需保留同一枚举 |
| leaf.model_family | LLM 模型族 | RQ1 | Fig. 4 / §3.1 / 复现包 | 论文使用的具体 LLM 实例族 | 70+ 实例（BERT/CodeBERT/T5/GPT-x/ChatGPT/Codex/LLaMA/...） | 开放枚举（高频集合 + 长尾） | 多模型同存 → 多值；未声明 → `unknown` | per-模型 频次 / Top-N | 模型 adoption 趋势、商业 vs 开源比例 | E7, Fig. 4 | 模型实例对时间漂移强，迁移须重报当年 list |
| leaf.parameter_size | 参数规模 | RQ1 | Table 5 (item 3) / 复现包 | 论文中声明的 LLM 参数数量 | numeric (M/B) ∪ {未声明（not declared）} | 数值或 `未声明（not declared）` | 占比可统计 | size vs task fit | 大模型对生成任务的偏置 | §3.1 footnote, Table 1 | 跨研究 size 定义不一致，注意区分 base/instruct/chat |
| leaf.data_source | 数据来源 | RQ2 | §4.1 / Fig. 6 / Table 5 (item 4) | 训练 / 评测数据集的获取方式 | {开源（开源）, 收集（收集）, 构造（构造）, 工业（industrial）} | 完整枚举 | 多源 → 多值；未声明 → 不计入 374 | 4 类频次（235/98/60/6） + 学术-工业 缺口（gap） | 工业数据集缺口 警示 | E9, §4.1 | 仅 LLM4SE 当前观察；safety-critical 子域可能 工业（industrial） > 开源（开源） |
| leaf.data_type | 数据类型 | RQ2 | §4.2 / Table 7 / Appendix A Table 13 | 数据载体形态 | {文本类（文本类）, 代码类（代码类）, 图类（图类）, 软件仓库类（软件仓库类）, 组合类（组合类）} 含 60+ 子类 | 层级枚举 | 多类型 → 多值 | 类型 × architecture × task 交叉 | graph/multimodal 低覆盖 | E10, Table 7/13 | 子类枚举对当前 SE 任务定制，迁移到 STM 需扩展（如 timed-trace、TA 模型） |
| leaf.preprocess_step | 预处理步骤 | RQ2 | §4.3 / Fig. 7/8 | 数据流水线步骤集合 | text: 7 步序列；code: 7 步序列（含 编译/删除不可编译项/code-representation） | 序列（顺序可变） | 步骤缺失 → 标 `omitted` | 共同步骤频次（抽取/dup deletion/分段 等） | 复现可靠性 | E10, Fig. 7/8 | text vs code 步骤名同，但语义不同；迁移须分支 |
| leaf.input_form | 输入形式 | RQ2 | §4.4 / Table 8 / Appendix B Table 14 | LLM 输入的模态/结构 | {基于 token（token_based）(text/code/code&text), 树_based, 图类（图类）, 基于像素（基于像素）, 混合（混合）} | 层级枚举 | 未声明 → 不计入 355 | 形态分布、树/graph adoption 趋势 | 树/graph 仍小众 | E10, Table 8/14 | 取值空间是当前主流 LLM 假设；状态机相关结构可作为 混合（混合）/树 子叶 |
| leaf.tuning | 调优技术 | RQ3 | §5.1 / Table 5 (item 5) | 模型适配方法 | {全量微调（完整 fine-tuning）, ICL, PEFT.LoRA, PEFT 提示调优（prompt tuning）, PEFT 前缀调优（prefix tuning）, PEFT 适配器调优（adapter tuning）, RL, SFT, syntax_FT, knowledge_preservation_FT, task_oriented_FT, ...} | 开放层级枚举 | 仅使用预训练 → `无更新 / 仅推理（inference only）` | 各方法频次（全量微调（完整 fine-tuning） 83, LoRA 8, ...） | PEFT 兴起、完整 FT 仍主导某些子族（BERT 系列） | §5.1 | LLM4SE 当前观察；safety-critical 域可能偏 fine-tune 而非 ICL |
| leaf.prompt | Prompt 工程技术 | RQ3 | §5.2 / Fig. 9 / Appendix C Table 15 | 推理时 prompt 设计策略 | {少样本（few_shot）, 零样本（zero_shot）, CoT, APE, CoC, Auto_CoT, MoT, SCoT, 其他（Others）} | 完整枚举 + 其他（Others） 漏斗 | 不适用（不适用）（only fine-tuning） | 8 类 + 其他（Others） 频次（88/79/18/2/2/1/1/1/76） | CoT / SCoT 在代码任务的兴起 | E11, Fig. 9 | prompt 命名为 LLM4SE 自创/借用混合；迁移须保留 “Others=76” |
| leaf.metric_by_problem_type | 评价指标 × 问题类型 | RQ3 | §5.3 / Table 9 / Appendix D Table 16 | 评估时使用的量化指标，按问题类型分组 | 回归 {MAE}; 分类 {Prec, 召回率, F1, Acc, AUC, ROC, FPR, FNR, MCC}; 推荐 {MRR, Prec@k, MAP@k, F@k, 召回率@k, Acc}; 生成 {BLEU 系, Pass@k, EM, CodeBLEU, ROUGE 系, METEOR, Edit Similarity, ChrF, CrystalBLEU, CodeBERTScore, MFR, PP, ...} | 关系值（problem_type × metric_set） | 单指标论文 → 单值；多指标 → 集合 | 指标 数 × problem_type 交叉表 | 评价 指标 过于代码中心、与“能力”脱钩 | E11, Table 9/16 | Pass@k / CodeBLEU 等仅生成代码语义有效；迁移到 STM/形式化任务须重选 指标 set |
| leaf.sdlc_phase | 软件生命周期活动 | RQ4 | §6.1 / Fig. 10a / Table 10 / Appendix E Table 17 | 任务所属软件生命周期阶段 | {需求工程、软件设计、软件开发、软件质量保障、软件维护、软件管理} | 完整枚举（6 类） | 任务跨阶段时记为多值（少数） | 按本行枚举顺序：需求工程 3.90%、软件设计 0.92%、软件开发 56.65%、软件质量保障 15.14%、软件维护 22.71%、软件管理 0.69% | 需求工程 / 设计 / 管理严重低覆盖；形式化验证仅 5 篇 | E12, Fig. 10a, Table 10 | 仅 LLM4SE 当前观察；不能作为 LLM4STM 的饱和度结论 |
| leaf.specific_task | 具体 SE 任务 | RQ4 | §6.2--§6.7 / Table 10 / Appendix E Table 17 | 论文针对的具体 SE 任务 | 85 个开放命名（code_生成 118 / program_repair 35 / code_completion 22 / ... / specification_formalization 1 / verification 5 / traceability_automation 1） | 开放层级枚举 | 多任务论文 → 多值 | 任务级频次、Top-N | 与本仓库相关：specification_formalization、verification、requirements 任务低频 | E12, Table 10/17 | 命名规范借用 LLM4SE 既有词汇；迁移到 control-system / STM 须显式扩展 |
| leaf.problem_type | 问题类型 | RQ4 | §6.1 / Fig. 10b / Table 5 (item 7) | 任务的形式化求解类型 | {生成（生成）、分类（分类）、推荐（推荐）、回归（回归）} | 完整枚举（4 类） | 多类型混合 → 多值 | 4 类分布（70.97/21.61/6.77/0.65%） | 生成类问题过度主导；回归 极稀疏 | E12, Fig. 10b | 这一抽象层是 ML 通用，可迁移；与 指标 set 强耦合 |

（关于 venue、qac_score、search 阶段分母等 meta 字段，叶子定义与上类似，限于篇幅省略。）

---

### 5. 关系边表

该文确实建立了若干显式 模式 内关系（不是因果，而是字段-字段映射）。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge.architecture_task | leaf.architecture | 适用于（suited_for） | leaf.specific_task / leaf.problem_type | 仅编码器（encoder-only） ↔ 理解 任务（Code Understanding, Bug Localization, Vulnerability Detection）；编码器-解码器（encoder-decoder） ↔ Code Summarization / Translation / Program Repair；仅解码器（decoder-only） ↔ Code 生成（Generation） / Completion / Test Case 生成（Generation） | 论文未声明 → `未报告` | §3.1 Table 6 | architecture × task 适配性 |
| edge.architecture_year | leaf.architecture | 按年份计频（frequency_in_year） | meta-A.publication_year | 按数值统计 (arch × year) | 0 | §3.2 Fig. 5；2020:8/0/0、2021:8/2/9、2022:52/17/73、2023:94/85/432、2024:19/24/77 | architecture 趋势漂移 |
| edge.task_architecture_distribution | leaf.specific_task | 使用架构（uses_architecture） | leaf.architecture | 分布计数 (多对多) | 未报告 | 复现包 + Appendix（隐含） | 任务–架构亲和 |
| edge.problem_metric | leaf.problem_type | 由指标评价（evaluated_by） | leaf.metric_by_problem_type | 指标 按问题类型分组的指标集合（详见 Table 9 / 16） | 回归 仅 1 指标 → 取值空间稀疏 | E11, Table 9 | 评价合同：哪些 指标 服务哪类问题 |
| edge.datatype_preprocess | leaf.data_type | 使用流水线（uses_pipeline） | leaf.preprocess_step | text → Fig. 7 流水线；code → Fig. 8 流水线 | 组合类（组合类） / graph / repo → 复合或不适用 | Fig. 7/8 | 数据-预处理绑定 |
| edge.task_sdlc | leaf.specific_task | 属于阶段（is_in_phase） | leaf.sdlc_phase | 85 task 严格归属 1 个 SDLC（极少跨阶段） | -- | Table 10 / Appendix E Table 17 | 任务-阶段映射、覆盖度评估 |
| edge.tuning_model | leaf.tuning | 应用到（applied_to） | leaf.model_family | 关系值（如 LoRA → {StarCoder, LLaMA, CodeT5+, ...}） | 未报告 | §5.1 案例段落 | 哪些 tuning 适合哪些族 |
| edge.rq_fields | meta-RQ index | 抽取字段（extracts） | Table 5 的 8 个 data items | RQ → field 多对多 | -- | Table 5 | RQ-字段合同（字段模式（field 模式） 服务 RQ） |
| edge.paper_anchor | leaf.data_type / leaf.input_form / leaf.prompt / leaf-指标 / leaf.specific_task | 拥有证据论文（has_evidence_papers） | reference ID 集合 | 每个取值附 paper ID 列表 | -- | Appendix A--E Table 13/14/15/16/17 | source-anchor：从字段值跳回 原始研究 |

---

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段 / 统计表支撑的统计观察（可作为 Paper2 模式池 / 投影分析候选）
- O1：395 篇中 154 peer-reviewed、241 arXiv；arXiv 占比 61.0%（E3, E5）。
- O2：架构选择漂移：2020 仅编码器（encoder-only） 主导 → 2021 仅解码器（decoder-only） 已 47.4% → 2023 仅解码器（decoder-only） 70.7% → 2024.01 仅解码器（decoder-only） 64.17%（E8）。
- O3：数据集 source 严重不均：工业（industrial） 仅 6 / 374 ≈ 1.6%（E9）。
- O4：input form：token-based 占 97.75%；树/graph 占 1.4%；pixel 约 0.28%，hybrid 2/355≈0.56%（Table 8 与正文存在 tree/graph、pixel、hybrid 口径冲突，A2a 前只作候选）。
- O5：SDLC 严重不均：development+maintenance ≈ 79.4%；RE+design+management ≈ 5.5%；verification 仅 5 篇（E12）。
- O6：problem type 严重偏 生成（70.97%），回归 极稀疏（0.65%）（E12）。
- O7：指标 集中度高：分类 总 instances 147、生成 总 instances 338、推荐 总 instances 39、回归 总 instances 1（E11）。

#### 6.2 原文 discussion / 路线图 提出的“候选发现”（仅可作候选，须研究者裁决再升级）
- C1：under-explored SE phases (RE / design / management) 是机会窗口。
- C2：工业数据集缺口 提示学界与产业之间存在错位。
- C3：评价指标体系不足以覆盖 interpretability / robustness / safety 等质性维度。
- C4：Collaborative LLMs / multi-LLM / multimodal input 是潜在方向。
- C5：SE4LLM 反向研究方向新出现。
- C6：formal verification × LLM 仍是早期方向（仅 5 篇 verification，1 篇 specification_formalization；引 Charalambous 2023）。

#### 6.3 对 Paper2 可迁移的“方法学启发”
- M1：**Table 5 范式**——每个抽取字段必须显式服务至少 1 个 RQ；Paper2 可以把这条提升为字段合同。
- M2：**QGS 脚手架**——高置信顶级 venue → 51 篇 → 关键词族 → DB 检索 → 多阶段 filter → QAC。
- M3：**Appendix-as-source-anchor**——把每个分类取值附上 paper ID 清单（Table 13--17 范式），即 模式 与 原始研究 之间存在可审计回链。
- M4：**RQ-级 summary box**——每 RQ 末尾 3 条总结，用于把统计观察提升为候选发现。
- M5：**multi-architecture × year 矩阵**统计模式（Fig. 5）。
- M6：**problem_type × metric_set** 评价合同（Table 9）。

#### 6.4 绝不能迁移到 Paper2 目标领域的内容
- 任何 LLM4SE 具体频次、模型族占比、SDLC 分布百分比都**不能**作为 LLM4STM / 控制系统状态机 / formal verification × LLM 的领域结论；其取值空间和样本基础不同。
- 任何关于 specific_se_task 的命名清单（如 code_生成、program_repair 等）的“最优 LLM”结论（Tables 11, 12）都受限于论文收集截止日为 2024-01-31，且与本仓库目标 task 不直接对应。
- 制品 URL 不可作为既定事实引用（见 §1.1 关于 `xinyi-hou` vs `security-pride` 的差异）。

---

## survey_of_surveys 自身 schema 抽取

本节把该论文投影到本目录自己的脚手架综述 schema（S1--S8）。判定等级只说明该维度在原文和本地证据链中的可用程度：`强` = 有明确原文结构和证据锚点；`中` = 有可复用结构但存在范围、裁决或精核限制；`弱` = 只作边界启发或风险提示；`不适用` = 原文类型不支持该维度进入统计池。

| 维度 | 判定等级 | 一句话抽取结果 | 证据位置 |
|---|---|---|---|
| S1 综述任务设定 | 强 | 该文以 LLM4SE 为对象，设置 RQ1--RQ4 覆盖模型、数据、优化/评价和 SE 任务，并声明采用 Kitchenham-style SLR。 | `review.md` §2.1、§2.2、维度树复原 §0；`evidence_chain.md` A.2 `ev-llm4se-systematic-review-type` |
| S2 语料收集与筛选 | 强 | 语料覆盖 2017 年 1 月至 2024 年 1 月，论文收集截止日为 2024-01-31；经 QGS、7 个数据库检索、多阶段过滤、QAC 质量评估和 snowballing，最终纳入 395 篇。数据库分项命中数存在文本提取 / 图表合计差异，精确分项数待 PDF Fig.1 视觉核验。 | `review.md` §2.3、§2.4、维度树复原 §1.3；`evidence_chain.md` A.2 `ev-llm4se-systematic-review-denom`；`audits/a1-s1s8-19x1/adjudications/llm4se-systematic-review.md` |
| S3 原生维度树/样本编码对象 | 强 | 样本编码对象是一篇被纳入的 LLM4SE research paper/study；最终集合按 QAC3 目标上排除 secondary study，但 QAC3 与 survey/review 临时保留流程存在表述歧义，待 A2a 核验。原生结构是 4 个 RQ 展开的维度森林，并由 Table 5 的 8 项 data items 串联。 | `review.md` 维度树复原 §2、§3；`evidence_chain.md` A.3 `clm-llm4se-systematic-review-unit`、`clm-llm4se-systematic-review-tree`；`audits/a1-s1s8-19x1/adjudications/llm4se-systematic-review.md` |
| S4 字段级证据 | 强 | 字段级证据由 Table 5 定义字段合同，并通过 Appendix A--E 将 data type、input form、prompt、metric、SE task 等取值回链到 primary-study references。 | `review.md` §2.5、§2.7、维度树复原 §4、§5；`evidence_chain.md` A.2 `ev-llm4se-systematic-review-tree` |
| S5 维度模式演化 | 中 | RQ/字段形成参考 Kitchenham 与前序 DL4SE 综述，并在 full-text review 中抽取 Table 5 字段；原文未暴露 open coding、schema revision history 或 conflict log。 | `review.md` §2.5、§2.8、维度树复原 §6.1、§6.3；`evidence_chain.md` A.3 `clm-llm4se-systematic-review-tree` |
| S6 统计分析 | 强 | 该文提供 N=395 主分母、数据源/输入形式子分母、架构年度趋势、SDLC 阶段分布、problem type 与 metric 分布。 | `review.md` §2.6、维度树复原 §0、§4、§6.1；`evidence_chain.md` A.2 `ev-llm4se-systematic-review-denom` |
| S7 候选 finding | 强 | 原文将统计观察提升为 challenges、opportunities 与 roadmap；对 Paper2 只迁移 finding 生成模式，不迁移 LLM4SE 领域结论。 | `review.md` §3、§6.1--§6.2、维度树复原 §6.2--§6.4；`evidence_chain.md` A.3 `clm-llm4se-systematic-review-pool` |
| S8 研究者/作者质疑与裁决 | 中 | 该文有 QAC、两名 reviewers secondary review、threats 和 replication package 作为质量控制机制，但缺少字段级 coder agreement 与冲突解决日志。 | `review.md` §2.4、§2.8、§6.2、维度树复原 §1.3；`evidence_chain.md` A.3 `clm-llm4se-systematic-review-pool` |

### S1--S8 四分栏证据拆分

#### 总体统计池裁决

裁决：**后续主统计池候选，但当前仅按 `schema_seed` 使用；A2a 完成页码、表图、ACM final 与 replication package 精核前，不进入最终定量统计或目标领域 finding。** 该文是 Kitchenham-style LLM4SE SLR，原文明确分析 2017-01 至 2024-01 的 395 篇 LLM4SE research papers，具备系统检索、纳排、QAC、snowballing、RQ-字段表与大量分布统计；但它的领域是 LLM4SE，不是 LLM4STM / 控制系统状态机 / formal verification × LLM，因此只能贡献“SE SLR 如何构造维度树、字段证据和候选 finding”的方法模式，不能把 LLM4SE 频次或路线图外推为本仓库目标领域结论。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要与 §2.1 声明回答 RQ1--RQ4：LLM、数据、优化/评价、SE tasks；§2 开头声明 follows Kitchenham et al. methodology。 | 复原为“LLM4SE 综合 SLR”的顶层任务树：RQ1 模型、RQ2 数据、RQ3 优化/评价、RQ4 SE 任务。 | **合格候选**：可作为 SLR 任务设定与 RQ-field contract 的统计池样本；不作为目标领域 evidence pool。 | 核对 ACM final 与本地 arXiv v6 在 RQ 表述、出版日期、页码上的差异。 |
| S2 语料收集与筛选 | Fig.1/§2.2--§2.4：QGS、6 个 SE venue、7 个数据库、218,765 初始候选、QAC 后 382、snowballing 补 13、最终 395；截止日 2024-01-31。 | 复原为完整分母链：manual search / automated search / filtering / QAC / snowballing；样本单位为一篇 LLM4SE research paper。 | **合格候选**：分母链足以进入后续统计池；当前只记录候选资格。 | PDF 视觉核验 Fig.1 数据库分项数；核对 ScienceDirect 正文 62,290 与 Fig.1/合计疑似 65,290 的差异；确认 QGS 手工检索分母 4,618/图中阶段数。 |
| S3 原生维度树/样本编码对象 | Table 5 把 8 个 extracted data items 绑定 RQ；正文和附录按模型、数据、优化/评价、任务组织 395 篇。QAC3 要求 “not a secondary study”，但正文又称 systematic views/survey/review papers 会保留到质量评估阶段。 | 复原为 4 个 RQ 子树 + bibliographic/search meta 的维度森林；编码对象是 primary study / research paper，而非二次研究本身。 | **合格候选但带 caveat**：S3 可入统计池；secondary-study 纳排边界需标注。 | A2a 核验 QAC3 与 “retained systematic views/survey/review papers” 是否导致最终 395 中混入 secondary study；必要时在总账中加 “primary-study intended” 限定。 |
| S4 字段级证据 | Table 5 定义抽取字段；Appendix A--E / Tables 13--17 为 data type、input form、prompt、metric、SE task 等提供 study references；正文 footnote 给 replication package。 | 字段级证据链较强：字段合同 → 取值统计 → appendix reference list → replication package。 | **合格候选**：可作为 source-anchor / appendix-as-evidence 模式样本。 | 必须核验 replication package URL：paper text 为 `xinyi-hou/LLM4SE_SLR`，metadata abstract 为 `security-pride/LLM4SE_SLR`；核验 license、文件结构、与 ACM final 的 artifact 声明一致性。 |
| S5 维度模式演化 | §7 threats 称 RQ 与分类参考 DL4SE 等前序综述，并在每个 RQ 前阅读相关文献以预定义 categories；但原文未给 open coding、schema revision history、coder agreement 或 conflict log。 | 复原为“预定义分类 + full-text review 抽取”的模式演化，证据弱于字段结果本身。 | **降为中等资格**：可用于统计“是否报告 schema 来源/演化”的字段，但不能统计为已公开完整编码过程。 | 建议修正任何“字段审计过程充分公开”的强表述；A2a 查 replication package 是否有编码表、版本记录、冲突处理记录。 |
| S6 统计分析 | §2.5、§3--§6 与 Fig.2--10 / Tables 6--17 给出 N=395、154 peer-reviewed + 241 arXiv、年度分布、架构、数据源、输入形式、prompt、metric、SDLC/task/problem type 等统计。 | 复原为多个可计数字段叶：architecture、data_source、input_form、prompt、metric_by_problem_type、sdlc_phase、specific_task、problem_type。 | **合格候选**：适合后续统计池抽取字段分布；当前不得把 LLM4SE 数值外推为 LLM4STM 结论。 | 精核所有比例与分母：N=374 dataset、N=355 input form、task-instance vs paper count；ACM final 表图页码与 arXiv v6 是否一致。 |
| S7 候选 finding | §8 将统计观察组织为 challenges、opportunities 与 roadmap，例如 SE phase 覆盖不均、工业数据缺口、评价框架需求、domain-specific challenges。 | 复原为“统计观察 → challenge/opportunity/roadmap”的 finding 生成路径；Paper2 只迁移生成模式，不迁移 LLM4SE 领域结论。 | **模式合格，领域 finding 降级**：可入方法模式池；不得进入目标领域 final finding。 | 建议在后续汇总中持续保留“LLM4SE-only”边界；A2a 核验 §8 finding 是否均有前文统计支撑，避免 roadmap prose 直接升级。 |
| S8 研究者/作者质疑与裁决 | §7 reports search omission、study selection bias、empirical knowledge bias；两位 SE/LLM reviewers secondary review；QAC 与 replication package 作为缓解措施。 | 复原为质量控制 / threat 树：QGS、纳排、QAC、secondary review、replication package、threat mitigation；但缺字段级 coder agreement。 | **中等资格**：可统计“是否有 QA/threat/replication package”，但不能统计为强审计型研究。 | A2a 核验 reviewer 角色、是否独立双人抽取、是否存在 inter-rater agreement；若 replication package 不含审计记录，应维持 S8=中而非强。 |

## 证据链入口

详见 [evidence_chain.md](./evidence_chain.md)；A.1--A.4 证据链与结论-证据映射已迁出，当前证据状态（如 `not_verified`、待 A2a、`schema_seed`）保持原样。
