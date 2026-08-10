# 14 条只能人工验收的记录 —— 逐条明细

这 14 条构成 expected issue set 的**自动化上限**：缺陷成立、可归因，但现有 19 个封闭谓词给不出可复跑的正面断言。它们**仍然是 expected issue**——入选条件是「缺陷真实且可归因」，不是「本工具当前能不能表述它」。按可表述性剔除，就会用工具能力反向定义研究边界。

正文对这批条目的成因分析与扩谓词决策见 [issue #172 §4.3–4.5](https://github.com/HansBug/research_ideas/issues/172)。

## 分布

| 维度 | 分布 |
| --- | --- |
| 元组分量 | **A** 8、**Tr** 3、**V** 2、**S** 1 |
| 缺陷方向 | `effect_action` 6、`pseudostate` 2、`guard` 2、`unclassified` 2、`reachability` 1、`entry` 1 |
| 归因层 | `nl_named` 12、`over_specification` 1、`wellformedness` 1 |

## 逐条

### EIS-0005-03 — `0005` NL10 × GPT-4o

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `effect_action` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0005-eis.md`](#file-0005-eis-md) |

**缺陷描述**

NL 第 5/6/7/8 句显式要求 timer 启停与 cooking time 的显示/更新（『where the timer starts』『stops the timer』『the cooking time is displayed and updated』『canceling or updating the cooking time』），参考模型全部以迁移 effect 承载，生成侧完全没有表达。这是 NL 显式义务的丢失，不是参考独有细化。

**NL 依据**

> NL10 四句显式点名 timer 与 cooking time 两个对象及其动作：S5 'where the cooking time is displayed and updated'、S6 'canceling or updating the cooking time'、S7 'the system transitions to the Cooking state, where the timer starts'、S8 'opening the door stops the timer'

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0007-03 — `0007` NL07 × GPT-4o

| 字段 | 值 |
| --- | --- |
| 归因层 | `over_specification` |
| 缺陷方向 | `reachability` |
| 元组分量 | **S** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | S 族全是具名点查询，无存在量词，「壳缺失」只能照搬参考名 |
| 完整台帐 | [`0007-eis.md`](#file-0007-eis-md) |

**缺陷描述**

整棵子树是 NL 完全未提及的臆造内容（信号反馈、健康检查、通信控制），且无任何入边（死代码），内部还在同一个非正交区里放了三条初始迁移（非确定初始）。属 over-specification 叠加结构缺陷。

**曾尝试的表达式（4 条，均不可求值或不判别）**

```python
# recovered_unverified — 实测 None
reaches('[*]', OperationalControls, 5)
# recovered_unverified — 实测 None
reaches('[*]', OperationalControls.FeedbackControl, 6)
# recovered_unverified — 实测 None
initial_target(OperationalControls, FeedbackControl)
# corroborating — 实测 False
reaches(source='[*]', target='llms_emp_feedback_final_0007.OperationalControls', within_cycles=5)
```

---

### EIS-0008-05 — `0008` NL04 × GPT-4o

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `pseudostate` |
| 元组分量 | **Tr** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `edge_declared` 强制要求具名 trigger，completion 边（无触发）表达不出 |
| 完整台帐 | [`0008-eis.md`](#file-0008-eis-md) |

**缺陷描述**

NL 第 7 句明确『The choice3 state also transitions to Junction3』，该直连分支缺失，闪光未充电时无路可走。与台帐 EXP-0008-TR-001 一致。

**NL 依据**

> NL 第 7 句逐字含 "The choice3 state also transitions to Junction3"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0015-01 — `0015` NL10 × GPT-4

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `effect_action` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0015-eis.md`](#file-0015-eis-md) |

**缺陷描述**

同 0005：NL 第 5/6/7/8 句显式要求 timer 启停与 cooking time 显示更新，参考以迁移 effect 承载，生成侧完全缺失。属 NL 显式义务丢失。

**NL 依据**

> NL 第 7 句逐字含 "the system transitions to the Cooking state, where the timer starts"；第 8 句逐字含 "opening the door stops the timer" 与 "if the timer expires"；第 5 句逐字含 "where the cooking time is displayed and updated"；第 6 句逐字含 "canceling or updating the cooking time"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0025-01 — `0025` NL10 × Llama

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `guard` |
| 元组分量 | **V** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | R4.5 从不把方括号解析为守卫；作者自有守卫全库为零，`guard_distinguishable` 的判别分支不可达 |
| 完整台帐 | [`0025-eis.md`](#file-0025-eis-md) |

**缺陷描述**

该边既无守卫也未在事件名中点出零时，因此在已输入烹饪时间的情形下关门仍然落到 DoorShutWithItem。NL 第 4 句把这个去向限定在『with zero time set』，其对偶义务（时间已设则不应落 DoorShutWithItem）被丢失，NL 所述『门关后去向取决于时间设定』这一依赖关系在模型中消失。这是本 case 与同构的 0015/0045/0055 唯一的实质差别。

**NL 依据**

> NL 第 4 句逐字含 "the system can transition to DoorShutWithItem if the door is closed with zero time set or to ReadytoCook if cooking time is entered"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0025-02 — `0025` NL10 × Llama

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `unclassified` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0025-eis.md`](#file-0025-eis-md) |

**缺陷描述**

同 0005/0015：NL 第 5/6/7/8 句显式要求的 timer 启停与 cooking time 显示更新完全缺失。

**NL 依据**

> NL 第 7 句逐字含 "the system transitions to the Cooking state, where the timer starts"；第 8 句逐字含 "opening the door stops the timer" 与 "if the timer expires"；第 5 句逐字含 "where the cooking time is displayed and updated"；第 6 句逐字含 "canceling or updating the cooking time"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0033-02 — `0033` NL06 × Kimi

| 字段 | 值 |
| --- | --- |
| 归因层 | `wellformedness` |
| 缺陷方向 | `entry` |
| 元组分量 | **Tr** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | 缺 `initial_edge_count` / `unique_default_entry` / `entry_is_in_scope` 一类谓词；`initial_target` 的拒答语义把整个「多默认进入点」族变成不可判定 |
| 完整台帐 | [`0033-eis.md`](#file-0033-eis-md) |

**缺陷描述**

NL 3 要求系统首先进入 PumpState。生成侧的三条初始边目标全部越出了 PumpControl 的子作用域，投影因此把它们替换成三个 Invalid 标记——PumpControl 没有任何有效的默认进入点，NL 3/4/5 描述的三个进入动作在 PumpControl 的入口处一个都无法实现。同时三条初始边并存本身也使默认进入点不唯一。

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0034-04 — `0034` NL01 × Kimi

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `effect_action` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0034-eis.md`](#file-0034-eis-md) |

**缺陷描述**

NL 第 9 句要求 Approaching 发送 'Send' 信号；NL 第 6、7 句里 Decelerate 是 'Approached/Decelerate' 迁移的效果，不是 Approaching 的状态局部动作。作者把迁移效果搬成状态 entry 动作，同时 Send 动作在全模型不存在（FCSTM 中 Approaching 只有 enter abstract Decelerate）。既丢失 NL 要求的输出动作，又把迁移效果错置为状态动作。

**NL 依据**

> NL 第 9 句逐字含 'the system sends the "Send" signal'；NL 第 6、7 句把 Decelerate 定为 'Approached/Decelerate' 迁移的效果，而非 Approaching 的状态局部动作。

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0034-05 — `0034` NL01 × Kimi

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `effect_action` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0034-eis.md`](#file-0034-eis-md) |

**缺陷描述**

NL 第 3 句要求 EmergencyStopping 既执行 'Emergency Stop' 又发送 'Obstacle Detected' 信号。作者只保留了前者，后者在全模型任何相位、任何迁移上都不存在（FCSTM 中 EmergencyStopping 只有 enter abstract EmergencyStop）。这是 NL 明确要求的输出动作彻底缺失。

**NL 依据**

> NL 第 3 句逐字含 'which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal'——两个动作都被点名，生成方只保留前者。

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0035-03 — `0035` NL10 × Kimi

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `guard` |
| 元组分量 | **V** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | R4.5 从不把方括号解析为守卫；作者自有守卫全库为零，`guard_distinguishable` 的判别分支不可达 |
| 完整台帐 | [`0035-eis.md`](#file-0035-eis-md) |

**缺陷描述**

与 0025 同形：该边既无守卫也未在事件名点出零时，已输入烹饪时间时关门仍落 DoorShutWithItem，丢失 NL 第 4 句把该去向限定于零时的义务。

**NL 依据**

> NL 第 4 句逐字含 "if the door is closed with zero time set"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0035-04 — `0035` NL10 × Kimi

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `unclassified` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0035-eis.md`](#file-0035-eis-md) |

**缺陷描述**

同组其余 case：NL 第 5/6/7/8 句显式要求的 timer 启停与 cooking time 显示更新完全缺失。

**NL 依据**

> NL 第 7 句逐字含 "the system transitions to the Cooking state, where the timer starts"；第 8 句逐字含 "opening the door stops the timer" 与 "if the timer expires"；第 5 句逐字含 "where the cooking time is displayed and updated"；第 6 句逐字含 "canceling or updating the cooking time"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0038-04 — `0038` NL04 × Kimi

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `pseudostate` |
| 元组分量 | **Tr** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `edge_declared` 强制要求具名 trigger，completion 边（无触发）表达不出 |
| 完整台帐 | [`0038-eis.md`](#file-0038-eis-md) |

**缺陷描述**

NL 第 7 句明确要求 choice3 也直连 Junction3，该分支缺失。与台帐 EXP-0038-TR-001 一致。

**NL 依据**

> NL 第 7 句逐字含 "The choice3 state also transitions to Junction3"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0045-01 — `0045` NL10 × DeepSeek

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `effect_action` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0045-eis.md`](#file-0045-eis-md) |

**缺陷描述**

同组其余 case：NL 第 5/6/7/8 句显式要求的 timer 启停与 cooking time 显示更新完全缺失，参考以迁移 effect 承载。

**NL 依据**

> NL 第 7 句逐字含 "the system transitions to the Cooking state, where the timer starts"；第 8 句逐字含 "opening the door stops the timer" 与 "if the timer expires"；第 5 句逐字含 "where the cooking time is displayed and updated"；第 6 句逐字含 "canceling or updating the cooking time"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---

### EIS-0055-01 — `0055` NL10 × Claude

| 字段 | 值 |
| --- | --- |
| 归因层 | `nl_named` |
| 缺陷方向 | `effect_action` |
| 元组分量 | **A** |
| 归因重放 | `declared_not_expressible` |
| 词表缺口 | `action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`） |
| 完整台帐 | [`0055-eis.md`](#file-0055-eis-md) |

**缺陷描述**

同组其余 case：NL 第 5/6/7/8 句显式要求的 timer 启停与 cooking time 显示更新完全缺失，参考以迁移 effect 承载。这是本 case 唯一的实质缺口。

**NL 依据**

> NL 第 7 句逐字含 "the system transitions to the Cooking state, where the timer starts"；第 8 句逐字含 "opening the door stops the timer" 与 "if the timer expires"；第 5 句逐字含 "where the cooking time is displayed and updated"；第 6 句逐字含 "canceling or updating the cooking time"

**断言组：空** —— 复核者尝试后判定 19 谓词写不出。

---
