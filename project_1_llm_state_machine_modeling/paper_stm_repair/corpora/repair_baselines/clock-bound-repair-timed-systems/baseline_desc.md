# Clock Bound Repair for Timed Systems — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `clock-bound-repair-timed-systems` |
| 标题 | Clock Bound Repair for Timed Systems |
| 年份 / venue | 2019 / CAV |
| 当前角色 | 异构 timed-automata repair 强近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL；timed safety property 是形式化性质/需求约束，不是自然语言 repair 输入 |
| 模型 / STM 输入 | Networks of Timed Automata (NTA) / UPPAAL timed automata |
| 修正输入 | NTA + UPPAAL timed diagnostic trace (TDT) + violated timed safety property |
| 修正输出 | 修改 clock bounds 的 repaired NTA 候选；通过 functional equivalence/admissibility 检查 |
| 修正 / 补全 / refinement 方法 | TDT 线性实数编码 + MaxSMT/Z3 最小 syntactic repair + untimed-language functional equivalence admissibility |
| feedback 来源 | UPPAAL timed diagnostic trace / timed safety violation / admissibility check |
| 自动化程度 | 自动化工具 TarTar 原型；实验基于 fault seeding |
| LLM / agent 角色 | 无 |

## 3. 与本文 `<NL, STM_0> -> Better STM` 的关系

不满足本文 baseline：没有 NL，也没有由 NL 生成的 STM_0；但提供 verifier/counterexample-guided formal repair 的方法近邻。

## 4. 证据位置

paper_content.txt:8-20, 92-121, 586-620, 690-706；论文脚注给出 TarTar/model GitHub：paper_content.txt:114-115

## 5. 主要风险与使用边界

Timed automata 与本文 T0+FSM/HSM/EFSM/statechart 谱系不同；输入是 formal property + TDT，不是 NL；只能作异构形式化 repair 参考。
