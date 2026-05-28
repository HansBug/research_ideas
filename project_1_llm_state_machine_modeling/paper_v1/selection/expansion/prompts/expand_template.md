# PATH1 候选样本 — 扩充版 NL 生成任务（严格溯源版）

你正在为我的 PATH1 sprint 实验**生成一条"扩充版自然语言需求描述"**，作为 LLM-based NL → pyfcstm DSL 生成实验的输入。这条扩充 NL 会替代 STM.md §2 的原短描述，**直接喂给 baseline (structure_event Hybrid SMF on GPT-5.5) 与 our method (agent loop on pyfcstm) 两路**做对比，所以它的质量和可信度直接决定整组实验是否能成立。

> **PATH1 评测框架（6 评测轴 = 4 主维度 + bd + ft）**：
>
> 4 主维度（5-component manual eval 对准 Apvrille 2025 baseline 自报最弱列）：
>   - **H** Hierarchical states — baseline hierarchical F1 ~0.5
>   - **G** Guards arithmetic — baseline guards F1=0.23-0.42
>   - **A** Actions non-trivial — baseline actions F1=0.00-0.34（最弱列）
>   - **F** Fault recovery / global escape
>
> 两侧综合分：
>   - **bd** Baseline-trap density — NL 里有多少 baseline 文献自报的失败模式（cross-section 信息拆段 / implicit-domain 领域术语 / implicit-action-prose 散叙述动作 / multivar-guard 多变量算术守卫 / composite-internal 复合状态自身行为 / global-cross-cutting 全局应急横切规则）
>   - **ft** pyfcstm Fit — NL 里有多少适合 pyfcstm primitive 独占优势的片段（深复合 + 非平凡 init / Expr-IR 多变量 SMT 守卫 / forced reset + per-tick aspect / effector-agnostic abstract action）
>
> 扩充 NL 的核心目的是**让原文里真实存在的 H/G/A/F 内容在 expanded_nl 里被 baseline 和我们的 method 同样能看见**，而不是为了讨好任何一方注入虚构信息。bd / ft 两侧综合分用于一段 1 句的总结性描述（说明 expanded_nl 暴露的 baseline 失败模式 & pyfcstm 独占优势 落点），**不为暴露这些而扭曲原文**。

## 硬约束 — 严格溯源、禁止无中生有

1. **expanded_nl 中的任何事实陈述都必须能在 paper.pdf 或 STM.md §1 原文摘录里找到原文支撑**。不能"看着像、应该如此、行业常识、模型一般这么做"。
2. 找不到原文支撑就**别写那一句**。宁可让扩充 NL 短一点、信息密度低一点，也绝不允许凭空发明 valve 编号、阈值数字、传感器型号、mode 名、恢复路径。
3. 每个有 substantive 信息的句子都要带 inline citation marker `[E1] [E2] [E3] ...`，并在 `provenance` 数组里给出 marker → (source_location, original_quote)。
4. 如果原文压根不支持某条评测轴（如本 case 真无 hierarchy / 真无 fault recovery / pyfcstm primitive 适用面窄），就在 `axis_coverage` 字段如实写"原文不支持，未提供 X 轴覆盖"，**不要硬编**。

## 必读上下文（请使用工具读取实际文件）

1. **STM 文件**：`{{STM_PATH}}`
   - 你要扩充的 case 在该文件的 `## 条目 N: {{CASE_NAME}}` 段落中（grep 定位 N）
   - 重点读该 case 的 §0 / §1 原文摘录 / §2 现有 NL 描述 / §3 逐句溯源
   - **§1 摘录段**已经给出 "出处：第 X 页，Figure / Table / 行号" 锚点，你的 provenance 字段可以直接引用这些锚点
2. **原文 PDF**：`{{PAPER_PDF}}`
   - 必须打开扫与本 case 相关的章节（STM §1 摘录里给了页码/行号锚点）
   - **凡是 STM §1 摘录未覆盖但你想写进 expanded_nl 的细节，必须能给出新的 PDF 页码/段落引用**
3. **辅助文本**：`{{PAPER_CONTENT}}`
   - PDF 经 pdf_extractor 提取的纯文本，可用 grep 查关键词，便于定位 PDF 段落
4. **baselines NL 风格 brief**：`{{BRIEF_BASELINES}}`
   - 6 个主力 baseline 数据集的 NL 长度 / 结构 / 细节级别调研
5. **pyfcstm grounding brief**：`{{BRIEF_PYFCSTM}}`
   - pyfcstm 4 条 primitive 各自对应的 NL 语言模式 + 硬约束（哪些数学函数 Z3 不支持等）—— 仅作 ft 评测轴的背景理解参考

## 任务定义

输出一条**单段流畅自然语言描述**，目标长度 **150-280 词（英文）**，描述该 case 的控制系统、典型流程、关键变量与守卫、硬件 effector、异常/恢复路径。每条 substantive 句子带 `[En]` 标记。

### 长度与风格基线

- baselines brief 锚点：ttool-ai coffee 90 词（下界）/ fsm-gen-iec-61499 cylinder 130 词（中段）/ structure-event-driven 估 150-300 词（上界）
- 我们 case 因含 mode hierarchy + 多 effector 略偏长，**严禁超过 300 词**
- 单段自由叙述（不分多段，不分 bullet / 标题 / markdown）；句间用 ". " 或 "; "
- 第三人称、当前时态、技术英文
- inline citation 用方括号：`The controller starts each cycle by sampling pressure PT-102 [E3] ...`

### 内容要求 — 必须忠实于原文 + 优先暴露 PATH1 4 主评测轴

1. **必须忠实于原文**：所有事实必须在 paper.pdf 或 STM §1 摘录里找到原文支撑，否则不写
2. **优先暴露 PATH1 4 主评测轴 H/G/A/F（仅在原文支持时）**：
   - **H hook (Hierarchical)**：原文若有显式 mode / sub-mode / phase / 嵌套结构，自然提及"哪个 mode 内部含哪些 phase + 进入该 mode 时默认从哪里开始"（关键 mode 名可提 1-2 个；**禁止逐个 enumerate 全部 state**）
   - **G hook (Guards arithmetic)**：原文若有数值阈值/区间/复合 guard，用**具名变量 + 自然语言复合条件**写（如 "when the pressure stays within the allowed band AND the manual override is disengaged"），**禁止伪代码**
   - **A hook (Actions non-trivial)**：原文若有 entry/exit/do action 或 transition action（变量赋值、I/O 输出、cross-cutting 监控），用自然句式描述"进入/退出某 mode 时 effector 做什么 / 每 cycle 监控什么"
   - **F hook (Fault recovery)**：原文若有 emergency / abort / safe-state / fail-safe / 全局应急路径，明确用横切句式写（如 "from any state, an emergency stop forces the system into the Safe mode"）
3. **两侧综合视角**（仅描述 NL 已有片段、不为暴露而注入）：
   - **bd 视角**：observe 在 expanded_nl 里你已写的句子有哪些恰好命中 baseline 失败模式（信息跨段/领域术语/动作散叙述/多变量守卫/复合内行为/全局横切），用一句中文综合描述
   - **ft 视角**：observe 在 expanded_nl 里你已写的句子有哪些恰好暴露 pyfcstm primitive 独占优势（深复合 init / 多变量 SMT 守卫 / forced+aspect / abstract action），用一句中文综合描述
4. **不许凭空发明**：原文没有的 Valve 编号 / 阈值数字 / forced fault path / 数学函数都不要硬加；axis_coverage 字段如实标"原文不支持"
5. **避免 Z3 不支持的数学函数**：原文用 sin/cos/log/exp 时，重述为阈值比较/查表，不要在 guard 里直接出现

### 严格禁止

1. 列出全部 state name（点名 1-2 个关键 mode 可以，但禁止逐个 enumerate）
2. 伪代码 guard（如 `if (x > 0 && y < 10)`）
3. 长 BOOL I/O 表 / 信号字典（即使原文是 PLC 案例也用自然叙述代替）
4. markdown 列表 / 标题 / 多段（必须单段）
5. 论文级长篇背景（"This system, proposed in [9], is based on ..."）
6. 用户故事风（"the user/operator wants to ..."）
7. **任何无 `[En]` 标记的 substantive 事实陈述**（背景过渡句如 "the controller manages the process by ..." 可不标，但只要带具体细节就必须标）

## 输出 strict JSON（不要 markdown 包裹）

```json
{
  "case_id": "{{CASE_ID}}",
  "case_name": "{{CASE_NAME}}",
  "expanded_nl": "<the expanded NL paragraph with inline [E1] [E2] ... citation markers, single paragraph, 150-280 English words>",
  "provenance": [
    {
      "marker": "E1",
      "source": "STM §1 摘录 A | paper.pdf p.5 §3.2 | paper_content.txt 行 240-251",
      "quote": "原文支撑句的精确引用（≤30 词），保持原文表述",
      "supports": "expanded_nl 中哪个具体短语 / 哪段事实陈述"
    },
    {"marker": "E2", "source": "...", "quote": "...", "supports": "..."}
  ],
  "axis_coverage": {
    "H_hierarchical":       "1 句中文，说明 expanded_nl 里哪段文字暴露了层次结构（关键 mode 名 + 子相位 + 默认 init），引用对应 [En] markers；如原文无 hierarchy 就写「原文无显式层次结构，未提供 H 轴覆盖」",
    "G_guards_arith":       "1 句中文，G 钩子位置 + 具名变量 + 自然语言复合条件 + 对应 [En] markers；不支持就明示",
    "A_actions_nontrivial": "1 句中文，A 钩子位置 + 进入/退出 effector 行为或 transition 动作 + 对应 [En] markers；不支持就明示",
    "F_fault_recovery":     "1 句中文，F 钩子位置 + 横切应急/safe-state 句式 + 对应 [En] markers；不支持就明示",
    "bd_baseline_traps":    "1 句中文综合描述 expanded_nl 已写的句子里哪些恰好命中 baseline 失败模式（cross-section / implicit-domain / implicit-action-prose / multivar-guard / composite-internal / global-cross-cutting，可列其中 1-3 类），引用对应 [En] markers；如基本不命中就明示「baseline 失败模式覆盖弱」",
    "ft_fcstm_fit":         "1 句中文综合描述 expanded_nl 已写的句子里哪些恰好暴露 pyfcstm 独占优势片段（深复合 init 链 / 多变量 SMT 守卫 / forced+aspect 横切 / abstract action effector 解耦，可列其中 1-3 类），引用对应 [En] markers；如适用面窄就明示「pyfcstm 独占优势覆盖弱」"
  },
  "word_count_estimate": <int 数值, 实际 expanded_nl 的 word count（计入 [E1] 等 marker）>,
  "intentional_omissions": "1-2 句中文，本来想加但原文不支持因而克制的内容"
}
```

## 评审纪律

1. **JSON only**：无 markdown 包裹，无前后缀
2. **expanded_nl 必须是单 string**（含 \n 也用 ". " 替代，保持单段流畅）
3. **每个 [En] marker 必须在 provenance 数组里有对应条目**，反之 provenance 里没用到的 marker 不写
4. **provenance.quote 必须是原文表述**（英文原文，不要翻译；如原文中文可保留中文）
5. **provenance.source 必须可追溯**：优先 "STM §1 摘录 X"（最稳）；其次 "paper.pdf p.N §X.Y"；最次 "paper_content.txt 行 N-M"
6. **不超 300 词** / **不少于 150 词**
7. **绝不发明事实**：拿不准就别写，让 expanded_nl 短一点
