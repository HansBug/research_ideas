# #85 相关工作与基线初筛指南

## 1. 目标与边界

目标：从 issue #95 的 438 行 CCF-A/B 综述候选与定向直接近邻安全检索中，形成 #85 的 D1--D7 初筛矩阵、人工下载队列和声明风险控制底座。

非目标：不写最终相关工作，不提交 PDF/全文，不把仅元数据判断升级成已核验事实。

## 2. D1--D7 字段合同

| 维度 | 中文名 | 作用 |
|---|---|---|
| D1 | 控制系统领域贴近度 | 是否同属控制、CPS、嵌入式、安全关键、自动化等领域 |
| D2 | 行为模型与状态机贴近度 | 是否涉及 STM、statechart、automata、行为模型、MBSE、MDE |
| D3 | 语料、基准与景观研究贴近度 | 是否支持语料、基准来源、景观、系统映射叙事 |
| D4 | 大模型辅助建模贴近度 | 是否涉及 LLM、生成式 AI 或 AI 辅助建模 |
| D5 | 系统综述与系统映射方法严谨性 | 是否可作 CCF-A/B 系统综述 / 系统映射写作门槛参照 |
| D6 | 制品、可复现性与获取价值 | 是否有公开 PDF、数据、代码、附录、主研究清单或 DOI 落地页 |
| D7 | 对 #85 证据门支撑度 | 是否影响 #85 研究缺口、新颖性、G3/G6/G7/G10 |

Emoji 口径：`🟢` 核心强相关，`🟡` 高度近邻，`🟠` 值得关注，`🔴` 低相关 / 排除。

## 3. 自动全文暂缓复查门禁

自动全文轻量复查标记为 `yes` 的行不能最终排除，直到完成轻量方法节复查。复查至少记录是否出现状态机（`state machine`）、行为模型（`behavioral model`）、基准（`benchmark`）、语料（`corpus`）、LLM4Modeling 等关键词，以及保持“暂缓 / 暂不下载（`Skip`）”、升级为 P1/P0，或转入“已核验近邻（`verified_near_neighbor`）”的原因。

## 4. 审查门禁

C/I 级问题包括：P0/P1 BibTeX 不完整、438 行审计缺失、7 条自动全文门禁未复查就最终排除、仅元数据判断被写成已核验声明、遗漏明显直接近邻。纯格式问题为 M。


## 5. 438 行审计与 69 行矩阵的字段边界

`screening_audit.csv` 覆盖 #95 的 438 行候选；未进入 69 行矩阵的候选只要求保留 `screening_decision`、`screening_reason`、题名、年份、venue、DOI 和下载审计摘要。进入 69 行矩阵的候选必须完整填写 D1--D7 的 `score / evidence_level / evidence_locator / rationale / pending_verification`，并保留 `relation_derivation_rule / supports_gate / D7_claim_element / difference_from_85`。

`targeted_search_audit.csv` 当前是 Stage 1b 起点审计：它记录命中、零命中与访问受限入口，但不关闭后续 G3 全面 direct-competitor safety search。
