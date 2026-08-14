# #85 基线初筛输入快照

核验时间：`2026-06-11 19:06:00`。本文件冻结 #95 / #85 规划输入快照；若原始 URL 后续漂移，必须新增快照而不是静默覆盖。

| 文件 | 行数 | SHA256 | 来源 |
|---|---:|---|---|
| `issue95_ccf_ab_review_candidates_2023_2026.csv` | 438 / lines 439 | `d91229d843314a033a8ae74bec36a4a983b8ffed61a9be25758e24bb1a5345b6` | [来源](https://gist.githubusercontent.com/HansBug/2310896ff4921f3d4809001571228820/raw/issue95_ccf_ab_review_candidates_2023_2026.csv) |
| `issue95_fulltext_structure_analysis_87papers.csv` | 87 / lines 88 | `2bbc0bd6bc0a6068c4482c6ff0e5858223f9c0f78e1af29aecd6e8d1e403c2c1` | [来源](https://gist.githubusercontent.com/HansBug/2310896ff4921f3d4809001571228820/raw/issue95_fulltext_structure_analysis_87papers.csv) |
| `issue95_fulltext_download_audit_438papers.csv` | 438 / lines 439 | `31965751e000e42be71561d464f76d6144f9f00b646a5ab00de50c9b48c78644` | [来源](https://gist.githubusercontent.com/HansBug/2310896ff4921f3d4809001571228820/raw/issue95_fulltext_download_audit_438papers.csv) |
| `issue85_narrowed_related_candidates_preliminary.csv` | 69 / lines 70 | `73a1d584c76241c320785312658a479535a08df6a6493bcc5180b05f8f35e697` | [来源](https://gist.github.com/HansBug/57dd103e27205a25b97e816a4167fa1d) |
| `issue85_manual_download_needed_preliminary.bib` | n/a / lines 249 | `11c867b07985069f1ed0aefd025739c4f5b133d3512e57eb74af53f9ee4d63ce` | [来源](https://gist.github.com/HansBug/57dd103e27205a25b97e816a4167fa1d) |

## 本 PR 派生文件快照

以下快照对应当前仓库内已硬化后的派生文件；它们可能不同于计划阶段 Gist 的原始 hash。

| 文件 | 本地行数 | 本地 SHA256 | 说明 |
|---|---:|---|---|
| `issue85_narrowed_related_candidates_preliminary.csv` | 70 | `88f30ab896c2b2d6702e15fa246ea469b863c10d6c8e8316f6ae9a78bba39173` | 本 PR 派生 / 硬化后的机器审计文件 |
| `screening_audit.csv` | 439 | `0c615f561ebb07d95a6e593752777ad68d826a4cbaa7e5cda8fc06e3a643b18b` | 本 PR 派生 / 硬化后的机器审计文件 |
| `targeted_search_audit.csv` | 20 | `ffa6f35e093a5b653e7c59045b58ada631d018e47773fe6b74f7830ac534c844` | 本 PR 派生 / 硬化后的机器审计文件 |
| `auto_fulltext_light_review_gate.csv` | 22 | `ef9e961b19b95984323f8b151292339fd50ea912b9351ee0b31b74da14684f59` | 本 PR 派生 / 硬化后的机器审计文件 |
| `manual_download_needed.bib` | 249 | `11c867b07985069f1ed0aefd025739c4f5b133d3512e57eb74af53f9ee4d63ce` | 本 PR 派生 / 硬化后的机器审计文件 |
| `survey_baseline_library/data/fulltext_review_matrix.csv` | 26 | `1a1145bac13396c177430b5d88ee73c295832afff6bb45ee7079dd4758f47e3e` | P0/P1 全文级 baseline 主矩阵 |
| `survey_baseline_library/data/local_fulltext_receipt.csv` | 26 | `e23f1c666c1045fcacc74647c8a486d75074af5de8499ad70c13b424b74f4107` | P0/P1 单篇四件套 receipt |

## 漂移处理策略

1. `issue95_*` CSV 原始 URL 视为可变输入；正式成稿前必须重新下载并比对 SHA256。
2. 若 SHA256 变化，保留旧快照记录并生成新版 `screening_audit.csv`；不得把新旧统计混写。
3. #95 元数据、CCF、DOI、PDF 状态默认只是 `source_claim`；进入论文正文前必须按 DOI 落地页、出版社页面、DBLP 或人工全文核验升级。

## 表头快照

以下代码块保留原始 CSV 字段名，便于机器复验；这些字段名是输入文件的机器字段，不翻译为中文，中文字段释义以 [../GUIDE.md](../GUIDE.md) 与本目录其他说明文件为准。

### `issue95_ccf_ab_review_candidates_2023_2026.csv`

```text
source_comment, appendix_url, year_issue_table, ccf_rank, ccf_emoji, journal_issue_table, auto_type_issue_table, title_issue_table, title_en, title_zh_machine, abstract_en_metadata, abstract_zh_machine, brief_note_zh_machine, rqs_en_metadata_or_status, rqs_zh_machine_or_status, rq_extraction_status, authors_metadata, journal_metadata, publication_year_metadata, publication_date_metadata, doi, doi_url, landing_page_url, openalex_url, crossref_url, oa_status_openalex, oa_pdf_url_openalex, ref_count_metadata, fulltext_status_issue_table, metadata_sources, important_notes
```

### `issue95_fulltext_structure_analysis_87papers.csv`

```text
doi, title, ccf, journal, year, pdf_source, pages, chars, rq_count_detected, rq_snippets, section_count_detected, sections, has_method_or_methodology, has_protocol, has_search, has_inclusion_exclusion, has_prisma_or_flow, has_quality_assessment, has_irr_or_agreement, has_threats_or_limitations, has_artifact_or_data_availability
```

### `issue95_fulltext_download_audit_438papers.csv`

```text
doi, title, ccf_rank, journal, year_issue_table, publication_year_metadata, oa_status_openalex, discovered_pdf_url_count, discovered_pdf_urls, download_attempt, download_status, download_error_or_source, pdf_local_path, pdf_bytes, pdf_sha256, text_local_path, text_bytes, text_sha256, structure_analysis_status, structure_pages, structure_rq_count_detected
```

### `issue85_narrowed_related_candidates_preliminary.csv`

```text
prelim_row_id, source_row_index, row_id, doi_value, doi_source, doi_verification_status, venue_value, venue_source, venue_verification_status, ccf_rank_value, ccf_source, ccf_verification_status, url, public_pdf_url_state, auto_fulltext_state, download_failure_reason, pdf_url, pdf_url_source, pdf_access_status, pdf_status_source, discovery_source, include_reason, ccf_rank_source_claim, venue_source_claim, year_source_claim, title, authors_metadata, doi, doi_url, landing_page_url, fulltext_status_issue95, audit_download_status_raw, audit_discovered_pdf_url_count, audit_download_error_or_source, D1_score, D2_score, D3_score, D4_score, D5_score, D6_score, D7_score, preliminary_relation_level, relation_derivation_rule, supports_gate, D7_claim_element, D7_challenge_or_support, novelty_action, difference_from_85, verification_status, manual_priority, manual_download_decision, manual_decision_reason, preliminary_rationale, note, D1_evidence_level, D1_evidence_locator, D1_rationale, D1_pending_verification, D1_preliminary_rationale, D2_evidence_level, D2_evidence_locator, D2_rationale, D2_pending_verification, D2_preliminary_rationale, D3_evidence_level, D3_evidence_locator, D3_rationale, D3_pending_verification, D3_preliminary_rationale, D4_evidence_level, D4_evidence_locator, D4_rationale, D4_pending_verification, D4_preliminary_rationale, D5_evidence_level, D5_evidence_locator, D5_rationale, D5_pending_verification, D5_preliminary_rationale, D6_evidence_level, D6_evidence_locator, D6_rationale, D6_pending_verification, D6_preliminary_rationale, D7_evidence_level, D7_evidence_locator, D7_rationale, D7_pending_verification, D7_preliminary_rationale, auto_fulltext_light_review_flag, auto_fulltext_light_review_reason
```


### `screening_audit.csv`

```text
source_row_index, row_id, discovery_source, doi_value, doi_source, doi_verification_status, venue_value, venue_source, venue_verification_status, ccf_rank_value, ccf_source, ccf_verification_status, url, audit_download_status_raw, public_pdf_url_state, auto_fulltext_state, download_failure_reason, pdf_url, pdf_url_source, pdf_access_status, pdf_status_source, manual_decision_reason, screening_decision, screening_reason, prelim_row_id, manual_priority, manual_download_decision, preliminary_relation_level, relation_derivation_rule, supports_gate, D7_claim_element, D7_challenge_or_support, novelty_action, difference_from_85, verification_status, auto_fulltext_light_review_flag, title, year, venue, ccf_rank, doi, landing_page_url, fulltext_audit_status, discovered_pdf_url_count, D1_score, D2_score, D3_score, D4_score, D5_score, D6_score, D7_score, D1_evidence_level, D1_evidence_locator, D1_rationale, D1_pending_verification, D1_preliminary_rationale, D2_evidence_level, D2_evidence_locator, D2_rationale, D2_pending_verification, D2_preliminary_rationale, D3_evidence_level, D3_evidence_locator, D3_rationale, D3_pending_verification, D3_preliminary_rationale, D4_evidence_level, D4_evidence_locator, D4_rationale, D4_pending_verification, D4_preliminary_rationale, D5_evidence_level, D5_evidence_locator, D5_rationale, D5_pending_verification, D5_preliminary_rationale, D6_evidence_level, D6_evidence_locator, D6_rationale, D6_pending_verification, D6_preliminary_rationale, D7_evidence_level, D7_evidence_locator, D7_rationale, D7_pending_verification, D7_preliminary_rationale
```

### `issue85_manual_download_needed_preliminary.bib`

```text
BibTeX 无表头；按 entry 数量、DOI 字段与 SHA256 复验。
```
