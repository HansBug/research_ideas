# prompts/

保存 A1-DT v2 19×3 审计的原始 prompt。建议命名：`<slug>__<agent>.prompt.md`。

每份 prompt 必须强调：单篇原生维度树 / 维度森林优先，A1-M0--M6 只作跨论文投影，roadmap / guideline 等无系统样本库论文必须降级。

## 证据链边界

本目录下已经物化的 `*.prompt.md` 是对应 57 次审计运行的历史输入证据，应保持原貌以便复验当时的 agent 行为；它们不是后续生成 prompt 的事实真源。若要修改后续任务提示词，只能修改上级目录的 [generate_prompts.py](../generate_prompts.py)，并重新生成新批次 prompt。历史 prompt、`logs/` 和 `results/` 允许保留当时的候选性措辞，但不得绕过主线程裁决、A2a 原文版面精核和结构门禁进入正式 `review.md` 附录或 `SUMMARY.md` 总账。
