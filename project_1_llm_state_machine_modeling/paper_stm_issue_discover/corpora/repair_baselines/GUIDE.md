# repair_baselines/GUIDE.md

> 🟡 **收录标准照旧；变的只是「这批文献服务谁」。**
>
> 2026-08 导师定调把 paper1 **收窄为 issue discover 单独成篇**，repair 另立后续论文。因此：
>
> | | 现状 |
> | :-- | :-- |
> | 本 GUIDE 的收录 / 排除 / 分级 / 去重规则 | 🟢 **全部照旧执行，一条不改**。repair 近邻工作仍然照原标准收 |
> | 下文「`NL + raw/source STM_0 -> source-level issue discovery / repair / closure` 主线」 | 🟡 读作**本文库自身的收录口径**，不是 paper1 的任务定义 |
> | 「本文 baseline」「严格全绿 baseline」这类措辞 | 🔴 paper1 **不做 repair，没有 repair baseline 可对照**。这些等级现在的含义是「作为后续 repair 论文 baseline 的成熟度」 |
>
> paper1 当前对本文库的两个用途：§Related Work 靶子文献，以及后续论文的 baseline 储备。
> 贡献口径见 [../../README.md](../../README.md) §2，定位变更见 [README.md](./README.md) 顶部。

## 1. 目标与边界

本 GUIDE 约束 `repair_baselines/` 的后续维护。本目录只记录与 `NL + raw/source STM_0 -> source-level issue discovery / repair / closure` 主线有关的 **修正、补全、refinement、consistency fixing、feedback-guided repair、verification / simulation / diagnostic feedback、LLM / agentic repair** 工作。

**硬定义**：能被写成本文 baseline 的工作必须同时满足：输入含 `NL` 与 `STM_0`；`STM_0` 明确由同一 `NL` 生成 / 派生；任务目标是发现 / 修复已有 `NL + raw/source STM_0` 中的 source-level behavioral issues，并给出 closure / regression evidence。只有 `STM + error / tests / oracle / diagnostics` 的 repair 工作，即使机制很强，也只能作为 repair-engine near-neighbor 或 related work。

不得把本目录写成旧 `NL -> STM` generation baseline 文库。若某工作只证明 `STM_0` 可由 `NL` 生成，但没有修正或 feedback 环节，应进入 [../seed_library/](../seed_library/)；若某工作只有控制系统 NL 数据，应留给 [../nl_datasets/](../nl_datasets/)。

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
| 路线近邻 / 条件对照 | 本库里最接近 `NL + raw/source STM_0 -> source-level issue discovery / repair / closure` 主任务、且适合作为写作与汇报优先展开的条目。它**不**表示严格 baseline 已成立；若仍有关键条件待核，必须在 [SUMMARY.md](./SUMMARY.md) 中单独写出缺口，不能因“条件对照”四字自动升级。 |
| 前驱 / 条件线索 | 与主任务存在方法史或任务史上的前后承接关系，但通常只提供生成前史、历史原型或术语线索，不直接满足 `NL + raw/source STM_0 -> source-level issue discovery / repair / closure`。 |
| 直接 STM 修正近邻 | 明确存在 `STM_0 -> STM_k`、state machine repair、statechart repair、transition completion、guard/action correction，但缺少 NL 或 `NL -> STM_0` 关系。 |
| 模型制品补全 / 修复 | UML / SysML / Stateflow / IEC 61499 / behavioral model artifact 的 completion、refinement、consistency fixing。 |
| 反馈驱动修复 | checker、verification、simulation、testing、diagnostic、counterexample、proof feedback 进入模型修正。 |
| LLM / agentic repair | LLM self-repair、multi-step repair、agent loop、reviewer-feedback repair，用于模型制品或可映射形式模型。 |
| generation pipeline 中的修正环节 | `NL -> STM` 工作若有 check / feedback / refinement / repair，登记其 repair slice，并 crosslink seed 文库。 |

### 3.2 排除对象

| 排除对象 | 处理 |
|---|---|
| 只做 `NL -> STM_0` 且无修正环节 | 排除出本库核心，回到 seed 文库。 |
| `STM + error / tests / oracle / diagnostics` 但无 NL 或无 `NL -> STM_0` 关系 | 只可作为 repair-engine near-neighbor / related work，不能称本文 baseline。 |
| 纯 program repair / test repair / build repair | 只可作为远背景，不入正式 baseline 表。 |
| 纯 NL requirement rewriting | 不入本库；如有 NL 数据价值留给 [../nl_datasets/](../nl_datasets/)。 |
| BPMN / Petri / CSP / Event-B / TLA+ / Alloy 等非 STM family | 只有当 repair feedback 机制对本文非常关键时，作为异构 related / negative evidence 入账，不能写成同构 baseline。 |
| protocol FSM / 3GPP / RFC FSM | 默认 out-of-domain；只保留少量哨兵，避免混入控制系统 STM 任务。 |

## 4. emoji / enum 标准

正式表格中，emoji 列只写 emoji，中文释义集中写在本节和 [SUMMARY.md](./SUMMARY.md)。有偏序关系的维度默认按 **🟢 > 🟡 > 🟠 > 🔴** 表达；`❓` 表示待核，`⚪` 表示不适用。

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| NL 参与 | repair 输入同时含 NL 与 STM | 初始生成阶段含 NL，repair 阶段主要看模型 | 有 NL 但与 repair 输入关系弱，或仅作背景 | 与 NL/STM 无关 | 待核 | 不适用 |
| `STM_0` 输入 | repair / completion 输入明确包含初始 STM 或 partial STM | 有初始模型制品，但是否为 STM 或 repair 输入需重建 | 只有非 STM 模型制品或弱初始制品 | 无初始 STM / 模型输入 | 待核 | 不适用 |
| `NL -> STM_0` 关系 | `STM_0` 明确由同一 NL 生成 / 派生，且作为 repair 输入 | NL 与 `STM_0` 有强 trace / 补全关系，但骨架或生成过程需人工重建 | 只有 NL 或只有 STM，或二者关系弱 | 无 `NL -> STM_0` 关系 | 待核 | 不适用 |
| 修正任务匹配 | 明确同构 `NL + raw/source STM_0 -> source-level issue discovery / repair / closure` repair / completion | `STM_0 -> STM_k` 或模型制品 repair，可较清楚映射到 STM | 只有局部 feedback / consistency / completion 线索 | 无 repair / feedback | 待核 | 不适用 |
| STM 谱系匹配 | T0+FSM/HSM/EFSM/statechart 明确 | UML/SysML/Stateflow/IEC 61499 等可转换模型 | 状态机边界弱或需大量转换 | 非目标形式主义 / 非模型制品 | 待核 | 不适用 |
| 反馈来源 | 结构化 diagnostics / verification / simulation / counterexample / proof | rule / test / consistency feedback | 人工审阅、弱反馈或非结构化反馈 | 无反馈 | 待核 | 不适用 |
| 自动化程度 | 无人化自动闭环 | 半自动，少量人工配置或选择 | 人在回路强依赖 | 手工方法 | 待核 | 不适用 |
| LLM / agent loop | 明确 LLM agentic repair loop | LLM self-refine / feedback regeneration | LLM 只做局部建议或前处理 | 无 LLM | 待核 | 不适用 |
| 可作为 baseline | 代码 / 数据 / 输入输出 / 许可基本可复验 | 可论文级重建或部分复现 | 只能概念对照 | 不可作为 baseline | 待核 | 不适用 |
| 资源可获取性 | 论文、代码、数据、输入输出、许可、版本清楚 | 关键资源部分公开 | 只能从论文图表 / 附录重建 | 关键资源不可得 | 待核 | 不适用 |

### 4.1 分类型字段

| 字段 | 推荐取值 |
|---|---|
| 当前角色 | 严格 baseline / P0 路线近邻 / 条件对照 / 前驱 / 条件线索 / 生成链内 feedback / repair-engine 近邻 / 异构形式化近邻 / 模型一致性近邻 / 方法近邻 / negative evidence / 待核 |
| NL 类型 | 需求文本 / 用例 / 场景 / 系统描述 / 无 NL / 合成需求 / 待核 |
| STM 类型 | FSM / DFSM / HSM / EFSM / UML statechart / SysML SMD / IEC 61499 ECC / Stateflow / Timed automata / CSP# / Event-B / BPMN / 非目标 |
| feedback 类型 | 语法 / 结构 / 语义 / 需求一致性 / 仿真 / 测试 / 模型检查 / 反例 / 证明 / 用户反馈 / oracle / 无 |
| 使用方式 | 路线近邻 / 条件对照 / 前驱线索 / 消融参考 / related work / 转换压力 / negative sentinel / manual queue / 排除 |

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

## 6. 全文阅读与旁路核验规则

1. 凡进入 [SUMMARY.md](./SUMMARY.md) 正式 baseline / related 表且全文可获取的论文，最低要求是完成可追溯全文阅读，并在单篇文件中给出证据位置；阅读可以来自主 session 全文阅读、独立 subagent 全文阅读，或二者组合。
2. P0/P1 强候选与后续可能进入实验 baseline 的论文，优先安排独立 subagent 复核；若本轮只完成“主 session 全文阅读 + 旁路核验材料”，应在单篇 `baseline_desc.md` 的“阅读来源”中如实标注。
3. 全文阅读必须覆盖摘要、引言、方法、实验/案例、artifact/data availability、结论，以及和 repair baseline 相关的关键段落。
4. 没有完成全文阅读或可靠 HTML 全文核验的候选不得升级为正式结论；只能留在候选池 / manual queue / 待核表。
5. 阅读结果写入单篇 `baseline_desc.md` 与 `artifacts.md`；横向结论再汇总到 [SUMMARY.md](./SUMMARY.md)。后续若某条目被选为可复现实验 baseline，应补充 reader / task ID、版本和复验命令。
6. 单篇 `baseline_desc.md` 必须写明：任务类型、输入、输出、STM 谱系、repair 机制、feedback 来源、自动化程度、LLM 角色、与本文关系、为什么可作为 baseline / related / negative、证据位置、风险。
7. 单篇 `artifacts.md` 必须写明：论文入口、作者资源、代码、数据、NL、STM、repair case、许可、版本、可复现阻塞、人工下载需求。

## 7. 检索覆盖与去重规则

每轮大范围检索必须在 [SUMMARY.md](./SUMMARY.md) 的检索覆盖表中记录：`检索切片`、`日期`、`来源/venue`、`query`、`粗略命中`、`§2.1 去重候选`、`入库`、`人工队列`、`待核`、`降级/negative`、`备注`。其中粗略命中可保留检索噪声估计，不参与精确复算；其余统计必须能从候选池 / 筛查账按来源切片复算。

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

例如 `designing-fsm-gpt4` 的初始 CSV DFSM 生成属于 seed；oracle / trace / fault-model repair 属于本目录，但因 repair 输入主要是 `STM + oracle/trace/fault-model`，不能写成本文真 baseline。`llms-emp` 的初始 STM 生成属于 seed；Phase-II feedback regeneration 属于本目录，但同样只作生成链内 feedback 近邻。

## 10. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 18:35:00 | 收紧本文 baseline 硬定义，新增 `STM_0` 与 `NL -> STM_0` 维度，并明确无 NL / 无 `NL -> STM_0` 的 repair 工作只能作为 near-neighbor 或 related work。 |
| 2026-06-15 17:40:00 | 放宽全文阅读合同为“可追溯全文阅读 + P0/P1 优先独立复核”，避免把 PR 施工调度误写成不可满足的长期文库硬约束。 |
| 2026-06-15 16:20:00 | PR-R1.8-C 初始化本 GUIDE，冻结 repair baseline 收录、emoji、资源、全文阅读和 crosslink 规则。 |
