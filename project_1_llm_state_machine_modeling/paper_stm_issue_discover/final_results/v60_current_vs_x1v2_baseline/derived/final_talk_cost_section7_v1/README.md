# Final talk method-cost audit v1

This evaluation-only audit reads the archived method provider-usage receipts for the frozen 162 cells on each side. It excludes evaluator, human review, CPU, storage, waiting, and development costs. `output_tokens` already include reasoning tokens and are charged once.

The frozen `gpt-5.6-luna` price card records `https://developers.openai.com/api/docs/pricing`, verified on `2026-08-18`, with `basis=official_list_price`. Its three source artifacts and `source_closure_sha256` are recorded in `method_cost_audit_v1.json#/pricing`.

`ours` has a complete receipt closure: `$7.18277320`. `baseline` has a known recorded subtotal: `$0.22523328`; one billed schema-error attempt has no retained usage receipt, so its complete cost is `$0.22523328 + missing schema-attempt cost`, not an exact total. The corresponding subtotal ratio is at most `31.8904x`, not a complete ratio.

Rebuild: `python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_final_talk_cost_section7_v1.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline`

Validate: append `--validate` to the same command.
