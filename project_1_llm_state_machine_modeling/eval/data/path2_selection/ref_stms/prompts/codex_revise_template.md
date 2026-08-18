# REF STM 修订任务（case {{CASE_ID}}）

你之前为 case `{{CASE_ID}}` (`{{CASE_NAME}}`) 起草了 reference pyfcstm STM 并通过了 pyfcstm 验证 + 0 warning lint。但 **claude 交叉评审给出了 REVISE 判决**，列出了具体问题与修订建议。你的任务是**按 claude 反馈把 ref 修到 APPROVE 质量**。

## 必读：前次产物 + claude 评审反馈

1. **前次起草的 ref DSL**：`{{PREVIOUS_FCSTM}}`
2. **前次起草的 scenarios**：`{{PREVIOUS_SCENARIOS}}`
3. **前次 codex notes**：`{{PREVIOUS_NOTES}}`
4. **claude 评审 JSON（含 hallucinations / revision_suggestions / missing_scenarios）**：`{{CLAUDE_REVIEW}}`
5. **原始上下文**（与起草阶段相同）：
   - STM.md case section: `{{STM_PATH}}`
   - expansion NL: `{{EXPANSION_PATH}}`
   - paper PDF: `{{PAPER_PDF}}`
   - pyfcstm grammar: `{{GRAMMAR_REF_PATH}}`

## 修订纪律

1. **逐条响应**：claude 列的 `hallucinations_found` 必须全部修复；`specific_revision_suggestions` 必须全部采纳（除非有充分理由拒绝，并在 notes §6 详细说明）；`missing_scenarios_suggestions` 至少补充 80%。
2. **保留前次好东西**：claude 没 flag 的部分（如 grounding 用法、变量命名、scenarios 覆盖度的合理部分）应**保留**，**不要全部推翻重写**。
3. **依然必须通过验证 + 0 warning**：完整 verifier (parse / sem / sim / scenarios / lint) 全过。
4. **变量原则不变**：禁止 write-only var / 装饰性 indicator；变量必须有读者。
5. **C-axis grounding 仍由 NL 支持决定**：如果 claude 建议加 C3 forced transition 且 NL 确实支持，加；如果 claude 建议某 C-axis 是发明，删。

## 验证（与起草阶段相同）

```bash
cd /home/zhangshaoang/oo-projects/research_ideas-2
source venv/bin/activate
python3 project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms/verify_pyfcstm_full.py {{OUTPUT_FCSTM}} {{OUTPUT_SCENARIOS}}
```

期望最后两行：`LINT_SUMMARY: warnings=0 by_code={}` + `ALL_OK`

Max 5 iter combined。每次 fail → 读错误 → 修复 DSL 或 scenarios → 再跑。

## 输出文件

1. `{{OUTPUT_FCSTM}}`：修订后的 pyfcstm DSL
2. `{{OUTPUT_SCENARIOS}}`：修订后的 scenarios（补充 claude 列的 missing_scenarios + 删去因 mode 折叠不再适用的）
3. `{{OUTPUT_NOTES}}`：修订笔记，必须包含一节 `## 6. claude 评审反馈响应`，逐条列出：
   - claude 提的每条 hallucination → 我怎么修复
   - claude 每条 revision_suggestion → 是否采纳 + 怎么改
   - claude 每条 missing_scenario → 是否补 + 哪个 scenario_name 对应

## 最终 JSON 输出（agent_message）

```json
{
  "case_id": "{{CASE_ID}}",
  "revision_round": 1,
  "iterations": <int>,
  "final_validation": {
    "parse": "OK" | "FAIL",
    "sem": "OK" | "FAIL",
    "sim": "OK" | "FAIL",
    "scenarios_total": <int>,
    "scenarios_pass": <int>,
    "scenarios_fail": <int>,
    "scenarios_error": <int>,
    "lint_warnings": <int>,
    "states_count": <int>
  },
  "claude_feedback_addressed": {
    "hallucinations_fixed": <int>,
    "hallucinations_total": <int>,
    "suggestions_adopted": <int>,
    "suggestions_total": <int>,
    "missing_scenarios_added": <int>,
    "missing_scenarios_total": <int>
  },
  "design_summary": "1-2 句中文，说明本次修订的主要变化",
  "files_written": ["{{OUTPUT_FCSTM}}", "{{OUTPUT_SCENARIOS}}", "{{OUTPUT_NOTES}}"]
}
```

输出**仅** JSON，无 markdown fence，无前后缀。

## 评审纪律

1. **JSON only**
2. **完成 ≠ 推翻重做**：保留好的部分 + 精准修复 claude flag 的部分
3. **诚实**：如果 claude 某条建议你不同意（如不实际可行），在 notes §6 写清拒绝理由 + 给替代方案；不要假装采纳了
4. **lint 必须 0 warning**：修订不能引入新的 dead var / unused event
