# 历史版本逐文件引用清单

本文件由当前工作树中的历史关键词命中机械枚举，再按路径优先级标注文档职责。枚举不替代语义复核：每一行说明该文件为何可保留历史版本名，以及它不能承担的当前职责。

```bash
rg -l -i --glob '*.md' 'v27(?:-stream)?|v46|v26|feedback[_ -]?loop|59\.8%|70\.3%|47\.9%' project_1_llm_state_machine_modeling/paper_stm_issue_discover | sort
```

| 文件 | 分类 | 允许原因与当前边界 |
| --- | --- | --- |
| `GUIDE.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `PENDING_DECISIONS.md` | historical/planning | 保存过去的实验设计或决策背景；不构成 current 执行授权。 |
| `README.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `RELEASE_STRUCTURE_PLAN.md` | provenance | 保存历史关系或审计依据；不作为 current 方法、结果或默认复算入口。 |
| `STATUS.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `SUMMARY.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `TODO.md` | historical/planning | 保存过去的实验设计或决策背景；不构成 current 执行授权。 |
| `archive/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/experiment_history/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/legacy/feedback_loop/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/audit.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/composition.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/preregistered.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/result.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/unexpected_adjudication.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/unexpected_evidence.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/unexpected_merged.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r10_ledger_v1_and_v46/v46/unexpected_tables.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-baseline-seed-method-crosswalk.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r5_7_better_stm_snapshot/reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r7_issue_lifecycle_scaffold/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r7_issue_lifecycle_scaffold/evidence_ledgers/legacy_asset_inheritance.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/story/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/story/claim_evidence_map.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/story/model_scope.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/story/paper_outline.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/story/paper_story.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/story/task_boundary.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r8_story_pre_rebuild/story/terminology_policy.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r9_agent_loop_pipeline/ARCHIVE_README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `archive/r9_agent_loop_pipeline/agent_loop/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `baseline_arm/docs/generations/x1v2/result.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/docs/generations/x1v2/verdicts.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/judging_instructions.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/preregistered.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/preregistered_actionability.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/results/form_control/rendering_rules.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/results/metrics.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/results/rejudge/REJUDGE_REPORT.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/results/rejudge/positions_final.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/results/rejudge/rejudge_instructions.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/results/unexpected_verdicts/comparison.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `baseline_arm/results/unexpected_verdicts/evidence.md` | historical/provenance | 保存 X1v2 的设计、旧判定或分析；current baseline 使用 issue #195 rejudge 的 final archive。 |
| `corpora/nl_datasets/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/nl_segmentation/PROVENANCE.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/nl_segmentation/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/repair_baselines/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/repair_baselines/SUMMARY.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/repair_baselines/ttool-ai-feedback/baseline_desc.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/seed_library/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/seed_library/llms-emp-stm-subset/artifacts.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `corpora/seed_library/pushing-generative-envelope-mbse/seed_desc.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/README.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `discover_matrix/docs/findings/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/findings/human_baseline_and_assertion_cot.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/findings/predicates/defects_registered.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/findings/ref_flip_feasibility.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/findings/representation_debt.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/findings/um_residue_ruling.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/findings/v46_weakness_anatomy.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/generations/v21/preregistered_calibre.md` | historical/preregistered | 保存代次登记与过程记录；不定义 current headline 或 current Judge 指标。 |
| `discover_matrix/docs/generations/v22/backlog.md` | historical/preregistered | 保存代次登记与过程记录；不定义 current headline 或 current Judge 指标。 |
| `discover_matrix/docs/generations/v22/progress.md` | historical/preregistered | 保存代次登记与过程记录；不定义 current headline 或 current Judge 指标。 |
| `discover_matrix/docs/generations/v24/report_determined.md` | historical/preregistered | 保存代次登记与过程记录；不定义 current headline 或 current Judge 指标。 |
| `discover_matrix/docs/generations/v27/preregistered.md` | historical/preregistered | 保存代次登记与过程记录；不定义 current headline 或 current Judge 指标。 |
| `discover_matrix/docs/generations/x1-split-intervention/preregistered.md` | historical/preregistered | 保存代次登记与过程记录；不定义 current headline 或 current Judge 指标。 |
| `discover_matrix/docs/generations/x1-split-intervention/result.md` | historical/preregistered | 保存代次登记与过程记录；不定义 current headline 或 current Judge 指标。 |
| `discover_matrix/docs/protocol/archive/legacy_20260821/method_provenance_policy.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/protocol/archive/legacy_20260821/rules/conditional_activation.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/protocol/archive/legacy_20260821/rulings/wellformedness_attribution.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/docs/protocol/dtier_triage.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/docs/protocol/ground_truth_limitations.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/docs/protocol/hit_criterion.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/docs/protocol/nl_scope_rule.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/docs/protocol/rule_provenance.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/docs/protocol/unexpected_taxonomy.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/docs/protocol/verdict_methodology.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `discover_matrix/ledger_v2/README.md` | provenance | 保存历史关系或审计依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/X1V2_RESULTS.md` | provenance | 保存历史关系或审计依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/provenance/FINAL_STRATIFICATION.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/provenance/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/provenance/STRATIFICATION.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/provenance/eis_bundle/audit/predcov_BRIEF.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/provenance/predicate_coverage/BRIEF.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/provenance/relabel/HOWTO.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `discover_matrix/ledger_v2/provenance/relabel/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `evidence/matrices/baseline_candidate_matrix.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `experiment_design/next_round.md` | historical/planning | 保存过去的实验设计或决策背景；不构成 current 执行授权。 |
| `final_results/v60_current_vs_x1v2_baseline/README.md` | current/result | 这是 current 冻结结果归档；历史版本名仅用于 provenance 或 superseded 判别。 |
| `judge/src/paper_stm_judge/resources/semantic_judge_issue_195.snapshot.md` | frozen-protocol | 保存冻结规则或 protocol snapshot；历史版本名只在其原始语境中保留。 |
| `pipeline/README.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/archive/witness_search_prototype_legacy_20260821/README.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `pipeline/conversion/README.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/evidence_discovery/README.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/representation/README.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/representation/reports/llms_emp_r45_java_60/pairs/0000/SEGMENTATION_NOTE.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/representation/reports/llms_emp_r45_java_60/pairs/0010/SEGMENTATION_NOTE.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/representation/reports/llms_emp_r45_java_60/pairs/0020/SEGMENTATION_NOTE.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/representation/reports/llms_emp_r45_java_60/pairs/0030/SEGMENTATION_NOTE.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/representation/reports/llms_emp_r45_java_60/pairs/0040/SEGMENTATION_NOTE.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `pipeline/representation/reports/llms_emp_r45_java_60/pairs/0050/SEGMENTATION_NOTE.md` | compatibility/provenance | 保留兼容 namespace、输入准备或旧过程材料；current 入口分别是 method、judge 与 evaluation。 |
| `related_work/archive/legacy_20260821/CONTINGENCY_L2.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `related_work/assertion_output_form_evidence.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/deployment/README.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/deployment/c2_rebuttal.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/deployment/c4_rebuttal_neg_result.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/deployment/c5_arithmetic_check.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/deployment/h200x4_inference_perf.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/deployment/small_model_papers.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/form_asymmetry_evidence.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/CRITERIA_MIGRATION.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/SUMMARY.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/TOOL_ROLE_TAXONOMY.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/_ours-v46.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/_taxonomy-and-semantic-feedback.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/accurate-consistent-graph-model-generation.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/asew2025-eventb-model-repair.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/emse2026-ladex-critique-ablation.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/erts2026-safe-llm-mde.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/etfa2025-stpa-fsm-refinement.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/event-b-agent.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/iet-software-2025-consistency-traceability.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/internetware2025-sysml-behavior-generation.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/llm-guided-predicate-discovery.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/mcet-models2025.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/models2024-ai-driven-sysml-consistency.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/pat-agent.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/rfseek.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/sosym2026-state-machine-consistency.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/standard-conformant-prompting.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/stateful-multiagent-crossview-drift.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/structure-event-driven-stm-frameworks.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/synthesizing-protocol-specs.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/tla-bench-execution-grounded.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/cards/zenodo-simulink-repair-traces.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/design_evidence.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/m1_recommendations.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/pipeline_forms.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/neighborhood/tool_roles.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/provenance/archive/legacy_20260821/SUMMARY.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `related_work/provenance/archive/legacy_20260821/evidence_distribution.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `related_work/provenance/archive/legacy_20260821/methodology.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `related_work/provenance/archive/legacy_20260821/predicate_motive_audit.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `related_work/provenance/corpus_scan_findings.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `related_work/provenance/predicate_provenance.md` | provenance | 保存输入、资料、ledger 或历史诊断依据；不作为 current 方法、结果或默认复算入口。 |
| `release/documentation_audit/current_facing_markdown_inventory.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/facts_ledger.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/legacy_version_reference_audit.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/legacy_version_reference_rows.md` | release/provenance | 保存机械枚举与逐文件职责判断；不替代论文主实验归档。 |
| `release/documentation_audit/review_disposition.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/reviews/01_numeric_experiment_facts_review.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/reviews/02_architecture_boundary_review.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/reviews/03_history_archaeology_review.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/reviews/04_documentation_navigation_review.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `release/documentation_audit/shuorenhua_rewrite_record.md` | release/provenance | 保存 release、审计或 internal RC 的可复核证据；不替代论文主实验归档。 |
| `reports/2026-08-11-post-refactor-e2e-smoke.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-19-judge-model-comparison.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-19-luna-full-x3-v26.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-19-luna-full-x3-v26/REPORT-sol.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-19-luna-full-x3-v26/judge-sol/README.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-20-luna-full-x3-v27-stream/README.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-20-luna-full-x3-v27-stream/RUN_AUDIT.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/2026-08-25-evidence-discovery-v51-final-54x3.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/README.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `reports/SUMMARY.md` | historical/report | 保存日期化研究报告和旧 Judge/运行记录；current 结果只以 final archive 为准。 |
| `story/README.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `story/archive/legacy_20260821/blueprint_proposal.md` | historical/archive | 保存归档路线、冻结材料或旧叙事；不作为 current 方法、结果或默认复算入口。 |
| `story/claim_evidence_map.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `story/paper_outline.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `story/paper_story.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
| `story/terminology_policy.md` | current/public | 默认入口仅将历史版本用于不可比性限制或历史索引链接，不把它们作为 current 事实源。 |
