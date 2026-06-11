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

### 2.1 字段级 provenance 与下载拆分字段

进入 69 行矩阵的候选必须保留字段级来源与核验状态：`doi_value / doi_source / doi_verification_status`、`venue_value / venue_source / venue_verification_status`、`ccf_rank_value / ccf_source / ccf_verification_status` 与 `url`。来自 #95 的 DOI、venue、CCF 和 PDF 状态默认只是 `source_claim_unverified`，不能写成已核验事实。

下载字段必须拆分为事实字段与人工决策字段：`public_pdf_url_state / auto_fulltext_state / download_failure_reason / pdf_url / pdf_url_source / pdf_access_status / pdf_status_source / manual_download_decision / manual_priority / manual_decision_reason`。后续人工下载后，只能通过这些字段升级状态，不得把 PDF 或全文提交到仓库。

D1 的 `human-in-the-loop` 只在同时出现 CPS、控制、嵌入式、安全关键、自动驾驶、机器人、工业自动化等领域上下文时才可作为控制系统强证据；如果只是泛 SE / LLM workflow / 治理策略，应降为 `🟠` 或更低，并在 rationale 中说明不能支撑控制系统领域贴近度。

## 3. 自动全文暂缓复查门禁

自动全文轻量复查标记为 `yes` 的行不能最终排除，直到完成轻量方法节复查。复查至少记录是否出现状态机（`state machine`）、行为模型（`behavioral model`）、基准（`benchmark`）、语料（`corpus`）、LLM4Modeling 等关键词，以及保持“暂缓 / 暂不下载（`Skip`）”、升级为 P1/P0，或转入“已核验近邻（`verified_near_neighbor`）”的原因。

升级时必须同步更新 `issue85_narrowed_related_candidates_preliminary.csv` 的 `manual_priority / manual_download_decision / verification_status`、`screening_audit.csv` 对应行、`SUMMARY.md` 的统计与门禁条目数；不得只在 `auto_fulltext_light_review_gate.csv` 单点修改导致跨文件统计漂移。

## 4. 审查门禁

C/I 级问题包括：P0/P1 BibTeX 不完整、438 行审计缺失、7 条自动全文门禁未复查就最终排除、仅元数据判断被写成已核验声明、遗漏明显直接近邻。纯格式问题为 M。


## 5. 438 行审计与 69 行矩阵的字段边界

`screening_audit.csv` 覆盖 #95 的 438 行候选；未进入 69 行矩阵的候选只要求保留 `screening_decision`、`screening_reason`、题名、年份、venue、DOI 和下载审计摘要。进入 69 行矩阵的候选必须完整填写 D1--D7 的 `score / evidence_level / evidence_locator / rationale / pending_verification`，并保留 `relation_derivation_rule / supports_gate / D7_claim_element / difference_from_85`。

`targeted_search_audit.csv` 当前是 Stage 1b 起点审计：它记录命中、零命中与访问受限入口，但不关闭后续 G3 全面 direct-competitor safety search。


## 6. 人工下载 request ledger

[MANUAL_DOWNLOAD_REQUESTS.md](./MANUAL_DOWNLOAD_REQUESTS.md) 是 P0/P1 人工协作 receipt 真源。每行必须至少记录 `request_id / priority / title / DOI / publisher_or_landing_url / public_pdf_candidate_url / access_route / why_needed / blocking_gate_or_claim / needed_for_gate / requested_action / after_download_action / request_status / user_response / manual_check_status / final_verification_status / copyright_note / do_not_commit_pdf_or_fulltext`。

若用户后续确认可访问或不可访问，只能更新 receipt 字段和矩阵中的核验状态；不得提交用户下载的 PDF、出版社全文、长摘录或 OCR 全文。
