# `2013` 年度汇总

## 1. 年份说明

- 年份：`2013`
- 覆盖范围：`CCF_SE_A_B_C.md` 当前保留的 `CCF` 软件工程高相关 venue 子集
- 当前覆盖的 venue 数量：`57`
- 当前已入表论文数量：`3130`
- 更新时间：`2026-04-07 10:33`
- 说明：本页先由 `tools/ccf_se_index_builder.py` 生成基础元数据，再由 `tools/ccf_se_classifier.py` 对未终判条目做启发式初判；若 `metadata/*.json` 中已写回人工终判，则直接保留该终判。逐篇论文名录拆分到 `venues/*.md`。

## 2. 年度汇总统计

- A 类会议：`336`
- A 类期刊：`183`
- B 类会议：`639`
- B 类期刊：`831`
- C 类会议：`993`
- C 类期刊：`148`
- 期望总条目数：`3130`
- 实际总条目数：`3130`
- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (811) / 🟡 保留观察 (1038) / ⏳ 待补信息 (1075) / ⚪ 暂不跟进 (206)
- 一级总判定分布：软件工程 (1680) / 跨域/待判定 (1060) / 程序设计语言与形式化基础 (322) / 系统软件 (68)
- 软工纳入判定分布：属于软件工程 (1605) / 不属于软件工程 (1450) / 跨域但软工主导 (75)
- 判定来源分布：启发式初判 (3130)
- 人工复核状态分布：未人工复核 (3130)
- 高频软工主路径：1.1.1 需求获取与发现 (146) / 7.1.1 代码生成、补全与变换 (120) / 6.3.1 实验、案例研究与调查 (120) / 4.1.1 缺陷修复与维护性修正 (93) / 3.1.4 场景化测试 (89) / 7.1.4 AI 支持的架构、设计与工程决策 (68) / 1.3.1 建模语言与元模型 (67) / 3.1.1 测试生成与增强 (56) / 3.2.3 面向质量属性的分析 (42) / 3.2.1 静态分析与抽象解释 (42) / 2.1.1 架构描述与恢复 (39) / 1.3.3 模型分析、仿真与验证 (39)

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
- `主体归属`、`软工归属级别`、`氛围` 与 `典型软工路径（先验）` 来自 venue 级先验；`2013` 逐篇统计直接按本年度 `metadata/*.json` 中的终判字段汇总。
- `典型软工路径（先验）` 与 `2013 高频软工主路径` 使用 [SOFTWARE_ENGINEERING_FIELD_TREE.md](../../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的方向树口径。

| venue | 全称 | 等级 | 类型 | 论文数 | 软工归属级别 | 氛围 | 主体归属 | 典型软工路径（先验） | 当年一级总判定 | 当年软工纳入 | 初筛分布 | 当年高频软工主路径 | 论文名录 | 数据文件 | 备注 |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | `A` | `会议` | 0 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 3.4.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/pldi_conf_a.md) | [metadata](metadata/pldi_conf_a.json) | 计数一致；2013 无条目，暂以先验为准 |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | `A` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/fse_conf_a.md) | [metadata](metadata/fse_conf_a.json) | 计数一致；2013 无条目，暂以先验为准 |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages, and Applications | `A` | `会议` | 0 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 3.4.x / 4.2.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/oopsla_conf_a.md) | [metadata](metadata/oopsla_conf_a.json) | 计数一致；2013 无条目，暂以先验为准 |
| `ASE / 会议 / A` | International Conference on Automated Software Engineering | `A` | `会议` | 94 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 91 / 跨域/待判定 2 / 程序设计语言与形式化基础 1 | 属于软件工程 91 / 不属于软件工程 3 | 🟢 优先跟进 (41) / 🟡 保留观察 (49) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 7.1.1 代码生成、补全与变换 (21) / 1.1.1 需求获取与发现 (6) | [venue](venues/ase_conf_a.md) | [metadata](metadata/ase_conf_a.json) | 计数一致；2013 与先验一致 |
| `ICSE` | International Conference on Software Engineering | `A` | `会议` | 242 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 222 / 跨域/待判定 19 / 程序设计语言与形式化基础 1 | 属于软件工程 222 / 不属于软件工程 20 | 🟢 优先跟进 (68) / 🟡 保留观察 (148) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (25) | 7.1.1 代码生成、补全与变换 (43) / 7.1.4 AI 支持的架构、设计与工程决策 (16) | [venue](venues/icse_conf_a.md) | [metadata](metadata/icse_conf_a.json) | 计数一致；2013 与先验一致 |
| `ISSTA` | International Symposium on Software Testing and Analysis | `A` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/issta_conf_a.md) | [metadata](metadata/issta_conf_a.json) | 计数一致；2013 无条目，暂以先验为准 |
| `FM` | International Symposium on Formal Methods | `A` | `会议` | 0 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/fm_conf_a.md) | [metadata](metadata/fm_conf_a.json) | 计数一致；2013 无条目，暂以先验为准 |
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | `A` | `期刊` | 38 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 35 / 跨域/待判定 3 | 属于软件工程 35 / 不属于软件工程 3 | 🟢 优先跟进 (22) / 🟡 保留观察 (13) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 7.1.1 代码生成、补全与变换 (7) / 1.1.1 需求获取与发现 (4) | [venue](venues/tosem_journal_a.md) | [metadata](metadata/tosem_journal_a.json) | 计数一致；2013 与先验一致 |
| `TSE` | IEEE Transactions on Software Engineering | `A` | `期刊` | 100 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 95 / 跨域/待判定 5 | 属于软件工程 95 / 不属于软件工程 5 | 🟢 优先跟进 (41) / 🟡 保留观察 (56) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 7.1.1 代码生成、补全与变换 (17) / 6.3.1 实验、案例研究与调查 (7) | [venue](venues/tse_journal_a.md) | [metadata](metadata/tse_journal_a.json) | 计数一致；2013 与先验一致 |
| `TSC` | IEEE Transactions on Services Computing | `A` | `期刊` | 45 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 5.3.x / 8.2.x | 跨域/待判定 34 / 软件工程 7 / 系统软件 4 | 不属于软件工程 38 / 属于软件工程 6 / 跨域但软工主导 1 | 🟢 优先跟进 (12) / 🟡 保留观察 (26) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (6) | 2.1.4 云/服务/平台架构 (2) / 6.1.2 过程挖掘、符合性与改进 (2) | [venue](venues/tsc_journal_a.md) | [metadata](metadata/tsc_journal_a.json) | 计数一致；2013 比先验更偏非软工 |
| `ECOOP` | European Conference on Object-Oriented Programming | `B` | `会议` | 29 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 4.2.x | 程序设计语言与形式化基础 24 / 软件工程 4 / 系统软件 1 | 不属于软件工程 25 / 跨域但软工主导 4 | 🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (28) / ⚪ 暂不跟进 (0) | 2.2.1 设计原则、模式与反模式 (1) / 2.2.2 模块化、依赖与解耦 (1) | [venue](venues/ecoop_conf_b.md) | [metadata](metadata/ecoop_conf_b.json) | 计数一致；2013 比先验更偏非软工 |
| `ICPC` | IEEE International Conference on Program Comprehension | `B` | `会议` | 31 | 完全属于软工 | B 🟢 | 软件工程 | 4.2.x / 4.1.x / 6.5.1 | 软件工程 29 / 跨域/待判定 1 / 程序设计语言与形式化基础 1 | 属于软件工程 29 / 不属于软件工程 2 | 🟢 优先跟进 (7) / 🟡 保留观察 (20) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 6.5.1 开发者认知、生产力与福祉 (6) / 4.2.4 克隆、相似性与理解支持 (5) | [venue](venues/icpc_conf_b.md) | [metadata](metadata/icpc_conf_b.json) | 计数一致；2013 与先验一致 |
| `RE / 会议 / B` | IEEE International Requirements Engineering Conference | `B` | `会议` | 67 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x / 6.1.x | 软件工程 65 / 跨域/待判定 2 | 属于软件工程 65 / 不属于软件工程 2 | 🟢 优先跟进 (63) / 🟡 保留观察 (2) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 1.1.1 需求获取与发现 (33) / 1.1.4 需求追踪、变更与演化 (7) | [venue](venues/re_conf_b.md) | [metadata](metadata/re_conf_b.json) | 计数一致；2013 与先验一致 |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | `B` | `会议` | 89 | 部分属于软工 | B 🟢 | 信息系统工程与软件工程交叉 | 1.3.x / 2.1.x / 4.3.x / 8.3.x | 跨域/待判定 75 / 软件工程 13 / 系统软件 1 | 不属于软件工程 76 / 跨域但软工主导 7 / 属于软件工程 6 | 🟢 优先跟进 (12) / 🟡 保留观察 (0) / ⏳ 待补信息 (77) / ⚪ 暂不跟进 (0) | 6.3.1 实验、案例研究与调查 (4) / 1.3.1 建模语言与元模型 (4) | [venue](venues/caise_conf_b.md) | [metadata](metadata/caise_conf_b.json) | 计数一致；2013 比先验更偏非软工 |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | `B` | `会议` | 47 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 29 / 跨域/待判定 18 | 属于软件工程 29 / 不属于软件工程 18 | 🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (39) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (16) / 3.3.3 assurance、认证与合规验证 (2) | [venue](venues/models_conf_b.md) | [metadata](metadata/models_conf_b.json) | 计数一致；2013 比先验更偏非软工 |
| `ICSOC` | International Conference on Service Oriented Computing | `B` | `会议` | 65 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 63 / 软件工程 2 | 不属于软件工程 63 / 属于软件工程 2 | 🟢 优先跟进 (1) / 🟡 保留观察 (2) / ⏳ 待补信息 (62) / ⚪ 暂不跟进 (0) | 6.2.1 估算、计划与排程 (1) / 1.3.1 建模语言与元模型 (1) | [venue](venues/icsoc_conf_b.md) | [metadata](metadata/icsoc_conf_b.json) | 计数一致；2013 比先验更偏非软工 |
| `SANER` | IEEE International Conference on Software Analysis, Evolution, and Reengineering | `B` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 3.2.x / 3.4.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/saner_conf_b.md) | [metadata](metadata/saner_conf_b.json) | 计数一致；2013 无条目，暂以先验为准 |
| `ICSME` | International Conference on Software Maintenance and Evolution | `B` | `会议` | 92 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 4.3.x / 6.4.x | 软件工程 89 / 跨域/待判定 3 | 属于软件工程 89 / 不属于软件工程 3 | 🟢 优先跟进 (10) / 🟡 保留观察 (74) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8) | 4.1.1 缺陷修复与维护性修正 (28) / 4.1.2 重构、重模块化与代码清理 (8) | [venue](venues/icsme_conf_b.md) | [metadata](metadata/icsme_conf_b.json) | 计数一致；2013 与先验一致 |
| `VMCAI` | International Conference on Verification, Model Checking, and Abstract Interpretation | `B` | `会议` | 31 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 28 / 软件工程 2 / 系统软件 1 | 不属于软件工程 29 / 跨域但软工主导 2 | 🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0) | 3.2.1 静态分析与抽象解释 (2) | [venue](venues/vmcai_conf_b.md) | [metadata](metadata/vmcai_conf_b.json) | 计数一致；2013 比先验更偏非软工 |
| `ICWS` | IEEE International Conference on Web Services | `B` | `会议` | 85 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 5.3.x / 8.2.3 | 跨域/待判定 69 / 软件工程 11 / 系统软件 5 | 不属于软件工程 74 / 属于软件工程 9 / 跨域但软工主导 2 | 🟢 优先跟进 (26) / 🟡 保留观察 (48) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (11) | 2.1.4 云/服务/平台架构 (4) / 3.1.4 场景化测试 (3) | [venue](venues/icws_conf_b.md) | [metadata](metadata/icws_conf_b.json) | 计数一致；2013 比先验更偏非软工 |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | `B` | `会议` | 56 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 55 / 跨域/待判定 1 | 属于软件工程 55 / 不属于软件工程 1 | 🟢 优先跟进 (12) / 🟡 保留观察 (36) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8) | 6.3.1 实验、案例研究与调查 (24) / 4.1.1 缺陷修复与维护性修正 (8) | [venue](venues/esem_conf_b.md) | [metadata](metadata/esem_conf_b.json) | 计数一致；2013 与先验一致 |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | `B` | `会议` | 47 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x / 5.2.x / 4.4.x | 软件工程 47 | 属于软件工程 47 | 🟢 优先跟进 (14) / 🟡 保留观察 (32) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 3.3.3 assurance、认证与合规验证 (11) / 3.1.1 测试生成与增强 (6) | [venue](venues/issre_conf_b.md) | [metadata](metadata/issre_conf_b.json) | 计数一致；2013 与先验一致 |
| `ASE / 期刊 / B` | Automated Software Engineering | `B` | `期刊` | 20 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 15 / 跨域/待判定 5 | 属于软件工程 15 / 不属于软件工程 5 | 🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (17) / ⚪ 暂不跟进 (0) | 7.1.1 代码生成、补全与变换 (6) / 1.1.1 需求获取与发现 (2) | [venue](venues/ase_journal_b.md) | [metadata](metadata/ase_journal_b.json) | 计数一致；2013 与先验一致 |
| `ESE` | Empirical Software Engineering | `B` | `期刊` | 37 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 28 / 跨域/待判定 9 | 属于软件工程 28 / 不属于软件工程 9 | 🟢 优先跟进 (4) / 🟡 保留观察 (2) / ⏳ 待补信息 (31) / ⚪ 暂不跟进 (0) | 4.1.1 缺陷修复与维护性修正 (9) / 3.2.3 面向质量属性的分析 (4) | [venue](venues/ese_journal_b.md) | [metadata](metadata/ese_journal_b.json) | 计数一致；2013 与先验一致 |
| `IETS` | IET Software | `B` | `期刊` | 29 | 大部分属于软工 | C 🟡 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 5.x.x | 软件工程 20 / 跨域/待判定 9 | 属于软件工程 20 / 不属于软件工程 9 | 🟢 优先跟进 (10) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 1.3.1 建模语言与元模型 (2) / 1.1.1 需求获取与发现 (2) | [venue](venues/iets_journal_b.md) | [metadata](metadata/iets_journal_b.json) | 计数一致；2013 比先验更偏非软工 |
| `IST` | Information and Software Technology | `B` | `期刊` | 136 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 跨域/待判定 76 / 软件工程 59 / 程序设计语言与形式化基础 1 | 不属于软件工程 77 / 属于软件工程 59 | 🟢 优先跟进 (25) / 🟡 保留观察 (2) / ⏳ 待补信息 (108) / ⚪ 暂不跟进 (1) | 1.1.1 需求获取与发现 (21) / 7.1.1 代码生成、补全与变换 (10) | [venue](venues/ist_journal_b.md) | [metadata](metadata/ist_journal_b.json) | 计数一致；2013 比先验更偏非软工 |
| `JSEP` | Journal of Software: Evolution and Process | `B` | `期刊` | 63 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.3.x / 6.1.x / 6.4.x | 软件工程 61 / 跨域/待判定 2 | 属于软件工程 61 / 不属于软件工程 2 | 🟢 优先跟进 (15) / 🟡 保留观察 (41) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 4.1.1 缺陷修复与维护性修正 (18) / 6.1.2 过程挖掘、符合性与改进 (6) | [venue](venues/jsep_journal_b.md) | [metadata](metadata/jsep_journal_b.json) | 计数一致；2013 与先验一致 |
| `JSS` | Journal of Systems and Software | `B` | `期刊` | 229 | 大部分属于软工 | B 🟢 | 软件工程 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 158 / 软件工程 66 / 系统软件 5 | 不属于软件工程 163 / 属于软件工程 66 | 🟢 优先跟进 (18) / 🟡 保留观察 (1) / ⏳ 待补信息 (209) / ⚪ 暂不跟进 (1) | 2.1.1 架构描述与恢复 (22) / 7.1.4 AI 支持的架构、设计与工程决策 (6) | [venue](venues/jss_journal_b.md) | [metadata](metadata/jss_journal_b.json) | 计数一致；2013 比先验更偏非软工 |
| `RE / 期刊 / B` | Requirements Engineering | `B` | `期刊` | 20 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 18 / 跨域/待判定 2 | 属于软件工程 18 / 不属于软件工程 2 | 🟢 优先跟进 (14) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (8) / 3.2.3 面向质量属性的分析 (4) | [venue](venues/re_journal_b.md) | [metadata](metadata/re_journal_b.json) | 计数一致；2013 与先验一致 |
| `SCP` | Science of Computer Programming | `B` | `期刊` | 140 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 4.1.x | 程序设计语言与形式化基础 112 / 软件工程 24 / 系统软件 4 | 不属于软件工程 116 / 跨域但软工主导 14 / 属于软件工程 10 | 🟢 优先跟进 (11) / 🟡 保留观察 (1) / ⏳ 待补信息 (128) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (11) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) | [venue](venues/scp_journal_b.md) | [metadata](metadata/scp_journal_b.json) | 计数一致；2013 比先验更偏非软工 |
| `SoSyM` | Software and Systems Modeling | `B` | `期刊` | 53 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 跨域/待判定 29 / 软件工程 23 / 系统软件 1 | 不属于软件工程 30 / 属于软件工程 23 | 🟢 优先跟进 (8) / 🟡 保留观察 (3) / ⏳ 待补信息 (42) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (11) / 7.1.4 AI 支持的架构、设计与工程决策 (2) | [venue](venues/sosym_journal_b.md) | [metadata](metadata/sosym_journal_b.json) | 计数一致；2013 比先验更偏非软工 |
| `STVR` | Software Testing, Verification and Reliability | `B` | `期刊` | 30 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x | 软件工程 27 / 跨域/待判定 3 | 属于软件工程 27 / 不属于软件工程 3 | 🟢 优先跟进 (12) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.1 测试生成与增强 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) | [venue](venues/stvr_journal_b.md) | [metadata](metadata/stvr_journal_b.json) | 计数一致；2013 与先验一致 |
| `SPE` | Software: Practice and Experience | `B` | `期刊` | 74 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.3.x / 4.3.x / 4.4.x / 6.3.x / 8.2.x | 跨域/待判定 45 / 系统软件 12 / 软件工程 11 / 程序设计语言与形式化基础 6 | 不属于软件工程 63 / 属于软件工程 9 / 跨域但软工主导 2 | 🟢 优先跟进 (21) / 🟡 保留观察 (41) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (12) | 6.3.1 实验、案例研究与调查 (4) / 2.3.1 代码生成、脚手架与 DSL 工程 (1) | [venue](venues/spe_journal_b.md) | [metadata](metadata/spe_journal_b.json) | 计数一致；2013 比先验更偏非软工 |
| `PASTE` | ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | `C` | `会议` | 7 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 3.2.x / 3.4.x / 4.2.x | 程序设计语言与形式化基础 5 / 系统软件 2 | 不属于软件工程 7 | 🟢 优先跟进 (2) / 🟡 保留观察 (4) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 无纳入软工主路径 | [venue](venues/paste_conf_c.md) | [metadata](metadata/paste_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `APSEC` | Asia-Pacific Software Engineering Conference | `C` | `会议` | 107 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 83 / 跨域/待判定 23 / 程序设计语言与形式化基础 1 | 属于软件工程 83 / 不属于软件工程 24 | 🟢 优先跟进 (45) / 🟡 保留观察 (55) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7) | 1.1.1 需求获取与发现 (6) / 6.3.1 实验、案例研究与调查 (5) | [venue](venues/apsec_conf_c.md) | [metadata](metadata/apsec_conf_c.json) | 计数一致；2013 与先验一致 |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | `C` | `会议` | 31 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 30 / 跨域/待判定 1 | 属于软件工程 30 / 不属于软件工程 1 | 🟢 优先跟进 (5) / 🟡 保留观察 (23) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 6.3.1 实验、案例研究与调查 (11) / 6.3.3 系统综述、mapping 与 meta-analysis (5) | [venue](venues/ease_conf_c.md) | [metadata](metadata/ease_conf_c.json) | 计数一致；2013 与先验一致 |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | `C` | `会议` | 39 | 部分属于软工 | B 🟢 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.3.x | 跨域/待判定 25 / 软件工程 7 / 程序设计语言与形式化基础 4 / 系统软件 3 | 不属于软件工程 32 / 属于软件工程 7 | 🟢 优先跟进 (21) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 1.3.2 模型转换、同步与协同 (1) / 1.1.2 需求分析、协商与优先级 (1) | [venue](venues/iceccs_conf_c.md) | [metadata](metadata/iceccs_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | `C` | `会议` | 71 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 软件工程 71 | 属于软件工程 71 | 🟢 优先跟进 (25) / 🟡 保留观察 (45) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 3.1.1 测试生成与增强 (19) / 3.1.4 场景化测试 (8) | [venue](venues/icst_conf_c.md) | [metadata](metadata/icst_conf_c.json) | 计数一致；2013 与先验一致 |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | `C` | `会议` | 24 | 大部分属于软工 | B 🟢 | 软件工程 | 3.2.x / 4.2.x / 4.1.x / 3.4.x | 软件工程 15 / 跨域/待判定 8 / 程序设计语言与形式化基础 1 | 属于软件工程 15 / 不属于软件工程 9 | 🟢 优先跟进 (2) / 🟡 保留观察 (17) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5) | 3.2.1 静态分析与抽象解释 (7) / 3.4.2 缺陷定位、补丁生成与程序修复 (1) | [venue](venues/scam_conf_c.md) | [metadata](metadata/scam_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `COMPSAC` | International Computer Software and Applications Conference | `C` | `会议` | 140 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 100 / 软件工程 24 / 系统软件 14 / 程序设计语言与形式化基础 2 | 不属于软件工程 116 / 属于软件工程 20 / 跨域但软工主导 4 | 🟢 优先跟进 (43) / 🟡 保留观察 (59) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (38) | 2.1.1 架构描述与恢复 (5) / 1.1.1 需求获取与发现 (4) | [venue](venues/compsac_conf_c.md) | [metadata](metadata/compsac_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `ICFEM` | International Conference on Formal Engineering Methods | `C` | `会议` | 29 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 20 / 软件工程 8 / 系统软件 1 | 不属于软件工程 21 / 属于软件工程 5 / 跨域但软工主导 3 | 🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (3) / 1.3.1 建模语言与元模型 (1) | [venue](venues/icfem_conf_c.md) | [metadata](metadata/icfem_conf_c.json) | 计数一致；2013 与先验一致 |
| `SSE` | IEEE International Conference on Software Services Engineering | `C` | `会议` | 108 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 96 / 系统软件 7 / 软件工程 3 / 程序设计语言与形式化基础 2 | 不属于软件工程 105 / 属于软件工程 3 | 🟢 优先跟进 (31) / 🟡 保留观察 (59) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18) | 2.1.4 云/服务/平台架构 (2) / 4.4.2 事故诊断、回滚与恢复 (1) | [venue](venues/sse_conf_c.md) | [metadata](metadata/sse_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `ICSSP` | International Conference on Software and System Process | `C` | `会议` | 23 | 完全属于软工 | C 🟡 | 软件工程 | 6.1.x / 6.2.x / 6.5.x | 软件工程 20 / 跨域/待判定 3 | 属于软件工程 20 / 不属于软件工程 3 | 🟢 优先跟进 (5) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6) | 6.1.1 敏捷、精益与 DevOps 方法 (7) / 6.2.2 风险、价值与优先级 (3) | [venue](venues/icssp_conf_c.md) | [metadata](metadata/icssp_conf_c.json) | 计数一致；2013 与先验一致 |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | `C` | `会议` | 143 | 部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 跨域/待判定 109 / 软件工程 34 | 不属于软件工程 109 / 属于软件工程 18 / 跨域但软工主导 16 | 🟢 优先跟进 (14) / 🟡 保留观察 (0) / ⏳ 待补信息 (129) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (16) / 1.1.4 需求追踪、变更与演化 (3) | [venue](venues/seke_conf_c.md) | [metadata](metadata/seke_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `QRS` | International Conference on Software Quality, Reliability and Security | `C` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 3.x.x / 5.1.x / 5.2.x / 4.4.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/qrs_conf_c.md) | [metadata](metadata/qrs_conf_c.json) | 计数一致；2013 无条目，暂以先验为准 |
| `ICSR` | International Conference on Software Reuse | `C` | `会议` | 27 | 完全属于软工 | C 🟡 | 软件工程 | 1.4.x / 2.3.x / 4.1.x / 4.3.x | 软件工程 15 / 跨域/待判定 12 | 属于软件工程 15 / 不属于软件工程 12 | 🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (27) / ⚪ 暂不跟进 (0) | 1.4.1 特征建模与配置 (12) / 3.3.3 assurance、认证与合规验证 (1) | [venue](venues/icsr_conf_c.md) | [metadata](metadata/icsr_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `SPIN` | International Symposium on Model Checking of Software | `C` | `会议` | 22 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x | 程序设计语言与形式化基础 18 / 软件工程 4 | 不属于软件工程 18 / 属于软件工程 4 | 🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (14) / ⚪ 暂不跟进 (0) | 1.3.3 模型分析、仿真与验证 (3) / 1.2.1 形式化规约与契约 (1) | [venue](venues/spin_conf_c.md) | [metadata](metadata/spin_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `TASE` | Theoretical Aspects of Software Engineering Conference | `C` | `会议` | 35 | 部分属于软工 | B 🟢 | 形式化方法与软件工程交叉 | 1.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 25 / 软件工程 8 / 系统软件 2 | 不属于软件工程 27 / 属于软件工程 7 / 跨域但软工主导 1 | 🟢 优先跟进 (18) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 3.3.1 面向软工问题的形式化验证 (3) / 5.1.2 容错、韧性与恢复能力 (1) | [venue](venues/tase_conf_c.md) | [metadata](metadata/tase_conf_c.json) | 计数一致；2013 比先验更偏非软工 |
| `MSR` | Mining Software Repositories | `C` | `会议` | 64 | 完全属于软工 | B 🟢 | 软件工程 | 6.4.x / 6.3.x / 4.1.x / 6.5.x | 软件工程 60 / 跨域/待判定 4 | 属于软件工程 60 / 不属于软件工程 4 | 🟢 优先跟进 (7) / 🟡 保留观察 (51) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6) | 6.3.4 replication、benchmark 与开放科学 (16) / 4.1.1 缺陷修复与维护性修正 (13) | [venue](venues/msr_conf_c.md) | [metadata](metadata/msr_conf_c.json) | 计数一致；2013 与先验一致 |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | `C` | `会议` | 28 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 25 / 跨域/待判定 3 | 属于软件工程 25 / 不属于软件工程 3 | 🟢 优先跟进 (21) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (18) / 1.1.4 需求追踪、变更与演化 (3) | [venue](venues/refsq_conf_c.md) | [metadata](metadata/refsq_conf_c.json) | 计数一致；2013 与先验一致 |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | `C` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 2.1.x / 2.2.x / 4.1.x | 无 2013 条目 | 无 2013 条目 | 无 2013 条目 | 无纳入软工主路径 | [venue](venues/wicsa_conf_c.md) | [metadata](metadata/wicsa_conf_c.json) | 计数一致；2013 无条目，暂以先验为准 |
| `Internetware` | Asia-Pacific Symposium on Internetware | `C` | `会议` | 34 | 大部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.x | 软件工程 24 / 跨域/待判定 7 / 系统软件 3 | 属于软件工程 24 / 不属于软件工程 10 | 🟢 优先跟进 (9) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 2.1.4 云/服务/平台架构 (13) / 3.1.4 场景化测试 (2) | [venue](venues/internetware_conf_c.md) | [metadata](metadata/internetware_conf_c.json) | 计数一致；2013 与先验一致 |
| `RV` | International Conference on Runtime Verification | `C` | `会议` | 61 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.3.2 / 4.4.4 / 5.1.x | 程序设计语言与形式化基础 42 / 软件工程 18 / 系统软件 1 | 不属于软件工程 43 / 跨域但软工主导 14 / 属于软件工程 4 | 🟢 优先跟进 (22) / 🟡 保留观察 (1) / ⏳ 待补信息 (38) / ⚪ 暂不跟进 (0) | 3.3.2 运行时验证与运行时监测 (14) / 3.2.2 动态与混合分析 (2) | [venue](venues/rv_conf_c.md) | [metadata](metadata/rv_conf_c.json) | 计数一致；2013 与先验一致 |
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | `C` | `期刊` | 64 | 大部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 软件工程 46 / 跨域/待判定 18 | 属于软件工程 46 / 不属于软件工程 18 | 🟢 优先跟进 (19) / 🟡 保留观察 (31) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (11) | 7.1.1 代码生成、补全与变换 (5) / 1.3.3 模型分析、仿真与验证 (4) | [venue](venues/ijseke_journal_c.md) | [metadata](metadata/ijseke_journal_c.json) | 计数一致；2013 与先验一致 |
| `STTT` | International Journal of Software Tools for Technology Transfer | `C` | `期刊` | 36 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 28 / 软件工程 8 | 不属于软件工程 28 / 属于软件工程 4 / 跨域但软工主导 4 | 🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (20) / ⚪ 暂不跟进 (0) | 3.2.1 静态分析与抽象解释 (3) / 3.3.1 面向软工问题的形式化验证 (2) | [venue](venues/sttt_journal_c.md) | [metadata](metadata/sttt_journal_c.json) | 计数一致；2013 比先验更偏非软工 |
| `SOCA` | Service Oriented Computing and Applications | `C` | `期刊` | 20 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 8.2.3 | 跨域/待判定 15 / 软件工程 4 / 系统软件 1 | 不属于软件工程 16 / 属于软件工程 3 / 跨域但软工主导 1 | 🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0) | 2.1.4 云/服务/平台架构 (2) / 8.2.3 服务系统与 API 生态 (1) | [venue](venues/soca_journal_c.md) | [metadata](metadata/soca_journal_c.json) | 计数一致；2013 比先验更偏非软工 |
| `SQJ` | Software Quality Journal | `C` | `期刊` | 28 | 完全属于软工 | B 🟢 | 软件工程 | 5.x.x / 3.x.x / 6.3.x | 软件工程 25 / 跨域/待判定 3 | 属于软件工程 25 / 不属于软件工程 3 | 🟢 优先跟进 (5) / 🟡 保留观察 (1) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0) | 3.1.1 测试生成与增强 (10) / 6.3.1 实验、案例研究与调查 (3) | [venue](venues/sqj_journal_c.md) | [metadata](metadata/sqj_journal_c.json) | 计数一致；2013 与先验一致 |

## 6. Venue 导航

---

### `PLDI`

- 基本信息：
- 全称：ACM SIGPLAN Conference on Programming Language Design and Implementation
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：程序分析 / 软件验证 / repair 邻近但需严格筛选
- 初筛分布：无 2013 条目
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
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE + `LLM/需求建模/测试验证/修复` 主线
- 初筛分布：无 2013 条目
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
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件结构 / 程序分析 / 重构与验证偶发贴题
- 初筛分布：无 2013 条目
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
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `ASE / 会议 / A`

- 基本信息：
- 全称：International Conference on Automated Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2013`
- 条目数：`94`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (41) / 🟡 保留观察 (49) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/ase_conf_a.md](./venues/ase_conf_a.md)
- 数据文件：[metadata](metadata/ase_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ase-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/kbse/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6684409/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ase_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (91) / 跨域/待判定 (2) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (91) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (41) / 🟡 保留观察 (49) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (94)
- 人工复核状态分布：未人工复核 (94)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (21) / 1.1.1 需求获取与发现 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (6) / 3.1.1 测试生成与增强 (5) / 3.1.4 场景化测试 (5) / 1.3.2 模型转换、同步与协同 (4) / 3.2.3 面向质量属性的分析 (3) / 1.2.3 规约质量与一致性 (3)
- 主题标签补充：测试与验证 (38) / 建模/模型驱动 (32) / 需求工程 (26) / 可靠性/安全 (24) / 经验软件工程 (23)

---

### `ICSE`

- 基本信息：
- 全称：International Conference on Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2013`
- 条目数：`242`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主会，需求-建模-验证-修复全链可见
- 初筛分布：🟢 优先跟进 (68) / 🟡 保留观察 (148) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (25)
- 论文名录页：[venues/icse_conf_a.md](./venues/icse_conf_a.md)
- 数据文件：[metadata](metadata/icse_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icse_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icse-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icse/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6596173/proceeding / https://www.computer.org/csdl/proceedings/icse/2013/3073/00/index.html / http://dl.acm.org/citation.cfm?id=2486788
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icse_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (222) / 跨域/待判定 (19) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (222) / 不属于软件工程 (20)
- 初筛分布：🟢 优先跟进 (68) / 🟡 保留观察 (148) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (25)
- 判定来源分布：启发式初判 (242)
- 人工复核状态分布：未人工复核 (242)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (43) / 7.1.4 AI 支持的架构、设计与工程决策 (16) / 6.3.1 实验、案例研究与调查 (15) / 3.1.4 场景化测试 (14) / 1.1.1 需求获取与发现 (11) / 3.2.1 静态分析与抽象解释 (9) / 2.2.1 设计原则、模式与反模式 (7) / 1.3.3 模型分析、仿真与验证 (7)
- 主题标签补充：维护与演化 (74) / 测试与验证 (73) / 建模/模型驱动 (61) / 经验软件工程 (56) / 可靠性/安全 (47)

---

### `ISSTA`

- 基本信息：
- 全称：International Symposium on Software Testing and Analysis
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试分析 / 形式化验证 / 缺陷定位与修复主场
- 初筛分布：无 2013 条目
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
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：形式化方法 / timed automata / 工业与控制系统验证邻近
- 初筛分布：无 2013 条目
- 论文名录页：[venues/fm_conf_a.md](./venues/fm_conf_a.md)
- 数据文件：[metadata](metadata/fm_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-fm_conf_a)

- 关键信息页面：
- 年主页：待补
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
- 年份：`2013`
- 条目数：`38`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件工程方法 / 需求建模 / 测试验证 / `AI for SE`
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (13) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/tosem_journal_a.md](./venues/tosem_journal_a.md)
- 数据文件：[metadata](metadata/tosem_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tosem_journal_a)

- 关键信息页面：
- 期刊主页：https://dl.acm.org/journal/tosem
- 学术索引页：http://dblp.uni-trier.de/db/journals/tosem/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tosem_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (35) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (35) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (13) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (38)
- 人工复核状态分布：未人工复核 (38)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (7) / 1.1.1 需求获取与发现 (4) / 1.2.3 规约质量与一致性 (3) / 7.1.2 AI 支持的测试、分析与修复 (2) / 3.4.1 调试、分诊与根因分析 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 3.1.4 场景化测试 (1)
- 主题标签补充：测试与验证 (14) / 可靠性/安全 (13) / 形式化方法 (13) / 需求工程 (12) / 建模/模型驱动 (11)

---

### `TSE`

- 基本信息：
- 全称：IEEE Transactions on Software Engineering
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`100`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主刊 / 建模验证修复与 `LLM` 子题持续出现
- 初筛分布：🟢 优先跟进 (41) / 🟡 保留观察 (56) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/tse_journal_a.md](./venues/tse_journal_a.md)
- 数据文件：[metadata](metadata/tse_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tse_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32
- 学术索引页：http://dblp.uni-trier.de/db/journals/tse/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tse_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (95) / 跨域/待判定 (5)
- 软工纳入判定分布：属于软件工程 (95) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (41) / 🟡 保留观察 (56) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (100)
- 人工复核状态分布：未人工复核 (100)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (17) / 6.3.1 实验、案例研究与调查 (7) / 7.1.4 AI 支持的架构、设计与工程决策 (7) / 1.1.1 需求获取与发现 (7) / 1.3.3 模型分析、仿真与验证 (5) / 6.2.1 估算、计划与排程 (5) / 1.2.1 形式化规约与契约 (5) / 3.1.4 场景化测试 (4)
- 主题标签补充：测试与验证 (44) / 建模/模型驱动 (41) / 需求工程 (33) / 经验软件工程 (25) / 维护与演化 (24)

---

### `TSC`

- 基本信息：
- 全称：IEEE Transactions on Services Computing
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`45`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务工作流 / 平台 orchestration 邻近，可补性质工程
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (26) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/tsc_journal_a.md](./venues/tsc_journal_a.md)
- 数据文件：[metadata](metadata/tsc_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tsc_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=4629386
- 学术索引页：http://dblp.uni-trier.de/db/journals/tsc/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tsc_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (34) / 软件工程 (7) / 系统软件 (4)
- 软工纳入判定分布：不属于软件工程 (38) / 属于软件工程 (6) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (26) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (6)
- 判定来源分布：启发式初判 (45)
- 人工复核状态分布：未人工复核 (45)
- 高频软工主路径：2.1.4 云/服务/平台架构 (2) / 6.1.2 过程挖掘、符合性与改进 (2) / 1.2.1 形式化规约与契约 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.1.4 场景化测试 (1)
- 主题标签补充：建模/模型驱动 (23) / 维护与演化 (11) / 形式化方法 (10) / 可靠性/安全 (8) / 需求工程 (8)

---

### `ECOOP`

- 基本信息：
- 全称：European Conference on Object-Oriented Programming
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`29`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`OO` 程序结构 / 分析与重构邻近
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (28) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ecoop_conf_b.md](./venues/ecoop_conf_b.md)
- 数据文件：[metadata](metadata/ecoop_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ecoop_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ecoop/
- 官方论文集页：https://doi.org/10.1007/978-3-642-39038-8
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ecoop_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (24) / 软件工程 (4) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (25) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (28) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (29)
- 人工复核状态分布：未人工复核 (29)
- 高频软工主路径：2.2.1 设计原则、模式与反模式 (1) / 2.2.2 模块化、依赖与解耦 (1) / 6.3.1 实验、案例研究与调查 (1) / 4.1.2 重构、重模块化与代码清理 (1)
- 主题标签补充：待人工细分 (19) / 测试与验证 (3) / 形式化方法 (2) / 程序设计语言/编译 (2) / 程序分析 (2)

---

### `ICPC`

- 基本信息：
- 全称：IEEE International Conference on Program Comprehension
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`31`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序理解 / 缺陷分析 / 修复解释与人因辅助
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (20) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/icpc_conf_b.md](./venues/icpc_conf_b.md)
- 数据文件：[metadata](metadata/icpc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icpc_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/iwpc/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6597032/proceeding / https://www.computer.org/csdl/proceedings/icpc/2013/3092/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icpc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (29) / 跨域/待判定 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (29) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (20) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (31)
- 人工复核状态分布：未人工复核 (31)
- 高频软工主路径：6.5.1 开发者认知、生产力与福祉 (6) / 4.2.4 克隆、相似性与理解支持 (5) / 4.2.1 代码搜索、导航与摘要 (3) / 4.1.1 缺陷修复与维护性修正 (2) / 6.3.1 实验、案例研究与调查 (1) / 3.1.4 场景化测试 (1) / 4.1.5 技术债、克隆与可维护性治理 (1) / 2.2.2 模块化、依赖与解耦 (1)
- 主题标签补充：经验软件工程 (19) / 维护与演化 (10) / 测试与验证 (7) / 建模/模型驱动 (6) / 可靠性/安全 (4)

---

### `RE / 会议 / B`

- 基本信息：
- 全称：IEEE International Requirements Engineering Conference
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`67`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (63) / 🟡 保留观察 (2) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/re_conf_b.md](./venues/re_conf_b.md)
- 数据文件：[metadata](metadata/re_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/re/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6621629/proceeding / http://www.computer.org/csdl/proceedings/re/2013/9999/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/re_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (65) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (65) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (63) / 🟡 保留观察 (2) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (67)
- 人工复核状态分布：未人工复核 (67)
- 高频软工主路径：1.1.1 需求获取与发现 (33) / 1.1.4 需求追踪、变更与演化 (7) / 6.3.1 实验、案例研究与调查 (6) / 1.1.2 需求分析、协商与优先级 (2) / 1.3.1 建模语言与元模型 (2) / 3.2.3 面向质量属性的分析 (2) / 2.3.3 组件、包与集成工程 (2) / 5.1.5 功能安全、危害分析与 safety assurance (1)
- 主题标签补充：需求工程 (63) / 建模/模型驱动 (22) / 维护与演化 (12) / 经验软件工程 (11) / 形式化方法 (9)

---

### `CAiSE`

- 基本信息：
- 全称：International Conference on Advanced Information Systems Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`89`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：信息系统与过程/模型工程，适合补需求-建模-规约链
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (0) / ⏳ 待补信息 (77) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/caise_conf_b.md](./venues/caise_conf_b.md)
- 数据文件：[metadata](metadata/caise_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-caise_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/caise/
- 官方论文集页：https://doi.org/10.1007/978-3-642-38709-8 / https://ceur-ws.org/Vol-961 / https://nbn-resolving.org/urn:nbn:de:0074-961-0
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/caise_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (75) / 软件工程 (13) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (76) / 跨域但软工主导 (7) / 属于软件工程 (6)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (0) / ⏳ 待补信息 (77) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (89)
- 人工复核状态分布：未人工复核 (89)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (4) / 1.3.1 建模语言与元模型 (4) / 1.1.1 需求获取与发现 (2) / 8.2.3 服务系统与 API 生态 (1) / 7.1.1 代码生成、补全与变换 (1) / 6.2.4 组合治理与决策支持 (1)
- 主题标签补充：待人工细分 (52) / 建模/模型驱动 (20) / 需求工程 (11) / 测试与验证 (3) / 系统软件 (3)

---

### `MoDELS`

- 基本信息：
- 全称：ACM/IEEE International Conference on Model Driven Engineering Languages and Systems
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`47`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：模型驱动 / 状态机-SysML / 形式化建模主场
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (39) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/models_conf_b.md](./venues/models_conf_b.md)
- 数据文件：[metadata](metadata/models_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-models_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/models/
- 官方论文集页：https://doi.org/10.1007/978-3-642-41533-3
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/models_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (29) / 跨域/待判定 (18)
- 软工纳入判定分布：属于软件工程 (29) / 不属于软件工程 (18)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (39) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (47)
- 人工复核状态分布：未人工复核 (47)
- 高频软工主路径：1.3.1 建模语言与元模型 (16) / 3.3.3 assurance、认证与合规验证 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 1.4.1 特征建模与配置 (2) / 2.2.3 API、接口与协议设计 (1) / 2.1.3 架构演化与重构 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.3.1 面向软工问题的形式化验证 (1)
- 主题标签补充：建模/模型驱动 (34) / 测试与验证 (8) / 待人工细分 (7) / 维护与演化 (5) / 形式化方法 (4)

---

### `ICSOC`

- 基本信息：
- 全称：International Conference on Service Oriented Computing
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`65`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务组合 / 流程 / 性质与治理偶有贴题
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (2) / ⏳ 待补信息 (62) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsoc_conf_b.md](./venues/icsoc_conf_b.md)
- 数据文件：[metadata](metadata/icsoc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsoc_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsoc/
- 官方论文集页：https://doi.org/10.1007/978-3-642-45005-1 / https://www.wikidata.org/entity/Q134464527
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsoc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (63) / 软件工程 (2)
- 软工纳入判定分布：不属于软件工程 (63) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (2) / ⏳ 待补信息 (62) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (65)
- 人工复核状态分布：未人工复核 (65)
- 高频软工主路径：6.2.1 估算、计划与排程 (1) / 1.3.1 建模语言与元模型 (1)
- 主题标签补充：待人工细分 (34) / 系统软件 (13) / 建模/模型驱动 (11) / 运行时监测 (7) / 测试与验证 (4)

---

### `SANER`

- 基本信息：
- 全称：IEEE International Conference on Software Analysis, Evolution, and Reengineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：代码分析 / 逆向 / 演化与 reengineering
- 初筛分布：无 2013 条目
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
- 年份：`2013`
- 条目数：`92`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：维护演化 / 修复 / 回归验证 / 工程闭环邻近
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (74) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/icsme_conf_b.md](./venues/icsme_conf_b.md)
- 数据文件：[metadata](metadata/icsme_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsme_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsm/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsme_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (89) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (89) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (74) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (92)
- 人工复核状态分布：未人工复核 (92)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (28) / 4.1.2 重构、重模块化与代码清理 (8) / 6.3.1 实验、案例研究与调查 (6) / 3.1.4 场景化测试 (5) / 7.1.4 AI 支持的架构、设计与工程决策 (5) / 2.2.1 设计原则、模式与反模式 (3) / 6.3.4 replication、benchmark 与开放科学 (3) / 3.1.2 回归测试与测试选择 (2)
- 主题标签补充：维护与演化 (50) / 经验软件工程 (41) / 可靠性/安全 (22) / 测试与验证 (21) / 建模/模型驱动 (20)

---

### `VMCAI`

- 基本信息：
- 全称：International Conference on Verification, Model Checking, and Abstract Interpretation
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`31`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：程序验证 / 模型检查 / 抽象解释直接支撑验证框架
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/vmcai_conf_b.md](./venues/vmcai_conf_b.md)
- 数据文件：[metadata](metadata/vmcai_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-vmcai_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/vmcai/
- 官方论文集页：https://doi.org/10.1007/978-3-642-35873-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/vmcai_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (28) / 软件工程 (2) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (29) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (31)
- 人工复核状态分布：未人工复核 (31)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (2)
- 主题标签补充：待人工细分 (20) / 形式化方法 (5) / 建模/模型驱动 (3) / 可靠性/安全 (2) / 程序修复 (1)

---

### `ICWS`

- 基本信息：
- 全称：IEEE International Conference on Web Services
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`85`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：Web services / orchestration / 性质验证偶有贴题
- 初筛分布：🟢 优先跟进 (26) / 🟡 保留观察 (48) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (11)
- 论文名录页：[venues/icws_conf_b.md](./venues/icws_conf_b.md)
- 数据文件：[metadata](metadata/icws_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icws_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icws/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6596022/proceeding / http://www.computer.org/csdl/proceedings/icws/2013/5025/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icws_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (69) / 软件工程 (11) / 系统软件 (5)
- 软工纳入判定分布：不属于软件工程 (74) / 属于软件工程 (9) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (26) / 🟡 保留观察 (48) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (11)
- 判定来源分布：启发式初判 (85)
- 人工复核状态分布：未人工复核 (85)
- 高频软工主路径：2.1.4 云/服务/平台架构 (4) / 3.1.4 场景化测试 (3) / 1.1.4 需求追踪、变更与演化 (1) / 8.2.3 服务系统与 API 生态 (1) / 2.2.1 设计原则、模式与反模式 (1) / 1.1.1 需求获取与发现 (1)
- 主题标签补充：建模/模型驱动 (36) / 需求工程 (25) / 维护与演化 (21) / 可靠性/安全 (18) / 测试与验证 (18)

---

### `ESEM`

- 基本信息：
- 全称：International Symposium on Empirical Software Engineering and Measurement
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`56`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证方法 / 评测设计 / `LLM-SE` 实验口径重要
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (36) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/esem_conf_b.md](./venues/esem_conf_b.md)
- 数据文件：[metadata](metadata/esem_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-esem_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/esem/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6681322/proceeding / http://www.computer.org/csdl/proceedings/esem/2013/5056/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/esem_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (55) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (55) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (36) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (56)
- 人工复核状态分布：未人工复核 (56)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (24) / 4.1.1 缺陷修复与维护性修正 (8) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 4.1.2 重构、重模块化与代码清理 (2) / 6.3.4 replication、benchmark 与开放科学 (2) / 3.4.1 调试、分诊与根因分析 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (2) / 2.2.3 API、接口与协议设计 (1)
- 主题标签补充：经验软件工程 (23) / 测试与验证 (19) / 建模/模型驱动 (19) / 维护与演化 (12) / 可靠性/安全 (10)

---

### `ISSRE`

- 基本信息：
- 全称：IEEE International Symposium on Software Reliability Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2013`
- 条目数：`47`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：可靠性 / assurance / 安全关键验证与缺陷检测很近
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (32) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/issre_conf_b.md](./venues/issre_conf_b.md)
- 数据文件：[metadata](metadata/issre_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-issre_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/issre/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6689494/proceeding / http://www.computer.org/csdl/proceedings/issre/2013/9999/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/issre_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (47)
- 软工纳入判定分布：属于软件工程 (47)
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (32) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (47)
- 人工复核状态分布：未人工复核 (47)
- 高频软工主路径：3.3.3 assurance、认证与合规验证 (11) / 3.1.1 测试生成与增强 (6) / 3.1.4 场景化测试 (5) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 7.1.2 AI 支持的测试、分析与修复 (2) / 3.2.1 静态分析与抽象解释 (2) / 3.2.2 动态与混合分析 (2)
- 主题标签补充：测试与验证 (26) / 可靠性/安全 (23) / 建模/模型驱动 (17) / 经验软件工程 (11) / 维护与演化 (10)

---

### `ASE / 期刊 / B`

- 基本信息：
- 全称：Automated Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`20`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (17) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ase_journal_b.md](./venues/ase_journal_b.md)
- 数据文件：[metadata](metadata/ase_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10515
- 学术索引页：http://dblp.uni-trier.de/db/journals/ase/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ase_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (15) / 跨域/待判定 (5)
- 软工纳入判定分布：属于软件工程 (15) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (17) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (20)
- 人工复核状态分布：未人工复核 (20)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (6) / 1.1.1 需求获取与发现 (2) / 1.3.1 建模语言与元模型 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 6.2.1 估算、计划与排程 (1) / 4.1.2 重构、重模块化与代码清理 (1) / 1.3.2 模型转换、同步与协同 (1)
- 主题标签补充：待人工细分 (9) / 建模/模型驱动 (6) / 测试与验证 (5) / 需求工程 (2) / 维护与演化 (1)

---

### `ESE`

- 基本信息：
- 全称：Empirical Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`37`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证研究 / 数据集 / benchmark / 人因与评测设计
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (2) / ⏳ 待补信息 (31) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ese_journal_b.md](./venues/ese_journal_b.md)
- 数据文件：[metadata](metadata/ese_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ese_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10664
- 学术索引页：http://dblp.uni-trier.de/db/journals/ese/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ese_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (28) / 跨域/待判定 (9)
- 软工纳入判定分布：属于软件工程 (28) / 不属于软件工程 (9)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (2) / ⏳ 待补信息 (31) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (37)
- 人工复核状态分布：未人工复核 (37)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (9) / 3.2.3 面向质量属性的分析 (4) / 6.2.1 估算、计划与排程 (3) / 4.2.4 克隆、相似性与理解支持 (2) / 6.3.1 实验、案例研究与调查 (1) / 5.1.1 故障预测与失效分析 (1) / 1.1.4 需求追踪、变更与演化 (1) / 5.2.3 供应链安全与可追溯信任 (1)
- 主题标签补充：待人工细分 (13) / 经验软件工程 (10) / 建模/模型驱动 (6) / 维护与演化 (5) / 可靠性/安全 (5)

---

### `IETS`

- 基本信息：
- 全称：IET Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`29`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：broad SE 期刊，可筛少量建模/验证论文
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/iets_journal_b.md](./venues/iets_journal_b.md)
- 数据文件：[metadata](metadata/iets_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iets_journal_b)

- 关键信息页面：
- 期刊主页：https://ietresearch.onlinelibrary.wiley.com/journal/1751880x
- 学术索引页：https://dblp.uni-trier.de/db/journals/iet-sen
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/iets_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (20) / 跨域/待判定 (9)
- 软工纳入判定分布：属于软件工程 (20) / 不属于软件工程 (9)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (29)
- 人工复核状态分布：未人工复核 (29)
- 高频软工主路径：1.3.1 建模语言与元模型 (2) / 1.1.1 需求获取与发现 (2) / 2.2.4 技术债与设计质量 (2) / 3.1.1 测试生成与增强 (1) / 7.1.1 代码生成、补全与变换 (1) / 4.1.4 迁移、现代化与遗留系统更新 (1) / 6.2.1 估算、计划与排程 (1) / 2.3.3 组件、包与集成工程 (1)
- 主题标签补充：测试与验证 (15) / 建模/模型驱动 (10) / 需求工程 (8) / 形式化方法 (7) / 可靠性/安全 (6)

---

### `IST`

- 基本信息：
- 全称：Information and Software Technology
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`136`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 建模测试 / `AI4SE` 论文较常见
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (2) / ⏳ 待补信息 (108) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/ist_journal_b.md](./venues/ist_journal_b.md)
- 数据文件：[metadata](metadata/ist_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ist_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/information-and-software-technology
- 学术索引页：http://dblp.uni-trier.de/db/journals/infsof/index.html
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ist_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (76) / 软件工程 (59) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (77) / 属于软件工程 (59)
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (2) / ⏳ 待补信息 (108) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (136)
- 人工复核状态分布：未人工复核 (136)
- 高频软工主路径：1.1.1 需求获取与发现 (21) / 7.1.1 代码生成、补全与变换 (10) / 6.2.1 估算、计划与排程 (3) / 6.3.1 实验、案例研究与调查 (2) / 3.1.4 场景化测试 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (2) / 1.3.1 建模语言与元模型 (2) / 3.2.1 静态分析与抽象解释 (2)
- 主题标签补充：待人工细分 (53) / 测试与验证 (29) / 建模/模型驱动 (28) / 经验软件工程 (17) / 维护与演化 (12)

---

### `JSEP`

- 基本信息：
- 全称：Journal of Software: Evolution and Process
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`63`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：演化 / 过程 / 迭代闭环与工程实践邻近
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (41) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/jsep_journal_b.md](./venues/jsep_journal_b.md)
- 数据文件：[metadata](metadata/jsep_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jsep_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/20477481
- 学术索引页：http://dblp.uni-trier.de/db/journals/smr/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jsep_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (61) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (61) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (15) / 🟡 保留观察 (41) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (63)
- 人工复核状态分布：未人工复核 (63)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (18) / 6.1.2 过程挖掘、符合性与改进 (6) / 3.1.4 场景化测试 (5) / 1.1.4 需求追踪、变更与演化 (5) / 2.2.1 设计原则、模式与反模式 (4) / 2.2.4 技术债与设计质量 (3) / 1.3.1 建模语言与元模型 (2) / 6.3.1 实验、案例研究与调查 (2)
- 主题标签补充：维护与演化 (39) / 建模/模型驱动 (20) / 测试与验证 (17) / 经验软件工程 (15) / 需求工程 (12)

---

### `JSS`

- 基本信息：
- 全称：Journal of Systems and Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`229`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：系统与软件工程综合刊，常见建模/验证/CPS 个案
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (1) / ⏳ 待补信息 (209) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/jss_journal_b.md](./venues/jss_journal_b.md)
- 数据文件：[metadata](metadata/jss_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jss_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/journal-of-systems-and-software
- 学术索引页：http://dblp.uni-trier.de/db/journals/jss/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jss_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (158) / 软件工程 (66) / 系统软件 (5)
- 软工纳入判定分布：不属于软件工程 (163) / 属于软件工程 (66)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (1) / ⏳ 待补信息 (209) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (229)
- 人工复核状态分布：未人工复核 (229)
- 高频软工主路径：2.1.1 架构描述与恢复 (22) / 7.1.4 AI 支持的架构、设计与工程决策 (6) / 3.1.4 场景化测试 (6) / 6.3.1 实验、案例研究与调查 (6) / 4.1.2 重构、重模块化与代码清理 (3) / 1.3.1 建模语言与元模型 (2) / 1.1.2 需求分析、协商与优先级 (2) / 3.2.3 面向质量属性的分析 (2)
- 主题标签补充：待人工细分 (129) / 建模/模型驱动 (33) / 系统软件 (20) / 测试与验证 (20) / 可靠性/安全 (15)

---

### `RE / 期刊 / B`

- 基本信息：
- 全称：Requirements Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`20`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/re_journal_b.md](./venues/re_journal_b.md)
- 数据文件：[metadata](metadata/re_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/766
- 学术索引页：http://dblp.uni-trier.de/db/journals/re/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/re_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (18) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (18) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (0) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (20)
- 人工复核状态分布：未人工复核 (20)
- 高频软工主路径：1.1.1 需求获取与发现 (8) / 3.2.3 面向质量属性的分析 (4) / 6.3.1 实验、案例研究与调查 (2) / 7.1.5 人机协同开发与评估 (1) / 1.1.2 需求分析、协商与优先级 (1) / 5.2.2 隐私工程与数据治理 (1) / 1.2.3 规约质量与一致性 (1)
- 主题标签补充：需求工程 (14) / 可靠性/安全 (6) / 系统软件 (5) / 待人工细分 (4) / 经验软件工程 (2)

---

### `SCP`

- 基本信息：
- 全称：Science of Computer Programming
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`140`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件程序与形式化/验证/程序分析交叉，贴题概率中高
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (1) / ⏳ 待补信息 (128) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/scp_journal_b.md](./venues/scp_journal_b.md)
- 数据文件：[metadata](metadata/scp_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scp_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/science-of-computer-programming
- 学术索引页：http://dblp.uni-trier.de/db/journals/scp/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/scp_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (112) / 软件工程 (24) / 系统软件 (4)
- 软工纳入判定分布：不属于软件工程 (116) / 跨域但软工主导 (14) / 属于软件工程 (10)
- 初筛分布：🟢 优先跟进 (11) / 🟡 保留观察 (1) / ⏳ 待补信息 (128) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (140)
- 人工复核状态分布：未人工复核 (140)
- 高频软工主路径：1.2.1 形式化规约与契约 (11) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 4.1.2 重构、重模块化与代码清理 (2) / 3.2.1 静态分析与抽象解释 (2) / 3.3.1 面向软工问题的形式化验证 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 4.1.1 缺陷修复与维护性修正 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：待人工细分 (85) / 建模/模型驱动 (16) / 形式化方法 (15) / 测试与验证 (10) / 程序设计语言/编译 (8)

---

### `SoSyM`

- 基本信息：
- 全称：Software and Systems Modeling
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`53`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件与系统建模 / DSL / 状态机与模型分析主场
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (3) / ⏳ 待补信息 (42) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sosym_journal_b.md](./venues/sosym_journal_b.md)
- 数据文件：[metadata](metadata/sosym_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sosym_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10270
- 学术索引页：http://dblp.uni-trier.de/db/journals/sosym/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sosym_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (29) / 软件工程 (23) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (30) / 属于软件工程 (23)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (3) / ⏳ 待补信息 (42) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (53)
- 人工复核状态分布：未人工复核 (53)
- 高频软工主路径：1.3.1 建模语言与元模型 (11) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 1.3.2 模型转换、同步与协同 (1) / 1.3.3 模型分析、仿真与验证 (1) / 1.1.4 需求追踪、变更与演化 (1) / 2.1.1 架构描述与恢复 (1) / 1.3.5 模型质量、仓库与治理 (1) / 3.1.4 场景化测试 (1)
- 主题标签补充：建模/模型驱动 (30) / 待人工细分 (18) / 需求工程 (6) / 维护与演化 (3) / 测试与验证 (3)

---

### `STVR`

- 基本信息：
- 全称：Software Testing, Verification and Reliability
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`30`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 验证 / 可靠性与 formal properties 非常贴题
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/stvr_journal_b.md](./venues/stvr_journal_b.md)
- 数据文件：[metadata](metadata/stvr_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-stvr_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/10991689
- 学术索引页：http://dblp.uni-trier.de/db/journals/stvr/index.html
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/stvr_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (27) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (27) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (18) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (30)
- 人工复核状态分布：未人工复核 (30)
- 高频软工主路径：3.1.1 测试生成与增强 (7) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (6) / 3.1.4 场景化测试 (5) / 1.2.1 形式化规约与契约 (2) / 1.1.4 需求追踪、变更与演化 (2) / 5.3.4 扩展性、吞吐与时延保证 (1) / 1.3.3 模型分析、仿真与验证 (1) / 1.3.2 模型转换、同步与协同 (1)
- 主题标签补充：测试与验证 (26) / 需求工程 (9) / 维护与演化 (7) / 建模/模型驱动 (7) / 形式化方法 (6)

---

### `SPE`

- 基本信息：
- 全称：Software: Practice and Experience
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`74`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：工程实践 / 系统实现为主，偶有 runtime/verification
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (41) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (12)
- 论文名录页：[venues/spe_journal_b.md](./venues/spe_journal_b.md)
- 数据文件：[metadata](metadata/spe_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spe_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/1097024x
- 学术索引页：http://dblp.uni-trier.de/db/journals/spe/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/spe_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (45) / 系统软件 (12) / 软件工程 (11) / 程序设计语言与形式化基础 (6)
- 软工纳入判定分布：不属于软件工程 (63) / 属于软件工程 (9) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (41) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (12)
- 判定来源分布：启发式初判 (74)
- 人工复核状态分布：未人工复核 (74)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (4) / 2.3.1 代码生成、脚手架与 DSL 工程 (1) / 7.1.1 代码生成、补全与变换 (1) / 3.1.4 场景化测试 (1) / 3.4.1 调试、分诊与根因分析 (1) / 6.2.2 风险、价值与优先级 (1) / 2.2.1 设计原则、模式与反模式 (1) / 1.3.1 建模语言与元模型 (1)
- 主题标签补充：测试与验证 (23) / 建模/模型驱动 (21) / 可靠性/安全 (16) / 形式化方法 (16) / 需求工程 (15)

---

### `PASTE`

- 基本信息：
- 全称：ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`7`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (4) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/paste_conf_c.md](./venues/paste_conf_c.md)
- 数据文件：[metadata](metadata/paste_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-paste_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/paste/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/paste_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (5) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (7)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (4) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (7)
- 人工复核状态分布：未人工复核 (7)
- 主题标签补充：程序设计语言/编译 (3) / 需求工程 (2) / 可靠性/安全 (2) / 测试与验证 (2) / 维护与演化 (1)

---

### `APSEC`

- 基本信息：
- 全称：Asia-Pacific Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`107`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 亚洲社区，`LLM-SE/测试/建模` 可见
- 初筛分布：🟢 优先跟进 (45) / 🟡 保留观察 (55) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/apsec_conf_c.md](./venues/apsec_conf_c.md)
- 数据文件：[metadata](metadata/apsec_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-apsec_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/apsec/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=6805370 / https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=6754325
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/apsec_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (83) / 跨域/待判定 (23) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (83) / 不属于软件工程 (24)
- 初筛分布：🟢 优先跟进 (45) / 🟡 保留观察 (55) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (107)
- 人工复核状态分布：未人工复核 (107)
- 高频软工主路径：1.1.1 需求获取与发现 (6) / 6.3.1 实验、案例研究与调查 (5) / 7.1.1 代码生成、补全与变换 (5) / 6.3.4 replication、benchmark 与开放科学 (4) / 3.2.1 静态分析与抽象解释 (3) / 1.3.3 模型分析、仿真与验证 (3) / 3.3.1 面向软工问题的形式化验证 (3) / 1.3.1 建模语言与元模型 (3)
- 主题标签补充：建模/模型驱动 (47) / 形式化方法 (33) / 需求工程 (31) / 测试与验证 (25) / 维护与演化 (24)

---

### `EASE`

- 基本信息：
- 全称：International Conference on Evaluation and Assessment in Software Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`31`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：评测与实验设计 / benchmark / replication 有用
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (23) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/ease_conf_c.md](./venues/ease_conf_c.md)
- 数据文件：[metadata](metadata/ease_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ease_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ease/
- 官方论文集页：http://dl.acm.org/citation.cfm?id=2460999
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ease_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (30) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (30) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (23) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (31)
- 人工复核状态分布：未人工复核 (31)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (11) / 6.3.3 系统综述、mapping 与 meta-analysis (5) / 4.1.1 缺陷修复与维护性修正 (4) / 6.5.3 开源社区、多样性与治理 (2) / 4.1.5 技术债、克隆与可维护性治理 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1) / 3.2.1 静态分析与抽象解释 (1) / 6.3.4 replication、benchmark 与开放科学 (1)
- 主题标签补充：经验软件工程 (16) / 维护与演化 (11) / 建模/模型驱动 (8) / 测试与验证 (7) / 形式化方法 (6)

---

### `ICECCS`

- 基本信息：
- 全称：International Conference on Engineering of Complex Computer Systems
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`39`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：复杂系统建模与验证 / safety-critical / CPS 邻近
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/iceccs_conf_c.md](./venues/iceccs_conf_c.md)
- 数据文件：[metadata](metadata/iceccs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iceccs_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/iceccs/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6599337/proceeding / http://www.computer.org/csdl/proceedings/iceccs/2013/5007/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/iceccs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (25) / 软件工程 (7) / 程序设计语言与形式化基础 (4) / 系统软件 (3)
- 软工纳入判定分布：不属于软件工程 (32) / 属于软件工程 (7)
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (15) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (39)
- 人工复核状态分布：未人工复核 (39)
- 高频软工主路径：1.3.2 模型转换、同步与协同 (1) / 1.1.2 需求分析、协商与优先级 (1) / 4.3.1 版本、配置与构建工程 (1) / 6.3.4 replication、benchmark 与开放科学 (1) / 2.3.3 组件、包与集成工程 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1)
- 主题标签补充：建模/模型驱动 (19) / 形式化方法 (15) / 测试与验证 (15) / 需求工程 (13) / 可靠性/安全 (8)

---

### `ICST`

- 基本信息：
- 全称：IEEE International Conference on Software Testing, Verification and Validation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`71`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 形式化验证 / 缺陷检测与修复直接相关
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (45) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/icst_conf_c.md](./venues/icst_conf_c.md)
- 数据文件：[metadata](metadata/icst_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icst_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icst/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6569023/proceeding / http://www.computer.org/csdl/proceedings/icst/2013/4968/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icst_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (71)
- 软工纳入判定分布：属于软件工程 (71)
- 初筛分布：🟢 优先跟进 (25) / 🟡 保留观察 (45) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (71)
- 人工复核状态分布：未人工复核 (71)
- 高频软工主路径：3.1.1 测试生成与增强 (19) / 3.1.4 场景化测试 (8) / 3.2.3 面向质量属性的分析 (7) / 1.3.1 建模语言与元模型 (4) / 6.3.1 实验、案例研究与调查 (3) / 3.1.2 回归测试与测试选择 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 1.3.2 模型转换、同步与协同 (2)
- 主题标签补充：测试与验证 (64) / 可靠性/安全 (24) / 建模/模型驱动 (20) / 维护与演化 (14) / 需求工程 (10)

---

### `SCAM`

- 基本信息：
- 全称：IEEE International Working Conference on Source Code Analysis and Manipulation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`24`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：源码分析与变换 / 缺陷修复 / 程序理解邻近
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (17) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/scam_conf_c.md](./venues/scam_conf_c.md)
- 数据文件：[metadata](metadata/scam_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scam_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/scam/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6636284/proceeding / http://www.computer.org/csdl/proceedings/scam/2013/9999/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/scam_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (15) / 跨域/待判定 (8) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (15) / 不属于软件工程 (9)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (17) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (24)
- 人工复核状态分布：未人工复核 (24)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (7) / 3.4.2 缺陷定位、补丁生成与程序修复 (1) / 2.3.2 构建工具链与开发环境 (1) / 2.2.2 模块化、依赖与解耦 (1) / 4.1.1 缺陷修复与维护性修正 (1) / 6.3.4 replication、benchmark 与开放科学 (1) / 3.2.2 动态与混合分析 (1) / 3.1.4 场景化测试 (1)
- 主题标签补充：经验软件工程 (9) / 测试与验证 (6) / 可靠性/安全 (5) / 程序分析 (5) / 维护与演化 (4)

---

### `COMPSAC`

- 基本信息：
- 全称：International Computer Software and Applications Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`140`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：覆盖过宽，需按建模/验证/`AI4SE` 子题筛选
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (59) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (38)
- 论文名录页：[venues/compsac_conf_c.md](./venues/compsac_conf_c.md)
- 数据文件：[metadata](metadata/compsac_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-compsac_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/compsac/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6605717/proceeding / http://www.computer.org/csdl/proceedings/compsac/2013/4987/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/compsac_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (100) / 软件工程 (24) / 系统软件 (14) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：不属于软件工程 (116) / 属于软件工程 (20) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (43) / 🟡 保留观察 (59) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (38)
- 判定来源分布：启发式初判 (140)
- 人工复核状态分布：未人工复核 (140)
- 高频软工主路径：2.1.1 架构描述与恢复 (5) / 1.1.1 需求获取与发现 (4) / 3.3.1 面向软工问题的形式化验证 (3) / 3.2.3 面向质量属性的分析 (2) / 3.1.4 场景化测试 (2) / 2.2.1 设计原则、模式与反模式 (2) / 3.1.2 回归测试与测试选择 (1) / 3.2.4 分析驱动的理解、重构与综合 (1)
- 主题标签补充：建模/模型驱动 (45) / 测试与验证 (41) / 待人工细分 (34) / 需求工程 (27) / 形式化方法 (22)

---

### `ICFEM`

- 基本信息：
- 全称：International Conference on Formal Engineering Methods
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`29`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：formal engineering / 规约建模 / 验证与证明
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icfem_conf_c.md](./venues/icfem_conf_c.md)
- 数据文件：[metadata](metadata/icfem_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icfem_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icfem/
- 官方论文集页：https://doi.org/10.1007/978-3-642-41202-8
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icfem_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (20) / 软件工程 (8) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (21) / 属于软件工程 (5) / 跨域但软工主导 (3)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (29)
- 人工复核状态分布：未人工复核 (29)
- 高频软工主路径：1.2.1 形式化规约与契约 (3) / 1.3.1 建模语言与元模型 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.2.1 静态分析与抽象解释 (1) / 1.1.4 需求追踪、变更与演化 (1) / 8.2.3 服务系统与 API 生态 (1)
- 主题标签补充：测试与验证 (9) / 形式化方法 (8) / 待人工细分 (7) / 需求工程 (6) / 建模/模型驱动 (4)

---

### `SSE`

- 基本信息：
- 全称：IEEE International Conference on Software Services Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`108`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件服务工程混合
- 初筛分布：🟢 优先跟进 (31) / 🟡 保留观察 (59) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18)
- 论文名录页：[venues/sse_conf_c.md](./venues/sse_conf_c.md)
- 数据文件：[metadata](metadata/sse_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sse_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/IEEEscc/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/sse_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (96) / 系统软件 (7) / 软件工程 (3) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：不属于软件工程 (105) / 属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (31) / 🟡 保留观察 (59) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18)
- 判定来源分布：启发式初判 (108)
- 人工复核状态分布：未人工复核 (108)
- 高频软工主路径：2.1.4 云/服务/平台架构 (2) / 4.4.2 事故诊断、回滚与恢复 (1)
- 主题标签补充：建模/模型驱动 (52) / 系统软件 (28) / 需求工程 (23) / 维护与演化 (17) / 测试与验证 (16)

---

### `ICSSP`

- 基本信息：
- 全称：International Conference on Software and System Process
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`23`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件过程 / 团队与流程，对主问题较间接
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/icssp_conf_c.md](./venues/icssp_conf_c.md)
- 数据文件：[metadata](metadata/icssp_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icssp_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ispw/
- 官方论文集页：http://dl.acm.org/citation.cfm?id=2486046
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icssp_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (20) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (20) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 判定来源分布：启发式初判 (23)
- 人工复核状态分布：未人工复核 (23)
- 高频软工主路径：6.1.1 敏捷、精益与 DevOps 方法 (7) / 6.2.2 风险、价值与优先级 (3) / 6.3.1 实验、案例研究与调查 (2) / 6.3.3 系统综述、mapping 与 meta-analysis (1) / 2.2.1 设计原则、模式与反模式 (1) / 6.5.1 开发者认知、生产力与福祉 (1) / 6.2.1 估算、计划与排程 (1) / 1.1.1 需求获取与发现 (1)
- 主题标签补充：建模/模型驱动 (7) / 需求工程 (5) / 待人工细分 (5) / 维护与演化 (5) / 测试与验证 (5)

---

### `SEKE`

- 基本信息：
- 全称：International Conference on Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`143`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 偶有贴题
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (0) / ⏳ 待补信息 (129) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/seke_conf_c.md](./venues/seke_conf_c.md)
- 数据文件：[metadata](metadata/seke_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-seke_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/seke/
- 官方论文集页：http://ksiresearchorg.ipage.com/seke/Proceedings/seke/SEKE2013_Proceedings.pdf
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/seke_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (109) / 软件工程 (34)
- 软工纳入判定分布：不属于软件工程 (109) / 属于软件工程 (18) / 跨域但软工主导 (16)
- 初筛分布：🟢 优先跟进 (14) / 🟡 保留观察 (0) / ⏳ 待补信息 (129) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (143)
- 人工复核状态分布：未人工复核 (143)
- 高频软工主路径：1.1.1 需求获取与发现 (16) / 1.1.4 需求追踪、变更与演化 (3) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (2) / 3.1.4 场景化测试 (2) / 6.2.2 风险、价值与优先级 (1) / 1.4.1 特征建模与配置 (1) / 2.1.1 架构描述与恢复 (1) / 3.2.3 面向质量属性的分析 (1)
- 主题标签补充：待人工细分 (72) / 建模/模型驱动 (21) / 测试与验证 (19) / 经验软件工程 (10) / 需求工程 (9)

---

### `QRS`

- 基本信息：
- 全称：International Conference on Software Quality, Reliability and Security
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：质量 / 可靠性 / 安全 / assurance 与验证链很近
- 初筛分布：无 2013 条目
- 论文名录页：[venues/qrs_conf_c.md](./venues/qrs_conf_c.md)
- 数据文件：[metadata](metadata/qrs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-qrs_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.uni-trier.de/db/conf/qrs
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/qrs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `ICSR`

- 基本信息：
- 全称：International Conference on Software Reuse
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`27`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：复用 / 组件资产，可补模型资产与可复用工件
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (27) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsr_conf_c.md](./venues/icsr_conf_c.md)
- 数据文件：[metadata](metadata/icsr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsr_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsr/
- 官方论文集页：https://doi.org/10.1007/978-3-642-38977-1
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (15) / 跨域/待判定 (12)
- 软工纳入判定分布：属于软件工程 (15) / 不属于软件工程 (12)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (27) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：1.4.1 特征建模与配置 (12) / 3.3.3 assurance、认证与合规验证 (1) / 3.3.2 运行时验证与运行时监测 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1)
- 主题标签补充：待人工细分 (13) / 建模/模型驱动 (8) / 测试与验证 (3) / 经验软件工程 (2) / 形式化方法 (1)

---

### `SPIN`

- 基本信息：
- 全称：International Symposium on Model Checking of Software
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`22`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件模型检查 / state-based verification / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (14) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/spin_conf_c.md](./venues/spin_conf_c.md)
- 数据文件：[metadata](metadata/spin_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spin_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/spin/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-642-39176-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/spin_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (18) / 软件工程 (4)
- 软工纳入判定分布：不属于软件工程 (18) / 属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (14) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (22)
- 人工复核状态分布：未人工复核 (22)
- 高频软工主路径：1.3.3 模型分析、仿真与验证 (3) / 1.2.1 形式化规约与契约 (1)
- 主题标签补充：待人工细分 (10) / 形式化方法 (7) / 测试与验证 (5) / 建模/模型驱动 (4) / 经验软件工程 (1)

---

### `TASE`

- 基本信息：
- 全称：Theoretical Aspects of Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`35`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件工程名下的 formal verification / assurance 邻近
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/tase_conf_c.md](./venues/tase_conf_c.md)
- 数据文件：[metadata](metadata/tase_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tase_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/tase/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6597031/proceeding / http://www.computer.org/csdl/proceedings/tase/2013/5053/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/tase_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (25) / 软件工程 (8) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (27) / 属于软件工程 (7) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (35)
- 人工复核状态分布：未人工复核 (35)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (3) / 5.1.2 容错、韧性与恢复能力 (1) / 1.2.1 形式化规约与契约 (1) / 1.3.1 建模语言与元模型 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.1.4 场景化测试 (1)
- 主题标签补充：建模/模型驱动 (21) / 形式化方法 (15) / 需求工程 (10) / 程序设计语言/编译 (9) / 测试与验证 (7)

---

### `MSR`

- 基本信息：
- 全称：Mining Software Repositories
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`64`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：仓库挖掘 / benchmark / `LLM-SE` 证据与数据建设有用
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (51) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/msr_conf_c.md](./venues/msr_conf_c.md)
- 数据文件：[metadata](metadata/msr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-msr_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/msr/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6597024/proceeding / http://www.computer.org/csdl/proceedings/msr/2013/0345/00/index.html / http://dl.acm.org/citation.cfm?id=2487085
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/msr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (60) / 跨域/待判定 (4)
- 软工纳入判定分布：属于软件工程 (60) / 不属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (51) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 判定来源分布：启发式初判 (64)
- 人工复核状态分布：未人工复核 (64)
- 高频软工主路径：6.3.4 replication、benchmark 与开放科学 (16) / 4.1.1 缺陷修复与维护性修正 (13) / 6.3.1 实验、案例研究与调查 (6) / 3.1.4 场景化测试 (3) / 2.2.1 设计原则、模式与反模式 (3) / 2.2.2 模块化、依赖与解耦 (2) / 3.2.3 面向质量属性的分析 (2) / 6.5.2 协作、评审与知识共享 (2)
- 主题标签补充：经验软件工程 (34) / 维护与演化 (27) / 可靠性/安全 (13) / 建模/模型驱动 (10) / 测试与验证 (9)

---

### `REFSQ`

- 基本信息：
- 全称：Requirements Engineering: Foundation for Software Quality
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`28`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求质量 / 需求规约 / 需求到性质非常贴题
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/refsq_conf_c.md](./venues/refsq_conf_c.md)
- 数据文件：[metadata](metadata/refsq_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-refsq_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/refsq/
- 官方论文集页：https://doi.org/10.1007/978-3-642-37422-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/refsq_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (25) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (25) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (21) / 🟡 保留观察 (0) / ⏳ 待补信息 (7) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (28)
- 人工复核状态分布：未人工复核 (28)
- 高频软工主路径：1.1.1 需求获取与发现 (18) / 1.1.4 需求追踪、变更与演化 (3) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 6.3.1 实验、案例研究与调查 (1) / 1.3.1 建模语言与元模型 (1) / 8.3.3 系统之系统与互操作 (1)
- 主题标签补充：需求工程 (22) / 待人工细分 (5) / 建模/模型驱动 (3) / 形式化方法 (2) / 运行时监测 (1)

---

### `WICSA`

- 基本信息：
- 全称：Working IEEE/IFIP Conference on Software Architecture
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件架构 / 设计决策 / 模型结构与演化有用
- 初筛分布：无 2013 条目
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
- 年份：`2013`
- 条目数：`34`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：平台 / 网络化软件 / 运行治理邻近
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/internetware_conf_c.md](./venues/internetware_conf_c.md)
- 数据文件：[metadata](metadata/internetware_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-internetware_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.org/db/conf/internetware/index.html
- 官方论文集页：https://doi.org/10.1145/2532443
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/internetware_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (24) / 跨域/待判定 (7) / 系统软件 (3)
- 软工纳入判定分布：属于软件工程 (24) / 不属于软件工程 (10)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (21) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (34)
- 人工复核状态分布：未人工复核 (34)
- 高频软工主路径：2.1.4 云/服务/平台架构 (13) / 3.1.4 场景化测试 (2) / 7.1.5 人机协同开发与评估 (2) / 5.3.1 性能建模、基准与调优 (1) / 3.2.4 分析驱动的理解、重构与综合 (1) / 5.1.1 故障预测与失效分析 (1) / 7.1.4 AI 支持的架构、设计与工程决策 (1) / 2.2.1 设计原则、模式与反模式 (1)
- 主题标签补充：建模/模型驱动 (17) / 经验软件工程 (10) / 需求工程 (8) / 系统软件 (8) / 维护与演化 (7)

---

### `RV`

- 基本信息：
- 全称：International Conference on Runtime Verification
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2013`
- 条目数：`61`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：运行时验证 / 监测 / 时序性质 / 工具链直接邻近
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (1) / ⏳ 待补信息 (38) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/rv_conf_c.md](./venues/rv_conf_c.md)
- 数据文件：[metadata](metadata/rv_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-rv_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.org/db/conf/rv/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-642-35632-2 / https://doi.org/10.1007/978-3-642-40787-1
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/rv_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (42) / 软件工程 (18) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (43) / 跨域但软工主导 (14) / 属于软件工程 (4)
- 初筛分布：🟢 优先跟进 (22) / 🟡 保留观察 (1) / ⏳ 待补信息 (38) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (61)
- 人工复核状态分布：未人工复核 (61)
- 高频软工主路径：3.3.2 运行时验证与运行时监测 (14) / 3.2.2 动态与混合分析 (2) / 3.2.1 静态分析与抽象解释 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：运行时监测 (25) / 待人工细分 (18) / 测试与验证 (17) / 形式化方法 (11) / 建模/模型驱动 (4)

---

### `IJSEKE`

- 基本信息：
- 全称：International Journal of Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`64`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 可补链但不稳定
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (31) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (11)
- 论文名录页：[venues/ijseke_journal_c.md](./venues/ijseke_journal_c.md)
- 数据文件：[metadata](metadata/ijseke_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ijseke_journal_c)

- 关键信息页面：
- 期刊主页：https://www.worldscientific.com/worldscinet/ijseke
- 学术索引页：http://dblp.uni-trier.de/db/journals/ijseke/index.html
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ijseke_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (46) / 跨域/待判定 (18)
- 软工纳入判定分布：属于软件工程 (46) / 不属于软件工程 (18)
- 初筛分布：🟢 优先跟进 (19) / 🟡 保留观察 (31) / ⏳ 待补信息 (3) / ⚪ 暂不跟进 (11)
- 判定来源分布：启发式初判 (64)
- 人工复核状态分布：未人工复核 (64)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (5) / 1.3.3 模型分析、仿真与验证 (4) / 1.2.1 形式化规约与契约 (4) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 1.1.1 需求获取与发现 (3) / 6.3.1 实验、案例研究与调查 (2) / 3.2.3 面向质量属性的分析 (2) / 3.1.4 场景化测试 (2)
- 主题标签补充：测试与验证 (21) / 建模/模型驱动 (21) / 形式化方法 (19) / 需求工程 (15) / 待人工细分 (12)

---

### `STTT`

- 基本信息：
- 全称：International Journal of Software Tools for Technology Transfer
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`36`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：验证工具 / formal methods tool transfer / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (20) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sttt_journal_c.md](./venues/sttt_journal_c.md)
- 数据文件：[metadata](metadata/sttt_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sttt_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10009
- 学术索引页：http://dblp.uni-trier.de/db/journals/sttt/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sttt_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (28) / 软件工程 (8)
- 软工纳入判定分布：不属于软件工程 (28) / 属于软件工程 (4) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (0) / ⏳ 待补信息 (20) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (36)
- 人工复核状态分布：未人工复核 (36)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (3) / 3.3.1 面向软工问题的形式化验证 (2) / 1.3.3 模型分析、仿真与验证 (1) / 3.2.4 分析驱动的理解、重构与综合 (1) / 6.3.1 实验、案例研究与调查 (1)
- 主题标签补充：形式化方法 (13) / 待人工细分 (13) / 建模/模型驱动 (7) / 测试与验证 (3) / 需求工程 (2)

---

### `SOCA`

- 基本信息：
- 全称：Service Oriented Computing and Applications
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`20`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务计算与应用为主
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/soca_journal_c.md](./venues/soca_journal_c.md)
- 数据文件：[metadata](metadata/soca_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-soca_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11761
- 学术索引页：http://dblp.uni-trier.de/db/journals/soca/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/soca_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (15) / 软件工程 (4) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (16) / 属于软件工程 (3) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (1) / 🟡 保留观察 (0) / ⏳ 待补信息 (19) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (20)
- 人工复核状态分布：未人工复核 (20)
- 高频软工主路径：2.1.4 云/服务/平台架构 (2) / 8.2.3 服务系统与 API 生态 (1) / 3.1.4 场景化测试 (1)
- 主题标签补充：待人工细分 (13) / 运行时监测 (2) / 系统软件 (2) / 维护与演化 (1) / 需求工程 (1)

---

### `SQJ`

- 基本信息：
- 全称：Software Quality Journal
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2013`
- 条目数：`28`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：质量 / 度量 / assurance 视角可支撑验证评价
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (1) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sqj_journal_c.md](./venues/sqj_journal_c.md)
- 数据文件：[metadata](metadata/sqj_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sqj_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11219
- 学术索引页：http://dblp.uni-trier.de/db/journals/sqj/
- 2013 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sqj_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (25) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (25) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (1) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (28)
- 人工复核状态分布：未人工复核 (28)
- 高频软工主路径：3.1.1 测试生成与增强 (10) / 6.3.1 实验、案例研究与调查 (3) / 3.2.3 面向质量属性的分析 (3) / 3.2.4 分析驱动的理解、重构与综合 (2) / 6.2.2 风险、价值与优先级 (1) / 6.2.1 估算、计划与排程 (1) / 1.1.4 需求追踪、变更与演化 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：待人工细分 (10) / 测试与验证 (6) / 建模/模型驱动 (4) / 需求工程 (3) / 维护与演化 (3)

## 7. 本年度总体观察

- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (811) / 🟡 保留观察 (1038) / ⏳ 待补信息 (1075) / ⚪ 暂不跟进 (206)
- 一级总判定分布：软件工程 (1680) / 跨域/待判定 (1060) / 程序设计语言与形式化基础 (322) / 系统软件 (68)
- 软工纳入判定分布：属于软件工程 (1605) / 不属于软件工程 (1450) / 跨域但软工主导 (75)
- 判定来源分布：启发式初判 (3130)
- 人工复核状态分布：未人工复核 (3130)
- 高频软工主路径：1.1.1 需求获取与发现 (146) / 7.1.1 代码生成、补全与变换 (120) / 6.3.1 实验、案例研究与调查 (120) / 4.1.1 缺陷修复与维护性修正 (93) / 3.1.4 场景化测试 (89) / 7.1.4 AI 支持的架构、设计与工程决策 (68) / 1.3.1 建模语言与元模型 (67) / 3.1.1 测试生成与增强 (56) / 3.2.3 面向质量属性的分析 (42) / 3.2.1 静态分析与抽象解释 (42) / 2.1.1 架构描述与恢复 (39) / 1.3.3 模型分析、仿真与验证 (39) / 1.1.4 需求追踪、变更与演化 (39) / 1.2.1 形式化规约与契约 (39) / 6.3.4 replication、benchmark 与开放科学 (39)
- 计数复核状态：以 [verification.json](./verification.json) 为准；默认要求 `expected_total == actual_total`。
- 分类终判状态：以 `metadata/*.json` 中的 `classification_source / manual_review_status / manual_review_note` 为准。
- 后续若继续扩年份或重跑年度页，建议先运行 `tools/ccf_se_index_builder.py`，再运行 `tools/ccf_se_classifier.py`。
