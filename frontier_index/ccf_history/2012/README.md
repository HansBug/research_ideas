# `2012` 年度汇总

## 1. 年份说明

- 年份：`2012`
- 覆盖范围：`CCF_SE_A_B_C.md` 当前保留的 `CCF` 软件工程高相关 venue 子集
- 当前覆盖的 venue 数量：`57`
- 当前已入表论文数量：`2932`
- 更新时间：`2026-04-07 10:36`
- 说明：本页先由 `tools/ccf_se_index_builder.py` 生成基础元数据，再由 `tools/ccf_se_classifier.py` 对未终判条目做启发式初判；若 `metadata/*.json` 中已写回人工终判，则直接保留该终判。逐篇论文名录拆分到 `venues/*.md`。

## 2. 年度汇总统计

- A 类会议：`345`
- A 类期刊：`147`
- B 类会议：`588`
- B 类期刊：`705`
- C 类会议：`1009`
- C 类期刊：`138`
- 期望总条目数：`2932`
- 实际总条目数：`2932`
- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (769) / 🟡 保留观察 (988) / ⏳ 待补信息 (962) / ⚪ 暂不跟进 (213)
- 一级总判定分布：软件工程 (1651) / 跨域/待判定 (949) / 程序设计语言与形式化基础 (263) / 系统软件 (69)
- 软工纳入判定分布：属于软件工程 (1579) / 不属于软件工程 (1281) / 跨域但软工主导 (72)
- 判定来源分布：启发式初判 (2932)
- 人工复核状态分布：未人工复核 (2932)
- 高频软工主路径：1.1.1 需求获取与发现 (119) / 7.1.1 代码生成、补全与变换 (109) / 4.1.1 缺陷修复与维护性修正 (98) / 6.3.1 实验、案例研究与调查 (94) / 3.1.4 场景化测试 (88) / 1.3.1 建模语言与元模型 (86) / 2.1.1 架构描述与恢复 (66) / 7.1.4 AI 支持的架构、设计与工程决策 (59) / 1.1.4 需求追踪、变更与演化 (49) / 3.2.3 面向质量属性的分析 (44) / 3.1.1 测试生成与增强 (42) / 3.3.1 面向软工问题的形式化验证 (37)

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
- `主体归属`、`软工归属级别`、`氛围` 与 `典型软工路径（先验）` 来自 venue 级先验；`2012` 逐篇统计直接按本年度 `metadata/*.json` 中的终判字段汇总。
- `典型软工路径（先验）` 与 `2012 高频软工主路径` 使用 [SOFTWARE_ENGINEERING_FIELD_TREE.md](../../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的方向树口径。

| venue | 全称 | 等级 | 类型 | 论文数 | 软工归属级别 | 氛围 | 主体归属 | 典型软工路径（先验） | 当年一级总判定 | 当年软工纳入 | 初筛分布 | 当年高频软工主路径 | 论文名录 | 数据文件 | 备注 |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | `A` | `会议` | 0 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 3.4.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/pldi_conf_a.md) | [metadata](metadata/pldi_conf_a.json) | 计数一致；2012 无条目，暂以先验为准 |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | `A` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/fse_conf_a.md) | [metadata](metadata/fse_conf_a.json) | 计数一致；2012 无条目，暂以先验为准 |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages, and Applications | `A` | `会议` | 0 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 3.4.x / 4.2.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/oopsla_conf_a.md) | [metadata](metadata/oopsla_conf_a.json) | 计数一致；2012 无条目，暂以先验为准 |
| `ASE / 会议 / A` | International Conference on Automated Software Engineering | `A` | `会议` | 68 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 软件工程 67 / 跨域/待判定 1 | 属于软件工程 67 / 不属于软件工程 1 | 🟢 优先跟进 (27) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6) | 7.1.1 代码生成、补全与变换 (14) / 3.4.1 调试、分诊与根因分析 (5) | [venue](venues/ase_conf_a.md) | [metadata](metadata/ase_conf_a.json) | 计数一致；2012 与先验一致 |
| `ICSE` | International Conference on Software Engineering | `A` | `会议` | 239 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 231 / 跨域/待判定 7 / 系统软件 1 | 属于软件工程 231 / 不属于软件工程 8 | 🟢 优先跟进 (74) / 🟡 保留观察 (144) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (20) | 7.1.1 代码生成、补全与变换 (50) / 1.1.1 需求获取与发现 (16) | [venue](venues/icse_conf_a.md) | [metadata](metadata/icse_conf_a.json) | 计数一致；2012 与先验一致 |
| `ISSTA` | International Symposium on Software Testing and Analysis | `A` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/issta_conf_a.md) | [metadata](metadata/issta_conf_a.json) | 计数一致；2012 无条目，暂以先验为准 |
| `FM` | International Symposium on Formal Methods | `A` | `会议` | 38 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 32 / 软件工程 6 | 不属于软件工程 32 / 跨域但软工主导 5 / 属于软件工程 1 | 🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (3) / 6.3.1 实验、案例研究与调查 (1) | [venue](venues/fm_conf_a.md) | [metadata](metadata/fm_conf_a.json) | 计数一致；2012 比先验更偏非软工 |
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | `A` | `期刊` | 19 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 17 / 跨域/待判定 1 / 程序设计语言与形式化基础 1 | 属于软件工程 17 / 不属于软件工程 2 | 🟢 优先跟进 (7) / 🟡 保留观察 (11) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 6.3.1 实验、案例研究与调查 (3) / 1.3.1 建模语言与元模型 (3) | [venue](venues/tosem_journal_a.md) | [metadata](metadata/tosem_journal_a.json) | 计数一致；2012 与先验一致 |
| `TSE` | IEEE Transactions on Software Engineering | `A` | `期刊` | 85 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x | 软件工程 80 / 跨域/待判定 4 / 系统软件 1 | 属于软件工程 80 / 不属于软件工程 5 | 🟢 优先跟进 (26) / 🟡 保留观察 (54) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5) | 7.1.1 代码生成、补全与变换 (12) / 1.1.1 需求获取与发现 (9) | [venue](venues/tse_journal_a.md) | [metadata](metadata/tse_journal_a.json) | 计数一致；2012 与先验一致 |
| `TSC` | IEEE Transactions on Services Computing | `A` | `期刊` | 43 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 5.3.x / 8.2.x | 跨域/待判定 35 / 系统软件 5 / 软件工程 2 / 程序设计语言与形式化基础 1 | 不属于软件工程 41 / 属于软件工程 2 | 🟢 优先跟进 (9) / 🟡 保留观察 (28) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (4) | 3.2.1 静态分析与抽象解释 (1) / 3.1.4 场景化测试 (1) | [venue](venues/tsc_journal_a.md) | [metadata](metadata/tsc_journal_a.json) | 计数一致；2012 比先验更偏非软工 |
| `ECOOP` | European Conference on Object-Oriented Programming | `B` | `会议` | 32 | 部分属于软工 | C 🟡 | 程序设计语言与形式化基础 | 2.2.x / 3.2.x / 4.2.x | 程序设计语言与形式化基础 26 / 软件工程 4 / 系统软件 2 | 不属于软件工程 28 / 跨域但软工主导 4 | 🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0) | 4.1.2 重构、重模块化与代码清理 (1) / 2.2.1 设计原则、模式与反模式 (1) | [venue](venues/ecoop_conf_b.md) | [metadata](metadata/ecoop_conf_b.json) | 计数一致；2012 比先验更偏非软工 |
| `ICPC` | IEEE International Conference on Program Comprehension | `B` | `会议` | 38 | 完全属于软工 | B 🟢 | 软件工程 | 4.2.x / 4.1.x / 6.5.1 | 软件工程 35 / 跨域/待判定 3 | 属于软件工程 35 / 不属于软件工程 3 | 🟢 优先跟进 (3) / 🟡 保留观察 (25) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10) | 6.5.1 开发者认知、生产力与福祉 (14) / 4.2.4 克隆、相似性与理解支持 (6) | [venue](venues/icpc_conf_b.md) | [metadata](metadata/icpc_conf_b.json) | 计数一致；2012 与先验一致 |
| `RE / 会议 / B` | IEEE International Requirements Engineering Conference | `B` | `会议` | 51 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x / 6.1.x | 软件工程 50 / 跨域/待判定 1 | 属于软件工程 50 / 不属于软件工程 1 | 🟢 优先跟进 (45) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 1.1.1 需求获取与发现 (16) / 1.1.4 需求追踪、变更与演化 (5) | [venue](venues/re_conf_b.md) | [metadata](metadata/re_conf_b.json) | 计数一致；2012 与先验一致 |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | `B` | `会议` | 48 | 部分属于软工 | B 🟢 | 信息系统工程与软件工程交叉 | 1.3.x / 2.1.x / 4.3.x / 8.3.x | 跨域/待判定 37 / 软件工程 11 | 不属于软件工程 37 / 跨域但软工主导 6 / 属于软件工程 5 | 🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (45) / ⚪ 暂不跟进 (0) | 6.1.1 敏捷、精益与 DevOps 方法 (2) / 6.3.1 实验、案例研究与调查 (2) | [venue](venues/caise_conf_b.md) | [metadata](metadata/caise_conf_b.json) | 计数一致；2012 比先验更偏非软工 |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | `B` | `会议` | 51 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 33 / 跨域/待判定 18 | 属于软件工程 33 / 不属于软件工程 18 | 🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (41) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (14) / 1.3.2 模型转换、同步与协同 (2) | [venue](venues/models_conf_b.md) | [metadata](metadata/models_conf_b.json) | 计数一致；2012 比先验更偏非软工 |
| `ICSOC` | International Conference on Service Oriented Computing | `B` | `会议` | 62 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 60 / 软件工程 2 | 不属于软件工程 60 / 属于软件工程 2 | 🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (59) / ⚪ 暂不跟进 (0) | 8.2.3 服务系统与 API 生态 (1) / 2.1.4 云/服务/平台架构 (1) | [venue](venues/icsoc_conf_b.md) | [metadata](metadata/icsoc_conf_b.json) | 计数一致；2012 比先验更偏非软工 |
| `SANER` | IEEE International Conference on Software Analysis, Evolution, and Reengineering | `B` | `会议` | 0 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 3.2.x / 3.4.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/saner_conf_b.md) | [metadata](metadata/saner_conf_b.json) | 计数一致；2012 无条目，暂以先验为准 |
| `ICSME` | International Conference on Software Maintenance and Evolution | `B` | `会议` | 84 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.2.x / 4.3.x / 6.4.x | 软件工程 79 / 跨域/待判定 5 | 属于软件工程 79 / 不属于软件工程 5 | 🟢 优先跟进 (20) / 🟡 保留观察 (54) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10) | 4.1.1 缺陷修复与维护性修正 (26) / 1.1.4 需求追踪、变更与演化 (9) | [venue](venues/icsme_conf_b.md) | [metadata](metadata/icsme_conf_b.json) | 计数一致；2012 与先验一致 |
| `VMCAI` | International Conference on Verification, Model Checking, and Abstract Interpretation | `B` | `会议` | 29 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 23 / 软件工程 5 / 系统软件 1 | 不属于软件工程 24 / 跨域但软工主导 3 / 属于软件工程 2 | 🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (3) / 3.2.1 静态分析与抽象解释 (2) | [venue](venues/vmcai_conf_b.md) | [metadata](metadata/vmcai_conf_b.json) | 计数一致；2012 比先验更偏非软工 |
| `ICWS` | IEEE International Conference on Web Services | `B` | `会议` | 110 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 5.3.x / 8.2.3 | 跨域/待判定 95 / 系统软件 8 / 软件工程 7 | 不属于软件工程 103 / 属于软件工程 6 / 跨域但软工主导 1 | 🟢 优先跟进 (33) / 🟡 保留观察 (47) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (30) | 2.1.4 云/服务/平台架构 (2) / 8.2.3 服务系统与 API 生态 (1) | [venue](venues/icws_conf_b.md) | [metadata](metadata/icws_conf_b.json) | 计数一致；2012 比先验更偏非软工 |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | `B` | `会议` | 45 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 40 / 跨域/待判定 5 | 属于软件工程 40 / 不属于软件工程 5 | 🟢 优先跟进 (8) / 🟡 保留观察 (29) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8) | 4.1.1 缺陷修复与维护性修正 (10) / 6.3.1 实验、案例研究与调查 (9) | [venue](venues/esem_conf_b.md) | [metadata](metadata/esem_conf_b.json) | 计数一致；2012 与先验一致 |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | `B` | `会议` | 38 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x / 5.2.x / 4.4.x | 软件工程 38 | 属于软件工程 38 | 🟢 优先跟进 (8) / 🟡 保留观察 (30) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.3.3 assurance、认证与合规验证 (8) / 3.1.4 场景化测试 (5) | [venue](venues/issre_conf_b.md) | [metadata](metadata/issre_conf_b.json) | 计数一致；2012 与先验一致 |
| `ASE / 期刊 / B` | Automated Software Engineering | `B` | `期刊` | 18 | 完全属于软工 | A 🔥 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x | 跨域/待判定 11 / 软件工程 7 | 不属于软件工程 11 / 属于软件工程 7 | 🟢 优先跟进 (4) / 🟡 保留观察 (1) / ⏳ 待补信息 (13) / ⚪ 暂不跟进 (0) | 7.1.1 代码生成、补全与变换 (2) / 1.3.3 模型分析、仿真与验证 (2) | [venue](venues/ase_journal_b.md) | [metadata](metadata/ase_journal_b.json) | 计数一致；2012 比先验更偏非软工 |
| `ESE` | Empirical Software Engineering | `B` | `期刊` | 27 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 24 / 跨域/待判定 2 / 系统软件 1 | 属于软件工程 24 / 不属于软件工程 3 | 🟢 优先跟进 (2) / 🟡 保留观察 (2) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0) | 4.1.1 缺陷修复与维护性修正 (7) / 3.2.3 面向质量属性的分析 (3) | [venue](venues/ese_journal_b.md) | [metadata](metadata/ese_journal_b.json) | 计数一致；2012 与先验一致 |
| `IETS` | IET Software | `B` | `期刊` | 51 | 大部分属于软工 | C 🟡 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 5.x.x | 软件工程 36 / 跨域/待判定 14 / 程序设计语言与形式化基础 1 | 属于软件工程 36 / 不属于软件工程 15 | 🟢 优先跟进 (16) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9) | 3.1.4 场景化测试 (7) / 1.1.1 需求获取与发现 (5) | [venue](venues/iets_journal_b.md) | [metadata](metadata/iets_journal_b.json) | 计数一致；2012 与先验一致 |
| `IST` | Information and Software Technology | `B` | `期刊` | 93 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 跨域/待判定 47 / 软件工程 44 / 系统软件 2 | 不属于软件工程 49 / 属于软件工程 44 | 🟢 优先跟进 (16) / 🟡 保留观察 (2) / ⏳ 待补信息 (75) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (9) / 6.3.1 实验、案例研究与调查 (7) | [venue](venues/ist_journal_b.md) | [metadata](metadata/ist_journal_b.json) | 计数一致；2012 比先验更偏非软工 |
| `JSEP` | Journal of Software: Evolution and Process | `B` | `期刊` | 57 | 完全属于软工 | B 🟢 | 软件工程 | 4.1.x / 4.3.x / 6.1.x / 6.4.x | 软件工程 54 / 跨域/待判定 2 / 系统软件 1 | 属于软件工程 54 / 不属于软件工程 3 | 🟢 优先跟进 (17) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5) | 4.1.1 缺陷修复与维护性修正 (11) / 6.1.2 过程挖掘、符合性与改进 (8) | [venue](venues/jsep_journal_b.md) | [metadata](metadata/jsep_journal_b.json) | 计数一致；2012 与先验一致 |
| `JSS` | Journal of Systems and Software | `B` | `期刊` | 220 | 大部分属于软工 | B 🟢 | 软件工程 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 153 / 软件工程 62 / 系统软件 5 | 不属于软件工程 158 / 属于软件工程 62 | 🟢 优先跟进 (12) / 🟡 保留观察 (0) / ⏳ 待补信息 (207) / ⚪ 暂不跟进 (1) | 2.1.1 架构描述与恢复 (26) / 6.1.1 敏捷、精益与 DevOps 方法 (5) | [venue](venues/jss_journal_b.md) | [metadata](metadata/jss_journal_b.json) | 计数一致；2012 比先验更偏非软工 |
| `RE / 期刊 / B` | Requirements Engineering | `B` | `期刊` | 19 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 16 / 跨域/待判定 3 | 属于软件工程 16 / 不属于软件工程 3 | 🟢 优先跟进 (12) / 🟡 保留观察 (1) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (12) / 6.3.1 实验、案例研究与调查 (2) | [venue](venues/re_journal_b.md) | [metadata](metadata/re_journal_b.json) | 计数一致；2012 与先验一致 |
| `SCP` | Science of Computer Programming | `B` | `期刊` | 78 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 1.2.x / 3.2.x / 3.3.x / 4.1.x | 程序设计语言与形式化基础 65 / 软件工程 12 / 系统软件 1 | 不属于软件工程 66 / 属于软件工程 8 / 跨域但软工主导 4 | 🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (65) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (7) / 4.1.3 API、依赖与库演化 (1) | [venue](venues/scp_journal_b.md) | [metadata](metadata/scp_journal_b.json) | 计数一致；2012 比先验更偏非软工 |
| `SoSyM` | Software and Systems Modeling | `B` | `期刊` | 44 | 大部分属于软工 | A 🔥 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.1.x | 软件工程 22 / 跨域/待判定 21 / 程序设计语言与形式化基础 1 | 属于软件工程 22 / 不属于软件工程 22 | 🟢 优先跟进 (4) / 🟡 保留观察 (2) / ⏳ 待补信息 (38) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (13) / 2.2.1 设计原则、模式与反模式 (2) | [venue](venues/sosym_journal_b.md) | [metadata](metadata/sosym_journal_b.json) | 计数一致；2012 比先验更偏非软工 |
| `STVR` | Software Testing, Verification and Reliability | `B` | `期刊` | 27 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.3.x / 5.1.x | 软件工程 26 / 跨域/待判定 1 | 属于软件工程 26 / 不属于软件工程 1 | 🟢 优先跟进 (13) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0) | 3.1.1 测试生成与增强 (5) / 3.1.4 场景化测试 (4) | [venue](venues/stvr_journal_b.md) | [metadata](metadata/stvr_journal_b.json) | 计数一致；2012 与先验一致 |
| `SPE` | Software: Practice and Experience | `B` | `期刊` | 71 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.3.x / 4.3.x / 4.4.x / 6.3.x / 8.2.x | 跨域/待判定 41 / 系统软件 13 / 软件工程 10 / 程序设计语言与形式化基础 7 | 不属于软件工程 61 / 属于软件工程 9 / 跨域但软工主导 1 | 🟢 优先跟进 (20) / 🟡 保留观察 (36) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (14) | 1.3.1 建模语言与元模型 (2) / 6.3.1 实验、案例研究与调查 (1) | [venue](venues/spe_journal_b.md) | [metadata](metadata/spe_journal_b.json) | 计数一致；2012 比先验更偏非软工 |
| `PASTE` | ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | `C` | `会议` | 0 | 部分属于软工 | B 🟢 | 程序设计语言与形式化基础 | 3.2.x / 3.4.x / 4.2.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/paste_conf_c.md) | [metadata](metadata/paste_conf_c.json) | 计数一致；2012 无条目，暂以先验为准 |
| `APSEC` | Asia-Pacific Software Engineering Conference | `C` | `会议` | 122 | 大部分属于软工 | B 🟢 | 软件工程 | 1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x | 软件工程 96 / 跨域/待判定 24 / 系统软件 2 | 属于软件工程 96 / 不属于软件工程 26 | 🟢 优先跟进 (51) / 🟡 保留观察 (58) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (13) | 1.1.1 需求获取与发现 (13) / 7.1.1 代码生成、补全与变换 (13) | [venue](venues/apsec_conf_c.md) | [metadata](metadata/apsec_conf_c.json) | 计数一致；2012 与先验一致 |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | `C` | `会议` | 38 | 完全属于软工 | B 🟢 | 软件工程 | 6.3.x / 6.4.x / 6.5.x / 4.1.x | 软件工程 36 / 跨域/待判定 2 | 属于软件工程 36 / 不属于软件工程 2 | 🟢 优先跟进 (12) / 🟡 保留观察 (22) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (3) | 6.3.1 实验、案例研究与调查 (9) / 6.3.3 系统综述、mapping 与 meta-analysis (5) | [venue](venues/ease_conf_c.md) | [metadata](metadata/ease_conf_c.json) | 计数一致；2012 与先验一致 |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | `C` | `会议` | 38 | 部分属于软工 | B 🟢 | 软件工程与系统建模交叉 | 1.3.x / 2.1.x / 3.3.x / 8.3.x | 跨域/待判定 28 / 软件工程 8 / 系统软件 2 | 不属于软件工程 30 / 属于软件工程 8 | 🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (31) / ⚪ 暂不跟进 (0) | 1.3.1 建模语言与元模型 (7) / 1.1.1 需求获取与发现 (1) | [venue](venues/iceccs_conf_c.md) | [metadata](metadata/iceccs_conf_c.json) | 计数一致；2012 比先验更偏非软工 |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | `C` | `会议` | 127 | 完全属于软工 | A 🔥 | 软件工程 | 3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x | 软件工程 125 / 跨域/待判定 1 / 程序设计语言与形式化基础 1 | 属于软件工程 125 / 不属于软件工程 2 | 🟢 优先跟进 (49) / 🟡 保留观察 (76) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2) | 3.1.4 场景化测试 (21) / 3.1.1 测试生成与增强 (17) | [venue](venues/icst_conf_c.md) | [metadata](metadata/icst_conf_c.json) | 计数一致；2012 与先验一致 |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | `C` | `会议` | 22 | 大部分属于软工 | B 🟢 | 软件工程 | 3.2.x / 4.2.x / 4.1.x / 3.4.x | 软件工程 19 / 跨域/待判定 2 / 程序设计语言与形式化基础 1 | 属于软件工程 19 / 不属于软件工程 3 | 🟢 优先跟进 (5) / 🟡 保留观察 (16) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1) | 3.2.3 面向质量属性的分析 (3) / 3.2.1 静态分析与抽象解释 (3) | [venue](venues/scam_conf_c.md) | [metadata](metadata/scam_conf_c.json) | 计数一致；2012 与先验一致 |
| `COMPSAC` | International Computer Software and Applications Conference | `C` | `会议` | 111 | 部分属于软工 | C 🟡 | 软件工程与系统软件交叉 | 2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x | 跨域/待判定 73 / 软件工程 32 / 系统软件 5 / 程序设计语言与形式化基础 1 | 不属于软件工程 79 / 属于软件工程 26 / 跨域但软工主导 6 | 🟢 优先跟进 (35) / 🟡 保留观察 (58) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18) | 2.1.1 架构描述与恢复 (5) / 3.1.4 场景化测试 (4) | [venue](venues/compsac_conf_c.md) | [metadata](metadata/compsac_conf_c.json) | 计数一致；2012 与先验一致 |
| `ICFEM` | International Conference on Formal Engineering Methods | `C` | `会议` | 34 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x | 程序设计语言与形式化基础 26 / 软件工程 8 | 不属于软件工程 26 / 跨域但软工主导 6 / 属于软件工程 2 | 🟢 优先跟进 (9) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0) | 1.2.1 形式化规约与契约 (4) / 1.3.3 模型分析、仿真与验证 (2) | [venue](venues/icfem_conf_c.md) | [metadata](metadata/icfem_conf_c.json) | 计数一致；2012 比先验更偏非软工 |
| `SSE` | IEEE International Conference on Software Services Engineering | `C` | `会议` | 101 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.3 | 跨域/待判定 78 / 软件工程 11 / 系统软件 10 / 程序设计语言与形式化基础 2 | 不属于软件工程 90 / 属于软件工程 10 / 跨域但软工主导 1 | 🟢 优先跟进 (33) / 🟡 保留观察 (46) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (22) | 2.1.4 云/服务/平台架构 (6) / 8.2.3 服务系统与 API 生态 (2) | [venue](venues/sse_conf_c.md) | [metadata](metadata/sse_conf_c.json) | 计数一致；2012 比先验更偏非软工 |
| `ICSSP` | International Conference on Software and System Process | `C` | `会议` | 37 | 完全属于软工 | C 🟡 | 软件工程 | 6.1.x / 6.2.x / 6.5.x | 软件工程 36 / 跨域/待判定 1 | 属于软件工程 36 / 不属于软件工程 1 | 🟢 优先跟进 (9) / 🟡 保留观察 (23) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5) | 1.3.3 模型分析、仿真与验证 (9) / 6.1.1 敏捷、精益与 DevOps 方法 (6) | [venue](venues/icssp_conf_c.md) | [metadata](metadata/icssp_conf_c.json) | 计数一致；2012 与先验一致 |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | `C` | `会议` | 143 | 部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 跨域/待判定 111 / 软件工程 32 | 不属于软件工程 111 / 属于软件工程 21 / 跨域但软工主导 11 | 🟢 优先跟进 (18) / 🟡 保留观察 (0) / ⏳ 待补信息 (125) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (12) / 6.3.1 实验、案例研究与调查 (3) | [venue](venues/seke_conf_c.md) | [metadata](metadata/seke_conf_c.json) | 计数一致；2012 比先验更偏非软工 |
| `QRS` | International Conference on Software Quality, Reliability and Security | `C` | `会议` | 0 | 完全属于软工 | A 🔥 | 软件工程 | 3.x.x / 5.1.x / 5.2.x / 4.4.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/qrs_conf_c.md) | [metadata](metadata/qrs_conf_c.json) | 计数一致；2012 无条目，暂以先验为准 |
| `ICSR` | International Conference on Software Reuse | `C` | `会议` | 0 | 完全属于软工 | C 🟡 | 软件工程 | 1.4.x / 2.3.x / 4.1.x / 4.3.x | 无 2012 条目 | 无 2012 条目 | 无 2012 条目 | 无纳入软工主路径 | [venue](venues/icsr_conf_c.md) | [metadata](metadata/icsr_conf_c.json) | 计数一致；2012 无条目，暂以先验为准 |
| `SPIN` | International Symposium on Model Checking of Software | `C` | `会议` | 20 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 1.2.x / 1.3.x / 3.3.x | 软件工程 11 / 程序设计语言与形式化基础 9 | 不属于软件工程 9 / 属于软件工程 7 / 跨域但软工主导 4 | 🟢 优先跟进 (9) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (4) / 1.3.3 模型分析、仿真与验证 (4) | [venue](venues/spin_conf_c.md) | [metadata](metadata/spin_conf_c.json) | 计数一致；2012 与先验一致 |
| `TASE` | Theoretical Aspects of Software Engineering Conference | `C` | `会议` | 42 | 部分属于软工 | B 🟢 | 形式化方法与软件工程交叉 | 1.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 22 / 软件工程 15 / 系统软件 5 | 不属于软件工程 27 / 属于软件工程 13 / 跨域但软工主导 2 | 🟢 优先跟进 (27) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 3.3.1 面向软工问题的形式化验证 (5) / 1.2.1 形式化规约与契约 (2) | [venue](venues/tase_conf_c.md) | [metadata](metadata/tase_conf_c.json) | 计数一致；2012 与先验一致 |
| `MSR` | Mining Software Repositories | `C` | `会议` | 38 | 完全属于软工 | B 🟢 | 软件工程 | 6.4.x / 6.3.x / 4.1.x / 6.5.x | 软件工程 35 / 跨域/待判定 3 | 属于软件工程 35 / 不属于软件工程 3 | 🟢 优先跟进 (4) / 🟡 保留观察 (31) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3) | 3.2.3 面向质量属性的分析 (5) / 6.3.1 实验、案例研究与调查 (5) | [venue](venues/msr_conf_c.md) | [metadata](metadata/msr_conf_c.json) | 计数一致；2012 与先验一致 |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | `C` | `会议` | 27 | 完全属于软工 | A 🔥 | 软件工程 | 1.1.x / 1.2.x / 1.4.x | 软件工程 20 / 跨域/待判定 7 | 属于软件工程 20 / 不属于软件工程 7 | 🟢 优先跟进 (18) / 🟡 保留观察 (0) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (0) | 1.1.1 需求获取与发现 (11) / 1.1.4 需求追踪、变更与演化 (2) | [venue](venues/refsq_conf_c.md) | [metadata](metadata/refsq_conf_c.json) | 计数一致；2012 与先验一致 |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | `C` | `会议` | 48 | 完全属于软工 | B 🟢 | 软件工程 | 2.1.x / 2.2.x / 4.1.x | 软件工程 47 / 跨域/待判定 1 | 属于软件工程 47 / 不属于软件工程 1 | 🟢 优先跟进 (12) / 🟡 保留观察 (28) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8) | 2.1.1 架构描述与恢复 (18) / 7.1.4 AI 支持的架构、设计与工程决策 (8) | [venue](venues/wicsa_conf_c.md) | [metadata](metadata/wicsa_conf_c.json) | 计数一致；2012 与先验一致 |
| `Internetware` | Asia-Pacific Symposium on Internetware | `C` | `会议` | 26 | 大部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.3.x / 4.4.x / 8.2.x | 软件工程 20 / 跨域/待判定 5 / 系统软件 1 | 属于软件工程 20 / 不属于软件工程 6 | 🟢 优先跟进 (8) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4) | 2.1.4 云/服务/平台架构 (11) / 7.1.4 AI 支持的架构、设计与工程决策 (3) | [venue](venues/internetware_conf_c.md) | [metadata](metadata/internetware_conf_c.json) | 计数一致；2012 与先验一致 |
| `RV` | International Conference on Runtime Verification | `C` | `会议` | 35 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.3.2 / 4.4.4 / 5.1.x | 程序设计语言与形式化基础 20 / 软件工程 14 / 系统软件 1 | 不属于软件工程 21 / 跨域但软工主导 12 / 属于软件工程 2 | 🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0) | 3.3.2 运行时验证与运行时监测 (11) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) | [venue](venues/rv_conf_c.md) | [metadata](metadata/rv_conf_c.json) | 计数一致；2012 与先验一致 |
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | `C` | `期刊` | 49 | 大部分属于软工 | C 🟡 | 软件工程与知识工程交叉 | 1.x.x / 2.x.x / 3.x.x / 7.1.x | 软件工程 34 / 跨域/待判定 13 / 系统软件 2 | 属于软件工程 34 / 不属于软件工程 15 | 🟢 优先跟进 (16) / 🟡 保留观察 (21) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (7) | 3.1.4 场景化测试 (7) / 1.1.1 需求获取与发现 (3) | [venue](venues/ijseke_journal_c.md) | [metadata](metadata/ijseke_journal_c.json) | 计数一致；2012 比先验更偏非软工 |
| `STTT` | International Journal of Software Tools for Technology Transfer | `C` | `期刊` | 37 | 部分属于软工 | A 🔥 | 形式化方法与软件工程交叉 | 3.2.x / 3.3.x / 5.1.x | 程序设计语言与形式化基础 24 / 软件工程 13 | 不属于软件工程 24 / 属于软件工程 8 / 跨域但软工主导 5 | 🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (24) / ⚪ 暂不跟进 (0) | 3.3.1 面向软工问题的形式化验证 (8) / 3.3.2 运行时验证与运行时监测 (3) | [venue](venues/sttt_journal_c.md) | [metadata](metadata/sttt_journal_c.json) | 计数一致；2012 与先验一致 |
| `SOCA` | Service Oriented Computing and Applications | `C` | `期刊` | 27 | 部分属于软工 | C 🟡 | 软件工程与服务系统工程交叉 | 2.1.4 / 4.4.x / 8.2.3 | 跨域/待判定 25 / 软件工程 2 | 不属于软件工程 25 / 属于软件工程 1 / 跨域但软工主导 1 | 🟢 优先跟进 (0) / 🟡 保留观察 (1) / ⏳ 待补信息 (26) / ⚪ 暂不跟进 (0) | 7.1.1 代码生成、补全与变换 (1) / 3.3.2 运行时验证与运行时监测 (1) | [venue](venues/soca_journal_c.md) | [metadata](metadata/soca_journal_c.json) | 计数一致；2012 比先验更偏非软工 |
| `SQJ` | Software Quality Journal | `C` | `期刊` | 25 | 完全属于软工 | B 🟢 | 软件工程 | 5.x.x / 3.x.x / 6.3.x | 软件工程 17 / 跨域/待判定 8 | 属于软件工程 17 / 不属于软件工程 8 | 🟢 优先跟进 (2) / 🟡 保留观察 (1) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0) | 3.1.1 测试生成与增强 (9) / 1.4.1 特征建模与配置 (2) | [venue](venues/sqj_journal_c.md) | [metadata](metadata/sqj_journal_c.json) | 计数一致；2012 比先验更偏非软工 |

## 6. Venue 导航

---

### `PLDI`

- 基本信息：
- 全称：ACM SIGPLAN Conference on Programming Language Design and Implementation
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：程序分析 / 软件验证 / repair 邻近但需严格筛选
- 初筛分布：无 2012 条目
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
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE + `LLM/需求建模/测试验证/修复` 主线
- 初筛分布：无 2012 条目
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
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件结构 / 程序分析 / 重构与验证偶发贴题
- 初筛分布：无 2012 条目
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
- 年份：`2012`
- 条目数：`68`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 论文名录页：[venues/ase_conf_a.md](./venues/ase_conf_a.md)
- 数据文件：[metadata](metadata/ase_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/ase-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/kbse/
- 官方论文集页：http://dl.acm.org/citation.cfm?id=2351676
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ase_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (67) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (67) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (6)
- 判定来源分布：启发式初判 (68)
- 人工复核状态分布：未人工复核 (68)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (14) / 3.4.1 调试、分诊与根因分析 (5) / 2.2.1 设计原则、模式与反模式 (4) / 4.1.1 缺陷修复与维护性修正 (3) / 3.1.4 场景化测试 (3) / 7.1.2 AI 支持的测试、分析与修复 (3) / 3.1.1 测试生成与增强 (3) / 1.2.1 形式化规约与契约 (2)
- 主题标签补充：测试与验证 (23) / 维护与演化 (21) / 建模/模型驱动 (19) / 经验软件工程 (16) / 需求工程 (15)

---

### `ICSE`

- 基本信息：
- 全称：International Conference on Software Engineering
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2012`
- 条目数：`239`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主会，需求-建模-验证-修复全链可见
- 初筛分布：🟢 优先跟进 (74) / 🟡 保留观察 (144) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (20)
- 论文名录页：[venues/icse_conf_a.md](./venues/icse_conf_a.md)
- 数据文件：[metadata](metadata/icse_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icse_conf_a)

- 关键信息页面：
- 年主页：https://conf.researchr.org/home/icse-2025
- 学术索引页：http://dblp.uni-trier.de/db/conf/icse/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6218989/proceeding / https://www.computer.org/csdl/proceedings/icse/2012/1066/00/index.html / http://dl.acm.org/citation.cfm?id=2337223
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icse_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (231) / 跨域/待判定 (7) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (231) / 不属于软件工程 (8)
- 初筛分布：🟢 优先跟进 (74) / 🟡 保留观察 (144) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (20)
- 判定来源分布：启发式初判 (239)
- 人工复核状态分布：未人工复核 (239)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (50) / 1.1.1 需求获取与发现 (16) / 3.1.4 场景化测试 (12) / 7.1.4 AI 支持的架构、设计与工程决策 (11) / 6.3.1 实验、案例研究与调查 (10) / 1.1.4 需求追踪、变更与演化 (8) / 2.2.1 设计原则、模式与反模式 (8) / 4.1.1 缺陷修复与维护性修正 (7)
- 主题标签补充：维护与演化 (79) / 经验软件工程 (76) / 建模/模型驱动 (63) / 测试与验证 (60) / 可靠性/安全 (55)

---

### `ISSTA`

- 基本信息：
- 全称：International Symposium on Software Testing and Analysis
- `CCF` 等级：`A`
- 类型：`会议`
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试分析 / 形式化验证 / 缺陷定位与修复主场
- 初筛分布：无 2012 条目
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
- 年份：`2012`
- 条目数：`38`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：形式化方法 / timed automata / 工业与控制系统验证邻近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/fm_conf_a.md](./venues/fm_conf_a.md)
- 数据文件：[metadata](metadata/fm_conf_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-fm_conf_a)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/fm/
- 官方论文集页：https://doi.org/10.1007/978-3-642-32759-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/fm_conf_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (32) / 软件工程 (6)
- 软工纳入判定分布：不属于软件工程 (32) / 跨域但软工主导 (5) / 属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (0) / ⏳ 待补信息 (30) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (38)
- 人工复核状态分布：未人工复核 (38)
- 高频软工主路径：1.2.1 形式化规约与契约 (3) / 6.3.1 实验、案例研究与调查 (1) / 1.3.1 建模语言与元模型 (1) / 1.3.3 模型分析、仿真与验证 (1)
- 主题标签补充：待人工细分 (18) / 形式化方法 (11) / 测试与验证 (7) / 建模/模型驱动 (3) / 运行时监测 (2)

---

### `TOSEM`

- 基本信息：
- 全称：ACM Transactions on Software Engineering and Methodology
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`19`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件工程方法 / 需求建模 / 测试验证 / `AI for SE`
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (11) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/tosem_journal_a.md](./venues/tosem_journal_a.md)
- 数据文件：[metadata](metadata/tosem_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tosem_journal_a)

- 关键信息页面：
- 期刊主页：https://dl.acm.org/journal/tosem
- 学术索引页：http://dblp.uni-trier.de/db/journals/tosem/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tosem_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (17) / 跨域/待判定 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (17) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (11) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (19)
- 人工复核状态分布：未人工复核 (19)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (3) / 1.3.1 建模语言与元模型 (3) / 2.2.2 模块化、依赖与解耦 (2) / 1.1.1 需求获取与发现 (2) / 4.1.2 重构、重模块化与代码清理 (1) / 1.3.3 模型分析、仿真与验证 (1) / 3.1.4 场景化测试 (1) / 3.4.1 调试、分诊与根因分析 (1)
- 主题标签补充：形式化方法 (14) / 测试与验证 (9) / 建模/模型驱动 (6) / 需求工程 (4) / 可靠性/安全 (4)

---

### `TSE`

- 基本信息：
- 全称：IEEE Transactions on Software Engineering
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`85`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：broad SE 主刊 / 建模验证修复与 `LLM` 子题持续出现
- 初筛分布：🟢 优先跟进 (26) / 🟡 保留观察 (54) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/tse_journal_a.md](./venues/tse_journal_a.md)
- 数据文件：[metadata](metadata/tse_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tse_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32
- 学术索引页：http://dblp.uni-trier.de/db/journals/tse/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tse_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (80) / 跨域/待判定 (4) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (80) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (26) / 🟡 保留观察 (54) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (85)
- 人工复核状态分布：未人工复核 (85)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (12) / 1.1.1 需求获取与发现 (9) / 1.3.1 建模语言与元模型 (6) / 4.1.2 重构、重模块化与代码清理 (5) / 7.1.4 AI 支持的架构、设计与工程决策 (4) / 6.2.1 估算、计划与排程 (4) / 4.1.1 缺陷修复与维护性修正 (3) / 3.3.2 运行时验证与运行时监测 (3)
- 主题标签补充：测试与验证 (38) / 经验软件工程 (26) / 建模/模型驱动 (22) / 需求工程 (20) / 维护与演化 (18)

---

### `TSC`

- 基本信息：
- 全称：IEEE Transactions on Services Computing
- `CCF` 等级：`A`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`43`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务工作流 / 平台 orchestration 邻近，可补性质工程
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (28) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/tsc_journal_a.md](./venues/tsc_journal_a.md)
- 数据文件：[metadata](metadata/tsc_journal_a.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tsc_journal_a)

- 关键信息页面：
- 期刊主页：https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=4629386
- 学术索引页：http://dblp.uni-trier.de/db/journals/tsc/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/tsc_journal_a.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (35) / 系统软件 (5) / 软件工程 (2) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (41) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (28) / ⏳ 待补信息 (2) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (43)
- 人工复核状态分布：未人工复核 (43)
- 高频软工主路径：3.2.1 静态分析与抽象解释 (1) / 3.1.4 场景化测试 (1)
- 主题标签补充：建模/模型驱动 (19) / 系统软件 (12) / 可靠性/安全 (12) / 形式化方法 (10) / 维护与演化 (8)

---

### `ECOOP`

- 基本信息：
- 全称：European Conference on Object-Oriented Programming
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`32`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`OO` 程序结构 / 分析与重构邻近
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ecoop_conf_b.md](./venues/ecoop_conf_b.md)
- 数据文件：[metadata](metadata/ecoop_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ecoop_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ecoop/
- 官方论文集页：https://doi.org/10.1007/978-3-642-31057-7
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ecoop_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (26) / 软件工程 (4) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (28) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (0) / ⏳ 待补信息 (32) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (32)
- 人工复核状态分布：未人工复核 (32)
- 高频软工主路径：4.1.2 重构、重模块化与代码清理 (1) / 2.2.1 设计原则、模式与反模式 (1) / 2.2.2 模块化、依赖与解耦 (1) / 3.2.1 静态分析与抽象解释 (1)
- 主题标签补充：待人工细分 (22) / 程序分析 (3) / 维护与演化 (2) / 程序设计语言/编译 (2) / 系统软件 (1)

---

### `ICPC`

- 基本信息：
- 全称：IEEE International Conference on Program Comprehension
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`38`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序理解 / 缺陷分析 / 修复解释与人因辅助
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (25) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10)
- 论文名录页：[venues/icpc_conf_b.md](./venues/icpc_conf_b.md)
- 数据文件：[metadata](metadata/icpc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icpc_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/iwpc/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6230782/proceeding / https://www.computer.org/csdl/proceedings/icpc/2012/1213/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icpc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (35) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (35) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (25) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10)
- 判定来源分布：启发式初判 (38)
- 人工复核状态分布：未人工复核 (38)
- 高频软工主路径：6.5.1 开发者认知、生产力与福祉 (14) / 4.2.4 克隆、相似性与理解支持 (6) / 4.1.1 缺陷修复与维护性修正 (3) / 1.3.1 建模语言与元模型 (2) / 1.1.4 需求追踪、变更与演化 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 2.1.1 架构描述与恢复 (1) / 2.2.2 模块化、依赖与解耦 (1)
- 主题标签补充：经验软件工程 (17) / 维护与演化 (14) / 建模/模型驱动 (9) / 待人工细分 (9) / 形式化方法 (5)

---

### `RE / 会议 / B`

- 基本信息：
- 全称：IEEE International Requirements Engineering Conference
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`51`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (45) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/re_conf_b.md](./venues/re_conf_b.md)
- 数据文件：[metadata](metadata/re_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/re/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6336974/proceeding / http://www.computer.org/csdl/proceedings/re/2012/2783/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/re_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (50) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (50) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (45) / 🟡 保留观察 (5) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (51)
- 人工复核状态分布：未人工复核 (51)
- 高频软工主路径：1.1.1 需求获取与发现 (16) / 1.1.4 需求追踪、变更与演化 (5) / 1.4.1 特征建模与配置 (4) / 1.1.2 需求分析、协商与优先级 (4) / 6.3.1 实验、案例研究与调查 (4) / 3.1.4 场景化测试 (2) / 1.2.3 规约质量与一致性 (2) / 5.2.4 公平性、问责与法规符合 (2)
- 主题标签补充：需求工程 (45) / 建模/模型驱动 (20) / 维护与演化 (13) / 测试与验证 (6) / 经验软件工程 (6)

---

### `CAiSE`

- 基本信息：
- 全称：International Conference on Advanced Information Systems Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`48`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：信息系统与过程/模型工程，适合补需求-建模-规约链
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (45) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/caise_conf_b.md](./venues/caise_conf_b.md)
- 数据文件：[metadata](metadata/caise_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-caise_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/caise/
- 官方论文集页：https://doi.org/10.1007/978-3-642-31095-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/caise_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (37) / 软件工程 (11)
- 软工纳入判定分布：不属于软件工程 (37) / 跨域但软工主导 (6) / 属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (45) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (48)
- 人工复核状态分布：未人工复核 (48)
- 高频软工主路径：6.1.1 敏捷、精益与 DevOps 方法 (2) / 6.3.1 实验、案例研究与调查 (2) / 1.4.1 特征建模与配置 (2) / 1.3.2 模型转换、同步与协同 (1) / 7.1.1 代码生成、补全与变换 (1) / 1.3.1 建模语言与元模型 (1) / 3.4.1 调试、分诊与根因分析 (1) / 4.1.2 重构、重模块化与代码清理 (1)
- 主题标签补充：待人工细分 (21) / 建模/模型驱动 (18) / 测试与验证 (4) / 形式化方法 (4) / 需求工程 (3)

---

### `MoDELS`

- 基本信息：
- 全称：ACM/IEEE International Conference on Model Driven Engineering Languages and Systems
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`51`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：模型驱动 / 状态机-SysML / 形式化建模主场
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (41) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/models_conf_b.md](./venues/models_conf_b.md)
- 数据文件：[metadata](metadata/models_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-models_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/models/
- 官方论文集页：https://doi.org/10.1007/978-3-642-33666-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/models_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (33) / 跨域/待判定 (18)
- 软工纳入判定分布：属于软件工程 (33) / 不属于软件工程 (18)
- 初筛分布：🟢 优先跟进 (10) / 🟡 保留观察 (0) / ⏳ 待补信息 (41) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (51)
- 人工复核状态分布：未人工复核 (51)
- 高频软工主路径：1.3.1 建模语言与元模型 (14) / 1.3.2 模型转换、同步与协同 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 6.3.1 实验、案例研究与调查 (2) / 7.1.1 代码生成、补全与变换 (2) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 3.3.2 运行时验证与运行时监测 (1) / 3.1.1 测试生成与增强 (1)
- 主题标签补充：建模/模型驱动 (36) / 待人工细分 (9) / 维护与演化 (4) / 测试与验证 (4) / 形式化方法 (3)

---

### `ICSOC`

- 基本信息：
- 全称：International Conference on Service Oriented Computing
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`62`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务组合 / 流程 / 性质与治理偶有贴题
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (59) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icsoc_conf_b.md](./venues/icsoc_conf_b.md)
- 数据文件：[metadata](metadata/icsoc_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsoc_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsoc/
- 官方论文集页：https://doi.org/10.1007/978-3-642-34321-6
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsoc_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (60) / 软件工程 (2)
- 软工纳入判定分布：不属于软件工程 (60) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (3) / 🟡 保留观察 (0) / ⏳ 待补信息 (59) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (62)
- 人工复核状态分布：未人工复核 (62)
- 高频软工主路径：8.2.3 服务系统与 API 生态 (1) / 2.1.4 云/服务/平台架构 (1)
- 主题标签补充：待人工细分 (38) / 建模/模型驱动 (12) / 系统软件 (7) / 需求工程 (2) / 形式化方法 (2)

---

### `SANER`

- 基本信息：
- 全称：IEEE International Conference on Software Analysis, Evolution, and Reengineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：代码分析 / 逆向 / 演化与 reengineering
- 初筛分布：无 2012 条目
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
- 年份：`2012`
- 条目数：`84`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：维护演化 / 修复 / 回归验证 / 工程闭环邻近
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (54) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10)
- 论文名录页：[venues/icsme_conf_b.md](./venues/icsme_conf_b.md)
- 数据文件：[metadata](metadata/icsme_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsme_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsm/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsme_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (79) / 跨域/待判定 (5)
- 软工纳入判定分布：属于软件工程 (79) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (54) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (10)
- 判定来源分布：启发式初判 (84)
- 人工复核状态分布：未人工复核 (84)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (26) / 1.1.4 需求追踪、变更与演化 (9) / 4.1.2 重构、重模块化与代码清理 (6) / 7.1.4 AI 支持的架构、设计与工程决策 (4) / 3.1.4 场景化测试 (4) / 2.3.2 构建工具链与开发环境 (3) / 4.2.4 克隆、相似性与理解支持 (3) / 4.3.1 版本、配置与构建工程 (3)
- 主题标签补充：维护与演化 (43) / 经验软件工程 (29) / 测试与验证 (20) / 建模/模型驱动 (16) / 可靠性/安全 (13)

---

### `VMCAI`

- 基本信息：
- 全称：International Conference on Verification, Model Checking, and Abstract Interpretation
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`29`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：程序验证 / 模型检查 / 抽象解释直接支撑验证框架
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/vmcai_conf_b.md](./venues/vmcai_conf_b.md)
- 数据文件：[metadata](metadata/vmcai_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-vmcai_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/vmcai/
- 官方论文集页：https://doi.org/10.1007/978-3-642-27940-9
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/vmcai_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (23) / 软件工程 (5) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (24) / 跨域但软工主导 (3) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (6) / 🟡 保留观察 (0) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (29)
- 人工复核状态分布：未人工复核 (29)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (3) / 3.2.1 静态分析与抽象解释 (2)
- 主题标签补充：待人工细分 (14) / 形式化方法 (7) / 测试与验证 (6) / 建模/模型驱动 (3) / 需求工程 (1)

---

### `ICWS`

- 基本信息：
- 全称：IEEE International Conference on Web Services
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`110`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：Web services / orchestration / 性质验证偶有贴题
- 初筛分布：🟢 优先跟进 (33) / 🟡 保留观察 (47) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (30)
- 论文名录页：[venues/icws_conf_b.md](./venues/icws_conf_b.md)
- 数据文件：[metadata](metadata/icws_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icws_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icws/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6257069/proceeding / http://www.computer.org/csdl/proceedings/icws/2012/2131/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icws_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (95) / 系统软件 (8) / 软件工程 (7)
- 软工纳入判定分布：不属于软件工程 (103) / 属于软件工程 (6) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (33) / 🟡 保留观察 (47) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (30)
- 判定来源分布：启发式初判 (110)
- 人工复核状态分布：未人工复核 (110)
- 高频软工主路径：2.1.4 云/服务/平台架构 (2) / 8.2.3 服务系统与 API 生态 (1) / 5.3.4 扩展性、吞吐与时延保证 (1) / 3.1.4 场景化测试 (1) / 6.1.2 过程挖掘、符合性与改进 (1) / 6.5.4 教育、培训与入门支持 (1)
- 主题标签补充：建模/模型驱动 (40) / 需求工程 (25) / 待人工细分 (20) / 系统软件 (17) / 维护与演化 (17)

---

### `ESEM`

- 基本信息：
- 全称：International Symposium on Empirical Software Engineering and Measurement
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`45`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证方法 / 评测设计 / `LLM-SE` 实验口径重要
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (29) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/esem_conf_b.md](./venues/esem_conf_b.md)
- 数据文件：[metadata](metadata/esem_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-esem_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/esem/
- 官方论文集页：http://dl.acm.org/citation.cfm?id=2372251 / https://ieeexplore.ieee.org/xpl/conhome/6450608/proceeding / http://www.computer.org/csdl/proceedings/esem/2012/1056/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/esem_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (40) / 跨域/待判定 (5)
- 软工纳入判定分布：属于软件工程 (40) / 不属于软件工程 (5)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (29) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (45)
- 人工复核状态分布：未人工复核 (45)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (10) / 6.3.1 实验、案例研究与调查 (9) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 3.2.3 面向质量属性的分析 (2) / 3.1.4 场景化测试 (2) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 1.1.1 需求获取与发现 (1) / 2.2.1 设计原则、模式与反模式 (1)
- 主题标签补充：经验软件工程 (19) / 建模/模型驱动 (13) / 维护与演化 (11) / 测试与验证 (9) / 可靠性/安全 (9)

---

### `ISSRE`

- 基本信息：
- 全称：IEEE International Symposium on Software Reliability Engineering
- `CCF` 等级：`B`
- 类型：`会议`
- 年份：`2012`
- 条目数：`38`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：可靠性 / assurance / 安全关键验证与缺陷检测很近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (30) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/issre_conf_b.md](./venues/issre_conf_b.md)
- 数据文件：[metadata](metadata/issre_conf_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-issre_conf_b)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/issre/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6403947/proceeding / http://www.computer.org/csdl/proceedings/issre/2012/4888/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/issre_conf_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (38)
- 软工纳入判定分布：属于软件工程 (38)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (30) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (38)
- 人工复核状态分布：未人工复核 (38)
- 高频软工主路径：3.3.3 assurance、认证与合规验证 (8) / 3.1.4 场景化测试 (5) / 3.1.1 测试生成与增强 (4) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 3.3.1 面向软工问题的形式化验证 (2) / 1.2.3 规约质量与一致性 (1) / 8.1.1 工业控制、汽车、航空与医疗软件 (1) / 6.2.1 估算、计划与排程 (1)
- 主题标签补充：测试与验证 (24) / 可靠性/安全 (14) / 经验软件工程 (12) / 建模/模型驱动 (10) / 需求工程 (6)

---

### `ASE / 期刊 / B`

- 基本信息：
- 全称：Automated Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`18`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：自动化软件工程 / `LLM for SE` / 建模-验证-修复主场
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (1) / ⏳ 待补信息 (13) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ase_journal_b.md](./venues/ase_journal_b.md)
- 数据文件：[metadata](metadata/ase_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ase_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10515
- 学术索引页：http://dblp.uni-trier.de/db/journals/ase/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ase_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (11) / 软件工程 (7)
- 软工纳入判定分布：不属于软件工程 (11) / 属于软件工程 (7)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (1) / ⏳ 待补信息 (13) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (18)
- 人工复核状态分布：未人工复核 (18)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (2) / 1.3.3 模型分析、仿真与验证 (2) / 3.2.1 静态分析与抽象解释 (1) / 4.1.2 重构、重模块化与代码清理 (1) / 1.2.2 自然语言到规约/属性 (1)
- 主题标签补充：待人工细分 (11) / 测试与验证 (3) / 形式化方法 (3) / 经验软件工程 (2) / 建模/模型驱动 (2)

---

### `ESE`

- 基本信息：
- 全称：Empirical Software Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`27`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：实证研究 / 数据集 / benchmark / 人因与评测设计
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (2) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ese_journal_b.md](./venues/ese_journal_b.md)
- 数据文件：[metadata](metadata/ese_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ese_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10664
- 学术索引页：http://dblp.uni-trier.de/db/journals/ese/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ese_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (24) / 跨域/待判定 (2) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (24) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (2) / ⏳ 待补信息 (23) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (7) / 3.2.3 面向质量属性的分析 (3) / 6.2.1 估算、计划与排程 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (2) / 6.3.1 实验、案例研究与调查 (2) / 4.2.1 代码搜索、导航与摘要 (1) / 6.4.1 代码、提交、issue 与 PR 挖掘 (1) / 6.3.4 replication、benchmark 与开放科学 (1)
- 主题标签补充：待人工细分 (7) / 维护与演化 (6) / 建模/模型驱动 (5) / 经验软件工程 (5) / 可靠性/安全 (4)

---

### `IETS`

- 基本信息：
- 全称：IET Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`51`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：broad SE 期刊，可筛少量建模/验证论文
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9)
- 论文名录页：[venues/iets_journal_b.md](./venues/iets_journal_b.md)
- 数据文件：[metadata](metadata/iets_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iets_journal_b)

- 关键信息页面：
- 期刊主页：https://ietresearch.onlinelibrary.wiley.com/journal/1751880x
- 学术索引页：https://dblp.uni-trier.de/db/journals/iet-sen
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/iets_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (36) / 跨域/待判定 (14) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (36) / 不属于软件工程 (15)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (26) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (9)
- 判定来源分布：启发式初判 (51)
- 人工复核状态分布：未人工复核 (51)
- 高频软工主路径：3.1.4 场景化测试 (7) / 1.1.1 需求获取与发现 (5) / 3.2.3 面向质量属性的分析 (3) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 6.3.1 实验、案例研究与调查 (2) / 1.3.2 模型转换、同步与协同 (2) / 4.1.1 缺陷修复与维护性修正 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (1)
- 主题标签补充：测试与验证 (21) / 建模/模型驱动 (20) / 需求工程 (12) / 维护与演化 (12) / 经验软件工程 (10)

---

### `IST`

- 基本信息：
- 全称：Information and Software Technology
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`93`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 建模测试 / `AI4SE` 论文较常见
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (2) / ⏳ 待补信息 (75) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/ist_journal_b.md](./venues/ist_journal_b.md)
- 数据文件：[metadata](metadata/ist_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ist_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/information-and-software-technology
- 学术索引页：http://dblp.uni-trier.de/db/journals/infsof/index.html
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ist_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (47) / 软件工程 (44) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (49) / 属于软件工程 (44)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (2) / ⏳ 待补信息 (75) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (93)
- 人工复核状态分布：未人工复核 (93)
- 高频软工主路径：1.1.1 需求获取与发现 (9) / 6.3.1 实验、案例研究与调查 (7) / 7.1.1 代码生成、补全与变换 (4) / 6.1.1 敏捷、精益与 DevOps 方法 (3) / 1.3.1 建模语言与元模型 (3) / 1.1.4 需求追踪、变更与演化 (2) / 4.1.2 重构、重模块化与代码清理 (2) / 4.1.1 缺陷修复与维护性修正 (2)
- 主题标签补充：待人工细分 (50) / 建模/模型驱动 (16) / 测试与验证 (12) / 需求工程 (10) / 可靠性/安全 (6)

---

### `JSEP`

- 基本信息：
- 全称：Journal of Software: Evolution and Process
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`57`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：演化 / 过程 / 迭代闭环与工程实践邻近
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/jsep_journal_b.md](./venues/jsep_journal_b.md)
- 数据文件：[metadata](metadata/jsep_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jsep_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/20477481
- 学术索引页：http://dblp.uni-trier.de/db/journals/smr/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jsep_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (54) / 跨域/待判定 (2) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (54) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (17) / 🟡 保留观察 (35) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (57)
- 人工复核状态分布：未人工复核 (57)
- 高频软工主路径：4.1.1 缺陷修复与维护性修正 (11) / 6.1.2 过程挖掘、符合性与改进 (8) / 6.1.1 敏捷、精益与 DevOps 方法 (5) / 6.5.2 协作、评审与知识共享 (4) / 1.1.4 需求追踪、变更与演化 (2) / 6.3.1 实验、案例研究与调查 (2) / 6.3.5 路线图、研究议程与领域回顾 (2) / 4.3.1 版本、配置与构建工程 (2)
- 主题标签补充：建模/模型驱动 (24) / 维护与演化 (19) / 测试与验证 (16) / 需求工程 (15) / 形式化方法 (13)

---

### `JSS`

- 基本信息：
- 全称：Journal of Systems and Software
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`220`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：系统与软件工程综合刊，常见建模/验证/CPS 个案
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (0) / ⏳ 待补信息 (207) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/jss_journal_b.md](./venues/jss_journal_b.md)
- 数据文件：[metadata](metadata/jss_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-jss_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/journal-of-systems-and-software
- 学术索引页：http://dblp.uni-trier.de/db/journals/jss/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/jss_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (153) / 软件工程 (62) / 系统软件 (5)
- 软工纳入判定分布：不属于软件工程 (158) / 属于软件工程 (62)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (0) / ⏳ 待补信息 (207) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (220)
- 人工复核状态分布：未人工复核 (220)
- 高频软工主路径：2.1.1 架构描述与恢复 (26) / 6.1.1 敏捷、精益与 DevOps 方法 (5) / 7.1.4 AI 支持的架构、设计与工程决策 (5) / 6.3.1 实验、案例研究与调查 (4) / 4.1.1 缺陷修复与维护性修正 (3) / 3.1.2 回归测试与测试选择 (2) / 1.3.1 建模语言与元模型 (2) / 2.2.2 模块化、依赖与解耦 (2)
- 主题标签补充：待人工细分 (132) / 建模/模型驱动 (31) / 维护与演化 (15) / 可靠性/安全 (15) / 测试与验证 (11)

---

### `RE / 期刊 / B`

- 基本信息：
- 全称：Requirements Engineering
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`19`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求工程 / 规约抽取 / 性质生成 / 需求到模型
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (1) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/re_journal_b.md](./venues/re_journal_b.md)
- 数据文件：[metadata](metadata/re_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-re_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/766
- 学术索引页：http://dblp.uni-trier.de/db/journals/re/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/re_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (16) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (16) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (1) / ⏳ 待补信息 (6) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (19)
- 人工复核状态分布：未人工复核 (19)
- 高频软工主路径：1.1.1 需求获取与发现 (12) / 6.3.1 实验、案例研究与调查 (2) / 3.2.3 面向质量属性的分析 (1) / 1.1.4 需求追踪、变更与演化 (1)
- 主题标签补充：需求工程 (12) / 待人工细分 (5) / 建模/模型驱动 (4) / 可靠性/安全 (1) / 维护与演化 (1)

---

### `SCP`

- 基本信息：
- 全称：Science of Computer Programming
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`78`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件程序与形式化/验证/程序分析交叉，贴题概率中高
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (65) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/scp_journal_b.md](./venues/scp_journal_b.md)
- 数据文件：[metadata](metadata/scp_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scp_journal_b)

- 关键信息页面：
- 期刊主页：https://www.sciencedirect.com/journal/science-of-computer-programming
- 学术索引页：http://dblp.uni-trier.de/db/journals/scp/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/scp_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (65) / 软件工程 (12) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (66) / 属于软件工程 (8) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (65) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (78)
- 人工复核状态分布：未人工复核 (78)
- 高频软工主路径：1.2.1 形式化规约与契约 (7) / 4.1.3 API、依赖与库演化 (1) / 1.1.4 需求追踪、变更与演化 (1) / 3.3.1 面向软工问题的形式化验证 (1) / 3.3.2 运行时验证与运行时监测 (1) / 2.1.5 架构知识、决策与不确定性管理 (1)
- 主题标签补充：待人工细分 (39) / 形式化方法 (16) / 建模/模型驱动 (14) / 测试与验证 (10) / 程序设计语言/编译 (3)

---

### `SoSyM`

- 基本信息：
- 全称：Software and Systems Modeling
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`44`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件与系统建模 / DSL / 状态机与模型分析主场
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (2) / ⏳ 待补信息 (38) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sosym_journal_b.md](./venues/sosym_journal_b.md)
- 数据文件：[metadata](metadata/sosym_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sosym_journal_b)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10270
- 学术索引页：http://dblp.uni-trier.de/db/journals/sosym/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sosym_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (22) / 跨域/待判定 (21) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (22) / 属于软件工程 (22)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (2) / ⏳ 待补信息 (38) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (44)
- 人工复核状态分布：未人工复核 (44)
- 高频软工主路径：1.3.1 建模语言与元模型 (13) / 2.2.1 设计原则、模式与反模式 (2) / 7.1.1 代码生成、补全与变换 (2) / 1.3.2 模型转换、同步与协同 (2) / 8.3.3 系统之系统与互操作 (1) / 1.3.3 模型分析、仿真与验证 (1) / 6.1.2 过程挖掘、符合性与改进 (1)
- 主题标签补充：建模/模型驱动 (34) / 待人工细分 (8) / 形式化方法 (4) / 维护与演化 (3) / 经验软件工程 (3)

---

### `STVR`

- 基本信息：
- 全称：Software Testing, Verification and Reliability
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`27`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 验证 / 可靠性与 formal properties 非常贴题
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/stvr_journal_b.md](./venues/stvr_journal_b.md)
- 数据文件：[metadata](metadata/stvr_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-stvr_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/10991689
- 学术索引页：http://dblp.uni-trier.de/db/journals/stvr/index.html
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/stvr_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (26) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (26) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：3.1.1 测试生成与增强 (5) / 3.1.4 场景化测试 (4) / 3.3.3 assurance、认证与合规验证 (4) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (3) / 1.3.4 基于模型的生成、测试与运行时支持 (2) / 1.3.1 建模语言与元模型 (2) / 4.2.5 文档工程、解释与设计 rationale 恢复 (1) / 5.3.4 扩展性、吞吐与时延保证 (1)
- 主题标签补充：测试与验证 (25) / 建模/模型驱动 (11) / 形式化方法 (9) / 需求工程 (8) / 可靠性/安全 (7)

---

### `SPE`

- 基本信息：
- 全称：Software: Practice and Experience
- `CCF` 等级：`B`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`71`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：工程实践 / 系统实现为主，偶有 runtime/verification
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (36) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (14)
- 论文名录页：[venues/spe_journal_b.md](./venues/spe_journal_b.md)
- 数据文件：[metadata](metadata/spe_journal_b.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spe_journal_b)

- 关键信息页面：
- 期刊主页：https://onlinelibrary.wiley.com/journal/1097024x
- 学术索引页：http://dblp.uni-trier.de/db/journals/spe/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/spe_journal_b.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (41) / 系统软件 (13) / 软件工程 (10) / 程序设计语言与形式化基础 (7)
- 软工纳入判定分布：不属于软件工程 (61) / 属于软件工程 (9) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (20) / 🟡 保留观察 (36) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (14)
- 判定来源分布：启发式初判 (71)
- 人工复核状态分布：未人工复核 (71)
- 高频软工主路径：1.3.1 建模语言与元模型 (2) / 6.3.1 实验、案例研究与调查 (1) / 2.1.4 云/服务/平台架构 (1) / 2.1.1 架构描述与恢复 (1) / 3.2.3 面向质量属性的分析 (1) / 3.4.1 调试、分诊与根因分析 (1) / 6.3.4 replication、benchmark 与开放科学 (1) / 5.3.4 扩展性、吞吐与时延保证 (1)
- 主题标签补充：建模/模型驱动 (19) / 维护与演化 (18) / 需求工程 (16) / 程序设计语言/编译 (16) / 系统软件 (14)

---

### `PASTE`

- 基本信息：
- 全称：ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：程序分析与软件工具工程，对验证/修复较近
- 初筛分布：无 2012 条目
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
- 年份：`2012`
- 条目数：`122`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：broad SE / 亚洲社区，`LLM-SE/测试/建模` 可见
- 初筛分布：🟢 优先跟进 (51) / 🟡 保留观察 (58) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (13)
- 论文名录页：[venues/apsec_conf_c.md](./venues/apsec_conf_c.md)
- 数据文件：[metadata](metadata/apsec_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-apsec_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/apsec/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=6462577
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/apsec_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (96) / 跨域/待判定 (24) / 系统软件 (2)
- 软工纳入判定分布：属于软件工程 (96) / 不属于软件工程 (26)
- 初筛分布：🟢 优先跟进 (51) / 🟡 保留观察 (58) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (13)
- 判定来源分布：启发式初判 (122)
- 人工复核状态分布：未人工复核 (122)
- 高频软工主路径：1.1.1 需求获取与发现 (13) / 7.1.1 代码生成、补全与变换 (13) / 6.3.1 实验、案例研究与调查 (6) / 3.1.4 场景化测试 (5) / 7.1.4 AI 支持的架构、设计与工程决策 (5) / 3.2.1 静态分析与抽象解释 (5) / 1.1.4 需求追踪、变更与演化 (4) / 1.3.1 建模语言与元模型 (4)
- 主题标签补充：建模/模型驱动 (48) / 需求工程 (37) / 测试与验证 (32) / 形式化方法 (31) / 维护与演化 (27)

---

### `EASE`

- 基本信息：
- 全称：International Conference on Evaluation and Assessment in Software Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`38`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：评测与实验设计 / benchmark / replication 有用
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (22) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/ease_conf_c.md](./venues/ease_conf_c.md)
- 数据文件：[metadata](metadata/ease_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ease_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ease/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6262522/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/ease_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (36) / 跨域/待判定 (2)
- 软工纳入判定分布：属于软件工程 (36) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (22) / ⏳ 待补信息 (1) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (38)
- 人工复核状态分布：未人工复核 (38)
- 高频软工主路径：6.3.1 实验、案例研究与调查 (9) / 6.3.3 系统综述、mapping 与 meta-analysis (5) / 4.1.1 缺陷修复与维护性修正 (4) / 6.1.1 敏捷、精益与 DevOps 方法 (3) / 6.3.4 replication、benchmark 与开放科学 (2) / 1.1.4 需求追踪、变更与演化 (2) / 6.2.1 估算、计划与排程 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (1)
- 主题标签补充：经验软件工程 (18) / 建模/模型驱动 (12) / 维护与演化 (9) / 需求工程 (7) / 测试与验证 (7)

---

### `ICECCS`

- 基本信息：
- 全称：International Conference on Engineering of Complex Computer Systems
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`38`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：复杂系统建模与验证 / safety-critical / CPS 邻近
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (31) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/iceccs_conf_c.md](./venues/iceccs_conf_c.md)
- 数据文件：[metadata](metadata/iceccs_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-iceccs_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/iceccs/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6298769/proceeding / http://www.computer.org/csdl/proceedings/iceccs/2012/4700/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/iceccs_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (28) / 软件工程 (8) / 系统软件 (2)
- 软工纳入判定分布：不属于软件工程 (30) / 属于软件工程 (8)
- 初筛分布：🟢 优先跟进 (7) / 🟡 保留观察 (0) / ⏳ 待补信息 (31) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (38)
- 人工复核状态分布：未人工复核 (38)
- 高频软工主路径：1.3.1 建模语言与元模型 (7) / 1.1.1 需求获取与发现 (1)
- 主题标签补充：待人工细分 (15) / 建模/模型驱动 (9) / 形式化方法 (6) / 需求工程 (4) / 系统软件 (2)

---

### `ICST`

- 基本信息：
- 全称：IEEE International Conference on Software Testing, Verification and Validation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`127`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：测试 / 形式化验证 / 缺陷检测与修复直接相关
- 初筛分布：🟢 优先跟进 (49) / 🟡 保留观察 (76) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 论文名录页：[venues/icst_conf_c.md](./venues/icst_conf_c.md)
- 数据文件：[metadata](metadata/icst_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icst_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icst/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6200016/proceeding / http://www.computer.org/csdl/proceedings/icst/2012/4670/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icst_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (125) / 跨域/待判定 (1) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (125) / 不属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (49) / 🟡 保留观察 (76) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (2)
- 判定来源分布：启发式初判 (127)
- 人工复核状态分布：未人工复核 (127)
- 高频软工主路径：3.1.4 场景化测试 (21) / 3.1.1 测试生成与增强 (17) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (15) / 3.2.3 面向质量属性的分析 (11) / 3.1.2 回归测试与测试选择 (7) / 1.3.1 建模语言与元模型 (6) / 3.2.1 静态分析与抽象解释 (6) / 6.3.1 实验、案例研究与调查 (5)
- 主题标签补充：测试与验证 (109) / 建模/模型驱动 (40) / 可靠性/安全 (36) / 形式化方法 (25) / 需求工程 (24)

---

### `SCAM`

- 基本信息：
- 全称：IEEE International Working Conference on Source Code Analysis and Manipulation
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`22`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：源码分析与变换 / 缺陷修复 / 程序理解邻近
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (16) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 论文名录页：[venues/scam_conf_c.md](./venues/scam_conf_c.md)
- 数据文件：[metadata](metadata/scam_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-scam_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/scam/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6389882/proceeding / http://www.computer.org/csdl/proceedings/scam/2012/4783/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/scam_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (19) / 跨域/待判定 (2) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：属于软件工程 (19) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (5) / 🟡 保留观察 (16) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (1)
- 判定来源分布：启发式初判 (22)
- 人工复核状态分布：未人工复核 (22)
- 高频软工主路径：3.2.3 面向质量属性的分析 (3) / 3.2.1 静态分析与抽象解释 (3) / 4.1.1 缺陷修复与维护性修正 (2) / 4.1.2 重构、重模块化与代码清理 (2) / 2.2.2 模块化、依赖与解耦 (1) / 3.2.4 分析驱动的理解、重构与综合 (1) / 7.3.1 自适应与反馈回路工程 (1) / 4.1.5 技术债、克隆与可维护性治理 (1)
- 主题标签补充：经验软件工程 (10) / 测试与验证 (9) / 可靠性/安全 (8) / 维护与演化 (5) / 程序设计语言/编译 (4)

---

### `COMPSAC`

- 基本信息：
- 全称：International Computer Software and Applications Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`111`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：覆盖过宽，需按建模/验证/`AI4SE` 子题筛选
- 初筛分布：🟢 优先跟进 (35) / 🟡 保留观察 (58) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18)
- 论文名录页：[venues/compsac_conf_c.md](./venues/compsac_conf_c.md)
- 数据文件：[metadata](metadata/compsac_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-compsac_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/compsac/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6340121/proceeding / http://www.computer.org/csdl/proceedings/compsac/2012/4736/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/compsac_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (73) / 软件工程 (32) / 系统软件 (5) / 程序设计语言与形式化基础 (1)
- 软工纳入判定分布：不属于软件工程 (79) / 属于软件工程 (26) / 跨域但软工主导 (6)
- 初筛分布：🟢 优先跟进 (35) / 🟡 保留观察 (58) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (18)
- 判定来源分布：启发式初判 (111)
- 人工复核状态分布：未人工复核 (111)
- 高频软工主路径：2.1.1 架构描述与恢复 (5) / 3.1.4 场景化测试 (4) / 3.2.3 面向质量属性的分析 (2) / 4.1.2 重构、重模块化与代码清理 (2) / 2.2.1 设计原则、模式与反模式 (2) / 7.1.5 人机协同开发与评估 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 7.1.1 代码生成、补全与变换 (1)
- 主题标签补充：测试与验证 (32) / 建模/模型驱动 (29) / 需求工程 (28) / 维护与演化 (25) / 可靠性/安全 (22)

---

### `ICFEM`

- 基本信息：
- 全称：International Conference on Formal Engineering Methods
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`34`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：formal engineering / 规约建模 / 验证与证明
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/icfem_conf_c.md](./venues/icfem_conf_c.md)
- 数据文件：[metadata](metadata/icfem_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icfem_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icfem/
- 官方论文集页：https://doi.org/10.1007/978-3-642-34281-3 / https://www.wikidata.org/entity/Q56501423
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icfem_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (26) / 软件工程 (8)
- 软工纳入判定分布：不属于软件工程 (26) / 跨域但软工主导 (6) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (0) / ⏳ 待补信息 (25) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (34)
- 人工复核状态分布：未人工复核 (34)
- 高频软工主路径：1.2.1 形式化规约与契约 (4) / 1.3.3 模型分析、仿真与验证 (2) / 3.3.1 面向软工问题的形式化验证 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：形式化方法 (12) / 测试与验证 (9) / 待人工细分 (9) / 建模/模型驱动 (7) / 需求工程 (2)

---

### `SSE`

- 基本信息：
- 全称：IEEE International Conference on Software Services Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`101`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件服务工程混合
- 初筛分布：🟢 优先跟进 (33) / 🟡 保留观察 (46) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (22)
- 论文名录页：[venues/sse_conf_c.md](./venues/sse_conf_c.md)
- 数据文件：[metadata](metadata/sse_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sse_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/IEEEscc/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/sse_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (78) / 软件工程 (11) / 系统软件 (10) / 程序设计语言与形式化基础 (2)
- 软工纳入判定分布：不属于软件工程 (90) / 属于软件工程 (10) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (33) / 🟡 保留观察 (46) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (22)
- 判定来源分布：启发式初判 (101)
- 人工复核状态分布：未人工复核 (101)
- 高频软工主路径：2.1.4 云/服务/平台架构 (6) / 8.2.3 服务系统与 API 生态 (2) / 4.1.1 缺陷修复与维护性修正 (2) / 5.2.3 供应链安全与可追溯信任 (1)
- 主题标签补充：建模/模型驱动 (47) / 需求工程 (27) / 系统软件 (19) / 维护与演化 (17) / 待人工细分 (15)

---

### `ICSSP`

- 基本信息：
- 全称：International Conference on Software and System Process
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`37`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：软件过程 / 团队与流程，对主问题较间接
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (23) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 论文名录页：[venues/icssp_conf_c.md](./venues/icssp_conf_c.md)
- 数据文件：[metadata](metadata/icssp_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icssp_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/ispw/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6219601/proceeding / https://www.computer.org/csdl/proceedings/icssp/2012/2352/00/index.html / http://dl.acm.org/citation.cfm?id=2664360
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icssp_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (36) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (36) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (23) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (5)
- 判定来源分布：启发式初判 (37)
- 人工复核状态分布：未人工复核 (37)
- 高频软工主路径：1.3.3 模型分析、仿真与验证 (9) / 6.1.1 敏捷、精益与 DevOps 方法 (6) / 6.2.1 估算、计划与排程 (3) / 6.3.1 实验、案例研究与调查 (2) / 6.5.1 开发者认知、生产力与福祉 (2) / 6.1.2 过程挖掘、符合性与改进 (2) / 1.1.1 需求获取与发现 (2) / 4.1.2 重构、重模块化与代码清理 (1)
- 主题标签补充：建模/模型驱动 (27) / 测试与验证 (8) / 需求工程 (7) / 待人工细分 (5) / 维护与演化 (5)

---

### `SEKE`

- 基本信息：
- 全称：International Conference on Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`143`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 偶有贴题
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (0) / ⏳ 待补信息 (125) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/seke_conf_c.md](./venues/seke_conf_c.md)
- 数据文件：[metadata](metadata/seke_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-seke_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/seke/
- 官方论文集页：http://ksiresearchorg.ipage.com/seke/Proceedings/seke/SEKE2012_Proceedings.pdf
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/seke_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (111) / 软件工程 (32)
- 软工纳入判定分布：不属于软件工程 (111) / 属于软件工程 (21) / 跨域但软工主导 (11)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (0) / ⏳ 待补信息 (125) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (143)
- 人工复核状态分布：未人工复核 (143)
- 高频软工主路径：1.1.1 需求获取与发现 (12) / 6.3.1 实验、案例研究与调查 (3) / 1.3.1 建模语言与元模型 (3) / 1.1.4 需求追踪、变更与演化 (2) / 3.2.3 面向质量属性的分析 (2) / 6.1.1 敏捷、精益与 DevOps 方法 (1) / 3.1.4 场景化测试 (1) / 4.2.4 克隆、相似性与理解支持 (1)
- 主题标签补充：待人工细分 (67) / 建模/模型驱动 (29) / 测试与验证 (22) / 需求工程 (12) / 形式化方法 (11)

---

### `QRS`

- 基本信息：
- 全称：International Conference on Software Quality, Reliability and Security
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：质量 / 可靠性 / 安全 / assurance 与验证链很近
- 初筛分布：无 2012 条目
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
- 年份：`2012`
- 条目数：`0`
- `软工归属级别`：`完全属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：复用 / 组件资产，可补模型资产与可复用工件
- 初筛分布：无 2012 条目
- 论文名录页：[venues/icsr_conf_c.md](./venues/icsr_conf_c.md)
- 数据文件：[metadata](metadata/icsr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-icsr_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/icsr/
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/icsr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 本年度未检出直接归属该 venue 的主论文条目。

---

### `SPIN`

- 基本信息：
- 全称：International Symposium on Model Checking of Software
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`20`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：软件模型检查 / state-based verification / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/spin_conf_c.md](./venues/spin_conf_c.md)
- 数据文件：[metadata](metadata/spin_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-spin_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/spin/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/spin_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (11) / 程序设计语言与形式化基础 (9)
- 软工纳入判定分布：不属于软件工程 (9) / 属于软件工程 (7) / 跨域但软工主导 (4)
- 初筛分布：🟢 优先跟进 (9) / 🟡 保留观察 (0) / ⏳ 待补信息 (11) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (20)
- 人工复核状态分布：未人工复核 (20)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (4) / 1.3.3 模型分析、仿真与验证 (4) / 1.2.1 形式化规约与契约 (1) / 1.3.1 建模语言与元模型 (1) / 1.3.2 模型转换、同步与协同 (1)
- 主题标签补充：形式化方法 (9) / 建模/模型驱动 (8) / 测试与验证 (6) / 待人工细分 (6) / 程序修复 (2)

---

### `TASE`

- 基本信息：
- 全称：Theoretical Aspects of Software Engineering Conference
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`42`
- `软工归属级别`：`部分属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件工程名下的 formal verification / assurance 邻近
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/tase_conf_c.md](./venues/tase_conf_c.md)
- 数据文件：[metadata](metadata/tase_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-tase_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/tase/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6269388/proceeding / http://www.computer.org/csdl/proceedings/tase/2012/4751/00/index.html
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/tase_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (22) / 软件工程 (15) / 系统软件 (5)
- 软工纳入判定分布：不属于软件工程 (27) / 属于软件工程 (13) / 跨域但软工主导 (2)
- 初筛分布：🟢 优先跟进 (27) / 🟡 保留观察 (12) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (42)
- 人工复核状态分布：未人工复核 (42)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (5) / 1.2.1 形式化规约与契约 (2) / 1.3.3 模型分析、仿真与验证 (2) / 3.1.4 场景化测试 (1) / 3.2.1 静态分析与抽象解释 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1) / 3.1.1 测试生成与增强 (1) / 6.3.1 实验、案例研究与调查 (1)
- 主题标签补充：形式化方法 (26) / 建模/模型驱动 (21) / 测试与验证 (17) / 需求工程 (16) / 维护与演化 (5)

---

### `MSR`

- 基本信息：
- 全称：Mining Software Repositories
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`38`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：仓库挖掘 / benchmark / `LLM-SE` 证据与数据建设有用
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (31) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 论文名录页：[venues/msr_conf_c.md](./venues/msr_conf_c.md)
- 数据文件：[metadata](metadata/msr_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-msr_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/msr/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6220358/proceeding / http://www.computer.org/csdl/proceedings/msr/2012/1760/00/index.html / http://dl.acm.org/citation.cfm?id=2664446
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/msr_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (35) / 跨域/待判定 (3)
- 软工纳入判定分布：属于软件工程 (35) / 不属于软件工程 (3)
- 初筛分布：🟢 优先跟进 (4) / 🟡 保留观察 (31) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (3)
- 判定来源分布：启发式初判 (38)
- 人工复核状态分布：未人工复核 (38)
- 高频软工主路径：3.2.3 面向质量属性的分析 (5) / 6.3.1 实验、案例研究与调查 (5) / 4.1.1 缺陷修复与维护性修正 (5) / 6.4.1 代码、提交、issue 与 PR 挖掘 (3) / 6.3.4 replication、benchmark 与开放科学 (2) / 7.1.2 AI 支持的测试、分析与修复 (2) / 7.1.4 AI 支持的架构、设计与工程决策 (2) / 4.3.1 版本、配置与构建工程 (2)
- 主题标签补充：可靠性/安全 (19) / 经验软件工程 (18) / 维护与演化 (18) / 测试与验证 (8) / 建模/模型驱动 (6)

---

### `REFSQ`

- 基本信息：
- 全称：Requirements Engineering: Foundation for Software Quality
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`27`
- `软工归属级别`：`完全属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：需求质量 / 需求规约 / 需求到性质非常贴题
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (0) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/refsq_conf_c.md](./venues/refsq_conf_c.md)
- 数据文件：[metadata](metadata/refsq_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-refsq_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/refsq/
- 官方论文集页：https://doi.org/10.1007/978-3-642-28714-5
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/refsq_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (20) / 跨域/待判定 (7)
- 软工纳入判定分布：属于软件工程 (20) / 不属于软件工程 (7)
- 初筛分布：🟢 优先跟进 (18) / 🟡 保留观察 (0) / ⏳ 待补信息 (9) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：1.1.1 需求获取与发现 (11) / 1.1.4 需求追踪、变更与演化 (2) / 6.2.2 风险、价值与优先级 (1) / 1.1.2 需求分析、协商与优先级 (1) / 1.4.1 特征建模与配置 (1) / 3.3.2 运行时验证与运行时监测 (1) / 2.1.1 架构描述与恢复 (1) / 6.3.1 实验、案例研究与调查 (1)
- 主题标签补充：需求工程 (18) / 待人工细分 (9) / 维护与演化 (1) / 可靠性/安全 (1) / 经验软件工程 (1)

---

### `WICSA`

- 基本信息：
- 全称：Working IEEE/IFIP Conference on Software Architecture
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`48`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：软件架构 / 设计决策 / 模型结构与演化有用
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (28) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 论文名录页：[venues/wicsa_conf_c.md](./venues/wicsa_conf_c.md)
- 数据文件：[metadata](metadata/wicsa_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-wicsa_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：http://dblp.uni-trier.de/db/conf/wicsa/
- 官方论文集页：https://ieeexplore.ieee.org/xpl/conhome/6336551/proceeding
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/wicsa_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (47) / 跨域/待判定 (1)
- 软工纳入判定分布：属于软件工程 (47) / 不属于软件工程 (1)
- 初筛分布：🟢 优先跟进 (12) / 🟡 保留观察 (28) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (8)
- 判定来源分布：启发式初判 (48)
- 人工复核状态分布：未人工复核 (48)
- 高频软工主路径：2.1.1 架构描述与恢复 (18) / 7.1.4 AI 支持的架构、设计与工程决策 (8) / 6.3.1 实验、案例研究与调查 (4) / 2.3.3 组件、包与集成工程 (2) / 4.1.1 缺陷修复与维护性修正 (2) / 1.1.4 需求追踪、变更与演化 (2) / 2.1.3 架构演化与重构 (1) / 6.1.1 敏捷、精益与 DevOps 方法 (1)
- 主题标签补充：建模/模型驱动 (19) / 维护与演化 (18) / 需求工程 (11) / 形式化方法 (7) / 待人工细分 (6)

---

### `Internetware`

- 基本信息：
- 全称：Asia-Pacific Symposium on Internetware
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`26`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：平台 / 网络化软件 / 运行治理邻近
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 论文名录页：[venues/internetware_conf_c.md](./venues/internetware_conf_c.md)
- 数据文件：[metadata](metadata/internetware_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-internetware_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.org/db/conf/internetware/index.html
- 官方论文集页：http://dl.acm.org/citation.cfm?id=2430475
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/internetware_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (20) / 跨域/待判定 (5) / 系统软件 (1)
- 软工纳入判定分布：属于软件工程 (20) / 不属于软件工程 (6)
- 初筛分布：🟢 优先跟进 (8) / 🟡 保留观察 (14) / ⏳ 待补信息 (0) / ⚪ 暂不跟进 (4)
- 判定来源分布：启发式初判 (26)
- 人工复核状态分布：未人工复核 (26)
- 高频软工主路径：2.1.4 云/服务/平台架构 (11) / 7.1.4 AI 支持的架构、设计与工程决策 (3) / 3.1.4 场景化测试 (2) / 1.3.1 建模语言与元模型 (1) / 2.2.1 设计原则、模式与反模式 (1) / 1.2.1 形式化规约与契约 (1) / 4.3.1 版本、配置与构建工程 (1)
- 主题标签补充：建模/模型驱动 (14) / 维护与演化 (8) / 程序分析 (6) / 需求工程 (6) / 经验软件工程 (5)

---

### `RV`

- 基本信息：
- 全称：International Conference on Runtime Verification
- `CCF` 等级：`C`
- 类型：`会议`
- 年份：`2012`
- 条目数：`35`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：运行时验证 / 监测 / 时序性质 / 工具链直接邻近
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/rv_conf_c.md](./venues/rv_conf_c.md)
- 数据文件：[metadata](metadata/rv_conf_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-rv_conf_c)

- 关键信息页面：
- 年主页：待补
- 学术索引页：https://dblp.org/db/conf/rv/index.html
- 官方论文集页：https://doi.org/10.1007/978-3-642-29860-8
- `CFP`：待补

- 名录说明：对应 [venue 页面](./venues/rv_conf_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (20) / 软件工程 (14) / 系统软件 (1)
- 软工纳入判定分布：不属于软件工程 (21) / 跨域但软工主导 (12) / 属于软件工程 (2)
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (35)
- 人工复核状态分布：未人工复核 (35)
- 高频软工主路径：3.3.2 运行时验证与运行时监测 (11) / 3.1.3 模糊、搜索式、变异与性质驱动测试 (1) / 3.3.1 面向软工问题的形式化验证 (1) / 3.2.2 动态与混合分析 (1)
- 主题标签补充：运行时监测 (19) / 测试与验证 (12) / 待人工细分 (9) / 建模/模型驱动 (3) / 形式化方法 (2)

---

### `IJSEKE`

- 基本信息：
- 全称：International Journal of Software Engineering and Knowledge Engineering
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`49`
- `软工归属级别`：`大部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：`SE + 知识工程` 混合，`AI/建模` 可补链但不稳定
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (21) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (7)
- 论文名录页：[venues/ijseke_journal_c.md](./venues/ijseke_journal_c.md)
- 数据文件：[metadata](metadata/ijseke_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-ijseke_journal_c)

- 关键信息页面：
- 期刊主页：https://www.worldscientific.com/worldscinet/ijseke
- 学术索引页：http://dblp.uni-trier.de/db/journals/ijseke/index.html
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/ijseke_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (34) / 跨域/待判定 (13) / 系统软件 (2)
- 软工纳入判定分布：属于软件工程 (34) / 不属于软件工程 (15)
- 初筛分布：🟢 优先跟进 (16) / 🟡 保留观察 (21) / ⏳ 待补信息 (5) / ⚪ 暂不跟进 (7)
- 判定来源分布：启发式初判 (49)
- 人工复核状态分布：未人工复核 (49)
- 高频软工主路径：3.1.4 场景化测试 (7) / 1.1.1 需求获取与发现 (3) / 7.1.1 代码生成、补全与变换 (3) / 1.3.1 建模语言与元模型 (3) / 6.3.4 replication、benchmark 与开放科学 (2) / 1.1.4 需求追踪、变更与演化 (2) / 6.5.2 协作、评审与知识共享 (1) / 4.3.1 版本、配置与构建工程 (1)
- 主题标签补充：建模/模型驱动 (20) / 测试与验证 (15) / 需求工程 (13) / 待人工细分 (10) / 经验软件工程 (10)

---

### `STTT`

- 基本信息：
- 全称：International Journal of Software Tools for Technology Transfer
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`37`
- `软工归属级别`：`部分属于软工`
- `氛围`：`A 🔥`
- 与本课题的关系：验证工具 / formal methods tool transfer / `UPPAAL` 邻近
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (24) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sttt_journal_c.md](./venues/sttt_journal_c.md)
- 数据文件：[metadata](metadata/sttt_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sttt_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/10009
- 学术索引页：http://dblp.uni-trier.de/db/journals/sttt/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sttt_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：程序设计语言与形式化基础 (24) / 软件工程 (13)
- 软工纳入判定分布：不属于软件工程 (24) / 属于软件工程 (8) / 跨域但软工主导 (5)
- 初筛分布：🟢 优先跟进 (13) / 🟡 保留观察 (0) / ⏳ 待补信息 (24) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (37)
- 人工复核状态分布：未人工复核 (37)
- 高频软工主路径：3.3.1 面向软工问题的形式化验证 (8) / 3.3.2 运行时验证与运行时监测 (3) / 3.2.1 静态分析与抽象解释 (1) / 1.3.4 基于模型的生成、测试与运行时支持 (1)
- 主题标签补充：建模/模型驱动 (16) / 测试与验证 (12) / 形式化方法 (10) / 待人工细分 (7) / 运行时监测 (5)

---

### `SOCA`

- 基本信息：
- 全称：Service Oriented Computing and Applications
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`27`
- `软工归属级别`：`部分属于软工`
- `氛围`：`C 🟡`
- 与本课题的关系：服务计算与应用为主
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (1) / ⏳ 待补信息 (26) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/soca_journal_c.md](./venues/soca_journal_c.md)
- 数据文件：[metadata](metadata/soca_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-soca_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11761
- 学术索引页：http://dblp.uni-trier.de/db/journals/soca/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/soca_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：跨域/待判定 (25) / 软件工程 (2)
- 软工纳入判定分布：不属于软件工程 (25) / 属于软件工程 (1) / 跨域但软工主导 (1)
- 初筛分布：🟢 优先跟进 (0) / 🟡 保留观察 (1) / ⏳ 待补信息 (26) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (27)
- 人工复核状态分布：未人工复核 (27)
- 高频软工主路径：7.1.1 代码生成、补全与变换 (1) / 3.3.2 运行时验证与运行时监测 (1)
- 主题标签补充：待人工细分 (15) / 系统软件 (5) / 建模/模型驱动 (3) / 形式化方法 (2) / 运行时监测 (2)

---

### `SQJ`

- 基本信息：
- 全称：Software Quality Journal
- `CCF` 等级：`C`
- 类型：`期刊`
- 年份：`2012`
- 条目数：`25`
- `软工归属级别`：`完全属于软工`
- `氛围`：`B 🟢`
- 与本课题的关系：质量 / 度量 / assurance 视角可支撑验证评价
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (1) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 论文名录页：[venues/sqj_journal_c.md](./venues/sqj_journal_c.md)
- 数据文件：[metadata](metadata/sqj_journal_c.json)
- 近 `5` 年投稿时间线：[timeline](../SUBMISSION_TIMELINES.md#timeline-sqj_journal_c)

- 关键信息页面：
- 期刊主页：https://link.springer.com/journal/11219
- 学术索引页：http://dblp.uni-trier.de/db/journals/sqj/
- 2012 年官方 article page：见对应 venue 页中的 `官方落地页` 列

- 名录说明：对应 [venue 页面](./venues/sqj_journal_c.md) 中已按 `🟢 -> 🟡 -> ⏳ -> ⚪` 初筛优先级完成排序。

- 本 venue 年度观察：
- 一级总判定分布：软件工程 (17) / 跨域/待判定 (8)
- 软工纳入判定分布：属于软件工程 (17) / 不属于软件工程 (8)
- 初筛分布：🟢 优先跟进 (2) / 🟡 保留观察 (1) / ⏳ 待补信息 (22) / ⚪ 暂不跟进 (0)
- 判定来源分布：启发式初判 (25)
- 人工复核状态分布：未人工复核 (25)
- 高频软工主路径：3.1.1 测试生成与增强 (9) / 1.4.1 特征建模与配置 (2) / 6.3.1 实验、案例研究与调查 (2) / 4.1.2 重构、重模块化与代码清理 (1) / 2.2.4 技术债与设计质量 (1) / 6.3.3 系统综述、mapping 与 meta-analysis (1) / 5.3.1 性能建模、基准与调优 (1)
- 主题标签补充：待人工细分 (15) / 建模/模型驱动 (6) / 测试与验证 (5) / 需求工程 (2) / 程序设计语言/编译 (1)

## 7. 本年度总体观察

- `软工归属级别` 分布：完全属于软工 26 / 部分属于软工 22 / 大部分属于软工 9
- `氛围` 分布：A 🔥 22 / B 🟢 19 / C 🟡 16
- 初筛分布：🟢 优先跟进 (769) / 🟡 保留观察 (988) / ⏳ 待补信息 (962) / ⚪ 暂不跟进 (213)
- 一级总判定分布：软件工程 (1651) / 跨域/待判定 (949) / 程序设计语言与形式化基础 (263) / 系统软件 (69)
- 软工纳入判定分布：属于软件工程 (1579) / 不属于软件工程 (1281) / 跨域但软工主导 (72)
- 判定来源分布：启发式初判 (2932)
- 人工复核状态分布：未人工复核 (2932)
- 高频软工主路径：1.1.1 需求获取与发现 (119) / 7.1.1 代码生成、补全与变换 (109) / 4.1.1 缺陷修复与维护性修正 (98) / 6.3.1 实验、案例研究与调查 (94) / 3.1.4 场景化测试 (88) / 1.3.1 建模语言与元模型 (86) / 2.1.1 架构描述与恢复 (66) / 7.1.4 AI 支持的架构、设计与工程决策 (59) / 1.1.4 需求追踪、变更与演化 (49) / 3.2.3 面向质量属性的分析 (44) / 3.1.1 测试生成与增强 (42) / 3.3.1 面向软工问题的形式化验证 (37) / 6.1.1 敏捷、精益与 DevOps 方法 (37) / 1.3.3 模型分析、仿真与验证 (36) / 1.2.1 形式化规约与契约 (33)
- 计数复核状态：以 [verification.json](./verification.json) 为准；默认要求 `expected_total == actual_total`。
- 分类终判状态：以 `metadata/*.json` 中的 `classification_source / manual_review_status / manual_review_note` 为准。
- 后续若继续扩年份或重跑年度页，建议先运行 `tools/ccf_se_index_builder.py`，再运行 `tools/ccf_se_classifier.py`。
