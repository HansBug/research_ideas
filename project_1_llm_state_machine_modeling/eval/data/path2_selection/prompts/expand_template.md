# PATH2 候选样本 — 扩充版 NL 生成任务（严格溯源版）

你正在为我的 PATH2 sprint 实验**生成一条"扩充版自然语言需求描述"**，作为 LLM-based NL → pyfcstm DSL 生成实验的输入。这条扩充 NL 会替代 STM.md §2 的原短描述，**直接喂给 baseline (single-prompt) 与 our method (agent loop) 两路**做对比，所以它的质量和可信度直接决定整组实验是否能成立。

## 硬约束 — 严格溯源、禁止无中生有

1. **expanded_nl 中的任何事实陈述都必须能在 paper.pdf 或 STM.md §1 原文摘录里找到原文支撑**。不能"看着像、应该如此、行业常识、模型一般这么做"。
2. 找不到原文支撑就**别写那一句**。宁可让扩充 NL 短一点、信息密度低一点，也绝不允许凭空发明 valve 编号、阈值数字、传感器型号、mode 名、恢复路径。
3. 每个有 substantive 信息的句子都要带 inline citation marker `[E1] [E2] [E3] ...`，并在 `provenance` 数组里给出 marker → (source_location, original_quote)。
4. 如果原文压根不支持某条 C-axis 钩子（如没有 forced fault），就在 `axis_coverage` 字段如实写"原文不支持，无 C3 钩子"，**不要硬编**。

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
   - C1-C4 4 条 pyfcstm 特性各自对应的 NL 语言模式 + 硬约束（哪些数学函数 Z3 不支持等）

## 任务定义

输出一条**单段流畅自然语言描述**，目标长度 **150-280 词（英文）**，描述该 case 的控制系统、典型流程、关键变量与守卫、硬件 effector、异常/恢复路径。每条 substantive 句子带 `[En]` 标记。

### 长度与风格基线

- baselines brief 锚点：ttool-ai coffee 90 词（下界）/ fsm-gen-iec-61499 cylinder 130 词（中段）/ structure-event-driven 估 150-300 词（上界）
- 我们 case 因含 mode hierarchy + 多 effector 略偏长，**严禁超过 300 词**
- 单段自由叙述（不分多段，不分 bullet / 标题 / markdown）；句间用 ". " 或 "; "
- 第三人称、当前时态、技术英文
- inline citation 用方括号：`The controller starts each cycle by sampling pressure PT-102 [E3] ...`

### 内容要求 — 必须忠实于原文 + 仅在原文支持范围内暴露 pyfcstm grounding

1. **必须忠实于原文**：所有事实必须在 paper.pdf 或 STM §1 摘录里找到原文支撑，否则不写
2. **暴露 pyfcstm grounding hooks（仅在原文支持时）**：
   - **C1 hook**：原文若有层次/sub-mode/phase 边界，自然提及"哪个 mode 内部含哪些 phase + 进入该 mode 时默认从哪里开始"（关键 mode 名可提 1-2 个）
   - **C2 hook**：原文若有数值阈值/区间/复合 guard，用**具名变量 + 自然语言复合条件**写（如 "when the pressure stays within the allowed band AND the manual override is disengaged"），**禁止伪代码**
   - **C3 hook**：原文若有 cross-cutting 语义（"any state under emergency"、"each cycle assert safety"），明确用横切句式写
   - **C4 hook**：原文若有具名物理 effector，明确写"进入/退出某 mode 时 effector 做什么"或"每 cycle 读哪个 sensor"
3. **不许凭空发明**：原文没有的 Valve 编号 / 阈值数字 / forced fault path / 数学函数都不要硬加；axis_coverage 字段如实标"原文不支持"
4. **避免 Z3 不支持的数学函数**：原文用 sin/cos/log/exp 时，重述为阈值比较/查表，不要在 guard 里直接出现

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
    "C1": "1 句中文，说明 expanded_nl 里哪段文字暴露了 C1，引用对应 [En] markers；如原文不支持就写「原文无层次结构，未提供 C1 钩子」",
    "C2": "1 句中文，C2 钩子位置 + 具体变量/阈值 + 对应 [En] markers；不支持就明示",
    "C3": "1 句中文，C3 钩子位置 + 横切语义 + 对应 [En] markers；不支持就明示",
    "C4": "1 句中文，C4 钩子位置 + 物理 effector + 对应 [En] markers；不支持就明示"
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
