PDF confirmed present (1.4MB). Now I have all evidence needed. Let me compile the complete A1-DT v2 audit report.

---

# A1-DT v2 单篇全文审计报告：`requirements-quality-theory-roadmap`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `requirements-quality-theory-roadmap` |
| agent | `deepseek`（本 exec 进程独立完成） |
| 是否已读 `paper_content.txt` | 是。全文 1187 行，14 页（PDF 页码 507–520），已分段通读 Sections 1–6 及 References。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。均完整读取。 |
| 是否打开或核对 `paper.pdf` | 是，已确认 PDF 存在（1.4MB）。未逐页核验 Fig. 2 / Fig. 4 / Fig. 5 / Table 1 的图形像素细节；text 提取内容与 prose 描述一致。需要在 A2a 精核阶段做版面级核对。 |
| 原文类型 | **research commentary / VIEW POINT**（期刊明确标注）。非 SLR、非 SMS、非 tertiary、非 MLR。属于「theory + evaluation + roadmap」三合一。 |
| 被编码样本单位 | **57 篇 primary studies**（需求质量因子文献），来自作者此前系统研究 [7] 的便利样本（convenience sample）。 |
| 样本数量 / 分母 | 57（编码母体）/ 无系统检索纳排流程（便利样本）。辅助编码一致性检验使用其中 6 篇（≈10%）。 |
| 原生树类型 | **单树（codebook 树）**，以 RQT 概念模型为框架，对每篇 primary study 做 categorical coding。不是维度森林（无多棵并列分类树）。 |
| 主统计池资格 | **局部可统计**。57 篇编码统计可用于描述性观察（descriptive statistics），不能进入 SLR/SMS 的跨论文定量合成池。理由：(a) 样本为便利样本，非系统检索纳排；(b) 编码方案 ad hoc 迭代生成，IRR 中等（S-Score 76.8%）；(c) 论文本身是 research commentary，其统计服务于 gap identification 和 roadmap 论证，不是独立的 SLR/SMS 结果。 |
| 总体判定 | **pass（需 A2a 精核）**。原生维度树已从原文 codebook 复原；现有 `review.md` 需要返修以区分原生 codebook 树与跨论文六叶投影。 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取文件清单

| 文件 | 读取状态 | 说明 |
|---|---|---|
| `bibtex.bib` | ✅ 完整 | Frattini et al. 2023, Requirements Engineering 28(4):507–520 |
| `metadata.json` | ✅ 完整 | 含 eligibility、evidence_role、statistical_pool 判定 |
| `paper_content.txt` | ✅ 分四段通读 | 1187 行全覆盖：Sect. 1–6 + References |
| `review.md` | ✅ 完整 | 含 A.1–A.4、evidence ledger、conclusion map |
| `paper.pdf` | ✅ 确认存在 | 1.4MB，未逐页 pixel-level 核对 Fig. 2/4/5/Table 1 |

### 1.2 仍需 PDF 视觉核验的内容

以下内容在 `paper_content.txt` 中仅以 prose 引用或文字描述出现，原文精确布局、取值、颜色编码、箭头方向、表头行数等需要打开 `paper.pdf` 做版面级核对：

- **Fig. 2**：RQT 概念图（Entity / Factor / Entity-fact / Agent / Activity / Attribute / Activity-fact / Impact / Context factor / Resource / Cost 的 UML 类图式布局与连线方向）
- **Table 1**：每个 RQT 概念的 definition、example（text 中未逐行抽取 Table 1 内容）
- **Fig. 3**：RQT 的实例化示例（user story 场景的具体填入值）
- **Fig. 4**：57 篇文献的编码分布柱状图（每个 concept 的 bar height + dimension breakdown）
- **Fig. 5**：工具支持的架构概览图（各模块与数据流方向）

### 1.3 关键证据锚点（12 个）

| # | 锚点 | 原文章节/线索 | 短引或释义 |
|---|---|---|---|
| 1 | 论文类型声名 | 标题下方「VIEW POINT」标签 | "VIEW POINT" — 期刊明确标注为观点/评论文章 |
| 2 | 三大贡献 | Sect. 1, ¶2 | "(1) a harmonized requirements quality theory ... (2) an evaluation of the current state ... (3) a research roadmap" |
| 3 | RQT 理论类型 | Sect. 3, ¶1 | "the RQT is both explanatory ... and prescriptive" |
| 4 | RQT 概念清单 | Sect. 3.1, Fig. 2 + Table 1 | Entity, Factor, Entity-fact, Agent, Activity, Attribute, Activity-fact, Impact, Context factor, Resource, Cost — 共 11 个核心概念 |
| 5 | Entity 的可分解性 | Sect. 3.1, ¶2 | "Entities represent requirements artifacts of different granularity, which can be decomposed" |
| 6 | Activity 的非传统定义 | Sect. 3.1, ¶3 | "every process that takes a requirements entity as input and produces an output" — 不是传统 RE 活动分类 |
| 7 | Impact 的广义化 | Sect. 3.1, ¶5 | "we consider the impact to model any kind of relationship between Entity-facts and Activity-facts" |
| 8 | 样本来源 | Sect. 4.1 | "a sample of 57 primary studies" from "a previous research endeavor [7]" — 便利样本 |
| 9 | 编码方案设计 | Sect. 4.2 | extraction guideline based on RQT concepts; codes "created ad hoc in the first iteration and refined based on discussions" |
| 10 | IRR 报告 | Sect. 4.2, ¶end | percentage agreement 83.3%, Cohen's Kappa 54.2%, S-Score 76.8% ("good agreement") |
| 11 | 核心统计发现 | Sect. 4.3 | 42.1% entities reported implicitly; 29.8% no impact reported; 47.5% of impacts hypothesized; context factors "almost completely neglected" |
| 12 | 六条 roadmap 流 | Sect. 5.1–5.6 | (1) artifact & usage model, (2) taxonomy of quality factors, (3) impact framework, (4) context factors, (5) economic impact, (6) tool support |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象

**对象 = 57 篇 primary studies**，每篇都是需求质量因子文献（即提出或评估某个 requirements quality factor 的原始研究）。这些文献来自作者此前的一项系统研究 [7]（Frattini et al. 2022, "A live extensible ontology of quality factors for textual requirements"）。

### 2.2 系统检索 / 纳排 / 数据抽取 / 编码方案

- **检索**：无独立检索。直接复用 [7] 的 57 篇样本，分类为「convenience sampling」（非概率抽样）。
- **纳排**：无独立纳排流程。入口条件隐含为「提出或讨论 requirements quality factor 的 primary study」。
- **数据抽取**：每位作者（第一作者为主）使用 extraction guideline 对每篇文献在 RQT 各概念上分配 categorical code。
- **编码方案**：ad hoc 迭代生成。第一轮初步编码后，基于讨论和理论背景在第二轮细化。每个 RQT 概念关联一个或多个 categorical variable，每个 variable 包含一组 codes。

### 2.3 原文字段来源

字段来自 **RQT 概念模型本身**（即 Fig. 2 + Table 1 定义的 11 个概念），转化为 extraction guideline 中的 categorical variables。这不是外部分类法引用（如 IEEE 830、SWEBOK），而是作者自己构建的理论框架用作 codebook。

来源层级：
1. **直接来源**：RQT 概念模型（Sect. 3.1, Fig. 2, Table 1）
2. **操作化来源**：extraction guideline（Sect. 4.2，未在正文中全文列出，存在于 replication package `zenodo.8167598`）
3. **统计输出**：Fig. 4 的编码分布 + Sect. 4.3 的描述性统计

### 2.4 RQ 与样本单位的关系

RQ = "How are the concepts of the requirements quality theory reported in requirements quality literature?"

关系：**RQ 是编码框架的使用目的**（classification purpose），RQT 概念是编码维度（classification dimensions），57 篇 primary studies 是被编码对象（classified objects），Fig. 4 的分布统计是编码结果。

RQ 不是维度树的「根」——根是每篇 primary study。RQ 是整个 classification exercise 的驱动问题。

### 2.5 降级判定

本文不降级为「无系统样本库」。它有明确的 57 个编码对象、有 codebook、有 IRR 报告、有描述性统计。但它降级为「不进入主统计池」的理由已在上文 0 节说明（便利样本 + ad hoc 编码 + research commentary 类型）。

---

## 3. 原生样本编码维度树 / 维度森林

以下为该论文自己的原生编码 schema（即 RQT codebook tree），以 text tree 表示。**这不是六叶通用接口，而是 Frattini et al. 实际用于编码 57 篇 primary study 的分类框架。**

```
[ROOT] Primary Study (n=57)
│
├── [B1] Entity（需求实体）
│   ├── [L1.1] reported: yes/no（全部 57 篇均 report）
│   └── [L1.2] explicitness: explicit / implicit
│        取值空间类型: 布尔（reported）+ 层级枚举（explicit/implicit）
│        证据: Sect. 4.3 ¶1; 42.1% implicit
│
├── [B2] Factor（质量因子）
│   ├── [L2.1] reported: yes/no（全部 57 篇均 report）
│   ├── [L2.2] explicitness: explicit / referenced
│   └── [L2.3] form: textual description / logical or mathematical formula
│        取值空间类型: 层级枚举
│        证据: Sect. 4.2 ¶4–5; Sect. 4.3 ¶1
│
├── [B3] Entity-fact（实体事实）
│   └── [L3.1] reported: yes / no / N/A
│        取值空间类型: 层级枚举
│        证据: Fig. 4 (entity-fact bar); replication package 中
│
├── [B4] Agent（代理）
│   └── [L4.1] reported: yes / no
│        取值空间类型: 布尔
│        证据: Sect. 4.3 ¶2; 24.6% report agents
│
├── [B5] Activity（受影响活动）
│   ├── [L5.1] reported: yes / no
│   └── [L5.2] elicitation_method: ad hoc / systematic
│        取值空间类型: 层级枚举
│        证据: Sect. 4.3 ¶2; 92% ad hoc
│
├── [B6] Attribute（活动属性）
│   └── [L6.1] reported: yes / no
│        取值空间类型: 布尔
│        证据: Sect. 4.3 ¶2; 14% report attributes
│
├── [B7] Activity-fact（活动事实）
│   └── [L7.1] reported: yes / no / N/A
│        取值空间类型: 层级枚举
│        证据: Fig. 4 (activity-fact bar); replication package 中
│
├── [B8] Impact（影响关系）
│   ├── [L8.1] reported: N/A / yes
│   ├── [L8.2] evidence_type: hypothesized / inductive / referenced
│   ├── [L8.3] modality: necessary / possible
│   ├── [L8.4] generality: （编码存在但正文未报告细节，见 replication package）
│   └── [L8.5] frame_of_reference: （同上）
│        取值空间类型: 层级枚举
│        证据: Sect. 4.3 ¶3; 47.5% hypothesized
│
├── [B9] Context factor（上下文因素）
│   ├── [L9.1] process: reported: yes / no
│   ├── [L9.2] product: reported: yes / no（14/57 = 24.6%）
│   ├── [L9.3] people: reported: yes / no
│   ├── [L9.4] organization: reported: yes / no
│   └── [L9.5] tools: reported: yes / no（0/57）
│        取值空间类型: 布尔（每个子维度独立）
│        证据: Sect. 4.3 ¶4
│
├── [B10] Resource（资源）
│   └── [L10.1] reported: yes / no; if yes → type: money / time
│        取值空间类型: 层级枚举
│        证据: Sect. 4.3 ¶5; 8.8% report resources
│
└── [B11] Cost（成本）
    └── [L11.1] reported: yes / no; if yes → estimation: expected change / general magnitude
         取值空间类型: 层级枚举
         证据: Sect. 4.3 ¶5; 15.8% report cost
```

**说明**：
- 此树根节点是「每篇 primary study」，B1–B11 是 RQT 的 11 个概念用作编码维度，L 叶子是每个概念下的 categorical code。
- 部分叶子的确切取值集合需要查阅 replication package（Zenodo `8167598`），正文仅报告了最显著的统计分布。这在 A2a 精核阶段需要补齐。
- 这不是「维度森林」（多棵并列分类树），而是单棵 codebook 树，因为所有 57 篇样本使用同一套 RQT 概念框架编码。

---

## 4. 叶子维度表

仅列出正文有明确证据的叶子。标注 `[RP]` 表示详细取值依赖 replication package，正文未完整列出。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rqt-leaf-entity-explicitness` | 实体报告显式性 | Entity (B1) | Sect. 4.2 ¶4; extraction guideline | 实体是否明确定义 scope 与 form | {explicit, implicit} | 层级枚举 | implicit = 实体 scope 不明（如只说 "requirement" 而不定义粒度） | 42.1% implicit → 领域术语模糊 | Paper2 可类比：编码对象定义是否清晰 | 锚点 #5, #9 | 仅限 RQT 语境；Paper2 需自定义实体粒度 |
| `rqt-leaf-factor-explicitness` | 因子报告显式性 | Factor (B2) | Sect. 4.2 ¶5 | 因子是显式定义还是引用自其他文献 | {explicit, referenced} | 层级枚举 | 待查 RP | 描述因子定义的来源分布 | — | 锚点 #9 | — |
| `rqt-leaf-factor-form` | 因子表达形式 | Factor (B2) | Sect. 4.2 ¶5 | 因子以文本描述还是逻辑/数学公式表达 | {textual, logical/mathematical} | 层级枚举 | 待查 RP | 描述因子的可操作化程度 | Paper2 可类比：LLM 生成的 state machine 质量因子是 textual 还是 formulaic | 锚点 #9 | — |
| `rqt-leaf-agent-reported` | 代理是否报告 | Agent (B4) | Sect. 4.3 ¶2 | 是否报告参与活动的 agent | {yes, no} | 布尔 | no = 未考虑 agent | 24.6% 报告 | — | 锚点 #11 | — |
| `rqt-leaf-activity-elicitation` | 活动引出方式 | Activity (B5) | Sect. 4.3 ¶2 | 受影响活动的识别是否有系统方法 | {ad_hoc, systematic, N/A} | 层级枚举 | N/A = 未报告 activity | 92% ad hoc → 缺乏系统活动模型 | Paper2 可类比：verification activity 是否系统定义 | 锚点 #11 | — |
| `rqt-leaf-attribute-reported` | 活动属性是否报告 | Attribute (B6) | Sect. 4.3 ¶2 | 是否报告活动的可测属性 | {yes, no} | 布尔 | no = 未量化活动 | 14% 报告 | — | 锚点 #11 | — |
| `rqt-leaf-impact-evidence` | 影响证据类型 | Impact (B8) | Sect. 4.3 ¶3 | 影响关系的证据来源 | {hypothesized, inductive, referenced, N/A} | 层级枚举 | N/A = 未报告 impact | 47.5% hypothesized → 缺乏实证 | Paper2 关键迁移：verification 结果的 evidence type 分类 | 锚点 #11 | 取值空间可扩展 |
| `rqt-leaf-impact-modality` | 影响模态 | Impact (B8) | Sect. 4.3 ¶3 | 影响关系是确定性的还是可能性的 | {necessary, possible} | 层级枚举 | 待查 RP | balance between necessary and possible | — | 锚点 #11 | — |
| `rqt-leaf-context-product` | 产品上下文因素 | Context factor (B9) | Sect. 4.3 ¶4 | 是否报告产品相关上下文（如系统规模/类型） | {yes, no} | 布尔 | no = 未控制上下文 | 24.6% report | Paper2 可类比：state machine 的 system context 是否报告 | 锚点 #11 | — |
| `rqt-leaf-context-tools` | 工具上下文因素 | Context factor (B9) | Sect. 4.3 ¶4 | 是否报告工具影响 | {yes, no} | 布尔 | no = 未考虑工具因素 | 0% report | — | 锚点 #11 | — |
| `rqt-leaf-resource-type` | 资源类型 | Resource (B10) | Sect. 4.3 ¶5 | 受影响的资源类型 | {money, time, N/A} | 层级枚举 | N/A = 未报告 resource | 8.8% report any | — | 锚点 #11 | — |
| `rqt-leaf-cost-estimation` | 成本估算方式 | Cost (B11) | Sect. 4.3 ¶5 | 成本如何估算 | {expected_change, general_magnitude, N/A} | 层级枚举 | N/A = 未报告 cost | 15.8% report any | — | 锚点 #11 | — |

**注**：[RP] 标记的叶子（Entity-fact 的详细 codes、Activity-fact 的详细 codes、Impact 的 generality 和 frame_of_reference 维度）正文明确说「yielded no additional insight」或「contained in the replication package」，正文未展开其取值空间。A2a 精核时可选择下载 replication package 补全，或标记为 `schema_seed_待补`。

---

## 5. 关系边表

本文的编码 schema 本质上是 **flat categorical coding**：每篇 primary study 在每个 RQT 概念上分配一个 code。概念之间存在 RQT 理论定义的关系（例如 Entity-fact 和 Activity-fact 之间通过 Impact 连接），但这些关系是 **理论层的关系**，不是编码层的关系——即作者没有在 57 篇样本之间编码「Entity A 的 Factor X 通过 Impact Y 影响 Activity B 的 Attribute Z」这样的跨概念关系实例。

因此，**编码层未发现显式关系边**。编码 schema 是一个以 primary study 为根的 flat multi-attribute 分类，每个 attribute（RQT 概念）独立编码。

但 **理论层存在显式关系**（来自 RQT 概念模型 Fig. 2），值得记录为 schema seed：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rqt-rel-entity-factor` | Entity (B1) | has_quality | Factor (B2) | Factor 取值空间 | — | Fig. 2 | 理论关系：实体拥有质量因子 |
| `rqt-rel-factor-entityfact` | Factor (B2) | evaluates_to | Entity-fact (B3) | Entity-fact 取值空间 | — | Fig. 2 | 因子对实体的评估形成实体事实 |
| `rqt-rel-entityfact-impact` | Entity-fact (B3) | impacts | Activity-fact (B7) | 通过 Impact (B8) 的取值空间 | Impact not reported → 关系断裂 | Fig. 2; 锚点 #7 | 核心因果链：实体质量 → 活动效果 |
| `rqt-rel-agent-activity` | Agent (B4) | performs | Activity (B5) | Activity 取值空间 | Agent not reported → 执行者不明 | Fig. 2 | — |
| `rqt-rel-activity-activityfact` | Activity (B5) | measured_by | Activity-fact (B7) | 通过 Attribute (B6) | Attribute not reported → 无法量化 | Fig. 2 | — |
| `rqt-rel-context-impact` | Context factor (B9) | moderates | Impact (B8) | Context factor 各子维度取值空间 | Context not reported → 调节效应缺失 | Fig. 2; 锚点 #11 | 关键：上下文调节 impact 关系 |
| `rqt-rel-activityfact-resource` | Activity-fact (B7) | consumes | Resource (B10) | Resource 取值空间 | — | Fig. 2 | — |
| `rqt-rel-resource-cost` | Resource (B10) | translates_to | Cost (B11) | Cost 取值空间 | — | Fig. 2 | — |

这些理论关系边对 Paper2 的方法学启发是：如果 Paper2 要构建自己的 researcher-defined meta-model，需要考虑对象之间的因果/结构关系，而不仅仅是 flat attribute coding。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段/统计表支持的统计观察

以下观察直接来自 Fig. 4 + Sect. 4.3 的描述性统计，有明确数字支撑：

| # | 统计观察 | 支持数据 | 证据强度 |
|---|---|---|---|
| SO1 | 100% 的文献报告 Entity 和 Factor（artifact-centric 全覆盖） | 57/57 | strong（全样本） |
| SO2 | 42.1% 的 Entity 被隐式报告，scope 不清 | 24/57 | strong |
| SO3 | 29.8% 的文献完全不报告 Impact，切断实践相关性 | 17/57 | strong |
| SO4 | 仅 24.6% 报告 Agent | 14/57 | strong |
| SO5 | 92% 的 Activity 是 ad hoc 引出的（37/40） | 37/40 | moderate（分母 40 = 报告了 activity 的子集） |
| SO6 | 仅 14% 报告 Attribute | 8/57 | strong |
| SO7 | 47.5% 的 Impact 证据类型是 hypothesized | 19/40 | moderate（分母是报告 impact 的子集） |
| SO8 | Context factor 几乎被完全忽视（tools 0%） | 0/57–14/57 | strong |
| SO9 | Resource 和 Cost 极少报告（8.8% / 15.8%） | 5/57, 9/57 | strong |

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

以下来自 Sect. 4.4（Interpretation）和 Sect. 5（Roadmap），属于作者基于统计观察的推论与方向性建议，**不是从编码表中直接统计得出的 finding**：

| # | 候选 finding | 来源 | 性质 |
|---|---|---|---|
| CF1 | 「需求质量研究偏 artifact-centric，忽视 activity-related 概念」 | Sect. 4.4 | 统计观察的定性总结 |
| CF2 | 「缺少 activity perspective 使质量因子沦为规范性规定，阻碍工业采纳」 | Sect. 4.4 | 因果推论（有支撑但非直接证据） |
| CF3 | 「需要一个 reference model for requirements-affected activities 来系统化活动识别」 | Sect. 5.1 (roadmap) | 方向性建议 |
| CF4 | 「impact 关系应建模为回归问题而非简单分类/线性关系」 | Sect. 5.3 (roadmap) | 方法学建议 |
| CF5 | 「interpretation sub-activity 最易出错，可解释社区对 ambiguity 的关注」 | Sect. 5.1 | 推测性解释 |
| CF6 | 「工具支持架构」 | Sect. 5.6, Fig. 5 | 设计蓝图（非 finding） |

### 6.3 对 Paper2 可迁移的方法学启发

| # | 启发 | 迁移方式 |
|---|---|---|
| M1 | **「先定义理论对象与关系 → 用对象级 codebook 评价现有研究 → 把缺口组织成 roadmap」的三段式结构** | 可直接作为 Paper2 的整体论文架构模板：定义 state machine quality meta-model → 用 meta-model 评价现有 LLM-for-STM 文献 → roadmap |
| M2 | **codebook 的 ad hoc 迭代 + IRR 验证模式** | Paper2 在构建自己的 classification schema 时可采用类似的两轮编码 + IRR 流程 |
| M3 | **活动视角（activity-based perspective）** | Paper2 的 verification 部分可借鉴：不仅评价 state machine 本身的属性，还要评价 state machine 在后续 verification activity 中的 impact |
| M4 | **impact 的 evidence type 分类（hypothesized / inductive / referenced）** | Paper2 在评价 LLM 生成的 state machine 质量时，可对不同 quality claim 区分 evidence type |
| M5 | **便利样本的局限性透明报告** | Paper2 若使用非概率样本，应明确报告并限制统计推广范围 |

### 6.4 绝不能迁移的领域结论

- requirements quality 的具体 quality factor 列表（ambiguity、passive voice、template conformance 等）→ 与 state machine 无关
- 57 篇文献的具体统计数字 → 领域特定
- 「工业界对需求质量因子持怀疑态度」→ 领域特定
- economic impact 的具体 resource/cost 分类 → 领域特定，但分类思路可借鉴

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 C 级（Critical — 必须修正）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| C1 | **维度树未区分「原生 RQT codebook 树」与「跨论文六叶投影」**。现有 `review.md` 的维度树使用 `orig-quality-construct`、`orig-theory-model`、`orig-evaluation-method`、`orig-roadmap-question`、`orig-boundary` 五节点，这是从论文的功能结构（theory / evaluation / roadmap）派生的分类，而非作者实际用于编码 57 篇文献的 codebook。 | A.1 维度树定义部分 | **(a)** 新增一节「原生编码维度树」，以 RQT 11 概念为 B1–B11、每概念下的 categorical codes 为 leaf，完整复原 codebook tree（参考本报告第 3 节）。**(b)** 将现有五节点树显式标记为「跨论文功能结构投影（A1-M* 投影层）」，不要混入原生树。**(c)** 在 SUMMARY 表中修正 `原生树类型` 为 `单树（RQT codebook 树）`。 |
| C2 | **叶子维度表中的叶子全部是「六叶通用叶子」**（orig-quality-construct, orig-theory-model, orig-evaluation-method, orig-roadmap-question, orig-boundary, orig-meta-layer），不是 RQT codebook 的实际叶子。 | A.1 叶子维度表 | 重写叶子维度表，以本报告第 3 节中的 L1.1–L11.1 为叶子标识。保留六叶叶子作为独立的「跨论文投影叶子表」。 |
| C3 | **SUMMARY 表中 `样本单位 / 样本数量 / 原生树类型 / 统计池资格` 需要修正**。当前 `review.md` 未明确标注「样本单位 = 57 篇 primary studies」，也未给出原生树类型。 | 结论卡片或 SUMMARY 部分 | 补全：(a) 样本单位 = 57 篇 primary studies（便利样本）；(b) 样本数量 = 57；(c) 原生树类型 = 单树（RQT codebook 树）；(d) 统计池资格 = 局部可统计（不进入主 SLR/SMS 统计池）。 |

### 7.2 I 级（Important — 建议修正）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| I1 | **A.2 证据账本中缺少对 RQT codebook 叶子取值空间的证据条目**。现有 A.2 的证据条目主要覆盖 paper 结构层面（理论/评价/路线图），未记录 Fig. 4 中各 code 分布的具体数字来源。 | A.2 证据账本 | 新增 8–10 条证据条目，对应 SO1–SO9 的每个统计观察，标注来源为 Sect. 4.3 + Fig. 4。 |
| I2 | **未记录 replication package 的存在与局限性**。正文明确提到 replication package 在 Zenodo (`8167598`)，但 `review.md` 未提及。Impact 的 generality 和 frame_of_reference 维度、Entity-fact 和 Activity-fact 的详细 codes 仅在 replication package 中。 | A.1 或 A.2 | 新增「外部依赖」条目：标注 replication package DOI，说明哪些叶子需要外部数据补全。 |
| I3 | **Fig. 4 / Table 1 / Fig. 2 的版面核验状态未独立记录**。现有 `review.md` 只说「图形细节待人工原文核对」，未逐图列出具体核验需求。 | A.4 人工核验清单 | 将 Fig. 2 / Table 1 / Fig. 3 / Fig. 4 / Fig. 5 各列为独立检查项，每项标注需核验的具体内容（如 Fig. 2 的箭头方向、Table 1 的 definition 列）。 |

### 7.3 M 级（Minor — 可选修正）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| M1 | `review.md` 的 A.3 conclusion map 中有 9 条 `clm-*` 条目，全部标记为 `weak` / `schema_seed` / `boundary_anchor` / `candidate_finding`。这些条目描述的是本论文的功能角色，而非对 RQT codebook 内部结构的结论。建议新增 3–5 条针对 codebook 内部结构的结论条目（如「42.1% 的 entity 隐式报告」→ 统计观察级结论）。 | A.3 | 新增以 SO1–SO9 为来源的结论条目，标记结论类型为 `statistical_observation`。 |
| M2 | 「一句话结论」说「最值得迁移的是三段式结构」，但未提及 codebook design pattern（ad hoc 迭代 + IRR）本身也是可迁移资产。 | 快速结论卡片下方 | 补充一句关于 codebook design pattern 的可迁移性。 |

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-002 | paper_content.txt | Sect. 3.1 | Fig. 2; Table 1; ¶1–6 | "The concepts that constitute this theory are visualized in Fig. 2, and each concept is described in Table 1" | 定义 RQT 11 概念及其关系 | strong（正文明确定义） | B1–B11 全部节点; 关系边 R1–R8 | 是 — Fig. 2 的节点连线方向、Table 1 的 definition/example 列 | 仅限 RQT 语境 |
| EV-003 | paper_content.txt | Sect. 4.1 | ¶1 | "a sample of 57 primary studies" from [7]; "convenience sampling" | 确定样本单位与抽样方式 | strong | 根节点（Primary Study n=57） | 否 | 便利样本 → 不可推广至全体需求质量文献 |
| EV-004 | paper_content.txt | Sect. 4.2 | ¶3–7 | "extraction guideline based on the RQT concepts"; codes "created ad hoc ... refined"; percentage agreement 83.3%, Kappa 54.2%, S-Score 76.8% | 定义编码方案设计与 IRR | strong | B1–B11 的编码方法学 | 否 — IRR 数字来自正文 | ad hoc 编码 → 不可视为 validated instrument |
| EV-005 | paper_content.txt | Sect. 4.3 | ¶1 | "42.1% of entities is reported implicitly"; "all 57 publications" report entity and factor | 支撑 L1.2 (entity explicitness) 的统计分布 | strong | L1.2 | 是 — Fig. 4 bar chart exact values | 仅限此 57 篇样本 |
| EV-006 | paper_content.txt | Sect. 4.3 | ¶2 | "29.8% do not report any impact"; "Agents are only reported in 14 (24.6%)"; "Activities ... predominantly elicited ad hoc (92%)"; "Attributes ... only rarely reported (8/57=14%)" | 支撑 B4–B8 各叶子的统计分布 | strong | L4.1, L5.2, L6.1, L8.1 | 是 — Fig. 4 的 activity 相关 bars | 仅限此 57 篇样本 |
| EV-007 | paper_content.txt | Sect. 4.3 | ¶3 | "evidence for the impact ... dominantly hypothesized (19/40=47.5%)"; "modality ... balanced between necessary and possible" | 支撑 L8.2 (impact evidence type) 和 L8.3 (modality) | strong | L8.2, L8.3 | 是 — Fig. 4 impact dimension bars | 分母 40 = 报告 impact 的子集 |
| EV-008 | paper_content.txt | Sect. 4.3 | ¶4 | "Context factors are almost completely neglected"; tools 0/57; product 14/57 (24.6%) | 支撑 B9 各子叶子的统计分布 | strong | L9.1–L9.5 | 是 — Fig. 4 context factor bars | 仅限此 57 篇样本 |
| EV-009 | paper_content.txt | Sect. 4.3 | ¶5 | "cost and resources are reported only rarely (9/57=15.8% and 5/57=8.8%)"; "never determined empirically" | 支撑 B10/B11 叶子的统计分布 | strong | L10.1, L11.1 | 是 — Fig. 4 cost/resource bars | 仅限此 57 篇样本 |
| EV-010 | paper_content.txt | Sect. 4.3 | ¶5 | "Money and time are mentioned as the resources"; cost estimated as "expected change" or "general magnitude" | 支撑 L10.1 和 L11.1 的取值空间 | moderate（取值空间描述简略） | L10.1 (type), L11.1 (estimation) | 否 | 取值空间可能 incomplete |
| EV-011 | paper_content.txt | Sect. 4.3 | ¶3 | "The remaining two dimensions of impact (generality and frame of reference) yielded no additional insight ... contained in the replication package" | 标记 L8.4/L8.5 需要外部数据 | moderate（正文承认未报告） | L8.4, L8.5 | 否 — 需查 replication package | 正文无数据，依赖外部 |
| EV-012 | paper_content.txt | Sect. 5.1–5.6 | 各小节 | 六条 roadmap stream 的命题 | 支撑候选发现 CF3–CF6 | weak（roadmap 是方向性建议，非 evidence-based finding） | CF3–CF6 | 否 | 不可当作已验证结论迁移 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CONC-001 | 本文的样本单位是 57 篇 primary studies（需求质量因子文献），编码框架是 RQT 11 概念模型用作 codebook | sample_unit_identification | 根节点; B1–B11 | EV-003, EV-004 | strong | 维度树根节点定义；统计池资格判定 | 便利样本；非概率抽样 |
| CONC-002 | 原生维度树是单棵 codebook 树：每篇 primary study 在 11 个 RQT 概念上分配 categorical code，形成 flat multi-attribute 编码 | native_tree_type | 整棵树 | EV-002, EV-004 | strong | 维度树类型标注 | 不是维度森林（无多棵并列分类树） |
| CONC-003 | 100% 文献报告 Entity 和 Factor，但 42.1% 的 Entity 隐式报告 | statistical_observation | L1.2 | EV-005 | strong | 描述 artifact-centric 偏向的证据 | 仅限此 57 篇样本 |
| CONC-004 | 29.8% 完全不报告 Impact；47.5% 的 Impact 证据为 hypothesized | statistical_observation | L8.1, L8.2 | EV-006, EV-007 | strong | 描述 evidence gap 的证据 | 分母为 40（报告 impact 的子集） |
| CONC-005 | Context factor 几乎被忽视（tools 0%，product 最高 24.6%） | statistical_observation | L9.1–L9.5 | EV-008 | strong | 描述 context gap 的证据 | 仅限此 57 篇样本 |
| CONC-006 | 本文不可进入 SLR/SMS 主统计池 | eligibility_judgment | 根节点 | EV-003, EV-004 | strong | 统计池 gate | 便利样本 + ad hoc 编码 + research commentary 类型 |
| CONC-007 | 本文对 Paper2 的核心可迁移资产是「理论对象 → codebook 评价 → roadmap」三段式结构 + codebook design pattern | migration_heuristic | 全树 | EV-002, EV-004, 全量统计观察 | moderate | Paper2 论文架构设计；classification schema 设计 | 不可迁移领域特定结论 |
| CONC-008 | RQT 概念之间存在理论层关系边（Entity→Factor→Entity-fact→Impact→Activity-fact 因果链），但编码层未编码跨概念关系实例 | schema_limitation | R1–R8 | EV-002 | moderate | Paper2 meta-model 的关系设计参考 | 关系边的取值空间需 Paper2 自行定义 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取技能文件及采用原则

| 技能文件 | 采用原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | **Claim-evidence engineering workflow**：每条结论必须绑定证据锚点；无证据则降级。本报告所有统计观察均标注原文章节与短引。**Evidence gate** 原则贯穿全文。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | **Common Reviewer Concerns**：特别关注「claims in Abstract exceed evidence」→ 本报告将 roadmap 建议与统计观察明确分开。**Constructive Specificity Standard**：每个返修建议都指向 `review.md` 的具体位置与具体修正动作。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | **Claim Audit**：对 A.3 的每条结论做了 claim → evidence → risk → revision 的思维校验。**Adversarial Questions**：对照检查了「样本单位到底是什么」「原生树是否真的是原文自己的编码框架」。 |
| `research-planning/SKILL.md` | 主要借鉴其「明确研究上下文 → 结构化输出」的 workflow 思维，用于组织本报告的章节结构。 |
| `research-planning/references/planning-prompts.md` | 间接用于理解「plan 应先于 code」的 contract-first 原则在本审计任务中的对应：先判定样本单位与字段来源，再复原维度树。 |
| `research-planning/references/output-schemas.md` | 未直接使用其 JSON schema，但借鉴了 task dependency 的结构化思维用于组织返修建议的 C/I/M 优先级。 |
| `autoresearch/SKILL.md` | **Completion artifact gate** 原则：不因「看起来完成」而声称完成，必须有可审计的证据链。直接指导了本报告的 0 节审计结论卡片和 9.2 节风险自审。 |

### 9.2 本输出最高风险 3 点及主线程合并复核建议

| # | 风险 | 风险等级 | 主线程复核方式 |
|---|---|---|---|
| R1 | **RQT codebook 的部分叶子取值空间依赖 replication package（Zenodo `8167598`）**，正文未完整列出。本报告已在叶子上标注 `[RP]`，但若主线程直接将这些叶子填入 SUMMARY 统计表而未经 replication package 核验，可能引入 incomplete 取值空间。 | high | 主线程合并前：(a) 尝试获取 replication package 中的 extraction guideline spreadsheet；(b) 若不可获取，将 `[RP]` 叶子标记为 `schema_seed_待外部数据`，不得进入任何定量统计。 |
| R2 | **Fig. 2 / Fig. 4 / Fig. 5 / Table 1 未经版面级核验**。本报告的关系边方向、节点命名、统计数字均基于 text extraction 的 prose 描述推导。若 PDF 原图与 prose 描述存在偏差（如 Fig. 2 的箭头实际方向与 text 描述不同），则维度树可能需要微调。 | medium | 主线程合并前：至少人工打开 `paper.pdf` 核对 Fig. 2 的节点与连线、Fig. 4 的 bar height 与数字标注。将核对结果记录到 A.4 人工核验清单。 |
| R3 | **现有 `review.md` 的 A.1–A.4 体系与本报告的维度树体系存在结构性差异**。本报告以 RQT codebook 为主树，`review.md` 以功能结构（theory/evaluation/roadmap）为主树。合并时若简单叠加而不做结构性 reconciliation，会导致两份树并存、互相矛盾。 | medium | 主线程合并策略：(a) 以本报告的 RQT codebook 树为「原生维度树」（A.1 主节）；(b) 将 `review.md` 的五节点功能结构树降级为「跨论文功能投影」（A.1 子节或附录）；(c) 同步更新叶子维度表、关系边表、A.2/A.3 的证据条目编号以匹配新树。 |

### 9.3 blocked / timeout / 文件缺失状态

| 状态 | 说明 |
|---|---|
| **未 blocked** | 所有必需文件均可读取，无权限错误。 |
| **未 timeout** | 所有命令在正常时间内返回。 |
| **文件缺失** | 无。`paper_content.txt`（1187 行）、`bibtex.bib`、`metadata.json`、`review.md`、`paper.pdf` 均存在且可读。 |
| **部分内容依赖外部** | RQT codebook 的完整 categorical code 集合依赖 replication package（Zenodo `8167598`）；Impact 的 generality 和 frame_of_reference 维度正文未展开。这些不是文件缺失，而是原文设计如此。 |

---

**审计完成。** 本报告是自包含完整报告，所有必填章节均已包含实质内容。可直接用于主线程重写 `review.md` 的 A.1–A.4 部分。