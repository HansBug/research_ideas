# `SCAM` (`2010`) 论文名录

## 1. 文件导航

- 年度总页：[../README.md](../README.md)
- 计数复核：[../verification.json](../verification.json)
- 数据文件：[metadata](../metadata/scam_conf_c.json)
- 近 `5` 年投稿时间线：[../../SUBMISSION_TIMELINES.md#timeline-scam_conf_c](../../SUBMISSION_TIMELINES.md#timeline-scam_conf_c)
- 说明：本页承载本 venue 的逐篇论文名录，并按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级从高到低排序。

## 2. 基本信息

- 全称：IEEE International Working Conference on Source Code Analysis and Manipulation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2010`
- 条目数：`21`
- 主体归属：软件工程
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：源码分析与变换 / 缺陷修复 / 程序理解邻近

## 3. 关键信息页面

- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/scam/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/5600365/proceeding / http://www.computer.org/csdl/proceedings/scam/2010/4178/00/index.html
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 一级总判定分布：软件工程 16 / 跨域/待判定 3 / 程序设计语言与形式化基础 2
- 软工纳入判定分布：属于软件工程 16 / 不属于软件工程 5
- 判定来源分布：启发式初判 (21)
- 人工复核状态分布：未人工复核 (21)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (6) / 2.2.2 模块化、依赖与解耦 (3) / 1.1.3 需求质量与歧义控制 (1) / 6.3.1 实验、案例研究与调查 (1) / 6.3.4 replication、benchmark 与开放科学 (1) / 4.1.5 技术债、克隆与可维护性治理 (1) / 4.2.4 克隆、相似性与理解支持 (1) / 4.1.1 缺陷修复与维护性修正 (1)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Reconstruction of Composite Types for Decompilation | Katerina Troshina, Yegor Derevenets, Alexander Chernov | Decompilation is reconstruction of a program in a high-level language from a program in a low-level language. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=1; D2=1; D3=0; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.24](https://doi.org/10.1109/scam.2010.24) | [link](http://ieeexplore.ieee.org/document/5601851/) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2010:conf_scam_TroshinaDC10` |  |
| 2 | Deriving Coupling Metrics from Call Graphs | Simon Allier, Stéphane Vaucher, Bruno Dufour, Houari A. Sahraoui | Coupling metrics play an important role in empirical software engineering research as well as in industrial measurement programs. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 2.2.2 模块化、依赖与解耦 | 3.2.1 静态分析与抽象解释；6.3.1 实验、案例研究与调查；3.2.2 动态与混合分析 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.25](https://doi.org/10.1109/scam.2010.25) | [link](http://ieeexplore.ieee.org/document/5601830/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_AllierVDS10` |  |
| 3 | Effective Static Analysis to Find Concurrency Bugs in Java | Zhi Da Luo, Linda Hillis, Raja Das, Yao Qi | Multithreading and concurrency are core features of the Java language. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.3 面向质量属性的分析；3.3.3 assurance、认证与合规验证；3.2.2 动态与混合分析 | X1=否; D1=2; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.20](https://doi.org/10.1109/scam.2010.20) | [link](http://ieeexplore.ieee.org/document/5601820/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_LuoHDQ10` |  |
| 4 | Encapsulating Software Platform Logic by Aspect-Oriented Programming: A Case Study in Using Aspects for Language Portability | Lennart C. L. Kats, Eelco Visser | Software platforms such as the Java Virtual Machine or the CLR. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 6.3.1 实验、案例研究与调查 | 1.3.2 模型转换、同步与协同；7.1.1 代码生成、补全与变换；8.3.3 系统之系统与互操作 | X1=否; D1=2; D2=1; D3=1; D4=1; venue=大部分属于软工; cross=是 | [10.1109/scam.2010.11](https://doi.org/10.1109/scam.2010.11) | [link](http://ieeexplore.ieee.org/document/5601821/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_KatsV10` | 跨域 |
| 5 | Estimating the Optimal Number of Latent Concepts in Source Code Analysis | Scott Grant, James R. Cordy | The optimal number of latent topics required to model the most accurate latent substructure for a source code corpus is an open question in source code analysis. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 6.3.4 replication、benchmark 与开放科学 | 3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析；3.2.3 面向质量属性的分析 | X1=否; D1=1; D2=2; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.22](https://doi.org/10.1109/scam.2010.22) | [link](http://ieeexplore.ieee.org/document/5601828/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_GrantC10` |  |
| 6 | Evaluating Code Clone Genealogies at Release Level: An Empirical Study | Ripon K. Saha, Muhammad Asaduzzaman, Minhaz F. Zibran, Chanchal K. Roy, Kevin A. Schneider | Code clone genealogies show how clone groups evolve with the evolution of the associated software system, and thus could provide important insights on the maintenance implications of clones. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 4.1.5 技术债、克隆与可维护性治理 | 6.3.1 实验、案例研究与调查；4.1.1 缺陷修复与维护性修正；4.1.2 重构、重模块化与代码清理 | X1=否; D1=2; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.32](https://doi.org/10.1109/scam.2010.32) | [link](http://ieeexplore.ieee.org/document/5601826/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_SahaAZRS10` |  |
| 7 | How Good is Static Analysis at Finding Concurrency Bugs? | Devin Kester, Martin Mwebesa, Jeremy S. Bradbury | Detecting bugs in concurrent software is challenging due to the many different thread interleavings. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；6.3.1 实验、案例研究与调查 | X1=否; D1=2; D2=1; D3=2; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.26](https://doi.org/10.1109/scam.2010.26) | [link](http://ieeexplore.ieee.org/document/5601822/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_KesterMB10` |  |
| 8 | Language-Independent Clone Detection Applied to Plagiarism Detection | Romain Brixtel, Mathieu Fontaine 0001, Boris Lesner, Cyril Bazin, Romain Robbes | Clone detection is usually applied in the context of detecting small-to medium scale fragments of duplicated code in large software systems. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 4.2.4 克隆、相似性与理解支持 | 7.1.4 AI 支持的架构、设计与工程决策；3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工; cross=是 | [10.1109/scam.2010.19](https://doi.org/10.1109/scam.2010.19) | [link](http://ieeexplore.ieee.org/document/5601829/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_BrixtelFLBR10` | 跨域 |
| 9 | Learning from 6, 000 Projects: Mining Models in the Large | Andreas Zeller | Models - abstract and simple descriptions of some artifact - are the backbone of all software engineering activities. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=1; D2=2; D3=1; D4=0; venue=大部分属于软工; cross=是 | [10.1109/scam.2010.23](https://doi.org/10.1109/scam.2010.23) | [link](http://ieeexplore.ieee.org/document/5601834/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_Zeller10` | 跨域 |
| 10 | MemSafe: Ensuring the Spatial and Temporal Memory Safety of C at Runtime | Matthew S. Simpson, Rajeev Barua | Memory access violations are a leading source of unreliability in C programs. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=大部分属于软工; PL=compiler | [10.1109/scam.2010.15](https://doi.org/10.1109/scam.2010.15) | [link](http://ieeexplore.ieee.org/document/5601849/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_SimpsonB10` |  |
| 11 | New Conceptual Coupling and Cohesion Metrics for Object-Oriented Systems | Bela Ujhazi, Rudolf Ferenc, Denys Poshyvanyk, Tibor Gyimóthy | The paper presents two novel conceptual metrics for measuring coupling and cohesion in software systems. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 2.2.2 模块化、依赖与解耦 | 3.2.3 面向质量属性的分析；3.3.3 assurance、认证与合规验证；3.2.1 静态分析与抽象解释 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工; cross=是 | [10.1109/scam.2010.14](https://doi.org/10.1109/scam.2010.14) | [link](http://ieeexplore.ieee.org/document/5601833/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_UjhaziFPG10` | 跨域 |
| 12 | Parallel Reachability and Escape Analyses | Marcus Edvinsson, Jonas Lundberg, Welf Löwe | Static program analysis usually consists of a number of steps, each producing partial results. | 跨域/待判定 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.10](https://doi.org/10.1109/scam.2010.10) | [link](http://ieeexplore.ieee.org/document/5601823/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_EdvinssonLL10` |  |
| 13 | Recovering the Memory Behavior of Executable Programs | Alain Ketterlin, Philippe Clauss | This paper deals with the binary analysis of executable programs, with the goal of understanding how they access memory. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.18](https://doi.org/10.1109/scam.2010.18) | [link](http://ieeexplore.ieee.org/document/5601848/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_KetterlinC10` |  |
| 14 | Refactoring Support for Modularity Maintenance in Erlang | Huiqing Li, Simon J. Thompson | Low coupling between modules and high cohesion inside each module are key features of good software architecture. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 2.2.2 模块化、依赖与解耦 | 4.1.1 缺陷修复与维护性修正；4.1.2 重构、重模块化与代码清理；3.2.3 面向质量属性的分析 | X1=否; D1=3; D2=2; D3=1; D4=0; venue=大部分属于软工 | [10.1109/scam.2010.17](https://doi.org/10.1109/scam.2010.17) | [link](http://ieeexplore.ieee.org/document/5601817/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_LiT10` |  |
| 15 | Speeding Up Context-, Object- and Field-Sensitive SDG Generation | Jürgen Graf 0001 | System dependence graphs (SDGs) are an established tool for precise interprocedural program analysis. | 跨域/待判定 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=大部分属于软工 | [10.1109/scam.2010.9](https://doi.org/10.1109/scam.2010.9) | [link](http://ieeexplore.ieee.org/document/5601825/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_Graf10` |  |
| 16 | Subclass Instantiation Distribution | Amy Wheeler, Dave W. Binkley | During execution, an objected-oriented program typically creates a large number of objects. | 跨域/待判定 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=2; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.12](https://doi.org/10.1109/scam.2010.12) | [link](http://ieeexplore.ieee.org/document/5601832/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_WheelerB10` |  |
| 17 | The Fika Parser Generator | Michael Píse | Parser generators automate conversion of a context-free grammar into an executable parser and therefore increase developers' productivity. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=大部分属于软工; PL=parser | [10.1109/scam.2010.27](https://doi.org/10.1109/scam.2010.27) | [link](http://ieeexplore.ieee.org/document/5601827/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_Pise10` |  |
| 18 | Validating the Use of Topic Models for Software Evolution | Stephen W. Thomas, Bram Adams, Ahmed E. Hassan, Dorothea Blostein | Topics are collections of words that co-occur frequently in a text corpus. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 4.1.1 缺陷修复与维护性修正 | 6.3.4 replication、benchmark 与开放科学；6.3.1 实验、案例研究与调查；3.2.1 静态分析与抽象解释 | X1=否; D1=2; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2010.13](https://doi.org/10.1109/scam.2010.13) | [link](http://ieeexplore.ieee.org/document/5601831/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_ThomasAHB10` |  |
| 19 | Visualization of C++ Template Metaprograms | Zoltan Borok-Nagy, Viktor Majer, József Mihalicza, Norbert Pataki, Zoltán Porkoláb | Template metaprograms have become an essential part of today's C++ programs: with proper template definitions we can force the C++ compiler to execute algorithms at compilation time. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.3 面向质量属性的分析 | 3.3.3 assurance、认证与合规验证；3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析 | X1=否; D1=1; D2=1; D3=1; D4=0; venue=大部分属于软工; cross=是 | [10.1109/scam.2010.16](https://doi.org/10.1109/scam.2010.16) | [link](http://ieeexplore.ieee.org/document/5601850/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_scam_Borok-NagyMMPP10` | 跨域 |
| 20 | AMBIDEXTER: Practical Ambiguity Detection | Bas Basten, Tijs van der Storm | Ambiguity detection tools try to statically track down ambiguities in context-free grammars. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 1.1.3 需求质量与歧义控制 | 3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析；3.2.3 面向质量属性的分析 | X1=否; D1=2; D2=1; D3=0; D4=0; venue=大部分属于软工 | [10.1109/scam.2010.21](https://doi.org/10.1109/scam.2010.21) | [link](http://ieeexplore.ieee.org/document/5601824/) | ⚪ 暂不跟进 | ⚪ 暂不获取 | `CCF2010:conf_scam_BastenS10` |  |
| 21 | Why Source Code Analysis and Manipulation Will Always be Important | Mark Harman | This paper makes a case for Source Code Analysis and Manipulation. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=1; D2=1; D3=0; D4=0; venue=大部分属于软工 | [10.1109/scam.2010.28](https://doi.org/10.1109/scam.2010.28) | [link](http://ieeexplore.ieee.org/document/5601835/) | ⚪ 暂不跟进 | ⚪ 暂不获取 | `CCF2010:conf_scam_Harman10` |  |

## 6. 本 venue 年度观察

- 主题标签补充：经验软件工程 (8) / 程序分析 (7) / 可靠性/安全 (6) / 建模/模型驱动 (5) / 测试与验证 (5)
- 建议优先获取 `PDF` 的论文：`Reconstruction of Composite Types for Decompilation`
