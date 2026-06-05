# `ccf_venues/` README

> 信息更新时间：`2026-06-05 15:59`（Asia/Shanghai）

## 1. 路径定位

`ccf_venues/` 是本仓库面向 `CCF` 相关会议与期刊的 **venue 情报库**。它服务于博士研究四个 project 的长期选题、投稿、论文检索与前沿追踪，不直接承担单篇论文全文收录职责。

本路径重点维护：

1. 与本仓库四个 project 强相关或中相关的 `CCF` 会议 / 期刊基本信息。
2. 每个 venue 的研究方向、官方入口、出版入口、`DBLP` 入口和 project 相关性。
3. 自 `2022` 年以来每一年的年度主页、`CFP` / important dates / author guidelines、submission system、program / accepted papers、proceedings / volume issue、论文名录页面和论文数量，并在表格中直接挂可点击超链接。
4. 尚未召开但已经能找到官方年度主页、`CFP` 或 important dates 的未来年度信息。
5. 以 [TIMELINE.md](./TIMELINE.md) 按事件发生年份串联所有投稿相关 important dates，形成跨 venue 时间线。
6. 每个会议 / 期刊的核心人员情报：组织委员会、PC / Research Track chair、Steering Committee、领域权威及其研究方向、代表作、近年论文线索。
7. venue 当前阶段状态，例如投稿中、已截稿、审稿中、通知后、会期临近、已结束、期刊滚动开放等。

换言之，这里回答的问题是：**哪些 CCF venue 值得持续盯、每一年官网与关键时间点在哪里、什么时候该准备投稿、年度论文入口 / 论文集 / 期刊卷期入口在哪里、谁是该 venue 当前最值得关注的组织者 / PC / 领域权威，并能直接从表格点击跳转。**

## 2. 与现有材料的关系

当前 `main` 分支已有 [../VENUES.md](../VENUES.md)，它是面向毕业与投稿选择的 venue 总览；`ccf_venues/` 则进一步把 venue 拆成可长期维护的事实情报库。

后续可参考但不直接照搬的历史资源包括：

1. [../VENUES.md](../VENUES.md)：提供强相关 venue 的初始名录、CCF 等级和四个 project 的投稿相关性。
2. 历史 PR #5 中的 `frontier_index/CCF_SE_A_B_C.md`：可作为软工相关 venue 范围和方向边界的参考来源；当前分支没有该路径，不能当作可点击仓库文件。
3. 历史 PR #5 中的 `frontier_index/CCF_SE_2026_DEADLINES.md` 与 `frontier_index/ccf_history/SUBMISSION_TIMELINES.md`：可作为 deadline 调研思路参考；当前分支没有这些路径，不能无核验地整表搬入。

## 3. CCF 官方来源基准

本库的 CCF 等级与官方缩写默认以以下页面为准：

1. CCF 软件工程 / 系统软件 / 程序设计语言目录：<https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>
2. CCF 计算机科学理论目录：<https://www.ccf.org.cn/Academic_Evaluation/TCS/>
3. CCF 推荐目录更新 / 更名通知：<https://www.ccf.org.cn/Academic_Evaluation/By_category/2024-06-28/825349.shtml>

若 [../VENUES.md](../VENUES.md)、`PR #5` 或其他旧材料与 CCF 官方页面冲突，以当前官方页面为准，并在具体 venue README 的“证据与核查记录”中说明差异。

## 4. 收录范围

### 4.1 初始优先范围

本库优先覆盖和下列 project 直接相关的 CCF venue：

1. `project_1`：LLM 状态机结构化建模、需求到模型、`MDE`、`SysML/UML`、状态机生成。
2. `project_2`：验证场景生成、性质生成、`LTL/CTL`、自然语言到规约。
3. `project_3`：模型检查、时间自动机、`UPPAAL`、验证剖面、形式化验证。
4. `project_4`：模型修复、程序/规约修复、反例驱动修复、维护与演化。

### 4.2 时间范围

默认调查 `2022` 年至**当前年份 + 2**；以当前日期 `2026-06-05` 为例，初始化骨架应覆盖到 `2028` 年。`当前年份 + 2` 是默认检索与占位下限，不是未来年度上限；若任何 venue 已经能找到 `2029` 或更远年份的官方年度主页、`CFP`、important dates 或投稿入口，也必须继续纳入。

1. 已经结束的年度：记录年度主页、重要时间点、论文名录页面和论文数量。
2. 当前年份、未来两年和更远已公布未来年度：只要已经公布官网、`CFP` 或 important dates，就记录官方主页、关键时间点和当前阶段。
3. 当前年份 + 1 / 当前年份 + 2 尚未找到官方主页时：仍保留年度占位，并在上级 venue README / [TIMELINE.md](./TIMELINE.md) 中标记为 `⏳ 待官网` 或 `⏳ 已检索未公布`，不伪造日期。
4. 当前年份 + 3 或更远年度：没有官方信息时不强制占位；一旦有官方信息，必须新增年度 README、venue 汇总行和 [TIMELINE.md](./TIMELINE.md) 年份章节。

### 4.3 不收录内容

1. 不收录单篇论文全文、`paper.pdf` 或 `paper_content.txt`。
2. 不把博客、新闻、第三方倒计时网站作为主证据。
3. 不为缺失年份编造主页、`CFP`、投稿时间或论文数量。
4. 不把 `DBLP` 当作会议官方主页；`DBLP` 只可作为论文名录 / bibliographic fallback。

### 4.4 试点后维护边界

当前情报库已完成 6 个会议 / 期刊试点 venue、PR-2 的 5 个软工 / 需求会议 venue、PR-3 的 8 个形式化 / 验证会议 venue、PR-4 的 3 个剩余 P0 期刊 venue 的基础建档与部分核验；merge-upstream 合流后共有 22 个 venue 根 README、154 个年度 README。PR-3 本轮交付物仍按 8 个目标 venue 计数，即 8 个根 README + 56 个年度 README = 64 个 README；PR-4 本轮交付物仍按 3 个目标期刊 venue 计数，即 3 个根 README + 21 个年度 README = 24 个 README。PR-5 后进入“P0 已建档事实维护 + P1/P2 按冻结合同分批扩展”的长期维护阶段：PR-6 / PR-7 / PR-8 / PR-9 分别承担 P1/P2 venue 数据填充，PR-10 在这些分支全部合入后做 P1/P2 全局审计。新增或修改 venue 时必须以 [SUMMARY.md](./SUMMARY.md)、[TIMELINE.md](./TIMELINE.md) 与对应模板为同步边界，不得把待建 venue、未公布年度、未核验论文数量或候选人员线索写成已完成事实；任何 merge-upstream / base 合流后的冲突解决都必须复审 PR-2 / PR-3 / PR-4 venue、期刊 rolling / dated events、共享规则和更新日志是否共存，防止回退到旧目录统计口径。

## 5. 目录命名规范

每个 venue 使用一个子路径，目录名统一为：

```text
<conf|journal>-<a|b|c>-<slug>
```

示例：

1. `conf-a-icse`
2. `conf-a-ase`
3. `conf-b-models`
4. `conf-b-re`
5. `conf-c-refsq`
6. `journal-a-tse`
7. `journal-b-sosym`
8. `journal-b-re`
9. `journal-c-sttt`

若 venue 属于 CCF 理论类、交叉类或国内高质量目录，但仍纳入本库，目录名仍先按等价 A/B/C 档记录，具体 CCF 大类写在 venue README 的元信息字段中。


## 6. 核心 URL 与超链接要求

本库不是只记录“有 / 无”的静态目录，而是可直接点击使用的情报入口。后续任何 venue 数据填充 PR 都必须满足：

1. **venue 根 README 的年度汇总表必须直接挂核心 URL**：会议至少包含官方年度主页、CFP、Important Dates、submission system、program / accepted papers、proceedings、DBLP 年度页；期刊至少包含期刊主页、author guidelines、submission system、special issue / topical collection、volume / issue、online first / articles in press、DBLP 年度页。
2. **年度 README 必须集中维护年度核心 URL 索引**：当年主页、CFP / dates、投稿系统、论文集 / 论文名录或期刊卷期入口、DBLP fallback 都要有独立表格字段，不能只散落在正文。
3. **TIMELINE.md 的事件行必须保留可点击来源链**：每条 dated event 至少链接事件官方来源和本库年度 README；若会议已结束或论文入口已发布，应同时挂年度主页、论文集 / 论文名录链接。
4. **缺失链接要显式标注**：未公布写 `未公布`，已检索未找到写 `⏳ 已检索未公布`，待人工补证写 `待补`；不得留空，也不得把第三方聚合页伪装成官方来源。
5. **链接优先级必须清楚**：官方页面优先；出版商页面用于 proceedings / volume issue；DBLP 只能作论文名录或计数 fallback；PR #5 和旧材料只作发现线索。
6. **核心人员情报必须可追溯**：会议至少记录当前 / 未来年度 General Chair、Program / Research Track Chair、Steering Committee 与本仓库强相关的领域权威；期刊至少记录 Editor-in-Chief、Co-Editor-in-Chief、Associate / Area Editor-in-Chief、Managing Editor、Editorial Board leadership 与相关 special issue guest editor，并给出官方角色页、个人主页或 DBLP / Google Scholar 等来源；期刊人员必须保留 `核验等级 / 当前性`。

## 7. 标准目录结构

```text
ccf_venues/
├── README.md
├── GUIDE.md
├── SUMMARY.md
├── TIMELINE.md
├── 01-venue-scope.md
├── templates/
│   ├── conference-venue-readme-template.md
│   ├── conference-year-readme-template.md
│   ├── journal-venue-readme-template.md
│   └── journal-year-readme-template.md
├── conf-a-icse/
│   ├── README.md
│   ├── 2028/README.md
│   ├── 2027/README.md
│   ├── 2026/README.md
│   ├── 2025/README.md
│   └── 2024/README.md
└── journal-b-sosym/
    ├── README.md
    ├── 2028/README.md
    ├── 2027/README.md
    ├── 2026/README.md
    └── 2025/README.md
```

## 8. 文件说明

1. [README.md](./README.md)
   - 本库定位、范围、命名规则和入口说明。
2. [GUIDE.md](./GUIDE.md)
   - 后续调研、记录、核验、排序、状态标记和更新日志规范。
3. [SUMMARY.md](./SUMMARY.md)
   - 当前总账、优先级、覆盖进度、状态口径和后续批次。
4. [TIMELINE.md](./TIMELINE.md)
   - 按年份汇总所有 venue 的投稿相关 important dates，并用表格 + Mermaid Gantt 形成跨 venue 时间线。
5. [01-venue-scope.md](./01-venue-scope.md)
   - 初始强相关 venue 范围、分批策略和暂缓收录清单。
6. [templates/](./templates/)
   - 会议 / 期刊的 venue README 与年度 README 模板。
7. `conf-a-icse/`、`journal-b-sosym/` 等 venue 子路径
   - 每个会议或期刊一个子路径；每个年度一个子目录。

## 9. AI 工作入口提示

涉及本库的任务默认按以下顺序阅读：

1. 先读 [README.md](./README.md)，明确范围与目录命名。
2. 再读 [GUIDE.md](./GUIDE.md)，明确字段、时间、来源和状态规范。
3. 再读 [SUMMARY.md](./SUMMARY.md)，了解当前覆盖进度和下一批优先级。
4. 若任务涉及投稿 ddl 或年度时间规划，再读 [TIMELINE.md](./TIMELINE.md)。
5. 若要新增 venue，先查 [01-venue-scope.md](./01-venue-scope.md)，确认是否属于当前批次。
6. 最后进入 `<conf|journal>-<rank>-<slug>/` 维护具体 venue。
7. 若任务属于 P1/P2 扩展，必须先查 [SUMMARY.md](./SUMMARY.md) §9 与 [01-venue-scope.md](./01-venue-scope.md) 中 PR-6~PR-10 的 ownership；不得跨 PR 新增或修改其他批次 venue 目录。

会议与期刊数据合流时，会议事实、会议核心人员、会议 dated events、期刊事实、期刊核心编辑人员、期刊 rolling 表和期刊 special issue dated events 必须共存；共享规范可统一吸收，但任何一类事实表不得被另一类空白占位覆盖或回退。

若当前 PR 合入上游 / base 后出现共享文件冲突，冲突解决本身必须进入复审范围：确认上游新增 venue、当前 PR venue、期刊 rolling / dated events、共享规则和更新日志均未被覆盖或回退，并在 `git status` / `git ls-files -u` 层面确认冲突已标记 resolved。

## 10. 更新日志

> 更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-05 15:59` | 实现后 review 修复：将 README 历史 PR #5 / `frontier_index` 资源口径与 SUMMARY 对齐，明确这些路径不是当前分支可点击文件。 |
| `2026-06-05 15:36` | PR-5 全局收口：冻结 P1/P2 后续 PR-6~PR-10 ownership，明确 P0 22 个 venue / 154 个年度 README 进入长期维护状态，并把后续扩展入口指向 SUMMARY / scope 合同。 |
| `2026-06-05 14:06` | 修复 PR #46 review 入口口径：将 merge-upstream 后当前状态统一为 22 个 venue 根 README、154 个年度 README，并同时保留 PR-3 / PR-4 本轮交付计数和共享文件合流复审纪律。 |
| `2026-06-05 11:25` | 合并上游 PR-2 后更新入口状态：记录 PR-3 当时的合流目录统计，明确 PR-3 自身交付物仍是 8 个 venue / 64 个 README，并把 upstream merge 冲突解决纳入后续复审纪律；当前总量以 14:06 记录的 22 / 154 为准。 |
| `2026-06-05 08:46` | 完成 PR-2 后更新入口状态：说明 6 个试点 venue 与 5 个软工 / 需求会议 venue 均已基础建档，后续进入已建档事实维护与批量扩展阶段。 |
| `2026-06-05 01:08` | 修复合流后入口仍保留“只建骨架”的旧初始化口径，改为试点后长期维护边界。 |
| `2026-06-05 00:36` | 合入期刊试点后完成会议 / 期刊合流：正文改为长期维护规则，保留会议与期刊事实共存、核心人员分轨、TIMELINE 事件发生年份和更新日志降序口径。 |
| `2026-06-04 23:04` | 吸收 PR-1A / PR-1B 合流协议：TIMELINE 改按事件发生年份，会议 / 期刊核心人员分轨，期刊人员保留 `核验等级 / 当前性`，并明确并行 PR 事实 owner 不互相覆盖。 |
| `2026-06-04 22:20` | 明确模板占位链接、根表计数口径与年度更新日志提示的 review 修复要求。 |
| `2026-06-04 21:55` | 将核心人员情报和更新日志降序要求同步为本库入口级维护口径。 |
| `2026-06-04 21:42` | 补充核心人员情报的收录目标，要求每个 venue 维护组织者、PC / Steering 与领域权威的可追溯信息。 |
| `2026-06-04 19:37` | 补充 venue 根 README、年度 README 与 TIMELINE 必须直接挂核心 URL / Markdown 超链接的要求。 |
| `2026-06-04 18:55` | 明确默认未来检索/占位下限为当前年份 + 2（当前到 2028），更远未来若已有官方 CFP / important dates 也必须纳入。 |
