# Generating SysML Behavior Models via Large Language Models: an Empirical Study — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `llms-emp-feedback` |
| 标题 | Generating SysML Behavior Models via Large Language Models: an Empirical Study |
| 年份 / venue | 2025 / Internetware |
| 当前角色 | STM 子集 feedback-regeneration baseline |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | SysML behavior model requirements descriptions；只取 STM 子集 |
| 模型 / STM 输出 | PlantUML/SysML State Machine Diagram；含 state、region、pseudostate、transition 等 |
| 修正 / 补全 / refinement 方法 | Phase-I 生成；Phase-II 用 model-checking rules 检出 format / grammar / semantic / requirement inconsistency，把 Error(E) 反馈给 fresh LLM session 再生成 |
| feedback 来源 | PlantUML 格式、SysML grammar、SysML semantics、requirements consistency；含人工检查成分 |
| 自动化程度 | LLM 调用自动；grammar / semantic checking 有人工边界 |
| LLM / agent 角色 | GPT-4 Turbo、GPT-4o、Kimi、Claude 3 Haiku、Llama3.1、DeepSeek-v3 |

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

P1：比 TTool-AI 更直接报告 feedback regeneration 效果，特别适合 related work 和消融设计；必须只写 STM 子集。

## 4. 证据位置

`paper_content.txt` RQ、两阶段流程、prompt Error(E)、STM 错误类型、Phase-II 修复率；旁路核验材料复核。

## 5. 主要风险与使用边界

pipeline 源码未公开；STM 数量口径存在 34/36/38 等需数据复核；feedback 不是 formal counterexample；不能混入 ACT/SD。
