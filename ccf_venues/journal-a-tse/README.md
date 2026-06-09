# TSE README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | TSE |
| 全称 | IEEE Transactions on Software Engineering |
| 类型 | 期刊 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | A |
| 出版商 | IEEE Computer Society / IEEE |
| ISSN | 0098-5589（print）；1939-3520（online） |
| 期刊主页 | [IEEE Computer Society TSE](https://www.computer.org/csdl/journal/ts) |
| Author guidelines | [IEEE Computer Society Author Resources](https://www.computer.org/publications/author-resources/) |
| Submission system | [IEEE Publishing Portal](https://publishingportal.ieee.org/)；[Author Center 说明](https://journals.ieeeauthorcenter.ieee.org/submit-your-article-for-peer-review/ieee-publishing-portal/) |
| Special issues / topical collections | [IEEE Computer Society Calls for Papers](https://www.computer.org/cfp) |
| Volume / issue archive | [IEEE Computer Society TSE archive](https://www.computer.org/csdl/journal/ts) |
| Articles in press / online first | [IEEE Computer Society TSE archive](https://www.computer.org/csdl/journal/ts) |
| DBLP venue page | [DBLP TSE](https://dblp.org/db/journals/tse/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现官方已公布年度卷期 / CFP |

### 1.1 索引与分区信息

> 本节在 PR #91 中从 PR #90 占位推进为“证据链优先”的真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。JCR / CAS 若没有可追溯单刊证据，宁可写 `⏳`，不得用第三方站点补成分区事实。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🟡 | 沿用本库 CCF A 级；官方目录入口已定位，单条目仍需浏览器行级复核 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本 PR 不重新定义 CCF scope，只保留可点击官方基线入口 | `2026-06-09 13:52` |
| WoS Collection | ⏳ | 待人工核验 Web of Science Core Collection 收录集合 | [Clarivate Master Journal List](https://mjl.clarivate.com/search-results) 为官方检索入口；本轮命令行仅确认 SPA 入口可访问，未取得可审计单刊 `SCIE/SSCI/AHCI/ESCI` 行级结果；后续用 ISSN / eISSN 通过浏览器或机构入口复核 | `2026-06-09 13:52` |
| JCR Quartile | ⏳ | 待人工核验 2025 JCR 单刊 category / rank / quartile | [JCR 平台](https://jcr.clarivate.com/jcr/home)；[2025 JCR 发布说明](https://clarivate.com/news/clarivate-unveils-the-2025-journal-citation-reports/) 仅证明 release 存在，不证明本刊 quartile；需机构入口导出单刊 category、rank、quartile、percentile 后再改为 `1️⃣`--`4️⃣` | `2026-06-09 13:52` |
| CAS 分区 | ⏳ | 待人工核验中科院历史版分区 | [中国科学院文献情报中心停更公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 证明 2026 起不再更新发布；本轮未获得本刊历史版官方行级分区，后续只可用官方 / 机构历史版证据补写 | `2026-06-09 13:52` |
| EI / Compendex | 🟢 | 官方 Compendex `SERIALS` 精确命中，按 source-level 期刊记录 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本地 snapshot `compendex_source_list_2026-06-09.xlsx`，sheet `SERIALS`，Source title `IEEE Transactions on Software Engineering`，Source type `Journal`，ISSN `0098-5589`，EISSN `1939-3520`，Publisher `Institute of Electrical and Electronics Engineers Inc.` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | EI 已有官方 source-list 证据；WoS / JCR / CAS 仍待人工或机构入口核验 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；后续 reviewer 需复核本节链接与 source-list 字段 | `2026-06-09 13:52` |

## 2. Scope 与栏目

- 官方 scope 摘要：TSE 面向软件工程理论结果与实证研究，覆盖软件开发与维护方法、评估方法、项目管理、工具与环境、系统问题和综述。
- Article types：研究论文、综述和 IEEE TSE 当前主页 / CFP 支持的期刊稿件类型；具体栏目以 IEEE TSE 当前主页和 author resources 为准。
- 投稿模式：常规滚动投稿；只有带明确截止日期的 special issue / topical collection 才进入 [../TIMELINE.md](../TIMELINE.md) dated timeline。

## 3. 核心编辑人员情报

本节只记录当前公开可核验的 editorial leadership 及候选核心人员线索，不展开全量 editorial board。TSE 的 CSDL 落地页在命令行环境中是动态页，当前人员以 IEEE Computer Society 公告、TSE 相关官方会议页、个人主页 / DBLP / 机构页交叉核验；研究方向与 P1-P4 相关性为基于公开资料的判断。`核验等级 / 当前性` 列用于区分“官方当前 roster / 官方公告 / 个人或机构候选线索”，避免把待复核人员误读为已完全核验。

| 姓名 | 期刊角色 | 单位 | 角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Mauro Pezzè | Editor-in-Chief（2026 起） | USI Università della Svizzera italiana；Università degli Studi di Milano-Bicocca | [IEEE CS 2026 EIC 公告](https://www.computer.org/press-room/2026-eics-announced)；[ICSE 2026 TSE Editorial Board Meeting](https://conf.researchr.org/details/icse-2026/icse-2026-meetings-and-bof/10/TSE-Journal-Editorial-Board-Meeting) | [USI 主页](https://www.inf.usi.ch/faculty/pezze/vitae.html)；[DBLP](https://dblp.org/search?q=Mauro%20Pezz%C3%A8) | 软件测试、程序分析、测试 oracle、自愈 / 自适应软件系统 | [DBLP 近年论文入口](https://dblp.org/search?q=Mauro%20Pezz%C3%A8)：Tratto / LLM test oracles / Prevent 等 | P2/P3/P4 强；P1 中 | 官方公告核验；IEEE CS press-room 可能需浏览器访问，ICSE 2026 TSE meeting 交叉核验 | `2026-06-04 22:05` |
| Marsha Chechik | Associate Editor-in-Chief（候选线索，待 TSE 当前 roster 复核） | University of Toronto | [SIGSOFT 2024 选举材料](https://www.acm.org/binaries/content/assets/sigs/elections/2024-sigsoft.pdf) | [个人主页](https://www.cs.toronto.edu/~chechik/)；[DBLP](https://dblp.org/search?q=Marsha%20Chechik) | 软件建模与分析、规约与验证、需求工程、Safe AI 软件工程 | [DBLP 近年论文入口](https://dblp.org/search?q=Marsha%20Chechik)：AI agents norms、FOL* satisfiability、controller verification 等 | P1/P2/P3 强；P4 中 | 间接 / 候选线索；来源为 2024 年材料，且与 SoSyM EIC 同期角色需 IEEE / TSE 当前 roster 复核 | `2026-06-04 22:05` |
| Massimiliano Di Penta | Associate Editor-in-Chief（候选线索，待 TSE 当前 roster 复核） | University of Sannio | 待补 TSE 角色直接来源；[USI visiting professor page](https://www.inf.usi.ch/it/ricerca-informatica/programma-visiting-professor) 仅作机构线索 | [个人主页](https://mdipenta.github.io/)；[DBLP](https://dblp.org/search?q=Massimiliano%20Di%20Penta) | 软件演化、软件分析、技术债、软件工程推荐系统 | [DBLP 近年论文入口](https://dblp.org/search?q=Massimiliano%20Di%20Penta)：refactoring、technical debt、software evolution 等 | P4 强；P2 中；P1/P3 弱到中 | 候选线索；当前行不作为已官方核验的 TSE AEiC 事实，待 TSE roster 或个人 service 页直接确认 | `2026-06-04 22:05` |
| Tao Zhang | Associate Editor-in-Chief（2026-present，待 TSE 当前 roster 复核） | Macau University of Science and Technology | [个人 CV](https://cszhangtao.github.io/assets/CV.pdf)；[ICSSIP 2026 keynote page](https://icssip.net/speaker.html) | [DBLP](https://dblp.org/search?q=Tao%20Zhang)；[个人 CV](https://cszhangtao.github.io/assets/CV.pdf) | 软件测试、程序分析、调试与修复、LLM for SE、漏洞检测 | [DBLP 近年论文入口](https://dblp.org/search?q=Tao%20Zhang)：smart contract state analysis、HLS bug detection、PLM for SE tasks 等 | P1/P2/P3/P4 强 | 个人 / 会议公开材料交叉线索；待 IEEE / TSE 当前 roster 复核 | `2026-06-04 22:05` |
| Yingfei Xiong | Associate Editor-in-Chief（2026-2028，待 TSE 当前 roster 复核） | Peking University | [个人主页](https://xiongyingfei.github.io/index.html)；[services 页](https://xiongyingfei.github.io/services.html) | [个人主页](https://xiongyingfei.github.io/index.html)；[DBLP](https://dblp.org/search?q=Yingfei%20Xiong) | 程序综合、程序修复、fault localization、程序正确性、LLM agents | [个人主页近年论文](https://xiongyingfei.github.io/index.html)：PredicateFix、HoarePrompt、LLM agent cost reduction、SmartFL 等 | P1/P2/P4 强；P3 中到强 | 个人主页 service 页核验；待 IEEE / TSE 当前 roster 复核 | `2026-06-04 22:05` |

补充说明：上表是本轮核心人员试点口径，不声称覆盖 TSE 全量 editorial board；Co-Editor-in-Chief 当前名单未找到公开可核验来源。除 Mauro Pezzè 的 EiC 角色外，AEiC 条目均按候选 / 间接线索处理，后续需用 IEEE / TSE 当前 roster 做一次人工快照。

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 强相关 | 需求到模型、LLM4SE、建模方法和实证评估均可对齐。 |
| P2 场景与性质生成 | 强相关 | 软件需求、测试、规约和性质生成可作为 TSE 期刊论文方向。 |
| P3 验证剖面与模型检查 | 中相关 | 模型检查、验证工具和实证评估可投稿，但需突出软件工程贡献。 |
| P4 模型修复 | 强相关 | 修复、维护、演化、自动化软件工程和工具评估均适配。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [IEEE Computer Society TSE](https://www.computer.org/csdl/journal/ts) | IEEE Computer Society 官方入口 | `2026-06-04 21:15` |
| Aims and scope | [TSE CFP / scope](https://www.computer.org/digital-library/journals/ts/cfp-ieee-transactions-on-software-engineering) | CFP 页面含 scope 与 rolling submission 入口 | `2026-06-04 21:15` |
| Author guidelines | [IEEE CS Author Resources](https://www.computer.org/publications/author-resources/) | TSE-specific 细则以 TSE 当前主页为准 | `2026-06-04 21:15` |
| Submission system | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | [Author Center 说明](https://journals.ieeeauthorcenter.ieee.org/submit-your-article-for-peer-review/ieee-publishing-portal/)；Publishing Portal 是入口，实际 peer-review destination 待官方当前页确认 | `2026-06-04 21:15` |
| Special issues / topical collections | [IEEE Computer Society CFP](https://www.computer.org/cfp) | 当前未发现 TSE 正在开放且带明确 deadline 的专刊 CFP | `2026-06-04 21:15` |
| Volume / issue archive | [IEEE CS TSE archive](https://www.computer.org/csdl/journal/ts) | DBLP 年度页用于可点击年度 fallback | `2026-06-04 21:15` |
| Articles in press / online first | [IEEE CS TSE archive](https://www.computer.org/csdl/journal/ts) | Early Access / online first 与正式卷期可能存在年份差异 | `2026-06-04 21:15` |
| DBLP venue | [DBLP TSE](https://dblp.org/db/journals/tse/index.html) | 年度计数 baseline / bibliographic fallback | `2026-06-04 21:15` |

## 6. 年度信息汇总

| 年份 | 年度状态 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Articles / Online first | DBLP 年度页 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| [`2028`](./2028/README.md) | 🟢 滚动开放 | [TSE](https://www.computer.org/csdl/journal/ts) | [Author Resources](https://www.computer.org/publications/author-resources/) | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | 无已知 | 滚动投稿 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | 🟢 滚动开放 | [TSE](https://www.computer.org/csdl/journal/ts) | [Author Resources](https://www.computer.org/publications/author-resources/) | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | 无已知 | 滚动投稿 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟢 滚动开放 | [TSE](https://www.computer.org/csdl/journal/ts) | [Author Resources](https://www.computer.org/publications/author-resources/) | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | 无已知 | 滚动投稿 | [TSE archive](https://www.computer.org/csdl/journal/ts) | [TSE archive](https://www.computer.org/csdl/journal/ts) | [DBLP Vol. 52](https://dblp.org/db/journals/tse/tse52.html) | 98 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 年度已归档 | [TSE](https://www.computer.org/csdl/journal/ts) | [Author Resources](https://www.computer.org/publications/author-resources/) | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | 无已知 active dated CFP | 滚动投稿 | [TSE archive](https://www.computer.org/csdl/journal/ts) | [TSE archive](https://www.computer.org/csdl/journal/ts) | [DBLP Vol. 51](https://dblp.org/db/journals/tse/tse51.html) | 228 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 年度已归档 | [TSE](https://www.computer.org/csdl/journal/ts) | [Author Resources](https://www.computer.org/publications/author-resources/) | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | 无已知 | 滚动投稿 | [TSE archive](https://www.computer.org/csdl/journal/ts) | [TSE archive](https://www.computer.org/csdl/journal/ts) | [DBLP Vol. 50](https://dblp.org/db/journals/tse/tse50.html) | 182 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 年度已归档 | [TSE](https://www.computer.org/csdl/journal/ts) | [Author Resources](https://www.computer.org/publications/author-resources/) | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | 无已知 | 滚动投稿 | [TSE archive](https://www.computer.org/csdl/journal/ts) | [TSE archive](https://www.computer.org/csdl/journal/ts) | [DBLP Vol. 49](https://dblp.org/db/journals/tse/tse49.html) | 278 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 年度已归档 | [TSE](https://www.computer.org/csdl/journal/ts) | [Author Resources](https://www.computer.org/publications/author-resources/) | [IEEE Publishing Portal](https://publishingportal.ieee.org/) | 无已知 | 滚动投稿 | [TSE archive](https://www.computer.org/csdl/journal/ts) | [TSE archive](https://www.computer.org/csdl/journal/ts) | [DBLP Vol. 48](https://dblp.org/db/journals/tse/tse48.html) | 284 | 🟡 部分核验 |

## 7. 维护备注

- TSE 常规投稿按 rolling submission 处理，不进入 dated Mermaid。
- 2022-2026 年度论文数量已填 DBLP `entry article` baseline；这不是 publisher 最终闭合数，后续仍需用 IEEE CSDL / Early Access 按 article type 交叉核验。
- IEEE CSDL 根 archive 当前不提供稳定年度分卷 permalink，根表 Volume / issue 列统一指向主 archive；年度区分以 DBLP volume/year 为可点击 fallback。
- 2027、2028 和 `2029+` 未发现官方年度卷期或专刊 deadline，已保留核查记录，不预设未来卷号。

## 8. TIMELINE.md 同步提示

- TSE rolling submission 已进入 [../TIMELINE.md](../TIMELINE.md) 的“期刊滚动投稿 / 未定日期”表。
- 当前未发现 TSE 正在开放且带明确截止日期的 special issue / topical collection，不新增 dated event 或 Mermaid milestone。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 01:08` | 修复核心人员补充说明中的排版空格，保持期刊人员画像表述稳定。 |
| `2026-06-04 22:05` | 根据正式复审补充 TSE 人员核验等级和年度 DBLP `entry article` baseline，并明确 IEEE CSDL 年度 permalink 限制。 |
| `2026-06-04 21:46` | 补充 TSE 当前公开可核验的核心编辑人员情报，并记录研究方向、近年论文入口和与 P1-P4 的相关性判断。 |
| `2026-06-04 21:15` | 根据 review 修正投稿入口表述：Publishing Portal 只作入口，actual peer-review destination 待官方当前页确认；TSE 2025 周年条目从 special issue 字段降为备注。 |
| `2026-06-04 20:43` | 初始化 TSE 期刊 README，记录 IEEE / CCF / DBLP 核心入口和 2022-2028 年度占位。 |
| `2026-06-04 20:43` | 将投稿入口收紧为 IEEE Publishing Portal，避免误写成已确认的 TSE 专属 ScholarOne。 |
