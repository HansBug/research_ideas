# `ccf_venues/` GUIDE

> 信息更新时间：`2026-06-09 20:50:00`（Asia/Shanghai）

## 1. 目标与任务边界

`ccf_venues/` 维护的是 `CCF` 相关会议 / 期刊的 venue 情报，而不是单篇论文全文库。

本库应做：

1. 固定和本仓库 project 相关的 venue 范围。
2. 维护每个 venue 的稳定信息：官方主页、scope、出版方、CCF 等级、project 相关性。
3. 维护自 `2022` 年以来每个年度的官方主页、`CFP` / important dates、submission system、program / accepted papers、proceedings / volume issue、论文名录入口和论文数量，并把这些入口以 Markdown 超链接挂进表格。
4. 对尚未召开但已有官方信息的年度，记录当前状态和关键 ddl。
5. 维护 [TIMELINE.md](./TIMELINE.md)，按事件发生年份汇总跨 venue 投稿相关 important dates。
6. 维护会议 / 期刊核心人员情报，至少覆盖官方角色、主要研究方向、代表作或近 5 年论文入口、与本仓库 project 的关系和核验状态。
7. 给后续论文初筛、投稿计划、前沿追踪提供稳定入口。

本库不应做：

1. 不下载或保存论文 PDF。
2. 不展开单篇论文深读分析。
3. 不记录无法追溯来源的非官方时间点。
4. 不把第三方聚合站当作官方证据；第三方站最多作为发现线索。

## 2. 目录与命名规范

### 2.1 venue 目录命名

统一使用：

```text
<conf|journal>-<a|b|c>-<slug>/
```

规则：

1. `conf` 表示会议，`journal` 表示期刊。
2. `a/b/c` 表示 CCF 等级；若原始大类是理论、交叉或国内目录，在 README 元信息里另写 `CCF 大类`。
3. `slug` 使用稳定小写缩写；例如 `icse`、`models`、`sosym`、`tse`。
4. 同名冲突必须显式区分，例如：
   - `conf-a-ase`
   - `journal-b-ase`
   - `conf-b-re`
   - `journal-b-re`

### 2.2 年度目录命名

每个年度使用四位年份目录：

```text
ccf_venues/conf-a-icse/2026/README.md
ccf_venues/journal-b-sosym/2025/README.md
```

默认维护 `2022` 年至当前年份 + 2；以 `2026-06-04` 为例，初始化骨架至少覆盖到 `2028`。`当前年份 + 2` 是默认检索与占位下限，不是未来年度上限；若能找到更远未来年度的官方主页、`CFP` 或 important dates，必须继续新增对应年度目录。

### 2.5 SUMMARY.md 单表总账纪律

[SUMMARY.md](./SUMMARY.md) 是读者查阅入口，不是 PR 流程、执行合同、踩坑长表或分批完成记录的正文承载处。后续任何 PR 修改 SUMMARY 时必须遵守：

1. 正文结构只允许保留：`当前总览`、`外部索引与分区核验口径`、`Venue 总表`、`待补与核查记录`、`更新日志`。
2. `Venue 总表` 是唯一全量 venue 事实总表，至少包含：`目录名`、`类型`、`CCF`、`主要价值`、`主要对应 project`、`WoS`、`JCR`、`CAS`、`EI`、`索引核验`；可在同一表内继续补充年度入口、核心人员 / 计数口径、索引摘要等读者查阅字段。
3. `Venue 总表` 排序固定为：先按 CCF `🏆 -> 🥈 -> 🥉 -> ⚪ -> ❓`，同等级内按 `会议 -> 期刊`，再按目录名升序。不得按 PR 批次、编辑顺序或更新时间拆表。
4. `待补与核查记录` 只允许是一个全库合并表，用于记录未闭合事实、降级原因和升级条件；不得拆成 PR-2 / PR-3 / PR-6 等批次小节，也不得堆叠踩坑长表。
5. PR 分工、编辑流程、执行合同、分批结构、踩坑复盘、watchlist 生成过程和单轮刷新过程不得写入 SUMMARY 正文；这些信息应写入本 GUIDE、[01-venue-scope.md](./01-venue-scope.md)、独立规则文档，或仅作为各文件更新日志中的单行记录。
6. 若某轮 review 发现共性坑，优先把可复用规则写回本 GUIDE；只属于单 venue / 单年度的未闭合事实写入对应 README 的“证据与核查记录”。SUMMARY 只保留读者需要快速看到的聚合状态和升级条件。
7. 更新日志表是 SUMMARY 中唯一允许保留单次 PR / 编辑流程信息的位置，且必须按时间降序排列。

## 3. 时间格式规范

本库区分两类时间字段：

1. **投稿 / 事件 / 会期时间**：默认精确到分钟，格式统一为：

```text
yyyy-mm-dd hh:mm
```

2. **信息更新时间 / 更新日志时间**：默认精确到秒，格式统一为：

```text
yyyy-mm-dd hh:mm:ss
```

补充规则：

1. 若官方只给日期，不给具体时间，写成 `yyyy-mm-dd 待补时刻`，并在备注中说明“官方仅公布日期”。
2. 若官方只给日期且明确时区，写成 `yyyy-mm-dd 待补时刻 AoE` 或 `yyyy-mm-dd 待补时刻 UTC-12h`；其语义是“日期与时区已核验，具体钟点未公布或待补”，不得理解为日期本身待补。
3. 若官方给出 timezone，必须保留 timezone，例如 `2026-01-15 23:59 AoE`。
4. 若官方给出多个时区，以官方原文为准，不擅自换算；如需换算，另加一列 `北京时间换算`。
5. 历史更新日志中已存在的 `yyyy-mm-dd hh:mm` 分钟级记录可以保留；新写或本轮触碰的文库级更新日志默认使用秒级，若能从 `git log` 或其他可追溯记录恢复秒级时间，应优先补到秒。
6. 所有名为“更新日志”的表格必须按时间降序排列，最新记录放在表头后的第一行；新增日志时不得简单追加到表格末尾。若本轮修改触及某个文件，必须顺手校正该文件更新日志顺序。

## 4. 来源优先级

### 4.1 会议来源优先级

1. 官方年度主页，例如 `conf.researchr.org/home/icse-2026`。
2. 官方 `Call for Papers` / `Important Dates` / track page。
3. 官方 proceedings 页面，例如 ACM DL、IEEE Xplore、Springer LNCS、Dagstuhl、USENIX 官方页。
4. `DBLP` 年度页面，用于论文名录 fallback 或交叉核验。
5. 其他第三方页面只可作为发现线索，不能作为最终证据。

会议核心人员情报的来源优先级：

1. 官方年度 organizing committee / program committee / track chair / steering committee 页面。
2. 官方年度主页、track page 或 conference series 页面中的人员信息。
3. 学会、出版社或主办组织的官方公告。
4. 个人主页、机构主页、实验室主页。
5. DBLP、Google Scholar、Semantic Scholar、ORCID 等学术入口。
6. 第三方介绍页只可作为发现线索，不得单独支撑研究方向、代表作或近年论文结论。

会议核心人员的 `官方角色来源` 必须能直接支撑“姓名 + 具体角色 / committee 层级”。只出现 series 主页、年度主页壳、CFP、Important Dates、投稿系统、第三方简介或个人主页时，不得写成已核验官方角色；应降级为 `学术线索 / 官方角色页待补`，核验状态写 `⏳ 待核验`，并把缺口写入待补 / 风险记录。

会议历史投稿系统补充纪律：历史年度的 submission system 只记录当年官方 CFP / Important Dates / author instructions 明确给出的入口；若入口已经关闭、重定向、登录后不可见或只剩 EasyChair / HotCRP / PCS 等历史壳，应写成 `历史投稿入口已关闭 / 登录后流程未获可审计正文`，不得用当前年度投稿系统反推旧年度，也不得把投稿系统入口冒充年度主页、CFP 或 accepted papers 来源。ESEM 这类实证会议的历史年度尤其要保留“官方来源仍可证明当年使用过该系统”和“当前是否还能访问正文 / 表单”两层事实。

### 4.2 期刊来源优先级

1. 期刊官方主页。
2. 官方 author guidelines / submission guidelines。
3. 出版商 volume / issue / articles in press / online first 页面。
4. 官方 special issue `CFP` 页面。
5. `DBLP` 年度页面，用于年度论文名录 fallback 或计数核验。

期刊核心编辑人员情报的来源优先级：

1. 官方 journal editorial board / editorial team / editors 页面。
2. 出版商 journal 页面中的 Editor-in-Chief / Editors-in-Chief / Managing Editor / Editorial Board leadership 信息。
3. 个人主页、机构主页、实验室主页。
4. DBLP、Google Scholar、Semantic Scholar、ORCID 等学术入口。
5. 第三方介绍页只可作为发现线索，不得单独支撑研究方向、代表作或近年论文结论。

期刊核心人员指 Editor-in-Chief / Editors-in-Chief、Co-Editor-in-Chief、Managing Editor、Associate / Area Editor-in-Chief、Editorial Board leadership、官方列出的同等编辑领导角色，以及当年 special issue / topical collection guest editor。期刊核心人员的当前角色必须由官方 editorial board / editorial team / editors 页面或出版商 / 学会任命公告支撑；个人主页、机构页和 DBLP 只能补研究方向、代表作和近 5 年论文入口，不能单独支撑当前 editorial roster。

补充纪律：若 Wiley / ACM / IEEE / Elsevier / ScienceDirect 等 publisher 页面在命令行环境中返回 WAF、Cloudflare、403、SPA 壳或登录页，必须保留官方 URL 作为核验入口，并在对应字段写清“未获公开可审计正文”；不得用第三方页面替代当前官方 roster、author guidelines、articles in press、online first 或卷期正文，也不得臆造 Editor-in-Chief / editorial board 当前名单。ScienceDirect 命令行 `403` / WAF 只说明 CLI 抓取受限，不等价于官方页面不存在；JSS / IST / SCP 这类 Elsevier 期刊应保留 ScienceDirect / Elsevier 官方入口并标注访问风险，DBLP 只能作论文名录或计数 fallback。

## 5. 核心 URL 字段与超链接规范

后续数据填充不是只写摘要，而是要把可复用入口直接挂进表格，方便人和 AI 点击核验。

### 5.1 会议必须维护的核心 URL

会议根 README 与年度 README 至少维护以下链接字段：

| 链接字段 | 放置位置 | 来源优先级 | 缺失时写法 |
|---|---|---|---|
| 官方 series page | venue 根 README 基本信息与核心链接索引 | 官方长期主页 | `待补` |
| 官方年度主页 | venue 年度汇总表、年度 README、TIMELINE | 官方年度主页 | `⏳ 待官网` 或 `⏳ 已检索未公布` |
| CFP / Call for Papers | venue 年度汇总表、年度 README | 官方 CFP / track CFP | `未公布` / `待补` |
| Important Dates | venue 年度汇总表、年度 README、TIMELINE | 官方 dates 页；可与 CFP 同页 | `未公布` / `待补` |
| Submission system | venue 年度汇总表、年度 README | 官方投稿入口 | `未公布` / `不公开` |
| Program / accepted papers | venue 年度汇总表、年度 README | 官方 program / accepted paper list | 未结束写 `未公布` |
| Proceedings | venue 年度汇总表、年度 README | 出版商 / 官方 proceedings | 未发布写 `未公布` |
| DBLP 年度页 | venue 年度汇总表、年度 README | DBLP | 仅 fallback，写明口径 |

会议根 README 的年度表不允许只写“见年度页”；至少官方年度主页、CFP / Important Dates、论文名录 / proceedings、DBLP 年度页这些核心入口要能直接点击。

PR-7 ESEM 填充后的补充规则：

1. ESEM 历史年度投稿系统若来自当年官方 CFP / submission instructions，可以记录为历史事实；若入口已关闭或需登录，字段写 `历史入口已关闭 / 登录后流程未获可审计正文`，不要改写成 `未公布`，也不要用新年度系统补旧年度。
2. ESEM 年度主页、submission system、program / accepted papers、proceedings 和 DBLP 年度页必须分字段维护；投稿系统只能证明投稿入口，不能替代年度主页、CFP、Important Dates 或论文名录。
3. 若官方年度站点只保留 program / proceedings 而历史 CFP 消失，应把 program / proceedings 作为论文入口来源，把 CFP / dates 写 `待补` 或 `⏳ 已检索未公布`，并在证据记录说明已检索的官方入口。

### 5.2 期刊必须维护的核心 URL

期刊根 README 与年度 README 至少维护以下链接字段：

| 链接字段 | 放置位置 | 来源优先级 | 缺失时写法 |
|---|---|---|---|
| Journal homepage | 期刊根 README、年度 README | 出版商官方主页 | `待补` |
| Aims and scope | 期刊根 README 核心链接索引 | 官方 scope 页 | `待补` |
| Author guidelines | 期刊根 README、年度汇总表、年度 README、TIMELINE 未定日期表 | 官方指南 | `待补` |
| Submission system | 期刊根 README、年度汇总表、年度 README、TIMELINE 未定日期表 | 官方投稿入口 | `待补` |
| Special issue / topical collection CFP | 年度汇总表、年度 README、TIMELINE dated event | 官方专刊 CFP | 无则 `无已知` |
| Volume / issue archive | 年度汇总表、年度 README | 出版商卷期页 | `待补` |
| Articles in press / online first | 年度汇总表、年度 README | 出版商 online first 页 | `待补` |
| DBLP 年度页 | 年度汇总表、年度 README | DBLP | 仅 fallback，写明口径 |

期刊 rolling submission 不进入 dated Mermaid，但 [TIMELINE.md](./TIMELINE.md) 的“期刊滚动投稿 / 未定日期”表也必须挂 author guidelines、submission system、volume / issue、online first 和本库年度页链接。

PR-4 期刊填充后的补充规则：

1. Springer `collections` / topical collections 若给出明确 submission deadline，应进入对应年份事件表和 Mermaid；若只给 revision / final decision 的月份，不能硬凑具体日期，只能放备注或待补记录。
2. Requirements Engineering 这类期刊 collection deadline 是期刊专刊事件，不是同名会议 deadline；TIMELINE 的 `类型-CCF` 应写作 `期刊专刊-🥈`、`期刊专刊-🥉` 等 emoji 编码，不得回退为旧式 CCF 字母文本。
3. STTT 这类期刊常包含 TACAS / SPIN / FMICS / Runtime Verification / ECBS 等 conference-based special issue、invited 或 extended papers；DBLP `entry article` baseline 不能与对应会议 proceedings 数混算，也不能用会议会期或会议 CFP 反推期刊 deadline。
4. Wiley Online Library / Wiley Author Services / Equinocs、ScholarOne 等 publisher 或投稿系统若在命令行环境返回 WAF、Cloudflare、403、SPA / 登录壳，应记录为“官方入口已定位，正文 / 具体表单 / journal routing 未获公开可审计正文或登录后流程”；不得用第三方页面替代 STVR 这类 Wiley 期刊的当前 roster、author guidelines 或卷期正文。

PR-8 期刊填充后的补充规则：

1. Elsevier / ScienceDirect 页面若在命令行环境返回 WAF/403，只能确认官方入口；scope 正文、editorial board 当前 roster、special issue deadline、guest editor、volume / issue 正文和 Articles in Press 当前列表均应写作“未获公开可审计正文”，不得用第三方页面或 candidate URL 补成已核验事实。
2. ScienceDirect `special-issues` / `about/call-for-papers` 中的 candidate special issue 只有在公开可审计核验到明确 submission deadline 后，才能进入 [TIMELINE.md](./TIMELINE.md) 年度 dated event 和 Mermaid；否则只进入期刊根 README / 年度 README 的 candidate 线索和待补记录。
3. Editorial Manager 投稿系统 code 不得按 venue slug 臆造；例如 SCP 使用 `scico`，不是 `scp`。只能记录已定位的官方 / 出版商跳转或可访问投稿入口，并在登录 / 表单细节处保留待核验说明。

PR-7 实证 / 质量期刊填充后的补充规则：

1. Springer `collections` / topical collections 若状态为 `Closed`，仍可作为历史 special issue / collection 事实记录；若官方页给出 historical submission deadline，应按事件发生年份进入 [TIMELINE.md](./TIMELINE.md) 的历史 dated event，并在备注写明 `Closed / 历史 deadline`。Closed collection 不得写成当前 `🟡 专刊征稿`，也不得反推未来年度 active CFP。
2. Empirical Software Engineering 等 Springer 期刊 collection 页面可能同时列出 `Submission deadline`、`Notification`、`Revision due`、`Final decision`、`Publication` 等多类事件；年度 README 和 [TIMELINE.md](./TIMELINE.md) 必须保留官方事件语义，不能把 notification、revision 或 final decision 统一改名为 submission deadline。只有官方给出明确日期的事件进入 dated 表；只给月份或季度的事件只能写入备注 / 待补记录。
3. Special issue / topical collection editors、guest editors 或 collection editors 是当期专题角色，不等同于长期 editorial board / editorial leadership。除非同一人员另有官方当前 editorial board 页面支撑，否则不得把 collection editor 写入期刊根 README 的当前核心编辑人员正表；应放在年度 special issue / collection 小节或单独“专题编辑线索”小节。
4. Elsevier / ScienceDirect 的 guide for authors、volume / issue、articles in press、online first、editorial board 页面若在 CLI 中返回 `403`、WAF、JS 壳或空正文，应保留官方链接并标注 `CLI 403/WAF，未获公开可审计正文`；不得用 DBLP、Scimago、LetPub、Guide2Research 或第三方索引替代官方入口。DBLP 可用于年度论文名录 / 计数 fallback，但不能支撑 author guidelines、current roster 或 articles in press 当前性。


### 5.4 PR #63 CCF 名录与 LLM4Modeling-SE 扩展补充规则

1. CCF 等级优先以 [CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) 为主证据；若 CLI 遇到阿里云 WAF / CAPTCHA / 动态页壳，只能写“官方入口已定位，正文未获公开可审计正文”，不得把 `ccf.atom.im` 或旧 [../VENUES.md](../VENUES.md) 写成官方事实。
2. `ccf.atom.im` 只能作为非官方机器检索镜像 / 差集筛查线索；其 `2026 / 第七版` 标注必须写成镜像标注或待官方核验线索。
3. `journal-b-ase` 必须与 [conf-a-ase](./conf-a-ase/README.md) 消歧；期刊常规 rolling 不进 dated Mermaid，Springer collection guest editors 不混入长期 editorial board。
4. `conf-b-caise` 只作为 Information Systems Engineering / conceptual modeling / requirements / MDE 分流；Forum、DC、Workshop、BPMDS、EMMSAD 与 main conference 计数分开。
5. `conf-c-iceccs` 是 🥉 档 P2/P3 工程案例观察，不升级为 P0/P1 主投目标；未找到 stable series page 或 2024 official annual site 时写待补，不用 DBLP / 第三方页面冒充官方。

### 5.3 Markdown 链接写法

1. 已找到 URL 时，表格中直接写 Markdown 链接，例如 `[ICSE 2026](https://conf.researchr.org/home/icse-2026)`。
2. 本库内部页使用相对路径，且示例链接必须真实可达：在文库根文档中写 [`conf-a-fse/2026`](./conf-a-fse/2026/README.md)、[TIMELINE.md](./TIMELINE.md)；在 venue 根 README 中才写 `./2026/README.md` 这类相对年度页。
3. 未找到 URL 时不要伪造链接，写 `待补`、`未公布`、`无已知` 或 `⏳ 已检索未公布`，并在证据 / 核查记录里写核查时间。
4. 模板中的外部 URL 占位符不得写成 Markdown 链接；统一写 `待补（占位：OFFICIAL_URL；核验后改为 Markdown 链接）`。这样能避免模板被误读为已有可点击事实来源。
5. 模板文件位于 [templates/](./templates/) 下，`./2026/README.md`、`../TIMELINE.md`、`../../TIMELINE.md` 这类路径在模板目录本身并不真实成立，因此模板占位默认写成代码样式纯文本；实例化到 venue 根目录或年度目录后，必须改回可点击相对 Markdown 链接。
6. 第三方聚合页只能放在备注或 fallback，不得放进“官方来源”列。
7. 官方年度主页、series page、organizer call、CFP、Important Dates、submission system、program / accepted papers 和 proceedings 是不同字段；只有能直接代表该年度 edition 的页面才可写入“官方年度主页”。Series page / organizer call / submission system 只能放入对应字段或 fallback / 备注，不得冒充年度主页或 CFP。
8. 不得把某一个年度站点冒充为 stable series page；若未发现独立稳定 series page，根 README 写 `待补`，可把 DBLP venue index 或官方年度页写作 fallback / 年度事实来源。
9. 命令行访问遇到证书问题时可以使用 `curl -k`、带 `User-Agent` 或公开归档继续核验；但 `404`、Access denied、空页、WAF 返回页、未公布占位、只有 series 入口等都不是有效事实来源，必须写成访问风险或 `⏳ 已检索未公布`。
10. QRS 这类 techconf 年度站需要区分 yearly site、series latest、proceedings policy、submission statistics、regular acceptance statistics、program / accepted list、IEEE proceedings 与 DBLP fallback；submission stats 或 regular acceptance stats 不能替代最终 accepted paper count。
11. TASE 这类年度站分散且缺少 stable series page 的会议，不得用最新年度主页冒充 series page；Important Dates、CFP、Accepted Papers、Springer TOC、DBLP 年度页和 Springer about 的 full / short / invited 口径必须各自标明来源，发生日期冲突时说明采用依据。

### 5.4 核心人员情报规范

核心人员情报是本库的一等学术情报，不是可选备注。它服务于后续判断 venue 的研究共同体、审稿偏好、主题连续性和潜在投稿适配度。

会议根 README 应维护“核心人员情报”小节。默认覆盖：

1. 当前 / 未来年度 General Chair、Program Chair、Research Track Chair、Technical Track Chair、Artifact / Tool / SEIP 等与本仓库 project 强相关 track 的 chair。
2. Steering Committee / Advisory Board / Organizing Committee leadership。
3. 在相关 track 或历年组织中反复出现、且与本仓库 project 强相关的领域权威。
4. 对 umbrella venue，例如 ETAPS，应区分 umbrella 层级、main conference / satellite conference 层级和具体 track 层级；不要把 TACAS chair、ETAPS general chair 和 workshop organizer 混写成同一类角色。

会议人员表至少包含：姓名、年度 / 层级、会议角色、单位、官方角色来源、主页或学术入口、主要研究方向、代表作或近 5 年论文入口、与本仓库 project 的关系、核验状态、核查时间。人员事实应优先来自官方 committee / track 页面；研究方向和代表作可来自主页、DBLP 或学术入口，但必须说明是公开资料判断。

期刊根 README 应维护“核心编辑人员情报”小节。默认覆盖 Editor-in-Chief / Editors-in-Chief、Co-Editor-in-Chief、Associate / Area Editor-in-Chief、Managing Editor、Editorial Board leadership、与本仓库强相关的 editorial board 成员，以及当年 special issue / topical collection guest editor。期刊人员表必须保留 `核验等级 / 当前性` 列，区分官方当前 roster、官方公告、个人 / 机构页候选线索和 legacy / 运营线索。

完整人员表放在各 venue 根 README；[SUMMARY.md](./SUMMARY.md) 只在 Venue 总表的精简字段中给出读者查阅入口和关键口径，不复制全量人员表，也不承载人员待补长表。

## 6. 会议 README 结构规范

每个会议根 README 必须包含：

1. 顶部 `信息更新时间`。
2. 基本信息：缩写、全称、CCF 大类与等级、出版方、官方 series page、DBLP venue page。
3. 官方 scope 与研究方向摘要。
4. 与本仓库 project 的相关性表。
5. 核心人员情报：至少覆盖当前 / 未来年度 General Chair、Program / Research Track Chair、Steering Committee、强相关 track chair 和领域权威；每行必须给出官方角色来源、研究方向 / 代表作来源、核验状态和核查时间。
6. `2022` 年以来年度汇总表，按年份降序排列。
7. 文末更新日志表。

年度汇总表至少包含：

| 字段 | 说明 |
|---|---|
| 年份 | 链接到对应年度 README |
| 阶段状态 | 使用 `emoji + 短文本`，例如 `🟢 投稿中` |
| 官方主页 | 链接到官方年度主页；未找到则写 `待补` |
| CFP / Important Dates | 直接链接到官方 `CFP` 或日期页，不允许只写纯文本 |
| Abstract deadline | 精确到分钟；无则 `未公布` |
| Submission deadline | 精确到分钟；无则 `未公布` |
| Notification | 精确到分钟；无则 `未公布` |
| 会期 | 起止日期或日期时间；根 README 年度汇总表统一使用 `yyyy-mm-dd..yyyy-mm-dd`，跨年或多地会议须在备注中解释；TIMELINE 表格可使用更适合人读的区间写法 |
| 论文数量 | 仅已召开且可核验时填写；根 README 单元格必须携带计数口径，例如 `Research Track: 245`、`DBLP inproceedings: 27`、`ETAPS umbrella: 138；TACAS: 56`；年度 README 继续解释计数来源 |
| 论文名录 | 官方 program / accepted papers / proceedings 优先，`DBLP` 可作 fallback，必须是可点击链接 |
| 核验状态 | 例如 `已核验`、`部分核验`、`待补` |

说明：`阶段状态` 列按用户需求明确允许 `emoji + 短文本`，它不是仓库通用“emoji 口径列”。

## 7. 会议年度 README 结构规范

每个会议年度 README 必须包含：

1. 顶部 `信息更新时间`。
2. 年度基本信息：venue、年份、地点、官方主页、主办组织、出版方。
3. 关键链接：官方主页、`CFP`、important dates、submission system、proceedings、`DBLP`。
4. 重要时间点表：所有时间精确到分钟。
5. Track 信息：Research、SEIP、NIER、Tool Demo、Artifact 等，按该 venue 实际情况记录。
6. 论文名录与数量：仅会议已召开或 proceedings 已发布时填写。
7. 与本仓库 project 的年度相关性观察。
8. 证据与核查记录。
9. 文末更新日志表。

## 8. 期刊 README 结构规范

期刊没有会议式年度 ddl，因此期刊根 README 应改用期刊结构，至少包含：

1. 顶部 `信息更新时间`。
2. 基本信息：缩写、全称、CCF 大类与等级、出版商、ISSN、主页、author guidelines、submission system。
3. Scope 与栏目类型。
4. 投稿模式：rolling submission、special issue、open access / hybrid、article type。
5. 核心编辑人员情报：至少覆盖 Editor-in-Chief / Editors-in-Chief、Co-Editor-in-Chief、Associate / Area Editor-in-Chief、Managing Editor、Editorial Board leadership 或官网列出的等价核心角色；每人记录姓名、期刊角色、单位、官方来源、主页或学术入口、主要研究方向、代表作或近 5 年代表论文入口、与本仓库 project 的相关性判断、核验等级 / 当前性和核查时间。
6. 与本仓库 project 的相关性表。
7. `2022` 年以来年度汇总表，按年份降序排列。
8. 文末更新日志表。

期刊核心编辑人员情报应优先写在期刊根 README，作为当前 editorial leadership 入口。年度 README 不重复长期核心编辑人员；只有当某年度 special issue / topical collection 有 guest editor、年度 editorial team 或人员变更与当年事实直接相关时，才在年度 README 中单独记录。

Special issue / topical collection editors 必须与长期 editorial board 分离：前者服务于某一专题、collection 或年度征稿，后者才是期刊当前 roster / leadership。根 README 的核心编辑人员表只收官方当前 editorial board / editorial team / editors 页面或任命公告能支撑的长期角色；专题编辑若没有长期角色证据，只能作为年度事实或候选线索记录，并保留 `待官方 roster 复核`。

期刊核心编辑人员表必须显式区分证据等级和当前性，避免把候选线索写成已核验 roster。推荐使用 `核验等级 / 当前性` 列，至少区分：

1. `官方当前 roster 核验`：来自 journal editorial board / editorial team / editors 当前页。
2. `官方公告核验`：来自 publisher / society 对 EiC、Co-EiC 或等价核心角色的任命公告，但不等同于完整 roster。
3. `官方访谈 / 期刊公告维护角色`：可记录 Information Director、special section guest editor 等角色，但必须说明不等同于完整 editorial leadership。
4. `个人 / 机构页候选线索`：可作为发现线索，必须写“待官方 roster 复核”，不得写成已完全核验当前角色。
5. `legacy / 运营线索`：历史镜像、非 publisher 域名、运营联系人等只能放在补充说明或待复核小节，不应混入当前核心编辑人员正表。

研究方向、代表作或近 5 年论文入口来自公开资料时，必须说明是基于公开主页、DBLP、机构页等的判断，不是期刊官方评价。

期刊年度汇总表至少包含：

| 字段 | 说明 |
|---|---|
| 年份 | 链接到对应年度 README |
| 年度状态 | 例如 `🟢 滚动开放`、`✅ 年度已归档` |
| Author guidelines | 当年核验到的官方指南链接，必须可点击 |
| Special issue | 当年 special issue `CFP` 链接或 `无已知`，有链接时必须可点击 |
| 关键截止时间 | special issue ddl；rolling journal 可写 `滚动投稿` |
| Volume / issue | 出版商年度卷期入口，必须可点击 |
| Online first | 出版商 online first / articles in press 入口，必须可点击 |
| 论文数量 | 年度结束且可核验时填写 |
| 论文名录 | 出版商年度页面优先，`DBLP` fallback |
| 核验状态 | `已核验`、`部分核验`、`待补` |

## 9. 期刊年度 README 结构规范

每个期刊年度 README 至少包含：

1. 顶部 `信息更新时间`。
2. 年度基本信息：journal、年份、出版商、volume / issues。
3. 投稿入口核验：author guidelines、submission system、article type。
4. 当年 special issue / topical collection 记录。
5. 年度论文入口与论文数量。
6. 与本仓库 project 的年度相关性观察。
7. 证据与核查记录。
8. 文末更新日志表。

## 10. 阶段状态口径

会议推荐状态：

| 状态 | 使用场景 |
|---|---|
| `⏳ 待官网` | 尚未找到官方年度主页 |
| `🟦 已有主页` | 已有年度主页，但尚未公布完整 CFP / 日期 |
| `🟢 投稿中` | 投稿窗口尚未关闭 |
| `🟡 审稿中` | submission 已截止，正在审稿 / rebuttal / author response |
| `🟡 已截稿` | submission 已截止，等待审稿 / rebuttal |
| `🟣 通知后` | acceptance notification 已出，等待 camera-ready / 会期 |
| `🔵 会期临近` | camera-ready 后且会议尚未结束 |
| `✅ 已结束` | 会议已结束，或 proceedings 已发布 |
| `⚠️ 信息不全` | 官方信息存在矛盾或关键字段缺失 |

期刊推荐状态：

| 状态 | 使用场景 |
|---|---|
| `🟢 滚动开放` | 常规投稿开放 |
| `🟡 专刊征稿` | 有 special issue / topical collection 正在征稿 |
| `🟣 专刊审稿` | special issue 截稿后等待处理 |
| `✅ 年度已归档` | 年度卷期和论文数量已可核验 |
| `⚠️ 信息不全` | 年度卷期、论文数量或 special issue 信息待补 |


核验状态推荐口径：

| 状态 | 使用场景 |
|---|---|
| `🟢 已核验` | 关键字段已有官方来源或 DBLP fallback 交叉核验 |
| `🟡 部分核验` | 关键链接可用，但时间点、论文数量或计数口径仍有缺项 |
| `⏳ 待核验` | 已有待查字段，但尚未完成来源核验 |
| `⚠️ 矛盾待解` | 官方页、出版页、DBLP 或历史记录之间存在明显冲突 |

注意：阶段状态描述会议 / 期刊生命周期，核验状态描述证据完整度，二者不得混写。


### 10.1 补充状态词（2026-08-07 增补）

本节此前的词表未覆盖以下三类实际使用中的状态，现予补入，避免各 venue 各写各的：

| 状态 | 适用 | 说明 |
|---|---|---|
| `⏳ 待官网（槽位已建未发布）` | 会议 | researchr / 官方站返回 **HTTP 200 + `Access denied`**（不是 404），页面槽位已建但未公开发布。位于 `⏳ 已检索未公布` 与 `🟦 已有主页` 之间，判别与实例见 [§16.6.2](#1662-access-denied--404researchr-入口的三种语义)。 |
| `🟦 已有预告` | 会议 | 年度主页尚未建站或未公开，但**另有官方来源**已公布该年度的地点 / 月份等实质事实（如 ICSE 指导委员会官方站、issta.org、esec-fse.org）。必须挂该官方来源 URL。 |
| `🟦 主办征集中` | 会议 | 会议族官方组织（如 FME）已发出 call for organizers，但主办方 / 地点 / CFP 均未定。仅适用于有此流程的会议族。 |

上述三态与 §12.6 的迁移链关系见 [§16.6.2](#1662-access-denied--404researchr-入口的三种语义)。

## 11. TIMELINE.md 结构规范

[TIMELINE.md](./TIMELINE.md) 是跨 venue 投稿时间线总览，必须随着 venue README / 年度 README 同步维护。

### 11.1 年度章节

1. 年份按降序排列，例如 `2028`、`2027`、`2026`、`2025`、`2024`、`2023`、`2022`。
2. 年份表示事件实际发生年份，不等同于会议 edition 年份；例如 `ICSE 2027` 的 abstract / submission deadline 若发生在 `2026`，应进入 `2026` 年章节，并在 Venue 字段保留 `ICSE 2027`。
3. 每个年份章节内先写投稿事件总表，再写 Mermaid 可视化。
4. 同一年表格内的事件必须按日期时间升序排列。
5. 当前年份 + 1 和当前年份 + 2 的章节必须存在，并在实际检索后记录 `⏳ 已检索未公布` 或可用官方信息；更远未来年度一旦能找到官方主页、`CFP` 或 important dates，就必须新增对应年份章节。

### 11.2 年度事件表字段

| 字段 | 说明 |
|---|---|
| 日期时间 | `yyyy-mm-dd hh:mm`；官方只给日期时写 `yyyy-mm-dd 待补时刻` |
| Venue | 链接到 venue 年度 README；模板阶段可写 `ICSE 2026 -> ./conf-a-icse/2026/README.md`，实例化后改为真实 Markdown 链接 |
| 类型 | 会议 / 期刊专刊 / 期刊滚动投稿 |
| Track / 栏目 | Research、Tool Demo、SEIP、Special Issue 等 |
| 事件 | Abstract deadline、Submission deadline、Notification、Camera-ready、Conference dates 等 |
| 阶段状态 | 使用本 GUIDE 的阶段状态口径 |
| 事件官方来源 | 官方 `CFP`、Important Dates、special issue、author guidelines 或年度 README 链接，必须可点击 |
| 年度主页 | 官方年度主页或期刊年度入口链接，必须可点击 |
| 论文集 / 名录 | proceedings、accepted papers、volume / issue、online first 或 DBLP fallback；无则写 `未公布` / `不适用` |
| 本库年度页 | 链接到本库对应年度 README |
| 备注 | AoE、官方仅给日期、DBLP fallback、计数口径等 |

### 11.3 Mermaid 规范

1. 默认使用 `gantt` 图，不使用 Mermaid `timeline` 语法作为主图；`gantt` 在 GitHub 上更稳定，且适合表达 deadline / 会期窗口。
2. 单日 deadline 使用 `milestone`，多日窗口使用普通任务。
3. Mermaid 图只放短标题，不放 URL；来源链接必须留在年度表格中。
4. 如果某一年事件超过 `40` 条，按 `🏆 / 🥈 / 🥉 档`、`会议 / 期刊专刊` 或本轮 PR 增量拆成多张 `gantt` 图；年度总表仍保留统一事实总账，每张分片图的事件数原则上不超过 `40`。
5. Mermaid 展示 label 必须使用 **venue edition 年份**，不能使用事件发生年份。例如 `FSE 2026` 的 `2025-09` submission 在图中显示 `FSE26 Submission`，而不是 `FSE25 Submission`。
6. Mermaid event id 推荐使用 `<venue_slug>_<event_year>_<sequence>_<yyyymmdd>`，其中 `sequence` 只保证同一事件发生年份内唯一；展示 label 与 event id 可以不同。
7. Mermaid label 使用短但完整的英文事件词：`Abstract`、`Submission`、`Notify`、`Camera`、`Rebuttal`、`Conference`；不要写成 `Notificati`、`Cameraread` 等机械截断词。
8. Mermaid 更新后必须至少本地 Markdown 预览；若本地具备 Mermaid CLI，可补充渲染检查。

### 11.4 同步规则

1. 新增或修改任何年度 README 中的投稿相关 important date 后，必须同步检查 [TIMELINE.md](./TIMELINE.md)。`Conference dates` 也是 important date；只要年度 README 已有官方会期且事件发生年份在本库范围内，就必须进入 TIMELINE 表格和 Mermaid，不能只同步 submission / notification。
2. 若某个时间点因官方来源冲突被标为 `⚠️ 矛盾待解`，TIMELINE 表格也必须保留该状态，不得只在 venue 年度 README 中记录。
3. [TIMELINE.md](./TIMELINE.md) 只汇总已进入本库的 venue，不替代 P1/P2 待补清单。
4. 会议填充负责维护会议 dated events；期刊填充负责维护期刊 rolling 表和期刊 special issue dated events。合流时不得互相删除已经核验的事件行。
5. 临时 PR 增量表、`_events_draft.md` 或等价草稿只能作为迁移过程中的审计辅助，不得长期作为 dated event 事实源；一旦事件已核验，应并入正式年份章节与 Mermaid。
6. 最终提交前必须删除临时草稿，并把所有根 README / 年度 README 中的草稿链接改成指向 [TIMELINE.md](./TIMELINE.md) 的事实陈述；不得在正式文档中留下 `_events_draft.md` 死链接或“主 session 合流时”这类 PR 内部流程语气。
7. TIMELINE 表格与 Mermaid 必须一起更新：表格按事件发生日期升序，Mermaid 不放 URL，且图中 edition label 必须与表格 Venue edition 一致。

## 12. 常态化投稿情报更新流程

本节用于处理“最新投稿情报 / 近期 deadline / CFP 更新 / accepted papers 发布 / 期刊 special issue 状态变化”这类长期滚动维护任务。它不替代 §14 的一次性数据填充流程，也不允许绕过 [01-venue-scope.md](./01-venue-scope.md) 的 venue 范围约束；它只规定**已收录 venue** 如何持续刷新事实并服务真实投稿决策。

### 12.1 适用任务与非目标

适用任务包括：

1. 会议年度主页、`CFP`、Important Dates、track page、submission system、program / accepted papers、proceedings 或 DBLP 年度页发生更新。
2. 期刊 author guidelines、submission system、special issue / topical collection、collection status、guest editor、volume / issue、online first 或 DBLP 年度页发生更新。
3. [TIMELINE.md](./TIMELINE.md) §3“近期投稿窗口速览”中的窗口临近、过期、延期、重开或需要从 `待补时刻` 升级为精确时刻。
4. 当前年份 + 1 / 当前年份 + 2 或更远未来年度从“未公布”变成“已有 official home / CFP / dates”。
5. 投稿前专项决策需要确认未来 3--6 个月内哪些窗口仍可行动、证据等级如何、风险 caveat 是否会影响准备节奏。

非目标包括：

1. 不新增新的 venue；确需新增时必须先修改 [01-venue-scope.md](./01-venue-scope.md) 与对应 PR body。
2. 不把 P2 邻近观察 venue 升级为 P0/P1 主投目标；P2 只能因已有 open 窗口或用户明确指定而临时纳入 watchlist，并在备注中保留 `P2 / 不升级`。
3. 不用第三方 deadline 聚合页、论坛、博客或个人整理表替代官方来源。
4. 不把一次常态化刷新写成全库重审；除非用户明确要求，否则只刷新 watchlist 与受影响文件。

### 12.2 刷新频率与触发条件

| 刷新类型 | 建议频率 / 触发 | 主要目标 | 最小输出 |
|---|---|---|---|
| 近期窗口高频刷新 | 以本轮刷新日期为起点向后 3--6 个月；投稿决策前必须刷新，密集期可每 1--2 周刷新 | 确认 open / extended / closed / reopened deadline、时区、证据等级和准备风险 | 年度 README、根 README、[TIMELINE.md](./TIMELINE.md) §3 与对应年度表 / Mermaid；必要时只更新 [SUMMARY.md](./SUMMARY.md) Venue 总表短摘要和更新日志 |
| 正常月度维护 | 每月或阶段性调研时刷新未来 6--12 个月 | 发现 next edition、official home、CFP、dates、special issue 状态变化 | 年度 README 占位或事实升级、TIMELINE 待补 / 近期窗口更新 |
| 年度滚动扩展 | 每年年初、CCF / venue 年度信息集中发布期，或当前年份 + 2 信息不足时 | 维持 `当前年份 + 2` 默认检索下限；更远未来有官方信息也纳入 | 新增 / 更新未来年度 README、根 README 年度汇总、TIMELINE 年份章节 |
| 历史补证 | accepted papers、proceedings、volume / issue、DBLP 年度页发布后 | 闭合已结束年度事实链，补论文入口和计数口径 | 年度 README、根 README；若影响全库聚合状态，再更新 SUMMARY §13 合并待补表 |
| 触发式刷新 | 官方 CFP 延期、postponed、reopened、special issue open/closed、CCF 更名、WAF 页面可公开审计访问时 | 修正会直接影响投稿决策或证据等级的事实 | 受影响文件最小闭环 + 更新日志 |

### 12.3 默认 watchlist 启动口径

常态化刷新不能默认全量扫描 42 个 venue。若用户没有给出明确目标，本轮 watchlist 按以下顺序确定：

1. **P0 默认核心**：P0 22 个 venue 永远是投稿决策主线候选，但本轮只实际刷新其中“未来 6 个月有窗口、待补项影响决策、或已有 next edition 线索”的 venue；该筛选口径由本 GUIDE 与 [TIMELINE.md](./TIMELINE.md) §3 共同约束，不再依赖 SUMMARY 的流程小节。
2. **P1 近期窗口**：P1 venue 只有在 [TIMELINE.md](./TIMELINE.md) §3 已有未来 6 个月 open 窗口、[SUMMARY.md](./SUMMARY.md) §13 合并待补表指向近期窗口、或官方 next edition 已公布时进入本轮 watchlist。
3. **P2 临时观察**：P2 venue 只在 [TIMELINE.md](./TIMELINE.md) §3 已有明确 open 窗口、用户指定投稿分流，或其 deadline 与当前 project 有直接机会窗口时临时纳入；所有表格备注必须保留 `P2 / 不升级`。
4. **高风险来源回访**：WAF/403/CAPTCHA/Authwall、交互式页面受限、旧站证书、日期冲突、`待补时刻`、week/month-only、publisher candidate CFP 等高风险项可独立进入 watchlist。
5. **历史补证**：仅当 proceedings / DBLP / accepted papers 发布会影响论文数量或年度闭合时进入 watchlist；不要用历史补证挤占近期投稿窗口刷新。

若 watchlist 是由脚本、搜索或公开证据判断生成，必须在本轮 PR body、相关 venue README 更新日志、[TIMELINE.md](./TIMELINE.md) 或本 GUIDE 的规则段落中写明刷新日期、选择依据和未覆盖范围；SUMMARY 正文不承载 watchlist 生成过程。

### 12.4 单轮刷新闭环 checklist

每轮常态化刷新按以下顺序执行；除非用户明确要求只做只读调查，否则完成事实修改时不得跳步：

1. **读取入口**：先读 [README.md](./README.md)、本 [GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 的总览 / Venue 总表 / §13 待补与核查记录、[TIMELINE.md](./TIMELINE.md) §3（近期投稿窗口速览）与 §15（TIMELINE 待补与核查记录）；新增或跨批次 venue 时再读 [01-venue-scope.md](./01-venue-scope.md)。
2. **确定 watchlist**：按 §12.3 选择 venue、年度、track / special issue，并记录本轮刷新日期作为“未来 6 个月”计算锚点。
3. **核验官方来源**：会议查 official home、CFP / Important Dates、track page、submission system、program / accepted papers、proceedings、DBLP；期刊查 homepage、author guidelines、submission system、special issue / collection、volume / issue、online first、DBLP。
4. **更新年度 README**：年度页是单年度事实承载入口；新增 / 修改日期、状态、链接、论文入口、证据与核查记录时，先在年度页落地。
5. **更新 venue 根 README**：同步年度汇总表、当前阶段状态、核心链接索引、人员 / guest editor 或维护备注；不得让根表与年度页矛盾。
6. **更新 TIMELINE 年度表**：凡属于 dated event 的 abstract、submission、notification、camera-ready、conference dates、special issue deadline 等，都进入事件发生年份的年度表；会议 edition 年份保留在 Venue 字段。
7. **更新 TIMELINE §3 近期窗口**：只有截至本轮刷新日期仍可行动的 abstract / submission / special issue / intent 等窗口进入 §3；§3 是年度全量表的筛选视图，不是独立事实源。
8. **更新 Mermaid**：任何新增、删除或修改 dated event 都必须同步受影响年度 Mermaid；图中 label 使用 venue edition 年份，表格保留 URL 和 caveat。
9. **更新 SUMMARY 读者总表**：只有当 venue 事实、外部索引、年度入口、核心人员 / 计数口径或全库待补状态发生变化时，才更新 [SUMMARY.md](./SUMMARY.md) 的 Venue 总表或 §13 合并待补表；不得把本轮 watchlist、PR 执行过程或 TIMELINE §3 全量行复制进 SUMMARY 正文。单轮流程只在更新日志中保留一行。
10. **更新时间戳与更新日志**：修改过的 README / GUIDE / SUMMARY / TIMELINE / venue 文件均需更新 `信息更新时间` 与文末更新日志；新写日志默认精确到秒，历史分钟级记录可保留，日志按时间降序。
11. **同步散文与非表格落点（2026-08-07 新增，必做）**：前十步只覆盖**结构化表格**。同一个事实在本库最多有 **7 个落点**，其中三类**不在**上面任何一步里，且**无法被列数 / 排序 / multiset 这类不变量脚本发现**：

    | 遗漏落点 | 位置 | 为什么容易漏 |
    |---|---|---|
    | venue 根 README 的 **§7 维护备注 / 计数口径 bullet** | 散文，非表格 | 复述了同一事实但不在任何同步清单上；`journal-b-ase` 曾出现根表写对 `2026-08-15`、同文件 bullet 仍写已过期 `2026-07-15` 的**文件内自相矛盾** |
    | 年度页的 **§8 待补 / 风险记录**段 | 散文 | 常保留"官方仍为 TBD / 尚未到"这类**时效性判断**，事实更新后即失效 |
    | [TIMELINE.md](./TIMELINE.md) **§14 期刊滚动投稿 / 未定日期表** | 表格，但不在 §12.4 第 6/7 步的"年度表 / §3"范围内 | 它**长得像总览、实际是 live-state 列**（`截止时间` 列会随官方延期变化）；`2026-08` 那轮六处都改对了，唯独漏掉 §14，把仍开放的窗口写成已关闭 |

    **执行要求**：每完成一次事实更新，必须用该事实的**旧值**（旧日期 / 旧状态词 / 旧计数）对全库做一次 `grep`，逐条判定命中是「当前值残留」还是「合规的历史记录」。**合规的历史记录**指：位于 dated 更新日志中，或带有 `已作废` / `已更正` / `原记` / `保留历史` 等明确标记。除此之外的命中一律按当前值处理并修正。

    **如何识别一张表是不是 live 表（2026-08-07 补充判据）**：不要靠标题判断。以下三张表的标题都像"归档 / 审计 / 待补"，实际语义却是 **current-value**，`2026-08` 那轮各自漏改过至少一次：

    | 表 | 标题给人的印象 | 实际语义 |
    |---|---|---|
    | [TIMELINE.md](./TIMELINE.md) §6 PR-3 合流审计与风险记录 | 历史审计 | preamble 明写「只保留**未公布年度**、来源降级和后续复查风险」——是待办 |
    | [TIMELINE.md](./TIMELINE.md) §15 待补与核查记录 | 待补清单 | `当前处理` / `下一步` 两列都是给下一轮 agent 的**现行指令** |
    | [TIMELINE.md](./TIMELINE.md) §14 期刊滚动投稿 / 未定日期 | 滚动总览 | `截止时间` 列随官方延期变化——是 live 状态 |

    **通用判据**：一张表若**没有时间戳 / 核查时间列**、且单元格内容是**状态断言**（「未公布」「仍为 TBD」「尚未到」「不预设」等），它就是 live 表，必须进入本步的旧值 grep 范围。反之，带 dated 列的表（如各文件 §7 证据与核查记录）属历史快照，其中的旧值应**加作废标注而非改写**。

    ⚠️ `2026-08` 那轮的实证：`TIMELINE.md` §6 的 ICST 2027 行把「Research track / CFP 未公布」当当前值写着，**这个错误在本轮之前就已存在于 `main`**——说明 §6 从未被纳入任何同步流程，是只写不读的表。

12. **一致性检查**：运行本节 §12.10 的命令，并本地检查 Markdown 相对链接、emoji 列口径、Mermaid label、统计数字、P0/P1/P2 边界。

13. **不变量自查的强度要求（2026-08-07 新增）**：脚本自查必须校验**不变式**而非"我改对了吗"，且不变式要足够强：
    - 年度表 ↔ Mermaid **不能只比数量**（`2026-08` 那轮曾出现 `190 = 190` 但集合不同），必须按**日期 multiset** 比对；
    - §3 每一行必须能在对应年度表找到同日期同 venue 的事件（§3 是筛选视图，不是独立事实源）；
    - §3 不得含已过期行、重复行，以及 `Notification` / `Camera-ready` / `Conference` / `Rebuttal` 类型行；
    - **§3 每行的「日期时间」列与年度表对应行必须逐字一致**（不只是日期相同）——§3 是筛选视图，后缀差异（如一侧写 `AoE`、另一侧写 `AoE / UTC-12h`）即为不同步；
    - **§3 每行的 track / 事项名必须与年度表逐字一致**——简称与正式题名混用会让「§3 是年度表子集」这一不变量失效，也会让自动校验误报孤儿行；
    - 全库 Markdown 表格列数与表头一致；Mermaid milestone id 唯一；Mermaid 内不含 URL 与 emoji；更新日志降序；仓库内相对链接目标存在。

    **以上不变量已固化为可执行脚本**：[scripts/check_consistency.py](./scripts/check_consistency.py)。用法：

    ```bash
    cd ccf_venues && python3 scripts/check_consistency.py --today 2026-08-07
    ```

    每轮刷新与每次 review 都应直接运行它，而不是各自重写等价脚本（`2026-08` 那轮有四位 reviewer 分别重写了一遍，并因计数口径不同产生了跨两轮的争论）。

    **计数口径必须写死，避免跨轮次歧义（2026-08-07 补充）**：同一张年度表存在两种合法计数，二者相差「多日事件的结束日期是否单独计一次」：

    ```text
    数据行数（以 `| 20XX-` 开头的行）        + 日期区间行数 = 日期出现总次数
    2027：50 + 13 = 63        2026：192 + 40 = 232
    ```

    两种口径下 **表↔图不变量都应成立**（`50=50` 且 `63=63`）。报告数字时必须写明用的是哪一种；`2026-08` 那轮曾因 reviewer 用「日期出现总次数」、作者用「数据行数」而产生两轮口径分歧，最终由本换算式闭合。

    ⚠️ **但必须清楚脚本的边界**：以上不变量**抓不到散文中的旧事实**。第 11 步的旧值 grep 是唯一能覆盖该盲区的手段，不可用脚本通过来替代。

### 12.5 投稿决策字段与落点

常态化刷新应把投稿决策所需字段固定到合适文件，避免 GUIDE / SUMMARY / TIMELINE 各自形成第二套事实表。

| 字段 | 含义 | 权威定义 | 行级数据承载 | SUMMARY 口径 |
|---|---|---|---|---|
| 窗口状态 | `投稿中`、`已截稿`、`审稿中`、`已关闭`、`reopened` 等 | 本节 §12.6 与 §10 | 年度 README、根 README、[TIMELINE.md](./TIMELINE.md) §3 / 年度表 | 只写计数和风险摘要 |
| deadline 类型 | Abstract、Submission、Intent、Special issue、Notification、Camera-ready、Conference 等 | [TIMELINE.md](./TIMELINE.md) §4 与本节 | 年度 README、TIMELINE 表 | 不逐行复制 |
| 准确时间与时区 | 日期、时刻、AoE / UTC offset / local time、`待补时刻` | §3 时间格式规范 | 年度 README、TIMELINE 表 | 只记录待补时刻数量或高风险项 |
| 准备建议 | 是否仍可行动、需先投 abstract、需 artifact / rebuttal、是否邀请制 | 本节 | TIMELINE §3 备注、年度 README 备注 | 只写下一轮优先建议 |
| 相关 project | project_1~4 的投稿适配度 | README / venue 根 README 的 project 相关性 | venue 根 README、TIMELINE §3 备注（必要时） | 只写主题级建议 |
| 证据等级 | 官方完全核验、部分核验、交互式页面受限 待核验、第三方线索 | §12.7 | 年度 README 证据记录、TIMELINE 核验状态 | 高风险入口摘要 |
| 风险 caveat | WAF/403/CAPTCHA/Authwall、日期冲突、old page、candidate CFP、P2 不升级 | §12.7 / §12.9 | 年度 README、根 README、TIMELINE 备注 | 待补与核查记录 |

### 12.6 状态迁移规则

会议主链默认按以下状态迁移：

```text
⏳ 已检索未公布 -> ⏳ 待官网（槽位已建未发布） -> 🟦 已有主页 / 🟦 已有预告 -> 🟢 投稿中 -> 🟡 已截稿 / 🟡 审稿中 -> 🟣 通知后 -> 🔵 会期临近 -> ✅ 已结束 -> proceedings / DBLP 待补 -> 历史闭合
```

> `⏳ 待官网（槽位已建未发布）`、`🟦 已有预告`、`🟦 主办征集中` 三个状态词的定义与判别见 [§10.1](#101-补充状态词2026-08-07-增补) 与 [§16.6.2](#1662-access-denied--404researchr-入口的三种语义)。

其中 `⏳ 已检索未公布` 表示只找到 stable series、publisher placeholder 或旧站入口，尚无本年度 official home / CFP / dates；它不得被硬升为 `🟦 已有主页`，也不得作为事件本身进入 dated TIMELINE / Mermaid。若某条 dated event 已由官方日期支撑，TIMELINE 的论文集 / 名录等辅助列可以写 `⏳ 已检索未公布` 表示 proceedings、paper list 或卷期入口尚未发布；这不等同于把年度 placeholder 伪造成 dated event，但必须确保事件日期、阶段状态和来源列已核验。

期刊主链默认按以下状态迁移：

```text
🟢 滚动开放 / 🟡 专刊征稿 -> 🟣 专刊审稿 -> ✅ 年度已归档 -> volume / issue / DBLP 待补 -> 历史闭合
```

回退和异常迁移必须保留证据：

1. 官方 deadline extension、postponed、reopened CFP 可使 `已截稿` 回到 `投稿中`；必须写清原 deadline、新 deadline、官方来源和核查时间。
2. special issue / collection 从 `Closed` 回到 `Open`、从 invite-only 改为 public CFP、或从 candidate CFP 升级为官方 CFP 时，必须同步年度 README、根 README、TIMELINE §3 / 年度表；若影响全库读者判断，再同步 SUMMARY §13 合并待补表。
3. `Notification`、`Camera-ready`、`Conference`、`Proceedings online` 不应误写成当前可投窗口；它们可以进入年度表和 Mermaid，但默认不进入 TIMELINE §3，除非备注说明仍需行动。
4. 已结束年度补 proceedings / DBLP 属于历史补证，不得反向改变当年投稿窗口状态，除非官方同时修正了 deadline 事实。

### 12.7 来源等级与访问降级规则

| 等级 | 可写事实 | 使用限制 |
|---|---|---|
| 官方完全核验 | 官方年度主页、CFP / dates、publisher collection、official program / proceedings 明确给出的时间、状态、人员或入口 | 可进入年度 README、根 README、TIMELINE 与 Mermaid |
| 官方入口 + 部分核验 | 官方 URL 可定位，但只给日期、缺时刻、缺 track、页面需交互式展开、或信息不完整 | 可写 `待补时刻` / `部分核验`，必须保留 caveat |
| 动态页面受限 / WAF / 403 / CAPTCHA / Authwall / JS 壳 | 官方 URL 存在但 CLI 受限、需要交互式页面或登录、返回 JS 壳 / WAF / 403 / CAPTCHA / Authwall | 保留官方 URL，写 `未获公开可审计正文`，并**按 §16.6 的四类分别标注具体阻断形式**；不得改写成“无官方信息”，也不得统称 `WAF` |
| DBLP fallback | 年度论文名录、计数、bibliographic cross-check | 不能支撑 CFP、deadline、current roster、author guidelines 或当前 articles in press |
| 第三方线索 | 发现候选 CFP、deadline 或人员线索 | 不得进入官方来源列；只能写备注 / 待补记录，核验后再升级 |

处理要求：

1. official home / CFP / dates 优先；publisher / journal 官方页次之；DBLP 只做论文名录和计数 fallback。
2. researchr dates 页必须逐 track 核验，不得把某 track 的 AoE / UTC offset 套到另一个 track；必要时检查 HTML `title="Timezone: ..."`。
3. 官方只给日期时写 `yyyy-mm-dd 待补时刻`；只给 week / month / quarter 时不能硬落日期，也不能进入 dated Mermaid。
4. ScienceDirect / Elsevier / Wiley / ACM / IEEE 等入口在命令行遇到 WAF/403/CAPTCHA/Authwall 时，保留官方链接与风险说明；不要用第三方页面补成完全核验。
5. 如果来源从第三方线索升级为官方核验，必须在证据记录中说明升级路径和核查时间。

### 12.8 近期投稿窗口与 SUMMARY 的分工

1. [TIMELINE.md](./TIMELINE.md) §3“近期投稿窗口速览”是近期可行动窗口的行级承载表；它是年度全量表的筛选视图，不是独立事实源。
2. 新增、删除或修改 §3 行时，必须同步对应年度事件表；若事件进入 Mermaid，也必须同步对应年度 Mermaid。
3. [SUMMARY.md](./SUMMARY.md) 不再维护近期窗口流程入口；只在 Venue 总表 / §13 合并待补表中保留会影响读者判断的聚合状态、降级原因和升级条件。不得复制 TIMELINE §3 的全量窗口行。
4. 年度 README 与 venue 根 README 保存单 venue 事实链；GUIDE 只定义流程与字段，不承载事实。
5. 若 SUMMARY、TIMELINE §3、年度表之间出现不一致，以年度 README + 官方来源为回溯起点；先修正年度 README / TIMELINE 行级事实，再同步 SUMMARY 的总表短摘要或 §13 合并待补表。

### 12.9 P0/P1/P2 与统计不回退规则

1. 当前组合统计为 **42 个 venue 根 README、295 个年度 README**（`2026-08-07` 因新增 [ICSE 2029 年度页](./conf-a-icse/2029/README.md) 由 294 增至 295，venue 数不变）；P0 冻结基线为 22 个 venue 根 README、154 个年度 README；PR-10 后、PR #63 前的 39/273 只能作为历史状态。常态化更新不得把正文当前状态回退到历史中间统计。
2. 历史更新日志中的 26 / 182、30 / 210、34 / 238 等旧统计是当时真实记录，不得为了 `rg` 零命中而删除或篡改。
3. P2 venue 可以出现在近期窗口和历史事件表中，但必须保留 `P2 / 不升级` 或等价说明；不得在 README、SUMMARY、PR body 或投稿建议中改写成 P0/P1 主投目标。
4. 常态化刷新若发现 CCF 官方更名、venue 分裂 / 合并或确有强相关漏项，不能直接新增目录；先更新 [01-venue-scope.md](./01-venue-scope.md) 与 PR body，再进入新增 venue 流程。

### 12.10 本地自查与 dry-run 验收

常态化更新完成后至少运行：

```bash
git status --short
rg -n "常态化|滚动刷新|投稿窗口|近期窗口|刷新" ccf_venues/README.md ccf_venues/GUIDE.md ccf_venues/SUMMARY.md
rg -n "42.*venue|29[45].*年度|P2|PR #63" ccf_venues/README.md ccf_venues/SUMMARY.md ccf_venues/01-venue-scope.md   # 2026-08-07 起当前口径为 295 个年度 README，历史日志中的 294 需保留
rg -n '^(<<<<<<<|=======|>>>>>>>)' ccf_venues || true
```

若本轮修改了 TIMELINE 或年度 README，还必须本地检查：

1. 年度 README、venue 根 README、TIMELINE 年度表、TIMELINE §3、Mermaid、SUMMARY Venue 总表 / §13 合并待补表是否都已同步。
2. TIMELINE 年度表按事件发生日期升序；Mermaid label 使用 venue edition 年份；Mermaid 不包含 URL。
3. `待补时刻`、AoE、UTC offset、local time、WAF/403/CAPTCHA/Authwall、P2 / 不升级等 caveat 没有在同步过程中丢失。
4. 新增内部 Markdown 链接均使用相对路径，且不是模板位置下的伪链接。
5. 修改过的文件都有更新日志，且更新日志按时间降序。

PR 实现后 reviewer 必须亲自验证本节是否可用，而不是只读文字：

1. 至少抽样 1--3 个真实 venue / 近期窗口 / 待补项做 dry-run；codex reviewer 至少给出 1 个真实 venue dry-run 证据。
2. dry-run 应说明选择的 venue、官方来源、按本节判断应修改哪些文件、是否涉及 TIMELINE §3 / 年度表 / Mermaid / SUMMARY、以及为何本次实际修改或只读验证。
3. 若 dry-run 无法判断更新范围、同步文件、证据等级、状态迁移、P2 边界或 WAF/403/CAPTCHA/Authwall 降级方式，则至少列为 I 级，必须先修本 GUIDE 再声称 ready。

## 13. 初始化 PR 自审流程

当任务是“先开初始化 PR，不填实际 venue 数据”时，必须按以下顺序自审：

1. 确认 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[TIMELINE.md](./TIMELINE.md)、[01-venue-scope.md](./01-venue-scope.md) 和 [templates/](./templates/) 均已存在。
2. 确认 PR body 是可执行计划，包含目标、骨架交付物、P0/P1/P2 分批、TIMELINE 同步规则、验收标准、已知限制和下一步停靠点。
3. 确认 `SUMMARY.md` 不声称任何未建 venue 已完成。
4. 确认模板中的相对链接在未来实际 venue 路径下可成立。
5. 确认 Mermaid 代码块使用 GitHub 较稳定的 `gantt` 语法，不使用实验性 `timeline` 作为主图。
6. 完成自审后停止，等待用户确认是否进入 P0 数据填充。

## 14. 一轮数据填充流程

1. 先读 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
2. 根据 [01-venue-scope.md](./01-venue-scope.md) 选择本轮 venue。
3. 新建或更新 `<conf|journal>-<rank>-<slug>/README.md`。
4. 从最新年份开始，按降序补年度 README，默认覆盖到 `2022`。
5. 若目标是会议 venue，补根 README 的核心人员情报；至少覆盖当前 / 未来年度组织与审稿 leadership、Steering / Advisory 层级、强相关 track chair 和领域权威；umbrella venue 必须写清层级。
6. 若目标是期刊 venue，补根 README 的核心编辑人员情报；若暂不能核验，写明缺口、检索入口和核查时间。年度页只在 special issue guest editor、年度 editorial team 或人员变更与当年事实直接相关时单独记录。
7. 回填上级 venue README 的年度汇总表。
8. 若更新内容涉及投稿相关 important date，同步回填 [TIMELINE.md](./TIMELINE.md) 的年度表格与 Mermaid Gantt；事件行必须包含事件官方来源、年度主页、本库年度页，已结束年度还应尽量包含论文集 / 论文名录链接。
9. 回填 [SUMMARY.md](./SUMMARY.md) 的 Venue 总表短摘要和 §13 合并待补表；踩坑记录写入本 GUIDE 或相关 README，不写入 SUMMARY 正文。
10. 若本轮 review / 自查发现新的 C/I 级问题，或发现会反复影响后续填充的 M 级共性坑，必须把修复后的规则回写到本 [GUIDE.md](./GUIDE.md) 或相关 README 的证据记录；SUMMARY 正文不再设置“踩坑”小节，不能只在 PR comment 中解决一次。
11. 检查所有链接可点击、投稿 / 事件时间精确到分钟、信息更新时间 / 更新日志默认精确到秒、所有状态符合口径，且 Mermaid 语法可预览。
12. 在相关 README 文末更新日志中按时间降序插入记录。

### 14.1 P1/P2 stacked PR 执行纪律

PR-5 已将 P1/P2 扩展冻结为 PR-6~PR-10 的 stacked execution contract；后续 AI 不得只凭 [01-venue-scope.md](./01-venue-scope.md) 的范围清单自由拆分。执行合同、允许修改范围与依赖关系以本节和 [01-venue-scope.md](./01-venue-scope.md) 为准，不再指向 SUMMARY。

| 子级 PR | 主题 | Venue ownership | 默认产物 | 共享文件纪律 |
|---|---|---|---|---|
| PR-6 | P1-Maintenance / Repair | `conf-b-saner`、`conf-b-icsme`、`conf-b-icpc`、`journal-b-jsep` | 4 个 venue + 28 个年度 README；已基础建档 | 只增量维护自有 venue 的 SUMMARY / TIMELINE / README / GUIDE / scope 事实 |
| PR-7 | P1-Empirical / Quality | `conf-b-esem`、`journal-b-ese`、`journal-b-jss`、`journal-c-sqj` | 4 个 venue + 28 个年度 README；已基础建档 | 保留 PR-6 与 P0 facts，期刊 rolling 不写成 dated Mermaid |
| PR-8 | P1-Formal / Toolchain | `journal-b-ist`、`journal-b-scp`、`conf-c-qrs`、`conf-c-tase` | 4 个 venue + 28 个年度 README；已基础建档并合入上游 | 已吸收 PR-6 / PR-7 上游 facts；形式化 / 工具链计数不得混用 DBLP fallback；不得覆盖 PR-6 / PR-7 facts |
| PR-9 | P2 Neighboring Observation | `conf-c-apsec`、`conf-c-seke`、`conf-c-ease`、`conf-c-msr`、`conf-c-rv` | 5 个 venue + 35 个年度 README；已基础建档 | 当前合流分支已 merge 最新上游 PR-8 并吸收 PR-6 / PR-7 / PR-8 适用踩坑规则；不升级为 P0/P1 主投目标 |
| PR-10 | P1/P2 Global Audit | 不新增 venue；审计 PR-6~PR-9 | 统计 / 时间线 / Mermaid / 待补项全局收口 | 必须等 PR-6~PR-9 全部合入上游后执行 |

执行要求：

1. 每个子 PR 只能创建 / 修改自己 ownership 内的 venue 目录；共享文件只能做自有事实的增量合流，不得删除 P0、会议试点、期刊试点或其他子 PR 已核验事实。
2. 默认年度范围仍为 `2022` 至当前年份 + 2；发现更远未来官方 CFP / important dates 时继续纳入，并在 PR body 与更新日志说明。
3. 不得静默新增合同外 venue。确需新增时，先更新 [01-venue-scope.md](./01-venue-scope.md) 与 PR body，并给出 CCF 官方或 venue 官方来源。
4. final ready 前必须 merge upstream staging head；若有 conflict，冲突解决后必须复核 `git ls-files -u` 为空、冲突标记消失、双方 TIMELINE / Mermaid / rolling 表 / 更新日志 facts 均保留。
5. PR-8 的并行开工修订属于执行合同修订：可调整 PR-8 前置条件，但不得删除 P0、PR-6、PR-7、PR-9 的 venue facts、TIMELINE facts、rolling 表或更新日志。
6. PR-6 / PR-7 / PR-8 同时 open draft 时，共享文件中的 “当前总量” 必须标清 branch-local 或组合统计口径；若当前分支不是第一个合入的 sibling，final ready 前必须 merge 最新 upstream 并重算组合统计，不能把自身 26 / 182 等旧口径覆盖已合入 facts。
7. 历史更新日志可以保留当时真实的旧统计数字；旧口径扫描应聚焦正文和当前总账，不得为了让 `rg` 零命中而篡改历史日志。

## 15. 会议 / 期刊合流与事实共存规则

本库的会议数据、期刊数据、共享规范和模板会被不同轮次持续维护。任何合流或冲突解决都必须遵守以下长期规则：

1. **共享规范优先**：时间格式、更新日志降序、Markdown 链接占位、核心 URL、核心人员情报和 TIMELINE 事件发生年份规则属于共享规范；任一轮修正后，后续维护应吸收协议层规则。
2. **事实类型分离**：会议事实、会议年度 README、会议核心人员和会议 dated events，与期刊事实、期刊年度 README、期刊核心编辑人员、期刊 rolling 表和期刊 special issue dated events 分开维护。
3. **SUMMARY 不回退事实**：已经完成基础核验的会议或期刊不得被后续空白占位写回 `⏳ 待建`；若某轮不处理某类事实，应保留既有状态和链接。
4. **TIMELINE 不互删事件**：会议 dated events、期刊 rolling 表和期刊 special issue dated events 合流后必须共存；冲突解决时以“事件发生年份 + 来源可点击 + 已核验事实不删除”为准。
5. **模板统一协议**：模板文件中的外部 URL 和目录相对路径都使用纯文本占位，避免 link checker 把模板位置下不存在的 `./2028/README.md` / `../TIMELINE.md` 当成坏链；实例化后的正式 README 必须使用真实可点击相对 Markdown 链接。更新日志提示统一为“更新日志按时间降序排列，最新记录置于最上方。”。
6. **试点经验保留边界**：会议试点和期刊试点的可复用踩坑结论应保留在本 GUIDE 或独立规则文档；不得把某一类试点的 deadline、论文数量或人员 roster 复制成另一类事实，也不得回写成 SUMMARY 正文长表。

## 16. 踩坑复盘与规则回写纪律

本库是长期情报库，不是一次性 PR 产物。任何一轮踩坑都必须沉淀为后续 AI 能直接执行的规则，避免同类错误在后续 venue 中重复出现。

### 16.1 必须回写的踩坑类型

1. **来源与计数口径坑**：例如 FSE / ESEC-FSE / PACMSE 命名与计数、ISSTA 与 FSE / ECOOP / SPLASH co-location、ASE 多 track 与 DBLP 全 proceedings fallback、RE 的 IEEE Xplore conference number、REFSQ 的 Springer / CEUR / DBLP 分散入口。
2. **TIMELINE 组织坑**：例如 edition 年份与事件发生年份错位、Mermaid label 使用事件年份导致误读、年度表格已更新但 TIMELINE 未同步、会期事件在根表 / 年度 README 中存在但全局时间线缺失。PR-2 已踩过 ISSTA 2022/2023 年度页有 `Conference dates` 但 TIMELINE 漏写的坑，后续必须把会期同步纳入强制检查。
3. **链接与草稿坑**：例如 `_events_draft.md` 已删除但正式 README 仍链接、模板占位链接被误认为事实链接、官方页面 access denied 但未标明 probe / fallback。
4. **核心人员情报坑**：例如不同 venue 人员表列结构不一致、缺少 `核验状态` / `核查时间`、只写聚合 Steering Committee 而没有可追踪具体人员、研究方向或代表作没有主页 / DBLP / 学术入口支撑。
5. **未来年度信息坑**：例如只查到当前年而未查当前年份 + 2，或未来年度已有官方主页 / CFP 却未入年度 README；反过来也不得为未公布年度虚构 deadline。
6. **合流与共享文件坑**：例如后续 PR 修改 [TIMELINE.md](./TIMELINE.md) 时误删期刊 rolling 表、SoSyM special issue dated event、Requirements Engineering 2026 collection dated events、已核验会议事件，或把上游试点 venue 写回待建。
7. **访问异常与来源冒充坑**：证书问题可以用 `curl -k`、带 `User-Agent` 或公开归档重试；但 `404`、Access denied、空页、WAF 返回页、未公布占位、只有 series 入口、投稿系统入口或 organizer call 都不得写成年度主页 / CFP / committee 官方角色源；Wiley STVR 等 publisher 页面在 CLI 中 WAF/403 时仍应保留官方链接和未获公开可审计正文状态，不能把“无法命令行抓取”改写成“无编辑人员”或用第三方页面补成当前 roster。
8. **track 与角色混算坑**：research、industry、tool、artifact、workshop、journal-first、companion、umbrella conference 与 satellite conference 必须分列；committee / editorial roster 角色不足时只能写成线索，不能升级为已核验核心人员事实。
9. **期刊专刊 / 会议扩展混算坑**：例如 STTT 的 conference-based special issue 只能按期刊 article baseline 记录，不能和 TACAS / SPIN / FMICS / RV 等会议 proceedings 合并计数。
10. **维护 / 演化 venue 历史入口坑**：SANER / ICSME / ICPC 等维护、演化、程序理解会议的旧年度站点、CFP、submission system、program、proceedings、DBLP slug 经常分散；找不到官方 CFP 时只能写 `待补` 或 `第三方线索`，不能把第三方 deadline 写成官方事实。
11. **冲突日期同步坑**：若 ICSME 2022 这类年度出现 IEEE CFP、archive 首页、proceedings 封面会期不一致，根 README、年度 README、[TIMELINE.md](./TIMELINE.md) 与待补表必须同步标 `日期冲突待核`，不能只在单个文件说明。
12. **证书风险入口坑**：若官方旧站 HTTPS 证书主机名不匹配但 HTTP 可访问，例如 SANER 2022，应优先使用可访问的 HTTP 官方站入口，并在备注中显式写明 HTTPS 证书风险；不要留下会让读者点击失败的裸 HTTPS 链接。
13. **Wiley current issue / Early View 混写坑**：Wiley `currentissue` 只可写作 current issue candidate，不能冒充 Early View / articles in press；若 Early View 入口未定位，应单独写 `Early View / articles in press 入口待定位`。JSEP 本轮已按此规则将 2026+ rolling 状态降级为 `🟡 rolling 候选 / 已检索未获可审计证据`；STVR 等既有 Wiley WAF/403 历史条目在后续触碰或专项复核时也应吸收该口径。不得在 author guidelines / ScholarOne 路由未公开可审计确认前，把新建或本轮修改的 Wiley WAF 条目写成 `🟢 滚动开放`。
14. **未来年度维护会议预造坑**：SANER / ICSME / ICPC 的 2027/2028/2029+ 若只找到 series page、announcement、townhall、program 预告或无 official research track dates，应写 `⏳ 已检索未公布`，不得预造 official CFP、submission deadline、DBLP 年度页或 proceedings。
15. **P1/P2 sibling 合流统计坑**：PR-6、PR-7、PR-8 单独或两两合流时会产生 26/182 或 30/210 的中间口径；PR-6 / PR-7 / PR-8 三者合流后必须重算为 34 个 venue / 238 个年度 README（22 会议 / 12 期刊）；PR-9 合流后必须重算为 39 个 venue / 273 个年度 README（27 会议 / 12 期刊）；PR #63 合流后必须重算为 42 个 venue / 294 个年度 README（29 会议 / 13 期刊），并同时保留 P0 22/154 冻结基线、各 sibling 已建档事实和 PR-10 全局审计依赖。
16. **PR-7 实证 / 质量 venue 坑**：Springer Closed collection 仍可能有 historical deadline，必须写成历史 dated event 而不是当前征稿；ESE collection 多事件类型要保留 submission / notification / revision / final decision 的原始语义；ScienceDirect CLI `403` / WAF 只能标注未获公开可审计正文，不能替代或删除官方 Elsevier 链接；ESEM historical submission system 要区分“当年官方使用过”和“当前是否还能访问正文 / 表单”。
17. **Elsevier / ScienceDirect candidate CFP 坑**：命令行只能打开入口或遇到 WAF/403 时，candidate special issue、editorial roster 和 issue 正文只能写作未获公开可审计正文；不能为了填满 TIMELINE 而把未核验 deadline 变成 dated event。
18. **投稿系统 code 臆造坑**：Editorial Manager / ScholarOne / Equinocs / publisher dashboard 的路径 code 不一定等于 venue slug；必须由官方跳转或可访问入口支撑，不能按缩写猜 URL。
19. **QRS / TASE 计数多源坑**：techconf stats、official accepted list、Springer TOC、DBLP 和 publisher proceedings 入口都可能不是同一口径；必须并列保留，不得写成单一“论文数量”。
20. **PR-10 全局审计降级核验坑**：若 subagent 服务出现 503 / 429，不能把“agent 未返回”当作可遗留待核验项；主 session 必须用本地脚本、官方页面、带 User-Agent 的 `requests` / `curl`、`claude -p` / `codex-deepseek exec` 等替代路径完成核验，并在 SUMMARY / PR body 说明降级方式。
21. **researchr 日期行时区坑**：researchr dates 页同一 venue 不同 track 可能混用 `AoE (UTC-12h)`、`AoE (Anywhere on Earth)`、`UTC+8h`、本地时区或无具体时刻；**必须逐 track 读原始 HTML 的 `title="Timezone: …"` 属性**，不能把某个 track 的时区套到 main / technical / research chain，也不能凭纯文本提取断言「页面无时区声明」（见 §16.6.5 第 3 条）。⚠️ **2026-08-07 更正范例**：本条初稿曾以「APSEC 2026 Technical Track 是 `UTC+8 (Bali time)`，不是 AoE」作为 worked example —— **该范例事实错误**。实测 `dates/apsec-2026` 的 Technical Track **全 8 行 tooltip 均为 `AoE (Anywhere on Earth)`**，CFP 小标题亦为 `Key Dates (AoE)`；`UTC+8h` 只属于 Local Student Forum 与 Doctoral Symposium 两个旁支 track。正确的 worked example 应是：**同一张 dates 页上，APSEC 2026 的 Technical Track 为 `AoE`、Local Student Forum / Doctoral Symposium 为 `UTC+8h`** —— 这正说明为什么必须逐 track 核对，而不是读一行推全表。

### 16.2 回写位置

1. 能形成长期操作规则的，优先写入本 [GUIDE.md](./GUIDE.md) 对应章节；若找不到合适章节，写入本节。
2. 只属于某一批 venue 的事实性经验，写入相关 venue 根 README 的维护备注 / 证据与核查记录；若会影响全库读者判断，只在 [SUMMARY.md](./SUMMARY.md) §13 合并待补表中保留一行聚合状态。
3. 单个年度或单个字段的 unresolved fact，写入对应年度 README 的“证据与核查记录”；只有跨 venue 或影响总表判断的缺口才进入 [SUMMARY.md](./SUMMARY.md) §13 合并待补表，不要扩大成全库规则。
4. PR comment 中提出的 C/I 级问题若已经修复，必须在最终 PR 汇总或 PR body 中说明“修复点 -> 本库规则 / 文档落点”，便于后续 reviewer 追踪。
5. 若时间不足，至少在本轮更新日志中明确“哪些坑尚未完全规则化”，不得只把坑留在 PR comment 或口头总结里。

### 16.3 PR 结束前强制自查

每轮数据填充 PR 在声称 ready 前至少执行以下检查：

1. `rg -n "_events_draft|主 session 合流|候选事件见" ccf_venues/<本轮 venue>` 应无正式文档残留；历史更新日志除外。旧统计口径扫描同理：只清理当前正文和总账，历史更新日志可保留当时真实状态。
2. 本轮新增 / 修改的 venue 根 README 与年度 README 不应存在指向不存在本库文件的相对链接；模板目录的占位链接单独按模板规则解释。
3. [TIMELINE.md](./TIMELINE.md) 年份章节按降序，节内事件按日期升序；Mermaid 不含 URL / Markdown 链接。
4. Mermaid label 的 venue edition 必须与表格 Venue 一致，尤其检查 `ICSE`、`FSE`、`ETAPS/TACAS` 等前一年投稿的会议。
5. 对本轮新增 / 修改的会议年度 README，逐一抽查 `Conference dates`：若不是 `未公布` / `⏳ 已检索未公布`，则 [TIMELINE.md](./TIMELINE.md) 必须同时存在对应表格行和 Mermaid `Conference` 行；不要出现 ISSTA 2022/2023 这类年度页有会期但全局时间线缺会期的断链。
6. 本轮新增的会议根 README 人员表必须包含 `官方角色来源`、`主页 / 学术入口`、`代表作 / 近 5 年论文入口`、`核验状态`、`核查时间`；期刊人员表必须保留 `核验等级 / 当前性`。
7. 本轮新增的期刊若存在 `rolling submission`，则 [TIMELINE.md](./TIMELINE.md) 的“期刊滚动投稿 / 未定日期”表必须有对应行；若存在 dated collection / special issue deadline，年度事件表和 Mermaid 必须同步；若无 dated CFP，必须显式写“无已知 active dated CFP”。
8. [SUMMARY.md](./SUMMARY.md) 的总览统计、Venue 总表、§13 合并待补表与实际目录一致；更新日志仍按时间降序。
9. 若复审暴露新的共性坑，先补 [GUIDE.md](./GUIDE.md) 或相关 README 证据记录；若影响全库读者判断，再同步 [SUMMARY.md](./SUMMARY.md) §13 合并待补表。不得把“下次注意”只留在聊天记录或 PR comment 中。
10. 若当前 PR 合入上游或 base 分支并出现冲突，必须把冲突处理纳入后续复审项：确认上游新增 venue、当前 PR venue、期刊 rolling / dated events、共享规则和更新日志均未被覆盖或回退；同时用 `git status --short` 和 `git ls-files -u` 确认冲突已被 `git add` 标记 resolved，不能只看文本里没有冲突标记。
11. 全局审计 PR 声称 ready 前，必须把“需要核实的信息”和“需要纠正的问题”清零到可验收状态：事实错误必须修正；无法命令行穿透的官方 WAF / 403 必须明确写成 access caveat，并不得把它升级成已完全核验事实；subagent 失败必须有替代核验记录。

### 16.4 PR-9 P2 邻近观察补充规则

1. P2 venue 只服务检索扩展、投稿分流和社区画像，不得在 README / SUMMARY / PR body 中升级为 P0/P1 主投目标。
2. 对 APSEC / EASE / MSR 这类 researchr venue，`dates` 页常混入多个 track；TIMELINE 默认只同步 main / technical / research chain 与 conference dates，SEIP / ERA / data-tool / challenge / industry 等 track 必须在年度 README 中分列，不能混算。
3. 对 SEKE 这类旧站，若 program 页存在旧内容残留、proceedings archive 与 CFP 会期冲突，只能写成需公开可审计证据确认；不得用旧页闭合 2026+ 事实。
4. 对 RV 这类 Springer / DBLP 入口，年度官网、CFP、program、Springer proceedings 与 DBLP fallback 必须分列；某年度未列 General Chair 时不得臆造，只记录 Program Chair / Steering 等官方角色。
5. 若 RV 等 P2 venue 的官方日期只给 week / month / quarter（例如 RV 2022 Notification 仅给 `Week 26`），只能写入年度 README、根 README 或待补记录，不得硬落某一天并进入 dated TIMELINE / Mermaid。
6. 2027/2028 若只找到 stable series 或 future event 线索，不能当成年度主页 / CFP；只能在年度 README 写 `⏳ 已检索未公布`，不进入 dated Mermaid。


### 16.5 PR #63 LLM4Modeling-SE 扩展规则

1. PR #63 新增 `journal-b-ase`、`conf-b-caise`、`conf-c-iceccs` 后，组合统计重算为 42 个 venue / 294 个年度 README（29 个会议 / 13 个期刊）；`2026-08-07` 新增 ICSE 2029 年度页后为 42 个 venue / **295** 个年度 README；历史 39/273 只能作为 PR-10 后、PR #63 前状态。
2. ASE Journal 与 ASE Conference 同缩写但不同 venue；任何投稿决策表、SUMMARY、TIMELINE label 都必须写清 Journal / Conference。
3. CAiSE 只在需求、概念建模、MDE、信息系统 / 过程 / 企业建模语境下适投；不得将泛 LLM4SE 工具评测硬写为 CAiSE 主场。
4. ICECCS 只作为 🥉 档复杂系统工程 / formal engineering / V&V 工程案例来源；不得把全部 complex systems 论文自动标为 LLM 状态机建模强相关。
5. 若 CAiSE 2024 或 ICECCS 2024 只找到 DBLP / proceedings / 第三方 deadline，不得补写 abstract / submission / notification 等 official dates；会期可以由 proceedings record 支撑，但必须标明来源降级。
6. Springer collections 进入 TIMELINE 前必须记录 collection 语义、状态、deadline 与本仓库相关性；弱相关 open collection 可留作观察线索，不必进入近期投稿重点，但不能把它写成已同步事实。

### 16.6 访问失败分类、入口语义与 slug 漂移（2026-08-07 全量刷新后固化）

本节把 `2026-08-07` 全库刷新中暴露的检索与取证踩坑固化为硬规则。这些问题不是个别疏漏，而是**会系统性造成假阴性 / 假阳性**的检索策略缺陷。

#### 16.6.1 访问失败必须分四类记录，不得统称 `WAF`

| 站点族 | 精确表现 | 记录写法 | 可用 fallback |
|---|---|---|---|
| Springer（`link.springer.com`） | WebFetch → `idp.springer.com/authorize` **303 authwall**，回跳带 `?error=cookies_not_supported`；`curl` → **HTTP 200 但 body 恒为约 3038 字节的 F5 `<title>Client Challenge</title>` JS 壳** | `authwall（idp 303）+ JS 壳（Client Challenge）` | **`rd.springer.com` 同路径可直出完整官方 HTML**（Springer 同源镜像域，页脚 `© 2026 Springer Nature`）。这是本库当前唯一可靠的 Springer 正文通道，取得的内容按「官方正文」计。**披露要求（硬性）**：凡仅通过 `rd.` 域取得的事实，必须在该事实所在单元格逐条注明取证域，范例见 [journal-b-ase/2026/README.md](./journal-b-ase/2026/README.md) 的 Green / Genetic Improvement 两行；只在方法论章节声明而不在事实处落实，等于没有披露 |
| ScienceDirect / Elsevier | 直连 **HTTP 403**；经第三方渲染代理 **`r.jina.ai`** → **Elsevier CAPTCHA**（`Are you a robot?` + Reference number + UTC 时间戳） | `直连 403 / 代理 CAPTCHA（含 Reference number）` | 无等价通道；`editorialmanager.com` 可核验 rolling 投稿入口，DBLP 可作计数 fallback |
| ACM DL（`dl.acm.org`） | 直连 **403**；代理 → `Performing security verification` bot 页；**连静态 CFP PDF 资源也 403** | `直连 403 / 代理 bot 验证页` | 无；DBLP 作计数 fallback |
| Wiley（`onlinelibrary.wiley.com`） | Cloudflare **`Just a moment...` 403**；special issues 页经 WebFetch 返回 **HTTP 402 Payment Required** | `Cloudflare WAF/403`（402 需单列） | 无；DBLP 作计数 fallback |
| CCF 官网（`www.ccf.org.cn`） | `curl`（含浏览器 UA / Referer）→ **HTTP 200 + 约 15999 字节阿里云 WAF CAPTCHA 挑战页**（`aliyun_waf_aa`、`aliyunCaptcha-sliding-slider`）；PDF 下载 URL 亦被替换为挑战页 | `阿里云 WAF CAPTCHA（HTTP 200 伪装）` | **WebFetch 通道可穿透** |

**通用铁律**：`HTTP 200` 不等于取到正文。凡上述站点族，必须检查 body 内容与长度，否则会把挑战页当成「页面不存在 / collection 已关闭」。

**渲染代理具名要求（硬性）**：本库涉及的第三方渲染代理为 **`r.jina.ai`**（用法 `https://r.jina.ai/<目标URL>`）。它**不是我方直连**，属 [CLAUDE.md](../CLAUDE.md) §2 口径下的中间层，必须具名而非笼统称「渲染代理」。判定规则：

1. 经 `r.jina.ai` 访问 **`rd.springer.com`** 等**官方域**并取得该域自有 DOM（可用 `URL Source` 与 Springer 自有 class 如 `app-collection-page-sidebar__text-bold`、`id="submission-status"` 交叉印证）时，事实按「官方正文（经代理取得）」计，但**必须在事实所在单元格逐条注明取证域与路径**。
2. 经 `r.jina.ai` 取得的**非官方域**内容，一律只作发现线索，不得升级为官方事实。
3. 代理返回 CAPTCHA / bot 验证页时，按「官方入口已定位，正文未取得可审计快照」记录，**不得**据此断言目标不存在或已关闭。
4. 只在本方法论章节声明披露规则、而不在具体事实处落实，**等于没有披露**；reviewer 应按此判定。

#### 16.6.2 `Access denied` ≠ `404`：researchr 入口的三种语义

| 返回 | 语义 | 记录写法 | **阶段状态（接入 §10 词表与 §12.6 迁移链）** | 复查优先级 |
|---|---|---|---|---|
| HTTP 200 + `Access denied`（`You do not have the privileges to access this part.`） | 页面槽位**已建立但未公开发布**，通常意味着主办方已确定并在筹备 | 「官方入口已定位，正文未取得可审计快照（未发布 / 需登录）」，并注明这是**即将发布的弱正向信号** | **`⏳ 待官网（槽位已建未发布）`** —— 这是 §12.6 迁移链中 `⏳ 已检索未公布` 与 `🟦 已有主页` **之间的中间态**，不得直接写成 `🟦 已有主页`（正文未取得，不满足「已有主页」的证据要求），也不得写成裸的 `⏳ 已检索未公布`（会丢失筹备信号）。若同时另有**其他官方来源**已给出该年度的地点 / 月份等实质事实（如 ICSE 2028 由 icse-conferences.org 公布 `Apr 2028 / Hawaii`），则以那条实质事实定档为 `🟦 已有预告`，并在证据记录中同时注明 researchr 为 Access denied | **高频复查** |
| HTTP 404 | 尚未建站 | `⏳ 已检索未公布` | `⏳ 已检索未公布` | 常规 |
| HTTP 200 + 空 dates 表（表头在、无数据行） | 页面已建、chair 尚未填 | `🟦 已有主页 / CFP 待发布` | `🟦 已有主页` | 高频复查 |

**§12.6 迁移链据此扩展为**：

```text
⏳ 已检索未公布 -> ⏳ 待官网（槽位已建未发布） -> 🟦 已有主页 / 🟦 已有预告 -> 🟢 投稿中 -> ...
```

**四个实例的正确编码（2026-08-07 统一）**：`RE 2027` 与 `ICSME 2027` = **`⏳ 待官网（槽位已建未发布）`**（规范 token，见 §10.1；researchr 是唯一来源）；`FM 2027` = `🟦 主办征集中`（researchr Access denied，但 FME 另有官方 organizer call 这一实质事实，故用该会议族专有态）；`ICSE 2028` = `🟦 已有预告`（researchr Access denied，但 ICSE 指导委员会官方站已公布 `Apr 2028 / Hawaii, USA`）。**关键判别：Access denied 本身只决定「不低于 `⏳ 待官网`」，最终档位由是否另有官方实质事实决定。**

`2026-08-07` 实例：RE 2027、ICSME 2027、FM 2027、ICSE 2028 均为 `Access denied`（此前本库统一记作 404 或「已检索未公布」，丢失了信号）；RE 2028、ICSME 2028、ASE 2027 为真 404；EASE 2027 为空 dates 表。

另有两类非 researchr 的陷阱：

1. **UA 型 bot 过滤**：`cyprusconferences.org`（ISSRE 2026）对默认 `curl` UA 返回 **404**，对浏览器 UA 返回 **200**。裸 curl 复查会误判「官网已下线」。
2. **通配符域假阳性**：`2027.models-conf.com` 返回 HTTP 200，但与 `www.models-conf.com` 内容**字节级相同**且 `<title>` 为空。HTTP 200 **不构成**该年度已发布的证据。

#### 16.6.3 slug 与 series 入口不得假定稳定

`2026-08-07` 的四例漏检全部源于此：

1. **series 根页退化**：`conferences.i-cav.org/` 现只返回占位文本 `This is a repo`，无法用于发现未来 edition —— 必须直接 probe `https://conferences.i-cav.org/<year>/`。这是 CAV 2027 被漏掉的直接原因。
2. **大小写 slug**：researchr 上 VMCAI 使用**大写** `VMCAI-2027`（RE 亦为 `RE-2027`）；只探测小写会漏。
3. **track slug 变更**：ICPC 2027 的 Research Track slug 由历史 `icpc-YYYY-research` 改为 `icpc-2027-research-track`，旧模式 404。
4. **合办改名**：ATVA 与 APLAS 合办后官方页托管在 `conf.researchr.org/aplas-atva-2026`，按 `atva-YYYY` 探测必然 404；且 `atva-conference.org` series 站长期停更在 2025。

**规则**：任何 venue 的年度巡检至少尝试 ① 大小写两种 slug、② 已知合办组合 slug、③ 直接按年份 probe 独立域名路径；并且**不得**把 series 页 / 长期主页作为「是否公布」的唯一判据（`program-comprehension.org` 停在 ICPC 2025、`icse-conferences.org` 才是 ICSE 2028/2029 的真源而 researchr series 只到 2027，均为反例）。

#### 16.6.4 伞会议必须按子会议展开维护

CCF 目录以单一 `ETAPS` 伞条目收录（第七版全 72 页 PDF 中无 TACAS / FASE / iFS 字样），但**实际投稿单位是具体子会议，其 scope 差异极大**。本库此前 `conf-b-etaps` 只跟踪 TACAS（P3 视角的决定），导致 FASE→iFS 的合并与 iFS 2027 首届窗口被完整漏掉。

**规则**：伞会议目录必须在年度页逐子会议维护本库跟踪范围，并在 [01-venue-scope.md](./01-venue-scope.md) 写明跟踪哪些主会、为什么；同一目录内扩展跟踪范围**不算新增 venue**，但仍须在 scope 文档与 PR body 中显式记录。会议合并 / 更名会让基于旧名的监控同时失效（搜 FASE 找不到、搜 iFS 不知道要搜），因此伞会议的年度巡检必须以 **umbrella 官方 CFP 页**（如 `etaps.org/<year>/cfp/`）为入口，而非按子会议名逐个搜。

#### 16.6.5 HTML 注释与删除线不得当作正文

1. **HTML 注释残留**：ICECCS 2026 官网的 `<!-- -->` 中藏有「location has been changed to Nansha, Guangzhou」「注册费表」等内容，而**可见正文**的 `Host City and Venue` 为 `TBA`、页头仍写 Brisbane。TASE 2026 主页的「IEEE Computer Society Press」出版方说法同样位于注释内（可见正文为 Springer LNCS）。**抓取前必须先剥离 HTML 注释**，否则会把注释内容写成事实。
2. **删除线表示的 extended 日期**：TASE / RV / SPIN / ICECCS / ISSRE 等站用 `<s>` 或 `text-decoration: line-through` 表示旧日期，纯文本提取会把新旧日期并排输出，**极易误读**。必须回原始 HTML 判定删除线归属。
3. **时区藏在属性里**：researchr 的时区信息位于 HTML `title="Timezone: AoE (UTC-12h)"` 属性中，**纯文本提取会完全丢失**；核验 AoE 必须查原始 HTML。⚠️ **2026-08-07 更正**：本节初稿曾写「`/dates/<venue>-<year>` 页普遍不带时区声明，AoE 只在各 track 页侧栏，引 dates 页即为证据链断裂」——**该判断不成立**，是把「纯文本提取丢失了属性」误读成「页面没有声明」。实测 `dates/issta-2027`(7 行) / `VMCAI-2027`(3) / `fse-2027`(8) / `icpc-2027`(16) / `apsec-2026`(24) / `saner-2027`(46) / `msr-2027`(15) **每一个日期行都带 `title="Timezone: …"`**。正确规则是：**dates 页与 track 页侧栏均为有效时区来源，但两者都必须读原始 HTML**；且同一 dates 页上不同 track 的 tooltip 可能不同（APSEC 2026 即同页并存 `AoE (Anywhere on Earth)`、`AoE (UTC-12h)` 与 `UTC+8h`），**必须逐 track 核对，不得把某 track 的时区套到另一 track**。
4. **frameset**：`ksiresearch.org/seke/sekeNN.html` 是 FRAMESET，须改抓 `sekeNNmain.html` / `sekeNNleft.html`，并带 `--compressed`（否则得 gzip 乱码）；SEKE 的官方 program 入口是 **`.txt` 而非 `.html`**。

#### 16.6.6 空白位翻新与已有事实维护同等重要

本轮五条主轨窗口漏检（CAV 2027 / ISSTA 2027 / VMCAI 2027 / iFS 2027 / ICPC 2027）有共同特征：**都是上一轮判定为「未公布」后就停止主动复查的 venue**。本库既有复查策略偏向「已有事实的维护」，对「空白位的翻新」覆盖不足。

**规则**：常态化刷新的 watchlist 必须显式包含「上一轮记为 `⏳ 已检索未公布` / `🟦 已有主页` 且属 P0/P1 的 venue-year」，其优先级不低于已有 deadline 的复核。漏掉一个 40 天窗口的代价远大于重复核验一个已知 deadline。

## 17. 外部索引与分区制度化规则

外部索引与分区信息用于快速查阅 venue 的 WoS / JCR / CAS / EI 状态，但不得替代 CCF 分类，也不得替代官方 venue / 投稿事实。本节是后续维护的硬规则。

### 17.1 来源优先级

1. **CCF**：以 CCF 官方目录、官方更新 / 更名通知为主证据；镜像仅作差集筛查线索。
2. **WoS / SCI 相关**：以 Clarivate MJL、Web of Science Core Collection、CPCI 官方入口为主证据；期刊优先用 ISSN / eISSN 精确检索，会议只可记录 CPCI-S / CPCI-SSH proceedings 证据，不得写成 JCR 期刊。
3. **JCR Quartile**：以 Clarivate JCR 为主证据；必须记录 release year、metric/data year、category、rank、quartile、percentile、evidence URL 与 access note。多 category 必须逐条记录，SUMMARY 的 emoji 列只写派生 best quartile。
4. **CAS / 中科院分区**：只记录中国科学院文献情报中心官方 / 历史版可追溯分区；必须记录版本年份、学科分类、来源 URL 与 access note。2026-03-27 之后应按历史版 / 停更口径处理，不写成实时官方分区。
5. **EI / Compendex**：以 Elsevier / Engineering Village 官方 Compendex source list snapshot 为主证据；必须记录 source title、source type 原值、sheet、snapshot date、download/query date、publisher、ISSN/eISSN/ISBN、coverage / final coverage。

### 17.2 emoji 列口径

正式总表中的 emoji 列只写一个真实 emoji，不写“emoji + 中文”。本库凡字段名或语义明确承载 CCF 等级（包括正式 `CCF` 列、venue 根 README 的 `CCF 等级` 元信息行、TIMELINE 的 `类型-CCF` / `会议-*` / `期刊专刊-*` 组合标签、模板占位）均统一使用 `🏆 / 🥈 / 🥉 / ⚪ / ❓`，不得写回旧式字母等级文本或单色编码。证据链接、官方目录说明、镜像 caveat 放入 `CCF 大类`、§1.1 `CCF` 行或备注列，不塞进等级单元格。

| 维度 | 允许 emoji | 说明 |
|---|---|---|
| CCF | 🏆 / 🥈 / 🥉 / ⚪ / ❓ | CCF 三档等级 / 未列入 / 待核验 |
| WoS / CPCI | 🟢 / 🟡 / 🟠 / ⚪ / ⏳ / 🔴 / ❓ | 期刊集合 / 部分核验 / 会议卷 / 不适用或未查到 / 已检索未获可审计证据 / 已检索未获证据 / 待启动 |
| JCR | 1️⃣ / 2️⃣ / 3️⃣ / 4️⃣ / ⚪ / ⏳ / 🔴 / ❓ | JCR Q1/Q2/Q3/Q4 / 不适用或无 JCR / 已检索未获可审计证据 / 已检索未获证据 / 待启动 |
| CAS | 1️⃣ / 2️⃣ / 3️⃣ / 4️⃣ / ⚪ / ⏳ / 🔴 / ❓ | CAS 1区/2区/3区/4区 / 不适用或未查到 / 已检索未获可审计证据 / 已检索未获证据 / 待启动 |
| EI / Compendex | 🟢 / 🟡 / 🟠 / ⚪ / ⏳ / 🔴 / ❓ | source 级 / book-series 或部分核验 / proceedings 级 / 未查到或不适用 / 已检索未获可审计证据 / 已检索未获证据 / 待启动 |
| 索引核验 | 🟢 / 🟡 / 🔴 / ⏳ / ❓ | 官方证据齐全 / 部分核验 / 未找到 / 已检索未获可审计证据 / 待启动 |

JCR 与 CAS 都使用 `1️⃣` / `2️⃣` / `3️⃣` / `4️⃣`，具体含义由列名和口径表决定。不得在 emoji 列写 `JCR Q1`、`CAS 1区`、`1️⃣ JCR Q1` 或 `1️⃣ CAS 1区`。

venue README 的 `emoji` 列与 `当前结论` 列职责分离：`emoji` 列只写单个编码；`当前结论` 列在占位阶段可写 `待核验`、`不适用`、`待启动` 等短文本，正式核验后替换为可读结论摘要。TIMELINE 的 `索引入口` 列允许在确实无法定位 venue 根 README 时临时写 `待补`；`索引核验` 列仍必须只写单个 emoji。

PR #91 scope note：本轮强制纯 emoji 的列是外部索引相关编码列（`emoji`、`WoS`、`JCR`、`CAS`、`EI`、`索引核验`）。历史表格中 `阶段状态`、`当前状态`、`核验状态` 等“emoji + 短文本”的混合语义列属于既有投稿情报状态字段，若要迁移为纯 emoji + 说明列，应另开结构化 schema PR，不能在本轮索引事实核验中顺手大改以免破坏 TIMELINE 可读性。

### 17.3 文件同步要求

1. 每个 venue 根 README 必须在 §1 基本信息之后维护 `### 1.1 索引与分区信息`，即使尚未核验，也要用 `❓` / `⚪` / `⏳` 显式占位。
2. [SUMMARY.md](./SUMMARY.md) 的 Venue 总表必须包含 WoS / JCR / CAS / EI / 索引核验列；P0/P1/P2 清单与批量填充记录不再进入 SUMMARY 正文，相关范围 / ownership 留在 [01-venue-scope.md](./01-venue-scope.md) 和本 GUIDE。
3. [TIMELINE.md](./TIMELINE.md) 的投稿事件表与期刊 rolling 表必须包含 `索引入口` 与 `索引核验` 列，链接到 venue 根 README 的索引小节，并用单 emoji 表示索引核验状态；不得在 TIMELINE 中展开 JCR/CAS/EI 细节。
4. `templates/*venue-readme-template.md` 必须包含索引与分区信息模板，防止后续新 venue 漏字段。
5. 所有 `❓`、`🟡`、`⏳`、`🔴` 条目必须在 venue README 内给出行级证据或 access note；若属于跨 venue 共性风险，再同步进入 [SUMMARY.md](./SUMMARY.md) §13 合并待补表，不能只在 venue README 内部孤立标注。

### 17.4 访问受限与缺证处理

若 MJL、JCR、CAS、Engineering Village、publisher 或 source list 页面因订阅墙、WAF、403、登录页、动态页或证书问题不可达，应先保留官方入口与 access note，并继续寻找可点击、字段完整、逐刊逐版本的公开二级证据。若只能取得 AbleSci、AIS 等第三方公开镜像，可展示其 JCR / CAS 数值，但必须显式写明“非 Clarivate/CAS 官方导出 / 公开官方行级记录未获可复现访问”，且 `索引核验` 不得升级为 `🟢`。若二级证据也不可复现，再写 `🔴 已检索未获公开可审计证据`，不得停留在未闭合核验占位。


### 17.5 PR #91 真实核验执行纪律：证据链接、缺证降级与 reviewer 复核

PR #91 将 PR #90 的外部索引占位推进为真实核验记录，后续维护必须遵守以下硬规则：

1. **venue README 是行级证据落点**：每个 `<conf|journal>-*/README.md` 的 `### 1.1 索引与分区信息` 不能只写结论；每一行都必须给出可点击官方入口、source-list snapshot 字段，或明确 access note（如 SPA / WAF / 机构订阅 / 未获公开可审计正文）。
2. **二级公开镜像必须降权标注**：Scimago、LetPub、Guide2Research、DBLP、publisher 年度页、搜索结果页等通常只能作 discovery / 交叉线索；AbleSci、AIS 等若能直接展示逐刊逐版本的 JCR / CAS 字段，可作为二级可审计证据暂存数值，但必须在 venue README 写明“非 Clarivate/CAS 官方导出”，并把 `索引核验` 保持为 `🟡` 或更低。
3. **Elsevier Compendex source list 写法**：使用 [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex) 与 [官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx) 时，必须记录下载 / 查询日期、文件名、sheet、Source title、Source type、ISSN / EISSN 或 ISBN。`SERIALS` 中的 `Journal` 可写 `🟢`；`NON-SERIALS` 中年度 proceedings 只写 `🟠`；LNCS / LNBIP / CCIS 等 book-series 只写 `🟡`，不得冒充会议 source-level。
4. **Clarivate / JCR 踩坑**：MJL / JCR 是官方入口；若官方产品登录或 SPA 壳阻断单刊导出，可用 MJL ISSN 精确命中 + 第三方公开镜像交叉暂存 JCR category/rank/quartile，但必须标注“非 Clarivate 官方导出”。Clarivate press release 只能证明 JCR release 存在，不能单独支撑某刊 quartile。
5. **CAS 踩坑**：[中国科学院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 证明 2026 起停更与第三方发布无关；第三方镜像中的 2025 中科院升级版分区只能写作“公开第三方镜像 / 非 CAS 官方导出”。不得写“2026 CAS 实时分区”，也不得把镜像说成 CAS 官方行级证据。
6. **会议不继承期刊分区**：会议默认 `JCR=⚪`、`CAS=⚪`；同名或近名 venue（如 `conf-a-ase` vs `journal-b-ase`、`conf-b-re` vs `journal-b-re`）必须分开核验。
7. **reviewer 复核要求**：实现后 review 必须抽样打开 venue README 的证据链接；所有 `🟢` EI source-level、所有 `🟠` proceedings-level、所有 `🟡` book-series-level、所有 `⏳`/`🔴` 缺证项都必须检查证据是否支撑当前结论。链接不能支撑结论时，应列为 C/I 级事实风险并要求降级或补证。
8. **source-list snapshot 存储纪律**：venue README 可记录本轮使用的官方 snapshot URL、下载日期、文件名、sheet 与行级字段；大型第三方 `xlsx` 不默认提交进仓库。若后续需要长期归档，应另用 Git LFS、外部 artifact 或专门数据目录，并在本 GUIDE 或专门证据文档记录 hash / 获取方式；SUMMARY 只保留读者需要的短状态，不得因为本地 `/tmp` 文件存在就把它当成永久证据。
9. **source-list 更新纪律**：README 中的 CDN `xlsx` 链接只代表本轮核验 snapshot；后续维护应先从 [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex) 重新进入 `View source list` 获取当期 latest，再决定是否沿用旧 snapshot。若 latest 与旧 snapshot 字段变化，必须回写本节并在更新日志说明差异。
10. **外部索引列不得污染非索引合同表**：WoS / JCR / CAS / EI / 索引核验列只允许进入 SUMMARY Venue 总表、venue README 索引表、TIMELINE 索引入口或明确新增的索引表；不得覆盖 PR ownership、职责边界、数量、允许修改、禁止事项、依赖关系等非索引语义字段。自动脚本批量写表后必须抽查这些合同表。
11. **ICSE / ETAPS dry-run 证据解释纪律**：`Proceedings - International Conference on Software Engineering` 这类 Compendex book-series 行、某一年 ICSE `NON-SERIALS` proceedings 行，以及 LNCS / LNBIP 等 Springer book-series 行，只能支撑 proceedings/book-series 级事实或 discovery 线索；不得把它们写成整个会议 venue 已获 EI source-level 认证。`索引核验` 行也必须同步写清这一点，避免读者只看总表 emoji 后误读。
12. **Clarivate / CAS access note 纪律**：MJL / collection download / journal profile、JCR product record、fenqubiao 历史分区或 API 若需要 free login、product login、机构账号、IP 或 user/password，必须记录官方入口与 access note；裸 GET 得到 SPA 壳页或登录页不能作为单刊官方结论证据。若使用第三方镜像补 JCR/CAS 数值，证据字段必须同时列官方入口、镜像 URL、版本年份和“非官方导出” caveat。
13. **publisher / 镜像交叉证据边界**：ScienceDirect、Wiley、Springer、IEEE 等 publisher 页面若显示 abstracting/indexing、impact factor 或 SCIE 字样，可作为交叉验证或 discovery note；AbleSci、AIS 等公开镜像可作为 JCR/CAS 二级证据展示 emoji，但不能让读者误以为已经取得 Clarivate / CAS 官方导出。任何这类条目的 `索引核验` 最高为 `🟡`。
14. **CAV / 缩写碰撞防误读纪律**：Compendex source list 中的 `CAVS`、`EDCAV` 或其他相近缩写命中不得自动视为 CAV、CAV conference 或任一目标会议的 venue-level EI 证据；必须同时匹配会议全称、proceedings title、ISBN / ISSN、publisher 与年度上下文。若只得到缩写碰撞或其他会议条目，写 `🔴 已检索未获行级证据`，并在 README / SUMMARY 明确“不能作为目标会议证据”。
15. **终态文档不得保留本轮复核动作**：PR ready 前，venue 根 README 的 `索引核验` 行应写成“本轮已完成的证据链、降级理由和后续升级 / 降级条件”，不得把本轮应完成的核验写成仍需 reviewer 或后续人员复查的当前动作；review 要求应留在 GUIDE 或 PR comment，不能作为单个 venue 的事实结论。
16. **踩坑必须回写 GUIDE**：若执行中发现新的 WAF、登录、source-list 字段变化、会议卷歧义、同名混淆、证据不可复现或批量脚本误改非索引字段情况，必须先回写本节或 §16，再判定 PR ready。

## 18. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 21:30:00` | 将 §12.4 第 13 步的结构不变量固化为可执行脚本 [scripts/check_consistency.py](./scripts/check_consistency.py)（覆盖七个年度表↔Mermaid 日期 multiset、年度表升序、§3 孤儿 / 重复 / 过期 / 错类型行、**§3 与年度表的「日期时间」列与 track 名逐字一致**、Mermaid id 唯一与内容洁净、全库表格列数、venue 与年度 README 统计、更新日志降序、相对链接可达），终结每轮 reviewer 各自重写等价脚本并因口径不同产生争论的问题；同时把两条新不变量写入正文。脚本首部与输出均显式声明其边界：**只查结构，抓不到散文中的旧事实，不得替代第 11 步的旧值 grep**。该脚本在引入当轮即抓出 3 处 §3 与年度表的 track 名漂移（简称 vs 正式题名），已一并对齐。 |
| `2026-08-07 21:05:00` | 补强 §12.4 第 11 / 13 步：新增「如何识别一张表是不是 live 表」的通用判据 —— 不靠标题而靠「**无时间戳列 + 内容为状态断言**」判定，并点名 TIMELINE §6 / §15 / §14 三张标题像归档、语义却是 current-value 的表（各自在 2026-08 那轮漏改过至少一次；其中 §6 的 ICST 2027 行错误在本轮之前即已存在于 main，说明该表从未进入同步流程）；同时写死年度表的两种合法计数口径及其换算式（数据行数 + 日期区间行数 = 日期出现总次数，2027 为 50+13=63、2026 为 192+40=232），终结跨轮次的计数分歧。 |
| `2026-08-07 20:50:00` | 扩展 §12.4 常态化刷新 checklist 由 11 步增至 13 步，修复本轮 review 反复暴露的根因：新增第 11 步「同步散文与非表格落点」，点名三类不在原 checklist 内且无法被不变量脚本发现的遗漏位置（venue 根 README §7 散文 bullet、年度页 §8 待补记录、TIMELINE §14 期刊滚动表的 live-state 列），并规定每次事实更新后必须用旧值对全库 grep、逐条判定是当前值残留还是合规历史记录；新增第 13 步「不变量自查的强度要求」，明确年度表与 Mermaid 不能只比数量而必须按日期 multiset 比对（本轮曾出现 190=190 但集合不同），并写明脚本抓不到散文旧事实、不可用脚本通过替代旧值 grep。 |
| `2026-08-07 20:40:00` | 2026-08 全量刷新后固化检索与取证规则：新增 §16.6，把访问失败四分类（Springer authwall+JS 壳 / Elsevier CAPTCHA / ACM bot 页 / Wiley Cloudflare+402）、`rd.springer.com` 官方 fallback 通道、`Access denied ≠ 404` 的三种 researchr 入口语义、UA 型 bot 过滤与通配符域假阳性、slug 与 series 入口漂移、伞会议按子会议展开维护、HTML 注释 / 删除线 / 时区属性 / frameset 的解析陷阱，以及「空白位翻新与已有事实维护同等重要」写成硬规则；同步收紧 §12.7 的访问受限行记录要求。 |
| `2026-06-09 20:50:00` | 清理可能和旧 CCF 字母等级混淆的 字母等级表达，改用 🏆/🥈/🥉 档表述，保持与 SUMMARY / venue README 的 emoji 口径一致。 |
| `2026-06-09 20:36:00` | 按最新 SUMMARY 单表化要求制度化：SUMMARY 正文只保留总览、外部索引口径、一个 Venue 总表、一个待补核查表和更新日志；PR 流程、执行合同、踩坑长表、watchlist 过程回到 GUIDE / scope / README / changelog。 |
| `2026-06-09 18:52:22` | PR #91 终态收口规则回写：索引核验行应记录已完成证据链与后续升级条件，不得把本轮核验留成 reviewer 复核动作；同步 venue 根 README 口径。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查与 CAV 缩写碰撞防误读：规定所有 CCF 等级字段统一使用 🏆/🥈/🥉，并禁止将 CAVS/EDCAV 等相近缩写升级为 CAV EI 证据。 |
| `2026-06-09 17:53:17` | PR #91 reviewer M 级建议修复：将时间格式规则拆分为投稿 / 事件时间默认分钟级、信息更新时间 / 更新日志默认秒级，历史分钟级日志兼容保留。 |
| `2026-06-09 17:05:00` | PR #91 复核后修正：明确 CCF 三档等级使用 🏆/🥈/🥉，禁止回退为单色编码；将访问受限处理改为公开可审计核验 / 二级镜像降权，不再停留为未闭合核验占位。 |
| `2026-06-09 14:35:00` | 吸收 dry-run 证据复核：补充 ICSE proceedings / ETAPS LNCS book-series 不得升级为 venue-level EI 事实，并明确 MJL/JCR/CAS 登录壳页与 publisher 交叉证据边界。 |
| `2026-06-09 14:20:00` | 吸收 PR #91 实现 review C/M 级反馈：补充 source-list snapshot 存储与更新纪律，并禁止外部索引列覆盖 PR ownership 等非索引合同字段。 |
| `2026-06-09 13:52:01` | PR #91 真实核验执行：新增证据链接落点、Compendex source list、Clarivate/JCR/CAS 缺证降级与 reviewer 复核纪律。 |
| `2026-06-09 12:13:06` | 修复外部索引制度化复审问题：将外部索引规则独立为 §17，并补充 venue README `emoji` / `当前结论` 分工与 TIMELINE `索引入口` 占位边界。 |
| `2026-06-09 11:13` | 新增外部索引与分区制度化规则，规定 WoS/JCR/CAS/EI 来源、emoji 列、SUMMARY/TIMELINE/venue README 同步要求与缺证处理。 |
| `2026-06-07 12:47` | PR #63 LLM4Modeling-SE 扩展：补充 CCF 官方 / 镜像证据等级、ASE Journal / CAiSE / ICECCS 的消歧、scope 边界、计数与 TIMELINE 同步规则。 |
| `2026-06-07 11:25` | PR #62 final M 级 polish：补充 SUMMARY 最新事实刷新锚点更新条件、P0 默认 watchlist 交叉锚定，以及 TIMELINE 辅助列中 `⏳ 已检索未公布` 的合法使用边界。 |
| `2026-06-07 11:10` | PR #62 实现后 review 修复：将冲突标记自查命令改为行首锚定，补充 TIMELINE §15 / SUMMARY §13 入口释义，并明确 `⏳ 已检索未公布` 不得进入 dated TIMELINE / Mermaid。 |
| `2026-06-07 10:52` | PR #62 常态化投稿情报更新机制：新增 §12，固定刷新频率、watchlist、字段落点、状态迁移、来源降级、SUMMARY/TIMELINE 分工与 reviewer dry-run 验收规则。 |
| `2026-06-06 00:41` | PR-10 实现后 review 修复规则回写：明确 researchr 行级 `Timezone` 已给出时，必须把 AoE / UTC offset 写入 TIMELINE 与年度页，不能继续写“官方仅日期”。 |
| `2026-06-06 00:16` | PR-10 全局审计规则回写：补充 subagent 503/429 降级核验、researchr 行级时区检查、模板占位路径非伪链接和 ready 前核实项清零纪律。 |
| `2026-06-05 23:06` | PR-9 冲突后复审修复：同步 PR-9 已完成状态、39/273 合流统计纪律，并补充 week-only 日期不得进入 dated TIMELINE / Mermaid 的 P2 规则。 |
| `2026-06-05 22:34` | PR-9 merge 最新上游 PR-8：保留 PR-6 / PR-7 / PR-8 规则回写与 PR-9 §16.4 P2 邻近观察规则，要求冲突复审同时覆盖 P1/P2 facts、TIMELINE、Mermaid、rolling 表、统计与更新日志。 |
| `2026-06-05 21:16` | PR-8 merge 最新上游 PR-6 / PR-7：合并 PR-6 维护 / 修复 venue 规则、PR-7 实证 / 质量 venue 规则与 PR-8 形式化 / 工具链规则，明确三路 P1 sibling 合流后统计为 34/238 且冲突解决必须保留双方 TIMELINE、rolling 表、统计与更新日志 facts。 |
| `2026-06-05 20:56` | PR-6 合流 PR-7 后回写冲突处理纪律：强调合流统计需重算为 30/210，PR-6 / PR-7 facts 必须共存，PR-8 / PR-9 不得误标完成。 |
| `2026-06-05 20:35` | PR-8 merge upstream PR-7：合并 PR-7 Springer collection / ESEM 历史投稿系统纪律与 PR-8 Elsevier / QRS / TASE 纪律，明确冲突解决必须保留双方 TIMELINE、rolling 表、统计与更新日志事实。 |
| `2026-06-05 19:16` | 修复 PR-8 实现后 review：补强超 40 条年度 Mermaid 拆图执行规则，并明确 sibling PR 共享统计必须区分 branch-local / 组合口径。 |
| `2026-06-05 18:40` | PR-8 形式化 / 工具链补链规则回写：补充 Elsevier / ScienceDirect WAF/403、Editorial Manager code、QRS techconf 计数拆分与 TASE 分散年度站处理纪律。 |
| `2026-06-05 18:13` | PR-6 踩坑规则回写：补充 SANER/ICSME/ICPC 历史入口与日期冲突、SANER 2022 证书风险、JSEP Wiley WAF/current issue/Early View/rolling 候选口径。 |
| `2026-06-05 18:12` | PR-7 实证 / 质量 venue 规则回写：补充 ESEM historical submission system、Springer Closed collection / historical deadline、ESE 多事件类型、special issue editors 与长期 editorial board 分离，以及 Elsevier / ScienceDirect CLI 403 / WAF 处理纪律。 |
| `2026-06-05 15:59` | 实现后 review 修复：明确 GUIDE §14.1 只是 SUMMARY §9.1 合同摘要，并同步 PR-8 / PR-9 前置条件提示。 |
| `2026-06-05 15:36` | PR-5 全局收口：补充 PR-6~PR-10 stacked execution contract、共享文件增量合流边界、合同外 venue 禁止事项和历史更新日志扫描口径。 |
| `2026-06-05 13:25` | merge upstream / PR-3+PR-4 合流规则：解决 GUIDE 冲突，保留形式化验证会议来源冒充、committee / track 分层、`curl -k` / 冲突复审纪律，同时保留 PR-4 期刊 rolling / dated event、Wiley WAF/403、Springer collections 和 STTT conference-based special issue 计数纪律。 |
| `2026-06-05 12:35` | PR-4 SUMMARY/GUIDE 专项复核：补强 Wiley WAF/403/SPA 壳处理表述，明确需保留官方入口并未获公开可审计正文，不能以第三方页面替代 STVR 当前 roster / guidelines / 卷期正文。 |
| `2026-06-05 12:18` | 吸收 PR-4 期刊填充经验：补充 Springer collections dated event、Wiley WAF/403、Equinocs / Wiley Authors SPA、STTT conference-based special issue 计数和期刊 rolling / dated event 同步纪律。 |
| `2026-06-05 11:43` | 收尾复审后补充 `待补时刻 AoE` 的固定语义：日期和时区已核验，只有具体钟点待补，避免 reviewer 误读为日期待补。 |
| `2026-06-05 11:25` | 根据 upstream merge 复审补强 GUIDE：明确不能用单年度站点冒充 stable series page，并要求冲突解决同时检查文本标记和 Git index resolved 状态。 |
| `2026-06-05 10:58` | 合并上游 PR-2 规则与 PR-3 复审规则：保留会期同步、草稿清理、Mermaid label、自查纪律，同时补充来源冒充、committee 角色源、`curl -k` / WAF 访问异常和冲突处理复审要求。 |
| `2026-06-05 10:04` | PR-3 复审后补充硬纪律：踩坑必须按影响范围写回 README / SUMMARY / GUIDE，明确年度主页、series page、CFP、投稿入口、committee 角色源和 `curl -k` 访问异常的边界。 |
| `2026-06-05 10:00` | 根据 PR-2 修复后复审继续补强 GUIDE：修正链接规范示例，明确 `Conference dates` 也必须同步进 TIMELINE 表格与 Mermaid，并把 ISSTA 2022/2023 会期漏同步沉淀为强制自查项。 |
| `2026-06-05 09:43` | 根据 PR-2 复审与用户补充要求，新增踩坑复盘与规则回写纪律，补强 TIMELINE Mermaid edition label、临时草稿链接清理、核心人员字段一致性和 review 经验回写要求。 |
| `2026-06-05 00:36` | 合入期刊试点后完成共享规则合流：正文改为会议 / 期刊长期事实共存规则，保留期刊核验等级、会议核心人员分层、模板占位链接和 TIMELINE 事件发生年份口径。 |
| `2026-06-04 23:04` | 吸收 PR-1A 合流协议：明确会议 / 期刊核心人员分轨、TIMELINE 事件发生年份规则、模板占位链接规则和并行 PR 事实 ownership。 |
| `2026-06-04 22:05` | 根据正式复审补充期刊核心编辑人员的核验等级 / 当前性规则，明确候选线索和 legacy 运营线索不得写成当前 roster。 |
| `2026-06-04 21:30` | 补充全库更新日志降序规则，并新增期刊核心编辑人员情报规则：期刊 PR 必须核验核心编辑的研究方向、代表作和近 5 年论文入口。 |
| `2026-06-04 19:37` | 新增核心 URL 字段与 Markdown 超链接规范，要求 venue 根表、年度页和 TIMELINE 都挂可点击链接。 |
| `2026-06-04 18:55` | 明确后续搜索必须至少到当前年份 + 2；当前初始化覆盖到 2028，更远未来若已有官方信息也继续纳入。 |
