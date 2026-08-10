> **Cold archive / deprecated historical snapshot.** 本文件已经脱离当前 R5.5+ 主线，只用于追溯 R1.5--R1.7 旧 seed_corpus 的历史证据链；不得作为当前 seed、baseline、eligibility 或主实验事实源。当前事实请回到 `paper_stm_repair/corpora/`、`paper_stm_repair/reports/` 与 `paper_stm_repair/pipeline/` 的对应入口。

## 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/baseline_seed_method_crosswalk.md` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-baseline-seed-method-crosswalk.md` |
| 时间前缀 / 内容冻结依据 | `d3758f2bd5a780274ff1a249b40c7184a4230242` — 2026-06-14 11:18:35 +0800 — fix(paper1-r1.7): 补齐旧baseline seed方法入账 |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| 当前事实源替代入口 | [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)、[../../../corpora/repair_baselines/SUMMARY.md](../../../corpora/repair_baselines/SUMMARY.md)、[../../../corpora/nl_datasets/SUMMARY.md](../../../corpora/nl_datasets/SUMMARY.md)、[../../../reports/SUMMARY.md](../../../reports/SUMMARY.md) |

# 旧九个 direct baseline 到 seed 方法集合的 crosswalk

本文件用于修正一个容易混淆的口径：在当前第一篇论文的 `<NL, STM_0> -> STM_k / Better STM` 任务中，**seed 不是要被击败的 baseline，也不是只包含可立即进入四例的样本**。seed 文库首先记录的是上游 `NL -> STM_0` 的方法 / 论文 / artifact 来源集合；主实验四例只是从该集合中按资产可获取性、领域贴合度、可冻结程度和泄漏风险再抽样。

因此，旧九个 direct baseline 都应在本 seed 文库中有明确位置。它们是否进入 PR-R2 主四例，是第二层问题；不能因为 artifact 弱、protocol domain、private data 或 paper-only 就从 seed 方法集合中消失。

## 字段口径

| 字段 | 含义 |
|---|---|
| `seed 方法 ID` | 当前 `seed_corpus` 使用的稳定 ID；若与原 baseline slug 不同，保留映射。 |
| `输入 NL` | 上游方法接收的自然语言 / 文本规格 / 系统描述是什么。 |
| `输出 STM` | 生成或抽取出的状态机族工件是什么。 |
| `方法 / LLM` | 生成方式、模型、prompt / pipeline、是否 agent / feedback。 |
| `原装 <NL, STM> 可获取性` | 是否能取得作者直接提供的输入与输出 pair，而不是本项目复跑后才生成。 |
| `源码 / 数据 / 输出资产` | 代码、数据、输出、结果表、license 与稳定性。 |
| `R2 当前用途` | 作为主候选、条件候选、converter pressure、paper-only seed evidence、protocol-domain seed method 等。 |

## 旧九个 direct baseline 全量入账

| 原 baseline | seed 方法 ID | 矩阵 / screening ID | 单篇目录 | 输入 NL | 输出 STM | 方法 / LLM | 原装 `<NL, STM>` 可获取性 | 源码 / 数据 / 输出资产 | R2 当前用途 |
|---|---|---|---|---|---|---|---|---|---|
| Structure- and Event-Driven Frameworks | `sefm-llm-state-machine` | `sefm-llm-state-machine` | [papers/sefm-llm-state-machine](../../../corpora/seed_library/sefm-llm-state-machine/) | 8 个非结构化 reactive-system / system descriptions | UML state machine / statechart，含 reference solutions 和多策略生成结果 | LLM；single prompt、structure-driven、event-driven、hybrid strategy；有生成策略但不是 repair loop | 较强：4open artifact 提供 descriptions、reference solutions、生成图 / 表；仍需本地冻结 hash 和 license | 代码 / 数据 / F1 workbook 可访问；anonymous 4open 无正式 release/license | 强主 seed 候选；优先进入 PR-R2 裁决 |
| LLMS EMP / SysML Behavior Models | `llms-emp-stm-subset` | `llms-emp-stm-subset` | [papers/llms-emp-stm-subset](../../../corpora/seed_library/llms-emp-stm-subset/) | 107 个 SysML 行为模型需求描述；只取 `diagram_type=stm` 子集 | PlantUML / SysML STM；ACT/SD 必须排除 | LLM；requirements + prompt；论文含 checking / feedback-regeneration 设计，但公开代码不足 | 较强：本地 parquet 已冻结，可抽 STM 子集输入与目标 / 输出字段 | 数据 / human review / results 强；生成 pipeline 代码未公开；Drive/license 待核 | 强主 seed 候选；STM 子集 seed / judge calibration |
| Designing FSM with GPT-4 | `designing-fsm-gpt4` | `designing-fsm-gpt4` | [papers/designing-fsm-gpt4](../../../corpora/seed_library/designing-fsm-gpt4/) | 合成英文 DFSM / Mealy 需求描述 | CSV DFSM / Mealy machine | GPT-4/GPT-4o；初始生成 + oracle / checking / repair 实验；seed 只能取 initial generation | 中等：GitHub 有样例数据、generated text、部分 Graphviz / score；需隔离 initial outputs，不能混入 oracle repair | 代码仓可访问但无 release/license/依赖锁；部分结果非论文级整理包 | 条件主 seed；initial-generation-only，强防泄漏 |
| TTool-AI | `ttool-ai-smd-subset` | `ttool-ai-smd-subset` | [papers/ttool-ai-smd-subset](../../../corpora/seed_library/ttool-ai-smd-subset/) | platooning、spacebasedsystem、AutomatedBraking 等自然语言系统规范 | SysML/TTool state-machine diagram subset；同时含 BD/IBD 等非 STM | ChatGPT 3.5；TTool-AI 自动反馈循环、语法/语义检查、JSON→TTool XML | 较强但需切片：仓库有规范、XML、results.ods；需要从联合 SysML 模型中分离 SMD | GitHub artifact 强；TTool/OpenAI/provider drift 和 license 需核；有 timed / signal / guard caveat | converter pressure / 条件 seed 方法；R3 定义 SMD/timing 处理后可重裁 |
| Umple thesis | `umple-nl-state-machine` | `umple-nl-state-machine` | [papers/umple-nl-state-machine](../../../corpora/seed_library/umple-nl-state-machine/) | 5 个自然语言 requirements 系统：Blackjack、Course Section、Credit Card、Driver License、Hotel Stay | Umple textual state machine code | Llama 3；zero-shot、one-shot、RAG；无自动 repair loop | 弱：论文给需求与示例，但未公开完整 benchmark、逐次 outputs、corrected references | PDF / thesis 稳定；实验仓库、RAG bundle、输出包、评测脚本未公开 | paper-only seed evidence / 手工重建线索 |
| REQ automotive thesis | `req-mermaid-statechart` | `req-mermaid-statechart` | [papers/req-mermaid-statechart](../../../corpora/seed_library/req-mermaid-statechart/) | Volvo Cars / Car Weaver 产品功能自然语言需求 | Mermaid.js statechart | GPT-3.5/GPT-4/GPT-4o；含数据增强 / 微调 / prompt 生成；无公开闭环资产 | 很弱 / 私有：核心 NL、人工 statecharts、专家评分和输出样本未公开 | 论文公开；代码、数据、输出、训练集均私有或未公开 | private-data seed method / related work；不进主四例 |
| Pushing the Generative Envelope | `pushing-generative-envelope-mbse` | `pushing-generative-envelope-mbse` | [papers/pushing-generative-envelope-mbse](../../../corpora/seed_library/pushing-generative-envelope-mbse/) | air purifier、vacuum 两个简短自然语言 MBSE 题项 | SysML v2 state machine diagrams，同时生成 requirements list | local LLM；Mixtral-8x7B-Instruct、Llama-3-Smaug-8B；zero/one/few-shot、CoT、temperature 消融；无 feedback loop | 弱：论文内题项 / 表格可读，但无逐次 generated STM 包 | 论文公开；无代码、数据包、supplement、raw outputs 或 license | paper-only seed method evidence；prompt/temperature 变量参考 |
| FlowFSM / Agentic Flow | `protocol-flowfsm-seed-method` | `protocol-flowfsm-sentinel` | baseline-only；见矩阵本地 baseline path | RFC 自然语言协议文档，FTP / RTSP | protocol FSM / command rulebook / states-transitions | LLM agent / CrewAI；prompt chaining、CoT、command extraction→transition analysis→rulebook synthesis | 弱：公开 RFC 输入；作者原装 rulebook / GT / extracted transitions 未公开 | GitHub 目前是仓库壳；无源码、GT、逐转移输出；论文表格可读 | protocol-domain seed method；长文档/agentic extraction 参考，不默认进控制系统四例 |
| SpecGPT / 3GPP extraction | `specgpt-3gpp-seed-method` | `3gpp-protocol-sentinel` | baseline-only；见矩阵本地 baseline path | 3GPP Release 17 NAS / NGAP / PFCP 自然语言/半结构化标准文档 | protocol FSM，含状态、condition/action、转移 | GPT-4o、DeepSeek V3、Qwen Turbo、Claude Sonnet 4、Gemini 2.5 Pro；CoT/few-shot/context stitching/ensemble | 弱：输入规格公开，但作者原装 GT、输出 FSM、逐转移结果未公开 | 无公开 SpecGPT 代码和 GT；3GPP dynareport 是活入口，需锁版本 | protocol-domain seed method；ensemble / span grounding 方法参考，不默认进控制系统四例 |

## 当前必须保留的解释

1. **旧九个 direct baseline 全部属于 seed 方法视野**：它们都说明了一类 `NL / 文本规格 -> STM-family` 的上游生成、抽取或建模路线。
2. **是否进入 PR-R2 主四例取决于资产层**：需要能冻结原装输入、原装 STM 输出、license / hash、样本切片和泄漏控制；不是只看论文是否相关。
3. **protocol-domain 不等于“没有 seed 价值”**：FlowFSM 和 SpecGPT 不适合作为默认控制系统四例，但它们仍是长文档文本到 FSM 的 seed 方法证据和方法学参考。
4. **paper-only 不等于“没考虑”**：Pushing Envelope、Umple、REQ 等应作为 seed 方法证据 / related work / reconstruction 线索入账，只是不直接计入当前主四例。
