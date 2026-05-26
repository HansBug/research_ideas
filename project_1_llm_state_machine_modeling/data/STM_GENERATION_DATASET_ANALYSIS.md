# NL→STM 生成任务的数据集学术分析

> **这是什么**：本文站在 `project_1`（控制系统 LLM 状态机建模）的学术角度，对 [`data/`](./README.md) 下 4 个公开数据集的**自然语言输入特征**做实证分析，提炼出"能担任 STM generation 任务的数据集应满足的硬要求"，再回头评估 4 个数据集对这些要求的满足情况，最后给出**对 `project_1` 自家数据集（[`../sources/`](../sources/)）建设的启示**。
>
> **方法**：所有数字与样例都来自 `data/<paper>/simple.parquet` 真实抽样（不是从论文叙事抽象概括），统计代码可参见 [`scripts/_build_simple_parquet.py`](./scripts/_build_simple_parquet.py)。

---

## 1. 学术坐标：什么是 NL→STM generation？

`project_1` 关心的任务可以严格写作：

$$
f_{\text{LLM}}: \mathrm{Req}_{\text{NL}} \;\longrightarrow\; M = (S, S_0, E, V, C, \mathit{Tr}, \mathrm{Inv}, \mathrm{Act})
$$

其中 $\mathrm{Req}_{\text{NL}}$ 是非形式化需求文本，$M$ 是状态机族模型（含状态、迁移、事件、变量、时钟、不变式、动作）。一个**真正可信**的 STM generation benchmark，不是"NL 进去、文本出来"那么简单：它必须能让评估者**就地**回答以下学术问题：

1. **任务真实性**：输入是不是真自由文本？还是已经被作者形式化预处理过的伪代码？
2. **输出表达力**：reference STM 是否覆盖 layered / concurrent / guarded / timed / hierarchical-history 等 control system 软件常见结构？
3. **领域对齐**：样本是否来自控制系统软件（汽车 / 航空 / 工业自动化 / 安全关键），还是用家电 / 教学例子充数？
4. **可比性**：是否同时公开 input + reference + prediction，让多个方法在同样输入上对照？
5. **样本规模与多样性**：是否只够 toy demo？还是足以做统计稳健的对照？
6. **评测维度多样**：是否只有 F1，还是同时有时间约束保留率 / 层次结构正确率 / 安全性质保留率等控制系统专门维度？

下面 §2 实证看 4 个数据集在这些维度上长什么样。

---

## 2. 4 个数据集的 NL 输入实证特征

### 2.1 量化对照表（统计来自所有 simple.parquet 的唯一 input）

| 维度 | `llms_emp` | `ttool_ai` | `light_control_nimbus` | `structure_event_driven` |
|------|:----------:|:----------:|:----------------------:|:------------------------:|
| **唯一 input 数** | 30 | **3** | 4 | 8 |
| **input median 字符** | 1109 | **2132** | 730 | 1838 |
| **input median 单词** | 163 | **359** | 136 | 327 |
| **expected median 字符** | 543 | _无 reference_ | 524 | **1203** |
| **time 词频 / 100 词** | 0.76 | 0.87 | **3.91** ⭐ | 2.73 |
| **state 词频 / 100 词** | **4.09** ⭐ | 1.13 | 2.98 | 2.86 |
| **hierarchical 词频 / 100 词** | 0.23 | 0.09 | 0 | 0 |
| **control-system 词频 / 100 词** | 1.75 | **1.39** | 0.37 | 0.26 |

> **time** 模式：`after / within / before / every / seconds / minutes / hours / delay / timeout / T1-T3 / periodic / cycle`
> **state** 模式：`state / mode / status / phase / when / while / if / trigger / transition / event / activate`
> **hierarchical** 模式：`parallel / concurrent / hierarchical / sub-state / nested / composite / orthogonal`
> **control-system** 模式：`sensor / actuator / controller / safety / fault / brake / emergency / threshold / signal / interrupt / firmware / protocol / critical`

**3 个非平凡的发现**：

1. **没有任何一个数据集的 NL 输入显式提到层次/平行结构**（`hierarchical` 词频几乎全 0）。但输出里 `structure_event_driven` 至少 5 个 case 有 `hierarchical_states` ≥ 1，`light_control_nimbus` 输出有平行 region。**这是 STM generation 真正的 LLM 难点：从扁平 NL 推断层次。**
2. **时间约束密度由 `light_control_nimbus`（3.91）领先**，超过 ttool-ai（0.87）—— 但 ttool-ai 的输出 parquet 含 `after_min/after_max` 时间字段。也就是 ttool-ai 的"时间语义"是从 system spec 描述里**隐式**抽出来的，而 `light_control_nimbus` 是 NL 里**显式**写明 `T1 minutes`。
3. **领域分布**：`llms_emp`（1.75）+ `ttool_ai`（1.39）是控制系统相关；`light_control_nimbus`（0.37 building automation）和 `structure_event_driven`（0.26 家电/办公）远离工业控制系统。

### 2.2 各数据集的 NL 风格定性分析

#### `llms_emp` — "教学化伪代码"风格

```
1 The human driving mode is represented by a simple state.
2 The autonomous mode has sub-states and is represented by a sub machine state.
3. when power on, the system turn into human driving mode
4 when front_distance > 10, auto transport to autonomous state
5 when power off, it will transit to final state
```

**学术评估**：

- 优势：30 个唯一输入是 4 个数据集中**最多**；状态术语显式（`state`/`sub-state`/`transit`）；同时有 6 个 LLM 的 192 行人评 → 可做严格 1:1 对齐 benchmark。
- 隐忧：作者已经把状态机的**结构**写进了 NL 里（"is represented by a simple state" / "has sub-states"）—— 这让 LLM 任务退化为"近义句改写 + 形式化语法填充"，而不是"从需求**推断**状态机结构"。
- 后果：在这种 NL 上跑出的高 F1 **未必能外推**到真实控制系统需求文档（那里没人会写"this is a state"）。

#### `ttool_ai` — "真实工业 system spec"风格

```
Platooning is a transportation technique that consists in grouping trucks or vehicles
together to reduce CO2 emissions. A platoon consists of one or several vehicles, the
first one in the platoon playing the role of the platoon leader, ...

1. A vehicle can create a platoon: this vehicle is then the leader of this platoon.
   This vehicle informs neighbour cars about this platoon by sending a platoon
   information message (position, speed, acceleration) every second. ...
```

**学术评估**：

- 优势：来自 3 个**真实欧洲项目**的工业级规范文档（车辆编队 / 空间系统 / 自动刹车）—— **任务真实性最强**；输出含 `after_min/after_max/probability` 时间自动机字段，是 4 个数据集里**唯一直接对接控制系统时间语义**的。
- 隐忧：仅 3 个 case，**完全不够做统计稳健 benchmark**；论文未公开 reference STM（只有 LLM-generated AVATAR 模型 + 人工评分）—— 没法做严格 input-ref-pred 对齐。
- 后果：能作为"工业现实性 demonstration"，但作为标准 benchmark 数据量太少。

#### `light_control_nimbus` — "Dagstuhl reference problem"风格

```
U1: If a person occupies a room, the light has to be sufficient to move safely.
U3: If the room is reoccupied within T1 minutes after the last person has left
    the room, the last chosen light scene has to be reestablished.
U4: If the room is reoccupied after more than T1 minutes since the last person
    has left the room, the standard light scene has to be established.
U11: If the outdoor light sensor or the motion detector of a room does not work
     correctly, ...
```

**学术评估**：

- 优势：U1-U12 编号 + 时间常量 `T1` + 故障模式 FM1-FM8 —— **结构化与时间语义最齐全**；输出端自带平行 region（`Chosen_Light_Scene` / `Failure_Modes`）+ 层次状态。
- 隐忧：仅 4 个重建片段；非 LLM 工作（论文是 2000 年），**没有 prediction**；领域是建筑/IoT 控制（不是机械/汽车控制系统）。
- 后果：作为**方法学样本**（HSM + 时间约束 + V&V 流程）有教科书价值；作为 LLM benchmark 不可用。

#### `structure_event_driven` — "本科 reactive-system 课题"风格

```
A dishwasher comes with various programs that govern how the dishwasher cleans dishes.
The user may select one of the programs, adjust the drying time, and press the start
button to start the selected program. When a dishwasher is started, water is first
taken from the water intake pipe. Then, the dishes are washed for 10 minutes and the
water is drained. ...
```

**学术评估**：

- 优势：8 个 paper-eval case + 4 种 strategy × 多 LLM × 7 类组件的逐组件 TP/FP/FN/F1 矩阵（**512 行人评**）；reference 用 Umple 写，结构表达力齐全（hierarchical / parallel / history）；含定时（10 min / 20 min / 5 min）。
- 隐忧：领域是**家电 / 办公设备**（dishwasher / spa-manager / printer / chess-clock）—— 远离控制系统软件；NL 风格是本科生作业题（winter 2017 / fall 2019）；prediction Umple 文本 4open 没公开（只有 png 的 metric 数字）。
- 后果：是 4 个数据集中**最完整的逐组件 benchmark**，但领域偏移让结论在 control-system software 上不能直接外推。

---

## 3. NL→STM 任务对数据集的要求（学术维度推导）

把上面的实证 + `project_1` 的研究目标叠在一起，提炼 8 条数据集硬要求：

### R1. **输入是真实自由文本**（不能"半形式化预处理"）

合格 NL 应像工程师 / domain expert 在需求文档中真的会写的样子。**不能**用 "this is represented by a state X" 这种把答案直接编码进 NL 的写法 —— 那不是 generation 任务，是 reformatting 任务。

### R2. **输出元模型表达力够**

`project_1` 关心的目标元模型 `TSM = (S, S₀, E, V, C, Tr, Inv, Act)` 含：层次状态、平行区域、时钟约束、不变式、guard、action。**reference STM 必须能体现**这些，否则评测的是阉割版状态机。

### R3. **样本规模够**

经验上，方差稳健的 LLM benchmark 至少需要 **100+ 唯一输入**（参考 SysMBench 的 151，MERA 的 ~200）。低于这个数字，单个 case 的随机性会主导分数。

### R4. **领域贴近控制系统软件**

控制系统软件（汽车 ECU / 航空 / 工业自动化 / 安全关键）的 NL 需求有独特的措辞习惯：传感器 / 执行器 / 阈值 / 故障模式 / 模式切换 / 安全约束。家电、IoT、办公设备的 NL 不能直接代理。

### R5. **时间约束含量足够**

`project_1` 关心时间自动机；reference 必须含 $x \le c$ 形式的时钟约束，或在 NL 中显式有 "within T minutes" / "every k seconds" 之类的时间语义。

### R6. **可比性：同时公开 input + reference + prediction**

只有"input + reference"做的是 paper benchmark；"input + prediction"做的是方法 demonstration；**三者全有**才能做严格的 input-ref-pred 对齐和 cross-method 横评。

### R7. **评测维度多样**

不能只有 string-level F1；至少要分**组件级**（state / transition / guard / action / hierarchical / history / parallel）的 TP/FP/FN，以及**语义级**评估（safety property preservation / liveness / determinism）。

### R8. **多 LLM 多 strategy 对照**

至少含 GPT-4 / Claude 两家主流 LLM 的输出，且最好含 single-prompt / CoT / multi-step 等 strategy，避免单点结果。

---

## 4. 4 数据集对照矩阵

| 要求 | `llms_emp` | `ttool_ai` | `light_control_nimbus` | `structure_event_driven` |
|------|:----------:|:----------:|:----------------------:|:------------------------:|
| **R1** 真实自由文本 | ⚠️ 偏教学化 | ✅ 工业 spec | ✅ Dagstuhl ref problem | ⚠️ 教学题目 |
| **R2** 输出元模型表达力 | ⚠️ PlantUML，弱 HSM | ✅ AVATAR + 时间字段 | ✅ RSML-e + 平行 + 时间 | ✅ Umple + HSM + parallel |
| **R3** 规模 ≥ 100 | ⚠️ 30 输入 | ❌ 3 输入 | ❌ 4 片段 | ❌ 8 case |
| **R4** 控制系统领域 | ✅（含汽车/工业） | ✅ 汽车/航空 | ⚠️ 建筑控制 | ❌ 家电/办公 |
| **R5** 时间约束含量 | ⚠️ 0.76% | ⚠️ NL 0.87% / 输出强 | ✅ NL 3.91% + T1 | ✅ NL 2.73% + 定时 |
| **R6** input+ref+pred 全有 | ✅ 192/192 | ❌ 无 ref | ❌ 无 pred | ⚠️ pred 文本几乎全空 |
| **R7** 评测维度多样 | ⚠️ 只有 sample-level F1 | ⚠️ overall + case 总分 | ❌ 无评分 | ✅ 组件级 TP/FP/FN/F1 |
| **R8** 多 LLM × strategy | ✅ 6 LLM × single | ⚠️ TTool workflow GPT-4 单管线 | ❌ 非 LLM | ✅ 2 LLM × 4 strategy |

**说明**：⚠️ = 部分满足或有结构性缺陷；❌ = 不满足；✅ = 基本满足。

---

## 5. 综合结论

### 5.1 4 个数据集都"半合格"，没有任何一个能独立担当严格 NL→STM benchmark

把上表横向看，每个数据集都至少有 2-3 个 ❌ 或 ⚠️：

- `llms_emp`：规模最大、样本最齐，但**输入风格半形式化**（违反 R1）→ 评测结果向"会形式化重写"的模型偏；**只有 sample-level F1**（违反 R7）→ 看不到 component-level 的精确归因
- `ttool_ai`：**最贴近真实工业**（R4 强）、含**时间自动机字段**（R2/R5 强），但 **3 个 case** 远不够做统计（违反 R3）→ 单点 demonstration 性质，不构成 benchmark
- `light_control_nimbus`：**结构化最齐全**（HSM + 平行 + 时间），但**非 LLM 工作 + 4 个片段**（违反 R3/R6）→ 是方法学教科书样本，不是 benchmark
- `structure_event_driven`：**唯一组件级评测齐全**（R7 ✅），且 reference 元模型最齐全（Umple 含 HSM + history + parallel），但 **8 个家电 case**（违反 R3/R4）→ 在家电领域内可信，无法外推到控制系统软件

### 5.2 真正的"未被覆盖空白"是哪条？

把 4 个数据集的 ✅ 并起来，能覆盖 R1 / R2 / R5 / R6 / R7 / R8 的某些组合，但**没有任何一个数据集同时满足 R1+R2+R3+R4+R5**。具体说：

- "**真实工业控制系统 NL + ≥ 100 样本 + 含时间约束 + reference STM 元模型表达力齐全**" —— 没有任何公开数据集满足
- 这正是 `project_1` 自家的 sources/ 池子（[PR #7](https://github.com/HansBug/research_ideas/pull/7) 在筛 60-100 条 EFSM/HSM+T0+双A 候选）想填的空白

### 5.3 对 `project_1` 自家数据集（[`../sources/`](../sources/)）建设的启示

把 4 个公开数据集的得失做"反推"，project_1 自己做实验集时应该：

1. **保留 R1 的真实性**：sources/ 池里的 240 篇控制系统论文 NL 需求，**不要按 llms_emp 那样重写成"this is a state X"**；应该保留原文风格，让 LLM 真做 generation 而非 reformatting。
2. **达到 R3 的规模**：60-100 条是合适的目标（与 SysMBench 151 / MERA ~200 同量级）；PR #7 的 241 候选池 → 60-100 实验集这个收口口径**对的**。
3. **强化 R4 的领域聚焦**：sources/ 已经做了 EFSM/HSM + T0（无时间）+ 双 A（原文与描述都 🟢）的硬筛 → 在领域纯度上比 4 个公开数据集都高；这是 project_1 的天然优势。
4. **R5 时间约束这一条要专门补**：当前 sources/ 池筛的是 T0（无时间），但 project_1 后续要做时间状态机；建议把"T1 含时间"也作为另一个 60-100 子集单独治理（与 T0 子集对照）。
5. **R6 公开 reference 这一条要从一开始就规划**：project_1 自家实验集的 reference STM 是用 pyfcstm 还是 UPPAAL XML 写，要早定，且要**与 NL 同步公开**，避免重蹈 ttool_ai（只有 prediction 没 reference）和 light_control_nimbus（只有 reference 没 prediction）的覆辙。
6. **R7 组件级 TP/FP/FN 评测要从 structure_event_driven 学**：把 7 类组件分别打分而不是单一 F1；project_1 的评估口径在这一点上可以**直接套用 structure_event_driven 的 metric schema**（甚至 parquet 字段都能复用）。
7. **R8 多 LLM × strategy 对照**：至少做 GPT-4o + Claude 3.5 Sonnet + 一个开源（如 DeepSeek 或 Qwen）的 3-way 对比，避免单 LLM 偏置。

### 5.4 4 个数据集在 project_1 中的"角色分配"建议

不把它们当作"主 benchmark"用（都不合格），而是各司其职：

| 数据集 | 在 project_1 中的角色 |
|--------|----------------------|
| `llms_emp` | **训 / 评 reviewer**：唯一逐样本三元组齐全 → 适合做 LLM-as-judge / project_ex1 reviewer 的训练数据 |
| `ttool_ai` | **时间自动机字段对照源**：transitions.parquet 的 `after_min/after_max/probability` 是少有的真实时间标注 → 抽取作为 project_1 实验集的 reference STM 时间标注规范 |
| `light_control_nimbus` | **HSM + 平行 region 表达力示范**：4 个片段 + RSML-e 输出作为 reference 元模型设计参考 |
| `structure_event_driven` | **组件级评测协议复用源**：512 行 metric 的 schema + 评分协议直接用于 project_1 自家实验集 |

---

## 6. 留给后续讨论的开放问题

1. **R1 真实性 vs R2 表达力的张力**：真实控制系统需求文档（如 ISO 26262 HAZOP）大多写得很啰嗦、夹杂大量非状态机相关上下文；NL→STM 任务要求 LLM 先做"信息抽取 + 噪声过滤"再"建模"。**这一步是否要拆成两阶段任务**？还是端到端？
2. **数据集大小 vs 多样性的张力**：100 个 case 如果都来自同一个领域（如 BSN），泛化能力存疑；project_1 的 sources/ 是 9 个领域 → 60-100 条均匀分布意味着每个领域只有 7-11 case。**这种密度够不够做 cross-domain 泛化分析**？
3. **时间约束的 NL 显式度**：`light_control_nimbus`（3.91）和 `structure_event_driven`（2.73）的时间词频明显高于 `ttool_ai`（0.87），但 `ttool_ai` 的输出反而**显式编码了时间约束**。这是不是意味着"输出端有时间字段比 input 端有时间词更重要"？project_1 的实验集的 reference 应不应该强制要求**时间约束字段非空**？
4. **layer/parallel 推断难度**：4 个数据集 NL input 的 hierarchical 词频几乎全 0，但输出有层次结构 —— 说明这是一个 LLM 必须"无监督"推断的任务。**是否需要为 project_1 实验集专门设计"层次推断难度"标注**（如 `hier_difficulty: low/medium/high`）？

— 这 4 个问题留给和你当面讨论。
