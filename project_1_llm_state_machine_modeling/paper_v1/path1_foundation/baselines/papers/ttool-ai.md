# ttool-ai

## 0. 元信息与 source pointer

| 字段 | 内容 |
|---|---|
| 稳定引用键 | `apvrille_system_2024` |
| 论文 | *System Architects Are not Alone Anymore: Automatic System Modeling with AI* |
| 作者 / 年份 | Ludovic Apvrille, Bastien Sultan / 2024 |
| Venue | MODELSWARD 2024 |
| DOI / URL | `10.5220/0012320100003645` / <https://telecom-paris.hal.science/hal-04483279> |
| 原始目录 | `project_1_llm_state_machine_modeling/baselines/ttool-ai/` |
| 本篇定位 | mandatory closest；它已经把 ChatGPT 集成到 MBSE 工具 TTool，支持从自然语言系统规格生成 SysML block/internal/state machine diagrams，并有 JSON/constraint/TTool syntax feedback loop。Path-1 不能声称“首次工具集成”或“首次 SysML 状态机反馈生成”。 |

主要 source pointer：

> 以下未带目录前缀的 source pointer 均相对于上表“原始目录”；跨库文件使用完整相对路径。

- 元信息：`bibtex.bib:1-20`；`DESC.md:3-11`；`ASSETS.md:21-24`。
- 任务与贡献：`paper_content.txt:32-40`（摘要）、`paper_content.txt:64-78`（需要增强 context 与 feedback loop）。
- TTool 背景：`paper_content.txt:117-129`（TTool 支持 UML/SysML 与 verification/simulation 工具，但这是工具能力背景）。
- LLM / OpenAI API：`paper_content.txt:157-180`（`gpt-3.5-turbo` 示例与 `gpt-3.5-turbo-16k-0613` response）。
- 框架：`paper_content.txt:196-244`（TTool-AI 输入、knowledge、feedback、render）、`paper_content.txt:324-352`（Algorithm 1 JSON/constraint feedback）、`paper_content.txt:353-379`（user in loop）。
- 状态机生成：`paper_content.txt:641-701`（block diagram + specification -> state machine，10 iterations，errors reported to AI）。
- 实现与评测：`paper_content.txt:777-854`（knowledge size、JSON extraction、syntax loop）、`paper_content.txt:855-893`（testing environment、public repo、grading criteria）、`paper_content.txt:894-930` 与 `paper_content.txt:992-1000`（结果）。
- 资产：`ASSETS.md:13-17`、`ASSETS.md:26-46`。

## 1. 阅读审计

| 文件 | 已读范围 | 用途 | 关键注意 |
|---|---|---|---|
| `bibtex.bib` | 全文 `1-20` | 元信息、HAL/DOI、abstract、venue | BibTeX abstract 已明确 structural + behavioral SysML diagrams 与 knowledge base / feedback loop。 |
| `paper_content.txt` | 覆盖摘要、context、framework、system design、implementation/evaluation、related work、conclusion；重点行见 §0 | 抽取任务、反馈 loop、state machine 生成、模型、评测与局限 | TTool 有 model-checkers/simulators 是工具背景；论文 LLM loop 主要使用 JSON/constraint/syntax feedback，simulator 用于评分观察，不是生成内仿真反馈。 |
| `DESC.md` | 全文 `1-390` | 复核中文摘要、实验设置、结果和局限 | `DESC.md:374` 的“块图平均分85”与正文 Table 1 / 同文档前文 81 不一致，本文件按正文 Table 1 采用 81。 |
| `ASSETS.md` | 全文 `1-46` | 复核 GitHub artifact、results.ods、复现风险 | 仓库是实验工件和复现说明，不是完整 TTool 源码；复现依赖 TTool 和 OpenAI provider。 |
| `project_1_llm_state_machine_modeling/baselines/SUMMARY.md` | 对应行 `128` 与资产行 `255` | 复核五绿 direct baseline 总账 | 总账已要求把 TTool-AI 的 JSON/SysML/TTool 检查与 simulator/评分区分 in-loop vs post-hoc。 |

## 2. 表 A：方法框架与任务定位

| 输入 NL | 任务目标 | agent/prompt 模式（多选 tag+解释） | LLM 模型四元组 | 输出 STM 类型（类型+语义能力/可执行性/guard/action/hierarchy/time/concurrency/应用场景/与本项目差距） | 人在回路角色 | 输出后人工改动 |
|---|---|---|---|---|---|---|
| 自然语言 system specification；结构阶段只需规格和 question type；行为阶段还需要已生成/选定的 internal block diagram 与 block definitions，最好同时提供 system specification。Source: `paper_content.txt:196-218`, `paper_content.txt:641-651`。 | 自动从系统规格生成 SysML 结构图与行为图：blocks/internal connections/state machines，并在 TTool 中渲染。Source: `paper_content.txt:32-40`, `paper_content.txt:380-385`。 | `knowledge-injection`：system engineering、JSON format、SysML/TTool constraints；`structured-JSON`：要求 LLM 输出 JSON；`tool-feedback-loop`：JSON parse、syntax、constraints 错误拼成新问题；`user-in-loop-optional`：自动 loop 后用户可继续 refine；非 multi-agent。Source: `paper_content.txt:247-323`, `paper_content.txt:324-379`。 | ChatGPT / OpenAI / API / `gpt-3.5-turbo`；测试环境为 ChatGPT 3.5 turbo + TTool nightly Oct 2023；上下文约束 16,000 tokens，示例 response 显示 `gpt-3.5-turbo-16k-0613`。Source: `paper_content.txt:157-180`, `paper_content.txt:790-805`, `paper_content.txt:855-858`。 | 输出为 TTool/SysML block definition diagrams、internal block diagrams、state machine diagrams，并可保存为 TTool XML。状态机包含 Start/state/transition、guard、action、signal send/receive、after delay 等 TTool 表达；TTool 可解析/绘制，工具本身有 simulator/model-checker 能力。但本论文生成 loop 不是本项目的独立 `pyfcstm` schema，不提供 scenario trace/run record；state machine 依赖 block/interface 上下文，层次/时间/concurrency 能力以 TTool/SysML 支持为主而非论文评测核心。Source: `paper_content.txt:117-125`, `paper_content.txt:641-701`, `paper_content.txt:716-776`, `ASSETS.md:16`。 | 通用框架中用户在自动 loop 成功或达到上限后介入，处理不可数学表达的质量约束、补知识、手工修正或改规格；评测中人类交互被禁用，学生只作为对照组，评分由相同 criteria 完成。Source: `paper_content.txt:237-244`, `paper_content.txt:353-379`, `paper_content.txt:921-930`。 | Running example 明确未改动 AI 生成的 states/transitions、未加入用户反馈，但 10 次迭代后仍有 useless guard 和错误信号参数，可手工处理。评测公开 XML/ODS，应视为生成 artifact；不应假设作者人工修好后才计分。Source: `paper_content.txt:686-693`, `ASSETS.md:15-17`。 |

## 3. 表 B：资产状态与可复现性

| 稳定引用键 | 论文与版本 | Reference/GT | 数据与 artifact | 已有本地复现资产 | 可复现路径 | 资源许可与访问风险 |
|---|---|---|---|---|---|---|
| `apvrille_system_2024`。Source: `bibtex.bib:1`。 | MODELSWARD 2024 / HAL 作者版 / DOI `10.5220/0012320100003645`；本地 PDF 与文本已提取。Source: `bibtex.bib:2-19`, `ASSETS.md:13`。 | 没有传统 GT statechart 文件；评测基于三类欧洲项目规格、TTool-AI 输出、学生输出和质量评分 criteria；`results.ods` 记录时间、100 分制 grading 与 overview。Source: `paper_content.txt:855-893`, `ASSETS.md:15-17`。 | GitHub `zebradile/ttool-ai` 公开 platooning、spacebasedsystem、AutomatedBraking 等目录，含 `.desc` 规格、`.xml` 模型和 `results.ods`；另有 DPS、SNCS、attacktrees、incoherencies 等补充工件。Source: `paper_content.txt:855-870`, `ASSETS.md:13-17`, `ASSETS.md:28-36`。 | 本地只有论文目录文件；尚未冻结完整 GitHub repo 或 ODS 内容到本目录。`ASSETS.md` 记录 HEAD `f2c52282cb7a826c31e7ab512356d42230c6d321`、ODS size/ETag。Source: `ASSETS.md:14-17`, `ASSETS.md:26-36`。 | 近似复现路径：固定 GitHub HEAD，安装 TTool nightly/兼容版本，配置 OpenAI key/model，打开/重跑 README 指令；将生成 XML 转成 normalized STM；但 provider drift 和 TTool 版本会影响结果。Source: `ASSETS.md:36-46`, `paper_content.txt:855-870`。 | GitHub 仓库是实验工件而非完整 TTool-AI 源码；结果受 ChatGPT 随机性、OpenAI 模型版本、TTool nightly 变化影响；license 与长期可访问性需正式实验前冻结。Source: `ASSETS.md:26-46`。 |

## 4. 表 C：生成流程内反馈

> 本表只统计影响 LLM 生成/再生成的反馈。TTool simulator 用于评估“行为是否符合规格”，以及 TTool 具备 model-checker/simulator 能力，不自动等于生成 loop 中使用了 simulation/model checking feedback。

| 静态/schema | 编译/可执行性 | oracle/trace/等价性 | 仿真执行 | 形式化验证 | 人类过程反馈 | 反馈粒度 | 反馈自动化程度 | 人类反馈交叉一致性 |
|---|---|---|---|---|---|---|---|---|
| 强。自动 loop 检查 expected output format（JSON）和 knowledge 中的 constraints；JSON extraction 失败、syntax errors 和 constraint violations 会被加入下一轮 feedback question。Source: `paper_content.txt:324-352`, `paper_content.txt:824-850`。 | 中。TTool-AI 从 JSON 构造 SysML 模型，若构造/语法检测有错误则反馈；这相当于 TTool parse/syntax 可接受性，不是执行语义等价。Source: `paper_content.txt:830-854`。 | 无 trace/oracle feedback。没有 distinguishing trace、oracle equivalence 或 reference statechart 自动比较进入 prompt。Source: `paper_content.txt:324-352`, `paper_content.txt:855-893`。 | 评测中使用 TTool simulator 观察 state machine behavior 是否符合 specification，但 source 将其列为 grading criteria；未见 simulator trace 被送回 GPT 作为自动修复信号。Source: `paper_content.txt:879-884`。 | 工具背景有 model-checkers/simulators/ProVerif，但本文 LLM feedback loop 证据是 JSON/constraints/syntax；不得写成完整 formal verification in-loop。Source: `paper_content.txt:117-125`, `paper_content.txt:324-352`。 | 通用流程允许用户在自动 loop 后继续 query、补 knowledge、手工修正或改 specification；评测中 human interaction disabled。Source: `paper_content.txt:353-379`, `paper_content.txt:921-930`。 | parser/syntax/constraint error 级；示例 screenshot 说 feedback loop reports 4 errors to AI；不是 counterexample 或 scenario trace。Source: `paper_content.txt:694-701`。 | 中高：JSON/syntax/constraint feedback 自动化明确；但 informal quality、人类期望命名、复杂语义仍靠用户/评分。Source: `paper_content.txt:353-379`, `paper_content.txt:879-893`。 | 未报告评分者一致性或 inter-rater；只说明 TTool-AI 和学生使用相同 grading criteria。Source: `paper_content.txt:871-893`。 |

## 5. 表 D：事后评测、指标与证据强度

| 评测项 | 指标 / 结果 | 证据强度 | 对 Path-1 的使用方式 | source pointer |
|---|---|---|---|---|
| 时间与得分 | TTool-AI：BD 40s / 81，SMD 178s / 63；学生：BD 2700s / 70，SMD 2700s / 58。 | 中强：表格公开，repo 有 `results.ods`；但评分主观。 | 说明已有工作在 SysML block+state machine 生成上已与学生对比，Path-1 不应过度声称“首次自动建模超越人工”。 | `paper_content.txt:992-1000`, `ASSETS.md:15` |
| 一致性 | TTool-AI 标准差 BD 16、SMD 15；学生 BD 26、SMD 32。 | 中 | 可用于说明 tool-integrated LLM baseline 稳定性，但需承认模型/provider drift。 | `paper_content.txt:992-1000`, `paper_content.txt:894-905` |
| 复杂度分析 | TTool-AI 对 platooning、space-based 表现好；AutomatedBraking 规格更长、更复杂、更模糊时，学生在 state machines 上略优。 | 中 | 可作为控制系统复杂需求下 LLM baseline 仍脆弱的 evidence。 | `paper_content.txt:906-913` |
| 评分 criteria | 包括 diagrams adequacy to specification、simulator-observed behavior、exchange count、readability、naming consistency、unused attributes、TTool syntax errors/warnings。 | 中 | 用于 S1b 描述其 post-hoc evaluation，而非 in-loop feedback。 | `paper_content.txt:879-893` |
| 资产证据 | GitHub repo + results.ods + XML models；README 复现说明。 | 强于大多数 baseline | 可进入 S3 possible tool comparison，但需冻结 HEAD/ODS 并处理 TTool/OpenAI drift。 | `paper_content.txt:855-870`, `ASSETS.md:13-17` |
| 方法局限 | AI context/knowledge capacity，overloading causes quality degradation；复杂系统仍挑战。 | 强 | 可作为本项目强调 run-record、分阶段、可执行反馈和 scope control 的动机。 | `paper_content.txt:1047-1065` |

## 6. 表 E：同样本近似与可比性决策

| 维度 | 决策 | 理由与 source pointer |
|---|---|---|
| 输入可同样本性 | 中。 | 原始规格公开且是自然语言，但 state machine 阶段还依赖 block/internal diagram context，和本项目单独 `NL -> STM` 输入不完全一致。Source: `paper_content.txt:641-651`, `ASSETS.md:16`。 |
| 输出可归一性 | 中。 | TTool XML/SysML state machines 可转为 normalized STM，但需处理 block signals、guards、actions、after delays 和 TTool 语义。Source: `paper_content.txt:641-701`, `paper_content.txt:716-776`。 |
| 模型预算 | 中。 | 使用 OpenAI GPT-3.5 turbo，provider drift 明显；上下文 16k 与知识实例 200-word 限制会影响复现。Source: `paper_content.txt:790-805`, `ASSETS.md:42-46`。 |
| 人在回路预算 | 低到中。 | 评测禁用 human interaction；但真实工具允许用户补知识/手工修正，若复现实验需明确是否禁用。Source: `paper_content.txt:353-379`, `paper_content.txt:921-930`。 |
| 反馈预算 | 中。 | JSON/syntax/constraint feedback 可近似；simulation/model-checking feedback 不应加入，除非明确作为本项目扩展而非复现。Source: `paper_content.txt:324-352`, `paper_content.txt:879-884`。 |
| GT 可得性 | 中。 | 有 public XML/ODS 与评分结果，但没有严格 GT statechart；学生模型/评分细则可能不完整。Source: `paper_content.txt:855-870`, `ASSETS.md:15-17`。 |
| 最终可比性决策 | **near / possible tool comparison**。 | 适合小规模 tool-assisted baseline 或 Related Work 反证；不建议作为主 same-sample exact baseline，除非先冻结 TTool repo、XML、ODS 并实现 XML-to-STM adapter。 |

## 7. 表 F：Claim 风险与 handoff

| 类型 | 内容 | 风险等级 | handoff |
|---|---|---|---|
| 会被打穿的 claim | “首次将 LLM 集成到 MBSE/SysML 工具生成状态机”；“首次使用自动反馈 loop 修复 SysML 生成”；“没有工具级 artifact baseline”。 | C/I | S1b 必须把 TTool-AI 列为 mandatory closest。 |
| 需要弱化的 claim | 可写“已有 TTool-AI 将 ChatGPT 接入 MBSE 工具并用 JSON/constraint feedback 生成 SysML state machines；本文差异在控制需求专用 schema、run record、scenario trace / executable feedback、可审计修复策略（以实际实验为准）”。 | C/I | 作为 Related Work 对比段核心之一。 |
| 不能误写的点 | TTool 背景的 model-checkers/simulators 不等于论文生成 loop 已用 model checking；simulator 是 post-hoc grading criterion；JSON/TTool syntax feedback 不等于 formal verification。 | C | S1b/S3 表格都必须保留 in-loop/post-hoc 区分。 |
| S1b handoff | mandatory closest；可与 `llms_emp` 组成“SysML/MBSE feedback baselines”小节。 | C/I | 关联 `project_1_llm_state_machine_modeling/baselines/SUMMARY.md:128`。 |
| S3 handoff | 若做 approximate，先冻结 GitHub HEAD `f2c52282...`、`results.ods` ETag、TTool version；实现 XML/TTool state machine adapter；明确是否禁用 human interaction。 | C/I | 关联 `ASSETS.md:14-17`, `ASSETS.md:42-46`。 |

## 8. 待补与风险

1. **冻结 artifact**：当前 `ASSETS.md` 记录 GitHub HEAD 和 ODS ETag，但本目录没有完整 repo snapshot；正式 S3 前需下载或 submodule/archive 固定。
2. **复核模型配置**：论文使用 `gpt-3.5-turbo` / `gpt-3.5-turbo-16k-0613` 口径；OpenAI 当前模型已漂移，复现需记录替代模型和影响。
3. **区分工具能力与论文用法**：TTool 支持 verification/simulation，但本文的 LLM feedback loop 主要是 JSON/syntax/constraints；不要把 TTool 全能力当成 baseline 已用 formal verification。
4. **评分主观性**：质量评分与学生对比有价值，但缺少 inter-rater / rubric 细节；只能作为 medium-strong evidence，不是可自动复算指标。
5. **DESC 内部小错**：`DESC.md:374` 写块图平均分 85，正文 Table 1 和同文件前文为 81；本文件采用正文 Table 1 的 81。
