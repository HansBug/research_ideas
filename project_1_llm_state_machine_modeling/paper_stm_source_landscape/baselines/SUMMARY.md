# #85 相关工作与基线初筛总账

更新时间：`2026-06-11 20:50:00`。本文件是 #85 相关工作 / 基线初筛的逐行总账。当前所有关系均为**元数据级初步判断**；除非后续明确标记为 `fulltext_manual_checked` 或 `verified_fact`，不得写成已核验事实。

> 说明：论文题名、期刊 / 会议名、DOI 链接和机器字段名保留官方英文；解释性文字尽量中文化。七维评分的机器可审计证据列见 [data/screening_audit.csv](./data/screening_audit.csv)。

## 0. 总览

| 指标 | 数量 / 状态 |
|---|---|
| #95 输入候选 | 438 |
| #85 初筛子集 | 69 |
| P0 | 7 |
| P1 | 18 |
| P2 | 13 |
| Skip | 31 |
| P0/P1 人工下载 BibTeX | 25 |
| 自动全文轻量复查门禁 | 7 |

## 1. `relation_level` 分布

| 关系等级字段 `relation_level` | 数量 |
|---|---|
| background_cluster_or_exclude_metadata_only | 8 |
| candidate_direct_metadata_only | 7 |
| candidate_near_metadata_only | 31 |
| methodology_anchor_metadata_only | 22 |
| watch_metadata_only | 1 |

## 2. `include_reason` 分布

| 纳入原因字段 `include_reason` | 数量 |
|---|---|
| control_cps_mapping_near_85 | 20 |
| core_seed | 18 |
| llm4modeling_near_85 | 1 |
| llm_benchmark_landscape_watch | 10 |
| methodology_anchor_for_85 | 9 |
| modeling_or_formal_mapping_near_85 | 11 |

## 3. 69 行 D1--D7 初筛矩阵

| # | 关系 | 优先级 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | 题名 | 期刊 / 会议 | DOI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `candidate_direct_metadata_only` | `P0` | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟢 | Model Driven Engineering, Artificial Intelligence, and DevOps for Software and Systems Engineering: A Systematic Mapping Study of Synergies and Challenges | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3759454) |
| 2 | `candidate_direct_metadata_only` | `P0` | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟠 | 🟢 | A Systematic Literature Review of Model-Driven Engineering Using Machine Learning | IEEE Transactions on Software Engineering | [DOI](https://doi.org/10.1109/tse.2024.3430514) |
| 3 | `candidate_direct_metadata_only` | `P0` | 🟡 | 🟢 | 🟡 | 🔴 | 🟡 | 🟡 | 🟢 | Early Validation and Verification of System Behaviour in Model-based Systems Engineering: A Systematic Literature Review | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3631976) |
| 4 | `candidate_direct_metadata_only` | `P0` | 🟡 | 🟡 | 🟢 | 🟢 | 🟠 | 🟠 | 🟢 | Formal requirements engineering and large language models: A two-way roadmap | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107697) |
| 5 | `candidate_direct_metadata_only` | `P0` | 🟠 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟢 | Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2024.107492) |
| 6 | `candidate_direct_metadata_only` | `P0` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | A systematic literature review on model-based requirements engineering | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2026.112836) |
| 7 | `candidate_direct_metadata_only` | `P0` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | Requirements extraction from model-based systems engineering: A systematic literature review | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2025.112407) |
| 8 | `candidate_near_metadata_only` | `P1` | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 | 🟠 | 🟡 | Quality assessment of software requirements using artificial intelligence methods: A systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107979) |
| 9 | `candidate_near_metadata_only` | `P1` | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | 🟠 | 🟡 | Machine learning for requirements engineering (ML4RE): A systematic literature review complemented by practitioners’ voices from Stack Overflow | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2024.107477) |
| 10 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟠 | 🟢 | 🟢 | 🟠 | 🟠 | 🟡 | Generative AI for Testing of Autonomous Driving Systems: A Survey | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3806653) |
| 11 | `candidate_near_metadata_only` | `P1` | 🟠 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 | Requirements-Driven Automated Software Testing: A Systematic Review | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3767739) |
| 12 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟢 | 🟢 | 🔴 | 🟠 | 🟠 | 🟡 | A Survey on Automated Driving System Testing: Landscapes and Trends | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3579642) |
| 13 | `candidate_near_metadata_only` | `P1` | 🟠 | 🟠 | 🟡 | 🟢 | 🟡 | 🟠 | 🟡 | Measuring the quality of generative AI systems: Mapping metrics to quality characteristics — Snowballing literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107802) |
| 14 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟠 | 🟢 | 🔴 | 🟡 | 🟠 | 🟡 | Runtime composition in dynamic system of systems: A systematic review of challenges, solutions, tools, and evaluation methods | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2025.112661) |
| 15 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | Model-driven safety and security co-analysis: A systematic literature review | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2024.112251) |
| 16 | `candidate_near_metadata_only` | `P1` | 🟠 | 🟠 | 🟢 | 🟢 | 🟠 | 🟠 | 🟡 | Surveying the Benchmarking Landscape of Large Language Models in Code Intelligence | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3800957) |
| 17 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟠 | 🟢 | 🔴 | 🟠 | 🟠 | 🟡 | A Roadmap for Simulation-Based Testing of Autonomous Cyber-Physical Systems: Challenges and Future Direction | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3711906) |
| 18 | `candidate_near_metadata_only` | `P1` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | Model transformation and property preservation in rigorous software development: A systematic literature review | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2025.112508) |
| 19 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟠 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | Cyber-physical systems with Human-in-the-Loop: A systematic review of socio-technical perspectives | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2025.112348) |
| 20 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | Automotive software product lines for ECU software configuration: A systematic literature review | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2025.112716) |
| 21 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | Fundamental requirements of Digital Twins for production system in Oil and Gas Industry: A systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107742) |
| 22 | `candidate_near_metadata_only` | `P1` | 🟠 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | Scalability and Limitations of Existing Software Requirements Prioritization Techniques: A Systematic Literature Review | Journal of Software: Evolution and Process | [DOI](https://doi.org/10.1002/smr.70039) |
| 23 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟠 | 🟡 | 🔴 | 🟡 | 🟠 | 🟡 | A Systematic Review of IoT Systems Testing: Objectives, Approaches, Tools, and Challenges | IEEE Transactions on Software Engineering | [DOI](https://doi.org/10.1109/tse.2024.3363611) |
| 24 | `candidate_near_metadata_only` | `P1` | 🟢 | 🟠 | 🟢 | 🔴 | 🟠 | 🟠 | 🟡 | Reflections on Surrogate-Assisted Search-Based Testing: A Taxonomy and Two Replication Studies based on Industrial ADAS and Simulink Models | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2023.107286) |
| 25 | `candidate_near_metadata_only` | `P1` | 🟠 | 🟡 | 🟠 | 🟢 | 🟠 | 🟠 | 🟠 | Large Language Model-Based Agents for Software Engineering: A Survey | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3796507) |
| 26 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟠 | 🟠 | 🟠 | Navigating the Risks: A Survey of Security and Privacy Threats in LLM-Based Agents | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3807666) |
| 27 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🟠 | 🟢 | 🟢 | 🟠 | 🟠 | 🟡 | Large Language Models for Constructing and Optimizing Machine Learning Workflows: A Survey | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3773084) |
| 28 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟡 | 🟠 | 🟡 | Systematic Literature Review on Software Security Vulnerability Information Extraction | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3745026) |
| 29 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟠 | 🟠 | 🟠 | Challenges in Testing Large Language Model Based Software: A Faceted Taxonomy | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3806396) |
| 30 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🟠 | 🟢 | 🟢 | 🟡 | 🟠 | 🟡 | Enhancing Automated Unit Test Generation with Large Language Models: A Systematic Literature Review | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3802827) |
| 31 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟠 | 🟠 | 🟡 | A survey of coverage-guided greybox fuzzing with deep neural models | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107797) |
| 32 | `methodology_anchor_metadata_only` | `P2` | 🟢 | 🔴 | 🟢 | 🟢 | 🟡 | 🟠 | 🟡 | Faster Code, Deeper Debt? A Multivocal Literature Review on Technical Debt and Its Early Signs in LLM-Assisted Software Development | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3820165) |
| 33 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟠 | 🟠 | 🟡 | Ethical Prompt Engineering for AI-driven SE: Evidence-informed Interaction-time Governance Roadmap to 2030 | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3801980) |
| 34 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🟡 | 🟢 | 🟢 | 🟠 | 🟠 | 🟠 | A Survey on LLM-based Code Generation for Low-Resource and Domain-Specific Programming Languages | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3770084) |
| 35 | `methodology_anchor_metadata_only` | `P2` | 🔴 | 🔴 | 🟢 | 🟢 | 🟠 | 🟡 | 🟡 | Patch Generation in APR: A Survey from the Perspectives of Utilizing LLMs and Using APR-Specific Information | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3764584) |
| 36 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟡 | 🟠 | 🟡 | Psycholinguistic analyses in software engineering text: A systematic mapping study | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107913) |
| 37 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟠 | 🟠 | 🟡 | A Survey on Large Language Models for Code Generation | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3747588) |
| 38 | `methodology_anchor_metadata_only` | `P2` | 🟠 | 🔴 | 🟢 | 🟢 | 🟠 | 🟠 | 🟡 | An overview of evaluation and enhancement methods for code generation by large language models | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2026.108185) |
| 39 | `candidate_near_metadata_only` | `Skip` | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | 🟢 | 🟡 | Testing, Validation, and Verification of Robotic and Autonomous Systems: A Systematic Review | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3542945) |
| 40 | `candidate_near_metadata_only` | `Skip` | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 | Bridging MDE and AI: a systematic review of domain-specific languages and model-driven practices in AI software systems engineering | Software and Systems Modeling | [DOI](https://doi.org/10.1007/s10270-024-01211-y) |
| 41 | `candidate_near_metadata_only` | `Skip` | 🟢 | 🟡 | 🟢 | 🔴 | 🟡 | 🟢 | 🟡 | Model-driven engineering for digital twins: a systematic mapping study | Software and Systems Modeling | [DOI](https://doi.org/10.1007/s10270-025-01264-7) |
| 42 | `candidate_near_metadata_only` | `Skip` | 🟢 | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟡 | IoT systems testing: Taxonomy, empirical findings, and recommendations | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2025.112408) |
| 43 | `candidate_near_metadata_only` | `Skip` | 🟡 | 🟡 | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | How mature is requirements engineering for AI-based systems? A systematic mapping study on practices, challenges, and future research directions | Requirements Engineering | [DOI](https://doi.org/10.1007/s00766-024-00432-3) |
| 44 | `candidate_near_metadata_only` | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟢 | 🟢 | 🟡 | Advances in automated support for requirements engineering: a systematic literature review | Requirements Engineering | [DOI](https://doi.org/10.1007/s00766-023-00411-0) |
| 45 | `candidate_near_metadata_only` | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟡 | Requirements engineering for sustainable software systems: a systematic mapping study | Requirements Engineering | [DOI](https://doi.org/10.1007/s00766-023-00402-1) |
| 46 | `candidate_near_metadata_only` | `Skip` | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🟡 | Finding Critical Scenarios for Automated Driving Systems: A Systematic Mapping Study | IEEE Transactions on Software Engineering | [DOI](https://doi.org/10.1109/tse.2022.3170122) |
| 47 | `candidate_near_metadata_only` | `Skip` | 🟠 | 🟠 | 🟢 | 🟡 | 🟡 | 🟢 | 🟡 | A Taxonomy of Information Attributes for Test Case Prioritisation: Applicability, Machine Learning | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3511805) |
| 48 | `candidate_near_metadata_only` | `Skip` | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 | Model driven engineering for machine learning components: A systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2024.107423) |
| 49 | `candidate_near_metadata_only` | `Skip` | 🟠 | 🟠 | 🟡 | 🔴 | 🟢 | 🟢 | 🟡 | Understanding and evaluating software reuse costs and benefits from industrial cases—A systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2024.107451) |
| 50 | `candidate_near_metadata_only` | `Skip` | 🟢 | 🟡 | 🟡 | 🔴 | 🟡 | 🟢 | 🟡 | Digital-twin-based testing for cyber–physical systems: A systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2022.107145) |
| 51 | `candidate_near_metadata_only` | `Skip` | 🟠 | 🟡 | 🟡 | 🔴 | 🟢 | 🟢 | 🟡 | On transforming model‐based tests into code: A systematic literature review | Software Testing, Verification and Reliability | [DOI](https://doi.org/10.1002/stvr.1860) |
| 52 | `methodology_anchor_metadata_only` | `Skip` | 🔴 | 🔴 | 🟢 | 🟢 | 🟡 | 🟢 | 🟡 | IaC Generation with LLMs: An Error Taxonomy and A Study on Configuration Knowledge Injection | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3817608) |
| 53 | `methodology_anchor_metadata_only` | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟠 | Systematic mapping study on requirements engineering for regulatory compliance of software systems | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2024.107622) |
| 54 | `methodology_anchor_metadata_only` | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟡 | Requirements management in DevOps environments: a multivocal mapping study | Requirements Engineering | [DOI](https://doi.org/10.1007/s00766-023-00396-w) |
| 55 | `methodology_anchor_metadata_only` | `Skip` | 🔴 | 🟡 | 🟡 | 🔴 | 🟢 | 🟢 | 🟡 | Accessibility of low-code approaches: A systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2024.107570) |
| 56 | `methodology_anchor_metadata_only` | `Skip` | 🟠 | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟠 | Data catalog tools: A systematic multivocal literature review | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2025.112584) |
| 57 | `methodology_anchor_metadata_only` | `Skip` | 🟠 | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟠 | Automatic identification of privacy and security requirements: a systematic literature review | Requirements Engineering | [DOI](https://doi.org/10.1007/s00766-025-00455-4) |
| 58 | `methodology_anchor_metadata_only` | `Skip` | 🟡 | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟠 | An empirically based model of software prototyping: a mapping study and a multi-case study | Empirical Software Engineering | [DOI](https://doi.org/10.1007/s10664-023-10331-w) |
| 59 | `methodology_anchor_metadata_only` | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟢 | 🟢 | 🟠 | Requirements engineering for older adult digital health software: A systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107718) |
| 60 | `methodology_anchor_metadata_only` | `Skip` | 🟠 | 🟡 | 🟡 | 🔴 | 🟢 | 🟢 | 🟠 | Exploring data management challenges and solutions in agile software development: a literature review and practitioner survey | Empirical Software Engineering | [DOI](https://doi.org/10.1007/s10664-025-10630-4) |
| 61 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟢 | 🟢 | 🟠 | Design of blockchain-based applications using model-driven engineering and low-code/no-code platforms: a structured literature review | Software and Systems Modeling | [DOI](https://doi.org/10.1007/s10270-023-01109-1) |
| 62 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟠 | 🟢 | 🟢 | 🟢 | 🟡 | 🟠 | 🟠 | Simulation Approaches for Supporting Microservice Architectures: A Systematic Review | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3816152) |
| 63 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟠 | 🟠 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 | Mining software repositories for software architecture — A systematic mapping study | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2025.107677) |
| 64 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟠 | 🟠 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 | Industrial applications of software defect prediction using machine learning: A business-driven systematic literature review | Information and Software Technology | [DOI](https://doi.org/10.1016/j.infsof.2023.107192) |
| 65 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟠 | 🟠 | 🟢 | 🔴 | 🟡 | 🟠 | 🟡 | Code smell prioritization in object‐oriented software systems: A systematic literature review | Journal of Software: Evolution and Process | [DOI](https://doi.org/10.1002/smr.2536) |
| 66 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | 🟠 | 🟠 | Addressing Visual Impairments with Model-Driven Engineering: A Systematic Literature Review | ACM Transactions on Software Engineering and Methodology | [DOI](https://doi.org/10.1145/3803865) |
| 67 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟠 | 🟠 | 🟢 | 🔴 | 🟠 | 🟠 | 🟡 | Web application testing—Challenges and opportunities | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2024.112186) |
| 68 | `background_cluster_or_exclude_metadata_only` | `Skip` | 🟠 | 🟠 | 🟡 | 🔴 | 🟢 | 🟢 | 🟠 | Software architecture for quantum computing systems — A systematic review | Journal of Systems and Software | [DOI](https://doi.org/10.1016/j.jss.2023.111682) |
| 69 | `watch_metadata_only` | `Skip` | 🟠 | 🟢 | 🟠 | 🔴 | 🟠 | 🟢 | 🔴 | An overview of research with Slco on seamless integration of formal verification into model-driven software engineering | Science of Computer Programming | [DOI](https://doi.org/10.1016/j.scico.2025.103386) |

## 4. P0/P1 人工下载入口

完整 BibTeX 见 [data/manual_download_needed.bib](./data/manual_download_needed.bib)，人工协作队列见 [MANUAL_DOWNLOAD_REQUESTS.md](./MANUAL_DOWNLOAD_REQUESTS.md)。

## 5. 自动全文复查门禁

当前共有 `7` 行自动全文轻量复查标记为 `yes`，详见 [data/auto_fulltext_light_review_gate.csv](./data/auto_fulltext_light_review_gate.csv)。复查前不得把这些行最终排除。

## 6. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-11 20:50:00 | 修复 D1 评分的泛词误命中，避免把 `security`、`execution` 等误判为 ECU / 嵌入式证据；继续保留元数据级边界。 |
| 2026-06-11 20:30:00 | 修复 `source_row_index` 为 #95 原始 CSV 1-based 行号；补齐 D1--D7 evidence/rationale/pending 字段；中文化自动全文复查理由。 |
| 2026-06-11 19:06:00 | 初始化 #85 相关工作与基线初筛总账；落地 438 行审计、69 行初筛、25 条人工下载 BibTeX、7 条自动全文复查门禁。 |
