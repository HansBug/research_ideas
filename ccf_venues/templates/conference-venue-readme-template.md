# `<VENUE>` README

> 信息更新时间：`yyyy-mm-dd hh:mm`（Timezone）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | `<VENUE>` |
| 全称 | `<Full Name>` |
| 类型 | 会议 |
| CCF 大类 | `<E / 理论 / T / ...>` |
| CCF 等级 | `<A/B/C>` |
| 出版方 | `<ACM/IEEE/Springer/...>` |
| 官方 series page | 待补（占位：OFFICIAL_SERIES_URL；核验后改为 Markdown 链接） |
| 官方当前 / 最新年度主页 | 待补（占位：LATEST_YEAR_HOME_URL；核验后改为 Markdown 链接） |
| 官方 CFP / Important Dates 总入口 | 待补（占位：OFFICIAL_CFP_OR_DATES_URL；核验后改为 Markdown 链接） |
| 官方 proceedings / paper list 总入口 | 待补（占位：OFFICIAL_PROCEEDINGS_OR_PAPERS_URL；核验后改为 Markdown 链接） |
| DBLP venue page | 待补（占位：DBLP_VENUE_URL；核验后改为 Markdown 链接） |
| 当前默认调查范围 | `2022` 至当前年份 + 2；若更远未来年度已有官方信息也继续纳入 |

### 1.1 索引与分区信息

> 本节记录外部索引与分区事实。实例化时必须按 [GUIDE.md](../GUIDE.md) 的外部索引规则补证；每一行都必须给出可点击官方入口、source-list snapshot 字段或明确 access note。若尚未核验，不得留空或脑补，应写 `❓` / `⚪` / `⏳` 等规范占位。JCR 与 CAS 的 emoji 列只允许写真实 emoji，例如 `1️⃣` / `2️⃣` / `3️⃣` / `4️⃣` / `⚪` / `⏳`，文字解释放在口径说明或相邻列。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | ❓ | 待核验 | 待补（占位：CCF_OFFICIAL_URL；核验后改为 Markdown 链接 + CCF 等级证据） | `yyyy-mm-dd hh:mm` |
| WoS / CPCI | ⏳ | 已检索未获可审计证据 | 待补（占位：CLARIVATE_CPCI_OR_MJL_URL；会议仅按 CPCI-S / CPCI-SSH proceedings 或官方会议卷证据记录） | `yyyy-mm-dd hh:mm` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 默认不适用 JCR 期刊分区；如有同名期刊，另在 `journal-*` 目录核验 | `yyyy-mm-dd hh:mm` |
| CAS 分区 | ⚪ | 不适用 | 会议 venue 默认不填 CAS 分区；CAS 仅用于期刊历史版分区 | `yyyy-mm-dd hh:mm` |
| EI / Compendex | ❓ | 待核验 | 待补（占位：ELSEVIER_SOURCE_LIST_URL；记录 snapshot、sheet、Source title、Source type、ISBN/ISSN） | `yyyy-mm-dd hh:mm` |
| 索引核验 | ❓ | 待启动 | 缺证条目须同步登记到 SUMMARY 风险 / 待核验表；证据链接不能只留在 PR comment | `yyyy-mm-dd hh:mm` |

## 2. Scope 与方向

- 官方 scope 摘要：待补。
- 与本仓库最相关的方向：待补。
- 明显不属于本仓库重点的方向：待补。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 待判定 | 待补 |
| P2 场景与性质生成 | 待判定 | 待补 |
| P3 验证剖面与模型检查 | 待判定 | 待补 |
| P4 模型修复 | 待判定 | 待补 |

## 4. 核心链接索引

本节放跨年度稳定入口；年度专属链接必须继续写入 §6 年度信息汇总和各年度 README。

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | 待补（占位：OFFICIAL_SERIES_URL；核验后改为 Markdown 链接） | 待补 | `yyyy-mm-dd hh:mm` |
| Latest year homepage | 待补（占位：LATEST_YEAR_HOME_URL；核验后改为 Markdown 链接） | 待补 | `yyyy-mm-dd hh:mm` |
| CFP / Call for Papers | 待补（占位：OFFICIAL_CFP_URL；核验后改为 Markdown 链接） | 若分 track，逐年度页展开 | `yyyy-mm-dd hh:mm` |
| Important Dates | 待补（占位：OFFICIAL_DATES_URL；核验后改为 Markdown 链接） | 可与 CFP 同页 | `yyyy-mm-dd hh:mm` |
| Submission system | 待补（占位：SUBMISSION_SYSTEM_URL；核验后改为 Markdown 链接） | 若不公开写 `未公布` | `yyyy-mm-dd hh:mm` |
| Program / accepted papers | 待补（占位：OFFICIAL_PROGRAM_OR_ACCEPTED_URL；核验后改为 Markdown 链接） | 已结束年度优先官方 | `yyyy-mm-dd hh:mm` |
| Proceedings | 待补（占位：OFFICIAL_PROCEEDINGS_URL；核验后改为 Markdown 链接） | 出版商页面优先 | `yyyy-mm-dd hh:mm` |
| DBLP venue | 待补（占位：DBLP_VENUE_URL；核验后改为 Markdown 链接） | 仅作论文名录 / 计数 fallback | `yyyy-mm-dd hh:mm` |

## 5. 核心人员情报

本节记录会议核心人员，不要求全量 PC roster。对 umbrella venue 必须区分 umbrella、main conference、satellite conference 和 track 层级。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| 待补 | `<YEAR>` / `<LEVEL>` | General Chair / Program Chair / Research Track Chair / Steering Committee | 待补 | 待补 | 待补 | 待补 | 待补 | 待判定 | ⏳ 待核验 | `yyyy-mm-dd hh:mm` |

## 6. 年度信息汇总

年度汇总表必须把核心 URL 直接做成 Markdown 超链接；不要只写“见年度页”。若官方未公布，写 `待补` / `未公布` / `⏳ 已检索未公布`，并在年度 README 记录核查时间。

本模板位于 [templates/](../templates/) 下，年度路径在模板文件中只用代码样式占位；实例化到具体 venue 根目录后，必须把 `2028/README.md` 等改为真实可点击相对链接（例如年份文本 `2028` 指向同级年度页 `./2028/README.md`）。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `2028/README.md` | ⏳ 待官网 | 待补 | 待补 | 待补 | 未公布 | 未公布 | 未公布 | 待补 | 未公布 | 未公布 | 未公布 | 未公布 |  | ⏳ 待核验 |
| `2027/README.md` | ⏳ 待官网 | 待补 | 待补 | 待补 | 未公布 | 未公布 | 未公布 | 待补 | 未公布 | 未公布 | 未公布 | 未公布 |  | ⏳ 待核验 |
| `2026/README.md` | ⏳ 待官网 | 待补 | 待补 | 待补 | 未公布 | 未公布 | 未公布 | 待补 | 未公布 | 未公布 | 未公布 | 未公布 |  | ⏳ 待核验 |
| `2025/README.md` | ✅ 已结束 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | ⏳ 待核验 |
| `2024/README.md` | ✅ 已结束 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | ⏳ 待核验 |
| `2023/README.md` | ✅ 已结束 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | ⏳ 待核验 |
| `2022/README.md` | ✅ 已结束 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | ⏳ 待核验 |

## 7. 维护备注

- 待补。

## 8. TIMELINE.md 同步提示

- 若本 README 的年度汇总表新增或修改投稿相关 important date，必须同步更新 `../TIMELINE.md`（实例化后按相对路径核对）。
- `../TIMELINE.md` 中对应事件行也必须保留可点击的 `事件官方来源`、`年度主页`、`论文集 / 名录` 和 `本库年度页` 链接。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 13:52:01` | PR #91 同步证据链模板纪律：索引表每行必须有官方链接、source-list 字段或 access note。 |
| `2026-06-09 11:13` | 新增会议 venue 外部索引与分区信息模板。 |
| `yyyy-mm-dd hh:mm` | 初始化 `<VENUE>` venue README。 |
