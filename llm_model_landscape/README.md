# LLM 模型现状文库

本目录是仓库根目录下的 **LLM 模型现状微型文库**，用于长期维护 `project_1` 及后续博士研究中会用到的常见大语言模型、开放权重模型与 hosted API 模型的上下文窗口、最大输出、价格、发布时间、可获取方式与官方来源。

> 维护口径：本目录不是论文原文文库，也不是 benchmark 结果库；它是一个固定三件套的小型模型信息总账。默认只维护 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)，除非后续明确需要自动化脚本或快照证据，否则不新增更多 Markdown 分册。

## 1. 文库定位

本微型文库服务于以下研究任务：

1. 为 `project_1_llm_state_machine_modeling` 的 baseline 选择、模型矩阵设计、成本估算和实验记录提供统一模型信息入口。
2. 为 `project_ex1_llm_judge_for_stm`、`project_2`、`project_3`、`project_4` 后续使用 LLM-as-Judge、性质生成、验证剖面生成、模型修复时提供可追溯模型口径。
3. 固定“模型名、发布时间、上下文窗口、最大输出、官方价格、官方来源链接”这些容易随时间漂移的信息，减少讨论纪要和 PR comment 中重复整理。
4. 把 issue 讨论中的一次性调研结果沉淀为 repo 内可维护文档。

## 2. 设立宗旨与期望收获

需要单独建立该文库的原因：

1. LLM 模型迭代速度快，`GPT`、`Claude`、`Gemini`、`DeepSeek`、`Qwen`、`Llama`、`Grok` 等系列的可用型号、上下文窗口和价格会频繁变化。
2. `project_1` baseline 文献已经横跨多代模型；若不维护统一总账，后续实验容易把旧模型、别名、preview 模型和 hosted API 混在一起。
3. 开放权重模型与 hosted API 模型的“价格”含义不同：开放权重通常无统一 token 价，hosted API 才有官方 token 价。
4. 论文写作需要能解释“为什么选择这些模型作为 baseline”，因此模型选择必须有官方链接和日期口径。

期望沉淀：

1. 当前主流模型的发布时间降序表。
2. 每个模型族的代表型号、上下文长度、最大输出和官方价格。
3. `project_1/baselines` 中实际出现过的模型族与年份对应关系。
4. 后续实验选择强/中/低价/开源模型矩阵时的推荐口径。
5. 需要定期复查的高风险项，如 preview、retired、alias、discount、region-specific pricing。

## 3. 收录范围

### 3.1 需要收录

1. `project_1_llm_state_machine_modeling/baselines` 文献中实际使用或明确提到的 LLM / foundation model。
2. 当前可通过官方 API、云平台、Hugging Face、GitHub、ModelScope 等入口稳定获取的主流模型。
3. 对 `project_1` baseline、公平对比、成本估算、长上下文能力或自托管复现有直接影响的模型族。
4. 需要单独追踪的主力系列：OpenAI GPT、Anthropic Claude、Google Gemini、DeepSeek、Qwen、Meta Llama、xAI Grok、Mistral/Mixtral、Gemma、Granite、Nemotron、Phi、GLM、Kimi/Moonshot 等。
5. 历史 baseline 中仍需说明的旧模型，如 GPT-3.5、GPT-4、GPT-J、GPT-Neo、CogVLM。

### 3.2 不需要收录

1. 仅用于图像、语音、embedding、rerank 且与本研究状态机建模/验证/修复无直接关系的模型，除非 baseline 文献明确使用。
2. 没有官方来源、无法稳定检索、只有二手传言的模型。
3. 纯 benchmark 排名信息；本目录维护“可用性与调用口径”，不维护性能 leaderboard。
4. 个人微调、社区量化、GGUF 镜像、第三方转存，除非它是实验实际使用对象且官方原模型已记录。
5. 只有聊天产品名但没有可复现实验 model ID 的条目。

## 4. 纳入/排除判定标准

| 维度 | 纳入标准 | 排除或降优先级标准 |
|---|---|---|
| 研究相关性 | 能作为 `project_1` 或后续项目的生成/评审/修复模型 | 与状态机建模、需求工程、代码/结构化输出无直接关系 |
| 可获取性 | 有官方 API、官方模型卡、官方 GitHub/HF/ModelScope 权重或云平台文档 | 只有新闻转述、论坛传言或不可访问入口 |
| 可追溯性 | 能给出官方链接、发布时间或 lastModified、context、价格/计价说明 | 无法确认上下文窗口、价格或具体 model ID |
| 实验价值 | 能代表 frontier、平衡、低价、开源/自托管中的一类 | 与已有条目高度重复且没有新能力或新使用价值 |
| 长期维护价值 | 是高频 baseline、主力系列或即将替代旧模型的新线 | 临时 preview 且无明确 API ID，除非对当前实验关键 |

## 5. 本文库下文件说明

| 文件 | 职责 | 阅读用途 |
|---|---|---|
| [README.md](./README.md) | 说明本文库定位、范围、收录标准和 AI 工作入口 | 先判断一个模型信息是否应该进入本文库 |
| [GUIDE.md](./GUIDE.md) | 规定长期维护流程、排序规则、字段口径、来源优先级和一致性检查 | 实际更新模型表之前必须先读 |
| [SUMMARY.md](./SUMMARY.md) | 模型信息总账，包含 baseline 模型清单、hosted API 表、各系列专项表和更新日志 | 查询当前模型状态和后续实验建议 |

## 6. 单条模型记录约束

本文库不采用“单模型一个目录”的结构。每个模型条目默认直接写入 [SUMMARY.md](./SUMMARY.md) 的表格中，并至少包含：

1. 模型族或 provider。
2. 精确 model ID 或代表模型名。
3. 发布时间、公告时间、GA 时间或官方 lastModified。
4. 上下文窗口和最大输出；若官方未统一公开，必须写明“官方未统一列”。
5. 官方价格；若为开放权重，则写“开放权重无统一 token 价”。
6. 官方来源链接。
7. 与 `project_1` 的适配说明或风险备注。

## 7. AI 工作入口提示

后续 AI 维护该目录时，默认顺序是：

1. 先读 [README.md](./README.md)：确认文库边界与收录标准。
2. 再读 [GUIDE.md](./GUIDE.md)：确认来源优先级、表格字段、发布时间降序排序规则。
3. 再读 [SUMMARY.md](./SUMMARY.md)：查看当前总账、更新日志和待复查项。
4. 若更新来自 issue/PR/讨论纪要，应把一次性讨论内容整合进 [SUMMARY.md](./SUMMARY.md)，不要机械追加重复段落。
5. 若模型信息来自官方网页，应记录具体链接和核验日期；如果来源不稳定，应在风险项中标注。

