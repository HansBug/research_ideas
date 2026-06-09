# ICECCS README

> 信息更新时间：`2026-06-09 18:18:06`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ICECCS |
| 全称 | International Conference on Engineering of Complex Computer Systems |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录入口](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；CLI 可能触发 WAF，正文未获公开可审计正文） |
| CCF 等级 | 🥉 |
| 出版方 | IEEE CPS / IEEE Xplore（2022/2023）；Springer LNCS 线索（2025/2026）；2024 待复核 |
| 官方 series page | 待补（未发现稳定 official series page；年度事实以年度主页为准） |
| 官方当前 / 最新年度主页 | [ICECCS 2026](https://formal-analysis.com/iceccs/2026/) |
| 官方 CFP / Important Dates 总入口 | [ICECCS 2026 submission section](https://formal-analysis.com/iceccs/2026/#submission) / [ICECCS 2026 dates](https://formal-analysis.com/iceccs/2026/#dates) |
| 官方 proceedings / paper list 总入口 | 未公布；曾检索到 `ICECCS_2026_Accepted_Papers.txt` candidate，但 2026-06-07 CLI `curl -I` 返回 404，待补 / 不作 official paper-list 链接 |
| DBLP venue page | [DBLP ICECCS](https://dblp.org/db/conf/iceccs/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；未公布未来年度不预造 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF 🥉 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `Proceedings - 2012 IEEE 17th International Conference on Engineering of Complex Computer Systems, ICECCS 2012`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核本节链接与 source-list 字段，尤其不能把 book-series 线索升级为 venue-level EI 事实 | `2026-06-09 16:20` |

## 2. Scope 与方向

ICECCS 聚焦 complex computer-based systems / complex computer systems 的工程理论、方法、语言、工具与工业案例，覆盖 requirements analysis and specification、verification and validation、formal engineering methods、reliability / safety-critical / fault-tolerant architectures、cyber-physical systems、IoT、software architecture、adaptive / self-managing systems 与 industrial case studies。

本库将 ICECCS 作为 CCF 🥉 的 P2/P3 邻近观察与工程案例来源，不升级为 P0/P1 主投目标。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中 | 可作为复杂系统工程、需求规约、控制 / 嵌入式 / CPS 案例来源；不是专门状态机建模 venue。 |
| P2 场景与性质生成 | 中 | verification / validation、requirements / specification、case study 可抽取验证场景与性质。 |
| P3 验证剖面与模型检查 | 中 | formal engineering methods、model checking、runtime verification、safety / reliability 可支撑验证 profile。 |
| P4 模型修复 | 中低 | repair / fault localization / feedback-guided improvement 只在个别论文中出现，需二次筛选。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | 待补（未发现稳定 official series page；年度事实以年度主页为准） | 若长期站访问异常，年度事实以年度 official site 为准 | `2026-06-07 12:47` |
| Latest year homepage | [ICECCS 2026](https://formal-analysis.com/iceccs/2026/) | future 年度未公布时写 `⏳ 已检索未公布` | `2026-06-07 12:47` |
| CFP / Call for Papers | [ICECCS 2026 submission section](https://formal-analysis.com/iceccs/2026/#submission) | 若分 track，年度页展开 | `2026-06-07 12:47` |
| Important Dates | [ICECCS 2026 dates](https://formal-analysis.com/iceccs/2026/#dates) | 可与 CFP 同页 | `2026-06-07 12:47` |
| Submission system | [EasyChair ICECCS 2026](https://easychair.org/conferences/?conf=iceccs2026) | 只能证明投稿入口，不替代 CFP / dates | `2026-06-07 12:47` |
| Program / accepted papers | 未公布；404 candidate 已降级为待补风险 | 已结束年度优先 official accepted/program；不得把 404 candidate 写成 official paper-list | `2026-06-07 13:33` |
| Proceedings | 未公布 / Springer LNCS 待补 | publisher / DBLP fallback 分开 | `2026-06-07 12:47` |
| DBLP venue | [DBLP ICECCS](https://dblp.org/db/conf/iceccs/index.html) | 仅作论文名录 / 计数 fallback | `2026-06-07 12:47` |

## 5. 核心人员情报

> 人员角色以年度 official committee / editorial pages 为准；DBLP / 个人主页只补研究方向与代表作。不要把 invited speaker、guest editor 或普通 PC member 升级为 chair / steering。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Shaoying Liu | 2022 / conference | General Chair | Hiroshima University | [ICECCS 2022 committee](http://iceccs2022.xsrv.jp/#committee) | [DBLP](https://dblp.org/pid/l/ShaoyingLiu.html) | formal methods、SOFL、software engineering methodology | [DBLP 近年论文入口](https://dblp.org/pid/l/ShaoyingLiu.html) | P1-P4 均相关 | 🟡 部分核验 | `2026-06-07 12:47` |
| Zhi Jin | 2022 / conference | General Chair | Peking University | [ICECCS 2022 committee](http://iceccs2022.xsrv.jp/#committee) | [DBLP](https://dblp.org/pid/j/ZhiJin.html) | requirements engineering、software engineering | [DBLP 近年论文入口](https://dblp.org/pid/j/ZhiJin.html) | P1/P2 相关 | 🟡 部分核验 | `2026-06-07 12:47` |
| Étienne André | 2023 / committee | committee / program role 线索 | Université de Lorraine / LORIA | [ICECCS 2023 committee](https://www.irit.fr/iceccs2023/#committee) | [DBLP](https://dblp.org/pid/49/2992.html) | timed automata、model checking、formal methods | [DBLP 近年论文入口](https://dblp.org/pid/49/2992.html) | P1/P2/P3 强 | 🟡 部分核验 | `2026-06-07 12:47` |
| Huibiao Zhu | 2025 / steering / chair role 线索 | Steering / general / program role 线索 | East China Normal University | [ICECCS 2025 committee](https://iceccs2025-hangzhou.github.io/#committee) | [DBLP](https://dblp.org/pid/76/1462.html) | formal methods、semantics、CPS | [DBLP 近年论文入口](https://dblp.org/pid/76/1462.html) | P1/P3 相关 | 🟡 部分核验 | `2026-06-07 12:47` |
| Jonathan Bowen | 2025 / steering | Steering Committee | London South Bank University | [ICECCS 2025 committee](https://iceccs2025-hangzhou.github.io/#committee) | [DBLP](https://dblp.org/pid/b/JonathanPBowen.html) | formal methods、software engineering history | [DBLP 近年论文入口](https://dblp.org/pid/b/JonathanPBowen.html) | P1/P3 背景相关 | 🟡 部分核验 | `2026-06-07 12:47` |
| Yamine Ait Ameur | 2026 / program | Program Co-Chair | IRIT / ENSEEIHT | [ICECCS 2026 committee](https://formal-analysis.com/iceccs/2026/#committee) | [DBLP](https://dblp.org/pid/a/YamineAitAmeur.html) | formal methods、Event-B、verification | [DBLP 近年论文入口](https://dblp.org/pid/a/YamineAitAmeur.html) | P1/P3 相关 | 🟡 部分核验 | `2026-06-07 12:47` |
| Zhenhua Duan | 2026 / program | Program Co-Chair | Xidian University | [ICECCS 2026 committee](https://formal-analysis.com/iceccs/2026/#committee) | [DBLP](https://dblp.org/pid/80/2625.html) | formal methods、temporal logic、verification | [DBLP 近年论文入口](https://dblp.org/pid/80/2625.html) | P2/P3 相关 | 🟡 部分核验 | `2026-06-07 12:47` |

## 6. 年度信息汇总

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | Camera-ready | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ICECCS index](https://dblp.org/db/conf/iceccs/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ICECCS index](https://dblp.org/db/conf/iceccs/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🟢 投稿中 | [ICECCS 2026](https://formal-analysis.com/iceccs/2026/) | [Submission section](https://formal-analysis.com/iceccs/2026/#submission) | [Important Dates](https://formal-analysis.com/iceccs/2026/#dates) | [EasyChair ICECCS 2026](https://easychair.org/conferences/?conf=iceccs2026) | 未公布；404 candidate 已降级为待补风险 | 未公布；官网说明 planned Springer LNCS | [DBLP ICECCS index](https://dblp.org/db/conf/iceccs/index.html) | 2026-06-29 待补时刻 | 2026-07-06 待补时刻 | 2026-08-17 待补时刻 | 2026-08-31 待补时刻 | 2026-11-23..2026-11-24（Brisbane, Australia） | 未公布；accepted-list candidate 2026-06-07 CLI 404 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [ICECCS 2025](https://iceccs2025-hangzhou.github.io/) | [Submission and Publication](https://iceccs2025-hangzhou.github.io/#submissionandpublication) | [Important Dates](https://iceccs2025-hangzhou.github.io/#importantdates) | [EasyChair ICECCS 2025](https://easychair.org/conferences/?conf=iceccs2025) | [Program](https://iceccs2025-hangzhou.github.io/#program) / [Program PDF](https://iceccs2025-hangzhou.github.io/Program.pdf) | 官网说明 Springer LNCS；具体 Springer volume URL 待补 | [DBLP ICECCS index](https://dblp.org/db/conf/iceccs/index.html) | 2025-01-28 待补时刻 AoE | 2025-02-11 待补时刻 AoE | 2025-04-04 待补时刻 AoE | 2025-05-02 待补时刻 AoE | 2025-07-02..2025-07-04 UTC+8 | 待按 official program / proceedings / DBLP 分口径计数 | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 / 待补 | 待补；候选 `https://cyprusconferences.org/iceccs2024/` 当前 CLI 404 | 待补 | 待补 | 待补 | 待补 | 待补 | [DBLP ICECCS index](https://dblp.org/db/conf/iceccs/index.html) | 待补 | 待补 | 待补 | 待补 | 待补 | 待 DBLP / proceedings 复核 | ⏳ 待核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [ICECCS 2023](https://www.irit.fr/iceccs2023/) | [Submission section](https://www.irit.fr/iceccs2023/#submission) | [Important Dates](https://www.irit.fr/iceccs2023/#dates) | [EasyChair ICECCS 2023](https://easychair.org/conferences/?conf=iceccs2023) | [Accepted Papers](https://www.irit.fr/iceccs2023/#acceptedpapers) | [Local proceedings page](https://www.irit.fr/iceccs2023/doc/proc.html)；IEEE Xplore 待补 | [DBLP ICECCS index](https://dblp.org/db/conf/iceccs/index.html) | 2023-01-16 待补时刻 | 2023-01-16 待补时刻 | 2023-03-15 待补时刻 | 2023-04-15 待补时刻 | 2023-06-14..2023-06-16 | 待从 accepted/proceedings/DBLP 分口径计数 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [ICECCS 2022](http://iceccs2022.xsrv.jp/) | [Scope / CFP](http://iceccs2022.xsrv.jp/#scope) | [Important Dates](http://iceccs2022.xsrv.jp/#dates) | [EasyChair ICECCS 2022](https://easychair.org/conferences/?conf=iceccs2022) | [Accepted Papers](http://iceccs2022.xsrv.jp/#accepted%20papers) / [Program PDF](http://iceccs2022.xsrv.jp/ICECCS2022WholeConferenceProgram_FinalforUse_WithZoomURL_videoPresentationLink.pdf) | IEEE Xplore URL 待补；页面 stale 2019 proceedings link 不复用 | [DBLP ICECCS index](https://dblp.org/db/conf/iceccs/index.html) | 2021-10-01 待补时刻 | 2021-10-15 待补时刻 | 2021-12-20 待补时刻 | 2022-01-28 待补时刻 | 2022-03-26..2022-03-30 | official accepted page lists regular + short papers；exact count 待复核 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 未发现稳定 official series page；不要用 DBLP venue index 或第三方 deadline 聚合页冒充 official series。
- 2024 候选 annual site 当前 CLI 返回 404，CFP / dates / submission / proceedings 继续待补，不进入 TIMELINE。
- 2026 accepted-list candidate `ICECCS_2026_Accepted_Papers.txt` 在 2026-06-07 CLI `curl -I` 返回 404，不得作为 official Program / Accepted papers 链接；后续若发布再恢复。
- 2022 年度页含 stale 2019 proceedings link，不得复用为 2022 proceedings；IEEE CLI WAF/418 只能说明命令行访问受限。
- ICECCS 是 CCF 🥉 补充观察与工程案例来源，不把 complex systems 全量论文自动标为 LLM4Modeling 强相关。

## 8. 证据与核查记录

| 类型 | 链接 | 核查时间 | 结论 |
|---|---|---|---|
| CCF official entry | [CCF TCSE_SS_PDL](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) | `2026-06-07 12:47` | 官方入口已定位；CLI 可能触发 WAF / 动态页，正文与第七版状态未获公开可审计正文。 |
| 非官方 CCF 镜像线索 | [ccf.atom.im](https://ccf.atom.im/) | `2026-06-07 12:47` | 仅作机器检索 / 差集筛查线索，不作为 CCF 官方事实。 |
| Official annual pages | [ICECCS 2026](https://formal-analysis.com/iceccs/2026/) / [ICECCS 2025](https://iceccs2025-hangzhou.github.io/) / [ICECCS 2023](https://www.irit.fr/iceccs2023/) / [ICECCS 2022](http://iceccs2022.xsrv.jp/) | `2026-06-07 12:47` | 2022/2023/2025/2026 年度 official chain 已定位；2024 official annual site 待补。 |
| 2024 candidate | `https://cyprusconferences.org/iceccs2024/` | `2026-06-07 12:47` | 当前 CLI 返回 404 / page-not-found，不写作已核验官方主页。 |
| DBLP fallback | [DBLP ICECCS](https://dblp.org/db/conf/iceccs/index.html) | `2026-06-07 12:47` | 仅作 bibliographic fallback；IEEE / Springer proceedings 待 publisher 或公开证据复核。 |

## 9. TIMELINE.md 同步提示

- 本 venue 已核验 dated events 已同步至 [../TIMELINE.md](../TIMELINE.md) 对应年份表格与 PR #63 Mermaid 分片。
- 未公布年度、第三方线索、WAF / 404 / CAPTCHA 候选页不得进入 dated TIMELINE / Mermaid。

## 10. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-07 13:33` | 修复实现后 review：降级 ICECCS 2026 accepted-list 404 candidate，补入 2026-11-23..2026-11-24 Brisbane 会期并同步 TIMELINE。 |
| `2026-06-07 12:47` | PR #63 初始化 ICECCS 情报，补充 CCF / official / DBLP 证据、2022--2028 年度索引、核心人员、TIMELINE 同步和待补口径。 |
