# `ccf_venues/` GUIDE

> 信息更新时间：`2026-06-04 23:04`（Asia/Shanghai）

## 1. 目标与任务边界

`ccf_venues/` 维护的是 `CCF` 相关会议 / 期刊的 venue 情报，而不是单篇论文全文库。

本库应做：

1. 固定和本仓库 project 相关的 venue 范围。
2. 维护每个 venue 的稳定信息：官方主页、scope、出版方、CCF 等级、project 相关性。
3. 维护自 `2022` 年以来每个年度的官方主页、`CFP` / important dates、submission system、program / accepted papers、proceedings / volume issue、论文名录入口和论文数量，并把这些入口以 Markdown 超链接挂进表格。
4. 对尚未召开但已有官方信息的年度，记录当前状态和关键 ddl。
5. 维护 [TIMELINE.md](./TIMELINE.md)，按年份汇总跨 venue 投稿相关 important dates。
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
2. 若官方给出 timezone，必须保留 timezone，例如 `2026-01-15 23:59 AoE`。
3. 若官方给出多个时区，以官方原文为准，不擅自换算；如需换算，另加一列 `北京时间换算`。
4. `信息更新时间` 与 `更新日志` 也统一精确到分钟，不写秒。
5. 所有名为“更新日志”的表格必须按时间降序排列，最新记录放在表头后的第一行；新增日志时不得简单追加到表格末尾。若本轮修改触及某个文件，必须顺手校正该文件更新日志顺序。

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

### 5.3 Markdown 链接写法

1. 已找到 URL 时，表格中直接写 Markdown 链接，例如 `[ICSE 2026](https://conf.researchr.org/home/icse-2026)`。
2. 本库内部页使用相对路径，例如 [`2026`](./2026/README.md)、[TIMELINE.md](../TIMELINE.md)。
3. 未找到 URL 时不要伪造链接，写 `待补`、`未公布`、`无已知` 或 `⏳ 已检索未公布`，并在证据 / 核查记录里写核查时间。
4. 模板中的外部 URL 占位符不得写成 Markdown 链接；统一写 `待补（占位：OFFICIAL_URL；核验后改为 Markdown 链接）`。这样能避免模板被误读为已有可点击事实来源。
5. 模板中的本库内部已知路径必须继续写相对 Markdown 链接，例如 [TIMELINE.md](./TIMELINE.md)、[2026](./2026/README.md)；不要把内部已知路径降级成纯文本。
6. 第三方聚合页只能放在备注或 fallback，不得放进“官方来源”列。

### 5.4 核心人员情报规范

核心人员情报是本库的一等学术情报，不是可选备注。它服务于后续判断 venue 的研究共同体、审稿偏好、主题连续性和潜在投稿适配度。

会议根 README 应维护“核心人员情报”小节。默认覆盖：

1. 当前 / 未来年度 General Chair、Program Chair、Research Track Chair、Technical Track Chair、Artifact / Tool / SEIP 等与本仓库 project 强相关 track 的 chair。
2. Steering Committee / Advisory Board / Organizing Committee leadership。
3. 在相关 track 或历年组织中反复出现、且与本仓库 project 强相关的领域权威。
4. 对 umbrella venue，例如 ETAPS，应区分 umbrella 层级、main conference / satellite conference 层级和具体 track 层级；不要把 TACAS chair、ETAPS general chair 和 workshop organizer 混写成同一类角色。

会议人员表至少包含：姓名、年度 / 层级、会议角色、单位、官方角色来源、主页或学术入口、主要研究方向、代表作或近 5 年论文入口、与本仓库 project 的关系、核验状态、核查时间。人员事实应优先来自官方 committee / track 页面；研究方向和代表作可来自主页、DBLP 或学术入口，但必须说明是公开资料判断。

期刊根 README 应维护“核心编辑人员情报”小节。默认覆盖 Editor-in-Chief / Editors-in-Chief、Co-Editor-in-Chief、Associate / Area Editor-in-Chief、Managing Editor、Editorial Board leadership、与本仓库强相关的 editorial board 成员，以及当年 special issue / topical collection guest editor。期刊人员表必须保留 `核验等级 / 当前性` 列，区分官方当前 roster、官方公告、个人 / 机构页候选线索和 legacy / 运营线索。

完整人员表放在各 venue 根 README；[SUMMARY.md](./SUMMARY.md) 只记录覆盖状态、主要缺口和跨 PR 合流提示，不复制全量人员表。

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
| 会期 | 起止日期或日期时间；根表建议写 `yyyy-mm-dd..yyyy-mm-dd`，跨年或多地会议须在备注中解释 |
| 论文数量 | 仅已召开且可核验时填写；必须在备注或年度 README 写明计数口径，例如 research papers、all accepted papers、main conference only、DBLP `entry article` baseline |
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
5. Mermaid 更新后必须至少人工预览；若本地具备 Mermaid CLI，可补充渲染检查。

### 11.4 同步规则

1. 新增或修改任何年度 README 中的投稿相关 important date 后，必须同步检查 [TIMELINE.md](./TIMELINE.md)。
2. 若某个时间点因官方来源冲突被标为 `⚠️ 矛盾待解`，TIMELINE 表格也必须保留该状态，不得只在 venue 年度 README 中记录。
3. [TIMELINE.md](./TIMELINE.md) 只汇总已进入本库的 venue，不替代 P1/P2 待补清单。
4. PR-1A / 会议填充负责维护会议 dated events；PR-1B / 期刊填充负责维护期刊 rolling 表和期刊 special issue dated events。并行 PR 合并时不得互相删除对方已经核验的事件行。

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
9. 回填 [SUMMARY.md](./SUMMARY.md) 的覆盖进度、核心人员覆盖状态和待补清单。
10. 检查所有链接可点击、所有时间精确到分钟、所有状态符合口径，且 Mermaid 语法可预览。
11. 在相关 README 文末更新日志中按时间降序插入记录。

## 14. PR-1A / PR-1B 并行合流协议

本库已经进入会议试点 PR-1A 与期刊试点 PR-1B 并行阶段。两个 PR 都会修改 [GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[TIMELINE.md](./TIMELINE.md) 和 [templates/](./templates/)，因此合并时必须遵守以下协议：

1. **共享规范优先**：时间格式、更新日志降序、Markdown 链接占位、核心 URL、核心人员情报、TIMELINE 事件年份规则属于共享规范；任一 PR 修正后，另一 PR 只吸收协议层，不复制对方事实表。
2. **事实 ownership 分离**：PR-1A 负责会议事实、会议年度 README、会议核心人员和会议 dated events；PR-1B 负责期刊事实、期刊年度 README、期刊核心编辑人员、期刊 rolling 表和期刊 special issue dated events。
3. **SUMMARY 不互相回退**：PR-1A 已填充的会议不得被 PR-1B 写回 `⏳ 待建`；PR-1B 已填充的期刊不得被 PR-1A 写回 `⏳ 待建`。并行期间若本 PR 不拥有对方事实，状态写“由 PR-1A/PR-1B 负责，本 PR 不覆盖”。
4. **TIMELINE 不互相删除**：会议 dated events、期刊 rolling 表和 SoSyM Industry 5.0 dated events 合并后必须共存；冲突解决时以“事件发生年份 + 来源可点击 + owner 不互删”为准。
5. **模板统一协议**：外部 URL 占位符使用纯文本占位，内部已知路径使用相对 Markdown 链接；更新日志提示统一为“更新日志按时间降序排列，最新记录置于最上方。”。
6. **试点踩坑保留边界**：PR-1A 的会议踩坑和 PR-1B 的期刊踩坑都应保留，但不得把对方试点的具体 deadline、论文数量或人员 roster 复制到本 PR 的事实表。

## 15. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-04 23:04` | 吸收 PR-1A 合流协议：明确会议 / 期刊核心人员分轨、TIMELINE 事件发生年份规则、模板占位链接规则和并行 PR 事实 ownership。 |
| `2026-06-04 22:05` | 根据正式复审补充期刊核心编辑人员的核验等级 / 当前性规则，明确候选线索和 legacy 运营线索不得写成当前 roster。 |
| `2026-06-04 21:30` | 补充全库更新日志降序规则，并新增期刊核心编辑人员情报规则：期刊 PR 必须核验核心编辑的研究方向、代表作和近 5 年论文入口。 |
| `2026-06-04 19:37` | 新增核心 URL 字段与 Markdown 超链接规范，要求 venue 根表、年度页和 TIMELINE 都挂可点击链接。 |
| `2026-06-04 18:55` | 明确后续搜索必须至少到当前年份 + 2；当前初始化覆盖到 2028，更远未来若已有官方信息也继续纳入。 |
