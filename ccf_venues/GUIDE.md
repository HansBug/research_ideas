# `ccf_venues/` GUIDE

> 信息更新时间：`2026-06-04 21:55`（Asia/Shanghai）

## 1. 目标与任务边界

`ccf_venues/` 维护的是 `CCF` 相关会议 / 期刊的 venue 情报，而不是单篇论文全文库。

本库应做：

1. 固定和本仓库 project 相关的 venue 范围。
2. 维护每个 venue 的稳定信息：官方主页、scope、出版方、CCF 等级、project 相关性。
3. 维护自 `2022` 年以来每个年度的官方主页、`CFP` / important dates、submission system、program / accepted papers、proceedings / volume issue、论文名录入口和论文数量，并把这些入口以 Markdown 超链接挂进表格。
4. 对尚未召开但已有官方信息的年度，记录当前状态和关键 ddl。
5. 维护 [TIMELINE.md](./TIMELINE.md)，按年份汇总跨 venue 投稿相关 important dates。
6. 给后续论文初筛、投稿计划、前沿追踪提供稳定入口。
7. 维护每个 venue 的核心人员情报，帮助后续判断该 venue 当前技术风向、评审偏好、社区权威和潜在相关工作入口。

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
5. 所有 `更新日志` 表格必须按时间降序排列，最新修改在最上方；新增日志时先插入表格第一条，不要追加到末尾。

## 4. 来源优先级

### 4.1 会议来源优先级

1. 官方年度主页，例如 `conf.researchr.org/home/icse-2026`。
2. 官方 `Call for Papers` / `Important Dates` / track page。
3. 官方 proceedings 页面，例如 ACM DL、IEEE Xplore、Springer LNCS、Dagstuhl、USENIX 官方页。
4. `DBLP` 年度页面，用于论文名录 fallback 或交叉核验。
5. 其他第三方页面只可作为发现线索，不能作为最终证据。

### 4.2 期刊来源优先级

1. 期刊官方主页。
2. 官方 author guidelines / submission guidelines。
3. 出版商 volume / issue / articles in press / online first 页面。
4. 官方 special issue `CFP` 页面。
5. `DBLP` 年度页面，用于年度论文名录 fallback 或计数核验。


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
2. 本库内部页使用相对路径，例如 [conf-a-icse/2026/README.md](./conf-a-icse/2026/README.md)、[TIMELINE.md](./TIMELINE.md)。模板中已经能确定的内部路径（如 `./2028/README.md`、`../../TIMELINE.md`）也必须写成相对 Markdown 链接，不能退化为代码样式。
3. 模板里的外部 URL 占位符不得写成 Markdown 链接；应写 `待补（占位：OFFICIAL_YEAR_HOME_URL）` 这类纯文本。只有实例化并核验真实 URL 后，才允许改为 `[label](url)`。
4. 未找到 URL 时不要伪造链接，写 `待补`、`未公布`、`无已知` 或 `⏳ 已检索未公布`，并在证据 / 核查记录里写核查时间.
5. 第三方聚合页只能放在备注或 fallback，不得放进“官方来源”列。

### 5.4 核心人员情报规范

每个 venue 根 README 必须维护“核心人员情报”小节；年度 README 可在组织委员会变化较大时补充年度人员页链接，但默认不要求逐年复制完整人员表。

#### 5.4.1 会议人员字段

会议至少覆盖以下对象：

1. 当前年份、当前年份 +1、当前年份 +2 中已经公开的 `General Chair` / `Program Chair` / `Research Track Chair` / `PC Chair`。
2. `Steering Committee` 的 chair / co-chair / 与本仓库 project 强相关成员。
3. 对该 venue 技术风向影响明显、且与本仓库 P1/P2/P3/P4 强相关的领域权威。
4. 若 venue 是 umbrella venue（例如 ETAPS / TACAS），必须显式说明人员是 umbrella 层面还是分会 / track 层面。

会议人员表推荐字段：

| 字段 | 说明 |
|---|---|
| 人员 | 姓名；如官方拼写与 DBLP 拼写不一致，必须备注 |
| 角色 / 年度 | 例如 `2027 PC Chair`、`Steering Committee Chair` |
| 官方角色来源 | 官方 committee / track / steering 页面链接 |
| 主要研究方向 | 基于官方简介、个人主页、DBLP 近年论文归纳；推断必须写明 |
| 代表作 / 近年论文线索 | 1-3 条可点击链接，优先 DBLP / DOI / 出版页 / 个人论文页 |
| 与本仓库关系 | 明确对应 P1/P2/P3/P4 或 project_ex1 |
| 待深挖 | 当前证据缺口、需要后续追踪的论文或角色 |

#### 5.4.2 期刊人员字段

期刊至少覆盖：

1. `Editor-in-Chief` / `Co-Editor-in-Chief`。
2. 与本仓库方向强相关的 `Associate Editor` / `Editorial Board` 成员。
3. Special issue / topical collection 的 guest editor（若该 special issue 与本仓库相关）。

期刊人员表字段可沿用会议人员表，但 `角色 / 年度` 应写成编辑角色、任期或核查年份。

#### 5.4.3 来源与维护要求

1. 官方 committee / editorial board 页面是角色真源；DBLP / 个人主页只用于研究方向与论文线索。
2. 不得凭姓名相似直接合并人物；同名作者必须用机构、ORCID、个人主页或 DBLP pid 消歧。
3. 研究方向可以归纳，但必须保留“基于公开主页 / DBLP 近年论文推断”的证据链；不确定时写 `待核验`。
4. 人员信息至少在每次年度 CFP / committee 更新时复核一次；新增年份时同步检查人员表是否需要更新。
5. `SUMMARY.md` 只放核心人员覆盖状态和高层观察，完整人员表放在各 venue 根 README。

## 6. 会议 README 结构规范

每个会议根 README 必须包含：

1. 顶部 `信息更新时间`。
2. 基本信息：缩写、全称、CCF 大类与等级、出版方、官方 series page、DBLP venue page。
3. 官方 scope 与研究方向摘要。
4. 与本仓库 project 的相关性表。
5. 核心人员情报：组织者、PC / Research Track chair、Steering Committee、领域权威、研究方向、代表作 / 近年论文线索。
6. `2022` 年以来年度汇总表，按年份降序排列。
7. 文末更新日志表，按时间降序排列。

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
| 会期 | 起止日期或日期时间；根 README 年度汇总表统一使用 `yyyy-mm-dd..yyyy-mm-dd`，TIMELINE 表格可用 `至` 表达人类可读区间 |
| 论文数量 | 仅已召开且可核验时填写；根 README 必须在单元格内携带计数口径，例如 `Research Track: 245`、`DBLP inproceedings: 27`、`ETAPS umbrella: 138；TACAS: 56` |
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
9. 文末更新日志表，按时间降序排列。

## 8. 期刊 README 结构规范

期刊没有会议式年度 ddl，因此期刊根 README 应改用期刊结构，至少包含：

1. 顶部 `信息更新时间`。
2. 基本信息：缩写、全称、CCF 大类与等级、出版商、ISSN、主页、author guidelines、submission system。
3. Scope 与栏目类型。
4. 投稿模式：rolling submission、special issue、open access / hybrid、article type。
5. 与本仓库 project 的相关性表。
6. `2022` 年以来年度汇总表，按年份降序排列。
7. 文末更新日志表。

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
8. 文末更新日志表，按时间降序排列。

## 10. 阶段状态口径

会议推荐状态：

| 状态 | 使用场景 |
|---|---|
| `⏳ 待官网` | 尚未找到官方年度主页 |
| `🟦 已有主页` | 已有年度主页，但尚未公布完整 CFP / 日期 |
| `🟢 投稿中` | 投稿窗口尚未关闭 |
| `🟡 已截稿` | submission 已截止，等待审稿 / rebuttal |
| `🟡 审稿中` | submission / response 已截止，等待 notification 或最终决定 |
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
2. 每个年份章节内先写投稿事件总表，再写 Mermaid 可视化。
3. 同一年表格内的事件必须按日期时间升序排列。
4. 当前年份 + 1 和当前年份 + 2 的章节必须存在，并在实际检索后记录 `⏳ 已检索未公布` 或可用官方信息；更远未来年度一旦能找到官方主页、`CFP` 或 important dates，就必须新增对应年份章节。

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

## 12. 初始化 PR 自审流程

当任务是“先开初始化 PR，不填实际 venue 数据”时，必须按以下顺序自审：

1. 确认 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[TIMELINE.md](./TIMELINE.md)、[01-venue-scope.md](./01-venue-scope.md) 和 [templates/](./templates/) 均已存在。
2. 确认 PR body 是可执行计划，包含目标、骨架交付物、P0/P1/P2 分批、TIMELINE 同步规则、验收标准、已知限制和下一步停靠点。
3. 确认 PR body / DoD 显式包含更新日志降序、核心 URL 可点击、核心人员情报、`SUMMARY.md` 覆盖状态与 `TIMELINE.md` 同步验收项。
4. 确认 `SUMMARY.md` 不声称任何未建 venue 已完成，并已为已建 venue 记录核心人员覆盖状态或待补状态。
5. 确认模板中的相对链接在未来实际 venue 路径下可成立。
6. 确认 Mermaid 代码块使用 GitHub 较稳定的 `gantt` 语法，不使用实验性 `timeline` 作为主图。
7. 完成自审后停止，等待用户确认是否进入 P0 数据填充。

## 13. 一轮数据填充流程

1. 先读 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
2. 根据 [01-venue-scope.md](./01-venue-scope.md) 选择本轮 venue。
3. 新建或更新 `<conf|journal>-<rank>-<slug>/README.md`。
4. 从最新年份开始，按降序补年度 README，默认覆盖到 `2022`。
5. 回填上级 venue README 的年度汇总表。
6. 若更新内容涉及投稿相关 important date，同步回填 [TIMELINE.md](./TIMELINE.md) 的年度表格与 Mermaid Gantt；事件行必须包含事件官方来源、年度主页、本库年度页，已结束年度还应尽量包含论文集 / 论文名录链接。
7. 回填 [SUMMARY.md](./SUMMARY.md) 的覆盖进度、核心人员情报覆盖状态和待补清单。
8. 检查所有链接可点击、所有时间精确到分钟、所有状态符合口径，核心人员表包含官方角色来源、研究方向、代表作 / 近年论文线索，且 Mermaid 语法可预览。
9. 在相关 README 文末更新日志表首行插入记录，并保持时间降序。

## 14. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-04 22:20` | 明确模板外部 URL 占位不得伪造 Markdown 链接，内部已知路径仍必须使用相对 Markdown 链接；统一会议根表会期和论文数量口径。 |
| `2026-06-04 21:55` | 修正数据填充流程中的更新日志写法，补充 PR 自审与 `SUMMARY.md` 核心人员覆盖验收项。 |
| `2026-06-04 21:44` | 补充核心人员情报规范，并明确所有更新日志表格必须按时间降序排列。 |
| `2026-06-04 21:10` | 根据 PR-1A 会议试点补充事件发生年份时间线口径、`🟡 审稿中` 阶段状态，并修正模板占位链接为代码样式。 |
| `2026-06-04 19:37` | 新增核心 URL 字段与 Markdown 超链接规范，要求 venue 根表、年度页和 TIMELINE 都挂可点击链接。 |
| `2026-06-04 18:55` | 明确后续搜索必须至少到当前年份 + 2；当前初始化覆盖到 2028，更远未来若已有官方信息也继续纳入。 |
