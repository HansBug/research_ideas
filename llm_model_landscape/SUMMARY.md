# LLM 模型现状总账

> 核验日期：2026-06-04。价格默认是 **USD / 1M tokens**，除非单元格明确说明。完整模型表已拆到独立 Markdown；本文件只保留统计结论、当前重点模型摘要、风险记录和跳转入口，不替代各分册中的完整事实表。模型可用性、上下文窗口、最大输出、官方价格、preview/stable/retired 状态、折扣和区域可用性会变化；正式实验必须记录精确 `model_id`、provider、region、调用日期和官方链接。

## 1. 文库整体概况

| 项 | 当前状态 |
|---|---:|
| 当前维护文件数 | 12 |
| 总览文件数 | 3 |
| 完整表文件数 | 9 |
| `project_1/baselines` LLM 相关条目数 | 34 |
| OpenAI 完整表条目数 | 12 |
| Claude 完整表条目数 | 11 |
| Gemini 完整表条目数 | 8 |
| DeepSeek 完整表条目数 | 11 |
| Qwen 完整表条目数 | 8 |
| Llama 完整表条目数 | 6 |
| Grok 完整表条目数 | 7 |
| 其他开源/开放权重完整表条目数 | 15 |
| 本轮新增数量 | 新增 1 个 LLM 模型现状文库；当前包含 3 个入口文件与 9 个完整表分册 |
| 尚待复查项 | Gemini 3.x/3.5 精确 ID、Kimi K2.x、部分云厂商价格、Qwen3.7 国内/国际价差 |

## 2. 文件索引

| 文件 | 内容 | 维护口径 |
|---|---|---|
| [baseline_models.md](./baseline_models.md) | `project_1/baselines` 论文中使用/提到的 LLM 完整表、年度统计和热门模型族分析 | 按论文年份降序；同年内部保持当前整理顺序 |
| [openai_models.md](./openai_models.md) | OpenAI / GPT / Codex 系列完整表 | 按官方发布时间降序 |
| [claude_models.md](./claude_models.md) | Anthropic Claude 系列完整表 | 按官方发布时间降序 |
| [gemini_models.md](./gemini_models.md) | Google Gemini 系列完整表 | 按官方发布时间降序；实验前重查精确 ID |
| [deepseek_models.md](./deepseek_models.md) | DeepSeek hosted API 与开放权重完整表 | 按官方发布时间降序，alias 单独标注 |
| [qwen_models.md](./qwen_models.md) | Qwen hosted API 与开放权重完整表 | 按官方发布时间降序；hosted 与 open-weight 分清 |
| [llama_models.md](./llama_models.md) | Meta Llama 系列完整表 | 按官方发布时间降序 |
| [grok_models.md](./grok_models.md) | xAI Grok 系列完整表 | 按官方发布时间降序；`2026-current` 表示 docs-visible latest |
| [other_open_models.md](./other_open_models.md) | OpenAI gpt-oss、Kimi/Moonshot、Mistral、Gemma、Granite、Nemotron、Phi、GLM、InternLM、Baichuan、Yi、CogVLM、Falcon、GPT-J/GPT-Neo 等 | 按可核验发布时间降序；年份级条目同年内部不表达严格先后，后续补精确日期 |

## 3. `project_1` baseline 模型使用统计结论

完整表与年度统计见 [baseline_models.md](./baseline_models.md)。

### 3.1 年度分布

| Year | LLM 相关 baseline 条目数 | 当年最常出现模型族 | 结论 |
|---:|---:|---|---|
| 2026 | 4 | OpenAI/GPT(4), Claude(3), Gemini(2), Llama(2), Grok(2), Qwen(2) | 新论文开始明显转向 GPT-5、Claude 4.x、Gemini 2.5/3.x、Qwen3、Llama4、Grok 等新一代模型；新实验不能只停留在 GPT-4o / Claude 3.5。 |
| 2025 | 18 | OpenAI/GPT(15), Llama(10), DeepSeek(7), Claude(5), Mistral/Mixtral/Codestral(4) | LLM-for-modeling 论文爆发年，OpenAI/GPT 仍最常见，但开放权重与多模型矩阵显著增多，DeepSeek/Llama/Qwen/Mistral 已成为常见 baseline。 |
| 2024 | 8 | OpenAI/GPT(8), Llama(2), Claude(1), Gemini(1), CogVLM(1) | ChatGPT/GPT-4/GPT-4o 仍是主线，同时开始出现 Claude、Gemini、CogVLM、LLaMA/Qwen 等替代路线。 |
| 2023 | 3 | OpenAI/GPT(3) | 主要是 ChatGPT/GPT-4/GPT-3 时代的早期 UML/MDSE 探索，模型选择集中度很高。 |
| 2022 | 1 | OpenAI/GPT(1), GPT-J/GPT-Neo(1) | pre-ChatGPT few-shot MDSE 背景，主要用于历史相关工作。 |

### 3.2 总体高频模型族

| 排名 | 模型族 | 出现条目数 | 对 baseline 选择的含义 |
|---:|---|---:|---|
| 1 | OpenAI/GPT | 31 | 几乎贯穿所有年份，是历史 baseline 与当前 frontier 的共同主线；新实验至少保留一个强 GPT 与一个低价 GPT。 |
| 2 | Llama | 14 | 开放权重/自托管最常见路线；适合作为可复现 baseline。 |
| 3 | Claude | 9 | 强闭源对照中高频；适合与 GPT 形成 frontier 双基线。 |
| 4 | DeepSeek | 8 | 2025 后快速进入 UML/SysML/benchmark baseline；适合作为高性价比 hosted 与 open-weight 双线。 |
| 5 | Qwen | 6 | 中文与开放权重双线候选；Qwen3.7 hosted 与 Qwen3.6/3.5 open-weight 要分开记录。 |
| 6 | Gemini | 5 | 多模态/长上下文闭源对照；需要实验前核验 preview/stable 和精确 ID。 |
| 7 | Mistral/Mixtral/Codestral | 5 | 欧洲/开放生态常用替代基线，适合补充 open-weight 与代码模型对照。 |
| 8 | Grok | 3 | 新一代 agentic/coding 对照，适合放入 frontier 扩展组。 |

## 4. OpenAI GPT 当前重点模型

完整表见 [openai_models.md](./openai_models.md)。

| 优先级 | 模型 | 为什么当前值得关注 | 风险/注意 |
|---:|---|---|---|
| 1 | `gpt-5.5` | GPT 强能力上界，1.05M context / 128K output | 长上下文价与标准价不同 |
| 2 | `gpt-5.4-mini` | 较新的低价 GPT-5.4 线，适合成本敏感实验 | 晚于 GPT-5.4，不能按型号数字误排 |
| 3 | `gpt-5.3-codex` | Codex 专项，适合 agentic/coding 对照 | 与通用 GPT baseline 分开记录 |

## 5. Claude 当前重点模型

完整表见 [claude_models.md](./claude_models.md)。

| 优先级 | 模型 | 为什么当前值得关注 | 风险/注意 |
|---:|---|---|---|
| 1 | Claude Opus 4.8 | 当前 Claude 强能力上界，1M context | 成本高，输出上限需按调用配置核验 |
| 2 | Claude Sonnet 4.6 | 当前 Sonnet 平衡线，适合主力 baseline | 与 Opus 价格/能力差异需写明 |
| 3 | Claude Haiku 4.5 | 低价 Claude 对照 | 适合作成本组，不宜代表 Claude 上界 |

## 6. Gemini 当前重点模型

完整表见 [gemini_models.md](./gemini_models.md)。

| 优先级 | 模型 | 为什么当前值得关注 | 风险/注意 |
|---:|---|---|---|
| 1 | Gemini 3.5 Flash | Google models 页 current 新线，适合多模态/长上下文对照 | 精确 ID、preview/stable、pricing 需实验前重查 |
| 2 | Gemini 3 Pro / 3 Flash | Gemini 3 系列 frontier/低价组合 | preview/lifecycle 变化快 |
| 3 | Gemini 2.5 Pro / Flash / Flash-Lite | baseline 文献常见，GA/长上下文对照 | 低于 Gemini 3.x，适合作历史/稳定对照 |

## 7. DeepSeek 当前重点模型

完整表见 [deepseek_models.md](./deepseek_models.md)。

| 优先级 | 模型 | 为什么当前值得关注 | 风险/注意 |
|---:|---|---|---|
| 1 | DeepSeek V4-Pro / V4-Flash | 1M context / 384K output；Flash 价格低 | `deepseek-chat` / `deepseek-reasoner` 是 alias，不宜作长期 ID |
| 2 | DeepSeek-R1 / R1-0528 | reasoning open-weight 常用对照 | hosted 与 checkpoint 口径分开 |
| 3 | DeepSeek-V3/V3.1/V3.2 | 2025 baseline 高频开权重线 | 需记录具体 checkpoint |

## 8. Qwen 当前重点模型

完整表见 [qwen_models.md](./qwen_models.md)。

| 优先级 | 模型 | 类型 | 为什么当前值得关注 | 风险/注意 |
|---:|---|---|---|---|
| 1 | `qwen3.7-plus` | hosted API | 2026-06 可见，1M context，成本较低，多模态/agent 能力强 | 不是开放权重；需要记录 Qwen Cloud / region / 折扣状态 |
| 2 | `qwen3.7-max` | hosted API | Qwen3.7 系列强能力 hosted 上界，1M context | 价格高于 Plus，public interface 以 text 为主 |
| 3 | Qwen3.6-35B-A3B / 27B | 开放权重 | HF 官方 org 可见，262K 原生、可扩 1.01M | 自托管需记录量化、推理框架、rope/Yarn 设置 |
| 4 | Qwen3-Coder-480B-A35B / 30B-A3B | 开放权重/代码 | repository-scale coding 与 agentic coding 候选 | 推理成本高，需明确硬件与部署方式 |

## 9. Llama 当前重点模型

完整表见 [llama_models.md](./llama_models.md)。

| 优先级 | 模型 | 为什么当前值得关注 | 风险/注意 |
|---:|---|---|---|
| 1 | Llama 4 Scout / Maverick | 当前 Meta 主系列上界；Scout 10M、Maverick 1M context | 官方未统一列 max output；部署成本高 |
| 2 | Llama 3.3-70B-Instruct | 70B 开放权重强基线，生态成熟 | 只是 3.x 更新线，不是 Llama 4 后继 |
| 3 | Llama 3.1 8B/70B/405B | 128K context，baseline 文献高频 | 旧于 Llama 3.3/4，但适合历史可比 |

截至本轮官方核验，未找到 Llama 4 之后的新主系列。

## 10. Grok 当前重点模型

完整表见 [grok_models.md](./grok_models.md)。

| 优先级 | 模型 | 为什么当前值得关注 | 风险/注意 |
|---:|---|---|---|
| 1 | `grok-4.3` | 当前 xAI docs-visible latest，1M context，支持 tools/structured/reasoning 等 | 首发日待精确核验，需记录调用日期 |
| 2 | `grok-4.20-0309-*` / multi-agent | 2026-03 release notes 明确，适合 agentic 上界/多智能体对照 | multi-agent 不宜作为常规 baseline 上限外推 |
| 3 | Grok-4 legacy / 4.1 Fast | 解释历史迁移与 reroute | 作为历史/兼容背景，不建议新实验主用 legacy ID |

## 11. 其他常见模型当前重点系列

完整表见 [other_open_models.md](./other_open_models.md)。

| 优先级 | 系列 | 当前值得关注的代表 | 为什么值得关注 | 风险/注意 |
|---:|---|---|---|---|
| 1 | OpenAI gpt-oss | gpt-oss-120b / gpt-oss-20b | 已进入 baseline 文献口径，适合作开放权重 GPT-family 对照 | 与 OpenAI hosted GPT API 不是同一价格/部署口径 |
| 2 | Kimi/Moonshot | Kimi-K2-Instruct / Kimi-K2-Thinking | 进入待复查项，适合作中文/agentic 开放权重补充 | hosted 与开放权重需分开记录 |
| 3 | DeepSeek open weights | V4 / V3.2 / R1 updates | hosted 与 open-weight 双线，价格/能力比高 | checkpoint 与 hosted ID 不能混写 |
| 4 | Mistral/Mixtral/Codestral | Large/Small/Magistral/Codestral | 欧洲/开放生态常见替代 baseline，代码模型可补强 | 具体 context/price 按模型页变化 |
| 5 | Gemma | Gemma3 | Google 开放模型线，适合轻量/可复现对照 | 与 Gemini hosted 不是同一口径 |
| 6 | GLM/ChatGLM | GLM-4.7 / GLM-5 | 中文 hosted/API 线候选 | 价格和可用区域需实验前核验 |
| 7 | Phi / Granite / Nemotron | Phi-4、Granite 3.x、Nemotron-3 | 小模型、企业开源、NIM 部署等补充线 | 多数不是 project_1 主 baseline，只作补充组 |

## 12. 风险项、待复查与失败记录

### 12.1 风险项与待复查记录

| 项 | 状态 | 建议 |
|---|---|---|
| Qwen3.7 | hosted API 已见；HF `Qwen` org 本轮未见同名开权重 | issue/实验中写 `qwen3.7-max` / `qwen3.7-plus` 并标 hosted；不要写成开源权重 |
| Qwen3.5/3.6 | HF 开权重已见，很多卡片是 262K 原生、可扩 1.01M | 若自托管，必须记录 checkpoint、量化、推理框架、YaRN/rope scaling 设置 |
| Llama 4 | 当前 Meta 主系列上界；Llama 3.3 是 70B Instruct 更新线 | 若用 Llama baseline，优先 Llama 4 Scout/Maverick 或 Llama 3.3/3.1 作为可复现对照 |
| Gemini 3.x / 3.5 | 官方页存在较新/preview/stable 条目，生命周期变化快 | 实验必须写精确 model ID 与调用日期，不只写 Gemini |
| DeepSeek aliases | `deepseek-chat` / `deepseek-reasoner` 有兼容/退役风险 | 正式 baseline 写 V4-Pro/Flash 或具体 open-weight checkpoint |
| GPT legacy / davinci / old Codex | 多数已停用或 legacy | 只作为历史相关工作，不作为新实验 baseline |
| 开源模型 API 价格 | 多数开放权重无统一官方 token 价 | 自托管记录硬件、量化、框架、吞吐；云托管记录云厂商、region、价格页 |

### 12.2 失败与阻塞记录

| 时间 | 对象 | 类型 | 记录 | 后续处理 |
|---|---|---|---|---|
| 2026-06-04 15:31:19 | Qwen3.7 开放权重 | 未发现/待复查 | 本轮在 Hugging Face `Qwen` 官方 org 未发现同名 `Qwen3.7` 开放权重集合；仅确认 Qwen Cloud hosted API 线 | 后续若 Qwen 官方发布开权重，应新增独立条目并更新 hosted/open-weight 区分 |
| 2026-06-04 15:31:19 | Grok-4.3 首发日 | 证据不足 | 本轮确认 xAI docs-visible latest 与模型页规格/价格，但未找到像 Grok-4.20 release notes 一样清晰的单页首发日 | 暂用 `2026-current` 排序键，后续补精确官方发布日期 |
| 2026-06-04 15:31:19 | Gemini 3.x/3.5 精确 ID | 待复查 | Gemini 官方 models/pricing 页面变化快，部分条目需按实验前精确 model ID 再核 | 实验前重新核验 lifecycle、pricing、preview/stable 状态 |

## 13. 对 `proj1` Path-1 / Path-2 的直接影响

1. baseline 不能只选旧 GPT-4o / Claude 3.5：baseline 文献已经出现 GPT-5、Claude 4.x、Gemini 3.x、DeepSeek V4、Qwen3.x、Llama4、Grok4.x 这类新线；新实验至少应覆盖“强闭源 + 成本平衡 + 开权重/自托管”三层。
2. Qwen 要双轨记录：开放权重最新可核验到 Qwen3.6/3.5 与 Qwen3-Coder；Qwen3.7 当前是 hosted API 线。
3. Llama 4 是当前 Meta 主系列上界：Llama 3.3 存在但只是 70B Instruct 更新；未核验到 Llama 5 或 Llama 4 后继主系列。
4. 价格敏感实验优先 DeepSeek V4-Flash / Gemini Flash / Qwen3.7-Plus / GPT-5.4-mini；强能力上界优先 GPT-5.5 / Claude Opus 4.8 / Gemini 3.x / DeepSeek V4-Pro / Grok-4.3。
5. 所有 run record 必须保存 model ID：不要只写“Claude”“Gemini”“Qwen”“Grok”，否则后续无法解释上下文长度、输出上限、价格和退役差异。

## 14. 更新日志

| 时间 | 更新内容 | 备注 |
|---|---|---|
| 2026-06-04 16:05:00 | 将 SUMMARY 中完整大表拆分为 [baseline_models.md](./baseline_models.md)、[openai_models.md](./openai_models.md)、[claude_models.md](./claude_models.md)、[gemini_models.md](./gemini_models.md)、[deepseek_models.md](./deepseek_models.md)、[qwen_models.md](./qwen_models.md)、[llama_models.md](./llama_models.md)、[grok_models.md](./grok_models.md)、[other_open_models.md](./other_open_models.md) | SUMMARY 改为统计结论、重点模型与链接索引 |
| 2026-06-04 15:31:19 | 初始化根目录 LLM 模型现状微型文库，建立 README/GUIDE/SUMMARY 三件套，并把 issue #32 调研内容整理为长期总账 | 各模型表按发布时间降序；后续仍需持续核验价格与生命周期 |

## 15. 后续建议

- [ ] 选定 `proj1` 第一轮模型矩阵：强/平衡/低价/开源各 2-4 个。
- [ ] 为每个模型固定精确 `model_id`、provider、region、调用日期、价格链接。
- [ ] 把本目录的 baseline 文献模型清单择要回填到 `project_1_llm_state_machine_modeling/baselines/SUMMARY.md` 的模型盘点部分。
- [ ] 对 Gemini 3.x、Qwen3.7、Kimi K2.x、Grok 4.x 等 2026 新模型定期做精确 model ID 级核验。
