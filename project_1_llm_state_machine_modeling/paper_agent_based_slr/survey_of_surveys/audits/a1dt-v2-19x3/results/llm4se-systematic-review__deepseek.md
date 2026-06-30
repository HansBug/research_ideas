Now I have read all the skill/guide files and the paper content thoroughly. Let me produce the complete audit report.

---

# A1-DT v2 单篇全文审计报告：`llm4se-systematic-review`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `llm4se-systematic-review` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是。全文 `paper_content.txt`（4152行）已完整通读，覆盖 Abstract、Introduction (§1)、Methodology (§2)、RQ1 (§3)、RQ2 (§4)、RQ3 (§5)、RQ4 (§6)、Threats (§7)、Challenges & Opportunities (§8)、Conclusion (§9)、References 及 Appendix 相关文本。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`bibtex.bib` 确认期刊为 TOSEM Vol.33(8), pp.1--79, 2024。`metadata.json` 确认 CCF-A、SLR 类型、evidence_role 为 `slr_field_schema_pattern`。 |
| 是否打开或核对 `paper.pdf` | 否。本审计基于 `paper_content.txt`（文本提取产物）。未对 `paper.pdf` 做逐页版面/图表视觉核验。图4（LLM architecture taxonomy tree）、表8（input forms）、表17（SE task mapping）、附录A--E 的精确表头/取值/页码均来自 `paper_content.txt` 文本线索；若需精确阈值/排版证据，必须补 PDF 视觉核验。 |
| 原文类型 | SLR（Systematic Literature Review）。遵循 Kitchenham 方法学；有系统检索、纳排标准、质量评估、数据抽取表（Table 5）、编码方案、统计分析与附录全文引用表。 |
| 被编码样本单位 | primary study（单篇 LLM4SE 研究论文）。最终纳入 395 篇，覆盖 2017-01 至 2024-01-31。 |
| 样本数量 / 分母 | 395（检索 218,765 条 → 自动筛选 → 全文扫描 594 → 质量评估 382 → snowballing +13 = 395）。其中 peer-reviewed venue 154 篇，arXiv 241 篇。 |
| 原生树类型 | **维度森林**（Dimension Forest）。以四个 RQ 为主干、每个 RQ 挂载 2--6 个编码层级的分类学（taxonomy）/ 抽取字段表（extraction form），叶子分布在 LLM 架构、数据源/类型/预处理/输入形式、优化/评价策略、SE activity/task 四个维度域中，互相正交但同源（同一批 395 篇 primary studies）。 |
| 主统计池资格 | **是**。该文是一级 SLR（非 tertiary/umbrella review、非 roadmap/guideline，有系统样本库与编码方案），可参与跨论文 schema 统计。但注意：其领域是 LLM4SE，不是 LLM4STM/formal methods；其统计值只能作为「SLR 字段设计模式」和「SE SLR 编码树结构样本」迁移，领域结论不可迁移。 |
| 总体判定 | **pass**（可用于 schema_seed）。原文编码树丰富、字段来源可追溯、附录完整。现有 `review.md` 需要返修：当前维度树用"六个通用接口叶"代替原文树，需重写为以四 RQ 为主干 + 原文抽取字段为叶子的原生树复原。 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取范围

- **`paper_content.txt`**：全文 4152 行（80 页），逐段阅读，覆盖全部章节；
- **`bibtex.bib`**：确认引用元数据；
- **`metadata.json`**：确认分类口径、evidence_role、eligibility 字段；
- **未打开 `paper.pdf`**：所有图表/附录证据锚点均来自 text 文件的段落文本线索；精确页码、表头对齐、取值完整性以 text 为准，必要时需 PDF 视觉核验。

### 1.2 关键原文证据锚点（10 个）

| # | 锚点 | 原文章节/位置 | 内容摘要 |
|---|---|---|---|
| 1 | Table 5 "Extracted data items and related RQs" | §2.5 (p.9--10) | 定义了 8 个抽取数据项：SE task category、LLM category、LLM characteristics、data handling techniques、optimizer/algorithms、evaluation metrics、SE activity、solutions/strategies。这是原生编码 schema 的总入口。 |
| 2 | Fig. 4 "Distribution of the LLMs" | §3.1 (p.10) | 以 taxonomy tree 将 LLM 分为 encoder-only / encoder-decoder / decoder-only 三类，挂载 >70 种具体模型名及使用频次。 |
| 3 | Table 6 "Summary of LLMs with different architectures" | §3.1 (p.11) | 将三类架构映射到典型 SE task 类型（understanding / understanding+generation / generation）。 |
| 4 | Fig. 5 "Temporal trends" | §3.5 (p.13) | 逐年架构使用趋势（2020--2024.1），展示 decoder-only 从 39.1% 升至 70.7%（2023）。 |
| 5 | §4.2 "What are the common types of datasets" | §4 (p.16--17) | 将数据源分四类（text-based, code-based, graph-based, software repository-based），每类列举具体 data type 及频次。 |
| 6 | Fig. 7/Fig. 8 "Data preprocessing procedure" | §4.3 (p.18--19) | 分别定义 text-based 和 code-based 的 7-step 预处理管道，每步有具体操作名和示例。 |
| 7 | Table 8 "Various input forms of LLMs" | §4.4 (p.20) | 输入形式枚举：NL text, code snippets, code+NL, AST, CFG, PDG, screenshots, GUI hierarchies 等。 |
| 8 | §5.1--§5.3 "Optimization techniques" | §5 (p.22--27) | fine-tuning（FT/PEFT）、prompt engineering（zero/few-shot、CoT、prompt design/tuning）、evaluation metrics（BLEU/CodeBLEU/exact match/accuracy/F1/pass@k/MRR）。 |
| 9 | Table 16 "Software engineering activities and tasks" | §6 (p.34--37) | 将 SE 任务按 6 个 activity（requirements, design, development, QA, maintenance, management）组织，再细分 60+ specific task。 |
| 10 | Table 17 "Complete mapping" + Appendix A--E | §6 (p.77--79) + Appendix | 每篇 primary study 被映射到具体的 SE activity/task，并带完整引用编号。附录提供 RQ1--RQ4 全引用表。 |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象

**纳入对象**：单篇 LLM4SE primary study（研究论文）。作者明确将每篇论文作为一个可编码观察单位，对其抽取 LLM 类型、数据方法、优化策略、SE 任务等属性。

### 2.2 系统检索/纳排/数据抽取/编码方案

是。作者遵循 Kitchenham SLR 方法学，实施了完整的系统流程：
1. **检索**：手动检索 6 个顶级 SE venue（ICSE/ESEC-FSE/ASE/ISSTA/TOSEM/TSE）4,618 篇 → 构造 QGS（51 篇）→ 导出 search string → 自动化检索 7 个数据库（IEEE Xplore/ACM DL/ScienceDirect/Web of Science/Springer/arXiv/DBLP）→ 初始 218,765 条。
2. **筛选**：去重 → 排除 <8 页 → 标题/摘要/关键词过滤 → 全文扫描 → 质量评估（Table 3/4 inclusion/exclusion criteria）。
3. **数据抽取**：使用预定义的 extraction form（Table 5，8 个 data item），全文阅读后逐篇填写。
4. **编码方案**：LLM 按 architecture taxonomy（Pan et al. [326] 的三分法）、SE task 按 6-activity SDLC 分类、优化策略按 FT/PEFT/prompt engineering 分类。

### 2.3 原文字段来源

| 字段来源 | 具体载体 | 证据 |
|---|---|---|
| Extraction form | Table 5 (§2.5) | 8 个抽取项直接对应 RQ。 |
| LLM taxonomy | Fig. 4 (§3.1) | 三分法（encoder-only / encoder-decoder / decoder-only）引自 Pan et al. [326]。 |
| Data type classification | §4.1--§4.2 | 作者自建四类分类（text/code/graph/repo-based），每类再细分数种子类型。 |
| Preprocessing pipeline | Fig. 7/Fig. 8 (§4.3) | 作者从 395 篇中归纳出 7-step 通用管道。 |
| Input form enumeration | Table 8 (§4.4) | 从 primary studies 中归纳所有输入表示形式。 |
| Optimization taxonomy | §5.1--§5.3 | FT/PEFT/prompt engineering，参考 Sahoo et al. [370] 等。 |
| Evaluation problem type | §5.4 | generation / classification / recommendation / regression 四分法。 |
| SE activity/task mapping | Table 16 (§6) + Appendix | 6-activity SDLC + 60+ specific tasks。 |
| Replication package | GitHub (`LLM4SE_SLR`) | 公开 artifact，含完整引用表和分类数据。 |

### 2.4 RQ 与样本单位的关系

四个 RQ 不是树根，而是**四个正交维度域的分组标签**。真正的树根是 395 篇 primary studies，每个 primary study 在四个 RQ 维度域上各自被赋予一组编码值。Relation 可以概括为：

- **RQ 是字段用途（field purpose）**：每个 RQ 定义"我们对这 395 篇论文要问什么"。
- **被抽取字段是叶子**：它们来自 extraction form（Table 5）和从 primary studies 中归纳的分类框架。
- **RQ 的 summary bullet points 是统计观察**：是字段统计后的聚合发现，不是字段本身。

### 2.5 样本库存在性

有系统样本库。395 篇 primary studies 是完备的编码分母。该文不是 roadmap / vision / proposal / guideline，不触发降级。

---

## 3. 原生样本编码维度树 / 维度森林

以下用 text tree 给出原文的原生维度森林。根对象是 `395 primary studies`。四个主维度域对应四个 RQ。

```
395 PRIMARY STUDIES (2017-01--2024-01-31)
│
├─ [RQ1] LLM 模型维度域
│   ├─ LLM Architecture
│   │   ├─ encoder-only          [完整枚举: BERT, RoBERTa, ALBERT, CodeBERT, GraphCodeBERT, ...]
│   │   ├─ encoder-decoder       [完整枚举: BART, T5, CodeT5, CodeT5+, AlphaCode, CoTexT, ...]
│   │   └─ decoder-only          [完整枚举: GPT-1/2/3/4, ChatGPT, GPT-3.5, Codex, CodeGen, LLaMA, StarCoder, ...]
│   ├─ Specific Model Name       [层级枚举: >70 种模型名; 见 Fig.4 和附录]
│   ├─ Parameter Size            [数值或区间: if declared in paper; 见 GitHub artifact]
│   ├─ Model Family              [层级枚举: GPT series, CodeBERT series, T5 series, LLaMA series, ...]
│   ├─ Model Fit for SE Task Type [关系值: 三类架构 → {understanding, understanding+generation, generation}; 见 Table 6]
│   └─ Temporal Usage Trend      [数值: 逐年 paper count per architecture; 见 §3.5 Fig.5]
│
├─ [RQ2] 数据维度域
│   ├─ Data Source Category
│   │   ├─ text-based            [布尔 + 具体 data type 枚举; §4.2]
│   │   ├─ code-based            [布尔 + 具体 data type 枚举; §4.2]
│   │   ├─ graph-based           [布尔 + 具体 data type 枚举; §4.2]
│   │   ├─ repository-based      [布尔 + 具体 data type 枚举; §4.2]
│   │   └─ combined              [布尔 + 具体组合枚举; §4.2]
│   ├─ Data Type
│   │   ├─ programming tasks/problems    [频次: 42]
│   │   ├─ prompts                       [频次: 33]
│   │   ├─ SO posts                      [频次: 12]
│   │   ├─ bug reports                   [频次: 11]
│   │   ├─ source code                   [频次: 60]
│   │   ├─ bugs/buggy code               [频次: 16]
│   │   ├─ patches                       [频次: 4]
│   │   ├─ vulnerable source code        [频次: 8]
│   │   └─ ... (更多 data type; 完整列表见 §4.2)
│   ├─ Data Preprocessing Steps
│   │   ├─ text pipeline [层级枚举: data extraction → initial segmentation → unqualified deletion → text preprocessing → dup deletion → tokenization → data segmentation]
│   │   └─ code pipeline [层级枚举: data extraction → unqualified deletion → dup deletion → compilation → uncompilable deletion → code representation → data segmentation]
│   ├─ Code Representation Form
│   │   ├─ token-based     [布尔]
│   │   ├─ tree-based (AST) [布尔]
│   │   └─ graph-based (CFG/CG/PDG) [布尔]
│   └─ Input Form to LLM
│       ├─ natural language text      [布尔; Table 8]
│       ├─ code snippets              [布尔; Table 8]
│       ├─ code + NL combined         [布尔; Table 8]
│       ├─ AST                        [布尔; Table 8]
│       ├─ CFG/PDG                    [布尔; Table 8]
│       └─ screenshots/GUI hierarchy  [布尔; Table 8]
│
├─ [RQ3] 优化与评价维度域
│   ├─ Optimization Strategy
│   │   ├─ Fine-Tuning (FT)
│   │   │   ├─ full fine-tuning         [布尔]
│   │   │   └─ PEFT (LoRA, adapters, prefix-tuning, ...) [层级枚举; §5.1]
│   │   └─ Prompt Engineering
│   │       ├─ zero-shot                [布尔]
│   │       ├─ few-shot                 [布尔]
│   │       ├─ prompt design            [自由文本加理由; 具体 prompt 样例见 §5.2]
│   │       ├─ prompt tuning            [布尔]
│   │       └─ Chain-of-Thought (CoT)   [布尔]
│   ├─ Weight Training Algorithm        [自由文本加理由: 从 primary study 中抽取; §5.1]
│   ├─ Optimizer                        [自由文本加理由: 从 primary study 中抽取; §5.1]
│   ├─ Evaluation Problem Type
│   │   ├─ generation                   [布尔; §5.4]
│   │   ├─ classification               [布尔; §5.4]
│   │   ├─ recommendation               [布尔; §5.4]
│   │   └─ regression                   [布尔; §5.4]
│   └─ Evaluation Metric
│       ├─ BLEU / CodeBLEU              [布尔/数值; §5.4 & Appendix D]
│       ├─ exact match (EM)             [布尔/数值; §5.4]
│       ├─ accuracy                     [布尔/数值; §5.4]
│       ├─ F1-score                     [布尔/数值; §5.4]
│       ├─ pass@k                       [布尔/数值; §5.4]
│       ├─ MRR                          [布尔/数值; §5.4]
│       └─ ... (更多 metric; 完整见 §5.4 & Appendix D)
│
├─ [RQ4] SE 任务维度域
│   ├─ SE Activity (SDLC phase)
│   │   ├─ Requirements Engineering    [层级枚举: 含 3 specific tasks]
│   │   ├─ Software Design             [层级枚举: 含 4 specific tasks]
│   │   ├─ Software Development        [层级枚举: 含 18 specific tasks; 如 code generation[118], code completion[22], code summarization[21], ...]
│   │   ├─ Software Quality Assurance  [层级枚举: 含 17 specific tasks; 如 vulnerability detection[18], test generation[17], ...]
│   │   ├─ Software Maintenance        [层级枚举: 含 26 specific tasks; 如 program repair[35], code clone detection[8], ...]
│   │   └─ Software Management         [层级枚举: 含 2 specific tasks]
│   ├─ Specific SE Task                [层级枚举: 60+ tasks; 完整列表见 Table 16/Table 17 及附录]
│   ├─ Solution Strategy               [自由文本加理由: 从 primary study 中归纳; §6]
│   └─ Task Paper Count                [数值: per task statistics; Table 17]
│
└─ [跨域] 质量评估 & 文献属性
    ├─ Venue Type (peer-reviewed / arXiv) [布尔; §2.5 Fig.2(a)]
    ├─ Publication Year                  [数值; §2.5 Fig.2(b)]
    └─ Quality Assessment Score          [数值: 基于 Table 4 rubric; 仅用于纳排，不进入主编码树]
```

### 缺失部分与 A2a 精核任务

- **RQ1 具体模型-参数映射**：`paper_content.txt` 有 Fig.4 的文本描述（含频次数字），但完整参数大小表在 GitHub artifact。A2a 需下载 artifact 或 PDF 核对 Fig.4 的精确数字。
- **Appendix A--E 完整表**：`paper_content.txt` 在 RQ1--RQ4 各处提示「*See Appendix X for the full table」，但 text 提取未完整呈现附录全文。A2a 需 PDF 视觉核验附录完整性。
- **RQ3 evaluation metric 完整枚举**：§5.4 和 Table 9 有代表性 metric 列表，但 text 行文中有省略号。A2a 需核验完整 metric 枚举。
- **Challenges & Opportunities (§8)**：不是编码字段，而是从编码统计推演出的高级 discussion finding。不应混入原生维度树。

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `LLM_ARCH` | LLM 架构类别 | RQ1 → LLM Architecture | Table 5 "category of LLM" + Fig.4 taxonomy | 按 encoder/decoder 结构将 LLM 分为三类 | {encoder-only, encoder-decoder, decoder-only} | 完整枚举 | 若 primary study 未明确声明架构，无法编码 | RQ1 统计各架构 paper count 和 temporal trend | 可迁移为 Paper2 的"被评论文献所用的模型架构类型"字段 | Fig.4, §3.1, Table 6 | 结构可迁移；具体模型名不可迁移（领域不同） |
| `LLM_NAME` | 具体模型名称 | RQ1 → Specific Model Name | Fig.4 + GitHub artifact | 论文中使用的具体 LLM 名称 | >70 种模型名（BERT, CodeBERT, GPT-3, GPT-4, ChatGPT, Codex, CodeGen, LLaMA, StarCoder, ...） | 层级枚举 | 部分论文可能使用未命名/私有/内部模型 | 映射模型使用频次 | 可迁移为 Paper2 的"被评论文献所用的模型名称"字段 | Fig.4 full taxonomy tree | 枚举集完全不同 |
| `LLM_PARAM_SIZE` | 模型参数量 | RQ1 → Parameter Size | §3.1 "parameter sizes (if declared in the paper)" | 论文中声明的模型参数规模 | 数值（如 125M, 1.5B, 175B, ...） | 数值或区间 | 很多论文未声明参数大小 | RQ1 中作为补充描述 | 启发 Paper2 收集"被评论文献所用模型规模"字段 | §3.1 GitHub artifact reference | 结构可迁移 |
| `LLM_TASK_FIT` | 架构-SE任务适配 | RQ1 → Model Fit | Table 6 | 三类架构适配的 SE 任务类型 | encoder-only→understanding; encoder-decoder→understanding+generation; decoder-only→generation | 关系值（架构↔任务类型） | N/A（基于架构定义，非逐篇编码） | RQ1 摘要性观察 | 启发 Paper2 建立"模型类型→验证任务类型"的关系映射 | Table 6 | 关系结构可迁移 |
| `LLM_TREND` | 年度使用趋势 | RQ1 → Temporal Trend | §3.5 Fig.5 | 各架构逐年使用论文数 | paper count per architecture per year | 数值（时序） | N/A | 趋势分析 | 启发 Paper2 的时序分析方法 | §3.5 | 分析方法可迁移 |
| `DATA_SOURCE` | 数据来源类别 | RQ2 → Data Source Category | §4.1--§4.2 | 数据来源的宏观分类 | {text-based, code-based, graph-based, repository-based, combined} | 完整枚举 | 部分论文的数据来源可能跨类或未分类 | RQ2 数据源分布统计 | 可迁移为 Paper2 的"被评论文献所用数据类型"字段 | §4.2 四类分类 | 分类结构可迁移 |
| `DATA_TYPE` | 数据类型 | RQ2 → Data Type | §4.2 枚举 | 数据的具体类型 | {programming tasks, prompts, SO posts, bug reports, source code, bugs/buggy code, patches, vulnerable source code, test suites, ...} | 层级枚举（二分类 text/code 下挂子类型） | 部分论文的数据类型不在预定义枚举中 | RQ2 数据类型频次统计 | 可迁移为 Paper2 的数据类型字段 | §4.2 枚举 + 频次数字 | 枚举名可迁移；具体频次无关 |
| `DATA_PREPROC` | 数据预处理管道 | RQ2 → Preprocessing | §4.3 Fig.7/Fig.8 | 数据预处理步骤序列 | {data extraction → (init segmentation) → unqualified deletion → (text preprocessing / compilation) → dup deletion → (tokenization / code representation) → data segmentation} | 层级枚举（管道步骤序列） | N/A（归纳性发现，非逐篇编码） | RQ2 预处理方法总结 | 启发 Paper2 的"被评论文献数据处理方法"描述字段 | Fig.7, Fig.8 | 管道结构可迁移 |
| `CODE_REPR` | 代码表示形式 | RQ2 → Code Representation | §4.3 | 代码在输入 LLM 前的表示形式 | {token-based, tree-based (AST), graph-based (CFG/CG/PDG)} | 完整枚举 | 不适用于无代码的论文 | RQ2 代码表示分布 | 迁移为 Paper2 的代码/模型表示字段 | §4.3 | 可迁移 |
| `INPUT_FORM` | 输入形式 | RQ2 → Input Form | Table 8 (§4.4) | LLM 接收的输入表示形式 | {NL text, code snippets, code+NL, AST, CFG, PDG, screenshots, GUI hierarchy, ...} | 层级枚举 | 部分论文使用未在表8中的特殊输入形式 | RQ2 输入形式分布 | 迁移为 Paper2 的输入/输出表示字段 | Table 8 | 可迁移 |
| `OPT_STRATEGY` | 优化策略 | RQ3 → Optimization Strategy | §5.1--§5.2 | LLM 用于 SE 任务时的优化方法 | {full FT, PEFT (LoRA/adapters/prefix), prompt engineering (zero/few-shot, CoT, prompt design/tuning)} | 层级枚举 | 部分论文组合多种策略 | RQ3 优化策略频次和趋势 | 迁移为 Paper2 的"被评论文献所用优化/适配方法"字段 | §5.1, §5.2 | 可迁移 |
| `EVAL_PROBLEM_TYPE` | 评价问题类型 | RQ3 → Problem Type | §5.4 | SE 任务的评价问题分类 | {generation, classification, recommendation, regression} | 完整枚举 | N/A（宏观分类） | RQ3 问题类型分布 | 启发 Paper2 的"验证任务类型"分类 | §5.4 | 四分法可迁移 |
| `EVAL_METRIC` | 评价指标 | RQ3 → Evaluation Metric | §5.4 Table 9 + Appendix D | 论文中使用的评价指标 | {BLEU, CodeBLEU, exact match, accuracy, F1, pass@k, MRR, ...} | 层级枚举 | 部分论文使用自定义/非标准 metric | RQ3 metric 使用频次 | 迁移为 Paper2 的"评价指标"字段 | §5.4, Table 9, Appendix D | 可迁移 |
| `SE_ACTIVITY` | SE 活动类别 | RQ4 → SE Activity | Table 16 (§6) | 按 SDLC 阶段分类 | {Requirements Engineering, Software Design, Software Development, Software Quality Assurance, Software Maintenance, Software Management} | 完整枚举 | N/A | RQ4 SE activity 分布统计 | 启发 Paper2 按 activity 组织被评论文献 | Table 16 | 结构可迁移；具体 activity 不同 |
| `SE_TASK` | 具体 SE 任务 | RQ4 → Specific SE Task | Table 16/Table 17 (§6) + Appendix E | 精细的 SE 任务名称 | >60 种任务名（code generation, code completion, code summarization, vulnerability detection, test generation, program repair, ...） | 层级枚举（按 activity 分组） | 不属于任何已知 SE task 的论文归入"Others" | RQ4 task 频次和分布 | 迁移为 Paper2 的"任务类型"字段 | Table 16, Table 17 | 层级枚举结构可迁移；具体任务名不同 |
| `SE_TASK_COUNT` | SE 任务论文数 | RQ4 → Task Paper Count | Table 17 (§6) | 每个具体 SE task 的论文数 | 数值（如 code generation=118, program repair=35, ...） | 数值 | N/A | 任务热度排序 | 不直接迁移（领域不同） | Table 17 | 不迁移 |
| `SOLUTION_STRATEGY` | 解决策略 | RQ4 → Solution Strategy | §6 各节叙述 | 论文中针对 SE 任务提出的具体解决方案策略 | 自由文本加理由 | 自由文本加理由 | 部分论文策略描述不详 | RQ4 定性总结 | 启发 Paper2 的"方案策略"字段 | §6 | 模板可迁移 |
| `VENUE_TYPE` | 发表类型 | 跨域 → Venue | §2.5 Fig.2(a) | peer-reviewed venue 还是 arXiv pre-print | {peer-reviewed, arXiv} | 完整枚举 | N/A | 语料质量分布 | 迁移为 Paper2 的"文献发表类型"字段 | §2.5 | 可迁移 |
| `PUB_YEAR` | 发表年份 | 跨域 → Year | §2.5 Fig.2(b) | 论文发表年份 | 数值（2017--2024） | 数值或区间 | N/A | 时序分布 | 迁移为 Paper2 的"文献年份"字段 | §2.5 | 可迁移 |

---

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `EDGE_ARCH_TO_TASK` | LLM_ARCH | 适配关系 | SE_TASK 类型（understanding / generation / mixed） | {understanding, generation, understanding+generation} | N/A（基于架构设计推断） | Table 6, §3.1 | 连结 RQ1 和 RQ4：架构选择由任务特性驱动 |
| `EDGE_ARCH_TO_TREND` | LLM_ARCH | 时序统计关系 | PUB_YEAR + paper count | 数值（逐年各架构 count） | N/A | §3.5, Fig.5 | 展示架构偏好的历史变迁 |
| `EDGE_DATA_TO_TASK` | DATA_TYPE / DATA_SOURCE | 使用关系 | SE_TASK | 交叉统计（未逐项给出定量） | 部分论文的数据-task 映射不完整 | §4, §6 | 不同 SE task 倾向不同数据类型（RQ2→RQ4） |
| `EDGE_OPT_TO_TASK` | OPT_STRATEGY | 应用关系 | SE_TASK | 交叉描述（§5--§6 行文中散布） | 未显式做 cross-tabulation | §5, §6 | 不同 SE task 倾向不同优化策略 |
| `EDGE_EVAL_TO_TASK` | EVAL_PROBLEM_TYPE / EVAL_METRIC | 评估关系 | SE_TASK | 交叉描述 | 未显式做 cross-tabulation | §5.4, §6 | 不同 SE task 倾向不同 evaluation type/metric |
| `EDGE_QA_TO_POOL` | Quality Assessment Score | 筛选关系 | 纳入资格 | 0--N 分 → pass/fail | 未公开具体分数 | §2.4 Table 4 | QA 是从 594→382 的筛选门；不进入编码 |
| `EDGE_VENUE_TO_YEAR` | VENUE_TYPE | 统计关系 | PUB_YEAR + paper count | 数值（peer-reviewed vs arXiv 逐年 count） | N/A | §2.5 Fig.2(a)(b) | 展示 arXiv 占比增加趋势 |

**未发现显式关系边**：原文主要是**平行维度编码**结构，395 篇论文在四个 RQ 维度上被独立编码。论文未显式做 RQ1×RQ2×RQ3×RQ4 的交叉统计/列联表/多变量回归。关系边以定性叙述（§3--§6 的行文）为主，定量交叉表仅限于 RQ 内部的简单统计分布。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文由字段/统计表支持的统计观察

| # | 统计观察 | 来源字段 | 证据 | 类型 |
|---|---|---|---|---|
| O1 | decoder-only 架构在 2023 年占 70.7%（195/276 篇），较 2022 年（51.4%）大幅上升 | LLM_ARCH × PUB_YEAR | §3.5, Fig.5 数字 | 描述性统计 |
| O2 | 395 篇中 >70 种不同 LLM 被使用，ChatGPT（72 次）、Codex（62 次）、GPT-4（53 次）、GPT-3.5（54 次）、CodeBERT（51 次）、BERT（50 次）、CodeT5（46 次）等最频繁 | LLM_NAME | Fig.4 频次数字 | 频次统计 |
| O3 | source code (60 次）和 programming tasks (42 次）是最常见的数据类型 | DATA_TYPE | §4.2 频次数字 | 频次统计 |
| O4 | code generation (118 篇）、program repair (35 篇）、code completion (22 篇）、code summarization (21 篇）是最热门的 SE task | SE_TASK × SE_TASK_COUNT | Table 17 | 频次统计 |
| O5 | 2023 年 LLM4SE 论文爆炸式增长：273 篇（vs 2022 年 56 篇） | PUB_YEAR | §2.5 Fig.2(b) | 时序统计 |
| O6 | 241/395（61%）的论文来自 arXiv（非 peer-reviewed） | VENUE_TYPE | §2.5 | 比例统计 |
| O7 | fine-tuning 和 prompt engineering 是两种主要优化路线，各有适用场景 | OPT_STRATEGY | §5.1--§5.2 | 定性归纳 |

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

| # | 候选 finding | 原文位置 | 是否可迁移到 Paper2 |
|---|---|---|---|
| C1 | LLM4SE 面临 model size/deployment 挑战（存储、计算、能耗）→ 需要压缩和高效推理 | §8.1.1 | 弱相关。Paper2 的 LLM4STM 领域也面临类似挑战，但具体领域约束不同。 |
| C2 | data dependency 是核心瓶颈：benchmark contamination、PII leakage、domain-specific data 稀缺 | §8.1.1 | 可迁移为方法学原则（数据质量/偏倚/污染风险），不是领域结论。 |
| C3 | LLM 在代码生成中的 ambiguity 问题→需要 domain-specific knowledge 注入 | §8.1.1 | 弱相关。可启发 Paper2 中关于"LLM 状态机生成中的歧义消解"讨论。 |
| C4 | LLM generalizability 不足：跨任务/跨领域/跨语言性能下降 | §8.1.2 | 强相关。可迁移为"LLM4STM 方法学的可泛化性讨论"种子。 |
| C5 | SE4LLM 是新兴方向：需要专用 SE 实践来开发/维护 LLM 本身 | §8.2 | 可作为 Paper2 background 或 future work 的灵感来源。 |
| C6 | 未来应探索 LLM 在 software security（自动审计、合规验证、漏洞检测）中的角色 | §8.2 | 部分相关。Paper2 涉及形式化验证，可引用此方向。 |
| C7 | benchmark 标准化和 evaluation protocol 统一是 LLM4SE 的 urgent need | §8.1.1, §8.2 | 强相关。可迁移为 Paper2 关于"benchmarking LLM4STM 需要标准化评价"的论点种子。 |

### 6.3 对 Paper2 可迁移的方法学启发

| # | 启发 | 迁移方式 |
|---|---|---|
| M1 | 四 RQ 平行维度编码结构 | 直接：Paper2 可借鉴将本文的 RQ1→RQ4 映射为 Paper2 的编码维度域 |
| M2 | Extraction form（Table 5）+ Appendix 全文引用表 | 直接：Paper2 应建立类似的 extraction form + 公开 artifact |
| M3 | 从 primary study 归纳分类学而非预设 taxonomy | 直接：Paper2 的 SE task 分类应来自被评论文献而非外部标准 |
| M4 | 统计观察→challenge→opportunity→roadmap 的证据升级链 | 直接：Paper2 可借鉴此链组织 discussion |
| M5 | QGS-based search string derivation | 直接：Paper2 的 SLR 检索策略可参考 |
| M6 | QC rubric（Table 4）用于纳排门 | 直接：Paper2 应建立类似质量评估标准 |

### 6.4 绝不能迁移的领域结论

- 具体 LLM 在 specific SE task（如 code generation/vulnerability detection/program repair）上的性能排名、频次分布、趋势；
- 具体 SE task 热度排名（code generation 最高等）；
- 具体 data type 分布（source code 60 次等）；
- 任何关于 LLM4SE 领域的 causal claim 或 performance claim；
- §8 中关于 SE task 特定方向的 roadmap item。

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 严重级别（C）问题

| ID | 问题 | 位置 | 建议修改 | 优先级 |
|---|---|---|---|---|
| C01 | **维度树用六个通用接口叶代替原文原生树**。现有 review 的 A.1 维度树叶子为「范围/语料/分类/方法/证据/finding」六叶，这不是该论文自己的编码树，而是跨论文投影模板。 | A.1 维度树定义 + A.1DT-llm4se-systematic-review-C01--C05 | 必须重写：用本审计报告 §3 的原生维度森林替换，根为 395 primary studies，四个主干为 RQ1--RQ4，叶子为 §4 表格中的具体字段。 | 🔴 阻塞 |
| C02 | **样本单位定义偏差**。现有 review 说"被编码对象是 primary study"，但未在维度树中体现 primary study 是根、而不是 RQ/activity 是根。 | 快速结论卡片 + A.1 | 修正：明确样本单位 = 395 篇 primary study，它们是编码树叶子的赋值对象。 | 🔴 |
| C03 | **统计数据池资格标记可能不准确**。现有 review 标记 `eligible_for_statistical_synthesis: true`，这对 schema 级别是对的，但需明确区分：可进入 schema 统计池 ≠ 可进入领域 finding 统计池。 | metadata.json + review | 修正：在 review 中补充「此论文的统计值只能进入 schema 结构统计池（编码树形态、extraction form 字段设计），领域统计值（如 code generation 118 篇）不可进入 Paper2 目标领域统计」。 | 🟡 |

### 7.2 重要级别（I）问题

| ID | 问题 | 位置 | 建议修改 | 优先级 |
|---|---|---|---|---|
| I01 | **缺少 RQ2 数据维度域的细节叶子**。现有维度树没有 DATA_SOURCE、DATA_TYPE、DATA_PREPROC、CODE_REPR、INPUT_FORM 等 RQ2 原生叶子。 | A.1 维度树 | 新增：从本审计 §4 的叶子表中补入 RQ2 相关叶子。 | 🟡 |
| I02 | **缺少 RQ3 优化与评价维度域的细节叶子**。现有维度树没有 OPT_STRATEGY、EVAL_PROBLEM_TYPE、EVAL_METRIC 等 RQ3 原生叶子。 | A.1 维度树 | 新增：从本审计 §4 的叶子表中补入。 | 🟡 |
| I03 | **A.1 维度树中的 leaf 名称不应使用通用术语**。如"leaf-llm4se-systematic-review-orig-se-task"等名称含 "orig"，但实际是通用投影而非原文原始字段。 | A.1 leaf 名称 | 重命名：使用本审计 §4 的叶子标识（如 `LLM_ARCH`、`SE_TASK` 等），直接对应原文字段。 | 🟡 |
| I04 | **SUMMARY 表的"原生树类型"字段可能需要修正**。当前标注为"单树"还是"维度森林"? | 快速结论卡片 | 修正为"维度森林"（如本审计 §0 结论卡片所定）。 | 🟡 |
| I05 | **缺少关系边表**。现有 review 有一段关系描述（§Discussion: 跨字段关系），但未形成正式的关系边表。 | A.1 | 新增：参照本审计 §5 的关系边表模板。 | 🟡 |

### 7.3 轻微级别（M）建议

| ID | 问题 | 位置 | 建议修改 |
|---|---|---|---|
| M01 | **§2.3 语料范围**描述偏重 RQ 列表，缺少对 extraction form（Table 5）的强调。Table 5 是该文编码 schema 的总入口，应显式引用。 | §2.3 | 在 §2.3 开头补充："提取 schema 来自 Table 5（8 个 data item），架构分类来自 Pan et al. [326]，SE task 分类为作者自建。" |
| M02 | **review 中对 challenges & opportunities (§8) 的描述应降级**：它不是编码叶子，而是从统计中推演的高级 discussion finding。 | §2.2, A.1 | 将 §8 内容明确标注为"discussion-derived finding（非编码维度）"，并移到 §6 候选 finding 区。 |
| M03 | **建议补 A.4 的 PDF 视觉核验结论**。当前 `needs_manual_check` 状态可考虑改为具体的 check 记录（即使失败也比 never-checked 强）。 | A.4 | 尝试用本地工具打开 paper.pdf 至少核验 Table 5、Fig.4、Table 17 的页码和编号一致性。 |

---

## 8. 审计附录草案：证据账本与结论映射

### 8.1 A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | §2.5 p.9--10 | Table 5 "Extracted data items and related RQs" | 8 个抽取数据项：SE task category, LLM category, LLM characteristics, data handling techniques, optimizer, evaluation metrics, SE activity, solutions/strategies | 编码 schema 定义 | **strong**（原文明确给出 extraction form 表） | 全部叶子字段的总入口 | 是。需 PDF 核验 Table 5 的完整行项与精确列名。 | 仅定义结构，不包含取值空间 |
| EV-002 | paper_content.txt | §3.1 p.10--11 | Fig.4 "Distribution of the LLMs" taxonomy tree | encoder-only / encoder-decoder / decoder-only 三分法 + 具体模型名（BERT(50), CodeBERT(51), GPT-4(53), ChatGPT(72), Codex(62), ...） | LLM 架构分类 + 频次 | **strong**（完整 taxonomy tree + 数字） | `LLM_ARCH`, `LLM_NAME` | 是。需 PDF 核验 Fig.4 的完整 tree 结构。 | 具体模型名不可迁移 |
| EV-003 | paper_content.txt | §3.1 p.11 | Table 6 "Summary of LLMs with different architectures" | 三类架构→SE task 类型映射 | 架构-任务适配关系 | **moderate**（分类清晰但每类仅举例，非穷尽） | `LLM_TASK_FIT`, EDGE_ARCH_TO_TASK | 是 | 关系结构可迁移 |
| EV-004 | paper_content.txt | §3.5 p.13--14 | §3.5 "Temporal trends" + Fig.5 | 逐年各架构 paper count 和百分比 | 时序趋势数据 | **strong**（有逐年数字） | `LLM_TREND`, EDGE_ARCH_TO_TREND | 是。需 PDF 核验 Fig.5 精确数字。 | 具体数字不可迁移 |
| EV-005 | paper_content.txt | §4.1--§4.2 p.16--17 | 四类数据源分类 + 数据类型枚举 | text-based / code-based / graph-based / software repository-based；programming tasks(42), prompts(33), source code(60), ... | 数据维度分类 + 频次 | **strong**（分类完整 + 有频次数字） | `DATA_SOURCE`, `DATA_TYPE` | 否（text 已有完整枚举和数字）。 | 分类结构可迁移 |
| EV-006 | paper_content.txt | §4.3 p.18--19 | Fig.7 (text pipeline) + Fig.8 (code pipeline) | 7-step preprocessing pipeline with step names | 预处理管道定义 | **strong**（有流程图的文本描述） | `DATA_PREPROC`, `CODE_REPR` | 是。需 PDF 核验 Fig.7/8 的图形完整性。 | 管道结构可迁移 |
| EV-007 | paper_content.txt | §4.4 p.20 | Table 8 "Various input forms of LLMs" | NL text, code snippets, code+NL, AST, CFG, PDG, screenshots, GUI hierarchy, ... | 输入形式枚举 | **moderate**（text 描述不完整；原文说"See Appendix B for the full table"） | `INPUT_FORM` | 是。需 PDF 核验 Table 8 + Appendix B 完整列表。 | 枚举部分可迁移 |
| EV-008 | paper_content.txt | §5.1--§5.2 p.22--26 | Fine-tuning, PEFT, prompt engineering 分类 | full FT, PEFT (LoRA/adapters/prefix), zero/few-shot, CoT, prompt design/tuning | 优化策略分类 | **strong**（分类完整，有方法描述和示例） | `OPT_STRATEGY` | 是。需 PDF 核验 Fig.9 prompt engineering techniques tree。 | 可迁移 |
| EV-009 | paper_content.txt | §5.4 p.26--27 | Table 9 "Common evaluation metrics" + problem type 分类 | generation/classification/recommendation/regression；BLEU, CodeBLEU, EM, accuracy, F1, pass@k, MRR, ... | 评价维度分类 | **moderate**（text 描述不完整；原文说"See Appendix D for the full table"） | `EVAL_PROBLEM_TYPE`, `EVAL_METRIC` | 是。需 PDF 核验 Appendix D 完整 metric 列表。 | 可迁移 |
| EV-010 | paper_content.txt | §6 p.34--37, p.77--79 | Table 16 (SE activities and tasks) + Table 17 (complete mapping) | 6-activity SDLC + 60+ specific tasks + paper counts per task + full reference list | SE 任务维度分类 + 频次 | **strong**（分类完整 + 全文引用表） | `SE_ACTIVITY`, `SE_TASK`, `SE_TASK_COUNT` | 是。需 PDF 核验 Table 17 的精确数字和完整引用映射。 | 分类结构可迁移；具体 task 名和频次不可迁移 |
| EV-011 | paper_content.txt | §2.5 p.9 | Fig.2(a)(b) venue/year distribution | 154 peer-reviewed / 241 arXiv；逐年 count | 元数据描述 | **strong**（有图有数字） | `VENUE_TYPE`, `PUB_YEAR` | 否 | 可迁移 |
| EV-012 | paper_content.txt | §8 p.41--47 | Challenges & Opportunities 全文 | model size, data dependency, ambiguity, generalizability, SE4LLM, security, ... | discussion-derived finding | **moderate**（有 reasoning 但非数据驱动） | 候选 finding C1--C7 | 否 | 仅启发，不可直接迁移 |

### 8.2 A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CONC-01 | 该 SLR 的原生编码树是以四个 RQ 为主干、395 primary studies 为根的维度森林，包含 19+ 原生叶子字段 | schema 判定 | `dim_root` + 全部叶子 | EV-001, EV-002, EV-005, EV-008, EV-010 | **strong** | 直接用于重写 review.md 的维度树定义 | 字段完整性依赖 PDF 视觉核验和 GitHub artifact 复核 |
| CONC-02 | 现有 review.md 的六叶通用接口树不是该论文的原生维度树，需要重写 | 返修诊断 | review.md A.1 维度树 | 对比 EV-001--EV-012 与现有 review 的六叶结构 | **strong** | 触发 C01 返修 | 如果 future audits 对比其他论文也有此问题，需建全局 review template |
| CONC-03 | 该论文的 extraction form (Table 5) + Appendix 引用表是其编码 schema 的可审计骨架 | schema 特征 | 全部叶子字段的来源 | EV-001, EV-010, EV-012 | **strong** | 启发 Paper2 建立类似的 extraction form + artifact | Table 5 仅 8 项，实际叶子更细粒（来自分类归纳而非逐项提取） |
| CONC-04 | 该论文的统计值只能进入 schema 结构统计池，不能进入 Paper2 目标领域证据池 | 迁移边界 | 全部领域统计值 | EV-002, EV-005, EV-010 的频次数字 | **strong** | 指导 Paper2 的 statistical synthesis eligibility | 如果 Paper2 报告 LLM4SE 领域背景时，可谨慎引用个别数字并注明来源 |
| CONC-05 | RQ1--RQ4 间的关系主要是平行维度编码，缺乏显式多变量交叉统计 | 方法论缺口 | EDGE 系列关系边 | EV-003, EV-004, 以及 §3--§6 行文定性叙述 | **moderate** | 启发 Paper2 补充多变量交叉分析 | 这是该 SLR 的方法学特征（非缺陷），不代表所有 SLR 都缺乏交叉统计 |
| CONC-06 | §8 Challenges & Opportunities 是 discussion-derived finding，不是编码维度 | 分类边界 | 候选 finding C1--C7 | EV-012 | **strong** | 区分编码树 vs. discussion finding | 部分 C-level finding 有编码统计支撑（如 model size 挑战来自 RQ1 的参数统计），但整体是推演而非直接编码 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取技能文件

| 文件 | 采用原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | claim-evidence engineering 原则：每个 major claim 必须有代码/结果/notes/verified citations 支撑；对不确定内容降级而非脑补。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 通用 reviewer 维度（originality, quality, clarity, significance, reproducibility, ethics）和常见 reviewer concerns 用于校准本审计的批判性视角。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 五维评分（contribution, writing clarity, experimental strength, evaluation completeness, method soundness）和 claim audit 流程。本次审计聚焦论文的编码 schema 而非全文 writing quality，故选择性采用。 |
| `research-planning/SKILL.md` | 四阶段规划范式（overall plan → architecture design → logic design → configuration）提醒本审计应区分维度树的不同层级（根→主干→叶子→取值空间）。 |
| `research-planning/references/planning-prompts.md` | Paper2Code 的 task dependency 思路 → 映射为本审计中维度树叶子间的"关系边"建模。 |
| `research-planning/references/output-schemas.md` | JSON schema 规范性提示：每个叶子应有明确的 type 和 allowed values。本审计用"取值空间"和"取值空间类型"来模拟。 |
| `autoresearch/SKILL.md` | validation-gated completion 原则：审计结论必须通过证据验证门，不能仅凭"读起来合理"。 |

### 9.2 最高风险 3 点

| # | 风险 | 说明 | 主线程合并时如何复核 |
|---|---|---|---|
| R1 | **PDF 视觉核验缺失** | 本审计基于 `paper_content.txt`（文本提取产物），未打开 `paper.pdf` 逐页核验。Fig.4 的 taxonomy tree、Table 5 的精确列名、Appendix A--E 的完整内容均依赖文本提取质量。如果 text 提取有遗漏/错位，取值空间枚举可能不完整。 | 主线程应：1) 打开 `paper.pdf` 至少核验 Table 5、Fig.4、Table 8、Table 17 的图/表编号和内容完整性；2) 对比本审计 §3 的维度树与 PDF 中的实际 taxonomy structure；3) 若有出入，以降级的 PDF 证据覆盖本审计结论。 |
| R2 | **叶子字段的完整性与归属不确定性** | 本审计从 `paper_content.txt` 的行文中复原了 19 个叶子字段，但原文有些字段（如 parameter size、optimizer）是在行文中提到而非在 Table 5 中显式定义。如果原文的 GitHub artifact 包含更完整的字段枚举，则本审计的叶子表可能需要扩展。 | 主线程应：1) 若环境允许，下载 GitHub artifact (`LLM4SE_SLR`) 检查实际数据表结构；2) 与本审计 §4 的叶子表比对；3) 标注"artifact-derived" vs "text-derived" 来源差异。 |
| R3 | **与现有 review.md 的返修冲突风险** | 本审计指出 C01（六叶通用树→原生维度森林）需要大幅重写 review.md 的 A.1 维度树。但现有 review 中还包含了 A.1DT-llm4se-systematic-review-C01--C12 等 12 个结论条目和新旧 transitional schema。如果返修时不保留这些历史条目作为"版本迁移记录"，可能丢失审计可追溯性。 | 主线程应在返修 review.md 时：1) 保留旧的 A.1DT 条目作为 `deprecated` 标记，在 A.1 中新增 `current` 标记的维度树；2) 更新快速结论卡片；3) 更新 SUMMARY 表的"原生树类型"和"统计池资格"字段。 |

### 9.3 Blocked / Timeout / 文件缺失

- **未 blocked**。所有必需文件（`paper_content.txt`, `bibtex.bib`, `metadata.json`, `review.md` 及 7 个技能/指南文件）均可读取。
- **未 timeout**。全文审计在单进程中完成。
- **PDF 版面核验缺失**：不是 blocked，而是已知的 `needs_manual_check` 状态（已在 §0 审计结论卡片和 §9.2 R1 中记录）。这不阻塞 schema_seed 级别的维度树复原和返修建议生成，但会在 A.2 证据账本中标记"需要原文版面核验"。

---

**审计报告结束。** 本报告为自包含完整文档，所有必填章节的实质内容已包含在内，可直接用于主线程重写 `review.md` 的维度树定义、补全 A.2/A.3 附录草案、并修正 SUMMARY 表中的相关字段。