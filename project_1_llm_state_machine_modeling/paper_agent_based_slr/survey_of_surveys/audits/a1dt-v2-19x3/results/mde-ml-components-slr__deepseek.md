Now I have all the evidence I need. Let me produce the complete audit report.

---

# A1-DT v2 单篇全文审计报告：`mde-ml-components-slr`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `mde-ml-components-slr` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是，逐行通读全部 2123 行（§1–§7、Appendix B、References），覆盖 Introduction、Background、Method、4 个 RQ 结果、Discussion、Threats to Validity、Conclusion |
| 是否读取 `bibtex.bib` / `metadata.json` | 是，分别读取并核验作者、标题、年份、DOI、期刊与 metadata 口径一致性 |
| 是否打开或核对 `paper.pdf` | 否（未做 PDF 版面核验）；table/figure 编号与统计值的精确锚定基于 `paper_content.txt` text 提取结果；Fig. 5（feature tree）、Fig. 8、Fig. 9、Fig. 10、Table 3–9 的具体视觉结构和数字需要后续 PDF 二次核对 |
| 原文类型 | SLR（Systematic Literature Review），遵循 Kitchenham guidelines |
| 被编码样本单位 | 46 篇 primary study（P1–P46），来自系统数据库检索（32 篇）+ 前向/后向 snowballing（14 篇） |
| 样本数量 / 分母 | 初始 3934 → 去重 3570 → 三轮筛选得 32 → snowballing 增补 14 → **最终 46** |
| 原生树类型 | **维度森林**（多子树）：一棵以 Google Form 40 题 5 section 为抽取根的特征树（Fig. 5）+ 四棵 RQ 回答子树，彼此之间存在显式交叉引用与统计关系 |
| 主统计池资格 | **是**：具备系统检索、纳排 protocol、data extraction form、显式编码方案、pilot test、名义 quality assessment、及每 RQ 的显式统计报告。46 篇 primary study 可进入 A2a 精核后的主统计池 |
| 总体判定 | **needs repair**：现有 `review.md` 在承认"六个 leaf-* 是跨论文通用接口"的同时仍以其为主维度树，原生树被降级为"候选叶子映射"置于旁路；需要将原生 Google Form / feature tree 提升为主树，六叶接口降级为跨论文投影标注 |

---

## 1. 原文证据阅读说明

### 已读取文件

| 文件 | 行数/大小 | 读取方式 |
|---|---|---|
| `paper_content.txt` | 2123 行 | 分段（0–500, 501–1000, 1001–1500, 1501–2123）全文阅读 |
| `bibtex.bib` | 1 entry | 全文 |
| `metadata.json` | 完整 JSON | 全文 |
| `review.md` | 477 行 | 全文（含 A.1–A.4 审计附录） |

### 是否需要 PDF 视觉核验

当前证据全部基于 `paper_content.txt` text 提取。以下项目需要 PDF 版面核验：

- **Fig. 5（feature tree）**：论文的核心编码框架图，text 中以文字提及但未完整展开树形结构。图中哪些节点是叶子、哪些是分组节点、是否存在不体现在行文中的细粒度分类——均需 PDF 核验。
- **Fig. 6（Venn diagram of RQ1）**：motivations 三大类的交集区域大小需要 PDF 视觉确认。
- **Fig. 8（RQ2 各维度的条形图/饼图）**：model representation type、model level、automation level 的精确计数。
- **Fig. 9（ML aspects + generated languages）**：ML aspects 的精确频次柱状图、languages 分布。
- **Fig. 10（evaluation metrics）**：ML metrics 与 MDE metrics 的频次分布。
- **Table 3–9**：text 提取中大部分 table 的内容已可读，但部分 table 的 cell 对齐、多行合并、footnote 需要 PDF 确认。
- **Appendix A（46 篇 primary study 完整引用列表）**：需确认是否全部 46 条均在 text 中正确提取。

### 关键原文证据锚点（12 个）

| 锚点编号 | 章节/段落线索 | 短引或释义 |
|---|---|---|
| EA-01 | §3.3 | 检索 7 个数据库 → 3934 papers → 去重 3570 → 三轮筛选 → 32 selected + snowballing(+14) → **46 final** |
| EA-02 | §3.4 | "Google Form with 40 questions corresponding to our four RQs… divided into five sections: general information… motivations… MDE approaches… evaluation… limitation" |
| EA-03 | §3.4 | 数据抽取由第一作者执行，pilot test 对比 6 篇 dual-extraction，"close match" 后第一作者抽取其余 |
| EA-04 | §3.5 | QA 五点评分：QA1 aims clear / QA2 solution clear / QA3 measures clear / QA4 implications for practice / QA5 adds to literature；结果 19/46 good, 15/46 average, 12/46 poor，未排除任何论文 |
| EA-05 | §4.1 | "Fig. 5 shows a feature tree of the examined features… derived from the data extraction categories based on the RQs" |
| EA-06 | §4.2.1 | RQ1 motivations 三大类：effort reduction (43/46)、quality improvement (13/46)、increased stakeholder understanding (not counted exactly) |
| EA-07 | §4.3.1 | RQ2 model representation：graphical (18 studies)、textual (17)、both (11)；modeling language：DSL 最多 (General Purpose DSL 22、ML DSL 12) |
| EA-08 | §4.3.2 | 17 ML aspects：design & development 最频繁 (28/46)、training (22/46)、deployment (10/46)；monitoring 仅 2 篇、documentation 仅 1 篇 |
| EA-09 | §4.3.3 | transformations：M2T only 35/46、M2M only 4/46、both 7/46；automation：fully 38/46、partially 8/46；tool availability：open-source 17、proprietary 6、no tool 23 |
| EA-10 | §4.4.2 | evaluation methods：none 8 篇、case study 16、experiment 11、survey 4、criteria-based assessment 3、demonstration 3、running example 1 |
| EA-11 | §5.1 | Limitations 三类：approach（limited scope/generalizability/scalability/learning curve/manual steps）、evaluation、solution quality |
| EA-12 | §6 | Discussion 提出 7 个 recommendation theme：broaden ML lifecycle coverage、unsupervised+RL coverage、MDE detail in ML venues、solution maturity、domain expert tools、ML terminology consensus、scalability |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

46 篇 **primary study**（P1–P46），即对 ML component 应用了至少一种 MDE technique 的原创研究论文。每篇 primary study 都是独立的设计/实现/评价单元，被 data extraction form 逐项编码为 40 个字段。

作者在 §3.4 明确声明："We created a Google Form with 40 questions corresponding to our four RQs to ensure all required data was extracted from the papers."

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**四项全部具备**：

1. **系统检索**：7 个数据库（ACM DL、IEEE Xplore、Scopus、Web of Science、Springer、ScienceDirect、Google Scholar），明确 search string（ML 关键词 × MDE 关键词 AND 组合，详见 §3.3.2 中完整 search string），检索时间 2023 年 3 月。
2. **纳排**：11 条 inclusion/exclusion criteria（Table 1），三轮筛选（title/abstract → full skim → data extraction 时终筛），Google Sheets 颜色标注跟踪。
3. **数据抽取**：Google Form 40 题、5 section，23 短答 + 10 长答 + 2 checkbox + 14 radio button。
4. **编码方案**：pilot test（6 篇 first-author vs. other-authors dual-extraction, "close match"）；first author 完成全量抽取 + synthesis；其他作者提供 guidance。

### 2.3 原文字段来自哪里？

| 来源 | 具体形式 | 覆盖 RQ |
|---|---|---|
| Google Form 40 questions | 5 sections：general info / motivations / MDE approaches / evaluation / limitations | RQ1–4 全部 |
| Fig. 5 feature tree | 数据抽取 category 的可视化组织 | 跨 RQ 的元框架 |
| Quality assessment rubric | 五点 Likert scale (1–5) 针对 QA1–QA5 | 独立于 RQ 的 meta-quality 维度 |
| 各 RQ Answer Summary | 每个 RQ 末尾的叙述性汇总 | RQ1–4 结果合成 |

### 2.4 RQ 与样本单位是什么关系？

RQ 是**字段的分组组织者**和**结果叙述的章节框架**，不是树根。真正的树根是 Fig. 5 的 feature tree（从 data extraction categories 推导），RQ 是 feature tree 下面的四个主干分支。

具体关系：

- RQ1 → motivations / goals / ML techniques / domains / users / contributions 字段子集
- RQ2 → model representation / modeling language / model level / ML aspects / frameworks / transformations / artifacts / automation / tools 字段子集
- RQ3 → evaluation context / methods / ML metrics / MDE metrics / datasets 字段子集
- RQ4 → limitations / future work 字段子集

这形成了一个"**feature tree 根 → RQ 主干 → 字段分支 → 分类项取值叶子**"的维度森林，而非单棵扁平树。

### 2.5 无系统样本库情况下的降级

**不适用降级**：本文有系统样本库（46 primary study），降级规则不适用。

---

## 3. 原生样本编码维度树 / 维度森林

以下是本文自身的数据抽取编码 schema，以 Fig. 5 feature tree 为根，Google Form 5 section + 4 RQ 为组织框架。这不是跨论文投影的通用六叶接口，而是 **Naveed et al. (2024) 实际用来编码 46 primary study 的原生字段体系**。

由于 Fig. 5 的完整图形结构需要 PDF 核验，以下基于 paper_content.txt 全文证据复原。标注 `[PDF核验]` 的节点表示需要 PDF 视觉确认的图形层级关系。

### 3.1 维森林总根

```
[1_root] MDE4ML Feature Tree (Fig. 5)
│   来源：§4.1 "Fig. 5 shows a feature tree of the examined features of the primary studies.
│   The features in the tree were derived from the data extraction categories based on the RQs"
│   取值空间类型：(树根，不直接取值)
```

### 3.2 RQ1 子树：动机与上下文（Motivations & Context）

```
[1_root] MDE4ML Feature Tree
├── [2_rq1] RQ1: Motivation & Context (§4.2)
│   ├── [3_rq1_goal] Motivation/Goal (§4.2.1, Table 3)
│   │   ├── [4_rq1_goal_effort] Effort Reduction (43/46 studies)
│   │   │   ├── [5_leaf] Abstraction [层级枚举]
│   │   │   ├── [6_leaf] Automation [层级枚举]
│   │   │   ├── [7_leaf] Integration [层级枚举]
│   │   │   ├── [8_leaf] Monitoring [层级枚举]
│   │   │   ├── [9_leaf] System Management [层级枚举]
│   │   │   └── [10_leaf] Data Management [层级枚举]
│   │   ├── [11_rq1_goal_quality] Quality Improvement (13/46 studies)
│   │   │   ├── [12_leaf] Reusability [层级枚举]
│   │   │   ├── [13_leaf] Extensibility [层级枚举]
│   │   │   ├── [14_leaf] Standardization [层级枚举]
│   │   │   ├── [15_leaf] Responsible ML [层级枚举]
│   │   │   ├── [16_leaf] Interoperability [层级枚举]
│   │   │   ├── [17_leaf] Maintainability [层级枚举]
│   │   │   ├── [18_leaf] Scalability [层级枚举]
│   │   │   └── [19_leaf] Reliability [层级枚举]
│   │   └── [20_rq1_goal_stakeholder] Increased Stakeholder Understanding
│   │       ├── [21_leaf] Support non-ML Experts [层级枚举]
│   │       └── [22_leaf] Common Language [层级枚举]
│   ├── [23_rq1_ml_technique] ML Technique Type (§4.2.2, Table 4)
│   │   ├── [24_leaf] Supervised Learning [层级枚举/外部分类法引用]
│   │   │   ├── (子类) Traditional Supervised Learning [层级枚举]
│   │   │   └── (子类) Ensemble Learning [层级枚举]
│   │   ├── [25_leaf] Deep Learning [层级枚举]
│   │   ├── [26_leaf] Reinforcement Learning [层级枚举]
│   │   ├── [27_leaf] Unsupervised Learning [层级枚举]
│   │   ├── [28_leaf] Semi-supervised Learning [层级枚举]
│   │   └── [29_leaf] Not Specified [层级枚举，含缺失值语义]
│   ├── [30_rq1_domain] Application Domain (§4.2.2, Table 5)
│   │   └── [31_leaf] Domain Name [完整枚举：healthcare, finance, transport, entertainment,
│   │        robotics, smart home/IoT, agriculture, energy, manufacturing, smart city,
│   │        education, telecom, etc. — 共 21 domains，需 PDF 核验完整列表]
│   ├── [32_rq1_users] End Users (§4.2.2, Table 5)
│   │   ├── [33_leaf] ML-related Roles [层级枚举：ML engineer, data analyst/engineer/scientist]
│   │   ├── [34_leaf] Software & Systems Roles [层级枚举：software engineer, system designer/architect,
│   │   │   researcher, product manager, student, system operator]
│   │   └── [35_leaf] Other Roles [层级枚举：domain expert]
│   └── [36_rq1_contribution] Contribution Type (§4.2.3, Table 6)
│       ├── [37_leaf] Tool/DSL [完整枚举/外部分类法引用]
│       ├── [38_leaf] Process/Methodology [完整枚举]
│       ├── [39_leaf] Framework/Architecture [完整枚举]
│       └── [40_leaf] Model/Profile [完整枚举]
```

### 3.3 RQ2 子树：MDE 方案与工具（MDE Approaches & Tools）

```
[1_root]
├── [2_rq2] RQ2: MDE Approaches & Tools (§4.3)
│   ├── [41_rq2_model_rep] Model Representation Type (§4.3.1, Fig. 8(a))
│   │   ├── [42_leaf] Graphical [层级枚举：18 studies]
│   │   ├── [43_leaf] Textual [层级枚举：17 studies]
│   │   └── [44_leaf] Both [层级枚举：11 studies]
│   ├── [45_rq2_model_lang] Modeling Language Type (§4.3.1, Fig. 8(b))
│   │   ├── [46_leaf] DSL [层级枚举]
│   │   │   ├── (子类) General Purpose DSL [层级枚举：22 studies]
│   │   │   └── (子类) ML DSL [层级枚举：12 studies]
│   │   ├── [47_leaf] UML/MARTE/SysML [层级枚举]
│   │   │   ├── (子类) UML Profile [层级枚举]
│   │   │   ├── (子类) UML [层级枚举]
│   │   │   └── (子类) SysML [层级枚举]
│   │   ├── [48_leaf] Goal Models [层级枚举]
│   │   ├── [49_leaf] Feature Models [层级枚举]
│   │   ├── [50_leaf] Data-flow Models [层级枚举]
│   │   ├── [51_leaf] Ontology [层级枚举]
│   │   └── [52_leaf] Metamodel [层级枚举]
│   ├── [53_rq2_model_level] Model Level/Type (§4.3.1)
│   │   ├── [54_leaf] CIM (Computation Independent Model) [层级枚举]
│   │   ├── [55_leaf] PIM (Platform Independent Model) [层级枚举：≥43/46 studies "propose models at PIM level"]
│   │   ├── [56_leaf] PSM (Platform Specific Model) [层级枚举]
│   │   ├── [57_leaf] CIM+PIM [层级枚举]
│   │   └── [58_leaf] PIM+PSM [层级枚举]
│   ├── [59_rq2_ml_aspect] ML Aspect (§4.3.2, Fig. 9(a))
│   │   ├── [60_leaf] Requirements Engineering [层级枚举]
│   │   ├── [61_leaf] Data Preprocessing [层级枚举]
│   │   ├── [62_leaf] Design & Development [层级枚举：28/46, 最高频]
│   │   ├── [63_leaf] Training [层级枚举：22/46]
│   │   ├── [64_leaf] Evaluation [层级枚举]
│   │   ├── [65_leaf] Deployment [层级枚举：10/46]
│   │   ├── [66_leaf] Integration [层级枚举]
│   │   ├── [67_leaf] Inference [层级枚举]
│   │   ├── [68_leaf] Monitoring [层级枚举：2 studies]
│   │   ├── [69_leaf] Management [层级枚举]
│   │   ├── [70_leaf] Data Generation [层级枚举]
│   │   ├── [71_leaf] Data Storage [层级枚举：1 study]
│   │   ├── [72_leaf] Data Visualization [层级枚举：1 study]
│   │   ├── [73_leaf] Documentation [层级枚举：1 study]
│   │   ├── [74_leaf] ML Pipeline Development [层级枚举]
│   │   └── [75_leaf] ML Knowledge Base Development [层级枚举]
│   ├── [76_rq2_ml_framework] ML Framework (§4.3.2, Table 7)
│   │   └── [77_leaf] Framework Name [完整枚举：TensorFlow, MXNet, Caffee, PyTorch,
│   │        TensorFlow Lite, ZenML, DL4J, Infer.NET, AI-toolbox]
│   ├── [78_rq2_ml_library] ML Library (§4.3.2, Table 7)
│   │   └── [79_leaf] Library Name [完整枚举：Weka, Scikit-learn, NumPy, Keras, Pandas,
│   │        Encog, NetLogo for RL, Neuroph, OpenAI Gym]
│   ├── [80_rq2_transformation] Transformation Type (§4.3.3)
│   │   ├── [81_leaf] M2T only [层级枚举：35/46]
│   │   ├── [82_leaf] M2M only [层级枚举：4/46]
│   │   └── [83_leaf] Both M2M+M2T [层级枚举：7/46]
│   ├── [84_rq2_engineering_dir] Engineering Direction (§4.3.3)
│   │   └── [85_leaf] Forward Engineering only [布尔：all 46]
│   ├── [86_rq2_generated_artifact] Generated Artifact Type (§4.3.3)
│   │   ├── [87_leaf] ML Model Code / Training Code [层级枚举：36/46]
│   │   ├── [88_leaf] Software/Intermediate Models [层级枚举：15/46]
│   │   ├── [89_leaf] Deployment Configurations [层级枚举：8/46]
│   │   ├── [90_leaf] Datasets/Subsets [层级枚举：4/46]
│   │   ├── [91_leaf] Text Files [层级枚举：2/46]
│   │   ├── [92_leaf] API Code [层级枚举：2/46]
│   │   ├── [93_leaf] Recommendation Rules/Queries [层级枚举：2/46]
│   │   └── [94_leaf] Meta-models [层级枚举：1/46]
│   ├── [95_rq2_generated_lang] Generated Language (§4.3.3, Fig. 9(b))
│   │   └── [96_leaf] Language [完整枚举：Python (15/46), Java (10/46), C++ (4/46),
│   │        R, Lua, TensorFlow-specific, JavaScript, Scikit-learn-specific]
│   ├── [97_rq2_automation] Automation Level (§4.3.3, Fig. 8(c))
│   │   ├── [98_leaf] Fully Automated [层级枚举：38/46]
│   │   └── [99_leaf] Partially Automated [层级枚举：8/46]
│   ├── [100_rq2_tool_avail] Tool Availability (§4.3.3)
│   │   ├── [101_leaf] Open-source [层级枚举：17/46]
│   │   ├── [102_leaf] Proprietary [层级枚举：6/46]
│   │   └── [103_leaf] No Tool Mentioned [层级枚举：23/46，含缺失值语义]
│   └── [104_rq2_meta] Meta Tools & Frameworks (§4.3.3, Table 8)
│       ├── [105_leaf] Modeling Framework [完整枚举：EMF (15), MontiAnna/MontiArc (4), ...]
│       ├── [106_leaf] Meta Tool [完整枚举：Sirius (10), MontiAnna/MontiArc (4), Eclipse IDE (4), ...]
│       └── [107_leaf] Transformation Language [完整枚举：XTend (5), EGL (4), ...]
```

### 3.4 RQ3 子树：评价（Evaluation）

```
[1_root]
├── [2_rq3] RQ3: Evaluation (§4.4)
│   ├── [108_rq3_context] Evaluation Context (§4.4.1)
│   │   ├── [109_leaf] Academia [层级枚举：41/46, 89%]
│   │   └── [110_leaf] Industry [层级枚举：5/46]
│   ├── [111_rq3_method] Evaluation Method (§4.4.2)
│   │   ├── [112_leaf] No Evaluation [层级枚举：8/46]
│   │   ├── [113_leaf] Case Study [层级枚举：16/46]
│   │   ├── [114_leaf] Experiment [层级枚举：11/46]
│   │   ├── [115_leaf] Survey [层级枚举：4/46]
│   │   ├── [116_leaf] Criteria-based Assessment [层级枚举：3/46]
│   │   ├── [117_leaf] Demonstration [层级枚举：3/46]
│   │   └── [118_leaf] Running Example [层级枚举：1/46]
│   ├── [119_rq3_ml_metric] ML Metric (§4.4.2, Fig. 10(a))
│   │   ├── [120_leaf] Classification Metrics [层级枚举：accuracy, precision, recall,
│   │   │   F1-score, AUC-ROC (各可独立统计)]
│   │   ├── [121_leaf] Regression Metrics [层级枚举：R², RMSE/MAE]
│   │   ├── [122_leaf] Time & Resource Metrics [层级枚举：execution time, training time,
│   │   │   model size, coverage]
│   │   └── [123_leaf] Fairness Metrics [层级枚举]
│   ├── [124_rq3_mde_metric] MDE Metric (§4.4.2, Fig. 10(b))
│   │   ├── [125_leaf] Correctness [层级枚举]
│   │   ├── [126_leaf] Effort Reduction [层级枚举]
│   │   ├── [127_leaf] Code Reduction [层级枚举]
│   │   ├── [128_leaf] Transformation Time [层级枚举]
│   │   ├── [129_leaf] Model Quality [层级枚举]
│   │   └── [130_leaf] Code Metrics [层级枚举]
│   └── [131_rq3_dataset] Dataset (§4.4.2)
│       └── [132_leaf] Dataset Name & Size [自由文本加理由：原文提及 Iris, MNIST 等常用数据集，
│            但未做系统性的 dataset taxonomy]
│   └── [133_rq3_qa] Quality Assessment (§3.5, Appendix B)
│       ├── [134_leaf] QA1: Aims Clear [数值或区间：Likert 1–5]
│       ├── [135_leaf] QA2: Solution Clear [数值或区间：Likert 1–5]
│       ├── [136_leaf] QA3: Measures Clear [数值或区间：Likert 1–5 or N/A]
│       ├── [137_leaf] QA4: Practice Implications [数值或区间：Likert 1–5 or N/A]
│       └── [138_leaf] QA5: Adds to Literature [数值或区间：Likert 1–5 or N/A]
```

### 3.5 RQ4 子树：局限与未来工作（Limitations & Future Work）

```
[1_root]
├── [2_rq4] RQ4: Limitations & Future Work (§5)
│   ├── [139_rq4_limitation] Limitation Category (§5.1)
│   │   ├── [140_leaf] Approach Limitations [层级枚举]
│   │   │   ├── (子类) Limited Scope [层级枚举]
│   │   │   ├── (子类) Limited Generalizability [层级枚举]
│   │   │   ├── (子类) Limited Scalability [层级枚举]
│   │   │   ├── (子类) Steep Learning Curve [层级枚举]
│   │   │   └── (子类) Manual Steps Required [层级枚举]
│   │   ├── [141_leaf] Evaluation Limitations [层级枚举]
│   │   │   ├── (子类) Simple Evaluation [层级枚举]
│   │   │   ├── (子类) Limited Results [层级枚举]
│   │   │   ├── (子类) No User Evaluation [层级枚举]
│   │   │   └── (子类) Lacking MDE Metrics [层级枚举]
│   │   └── [142_leaf] Solution Quality Limitations [层级枚举]
│   │       ├── (子类) Faulty Design [层级枚举]
│   │       └── (子类) Limited Integration [层级枚举]
│   └── [143_rq4_future] Future Work Category (§5.2)
│       ├── [144_leaf] Approach Enhancement [层级枚举]
│       ├── [145_leaf] Further Evaluation [层级枚举]
│       └── [146_leaf] Quality Enhancement [层级枚举]
```

### 3.6 独立于 RQ 的元维度（Meta-dimensions）

```
[1_root]
├── [147_meta_pub] Publication Metadata (§4.1, Table 2)
│   ├── [148_leaf] Year [数值或区间：2008–2023]
│   ├── [149_leaf] Venue Type [层级枚举：Conference/Journal/Workshop]
│   ├── [150_leaf] Venue Name [自由文本]
│   └── [151_leaf] Citation Count [数值]
└── [152_meta_discussion] Discussion Recommendations (§6)
    ├── [153_leaf] Recommendation Theme [完整枚举：7 themes — broaden ML lifecycle,
    │    unsupervised+RL, MDE detail in ML venues, solution maturity, domain expert tools,
    │    ML terminology consensus, scalability]
    └── [154_leaf] Recommendation Strength [自由文本加理由：来自 discussion，非来自
         primary study 编码]
```

### 3.7 缺失部分与 A2a 精核任务

当前复原基于 text extraction，以下待 A2a 在 PDF 精核中补全：

1. **Fig. 5 的全部节点和层级关系**：text 无法还原图的完整树形，一部分分支可能只存于图中。
2. **Table 3–9 的完整数据**：部分 table 的跨行合并、子类别、footnote 在 text 中可能有损。
3. **各叶子的精确频次/百分比**：部分统计值只在图中表示为 bar，text 未给出精确数字。
4. **21 application domains 的完整枚举**。
5. **Contribution type 的完整子类别枚举**（Table 6 结构复杂）。
6. **Appendix A 的 46 篇 primary study 完整元数据**。
7. **Appendix B 的 QA 评分逐篇明细**。

---

## 4. 叶子维度表

（限于篇幅，列出核心代表性叶子；完整表应在 A2a 中补全至所有约 154 个节点和叶子。）

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `[5_leaf]` Abstraction | 抽象化动机 | `[4_rq1_goal_effort]` Effort Reduction | Google Form §2 "motivations" section → Table 3 | 用模型隐藏不必要细节以降低复杂度 | {present, absent} / 46 | 层级枚举 | 未列为 goal 则 absent | 频次统计（43/46 属 effort reduction 大类的精确子计数需 Table 3 复核） | 识别 abstraction 作为 MDE4ML 最普遍动机是否可泛化 | EA-06 + Table 3 | 不可迁移到非 MDE 领域 |
| `[24_leaf]` Supervised Learning | 监督学习 | `[23_rq1_ml_technique]` ML Technique Type | Google Form §2 → Table 4 | 被 primary study 使用或支持的有标签学习类型 | {present, absent} + subclass (traditional/ensemble) / 46 | 层级枚举 | 未提及即未覆盖；另有 `[29_leaf]` Not Specified | 各类 ML 技术的被覆盖比例 | "supervised + deep learning dominant, unsupervised 未被 sole focus" | EA-12 + Table 4 | 技术覆盖图不可外推到本仓库目标领域 |
| `[31_leaf]` Domain Name | 应用领域 | `[30_rq1_domain]` Application Domain | Google Form §2 → Table 5 | primary study 中示例或评价的目标应用领域 | {healthcare, finance, transport, entertainment, robotics, smart home/IoT, agriculture, energy, manufacturing, smart city, education, telecom, ...} | 完整枚举（约 21 domains） | 不在枚举中的标注为 "other" 或缺失 | 领域覆盖热力图 | "MDE4ML 在 healthcare/IoT 最密集，在制造/教育稀疏" | EA-06 + Table 5 | 不可迁移 |
| `[42_leaf]` Graphical | 图形化模型表示 | `[41_rq2_model_rep]` Model Representation Type | Google Form §3 → Fig. 8(a) | primary study 的模型表示是否为图形化 | {graphical, textual, both} / 46 | 层级枚举 | 不适用（三值完备） | 表示形式分布 | 图形 vs 文本几乎均分，暗示两者都有成熟度 | EA-07 | 可迁移为"表示形式"维度种子 |
| `[46_leaf]` DSL | 领域特定语言 | `[45_rq2_model_lang]` Modeling Language Type | Google Form §3 → Fig. 8(b) | primary study 是否定义或使用 DSL | {General Purpose DSL, ML DSL, UML Profile, UML, SysML, Goal Models, Feature Models, Data-flow Models, Ontology, Metamodel} / 46 | 层级枚举 | 不在枚举中为缺失 | DSL 采用率 | "DSL 是 MDE4ML 最主流的建模语言形式" | EA-07 | 可迁移为建模语言分类 seed |
| `[62_leaf]` Design & Development | 设计与开发 | `[59_rq2_ml_aspect]` ML Aspect | Google Form §3 → §4.3.2, Fig. 9(a) | ML component 的设计与开发阶段 | {present, absent} / 46 | 层级枚举 | 不覆盖该阶段即 absent | ML 生命周期阶段覆盖热力图 | "design & development 最密集；monitoring/documentation 严重不足" | EA-08 | 可迁移为 ML lifecycle coverage 维度 pattern |
| `[98_leaf]` Fully Automated | 全自动化 | `[97_rq2_automation]` Automation Level | Google Form §3 → §4.3.3, Fig. 8(c) | transformation 是否需要人工干预 | {fully automated, partially automated} / 46 | 层级枚举 | 两值完备 | 自动化程度分布 | "MDE4ML 转换大多是全自动化的（83%）" | EA-09 | 不可简单迁移 |
| `[112_leaf]` No Evaluation | 无评价 | `[111_rq3_method]` Evaluation Method | Google Form §4 → §4.4.2 | primary study 是否没有任何评价 | {present, absent} / 46 | 层级枚举 | 无评价即 present | 评价缺失率 | "仍有 17% (8/46) 的研究无任何评价" | EA-10 | 可迁移为 evaluation rigor 维度 |
| `[120_leaf]` Classification Metrics | 分类指标 | `[119_rq3_ml_metric]` ML Metric | Google Form §4 → Fig. 10(a) | 使用的 ML 评价指标 | {accuracy, precision, recall, F1-score, AUC-ROC, ...} / studies with evaluation | 层级枚举 | N/A（无 evaluation 的研究不取值） | 指标使用偏好 | "分类指标是主要评价方式" | EA-10 + Fig. 10(a) | 可迁移为 metric 分类 seed |
| `[140_leaf]` Approach Limitations | 方法局限 | `[139_rq4_limitation]` Limitation Category | Google Form §5 → §5.1 | primary study 自报的 method 层面的局限 | {limited scope, generalizability, scalability, learning curve, manual steps} / 46 | 层级枚举 | 未报告 limitation 为缺失 | 自报局限性分布 | "scalability 是最常被忽视的维度，75% 论文不讨论" | EA-11 | 可迁移为 limitation taxonomy pattern |

---

## 5. 关系边表

### 5.1 已发现的显式关系边

论文中存在以下跨 RQ 的显式统计关系和层级关系：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `[rel-rq1-rq2-ml-aspect]` | `[23_rq1_ml_technique]` ML Technique Type | 交叉分析 | `[59_rq2_ml_aspect]` ML Aspect | {ML technique} × {ML aspect} / 46 | 两者的缺失分别处理 | §4.2.2 + §4.3.2，text 中有 cross-reference | 技术类型 × 生命周期阶段的联合覆盖可形成 2D 热力图 |
| `[rel-rq2-model-lang-tool]` | `[45_rq2_model_lang]` Modeling Language | 统计联立 | `[100_rq2_tool_avail]` Tool Availability | {language type} × {open/proprietary/none} / 46 | tool 缺失记为 "none" | §4.3 交叉引用 | 建模语言选择是否影响工具可用性 |
| `[rel-rq3-context-quality]` | `[108_rq3_context]` Evaluation Context | 因果主张 | `[133_rq3_qa]` Quality Assessment | {academia, industry} × {QA1–5 scores} / 46 | N/A 处理 | §4.4.1 + §3.5 | 工业评价是否关联更高的研究质量 |
| `[rel-yaer-rq1-rq2]` Publication Year | `[148_leaf]` Year | 时间趋势 | 各 RQ 叶子频次 | year × {各分类维度计数} | 年份为客观值 | Fig. 4 + 全文 | 时间趋势分析（如 2019 年后 MDE4ML 增长） |
| `[rel-rq4-lim-future]` | `[139_rq4_limitation]` Limitation | 语义对应 | `[143_rq4_future]` Future Work | {limitation category} → {future work category} | 各自处理 | §5.1 + §5.2 | 自报 limitation 是否直接映射到 proposed future work |
| `[rel-goal-mltype-contrib]` | `[3_rq1_goal]` Motivation/Goal | 联合分类（Venn） | `[23_rq1_ml_technique]` + `[36_rq1_contribution]` | multi-label | Fig. 6 Venn 图 | EA-06 + Fig. 6 | 动机 × 技术 × 贡献的三维交叉 |

### 5.2 未发现的关系边

以下关系类型在论文中**未显式建立**，但有潜在分析价值：

1. **RAG（retrieval-augmented generation）式数据链路**：无。论文是 SLR，不存在 primary study 之间的数据流。
2. **因果图/因果推断**：无。所有关系都是描述性关联，非因果声明。
3. **形式化关系（formal relation）**：无。没有 `extends`、`refines`、`implements` 等形式化建模关系。
4. **Primary study 之间的引用关系**：Google Form 未抽取 primary study 之间是否互相引用。
5. **效度威胁 → 统计结论的关系**：threats to validity (§7) 列出了 inter-rater reliability、search string coverage、publication bias 等威胁，但**未定量分析这些威胁对具体统计数字的影响方向和大小**。这是 I 级风险——例如 initial count 3496 vs 3934 的不一致已在 `review.md` 中指出的。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 统计观察（由原文字段 / 统计表支持）

| 统计观察 | 支撑字段 | 证据强度 |
|---|---|---|
| SO-01: 43/46 (93%) 的 primary study 以 effort reduction 为 motivation | `[4_rq1_goal_effort]` | strong（Table 3 有逐篇映射） |
| SO-02: motivation 三大类有显著交集（Venn 图），说明多数研究追求多维目标 | `[3_rq1_goal]` | medium（需 PDF 核验 Venn 图大小） |
| SO-03: supervised learning + deep learning 占 ML technique 主导，unsupervised 无 sole-focus 研究 | `[24_leaf]`–`[28_leaf]` | medium |
| SO-04: graphical (18) vs textual (17) model representation 几乎均分 | `[42_leaf]`, `[43_leaf]` | medium（需 Fig. 8(a) 精确数字核验） |
| SO-05: 28/46 (61%) 覆盖 design & development，仅 2/46 覆盖 monitoring，1/46 覆盖 documentation | `[62_leaf]`, `[68_leaf]`, `[73_leaf]` | medium |
| SO-06: 35/46 (76%) 仅使用 M2T transformation；所有 46 篇都是 forward engineering | `[81_leaf]`, `[85_leaf]` | strong |
| SO-07: 38/46 (83%) transformations 为 fully automated，但仅 17/46 (37%) 提供开源工具 | `[98_leaf]`, `[101_leaf]` | medium |
| SO-08: 8/46 (17%) 无任何 evaluation | `[112_leaf]` | medium（需核对 8 篇是否与 QA 缺失一致） |
| SO-09: classification metrics 是最常用的 ML evaluation metric | `[120_leaf]` | medium |
| SO-10: 约 75% 的 primary study 不讨论 scalability | `[140_leaf]` (limited scalability) | weak（论文未给精确百分比，是叙述性估计） |

### 6.2 候选 finding（原文 discussion / recommendation / roadmap 提出）

| 候选 finding | 来源章节 | 本仓库可迁移性 | 证据链 |
|---|---|---|---|
| CF-01: MDE4ML 研究严重偏向 design & training 阶段，monitoring / documentation / deployment 不足 | §6.1.1 Discussion | 可迁移为 "LLM-for-STM 领域生命周期覆盖"的检查维度 pattern | SO-05 |
| CF-02: unsupervised learning 和 RL 在 MDE4ML 中严重覆盖不足 | §6.1.2 Discussion | 可迁移为 "coverage gap" 的检查方法论 pattern | SO-03 |
| CF-03: ML venue 中的 MDE4ML 论文缺少 MDE 细节（如 meta-model、transformation），反之亦然 | §6.1.2 Discussion | 可迁移为 "跨领域论文表述完整性" 的 audit 维度 | EA-12 |
| CF-04: 现有 MDE4ML 方案成熟度低，多为 proof-of-concept，缺少端到端 ML lifecycle 支持 | §6.1.3 Discussion | 可迁移为 "成熟度评估" 维度 seed | SO-07 |
| CF-05: 仅 5/46 有 industrial evaluation，4/46 有 user study | §6.2 Discussion | 可迁移为 "evaluation rigor" 维度 | SO-08 |
| CF-06: MDE4ML 中 responsible ML / human-centric aspects 仅 9/46 覆盖 | §6.1.7 Discussion | 可迁移为 "responsible AI coverage" 维度 seed | EA-12 |
| CF-07: ML terminology 不一致导致难以跨研究比较 | §6.1.5 Discussion | 低迁移价值（领域特定问题） | EA-12 |

### 6.3 对 Paper2 的方法学启发（可迁移）

| 启发 | 迁移对象 | 限制 |
|---|---|---|
| "RQ → data extraction form → feature tree → RQ answer summary"的四层结构 | Paper2 的综述方法论设计 | 需要 Paper2 自己的 RQ 驱动 |
| 每个 RQ 末尾的 "RQ Answer Summary" 作为 narrative synthesis 的标准化格式 | Paper2 的结果呈现 | 格式可复用，内容不可复用 |
| pilot test + dual extraction 的 inter-rater reliability 记录 | Paper2 的方法学质量保障 | 需按 Paper2 实际条件调整 |
| limitations 的三层分类（approach/evaluation/solution quality）+ future work 三层分类 | Paper2 的 discussion 结构 | 可复用分类框架 |

### 6.4 绝不能迁移的领域结论

1. **"TensorFlow 是 MDE4ML 中最常用的 ML framework"** → 对本仓库 STM 研究无意义。
2. **"healthcare 是 MDE4ML 最频繁的应用领域"** → 不可外推。
3. **"图形化与文本化建模语言几乎均分"** → 这是 MDE 领域的发现，不可直接类比到 LLM-based STM。
4. **任何 specific primary study (P1–P46) 的技术细节或统计数字** → 不可迁移。

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 C 级（Critical — 必须修）

| 编号 | 问题 | 建议 |
|---|---|---|
| C-01 | **维度树主树是六叶通用接口，而非原生 schema**。review §维度树复原中，`[dim-...-b1]` 到 `[dim-...-b5]` + 六个 `leaf-*` 是 reviewer 自行定义的"范围/语料/分类/方法/证据/finding"六叶接口，不是 Naveed et al. (2024) 实际使用的编码体系。review 自己承认"六个 leaf-* 是跨论文通用接口层"，但**仍然将其列为一级维度树**，而把真正来自原文的 Google Form 字段 + Fig. 5 feature tree 降级为"原文模式候选叶子映射（A1 种子）"置于旁路。 | 重写维度树复原章节：**原生树优先，六叶降级为标注**。以 Fig. 5 feature tree 的四 RQ 分支 + Google Form 5 section 为主树，将 40 个抽取问题重建为约 150 个节点/叶子的维度森林。六叶接口保留为跨论文对齐标记（annotation），不作为结构框架。 |
| C-02 | **叶子维度表中六个 leaf-* 覆盖了所有叶子**，原文的 real leaf（如 Abstraction、Graphical、Fully Automated、No Evaluation 等）被合并到 `[leaf-mde-ml-components-slr-method]` 的单行中，失去了粒度。 | 将叶子维度表拆分为原生叶子表（约 150 行）+ 六叶接口映射表。原生叶子表必须以本报告 §4 为基础粒度。 |
| C-03 | **统计池资格判定含糊**。review 的 SUMMARY 表中既写"具备系统性证据，可作为后续主统计池候选"，又在同一行写"否（A1-DT 阶段仅作 schema seed）"。这是自相矛盾的——46 篇 primary study 的统计频次、交叉表等**已在原文中报告并可在 A2a 精核后直接进入主统计池**，不应因其证据强度暂为 `not_verified` 而否定其统计资格。 | 将统计池资格改为"是（待 A2a 精核后升级）"，明确当前阻塞条件是需要 PDF 核验 + 页码锚定，而非方法学资格不足。 |
| C-04 | **缺乏 Fig. 5 的节点结构证据**。review 中提到"Fig. 5 feature tree"但未给出该树的节点列表或结构解析，也未标注哪些叶子来自 Fig. 5 本身、哪些来自 text。 | 明确 Fig. 5 是主编码框架的事实源；标注所有来自 Fig. 5 需 PDF 核验的节点；当前用 text 证据给出最大复原 + 标注。 |

### 7.2 I 级（Important — 应该修）

| 编号 | 问题 | 建议 |
|---|---|---|
| I-01 | A.2 证据账本中大多数证据行标记为 `not_verified`，但 "not_verified" 混淆了两种不同情况：①text 中已有足够证据但未做 PDF 版面核对（如 EA-01–EA-12 的文本证据）；②原文中确实未提供精确数字或字段（如 RQ2 某些 modeling language 子类的精确计数未在 text 中出现）。 | 将 `not_verified` 拆分为 `text_verified`（text 中已确认但待 PDF 版面复核）和 `not_extractable`（原文未给出该数字，只能靠 Fig. 估计）。 |
| I-02 | A.3 结论-证据映射中，C01–C09 的结论内容多来自 reviewer 对论文的方法学观察，而非论文自身的原生 finding 或 recommendation。例如 C01 "综述范围、方法、样本规模和报告结构高度可迁移"就是 reviewer 的 meta-level 判断，不是原文结论。 | 重构 A.3 为两层：①原文原生 finding 的结论映射（如 CF-01–CF-07）；② reviewer 对本文方法学价值的 meta 结论。两层分开叙述。 |
| I-03 | review 中多处标注了 3496/3934 的不一致但未给出分析或 resolution。 | 在返修中明确这一数据不一致的来源（哪种页面/段落给出了哪个数字）并记录为需要 author query 或标记为 low-risk data entry error。 |
| I-04 | §7 Threats to Validity 部分在 review 中只简要提及，未分析其对维度树复原的潜在影响（特别是 single-extractor bias 和 inter-rater 仅 pilot 6 篇的边界）。 | 在维度树复原中增加一个 "编码质量威胁" 子节，记录 single-extractor 对字段一致性的潜在影响和 pilot test 的覆盖边界。 |

### 7.3 M 级（Minor — 建议修）

| 编号 | 问题 | 建议 |
|---|---|---|
| M-01 | SUMMARY 表中 "样本数量/分母" 应补入"46 primary studies / 3934 initial"。当前列只有"19 篇 survey-of-surveys 样本"是 cross-paper 语境。 | 在单篇 review 的 SUMMARY 中优先写本文自身样本量（46），cross-paper 分母放在 paper2 共享 SUMMARY。 |
| M-02 | A.4 的本地复验命令缺少对 Fig. 5 的视觉核查清单。 | 补充一条 `[cmd-...-fig5-check]`：人工打开 PDF Fig. 5 逐节点对照本报告 §3 的维度森林复原，标注差异。 |
| M-03 | 英文缩写首次出现未加中文全称（如 SLR / DSL / M2T / M2M / PIM / CIM 等），影响非 MDE 背景读者的可读性。 | 在 review 首部或维度树复原开头增加术语表。 |

---

## 8. 审计附录草案：证据账本与结论映射

### 8.1 A.2 维度树证据账本草案

以下为可直接迁移到 `review.md` A.2 的核心证据行草案（精编版；完整版应包含本报告 §3 中约 150 个节点的逐条证据）。

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | §3.3.2 | database search流程 | "executed on the selected online database search engines to extract an initial pool of 3934 papers" | 样本分母 | text_verified | [3_rq1_goal] et al. | false — text 中明确 | 不可外推 |
| EV-002 | paper_content.txt | §3.3.3 | 三轮筛选 | "filtered 3570 potentially relevant papers in three iterations" → 72 → 55 → 32 | 纳排链条 | text_verified | corpus | false | 不可外推 |
| EV-003 | paper_content.txt | §3.4 | data extraction form | "Google Form with 40 questions… divided into five sections" | 字段来源根 | text_verified | 所有 leaf | false | 方法论可迁移 |
| EV-004 | paper_content.txt | §3.4 | pilot test | "first author extracted data for six papers and compared it with data extracted by the other authors… close match" | inter-rater reliability | text_verified（weak — 仅 pilot 6/46） | code quality | false | 方法论可迁移 |
| EV-005 | paper_content.txt, paper.pdf | §4.1 | Fig. 5 | "Fig. 5 shows a feature tree of the examined features… derived from the data extraction categories based on the RQs" | 维度树框架 | text_verified（text 描述），needs_pdf（树形结构） | [1_root] 及所有分支 | true — Fig. 5 图形结构 | feature tree pattern 可迁移 |
| EV-006 | paper_content.txt, paper.pdf | §4.2.1, Table 3 | Table 3 — Goals of primary studies | 三主类 effort reduction / quality improvement / stakeholder understanding + 子类映射到 P1–P46 | 叶子取值空间 | text_verified（内容可读），needs_pdf（表格格式复核） | [3_rq1_goal] 及其所有子叶 | true — Table 3 格式复核 | 分类框架可迁移，具体映射不可 |
| EV-007 | paper_content.txt, paper.pdf | §4.3.1, Fig. 8(a)(b) | Fig. 8(a) model representation, Fig. 8(b) modeling language | graphical 18, textual 17, both 11; DSL 主导 | 叶子统计频次 | text_verified（数字明确），needs_pdf（图复核） | [42_leaf]–[52_leaf] | true — Fig. 8 图形复核 | 分布数字不可迁移 |
| EV-008 | paper_content.txt, paper.pdf | §4.3.2, Fig. 9(a) | Fig. 9(a) ML aspects distribution | 17 ML aspects 的频次分布 | 叶子统计频次 | text_verified（design & dev 28, training 22, deployment 10 等），needs_pdf（全部 17 个的精确值） | [60_leaf]–[75_leaf] | true — Fig. 9(a) | 分类框架可迁移 |
| EV-009 | paper_content.txt, paper.pdf | §4.3.3 | Table 8 + 正文 | EMF 15, Sirius 10, XTend 5; M2T only 35/46 | 叶子统计频次 | text_verified（核心数字），needs_pdf（Table 8 完整） | [80_leaf]–[107_leaf] | true — Table 8 | 不可迁移 |
| EV-010 | paper_content.txt, paper.pdf | §4.4.2 | evaluation methods | 8 no evaluation, 16 case study, 11 experiment, 4 survey, 3 criteria-based, 3 demonstration, 1 running example | 叶子统计频次 | text_verified | [111_leaf]–[118_leaf] | false — text 中数字明确 | 评价方法分类可迁移 |
| EV-011 | paper_content.txt | §5.1 | limitation categories | approach limitations (scope/generalizability/scalability/learning curve/manual), evaluation limitations, solution quality limitations | 叶子分类 schema | text_verified | [139_leaf]–[142_leaf] | false | limitation taxonomy 可迁移 |
| EV-012 | paper_content.txt | §6.1–§6.2 | discussion recommendations | 7 recommendation themes with evidence refs | 候选 finding 来源 | text_verified | [153_leaf] | false | recommendation pattern 可迁移 |

### 8.2 A.3 结论-证据映射草案

以下为可直接迁移到 `review.md` A.3 的结论映射草案。分两层：（A）原文原生发现；（B）reviewer 对该论文方法学价值的 meta 结论。

#### A 层：原文原生发现

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CON-N01 | MDE4ML 研究自 2019 年快速增长，但方案成熟度低，主要停留在 proof-of-concept | 时间趋势 + 成熟度判断 | [1_root] | EV-005 (Fig. 5), EV-008, EV-009; §6.1.3 Discussion | medium — 有数据但无成熟度 operational definition | 作为 Paper2 的 context/trend background | 成熟度判断部分 subjective；2024 至今可能有新进展 |
| CON-N02 | MDE4ML 严重偏向 ML lifecycle 的 design & training 阶段，monitoring/documentation/deployment 极度不足 | 覆盖缺口（gap finding） | [59_rq2_ml_aspect] | EV-008 (28 design & dev vs 2 monitoring vs 1 documentation) | medium — 频次数据明确但未做缺口显著性检验 | 形成"生命周期覆盖"维度并用于 Paper2 架构 | 46 为小样本，缺口统计可能不显著 |
| CON-N03 | 评价 rigor 不足：17% 无任何 evaluation，仅 11% 有 industrial evaluation | 质量 assessment | [111_rq3_method] | EV-010 (8/46 no eval, 5/46 industry) | medium | 为 Paper2 建立 "evaluation rigor" check 维度 | 样本量和评价标准可能随 MDE4ML 子领域变化 |
| CON-N04 | 开源工具可用性低（仅 37%），阻碍 adoption 和 reproducibility | 基础设施 gap | [100_rq2_tool_avail] | EV-009 (17 open-source vs 23 no tool) | medium | 为 Paper2 建立 "artifact availability" check 维度 | 工具可用性受领域和年份影响大 |
| CON-N05 | responsible ML / human-centric aspects 仅在 9/46 中覆盖 | gap finding | discussion recommendations | EV-012 + §6.1.7 | weak — 9/46 的 "responsible ML" 定义不够 operationalized | candidate finding seed | 对 "responsible ML" 的编码标准可能不统一 |

#### B 层：方法学价值 meta 结论

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CON-M01 | 本文的 "RQ → data extraction form (40 questions 5 sections) → feature tree (Fig. 5) → RQ answer summary" 四层结构是 SLR 维度树设计的高质量模板 | 方法学 pattern 识别 | [1_root] 整棵树 | EV-003, EV-005, EV-006–012 | medium | 直接用作 Paper2 SLR 的方法学模板参考 | 本文是 MDE 子领域，其 RQ 设计可能不完全适用于 LLM-for-STM |
| CON-M02 | 本文 RQ2 的 "model representation / language / level" 三层次分类 + RQ3 的 "context × method × metric" 三层次分类提供了详细且可复用的分类框架结构 | schema seed | [41_rq2_model_rep]–[58_leaf], [108_rq3_context]–[132_leaf] | EV-007, EV-008, EV-010 | medium | 为 Paper2 的方案分类和评价分类提供 schema 种子 | 需 G0/G1 重新批准与调整 |
| CON-M03 | 本文 limitation 的三层分类 (approach / evaluation / solution quality) + future work 三层分类 (approach enhancement / further evaluation / quality enhancement) 可迁移为通用的 paper audit 模板 | schema seed | [139_rq4_limitation]–[145_leaf] | EV-011 | medium | 为 Paper2 的每个 primary study 建立 limitation/future work 编码维度 | 需按目标领域调整子类 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取技能文件

| 文件 | 实际读取 | 采用的原则 |
|---|---|---|
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | 是 | "claim-evidence-engineering workflow"、"evidence gate"、"citation gate"——每条 claim 必须锚定到原文证据 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` | 是 | 六维审稿框架（Originality/Quality/Clarity/Significance/Reproducibility/Ethics）、"Constructive Specificity Standard"——reviewer objection 必须具体到章节/术语/缺失定义 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` | 是 | 五维自审评分（Contribution/Writing/Experimental/Evaluation/Method/Responsibility）、"Adversarial Questions"、claim audit 原则——强 claim 需直接证据、无证据则降级 |
| `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | 是 | 研究计划的结构化方法论——但本任务不需要生成 plan，该 SKILL 用于确认维度树与该 skill 的 `paper_structure` 定义不冲突 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` | 是 | 采用 Paper2Code 的"详细且可操作"原则——维度树叶子/取值空间必须有原文锚点 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md` | 是 | 确认输出 schema 与 task description 不冲突，本报告使用 task description 中规定的 Markdown 结构 |
| `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | 是 | 采用"completion is artifact-gated"原则——本报告本身是 completion artifact，所有 claim 必须可追溯到原文证据 |

### 9.2 最高风险 3 点（reviewer 视角）

| 风险 | 严重度 | 表现 | 主线程合并时复核方式 |
|---|---|---|---|
| **R1: Fig. 5 未做 PDF 核验导致维度树失真** | 高 | §3 的维度森林复原完全基于 text 描述，Fig. 5 的图形节点、层级、连线可能在 text extraction 中丢失或错位。如果 Fig. 5 与 text 描述有结构性差异（如分支命名不同、多出的分类轴未在行文中提及），则维度树骨干可能错误。 | 合并前必须人工打开 PDF 核对 Fig. 5 的完整树结构，逐节点对比 §3 的复原，标注差异并修正。 |
| **R2: 约 150 个节点/叶子的完整性与当前 text 证据强度不匹配** | 中 | §3 复原了约 150 个节点，但部分叶子的确切取值空间、精确计数或子分类来源于 text 中的叙述性描述而非结构化表格（如 Table 6 的 contribution type 完整子类）。某些叶子可能在原文中实为更粗或更细的粒度。 | A2a 精核时逐表/逐图复核每个叶子的取值空间和统计值；对仅有叙述性描述的叶子标记为 `estimated_from_narrative`。 |
| **R3: 对现有 review.md 的返修可能被解读为"否定现有 review 的全部工作"** | 低 | §7 的 C 级返修建议指出六叶接口不该是主树，建议重写维度树复原——但现有 review 的 A.1–A.4 审计附录框架、证据锚点、本地复验命令等是有价值的。若主线程只执行"重写维度树"而不保留有价值部分，会丢失已积累的证据。 | 合并时采用"保留 + 增强"策略：①保留现有 A.1–A.4 框架和已建立的全部证据 ID；②将六叶维度树降级为 §维度树复原 的子节（"跨论文投影标注"）；③新增约 150 行的 native leaf table；④UPDATE 而非 DELETE 现有 evidence rows 的强度标记。 |

### 9.3 任务状态

- **blocked**：否
- **timeout**：否
- **文件缺失**：否（所有指定文件均可读取）
- **pdf 版面核验**：**未做**（如上述 R1）
- 本报告为自包含完整审计报告，不依赖任何上一条消息或中间工具调用输出中未出现在本报告正文中的内容。

---

*审计结束。报告由 deepseek agent 独立完成，2026-06-30。*