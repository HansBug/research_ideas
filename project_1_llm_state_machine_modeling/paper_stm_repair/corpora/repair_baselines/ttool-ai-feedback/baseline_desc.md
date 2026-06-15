# System Architects Are not Alone Anymore: Automatic System Modeling with AI — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `ttool-ai-feedback` |
| 标题 | System Architects Are not Alone Anymore: Automatic System Modeling with AI |
| 年份 / venue | 2024 / MODELSWARD |
| 当前角色 | 生成链内 feedback-regeneration baseline |
| 阅读来源 | 本地 `paper_content.txt` + 独立全文阅读任务结果 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 自然语言系统规范 + SysML/TTool 知识与图上下文 |
| 模型 / STM 输出 | TTool/SysML BDD/IBD/SMD；本目录只关心 SMD feedback |
| 修正 / 补全 / refinement 方法 | LLM 生成 JSON / model 后，TTool-AI 检查格式、JSON、SysML/TTool syntax / constraints，错误反馈再问 GPT |
| feedback 来源 | JSON parsing、syntax、TTool/SysML constraint feedback；非 model-checking counterexample |
| 自动化程度 | 实验中生成与反馈循环高度自动，但可有人机 refinement |
| LLM / agent 角色 | GPT-3.5 turbo 作为生成器与反馈再生成器 |

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

P1：说明工具检查反馈能改善 LLM 生成模型，但反馈深度主要是语法/约束级。

## 4. 证据位置

`paper_content.txt` 框架、feedback loop、state machine identification、GitHub artifact；独立全文阅读任务核验。

## 5. 主要风险与使用边界

不是独立 `STM_0 -> STM_k` formal repair；状态机仍可能留下 guard/signal 问题；复现依赖 TTool/OpenAI/provider drift。
