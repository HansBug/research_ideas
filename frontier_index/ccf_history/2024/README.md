# `2024` 年度汇总

## 1. 年份说明

- 年份：`2024`
- 覆盖范围：`CCF_SE_A_B_C.md` 当前保留的 `CCF` 软件工程高相关 venue 子集
- 当前覆盖的 venue 数量：`57`
- 当前已入表论文数量：`4763`
- 更新时间：`2026-04-07 00:10`
- 说明：本页先由 `tools/ccf_se_index_builder.py` 生成基础元数据，再由 `tools/ccf_se_classifier.py` 对未终判条目做启发式初判；若 `metadata/*.json` 中已写回人工终判，则直接保留该终判。逐篇论文名录拆分到 `venues/*.md`。

## 2. 年度汇总统计

- A 类会议：`861`
- A 类期刊：`728`
- B 类会议：`677`
- B 类期刊：`1166`
- C 类会议：`1126`
- C 类期刊：`205`
- 期望总条目数：`4763`
- 实际总条目数：`4763`
- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (1229) / 🟡 保留观察 (2474) / ⏳ 待补信息 (765) / ⚪ 暂不跟进 (295)
- 一级总判定分布：软件工程 (2890) / 跨域/待判定 (1197) / 程序设计语言与形式化基础 (438) / 系统软件 (238)
- 软工纳入判定分布：属于软件工程 (2798) / 不属于软件工程 (1873) / 跨域但软工主导 (92)
- 判定来源分布：启发式初判 (4763)
- 人工复核状态分布：未人工复核 (4763)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (306) / 6.3.1 实验、案例研究与调查 (191) / 6.3.4 replication、benchmark 与开放科学 (186) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (173) / 7.1.2 AI 支持的测试、分析与修复 (120) / 4.1.1 缺陷修复与维护性修正 (112) / 7.1.4 AI 支持的架构、设计与工程决策 (107) / 3.1.4 场景化测试 (98) / 1.1.1 需求获取与发现 (94) / 3.2.1 静态分析与抽象解释 (78) / 3.2.3 面向质量属性的分析 (77) / 2.1.4 云/服务/平台架构 (69)

## 3. 标准口径

- `软工归属级别` 统一使用 [CCF_SE_A_B_C.md](../../CCF_SE_A_B_C.md) 中的 `完全属于软工 / 大部分属于软工 / 部分属于软工`。
- `氛围` 统一使用 [CCF_SE_A_B_C.md](../../CCF_SE_A_B_C.md) 中的 `A 🔥 / B 🟢 / C 🟡`。
- 若需要表达 venue 的持续跟踪优先级，直接复用 `氛围`；同档再参考 `软工归属级别`，不要再另造 `A/B/C/D` 或其他四级制。
- 逐篇论文层面不再额外发明 `A/B/C/D` 第二套等级；论文名录只按现有 `初筛` 优先级 `🟢 -> 🟡 -> ⏳ -> ⚪` 排序。

## 4. 投稿时间线资料

- 总入口：[../SUBMISSION_TIMELINES.md](../SUBMISSION_TIMELINES.md)
- 会议 venue：默认看最近 `5` 年 `摘要截止 / 投稿截止 / rebuttal / 通知 / camera-ready / 会期`。
- 期刊 venue：默认看滚动投稿与 special issue 提醒，不机械构造 conference 式年度 `CFP`。
- 本页每个 venue 导航 section 与对应 `venues/*.md` 都附了该 venue 的时间线锚点。

## 5. 覆盖 venue 列表

- 口径：当前年度页只覆盖 [CCF_SE_A_B_C.md](../../CCF_SE_A_B_C.md) 中保留的 venue。
- `主体归属`、`软工归属级别`、`氛围` 与 `典型软工路径（先验）` 来自 venue 级先验；`2024` 逐篇统计直接按本年度 `metadata/*.json` 中的终判字段汇总。
- `典型软工路径（先验）` 与 `2024 高频软工主路径` 使用 [SOFTWARE_ENGINEERING_FIELD_TREE.md](../../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的方向树口径。

| venue | 全称 | 等级 | 类型 | 论文数 | 软工归属级别 | 氛围 | 主体归属 | 典型软工路径（先验） | 当年一级总判定 | 当年软工纳入 | 初筛分布 | 当年高频软工主路径 | 论文名录 | 数据文件 | 备注 |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | `A` | `会议` | 89 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 3.4.x | 程序设计语言与形式化基础 71 / 系统软件 10 / 软件工程 8 | 不属于软件工程 81 / 属于软件工程 7 / 跨域但软工主导 1 | 🟢 优先跟进 (41) / 🟡 保留观察 (40) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8) | 3.2.1 静态分析与抽象解释 (4) / 3.2.3 面向质量属性的分析 (1) | [venue](venues/pldi_conf_a.md) | [metadata](metadata/pldi_conf_a.json) | 计数一致；2024 比先验更偏非软工 |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | `A` | `会议` | 121 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 121 | 属于软件工程 121 | 🟢 优先跟进 (43) / 🟡 保留观察 (75) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 7.1.1 代码生成、补全与变换 (25) / 6.3.4 replication、benchmark 与开放科学 (18) | [venue](venues/fse_conf_a.md) | [metadata](metadata/fse_conf_a.json) | 计数一致；2024 与先验一致 |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages, and Applications | `A` | `会议` | 148 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 3.4.x / 4.2.x | 程序设计语言与形式化基础 118 / 软件工程 19 / 系统软件 11 | 不属于软件工程 129 / 属于软件工程 14 / 跨域但软工主导 5 | 🟢 优先跟进 (56) / 🟡 保留观察 (77) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (15) | 3.2.1 静态分析与抽象解释 (4) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) | [venue](venues/oopsla_conf_a.md) | [metadata](metadata/oopsla_conf_a.json) | 计数一致；2024 比先验更偏非软工 |
| `ASE / 会议 / A` | International Conference on Automated Software Engineering | `A` | `会议` | 266 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 261 / 跨域/待判定 3 / 程序设计语言与形式化基础 1 / 系统软件 1 | 属于软件工程 261 / 不属于软件工程 5 | 🟢 优先跟进 (73) / 🟡 保留观察 (175) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (16) | 7.1.1 代码生成、补全与变换 (75) / 7.1.2 AI 支持的测试、分析与修复 (23) | [venue](venues/ase_conf_a.md) | [metadata](metadata/ase_conf_a.json) | 计数一致；2024 与先验一致 |
| `ICSE` | International Conference on Software Engineering | `A` | `会议` | 237 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 227 / 跨域/待判定 8 / 程序设计语言与形式化基础 1 / 系统软件 1 | 属于软件工程 227 / 不属于软件工程 10 | 🟢 优先跟进 (75) / 🟡 保留观察 (154) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8) | 7.1.1 代码生成、补全与变换 (49) / 7.1.2 AI 支持的测试、分析与修复 (18) | [venue](venues/icse_conf_a.md) | [metadata](metadata/icse_conf_a.json) | 计数一致；2024 与先验一致 |
| `ISSTA` | International Symposium on Software Testing and Analysis | `A` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 无 2024 条目 | 无 2024 条目 | 无 2024 条目 | 无纳入软工主路径 | [venue](venues/issta_conf_a.md) | [metadata](metadata/issta_conf_a.json) | 计数一致；2024 无条目，暂以先验为准 |
| `FM` | International Symposium on Formal Methods | `A` | `会议` | 0 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 无 2024 条目 | 无 2024 条目 | 无 2024 条目 | 无纳入软工主路径 | [venue](venues/fm_conf_a.md) | [metadata](metadata/fm_conf_a.json) | 计数一致；2024 无条目，暂以先验为准 |
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | `A` | `期刊` | 223 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 217 / 跨域/待判定 6 | 属于软件工程 217 / 不属于软件工程 6 | 🟢 优先跟进 (66) / 🟡 保留观察 (148) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (8) | 7.1.1 代码生成、补全与变换 (34) / 6.3.4 replication、benchmark 与开放科学 (26) | [venue](venues/tosem_journal_a.md) | [metadata](metadata/tosem_journal_a.json) | 计数一致；2024 与先验一致 |
| `TSE` | IEEE Transactions on Software Engineering | `A` | `期刊` | 182 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 177 / 跨域/待判定 5 | 属于软件工程 177 / 不属于软件工程 5 | 🟢 优先跟进 (61) / 🟡 保留观察 (114) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 7.1.1 代码生成、补全与变换 (31) / 6.3.4 replication、benchmark 与开放科学 (15) | [venue](venues/tse_journal_a.md) | [metadata](metadata/tse_journal_a.json) | 计数一致；2024 与先验一致 |
| `TSC` | IEEE Transactions on Services Computing | `A` | `期刊` | 323 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 5.3.x / 8.2.x | 跨域/待判定 201 / 系统软件 92 / 软件工程 30 | 不属于软件工程 293 / 属于软件工程 27 / 跨域但软工主导 3 | 🟢 优先跟进 (76) / 🟡 保留观察 (213) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (34) | 2.1.4 云/服务/平台架构 (9) / 6.2.1 估算、计划与排程 (6) | [venue](venues/tsc_journal_a.md) | [metadata](metadata/tsc_journal_a.json) | 计数一致；2024 比先验更偏非软工 |
| `ECOOP` | European Conference on Object-Oriented Programming | `B` | `会议` | 48 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 4.2.x | 程序设计语言与形式化基础 41 / 系统软件 5 / 软件工程 2 | 不属于软件工程 46 / 跨域但软工主导 2 | 🟢 优先跟进 (11) / 🟡 保留观察 (13) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (1) | 3.2.1 静态分析与抽象解释 (2) | [venue](venues/ecoop_conf_b.md) | [metadata](metadata/ecoop_conf_b.json) | 计数一致；2024 比先验更偏非软工 |
| `ICPC` | IEEE International Conference on Program Comprehension | `B` | `会议` | 46 | 完全属于软工 | B 🟢 | 软件工程 | 4.2.x / 4.1.x / 6.5.1 | 软件工程 45 / 跨域/待判定 1 | 属于软件工程 45 / 不属于软件工程 1 | 🟢 优先跟进 (5) / 🟡 保留观察 (38) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (2) | 6.5.1 开发者认知、生产力与福祉 (15) / 7.1.1 代码生成、补全与变换 (7) | [venue](venues/icpc_conf_b.md) | [metadata](metadata/icpc_conf_b.json) | 计数一致；2024 与先验一致 |
| `RE / 会议 / B` | IEEE International Requirements Engineering Conference | `B` | `会议` | 60 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x / 6.1.x | 软件工程 60 | 属于软件工程 60 | 🟢 优先跟进 (55) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (19) / 6.3.1 实验、案例研究与调查 (3) | [venue](venues/re_conf_b.md) | [metadata](metadata/re_conf_b.json) | 计数一致；2024 与先验一致 |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | `B` | `会议` | 36 | 部分属于软工 | B 🟢 | 信息系统工程与软件工程交叉 | 1.3.x / 2.1.x / 4.3.x / 8.3.x | 跨域/待判定 26 / 软件工程 9 / 系统软件 1 | 不属于软件工程 27 / 跨域但软工主导 5 / 属于软件工程 4 | 🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0) | 6.1.2 过程挖掘、符合性与改进 (3) / 6.2.4 组合治理与决策支持 (1) | [venue](venues/caise_conf_b.md) | [metadata](metadata/caise_conf_b.json) | 计数一致；2024 与先验一致 |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | `B` | `会议` | 26 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 24 / 跨域/待判定 2 | 属于软件工程 24 / 不属于软件工程 2 | 🟢 优先跟进 (18) / 🟡 保留观察 (8) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (10) / 3.3.2 运行时验证与运行时监测 (2) | [venue](venues/models_conf_b.md) | [metadata](metadata/models_conf_b.json) | 计数一致；2024 与先验一致 |
| `ICSOC` | International Conference on Service Oriented Computing | `B` | `会议` | 58 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 45 / 软件工程 12 / 系统软件 1 | 不属于软件工程 46 / 跨域但软工主导 7 / 属于软件工程 5 | 🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (57) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (7) / 1.1.1 需求获取与发现 (1) | [venue](venues/icsoc_conf_b.md) | [metadata](metadata/icsoc_conf_b.json) | 计数一致；2024 比先验更偏非软工 |
| `SANER` | IEEE International Conference on Software Analysis, Evolution, and Reengineering | `B` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 3.2.x / 3.4.x | 无 2024 条目 | 无 2024 条目 | 无 2024 条目 | 无纳入软工主路径 | [venue](venues/saner_conf_b.md) | [metadata](metadata/saner_conf_b.json) | 计数一致；2024 无条目，暂以先验为准 |
| `ICSME` | International Conference on Software Maintenance and Evolution | `B` | `会议` | 89 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 4.3.x / 6.4.x | 软件工程 88 / 跨域/待判定 1 | 属于软件工程 88 / 不属于软件工程 1 | 🟢 优先跟进 (22) / 🟡 保留观察 (64) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (2) | 4.1.1 缺陷修复与维护性修正 (15) / 3.1.4 场景化测试 (5) | [venue](venues/icsme_conf_b.md) | [metadata](metadata/icsme_conf_b.json) | 计数一致；2024 与先验一致 |
| `VMCAI` | International Conference on Verification, Model Checking, and Abstract Interpretation | `B` | `会议` | 30 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 22 / 软件工程 7 / 系统软件 1 | 不属于软件工程 23 / 跨域但软工主导 5 / 属于软件工程 2 | 🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0) | 3.2.1 静态分析与抽象解释 (3) / 3.3.1 面向软工问题的形式化验证 (2) | [venue](venues/vmcai_conf_b.md) | [metadata](metadata/vmcai_conf_b.json) | 计数一致；2024 比先验更偏非软工 |
| `ICWS` | IEEE International Conference on Web Services | `B` | `会议` | 165 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 5.3.x / 8.2.3 | 跨域/待判定 114 / 系统软件 31 / 软件工程 19 / 程序设计语言与形式化基础 1 | 不属于软件工程 146 / 属于软件工程 15 / 跨域但软工主导 4 | 🟢 优先跟进 (29) / 🟡 保留观察 (111) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (22) | 2.1.4 云/服务/平台架构 (5) / 5.3.4 扩展性、吞吐与时延保证 (3) | [venue](venues/icws_conf_b.md) | [metadata](metadata/icws_conf_b.json) | 计数一致；2024 比先验更偏非软工 |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | `B` | `会议` | 66 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 63 / 跨域/待判定 3 | 属于软件工程 63 / 不属于软件工程 3 | 🟢 优先跟进 (15) / 🟡 保留观察 (48) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 4.1.1 缺陷修复与维护性修正 (12) / 6.3.1 实验、案例研究与调查 (12) | [venue](venues/esem_conf_b.md) | [metadata](metadata/esem_conf_b.json) | 计数一致；2024 与先验一致 |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | `B` | `会议` | 53 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x / 5.2.x / 4.4.x | 软件工程 52 / 系统软件 1 | 属于软件工程 52 / 不属于软件工程 1 | 🟢 优先跟进 (17) / 🟡 保留观察 (34) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 3.3.3 assurance、认证与合规验证 (9) / 4.4.1 可观测性、日志与异常检测 (7) | [venue](venues/issre_conf_b.md) | [metadata](metadata/issre_conf_b.json) | 计数一致；2024 与先验一致 |
| `ASE / 期刊 / B` | Automated Software Engineering | `B` | `期刊` | 71 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 54 / 跨域/待判定 16 / 程序设计语言与形式化基础 1 | 属于软件工程 54 / 不属于软件工程 17 | 🟢 优先跟进 (8) / 🟡 保留观察 (10) / ⏳ 待补信息 (53) / ⚪ 暂不跟进 (0) | 7.1.1 代码生成、补全与变换 (11) / 7.1.2 AI 支持的测试、分析与修复 (6) | [venue](venues/ase_journal_b.md) | [metadata](metadata/ase_journal_b.json) | 计数一致；2024 与先验一致 |
| `ESE` | Empirical Software Engineering | `B` | `期刊` | 163 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 136 / 跨域/待判定 26 / 系统软件 1 | 属于软件工程 136 / 不属于软件工程 27 | 🟢 优先跟进 (20) / 🟡 保留观察 (59) / ⏳ 待补信息 (82) / ⚪ 暂不跟进 (2) | 6.3.1 实验、案例研究与调查 (39) / 4.1.1 缺陷修复与维护性修正 (20) | [venue](venues/ese_journal_b.md) | [metadata](metadata/ese_journal_b.json) | 计数一致；2024 与先验一致 |
| `IETS` | IET Software | `B` | `期刊` | 21 | 大部分属于软工 | C 🟡 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 5.x.x | 软件工程 20 / 跨域/待判定 1 | 属于软件工程 20 / 不属于软件工程 1 | 🟢 优先跟进 (2) / 🟡 保留观察 (19) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 6.3.4 replication、benchmark 与开放科学 (5) / 6.4.3 度量、预测与风险模型 (4) | [venue](venues/iets_journal_b.md) | [metadata](metadata/iets_journal_b.json) | 计数一致；2024 与先验一致 |
| `IST` | Information and Software Technology | `B` | `期刊` | 145 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 82 / 跨域/待判定 63 | 属于软件工程 82 / 不属于软件工程 63 | 🟢 优先跟进 (22) / 🟡 保留观察 (35) / ⏳ 待补信息 (83) / ⚪ 暂不跟进 (5) | 7.1.1 代码生成、补全与变换 (13) / 6.1.1 敏捷、精益与 DevOps 方法 (7) | [venue](venues/ist_journal_b.md) | [metadata](metadata/ist_journal_b.json) | 计数一致；2024 比先验更偏非软工 |
| `JSEP` | Journal of Software: Evolution and Process | `B` | `期刊` | 174 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.3.x / 6.1.x / 6.4.x | 软件工程 172 / 跨域/待判定 2 | 属于软件工程 172 / 不属于软件工程 2 | 🟢 优先跟进 (43) / 🟡 保留观察 (122) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9) | 4.1.1 缺陷修复与维护性修正 (22) / 6.3.1 实验、案例研究与调查 (13) | [venue](venues/jsep_journal_b.md) | [metadata](metadata/jsep_journal_b.json) | 计数一致；2024 与先验一致 |
| `JSS` | Journal of Systems and Software | `B` | `期刊` | 242 | 大部分属于软工 | B 🟢 | 软件工程 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 软件工程 147 / 跨域/待判定 91 / 系统软件 3 / 程序设计语言与形式化基础 1 | 属于软件工程 147 / 不属于软件工程 95 | 🟢 优先跟进 (56) / 🟡 保留观察 (65) / ⏳ 待补信息 (109) / ⚪ 暂不跟进 (12) | 2.1.1 架构描述与恢复 (13) / 3.2.3 面向质量属性的分析 (12) | [venue](venues/jss_journal_b.md) | [metadata](metadata/jss_journal_b.json) | 计数一致；2024 比先验更偏非软工 |
| `RE / 期刊 / B` | Requirements Engineering | `B` | `期刊` | 24 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 21 / 跨域/待判定 3 | 属于软件工程 21 / 不属于软件工程 3 | 🟢 优先跟进 (19) / 🟡 保留观察 (0) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (8) / 1.2.3 规约质量与一致性 (2) | [venue](venues/re_journal_b.md) | [metadata](metadata/re_journal_b.json) | 计数一致；2024 与先验一致 |
| `SCP` | Science of Computer Programming | `B` | `期刊` | 109 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 4.1.x | 程序设计语言与形式化基础 82 / 软件工程 27 | 不属于软件工程 82 / 属于软件工程 14 / 跨域但软工主导 13 | 🟢 优先跟进 (27) / 🟡 保留观察 (15) / ⏳ 待补信息 (64) / ⚪ 暂不跟进 (3) | 1.2.1 形式化规约与契约 (6) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) | [venue](venues/scp_journal_b.md) | [metadata](metadata/scp_journal_b.json) | 计数一致；2024 比先验更偏非软工 |
| `SoSyM` | Software and Systems Modeling | `B` | `期刊` | 75 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 45 / 跨域/待判定 29 / 系统软件 1 | 属于软件工程 45 / 不属于软件工程 30 | 🟢 优先跟进 (32) / 🟡 保留观察 (14) / ⏳ 待补信息 (27) / ⚪ 暂不跟进 (2) | 1.3.1 建模语言与元模型 (13) / 7.1.4 AI 支持的架构、设计与工程决策 (3) | [venue](venues/sosym_journal_b.md) | [metadata](metadata/sosym_journal_b.json) | 计数一致；2024 比先验更偏非软工 |
| `STVR` | Software Testing, Verification and Reliability | `B` | `期刊` | 26 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x | 软件工程 26 | 属于软件工程 26 | 🟢 优先跟进 (5) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.3 模糊、搜索式、变异与性质驱动测试 (14) / 2.2.1 设计原则、模式与反模式 (2) | [venue](venues/stvr_journal_b.md) | [metadata](metadata/stvr_journal_b.json) | 计数一致；2024 与先验一致 |
| `SPE` | Software: Practice and Experience | `B` | `期刊` | 116 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.3.x / 4.3.x / 4.4.x / 6.3.x / 8.2.x | 跨域/待判定 62 / 系统软件 26 / 软件工程 23 / 程序设计语言与形式化基础 5 | 不属于软件工程 93 / 属于软件工程 22 / 跨域但软工主导 1 | 🟢 优先跟进 (25) / 🟡 保留观察 (62) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (20) | 6.3.1 实验、案例研究与调查 (5) / 2.1.4 云/服务/平台架构 (3) | [venue](venues/spe_journal_b.md) | [metadata](metadata/spe_journal_b.json) | 计数一致；2024 比先验更偏非软工 |
| `PASTE` | ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | `C` | `会议` | 0 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 3.2.x / 3.4.x / 4.2.x | 无 2024 条目 | 无 2024 条目 | 无 2024 条目 | 无纳入软工主路径 | [venue](venues/paste_conf_c.md) | [metadata](metadata/paste_conf_c.json) | 计数一致；2024 无条目，暂以先验为准 |
| `APSEC` | Asia-Pacific Software Engineering Conference | `C` | `会议` | 68 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 55 / 跨域/待判定 12 / 程序设计语言与形式化基础 1 | 属于软件工程 55 / 不属于软件工程 13 | 🟢 优先跟进 (23) / 🟡 保留观察 (35) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (8) | 7.1.1 代码生成、补全与变换 (10) / 6.3.4 replication、benchmark 与开放科学 (9) | [venue](venues/apsec_conf_c.md) | [metadata](metadata/apsec_conf_c.json) | 计数一致；2024 与先验一致 |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | `C` | `会议` | 100 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 96 / 跨域/待判定 4 | 属于软件工程 96 / 不属于软件工程 4 | 🟢 优先跟进 (10) / 🟡 保留观察 (81) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9) | 6.3.1 实验、案例研究与调查 (17) / 6.4.1 代码、提交、issue 与 PR 挖掘 (10) | [venue](venues/ease_conf_c.md) | [metadata](metadata/ease_conf_c.json) | 计数一致；2024 与先验一致 |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | `C` | `会议` | 22 | 部分属于软工 | B 🟢 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.3.x | 跨域/待判定 17 / 软件工程 5 | 不属于软件工程 17 / 属于软件工程 3 / 跨域但软工主导 2 | 🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (1) / 3.3.1 面向软工问题的形式化验证 (1) | [venue](venues/iceccs_conf_c.md) | [metadata](metadata/iceccs_conf_c.json) | 计数一致；2024 比先验更偏非软工 |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | `C` | `会议` | 49 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 软件工程 49 | 属于软件工程 49 | 🟢 优先跟进 (23) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.3 模糊、搜索式、变异与性质驱动测试 (13) / 3.1.1 测试生成与增强 (7) | [venue](venues/icst_conf_c.md) | [metadata](metadata/icst_conf_c.json) | 计数一致；2024 与先验一致 |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | `C` | `会议` | 24 | 大部分属于软工 | B 🟢 | 软件工程 | 3.2.x / 4.2.x / 4.1.x / 3.4.x | 软件工程 20 / 跨域/待判定 4 | 属于软件工程 20 / 不属于软件工程 4 | 🟢 优先跟进 (4) / 🟡 保留观察 (20) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 4.1.1 缺陷修复与维护性修正 (4) / 6.3.1 实验、案例研究与调查 (3) | [venue](venues/scam_conf_c.md) | [metadata](metadata/scam_conf_c.json) | 计数一致；2024 与先验一致 |
| `COMPSAC` | International Computer Software and Applications Conference | `C` | `会议` | 388 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 294 / 软件工程 51 / 系统软件 37 / 程序设计语言与形式化基础 6 | 不属于软件工程 337 / 属于软件工程 41 / 跨域但软工主导 10 | 🟢 优先跟进 (61) / 🟡 保留观察 (270) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (57) | 2.1.1 架构描述与恢复 (5) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (4) | [venue](venues/compsac_conf_c.md) | [metadata](metadata/compsac_conf_c.json) | 计数一致；2024 比先验更偏非软工 |
| `ICFEM` | International Conference on Formal Engineering Methods | `C` | `会议` | 22 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 14 / 软件工程 8 | 不属于软件工程 14 / 属于软件工程 5 / 跨域但软工主导 3 | 🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0) | 1.3.3 模型分析、仿真与验证 (3) / 1.2.1 形式化规约与契约 (2) | [venue](venues/icfem_conf_c.md) | [metadata](metadata/icfem_conf_c.json) | 计数一致；2024 与先验一致 |
| `SSE` | IEEE International Conference on Software Services Engineering | `C` | `会议` | 47 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 30 / 软件工程 9 / 系统软件 7 / 程序设计语言与形式化基础 1 | 不属于软件工程 38 / 属于软件工程 6 / 跨域但软工主导 3 | 🟢 优先跟进 (11) / 🟡 保留观察 (25) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (10) | 6.5.4 教育、培训与入门支持 (2) / 2.1.4 云/服务/平台架构 (2) | [venue](venues/sse_conf_c.md) | [metadata](metadata/sse_conf_c.json) | 计数一致；2024 比先验更偏非软工 |
| `ICSSP` | International Conference on Software and System Process | `C` | `会议` | 9 | 完全属于软工 | C 🟡 | 软件工程 | 6.1.x / 6.2.x / 6.5.x | 软件工程 8 / 跨域/待判定 1 | 属于软件工程 8 / 不属于软件工程 1 | 🟢 优先跟进 (2) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 6.5.2 协作、评审与知识共享 (1) / 6.5.1 开发者认知、生产力与福祉 (1) | [venue](venues/icssp_conf_c.md) | [metadata](metadata/icssp_conf_c.json) | 计数一致；2024 与先验一致 |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | `C` | `会议` | 81 | 部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 跨域/待判定 61 / 软件工程 12 / 程序设计语言与形式化基础 4 / 系统软件 4 | 不属于软件工程 69 / 属于软件工程 9 / 跨域但软工主导 3 | 🟢 优先跟进 (9) / 🟡 保留观察 (44) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (5) | 4.2.1 代码搜索、导航与摘要 (2) / 1.3.3 模型分析、仿真与验证 (2) | [venue](venues/seke_conf_c.md) | [metadata](metadata/seke_conf_c.json) | 计数一致；2024 比先验更偏非软工 |
| `QRS` | International Conference on Software Quality, Reliability and Security | `C` | `会议` | 71 | 完全属于软工 | A 🔥 | 软件工程 | 3.x.x / 5.1.x / 5.2.x / 4.4.x | 软件工程 70 / 跨域/待判定 1 | 属于软件工程 70 / 不属于软件工程 1 | 🟢 优先跟进 (23) / 🟡 保留观察 (43) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5) | 3.1.1 测试生成与增强 (8) / 3.2.3 面向质量属性的分析 (8) | [venue](venues/qrs_conf_c.md) | [metadata](metadata/qrs_conf_c.json) | 计数一致；2024 与先验一致 |
| `ICSR` | International Conference on Software Reuse | `C` | `会议` | 11 | 完全属于软工 | C 🟡 | 软件工程 | 1.4.x / 2.3.x / 4.1.x / 4.3.x | 软件工程 8 / 跨域/待判定 3 | 属于软件工程 8 / 不属于软件工程 3 | 🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0) | 2.2.1 设计原则、模式与反模式 (2) / 1.4.1 特征建模与配置 (1) | [venue](venues/icsr_conf_c.md) | [metadata](metadata/icsr_conf_c.json) | 计数一致；2024 与先验一致 |
| `SPIN` | International Symposium on Model Checking of Software | `C` | `会议` | 14 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x | 软件工程 7 / 程序设计语言与形式化基础 7 | 不属于软件工程 7 / 属于软件工程 5 / 跨域但软工主导 2 | 🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (3) / 1.3.3 模型分析、仿真与验证 (3) | [venue](venues/spin_conf_c.md) | [metadata](metadata/spin_conf_c.json) | 计数一致；2024 与先验一致 |
| `TASE` | Theoretical Aspects of Software Engineering Conference | `C` | `会议` | 27 | 部分属于软工 | B 🟢 | 形式化方法与软件工程交叉 | 1.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 18 / 软件工程 8 / 系统软件 1 | 不属于软件工程 19 / 跨域但软工主导 7 / 属于软件工程 1 | 🟢 优先跟进 (2) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) | [venue](venues/tase_conf_c.md) | [metadata](metadata/tase_conf_c.json) | 计数一致；2024 与先验一致 |
| `MSR` | Mining Software Repositories | `C` | `会议` | 97 | 完全属于软工 | B 🟢 | 软件工程 | 6.4.x / 6.3.x / 4.1.x / 6.5.x | 软件工程 94 / 跨域/待判定 3 | 属于软件工程 94 / 不属于软件工程 3 | 🟢 优先跟进 (16) / 🟡 保留观察 (75) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6) | 6.3.4 replication、benchmark 与开放科学 (39) / 4.1.1 缺陷修复与维护性修正 (11) | [venue](venues/msr_conf_c.md) | [metadata](metadata/msr_conf_c.json) | 计数一致；2024 与先验一致 |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | `C` | `会议` | 22 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 17 / 跨域/待判定 5 | 属于软件工程 17 / 不属于软件工程 5 | 🟢 优先跟进 (15) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (9) / 3.2.3 面向质量属性的分析 (1) | [venue](venues/refsq_conf_c.md) | [metadata](metadata/refsq_conf_c.json) | 计数一致；2024 与先验一致 |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | `C` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 2.1.x / 2.2.x / 4.1.x | 无 2024 条目 | 无 2024 条目 | 无 2024 条目 | 无纳入软工主路径 | [venue](venues/wicsa_conf_c.md) | [metadata](metadata/wicsa_conf_c.json) | 计数一致；2024 无条目，暂以先验为准 |
| `Internetware` | Asia-Pacific Symposium on Internetware | `C` | `会议` | 56 | 大部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.x | 软件工程 49 / 跨域/待判定 6 / 程序设计语言与形式化基础 1 | 属于软件工程 49 / 不属于软件工程 7 | 🟢 优先跟进 (15) / 🟡 保留观察 (38) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 2.1.4 云/服务/平台架构 (20) / 7.1.2 AI 支持的测试、分析与修复 (5) | [venue](venues/internetware_conf_c.md) | [metadata](metadata/internetware_conf_c.json) | 计数一致；2024 与先验一致 |
| `RV` | International Conference on Runtime Verification | `C` | `会议` | 18 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.3.2 / 4.4.4 / 5.1.x | 程序设计语言与形式化基础 12 / 软件工程 5 / 系统软件 1 | 不属于软件工程 13 / 跨域但软工主导 4 / 属于软件工程 1 | 🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0) | 3.3.2 运行时验证与运行时监测 (5) | [venue](venues/rv_conf_c.md) | [metadata](metadata/rv_conf_c.json) | 计数一致；2024 与先验一致 |
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | `C` | `期刊` | 76 | 大部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 软件工程 60 / 跨域/待判定 15 / 系统软件 1 | 属于软件工程 60 / 不属于软件工程 16 | 🟢 优先跟进 (23) / 🟡 保留观察 (48) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (4) | 7.1.1 代码生成、补全与变换 (11) / 6.3.4 replication、benchmark 与开放科学 (5) | [venue](venues/ijseke_journal_c.md) | [metadata](metadata/ijseke_journal_c.json) | 计数一致；2024 与先验一致 |
| `STTT` | International Journal of Software Tools for Technology Transfer | `C` | `期刊` | 48 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 29 / 软件工程 18 / 系统软件 1 | 不属于软件工程 30 / 跨域但软工主导 11 / 属于软件工程 7 | 🟢 优先跟进 (17) / 🟡 保留观察 (10) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (2) | 3.2.1 静态分析与抽象解释 (8) / 3.3.1 面向软工问题的形式化验证 (4) | [venue](venues/sttt_journal_c.md) | [metadata](metadata/sttt_journal_c.json) | 计数一致；2024 与先验一致 |
| `SOCA` | Service Oriented Computing and Applications | `C` | `期刊` | 25 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 8.2.3 | 跨域/待判定 23 / 软件工程 1 / 程序设计语言与形式化基础 1 | 不属于软件工程 24 / 跨域但软工主导 1 | 🟢 优先跟进 (0) / 🟡 保留观察 (3) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (1) | [venue](venues/soca_journal_c.md) | [metadata](metadata/soca_journal_c.json) | 计数一致；2024 比先验更偏非软工 |
| `SQJ` | Software Quality Journal | `C` | `期刊` | 56 | 完全属于软工 | B 🟢 | 软件工程 | 5.x.x / 3.x.x / 6.3.x | 软件工程 46 / 跨域/待判定 10 | 属于软件工程 46 / 不属于软件工程 10 | 🟢 优先跟进 (12) / 🟡 保留观察 (12) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0) | 3.1.1 测试生成与增强 (8) / 6.3.1 实验、案例研究与调查 (7) | [venue](venues/sqj_journal_c.md) | [metadata](metadata/sqj_journal_c.json) | 计数一致；2024 与先验一致 |

## 6. Venue 导航

---

### `PLDI`

- 基本信息：
- 全称：ACM SIGPLAN Conference on Programming Language Design and Implementation
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2024`
- 条目数：`89`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：程序分析 / 软件验证 / repair 邻近但需严格筛选
- 初筛分布：🟢 优先跟进 (41) / 🟡 保留观察 (40) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/pldi_conf_a.md](./venues/pldi_conf_a.md)
- 数据文件：[metadata](metadata/pldi_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-pldi_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/pldi-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/pldi/
- 正式发布载体页：https://dl.acm.org/journal/pacmpl
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/pldi_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (71) / 系统软件 (10) / 软件工程 (8)
- 软工纳入判定分布：不属于软件工程 (81) / 属于软件工程 (7) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (41) / 🟡 保留观察 (40) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (89)
- 人工复核状态分布：未人工复核 (89)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (4) / 3.2.3 面向质量属性的分析 (1) / 3.2.4 分析驱动的理解、重构与综合 (1) / 1.2.1 形式化规约与契约 (1) / 4.2.1 代码搜索、导航与摘要 (1)
- 主题标签补充：形式化方法 (48) / 测试与验证 (35) / 程序设计语言/编译 (34) / 建模/模型驱动 (22) / 需求工程 (18)

---

### `FSE`

- 基本信息：
- 全称：ACM International Conference on the Foundations of Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2024`
- 条目数：`121`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE + `LLM/需求建模/测试验证/修复` 主线
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (75) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
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
- 一级总判定分布：软件工程 (121)
- 软工纳入判定分布：属于软件工程 (121)
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (75) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (121)
- 人工复核状态分布：未人工复核 (121)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (25) / 6.3.4 replication、benchmark 与开放科学 (18) / 7.1.2 AI 支持的测试、分析与修复 (12) / 7.1.4 AI 支持的架构、设计与工程决策 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 3.2.1 静态分析与抽象解释 (5) / 6.3.1 实验、案例研究与调查 (4) / 2.2.1 设计原则、模式与反模式 (4)
- 主题标签补充：测试与验证 (49) / 建模/模型驱动 (45) / LLM/AI for SE (40) / 可靠性/安全 (34) / 维护与演化 (30)

---

### `OOPSLA`

- 基本信息：
- 全称：Conference on Object-Oriented Programming Systems, Languages, and Applications
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2024`
- 条目数：`148`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件结构 / 程序分析 / 重构与验证偶发贴题
- 初筛分布：🟢 优先跟进 (56) / 🟡 保留观察 (77) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (15)
- 论文名录页：[venues/oopsla_conf_a.md](./venues/oopsla_conf_a.md)
- 数据文件：[metadata](metadata/oopsla_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-oopsla_conf_a)

- 关键信息页面：
- 年主页：https://2024.splashcon.org/track/splash-2024-oopsla
- 学术索引页：http://dblp.uni-trier.de/db/conf/oopsla/
- 正式发布载体页：https://dl.acm.org/journal/pacmpl
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/oopsla_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (118) / 软件工程 (19) / 系统软件 (11)
- 软工纳入判定分布：不属于软件工程 (129) / 属于软件工程 (14) / 跨域但软工主导 (5)
- 初筛分布：🟢 优先跟进 (56) / 🟡 保留观察 (77) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (15)
- 判定来源分布：启发式初判 (148)
- 人工复核状态分布：未人工复核 (148)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (4) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 1.3.3 模型分析、仿真与验证 (3) / 2.2.1 设计原则、模式与反模式 (2) / 7.1.1 代码生成、补全与变换 (2) / 3.2.3 面向质量属性的分析 (2) / 7.1.2 AI 支持的测试、分析与修复 (1) / 6.3.4 replication、benchmark 与开放科学 (1)
- 主题标签补充：形式化方法 (80) / 程序设计语言/编译 (56) / 测试与验证 (56) / 建模/模型驱动 (41) / 可靠性/安全 (32)

---

### `ASE / 会议 / A`

- 基本信息：
- 全称：International Conference on Automated Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2024`
- 条目数：`266`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (73) / 🟡 保留观察 (175) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (16)
- 论文名录页：[venues/ase_conf_a.md](./venues/ase_conf_a.md)
- 数据文件：[metadata](metadata/ase_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ase-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/kbse/
- 官方论文集页：https://doi.org/10.1145/3691620
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ase_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (261) / 跨域/待判定 (3) / 系统软件 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (261) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (73) / 🟡 保留观察 (175) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (16)
- 判定来源分布：启发式初判 (266)
- 人工复核状态分布：未人工复核 (266)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (75) / 7.1.2 AI 支持的测试、分析与修复 (23) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (20) / 3.1.4 场景化测试 (14) / 7.1.3 AI 支持的需求、建模与文档 (9) / 3.2.1 静态分析与抽象解释 (9) / 7.1.4 AI 支持的架构、设计与工程决策 (6) / 1.2.3 规约质量与一致性 (6)
- 主题标签补充：建模/模型驱动 (115) / 测试与验证 (100) / LLM/AI for SE (93) / 可靠性/安全 (72) / 维护与演化 (41)

---

### `ICSE`

- 基本信息：
- 全称：International Conference on Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2024`
- 条目数：`237`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主会，需求-建模-验证-修复全链可见
- 初筛分布：🟢 优先跟进 (75) / 🟡 保留观察 (154) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/icse_conf_a.md](./venues/icse_conf_a.md)
- 数据文件：[metadata](metadata/icse_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icse_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icse-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icse/
- 官方论文集页：https://doi.org/10.1145/3597503 / https://ieeexplore.ieee.org/xpl/conhome/10548016/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icse_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (227) / 跨域/待判定 (8) / 系统软件 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (227) / 不属于软件工程 (10)
- 初筛分布：🟢 优先跟进 (75) / 🟡 保留观察 (154) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (237)
- 人工复核状态分布：未人工复核 (237)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (49) / 7.1.2 AI 支持的测试、分析与修复 (18) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (16) / 6.3.4 replication、benchmark 与开放科学 (14) / 3.1.4 场景化测试 (12) / 6.3.1 实验、案例研究与调查 (12) / 7.1.4 AI 支持的架构、设计与工程决策 (12) / 3.2.1 静态分析与抽象解释 (9)
- 主题标签补充：建模/模型驱动 (84) / 可靠性/安全 (76) / 测试与验证 (75) / LLM/AI for SE (50) / 经验软件工程 (47)

---

### `ISSTA`

- 基本信息：
- 全称：International Symposium on Software Testing and Analysis
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2024`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试分析 / 形式化验证 / 缺陷定位与修复主场
- 初筛分布：无 2024 条目
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
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `FM`

- 基本信息：
- 全称：International Symposium on Formal Methods
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2024`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：形式化方法 / timed automata / 工业与控制系统验证邻近
- 初筛分布：无 2024 条目
- 论文名录页：[venues/fm_conf_a.md](./venues/fm_conf_a.md)
- 数据文件：[metadata](metadata/fm_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-fm_conf_a)

- 关键信息页面：
- 年主页：https://www.fm24.polimi.it/?page_id=59#call-for-papers
- 学术索引页：http://dblp.uni-trier.de/db/conf/fm/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/fm_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `TOSEM`

- 基本信息：
- 全称：ACM Transactions on Software Engineering and Methodology
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`223`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件工程方法 / 需求建模 / 测试验证 / `AI for SE`
- 初筛分布：🟢 优先跟进 (66) / 🟡 保留观察 (148) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/tosem_journal_a.md](./venues/tosem_journal_a.md)
- 数据文件：[metadata](metadata/tosem_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tosem_journal_a)

- 关键信息页面：
- 期刊主页：https://dl.acm.org/journal/tosem
- 学术索引页：http://dblp.uni-trier.de/db/journals/tosem/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tosem_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (217) / 跨域/待判定 (6)
- 软工纳入判定分布：属于软件工程 (217) / 不属于软件工程 (6)
- 初筛分布：🟢 优先跟进 (66) / 🟡 保留观察 (148) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (223)
- 人工复核状态分布：未人工复核 (223)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (34) / 6.3.4 replication、benchmark 与开放科学 (26) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (23) / 7.1.4 AI 支持的架构、设计与工程决策 (15) / 6.3.1 实验、案例研究与调查 (15) / 7.1.2 AI 支持的测试、分析与修复 (10) / 4.2.1 代码搜索、导航与摘要 (7) / 3.1.1 测试生成与增强 (6)
- 主题标签补充：建模/模型驱动 (102) / 测试与验证 (102) / 可靠性/安全 (56) / LLM/AI for SE (50) / 经验软件工程 (49)

---

### `TSE`

- 基本信息：
- 全称：IEEE Transactions on Software Engineering
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`182`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主刊 / 建模验证修复与 `LLM` 子题持续出现
- 初筛分布：🟢 优先跟进 (61) / 🟡 保留观察 (114) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/tse_journal_a.md](./venues/tse_journal_a.md)
- 数据文件：[metadata](metadata/tse_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tse_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32
- 学术索引页：http://dblp.uni-trier.de/db/journals/tse/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tse_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (177) / 跨域/待判定 (5)
- 软工纳入判定分布：属于软件工程 (177) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (61) / 🟡 保留观察 (114) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (182)
- 人工复核状态分布：未人工复核 (182)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (31) / 6.3.4 replication、benchmark 与开放科学 (15) / 7.1.2 AI 支持的测试、分析与修复 (12) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (11) / 7.1.4 AI 支持的架构、设计与工程决策 (10) / 3.1.4 场景化测试 (8) / 6.3.1 实验、案例研究与调查 (7) / 1.3.3 模型分析、仿真与验证 (5)
- 主题标签补充：测试与验证 (87) / 建模/模型驱动 (79) / LLM/AI for SE (51) / 可靠性/安全 (45) / 维护与演化 (40)

---

### `TSC`

- 基本信息：
- 全称：IEEE Transactions on Services Computing
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`323`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务工作流 / 平台 orchestration 邻近，可补性质工程
- 初筛分布：🟢 优先跟进 (76) / 🟡 保留观察 (213) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (34)
- 论文名录页：[venues/tsc_journal_a.md](./venues/tsc_journal_a.md)
- 数据文件：[metadata](metadata/tsc_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tsc_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=4629386
- 学术索引页：http://dblp.uni-trier.de/db/journals/tsc/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tsc_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (201) / 系统软件 (92) / 软件工程 (30)
- 软工纳入判定分布：不属于软件工程 (293) / 属于软件工程 (27) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (76) / 🟡 保留观察 (213) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (34)
- 判定来源分布：启发式初判 (323)
- 人工复核状态分布：未人工复核 (323)
- 高频软工主路径：2.1.4 云/服务/平台架构 (9) / 6.2.1 估算、计划与排程 (6) / 1.3.4 基于模型的生成、测试与运行时支持 (3) / 2.1.3 架构演化与重构 (2) / 4.4.3 运行时重配置与自适应运维 (2) / 4.4.1 可观测性、日志与异常检测 (2) / 3.2.3 面向质量属性的分析 (1) / 4.3.2 CI/CD 与发布工程 (1)
- 主题标签补充：建模/模型驱动 (165) / 可靠性/安全 (117) / 系统软件 (68) / 形式化方法 (58) / 需求工程 (56)

---

### `ECOOP`

- 基本信息：
- 全称：European Conference on Object-Oriented Programming
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`48`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`OO` 程序结构 / 分析与重构邻近
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (13) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/ecoop_conf_b.md](./venues/ecoop_conf_b.md)
- 数据文件：[metadata](metadata/ecoop_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ecoop_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ecoop-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/ecoop/
- 官方论文集页：https://www.dagstuhl.de/dagpub/978-3-95977-341-6
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ecoop_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (41) / 系统软件 (5) / 软件工程 (2)
- 软工纳入判定分布：不属于软件工程 (46) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (13) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (48)
- 人工复核状态分布：未人工复核 (48)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (2)
- 主题标签补充：待人工细分 (16) / 形式化方法 (15) / 程序设计语言/编译 (14) / 需求工程 (7) / 可靠性/安全 (6)

---

### `ICPC`

- 基本信息：
- 全称：IEEE International Conference on Program Comprehension
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`46`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序理解 / 缺陷分析 / 修复解释与人因辅助
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (38) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/icpc_conf_b.md](./venues/icpc_conf_b.md)
- 数据文件：[metadata](metadata/icpc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icpc_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icpc-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/iwpc/
- 官方论文集页：https://doi.org/10.1145/3643916 / https://ieeexplore.ieee.org/xpl/conhome/10555568/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icpc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (45) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (45) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (38) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (46)
- 人工复核状态分布：未人工复核 (46)
- 高频软工主路径：6.5.1 开发者认知、生产力与福祉 (15) / 7.1.1 代码生成、补全与变换 (7) / 6.3.4 replication、benchmark 与开放科学 (3) / 4.2.1 代码搜索、导航与摘要 (3) / 4.2.5 文档工程、解释与设计 rationale 恢复 (2) / 6.4.1 代码、提交、issue 与 PR 挖掘 (2) / 4.1.1 缺陷修复与维护性修正 (2) / 4.1.5 技术债、克隆与可维护性治理 (2)
- 主题标签补充：建模/模型驱动 (26) / 维护与演化 (16) / 经验软件工程 (16) / LLM/AI for SE (12) / 可靠性/安全 (8)

---

### `RE / 会议 / B`

- 基本信息：
- 全称：IEEE International Requirements Engineering Conference
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`60`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (55) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/re_conf_b.md](./venues/re_conf_b.md)
- 数据文件：[metadata](metadata/re_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/re-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/re/
- 官方论文集页：https://doi.org/10.1109/RE59067.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/re_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (60)
- 软工纳入判定分布：属于软件工程 (60)
- 初筛分布：🟢 优先跟进 (55) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (60)
- 人工复核状态分布：未人工复核 (60)
- 高频软工主路径：1.1.1 需求获取与发现 (19) / 6.3.1 实验、案例研究与调查 (3) / 7.1.1 代码生成、补全与变换 (3) / 6.3.4 replication、benchmark 与开放科学 (3) / 2.3.3 组件、包与集成工程 (3) / 7.1.3 AI 支持的需求、建模与文档 (3) / 2.2.1 设计原则、模式与反模式 (3) / 7.1.5 人机协同开发与评估 (2)
- 主题标签补充：需求工程 (55) / 建模/模型驱动 (19) / LLM/AI for SE (15) / 测试与验证 (14) / 形式化方法 (11)

---

### `CAiSE`

- 基本信息：
- 全称：International Conference on Advanced Information Systems Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`36`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：信息系统与过程/模型工程，适合补需求-建模-规约链
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/caise_conf_b.md](./venues/caise_conf_b.md)
- 数据文件：[metadata](metadata/caise_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-caise_conf_b)

- 关键信息页面：
- 年主页：https://cyprusconferences.org/caise2024/
- 学术索引页：http://dblp.uni-trier.de/db/conf/caise/
- 官方论文集页：https://doi.org/10.1007/978-3-031-61057-8
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/caise_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (26) / 软件工程 (9) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (27) / 跨域但软工主导 (5) / 属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (36)
- 人工复核状态分布：未人工复核 (36)
- 高频软工主路径：6.1.2 过程挖掘、符合性与改进 (3) / 6.2.4 组合治理与决策支持 (1) / 3.3.2 运行时验证与运行时监测 (1) / 1.1.1 需求获取与发现 (1) / 1.3.1 建模语言与元模型 (1) / 1.1.4 需求追踪、变更与演化 (1) / 4.4.1 可观测性、日志与异常检测 (1)
- 主题标签补充：待人工细分 (15) / 建模/模型驱动 (7) / 经验软件工程 (5) / 运行时监测 (4) / 需求工程 (3)

---

### `MoDELS`

- 基本信息：
- 全称：ACM/IEEE International Conference on Model Driven Engineering Languages and Systems
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`26`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：模型驱动 / 状态机-SysML / 形式化建模主场
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (8) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/models_conf_b.md](./venues/models_conf_b.md)
- 数据文件：[metadata](metadata/models_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-models_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/models-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/models/
- 官方论文集页：https://dl.acm.org/doi/proceedings/10.1145/3640310
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/models_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (24) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (24) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (8) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (26)
- 人工复核状态分布：未人工复核 (26)
- 高频软工主路径：1.3.1 建模语言与元模型 (10) / 3.3.2 运行时验证与运行时监测 (2) / 6.5.2 协作、评审与知识共享 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1) / 7.1.1 代码生成、补全与变换 (1) / 1.3.3 模型分析、仿真与验证 (1) / 1.4.1 特征建模与配置 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1)
- 主题标签补充：建模/模型驱动 (19) / 形式化方法 (9) / 需求工程 (9) / 测试与验证 (8) / LLM/AI for SE (5)

---

### `ICSOC`

- 基本信息：
- 全称：International Conference on Service Oriented Computing
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`58`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务组合 / 流程 / 性质与治理偶有贴题
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (57) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsoc_conf_b.md](./venues/icsoc_conf_b.md)
- 数据文件：[metadata](metadata/icsoc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsoc_conf_b)

- 关键信息页面：
- 年主页：http://icsoc.org
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsoc/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsoc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (45) / 软件工程 (12) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (46) / 跨域但软工主导 (7) / 属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (57) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (58)
- 人工复核状态分布：未人工复核 (58)
- 高频软工主路径：2.1.4 云/服务/平台架构 (7) / 1.1.1 需求获取与发现 (1) / 1.4.1 特征建模与配置 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 1.1.4 需求追踪、变更与演化 (1) / 4.4.1 可观测性、日志与异常检测 (1)
- 主题标签补充：待人工细分 (37) / LLM/AI for SE (7) / 可靠性/安全 (4) / 系统软件 (3) / 运行时监测 (3)

---

### `SANER`

- 基本信息：
- 全称：IEEE International Conference on Software Analysis, Evolution, and Reengineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：代码分析 / 逆向 / 演化与 reengineering
- 初筛分布：无 2024 条目
- 论文名录页：[venues/saner_conf_b.md](./venues/saner_conf_b.md)
- 数据文件：[metadata](metadata/saner_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-saner_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/saner-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/wcre/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/saner_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `ICSME`

- 基本信息：
- 全称：International Conference on Software Maintenance and Evolution
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`89`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：维护演化 / 修复 / 回归验证 / 工程闭环邻近
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (64) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/icsme_conf_b.md](./venues/icsme_conf_b.md)
- 数据文件：[metadata](metadata/icsme_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsme_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icsme-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsm/
- 官方论文集页：https://doi.org/10.1109/ICSME58944.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsme_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (88) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (88) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (64) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (89)
- 人工复核状态分布：未人工复核 (89)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (15) / 3.1.4 场景化测试 (5) / 6.3.1 实验、案例研究与调查 (5) / 6.4.1 代码、提交、issue 与 PR 挖掘 (5) / 4.2.1 代码搜索、导航与摘要 (4) / 4.1.2 重构、重模块化与代码清理 (4) / 3.4.2 缺陷定位、补丁生成与程序修复 (3) / 7.1.2 AI 支持的测试、分析与修复 (3)
- 主题标签补充：维护与演化 (42) / 建模/模型驱动 (38) / 测试与验证 (32) / 经验软件工程 (30) / LLM/AI for SE (23)

---

### `VMCAI`

- 基本信息：
- 全称：International Conference on Verification, Model Checking, and Abstract Interpretation
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`30`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：程序验证 / 模型检查 / 抽象解释直接支撑验证框架
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/vmcai_conf_b.md](./venues/vmcai_conf_b.md)
- 数据文件：[metadata](metadata/vmcai_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-vmcai_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/vmcai-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/vmcai/
- 官方论文集页：https://doi.org/10.1007/978-3-031-50524-9 / https://doi.org/10.1007/978-3-031-50521-8
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/vmcai_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (22) / 软件工程 (7) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (23) / 跨域但软工主导 (5) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (30)
- 人工复核状态分布：未人工复核 (30)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (3) / 3.3.1 面向软工问题的形式化验证 (2) / 1.2.1 形式化规约与契约 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：待人工细分 (14) / 形式化方法 (7) / 测试与验证 (7) / 建模/模型驱动 (5) / LLM/AI for SE (2)

---

### `ICWS`

- 基本信息：
- 全称：IEEE International Conference on Web Services
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`165`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：Web services / orchestration / 性质验证偶有贴题
- 初筛分布：🟢 优先跟进 (29) / 🟡 保留观察 (111) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (22)
- 论文名录页：[venues/icws_conf_b.md](./venues/icws_conf_b.md)
- 数据文件：[metadata](metadata/icws_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icws_conf_b)

- 关键信息页面：
- 年主页：https://icws.conferences.computer.org/2024/
- 学术索引页：http://dblp.uni-trier.de/db/conf/icws/
- 官方论文集页：https://doi.org/10.1109/ICWS62655.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icws_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (114) / 系统软件 (31) / 软件工程 (19) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (146) / 属于软件工程 (15) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (29) / 🟡 保留观察 (111) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (22)
- 判定来源分布：启发式初判 (165)
- 人工复核状态分布：未人工复核 (165)
- 高频软工主路径：2.1.4 云/服务/平台架构 (5) / 5.3.4 扩展性、吞吐与时延保证 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 2.3.3 组件、包与集成工程 (1) / 8.5.4 异构与新型计算平台的软件工程 (1) / 4.4.1 可观测性、日志与异常检测 (1) / 4.4.2 事故诊断、回滚与恢复 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1)
- 主题标签补充：建模/模型驱动 (92) / 可靠性/安全 (56) / LLM/AI for SE (35) / 系统软件 (30) / 测试与验证 (23)

---

### `ESEM`

- 基本信息：
- 全称：International Symposium on Empirical Software Engineering and Measurement
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`66`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证方法 / 评测设计 / `LLM-SE` 实验口径重要
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (48) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/esem_conf_b.md](./venues/esem_conf_b.md)
- 数据文件：[metadata](metadata/esem_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-esem_conf_b)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/esem-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/esem/
- 官方论文集页：https://doi.org/10.1145/3674805
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/esem_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (63) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (63) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (48) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (66)
- 人工复核状态分布：未人工复核 (66)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (12) / 6.3.1 实验、案例研究与调查 (12) / 6.3.4 replication、benchmark 与开放科学 (5) / 6.5.4 教育、培训与入门支持 (4) / 3.2.3 面向质量属性的分析 (3) / 3.2.1 静态分析与抽象解释 (3) / 6.3.3 系统综述、mapping 与 meta-analysis (3) / 5.2.4 公平性、问责与法规符合 (3)
- 主题标签补充：经验软件工程 (32) / 建模/模型驱动 (28) / LLM/AI for SE (14) / 维护与演化 (13) / 可靠性/安全 (12)

---

### `ISSRE`

- 基本信息：
- 全称：IEEE International Symposium on Software Reliability Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2024`
- 条目数：`53`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：可靠性 / assurance / 安全关键验证与缺陷检测很近
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (34) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/issre_conf_b.md](./venues/issre_conf_b.md)
- 数据文件：[metadata](metadata/issre_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-issre_conf_b)

- 关键信息页面：
- 年主页：未检出 2024 年主页
- 学术索引页：http://dblp.uni-trier.de/db/conf/issre/
- 官方论文集页：https://doi.org/10.1109/ISSRE62328.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/issre_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (52) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (52) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (34) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (53)
- 人工复核状态分布：未人工复核 (53)
- 高频软工主路径：3.3.3 assurance、认证与合规验证 (9) / 4.4.1 可观测性、日志与异常检测 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (5) / 3.1.1 测试生成与增强 (4) / 5.2.1 安全开发与漏洞治理 (4) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 7.1.1 代码生成、补全与变换 (2) / 4.4.2 事故诊断、回滚与恢复 (2)
- 主题标签补充：建模/模型驱动 (28) / 可靠性/安全 (26) / 测试与验证 (18) / LLM/AI for SE (12) / 经验软件工程 (11)

---

### `ASE / 期刊 / B`

- 基本信息：
- 全称：Automated Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`71`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (10) / ⏳ 待补信息 (53) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ase_journal_b.md](./venues/ase_journal_b.md)
- 数据文件：[metadata](metadata/ase_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10515
- 学术索引页：http://dblp.uni-trier.de/db/journals/ase/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ase_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (54) / 跨域/待判定 (16) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (54) / 不属于软件工程 (17)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (10) / ⏳ 待补信息 (53) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (71)
- 人工复核状态分布：未人工复核 (71)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (11) / 7.1.2 AI 支持的测试、分析与修复 (6) / 6.3.1 实验、案例研究与调查 (4) / 3.2.3 面向质量属性的分析 (3) / 4.1.2 重构、重模块化与代码清理 (3) / 1.1.1 需求获取与发现 (3) / 3.1.2 回归测试与测试选择 (3) / 2.3.3 组件、包与集成工程 (2)
- 主题标签补充：待人工细分 (28) / 测试与验证 (16) / 可靠性/安全 (14) / 建模/模型驱动 (12) / LLM/AI for SE (7)

---

### `ESE`

- 基本信息：
- 全称：Empirical Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`163`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证研究 / 数据集 / benchmark / 人因与评测设计
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (59) / ⏳ 待补信息 (82) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/ese_journal_b.md](./venues/ese_journal_b.md)
- 数据文件：[metadata](metadata/ese_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ese_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10664
- 学术索引页：http://dblp.uni-trier.de/db/journals/ese/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ese_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (136) / 跨域/待判定 (26) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (136) / 不属于软件工程 (27)
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (59) / ⏳ 待补信息 (82) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (163)
- 人工复核状态分布：未人工复核 (163)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (39) / 4.1.1 缺陷修复与维护性修正 (20) / 6.3.4 replication、benchmark 与开放科学 (14) / 6.5.2 协作、评审与知识共享 (6) / 3.1.4 场景化测试 (4) / 3.2.3 面向质量属性的分析 (4) / 4.1.2 重构、重模块化与代码清理 (3) / 7.1.4 AI 支持的架构、设计与工程决策 (3)
- 主题标签补充：经验软件工程 (57) / 待人工细分 (42) / 可靠性/安全 (37) / 建模/模型驱动 (32) / 维护与演化 (30)

---

### `IETS`

- 基本信息：
- 全称：IET Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`21`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：broad SE 期刊，可筛少量建模/验证论文
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (19) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/iets_journal_b.md](./venues/iets_journal_b.md)
- 数据文件：[metadata](metadata/iets_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iets_journal_b)

- 关键信息页面：
- 期刊主页：https://ietresearch.onlinelibrary.wiley.com/journal/1751880x
- 学术索引页：https://dblp.uni-trier.de/db/journals/iet-sen
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/iets_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (20) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (20) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (19) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (21)
- 人工复核状态分布：未人工复核 (21)
- 高频软工主路径：6.3.4 replication、benchmark 与开放科学 (5) / 6.4.3 度量、预测与风险模型 (4) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 3.1.4 场景化测试 (1) / 5.3.4 扩展性、吞吐与时延保证 (1) / 4.2.1 代码搜索、导航与摘要 (1) / 3.1.2 回归测试与测试选择 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：建模/模型驱动 (16) / 经验软件工程 (6) / 测试与验证 (6) / 维护与演化 (5) / 可靠性/安全 (4)

---

### `IST`

- 基本信息：
- 全称：Information and Software Technology
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`145`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 建模测试 / `AI4SE` 论文较常见
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (35) / ⏳ 待补信息 (83) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/ist_journal_b.md](./venues/ist_journal_b.md)
- 数据文件：[metadata](metadata/ist_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ist_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/information-and-software-technology
- 学术索引页：http://dblp.uni-trier.de/db/journals/infsof/index.html
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ist_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (82) / 跨域/待判定 (63)
- 软工纳入判定分布：属于软件工程 (82) / 不属于软件工程 (63)
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (35) / ⏳ 待补信息 (83) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (145)
- 人工复核状态分布：未人工复核 (145)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (13) / 6.1.1 敏捷、精益与 DevOps 方法 (7) / 6.3.1 实验、案例研究与调查 (7) / 6.3.3 系统综述、mapping 与 meta-analysis (6) / 6.3.4 replication、benchmark 与开放科学 (6) / 3.1.4 场景化测试 (4) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (4) / 1.1.1 需求获取与发现 (4)
- 主题标签补充：待人工细分 (54) / 建模/模型驱动 (33) / 经验软件工程 (26) / 可靠性/安全 (25) / 测试与验证 (25)

---

### `JSEP`

- 基本信息：
- 全称：Journal of Software: Evolution and Process
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`174`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：演化 / 过程 / 迭代闭环与工程实践邻近
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (122) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9)
- 论文名录页：[venues/jsep_journal_b.md](./venues/jsep_journal_b.md)
- 数据文件：[metadata](metadata/jsep_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jsep_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/20477481
- 学术索引页：http://dblp.uni-trier.de/db/journals/smr/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jsep_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (172) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (172) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (122) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9)
- 判定来源分布：启发式初判 (174)
- 人工复核状态分布：未人工复核 (174)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (22) / 6.3.1 实验、案例研究与调查 (13) / 4.1.2 重构、重模块化与代码清理 (11) / 3.1.4 场景化测试 (10) / 6.1.1 敏捷、精益与 DevOps 方法 (8) / 4.3.1 版本、配置与构建工程 (8) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (8) / 7.1.2 AI 支持的测试、分析与修复 (7)
- 主题标签补充：建模/模型驱动 (71) / 测试与验证 (63) / 维护与演化 (59) / 经验软件工程 (51) / 可靠性/安全 (43)

---

### `JSS`

- 基本信息：
- 全称：Journal of Systems and Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`242`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：系统与软件工程综合刊，常见建模/验证/CPS 个案
- 初筛分布：🟢 优先跟进 (56) / 🟡 保留观察 (65) / ⏳ 待补信息 (109) / ⚪ 暂不跟进 (12)
- 论文名录页：[venues/jss_journal_b.md](./venues/jss_journal_b.md)
- 数据文件：[metadata](metadata/jss_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jss_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/journal-of-systems-and-software
- 学术索引页：http://dblp.uni-trier.de/db/journals/jss/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jss_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (147) / 跨域/待判定 (91) / 系统软件 (3) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (147) / 不属于软件工程 (95)
- 初筛分布：🟢 优先跟进 (56) / 🟡 保留观察 (65) / ⏳ 待补信息 (109) / ⚪ 暂不跟进 (12)
- 判定来源分布：启发式初判 (242)
- 人工复核状态分布：未人工复核 (242)
- 高频软工主路径：2.1.1 架构描述与恢复 (13) / 3.2.3 面向质量属性的分析 (12) / 6.3.1 实验、案例研究与调查 (8) / 6.1.1 敏捷、精益与 DevOps 方法 (8) / 3.1.4 场景化测试 (7) / 2.1.4 云/服务/平台架构 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (7) / 3.2.1 静态分析与抽象解释 (5)
- 主题标签补充：待人工细分 (66) / 测试与验证 (55) / 经验软件工程 (50) / 可靠性/安全 (48) / 建模/模型驱动 (45)

---

### `RE / 期刊 / B`

- 基本信息：
- 全称：Requirements Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`24`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (0) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/re_journal_b.md](./venues/re_journal_b.md)
- 数据文件：[metadata](metadata/re_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/766
- 学术索引页：http://dblp.uni-trier.de/db/journals/re/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/re_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (21) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (21) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (0) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (24)
- 人工复核状态分布：未人工复核 (24)
- 高频软工主路径：1.1.1 需求获取与发现 (8) / 1.2.3 规约质量与一致性 (2) / 5.2.2 隐私工程与数据治理 (1) / 1.1.4 需求追踪、变更与演化 (1) / 6.5.4 教育、培训与入门支持 (1) / 5.3.1 性能建模、基准与调优 (1) / 3.2.3 面向质量属性的分析 (1) / 4.1.5 技术债、克隆与可维护性治理 (1)
- 主题标签补充：需求工程 (20) / 建模/模型驱动 (10) / 测试与验证 (4) / 可靠性/安全 (3) / 经验软件工程 (2)

---

### `SCP`

- 基本信息：
- 全称：Science of Computer Programming
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`109`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件程序与形式化/验证/程序分析交叉，贴题概率中高
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (15) / ⏳ 待补信息 (64) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/scp_journal_b.md](./venues/scp_journal_b.md)
- 数据文件：[metadata](metadata/scp_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scp_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/science-of-computer-programming
- 学术索引页：http://dblp.uni-trier.de/db/journals/scp/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/scp_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (82) / 软件工程 (27)
- 软工纳入判定分布：不属于软件工程 (82) / 属于软件工程 (14) / 跨域但软工主导 (13)
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (15) / ⏳ 待补信息 (64) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (109)
- 人工复核状态分布：未人工复核 (109)
- 高频软工主路径：1.2.1 形式化规约与契约 (6) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 6.1.1 敏捷、精益与 DevOps 方法 (2) / 4.1.2 重构、重模块化与代码清理 (2) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 1.3.1 建模语言与元模型 (2) / 3.2.4 分析驱动的理解、重构与综合 (1) / 3.2.2 动态与混合分析 (1)
- 主题标签补充：待人工细分 (32) / 建模/模型驱动 (29) / 测试与验证 (28) / 形式化方法 (25) / 需求工程 (13)

---

### `SoSyM`

- 基本信息：
- 全称：Software and Systems Modeling
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`75`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件与系统建模 / DSL / 状态机与模型分析主场
- 初筛分布：🟢 优先跟进 (32) / 🟡 保留观察 (14) / ⏳ 待补信息 (27) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/sosym_journal_b.md](./venues/sosym_journal_b.md)
- 数据文件：[metadata](metadata/sosym_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sosym_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10270
- 学术索引页：http://dblp.uni-trier.de/db/journals/sosym/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sosym_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (45) / 跨域/待判定 (29) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (45) / 不属于软件工程 (30)
- 初筛分布：🟢 优先跟进 (32) / 🟡 保留观察 (14) / ⏳ 待补信息 (27) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (75)
- 人工复核状态分布：未人工复核 (75)
- 高频软工主路径：1.3.1 建模语言与元模型 (13) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 3.1.4 场景化测试 (3) / 7.1.1 代码生成、补全与变换 (2) / 3.3.1 面向软工问题的形式化验证 (2) / 6.3.1 实验、案例研究与调查 (2) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 3.2.1 静态分析与抽象解释 (2)
- 主题标签补充：建模/模型驱动 (44) / 形式化方法 (24) / 需求工程 (16) / 测试与验证 (13) / 待人工细分 (13)

---

### `STVR`

- 基本信息：
- 全称：Software Testing, Verification and Reliability
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`26`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 验证 / 可靠性与 formal properties 非常贴题
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/stvr_journal_b.md](./venues/stvr_journal_b.md)
- 数据文件：[metadata](metadata/stvr_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-stvr_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/10991689
- 学术索引页：http://dblp.uni-trier.de/db/journals/stvr/index.html
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/stvr_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (26)
- 软工纳入判定分布：属于软件工程 (26)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (26)
- 人工复核状态分布：未人工复核 (26)
- 高频软工主路径：3.1.3 模糊、搜索式、变异与性质驱动测试 (14) / 2.2.1 设计原则、模式与反模式 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 5.2.1 安全开发与漏洞治理 (1) / 3.1.2 回归测试与测试选择 (1) / 3.1.4 场景化测试 (1) / 2.3.3 组件、包与集成工程 (1) / 2.1.3 架构演化与重构 (1)
- 主题标签补充：测试与验证 (20) / LLM/AI for SE (11) / 建模/模型驱动 (11) / 可靠性/安全 (9) / 维护与演化 (9)

---

### `SPE`

- 基本信息：
- 全称：Software: Practice and Experience
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`116`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：工程实践 / 系统实现为主，偶有 runtime/verification
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (62) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (20)
- 论文名录页：[venues/spe_journal_b.md](./venues/spe_journal_b.md)
- 数据文件：[metadata](metadata/spe_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spe_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/1097024x
- 学术索引页：http://dblp.uni-trier.de/db/journals/spe/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/spe_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (62) / 系统软件 (26) / 软件工程 (23) / 程序设计语言与形式化基础 (5)
- 软工纳入判定分布：不属于软件工程 (93) / 属于软件工程 (22) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (62) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (20)
- 判定来源分布：启发式初判 (116)
- 人工复核状态分布：未人工复核 (116)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (5) / 2.1.4 云/服务/平台架构 (3) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (2) / 2.3.3 组件、包与集成工程 (2) / 2.3.1 代码生成、脚手架与 DSL 工程 (2) / 1.1.1 需求获取与发现 (2) / 1.2.3 规约质量与一致性 (1)
- 主题标签补充：建模/模型驱动 (46) / 测试与验证 (31) / 系统软件 (25) / 维护与演化 (25) / 可靠性/安全 (23)

---

### `PASTE`

- 基本信息：
- 全称：ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近
- 初筛分布：无 2024 条目
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

### `APSEC`

- 基本信息：
- 全称：Asia-Pacific Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`68`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 亚洲社区，`LLM-SE/测试/建模` 可见
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (35) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/apsec_conf_c.md](./venues/apsec_conf_c.md)
- 数据文件：[metadata](metadata/apsec_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-apsec_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/apsec-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/apsec/
- 官方论文集页：https://doi.org/10.1109/APSEC65559.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/apsec_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (55) / 跨域/待判定 (12) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (55) / 不属于软件工程 (13)
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (35) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (68)
- 人工复核状态分布：未人工复核 (68)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (10) / 6.3.4 replication、benchmark 与开放科学 (9) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (7) / 6.4.1 代码、提交、issue 与 PR 挖掘 (5) / 1.1.1 需求获取与发现 (4) / 7.1.2 AI 支持的测试、分析与修复 (3) / 7.1.3 AI 支持的需求、建模与文档 (2) / 1.1.4 需求追踪、变更与演化 (2)
- 主题标签补充：建模/模型驱动 (29) / LLM/AI for SE (24) / 测试与验证 (23) / 可靠性/安全 (18) / 经验软件工程 (11)

---

### `EASE`

- 基本信息：
- 全称：International Conference on Evaluation and Assessment in Software Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`100`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：评测与实验设计 / benchmark / replication 有用
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (81) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9)
- 论文名录页：[venues/ease_conf_c.md](./venues/ease_conf_c.md)
- 数据文件：[metadata](metadata/ease_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ease_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ease-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/ease/
- 官方论文集页：https://doi.org/10.1145/3661167 / https://www.wikidata.org/entity/Q126710546
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ease_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (96) / 跨域/待判定 (4)
- 软工纳入判定分布：属于软件工程 (96) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (81) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9)
- 判定来源分布：启发式初判 (100)
- 人工复核状态分布：未人工复核 (100)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (17) / 6.4.1 代码、提交、issue 与 PR 挖掘 (10) / 4.1.1 缺陷修复与维护性修正 (10) / 6.3.4 replication、benchmark 与开放科学 (8) / 6.1.1 敏捷、精益与 DevOps 方法 (7) / 7.1.1 代码生成、补全与变换 (4) / 5.2.1 安全开发与漏洞治理 (4) / 3.2.3 面向质量属性的分析 (4)
- 主题标签补充：可靠性/安全 (42) / 建模/模型驱动 (41) / 经验软件工程 (31) / 测试与验证 (25) / LLM/AI for SE (21)

---

### `ICECCS`

- 基本信息：
- 全称：International Conference on Engineering of Complex Computer Systems
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`22`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：复杂系统建模与验证 / safety-critical / CPS 邻近
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/iceccs_conf_c.md](./venues/iceccs_conf_c.md)
- 数据文件：[metadata](metadata/iceccs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iceccs_conf_c)

- 关键信息页面：
- 年主页：https://cyprusconferences.org/iceccs2024/
- 学术索引页：http://dblp.uni-trier.de/db/conf/iceccs/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/iceccs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (17) / 软件工程 (5)
- 软工纳入判定分布：不属于软件工程 (17) / 属于软件工程 (3) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (22)
- 人工复核状态分布：未人工复核 (22)
- 高频软工主路径：1.3.1 建模语言与元模型 (1) / 3.3.1 面向软工问题的形式化验证 (1) / 4.1.5 技术债、克隆与可维护性治理 (1) / 6.3.1 实验、案例研究与调查 (1) / 3.2.4 分析驱动的理解、重构与综合 (1)
- 主题标签补充：待人工细分 (9) / 测试与验证 (8) / 建模/模型驱动 (3) / LLM/AI for SE (2) / 程序修复 (2)

---

### `ICST`

- 基本信息：
- 全称：IEEE International Conference on Software Testing, Verification and Validation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`49`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 形式化验证 / 缺陷检测与修复直接相关
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icst_conf_c.md](./venues/icst_conf_c.md)
- 数据文件：[metadata](metadata/icst_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icst_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icst-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/icst/
- 官方论文集页：https://doi.org/10.1109/ICST60714.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icst_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (49)
- 软工纳入判定分布：属于软件工程 (49)
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (49)
- 人工复核状态分布：未人工复核 (49)
- 高频软工主路径：3.1.3 模糊、搜索式、变异与性质驱动测试 (13) / 3.1.1 测试生成与增强 (7) / 3.1.5 测试质量、脆弱性与测试资产维护 (4) / 3.4.1 调试、分诊与根因分析 (3) / 3.4.2 缺陷定位、补丁生成与程序修复 (3) / 3.2.3 面向质量属性的分析 (3) / 7.1.2 AI 支持的测试、分析与修复 (2) / 7.1.5 人机协同开发与评估 (2)
- 主题标签补充：测试与验证 (45) / 建模/模型驱动 (20) / 可靠性/安全 (15) / LLM/AI for SE (14) / 形式化方法 (9)

---

### `SCAM`

- 基本信息：
- 全称：IEEE International Working Conference on Source Code Analysis and Manipulation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`24`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：源码分析与变换 / 缺陷修复 / 程序理解邻近
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (20) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/scam_conf_c.md](./venues/scam_conf_c.md)
- 数据文件：[metadata](metadata/scam_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scam_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/track/scam-2024/SCAM-2024-research-track
- 学术索引页：http://dblp.uni-trier.de/db/conf/scam/
- 官方论文集页：https://doi.org/10.1109/SCAM63643.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/scam_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (20) / 跨域/待判定 (4)
- 软工纳入判定分布：属于软件工程 (20) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (20) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (24)
- 人工复核状态分布：未人工复核 (24)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (4) / 6.3.1 实验、案例研究与调查 (3) / 4.2.1 代码搜索、导航与摘要 (2) / 7.1.1 代码生成、补全与变换 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (1) / 7.1.5 人机协同开发与评估 (1) / 6.4.1 代码、提交、issue 与 PR 挖掘 (1) / 3.2.1 静态分析与抽象解释 (1)
- 主题标签补充：经验软件工程 (14) / 维护与演化 (9) / 程序设计语言/编译 (6) / LLM/AI for SE (6) / 建模/模型驱动 (6)

---

### `COMPSAC`

- 基本信息：
- 全称：International Computer Software and Applications Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`388`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：覆盖过宽，需按建模/验证/`AI4SE` 子题筛选
- 初筛分布：🟢 优先跟进 (61) / 🟡 保留观察 (270) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (57)
- 论文名录页：[venues/compsac_conf_c.md](./venues/compsac_conf_c.md)
- 数据文件：[metadata](metadata/compsac_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-compsac_conf_c)

- 关键信息页面：
- 年主页：https://ieeecompsac.computer.org/2024/
- 学术索引页：http://dblp.uni-trier.de/db/conf/compsac/
- 官方论文集页：https://doi.org/10.1109/COMPSAC61105.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/compsac_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (294) / 软件工程 (51) / 系统软件 (37) / 程序设计语言与形式化基础 (6)
- 软工纳入判定分布：不属于软件工程 (337) / 属于软件工程 (41) / 跨域但软工主导 (10)
- 初筛分布：🟢 优先跟进 (61) / 🟡 保留观察 (270) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (57)
- 判定来源分布：启发式初判 (388)
- 人工复核状态分布：未人工复核 (388)
- 高频软工主路径：2.1.1 架构描述与恢复 (5) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (4) / 3.2.1 静态分析与抽象解释 (3) / 7.1.1 代码生成、补全与变换 (3) / 2.1.4 云/服务/平台架构 (2) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (2) / 4.1.1 缺陷修复与维护性修正 (2)
- 主题标签补充：建模/模型驱动 (195) / 测试与验证 (98) / 可靠性/安全 (82) / LLM/AI for SE (71) / 维护与演化 (52)

---

### `ICFEM`

- 基本信息：
- 全称：International Conference on Formal Engineering Methods
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`22`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：formal engineering / 规约建模 / 验证与证明
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icfem_conf_c.md](./venues/icfem_conf_c.md)
- 数据文件：[metadata](metadata/icfem_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icfem_conf_c)

- 关键信息页面：
- 年主页：https://icfem2024.info/
- 学术索引页：http://dblp.uni-trier.de/db/conf/icfem/
- 官方论文集页：https://doi.org/10.1007/978-981-96-0617-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icfem_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (14) / 软件工程 (8)
- 软工纳入判定分布：不属于软件工程 (14) / 属于软件工程 (5) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (22)
- 人工复核状态分布：未人工复核 (22)
- 高频软工主路径：1.3.3 模型分析、仿真与验证 (3) / 1.2.1 形式化规约与契约 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 4.4.1 可观测性、日志与异常检测 (1) / 3.3.1 面向软工问题的形式化验证 (1)
- 主题标签补充：形式化方法 (13) / 测试与验证 (6) / 建模/模型驱动 (5) / 待人工细分 (4) / LLM/AI for SE (3)

---

### `SSE`

- 基本信息：
- 全称：IEEE International Conference on Software Services Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`47`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件服务工程混合
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (25) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (10)
- 论文名录页：[venues/sse_conf_c.md](./venues/sse_conf_c.md)
- 数据文件：[metadata](metadata/sse_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sse_conf_c)

- 关键信息页面：
- 年主页：未检出 2024 年主页
- 学术索引页：http://dblp.uni-trier.de/db/conf/IEEEscc/
- 官方论文集页：https://doi.org/10.1109/SSE62657.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/sse_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (30) / 软件工程 (9) / 系统软件 (7) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (38) / 属于软件工程 (6) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (25) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (10)
- 判定来源分布：启发式初判 (47)
- 人工复核状态分布：未人工复核 (47)
- 高频软工主路径：6.5.4 教育、培训与入门支持 (2) / 2.1.4 云/服务/平台架构 (2) / 7.1.2 AI 支持的测试、分析与修复 (2) / 4.4.1 可观测性、日志与异常检测 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 1.3.1 建模语言与元模型 (1)
- 主题标签补充：建模/模型驱动 (22) / 待人工细分 (11) / LLM/AI for SE (11) / 需求工程 (10) / 经验软件工程 (9)

---

### `ICSSP`

- 基本信息：
- 全称：International Conference on Software and System Process
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`9`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件过程 / 团队与流程，对主问题较间接
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/icssp_conf_c.md](./venues/icssp_conf_c.md)
- 数据文件：[metadata](metadata/icssp_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icssp_conf_c)

- 关键信息页面：
- 年主页：https://icssp2024.events.isspa-process.org/
- 学术索引页：http://dblp.uni-trier.de/db/conf/ispw/
- 官方论文集页：https://doi.org/10.1145/3666015
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icssp_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (8) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (8) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (9)
- 人工复核状态分布：未人工复核 (9)
- 高频软工主路径：6.5.2 协作、评审与知识共享 (1) / 6.5.1 开发者认知、生产力与福祉 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 4.1.1 缺陷修复与维护性修正 (1) / 2.1.4 云/服务/平台架构 (1) / 1.2.3 规约质量与一致性 (1) / 3.1.4 场景化测试 (1) / 1.1.4 需求追踪、变更与演化 (1)
- 主题标签补充：建模/模型驱动 (6) / 维护与演化 (3) / 形式化方法 (2) / 需求工程 (2) / 经验软件工程 (1)

---

### `SEKE`

- 基本信息：
- 全称：International Conference on Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`81`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 偶有贴题
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (44) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/seke_conf_c.md](./venues/seke_conf_c.md)
- 数据文件：[metadata](metadata/seke_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-seke_conf_c)

- 关键信息页面：
- 年主页：https://ksiresearch.org/seke/seke24.html
- 学术索引页：http://dblp.uni-trier.de/db/conf/seke/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/seke_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (61) / 软件工程 (12) / 程序设计语言与形式化基础 (4) / 系统软件 (4)
- 软工纳入判定分布：不属于软件工程 (69) / 属于软件工程 (9) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (44) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (81)
- 人工复核状态分布：未人工复核 (81)
- 高频软工主路径：4.2.1 代码搜索、导航与摘要 (2) / 1.3.3 模型分析、仿真与验证 (2) / 7.1.2 AI 支持的测试、分析与修复 (1) / 1.1.3 需求质量与歧义控制 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 4.4.1 可观测性、日志与异常检测 (1) / 4.1.1 缺陷修复与维护性修正 (1) / 3.2.1 静态分析与抽象解释 (1)
- 主题标签补充：建模/模型驱动 (36) / 待人工细分 (16) / 可靠性/安全 (15) / 维护与演化 (11) / LLM/AI for SE (11)

---

### `QRS`

- 基本信息：
- 全称：International Conference on Software Quality, Reliability and Security
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`71`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：质量 / 可靠性 / 安全 / assurance 与验证链很近
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (43) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/qrs_conf_c.md](./venues/qrs_conf_c.md)
- 数据文件：[metadata](metadata/qrs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-qrs_conf_c)

- 关键信息页面：
- 年主页：https://qrs24.techconf.org/
- 学术索引页：https://dblp.uni-trier.de/db/conf/qrs
- 官方论文集页：https://doi.org/10.1109/QRS62785.2024
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/qrs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (70) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (70) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (43) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (71)
- 人工复核状态分布：未人工复核 (71)
- 高频软工主路径：3.1.1 测试生成与增强 (8) / 3.2.3 面向质量属性的分析 (8) / 7.1.4 AI 支持的架构、设计与工程决策 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 7.1.2 AI 支持的测试、分析与修复 (4) / 3.1.4 场景化测试 (3) / 3.3.1 面向软工问题的形式化验证 (3) / 4.2.1 代码搜索、导航与摘要 (3)
- 主题标签补充：测试与验证 (36) / 建模/模型驱动 (33) / 可靠性/安全 (29) / LLM/AI for SE (20) / 形式化方法 (14)

---

### `ICSR`

- 基本信息：
- 全称：International Conference on Software Reuse
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`11`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：复用 / 组件资产，可补模型资产与可复用工件
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsr_conf_c.md](./venues/icsr_conf_c.md)
- 数据文件：[metadata](metadata/icsr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsr_conf_c)

- 关键信息页面：
- 年主页：https://icsr2024.dk/
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsr/
- 官方论文集页：https://doi.org/10.1007/978-3-031-66459-5
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (8) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (8) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (11)
- 人工复核状态分布：未人工复核 (11)
- 高频软工主路径：2.2.1 设计原则、模式与反模式 (2) / 1.4.1 特征建模与配置 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 3.2.1 静态分析与抽象解释 (1) / 7.1.1 代码生成、补全与变换 (1) / 2.2.2 模块化、依赖与解耦 (1) / 4.2.1 代码搜索、导航与摘要 (1)
- 主题标签补充：待人工细分 (6) / 维护与演化 (1) / 测试与验证 (1) / 程序分析 (1) / LLM/AI for SE (1)

---

### `SPIN`

- 基本信息：
- 全称：International Symposium on Model Checking of Software
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`14`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件模型检查 / state-based verification / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/spin_conf_c.md](./venues/spin_conf_c.md)
- 数据文件：[metadata](metadata/spin_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spin_conf_c)

- 关键信息页面：
- 年主页：https://spin-web.github.io/SPIN2024/
- 学术索引页：http://dblp.uni-trier.de/db/conf/spin/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/spin_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (7) / 软件工程 (7)
- 软工纳入判定分布：不属于软件工程 (7) / 属于软件工程 (5) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (14)
- 人工复核状态分布：未人工复核 (14)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (3) / 1.3.3 模型分析、仿真与验证 (3) / 1.3.1 建模语言与元模型 (1)
- 主题标签补充：测试与验证 (6) / 形式化方法 (6) / 建模/模型驱动 (5) / 待人工细分 (3) / 维护与演化 (2)

---

### `TASE`

- 基本信息：
- 全称：Theoretical Aspects of Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`27`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件工程名下的 formal verification / assurance 邻近
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/tase_conf_c.md](./venues/tase_conf_c.md)
- 数据文件：[metadata](metadata/tase_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tase_conf_c)

- 关键信息页面：
- 年主页：https://tase2024.github.io/
- 学术索引页：http://dblp.uni-trier.de/db/conf/tase/
- 官方论文集页：https://doi.org/10.1007/978-3-031-64626-3
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/tase_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (18) / 软件工程 (8) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (19) / 跨域但软工主导 (7) / 属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：1.2.1 形式化规约与契约 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 3.2.1 静态分析与抽象解释 (1) / 1.3.3 模型分析、仿真与验证 (1) / 1.1.4 需求追踪、变更与演化 (1)
- 主题标签补充：测试与验证 (10) / 待人工细分 (7) / 形式化方法 (4) / 可靠性/安全 (4) / LLM/AI for SE (3)

---

### `MSR`

- 基本信息：
- 全称：Mining Software Repositories
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`97`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：仓库挖掘 / benchmark / `LLM-SE` 证据与数据建设有用
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (75) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/msr_conf_c.md](./venues/msr_conf_c.md)
- 数据文件：[metadata](metadata/msr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-msr_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/msr-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/msr/
- 官方论文集页：https://doi.org/10.1145/3643991 / https://ieeexplore.ieee.org/xpl/conhome/10555570/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/msr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (94) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (94) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (75) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 判定来源分布：启发式初判 (97)
- 人工复核状态分布：未人工复核 (97)
- 高频软工主路径：6.3.4 replication、benchmark 与开放科学 (39) / 4.1.1 缺陷修复与维护性修正 (11) / 6.3.1 实验、案例研究与调查 (10) / 7.1.1 代码生成、补全与变换 (8) / 6.4.1 代码、提交、issue 与 PR 挖掘 (6) / 3.1.4 场景化测试 (3) / 6.1.1 敏捷、精益与 DevOps 方法 (3) / 7.1.4 AI 支持的架构、设计与工程决策 (2)
- 主题标签补充：经验软件工程 (43) / 建模/模型驱动 (37) / 维护与演化 (31) / 可靠性/安全 (23) / LLM/AI for SE (20)

---

### `REFSQ`

- 基本信息：
- 全称：Requirements Engineering: Foundation for Software Quality
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`22`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求质量 / 需求规约 / 需求到性质非常贴题
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/refsq_conf_c.md](./venues/refsq_conf_c.md)
- 数据文件：[metadata](metadata/refsq_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-refsq_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/refsq-2024
- 学术索引页：http://dblp.uni-trier.de/db/conf/refsq/
- 官方论文集页：https://doi.org/10.1007/978-3-031-57327-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/refsq_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (17) / 跨域/待判定 (5)
- 软工纳入判定分布：属于软件工程 (17) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (22)
- 人工复核状态分布：未人工复核 (22)
- 高频软工主路径：1.1.1 需求获取与发现 (9) / 3.2.3 面向质量属性的分析 (1) / 5.2.2 隐私工程与数据治理 (1) / 1.1.3 需求质量与歧义控制 (1) / 2.2.1 设计原则、模式与反模式 (1) / 1.2.1 形式化规约与契约 (1) / 7.2.4 MLOps、部署与演化 (1) / 6.3.1 实验、案例研究与调查 (1)
- 主题标签补充：需求工程 (15) / 待人工细分 (6) / 可靠性/安全 (3) / LLM/AI for SE (3) / 建模/模型驱动 (2)

---

### `WICSA`

- 基本信息：
- 全称：Working IEEE/IFIP Conference on Software Architecture
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件架构 / 设计决策 / 模型结构与演化有用
- 初筛分布：无 2024 条目
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

---

### `Internetware`

- 基本信息：
- 全称：Asia-Pacific Symposium on Internetware
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`56`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：平台 / 网络化软件 / 运行治理邻近
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (38) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/internetware_conf_c.md](./venues/internetware_conf_c.md)
- 数据文件：[metadata](metadata/internetware_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-internetware_conf_c)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/internetware-2024
- 学术索引页：https://dblp.org/db/conf/internetware/index.html
- 官方论文集页：https://doi.org/10.1145/3671016
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/internetware_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (49) / 跨域/待判定 (6) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (49) / 不属于软件工程 (7)
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (38) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (56)
- 人工复核状态分布：未人工复核 (56)
- 高频软工主路径：2.1.4 云/服务/平台架构 (20) / 7.1.2 AI 支持的测试、分析与修复 (5) / 5.3.4 扩展性、吞吐与时延保证 (3) / 4.4.1 可观测性、日志与异常检测 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 3.1.4 场景化测试 (2) / 3.2.1 静态分析与抽象解释 (2) / 6.2.1 估算、计划与排程 (1)
- 主题标签补充：建模/模型驱动 (24) / 测试与验证 (18) / 可靠性/安全 (16) / LLM/AI for SE (9) / 维护与演化 (9)

---

### `RV`

- 基本信息：
- 全称：International Conference on Runtime Verification
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2024`
- 条目数：`18`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：运行时验证 / 监测 / 时序性质 / 工具链直接邻近
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/rv_conf_c.md](./venues/rv_conf_c.md)
- 数据文件：[metadata](metadata/rv_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-rv_conf_c)

- 关键信息页面：
- 年主页：https://bouncmpe.github.io/rv24/
- 学术索引页：https://dblp.org/db/conf/rv/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/rv_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (12) / 软件工程 (5) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (13) / 跨域但软工主导 (4) / 属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (18)
- 人工复核状态分布：未人工复核 (18)
- 高频软工主路径：3.3.2 运行时验证与运行时监测 (5)
- 主题标签补充：运行时监测 (10) / 形式化方法 (4) / 待人工细分 (4) / 测试与验证 (3) / 需求工程 (2)

---

### `IJSEKE`

- 基本信息：
- 全称：International Journal of Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`76`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 可补链但不稳定
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (48) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/ijseke_journal_c.md](./venues/ijseke_journal_c.md)
- 数据文件：[metadata](metadata/ijseke_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ijseke_journal_c)

- 关键信息页面：
- 期刊主页：https://www.worldscientific.com/worldscinet/ijseke
- 学术索引页：http://dblp.uni-trier.de/db/journals/ijseke/index.html
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ijseke_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (60) / 跨域/待判定 (15) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (60) / 不属于软件工程 (16)
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (48) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (76)
- 人工复核状态分布：未人工复核 (76)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (11) / 6.3.4 replication、benchmark 与开放科学 (5) / 7.1.4 AI 支持的架构、设计与工程决策 (4) / 3.1.4 场景化测试 (4) / 1.3.1 建模语言与元模型 (3) / 1.1.1 需求获取与发现 (3) / 3.2.3 面向质量属性的分析 (3) / 4.3.1 版本、配置与构建工程 (2)
- 主题标签补充：建模/模型驱动 (34) / 测试与验证 (24) / 经验软件工程 (18) / 维护与演化 (17) / 可靠性/安全 (15)

---

### `STTT`

- 基本信息：
- 全称：International Journal of Software Tools for Technology Transfer
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`48`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：验证工具 / formal methods tool transfer / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (10) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/sttt_journal_c.md](./venues/sttt_journal_c.md)
- 数据文件：[metadata](metadata/sttt_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sttt_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10009
- 学术索引页：http://dblp.uni-trier.de/db/journals/sttt/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sttt_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (29) / 软件工程 (18) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (30) / 跨域但软工主导 (11) / 属于软件工程 (7)
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (10) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (48)
- 人工复核状态分布：未人工复核 (48)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (8) / 3.3.1 面向软工问题的形式化验证 (4) / 6.3.1 实验、案例研究与调查 (2) / 1.2.1 形式化规约与契约 (1) / 4.1.1 缺陷修复与维护性修正 (1) / 4.3.2 CI/CD 与发布工程 (1) / 3.2.3 面向质量属性的分析 (1)
- 主题标签补充：形式化方法 (19) / 测试与验证 (18) / 建模/模型驱动 (11) / 程序分析 (9) / 需求工程 (8)

---

### `SOCA`

- 基本信息：
- 全称：Service Oriented Computing and Applications
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`25`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务计算与应用为主
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (3) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/soca_journal_c.md](./venues/soca_journal_c.md)
- 数据文件：[metadata](metadata/soca_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-soca_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11761
- 学术索引页：http://dblp.uni-trier.de/db/journals/soca/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/soca_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (23) / 程序设计语言与形式化基础 (1) / 软件工程 (1)
- 软工纳入判定分布：不属于软件工程 (24) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (3) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (25)
- 人工复核状态分布：未人工复核 (25)
- 高频软工主路径：2.1.4 云/服务/平台架构 (1)
- 主题标签补充：待人工细分 (12) / 可靠性/安全 (4) / 建模/模型驱动 (3) / 程序设计语言/编译 (2) / 维护与演化 (2)

---

### `SQJ`

- 基本信息：
- 全称：Software Quality Journal
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2024`
- 条目数：`56`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：质量 / 度量 / assurance 视角可支撑验证评价
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (12) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sqj_journal_c.md](./venues/sqj_journal_c.md)
- 数据文件：[metadata](metadata/sqj_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sqj_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11219
- 学术索引页：http://dblp.uni-trier.de/db/journals/sqj/
- 2024 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sqj_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (46) / 跨域/待判定 (10)
- 软工纳入判定分布：属于软件工程 (46) / 不属于软件工程 (10)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (12) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (56)
- 人工复核状态分布：未人工复核 (56)
- 高频软工主路径：3.1.1 测试生成与增强 (8) / 6.3.1 实验、案例研究与调查 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (5) / 3.2.3 面向质量属性的分析 (5) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 3.3.1 面向软工问题的形式化验证 (2) / 4.1.5 技术债、克隆与可维护性治理 (2) / 4.1.2 重构、重模块化与代码清理 (1)
- 主题标签补充：建模/模型驱动 (17) / 测试与验证 (16) / 可靠性/安全 (13) / 待人工细分 (12) / 需求工程 (6)

## 7. 本年度总体观察

- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (1229) / 🟡 保留观察 (2474) / ⏳ 待补信息 (765) / ⚪ 暂不跟进 (295)
- 一级总判定分布：软件工程 (2890) / 跨域/待判定 (1197) / 程序设计语言与形式化基础 (438) / 系统软件 (238)
- 软工纳入判定分布：属于软件工程 (2798) / 不属于软件工程 (1873) / 跨域但软工主导 (92)
- 判定来源分布：启发式初判 (4763)
- 人工复核状态分布：未人工复核 (4763)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (306) / 6.3.1 实验、案例研究与调查 (191) / 6.3.4 replication、benchmark 与开放科学 (186) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (173) / 7.1.2 AI 支持的测试、分析与修复 (120) / 4.1.1 缺陷修复与维护性修正 (112) / 7.1.4 AI 支持的架构、设计与工程决策 (107) / 3.1.4 场景化测试 (98) / 1.1.1 需求获取与发现 (94) / 3.2.1 静态分析与抽象解释 (78) / 3.2.3 面向质量属性的分析 (77) / 2.1.4 云/服务/平台架构 (69) / 3.1.1 测试生成与增强 (52) / 6.4.1 代码、提交、issue 与 PR 挖掘 (52) / 4.2.1 代码搜索、导航与摘要 (50)
- 计数复核状态：以 [verification.json](./verification.json) 为准；默认要求 `expected_total == actual_total`。
- 分类终判状态：以 `metadata/*.json` 中的 `classification_source / manual_review_status / manual_review_note` 为准。
- 后续若继续扩年份或重跑年度页，建议先运行 `tools/ccf_se_index_builder.py`，再运行 `tools/ccf_se_classifier.py`。
