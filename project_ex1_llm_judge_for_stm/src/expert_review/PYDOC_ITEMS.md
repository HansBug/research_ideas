# `expert_review/` 全部待写 docstring 清单（per-file checklist）

> **生成时间**: 2026-05-09 14:50:00（AST 自动扫描）
> **配套文件**: [PYDOC_INVENTORY.md](./PYDOC_INVENTORY.md) — 高层盘点 + 死代码 + Phase 计划
> **使用方式**: 用户逐项过；写完一项把 `[ ]` 改 `[x]`；处理完一个文件后在文件标题加 ✅

**Legend**：
- 状态符号：`✗` 缺 docstring  /  `🇺🇸` 已有英文（待中文化）  /  `🇨🇳` 已有中文 ✓
- 类型缩写：`Cls` = class  /  `Fn ` = func（顶层）  /  `Mth` = method（class 内）
- L = 行号

---

## Phase 1 — 核心 schema + 入口

### `__init__.py`  module:✗
（仅加 module docstring，包入口）

### `__main__.py`  module:✗

- [ ] ✗ `Fn ` `main` (L9)

### `agent.py`  module:✗

- [ ] ✗ `Cls` `ExpertReviewAgent` (L19)
- [ ] ✗ `Mth` `ExpertReviewAgent.__init__` (L20)
- [ ] ✗ `Mth` `ExpertReviewAgent._build_llm` (L37)
- [ ] ✗ `Mth` `ExpertReviewAgent.review` (L58)

### `schema.py`  module:✗

- [ ] ✗ `Cls` `DimensionDefinition` (L11)
- [ ] ✗ `Cls` `EvidenceItem` (L23)
- [ ] ✗ `Cls` `TraceLink` (L31)
- [ ] ✗ `Cls` `RequirementTraceResult` (L39)
- [ ] ✗ `Cls` `ElementIssue` (L49)
- [ ] ✗ `Cls` `DimensionReviewResult` (L58)
- [ ] ✗ `Cls` `ExpertReviewRequest` (L72)
- [ ] ✗ `Cls` `ExpertReviewResult` (L81)
- [ ] ✗ `Fn ` `judgement_from_score` (L98)
- [ ] ✗ `Fn ` `to_dict` (L110)
- [ ] ✗ `Fn ` `to_json` (L114)
- [ ] ✗ `Fn ` `evidence_item_from_dict` (L118)
- [ ] ✗ `Fn ` `trace_link_from_dict` (L127)
- [ ] ✗ `Fn ` `element_issue_from_dict` (L136)
- [ ] ✗ `Fn ` `requirement_trace_from_dict` (L146)
- [ ] ✗ `Fn ` `dimension_review_from_dict` (L157)
- [ ] ✗ `Fn ` `result_to_flat_row` (L172)

### `schemas/__init__.py`  module:✗
（仅加 module docstring）

### `schemas/request.py`  module:✗
（仅加 module docstring）

### `schemas/result.py`  module:✗
（仅加 module docstring）

### `schemas/dossiers.py`  module:✗

- [ ] ✗ `Cls` `ReviewContract` (L9)
- [ ] ✗ `Cls` `EvidenceRegime` (L20)
- [ ] ✗ `Cls` `ArtifactElement` (L31)
- [ ] ✗ `Cls` `ArtifactRelation` (L40)
- [ ] ✗ `Cls` `ArtifactDossier` (L53)
- [ ] ✗ `Cls` `InputDossier` (L76)

### `schemas/graph_state.py`  module:✗

- [ ] ✗ `Cls` `ReviewGraphState` (L12)

---

## Phase 2 — graph/ pipeline 编排

### `graph/__init__.py`  module:✗
（仅加 module docstring）

### `graph/edges.py`  module:✗
（仅加 module docstring，含 PREPARATION/ANALYSIS/FINAL stage 元组的设计说明）

### `graph/subgraphs.py`  module:✗

- [ ] ✗ `Fn ` `ordered_stage_groups` (L4)

### `graph/nodes.py`  module:✗

- [ ] ✗ `Fn ` `run_contract_router_node` (L31)
- [ ] ✗ `Fn ` `run_input_analyst_node` (L39)
- [ ] ✗ `Fn ` `run_prediction_extractor_node` (L43)
- [ ] ✗ `Fn ` `run_reference_extractor_node` (L51)
- [ ] ✗ `Fn ` `run_evidence_regime_node` (L59)
- [ ] ✗ `Fn ` `run_review_policy_builder_node` (L68)
- [ ] ✗ `Fn ` `run_traceability_node` (L91)
- [ ] ✗ `Fn ` `run_equivalence_node` (L106)
- [ ] ✗ `Fn ` `run_quality_node` (L124)
- [ ] ✗ `Fn ` `run_missing_evidence_node` (L144)
- [ ] ✗ `Fn ` `run_score_composer_node` (L190)
- [ ] ✗ `Fn ` `run_final_synthesizer_node` (L223)

### `graph/runtime.py`  module:✗

- [ ] ✗ `Fn ` `_default_equivalence_report` (L29)
- [ ] ✗ `Fn ` `_append_runtime_notes` (L49)
- [ ] ✗ `Fn ` `run_expert_review_workflow` (L87)

---

## Phase 3 — agents/

### `agents/__init__.py`  module:✗
（包入口）

### `agents/common.py`  module:✗

- [ ] ✗ `Fn ` `clip01` (L58)
- [ ] ✗ `Fn ` `tokenize` (L62)
- [ ] ✗ `Fn ` `content_tokens` (L68)
- [ ] ✗ `Fn ` `_stem` (L79)
- [ ] ✗ `Fn ` `token_set` (L88)
- [ ] ✗ `Fn ` `stem_set` (L92)
- [ ] ✗ `Fn ` `overlap_score` (L102)
- [ ] ✗ `Fn ` `stem_overlap_score` (L110)
- [ ] ✗ `Fn ` `combined_overlap_score` (L118)
- [ ] ✗ `Fn ` `dedupe_strings` (L124)
- [ ] ✗ `Fn ` `make_evidence_item` (L137)
- [ ] ✗ `Fn ` `candidate_texts_from_dossier` (L146)
- [ ] ✗ `Fn ` `requirement_grounding_tokens` (L175)
- [ ] ✗ `Fn ` `relation_signature_tokens` (L188)
- [ ] ✗ `Fn ` `find_best_relation_overlap` (L203)
- [ ] ✗ `Fn ` `is_grounded_to_input` (L217)
- [ ] ✗ `Fn ` `major_element_name_set` (L224)
- [ ] ✗ `Fn ` `initial_targets_from_behaviors` (L231)
- [ ] ✗ `Fn ` `shared_source_target_map` (L240)
- [ ] ✗ `Fn ` `infer_count_hint` (L251)

### `agents/contract_router.py`  module:✗

- [ ] ✗ `Fn ` `default_contract` (L76)
- [ ] ✗ `Fn ` `route_contract` (L103)

### `agents/input_analyst.py`  module:✗

- [ ] ✗ `Fn ` `_make_evidence_item` (L13)
- [ ] ✗ `Fn ` `_dedupe_strings` (L73)
- [ ] ✗ `Fn ` `build_input_dossier` (L86)

### `agents/prediction_extractor.py`  module:✗

- [ ] ✗ `Fn ` `extract_prediction_dossier` (L9)

### `agents/reference_extractor.py`  module:✗

- [ ] ✗ `Fn ` `extract_reference_dossier` (L9)

### `agents/evidence_regime_estimator.py`  module:✗

- [ ] ✗ `Fn ` `_metadata_surface` (L44)
- [ ] ✗ `Fn ` `estimate_evidence_regime` (L50)

### `agents/review_policy_builder.py`  module:✗

- [ ] ✗ `Fn ` `_clone_dimension` (L17)
- [ ] ✗ `Fn ` `build_dimensions` (L36)
- [ ] ✗ `Fn ` `build_review_policy_packet` (L78)

### `agents/traceability.py`  module:✗

- [ ] ✗ `Fn ` `_requirement_profile` (L22)
- [ ] ✗ `Fn ` `_structural_requirement_support` (L35)
- [ ] ✗ `Fn ` `deterministic_traceability` (L75)
- [ ] ✗ `Fn ` `traceability_with_llm` (L151)

### `agents/equivalence.py`  module:✗

- [ ] ✗ `Fn ` `_extra_issue_from_element` (L26)
- [ ] ✗ `Fn ` `_extra_issue_from_relation` (L36)
- [ ] ✗ `Fn ` `_synthetic_issue` (L46)
- [ ] ✗ `Fn ` `_detect_guard_polarity_conflict` (L56)
- [ ] ✗ `Fn ` `_detect_action_effect_conflict` (L76)
- [ ] ✗ `Fn ` `_major_relation_labels` (L84)
- [ ] ✗ `Fn ` `_parallel_structure_diagnostics` (L98)
- [ ] ✗ `Fn ` `deterministic_equivalence` (L136)
- [ ] ✗ `Fn ` `_json_safe_report` (L347)
- [ ] ✗ `Fn ` `equivalence_with_llm` (L376)

### `agents/pragmatic_quality.py`  module:✗

- [ ] ✗ `Fn ` `_issue` (L46)
- [ ] ✗ `Fn ` `_generic_name_count` (L57)
- [ ] ✗ `Fn ` `deterministic_pragmatic_quality` (L66)
- [ ] ✗ `Fn ` `pragmatic_quality_with_llm` (L228)

### `agents/missing_evidence_critic.py`  module:✗

- [ ] ✗ `Fn ` `_dedup_str_list` (L13)
- [ ] ✗ `Fn ` `deterministic_missing_evidence_critic` (L25)
- [ ] ✗ `Fn ` `missing_evidence_with_llm` (L110)

### `agents/orchestrator.py`  module:✗

- [ ] ✗ `Fn ` `record_agent_context` (L29)
- [ ] ✗ `Fn ` `record_fanout` (L42)
- [ ] ✗ `Fn ` `run_parallel` (L46)

### `agents/rubric_scorer.py`  module:🇺🇸

- [ ] 🇺🇸 `Fn ` `_get_sanity_bound` (L63)
- [ ] ✗ `Cls` `RubricScore` (L76)
- [ ] ✗ `Fn ` `_truncate` (L91)
- [ ] ✗ `Fn ` `_band_from_score` (L98)
- [ ] 🇺🇸 `Fn ` `llm_rubric_score` (L110)

### `agents/score_composer.py`  module:✗

- [ ] ✗ `Fn ` `_missing_signal_count` (L12)
- [ ] ✗ `Fn ` `_safe_int` (L22)
- [ ] ✗ `Fn ` `_f1_from_tp_fp_fn` (L29)
- [ ] ✗ `Fn ` `_normalized_locator_token` (L35)
- [ ] ✗ `Fn ` `_requirement_locator` (L40)
- [ ] ✗ `Fn ` `_prediction_locator` (L44)
- [ ] ✗ `Fn ` `_trace_dimension_evidence` (L48)
- [ ] ✗ `Fn ` `compose_scores` (L94)
- [ ] ✗ `Fn ` `final_confidence` (L814)

### `agents/final_synthesizer.py`  module:✗

- [ ] ✗ `Fn ` `_dimension_score_map` (L14)
- [ ] ✗ `Fn ` `coarse_overall_judgement` (L18)
- [ ] ✗ `Fn ` `overall_reason` (L53)
- [ ] ✗ `Fn ` `maybe_refine_overall_reason` (L133)
- [ ] ✗ `Fn ` `synthesize_result` (L166)

### `agents/llm_helpers.py`  module:✗

- [ ] ✗ `Fn ` `content_to_text` (L12)
- [ ] ✗ `Fn ` `_invoke_transport` (L27)
- [ ] ✗ `Fn ` `invoke_llm_text` (L84)
- [ ] ✗ `Fn ` `invoke_llm_json` (L127)

---

## Phase 4 — prompts/

### `prompts/__init__.py`  module:✗
（包入口）

### `prompts/contract_router.py`  module:✗
（仅加 module docstring，prompt 字符串说明）

### `prompts/extraction.py`  module:✗
（同上）

### `prompts/equivalence.py`  module:✗
（同上）

### `prompts/missing_evidence.py`  module:✗
（同上）

### `prompts/quality_review.py`  module:✗
（同上）

### `prompts/review_policy.py`  module:✗
（同上）

### `prompts/synthesis.py`  module:✗
（同上）

### `prompts/traceability.py`  module:✗
（同上）

### `prompts/rubric_dim_score.py`  module:🇺🇸

- [ ] ✗ `Fn ` `_format_rubric_table` (L253)
- [ ] ✗ `Fn ` `_format_anchors` (L257)
- [ ] ✗ `Fn ` `_format_pitfalls` (L261)
- [ ] 🇺🇸 `Fn ` `build_rubric_prompt` (L285)

---

## Phase 5 — tools/

### `tools/__init__.py`  module:✗
（包入口）

### `tools/policy_library.py`  module:✗

- [ ] ✗ `Fn ` `_metadata_value` (L261)
- [ ] ✗ `Fn ` `_metadata_int` (L267)
- [ ] ✗ `Fn ` `_joined_text` (L276)
- [ ] ✗ `Fn ` `_canonical_summary_target` (L280)
- [ ] ✗ `Fn ` `_canonical_diagram_type` (L303)
- [ ] ✗ `Fn ` `_summary_target_from_metadata` (L333)
- [ ] ✗ `Fn ` `_summary_target_axis_from_metadata` (L341)
- [ ] ✗ `Fn ` `_artifact_semantics_from_metadata` (L350)
- [ ] ✗ `Fn ` `_component_profile_from_metadata` (L358)
- [ ] ✗ `Fn ` `infer_summary_row_type` (L383)
- [ ] ✗ `Fn ` `infer_summary_target` (L405)
- [ ] ✗ `Fn ` `infer_record_diagram_type` (L418)
- [ ] ✗ `Fn ` `infer_summary_target_axis` (L431)
- [ ] ✗ `Fn ` `_summary_semantic_profile` (L444)
- [ ] ✗ `Fn ` `_record_semantic_profile` (L487)
- [ ] ✗ `Fn ` `infer_aggregate_signal` (L518)
- [ ] ✗ `Fn ` `_aggregate_signal_from_row_type` (L523)
- [ ] ✗ `Fn ` `detect_vv_roles` (L535)
- [ ] ✗ `Fn ` `build_review_policy` (L545)

### `tools/structured_extract.py`  module:✗

- [ ] ✗ `Fn ` `render_artifact_schema_hint` (L16)
- [ ] ✗ `Fn ` `should_use_llm_extractor` (L50)
- [ ] ✗ `Fn ` `extract_artifact_dossier` (L62)

### `tools/artifact_io.py`  module:✗

- [ ] ✗ `Fn ` `content_to_text` (L4)
- [ ] ✗ `Fn ` `artifact_excerpt` (L19)

### `tools/artifact_probe.py`  module:✗

- [ ] ✗ `Fn ` `_make_evidence_item` (L16)
- [ ] ✗ `Fn ` `_element_from_raw` (L25)
- [ ] ✗ `Fn ` `_relation_from_raw` (L46)
- [ ] ✗ `Fn ` `_element_merge_key` (L70)
- [ ] ✗ `Fn ` `_relation_merge_key` (L74)
- [ ] ✗ `Fn ` `_same_relation_family` (L90)
- [ ] ✗ `Fn ` `merge_text_fragments` (L104)
- [ ] ✗ `Fn ` `build_parser_dossier` (L118)

### `tools/dossier_merge.py`  module:✗

- [ ] ✗ `Fn ` `_make_evidence_item` (L12)
- [ ] ✗ `Fn ` `_element_merge_key` (L21)
- [ ] ✗ `Fn ` `_relation_merge_key` (L25)
- [ ] ✗ `Fn ` `merge_artifact_dossiers` (L40)

### `tools/known_format_lift.py`  module:✗

- [ ] ✗ `Fn ` `dedupe_strings` (L16)
- [ ] ✗ `Fn ` `guess_format` (L29)
- [ ] ✗ `Fn ` `format_confidence` (L54)
- [ ] ✗ `Fn ` `artifact_family_guess` (L68)
- [ ] ✗ `Fn ` `parse_transition_signature` (L85)
- [ ] ✗ `Fn ` `_self_named_composite_count_from_text` (L112)
- [ ] ✗ `Fn ` `_cross_composite_transition_risk_from_text` (L127)
- [ ] ✗ `Fn ` `surface_markers_from_text` (L151)
- [ ] ✗ `Fn ` `_extract_xml_inventory` (L167)
- [ ] ✗ `Fn ` `_derive_behavior_lines` (L227)
- [ ] ✗ `Fn ` `_derive_constraint_lines` (L241)
- [ ] ✗ `Fn ` `_derive_ambiguities` (L253)
- [ ] ✗ `Fn ` `_canonical_names_from_inventory` (L263)
- [ ] ✗ `Fn ` `_explicit_state_names_from_text` (L276)
- [ ] ✗ `Fn ` `_observability_from_inventory` (L285)
- [ ] ✗ `Fn ` `_structural_warnings_from_probe` (L310)
- [ ] ✗ `Fn ` `summary_from_inventory` (L327)
- [ ] ✗ `Fn ` `inventory_from_text` (L351)

### `tools/validation.py`  module:✗

- [ ] ✗ `Fn ` `status_counts` (L8)
- [ ] ✗ `Fn ` `json_safe_report` (L15)
- [ ] ✗ `Fn ` `evidence_summary_from_dimensions` (L46)
- [ ] ✗ `Fn ` `validate_result_shape` (L72)

---

## Phase 6 — utils + 顶层

### `utils.py`  module:✗

- [ ] ✗ `Fn ` `resolve_api_env` (L68)
- [ ] ✗ `Fn ` `normalize_text` (L90)
- [ ] ✗ `Fn ` `normalize_id` (L97)
- [ ] ✗ `Fn ` `is_cjk` (L105)
- [ ] ✗ `Fn ` `unicode_word_tokens` (L116)
- [ ] ✗ `Fn ` `semantic_terms` (L132)
- [ ] ✗ `Fn ` `safe_float` (L171)
- [ ] ✗ `Fn ` `prf_from_sets` (L182)
- [ ] ✗ `Fn ` `extract_json_object` (L199)
- [ ] ✗ `Fn ` `ensure_json` (L211)
- [ ] ✗ `Fn ` `normalize_machine` (L219)
- [ ] ✗ `Fn ` `count_machine_components` (L296)

### `inventory.py`  module:✗

- [ ] ✗ `Cls` `RequirementItem` (L22)
- [ ] ✗ `Fn ` `_split_free_text_requirements` (L35)
- [ ] ✗ `Fn ` `_split_inline_explicit_requirements` (L68)
- [ ] ✗ `Fn ` `parse_requirement_items` (L83)
- [ ] ✗ `Fn ` `parse_json_payload` (L121)
- [ ] ✗ `Fn ` `extract_plain_elements` (L137)
- [ ] ✗ `Fn ` `_dedupe_keep_order` (L157)
- [ ] ✗ `Fn ` `embedded_artifact_text` (L169)
- [ ] ✗ `Fn ` `extract_generic_inventory_from_text` (L188)
- [ ] ✗ `Fn ` `merge_inventory` (L242)
- [ ] ✗ `Fn ` `machine_elements_from_payload` (L249)
- [ ] ✗ `Fn ` `extract_model_inventory` (L336)
- [ ] ✗ `Fn ` `compute_set_match` (L368)
- [ ] ✗ `Fn ` `build_requirement_trace` (L380)
- [ ] 🇺🇸 `Fn ` `parse_requirements_tool` (L417)
- [ ] 🇺🇸 `Fn ` `extract_model_inventory_tool` (L431)
- [ ] 🇺🇸 `Fn ` `compare_model_elements_tool` (L442)
- [ ] 🇺🇸 `Fn ` `build_traceability_tool` (L450)
- [ ] ✗ `Fn ` `get_review_tools` (L465)

### `llm_telemetry.py`  module:✗

- [ ] ✗ `Cls` `LLMOperationRecord` (L11)
- [ ] ✗ `Cls` `LLMUsageSummary` (L27)
- [ ] ✗ `Cls` `_MutableRunTracker` (L51)
- [ ] ✗ `Mth` `_MutableRunTracker.record` (L57)
- [ ] ✗ `Mth` `_MutableRunTracker.summarize` (L60)
- [ ] ✗ `Fn ` `_p95` (L96)
- [ ] ✗ `Fn ` `llm_run_context` (L113)
- [ ] ✗ `Fn ` `record_llm_operation` (L132)
- [ ] ✗ `Fn ` `summarize_current_llm_usage` (L168)
- [ ] ✗ `Fn ` `usage_dict_from_response` (L175)

### `semantic_router.py`  module:✗

- [ ] ✗ `Cls` `SemanticCategory` (L17)
- [ ] ✗ `Fn ` `_invoke_llm_json` (L25)
- [ ] ✗ `Fn ` `_semantic_similarity` (L35)
- [ ] ✗ `Fn ` `_category_payload` (L51)
- [ ] ✗ `Fn ` `_category_score` (L60)
- [ ] ✗ `Fn ` `_semantic_fragments` (L84)
- [ ] ✗ `Fn ` `_prepare_texts` (L109)
- [ ] ✗ `Fn ` `semantic_single_label` (L123)
- [ ] ✗ `Fn ` `semantic_multi_label` (L183)

### `fallback_llm.py`  module:🇺🇸

- [ ] 🇺🇸 `Cls` `_CooldownState` (L26)
- [ ] ✗ `Mth` `_CooldownState.is_in_cooldown` (L33)
- [ ] ✗ `Mth` `_CooldownState.mark_failure` (L37)
- [ ] ✗ `Mth` `_CooldownState.mark_success` (L48)
- [ ] 🇺🇸 `Cls` `FallbackLLMClient` (L55)
- [ ] ✗ `Mth` `FallbackLLMClient.__init__` (L59)
- [ ] 🇺🇸 `Mth` `FallbackLLMClient.primary_provider_key` (L76)
- [ ] ✗ `Mth` `FallbackLLMClient._cooldown_for` (L80)
- [ ] 🇺🇸 `Mth` `FallbackLLMClient.invoke` (L83)
- [ ] 🇺🇸 `Mth` `FallbackLLMClient.bind` (L127)
- [ ] ✗ `Mth` `FallbackLLMClient.__getattr__` (L142)
- [ ] ✗ `Mth` `FallbackLLMClient.__repr__` (L148)
- [ ] 🇺🇸 `Fn ` `build_fallback_chain` (L153)

---

## Phase 7 — benchmark + batch

### `benchmark.py`  module:✗（**最大文件**，109 个 items）

- [ ] ✗ `Cls` `BenchmarkTask` (L95)
- [ ] ✗ `Fn ` `_stable_token` (L110)
- [ ] ✗ `Fn ` `_p95` (L117)
- [ ] ✗ `Fn ` `_family_key_for_record_row` (L127)
- [ ] ✗ `Fn ` `_family_key_for_protocol_row` (L172)
- [ ] ✗ `Fn ` `_prepare_record_level_pool` (L176)
- [ ] ✗ `Fn ` `_prepare_summary_level_pool` (L188)
- [ ] ✗ `Fn ` `_safe_json_dict` (L198)
- [ ] ✗ `Fn ` `_safe_json_list` (L209)
- [ ] ✗ `Fn ` `_safe_float` (L220)
- [ ] ✗ `Fn ` `_safe_int` (L230)
- [ ] ✗ `Fn ` `_component_f1_from_counts` (L240)
- [ ] ✗ `Fn ` `_reference_solution_text_by_basename` (L249)
- [ ] ✗ `Fn ` `_hydrate_component_public_evidence` (L260)
- [ ] ✗ `Fn ` `_prepare_component_level_table` (L323)
- [ ] ✗ `Fn ` `_prepare_component_level_pool` (L334)
- [ ] ✗ `Fn ` `_prepare_protocol_level_pool` (L341)
- [ ] ✗ `Fn ` `build_benchmark_inventory` (L348)
- [ ] ✗ `Fn ` `_counts_dict` (L366)
- [ ] ✗ `Fn ` `build_component_alignment_schema` (L370)
- [ ] ✗ `Fn ` `summarize_benchmark_coverage` (L395)
- [ ] ✗ `Fn ` `_rows_to_tasks` (L466)
- [ ] ✗ `Fn ` `_family_split_assignments` (L480)
- [ ] ✗ `Fn ` `build_benchmark_split_bundle` (L528)
- [ ] ✗ `Fn ` `build_lofo_task_bundles` (L573)
- [ ] ✗ `Fn ` `_load_benchmark_tables` (L605)
- [ ] ✗ `Fn ` `_normalize_score` (L612)
- [ ] ✗ `Fn ` `_safe_text` (L626)
- [ ] ✗ `Fn ` `_truncate_artifact` (L632)
- [ ] ✗ `Fn ` `_collect_strings_from_json` (L639)
- [ ] ✗ `Fn ` `_taxonomy_from_text` (L655)
- [ ] ✗ `Fn ` `_judgement_label_index` (L680)
- [ ] ✗ `Fn ` `_weighted_kappa` (L687)
- [ ] ✗ `Fn ` `_human_issue_set_from_record` (L707)
- [ ] ✗ `Fn ` `_agent_issue_set` (L737)
- [ ] ✗ `Fn ` `_agent_critical_issue_set` (L785)
- [ ] ✗ `Fn ` `_issue_f1` (L798)
- [ ] ✗ `Fn ` `_spearman` (L814)
- [ ] ✗ `Fn ` `_pairwise_order_accuracy` (L827)
- [ ] ✗ `Fn ` `_score_align` (L848)
- [ ] ✗ `Fn ` `_equivalence_metrics` (L884)
- [ ] ✗ `Fn ` `_calibration_metrics` (L913)
- [ ] ✗ `Fn ` `_stability_metrics` (L939)
- [ ] ✗ `Fn ` `_summary_discipline_metrics` (L947)
- [ ] ✗ `Fn ` `_protocol_metrics` (L964)
- [ ] ✗ `Fn ` `_reason_alignment_metrics` (L992)
- [ ] ✗ `Fn ` `_judgement_metrics` (L1005)
- [ ] ✗ `Fn ` `_critical_issue_metrics` (L1042)
- [ ] ✗ `Fn ` `_dimension_map` (L1070)
- [ ] ✗ `Fn ` `_contradiction_metrics` (L1080)
- [ ] ✗ `Fn ` `_macro_f1_for_labels` (L1129)
- [ ] ✗ `Fn ` `_component_alignment_metrics` (L1144)
- [ ] ✗ `Fn ` `_build_record_prompt` (L1202)
- [ ] ✗ `Fn ` `_build_summary_prompt` (L1227)
- [ ] ✗ `Fn ` `_summary_row_type_from_row` (L1255)
- [ ] ✗ `Fn ` `_artifact_semantics_from_row` (L1273)
- [ ] ✗ `Fn ` `_summary_semantics_from_row` (L1283)
- [ ] ✗ `Fn ` `_build_protocol_prompt` (L1300)
- [ ] ✗ `Fn ` `_build_component_prompt` (L1309)
- [ ] ✗ `Fn ` `_build_component_pred_output` (L1330)
- [ ] ✗ `Fn ` `_build_component_input_text` (L1344)
- [ ] ✗ `Fn ` `_build_record_task` (L1356)
- [ ] ✗ `Fn ` `_build_summary_task` (L1386)
- [ ] ✗ `Fn ` `_build_protocol_task` (L1416)
- [ ] ✗ `Fn ` `_build_component_task` (L1458)
- [ ] ✗ `Fn ` `_sample_grouped` (L1499)
- [ ] ✗ `Fn ` `build_benchmark_slices` (L1523)
- [ ] ✗ `Fn ` `build_full_available_task_bundle` (L1558)
- [ ] ✗ `Fn ` `_regime_from_result` (L1572)
- [ ] ✗ `Fn ` `_dimension_score` (L1589)
- [ ] ✗ `Fn ` `_vv_role_coverage` (L1596)
- [ ] ✗ `Fn ` `_rerun_subset` (L1618)
- [ ] ✗ `Fn ` `_error_buckets_for_row` (L1649)
- [ ] ✗ `Fn ` `_build_error_map` (L1692)
- [ ] ✗ `Fn ` `_task_inventory` (L1760)
- [ ] ✗ `Fn ` `_runtime_metrics` (L1770)
- [ ] 🇺🇸 `Fn ` `_serialize_dc` (L1802)
- [ ] 🇺🇸 `Fn ` `_deserialize_dc` (L1824)
- [ ] ✗ `Fn ` `_evaluate_task_bundle` (L1843)
- [ ] ✗ `Fn ` `_safe_task_id_for_filename` (L1905)
- [ ] ✗ `Fn ` `_process_task` (L1908)
- [ ] ✗ `Fn ` `run_benchmark_iteration` (L2109)
- [ ] ✗ `Fn ` `_summarize_lofo_reports` (L2183)
- [ ] ✗ `Fn ` `_summarize_split_reports` (L2268)
- [ ] ✗ `Fn ` `_summarize_lofo_generalization` (L2288)
- [ ] ✗ `Fn ` `_core_metric_value` (L2332)
- [ ] ✗ `Fn ` `_build_phase14_lockbox_gate` (L2346)
- [ ] ✗ `Fn ` `_build_phase14_lofo_gate` (L2382)
- [ ] ✗ `Fn ` `_score_delta` (L2412)
- [ ] ✗ `Fn ` `_lockbox_primary_bucket` (L2420)
- [ ] ✗ `Fn ` `_lockbox_cluster_focus` (L2438)
- [ ] ✗ `Fn ` `_summarize_lockbox_residual_clusters` (L2450)
- [ ] ✗ `Fn ` `_build_phase14_promotion_evaluation` (L2525)
- [ ] ✗ `Fn ` `_resolve_pds_gate` (L2555)
- [ ] ✗ `Fn ` `run_phase7_evaluation_bundle` (L2598)
- [ ] ✗ `Fn ` `run_phase14_evaluation_bundle` (L2705)
- [ ] ✗ `Fn ` `_metric_delta` (L2756)
- [ ] ✗ `Fn ` `_phase15_recommendation` (L2760)
- [ ] ✗ `Fn ` `_build_phase15_report_comparison` (L2775)
- [ ] ✗ `Fn ` `run_phase15_comparison_bundle` (L2874)
- [ ] ✗ `Fn ` `_format_report` (L2971)
- [ ] ✗ `Fn ` `_jsonable_report` (L3059)
- [ ] ✗ `Fn ` `_jsonable_phase7_bundle` (L3068)
- [ ] ✗ `Fn ` `_jsonable_phase14_bundle` (L3083)
- [ ] ✗ `Fn ` `_jsonable_phase15_bundle` (L3096)
- [ ] ✗ `Fn ` `_format_phase7_bundle` (L3108)
- [ ] ✗ `Fn ` `_format_phase14_bundle` (L3279)
- [ ] ✗ `Fn ` `_format_phase15_bundle` (L3377)
- [ ] ✗ `Fn ` `main` (L3434)

### `batch.py`  module:✗

- [ ] ✗ `Cls` `BatchReviewItem` (L23)
- [ ] ✗ `Cls` `BatchTriagePolicy` (L33)
- [ ] ✗ `Cls` `BatchReviewRow` (L44)
- [ ] ✗ `Cls` `BatchReviewRun` (L68)
- [ ] ✗ `Fn ` `batch_item_from_dict` (L78)
- [ ] ✗ `Fn ` `load_batch_items` (L92)
- [ ] ✗ `Fn ` `_build_request` (L113)
- [ ] ✗ `Fn ` `_dimension_score` (L123)
- [ ] ✗ `Fn ` `_unsupported_issue_count` (L130)
- [ ] ✗ `Fn ` `triage_review_result` (L134)
- [ ] ✗ `Fn ` `_review_once` (L171)
- [ ] ✗ `Fn ` `_p95` (L185)
- [ ] ✗ `Fn ` `_row_to_export_dict` (L195)
- [ ] ✗ `Fn ` `export_batch_run` (L221)
- [ ] ✗ `Fn ` `run_batch_review` (L255)
- [ ] ✗ `Fn ` `main` (L425)

---

## Phase 8 — tests/

> 见 [PYDOC_INVENTORY.md §A5](./PYDOC_INVENTORY.md#a5-test_pypy-文件的-docstring-优先级)：建议 module-level + 关键 class docstring，单个 test_func 可跳过。

### `test_batch.py`  module:✗

- [ ] ✗ module docstring（说明该测试文件覆盖什么场景）
- [ ] _good_item / _bad_item / test_run_batch_review_produces_triage_and_observability / test_batch_load_and_export_round_trip — 按 §A5 决定是否写

### `test_benchmark.py`  module:✗

- [ ] ✗ module docstring
- [ ] FakeAgent 等 helper class 加 docstring
- [ ] 单个 test_xxx 函数按 §A5 决定

### `test_review.py`  module:✗

- [ ] ✗ module docstring
- [ ] DummyLLM 等 helper class 加 docstring
- [ ] 单个 test_xxx 函数按 §A5 决定

---

## Phase 9 — compatibility/

### `compatibility/__init__.py`  module:✗
（仅加 module docstring，标注 deprecated；指向 ExpertReviewAgent）

### `compatibility/legacy_api.py`  module:✗

- [ ] ✗ `Fn ` `review_artifacts` (L10)（加 deprecation 注释）
- [ ] ✗ `Fn ` `review_model` (L20)（加 deprecation 注释）
- [ ] ✗ `Fn ` `heuristic_expert_review` (L29)（加 deprecation 注释）

---

## Phase 0 — 死代码（按 [PYDOC_INVENTORY.md §A](./PYDOC_INVENTORY.md#a-死代码清理候选) 决策结果删除）

### `legacy/__init__.py`  module:✗  ⚠️ 候选删除
### `legacy/prompts.py`  module:✗  ⚠️ 候选删除（13 KB）
### `legacy/rubrics.py`  module:✗  ⚠️ 候选删除

如保留则需补 docstring；如删除则跳过 Phase 0。

---

## 总览统计

| Phase | 文件 | items 总数 | 备注 |
|---|---:|---:|---|
| Phase 0 (legacy/) | 3 | 5 | 待 §A1 决策 |
| Phase 1 (schema + 入口) | 9 | 30 | 高优 |
| Phase 2 (graph) | 5 | 16 | |
| Phase 3 (agents) | 17 | 79 | 最大 |
| Phase 4 (prompts) | 10 | 4 | 多数仅 module |
| Phase 5 (tools) | 8 | 58 | |
| Phase 6 (utils + 顶层) | 5 | 63 | |
| Phase 7 (benchmark + batch) | 2 | 125 | benchmark.py 109 个 items |
| Phase 8 (tests) | 3 | 57 | 按 §A5 可缩到 ~10 |
| Phase 9 (compatibility) | 2 | 3 | 加 deprecation |
| **合计** | **64** | **440** | |

