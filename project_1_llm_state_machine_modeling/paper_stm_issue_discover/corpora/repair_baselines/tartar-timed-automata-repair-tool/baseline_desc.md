# TarTar: A Timed Automata Repair Tool — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `tartar-timed-automata-repair-tool` |
| 标题 | TarTar: A Timed Automata Repair Tool |
| 年份 / venue | 2020 / CAV tool paper |
| 当前角色 | 异构 timed-automata repair 工具近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL |
| 模型 / STM 输入 | NTA / UPPAAL timed automata |
| 修正输入 | UPPAAL model + timed diagnostic trace / property violation |
| 修正输出 | clock-bound / comparison / clock-reference / reset / urgent-location syntactic repairs |
| 修正 / 补全 / refinement 方法 | TarTar 工具集成 repair computation 与 admissibility analysis，保证 TDT 不再可行并保持 untimed functional behavior |
| feedback 来源 | model checking TDT + admissibility check |
| 自动化程度 | 自动化工具；用户输入 timed model |
| LLM / agent 角色 | 无 |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

不满足本文 baseline：强 repair engine，但没有 NL 与 NL->STM_0；可作为 formal diagnostics-to-repair 上界参照。

## 4. 证据位置

paper_content.txt:9-16, 19-31, 72-85, 173-198, 284-388；GitHub 见 paper_content.txt:447

## 5. 主要风险与使用边界

工具论文篇幅短，主要复述/扩展 2019 TarTar；目标是 timed automata，不是本文 STM repair baseline。
