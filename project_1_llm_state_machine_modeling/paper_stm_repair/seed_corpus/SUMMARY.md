# strict seed 文库总账

## 当前状态

本目录当前处于 **PR-R1.7 bounded snapshot v4**：在 R1.6 的 36 条候选 / 36 条 screening / 15 个单篇目录 / 4 条可交接主或条件主候选基础上，继续执行广域 strict seed 文献调研、classic use-case/statechart 全文阅读、manual queue 资源复查、negative evidence 补强，并补齐旧九个 direct baseline 到 seed 方法集合的 crosswalk。

R1.7 的核心结论需要分成两层：**方法集合层**已经补齐旧九个 direct baseline 的 `NL / text -> STM-family` seed 方法入账，包括 paper-only、private-data 与 protocol-domain 方法；**PR-R2 四例样本计数层**仍没有新增可按 §1.3 公式与 `candidate_matrix.md` 的 `计数资格` 直接计入主 / 条件主 seed 的文献候选。因此 PR-R2 仍应以 R1.6 的 4 条主 / 条件主候选为核心，并准备 `fsm-bench-20` 复跑、`sources/` 构造、低配 prompt 或学生 / 人工种子作为 fallback。

## 当前统计（bounded snapshot v4）

| 指标 | 数量 | 说明 |
|---|---:|---|
| `candidate_matrix.md` 去重候选 | 47 | R1.6 36 条 + R1.7 新增 10 条正式候选 / 负例 / manual 记录 + 补入 `pushing-generative-envelope-mbse` 方法层条目。 |
| `screening_ledger.md` 已入账候选 | 47 | 与 candidate matrix 一一对应。 |
| 已完成单篇全文 / artifact 编码目录 | 24 | R1.6 15 个 + R1.7 新增 9 个：`nlp-req-formalization-testcase-generation`、`statistical-usage-testing-uml`、`unified-use-case-statecharts`、`statechart-codesign-usecases`、`object-models-uml-embedded`、`integrating-graphical-nl-specifications`、`specification-based-verification-usecase-sm`、`towards-automatic-model-completion`、`pushing-generative-envelope-mbse`。 |
| R1.7 search round | 8 | `round-r17-01` 到 `round-r17-08`，覆盖 OpenAlex、Crossref、arXiv、Semantic Scholar blocker、DBLP exact、classic fulltext、manual queue recheck。 |
| 旧九个 direct baseline 方法层覆盖 | 9/9 | 见 [baseline_seed_method_crosswalk.md](./baseline_seed_method_crosswalk.md)；其中 FlowFSM / SpecGPT 保留为 protocol-domain seed method，不计控制系统四例。 |
| 可按 §1.3 公式 + `计数资格` 计入的主 / 条件主候选 | 4 | 仍为 `sefm-llm-state-machine`、`llms-emp-stm-subset`、`designing-fsm-gpt4`、`unified-uml-multimodal-validation`；`fsm-bench-20` 虽为 `SS-A / SA-2` pipeline artifact，但 generated `STM_0` outputs 未公开冻结，在 `candidate_matrix.md` 标为 `no-pipeline-output-missing`，不直接计四例。 |
| R1.7 新增 paper-only strict/conditional evidence | 6 | `nlp-req-formalization-testcase-generation`、`statistical-usage-testing-uml`、`unified-use-case-statecharts`、`statechart-codesign-usecases`、`object-models-uml-embedded`、`pushing-generative-envelope-mbse`，均为 `SA-3`，不计主 seed。 |
| R1.7 新增 hard boundary / exclusion | 5+ | `integrating-graphical-nl-specifications`、`specification-based-verification-usecase-sm`、`towards-automatic-model-completion`、`ucgen-usecase-descriptions`、`web-tool-goal-statechart-derivation` 等。 |
| manual queue 状态 | 2 downloaded/excluded；2 excluded-by-metadata；10 still-blocked；2 new-manual-pending | 详见 [manual_download_queue.md](./manual_download_queue.md)。 |

## PR-R2 handoff 分组

| 分组 | 候选 | 当前用途 |
|---|---|---|
| 强主 seed 候选 | `sefm-llm-state-machine`、`llms-emp-stm-subset` | 最优先进入 PR-R2 四例候选池；仍需逐 case 冻结 artifact、license/hash、输入输出切片。 |
| 条件主 seed 候选 | `designing-fsm-gpt4`、`unified-uml-multimodal-validation` | 可补足四例候选数，但必须在 PR-R2 人工裁决：前者只能 initial-generation-only，后者必须标 synthetic requirements + license caveat。 |
| pipeline fallback | `fsm-bench-20` | 任务关系强、MIT / Zenodo / GitHub 可用；但公开包未冻结 generated outputs，需要 R2 复跑并保存 run record 后才可能升级。 |
| paper-only strict / conditional literature evidence | `nlp-req-formalization-testcase-generation`、`statistical-usage-testing-uml`、`unified-use-case-statecharts`、`statechart-codesign-usecases`、`object-models-uml-embedded`、`pushing-generative-envelope-mbse`、`from-use-cases-to-statecharts`、`beyond-scenarios-state-models`、`executable-state-machines-structured-text` 等 | related work、manual reconstruction 线索和 strict gate 论证；不计 R2 主 seed。 |
| extended / converter pressure | `ttool-ai-smd-subset`、`fsm-gen-iec-61499`、`execution-nl-req-bt-sm` | 对 converter、控制系统相关性和 feedback story 有价值，但因 timing / private artifact / intermediate BT 不计主 seed。 |
| protocol-domain seed method / hard exclusion sentinel | `protocol-flowfsm-sentinel`、`3gpp-protocol-sentinel` 与其他 protocol / sequence / completion / formal-spec / standard / co-exist / testbench 风险项 | FlowFSM / SpecGPT 保留为 protocol-domain seed 方法证据，但不计控制系统四例；其他 hard exclusion 供 reviewer 防误收。 |
| source candidate | `source-*` 五条代表项 | 只作为 fallback handoff；R1.7 不构造 `STM_0`，也不计 strict literature seed。 |

## R1.7 新增关键发现

1. **seed 方法集合比 R2 可计样本更大**：旧九个 direct baseline 现在按方法层 `9/9` 入账；Pushing Envelope、Umple、REQ 等 paper-only/private 方法不能计四例，但必须作为上游 `NL -> STM_0` 来源证据保留。
2. **新增全文并未把主候选数从 4 推高到 6**：新增 strict-like 论文主要是 `SA-3`，按合同不得计入 R1.7 主 / 条件主 seed 成功门。
3. **manual queue 大多仍是 paywall / browser-only / artifact-missing**：MARITACA、Automated Transition、Dependable Product-Families 等仍值得人工下载，但不能阻塞 PR-R2 先裁决已有 4 条。
4. **boundary 更清楚**：model completion、testbench state machine、graphical-notation-as-input、goal-model-to-statechart、output-not-STM 等都已入 exclusion / screening，降低误收风险。
5. **protocol-domain 不等于无 seed 价值**：FlowFSM / SpecGPT 因 `X_PROTOCOL` 不计控制系统四例，但作为长规范文本到 FSM 的 seed 方法与 agentic / ensemble extraction 参考保留。
6. **Semantic Scholar API 本轮 429**：已按 blocker 记录并由 OpenAlex/Crossref/arXiv/DBLP exact-title 替代；这不构成“未检索”的静默缺口。

## 关键风险

1. **四例候选仍紧绷**：按 `SS-A/SS-B + SA-1/SA-2 + 计数资格=yes-main/yes-conditional` 口径仍只有 4 条可交接候选，且其中 2 条为条件候选。
2. **`fsm-bench-20` 仍不能直接算 generated seed**：它适合 R2 复跑生成并冻结 `STM_0`，但公开包未给 generated outputs。
3. **paper-only / private / protocol 方法不能替代可运行样本**：它们必须进入 seed 方法集合，但不能冒充可复验实验输入。
4. **closed/manual 项可能改变 related-work 叙述，但不应改变 hard gate**：即使人工下载后确认生成关系，也大概率仍是 `SA-3/SA-5`，除非发现公开 artifact。
5. **本 snapshot 仍非全域 census**：R1.7 记录了广域 bounded search 与 negative evidence，不声称穷尽所有文献。

## 下一步

1. PR-R2 先从 seed 方法集合中裁决 4 条主 / 条件主候选，并同步记录为什么不选 paper-only/private/protocol/pipeline-output-missing 方法。
2. 若 PR-R2 拒绝任一条件候选，应优先启动 `sources/` 构造或低配 prompt / 学生人工 seed，并严格记录 provenance 与 leakage control。
3. 对 `MARITACA`、`Automated Transition`、`Dependable Product-Families`、`Rscharter` 做人工浏览器/机构下载，可用于 related work 或手工重建线索。
4. R3 converter 合同应考虑 R1.7 暴露的 PlantUML/CSV/JSON/UML statechart/image/table/manual transcription 多格式压力，但不要承诺通用转换。

## 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-14 13:20:00 | PR-R1.7 bounded snapshot v4：纠正 seed 方法集合 vs R2 四例计数口径，补齐旧九个 direct baseline crosswalk，新增 `pushing-generative-envelope-mbse`，扩展到 47 candidates / 47 screening / 24 single-paper dirs；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 12:10:00 | PR-R1.7 bounded snapshot v3：扩展到 46 candidates / 46 screening / 23 single-paper dirs / 8 R1.7 search rounds；新增 classic fulltext wave、manual queue 状态分布和 negative evidence；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 03:55:00 | PR-R1.6 bounded snapshot v2：扩展到 36 条候选、15 个单篇目录、4 条可交接主 / 条件主候选；新增 Zenodo/GitHub/HF artifact 核验、search_rounds 与 PR-R2 handoff。 |
| 2026-06-14 02:22:00 | 修复 PR-R1.5 implementation review C/I：补 `req-mermaid-statechart` 单篇目录，补齐 27 条 screening ledger，修正人工下载队列 6 条、主 seed 保守计数 3 条、TTool timing 降级和 R2 blocker 交接口径。 |
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |
