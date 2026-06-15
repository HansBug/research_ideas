# repair_baselines/GUIDE.md

## 1. 目标与边界

本 GUIDE 约束 `repair_baselines/` 的后续维护。本目录只记录与 `<NL, STM_0> -> STM_k / Better STM` 主线有关的 **修正、补全、refinement、consistency fixing、feedback-guided repair、verification / simulation / diagnostic feedback、LLM / agentic repair** 工作。

不得把本目录写成旧 `NL -> STM` generation baseline 文库。若某工作只证明 `STM_0` 可由 `NL` 生成，但没有修正或 feedback 环节，应进入 [../seed_library/](../seed_library/)；若某工作只有控制系统 NL 数据，应留给后续 `nl_datasets/`。

## 2. SUMMARY-first 规则

[SUMMARY.md](./SUMMARY.md) 是唯一横向事实真源，必须直接展示：

- 检索覆盖与来源切片；
- 候选全集与正式分级；
- emoji / enum 定义；
- repair baseline / related work 表；
- 资源可获取性表；
- 排除与 negative evidence；
- `manual_download_queue.bib` 状态；
- 最终结论与后续 handoff。

新增或修改任何单篇目录时，不得只改 `baseline_desc.md` 或 `artifacts.md`；必须同步更新 [SUMMARY.md](./SUMMARY.md) 的对应横向行。

## 3. 收录 / 排除标准

### 3.1 收录对象

| 类别 | 收录口径 |
|---|---|
| 直接 STM 修正 | 明确存在 `STM_0 -> STM_k`、state machine repair、statechart repair、transition completion、guard/action correction。 |
| 模型制品补全 / 修复 | UML / SysML / Stateflow / IEC 61499 / behavioral model artifact 的 completion、refinement、consistency fixing。 |
| 反馈驱动修复 | checker、verification、simulation、testing、diagnostic、counterexample、proof feedback 进入模型修正。 |
| LLM / agentic repair | LLM self-repair、multi-step repair、agent loop、reviewer-feedback repair，用于模型制品或可映射形式模型。 |
| generation pipeline 中的修正环节 | `NL -> STM` 工作若有 check / feedback / refinement / repair，登记其 repair slice，并 crosslink seed 文库。 |

### 3.2 排除对象

| 排除对象 | 处理 |
|---|---|
| 只做 `NL -> STM_0` 且无修正环节 | 排除出本库核心，回到 seed 文库。 |
| 纯 program repair / test repair / build repair | 只可作为远背景，不入正式 baseline 表。 |
| 纯 NL requirement rewriting | 不入本库；如有 NL 数据价值留给 `nl_datasets/`。 |
| BPMN / Petri / CSP / Event-B / TLA+ / Alloy 等非 STM family | 只有当 repair feedback 机制对本文非常关键时，作为异构 related / negative evidence 入账，不能写成同构 baseline。 |
| protocol FSM / 3GPP / RFC FSM | 默认 out-of-domain；只保留少量哨兵，避免混入控制系统 STM 任务。 |

## 4. emoji / enum 标准

正式表格中，emoji 列只写 emoji，中文释义集中写在本节和 [SUMMARY.md](./SUMMARY.md)。有偏序关系的维度默认按 **🟢 > 🟡 > 🟠 > 🔴** 表达；`❓` 表示待核，`⚪` 表示不适用。

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| 修正任务匹配 | 明确同构 `STM_0 -> STM_k` repair / completion | 模型制品 repair，可较清楚映射到 STM | 只有局部 feedback / consistency / completion 线索 | 无 repair / feedback | 待核 | 不适用 |
| STM 谱系匹配 | T0+FSM/HSM/EFSM/statechart 明确 | UML/SysML/Stateflow/IEC 61499 等可转换模型 | 状态机边界弱或需大量转换 | 非目标形式主义 / 非模型制品 | 待核 | 不适用 |
| NL 参与 | repair 输入同时含 NL 与 STM | 初始生成阶段含 NL，repair 阶段主要看模型 | 无 NL，但 repair 机制重要 | 与 NL/STM 无关 | 待核 | 不适用 |
| 反馈来源 | 结构化 diagnostics / verification / simulation / counterexample / proof | rule / test / consistency feedback | 人工审阅、弱反馈或非结构化反馈 | 无反馈 | 待核 | 不适用 |
| 自动化程度 | 无人化自动闭环 | 半自动，少量人工配置或选择 | 人在回路强依赖 | 手工方法 | 待核 | 不适用 |
| LLM / agent loop | 明确 LLM agentic repair loop | LLM self-refine / feedback regeneration | LLM 只做局部建议或前处理 | 无 LLM | 待核 | 不适用 |
| 可作为 baseline | 代码 / 数据 / 输入输出 / 许可基本可复验 | 可论文级重建或部分复现 | 只能概念对照 | 不可作为 baseline | 待核 | 不适用 |
| 资源可获取性 | 论文、代码、数据、输入输出、许可、版本清楚 | 关键资源部分公开 | 只能从论文图表 / 附录重建 | 关键资源不可得 | 待核 | 不适用 |

### 4.1 分类型字段

| 字段 | 推荐取值 |
|---|---|
| 当前角色 | 直接 baseline / 条件 baseline / 生成链内 feedback / 异构形式化近邻 / 模型一致性近邻 / 方法近邻 / negative evidence / 待核 |
| NL 类型 | 需求文本 / 用例 / 场景 / 系统描述 / 无 NL / 合成需求 / 待核 |
| STM 类型 | FSM / DFSM / HSM / EFSM / UML statechart / SysML SMD / IEC 61499 ECC / Stateflow / Timed automata / CSP# / Event-B / BPMN / 非目标 |
| feedback 类型 | 语法 / 结构 / 语义 / 需求一致性 / 仿真 / 测试 / 模型检查 / 反例 / 证明 / 用户反馈 / 无 |
| 使用方式 | 主 baseline 候选 / 消融参考 / related work / 转换压力 / negative sentinel / manual queue / 排除 |

## 5. 资源可获取性规则

资源可获取性必须分别判断，不得用一个“有 PDF”替代全部资产状态。最低资源列包括：

| 资源对象 | 判定要求 |
|---|---|
| 论文本体 | DOI、出版商页、arXiv、作者 PDF 或官方 proceedings。 |
| 代码 / 工具 | 作者仓库、artifact、Zenodo、OSF、supplement；需记录 release / commit / license 风险。 |
| NL / 输入数据 | 原始 requirements、use cases、system descriptions、model inputs 是否可直接取得。 |
| STM / 初始模型 | 作者原始 `STM_0`、partial STM、模型文件、PlantUML、XML、CSV 是否可取得。 |
| repaired 输出 | 修正后的 `STM_k`、repair trace、patch、result table 是否可取得。 |
| 原生 repair case | 是否有 `<输入, feedback, 输出>` 的可对齐 repair case。 |
| 许可与版本 | license、commit、hash、release、数据快照、下载日期。 |

**硬约束**：本仓库已有 PDF、parquet、ZIP、代码缓存，只能证明本地审计材料存在，不能自动算作论文一手公开资源。资源列必须给论文、作者、出版商、Zenodo、GitHub、OSF、Hugging Face 等一手链接；无法核验时写 `❓` 或 `🔴`。

## 6. 独立全文阅读规则

1. 凡进入 [SUMMARY.md](./SUMMARY.md) 正式 baseline / related 表且全文可获取的论文，默认必须由独立全文阅读任务完成全文阅读，产出可追踪要点。
2. 全文阅读必须覆盖摘要、引言、方法、实验/案例、artifact/data availability、结论，以及和 repair baseline 相关的关键段落。
3. 没有完成全文阅读的候选不得升级为 🟢 结论；只能留在候选池 / manual queue / 待核表。
4. 阅读结果写入单篇 `baseline_desc.md` 与 `artifacts.md`；横向结论再汇总到 [SUMMARY.md](./SUMMARY.md)。
5. 单篇 `baseline_desc.md` 必须写明：任务类型、输入、输出、STM 谱系、repair 机制、feedback 来源、自动化程度、LLM 角色、与本文关系、为什么可作为 baseline / related / negative、证据位置、风险。
6. 单篇 `artifacts.md` 必须写明：论文入口、作者资源、代码、数据、NL、STM、repair case、许可、版本、可复现阻塞、人工下载需求。

## 7. 检索覆盖与去重规则

每轮大范围检索必须在 [SUMMARY.md](./SUMMARY.md) 的检索覆盖表中记录：`检索切片`、`日期`、`来源/venue`、`query`、`命中数`、`初筛留存`、`全文入库`、`排除数`、`manual queue 增项`、`备注`。

去重优先级：DOI / arXiv ID > 标准化标题 > 标题 + 作者 + 年份。同一论文被多个切片命中时，正式候选表只保留一行，并在 `来源切片` 列合并 worker ID。

## 8. 人工下载队列

需要机构访问、登录、人工下载、或当前网络受阻的论文，进入 [manual_download_queue.bib](./manual_download_queue.bib)。`SUMMARY.md` 只记录队列状态和原因，不写长 BibTeX。

当用户补充 PDF 后，处理顺序为：

1. 放入对应单篇目录 `paper.pdf`。
2. 用 `tools/pdf_extractor.py` 生成 `paper_content.txt`。
3. 完成 `bibtex.bib`、`baseline_desc.md`、`artifacts.md`。
4. 更新 [SUMMARY.md](./SUMMARY.md) 候选表、资源表、manual queue 状态和更新日志。

## 9. 与 seed 文库的交叉链接

同一篇论文可以在两个文库中出现，但身份必须切片：

- [../seed_library/](../seed_library/) 记录 `NL -> STM_0` 关系；
- 本目录记录 `STM_0 -> STM_k`、feedback regeneration、completion、repair、diagnostics-to-repair 能力。

例如 `designing-fsm-gpt4` 的初始 CSV DFSM 生成属于 seed；oracle / trace / fault-model repair 属于本目录。`llms-emp` 的初始 STM 生成属于 seed；Phase-II feedback regeneration 属于本目录。

## 10. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 16:20:00 | PR-R1.8-C 初始化本 GUIDE，冻结 repair baseline 收录、emoji、资源、全文阅读和 crosslink 规则。 |
