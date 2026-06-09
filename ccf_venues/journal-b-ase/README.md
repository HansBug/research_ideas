# Automated Software Engineering Journal README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ASE Journal / Automated Software Engineering |
| 全称 | Automated Software Engineering |
| 类型 | 期刊 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录入口](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；CLI 可能触发 WAF，正文待人工浏览器复核） |
| CCF 等级 | B（官方入口已定位；`ccf.atom.im` 仅作非官方机器检索线索） |
| 出版商 | Springer / Springer Nature |
| ISSN | 0928-8910（print）；1573-7535（electronic） |
| 期刊主页 | [Springer Automated Software Engineering](https://link.springer.com/journal/10515) |
| Aims and scope | [Springer aims and scope](https://link.springer.com/journal/10515/aims-and-scope) |
| Author guidelines | [Springer submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) |
| Submission system | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3)（具体登录流程待人工浏览器核验） |
| Special issues / topical collections | [Springer collections](https://link.springer.com/journal/10515/collections) |
| Volume / issue archive | [Springer volumes and issues](https://link.springer.com/journal/10515/volumes-and-issues) |
| Articles / online first | [Springer articles](https://link.springer.com/journal/10515/articles) |
| Editorial board | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) |
| DBLP venue page | [DBLP Automated Software Engineering](https://dblp.org/db/journals/ase/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2027/2028` 卷期与 DBLP 年度页未公布时不预造 |

### 1.1 索引与分区信息

> 本节在 PR #91 中从 PR #90 占位推进为“证据链优先”的真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。JCR / CAS 若没有可追溯单刊证据，宁可写 `⏳`，不得用第三方站点补成分区事实。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🟡 | 沿用本库 CCF B 级；官方目录入口已定位，单条目仍需浏览器行级复核 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本 PR 不重新定义 CCF scope，只保留可点击官方基线入口 | `2026-06-09 13:52` |
| WoS Collection | ⏳ | 待人工核验 Web of Science Core Collection 收录集合 | [Clarivate Master Journal List](https://mjl.clarivate.com/search-results) 为官方检索入口；本轮命令行仅确认 SPA 入口可访问，未取得可审计单刊 `SCIE/SSCI/AHCI/ESCI` 行级结果；后续用 ISSN / eISSN 通过浏览器或机构入口复核 | `2026-06-09 13:52` |
| JCR Quartile | ⏳ | 待人工核验 2025 JCR 单刊 category / rank / quartile | [JCR 平台](https://jcr.clarivate.com/jcr/home)；[2025 JCR 发布说明](https://clarivate.com/news/clarivate-unveils-the-2025-journal-citation-reports/) 仅证明 release 存在，不证明本刊 quartile；需机构入口导出单刊 category、rank、quartile、percentile 后再改为 `1️⃣`--`4️⃣` | `2026-06-09 13:52` |
| CAS 分区 | ⏳ | 待人工核验中科院历史版分区 | [中国科学院文献情报中心停更公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 证明 2026 起不再更新发布；本轮未获得本刊历史版官方行级分区，后续只可用官方 / 机构历史版证据补写 | `2026-06-09 13:52` |
| EI / Compendex | 🟢 | 官方 Compendex `SERIALS` 精确命中，按 source-level 期刊记录 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本地 snapshot `compendex_source_list_2026-06-09.xlsx`，sheet `SERIALS`，Source title `Automated Software Engineering`，Source type `Journal`，ISSN `0928-8910`，EISSN `1573-7535`，Publisher `Springer` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | EI 已有官方 source-list 证据；WoS / JCR / CAS 仍待人工或机构入口核验 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；后续 reviewer 需复核本节链接与 source-list 字段 | `2026-06-09 13:52` |

## 2. Scope 与栏目

- Springer scope 将该刊定位为自动化复杂软件工程任务及其支撑工具的论坛，覆盖 automated reasoning、search-based software engineering、software analytics、testing、program repair、quality evaluation、AI for SE 等方向。
- 对本仓库而言，ASE Journal 与已有 [../conf-a-ase](../conf-a-ase/README.md) 同缩写但不同 venue：本目录只维护 Springer 期刊，不维护 ASE 会议。
- 常规稿件采用 rolling / continuous article publishing 期刊节奏；只有 Springer collection / topical collection 给出明确 deadline 时才进入 [../TIMELINE.md](../TIMELINE.md) dated event。
- Weakly related collections（如纯 quantum / green software 且与 project_1~4 暂无直接叙事）只作为观察线索，不进入近期投稿重点；若后续用户指定再单独补强。

## 3. 核心编辑人员情报

长期 roster 以 [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) 为主证据；collection guest editors 只在年度页 / collection 小节记录，不混入长期 editorial board。

| 姓名 | 期刊角色 | 单位 | 官方来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Tim Menzies | Editor-in-Chief | North Carolina State University | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | [DBLP](https://dblp.org/search?q=Tim%20Menzies) | software analytics、AI for SE、defect prediction、search-based SE | [DBLP 近年论文入口](https://dblp.org/search?q=Tim%20Menzies) | P1/P2/P4 强；P3 中 | Springer 当前 roster 核验；研究方向待个人主页细化 | `2026-06-07 12:47` |
| Hoa Dam | Deputy Editor-in-Chief | University of Wollongong | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | [DBLP](https://dblp.org/search?q=Hoa%20Dam) | AI for SE、requirements/software analytics、automation | [DBLP 近年论文入口](https://dblp.org/search?q=Hoa%20Dam) | P1/P2/P4 强 | Springer 当前 roster 核验；方向需后续补证 | `2026-06-07 12:47` |
| Gregory Gay | Deputy Editor-in-Chief | University of Gothenburg | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | [DBLP](https://dblp.org/search?q=Gregory%20Gay) | software testing、search-based testing、SE automation | [DBLP 近年论文入口](https://dblp.org/search?q=Gregory%20Gay) | P2/P3/P4 强 | Springer 当前 roster 核验；方向需后续补证 | `2026-06-07 12:47` |
| Sam Malek | Deputy Editor-in-Chief | University of California, Irvine | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | [DBLP](https://dblp.org/search?q=Sam%20Malek) | software architecture、self-adaptive systems、CPS / mobile systems | [DBLP 近年论文入口](https://dblp.org/search?q=Sam%20Malek) | P1/P3/P4 中到强 | Springer 当前 roster 核验；方向需后续补证 | `2026-06-07 12:47` |
| Matias Martinez | Deputy Editor-in-Chief | Universitat Politècnica de Catalunya - BarcelonaTech | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | [DBLP](https://dblp.org/search?q=Matias%20Martinez) | automated program repair、software maintenance、AI for SE | [DBLP 近年论文入口](https://dblp.org/search?q=Matias%20Martinez) | P4 强；P1/P2 中 | Springer 当前 roster 核验；方向需后续补证 | `2026-06-07 12:47` |
| Shiva Nejati | Deputy Editor-in-Chief | University of Ottawa | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | [DBLP](https://dblp.org/search?q=Shiva%20Nejati) | model-based testing、requirements / CPS、search-based testing | [DBLP 近年论文入口](https://dblp.org/search?q=Shiva%20Nejati) | P1/P2/P3 强 | Springer 当前 roster 核验；方向需后续补证 | `2026-06-07 12:47` |
| Justyna Petke | Deputy Editor-in-Chief | University College London | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | [DBLP](https://dblp.org/search?q=Justyna%20Petke) | genetic improvement、program repair、search-based SE | [DBLP 近年论文入口](https://dblp.org/search?q=Justyna%20Petke) | P4 强；P2 中 | Springer 当前 roster 核验；方向需后续补证 | `2026-06-07 12:47` |

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 强相关 | 自动化建模、低代码 / 建模 collection、LLM-assisted modeling 与需求到模型工具化对口。 |
| P2 场景与性质生成 | 强相关 | 自动测试、质量评价、review、explainability 与 requirements-to-test / properties 可承载场景与性质生成方法。 |
| P3 验证剖面与模型检查 | 中到强 | 若强调 model-based testing、verification workflow、CPS / architecture evidence，可对齐；纯形式化理论仍优先 STVR / SoSyM / TASE 等。 |
| P4 模型修复 | 强相关 | Automated program repair、SBSE、genetic improvement、quality feedback 与 repair loop 高度贴合。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [Springer ASE Journal](https://link.springer.com/journal/10515) | 与 [ASE Conference](../conf-a-ase/README.md) 明确消歧 | `2026-06-07 12:47` |
| Aims and scope | [Springer aims and scope](https://link.springer.com/journal/10515/aims-and-scope) | Springer 首页摘要作补充 | `2026-06-07 12:47` |
| Author guidelines | [Springer submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | rolling 常规投稿 | `2026-06-07 12:47` |
| Submission system | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | 具体登录 / article type 路由待人工浏览器核验 | `2026-06-07 12:47` |
| Collections | [Springer collections](https://link.springer.com/journal/10515/collections) | 只把 project-relevant dated collection 同步进 TIMELINE | `2026-06-07 12:47` |
| Volume / issue archive | [Springer volumes and issues](https://link.springer.com/journal/10515/volumes-and-issues) | 2022--2026 已有卷期；future 不预造 | `2026-06-07 12:47` |
| Articles / online first | [Springer articles](https://link.springer.com/journal/10515/articles) | continuous article publishing | `2026-06-07 12:47` |
| Editorial board | [Springer editorial board](https://link.springer.com/journal/10515/editorial-board) | 不展开全量 Associate Editors | `2026-06-07 12:47` |
| DBLP venue | [DBLP ASE Journal](https://dblp.org/db/journals/ase/index.html) | 仅作 bibliographic fallback / annual baseline | `2026-06-07 12:47` |

## 6. 年度信息汇总

| 年份 | 年度状态 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Articles / Online first | DBLP 年度页 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | 🟢 滚动开放 | [Springer ASE Journal](https://link.springer.com/journal/10515) | [Submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | 无已知 active dated CFP | 滚动投稿 | ⏳ 已检索未公布 | [Springer articles](https://link.springer.com/journal/10515/articles) | ⏳ 已检索未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟢 滚动开放 / collections 跨年 | [Springer ASE Journal](https://link.springer.com/journal/10515) | [Submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | SBSE in LLMs/Agents；APSEC collection | SBSE: 2027-01-30；APSEC: 2027-03-12 | ⏳ 已检索未公布 | [Springer articles](https://link.springer.com/journal/10515/articles) | ⏳ 已检索未公布 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🟡 滚动开放 / 多个 collection open | [Springer ASE Journal](https://link.springer.com/journal/10515) | [Submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | Ex-ASE；Low-Code Modeling；Reproducibility @ SANER；Interplay ASE/business；Code review quality；SBSE in LLMs/Agents | 2026-06-30 / 2026-08-15 / 2026-09-01 / 2026-09-30 / 2026-10-01 / 2027-01-30 | [Vol. 33 Issue 1](https://link.springer.com/journal/10515/volumes-and-issues/33-1) | [Springer articles](https://link.springer.com/journal/10515/articles) | [DBLP Vol. 33](https://dblp.org/db/journals/ase/ase33.html) | 待补（DBLP 仍变化） | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 年度已归档 | [Springer ASE Journal](https://link.springer.com/journal/10515) | [Submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | 历史 / closed collections 待补 | 滚动投稿 | [Vol. 32 Issue 1](https://link.springer.com/journal/10515/volumes-and-issues/32-1) | [Springer articles](https://link.springer.com/journal/10515/articles) | [DBLP Vol. 32](https://dblp.org/db/journals/ase/ase32.html) | 待补（DBLP API 曾限流） | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 年度已归档 | [Springer ASE Journal](https://link.springer.com/journal/10515) | [Submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | 无已知 active CFP | 滚动投稿 | [Vol. 31 Issue 1](https://link.springer.com/journal/10515/volumes-and-issues/31-1) | [Springer articles](https://link.springer.com/journal/10515/articles) | [DBLP Vol. 31](https://dblp.org/db/journals/ase/ase31.html) | DBLP fallback `entry article`≈71，待 publisher 复核 | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 年度已归档 | [Springer ASE Journal](https://link.springer.com/journal/10515) | [Submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | 无已知 active CFP | 滚动投稿 | [Vol. 30 Issue 1](https://link.springer.com/journal/10515/volumes-and-issues/30-1) | [Springer articles](https://link.springer.com/journal/10515/articles) | [DBLP Vol. 30](https://dblp.org/db/journals/ase/ase30.html) | DBLP fallback `entry article`≈32，待 publisher 复核 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 年度已归档 | [Springer ASE Journal](https://link.springer.com/journal/10515) | [Submission guidelines](https://link.springer.com/journal/10515/submission-guidelines) | [Springer Nature submission](https://submission.nature.com/new-submission/10515/3) | 无已知 active CFP | 滚动投稿 | [Vol. 29 Issue 1](https://link.springer.com/journal/10515/volumes-and-issues/29-1) | [Springer articles](https://link.springer.com/journal/10515/articles) | [DBLP Vol. 29](https://dblp.org/db/journals/ase/ase29.html) | DBLP fallback `entry article`≈62，待 publisher 复核 | 🟡 部分核验 |

## 7. 维护备注

- 常规投稿为 rolling / continuous publishing，不进入 dated Mermaid；[TIMELINE.md](../TIMELINE.md) 的“期刊滚动投稿 / 未定日期”表已记录本 venue。
- Springer collections 只维护与 LLM4Modeling / 自动化建模 / 模型质量 / 修复强相关的 subset；弱相关 open collections 不写入近期投稿窗口，以免误导投稿决策。
- DBLP `entry article` baseline 不等于 Springer 最终卷期闭合数；后续如做论文数量统计，必须按 publisher issue / article type 交叉核验。
- CCF 等级以 CCF 官方目录为准；`ccf.atom.im` 只作非官方检索线索，不作为官方证据。

## 8. 证据与核查记录

| 类型 | 链接 | 核查时间 | 结论 |
|---|---|---|---|
| CCF official entry | [CCF TCSE_SS_PDL](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) | `2026-06-07 12:47` | 官方入口已定位；CLI 可能触发 WAF / 动态页，正文与第七版状态待人工浏览器复核。 |
| 非官方 CCF 镜像线索 | [ccf.atom.im](https://ccf.atom.im/) | `2026-06-07 12:47` | 仅作机器检索 / 差集筛查线索，不作为 CCF 官方事实。 |
| Publisher homepage | [Springer Automated Software Engineering](https://link.springer.com/journal/10515) | `2026-06-07 12:47` | Springer 期刊入口、ISSN、submission、collections、volume / issue 与 editorial board 入口已定位。 |
| DBLP fallback | [DBLP ASE Journal](https://dblp.org/db/journals/ase/index.html) | `2026-06-07 12:47` | 仅作 bibliographic fallback / annual baseline；不得替代 publisher final count。 |

## 9. TIMELINE.md 同步提示

- ASE Journal rolling submission 已进入 [../TIMELINE.md](../TIMELINE.md) §14。
- Ex-ASE、Low-Code Modeling、Reproducibility @ SANER、Interplay ASE/business、Code Review Quality、SBSE in LLMs/Agents、APSEC collection 等 project-relevant dated collection events 已同步进对应年份表格与 Mermaid 分片。

## 10. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-07 12:47` | PR #63 初始化 Automated Software Engineering Journal 情报，补充 Springer / DBLP / CCF 证据、核心编辑人员、2022--2028 年度索引、rolling 与 collection TIMELINE 口径。 |
