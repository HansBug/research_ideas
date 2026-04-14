# `CCF` 软工相关 venue `2026` 投稿日期与主页核查表

## 1. 说明

- 核查时间：`2026-04-14 22:36:36`
- 项目相关性补充时间：`2026-04-14 22:51:36`
- 覆盖范围：以 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 当前保留的 `57` 个 software-engineering-oriented venue 为准。
- 核查口径：
  - 只记录**官方 `2026` 主页 / CFP / important dates / 作者指南**里的信息。
  - 不按往年日期外推；官方没发就直接写“未公布”。
  - 对 `2026` 会议，如果官方投稿实际发生在 `2025`，表中按官方真实日期原样记录。
  - 对期刊，如果官方主页未给出 `2026` 年固定 `ddl`，统一写“未见 `2026` 固定 `ddl`”，不把它强行改写成会议信息结构。
- 特殊说明：
  - `WICSA` 当前按官方延续系列 [ICSA 2026](https://conf.researchr.org/home/icsa-2026) 记录。
  - `ICSR` 当前按官方合流后的 [VARIABILITY 2026](https://conf.researchr.org/home/variability-2026) 记录；`2026` 没有独立 `ICSR` 主页。
- 项目相关性说明：
  - 为避免把四个项目压成一个含糊总分，下面把“和各个 project 的关联性”拆成 `P1/P2/P3/P4` 四列。
  - `P1 建模`：对应 [project_1_llm_state_machine_modeling/README.md](../project_1_llm_state_machine_modeling/README.md) 的“基于自然语言控制系统需求生成状态机模型”。
  - `P2 场景/性质`、`P3 验证`、`P4 修复`：对应 [TARGET.md](../TARGET.md) 中的研究内容二、三、四；当前 `project_2/3/4` 顶层仅有 `.keep`，因此这三列以 `TARGET.md` 的项目定义为主。
  - emoji 口径：`🟢` 高相关，值得重点跟踪；`🟡` 中相关，可持续关注；`🟠` 弱相关，仅局部子题可用；`⚪` 基本无关。
  - 这些 emoji 是 **venue 级先验**，服务于“先看哪些 venue 更值得跟踪”；不替代单篇论文终判。

## 2. A 类会议

| 简称 | 全称 | 官方链接 | 投稿关键日期 | 其他重要日期 | `P1 建模` | `P2 场景/性质` | `P3 验证` | `P4 修复` | 会期 / 状态 |
|---|---|---|---|---|---|---|---|---|---|
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | [主页](https://pldi26.sigplan.org/)<br>[CFP](https://pldi26.sigplan.org/track/pldi-2026-papers) | 全文 `2025-11-13` | 官方明确写明：`无摘要 ddl` | `⚪` | `⚪` | `🟡` | `🟡` | 主会 `2026-06-17 ~ 2026-06-19`<br>Workshop/Tutorial `2026-06-15 ~ 2026-06-16` |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | [主页](https://conf.researchr.org/home/fse-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/fse-2026) | 摘要 `2025-09-04`<br>全文 `2025-09-11` | 作者回复 `2025-11-21 ~ 2025-11-25`<br>初审通知 `2025-12-22` | `🟢` | `🟢` | `🟢` | `🟢` | `2026-07-05 ~ 2026-07-09`<br>已公布 |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages, and Applications | [主页 / CFP](https://2026.splashcon.org/track/oopsla-2026) | `R1` 全文 `2025-10-10`<br>`R2` 全文 `2026-03-17` | `R1` 回复 `2025-12-02 ~ 2025-12-05`；通知 `2025-12-17`；修回 `2026-02-03`；终判 `2026-02-17`；camera-ready `2026-02-27`<br>`R2` 回复 `2026-05-19 ~ 2026-05-22`；通知 `2026-06-10`；修回 `2026-07-21`；终判 `2026-08-07`；camera-ready `2026-08-14` | `🟠` | `⚪` | `🟠` | `🟡` | `2026-10-03 ~ 2026-10-09`<br>已公布 |
| `ASE` | International Conference on Automated Software Engineering | [主页](https://conf.researchr.org/home/ase-2026)<br>[Research Track Dates](https://conf.researchr.org/dates/ase-2026) | 全文 `2026-03-26` | Early reject `2026-05-25`<br>作者回复 `2026-05-25 ~ 2026-05-27`<br>初审通知 `2026-06-18`<br>大修提交 `2026-07-16`<br>大修终判 `2026-07-29`<br>camera-ready `2026-08-03` | `🟢` | `🟢` | `🟢` | `🟢` | `2026-10-12 ~ 2026-10-16`<br>已公布 |
| `ICSE` | International Conference on Software Engineering | [主页](https://conf.researchr.org/home/icse-2026)<br>[Research Track CFP](https://conf.researchr.org/track/icse-2026/icse-2026-research-track) | `R1` 摘要 `2025-03-07`；全文 `2025-03-14`<br>`R2` 摘要 `2025-07-11`（可选）；全文 `2025-07-18` | `R1` 回复 `2025-05-27 ~ 2025-05-29`；通知 `2025-06-20`；修回 `2025-07-18`；终判 `2025-10-17`；camera-ready `2025-09-10 / 2025-11-28`<br>`R2` 回复 `2025-09-23 ~ 2025-09-25`；通知 `2025-10-17`；修回 `2025-11-14`；终判 `2025-12-19`；camera-ready `2025-11-28 / 2026-01-16` | `🟢` | `🟢` | `🟢` | `🟢` | `2026-04-12 ~ 2026-04-18`<br>已公布 |
| `ISSTA` | International Symposium on Software Testing and Analysis | [主页](https://conf.researchr.org/home/issta-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/issta-2026) | 全文 `2026-01-29` | 作者回复 `2026-03-24 ~ 2026-03-26`<br>初审通知 `2026-04-16`<br>大修提交 `2026-05-21`<br>终判 `2026-06-25`<br>camera-ready `2026-07-23` | `🟠` | `🟡` | `🟢` | `🟢` | `2026-10-03 ~ 2026-10-09`<br>已公布 |
| `FM` | International Symposium on Formal Methods | [主页](https://conf.researchr.org/home/fm-2026)<br>[Research Track Dates](https://conf.researchr.org/dates/fm-2026) | 摘要 `2025-11-25`（optional）<br>全文 `2025-12-02` | 通知 `2026-02-06`<br>Final Version `2026-03-02` | `🟢` | `🟢` | `🟢` | `🟠` | `2026-05-18 ~ 2026-05-22`<br>已公布 |

## 3. A 类期刊

> 下表统一口径：截至 `2026-04-14`，官方主页均**未公布 `2026` 年固定 `ddl`**；也**未见统一 abstract / notification / camera-ready**，因此不按会议时间轴硬写。

| 简称 | 全称 | 官方主页 | `2026` 投稿状态 | `P1 建模` | `P2 场景/性质` | `P3 验证` | `P4 修复` | 备注 |
|---|---|---|---|---|---|---|---|---|
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | [主页](https://dl.acm.org/journal/tosem) | 未见 `2026` 固定 `ddl` | `🟢` | `🟢` | `🟢` | `🟢` | 常规期刊收稿 |
| `TSE` | IEEE Transactions on Software Engineering | [主页](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | 未见 `2026` 固定 `ddl` | `🟢` | `🟢` | `🟢` | `🟢` | 常规期刊收稿 |
| `TSC` | IEEE Transactions on Services Computing | [主页](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=4629386) | 未见 `2026` 固定 `ddl` | `⚪` | `🟠` | `🟠` | `⚪` | 常规期刊收稿 |

## 4. B 类会议

| 简称 | 全称 | 官方链接 | 投稿关键日期 | 其他重要日期 | `P1 建模` | `P2 场景/性质` | `P3 验证` | `P4 修复` | 会期 / 状态 |
|---|---|---|---|---|---|---|---|---|---|
| `ECOOP` | European Conference on Object-Oriented Programming | [主页](https://2026.ecoop.org/)<br>[Technical Papers Dates](https://2026.ecoop.org/dates/ecoop-2026) | `R1` 提交 `2025-11-27`<br>`R2` 提交 `2026-02-12` | `R1` 回复 `2026-01-12 ~ 2026-01-16`；通知 `2026-01-29`<br>`R2` 回复 `2026-03-23 ~ 2026-03-27`；通知 `2026-04-09`<br>camera-ready `2026-04-27` | `🟠` | `⚪` | `🟠` | `🟡` | `2026-06-29 ~ 2026-07-03`<br>Brussels, Belgium |
| `ICPC` | IEEE International Conference on Program Comprehension | [主页](https://conf.researchr.org/home/icpc-2026)<br>[Research Track Dates](https://conf.researchr.org/dates/icpc-2026) | 摘要 `2025-10-19`<br>全文 `2025-10-23` | Final Author Notification `2026-01-05`<br>Camera Ready `2026-01-26` | `⚪` | `🟠` | `🟠` | `🟢` | `2026-04-12 ~ 2026-04-13`<br>Rio de Janeiro, Brazil |
| `RE` | IEEE International Requirements Engineering Conference | [主页](https://conf.researchr.org/home/re-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/re-2026) | 摘要 `2026-02-16`<br>全文 `2026-02-23` | 通知 `2026-05-08`<br>camera-ready `2026-06-08` | `🟢` | `🟢` | `🟡` | `🟠` | `2026-08-17 ~ 2026-08-21`<br>Montreal, Canada |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | [主页](https://caise26.polimi.it/)<br>[Full Papers](https://caise26.polimi.it/?page_id=60) | 摘要 `2025-11-21`（mandatory，官方从 `2025-11-14` 延到 `2025-11-21`）<br>全文 `2025-11-28`（firm） | 录用通知 `2026-02-12` | `🟢` | `🟡` | `🟡` | `⚪` | `2026-06-08 ~ 2026-06-12`<br>已公布 |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | [主页](https://conf.researchr.org/home/models-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/models-2026) | 摘要 `2026-03-20`<br>全文 `2026-03-27` | 作者回复 `2026-05-27 ~ 2026-05-29`<br>录用通知 `2026-06-17`<br>camera-ready `2026-07-31` | `🟢` | `🟢` | `🟢` | `🟠` | `2026-10-04 ~ 2026-10-09`<br>Málaga, Spain |
| `ICSOC` | International Conference on Service Oriented Computing | [主页](https://icsoc2026.it.p.lodz.pl/)<br>[Important Dates](https://icsoc2026.it.p.lodz.pl/important-dates.html) | Early paper `2026-05-10`<br>Regular 摘要 `2026-07-05`<br>Regular / Industrial 全文 `2026-07-12` | Final notification `2026-09-13`<br>camera-ready `2026-09-27` | `⚪` | `🟠` | `🟠` | `⚪` | `2026-12-01 ~ 2026-12-04`<br>已公布 |
| `SANER` | IEEE International Conference on Software Analysis, Evolution, and Reengineering | [主页](https://conf.researchr.org/home/saner-2026)<br>[Research Track Dates](https://conf.researchr.org/dates/saner-2026) | 摘要 `2025-10-09`（mandatory）<br>全文 `2025-10-16` | 通知 `2025-12-09`<br>camera-ready / registration `2026-01-09` | `⚪` | `🟠` | `🟡` | `🟢` | `2026-03-17 ~ 2026-03-20`<br>Limassol, Cyprus |
| `ICSME` | International Conference on Software Maintenance and Evolution | [主页](https://conf.researchr.org/home/icsme-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/icsme-2026) | 摘要 `2026-02-27`<br>全文 `2026-03-06` | Early decisions `2026-05-03`<br>作者回复 `2026-05-04 ~ 2026-05-08`<br>Final notification `2026-05-29` | `⚪` | `🟠` | `🟡` | `🟢` | `2026-09-14 ~ 2026-09-18`<br>Benevento, Italy |
| `VMCAI` | International Conference on Verification, Model Checking, and Abstract Interpretation | [主页](https://conf.researchr.org/home/vmcai-2026)<br>[Dates](https://conf.researchr.org/dates/vmcai-2026) | Paper submission `2025-09-15`（Extended） | Artifact registration `2025-09-17`<br>Artifact submission `2025-09-22`<br>Notification `2025-11-06`<br>camera-ready `2025-11-20` | `🟠` | `🟡` | `🟢` | `🟠` | `2026-01-12 ~ 2026-01-13`<br>Rennes, France |
| `ICWS` | IEEE International Conference on Web Services | [主页](https://services.conferences.computer.org/2026/icws/)<br>[Call for Papers](https://services.conferences.computer.org/2026/icws/icws-call-for-papers) | Paper submission `2026-03-22`（official page 当前写 extended and firm） | Acceptance notifications `2026-05-10`<br>camera-ready / registration `2026-05-31` | `⚪` | `🟠` | `🟠` | `⚪` | `2026-07-13 ~ 2026-07-18`<br>Sydney, Australia |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | [主页](https://conf.researchr.org/home/eseiw-2026)<br>[Technical Track Dates](https://conf.researchr.org/dates/eseiw-2026) | 摘要 `2026-05-11`（mandatory）<br>全文 `2026-05-18` | 通知 `2026-06-30`<br>camera-ready `2026-08-17` | `⚪` | `🟠` | `🟠` | `🟠` | `2026-10-04 ~ 2026-10-09`<br>München, Germany |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | [主页](https://cyprusconferences.org/issre2026/)<br>[Research CFP](https://cyprusconferences.org/issre2026/cfp-research/) | 摘要 `2026-04-10`<br>全文 `2026-04-17` | 作者 rebuttal `2026-06-05 ~ 2026-06-08`<br>Decisions / early notification `2026-06-15`<br>Revision `2026-06-16 ~ 2026-07-03`<br>Notification to Authors `2026-07-08`<br>Camera Ready `2026-08-19` | `⚪` | `🟡` | `🟢` | `🟡` | `2026-10-20 ~ 2026-10-23`<br>Limassol, Cyprus |

## 5. B 类期刊

> 下表统一口径：截至 `2026-04-14`，官方主页均**未公布 `2026` 年固定 `ddl`**；也**未见统一 abstract / notification / camera-ready**。

| 简称 | 全称 | 官方主页 | `2026` 投稿状态 | `P1 建模` | `P2 场景/性质` | `P3 验证` | `P4 修复` | 备注 |
|---|---|---|---|---|---|---|---|---|
| `ASE` | Automated Software Engineering | [主页](https://link.springer.com/journal/10515) | 未见 `2026` 固定 `ddl` | `🟢` | `🟢` | `🟢` | `🟢` | 常规期刊收稿 |
| `ESE` | Empirical Software Engineering | [主页](https://link.springer.com/journal/10664) | 未见 `2026` 固定 `ddl` | `⚪` | `🟠` | `🟠` | `🟠` | 常规期刊收稿 |
| `IETS` | IET Software | [主页](https://ietresearch.onlinelibrary.wiley.com/journal/1751880x) | 未见 `2026` 固定 `ddl` | `🟠` | `🟠` | `🟠` | `🟠` | 常规期刊收稿 |
| `IST` | Information and Software Technology | [主页](https://www.sciencedirect.com/journal/information-and-software-technology) | 未见 `2026` 固定 `ddl` | `🟡` | `🟡` | `🟡` | `🟡` | 常规期刊收稿 |
| `JSEP` | Journal of Software: Evolution and Process | [主页](https://onlinelibrary.wiley.com/journal/20477481) | 未见 `2026` 固定 `ddl` | `⚪` | `⚪` | `🟠` | `🟢` | 常规期刊收稿 |
| `JSS` | Journal of Systems and Software | [主页](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | 未见 `2026` 固定 `ddl` | `🟡` | `🟡` | `🟡` | `🟡` | 常规期刊收稿 |
| `RE` | Requirements Engineering | [主页](https://link.springer.com/journal/766) | 未见 `2026` 固定 `ddl` | `🟢` | `🟢` | `🟡` | `🟠` | 常规期刊收稿 |
| `SCP` | Science of Computer Programming | [主页](https://www.sciencedirect.com/journal/science-of-computer-programming) | 未见 `2026` 固定 `ddl` | `🟠` | `🟠` | `🟡` | `🟠` | 常规期刊收稿 |
| `SoSyM` | Software and Systems Modeling | [主页](https://link.springer.com/journal/10270) | 未见 `2026` 固定 `ddl` | `🟢` | `🟢` | `🟢` | `🟠` | 常规期刊收稿 |
| `STVR` | Software Testing, Verification and Reliability | [主页](https://onlinelibrary.wiley.com/journal/10991689) | 未见 `2026` 固定 `ddl` | `⚪` | `🟡` | `🟢` | `🟡` | 常规期刊收稿 |
| `SPE` | Software: Practice and Experience | [主页](https://onlinelibrary.wiley.com/journal/1097024x) | 未见 `2026` 固定 `ddl` | `⚪` | `⚪` | `🟠` | `🟠` | 常规期刊收稿 |

## 6. C 类会议

| 简称 | 全称 | 官方链接 | 投稿关键日期 | 其他重要日期 | `P1 建模` | `P2 场景/性质` | `P3 验证` | `P4 修复` | 会期 / 状态 |
|---|---|---|---|---|---|---|---|---|---|
| `PASTE` | ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | [SPLASH 2026 主页](https://2026.splashcon.org/) | 截至 `2026-04-14` 未公布 | 截至 `2026-04-14`，在 `SPLASH 2026` 官方站未检索到 `PASTE 2026` 独立 track / CFP / important dates | `⚪` | `⚪` | `🟡` | `🟡` | `2026` 官方页未见 |
| `APSEC` | Asia-Pacific Software Engineering Conference | [主页](https://conf.researchr.org/home/apsec-2026)<br>[Technical Track Dates](https://conf.researchr.org/dates/apsec-2026) | 摘要 `2026-07-06`<br>全文 `2026-07-13` | Bidding `2026-07-14`<br>Papers assigned `2026-07-20 12:00`<br>First half reviews `2026-08-10`<br>Final reviews `2026-08-31`<br>Notification `2026-09-14`<br>camera-ready `2026-10-19` | `🟡` | `🟡` | `🟡` | `🟡` | `2026-12-07 ~ 2026-12-10`<br>Bali, Indonesia |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | [主页](https://conf.researchr.org/home/ease-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/ease-2026) | 摘要 `2026-01-16`<br>全文 `2026-01-23` | Notification `2026-03-13`<br>camera-ready `2026-04-20`<br>Early registration `2026-04-24` | `⚪` | `🟠` | `🟠` | `🟠` | `2026-06-09 ~ 2026-06-12`<br>Glasgow, United Kingdom |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | [主页](https://formal-analysis.com/iceccs/2026/) | 摘要 `2026-06-29`<br>全文 `2026-07-06` | Acceptance / rejection `2026-08-17`<br>camera-ready `2026-08-31` | `🟡` | `🟡` | `🟢` | `⚪` | `2026-11-23 ~ 2026-11-24`<br>Brisbane, Australia |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | [主页](https://conf.researchr.org/home/icst-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/icst-2026) | 全文 `2025-12-22` | Author notification `2026-02-20`<br>camera-ready `2026-03-06` | `🟠` | `🟡` | `🟢` | `🟢` | `2026-05-18 ~ 2026-05-22`<br>Daejeon, South Korea |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | [主页](https://conf.researchr.org/home/scam-2026)<br>[Research Track Dates](https://conf.researchr.org/dates/scam-2026) | 全文 `2026-06-11` | Author notification `2026-07-30`<br>camera-ready `2026-08-14` | `⚪` | `🟠` | `🟠` | `🟢` | `2026-09-14 ~ 2026-09-15`<br>Benevento, Italy |
| `COMPSAC` | International Computer Software and Applications Conference | [主页](https://ieeecompsac.computer.org/2026/)<br>[Call for Papers](https://ieeecompsac.computer.org/2026/call-for-papers/) | Symposium paper `2026-02-20`（official page 当前为 extended） | Acceptance notification `2026-04-12`<br>camera-ready `2026-05-21` | `🟠` | `🟠` | `🟠` | `🟠` | `2026-07-07 ~ 2026-07-10`<br>已公布 |
| `ICFEM` | International Conference on Formal Engineering Methods | [主页](https://icfem2026.github.io/) | 摘要 `2026-06-01`<br>全文 `2026-06-08` | Acceptance notification `2026-08-08`<br>camera-ready `2026-09-07` | `🟢` | `🟢` | `🟢` | `🟠` | `2026-11-17 ~ 2026-11-20`<br>Southampton, UK |
| `SSE` | IEEE International Conference on Software Services Engineering | [主页](https://services.conferences.computer.org/2026/sse/)<br>[Call for Papers](https://services.conferences.computer.org/2026/sse/sse-call-for-papers) | Paper submission `2026-03-22`（official page 当前为 extended and firm） | Acceptance notifications `2026-05-10`<br>camera-ready / registration `2026-05-31` | `⚪` | `🟠` | `🟠` | `⚪` | `2026-07-13 ~ 2026-07-18`<br>Sydney, Australia |
| `ICSSP` | International Conference on Software and System Process | [ISSPA Annual Conference](https://www.isspa-process.org/annual-conference/) | 截至 `2026-04-14` 未公布 | 截至 `2026-04-14`，官方系列页仅列到 `ICSSP 2024`，未见 `ICSSP 2026` 独立主页 / CFP / important dates | `⚪` | `⚪` | `⚪` | `⚪` | `2026` 官方页未见 |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | [主页](https://ksiresearch.org/seke/seke26.html)<br>[CFP PDF](https://ksiresearch.org/seke/seke26cfp.pdf) | 全文 `2026-05-01` | Notification `2026-06-20`<br>Revised paper for proceedings `2026-07-20`<br>Early registration `2026-07-20` | `🟠` | `🟠` | `🟠` | `⚪` | `2026-10-04 ~ 2026-10-10`<br>KSIR Virtual Conference Center, USA |
| `QRS` | International Conference on Software Quality, Reliability and Security | [主页](https://qrs26.techconf.org/) | 摘要 `2026-04-08`（页面保留为原定日期）<br>Regular / Short papers `2026-04-22`（extended） | Workshop / Special Session `2026-05-15`<br>Regular / Short 通知 `2026-05-30`<br>Fast Abstract / Industry `2026-06-03`<br>Poster `2026-06-03`<br>其余 track 通知 `2026-06-15`<br>camera-ready / registration `2026-07-01` | `⚪` | `🟡` | `🟢` | `🟡` | `2026-07-22 ~ 2026-07-25`<br>Florence, Italy |
| `ICSR` | International Conference on Software Reuse | [VARIABILITY 2026 主页](https://conf.researchr.org/home/variability-2026)<br>[VARIABILITY 2026 Dates](https://conf.researchr.org/dates/variability-2026) | `2026` 无独立 `ICSR`；官方并入 `VARIABILITY 2026`<br>初次提交 `2025-12-11`<br>二次提交 `2026-04-10` | 接收 / revisions `2026-02-16`<br>Second notification `2026-06-01`<br>Camera-ready `2026-04-15 / 2026-07-15`<br>Registration `2026-07-15` | `🟠` | `🟠` | `⚪` | `🟠` | `2026-09-29 ~ 2026-10-02`<br>按官方合流口径记录 |
| `SPIN` | International Symposium on Model Checking of Software | [主页 / CFP](https://spin-web.github.io/SPIN2026/) | 摘要 `2026-01-22`<br>全文 `2026-01-29` | Tool-related artifact `2026-02-05`（mandatory）<br>录用通知 `2026-03-05`<br>Accepted non-tool artifact `2026-03-12`<br>Additional artifact result `2026-04-09` | `🟡` | `🟡` | `🟢` | `🟠` | Symposium `2026-04-15 ~ 2026-04-16` |
| `TASE` | Theoretical Aspects of Software Engineering Conference | [主页](https://tase2026.github.io/)<br>[Important Dates](https://tase2026.github.io/c_impd.html) | 摘要 `2026-03-01`（页面保留原定 `2026-02-15`）<br>全文 `2026-03-07`（页面保留原定 `2026-02-21`） | Author notification `2026-04-15`（页面保留原定 `2026-04-01`）<br>camera-ready `2026-05-01` | `🟠` | `🟡` | `🟢` | `🟠` | `2026-07-04 ~ 2026-07-06`<br>Shanghai, China |
| `MSR` | Mining Software Repositories | [主页](https://2026.msrconf.org/)<br>[Technical Papers Dates](https://2026.msrconf.org/dates/msr-2026) | 摘要 `2025-10-20`<br>全文 `2025-10-23` | Author response `2025-12-08 ~ 2025-12-11`<br>Author notification `2026-01-07`<br>Camera Ready `2026-01-26` | `⚪` | `🟠` | `🟠` | `🟡` | `2026-04-13 ~ 2026-04-14`<br>Rio de Janeiro, Brazil |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | [主页](https://2026.refsq.org/)<br>[Research Track Dates](https://2026.refsq.org/dates/refsq-2026) | 摘要 `2025-10-10`（optional）<br>全文 `2025-10-17` | Grace period end `2025-10-24`<br>Authors notification `2025-12-15`<br>camera-ready `2026-01-19` | `🟢` | `🟢` | `🟡` | `🟠` | `2026-03-23 ~ 2026-03-26`<br>Poznań, Poland |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | [ICSA 2026 主页](https://conf.researchr.org/home/icsa-2026)<br>[Research Papers Dates](https://conf.researchr.org/dates/icsa-2026) | `WICSA` 当前按 `ICSA 2026` 官方系列延续记录<br>摘要 `2025-11-28`<br>全文 `2025-12-08` | Acceptance notification `2026-02-06`<br>camera-ready `2026-03-06` | `🟡` | `⚪` | `🟠` | `🟠` | `2026-06-22 ~ 2026-06-26`<br>按官方延续系列记录 |
| `Internetware` | Asia-Pacific Symposium on Internetware | [主页](https://conf.researchr.org/home/internetware-2026)<br>[Research Track Dates](https://conf.researchr.org/dates/internetware-2026) | `R1` 摘要 `2026-03-28`（mandatory）；全文 `2026-04-04`<br>`R2` 摘要 `2026-04-27`（mandatory）；全文 `2026-05-04` | `R1` 初审通知 `2026-05-07`；大修提交 `2026-05-18`<br>两轮最终通知 `2026-05-31`<br>camera-ready `2026-06-10` | `⚪` | `⚪` | `🟠` | `⚪` | `2026-07-18 ~ 2026-07-20`<br>Gold Coast, Australia |
| `RV` | International Conference on Runtime Verification | [主页](https://rv2026.smithengineering.queensu.ca/)<br>[CFP](https://rv2026.smithengineering.queensu.ca/cfp/) | Paper submission `2026-05-31` | Tutorial proposal `2026-05-31`<br>Notification `2026-07-16`<br>camera-ready `2026-07-27` | `⚪` | `🟡` | `🟢` | `🟠` | `2026-10-06 ~ 2026-10-09`<br>Kingston, Canada |

## 7. C 类期刊

> 下表统一口径：截至 `2026-04-14`，官方主页均**未公布 `2026` 年固定 `ddl`**；也**未见统一 abstract / notification / camera-ready**。

| 简称 | 全称 | 官方主页 | `2026` 投稿状态 | `P1 建模` | `P2 场景/性质` | `P3 验证` | `P4 修复` | 备注 |
|---|---|---|---|---|---|---|---|---|
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | [主页](https://www.worldscientific.com/worldscinet/ijseke) | 未见 `2026` 固定 `ddl` | `🟠` | `🟠` | `🟠` | `⚪` | 常规期刊收稿 |
| `STTT` | International Journal of Software Tools for Technology Transfer | [主页](https://link.springer.com/journal/10009) | 未见 `2026` 固定 `ddl` | `🟠` | `🟡` | `🟢` | `🟠` | 常规期刊收稿 |
| `SOCA` | Service Oriented Computing and Applications | [主页](https://link.springer.com/journal/11761) | 未见 `2026` 固定 `ddl` | `⚪` | `⚪` | `🟠` | `⚪` | 常规期刊收稿 |
| `SQJ` | Software Quality Journal | [主页](https://link.springer.com/journal/11219) | 未见 `2026` 固定 `ddl` | `⚪` | `🟠` | `🟡` | `⚪` | 常规期刊收稿 |

## 8. 快速结论

1. 已明确发布 `2026` 官方日期的会议很多，但有明显跨年现象，尤其 `ICSE / FSE / ICPC / SANER / MSR / REFSQ / VMCAI` 等，其投稿主窗口在 `2025`。
2. 仍有少数 venue 到 `2026-04-14` 还没有公开 `2026` 主页或 `CFP`，本次明确标成了 `未公布`，没有拿历年日期补空。
3. 期刊部分本次统一按“官方主页是否给出固定 `2026` 年度 ddl”来写；未见固定 `ddl` 的，一律不硬造投稿时间线。
4. 若按当前四个 project 看 venue 先验：`P1/P2` 应优先看 `RE / REFSQ / MoDELS / SoSyM / ICSE / ASE / FSE`，`P3` 应优先看 `FM / ICST / ISSTA / SPIN / RV / VMCAI / ISSRE / QRS / STVR`，`P4` 应优先看 `ASE / ICSE / FSE / ISSTA / ICSME / SANER / SCAM / ICPC`。
