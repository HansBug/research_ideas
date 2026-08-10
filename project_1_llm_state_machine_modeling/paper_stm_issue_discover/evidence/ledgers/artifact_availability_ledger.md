# artifact availability ledger：代码 / 数据 / 结果可获取性台账

## 1. 口径

本台账只记录 R1 阶段已能从当前本地文档和已核验入口获得的资产状态。`🟢` 表示已有明确公开入口或本地冻结；`🟡` 表示可作为复现起点但缺 release / license / 依赖锁 / 完整包；`🟠` 表示仅有论文内结果、仓库壳或线索；`🔒` 表示明确私有或难以取得。

补充口径：artifact 可用性不同于 strict seed eligibility。某论文可以满足 `NL -> T0 STM-family` 的文献方向，但若原始 NL、生成 STM、reference、逐次输出或 license 无法冻结，仍不能直接进入 PR-R2 可复验 seed 样本。反过来，protocol / process / formal-spec artifact 即使公开，也只能作为 related work 或 out-of-domain 资产。


## 2.1 strict seed artifact 额外字段

后续 PR-R2 若把某候选放入 seed registry，除本表五类可获取性外，还必须补下列字段：

| 字段 | 含义 | 阻塞条件 |
|---|---|---|
| `nl_input_available` | 自然语言需求 / 场景 / 系统描述是否可冻结。 | 只有论文概述或私有需求时不得进主样本。 |
| `generated_stm_available` | 由 NL 生成 / 派生的初始 STM 或 reference 是否可冻结。 | 只有图片或聚合分数时需标 `SA-2/SA-3`。 |
| `generation_relation_evidence` | 是否有证据说明 STM 由 NL 生成，而不是共现或已有图模型 / 形式模型转换。 | 缺证据时只能 pending / near。 |
| `license_or_access_risk` | 数据、代码、artifact 是否允许实验复用。 | 私有 / 无 license / live-only 入口需降级。 |
| `hash_or_commit_plan` | 是否能记录 commit、hash、文件清单和下载日期。 | 无法冻结时不得声称可复验。 |

## 2. 五绿 direct baseline 可获取性

| slug | 论文 | 代码 | 数据 / 输入 | 结果细则 | artifact | R1 结论 |
|---|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 可作为 near-approximate 复现起点，但必须固定 GitHub HEAD 并记录无 license / release 风险。 |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 当前 artifact 最完整的 external same-sample approximate 候选；正式实验前必须冻结 4open 副本和逐文件 hash。 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | 🟢 | 🟠 | 🟠 | 🟠 | 🟠 | 主要作 related-work / protocol FSM evidence，不适合 R2 预演 seed。 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | 🟢 | 🟠 | 🟡 | 🟠 | 🟠 | 只能确认公开 3GPP 输入规格；GT 和代码未公开。 |
| `req` | 🟢 | 🟠 | 🔒 | 🟠 | 🟠 | 工业私有数据，不适合作为可复验实验资产。 |
| `umple` | 🟢 | 🟠 | 🟡 | 🟠 | 🟠 | 工具链公开但 thesis pipeline 未公开；可做人工重建近似。 |
| `llms_emp` | 🟢 | 🟠 | 🟢 | 🟢 | 🟡 | 数据/评分强，pipeline 弱；适合 STM 子集 seed / judge 校准。 |
| `pushing-the-generative-envelope-mbse-artifacts` | 🟢 | 🟠 | 🟠 | 🟠 | 🟠 | 小样本 evidence-only。 |
| `ttool-ai` | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 工具 artifact 强；需处理 TTool 安装与 provider drift。 |

## 3. 对 R2/R3 的影响

1. `structure-and-event-driven...`、`llms_emp`、`ttool-ai`、`designing-fsm...` 是优先进入 R2 候选池的 external / baseline 资产。
2. `req`、FlowFSM、SpecGPT、Pushing Envelope 当前更适合 related-work / boundary evidence，不应作为四例预演主样本。
3. `umple` 可作为格式转换压力样本，但必须承认论文 benchmark bundle 未公开。
4. 所有 GitHub `main` / 4open / Drive / dynareport / live docs 都需要在正式实验前冻结本地副本、日期、hash 或 commit。
