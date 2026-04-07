# `SCAM` (`2017`) 论文名录

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
- 年份：`2017`
- 条目数：`18`
- 主体归属：软件工程
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：源码分析与变换 / 缺陷修复 / 程序理解邻近

## 3. 关键信息页面

- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/scam/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8089459/proceeding / https://www.computer.org/csdl/proceedings/scam/2017/3238/00/index.html
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 一级总判定分布：软件工程 14 / 跨域/待判定 4
- 软工纳入判定分布：属于软件工程 14 / 不属于软件工程 4
- 判定来源分布：启发式初判 (18)
- 人工复核状态分布：未人工复核 (18)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (6) / 4.1.1 缺陷修复与维护性修正 (3) / 3.1.4 场景化测试 (1) / 7.1.2 AI 支持的测试、分析与修复 (1) / 6.3.4 replication、benchmark 与开放科学 (1) / 3.2.3 面向质量属性的分析 (1) / 3.3.4 基准、工具评测与可复现验证 (1)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | An Exploratory Study of Functional Redundancy in Code Repositories | Marcelo Suzuki, Adriano Carvalho de Paula, Eduardo Guerra 0001, Cristina V. Lopes, Otávio Augusto Lazzarini Lemos | In large code repositories, the probability of functions to repeat across projects is high. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 7.1.2 AI 支持的测试、分析与修复 | 3.2.4 分析驱动的理解、重构与综合；3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.21](https://doi.org/10.1109/scam.2017.21) | [link](https://ieeexplore.ieee.org/document/8090136/) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2017:conf_scam_SuzukiPGLL17` |  |
| 2 | Extracting Timed Automata from Java Methods | Giovanni Liva, Muhammad Taimoor Khan 0001, Martin Pinzger 0001 | The verification of the time behavior in distributed, multi-threaded programs is challenging, mainly because modern programming languages only provide means to represent time without a proper semantics. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=1; D2=2; D3=1; D4=1; venue=大部分属于软工; cross=是 | [10.1109/scam.2017.9](https://doi.org/10.1109/scam.2017.9) | [link](http://ieeexplore.ieee.org/document/8090142/) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2017:conf_scam_LivaKP17` | 跨域 |
| 3 | Supporting Analysis of SQL Queries in PHP AiR | David Anderson, Mark Hills 0001 | The code behind dynamic webpages often includes calls to database libraries, with queries formed using a combination of static text and values computed at runtime. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.3 面向质量属性的分析 | 1.3.2 模型转换、同步与协同；7.1.1 代码生成、补全与变换；3.3.3 assurance、认证与合规验证 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.23](https://doi.org/10.1109/scam.2017.23) | [link](http://ieeexplore.ieee.org/document/8090149/) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2017:conf_scam_Anderson017` |  |
| 4 | Tree-Oriented vs. Line-Oriented Observation-Based Slicing | David W. Binkley, Nicolas Gold, Syed S. Islam, Jens Krinke, Shin Yoo | Observation-based slicing is a recently-introduced, language-independent slicing technique based on the dependencies observable from program behavior. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.3.4 基准、工具评测与可复现验证 | 3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析；3.2.3 面向质量属性的分析 | X1=否; D1=1; D2=2; D3=1; D4=0; venue=大部分属于软工 | [10.1109/scam.2017.11](https://doi.org/10.1109/scam.2017.11) | [link](http://ieeexplore.ieee.org/document/8090135/) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2017:conf_scam_BinkleyGIKY17` |  |
| 5 | Working Around Loops for Infeasible Path Detection in Binary Programs | Jordy Ruiz, Hugues Cassé, Marianne De Michiel | The research of a safe Worst-Case Execution Time (WCET) estimation is necessary to build reliable hard, critical real-time systems. | 跨域/待判定 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=0; venue=大部分属于软工 | [10.1109/scam.2017.13](https://doi.org/10.1109/scam.2017.13) | [link](https://ieeexplore.ieee.org/document/8090133/) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2017:conf_scam_RuizCM17` |  |
| 6 | A Methodology for Relating Software Structure with Energy Consumption | Abdul Ali Bangash, Hareem Sahar, Mirza Omer Beg | With the widespread use of mobile devices relying on limited battery power, the burden of optimizing applications for energy has shifted towards the application developers. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.1.4 场景化测试 | 6.4.3 度量、预测与风险模型；3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.18](https://doi.org/10.1109/scam.2017.18) | [link](http://ieeexplore.ieee.org/document/8090144/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_BangashSB17` |  |
| 7 | A Static Code Smell Detector for SQL Queries Embedded in Java Code | Csaba Nagy 0001, Anthony Cleve | A database plays a central role in the architecture of an information system, and the way it stores the data delimits its main features. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.3 面向质量属性的分析；3.3.3 assurance、认证与合规验证；3.2.2 动态与混合分析 | X1=否; D1=1; D2=2; D3=1; D4=0; venue=大部分属于软工; cross=是 | [10.1109/scam.2017.19](https://doi.org/10.1109/scam.2017.19) | [link](http://ieeexplore.ieee.org/document/8090148/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_NagyC17` | 跨域 |
| 8 | Automatically Adding Missing Libraries to Java Projects to Foster Better Results from Static Analysis | Thomas Atzenhofer, Reinhold Plösch | The measurement of software quality, including the preparation and management of the necessary resources and libraries, is a major challenge in continuous software quality measurement and assessment. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 1.2.3 规约质量与一致性；3.2.2 动态与混合分析；3.2.3 面向质量属性的分析 | X1=否; D1=2; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.10](https://doi.org/10.1109/scam.2017.10) | [link](http://ieeexplore.ieee.org/document/8090147/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_AtzenhoferP17` |  |
| 9 | Contextual Recommendation of Relevant Program Elements in an Interactive Feature Location Process | Jinshui Wang, Xin Peng 0001, Zhenchang Xing, Kun Fu, Wenyun Zhao | When performing feature location tasks, developers often need to explore a large number of program elements by following a variety of clues (such as program element location, dependency, and content). | 跨域/待判定 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.14](https://doi.org/10.1109/scam.2017.14) | [link](http://ieeexplore.ieee.org/document/8090139/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_WangPXFZ17` |  |
| 10 | Detecting Security Vulnerabilities in Object-Oriented PHP Programs | Mona Nashaat, Karim Ali 0001, James Miller 0001 | PHP is one of the most popular web development tools in use today. | 跨域/待判定 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.20](https://doi.org/10.1109/scam.2017.20) | [link](https://ieeexplore.ieee.org/document/8090150/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_NashaatAM17` |  |
| 11 | Does the Choice of Configuration Framework Matter for Developers? Empirical Study on 11 Java Configuration Frameworks | Mohammed Sayagh, Zhen Dong 0004, Artur Andrzejak 0001, Bram Adams | Configuration frameworks are routinely used in software systems to change application behavior without recompilation. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 4.1.1 缺陷修复与维护性修正 | 6.3.1 实验、案例研究与调查；3.2.3 面向质量属性的分析；6.4.1 代码、提交、issue 与 PR 挖掘 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.25](https://doi.org/10.1109/scam.2017.25) | [link](http://ieeexplore.ieee.org/document/8090137/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_SayaghDAA17` |  |
| 12 | Harvesting the Wisdom of the Crowd to Infer Method Nullness in Java | Manuel Leuenberger, Haidar Osman, Mohammad Ghafari, Oscar Nierstrasz | Null pointer exceptions are common bugs in Java projects. | 跨域/待判定 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.22](https://doi.org/10.1109/scam.2017.22) | [link](http://ieeexplore.ieee.org/document/8090140/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_LeuenbergerOGN17` |  |
| 13 | How do Scratch Programmers Name Variables and Procedures? | Alaaeddin Swidan, Alexander Serebrenik, Felienne Hermans | Research shows the importance of selecting good names to identifiers in software code: more meaningful names improve readability. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 6.3.4 replication、benchmark 与开放科学 | 2.2.1 设计原则、模式与反模式；3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.12](https://doi.org/10.1109/scam.2017.12) | [link](http://ieeexplore.ieee.org/document/8090138/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_SwidanSH17` |  |
| 14 | Investigating the Use of Code Analysis and NLP to Promote a Consistent Usage of Identifiers | Bin Lin 0008, Simone Scalabrino, Andrea Mocci, Rocco Oliveto, Gabriele Bavota, Michele Lanza 0001 | Meaningless identifiers as well as inconsistent use of identifiers in the source code might hinder code readability and result in increased software maintenance efforts. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 4.1.1 缺陷修复与维护性修正；4.1.2 重构、重模块化与代码清理；6.3.1 实验、案例研究与调查 | X1=否; D1=1; D2=1; D3=2; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.17](https://doi.org/10.1109/scam.2017.17) | [link](http://ieeexplore.ieee.org/document/8090141/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_0008SMOBL17` |  |
| 15 | On the Relationships Between Stability and Bug-Proneness of Code Clones: An Empirical Study | Md. Saidur Rahman 0002, Chanchal K. Roy | Exact or similar copies of code fragments in a code base are known as code clones. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 4.1.1 缺陷修复与维护性修正 | 6.3.1 实验、案例研究与调查；3.2.3 面向质量属性的分析；3.3.3 assurance、认证与合规验证 | X1=否; D1=1; D2=1; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.26](https://doi.org/10.1109/scam.2017.26) | [link](http://ieeexplore.ieee.org/document/8090146/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_RahmanR17` |  |
| 16 | Revisiting Exception Handling Practices with Exception Flow Analysis | Guilherme B. de Pádua, Weiyi Shang | Modern programming languages, such as Java and C#, typically provide features that handle exceptions. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 4.1.1 缺陷修复与维护性修正 | 3.2.3 面向质量属性的分析；6.3.1 实验、案例研究与调查；3.3.3 assurance、认证与合规验证 | X1=否; D1=1; D2=2; D3=1; D4=1; venue=大部分属于软工 | [10.1109/scam.2017.16](https://doi.org/10.1109/scam.2017.16) | [link](https://ieeexplore.ieee.org/document/8090134/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_PaduaS17` |  |
| 17 | Security Smells in Android | Mohammad Ghafari, Pascal Gadient, Oscar Nierstrasz | The ubiquity of smartphones, and their very broad capabilities and usage, make the security of these devices tremendously important. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.3 面向质量属性的分析；3.3.3 assurance、认证与合规验证；3.2.2 动态与混合分析 | X1=否; D1=1; D2=1; D3=1; D4=0; venue=大部分属于软工 | [10.1109/scam.2017.24](https://doi.org/10.1109/scam.2017.24) | [link](http://ieeexplore.ieee.org/document/8090145/) | 🟡 保留观察 | 🟡 可选获取 | `CCF2017:conf_scam_GhafariGN17` |  |
| 18 | Towards Better Symbol Resolution for C/C++ Programs: A Cluster-Based Solution | Richárd Szalay, Zoltán Porkoláb, Dániel Krupp | Resolving symbol references is an important part of many application areas from development environments to various static analyser tools, especially when it is used for code comprehension purposes. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=1; D2=1; D3=0; D4=1; venue=大部分属于软工; cross=是 | [10.1109/scam.2017.15](https://doi.org/10.1109/scam.2017.15) | [link](http://ieeexplore.ieee.org/document/8090143/) | ⚪ 暂不跟进 | ⚪ 暂不获取 | `CCF2017:conf_scam_SzalayPK17` | 跨域 |

## 6. 本 venue 年度观察

- 主题标签补充：可靠性/安全 (8) / 经验软件工程 (8) / 程序分析 (7) / 维护与演化 (6) / 建模/模型驱动 (4)
- 建议优先获取 `PDF` 的论文：`An Exploratory Study of Functional Redundancy in Code Repositories`；`Extracting Timed Automata from Java Methods`；`Supporting Analysis of SQL Queries in PHP AiR`；`Tree-Oriented vs. Line-Oriented Observation-Based Slicing`；`Working Around Loops for Infeasible Path Detection in Binary Programs`
