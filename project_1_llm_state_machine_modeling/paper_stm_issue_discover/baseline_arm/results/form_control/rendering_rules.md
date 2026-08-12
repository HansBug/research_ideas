# x1-form-control · 渲染规则与保真性凭据（渲染组 D1）

本文件是 [rendered/](./rendered/) 下 120 段散文的**唯一可审计凭据**：它固定了渲染规则、给出 3 条逐字对照、并如实登记保真性风险与设计漏洞。⛔ 本文件与 `rendered/` 下的任何文件都不含判定结果。

## 一、任务与口径

把主臂（feedback-loop discover，v46）在 120 个命中位上的发现，**只换形态、不换内容**地渲染成自由文本散文，形态与基线臂产出同构（`issue` / `where` / `reason` 三段）。⭐ 判据是：读渲染版的人与读原版的人应当能指出**同一处**模型缺陷。

### 1.1 样本来源

复用 M1 组的 120 个位（`runs/paper1/x1-actionable/verdicts/M1.json` 的 `positions` 键集合），抽样口径原样继承 M1 的 `sampling` 字段：总体为 v46 的 355 个 REPORTABLE `hit@1` 位，按每条记录在其 6 位上的命中位数分池（`full6` / `near45` / `unstable13`），最大余数法等比分配，`random.Random(20260812).sample` 逐池抽取，`full6:75 / near45:31 / unstable13:14`。

材料来源目录同样继承 M1 已查实的两条事实：pair `{0000,0010,0020,0030,0040,0050}` 读 `runs/paper1/matrix-v46r`，其余 48 个 pair 读 `runs/paper1/matrix-v46-full`（`discover_matrix/apply_v46r.py` 把前 6 个 pair 整块替换成了 v46r，读 `-full` 会拿到与判定表对不上的 issue）；被测制品是 `selected_seed_examples/<pair>/model.fcstm`，⛔ 不是 `stm0.puml`。

### 1.2 渲染源文本 = 该位对应 issue 的 `title` + `rationale`

⭐ 这与 M1 判定所读的文本**逐字相同**——M1 每个位的 `note` 都写明「判据只读该 issue 的 title + rationale 所述命题」。因此渲染的输入与被判的输入是同一段文字，形态实验没有换掉底稿。

由此导出两条：`shared_root_cause` 与 `shared_elements` 字段**不参与渲染**（它们不在 M1 判读的文本内）；`released_assertion_results` 的 `terminal_expression` / `truth_value` / `function_call_trace` 也不参与渲染（它们正是本任务要求剥离的机器痕迹）。

一处例外须记录：`EIS-0032-02|run3/0032-gpt` 的 M1 `note` 里没有 issue id（反引号里是路径 `…0032.Operate`）。M1 的 `quote` 与 `ISSUE-accelerating-or-cruising-not-under-operate` 的 `rationale` **逐字相同**，据此绑定到该 issue。M1 的 note 另说该位的 argument 覆盖三条同族 issue，但被引用的那段文字只对应上述一条，故只渲染这一条。

## 二、写死的渲染规则

### R0 — 形态：三段，不增段不减段

- `issue`：一句话说「不符是什么」，由原文 `title` 改写。
- `where`：说「涉及模型的哪些元素」，只能由 `rationale`（与 `title`）中**已经出现**的元素指称重排而来。
- `reason`：说「为什么算不符」——规范要求什么、模型实际是什么、差在哪；原文若给了修法建议，照抄成自然语言（基线臂的 `reason` 段同样含修法议论，保留才同构）。

⚠️ 三段之间只做**版面重排**，不做内容增删。原文没有的元素指称，`where` 段不得凭空补。

### R1 — 谓词名一律消去，改写为它所断言的关系

固定对照表（只换措辞，不改断言内容）：

| 原谓词 | 渲染成 |
|---|---|
| `state_declared(X, kind=any)` | 模型里没有／有名为 X 的状态 |
| `state_declared(X, kind=composite)` | X 不是一个含子状态的复合状态（是个叶状态） |
| `containment(parent=P, child=C)` | C 不在 P 之下／未被声明为 P 的子状态 |
| `cardinality(scope=S, count=n)` | S 的直接（非伪）子状态不是 n 个 |
| `initial_target(composite=C, child=X)` | 进入 C 时默认落到的不是 X |
| `occupancy_after(src,trig,tgt,within_cycles=k)` | 在 src 收到 trig 后（k 个周期内）系统并没有到达／占据 tgt |
| `event_consumed(src,trig)` | src 处并没有把 trig 当作触发消耗掉 |
| `event_declared` / `variable_declared` | 模型没有声明名为 X 的事件／变量 |
| `action_declared(state, phase)` | X 上没有声明进入时／停留期间／退出时的动作 |
| `effect_declared(src,trig,var,sign)` | 该转移的效应里没有让变量 v 变小／变大 |
| `edge_declared(src,trig,tgt)` | 模型里没有这条从…到…、由…触发的边 |
| `terminates(scope,trig)` | 在 scope 中收到 trig 并不会让运行终止 |
| `reaches(src,tgt,within_cycles=k)` | 从 src 出发在 k 个周期内到不了 tgt |
| `guard_distinguishable(src,trig)` | 同一触发下的两条去向没有互不重叠的守卫可以区分 |
| `persists_until(state,release,bound=b)` | X 并不会一直停留到「release」为止（b 步界内） |
| `any([...])` | 这几个当中的任何一个都不是 |

### R2 — 路径自然语言化，但标识符逐字保留

模型根段（`llms_emp_feedback_final_XXXX`）渲染为「模型顶层」；其余每一段**照抄原标识符**，用「…里的…」连接。⛔ 不做名称纠正、不做拼写修复：原文引用的名字若在模型中并不存在，仍照抄该名字。

例：`llms_emp_feedback_final_0032.Operate` → 「模型顶层名为 Operate 的状态」，⛔ 不得改写成 `OperateState`。这条是硬的——纠正名字会翻转命题真值，把原判定要面对的可定位性问题擦掉。

### R3 — 真值标记删除，改写为直陈句

`= False`、「为 False」、「返回 false」、「判假」、「探针都为假」→ 直接写「模型没有…」「并没有…」。⛔ 渲染文本中不得出现 True／False 字样，也不得出现「断言」「谓词」「检查结果」「已发布结果」这类判定机器措辞。原文里为真的旁证（如「这条边确实声明了」）保留其**极性**，只去掉真值词。

### R4 — 需求条目编号删除，用它要求的内容顶替

`REQ-xxx`、`NL-Lxxx`、`NL-Mxxx`、`AST-xxx-n` 一律去掉。原文若在同句给出了该需求要求什么，就用那句内容顶替（写成「规范要求…」）。⭐ 原文若引了规范的英文原句（如 `"where the timer starts"`、`"The door can be closed to return to the DoorShut state"`），**保留该英文原句**——它是规范内容，不是编号。原文若只给编号未给内容，写「规范中的相关要求」并登记为风险（本批 120 位中未出现此情形）。

### R5 — 主臂管线内部词汇删除；承载实质的改写为普通话

`released result`／`已发布结果`／`stm_text`／`declared_model_vocabulary`／`excluded_observations`／`representation_debt`／`primary`／`supporting`／`precondition`／`transition:N`／`AST-…-n` 等一律去掉。其中承载实质主张的两类改写而非删除：

- 「归因为 safe」→「这一处可以直接归到模型本身」（它是一条关于缺陷归属的实质主张，删掉是内容损失）。
- 「前置为 False 因而行为断言被阻塞」→「因为这个前提不成立，随后那条行为主张也就无从谈起」（保留因果链，去掉机器词）。

### R6 — 转换器／编译器插入物的名字保留

`UnspecifiedInitial`、`InvalidInitialtr_*`、`FinalWaittr_0005`、`R45RouteToken` 是 `model.fcstm` 中真实存在的元素名，⭐ 照抄，并保留原文对它们「由转换器／编译器注入」的说明。删掉它们等于删掉被审模型的一部分。

### R7 — 模型源码片段允许保留

`[*] -> FinalState : /Power_Off`、`HumanDriving -> AutonomousFinal : /Power_Off` 这类是**模型文本摘录**，不是断言表达式；基线判定材料的 `where` 段同样逐字引模型源片段（如 `[*] --> Off : keyOff`），保留才同构。

### R8 — 不许增补

⛔ 渲染时不查 `model.fcstm`、不查 `stm0.puml`、不查 NL 原文、不查 `sketch`／`shared_elements` 来补原文没说的东西。渲染只能是原文的重写。

**执行中触发过 R8 的两处**：`EIS-0005-03|run1/0005-gpt` 的 `sketch` 写着 `state="DoorOpenWithItem.ReadytoCook"`，但 `rationale` 只说「ReadytoCook」——渲染保持「ReadytoCook」，不补父路径。`EIS-0053-01|run1/0053-claude` 的 `sketch` 写着 `PumpControl.PumpRegion.PumpState`，`rationale` 只说「PumpState」——渲染保持「PumpState」，不补 region 层。

## 三、3 条逐字对照（原文 → 渲染后）

### 对照 1 · `EIS-0000-01|run2/0000-gpt`（触发 R1/R3/R4/R7）

**原文 title**

> Power_Off 到 FinalState 的转移声明在初始化入口而非运行模式上

**原文 rationale**

> REQ-006 和 REQ-006C 分别要求系统在 HumanDrivingMode 与 AutonomousMode 中运行时，Power_Off 后一周期内进入 FinalState；两个主断言均为 False。模型将 Power_Off 到 FinalState 的边声明为 [*] -> FinalState : /Power_Off，而不是从 HumanDrivingMode 或 AutonomousMode 运行源触发，因此运行中 power off 响应不能从任一模式到达 FinalState。

**渲染后**

> **Power_Off 到 FinalState 的这条转移被挂在了初始化入口上，而不是挂在运行模式上。**
>
> - **where**：从初始伪状态出发、以 Power_Off 为触发、指向 FinalState 的那条边 `[*] -> FinalState : /Power_Off`；以及本该作为它源头的两个运行模式 HumanDrivingMode 与 AutonomousMode。
> - **reason**：规范分别要求系统在 HumanDrivingMode 中运行时、以及在 AutonomousMode 中运行时，收到 Power_Off 后一个周期内进入 FinalState，这两条要求模型都没有做到。模型把 Power_Off 到 FinalState 的边写成了从初始化入口出发的 `[*] -> FinalState : /Power_Off`，而不是从 HumanDrivingMode 或 AutonomousMode 这两个运行源触发，所以运行当中的 power off 响应无法从这两个模式中的任何一个到达 FinalState。

**逐项核对**：`REQ-006`/`REQ-006C` 两个编号去掉、内容（两个模式各一条、一周期内、进入 FinalState）全留；「两个主断言均为 False」去掉真值词，改成「这两条要求模型都没有做到」；模型源片段 `[*] -> FinalState : /Power_Off` 逐字保留；元素 HumanDrivingMode、AutonomousMode、FinalState、Power_Off 全留；`where` 段的内容全部来自原 rationale，无新增。

### 对照 2 · `EIS-0032-02|run3/0032-claude`（触发 R1/R2/R3/R4）

**原文 title**

> IdleState 未作为 OperateState 的直接子状态（被包裹在 IdleRegion 中）

**原文 rationale**

> NL-L001/NL-L003 将 Idle 列为 Operate 的直接子状态。模型将 IdleState 声明在中间层 IdleRegion 之内，导致 containment(OperateState, IdleState) 为假。需要将 IdleState 提升为 Operate 的直接子状态，或移除多余的 IdleRegion 层级。

**渲染后**

> **IdleState 没有作为 OperateState 的直接子状态，它被包裹在 IdleRegion 中。**
>
> - **where**：OperateState、它里面的 IdleRegion 这一中间层、以及被放在该层之内的 IdleState。
> - **reason**：规范把 Idle 列为 Operate 的直接子状态。模型将 IdleState 声明在中间层 IdleRegion 之内，导致 IdleState 并不是 OperateState 的直接子状态。需要将 IdleState 提升为 Operate 的直接子状态，或移除多余的 IdleRegion 层级。

**逐项核对**：`NL-L001/NL-L003` 去掉、其内容（Idle 是 Operate 的直接子状态）全留；`containment(OperateState, IdleState) 为假` → 「IdleState 并不是 OperateState 的直接子状态」，谓词名与真值词同时消去、关系不变；原文区分的三个名字 `Idle`／`IdleState`／`OperateState`／`Operate` 全部按原样保留，⛔ 未做统一化；修法建议（提升或移除层级）照抄。

### 对照 3 · `EIS-0032-02|run3/0032-gpt`（触发 R2 的硬约束：⛔ 不许纠正不存在的名字）

**原文 title**

> Accelerating or Cruising 未作为 Operate 的子状态声明

**原文 rationale**

> REQ-004 要求 NL 命名的 Accelerating or Cruising 作为 NL 父级 Operate 的子状态。released containment 检查为 False，说明模型没有声明 parent=llms_emp_feedback_final_0032.Operate、child=llms_emp_feedback_final_0032.OperateState.Accelerating_or_Cruising 的包含关系。

**渲染后**

> **规范里叫 Accelerating or Cruising 的那个状态没有被声明为 Operate 的子状态。**
>
> - **where**：作为父的、模型顶层名为 Operate 的状态；以及作为子的、OperateState 里名为 Accelerating_or_Cruising 的状态。
> - **reason**：规范要求它在自然语言里命名的 Accelerating or Cruising 作为自然语言里的父级 Operate 的子状态。模型没有声明这样一层包含关系：以模型顶层的 Operate 为父、以 OperateState 下的 Accelerating_or_Cruising 为子的包含关系，在模型里不存在。

**逐项核对**：`REQ-004` 去掉、内容全留；`released containment 检查为 False` → 「模型没有声明这样一层包含关系」；`llms_emp_feedback_final_0032.Operate` → 「模型顶层名为 Operate 的状态」，⭐ 名字 `Operate` 逐字保留、**层级位置（模型顶层）也保留**；`llms_emp_feedback_final_0032.OperateState.Accelerating_or_Cruising` → 「OperateState 里名为 Accelerating_or_Cruising 的状态」，同样逐字保留。⭐ 这一位是 R2 硬约束的检验点：把 `Operate` 顺手改成模型里真实存在的 `OperateState`，会让这条主张从「锚点在模型里查不到」变成「锚点存在且关系为真」，直接翻转命题——渲染没有这么做。

## 四、机械核查

对 120 段渲染文本跑了残留扫描，结果为 0：

- 谓词名（`state_declared` / `containment` / `cardinality` / `initial_target` / `occupancy_after` / `event_consumed` / `event_declared` / `variable_declared` / `action_declared` / `effect_declared` / `edge_declared` / `terminates` / `reaches` / `guard_distinguishable` / `persists_until`）：0 命中。
- 真值与判定机器词（`False` / `True` / 「为假」/「判假」/「返回 false」/「断言」/「谓词」）：0 命中。
- 编号与内部句柄（`REQ-` / `NL-L` / `NL-M` / `AST-` / `llms_emp_feedback_final_` / `truth_value` / `terminal_expression` / `function_call_trace` / `within_cycles` / `scope=` / `parent=` / `child=` / `source=` / `target=` / `trigger=`）：0 命中。
- 台账与实验标识（`EIS-` / `hit@` / `v46` / `discover`）：正文 0 命中（位键出现在每节标题里，这是任务要求的「一节含位键」，与基线判定材料把台账记录号写在 §三 的做法一致）。

篇幅口径（字符数中位数）：

| 段 | 基线臂（n=1147） | 本次渲染（n=120） |
|---|---|---|
| `issue` | 51 | 39 |
| `where` | 50 | 84 |
| `reason` | 129 | 168 |
| 三段合计 | 240 | 303 |

逐位「渲染字数 / 原文（title+rationale）字数」中位数 1.16，区间 0.54–1.77。

## 五、保真性风险自评（⛔ 如实登记；⭐ 分析时应单独标注这些位）

### 5.1 位级风险

| 位 | 风险 | 说明 |
|---|---|---|
| `EIS-0057-01\|run1/0057-claude` | **解读性改写** | 原文「三次 initial_target 探针都为假」。渲染为「就这三个区域逐个核对，结论一致」——把「三次」读成「三个区域各一次」。若原意是「三轮运行」，这是误读。⚠️ 这是全批唯一一处我对原文语义做了判断而非转写。 |
| `EIS-0030-03\|run2/0030-claude` | **机器词密集段落的意译** | 原文「该 Requirement 的证据因 representation_debt/unattributed 被路由到 excluded_observations」渲染为「那条要求本身因为表示债务、无法归到模型头上而被单独排除在外」。语义应当等价，但这是意译不是转写。 |
| `EIS-0040-03\|run1/0040-gpt` | 同上 | 原文「另一 primary 断言为 unattributed，已作为排除发现记录」→「那一处无法归因，已作为排除的发现记录，不在此处主张之内」。 |
| `EIS-0034-06\|run1/0034-claude` | **量词口径** | 原文 `bound=4`，渲染为「4 步界内」。`bound` 的单位（步／周期）在原文中未言明，我按「步」写。 |
| `EIS-0010-04\|run1/0010-claude` | 量词保留 | 原文 `within_cycles=5` 出现在 rationale 内，渲染保留「5 个周期内」。⭐ 无损，登记备查。 |
| `EIS-0012-01\|run3/0012-claude` | **保留了正极性真值** | 原文「AST-REQ-001-2 的 edge_declared 为真」被渲染为「这条边确实存在」。R3 要求去掉真值词，但这里的正极性是论证的实质（边存在却不生效），删掉会损失内容，故保留极性、只去词。 |
| `EIS-0009-03\|run3/0009-claude`、`EIS-0030-01\|run3/0030-claude`、`EIS-0049-02\|run2/0049-claude` | **阻塞链改写** | 三处都含「前置断言 False → 行为断言被阻塞未执行」的链条，渲染为「前提不成立 → 那条行为主张无从谈起」。因果保留，但「未执行」这一运行事实被弱化成了「无从谈起」。 |

### 5.2 `where` 段偏薄的位（原文本身就薄，非渲染造成）

原文 rationale 只点了一个元素、`where` 段无从丰富的位：`EIS-0005-03|run1/0005-gpt`、`EIS-0010-02|run2/0010-gpt`、`EIS-0014-01|run3/0014-gpt`、`EIS-0020-01|run1/0020-gpt`、`EIS-0025-02|run2/0025-gpt`、`EIS-0025-02|run3/0025-gpt`、`EIS-0026-02|run2/0026-gpt`、`EIS-0035-04|run1/0035-gpt`、`EIS-0042-01|run3/0042-gpt`、`EIS-0055-01|run2/0055-gpt`、`EIS-0056-02|run1/0056-gpt`。⚠️ 这些位的 `where` 段与基线臂典型 `where` 段（中位 50 字）体量相当甚至更短，若它们判定结果偏低，⛔ 不能归因为形态。

### 5.3 渲染文本完全相同的 5 组位（10 个位）

同一条 issue 被两条台账记录各占一个位，渲染文本因此逐字相同：

- `EIS-0002-01|run3/0002-claude` 与 `EIS-0002-03|run3/0002-claude`
- `EIS-0016-01|run1/0016-claude` 与 `EIS-0016-03|run1/0016-claude`
- `EIS-0024-02|run3/0024-gpt` 与 `EIS-0024-03|run3/0024-gpt`
- `EIS-0034-01|run1/0034-claude` 与 `EIS-0034-02|run1/0034-claude`
- `EIS-0034-01|run2/0034-claude` 与 `EIS-0034-06|run2/0034-claude`

⚠️ 这忠实于原始产出（原文本来就是同一条 issue），但意味着这 5 组内部的判定差异只能来自台账那一侧，不能来自文本。

### 5.4 规则层的系统性损失（全批适用）

1. **谓词身份不可恢复。** R1 保留了每个谓词所断言的**关系语义**，但读者无法再区分它用的是 `occupancy_after`（k 周期内占据）、`reaches`（可达）还是 `terminates`（UML 终止语义）——我用中文措辞尽量区分，但这三者的形式差别已不在文本里。⭐ 这是整个任务里最深的一条形态／内容边界：谓词名是形态，谓词语义是内容，我按「保语义、弃名字」处理，但边界不可能划得绝对干净。
2. **需求编号不可恢复。** 原文用编号区分「这是第几条要求」；渲染改用内容指称。凡原文以编号做**枚举计数**的地方（如「同时解决 REQ-006/007/008 的 containment、REQ-009 的复合声明、…」），我保留了计数（「同时解决七处失败：三条包含关系、复合声明、…」），但读者无法回指到具体需求条目。
3. **`shared_root_cause` / `shared_elements` 未进入渲染**（理由见 §1.2）。若判定方认为主臂发现应包含这两个字段，那本材料相对主臂真实产出是偏薄的——⭐ 但它与 M1 判读的文本一致。
4. **三段式布局本身可能不是中性的**（详见 §6.4）。

## 六、我认为这个对照设计的漏洞

⛔ 以下四条按严重性排序，第 1、2 条我认为足以影响结论是否成立。

### 6.1 【最重】样本全是命中位，形态效应在关心的方向上不可测

120 个位全部取自主臂的 **REPORTABLE `hit@1` 命中位**。这些位在原判定下已经是「命中」，重判只能持平或下降，⛔ **命中率不可能上升**。而任务给出的判据是「若命中率上升，形态效应就被直接量出来了」——这个判据在本样本上无法被满足，不是因为形态无效应，而是因为已经封顶。

若「判定对散文更宽松」这个假设为真，它应当表现为：主臂那些**当前判为未命中**的发现，换成散文后被判成命中。⭐ 那批位一个都不在样本里。所以本设计能测的只有**形态导致的损失**（散文化之后反而认不出来了），测不到**形态导致的增益**——而后者才是解释「基线数字更高」所需要的量。

**建议**：要测想测的东西，样本必须包含主臂的未命中位（`hit@1` 为否的位，尤其是 `hit@3=0` 的 `zero0` 池——M1 的 `sampling` 显示该池有 23 条记录、0 个命中位，被整体排除在总体之外）。可以保留现有 120 位作为「形态损失」的对照臂，另抽一批未命中位作为「形态增益」的主臂。

### 6.2 【重】判定底稿不同：主臂看 `model.fcstm`，基线判定材料要求看 `stm0.puml`

基线判定材料在抬头明确写「判定时读下面的 PlantUML 作者源，⛔ 不读 `model.fcstm`（编译产物）——否则会把编译债务当成模型缺陷」。而主臂的发现全部是对 `model.fcstm` 做出的。

⛔ 如果下一组拿 PlantUML 源来判本材料，**120 位中有 23 位**会立刻遇到指称不上的元素——它们提到了只存在于 `model.fcstm` 的转换产物：`UnspecifiedInitial`（13 位）、`R45RouteToken`（6 位）、`FinalWaittr_0005`（3 位）、`InvalidInitialtr_*`（2 位）（有重叠）。完整名单：

`EIS-0006-02|run3/0006-claude`、`EIS-0007-02|run3/0007-claude`、`EIS-0007-03|run2/0007-claude`、`EIS-0009-03|run2/0009-claude`、`EIS-0019-02|run1/0019-claude`、`EIS-0019-02|run2/0019-gpt`、`EIS-0019-02|run3/0019-claude`、`EIS-0029-04|run2/0029-claude`、`EIS-0030-01|run3/0030-claude`、`EIS-0033-01|run1/0033-claude`、`EIS-0033-01|run2/0033-claude`、`EIS-0035-01|run1/0035-gpt`、`EIS-0035-01|run2/0035-claude`、`EIS-0044-01|run1/0044-claude`、`EIS-0044-01|run1/0044-gpt`、`EIS-0044-01|run2/0044-gpt`、`EIS-0047-02|run1/0047-claude`、`EIS-0050-01|run1/0050-gpt`、`EIS-0050-01|run2/0050-gpt`、`EIS-0050-01|run3/0050-claude`、`EIS-0053-01|run1/0053-claude`、`EIS-0057-01|run1/0057-claude`、`EIS-0057-01|run2/0057-gpt`。

更普遍的问题是层级：M1 已记录 `model.fcstm` 与 `stm0.puml` 的层级不同（例如 0005 的 `ReadytoCook`/`Cooking` 在 puml 里是顶层，在 fcstm 里是 `DoorOpenWithItem.ReadytoCook.Cooking`）。⚠️ **底稿一换，本材料测到的就不是形态效应，而是底稿效应。** 每个 `rendered/<pair>.md` 的抬头已写死这条警告，但它是流程约束、不是技术保证。

### 6.3 【中】篇幅与完备度不是同一个变量，本设计把两者一起换了

「只有形态变了」这句话在字面上不成立：渲染后的 `where` 段中位 84 字，基线臂中位 50 字；三段合计 303 对 240。散文化本身没有加信息（§四已核），但**主臂的 rationale 原本就比基线的 reason 长**（原文中位 256 字）。所以本对照实际比较的是「长散文 vs 短散文」，不是「结构化 vs 散文」的净效应。⭐ 若结果显示渲染版判得更高，⛔ 不能排除是篇幅／完备度而非形态在起作用。

**建议**：至少把篇幅作为协变量记录下来（逐位字数已可从本材料算出），或者补一个「压缩到基线篇幅」的第二渲染臂。

### 6.4 【中】三段式布局本身可能是一次干预，不是中性重排

主臂的原始产出没有独立的 `where` 字段——元素指称散落在 `rationale` 的行文里。我按 R0 把它们**抽出来集中放进 `where` 段**。这一步在「不增信息」的意义上是保真的，但在「可读性／可定位性」的意义上未必中性：把散落的指称聚成一段，本身就可能让判定者更容易定位。

⚠️ 也就是说，若渲染版判得更高，可能是三段式**版面**的功劳，而不是「散文 vs 结构化」的功劳。这两者在本设计里被绑在一起了。

**建议**：如果要把「形态」这个变量切干净，应当再做一个「单段连续散文、不拆 where」的第三臂；本批 120 位的 `issue`+`where`+`reason` 已经足以机械地合并成单段，成本不高。

### 6.5 【低】渲染者非盲

我在渲染时知道每个位属于主臂、知道它们全是命中位（虽然⛔ 没有读 M1 的逐位判定字段，除了绑定 issue 所必需的 `note`）。⚠️ 无意识的「帮忙写清楚」无法从流程上排除；§三的三条逐字对照与 §四的机械核查是我能提供的全部对冲，⛔ 它们证不了不存在偏向。若要更硬，应由第三方按本文件的规则复渲染一个随机子集（比如 20 位）做一致性比对。
