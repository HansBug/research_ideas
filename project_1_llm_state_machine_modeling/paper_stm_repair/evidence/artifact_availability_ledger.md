# artifact availability ledger：代码 / 数据 / 结果可获取性台账

## 1. 口径

本台账只记录 R1 阶段已能从当前本地文档和已核验入口获得的资产状态。`🟢` 表示已有明确公开入口或本地冻结；`🟡` 表示可作为复现起点但缺 release / license / 依赖锁 / 完整包；`🟠` 表示仅有论文内结果、仓库壳或线索；`🔒` 表示明确私有或难以取得。

## 2. 五绿 direct baseline 可获取性

| slug | 论文 | 代码 | 数据 / 输入 | 结果细则 | artifact | R1 结论 |
|---|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 可作为 near-approximate 复现起点，但必须固定 GitHub HEAD 并记录无 license / release 风险。 |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 当前最强 external same-sample approximate 候选；正式实验前必须冻结 4open 副本和逐文件 hash。 |
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
