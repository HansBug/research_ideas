# X1v2 Witness Correction Independent Review

## Scope

An independent pane5 subagent performed this provider-free, read-only review after the semantic issue was identified. It did not edit raw artifacts, method/Judge code, review decisions, labels, or reports, and it did not invoke a provider or run an experiment.

## Findings

`0036:r1:0036:r1:baseline_issue_4` is W0 under the issue #189 definition. The raw `where` is only “整体状态机，特别是终止/完成相关建模”; neither it nor the finding's issue/reason identifies a state, event, guard, transition, endpoint pair, bounded fragment, or finite path. The source PlantUML contains `TargetSearch` and concrete transitions, but those source objects cannot be used to retrofit a carrier absent from the finding. The evidence is `raw/x1v2_baseline/method/run1/0036-luna/record.json#/parsed_output/issues/3`, `derived/x1v2_witness_review_packet.json#audit_key=0036:r1:0036:r1:baseline_issue_4`, and `reference/x1v2_input_closure/pairs/0036/{nl.txt,plantuml.puml}`. Judge linkage was not used.

`0050:r3:0050:r3:baseline_issue_1` is source-faithful. Its packet `issue`, `where`, and `finding_reason` are byte-identical to raw `/parsed_output/issues/0`; their SHA-256 values are respectively `sha256:0d2c64efcc14154538e62d4f4a965d7c3cc0c4177ecd8d01b5563c0282a8f924`, `sha256:473ce9372190cfe5b2fb6f29e5c57c8abddd6654ba91c5af9fb0568a472eecc3`, and `sha256:cf8af238a2554e9208984b38eb3cb331cf01a5a5edbd04e0c659c43d881f8d53`. The visible `\\n` sequence is a literal frozen source sequence, not a packet normalization.

The reviewer also found that a correction record must not accept an arbitrary review-path string. The reporting fix requires `independent_review_path` to be an archive-relative `reviews/` path, requires it to resolve to an existing file containing the audit key, preserves the two blind decisions verbatim, and restricts post-review corrections to the single audited key. Focused regression tests cover invalid paths, allowlist rejection, raw-text fidelity, and the final archive validation path.

## Conclusion

Accept the W1-to-W0 correction for `0036:r1:0036:r1:baseline_issue_4`. The item is not a FULL supporting report, so it changes finding-level W counts only. This review does not attribute any experimental result to a method or Judge change and does not create baseline W2 evidence.
