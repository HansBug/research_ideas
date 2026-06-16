# Automated repair for timed systems — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `automated-repair-timed-systems` |
| 标题 | Automated repair for timed systems |
| 年份 / venue | 2021/2022 / FMSD |
| 当前角色 | 异构 timed-automata repair journal 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL；形式化 timed safety property |
| 模型 / STM 输入 | NTA / UPPAAL timed automata |
| 修正输入 | NTA + real-time model checking TDT |
| 修正输出 | clock bounds / operators / resets / urgency 等 syntactic repair；admissible repaired NTA |
| 修正 / 补全 / refinement 方法 | TarTar journal extension：TDT LRA encoding + MaxSMT/Z3 + functional equivalence admissibility |
| feedback 来源 | UPPAAL/Kronos/opaal 类 model checker 返回的 TDT |
| 自动化程度 | 自动化工具原型；fault-seeding evaluation |
| LLM / agent 角色 | 无 |

## 3. 与本文 `<NL, STM_0> -> Better STM` 的关系

不满足本文 baseline：缺 NL 与 NL->STM_0；但 formal counterexample-guided repair 机制最强。

## 4. 证据位置

paper_content.txt:9-24, 52-61, 92-122, 1060-1139, 1162-1453；数据/代码见 paper_content.txt:1468-1469

## 5. 主要风险与使用边界

目标是 timed automata；实验为 seeded faults；无同构 NL-based STM repair 输入。
