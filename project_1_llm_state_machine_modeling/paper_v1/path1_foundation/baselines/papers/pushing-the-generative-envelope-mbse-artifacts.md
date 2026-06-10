# pushing-the-generative-envelope-mbse-artifacts

## 0. 元信息与 source pointer

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `crabb2025pushing` |
| 论文 | *Pushing the (Generative) Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts* |
| 作者 / 年份 | Erin Smith Crabb, Cedric Bernard, Matthew T. Jones, Daniel Dakota / 2025 |
| Venue | Proceedings of Recent Advances in Natural Language Processing, RANLP 2025 |
| DOI / URL | `10.26615/978-954-452-098-4-137` / <https://aclanthology.org/2025.ranlp-1.137/> |
| 原始目录 | `project_1_llm_state_machine_modeling/baselines/pushing-the-generative-envelope-mbse-artifacts/` |
| 本篇定位 | direct baseline 证据项，但更适合支撑 prompt technique / temperature / local LLM 可行性讨论；不适合作为主 same-sample baseline，因为样本极小、无代码/输出包、无 in-loop checker 或可执行语义。 |

主要 source pointer：

> 以下未带目录前缀的 source pointer 均相对于上表“原始目录”；跨库文件使用完整相对路径。

- 元信息：`bibtex.bib:1-8`；`DESC.md:5-12`；`ASSETS.md:21-24`。
- 任务与动机：`paper_content.txt:11-30`（摘要）、`paper_content.txt:31-71`（MBSE/SysML v2、requirements list 与 state machine diagrams）。
- 模型与运行成本：`paper_content.txt:107-153`（Mixtral、Smaug、EC2、成本/时间约束）。
- prompt 与样本：`paper_content.txt:176-230`（MBSE/SysML v2 知识、dot notation、air purifier/vacuum、zero/one/few-shot）。
- 评测：`paper_content.txt:231-264`（expert gold exemplar、dot notation、METEOR、100 runs）、`paper_content.txt:265-376`（Mixtral/Smaug/CoT 结果）。
- 温度与局限：`paper_content.txt:377-444`（t-tests、semantic equivalence、limitations/conclusion）。
- 资产：`ASSETS.md:13-17`、`ASSETS.md:26-46`。

## 1. 阅读审计

| 文件 | 已读范围 | 用途 | 关键注意 |
|---|---|---|---|
| `bibtex.bib` | 全文 `1-8` | 元信息、DOI、ACL Anthology URL | BibTeX 未给页码；页码来自 `paper_content.txt:2-4`。 |
| `paper_content.txt` | 全文 `1-534`，覆盖摘要、引言、相关工作、实验设置、结果、局限、结论 | 抽取输入、prompt、模型、评测与局限 | 这是 prompt technique + METEOR/SME 评测研究，不是 checker/repair/verification pipeline。 |
| `DESC.md` | 全文 `1-136` | 复核中文摘要、任务定位、模型、局限 | `DESC.md` 已标注 direct baseline，但本文件需把可复现性和语义强度降级。 |
| `ASSETS.md` | 全文 `1-46` | 代码、数据、结果包与风险 | 明确无公开代码、无数据包、无 supplementary / 输出包。 |
| `project_1_llm_state_machine_modeling/baselines/SUMMARY.md` | 对应行 `127` 与数据集表 `254` | 复核五绿总账定位 | 总账已将其定位为 evidence-only / prompt-technique evidence。 |

## 2. 表 A：方法框架与任务定位

| 输入 NL | 任务目标 | agent/prompt 模式（多选 tag+解释） | LLM 模型四元组 | 输出 STM 类型（类型+语义能力/可执行性/guard/action/hierarchy/time/concurrency/应用场景/与本项目差距） | 人在回路角色 | 输出后人工改动 |
|---|---|---|---|---|---|---|
| 简短物品/系统描述与生成指令，例如 vacuum / air purifier；不是工业控制需求集。Source: `paper_content.txt:197-212`, `paper_content.txt:213-220`。 | 评估 local/open LLM 能否生成初始 SysML v2 artifacts，并测量 prompt technique 与 temperature 对 requirements list 和 state machine diagrams 的影响。Source: `paper_content.txt:62-71`, `paper_content.txt:197-212`。 | `zero-shot`：只给简单生成指令；`one-shot/few-shot`：给不同目标领域的 SysML v2 示例；`CoT`：先生成 requirements list，再用其支持 state machine design；`temperature-ablation`：0.2/0.6/0.95；`dot-notation-normalization`：为绕开 SysML v2 格式知识不足。不是 agentic loop，也没有 feedback repair。Source: `paper_content.txt:176-230`, `paper_content.txt:325-376`。 | Mixtral-8x7B-Instruct-v0.1 / Mistral open model / local EC2 `p4d.24xlarge` / 46.7B sparse MoE；Llama-3-Smaug-8B / Smaug open model / local EC2 `g4dn.12xlarge` / 8.03B DPO-Positive；每个设置 100 runs，temperature 0.2/0.6/0.95。注意原文 footnote URL 显示 `Smaug-72B-v0.1`，与正文 “8B/8.03B” 有命名风险。Source: `paper_content.txt:122-153`, `paper_content.txt:197-212`。 | 输出包括 SysML v2 requirements list 与 state machine diagrams；为了评测，作者使用 dot notation versions 而非严格 SysML v2 textual syntax。状态机语义主要是状态/迁移/标签层面的图工件；无可执行 runner，无 guard/action/hierarchy/time/concurrency 的系统化 schema，也无控制系统 scenario trace。应用场景是 MBSE 初稿辅助；与本项目差距在于非控制系统、非可执行 STM、无检查/修复闭环。Source: `paper_content.txt:51-66`, `paper_content.txt:189-194`, `paper_content.txt:231-264`。 | SME 和 systems engineering expert 主要在事后：专家产生 gold-standard exemplar，SME reviews 解释 one/few-shot 差异；没有证据表明 SME 在生成流程内逐轮反馈。Source: `paper_content.txt:231-264`, `paper_content.txt:325-337`。 | Gold exemplars 被翻译成 dot notation；生成输出也转成 dot notation 做 METEOR。没有公开逐次输出，也没有报告人工后编辑生成图后再计分。CoT 生成的 900 requirements lists 未计入最终评分。Source: `paper_content.txt:242-253`, `paper_content.txt:414-419`, `ASSETS.md:15-17`。 |

## 3. 表 B：资产状态与可复现性

| 稳定引用键 | 论文与版本 | Reference/GT | 数据与 artifact | 已有本地复现资产 | 可复现路径 | 资源许可与访问风险 |
|---|---|---|---|---|---|---|
| `crabb2025pushing`。Source: `bibtex.bib:1`。 | RANLP 2025 ACL Anthology 公开论文，DOI `10.26615/978-954-452-098-4-137`。Source: `bibtex.bib:4-8`, `ASSETS.md:13`。 | 每个 item 有 systems engineering expert 产生的 gold-standard exemplar，并翻译成 dot notation；没有公开 GT 文件。Source: `paper_content.txt:242-253`。 | 只有论文内描述、表格和 SME feedback；未发现 GitHub、OSF、Zenodo、supplementary、逐次输出包或独立 benchmark。Source: `ASSETS.md:13-17`, `ASSETS.md:28-36`。 | 本地仅有 PDF、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md`；无本地结果包。Source: `ASSETS.md:13-17`。 | 只能 approximate：手工重建 prompts、选择相同/近似 local models、设置 temperature 与 100 runs、构造 gold dot notation、跑 METEOR，再请 SME 审核；由于 prompts/outputs/GT 不公开，不能称 replication。Source: `paper_content.txt:197-264`, `ASSETS.md:38-46`。 | 样本只有 air purifier / vacuum，外推性弱；local model 精确版本存在 Smaug 命名不一致；模型许可、EC2 成本和随机性需另行锁定；RANLP 非 CCF 口径。Source: `paper_content.txt:135-149`, `paper_content.txt:414-444`, `ASSETS.md:42-46`。 |

## 4. 表 C：生成流程内反馈

> 本表只统计 in-loop feedback。METEOR、SME comments、expert exemplar 和 t-tests 都是 post-hoc evaluation / analysis，不得写成生成流程内反馈。

| 静态/schema | 编译/可执行性 | oracle/trace/等价性 | 仿真执行 | 形式化验证 | 人类过程反馈 | 反馈粒度 | 反馈自动化程度 | 人类反馈交叉一致性 |
|---|---|---|---|---|---|---|---|---|
| 无 in-loop schema checker。作者因 SysML v2 格式知识不足，改用 dot notation 评估内容，未报告生成时自动 parse/validate。Source: `paper_content.txt:189-194`, `paper_content.txt:231-264`。 | 无。没有编译、渲染、TTool/PlantUML parser 或可执行状态机检查。Source: `paper_content.txt:231-264`, `ASSETS.md:15-17`。 | 无流程内 oracle/trace。Gold exemplar 与 METEOR 是生成后比较；不是反馈给 LLM 的修复信号。Source: `paper_content.txt:242-264`。 | 无。论文只评估生成文本/图工件，未执行仿真。Source: `paper_content.txt:31-50`, `paper_content.txt:414-444`。 | 无。没有 model checker、theorem prover、SAT/SMT 或形式化引擎。Source: `paper_content.txt:231-264`。 | 无 in-loop 人类反馈。SME reviews 是事后解释 prompt 差异，并触发作者另做 CoT 实验设计，但不是同一次生成中的在线反馈。Source: `paper_content.txt:325-337`。 | 不适用；CoT 的“先生成 requirements list 再生成 state machine”是 prompt decomposition，不是错误反馈。Source: `paper_content.txt:325-337`。 | 低；生成流程本身只是 prompt+temperature 采样，评测自动化为 METEOR。Source: `paper_content.txt:251-264`。 | 未报告 SME 数量、评分 rubric 细则或交叉一致性统计。Source: `paper_content.txt:231-264`, `paper_content.txt:325-337`。 |

## 5. 表 D：事后评测、指标与证据强度

| 评测项 | 指标 / 结果 | 证据强度 | 对 Path-1 的使用方式 | source pointer |
|---|---|---|---|---|
| METEOR 平均分 | 每个 item/artifact/temperature/prompt 设置跑 100 次，用 generated dot notation 与 expert gold dot notation 比较并报告平均 METEOR。 | 中低：流程清楚，但 GT/outputs 不公开，METEOR 偏 lexical。 | 可作为 prompt/temperature sensitivity 的 supporting evidence，不能作为强语义正确性证据。 | `paper_content.txt:242-264` |
| prompt technique | Mixtral 上 requirements list 通常 one-shot 更好；state machine 中 air purifier 提升不明显，vacuum 更接近 requirements list 的趋势；CoT 对 vacuum state machine 有明显帮助。 | 中低：样本只有 2 个 items。 | 说明 prompt technique 影响大，不能把 baseline 差异全归因于模型能力。 | `paper_content.txt:267-277`, `paper_content.txt:368-376` |
| local model feasibility | Smaug 在部分任务上接近或超过 Mixtral；作者认为较小 local models 具备支持 MBSE 初稿的潜力。 | 中低：只测两个模型，且模型命名需复核。 | Related Work 可写 local/open model path 已被探索。 | `paper_content.txt:313-324`, `paper_content.txt:427-444` |
| temperature | 平均分看似稳定，但 t-tests 显示许多 temperature pairs 的 underlying distribution 有显著差异；语义等价不同表达会影响表层分数。 | 中：分析有统计检验，但无原始输出。 | 可用于实验设计中要求固定 temperature、run count 和 output normalization。 | `paper_content.txt:377-413` |
| SME feedback | SME 指出过长 examples 可能诱发更长 response 和 hallucinations，作者因此尝试 CoT。 | 弱：缺 rubric/一致性。 | 只能作为 qualitative observation，不能写成可复现人类反馈闭环。 | `paper_content.txt:325-337` |
| 资产证据 | 无代码/数据/输出包。 | 弱 | 不进入 S3 主 baseline；最多手工重建小样本 sanity check。 | `ASSETS.md:13-17`, `ASSETS.md:42-46` |

## 6. 表 E：同样本近似与可比性决策

| 维度 | 决策 | 理由与 source pointer |
|---|---|---|
| 输入可同样本性 | 低。 | 只有 air purifier / vacuum 两个简短题项，且 prompts/GT 未成包。Source: `paper_content.txt:197-212`, `ASSETS.md:30-36`。 |
| 输出可归一性 | 低到中。 | state machine diagrams 以 dot notation 评测，可映射状态/迁移，但不是本项目可执行 STM schema，也无 guard/action/time/hierarchy 标准字段。Source: `paper_content.txt:189-194`, `paper_content.txt:395-413`。 |
| 模型预算 | 中高。 | 每设置 100 runs，作者称即使两个 local models 也需 6-8 小时且每 100 runs 至少约 500 美元。Source: `paper_content.txt:135-149`。 |
| 人在回路预算 | 高且不可控。 | 需要 systems engineering expert gold 与 SME qualitative review，原文未公开 rubric/一致性。Source: `paper_content.txt:231-264`, `paper_content.txt:325-337`。 |
| 反馈预算 | 无。 | 没有 in-loop feedback，可作为 prompt ablation，不适合作为 repair/checker baseline。Source: `paper_content.txt:213-230`, `paper_content.txt:325-337`。 |
| GT 可得性 | 低。 | Gold exemplars 只在论文方法中描述，未公开文件。Source: `paper_content.txt:242-253`, `ASSETS.md:15-17`。 |
| 最终可比性决策 | **evidence-only**。 | 适合作为“prompt technique 与 local LLM 已被用于 SysML state machine 初稿”的证据；不建议纳入主 same-sample approximate baseline。 |

## 7. 表 F：Claim 风险与 handoff

| 类型 | 内容 | 风险等级 | handoff |
|---|---|---|---|
| 会被打穿的 claim | “没有人评估 prompt technique/temperature 对 SysML state machine generation 的影响”；“local LLM 不能生成 MBSE state machine 初稿”。 | M | S1b Related Work 中可一笔承认该小样本研究。 |
| 需要弱化的 claim | 可写“已有小样本研究比较了 zero/one/few-shot、CoT 和 temperature；本文聚焦更复杂控制系统需求、可执行 STM schema 与反馈/审计链”。 | M | 避免把 prompt trick 写成核心 novelty。 |
| 不能误写的点 | METEOR/SME 是 post-hoc evaluation；没有 in-loop checker、simulation、formal verification、repair loop；state machine diagram 不等于可执行控制 STM。 | I | S1b/S3 都不要把它列为 checker baseline。 |
| S1b handoff | 放在 prompt/temperature/local model 相关工作或 baseline matrix 的 evidence-only 行。 | M | 关联 `project_1_llm_state_machine_modeling/baselines/SUMMARY.md:127`。 |
| S3 handoff | 不进入主对比；若有余力，可复刻两个题项做 prompt sanity check，但要标注 approximate/manual GT。 | M | 关联 `ASSETS.md:38-46`。 |

## 8. 待补与风险

1. **模型精确版本需复核**：正文称 Llama-3-Smaug-8B/8.03B，footnote URL 指向 Smaug-72B-v0.1；若未来重跑需从作者或 artifact 进一步确认。
2. **缺 GT 与输出**：无 gold dot notation、100-run generations、prompt full text包；不能做强复现。
3. **评测语义较弱**：METEOR 能容忍部分同义表达，但仍不是状态机行为等价。
4. **样本过小**：air purifier / vacuum 不代表控制系统或安全关键需求；只能作为 prompt sensitivity evidence。
