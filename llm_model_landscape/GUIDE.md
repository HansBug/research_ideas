# LLM 模型现状文库维护指南

本指南约束根目录 [llm_model_landscape/](./) 的长期维护。该目录是固定三件套微型文库，默认只维护 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。

## 1. 目标与任务边界

### 1.1 目标

1. 为 `project_1` 及后续研究提供可复用的 LLM 模型信息总账。
2. 记录模型发布时间、上下文窗口、最大输出、官方价格、官方来源、可获取方式和实验适配建议。
3. 让模型选择、成本估算、baseline 公平性和论文写作中的模型描述有统一出处。
4. 防止把旧模型、别名、preview、hosted API、开放权重和第三方托管混为一谈。

### 1.2 边界

本文库不做：

1. 不维护 benchmark 排名或实验结果 leaderboard。
2. 不保存 PDF 原文，不替代 `project_1_llm_state_machine_modeling/baselines/`。
3. 不维护每个模型的完整技术报告摘要，只记录对研究实验必要的可调用/可获取信息。
4. 不记录无官方来源的传言模型。
5. 不新增大量分册；若信息膨胀，应优先压缩 [SUMMARY.md](./SUMMARY.md)，而不是拆出许多临时 Markdown。

## 2. 来源优先级

更新模型信息时，必须优先使用官方或一手来源，优先级如下：

1. Provider 官方 API 文档、模型页、pricing 页、release notes。
2. 官方模型卡：Hugging Face org、ModelScope、GitHub release、官方 technical report。
3. 官方博客或新闻稿。
4. 云厂商官方文档，如 Vertex AI、Azure AI Foundry、Amazon Bedrock、Alibaba Cloud Model Studio。
5. 只有当官方来源缺失时，才允许用论文或第三方材料补充历史背景；此时必须标注“非官方来源”。

高优先级官方入口示例：

| Provider/系列 | 优先入口 |
|---|---|
| OpenAI | `developers.openai.com` 模型页与 pricing 页 |
| Anthropic | `docs.anthropic.com` / `platform.claude.com` pricing 与 `anthropic.com/news` |
| Google Gemini | `ai.google.dev` models/pricing 与 Vertex AI lifecycle/pricing |
| DeepSeek | `api-docs.deepseek.com` release/pricing 与官方 GitHub |
| Qwen | `qwen.ai`、`qwencloud.com`、`qwenlm.github.io`、`huggingface.co/Qwen`、`github.com/QwenLM` |
| Llama | `ai.meta.com` 与 `huggingface.co/meta-llama` |
| Grok | `docs.x.ai` 与 `x.ai/news` |
| Mistral | `docs.mistral.ai` |

## 3. 排序规则

### 3.1 硬性排序规则

[SUMMARY.md](./SUMMARY.md) 中所有正式模型表格默认必须按**发布时间从高到低**排序，即最新模型靠前、老旧模型靠后。

适用范围：

1. Hosted / frontier API 总表。
2. Qwen 专项表。
3. Llama 专项表。
4. Grok 专项表。
5. Open-source / open-weight 高频系列表。
6. `project_1/baselines` 文献模型清单。

### 3.2 发布时间取值优先级

若一个模型有多个时间字段，按以下优先级确定排序键：

1. 官方 release / announcement 日期。
2. 官方 GA 日期。
3. 官方模型卡 `lastModified` 或 model card 发布时间。
4. 论文发表年份或 arXiv 年份。
5. 若只能确认年份，按该年份排序；同年内部再按模型族重要性和可用性排序。

### 3.3 系列与子型号排序

1. 同一 provider 内，先按最新具体模型线排序，再列历史线。
2. 同一系列中，hosted/API 最新线优先于历史线；开放权重与 hosted API 必须分清。
3. preview 模型可以排在对应发布时间位置，但必须在“状态/风险”字段写明 preview。
4. legacy / retired / alias 模型放在同系列末尾，并写明不建议作为长期 baseline。

## 4. 字段口径

正式表格默认使用以下字段：

| 字段 | 说明 |
|---|---|
| Provider/系列 | 模型提供方或模型族，如 OpenAI GPT、Qwen、Llama |
| 代表 model ID | 可调用或可下载的精确 model ID；若无精确 ID，写代表模型名 |
| 发布时间/状态 | 官方发布时间、GA/preview/retired/lastModified 状态 |
| context / max output | 上下文窗口与最大输出；无官方统一口径时明确写“官方未统一列” |
| 官方价格/计价 | hosted API 写官方 token 价；开放权重写“无统一 token 价” |
| 来源 | 官方可点击链接 |
| 备注/风险 | preview、alias、discount、region-specific、开源/闭源差异等 |

## 5. 价格规则

1. 默认单位为 `USD / 1M tokens`。
2. 若官方价格为 RMB、per 1K tokens、云平台区域价，必须在单元格中显式说明。
3. 若页面同时给 list price 和折扣价，优先记录 list price，并在备注中写折扣价或折扣状态。
4. 开放权重模型不写第三方托管价格作为“官方价格”；应写“开放权重无统一 token 价”。
5. 若实际实验使用第三方托管，应在实验 run record 中另行记录 provider、region、价格页和调用日期。

## 6. 更新流程

一次完整维护默认按以下步骤执行：

1. 阅读 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
2. 明确本轮更新目标：新增模型、更新价格、修正上下文、重排表格、补来源、处理 retired/alias。
3. 优先访问官方来源，必要时用 Hugging Face API、GitHub release、provider docs 辅助核验。
4. 更新 [SUMMARY.md](./SUMMARY.md) 表格，保证每个表按发布时间降序。
5. 更新统计、待复查项、失败记录和更新日志。
6. 若本轮更新改变了维护口径，同步更新本 [GUIDE.md](./GUIDE.md)。
7. 若新增了本文库职责或入口，同步更新仓库根级 [../CLAUDE.md](../CLAUDE.md)。注意 [../AGENTS.md](../AGENTS.md) 是软链接，不要重复编辑两份。
8. 结束前做一致性检查。

## 7. 一致性检查清单

每轮提交前必须检查：

- [ ] [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 三件套存在且链接相互可达。
- [ ] 所有正式模型表格按发布时间降序排列。
- [ ] 每个模型条目都有来源链接；没有来源的条目标为待核验，不写成事实。
- [ ] hosted API 与开放权重没有混写。
- [ ] 价格单位清楚；折扣价与 list price 没有混淆。
- [ ] preview / retired / alias / region-specific 风险已标注。
- [ ] 更新日志时间使用 `yyyy-mm-dd hh:mm:ss`。
- [ ] 若更新了根级引导，只编辑 [../CLAUDE.md](../CLAUDE.md)，不单独编辑软链接 [../AGENTS.md](../AGENTS.md)。

## 8. 与 issue / PR / 讨论纪要的关系

1. GitHub issue 可以作为一次性调研草稿，但长期真源应回填到 [SUMMARY.md](./SUMMARY.md)。
2. PR body 或 discussion comment 中的模型信息若有长期价值，应整合进 [SUMMARY.md](./SUMMARY.md)，不要只停留在评论里。
3. 若 issue 与 [SUMMARY.md](./SUMMARY.md) 不一致，以最近一次官方核验过的 [SUMMARY.md](./SUMMARY.md) 为准；issue 可保留历史讨论痕迹。
4. 后续论文写作引用模型信息时，优先引用 provider 官方来源；本文库负责帮忙定位这些来源，不替代正式引用。

