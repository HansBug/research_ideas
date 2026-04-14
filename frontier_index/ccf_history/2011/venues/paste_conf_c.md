# `PASTE` (`2011`) 论文名录

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
- 年份：`2011`
- 条目数：`6`
- 主体归属：程序设计语言与形式化基础
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近

## 3. 关键信息页面

- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/paste/
- `CFP`：待补

## 4. 本 venue 统计

- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (3) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 一级总判定分布：程序设计语言与形式化基础 4 / 软件工程 1 / 系统软件 1
- 软工纳入判定分布：不属于软件工程 5 / 跨域但软工主导 1
- 判定来源分布：启发式初判 (6)
- 人工复核状态分布：未人工复核 (6)
- 高频软工主路径：2.2.2 模块化、依赖与解耦 (1)

## 5. 论文名录

- 说明：完整摘要、初筛理由、`BibTeX` 与软工判定字段已内嵌写入对应 `metadata` 文件。

| 序号 | 标题 | 作者 | 一句话说明 | 一级总判定 | 软工纳入判定 | 判定来源 | 人工复核状态 | 软工主路径 | 软工次路径/标签 | 判定依据 | DOI | 官方落地页 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Anywhere, any-time binary instrumentation | Andrew R. Bernat, Barton P. Miller | The Dyninst binary instrumentation and analysis framework distinguishes itself from other binary instrumentation tools through its abstract, machine independent interface; its emphasis on anywhere, any-time binary instrumentation; and its low overhead that is  | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=0; D4=0; venue=部分属于软工 | [10.1145/2024569.2024572](https://doi.org/10.1145/2024569.2024572) | [link](https://dl.acm.org/doi/10.1145/2024569.2024572) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2011:conf_paste_BernatM11` |  |
| 2 | Locating failure-inducing environment changes | Dawei Qi, Minh Ngoc Ngo, Tao Sun, Abhik Roychoudhury | Traditionally, debugging refers to the process of locating the program portions which are responsible for a program failure. | 系统软件 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=1; D3=1; D4=0; venue=部分属于软工; SYS=operating system,kernel | [10.1145/2024569.2024576](https://doi.org/10.1145/2024569.2024576) | [link](https://dl.acm.org/doi/10.1145/2024569.2024576) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2011:conf_paste_QiNSR11` |  |
| 3 | Towards systematic, comprehensive trace generation for behavioral pattern detection through symbolic execution | Markus von Detten | In reverse engineering, dynamic pattern detection is accomplished by collecting execution traces and comparing them to expected behavioral patterns. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=0; D3=1; D4=0; venue=部分属于软工 | [10.1145/2024569.2024573](https://doi.org/10.1145/2024569.2024573) | [link](https://dl.acm.org/doi/10.1145/2024569.2024573) | 🟢 优先跟进 | 🟢 建议获取 PDF | `CCF2011:conf_paste_Detten11` |  |
| 4 | An evaluation of change-based coverage criteria | Marc Fisher II, Jan Wloka, Frank Tip, Barbara G. Ryder, Alexander Luchansky | Various coverage criteria are commonly used to assess the quality of test suites, but achieving full coverage according to these criteria is often impossible or impractical. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=1; D2=1; D3=1; D4=1; venue=部分属于软工 | [10.1145/2024569.2024575](https://doi.org/10.1145/2024569.2024575) | [link](https://dl.acm.org/doi/10.1145/2024569.2024575) | 🟡 保留观察 | 🟡 可选获取 | `CCF2011:conf_paste_FisherWTRL11` |  |
| 5 | Assessing modularity via usage changes | Yana Momchilova Mileva, Andreas Zeller | Good program design strives towards modularity, that is, limiting the effects of changes to the code. | 软件工程 | 跨域但软工主导 | 启发式初判 | 未人工复核 | 2.2.2 模块化、依赖与解耦 | 8.2.3 服务系统与 API 生态；3.2.1 静态分析与抽象解释；3.2.2 动态与混合分析 | X1=否; D1=2; D2=0; D3=1; D4=1; venue=部分属于软工; cross=是 | [10.1145/2024569.2024577](https://doi.org/10.1145/2024569.2024577) | [link](https://dl.acm.org/doi/10.1145/2024569.2024577) | 🟡 保留观察 | 🟡 可选获取 | `CCF2011:conf_paste_MilevaZ11` | 跨域 |
| 6 | Labeling library functions in stripped binaries | Emily R. Jacobson, Nathan E. Rosenblum, Barton P. Miller | Binary code presents unique analysis challenges, particularly when debugging information has been stripped from the executable. | 程序设计语言与形式化基础 | 不属于软件工程 | 启发式初判 | 未人工复核 |  |  | X1=否; D1=0; D2=1; D3=1; D4=0; venue=部分属于软工 | [10.1145/2024569.2024571](https://doi.org/10.1145/2024569.2024571) | [link](https://dl.acm.org/doi/10.1145/2024569.2024571) | 🟡 保留观察 | 🟡 可选获取 | `CCF2011:conf_paste_JacobsonRM11` |  |

## 6. 本 venue 年度观察

- 主题标签补充：维护与演化 (3) / 程序修复 (2) / 可靠性/安全 (2) / 待人工细分 (1) / 需求工程 (1)
- 建议优先获取 `PDF` 的论文：`Anywhere, any-time binary instrumentation`；`Locating failure-inducing environment changes`；`Towards systematic, comprehensive trace generation for behavioral pattern detection through symbolic execution`
