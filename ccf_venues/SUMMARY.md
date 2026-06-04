# `ccf_venues/` SUMMARY

> 信息更新时间：`2026-06-04 22:20`（Asia/Shanghai）

## 1. 当前整体状态

| 项目 | 数量 / 状态 |
|---|---:|
| 文库状态 | PR-1A 会议试点数据已填充，等待实现 review 与后续迭代 |
| 已建立核心文档 | 5 |
| 已建立模板文件 | 4 |
| 已正式完成 venue 目录 | 3 |
| 已正式完成年度 README | 21 |
| 本轮新增 venue | 3：[`conf-a-icse`](./conf-a-icse/README.md)、[`conf-b-models`](./conf-b-models/README.md)、[`conf-b-etaps`](./conf-b-etaps/README.md) |
| 默认调查范围 | 2022 至当前年份 + 2 为默认检索与占位下限；已公布 CFP / important dates 的更远未来年度也必须纳入 |
| TIMELINE 状态 | 已按事件发生年份回填 2022-2028 的 PR-1A 会议时间线，见 [TIMELINE.md](./TIMELINE.md) |
| 核心人员情报状态 | PR-1A 三个会议根 README 已补“核心人员情报”表；完整人员表在各 venue 根 README，SUMMARY 仅保留覆盖状态和高层观察 |
| 当前优先批次 | PR-1B 期刊试点与后续 P0 批量 venue，需依赖 PR-1A review 结论 |

说明：PR-1A 只覆盖 3 个会议试点，不代表 P0 全量完成。后续 PR 必须继续按 [GUIDE.md](./GUIDE.md) 的核心 URL、时间格式、状态口径和 [TIMELINE.md](./TIMELINE.md) 同步规则维护。

## 2. PR-1A 会议试点完成情况

| Venue | CCF | 年度范围 | 根 README | 年度 README | TIMELINE | 核心人员情报 | 计数 / 状态口径 | 核验状态 |
|---|---|---|---|---:|---|---|---|---|
| ICSE | A | 2022-2028 | [conf-a-icse](./conf-a-icse/README.md) | 7 | 已同步 | 覆盖 2026/2027 GC/PC 与 Steering 代表人物；见根 README §5 | Research / Technical Track accepted papers；2026 Research Track count 待 DBLP/proceedings 复核 | 🟡 部分核验 |
| MoDELS | B | 2022-2028 | [conf-b-models](./conf-b-models/README.md) | 7 | 已同步 | 覆盖 2025/2026 GC/PC 与 Steering 代表人物，并补 DBLP / 代表作链接；见根 README §5 | DBLP `inproceedings` / 官方 accepted papers fallback，根表单元格显式写口径 | 🟡 部分核验 |
| ETAPS / TACAS | B | 2022-2028 | [conf-b-etaps](./conf-b-etaps/README.md) | 7 | 已同步 | 覆盖 TACAS 2026/2027 PC Chair、Area Chair 与 Steering 代表人物；见根 README §5 | ETAPS umbrella / TACAS 双口径分开 | 🟡 部分核验 |

## 3. PR-1A 试点踩坑结论

1. **年度主页与正式 CFP 不能混用**：ICSE 2028 仅有 Hawaii 预告且 `home/icse-2028` 当前 Access denied；ETAPS 2028 只有主页和会期；MoDELS 2027/2028 未发布。未来年度必须写清“已有主页 / 已检索未公布 / 仅预告”。
2. **edition 年份与事件发生年份不同**：ICSE 2027、ETAPS/TACAS 2027 的主要 submission 发生在 2026 年。因此 [TIMELINE.md](./TIMELINE.md) 按事件发生年份组织，Venue 列保留会议 edition。
3. **论文数量必须绑定计数口径**：ICSE 用 Research / Technical Track accepted papers；MoDELS 多数年份用 DBLP `inproceedings` fallback；ETAPS 必须拆 `ETAPS umbrella official count` 与 `TACAS official count`。
4. **出版入口可能分散或受限**：ICSE 2025 有 proceedings 页但 2026 DBLP/proceedings 未公开；MoDELS 2024 proceedings 当前 accessDenied，2022 ACM DL 可能 403；ETAPS 部分年份只有 proceedings 总说明页或旧站 HTML。
5. **venue URL 结构会随年份变化**：MoDELS 2025 使用独立域名 `2025.models-conf.com`，2024 及以前多在 `conf.researchr.org`；ETAPS 2022 是旧站 `.html`，2023 以后多为 `/year/cfp/` 与 `/year/conferences/tacas/`。
6. **submission system 也需可点击**：ICSE 年度 HotCRP、MoDELS 年度 EasyChair、TACAS 年度 EasyChair 均应进入根 README 和年度 README；历史年度可能重定向登录或归档，备注中说明即可。
7. **Mermaid 只放日期级可视化**：`AoE`、`UTC-12h`、官方仅日期、页面版本差异等细节留在表格备注，避免 Mermaid 图过长或不可读。
8. **核心人员情报需要强制可追溯**：venue 根 README 应记录组织者、PC / Research Track chair、Steering Committee 和强相关领域权威；每行至少保留官方角色来源，并尽量补 DBLP、个人主页、代表作或近年论文链接。MoDELS 试点表明，只有文字描述“近年论文线索”不够，后续 PR 应直接挂 DBLP / DOI / 出版页。

## 4. 当前可复用的既有资源

| 来源 | 当前用途 | 是否直接搬入 |
|---|---|---|
| [../VENUES.md](../VENUES.md) | 初始 venue 名录、CCF 等级、project 相关性 | 否，作为种子核验 |
| `PR #5 frontier_index/CCF_SE_A_B_C.md` | 软工相关 venue 边界与方向先验 | 否，作为参考 |
| `PR #5 frontier_index/CCF_SE_2026_DEADLINES.md` | deadline 调研字段与官方来源思路 | 否，需重新核验 |
| `PR #5 frontier_index/ccf_history/SUBMISSION_TIMELINES.md` | 近年时间线组织方式参考 | 否，需重新核验 |
| `PR #5 frontier_index/ccf_history/*/metadata/*.json` | 论文数量与 DBLP 计数的候选线索 | 否，只能作交叉核验 |

## 5. P0 强相关 venue 后续填充清单

P0 是“强相关先做完”的后续数据填充边界。当前 PR-1A 已完成 3 个会议试点；其余条目仍为待建或待后续 PR 处理。

| 目录名 | 类型 | CCF | 主要对应 project | 批次 | 状态 |
|---|---|---|---|---|---|
| [`conf-a-icse`](./conf-a-icse/README.md) | 会议 | A | P1/P2/P3/P4 | PR-1A | ✅ 已建 |
| `conf-a-fse` | 会议 | A | P1/P2/P4 | P0-A | ⏳ 待建 |
| `conf-a-ase` | 会议 | A | P1/P2/P4 | P0-A | ⏳ 待建 |
| `conf-a-issta` | 会议 | A | P2/P3/P4 | P0-A | ⏳ 待建 |
| `journal-a-tse` | 期刊 | A | P1/P2/P3/P4 | P0-A | ⏳ 待建 |
| `journal-a-tosem` | 期刊 | A | P1/P2/P4 | P0-A | ⏳ 待建 |
| [`conf-b-models`](./conf-b-models/README.md) | 会议 | B | P1/P2/P3 | PR-1A | ✅ 已建 |
| `conf-b-re` | 会议 | B | P1/P2 | P0-A | ⏳ 待建 |
| `journal-b-re` | 期刊 | B | P1/P2 | P0-A | ⏳ 待建 |
| `journal-b-sosym` | 期刊 | B | P1/P3 | P0-A | ⏳ 待建 |
| `conf-a-fm` | 会议 | A | P2/P3 | P0-B | ⏳ 待建 |
| `conf-a-cav` | 会议 | A | P3 | P0-B | ⏳ 待建 |
| [`conf-b-etaps`](./conf-b-etaps/README.md) | 会议 | B | P3 | PR-1A | ✅ 已建 |
| `conf-b-vmcai` | 会议 | B | P2/P3 | P0-B | ⏳ 待建 |
| `conf-b-issre` | 会议 | B | P2/P3 | P0-B | ⏳ 待建 |
| `journal-b-stvr` | 期刊 | B | P2/P3 | P0-B | ⏳ 待建 |
| `conf-c-icfem` | 会议 | C | P2/P3 | P0-B | ⏳ 待建 |
| `conf-c-spin` | 会议 | C | P3 | P0-B | ⏳ 待建 |
| `conf-c-atva` | 会议 | C | P3 | P0-B | ⏳ 待建 |
| `conf-c-icst` | 会议 | C | P2/P3/P4 | P0-B | ⏳ 待建 |
| `conf-c-refsq` | 会议 | C | P1/P2 | P0-B | ⏳ 待建 |
| `journal-c-sttt` | 期刊 | C | P3/P4 | P0-B | ⏳ 待建 |

## 6. P1 / P2 后续 venue

以下 venue 不属于 PR-1A 的数据填充目标；后续在 P0 试点与批量节奏稳定后分批推进。

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
| `conf-c-tase` | 会议 | C | 理论软工与形式化 | P1 |
| `journal-c-sqj` | 期刊 | C | 软件质量与评估 | P1 |
| `conf-c-apsec` | 会议 | C | 区域性软工、LLM4SE | P2 |
| `conf-c-seke` | 会议 | C | 知识工程与软工交叉 | P2 |
| `conf-c-ease` | 会议 | C | 实证评估 | P2 |
| `conf-c-msr` | 会议 | C | 仓库挖掘、数据集 | P2 |
| `conf-c-rv` | 会议 | C | 运行时验证 | P2 |

## 7. 核心 URL / 超链接覆盖口径

后续每个 venue 数据填充 PR 不得只写“主页 / CFP / 论文集见年度页”，而必须把核心 URL 直接挂进根 README、年度 README 和 [TIMELINE.md](./TIMELINE.md) 的表格中。

| 对象 | 必须直接挂链接的字段 | 说明 |
|---|---|---|
| 会议根 README 年度汇总表 | 年度主页、CFP、Important Dates、Submission system、Program / Accepted papers、Proceedings、DBLP 年度页 | 每个年份 row 都要能直接点击核心入口；未公布 / 待官网也要显式标注。 |
| 会议年度 README | 年度主页、CFP、Important Dates、Submission system、Program / Accepted papers、Proceedings、DBLP 年度页 | 年度页是事实源，必须有“年度核心 URL 索引”。 |
| 期刊根 README 年度汇总表 | 期刊主页、Author guidelines、Submission system、Special issue / CFP、Volume / issue、Online first、DBLP 年度页 | 期刊不硬套会议 deadline，但链接字段不能缺。 |
| 期刊年度 README | Author guidelines、Submission system、Special issue / topical collection、Volume / issue、Online first、Publisher article list、DBLP 年度页 | rolling 与 special issue 分开记录。 |
| TIMELINE.md | 事件官方来源、年度主页、论文集 / 名录、本库年度页 | dated event 和 rolling journal 表都必须是可点击索引。 |

缺失链接必须写 `待补`、`未公布`、`无已知` 或 `⏳ 已检索未公布`，并在证据 / 核查记录中说明核查时间；不得留空或用第三方聚合页冒充官方来源。

## 8. TIMELINE.md 同步验收口径

[TIMELINE.md](./TIMELINE.md) 是当前文库的一等入口。后续 venue 数据填充时必须同步满足：

1. `TIMELINE.md` 至少覆盖 `2022` 至当前年份 + 2；若已公布更远未来年度官方信息，也必须新增对应年份章节；年份按降序排列。
2. 当前文库采用“事件发生年份”组织时间线；会议 edition 的 ddl 落在前一年时，应在前一年章节记录，并在 Venue 列保留 edition。
3. 每个年份章节包含一张投稿事件总表，表内按时间升序排列。
4. 每个表格事件都必须链接到事件官方来源、年度主页、本库年度 README；若论文集 / 名录 / 卷期入口已发布，也必须直接挂链接。
5. 每个年份章节包含 Mermaid `gantt` 可视化；单日 deadline 用 `milestone`，多日窗口用普通任务。
6. 期刊 rolling submission 不进入 Mermaid 图；期刊 special issue / topical collection deadline 进入年度时间线。
7. 如果年度事件过多，应拆多张 Mermaid 图，不允许生成难以阅读的超长单图。

## 9. 待补与冲突记录

| Venue | 年份 | 问题 | 当前处理 | 下一步 |
|---|---|---|---|---|
| ICSE | 2028 | 年度主页当前 Access denied，仅找到 Hawaii 预告 | 根 README / 年度 README 不写成正式 CFP | 后续复查年度主页与 Research Track |
| ICSE | 2026 | accepted papers 已公开，但 proceedings / DBLP 年度页未公开 | 论文数量按官方 Research Track accepted papers 表记录，核验状态为部分核验 | 后续补 DBLP / proceedings |
| MoDELS | 2026 | submission / rebuttal 已过但 notification 尚未到达 | 当前阶段统一写作 `🟡 审稿中`，program probe 为 Access denied | notification 后复核状态并补 accepted papers / proceedings |
| MoDELS | 2027-2028 | 官方 home / dates / track 未发布 | 年度页标 `⏳ 已检索未公布` | 后续复查 researchr 与长期主页 |
| MoDELS | 2024 | proceedings 页面当前 accessDenied | 继续挂官方 URL，数量用 DBLP fallback | 后续复查 proceedings 页面 |
| ETAPS/TACAS | 2028 | 只有 ETAPS 主页，无 TACAS CFP / dates | 只记录会期，不写 TACAS submission | 后续复查 CFP 与 TACAS 分会页 |
| ETAPS/TACAS | 2024 | TACAS artifact deadline 页面版本差异 | 暂记 `2023-10-26 23:59 AoE` 并保留备注 | 后续精查官方页面 |

## 10. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-04 22:20` | 同步 ICSE/MoDELS/ETAPS review 修复状态，记录根表计数口径与 MoDELS 2026 审稿中状态。 |
| `2026-06-04 21:55` | 同步核心人员情报覆盖状态，记录核心人员表可追溯性试点结论，并补充更新日志降序提示。 |
| `2026-06-04 21:10` | 完成 PR-1A 会议试点：新增 ICSE、MoDELS、ETAPS/TACAS 根 README 与 2022-2028 年度 README，同步 TIMELINE，并记录试点踩坑结论。 |
| `2026-06-04 19:37` | 补充核心 URL / 超链接覆盖口径，要求根 README、年度 README 和 TIMELINE 都直接挂核心来源链接。 |
| `2026-06-04 18:55` | 明确默认未来检索/占位下限为当前年份 + 2（当前到 2028），更远未来若已有官方 CFP / important dates 也必须纳入。 |
