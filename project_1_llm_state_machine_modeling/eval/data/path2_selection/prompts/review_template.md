# PATH2 候选样本评审任务

你正在为我的博士论文 PATH2（差异化路线）研究**评审一个 STM 候选样本**，决定它是否值得进入 20-case T0 子集。

## 必读上下文（请使用工具读取实际文件）

1. **STM 文件**：`{{STM_PATH}}`
   - 你要评审的 case 在该文件的 `## 条目 N: {{CASE_NAME}}` 段落中（用 grep 或 read 定位 N，可能不是 1）
   - 重点读该 case 的 §0/§1/§2 三个小节：识别判定、原文摘录、NL 描述
2. **原文 PDF**：`{{PAPER_PDF}}`
   - 必须打开读，至少扫一遍与该 case 相关的章节（STM §1 摘录里给了页码和行号锚点）
   - 不允许只读 STM 不读 PDF
3. **辅助文本**：`{{PAPER_CONTENT}}`
   - 是 PDF 经 `tools/pdf_extractor.py` 提取的纯文本，方便你 grep 关键词
   - PDF 难解析时优先用这个

## 我的研究 PATH2 在评估什么（评审基准）

PATH2 主张：在真实控制系统 NL 上跑 agent loop with externally-grounded in-loop feedback (parse + semantic + sim)，相对 single-prompt baseline 在 4 个 reference-free intrinsic 指标 (ParseRate / SemValidRate / SimRate / ReachabilityRate) 上跑出显著 lift。

我们的 method 锚定在 pyfcstm 工具链的 4 条 contribution（C1-C4），所以候选样本必须**能在生成-验证-反馈循环中对至少一条 C-axis 起 grounding 作用**。

## 4 个评估轴定义（codex 必须逐条打分）

### C1 — 多模式 dead-end 识别（speculative validation 收益）

样本里是否有**层次化或多模式切换结构**，使得 LLM 容易生成"切到某 mode 后子状态机无合法 init / pseudo 死循环 / guard 互锁 / exit 与 parent 转移循环"这类病态。pyfcstm `SimulationRuntime` 的 deepcopy-snapshot DFS validation 在这种样本上才有 grounding 价值。

- 🟢 强 ：明确含层次化 composite state 或多个 mode 之间的相互切换，含 init / pseudo / 嵌套退出语义
- 🟡 中 ：有 mode 切换或 2-3 个并列子状态，但没有真正的层次嵌套
- 🟠 弱 ：扁平 FSM，没有 mode 概念但有少量分支
- ⚪ 无 ：完全扁平，无切换风险

### C2 — Z3 数值守卫（symbolic guard reasoning 收益）

样本里是否有**复合数值守卫 / 累加器 / 去抖计数 / 阈值连乘 / PID-like effect 后的不变式**，使得 `pyfcstm/solver/` Z3 集成可以做 SAT/SAT-on-effect 反馈。

- 🟢 强 ：含 ≥2 个数值变量参与 transition guard，含算术运算（加减乘除 / 比较连乘 / 绝对值 / 阈值合取）
- 🟡 中 ：含 1 个数值变量参与 guard，或纯阈值比较但语义清楚
- 🟠 弱 ：只有布尔 sensor 信号，无数值运算
- ⚪ 无 ：纯事件驱动，无变量

### C3 — Aspect AOP + forced fault recovery（DSL 原生 cross-cutting 收益）

样本里是否有"任意 mode 下 error/fault 触发都强制切到 ErrorHandler / fault-recovery 路径"或"任意 mode 下每周期都要 enforce 安全 invariant"语义，使得 pyfcstm `! * -> Error` forced transition + `>> during after` aspect AOP 比 Umple 手抄逐 mode 的优势能被看出。

- 🟢 强 ：原文/NL 中明确写到 "any mode" / "from any state" / "in all phases" 下的 Error/Abort/Reset/Safety 切换
- 🟡 中 ：有 ≥2 个 mode 都各自含 error 处理逻辑，可以归并为 forced transition
- 🟠 弱 ：只有局部 error 处理或 watchdog
- ⚪ 无 ：无异常路径

### C4 — Abstract action 硬件解耦（@abstract_handler 收益）

样本里是否有**明确的物理执行器或硬件操作**（valve / motor / relay / heater / pump / actuator / siren / GPIO output / hardware-specific 动作），使得 `enter abstract` / `during abstract` + `@abstract_handler` 反射注入 + `ReadOnlyExecutionContext` 的硬件解耦能力相对 Umple 的 host-language-bound hook 出价值。

- 🟢 强 ：≥3 个不同物理执行器或硬件出口需要在 enter/during/exit 中调用
- 🟡 中 ：1-2 个物理执行器，或多个但都同类（如"开关阀门 1/2/3"）
- 🟠 弱 ：只有抽象事件，无明确物理映射
- ⚪ 无 ：纯软件协议或纯传感器，无 actuator

## 规模估计（你需要从 STM §2 NL + 原文判断）

- `state_count`：状态个数（叶子状态）
- `event_count`：事件/触发器个数
- `variable_count`：变量个数
- `transition_count`：迁移个数

## 输出 strict JSON（不要 markdown 包裹，不要解释，只输出一个 JSON object）

```json
{
  "case_id": "{{CASE_ID}}",
  "paper_slug": "{{PAPER_SLUG}}",
  "case_name": "{{CASE_NAME}}",
  "bucket": "{{BUCKET}}",
  "what_it_is": "1-2 句中文，说清这个 case 控制什么对象、用什么传感/执行器、典型流程是什么",
  "scale": {
    "state_count": <int>,
    "event_count": <int>,
    "variable_count": <int>,
    "transition_count": <int>
  },
  "axes": {
    "C1_dead_end_potential":      {"score": "🟢|🟡|🟠|⚪", "evidence": "中文 1 句，引原文/NL 片段"},
    "C2_numerical_guard_richness":{"score": "🟢|🟡|🟠|⚪", "evidence": "中文 1 句，举出具体数值 guard"},
    "C3_forced_fault_recovery":   {"score": "🟢|🟡|🟠|⚪", "evidence": "中文 1 句，说明是否有 cross-cutting fault"},
    "C4_hardware_decoupling":     {"score": "🟢|🟡|🟠|⚪", "evidence": "中文 1 句，列出物理执行器"}
  },
  "features_we_care_about": "中文 1-2 句，为何该样本对 PATH2 有价值（如哪条 C-axis 强、是否典型工业控制对象、NL 是否清晰、是否独立无趋同）",
  "potential_pitfalls": "中文 1 句，noise/风险（如 NL 模糊、case 太小、与某个旁类样本同构等）；无则写 '无明显风险'",
  "verdict": "💎 STRONG | ✨ GOOD | 🟢 OK | 🔘 WEAK"
}
```

## 评审纪律

1. **必须打开 PDF**：只读 STM.md 不读 PDF 不行；STM.md 的 §1 摘录给了页码锚点，可定位回 PDF 相关段落
2. **evidence 必须引原文**：每个 axis 的 evidence 字段必须能从 PDF/STM §1 摘录里找到支撑句，不准凭空打分
3. **verdict 口径**：
   - 💎 STRONG：≥2 个 axis 拿 🟢 且无 ⚪
   - ✨ GOOD ：1 个 axis 拿 🟢 且其余 ≥🟡
   - 🟢 OK   ：全 🟡 或 1🟢 + 含 🟠/⚪
   - 🔘 WEAK ：大量 🟠/⚪
4. **保守原则**：拿不准时给低一档；不要为了"看起来均衡"硬给 🟢
5. **输出**：JSON only，无任何前后缀文字，无 ```code fence```
