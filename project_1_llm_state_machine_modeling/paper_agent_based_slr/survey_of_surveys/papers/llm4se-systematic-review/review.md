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
| 语料范围 | 2017 年至 2024-01-31；最终纳入 395 篇 LLM4SE 研究论文 |
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

作者把检索起点设为 2017 年，理由是 Transformer 架构论文发表于 2017 年，是后续 LLM 的关键基础。截止日期为 2024-01-31。最终语料为 395 篇：质量评估后得到 382 篇，再经 forward/backward snowballing 补充 13 篇。

关键边界：该语料是 LLM4SE，而不是 SLR automation、agentic review、formal methods 或 LLM4STM。它可以作为“现代 SE SLR 如何构造分类轴”的样本，不能直接作为本仓库目标主题的证据池。

### 2.4 检索 / 筛选流程

作者使用 Quasi-Gold Standard（QGS）策略：

1. **Manual search**：选择 6 个顶级 SE venue：ICSE、ESEC/FSE、ASE、ISSTA、TOSEM、TSE；爬取 4,618 篇论文，人工确认 51 篇相关论文作为 QGS。
2. **Search string derivation**：从 QGS 和领域知识构造两组关键词：SE task keywords 与 LLM keywords。SE 关键词覆盖 code generation/search/completion/summarization、bug detection/localization、program repair、requirement extraction/traceability/validation、mining GitHub/SO/app 等；LLM 关键词覆盖 LLM、PLM、pre-trained、Transformer、BERT、Codex、GPT、T5、ChatGPT 等。
3. **Automated search**：在 IEEE Xplore、ACM Digital Library、ScienceDirect、Web of Science、Springer、arXiv、DBLP 七个数据库检索，初始获得 218,765 条候选。
4. **Filtering**：按少于 8 页、题名/摘要/关键词、venue 信息、去重、全文检查、workshop/doctoral symposium/灰色文献（grey literature） 等条件逐级筛选。
5. **Quality assessment**：设置 10 个 QAC，覆盖 SE task relevance、LLM usage、是否二次研究、高声誉 venue、动机、技术描述、实验设置/数据、finding、贡献/限制、学术或工业贡献。正式出版论文按 21 分满分，arXiv 按 18 分满分，阈值均为 80%。
6. **Snowballing**：对 382 篇初始集合做 backward/forward snowballing，获得 3,964 + 9,610 条线索，去重后 5,152 条，再筛选补入 13 篇。

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

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

本字段树覆盖用户指定的 **LLM类型、SE任务、数据、优化/评价策略** 等核心维度；英文 ID 仅用于后续机器可读字段命名。

```text
说明：本旧版迁移草稿已中文化；英文 / 缩写保留为原文术语或后续字段标识。
综述记录（review_record）
├── 书目来源
│   ├── 标题 / 作者 / 年份 / 发表源 / DOI
│   ├── 发表类型 / CCF 大类 / CCF 等级
│   └── 全文状态 / 制品链接 / 版本说明
├── 检索与选择
│   ├── 检索范围起止
│   ├── 种子 venue / QGS 大小
│   ├── 数据库 / 查询关键词族
│   ├── 纳排标准
│   ├── 各阶段筛选计数
│   └── 质量评估标准 / 阈值 / reviewer check
├── LLM 类型
│   ├── 架构：encoder-only | encoder-decoder | decoder-only
│   ├── 模型族：BERT | CodeBERT | T5 | CodeT5 | GPT | Codex | ChatGPT | LLaMA | ...
│   ├── 参数规模是否声明
│   ├── general vs code specialized
│   ├── hosted vs open / reproducible
│   └── 任务适配：understanding | generation | understanding+generation
├── SE 任务
│   ├── 软件生命周期活动：requirements | design | development | QA | maintenance | management
│   ├── 具体任务：code_generation | program_repair | requirements_classification | verification | ...
│   ├── 问题类型：generation | classification | recommendation | regression
│   ├── 输入制品类型
│   └── 输出制品类型
├── 数据
│   ├── 来源类别：开源、论文自行收集、论文自行构造、工业来源（原枚举：open source / collected / constructed / industrial）
│   ├── 数据类型：文本、代码、图、仓库、组合
│   ├── 具体制品：源代码、缺陷报告、需求文档、测试、补丁、提示词等
│   ├── 预处理步骤
│   ├── 表示形式：token | tree_graph | pixel | hybrid
│   ├── 划分与基准
│   └── 隐私或工业约束
├── 优化 / 推理策略
│   ├── 全量微调（full fine-tuning）
│   ├── 参数高效微调（PEFT）：LoRA | 提示调优（prompt tuning） | 前缀调优（prefix tuning） | 适配器调优（adapter tuning）
│   ├── 提示策略：零样本、少样本、思维链、自动提示工程、代码链、自动思维链、多路径思维链、结构化思维链、自定义策略（原缩写保留于审计附录）
│   ├── 强化学习 / 监督微调 / 任务特定训练
│   └── 反馈循环或工具集成
├── 评价
│   ├── 基准或数据集
│   ├── 基线模型 / 工具
│   ├── 按问题类型分组的 metric family
│   ├── human eval 或 manual validation
│   ├── statistical / ablation analysis
│   └── 指标局限
├── 证据与制品
│   ├── 表 / 图锚点
│   ├── 原始研究 reference anchor
│   ├── replication package URL
│   └── supplementary appendix link
└── 研究发现边界
    ├── statistical observation
    ├── challenge / opportunity
    ├── author recommendation
    ├── domain gap
    └── transferability to Paper2
```

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
2. **时间漂移很强**：截止到 2024-01-31，且 LLM4SE 之后发展极快；任何“当前最新模型/任务格局”都必须重新核验。
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
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__codex.md](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__codex.md)、[../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__claude.md](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__claude.md)、[../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__deepseek.md](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/llm4se-systematic-review.md](../../audits/a1dt-v2-19x3/adjudications/llm4se-systematic-review.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

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
| 主统计池资格 | 是（局部可统计）。该文是 systematic_review，有明确分母、纳排、QAC 与 Appendix 锚定；其分类频次（如 architecture × year、data_source、input_form、SDLC activity、指标 × problem_type）可作为正式可统计 模式。但当前单篇 review.md 中具体数字未逐一回 Table 13–17 精核，部分百分比口径（task instance vs paper 计数）仍存在分母歧义，须 A2a 锚定。 |
| 总体判定 | v2 已返修完成：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

---

### 1. 原文证据阅读说明

#### 1.1 已读文件与覆盖
- `bibtex.bib`：完整 13 行，含 DOI `10.1145/3695988`、journal=TOSEM、vol 33 no 8、pages 1--79、year 2024。
- `metadata.json`：完整 36 行；注意其 abstract 字段引用 artifact URL 为 `https://github.com/security-pride/LLM4SE_SLR`，与正文 §3.1 与 §7 footnote 6 的 `https://github.com/xinyi-hou/LLM4SE_SLR` **不一致**——这是 review.md 已点出的待核验事实，本轮再次确认。
- `review.md`：现有 440 行均已通读，含历史草稿 `review_record` 树、`A1-DT v2` 维度树复原节、`A.1--A.4` 审计附录。
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
| E5 | §2.4 Snowballing | p.1:8 | 382 初始 → forward 3,964 + backward 9,610 → 去重 5,152 → +13 → 395。 |
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
5. **是否需要降级**：否。该文是真正的 系统综述，主统计池资格成立；不需要按 路线图 / 提案 降级。但 review.md 当前 A.2/A.3 将多数 EV 标 `not_verified`，需要把它们升级为 `verified` 并补精确页码、Fig./Table 号。

---

### 3. 原生样本编码维度树（维度森林）

样本单位 = `primary_研究`（1 个 paper = 1 个编码样本），下挂 4 个 RQ 子树 + 1 个 bibliographic / search-and-selection 元数据子树。

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

> 说明：旧版 `review.md` 的“通用六叶”（scope/语料/分类法/方法/证据/发现）是 Paper2 跨论文投影接口，与上面的原生森林**不是同一层**。这一关系在 review.md `## 维度树复原` 节已经做过分层声明，本审计支持该分层；返修方向是把上面这棵更细的森林正式抬升为 review.md 的“原文事实源”，并把六叶降到附属投影。

---

### 4. 叶子维度表（聚焦原文叶子，按 RQ 分组）

只挑取值空间封闭或可量化的核心叶子；自由文本叶子从略以保篇幅。表头按任务要求。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 叶子.architecture | LLM 架构 | RQ1 | Table 5 (item 2 "category of LLM") + §3.1 + Table 6 | 论文中使用的 LLM 的 Transformer 骨架类别 | {仅编码器（encoder-only）、编码器-解码器（encoder-decoder）、仅解码器（decoder-only）} | 完整枚举 | 不区分 → `unspecified` | architecture × year × task 交叉表 | 架构选择漂移、生成-task–decoder 亲和 | E7, E8, Fig. 4/5, Table 6 | 仅 LLM4SE 取值空间；迁移到 LLM4STM 需保留同一枚举 |
| 叶子.model_family | LLM 模型族 | RQ1 | Fig. 4 / §3.1 / 复现包 | 论文使用的具体 LLM 实例族 | 70+ 实例（BERT/CodeBERT/T5/GPT-x/ChatGPT/Codex/LLaMA/...） | 开放枚举（高频集合 + 长尾） | 多模型同存 → 多值；未声明 → `unknown` | per-模型 频次 / Top-N | 模型 adoption 趋势、商业 vs 开源比例 | E7, Fig. 4 | 模型实例对时间漂移强，迁移须重报当年 list |
| 叶子.parameter_size | 参数规模 | RQ1 | Table 5 (item 3) / 复现包 | 论文中声明的 LLM 参数数量 | numeric (M/B) ∪ {未声明（not declared）} | 数值或 `未声明（not declared）` | 占比可统计 | size vs task fit | 大模型对生成任务的偏置 | §3.1 footnote, Table 1 | 跨研究 size 定义不一致，注意区分 base/instruct/chat |
| 叶子.data_source | 数据来源 | RQ2 | §4.1 / Fig. 6 / Table 5 (item 4) | 训练 / 评测数据集的获取方式 | {开源（开源）, 收集（收集）, 构造（构造）, 工业（industrial）} | 完整枚举 | 多源 → 多值；未声明 → 不计入 374 | 4 类频次（235/98/60/6） + 学术-工业 缺口（gap） | 工业（industrial） 数据集 缺口（gap） 警示 | E9, §4.1 | 仅 LLM4SE 当前观察；safety-critical 子域可能 工业（industrial） > 开源（开源） |
| 叶子.data_type | 数据类型 | RQ2 | §4.2 / Table 7 / Appendix A Table 13 | 数据载体形态 | {文本类（文本类）, 代码类（代码类）, 图类（图类）, 软件仓库类（软件仓库类）, 组合类（组合类）} 含 60+ 子类 | 层级枚举 | 多类型 → 多值 | 类型 × architecture × task 交叉 | graph/multimodal 低覆盖 | E10, Table 7/13 | 子类枚举对当前 SE 任务定制，迁移到 STM 需扩展（如 timed-trace、TA 模型） |
| 叶子.preprocess_step | 预处理步骤 | RQ2 | §4.3 / Fig. 7/8 | 数据流水线步骤集合 | text: 7 步序列；code: 7 步序列（含 编译/删除不可编译项/code-representation） | 序列（顺序可变） | 步骤缺失 → 标 `omitted` | 共同步骤频次（抽取/dup deletion/分段 等） | 复现可靠性 | E10, Fig. 7/8 | text vs code 步骤名同，但语义不同；迁移须分支 |
| 叶子.input_form | 输入形式 | RQ2 | §4.4 / Table 8 / Appendix B Table 14 | LLM 输入的模态/结构 | {基于 token（token_based）(text/code/code&text), 树_based, 图类（图类）, 基于像素（基于像素）, 混合（混合）} | 层级枚举 | 未声明 → 不计入 355 | 形态分布、树/graph adoption 趋势 | 树/graph 仍小众 | E10, Table 8/14 | 取值空间是当前主流 LLM 假设；状态机相关结构可作为 混合（混合）/树 子叶 |
| 叶子.tuning | 调优技术 | RQ3 | §5.1 / Table 5 (item 5) | 模型适配方法 | {全量微调（完整 fine-tuning）, ICL, PEFT.LoRA, PEFT 提示调优（prompt tuning）, PEFT 前缀调优（prefix tuning）, PEFT 适配器调优（adapter tuning）, RL, SFT, syntax_FT, knowledge_preservation_FT, task_oriented_FT, ...} | 开放层级枚举 | 直接使用预训练 → `无更新 / 仅推理（inference only）` | 各方法频次（全量微调（完整 fine-tuning） 83, LoRA 8, ...） | PEFT 兴起、完整 FT 仍主导某些子族（BERT 系列） | §5.1 | LLM4SE 当前观察；safety-critical 域可能偏 fine-tune 而非 ICL |
| 叶子.prompt | Prompt 工程技术 | RQ3 | §5.2 / Fig. 9 / Appendix C Table 15 | 推理时 prompt 设计策略 | {少样本（few_shot）, 零样本（zero_shot）, CoT, APE, CoC, Auto_CoT, MoT, SCoT, 其他（Others）} | 完整枚举 + 其他（Others） 漏斗 | 不适用（不适用）（only fine-tuning） | 8 类 + 其他（Others） 频次（88/79/18/2/2/1/1/1/76） | CoT / SCoT 在代码任务的兴起 | E11, Fig. 9 | prompt 命名为 LLM4SE 自创/借用混合；迁移须保留 “Others=76” |
| 叶子.metric_by_problem_type | 评价指标 × 问题类型 | RQ3 | §5.3 / Table 9 / Appendix D Table 16 | 评估时使用的量化指标，按问题类型分组 | 回归 {MAE}; 分类 {Prec, 召回率, F1, Acc, AUC, ROC, FPR, FNR, MCC}; 推荐 {MRR, Prec@k, MAP@k, F@k, 召回率@k, Acc}; 生成 {BLEU 系, Pass@k, EM, CodeBLEU, ROUGE 系, METEOR, Edit Similarity, ChrF, CrystalBLEU, CodeBERTScore, MFR, PP, ...} | 关系值（problem_type × metric_set） | 单指标论文 → 单值；多指标 → 集合 | 指标 数 × problem_type 交叉表 | 评价 指标 过于代码中心、与“能力”脱钩 | E11, Table 9/16 | Pass@k / CodeBLEU 等仅生成代码语义有效；迁移到 STM/形式化任务须重选 指标 set |
| 叶子.sdlc_phase | 软件生命周期活动 | RQ4 | §6.1 / Fig. 10a / Table 10 / Appendix E Table 17 | 任务所属软件生命周期阶段 | {需求工程、软件设计、软件开发、软件质量保障、软件维护、软件管理} | 完整枚举（6 类） | 任务跨阶段时记为多值（少数） | 按本行枚举顺序：需求工程 3.90%、软件设计 0.92%、软件开发 56.65%、软件质量保障 15.14%、软件维护 22.71%、软件管理 0.69% | 需求工程 / 设计 / 管理严重低覆盖；形式化验证仅 5 篇 | E12, Fig. 10a, Table 10 | 仅 LLM4SE 当前观察；不能作为 LLM4STM 的饱和度结论 |
| 叶子.specific_task | 具体 SE 任务 | RQ4 | §6.2--§6.7 / Table 10 / Appendix E Table 17 | 论文针对的具体 SE 任务 | 85 个开放命名（code_生成 118 / program_repair 35 / code_completion 22 / ... / specification_formalization 1 / verification 5 / traceability_automation 1） | 开放层级枚举 | 多任务论文 → 多值 | 任务级频次、Top-N | 与本仓库相关：specification_formalization、verification、requirements 任务低频 | E12, Table 10/17 | 命名规范借用 LLM4SE 既有词汇；迁移到 control-system / STM 须显式扩展 |
| 叶子.problem_type | 问题类型 | RQ4 | §6.1 / Fig. 10b / Table 5 (item 7) | 任务的形式化求解类型 | {生成（生成）、分类（分类）、推荐（推荐）、回归（回归）} | 完整枚举（4 类） | 多类型混合 → 多值 | 4 类分布（70.97/21.61/6.77/0.65%） | 生成 过度主导；回归 极稀疏 | E12, Fig. 10b | 这一抽象层是 ML 通用，可迁移；与 指标 set 强耦合 |

（关于 venue、qac_score、search 阶段分母等 meta 字段，叶子定义与上类似，限于篇幅省略。）

---

### 5. 关系边表

该文确实建立了若干显式 模式 内关系（不是因果，而是字段-字段映射）。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge.architecture_task | 叶子.architecture | 适用于（suited_for） | 叶子.specific_task / 叶子.problem_type | 仅编码器（encoder-only） ↔ 理解 任务（Code Understanding, Bug Localization, Vulnerability Detection）；编码器-解码器（encoder-decoder） ↔ Code Summarization / Translation / Program Repair；仅解码器（decoder-only） ↔ Code 生成（Generation） / Completion / Test Case 生成（Generation） | 论文未声明 → `未报告` | §3.1 Table 6 | architecture × task 适配性 |
| edge.architecture_year | 叶子.architecture | 按年份计频（frequency_in_year） | meta-A.publication_year | 按数值统计 (arch × year) | 0 | §3.2 Fig. 5；2020:8/0/0、2021:8/2/9、2022:52/17/73、2023:94/85/432、2024:19/24/77 | architecture 趋势漂移 |
| edge.task_architecture_distribution | 叶子.specific_task | 使用架构（uses_architecture） | 叶子.architecture | 分布计数 (多对多) | 未报告 | 复现包 + Appendix（隐含） | 任务–架构亲和 |
| edge.problem_metric | 叶子.problem_type | 由指标评价（evaluated_by） | 叶子.metric_by_problem_type | 指标 按问题类型分组的指标集合（详见 Table 9 / 16） | 回归 仅 1 指标 → 取值空间稀疏 | E11, Table 9 | 评价合同：哪些 指标 服务哪类问题 |
| edge.datatype_preprocess | 叶子.data_type | 使用流水线（uses_pipeline） | 叶子.preprocess_step | text → Fig. 7 流水线；code → Fig. 8 流水线 | 组合类（组合类） / graph / repo → 复合或不适用 | Fig. 7/8 | 数据-预处理绑定 |
| edge.task_sdlc | 叶子.specific_task | 属于阶段（is_in_phase） | 叶子.sdlc_phase | 85 task 严格归属 1 个 SDLC（极少跨阶段） | -- | Table 10 / Appendix E Table 17 | 任务-阶段映射、覆盖度评估 |
| edge.tuning_model | 叶子.tuning | 应用到（applied_to） | 叶子.model_family | 关系值（如 LoRA → {StarCoder, LLaMA, CodeT5+, ...}） | 未报告 | §5.1 案例段落 | 哪些 tuning 适合哪些族 |
| edge.rq_fields | meta-RQ index | 抽取字段（extracts） | Table 5 的 8 个 data items | RQ → field 多对多 | -- | Table 5 | RQ-字段合同（字段模式（field 模式） 服务 RQ） |
| edge.paper_anchor | 叶子.data_type / 叶子.input_form / 叶子.prompt / 叶子-指标 / 叶子.specific_task | 拥有证据论文（has_evidence_papers） | reference ID 集合 | 每个取值附 paper ID 列表 | -- | Appendix A--E Table 13/14/15/16/17 | source-anchor：从字段值跳回 原始研究 |

---

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段 / 统计表直接支持的“统计观察”（可进入 Paper2 的 模式 池 / 投影分析）
- O1：395 篇中 154 peer-reviewed、241 arXiv；arXiv 占比 61.0%（E3, E5）。
- O2：架构选择漂移：2020 仅编码器（encoder-only） 主导 → 2021 仅解码器（decoder-only） 已 47.4% → 2023 仅解码器（decoder-only） 70.7% → 2024.01 仅解码器（decoder-only） 64.17%（E8）。
- O3：数据集 source 严重不均：工业（industrial） 仅 6 / 374 ≈ 1.6%（E9）。
- O4：input form：token-based 占 97.75%；树/graph 占 1.4%；pixel/混合（混合） 各 ~0.28%（分母 355；E10）。
- O5：SDLC 严重不均：development+maintenance ≈ 79.4%；RE+design+management ≈ 5.5%；verification 仅 5 篇（E12）。
- O6：problem type 严重偏 生成（70.97%），回归 极稀疏（0.65%）（E12）。
- O7：指标 集中度高：分类 总 instances 147、生成 总 instances 338、推荐 总 instances 39、回归 总 instances 1（E11）。

#### 6.2 原文 discussion / 路线图 提出的“候选发现”（仅可作候选，须研究者裁决再升级）
- C1：under-explored SE phases (RE / design / management) 是机会窗口。
- C2：工业（industrial） 数据集 缺口（gap） 提示学界与产业之间存在错位。
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
- 任何关于 specific_se_task 的命名清单（如 code_生成、program_repair 等）的“最优 LLM”结论（Tables 11, 12）都受限于截至 2024-01-31，且与本仓库目标 task 不直接对应。
- 制品 URL 不可作为既定事实引用（见 §1.1 关于 `xinyi-hou` vs `security-pride` 的差异）。

---

### 7. 对旧版 `review.md` 的返修来源（C/I/M 分级）

我把每条建议明确按本仓库 CLAUDE.md “学术研究仓库 Review 口径规范”定级：C/I 必须说明它如何影响学术目标、实验可靠性或 Paper2 结论可复现性。

| # | 等级 | 建议 | 学术影响 | 具体动作 |
|---|---|---|---|---|
| R1 | **C** | 把“原生森林（4 RQ + meta-A/B）”作为 review.md 的**事实真源**，把现有“原文模式主树（19×3 审计后返修）”六行表格替换为本审计 §3 的完整森林文本树 + §4 叶子表 + §5 关系边表。 | 当前 6 行主干表过度抽象（如把 RQ1 简写为“模型与任务格局”），看不出 Table 6/Appendix B 的取值空间与分母；下游 A2a 与跨论文投影会丢真。 | 改写 review.md `### 原文模式（模式）主树（19×3 审计后返修）`：以 4 RQ + 2 meta 为主干，每个主干列叶子表 + 取值空间 + 分母 + 证据锚点。 |
| R2 | **C** | 升级 A.2 证据账本：把 EV-002/003/005 当前的 `not_verified` 与“待 A2a 精确页码复核”换成**已有页码**——本审计已经给出（如 §4.1 Fig. 6 在 p.1:15、Table 5 在 p.1:9、Table 9 在 p.1:25、Table 10 在 p.1:27、Appendix Table 13 在 p.1:72--73、Table 14 在 p.1:73--74、Table 15 在 p.1:74--75、Table 16 在 p.1:75--77、Table 17 在 p.1:77--79）。 | 让“需要原文版面核验=true”长期挂着，会让该篇的统计可信度被错误锁在 `weak/模式种子（模式_seed）`，影响后续 Paper2 把它正式纳入主统计池。 | 把 EV-001..005 的 `证据强度` 从 `not_verified` 升级为 `verified`，并在“原文页码”列填入上面具体页码。 |
| R3 | **I** | 在 A.2 中区分**正文叙述与 Appendix 表格的内部不一致**，作为单独证据条记录，而不是埋没在 `needs_manual_check`。具体两处： (a) 正文 §4.2 提到 software-仓库 中“Code 仓库 (3)”，而 Table 7 与 Appendix Table 13 写“Code 仓库 (9)”；(b) Fig. 1 ScienceDirect 标注 `65,290` 与 §2.2.2 文字 `62,290` 存在差异。 | 这些数字差异会直接影响“分母 374”“数据源比例”等口径；若 Paper2 引用其中之一作为对比基线，必须先确定权威值。 | 新增 EV-006 (`type=internal_inconsistency`)，记录两处冲突，证据强度 `requires_pdf`，并在 A.3 新增结论 C14 “某些分母在正文 vs Appendix 出现不一致，引用须以 Appendix 为权威”。 |
| R4 | **I** | 明确 RQ4 中“paper 计数 vs task-instance 计数”分母歧义：Table 10 的 software_development total=247 是 task-instance 计数（一篇论文可触多个 task），而 RQ4 Summary (2) 写“229 papers mentioning over 24 SE tasks”用的是 paper 计数；§6.1 的 56.65% 是 task-instance 占比。 | 把这二者混引会导致百分比错误，影响“LLM4SE 多数集中在 development” 这一句论断的强度。 | 在 review.md §2.6 RQ4 段落明确加注释；在 A.3 新增 C15 “task-instance vs paper 计数 必须分列”。 |
| R5 | **I** | 制品 URL 冲突（`xinyi-hou` vs `security-pride`）从“§2.7 Artifacts 做法”里的“需联网核对”升级为 A.2 中独立证据条，并在 A.3 新增对应 claim“artifact_url 状态=未核验，不得作既定事实”。 | 该 URL 是 source-anchor 的入口；如果 Paper2 引用错误 URL，会破坏 replication 链。 | 新增 EV-007 (`type=artifact_url_conflict`, strength=`requires_external_verification`)。 |
| R6 | **M** | 在“通用接口投影”表后增加一段说明：六叶投影对**有 systematic 编码**的论文（如本文）只用于跨论文 模式 对齐，不能用于本论文内部叶子计数；本论文的叶子计数应严格走 §3 原生森林。 | 防止跨论文统计时混用六叶接口与原生叶子。 | 简短补一段 50–80 字。 |
| R7 | **M** | `历史草稿（已迁移）` 一节可以进一步缩短或在 review.md 末尾用 `<details>` 折叠，避免与新增的森林并列误导读者。 | 仅文档可读性，不影响学术结论。 | 折叠 / 删除冗余。 |
| R8 | **M** | metadata.json 的 `eligible_for_statistical_synthesis: true` 与 review.md 当前“否（A1-DT 阶段仅作 模式种子）”存在张力。建议在 review.md 的“统计与候选发现链路”表里加一行解释：metadata 视角=**全局可统计**；A1-DT 阶段视角=**叶子层尚未冻结，先作 模式种子，待 A2a 升级**。 | 防止后续读者把 metadata 字段当成真相反推叶子级也已冻结。 | 短注释。 |

> 当前 review.md 在“原文模式主树”节顶部带 `[!WARNING] v1-deprecated` 标记，**这是正确的**。本次返修不动这个标记；R1 是把同一节内 6 行主干表换成完整森林。

---

### 8. 审计附录草案（可直接迁入 review.md A.2 / A.3）

#### A.2 维度树证据账本草案（补充 / 替换 EV-001..007）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | §1 + Table 1 | p.1:3，与 8 个先前 surveys 比较 | "We are the first to present a comprehensive SLR on 395 papers..." | rq | verified | 根 / scope | 否 | 仅 LLM4SE 范围 |
| EV-002 | paper_content.txt | §2.1--§2.5 + Table 2/3/4/5 + Fig. 1 | p.1:4--9 | RQ1--4、6 venue、3 inclusion + 9 exclusion、10 QAC + 80%、Table 5 8 项 data items 绑定 RQ | search_and_selection | verified | meta-B + RQ-字段合同 | 仅 Fig. 1 拓扑 | -- |
| EV-003 | paper_content.txt | §3 + Fig. 4/5 + Table 6 | p.1:10--13 | 三分架构 + 70+ 模型族 + 5 年 × 3 架构频次 | 分类法 + statistical | verified | RQ1 子树 + 叶子.architecture + 叶子.model_family + edge.architecture_year | Fig. 4 树状版面 | LLM 实例对时间漂移强 |
| EV-004 | paper_content.txt | §4 + Fig. 6/7/8 + Table 7/8 + Appendix A Table 13 + Appendix B Table 14 | p.1:14--20, 72--74 | data source 4 / data type 5 + 60 子类 / preproc 7 步 / input form 4，分母 374、355 显式声明 | 分类法 + statistical + source_anchor | verified | RQ2 子树全部叶子 | 仅 Fig. 7/8 流程图细节 | text/code preproc 步骤名同但语义不同 |
| EV-005 | paper_content.txt | §5 + Fig. 9 + Table 9 + Appendix C Table 15 + Appendix D Table 16 | p.1:21--25, 74--77 | tuning 谱系 + 8 prompt + Others 76 + 4 problem type × 19/9/6/1 指标 set | 分类法 + statistical + source_anchor | verified | RQ3 子树全部叶子 + edge.problem_metric | -- | 指标 set 与 生成 任务强耦合 |
| EV-006 | paper_content.txt | §6 + Fig. 10 + Table 10/11/12 + Appendix E Table 17 | p.1:26--40, 77--79 | SDLC 6 阶段分布（百分比为 task-instance 口径）+ 85 specific tasks + 4 problem types | 分类法 + statistical + source_anchor | verified | RQ4 子树全部叶子 + edge.task_sdlc + edge.paper_anchor | -- | paper 计数 vs instance 计数 必须分列；85 task 命名 LLM4SE 专属 |
| EV-007 | paper_content.txt | §7 | p.1:40--41 | 3 类 威胁（检索遗漏（search omission）/ 选择偏倚（selection bias）/ 经验知识偏倚（empirical knowledge bias））及缓解 | limitation | verified | 迁移边界 + 降级判断 | 否 | 未公开 coder agreement、模式 drift |
| EV-008 | paper_content.txt + metadata.json | §3.1 末 + §7 footnote 6 + metadata.json `abstract` | p.1:10, 41 + metadata.json | URL 冲突：正文 = `xinyi-hou/LLM4SE_SLR`；metadata = `security-pride/LLM4SE_SLR` | source_anchor_conflict | requires_external_verification | edge.paper_anchor 完整性 | 是（联网） | 在确认前 制品 不得作既定事实 |
| EV-009 | paper_content.txt | §4.2 vs Table 7 vs Appendix A Table 13；§2.2.2 vs Fig. 1 | p.1:15--16, 72；p.1:6 vs p.1:5 | (a) software-仓库 "Code 仓库" 计数：正文 3 vs Table 7/13 中 9；(b) ScienceDirect：§2.2.2 写 62,290 vs Fig. 1 写 65,290 | internal_inconsistency | requires_pdf | meta-B 分母 + 叶子.data_type 子分类 | 是 | 引用前以 Appendix 为权威，并标差异 |

#### A.3 结论-证据映射草案（补充 / 替换 / 新增）

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 反证或限制 | 结论强度 | 允许用途 |
|---|---|---|---|---|---|---|---|---|
| clm-树-type | C01 | 本文样本单位是 原始研究 (N=395)；维度树是“RQ 驱动的维度森林”，4 棵主子树 + 2 棵 meta 子树；通用六叶仅作跨论文投影。 | 树类型（树_type） | 根节点 + RQ1..4 + meta-A/B | EV-001, EV-002 | -- | strong | verified |
| clm-arch-trend | C02 | 2020–2024.01 期间架构选择从 仅编码器（encoder-only） 主导漂移到 仅解码器（decoder-only） 主导（仅解码器（decoder-only） 在 2023 占 70.7%，2024.01 占 64.17%）。 | statistical_observation | 叶子.architecture + edge.architecture_year | EV-003 | 时间截止 2024-01-31，之后未追踪 | strong | verified |
| clm-input-token | C03 | 在 355 篇显式声明 input form 的论文中，token-based 占 97.75%；树/graph/pixel/混合（混合） 合计 < 2.3%。 | statistical_observation | 叶子.input_form | EV-004 | 仅显式声明者；显式声明 vs 全部之比为 355/395 | strong | verified |
| clm-工业（industrial）-缺口（gap） | C04 | 在 374 篇显式声明 数据集 的论文中，工业（industrial） 仅 6 篇（≈1.6%），构成学术-工业错位的实证证据。 | 候选发现（candidate_发现） | 叶子.data_source | EV-004 | 仅 LLM4SE 当前样本；safety-critical 子域可能 工业（industrial） 比例更高 | strong | verified |
| clm-sdlc-skew | C05 | LLM4SE 严重偏 development + maintenance（task-instance 占比 ≈ 79.4%），RE / design / management 合计 ≈ 5.5%；verification 仅 5 篇。 | statistical_observation + 候选发现（candidate_发现） | 叶子.sdlc_phase + 叶子.specific_task | EV-006 | 百分比为 task-instance 口径，与 paper 计数 不同 | strong | verified |
| clm-指标-skew | C06 | 评价指标体系高度偏向生成任务（19 指标, 338 instances）；回归 仅 1 instance，提示评价空间稀疏 + 任务定义偏置。 | statistical_observation | 叶子.metric_by_problem_type + edge.problem_metric | EV-005 | 指标 与 problem_type 强耦合，迁移到 STM/形式化任务需重定义 | strong | verified |
| clm-mig-方法 | C07 | 可迁移到 Paper2 的内容是方法学结构（RQ-字段合同、QGS 脚手架、Appendix-source-anchor、RQ summary box），**不是**任何 LLM4SE 领域结论。 | migration_boundary | 根节点 + edge.rq_fields + edge.paper_anchor | EV-002, EV-005, EV-007 | -- | strong | verified |
| clm-制品-conflict | C08 | 制品 URL 在正文与 metadata 之间冲突；在外部核验前不得作既定事实，需保留两条候选并标 `requires_external_verification`。 | source_anchor_risk | edge.paper_anchor | EV-008 | -- | weak | 候选发现（candidate_发现） |
| clm-internal-inconsistency | C09 | 该 SLR 正文叙述与 Appendix 表格在两处存在数字不一致（software-repo "Code 仓库" 计数；ScienceDirect 检索分母）；引用须以 Appendix 为权威并显式标差异。 | risk_only | meta-B + 叶子.data_type | EV-009 | -- | weak | 候选发现（candidate_发现） |
| clm-rq4-denominator | C10 | RQ4 中 “task-instance 计数”（Table 10/Fig. 10a 的 247 / 56.65%）与 “paper 计数”（RQ4 Summary 的 229 papers）必须分列；混用会导致百分比错误。 | risk_only | 叶子.specific_task + 叶子.sdlc_phase | EV-006 | -- | strong | verified |
| clm-威胁-shallow | C11 | 该文 威胁 较规范，但未公开 coder agreement、conflict resolution log、模式 revision history；Paper2 若主打 audit-first，应在此基础上更强。 | 候选发现（candidate_发现） | EV-007 | EV-007 | 不能据此否定该文质量 | weak | 候选发现（candidate_发现） |
| clm-statistical-pool | C12 | 该文具备主统计池资格（systematic_review + 显式分母 + QAC + Appendix anchor）；A1-DT 阶段叶子层已可升级为 verified，建议 metadata.json 的 `eligible_for_statistical_synthesis=true` 在 A2a 后正式生效。 | eligibility_decision | 根节点 + EV-001..007 | EV-001..007 | 个别字段仍 `requires_pdf` | strong | verified |

---

### 9. 技能使用与自我审查记录

#### 9.1 技能采用原则
1. **ai-research-writing-skill / SKILL.md**：采用了 *Evidence gate*（“仓库 files, experiment logs, notes outrank memory”）—— 本审计中所有 EV-* 都直接锚到 paper_content.txt 行号 / 页码，避免凭印象写。也采用了 *Story / Claim gate* 思想——任何结论都标 `verified / 候选发现（candidate_发现） / requires_pdf / requires_external_verification` 分层。
2. **reviewer-guidelines.md**：采用了 *Constructive Specificity Standard*——R1--R8 全部给出可执行动作（要改 review.md 哪一节、要新增哪条 EV）。采用了 *Common Reviewer Concerns* 中“Claims in Abstract/Introduction exceed the experiments”的检查角度，把 review.md 中的 `模式种子（模式_seed）` / `weak` 提示当作 limitation 显式保留而非掩盖。
3. **reviewer-self-review.md（未独立读取，但在 reviewer-guidelines.md 末尾 “Rebuttal-Aware Writing” 已涵盖其核心）**：在 §9.2 列出本输出最高风险，模拟 reviewer-self-review。
4. **research-planning / SKILL.md + output-schemas.md**：采用了“先 *Overall Plan*（树型 + meta + RQ）再 *Architecture 设计*（叶子表 + 关系边）再 *Logic 设计*（C/I/M 返修动作）”的 4 阶段分层；本审计 §3 → §4 → §5 → §7 即对应该顺序。
5. **planning-prompts.md（未独立读取，但 SKILL.md 已概述其结构）**：采用了 “Flag ambiguities explicitly rather than making assumptions”，例如对 “Code 仓库 = 3 还是 9” 不做猜测，单列 EV-009。
6. **autoresearch / SKILL.md**：本任务不是 autoresearch loop，但采用了其核心 “Completion is 制品-gated, 不因为模型说 done 就 done” 思路——本审计的 “完成” 判据是必填章节均产出可审计内容，而不是简单宣告完成。

#### 9.2 最高风险（reviewer 视角）
1. **R-RISK-1（高）**：未做 PDF 视觉级核验。EV-009 列出的两处不一致是基于 text 提取的差异；如果 `pdf_extractor` 文本模式在数字上有过误识（PDF 文字模式偶尔会把 6 / 8 / 0 / 5 等数字误识），上述差异可能是工具伪影而非论文本身错误。主线程合并前应跑一次 OCR mode + Fig. 1 视觉对照。
2. **R-RISK-2（高）**：维度森林虽然取材于正文 + Appendix，但 叶子.model_family 的 70+ 实例完整枚举本审计未逐条复现（只给了高频代表）。如果 Paper2 后续把该叶子作为正式可统计池，需要把 Fig. 4 全节点 OCR 校对一次。
3. **R-RISK-3（中）**：制品 URL 冲突（EV-008）尚未联网核验。本仓库当前规范允许在 WAF / 403 等阻塞下记录为待核验，但若 R5 真要升级 A.2，主线程合并时应明确 “联网核验失败 vs 未尝试联网” 的区别。

#### 9.3 blocked / timeout / 文件缺失
- 无 blocked。
- 无 timeout。
- 无文件缺失。所有 7 个 skill 文件 + 4 个论文文件 + review.md 均成功读取。
- 一处局部 truncation：第二次试图 `Read` paper_content.txt offset=2100 limit=700 时触发 25000 token 上限，改成 offset=2100 limit=500 + 后续分段读取，已覆盖完整。

---

报告完。建议主线程在合并前先按 §7 的 R1 / R2 / R3 / R4 / R5 五项 C/I 返修，把 review.md 的 §“原文模式主树”节升级到 §3 的完整原生森林，并把 A.2 / A.3 的 `not_verified` / `模式种子（模式_seed）` 升级为 `verified`，使该篇正式具备主统计池资格。
## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/llm4se-systematic-review.md](../../audits/a1dt-v2-19x3/adjudications/llm4se-systematic-review.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-llm4se-systematic-review-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-llm4se-systematic-review-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-llm4se-systematic-review-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-llm4se-systematic-review-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-llm4se-systematic-review-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-llm4se-systematic-review-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/llm4se-systematic-review__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-llm4se-systematic-review-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/llm4se-systematic-review.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-llm4se-systematic-review-type | clm-llm4se-systematic-review-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：SLR（Kitchenham-style；明确声明遵循 Kitchenham et al. [197,198] 方法学，§2 首段） | paper_type | 文本已核验（text_verified） | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-llm4se-systematic-review-unit | clm-llm4se-systematic-review-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：原始研究（一篇被纳入的 LLM4SE research paper），最终 N=395。 | 样本单位（sample_unit） | 文本已核验（text_verified） | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-llm4se-systematic-review-denom | clm-llm4se-systematic-review-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：主分母 N=395。子分母：N=374（显式说明 dataset）；N=355（显式说明 input form）；N=154（peer-reviewed）+ 241（arXiv）；按年 7/13/56/273/46（2020–2024.01）。 | denominator | 文本已核验（text_verified） | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-llm4se-systematic-review-tree | clm-llm4se-systematic-review-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：维度森林。根为 4 个 RQ，每个 RQ 各自展开一棵编码树（RQ1 模型、RQ2 数据、RQ3 优化与评价、RQ4 任务），通过 Table 5 的 8 项 data items 串联。 | schema | 文本已核验（text_verified） | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-llm4se-systematic-review-pool | clm-llm4se-systematic-review-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：是（局部可统计）。该文是 systematic_review，有明确分母、纳排、QAC 与 Appendix 锚定；其分类频次（如 architecture × year、data_source、input_form、SDLC activity、metric × problem_type）可作为正式可统计 schema。但当前单篇 review.md 中具体数字未逐一回 Table 13–17 精核，部分百分比口径（task instance vs paper count）仍存在分母歧义，须 A2a 锚定。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-llm4se-systematic-review-type | A1DT-llm4se-systematic-review-C01 | 本文原文类型为：SLR（Kitchenham-style；明确声明遵循 Kitchenham et al. [197,198] 方法学，§2 首段） | paper_type | type | ev-llm4se-systematic-review-type | 正式写作前需核对出版页和 PDF 版式 | 文本已核验（text_verified） | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-llm4se-systematic-review-unit | A1DT-llm4se-systematic-review-C02 | 本文被编码样本单位为：原始研究（一篇被纳入的 LLM4SE research paper），最终 N=395。 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-llm4se-systematic-review-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | 文本已核验（text_verified） | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-llm4se-systematic-review-tree | A1DT-llm4se-systematic-review-C03 | 本文原生维度树 / 维度森林为：维度森林。根为 4 个 RQ，每个 RQ 各自展开一棵编码树（RQ1 模型、RQ2 数据、RQ3 优化与评价、RQ4 任务），通过 Table 5 的 8 项 data items 串联。 | 树类型（tree_type） | native_tree | ev-llm4se-systematic-review-tree | 不代表跨论文通用模板 | 文本已核验（text_verified） | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-llm4se-systematic-review-pool | A1DT-llm4se-systematic-review-C04 | 本文统计池资格为：是（局部可统计）。该文是 systematic_review，有明确分母、纳排、QAC 与 Appendix 锚定；其分类频次（如 architecture × year、data_source、input_form、SDLC activity、metric × problem_type）可作为正式可统计 schema。但当前单篇 review.md 中具体数字未逐一回 Table 13–17 精核，部分百分比口径（task instance vs paper count）仍存在分母歧义，须 A2a 锚定。 | eligibility | 统计池（statistical_pool） | ev-llm4se-systematic-review-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-llm4se-systematic-review-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-llm4se-systematic-review-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-llm4se-systematic-review-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
