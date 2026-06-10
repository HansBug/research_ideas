# Automotive Statechart / 汽车自然语言需求到 Statechart

## 0. 元信息与 source pointer

| 项目 | 内容 | Source pointer |
|---|---|---|
| 稳定引用键 | `kurukuri_automated_nodate` | `project_1_llm_state_machine_modeling/baselines/req/bibtex.bib:2-11` |
| 论文 | Lakshmi Sri Rupa Kurukuri, *Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering*, Master's Thesis, 2025 | `.../bibtex.bib:2-11`; `.../DESC.md:5-16` |
| 本地原始目录 | `project_1_llm_state_machine_modeling/baselines/req/` | 本任务指定路径；`.../ASSETS.md:13-17` |
| 主要 source pointer 简写 | `P=`同目录 `paper_content.txt`；`D=`同目录 `DESC.md`；`A=`同目录 `ASSETS.md`；`S=` `project_1_llm_state_machine_modeling/baselines/SUMMARY.md` | 本文下方表格使用这些简写，但均指向上述原始目录 |
| 关键证据线索 | 任务与动机：`P:47-72`, `P:220-258`, `P:548-572`；方法：`P:710-746`, `P:747-883`, `P:882-990`, `P:1005-1031`, `P:1054-1180`；结果：`P:1407-1515`, `P:1539-1685`, `P:1690-1842`；附录测试样例：`P:1999-2117`；资产：`A:13-17`, `A:30-46` | 逐项结论见各表 Source pointer 列 |

## 1. 阅读审计

| 材料 | 已读范围 | 结论 | Source pointer |
|---|---|---|---|
| `bibtex.bib` | 全文 11 行 | 确认 2025 硕士论文、作者、Chalmers ODR PDF URL；BibTeX key 仍保留 `nodate` 但 `year=2025`。 | `.../bibtex.bib:2-11` |
| `paper_content.txt` | 覆盖摘要、引言、背景/相关工作、方法、数据收集/预处理/合成数据/微调、评估、结果、讨论、附录测试样例 | 任务与 Project 1 高度同构（汽车 NL requirements -> statechart），但数据、代码、评分原表和专家过程均非公开。 | `P:47-72`, `P:548-690`, `P:710-1180`, `P:1407-1685`, `P:1690-1842`, `P:1999-2117` |
| `DESC.md` | 全文阅读 | 既有派生文件记录了 Volvo/Car Weaver 私有数据、GPT 微调、Mermaid 输出和专家评分；可迁移为方法证据，不可复现实验。 | `D:14-16`, `D:18-115`, `D:139-250`, `D:265-307`, `D:575-648` |
| `ASSETS.md` | 全文阅读 | 论文公开；代码、训练数据、Car Weaver 数据、专家评分原始表和复现包均未公开；明确不主动把潜在联系写成公开申请路径。 | `A:13-17`, `A:30-46` |
| `SUMMARY.md` 对应行 | 核对 direct baseline 总账行 | 总账记录该项为五绿 direct baseline，但资产列标为 Volvo/Car Weaver 内部需求 + statecharts、无公开申请入口。 | `S:124`, `S:251` |

## 2. 表 A：方法框架与任务定位

| 字段 | 本篇结论 | Source pointer |
|---|---|---|
| 输入 NL | Volvo Cars / Car Weaver 中的自然语言 product function requirements；主数据为 20 个产品功能需求，测试集为 12 个由领域专家创建且排除在训练/合成数据外的 test cases。 | `P:594-611`, `P:710-746`, `D:24-26`, `A:16`, `A:32` |
| 任务目标 | 在汽车软件工程环境中自动从非结构化自然语言需求生成 statecharts，并比较微调 LLM 与基础 LLM、人工 statecharts 的功能正确性和可理解性。 | `P:548-572`, `P:580-611`, `P:627-646`, `D:20-27` |
| agent/prompt 模式（多选 tag+解释） | `fine-tuning`：Azure AI Foundry 上微调 GPT-3.5 Turbo / GPT-4 / GPT-4o；`supervised prompt-completion`：把文本需求转为 JSON prompt-completion pairs；`synthetic data`：从 20 个真实需求抽取 states/events/transitions/actions 后随机化扩充；`NLP preprocessing`：spaCy NER、POS tagging、JSON transformation；不是 agent loop，也不是 prompt chaining / RAG。 | `P:747-883`, `P:882-990`, `P:1005-1031`, `D:139-205` |
| LLM 模型四元组 | 模型：GPT-3.5 Turbo、GPT-4、GPT-4o；provider/平台：OpenAI 模型经 Azure AI Foundry / Azure OpenAI 微调与部署；调用/训练：batch size 16/32、learning rate 1.01/1.05、epoch 5/8、seed 42 的多轮 fine-tuning；版本锁：未给 Azure deployment id、模型 snapshot、训练数据 hash 或 API 日期。 | `P:984-990`, `P:1005-1031`, `P:1046-1080`, `D:192-205` |
| 输出 STM 类型 | Final output 是 Mermaid.js syntax / rendered statechart，训练/预处理阶段还出现 structured JSON statechart 表示。语义能力：states/events/transitions/actions；可执行性：Mermaid 主要用于渲染/可视化，未接 simulator 或 model checker；guard/action：动作和事件可文本化，复杂 guard/time 处理弱；hierarchy/time/concurrency：Statechart 理论支持，但本文输出未证明系统支持层次/并发/时间；应用场景：汽车早期建模草图和专家评审；与本项目差距：缺 pyfcstm 可执行语义、控制变量、scenario trace、自动反馈修复和公开 benchmark。 | `P:747-883`, `P:1163-1166`, `P:1400-1406`, `P:1717-1721`, `D:206-209`, `D:575-648` |
| 人在回路角色 | 强人在回路但多为数据/评测环节：Car Weaver 需求与人工 statecharts 来自 Volvo；domain experts 选作 evaluator；合成数据变异由人工/领域专家 review；四位 Volvo product simulation team 专家用 Likert 和访谈评估输出。 | `P:651-672`, `P:967-982`, `P:1153-1180`, `P:1407-1419`, `P:1525-1538`, `A:16`, `A:32` |
| 输出后人工改动 | 原文强调 LLM 生成 statecharts 仍需专家验证/细化，附录对 AI vs manual statecharts 做对比；但未公开逐输出人工修订记录，也没有把专家意见回灌到模型再生成。 | `P:1583-1642`, `P:1733-1742`, `P:1818-1829`, `P:1999-2117` |

## 3. 表 B：资产状态与可复现性

| 字段 | 本篇结论 | Source pointer |
|---|---|---|
| 稳定引用键 | `kurukuri_automated_nodate` | `.../bibtex.bib:2-11` |
| 论文与版本 | Chalmers University of Technology / University of Gothenburg Master's Thesis，2025；非 CCF venue。 | `D:5-12`, `A:21-24` |
| Reference / GT | Reference 是 Volvo Cars / Car Weaver 内部 requirements 及对应人工 statecharts；12 个专家测试用例与 manual statecharts 用于比较；不公开。 | `P:710-746`, `P:1153-1180`, `P:1521-1568`, `A:16`, `A:32` |
| 数据与 artifact | 无公开实验代码、训练脚本、数据集、专家评分原始表或复现包；论文只提供正文结果、附录问题与部分测试描述。 | `A:13-17`, `A:26-36`, `P:1999-2117` |
| 已有本地复现资产 | 本地四件套：`paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`、`ASSETS.md`；没有 Volvo 数据、Azure 微调配置文件、Mermaid 输出包或评分表。 | `A:13-17`, `A:30-36` |
| 可复现路径 | 不能复现原实验；只能迁移方法：用本项目公开需求构建 prompt-completion / synthetic augmentation / fine-tuning 或 adapter-free baseline，再用本项目 rubric 评估。不可声称复现 Volvo/Car Weaver 数据。 | `A:38-46`, `P:710-746`, `P:984-1031` |
| 资源许可与访问风险 | 工业私有数据且无公开申请渠道；Azure OpenAI fine-tuning 有 provider/model drift；专家评审不可外部复核。 | `A:30-46`, `P:1762-1805` |

## 4. 表 C：生成流程内反馈

> 专家评分、Likert、Wilcoxon、manual statechart 对比均为 post-hoc evaluation，不计为 LLM 生成流程内 feedback。普通 Mermaid 渲染/保存也不等于自动修复闭环。

| 字段 | in-loop feedback 判定 | Source pointer |
|---|---|---|
| 静态/schema | 训练数据构建阶段有 JSON prompt-completion schema 与 states/events/transitions/actions 结构化；但没有证据显示生成时用 schema validator 自动拒绝/修复输出。 | `P:747-883`, `D:166-180` |
| 编译/可执行性 | 无 in-loop compile。Mermaid.js editor 用于生成可视化 statecharts，论文未报告 render error 驱动再生成或语义执行。 | `P:1163-1166`, `D:206-209` |
| oracle/trace/等价性 | 无 in-loop oracle/trace。manual statecharts 与专家评分只用于事后比较。 | `P:1407-1515`, `P:1539-1685` |
| 仿真执行 | 无。Volvo 团队使用 statecharts 做 simulation/testing 是背景；本文生成流程没有仿真 trace feedback。 | `P:197-205`, `P:406-407`, `P:1153-1180` |
| 形式化验证 | 无。没有 model checker / theorem prover / SAT-SMT；统计检验是评测统计，不是模型形式化验证。 | `P:1138-1149`, `P:1465-1508`, `D:575-648` |
| 人类过程反馈 | 有数据层人工 QC：synthetic completion 被人工/领域专家 review；但实例级 LLM 输出的专家评审在生成后，未回灌成迭代修复。 | `P:967-982`, `P:1407-1515`, `P:1583-1642` |
| 反馈粒度 | 数据层为 JSON completion / statechart component；评估层为 test case × functional correctness / understandability / alignment；无 transition-level executable diagnostic。 | `P:840-880`, `P:1407-1424`, `P:1539-1548`, `P:1587-1613` |
| 反馈自动化程度 | W&B/Azure 指标用于 fine-tuned model selection，专家评审和 synthetic data validation 为人工；无自动 feedback-regeneration。 | `P:1046-1080`, `P:1218-1308`, `P:1407-1515` |
| 人类反馈交叉一致性 | 有 4 位专家平均评分和 Wilcoxon 检验，但未公开逐专家原始表、inter-rater agreement 或冲突处理。 | `P:1407-1419`, `P:1525-1538`, `P:1548-1568`, `A:15-17` |

## 5. 表 D：事后评测、指标与证据强度

| 评测项 | 结果 / 证据 | 证据强度 | Source pointer |
|---|---|---|---|
| 模型选择 | GPT-4 在 W&B `full_valid_mean_token_accuracy` 与 `full_valid_loss` 上略优于 GPT-3.5 Turbo / GPT-4o；ANOVA/Tukey 说明差异显著。 | 中：论文内数据清楚，训练集不公开。 | `P:1218-1308` |
| Fine-tuned vs base | 12 个测试用例、4 位专家；fine-tuned 平均 functional correctness 3.52 vs base 2.60，understandability 3.75 vs 2.96；Wilcoxon p=0.00002 / 0.00036。 | 中：指标和显著性明确，评分原表不公开。 | `P:1407-1515` |
| Fine-tuned vs manual | Manual model functional correctness mean/median 4.00/4.00，fine-tuned 2.81/3.00；p-value `9.72×10^-11`；人工状态图明显更好。 | 中：核心结论清楚，manual GT 私有。 | `P:1539-1568`, `P:1614-1685` |
| Expert qualitative issues | incomplete/unclear transitions、loop logic、generic requirement interpretation、terminology inconsistency；复杂 TC5 涉及 conditional logic/timing/overlap 时表现较弱。 | 中：访谈摘要可信，缺逐条原始材料。 | `P:1583-1642`, `P:1690-1722` |
| 附录样例 | mirror adjustments、hood/frunk、windscreen wiping 等测试描述公开片段，可用于理解任务形态，但不足以复现训练/评测。 | 弱-中。 | `P:2064-2117` |
| 证据总体 | 工业同构任务证据强，复现证据弱；适合写作反证和方法迁移，不适合实验复跑。 | 中偏弱。 | `A:13-17`, `A:38-46` |

## 6. 表 E：同样本近似与可比性决策

| 维度 | 决策 | Source pointer |
|---|---|---|
| 输入可同样本性 | 领域贴近（汽车需求），但原输入不可得；只能在本项目公开控制需求上迁移方法，不可同样本。 | `P:710-746`, `A:16`, `A:32` |
| 输出可归一性 | Mermaid statechart 可部分解析到 states/transitions/events/actions，但缺可执行语义、guard/time/concurrency；需要另写 parser/normalizer。 | `P:1163-1166`, `P:1400-1406`, `D:206-209` |
| 模型预算 | 原文为 Azure fine-tuned GPT-4 系列，复刻成本高且需要训练数据；与本项目直接 prompting / agent-loop 预算不可直接比较。 | `P:984-1031`, `A:44-46` |
| 人在回路预算 | 原文依赖 Volvo 专家、人工 statecharts、synthetic data review 和 expert ratings；本项目若比较需另行定义公开 human rubric。 | `P:967-982`, `P:1153-1180`, `P:1407-1515` |
| 反馈预算 | 无可复刻 in-loop feedback；只能作为 `fine-tuning + synthetic data + expert post-hoc` evidence。 | `P:747-883`, `P:1407-1685` |
| GT 可得性 | 不可得；论文没有公开申请入口。 | `A:16-17`, `A:30-46` |
| 最终决策 | `evidence-only`：任务同构且汽车领域重要，但因数据私有和微调资产缺失，不进入 same-sample approximate baseline。 | `A:38-46`, `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/baselines/SUMMARY.md:§6` |

## 7. 表 F：Claim 风险与 handoff

| 项目 | 结论 | Source pointer |
|---|---|---|
| 打穿的 claim | 不能声称“汽车自然语言需求到 statechart 生成尚无人做”或“首次把 LLM 用于汽车状态图生成”。 | `P:548-572`, `P:580-611`, `P:1743-1753` |
| 可保留的弱化表述 | 可说本文使用公开/可审计控制系统需求、可执行 STM schema、自动反馈/repair/run record；Automotive Statechart 使用私有 Volvo 数据、fine-tuning 和 post-hoc 专家评审。 | `A:16-17`, `A:38-46`, `P:1818-1835` |
| S1b handoff | Related Work 中作为“industrial automotive NL requirements -> statechart”的 evidence-only prior；突出其专家评审发现（复杂条件/时间/循环/术语仍弱）支持本文 problem motivation。 | `P:1583-1642`, `P:1690-1722`, `P:1762-1835` |
| S3 handoff | 不建议复刻 fine-tuning；如需 approximate，可在本项目样本上做 `GPT-4/4o + Mermaid-style direct generation` 或 `synthetic augmentation` ablation，但必须声明不是复现 Volvo thesis。 | `P:747-883`, `P:984-1031`, `A:38-46` |
| 风险等级 | I：claim 风险高；复现实验价值低。必须在 manuscript 中明确它已覆盖汽车状态图自动生成场景，但数据/工件私有导致只做 evidence-only。 | `S:124`, `S:251`, `A:42-46` |

## 8. 待补与风险

1. **数据私有**：Car Weaver 20 product functions、12 test cases、manual statecharts 和评分原始表不可访问；不得写成可复现 baseline。Source：`A:16-17`, `A:30-46`。
2. **表示口径不完全清楚**：训练数据描述为 JSON prompt-completion，最终输出又是 Mermaid.js syntax；S1b 引用时要区分 training label representation 与 final rendered statechart。Source：`P:747-883`, `P:1163-1166`。
3. **post-hoc 评审不可写成 in-loop feedback**：专家评分、Wilcoxon 和 manual comparison 都是事后评测。Source：`P:1407-1685`。
4. **复杂需求缺口可为本文动机**：TC5 等复杂条件、时序、重叠行为暴露模型短板，可支撑本文强调可执行 feedback / scenario trace。Source：`P:1631-1642`, `P:1717-1722`。
