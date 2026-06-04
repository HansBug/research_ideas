# `ccf_venues/` SUMMARY

> 信息更新时间：`2026-06-04 18:55`（Asia/Shanghai）

## 1. 当前整体状态

| 项目 | 数量 / 状态 |
|---|---:|
| 文库状态 | 初始化骨架已建立，等待用户确认后进入 P0 强相关 venue 数据填充 |
| 已建立核心文档 | 5 |
| 已建立模板文件 | 4 |
| 已正式完成 venue 目录 | 0 |
| 已正式完成年度 README | 0 |
| 默认调查范围 | 2022 至当前年份 + 2 为默认检索与占位下限；已公布 CFP / important dates 的更远未来年度也必须纳入 |
| 初始化 PR 验收目标 | 骨架路径、模板、TIMELINE 和执行计划完备，可开始后续 P0 数据填充 |
| 当前优先批次 | P0-A 建模 / 需求 / 软工综合；P0-B 形式化验证 / 测试验证 |

说明：当前提交只完成初始化骨架，不把任何待建 venue 冒充为已完成数据。PR body 应作为可执行计划，明确下一阶段优先补齐 P0-A/P0-B 强相关 venue；待初始化自审通过后，应停下等待用户确认再开始实际数据填充。

## 2. 当前可复用的既有资源

| 来源 | 当前用途 | 是否直接搬入 |
|---|---|---|
| [../VENUES.md](../VENUES.md) | 初始 venue 名录、CCF 等级、project 相关性 | 否，作为种子核验 |
| `PR #5 frontier_index/CCF_SE_A_B_C.md` | 软工相关 venue 边界与方向先验 | 否，作为参考 |
| `PR #5 frontier_index/CCF_SE_2026_DEADLINES.md` | deadline 调研字段与官方来源思路 | 否，需重新核验 |
| `PR #5 frontier_index/ccf_history/SUBMISSION_TIMELINES.md` | 近年时间线组织方式参考 | 否，需重新核验 |
| `PR #5 frontier_index/ccf_history/*/metadata/*.json` | 论文数量与 DBLP 计数的候选线索 | 否，只能作交叉核验 |

## 3. P0 强相关 venue 后续填充清单

P0 是“强相关先做完”的后续数据填充边界。初始化 PR 只把清单、模板、TIMELINE 与验收口径固定下来；获得用户确认后，下一阶段应为以下每个 venue 建立根 README，并覆盖 `2022` 至当前年份 + 2 的年度 README，年度表按年份降序排列。

| 目录名 | 类型 | CCF | 主要对应 project | 批次 | 状态 |
|---|---|---|---|---|---|
| `conf-a-icse` | 会议 | A | P1/P2/P3/P4 | P0-A | ⏳ 待建 |
| `conf-a-fse` | 会议 | A | P1/P2/P4 | P0-A | ⏳ 待建 |
| `conf-a-ase` | 会议 | A | P1/P2/P4 | P0-A | ⏳ 待建 |
| `conf-a-issta` | 会议 | A | P2/P3/P4 | P0-A | ⏳ 待建 |
| `journal-a-tse` | 期刊 | A | P1/P2/P3/P4 | P0-A | ⏳ 待建 |
| `journal-a-tosem` | 期刊 | A | P1/P2/P4 | P0-A | ⏳ 待建 |
| `conf-b-models` | 会议 | B | P1/P2/P3 | P0-A | ⏳ 待建 |
| `conf-b-re` | 会议 | B | P1/P2 | P0-A | ⏳ 待建 |
| `journal-b-re` | 期刊 | B | P1/P2 | P0-A | ⏳ 待建 |
| `journal-b-sosym` | 期刊 | B | P1/P3 | P0-A | ⏳ 待建 |
| `conf-a-fm` | 会议 | A | P2/P3 | P0-B | ⏳ 待建 |
| `conf-a-cav` | 会议 | A | P3 | P0-B | ⏳ 待建 |
| `conf-b-etaps` | 会议 | B | P3 | P0-B | ⏳ 待建 |
| `conf-b-vmcai` | 会议 | B | P2/P3 | P0-B | ⏳ 待建 |
| `conf-b-issre` | 会议 | B | P2/P3 | P0-B | ⏳ 待建 |
| `journal-b-stvr` | 期刊 | B | P2/P3 | P0-B | ⏳ 待建 |
| `conf-c-icfem` | 会议 | C | P2/P3 | P0-B | ⏳ 待建 |
| `conf-c-spin` | 会议 | C | P3 | P0-B | ⏳ 待建 |
| `conf-c-atva` | 会议 | C | P3 | P0-B | ⏳ 待建 |
| `conf-c-icst` | 会议 | C | P2/P3/P4 | P0-B | ⏳ 待建 |
| `conf-c-refsq` | 会议 | C | P1/P2 | P0-B | ⏳ 待建 |
| `journal-c-sttt` | 期刊 | C | P3/P4 | P0-B | ⏳ 待建 |

## 4. P1 / P2 后续 venue

以下 venue 不属于初始化 PR 的数据填充目标；后续在 P0 完成后分批推进。

| Venue | 类型 | CCF | 主要价值 | 后续批次 |
|---|---|---|---|---|
| `conf-b-saner` | 会议 | B | 维护、演化、修复 | P1 |
| `conf-b-icsme` | 会议 | B | 维护、演化、修复 | P1 |
| `conf-b-icpc` | 会议 | B | 程序理解、LLM4SE 实证 | P1 |
| `conf-b-esem` | 会议 | B | 实证评估与 benchmark | P1 |
| `journal-b-ese` | 期刊 | B | LLM4SE 实证 | P1 |
| `journal-b-jss` | 期刊 | B | 软工综合、系统案例 | P1 |
| `journal-b-ist` | 期刊 | B | 软工综合、需求/测试 | P1 |
| `journal-b-scp` | 期刊 | B | 形式化、程序与工具链 | P1 |
| `journal-b-jsep` | 期刊 | B | 演化、维护、修复 | P1 |
| `conf-c-qrs` | 会议 | C | 质量、可靠性、安全 | P1 |
| `conf-c-tase` | 会议 | C | 形式化与理论软工 | P1 |
| `journal-c-sqj` | 期刊 | C | 软件质量与评估 | P1 |
| `conf-c-apsec` | 会议 | C | 区域性软工、LLM4SE | P2 |
| `conf-c-seke` | 会议 | C | 知识工程与软工交叉 | P2 |
| `conf-c-ease` | 会议 | C | 实证评估 | P2 |
| `conf-c-msr` | 会议 | C | 仓库挖掘、数据集 | P2 |
| `conf-c-rv` | 会议 | C | 运行时验证 | P2 |

## 5. TIMELINE.md 同步验收口径

[TIMELINE.md](./TIMELINE.md) 是当前 PR 新增的一等入口。后续 P0 venue 数据填充时必须同步满足：

1. `TIMELINE.md` 至少覆盖 `2022` 至当前年份 + 2；若已公布更远未来年度官方信息，也必须新增对应年份章节；年份按降序排列。
2. 每个年份章节包含一张投稿事件总表，表内按时间升序排列。
3. 每个表格事件都必须链接到官方来源或对应年度 README。
4. 每个年份章节包含 Mermaid `gantt` 可视化；单日 deadline 用 `milestone`，多日窗口用普通任务。
5. 期刊 rolling submission 不进入 Mermaid 图；期刊 special issue / topical collection deadline 进入年度时间线。
6. 如果年度事件过多，应拆多张 Mermaid 图，不允许生成难以阅读的超长单图。

## 6. 当前验收口径

初始化完成后逐 venue 数据填充时，默认检查：

1. venue README 顶部有 `信息更新时间`，文末有更新日志表。
2. venue README 的年度汇总表至少覆盖 `2022` 至当前年份 + 2；若已公布更远未来年度官方信息，也必须继续纳入；按年份降序排列。
3. 每个年份行都能跳转到年度 README。
4. 每个年份行都包含官方年度主页链接；若未找到，明确写 `待补` 或 `⏳ 待官网`。
5. 已结束会议必须尽量包含论文数量和论文名录链接；若只能用 `DBLP`，必须注明 fallback 口径。
6. 尚未召开的会议只要能找到官方主页、`CFP` 或 important dates，也必须入表。
7. 所有关键时间精确到分钟；官方只给日期时必须显式标注 `待补时刻`；官方给 `AoE` 时保留原时区。
8. 会议和期刊使用不同结构，不能把期刊硬写成会议式 ddl 表。
9. 证据链接优先官方来源，`DBLP` 仅作论文名录 fallback 或核验。
10. [SUMMARY.md](./SUMMARY.md) 统计数字与实际目录保持一致。
11. PR body 必须区分“初始化已完成骨架”和“后续计划补齐数据”，不得把待建 venue 写成已完成。

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-04 18:55` | 明确默认未来检索/占位下限为当前年份 + 2（当前到 2028），更远未来若已有官方 CFP / important dates 也必须纳入。 |
