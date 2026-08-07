# ASE README

> 信息更新时间：`2026-08-07 20:25:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ASE |
| 全称 | IEEE/ACM International Conference on Automated Software Engineering |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | 🏆 |
| 出版方 | ACM / IEEE |
| 官方 series page | [ASE series](https://conf.researchr.org/series/ase) |
| 官方当前 / 最新年度主页 | [ASE 2026](https://conf.researchr.org/home/ase-2026)；2027/2028 已检索未公布 |
| 官方 CFP / Important Dates 总入口 | 逐年度 Research Papers / Research Track 页面维护 |
| 官方 proceedings / paper list 总入口 | 历年优先 [conf.researchr.org ASE program / track](https://conf.researchr.org/series/ase)，proceedings URL 当前多返回 Access denied；[DBLP ASE venue](https://dblp.org/db/conf/kbse/) 作 fallback |
| DBLP venue page | [DBLP ASE / KBSE venue](https://dblp.org/db/conf/kbse/) |
| 当前默认调查范围 | `2022` 至 `2028` |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🏆 | CCF 🏆 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `ASE 2016 - Proceedings of the 31st IEEE/ACM International Conference on Automated Software Engineering`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

- ASE 关注自动化软件工程，覆盖自动化需求、设计、建模、编码、测试、分析、验证、维护、修复与 AI for SE 等方向。
- 与本仓库最相关的方向：requirements and design、modeling / model-driven engineering、testing and analysis、program analysis and verification、automated program repair、AI and software engineering、tool / dataset track。
- 明显不属于本仓库重点但仍可作为趋势背景的方向：教育、社区治理、宽泛人因、非自动化的软件过程经验总结。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 高 | ASE Research Papers 明确覆盖 requirements/design、modeling、MDE 与 AI+SE，可追踪 LLM/工具辅助状态机建模与需求到模型转换。 |
| P2 场景与性质生成 | 高 | testing/analysis、requirements、AI+SE 论文可提供测试场景、属性生成、规约挖掘与自动化评估线索。 |
| P3 验证剖面与模型检查 | 中-高 | program analysis and verification、formal / symbolic analysis、可靠性与工具论文可支撑验证剖面与模型检查方法对比。 |
| P4 模型修复 | 高 | ASE 是 automated program repair、debugging、maintenance、LLM repair 与工具评估的重要入口。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [ASE series](https://conf.researchr.org/series/ase) | conf.researchr 长期 series 入口 | `2026-06-05 08:38` |
| Latest year homepage | [ASE 2026](https://conf.researchr.org/home/ase-2026)；[ASE series](https://conf.researchr.org/series/ase) | 2027 / 2028 候选路径于 2026-07-13 复查仍返回 404，未获正式年度信息 | `2026-07-13 19:13:21` |
| CFP / Call for Papers | [ASE 2026 Research Track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | 2022-2025 逐年度 Research Papers / Research Track 页面维护 | `2026-07-13 19:13:21` |
| Important Dates | [ASE 2026 Research Track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | dates 与 research track 同页；2026 大修、通知、camera-ready 仍由该页支撑 | `2026-07-13 19:13:21` |
| Submission system | [ASE 2026 HotCRP](https://ase26.hotcrp.com/) | 历年 HotCRP 见年度表；2027/2028 未公布 | `2026-06-05 08:38` |
| Program / accepted papers | [ASE 2025 Program](https://conf.researchr.org/program/ase-2025/program-ase-2025/) | 2022-2025 已有官方 program；Research Papers accepted list 页面不总是给出可计数清单 | `2026-06-05 08:38` |
| Proceedings | ⏳ [ASE 2025 proceedings probe](https://conf.researchr.org/info/ase-2025/proceedings) | 当前返回 Access denied；已结束年度用 DBLP `inproceedings` fallback 计数 | `2026-06-05 08:38` |
| DBLP venue | [DBLP ASE / KBSE venue](https://dblp.org/db/conf/kbse/) | 仅作论文名录 / 计数 fallback，不混入主 track 口径 | `2026-06-05 08:38` |

## 5. 核心人员情报

> 人员角色以 ASE 官方年度 organizing committee / track committee 为准；研究方向和代表作基于个人主页、DBLP 或公开学术入口归纳。ASE 多 track 明显，表中优先收录 General Chair、Research/Program Chair、与本仓库强相关的 track chair / area chair 和历年反复出现的领域权威；不等同于全量 PC roster。

| 人员 | 年度 / 层级 | 会议角色 | 单位 / 主页入口 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Stefan Winter | ASE 2026 | General Chair / Open Science Chair | 单位待补 | [ASE 2026 Organizing Committee](https://conf.researchr.org/committee/ase-2026/ase-2026-organizing-committee) | [DBLP](https://dblp.org/pid/161/1380.html) | automated software engineering, testing/debugging, open science（公开资料归纳） | DBLP 近年 automated testing / SE 论文入口；代表作待逐篇筛选 | P2/P4 中高：自动化测试、实验复现与开放科学入口 | 🟡 角色已核验，单位与代表作待深挖 | `2026-06-05 09:40` |
| Justyna Petke | ASE 2026 | Program Co-Chair | UCL | [ASE 2026 Research Track committee](https://conf.researchr.org/committee/ase-2026/ase-2026-research-track-programm-committee) | [UCL profile](https://profiles.ucl.ac.uk/43519-justyna-petke) / [DBLP](https://dblp.org/pid/84/5382.html) | genetic improvement, program repair, automated software engineering | UCL / DBLP 近年 genetic improvement 与 repair 论文入口 | P4 很高：程序修复、搜索式 SE 和自动改进可类比模型修复闭环 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Shiva Nejati | ASE 2026 / ASE 2022 | Program Co-Chair；Journal First Co-Chair | University of Ottawa | [ASE 2026 Research Track committee](https://conf.researchr.org/committee/ase-2026/ase-2026-research-track-programm-committee) / [ASE 2022 Organizing Committee](https://conf.researchr.org/committee/ase-2022/ase-2022-organizing-committee) | [University of Ottawa page](https://www.uottawa.ca/faculty-engineering/people/nejati-shiva) / [DBLP](https://dblp.org/pid/25/2537.html) | model-based testing, requirements / cyber-physical systems, search-based SE, ML-enabled systems verification | Ottawa profile / DBLP 近年 CPS、model-based testing 与 verification 论文入口 | P1/P2/P3 很高：需求、模型、测试和验证的交叉入口 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Marcel Böhme | ASE 2025 / ASE 2026 | Program Co-Chair；New Faculty Symposium Chair | MPI-SP | [ASE 2025 Organizing Committee](https://conf.researchr.org/committee/ase-2025/ase-2025-organizing-committee) / [ASE 2026 Organizing Committee](https://conf.researchr.org/committee/ase-2026/ase-2026-organizing-committee) | [MPI-SP page](https://mpi-softsec.github.io/people/marcel-boehme/) / [DBLP](https://dblp.org/pid/77/8115.html) | fuzzing, software testing, program analysis, security testing | MPI-SP / DBLP 近年 fuzzing 与 testing 论文入口 | P2/P4 高：自动测试、反馈驱动缺陷发现和修复评价 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Lingming Zhang | ASE 2025 / ASE 2024 | Program Co-Chair；AI+SE Area Chair | UIUC | [ASE 2025 Organizing Committee](https://conf.researchr.org/committee/ase-2025/ase-2025-organizing-committee) / [ASE 2024 Research Track](https://conf.researchr.org/track/ase-2024/ase-2024-research) | [UIUC page](https://lingming.cs.illinois.edu/) / [DBLP](https://dblp.org/pid/85/4630.html) | software testing, debugging, program repair, LLM/AI for SE | UIUC / DBLP 近年 testing、repair 与 LLM4SE 论文入口 | P2/P4 很高：测试、修复、LLM4SE baseline 与评估设计 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Shin Yoo | ASE 2025 | General Chair | KAIST | [ASE 2025 Organizing Committee](https://conf.researchr.org/committee/ase-2025/ase-2025-organizing-committee) | [KAIST page](https://coinse.kaist.ac.kr/professor/) / [DBLP](https://dblp.org/pid/y/ShinYoo.html) | search-based software engineering, software testing, automated repair | KAIST / DBLP 近年 SBSE、testing 与 repair 论文入口 | P2/P4 高：搜索式测试、自动修复和实验方法 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Baishakhi Ray | ASE 2024 | Program Co-Chair | Columbia University | [ASE 2024 Organizing Committee](https://conf.researchr.org/committee/ase-2024/ase-2024-organizing-committee) | [Columbia page](https://www.cs.columbia.edu/~rayb/) / [DBLP](https://dblp.org/pid/66/9413.html) | AI for SE, software bugs, program analysis, LLM/code models | Columbia / DBLP 近年 AI4SE 与 LLM/code model 论文入口 | P1/P2/P4 很高：AI4SE、LLM 代码/需求任务、缺陷分析 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Minghui Zhou | ASE 2024 | Program Co-Chair | Peking University | [ASE 2024 Organizing Committee](https://conf.researchr.org/committee/ase-2024/ase-2024-organizing-committee) | [Peking University page](https://sei.pku.edu.cn/~zhmh/) / [DBLP](https://dblp.org/pid/12/1245.html) | empirical SE, open source, software analytics | PKU / DBLP 近年 empirical SE 与 software analytics 论文入口 | P1/P4 中高：经验研究、开源数据集与评估方法 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Christian Bird | ASE 2023 | Research Papers Chair | Microsoft Research | [ASE 2023 Research Papers](https://conf.researchr.org/track/ase-2023/ase-2023-papers) | [Microsoft Research page](https://www.microsoft.com/en-us/research/people/cbird/) / [DBLP](https://dblp.org/pid/10/4745.html) | empirical software engineering, software analytics, developer productivity | MSR / DBLP 近年 empirical SE 与 productivity 论文入口 | P1/P4 中：实验设计、工具评估和开发者数据分析 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Federica Sarro | ASE 2023 | Research Papers Chair | UCL | [ASE 2023 Research Papers](https://conf.researchr.org/track/ase-2023/ase-2023-papers) | [UCL profile](https://profiles.ucl.ac.uk/13880-federica-sarro) / [DBLP](https://dblp.org/pid/72/7846.html) | search-based SE, software analytics, fairness / explainability in SE | UCL / DBLP 近年 SBSE 与 empirical methodology 论文入口 | P2/P4 中高：搜索式生成、经验评估和自动化决策 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Julia Rubin | ASE 2022 | Program Co-Chair | UBC | [ASE 2022 Organizing Committee](https://conf.researchr.org/committee/ase-2022/ase-2022-organizing-committee) | [UBC page](https://www.cs.ubc.ca/~mjulia/) / [DBLP](https://dblp.org/pid/19/4871.html) | software product lines, program analysis, security, software evolution | UBC / DBLP 近年 product lines、analysis 与 evolution 论文入口 | P1/P3/P4 高：变体建模、程序分析、演化与验证 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Shahar Maoz | ASE 2022 | Program Co-Chair | Tel Aviv University | [ASE 2022 Organizing Committee](https://conf.researchr.org/committee/ase-2022/ase-2022-organizing-committee) | [Tel Aviv University page](https://www.cs.tau.ac.il/~maozs/) / [DBLP](https://dblp.org/pid/84/4557.html) | software modeling, formal methods, scenario-based specification, synthesis | TAU / DBLP 近年 scenario-based modeling 与 synthesis 论文入口 | P1/P2/P3 很高：场景、模型、规约与合成直接相关 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |
| Marouane Kessentini | ASE 2022 | General Chair | Oakland University | [ASE 2022 Organizing Committee](https://conf.researchr.org/committee/ase-2022/ase-2022-organizing-committee) | [Oakland University page](https://www.oakland.edu/secs/directory/kessentini/) / [DBLP](https://dblp.org/pid/44/5155.html) | software refactoring, search-based SE, AI for SE, software quality | Oakland / DBLP 近年 refactoring、repair 与 AI4SE 论文入口 | P4 高：搜索式修复、重构和质量优化可支撑修复方法论 | 🟢 角色与学术入口已核验 | `2026-06-05 09:40` |

## 6. 年度信息汇总

年度汇总表按年份降序排列；官方仅公布日期未给具体时刻时写 `待补时刻`。ASE 多 track 明显，论文数量单元格必须说明是 DBLP proceedings fallback 还是 official research-track 口径，不把 NIER、Tool Demo、Industry、Journal-first、Artifact 等混入主论文数量。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | [ASE series](https://conf.researchr.org/series/ase)；年度页未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 待核验 |
| [2027](./2027/README.md) | ⏳ 已检索未公布 | [ASE series](https://conf.researchr.org/series/ase)；年度页未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 待核验 |
| [2026](./2026/README.md) | 🟣 通知后 | [ASE 2026](https://conf.researchr.org/home/ase-2026) | [Research Track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | [Research Track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | [HotCRP](https://ase26.hotcrp.com/) | [Accepted Papers](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | 未公布 | ⏳ 已检索未公布 | 未列出 | 2026-03-26 待补时刻 AoE / UTC-12h；major revision 2026-07-16 待补时刻 AoE / UTC-12h | initial 2026-06-18 待补时刻 AoE / UTC-12h；major revisions 2026-07-29 待补时刻 AoE / UTC-12h；camera-ready 2026-08-03 待补时刻 AoE / UTC-12h | 2026-10-12..2026-10-16 | 名录已公布 / 计数待补（页面过长，单次抓取被截断，不得填数字） | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [ASE 2025](https://conf.researchr.org/home/ase-2025) | [Research Papers](https://conf.researchr.org/track/ase-2025/ase-2025-papers) | [Research Papers](https://conf.researchr.org/track/ase-2025/ase-2025-papers) | [HotCRP](https://ase25.hotcrp.com/) | [Program](https://conf.researchr.org/program/ase-2025/program-ase-2025/) | ⏳ [Access denied](https://conf.researchr.org/info/ase-2025/proceedings) | [DBLP 2025](https://dblp.org/db/conf/kbse/ase2025.html) | 未列出 | 2025-05-30 待补时刻 AoE / UTC-12h | 2025-08-14 待补时刻 AoE / UTC-12h | 2025-11-16..2025-11-20 | DBLP inproceedings fallback: 389（全 proceedings，非主 track） | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [ASE 2024](https://conf.researchr.org/home/ase-2024) | [Research Papers](https://conf.researchr.org/track/ase-2024/ase-2024-research) | [Research Papers](https://conf.researchr.org/track/ase-2024/ase-2024-research) | [HotCRP](https://ase2024.hotcrp.com) | [Program](https://conf.researchr.org/program/ase-2024/program-ase-2024/) | ⏳ [Access denied](https://conf.researchr.org/info/ase-2024/proceedings) | [DBLP 2024](https://dblp.org/db/conf/kbse/ase2024.html) | 2024-05-31 待补时刻 AoE / UTC-12h | 2024-06-07 待补时刻 AoE / UTC-12h | 2024-08-06 待补时刻 AoE / UTC-12h | 2024-10-27..2024-11-01 | DBLP inproceedings fallback: 266（全 proceedings，非主 track） | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [ASE 2023](https://conf.researchr.org/home/ase-2023) | [Research Papers](https://conf.researchr.org/track/ase-2023/ase-2023-papers) | [Research Papers](https://conf.researchr.org/track/ase-2023/ase-2023-papers) | [HotCRP](https://ase2023.hotcrp.com/) | [Program](https://conf.researchr.org/program/ase-2023/program-ase-2023/) | ⏳ [Access denied](https://conf.researchr.org/info/ase-2023/proceedings) | [DBLP 2023](https://dblp.org/db/conf/kbse/ase2023.html) | 2023-04-28 待补时刻 AoE / UTC-12h | 2023-05-05 待补时刻 AoE / UTC-12h | 2023-07-17 待补时刻 AoE / UTC-12h | 2023-09-11..2023-09-15 | DBLP inproceedings fallback: 209（全 proceedings，非主 track） | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [ASE 2022](https://conf.researchr.org/home/ase-2022) | [Research Papers](https://conf.researchr.org/track/ase-2022/ase-2022-research-papers) | [Research Papers](https://conf.researchr.org/track/ase-2022/ase-2022-research-papers) | [HotCRP](https://ase2022.hotcrp.com) | [Program](https://conf.researchr.org/program/ase-2022/program-ase-2022/) | ⏳ [Access denied](https://conf.researchr.org/info/ase-2022/proceedings) | [DBLP 2022](https://dblp.org/db/conf/kbse/ase2022.html) | 2022-04-29 待补时刻 AoE / UTC-12h | 2022-05-06 待补时刻 AoE / UTC-12h | 2022-07-20 待补时刻 AoE / UTC-12h | 2022-10-10..2022-10-14 | DBLP inproceedings fallback: 228（全 proceedings，非主 track） | 🟡 部分核验 |

## 7. 维护备注

- ASE 2026 已有官方主页、Research Track 和 HotCRP；截至 2026-07-13 已过 initial notification，仍有 major revision submission `2026-07-16`、major revision notification `2026-07-29`、camera-ready `2026-08-03` 与会期 `2026-10-12..2026-10-16`，故阶段写作 `🟣 通知后`。
- ASE 2027 / 2028 的 conf.researchr 年度主页于 2026-07-13 复查仍未获正式 CFP / dates；不创建虚构 CFP 或日期。
- 2022-2025 proceedings probe 均返回 Access denied，本轮以官方 program / track 页作为论文名录入口，以 DBLP `inproceedings` 作为已结束年度全 proceedings fallback 计数；该计数会混入 NIER、Tool Demo、Industry、Journal-first、workshop/co-hosted 等条目风险，不能当作 Research Papers 数量。
- 2026 Research Track 页面未列 abstract deadline，只列 paper submission；根表 abstract deadline 写 `未列出` 而非推测。
- ASE 2025 官方 Research Papers 页面显示 program / accepted papers 导航，但页面正文未给出可直接自动计数的主 track accepted list；后续如需主论文数量，应公开证据从 program filter 或 ACM DL proceedings 分册复核。

## 8. TIMELINE.md 同步提示

- 本 venue 当前已记录的 dated events 已同步至 [TIMELINE.md](../TIMELINE.md)；后续新增或修正 important dates 时，必须同步更新对应年度 README 与 `TIMELINE.md` 的事件发生年份章节。
- 本目录不再保留 worker 事件草稿文件；事实源以各年度 README 的“重要时间点”表与 `TIMELINE.md` 为准。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:25:00` | 常态化刷新：2026 行 Program / Accepted papers 由 `未公布` 改为官方 Research Track `Accepted Papers` 入口（名录已上线）；论文数量改为「名录已公布 / 计数待补」—— 页面过长、单次抓取被截断，**不得填具体数字**。camera-ready `2026-08-03` 已过，2026 主链已无可行动节点。 |
| `2026-07-13 19:13:21` | 常态化刷新：复核 ASE 2026 Research Track 大修、通知、camera-ready 与会期；2027/2028 未获正式年度信息，仅保守记录复查。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 09:40` | 根据 PR-2 结果复审补齐 ASE 核心人员情报的核验状态与核查时间列，并统一 TIMELINE 同步提示。 |
| `2026-06-05 08:38` | 初始化 ASE venue 根 README、2022-2028 年度索引、核心人员情报和多 track 计数口径说明。 |
