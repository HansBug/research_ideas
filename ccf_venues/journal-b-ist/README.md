# IST README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | IST |
| 全称 | Information and Software Technology |
| 类型 | 期刊 |
| CCF 大类 | [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) |
| CCF 等级 | B（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版商 | Elsevier / ScienceDirect |
| ISSN | 0950-5849；eISSN 1873-6025（待 ScienceDirect / ISSN Portal 公开可审计复核） |
| 期刊主页 | [ScienceDirect journal page](https://www.sciencedirect.com/journal/information-and-software-technology) |
| Aims and scope | [ScienceDirect aims and scope](https://www.sciencedirect.com/journal/information-and-software-technology/about/aims-and-scope)（CLI WAF/403；正文未获公开可审计正文） |
| Author guidelines | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors)；[ScienceDirect journal path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors)（CLI WAF/403；保留官方入口） |
| Submission system | [Editorial Manager default](https://www.editorialmanager.com/infsof/default.aspx)；[Editorial Manager main page](https://www.editorialmanager.com/infsof/mainpage.html) |
| Open access options | [Open access options](https://www.sciencedirect.com/journal/information-and-software-technology/publish/open-access-options)（CLI WAF/403；未获公开可审计正文） |
| Special issues / topical collections | [ScienceDirect special issues](https://www.sciencedirect.com/journal/information-and-software-technology/special-issues)；[Calls for papers](https://www.sciencedirect.com/journal/information-and-software-technology/about/call-for-papers)（CLI WAF/403；candidate CFP 不写成已核验事实） |
| Volume / issue archive | [ScienceDirect all issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（CLI WAF/403；DBLP baseline 仅作 fallback） |
| Articles in press / online first | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press)（CLI WAF/403；不得与卷期文章双算） |
| Editorial board | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/information-and-software-technology/about/editorial-board)（CLI WAF/403；当前 roster 未获公开可审计正文） |
| DBLP venue page | [DBLP IST](https://dblp.org/db/journals/infsof/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现可命令行核验的官方年度卷期或 dated CFP |

> 核验 caveat：ScienceDirect / Elsevier 页面在当前 CLI 环境返回 WAF/403；Editorial Manager `infsof` 页面可打开但投稿表单仍需登录 / 公开可审计复核。 因此本目录只把 ScienceDirect 链接作为官方入口；凡 CLI 无法读取正文的 scope、editorial roster、special issue deadline 和 guest editor 均标作“未获公开可审计正文”，不得写成已完成事实。

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。JCR / CAS 若使用 AbleSci / AIS 等公开镜像暂存分区，只能作为二级可审计证据，并必须在行内标注非 Clarivate/CAS 官方导出；`索引核验` 不得因此升级为 `🟢`。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF B 级；emoji 已按 GUIDE 的 A/B/C 口径编码，不再统一写成黄色 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS Collection | 🟢 | Clarivate MJL ISSN 精确检索命中，Web of Science Core Collection = SCIE | [MJL ISSN exact search](https://mjl.clarivate.com/search-results?issn=0950-5849)；Clarivate MJL 页面核验显示 Exact Match / SCIE；[Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 作集合口径说明 | `2026-06-09 16:20` |
| JCR Quartile | 1️⃣ | 2025 JCR best：Q1；Software Engineering Q1 21/128，Information Systems Q2 65/258 | [公开第三方 JCR 镜像（非 Clarivate 官方导出）](https://www.ablesci.com/journal/detail?id=p3goNp)；[JCR 官方入口](https://jcr.clarivate.com/jcr/home) 需账号/机构权限，本行以可点击第三方镜像 + MJL SCIE 精确命中作为二级可审计证据；不是 Clarivate/CAS 官方导出，索引核验不升级为 `🟢` | `2026-06-09 16:20` |
| CAS 分区 | 2️⃣ | 2025 中科院升级版：计算机科学大类 2区；信息系统 / 软件工程小类均 2区 | [公开第三方中科院分区镜像（非 CAS 官方导出）](https://www.ablesci.com/journal/detail?id=p3goNp)；[中科院文献情报中心 2026-03-27 停更公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 说明 2026 起官方不再更新发布，因此本行记录版本化历史分区而非实时官方分区 | `2026-06-09 16:20` |
| EI / Compendex | 🟢 | 官方 Compendex `SERIALS` 精确命中，按 source-level 期刊记录 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `SERIALS`，Source title `Information and Software Technology`，Source type `Journal`，ISSN `0950-5849`，EISSN `-`，Publisher `Elsevier B.V.` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | WoS / EI 已有官方行级证据；JCR / CAS 仅由可点击第三方镜像给出版本化分区结论，公开官方行级记录未获可复现访问，因此索引核验不升级为 `🟢` | 已同步到 [SUMMARY.md](../SUMMARY.md)；reviewer 应复核 MJL、Compendex source-list 与公开分区页三类链接是否支撑本行 | `2026-06-09 16:20` |

## 2. Scope 与栏目

- 可复用方向线索：软件管理、过程、架构、建模、需求、测试、V&V、质量与经验软件工程相关方向；具体 Aims & Scope 以 ScienceDirect 官方入口后续公开可审计正文为准。
- 常规投稿按 rolling submission 处理；只有公开可审计核验到明确 deadline 的 special issue / topical collection 才能进入 [../TIMELINE.md](../TIMELINE.md) dated event 与 Mermaid。
- Article type、字数、伦理与 artefact 要求以官方 Guide for Authors 后续公开可审计正文为准；当前 CLI 仅确认官方入口，不能替代正文核验。

## 3. 核心编辑人员情报

本节只记录当前能稳妥维护的官方 roster 入口。由于 ScienceDirect editorial board 在当前 CLI 环境返回 WAF/403，本 PR 不臆造 Editor-in-Chief / Associate Editor / Editorial Board 名单；待官方 roster 公开可审计后再补姓名、角色、研究方向与近年论文入口。

| 姓名 | 期刊角色 | 单位 | 角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| 未获公开可审计正文 | Editor-in-Chief / Editorial Board leadership | 未获公开可审计正文 | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/information-and-software-technology/about/editorial-board) | 待官方 roster 核验后补 | 待官方 roster 核验后补 | 待官方 roster 核验后补 | P1/P2/P3/P4 相关，人员画像待补 | ⏳ ScienceDirect 官方当前 roster 未获公开可审计正文；CLI WAF/403 | `2026-06-05 18:24` |

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 强相关 | 强相关：需求、规约、MBSE、AI-driven architecture 与工具链案例可支撑从需求到模型的经验 / 工具论文。 |
| P2 场景与性质生成 | 强相关 | 强相关：requirements、testing、V&V 与 quality assurance 适合验证场景、oracle、性质生成线索。 |
| P3 验证剖面与模型检查 | 中相关 | 中相关：更偏经验 / 工具链评估，可承载验证剖面方法的工业案例与可靠性证据。 |
| P4 模型修复 | 强相关 | 强相关：software evolution、quality / defect 与 testing feedback 适合修复与缺陷分类。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [ScienceDirect journal page](https://www.sciencedirect.com/journal/information-and-software-technology) | CLI WAF/403；保留官方链接，未获公开可审计正文 | `2026-06-05 18:24` |
| Aims and scope | [ScienceDirect aims and scope](https://www.sciencedirect.com/journal/information-and-software-technology/about/aims-and-scope) | CLI WAF/403；不以第三方 scope 替代 | `2026-06-05 18:24` |
| Author guidelines | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors)；[ScienceDirect journal path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | CLI WAF/403；官方入口已定位 | `2026-06-05 18:24` |
| Submission system | [Editorial Manager default](https://www.editorialmanager.com/infsof/default.aspx)；[Editorial Manager main page](https://www.editorialmanager.com/infsof/mainpage.html) | 入口可能需登录；只记录官方投稿入口 | `2026-06-05 18:24` |
| Special issues / topical collections | [ScienceDirect special issues](https://www.sciencedirect.com/journal/information-and-software-technology/special-issues)；[Calls for papers](https://www.sciencedirect.com/journal/information-and-software-technology/about/call-for-papers) | CLI WAF/403；未完成公开可审计复核前不生成 dated event | `2026-06-05 18:24` |
| Volume / issue archive | [ScienceDirect all issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues) | publisher archive 优先；CLI WAF/403 时用 DBLP baseline 作 fallback | `2026-06-05 18:24` |
| Articles in press / online first | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | 会迁移到卷期；年度计数不得双算 | `2026-06-05 18:24` |
| Editorial board | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/information-and-software-technology/about/editorial-board) | CLI WAF/403；未获公开可审计正文当前 roster | `2026-06-05 18:24` |
| DBLP venue | [DBLP IST](https://dblp.org/db/journals/infsof/index.html) | 仅作 bibliographic / count fallback | `2026-06-05 18:24` |

## 6. 年度信息汇总

年度汇总表必须把期刊主页、author guidelines、submission system、special issue、volume / issue、online first、DBLP 等核心 URL 直接挂进表格。论文数量当前只采用 DBLP `entry article` baseline 或 `未公布`，不等同于 publisher article-type 闭合数。

| 年份 | 年度状态 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Articles / Online first | DBLP 年度页 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| [`2028`](./2028/README.md) | 🟡 rolling 入口开放；ScienceDirect WAF/403，dated CFP 未获公开可审计正文 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/infsof/default.aspx) / [main page](https://www.editorialmanager.com/infsof/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（未发现官方年度卷期 / DBLP 年度 volume） | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | [DBLP index](https://dblp.org/db/journals/infsof/index.html) | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | 🟡 rolling 入口开放；ScienceDirect WAF/403，dated CFP 未获公开可审计正文 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/infsof/default.aspx) / [main page](https://www.editorialmanager.com/infsof/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（未发现官方年度卷期 / DBLP 年度 volume） | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | [DBLP index](https://dblp.org/db/journals/infsof/index.html) | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟡 rolling 入口开放；ScienceDirect WAF/403，dated CFP 未获公开可审计正文 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/infsof/default.aspx) / [main page](https://www.editorialmanager.com/infsof/mainpage.html) | [Software Architecture for AI-Driven Systems](https://www.sciencedirect.com/special-issue/325890/software-architecture-for-ai-driven-systems-challenges-and-emerging-solutions)；[Human Factor in Generative AI](https://www.sciencedirect.com/special-issue/329824/human-factor-in-generative-ai-trust-usability-and-responsible-adoption)；[Green Software Evolution](https://www.sciencedirect.com/special-issue/330286/green-software-evolution)（候选线索 / 未核验；deadline / guest editors 未获公开可审计正文，当前不进 TIMELINE dated event，不可视为已确认可投窗口） | 滚动投稿；候选 special issue deadline 未获公开可审计正文 | [All issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（Vols. 189-197（DBLP baseline；年度进行中）） | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | [DBLP index](https://dblp.org/db/journals/infsof/index.html) | DBLP `entry article` baseline: 221 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 年度已归档 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/infsof/default.aspx) / [main page](https://www.editorialmanager.com/infsof/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（Vols. 177-188） | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | [DBLP index](https://dblp.org/db/journals/infsof/index.html) | DBLP `entry article` baseline: 243 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 年度已归档 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/infsof/default.aspx) / [main page](https://www.editorialmanager.com/infsof/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（Vols. 165-176） | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | [DBLP index](https://dblp.org/db/journals/infsof/index.html) | DBLP `entry article` baseline: 145 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 年度已归档 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/infsof/default.aspx) / [main page](https://www.editorialmanager.com/infsof/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（Vols. 153-164） | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | [DBLP index](https://dblp.org/db/journals/infsof/index.html) | DBLP `entry article` baseline: 184 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 年度已归档 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) | [Guide for Authors](https://www.sciencedirect.com/science/journal/09505849/publish/guide-for-authors) / [legacy path](https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/infsof/default.aspx) / [main page](https://www.editorialmanager.com/infsof/mainpage.html) | 无可命令行核验 active dated CFP | 滚动投稿 | [All issues](https://www.sciencedirect.com/journal/information-and-software-technology/issues)（Vols. 141-152） | [Articles in Press](https://www.sciencedirect.com/journal/information-and-software-technology/articles-in-press) | [DBLP index](https://dblp.org/db/journals/infsof/index.html) | DBLP `entry article` baseline: 166 | 🟡 部分核验 |

## 7. 维护备注

- 常规投稿按 rolling submission 处理，不进入 dated Mermaid。
- 2027/2028/2029+ 未发现可命令行核验的官方年度卷期或 dated CFP；不预设未来卷号。
- ScienceDirect 与 DBLP 对年度 volume / article 归属可能存在差异；publisher all issues / special issue 页面优先，DBLP 只作 bibliographic fallback。
- Articles in Press 是 online-first 状态，会迁移到正式卷期；年度计数不得与卷期文章双算。
- Candidate special issue URL 只能作为后续公开可审计复核入口；deadline、guest editor、状态未核验前不得同步到 [../TIMELINE.md](../TIMELINE.md) dated event，也不得在近期投稿安排中视为已确认可投窗口。

## 8. TIMELINE.md 同步提示

- 常规 rolling submission 已按“期刊滚动投稿 / 未定日期”规则同步到 [../TIMELINE.md](../TIMELINE.md)。
- 本 PR 未将 ScienceDirect candidate special issue 线索写入 dated timeline；后续只有在公开可审计核验到明确 deadline 后，才同步 [../TIMELINE.md](../TIMELINE.md) 的年度表格和 Mermaid。
- 后续若发现新的 dated CFP、special issue deadline 或年度卷期闭合信息，应同步维护本目录、[../TIMELINE.md](../TIMELINE.md) 与 [../SUMMARY.md](../SUMMARY.md)。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 11:46` | PR #35 近期窗口复审修复：在年度状态和 candidate special issue 表中显式写入“候选 / 未核验 / 不可视为当前可投窗口”，降低 ScienceDirect WAF/403 下的快读误判风险。 |
| `2026-06-05 18:24` | PR-8 review 前自查修复：因 ScienceDirect / Elsevier CLI WAF/403，将 editorial roster、scope 正文与 candidate special issue deadline 降级为未获公开可审计正文，避免把未核验事实写入 TIMELINE。 |
| `2026-06-05 18:05` | PR-8 初始化 IST 期刊 README，记录 ScienceDirect 官方入口、2022-2028 年度汇总和 ScienceDirect / DBLP 计数口径风险。 |
