# `2018` 年度汇总

## 1. 年份说明

- 年份：`2018`
- 覆盖范围：`CCF_SE_A_B_C.md` 当前保留的 `CCF` 软件工程高相关 venue 子集
- 当前覆盖的 venue 数量：`57`
- 当前已入表论文数量：`3315`
- 更新时间：`2026-04-07 09:27`
- 说明：本页先由 `tools/ccf_se_index_builder.py` 生成基础元数据，再由 `tools/ccf_se_classifier.py` 对未终判条目做启发式初判；若 `metadata/*.json` 中已写回人工终判，则直接保留该终判。逐篇论文名录拆分到 `venues/*.md`。

## 2. 年度汇总统计

- A 类会议：`371`
- A 类期刊：`163`
- B 类会议：`540`
- B 类期刊：`999`
- C 类会议：`1037`
- C 类期刊：`205`
- 期望总条目数：`3315`
- 实际总条目数：`3315`
- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (848) / 🟡 保留观察 (1281) / ⏳ 待补信息 (890) / ⚪ 暂不跟进 (296)
- 一级总判定分布：软件工程 (1780) / 跨域/待判定 (1075) / 程序设计语言与形式化基础 (349) / 系统软件 (111)
- 软工纳入判定分布：属于软件工程 (1713) / 不属于软件工程 (1535) / 跨域但软工主导 (67)
- 判定来源分布：启发式初判 (3315)
- 人工复核状态分布：未人工复核 (3315)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (133) / 7.1.1 代码生成、补全与变换 (101) / 1.1.1 需求获取与发现 (101) / 4.1.1 缺陷修复与维护性修正 (100) / 3.1.4 场景化测试 (90) / 1.3.1 建模语言与元模型 (71) / 3.2.3 面向质量属性的分析 (68) / 6.3.4 replication、benchmark 与开放科学 (67) / 6.1.1 敏捷、精益与 DevOps 方法 (59) / 7.1.4 AI 支持的架构、设计与工程决策 (57) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (51) / 3.1.1 测试生成与增强 (46)

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
- `主体归属`、`软工归属级别`、`氛围` 与 `典型软工路径（先验）` 来自 venue 级先验；`2018` 逐篇统计直接按本年度 `metadata/*.json` 中的终判字段汇总。
- `典型软工路径（先验）` 与 `2018 高频软工主路径` 使用 [SOFTWARE_ENGINEERING_FIELD_TREE.md](../../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的方向树口径。

| venue | 全称 | 等级 | 类型 | 论文数 | 软工归属级别 | 氛围 | 主体归属 | 典型软工路径（先验） | 当年一级总判定 | 当年软工纳入 | 初筛分布 | 当年高频软工主路径 | 论文名录 | 数据文件 | 备注 |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | `A` | `会议` | 0 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 3.4.x | 无 2018 条目 | 无 2018 条目 | 无 2018 条目 | 无纳入软工主路径 | [venue](venues/pldi_conf_a.md) | [metadata](metadata/pldi_conf_a.json) | 计数一致；2018 无条目，暂以先验为准 |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | `A` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 无 2018 条目 | 无 2018 条目 | 无 2018 条目 | 无纳入软工主路径 | [venue](venues/fse_conf_a.md) | [metadata](metadata/fse_conf_a.json) | 计数一致；2018 无条目，暂以先验为准 |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages, and Applications | `A` | `会议` | 60 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 3.4.x / 4.2.x | 程序设计语言与形式化基础 47 / 系统软件 7 / 软件工程 6 | 不属于软件工程 54 / 属于软件工程 4 / 跨域但软工主导 2 | 🟢 优先跟进 (18) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 2.2.1 设计原则、模式与反模式 (1) / 4.1.2 重构、重模块化与代码清理 (1) | [venue](venues/oopsla_conf_a.md) | [metadata](metadata/oopsla_conf_a.json) | 计数一致；2018 比先验更偏非软工 |
| `ASE / 会议 / A` | International Conference on Automated Software Engineering | `A` | `会议` | 112 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 108 / 跨域/待判定 3 / 程序设计语言与形式化基础 1 | 属于软件工程 108 / 不属于软件工程 4 | 🟢 优先跟进 (38) / 🟡 保留观察 (70) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 7.1.1 代码生成、补全与变换 (27) / 3.2.1 静态分析与抽象解释 (9) | [venue](venues/ase_conf_a.md) | [metadata](metadata/ase_conf_a.json) | 计数一致；2018 与先验一致 |
| `ICSE` | International Conference on Software Engineering | `A` | `会议` | 153 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 149 / 跨域/待判定 3 / 程序设计语言与形式化基础 1 | 属于软件工程 149 / 不属于软件工程 4 | 🟢 优先跟进 (49) / 🟡 保留观察 (94) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10) | 7.1.1 代码生成、补全与变换 (26) / 6.3.1 实验、案例研究与调查 (15) | [venue](venues/icse_conf_a.md) | [metadata](metadata/icse_conf_a.json) | 计数一致；2018 与先验一致 |
| `ISSTA` | International Symposium on Software Testing and Analysis | `A` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 无 2018 条目 | 无 2018 条目 | 无 2018 条目 | 无纳入软工主路径 | [venue](venues/issta_conf_a.md) | [metadata](metadata/issta_conf_a.json) | 计数一致；2018 无条目，暂以先验为准 |
| `FM` | International Symposium on Formal Methods | `A` | `会议` | 46 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 38 / 软件工程 7 / 系统软件 1 | 不属于软件工程 39 / 属于软件工程 4 / 跨域但软工主导 3 | 🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (36) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (2) / 1.3.3 模型分析、仿真与验证 (2) | [venue](venues/fm_conf_a.md) | [metadata](metadata/fm_conf_a.json) | 计数一致；2018 比先验更偏非软工 |
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | `A` | `期刊` | 25 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 23 / 跨域/待判定 2 | 属于软件工程 23 / 不属于软件工程 2 | 🟢 优先跟进 (9) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 1.2.3 规约质量与一致性 (3) / 4.1.2 重构、重模块化与代码清理 (2) | [venue](venues/tosem_journal_a.md) | [metadata](metadata/tosem_journal_a.json) | 计数一致；2018 与先验一致 |
| `TSE` | IEEE Transactions on Software Engineering | `A` | `期刊` | 61 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 58 / 跨域/待判定 3 | 属于软件工程 58 / 不属于软件工程 3 | 🟢 优先跟进 (12) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 7.1.1 代码生成、补全与变换 (7) / 4.1.2 重构、重模块化与代码清理 (6) | [venue](venues/tse_journal_a.md) | [metadata](metadata/tse_journal_a.json) | 计数一致；2018 与先验一致 |
| `TSC` | IEEE Transactions on Services Computing | `A` | `期刊` | 77 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 5.3.x / 8.2.x | 跨域/待判定 56 / 软件工程 11 / 系统软件 10 | 不属于软件工程 66 / 属于软件工程 8 / 跨域但软工主导 3 | 🟢 优先跟进 (27) / 🟡 保留观察 (32) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18) | 2.1.4 云/服务/平台架构 (5) / 3.3.3 assurance、认证与合规验证 (1) | [venue](venues/tsc_journal_a.md) | [metadata](metadata/tsc_journal_a.json) | 计数一致；2018 比先验更偏非软工 |
| `ECOOP` | European Conference on Object-Oriented Programming | `B` | `会议` | 27 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 4.2.x | 程序设计语言与形式化基础 22 / 系统软件 3 / 软件工程 2 | 不属于软件工程 25 / 属于软件工程 1 / 跨域但软工主导 1 | 🟢 优先跟进 (7) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5) | 3.1.1 测试生成与增强 (1) / 3.1.2 回归测试与测试选择 (1) | [venue](venues/ecoop_conf_b.md) | [metadata](metadata/ecoop_conf_b.json) | 计数一致；2018 比先验更偏非软工 |
| `ICPC` | IEEE International Conference on Program Comprehension | `B` | `会议` | 48 | 完全属于软工 | B 🟢 | 软件工程 | 4.2.x / 4.1.x / 6.5.1 | 软件工程 46 / 跨域/待判定 2 | 属于软件工程 46 / 不属于软件工程 2 | 🟢 优先跟进 (4) / 🟡 保留观察 (40) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 6.5.1 开发者认知、生产力与福祉 (14) / 4.2.4 克隆、相似性与理解支持 (6) | [venue](venues/icpc_conf_b.md) | [metadata](metadata/icpc_conf_b.json) | 计数一致；2018 与先验一致 |
| `RE / 会议 / B` | IEEE International Requirements Engineering Conference | `B` | `会议` | 70 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x / 6.1.x | 软件工程 70 | 属于软件工程 70 | 🟢 优先跟进 (66) / 🟡 保留观察 (4) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (26) / 6.3.1 实验、案例研究与调查 (6) | [venue](venues/re_conf_b.md) | [metadata](metadata/re_conf_b.json) | 计数一致；2018 与先验一致 |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | `B` | `会议` | 37 | 部分属于软工 | B 🟢 | 信息系统工程与软件工程交叉 | 1.3.x / 2.1.x / 4.3.x / 8.3.x | 跨域/待判定 32 / 软件工程 5 | 不属于软件工程 32 / 属于软件工程 3 / 跨域但软工主导 2 | 🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (34) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (3) / 6.1.1 敏捷、精益与 DevOps 方法 (1) | [venue](venues/caise_conf_b.md) | [metadata](metadata/caise_conf_b.json) | 计数一致；2018 比先验更偏非软工 |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | `B` | `会议` | 45 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 39 / 跨域/待判定 6 | 属于软件工程 39 / 不属于软件工程 6 | 🟢 优先跟进 (19) / 🟡 保留观察 (24) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 1.3.1 建模语言与元模型 (13) / 1.3.2 模型转换、同步与协同 (10) | [venue](venues/models_conf_b.md) | [metadata](metadata/models_conf_b.json) | 计数一致；2018 与先验一致 |
| `ICSOC` | International Conference on Service Oriented Computing | `B` | `会议` | 63 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 54 / 软件工程 7 / 系统软件 2 | 不属于软件工程 56 / 属于软件工程 6 / 跨域但软工主导 1 | 🟢 优先跟进 (2) / 🟡 保留观察 (0) / ⏳ 待补信息 (61) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (3) / 6.2.1 估算、计划与排程 (1) | [venue](venues/icsoc_conf_b.md) | [metadata](metadata/icsoc_conf_b.json) | 计数一致；2018 比先验更偏非软工 |
| `SANER` | IEEE International Conference on Software Analysis, Evolution, and Reengineering | `B` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 3.2.x / 3.4.x | 无 2018 条目 | 无 2018 条目 | 无 2018 条目 | 无纳入软工主路径 | [venue](venues/saner_conf_b.md) | [metadata](metadata/saner_conf_b.json) | 计数一致；2018 无条目，暂以先验为准 |
| `ICSME` | International Conference on Software Maintenance and Evolution | `B` | `会议` | 86 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 4.3.x / 6.4.x | 软件工程 86 | 属于软件工程 86 | 🟢 优先跟进 (18) / 🟡 保留观察 (64) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 4.1.1 缺陷修复与维护性修正 (12) / 6.4.1 代码、提交、issue 与 PR 挖掘 (6) | [venue](venues/icsme_conf_b.md) | [metadata](metadata/icsme_conf_b.json) | 计数一致；2018 与先验一致 |
| `VMCAI` | International Conference on Verification, Model Checking, and Abstract Interpretation | `B` | `会议` | 24 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 20 / 软件工程 4 | 不属于软件工程 20 / 属于软件工程 3 / 跨域但软工主导 1 | 🟢 优先跟进 (5) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (3) / 3.2.1 静态分析与抽象解释 (1) | [venue](venues/vmcai_conf_b.md) | [metadata](metadata/vmcai_conf_b.json) | 计数一致；2018 比先验更偏非软工 |
| `ICWS` | IEEE International Conference on Web Services | `B` | `会议` | 59 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 5.3.x / 8.2.3 | 跨域/待判定 48 / 系统软件 6 / 软件工程 5 | 不属于软件工程 54 / 属于软件工程 4 / 跨域但软工主导 1 | 🟢 优先跟进 (6) / 🟡 保留观察 (38) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (15) | 4.1.1 缺陷修复与维护性修正 (1) / 3.3.1 面向软工问题的形式化验证 (1) | [venue](venues/icws_conf_b.md) | [metadata](metadata/icws_conf_b.json) | 计数一致；2018 比先验更偏非软工 |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | `B` | `会议` | 58 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 55 / 跨域/待判定 3 | 属于软件工程 55 / 不属于软件工程 3 | 🟢 优先跟进 (10) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6) | 6.3.1 实验、案例研究与调查 (16) / 4.1.1 缺陷修复与维护性修正 (14) | [venue](venues/esem_conf_b.md) | [metadata](metadata/esem_conf_b.json) | 计数一致；2018 与先验一致 |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | `B` | `会议` | 23 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x / 5.2.x / 4.4.x | 软件工程 22 / 跨域/待判定 1 | 属于软件工程 22 / 不属于软件工程 1 | 🟢 优先跟进 (8) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 3.1.4 场景化测试 (4) / 3.1.2 回归测试与测试选择 (3) | [venue](venues/issre_conf_b.md) | [metadata](metadata/issre_conf_b.json) | 计数一致；2018 与先验一致 |
| `ASE / 期刊 / B` | Automated Software Engineering | `B` | `期刊` | 26 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 15 / 跨域/待判定 10 / 系统软件 1 | 属于软件工程 15 / 不属于软件工程 11 | 🟢 优先跟进 (4) / 🟡 保留观察 (1) / ⏳ 待补信息 (21) / ⚪ 暂不跟进 (0) | 1.1.4 需求追踪、变更与演化 (2) / 3.2.4 分析驱动的理解、重构与综合 (2) | [venue](venues/ase_journal_b.md) | [metadata](metadata/ase_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `ESE` | Empirical Software Engineering | `B` | `期刊` | 105 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 73 / 跨域/待判定 31 / 系统软件 1 | 属于软件工程 73 / 不属于软件工程 32 | 🟢 优先跟进 (18) / 🟡 保留观察 (10) / ⏳ 待补信息 (75) / ⚪ 暂不跟进 (2) | 4.1.1 缺陷修复与维护性修正 (27) / 6.3.1 实验、案例研究与调查 (13) | [venue](venues/ese_journal_b.md) | [metadata](metadata/ese_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `IETS` | IET Software | `B` | `期刊` | 56 | 大部分属于软工 | C 🟡 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 5.x.x | 软件工程 33 / 跨域/待判定 21 / 系统软件 2 | 属于软件工程 33 / 不属于软件工程 23 | 🟢 优先跟进 (14) / 🟡 保留观察 (34) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (6) | 1.1.1 需求获取与发现 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (3) | [venue](venues/iets_journal_b.md) | [metadata](metadata/iets_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `IST` | Information and Software Technology | `B` | `期刊` | 172 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 跨域/待判定 88 / 软件工程 84 | 不属于软件工程 88 / 属于软件工程 84 | 🟢 优先跟进 (19) / 🟡 保留观察 (7) / ⏳ 待补信息 (146) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (13) / 7.1.1 代码生成、补全与变换 (9) | [venue](venues/ist_journal_b.md) | [metadata](metadata/ist_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `JSEP` | Journal of Software: Evolution and Process | `B` | `期刊` | 87 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.3.x / 6.1.x / 6.4.x | 软件工程 82 / 跨域/待判定 4 / 系统软件 1 | 属于软件工程 82 / 不属于软件工程 5 | 🟢 优先跟进 (25) / 🟡 保留观察 (55) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 6.1.1 敏捷、精益与 DevOps 方法 (10) / 6.3.1 实验、案例研究与调查 (10) | [venue](venues/jsep_journal_b.md) | [metadata](metadata/jsep_journal_b.json) | 计数一致；2018 与先验一致 |
| `JSS` | Journal of Systems and Software | `B` | `期刊` | 216 | 大部分属于软工 | B 🟢 | 软件工程 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 113 / 软件工程 100 / 系统软件 3 | 不属于软件工程 116 / 属于软件工程 100 | 🟢 优先跟进 (23) / 🟡 保留观察 (8) / ⏳ 待补信息 (185) / ⚪ 暂不跟进 (0) | 2.1.1 架构描述与恢复 (25) / 6.3.1 实验、案例研究与调查 (7) | [venue](venues/jss_journal_b.md) | [metadata](metadata/jss_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `RE / 期刊 / B` | Requirements Engineering | `B` | `期刊` | 23 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 19 / 跨域/待判定 4 | 属于软件工程 19 / 不属于软件工程 4 | 🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (11) / 1.1.2 需求分析、协商与优先级 (2) | [venue](venues/re_journal_b.md) | [metadata](metadata/re_journal_b.json) | 计数一致；2018 与先验一致 |
| `SCP` | Science of Computer Programming | `B` | `期刊` | 123 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 4.1.x | 程序设计语言与形式化基础 104 / 软件工程 18 / 系统软件 1 | 不属于软件工程 105 / 属于软件工程 11 / 跨域但软工主导 7 | 🟢 优先跟进 (22) / 🟡 保留观察 (2) / ⏳ 待补信息 (99) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (8) / 3.3.1 面向软工问题的形式化验证 (4) | [venue](venues/scp_journal_b.md) | [metadata](metadata/scp_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `SoSyM` | Software and Systems Modeling | `B` | `期刊` | 60 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 35 / 跨域/待判定 25 | 属于软件工程 35 / 不属于软件工程 25 | 🟢 优先跟进 (16) / 🟡 保留观察 (7) / ⏳ 待补信息 (37) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (22) / 6.3.1 实验、案例研究与调查 (2) | [venue](venues/sosym_journal_b.md) | [metadata](metadata/sosym_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `STVR` | Software Testing, Verification and Reliability | `B` | `期刊` | 24 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x | 软件工程 22 / 跨域/待判定 2 | 属于软件工程 22 / 不属于软件工程 2 | 🟢 优先跟进 (11) / 🟡 保留观察 (13) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.4 场景化测试 (5) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (4) | [venue](venues/stvr_journal_b.md) | [metadata](metadata/stvr_journal_b.json) | 计数一致；2018 与先验一致 |
| `SPE` | Software: Practice and Experience | `B` | `期刊` | 107 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.3.x / 4.3.x / 4.4.x / 6.3.x / 8.2.x | 跨域/待判定 70 / 软件工程 17 / 系统软件 15 / 程序设计语言与形式化基础 5 | 不属于软件工程 90 / 属于软件工程 12 / 跨域但软工主导 5 | 🟢 优先跟进 (36) / 🟡 保留观察 (45) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (25) | 3.1.4 场景化测试 (3) / 6.3.1 实验、案例研究与调查 (2) | [venue](venues/spe_journal_b.md) | [metadata](metadata/spe_journal_b.json) | 计数一致；2018 比先验更偏非软工 |
| `PASTE` | ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | `C` | `会议` | 0 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 3.2.x / 3.4.x / 4.2.x | 无 2018 条目 | 无 2018 条目 | 无 2018 条目 | 无纳入软工主路径 | [venue](venues/paste_conf_c.md) | [metadata](metadata/paste_conf_c.json) | 计数一致；2018 无条目，暂以先验为准 |
| `APSEC` | Asia-Pacific Software Engineering Conference | `C` | `会议` | 95 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 82 / 跨域/待判定 13 | 属于软件工程 82 / 不属于软件工程 13 | 🟢 优先跟进 (40) / 🟡 保留观察 (52) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 1.1.1 需求获取与发现 (9) / 7.1.1 代码生成、补全与变换 (8) | [venue](venues/apsec_conf_c.md) | [metadata](metadata/apsec_conf_c.json) | 计数一致；2018 与先验一致 |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | `C` | `会议` | 26 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 23 / 跨域/待判定 3 | 属于软件工程 23 / 不属于软件工程 3 | 🟢 优先跟进 (3) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5) | 6.3.1 实验、案例研究与调查 (8) / 4.1.1 缺陷修复与维护性修正 (3) | [venue](venues/ease_conf_c.md) | [metadata](metadata/ease_conf_c.json) | 计数一致；2018 与先验一致 |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | `C` | `会议` | 29 | 部分属于软工 | B 🟢 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.3.x | 跨域/待判定 19 / 软件工程 5 / 系统软件 3 / 程序设计语言与形式化基础 2 | 不属于软件工程 24 / 属于软件工程 5 | 🟢 优先跟进 (11) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 1.3.1 建模语言与元模型 (2) / 4.1.2 重构、重模块化与代码清理 (1) | [venue](venues/iceccs_conf_c.md) | [metadata](metadata/iceccs_conf_c.json) | 计数一致；2018 比先验更偏非软工 |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | `C` | `会议` | 47 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 软件工程 47 | 属于软件工程 47 | 🟢 优先跟进 (20) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 3.1.4 场景化测试 (8) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) | [venue](venues/icst_conf_c.md) | [metadata](metadata/icst_conf_c.json) | 计数一致；2018 与先验一致 |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | `C` | `会议` | 27 | 大部分属于软工 | B 🟢 | 软件工程 | 3.2.x / 4.2.x / 4.1.x / 3.4.x | 软件工程 18 / 跨域/待判定 5 / 程序设计语言与形式化基础 3 / 系统软件 1 | 属于软件工程 18 / 不属于软件工程 9 | 🟢 优先跟进 (3) / 🟡 保留观察 (22) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 4.1.1 缺陷修复与维护性修正 (3) / 4.1.2 重构、重模块化与代码清理 (2) | [venue](venues/scam_conf_c.md) | [metadata](metadata/scam_conf_c.json) | 计数一致；2018 比先验更偏非软工 |
| `COMPSAC` | International Computer Software and Applications Conference | `C` | `会议` | 326 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 251 / 系统软件 42 / 软件工程 29 / 程序设计语言与形式化基础 4 | 不属于软件工程 297 / 属于软件工程 23 / 跨域但软工主导 6 | 🟢 优先跟进 (58) / 🟡 保留观察 (155) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (110) | 3.1.4 场景化测试 (3) / 3.2.1 静态分析与抽象解释 (2) | [venue](venues/compsac_conf_c.md) | [metadata](metadata/compsac_conf_c.json) | 计数一致；2018 比先验更偏非软工 |
| `ICFEM` | International Conference on Formal Engineering Methods | `C` | `会议` | 37 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 28 / 软件工程 9 | 不属于软件工程 28 / 属于软件工程 6 / 跨域但软工主导 3 | 🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0) | 1.3.3 模型分析、仿真与验证 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) | [venue](venues/icfem_conf_c.md) | [metadata](metadata/icfem_conf_c.json) | 计数一致；2018 比先验更偏非软工 |
| `SSE` | IEEE International Conference on Software Services Engineering | `C` | `会议` | 46 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 31 / 软件工程 8 / 系统软件 5 / 程序设计语言与形式化基础 2 | 不属于软件工程 38 / 属于软件工程 8 | 🟢 优先跟进 (18) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 2.1.4 云/服务/平台架构 (4) / 6.2.1 估算、计划与排程 (1) | [venue](venues/sse_conf_c.md) | [metadata](metadata/sse_conf_c.json) | 计数一致；2018 比先验更偏非软工 |
| `ICSSP` | International Conference on Software and System Process | `C` | `会议` | 21 | 完全属于软工 | C 🟡 | 软件工程 | 6.1.x / 6.2.x / 6.5.x | 软件工程 19 / 跨域/待判定 2 | 属于软件工程 19 / 不属于软件工程 2 | 🟢 优先跟进 (6) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 6.1.1 敏捷、精益与 DevOps 方法 (8) / 2.3.3 组件、包与集成工程 (2) | [venue](venues/icssp_conf_c.md) | [metadata](metadata/icssp_conf_c.json) | 计数一致；2018 与先验一致 |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | `C` | `会议` | 134 | 部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 跨域/待判定 89 / 软件工程 39 / 系统软件 5 / 程序设计语言与形式化基础 1 | 不属于软件工程 95 / 属于软件工程 25 / 跨域但软工主导 14 | 🟢 优先跟进 (36) / 🟡 保留观察 (78) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (15) | 6.1.1 敏捷、精益与 DevOps 方法 (7) / 3.2.3 面向质量属性的分析 (5) | [venue](venues/seke_conf_c.md) | [metadata](metadata/seke_conf_c.json) | 计数一致；2018 与先验一致 |
| `QRS` | International Conference on Software Quality, Reliability and Security | `C` | `会议` | 50 | 完全属于软工 | A 🔥 | 软件工程 | 3.x.x / 5.1.x / 5.2.x / 4.4.x | 软件工程 50 | 属于软件工程 50 | 🟢 优先跟进 (21) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 3.2.3 面向质量属性的分析 (11) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (5) | [venue](venues/qrs_conf_c.md) | [metadata](metadata/qrs_conf_c.json) | 计数一致；2018 与先验一致 |
| `ICSR` | International Conference on Software Reuse | `C` | `会议` | 11 | 完全属于软工 | C 🟡 | 软件工程 | 1.4.x / 2.3.x / 4.1.x / 4.3.x | 跨域/待判定 7 / 软件工程 4 | 不属于软件工程 7 / 属于软件工程 4 | 🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0) | 1.4.1 特征建模与配置 (2) / 1.3.1 建模语言与元模型 (1) | [venue](venues/icsr_conf_c.md) | [metadata](metadata/icsr_conf_c.json) | 计数一致；2018 比先验更偏非软工 |
| `SPIN` | International Symposium on Model Checking of Software | `C` | `会议` | 19 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x | 程序设计语言与形式化基础 11 / 软件工程 8 | 不属于软件工程 11 / 属于软件工程 6 / 跨域但软工主导 2 | 🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0) | 1.3.3 模型分析、仿真与验证 (4) / 1.3.4 基于模型的生成、测试与运行时支持 (1) | [venue](venues/spin_conf_c.md) | [metadata](metadata/spin_conf_c.json) | 计数一致；2018 与先验一致 |
| `TASE` | Theoretical Aspects of Software Engineering Conference | `C` | `会议` | 20 | 部分属于软工 | B 🟢 | 形式化方法与软件工程交叉 | 1.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 20 | 不属于软件工程 20 | 🟢 优先跟进 (8) / 🟡 保留观察 (9) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 无纳入软工主路径 | [venue](venues/tase_conf_c.md) | [metadata](metadata/tase_conf_c.json) | 计数一致；2018 比先验更偏非软工 |
| `MSR` | Mining Software Repositories | `C` | `会议` | 78 | 完全属于软工 | B 🟢 | 软件工程 | 6.4.x / 6.3.x / 4.1.x / 6.5.x | 软件工程 76 / 跨域/待判定 1 / 程序设计语言与形式化基础 1 | 属于软件工程 76 / 不属于软件工程 2 | 🟢 优先跟进 (11) / 🟡 保留观察 (64) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 6.3.4 replication、benchmark 与开放科学 (23) / 4.1.1 缺陷修复与维护性修正 (9) | [venue](venues/msr_conf_c.md) | [metadata](metadata/msr_conf_c.json) | 计数一致；2018 与先验一致 |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | `C` | `会议` | 23 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 18 / 跨域/待判定 5 | 属于软件工程 18 / 不属于软件工程 5 | 🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (13) / 6.3.1 实验、案例研究与调查 (2) | [venue](venues/refsq_conf_c.md) | [metadata](metadata/refsq_conf_c.json) | 计数一致；2018 与先验一致 |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | `C` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 2.1.x / 2.2.x / 4.1.x | 无 2018 条目 | 无 2018 条目 | 无 2018 条目 | 无纳入软工主路径 | [venue](venues/wicsa_conf_c.md) | [metadata](metadata/wicsa_conf_c.json) | 计数一致；2018 无条目，暂以先验为准 |
| `Internetware` | Asia-Pacific Symposium on Internetware | `C` | `会议` | 20 | 大部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.x | 软件工程 17 / 跨域/待判定 3 | 属于软件工程 17 / 不属于软件工程 3 | 🟢 优先跟进 (1) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 2.1.4 云/服务/平台架构 (9) / 3.1.4 场景化测试 (2) | [venue](venues/internetware_conf_c.md) | [metadata](metadata/internetware_conf_c.json) | 计数一致；2018 与先验一致 |
| `RV` | International Conference on Runtime Verification | `C` | `会议` | 28 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.3.2 / 4.4.4 / 5.1.x | 程序设计语言与形式化基础 18 / 软件工程 10 | 不属于软件工程 18 / 跨域但软工主导 9 / 属于软件工程 1 | 🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0) | 3.3.2 运行时验证与运行时监测 (10) | [venue](venues/rv_conf_c.md) | [metadata](metadata/rv_conf_c.json) | 计数一致；2018 与先验一致 |
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | `C` | `期刊` | 81 | 大部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 软件工程 55 / 跨域/待判定 26 | 属于软件工程 55 / 不属于软件工程 26 | 🟢 优先跟进 (22) / 🟡 保留观察 (43) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (11) | 7.1.1 代码生成、补全与变换 (12) / 3.1.4 场景化测试 (6) | [venue](venues/ijseke_journal_c.md) | [metadata](metadata/ijseke_journal_c.json) | 计数一致；2018 比先验更偏非软工 |
| `STTT` | International Journal of Software Tools for Technology Transfer | `C` | `期刊` | 40 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 21 / 软件工程 18 / 系统软件 1 | 不属于软件工程 22 / 属于软件工程 13 / 跨域但软工主导 5 | 🟢 优先跟进 (23) / 🟡 保留观察 (1) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (1) | 3.3.1 面向软工问题的形式化验证 (10) / 3.2.1 静态分析与抽象解释 (4) | [venue](venues/sttt_journal_c.md) | [metadata](metadata/sttt_journal_c.json) | 计数一致；2018 与先验一致 |
| `SOCA` | Service Oriented Computing and Applications | `C` | `期刊` | 27 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 8.2.3 | 跨域/待判定 22 / 软件工程 4 / 系统软件 1 | 不属于软件工程 23 / 属于软件工程 2 / 跨域但软工主导 2 | 🟢 优先跟进 (0) / 🟡 保留观察 (3) / ⏳ 待补信息 (24) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (3) / 5.1.2 容错、韧性与恢复能力 (1) | [venue](venues/soca_journal_c.md) | [metadata](metadata/soca_journal_c.json) | 计数一致；2018 比先验更偏非软工 |
| `SQJ` | Software Quality Journal | `C` | `期刊` | 57 | 完全属于软工 | B 🟢 | 软件工程 | 5.x.x / 3.x.x / 6.3.x | 软件工程 40 / 跨域/待判定 17 | 属于软件工程 40 / 不属于软件工程 17 | 🟢 优先跟进 (9) / 🟡 保留观察 (8) / ⏳ 待补信息 (40) / ⚪ 暂不跟进 (0) | 3.1.1 测试生成与增强 (13) / 6.3.1 实验、案例研究与调查 (6) | [venue](venues/sqj_journal_c.md) | [metadata](metadata/sqj_journal_c.json) | 计数一致；2018 与先验一致 |

## 6. Venue 导航

---

### `PLDI`

- 基本信息：
- 全称：ACM SIGPLAN Conference on Programming Language Design and Implementation
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2018`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：程序分析 / 软件验证 / repair 邻近但需严格筛选
- 初筛分布：无 2018 条目
- 论文名录页：[venues/pldi_conf_a.md](./venues/pldi_conf_a.md)
- 数据文件：[metadata](metadata/pldi_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-pldi_conf_a)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/pldi/
- 正式发布载体页：https://dl.acm.org/journal/pacmpl
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/pldi_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `FSE`

- 基本信息：
- 全称：ACM International Conference on the Foundations of Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2018`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE + `LLM/需求建模/测试验证/修复` 主线
- 初筛分布：无 2018 条目
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
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `OOPSLA`

- 基本信息：
- 全称：Conference on Object-Oriented Programming Systems, Languages, and Applications
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2018`
- 条目数：`60`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件结构 / 程序分析 / 重构与验证偶发贴题
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/oopsla_conf_a.md](./venues/oopsla_conf_a.md)
- 数据文件：[metadata](metadata/oopsla_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-oopsla_conf_a)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/oopsla/
- 正式发布载体页：https://dl.acm.org/journal/pacmpl
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/oopsla_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (47) / 系统软件 (7) / 软件工程 (6)
- 软工纳入判定分布：不属于软件工程 (54) / 属于软件工程 (4) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (60)
- 人工复核状态分布：未人工复核 (60)
- 高频软工主路径：2.2.1 设计原则、模式与反模式 (1) / 4.1.2 重构、重模块化与代码清理 (1) / 5.1.2 容错、韧性与恢复能力 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.2.3 面向质量属性的分析 (1) / 3.1.1 测试生成与增强 (1)
- 主题标签补充：程序设计语言/编译 (23) / 形式化方法 (23) / 测试与验证 (20) / 建模/模型驱动 (16) / 可靠性/安全 (10)

---

### `ASE / 会议 / A`

- 基本信息：
- 全称：International Conference on Automated Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2018`
- 条目数：`112`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (38) / 🟡 保留观察 (70) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/ase_conf_a.md](./venues/ase_conf_a.md)
- 数据文件：[metadata](metadata/ase_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ase-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/kbse/
- 官方论文集页：https://doi.org/10.1145/3238147
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ase_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (108) / 跨域/待判定 (3) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (108) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (38) / 🟡 保留观察 (70) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (112)
- 人工复核状态分布：未人工复核 (112)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (27) / 3.2.1 静态分析与抽象解释 (9) / 3.1.4 场景化测试 (7) / 3.1.1 测试生成与增强 (6) / 3.2.3 面向质量属性的分析 (5) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (5) / 3.3.1 面向软工问题的形式化验证 (4) / 4.1.1 缺陷修复与维护性修正 (4)
- 主题标签补充：测试与验证 (48) / 经验软件工程 (40) / 维护与演化 (33) / 可靠性/安全 (26) / 建模/模型驱动 (25)

---

### `ICSE`

- 基本信息：
- 全称：International Conference on Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2018`
- 条目数：`153`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主会，需求-建模-验证-修复全链可见
- 初筛分布：🟢 优先跟进 (49) / 🟡 保留观察 (94) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10)
- 论文名录页：[venues/icse_conf_a.md](./venues/icse_conf_a.md)
- 数据文件：[metadata](metadata/icse_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icse_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icse-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icse/
- 官方论文集页：https://doi.org/10.1145/3180155 / https://ieeexplore.ieee.org/xpl/conhome/8452039/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icse_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (149) / 跨域/待判定 (3) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (149) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (49) / 🟡 保留观察 (94) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10)
- 判定来源分布：启发式初判 (153)
- 人工复核状态分布：未人工复核 (153)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (26) / 6.3.1 实验、案例研究与调查 (15) / 3.1.4 场景化测试 (11) / 6.3.4 replication、benchmark 与开放科学 (10) / 3.2.4 分析驱动的理解、重构与综合 (7) / 4.1.2 重构、重模块化与代码清理 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (5) / 3.4.2 缺陷定位、补丁生成与程序修复 (5)
- 主题标签补充：经验软件工程 (60) / 测试与验证 (54) / 可靠性/安全 (42) / 维护与演化 (35) / 建模/模型驱动 (30)

---

### `ISSTA`

- 基本信息：
- 全称：International Symposium on Software Testing and Analysis
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2018`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试分析 / 形式化验证 / 缺陷定位与修复主场
- 初筛分布：无 2018 条目
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
- 年份：`2018`
- 条目数：`46`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：形式化方法 / timed automata / 工业与控制系统验证邻近
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (36) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/fm_conf_a.md](./venues/fm_conf_a.md)
- 数据文件：[metadata](metadata/fm_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-fm_conf_a)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/fm/
- 官方论文集页：https://doi.org/10.1007/978-3-319-95582-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/fm_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (38) / 软件工程 (7) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (39) / 属于软件工程 (4) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (36) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (46)
- 人工复核状态分布：未人工复核 (46)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (2) / 1.3.3 模型分析、仿真与验证 (2) / 1.2.1 形式化规约与契约 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 3.2.1 静态分析与抽象解释 (1)
- 主题标签补充：待人工细分 (20) / 建模/模型驱动 (12) / 形式化方法 (11) / 测试与验证 (9) / 需求工程 (5)

---

### `TOSEM`

- 基本信息：
- 全称：ACM Transactions on Software Engineering and Methodology
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`25`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件工程方法 / 需求建模 / 测试验证 / `AI for SE`
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/tosem_journal_a.md](./venues/tosem_journal_a.md)
- 数据文件：[metadata](metadata/tosem_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tosem_journal_a)

- 关键信息页面：
- 期刊主页：https://dl.acm.org/journal/tosem
- 学术索引页：http://dblp.uni-trier.de/db/journals/tosem/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tosem_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (23) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (23) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (25)
- 人工复核状态分布：未人工复核 (25)
- 高频软工主路径：1.2.3 规约质量与一致性 (3) / 4.1.2 重构、重模块化与代码清理 (2) / 7.1.1 代码生成、补全与变换 (2) / 6.3.4 replication、benchmark 与开放科学 (2) / 3.4.2 缺陷定位、补丁生成与程序修复 (2) / 1.4.3 变体感知分析、测试与验证 (2) / 6.3.1 实验、案例研究与调查 (1) / 2.2.1 设计原则、模式与反模式 (1)
- 主题标签补充：建模/模型驱动 (11) / 测试与验证 (8) / 经验软件工程 (7) / 程序修复 (5) / 需求工程 (4)

---

### `TSE`

- 基本信息：
- 全称：IEEE Transactions on Software Engineering
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`61`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主刊 / 建模验证修复与 `LLM` 子题持续出现
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/tse_journal_a.md](./venues/tse_journal_a.md)
- 数据文件：[metadata](metadata/tse_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tse_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32
- 学术索引页：http://dblp.uni-trier.de/db/journals/tse/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tse_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (58) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (58) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (61)
- 人工复核状态分布：未人工复核 (61)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (7) / 4.1.2 重构、重模块化与代码清理 (6) / 6.3.1 实验、案例研究与调查 (5) / 7.1.4 AI 支持的架构、设计与工程决策 (4) / 6.4.3 度量、预测与风险模型 (3) / 4.2.4 克隆、相似性与理解支持 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 6.3.4 replication、benchmark 与开放科学 (3)
- 主题标签补充：经验软件工程 (27) / 测试与验证 (21) / 维护与演化 (17) / 建模/模型驱动 (14) / 可靠性/安全 (14)

---

### `TSC`

- 基本信息：
- 全称：IEEE Transactions on Services Computing
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`77`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务工作流 / 平台 orchestration 邻近，可补性质工程
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (32) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18)
- 论文名录页：[venues/tsc_journal_a.md](./venues/tsc_journal_a.md)
- 数据文件：[metadata](metadata/tsc_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tsc_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=4629386
- 学术索引页：http://dblp.uni-trier.de/db/journals/tsc/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tsc_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (56) / 软件工程 (11) / 系统软件 (10)
- 软工纳入判定分布：不属于软件工程 (66) / 属于软件工程 (8) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (32) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18)
- 判定来源分布：启发式初判 (77)
- 人工复核状态分布：未人工复核 (77)
- 高频软工主路径：2.1.4 云/服务/平台架构 (5) / 3.3.3 assurance、认证与合规验证 (1) / 1.1.1 需求获取与发现 (1) / 5.3.4 扩展性、吞吐与时延保证 (1) / 3.1.1 测试生成与增强 (1) / 5.3.1 性能建模、基准与调优 (1) / 6.2.1 估算、计划与排程 (1)
- 主题标签补充：系统软件 (32) / 建模/模型驱动 (32) / 需求工程 (25) / 形式化方法 (15) / 维护与演化 (12)

---

### `ECOOP`

- 基本信息：
- 全称：European Conference on Object-Oriented Programming
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`27`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`OO` 程序结构 / 分析与重构邻近
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/ecoop_conf_b.md](./venues/ecoop_conf_b.md)
- 数据文件：[metadata](metadata/ecoop_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ecoop_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ecoop/
- 官方论文集页：http://www.dagstuhl.de/dagpub/978-3-95977-079-8
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ecoop_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (22) / 系统软件 (3) / 软件工程 (2)
- 软工纳入判定分布：不属于软件工程 (25) / 跨域但软工主导 (1) / 属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：3.1.1 测试生成与增强 (1) / 3.1.2 回归测试与测试选择 (1)
- 主题标签补充：形式化方法 (13) / 程序设计语言/编译 (12) / 测试与验证 (6) / 程序分析 (5) / 建模/模型驱动 (5)

---

### `ICPC`

- 基本信息：
- 全称：IEEE International Conference on Program Comprehension
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`48`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序理解 / 缺陷分析 / 修复解释与人因辅助
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (40) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/icpc_conf_b.md](./venues/icpc_conf_b.md)
- 数据文件：[metadata](metadata/icpc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icpc_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/iwpc/
- 官方论文集页：https://doi.org/10.1145/3196321 / https://ieeexplore.ieee.org/xpl/conhome/8961319/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icpc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (46) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (46) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (40) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (48)
- 人工复核状态分布：未人工复核 (48)
- 高频软工主路径：6.5.1 开发者认知、生产力与福祉 (14) / 4.2.4 克隆、相似性与理解支持 (6) / 4.1.1 缺陷修复与维护性修正 (4) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 6.3.4 replication、benchmark 与开放科学 (3) / 3.2.1 静态分析与抽象解释 (2) / 4.1.2 重构、重模块化与代码清理 (2) / 4.1.5 技术债、克隆与可维护性治理 (1)
- 主题标签补充：经验软件工程 (22) / 维护与演化 (17) / 可靠性/安全 (11) / 建模/模型驱动 (10) / 测试与验证 (8)

---

### `RE / 会议 / B`

- 基本信息：
- 全称：IEEE International Requirements Engineering Conference
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`70`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (66) / 🟡 保留观察 (4) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/re_conf_b.md](./venues/re_conf_b.md)
- 数据文件：[metadata](metadata/re_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/re/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8490808/proceeding / https://www.computer.org/csdl/proceedings/re/2018/7418/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/re_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (70)
- 软工纳入判定分布：属于软件工程 (70)
- 初筛分布：🟢 优先跟进 (66) / 🟡 保留观察 (4) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (70)
- 人工复核状态分布：未人工复核 (70)
- 高频软工主路径：1.1.1 需求获取与发现 (26) / 6.3.1 实验、案例研究与调查 (6) / 6.1.1 敏捷、精益与 DevOps 方法 (5) / 6.3.4 replication、benchmark 与开放科学 (5) / 3.2.3 面向质量属性的分析 (4) / 1.1.2 需求分析、协商与优先级 (4) / 1.1.4 需求追踪、变更与演化 (3) / 4.2.1 代码搜索、导航与摘要 (2)
- 主题标签补充：需求工程 (67) / 建模/模型驱动 (27) / 测试与验证 (15) / 维护与演化 (13) / 可靠性/安全 (12)

---

### `CAiSE`

- 基本信息：
- 全称：International Conference on Advanced Information Systems Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`37`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：信息系统与过程/模型工程，适合补需求-建模-规约链
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (34) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/caise_conf_b.md](./venues/caise_conf_b.md)
- 数据文件：[metadata](metadata/caise_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-caise_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/caise/
- 官方论文集页：https://doi.org/10.1007/978-3-319-91563-0 / https://www.wikidata.org/entity/Q124317305
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/caise_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (32) / 软件工程 (5)
- 软工纳入判定分布：不属于软件工程 (32) / 属于软件工程 (3) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (34) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (37)
- 人工复核状态分布：未人工复核 (37)
- 高频软工主路径：1.3.1 建模语言与元模型 (3) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 1.1.4 需求追踪、变更与演化 (1)
- 主题标签补充：待人工细分 (26) / 建模/模型驱动 (6) / 维护与演化 (2) / 经验软件工程 (1) / 测试与验证 (1)

---

### `MoDELS`

- 基本信息：
- 全称：ACM/IEEE International Conference on Model Driven Engineering Languages and Systems
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`45`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：模型驱动 / 状态机-SysML / 形式化建模主场
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (24) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/models_conf_b.md](./venues/models_conf_b.md)
- 数据文件：[metadata](metadata/models_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-models_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/models/
- 官方论文集页：https://doi.org/10.1145/3239372
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/models_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (39) / 跨域/待判定 (6)
- 软工纳入判定分布：属于软件工程 (39) / 不属于软件工程 (6)
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (24) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (45)
- 人工复核状态分布：未人工复核 (45)
- 高频软工主路径：1.3.1 建模语言与元模型 (13) / 1.3.2 模型转换、同步与协同 (10) / 6.3.1 实验、案例研究与调查 (3) / 3.3.3 assurance、认证与合规验证 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 4.1.2 重构、重模块化与代码清理 (2) / 3.3.2 运行时验证与运行时监测 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：建模/模型驱动 (40) / 形式化方法 (14) / 测试与验证 (13) / 维护与演化 (9) / 需求工程 (6)

---

### `ICSOC`

- 基本信息：
- 全称：International Conference on Service Oriented Computing
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`63`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务组合 / 流程 / 性质与治理偶有贴题
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (0) / ⏳ 待补信息 (61) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsoc_conf_b.md](./venues/icsoc_conf_b.md)
- 数据文件：[metadata](metadata/icsoc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsoc_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsoc/
- 官方论文集页：https://doi.org/10.1007/978-3-030-03596-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsoc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (54) / 软件工程 (7) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (56) / 属于软件工程 (6) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (0) / ⏳ 待补信息 (61) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (63)
- 人工复核状态分布：未人工复核 (63)
- 高频软工主路径：2.1.4 云/服务/平台架构 (3) / 6.2.1 估算、计划与排程 (1) / 3.1.4 场景化测试 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：待人工细分 (41) / 系统软件 (12) / 建模/模型驱动 (10) / 测试与验证 (4) / 程序设计语言/编译 (3)

---

### `SANER`

- 基本信息：
- 全称：IEEE International Conference on Software Analysis, Evolution, and Reengineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：代码分析 / 逆向 / 演化与 reengineering
- 初筛分布：无 2018 条目
- 论文名录页：[venues/saner_conf_b.md](./venues/saner_conf_b.md)
- 数据文件：[metadata](metadata/saner_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-saner_conf_b)

- 关键信息页面：
- 年主页：待补
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
- 年份：`2018`
- 条目数：`86`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：维护演化 / 修复 / 回归验证 / 工程闭环邻近
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (64) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/icsme_conf_b.md](./venues/icsme_conf_b.md)
- 数据文件：[metadata](metadata/icsme_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsme_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsm/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8528818/proceeding / https://www.computer.org/csdl/proceedings/icsme/2018/7870/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsme_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (86)
- 软工纳入判定分布：属于软件工程 (86)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (64) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (86)
- 人工复核状态分布：未人工复核 (86)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (12) / 6.4.1 代码、提交、issue 与 PR 挖掘 (6) / 3.1.4 场景化测试 (5) / 1.1.4 需求追踪、变更与演化 (5) / 4.2.1 代码搜索、导航与摘要 (4) / 4.1.5 技术债、克隆与可维护性治理 (4) / 3.4.2 缺陷定位、补丁生成与程序修复 (3) / 6.3.4 replication、benchmark 与开放科学 (3)
- 主题标签补充：维护与演化 (42) / 经验软件工程 (42) / 测试与验证 (25) / 可靠性/安全 (23) / 建模/模型驱动 (11)

---

### `VMCAI`

- 基本信息：
- 全称：International Conference on Verification, Model Checking, and Abstract Interpretation
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`24`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：程序验证 / 模型检查 / 抽象解释直接支撑验证框架
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/vmcai_conf_b.md](./venues/vmcai_conf_b.md)
- 数据文件：[metadata](metadata/vmcai_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-vmcai_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/vmcai/
- 官方论文集页：https://doi.org/10.1007/978-3-319-73721-8
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/vmcai_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (20) / 软件工程 (4)
- 软工纳入判定分布：不属于软件工程 (20) / 属于软件工程 (3) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (24)
- 人工复核状态分布：未人工复核 (24)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (3) / 3.2.1 静态分析与抽象解释 (1)
- 主题标签补充：待人工细分 (12) / 测试与验证 (6) / 形式化方法 (6) / 建模/模型驱动 (5)

---

### `ICWS`

- 基本信息：
- 全称：IEEE International Conference on Web Services
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`59`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：Web services / orchestration / 性质验证偶有贴题
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (38) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (15)
- 论文名录页：[venues/icws_conf_b.md](./venues/icws_conf_b.md)
- 数据文件：[metadata](metadata/icws_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icws_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icws/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8454867/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icws_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (48) / 系统软件 (6) / 软件工程 (5)
- 软工纳入判定分布：不属于软件工程 (54) / 属于软件工程 (4) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (38) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (15)
- 判定来源分布：启发式初判 (59)
- 人工复核状态分布：未人工复核 (59)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (1) / 3.3.1 面向软工问题的形式化验证 (1) / 2.1.3 架构演化与重构 (1) / 2.1.4 云/服务/平台架构 (1) / 8.2.3 服务系统与 API 生态 (1)
- 主题标签补充：建模/模型驱动 (27) / 系统软件 (16) / 待人工细分 (11) / 维护与演化 (10) / 测试与验证 (7)

---

### `ESEM`

- 基本信息：
- 全称：International Symposium on Empirical Software Engineering and Measurement
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`58`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证方法 / 评测设计 / `LLM-SE` 实验口径重要
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/esem_conf_b.md](./venues/esem_conf_b.md)
- 数据文件：[metadata](metadata/esem_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-esem_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/esem/
- 官方论文集页：https://doi.org/10.1145/3239235
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/esem_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (55) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (55) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (42) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 判定来源分布：启发式初判 (58)
- 人工复核状态分布：未人工复核 (58)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (16) / 4.1.1 缺陷修复与维护性修正 (14) / 6.1.1 敏捷、精益与 DevOps 方法 (3) / 6.4.1 代码、提交、issue 与 PR 挖掘 (3) / 6.5.1 开发者认知、生产力与福祉 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (1)
- 主题标签补充：经验软件工程 (24) / 维护与演化 (17) / 测试与验证 (16) / 建模/模型驱动 (16) / 可靠性/安全 (16)

---

### `ISSRE`

- 基本信息：
- 全称：IEEE International Symposium on Software Reliability Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2018`
- 条目数：`23`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：可靠性 / assurance / 安全关键验证与缺陷检测很近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/issre_conf_b.md](./venues/issre_conf_b.md)
- 数据文件：[metadata](metadata/issre_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-issre_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/issre/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8536838/proceeding / https://www.computer.org/csdl/proceedings/issre/2018/8321/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/issre_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (22) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (22) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (23)
- 人工复核状态分布：未人工复核 (23)
- 高频软工主路径：3.1.4 场景化测试 (4) / 3.1.2 回归测试与测试选择 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 3.3.3 assurance、认证与合规验证 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 3.1.1 测试生成与增强 (2) / 3.2.1 静态分析与抽象解释 (2) / 5.2.2 隐私工程与数据治理 (1)
- 主题标签补充：测试与验证 (13) / 可靠性/安全 (12) / 维护与演化 (7) / 程序修复 (5) / 建模/模型驱动 (4)

---

### `ASE / 期刊 / B`

- 基本信息：
- 全称：Automated Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`26`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (1) / ⏳ 待补信息 (21) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ase_journal_b.md](./venues/ase_journal_b.md)
- 数据文件：[metadata](metadata/ase_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10515
- 学术索引页：http://dblp.uni-trier.de/db/journals/ase/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ase_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (15) / 跨域/待判定 (10) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (15) / 不属于软件工程 (11)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (1) / ⏳ 待补信息 (21) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (26)
- 人工复核状态分布：未人工复核 (26)
- 高频软工主路径：1.1.4 需求追踪、变更与演化 (2) / 3.2.4 分析驱动的理解、重构与综合 (2) / 1.3.3 模型分析、仿真与验证 (1) / 6.5.3 开源社区、多样性与治理 (1) / 4.1.1 缺陷修复与维护性修正 (1) / 3.3.2 运行时验证与运行时监测 (1) / 4.1.2 重构、重模块化与代码清理 (1) / 1.1.1 需求获取与发现 (1)
- 主题标签补充：待人工细分 (14) / 测试与验证 (3) / 经验软件工程 (3) / 形式化方法 (3) / 维护与演化 (2)

---

### `ESE`

- 基本信息：
- 全称：Empirical Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`105`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证研究 / 数据集 / benchmark / 人因与评测设计
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (10) / ⏳ 待补信息 (75) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/ese_journal_b.md](./venues/ese_journal_b.md)
- 数据文件：[metadata](metadata/ese_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ese_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10664
- 学术索引页：http://dblp.uni-trier.de/db/journals/ese/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ese_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (73) / 跨域/待判定 (31) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (73) / 不属于软件工程 (32)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (10) / ⏳ 待补信息 (75) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (105)
- 人工复核状态分布：未人工复核 (105)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (27) / 6.3.1 实验、案例研究与调查 (13) / 3.2.4 分析驱动的理解、重构与综合 (4) / 6.3.4 replication、benchmark 与开放科学 (3) / 6.4.1 代码、提交、issue 与 PR 挖掘 (2) / 1.2.3 规约质量与一致性 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (2) / 6.1.2 过程挖掘、符合性与改进 (1)
- 主题标签补充：待人工细分 (39) / 经验软件工程 (33) / 维护与演化 (19) / 程序修复 (10) / 可靠性/安全 (10)

---

### `IETS`

- 基本信息：
- 全称：IET Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`56`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：broad SE 期刊，可筛少量建模/验证论文
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (34) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/iets_journal_b.md](./venues/iets_journal_b.md)
- 数据文件：[metadata](metadata/iets_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iets_journal_b)

- 关键信息页面：
- 期刊主页：https://ietresearch.onlinelibrary.wiley.com/journal/1751880x
- 学术索引页：https://dblp.uni-trier.de/db/journals/iet-sen
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/iets_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (33) / 跨域/待判定 (21) / 系统软件 (2)
- 软工纳入判定分布：属于软件工程 (33) / 不属于软件工程 (23)
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (34) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (6)
- 判定来源分布：启发式初判 (56)
- 人工复核状态分布：未人工复核 (56)
- 高频软工主路径：1.1.1 需求获取与发现 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 1.3.1 建模语言与元模型 (3) / 3.1.4 场景化测试 (3) / 3.2.3 面向质量属性的分析 (3) / 7.1.1 代码生成、补全与变换 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (1)
- 主题标签补充：测试与验证 (27) / 建模/模型驱动 (14) / 可靠性/安全 (12) / 经验软件工程 (10) / 维护与演化 (10)

---

### `IST`

- 基本信息：
- 全称：Information and Software Technology
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`172`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 建模测试 / `AI4SE` 论文较常见
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (7) / ⏳ 待补信息 (146) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ist_journal_b.md](./venues/ist_journal_b.md)
- 数据文件：[metadata](metadata/ist_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ist_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/information-and-software-technology
- 学术索引页：http://dblp.uni-trier.de/db/journals/infsof/index.html
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ist_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (88) / 软件工程 (84)
- 软工纳入判定分布：不属于软件工程 (88) / 属于软件工程 (84)
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (7) / ⏳ 待补信息 (146) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (172)
- 人工复核状态分布：未人工复核 (172)
- 高频软工主路径：1.1.1 需求获取与发现 (13) / 7.1.1 代码生成、补全与变换 (9) / 6.1.1 敏捷、精益与 DevOps 方法 (8) / 4.1.2 重构、重模块化与代码清理 (7) / 6.3.1 实验、案例研究与调查 (6) / 6.3.3 系统综述、mapping 与 meta-analysis (4) / 6.2.1 估算、计划与排程 (3) / 1.3.1 建模语言与元模型 (3)
- 主题标签补充：待人工细分 (68) / 建模/模型驱动 (27) / 测试与验证 (26) / 经验软件工程 (19) / 维护与演化 (18)

---

### `JSEP`

- 基本信息：
- 全称：Journal of Software: Evolution and Process
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`87`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：演化 / 过程 / 迭代闭环与工程实践邻近
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (55) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/jsep_journal_b.md](./venues/jsep_journal_b.md)
- 数据文件：[metadata](metadata/jsep_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jsep_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/20477481
- 学术索引页：http://dblp.uni-trier.de/db/journals/smr/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jsep_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (82) / 跨域/待判定 (4) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (82) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (55) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (87)
- 人工复核状态分布：未人工复核 (87)
- 高频软工主路径：6.1.1 敏捷、精益与 DevOps 方法 (10) / 6.3.1 实验、案例研究与调查 (10) / 4.1.1 缺陷修复与维护性修正 (8) / 7.1.4 AI 支持的架构、设计与工程决策 (5) / 4.2.4 克隆、相似性与理解支持 (3) / 3.2.3 面向质量属性的分析 (3) / 6.3.3 系统综述、mapping 与 meta-analysis (3) / 3.1.4 场景化测试 (3)
- 主题标签补充：建模/模型驱动 (34) / 维护与演化 (29) / 经验软件工程 (25) / 测试与验证 (19) / 形式化方法 (18)

---

### `JSS`

- 基本信息：
- 全称：Journal of Systems and Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`216`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：系统与软件工程综合刊，常见建模/验证/CPS 个案
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (8) / ⏳ 待补信息 (185) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/jss_journal_b.md](./venues/jss_journal_b.md)
- 数据文件：[metadata](metadata/jss_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jss_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/journal-of-systems-and-software
- 学术索引页：http://dblp.uni-trier.de/db/journals/jss/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jss_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (113) / 软件工程 (100) / 系统软件 (3)
- 软工纳入判定分布：不属于软件工程 (116) / 属于软件工程 (100)
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (8) / ⏳ 待补信息 (185) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (216)
- 人工复核状态分布：未人工复核 (216)
- 高频软工主路径：2.1.1 架构描述与恢复 (25) / 6.3.1 实验、案例研究与调查 (7) / 3.2.3 面向质量属性的分析 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (5) / 6.1.1 敏捷、精益与 DevOps 方法 (5) / 3.1.4 场景化测试 (5) / 1.1.4 需求追踪、变更与演化 (4) / 4.1.5 技术债、克隆与可维护性治理 (3)
- 主题标签补充：待人工细分 (88) / 建模/模型驱动 (38) / 测试与验证 (31) / 可靠性/安全 (26) / 系统软件 (19)

---

### `RE / 期刊 / B`

- 基本信息：
- 全称：Requirements Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`23`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/re_journal_b.md](./venues/re_journal_b.md)
- 数据文件：[metadata](metadata/re_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/766
- 学术索引页：http://dblp.uni-trier.de/db/journals/re/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/re_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (19) / 跨域/待判定 (4)
- 软工纳入判定分布：属于软件工程 (19) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (23)
- 人工复核状态分布：未人工复核 (23)
- 高频软工主路径：1.1.1 需求获取与发现 (11) / 1.1.2 需求分析、协商与优先级 (2) / 6.3.1 实验、案例研究与调查 (2) / 3.1.4 场景化测试 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 5.2.4 公平性、问责与法规符合 (1) / 6.1.3 治理、合规与过程追踪 (1)
- 主题标签补充：需求工程 (17) / 待人工细分 (5) / 建模/模型驱动 (5) / 经验软件工程 (3) / 测试与验证 (3)

---

### `SCP`

- 基本信息：
- 全称：Science of Computer Programming
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`123`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件程序与形式化/验证/程序分析交叉，贴题概率中高
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (2) / ⏳ 待补信息 (99) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/scp_journal_b.md](./venues/scp_journal_b.md)
- 数据文件：[metadata](metadata/scp_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scp_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/science-of-computer-programming
- 学术索引页：http://dblp.uni-trier.de/db/journals/scp/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/scp_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (104) / 软件工程 (18) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (105) / 属于软件工程 (11) / 跨域但软工主导 (7)
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (2) / ⏳ 待补信息 (99) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (123)
- 人工复核状态分布：未人工复核 (123)
- 高频软工主路径：1.2.1 形式化规约与契约 (8) / 3.3.1 面向软工问题的形式化验证 (4) / 3.2.1 静态分析与抽象解释 (2) / 3.2.3 面向质量属性的分析 (1) / 3.2.4 分析驱动的理解、重构与综合 (1) / 1.3.3 模型分析、仿真与验证 (1) / 4.1.5 技术债、克隆与可维护性治理 (1)
- 主题标签补充：待人工细分 (62) / 形式化方法 (27) / 建模/模型驱动 (20) / 测试与验证 (12) / 需求工程 (11)

---

### `SoSyM`

- 基本信息：
- 全称：Software and Systems Modeling
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`60`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件与系统建模 / DSL / 状态机与模型分析主场
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (7) / ⏳ 待补信息 (37) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sosym_journal_b.md](./venues/sosym_journal_b.md)
- 数据文件：[metadata](metadata/sosym_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sosym_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10270
- 学术索引页：http://dblp.uni-trier.de/db/journals/sosym/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sosym_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (35) / 跨域/待判定 (25)
- 软工纳入判定分布：属于软件工程 (35) / 不属于软件工程 (25)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (7) / ⏳ 待补信息 (37) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (60)
- 人工复核状态分布：未人工复核 (60)
- 高频软工主路径：1.3.1 建模语言与元模型 (22) / 6.3.1 实验、案例研究与调查 (2) / 6.1.2 过程挖掘、符合性与改进 (2) / 1.1.4 需求追踪、变更与演化 (1) / 3.2.4 分析驱动的理解、重构与综合 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 3.3.3 assurance、认证与合规验证 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：建模/模型驱动 (41) / 测试与验证 (11) / 待人工细分 (10) / 形式化方法 (8) / 需求工程 (7)

---

### `STVR`

- 基本信息：
- 全称：Software Testing, Verification and Reliability
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`24`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 验证 / 可靠性与 formal properties 非常贴题
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (13) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/stvr_journal_b.md](./venues/stvr_journal_b.md)
- 数据文件：[metadata](metadata/stvr_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-stvr_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/10991689
- 学术索引页：http://dblp.uni-trier.de/db/journals/stvr/index.html
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/stvr_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (22) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (22) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (13) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (24)
- 人工复核状态分布：未人工复核 (24)
- 高频软工主路径：3.1.4 场景化测试 (5) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (4) / 3.2.3 面向质量属性的分析 (2) / 3.1.1 测试生成与增强 (2) / 3.3.1 面向软工问题的形式化验证 (2) / 3.3.3 assurance、认证与合规验证 (1) / 3.3.4 基准、工具评测与可复现验证 (1) / 5.1.1 故障预测与失效分析 (1)
- 主题标签补充：测试与验证 (21) / 建模/模型驱动 (8) / 可靠性/安全 (7) / 形式化方法 (7) / 维护与演化 (7)

---

### `SPE`

- 基本信息：
- 全称：Software: Practice and Experience
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`107`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：工程实践 / 系统实现为主，偶有 runtime/verification
- 初筛分布：🟢 优先跟进 (36) / 🟡 保留观察 (45) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (25)
- 论文名录页：[venues/spe_journal_b.md](./venues/spe_journal_b.md)
- 数据文件：[metadata](metadata/spe_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spe_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/1097024x
- 学术索引页：http://dblp.uni-trier.de/db/journals/spe/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/spe_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (70) / 软件工程 (17) / 系统软件 (15) / 程序设计语言与形式化基础 (5)
- 软工纳入判定分布：不属于软件工程 (90) / 属于软件工程 (12) / 跨域但软工主导 (5)
- 初筛分布：🟢 优先跟进 (36) / 🟡 保留观察 (45) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (25)
- 判定来源分布：启发式初判 (107)
- 人工复核状态分布：未人工复核 (107)
- 高频软工主路径：3.1.4 场景化测试 (3) / 6.3.1 实验、案例研究与调查 (2) / 5.3.4 扩展性、吞吐与时延保证 (1) / 5.3.1 性能建模、基准与调优 (1) / 1.3.1 建模语言与元模型 (1) / 1.1.4 需求追踪、变更与演化 (1) / 2.2.2 模块化、依赖与解耦 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：建模/模型驱动 (39) / 系统软件 (37) / 需求工程 (27) / 维护与演化 (20) / 测试与验证 (18)

---

### `PASTE`

- 基本信息：
- 全称：ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近
- 初筛分布：无 2018 条目
- 论文名录页：[venues/paste_conf_c.md](./venues/paste_conf_c.md)
- 数据文件：[metadata](metadata/paste_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-paste_conf_c)

- 关键信息页面：
- 年主页：待补
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
- 年份：`2018`
- 条目数：`95`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 亚洲社区，`LLM-SE/测试/建模` 可见
- 初筛分布：🟢 优先跟进 (40) / 🟡 保留观察 (52) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/apsec_conf_c.md](./venues/apsec_conf_c.md)
- 数据文件：[metadata](metadata/apsec_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-apsec_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/apsec/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8716285/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/apsec_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (82) / 跨域/待判定 (13)
- 软工纳入判定分布：属于软件工程 (82) / 不属于软件工程 (13)
- 初筛分布：🟢 优先跟进 (40) / 🟡 保留观察 (52) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (95)
- 人工复核状态分布：未人工复核 (95)
- 高频软工主路径：1.1.1 需求获取与发现 (9) / 7.1.1 代码生成、补全与变换 (8) / 7.1.4 AI 支持的架构、设计与工程决策 (8) / 6.3.1 实验、案例研究与调查 (6) / 3.1.4 场景化测试 (4) / 3.1.2 回归测试与测试选择 (3) / 6.3.4 replication、benchmark 与开放科学 (3) / 6.4.1 代码、提交、issue 与 PR 挖掘 (3)
- 主题标签补充：建模/模型驱动 (32) / 测试与验证 (30) / 经验软件工程 (29) / 需求工程 (24) / 维护与演化 (23)

---

### `EASE`

- 基本信息：
- 全称：International Conference on Evaluation and Assessment in Software Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`26`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：评测与实验设计 / benchmark / replication 有用
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/ease_conf_c.md](./venues/ease_conf_c.md)
- 数据文件：[metadata](metadata/ease_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ease_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ease/
- 官方论文集页：http://dl.acm.org/citation.cfm?id=3210459
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ease_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (23) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (23) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (26)
- 人工复核状态分布：未人工复核 (26)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (8) / 4.1.1 缺陷修复与维护性修正 (3) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 3.2.3 面向质量属性的分析 (2) / 6.4.1 代码、提交、issue 与 PR 挖掘 (1) / 6.2.1 估算、计划与排程 (1) / 2.2.1 设计原则、模式与反模式 (1) / 6.4.3 度量、预测与风险模型 (1)
- 主题标签补充：经验软件工程 (11) / 测试与验证 (7) / 待人工细分 (5) / 可靠性/安全 (5) / 维护与演化 (4)

---

### `ICECCS`

- 基本信息：
- 全称：International Conference on Engineering of Complex Computer Systems
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`29`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：复杂系统建模与验证 / safety-critical / CPS 邻近
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/iceccs_conf_c.md](./venues/iceccs_conf_c.md)
- 数据文件：[metadata](metadata/iceccs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iceccs_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/iceccs/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8592780/proceeding / https://www.computer.org/csdl/proceedings/iceccs/2018/9341/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/iceccs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (19) / 软件工程 (5) / 系统软件 (3) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：不属于软件工程 (24) / 属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (29)
- 人工复核状态分布：未人工复核 (29)
- 高频软工主路径：1.3.1 建模语言与元模型 (2) / 4.1.2 重构、重模块化与代码清理 (1) / 1.1.4 需求追踪、变更与演化 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：建模/模型驱动 (14) / 形式化方法 (11) / 测试与验证 (9) / 需求工程 (7) / 维护与演化 (6)

---

### `ICST`

- 基本信息：
- 全称：IEEE International Conference on Software Testing, Verification and Validation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`47`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 形式化验证 / 缺陷检测与修复直接相关
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/icst_conf_c.md](./venues/icst_conf_c.md)
- 数据文件：[metadata](metadata/icst_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icst_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icst/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8365877/proceeding / https://www.computer.org/csdl/proceedings/icst/2018/5012/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icst_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (47)
- 软工纳入判定分布：属于软件工程 (47)
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (47)
- 人工复核状态分布：未人工复核 (47)
- 高频软工主路径：3.1.4 场景化测试 (8) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 3.1.1 测试生成与增强 (5) / 3.4.2 缺陷定位、补丁生成与程序修复 (3) / 1.2.1 形式化规约与契约 (2) / 3.2.3 面向质量属性的分析 (2) / 3.2.4 分析驱动的理解、重构与综合 (2) / 3.3.1 面向软工问题的形式化验证 (2)
- 主题标签补充：测试与验证 (38) / 可靠性/安全 (17) / 经验软件工程 (11) / 建模/模型驱动 (10) / 形式化方法 (9)

---

### `SCAM`

- 基本信息：
- 全称：IEEE International Working Conference on Source Code Analysis and Manipulation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`27`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：源码分析与变换 / 缺陷修复 / 程序理解邻近
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (22) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/scam_conf_c.md](./venues/scam_conf_c.md)
- 数据文件：[metadata](metadata/scam_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scam_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/scam/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8528960/proceeding / https://www.computer.org/csdl/proceedings/scam/2018/8290/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/scam_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (18) / 跨域/待判定 (5) / 程序设计语言与形式化基础 (3) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (18) / 不属于软件工程 (9)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (22) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (3) / 4.1.2 重构、重模块化与代码清理 (2) / 3.2.1 静态分析与抽象解释 (2) / 3.2.3 面向质量属性的分析 (2) / 6.4.1 代码、提交、issue 与 PR 挖掘 (1) / 1.3.1 建模语言与元模型 (1) / 4.2.4 克隆、相似性与理解支持 (1) / 4.1.5 技术债、克隆与可维护性治理 (1)
- 主题标签补充：经验软件工程 (10) / 维护与演化 (10) / 程序设计语言/编译 (9) / 建模/模型驱动 (7) / 测试与验证 (6)

---

### `COMPSAC`

- 基本信息：
- 全称：International Computer Software and Applications Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`326`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：覆盖过宽，需按建模/验证/`AI4SE` 子题筛选
- 初筛分布：🟢 优先跟进 (58) / 🟡 保留观察 (155) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (110)
- 论文名录页：[venues/compsac_conf_c.md](./venues/compsac_conf_c.md)
- 数据文件：[metadata](metadata/compsac_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-compsac_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/compsac/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8377622 / https://www.computer.org/csdl/proceedings/compsac/2018/2666/01/index.html / https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8377622
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/compsac_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (251) / 系统软件 (42) / 软件工程 (29) / 程序设计语言与形式化基础 (4)
- 软工纳入判定分布：不属于软件工程 (297) / 属于软件工程 (23) / 跨域但软工主导 (6)
- 初筛分布：🟢 优先跟进 (58) / 🟡 保留观察 (155) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (110)
- 判定来源分布：启发式初判 (326)
- 人工复核状态分布：未人工复核 (326)
- 高频软工主路径：3.1.4 场景化测试 (3) / 3.2.1 静态分析与抽象解释 (2) / 2.1.1 架构描述与恢复 (2) / 2.3.3 组件、包与集成工程 (2) / 6.3.1 实验、案例研究与调查 (2) / 3.3.1 面向软工问题的形式化验证 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 3.1.2 回归测试与测试选择 (2)
- 主题标签补充：建模/模型驱动 (101) / 待人工细分 (99) / 测试与验证 (61) / 可靠性/安全 (57) / 形式化方法 (43)

---

### `ICFEM`

- 基本信息：
- 全称：International Conference on Formal Engineering Methods
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`37`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：formal engineering / 规约建模 / 验证与证明
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icfem_conf_c.md](./venues/icfem_conf_c.md)
- 数据文件：[metadata](metadata/icfem_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icfem_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icfem/
- 官方论文集页：https://doi.org/10.1007/978-3-030-02450-5
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icfem_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (28) / 软件工程 (9)
- 软工纳入判定分布：不属于软件工程 (28) / 属于软件工程 (6) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (37)
- 人工复核状态分布：未人工复核 (37)
- 高频软工主路径：1.3.3 模型分析、仿真与验证 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 1.2.1 形式化规约与契约 (1) / 1.3.1 建模语言与元模型 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 6.3.1 实验、案例研究与调查 (1)
- 主题标签补充：形式化方法 (14) / 建模/模型驱动 (11) / 测试与验证 (10) / 待人工细分 (9) / 可靠性/安全 (3)

---

### `SSE`

- 基本信息：
- 全称：IEEE International Conference on Software Services Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`46`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件服务工程混合
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/sse_conf_c.md](./venues/sse_conf_c.md)
- 数据文件：[metadata](metadata/sse_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sse_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/IEEEscc/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/sse_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (31) / 软件工程 (8) / 系统软件 (5) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：不属于软件工程 (38) / 属于软件工程 (8)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (46)
- 人工复核状态分布：未人工复核 (46)
- 高频软工主路径：2.1.4 云/服务/平台架构 (4) / 6.2.1 估算、计划与排程 (1) / 5.1.2 容错、韧性与恢复能力 (1) / 5.2.3 供应链安全与可追溯信任 (1) / 1.1.2 需求分析、协商与优先级 (1)
- 主题标签补充：建模/模型驱动 (25) / 需求工程 (15) / 系统软件 (14) / 维护与演化 (13) / 形式化方法 (9)

---

### `ICSSP`

- 基本信息：
- 全称：International Conference on Software and System Process
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`21`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件过程 / 团队与流程，对主问题较间接
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/icssp_conf_c.md](./venues/icssp_conf_c.md)
- 数据文件：[metadata](metadata/icssp_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icssp_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ispw/
- 官方论文集页：https://doi.org/10.1145/3202710
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icssp_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (19) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (19) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (21)
- 人工复核状态分布：未人工复核 (21)
- 高频软工主路径：6.1.1 敏捷、精益与 DevOps 方法 (8) / 2.3.3 组件、包与集成工程 (2) / 6.1.2 过程挖掘、符合性与改进 (2) / 7.1.1 代码生成、补全与变换 (2) / 6.5.4 教育、培训与入门支持 (1) / 6.2.1 估算、计划与排程 (1) / 6.5.1 开发者认知、生产力与福祉 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1)
- 主题标签补充：建模/模型驱动 (10) / 测试与验证 (6) / 经验软件工程 (6) / 维护与演化 (4) / 需求工程 (4)

---

### `SEKE`

- 基本信息：
- 全称：International Conference on Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`134`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 偶有贴题
- 初筛分布：🟢 优先跟进 (36) / 🟡 保留观察 (78) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (15)
- 论文名录页：[venues/seke_conf_c.md](./venues/seke_conf_c.md)
- 数据文件：[metadata](metadata/seke_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-seke_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/seke/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/seke_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (89) / 软件工程 (39) / 系统软件 (5) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (95) / 属于软件工程 (25) / 跨域但软工主导 (14)
- 初筛分布：🟢 优先跟进 (36) / 🟡 保留观察 (78) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (15)
- 判定来源分布：启发式初判 (134)
- 人工复核状态分布：未人工复核 (134)
- 高频软工主路径：6.1.1 敏捷、精益与 DevOps 方法 (7) / 3.2.3 面向质量属性的分析 (5) / 4.1.5 技术债、克隆与可维护性治理 (4) / 1.3.1 建模语言与元模型 (2) / 4.1.1 缺陷修复与维护性修正 (2) / 6.3.1 实验、案例研究与调查 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 2.3.3 组件、包与集成工程 (2)
- 主题标签补充：建模/模型驱动 (60) / 测试与验证 (34) / 维护与演化 (31) / 形式化方法 (27) / 可靠性/安全 (26)

---

### `QRS`

- 基本信息：
- 全称：International Conference on Software Quality, Reliability and Security
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`50`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：质量 / 可靠性 / 安全 / assurance 与验证链很近
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/qrs_conf_c.md](./venues/qrs_conf_c.md)
- 数据文件：[metadata](metadata/qrs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-qrs_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.uni-trier.de/db/conf/qrs
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8424855/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/qrs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (50)
- 软工纳入判定分布：属于软件工程 (50)
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (50)
- 人工复核状态分布：未人工复核 (50)
- 高频软工主路径：3.2.3 面向质量属性的分析 (11) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (5) / 3.1.1 测试生成与增强 (4) / 3.3.1 面向软工问题的形式化验证 (3) / 6.3.1 实验、案例研究与调查 (3) / 1.1.4 需求追踪、变更与演化 (2) / 3.2.1 静态分析与抽象解释 (2) / 3.1.4 场景化测试 (2)
- 主题标签补充：测试与验证 (24) / 可靠性/安全 (17) / 建模/模型驱动 (16) / 形式化方法 (15) / 维护与演化 (13)

---

### `ICSR`

- 基本信息：
- 全称：International Conference on Software Reuse
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`11`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：复用 / 组件资产，可补模型资产与可复用工件
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsr_conf_c.md](./venues/icsr_conf_c.md)
- 数据文件：[metadata](metadata/icsr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsr_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsr/
- 官方论文集页：https://doi.org/10.1007/978-3-319-90421-4
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (7) / 软件工程 (4)
- 软工纳入判定分布：不属于软件工程 (7) / 属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (11)
- 人工复核状态分布：未人工复核 (11)
- 高频软工主路径：1.4.1 特征建模与配置 (2) / 1.3.1 建模语言与元模型 (1) / 4.1.1 缺陷修复与维护性修正 (1)
- 主题标签补充：待人工细分 (7) / 建模/模型驱动 (2) / 经验软件工程 (1) / 维护与演化 (1) / 需求工程 (1)

---

### `SPIN`

- 基本信息：
- 全称：International Symposium on Model Checking of Software
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`19`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件模型检查 / state-based verification / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/spin_conf_c.md](./venues/spin_conf_c.md)
- 数据文件：[metadata](metadata/spin_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spin_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/spin/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-319-94111-0
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/spin_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (11) / 软件工程 (8)
- 软工纳入判定分布：不属于软件工程 (11) / 属于软件工程 (6) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (12) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (19)
- 人工复核状态分布：未人工复核 (19)
- 高频软工主路径：1.3.3 模型分析、仿真与验证 (4) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 1.2.1 形式化规约与契约 (1) / 3.3.2 运行时验证与运行时监测 (1) / 1.3.2 模型转换、同步与协同 (1)
- 主题标签补充：待人工细分 (8) / 建模/模型驱动 (8) / 形式化方法 (5) / 测试与验证 (4) / 运行时监测 (1)

---

### `TASE`

- 基本信息：
- 全称：Theoretical Aspects of Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`20`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件工程名下的 formal verification / assurance 邻近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (9) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/tase_conf_c.md](./venues/tase_conf_c.md)
- 数据文件：[metadata](metadata/tase_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tase_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/tase/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/8558619/proceeding / https://www.computer.org/csdl/proceedings/tase/2018/7305/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/tase_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (20)
- 软工纳入判定分布：不属于软件工程 (20)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (9) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (20)
- 人工复核状态分布：未人工复核 (20)
- 主题标签补充：形式化方法 (11) / 建模/模型驱动 (9) / 程序设计语言/编译 (7) / 测试与验证 (7) / 待人工细分 (3)

---

### `MSR`

- 基本信息：
- 全称：Mining Software Repositories
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`78`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：仓库挖掘 / benchmark / `LLM-SE` 证据与数据建设有用
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (64) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/msr_conf_c.md](./venues/msr_conf_c.md)
- 数据文件：[metadata](metadata/msr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-msr_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/msr/
- 官方论文集页：https://doi.org/10.1145/3196398 / https://ieeexplore.ieee.org/xpl/conhome/8593335/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/msr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (76) / 跨域/待判定 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (76) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (64) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (78)
- 人工复核状态分布：未人工复核 (78)
- 高频软工主路径：6.3.4 replication、benchmark 与开放科学 (23) / 4.1.1 缺陷修复与维护性修正 (9) / 6.3.1 实验、案例研究与调查 (7) / 2.3.2 构建工具链与开发环境 (6) / 3.1.4 场景化测试 (4) / 6.4.1 代码、提交、issue 与 PR 挖掘 (4) / 1.1.4 需求追踪、变更与演化 (2) / 2.2.4 技术债与设计质量 (2)
- 主题标签补充：经验软件工程 (46) / 维护与演化 (34) / 可靠性/安全 (19) / 测试与验证 (15) / 建模/模型驱动 (11)

---

### `REFSQ`

- 基本信息：
- 全称：Requirements Engineering: Foundation for Software Quality
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`23`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求质量 / 需求规约 / 需求到性质非常贴题
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/refsq_conf_c.md](./venues/refsq_conf_c.md)
- 数据文件：[metadata](metadata/refsq_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-refsq_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/refsq/
- 官方论文集页：https://doi.org/10.1007/978-3-319-77243-1
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/refsq_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (18) / 跨域/待判定 (5)
- 软工纳入判定分布：属于软件工程 (18) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (23)
- 人工复核状态分布：未人工复核 (23)
- 高频软工主路径：1.1.1 需求获取与发现 (13) / 6.3.1 实验、案例研究与调查 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (2) / 1.1.2 需求分析、协商与优先级 (1)
- 主题标签补充：需求工程 (16) / 待人工细分 (6) / 建模/模型驱动 (3) / 经验软件工程 (2) / 测试与验证 (1)

---

### `WICSA`

- 基本信息：
- 全称：Working IEEE/IFIP Conference on Software Architecture
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件架构 / 设计决策 / 模型结构与演化有用
- 初筛分布：无 2018 条目
- 论文名录页：[venues/wicsa_conf_c.md](./venues/wicsa_conf_c.md)
- 数据文件：[metadata](metadata/wicsa_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-wicsa_conf_c)

- 关键信息页面：
- 年主页：待补
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
- 年份：`2018`
- 条目数：`20`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：平台 / 网络化软件 / 运行治理邻近
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/internetware_conf_c.md](./venues/internetware_conf_c.md)
- 数据文件：[metadata](metadata/internetware_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-internetware_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.org/db/conf/internetware/index.html
- 官方论文集页：https://doi.org/10.1145/3275219
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/internetware_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (17) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (17) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (20)
- 人工复核状态分布：未人工复核 (20)
- 高频软工主路径：2.1.4 云/服务/平台架构 (9) / 3.1.4 场景化测试 (2) / 6.2.1 估算、计划与排程 (1) / 4.1.1 缺陷修复与维护性修正 (1) / 8.2.1 Web 与移动应用工程 (1) / 4.2.1 代码搜索、导航与摘要 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1) / 5.3.1 性能建模、基准与调优 (1)
- 主题标签补充：建模/模型驱动 (9) / 经验软件工程 (9) / 测试与验证 (5) / 可靠性/安全 (4) / 系统软件 (3)

---

### `RV`

- 基本信息：
- 全称：International Conference on Runtime Verification
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2018`
- 条目数：`28`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：运行时验证 / 监测 / 时序性质 / 工具链直接邻近
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/rv_conf_c.md](./venues/rv_conf_c.md)
- 数据文件：[metadata](metadata/rv_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-rv_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.org/db/conf/rv/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-030-03769-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/rv_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (18) / 软件工程 (10)
- 软工纳入判定分布：不属于软件工程 (18) / 跨域但软工主导 (9) / 属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (28)
- 人工复核状态分布：未人工复核 (28)
- 高频软工主路径：3.3.2 运行时验证与运行时监测 (10)
- 主题标签补充：运行时监测 (15) / 待人工细分 (10) / 测试与验证 (10) / 形式化方法 (3) / 需求工程 (1)

---

### `IJSEKE`

- 基本信息：
- 全称：International Journal of Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`81`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 可补链但不稳定
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (43) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (11)
- 论文名录页：[venues/ijseke_journal_c.md](./venues/ijseke_journal_c.md)
- 数据文件：[metadata](metadata/ijseke_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ijseke_journal_c)

- 关键信息页面：
- 期刊主页：https://www.worldscientific.com/worldscinet/ijseke
- 学术索引页：http://dblp.uni-trier.de/db/journals/ijseke/index.html
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ijseke_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (55) / 跨域/待判定 (26)
- 软工纳入判定分布：属于软件工程 (55) / 不属于软件工程 (26)
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (43) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (11)
- 判定来源分布：启发式初判 (81)
- 人工复核状态分布：未人工复核 (81)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (12) / 3.1.4 场景化测试 (6) / 3.2.3 面向质量属性的分析 (5) / 2.1.1 架构描述与恢复 (5) / 1.1.1 需求获取与发现 (2) / 1.3.3 模型分析、仿真与验证 (2) / 2.2.2 模块化、依赖与解耦 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2)
- 主题标签补充：测试与验证 (33) / 建模/模型驱动 (31) / 维护与演化 (20) / 经验软件工程 (16) / 待人工细分 (15)

---

### `STTT`

- 基本信息：
- 全称：International Journal of Software Tools for Technology Transfer
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`40`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：验证工具 / formal methods tool transfer / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (1) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/sttt_journal_c.md](./venues/sttt_journal_c.md)
- 数据文件：[metadata](metadata/sttt_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sttt_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10009
- 学术索引页：http://dblp.uni-trier.de/db/journals/sttt/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sttt_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (21) / 软件工程 (18) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (22) / 属于软件工程 (13) / 跨域但软工主导 (5)
- 初筛分布：🟢 优先跟进 (23) / 🟡 保留观察 (1) / ⏳ 待补信息 (15) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (40)
- 人工复核状态分布：未人工复核 (40)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (10) / 3.2.1 静态分析与抽象解释 (4) / 1.3.1 建模语言与元模型 (2) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：形式化方法 (20) / 建模/模型驱动 (16) / 测试与验证 (13) / 待人工细分 (7) / 需求工程 (6)

---

### `SOCA`

- 基本信息：
- 全称：Service Oriented Computing and Applications
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`27`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务计算与应用为主
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (3) / ⏳ 待补信息 (24) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/soca_journal_c.md](./venues/soca_journal_c.md)
- 数据文件：[metadata](metadata/soca_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-soca_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11761
- 学术索引页：http://dblp.uni-trier.de/db/journals/soca/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/soca_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (22) / 软件工程 (4) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (23) / 属于软件工程 (2) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (3) / ⏳ 待补信息 (24) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：2.1.4 云/服务/平台架构 (3) / 5.1.2 容错、韧性与恢复能力 (1)
- 主题标签补充：待人工细分 (8) / 建模/模型驱动 (7) / 可靠性/安全 (6) / 系统软件 (5) / 测试与验证 (2)

---

### `SQJ`

- 基本信息：
- 全称：Software Quality Journal
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2018`
- 条目数：`57`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：质量 / 度量 / assurance 视角可支撑验证评价
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (8) / ⏳ 待补信息 (40) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sqj_journal_c.md](./venues/sqj_journal_c.md)
- 数据文件：[metadata](metadata/sqj_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sqj_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11219
- 学术索引页：http://dblp.uni-trier.de/db/journals/sqj/
- 2018 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sqj_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (40) / 跨域/待判定 (17)
- 软工纳入判定分布：属于软件工程 (40) / 不属于软件工程 (17)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (8) / ⏳ 待补信息 (40) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (57)
- 人工复核状态分布：未人工复核 (57)
- 高频软工主路径：3.1.1 测试生成与增强 (13) / 6.3.1 实验、案例研究与调查 (6) / 3.1.4 场景化测试 (3) / 3.2.3 面向质量属性的分析 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (2) / 6.3.4 replication、benchmark 与开放科学 (2) / 1.1.1 需求获取与发现 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1)
- 主题标签补充：待人工细分 (23) / 测试与验证 (17) / 建模/模型驱动 (13) / 可靠性/安全 (6) / 维护与演化 (6)

## 7. 本年度总体观察

- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (848) / 🟡 保留观察 (1281) / ⏳ 待补信息 (890) / ⚪ 暂不跟进 (296)
- 一级总判定分布：软件工程 (1780) / 跨域/待判定 (1075) / 程序设计语言与形式化基础 (349) / 系统软件 (111)
- 软工纳入判定分布：属于软件工程 (1713) / 不属于软件工程 (1535) / 跨域但软工主导 (67)
- 判定来源分布：启发式初判 (3315)
- 人工复核状态分布：未人工复核 (3315)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (133) / 7.1.1 代码生成、补全与变换 (101) / 1.1.1 需求获取与发现 (101) / 4.1.1 缺陷修复与维护性修正 (100) / 3.1.4 场景化测试 (90) / 1.3.1 建模语言与元模型 (71) / 3.2.3 面向质量属性的分析 (68) / 6.3.4 replication、benchmark 与开放科学 (67) / 6.1.1 敏捷、精益与 DevOps 方法 (59) / 7.1.4 AI 支持的架构、设计与工程决策 (57) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (51) / 3.1.1 测试生成与增强 (46) / 3.2.1 静态分析与抽象解释 (42) / 2.1.1 架构描述与恢复 (42) / 4.1.2 重构、重模块化与代码清理 (40)
- 计数复核状态：以 [verification.json](./verification.json) 为准；默认要求 `expected_total == actual_total`。
- 分类终判状态：以 `metadata/*.json` 中的 `classification_source / manual_review_status / manual_review_note` 为准。
- 后续若继续扩年份或重跑年度页，建议先运行 `tools/ccf_se_index_builder.py`，再运行 `tools/ccf_se_classifier.py`。
