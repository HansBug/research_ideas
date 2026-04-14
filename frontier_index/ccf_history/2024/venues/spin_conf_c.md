# `SPIN` (`2024`) 论文名录

## 1. 文件导航

- 年度总页：[../README.md](../README.md)
- 计数复核：[../verification.json](../verification.json)
- 数据文件：[metadata](../metadata/spin_conf_c.json)
- 近 `5` 年投稿时间线：[../../SUBMISSION_TIMELINES.md#timeline-spin_conf_c](../../SUBMISSION_TIMELINES.md#timeline-spin_conf_c)
- 说明：本页承载本 venue 的逐篇论文名录，并按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级从高到低排序。

## 2. 基本信息

- 全称：International Symposium on Model Checking of Software
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`14`
- 主体归属：形式化方法与软件工程交叉
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件模型检查 / state-based verification / `UPPAAL` 邻近

## 3. 关键信息页面

- 年主页：https://spin-web.github.io/SPIN2024/
- 学术索引页：http://dblp.uni-trier.de/db/conf/spin/index.html
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 一级总判定分布：软件工程 7 / 程序设计语言与形式化基础 7
- 软工纳入判定分布：不属于软件工程 7 / 属于软件工程 5 / 跨域但软工主导 2
- 判定来源分布：启发式初判 (14)
- 人工复核状态分布：未人工复核 (14)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (3) / 1.3.3 模型分析、仿真与验证 (3) / 1.3.1 建模语言与元模型 (1)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Augmenting Interpolation-Based Model Checking with Auxiliary Invariants | Dirk Beyer 0001, Po-Chun Chien, Nian-Ze Lee | Abstract Software model checking is a challenging problem, and generating relevant invariants is a key factor in proving the safety properties of a program. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.3.1 面向软工问题的形式化验证 | 1.2.1 形式化规约与契约；1.3.3 模型分析、仿真与验证；3.2.1 静态分析与抽象解释 | X1=否; D1=2; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_13](https://doi.org/10.1007/978-3-031-66149-5_13) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_13) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_BeyerCL24` | 跨域 |
| 2 | Fault Localization on Verification Witnesses | Dirk Beyer 0001, Matthias Kettl, Thomas Lemberger 0002 | Abstract When verifiers report an alarm, they export a violation witness (exchangeable counterexample) that helps validate the reachability of that alarm. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_12](https://doi.org/10.1007/978-3-031-66149-5_12) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_12) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_BeyerKL24` |  |
| 3 | Learning the State Machine Behind a Modal Text Editor: The (Neo)Vim Case Study | Pierre Ganty | 围绕《Learning the State Machine Behind a Modal Text Editor: The (Neo)Vim Case Study》开展研究。 | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 1.3.1 建模语言与元模型 | 6.3.1 实验、案例研究与调查；1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性 | X1=否; D1=2; D2=1; D3=1; D4=1; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_9](https://doi.org/10.1007/978-3-031-66149-5_9) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_9) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_Ganty24` | 跨域 |
| 4 | MoXI: An Intermediate Language for Symbolic Model Checking | Kristin Yvonne Rozier, Rohit Dureja, Ahmed Irfan, Chris Johannsen, Karthik Nukala, Natarajan Shankar, Cesare Tinelli, Moshe Y. Vardi | 围绕《MoXI: An Intermediate Language for Symbolic Model Checking》开展研究。 | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 1.3.3 模型分析、仿真与验证 | 3.3.1 面向软工问题的形式化验证；1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性 | X1=否; D1=2; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_2](https://doi.org/10.1007/978-3-031-66149-5_2) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_2) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_RozierDIJNSTV24` | 跨域 |
| 5 | Software Verification Witnesses 2.0 | Paulína Ayaziová, Dirk Beyer 0001, Marian Lingsch Rosenfeld, Martin Spiessl, Jan Strejcek | Abstract Verification witnesses are now widely accepted objects used not only to confirm or refute verification results, but also for general exchange of information among various tools for program verification. | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.1 面向软工问题的形式化验证 | 4.3.1 版本、配置与构建工程；1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_11](https://doi.org/10.1007/978-3-031-66149-5_11) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_11) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_AyaziovaBRSS24` | 跨域 |
| 6 | Synchronisation in Language-Level Symmetry Reduction for Probabilistic Model Checking | Ivaylo Valkov, Alastair F. Donaldson, Alice Miller 0001 | 围绕《Synchronisation in Language-Level Symmetry Reduction for Probabilistic Model Checking》开展研究。 | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 1.3.3 模型分析、仿真与验证 | 3.3.1 面向软工问题的形式化验证；1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性 | X1=否; D1=2; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_3](https://doi.org/10.1007/978-3-031-66149-5_3) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_3) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_ValkovDM24` | 跨域 |
| 7 | Test-Case Generation with Automata-Based Software Model Checking | Max Barth, Marie-Christine Jakobs | 围绕《Test-Case Generation with Automata-Based Software Model Checking》开展研究。 | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 1.3.3 模型分析、仿真与验证 | 3.3.1 面向软工问题的形式化验证；1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性 | X1=否; D1=2; D2=1; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_14](https://doi.org/10.1007/978-3-031-66149-5_14) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_14) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_BarthJ24` | 跨域 |
| 8 | Two Decades of Industrializing Formal Verification: The Reactis Story | Rance Cleaveland, David Hansel, Steve Sims, Scott A. Smolka | 围绕《Two Decades of Industrializing Formal Verification: The Reactis Story》开展研究。 | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.3.1 面向软工问题的形式化验证 | 1.2.1 形式化规约与契约；1.2.2 自然语言到规约/属性；1.2.3 规约质量与一致性 | X1=否; D1=2; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_5](https://doi.org/10.1007/978-3-031-66149-5_5) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_5) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2024:conf_spin_CleavelandHSS24` | 跨域 |
| 9 | A Hypergraph-Based Formalization of Hierarchical Reactive Modules and a Compositional Verification Method | Daisuke Ishii | 围绕《A Hypergraph-Based Formalization of Hierarchical Reactive Modules and a Compositional Verification Method》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_4](https://doi.org/10.1007/978-3-031-66149-5_4) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_4) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2024:conf_spin_Ishii24` |  |
| 10 | Automated Reasoning in Quantum Circuit Compilation | Dimitrios Thanos, Alejandro Villoria, Sebastiaan Brand, Arend-Jan Quist, Jingyi Mei, Tim Coopmans, Alfons Laarman | 围绕《Automated Reasoning in Quantum Circuit Compilation》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是; PL=compilation; SYS=quantum circuit; OTHER=circuit | [10.1007/978-3-031-66149-5_6](https://doi.org/10.1007/978-3-031-66149-5_6) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_6) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2024:conf_spin_ThanosVBQMCL24` |  |
| 11 | Random Access on Narrow Decision Diagrams in External Memory | Steffan Christ Sølvsten, Casper Moldrup Rysgaard, Jaco van de Pol | 围绕《Random Access on Narrow Decision Diagrams in External Memory》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_7](https://doi.org/10.1007/978-3-031-66149-5_7) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_7) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2024:conf_spin_SolvstenRP24` |  |
| 12 | Solving Constrained Horn Clauses as C Programs with CHC2C | Levente Bajczi, Vince Molnár | 围绕《Solving Constrained Horn Clauses as C Programs with CHC2C》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_8](https://doi.org/10.1007/978-3-031-66149-5_8) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_8) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2024:conf_spin_BajcziM24` |  |
| 13 | Taming the AI Monster: Monitoring of Individual Fairness for Effective Human Oversight | Kevin Baum 0001, Sebastian Biewer, Holger Hermanns, Sven Hetmank, Markus Langer, Anne Lauber-Rönsberg, Sarah Sterz | 围绕《Taming the AI Monster: Monitoring of Individual Fairness for Effective Human Oversight》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_1](https://doi.org/10.1007/978-3-031-66149-5_1) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_1) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2024:conf_spin_BaumBHHLLS24` |  |
| 14 | Tolerange: Quantifying Fault Masking in Stochastic Systems | Luciano Putruele, Ramiro Demasi, Pablo F. Castro, Pedro R. D&apos;Argenio | 围绕《Tolerange: Quantifying Fault Masking in Stochastic Systems》开展研究。 | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1007/978-3-031-66149-5_10](https://doi.org/10.1007/978-3-031-66149-5_10) | [link](https://link.springer.com/10.1007/978-3-031-66149-5_10) | ⏳ 待补信息 | ⏳ 未判断 | `CCF2024:conf_spin_PutrueleDCD24` |  |

## 6. 本 venue 年度观察

- 主题标签补充：测试与验证 (6) / 形式化方法 (6) / 建模/模型驱动 (5) / 待人工细分 (3) / 维护与演化 (2)
- 建议优先获取 `PDF` 的论文：`Augmenting Interpolation-Based Model Checking with Auxiliary Invariants`；`Fault Localization on Verification Witnesses`；`Learning the State Machine Behind a Modal Text Editor: The (Neo)Vim Case Study`；`MoXI: An Intermediate Language for Symbolic Model Checking`；`Software Verification Witnesses 2.0`
