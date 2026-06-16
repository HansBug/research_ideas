# seed corpus agent provenance

本文件只记录 `seed_corpus/` 内部与文献筛查、全文阅读、证据等级判断直接相关的审计细账。跨 PR / issue 的执行计划、review 状态、ready gate、commit / push 汇报和 merge 进度以 GitHub PR / issue body 与 comment 为准，不在仓库内另建动态流程总账。

## 1. 记录边界

| 可记录内容 | 不记录内容 |
|---|---|
| 文献筛查批次、全文阅读对象、证据等级调整、事实复核导致的条目变更、失败 / blocker 的研究性原因。 | GitHub review 流水、C/I/M 处理流水、ready-to-merge 状态、commit / push / merge 进度、跨 PR 施工摘要。 |

## 2. 文献筛查与全文阅读审计细账

| 时间 | agent / 来源 | 类型 | 输入 | 研究性输出 | 失败 / 风险 | 复核口径 |
|---|---|---|---|---|---|---|
| 2026-06-14 | 主 session | 初始化 | PR #100 / #104 / R1 strict 协议 | 初始化 seed_corpus 框架与候选矩阵；将上游 `NL -> STM_0` seed 定义转为候选筛查字段。 | 初始候选多为 pending，需全文阅读核验。 | 后续只保留研究性事实，不记录 PR 流程状态。 |
| 2026-06-14 | literature scout A/B/C | 只读预侦察 | baselines / sources / external query plan | 形成候选线索、检索策略、噪声模式和初始排除方向。 | 部分外部检索命中噪声高，需依靠 strict seed 谓词筛掉。 | 主 session 按 candidate / screening / exclusion 口径整合。 |
| 2026-06-14 | paper-reader batch 1 | 单篇全文核验 | `sefm-llm-state-machine` / `llms-emp-stm-subset` / `ttool-ai-smd-subset` / `designing-fsm-gpt4` / `umple-nl-state-machine` / `from-use-cases-to-statecharts` | 产出或更新 6 个 `seed_desc.md` 与 `artifacts.md`；区分 strict seed、条件候选、文献证据和 out-of-scope。 | SA/SS 结论依赖论文全文和 artifact 可用性，不能只凭标题 / 摘要。 | 复核重点是生成关系、T0 边界、artifact 可冻结性和 leakage control。 |
| 2026-06-14 | paper-reader batch 2 | 单篇全文核验 | `beyond-scenarios-state-models` / `scenarios-statecharts-interrelated` / `executable-state-machines-structured-text` | 产出 3 个 `seed_desc.md` 与 `artifacts.md`；形成 1 个 NN-D 负例、2 个 SS-B / SA-3 文献证据。 | 经典方法常缺少可冻结 raw output，只能作为文献证据或手工重建线索。 | 复核重点是不要把 scenario / interrelated model 误计为可直接主 seed。 |
| 2026-06-14 | R1.6 completion / use-case / scenario readers | 只读候选核验 | `completion-sysml-gwt` / `towards-automatic-model-completion` / `automated-transition-use-cases-uml-sm` / `from-use-cases-to-statecharts` / `execution-nl-req-bt-sm` / scenario-statechart 候选 | 区分 completion-only、BT intermediate、sequence / formal scenario 与 classic use-case statechart 线索；多数降为 `SA-3/SA-5` 或 P1/P3 失败。 | 多数对象不能直接作为主 seed，但可作为 repair baseline、转换压力或 related work 线索。 | 回填时应写研究角色和降级理由，不写 PR review 状态。 |
| 2026-06-14 | R1.6 LLM / recent reader | 只读候选核验 | `fsm-bench-20`、IJISRT UML state diagrams、TechScience / HF unified UML dataset、fbAssistant 等 | 判定 `fsm-bench-20` outputs 未冻结；`unified-uml-multimodal-validation` 为条件候选；IJISRT 属 paper-only 手工重建线索。 | 存在 synthetic requirement、license unclear、outputs missing 等风险。 | 可公开 artifacts 只作为 evidence；能否进入主样本等待后续 seed freeze。 |
| 2026-06-14 | R1.7 scout / structure readers | 只读候选侦察与结构审查 | seed-scout 输出候选与噪声模式；artifact scout 输出 manual queue 状态；structure review 输出事实一致性缺口 | 暴露中央台账未同步、新增目录未入账、manual queue 未收口等事实一致性风险；后续修正为 47 candidates / 47 screening / 24 dirs。 | 新增广域候选仍未显著增加主 / 条件主可计样本。 | 复核重点是 candidate / screening ID 对齐、manual blocker 透明和 negative evidence 保留。 |
| 2026-06-14 | 主 session | 广域整合 | 新增 search round、候选 / 负例、单篇目录、manual queue 状态分布和 R2 handoff negative evidence | 形成 bounded snapshot：47 candidates / 47 screening / 24 single-paper dirs；主 / 条件主可计候选仍为 4。 | Semantic Scholar API 429；部分 manual 下载和 artifact license 仍待人工核验。 | 不声称全域 census；只作为后续 seed freeze 的候选证据。 |
