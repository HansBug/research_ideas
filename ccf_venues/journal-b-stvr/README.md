# STVR README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | STVR |
| 全称 | Software Testing, Verification and Reliability |
| 类型 | 期刊 |
| CCF 大类 | [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) |
| CCF 等级 | B（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版商 | [Wiley / Wiley Online Library](https://onlinelibrary.wiley.com/journal/10991689) |
| ISSN | 待人工浏览器核验（[Wiley STVR 期刊主页](https://onlinelibrary.wiley.com/journal/10991689)；CLI 命令行访问返回 WAF/403） |
| 期刊主页 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) |
| Aims and scope | [Wiley product information / aims scope](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/productinformation.html)（CLI WAF/403，需浏览器核验正文） |
| Author guidelines | [Wiley STVR for authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html)；[Wiley Authors STVR dashboard](https://authors.wiley.com/dashboard/journal?groupCode=STVR) |
| Submission system | [Wiley Authors STVR dashboard](https://authors.wiley.com/dashboard/journal?groupCode=STVR)；[Wiley submission candidate for STVR](https://submission.wiley.com/submission/submissionBoard/new/?journalCode=STVR) |
| Editorial board | [Wiley STVR editorial board](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/editorialboard.html)（CLI WAF/403，需人工浏览器核验） |
| Special issues / topical collections | [Wiley STVR 期刊主页](https://onlinelibrary.wiley.com/journal/10991689)；当前未发现可命令行核验的 active dated CFP |
| Volume / issue archive | [Wiley STVR volumes and issues](https://onlinelibrary.wiley.com/loi/10991689) |
| Articles in press / online first | [Wiley STVR Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) |
| DBLP venue page | [DBLP STVR](https://dblp.org/db/journals/stvr/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现可命令行核验的官方年度卷期 / dated CFP；Wiley 官方页需浏览器复核 |

> Wiley 官方页面在当前 CLI 环境中多次返回 Cloudflare/Wiley WAF `403 Just a moment...`。本目录保留 Wiley 官方链接作为事实核验入口；凡无法在 CLI 中读取正文的字段均显式标注“待人工浏览器核验”，不以第三方页面替代 Wiley 官方事实。

### 1.1 索引与分区信息

> 本节在 PR #91 中从 PR #90 占位推进为“证据链优先”的真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。JCR / CAS 若没有可追溯单刊证据，宁可写 `⏳`，不得用第三方站点补成分区事实。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🟡 | 沿用本库 CCF B 级；官方目录入口已定位，单条目仍需浏览器行级复核 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本 PR 不重新定义 CCF scope，只保留可点击官方基线入口 | `2026-06-09 13:52` |
| WoS Collection | ⏳ | 待人工核验 Web of Science Core Collection 收录集合 | [Clarivate Master Journal List](https://mjl.clarivate.com/search-results) 为官方检索入口；本轮命令行仅确认 SPA 入口可访问，未取得可审计单刊 `SCIE/SSCI/AHCI/ESCI` 行级结果；后续用 ISSN / eISSN 通过浏览器或机构入口复核 | `2026-06-09 13:52` |
| JCR Quartile | ⏳ | 待人工核验 2025 JCR 单刊 category / rank / quartile | [JCR 平台](https://jcr.clarivate.com/jcr/home)；[2025 JCR 发布说明](https://clarivate.com/news/clarivate-unveils-the-2025-journal-citation-reports/) 仅证明 release 存在，不证明本刊 quartile；需机构入口导出单刊 category、rank、quartile、percentile 后再改为 `1️⃣`--`4️⃣` | `2026-06-09 13:52` |
| CAS 分区 | ⏳ | 待人工核验中科院历史版分区 | [中国科学院文献情报中心停更公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 证明 2026 起不再更新发布；本轮未获得本刊历史版官方行级分区，后续只可用官方 / 机构历史版证据补写 | `2026-06-09 13:52` |
| EI / Compendex | 🟢 | 官方 Compendex `SERIALS` 精确命中，按 source-level 期刊记录 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本地 snapshot `compendex_source_list_2026-06-09.xlsx`，sheet `SERIALS`，Source title `Software Testing Verification and Reliability`，Source type `Journal`，ISSN `0960-0833`，EISSN `1099-1689`，Publisher `John Wiley and Sons Ltd` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | EI 已有官方 source-list 证据；WoS / JCR / CAS 仍待人工或机构入口核验 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；后续 reviewer 需复核本节链接与 source-list 字段 | `2026-06-09 13:52` |

## 2. Scope 与栏目

- 题名与 CCF 收录位置显示 STVR 面向 software testing、verification、reliability 方向；具体 aims / scope 以 [Wiley product information](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/productinformation.html) 浏览器可见正文为准。
- 投稿与栏目类型以 [Wiley STVR for authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) 与 [Wiley Authors STVR dashboard](https://authors.wiley.com/dashboard/journal?groupCode=STVR) 为准；CLI 当前只能确认官方入口存在，不能读取完整正文。
- 常规投稿按期刊 rolling submission 处理；若 Wiley 后续公布 special issue / topical collection 的明确 deadline，应同步更新本 README、对应年度 README 和 [../TIMELINE.md](../TIMELINE.md)。

## 3. 核心编辑人员情报

本节只记录可验证的当前 editorial leadership。由于 [Wiley STVR editorial board](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/editorialboard.html) 在 CLI 环境返回 WAF/403，当前不臆造 Editor-in-Chief、Co-Editor-in-Chief、Associate Editor 或 Managing Editor 名单；待人工浏览器打开官方 editorial board 后再补。

| 姓名 | 期刊角色 | 单位 | 角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| 待人工浏览器核验 | Editor-in-Chief / Editorial Board leadership | 待人工浏览器核验 | [Wiley STVR editorial board](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/editorialboard.html) | 待官方 roster 核验后补 | 待官方 roster 核验后补 | 待官方 roster 核验后补 | P2/P3 强相关，人员画像待补 | ⏳ Wiley 官方当前 roster 待人工浏览器核验；CLI WAF/403 | `2026-06-05 12:05` |

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中相关 | 若论文强调测试模型、行为模型或建模驱动测试，可作为邻近发表与检索入口。 |
| P2 场景与性质生成 | 强相关 | STVR 题名中的 testing / verification 与测试场景、性质生成、oracle 与需求到测试链路直接相关。 |
| P3 验证剖面与模型检查 | 强相关 | verification / reliability 与模型检查、验证剖面、形式化验证和可靠性证据链直接相关。 |
| P4 模型修复 | 中相关 | repair 若以测试、验证反馈或可靠性改善为评价目标，可作为候选期刊方向。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | CLI WAF/403；保留官方链接，需浏览器核验正文 | `2026-06-05 12:05` |
| Aims and scope | [Wiley product information / aims scope](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/productinformation.html) | CLI WAF/403；不以第三方 scope 替代 | `2026-06-05 12:05` |
| Author guidelines | [Wiley STVR for authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html)；[Wiley Authors STVR dashboard](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | Wiley Authors SPA 可访问但正文需前端渲染；Wiley Online Library for-authors CLI WAF/403 | `2026-06-05 12:05` |
| Submission system | [Wiley Authors STVR dashboard](https://authors.wiley.com/dashboard/journal?groupCode=STVR)；[Wiley submission candidate for STVR](https://submission.wiley.com/submission/submissionBoard/new/?journalCode=STVR) | Submission SPA 可访问但具体表单需前端/登录核验 | `2026-06-05 12:05` |
| Editorial board | [Wiley STVR editorial board](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/editorialboard.html) | CLI WAF/403；待人工浏览器核验当前 roster | `2026-06-05 12:05` |
| Special issues / topical collections | [Wiley STVR 期刊主页](https://onlinelibrary.wiley.com/journal/10991689) | 未发现可命令行核验的 active dated CFP；Wiley 主页仍需浏览器复核 | `2026-06-05 12:05` |
| Volume / issue archive | [Wiley STVR volumes and issues](https://onlinelibrary.wiley.com/loi/10991689) | 年度 DBLP 页作为 bibliographic / count fallback | `2026-06-05 12:05` |
| Articles in press / online first | [Wiley STVR Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | CLI WAF/403；待浏览器确认 Early View 当前内容 | `2026-06-05 12:05` |
| DBLP venue | [DBLP STVR](https://dblp.org/db/journals/stvr/index.html) | 仅作论文名录 / 年度计数 fallback | `2026-06-05 12:05` |

## 6. 年度信息汇总

年度论文数量采用 DBLP entry article baseline 口径：`2025=17`、`2024=26`、`2023=25`、`2022=31`；2026 DBLP 年度页未公布 / 待补，不写闭合数。

| 年份 | 年度状态 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Articles / Online first | DBLP 年度页 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| [`2028`](./2028/README.md) | 🟢 滚动开放 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | [For authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) | [Wiley Authors](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | 无已知 | 滚动投稿 | ⏳ 已检索未公布 | [Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 🟡 部分核验；Wiley CLI WAF/403 |
| [`2027`](./2027/README.md) | 🟢 滚动开放 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | [For authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) | [Wiley Authors](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | 无已知 | 滚动投稿 | ⏳ 已检索未公布 | [Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 🟡 部分核验；Wiley CLI WAF/403 |
| [`2026`](./2026/README.md) | 🟢 滚动开放 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | [For authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) | [Wiley Authors](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | 无已知 | 滚动投稿 | [Wiley volume archive](https://onlinelibrary.wiley.com/loi/10991689)（年度卷期待浏览器核验） | [Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | ⏳ 未公布 / 待补 | ⏳ 未公布 / 待补 | 🟡 部分核验；DBLP 年度页未发布 |
| [`2025`](./2025/README.md) | ✅ 年度已归档 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | [For authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) | [Wiley Authors](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | 无已知 | 滚动投稿 | [Wiley Vol.35 Issue 1](https://onlinelibrary.wiley.com/toc/10991689/2025/35/1) | [Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | [DBLP Vol.35](https://dblp.org/db/journals/stvr/stvr35.html) | 17 | 🟡 部分核验；Wiley CLI WAF/403 |
| [`2024`](./2024/README.md) | ✅ 年度已归档 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | [For authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) | [Wiley Authors](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | 无已知 | 滚动投稿 | [Wiley Vol.34 Issue 1](https://onlinelibrary.wiley.com/toc/10991689/2024/34/1) | [Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | [DBLP Vol.34](https://dblp.org/db/journals/stvr/stvr34.html) | 26 | 🟡 部分核验；Wiley CLI WAF/403 |
| [`2023`](./2023/README.md) | ✅ 年度已归档 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | [For authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) | [Wiley Authors](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | 无已知 | 滚动投稿 | [Wiley Vol.33 Issue 1](https://onlinelibrary.wiley.com/toc/10991689/2023/33/1) | [Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | [DBLP Vol.33](https://dblp.org/db/journals/stvr/stvr33.html) | 25 | 🟡 部分核验；Wiley CLI WAF/403 |
| [`2022`](./2022/README.md) | ✅ 年度已归档 | [Wiley STVR](https://onlinelibrary.wiley.com/journal/10991689) | [For authors](https://onlinelibrary.wiley.com/page/journal/10991689/homepage/forauthors.html) | [Wiley Authors](https://authors.wiley.com/dashboard/journal?groupCode=STVR) | 无已知 | 滚动投稿 | [Wiley Vol.32 Issue 1](https://onlinelibrary.wiley.com/toc/10991689/2022/32/1) | [Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview) | [DBLP Vol.32](https://dblp.org/db/journals/stvr/stvr32.html) | 31 | 🟡 部分核验；Wiley CLI WAF/403 |

## 7. 维护备注

- STVR 常规投稿按 rolling submission 处理，不进入 dated Mermaid。
- 当前未发现 2022-2028 active dated special issue / topical collection CFP；若后续发现 Wiley 官方 CFP，需新增 dated event 并同步 [../TIMELINE.md](../TIMELINE.md)。
- `2029+` 检索结论：已检查 [Wiley STVR volumes and issues](https://onlinelibrary.wiley.com/loi/10991689)、[Wiley STVR Early View](https://onlinelibrary.wiley.com/journal/10991689/earlyview)、[Wiley STVR 期刊主页](https://onlinelibrary.wiley.com/journal/10991689) 与 [DBLP STVR](https://dblp.org/db/journals/stvr/index.html)；CLI 受 Wiley WAF/403 限制，未发现可命令行核验的 `2029+` 年度卷期或 dated CFP，需人工浏览器复核。
- 2022-2025 年度论文数量为 DBLP `entry article` baseline，不等同于 Wiley publisher article-type 闭合数；后续需用 Wiley volume / issue 页面浏览器核验 editorial、erratum、front matter 等是否纳入。
- 2026 DBLP 年度页尚未公布；[DBLP STVR](https://dblp.org/db/journals/stvr/index.html) 目前未提供 2026 年度 volume 页，本目录不预设闭合论文数量。

## 8. TIMELINE.md 同步提示

- STVR 常规 rolling submission 按“期刊滚动投稿 / 未定日期”规则维护；当前无 dated event 需要写入 Mermaid。
- 当前没有 STVR dated special issue / topical collection deadline，因此不新增 Mermaid milestone。
- 后续若发现 Wiley 官方 dated CFP、special issue deadline 或年度卷期闭合信息，应同步维护本目录、[../TIMELINE.md](../TIMELINE.md) 与 [../SUMMARY.md](../SUMMARY.md)。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 14:28` | 实现后 review 收尾：补齐 CCF 等级字段的官方目录链接，与 REJ / STTT 同批次口径对齐。 |
| `2026-06-05 12:05` | 初始化 STVR 期刊 README，记录 Wiley 官方入口、DBLP entry article baseline、WAF/403 caveat、2022-2028 年度汇总与 2029+ 检索结论。 |
