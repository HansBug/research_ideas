# #85 Related Work / Baseline Screening Guide

## 1. 目标与边界

目标：从 issue #95 的 438 行 CCF-A/B 综述候选与 targeted direct-competitor safety search 中，形成 #85 的 D1--D7 初筛矩阵、人工下载队列和 claim 风险控制底座。

非目标：不写最终 Related Work，不提交 PDF/全文，不把 metadata-only 判断升级成 verified facts。

## 2. D1--D7 字段合同

| 维度 | 中文名 | 作用 |
|---|---|---|
| D1 | 控制系统领域贴近度 | 是否同属控制/CPS/嵌入式/安全关键/自动化等领域 |
| D2 | 行为模型与状态机贴近度 | 是否涉及 STM/statechart/automata/behavioral model/MBSE/MDE |
| D3 | 语料、基准与景观研究贴近度 | 是否支持 corpus / benchmark-source / landscape / SMS 叙事 |
| D4 | 大模型辅助建模贴近度 | 是否涉及 LLM / generative AI / AI-assisted modeling |
| D5 | 系统综述与系统映射方法严谨性 | 是否可作 CCF-A/B SLR/SMS 写作门槛参照 |
| D6 | 制品、可复现性与获取价值 | 是否有公开 PDF/数据/代码/附录/primary-study list 或 DOI landing page |
| D7 | 对 #85 证据门支撑度 | 是否影响 #85 gap、novelty、G3/G6/G7/G10 |

Emoji 口径：`🟢` 核心强相关，`🟡` 高度近邻，`🟠` 值得关注，`🔴` 低相关 / 排除。

## 3. Auto-fulltext Skip gate

`auto_fulltext_light_review_flag=yes` 的行不能最终排除，直到完成轻量方法节复查。复查至少记录是否出现 state machine / behavioral model / benchmark / corpus / LLM4Modeling 关键词，以及保持 Skip、升级 P1/P0 或转入 `verified_near_neighbor` 的原因。

## 4. Review gate

C/I 级问题包括：P0/P1 BibTeX 不完整、438 行审计缺失、7 条 auto-fulltext gate 未复查就最终排除、metadata-only 被写成 verified claim、遗漏明显 direct competitor。纯格式问题为 M。
