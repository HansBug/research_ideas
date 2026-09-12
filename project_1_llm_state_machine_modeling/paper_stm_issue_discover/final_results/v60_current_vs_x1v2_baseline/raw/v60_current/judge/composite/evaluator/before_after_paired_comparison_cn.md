# Soundness/S2 Before-After Audit

- 这是一份 evaluator-only 配对比较；method 与冻结 Judge 制品均保持不可变。
- Overall FULL: 301/435 -> 306/435 (delta +5).
- L2 FULL: 101/117 -> 104/117 (delta +3).
- Semantic precision: 0.9237 -> 0.9166 (delta -0.0071).
- FULL-hit max-W2 share: 0.7076 -> 0.6895 (delta -0.0181).
- S2 matched-input verdict flips: 0/147; before-only carriers: 221; after-only carriers: 235.
- Expected pair-round relation changes: 99; typed report-surface changes: 1590.
- 单次配对结果仍包含新 LLM 采样波动；本摘要不将任一单格差异单独归因于 soundness 或 S2 修正。
