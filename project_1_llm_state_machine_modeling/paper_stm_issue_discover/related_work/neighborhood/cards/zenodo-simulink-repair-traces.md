# 卡片 · **Agentic LLM traces for Simulink Model Repair**（⭐ 资产卡）

⚠️⚠️ **两条必须先说的话：**

1. ⛔⛔ **该 Zenodo 记录已被删除。** ⭐ 本轮（2026-08-13）实测：DOI 解析后返回 **HTTP 410 Record deleted**，⭐ Zenodo 给出的 `removal_reason` 逐字是 **`test-record`**，`removal_date` 为 **2026-05-03T13:34:35Z**。⛔ **文件已不可从 Zenodo 下载。** ⭐ 但我们**已在本机持有完整副本**（10 文件 / 162,663,460 字节），⭐ md5 全部在 D 节钉住。⭐ 本卡的一切 M 级断言来自**该本地副本的实物**，⛔ 不是来自网页描述。
2. ⛔⛔ **制品不是状态机。** ⭐ 4 个基础模型是 Simulink **连续 / 混成动力学**块图（直流电机电梯、液压缸、浮筒泵、并联混动），⛔ **没有 Stateflow、没有 state / transition**。⭐ 变异算子作用在 Gain / Sum / Product / Constant / Lookup / Switch / Integrator 初值 / MATLAB Function 上。⭐ **按本轨 §2.1 三档标注，它是 `界外`。** ⛔ **它进 L3 的理由只有一条：它是一份可实物取用的资产**（变异分类学 + 192 条 agent 轨迹 + 差分 oracle），⛔ 不是因为制品类型对得上。

⭐ 本卡按 schema 要求把 **D 节写得比别的卡厚**，⭐ 并把**变异分类学**（任务问题 3，优先级最高）与 **JSONL schema 对照**（任务问题 2）各单独立节。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `zenodo-simulink-repair-traces` |
| 数据集 `title` | Agentic LLM traces for Simulink Model Repair（v1.0.0） |
| ⭐ 配套论文 `title` | ⭐ **Evaluating Large Language Model Agents for Simulink Model Repair**（⭐ 本轮已定位并核验，⛔ 不是「找不到」） |
| `year` | 2026（⭐ 数据集 `publicationYear` 2026；⭐ 论文 Crossref `published` 2026，deposit 2026-07-18） |
| `venue` | ⛔ **数据集：Zenodo（⛔ 已 tombstone）** · ⛔ **论文：SSRN 预印本**（Crossref `type` = `posted-content`，publisher `Elsevier BV`） |
| `ccf` | ⛔ **未收录**（⛔ 预印本 + 数据集，⛔ 无 CCF venue） |
| `doi`（数据集） | [`10.5281/zenodo.19819244`](https://doi.org/10.5281/zenodo.19819244) —— ⭐ **DataCite 元数据仍在**（本轮 `api.datacite.org` 实取成功），⛔ **Zenodo 记录 410**。⚠️ ⛔ 走 Crossref 查会报「不存在」，⭐ 必须走 DataCite |
| `doi`（论文） | [`10.2139/ssrn.7138608`](https://doi.org/10.2139/ssrn.7138608) —— ⭐ **本轮实际访问 Crossref API 成功**，⭐ 标题 / 作者 / ORCID / 摘要全取到 |
| 作者 | ⭐ **Rohail Malik**（[ORCID 0009-0006-4303-6881](https://orcid.org/0009-0006-4303-6881)）· **Jari Vepsäläinen**（[ORCID 0000-0002-9379-5687](https://orcid.org/0000-0002-9379-5687)）—— ⭐ 均 **Aalto University** |
| license | ⭐ **CC-BY-4.0**（DataCite `rightsList` 明写） |
| `artifact_type` | ⛔ **Simulink 块图**（连续 / 混成动力学；⛔ **非** Stateflow / 非状态机） |
| `task` | ⭐ **修复**（faulty model → repaired model）+ ⭐ **缺陷注入**（mutation-based fault injection） |
| `boundary` | ⛔ **`界外`** —— ⛔ 连续动力学 / 混成，⛔ 不在 $M=(S,E,V,Tr,A)$ 内 |

---

## B. LLM 应用形态

### B1 · 流水线阶段

```
[确定性 · MATLAB] 变异注入器（16 算子 · 4 难度档 · 加权采样）
   → [人] 单条 zero-shot 系统提示（⭐ 全文见下）
   → [LLM agent] 自主多轮循环（⭐ 经 MCP 调 MATLAB / 读 Simulink 结构 / 跑代码）
        ⇄ [测试执行] run_tests 差分 oracle（⭐ 1% 归一化容差 + 失败信号图）
   → [agent 自己] 判定「修好了」并终止   ⛔ 或撞 600 s 墙钟上限
   → [作者] 逐 mutation 判 Fixed? / 逐 variant 算 Score / Status / Cost / Time
```

⭐ **阶段总数 6，⛔ 其中 LLM 阶段 1**（⛔ 但那一个阶段内部是多轮 agent 循环）。⭐ 其余全是确定性或人。

⭐⭐ **形态上它与我们最大的不同：⛔ 它没有多节点编排。** ⭐ 整个方法就是「**给一个 agent 一句话 + 一套工具 + 一个可反复调用的 oracle，让它自己跑**」—— ⛔ 没有 split / review / convert / adjudicate 这些分工节点。⭐ 复杂度全部下沉到 agent 自身的 tool loop 里。

⭐ **系统提示全文（M · 从本地 JSONL 逐字抄，⛔ 6 个配置下完全一致）**：
> "You are a Simulink assistant. Your task is to identify the mistake(s) in a Simulink model and fix them. The model may have several mistakes. A test function run_tests can be called with the model name to check if the model passes the tests. If the model fails, the oracle will return either the MATLAB error if simulation did not complete, or a notification that output signals deviate from reference values, accompanied by plots of the failing signals. You are not allowed to open any .slx files other than the model you are tasked to fix. You are also not allowed to modify or add something to the MATLAB path, or use absolute paths. You are only allowed access to the current working directory. The test oracle is hidden and its source code is not available. The model will have a script alongside it in the same directory, which contains values of necessary variables needed to be loaded for simulation. All the values defined in the script are correct.
>
> In the current workspace, find and fix the Simulink model."

⚠️ **注意其中一条设计选择**：⛔ **"The test oracle is hidden and its source code is not available."** ⭐ 即 oracle 是黑盒 —— ⭐ agent 只能看它的**判决与失败信号图**，⛔ 看不到判据。⭐ 这是一条刻意的防泄漏措施，⭐ 值得我们借鉴（⭐ 对照我们 §3.5 的泄漏审查）。

### B2 · 每次 LLM 调用的角色

| 角色 | 证据 |
| :-- | :-- |
| ⭐ **修复者** | ⭐ 主角色，⭐ 全部产出都是对 `.slx` 的编辑 |
| ⭐ **规划者** | ⭐ 实测调用 `update_plan`（Codex 侧）/ `TodoWrite`（Claude 侧） |
| ⭐ **抽取器 / 解释者** | ⭐ 通过 `read_simulink_system` 把非文本模型读成字典结构再理解 |
| ⛔ **评审者 / 裁决者** | ⛔ **无** —— ⭐ 判定权在 oracle，⛔ 不在 LLM |

⭐⭐ **本卡的 `judged_by` 不是 LLM-as-judge，⭐ 这一点比我们干净。**

### B3 · prompt 策略

⭐ `zero-shot`（⛔ 无 few-shot、⛔ 无 worked example）· ⭐⭐ **工具调用 / MCP**（核心）· ⛔ **无结构化输出约束**（无 JSON schema、无受限解码）· ⛔ 无 CoT 显式提示 · ⛔ 无 self-consistency · ⛔ 无多智能体辩论 · ⛔ 无 RAG。

⭐ **prompt 完全公开**（⭐ 就在 JSONL 里，⭐ 逐字可取）—— ⭐ 这是本资产的一个实打实的优点。

⭐ **实测工具集（从本地 192 条轨迹统计）**：

| MCP 工具 | 用途 |
| :-- | :-- |
| `MATLAB_Simulink_MCP.access_matlab` | 连接 MATLAB 会话 |
| ⭐⭐ `MATLAB_Simulink_MCP.run_matlab_code` | ⭐ **主力**（改模型、跑 `run_tests`、查参数）—— ⭐ 全语料出现最频繁 |
| ⭐⭐ `MATLAB_Simulink_MCP.read_simulink_system` | ⭐⭐ **拓扑的字典表示** —— ⭐ **这正是被消融掉的那个工具** |
| `MATLAB_Simulink_MCP.read_matlab_code` | 读 `_Script.m` |
| `MATLAB_Simulink_MCP.search_simulink_library` | 查库（⭐ 极少用） |
| 宿主内建 | `shell_command` / `update_plan` / `list_mcp_resources`（Codex）；`Bash` / `Read` / `Glob` / `TodoWrite` / `ToolSearch`（Claude Code） |

### B4 · ⭐⭐ 循环与裁决者

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无循环 | ⭐⭐ **有 —— agent 自主 tool loop** | **M**（轨迹里 `run_tests` 被反复调用） |
| ⭐⭐ **裁决者是谁** | ⭐⭐ **`测试执行`** —— ⭐ `run_tests.m`：**差分 oracle**，把仿真输出的每条 timeseries 与参考 `.mat` 比对，⭐ **归一化误差容差 1%**；⛔ 仿真崩了就把 MATLAB 异常回传。⛔⛔ **但「要不要再来一轮」的决定权在 agent 自己，⛔ 不在 oracle** | **M** |
| ⭐ 裁决者类型细分 | ⚠️ **它是 sound 的「必要方向」，⛔ 不是充分方向**：⭐ oracle 说 fail 一定有问题（可信）；⛔ oracle 说 pass **只说明在这组参考轨迹上 1% 内一致**，⛔ 不等于修对了（⚠️ 与我们 §3.5 的口径一致：这是测试执行，⛔ 不是 sound oracle） | **S** |
| 终止条件 | ⭐⭐ **两个：① agent 自认完成；② ⛔ 600 秒墙钟预算耗尽** | **S**（⭐ 从台账 `Time` 列在 **79** 个格上精确等于 600 推出；⛔ 论文摘要未提这个上限） |
| 最大轮数 | ⛔ **原文未提供**（⛔ 无轮数上限，⛔ 只有时间上限） | — |
| ⭐⭐ 有无报**循环的边际收益** | ⛔⛔ **无逐轮数字** —— ⭐ 论文与台账都只给终局。⚠️ **但 JSONL 里逐轮 token 用量与逐次 `run_tests` 结果全都在，⭐ 这份逐轮收益曲线是可以由我们自己算出来的**（见 E1） | **M**（无报告）/ ⭐ **可算** |

⭐⭐ **`run_tests.m` 的判据（M · 从本地 `test_oracle.zip` 逐字抄）**：
```matlab
TOLERANCE = 0.01;   % 1 % normalised error
...
range = max(y_ref) - min(y_ref);
if range == 0
    norm_err = max(abs(y_attempt - y_ref));          % absolute fallback
else
    norm_err = max(abs(y_attempt - y_ref) / range);  % normalised
end
status = norm_err <= tolerance;
```
⭐ **全部信号都必须过**才算通过（`if all(statuses)`）；⭐ 参考数据是 `reference_data.mat`（**32,906,083** 字节，⭐ 按 base model 名分 struct）。⭐ 失败时给出信号名 + `plotPair` 画的 ref vs test 对比图。

### B5 · 中间表示

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无 | ⭐ **有，两处，⛔ 且性质完全不同** | **M** |
| ⭐ **① 上下文侧**（给 agent 看的） | ⭐ **拓扑的字典表示**（`read_simulink_system` 的输出）**vs 模型快照图像** —— ⭐ 论文摘要逐字："using either a dictionary representation of topology or a model snapshot for context"。⚠️ **这两者的对照就是本文的消融轴** | **M** |
| ⭐⭐ **② 缺陷侧**（造语料用的） | ⭐⭐ **16 条闭合变异算子分类学**，⭐ 分**两族**（parametric 1–8 / structural 9–16），⭐ 配 **4 档难度模板** | **M** |
| ⭐ **是否闭合** | ⭐⭐ **① 开放**（字典是模型的完整转写，⛔ 无候选集）；⭐⭐ **② 严格闭合**（16 条，⛔ `applyMutation` 的 `otherwise` 直接 `error('Unsupported mutation type')`） | **M** |
| ⭐ **谁定的** | ⭐ **② 由作者预编**（硬编码在 MATLAB 里），⛔ **不是 LLM 选、⛔ 也不是从语料归纳**。⚠️ **关键：这份分类学在注入侧，⛔ agent 侧完全看不到它** | **M** |

⚠️⚠️ **这是与我们最重要的一处结构差异，⭐ 必须说清：** ⭐ 我们的 19 条闭合谓词词表是**给 LLM 选的**（检测侧闭合）；⛔ 它的 16 条闭合分类学是**给注入器用的**（生成侧闭合），⛔ **agent 从头到尾不知道有这 16 类**。⛔ **所以「闭合 19 条 + LLM 自动选」这个组合，本卡同样提供 0 个先例。** ⭐ 但它提供了另一个东西：**一份可直接对位的行为模型缺陷分类学**（见专节）。

### B6 · 模型

| 配置 | 模型 | 宿主 |
| :-- | :-- | :-- |
| C=1 | ⭐ **GPT-5.4** | ⭐ Codex CLI（⭐ 实测 `cli_version` **0.118.0**，`originator` `codex-tui`） |
| C=2 | ⭐ **GPT-5.2** | ⭐ 同上 |
| C=3 | ⭐ **Claude Sonnet 4.6**（⭐ JSONL 内 `model` 字段逐字 `claude-sonnet-4-6`） | ⭐ Claude Code（⭐ 实测 `version` **2.1.92**，`entrypoint` `claude-desktop`） |

⭐ **3 模型 × 2 设置 = 6 个配置，⭐ 每配置 32 格 = 192 次运行。** ⭐ **有多模型对照，⭐ 且跨两个不同 agent 宿主**（⚠️ 后者引入混淆变量，见 F）。

⭐ **模型定价（M · `usage_calc.py` 逐字，⭐ 单位 $/M token）**：`claude-sonnet-4-6` input 3.00 / cache_write 3.75 / cache_read 0.30 / output 15.00；`gpt-5.2` input 1.75 / cached 0.175 / output 14.0；`gpt-5.4` input 2.50 / cached 0.250 / output 15.0。

⭐ **环境元数据（⭐ 实测，⭐ 这一格比论文里能读到的多）**：`cwd` = `C:\Data\Research\Doctoral\Paper 1\Setup\workspace`（⭐ Windows）· `timezone` `Europe/Kiev` · `sandbox_policy` `workspace-write` 且 **`network_access: false`** · `approval_policy` `on-request` · `reasoning_effort` **medium** · `model_context_window` **258400** · MATLAB **R2025b**。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | 是否 sound |
| :-- | :-- | :-: |
| ⭐⭐ **变异注入器** | ⭐ 纯 MATLAB（`generateVariants.m` / `findAllSites.m` / `applyMutation.m`），⭐ **带 RNG seed 参数**，⭐ 加权采样（重复算子权重 $0.25^{\text{count}}$ 指数衰减；站点权重 $\frac{1}{1+\text{count}} \times (\text{depth}+1)$，⭐ **偏好更深层的子系统**） | ⭐ 是（⭐ ground truth 白盒） |
| ⭐⭐ **`run_tests.m` 差分 oracle** | ⭐ 数据驱动，1% 归一化容差，全信号必过 | ⚠️ 单向 sound |
| Simulink `sim()` | 数值仿真 | ⭐ 是（⭐ 但依赖 solver 设定） |
| 成本 / 时间统计 | ⭐ `usage_calc.py` 从 JSONL 逐条 usage 累加（⭐ 按 `requestId` 去重） | ⭐ 是 |
| ⭐ 站点发现 | ⭐ `find_system` + `BlockType` / `ReferenceBlock` 过滤（⭐ 每类算子一套专用过滤器） | ⭐ 是 |

⭐⭐ **底座评价：⭐ 它的确定性底座比我们**在缺陷侧**更硬 —— ⭐ 缺陷是机械注入的，于是 ground truth 是白盒（算子 + 站点路径 + 描述全部落表）。⛔ 但在**裁决侧**比我们软 —— ⭐ 它只有测试执行，⛔ 没有任何形式化检查。

---

## B-bis. ⭐⭐⭐ 任务问题 3（优先级最高）：变异注入器注入哪几类缺陷 —— **逐类抄下来**

⭐⭐ **16 条，闭合，分两族。⭐ 名称逐字取自 `generateVariants.m` 的 `getMutationName`，⭐ 语义逐字取自 `applyMutation.m` 的函数注释，⭐ 站点逐字取自 `findAllSites.m`。**

### 族 A · Parametric（算子 / 取值类，tag 1–8）

| tag | ⭐ 名称（逐字） | ⭐ 语义（逐字注释） | ⭐ 站点（`findAllSites`） |
| :-: | :-- | :-- | :-- |
| **1** | **Relational Operator Replacement** | "Mutates relational operators for Relational Operator, Compare To Constant, Compare To Zero" | `RelationalOperator` 块 + `Compare To Constant` / `Compare To Zero` |
| **2** | **Logical Operator Replacement** | "Mutates the Operator parameter of a Logical Operator block. AND -> OR, NAND / OR -> AND, NOR" | `Logic` 块 |
| **3** | **Arithmetic Operator Replacement** | "Mutate an arithematic operation by swapping two operators. If all operators are same, flip one randomly" | `Sum` + `Product`（⛔ 排除纯 `/` 的倒数块） |
| **4** | **Initial Value Perturbation** | "Mutate an Initial condition by changing zero to non-zero and vice versa" | 有初值的块（积分器 / 延迟） |
| **5** | **Embedded Code Mutation** | "Mutates the code in MATLAB function block by dropping parentheses in denominator, or if not possible then swapping two inputs" | `MATLAB Function` 块 |
| **6** | **Constant Value Transposition** | "Swaps parameter values of two Constant or Gain blocks."（⭐ **需两个站点**） | `Gain` + `Constant` |
| **7** | **Constant Expression Mutation** | ⭐ 丢掉分母括号，或不行则**取一个变量做取反** | `Gain` + `Constant` |
| **8** | **Lookup Breakpoints Transposition** | "Mutates lookup table data by swapping parameter contents directly. For 1-D lookup: swaps Table and BreakpointsForDimension1. For 2-D or higher: swaps BreakpointsForDimension1 and BreakpointsForDimension2." | `Lookup` 块 |

### 族 B · Structural（结构类，tag 9–16）

| tag | ⭐ 名称（逐字） | ⭐ 语义（逐字注释） | ⭐ 站点 |
| :-: | :-- | :-- | :-- |
| **9** | **Algebraic Loop Formulation** | "Deletes a delay or ic to create a potential alegbraic loop" | 有初值的块 |
| **10** | **Arithmetic Block Type Swap** | "Replace a Sum block with product and vice versa. Maps '+' -> '\*' and '-' -> '/' and restores connections." | `Sum` + `Product` |
| **11** | **Conditional Input Transposition** | "Swaps the two data inputs (u1 and u3) of a Switch block." | `Switch` 块 |
| **12** | **Gain Block Deletion** | "Deletes a gain block altogether" | `Gain` 块 |
| **13** | **Direct Connection Transposition** | ⭐ 交换两条连线的目的端（⭐ **需两个站点，且必须同一父系统**） | 连线（`line`） |
| **14** | **Unary Block Deletion** | "Deletes a 1-in/1-out block and reconnects its input directly to all destinations of its output" | 单入单出块 |
| **15** | **Type Conversion Omission** | "Deletes a block causing data type conversion, such as relational operators (i.e. float to boolean)" | `Compare To Constant/Zero`（单入） |
| **16** | **Signal Tag Transposition** | "Swaps tags of two From blocks. Both GoTos exist, just their outlets swapped here in From blocks" | `From` 块（⭐ **需两个站点**） |

### ⭐⭐ 4 档难度模板（M · `get_template_tier` 逐字）

| tier | 组合 | 变异条数 |
| :-: | :-- | :-: |
| **1** | `{1–8}` | ⭐ **1**（纯 parametric） |
| **2** | `{1–8}` + `{9–16}` | ⭐ **2**（1 参数 + 1 结构） |
| **3** | `{1–8}` + `{1–8}` + `{9–16}` | ⭐ **3** |
| **4** | `{1–8}` + `{1–8}` + `{9–16}` + `{9–16}` | ⭐ **4** |

⭐ **每档 `n=2` 个变体 → 每个基础模型 8 个 faulty variant（⭐ 这就是文件名里 B=1..8 的来源）。**

### ⭐⭐ 与我们 G1 的 issue 字段对位分析（⚠️ 这一格是 I 级判断，⛔ 不是原文主张）

| ⭐ 可直接借用的设计 | ⭐ 说明 |
| :-- | :-- |
| ⭐⭐ **两族划分（parametric / structural）** | ⭐ 这条抽象层级足够高，**跨制品类型成立**：⭐ 「改了一个取值 / 改了图的形状」是任何图状行为模型都有的二分。⭐ 我们的台账目前**没有这一层**，⭐ 而它能直接支撑「结构缺陷 vs 语义缺陷哪类更难被发现」这个分析 |
| ⭐⭐ **难度 = 变异条数的组合模板** | ⭐ 「1 参数 / 1 参数+1 结构 / 2+1 / 2+2」这种**显式组合表**比我们「按 pair 天然难度」更可控。⚠️ 但注意：⭐ 他们自己的结果显示**这个难度轴几乎不起作用**（见 C 节 tier 数据），⛔ 起作用的是基础模型复杂度 |
| ⭐ **每条变异都落表：算子 + 站点路径 + 人类可读描述** | ⭐ 台账列逐字为 `Variant / VariantTier / MutationTag / MutationName / Site / Description`。⭐ **`Description` 那列是人类可读的缺陷陈述**（如 `k_t replaced with 1/(k_t)`），⭐ 与我们台账的「期望发现」字段同构 |
| ⭐ **站点采样偏向深层子系统** | ⭐ 权重 $(\text{depth}+1)$ —— ⭐ 即刻意把缺陷藏得更深。⭐ 这是一条可借用的**难度旋钮**（⛔ 与变异条数正交） |
| ⛔ **逐类算子不可直接对位** | ⛔ 它的 16 类全部是**块级 / 参数级**（Gain 值、Switch 输入、Lookup 断点）；⛔ 我们的缺陷是**语义级**（状态可达性、守卫互斥 / 不完备、层次一致性、初始状态）。⛔ **一对一映射不存在。** ⭐ 能搬的是**分族方式与登记格式**，⛔ 不是类目本身 |

⭐⭐ **一句话给 G1**：⭐ **搬「parametric / structural 两族 + 组合式难度模板 + 六列登记格式（含人类可读 Description）」，⛔ 不要搬 16 个类目名。** ⭐ 并且注意他们的反面教训：⛔ **变异条数这个难度轴实测几乎无效**（tier 1 反而最低），⛔ 别把它当主难度轴。

---

## B-ter. ⭐⭐ 任务问题 2：JSONL schema —— 逐字段抄 + 与我们 run record 对照

⭐⭐ **重要前提：⛔ 这不是作者自定义的 run record，⭐ 而是两个 agent 宿主的原生会话日志原样导出。** ⭐ 于是它有的字段来自 Codex / Claude Code，⛔ 不是作者设计的。

### ⭐ 文件命名与规模

⭐ **`A.B.C.D.jsonl`**（M · `schema.json` + `README.md` 逐字）：`A` = Simulink 模型（1 DC Motor Elevator / 2 Hydraulic Cylinder / 3 Buoy Pump / 4 Parallel Hybrid）· `B` = faulty variant 1–8 · `C` = LLM（1 GPT-5.4 / 2 GPT-5.2 / 3 Sonnet 4.6）· `D` = 设置（1 full / 2 ablated）。

⭐ **实测：`llm_traces.zip` 内 192 个 `.jsonl`（198 项含 6 个目录），⭐ 解压后 212,212,657 字节，⭐ 6 目录 × 32 文件，⛔ 完全无缺格。**

### ⭐ 形态 ①：Codex（GPT-5.2 / 5.4，4 个目录 128 文件）

⭐ **每行三字段：`{timestamp, type, payload}`**（⭐ 实测某文件 140 行全部同构）。

| `type` | `payload.type` | 内容 |
| :-- | :-- | :-- |
| `session_meta` | — | ⭐ `id` · `timestamp` · `cwd` · `originator` · ⭐ **`cli_version`** · `source` · ⭐ **`model_provider`** · ⭐⭐ **`base_instructions`（系统提示全文）** |
| `turn_context` | — | ⭐ `turn_id` · `cwd` · `current_date` · `timezone` · ⭐ **`approval_policy`** · ⭐⭐ **`sandbox_policy`（含 `network_access`）** · ⭐ **`model`** · `personality` · ⭐ **`collaboration_mode`（含 `reasoning_effort` 与 developer instructions 全文）** · ⭐ **`effort`** · ⭐ **`truncation_policy`** |
| `event_msg` | ⭐⭐ **`token_count`** | ⭐⭐ **`info.total_token_usage`**（`input_tokens` · `cached_input_tokens` · `output_tokens` · ⭐ **`reasoning_output_tokens`** · `total_tokens`）· ⭐⭐ **`info.last_token_usage`（逐轮！）** · ⭐ **`model_context_window`** · ⭐ **`rate_limits`**（`used_percent` · `window_minutes` · `resets_at` · `plan_type`） |
| `event_msg` | `user_message` | ⭐ 任务提示逐字 |
| `event_msg` | `agent_message` / `agent_reasoning` | 回复与推理摘要 |
| `event_msg` | ⭐ `mcp_tool_call_end` | ⭐ `call_id` · ⭐ **`invocation`（server + tool + arguments）** · ⭐ **`duration`（secs/nanos）** · ⭐ **`result.Ok.content`** · ⭐⭐ **`isError`** |
| `event_msg` | ⭐ `exec_command_end` | ⭐ `command`（数组）· `cwd` · `parsed_cmd` · ⭐ **`stdout` / `stderr` / `aggregated_output`** · ⭐⭐ **`exit_code`** · `duration` |
| `event_msg` | `task_started` / ⭐ **`task_complete`** | ⭐ `task_complete` 含 ⭐⭐ **`last_agent_message`（agent 自述修了什么）** |
| `response_item` | `function_call` / `function_call_output` / `reasoning` / `message` | ⭐ 原始 API 层的调用与返回 |

⭐ **实测一格的用量样例**（`GPT-5.2/1.1.2.1.jsonl`，full 设置）：`input 521,906 · cached_input 504,448 · output 4,201 · reasoning_output 2,461 · total 526,107`；⭐ **同格 ablated**（`1.1.2.2.jsonl`）：`input 110,179 · cached 97,152 · output 2,665 · reasoning 514 · total 112,844`。⭐⭐ **即消融把总 token 降到 21%** —— ⭐ 这就是论文摘要说的 "reduces cost"。

### ⭐ 形态 ②：Claude Code（Sonnet 4.6，2 个目录 64 文件）

⭐ **完全不同的 schema**（⭐ `usage_calc.py` 的 `detect_format` 就是靠 `message` vs `payload` 区分的）。

| 字段 | 内容 |
| :-- | :-- |
| `type` | `assistant` / `user` / ⭐ `queue-operation` / `attachment` |
| ⭐ `message` | ⭐ `model`（`claude-sonnet-4-6`）· `id` · `role` · `content`（含 `tool_use` / `tool_result`）· ⭐ **`stop_reason` / `stop_details`** · ⭐⭐ **`usage`**（`input_tokens` · ⭐ **`cache_creation_input_tokens`** · ⭐ **`cache_read_input_tokens`** · ⭐ **`cache_creation.ephemeral_5m/1h`** · `output_tokens` · ⭐ **`service_tier`** · `inference_geo`） |
| ⭐ 会话链 | ⭐⭐ **`uuid` / `parentUuid`（父子链，⭐ 可重建完整因果树）** · `sessionId` · `requestId` · `promptId` · ⭐ `sourceToolAssistantUUID` |
| ⭐ 工具结果 | ⭐⭐ **`toolUseResult`** · ⭐ `mcpMeta` |
| ⭐ 环境 | `cwd` · ⭐ **`version`**（`2.1.92`）· ⭐ **`entrypoint`**（`claude-desktop`）· `gitBranch` · `userType` · ⭐ `permissionMode` · `isSidechain` · `slug` |

### ⭐⭐ 任务问题 2 的直接回答：有没有记这四件事

| 问题 | 答案 | 证据 |
| :-- | :-: | :-- |
| ⭐⭐ **每轮 token 用量** | ⭐⭐ **有，而且比我们细** | ⭐ Codex 侧 `last_token_usage` **逐轮**给，⭐ 且**单列 `reasoning_output_tokens`**；⭐ Claude 侧每条 assistant 消息带 `usage`，⭐ **cache 读/写分开计**、⭐ 还分 5m/1h ephemeral |
| ⭐⭐ **工具调用** | ⭐⭐ **有，全量** | ⭐ 工具名 · 参数 · 返回内容 · ⭐ **`isError`** · ⭐ **`duration`** · ⭐ shell 的 `exit_code` 与 `stdout`/`stderr` 全在 |
| ⭐ **失败原因** | ⚠️ **半有** | ⭐ **工具层失败有**（`isError` / `exit_code` / MATLAB 异常原文）；⛔⛔ **格级失败原因没有** —— ⛔ 无 `failure_reason` 字段，⛔ 「为什么这格没修好」只能靠读轨迹或看台账的 `Status=0` + `Time=600` 反推 |
| ⭐⭐ **终止条件** | ⚠️ **间接有** | ⭐ Codex 有 `task_complete`（正常完成）；⭐ Claude 有 `stop_reason`。⛔⛔ **但「撞 600 s 上限」这个终止原因不在 JSONL 里**，⛔ 只能从 `Results.xlsx` 的 `Time` 列等于 600 推出 |
| ⭐⭐ **预算耗尽** | ⚠️ **有，⛔ 但在错的地方** | ⛔⛔ **JSONL 里没有任何预算字段**；⭐ 它以 **`Results.xlsx` 的 `Time = 600`** 这个隐式形式存在，⭐ **实测 79/192 = 41.1% 的格撞上限**（见 C 节）。⛔ **这是一个明显的 run record 设计缺陷：最重要的失败类别没有被结构化记录** |

### ⭐⭐ 与我们自己的 run record 对照：我们缺什么 / 多什么

| 维度 | ⭐ 他们 | ⭐ 我们（`AgentLoopRunRecord` / v46 discover） | ⭐ 裁定 |
| :-- | :-- | :-- | :-- |
| ⭐ **reasoning token 单列** | ⭐ **有**（`reasoning_output_tokens`） | ⚠️ **待核** | ⭐⭐ **可能是我们缺的** —— ⭐ 我们「修订机器吃 79% token」这条结论里，⛔ **有多少是 reasoning token 目前分不出来**。⭐ 若真缺，这是一条低成本高价值的补记 |
| ⭐ **cache 读/写分列** | ⭐ **有**（Claude 侧还分 5m/1h ephemeral） | ⚠️ **待核** | ⭐ 影响成本核算精度（⭐ cache_read 只要 1/10 价） |
| ⭐ **工具调用 duration** | ⭐ **有**（每次 MCP 调用的 secs/nanos） | ⛔ **我们没有工具调用**（无 tool loop） | ⛔ **不适用** |
| ⭐ **沙箱 / 网络策略落盘** | ⭐ **有**（`network_access: false` 明确写进每个 turn） | ⚠️ **待核** | ⭐ **值得补** —— ⭐ 它是「结果不受外部检索污染」的可审计证据 |
| ⭐ **宿主版本号** | ⭐ **有**（`cli_version 0.118.0` / `version 2.1.92`） | ⛔ **我们没有宿主**，⭐ 但**代码版本同样缺**（⚠️ §3.5.1 已记：run record 无代码版本字段，⛔ 只能靠时间戳反推 commit） | ⭐⭐ **这是我们的已知缺口，⭐ 本卡为它提供了一个外部对照：别人连 CLI patch 版本都记了** |
| ⭐ **父子因果链** | ⭐ **有**（Claude 侧 `uuid`/`parentUuid` 可重建完整树） | ⭐ **有等价物**（LangGraph 节点序列） | ⭐ **不缺** |
| ⭐⭐ **降级 / 未满足义务的结构化诊断** | ⛔⛔ **无** —— ⛔ 无 quarantine / coverage_gap / unmet_contract 概念，⛔ 预算耗尽只体现为一个 600 | ⭐⭐ **有**（§10 要求的三类结构化诊断） | ⭐⭐ **我们多，⭐ 而且这是实质优势。** ⭐ 他们 41.1% 的格撞上限却**没有任何结构化记录说明卡在哪一条义务上** —— ⛔ 那正是我们 §10 明写要避免的情形 |
| ⭐⭐ **多轮 / `@k` 口径** | ⛔⛔ **无** —— ⭐ 每格只跑 1 次 | ⭐⭐ **有**（`hit@1` / `hit@3` / `hit@all`） | ⭐⭐ **我们多，⭐ 优势明确** |
| ⭐ **逐位人工判定** | ⛔ **无**（⭐ 只有逐 mutation 的 0/0.5/1） | ⭐ **有**（574 位逐位 + 288 簇五类） | ⭐ **我们多** |
| ⭐⭐ **prompt 落盘** | ⭐⭐ **有，逐字在 JSONL 里**（⭐ 连 developer instructions 全文都在） | ⭐ **有**（源码内） | ⭐ **打平**，⛔ 但他们的做法**更利于第三方审计**（⭐ 不必读我们的代码就能看到当次实际提示） |
| ⭐ **模型精确 ID** | ⭐ **有**（`claude-sonnet-4-6` / `gpt-5.2`），⛔ **但无 snapshot 日期** | ⭐ **有** | ⭐ 打平 |

⭐⭐ **一句话结论**：⭐ **我们在「判定质量、多轮口径、降级诊断」三项明显更强；⛔ 他们在「资源计量的粒度（reasoning / cache 分列）、环境可审计性（沙箱策略 + 宿主版本）、prompt 的第三方可审计性」三项更强。** ⭐ **前两项是我们可以低成本补上的。**

---

## C. 实验

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `baseline` | ⛔⛔ **无方法 baseline** —— ⛔ 无「非 agent 的自动修复」对照、⛔ 无「人类工程师」对照、⛔ 无「随机改」对照。⭐ **唯一对照是 full vs ablated 消融**（⭐ 消融轴 = 有无 `read_simulink_system`） | **M / S** |
| `dataset` | ⭐ **4 个基础 Simulink 模型 × 8 个 faulty variant = 32 个 faulty model**；⭐ 每个 variant 含 1–4 条注入变异，⭐ **每配置 80 条 mutation 实例**（⭐ 实测精确计数），⭐ 6 配置合计 **480 条**。⭐ **分母怎么定的**：⭐ **由注入器白盒决定**（⭐ 注入了几条就是几条，⛔ 无人工裁定分母的空间）。⭐ 基础模型来自作者自己的动力总成研究（⭐ MATLAB R2025b 创建） | **M** |
| `metrics` | ⭐ **`Fixed?`**（逐 mutation，⭐ 取值 **1 / 0.5 / 0**）· ⭐ **`Score`**（逐 variant，⭐ = 该 variant 内 `Fixed?` 的均值）· ⭐ **`Status`**（逐 variant 二值，⭐ 全修好且过 oracle 才 1）· ⭐ **`Cost ($)`** · ⭐ **`Time`（秒，⛔ 上限 600）**。⛔⛔ **无任何 `@k` 口径** | **M** |
| ⭐ `judged_by` | ⚠️⚠️ **混合，⛔ 且逐 mutation 那一层的判定者未说明**：⭐ **`Status` 是自动的**（oracle 判 pass/fail）；⛔⛔ **但 `Fixed?` 的逐 mutation 归因看起来是作者人工做的** —— ⭐ 因为 oracle 只给整体 pass/fail，⛔ 给不出「这 4 条变异里第 2 条被修好了」这种粒度，⭐ 而 `0.5` 这个取值只能来自人工判断。⛔⛔ **无标注者间一致性、无 $\kappa$、⛔ 未说几个人判、⛔ 未说判据** | ⭐ `Status` **M** / ⛔ `Fixed?` 判定者 **I**（⭐ 我方推断，⛔ 原文未说明） |
| `human_baseline` | ⛔ **无** | **S** |
| `runs` | ⛔⛔ **每格 1 次，⛔ 无重复、⛔ 无方差、⛔ 无置信区间、⛔ 无 seed 记录**（⚠️ `generateVariants` 有 seed 参数，⛔ 但用的哪个 seed 未落盘） | **M / S** |
| ⭐ `adverse_results` | ⭐ 见下（⚠️ **有一处措辞弱化**） | **M / S** |

### ⭐⭐ 192 次运行的结果分布（⭐ 全部由我方从 `Results.xlsx` 实算，⭐ 复算口径见下）

| 配置 | 格数 | ⭐ `Status=1` | ⭐ 完全成功率 | mutation 数 | ⭐ 修好数 | ⭐ **mutation fix rate** | ⛔ **`Time=600`** | ⭐ 平均 `Score` | ⭐ 总成本 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| **GPT-5.4** | 32 | 26 | ⭐ **81.2%** | 80 | 74.0 | ⭐⭐ **92.5%** | 6 | 94.5% | $16.08 |
| GPT-5.4 (Ablated) | 32 | 24 | 75.0% | 80 | 68.0 | 85.0% | 8 | 83.1% | $19.32 |
| GPT-5.2 | 32 | 20 | 62.5% | 80 | 63.5 | 79.4% | 12 | 78.5% | $17.10 |
| GPT-5.2 (Ablated) | 32 | 21 | 65.6% | 80 | 59.0 | 73.8% | 12 | 73.4% | $12.66 |
| ⛔ **Sonnet-4.6** | 32 | 10 | ⛔ **31.2%** | 80 | 45.5 | ⛔ **56.9%** | ⛔ **22** | 57.7% | $14.69 |
| Sonnet-4.6 (Ablated) | 32 | 13 | 40.6% | 80 | 48.5 | 60.6% | 19 | 60.4% | ⛔ **$26.64** |
| ⭐ **合计** | **192** | **114** | ⭐ **59.4%** | **480** | **358.5** | ⭐ **74.7%** | ⛔⭐ **79** | **74.6%** | **$106.48** |

⭐ **复算口径**：⭐ `Fixed?` 按 `analysis.py` 的 `clean_fixed_value` 处理（>1 则 /100）；⭐ variant 行按 `Variant` 列非空计（⭐ 合并单元格式的续行不重复计）；⭐ `Time=600` 判据为 $|t - 600| < 10^{-6}$。

### ⛔⛔ 任务问题 5 的直接回答：**有「预算耗尽」这一类，⭐ 而且占比很高**

⭐⭐ **`Time = 600` 精确命中 79/192 = 41.1%。** ⭐ 且它**不是**「失败」的同义词 —— ⭐ 有的格 `Score = 0.83` 但 `Status = 0` 且 `Time = 600`，⭐ 即**部分修好后撞墙钟**。

⭐ **逐配置的耗尽率**：GPT-5.4 **18.8%**（6/32）· GPT-5.4-Abl **25.0%** · GPT-5.2 **37.5%** · GPT-5.2-Abl **37.5%** · ⛔ **Sonnet-4.6 68.8%**（22/32）· Sonnet-4.6-Abl **59.4%**。

⭐⭐ **与我们 v44 的对照**：⭐ 我们 **22/35 格降级、97 次降级事件**；⭐ 他们 **79/192 格撞预算上限**。⭐ **两边都在同一个量级上（我们 62.9%，他们 41.1%），⛔ 差别在于：⭐ 我们把它记成了结构化降级事件（能回答「卡在哪条义务上」），⛔ 他们只留下一个 `600`。** ⚠️ **所以这条不能当「别人也这样所以没事」用**；⭐ 它的正确用法是：⭐ **「agent 型修复流水线上，四成格撞预算是常态而非异常」这件事有了外部旁证** —— ⭐ 于是我们 §10「一律降级不许抛」那条纪律得到支持，⛔ 而「降级率高本身」不构成方法失效的证据。

### ⭐ 失败模式与归因

| 轴 | 数据 | ⭐ 结论 |
| :-- | :-- | :-- |
| ⭐ **按 tier（变异条数）** | tier 1 **69.8%** · tier 2 **79.7%** · tier 3 **76.0%** · tier 4 **72.9%**（⭐ 平均 `Score`，⭐ 每档 n=48） | ⛔⛔ **非单调，⭐ 且极差只有 9.9pp** —— ⭐ **变异条数几乎不影响难度**，⛔ tier 1 反而最低 |
| ⭐⭐ **按基础模型（复杂度）** | ⭐ Hydraulic_Cylinder **93.4%** · Elevator_Motor **82.1%** · Buoy_Pump **79.6%** · ⛔ **Parallel_Hybrid 43.3%**（⭐ 每个 n=48） | ⭐⭐ **极差 50.1pp** —— ⭐ **这才是主难度轴**，⭐ 与论文摘要逐字一致："Repair success is more strongly affected by model complexity than by mutation count." |
| ⭐ **按变异族** | ⭐ Parametric(1–8) **75.5%**（n=288）· Structural(9–16) **73.4%**（n=192） | ⚠️ **两族几乎无差**（2.1pp）—— ⛔ 与直觉相反（⭐ 本以为结构缺陷更难） |
| ⭐ **最难的单个算子** | ⛔ **tag 9 Algebraic Loop Formulation：0.0%**（n=6，⭐ 全军覆没）· ⛔ tag 2 Logical Operator Replacement **33.3%**（n=6）· ⛔ tag 5 Embedded Code Mutation **45.8%**（n=24）· ⛔ tag 15 Type Conversion Omission **50.0%**（n=12） | ⚠️ **注意 n 极小**（⭐ 有 4 个算子 n=6），⛔ 这些逐类率**不可作强结论** |
| ⭐ **最易的算子** | ⭐ tag 8 Lookup Breakpoints Transposition **100%**（n=12）· tag 16 Signal Tag Transposition **100%**（n=6）· tag 6/7 Constant 类 **86.7%**（各 n=60） | — |

### ⭐ `adverse_results` 的处理

1. ⭐ **模型间差距巨大且照实报**：⛔ Sonnet-4.6 只有 **31.2%** 完全成功率 vs GPT-5.4 的 **81.2%**，⛔ 且 Sonnet 成本最高（ablated 那格 $26.64）。⭐ **既慢、既贵、既差三件事同时报了。**
2. ⛔⛔ **但消融结论被措辞弱化了。** ⭐ 摘要逐字：
> "An ablation study indicates that dictionary-based structural context reduces cost and generally improves repair performance."

   ⚠️ **"generally" 这个词遮住了一个反例**：⛔ **Sonnet-4.6 的 ablated 反而更好**（`Status` 40.6% vs 31.2%；fix rate 60.6% vs 56.9%；平均 Score 60.4% vs 57.7%）。⭐ 即 **3 个模型里有 1 个方向相反（1/3）**，⛔ 而 "generally" 让读者以为只是幅度差异。⚠️ **按我们 §7.5 的方向性松紧一致要求，这属于对自己有利方向的限定写得不足。**
3. ⚠️ **"reduces cost" 也只在 GPT 侧成立**：⭐ GPT-5.2 ablated $12.66 < full $17.10（✓）；⛔ 但 **GPT-5.4 ablated $19.32 > full $16.08**（✗），⛔ **Sonnet ablated $26.64 > full $14.69**（✗）。⭐⭐ **即「降成本」在 3 个模型里也只有 1 个成立。** ⚠️ ⛔ **这与摘要的表述冲突。**（⚠️ 我方复算，**S 级**；⛔ 可能作者用的是 token 数而非美元数 —— ⭐ 单格 token 对照确实降到 21%，见 B-ter。⭐ 但台账里的 `Cost ($)` 列不支持这个说法，⛔ 两者口径差异原文未解释。）
4. ⛔ **41.1% 的格撞预算上限这件事，摘要与台账都没有作为一个结果被讨论**（⛔ 只以 `Time=600` 隐式存在）。

⚠️ **⛔ 另有一处数字对不上**：⭐ 摘要说 "best performing agent fixing up to **93.1%** of mutations"，⛔ 而我方从台账实算 GPT-5.4 = **74/80 = 92.5%**（⭐ 且该 sheet 的 `Fixed?` 全为 0/1 二值，⛔ 无 0.5）。⛔ **口径差异未解**（见 F）。

---

## D. ⭐⭐ 资产（⭐ 本卡重点，⛔ 按 schema 要求写厚）

### ⭐⭐ D.1 · 可访问性总判：⛔ **🟠**（⛔ 不是 🟢）

| 入口 | ⭐ 本轮实测结果 |
| :-- | :-- |
| `https://doi.org/10.5281/zenodo.19819244` | ⛔ **302 → `zenodo.org/records/19819245` → HTTP 410** |
| `https://zenodo.org/api/records/19819244` | ⛔ **302 → `/api/records/19819245`** |
| `https://zenodo.org/api/records/19819245` | ⛔⛔ **HTTP 410 `{"status":410,"message":"Record deleted","tombstone":{...}}`** |
| `https://zenodo.org/api/records/19819245/files` | ⛔ **HTTP 410** |
| `https://zenodo.org/records/19819245/files/<name>?download=1` | ⛔⛔ **HTTP 410（⭐ 逐个试了 README.md / schema.json / Results.xlsx，⛔ 全部 410）** |
| `https://api.datacite.org/dois/10.5281/zenodo.19819244` | ⭐ **200 —— ⭐ 元数据仍完整**（标题 / 作者 / ORCID / 描述 / license / version 1.0.0 / publicationYear 2026） |
| `https://api.crossref.org/works/10.5281/zenodo.19819244` | ⛔ **不存在**（⚠️ Zenodo 走 DataCite，⛔ 不走 Crossref） |

⭐ **tombstone 逐字**：`removal_reason.id` = **`test-record`** · `removal_date` = **`2026-05-03T13:34:35.515001+00:00`** · `deletion_policy.id` = `grace-period-v1` · `removed_by.user` = `1626688` · `citation_text` 指向 `https://doi.org/10.5281/zenodo.19819245`。

⚠️⚠️ **`test-record` 这个删除理由值得注意**：⭐ 它是 Zenodo 用于清理测试性上传的标记。⭐ 也就是说**这份 deposit 很可能是作者的一次测试上传，⛔ 后被 Zenodo 清理**。⭐ **正式 deposit 可能另在别处（⛔ 本轮未找到）。** ⛔ **后果：⛔ 这个 DOI 不可引用、⛔ 不可作为「资产可得」的证据。**

⚠️ **⛔ 一个未解的矛盾**：⭐ 文件在**本轮同一天 02:10** 被成功下载（⭐ 完整 10 文件），⛔ 而 06 分钟后（02:16）同样的 URL 已返回 410，⭐ 且 tombstone 的 `removal_date` 是 3 个多月前。⛔ **本轮无法解释这个时序** —— ⭐ 可能是 CDN / 缓存层短暂仍在服务。⛔ **无论如何：⛔ 现在拿不到了。**

### ⭐⭐ D.2 · 文件清单 · 大小 · 校验和

⚠️ **schema 里说「Zenodo API 直接给 md5，不必自己下完再算」—— ⛔ 但记录已删，API 的 `files[].checksum` 拿不到了。⭐ 所以下面的 md5 全部是我方对本地副本实算的（`md5sum`），⛔ 无法与 Zenodo 的原始校验和交叉验证。**

| # | 文件 | 大小（字节） | ⭐ md5（本地实算） | 内容（⭐ 已实际打开核验） |
| :-: | :-- | --: | :-- | :-- |
| 1 | ⭐⭐ `llm_traces.zip` | **127,897,632** | `f0c15aa42cf14ddde6a51a7886f1cfe0` | ⭐⭐ **192 个 `.jsonl`**（⭐ 解压 212,212,657 字节）· 6 目录 × 32 · ⭐ 见 B-ter |
| 2 | ⭐⭐ `test_oracle.zip` | **32,859,389** | `87a633c0e5bb866259f367d32ce33dd7` | ⭐ 2 文件：⭐ **`reference_data.mat`**（32,906,083 B，⭐ 参考轨迹）+ ⭐⭐ **`run_tests.m`**（3,718 B，⭐ 差分 oracle 源码） |
| 3 | ⭐ `mutated_simulink_models.zip` | **1,457,434** | `aa62f95df2f4ae03965b2ba98c1475f8` | ⭐ **32 个 faulty `.slx`**（4 目录 × `_v1`…`_v8`）+ 各自的 `_Script.m` |
| 4 | ⭐ `simulink_models.zip` | **356,492** | `1fb495ab30a3d95124dde8f679e84f2e` | ⭐ **4 个原始 `.slx`** + `_Script.m` + 2 个数据 `.mat`（14 项） |
| 5 | ⭐⭐ `mutation_injection.zip` | **11,421** | `eb27244acfd092b64b6674a27673dbbd` | ⭐⭐ **3 个 `.m`：`generateVariants.m` / `findAllSites.m` / `applyMutation.m`** —— ⭐ **变异分类学的全部源码** |
| 6 | ⭐⭐ `Results.xlsx` | **64,677** | `83ba7c8e0a9438e521ddb9cc298e90cb` | ⭐⭐ **7 sheet**（`Test` 汇总 + 6 个配置各一张）；⭐ 每张 81 行；⭐ 列 `MutationTag/MutationName/Site/Description/Fixed?/Variant/VariantTier/Score/Status/Cost/Time` |
| 7 | ⭐ `analysis.py` | **7,773** | `1dfccff25225a8456cd98c427a08449b` | ⭐ 按 tag / tier / base model 算 fix rate 并画图；⭐ **内含 Parametric/Structural 二分的官方定义** |
| 8 | ⭐ `usage_calc.py` | **7,641** | `82fd4391410ca1998d417923c60de6c7` | ⭐ 从 JSONL 算 token 与耗时；⭐ **内含三个模型的官方定价表** |
| 9 | `schema.json` | **623** | `c2ba820733cde7364410c3e374ef2905` | ⭐ `A.B.C.D` 文件名映射 |
| 10 | `README.md` | **378** | `a7097cf4552a7187b55c38d25dcc0dac` | ⭐ 命名规范（⚠️ 内含 "see paper Section X" 的**占位未填**） |
| — | ⭐ **合计** | ⭐ **162,663,460** | — | ⭐ 10 文件，⛔ **无缺失** |

### ⭐⭐ D.3 · 按 schema 的资源类型表

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| ⭐ **配套论文全文** | ⛔ **🟠** | [`10.2139/ssrn.7138608`](https://doi.org/10.2139/ssrn.7138608) | ⭐ **Crossref API 200**：标题 / 双作者 / 双 ORCID（均 `authenticated-orcid: true`）/ ⭐ **完整摘要**（⭐ 已逐字取回，⭐ 见 A 与 C）/ publisher `Elsevier BV` / type `posted-content` / deposit 2026-07-18。⛔⛔ **但 SSRN 页面 HTTP 403**（⭐ `www.ssrn.com/abstract=7138608` 与 DOI 跳转终点都是 403）→ ⛔ **正文拿不到**，⛔ 只有摘要。⛔ 未试：机构代理 / 作者主页 / Aaltodoc（⚠️ 本轮时间预算内未做） |
| ⭐⭐ **实验代码 · 变异注入器** | ⭐ **🟢（本地）/ ⛔ 🟠（在线）** | `mutation_injection.zip`（本地）；⛔ 在线 410 | ⭐ **实际打开并逐函数读完**：`applyMutation.m` 45 KB 含 16 个变异函数 + 12 个 helper；`findAllSites.m` 含每类算子的专用站点过滤器；`generateVariants.m` 含 4 档模板、加权采样、metadata 落表。⛔ **无 license 文件**（⭐ Zenodo 层是 CC-BY-4.0）。⛔ **无 git 仓库、无 HEAD sha** |
| ⭐⭐ **实验代码 · 测试 oracle** | ⭐ **🟢（本地）/ ⛔ 🟠（在线）** | `test_oracle.zip` | ⭐ **`run_tests.m` 全文已读**（⭐ 1% 归一化容差、全信号必过、异常兜底、失败画图）。⭐ **这是「hidden oracle」的实物** —— ⚠️ 即 agent 当时看不到的东西，⭐ 现在我们能看到 |
| ⭐ 分析脚本 | ⭐ **🟢（本地）** | `analysis.py` / `usage_calc.py` | ⭐ 两份全文已读；⭐ 依赖 pandas / numpy / matplotlib / openpyxl。⚠️ **`analysis.py` 的 `TARGET_SHEETS` 硬编码只跑 Sonnet 两张表**，⛔ 要跑全部 6 个配置需自行改（⭐ 我们已改并复算，见 C） |
| ⭐⭐ **数据集 / Benchmark** | ⭐ **🟢（本地）/ ⛔ 🟠（在线）** | `simulink_models.zip` + `mutated_simulink_models.zip` | ⭐ **条目数：4 base + 32 faulty variant**（⭐ 逐个在 zip 清单里核过）。⭐ **格式：`.slx`（⛔ 二进制、⛔ 专有）+ `.m` 脚本 + `.mat` 数据**。⭐⭐ **有 ground truth：⭐ `Results.xlsx` 的 `MutationTag`/`Site`/`Description` 三列构成逐条白盒真值**。⛔⛔ **但需 MATLAB/Simulink R2025b 许可证才能打开** → ⭐ **对我们实际上只有分类学与台账可用，⛔ 模型本身用不了** |
| ⭐⭐ **实验结果细则** | ⭐ **🟢（本地）** | `Results.xlsx` | ⭐⭐ **有逐条可下载结果**（⛔ 不只是论文内表格）：⭐ 6 配置 × 32 variant × 逐 mutation 的 `Fixed?`，⭐ 加逐 variant 的 `Score`/`Status`/`Cost`/`Time`。⭐ **我方已全部复算**（见 C 的表）。⛔ **无逐轮记录**（⛔ 那要回 JSONL 自己算） |
| ⭐⭐ **原始 agent 轨迹** | ⭐ **🟢（本地）/ ⛔ 🟠（在线）** | `llm_traces.zip` | ⭐⭐ **192 个完整会话日志，⭐ 逐工具调用 · 逐 token · 逐 stdout 全在。⭐ 这是本资产最独特的部分** —— ⛔ 绝大多数论文不放这个 |
| Artifact / 复现包 | ⛔ **🟠** | Zenodo DOI（⛔ tombstoned） | ⛔ **入口存在过但已删除** —— ⭐ 按 schema 的「入口存在但内容是空壳」条款的**同类情形**（⛔ 甚至更糟：⛔ 连壳都没了）→ ⛔ **判 🟠** |
| ⭐⭐ **prompt 是否公开** | ⭐⭐ **🟢（本地）** | `llm_traces.zip` 内每个 JSONL | ⭐⭐ **完全公开，逐字可取** —— ⭐ 系统提示（Codex 的 `base_instructions` / Claude 的首条 `queue-operation`）· ⭐ 任务提示（`user_message`）· ⭐ 甚至 collaboration-mode 的 developer instructions 全文。⭐ **比论文附录形式更强**（⭐ 是**当次实际发出的**文本，⛔ 不是事后整理版） |
| ⭐ 模型 seed / 随机性记录 | ⛔ **⚪** | — | ⛔ `generateVariants(baseModel, randomSeed, n)` **有 seed 参数**，⛔ 但**实际用值未落盘** → ⛔ **变异集不可精确重现** |

### ⭐ D.4 · ⛔ 复现门槛（⭐ 我方评估，**I 级**）

| 依赖 | 状态 |
| :-- | :-- |
| ⛔ **MATLAB + Simulink R2025b** | 🔒 **商业许可证** —— ⛔ 打开 `.slx` / 跑 oracle / 跑注入器都需要 |
| ⛔ **MATLAB_Simulink_MCP** 服务器 | ⛔ **⚪ 未在数据集内，⛔ 论文摘要说"We develop a MCP-based toolkit"但未给入口** → ⛔ **agent 侧无法复现** |
| ⛔ **Codex CLI 0.118.0 / Claude Code 2.1.92** | ⚠️ 具体版本已不易取得 |
| ⛔ **GPT-5.4 / 5.2 / Sonnet-4.6** | ⚠️ 需 API 额度（⭐ 总成本 $106.48 可参考） |

⭐⭐ **所以对我们真正可用的，⛔ 是「不需要 MATLAB 就能读」的那四样**：⭐⭐ **① 16 类变异分类学源码 · ② 192 条 JSONL 轨迹 · ③ `Results.xlsx` 逐条台账 · ④ `run_tests.m` oracle 设计**。⛔ **模型实物与 MCP toolkit 都用不上。**

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

1. ⭐⭐⭐ **变异分类学的「两族 + 组合难度模板 + 六列登记」这个形状，可以直接搬进 G1。** ⭐ 见 B-bis 的对位表：⭐ 搬 **parametric / structural 二分**（跨制品类型成立）、⭐ 搬 **`{参数}×a + {结构}×b` 的显式组合模板**、⭐ 搬 **`MutationTag / MutationName / Site / Description` 四列登记格式**（⭐ 尤其 `Description` 那列是人类可读缺陷陈述，⭐ 与我们的「期望发现」同构）。⛔ **不要搬 16 个类目名**（⛔ 块级 vs 语义级，对不上）。
2. ⭐⭐ **「缺陷由确定性注入器造，于是 ground truth 是白盒」这个设计消灭了分母争议。** ⭐ 他们不需要人工裁定「这算不算一条缺陷」—— ⭐ 注入了几条就是几条，⛔ 也没有「口径迁就结果」的空间。⚠️ 对照我们：⭐ 我们的 98 条能力分母是人工台账，⭐ 正在 G1 全量重标，⛔ 且历史上有过 `boundary_ruling` 逐条剔除。⭐⭐ **若 G1 能引入一条「机械注入 + 白盒真值」的补充语料，分母争议会一次性消失** —— ⭐ 这可能是本卡对我们最有价值的一条**方法论**建议（⛔ 不是数据建议）。
3. ⭐⭐ **oracle 对 agent 保持黑盒，是一条明确的防泄漏措施。** ⭐ 提示逐字写 "The test oracle is hidden and its source code is not available."。⭐ 对照我们 §3.5 的泄漏审查：⭐ **把判据实物与被判对象物理隔离**，与我们 §9.5 第 6 条「`protocol/` 与 `judges/` 的物理分离本身就是防泄漏机制」是同一个原则的另一种落法。⭐ 可以在我们的求值端借鉴（⛔ 目前我们的谓词判据对生成端是可见的）。
4. ⭐⭐ **run record 的资源计量粒度值得直接抄两条**：⭐ ① **`reasoning_output_tokens` 单列**；⭐ ② **cache 读 / 写分列**。⭐ 我们「修订机器吃 79% token」这个结论目前**分不出多少是 reasoning**，⛔ 而这直接影响「拆掉 reviewer 能省多少」的估算精度。⭐ 补记成本极低。
5. ⭐ **环境可审计性值得抄一条**：⭐ 把 **sandbox / 网络策略**（他们逐 turn 写 `network_access: false`）与**代码/宿主版本**落进 run record。⭐ 后者我们已知是缺口（§3.5.1 明写 run record 无代码版本字段）—— ⭐ **本卡提供了一个「别人连 CLI patch 版本都记」的外部对照，⭐ 可以拿来推动这条补记。**
6. ⭐⭐ **「41.1% 的格撞预算上限」为我们 §10 那条纪律提供了外部旁证。** ⭐ 在 agent 型修复流水线上，**四成格耗尽预算是常态**。⭐ 于是我们 v44 的 22/35 降级**不构成「方法失效」的证据**，⛔ 它是这类流水线的固有特征。⭐⭐ **而我们比他们强的地方在于：我们的降级带结构化诊断（能回答卡在哪条义务上），⛔ 他们只留下一个 `600`。** ⭐ 这一点可以在论文里当**方法学优势**写。
7. ⭐ **prompt 以「当次实际发出的原文」形式随数据发布**，⛔ 而不是事后整理的附录。⭐ 这个做法比附录强，⭐ 且成本为零（⭐ 只要不删日志）。⭐ 我们若将来放 artifact，可以照这个做。

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔ **它踩了我们已经用 `@k` 口径解决过的坑：每格只跑一次。** ⛔ 192 格 = 192 次单跑，⛔ 无重复、⛔ 无方差、⛔ 无 seed。⚠️ 而它的 agent 是**高方差**的（⛔ 同一格 full 与 ablated 的 token 差 4.6 倍）。⛔ **它的逐算子 fix rate（有 4 个算子 n=6）在统计上几乎不可用**，⛔ 却被 `analysis.py` 直接画成柱状图。⛔ **不要退回单轮口径。**
2. ⛔⛔ **预算耗尽与能力不足被混在一个 `Status=0` 里。** ⭐ 41.1% 的格撞 600 s，⛔ 但台账没有任何字段区分「它不会修」与「它没修完」。⚠️ 这正是我们 §10 明写要避免的：⛔ **降级必须留下「为什么没做到」的结构化诊断**。⛔ **不要照抄这个记录方式。**
3. ⛔⛔ **`Fixed?` 的逐 mutation 判定者与判据都没说明，⛔ 且出现 `0.5`。** ⭐ oracle 只给整体 pass/fail，⛔ 给不出逐条粒度；⭐ 而 `0.5` 只能来自人工判断。⛔ **无 $\kappa$、无一致率、无判据文档、未说几个人判。** ⚠️ 按我们 §3.5 的口径，⛔ **这一层判定不可审计**。⭐ 我们自己 574 位逐位判定 + 288 簇五类裁定的做法比它扎实得多，⛔ **不要因为「别人没做」而放松。**
4. ⛔⛔ **消融结论的措辞与数据不一致（方向性松紧不一致）。** ⭐ 摘要说 "reduces cost and generally improves"，⛔ 但实测 **3 个模型里降成本只成立 1 个、提升只成立 2 个**（⛔ Sonnet 方向相反）。⚠️ 按我们 §7.5 的要求，⛔ **这属于对自己有利方向的限定写得不足**。⛔ **我们写 −15.82pp 时不要犯反向的错**（⛔ 过度自我批评同样是失真）。
5. ⛔ **无任何 baseline。** ⛔ 没有非 agent 对照、⛔ 没有人类对照、⛔ 没有随机改对照。⭐ 于是 "74.7% fix rate" 这个数字**没有参照系** —— ⛔ 不知道它算好还是算差。⚠️ 对照我们：⭐ 我们至少自建了 X1 朴素基线（⭐ 即便它给出的是对我方不利的 76.2%）。⛔ **不要因为「别人也没有」就放弃 baseline。**
6. ⛔ **两个 agent 宿主构成混淆变量。** ⭐ GPT 侧用 Codex CLI，Claude 侧用 Claude Code。⛔ 于是「Sonnet-4.6 表现最差」**无法归因**到模型 —— ⛔ 可能是宿主的工具集、上下文管理或超时行为不同（⚠️ 而 Sonnet 侧的 `ToolSearch` / `TodoWrite` 确实是 Codex 侧没有的）。⛔ **模型对照必须控制宿主。**
7. ⛔ **数据集的长期可得性完全失败。** ⛔ Zenodo 记录被删（`test-record`），⛔ 论文正文 403。⚠️ **这意味着：⛔ 即便我们想在论文里引用它，也只能引 SSRN 预印本的摘要 + 我方本地副本的 md5** —— ⛔ 而后者别人验证不了。⭐ **教训：artifact 要放在真正的正式 deposit 上，⛔ 不要留在测试记录里。**

### 3. ⚠️ 与我们的关键差别

1. ⛔⛔ **制品完全不同：连续 / 混成动力学块图 vs 离散状态机。** ⭐ 它的缺陷是「Gain 值被换成倒数」「Switch 的两个输入被交换」「Lookup 断点被调换」；⭐ 我们的缺陷是「状态不可达」「守卫不互斥」「层次不一致」。⛔ **逐类算子零对位。** ⭐ 能迁移的只有**分族方式与登记格式**（B-bis 已列）。
2. ⛔⛔ **裁决者的性质不同，⛔ 而这决定了两套流水线的形状。** ⭐ 它有一个**可反复调用、给出可读诊断（失败信号名 + 对比图）的差分 oracle** —— ⭐ 于是 agent 能自己闭环，⛔ 根本不需要 reviewer / adjudicator 节点。⛔ **我们没有这样的 oracle**：⭐ pyfcstm 能求值单个谓词，⛔ 但「这份状态机与这份 NL 需求是否一致」没有可执行判据。⭐⭐ **这就是为什么我们不得不引入 LLM 裁决者，⛔ 也是为什么它们零收益** —— ⚠️ **本卡把这个因果讲清楚了：⛔ 缺的不是更好的 reviewer prompt，⭐ 缺的是一个可反复调用的判据。**
3. ⚠️ **它的任务是修复，⛔ 我们的任务是发现。** ⭐ 修复任务天然有闭环信号（⭐ 跑一下就知道好没好）；⛔ 发现任务没有（⛔ 「你没发现的那条」不会自己举手）。⛔ **所以它「agent 自主 tool loop」的极简形态我们照搬不了** —— ⭐ 我们的多节点编排不是过度设计，⛔ 而是缺少闭环信号的直接后果。
4. ⚠️ **闭合词表的位置相反。** ⭐ 它的 16 条闭合分类学在**注入侧**（agent 不知道）；⭐ 我们的 19 条闭合谓词在**检测侧**（LLM 从里面选）。⛔ **所以它对「闭合 + LLM 自动选」这个组合提供 0 个先例**（⭐ 与 LLM-FSM 那张卡一致）。
5. ⚠️ **成本量级差两个数量级。** ⭐ 它 192 次运行总共 **$106.48**（⭐ 均 $0.55/格）。⭐ 我们 324 格 + 修订机器的成本远高于此（⚠️ 具体倍数本轮未算）。⭐ **他们的成本纪律值得注意**：⛔ 600 s 硬上限虽然造成 41.1% 耗尽，⛔ 但也把总成本压在 100 美元级。
6. ⚠️ **它是 `界外`，⛔ 所以按本轨 §3 的防火墙，本卡的任何内容都不得直接进论文。** ⭐ 若要引用它的变异分类学做 Related Work 或出处，⛔ **必须回 L1 / L2 的门重走一遍**（⛔ 而它大概率过不了 L2 的出处轴 —— ⛔ 制品类型不匹配）。⭐ **它的价值纯粹在方法素材层面。**

---

## F. 存疑与未核项

1. ⛔⛔ **Zenodo 记录为何被标为 `test-record` 删除、正式 deposit 是否另在别处，未知** —— 已试过：⭐ DataCite API（⭐ 元数据在，⛔ 无替代 DOI）· ⭐ Zenodo API 记录 19819243/19819244/19819245（⭐ 19819243 是无关的第三方记录）· ⭐ `relatedIdentifiers`（⛔ 只有一条 `IsVersionOf` 指向自己）；⛔ 结果：**找不到替代入口**。⛔ 未试：给作者发信 · 查 Aaltodoc · 查 SSRN 附件。
2. ⛔⛔ **文件在 02:10 下载成功、02:16 返回 410，⛔ 而 tombstone 日期是 3 个月前 —— 这个时序无法解释** —— 已试过：⭐ 重试全部文件 URL 变体（`/records/.../files/...?download=1`、`/api/records/.../files`、concept id）；⛔ 结果：⛔ **全部 410 或 404**。⚠️ **推测是 CDN 缓存（I 级，⛔ 不写成事实）。** ⛔ **后果：本卡的一切实物断言依赖一份不可再取的本地副本，⛔ 其 md5 无法与官方校验和交叉验证。**
3. ⛔⛔ **消融的定义与 Sonnet 侧的实现不一致。** ⭐ 实测（⭐ 全 192 文件机械计数 `read_simulink_system` 出现次数）：GPT-5.2 **32/32 文件用**、GPT-5.2-Abl **0/32**、GPT-5.4 **32/32**、GPT-5.4-Abl **0/32** —— ⭐ **GPT 侧消融干净**。⛔⛔ **但 Sonnet-4.6-Abl 有 16/32 文件仍在用它（253 次提及）。** ⛔ **所以「ablated = 去掉 `read_simulink_system`」这个解释在 Sonnet 侧不成立。** ⛔ 未解：⛔ 是标注错误、⛔ 是配置泄漏、⛔ 还是 Sonnet 侧的消融是别的东西。⚠️ **若是配置泄漏，⛔ 则 Sonnet 那两列的消融对照无效** —— ⭐ 而那恰好是唯一方向相反的模型。⛔ **需读论文正文才能定，⛔ 而正文 403。**
4. ⛔ **摘要的 "93.1%" 与台账实算的 92.5%（74/80）对不上** —— 已试过：⭐ 逐值 dump GPT-5.4 sheet 的 `Fixed?` 列（⭐ 80 行，⛔ 全为 0/1 二值：74 个 1、6 个 0）· ⭐ 试过 mean-Score 口径（**94.5%**）；⛔ 结果：⛔ **两个口径都不是 93.1%**。⛔ 未解：⛔ 分母可能不同（⭐ 93.1% = 74.5/80）、⛔ 或论文用的是更早的数据版本。⚠️ **本卡一律报我方复算值并标明口径。**
5. ⛔ **`Fixed?` 逐 mutation 的判定者、判据、`0.5` 的含义未知** —— 已试过：⭐ 读 `README.md`（⛔ 378 字节，⛔ 内含未填的 "see paper Section X"）· ⭐ 读 `analysis.py`（⭐ 只有 `>1 则 /100` 的清洗，⛔ 无判据说明）· ⭐ 读 `run_tests.m`（⛔ 只给整体 pass/fail）；⛔ 结果：⛔ **无文档**。⭐ 我方推断是人工归因（**I 级**）。
6. ⛔ **变异注入时用的 `randomSeed` 未落盘** —— ⭐ `generateVariants(baseModel, randomSeed, n)` 签名里有，⛔ 但 `Results.xlsx` 与 README 都没记 → ⛔ **32 个 variant 不可精确重现**。
7. ⚠️ **`generateVariants.m` 的头注释描述了一个「注入后调用 oracle 确认失败，不失败就重来」的设计，⛔ 但代码里没有任何 oracle 调用。** 逐字注释：`"check if oracle fails or passes, if it fails repeat, otherwise move to next level"`。⛔ **实现与注释不一致** → ⚠️ **可能存在「注入了但语义未改变」的等价变异（equivalent mutant）未被剔除**。⛔ 未核：⛔ 无法在无 MATLAB 环境下验证。⚠️ **若真有等价变异混入，⛔ 则 fix rate 的分母偏大（⭐ 有些"没修好"其实根本没坏）。**
8. ⛔ **MCP toolkit（`MATLAB_Simulink_MCP`）未随数据发布** —— 已试过：⭐ 通查 10 个文件（⛔ 无服务器代码）· ⭐ 摘要逐字 "We develop a Model Context Protocol (MCP)-based toolkit"（⛔ 无入口）；⛔ 结果：⛔ **⚪ 未提供** → ⛔ **agent 侧不可复现**。⛔ 未试：⛔ GitHub 搜（⚠️ 本轮时间预算内未做）。
9. ⛔ **配套论文正文不可得** —— 已试过：⭐ `doi.org` 跳转（⛔ 403）· ⭐ `www.ssrn.com/abstract=7138608`（⛔ 403）· ⭐ WebSearch 两轮（⛔ 未命中该标题）；⭐ **但通过 ORCID works API 定位到了它**（⭐ 这是本轮成功的路径），⭐ 并从 Crossref 取到**完整摘要**。⛔ 未试：⛔ 机构代理 · ⛔ Aaltodoc · ⛔ 作者主页 · ⛔ 给作者发信。⚠️ **后果：⛔ 「fault variant B=1–8 对应 paper Section X」这个映射的正文说明、⛔ 600 s 上限的官方说法、⛔ 消融的官方定义、⛔ 93.1% 的分母口径，⛔ 四件事都只能靠推断。**
10. ⚠️ **4 个基础模型的复杂度（块数 / 层深）未量化** —— ⛔ 论文说「复杂度比变异数更重要」，⛔ 但**没给复杂度的度量**。⭐ 我方只能用 `.slx` 字节数当粗代理（⭐ Elevator 138 KB · Hydraulic 132 KB · Parallel_Hybrid 61 KB · Buoy 41 KB）—— ⚠️ **而这个代理与结果不相关**（⛔ 最小的 Parallel_Hybrid 反而最难，43.3%）。⛔ **所以「复杂度」指的是什么，本轮无法确定。**
11. ⚠️ **`Sonnet-4.6` sheet 的 `max_row` 是 113 而其他是 81** —— ⭐ 已核：⛔ 82–113 行全空（⭐ 逐行 dump 确认），⛔ 是残留格式而非隐藏数据。⭐ **不影响统计。**
12. ⚠️ **Yosys / 其它第三方依赖本轮未跑 `tools.verify_assets`** —— ⭐ 本卡唯一跑过该工具的是 `fsm2sv`（⚠️ 那属于另一张卡）。⛔ 本卡的资产核验全部靠**本地实物打开**，⛔ 不是靠该工具（⭐ 因为对象是 Zenodo 而非 GitHub，⛔ 工具不适用）。
