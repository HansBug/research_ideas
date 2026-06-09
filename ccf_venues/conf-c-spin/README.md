# SPIN README

> 信息更新时间：`2026-06-09 11:13`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | SPIN |
| 全称 | International Symposium on Model Checking of Software |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 模型检查 / 运行时验证 |
| CCF 等级 | C |
| 本库目录 | `conf-c-spin` |
| 出版方 | Springer LNCS / SPIN official pages |
| 官方 series page | [SPIN official pages](https://spin-web.github.io/) |
| DBLP venue page | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节由 PR #90 建立为外部索引占位入口；当前仅完成规则制度化与待核验占位，真实 WoS / JCR / CAS / EI 结论需按 [GUIDE.md](../GUIDE.md) 的外部索引规则逐项补证。JCR 与 CAS 的 emoji 列只允许写真实 emoji，例如 `1️⃣` / `2️⃣` / `3️⃣` / `4️⃣` / `⚪` / `❓`，文字解释放在口径说明或相邻列。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | ❓ | 待复核 CCF 官方目录证据 | 沿用 §1 CCF 等级；后续需补 CCF 官方目录链接与核验时间 | `待补` |
| WoS / CPCI | ❓ | 待核验 | 会议不写作 SCI/JCR 期刊；仅按 CPCI-S / CPCI-SSH proceedings 或官方会议卷证据记录 | `待补` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 默认不适用 JCR 期刊分区；若存在同名期刊必须另按期刊 venue 记录 | `待补` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅适用于期刊历史版分区证据；会议 venue 不填 CAS 区 | `待补` |
| EI / Compendex | ❓ | 待核验 | 需按官方 Compendex Source List snapshot 核验 proceedings / book-series / source type / final coverage | `待补` |
| 索引核验 | ❓ | 待启动 | 缺证条目须同步登记到 [SUMMARY.md](../SUMMARY.md) 风险 / 待核验表 | `待补` |

## 2. Scope 与方向

SPIN 聚焦软件模型检查、运行时验证、验证工具、形式化建模、自动机和工业案例；artifact / tool paper 与 full paper 必须分开。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟢 高 | Promela/SPIN、状态空间和状态机建模是直接素材。 |
| P2 | 🟢 高 | 性质、monitor、counterexample 与场景生成直接相关。 |
| P3 | 🟢 高 | 模型检查与验证工具是 P3 的核心。 |
| P4 | 🟡 中 | 修复线索需从 counterexample / runtime verification 论文筛选。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [SPIN official pages](https://spin-web.github.io/) | 长期入口，年度信息仍以年度页 / CFP 为准 | `2026-06-05 09:15` |
| DBLP venue page | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| 最新年度入口 | ⏳ 已检索未公布 | `2029+` 已检索未公布；未来年度不得伪造 | `2026-06-05 09:15` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Gidon Ernst | SPIN 2025 Program Chair；SPIN 2026 Program Committee | Ludwig-Maximilians-Universität München | [SPIN 2025 Committees](https://spin-web.github.io/SPIN2025/committees) / [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [Homepage](https://www.gidonernst.de/) | logic and formal methods for reliable software and systems | [DBLP](https://dblp.org/pid/19/1202.html) | P2/P3：形式化逻辑、验证工具和可靠软件。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Kristin Yvonne Rozier | SPIN 2025 Program Chair；SPIN 2026 Program Committee | Iowa State University | [SPIN 2025 Committees](https://spin-web.github.io/SPIN2025/committees) / [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/67/519.html) | temporal logic、runtime observers、safety-critical systems | [DBLP 论文入口](https://dblp.org/pid/67/519.html) | P2/P3：时序性质与 runtime monitor。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Vincenzo Ciancia | SPIN 2026 Program Chair | ISTI-CNR | [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/31/4665.html) | spatial logics、model checking、formal methods | [DBLP 论文入口](https://dblp.org/pid/31/4665.html) | P2/P3：逻辑性质与模型检查。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Arnd Hartmanns | SPIN 2026 Program Chair | University of Twente | [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/77/7997.html) | probabilistic model checking、stochastic systems、tools | [DBLP 论文入口](https://dblp.org/pid/77/7997.html) | P3：概率/定量验证 profile。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Gerard Holzmann | SPIN 2025/2026 Steering Committee | Nimble Research | [SPIN 2025 Committees](https://spin-web.github.io/SPIN2025/committees) / [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/h/GerardJHolzmann.html) | SPIN model checker、Promela、software model checking | [DBLP 论文入口](https://dblp.org/pid/h/GerardJHolzmann.html) | P1/P3：状态机建模和软件模型检查 foundational。 | 🟡 部分核验 | `2026-06-05 10:04` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | ✅ 已结束 | [SPIN 2026](https://spin-web.github.io/SPIN2026/) | [CFP](https://spin-web.github.io/SPIN2026/cfp) | [Important Dates](https://spin-web.github.io/SPIN2026/cfp) | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/spin/index.html) | 2026-01-22 待补时刻 AoE | 2026-01-29 待补时刻 AoE | 2026-03-05 待补时刻 | 2026-04-15..2026-04-16 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [SPIN 2025](https://spin-web.github.io/SPIN2025/) | [CFP](https://spin-web.github.io/SPIN2025/cfp) | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/9783032068460) | [DBLP](https://dblp.org/db/conf/spin/spin2025) | 未公布 | 未公布 | 未公布 | 2025 待补精确日期 | 9 full papers / 20 submissions | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [SPIN 2024](https://spin-web.github.io/SPIN2024/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-66149-5) | [DBLP](https://dblp.org/db/conf/spin/spin2024) | 未公布 | 未公布 | 未公布 | 2024 待补精确日期 | 14 papers / 1 volume | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [SPIN 2023](https://spin-web.github.io/SPIN2023/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-32156-6) | [DBLP](https://dblp.org/db/conf/spin/spin2023) | 未公布 | 未公布 | 未公布 | 2023 待补精确日期 | 11 papers / 1 volume | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [SPIN 2022](https://spinroot.com/spin/Workshops/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-15077-7) | [DBLP](https://dblp.org/db/conf/spin/spin2022) | 未公布 | 未公布 | 未公布 | 2022 待补精确日期 | 8 full papers / 9 TOC entries | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 均已做公开入口检索；未公布年度保留占位与核查记录，不预设 CFP。
- 2028 计数口径：未发现 SPIN 2028 官方年页。
- 2027 计数口径：未发现 SPIN 2027 官方年页。
- 2026 计数口径：程序 / proceedings 尚未作为闭合 count 纳入。
- 2025 计数口径：Springer count；不混入 artifact/tool 额外项。
- 2022 计数口径：矛盾待解：Springer book page 写 8 full papers selected from 11 submissions；Springer/DBLP TOC 口径可见 9 entries。正式 full-paper 口径优先 8。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-3 已把 2025--2027 年可核验的主要 dated events 并入 [TIMELINE.md](../TIMELINE.md) 的正式年度时间线与 Mermaid；历史年度未完全补齐的 deadline 留在各年度 README 待后续精查。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 10:04` | 根据复审把 SPIN 核心人员来源改为 `/committees` 直达页，明确 Program Chair / Program Committee / Steering Committee 角色。 |
| `2026-06-05 09:15` | PR-3 初始化 SPIN venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
