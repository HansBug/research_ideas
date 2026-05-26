# Baselines NL 风格调研

> 用途：为 `path2_selection` 30 case 的"扩充版 NL"提供对照锚点。避免我们写的扩充 NL 长度 / 结构与 baseline 论文实验集偏差太大（否则不可比）。
>
> 信息源：6 个 baseline 各自的 `paper_content.txt`（必要时回到 `paper.pdf`）。包含 NL 字面摘录的来源 baseline：`structure-event-driven`（仅元信息，正文无完整 NL 字面）、`llms_emp`（dataset metadata + prompt 模板）、`fsm-gen-iec-61499`（cylinder + pick&place 完整 NL）、`req`（Volvo product function NL + Mermaid 例）、`umple`（5 个 example 的完整 bullet NL）、`ttool-ai`（coffee machine NL）。

## 总览速查

| baseline | 数据集 N | 单条 NL 长度（粗估词数） | 结构 | 典型领域 | 数值阈值 | I/O port 明确给出 |
|---|---|---|---|---|---|---|
| structure-event-driven | 8 reactive systems (Dishwasher, Chess Clock, Printer, Spa Manager, Bread Maker, Thermomix TM6, W-UMPLE, SSC7) | 无字面 NL；按 Umple ground-truth 复杂度（6-17 states, 16-41 transitions）反推约 150-300 词 | 单段非结构化叙述（论文反复强调 "non-structured NL"） | 通用家电 / reactive system 教学题 | 偶有（例：定时器秒数）但非主导 | 否 |
| llms_emp | 107 SysML 行为模型（34 STM）；7 来源（HSUV, RCCS, LRCS, MOCV, DCS, ATM, PCASS） | 无字面正文摘录；论文称遵循"requirements specification template" | 模板化分小节（role / instruction / requirements / sample / error），requirements 内含 functional 描述 + PlantUML 输出格式约束 | 工业混合（航空、轨交、IoT、制造、军事） | 部分（领域决定） | 否（focus 在 SysML 语法） |
| fsm-gen-iec-61499 | 2 详细 case study（Cylinder, Pick&Place）；无单独数据集 | Cylinder 主 NL ≈ 130 词 + I/O 表 ≈ 90 词；Pick&Place ≈ 100 词 | 多段：(1) I/O 表（信号名/方向/类型/中文释义），(2) NL 行为描述段，(3) 后续 NL 增量 patch | 工业 PLC / IEC 61499 自动化（气动缸、机械手） | 是（少量；定位、计数） | 是（明确 BOOL 信号列表） |
| req（Volvo Mermaid） | 20 primary product functions + 1000s 合成 + 12 expert test cases（windscreen wiping, mirror adjust, hood frunk, car locator…） | 单 TC ≈ 50-120 词；车定位例 NL ≈ 40 词；TC6（windscreen washing）行为约 80-120 词 | 单段简短叙述 + 少量 bullet；偶含 user-action 触发条件（"User pulls right stalk for >1 second"） | 汽车 product feature 需求（Volvo 车载） | 是（时间阈值 "> 1 second", "After 3 more wipes"） | 否（用户视角） |
| umple（Llama3） | 5 example state machines（Blackjack, Course Section, Credit Card Transaction, Driver License, Hotel Stay） | 短：3-8 条 bullet，整体 30-80 词 | **bullet list**（要求点逐条列），无 I/O 表，无伪代码 | 通用教学 / 业务流程 | 否（除"minimum/maximum number"这种符号化阈值） | 否 |
| ttool-ai | 3 European-project system specs（platooning, space-based system, automated braking）+ 教学 coffee machine | Coffee machine ≈ 90 词；正式 3 个 spec 论文未全文展开，估 100-300 词 | 单段自由叙述（"totally-free natural language"） | 嵌入式 / 系统工程（车辆编队、航天、刹车系统、咖啡机） | 是（"10 seconds to brew a coffee", "8 seconds to make a tea"） | 否（block 由 LLM 推断） |

## 各 baseline 详情

### 1. structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models

- **数据集**：8 个 reactive system scenarios，来自本科建模课程，含 Dishwasher / Chess Clock / Printer / Spa Manager / Bread Maker / Thermomix TM6 / W-UMPLE / SSC7。ground-truth 状态机规模见 paper Table I：状态 6-17，迁移 16-41，guards 4-10，actions 0-24。
- **典型 NL 长度**：论文未在正文给出 NL 字面（artifact 在 anonymous.4open.science）。按 ground-truth 复杂度反推为 1 段非结构化自由文本，**约 150-300 词**。
- **NL 结构**：明确强调 "non-structured NL system description"，无 GWT / use case / DSL，单段自由叙述。
- **细节级别**：通用家电 / 简单机械（无具体传感器型号、无 PLC 信号），含状态语义和典型用户操作，guard / action 较弱（故 actions 槽位 F1=0.0-0.16）。
- **典型例子**：原文未给字面 NL 摘录；artifact 也是匿名仓库，**无法核验**单条 NL 字面。
- **对我们的启发**：扩充 NL 应保持"自然口语化叙述 + 单段"，规模在 150-300 词；不要做 bullet list 化（会偏离他们的 "non-structured" 定义）。

### 2. llms_emp（SysML 行为模型经验研究）

- **数据集**：107 SysML 行为模型（34 STM + 36 ACT + 35 SD），来自 17 个 case，跨制造 / 轨交 / IoT / 航空 / 军事。每条配 PlantUML ground-truth + NL requirement。
- **典型 NL 长度**：论文未在正文摘录任何单条完整 NL 字面（Figure 2 是 "state machine example and its requirements" 图，paper_content.txt 仅保留 caption）。
- **NL 结构**：作者声称用了 "requirements specification template"；prompt 内 Requirements 分 3 子项（output format / output content / requirements descriptions）。即 NL 描述本身是**功能行为段**，加上 PlantUML 语法 + RAG sample。
- **细节级别**：领域是行业 SysML 案例（HSUV, MOCV 微波, ATM, 列车控制等），含较丰富的工业子系统行为，但不深入到 I/O 信号；temperature=0。
- **典型例子**：**无法从 paper_content.txt 核验单条 NL 字面**；要看 open-data resource。
- **对我们的启发**：可以确认在 SysML 工业风评测里，NL 多为"功能行为段 + 模板约束"，没有 bullet 化趋势；但因为 paper 没给字面长度，不能拿这条做硬锚点。

### 3. fsm-gen-iec-61499（fbAssistant）

- **数据集**：2 个 case study（Cylinder + Pick&Place），无独立 benchmark；正文给出完整 NL。
- **典型 NL 长度**：Cylinder 主行为 NL 约 130 词；I/O 表另含约 90 词；Pick&Place 行为段约 100 词。
- **NL 结构**：**强工业风**：(1) 单独的 I/O 信号表（信号名 / IN-OUT / BOOL / 中文释义），(2) 单段自然语言行为描述，(3) 后续以 NL patch 增量加 emergency stop 等功能。
- **细节级别**：高 —— 明确给出每个 BOOL 信号语义（home/end 是 sensor，Start/Stop 是 button，fwd/bkwd 是 actuator output），并在 NL 内直接点名 state 名（TOLEFT, ATLEFT, ATRIGHT, GO, GOBACK）和初始迁移条件（"Always"）。
- **典型例子**（≤200 词摘录）：

> When the system starts up, it initializes and makes sure the cylinder is in a known state. If the cylinder is not at home, the controller automatically moves it backward until it reaches the home position. Once at home, the cylinder waits for a user command. When the user presses "Start", the cylinder extends forward until it reaches the end position. If "Start" is pressed again, the cylinder moves backward to home. In addition to the existing states START and INIT, the resulting state machine must have states: TOLEFT, ATLEFT, ATRIGHT, GO and GOBACK. In TOLEFT cylinder moves to the home position state ATLEFT after initialisation. The condition transition from INIT to TOLEFT should be Always. In the state ATLEFT the cylinder is standing still and waiting for the Start button. … Make sure to always reset the control signals when the motion should end.

- **对我们的启发**：**这是与我们 `sources/` 控制系统 case 最接近的风格**。NL 不只是叙述，还显式包含 I/O 表 + state 命名提示。我们的扩充 NL 可以保留同样级别的 I/O 与初值约束信息，但**不要也把 state name 全部点名**（否则任务退化为"补迁移"，丢失生成挑战）。

### 4. req（Volvo Mermaid 项目）

- **数据集**：20 个 product function（来自 Volvo Car Weaver 工具）作为主数据 + 合成扩充 + 12 expert test cases。其中 TC5 = windscreen wiping, TC6 = windscreen washing, TC9 = hood frunk, TC11 = mirror adjustments 等。
- **典型 NL 长度**：单 TC 约 50-120 词；Car Locator 例摘录约 40 词。
- **NL 结构**：单段叙述，含 user-action 触发（"User pulls right stalk for >1 second"）和 timing 条件（"After 3 more wipes"）。无 I/O 表，无 state 命名提示。
- **细节级别**：用户视角，无传感器型号、无 PLC 信号，含少量自然时间阈值。
- **典型例子**（Car Locator 摘录，约 40 词）：

> The car location is presented to a remote client. One such client might be the Volvo Cars Mobile App, where both the vehicle location is presented relative to user position. User can request activation of horn and light from VOC mobile app. Car locator is not available during drive.

  TC6 windscreen washing 的 ground-truth Mermaid 含 5 states + ~9 transitions，对应 NL 估计 80-120 词。

- **对我们的启发**：偏短，且偏"用户行为描述"，不像我们 `sources/` 的工程 spec 那么硬。可作为下界（不要再短了）。

### 5. umple（Llama3 zero/one-shot/RAG）

- **数据集**：5 个 example（Blackjack, Course Section, Credit Card Transaction, Driver License, Hotel Stay）；leave-one-out 交叉。
- **典型 NL 长度**：每个 example 只有 3-8 条 bullet，整体 **30-80 词**，是 6 个 baseline 里最短的。
- **NL 结构**：**纯 bullet list**（"Requirements:" 后接 `•`），无段落，无 I/O，无 state 提示。
- **细节级别**：极简，只描述业务规则，无数值、无传感器，无 timing。
- **典型例子**（Course Section 完整 NL，约 70 词）：

> Requirements:
> - A course will initially be in the planning stage
> - Once a course is open students can request to register
> - A course needs to reach a minimum number of registered students
> - When a course exceeds its maximum number of students, the course is closed
> - If the course did not reach the minimum number of registered students, when the deadline for registration is reached the class is cancelled
> - If the course did reach the minimum number of registered students, when deadline for registration is reached the class is closed
> - The class may be cancelled at any step of this process

- **对我们的启发**：bullet 风极简，远低于我们目标 case 复杂度。**不建议向 umple 风格靠拢**（否则信息密度不够）。但可以作为"NL 长度下界" + "可读 bullet 化"参考。

### 6. ttool-ai（SysML AVATAR）

- **数据集**：教学例 = coffee machine（正文展示）；正式评测 = platooning / space-based system / automated braking，3 个 European-project use-case spec。
- **典型 NL 长度**：Coffee machine NL **约 90 词**；正式 3 个 spec 估 100-300 词（论文未全展开，仅评分）。
- **NL 结构**：单段自由叙述，作者多次强调 "totally-free natural language" 与 "knowledge-augmented" 路线。
- **细节级别**：含数值时间常数（"10 seconds to brew a coffee", "8 seconds to make a tea"），含 user-action 与 timeout 行为，但**不点名 block / state**（由 LLM 推断）。
- **典型例子**（coffee machine 完整 NL，约 90 词）：

> This coffee machine dispenses a beverage only after two coins have been deposited. If there's a substantial delay between the insertion of the first and second coins, the machine returns the initial coin. Likewise, if a beverage isn't selected promptly after the deposit of the two coins, both coins are automatically ejected. If either of the beverage buttons (tea or coffee) is pressed before the coins are ejected, the machine begins to prepare the selected drink. Notably, it takes 10 seconds to brew a coffee and 8 seconds to make a tea. Once the beverage has been collected, the machine is ready to accept new coins for the next order.

- **对我们的启发**：**与我们 sources/ 风格最接近的"短中等长度自由文本"模板**。含 timing 数值但不点 state name。建议作为我们扩充 NL 的核心锚点 —— 既比 umple 信息密度高，又不像 fsm-gen-iec-61499 那样手把手喂 state name。

## 综合启发（给 path2_selection 扩充 NL prompt 用）

1. **推荐目标 NL 长度区间：约 120-250 词**（≈ 8-15 句）。锚点：ttool-ai coffee 90 词 = 下界轻量，fsm-gen cylinder 130 词 + I/O 表 = 中等工业，structure-event-driven 估计 150-300 词 = 上界 reactive system。**不要超过 300 词**，会显著超 baseline 实验集。
2. **结构推荐：单段自由叙述为主，必要时附少量 bullet（≤5 条）或简短 I/O 提示**；不要写成 umple 风的纯 bullet（信息不足），也不要写成 IEC 61499 那种完整 BOOL 信号表（与多数 baseline 不可比）。
3. **必须保留的细节**：user action / external event 触发条件；timing 常数（"After X seconds", "if not within T"）；初始 / 错误 / 超时行为；状态语义但**不要直接点名 state**（保留生成挑战）。
4. **应避免**：(a) 列出全部 state name；(b) 给伪代码 guard；(c) 长 BOOL I/O 表（除非 case 本身就是 PLC 风）；(d) 论文级长篇背景；(e) 极短只列 3-5 条 bullet（umple 风）。
5. **领域风格保持中性**：以"自然语言系统行为说明"为主，工业控制 case 可适度引入信号名（参 fsm-gen-iec-61499），但不到 IEC 61499 那种规整度。
6. **数值阈值倾向**：每条 NL 至少含 1-2 个具体数值（时间 / 计数 / 阈值），对照 ttool-ai 和 fsm-gen-iec-61499，避免完全无数字（umple 路线）。
