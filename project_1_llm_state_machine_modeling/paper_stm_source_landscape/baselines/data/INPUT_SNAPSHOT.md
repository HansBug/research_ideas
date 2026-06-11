# #85 baseline screening input snapshot

核验时间：`2026-06-11 19:06:00`。本文件冻结 #95 / #85 planning 输入快照；若 raw URL 后续漂移，必须新增快照而不是静默覆盖。

| 文件 | 行数 | SHA256 | 来源 |
|---|---:|---|---|
| `issue95_ccf_ab_review_candidates_2023_2026.csv` | 438 / lines 439 | `d91229d843314a033a8ae74bec36a4a983b8ffed61a9be25758e24bb1a5345b6` | [source](https://gist.githubusercontent.com/HansBug/2310896ff4921f3d4809001571228820/raw/issue95_ccf_ab_review_candidates_2023_2026.csv) |
| `issue95_fulltext_structure_analysis_87papers.csv` | 87 / lines 88 | `2bbc0bd6bc0a6068c4482c6ff0e5858223f9c0f78e1af29aecd6e8d1e403c2c1` | [source](https://gist.githubusercontent.com/HansBug/2310896ff4921f3d4809001571228820/raw/issue95_fulltext_structure_analysis_87papers.csv) |
| `issue95_fulltext_download_audit_438papers.csv` | 438 / lines 439 | `31965751e000e42be71561d464f76d6144f9f00b646a5ab00de50c9b48c78644` | [source](https://gist.githubusercontent.com/HansBug/2310896ff4921f3d4809001571228820/raw/issue95_fulltext_download_audit_438papers.csv) |
| `issue85_narrowed_related_candidates_preliminary.csv` | 69 / lines 70 | `73a1d584c76241c320785312658a479535a08df6a6493bcc5180b05f8f35e697` | [source](https://gist.github.com/HansBug/57dd103e27205a25b97e816a4167fa1d) |
| `issue85_manual_download_needed_preliminary.bib` | n/a / lines 249 | `11c867b07985069f1ed0aefd025739c4f5b133d3512e57eb74af53f9ee4d63ce` | [source](https://gist.github.com/HansBug/57dd103e27205a25b97e816a4167fa1d) |

## Drift policy

1. `issue95_*` CSV raw URL 视为可变输入；正式 manuscript 前必须重新下载并比对 SHA256。
2. 若 SHA256 变化，保留旧快照记录并生成新版 `screening_audit.csv`；不得把新旧统计混写。
3. #95 元数据、CCF、DOI、PDF 状态默认只是 `source_claim`；进入论文正文前必须按 DOI landing page、publisher、DBLP 或人工全文核验升级。

## Header snapshot

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
prelim_row_id, source_row_index, discovery_source, include_reason, ccf_rank_source_claim, venue_source_claim, year_source_claim, title, authors_metadata, doi, doi_url, landing_page_url, fulltext_status_issue95, audit_download_status_raw, audit_discovered_pdf_url_count, audit_download_error_or_source, D1_score, D2_score, D3_score, D4_score, D5_score, D6_score, D7_score, preliminary_relation_level, verification_status, manual_priority, manual_download_decision, manual_decision_reason, preliminary_rationale, note, D1_preliminary_rationale, D2_preliminary_rationale, D3_preliminary_rationale, D4_preliminary_rationale, D5_preliminary_rationale, D6_preliminary_rationale, D7_preliminary_rationale, auto_fulltext_light_review_flag, auto_fulltext_light_review_reason
```

### `issue85_manual_download_needed_preliminary.bib`

```text

```
