# PAT-Agent: Autoformalization for Model Checking — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `pat-agent` |
| 标题 | PAT-Agent: Autoformalization for Model Checking |
| 年份 / venue | 2025 / arXiv / ASE 2025 accepted |
| 当前角色 | 异构形式化 repair 强近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 自然语言系统描述 + assertions / expected result |
| 模型 / STM 输出 | PAT/CSP# process model；可展开 LTS，但非 STM family |
| 修正 / 补全 / refinement 方法 | Planning LLM + Code Generation LLM + PAT model checking；结果不符时用 counterexample trace 定位可疑 action 并迭代 repair |
| feedback 来源 | PAT verification outcome、counterexample / violation trace、property type 与 expected result |
| 自动化程度 | pipeline 可全自动；另有 web interface |
| LLM / agent 角色 | Planning: OpenAI o3-mini-2025-01-31；Code Generation: Claude 3.7 Sonnet；还评估 DeepSeek-R1 等 |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

不能作为同构 STM baseline；但强力支撑“formal checker counterexample 可转化为局部修复指令”的方法论。

## 4. 证据位置

`paper_content.txt` 摘要、框架、verification-repair loop、case、实验、ablation、结论；旁路核验材料复核。

## 5. 主要风险与使用边界

输入包含 properties / expected result 强监督；输出 CSP# 非 STM；repair heuristic 泛化需谨慎；正式 proceedings 元数据待复核。
