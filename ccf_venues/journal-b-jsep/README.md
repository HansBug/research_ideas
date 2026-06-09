# JSEP README

> 信息更新时间：`2026-06-09 11:13`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | JSEP |
| 全称 | Journal of Software: Evolution and Process |
| 类型 | 期刊 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| CCF 等级 | B（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版商 | Wiley / Wiley Online Library |
| ISSN | 2047-7473（print）/ 2047-7481（online）；Wiley / DBLP 多源交叉核验，editorial roster 仍待人工浏览器核验 |
| 期刊主页 | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481)（CLI WAF/403，需人工浏览器核验正文） |
| Author guidelines | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html)（CLI WAF/403，需人工浏览器核验正文） |
| Submission system | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme)（候选入口；是否仍为当前总入口待 Wiley 浏览器核验） |
| Special issues / topical collections | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481)；DBLP 年度页显示多期 special issue 线索 |
| Volume / issue archive | [Wiley issues](https://onlinelibrary.wiley.com/journal/20477481/issues)（CLI WAF/403）；DBLP 年度页作 fallback |
| Current issue candidate / Early View 待定位 | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue)（CLI WAF/403，待核验） |
| DBLP venue page | [DBLP JSEP](https://dblp.org/db/journals/smr/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现可命令行核验的官方年度卷期或 dated CFP |

> Wiley 官方页面在当前 CLI 环境中返回 Cloudflare / Wiley WAF `403 Just a moment...`。本目录保留 Wiley 官方链接作为事实核验入口；凡无法在 CLI 中读取正文的字段均显式标注“待人工浏览器核验”，不以第三方页面替代 Wiley 官方事实。

### 1.1 索引与分区信息

> 本节由 PR #90 建立为外部索引占位入口；当前仅完成规则制度化与待核验占位，真实 WoS / JCR / CAS / EI 结论需按 [GUIDE.md](../GUIDE.md) 的外部索引规则逐项补证。JCR 与 CAS 的 emoji 列只允许写真实 emoji，例如 `1️⃣` / `2️⃣` / `3️⃣` / `4️⃣` / `⚪` / `❓`，文字解释放在口径说明或相邻列。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | ❓ | 待复核 CCF 官方目录证据 | 沿用 §1 CCF 等级；后续需补 CCF 官方目录链接与核验时间 | `待补` |
| WoS Collection | ❓ | 待核验 | 需按 ISSN / eISSN 在 Clarivate MJL / WoS 中核验 SCIE / SSCI / AHCI / ESCI 归属 | `待补` |
| JCR Quartile | ❓ | 待核验 | 需记录 JCR release year、metric/data year、category、rank、quartile、percentile 与证据 URL | `待补` |
| CAS 分区 | ❓ | 待核验 | 仅可记录中国科学院文献情报中心官方 / 历史版可追溯分区；需写版本年份与来源 | `待补` |
| EI / Compendex | ❓ | 待核验 | 需按官方 Compendex Source List snapshot 核验 source title、source type、sheet、coverage | `待补` |
| 索引核验 | ❓ | 待启动 | 缺证条目须同步登记到 [SUMMARY.md](../SUMMARY.md) 风险 / 待核验表 | `待补` |

## 2. Scope 与栏目

JSEP 面向软件演化、维护、过程改进、项目 / 过程管理、软件质量、重构、测试与维护实践，是 P4 模型修复、修复过程管理、演化证据链和修复效果评估的 CCF B 期刊入口。

## 3. 核心编辑人员情报

本节只记录当前可见的核心编辑人员线索。由于 Wiley editorial board 在当前 CLI 环境返回 WAF/403，下表使用个人 / 机构页面作为 B 级临时证据，必须待人工浏览器打开 Wiley editorial board 后升级或修正；不得把 B 级线索写成 Wiley 当前 roster 已完全核验。

| 姓名 | 期刊角色 | 单位 | 角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Massimiliano Di Penta | Editor-in-Chief（个人服务页，2019-；Wiley roster 待核） | University of Sannio | [个人 service page](https://mdipenta.github.io/service/)（非 Wiley；待人工核验） | [个人主页](https://mdipenta.github.io/) | software maintenance & evolution、MSR、empirical SE、DevOps、testing | DBLP / personal page recent papers | P4 强：维护、演化、技术债、测试与修复评估 | B：个人主页角色自述；Wiley editorial board CLI WAF/403 | `2026-06-05 17:35` |
| Darren Dalcher | Editor-in-Chief（机构页；Wiley roster 待核） | Lancaster University | [Lancaster profile](https://research.lancaster-university.uk/en/persons/darren-dalcher/)（非 Wiley；待人工核验） | [Lancaster profile](https://research.lancaster-university.uk/en/persons/darren-dalcher/) | process improvement、systems engineering、decision making、change management | institutional profile / DBLP search | P4 中强：修复流程治理、过程改进和项目管理 | B：机构页角色线索；Wiley editorial board CLI WAF/403 | `2026-06-05 17:35` |
| Xin Peng | Co-Editor-in-Chief（个人主页，2020-；Wiley roster 待核） | Fudan University | [个人主页](https://cspengxin.github.io/)（非 Wiley；待人工核验） | [个人主页](https://cspengxin.github.io/) / [DBLP search](https://dblp.org/search?q=Xin%20Peng) | software analytics、AI for software development、AIOps、microservices | personal page / DBLP recent papers | P1/P4 强：AI4SE、日志/演化分析、修复闭环 | B：个人主页角色自述；Wiley editorial board CLI WAF/403 | `2026-06-05 17:35` |
| David Raffo | Co-Editor-in-Chief（机构页；Wiley roster 待核） | Portland State University | [PSU profile](https://www.pdx.edu/profile/david-raffo)（非 Wiley；待人工核验） | [PSU profile](https://www.pdx.edu/profile/david-raffo) | strategic software engineering、process simulation/modeling、process improvement、QA planning | institutional profile / DBLP search | P4 强：过程建模、修复评估、质量保障 | B：机构页角色线索；Wiley editorial board CLI WAF/403 | `2026-06-05 17:35` |

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中 | 中：从程序理解、维护历史、工件分析中抽取结构化上下文，可辅助需求 / 代码 / 模型到状态机的建模。 |
| P2 场景与性质生成 | 中 | 中：缺陷报告、回归测试、维护历史和负结果可作为场景与性质生成线索。 |
| P3 验证剖面与模型检查 | 中 | 中：工具、trace、profile、reproducibility 和质量证据可为验证剖面提供经验输入。 |
| P4 模型修复 | 高 | 高：维护、演化、重构、程序理解和过程改进与迭代式模型修复闭环直接相关。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | CLI WAF/403；保留官方链接，需浏览器核验正文 | `2026-06-05 17:35` |
| Aims and scope | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | Scope 事实待 Wiley 浏览器核验 | `2026-06-05 17:35` |
| Author guidelines | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | CLI WAF/403；不以第三方指南替代 | `2026-06-05 17:35` |
| Submission system | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | 候选 Manuscript Central 入口；当前性待 Wiley 核验 | `2026-06-05 17:35` |
| Editorial board | [Wiley editorial board candidate](https://onlinelibrary.wiley.com/page/journal/20477481/homepage/editorialboard.html) | CLI WAF/403；待人工浏览器核验当前 roster | `2026-06-05 17:35` |
| Special issues / topical collections | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | DBLP 年度页显示已出版 special issue 线索；active dated CFP 未发现 | `2026-06-05 17:35` |
| Volume / issue archive | [Wiley issues](https://onlinelibrary.wiley.com/journal/20477481/issues) | DBLP 年度页作 bibliographic / count fallback | `2026-06-05 17:35` |
| Current issue candidate / Early View 待定位 | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | CLI WAF/403；current issue 待浏览器确认；Early View / articles in press 入口待定位 | `2026-06-05 17:35` |
| DBLP venue | [DBLP JSEP](https://dblp.org/db/journals/smr/index.html) | 仅作论文名录 / 年度计数 fallback | `2026-06-05 17:35` |

## 6. 年度信息汇总

年度论文数量采用 DBLP `entry article` baseline 口径：`2025=120`、`2024=174`、`2023=82`、`2022=55`；2026+ DBLP 年度页未公布 / 待补，不写闭合数。

| 年份 | 年度状态 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Current issue / Early View | DBLP 年度页 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | 🟡 rolling 候选 / 待人工核验 | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | 无已知 active dated CFP | rolling 投稿候选（待 Wiley 浏览器核验） | ⏳ 已检索未公布 | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 🟡 部分核验；Wiley CLI WAF/403 |
| [2027](./2027/README.md) | 🟡 rolling 候选 / 待人工核验 | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | 无已知 active dated CFP | rolling 投稿候选（待 Wiley 浏览器核验） | ⏳ 已检索未公布 | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 🟡 部分核验；Wiley CLI WAF/403 |
| [2026](./2026/README.md) | 🟡 rolling 候选 / 待人工核验 | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | 无已知 active dated CFP | rolling 投稿候选（待 Wiley 浏览器核验） | ⏳ 已检索未公布 | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 🟡 部分核验；Wiley CLI WAF/403 |
| [2025](./2025/README.md) | ✅ 年度已归档 / DBLP baseline | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | Software refactoring special issue；SCAM 2022 special issue 线索 | 滚动投稿 | [DBLP Vol. 37](https://dblp.org/db/journals/smr/smr37.html) | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | [DBLP Vol. 37](https://dblp.org/db/journals/smr/smr37.html) | 120（DBLP entry article baseline） | 🟡 部分核验；Wiley CLI WAF/403 |
| [2024](./2024/README.md) | ✅ 年度已归档 / DBLP baseline | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | Software Quality for Modern Systems；emerging technologies and software/systems processes special issue 线索 | 滚动投稿 | [DBLP Vol. 36](https://dblp.org/db/journals/smr/smr36.html) | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | [DBLP Vol. 36](https://dblp.org/db/journals/smr/smr36.html) | 174（DBLP entry article baseline） | 🟡 部分核验；Wiley CLI WAF/403 |
| [2023](./2023/README.md) | ✅ 年度已归档 / DBLP baseline | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | Automation of software test and test code quality special issue 线索 | 滚动投稿 | [DBLP Vol. 35](https://dblp.org/db/journals/smr/smr35.html) | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | [DBLP Vol. 35](https://dblp.org/db/journals/smr/smr35.html) | 82（DBLP entry article baseline） | 🟡 部分核验；Wiley CLI WAF/403 |
| [2022](./2022/README.md) | ✅ 年度已归档 / DBLP baseline | [Wiley JSEP](https://onlinelibrary.wiley.com/journal/20477481) | [Wiley for authors](https://onlinelibrary.wiley.com/hub/journal/20477481/homepage/forauthors.html) | [ScholarOne / Manuscript Central candidate](https://mc.manuscriptcentral.com/jsme) | Distributed complex systems；Automatic Software Testing from the Trenches special issue 线索 | 滚动投稿 | [DBLP Vol. 34](https://dblp.org/db/journals/smr/smr34.html) | [Wiley current issue candidate（Early View 待定位）](https://onlinelibrary.wiley.com/journal/20477481/currentissue) | [DBLP Vol. 34](https://dblp.org/db/journals/smr/smr34.html) | 55（DBLP entry article baseline） | 🟡 部分核验；Wiley CLI WAF/403 |

## 7. 维护备注

- JSEP 常规投稿按 rolling submission 候选处理，但 `author guidelines / submission system / online first` 均需 Wiley 浏览器核验。
- 当前未发现 2022-2028 active dated special issue / topical collection CFP；已出版 special issue 线索只作为年度论文筛选线索，不生成 Mermaid milestone。
- `2029+` 检索结论：未发现可命令行核验的官方年度卷期、DBLP 年度页或 dated CFP；后续待 Wiley / DBLP 发布后补录。
- 2022-2025 年度论文数量为 DBLP `entry article` baseline，不等同于 Wiley publisher article-type 闭合数；后续需用 Wiley issue TOC 浏览器核验 editorial、erratum、front matter 等是否纳入。

## 8. TIMELINE.md 同步提示

- JSEP 常规 rolling submission 按“期刊滚动投稿 / 未定日期”规则维护；当前无 active dated CFP 需要写入 Mermaid。
- 后续若发现 Wiley 官方 dated CFP、special issue deadline 或年度卷期闭合信息，应同步维护本目录、[../TIMELINE.md](../TIMELINE.md) 与 [../SUMMARY.md](../SUMMARY.md)。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 18:38` | 吸收 final review M 级 polish：将 ISSN 字段从“待 Wiley 浏览器核验”改为 Wiley / DBLP 多源交叉核验，同时保留 editorial roster 待人工核验 caveat。 |
| `2026-06-05 18:13` | PR-6 收尾复核：降级 Wiley rolling 投稿为候选口径，并将 current issue 与 Early View / articles in press 入口明确分离。 |
| `2026-06-05 17:35` | PR-6 初始化 JSEP 期刊 README，记录 Wiley 官方入口、DBLP entry article baseline、WAF/403 caveat、2022-2028 年度汇总、2029+ 检索结论与核心编辑人员临时画像。 |
