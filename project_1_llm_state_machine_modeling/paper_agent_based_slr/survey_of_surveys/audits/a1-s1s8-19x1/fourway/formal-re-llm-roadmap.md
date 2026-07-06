# formal-re-llm-roadmap：S1--S8 四分栏审计补充

## 总体统计池裁决

不进入主统计池。该文是 IST 2025 vision/roadmap paper，原文明示“不提供 sound empirical evidence”，且 Data availability 声明“No data was used”。可作为 Paper2 的边界锚点、roadmap schema 种子、concern→mechanism→action 启发，但不能作为 SLR/SMS 样本统计、频次分母或最终经验 finding 来源。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | §1 明确贡献是两个 roadmaps：LLM 支持 formal RE/FM、formal RE/FM 支持 LLM-based RE；同时声明 vision paper、非 empirical evidence、non-exhaustive。 | 可复原为“双向路线图”任务设定，而非 SLR/SMS RQ；样本单位需降级为 roadmap topics / action points。 | 不入主统计池；可作任务边界与 roadmap 类型样本。 | 精确核对 Page 2 vision paper 原文、贡献列表和页码。 |
| S2 语料收集与筛选 | 原文无检索库、检索式、纳排、质量评价、PRISMA、数据抽取；Data availability 声明无数据。 | 无语料构造树；参考文献只作作者论证线索，不构成系统语料。 | 不适用；这是阻断主统计池资格的核心证据。 | 核对全文是否存在 supplement / appendix；核对 Data availability 页码。 |
| S3 原生维度树 / 样本编码对象 | §4/Fig.2 有 Roadmap A；§6/Fig.4 有 Roadmap B；§7 有 practical considerations。 | 原生结构应写为“双根 roadmap 森林 + 边界森林”：A 为 5 个 discussion topics（其中 7 个 Action Point 文本块），B 为 7 个 discussion topics/action points，§7 为 7 类限制。 | 不入统计池；可作为维度树 / 字段树种子。 | 必须视觉核对 Fig.2/Fig.4 的圈号、layer label，并澄清“5 topics”与“7 Action Point statements”的分母差异。 |
| S4 字段级证据 | Action Point 段落可抽 concern、mechanism、artifact、recommendation、supporting refs；但没有样本级抽取表。 | 可降级为 action-point-level 字段树，不是 study-level coding form。 | 不入主统计池；可进入 pattern library seed。 | A2a 若继续使用，应逐 AP 建表并标注页码、段落、inferred_by_reviewer。 |
| S5 维度模式演化 | 原文以 worked examples + 作者经验 + seminal works 构造 roadmap；无 open coding、迭代 codebook、冲突裁决。 | 只有概念链条：example → concern → mechanism → action；不是可审计维度演化流程。 | 不入统计池；只作 researcher-defined meta-model 的启发。 | 核查 §4/§6 是否有更明确的 roadmap construction 说明；大概率仍为弱证据。 |
| S6 统计分析 | 无频次、比例、趋势、交叉表、样本分母；“No data was used”。 | 无统计节点；action point 数量只能描述原文结构，不能转成经验统计。 | 不适用；不得把 5/7/14/7 等结构数作为领域分母。 | 核对全文表格、图注和附录，确认无隐藏统计综合。 |
| S7 候选 finding | Roadmap B 提出 formal prompts、formal verification、runtime monitoring、ethical requirements 等建议；§7 提出 overreliance、evaluation difficulty 等风险。 | 可抽候选 finding heuristic：concern→mechanism→action；全部 evidence strength ≤ worked_example / author opinion。 | 不入主统计池；只能作为候选 finding 生成规则。 | A2a 需逐条标注 AP 来源和证据强度，防止写成已验证结论。 |
| S8 研究者 / 作者质疑与裁决 | §7 有 practical considerations：专家协作、empirical evaluation 难、overreliance、人类质量控制、技术演进等。 | 只有作者限制讨论与风险提醒；无多研究者筛选、编码分歧、QA 裁决日志。 | 不入统计池；可作 human-in-the-loop 风险字段种子。 | 核对 §7 各小标题页码；不要把 limitation discussion 升级为正式裁决机制。 |

## 建议降级 / 修正

1. S3 分母表述需修正：当前证据链中“Roadmap A 5 + Roadmap B 7 = 12 action points”容易误导。应区分 Roadmap A 是 5 个 discussion topics，但正文出现 7 个 `Action Point:` 文本块；Roadmap B 是 7 个 action points。
2. S7 建议从“中”改为“弱/中（roadmap heuristic）”：可保留候选 finding 启发价值，但必须显式说明不是 empirical finding。
3. S4 的“弱 / 中”建议拆开写：对 roadmap 字段抽取是“中”，对系统综述样本级字段证据是“弱 / 不适用”。这样可避免 A2a 误纳入统计池。
