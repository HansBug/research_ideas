# Final talk method-cost audit v1

This evaluation-only audit reads the archived method provider-usage receipts for the frozen 162 cells on each side. It excludes evaluator, human review, CPU, storage, waiting, and development costs. `output_tokens` already include reasoning tokens and are charged once.

`ours` has a complete receipt closure: `$7.18277320`. `baseline` has a known recorded subtotal: `$0.22523328`; one billed schema-error attempt has no retained usage receipt, so its complete cost is `$0.22523328 + missing schema-attempt cost`, not an exact total. The corresponding subtotal ratio is at most `31.8904x`, not a complete ratio.

The historical `$6.77501040` artifact at `raw/x1v2_baseline/method/corrected_cost_audit.json` belongs to the old current/evidence-discovery run `90d1c41e000000000000000000000162`. It is retained only as a misbound historical provenance artifact and is not baseline cost.

Rebuild: `python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_final_talk_cost_section7_v1.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline`

Validate: append `--validate` to the same command.
