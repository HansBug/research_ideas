# Claude 交叉评审任务（case {{CASE_ID}} reference STM）

你正在**交叉评审** codex 起草的 reference pyfcstm STM。这份 ref 已经通过 pyfcstm parse + sem + sim 三关 + scenarios 自检，但**机械合规 ≠ 语义正确**。你的任务是从**语义忠实性 / NL 覆盖度 / C-axis grounding 恰当性 / hallucination 检查**4 个维度独立审阅，给出 verdict + 具体修订建议。

## 必读上下文

1. **STM.md case section**：`{{STM_PATH}}`
   - 找 `## 条目 N: {{CASE_NAME}}` 段，读 §0/§1/§2/§3
2. **expansion NL（含 [E] 溯源 markers）**：`{{EXPANSION_PATH}}`
3. **paper PDF**（必要时核对）：`{{PAPER_PDF}}`
4. **codex 起草的 ref DSL**：`{{REF_FCSTM}}`
5. **codex 起草的 scenarios**：`{{REF_SCENARIOS}}`
6. **codex 自己的设计笔记**：`{{REF_NOTES}}`

## 评审维度（每条独立打分）

### A. semantic_correctness — DSL 实际语义是否对

- ref 中每个 state / event / variable 是否与 STM §1 摘录中原文出现的命名 / 含义一致？
- transitions 的 guard / effect 是否对应原文描述的真实条件？
- per-cycle 行为（if any）是否与原文"每周期做什么"一致？
- mode 嵌套层次（如 HSM）是否对应原文 mode 关系？

打分：🟢 完全对应 / 🟡 大体对应有小偏差 / 🟠 多处偏差 / 🔴 重大语义错误

### B. nl_faithfulness — 是否引入 NL 没有的内容（hallucination）

- ref 中是否有 state / event / variable / threshold 在 STM 摘录 + expansion NL 里找不到出处？
- 是否有 fault path / 数值阈值 / 硬件名是 codex "脑补"出来的？
- 是否有为了"凑 C-axis 使用"硬塞的 feature 而不被 NL 支持？

打分：🟢 零 hallucination / 🟡 1-2 处合理推断（如默认值） / 🟠 多处发明 / 🔴 大量编造

### C. c_axis_grounding_appropriateness — pyfcstm grounding feature 使用是否合理

- **C1 (周期执行)**：用了 `during {}` / `>> during` aspect 吗？若用了，原文是否支持周期行为？若没用，原文是否本来就不需要？
- **C2 (数值守卫)**：复合数值 guard 是否用 Expr IR 多变量算术表达？变量名 + 阈值是否来自原文？
- **C3 (forced fault)**：`! * -> Error :: Event` 是否对应原文"任意 mode 下 Error / Emergency / Abort" 全局 fault 语义？还是把局部 fault 错放成 forced？
- **C4 (硬件)**：`enter/during/exit abstract` 占位是否对应原文具名 effector？还是把通用 action 错放成 abstract？

打分：🟢 4 个 axis 全部恰当 / 🟡 1-2 个 axis 有改进空间 / 🟠 多个 axis 错用或漏用 / 🔴 grounding 普遍不恰当

### D. nl_coverage — scenarios 是否覆盖 NL 全部关键特性

- 每个关键 mode 是否有 scenario 验证？
- 每个数值 guard 阈值边界是否有 scenario？
- 每个 fault path 是否有 scenario 触发？
- 每个 per-cycle 行为是否有 ≥3 cycle 的 scenario？
- 每个具名 effector 是否被 scenarios 触达？

打分：🟢 全特性覆盖 / 🟡 主要特性覆盖少数遗漏 / 🟠 多个特性未覆盖 / 🔴 仅 smoke 级别覆盖

## verdict 判定

- **APPROVE**: 4 个维度均 🟢 或 🟡（即 codex draft 直接可用 / 略调即可）
- **REVISE**: 任一维度 🟠 或 🔴（codex 必须根据 comments 修订）

## 输出 strict JSON

```json
{
  "case_id": "{{CASE_ID}}",
  "verdict": "APPROVE" | "REVISE",
  "scores": {
    "semantic_correctness": {"emoji": "🟢|🟡|🟠|🔴", "evidence": "1 句中文 + 关键 NL 片段引用"},
    "nl_faithfulness": {"emoji": "🟢|🟡|🟠|🔴", "evidence": "1 句中文，列出可疑 hallucination（如果有）"},
    "c_axis_grounding_appropriateness": {"emoji": "🟢|🟡|🟠|🔴", "evidence": "1 句中文，按 C1-C4 打分理由"},
    "nl_coverage": {"emoji": "🟢|🟡|🟠|🔴", "evidence": "1 句中文，scenarios 覆盖度"}
  },
  "hallucinations_found": [
    {"type": "state|event|var|threshold|effector|fault", "name": "...", "issue": "..."}
  ],
  "specific_revision_suggestions": [
    "具体 1 句中文修订建议（如 'state Y 中加 during {} 以模拟原文 [E5] 的 per-cycle 监控行为'）",
    "..."
  ],
  "missing_scenarios_suggestions": [
    "建议补充的 scenario 名 + 简述（如 'fault_recovery_from_running: 验证 Running 状态下 Emergency 触发后到达 ErrorHandler'）"
  ],
  "overall_comment": "2-3 句中文总评"
}
```

输出**仅** JSON，无 markdown fence，无前后缀。

## 评审纪律

1. **要严格**：codex draft 自检通过不代表语义对，你的 job 就是 catch codex 漏的 / 错的
2. **拿不准要查原文**：原文支持就写 evidence 引用，原文不支持就明确说"原文未支持"
3. **REVISE 的 comments 要具体**：别说"建议改进 C3"，要说"原文 [E12] 描述任意状态下 Error 都强制切到 Idle，建议 ref 加 `! * -> Idle :: Error`"
4. **APPROVE 不要轻易给**：宁可 REVISE 多一轮迭代也别让有问题的 ref 进入下一阶段
