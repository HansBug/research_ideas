# Towards Automatic Model Completion: from Requirements to SysML State Machines — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `towards-automatic-model-completion` |
| 标题 | Towards Automatic Model Completion: from Requirements to SysML State Machines |
| 年份 / venue | 2022 / arXiv |
| 当前角色 | precursor / 弱 baseline |
| 阅读来源 | 本地 `paper_content.txt` + 独立全文阅读任务结果 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | BDD/GWT textual requirements |
| 模型 / STM 输出 | partial SysML SMD；已有 states，补 transitions |
| 修正 / 补全 / refinement 方法 | ClauseExtractor + AST + givenCmp/whenCmp/thenCmp，生成 SysML state-machine fragments |
| feedback 来源 | 主要是 modeller check / traceability support；无自动 verifier loop |
| 自动化程度 | 概念性半自动 |
| LLM / agent 角色 | 无核心 LLM 角色 |

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

2024 SoSyM 工作的早期版本，适合记录方法演进，不应重复计为独立强 baseline。

## 4. 证据位置

`paper_content.txt` 摘要、目标、partial SMD、toolchain、railway example；独立全文阅读任务核验。

## 5. 主要风险与使用边界

早期构想，工具链未完全落地；实验弱；无公开代码/数据；非 repair loop。
