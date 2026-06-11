# STM Source Landscape Paper Story

## Working title

From Control-System Papers to Benchmark-Source Landscapes: A Retrospective Systematic Mapping of State-Machine Cases

## Thesis

We study how state-machine, mode-switching, and guarded-control descriptions embedded in control-system papers can be audited into a copyright-safe, stratified benchmark-source landscape for LLM-based state-machine modeling.

## Task Boundary

- **Inputs**：`sources/` 中已入库的控制系统论文、`STM.md` 案例标注、BibTeX、摘要级与全文级证据定位。
- **Outputs**：metadata / labels / codebook / evidence locators / sanitized benchmark-card rules，不输出受版权保护 PDF 或全文。
- **Supported settings**：控制系统、CPS、机器人/自动驾驶、嵌入式、安全关键、工业自动化、铁路、交通、医疗、楼宇机电等含离散行为或模式切换的论文。
- **Out-of-scope settings**：证明 LLM 性能、发布最终 benchmark、覆盖所有控制系统文献、完整形式化验证或工业认证。

## Gap

LLM4SE / LLM4MDE / requirements automation 已快速增长，但缺少面向 LLM 状态机建模的、跨控制域、带质量标签、同质性风险与版权边界的 benchmark-source map。

## Technical Challenge

1. 状态机信息分散在正文、图、表、模式描述、控制逻辑和实验场景中。
2. `sources/` 是长期增量文库，必须写成 retrospective SMS with audit protocol。
3. `STM.md` 标签不是 gold standard，必须做 codebook、reliability 与 negative/excluded sample audit。
4. PDF、全文抽取物和长引用存在版权风险，公开 artifact 必须 sanitized。
5. 同质样本簇会导致 benchmark 偏斜，必须分层采样与降同质化。

## Method Insight

把“发现论文中的状态机案例”与“构造 LLM benchmark”分离：前者用 retrospective SMS + codebook + audit 得到 corpus landscape；后者只作为 evidence-informed benchmark design implication，并通过 sanitized task-card pilot 验证可用性。

## Contributions

1. 控制系统论文到状态机案例的 source landscape。
2. 从论文原文识别和标注状态机案例的 codebook 与审计协议。
3. 对案例质量、结构复杂度、时间约束、领域分布和同质簇的系统分析。
4. 面向 LLM 状态机建模 benchmark 的分层采样、降同质化与版权安全 artifact 设计原则。
5. 明确的 claim / artifact / copyright gate，避免把内部文库整理过度包装成最终 benchmark。

## Evidence

- 当前 planning baseline：`sources/` 787 篇论文、746 条正例案例、787/787 `STM.md` 覆盖。
- 本 PR 交付：#95 的 438 行候选审计、69 行初筛矩阵、25 条 P0/P1 人工下载 BibTeX、7 条 auto-fulltext 复查 gate。
- 正式结果前必须完成 snapshot 复算、codebook reliability、related-work direct competitor matrix、sanitized package。

## Related Work Positioning

- Direct / near：MDE/AI/DevOps SMS、MDE+ML SLR、MBSE behaviour V&V SLR、MDSE modelling assistants SMS、MBSE requirements extraction SLR。
- Methodology anchors：TSE/TOSEM/IST/JSS/SoSyM 的 SLR/SMS/landscape/bar 样本。
- Boundary works：LLM to UML/state machine generation、ProtocolGPT、UML diagram benchmarking、LLM4SE surveys。

## Claims to Avoid

- 不写 first / largest / complete / public benchmark dataset。
- 不写完整覆盖控制系统文献。
- 不写 LLM 能力提升或性能结论。
- 不把 `sources/` 现有 PDF / 全文抽取物当作公开 artifact。
