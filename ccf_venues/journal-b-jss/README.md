# JSS README

> 信息更新时间：`2026-06-09 18:18:06`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | JSS |
| 全称 | Journal of Systems and Software |
| 类型 | 期刊 |
| CCF 大类 | [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) |
| CCF 等级 | 🥈 |
| 出版商 | Elsevier / ScienceDirect |
| ISSN | 0164-1212（print）；1873-1228（online） |
| 期刊主页 | [ScienceDirect JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) |
| Author guidelines | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) |
| Submission system | [Editorial Manager JSS](https://www.editorialmanager.com/jssoftware/default.aspx)（CLI/landing 可能提示 `site under development`，CLI/动态页/登录流程受限，未获公开可审计正文） |
| Special issues / article collections | [ScienceDirect special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues) |
| Volume / issue archive | [ScienceDirect all issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/issues) |
| Articles in press / online first | [ScienceDirect articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) |
| DBLP venue page | [DBLP JSS](https://dblp.org/db/journals/jss/) |
| 当前默认调查范围 | `2022` 至 `2028`；2027/2028 已检索但年度卷期、DBLP 年度页和 dated CFP 未公布 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。JCR / CAS 若使用 AbleSci / AIS 等公开镜像暂存分区，只能作为二级可审计证据，并必须在行内标注非 Clarivate/CAS 官方导出；`索引核验` 不得因此升级为 `🟢`。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS Collection | 🟢 | Clarivate MJL ISSN 精确检索命中，Web of Science Core Collection = SCIE | [MJL ISSN exact search](https://mjl.clarivate.com/search-results?issn=0164-1212)；Clarivate MJL 页面核验显示 Exact Match / SCIE；[Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 作集合口径说明 | `2026-06-09 16:20` |
| JCR Quartile | 1️⃣ | 2025 JCR best：Q1；Software Engineering Q1 23/128，Theory & Methods Q1 30/147 | [公开第三方 JCR 镜像（非 Clarivate 官方导出）](https://www.ablesci.com/journal/detail?id=pPEbn5)；[JCR 官方入口](https://jcr.clarivate.com/jcr/home) 需账号/机构权限，本行以可点击第三方镜像 + MJL SCIE 精确命中作为二级可审计证据；不是 Clarivate/CAS 官方导出，索引核验不升级为 `🟢` | `2026-06-09 16:20` |
| CAS 分区 | 2️⃣ | 2025 中科院升级版：计算机科学大类 2区；软件工程 / 理论方法小类均 2区 | [公开第三方中科院分区镜像（非 CAS 官方导出）](https://www.ablesci.com/journal/detail?id=pPEbn5)；[中科院文献情报中心 2026-03-27 停更公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 说明 2026 起官方不再更新发布，因此本行记录版本化历史分区而非实时官方分区 | `2026-06-09 16:20` |
| EI / Compendex | 🟢 | 官方 Compendex `SERIALS` 精确命中，按 source-level 期刊记录 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `SERIALS`，Source title `Journal of Systems and Software`，Source type `Journal`，ISSN `0164-1212`，EISSN `-`，Publisher `Elsevier Inc.` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | WoS / EI 已有官方行级证据；JCR / CAS 仅由可点击第三方镜像给出版本化分区结论，公开官方行级记录未获可复现访问，因此索引核验不升级为 `🟢` | 已同步到 [SUMMARY.md](../SUMMARY.md)；reviewer 应复核 MJL、Compendex source-list 与公开分区页三类链接是否支撑本行 | `2026-06-09 16:20` |

## 2. Scope 与栏目

- 官方 scope 摘要：JSS 面向软件工程各方面，覆盖 requirements、design、architecture、verification and validation、testing、maintenance and evolution 等方向，适合作为 P1-P4 的综合软件工程期刊入口。
- 证据要求：JSS 要求论文用 empirical studies、simulation、formal proofs 或其他 validation 支撑 claims；这与本仓库强调“生成-验证-修复”证据链相容。
- 栏目模式：除 regular papers 外，JSS 明确维护 In Practice、New Ideas and Trends Papers、special issues 与 Journal First Initiative。
- 投稿模式：常规投稿按 rolling submission 处理；special issue 需在投稿系统中选择对应 article type。
- 本库当前只展开 deadline-bearing / project-relevant 的 ScienceDirect special issue；`Open Science articles`、practice perspective 等不带明确 deadline 或与本库主线较弱的 collection 只保留在 ScienceDirect special issues 总入口中，后续可按专题补全。

## 3. 核心编辑人员情报

本节分离维护 ScienceDirect 当前长期 editorial roster 与 special issue / article collection guest editors：§3.1 只记录 [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) 可支撑的当前长期角色；§3.2 只记录具体 special issue / article collection 的 guest editor 线索，当前性限于对应 CFP，不等同于期刊长期 editorial leadership。研究方向与 project 关系为基于公开学术入口的归纳，需后续公开可审计复核。

### 3.1 当前 editorial leadership / board roles

| 姓名 | 期刊长期角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| P. Avgeriou | Editor-in-Chief | University of Groningen | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) | [DBLP](https://dblp.org/search?q=P.%20Avgeriou) | software architecture、technical debt、software evolution | [DBLP 近年论文入口](https://dblp.org/search?q=P.%20Avgeriou) | P1/P2/P4 强；P3 中 | 官方当前 roster 核验；方向基于 DBLP 归纳 | `2026-06-05 17:21` |
| D. Shepherd | Editor-in-Chief | Louisiana State University | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) | [DBLP](https://dblp.org/search?q=D.%20Shepherd) | empirical software engineering、developer tools、program comprehension | [DBLP 近年论文入口](https://dblp.org/search?q=D.%20Shepherd) | P1/P2 中到强；P4 中 | 官方当前 roster 核验；方向基于 DBLP 归纳 | `2026-06-05 17:21` |
| L. Duchien | Speciality Editor | University of Lille | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) | [DBLP](https://dblp.org/search?q=L.%20Duchien) | software architecture、adaptive / service systems、component-based software | [DBLP 近年论文入口](https://dblp.org/search?q=L.%20Duchien) | P1/P2 强；P3/P4 中 | 官方当前 roster 核验；方向基于 DBLP 归纳 | `2026-06-05 17:21` |
| R. Mirandola | Speciality Editor | Polytechnic University of Milan | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) | [DBLP](https://dblp.org/search?q=R.%20Mirandola) | performance / reliability engineering、software architecture、model-based analysis | [DBLP 近年论文入口](https://dblp.org/search?q=R.%20Mirandola) | P2/P3 强；P4 中 | 官方当前 roster 核验；方向基于 DBLP 归纳 | `2026-06-05 17:21` |
| C. Treude | Open Science Editor | Singapore Management University | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) | [DBLP](https://dblp.org/search?q=C.%20Treude) | empirical SE、NLP/LLM for SE、developer knowledge、open science | [DBLP 近年论文入口](https://dblp.org/search?q=C.%20Treude) | P1/P2 强；P3/P4 中 | 官方当前 roster 核验；方向基于 DBLP 归纳 | `2026-06-05 17:21` |
| W. Eric Wong | Senior Associate Editor | The University of Texas at Dallas | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) | [DBLP](https://dblp.org/search?q=W.%20Eric%20Wong) | software testing、reliability、dependability、fault localization | [DBLP 近年论文入口](https://dblp.org/search?q=W.%20Eric%20Wong) | P2/P3/P4 强；P1 中 | 官方当前 roster 核验；Software Dependability guest editor 另见 §3.2，不并入长期角色列 | `2026-06-05 17:21` |

### 3.2 Special issue / article collection guest editors

本节只记录带具体 CFP / article collection 证据的专题 guest editor；这些角色服务于对应 special issue，不等同于 JSS 当前长期 editorial board / editorial leadership。若某人同时具备长期 roster 角色（如 W. Eric Wong），长期角色仍以 §3.1 为准，本表仅补专题上下文。

| 姓名 | Special issue / 专题角色 | 官方来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|
| W. Eric Wong | Software Dependability: A Path Forward guest editor | [Software Dependability CFP](https://www.sciencedirect.com/special-issue/326119/special-issue-on-software-dependability-a-path-forward) | [DBLP](https://dblp.org/search?q=W.%20Eric%20Wong) | software testing、reliability、dependability、fault localization | [DBLP 近年论文入口](https://dblp.org/search?q=W.%20Eric%20Wong) | P2/P3/P4 强；P1 中 | special issue CFP 核验；当前性限于该 2025 deadline-bearing special issue；长期 Senior Associate Editor 见 §3.1 | `2026-06-05 17:21` |

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 强相关 | JSS scope 覆盖 requirements、design、architecture、model-driven / AI-assisted software engineering，可承接需求到状态机建模和 LLM for SE 经验研究。 |
| P2 场景与性质生成 | 强相关 | verification and validation、testing、quality evidence 与场景 / 性质生成高度相关。 |
| P3 验证剖面与模型检查 | 中到强 | 若工作包含 formal proof、simulation、model-based validation 或可靠性证据，可对齐 JSS 的验证与软件质量栏目。 |
| P4 模型修复 | 强相关 | maintenance、evolution、technical debt、dependability 和 reliability special issue 可支撑模型修复与缺陷闭环研究。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [ScienceDirect JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [DBLP JSS](https://dblp.org/db/journals/jss/) 作 bibliographic fallback | `2026-06-05 17:21` |
| Aims and scope | [ScienceDirect JSS homepage](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | scope 在 About the journal 中展开 | `2026-06-05 17:21` |
| Author guidelines | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | Elsevier / ScienceDirect 官方作者指南 | `2026-06-05 17:21` |
| Submission system | [Editorial Manager JSS](https://www.editorialmanager.com/jssoftware/default.aspx) | CLI/landing 可能提示 `site under development`，CLI/动态页/登录流程受限，未获公开可审计正文 | `2026-06-05 17:21` |
| Editorial board | [ScienceDirect editorial board](https://www.sciencedirect.com/journal/journal-of-systems-and-software/about/editorial-board) | 当前人员角色来源 | `2026-06-05 17:21` |
| Special issues / article collections | [ScienceDirect special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues) | 年度页展开 dated CFP | `2026-06-05 17:21` |
| Volume / issue archive | [ScienceDirect all issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/issues) | DBLP volume set 与 publisher issue archive 需后续交叉核验 | `2026-06-05 17:21` |
| Articles in press | [ScienceDirect articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | online-first 与正式 volume 可能跨年 | `2026-06-05 17:21` |
| DBLP venue | [DBLP JSS](https://dblp.org/db/journals/jss/) | 本目录按已记录的 DBLP volume ranges 记录 baseline | `2026-06-05 17:21` |

## 6. 年度信息汇总

状态口径：`🟢`=滚动开放/年度进行中；`✅`=年度已归档；核验口径：`🟡`=基础官方链接与 DBLP volume baseline 已记录，但论文数量和 publisher issue TOC 仍待逐卷核验。

| 年份 | 状态 | 状态说明 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Articles in press | DBLP volume set | 论文数量 | 核验 |
|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [`2028`](./2028/README.md) | 🟢 | 滚动开放；年度卷期 / DBLP 年度归档待公布 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/jssoftware/default.aspx) | ⏳ 已检索未公布（[special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues)） | ⏳ 已检索未公布 | ⏳ 已检索未公布（[All issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/issues)） | [Articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | ⏳ 已检索未公布（[DBLP JSS](https://dblp.org/db/journals/jss/)） | ⏳ 已检索未公布 | 🟡 |
| [`2027`](./2027/README.md) | 🟢 | 滚动开放；年度卷期 / DBLP 年度归档待公布 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/jssoftware/default.aspx) | ⏳ 已检索未公布（[special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues)） | ⏳ 已检索未公布 | ⏳ 已检索未公布（[All issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/issues)） | [Articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | ⏳ 已检索未公布（[DBLP JSS](https://dblp.org/db/journals/jss/)） | ⏳ 已检索未公布 | 🟡 |
| [`2026`](./2026/README.md) | 🟢 | 年度进行中；按 DBLP volume set 维护 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/jssoftware/default.aspx) | [AI for Software Architecting](https://www.sciencedirect.com/special-issue/329237/artificial-intelligence-for-software-architecting-ai-for-sa)；[AI Techniques for Performance / Reliability / Sustainability](https://www.sciencedirect.com/special-issue/329342/special-issue-on-ai-techniques-for-performance-reliability-and-sustainability-of-modern-software-systems) | 2026-03-15 待补时刻；2026-09-30 待补时刻 | Vol. 232-240 | [Articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | DBLP Vol. 232-240（[232](https://dblp.org/db/journals/jss/jss232.html)–[240](https://dblp.org/db/journals/jss/jss240.html)；[index](https://dblp.org/db/journals/jss/)） | 待逐卷计数 | 🟡 |
| [`2025`](./2025/README.md) | ✅ | 年度已归档；按 DBLP volume set 维护 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/jssoftware/default.aspx) | [Software Dependability: A Path Forward](https://www.sciencedirect.com/special-issue/326119/special-issue-on-software-dependability-a-path-forward) | 2025-11-15 待补时刻 | Vol. 219-231 | [Articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | DBLP Vol. 219-231（[219](https://dblp.org/db/journals/jss/jss219.html)–[231](https://dblp.org/db/journals/jss/jss231.html)；[index](https://dblp.org/db/journals/jss/)） | 待逐卷计数 | 🟡 |
| [`2024`](./2024/README.md) | ✅ | 年度已归档；按 DBLP volume set 维护 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/jssoftware/default.aspx) | 无已知 dated CFP（[special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues)） | 滚动投稿 | Vol. 207-218 | [Articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | DBLP Vol. 207-218（[207](https://dblp.org/db/journals/jss/jss207.html)–[218](https://dblp.org/db/journals/jss/jss218.html)；[index](https://dblp.org/db/journals/jss/)） | 待逐卷计数 | 🟡 |
| [`2023`](./2023/README.md) | ✅ | 年度已归档；按 DBLP volume set 维护 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/jssoftware/default.aspx) | 无已知 dated CFP（[special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues)） | 滚动投稿 | Vol. 195-206 | [Articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | DBLP Vol. 195-206（[195](https://dblp.org/db/journals/jss/jss195.html)–[206](https://dblp.org/db/journals/jss/jss206.html)；[index](https://dblp.org/db/journals/jss/)） | 待逐卷计数 | 🟡 |
| [`2022`](./2022/README.md) | ✅ | 年度已归档；按 DBLP volume set 维护 | [JSS](https://www.sciencedirect.com/journal/journal-of-systems-and-software) | [Guide for authors](https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors) | [Editorial Manager](https://www.editorialmanager.com/jssoftware/default.aspx) | 无已知 dated CFP（[special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues)） | 滚动投稿 | Vol. 183-194 | [Articles in press](https://www.sciencedirect.com/journal/journal-of-systems-and-software/articles-in-press) | DBLP Vol. 183-194（[183](https://dblp.org/db/journals/jss/jss183.html)–[194](https://dblp.org/db/journals/jss/jss194.html)；[index](https://dblp.org/db/journals/jss/)） | 待逐卷计数 | 🟡 |

## 7. 维护备注

- JSS 常规投稿按 rolling submission 处理，不进入 dated Mermaid；带明确 deadline 的 special issue 已同步至 [../TIMELINE.md](../TIMELINE.md)；后续若 ScienceDirect 更新状态或具体时刻再增量维护。
- 2022-2026 年度 volume 使用已记录的 DBLP baseline：2022=Vol. 183-194，2023=Vol. 195-206，2024=Vol. 207-218，2025=Vol. 219-231，2026=Vol. 232-240；ScienceDirect all-issues 与 DBLP volume set 可能存在归档口径差异，后续需逐卷核验。
- 2027/2028：已检索 [ScienceDirect all issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/issues)、[special issues](https://www.sciencedirect.com/journal/journal-of-systems-and-software/special-issues) 与 [DBLP JSS](https://dblp.org/db/journals/jss/)，年度卷期 / DBLP volume set / dated CFP 均按 `⏳ 已检索未公布` 记录。

## 8. TIMELINE.md 同步提示

- 2025-11-15 `[JSS] Software Dependability: A Path Forward`、2026-03-15 `[JSS] AI for Software Architecting`、2026-09-30 `[JSS] AI Techniques for Performance / Reliability / Sustainability` 已作为 dated events 同步至 [../TIMELINE.md](../TIMELINE.md)。
- `Editorial Manager` rolling submission 入口可作为期刊滚动投稿 / 未定日期入口候选，但提交系统 landing 仍需公开可审计证据补齐。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 19:01` | 最终复审修复：将长期 editorial roster 与 Software Dependability special issue guest editor 拆成 §3.1 / §3.2，避免专题角色被误读为长期 roster。 |
| `2026-06-05 18:13` | PR-7 全局同步收口：确认 JSS special issue dated events 已同步至 TIMELINE / SUMMARY，并保留 ScienceDirect CLI/WAF 未获公开可审计正文口径。 |
| `2026-06-05 17:21` | 初始化 JSS 期刊 README，记录 ScienceDirect / Editorial Manager / DBLP 核心入口、2022-2028 年度汇总、special issue deadline、核心编辑人员情报与待同步风险。 |
