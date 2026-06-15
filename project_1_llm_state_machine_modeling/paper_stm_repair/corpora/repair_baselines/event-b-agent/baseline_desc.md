# Event-B Agent: Towards LLM Agent for Formal Model Synthesis and Repair — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `event-b-agent` |
| 标题 | Event-B Agent: Towards LLM Agent for Formal Model Synthesis and Repair |
| 年份 / venue | 2026 / arXiv / FSE 2026 accepted |
| 当前角色 | 异构 formal-state repair 强近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 自然语言需求文档；实验含轻量 EQP/FUN 标签用于评估 |
| 模型 / STM 输出 | Event-B contexts / machines / variables / invariants / events / refinements / proofs；非 STM family |
| 修正 / 补全 / refinement 方法 | LLM refinement planning + schema-guided synthesis + ProB/Rodin/SMT/proof feedback + atomic repair functions；修改后 replay proofs |
| feedback 来源 | compiler / schema diagnostics、ProB counterexample、Rodin/SMT/prover proof states、proof obligation 类型、repair history |
| 自动化程度 | 高自动化，但假设需求内部一致 |
| LLM / agent 角色 | GPT-5 medium reasoning backbone；soundness 由 deterministic tools 复核 |

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

显示 SOTA 正从 one-shot NL->formal model 转向 verifier/prover-mediated repair；只能作异构方法上界/近邻。

## 4. 证据位置

`paper_content.txt` 摘要、三阶段、problem statement、refinement、atomic repair、实验、ablation、repair case、data availability；旁路核验材料复核。

## 5. 主要风险与使用边界

输出不是 STM；RC/RF 依赖标签和 refinement assumption；数据部分人工构造；运行成本高；正式元数据待复核。
