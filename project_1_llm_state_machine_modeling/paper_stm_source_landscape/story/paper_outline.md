# STM Source Landscape Paper Outline

## 1. 写作锚点

本文主线是 **benchmark-source landscape**：用 retrospective SMS + audit protocol 说明控制系统论文中的状态机案例如何成为 LLM 状态机建模 benchmark 的可追溯来源。

## 2. 建议 RQ / DQ

| 编号 | 问题 | 证据 | 边界 |
|---|---|---|---|
| RQ1 | frozen `sources` audited corpus 中哪些控制领域提供可抽取 STM / mode-switching / guarded-control 案例？ | 领域、STM 状态、案例数、negative audit | 只回答 corpus 内部分布 |
| RQ2 | 案例呈现哪些状态机类型、时间级别和结构复杂度？ | FSM/EFSM/HSM/Hybrid、T0--T3、结构标签 | 只解释 codebook 分类 |
| RQ3 | 预定义 eligibility rule 下，哪些案例适合核心候选、清洗候选、降采样候选？ | 质量标签、版权 gate、sensitivity | 不宣称最终 benchmark |
| RQ4 | 哪些同质簇会影响 benchmark 代表性？ | cluster / stratified analysis | 给 empirical constraints |
| DQ1 | 如何设计 copyright-safe、分层、可复现的 LLM STM benchmark-source artifact？ | RQ1--RQ4 synthesis、task-card pilot | discussion / design implication |

## 3. Section architecture

1. Introduction：LLM4Modeling benchmark-source gap 与贡献边界。
2. Background and Related Work：LLM4MDE / MDE / MBSE / RE / state-machine generation / CCF-A SMS bar。
3. Retrospective Mapping Protocol：snapshot、inclusion/exclusion、data extraction、quality / copyright policy。
4. Codebook and Corpus：领域、状态机类型、时间级别、结构标签、quality labels、evidence locator。
5. Results：RQ1--RQ4。
6. Benchmark-Source Design Implications：eligibility rules、stratified sampling、sanitized task-card schema。
7. Threats to Validity：retrospective provenance、selection bias、coding bias、copyright、LLM contamination。
8. Artifact Availability and Conclusion：metadata / labels / codebook / evidence locators / scripts / sanitized cards。

## 4. Related Work 红线

| 风险 claim | 安全替代表述 |
|---|---|
| “没有人做过状态机生成 / UML state machine generation” | “prior work addresses LLM-to-state-machine/modeling; our focus is benchmark-source landscape from control-system papers” |
| “本文发布了 benchmark” | “本文提出 benchmark-source eligibility and task-card pilot” |
| “systematic review 完整覆盖控制系统文献” | “retrospective systematic mapping over an audited corpus snapshot” |
