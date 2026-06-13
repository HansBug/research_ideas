# strict seed 文库总账

## 当前状态

本 PR 当前处于 **PR-R1.5 bounded snapshot v1**：已建立 seed 文库结构、strict seed 编码字段、初始本地候选矩阵、人工下载队列和负例 sentinel，并完成 `10` 个本地单篇目录的全文 / artifact 编码。该 snapshot 用于向 PR-R2 交接候选与 blocker，**不声称完成全域 census，也不声称已冻结四例样本**。

## 当前统计（bounded snapshot v1）

| 指标 | 数量 | 说明 |
|---|---:|---|
| `candidate_matrix.md` 去重候选 | 27 | 来自 R1 baseline / reproduction、external planner、sources scout 与 OpenAlex 初始检索。 |
| `screening_ledger.md` 已入账候选 | 27 | 已补齐与 candidate matrix 一一对应的 title/abstract / fulltext / artifact 层级记录。 |
| 已完成单篇全文 / artifact 编码目录 | 10 | 10 个 `papers/<slug>/` 目录均含 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`seed_desc.md`、`artifacts.md`。 |
| 当前可作为 PR-R2 主 seed 的候选 | 3 | `sefm-llm-state-machine`、`llms-emp-stm-subset`、`designing-fsm-gpt4`；其中 `designing-fsm-gpt4` 仅限 initial-generation-only。 |
| converter / timed boundary 候选 | 1 | `ttool-ai-smd-subset` 含 `after (5, 5)` 时间语义，当前降为 `ES-C + SA-2`，不计入主 seed 下限。 |
| 文献证据 / related-work-only 候选 | 5 | `umple-nl-state-machine`、`req-mermaid-statechart`、`from-use-cases-to-statecharts`、`beyond-scenarios-state-models`、`executable-state-machines-structured-text`。 |
| 明确负例 / 边界 sentinel | 10 | 见 [exclusion_ledger.md](./exclusion_ledger.md)，覆盖 protocol、process、formal-spec、repair-only、sequence/scenario、completion、T1+ 等边界。 |
| 人工下载队列 | 6 | 见 [manual_download_queue.md](./manual_download_queue.md)，均为外部候选待人工下载 / 进一步核验。 |

## 初步候选分组

当前按 hard gate 保守计数，**PR-R2 主 seed 可交接候选只有 3 条，未达到 4 条四例冻结下限**。因此本 PR-R1.5 的交付形式是“bounded snapshot + blocker handoff”：PR-R2 需要继续外部检索 / 人工下载、从 `sources/` 构造可追踪 `STM_0`、或用低配 prompt / 学生人工构造补足样本，并记录 provenance 与 leakage control。

| 分组 | 候选 | 当前用途 |
|---|---|---|
| R2 主 seed 候选 | `sefm-llm-state-machine`、`llms-emp-stm-subset` | 最优先进入 PR-R2 四例候选池；仍需冻结 artifact、license/hash、case-level 输入输出。 |
| R2 条件主 seed 候选 | `designing-fsm-gpt4` | 只可隔离初始 `NL description -> DFSM/Mealy CSV` 生成链路；repair/oracle 部分全部排除。 |
| converter / timed-SMD boundary | `ttool-ai-smd-subset` | 公开 artifact 有价值，但含 `after (5, 5)` 等时间语义；除非后续完成 case-level T0 isolation，否则不计入 R2 主 seed 下限。 |
| private / paper-only related work | `umple-nl-state-machine`、`req-mermaid-statechart`、`from-use-cases-to-statecharts`、`beyond-scenarios-state-models`、`executable-state-machines-structured-text` | 用于 related work、任务边界、manual reconstruction 线索，不直接冻结为 R2 主样本。 |
| hard exclusion sentinel | `protocol-flowfsm-sentinel`、`3gpp-protocol-sentinel`、`completion-sysml-gwt`、`generating-statechart-designs-from-scenarios` 等 | 校准 strict seed 排除门，避免把 protocol、sequence diagram、completion-only 或 formal-spec-only 误收。 |
| source candidate | `source-autonomous-driving-hsm`、`source-rotorcraft-uas-hsm`、`source-smarthand-hsm`、`source-hfsm-human-robot`、`source-avp-hsm` | 只证明本项目有真实控制系统 NL / HSM 描述池；若用于 R2，需要另行构造 `STM_0` 并记录防泄漏。 |

## 关键风险

1. **四例下限 blocker**：当前保守可交接主 seed 为 `3` 条，不足 `4` 条；PR-R1.5 只交接 blocker，不得声称已具备四例冻结输入。
2. **SA-3 / SA-4 不计入主 seed 下限**：paper-only、私有数据或不可再分发 artifact 只能作文献证据 / related work。
3. **TTool timing caveat**：`ttool-ai-smd-subset` 当前不计主 seed；若后续要升级，必须证明所选 case 的 `after` / signal / guard-action 语义可被 PR-R3 converter 无损或有审计地规范化。
4. **`designing-fsm-gpt4` 只限 initial generation**：只能取 `NL -> DFSM/Mealy CSV` 初始生成链路；oracle repair、distinguishing / checking sequence 和 fault-model repair 只作方法参考。
5. **`sources/` 宽池不等于 strict seed**：`sources/` 可提供真实控制系统描述，但其 `STM_0` 必须由本项目另行构造或记录来源，不能自动等同于文献 strict seed。
6. **外部检索尚未闭合**：IEEE / ACM / DBLP / publisher exact search、snowballing、人工下载和 license/hash 冻结仍需后续执行。

## 下一步

1. PR-R2 先处理四例下限 blocker：从本 PR 的 3 条主候选出发，继续查外部候选、人工下载队列和 `sources/` 构造方案。
2. 对 `designing-fsm-gpt4` 建立 initial-generation-only 的独立 seed 切片，避免 repair/oracle 信息泄漏。
3. 若考虑 `ttool-ai-smd-subset`，先在 PR-R3 converter contract 中定义 timed-SMD 到 T0/EFSM 的保留、抽象或剔除策略，再决定是否升级。
4. 执行 IEEE / ACM / DBLP / publisher 与 snowballing 检索，补外部候选下载、BibTeX、PDF 和全文编码。
5. 对人工下载队列完成后，按 [GUIDE.md](./GUIDE.md) 补单篇目录、`screening_ledger.md`、`candidate_matrix.md` 与本总账。

## 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-14 02:22:00 | 修复 implementation review C/I：补 `req-mermaid-statechart` 单篇目录，补齐 27 条 screening ledger，修正人工下载队列 6 条、主 seed 保守计数 3 条、TTool timing 降级和 R2 blocker 交接口径。 |
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |
