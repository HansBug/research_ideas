# A1 最小闭环种子论文选择表

核验时间：2026-06-28 19:47:37 +0800

## 1. 结论速读

A1 选择 5 篇正选种子，目的不是建立最终 benchmark，而是给 A2 / A3 / A5a 提供真实论文压力：状态机槽位、SysML 多视图、公开数据集、合成 oracle / repair、私有工业数据这五类证据形态均被覆盖。

本轮正选：

1. [Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/)
2. [System Architects Are not Alone Anymore: Automatic System Modeling with AI](../../baselines/ttool-ai/)
3. [Generating SysML Behavior Models via Large Language Models: an Empirical Study](../../baselines/llms_emp/)
4. [Designing FSMs Specifications from Requirements with GPT 4.0](../../baselines/designing-fsm-specifications-from-requirements-gpt4/)
5. [Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering](../../baselines/req/)

核心判断：前 4 篇提供可公开审计的强锚点，第 5 篇故意保留为困难样本，用来迫使 A2 / A3 / A5a 正确处理“主题非常贴合但数据 / 代码不可公开”的工业证据边界。

## 2. 选择标准

状态列只放 emoji：🟢 = 当前可直接作为 A1 正选；🟡 = 可用但带重要限制；🟠 = 适合作为备选或压力线索；⚪ = 不进入 A1 正选。困难样本列采用文字分级：`强锚点 / 边界压力 / 主困难样本`，避免把所有正选都等价写成困难样本。

| 维度 | A1 要求 | 本轮执行方式 |
|---|---|---|
| 主题贴合 | 贴近 LLM4STM / LLM4Modeling / 状态机族模型生成或抽取。 | 正选均来自 [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md) 中五绿 direct baseline。 |
| 全文可审计 | 本地具备 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`，优先具备 `ASSETS.md`。 | 正选 5 篇全部满足。 |
| 维度压力 | 合计覆盖输入、输出、方法、工具、数据、制品、评价、缺失语义。 | 以覆盖矩阵记录，不用单一总等级替代。 |
| 困难样本 | 至少一篇必须暴露缺失 / 私有 / 证据定位 / 主张降级风险。 | 选择 `req` 作为私有工业数据困难样本，同时 `llms_emp` 和 `structure-and-event...` 也有制品边界压力。 |
| 非 cherry-picking | 必须保留备选 / 排除候选。 | 见 §6。 |

## 3. 正选种子总表

| seed_id | 状态 | 题名 / 路径 | 年份 | Venue / 状态 | 证据层级 | 本地证据 | 种子角色 | 困难样本 | A2 / A3 / A5a 交接 |
|---|---:|---|---:|---|---|---|---|---|---|
| A1-SEED-01 | 🟢 | [Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) | 2026 | arXiv / cs.SE（预印本 / 未经同行评审） | T0 | PDF / TXT / Bib / DESC / ASSETS | 状态机槽位与公开制品头牌样本 | 边界压力：输出边界复杂、证据定位困难、匿名制品漂移 | A2：输出类型树与证据锚点；A3：状态/迁移/守卫/动作槽位；A5a：来源锚点准确性和制品断链率 |
| A1-SEED-02 | 🟢 | [System Architects Are not Alone Anymore: Automatic System Modeling with AI](../../baselines/ttool-ai/) | 2024 | MODELSWARD | T0 | PDF / TXT / Bib / DESC / ASSETS | SysML 多视图 + 反馈循环样本 | 强锚点：多图输出、工具链反馈、语法/语义检查边界 | A2：多视图字段与反馈类型；A3：工具闭环 mini-case；A5a：反馈日志与错误分类 |
| A1-SEED-03 | 🟢 | [Generating SysML Behavior Models via Large Language Models: an Empirical Study](../../baselines/llms_emp/) | 2025 | Internetware / CCF C | T0 | PDF / TXT / Bib / DESC / ASSETS | 公开数据集 + SysML 行为模型混合样本 | 边界压力：行为模型类型混杂、代码未公开 | A2：模型类型切分和缺失 pipeline 语义；A3：state machine 子集抽样；A5a：公开数据 / 非公开代码分离 |
| A1-SEED-04 | 🟡 | [Designing FSMs Specifications from Requirements with GPT 4.0](../../baselines/designing-fsm-specifications-from-requirements-gpt4/) | 2026 | arXiv / cs.SE（预印本 / 未经同行评审；链接已于 2026-06-28 以 HTTP HEAD 方式复验返回 200） | T0 | PDF / TXT / Bib / DESC / ASSETS | 合成 DFSM + oracle / repair 样本 | 边界压力：合成数据、repair oracle、仓库未锁 release | A2：oracle / repair 字段；A3：fault model 幻觉陷阱；A5a：合成数据外推与修复成功证据 |
| A1-SEED-05 | 🟡 | [Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering](../../baselines/req/) | 2025 | Master’s Thesis | T0 | PDF / TXT / Bib / DESC / ASSETS | 工业控制系统 + 私有数据困难样本 | 主困难样本：私有数据、微调、专家评估、不可复现 | A2：受限证据 / 不可公开字段；A3：主张降级样本；A5a：artifact 可用性和 claim boundary 指标 |


### 3.1 正选种子最低字段审计表

本表把正选种子的最低字段展开，供 A2 / A3 / A5a 直接消费。`reading_level` 的含义是：既有 Project 1 baseline 文库已完成全文分析，本 PR-A1 复核了 `bibtex.bib`、`paper_content.txt`、`DESC.md`、`ASSETS.md` 与总账字段；A1 本身未重新跑作者代码，也未重新调用大语言模型。

字段映射说明：任务包中的“选择理由”对应本表 `inclusion_reason`，“下游消费者 / A2-A3-A5a 交接”由 `seed_role`、`scenario_mapping`、`expected_schema_stress` / `metric_hooks` 与 §7--§9 共同承担；后续机器检查若需要固定英文键，应优先消费这些已落表字段，而不是另造平行列名。

| `paper_id` / 论文ID | `normalized_title` / 标准题名 | DOI / 官方入口 | `local_evidence_path` / 本地证据路径 | `reading_level` / 阅读层级 | `evidence_tier` / 证据层级 | `selection_universe` / 选择母体 | `inclusion_reason` / 纳入理由 | `seed_role` / 种子角色 | `scenario_mapping` / 场景映射 | `baseline_threat_group` / 近邻威胁组 | D/P 层级 | `publicness_and_license` / 公开性与许可 | `artifact_status` / 制品状态 | `claim_allowed` / 可写主张 | `claim_forbidden` / 禁止主张 | `expected_schema_stress` / `metric_hooks` | `uncertainty_notes` / 不确定性 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1-SEED-01 | Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models | [arXiv:2604.00275](https://arxiv.org/abs/2604.00275) / [DOI](https://doi.org/10.48550/arXiv.2604.00275)；预印本 / 未经同行评审 | [../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) | 已有全文分析 + A1 资产复核 | T0 | Project 1 五绿 direct baseline | 最直接的自由文本到 UML 状态机样本，公开制品强 | 头牌公开制品种子 | A3 可选 1--2 个 4open reference solution 案例 | LLM4STM direct baseline | 评估=🟢；五条件全绿 | 论文公开；匿名 4open 制品需冻结和许可复核 | 代码 / 输入 / 参考解 / workbook 均可访问但无正式 DOI/release | 可说是强公开制品种子 | 不可说本 PR 已复跑或制品长期稳定 | 输出谱系、槽位证据、来源锚点准确性、断链率 | 匿名 artifact 可能漂移，正式运行前需本地冻结。 |
| A1-SEED-02 | System Architects Are not Alone Anymore: Automatic System Modeling with AI | [HAL](https://telecom-paris.hal.science/hal-04483279) / [DOI](https://doi.org/10.5220/0012320100003645) | [../../baselines/ttool-ai/](../../baselines/ttool-ai/) | 已有全文分析 + A1 资产复核 | T0 | Project 1 五绿 direct baseline | 覆盖多视图 SysML 与自动反馈循环 | 工具闭环种子 | A3 可选 platooning / spacebasedsystem / AutomatedBraking | LLM4Modeling tool-assisted baseline | 评估=🟢；五条件全绿 | 论文公开；GitHub 工件公开；复跑需 TTool 和 provider 配置 | 公开实验工件和结果表；非完整 TTool 源码 | 可说是多视图 / 反馈循环强近邻 | 不可把反馈循环写成形式化验证 | 多视图字段、反馈日志、错误分类、跨图一致性 | 结果受 provider drift 和工具环境影响。 |
| A1-SEED-03 | Generating SysML Behavior Models via Large Language Models: an Empirical Study | [ACM DOI](https://doi.org/10.1145/3755881.3755926) | [../../baselines/llms_emp/](../../baselines/llms_emp/) | 已有全文分析 + A1 资产复核 | T0 | Project 1 五绿 direct baseline | 有公开数据集与 36 个 state machine 子集 | 公开数据集种子 | A3 可从 state machine 子集抽样 | LLM4SysML behavior baseline | 评估=🟢；五条件全绿 | 论文公开；数据集公开；生成代码未公开 | Google Drive / 本地 parquet 可用；pipeline 缺失 | 可说是公开数据集强样本 | 不可说生成流程完全可复现 | 行为模型类型切分、公开数据/非公开代码分离、人工评分锚点 | 需要避免把 activity/sequence 混入 state machine 结论。 |
| A1-SEED-04 | Designing FSMs Specifications from Requirements with GPT 4.0 | [arXiv:2603.29140](https://arxiv.org/abs/2603.29140)；预印本 / 未经同行评审；2026-06-28 复验可访问 | [../../baselines/designing-fsm-specifications-from-requirements-gpt4/](../../baselines/designing-fsm-specifications-from-requirements-gpt4/) | 已有全文分析 + A1 资产复核 | T0 | Project 1 五绿 direct baseline | 覆盖 DFSM CSV、oracle 比较和 repair | repair / oracle 种子 | A3 可构造 fault-model 幻觉陷阱 | LLM4FSM repair baseline | 评估=🟢；五条件全绿 | 论文公开；GitHub 可访问但无 release/license | 数据和结果文件可见；不是冻结 replication package | 可说是合成 oracle + repair 种子 | 不可把合成数据外推为工业需求结论 | oracle 字段、repair 字段、合成数据边界、主张降级 | 需要保留合成数据和仓库未锁版本限制。 |
| A1-SEED-05 | Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering | [Chalmers ODR PDF](https://odr.chalmers.se/bitstreams/7c06ef2c-d1ae-40b4-b13c-a35087077bce/download) | [../../baselines/req/](../../baselines/req/) | 已有全文分析 + A1 资产复核 | T0 | Project 1 五绿 direct baseline | 主题最贴近工业控制状态图，但资产受限 | 困难 / 降级种子 | A3 只能使用论文正文可公开事实 | Industrial LLM4Statechart baseline | 评估=🟢；五条件全绿 | 论文公开；真实数据和代码私有 | 无公开训练/评测数据或代码 | 可说是私有工业数据困难样本 | 不可声称可复现或可公开 Volvo/Car Weaver 数据 | 受限证据语义、artifact 可用性、claim boundary、缺失处理 | 正适合测试“强相关但不可复现”的降级策略。 |

## 4. 覆盖矩阵

| seed_id | 输入 | 输出 | 输出谱系 | 方法 | 模型 / 工具 | 数据 / 制品 | 评价方式 | 主要风险触发 |
|---|---|---|---|---|---|---|---|---|
| A1-SEED-01 | 非结构化 reactive-system 描述 | UML 状态机 / Umple / HTML tables | UML state machine，含状态、迁移、守卫、动作、层次、并行、历史状态 | 单提示、结构驱动、事件驱动、Hybrid | GPT-4o、Claude 3.5 Sonnet、4open 制品 | 8 个系统描述、参考解、F1 workbook、匿名制品 | 槽位级 precision / recall / F1 | 匿名制品漂移；单提示与多步输出不完全同构；小样本外部效度 |
| A1-SEED-02 | 自然语言系统规范 + 知识库 + SysML 语法约束 | SysML 块图、内部块图、状态机图、TTool XML | SysML behavioral / structural views | 知识注入、自动反馈循环、JSON 到 SysML | ChatGPT / TTool-AI / TTool | GitHub 工件、`results.ods`、3 个核心系统 | 学生手工建模对比、质量评分、速度 | 反馈循环不等于形式化验证；多图一致性难抽取；provider drift |
| A1-SEED-03 | 自然语言需求 + PlantUML / SysML 规范 + few-shot / RAG | PlantUML 格式 SysML 行为模型 | state machine / activity / sequence diagrams | 五组件 prompt、RAG、few-shot、规则反馈修复 | LLM + PlantUML / SysML 规范 | Google Drive 数据集、本地 parquet；无生成代码 | 人工评分、错误分类、Phase-I/II | 36 个 state machine 子集需切分；数据公开但代码缺失；语义一致性难核验 |
| A1-SEED-04 | 合成英文 DFSM 需求描述 | CSV DFSM / Mealy machine | deterministic FSM / Mealy machine | GPT 生成、oracle 比较、distinguishing / checking sequence、fault model repair | GPT-4 / GPT-4o、作者 GitHub | 合成 oracle、`generated_text.csv`、结果文件；无正式 release | oracle 等价、fault / mutation repair、检查序列 | 合成数据不是工业需求；repair 依赖 oracle；仓库许可 / 依赖未锁 |
| A1-SEED-05 | Volvo Cars / Car Weaver 自然语言产品需求 | Mermaid.js 状态机 / statechart | automotive statechart | NLP 特征提取、合成数据、领域微调、专家评估 | GPT-3.5 / GPT-4 / GPT-4o 微调、Azure OpenAI | 论文公开；真实数据和代码私有 | 专家评分、功能正确性、可理解性 | 主题贴合但不可复现；私有数据不能公开；样本偏小和微调漂移 |

## 5. 正选种子逐篇说明

### 5.1 A1-SEED-01：结构驱动 / 事件驱动状态机生成

- **为什么入选**：最直接覆盖“非结构化自然语言 → UML 状态机”，且有公开输入、参考解、生成结果和 F1 workbook；能支撑 A2 设计状态机槽位证据对象。
- **可写主张**：可写为 A1 的强公开制品样本和 direct baseline。
- **禁止主张**：不能写成已由本 PR 复跑；不能声称其匿名制品具有长期归档保障。
- **A3 候选场景**：选 1--2 个 `bread-maker / dishwasher / printer / spa-manager` 等案例，构造状态 / 迁移 / 守卫 / 动作证据锚点。
- **A5a 指标钩子**：来源锚点准确性、状态机槽位错误分类、参考解断链率、制品冻结状态。

### 5.2 A1-SEED-02：TTool-AI 多视图系统建模

- **为什么入选**：提供自然语言规范到 SysML 多视图的工具闭环，能检验 A2 是否能同时表达状态机图和非状态机图的关系。
- **可写主张**：可写为工具链与反馈循环强近邻。
- **禁止主张**：不能把 TTool-AI 的语法 / 规则反馈写成模型检查或性质验证。
- **A3 候选场景**：优先使用 `platooning`、`spacebasedsystem` 或 `AutomatedBraking` 中明确包含状态机图的案例。
- **A5a 指标钩子**：反馈次数、错误类型、反馈前后字段变化、跨图一致性证据。

### 5.3 A1-SEED-03：SysML 行为模型实证研究

- **为什么入选**：它有公开数据集和本地 parquet 冻结，且明确包含 36 个 state machine diagrams，适合测试 A2 对混合行为模型的分类能力。
- **可写主张**：可写为公开数据集强样本。
- **禁止主张**：不能写成生成 pipeline 已公开，也不能把 activity / sequence 子集混入 state machine 结论。
- **A3 候选场景**：从 36 个 state machine 子集中抽 1--2 个带人类评分 / 错误标注的样本。
- **A5a 指标钩子**：模型类型分类准确性、公开数据与非公开代码的分离、人工评分证据锚点。

### 5.4 A1-SEED-04：合成 DFSM 与 repair

- **为什么入选**：它把自然语言、DFSM CSV、oracle 比较和 repair 串在一起，能逼 A2 区分生成、诊断、修复、oracle、fault model 等字段。
- **可写主张**：可写为 repair 型状态机生成种子。
- **禁止主张**：不能把合成描述等同于真实需求；不能把 GitHub 仓库写成正式 replication package。
- **A3 候选场景**：选择一条 missing transition / non-determinism / output fault 的合成例子，作为主张强度与 oracle 依赖测试。
- **A5a 指标钩子**：错误诊断证据、repair 成功支撑、合成数据外推风险。

### 5.5 A1-SEED-05：汽车状态图生成困难样本

- **为什么入选**：主题非常贴近控制系统状态机，但真实需求和代码不可公开；它能迫使 A2/A3/A5a 对“强相关但不可复现”的证据进行降级和边界管理。
- **可写主张**：可写为困难样本、工业需求边界样本。
- **禁止主张**：不能写成可复现实验数据，也不能声称可公开 Volvo / Car Weaver 原始需求。
- **A3 候选场景**：只使用论文正文中可引用的需求 / 状态图描述，不使用私有数据。
- **A5a 指标钩子**：受限证据标记、不可复现主张降级、专家评估证据边界。

## 6. 备选 / 排除候选

| candidate_id | 状态 | 论文 / 路径 | 证据层级 | 当前判断 | 未进正选原因 | 后续复查条件 |
|---|---:|---|---|---|---|---|
| A1-ALT-01 | 🟠 | [Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles](../../baselines/automated-extraction-protocol-state-machines-3gpp-specifications/) | T0 | 强长文档 / 协议 FSM 备选 | 输入是 3GPP 协议规范，域偏离控制系统；代码和 ground truth 未公开。 | 若 A3 需要长规格文档 / ensemble / condition-action span 困难样本，可替换 A1-SEED-05 或作为额外陷阱。 |
| A1-ALT-02 | 🟠 | [An Agentic Flow for Finite State Machine Extraction using Prompt Chaining](../../baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/) | T0 | 强 agentic / prompt chaining 线索 | GitHub 当前是仓库壳，源码和 ground truth 未公开；复现性弱。 | 若仓库放出源码 / rulebook / GT，优先升级为 agentic baseline；若 A3 启动时仍未公开上述资产，则自动降级为 ⚪ 排除或仅保留为 related work 线索。 |
| A1-ALT-03 | 🟠 | [Exploring How Well Llama3 can Generate State Machines Represented in Umple](../../baselines/umple/) | T0 | DSL / Umple 代码生成备选 | 工具链公开但 thesis 实验脚本、RAG 语料和 benchmark bundle 未公开；系统较简单。 | 若 A3 需要 DSL 编译 / pass@k / RAG 示例，可作为补充 mini-case。 |
| A1-REJ-01 | ⚪ | [Pushing the Generative Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts](../../baselines/pushing-the-generative-envelope-mbse-artifacts/) | T0 | 背景 / prompt 敏感性参考 | 只有两个 MBSE 题项，无代码、无结果包、无标准 benchmark；样本太小。 | 仅在 A6 related work 或 prompt / temperature 讨论中引用。 |

## 7. 对 A2 的字段压力

A2 至少应考虑以下字段族，而不是只做扁平表：

1. 输入材料：自由文本系统描述、系统规范、自然语言需求、长规格文档、合成描述、私有需求。
2. 输出谱系：UML 状态机、SysML 状态机、SysML 行为模型、DFSM / Mealy machine、Mermaid statechart、Umple code、协议 FSM。
3. 方法谱系：单提示、多步提示、结构驱动、事件驱动、Hybrid、RAG、反馈修复、工具链转换、领域微调、oracle repair。
4. 证据对象：论文正文、表格、图、外部仓库、结果 workbook、数据集、parquet 冻结、论文内专家评估、缺失说明。
5. 缺失语义：未公开代码、未公开数据、匿名制品无 release、私有工业数据、合成数据、论文内结果、可重建但未打包。
6. 主张强度：可复现强、可审计但不可复跑、主题贴合但私有、只有论文内说明、只能作背景。

## 8. 对 A3 的 mini-case 建议

最小闭环不宜一开始选择最顺滑的全部公开样本。建议 A3 至少包含：

1. 一个强公开制品样本：A1-SEED-01 或 A1-SEED-02。
2. 一个公开数据但代码缺失样本：A1-SEED-03。
3. 一个困难 / 降级样本：A1-SEED-05，或在需要长文档时替换为 A1-ALT-01。

A3 构造金事实 / 银事实时，应显式记录“无法支撑的字段”和“必须降级的主张”，不要只挑能完整抽取的字段。

## 9. 对 A5a 的运行前指标建议

A5a 至少要把以下风险转成指标定义或人工核验规则：

1. 来源锚点准确性：字段值是否能回到页码、章节、表格、图或外部制品。
2. 制品公开性分类准确性：公开、部分公开、私有、未公开、可重建但未打包是否区分。
3. 主张过强率：候选发现是否把私有 / 合成 / 小样本结果写成泛化结论。
4. 模型类型分类错误：state machine / behavior model / protocol FSM / Umple code 是否混淆。
5. 回填触发：若 A2 后续修改输出谱系或缺失语义，哪些种子需要回填。
6. 审计成本：每篇论文定位字段证据所需时间、外部制品访问次数和人工质疑次数。

## 10. 当前不确定性

1. A1 未复跑任何作者代码或 LLM；所有结论来自本地论文、`DESC.md`、`ASSETS.md` 与总账审计。
2. A1-SEED-01 的 4open 制品、A1-SEED-02 的 GitHub 工件、A1-SEED-03 的 Google Drive 数据集仍需在真实运行前冻结本地副本。
3. A1-SEED-05 的真实工业数据不可公开，因此只能作为困难样本和证据边界样本，不适合作为可复现实验主样本。
4. PR #97 仍未合入；本文件没有消费 PR #97 资产。
