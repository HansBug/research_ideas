# `RV` (`2022`) 论文名录

## 1. 文件导航

- 年度总页：[../README.md](../README.md)
- 计数复核：[../verification.json](../verification.json)
- 数据文件：[metadata](../metadata/rv_conf_c.json)
- 近 `5` 年投稿时间线：[../../SUBMISSION_TIMELINES.md#timeline-rv_conf_c](../../SUBMISSION_TIMELINES.md#timeline-rv_conf_c)
- 说明：本页承载本 venue 的逐篇论文名录，并按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级从高到低排序。

## 2. 基本信息

- 全称：International Conference on Runtime Verification
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2022`
- 条目数：`22`
- 主体归属：形式化方法与软件工程交叉
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：运行时验证 / 监测 / 时序性质 / 工具链直接邻近

## 3. 关键信息页面

- 年主页：https://rv22.gitlab.io
- 学术索引页：https://dblp.org/db/conf/rv/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-031-17196-3
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (1) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0)
- 一级总判定分布：程序设计语言与形式化基础 13 / 软件工程 9
- 软工纳入判定分布：不属于软件工程 13 / 跨域但软工主导 7 / 属于软件工程 2
- 判定来源分布：启发式初判 (22)
- 人工复核状态分布：未人工复核 (22)
- 高频软工主路径：3.3.2 运行时验证与运行时监测 (8) / 3.2.2 动态与混合分析 (1)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Abstract Monitors for Quantitative Specifications | Thomas A. Henzinger, Nicolas Mazzocchi, N. Ege Saraç | Abstract Quantitative monitoring can be universal and approximate: For every finite sequence of observations, the specification provides a value and the monitor outputs a best-effort approximation of it. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_11](https://doi.org/10.1007/978-3-031-17196-3_11) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_11) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_HenzingerMS22` |  |
| 2 | Anticipatory Recurrent Monitoring with Uncertainty and Assumptions | Hannes Kallwies, Martin Leucker, César Sánchez 0001, Torben Scheffel | Abstract Runtime Verification is a lightweight verification approach that aims at checking that a run of a system under observation adheres to a formal specification. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_10](https://doi.org/10.1007/978-3-031-17196-3_10) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_10) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_KallwiesLSS22` |  |
| 3 | AspectSol: A Solidity Aspect-Oriented Programming Tool with Applications in Runtime Verification | Shaun Azzopardi, Joshua Ellul, Ryan Falzon, Gordon J. Pace | 围绕《AspectSol: A Solidity Aspect-Oriented Programming Tool with Applications in Runtime Verification》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析；5.1.2 容错、韧性与恢复能力 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_13](https://doi.org/10.1007/978-3-031-17196-3_13) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_13) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_AzzopardiEFP22a` | 跨域 |
| 4 | Optimizing Prestate Copies in Runtime Verification of Function Postconditions | Jean-Christophe Filliâtre, Clément Pascutto | 围绕《Optimizing Prestate Copies in Runtime Verification of Function Postconditions》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析；5.1.2 容错、韧性与恢复能力 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_5](https://doi.org/10.1007/978-3-031-17196-3_5) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_5) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_FilliatreP22` | 跨域 |
| 5 | Relaxing Safety for Metric First-Order Temporal Logic via Dynamic Free Variables | Jonathan Julián Huerta y Munive | 围绕《Relaxing Safety for Metric First-Order Temporal Logic via Dynamic Free Variables》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_3](https://doi.org/10.1007/978-3-031-17196-3_3) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_3) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_Munive22` |  |
| 6 | Runtime Verification for FMI-Based Co-simulation | Anastasios Temperekidis, Nikolaos Kekatos, Panagiotis Katsaros | 围绕《Runtime Verification for FMI-Based Co-simulation》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 1.3.3 模型分析、仿真与验证；4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析 | X1=否; D1=2; D2=0; D3=2; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_19](https://doi.org/10.1007/978-3-031-17196-3_19) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_19) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_TemperekidisKK22` | 跨域 |
| 7 | Runtime Verification of Kotlin Coroutines | Denis Furian, Shaun Azzopardi, Yliès Falcone, Gerardo Schneider | 围绕《Runtime Verification of Kotlin Coroutines》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析；5.1.2 容错、韧性与恢复能力 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_12](https://doi.org/10.1007/978-3-031-17196-3_12) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_12) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_FurianAFS22` | 跨域 |
| 8 | Tainting in Smart Contracts: Combining Static and Runtime Verification | Shaun Azzopardi, Joshua Ellul, Ryan Falzon, Gordon J. Pace | 围绕《Tainting in Smart Contracts: Combining Static and Runtime Verification》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析；5.1.2 容错、韧性与恢复能力 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_8](https://doi.org/10.1007/978-3-031-17196-3_8) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_8) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_AzzopardiEFP22` | 跨域 |
| 9 | TeSSLa - An Ecosystem for Runtime Verification | Hannes Kallwies, Martin Leucker, Malte Schmitz 0001, Albert Schulz, Daniel Thoma, Alexander Weiss | Abstract Runtime verification deals with checking correctness properties on the runs of a system under scrutiny. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 4.4.4 持续 assurance 与运行时治理；2.3.2 构建工具链与开发环境；3.2.2 动态与混合分析 | X1=否; D1=2; D2=2; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_20](https://doi.org/10.1007/978-3-031-17196-3_20) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_20) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_KallwiesLSSTW22` | 跨域 |
| 10 | Towards Specificationless Monitoring of Provenance-Emitting Systems | Martin Stoffers, Alexander Weinert | 围绕《Towards Specificationless Monitoring of Provenance-Emitting Systems》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_14](https://doi.org/10.1007/978-3-031-17196-3_14) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_14) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2022:conf_rv_StoffersW22` |  |
| 11 | Real-Time Visualization of Stream-Based Monitoring Data | Jan Baumeister, Bernd Finkbeiner, Stefan Gumhold, Malte Schledjewski | Abstract Stream-based runtime monitors are used in safety-critical applications such as Unmanned Aerial Systems (UAS) to compute comprehensive statistics and logical assessments of system health that provide the human operator with critical information in hand | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_21](https://doi.org/10.1007/978-3-031-17196-3_21) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_21) | 🟡 保留观察 | 🟡 可选获取 | `CCF2022:conf_rv_BaumeisterFGS22` |  |
| 12 | A Barrier Certificate-Based Simplex Architecture with Application to Microgrids | Amol Damare, Shouvik Roy, Scott A. Smolka, Scott D. Stoller | 围绕《A Barrier Certificate-Based Simplex Architecture with Application to Microgrids》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_6](https://doi.org/10.1007/978-3-031-17196-3_6) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_6) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_DamareRSS22` |  |
| 13 | A Python Library for Trace Analysis | Dennis Dams, Klaus Havelund, Sean Kauffman | 围绕《A Python Library for Trace Analysis》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.2.2 动态与混合分析 | 3.3.2 运行时验证与运行时监测；4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_15](https://doi.org/10.1007/978-3-031-17196-3_15) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_15) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_DamsHK22` | 跨域 |
| 14 | Automated Surgical Procedure Assistance Framework Using Deep Learning and Formal Runtime Monitoring | Gaurav Gupta, Saumya Shankar, Srinivas Pinisetty | 围绕《Automated Surgical Procedure Assistance Framework Using Deep Learning and Formal Runtime Monitoring》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析；5.1.2 容错、韧性与恢复能力 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_2](https://doi.org/10.1007/978-3-031-17196-3_2) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_2) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_GuptaSP22` | 跨域 |
| 15 | Automating Numerical Parameters Along the Evolution of a Nonlinear System | Luca Geretti, Pieter Collins, Davide Bresolin, Tiziano Villa | 围绕《Automating Numerical Parameters Along the Evolution of a Nonlinear System》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_22](https://doi.org/10.1007/978-3-031-17196-3_22) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_22) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_GerettiCBV22` |  |
| 16 | Decent: A Benchmark for Decentralized Enforcement | Florian Gallay, Yliès Falcone | 围绕《Decent: A Benchmark for Decentralized Enforcement》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=1; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_18](https://doi.org/10.1007/978-3-031-17196-3_18) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_18) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_GallayF22` |  |
| 17 | Lock Contention Performance Classification for Java Intrinsic Locks | Nahid Hasan Khan, Joseph Robertson, Ramiro Liscano, Akramul Azim, Vijay Sundaresan, Yee-Kang Chang | 围绕《Lock Contention Performance Classification for Java Intrinsic Locks》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_16](https://doi.org/10.1007/978-3-031-17196-3_16) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_16) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_KhanRLASC22` |  |
| 18 | Optimal Finite-State Monitoring of Partial Traces | Peeyush Kushwaha, Rahul Purandare, Matthew B. Dwyer | 围绕《Optimal Finite-State Monitoring of Partial Traces》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_7](https://doi.org/10.1007/978-3-031-17196-3_7) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_7) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_KushwahaPD22` |  |
| 19 | Randomized First-Order Monitoring with Hashing | Joshua Schneider 0001 | 围绕《Randomized First-Order Monitoring with Hashing》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_1](https://doi.org/10.1007/978-3-031-17196-3_1) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_1) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_Schneider22` |  |
| 20 | Rule-Based Runtime Mitigation Against Poison Attacks on Neural Networks | Muhammad Usman 0024, Divya Gopinath, Youcheng Sun, Corina S. Pasareanu | 围绕《Rule-Based Runtime Mitigation Against Poison Attacks on Neural Networks》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_4](https://doi.org/10.1007/978-3-031-17196-3_4) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_4) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_UsmanGSP22` |  |
| 21 | TestSelector: Automatic Test Suite Selection for Student Projects | Filipe Marques, António Morgado 0001, José Fragoso Santos, Mikolás Janota | 围绕《TestSelector: Automatic Test Suite Selection for Student Projects》开展研究。 | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.3.2 运行时验证与运行时监测 | 4.4.4 持续 assurance 与运行时治理；5.1.1 故障预测与失效分析；5.1.2 容错、韧性与恢复能力 | X1=否; D1=2; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_17](https://doi.org/10.1007/978-3-031-17196-3_17) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_17) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_MarquesMSJ22` | 跨域 |
| 22 | Transaction Monitoring of Smart Contracts | Margarita Capretto, Martín Ceresa, César Sánchez 0001 | 围绕《Transaction Monitoring of Smart Contracts》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-17196-3_9](https://doi.org/10.1007/978-3-031-17196-3_9) | [link](https://link.springer.com/10.1007/978-3-031-17196-3_9) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2022:conf_rv_CaprettoCS22` |  |

## 6. 本 venue 年度观察

- 主题标签补充：运行时监测 (12) / 测试与验证 (8) / 形式化方法 (5) / 需求工程 (4) / 待人工细分 (4)
- 建议优先获取 `PDF` 的论文：`Abstract Monitors for Quantitative Specifications`；`Anticipatory Recurrent Monitoring with Uncertainty and Assumptions`；`AspectSol: A Solidity Aspect-Oriented Programming Tool with Applications in Runtime Verification`；`Optimizing Prestate Copies in Runtime Verification of Function Postconditions`；`Relaxing Safety for Metric First-Order Temporal Logic via Dynamic Free Variables`
