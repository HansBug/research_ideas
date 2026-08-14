# ai-native-se-roadmap · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是
  - 主 SKILL：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - `references/paper-story.md`
  - `references/reviewer-guidelines.md`
  - `references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是
  - 主 SKILL：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - `references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是
  - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是
  - 全文 1146 行，覆盖 Abstract、Introduction、§2 SE 2.0 Limitations（§2.1--§2.3）、§3 SE 3.0 Vision（§3.1--§3.6 technology stack）、§4 Challenges（§4.1--§4.6）、§5 Conclusion 及 References。未跳读，逐段核验。
- **是否核对 `paper.pdf`**：否
  - 未人工打开 PDF 核对 Figure 1--7、Table 1 及 challenge roadmap 精确页码 / 表图编号。当前审计完全基于 `paper_content.txt` 全文文本，对图表细节（Figure 3 technology stack 精确节点、Figure 4 intent-centric dev loop、Figure 6 FM code landscape、图/表编号）的引用均为文本提取级，需后续 A2a 视觉核对。
- **额外读取的文库级规则**：
  - `survey_of_surveys/README.md`：确认本文定位为 boundary_anchor、eligible_for_statistical_synthesis=false
  - `survey_of_surveys/GUIDE.md`：证据等级、三池规则、维度树复原纪律
  - `survey_of_surveys/SUMMARY.md`：19 篇现状、A1-M0--M6 元维度覆盖矩阵
  - `survey_of_surveys/patterns/pattern-field-schema.md`：字段合同、证据链合同、A1-DT 临时降级规则
  - `survey_of_surveys/../story/paper_story.md`：Paper2 主线框架、贡献分层、禁止主张清单

## 2. 原文真实结构复原

### 2.1 论文身份

Hassan et al. "Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap." ACM TOSEM, 2026. DOI: 10.1145/3807901。

**论文类型**：vision / roadmap / proposal。作者自身在 Abstract 中将其定位为 "a vision and a challenge roadmap" 和 "lays the foundation for future discussions"。它不是 SLR、SMS、tertiary study、systematic survey 或 guideline。metadata.json 已正确记录 `eligible_for_statistical_synthesis=false`，排除理由为 "vision/roadmap；没有系统检索、纳排、质量评价或数据综合"。

### 2.2 原文没有的东西（关键否定清单）

本文**不存在**以下 SLR/SMS 标准组件。以下每一条均经全文逐段核验确认：

- **RQ / 研究问题**：论文没有以 "RQ1/RQ2/..." 形式组织的正式研究问题。§2.2 有一个小节标题 "What are the limitations of Software Engineering 2.0?"，这是 rhetorical question（修辞性问题），不是协议驱动的研究问题。
- **系统检索协议**：论文提到 "surveys of academic and gray literature"（Page 2），但未给出检索式、数据库、检索日期、命中数或筛选流程。该提及是背景信息来源声明，不是系统综述方法。
- **纳排流程 / PRISMA 图**：无。论文没有筛选阶段、排除理由、纳入计数。
- **数据抽取表（extraction form）**：无。论文没有定义抽取字段、抽取协议或抽取结果表。
- **编码方案（coding scheme）**：无。论文没有编码手册、inter-rater agreement 或编码结果。
- **质量评价量表（quality rubric）**：无。论文没有质量评分、质量 checklist 或质量加权。
- **统计综合 / meta-analysis**：无。论文没有任何频次统计、分布分析、交叉表或效应量。
- **完成型 research finding**：无。论文的 §4 Challenges 以 "Description / Affects / Open question / Our vision" 组织，是 vision statement 和 open question，不是基于证据综合的 completed finding。

### 2.3 原文真实结构

#### 2.3.1 宏观章节

| 章节 | 页码范围（paper_content.txt） | 内容 |
|---|---|---|
| Abstract | Page 1 | SE 2.0 局限 → SE 3.0 愿景 → 4 层技术栈 → challenge roadmap |
| §1 Introduction | Page 1--3 | SE 1.0/2.0 定义、SE 2.0 局限概述、SE 3.0 提案、论文结构 |
| §2 SE 2.0 Limitations | Page 3--6 | §2.1 Background、§2.2.1 认知过载、§2.2.2 无效训练与理解不足、§2.2.3 代码质量与 additive bias、§2.3 Autonomous SE |
| §3 SE 3.0 Vision | Page 6--13 | §3.1 Principles（人机互补、对话式意图对齐、AI-native 代码合成）→ §3.2 Teammate.next → §3.3 IDE.next → §3.4 Compiler.next → §3.5 Runtime.next → §3.6 Cross-cutting concerns（Security & Privacy、Evaluation & Benchmarking、Knowledge Management + Curriculum Engineering） |
| §4 Challenges | Page 13--19 | §4.1 Speeding up human-AI alignment → §4.2 Improving efficiency of code synthesis → §4.3 Improving runtime performance → §4.4 Improving FM's understanding of code and SE → §4.5 Eliminating prompt engineering → §4.6 Other open questions（OQ7--OQ14，共 8 个） |
| §5 Conclusion | Page 19 | 总结 SE 2.0→SE 3.0 转变 |
| References | Page 19--25 | 117 条参考文献 |

#### 2.3.2 原文核心 schema：技术栈 + 挑战路线图

论文的核心组织 schema 是两层正交维度：

**第一层：技术栈分层（§3，Figure 3）**

```
SE 3.0 Technology Stack
├── Teammate.next（AI teammate：ToM、个性化、持续学习）
├── IDE.next（意图中心对话式开发环境）
├── Compiler.next（多目标代码合成 + prompt orchestration + model routing）
├── Runtime.next（SLA-aware execution + edge-computing）
└── Cross-cutting
    ├── Security & Privacy
    ├── Evaluation & Benchmarking
    └── Knowledge Management（含 Curriculum Engineering）
```

**第二层：挑战路线图（§4）**

每个 challenge 的 schema：
- `Description`：挑战本质
- `Affects`：影响哪些技术栈层
- `Open question #N`：一个或多个开放问题
- `Our vision`：作者愿景 / 解决方向

5 个核心 challenge（§4.1--§4.5）：
1. **Speeding up human-AI alignment**（Affects: IDE.next, Teammate.next；OQ1）
2. **Improving efficiency of code synthesis**（Affects: Compiler.next, Teammate.next；OQ2）
3. **Improving runtime performance**（Affects: Runtime.next；OQ3, OQ4）
4. **Improving FM's understanding of code and SE**（Affects: Compiler.next, Teammate.next；OQ5）
5. **Eliminating prompt engineering**（Affects: entire stack；OQ6）

+ 8 个 additional open questions（OQ7--OQ14，§4.6）

#### 2.3.3 原文其他可抽取语义对象

| 对象 | 原文位置 | 可抽取性 |
|---|---|---|
| SE 1.0 / SE 2.0 / SE 3.0 时期划分 | §1, Figure 1 | 可作分类标签 |
| 3 条 SE 3.0 愿景原则 | §3.1 | 可作取值维度 |
| 4 层技术栈 + cross-cutting | §3.2--§3.6, Figure 3 | 核心 schema 轴 |
| 5 个核心 challenge | §4.1--§4.5 | 可作 challenge 条目表 |
| 每个 challenge 的 Affects 映射 | §4 各段 "Affects." | 关系边（challenge → stack layer） |
| 8 个额外 open questions | §4.6 | 可作 open question 条目表 |
| SE 2.0 局限分类（3 类 + autonomous SE） | §2.2--§2.3 | 可作 limitation taxonomy |
| Curriculum Engineering 的 taxonomy 方法 | §3.6, Page 12--13 | 方法学启发（非本文主 schema） |
| 引用文献 117 条 | References | 可作引文网络（非本文系统综述语料） |

#### 2.3.4 原文如何形成 conclusion

本文的 conclusion 形成方式不是 "从字段/统计观察形成 finding"，而是 "从作者经验、社区讨论、文献调研和工业互动中提炼 vision + open question"。原文明确说明其来源为：

1. surveys of academic and gray literature（非系统综述）
2. community events and workshops
3. customer and internal team discussions
4. 作者自身 FMware / SE 3.0 stack 研发经验
5. OPEA alliance 40+ 工业伙伴互动

（以上见 paper_content.txt Page 2 第 4 段）

## 3. 当前 `review.md` 维度树审计

### 3.1 审计总论

当前 `review.md` 的维度树存在一个结构性错位：**主树以 6 个通用 A1-M1--M6 接口叶子为骨架，但对这篇 vision/roadmap 论文而言，其中多个叶子对应的 SLR 组件根本不存在于原文**。更严重的是，这 6 个叶子都被标注为 "来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构"，而原文既无 RQ，也无纳排、统计观察或质量评价——这个来源声明对 vision/roadmap 论文构成误导。

review.md 确实在 `metadata.json` 中正确标记了 `eligible_for_statistical_synthesis=false`，也正确记录了所有结论强度为 `weak`、允许用途为 `boundary_anchor` 或 `schema_seed`。但这些安全围栏无法消除主树结构本身把通用 SLR 接口冒充为"原文 schema"的问题。

### 3.2 逐项检查

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确 | `[dim-ai-native-se-roadmap-root]` 定义为 "SE 3.0 愿景 / 技术栈 / 挑战路线图"，与原文定位大体一致；但根节点下直接接了 6 个 A1-M 通用维度而非原文自身的技术栈-挑战结构，导致根节点与主干分支脱节。 | I |
| 主干分支是否覆盖原文 schema | 否——主干分支是通用 A1-M 接口，不是原文 schema | 主树 6 个 leaf（scope, corpus, taxonomy, method, evidence, finding）映射 A1-M1--M6。本文没有 corpus/纳排（M1）、没有统计观察（M6）、没有 quality rubric（M4）。review.md 把通用脚手架维度写成主树，而原文的真实 schema（4 层技术栈 + 5 个 challenge + 8 个 OQ + 3 条原则）被放在 §2.3.5 "原文模式候选叶子映射" 的 5 个 `[leaf-ai-native-se-roadmap-orig-*]` 中，作为独立于主树的辅助材料。主树与原文 schema 是平行关系而非投影关系。 | C |
| 叶子维度是否足够具体 | 主树叶子太泛；候选叶子尚可但未集成 | 主树 6 个叶子对本文全部是 "来自本文的 RQ/方法/分类/评价/讨论结构"——这个声明对 corpus/finding 两叶尤为虚假。5 个候选叶子（vision-object, stack-layer, challenge, roadmap-action, boundary-risk）更贴近原文，但无取值空间定义、无证据锚点（仅 `EV-ai-native-se-roadmap-002/003` 两个泛标识覆盖全部 5 个）、无统计用途或缺失语义。 | C |
| 取值空间是否可执行 | 不可执行 | 主树 6 个叶子在 A.2 证据账本中被标注为 `not_verified`（EV-002, EV-003），无任何具体取值空间。候选 5 个叶子的 "取值空间" 写成 "原文词语 + 待 A2a 闭合"，等于未定义。对本文，不存在 "corpus" 的取值空间，也不存在 "statistical finding" 的取值空间——这些叶子不应存在于本文的主树中。 | I |
| 关系边是否缺失 | 是——原文最核心的关系边未被捕获 | 原文的关键关系是 challenge → stack layer 的 "Affects" 映射（§4 每段），以及 stack layer → cross-cutting concern 的从属关系。review.md 的 A.2 证据账本中没有任何关系边记录。虽然 pattern-field-schema §8.3 规定了关系边合同，但在本文的 review 中没有实现。 | I |
| 统计用途 / 分母是否正确 | 主树定义了不可用的统计叶子 | A.1-M6 "统计分析与候选发现" 被映射为 `[leaf-ai-native-se-roadmap-finding]`，但对本文，不存在可统计数据。review.md 虽然把所有 leaf 的 A.3 结论强度写为 `weak`，但保留 `finding` 叶子和 "统计观察与候选发现" 标签，让不读结论强度表的读者可能误以为本文有可抽取的统计结果。 | I |
| 候选 finding 路径是否完整 | 候选 finding 路径是空的 | review.md A.3 中 `[clm-ai-native-se-roadmap-finding-boundary]`（C09）只声明 "本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决"——这是一个方法论边界声明，不是从本文实际内容中提取的候选 finding。5 个 candidate finding 的声明（C10--C11 等）均未填充具体内容，标注为 `--`。说明在当前 review.md 中，没有任何从本文原文中提取的候选发现信号。 | M |
| A.1--A.4 证据链是否足够 | 证据链形式合规但内容薄弱 | A.1 来源清单正确；A.2 只有 4 条证据（EV-001 来自 bibtex/metadata，EV-002/003 标注全文但 `not_verified`，EV-004 标注全文但仅限 "原文作者讨论"）；EV-002/003 覆盖了全部主树 6 个 leaf + 5 个候选 leaf，这种一对多映射意味着单条 `not_verified` 证据同时支撑 11 个维度节点，无法区分哪个节点有实际原文证据、哪个没有。A.3 结论全部 `weak`、`boundary_anchor`。A.4 标注 `needs_manual_check`。形式合规但证据质量不足。 | I |
| 是否存在可能误导 A2a 的强主张 | 是——"来自本文的 RQ" 声明构成对 A2a 的误导 | review.md 对 6 个主树叶子的一致性声明为 "来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构"。本文没有 RQ，没有 systematic 方法，没有 quality rubric，没有 statistical finding。任何后续 A2a agent 或人类研究者阅读这 6 个 leaf 的声明时，可能被误导认为本文具备这些 SLR 组件并试图定位原文对应内容，导致无效搜索或错误证据归因。 | C |

## 4. 建议维度树骨架

以下维度树直接反映本文的 vision/roadmap 结构，不再强行套用 A1-M1--M6 的 SLR 通用接口。在后续 A2a/A2b 跨论文汇总时，这些叶子可以作为该篇对 A1-M 元维度的具体贡献回链。

```
[dim-ai-native-se-roadmap-root] SE 3.0 愿景与技术栈路线图
│
├── [dim-ai-native-se-roadmap-vision-era] 时期划分
│   ├── [leaf-ai-native-se-roadmap-era-label] 时期标签
│   │   ├── 取值空间: {SE 1.0, SE 2.0, SE 3.0}
│   │   ├── 证据来源: §1, Figure 1 (Page 1--3)
│   │   ├── 缺失语义: --
│   │   └── 统计用途: 不统计（vision 陈述）
│   │
│   ├── [leaf-ai-native-se-roadmap-era-def] 时期定义特征
│   │   ├── 取值空间: {code-centric, AI-assisted/task-driven, intent-centric/conversation-oriented}
│   │   ├── 证据来源: §1 (Page 1--3)
│   │   ├── 缺失语义: --
│   │   └── 统计用途: 不统计
│   │
│   └── [leaf-ai-native-se-roadmap-era-limitations] SE 2.0 局限分类
│       ├── 取值空间: {人类认知过载, 模型训练低效/理解不足, 代码质量与additive bias, autonomous SE 边界}
│       ├── 证据来源: §2.2.1--§2.3 (Page 3--6)
│       ├── 缺失语义: 作者声明此列表 "not meant to be extensive"
│       └── 统计用途: 不统计（author observation）
│
├── [dim-ai-native-se-roadmap-vision-principles] 愿景原则
│   ├── [leaf-ai-native-se-roadmap-principle] 原则条目
│   │   ├── 取值空间: {人机互补, 对话式意图对齐, AI-native 代码合成}
│   │   ├── 证据来源: §3.1 (Page 6--7)
│   │   ├── 缺失语义: --
│   │   └── 统计用途: 不统计
│   │
│   └── [leaf-ai-native-se-roadmap-principle-description] 原则详述
│       ├── 取值空间: 自由文本
│       ├── 证据来源: §3.1 各段
│       ├── 缺失语义: --
│       └── 统计用途: 不统计
│
├── [dim-ai-native-se-roadmap-stack] 技术栈分层
│   ├── [leaf-ai-native-se-roadmap-stack-layer] 技术栈层
│   │   ├── 取值空间: {Teammate.next, IDE.next, Compiler.next, Runtime.next}
│   │   ├── 证据来源: §3.2--§3.5, Figure 3 (Page 7--11)
│   │   ├── 缺失语义: --
│   │   └── 统计用途: 不统计（proposal schema）
│   │
│   ├── [leaf-ai-native-se-roadmap-stack-cross-cutting] 跨层关注
│   │   ├── 取值空间: {Security & Privacy, Evaluation & Benchmarking, Knowledge Management / Curriculum Engineering}
│   │   ├── 证据来源: §3.6 (Page 11--13)
│   │   ├── 缺失语义: --
│   │   └── 统计用途: 不统计
│   │
│   └── [leaf-ai-native-se-roadmap-stack-component-description] 层内组件描述
│       ├── 取值空间: 自由文本（每层 §3.x 详述）
│       ├── 证据来源: §3.2--§3.6
│       ├── 缺失语义: --
│       └── 统计用途: 不统计
│
├── [dim-ai-native-se-roadmap-challenge] 挑战路线图
│   ├── [leaf-ai-native-se-roadmap-challenge-id] 挑战标识
│   │   ├── 取值空间: {C1: Speeding up human-AI alignment, C2: Improving efficiency of code synthesis, C3: Improving runtime performance, C4: Improving FM's understanding of code and SE, C5: Eliminating prompt engineering}
│   │   ├── 证据来源: §4.1--§4.5 (Page 13--18)
│   │   ├── 缺失语义: 作者声明 "not meant to be extensive"
│   │   └── 统计用途: 不统计
│   │
│   ├── [leaf-ai-native-se-roadmap-challenge-description] 挑战描述
│   │   ├── 取值空间: 自由文本（§4.x "Description." 段）
│   │   ├── 证据来源: §4.1--§4.5 "Description." 段
│   │   ├── 缺失语义: --
│   │   └── 统计用途: 不统计
│   │
│   ├── [leaf-ai-native-se-roadmap-challenge-affects] 挑战影响的技术栈层（关系边）
│   │   ├── 取值空间: {Teammate.next, IDE.next, Compiler.next, Runtime.next, entire stack} 的子集
│   │   ├── 关系类型: challenge → stack layer 的 "Affects" 映射
│   │   ├── 证据来源: §4.1--§4.5 "Affects." 段
│   │   ├── 缺失语义: --
│   │   └── 统计用途: 不统计
│   │
│   ├── [leaf-ai-native-se-roadmap-challenge-open-question] 开放问题
│   │   ├── 取值空间: {OQ1, OQ2, OQ3, OQ4, OQ5, OQ6} 核心 OQ + {OQ7..OQ14} §4.6 额外 OQ
│   │   ├── 证据来源: §4.1--§4.6 "Open question #N" 和 "Other open questions"
│   │   ├── 缺失语义: OQ7--OQ14 作者声明 "not yet developed a thorough vision"
│   │   └── 统计用途: 不统计
│   │
│   └── [leaf-ai-native-se-roadmap-challenge-vision] 挑战愿景
│       ├── 取值空间: 自由文本（§4.x "Our vision." 段）
│       ├── 证据来源: §4.1--§4.5 "Our vision." 段
│       ├── 缺失语义: §4.6 OQ7--OQ14 无对应 vision
│       └── 统计用途: 不统计
│
├── [dim-ai-native-se-roadmap-source] 愿景来源声明
│   ├── [leaf-ai-native-se-roadmap-source-type] 来源类型
│   │   ├── 取值空间: {academic & gray literature surveys, community events & workshops, customer & internal discussions, 作者 FMware/SE3.0 R&D 经验, OPEA alliance 工业伙伴互动}
│   │   ├── 证据来源: Page 2 第 4 段
│   │   ├── 缺失语义: 各项来源的具体范围/时间/参与方未报告
│   │   └── 统计用途: 不统计
│   │
│   └── [leaf-ai-native-se-roadmap-source-systematicity] 来源系统性
│       ├── 取值空间: {non_systematic（无检索式/数据库/纳排/质量评价/数据综合）}
│       ├── 证据来源: 全文（无任何 SLR 方法组件）
│       ├── 缺失语义: --
│       └── 统计用途: 不统计
│
└── [dim-ai-native-se-roadmap-positioning] 与本库关系
    ├── [leaf-ai-native-se-roadmap-pool-eligibility] 统计池资格
    │   ├── 候选取值: false（vision/roadmap, non-systematic）
    │   ├── 排除理由: 无系统检索、纳排、质量评价或数据综合
    │   └── 证据来源: 全文 + metadata.json
    │
    ├── [leaf-ai-native-se-roadmap-evidence-role] 证据角色
    │   ├── 候选取值: roadmap_boundary_anchor | schema_seed
    │   ├── 可用用途: 提供 technology stack 分层、challenge 描述-影响-愿景 schema、SE 时代划分标签和 open question 模式作为 Paper2 维度树设计的边界锚点和候选节点
    │   └── 禁止用途: 进入主统计池；作为 completed SLR finding 证据；用本文 challenge schema 替代 SLR extraction form
    │
    └── [leaf-ai-native-se-roadmap-external-generalizability] 外推限制
        ├── 候选取值: 单篇 vision/roadmap 论文，来自 SE 领域权威作者组但未经跨论文验证
        └── 禁止: 声称本文 schema 代表 AI-native SE 社区共识或已完成 SLR 综合

```

**与当前 review.md 的关键差异**：

1. **主树不再是通用 A1-M1--M6 接口**，而是原文真实的 technology stack + challenge roadmap + vision principles + era classification 结构。
2. **移除了不存在的叶子**：corpus、statistical finding、quality rubric 不再作为本文主树叶。
3. **新增了原文实际存在但当前缺失的维度**：
   - 时期划分（SE 1.0/2.0/3.0）
   - vision principles（3 条）
   - challenge → stack layer 的 "Affects" 关系边
   - open question 条目（OQ1--OQ14）
   - source type 声明（5 类来源）
   - source systematicity 否定声明
   - 外推限制
4. **所有叶子明确标注 "不统计"**，与本文 vision/roadmap 性质一致。
5. **证据来源定位到具体段落**（而非泛化的 EV-002/EV-003）。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 移除对不存在组件的来源声明 | `review.md` §2.3.5 主维度树中 6 个 leaf 的 "原文来源" 列 | 将所有 6 个 leaf 的 "来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构" 替换为准确声明：对 scope/taxonomy/method 可保留 "来自本文 §2/§3 的组织结构，但非 SLR 协议驱动"；对 corpus/finding 必须写明 "本文无系统语料/纳排/统计发现，此叶为脚手架占位，非原文提取"；对 evidence 写明 "本文无 quality rubric 或证据表"。 | paper_content.txt 全文 | C |
| 重组主维度树以反映原文真实 schema | `review.md` §2.3.5 | 将当前 6 个 A1-M 通用叶子从主树降级为 "脚手架对照表"（见下文建议），将 5 个候选叶子升级并扩充为本文真正的主维度树（按 §4 建议骨架）。 | paper_content.txt §1--§4 全文 | C |
| 补充 challenge → stack layer 关系边 | `review.md` §2.3.5 + A.2 | 记录 5 个 challenge 各自的 "Affects" 映射：C1→{IDE.next, Teammate.next}、C2→{Compiler.next, Teammate.next}、C3→{Runtime.next}、C4→{Compiler.next, Teammate.next}、C5→{entire stack}。这些是原文最显式的关系边，当前完全缺失。 | paper_content.txt §4.1--§4.5 "Affects." 段 | I |
| 补充 open question 条目表 | `review.md` §2.3.5 | 新增叶子 `[leaf-ai-native-se-roadmap-challenge-open-question]`，列出 OQ1--OQ14，标注核心/额外状态。当前 review.md 未记录任何 open question 条目，遗漏了原文 §4 近一半内容。 | paper_content.txt §4.1--§4.6 | I |
| 补充 vision principles | `review.md` §2.3.5 | 新增 3 条 SE 3.0 原则（人机互补、对话式意图对齐、AI-native 代码合成）作为独立维度。当前 review.md 在 §2.3.3 中提及但未纳入维度树。 | paper_content.txt §3.1 (Page 6--7) | M |
| 补充 SE 1.0/2.0/3.0 时期划分 | `review.md` §2.3.5 | 新增时期维度，取值 {SE 1.0, SE 2.0, SE 3.0} + 定义特征。本文的核心叙事正是以此时期划分为骨架。 | paper_content.txt §1, Figure 1 | M |
| 补充来源系统性否定声明 | `review.md` §2.3.5 | 新增叶子记录本文来源为非系统性（5 类来源，无检索式/数据库/纳排/质量评价）。当前 A.2 只有 EV-001 记录来源，但未结构化。这很重要，因为 §2.1 已正确指出 "不是系统综述协议"，但维度树中没有对应叶子。 | paper_content.txt Page 2 第 4 段 | I |
| 拆分 A.2 证据条目，避免一对多映射 | `review.md` A.2 | 当前 EV-002/EV-003 一条证据支撑 11 个维度节点。应至少按维度域（vision、stack、challenge）拆分为独立证据条目，每条给出具体章节定位和 short quote。 | pattern-field-schema.md §8.4 证据链合同 | I |
| 修正 "统计观察与候选发现" 标签 | `review.md` §2.3.5 `[leaf-ai-native-se-roadmap-finding]` | 将该叶标签从 "统计观察与候选发现" 改为 "愿景声明与开放问题（非统计综合）"，并在取值空间中明确写入 "本文不含统计结果"。当前标签暗示本文有统计发现，构成误导。 | paper_content.txt 全文（无统计结果） | C |
| 补充外推限制叶子 | `review.md` §2.3.5 | 新增叶子记录本文外推限制：单篇 vision/roadmap、非系统证据、未经验证、作者组声明 "not meant to be extensive"。当前 A.3 C08 提到迁移边界但未纳入维度树。 | paper_content.txt §4 首段 + pattern-field-schema §8.2 | M |

## 6. C/I/M 结论

### 6.1 C 级问题（破坏 Paper2 学术目标 / 证据链可靠性）

| # | 问题 | 影响 |
|---|---|---|
| C1 | **主维度树使用通用 A1-M1--M6 接口冒充原文 schema**。6 个主树叶子被标注为 "来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构"，但本文既无 RQ，也无 corpus/纳排，也无 statistical finding。这会在后续 A2a 跨论文汇总时造成两个致命后果：(a) 后续 agent 可能误以为本文具有这些 SLR 组件，试图定位原文对应内容而导致无效搜索和错误证据归因；(b) 当 A2a 统计 "多少篇论文包含 corpus 字段" 时，本文会被误计为 "有 corpus"，扭曲统计结果。 |
| C2 | **corpus/纳排叶子存在于 vision/roadmap 论文的主树中**。即使标注 `weak` 强度，叶子本身的存在已经暗示 "本文在某种意义上包含这些信息"。对 vision/roadmap 论文，应该明确 "不适用" 而非保留叶位写 "weak"。当前做法违反了 pattern-field-schema §8.2 "不得把 roadmap/vision/proposal 写成完成型统计 finding" 和 §8.6 "不适用时应直接说明不适用" 的纪律。 |
| C3 | **"统计观察与候选发现" 标签对 vision 论文构成类别错误**。该标签暗示论文有统计结果，与本文性质根本矛盾。即使后续 A2a 理解 `eligible_for_statistical_synthesis=false`，该标签在视觉扫描和跨论文对比中会系统性地误导读者。 |

### 6.2 I 级问题（实质影响维度树可用性 / 原文 schema 复原 / 证据可审计性）

| # | 问题 | 影响 |
|---|---|---|
| I1 | **原文最核心的关系边（challenge → stack layer 的 Affects 映射）完全缺失**。这是本文 schema 区别于其他 roadmap 论文的关键特征——每个 challenge 精确标注影响哪些技术栈层——当前 review 未捕获。A2a 将无法从本文提取 challenge-layer 关联模式。 |
| I2 | **OQ7--OQ14 共 8 个 open question 未记录**。原文 §4.6 占约一页篇幅，当前 review 完全遗漏。这对后续提取 "open question 模式" 和 "未解决挑战声明方式" 构成信息损失。 |
| I3 | **来源系统性未结构化记录**。review.md §2.1 在自然语言中正确指出 "不是系统综述协议"，但维度树中没有对应叶子。后续 A2a 的机器可读处理会丢失这一关键分类信号。 |
| I4 | **A.2 证据一对多映射**。EV-002/EV-003 单条 `not_verified` 证据支撑全部 11 个节点，违反了 pattern-field-schema §8.4 "每条证据至少应给出具体章节定位和 short quote" 的合同。这使得 A.3→A.2→A.1 回链在操作上不可审计（无法判断哪个维度有独立证据、哪个完全是脚手架投影）。 |

### 6.3 M 级问题（不阻塞但建议修复）

| # | 问题 | 建议 |
|---|---|---|
| M1 | vision principles 未纳入维度树 | 新增叶子；当前只在 §2.3.3 自然语言中提及。 |
| M2 | SE 时代划分未纳入维度树 | SE 1.0/2.0/3.0 是本文的核心叙事骨架，应作为维度。 |
| M3 | challenge 的结构化程度被低估 | 本文不是只有 "challenge 条目"，而是有 {Description, Affects, Open Question, Our Vision} 四元组。当前 review 只把 challenge 作为一个叶子，丢失了四元组结构。 |
| M4 | 缺少外推限制叶 | 虽然 A.3 C08 记录了迁移边界，但维度树没有对应叶子记录 "此 leaf 的外推限制是什么"。 |

### 6.4 最终建议

**NEEDS FIX**

当前 `review.md` 在形式层面是合规的（有维度树、有 A.1--A.4、有证据链、有 safety labels），但在内容层面存在结构性错位：把一篇 vision/roadmap 论文强行套进 6 个通用 SLR 接口维度中，导致主树不代表原文 schema、corpus/finding 叶子对本文无意义、"来自本文的 RQ" 声明虚假、以及原文最丰富的 challenge → stack 关系边和 open question 条目完全遗漏。

建议的修复路径：

1. **主树替换**：用 §4 建议的维度树骨架替换当前 6 个 A1-M 主树叶。将 A1-M 通用维度作为"脚手架对照表"（映射表：本文哪些维度贡献了哪些 A1-M 元维度的启发），放在维度树之外，不混淆主树。
2. **移除不适用叶子**：corpus、statistical finding、quality rubric 不在本文主树中出现。在脚手架对照表中标注 "不适用: vision/roadmap"。
3. **补充关系边**：challenge → stack layer 的 Affects 映射。
4. **补充遗漏对象**：OQ1--OQ14、vision principles（3 条）、SE 时代划分、source type & systematicity。
5. **拆分 A.2 证据**：按 vision/stack/challenge/source 域拆分独立证据条目，满足 pattern-field-schema §8.4 合同。
6. **同步更新 SUMMARY**：在 SUMMARY 的 A1-M0--M6 覆盖矩阵中，对本文的 M1 (corpus)、M4 (quality/evidence)、M5 (statistical) 列标注 "不适用 (vision/roadmap)"，而非 "来自本文结构"。

---

**审计完成时间**：2026-06-29
**审计工具与入口**：Codex CLI deepseek 全文审计，未使用子 agent。
**审计输入清单**：
- 技能文件：7 个（ai-research-writing-skill SKILL + 3 refs, research-planning SKILL + 1 ref, autoresearch SKILL）
- 文库规则与 story：5 个（README, GUIDE, SUMMARY, pattern-field-schema, paper_story）
- 论文单篇文件：4 个（bibtex, metadata, paper_content.txt 全文 1146 行, review.md）
- 补充检查：grep of challenge/stack/roadmap keywords × 2
**未使用的能力**：paper.pdf 视觉核对、子 agent 并行、web search
