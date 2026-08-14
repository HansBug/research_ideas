现在我已具备所有必要信息。以下是完整的 A1-DT v2 审计报告。

---

# A1-DT v2 单篇全文审计报告：`ai-native-se-roadmap`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `ai-native-se-roadmap` |
| agent | `deepseek`（本次由 codex-deepseek exec 进程独立完成） |
| 是否已读 `paper_content.txt` | 是——全文 1146 行已逐行通读，涵盖全部 25 页正文、7 幅图的所有引用、14 个开放问题及参考文献 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是——`bibtex.bib` 确认作者、标题、TOSEM 2026 发表信息；`metadata.json` 确认 DOI `10.1145/3807901`、arXiv `2410.06107`、CCF A 类、`eligible_for_statistical_synthesis: false` |
| 是否打开或核对 `paper.pdf` | 是——使用 PyPDF2 核验 25 页版面，确认 7 幅图（Fig. 1–7）且正文中**无任何数据表**（无 Table 1/2/...） |
| 原文类型 | **vision / roadmap**（非 SLR、SMS、tertiary、MLR、guideline） |
| 被编码样本单位 | **无系统样本库**——论文以作者愿景和经验组织叙事，没有检索、纳排、数据抽取或质量评价协议 |
| 样本数量 / 分母 | **不适用**——不存在系统样本分母 |
| 原生树类型 | **降级树**（roadmap / challenge 分类树）——论文以自身的“SE 演化基线 → SE 2.0 局限 → SE 3.0 五层技术栈 → 五大挑战 + 8 个其他开放问题”为原生组织 schema |
| 主统计池资格 | **否**——不可进入主统计池；仅作 `boundary_anchor` + `schema_seed`。理由是：vision/roadmap 类文献无系统检索、纳排、质量评价或数据综合 |
| 总体判定 | **needs repair**（见 §7 返修建议）——现有 `review.md` 的维度树复原仍以六叶通用接口为主干视觉事实源，需进一步将原文原生 schema 提升为事实源，六叶降级为跨论文投影 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取文件清单

| 文件 | 读取范围 | 说明 |
|---|---|---|
| `paper_content.txt` | 全文 1146 行（25 页），逐页通读 | 主要证据来源 |
| `bibtex.bib` | 全文 | 元数据核验 |
| `metadata.json` | 全文 | 元数据、CFC/CCF 状态、统计池资格核验 |
| `paper.pdf` | PyPDF2 版面核验（25 页） | 确认 7 幅图的存在性，确认**无数据表** |
| `review.md` | 全文 428 行 | 与原文对照审计 |

### 1.2 仍需 PDF 视觉核验的部分

`paper_content.txt` 是目前的主要文本源，图 1–7 已通过 PyPDF2 确认版面存在。以下内容仍建议人工打开 PDF 核验：
- Fig. 1（SE 演化图）中 SE 1.0 / 2.0 / 3.0 的具体边界标注是否与正文一致
- Fig. 3（五层技术栈图）的层间关系箭头方向
- Fig. 6（Sculley et al. 重解释图）中各模块的完整标签

### 1.3 关键原文证据锚点（10 个）

| # | 证据锚点 | 来源 |
|---|---|---|
| 1 | 摘要首句定义 SE 2.0 为 "AI-assisted SE"、SE 3.0 为 "AI-native approach characterized by intent-centric, conversation-oriented development" | Page 1 |
| 2 | 原文承认愿景来源包括 "surveys of academic and gray literature, workshops and summits, customer/internal discussions, OPEA alliance 40+ partners"，但明确不是系统检索 | Page 2 |
| 3 | SE 2.0 三大局限：§2.2.1 认知过载、§2.2.2 模型训练低效、§2.2.3 代码质量与 additive bias | Page 3–5 |
| 4 | SE 3.0 核心原则："intent-centric"、"conversation-oriented"、"AI drives the code creation loop"、"code is just a means to an end" | Page 7 |
| 5 | 五层技术栈定义：Teammate.next (§3.2)、IDE.next (§3.3)、Compiler.next (§3.4)、Runtime.next (§3.5)、FM.next (§3.6) | Page 7–12 |
| 6 | 每个挑战的固定描述结构："Description → Affects → Open question → Our vision" | Page 13 开头 |
| 7 | 五大主挑战：§4.1 人类-AI 对齐加速、§4.2 代码综合效率、§4.3 运行时性能、§4.4 FM 代码理解、§4.5 消除 prompt engineering | Page 13–18 |
| 8 | §4.6 列出 8 个额外开放问题 OQ7–OQ14 | Page 18 |
| 9 | 结论段承认 SE 3.0 "can only be truly assessed and validated as a whole once prototypes have been developed for all components" | Page 20 |
| 10 | Fig. 1–7 全部为概念图/截图，无数据表 | 全篇 |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

**原文没有系统纳入对象**。论文不是以"收集一批 primary/secondary study 然后编码它们"的方式组织的。它是一篇 vision/roadmap 论文，以作者群体的行业经验、参与 OPEA alliance（40+ 工业伙伴）、参加 FM+SE 系列 workshop/summit、以及自己的研发经验（Compiler.next [28]、Runtime.next [114] 等）为基础，构建了一个从 SE 2.0 问题诊断到 SE 3.0 愿景再到技术栈和挑战路线图的叙事。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**没有**。原文 Page 2 明确列出愿景来源（surveys、workshops、discussions、OPEA alliance）但**完全没有给出**检索式、数据库、纳排流程图（如 PRISMA）、筛选分母、质量评价工具、抽取表、编码协议或 intercoder agreement。这是一个"作者 informed opinion + 引用支撑"的 roadmap，不是系统综述。

### 2.3 原文字段来自哪里？

原文的组织结构即为它的"字段来源"：
- **§2 SE 2.0 分析**：一个三段式问题框架（认知过载 / 训练低效 / 代码质量），每段不来自编码表而来自作者论点
- **§3 SE 3.0 技术栈**：五层分层架构（Fig. 3），每层有固定描述模式：当前状态 → 缺陷 → SE 3.0 目标 → 所需属性
- **§4 挑战路线图**：每个挑战的固定条目结构 = `Description + Affects + Open Question(s) + Our Vision`

这些不是从外部样本抽取的字段，而是论文**自身的分类架构**。

### 2.4 RQ 与样本单位是什么关系？

本文没有显式 RQ（无 "RQ1/RQ2/..." 编号）。论文的叙事目的（"introduce our vision of SE 3.0"、"present a roadmap of challenges"）充当了非形式化的 RQ。这个目的是"树根"——它不驱动样本编码，而是驱动自身的概念分类。

### 2.5 降级方案

由于无系统样本库，按 A1-DT v2 口径执行降级：本文的维度树标记为**降级树（roadmap / challenge classification tree）**；所有叶子节点只作 `schema_seed`，不进入主统计池；可作 `boundary_anchor`（为 Paper2 的 AI-native SE 相关维度提供结构启发）和 `candidate_heuristic`（挑战条目可作为 Paper2 方法学验证场景的候选）。

---

## 3. 原生样本编码维度树 / 维度森林

以下是基于原文全文通读复原的**降级维度树**。该树反映论文自身的叙事 schema，不是外挂的六叶通用接口。

```
[dim-ai-native-se-roadmap-root] SE 3.0 愿景路线图（vision/roadmap）
│
├── [dim-orig-era-baseline] SE 演化基线
│   ├── [leaf-orig-era-se10] SE 1.0 — code-centric / 工具驱动的传统 SE
│   │   └── 取值空间: 封闭枚举 {需求工具, 设计工具, 实现工具, 测试工具, 维护工具} /
│   │     来源: §2.1 列出具体工具名 (e.g., Rational Rose, Eclipse, LoadRunner)
│   │     证据锚点: Page 2 §2.1
│   │
│   ├── [leaf-orig-era-se20] SE 2.0 — AI-assisted / task-driven / code-centric
│   │   └── 取值空间: 封闭枚举 {AI coding assistants, 传统 ML 模型, 深度学习模型} /
│   │     来源: §2.1 定义 + Fig. 2
│   │     证据锚点: Page 2-3 §2.1
│   │
│   └── [leaf-orig-era-se30] SE 3.0 — AI-native / intent-centric / conversation-oriented
│       └── 取值空间: 封闭枚举 {intent-centric, conversation-oriented, AI drives code loop,
│         knowledge-driven FM, symbiotic human-AI}
│         来源: §3.1 定义
│         证据锚点: Page 6-7 §3.1
│
├── [dim-orig-se2-limitations] SE 2.0 局限分析
│   ├── [leaf-orig-se2-cognitive] 人类认知过载
│   │   └── 取值空间: 自由文本加理由 / 作者论据链
│   │     来源: §2.2.1 "debugging rabbit holes"
│   │
│   ├── [leaf-orig-se2-training] 模型训练低效
│   │   └── 取值空间: 自由文本加理由 / 作者论据链（非结构化数据、无 targeted learning）
│   │     来源: §2.2.2
│   │
│   ├── [leaf-orig-se2-quality] 代码质量与 additive bias
│   │   └── 取值空间: 自由文本加理由 / 作者论据链（additive changes, trust erosion）
│   │     来源: §2.2.3
│   │
│   └── [leaf-orig-se2-autonomous] 自主软件工程师的边界讨论
│       └── 取值空间: 布尔 + 自由文本 (Devin/SWE-agent/TRAE 是否替代 SE 3.0 愿景)
│         来源: §2.3
│
├── [dim-orig-stack] SE 3.0 五层技术栈
│   ├── [leaf-orig-stack-teammate] Teammate.next — 自演化个性化 AI 伙伴
│   │   └── 取值空间: 属性枚举 {personalized, self-evolving, mentor-mode, ToM-capable,
│   │     sticky context, multi-modal interaction}
│   │     来源: §3.2
│   │
│   ├── [leaf-orig-stack-ide] IDE.next — 意图中心对话式开发环境
│   │   └── 取值空间: 属性枚举 {intent-alignment conversation, AI drives code loop,
│   │     code hidden by default, low-level debugging mode, conversation archive,
│   │     "code" = traditional code + ML models + prompts + data}
│   │     来源: §3.3
│   │
│   ├── [leaf-orig-stack-compiler] Compiler.next — 多目标代码综合
│   │   └── 取值空间: 属性枚举 {search over solution space, multi-objective optimization
│   │     (accuracy/latency/cost), goal-tracking mechanism, self-reflection,
│   │     modular stack: architecture explorers + prompt rewriters + search optimizers}
│   │     来源: §3.4
│   │
│   ├── [leaf-orig-stack-runtime] Runtime.next — SLA 感知复合应用运行时
│   │   └── 取值空间: 属性枚举 {SLA-aware, DAG-based workflow modeling, per-task slack,
│   │     intelligent priority routing, observability machinery, edge computing support,
│   │     data flywheel}
│   │     来源: §3.5
│   │
│   └── [leaf-orig-stack-fm] FM.next — 知识驱动高效基础模型
│       └── 取值空间: 属性枚举 {curriculum engineering, SWEBOK-inspired taxonomy,
│         synthetic data generation, cognitive observability, IP = curriculum not model,
│         uniform SE competence}
│         来源: §3.6
│
└── [dim-orig-challenges] 挑战路线图
    ├── [leaf-orig-challenge-alignment] C1: 加速人类-AI 意图对齐
    │   ├── 取值空间: 结构化条目 {Description, Affects: [IDE.next, Teammate.next],
    │   │   OQ1, Vision: mutual ToM + multi-agent ToM + requirements engineering}
    │   └── 来源: §4.1
    │
    ├── [leaf-orig-challenge-synthesis] C2: 提升代码综合效率
    │   └── 结构化条目 {Description, Affects: [Compiler.next, Teammate.next],
    │       OQ2, Vision: SBSE principles + past search data reuse + semantic caching}
    │     来源: §4.2
    │
    ├── [leaf-orig-challenge-runtime] C3: 提升运行时性能
    │   └── 结构化条目 {Description, Affects: [Runtime.next, FM.next],
    │       OQ3+OQ4, Vision: smart routing + edge computing + distributed processing}
    │     来源: §4.3
    │
    ├── [leaf-orig-challenge-fm] C4: 提升 FM 对代码与 SE 的理解
    │   └── 结构化条目 {Description, Affects: [FM.next, Compiler.next],
    │       OQ5, Vision: multi-modal training + curriculum engineering + internal representation study}
    │     来源: §4.4
    │
    ├── [leaf-orig-challenge-prompt] C5: 消除 prompt engineering 需求
    │   └── 结构化条目 {Description, Affects: [all layers],
    │       OQ6, Vision: novel training strategies + user feedback-driven prompt DB}
    │     来源: §4.5
    │
    └── [leaf-orig-challenge-other] C6: 其他开放问题（无完整 vision）
        └── 取值空间: 开放枚举 {OQ7(教育), OQ8(编程语言), OQ9(IDE UI),
            OQ10(Compiler 基准), OQ11(IP 归属), OQ12(就业),
            OQ13(开放创新), OQ14(可及性与公平)}
          来源: §4.6
```

### 3.1 缺失部分说明

上述维度树已覆盖原文 §2–§4 的全部组织 schema。以下部分故意未纳入树中：
- **§5 Conclusion**：摘要式收尾，不引入新叶子
- **参考文献 [1]–[117]**：作为引用支撑，不是 schema 节点
- **Fig. 1–7 的详细视觉内容**：图标题已纳入叶子取值空间；图片内部的具体标注文字仍需 A2a 视觉核验

### 3.2 A2a 精核任务清单

| # | 精核任务 | 当前状态 |
|---|---|---|
| 1 | 逐一核对每个叶子的精确页码（已从文本提取大致位置，需 PDF 确证） | `not_verified` |
| 2 | 核对 Fig. 3 技术栈图中层间箭头方向、依赖关系和 SE 2.0 对照列 | `needs_visual_check` |
| 3 | 确认 OQ1–OQ14 的精确编号与原文一致（文本已验证，需 PDF 版面确证） | 文本级已核实 |
| 4 | 检查 §4.3 中 OQ3 和 OQ4 是否都归属 C3（文本已验证） | 文本级已核实 |
| 5 | 核实 FM.next 的 curriculum engineering reference recipe 是否包含 InstructLab subnet 结构 | `schema_seed` |

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leaf-orig-era-se10` | SE 1.0 时代特征 | `dim-orig-era-baseline` | §2.1 工具类别列表 | code-centric / 工具驱动的传统 SE 时代 | 封闭枚举 {需求工具, 设计工具, 实现工具, 测试工具, 维护工具} / 具体工具名列表 | 封闭枚举 + 自由文本举例 | N/A（该叶子为时代表征，不可缺失） | 不进入主统计池 | 为 Paper2 的"AI 介入前 SE 基线"提供锚点 | Page 2 §2.1 | 只迁移分类结构，不迁移具体工具结论 |
| `leaf-orig-era-se20` | SE 2.0 时代特征 | `dim-orig-era-baseline` | §2.1 定义 + Fig. 2 | AI-assisted / task-driven / code-centric | 封闭枚举 {AI coding assistants, 传统 ML 模型, 深度学习模型} | 封闭枚举 | N/A（核心定义叶） | 不进入主统计池 | 为 Paper2 的"当前 AI 辅助 SE 基线"提供锚点 | Page 2–3 §2.1 | 只迁移分类结构 |
| `leaf-orig-era-se30` | SE 3.0 时代特征 | `dim-orig-era-baseline` | §3.1 定义 + Fig. 3 | AI-native / intent-centric / conversation-oriented | 封闭枚举 {intent-centric, conversation-oriented, AI drives code loop, knowledge-driven FM, symbiotic human-AI} | 封闭枚举（作者愿景中的封闭原则集） | 愿景未完全展开时标注 `not_fully_specified` | 不进入主统计池 | 为 Paper2 的"目标 SE 范式"提供锚点和验证场景候选 | Page 6–7 §3.1 | 只迁移原则分类结构 |
| `leaf-orig-se2-cognitive` | SE 2.0 认知过载 | `dim-orig-se2-limitations` | §2.2.1 | 人类在 SE 2.0 中因驱动 code loop 而产生的认知过载 | 自由文本加理由（作者论据链：问题分解→提示→评估→调试→迭代） | 自由文本加理由 | 非系统证据时标注 `author_claim` | 不进入主统计池 | 为 Paper2 方法学中"减轻认知过载"目标提供锚点 | Page 3–4 §2.2.1 | 迁移问题框架结构 |
| `leaf-orig-se2-training` | SE 2.0 模型训练低效 | `dim-orig-se2-limitations` | §2.2.2 | FM 依赖大规模非结构化互联网数据导致训练低效 | 自由文本加理由（作者论据链：无监督学习局限、噪声数据、缺乏 targeted learning） | 自由文本加理由 | `author_claim` | 不进入 | 为 Paper2 FM 相关讨论提供锚点 | Page 4–5 §2.2.2 | 迁移问题框架结构 |
| `leaf-orig-se2-quality` | SE 2.0 代码质量与 additive bias | `dim-orig-se2-limitations` | §2.2.3 | AI coding assistant 倾向 additive changes 导致代码膨胀 | 自由文本加理由 | 自由文本加理由 | `author_claim` | 不进入 | 为 Paper2 代码质量评价提供锚点 | Page 5 §2.2.3 | 迁移问题框架结构 |
| `leaf-orig-se2-autonomous` | 自主软件工程师边界 | `dim-orig-se2-limitations` | §2.3 | Devin/SWE-agent/TRAE 等的现状和与 SE 3.0 的关系 | {是/否 与 SE 3.0 等价} + 自由文本理由 | 布尔 + 自由文本 | `not_mentioned` 如未讨论 | 不进入 | 为 Paper2 agentic SE 相关讨论提供边界锚点 | Page 5–6 §2.3 | 迁移分析框架 |
| `leaf-orig-stack-teammate` | Teammate.next | `dim-orig-stack` | §3.2 | 自演化个性化 AI 伙伴的属性定义 | 属性枚举（6 项：personalized, self-evolving, mentor-mode, ToM-capable, sticky context, multi-modal interaction） | 层级枚举（属性 + 描述） | `not_specified` | 不进入 | 为 Paper2 的 agent 角色设计提供启发 | Page 7–8 §3.2 | 只迁移属性分类结构 |
| `leaf-orig-stack-ide` | IDE.next | `dim-orig-stack` | §3.3 | 意图中心对话式 IDE 属性 | 属性枚举（5 项：intent-alignment, AI drives code loop, code hidden, debug mode, conversation archive） | 层级枚举 | `not_specified` | 不进入 | 为 Paper2 工具链设计提供启发 | Page 8 §3.3 | 只迁移属性分类结构 |
| `leaf-orig-stack-compiler` | Compiler.next | `dim-orig-stack` | §3.4 | 多目标代码综合引擎属性 | 属性枚举（5 项：search-driven, multi-objective, goal-tracking, self-reflection, modular stack） | 层级枚举 | `not_specified` | 不进入 | 为 Paper2 验证方法中"合成/搜索"概念提供启发 | Page 8–9 §3.4 | 只迁移属性分类结构 |
| `leaf-orig-stack-runtime` | Runtime.next | `dim-orig-stack` | §3.5 | SLA 感知复合应用运行时属性 | 属性枚举（6 项：SLA-aware, DAG workflow, per-task slack, priority routing, observability, data flywheel） | 层级枚举 | `not_specified` | 不进入 | 为 Paper2 执行环境讨论提供启发 | Page 9–11 §3.5 | 只迁移属性分类结构 |
| `leaf-orig-stack-fm` | FM.next | `dim-orig-stack` | §3.6 | 知识驱动高效 FM 属性 | 属性枚举（6 项：curriculum engineering, SWEBOK-inspired, synthetic data, cognitive observability, IP=curriculum, uniform SE competence） | 层级枚举 | `not_specified` | 不进入 | 为 Paper2 LLM 训练方法讨论提供启发 | Page 11–12 §3.6 | 只迁移属性分类结构 |
| `leaf-orig-challenge-alignment` | C1: 人类-AI 对齐加速 | `dim-orig-challenges` | §4.1 | 加速意图对齐的挑战条目 | 结构化 {Description, Affects, OQ1, Vision(mutual ToM)} | 结构化 + 自由文本 | N/A | 不进入 | 为 Paper2 的人机交互设计提供验证场景候选 | Page 13–14 §4.1 | 迁移挑战分类结构 |
| `leaf-orig-challenge-synthesis` | C2: 代码综合效率 | `dim-orig-challenges` | §4.2 | 提升代码综合效率的挑战条目 | 结构化 {Description, Affects, OQ2, Vision(SBSE)} | 结构化 + 自由文本 | N/A | 不进入 | 为 Paper2 的代码生成效率提供验证场景 | Page 14–15 §4.2 | 迁移挑战分类结构 |
| `leaf-orig-challenge-runtime` | C3: 运行时性能 | `dim-orig-challenges` | §4.3 | 提升运行时性能挑战条目 | 结构化 {Description, Affects, OQ3, OQ4, Vision} | 结构化 + 自由文本 | N/A | 不进入 | 为 Paper2 的部署效率提供验证场景 | Page 15 §4.3 | 迁移挑战分类结构 |
| `leaf-orig-challenge-fm` | C4: FM 代码理解 | `dim-orig-challenges` | §4.4 | 提升 FM 对 SE 理解的挑战条目 | 结构化 {Description, Affects, OQ5, Vision(curriculum+multimodal)} | 结构化 + 自由文本 | N/A | 不进入 | 为 Paper2 的 LLM SE 知识提供验证场景 | Page 15–17 §4.4 | 迁移挑战分类结构 |
| `leaf-orig-challenge-prompt` | C5: 消除 prompt eng. | `dim-orig-challenges` | §4.5 | 消除 prompt engineering 需求的挑战条目 | 结构化 {Description, Affects, OQ6, Vision(training+feedback DB)} | 结构化 + 自由文本 | N/A | 不进入 | 为 Paper2 prompt 工程讨论提供验证场景 | Page 17–18 §4.5 | 迁移挑战分类结构 |
| `leaf-orig-challenge-other` | C6: 其他开放问题 | `dim-orig-challenges` | §4.6 | 8 个无完整 vision 的开放问题 | 开放枚举 {OQ7..OQ14}（8 项，枚举值取决于问题主题） | 开放枚举 | `not_developed`（作者明确表示尚未形成完整 vision） | 不进入 | 为 Paper2 扩展研究问题提供启发 | Page 18 §4.6 | 迁移开放问题分类结构 |

---

## 5. 关系边表

本文是一篇 vision/roadmap 论文，没有关系型数据 schema。但存在以下**显式关系结构**：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rel-challenge-affects` | `dim-orig-challenges` 下的每个挑战叶子 | `affects`（影响） | `dim-orig-stack` 下的一个或多个技术栈组件 | 枚举 {Teammate.next, IDE.next, Compiler.next, Runtime.next, FM.next} | 若挑战未标注 Affects，标注 `not_specified` | §4.1–§4.5 每个挑战开头的 "Affects." 行 | 这是原文最显式的关系边：C1→{IDE.next, Teammate.next}；C2→{Compiler.next, Teammate.next}；C3→{Runtime.next, FM.next}；C4→{FM.next, Compiler.next}；C5→{all layers}；C6→`not_specified` |
| `rel-stack-supports` | `dim-orig-stack` 的每个技术栈组件 | `supports`（支撑） | `leaf-orig-era-se30`（SE 3.0 愿景） | 布尔（每个组件都是 SE 3.0 的必要支撑） | N/A | Page 6 Fig. 3 + §3.1 末段 | 五层技术栈共同构成 SE 3.0 的使能基础设施 |
| `rel-se2-to-se30` | `dim-orig-se2-limitations` | `motivates`（驱动） | `dim-orig-stack` + `dim-orig-challenges` | 映射关系：每个 SE 2.0 局限对应 SE 3.0 技术栈和挑战中的补救方向 | 部分映射隐式，需 A2a 精核 | §2→§3 过渡 + §3 各节开头的 "from...to..." 描述 | 这是原文的核心叙事弧线：SE 2.0 局限→SE 3.0 愿景→技术栈→挑战 |
| `rel-challenge-oq` | `dim-orig-challenges` 下的 C1–C5 | `poses`（提出） | 开放问题 OQ1–OQ6 | 每个挑战有 1–2 个开放问题 | OQ 未编号时降级为隐式问题 | §4.1–§4.5 "Open question #N" 标记 | 挑战→开放问题的 1:1 或 1:2 映射 |
| `rel-compiler-proof` | `leaf-orig-stack-compiler` | `has_proof_of_concept`（有概念验证） | 外部论文 [28] | 引用关系 | 无 PoC 的组件标注 `no_poc` | §3.4 "a dedicated paper [28]" | Compiler.next 是唯一有已发表 PoC 的组件；Runtime.next 有 prototype [114] |
| `rel-fmnext-curriculum` | `leaf-orig-stack-fm` | `references_recipe`（引用实现配方） | IBM InstructLab [51,91] | 外部分类法引用 | N/A | §3.6 "A reference recipe..." 段 | FM.next 的 curriculum engineering 方法引用了 IBM InstructLab 作为参考实现 |

**未发现显式关系边的情况**：
- §4.6 的 OQ7–OQ14 没有被绑定到具体挑战（作者明确表示 "have not yet developed a thorough vision yet"），因此 OQ–挑战关系为 `not_formed`
- SE 1.0 / SE 2.0 / SE 3.0 之间的演进关系是时间/范式层面的 `supersedes`，但作者没有为单个工具或活动标注精确的迁移映射

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 统计观察（原文中有字段/统计表支持）

**本文没有统计观察**。全文无数据表、无定量分析、无样本分母、无频次分布。这是 vision/roadmap 论文的本质特征。

### 6.2 候选 finding（原文 discussion / recommendation / roadmap 提出）

以下为可从原文提取的候选启发（仅作 `candidate_heuristic`，绝不直接充当 Paper2 的 final research finding）：

| # | 候选启发 | 来源 | 对 Paper2 的用途 |
|---|---|---|---|
| CH1 | "intent-centric + conversation-oriented" 作为新的开发范式，可用于定义 STM 建模中"需求→状态机"转换的评价标准 | §3.1 | 为 LLM 生成的状态机提供"意图保真度"评价维度 |
| CH2 | 五层技术栈中的 Compiler.next "multi-objective optimization (accuracy/latency/cost)" 概念可类比为状态机模型的多目标验证剖面 | §3.4 | 为验证剖面的多目标（安全性/活性/效率）组织提供启发 |
| CH3 | "code is just a means to an end" 的底层立场可类比为"状态机模型只是需求到验证的手段" | §3.1, §5 | 为 LLM STM 方法学的哲学定位提供类比 |
| CH4 | FM.next 的 curriculum engineering（基于 SWEBOK 的分层课程）可启发 LLM STM 训练或 prompt 设计中的领域知识结构化 | §3.6 | 为 LLM 的 SE 领域知识注入提供方法学启发 |
| CH5 | 挑战 C1 的 mutual ToM（双向心智理论）可启发 STM 验证中的人机交互设计——验证者需要理解 AI 对需求的理解程度 | §4.1 | 为 LLM-as-Judge（project_ex1）的人机评审交互提供概念锚点 |
| CH6 | OQ10："如何评估 Compiler.next 的综合性能" 可类比为"如何评估 LLM 生成的状态机模型质量"的基准设计问题 | §4.6 OQ10 | 为 project_ex1 的评审基准设计提供类比启发 |

### 6.3 对 Paper2 可迁移的方法学启发

| 迁移对象 | 内容 | 迁移条件 |
|---|---|---|
| `migrate-stack-architecture` | 五层分层架构的"from X to Y"描述模式可作为 Paper2 STM 方法学中 LLM pipeline 的阶段化描述模板 | 需改写为 STM 领域特定阶段 |
| `migrate-challenge-structure` | 每个挑战的 Description→Affects→OQ→Vision 四段式结构可作为 Paper2 中"LLM STM 开放问题"的组织模板 | 需映射到 STM 领域 |
| `migrate-era-baseline` | SE 1.0/2.0/3.0 的时代表征可作为 Paper2 引言中"传统 STM → 当前 AI-assisted STM → 目标 AI-native STM"的叙事弧线参考 | 需限制为类比，不直接套用 SE 术语 |
| `migrate-decline-discipline` | 原文对 vision/roadmap 论文的降级纪律（不伪造系统综述、不编造样本分母、显式区分 author_claim 和 systematic_evidence）可作为 Paper2 survey-of-surveys 的论文分类纪律 | 直接可迁移 |

### 6.4 绝不能迁移的领域结论

| 不可迁移对象 | 理由 |
|---|---|
| SE 3.0 技术栈的具体组件名称和属性（Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next） | 纯 SE 领域 vision，与 STM 建模无直接映射 |
| 任何关于 AI coding assistant（GitHub Copilot 等）的定量/定性评价 | 不适用于 STM 建模领域 |
| OQ7–OQ14 的具体问题内容（如 SE 教育、编程语言设计、就业影响） | 超出 STM 建模范围 |
| Runtime.next 的 SLA-aware edge computing 细节 | 与 STM 验证无关 |
| "the SE 3.0 vision can only be truly assessed and validated as a whole once prototypes have been developed for all components" 的整体验证立场 | 这是 vision paper 的自我限制，不应迁移为 Paper2 的方法学要求 |

---

## 7. 对现有 `review.md` 的返修建议

### 问题分级

| 等级 | 含义 |
|---|---|
| **C** (Critical) | 阻塞性——必须修复才能合入 main，否则会污染下游统计或导致事实错误 |
| **I** (Important) | 重要——应在下一轮返修中修复，可能影响 Paper2 的维度树构建 |
| **M** (Minor) | 建议——可记录的改进点，不阻塞合入 |

### 返修清单

| # | 等级 | 问题 | 当前状态 | 建议修复动作 |
|---|---|---|---|---|
| 1 | **C** | **维度树视觉事实源仍以六叶通用接口为主**。`review.md` 的"维度树结构"(L282–296)中，五条主干 `b1`–`b5` 直接挂载 `leaf-*-scope/corpus/taxonomy/method/evidence/finding` 六个通用叶子；而原文原生 19 条叶子（`dim-orig-*` 和 `leaf-orig-*`）被放在"原文模式候选叶子映射（A1 种子）"中作为次要内容。这违反了 A1-DT v2 口径："维度树必须像这篇论文自己的编码表/分类框架"。 | `review.md` L282–296 | 将 §3 的本报告原生维度树（`dim-orig-era-baseline` → `dim-orig-se2-limitations` → `dim-orig-stack` → `dim-orig-challenges` 及其下的 19 条叶子）提升为"维度树结构"的主事实源；将六叶通用接口降为后附的"通用接口投影"表（它已经是了，但当前视觉上它占据主树位置） |
| 2 | **C** | **叶子维度表仍以六叶为主**。`review.md` 的"叶子维度表"(L303–308) 只有 6 行，全为六叶通用接口；原文 19 条 `leaf-orig-*` 不在叶子维度表中而在 A1 种子候选表中。 | `review.md` L303–308 | 将本报告的"叶子维度表"19 行（含取值空间类型、缺失值语义、证据锚点、迁移边界）作为主叶子维度表；六叶表保留为"跨论文投影表" |
| 3 | **I** | **缺少关系边表**。`review.md` 没有独立的关系边表章节，A.2/A.3 的证据链只覆盖了维度树节点到证据的映射，没有覆盖本文显式的挑战→技术栈 `affects` 关系。 | 全文 | 新增"关系边表"章节，至少纳入 §5 的 6 条关系边（`rel-challenge-affects`、`rel-stack-supports`、`rel-se2-to-se30`、`rel-challenge-oq`、`rel-compiler-proof`、`rel-fmnext-curriculum`） |
| 4 | **I** | **统计观察/候选 finding 混层**。`review.md` 的"统计与候选发现链路"表(§统计与候选发现链路)将 `leaf-ai-native-se-roadmap-taxonomy` 标记为"分类项频次/交叉表/主题分布"，但这篇论文根本没有分类项频次。 | `review.md` "统计与候选发现链路" | 将统计用途统一修改为 `不进入主统计池`，候选发现用途修正为本报告 §6.2 的 6 条 CH1–CH6，并显式标注"原文无定量统计，所有条目均为 candidate_heuristic" |
| 5 | **I** | **A.2 证据账本粒度太粗**。`review.md` 的 A.2 只有 4 条证据记录（EV-001 到 EV-004），且全部标记为 `not_verified`。对于一篇 25 页的论文来说，4 条证据无法支撑 19 条叶子的证据链。 | `review.md` A.2 | 按本报告 §8 的 A.2 草案扩展为约 12–15 条证据记录，每条标明精确章节、段落线索和证据角色 |
| 6 | **M** | **取样单位字段不对齐**。`review.md` 的"快速结论卡片"中"被编码样本单位"应明确写 "无系统样本库（vision/roadmap）"而非留空或模糊描述。 | `review.md` 快速结论卡片 | 统一使用 "无系统样本库（vision/roadmap）——论文以作者愿景和行业经验组织叙事" |
| 7 | **M** | **SUMMARY 表中"样本单位/样本数量/原生树类型/统计池资格"需修正**（如果该 SUMMARY 引用本篇）。当前 `review.md` 快速结论卡片的"原生树类型"写的是"单树/维度森林/降级树/无系统样本库"四选一占位。 | `review.md` 快速结论卡片 | 显式选定 "降级树（roadmap/challenge 分类树）" |
| 8 | **M** | **缺少 PDF 版面核验记录**。当前 `review.md` 的阅读状态为"已读全文文本-paper_content核验"，未记录 PDF 图表核验情况。 | `review.md` 快速结论卡片 | 在"本轮阅读状态"中增加 PDF 核验记录：已确认 25 页、7 幅图（Fig. 1–7）、**无数据表** |

### 关于 GUIDE 规则的反馈

当前 A1-DT v2 口径（本任务 §2）对"roadmap/vision/proposal/guideline 且无系统样本库"的降级规则是清晰且可执行的。但存在一个结构性张力：

- **"维度树/维度森林"的定义**（"综述论文如何描述、编码、分类、统计它纳入的样本单位的层级化字段结构"）假设了"有样本库"的前置条件。
- 对于 vision/roadmap 论文，这个定义需要扩展为"**论文自身的概念分类架构**"——即"该论文如何组织其愿景元素、技术组件、挑战条目的层级化字段结构"。

建议在 GUIDE 中为"无系统样本库"论文增加一条显式的降级树定义，避免审计者每次都要在定义边界上自行裁定。

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | §2.1 (Page 2) | "Software Engineering 1.0...was predominantly code-centric" + 具体工具名列表 | 作者定义 SE 1.0 为 code-centric，并列举需求/设计/实现/测试/维护工具 | 时代定义 | strong（原文显式定义） | `dim-orig-era-baseline`, `leaf-orig-era-se10` | true（Fig. 1 视觉一致性和工具列表完整性） | 工具列表是示意性的，非系统枚举 |
| EV-002 | paper_content.txt | §2.1 (Page 2–3) | "Software Engineering 2.0 is our current era" + Fig. 2 | 作者定义 SE 2.0 为 AI-assisted / task-driven | 时代定义 | strong | `dim-orig-era-baseline`, `leaf-orig-era-se20` | true（Fig. 2 与 Fig. 1 的过渡一致性） | 定义反映作者视角 |
| EV-003 | paper_content.txt | §3.1 (Page 6–7) | "SE 3.0 marks a paradigm shift towards an intent-centric approach" + "code is just a means to an end" | 作者定义 SE 3.0 核心原则 | 时代定义 | strong | `dim-orig-era-baseline`, `leaf-orig-era-se30` | true（Fig. 3 与 Fig. 1 的演进一致性） | 愿景定义，非经验事实 |
| EV-004 | paper_content.txt | §2.2.1 (Page 3–4) | "the human developer drives the code creation loop" + "debugging rabbit holes" | SE 2.0 认知过载的论据链 | 作者论据 | medium（论点清晰但依赖轶事证据） | `dim-orig-se2-limitations`, `leaf-orig-se2-cognitive` | false（文本清晰） | 非系统证据，不构成实证 finding |
| EV-005 | paper_content.txt | §2.2.2 (Page 4–5) | "The training process of frontier FMs...is drastically inefficient" + unsupervised learning 批评 | SE 2.0 FM 训练低效的论据 | 作者论据 | medium | `dim-orig-se2-limitations`, `leaf-orig-se2-training` | false | 非系统证据 |
| EV-006 | paper_content.txt | §2.2.3 (Page 5) | "AI coding assistants tend to favor additive changes" + "erodes trust" | SE 2.0 代码质量问题的论据 | 作者论据 | medium（有引用支撑但无系统衡量） | `dim-orig-se2-limitations`, `leaf-orig-se2-quality` | false | 非系统证据 |
| EV-007 | paper_content.txt | §2.3 (Page 5–6) | "Devin AI [27]...TRAE...SWE-Bench Verified" | 自主软件工程师的现状评估 | 作者评估 | medium（引用具体工具但评估依赖作者判断） | `leaf-orig-se2-autonomous` | false | 工具生态快速变化 |
| EV-008 | paper_content.txt | §3.2 (Page 7–8) | "humans collaborate with AI teammates instead of AI coding assistants" + 六项属性 | Teammate.next 的定义和属性枚举 | 愿景定义 | medium（属性明确但无实现） | `dim-orig-stack`, `leaf-orig-stack-teammate` | false | 纯愿景 |
| EV-009 | paper_content.txt | §3.3 (Page 8) | "the human developer and his AI teammate first align on intents" + "code...hidden from the human by default" | IDE.next 的定义和属性枚举 | 愿景定义 | medium | `dim-orig-stack`, `leaf-orig-stack-ide` | true（Fig. 4 流程一致性） | 纯愿景 |
| EV-010 | paper_content.txt | §3.4 (Page 8–9) | "Compiler.next is organized as a modular stack" + "multi-objective optimization" + "proof-of-concept...on HumanEval-Plus" | Compiler.next 的定义、架构和 PoC 证据 | 愿景定义 + 概念验证 | medium-strong（有 PoC 论文 [28]） | `dim-orig-stack`, `leaf-orig-stack-compiler` | true（PoC 论文单独核验） | PoC 限于 HumanEval-Plus 基准 |
| EV-011 | paper_content.txt | §3.5 (Page 9–11) | "Runtime.next...SLA-aware" + "prototype implementation [114]" | Runtime.next 的定义和原型 | 愿景定义 + 原型 | medium（有 prototype 论文 [114]） | `dim-orig-stack`, `leaf-orig-stack-runtime` | true（prototype 论文单独核验） | 原型限于特定部署场景 |
| EV-012 | paper_content.txt | §3.6 (Page 11–12) | "curriculum engineering" + "InstructLab [51,91]" + "SWEBOK [106]" | FM.next 的定义和 curriculum engineering 配方 | 愿景定义 + 参考实现 | medium（引用 IBM InstructLab 作为参考，但未给出 FM.next 自身实现） | `dim-orig-stack`, `leaf-orig-stack-fm` | false | 参考配方不代表 FM.next 本身的可行性 |
| EV-013 | paper_content.txt | §4.1–§4.6 (Page 13–18) | 每个挑战的 "Description → Affects → Open question → Our vision" 结构 | 五大挑战和八个额外 OQ 的完整条目 | 挑战定义 | strong（结构一致、条目完整） | `dim-orig-challenges` 及其所有子叶 | true（OQ 编号和 Affects 精确性） | 挑战是作者 vision，非系统 gap analysis |
| EV-014 | paper_content.txt | §5 (Page 19–20) | "SE 3.0 vision can only be truly assessed and validated as a whole once prototypes have been developed" | 作者对愿景可验证性的自我限制 | 边界声明 | strong（作者显式承认） | `dim-orig-challenges`, 迁移边界 | false | 自我限制声明 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-001 | 本文为 vision/roadmap 论文，无系统样本库，不进入主统计池 | tree_type / boundary_anchor | `dim-ai-native-se-roadmap-root` | EV-001 至 EV-014（全局负证据：无检索式、无纳排、无数据表） | strong | 用作 boundary_anchor + schema_seed | metadata.json 已确认 `eligible_for_statistical_synthesis: false` |
| CLM-002 | 原生维度树为 roadmap/challenge 分类树，主干 = SE 演化基线 + SE 2.0 局限 + SE 3.0 技术栈 + 挑战路线图 | tree_type | `dim-orig-era-baseline`, `dim-orig-se2-limitations`, `dim-orig-stack`, `dim-orig-challenges` | EV-001–EV-014 | strong（原文显式组织结构） | 作为 schema_seed 为 Paper2 提供 AI-native SE 维度候选 | 树结构反映作者叙事选择，非实证分类 |
| CLM-003 | 五层技术栈的 "from X to Y" 描述模式可迁移为 Paper2 STM 方法学的阶段化描述模板 | migration_boundary | `dim-orig-stack` | EV-008–EV-012 | weak（迁移需改写为 STM 领域术语） | schema_seed | 不可直接套用 SE 领域术语 |
| CLM-004 | 挑战→技术栈的 `affects` 关系边可作为 Paper2 中 LLM-STM 问题→方法组件的映射模板 | migration_boundary | `rel-challenge-affects` | EV-013 | weak | schema_seed | 需要 STM 领域的对应映射 |
| CLM-005 | CH1–CH6 为候选启发，不得直接充当 Paper2 的 final research finding | candidate_finding | CH1–CH6 | EV-003, EV-008–EV-013 | weak | candidate_heuristic | 所有候选发现需跨论文验证和研究者裁决 |
| CLM-006 | Compiler.next 是五层技术栈中唯一有已发表 PoC 论文 [28] 的组件；Runtime.next 有 prototype [114] | evidence_boundary | `leaf-orig-stack-compiler`, `leaf-orig-stack-runtime` | EV-010, EV-011 | medium | 用于评估技术栈各层的成熟度差异 | PoC 均来自作者团队，独立复现未确认 |
| CLM-007 | 现有 review.md 需将六叶通用接口从维度树主位降级为投影表，并将原文 19 条原生叶子提升为主事实源 | audit_repair | 返修建议 §7 #1–#4 | 本报告 §3–§5 与现有 review.md 对照 | strong | 用于驱动 review.md 的下一轮返修 | 返修后仍需 A2a 精核页码/表图/附录 |

---

## 9. 技能使用与自我审查记录

### 9.1 读取的技能文件和采用的原则

| 技能文件 | 采用的核心原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | Claim-evidence-engineering 原则——每个主要声明必须有证据支撑，缺失证据时降级声明或标记缺口；"Never invent citations" |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 五个通用审查维度（Originality/Quality/Clarity/Significance/Reproducibility）；"Constructive Specificity Standard"——审查意见必须具体到作者可行动的程度 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 五维度评分框架（Contribution/Writing/Experimental/Evaluation/Method/Responsibility）；Rejection-risk audit；Claim audit 中对 "first/general/unified/robust" 等强词的特殊审查 |
| `research-planning/SKILL.md` | "Flag ambiguities explicitly rather than making assumptions"——不明确的字段取值空间标注为待核验 |
| `research-planning/references/planning-prompts.md` | Paper2Code 的四阶段规划方法——阶段化追踪（Overall → Architecture → Logic → Config），启示审计中也应保持阶段化证据链路 |
| `research-planning/references/output-schemas.md` | 结构化的 JSON 输出 schema——启示维度树应有稳定的节点标识和父子关系 |
| `autoresearch/SKILL.md` | "Completion is artifact-gated"——审计完成必须有可核验的 artifact（本报告）；"The loop does not stop because the model says done"——审计不能因为"看起来够了"就停止，需证据饱和 |

### 9.2 本输出最高风险的 3 点

| # | 风险 | 复核方式 |
|---|---|---|
| 1 | **19 条原生叶子的取值空间尚未经 PDF 视觉核验**。本报告的取值空间来自 `paper_content.txt` 的文本识别，Fig. 3（技术栈图）和 Fig. 4（IDE 流程图）中的细微标注可能未被文本提取捕获。若 Fig. 3 中存在六叶通用接口未覆盖的隐式层间属性，则需补充叶子。 | 主线程合并时：打开 `paper.pdf`，逐图核对 Fig. 3 中 SE 2.0 对照列和 SE 3.0 技术栈列的全部标注文字 |
| 2 | **CH1–CH6 候选启发可能过度类比**。将 Compiler.next 的 multi-objective optimization 类比为 STM 验证剖面的多目标组织是合理的，但若 Paper2 的验证剖面已经有自己成熟的定义框架，强行类比可能造成概念混淆。 | 与 Paper2 的当前研究设计交叉核对，确认是否存在概念冲突 |
| 3 | **A.2 证据账本的 14 条记录中 8 条标记为 `medium` 强度**——本报告的"medium"判断来自"原文显式定义但未经验证或非系统证据"，这个判定阈值需要与 codex/claude 两路审计对齐，避免三路之间的强度校准偏差。 | 将本报告的 EV-001 至 EV-014 与 codex/claude 的对应证据记录进行跨表格对比 |

### 9.3 本任务状态

- **是否出现 blocked**：否
- **是否出现 timeout**：否
- **是否出现文件缺失**：否——所有必需文件均已成功读取
- **是否出现 PDF 无法打开**：否——PyPDF2 成功读取 25 页
- **是否出现 paper_content.txt 被截断**：否——逐段读取覆盖全文 1146 行

---

**审计完成时间**：2026-06-30
**审计 agent**：deepseek（codex-deepseek exec）
**审计版本**：A1-DT v2