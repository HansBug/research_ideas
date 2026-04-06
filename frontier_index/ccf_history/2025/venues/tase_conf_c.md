# `TASE` (`2025`) 论文名录

## 1. 文件导航

- 年度总页：[../README.md](../README.md)
- 计数复核：[../verification.json](../verification.json)
- 数据文件：[metadata](../metadata/tase_conf_c.json)
- 说明：本页承载本 venue 的逐篇论文名录，并按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级从高到低排序。

## 2. 基本信息

- 全称：Theoretical Aspects of Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`22`
- 主体归属：形式化方法与软件工程交叉
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件工程名下的 formal verification / assurance 邻近

## 3. 关键信息页面

- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/tase/
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0)
- 一级总判定分布：程序设计语言与形式化基础 14 / 软件工程 8
- 软工纳入判定分布：不属于软件工程 14 / 跨域但软工主导 6 / 属于软件工程 2
- 判定来源分布：人工复核 (22)
- 人工复核状态分布：已人工复核 (22)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (4) / 5.3.1 性能建模、基准与调优 (1) / 1.2.1 形式化规约与契约 (1) / 3.1.1 测试生成与增强 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Adaptive Clause Management in SMT Solvers: A Dynamic Weighting Framework for Formal Verification | Wenda Leng, Meihua Liu, Yufeng Jin | 围绕《Adaptive Clause Management in SMT Solvers: A Dynamic Weighting Framework for Formal Verification》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | 人工复核：论文核心问题是 SMT solver 的 clause management 与验证性能优化，属于求解器算法问题，不是软件工程。 | [10.1007/978-3-031-98208-8_9](https://doi.org/10.1007/978-3-031-98208-8_9) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_9) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2025:conf_tase_LengLJ25` | 应从软工集合中移出。 |
| 2 | Machine-Checked Compositional Specification and Proofs for Embedded Systems | Karl Palmskog, Mattias Nyberg, Dilian Gurov | 围绕《Machine-Checked Compositional Specification and Proofs for Embedded Systems》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_5](https://doi.org/10.1007/978-3-031-98208-8_5) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_5) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2025:conf_tase_PalmskogNG25` |  |
| 3 | Random Testing of Model Checkers for Timed Automata with Automated Oracle Generation | Andrea Manini, Matteo G. Rossi, Pierluigi San Pietro | 围绕《Random Testing of Model Checkers for Timed Automata with Automated Oracle Generation》开展研究。 | 软件工程 | 属于软件工程 | 人工复核 | 已人工复核 | 3.1.1 测试生成与增强 | 1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性；1.2.3 规约质量与一致性 | X1=否; D1=3; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_20](https://doi.org/10.1007/978-3-031-98208-8_20) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_20) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2025:conf_tase_ManiniRP25` | 跨域 |
| 4 | Robust Deep Reinforcement Learning Using Formal Verification | Avraham Raviv, Shaiel Vistuch, Boaz Gurevich, Erel Dekel, Hillel Kugler | 围绕《Robust Deep Reinforcement Learning Using Formal Verification》开展研究。 | 软件工程 | 跨域但软工主导 | 人工复核 | 已人工复核 | 3.3.1 面向软工问题的形式化验证 | 1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性；1.2.3 规约质量与一致性 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_11](https://doi.org/10.1007/978-3-031-98208-8_11) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_11) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2025:conf_tase_RavivVGDK25` | 跨域 |
| 5 | Safeguarding Neural Network-Controlled Systems via Formal Methods: From Safety-by-Design to Runtime Assurance (Invited Talk) | Min Zhang 0002 | 围绕《Safeguarding Neural Network-Controlled Systems via Formal Methods: From Safety-by-Design to Runtime Assurance (Invited Talk)》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_1](https://doi.org/10.1007/978-3-031-98208-8_1) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_1) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2025:conf_tase_Zhang25` |  |
| 6 | Testing-Based Formal Verification with Program Slicing on Functional Soundness and Completeness | Ai Liu, Yang Liu 0003, Shaoying Liu, Zhibin Yang | 围绕《Testing-Based Formal Verification with Program Slicing on Functional Soundness and Completeness》开展研究。 | 软件工程 | 跨域但软工主导 | 人工复核 | 已人工复核 | 3.3.1 面向软工问题的形式化验证 | 3.3.1 面向软工问题的形式化验证；1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性 | 人工复核：论文主问题是基于 slicing 的测试辅助形式化验证，核心仍是软件形式化验证。 | [10.1007/978-3-031-98208-8_2](https://doi.org/10.1007/978-3-031-98208-8_2) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_2) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2025:conf_tase_LiuLLY25` | 跨域；人工复核后从 1.2.3 调整到 3.3.1。 |
| 7 | Unleash the Hidden Power of CAR-Based Model Checking Through Dynamic Traversal | Yibo Dong 0001, Yu Chen, Jianwen Li, Geguang Pu | 围绕《Unleash the Hidden Power of CAR-Based Model Checking Through Dynamic Traversal》开展研究。 | 软件工程 | 属于软件工程 | 人工复核 | 已人工复核 | 3.3.1 面向软工问题的形式化验证 | 1.3.3 模型分析、仿真与验证；1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性 | X1=否; D1=2; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_22](https://doi.org/10.1007/978-3-031-98208-8_22) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_22) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2025:conf_tase_DongCLP25` | 跨域 |
| 8 | A Coherent Index for Dichotomy in Version-Controlled Repositories | Laurent Bulteau, Pierre-Yves David, Florian Horn 0001, Euxane Tran-Girard | 围绕《A Coherent Index for Dichotomy in Version-Controlled Repositories》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_14](https://doi.org/10.1007/978-3-031-98208-8_14) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_14) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_BulteauDHT25` |  |
| 9 | A Cross-Domain Data Sharing Scheme Based on Federated Blockchain | Honglin Mao, Jie Zhang 0111, Yao Zhang 0019, Xiaohong Li 0001 | 围绕《A Cross-Domain Data Sharing Scheme Based on Federated Blockchain》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_17](https://doi.org/10.1007/978-3-031-98208-8_17) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_17) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_MaoZZL25` |  |
| 10 | A Formal Framework for Naturally Specifying and Verifying Sequential Algorithms | Chengxi Yang, Shushu Wu, Qinxiang Cao | 围绕《A Formal Framework for Naturally Specifying and Verifying Sequential Algorithms》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_4](https://doi.org/10.1007/978-3-031-98208-8_4) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_4) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_YangWC25` |  |
| 11 | A Formally Verified Neural Network Converter for the Interactive Theorem Prover Coq | Leo Alexander Gummersbach, Kim Völlinger, Andrei Aleksandrov | 围绕《A Formally Verified Neural Network Converter for the Interactive Theorem Prover Coq》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_12](https://doi.org/10.1007/978-3-031-98208-8_12) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_12) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_GummersbachVA25` |  |
| 12 | CASTLE: Benchmarking Dataset for Static Code Analyzers and LLMs Towards CWE Detection | Richard A. Dubniczky, Krisztofer Zoltán Horvát, Tamás Bisztray, Mohamed Amine Ferrag, Lucas C. Cordeiro, Norbert Tihanyi | 围绕《CASTLE: Benchmarking Dataset for Static Code Analyzers and LLMs Towards CWE Detection》开展研究。 | 软件工程 | 跨域但软工主导 | 人工复核 | 已人工复核 | 5.3.1 性能建模、基准与调优 | 6.3.4 replication、benchmark 与开放科学；8.5.3 大模型原生与 agentic 软件系统；1.2.1 形式化规约与契约 | X1=否; D1=2; D2=0; D3=1; D4=1; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_15](https://doi.org/10.1007/978-3-031-98208-8_15) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_15) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_DubniczkyHBFCT25` | 跨域 |
| 13 | COMPASS: An Agent for MLIR Compilation Pass Pipeline Generation | Hongbin Zhang, Shihao Gao, Yang Liu, Mingjie Xing, Yanjun Wu, Chen Zhao | 围绕《COMPASS: An Agent for MLIR Compilation Pass Pipeline Generation》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=1; D3=0; D4=0; venue=部分属于软工; cross=是; PL=compilation | [10.1007/978-3-031-98208-8_13](https://doi.org/10.1007/978-3-031-98208-8_13) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_13) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_ZhangGLXWZ25` |  |
| 14 | Dependent Assertion Logic for Modular Software Verification | Lukas Grätz | 围绕《Dependent Assertion Logic for Modular Software Verification》开展研究。 | 软件工程 | 跨域但软工主导 | 人工复核 | 已人工复核 | 3.3.1 面向软工问题的形式化验证 | 1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性；1.2.3 规约质量与一致性 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_3](https://doi.org/10.1007/978-3-031-98208-8_3) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_3) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_Gratz25` | 跨域 |
| 15 | Detecting Speculative Data Flow Vulnerabilities Using Weakest Precondition Reasoning | Graeme Smith 0001 | 围绕《Detecting Speculative Data Flow Vulnerabilities Using Weakest Precondition Reasoning》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_19](https://doi.org/10.1007/978-3-031-98208-8_19) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_19) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_Smith25` |  |
| 16 | Failure Divergence Refinement for Event-B | Sebastian Stock 0002, Michael Leuschel, Atif Mashkoor | 围绕《Failure Divergence Refinement for Event-B》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_6](https://doi.org/10.1007/978-3-031-98208-8_6) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_6) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_StockLM25` |  |
| 17 | FAMiT: Mitigating False Alarms for Program Analysis Using Large Language Models | Jiabao Zeng, Yuanlin Li, Ran Zhang, Yuanmin Xie, Kejia Li, Min Zhou 0001 | 围绕《FAMiT: Mitigating False Alarms for Program Analysis Using Large Language Models》开展研究。 | 软件工程 | 跨域但软工主导 | 人工复核 | 已人工复核 | 1.2.1 形式化规约与契约 | 8.5.3 大模型原生与 agentic 软件系统；1.2.2 自然语言到规约/属性；1.2.3 规约质量与一致性 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_16](https://doi.org/10.1007/978-3-031-98208-8_16) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_16) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_ZengLZXLZ25` | 跨域 |
| 18 | Mining Diamonds in Labelled Transition Systems | P. H. M. van Spaendonck, Kevin H. J. Jilissen | 围绕《Mining Diamonds in Labelled Transition Systems》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_7](https://doi.org/10.1007/978-3-031-98208-8_7) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_7) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_SpaendonckJ25` |  |
| 19 | Operational Semantics for Crystality: A Smart Contract Language for Parallel EVMs | Ziyun Xu, Hao Wang 0002, Meng Sun 0002 | 围绕《Operational Semantics for Crystality: A Smart Contract Language for Parallel EVMs》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=1; D3=0; D4=0; venue=部分属于软工; cross=是; PL=operational semantics | [10.1007/978-3-031-98208-8_18](https://doi.org/10.1007/978-3-031-98208-8_18) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_18) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_XuWS25` |  |
| 20 | Portability of Optimizations from SC to TSO | Akshay Gopalakrishnan, Clark Verbrugge | 围绕《Portability of Optimizations from SC to TSO》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_8](https://doi.org/10.1007/978-3-031-98208-8_8) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_8) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_GopalakrishnanV25` |  |
| 21 | SNRWLS: Improve (W)PMS Solver with Weighting Strategies Related to Number of Soft Clauses | Shuhao Chen, Menghua Jiang 0001, Yin Chen | 围绕《SNRWLS: Improve (W)PMS Solver with Weighting Strategies Related to Number of Soft Clauses》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 人工复核 | 已人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_10](https://doi.org/10.1007/978-3-031-98208-8_10) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_10) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_ChenJC25` |  |
| 22 | State Significance-Guided Fuzzing for Stateful Protocol Program | Kunpeng Jian, Yanyan Zou, Chen Wang, Ning Li, Menghao Li, Wei Huo | 围绕《State Significance-Guided Fuzzing for Stateful Protocol Program》开展研究。 | 软件工程 | 跨域但软工主导 | 人工复核 | 已人工复核 | 3.1.3 模糊、搜索式、变异与性质驱动测试 | 1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性；1.2.3 规约质量与一致性 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-98208-8_21](https://doi.org/10.1007/978-3-031-98208-8_21) | [link](https://link.springer.com/10.1007/978-3-031-98208-8_21) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2025:conf_tase_JianZWLLH25` | 跨域 |

## 6. 本 venue 年度观察

- 主题标签补充：形式化方法 (9) / 测试与验证 (6) / 待人工细分 (6) / LLM/AI for SE (4) / 建模/模型驱动 (3)
- 建议优先获取 `PDF` 的论文：`Adaptive Clause Management in SMT Solvers: A Dynamic Weighting Framework for Formal Verification`；`Machine-Checked Compositional Specification and Proofs for Embedded Systems`；`Random Testing of Model Checkers for Timed Automata with Automated Oracle Generation`；`Robust Deep Reinforcement Learning Using Formal Verification`；`Safeguarding Neural Network-Controlled Systems via Formal Methods: From Safety-by-Design to Runtime Assurance (Invited Talk)`
