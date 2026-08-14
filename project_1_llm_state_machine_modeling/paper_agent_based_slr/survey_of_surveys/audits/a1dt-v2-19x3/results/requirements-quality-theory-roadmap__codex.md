### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `requirements-quality-theory-roadmap` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已通读 14 页提取文本，重点核对 Sect. 3 RQT、Sect. 4 survey、Sect. 5 roadmap、threats 与 conclusion。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；`bibtex.bib` 确认 DOI、期刊、页码、年份；`metadata.json` 确认本地元信息、非主统计池标注与 schema seed 角色。 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo`、`pdftotext -layout` 和关键页 PNG 截图核对 PDF 第 4、8、11 页，覆盖 Fig. 2、Table 1、Fig. 4、Fig. 5。未下载或核验 Zenodo replication package。 |
| 原文类型 | other：research commentary / theory + survey-based evaluation + roadmap；不是标准 SLR/SMS/tertiary。 |
| 被编码样本单位 | 57 篇 requirements quality primary studies/publications，来自作者先前 systematic study 的 convenience sample。 |
| 样本数量 / 分母 | 原生 survey 分母为 57 篇；impact 子分母常为 40 篇；activities 子分母常为 40 篇。 |
| 原生树类型 | 维度森林：RQT 理论概念关系树 + 基于 RQT concept 的 publication-level categorical coding scheme；roadmap 是候选 action forest，不是样本编码主树。 |
| 主统计池资格 | 局部可统计：可统计“57 篇需求质量文献如何报告 RQT 概念”；但对本项目 A1 主统计池应降级为 `schema_seed` / `boundary_anchor`，因为本文不是标准 SLR/SMS/tertiary 且样本为 convenience sampling。 |
| 总体判定 | needs repair：当前 `review.md` 已有返修痕迹，但仍混入六叶通用接口和旧 v1 入口，需按原文 RQT-coded survey schema 重写。 |

### 1. 原文证据阅读说明

本轮实际读取了：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- `bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`

PDF 版面核验：已核对 `paper.pdf` 第 4 页 Fig. 2，第 5 页 Table 1 的 layout 文本，第 8 页 Fig. 4，第 11 页 Fig. 5。Fig. 4 中小字 code label 做了视觉核验，但完整 codebook 仍需 replication package 精核。

关键原文证据锚点：

1. 摘要：贡献是 harmonized theory、state evaluation、research roadmap；说明本文是 theory/evaluation/roadmap。
2. Sect. 3：RQT 被定位为 explanatory + prescriptive theory。
3. Fig. 2：RQT 三块结构：requirements artifact、requirements-affected activity、software process economics。
4. Table 1：列出 11 个 RQT concepts：Entity、Factor、Entity-fact、Agent、Activity、Attribute、Activity-fact、Impact、Context factor、Cost、Resource。
5. Sect. 3.1：Impact 被扩展为 Entity-facts 与 Activity-facts 之间“any kind of relationship”。
6. Sect. 4：唯一明确 survey RQ 是“RQT concepts 如何在 requirements quality literature 中被报告”。
7. Sect. 4.1：survey objects 是 57 篇 primary studies，sampling 是 non-probabilistic / convenience。
8. Sect. 4.2：instrument 是 extraction guideline；每个 RQT concept 对应一个或多个 categorical variables。
9. Fig. 4 / Sect. 4.3：报告 Entity 57、Factor 57、Impact 40/57、Agent 14/57、Attribute 8/57、Cost 9/57、Resource 5/57 等分布。
10. Sect. 4.5：threats 明确指出样本约束和隐式概念抽取困难。
11. Sect. 5.1--5.6：roadmap 六流：artifact and usage model、quality factor taxonomy、impact framework、context factors、economic impact、tool support。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是什么？

原文逐项编码对象是 57 篇 requirements quality primary studies/publications，不是工具、数据集、LLM 输出、roadmap action，也不是本文的参考文献全集。Sect. 4.1 明确说目标 population 是 dealing with quality factors in requirements artifacts 的 requirements quality literature，样本来自先前 systematic study。

2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

本文自身没有重新执行完整系统检索；它继承作者先前 systematic study 的 57 篇样本，并明确称为 convenience sampling。它有数据抽取和编码方案：基于 RQT concepts 建立 extraction guideline；每个 concept 对应 categorical variables 和 codes；第一作者全量编码，第二作者对 6 篇做 instrument validation，其中 4 篇用于 inter-rater reliability。

3. 原文字段来自哪里？

字段主要来自 RQT concept model 和 extraction guideline。Table 1 给出 concept definitions；Fig. 4 和 Sect. 4.3 给出部分 codes / dimensions / distributions。完整 codebook 未在正文完全展开，作者说包含在 replication package 中，本轮未核验该外部包。

4. RQ 与样本单位是什么关系？

RQ 不是维度树根，也不是 SLR 问题列表；RQ 是使用 RQT-coded extraction instrument 对 57 篇 publication 做 descriptive statistics 的评价问题。真正的编码根对象是 “publication in requirements quality literature”；主干字段来自 RQT concepts。

5. 若无系统样本库，如何降级？

本文不是“无系统样本库”：它有 57 篇样本。但样本来自先前研究且为 convenience sample，因此对本项目应降级为局部可统计。可使用它的 RQT → codebook → coverage → roadmap 推理结构；不得把 requirements quality 领域统计结论并入 Paper2 主统计发现。

### 3. 原生样本编码维度树 / 维度森林

```text
sample_unit: requirements quality publication / primary study (n = 57)
└── RQT concept reporting codebook
    ├── Artifact-related concepts
    │   ├── Entity
    │   │   ├── presence/count: reported in 57/57
    │   │   └── reporting explicitness: explicit / implicit
    │   ├── Factor
    │   │   ├── presence/count: reported in 57/57
    │   │   ├── explicitness: explicit / implicit / referenced
    │   │   └── form: descriptive / formula
    │   └── Entity-fact
    │       └── derived relation: Entity characterized by Factor
    ├── Activity-related concepts
    │   ├── Agent
    │   │   └── presence/count: reported in 14/57
    │   ├── Activity
    │   │   ├── presence/count: reported in 40/57
    │   │   └── elicitation/source: ad hoc / supposedly systematic / systematic
    │   ├── Attribute
    │   │   └── presence/count: reported in 8/57
    │   └── Activity-fact
    │       └── derived relation: Activity characterized by Attribute
    ├── Impact relationship
    │   ├── presence/count: reported in 40/57; N/A in 17/57
    │   ├── evidence: hypothesized / inductive / referenced
    │   ├── modality: necessary / possible
    │   ├── generality: in replication package, not reported in main text
    │   └── frame of reference: in replication package, not reported in main text
    ├── Context factors
    │   ├── presence/count: up to 14/57 depending category
    │   └── category: product / process / tools / people / organization / market
    ├── Economic concepts
    │   ├── Cost
    │   │   ├── presence/count: 9/57
    │   │   └── evidence/status: hypothesized or referenced, never empirically determined
    │   └── Resource
    │       ├── presence/count: 5/57
    │       └── resource type examples: money / time
    └── Reliability / process metadata
        ├── extraction role: first author full extraction
        ├── validation role: second author on 6 publications
        ├── agreement: percentage agreement 83.3%
        ├── Cohen's Kappa: 54.2%
        └── S-Score: 76.8%
```

取值空间类型说明：

- 完整枚举：Table 1 的 11 个 RQT concepts。
- 层级枚举：artifact-related / activity-related / impact / context / economic。
- 部分枚举：Fig. 4 展示的 code categories；但 full codebook 未在正文完全展开。
- 数值或区间：57/57、40/57、14/57、8/57、9/57、5/57、83.3%、54.2%、76.8%。
- 关系值：Entity produces Entity-fact；Factor characterizes Entity-fact；Entity-fact impacts Activity-fact；Context factors influence Impact；Activity-fact causes Cost；Cost affects Resource。
- 待核验：impact generality、frame of reference 及完整 code definitions，需要 replication package。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1-entity-presence | 实体报告 | Artifact-related concepts | Table 1, Fig. 4, Sect. 4.3 | publication 是否报告 requirements entity | reported count；本文为 57/57 | 数值 / 布尔 | 未报告则该研究无法定位 quality factor 作用对象 | 统计 artifact-centric 覆盖 | 支撑“entity 普遍存在”观察 | Fig. 4；Sect. 4.3 | 只迁移“对象粒度必须明确”的方法学原则 |
| L2-entity-explicitness | 实体明确性 | Entity | Sect. 4.2, Fig. 4 | entity scope/form 是否清楚 | explicit / implicit；33/24 | 完整枚举 | implicit 表示只说 requirement 但粒度不清 | 统计 terminological ambiguity | 支撑“实体粒度不清”候选 finding | Sect. 4.2；Fig. 4 | 不迁移 requirements entity 的具体分类 |
| L3-factor-presence | 因子报告 | Artifact-related concepts | Table 1, Fig. 4 | 是否报告 normative metric / quality factor | reported count；57/57 | 数值 / 布尔 | 未报告则不属于此 survey 关注核心 | 统计 factor 覆盖 | 支撑 artifact-centric 偏置 | Table 1；Fig. 4 | 可迁移为“field/factor 必须定义” |
| L4-factor-explicitness | 因子来源明确性 | Factor | Sect. 4.2, Fig. 4 | factor 是显式报告、隐含还是引用他文 | explicit / implicit / referenced；Fig. 4 显示 explicit 53、implicit 3、referenced 2，存在多 code 维度叠加 | 部分枚举；需 codebook 精核 | 取值可能非互斥或按维度分组，缺失需看 replication package | 统计 factor 报告质量 | 支撑“factor reporting 不完全一致” | Sect. 4.2；Fig. 4 | 数字使用前需核验 full codebook |
| L5-factor-form | 因子形式 | Factor | Sect. 4.2, Fig. 4 | factor 以文本描述还是逻辑/数学公式给出 | descriptive / formula；Fig. 4 可见 descriptive 53、formula 4 | 部分枚举 | 未说明形式则待核验 | 统计 operationalization 程度 | 支撑“多数 factor 仍是 descriptive” | Sect. 4.2；Fig. 4 | 不直接迁移为 Paper2 字段质量结论 |
| L6-agent-presence | agent 报告 | Activity-related concepts | Table 1, Fig. 4, Sect. 4.3 | 是否报告参与 activity 的人、群体或自动化机制 | reported count；14/57 | 数值 / 布尔 | 未报告 agent 表示 activity 使用主体缺失 | 统计 activity perspective 覆盖 | 支撑“agent 被忽略” | Table 1；Sect. 4.3 | 可迁移为“human/LLM/tool actor 必须记录” |
| L7-activity-presence | activity 报告 | Activity-related concepts | Table 1, Fig. 4, Sect. 4.3 | 是否报告 requirements-affected activity | reported / N/A；40/57 reported，17/57 no impact | 数值 / 布尔 | N/A 表示未报告 activity impact | 统计 practical relevance gap | 支撑“17/57 不报告 impact” | Sect. 4.3 | 只迁移 activity-linked evidence 思路 |
| L8-activity-elicitation | activity 识别方式 | Activity | Fig. 4, Sect. 4.3 | impacted activities 如何被识别 | ad hoc / supposedly systematic / systematic；37/40 ad hoc，2 supposedly systematic，1 systematic | 完整枚举，正文足够支持 | 未报告 activity 时不适用 | 统计 systematic activity elicitation 缺口 | 支撑“活动选择非系统化” | Fig. 4；Sect. 4.3 | 可迁移为“分析活动需有识别规则” |
| L9-attribute-presence | activity attribute 报告 | Activity-related concepts | Table 1, Fig. 4, Sect. 4.3 | 是否报告 activity 的 measurable property | reported count；8/57 | 数值 / 布尔 | 未报告 attribute 表示缺少 dependent variable measurement | 统计可测量性缺口 | 支撑“无法经验评价 impact” | Sect. 4.3--4.4 | 可迁移为“审计活动属性要可测” |
| L10-impact-presence | impact 报告 | Impact relationship | Table 1, Fig. 4, Sect. 4.3 | 是否报告 entity-fact 对 activity-fact 的影响 | reported 40/57；N/A 17/57 | 数值 / 布尔 | N/A 表示没有 activity impact | 统计 relevance 支撑 | 支撑“normative rule 风险” | Fig. 4；Sect. 4.3 | 不迁移具体质量因子影响 |
| L11-impact-evidence | impact 证据类型 | Impact | Fig. 4, Sect. 4.3 | impact 关系的证据来源 | hypothesized 19/40；inductive 11/40；referenced 10/40 | 完整枚举，正文支持 | 未报告 impact 时不适用 | 统计证据强度分布 | 支撑“hypothesized evidence dominant” | Sect. 4.3 | 可迁移为 claim-evidence 分级 |
| L12-impact-modality | impact 模态 | Impact | Fig. 4, Sect. 4.3 | impact 是确定必要还是可能 | necessary 22；possible 18 | 完整枚举，正文支持 | 未报告 impact 时不适用 | 统计 claim modality | 支撑“impact certainty/potential balanced” | Fig. 4；Sect. 4.3 | 迁移为候选 finding 强弱标注 |
| L13-impact-other-dimensions | impact 其他维度 | Impact | Sect. 4.3 | generality、frame of reference | contained in replication package；main text not reported | 待核验 | 正文未报告，不能补造 | 不进入本轮统计 | A2a 精核入口 | Sect. 4.3 | 必须查 replication package |
| L14-context-category | context factor 类别 | Context factors | Fig. 4, Sect. 4.3 | 影响 impact relationship 的上下文因素类别 | product 14、process 7、tools 0、people 10、organization 7、market 0 | 部分枚举，图形核验支持 | 未报告 context 表示 external validity 风险 | 统计 context 覆盖 | 支撑“context nearly neglected” | Fig. 4；Sect. 4.3--4.4 | 迁移类别需重建为 Paper2 context |
| L15-cost-presence | 成本报告 | Economic concepts | Table 1, Fig. 4, Sect. 4.3 | 是否报告 activity-fact associated cost | 9/57 | 数值 / 布尔 | 未报告则无法连接经济决策 | 统计 economic perspective 缺口 | 支撑“工业接受度风险” | Sect. 4.3--5.5 | 可迁移为复核/运行成本字段 |
| L16-resource-presence | 资源报告 | Economic concepts | Table 1, Fig. 4, Sect. 4.3 | 是否报告受经济影响的 resource | 5/57；money/time examples | 数值 + 自由文本例 | 未报告则经济后果不完整 | 统计 resource 覆盖 | 支撑“resource rarely reported” | Sect. 4.3 | 不迁移为具体成本数值 |
| L17-validation-sample | instrument validation 样本 | Process metadata | Sect. 4.2 | 第二作者独立抽取的验证样本 | 6 publications；2 training；4 reliability | 数值 | 无验证则可靠性风险更高 | 报告编码可靠性 | 支撑“有但有限的 validation” | Sect. 4.2 | 可迁移为抽查设计模板 |
| L18-reliability-metrics | inter-rater reliability | Process metadata | Sect. 4.2 | 编码一致性指标 | percentage agreement 83.3%；Kappa 54.2%；S-Score 76.8% | 数值 | 未报告则抽取可信度不足 | 方法质量评估 | 支撑“instrument sufficiently reliable by authors” | Sect. 4.2 | 不可外推到本项目 agent 抽取可靠性 |
| L19-roadmap-stream | roadmap 研究流 | Roadmap | Sect. 5.1--5.6 | 根据 state evaluation 推出的未来研究方向 | artifact and usage model；quality factors taxonomy；impact framework；context factors；economic impact；tool support | 完整枚举 | 不适用，不是样本字段 | 不作为主统计字段 | 候选方法学启发 | Sect. 5 | roadmap action 不能当已验证 finding |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1-entity-decomposes | Entity | decomposes into | Entity | specification / section / paragraph / sentence / requirement examples | 未描述粒度则 entity implicit | Fig. 2；Sect. 3.1 | 说明 entity 可层级化 |
| E2-factor-decomposes | Factor | decomposes into | Factor | factor / sub-factor examples | 未描述 sub-factor 不代表不存在 | Fig. 2；Sect. 3.1 | 支持 factor 层级结构 |
| E3-factor-characterizes | Factor | characterizes | Entity-fact | entity + factor composition | 缺 factor 或 entity 则无法形成 entity-fact | Fig. 2；Table 1 | 定义 artifact-side fact |
| E4-entity-produces | Entity | produces | Entity-fact | entity-fact | 未显式关系则待核验 | Fig. 2 | 支持编码对象到 fact 的关系 |
| E5-entity-used-in | Entity | is used in | Activity | requirements-affected activity | 未报告 activity 则 impact practical relevance 缺失 | Fig. 2；Sect. 3.1 | 连接 artifact 与 activity |
| E6-agent-involved-in | Agent | is involved in | Activity | person / group / automatism | 未报告 agent 则活动主体缺失 | Fig. 2；Table 1 | 支持 agent 字段 |
| E7-activity-decomposes | Activity | decomposes into | Activity | understanding / programming / validation subactivity examples | 未报告 subactivity 不代表无分解 | Sect. 3.1--3.2 | 支持 activity 层级 |
| E8-attribute-characterizes | Attribute | characterizes | Activity-fact | measurable property | 未报告 attribute 则 dependent variable 缺失 | Fig. 2；Table 1；Sect. 4.4 | 支持可测 activity-fact |
| E9-activity-produces-fact | Activity | composes with Attribute | Activity-fact | activity + attribute | 未报告 attribute 时 activity-fact 不完整 | Fig. 2；Table 1 | 支持 impact 目标定义 |
| E10-impact-link | Entity-fact | impacts | Activity-fact | any relationship；categorical / linear / complex possible | 未报告 impact 则质量因子停留在 normative rule | Fig. 2；Sect. 3.1--3.2 | 核心关系边 |
| E11-context-influence-impact | Context factor | influences | Impact | product / process / tools / people / organization / market 等 | 未报告 context 则 external validity 风险 | Fig. 2；Sect. 3.1；Fig. 4 | 支持 context 字段 |
| E12-activityfact-causes-cost | Activity-fact | causes | Cost | cost magnitude | 未报告 cost 则 economic impact unknown | Fig. 2；Sect. 3.1；Sect. 5.5 | 支持经济层 |
| E13-cost-affects-resource | Cost | affects | Resource | time / money examples | 未报告 resource 则成本对象不明确 | Fig. 2；Table 1 | 支持 resource 字段 |
| E14-roadmap-derived-from-gap | State evaluation gaps | motivates | Roadmap streams | six streams | roadmap 不是样本字段；缺失不影响 publication coding | Sect. 4.4；Sect. 5 | 候选启发，不进主统计 |

本文有显式关系型 schema，不能写成“未发现显式关系边”。但注意：Fig. 2 的 RQT 关系边是作者理论模型；Fig. 4 的 survey code 才是 publication-level 统计编码。两者相关但不能混成同一种样本字段。

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段 / 统计表支持的统计观察：

- 57/57 publications report Entity and Factor；artifact-related concepts 覆盖最高。
- 24/57 entities are implicit，说明 entity scope/form 经常不清。
- 17/57 publications do not report activity impact。
- Agent only 14/57；Attribute only 8/57。
- Activity reporting 中 37/40 是 ad hoc，systematic 只有 1，supposedly systematic 2。
- Impact evidence 在 40 篇中以 hypothesized 为主：19/40；inductive 11/40；referenced 10/40。
- Context factors 覆盖很低；tools 和 market 为 0，product 最高为 14/57。
- Cost 9/57，Resource 5/57，且没有 empirical determination。

原文 discussion / recommendation / roadmap 提出的候选 finding：

- requirements quality literature 存在 artifact-centric bias。
- 忽略 activity、attribute、context、economic impact 会削弱 practical relevance。
- 非系统化选择 impacted activities 可能遗漏正负影响并存的关系。
- 缺少 activity attributes 会阻碍 impact 的 empirical evaluation。
- 需要从 impact taxonomy 升级为 impact framework。
- 需要 context factors、economic impact 和 tool support 研究流。

对 Paper2 可迁移的方法学启发：

- 先建立理论对象与关系，再抽取字段。
- 每个 field/factor 必须说明服务哪个 downstream activity。
- 把 evidence type、modality、context、cost 作为审计字段，而不是只记录主题分类。
- 统计观察必须通过 candidate finding 和 human adjudication 才能升级。
- roadmap/action item 只能作为后续研究安排，不能冒充已验证结论。

绝不能迁移的领域结论：

- 不能把 requirements quality 文献中 artifact-centric bias 的比例外推到 LLM/agent-based SLR。
- 不能把 passive voice、template conformance、ambiguity 等 requirements quality factor 当成本项目通用字段。
- 不能把 Fig. 4 的 57 篇样本作为本项目 survey-of-surveys 统计分母。
- 不能把 RQT tool repository 说成已被本地验证可用；本轮未核验仓库状态。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 问题 | 最小返修建议 |
|---|---|---|
| C | 当前 `review.md` 仍保留六个通用 leaf 作为“维度树结构”，容易被误读为原文树。 | 将“维度树复原”的事实源改为 publication-level RQT coding forest；六叶接口只保留在“跨论文投影”小节，并明确不属于原文叶子。 |
| C | “原文模式候选叶子映射”中的 quality construct / theory model / evaluation method / roadmap question 仍过粗，未反映 Fig. 4 的 code dimensions。 | 用本报告第 3--5 节替换：Entity explicitness、Factor explicitness/form、Activity elicitation、Impact evidence/modality、Context category、Cost/Resource 等应成为核心叶子。 |
| C | 现有 review 把本文多处标为 `not_verified`，但本轮 PDF 已核验 Fig. 2 / Fig. 4 / Fig. 5。 | 升级本地正文与 PDF 已核验的证据强度；仍把 replication package 中未打开的 complete codebook 标为 `not_verified`。 |
| I | “主统计池资格”当前表达偏绝对否定，容易掩盖原文 57 篇 survey 的局部可统计性。 | 修正为“局部可统计：原文内部 57 篇可做 descriptive statistics；本项目主统计池降级为 schema_seed / boundary_anchor”。 |
| I | 现有 review 的 roadmap tree 与 sample coding tree 混层。 | 把 roadmap streams 放入候选 finding / 方法学启发，不放入样本单位字段主树。 |
| I | A.2 / A.3 证据账本过泛，证据强度大量 `not_verified`，不能支持直接改写。 | 用本报告第 8 节草案替换，增加具体 Fig. 2、Table 1、Fig. 4、Sect. 4.2、Sect. 5.1--5.6 锚点。 |
| M | `review.md` 中 v1-deprecated 和三路审计入口文字较长，压低当前事实源可读性。 | 保留历史说明但移动到附录末尾，主文只保留 v2 结论。 |
| M | SUMMARY 表字段建议修正。 | `样本单位=57 篇 requirements quality primary studies/publications`；`样本数量/分母=57，impact 子分母 40`；`原生树类型=维度森林 / RQT-coded publication survey`；`统计池资格=局部可统计，主池降级`。 |

是否需要补 A.1--A.4：需要。A.1 已基本有；A.2/A.3 需重写为具体证据账本；A.4 应更新 PDF 核验状态为已核验关键页、未核验 replication package。

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-A2-01 | `paper_content.txt`, `paper.pdf` | Abstract / Introduction | 贡献列表 | 贡献为 theory、state evaluation、roadmap | 原文类型 | strong | 原文类型、降级边界 | 否，已核对文本 | 不等同标准 SLR/SMS |
| EV-A2-02 | `paper_content.txt`, `paper.pdf` | Sect. 3.1 | Fig. 2 | RQT concepts visualized in Fig. 2 | 理论树根 | strong | RQT 关系型概念树 | 否，已核对 PDF 第 4 页 | Fig. 2 是理论模型，不是样本统计表 |
| EV-A2-03 | `paper_content.txt`, `paper.pdf` | Sect. 3.1 | Table 1 | 11 concepts definitions | 原生字段来源 | strong | Entity、Factor、Agent、Activity、Impact、Context、Cost、Resource 等 | 否，layout 已核对 | 只给 concept definitions，不给完整 codebook |
| EV-A2-04 | `paper_content.txt`, `paper.pdf` | Sect. 4 | RQ 段落 | 问 RQT concepts 如何在文献中报告 | RQ 与样本关系 | strong | publication-level coding task | 否 | RQ 不是维度树根 |
| EV-A2-05 | `paper_content.txt`, `paper.pdf` | Sect. 4.1 | Survey objects | 57 primary studies；convenience sampling | 样本单位 / 分母 | strong | sample_unit、n=57、sampling boundary | 否 | 不是新系统检索 |
| EV-A2-06 | `paper_content.txt`, `paper.pdf` | Sect. 4.2 | Instrument design | extraction guideline；concepts → categorical variables/codes | 编码方案 | strong | 原生维度森林 | 否 | 完整 codebook 在 replication package，本轮未核验 |
| EV-A2-07 | `paper_content.txt`, `paper.pdf` | Sect. 4.2 | Validation | first author extraction；second author 6 publications；agreement metrics | 可靠性元数据 | strong | validation sample、agreement metrics | 否 | reliability 只覆盖 instrument validation 小样本 |
| EV-A2-08 | `paper_content.txt`, `paper.pdf` | Sect. 4.3 | Fig. 4 | distribution of codes among concepts | 统计表 | strong for visible codes；medium for tiny labels | Entity/Factor/Activity/Impact/Context/Cost/Resource leaves | 否，已核对 PDF 第 8 页 | 未报告的 impact dimensions 需 replication package |
| EV-A2-09 | `paper_content.txt` | Sect. 4.4 | Interpretation | artifact-centric concepts common, activity/context/economic less covered | 统计解释 | strong | 候选 finding 边界 | 否 | 是 requirements quality 领域结论 |
| EV-A2-10 | `paper_content.txt` | Sect. 4.5 | Threats | convenience sampling、implicit extraction、empirical sample limits | 外推限制 | strong | 主统计池降级 | 否 | 限制本项目迁移强度 |
| EV-A2-11 | `paper_content.txt`, `paper.pdf` | Sect. 5.1--5.6 | Roadmap headings | six research streams | roadmap action | strong | 候选方法学启发 | 否，Fig. 5 已核对 | roadmap 不是已验证效果 |
| EV-A2-12 | `metadata.json` | local metadata | eligibility fields | `eligible_for_statistical_synthesis=false` | 本地状态 | medium | 本地统计池标注 | 否 | 本地元数据不能替代原文证据 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-A3-01 | 本文是 research commentary / theory + survey evaluation + roadmap，不是标准 SLR/SMS/tertiary。 | 原文类型 | paper | EV-A2-01, EV-A2-10 | strong | boundary anchor | 仍包含一个 57 篇样本 survey，不能说“无样本” |
| C-A3-02 | 原生样本单位是 57 篇 requirements quality primary studies/publications。 | 样本单位 | survey objects | EV-A2-05 | strong | review.md 主表 | 样本来自先前 systematic study，是 convenience sample |
| C-A3-03 | 原生编码字段来自 RQT concepts，而不是六个通用 SLR leaf。 | 维度树判定 | dimension forest | EV-A2-02, EV-A2-03, EV-A2-06 | strong | 维度树复原 | 完整 codebook 未在正文完全展开 |
| C-A3-04 | 原生树类型是 RQT 理论关系树 + publication-level categorical coding forest。 | 树型 | dimension forest | EV-A2-02, EV-A2-06, EV-A2-08 | strong | SUMMARY 修正 | roadmap streams 是辅助 action forest，不是主编码树 |
| C-A3-05 | 本文可局部统计 57 篇文献的 RQT concept reporting coverage。 | 统计资格 | statistical observation | EV-A2-05, EV-A2-08 | strong | 局部统计说明 | 不进入本项目主统计池的 final synthesis |
| C-A3-06 | 本文对本项目主统计池应降级为 `schema_seed` / `boundary_anchor`。 | 迁移边界 | A1 pool | EV-A2-01, EV-A2-10, EV-A2-12 | medium-strong | SUMMARY / review.md | 本地 metadata 是辅助证据，主因仍是原文类型与 sampling |
| C-A3-07 | 当前 `review.md` 必须删除或降级六叶通用接口作为原文主树的表述。 | 返修建议 | review.md | EV-A2-03, EV-A2-06, EV-A2-08 | strong | review repair | 可保留六叶接口为跨论文投影 |
| C-A3-08 | impact evidence/modality、activity elicitation、context category、cost/resource 是本文最关键的可迁移 schema seeds。 | 方法学启发 | Paper2 schema seed | EV-A2-08, EV-A2-09, EV-A2-11 | medium | candidate heuristic | 不迁移 requirements quality 领域结论 |
| C-A3-09 | 完整取值空间不能声称已饱和，因为 replication package 未核验。 | 证据限制 | codebook | EV-A2-06, EV-A2-08 | strong | A2a task | 正文只报告部分 dimensions |
| C-A3-10 | Roadmap 六流可作为 candidate finding / action pattern，不可作为 final finding。 | finding boundary | roadmap | EV-A2-11 | strong | 候选 finding | roadmap 是作者建议，不是完成型验证结果 |

### 9. 技能使用与自我审查记录

已读取的技能文件和采用原则：

- `ai-research-writing-skill/SKILL.md`：采用 claim-evidence-engineering 原则；强结论必须有本地证据，缺证据则降级。
- `reviewer-guidelines.md`：采用 reviewer-style risk 分级，优先指出可行动的 C/I/M 问题。
- `reviewer-self-review.md`：采用 claim audit、evidence gaps、revision priorities 的审稿自检方式。
- `research-planning/SKILL.md`：采用“先读资源、识别研究问题、明确风险与 testing/evaluation plan”的结构。
- `planning-prompts.md`：采用“不可补造 unclear detail，必须显式标注 unclear”的原则。
- `output-schemas.md`：采用结构化输出、risks、assumptions、evidence mapping 的约束。
- `autoresearch/SKILL.md`：采用 artifact-gated / validation-evidence-first 原则；本任务不启动 autoresearch workflow，只借用证据闭环纪律。

本输出最高风险 3 点：

1. Fig. 4 的小字 code labels 虽已 PDF 视觉核验，但完整 code definitions 在 replication package，本轮未读。主线程合并时应下载 Zenodo package 核对 codebook。
2. Factor explicitness/form 的具体数字在 Fig. 4 中可能属于多维 code，而非单一互斥枚举。合并时不要把这些数字直接写成互斥比例，除非 codebook 确认。
3. “局部可统计”容易被误读为可进入本项目主统计池。合并时应写清：仅原文内部统计有效；本项目 A1 主统计仍降级为 schema seed / boundary anchor。

blocked / timeout / 文件缺失：

- 未出现 blocked。
- 未出现 timeout。
- 指定本地文件均可读取。
- 唯一未完成项是外部 replication package 未核验；这不是本任务文件缺失，但应作为 A2a 精核风险记录。