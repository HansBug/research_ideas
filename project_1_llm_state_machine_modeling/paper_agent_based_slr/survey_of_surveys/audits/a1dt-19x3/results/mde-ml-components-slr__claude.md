# mde-ml-components-slr · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：否；本机 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/` 路径在当前 sandbox 中未实际打开，仅按其 paper-story / reviewer-guidelines / reviewer-self-review 的精神（claim-evidence 对齐、原文复原优先、不得用通用接口冒充原文 schema）执行审计；如需正式签发须在 codex 环境内逐文件复核。
- 是否读取 `$research-planning`：否（同上，仅按其 RQ→schema→统计→finding 分层规则审计）。
- 是否读取 `$oh-my-codex:autoresearch`：否（同上，仅按其原文优先、reviewer 须给出可执行修复项的精神执行）。
- 是否完整阅读 `paper_content.txt`：是。覆盖 §1 Introduction、§2 Background、§3 Methodology（RQ、study selection、search strategy、Table 1 纳排标准、§3.4 Data extraction、§3.5 Quality assessment QA1–QA5）、§4 Results（RQ1 Goals/Tables 3–5/Fig. 6 Venn/Fig. 7 bubble、RQ2 Modeling Characteristics/ML aspects/Table 7 frameworks/Table 8 meta-tools、RQ3 Target area/Methods/Metrics/Datasets、RQ4 Limitations/Future work）、§5 Threats（internal/construct/conclusion/external）、§6 Discussion roadmap、§7 Conclusion、Appendix A P1–P46、Table 9 QA。
- 是否核对 `paper.pdf`：否；本任务为只读文本审计，没有调用 PDF 渲染工具核对 Fig. 5/6/7/8/9/10 与 Table 2–9 的具体版面，已在 §5 列为 A2a 必须回 PDF 的项目。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明
- 原文 §3.1 显式列 4 个 RQ：RQ1 motivation/goal、RQ2 MDE approaches & tools、RQ3 evaluation、RQ4 limitations & future work。
- Introduction 与 §3.4 明确：每个 RQ 直接投影成一个 data extraction section，并在 §4 各小节末尾以 “RQ Answer Summary” 收束。

### 2.2 方法流程
- §3 把流程分为 Planning / Conducting / Reporting 三段（Fig. 2）。
- 检索：7 个数据库（IEEE Xplore、ACM、Springer、Wiley、Scopus、WoS、ScienceDirect），2023-03 截止；search string 在 ScienceDirect 上拆分；Python 脚本去重。
- 筛选链条：3934 → 3570（去重）→ 72（title/abstract）→ 55（brief full-paper）→ 32（detailed）→ +14 snowballing（前向 8 + 后向 6）→ 46 primary studies。结论处有 “3,496” 与 “3,934” 的疑似笔误。
- 数据抽取：Google Form **40 题**，分为 **5 个 section**（general/publication trends → motivations/goals/domain/users → MDE approaches → evaluation → limitations/future challenges），答案形态包含 23 short answer / 10 long answer / 2 checkbox / 14 radio button；第一作者先 pilot 6 篇，与其他作者对照后再 single-extractor 抽取剩余论文。
- 质量评价：QA1–QA5，5 分制；19/46 good、15/46 average、12/46 poor；QA3–QA5 对无评价研究记 NA。Appendix B / Table 9 列出每篇 P1–P46 的 QA 得分。
- finding 形成：先在每个 RQ 末尾给 “RQ Answer Summary” 频次/百分比，再在 §6 Discussion 中升级为 10 类 research roadmap（Data for ML、Solution focus、ML type、MDE detail、Solution maturity、Domain experts/low-code、Terminology、Scalability、Responsible ML、Evaluation rigor）。

### 2.3 显式 schema / taxonomy / coding scheme / 图表
- **Fig. 5** “Features of selected primary studies” feature tree（根=MDE Solution for ML；一级=Goal / Domain / End Users / Modeling / Supported ML Aspects / Tool Support / Evaluation / Scalability / Responsible ML；Modeling 再拆 Model Representation/Model Type/Model Level/Modeling Language；Tool Support 再拆 Meta Tool/Transformations/Generated Artifacts/Automation Level）——这是本文公开的 dimension tree 真源。
- **Table 1**：inclusion/exclusion criteria。
- **Table 2**：venues with ≥2 studies。
- **Table 3**：Goals × Sub-goals × Studies（Effort Reduction[Abstraction/Automation/...]、Quality Improvement[Reusability/Extensibility/Standardization/Responsible ML/Interoperability/Maintainability/Scalability/Reliability]、Stakeholder Understanding[non-ML expert support / common language / cross-role collaboration]）。
- **Table 4**：ML techniques（supervised 31/46、reinforcement 4/46、unsupervised 0、generic 11）。
- **Table 5**：End users（ML roles / software-systems roles / domain experts / other）。
- **Table 6**：Contributions（code generator 35/46、DSL 30/46、MDE framework 21/46、model generator、text generator、modeling approach、language extension、knowledge base、data synthesizer）。
- **Table 7**：ML frameworks（TensorFlow、MXNet、Caffee、PyTorch、Infer.NET、ZenML、AI-toolbox、DL4J、TF Lite）和 ML libraries（Weka、Scikit-learn、NumPy、Keras、Encog、Neuroph、Pandas、OpenAI Gym、NetLogo for RL）。
- **Table 8**：Modeling frameworks × Meta-tools × Transformation languages（EMF/Sirius/XTend、xText/Eclipse IDE/EGL、MontiAnna/MontiArc、PyEcore/Papyrus/Acceleo、GME/WebGME/ATL、MOF/TouchCore、GreyCat、Langium、SyncMeta/ANTLR、JastAdd/Pyro、i*/MetaEdit+/Xpand、CINCO/ENLIL、OPC UA、KM3/DL LDM）。
- **Fig. 6** RQ1 Venn diagram of three goal categories；**Fig. 7** bubble chart of goal × contribution × ML aspects；**Fig. 8** MDE solution characteristics（representation / language / automation）；**Fig. 9** ML aspects × generated text languages；**Fig. 10** evaluation metrics。
- **17 种 ML aspects**：requirements engineering、data preprocessing、design and development of ML models、training、evaluation、deployment、integration、inference、monitoring、management、data generation、data storage、data visualization、documentation、ML pipeline development、ML knowledge base development 等。
- **Model level**：CIM / PIM / PSM（PIM 42/46）。**Model type**：requirements / design / data-representation / feature / process / deployment。
- **Modeling language**：DSL 34/46、GPL 9/46、language extension 3/46。
- **Model representation**：graphical 23 / textual 21 / both 2。
- **Transformations**：M2T-only 35、M2M-only 4、both 7；全部 forward engineering。
- **Generated artifacts**：ML model/training code 36、software/intermediate models 15、deployment configurations 8、datasets 4、text files 2、API code 2、recommendation/queries 2、meta-models 1；语言：Python 15、Java 10、C++ 4 等。
- **Automation level**：fully 38 / partial 8。
- **Tool availability**：open-source 17 / proprietary 6 / none 23。
- **RQ3 target area**：academia 89% / industry 9% / both 1（P35）。
- **RQ3 method**：case study 23（industrial 4）、experiment 17（industrial 1，user study 4）、criteria-based 2、no eval 8、multi-method 3。
- **ML metrics**：classification（accuracy/precision/recall/F/AUC）、regression（loss/RMSE/MAE/MRE/RAE/R²）、time-resource（execution/training/latency/inference/resource usage）、fairness（mean diff、avg odds diff）。
- **MDE metrics**：quality（productivity/usability/scalability/learnability/desirability/completeness/effectiveness/correctness/expressiveness/usefulness/complexity reduction/generated code quality/flexibility）、time-resource（generation/modeling/execution/re-training time）、code（LOC/words/characters/generated pipelines）。
- **Datasets**：33 个；MNIST 7、Iris 3。
- **RQ4 limitations**：approach（manual config / limited ML models / non-generic / fragile model）、evaluation（no user study / no industrial eval / simple scenario / no eval）、solution quality（scalability / accessibility）；19 篇 no limitation。
- **RQ4 future work**：approach enhancement、further evaluation（13 studies）、quality enhancement；7 篇 no future work。
- **Threats**：internal / construct / conclusion / external（§5.1–§5.4）。
- **Data availability**：GitHub `hiraa221/MDE4ML-SLR-Data`。
- **Appendix A**：P1–P46 完整引用；**Appendix B / Table 9**：每篇 QA1–QA5。

### 2.4 finding 形成路径
- 字段频次/比例 → RQ Answer Summary（4 个）→ §6 Discussion 10 个 roadmap 主题 → §7 Conclusion 概括。Discussion 没有引入新分类轴，但把统计观察显式升级为 “recommendation / open challenge”。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确 | 根 `[dim-...-root]` 写成 “MDE for ML components 的研究目标 / RQ / 贡献声明” 较中性；但原文的 dimension tree 真源是 Fig. 5 “MDE Solution for ML”，根名与一级分支应直接锚定 Fig. 5，而非自造五段式接口。 | I |
| 主干分支是否覆盖原文 schema | 否 | 当前 5 个主干（scope / corpus / taxonomy / method / evidence-finding）是跨论文通用接口层，没有对应 Fig. 5 一级节点（Goal/Domain/End Users/Modeling/Supported ML Aspects/Tool Support/Evaluation/Scalability/Responsible ML），也没有把 RQ4 limitations/future work、QA1–QA5、Threats、Discussion roadmap 作为独立分支。 | C |
| 叶子维度是否足够具体 | 远远不够 | 6 个 `leaf-*` 是通用接口；§“原文模式候选叶子映射” 只补 5 个 seed（ml-lifecycle / mde-artifact / solution-type / motivation-benefit / evaluation-context），但原文有 ≥18 个一阶字段（见 §2.3）和数十个二阶取值；遗漏：Model Representation、Modeling Language（DSL/GPL/ext）、Model Level（CIM/PIM/PSM）、Model Type、17 种 ML aspects、Transformation（M2T/M2M/forward）、Automation Level、Tool Availability、Generated Artifacts、ML frameworks vs libraries、Meta-tool、End Users、Application Domain、Contribution、ML Technique、Target Area（academia/industry）、Evaluation Method、ML Metrics 四类、MDE Metrics 三类、Datasets、Limitation 三类与具体 sub-class、Future Work 三类、QA1–QA5、Threats 四类、Discussion roadmap 10 主题。 | C |
| 取值空间是否可执行 | 否 | 现有 5 个 seed 的取值空间是自由文本式短语（如 “需求、数据、训练、部署…”），未给出原文显式枚举（如 “DSL/GPL/language extension”、“CIM/PIM/PSM”、“M2T-only/M2M-only/both”、“fully/partial automation”、“open-source/proprietary/none”），也未标分母 46 与统计口径。 | C |
| 关系边是否缺失 | 是 | 原文 Fig. 7 bubble chart 已经把 Goal × Contribution × ML aspect 当作三元关系；Table 8 把 Modeling framework × Meta tool × Transformation language 当作三元映射；Modeling 节点也有 Representation/Language/Level/Type 的并列关系。当前树是纯单层叶子，未表达这些关系或一对多归属（如 P35 一篇既属 PIM/PSM/CIM，亦同时属于多种 metric）。 | I |
| 统计用途 / 分母是否正确 | 不充分 | 所有 leaf 的统计用途都写 “当前 19 篇 survey-of-surveys 样本”，把本篇内部 46 篇 primary studies 的分母与跨综述外部分母混淆；原文每个字段的天然分母都是 46（或扣除 NA 后的子集，如 ML metrics 的 36），review.md 没有显式登记。 | I |
| 候选 finding 路径是否完整 | 否 | 原文真实路径 = `字段频次 → RQ Answer Summary → Discussion 10 roadmap 主题 → Conclusion`；review.md §2.10 已经文字复述了这 10 个主题，但 “维度树复原” 部分只在 `leaf-...-finding` 上挂泛话 “统计观察与候选发现”，没有把 10 个 roadmap 主题作为可枚举候选发现登记为 schema_seed，A2a 读到此树将丢失 §6 的全部线索。 | C |
| A.1–A.4 证据链是否足够 | 不足 | A.2 只有 4 条 evidence（root/taxonomy/stat/risk），全部 `not_verified` + “待 A2a 精确页码复核”，没有任何一条锚定到具体表 / 图 / 段落（如 “Fig. 5”、“Table 3 P1–P46 列表”、“§4.3.1 Modeling Characteristics”），也没把 17 个 ML aspect、5 类 metrics、3 类 limitation 等已可直接定位的字段单独立 evidence。A.3 全部 weak/schema_seed，对 A2a 而言定位价值极低。 | I |
| 是否存在可能误导 A2a 的强主张 | 存在 | §维度树复原“一句话结论”称本文“候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据”；MDE4ML 是 SLR（不是 tertiary / MLR），措辞含糊，A2a 容易误用为 tertiary anchor。另外 “historical 第 5 节迁移” 在 §5 与 §8 各保留一份旧字段树，可读性 OK 但 schema 真源不唯一时容易让 A2a 误读旧版为新事实。 | I |

## 4. 建议维度树骨架

下树以 Fig. 5 + §3.4 Google Form 5 sections 为真源，对 A2a 精核入口。叶子标识沿用 `[leaf-mde-ml-components-slr-...]` 命名。

```text
[root] MDE Solution for ML (Fig. 5; §3.4 extraction form root)
├── B1 Publication metadata
│   ├── L year (2008–2023; Fig. 4)
│   ├── L publication type (conference 20 / journal 17 / workshop 9; §4.1)
│   ├── L venue (Table 2)
│   └── L primary-study ID P1–P46 (Appendix A)
├── B2 SLR protocol & corpus
│   ├── L databases (IEEE / ACM / Springer / Wiley / Scopus / WoS / ScienceDirect)
│   ├── L search string & adaptations
│   ├── L screening counts (3934 → 3570 → 72 → 55 → 32 → +14 → 46)
│   ├── L snowballing (forward 8 / backward 6; 3 rounds)
│   ├── L inclusion / exclusion criteria (Table 1)
│   └── L extraction form shape (40 Q / 5 sections / 23 short / 10 long / 2 checkbox / 14 radio)
├── B3 RQ1 Motivation tree
│   ├── L goal {effort reduction 43, quality improvement 13, stakeholder understanding 11}
│   ├── L sub-goal {abstraction, automation, integration, monitoring, system mgmt, data mgmt, reusability, extensibility, standardization, responsible ML, interoperability, maintainability, scalability, reliability, non-ML expert support, common language}
│   ├── L ML technique {supervised 31, reinforcement 4, unsupervised 0, generic 11; deep learning is dominant supervised sub-type}
│   ├── L application domain {CPS & sub-domains, manufacturing, autonomous vehicles, analytics, generic (≈half)}
│   ├── L end users {ML roles, software/systems roles, domain experts/other}
│   └── L contribution {code generator 35, DSL 30, MDE framework 21, model generator, text generator, modeling approach, language extension, knowledge base, data synthesizer}
├── B4 RQ2 MDE Solution tree (= Fig. 5 Modeling + Tool Support)
│   ├── L model representation {graphical 23, textual 21, both 2}
│   ├── L modeling language {new DSL 34, GPL 9, language extension 3}
│   ├── L model level {CIM, PIM 42, PSM}
│   ├── L model type {requirements 6, design 39, data 5, feature, process, deployment}
│   ├── L supported ML aspects (17 enumerated; design/dev 28, training 22, deployment 10, documentation 1, data storage 1, visualization 1, monitoring 2, data generation 2, ...)
│   ├── L ML framework (TensorFlow / MXNet / ...; Table 7)
│   ├── L ML library (Weka / Scikit-learn / NumPy / ...; Table 7)
│   ├── L transformation {M2T-only 35, M2M-only 4, both 7; forward 46/46}
│   ├── L generated artifact {ML/training code 36, software/intermediate models 15, deployment configs 8, datasets 4, text 2, API 2, recommendations 2, meta-models 1}
│   ├── L generation language {Python 15, Java 10, C++ 4, ...}
│   ├── L automation level {fully 38, partial 8}
│   ├── L tool availability {open-source 17, proprietary 6, none 23}
│   └── L meta-tool / modeling framework / transformation language (Table 8 三元映射)
├── B5 RQ3 Evaluation tree
│   ├── L target area {academia 89%, industry 9%, both (P35)}
│   ├── L evaluation method {case study 23 (industrial 4), experiment 17 (industrial 1, user study 4), criteria-based 2, no eval 8, multi-method 3}
│   ├── L ML metrics {classification (accuracy, precision, recall, F, AUC), regression (loss, RMSE, MAE, MRE, RAE, R²), time-resource (execution, training, latency, inference, resource usage), fairness (mean diff, avg odds diff), not mentioned 10, N/A 10}
│   ├── L MDE metrics {quality (productivity, usability, scalability, learnability, desirability, completeness, effectiveness, correctness, expressiveness, usefulness, complexity reduction, generated-code quality, flexibility), time-resource (generation, modeling, execution, re-training time reduction), code (LOC, words, characters, generated pipelines), not mentioned 18, N/A 8}
│   └── L datasets {33 total; MNIST 7, Iris 3, others}
├── B6 RQ4 Limitations & Future-work tree
│   ├── L limitation: approach (manual config, limited ML models, non-generic, fragile model)
│   ├── L limitation: evaluation (no user study, no industrial eval, simple scenario, no eval)
│   ├── L limitation: solution quality (scalability, accessibility)
│   ├── L no limitation reported (19/46)
│   ├── L future work: approach enhancement (46%)
│   ├── L future work: further evaluation (13/46 ≈28%)
│   ├── L future work: quality enhancement (integration / interoperability / optimization / model checking / scalability / reusability / adaptability)
│   └── L no future work reported (7/46)
├── B7 Quality assessment
│   ├── L QA1–QA5 5-point scale
│   ├── L NA rule for QA3–QA5 when no evaluation
│   └── L outcome distribution {good 19, average 15, poor 12}
├── B8 Threats to validity
│   ├── L internal (protocol review, search-string iteration, multi-round screening, pilot)
│   ├── L construct (7 DBs, automated+manual, terminology disagreement → discussion)
│   ├── L conclusion (extraction form aligned with RQs, pilot close-match)
│   └── L external (snowballing, peer-reviewed only, English only, no time range, no QA exclusion)
├── B9 Discussion roadmap (10 themes; finding-path)
│   ├── L Data for ML (first-class citizen)
│   ├── L Solution focus (RE / integration / pipeline / deployment / monitoring / documentation gaps)
│   ├── L ML type (supervised/deep dominant; unsupervised/RL gap)
│   ├── L MDE detail (元模型/转换细节不足)
│   ├── L Solution maturity (tool / end-to-end lifecycle)
│   ├── L Domain experts / low-code
│   ├── L Terminology (ML algo/technique 粒度不一致)
│   ├── L Scalability (~75% 未讨论)
│   ├── L Responsible ML (9/46)
│   └── L Evaluation rigor (industrial / user study / MDE+ML 双覆盖)
└── B10 Data availability & replication
    └── L GitHub repo URL（hiraa221/MDE4ML-SLR-Data；需 A2a 访问性核验）
```

每个 leaf 的统计用途默认分母 = 46（或 NA 扣除后的子集），缺失值语义分 “原文未报告 / NA / 不适用”；证据来源应锚定到具体 Fig./Table/§ 编号。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 把根名与一级分支锚定到 Fig. 5 | 维度树复原 §“维度树结构” | 把根写为 “MDE Solution for ML (Fig. 5)”；以 §4 节标题与 §3.4 Form 5 sections + Fig. 5 一级节点为主干分支（B1–B10 如上） | paper_content.txt §4.1、§4.2–§4.5、Fig. 5 | C |
| 把 §“原文模式候选叶子映射” 从 5 条扩充到至少覆盖 §2.3 列举的全部一阶字段 | review.md §“原文模式候选叶子映射（A1 种子）” | 至少补充：model-representation / modeling-language / model-level / model-type / ml-aspect(17 enumerated) / ml-framework / ml-library / transformation-type / generation-language / automation-level / tool-availability / meta-tool-triple / goal(3+sub) / ml-technique / application-domain / end-user / contribution / target-area / evaluation-method / ml-metrics(4 sub) / mde-metrics(3 sub) / dataset / limitation(3 sub) / future-work(3 sub) / QA1–QA5 / threats(4 sub) / discussion-roadmap(10 themes) / data-availability | paper_content.txt §3.4–§6、Tables 3–8、Fig. 5–10 | C |
| 给每个候选叶子写显式取值空间与分母 46 | 同上 | 列出原文显式枚举（如 DSL/GPL/extension、CIM/PIM/PSM、M2T-only/M2M-only/both、academia/industry/both 等）并在 “统计用途” 处写 “分母=46，NA 子集见原文 §4.4.3” | paper_content.txt §4.3、§4.4、§4.5 | C |
| 把 Discussion 10 个 roadmap 主题登记为候选 finding | 新增 B9 分支或在 leaf-finding 下展开 | 每个 roadmap 主题挂一个候选 finding 节点，标 `schema_seed`，引用 §6 对应小节段落 | paper_content.txt §6 Discussion | C |
| 增补 Threats / QA / Data availability 分支 | 维度树复原 §“维度树结构” | 新增 B7 / B8 / B10 分支并写明可执行字段（QA 分布、4 类 threats、GitHub repo URL） | §3.5、§5、§Data availability、Table 9 | I |
| 修正 A.2 evidence 锚点 | §A.2 维度树证据账本 | 把 EV-...-002 / 003 拆为多条，分别锚定到 Fig. 5 / Table 3 / Table 4 / Table 8 / Fig. 8–10 / §4.4.3 / §4.5 / Table 9 / §6 等具体位置；保留 `not_verified` 但写出可定位的章节号 | paper_content.txt 全文 | I |
| 修正 “主统计池资格” 措辞 | §“一句话结论” | 删除 “tertiary / MLR”，明确写本文是 SLR（systematic literature review），不要让 A2a 误用 tertiary anchor | §Abstract、§3 Methodology | I |
| 修正分母混淆 | §“统计与候选发现链路” | 把 “分母=当前 19 篇 survey-of-surveys 样本” 改为 “本篇内部 46 篇 primary studies；19-篇分母仅适用于跨综述聚合统计” | paper_content.txt §3.3 final count | I |
| 标注 3934 vs 3496 数量笔误 | §“待复核” 或 A.2 | 在 A.2 备注里写明 §Conclusion “3,496” 与 §Abstract/§3 “3,934” 不一致，A2a 引用须以方法节链条为准 | §3.3、§7 Conclusion | M |
| 给历史草稿 §5 / §8 加 “归档不再维护” 标注 | review.md §5/§8 历史草稿块 | 已有 “不作事实真源” 提示，但建议进一步把第 5 节 fenced tree 标 “与本节维度树重复，仅供回溯” | review.md 现状 | M |

## 6. C/I/M 结论

- **C（4）**：
  1. 主干分支偏离原文 schema（用 5 个通用接口替代 Fig. 5 + 4 个 RQ 子树）。
  2. 叶子层覆盖严重不足，遗漏 ≥80% 原文显式字段与取值。
  3. 取值空间与分母未显式登记，A2a 无法直接据此精核。
  4. Discussion 10 个 roadmap 主题未进入候选 finding 路径，丢失原文最有价值的 finding 形成链。
- **I（4）**：
  1. 根名/关系/Threats/QA/Data availability 分支缺失。
  2. 证据账本锚点过于泛化，不可定位。
  3. “tertiary / MLR” 措辞可能误导 A2a。
  4. 统计分母混淆（46 vs 19）。
- **M（2）**：3934/3496 笔误未标注；历史草稿区与新树并存的归档措辞可再加强。

对 Paper2 学术目标的影响：当前维度树若直接进入 A2a，会让该样本被当成 “通用接口模板” 而不是 “MDE4ML schema 真源”，导致 A2a 在做 cross-survey schema 综合时遗失 MDE4ML 特有的 17 种 ML aspect / CIM-PIM-PSM / M2T-M2M / Tool availability / Roadmap 10 主题等高价值模式先验，进而影响 Paper2 “综述之综述维度模式库” 的覆盖度与可统计性，并可能让 A2a 把 “候选发现路径” 误读为 “统计观察 → 通用接口 leaf-finding”，跳过 Discussion roadmap，造成 finding ledger 在 MDE 子领域上的系统性遗漏。

- **最终建议**：**NEEDS FIX**。需先完成 §5 列出的 4 项 C 级修复，并补齐 I 级证据锚点，再进入 A2a。

写入路径：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-19x3/results/mde-ml-components-slr__claude.md`。
