# `2025` 年度汇总

## 1. 年份说明

- 年份：`2025`
- 覆盖范围：`CCF_SE_A_B_C.md` 当前保留的 `CCF` 软件工程高相关 venue 子集
- 当前覆盖的 venue 数量：`57`
- 当前已入表论文数量：`5153`
- 更新时间：`2026-04-06 19:11`
- 说明：本年度条目已实现全量人工复核；最终裁决已直接固化在 `metadata/*.json` 中。本页只保留年度汇总与 venue 导航，逐篇论文名录拆分到 `venues/*.md`。

## 2. 年度汇总统计

- A 类会议：`1247`
- A 类期刊：`782`
- B 类会议：`646`
- B 类期刊：`1238`
- C 类会议：`1065`
- C 类期刊：`175`
- 期望总条目数：`5153`
- 实际总条目数：`5153`
- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (1408) / 🟡 保留观察 (2645) / ⏳ 待补信息 (899) / ⚪ 暂不跟进 (201)
- 一级总判定分布：软件工程 (3430) / 跨域/待判定 (972) / 程序设计语言与形式化基础 (510) / 系统软件 (241)
- 软工纳入判定分布：属于软件工程 (3324) / 不属于软件工程 (1723) / 跨域但软工主导 (106)
- 判定来源分布：人工复核 (5153)
- 人工复核状态分布：已人工复核 (5153)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (398) / 6.3.4 replication、benchmark 与开放科学 (229) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (222) / 7.1.2 AI 支持的测试、分析与修复 (218) / 6.3.1 实验、案例研究与调查 (169) / 7.1.4 AI 支持的架构、设计与工程决策 (112) / 1.1.1 需求获取与发现 (102) / 3.1.4 场景化测试 (101) / 4.1.1 缺陷修复与维护性修正 (82) / 3.2.1 静态分析与抽象解释 (76) / 5.2.1 安全开发与漏洞治理 (70) / 3.2.3 面向质量属性的分析 (68)

## 3. 标准口径

- `软工归属级别` 统一使用 [CCF_SE_A_B_C.md](../../CCF_SE_A_B_C.md) 中的 `完全属于软工 / 大部分属于软工 / 部分属于软工`。
- `氛围` 统一使用 [CCF_SE_A_B_C.md](../../CCF_SE_A_B_C.md) 中的 `A 🔥 / B 🟢 / C 🟡`。
- 若需要表达 venue 的持续跟踪优先级，直接复用 `氛围`；同档再参考 `软工归属级别`，不要再另造 `A/B/C/D` 或其他四级制。
- 逐篇论文层面不再额外发明 `A/B/C/D` 第二套等级；论文名录只按现有 `初筛` 优先级 `🟢 -> 🟡 -> ⏳ -> ⚪` 排序。

## 4. 投稿时间线资料

- 总入口：[../SUBMISSION_TIMELINES.md](../SUBMISSION_TIMELINES.md)
- 时间线总入口开头已提供基于 `2021-2025` 历史节奏推断的下一自然年周级投稿规划表，可先按周排全年准备节奏。
- 会议 venue：默认看最近 `5` 年 `摘要截止 / 投稿截止 / rebuttal / 通知 / camera-ready / 会期`。
- 期刊 venue：默认看滚动投稿与 special issue 提醒，不机械构造 conference 式年度 `CFP`。
- 本页每个 venue 导航 section 与对应 `venues/*.md` 都附了该 venue 的时间线锚点。

## 5. 覆盖 venue 列表

- 口径：当前年度页只覆盖 [CCF_SE_A_B_C.md](../../CCF_SE_A_B_C.md) 中保留的 venue。
- `主体归属`、`软工归属级别`、`氛围` 与 `典型软工路径（先验）` 来自 venue 级先验；`2025` 逐篇统计直接按本年度 `metadata/*.json` 中的终判字段汇总。
- `典型软工路径（先验）` 与 `2025 高频软工主路径` 使用 [SOFTWARE_ENGINEERING_FIELD_TREE.md](../../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的方向树口径。

| venue | 全称 | 等级 | 类型 | 论文数 | 软工归属级别 | 氛围 | 主体归属 | 典型软工路径（先验） | 当年一级总判定 | 当年软工纳入 | 初筛分布 | 当年高频软工主路径 | 论文名录 | 数据文件 | 备注 |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| `APSEC` | Asia-Pacific Software Engineering Conference | `C` | `会议` | 117 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 108 / 跨域/待判定 8 / 程序设计语言与形式化基础 1 | 属于软件工程 108 / 不属于软件工程 9 | 🟢 优先跟进 (36) / 🟡 保留观察 (77) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (2) | 7.1.1 代码生成、补全与变换 (23) / 6.3.4 replication、benchmark 与开放科学 (21) | [venue](venues/apsec_conf_c.md) | [metadata](metadata/apsec_conf_c.json) | 计数一致；2025 与先验一致 |
| `ASE / 会议 / A` | International Conference on Automated Software Engineering | `A` | `会议` | 389 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 387 / 程序设计语言与形式化基础 2 | 属于软件工程 387 / 不属于软件工程 2 | 🟢 优先跟进 (124) / 🟡 保留观察 (247) / ⏳ 待补信息 (13) / ⚪ 暂不跟进 (5) | 7.1.1 代码生成、补全与变换 (89) / 7.1.2 AI 支持的测试、分析与修复 (55) | [venue](venues/ase_conf_a.md) | [metadata](metadata/ase_conf_a.json) | 计数一致；2025 与先验一致 |
| `ASE / 期刊 / B` | Automated Software Engineering | `B` | `期刊` | 74 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 72 / 跨域/待判定 2 | 属于软件工程 72 / 不属于软件工程 2 | 🟢 优先跟进 (13) / 🟡 保留观察 (13) / ⏳ 待补信息 (47) / ⚪ 暂不跟进 (1) | 7.1.1 代码生成、补全与变换 (14) / 7.1.2 AI 支持的测试、分析与修复 (7) | [venue](venues/ase_journal_b.md) | [metadata](metadata/ase_journal_b.json) | 计数一致；2025 与先验一致 |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | `B` | `会议` | 35 | 部分属于软工 | B 🟢 | 信息系统工程与软件工程交叉 | 1.3.x / 2.1.x / 4.3.x / 8.3.x | 跨域/待判定 29 / 软件工程 5 / 系统软件 1 | 不属于软件工程 30 / 跨域但软工主导 3 / 属于软件工程 2 | 🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (2) / 6.1.2 过程挖掘、符合性与改进 (2) | [venue](venues/caise_conf_b.md) | [metadata](metadata/caise_conf_b.json) | 计数一致；2025 比先验更偏非软工 |
| `COMPSAC` | International Computer Software and Applications Conference | `C` | `会议` | 330 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 231 / 软件工程 61 / 系统软件 32 / 程序设计语言与形式化基础 6 | 不属于软件工程 269 / 属于软件工程 47 / 跨域但软工主导 14 | 🟢 优先跟进 (43) / 🟡 保留观察 (253) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (34) | 6.3.1 实验、案例研究与调查 (6) / 4.1.1 缺陷修复与维护性修正 (4) | [venue](venues/compsac_conf_c.md) | [metadata](metadata/compsac_conf_c.json) | 计数一致；2025 比先验更偏非软工 |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | `C` | `会议` | 126 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 122 / 跨域/待判定 4 | 属于软件工程 122 / 不属于软件工程 4 | 🟢 优先跟进 (25) / 🟡 保留观察 (87) / ⏳ 待补信息 (8) / ⚪ 暂不跟进 (6) | 6.3.1 实验、案例研究与调查 (25) / 6.3.4 replication、benchmark 与开放科学 (20) | [venue](venues/ease_conf_c.md) | [metadata](metadata/ease_conf_c.json) | 计数一致；2025 与先验一致 |
| `ECOOP` | European Conference on Object-Oriented Programming | `B` | `会议` | 43 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 4.2.x | 程序设计语言与形式化基础 35 / 软件工程 6 / 系统软件 2 | 不属于软件工程 37 / 属于软件工程 4 / 跨域但软工主导 2 | 🟢 优先跟进 (6) / 🟡 保留观察 (11) / ⏳ 待补信息 (26) / ⚪ 暂不跟进 (0) | 7.1.1 代码生成、补全与变换 (1) / 1.2.1 形式化规约与契约 (1) | [venue](venues/ecoop_conf_b.md) | [metadata](metadata/ecoop_conf_b.json) | 计数一致；2025 比先验更偏非软工 |
| `ESE` | Empirical Software Engineering | `B` | `期刊` | 178 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 144 / 跨域/待判定 31 / 程序设计语言与形式化基础 2 / 系统软件 1 | 属于软件工程 144 / 不属于软件工程 34 | 🟢 优先跟进 (22) / 🟡 保留观察 (51) / ⏳ 待补信息 (103) / ⚪ 暂不跟进 (2) | 6.3.1 实验、案例研究与调查 (33) / 4.1.1 缺陷修复与维护性修正 (25) | [venue](venues/ese_journal_b.md) | [metadata](metadata/ese_journal_b.json) | 计数一致；2025 与先验一致 |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | `B` | `会议` | 58 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 58 | 属于软件工程 58 | 🟢 优先跟进 (15) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 6.3.1 实验、案例研究与调查 (12) / 6.3.4 replication、benchmark 与开放科学 (9) | [venue](venues/esem_conf_b.md) | [metadata](metadata/esem_conf_b.json) | 计数一致；2025 与先验一致 |
| `FM` | International Symposium on Formal Methods | `A` | `会议` | 67 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 54 / 软件工程 7 / 系统软件 6 | 不属于软件工程 60 / 属于软件工程 5 / 跨域但软工主导 2 | 🟢 优先跟进 (46) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 3.3.1 面向软工问题的形式化验证 (3) / 3.2.4 分析驱动的理解、重构与综合 (1) | [venue](venues/fm_conf_a.md) | [metadata](metadata/fm_conf_a.json) | 计数一致；2025 比先验更偏非软工 |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | `A` | `会议` | 132 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 131 / 程序设计语言与形式化基础 1 | 属于软件工程 131 / 不属于软件工程 1 | 🟢 优先跟进 (39) / 🟡 保留观察 (92) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 7.1.1 代码生成、补全与变换 (30) / 6.3.4 replication、benchmark 与开放科学 (15) | [venue](venues/fse_conf_a.md) | [metadata](metadata/fse_conf_a.json) | 计数一致；2025 与先验一致 |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | `C` | `会议` | 22 | 部分属于软工 | B 🟢 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.3.x | 跨域/待判定 16 / 软件工程 6 | 不属于软件工程 16 / 属于软件工程 3 / 跨域但软工主导 3 | 🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (1) / 3.3.1 面向软工问题的形式化验证 (1) | [venue](venues/iceccs_conf_c.md) | [metadata](metadata/iceccs_conf_c.json) | 计数一致；2025 与先验一致 |
| `ICFEM` | International Conference on Formal Engineering Methods | `C` | `会议` | 21 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 15 / 软件工程 6 | 不属于软件工程 15 / 跨域但软工主导 4 / 属于软件工程 2 | 🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (1) / 3.2.1 静态分析与抽象解释 (1) | [venue](venues/icfem_conf_c.md) | [metadata](metadata/icfem_conf_c.json) | 计数一致；2025 与先验一致 |
| `ICPC` | IEEE International Conference on Program Comprehension | `B` | `会议` | 59 | 完全属于软工 | B 🟢 | 软件工程 | 4.2.x / 4.1.x / 6.5.1 | 软件工程 59 | 属于软件工程 59 | 🟢 优先跟进 (9) / 🟡 保留观察 (48) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (1) | 6.5.1 开发者认知、生产力与福祉 (17) / 7.1.1 代码生成、补全与变换 (10) | [venue](venues/icpc_conf_b.md) | [metadata](metadata/icpc_conf_b.json) | 计数一致；2025 与先验一致 |
| `ICSE` | International Conference on Software Engineering | `A` | `会议` | 245 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 245 | 属于软件工程 245 | 🟢 优先跟进 (75) / 🟡 保留观察 (166) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 7.1.1 代码生成、补全与变换 (43) / 7.1.2 AI 支持的测试、分析与修复 (28) | [venue](venues/icse_conf_a.md) | [metadata](metadata/icse_conf_a.json) | 计数一致；2025 与先验一致 |
| `ICSME` | International Conference on Software Maintenance and Evolution | `B` | `会议` | 102 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 4.3.x / 6.4.x | 软件工程 102 | 属于软件工程 102 | 🟢 优先跟进 (19) / 🟡 保留观察 (79) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 7.1.2 AI 支持的测试、分析与修复 (9) / 4.1.1 缺陷修复与维护性修正 (8) | [venue](venues/icsme_conf_b.md) | [metadata](metadata/icsme_conf_b.json) | 计数一致；2025 与先验一致 |
| `ICSOC` | International Conference on Service Oriented Computing | `B` | `会议` | 55 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 36 / 软件工程 17 / 系统软件 2 | 不属于软件工程 38 / 属于软件工程 9 / 跨域但软工主导 8 | 🟢 优先跟进 (4) / 🟡 保留观察 (0) / ⏳ 待补信息 (51) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (10) / 4.4.3 运行时重配置与自适应运维 (2) | [venue](venues/icsoc_conf_b.md) | [metadata](metadata/icsoc_conf_b.json) | 计数一致；2025 与先验一致 |
| `ICSR` | International Conference on Software Reuse | `C` | `会议` | 10 | 完全属于软工 | C 🟡 | 软件工程 | 1.4.x / 2.3.x / 4.1.x / 4.3.x | 软件工程 10 | 属于软件工程 10 | 🟢 优先跟进 (5) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (2) / 4.3.3 流水线与基础设施自动化 (1) | [venue](venues/icsr_conf_c.md) | [metadata](metadata/icsr_conf_c.json) | 计数一致；2025 与先验一致 |
| `ICSSP` | International Conference on Software and System Process | `C` | `会议` | 0 | 完全属于软工 | C 🟡 | 软件工程 | 6.1.x / 6.2.x / 6.5.x | 无 2025 条目 | 无 2025 条目 | 无 2025 条目 | 无纳入软工主路径 | [venue](venues/icssp_conf_c.md) | [metadata](metadata/icssp_conf_c.json) | 计数一致；2025 无条目，暂以先验为准 |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | `C` | `会议` | 101 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 软件工程 101 | 属于软件工程 101 | 🟢 优先跟进 (28) / 🟡 保留观察 (73) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.3 模糊、搜索式、变异与性质驱动测试 (17) / 3.1.4 场景化测试 (13) | [venue](venues/icst_conf_c.md) | [metadata](metadata/icst_conf_c.json) | 计数一致；2025 与先验一致 |
| `ICWS` | IEEE International Conference on Web Services | `B` | `会议` | 128 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 5.3.x / 8.2.3 | 跨域/待判定 72 / 系统软件 29 / 软件工程 25 / 程序设计语言与形式化基础 2 | 不属于软件工程 103 / 属于软件工程 21 / 跨域但软工主导 4 | 🟢 优先跟进 (25) / 🟡 保留观察 (87) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (10) | 2.1.4 云/服务/平台架构 (8) / 7.1.1 代码生成、补全与变换 (2) | [venue](venues/icws_conf_b.md) | [metadata](metadata/icws_conf_b.json) | 计数一致；2025 比先验更偏非软工 |
| `IETS` | IET Software | `B` | `期刊` | 35 | 大部分属于软工 | C 🟡 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 5.x.x | 软件工程 28 / 跨域/待判定 6 / 系统软件 1 | 属于软件工程 28 / 不属于软件工程 7 | 🟢 优先跟进 (10) / 🟡 保留观察 (22) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (1) | 3.1.4 场景化测试 (2) / 1.1.1 需求获取与发现 (2) | [venue](venues/iets_journal_b.md) | [metadata](metadata/iets_journal_b.json) | 计数一致；2025 与先验一致 |
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | `C` | `期刊` | 75 | 大部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 软件工程 55 / 跨域/待判定 18 / 程序设计语言与形式化基础 1 / 系统软件 1 | 属于软件工程 55 / 不属于软件工程 20 | 🟢 优先跟进 (17) / 🟡 保留观察 (54) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (1) | 7.1.1 代码生成、补全与变换 (10) / 6.3.4 replication、benchmark 与开放科学 (6) | [venue](venues/ijseke_journal_c.md) | [metadata](metadata/ijseke_journal_c.json) | 计数一致；2025 与先验一致 |
| `Internetware` | Asia-Pacific Symposium on Internetware | `C` | `会议` | 55 | 大部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.x | 软件工程 30 / 跨域/待判定 21 / 程序设计语言与形式化基础 2 / 系统软件 2 | 属于软件工程 30 / 不属于软件工程 25 | 🟢 优先跟进 (3) / 🟡 保留观察 (8) / ⏳ 待补信息 (44) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (10) / 7.1.1 代码生成、补全与变换 (2) | [venue](venues/internetware_conf_c.md) | [metadata](metadata/internetware_conf_c.json) | 计数一致；2025 比先验更偏非软工 |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | `B` | `会议` | 47 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x / 5.2.x / 4.4.x | 软件工程 47 | 属于软件工程 47 | 🟢 优先跟进 (10) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 3.3.3 assurance、认证与合规验证 (5) | [venue](venues/issre_conf_b.md) | [metadata](metadata/issre_conf_b.json) | 计数一致；2025 与先验一致 |
| `ISSTA` | International Symposium on Software Testing and Analysis | `A` | `会议` | 110 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 软件工程 110 | 属于软件工程 110 | 🟢 优先跟进 (45) / 🟡 保留观察 (65) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.3 模糊、搜索式、变异与性质驱动测试 (14) / 7.1.2 AI 支持的测试、分析与修复 (11) | [venue](venues/issta_conf_a.md) | [metadata](metadata/issta_conf_a.json) | 计数一致；2025 与先验一致 |
| `IST` | Information and Software Technology | `B` | `期刊` | 243 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 183 / 跨域/待判定 58 / 系统软件 2 | 属于软件工程 180 / 不属于软件工程 60 / 跨域但软工主导 3 | 🟢 优先跟进 (38) / 🟡 保留观察 (60) / ⏳ 待补信息 (136) / ⚪ 暂不跟进 (9) | 7.1.1 代码生成、补全与变换 (27) / 6.3.3 系统综述、mapping 与 meta-analysis (21) | [venue](venues/ist_journal_b.md) | [metadata](metadata/ist_journal_b.json) | 计数一致；2025 与先验一致 |
| `JSEP` | Journal of Software: Evolution and Process | `B` | `期刊` | 120 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.3.x / 6.1.x / 6.4.x | 软件工程 116 / 跨域/待判定 3 / 程序设计语言与形式化基础 1 | 属于软件工程 116 / 不属于软件工程 4 | 🟢 优先跟进 (30) / 🟡 保留观察 (83) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (4) | 6.1.1 敏捷、精益与 DevOps 方法 (12) / 6.3.3 系统综述、mapping 与 meta-analysis (7) | [venue](venues/jsep_journal_b.md) | [metadata](metadata/jsep_journal_b.json) | 计数一致；2025 与先验一致 |
| `JSS` | Journal of Systems and Software | `B` | `期刊` | 265 | 大部分属于软工 | B 🟢 | 软件工程 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 软件工程 190 / 跨域/待判定 71 / 程序设计语言与形式化基础 3 / 系统软件 1 | 属于软件工程 189 / 不属于软件工程 75 / 跨域但软工主导 1 | 🟢 优先跟进 (57) / 🟡 保留观察 (65) / ⏳ 待补信息 (134) / ⚪ 暂不跟进 (9) | 2.1.1 架构描述与恢复 (30) / 5.2.1 安全开发与漏洞治理 (13) | [venue](venues/jss_journal_b.md) | [metadata](metadata/jss_journal_b.json) | 计数一致；2025 与先验一致 |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | `B` | `会议` | 27 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 27 | 属于软件工程 27 | 🟢 优先跟进 (19) / 🟡 保留观察 (8) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (8) / 7.1.1 代码生成、补全与变换 (4) | [venue](venues/models_conf_b.md) | [metadata](metadata/models_conf_b.json) | 计数一致；2025 与先验一致 |
| `MSR` | Mining Software Repositories | `C` | `会议` | 109 | 完全属于软工 | B 🟢 | 软件工程 | 6.4.x / 6.3.x / 4.1.x / 6.5.x | 软件工程 109 | 属于软件工程 109 | 🟢 优先跟进 (13) / 🟡 保留观察 (90) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6) | 6.3.4 replication、benchmark 与开放科学 (48) / 4.1.1 缺陷修复与维护性修正 (8) | [venue](venues/msr_conf_c.md) | [metadata](metadata/msr_conf_c.json) | 计数一致；2025 与先验一致 |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages,and Applications | `A` | `会议` | 216 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 3.4.x / 4.2.x | 程序设计语言与形式化基础 165 / 软件工程 29 / 系统软件 22 | 不属于软件工程 187 / 属于软件工程 20 / 跨域但软工主导 9 | 🟢 优先跟进 (102) / 🟡 保留观察 (108) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6) | 3.1.3 模糊、搜索式、变异与性质驱动测试 (11) / 3.2.1 静态分析与抽象解释 (5) | [venue](venues/oopsla_conf_a.md) | [metadata](metadata/oopsla_conf_a.json) | 计数一致；2025 比先验更偏非软工 |
| `PASTE` | ACMSIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | `C` | `会议` | 0 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 3.2.x / 3.4.x / 4.2.x | 无 2025 条目 | 无 2025 条目 | 无 2025 条目 | 无纳入软工主路径 | [venue](venues/paste_conf_c.md) | [metadata](metadata/paste_conf_c.json) | 计数一致；2025 无条目，暂以先验为准 |
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | `A` | `会议` | 88 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 3.4.x | 程序设计语言与形式化基础 70 / 系统软件 15 / 软件工程 3 | 不属于软件工程 85 / 跨域但软工主导 2 / 属于软件工程 1 | 🟢 优先跟进 (37) / 🟡 保留观察 (44) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 3.2.3 面向质量属性的分析 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) | [venue](venues/pldi_conf_a.md) | [metadata](metadata/pldi_conf_a.json) | 计数一致；2025 比先验更偏非软工 |
| `QRS` | International Conference on Software Quality, Reliability and Security | `C` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 3.x.x / 5.1.x / 5.2.x / 4.4.x | 无 2025 条目 | 无 2025 条目 | 无 2025 条目 | 无纳入软工主路径 | [venue](venues/qrs_conf_c.md) | [metadata](metadata/qrs_conf_c.json) | 计数一致；2025 无条目，暂以先验为准 |
| `RE / 会议 / B` | IEEE International Requirements Engineering Conference | `B` | `会议` | 71 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x / 6.1.x | 软件工程 70 / 跨域/待判定 1 | 属于软件工程 70 / 不属于软件工程 1 | 🟢 优先跟进 (67) / 🟡 保留观察 (2) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 1.1.1 需求获取与发现 (24) / 7.1.3 AI 支持的需求、建模与文档 (8) | [venue](venues/re_conf_b.md) | [metadata](metadata/re_conf_b.json) | 计数一致；2025 与先验一致 |
| `RE / 期刊 / B` | Requirements Engineering | `B` | `期刊` | 9 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 9 | 属于软件工程 9 | 🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (3) / 7.1.3 AI 支持的需求、建模与文档 (1) | [venue](venues/re_journal_b.md) | [metadata](metadata/re_journal_b.json) | 计数一致；2025 与先验一致 |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | `C` | `会议` | 29 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 29 | 属于软件工程 29 | 🟢 优先跟进 (19) / 🟡 保留观察 (0) / ⏳ 待补信息 (10) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (20) / 6.3.1 实验、案例研究与调查 (2) | [venue](venues/refsq_conf_c.md) | [metadata](metadata/refsq_conf_c.json) | 计数一致；2025 与先验一致 |
| `RV` | International Conference on Runtime Verification | `C` | `会议` | 18 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.3.2 / 4.4.4 / 5.1.x | 程序设计语言与形式化基础 12 / 软件工程 5 / 系统软件 1 | 不属于软件工程 13 / 跨域但软工主导 4 / 属于软件工程 1 | 🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0) | 3.3.2 运行时验证与运行时监测 (5) | [venue](venues/rv_conf_c.md) | [metadata](metadata/rv_conf_c.json) | 计数一致；2025 与先验一致 |
| `SANER` | IEEE International Conference on Software Analysis, Evolution,and Reengineering | `B` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 3.2.x / 3.4.x | 无 2025 条目 | 无 2025 条目 | 无 2025 条目 | 无纳入软工主路径 | [venue](venues/saner_conf_b.md) | [metadata](metadata/saner_conf_b.json) | 计数一致；2025 无条目，暂以先验为准 |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | `C` | `会议` | 0 | 大部分属于软工 | B 🟢 | 软件工程 | 3.2.x / 4.2.x / 4.1.x / 3.4.x | 无 2025 条目 | 无 2025 条目 | 无 2025 条目 | 无纳入软工主路径 | [venue](venues/scam_conf_c.md) | [metadata](metadata/scam_conf_c.json) | 计数一致；2025 无条目，暂以先验为准 |
| `SCP` | Science of Computer Programming | `B` | `期刊` | 97 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 4.1.x | 程序设计语言与形式化基础 64 / 软件工程 29 / 系统软件 4 | 不属于软件工程 68 / 属于软件工程 18 / 跨域但软工主导 11 | 🟢 优先跟进 (32) / 🟡 保留观察 (11) / ⏳ 待补信息 (54) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (6) / 3.3.2 运行时验证与运行时监测 (3) | [venue](venues/scp_journal_b.md) | [metadata](metadata/scp_journal_b.json) | 计数一致；2025 与先验一致 |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | `C` | `会议` | 63 | 部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 跨域/待判定 36 / 软件工程 23 / 程序设计语言与形式化基础 3 / 系统软件 1 | 不属于软件工程 40 / 属于软件工程 18 / 跨域但软工主导 5 | 🟢 优先跟进 (14) / 🟡 保留观察 (31) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (7) | 7.1.2 AI 支持的测试、分析与修复 (4) / 3.1.4 场景化测试 (2) | [venue](venues/seke_conf_c.md) | [metadata](metadata/seke_conf_c.json) | 计数一致；2025 与先验一致 |
| `SOCA` | Service Oriented Computing and Applications | `C` | `期刊` | 24 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 8.2.3 | 跨域/待判定 24 | 不属于软件工程 24 | 🟢 优先跟进 (0) / 🟡 保留观察 (1) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0) | 无纳入软工主路径 | [venue](venues/soca_journal_c.md) | [metadata](metadata/soca_journal_c.json) | 计数一致；2025 比先验更偏非软工 |
| `SoSyM` | Software and Systems Modeling | `B` | `期刊` | 91 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 62 / 跨域/待判定 28 / 程序设计语言与形式化基础 1 | 属于软件工程 61 / 不属于软件工程 29 / 跨域但软工主导 1 | 🟢 优先跟进 (43) / 🟡 保留观察 (18) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (17) / 1.3.4 基于模型的生成、测试与运行时支持 (6) | [venue](venues/sosym_journal_b.md) | [metadata](metadata/sosym_journal_b.json) | 计数一致；2025 比先验更偏非软工 |
| `SPE` | Software: Practice and Experience | `B` | `期刊` | 109 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.3.x / 4.3.x / 4.4.x / 6.3.x / 8.2.x | 跨域/待判定 61 / 系统软件 26 / 软件工程 17 / 程序设计语言与形式化基础 5 | 不属于软件工程 92 / 属于软件工程 15 / 跨域但软工主导 2 | 🟢 优先跟进 (24) / 🟡 保留观察 (63) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (13) | 6.3.1 实验、案例研究与调查 (3) / 2.2.1 设计原则、模式与反模式 (2) | [venue](venues/spe_journal_b.md) | [metadata](metadata/spe_journal_b.json) | 计数一致；2025 比先验更偏非软工 |
| `SPIN` | International Symposium on Model Checking of Software | `C` | `会议` | 14 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x | 软件工程 8 / 程序设计语言与形式化基础 6 | 不属于软件工程 6 / 属于软件工程 5 / 跨域但软工主导 3 | 🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (3) / 1.3.3 模型分析、仿真与验证 (3) | [venue](venues/spin_conf_c.md) | [metadata](metadata/spin_conf_c.json) | 计数一致；2025 与先验一致 |
| `SQJ` | Software Quality Journal | `C` | `期刊` | 35 | 完全属于软工 | B 🟢 | 软件工程 | 5.x.x / 3.x.x / 6.3.x | 软件工程 29 / 跨域/待判定 6 | 属于软件工程 29 / 不属于软件工程 6 | 🟢 优先跟进 (8) / 🟡 保留观察 (7) / ⏳ 待补信息 (20) / ⚪ 暂不跟进 (0) | 3.4.2 缺陷定位、补丁生成与程序修复 (3) / 3.1.1 测试生成与增强 (3) | [venue](venues/sqj_journal_c.md) | [metadata](metadata/sqj_journal_c.json) | 计数一致；2025 与先验一致 |
| `SSE` | IEEE International Conference on Software Services Engineering | `C` | `会议` | 28 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 16 / 软件工程 10 / 程序设计语言与形式化基础 1 / 系统软件 1 | 不属于软件工程 18 / 属于软件工程 9 / 跨域但软工主导 1 | 🟢 优先跟进 (8) / 🟡 保留观察 (16) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 2.1.4 云/服务/平台架构 (5) / 4.4.1 可观测性、日志与异常检测 (1) | [venue](venues/sse_conf_c.md) | [metadata](metadata/sse_conf_c.json) | 计数一致；2025 与先验一致 |
| `STTT` | International Journal of Software Tools for Technology Transfer | `C` | `期刊` | 41 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 28 / 软件工程 12 / 系统软件 1 | 不属于软件工程 29 / 属于软件工程 6 / 跨域但软工主导 6 | 🟢 优先跟进 (18) / 🟡 保留观察 (9) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (3) | 3.2.1 静态分析与抽象解释 (3) / 6.3.1 实验、案例研究与调查 (1) | [venue](venues/sttt_journal_c.md) | [metadata](metadata/sttt_journal_c.json) | 计数一致；2025 与先验一致 |
| `STVR` | Software Testing, Verification and Reliability | `B` | `期刊` | 17 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x | 软件工程 17 | 属于软件工程 17 | 🟢 优先跟进 (6) / 🟡 保留观察 (11) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.3 模糊、搜索式、变异与性质驱动测试 (7) / 3.3.3 assurance、认证与合规验证 (3) | [venue](venues/stvr_journal_b.md) | [metadata](metadata/stvr_journal_b.json) | 计数一致；2025 与先验一致 |
| `TASE` | Theoretical Aspects of Software Engineering Conference | `C` | `会议` | 22 | 部分属于软工 | B 🟢 | 形式化方法与软件工程交叉 | 1.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 14 / 软件工程 8 | 不属于软件工程 14 / 跨域但软工主导 6 / 属于软件工程 2 | 🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (4) / 5.3.1 性能建模、基准与调优 (1) | [venue](venues/tase_conf_c.md) | [metadata](metadata/tase_conf_c.json) | 计数一致；2025 与先验一致 |
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | `A` | `期刊` | 242 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 241 / 跨域/待判定 1 | 属于软件工程 241 / 不属于软件工程 1 | 🟢 优先跟进 (79) / 🟡 保留观察 (156) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 7.1.1 代码生成、补全与变换 (45) / 6.3.5 路线图、研究议程与领域回顾 (23) | [venue](venues/tosem_journal_a.md) | [metadata](metadata/tosem_journal_a.json) | 计数一致；2025 与先验一致 |
| `TSC` | IEEE Transactions on Services Computing | `A` | `期刊` | 312 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 5.3.x / 8.2.x | 跨域/待判定 190 / 系统软件 88 / 软件工程 32 / 程序设计语言与形式化基础 2 | 不属于软件工程 280 / 属于软件工程 26 / 跨域但软工主导 6 | 🟢 优先跟进 (58) / 🟡 保留观察 (194) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (35) | 2.1.4 云/服务/平台架构 (9) / 6.2.1 估算、计划与排程 (5) | [venue](venues/tsc_journal_a.md) | [metadata](metadata/tsc_journal_a.json) | 计数一致；2025 比先验更偏非软工 |
| `TSE` | IEEE Transactions on Software Engineering | `A` | `期刊` | 228 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 224 / 跨域/待判定 3 / 系统软件 1 | 属于软件工程 224 / 不属于软件工程 4 | 🟢 优先跟进 (71) / 🟡 保留观察 (135) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (11) | 7.1.1 代码生成、补全与变换 (35) / 6.3.5 路线图、研究议程与领域回顾 (28) | [venue](venues/tse_journal_a.md) | [metadata](metadata/tse_journal_a.json) | 计数一致；2025 与先验一致 |
| `VMCAI` | International Conference on Verification,Model Checking, and Abstract Interpretation | `B` | `会议` | 21 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 14 / 软件工程 6 / 系统软件 1 | 不属于软件工程 15 / 跨域但软工主导 6 | 🟢 优先跟进 (5) / 🟡 保留观察 (0) / ⏳ 待补信息 (16) / ⚪ 暂不跟进 (0) | 3.2.1 静态分析与抽象解释 (1) / 3.3.2 运行时验证与运行时监测 (1) | [venue](venues/vmcai_conf_b.md) | [metadata](metadata/vmcai_conf_b.json) | 计数一致；2025 与先验一致 |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | `C` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 2.1.x / 2.2.x / 4.1.x | 无 2025 条目 | 无 2025 条目 | 无 2025 条目 | 无纳入软工主路径 | [venue](venues/wicsa_conf_c.md) | [metadata](metadata/wicsa_conf_c.json) | 计数一致；2025 无条目，暂以先验为准 |

## 6. Venue 导航

---

### `APSEC`

- 基本信息：
- 全称：Asia-Pacific Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`117`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 亚洲社区，`LLM-SE/测试/建模` 可见
- 初筛分布：🟢 优先跟进 (36) / 🟡 保留观察 (77) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/apsec_conf_c.md](./venues/apsec_conf_c.md)
- 数据文件：[metadata](metadata/apsec_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-apsec_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/apsec-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/apsec/
- 官方论文集页：https://doi.org/10.1109/APSEC66846.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/apsec_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (108) / 跨域/待判定 (8) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (108) / 不属于软件工程 (9)
- 初筛分布：🟢 优先跟进 (36) / 🟡 保留观察 (77) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (2)
- 判定来源分布：人工复核 (117)
- 人工复核状态分布：已人工复核 (117)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (23) / 6.3.4 replication、benchmark 与开放科学 (21) / 7.1.2 AI 支持的测试、分析与修复 (8) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (8) / 2.2.1 设计原则、模式与反模式 (4) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 4.2.1 代码搜索、导航与摘要 (3) / 6.4.3 度量、预测与风险模型 (3)
- 主题标签补充：建模/模型驱动 (64) / LLM/AI for SE (60) / 测试与验证 (49) / 可靠性/安全 (25) / 维护与演化 (24)

---

### `ASE / 会议 / A`

- 基本信息：
- 全称：International Conference on Automated Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2025`
- 条目数：`389`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (124) / 🟡 保留观察 (247) / ⏳ 待补信息 (13) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/ase_conf_a.md](./venues/ase_conf_a.md)
- 数据文件：[metadata](metadata/ase_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ase-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/kbse/
- 官方论文集页：https://doi.org/10.1109/ASE63991.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ase_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (387) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：属于软件工程 (387) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (124) / 🟡 保留观察 (247) / ⏳ 待补信息 (13) / ⚪ 暂不跟进 (5)
- 判定来源分布：人工复核 (389)
- 人工复核状态分布：已人工复核 (389)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (89) / 7.1.2 AI 支持的测试、分析与修复 (55) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (40) / 3.2.1 静态分析与抽象解释 (19) / 3.1.4 场景化测试 (15) / 7.1.4 AI 支持的架构、设计与工程决策 (14) / 3.1.1 测试生成与增强 (12) / 2.2.1 设计原则、模式与反模式 (10)
- 主题标签补充：LLM/AI for SE (202) / 测试与验证 (182) / 建模/模型驱动 (157) / 可靠性/安全 (85) / 维护与演化 (67)

---

### `ASE / 期刊 / B`

- 基本信息：
- 全称：Automated Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`74`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (13) / ⏳ 待补信息 (47) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/ase_journal_b.md](./venues/ase_journal_b.md)
- 数据文件：[metadata](metadata/ase_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10515
- 学术索引页：http://dblp.uni-trier.de/db/journals/ase/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ase_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (72) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (72) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (13) / ⏳ 待补信息 (47) / ⚪ 暂不跟进 (1)
- 判定来源分布：人工复核 (74)
- 人工复核状态分布：已人工复核 (74)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (14) / 7.1.2 AI 支持的测试、分析与修复 (7) / 3.1.4 场景化测试 (5) / 5.2.1 安全开发与漏洞治理 (4) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (4) / 1.3.3 模型分析、仿真与验证 (4) / 6.3.1 实验、案例研究与调查 (3) / 6.3.3 系统综述、mapping 与 meta-analysis (2)
- 主题标签补充：测试与验证 (21) / LLM/AI for SE (20) / 建模/模型驱动 (19) / 待人工细分 (17) / 可靠性/安全 (14)

---

### `CAiSE`

- 基本信息：
- 全称：International Conference on Advanced Information Systems Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`35`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：信息系统与过程/模型工程，适合补需求-建模-规约链
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/caise_conf_b.md](./venues/caise_conf_b.md)
- 数据文件：[metadata](metadata/caise_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-caise_conf_b)

- 关键信息页面：
- 年主页：https://conferences.big.tuwien.ac.at/caise2025/
- 学术索引页：http://dblp.uni-trier.de/db/conf/caise/
- 官方论文集页：https://doi.org/10.1007/978-3-031-94569-4 / https://doi.org/10.1007/978-3-031-94571-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/caise_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (29) / 软件工程 (5) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (30) / 跨域但软工主导 (3) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (35)
- 人工复核状态分布：已人工复核 (35)
- 高频软工主路径：1.3.1 建模语言与元模型 (2) / 6.1.2 过程挖掘、符合性与改进 (2) / 5.3.1 性能建模、基准与调优 (1)
- 主题标签补充：待人工细分 (15) / 建模/模型驱动 (9) / 运行时监测 (4) / 需求工程 (3) / LLM/AI for SE (3)

---

### `COMPSAC`

- 基本信息：
- 全称：International Computer Software and Applications Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`330`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：覆盖过宽，需按建模/验证/`AI4SE` 子题筛选
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (253) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (34)
- 论文名录页：[venues/compsac_conf_c.md](./venues/compsac_conf_c.md)
- 数据文件：[metadata](metadata/compsac_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-compsac_conf_c)

- 关键信息页面：
- 年主页：https://ieeecompsac.computer.org/2025/
- 学术索引页：http://dblp.uni-trier.de/db/conf/compsac/
- 官方论文集页：https://doi.org/10.1109/COMPSAC65507.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/compsac_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (231) / 软件工程 (61) / 系统软件 (32) / 程序设计语言与形式化基础 (6)
- 软工纳入判定分布：不属于软件工程 (269) / 属于软件工程 (47) / 跨域但软工主导 (14)
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (253) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (34)
- 判定来源分布：人工复核 (330)
- 人工复核状态分布：已人工复核 (330)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (6) / 4.1.1 缺陷修复与维护性修正 (4) / 3.1.4 场景化测试 (4) / 7.1.2 AI 支持的测试、分析与修复 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 6.2.2 风险、价值与优先级 (3) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 2.3.3 组件、包与集成工程 (2)
- 主题标签补充：建模/模型驱动 (190) / LLM/AI for SE (93) / 可靠性/安全 (80) / 测试与验证 (78) / 形式化方法 (56)

---

### `EASE`

- 基本信息：
- 全称：International Conference on Evaluation and Assessment in Software Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`126`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：评测与实验设计 / benchmark / replication 有用
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (87) / ⏳ 待补信息 (8) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/ease_conf_c.md](./venues/ease_conf_c.md)
- 数据文件：[metadata](metadata/ease_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ease_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ease-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/ease/
- 官方论文集页：https://doi.org/10.1145/3756681
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ease_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (122) / 跨域/待判定 (4)
- 软工纳入判定分布：属于软件工程 (122) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (87) / ⏳ 待补信息 (8) / ⚪ 暂不跟进 (6)
- 判定来源分布：人工复核 (126)
- 人工复核状态分布：已人工复核 (126)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (25) / 6.3.4 replication、benchmark 与开放科学 (20) / 4.1.1 缺陷修复与维护性修正 (8) / 7.1.1 代码生成、补全与变换 (7) / 7.1.2 AI 支持的测试、分析与修复 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (5) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (4) / 6.5.1 开发者认知、生产力与福祉 (4)
- 主题标签补充：建模/模型驱动 (53) / LLM/AI for SE (40) / 测试与验证 (38) / 维护与演化 (35) / 可靠性/安全 (35)

---

### `ECOOP`

- 基本信息：
- 全称：European Conference on Object-Oriented Programming
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`43`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`OO` 程序结构 / 分析与重构邻近
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (11) / ⏳ 待补信息 (26) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ecoop_conf_b.md](./venues/ecoop_conf_b.md)
- 数据文件：[metadata](metadata/ecoop_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ecoop_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ecoop-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/ecoop/
- 官方论文集页：https://www.dagstuhl.de/dagpub/978-3-95977-373-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ecoop_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (35) / 软件工程 (6) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (37) / 属于软件工程 (4) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (11) / ⏳ 待补信息 (26) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (43)
- 人工复核状态分布：已人工复核 (43)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (1) / 1.2.1 形式化规约与契约 (1) / 3.2.3 面向质量属性的分析 (1) / 3.2.1 静态分析与抽象解释 (1) / 3.2.2 动态与混合分析 (1) / 2.2.1 设计原则、模式与反模式 (1)
- 主题标签补充：待人工细分 (18) / 形式化方法 (12) / 程序设计语言/编译 (8) / 测试与验证 (8) / 可靠性/安全 (4)

---

### `ESE`

- 基本信息：
- 全称：Empirical Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`178`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证研究 / 数据集 / benchmark / 人因与评测设计
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (51) / ⏳ 待补信息 (103) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/ese_journal_b.md](./venues/ese_journal_b.md)
- 数据文件：[metadata](metadata/ese_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ese_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10664
- 学术索引页：http://dblp.uni-trier.de/db/journals/ese/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ese_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (144) / 跨域/待判定 (31) / 程序设计语言与形式化基础 (2) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (144) / 不属于软件工程 (34)
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (51) / ⏳ 待补信息 (103) / ⚪ 暂不跟进 (2)
- 判定来源分布：人工复核 (178)
- 人工复核状态分布：已人工复核 (178)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (33) / 4.1.1 缺陷修复与维护性修正 (25) / 3.2.3 面向质量属性的分析 (11) / 7.1.2 AI 支持的测试、分析与修复 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 6.5.2 协作、评审与知识共享 (6) / 6.3.4 replication、benchmark 与开放科学 (6) / 6.3.3 系统综述、mapping 与 meta-analysis (4)
- 主题标签补充：经验软件工程 (50) / 待人工细分 (48) / 建模/模型驱动 (40) / 可靠性/安全 (36) / 测试与验证 (32)

---

### `ESEM`

- 基本信息：
- 全称：International Symposium on Empirical Software Engineering and Measurement
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`58`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证方法 / 评测设计 / `LLM-SE` 实验口径重要
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/esem_conf_b.md](./venues/esem_conf_b.md)
- 数据文件：[metadata](metadata/esem_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-esem_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/esem-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/esem/
- 官方论文集页：https://doi.org/10.1109/ESEM64174.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/esem_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (58)
- 软工纳入判定分布：属于软件工程 (58)
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：人工复核 (58)
- 人工复核状态分布：已人工复核 (58)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (12) / 6.3.4 replication、benchmark 与开放科学 (9) / 6.5.2 协作、评审与知识共享 (4) / 7.1.1 代码生成、补全与变换 (3) / 6.5.3 开源社区、多样性与治理 (3) / 6.3.3 系统综述、mapping 与 meta-analysis (2) / 4.1.1 缺陷修复与维护性修正 (2) / 2.2.1 设计原则、模式与反模式 (2)
- 主题标签补充：建模/模型驱动 (25) / LLM/AI for SE (20) / 经验软件工程 (20) / 测试与验证 (18) / 可靠性/安全 (15)

---

### `FM`

- 基本信息：
- 全称：International Symposium on Formal Methods
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2025`
- 条目数：`67`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：形式化方法 / timed automata / 工业与控制系统验证邻近
- 初筛分布：🟢 优先跟进 (46) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/fm_conf_a.md](./venues/fm_conf_a.md)
- 数据文件：[metadata](metadata/fm_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-fm_conf_a)

- 关键信息页面：
- 年主页：未检出 standalone 2025 年主页
- 学术索引页：http://dblp.uni-trier.de/db/conf/fm/
- 官方论文集页：https://doi.org/10.1007/978-3-031-71162-6 / https://doi.org/10.1007/978-3-031-71177-0
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/fm_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (54) / 软件工程 (7) / 系统软件 (6)
- 软工纳入判定分布：不属于软件工程 (60) / 属于软件工程 (5) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (46) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：人工复核 (67)
- 人工复核状态分布：已人工复核 (67)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (3) / 3.2.4 分析驱动的理解、重构与综合 (1) / 3.4.2 缺陷定位、补丁生成与程序修复 (1) / 1.3.3 模型分析、仿真与验证 (1) / 7.1.1 代码生成、补全与变换 (1)
- 主题标签补充：形式化方法 (53) / 测试与验证 (29) / 建模/模型驱动 (23) / 需求工程 (21) / 程序分析 (7)

---

### `FSE`

- 基本信息：
- 全称：ACM International Conference on the Foundations of Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2025`
- 条目数：`132`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE + `LLM/需求建模/测试验证/修复` 主线
- 初筛分布：🟢 优先跟进 (39) / 🟡 保留观察 (92) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/fse_conf_a.md](./venues/fse_conf_a.md)
- 数据文件：[metadata](metadata/fse_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-fse_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/fse-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/sigsoft/
- 正式发布载体页：https://dl.acm.org/journal/pacmse
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/fse_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (131) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (131) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (39) / 🟡 保留观察 (92) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：人工复核 (132)
- 人工复核状态分布：已人工复核 (132)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (30) / 6.3.4 replication、benchmark 与开放科学 (15) / 7.1.2 AI 支持的测试、分析与修复 (11) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (8) / 7.1.4 AI 支持的架构、设计与工程决策 (7) / 3.1.4 场景化测试 (6) / 4.2.1 代码搜索、导航与摘要 (4) / 6.3.1 实验、案例研究与调查 (4)
- 主题标签补充：测试与验证 (56) / LLM/AI for SE (56) / 建模/模型驱动 (56) / 可靠性/安全 (40) / 维护与演化 (34)

---

### `ICECCS`

- 基本信息：
- 全称：International Conference on Engineering of Complex Computer Systems
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`22`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：复杂系统建模与验证 / safety-critical / CPS 邻近
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/iceccs_conf_c.md](./venues/iceccs_conf_c.md)
- 数据文件：[metadata](metadata/iceccs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iceccs_conf_c)

- 关键信息页面：
- 年主页：https://iceccs2025-hangzhou.github.io/
- 学术索引页：http://dblp.uni-trier.de/db/conf/iceccs/
- 官方论文集页：https://doi.org/10.1007/978-3-031-66456-4
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/iceccs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (16) / 软件工程 (6)
- 软工纳入判定分布：不属于软件工程 (16) / 属于软件工程 (3) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (22)
- 人工复核状态分布：已人工复核 (22)
- 高频软工主路径：1.3.1 建模语言与元模型 (1) / 3.3.1 面向软工问题的形式化验证 (1) / 4.1.5 技术债、克隆与可维护性治理 (1) / 6.3.1 实验、案例研究与调查 (1) / 3.1.1 测试生成与增强 (1) / 3.2.4 分析驱动的理解、重构与综合 (1)
- 主题标签补充：待人工细分 (9) / 测试与验证 (8) / 建模/模型驱动 (3) / LLM/AI for SE (2) / 程序修复 (2)

---

### `ICFEM`

- 基本信息：
- 全称：International Conference on Formal Engineering Methods
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`21`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：formal engineering / 规约建模 / 验证与证明
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icfem_conf_c.md](./venues/icfem_conf_c.md)
- 数据文件：[metadata](metadata/icfem_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icfem_conf_c)

- 关键信息页面：
- 年主页：https://icfem2025.github.io/
- 学术索引页：http://dblp.uni-trier.de/db/conf/icfem/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icfem_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (15) / 软件工程 (6)
- 软工纳入判定分布：不属于软件工程 (15) / 跨域但软工主导 (4) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (21)
- 人工复核状态分布：已人工复核 (21)
- 高频软工主路径：1.1.1 需求获取与发现 (1) / 3.2.1 静态分析与抽象解释 (1) / 6.3.1 实验、案例研究与调查 (1) / 3.3.1 面向软工问题的形式化验证 (1) / 1.2.1 形式化规约与契约 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：形式化方法 (11) / 建模/模型驱动 (9) / 测试与验证 (6) / LLM/AI for SE (5) / 待人工细分 (5)

---

### `ICPC`

- 基本信息：
- 全称：IEEE International Conference on Program Comprehension
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`59`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序理解 / 缺陷分析 / 修复解释与人因辅助
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (48) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/icpc_conf_b.md](./venues/icpc_conf_b.md)
- 数据文件：[metadata](metadata/icpc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icpc_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icpc-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/iwpc/
- 官方论文集页：https://doi.org/10.1109/ICPC66645.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icpc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (59)
- 软工纳入判定分布：属于软件工程 (59)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (48) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (1)
- 判定来源分布：人工复核 (59)
- 人工复核状态分布：已人工复核 (59)
- 高频软工主路径：6.5.1 开发者认知、生产力与福祉 (17) / 7.1.1 代码生成、补全与变换 (10) / 4.2.4 克隆、相似性与理解支持 (4) / 4.2.1 代码搜索、导航与摘要 (4) / 7.1.2 AI 支持的测试、分析与修复 (3) / 6.5.2 协作、评审与知识共享 (2) / 5.2.1 安全开发与漏洞治理 (2) / 6.3.4 replication、benchmark 与开放科学 (1)
- 主题标签补充：建模/模型驱动 (37) / LLM/AI for SE (26) / 维护与演化 (17) / 经验软件工程 (16) / 可靠性/安全 (13)

---

### `ICSE`

- 基本信息：
- 全称：International Conference on Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2025`
- 条目数：`245`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主会，需求-建模-验证-修复全链可见
- 初筛分布：🟢 优先跟进 (75) / 🟡 保留观察 (166) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/icse_conf_a.md](./venues/icse_conf_a.md)
- 数据文件：[metadata](metadata/icse_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icse_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icse-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icse/
- 官方论文集页：https://doi.org/10.1109/ICSE55347.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icse_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (245)
- 软工纳入判定分布：属于软件工程 (245)
- 初筛分布：🟢 优先跟进 (75) / 🟡 保留观察 (166) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：人工复核 (245)
- 人工复核状态分布：已人工复核 (245)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (43) / 7.1.2 AI 支持的测试、分析与修复 (28) / 6.3.4 replication、benchmark 与开放科学 (25) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (22) / 7.1.4 AI 支持的架构、设计与工程决策 (10) / 6.3.1 实验、案例研究与调查 (9) / 3.2.1 静态分析与抽象解释 (9) / 3.1.4 场景化测试 (7)
- 主题标签补充：测试与验证 (124) / LLM/AI for SE (101) / 建模/模型驱动 (92) / 可靠性/安全 (77) / 维护与演化 (47)

---

### `ICSME`

- 基本信息：
- 全称：International Conference on Software Maintenance and Evolution
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`102`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：维护演化 / 修复 / 回归验证 / 工程闭环邻近
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (79) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/icsme_conf_b.md](./venues/icsme_conf_b.md)
- 数据文件：[metadata](metadata/icsme_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsme_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icsme-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsm/
- 官方论文集页：https://doi.org/10.1109/ICSME64153.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsme_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (102)
- 软工纳入判定分布：属于软件工程 (102)
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (79) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：人工复核 (102)
- 人工复核状态分布：已人工复核 (102)
- 高频软工主路径：7.1.2 AI 支持的测试、分析与修复 (9) / 4.1.1 缺陷修复与维护性修正 (8) / 7.1.1 代码生成、补全与变换 (7) / 4.3.2 CI/CD 与发布工程 (6) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 4.1.2 重构、重模块化与代码清理 (6) / 7.1.3 AI 支持的需求、建模与文档 (5) / 4.3.1 版本、配置与构建工程 (4)
- 主题标签补充：LLM/AI for SE (43) / 测试与验证 (42) / 建模/模型驱动 (40) / 维护与演化 (40) / 可靠性/安全 (27)

---

### `ICSOC`

- 基本信息：
- 全称：International Conference on Service Oriented Computing
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`55`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务组合 / 流程 / 性质与治理偶有贴题
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (0) / ⏳ 待补信息 (51) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsoc_conf_b.md](./venues/icsoc_conf_b.md)
- 数据文件：[metadata](metadata/icsoc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsoc_conf_b)

- 关键信息页面：
- 年主页：http://icsoc2025.hit.edu.cn
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsoc/
- 官方论文集页：https://doi.org/10.1007/978-981-96-0805-8 / https://doi.org/10.1007/978-981-96-0808-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsoc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (36) / 软件工程 (17) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (38) / 属于软件工程 (9) / 跨域但软工主导 (8)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (0) / ⏳ 待补信息 (51) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (55)
- 人工复核状态分布：已人工复核 (55)
- 高频软工主路径：2.1.4 云/服务/平台架构 (10) / 4.4.3 运行时重配置与自适应运维 (2) / 5.3.1 性能建模、基准与调优 (1) / 6.2.1 估算、计划与排程 (1) / 7.1.3 AI 支持的需求、建模与文档 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 1.1.1 需求获取与发现 (1)
- 主题标签补充：待人工细分 (29) / 建模/模型驱动 (7) / LLM/AI for SE (7) / 可靠性/安全 (5) / 需求工程 (3)

---

### `ICSR`

- 基本信息：
- 全称：International Conference on Software Reuse
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`10`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：复用 / 组件资产，可补模型资产与可复用工件
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsr_conf_c.md](./venues/icsr_conf_c.md)
- 数据文件：[metadata](metadata/icsr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsr_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icsr-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsr/
- 官方论文集页：https://doi.org/10.1109/ICSR66718.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (10)
- 软工纳入判定分布：属于软件工程 (10)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (10)
- 人工复核状态分布：已人工复核 (10)
- 高频软工主路径：2.1.4 云/服务/平台架构 (2) / 4.3.3 流水线与基础设施自动化 (1) / 2.3.3 组件、包与集成工程 (1) / 3.1.4 场景化测试 (1) / 1.4.2 产品线架构与资产复用 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1) / 3.1.5 测试质量、脆弱性与测试资产维护 (1) / 1.2.4 合规与 assurance 规约 (1)
- 主题标签补充：需求工程 (4) / LLM/AI for SE (4) / 建模/模型驱动 (4) / 维护与演化 (4) / 系统软件 (3)

---

### `ICSSP`

- 基本信息：
- 全称：International Conference on Software and System Process
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件过程 / 团队与流程，对主问题较间接
- 初筛分布：无 2025 条目
- 论文名录页：[venues/icssp_conf_c.md](./venues/icssp_conf_c.md)
- 数据文件：[metadata](metadata/icssp_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icssp_conf_c)

- 关键信息页面：
- 年主页：未检出独立 2025 年主页
- 学术索引页：http://dblp.uni-trier.de/db/conf/ispw/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icssp_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `ICST`

- 基本信息：
- 全称：IEEE International Conference on Software Testing, Verification and Validation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`101`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 形式化验证 / 缺陷检测与修复直接相关
- 初筛分布：🟢 优先跟进 (28) / 🟡 保留观察 (73) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icst_conf_c.md](./venues/icst_conf_c.md)
- 数据文件：[metadata](metadata/icst_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icst_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icst-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icst/
- 官方论文集页：https://doi.org/10.1109/ICST62969.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icst_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (101)
- 软工纳入判定分布：属于软件工程 (101)
- 初筛分布：🟢 优先跟进 (28) / 🟡 保留观察 (73) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (101)
- 人工复核状态分布：已人工复核 (101)
- 高频软工主路径：3.1.3 模糊、搜索式、变异与性质驱动测试 (17) / 3.1.4 场景化测试 (13) / 3.1.1 测试生成与增强 (11) / 3.3.4 基准、工具评测与可复现验证 (11) / 2.3.3 组件、包与集成工程 (5) / 3.4.2 缺陷定位、补丁生成与程序修复 (5) / 3.2.3 面向质量属性的分析 (5) / 7.1.1 代码生成、补全与变换 (4)
- 主题标签补充：测试与验证 (92) / LLM/AI for SE (29) / 可靠性/安全 (28) / 建模/模型驱动 (26) / 维护与演化 (20)

---

### `ICWS`

- 基本信息：
- 全称：IEEE International Conference on Web Services
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`128`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：Web services / orchestration / 性质验证偶有贴题
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (87) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (10)
- 论文名录页：[venues/icws_conf_b.md](./venues/icws_conf_b.md)
- 数据文件：[metadata](metadata/icws_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icws_conf_b)

- 关键信息页面：
- 年主页：https://services.conferences.computer.org/2025/icws-2025/
- 学术索引页：http://dblp.uni-trier.de/db/conf/icws/
- 官方论文集页：https://doi.org/10.1109/ICWS67624.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icws_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (72) / 系统软件 (29) / 软件工程 (25) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：不属于软件工程 (103) / 属于软件工程 (21) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (87) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (10)
- 判定来源分布：人工复核 (128)
- 人工复核状态分布：已人工复核 (128)
- 高频软工主路径：2.1.4 云/服务/平台架构 (8) / 7.1.1 代码生成、补全与变换 (2) / 4.4.1 可观测性、日志与异常检测 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 7.1.2 AI 支持的测试、分析与修复 (1) / 4.2.2 痕迹、文档与知识恢复 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 3.4.1 调试、分诊与根因分析 (1)
- 主题标签补充：建模/模型驱动 (85) / LLM/AI for SE (47) / 可靠性/安全 (36) / 测试与验证 (22) / 需求工程 (19)

---

### `IETS`

- 基本信息：
- 全称：IET Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`35`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：broad SE 期刊，可筛少量建模/验证论文
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (22) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/iets_journal_b.md](./venues/iets_journal_b.md)
- 数据文件：[metadata](metadata/iets_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iets_journal_b)

- 关键信息页面：
- 期刊主页：https://ietresearch.onlinelibrary.wiley.com/journal/1751880x
- 学术索引页：https://dblp.uni-trier.de/db/journals/iet-sen
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/iets_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (28) / 跨域/待判定 (6) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (28) / 不属于软件工程 (7)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (22) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (1)
- 判定来源分布：人工复核 (35)
- 人工复核状态分布：已人工复核 (35)
- 高频软工主路径：3.1.4 场景化测试 (2) / 1.1.1 需求获取与发现 (2) / 6.3.4 replication、benchmark 与开放科学 (2) / 1.1.2 需求分析、协商与优先级 (2) / 7.1.1 代码生成、补全与变换 (2) / 4.1.1 缺陷修复与维护性修正 (1) / 8.5.4 异构与新型计算平台的软件工程 (1) / 7.1.3 AI 支持的需求、建模与文档 (1)
- 主题标签补充：建模/模型驱动 (24) / 测试与验证 (16) / 需求工程 (10) / LLM/AI for SE (6) / 可靠性/安全 (5)

---

### `IJSEKE`

- 基本信息：
- 全称：International Journal of Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`75`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 可补链但不稳定
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (54) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/ijseke_journal_c.md](./venues/ijseke_journal_c.md)
- 数据文件：[metadata](metadata/ijseke_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ijseke_journal_c)

- 关键信息页面：
- 期刊主页：https://www.worldscientific.com/worldscinet/ijseke
- 学术索引页：http://dblp.uni-trier.de/db/journals/ijseke/index.html
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ijseke_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (55) / 跨域/待判定 (18) / 系统软件 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (55) / 不属于软件工程 (20)
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (54) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (1)
- 判定来源分布：人工复核 (75)
- 人工复核状态分布：已人工复核 (75)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (10) / 6.3.4 replication、benchmark 与开放科学 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (6) / 7.1.2 AI 支持的测试、分析与修复 (4) / 1.1.1 需求获取与发现 (4) / 3.2.1 静态分析与抽象解释 (2) / 6.4.3 度量、预测与风险模型 (2) / 4.2.2 痕迹、文档与知识恢复 (1)
- 主题标签补充：建模/模型驱动 (42) / 测试与验证 (22) / 可靠性/安全 (20) / LLM/AI for SE (17) / 维护与演化 (13)

---

### `Internetware`

- 基本信息：
- 全称：Asia-Pacific Symposium on Internetware
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`55`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：平台 / 网络化软件 / 运行治理邻近
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (8) / ⏳ 待补信息 (44) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/internetware_conf_c.md](./venues/internetware_conf_c.md)
- 数据文件：[metadata](metadata/internetware_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-internetware_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/internetware-2025
- 学术索引页：https://dblp.org/db/conf/internetware/index.html
- 官方论文集页：https://doi.org/10.1145/3755881
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/internetware_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (30) / 跨域/待判定 (21) / 系统软件 (2) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：属于软件工程 (30) / 不属于软件工程 (25)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (8) / ⏳ 待补信息 (44) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (55)
- 人工复核状态分布：已人工复核 (55)
- 高频软工主路径：2.1.4 云/服务/平台架构 (10) / 7.1.1 代码生成、补全与变换 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 7.1.5 人机协同开发与评估 (2) / 5.2.1 安全开发与漏洞治理 (2) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 5.3.1 性能建模、基准与调优 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1)
- 主题标签补充：待人工细分 (16) / LLM/AI for SE (11) / 测试与验证 (10) / 可靠性/安全 (10) / 建模/模型驱动 (7)

---

### `ISSRE`

- 基本信息：
- 全称：IEEE International Symposium on Software Reliability Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`47`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：可靠性 / assurance / 安全关键验证与缺陷检测很近
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/issre_conf_b.md](./venues/issre_conf_b.md)
- 数据文件：[metadata](metadata/issre_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-issre_conf_b)

- 关键信息页面：
- 年主页：https://issre.github.io/2025/
- 学术索引页：http://dblp.uni-trier.de/db/conf/issre/
- 官方论文集页：https://doi.org/10.1109/ISSRE66568.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/issre_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (47)
- 软工纳入判定分布：属于软件工程 (47)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：人工复核 (47)
- 人工复核状态分布：已人工复核 (47)
- 高频软工主路径：3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 3.3.3 assurance、认证与合规验证 (5) / 7.1.2 AI 支持的测试、分析与修复 (4) / 5.2.1 安全开发与漏洞治理 (4) / 3.3.4 基准、工具评测与可复现验证 (3) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 3.1.1 测试生成与增强 (2) / 4.1.2 重构、重模块化与代码清理 (2)
- 主题标签补充：可靠性/安全 (23) / 建模/模型驱动 (20) / LLM/AI for SE (15) / 测试与验证 (14) / 形式化方法 (12)

---

### `ISSTA`

- 基本信息：
- 全称：International Symposium on Software Testing and Analysis
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2025`
- 条目数：`110`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试分析 / 形式化验证 / 缺陷定位与修复主场
- 初筛分布：🟢 优先跟进 (45) / 🟡 保留观察 (65) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/issta_conf_a.md](./venues/issta_conf_a.md)
- 数据文件：[metadata](metadata/issta_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-issta_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/issta-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/issta/
- 正式发布载体页：https://dl.acm.org/journal/pacmse
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/issta_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (110)
- 软工纳入判定分布：属于软件工程 (110)
- 初筛分布：🟢 优先跟进 (45) / 🟡 保留观察 (65) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (110)
- 人工复核状态分布：已人工复核 (110)
- 高频软工主路径：3.1.3 模糊、搜索式、变异与性质驱动测试 (14) / 7.1.2 AI 支持的测试、分析与修复 (11) / 3.2.3 面向质量属性的分析 (10) / 7.1.1 代码生成、补全与变换 (10) / 3.2.1 静态分析与抽象解释 (8) / 3.1.4 场景化测试 (6) / 3.1.1 测试生成与增强 (5) / 5.2.1 安全开发与漏洞治理 (5)
- 主题标签补充：测试与验证 (63) / LLM/AI for SE (50) / 可靠性/安全 (35) / 建模/模型驱动 (34) / 需求工程 (21)

---

### `IST`

- 基本信息：
- 全称：Information and Software Technology
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`243`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 建模测试 / `AI4SE` 论文较常见
- 初筛分布：🟢 优先跟进 (38) / 🟡 保留观察 (60) / ⏳ 待补信息 (136) / ⚪ 暂不跟进 (9)
- 论文名录页：[venues/ist_journal_b.md](./venues/ist_journal_b.md)
- 数据文件：[metadata](metadata/ist_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ist_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/information-and-software-technology
- 学术索引页：http://dblp.uni-trier.de/db/journals/infsof/index.html
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ist_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (183) / 跨域/待判定 (58) / 系统软件 (2)
- 软工纳入判定分布：属于软件工程 (180) / 不属于软件工程 (60) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (38) / 🟡 保留观察 (60) / ⏳ 待补信息 (136) / ⚪ 暂不跟进 (9)
- 判定来源分布：人工复核 (243)
- 人工复核状态分布：已人工复核 (243)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (27) / 6.3.3 系统综述、mapping 与 meta-analysis (21) / 6.1.1 敏捷、精益与 DevOps 方法 (16) / 1.1.1 需求获取与发现 (15) / 6.3.1 实验、案例研究与调查 (14) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (14) / 7.1.2 AI 支持的测试、分析与修复 (7) / 6.3.4 replication、benchmark 与开放科学 (6)
- 主题标签补充：建模/模型驱动 (79) / 待人工细分 (62) / 经验软件工程 (51) / 测试与验证 (42) / 可靠性/安全 (41)

---

### `JSEP`

- 基本信息：
- 全称：Journal of Software: Evolution and Process
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`120`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：演化 / 过程 / 迭代闭环与工程实践邻近
- 初筛分布：🟢 优先跟进 (30) / 🟡 保留观察 (83) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/jsep_journal_b.md](./venues/jsep_journal_b.md)
- 数据文件：[metadata](metadata/jsep_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jsep_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/20477481
- 学术索引页：http://dblp.uni-trier.de/db/journals/smr/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jsep_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (116) / 跨域/待判定 (3) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (116) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (30) / 🟡 保留观察 (83) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (4)
- 判定来源分布：人工复核 (120)
- 人工复核状态分布：已人工复核 (120)
- 高频软工主路径：6.1.1 敏捷、精益与 DevOps 方法 (12) / 6.3.3 系统综述、mapping 与 meta-analysis (7) / 6.3.4 replication、benchmark 与开放科学 (7) / 7.1.4 AI 支持的架构、设计与工程决策 (7) / 6.2.2 风险、价值与优先级 (6) / 6.3.1 实验、案例研究与调查 (6) / 6.4.3 度量、预测与风险模型 (5) / 5.2.1 安全开发与漏洞治理 (5)
- 主题标签补充：建模/模型驱动 (64) / 测试与验证 (47) / 可靠性/安全 (31) / 维护与演化 (31) / 经验软件工程 (24)

---

### `JSS`

- 基本信息：
- 全称：Journal of Systems and Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`265`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：系统与软件工程综合刊，常见建模/验证/CPS 个案
- 初筛分布：🟢 优先跟进 (57) / 🟡 保留观察 (65) / ⏳ 待补信息 (134) / ⚪ 暂不跟进 (9)
- 论文名录页：[venues/jss_journal_b.md](./venues/jss_journal_b.md)
- 数据文件：[metadata](metadata/jss_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jss_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/journal-of-systems-and-software
- 学术索引页：http://dblp.uni-trier.de/db/journals/jss/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jss_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (190) / 跨域/待判定 (71) / 程序设计语言与形式化基础 (3) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (189) / 不属于软件工程 (75) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (57) / 🟡 保留观察 (65) / ⏳ 待补信息 (134) / ⚪ 暂不跟进 (9)
- 判定来源分布：人工复核 (265)
- 人工复核状态分布：已人工复核 (265)
- 高频软工主路径：2.1.1 架构描述与恢复 (30) / 5.2.1 安全开发与漏洞治理 (13) / 7.1.4 AI 支持的架构、设计与工程决策 (8) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (7) / 6.1.1 敏捷、精益与 DevOps 方法 (7) / 4.1.5 技术债、克隆与可维护性治理 (7) / 2.2.1 设计原则、模式与反模式 (7) / 3.4.2 缺陷定位、补丁生成与程序修复 (7)
- 主题标签补充：建模/模型驱动 (75) / 待人工细分 (63) / 测试与验证 (63) / 可靠性/安全 (54) / 维护与演化 (43)

---

### `MoDELS`

- 基本信息：
- 全称：ACM/IEEE International Conference on Model Driven Engineering Languages and Systems
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`27`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：模型驱动 / 状态机-SysML / 形式化建模主场
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (8) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/models_conf_b.md](./venues/models_conf_b.md)
- 数据文件：[metadata](metadata/models_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-models_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/models-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/models/
- 官方论文集页：https://doi.org/10.1109/MODELS67397.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/models_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (27)
- 软工纳入判定分布：属于软件工程 (27)
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (8) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (27)
- 人工复核状态分布：已人工复核 (27)
- 高频软工主路径：1.3.1 建模语言与元模型 (8) / 7.1.1 代码生成、补全与变换 (4) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 3.3.4 基准、工具评测与可复现验证 (2) / 1.3.2 模型转换、同步与协同 (2) / 1.3.3 模型分析、仿真与验证 (2) / 4.3.2 CI/CD 与发布工程 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：建模/模型驱动 (23) / 测试与验证 (10) / 形式化方法 (9) / 维护与演化 (7) / 需求工程 (7)

---

### `MSR`

- 基本信息：
- 全称：Mining Software Repositories
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`109`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：仓库挖掘 / benchmark / `LLM-SE` 证据与数据建设有用
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (90) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/msr_conf_c.md](./venues/msr_conf_c.md)
- 数据文件：[metadata](metadata/msr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-msr_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/msr-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/msr/
- 官方论文集页：https://doi.org/10.1109/MSR66628.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/msr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (109)
- 软工纳入判定分布：属于软件工程 (109)
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (90) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 判定来源分布：人工复核 (109)
- 人工复核状态分布：已人工复核 (109)
- 高频软工主路径：6.3.4 replication、benchmark 与开放科学 (48) / 4.1.1 缺陷修复与维护性修正 (8) / 7.1.1 代码生成、补全与变换 (8) / 6.3.1 实验、案例研究与调查 (7) / 5.2.1 安全开发与漏洞治理 (5) / 2.2.1 设计原则、模式与反模式 (4) / 7.1.2 AI 支持的测试、分析与修复 (3) / 6.4.4 生态、依赖与开源分析 (3)
- 主题标签补充：经验软件工程 (44) / 维护与演化 (40) / 可靠性/安全 (35) / LLM/AI for SE (28) / 建模/模型驱动 (28)

---

### `OOPSLA`

- 基本信息：
- 全称：Conference on Object-Oriented Programming Systems, Languages,and Applications
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2025`
- 条目数：`216`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件结构 / 程序分析 / 重构与验证偶发贴题
- 初筛分布：🟢 优先跟进 (102) / 🟡 保留观察 (108) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/oopsla_conf_a.md](./venues/oopsla_conf_a.md)
- 数据文件：[metadata](metadata/oopsla_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-oopsla_conf_a)

- 关键信息页面：
- 年主页：https://2025.splashcon.org/track/oopsla
- 学术索引页：http://dblp.uni-trier.de/db/conf/oopsla/
- 正式发布载体页：https://dl.acm.org/journal/pacmpl
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/oopsla_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (165) / 软件工程 (29) / 系统软件 (22)
- 软工纳入判定分布：不属于软件工程 (187) / 属于软件工程 (20) / 跨域但软工主导 (9)
- 初筛分布：🟢 优先跟进 (102) / 🟡 保留观察 (108) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 判定来源分布：人工复核 (216)
- 人工复核状态分布：已人工复核 (216)
- 高频软工主路径：3.1.3 模糊、搜索式、变异与性质驱动测试 (11) / 3.2.1 静态分析与抽象解释 (5) / 2.2.1 设计原则、模式与反模式 (2) / 3.3.1 面向软工问题的形式化验证 (2) / 3.4.2 缺陷定位、补丁生成与程序修复 (2) / 7.1.1 代码生成、补全与变换 (1) / 3.3.2 运行时验证与运行时监测 (1) / 3.2.3 面向质量属性的分析 (1)
- 主题标签补充：形式化方法 (128) / 测试与验证 (97) / 程序设计语言/编译 (63) / 建模/模型驱动 (48) / 需求工程 (46)

---

### `PASTE`

- 基本信息：
- 全称：ACMSIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近
- 初筛分布：无 2025 条目
- 论文名录页：[venues/paste_conf_c.md](./venues/paste_conf_c.md)
- 数据文件：[metadata](metadata/paste_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-paste_conf_c)

- 关键信息页面：
- 年主页：无近 5 年 standalone 年主页
- 学术索引页：http://dblp.uni-trier.de/db/conf/paste/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/paste_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `PLDI`

- 基本信息：
- 全称：ACM SIGPLAN Conference on Programming Language Design and Implementation
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2025`
- 条目数：`88`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：程序分析 / 软件验证 / repair 邻近但需严格筛选
- 初筛分布：🟢 优先跟进 (37) / 🟡 保留观察 (44) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/pldi_conf_a.md](./venues/pldi_conf_a.md)
- 数据文件：[metadata](metadata/pldi_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-pldi_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/pldi-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/pldi/
- 正式发布载体页：https://dl.acm.org/journal/pacmpl
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/pldi_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (70) / 系统软件 (15) / 软件工程 (3)
- 软工纳入判定分布：不属于软件工程 (85) / 跨域但软工主导 (2) / 属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (37) / 🟡 保留观察 (44) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：人工复核 (88)
- 人工复核状态分布：已人工复核 (88)
- 高频软工主路径：3.2.3 面向质量属性的分析 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 7.1.1 代码生成、补全与变换 (1)
- 主题标签补充：形式化方法 (46) / 程序设计语言/编译 (42) / 测试与验证 (34) / 建模/模型驱动 (21) / 需求工程 (15)

---

### `QRS`

- 基本信息：
- 全称：International Conference on Software Quality, Reliability and Security
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：质量 / 可靠性 / 安全 / assurance 与验证链很近
- 初筛分布：无 2025 条目
- 论文名录页：[venues/qrs_conf_c.md](./venues/qrs_conf_c.md)
- 数据文件：[metadata](metadata/qrs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-qrs_conf_c)

- 关键信息页面：
- 年主页：https://qrs25.techconf.org/
- 学术索引页：https://dblp.uni-trier.de/db/conf/qrs
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/qrs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `RE / 会议 / B`

- 基本信息：
- 全称：IEEE International Requirements Engineering Conference
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`71`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (67) / 🟡 保留观察 (2) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/re_conf_b.md](./venues/re_conf_b.md)
- 数据文件：[metadata](metadata/re_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/re-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/re/
- 官方论文集页：https://doi.org/10.1109/RE63999.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/re_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (70) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (70) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (67) / 🟡 保留观察 (2) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：人工复核 (71)
- 人工复核状态分布：已人工复核 (71)
- 高频软工主路径：1.1.1 需求获取与发现 (24) / 7.1.3 AI 支持的需求、建模与文档 (8) / 1.1.4 需求追踪、变更与演化 (4) / 1.1.3 需求质量与歧义控制 (3) / 6.5.2 协作、评审与知识共享 (3) / 6.3.5 路线图、研究议程与领域回顾 (2) / 7.1.1 代码生成、补全与变换 (2) / 3.1.4 场景化测试 (2)
- 主题标签补充：需求工程 (67) / LLM/AI for SE (35) / 建模/模型驱动 (24) / 测试与验证 (18) / 形式化方法 (9)

---

### `RE / 期刊 / B`

- 基本信息：
- 全称：Requirements Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`9`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/re_journal_b.md](./venues/re_journal_b.md)
- 数据文件：[metadata](metadata/re_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/766
- 学术索引页：http://dblp.uni-trier.de/db/journals/re/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/re_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (9)
- 软工纳入判定分布：属于软件工程 (9)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (9)
- 人工复核状态分布：已人工复核 (9)
- 高频软工主路径：1.1.1 需求获取与发现 (3) / 7.1.3 AI 支持的需求、建模与文档 (1) / 3.2.3 面向质量属性的分析 (1) / 4.2.2 痕迹、文档与知识恢复 (1) / 1.3.1 建模语言与元模型 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 1.1.4 需求追踪、变更与演化 (1)
- 主题标签补充：需求工程 (8) / 建模/模型驱动 (6) / LLM/AI for SE (2) / 可靠性/安全 (1) / 测试与验证 (1)

---

### `REFSQ`

- 基本信息：
- 全称：Requirements Engineering: Foundation for Software Quality
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`29`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求质量 / 需求规约 / 需求到性质非常贴题
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (0) / ⏳ 待补信息 (10) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/refsq_conf_c.md](./venues/refsq_conf_c.md)
- 数据文件：[metadata](metadata/refsq_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-refsq_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/refsq-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/refsq/
- 官方论文集页：https://doi.org/10.1007/978-3-031-88531-0
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/refsq_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (29)
- 软工纳入判定分布：属于软件工程 (29)
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (0) / ⏳ 待补信息 (10) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (29)
- 人工复核状态分布：已人工复核 (29)
- 高频软工主路径：1.1.1 需求获取与发现 (20) / 6.3.1 实验、案例研究与调查 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (1) / 1.1.2 需求分析、协商与优先级 (1) / 7.1.3 AI 支持的需求、建模与文档 (1) / 5.4.3 人本评估与交互质量 (1) / 6.5.2 协作、评审与知识共享 (1) / 1.1.4 需求追踪、变更与演化 (1)
- 主题标签补充：需求工程 (20) / 建模/模型驱动 (6) / LLM/AI for SE (6) / 待人工细分 (3) / 维护与演化 (2)

---

### `RV`

- 基本信息：
- 全称：International Conference on Runtime Verification
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`18`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：运行时验证 / 监测 / 时序性质 / 工具链直接邻近
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/rv_conf_c.md](./venues/rv_conf_c.md)
- 数据文件：[metadata](metadata/rv_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-rv_conf_c)

- 关键信息页面：
- 年主页：https://rv25.isec.tugraz.at/
- 学术索引页：https://dblp.org/db/conf/rv/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-031-74234-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/rv_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (12) / 软件工程 (5) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (13) / 跨域但软工主导 (4) / 属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (18)
- 人工复核状态分布：已人工复核 (18)
- 高频软工主路径：3.3.2 运行时验证与运行时监测 (5)
- 主题标签补充：运行时监测 (10) / 形式化方法 (4) / 待人工细分 (4) / 测试与验证 (3) / 需求工程 (2)

---

### `SANER`

- 基本信息：
- 全称：IEEE International Conference on Software Analysis, Evolution,and Reengineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：代码分析 / 逆向 / 演化与 reengineering
- 初筛分布：无 2025 条目
- 论文名录页：[venues/saner_conf_b.md](./venues/saner_conf_b.md)
- 数据文件：[metadata](metadata/saner_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-saner_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/saner-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/wcre/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/saner_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `SCAM`

- 基本信息：
- 全称：IEEE International Working Conference on Source Code Analysis and Manipulation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`0`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：源码分析与变换 / 缺陷修复 / 程序理解邻近
- 初筛分布：无 2025 条目
- 论文名录页：[venues/scam_conf_c.md](./venues/scam_conf_c.md)
- 数据文件：[metadata](metadata/scam_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scam_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/scam-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/scam/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/scam_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `SCP`

- 基本信息：
- 全称：Science of Computer Programming
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`97`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件程序与形式化/验证/程序分析交叉，贴题概率中高
- 初筛分布：🟢 优先跟进 (32) / 🟡 保留观察 (11) / ⏳ 待补信息 (54) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/scp_journal_b.md](./venues/scp_journal_b.md)
- 数据文件：[metadata](metadata/scp_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scp_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/science-of-computer-programming
- 学术索引页：http://dblp.uni-trier.de/db/journals/scp/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/scp_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (64) / 软件工程 (29) / 系统软件 (4)
- 软工纳入判定分布：不属于软件工程 (68) / 属于软件工程 (18) / 跨域但软工主导 (11)
- 初筛分布：🟢 优先跟进 (32) / 🟡 保留观察 (11) / ⏳ 待补信息 (54) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (97)
- 人工复核状态分布：已人工复核 (97)
- 高频软工主路径：1.2.1 形式化规约与契约 (6) / 3.3.2 运行时验证与运行时监测 (3) / 3.3.1 面向软工问题的形式化验证 (3) / 1.3.4 基于模型的生成、测试与运行时支持 (3) / 2.1.4 云/服务/平台架构 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (1) / 3.4.1 调试、分诊与根因分析 (1) / 3.2.3 面向质量属性的分析 (1)
- 主题标签补充：形式化方法 (32) / 测试与验证 (32) / 待人工细分 (29) / 建模/模型驱动 (23) / 需求工程 (15)

---

### `SEKE`

- 基本信息：
- 全称：International Conference on Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`63`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 偶有贴题
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (31) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/seke_conf_c.md](./venues/seke_conf_c.md)
- 数据文件：[metadata](metadata/seke_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-seke_conf_c)

- 关键信息页面：
- 年主页：https://ksiresearch.org/seke/seke25.html
- 学术索引页：http://dblp.uni-trier.de/db/conf/seke/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/seke_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (36) / 软件工程 (23) / 程序设计语言与形式化基础 (3) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (40) / 属于软件工程 (18) / 跨域但软工主导 (5)
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (31) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (7)
- 判定来源分布：人工复核 (63)
- 人工复核状态分布：已人工复核 (63)
- 高频软工主路径：7.1.2 AI 支持的测试、分析与修复 (4) / 3.1.4 场景化测试 (2) / 6.3.4 replication、benchmark 与开放科学 (2) / 7.1.1 代码生成、补全与变换 (2) / 1.1.1 需求获取与发现 (1) / 6.5.4 教育、培训与入门支持 (1) / 2.2.2 模块化、依赖与解耦 (1) / 3.2.2 动态与混合分析 (1)
- 主题标签补充：建模/模型驱动 (35) / 测试与验证 (19) / LLM/AI for SE (17) / 形式化方法 (13) / 待人工细分 (11)

---

### `SOCA`

- 基本信息：
- 全称：Service Oriented Computing and Applications
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`24`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务计算与应用为主
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (1) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/soca_journal_c.md](./venues/soca_journal_c.md)
- 数据文件：[metadata](metadata/soca_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-soca_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11761
- 学术索引页：http://dblp.uni-trier.de/db/journals/soca/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/soca_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (24)
- 软工纳入判定分布：不属于软件工程 (24)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (1) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (24)
- 人工复核状态分布：已人工复核 (24)
- 主题标签补充：待人工细分 (14) / 建模/模型驱动 (7) / 可靠性/安全 (2) / 系统软件 (1) / 测试与验证 (1)

---

### `SoSyM`

- 基本信息：
- 全称：Software and Systems Modeling
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`91`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件与系统建模 / DSL / 状态机与模型分析主场
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (18) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sosym_journal_b.md](./venues/sosym_journal_b.md)
- 数据文件：[metadata](metadata/sosym_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sosym_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10270
- 学术索引页：http://dblp.uni-trier.de/db/journals/sosym/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sosym_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (62) / 跨域/待判定 (28) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (61) / 不属于软件工程 (29) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (18) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (91)
- 人工复核状态分布：已人工复核 (91)
- 高频软工主路径：1.3.1 建模语言与元模型 (17) / 1.3.4 基于模型的生成、测试与运行时支持 (6) / 1.3.2 模型转换、同步与协同 (4) / 1.1.1 需求获取与发现 (3) / 1.3.3 模型分析、仿真与验证 (3) / 1.3.5 模型质量、仓库与治理 (3) / 3.3.3 assurance、认证与合规验证 (3) / 7.1.4 AI 支持的架构、设计与工程决策 (3)
- 主题标签补充：建模/模型驱动 (69) / 需求工程 (23) / 维护与演化 (20) / 形式化方法 (20) / 测试与验证 (19)

---

### `SPE`

- 基本信息：
- 全称：Software: Practice and Experience
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`109`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：工程实践 / 系统实现为主，偶有 runtime/verification
- 初筛分布：🟢 优先跟进 (24) / 🟡 保留观察 (63) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (13)
- 论文名录页：[venues/spe_journal_b.md](./venues/spe_journal_b.md)
- 数据文件：[metadata](metadata/spe_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spe_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/1097024x
- 学术索引页：http://dblp.uni-trier.de/db/journals/spe/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/spe_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (61) / 系统软件 (26) / 软件工程 (17) / 程序设计语言与形式化基础 (5)
- 软工纳入判定分布：不属于软件工程 (92) / 属于软件工程 (15) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (24) / 🟡 保留观察 (63) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (13)
- 判定来源分布：人工复核 (109)
- 人工复核状态分布：已人工复核 (109)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (3) / 2.2.1 设计原则、模式与反模式 (2) / 2.1.1 架构描述与恢复 (1) / 1.3.1 建模语言与元模型 (1) / 6.3.3 系统综述、mapping 与 meta-analysis (1) / 2.1.4 云/服务/平台架构 (1) / 6.4.3 度量、预测与风险模型 (1) / 3.2.1 静态分析与抽象解释 (1)
- 主题标签补充：建模/模型驱动 (44) / 测试与验证 (26) / 经验软件工程 (22) / 需求工程 (20) / 形式化方法 (20)

---

### `SPIN`

- 基本信息：
- 全称：International Symposium on Model Checking of Software
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`14`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件模型检查 / state-based verification / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/spin_conf_c.md](./venues/spin_conf_c.md)
- 数据文件：[metadata](metadata/spin_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spin_conf_c)

- 关键信息页面：
- 年主页：https://spin-web.github.io/SPIN2025/cfp
- 学术索引页：http://dblp.uni-trier.de/db/conf/spin/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-031-66149-5
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/spin_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (8) / 程序设计语言与形式化基础 (6)
- 软工纳入判定分布：不属于软件工程 (6) / 属于软件工程 (5) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (14)
- 人工复核状态分布：已人工复核 (14)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (3) / 1.3.3 模型分析、仿真与验证 (3) / 3.4.2 缺陷定位、补丁生成与程序修复 (1) / 1.3.1 建模语言与元模型 (1)
- 主题标签补充：测试与验证 (6) / 形式化方法 (6) / 建模/模型驱动 (5) / 待人工细分 (3) / 维护与演化 (2)

---

### `SQJ`

- 基本信息：
- 全称：Software Quality Journal
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`35`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：质量 / 度量 / assurance 视角可支撑验证评价
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (7) / ⏳ 待补信息 (20) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sqj_journal_c.md](./venues/sqj_journal_c.md)
- 数据文件：[metadata](metadata/sqj_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sqj_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11219
- 学术索引页：http://dblp.uni-trier.de/db/journals/sqj/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sqj_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (29) / 跨域/待判定 (6)
- 软工纳入判定分布：属于软件工程 (29) / 不属于软件工程 (6)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (7) / ⏳ 待补信息 (20) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (35)
- 人工复核状态分布：已人工复核 (35)
- 高频软工主路径：3.4.2 缺陷定位、补丁生成与程序修复 (3) / 3.1.1 测试生成与增强 (3) / 6.4.3 度量、预测与风险模型 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 5.2.1 安全开发与漏洞治理 (2) / 3.2.3 面向质量属性的分析 (2) / 6.3.1 实验、案例研究与调查 (2) / 4.1.5 技术债、克隆与可维护性治理 (1)
- 主题标签补充：建模/模型驱动 (11) / 待人工细分 (10) / 测试与验证 (10) / 可靠性/安全 (8) / 维护与演化 (6)

---

### `SSE`

- 基本信息：
- 全称：IEEE International Conference on Software Services Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`28`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件服务工程混合
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (16) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/sse_conf_c.md](./venues/sse_conf_c.md)
- 数据文件：[metadata](metadata/sse_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sse_conf_c)

- 关键信息页面：
- 年主页：未检出 2025 年主页
- 学术索引页：http://dblp.uni-trier.de/db/conf/IEEEscc/
- 官方论文集页：https://doi.org/10.1109/SSE67621.2025
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/sse_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (16) / 软件工程 (10) / 系统软件 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (18) / 属于软件工程 (9) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (16) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：人工复核 (28)
- 人工复核状态分布：已人工复核 (28)
- 高频软工主路径：2.1.4 云/服务/平台架构 (5) / 4.4.1 可观测性、日志与异常检测 (1) / 4.2.1 代码搜索、导航与摘要 (1) / 8.2.3 服务系统与 API 生态 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 4.3.4 依赖、供应链与包生态治理 (1)
- 主题标签补充：建模/模型驱动 (14) / LLM/AI for SE (11) / 形式化方法 (9) / 需求工程 (7) / 可靠性/安全 (6)

---

### `STTT`

- 基本信息：
- 全称：International Journal of Software Tools for Technology Transfer
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`41`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：验证工具 / formal methods tool transfer / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (9) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/sttt_journal_c.md](./venues/sttt_journal_c.md)
- 数据文件：[metadata](metadata/sttt_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sttt_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10009
- 学术索引页：http://dblp.uni-trier.de/db/journals/sttt/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sttt_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (28) / 软件工程 (12) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (29) / 跨域但软工主导 (6) / 属于软件工程 (6)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (9) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (3)
- 判定来源分布：人工复核 (41)
- 人工复核状态分布：已人工复核 (41)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (3) / 6.3.1 实验、案例研究与调查 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 1.3.1 建模语言与元模型 (1) / 2.3.3 组件、包与集成工程 (1) / 3.2.3 面向质量属性的分析 (1) / 7.1.1 代码生成、补全与变换 (1) / 3.3.1 面向软工问题的形式化验证 (1)
- 主题标签补充：形式化方法 (17) / 测试与验证 (15) / 建模/模型驱动 (13) / 待人工细分 (8) / 程序分析 (6)

---

### `STVR`

- 基本信息：
- 全称：Software Testing, Verification and Reliability
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`17`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 验证 / 可靠性与 formal properties 非常贴题
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (11) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/stvr_journal_b.md](./venues/stvr_journal_b.md)
- 数据文件：[metadata](metadata/stvr_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-stvr_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/10991689
- 学术索引页：http://dblp.uni-trier.de/db/journals/stvr/index.html
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/stvr_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (17)
- 软工纳入判定分布：属于软件工程 (17)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (11) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (17)
- 人工复核状态分布：已人工复核 (17)
- 高频软工主路径：3.1.3 模糊、搜索式、变异与性质驱动测试 (7) / 3.3.3 assurance、认证与合规验证 (3) / 3.1.1 测试生成与增强 (2) / 1.2.1 形式化规约与契约 (1) / 6.3.3 系统综述、mapping 与 meta-analysis (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 3.3.2 运行时验证与运行时监测 (1) / 6.3.1 实验、案例研究与调查 (1)
- 主题标签补充：测试与验证 (13) / 建模/模型驱动 (8) / 可靠性/安全 (5) / 系统软件 (4) / 需求工程 (3)

---

### `TASE`

- 基本信息：
- 全称：Theoretical Aspects of Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`22`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件工程名下的 formal verification / assurance 邻近
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/tase_conf_c.md](./venues/tase_conf_c.md)
- 数据文件：[metadata](metadata/tase_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tase_conf_c)

- 关键信息页面：
- 年主页：https://cyprusconferences.org/tase2025/
- 学术索引页：http://dblp.uni-trier.de/db/conf/tase/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/tase_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (14) / 软件工程 (8)
- 软工纳入判定分布：不属于软件工程 (14) / 跨域但软工主导 (6) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (22)
- 人工复核状态分布：已人工复核 (22)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (4) / 5.3.1 性能建模、基准与调优 (1) / 1.2.1 形式化规约与契约 (1) / 3.1.1 测试生成与增强 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1)
- 主题标签补充：形式化方法 (9) / 待人工细分 (6) / 测试与验证 (6) / LLM/AI for SE (4) / 建模/模型驱动 (3)

---

### `TOSEM`

- 基本信息：
- 全称：ACM Transactions on Software Engineering and Methodology
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`242`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件工程方法 / 需求建模 / 测试验证 / `AI for SE`
- 初筛分布：🟢 优先跟进 (79) / 🟡 保留观察 (156) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/tosem_journal_a.md](./venues/tosem_journal_a.md)
- 数据文件：[metadata](metadata/tosem_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tosem_journal_a)

- 关键信息页面：
- 期刊主页：https://dl.acm.org/journal/tosem
- 学术索引页：http://dblp.uni-trier.de/db/journals/tosem/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tosem_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (241) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (241) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (79) / 🟡 保留观察 (156) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：人工复核 (242)
- 人工复核状态分布：已人工复核 (242)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (45) / 6.3.5 路线图、研究议程与领域回顾 (23) / 6.3.4 replication、benchmark 与开放科学 (22) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (21) / 6.3.1 实验、案例研究与调查 (13) / 7.1.2 AI 支持的测试、分析与修复 (12) / 3.1.4 场景化测试 (8) / 7.1.4 AI 支持的架构、设计与工程决策 (7)
- 主题标签补充：测试与验证 (106) / 建模/模型驱动 (104) / LLM/AI for SE (77) / 可靠性/安全 (70) / 维护与演化 (65)

---

### `TSC`

- 基本信息：
- 全称：IEEE Transactions on Services Computing
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`312`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务工作流 / 平台 orchestration 邻近，可补性质工程
- 初筛分布：🟢 优先跟进 (58) / 🟡 保留观察 (194) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (35)
- 论文名录页：[venues/tsc_journal_a.md](./venues/tsc_journal_a.md)
- 数据文件：[metadata](metadata/tsc_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tsc_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=4629386
- 学术索引页：http://dblp.uni-trier.de/db/journals/tsc/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tsc_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (190) / 系统软件 (88) / 软件工程 (32) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：不属于软件工程 (280) / 属于软件工程 (26) / 跨域但软工主导 (6)
- 初筛分布：🟢 优先跟进 (58) / 🟡 保留观察 (194) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (35)
- 判定来源分布：人工复核 (312)
- 人工复核状态分布：已人工复核 (312)
- 高频软工主路径：2.1.4 云/服务/平台架构 (9) / 6.2.1 估算、计划与排程 (5) / 5.3.4 扩展性、吞吐与时延保证 (3) / 3.1.4 场景化测试 (2) / 4.4.3 运行时重配置与自适应运维 (2) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 8.2.3 服务系统与 API 生态 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1)
- 主题标签补充：建模/模型驱动 (157) / 可靠性/安全 (102) / 系统软件 (81) / 程序设计语言/编译 (66) / 测试与验证 (43)

---

### `TSE`

- 基本信息：
- 全称：IEEE Transactions on Software Engineering
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2025`
- 条目数：`228`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主刊 / 建模验证修复与 `LLM` 子题持续出现
- 初筛分布：🟢 优先跟进 (71) / 🟡 保留观察 (135) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (11)
- 论文名录页：[venues/tse_journal_a.md](./venues/tse_journal_a.md)
- 数据文件：[metadata](metadata/tse_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tse_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32
- 学术索引页：http://dblp.uni-trier.de/db/journals/tse/
- 2025 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tse_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (224) / 跨域/待判定 (3) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (224) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (71) / 🟡 保留观察 (135) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (11)
- 判定来源分布：人工复核 (228)
- 人工复核状态分布：已人工复核 (228)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (35) / 6.3.5 路线图、研究议程与领域回顾 (28) / 7.1.2 AI 支持的测试、分析与修复 (23) / 6.3.4 replication、benchmark 与开放科学 (21) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (12) / 7.1.4 AI 支持的架构、设计与工程决策 (11) / 6.3.1 实验、案例研究与调查 (6) / 3.1.4 场景化测试 (6)
- 主题标签补充：建模/模型驱动 (89) / 测试与验证 (86) / LLM/AI for SE (76) / 维护与演化 (60) / 可靠性/安全 (48)

---

### `VMCAI`

- 基本信息：
- 全称：International Conference on Verification,Model Checking, and Abstract Interpretation
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2025`
- 条目数：`21`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：程序验证 / 模型检查 / 抽象解释直接支撑验证框架
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (0) / ⏳ 待补信息 (16) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/vmcai_conf_b.md](./venues/vmcai_conf_b.md)
- 数据文件：[metadata](metadata/vmcai_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-vmcai_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/vmcai-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/vmcai/
- 官方论文集页：https://doi.org/10.1007/978-3-031-82700-6 / https://doi.org/10.1007/978-3-031-82703-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/vmcai_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (14) / 软件工程 (6) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (15) / 跨域但软工主导 (6)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (0) / ⏳ 待补信息 (16) / ⚪ 暂不跟进 (0)
- 判定来源分布：人工复核 (21)
- 人工复核状态分布：已人工复核 (21)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (1) / 3.3.2 运行时验证与运行时监测 (1) / 1.2.1 形式化规约与契约 (1) / 3.3.1 面向软工问题的形式化验证 (1) / 6.3.1 实验、案例研究与调查 (1) / 3.4.2 缺陷定位、补丁生成与程序修复 (1)
- 主题标签补充：待人工细分 (9) / 形式化方法 (6) / 测试与验证 (3) / 系统软件 (2) / 程序分析 (1)

---

### `WICSA`

- 基本信息：
- 全称：Working IEEE/IFIP Conference on Software Architecture
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2025`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件架构 / 设计决策 / 模型结构与演化有用
- 初筛分布：无 2025 条目
- 论文名录页：[venues/wicsa_conf_c.md](./venues/wicsa_conf_c.md)
- 数据文件：[metadata](metadata/wicsa_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-wicsa_conf_c)

- 关键信息页面：
- 年主页：已并入 ICSA，请改跟踪 ICSA 年主页
- 学术索引页：http://dblp.uni-trier.de/db/conf/wicsa/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/wicsa_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

## 7. 本年度总体观察

- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (1408) / 🟡 保留观察 (2645) / ⏳ 待补信息 (899) / ⚪ 暂不跟进 (201)
- 一级总判定分布：软件工程 (3430) / 跨域/待判定 (972) / 程序设计语言与形式化基础 (510) / 系统软件 (241)
- 软工纳入判定分布：属于软件工程 (3324) / 不属于软件工程 (1723) / 跨域但软工主导 (106)
- 判定来源分布：人工复核 (5153)
- 人工复核状态分布：已人工复核 (5153)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (398) / 6.3.4 replication、benchmark 与开放科学 (229) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (222) / 7.1.2 AI 支持的测试、分析与修复 (218) / 6.3.1 实验、案例研究与调查 (169) / 7.1.4 AI 支持的架构、设计与工程决策 (112) / 1.1.1 需求获取与发现 (102) / 3.1.4 场景化测试 (101) / 4.1.1 缺陷修复与维护性修正 (82) / 3.2.1 静态分析与抽象解释 (76) / 5.2.1 安全开发与漏洞治理 (70) / 3.2.3 面向质量属性的分析 (68) / 2.1.4 云/服务/平台架构 (63) / 2.2.1 设计原则、模式与反模式 (62) / 6.3.5 路线图、研究议程与领域回顾 (61)
- 计数复核状态：以 [verification.json](./verification.json) 为准；默认要求 `expected_total == actual_total`。
- 分类终判状态：以 `metadata/*.json` 中的 `classification_source / manual_review_status / manual_review_note` 为准。
- 后续若继续扩年份或重跑年度页，建议先运行 `tools/ccf_se_index_builder.py`，再运行 `tools/ccf_se_classifier.py`。
