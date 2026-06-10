# Umple / Llama3 生成 Umple 状态机代码

## 0. 元信息与 source pointer

| 项目 | 内容 | Source pointer |
|---|---|---|
| 稳定引用键 | `pathak_exploring_2025` | `project_1_llm_state_machine_modeling/baselines/umple/bibtex.bib:2-13` |
| 论文 | Parva Pathak, *Exploring How Well Llama3 can Generate State Machines Represented in Umple*, Master's Thesis, University of Ottawa, 2025 | `.../bibtex.bib:2-13`; `.../DESC.md:5-13` |
| 本地原始目录 | `project_1_llm_state_machine_modeling/baselines/umple/` | 本任务指定路径；`.../ASSETS.md:13-18` |
| 主要 source pointer 简写 | `P=`同目录 `paper_content.txt`；`D=`同目录 `DESC.md`；`A=`同目录 `ASSETS.md`；`R=`同目录 `reproduction-2026-04-15-local-toolchain/` | 本文下方表格使用这些简写，但均指向上述原始目录 |
| 关键证据线索 | 研究问题/模型：`P:226-252`, `P:790-805`; 指标：`P:805-894`; 样例与 prompt/RAG：`P:895-1138`; zero/one-shot/RAG 结果：`P:1145-1243`, `P:1251-1457`, `P:1464-1780`; 结论/威胁：`P:1787-1876`; 资产：`A:13-18`, `A:31-47`; 本地 reproduction：`R/verification/reproduce.sh:78-110`, `R/logs/07_python_demo_run.log:1-9`, `R/logs/08_nusmv_verified_run.log:17-24`, `R/logs/13_garage_python_demo_run.log:1-8`, `R/logs/15_garage_nusmv_direct_properties.log:17-62` | 逐项结论见各表 Source pointer 列 |

## 1. 阅读审计

| 材料 | 已读范围 | 结论 | Source pointer |
|---|---|---|---|
| `bibtex.bib` | 全文 13 行 | 确认 2025 Ottawa 硕士论文、作者、RUOR URL 与引用键。 | `.../bibtex.bib:2-13` |
| `paper_content.txt` | 覆盖摘要、引言、背景、研究方法、5 个状态机样例、zero-shot / one-shot / RAG 三组实验、结论与威胁 | 原文支持“NL requirements -> Umple state-machine code”的 direct/near baseline；compile/pass@k/CodeBLEU 等均是评测，不是生成流程内反馈。 | `P:183-252`, `P:790-1138`, `P:1145-1780`, `P:1787-1876` |
| `DESC.md` | 全文阅读 | 既有派生文件已整理三种提示策略、指标体系、5 个样例、RAG 与 one-shot 结果，以及与 Project 1 的差异。 | `D:15-80`, `D:120-260`, `D:260-387`, `D:598-759` |
| `ASSETS.md` | 全文阅读 | 论文公开；无 thesis 实验脚本、RAG 文档库、prompt 输出或完整 benchmark bundle；Umple 工具链公开不等于论文 artifact 公开。 | `A:13-18`, `A:27-47` |
| `reproduction-2026-04-15-local-toolchain/` | 审计目录树、模型、verification 脚本与 logs；未启动任何子任务，只读 | 该目录是本地 Umple toolchain / NuSMV / Alloy smoke 资产，覆盖 Driver License 与 Garage Door 示例的 parse/generate/demo/model-check；不是论文 Llama3/RAG 输出复现，范围应标为 local-toolchain reproduction，非 thesis benchmark reproduction。 | `R/.gitignore:1-3`, `R/.java-version:1`, `R/models/driver_license_system.ump:1-98`, `R/models/garage_door_direct.ump:1-31`, `R/verification/reproduce.sh:78-110`, `R/logs/00_java_version.log:1-3` |
| `SUMMARY.md` 对应行 | 核对 direct baseline 与数据集总账行 | 总账记录 Umple 工具公开、thesis benchmark bundle 未公开；S1a 总账初判为 near / possible approximate。 | `project_1_llm_state_machine_modeling/baselines/SUMMARY.md:125`, `project_1_llm_state_machine_modeling/baselines/SUMMARY.md:252` |

## 2. 表 A：方法框架与任务定位

| 字段 | 本篇结论 | Source pointer |
|---|---|---|
| 输入 NL | 5 个系统的自然语言描述与需求列表：Blackjack、Course Section、Credit Card Transaction、Driver License、Hotel Stay；RAG / one-shot 会把其他示例的需求+代码作为上下文。 | `P:895-1030`, `P:1036-1097`, `P:1102-1138`, `D:19-21` |
| 任务目标 | 评估 Llama 3 能否从 requirements 生成 Umple state machine modeling code，并比较 zero-shot、one-shot、RAG 三种策略对可用性和修正工作量的影响。 | `P:226-252`, `P:790-805`, `P:1787-1806` |
| agent/prompt 模式（多选 tag+解释） | `zero-shot`：只给目标系统需求；`one-shot`：给一个示例对话+目标需求；`RAG`：用 Nomic embeddings + cosine similarity 选择 1-4 个示例追加到 system message；`structured system prompt`：要求只输出 Umple code、不解释；不是 agent loop，也没有自动 repair loop。 | `P:1032-1097`, `P:1098-1138`, `D:179-243` |
| LLM 模型四元组 | 模型：Llama 3 / Llama 3.1 8B（文中口径混用 Llama 3 与 conclusion 的 Llama 3.1）；provider：Meta open-weight/local model；调用方式：本地运行，按 Llama prompt format；版本锁：未给具体 checkpoint hash、runtime、sampling 参数或 hardware 完整锁定，且作者承认 8B 是最小版本、70B/405B 可能更好。 | `P:236-252`, `P:427-466`, `P:1036-1097`, `P:1838-1861` |
| 输出 STM 类型 | Umple state machine code。语义能力：文本 DSL，可生成 Java/Python/NuSMV/Alloy 等工具输出；支持 states/transitions、guards、actions、nested state machines（Driver License 示例涉及 nested state machine 讨论）；可执行性：Umple compiler 可编译，local reproduction 证明可生成 Python / NuSMV / Alloy；time/concurrency：论文样例未覆盖时间自动机或并发；应用场景：短需求到建模代码草稿；与本项目差距：无控制系统专属变量/时间约束/安全性质/trace feedback/run record。 | `P:300-330`, `P:805-814`, `P:982-1005`, `P:1132-1138`, `R/models/driver_license_system.ump:30-78`, `R/logs/02_generate_python.log:1-3`, `R/logs/03_generate_nusmv.log:1-3`, `R/logs/04_generate_alloy.log:1-3` |
| 人在回路角色 | 论文中 reference state machines / corrected versions 由作者构造，Levenshtein 距离衡量用户修正工作量；没有流程内专家反馈或多人 adjudication。Local reproduction 是后续本地工程审计，不是论文作者的人在回路。 | `P:820-843`, `P:1830-1837`, `D:280-294` |
| 输出后人工改动 | 事后评测要求把生成代码改成 corrected reference state machine 并计算 normalized Levenshtein distance；这是评价“修正努力”，不是生成流程中的自动修复反馈。 | `P:820-843`, `P:858-869`, `P:1821-1829` |

## 3. 表 B：资产状态与可复现性

| 字段 | 本篇结论 | Source pointer |
|---|---|---|
| 稳定引用键 | `pathak_exploring_2025` | `.../bibtex.bib:2-13` |
| 论文与版本 | University of Ottawa Master's Thesis, 2025；RUOR item / DOI 公开；非 CCF venue。 | `.../bibtex.bib:2-13`, `A:20-25` |
| Reference / GT | 论文使用 5 个系统的 reference / corrected state machines；完整 benchmark bundle、RAG 文档库、生成输出与逐样本结果未公开。 | `P:895-1030`, `P:820-843`, `A:16-18`, `A:31-37` |
| 数据与 artifact | Umple 官方示例/工具公开；论文专属实验代码、RAG 文档库、prompt 运行输出、结果表未公开。 | `A:13-18`, `A:27-37` |
| 已有本地复现资产 | 有 `reproduction-2026-04-15-local-toolchain/`：包含 Driver License requirements/model、Garage Door direct model、Umple 生成的 Python/NuSMV/Alloy、NuSMV/Alloy/Python demo scripts 与 logs。注意 `.gitignore` 排除 `tooling/`、`txl/`、`__pycache__`，目录中部分二进制/工具链可能只是本地存在，不应当作论文 artifact。 | `R/.gitignore:1-3`, `R/models/driver_license_requirements.ump:1-49`, `R/models/driver_license_system.ump:1-98`, `R/models/garage_door_direct.ump:1-31`, `R/verification/reproduce.sh:78-110` |
| 本地 reproduction 审计结论 | Local smoke 成功：Driver License 解析、Python/NuSMV/Alloy 生成成功；Python demo 走到 `python_demo_ok`；NuSMV verification-ready 模型验证多条 CTL，并给出故意失败性质的 counterexample；Garage Door Python demo 成功，NuSMV 证明 HalfOpen 可达且给出若干 CTL/LTL counterexamples。范围不包括 Llama3 调用、RAG 检索、论文生成输出或 ICP/EUCP/pass@k 复算。 | `R/logs/01_parse_driver_license.log:1-3`, `R/logs/07_python_demo_run.log:1-9`, `R/logs/08_nusmv_verified_run.log:17-24`, `R/logs/13_garage_python_demo_run.log:1-8`, `R/logs/14_garage_nusmv_raw_run.log:17-21`, `R/logs/15_garage_nusmv_direct_properties.log:17-62` |
| 可复现路径 | 论文级复现不可直接做；可做 near/approximate：用公开 Umple 示例重建需求和 reference，运行本地 Llama/Qwen/GPT 生成 Umple code，再用本地 Umple compiler + parser + normalized structural metrics 评估。 | `A:31-47`, `P:1036-1138`, `R/verification/reproduce.sh:78-110` |
| 资源许可与访问风险 | Umple 官方示例/工具是活资源，需冻结版本；Course Section 可能存在训练数据污染；论文没有结果包；本地 toolchain 与 thesis benchmark 范围不一致。 | `A:43-47`, `P:1851-1856`, `R/models/driver_license_system.smv:1-5` |

## 4. 表 C：生成流程内反馈

> Umple compiler、ICP/EUCP、Pass@K、CodeBLEU、normalized Levenshtein 在论文里均用于最终评测；普通 compile/pass@k 不算 in-loop feedback。Local reproduction 的 NuSMV/Alloy 是本地补充审计，不是论文生成 loop。

| 字段 | in-loop feedback 判定 | Source pointer |
|---|---|---|
| 静态/schema | 无 in-loop；prompt 有固定格式，生成后用 Umple compiler 评估 syntax/extra code，但未反馈给 Llama 再生成。 | `P:1036-1097`, `P:1132-1138`, `P:1145-1243` |
| 编译/可执行性 | 论文中 compile/ICP/EUCP 是 post-hoc metric；local reproduction 证明 Umple toolchain 可 parse/generate/run，但不属于论文 LLM generation loop。 | `P:876-883`, `P:1132-1138`, `R/logs/01_parse_driver_license.log:1-3`, `R/logs/07_python_demo_run.log:1-9` |
| oracle/trace/等价性 | 无 in-loop oracle/trace。Corrected reference + normalized Levenshtein 是事后修正工作量评估。 | `P:820-843`, `P:858-869`, `P:1787-1810` |
| 仿真执行 | 原论文无仿真执行反馈；本地 Python demos 是后续 local smoke。 | `P:805-814`, `R/logs/07_python_demo_run.log:1-9`, `R/logs/13_garage_python_demo_run.log:1-8` |
| 形式化验证 | 原论文无 formal verification；本地 reproduction 加了 NuSMV CTL/LTL 和 Alloy smoke，但这是本仓库后续资产，不能归因给 thesis 方法。 | `P:805-814`, `R/verification/driver_license_verified.smv:1-8`, `R/logs/08_nusmv_verified_run.log:17-24`, `R/logs/15_garage_nusmv_direct_properties.log:17-62` |
| 人类过程反馈 | 无流程内人类反馈；reference/corrected state machine 由作者构造，威胁有效性承认最好多人平均，但实际未做到。 | `P:1830-1837` |
| 反馈粒度 | 评测粒度为 code line / extra code line / character edit distance / pass threshold / CodeBLEU；不是 state/transition semantic diagnostic，也没有 FixLog。 | `P:858-894`, `P:1255-1288`, `P:1575-1606` |
| 反馈自动化程度 | 评测脚本可自动化，但生成策略没有自动使用评测结果修复；local reproduction 脚本自动跑工具链。 | `P:1090-1138`, `R/verification/reproduce.sh:78-110` |
| 人类反馈交叉一致性 | 无。作者在 threats 中承认 reference/corrected versions 不是多人平均。 | `P:1830-1837` |

## 5. 表 D：事后评测、指标与证据强度

| 评测项 | 结果 / 证据 | 证据强度 | Source pointer |
|---|---|---|---|
| Zero-shot | 20 次生成没有 passable state machines；Error/NSF 占主；生成代码多为 Java 嵌入 Umple，基本无用。 | 中：论文结果清楚，输出包未公开。 | `P:1145-1243` |
| One-shot syntax/effort | ICP/EUCP 大幅改善；normalized Levenshtein：Credit Card 0.13、Hotel 0.17、Course 0.18、Driver License 0.29、Blackjack 0.46；4/5 系统低于 0.30。 | 中。 | `P:1251-1327`, `P:1793-1799` |
| One-shot pass@k / CodeBLEU | pass@k 随阈值与 k 提升；CodeBLEU/BLEU 与编辑距离排序不一致。 | 中偏弱：CodeBLEU 对 Umple 不适配。 | `P:1340-1457`, `P:870-875` |
| RAG syntax/effort | RAG 平均 ICP/EUCP 很低；normalized Levenshtein：Hotel 0.07、Credit Card 0.25、Course 0.31、Blackjack 0.31、Driver License 0.32；平均 one-shot 0.246 vs RAG 0.244，RAG 方差更低但非单调改善。 | 中。 | `P:1571-1659`, `P:1800-1814` |
| RAG pass@k / semantic | RAG pass@1/5/10 表明不同用户阈值下结论不同；BLEU 与 normalized Levenshtein 无相关。 | 中偏弱。 | `P:1660-1780`, `P:1758-1765` |
| Threats | Llama 3/3.1 8B 是最小模型；Course Section code 可能被模型看过；requirements 未公开来源；CodeBLEU 缺 Umple 支持；样例简单。 | 中。 | `P:1830-1876` |
| Local reproduction 证据 | 强证明本地 Umple compiler/Python/NuSMV toolchain 可用于后续 approximate baseline；弱/无证明 thesis Llama3 结果。 | 对 toolchain 强，对论文复现弱。 | `R/logs/01_parse_driver_license.log:1-3`, `R/logs/07_python_demo_run.log:1-9`, `R/logs/08_nusmv_verified_run.log:17-24`, `R/logs/15_garage_nusmv_direct_properties.log:17-62` |

## 6. 表 E：同样本近似与可比性决策

| 维度 | 决策 | Source pointer |
|---|---|---|
| 输入可同样本性 | 可尝试 approximate：论文任务是短 NL requirements；但 thesis 的完整 5-system benchmark bundle/RAG docs 未公开，需要用公开 Umple examples 或本项目样本重建。 | `A:16-18`, `A:31-37`, `P:895-1030` |
| 输出可归一性 | 较好：Umple textual state machine 可 parse/compile，且可导出 Python/NuSMV/Alloy；但与 pyfcstm schema 的 guard/action/time/hierarchy 语义需写映射器。 | `P:1132-1138`, `R/models/driver_license_system.ump:30-78`, `R/models/driver_license_system.smv:1-5`, `R/logs/03_generate_nusmv.log:1-3` |
| 模型预算 | Llama 3/3.1 8B 本地模型可替代性较好；但原 checkpoint/sampling 未锁，直接复刻仍不严谨。 | `P:236-252`, `P:1838-1861` |
| 人在回路预算 | 原文 evaluation 需要作者修正 generated output 成 corrected reference；如果做 approximate，应改为 deterministic parser/semantic checker + limited human adjudication，避免不可控人工工作量。 | `P:820-843`, `P:1830-1837` |
| 反馈预算 | 可以将 Umple compiler/parser 作为本项目 baseline 的 post-hoc validity check；若要做 in-loop baseline，需显式新增 repair loop，不能声称是原论文方法。 | `P:1132-1138`, `R/verification/reproduce.sh:78-110` |
| GT 可得性 | 原 benchmark 不完整公开；但官方 Umple examples + 本地 reproduction 可形成近似 reference。 | `A:16-18`, `A:31-37`, `R/models/driver_license_requirements.ump:1-49` |
| 最终决策 | `near / possible approximate`：适合做一个 `NL -> Umple -> normalized STM` baseline 或 RAG/few-shot baseline；不适合作为严格复现论文结果。 | `A:39-47`, `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/baselines/SUMMARY.md:§6` |

## 7. 表 F：Claim 风险与 handoff

| 项目 | 结论 | Source pointer |
|---|---|---|
| 打穿的 claim | 不能声称“few-shot / RAG 生成状态机代码无人做过”或“LLM 生成 state-machine DSL 是本文首创”。 | `P:226-252`, `P:1036-1138`, `P:1821-1829` |
| 可保留的弱化表述 | 可强调本文面向控制系统、可执行 pyfcstm/diagnostics、scenario trace 和 repair/run-record；Umple thesis 主要是短样例、prompt/RAG 评测和 post-hoc compile/edit-distance。 | `P:805-894`, `P:1787-1876`, `R/verification/driver_license_verified.smv:1-8` |
| S1b handoff | Related Work 中作为 `NL requirements -> modeling language state machine code` 的 direct/near prior；引用其 zero-shot failure、RAG/one-shot 接近、BLEU 不可靠、8B/小样本威胁。 | `P:1145-1243`, `P:1758-1765`, `P:1807-1814`, `P:1830-1876` |
| S3 handoff | 可进入 possible approximate baseline：复用本地 Umple toolchain，定义输入样本、prompt variants、Umple compile validity、pyfcstm/Umple AST normalize、manual adjudication 上限；local reproduction 只能作为 toolchain readiness，不是 thesis replication。 | `R/verification/reproduce.sh:78-110`, `R/logs/07_python_demo_run.log:1-9`, `R/logs/08_nusmv_verified_run.log:17-24`, `R/logs/15_garage_nusmv_direct_properties.log:17-62` |
| 风险等级 | M/I：claim 风险中高；实验可作为 approximate 候选，但必须明确 benchmark bundle 不公开、local reproduction 范围有限。 | `A:43-47`, `P:1830-1876` |

## 8. 待补与风险

1. **reproduction 范围不明/有限**：当前 `reproduction-2026-04-15-local-toolchain` 是本地工具链与手写/改写示例 smoke，不覆盖 Llama3 原始 outputs、RAG doc DB、pass@k 复算。Source：`R/verification/reproduce.sh:78-110`, `A:31-47`。
2. **论文模型口径混用**：标题/正文多写 Llama 3，结论威胁处写 Llama 3.1 8B；S1b 应按“Llama 3/3.1 8B，精确 checkpoint 未锁”表述。Source：`P:236-252`, `P:1838-1861`。
3. **CodeBLEU 不适配 Umple**：原文自己承认除 BLEU 外的 CodeBLEU 子指标因用 Java 替代而不准确；本项目不要把 CodeBLEU 当主证据。Source：`P:870-875`, `P:1758-1765`, `P:1862-1866`。
4. **数据污染与小样本**：Course Section 来自 UmpleOnline，模型可能见过代码；5 个样例偏简单。Source：`P:954-957`, `P:1851-1856`, `P:1871-1876`。
5. **同样本 approximate 要重新定义成功标准**：若使用 Umple compile/pass@k，只能作为 validity/evaluation；若要和本文 in-loop feedback 对比，需要额外实现 repair loop 并清楚标注不是原论文方法。Source：`P:1132-1138`, `P:1787-1814`。
