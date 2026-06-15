# Designing FSMs Specifications from Requirements with GPT 4.0 — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `designing-fsm-gpt4-repair` |
| 标题 | Designing FSMs Specifications from Requirements with GPT 4.0 |
| 年份 / venue | 2026 / arXiv |
| 当前角色 | seed + repair 分段共存；本目录只登记 repair slice |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 合成英文 DFSM / Mealy 描述；repair 阶段还用 oracle / trace / expert output |
| 模型 / STM 输出 | CSV DFSM / Mealy machine；平坦 deterministic FSM |
| 修正 / 补全 / refinement 方法 | syntax fault repair、distinguishing sequence repair、checking sequence repair、fault-model / mutation-machine repair |
| feedback 来源 | oracle 结构差异、oracle trace、专家 checking sequence 输出、repair-domain query |
| 自动化程度 | 初始生成自动；repair 多处依赖 oracle 或专家，fault-model 较自动 |
| LLM / agent 角色 | GPT-4/GPT-4o 初始生成与部分 prompt-based repair；fault-model repair 更偏形式化候选搜索 |

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

最清楚展示“LLM 生成 FSM 后如何诊断/修复”的候选；但应切片，初始 `NL -> DFSM` 仍归 seed。

## 4. 证据位置

`paper_content.txt` DFSM 定义、repair 方法四节、实验结果与局限；旁路核验材料复核。

## 5. 主要风险与使用边界

数据合成且非真实控制系统；oracle 在现实场景通常缺失；STM 语义弱于本论文目标；论文未在正文给正式 artifact 链接。
