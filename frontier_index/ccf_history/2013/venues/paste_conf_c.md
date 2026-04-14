# `PASTE` (`2013`) 论文名录

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
- 年份：`2013`
- 条目数：`7`
- 主体归属：程序设计语言与形式化基础
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近

## 3. 关键信息页面

- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/paste/
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (4) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 一级总判定分布：程序设计语言与形式化基础 5 / 系统软件 2
- 软工纳入判定分布：不属于软件工程 7
- 判定来源分布：启发式初判 (7)
- 人工复核状态分布：未人工复核 (7)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Automated inference of atomic sets for safe concurrent execution | Peter Dinges, Minas Charalambides, Gul Agha | Atomic sets are a synchronization mechanism in which the programmer specifies the groups of data that must be accessed as a unit. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工; PL=compiler; SYS=inference | [10.1145/2462029.2462030](https://doi.org/10.1145/2462029.2462030) | [link](https://dl.acm.org/doi/10.1145/2462029.2462030) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2013:conf_paste_DingesCA13` |  |
| 2 | ShadowData: shadowing heap objects in Java | Matej Vitásek, Walter Binder, Matthias Hauswirth | In this paper we compare different approaches to maintain shadow state for heap objects in Java. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=1; D3=1; D4=0; venue=部分属于软工 | [10.1145/2462029.2462032](https://doi.org/10.1145/2462029.2462032) | [link](https://dl.acm.org/doi/10.1145/2462029.2462032) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2013:conf_paste_VitasekBH13` |  |
| 3 | A proper performance evaluation system that summarizes code placement effects | Masahiro Yasugi, Yuki Matsuda 0006, Tomoharu Ugawa | The growing complexity of underlying systems such as memory hierarchies and speculation mechanisms are making it difficult to perform proper performance evaluations. | 系统软件 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=1; venue=部分属于软工; SYS=cache | [10.1145/2462029.2462035](https://doi.org/10.1145/2462029.2462035) | [link](https://dl.acm.org/doi/10.1145/2462029.2462035) | 🟡 保留观察 | 🟡 可选获取 | `CCF2013:conf_paste_YasugiMU13` |  |
| 4 | Automatically mining program build information via signature matching | Charng-Da Lu | Program build information, such as compilers and libraries used, is vitally important in an auditing and benchmarking framework for High-Performance Computing (HPC) systems. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=0; D3=1; D4=1; venue=部分属于软工 | [10.1145/2462029.2462036](https://doi.org/10.1145/2462029.2462036) | [link](https://dl.acm.org/doi/10.1145/2462029.2462036) | 🟡 保留观察 | 🟡 可选获取 | `CCF2013:conf_paste_Lu13` |  |
| 5 | Exploring program phases for statistical bug localization | Varun Modi, Subhajit Roy 0001, Sanjeev K. Aggarwal | Statistical bug isolation techniques attempt to capture a correlation of various program features (like predicates and profiled paths) for debugging. | 系统软件 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=1; D4=0; venue=部分属于软工; SYS=cache | [10.1145/2462029.2462034](https://doi.org/10.1145/2462029.2462034) | [link](https://dl.acm.org/doi/10.1145/2462029.2462034) | 🟡 保留观察 | 🟡 可选获取 | `CCF2013:conf_paste_ModiRA13` |  |
| 6 | Increasing human-tool interaction via the web | Thomas Ball 0001, Peli de Halleux, Nikhil Swamy, Daan Leijen | Software tools researchers can accelerate their ability to learn by exposing tools to users via web technologies, allowing them to observe and test the interactions between humans and tools. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工 | [10.1145/2462029.2462031](https://doi.org/10.1145/2462029.2462031) | [link](https://dl.acm.org/doi/10.1145/2462029.2462031) | 🟡 保留观察 | 🟡 可选获取 | `CCF2013:conf_paste_BallHSL13` |  |
| 7 | A comprehensive toolchain for workload characterization across JVM languages | Aibek Sarimbekov, Andreas Sewe, Stephen Kell, Yudi Zheng, Walter Binder, Lubomír Bulej, Danilo Ansaloni | The Java Virtual Machine (JVM) today hosts implementations of numerous languages. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=1; D4=0; venue=部分属于软工; PL=compiler; SYS=garbage collection | [10.1145/2462029.2462033](https://doi.org/10.1145/2462029.2462033) | [link](https://dl.acm.org/doi/10.1145/2462029.2462033) | ⚪ 暂不跟进 | ⚪ 暂不获取 | `CCF2013:conf_paste_SarimbekovSKZBBA13` |  |

## 6. 本 venue 年度观察

- 主题标签补充：程序设计语言/编译 (3) / 需求工程 (2) / 可靠性/安全 (2) / 测试与验证 (2) / 维护与演化 (1)
- 建议优先获取 `PDF` 的论文：`Automated inference of atomic sets for safe concurrent execution`；`ShadowData: shadowing heap objects in Java`
