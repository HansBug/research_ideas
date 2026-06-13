# strict seed 文库总账

## 当前状态

本目录当前处于 **PR-R1.6 bounded snapshot v2**：在 PR-R1.5 的 27 条候选 / 10 个单篇目录 / 3 条保守主候选基础上，继续完成 recent LLM、classic use-case、completion/scenario 边界、Crossref refined search、Zenodo/GitHub/HuggingFace artifact 核验与逐候选回填。

R1.6 的核心结论是：**已把可交接给 PR-R2 人工裁决的主 / 条件主 seed 候选从 3 条扩展到 4 条**，但仍不冻结最终四例、不跑真实例子、不调用 LLM。若 PR-R2 拒绝任一条件候选，则优先走 `fsm-bench-20` 复跑冻结、`sources/` 构造或低配 prompt / 学生人工构造的 fallback，并单独记录 provenance。

## 当前统计（bounded snapshot v2）

| 指标 | 数量 | 说明 |
|---|---:|---|
| `candidate_matrix.md` 去重候选 | 36 | PR-R1.5 27 条 + R1.6 新增 / 拆分 9 条。 |
| `screening_ledger.md` 已入账候选 | 36 | 与 candidate matrix 一一对应。 |
| 已完成单篇全文 / artifact 编码目录 | 15 | PR-R1.5 的 10 个 + R1.6 新增 5 个：`fsm-gen-iec-61499`、`completion-sysml-gwt`、`fsm-bench-20`、`ijisrt-uml-state-diagrams-llm`、`unified-uml-multimodal-validation`。 |
| 可交接 PR-R2 的主 / 条件主候选 | 4 | `sefm-llm-state-machine`、`llms-emp-stm-subset`、`designing-fsm-gpt4`、`unified-uml-multimodal-validation`。后两者必须按条件候选处理。 |
| 保守强主候选 | 2 | `sefm-llm-state-machine`、`llms-emp-stm-subset`。 |
| 条件主候选 | 2 | `designing-fsm-gpt4` initial-generation-only；`unified-uml-multimodal-validation` synthetic requirements + HF state subset。 |
| pipeline fallback 候选 | 1 | `fsm-bench-20`：dataset/prompt/schema/code 可冻结，但 generated outputs / gold 未公开冻结，需要 PR-R2 复跑。 |
| converter / timed / extended 候选 | 2 | `ttool-ai-smd-subset`、`fsm-gen-iec-61499`；均不计 R1.6 四例下限。 |
| paper-only / private / manual 候选 | 10+ | `umple-nl-state-machine`、`req-mermaid-statechart`、classic use-case 论文等。 |
| 明确负例 / 边界 sentinel | 14+ | protocol、process、formal-spec、repair-only、sequence/scenario、completion-only、standard/protocol 等。 |
| 人工下载队列 | 11 | 见 [manual_download_queue.md](./manual_download_queue.md)。 |

## PR-R2 handoff 分组

| 分组 | 候选 | 当前用途 |
|---|---|---|
| 强主 seed 候选 | `sefm-llm-state-machine`、`llms-emp-stm-subset` | 最优先进入 PR-R2 四例候选池；仍需逐 case 冻结 artifact、license/hash、输入输出切片。 |
| 条件主 seed 候选 | `designing-fsm-gpt4`、`unified-uml-multimodal-validation` | 可补足四例候选数，但必须在 PR-R2 人工裁决：前者只能 initial-generation-only，后者必须标 synthetic requirements + license caveat。 |
| pipeline fallback | `fsm-bench-20` | 任务关系强、MIT / Zenodo / GitHub 可用；但公开包未冻结 generated outputs，需要 R2 复跑并保存 run record 后才可能升级。 |
| extended / converter pressure | `ttool-ai-smd-subset`、`fsm-gen-iec-61499`、`execution-nl-req-bt-sm` | 对 converter、控制系统相关性和 feedback story 有价值，但因 timing / private artifact / intermediate BT 不计主 seed。 |
| paper-only classic seed | `from-use-cases-to-statecharts`、`beyond-scenarios-state-models`、`executable-state-machines-structured-text`、`maritaca-use-case-behavior-models` 等 | related work、manual reconstruction 线索和 strict gate 边界；不计主 seed。 |
| hard exclusion / sentinel | protocol / sequence / completion / formal-spec / standard 风险项 | 供 reviewer 防误收。 |
| source candidate | `source-*` 五条代表项 | 只作为 fallback handoff；R1.6 不构造 `STM_0`，也不计 strict literature seed。 |

## R1.6 新增关键发现

1. **`unified-uml-multimodal-validation` 是当前最有价值的新条件候选**：HF `UMLCode_StateDiagram` 数据集公开、999 rows、state subset 可隔离；但输入由 LLaMA 合成，license 口径需 PR-R2 记录。
2. **`fsm-bench-20` 任务关系强但 outputs 未冻结**：Zenodo/GitHub/MIT、dataset/prompt/schema/code 都可用；但公开 ZIP 中 gold 是 placeholder，`outputs/` / `results/` 未包含，不能直接计四例。
3. **recent LLM paper-only 论文不能凑数**：`ijisrt-uml-state-diagrams-llm` 关系清楚但只有 PDF 内 prompt/listing/figure，`SA-3` 不计主 seed。
4. **classic use-case 方向仍主要是 paper-only / closed**：MARITACA、product-family use-case 等题名高度相关，但 metadata/abstract 级核验显示无公开 artifact，需人工下载且不能计数。
5. **completion/scenario 负例边界更清楚**：`completion-sysml-gwt` 是 partial-model completion；Whittle/LSC 等 scenario/statechart 工作输入不是 NL requirements。

## 关键风险

1. **四例候选不是四例冻结样本**：R1.6 只把可交接候选补到 4 条；PR-R2 仍需逐 case 冻结。
2. **条件候选可能被 PR-R2 拒绝**：`designing-fsm-gpt4` 有 oracle/repair 泄漏风险；`unified-uml-multimodal-validation` 是 synthetic requirements 且 license 不清。
3. **`fsm-bench-20` 不可直接算 generated seed**：没有已公开冻结的 generated FSM outputs；若使用必须复跑。
4. **manual queue 仍有 11 条**：closed IEEE / Springer / SSRN / AIAA PDF 可能改变 weak seed/related-work 结论，但不会自动放宽 hard gate。
5. **本 snapshot 不是全域 census**：R1.6 覆盖多轮 refined search 与 snowballing，但仍只声称 bounded snapshot。

## 下一步

1. PR-R2 基于 [seed_selection_candidates.md](./seed_selection_candidates.md) 先裁决 4 条主 / 条件主候选。
2. 对 `unified-uml-multimodal-validation` 做 row-level parse/render 抽检、license 记录和 case-level freeze。
3. 对 `designing-fsm-gpt4` 建立 initial-generation-only 切片，排除 repair/oracle/fault-model 信息。
4. 若四例仍不足，优先尝试 `fsm-bench-20` 复跑冻结，再考虑 `sources/` / student / manual / low-end prompt fallback。
5. 人工下载队列按优先级处理：classic use-case 与 `rscharter` 高于 protocol/standard sentinel。

## 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-14 03:55:00 | PR-R1.6 bounded snapshot v2：扩展到 36 条候选、15 个单篇目录、4 条可交接主 / 条件主候选；新增 Zenodo/GitHub/HF artifact 核验、search_rounds 与 PR-R2 handoff。 |
| 2026-06-14 02:22:00 | 修复 PR-R1.5 implementation review C/I：补 `req-mermaid-statechart` 单篇目录，补齐 27 条 screening ledger，修正人工下载队列 6 条、主 seed 保守计数 3 条、TTool timing 降级和 R2 blocker 交接口径。 |
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |
