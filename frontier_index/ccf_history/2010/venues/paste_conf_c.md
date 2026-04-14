# `PASTE` (`2010`) 论文名录

## 1. 文件导航

- 年度总页：[../README.md](../README.md)
- 计数复核：[../verification.json](../verification.json)
- 数据文件：[metadata](../metadata/paste_conf_c.json)
- 近 `5` 年投稿时间线：[../../SUBMISSION_TIMELINES.md#timeline-paste_conf_c](../../SUBMISSION_TIMELINES.md#timeline-paste_conf_c)
- 说明：本页承载本 venue 的逐篇论文名录，并按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级从高到低排序。

## 2. 基本信息

- 全称：ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2010`
- 条目数：`12`
- 主体归属：程序设计语言与形式化基础
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近

## 3. 关键信息页面

- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/paste/
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (6) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 一级总判定分布：程序设计语言与形式化基础 8 / 软件工程 3 / 系统软件 1
- 软工纳入判定分布：不属于软件工程 9 / 属于软件工程 2 / 跨域但软工主导 1
- 判定来源分布：启发式初判 (12)
- 人工复核状态分布：未人工复核 (12)
- 高频软工主路径：3.2.2 动态与混合分析 (2) / 3.2.1 静态分析与抽象解释 (1)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Learning universal probabilistic models for fault localization | Min Feng 0001, Rajiv Gupta 0001 | Recently there has been significant interest in employing probabilistic techniques for fault localization. | 系统软件 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=1; D4=0; venue=部分属于软工; SYS=inference | [10.1145/1806672.1806688](https://doi.org/10.1145/1806672.1806688) | [link](https://dl.acm.org/doi/10.1145/1806672.1806688) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2010:conf_paste_FengG10` |  |
| 2 | Opportunities for concurrent dynamic analysis with explicit inter-core communication | Jungwoo Ha, Stephen P. Crago | Multicore is now the dominant processor trend, and the number of cores is rapidly increasing. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.2 动态与混合分析 | 3.4.1 调试、分诊与根因分析；3.2.1 静态分析与抽象解释；3.2.3 面向质量属性的分析 | X1=否; D1=2; D2=1; D3=2; D4=0; venue=部分属于软工; cross=是 | [10.1145/1806672.1806676](https://doi.org/10.1145/1806672.1806676) | [link](https://dl.acm.org/doi/10.1145/1806672.1806676) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2010:conf_paste_HaC10` | 跨域 |
| 3 | Towards a unified fault-detection benchmark | Suzanna Schmeelk | Developing a unified benchmark to compare and contrast ways to detect faults is an important aspect for the future of fault detection. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=2; D3=1; D4=1; venue=部分属于软工 | [10.1145/1806672.1806684](https://doi.org/10.1145/1806672.1806684) | [link](https://dl.acm.org/doi/10.1145/1806672.1806684) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2010:conf_paste_Schmeelk10` |  |
| 4 | Coherent dependence clusters | Syed S. Islam, Jens Krinke, David W. Binkley, Mark Harman | Large clusters of mutual dependence can cause problems for comprehension, testing and maintenance. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=部分属于软工 | [10.1145/1806672.1806683](https://doi.org/10.1145/1806672.1806683) | [link](https://dl.acm.org/doi/10.1145/1806672.1806683) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_paste_IslamKBH10` |  |
| 5 | Expect the unexpected: error code mismatches between documentation and the real world | Cindy Rubio-González, Ben Liblit | Inaccurate documentation can mislead programmers and cause software to fail in unexpected ways. | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 3.2.1 静态分析与抽象解释 | 3.2.2 动态与混合分析；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=2; D2=0; D3=1; D4=1; venue=部分属于软工; cross=是 | [10.1145/1806672.1806687](https://doi.org/10.1145/1806672.1806687) | [link](https://dl.acm.org/doi/10.1145/1806672.1806687) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_paste_Rubio-GonzalezL10` | 跨域 |
| 6 | Extracting compiler provenance from program binaries | Nathan E. Rosenblum, Barton P. Miller, Xiaojin Zhu 0001 | We present a novel technique that identifies the source compiler of program binaries, an important element of program provenance. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=1; D3=2; D4=1; venue=部分属于软工; PL=compiler | [10.1145/1806672.1806678](https://doi.org/10.1145/1806672.1806678) | [link](https://dl.acm.org/doi/10.1145/1806672.1806678) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_paste_RosenblumMZ10` |  |
| 7 | Null dereference analysis in practice | Nathaniel Ayewah, William W. Pugh | Many analysis techniques have been proposed to determine when a potentially null value may be dereferenced. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=1; D3=1; D4=0; venue=部分属于软工; PL=type system | [10.1145/1806672.1806686](https://doi.org/10.1145/1806672.1806686) | [link](https://dl.acm.org/doi/10.1145/1806672.1806686) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_paste_AyewahP10` |  |
| 8 | Property-aware program sampling | Harish Narayanappa, Mukul S. Bansal, Hridesh Rajan | Monitoring or profiling programs provides us with an understanding for its further improvement and analysis. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工 | [10.1145/1806672.1806682](https://doi.org/10.1145/1806672.1806682) | [link](https://dl.acm.org/doi/10.1145/1806672.1806682) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_paste_NarayanappaBR10` |  |
| 9 | The RoadRunner dynamic analysis framework for concurrent programs | Cormac Flanagan, Stephen N. Freund | RoadRunner is a dynamic analysis framework designed to facilitate rapid prototyping and experimentation with dynamic analyses for concurrent Java programs. | 软件工程 | 属于软件工程 | 启发式初判 | 未人工复核 | 3.2.2 动态与混合分析 | 3.2.1 静态分析与抽象解释；3.2.3 面向质量属性的分析；3.2.4 分析驱动的理解、重构与综合 | X1=否; D1=2; D2=2; D3=1; D4=0; venue=部分属于软工; cross=是 | [10.1145/1806672.1806674](https://doi.org/10.1145/1806672.1806674) | [link](https://dl.acm.org/doi/10.1145/1806672.1806674) | 🟡 保留观察 | 🟡 可选获取 | `CCF2010:conf_paste_FlanaganF10` | 跨域 |
| 10 | Interprocedural induction variable analysis based on interprocedural SSA form IR | Silvian Calman, Jianwen Zhu | The induction variable analysis is a fundamental component of loop optimizations in compilers. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=0; D4=0; venue=部分属于软工 | [10.1145/1806672.1806680](https://doi.org/10.1145/1806672.1806680) | [link](https://dl.acm.org/doi/10.1145/1806672.1806680) | ⚪ 暂不跟进 | ⚪ 暂不获取 | `CCF2010:conf_paste_CalmanZ10` |  |
| 11 | Packrat parsers can handle practical grammars in mostly constant space | Kota Mizushima, Atusi Maeda, Yoshinori Yamaguchi | Packrat parsing is a powerful parsing algorithm presented by Ford in 2002. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工; PL=parser | [10.1145/1806672.1806679](https://doi.org/10.1145/1806672.1806679) | [link](https://dl.acm.org/doi/10.1145/1806672.1806679) | ⚪ 暂不跟进 | ⚪ 暂不获取 | `CCF2010:conf_paste_MizushimaMY10` |  |
| 12 | Visualizing threads, transactions and tasks | Steven P. Reiss, Suman Karumuri | Modern systems, particularly servers, involve multiple threads dealing with multiple incoming transactions using either implicit or explicit internal tasks. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=0; D4=0; venue=部分属于软工 | [10.1145/1806672.1806675](https://doi.org/10.1145/1806672.1806675) | [link](https://dl.acm.org/doi/10.1145/1806672.1806675) | ⚪ 暂不跟进 | ⚪ 暂不获取 | `CCF2010:conf_paste_ReissK10` |  |

## 6. 本 venue 年度观察

- 主题标签补充：程序分析 (5) / 测试与验证 (4) / 维护与演化 (3) / 程序修复 (2) / 建模/模型驱动 (2)
- 建议优先获取 `PDF` 的论文：`Learning universal probabilistic models for fault localization`；`Opportunities for concurrent dynamic analysis with explicit inter-core communication`；`Towards a unified fault-detection benchmark`
