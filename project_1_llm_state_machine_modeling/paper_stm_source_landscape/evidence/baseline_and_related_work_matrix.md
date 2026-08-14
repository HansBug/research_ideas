# 基线与相关工作矩阵桥接

完整逐行初筛真源见 [../baselines/SUMMARY.md](../baselines/SUMMARY.md) 与 [../baselines/data/screening_audit.csv](../baselines/data/screening_audit.csv)。P0/P1 的全文级初检真源见 [../survey_baseline_library/SUMMARY.md](../survey_baseline_library/SUMMARY.md) 与 [../survey_baseline_library/data/fulltext_review_matrix.csv](../survey_baseline_library/data/fulltext_review_matrix.csv)。本文件只记录对论文主线 / 声明门禁的桥接摘要，避免双事实源冲突。

## P0/P1 全文初检后的桥接结论

- 25 篇 P0/P1 本地私有 PDF 已全部找到并可抽取文本；仓库未提交 PDF 或全文。
- 7 篇 P0 当前归为 `verified_gap_neighbor_fulltext`：它们强烈约束 #85 的相关工作定位，但没有关闭“控制系统需求 → 状态机来源语料 / benchmark-source landscape → LLM4Modeling 任务”的三段式 gap。
- 18 篇 P1 分为 `verified_near_neighbor_fulltext` 与方法学 / LLM benchmark anchor；它们应进入 Related Work 分层和 CCF-A/B 方法学门槛，而不是写成直接竞品。
- 后续 G3 仍需补齐多数据库 direct-competitor safety search；21 条 auto-fulltext Skip gate 仍需复查。

## 直接近邻 / 可能阻断新颖性的候选

| 行号 | 优先级 | D1 | D2 | D3 | D4 | D7 | 题名 | 对论文主线的影响 |
|---|---|---|---|---|---|---|---|---|
| 1 | `P0` | 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | Model Driven Engineering, Artificial Intelligence, and DevOps for Software and Systems Engineering: A Systematic Mapping Study of Synergies and Challenges | 已全文初检为 gap neighbor；影响新颖性 / 贡献表述但未关闭 #85 gap |
| 2 | `P0` | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | A Systematic Literature Review of Model-Driven Engineering Using Machine Learning | 已全文初检为 gap neighbor；影响新颖性 / 贡献表述但未关闭 #85 gap |
| 3 | `P0` | 🟡 | 🟢 | 🟡 | 🔴 | 🟢 | Early Validation and Verification of System Behaviour in Model-based Systems Engineering: A Systematic Literature Review | 已全文初检为 gap neighbor；影响新颖性 / 贡献表述但未关闭 #85 gap |
| 4 | `P0` | 🟡 | 🟡 | 🟢 | 🟢 | 🟢 | Formal requirements engineering and large language models: A two-way roadmap | 已全文初检为 gap neighbor；影响新颖性 / 贡献表述但未关闭 #85 gap |
| 5 | `P0` | 🟠 | 🟡 | 🟢 | 🟡 | 🟢 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 已全文初检为 gap neighbor；影响新颖性 / 贡献表述但未关闭 #85 gap |
| 6 | `P0` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | A systematic literature review on model-based requirements engineering | 已全文初检为 gap neighbor；影响新颖性 / 贡献表述但未关闭 #85 gap |
| 7 | `P0` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | Requirements extraction from model-based systems engineering: A systematic literature review | 已全文初检为 gap neighbor；影响新颖性 / 贡献表述但未关闭 #85 gap |

## 需要人工全文核验的高度近邻 / 方法学锚点

| 行号 | 优先级 | D1 | D2 | D3 | D4 | D7 | 题名 | 对论文主线的影响 |
|---|---|---|---|---|---|---|---|---|
| 8 | `P1` | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 | Quality assessment of software requirements using artificial intelligence methods: A systematic literature review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 9 | `P1` | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | Machine learning for requirements engineering (ML4RE): A systematic literature review complemented by practitioners’ voices from Stack Overflow | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 10 | `P1` | 🟢 | 🟠 | 🟢 | 🟢 | 🟡 | Generative AI for Testing of Autonomous Driving Systems: A Survey | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 11 | `P1` | 🟠 | 🟡 | 🟢 | 🟡 | 🟡 | Requirements-Driven Automated Software Testing: A Systematic Review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 12 | `P1` | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | A Survey on Automated Driving System Testing: Landscapes and Trends | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 13 | `P1` | 🟠 | 🟠 | 🟡 | 🟢 | 🟡 | Measuring the quality of generative AI systems: Mapping metrics to quality characteristics — Snowballing literature review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 14 | `P1` | 🟢 | 🟠 | 🟢 | 🔴 | 🟡 | Runtime composition in dynamic system of systems: A systematic review of challenges, solutions, tools, and evaluation methods | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 15 | `P1` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | Model-driven safety and security co-analysis: A systematic literature review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 16 | `P1` | 🟠 | 🟠 | 🟢 | 🟢 | 🟡 | Surveying the Benchmarking Landscape of Large Language Models in Code Intelligence | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 17 | `P1` | 🟢 | 🟠 | 🟢 | 🔴 | 🟡 | A Roadmap for Simulation-Based Testing of Autonomous Cyber-Physical Systems: Challenges and Future Direction | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 18 | `P1` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | Model transformation and property preservation in rigorous software development: A systematic literature review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 19 | `P1` | 🟢 | 🟠 | 🟡 | 🔴 | 🟡 | Cyber-physical systems with Human-in-the-Loop: A systematic review of socio-technical perspectives | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 20 | `P1` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | Automotive software product lines for ECU software configuration: A systematic literature review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 21 | `P1` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | Fundamental requirements of Digital Twins for production system in Oil and Gas Industry: A systematic literature review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 22 | `P1` | 🟠 | 🟡 | 🟡 | 🔴 | 🟡 | Scalability and Limitations of Existing Software Requirements Prioritization Techniques: A Systematic Literature Review | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 23 | `P1` | 🟢 | 🟠 | 🟡 | 🔴 | 🟡 | A Systematic Review of IoT Systems Testing: Objectives, Approaches, Tools, and Challenges | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 24 | `P1` | 🟢 | 🟠 | 🟢 | 🔴 | 🟡 | Reflections on Surrogate-Assisted Search-Based Testing: A Taxonomy and Two Replication Studies based on Industrial ADAS and Simulink Models | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |
| 25 | `P1` | 🟠 | 🟡 | 🟠 | 🟢 | 🟠 | Large Language Model-Based Agents for Software Engineering: A Survey | 已全文初检；支撑相关工作定位 / 方法学门槛，不能写成直接竞品 |

## 宽口径方法学 / 期刊门槛锚点

| 行号 | 优先级 | D1 | D2 | D3 | D4 | D7 | 题名 | 对论文主线的影响 |
|---|---|---|---|---|---|---|---|---|
| 26 | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟠 | Navigating the Risks: A Survey of Security and Privacy Threats in LLM-Based Agents | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 27 | `P2` | 🟠 | 🟠 | 🟢 | 🟢 | 🟡 | Large Language Models for Constructing and Optimizing Machine Learning Workflows: A Survey | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 28 | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟡 | Systematic Literature Review on Software Security Vulnerability Information Extraction | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 29 | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟠 | Challenges in Testing Large Language Model Based Software: A Faceted Taxonomy | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 30 | `P2` | 🟠 | 🟠 | 🟢 | 🟢 | 🟡 | Enhancing Automated Unit Test Generation with Large Language Models: A Systematic Literature Review | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 31 | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟡 | A survey of coverage-guided greybox fuzzing with deep neural models | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 32 | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟡 | Faster Code, Deeper Debt? A Multivocal Literature Review on Technical Debt and Its Early Signs in LLM-Assisted Software Development | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 33 | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟡 | Ethical Prompt Engineering for AI-driven SE: Evidence-informed Interaction-time Governance Roadmap to 2030 | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 34 | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟠 | A Survey on LLM-based Code Generation for Low-Resource and Domain-Specific Programming Languages | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 35 | `P2` | 🔴 | 🔴 | 🟢 | 🟢 | 🟡 | Patch Generation in APR: A Survey from the Perspectives of Utilizing LLMs and Using APR-Specific Information | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 36 | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟡 | Psycholinguistic analyses in software engineering text: A systematic mapping study | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 37 | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟡 | A Survey on Large Language Models for Code Generation | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |
| 38 | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟡 | An overview of evaluation and enhancement methods for code generation by large language models | 支撑写作门槛、方法学或背景定位，不参与新颖性对抗 |

## 暂缓 / 已自动解析 / 背景候选

| 行号 | 优先级 | D1 | D2 | D3 | D4 | D7 | 题名 | 对论文主线的影响 |
|---|---|---|---|---|---|---|---|---|
| 39 | `Skip` | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | Testing, Validation, and Verification of Robotic and Autonomous Systems: A Systematic Review | 复查后决定是否保留为背景工作 / 排除审计 |
| 40 | `Skip` | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | Bridging MDE and AI: a systematic review of domain-specific languages and model-driven practices in AI software systems engineering | 复查后决定是否保留为背景工作 / 排除审计 |
| 41 | `Skip` | 🟢 | 🟡 | 🟢 | 🔴 | 🟡 | Model-driven engineering for digital twins: a systematic mapping study | 复查后决定是否保留为背景工作 / 排除审计 |
| 42 | `Skip` | 🟢 | 🟡 | 🟢 | 🔴 | 🟡 | IoT systems testing: Taxonomy, empirical findings, and recommendations | 复查后决定是否保留为背景工作 / 排除审计 |
| 43 | `Skip` | 🟡 | 🟡 | 🟢 | 🟡 | 🟡 | How mature is requirements engineering for AI-based systems? A systematic mapping study on practices, challenges, and future research directions | 复查后决定是否保留为背景工作 / 排除审计 |
| 44 | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | Advances in automated support for requirements engineering: a systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 45 | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟡 | Requirements engineering for sustainable software systems: a systematic mapping study | 复查后决定是否保留为背景工作 / 排除审计 |
| 46 | `Skip` | 🟢 | 🔴 | 🟢 | 🔴 | 🟡 | Finding Critical Scenarios for Automated Driving Systems: A Systematic Mapping Study | 复查后决定是否保留为背景工作 / 排除审计 |
| 47 | `Skip` | 🟠 | 🟠 | 🟢 | 🟡 | 🟡 | A Taxonomy of Information Attributes for Test Case Prioritisation: Applicability, Machine Learning | 复查后决定是否保留为背景工作 / 排除审计 |
| 48 | `Skip` | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | Model driven engineering for machine learning components: A systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 49 | `Skip` | 🟠 | 🟠 | 🟡 | 🔴 | 🟡 | Understanding and evaluating software reuse costs and benefits from industrial cases—A systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 50 | `Skip` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | Digital-twin-based testing for cyber–physical systems: A systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 51 | `Skip` | 🟠 | 🟡 | 🟡 | 🔴 | 🟡 | On transforming model‐based tests into code: A systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 52 | `Skip` | 🔴 | 🔴 | 🟢 | 🟢 | 🟡 | IaC Generation with LLMs: An Error Taxonomy and A Study on Configuration Knowledge Injection | 复查后决定是否保留为背景工作 / 排除审计 |
| 53 | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟠 | Systematic mapping study on requirements engineering for regulatory compliance of software systems | 复查后决定是否保留为背景工作 / 排除审计 |
| 54 | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟡 | Requirements management in DevOps environments: a multivocal mapping study | 复查后决定是否保留为背景工作 / 排除审计 |
| 55 | `Skip` | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 | Accessibility of low-code approaches: A systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 56 | `Skip` | 🟠 | 🟡 | 🟢 | 🔴 | 🟠 | Data catalog tools: A systematic multivocal literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 57 | `Skip` | 🟠 | 🟡 | 🟢 | 🔴 | 🟠 | Automatic identification of privacy and security requirements: a systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 58 | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟠 | An empirically based model of software prototyping: a mapping study and a multi-case study | 复查后决定是否保留为背景工作 / 排除审计 |
| 59 | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟠 | Requirements engineering for older adult digital health software: A systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 60 | `Skip` | 🟠 | 🟡 | 🟡 | 🔴 | 🟠 | Exploring data management challenges and solutions in agile software development: a literature review and practitioner survey | 复查后决定是否保留为背景工作 / 排除审计 |
| 61 | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟠 | Design of blockchain-based applications using model-driven engineering and low-code/no-code platforms: a structured literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 62 | `Skip` | 🟠 | 🟢 | 🟢 | 🟢 | 🟠 | Simulation Approaches for Supporting Microservice Architectures: A Systematic Review | 复查后决定是否保留为背景工作 / 排除审计 |
| 63 | `Skip` | 🟠 | 🟠 | 🟢 | 🟡 | 🟡 | Mining software repositories for software architecture — A systematic mapping study | 复查后决定是否保留为背景工作 / 排除审计 |
| 64 | `Skip` | 🟠 | 🟠 | 🟢 | 🟡 | 🟡 | Industrial applications of software defect prediction using machine learning: A business-driven systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 65 | `Skip` | 🟠 | 🟠 | 🟢 | 🔴 | 🟡 | Code smell prioritization in object‐oriented software systems: A systematic literature review | 复查后决定是否保留为背景工作 / 排除审计 |
| 66 | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟠 | Addressing Visual Impairments with Model-Driven Engineering: A Systematic Literature Review | 复查后决定是否保留为背景工作 / 排除审计 |
| 67 | `Skip` | 🟠 | 🟠 | 🟢 | 🔴 | 🟡 | Web application testing—Challenges and opportunities | 复查后决定是否保留为背景工作 / 排除审计 |
| 68 | `Skip` | 🟠 | 🟠 | 🟡 | 🔴 | 🟠 | Software architecture for quantum computing systems — A systematic review | 复查后决定是否保留为背景工作 / 排除审计 |
| 69 | `Skip` | 🟠 | 🟢 | 🟠 | 🔴 | 🔴 | An overview of research with Slco on seamless integration of formal verification into model-driven software engineering | 复查后决定是否保留为背景工作 / 排除审计 |

## 声明门禁关联

- P0 已完成本地私有全文初检，可写成 `verified_gap_neighbor_fulltext`，但不得写成最终 verified direct competitor 或完整竞品检索闭环。
- P1 已完成本地私有全文初检，可进入 Related Work 分层；仍需在最终稿中保留 locator / caveat。
- P2 主要支撑方法学和期刊门槛，不参与新颖性对抗。
- `Skip` 中自动全文轻量复查标记为 `yes` 的 21 行必须复查后才能最终排除。
