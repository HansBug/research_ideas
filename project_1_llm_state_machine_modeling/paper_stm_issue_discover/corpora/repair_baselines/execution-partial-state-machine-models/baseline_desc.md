# Execution of Partial State Machine Models — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `execution-partial-state-machine-models` |
| 标题 | Execution of Partial State Machine Models |
| 年份 / venue | 2022 / IEEE Transactions on Software Engineering；arXiv 2021 |
| 当前角色 | partial STM refinement / execution 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无自然语言需求；输入是 partial UML-RT model / HSM、component completeness setting、交互或 batch execution rules |
| 模型 / STM 输出 | refined partial UML-RT HSM，可通过 decision points、debugging agent、脚本或交互输入继续执行 |
| 修正 / 补全 / refinement 方法 | 三阶段框架：static analysis 检测 execution-blocking partial elements；automatic refinement 通过 M2M transformation 加入 decision points、debugging interface、额外 states/transitions/guards/actions；input-driven execution 由用户或脚本补充缺失选择 |
| feedback 来源 | execution semantics 驱动的 static-analysis diagnostics、stuck configuration / reachability / progress 问题、interactive / batch execution input |
| 自动化程度 | 静态分析、模型转换、代码生成和 build 可自动执行；缺失语义的选择仍依赖用户交互或脚本规则 |
| LLM / agent 角色 | 无 LLM / agent loop |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

这是 `STM_0 -> executable / refined STM` 的强近邻：它不含 NL，也不做 LLM 修复，但直接处理 partial state machine，并把不可执行 / 不完整状态机转成可执行、可调试、可由输入规则继续推进的 refined HSM。它适合支撑本文的一个关键边界：已有 MDE 工作已经能对 partial STM 做语义保持的 refinement / execution support，但并未解决 `<NL, STM_0>` 语义诊断、需求一致性与无人化 LLM repair loop。

## 4. 证据位置

- `paper_content.txt:5-19`：摘要明确 partial models execution、static analysis、automatic refinement、input-driven execution、PMExec 与 UML-RT。
- `paper_content.txt:59-73`：举例说明 state machine 可能缺少 component behavior、transition trigger/guard/action，目标是 best-effort execution。
- `paper_content.txt:167-205`：三阶段框架、行为保持、公开实现与 open-source toolchain。
- `paper_content.txt:663-701`：static analysis 与 automatic refinement 的通用定义，包含 lack of progress / reachability、missing elements、problematic specifications、unhandled inputs。
- `paper_content.txt:851-1014`：UML-RT HSM refinement algorithm，自动加入 decision point、states、transitions、guards、entry/exit points 等。
- `paper_content.txt:1035-1175`：refined partial model 的 interactive / batch execution 与 execution-rule 语义。
- `paper_content.txt:1562-1589`：PMExec 工具、Bitbucket repository、Papyrus-RT 插件与自动 static analysis / transformation / code generation / build。
- `paper_content.txt:1648-1695`：batch execution、保存用户决策为 execution rules / design model，以及 validation 组成。
- `paper_content.txt:2748-2766`：结论再次说明 problematic elements 被自动 fixed by adding decision points，并声明 PMExec publicly available。

## 5. 主要风险与使用边界

- 无 NL 输入，也没有 `NL -> STM_0` 关系，不能作为 `<NL, STM_0> -> STM_k` baseline；更适合作为 `STM_0 -> executable/refined STM` 的 repair-engine / execution-semantics 近邻。
- refinement 的目标是使 partial model 可执行 / 可调试，不是基于需求语义或形式化性质自动修复模型错误。
- 缺失信息仍由用户交互或 batch script 补充；不属于无人化 repair loop。
- 目标语言是 UML-RT / Papyrus-RT HSM，迁移到本文目标 STM DSL 需要转换和语义裁剪。
- PMExec 仓库虽在论文中声明公开，但后续仍需核验仓库当前可访问性、license、commit 与可复跑环境。
