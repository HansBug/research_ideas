# `ccf_venues/` GUIDE

> 信息更新时间：`2026-06-05 20:56`（Asia/Shanghai）

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

## 3. 时间格式规范

本库的所有时间字段必须精确到分钟，格式统一为：

```text
yyyy-mm-dd hh:mm
```

补充规则：

1. 若官方只给日期，不给具体时间，写成 `yyyy-mm-dd 待补时刻`，并在备注中说明“官方仅公布日期”。
2. 若官方只给日期且明确时区，写成 `yyyy-mm-dd 待补时刻 AoE` 或 `yyyy-mm-dd 待补时刻 UTC-12h`；其语义是“日期与时区已核验，具体钟点未公布或待补”，不得理解为日期本身待补。
3. 若官方给出 timezone，必须保留 timezone，例如 `2026-01-15 23:59 AoE`。
4. 若官方给出多个时区，以官方原文为准，不擅自换算；如需换算，另加一列 `北京时间换算`。
5. `信息更新时间` 与 `更新日志` 也统一精确到分钟，不写秒。
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

会议历史投稿系统补充纪律：历史年度的 submission system 只记录当年官方 CFP / Important Dates / author instructions 明确给出的入口；若入口已经关闭、重定向、登录后不可见或只剩 EasyChair / HotCRP / PCS 等历史壳，应写成 `历史投稿入口已关闭 / 待人工登录核验`，不得用当前年度投稿系统反推旧年度，也不得把投稿系统入口冒充年度主页、CFP 或 accepted papers 来源。ESEM 这类实证会议的历史年度尤其要保留“官方来源仍可证明当年使用过该系统”和“当前是否还能访问正文 / 表单”两层事实。

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

补充纪律：若 Wiley / ACM / IEEE / Elsevier / ScienceDirect 等 publisher 页面在命令行环境中返回 WAF、Cloudflare、403、SPA 壳或登录页，必须保留官方 URL 作为核验入口，并在对应字段写清“待人工浏览器核验”；不得用第三方页面替代当前官方 roster、author guidelines、articles in press、online first 或卷期正文，也不得臆造 Editor-in-Chief / editorial board 当前名单。ScienceDirect 命令行 `403` / WAF 只说明 CLI 抓取受限，不等价于官方页面不存在；JSS 这类 Elsevier 期刊应保留 ScienceDirect / Elsevier 官方入口并标注访问风险，DBLP 只能作论文名录或计数 fallback。

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

1. ESEM 历史年度投稿系统若来自当年官方 CFP / submission instructions，可以记录为历史事实；若入口已关闭或需登录，字段写 `历史入口已关闭 / 待人工登录核验`，不要改写成 `未公布`，也不要用新年度系统补旧年度。
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
2. Requirements Engineering 这类期刊 collection deadline 是期刊专刊事件，不是同名会议 deadline；TIMELINE 的 `类型-CCF` 应写作 `期刊专刊-CCF B/C` 等。
3. STTT 这类期刊常包含 TACAS / SPIN / FMICS / Runtime Verification / ECBS 等 conference-based special issue、invited 或 extended papers；DBLP `entry article` baseline 不能与对应会议 proceedings 数混算，也不能用会议会期或会议 CFP 反推期刊 deadline。
4. Wiley Online Library / Wiley Author Services / Equinocs、ScholarOne 等 publisher 或投稿系统若在命令行环境返回 WAF、Cloudflare、403、SPA / 登录壳，应记录为“官方入口已定位，正文 / 具体表单 / journal routing 待人工浏览器或登录核验”；不得用第三方页面替代 STVR 这类 Wiley 期刊的当前 roster、author guidelines 或卷期正文。

PR-7 实证 / 质量期刊填充后的补充规则：

1. Springer `collections` / topical collections 若状态为 `Closed`，仍可作为历史 special issue / collection 事实记录；若官方页给出 historical submission deadline，应按事件发生年份进入 [TIMELINE.md](./TIMELINE.md) 的历史 dated event，并在备注写明 `Closed / 历史 deadline`。Closed collection 不得写成当前 `🟡 专刊征稿`，也不得反推未来年度 active CFP。
2. Empirical Software Engineering 等 Springer 期刊 collection 页面可能同时列出 `Submission deadline`、`Notification`、`Revision due`、`Final decision`、`Publication` 等多类事件；年度 README 和 [TIMELINE.md](./TIMELINE.md) 必须保留官方事件语义，不能把 notification、revision 或 final decision 统一改名为 submission deadline。只有官方给出明确日期的事件进入 dated 表；只给月份或季度的事件只能写入备注 / 待补记录。
3. Special issue / topical collection editors、guest editors 或 collection editors 是当期专题角色，不等同于长期 editorial board / editorial leadership。除非同一人员另有官方当前 editorial board 页面支撑，否则不得把 collection editor 写入期刊根 README 的当前核心编辑人员正表；应放在年度 special issue / collection 小节或单独“专题编辑线索”小节。
4. Elsevier / ScienceDirect 的 guide for authors、volume / issue、articles in press、online first、editorial board 页面若在 CLI 中返回 `403`、WAF、JS 壳或空正文，应保留官方链接并标注 `CLI 403/WAF，待人工浏览器核验`；不得用 DBLP、Scimago、LetPub、Guide2Research 或第三方索引替代官方入口。DBLP 可用于年度论文名录 / 计数 fallback，但不能支撑 author guidelines、current roster 或 articles in press 当前性。

### 5.3 Markdown 链接写法

1. 已找到 URL 时，表格中直接写 Markdown 链接，例如 `[ICSE 2026](https://conf.researchr.org/home/icse-2026)`。
2. 本库内部页使用相对路径，且示例链接必须真实可达：在文库根文档中写 [`conf-a-fse/2026`](./conf-a-fse/2026/README.md)、[TIMELINE.md](./TIMELINE.md)；在 venue 根 README 中才写 `./2026/README.md` 这类相对年度页。
3. 未找到 URL 时不要伪造链接，写 `待补`、`未公布`、`无已知` 或 `⏳ 已检索未公布`，并在证据 / 核查记录里写核查时间。
4. 模板中的外部 URL 占位符不得写成 Markdown 链接；统一写 `待补（占位：OFFICIAL_URL；核验后改为 Markdown 链接）`。这样能避免模板被误读为已有可点击事实来源。
5. 模板中的本库内部已知路径必须继续写相对 Markdown 链接，例如 [TIMELINE.md](./TIMELINE.md)、[`conf-a-fse/2026`](./conf-a-fse/2026/README.md)；不要把内部已知路径降级成纯文本。若模板位于 venue 目录内，可用 `./2026/README.md` 指向同 venue 年度页。
6. 第三方聚合页只能放在备注或 fallback，不得放进“官方来源”列。
7. 官方年度主页、series page、organizer call、CFP、Important Dates、submission system、program / accepted papers 和 proceedings 是不同字段；只有能直接代表该年度 edition 的页面才可写入“官方年度主页”。Series page / organizer call / submission system 只能放入对应字段或 fallback / 备注，不得冒充年度主页或 CFP。
8. 不得把某一个年度站点冒充为 stable series page；若未发现独立稳定 series page，根 README 写 `待补`，可把 DBLP venue index 或官方年度页写作 fallback / 年度事实来源。
9. 命令行访问遇到证书问题时可以使用 `curl -k` 或浏览器继续核验；但 `404`、Access denied、空页、WAF 返回页、未公布占位、只有 series 入口等都不是有效事实来源，必须写成访问风险或 `⏳ 已检索未公布`。

### 5.4 核心人员情报规范

核心人员情报是本库的一等学术情报，不是可选备注。它服务于后续判断 venue 的研究共同体、审稿偏好、主题连续性和潜在投稿适配度。

会议根 README 应维护“核心人员情报”小节。默认覆盖：

1. 当前 / 未来年度 General Chair、Program Chair、Research Track Chair、Technical Track Chair、Artifact / Tool / SEIP 等与本仓库 project 强相关 track 的 chair。
2. Steering Committee / Advisory Board / Organizing Committee leadership。
3. 在相关 track 或历年组织中反复出现、且与本仓库 project 强相关的领域权威。
4. 对 umbrella venue，例如 ETAPS，应区分 umbrella 层级、main conference / satellite conference 层级和具体 track 层级；不要把 TACAS chair、ETAPS general chair 和 workshop organizer 混写成同一类角色。

会议人员表至少包含：姓名、年度 / 层级、会议角色、单位、官方角色来源、主页或学术入口、主要研究方向、代表作或近 5 年论文入口、与本仓库 project 的关系、核验状态、核查时间。人员事实应优先来自官方 committee / track 页面；研究方向和代表作可来自主页、DBLP 或学术入口，但必须说明是公开资料判断。

期刊根 README 应维护“核心编辑人员情报”小节。默认覆盖 Editor-in-Chief / Editors-in-Chief、Co-Editor-in-Chief、Associate / Area Editor-in-Chief、Managing Editor、Editorial Board leadership、与本仓库强相关的 editorial board 成员，以及当年 special issue / topical collection guest editor。期刊人员表必须保留 `核验等级 / 当前性` 列，区分官方当前 roster、官方公告、个人 / 机构页候选线索和 legacy / 运营线索。

完整人员表放在各 venue 根 README；[SUMMARY.md](./SUMMARY.md) 只记录覆盖状态、主要缺口和跨类型合流提示，不复制全量人员表。

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
4. 如果某一年事件超过 `40` 条，按 `A 类 / B 类 / C 类` 或 `会议 / 期刊专刊` 拆成多张 `gantt` 图。
5. Mermaid 展示 label 必须使用 **venue edition 年份**，不能使用事件发生年份。例如 `FSE 2026` 的 `2025-09` submission 在图中显示 `FSE26 Submission`，而不是 `FSE25 Submission`。
6. Mermaid event id 推荐使用 `<venue_slug>_<event_year>_<sequence>_<yyyymmdd>`，其中 `sequence` 只保证同一事件发生年份内唯一；展示 label 与 event id 可以不同。
7. Mermaid label 使用短但完整的英文事件词：`Abstract`、`Submission`、`Notify`、`Camera`、`Rebuttal`、`Conference`；不要写成 `Notificati`、`Cameraread` 等机械截断词。
8. Mermaid 更新后必须至少人工预览；若本地具备 Mermaid CLI，可补充渲染检查。

### 11.4 同步规则

1. 新增或修改任何年度 README 中的投稿相关 important date 后，必须同步检查 [TIMELINE.md](./TIMELINE.md)。`Conference dates` 也是 important date；只要年度 README 已有官方会期且事件发生年份在本库范围内，就必须进入 TIMELINE 表格和 Mermaid，不能只同步 submission / notification。
2. 若某个时间点因官方来源冲突被标为 `⚠️ 矛盾待解`，TIMELINE 表格也必须保留该状态，不得只在 venue 年度 README 中记录。
3. [TIMELINE.md](./TIMELINE.md) 只汇总已进入本库的 venue，不替代 P1/P2 待补清单。
4. 会议填充负责维护会议 dated events；期刊填充负责维护期刊 rolling 表和期刊 special issue dated events。合流时不得互相删除已经核验的事件行。
5. 临时 PR 增量表、`_events_draft.md` 或等价草稿只能作为迁移过程中的审计辅助，不得长期作为 dated event 事实源；一旦事件已核验，应并入正式年份章节与 Mermaid。
6. 最终提交前必须删除临时草稿，并把所有根 README / 年度 README 中的草稿链接改成指向 [TIMELINE.md](./TIMELINE.md) 的事实陈述；不得在正式文档中留下 `_events_draft.md` 死链接或“主 session 合流时”这类 PR 内部流程语气。
7. TIMELINE 表格与 Mermaid 必须一起更新：表格按事件发生日期升序，Mermaid 不放 URL，且图中 edition label 必须与表格 Venue edition 一致。

## 12. 初始化 PR 自审流程

当任务是“先开初始化 PR，不填实际 venue 数据”时，必须按以下顺序自审：

1. 确认 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[TIMELINE.md](./TIMELINE.md)、[01-venue-scope.md](./01-venue-scope.md) 和 [templates/](./templates/) 均已存在。
2. 确认 PR body 是可执行计划，包含目标、骨架交付物、P0/P1/P2 分批、TIMELINE 同步规则、验收标准、已知限制和下一步停靠点。
3. 确认 `SUMMARY.md` 不声称任何未建 venue 已完成。
4. 确认模板中的相对链接在未来实际 venue 路径下可成立。
5. 确认 Mermaid 代码块使用 GitHub 较稳定的 `gantt` 语法，不使用实验性 `timeline` 作为主图。
6. 完成自审后停止，等待用户确认是否进入 P0 数据填充。

## 13. 一轮数据填充流程

1. 先读 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
2. 根据 [01-venue-scope.md](./01-venue-scope.md) 选择本轮 venue。
3. 新建或更新 `<conf|journal>-<rank>-<slug>/README.md`。
4. 从最新年份开始，按降序补年度 README，默认覆盖到 `2022`。
5. 若目标是会议 venue，补根 README 的核心人员情报；至少覆盖当前 / 未来年度组织与审稿 leadership、Steering / Advisory 层级、强相关 track chair 和领域权威；umbrella venue 必须写清层级。
6. 若目标是期刊 venue，补根 README 的核心编辑人员情报；若暂不能核验，写明缺口、检索入口和核查时间。年度页只在 special issue guest editor、年度 editorial team 或人员变更与当年事实直接相关时单独记录。
7. 回填上级 venue README 的年度汇总表。
8. 若更新内容涉及投稿相关 important date，同步回填 [TIMELINE.md](./TIMELINE.md) 的年度表格与 Mermaid Gantt；事件行必须包含事件官方来源、年度主页、本库年度页，已结束年度还应尽量包含论文集 / 论文名录链接。
9. 回填 [SUMMARY.md](./SUMMARY.md) 的覆盖进度、核心人员覆盖状态、踩坑记录和待补清单。
10. 若本轮 review / 自查发现新的 C/I 级问题，或发现会反复影响后续填充的 M 级共性坑，必须把修复后的规则回写到本 [GUIDE.md](./GUIDE.md) 或 [SUMMARY.md](./SUMMARY.md) 对应“踩坑”小节，不能只在 PR comment 中解决一次。
11. 检查所有链接可点击、所有时间精确到分钟、所有状态符合口径，且 Mermaid 语法可预览。
12. 在相关 README 文末更新日志中按时间降序插入记录。

### 13.1 P1/P2 stacked PR 执行纪律

PR-5 已将 P1/P2 扩展冻结为 PR-6~PR-10 的 stacked execution contract；后续 AI 不得只凭 [01-venue-scope.md](./01-venue-scope.md) 的范围清单自由拆分。完整禁止事项、允许修改范围与依赖关系以 [SUMMARY.md](./SUMMARY.md) §9.1 为准，本节只保留执行纪律摘要。PR-6 与 PR-7 已完成基础建档并在当前合流分支中共存；当前统计不在本节维护，以 [SUMMARY.md](./SUMMARY.md) §1 与 §9 的完成状态为准；本节保留 stacked PR ownership 纪律。

| 子级 PR | 主题 | Venue ownership | 默认产物 | 共享文件纪律 |
|---|---|---|---|---|
| PR-6 | P1-Maintenance / Repair | `conf-b-saner`、`conf-b-icsme`、`conf-b-icpc`、`journal-b-jsep` | 4 个 venue + 28 个年度 README；已基础建档 | 只增量维护自有 venue 的 SUMMARY / TIMELINE / README / GUIDE / scope 事实 |
| PR-7 | P1-Empirical / Quality | `conf-b-esem`、`journal-b-ese`、`journal-b-jss`、`journal-c-sqj` | 4 个 venue + 28 个年度 README；已基础建档 | 保留 PR-6 与 P0 facts，期刊 rolling 不写成 dated Mermaid |
| PR-8 | P1-Formal / Toolchain | `journal-b-ist`、`journal-b-scp`、`conf-c-qrs`、`conf-c-tase` | 4 个 venue + 28 个年度 README | 须在 PR-6/7 合入上游并阅读其踩坑经验后开工；形式化 / 工具链计数不得混用 DBLP fallback |
| PR-9 | P2 Neighboring Observation | `conf-c-apsec`、`conf-c-seke`、`conf-c-ease`、`conf-c-msr`、`conf-c-rv` | 5 个 venue + 35 个年度 README | 须在 PR-6/7 合入上游后开工；建议同步吸收 PR-8 形式化 / 工具链踩坑经验；不升级为 P0/P1 主投目标 |
| PR-10 | P1/P2 Global Audit | 不新增 venue；审计 PR-6~PR-9 | 统计 / 时间线 / Mermaid / 待补项全局收口 | 必须等 PR-6~PR-9 全部合入上游后执行 |

执行要求：

1. 每个子 PR 只能创建 / 修改自己 ownership 内的 venue 目录；共享文件只能做自有事实的增量合流，不得删除 P0、会议试点、期刊试点或其他子 PR 已核验事实。
2. 默认年度范围仍为 `2022` 至当前年份 + 2；发现更远未来官方 CFP / important dates 时继续纳入，并在 PR body 与更新日志说明。
3. 不得静默新增合同外 venue。确需新增时，先更新 [01-venue-scope.md](./01-venue-scope.md) 与 PR body，并给出 CCF 官方或 venue 官方来源。
4. final ready 前必须 merge upstream staging head；若有 conflict，冲突解决后必须复核 `git ls-files -u` 为空、冲突标记消失、双方 TIMELINE / Mermaid / rolling 表 / 更新日志 facts 均保留。
5. 历史更新日志可以保留当时真实的旧统计数字；旧口径扫描应聚焦正文和当前总账，不得为了让 `rg` 零命中而篡改历史日志。

## 14. 会议 / 期刊合流与事实共存规则

本库的会议数据、期刊数据、共享规范和模板会被不同轮次持续维护。任何合流或冲突解决都必须遵守以下长期规则：

1. **共享规范优先**：时间格式、更新日志降序、Markdown 链接占位、核心 URL、核心人员情报和 TIMELINE 事件发生年份规则属于共享规范；任一轮修正后，后续维护应吸收协议层规则。
2. **事实类型分离**：会议事实、会议年度 README、会议核心人员和会议 dated events，与期刊事实、期刊年度 README、期刊核心编辑人员、期刊 rolling 表和期刊 special issue dated events 分开维护。
3. **SUMMARY 不回退事实**：已经完成基础核验的会议或期刊不得被后续空白占位写回 `⏳ 待建`；若某轮不处理某类事实，应保留既有状态和链接。
4. **TIMELINE 不互删事件**：会议 dated events、期刊 rolling 表和期刊 special issue dated events 合流后必须共存；冲突解决时以“事件发生年份 + 来源可点击 + 已核验事实不删除”为准。
5. **模板统一协议**：外部 URL 占位符使用纯文本占位，内部已知路径使用相对 Markdown 链接；更新日志提示统一为“更新日志按时间降序排列，最新记录置于最上方。”。
6. **试点经验保留边界**：会议试点和期刊试点的踩坑结论都应保留在 [SUMMARY.md](./SUMMARY.md) 的对应小节，但不得把某一类试点的 deadline、论文数量或人员 roster 复制成另一类事实。

## 15. 踩坑复盘与规则回写纪律

本库是长期情报库，不是一次性 PR 产物。任何一轮踩坑都必须沉淀为后续 AI 能直接执行的规则，避免同类错误在后续 venue 中重复出现。

### 15.1 必须回写的踩坑类型

1. **来源与计数口径坑**：例如 FSE / ESEC-FSE / PACMSE 命名与计数、ISSTA 与 FSE / ECOOP / SPLASH co-location、ASE 多 track 与 DBLP 全 proceedings fallback、RE 的 IEEE Xplore conference number、REFSQ 的 Springer / CEUR / DBLP 分散入口。
2. **TIMELINE 组织坑**：例如 edition 年份与事件发生年份错位、Mermaid label 使用事件年份导致误读、年度表格已更新但 TIMELINE 未同步、会期事件在根表 / 年度 README 中存在但全局时间线缺失。PR-2 已踩过 ISSTA 2022/2023 年度页有 `Conference dates` 但 TIMELINE 漏写的坑，后续必须把会期同步纳入强制检查。
3. **链接与草稿坑**：例如 `_events_draft.md` 已删除但正式 README 仍链接、模板占位链接被误认为事实链接、官方页面 access denied 但未标明 probe / fallback。
4. **核心人员情报坑**：例如不同 venue 人员表列结构不一致、缺少 `核验状态` / `核查时间`、只写聚合 Steering Committee 而没有可追踪具体人员、研究方向或代表作没有主页 / DBLP / 学术入口支撑。
5. **未来年度信息坑**：例如只查到当前年而未查当前年份 + 2，或未来年度已有官方主页 / CFP 却未入年度 README；反过来也不得为未公布年度虚构 deadline。
6. **合流与共享文件坑**：例如后续 PR 修改 [TIMELINE.md](./TIMELINE.md) 时误删期刊 rolling 表、SoSyM special issue dated event、Requirements Engineering 2026 collection dated events、已核验会议事件，或把上游试点 venue 写回待建。
7. **访问异常与来源冒充坑**：证书问题可以用 `curl -k`、浏览器或带 `User-Agent` 重试；但 `404`、Access denied、空页、WAF 返回页、未公布占位、只有 series 入口、投稿系统入口或 organizer call 都不得写成年度主页 / CFP / committee 官方角色源；Wiley STVR 等 publisher 页面在 CLI 中 WAF/403 时仍应保留官方链接和待人工浏览器核验状态，不能把“无法命令行抓取”改写成“无编辑人员”或用第三方页面补成当前 roster。
8. **track 与角色混算坑**：research、industry、tool、artifact、workshop、journal-first、companion、umbrella conference 与 satellite conference 必须分列；committee / editorial roster 角色不足时只能写成线索，不能升级为已核验核心人员事实。
9. **期刊专刊 / 会议扩展混算坑**：例如 STTT 的 conference-based special issue 只能按期刊 article baseline 记录，不能和 TACAS / SPIN / FMICS / RV 等会议 proceedings 合并计数。
10. **维护 / 演化 venue 历史入口坑**：SANER / ICSME / ICPC 等维护、演化、程序理解会议的旧年度站点、CFP、submission system、program、proceedings、DBLP slug 经常分散；找不到官方 CFP 时只能写 `待补` 或 `第三方线索`，不能把第三方 deadline 写成官方事实。
11. **冲突日期同步坑**：若 ICSME 2022 这类年度出现 IEEE CFP、archive 首页、proceedings 封面会期不一致，根 README、年度 README、[TIMELINE.md](./TIMELINE.md) 与待补表必须同步标 `日期冲突待核`，不能只在单个文件说明。
12. **证书风险入口坑**：若官方旧站 HTTPS 证书主机名不匹配但 HTTP 可访问，例如 SANER 2022，应优先使用可访问的 HTTP 官方站入口，并在备注中显式写明 HTTPS 证书风险；不要留下会让读者点击失败的裸 HTTPS 链接。
13. **Wiley current issue / Early View 混写坑**：Wiley `currentissue` 只可写作 current issue candidate，不能冒充 Early View / articles in press；若 Early View 入口未定位，应单独写 `Early View / articles in press 入口待定位`。JSEP 本轮已按此规则将 2026+ rolling 状态降级为 `🟡 rolling 候选 / 待人工核验`；STVR 等既有 Wiley WAF/403 历史条目在后续触碰或专项复核时也应吸收该口径。不得在 author guidelines / ScholarOne 路由未人工确认前，把新建或本轮修改的 Wiley WAF 条目写成 `🟢 滚动开放`。
14. **未来年度维护会议预造坑**：SANER / ICSME / ICPC 的 2027/2028/2029+ 若只找到 series page、announcement、townhall、program 预告或无 official research track dates，应写 `⏳ 已检索未公布`，不得预造 official CFP、submission deadline、DBLP 年度页或 proceedings。
15. **PR-6 / PR-7 合流统计坑**：PR-6 与 PR-7 单独分支各自都是 26 个 venue / 182 个年度 README；二者合流后必须重算为 30 个 venue / 210 个年度 README（20 会议 / 10 期刊），并同时保留 P0 22/154 冻结基线、PR-6 / PR-7 已建档事实、PR-8 / PR-9 pending 约束和 PR-10 全局审计依赖。
16. **PR-7 实证 / 质量 venue 坑**：Springer Closed collection 仍可能有 historical deadline，必须写成历史 dated event 而不是当前征稿；ESE collection 多事件类型要保留 submission / notification / revision / final decision 的原始语义；ScienceDirect CLI `403` / WAF 只能标注待浏览器核验，不能替代或删除官方 Elsevier 链接；ESEM historical submission system 要区分“当年官方使用过”和“当前入口是否仍可访问”。

### 15.2 回写位置

1. 能形成长期操作规则的，优先写入本 [GUIDE.md](./GUIDE.md) 对应章节；若找不到合适章节，写入本节。
2. 只属于某一批 venue 的事实性经验，写入 [SUMMARY.md](./SUMMARY.md) 的“踩坑记录 / 待补与核查记录”，并在相关 venue 根 README 的维护备注中保留。
3. 单个年度或单个字段的 unresolved fact，写入对应年度 README 的“证据与核查记录”和 [SUMMARY.md](./SUMMARY.md) 的待补表，不要扩大成全库规则。
4. PR comment 中提出的 C/I 级问题若已经修复，必须在最终 PR 汇总或 PR body 中说明“修复点 -> 本库规则 / 文档落点”，便于后续 reviewer 追踪。
5. 若时间不足，至少在本轮更新日志中明确“哪些坑尚未完全规则化”，不得只把坑留在 PR comment 或口头总结里。

### 15.3 PR 结束前强制自查

每轮数据填充 PR 在声称 ready 前至少执行以下检查：

1. `rg -n "_events_draft|主 session 合流|候选事件见" ccf_venues/<本轮 venue>` 应无正式文档残留；历史更新日志除外。旧统计口径扫描同理：只清理当前正文和总账，历史更新日志可保留当时真实状态。
2. 本轮新增 / 修改的 venue 根 README 与年度 README 不应存在指向不存在本库文件的相对链接；模板目录的占位链接单独按模板规则解释。
3. [TIMELINE.md](./TIMELINE.md) 年份章节按降序，节内事件按日期升序；Mermaid 不含 URL / Markdown 链接。
4. Mermaid label 的 venue edition 必须与表格 Venue 一致，尤其检查 `ICSE`、`FSE`、`ETAPS/TACAS` 等前一年投稿的会议。
5. 对本轮新增 / 修改的会议年度 README，逐一抽查 `Conference dates`：若不是 `未公布` / `⏳ 已检索未公布`，则 [TIMELINE.md](./TIMELINE.md) 必须同时存在对应表格行和 Mermaid `Conference` 行；不要出现 ISSTA 2022/2023 这类年度页有会期但全局时间线缺会期的断链。
6. 本轮新增的会议根 README 人员表必须包含 `官方角色来源`、`主页 / 学术入口`、`代表作 / 近 5 年论文入口`、`核验状态`、`核查时间`；期刊人员表必须保留 `核验等级 / 当前性`。
7. 本轮新增的期刊若存在 `rolling submission`，则 [TIMELINE.md](./TIMELINE.md) 的“期刊滚动投稿 / 未定日期”表必须有对应行；若存在 dated collection / special issue deadline，年度事件表和 Mermaid 必须同步；若无 dated CFP，必须显式写“无已知 active dated CFP”。
8. [SUMMARY.md](./SUMMARY.md) 的统计数字、完成状态、踩坑记录、待补项与实际目录一致；更新日志仍按时间降序。
9. 若复审暴露新的共性坑，先补 [GUIDE.md](./GUIDE.md) / [SUMMARY.md](./SUMMARY.md)，再声称 ready；不得把“下次注意”只留在聊天记录或 PR comment 中。
10. 若当前 PR 合入上游或 base 分支并出现冲突，必须把冲突处理纳入后续复审项：确认上游新增 venue、当前 PR venue、期刊 rolling / dated events、共享规则和更新日志均未被覆盖或回退；同时用 `git status --short` 和 `git ls-files -u` 确认冲突已被 `git add` 标记 resolved，不能只看文本里没有冲突标记。

## 16. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-05 20:56` | PR-6 合流 PR-7 后回写冲突处理纪律：强调合流统计需重算为 30/210，PR-6 / PR-7 facts 必须共存，PR-8 / PR-9 不得误标完成。 |
| `2026-06-05 18:13` | PR-6 踩坑规则回写：补充 SANER/ICSME/ICPC 历史入口与日期冲突、SANER 2022 证书风险、JSEP Wiley WAF/current issue/Early View/rolling 候选口径。 |
| `2026-06-05 18:12` | PR-7 实证 / 质量 venue 规则回写：补充 ESEM historical submission system、Springer Closed collection / historical deadline、ESE 多事件类型、special issue editors 与长期 editorial board 分离，以及 Elsevier / ScienceDirect CLI 403 / WAF 处理纪律。 |
| `2026-06-05 15:59` | 实现后 review 修复：明确 GUIDE §13.1 只是 SUMMARY §9.1 合同摘要，并同步 PR-8 / PR-9 前置条件提示。 |
| `2026-06-05 15:36` | PR-5 全局收口：补充 PR-6~PR-10 stacked execution contract、共享文件增量合流边界、合同外 venue 禁止事项和历史更新日志扫描口径。 |
| `2026-06-05 13:25` | merge upstream / PR-3+PR-4 合流规则：解决 GUIDE 冲突，保留形式化验证会议来源冒充、committee / track 分层、`curl -k` / 冲突复审纪律，同时保留 PR-4 期刊 rolling / dated event、Wiley WAF/403、Springer collections 和 STTT conference-based special issue 计数纪律。 |
| `2026-06-05 12:35` | PR-4 SUMMARY/GUIDE 专项复核：补强 Wiley WAF/403/SPA 壳处理表述，明确需保留官方入口并待人工浏览器核验，不能以第三方页面替代 STVR 当前 roster / guidelines / 卷期正文。 |
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
