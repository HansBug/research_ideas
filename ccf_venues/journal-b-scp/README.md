# SCP README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | SCP |
| 全称 | Science of Computer Programming |
| 类型 | 期刊 |
| CCF 大类 | [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) |
| CCF 等级 | B（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版商 | Elsevier / ScienceDirect |
| ISSN | 0167-6423；eISSN 1872-7964（待 ScienceDirect / ISSN Portal 浏览器复核） |
| 期刊主页 | [ScienceDirect journal page](https://www.sciencedirect.com/journal/science-of-computer-programming) |
| Aims and scope | [ScienceDirect aims and scope](https://www.sciencedirect.com/journal/science-of-computer-programming/about/aims-and-scope)（CLI WAF/403；正文待人工浏览器核验） |
| Author guidelines | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors)；[ScienceDirect journal path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors)（CLI WAF/403；保留官方入口） |
| Submission system | [Editorial Manager default](https://www.editorialmanager.com/scico/default.aspx)；[Editorial Manager main page](https://www.editorialmanager.com/scico/mainpage.html) |
| Open access options | [Open access options](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/open-access-options)（CLI WAF/403；待浏览器核验） |
| Special issues / topical collections | [ScienceDirect special issues](https://www.sciencedirect.com/journal/science-of-computer-programming/special-issues)；[Calls for papers](https://www.sciencedirect.com/journal/science-of-computer-programming/about/call-for-papers)（CLI WAF/403；candidate CFP 不写成已核验事实） |
| Volume / issue archive | [ScienceDirect all issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（CLI WAF/403；DBLP baseline 仅作 fallback） |
| Articles in press / online first | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press)（CLI WAF/403；不得与卷期文章双算） |
| Editorial board | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/science-of-computer-programming/about/editorial-board)（CLI WAF/403；当前 roster 待人工浏览器核验） |
| DBLP venue page | [DBLP SCP](https://dblp.org/db/journals/scp/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现可命令行核验的官方年度卷期或 dated CFP |

> 核验 caveat：ScienceDirect / Elsevier 页面在当前 CLI 环境返回 WAF/403；Editorial Manager 正确代码为 `scico`，不得误用 `scp`（该代码指向其他期刊）。 因此本目录只把 ScienceDirect 链接作为官方入口；凡 CLI 无法读取正文的 scope、editorial roster、special issue deadline 和 guest editor 均标作“待人工浏览器核验”，不得写成已完成事实。

### 1.1 索引与分区信息

> 本节在 PR #91 中从 PR #90 占位推进为“证据链优先”的真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。JCR / CAS 若没有可追溯单刊证据，宁可写 `⏳`，不得用第三方站点补成分区事实。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🟡 | 沿用本库 CCF B 级；官方目录入口已定位，单条目仍需浏览器行级复核 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本 PR 不重新定义 CCF scope，只保留可点击官方基线入口 | `2026-06-09 13:52` |
| WoS Collection | ⏳ | 待人工核验 Web of Science Core Collection 收录集合 | [Clarivate Master Journal List](https://mjl.clarivate.com/search-results) 为官方检索入口；本轮命令行仅确认 SPA 入口可访问，未取得可审计单刊 `SCIE/SSCI/AHCI/ESCI` 行级结果；后续用 ISSN / eISSN 通过浏览器或机构入口复核 | `2026-06-09 13:52` |
| JCR Quartile | ⏳ | 待人工核验 2025 JCR 单刊 category / rank / quartile | [JCR 平台](https://jcr.clarivate.com/jcr/home)；[2025 JCR 发布说明](https://clarivate.com/news/clarivate-unveils-the-2025-journal-citation-reports/) 仅证明 release 存在，不证明本刊 quartile；需机构入口导出单刊 category、rank、quartile、percentile 后再改为 `1️⃣`--`4️⃣` | `2026-06-09 13:52` |
| CAS 分区 | ⏳ | 待人工核验中科院历史版分区 | [中国科学院文献情报中心停更公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 证明 2026 起不再更新发布；本轮未获得本刊历史版官方行级分区，后续只可用官方 / 机构历史版证据补写 | `2026-06-09 13:52` |
| EI / Compendex | 🟢 | 官方 Compendex `SERIALS` 精确命中，按 source-level 期刊记录 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本地 snapshot `compendex_source_list_2026-06-09.xlsx`，sheet `SERIALS`，Source title `Science of Computer Programming`，Source type `Journal`，ISSN `0167-6423`，EISSN `-`，Publisher `Elsevier B.V.` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | EI 已有官方 source-list 证据；WoS / JCR / CAS 仍待人工或机构入口核验 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；后续 reviewer 需复核本节链接与 source-list 字段 | `2026-06-09 13:52` |

## 2. Scope 与栏目

- 可复用方向线索：requirements、specification、design、validation、verification、programming、testing、maintenance、metrics、programming languages、CPS 与 Software Track / software artefact 相关方向；具体 Aims & Scope 以 ScienceDirect 浏览器可见正文为准。
- 常规投稿按 rolling submission 处理；只有人工浏览器核验到明确 deadline 的 special issue / topical collection 才能进入 [../TIMELINE.md](../TIMELINE.md) dated event 与 Mermaid。
- Article type、字数、伦理与 artefact 要求以官方 Guide for Authors 浏览器可见正文为准；当前 CLI 仅确认官方入口，不能替代正文核验。

## 3. 核心编辑人员情报

本节只记录当前能稳妥维护的官方 roster 入口。由于 ScienceDirect editorial board 在当前 CLI 环境返回 WAF/403，本 PR 不臆造 Editor-in-Chief / Associate Editor / Editorial Board 名单；待人工浏览器打开官方 editorial board 后再补姓名、角色、研究方向与近年论文入口。

| 姓名 | 期刊角色 | 单位 | 角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| 待人工浏览器核验 | Editor-in-Chief / Editorial Board leadership | 待人工浏览器核验 | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/science-of-computer-programming/about/editorial-board) | 待官方 roster 核验后补 | 待官方 roster 核验后补 | 待官方 roster 核验后补 | P1/P2/P3/P4 相关，人员画像待补 | ⏳ ScienceDirect 官方当前 roster 待人工浏览器核验；CLI WAF/403 | `2026-06-05 18:24` |

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中相关 | 中相关：形式化 DSL、状态机建模工具、可执行 artefact 和 MBSE 工具链可进入 Software Track。 |
| P2 场景与性质生成 | 强相关 | 强相关：specification、validation、verification 与程序 / 规约性质直接相关。 |
| P3 验证剖面与模型检查 | 强相关 | 强相关：model checking、formal / semi-formal techniques、CPS verification 与工具 artefact 是核心线索。 |
| P4 模型修复 | 强相关 | 强相关：verification-guided repair、program synthesis、fault localization 与工具化评估适合 SCP。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [ScienceDirect journal page](https://www.sciencedirect.com/journal/science-of-computer-programming) | CLI WAF/403；保留官方链接，需浏览器核验正文 | `2026-06-05 18:24` |
| Aims and scope | [ScienceDirect aims and scope](https://www.sciencedirect.com/journal/science-of-computer-programming/about/aims-and-scope) | CLI WAF/403；不以第三方 scope 替代 | `2026-06-05 18:24` |
| Author guidelines | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors)；[ScienceDirect journal path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | CLI WAF/403；官方入口已定位 | `2026-06-05 18:24` |
| Submission system | [Editorial Manager default](https://www.editorialmanager.com/scico/default.aspx)；[Editorial Manager main page](https://www.editorialmanager.com/scico/mainpage.html) | 入口可能需登录；只记录官方投稿入口 | `2026-06-05 18:24` |
| Special issues / topical collections | [ScienceDirect special issues](https://www.sciencedirect.com/journal/science-of-computer-programming/special-issues)；[Calls for papers](https://www.sciencedirect.com/journal/science-of-computer-programming/about/call-for-papers) | CLI WAF/403；未人工核验前不生成 dated event | `2026-06-05 18:24` |
| Volume / issue archive | [ScienceDirect all issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues) | publisher archive 优先；CLI WAF/403 时用 DBLP baseline 作 fallback | `2026-06-05 18:24` |
| Articles in press / online first | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | 会迁移到卷期；年度计数不得双算 | `2026-06-05 18:24` |
| Editorial board | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/science-of-computer-programming/about/editorial-board) | CLI WAF/403；待人工浏览器核验当前 roster | `2026-06-05 18:24` |
| DBLP venue | [DBLP SCP](https://dblp.org/db/journals/scp/index.html) | 仅作 bibliographic / count fallback | `2026-06-05 18:24` |

## 6. 年度信息汇总

年度汇总表必须把期刊主页、author guidelines、submission system、special issue、volume / issue、online first、DBLP 等核心 URL 直接挂进表格。论文数量当前只采用 DBLP `entry article` baseline 或 `未公布`，不等同于 publisher article-type 闭合数。

| 年份 | 年度状态 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Articles / Online first | DBLP 年度页 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| [`2028`](./2028/README.md) | 🟢 rolling 入口开放；年度卷期 / dated CFP 未公布 | [SCP](https://www.sciencedirect.com/journal/science-of-computer-programming) | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/scico/default.aspx) / [main page](https://www.editorialmanager.com/scico/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（未发现官方年度卷期 / DBLP 年度 volume） | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | [DBLP index](https://dblp.org/db/journals/scp/index.html) | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | 🟢 rolling 入口开放；年度卷期 / dated CFP 未公布 | [SCP](https://www.sciencedirect.com/journal/science-of-computer-programming) | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/scico/default.aspx) / [main page](https://www.editorialmanager.com/scico/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（未发现官方年度卷期 / DBLP 年度 volume） | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | [DBLP index](https://dblp.org/db/journals/scp/index.html) | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟢 rolling 入口开放；年度卷期 / dated CFP 未公布 | [SCP](https://www.sciencedirect.com/journal/science-of-computer-programming) | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/scico/default.aspx) / [main page](https://www.editorialmanager.com/scico/mainpage.html) | [FSEN 2025 extended versions](https://www.sciencedirect.com/special-issue/327466/fundamentals-of-software-engineering-extended-versions-of-selected-papers-of-fsen-2025)；[ICFEM 2025 selected software](https://www.sciencedirect.com/special-issue/328870/selected-software-from-the-26th-international-conference-on-formal-engineering-methods)（候选线索；deadline / guest editors 待浏览器核验，当前不进 TIMELINE dated event） | 滚动投稿；候选 special issue deadline 待浏览器核验 | [All issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（Vols. 248-253（DBLP baseline；年度进行中）） | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | [DBLP index](https://dblp.org/db/journals/scp/index.html) | DBLP `entry article` baseline: 62 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 年度已归档 | [SCP](https://www.sciencedirect.com/journal/science-of-computer-programming) | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/scico/default.aspx) / [main page](https://www.editorialmanager.com/scico/mainpage.html) | [NLBSE’25 selected software / articles](https://www.sciencedirect.com/journal/science-of-computer-programming/special-issues)（候选线索；deadline / guest editors 待浏览器核验，当前不进 TIMELINE dated event） | 滚动投稿；候选 special issue deadline 待浏览器核验 | [All issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（Vols. 239-247） | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | [DBLP index](https://dblp.org/db/journals/scp/index.html) | DBLP `entry article` baseline: 113 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 年度已归档 | [SCP](https://www.sciencedirect.com/journal/science-of-computer-programming) | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/scico/default.aspx) / [main page](https://www.editorialmanager.com/scico/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（Vols. 231-238） | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | [DBLP index](https://dblp.org/db/journals/scp/index.html) | DBLP `entry article` baseline: 109 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 年度已归档 | [SCP](https://www.sciencedirect.com/journal/science-of-computer-programming) | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/scico/default.aspx) / [main page](https://www.editorialmanager.com/scico/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（Vols. 225-230） | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | [DBLP index](https://dblp.org/db/journals/scp/index.html) | DBLP `entry article` baseline: 64 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 年度已归档 | [SCP](https://www.sciencedirect.com/journal/science-of-computer-programming) | [Guide for Authors](https://www.sciencedirect.com/science/journal/01676423/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/science-of-computer-programming/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/scico/default.aspx) / [main page](https://www.editorialmanager.com/scico/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/science-of-computer-programming/issues)（Vols. 213-224） | [Articles in Press](https://www.sciencedirect.com/journal/science-of-computer-programming/articles-in-press) | [DBLP index](https://dblp.org/db/journals/scp/index.html) | DBLP `entry article` baseline: 79 | 🟡 部分核验 |

## 7. 维护备注

- 常规投稿按 rolling submission 处理，不进入 dated Mermaid。
- 2027/2028/2029+ 未发现可命令行核验的官方年度卷期或 dated CFP；不预设未来卷号。
- ScienceDirect 与 DBLP 对年度 volume / article 归属可能存在差异；publisher all issues / special issue 页面优先，DBLP 只作 bibliographic fallback。
- Articles in Press 是 online-first 状态，会迁移到正式卷期；年度计数不得与卷期文章双算。
- Candidate special issue URL 只能作为后续浏览器复核入口；deadline、guest editor、状态未核验前不得同步到 [../TIMELINE.md](../TIMELINE.md) dated event。

## 8. TIMELINE.md 同步提示

- 常规 rolling submission 已按“期刊滚动投稿 / 未定日期”规则同步到 [../TIMELINE.md](../TIMELINE.md)。
- 本 PR 未将 ScienceDirect candidate special issue 线索写入 dated timeline；后续只有在浏览器核验到明确 deadline 后，才同步 [../TIMELINE.md](../TIMELINE.md) 的年度表格和 Mermaid。
- 后续若发现新的 dated CFP、special issue deadline 或年度卷期闭合信息，应同步维护本目录、[../TIMELINE.md](../TIMELINE.md) 与 [../SUMMARY.md](../SUMMARY.md)。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 18:24` | PR-8 review 前自查修复：因 ScienceDirect / Elsevier CLI WAF/403，将 editorial roster、scope 正文与 candidate special issue deadline 降级为待人工浏览器核验，避免把未核验事实写入 TIMELINE。 |
| `2026-06-05 18:05` | PR-8 初始化 SCP 期刊 README，记录 ScienceDirect 官方入口、2022-2028 年度汇总和 ScienceDirect / DBLP 计数口径风险。 |
