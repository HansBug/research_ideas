# FSE README

> 信息更新时间：`2026-06-05 08:39`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | FSE |
| 全称 | ACM International Conference on the Foundations of Software Engineering（2024 起主名称）；历史年度常写 ESEC/FSE |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | A |
| 出版方 | ACM / PACMSE |
| 官方 series page | [FSE series](https://conf.researchr.org/series/fse) |
| 官方当前 / 最新年度主页 | [FSE 2027](https://conf.researchr.org/home/fse-2027)；[FSE 2028](https://conf.researchr.org/home/fse-2028) 当前 404 |
| 官方 CFP / Important Dates 总入口 | 逐年度 Research Papers track 维护 |
| 官方 proceedings / paper list 总入口 | 逐年度 program / proceedings；2024+ Research Papers 说明 PACMSE issue 是主 proceedings 口径 |
| DBLP venue page | [DBLP SIGSOFT/FSE venue](https://dblp.org/db/conf/sigsoft/) |
| 当前默认调查范围 | `2022` 至 `2028` |

## 2. Scope 与方向

- FSE 是软件工程旗舰会议，覆盖软件工程基础、方法、工具、实证与产业实践。
- 与本仓库最相关的方向：AI/LLM for SE、软件建模与规格、测试与分析、软件维护、程序修复、开源科学与 artifact。
- 明显不属于本仓库重点但仍可作背景：教育、会议组织、泛人因与社区议题。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 高 | 可追踪需求到模型、LLM 辅助建模、软件设计与工具论文。 |
| P2 场景与性质生成 | 高 | 可追踪测试生成、规格挖掘、属性 / oracle 生成与评估论文。 |
| P3 验证剖面与模型检查 | 中 | FSE 有程序分析、验证与可靠性论文，但不如 CAV/TACAS 聚焦形式化。 |
| P4 模型修复 | 高 | 自动修复、调试、缺陷定位和 LLM repair 是 FSE 常见主题。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [FSE series](https://conf.researchr.org/series/fse) | researchr 长期入口 | `2026-06-05 08:39` |
| Latest year homepage | [FSE 2027](https://conf.researchr.org/home/fse-2027) | 2028 未公布；2027 已有地点与会期 | `2026-06-05 08:39` |
| CFP / Call for Papers | [FSE 2026 Research Papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | 2027 CFP 未公布 | `2026-06-05 08:39` |
| Important Dates | [FSE 2026 Research Papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | Important Dates 与 Research Papers 同页 | `2026-06-05 08:39` |
| Submission system | [FSE 2026 HotCRP](https://fse2026.hotcrp.com/) | 历年入口见年度页 | `2026-06-05 08:39` |
| Program / accepted papers | [FSE 2026 Program](https://conf.researchr.org/program/fse-2026/program-fse-2026/) | 已结束年度优先官方 program，DBLP fallback | `2026-06-05 08:39` |
| Proceedings | [FSE 2025 proceedings](https://conf.researchr.org/info/fse-2025/proceedings) | 2024+ 注意 PACMSE issue 关系 | `2026-06-05 08:39` |
| DBLP venue | [DBLP SIGSOFT/FSE venue](https://dblp.org/db/conf/sigsoft/) | 仅作论文名录 / 计数 fallback | `2026-06-05 08:39` |

## 5. 核心人员情报

| 人员 | 角色 / 年度 | 官方角色来源 | 主要研究方向 | 代表作 / 近年论文线索 | 与本仓库关系 | 待深挖 |
|---|---|---|---|---|---|---|
| Foutse Khomh | FSE 2026 General Co-Chair | [FSE 2026 Organizing Committee](https://conf.researchr.org/committee/fse-2026/fse-2026-organizing-committee) | ML/AI software engineering, software quality, empirical SE | [DBLP](https://dblp.org/pid/21/7138) | P1/P2/P4 高相关：ML-enabled systems 与质量评估 | 待补个人主页与近 5 年代表作精确链接。 |
| Shin Hwei Tan | FSE 2026 General Co-Chair | [FSE 2026 Organizing Committee](https://conf.researchr.org/committee/fse-2026/fse-2026-organizing-committee) | program repair, software testing, SE automation | [DBLP](https://dblp.org/pid/26/9450) | P4 很高，P2 中高：修复与测试反馈闭环 | 待补个人主页 / 近年 LLM repair 论文。 |
| Julia Lawall | FSE 2026 Program Co-Chair | [FSE 2026 Organizing Committee](https://conf.researchr.org/committee/fse-2026/fse-2026-organizing-committee) | program analysis, Coccinelle, software evolution | [DBLP](https://dblp.org/pid/l/JuliaLawall) | P4/P3 高相关：规则化修复、程序分析证据链 | 待补 Coccinelle 代表作链接。 |
| Christoph Treude | FSE 2026 Program Co-Chair | [FSE 2026 Organizing Committee](https://conf.researchr.org/committee/fse-2026/fse-2026-organizing-committee) | AI for SE, developer knowledge, empirical SE | [DBLP](https://dblp.org/pid/42/4730) | P1/P2/P4 高相关：LLM4SE、开发者知识与实验评估 | 待补近年 LLM4SE 论文入口。 |
| Lin Tan | FSE 2024 Program Co-Chair | [FSE 2024 Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | software reliability, testing, program analysis | [DBLP](https://dblp.org/pid/t/LinTan) | P2/P3/P4 高相关 | 待补官方个人主页。 |
| David Lo | FSE 2024 Program Co-Chair | [FSE 2024 Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | software analytics, mining software repositories, testing | [DBLP](https://dblp.org/pid/39/8119) | P2/P4 高相关，适合追踪 LLM4SE 实证线索 | 待补近 5 年代表作。 |
| FSE Steering Committee | 长期治理层 | [FSE 2026 Organization navigation](https://conf.researchr.org/committee/fse-2026/fse-2026-steering-committee) | venue policy, PACMSE / conference naming, research track governance | 官方 steering 页面待逐人展开 | 与投稿制度、PACMSE 计数口径直接相关 | 后续应逐人补角色、DBLP 和任期。 |

## 6. 年度信息汇总

> 年度表按年份降序排列。FSE 冻结口径：目录 slug 固定为 `conf-a-fse`，根 README 主名称为 `FSE`；2022-2023 年度官方写 ESEC/FSE 时仅在年度页补注。PACMSE / proceedings 是 FSE Research Papers 的出版口径，不作为独立额外论文数量重复计数。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract / registration deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 待官网 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟦 已有主页 | [FSE 2027](https://conf.researchr.org/home/fse-2027) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 2027-07-12..2027-07-16 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🟡 已通知 / 会前 | [FSE 2026](https://conf.researchr.org/home/fse-2026) | [Research Papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | [HotCRP](https://fse2026.hotcrp.com/) | [FSE Program](https://conf.researchr.org/program/fse-2026/program-fse-2026/) | 未公布；PACMSE Issue FSE 2026 由 Research Papers track 说明 | ⏳ 已检索未公布 | 2025-09-04 23:59 AoE / UTC-12h | 2025-09-11 23:59 AoE / UTC-12h | 2025-12-22 23:59 AoE / UTC-12h；major revision final 2026-03-24 23:59 AoE / UTC-12h | 2026-07-05..2026-07-09 | 未最终核验；program 已有条目 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [FSE 2025](https://conf.researchr.org/home/fse-2025) | [Research Papers](https://conf.researchr.org/track/fse-2025/fse-2025-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2025/fse-2025-research-papers) | [HotCRP](https://fse2025.hotcrp.com/) | [FSE Program](https://conf.researchr.org/program/fse-2025/program-fse-2025/) | [Proceedings](https://conf.researchr.org/info/fse-2025/proceedings) / PACMSE Issue FSE 2025 | [DBLP 2025](https://dblp.org/db/conf/sigsoft/fse2025c.html) | 2024-09-05 23:59 AoE / UTC-12h | 2024-09-12 23:59 AoE / UTC-12h | 2025-01-14 23:59 AoE / UTC-12h（官方页疑似写 2024，按上下文待复核）；major revision final 2025-04-01 23:59 AoE / UTC-12h | 2025-06-23..2025-06-27 | DBLP inproceedings fallback: 259 | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [FSE 2024](https://conf.researchr.org/home/fse-2024) | [Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | [HotCRP](https://fse2024.hotcrp.com/) | [FSE Program](https://conf.researchr.org/program/fse-2024/program-fse-2024/) | [Proceedings](https://conf.researchr.org/info/fse-2024/proceedings) / PACMSE Issue FSE 2024 | [DBLP 2024](https://dblp.org/db/conf/sigsoft/fse2024c.html) | 2023-09-21 23:59 AoE / UTC-12h | 2023-09-28 23:59 AoE / UTC-12h | 2024-01-23 23:59 AoE / UTC-12h；major revision final 2024-04-16 23:59 AoE / UTC-12h | 2024-07-15..2024-07-19 | DBLP inproceedings fallback: 108 | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [ESEC/FSE 2023](https://conf.researchr.org/home/fse-2023) | [Research Papers](https://conf.researchr.org/track/fse-2023/fse-2023-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2023/fse-2023-research-papers) | [HotCRP](https://esecfse2023.hotcrp.com/) | [ESEC/FSE Program](https://conf.researchr.org/program/fse-2023/program-fse-2023/) | [Proceedings](https://conf.researchr.org/info/fse-2023/proceedings) | [DBLP 2023](https://dblp.org/db/conf/sigsoft/fse2023.html) | 2023-01-26 23:59 AoE / UTC-12h | 2023-02-02 23:59 AoE / UTC-12h | 2023-05-04 23:59 AoE / UTC-12h；major revision final 2023-07-27 23:59 AoE / UTC-12h | 2023-12-03..2023-12-09 | DBLP fallback 待复核 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [ESEC/FSE 2022](https://conf.researchr.org/home/fse-2022) | [Research Papers](https://conf.researchr.org/track/fse-2022/fse-2022-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2022/fse-2022-research-papers) | [HotCRP](https://fse2022.hotcrp.com/) | [ESEC/FSE Program](https://conf.researchr.org/program/fse-2022/program-fse-2022/) | [Proceedings](https://conf.researchr.org/info/fse-2022/proceedings) | [DBLP 2022](https://dblp.org/db/conf/sigsoft/fse2022.html) | 2022-03-10 23:59 AoE / UTC-12h | 2022-03-17 23:59 AoE / UTC-12h | 2022-06-14 23:59 AoE / UTC-12h | 2022-11-14..2022-11-18 | DBLP fallback 待复核 | 🟡 部分核验 |

## 7. 维护备注

- 2024 起官方说明会议名称调整为 FSE；2022-2023 年度页仍保留 ESEC/FSE 官方名称。
- 2024+ Research Papers 页面说明 PACMSE issue 是主 proceedings 入口；本库不得把 PACMSE 卷期再作为独立会议论文数量重复计数。
- 2025 Research Papers 页面 initial notification 年份疑似官方页笔误；本草稿按上下文记录为待复核，不作为最终 timeline 事实。
- 2022/2023 DBLP 数量本轮未稳定抓取，年度页保留 fallback 待复核。

## 8. TIMELINE.md 同步提示

- 本 worker 未修改 [TIMELINE.md](../TIMELINE.md)；候选事件见 [_events_draft.md](./_events_draft.md)。

## 9. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-05 08:39` | 初始化 FSE venue 根 README 与 2022-2028 年度索引草稿。 |
