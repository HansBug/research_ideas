# `baselines_double_green/` — 双绿 NL→STM 核心数据资产

## 0. 这是什么

本目录是 `project_1` 的 **核心数据资产入口**：4 个公开 NL→STM baseline 论文的数据集已经被解析、清洗、parquet 化、人评字段对齐，所有 21 个 parquet 文件统一落在这里管理。

> **"双绿"含义**：在 [`../../baselines/SUMMARY.md`](../../baselines/SUMMARY.md) §`数据集与 Benchmark 清单` 口径下，这 4 篇论文的 `BASELINE评估` 与 `数据集可获取性` 都达到 🟢（直接 baseline 对比 + 可立即获取）；区别于其他 `🟢/🟠` 或 `🟢/🔒` 混搭的论文。

## 1. 来路（这些 parquet 怎么来的）

- **原始解析记录**：[`../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md)（1885 行，含每个数据集的原始来源、字段说明、3 个真实例子和 §11 复用性最终判断）
- **生成脚本**：[`../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_parquets.py`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_parquets.py) 与 [`build_baseline_double_green_human_review_parquets.py`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_human_review_parquets.py)（保留在原 discussion 资产目录，作为该 discussion 的产物）
- **物理迁移**：parquet 在 2026-05-09 从原 `.assets/` 移到当前目录，作为对外的核心资产入口；discussion 仍是真源解释文档

## 2. 4 个数据集一览

| # | 数据集 | 论文 | 任务 | 输出元模型 | 公开链接 | 规模 | 适合做什么 |
|---|--------|------|------|------------|----------|------|------------|
| 1 | `llms_emp` | [Generating SysML Behavior Models via LLMs (2025)](../../baselines/llms_emp/) | NL → PlantUML 行为模型 | SysML STM/ACT/SD（PlantUML） | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 107 原始 / 98 完整 / 192 人评 | **主样本级 benchmark**（最完整） |
| 2 | `ttool_ai` | [System Architects Are not Alone Anymore (2024)](../../baselines/ttool-ai/) | NL → AVATAR 设计模型 | TTool AVATAR (含状态机) | [GitHub zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) | 3 真实案例 / 15 model 变体 / 122 SM panel / 708 状态 / 798 迁移 / 116 人评 | **时间约束 + 层次** baseline |
| 3 | `light_control_nimbus` | [Nimbus Light-Control Case Study (2000)](../../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/) | NL → RSML-e 层次状态机 | RSML-e | [PDF + Dagstuhl 挑战题](https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf) | 2 文档 / 4 片段 / 17 变量 / 20 状态 / 16 规则 | **V&V 流程 + HSM** 参考 |
| 4 | `structure_event_driven` | [Structure- and Event-Driven Frameworks (2026)](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) | NL → UML 状态机（Umple） | UML state machine (Umple) | [匿名工件](https://anonymous.4open.science/r/llm_state_machine_modeling/) | 9 case（8 paper-eval + 1 课堂）/ 6 完整 Umple 文本 / 8 完整组件计数 GT / 512 metric / 512 人评 | **逐组件 TP/FP/FN/F1 benchmark** |

> **§11 复用性最终判断（来自 discussion）**：`llms_emp` 主样本级 + `structure_event_driven` 组件级，两者并用是最适合的统一 benchmark 主干；`ttool_ai` 保留为人工总评分协议 + 工具链对比来源；`light_control_nimbus` 保留为 V&V 流程参考。

## 3. parquet 文件索引

### 3.1 跨数据集汇总（4 个 parquet）

| 文件 | 行数 | 列数 | 内容 |
|------|------|------|------|
| `baseline_double_green_dataset_catalog.parquet` | 4 | 8 | 4 个数据集的元数据（id / paper_slug / dataset_name / output_metamodel / sample_granularity / 规模 / notes） |
| `baseline_double_green_human_review_availability.parquet` | 4 | 9 | 4 篇人评公开可用性总表（input/ref/pred 是否可用 + 缺口说明） |
| `baseline_double_green_human_review_protocols.parquet` | 4 | 15 | 4 篇人评方法复原（reviewer pool / 评审维度 / 执行步骤 / 匹配规则 + 论文原文摘录） |
| `baseline_double_green_human_review_records.parquet` | 820 | 34 | 跨论文统一人评记录总表（按 paper_slug + record_type + review_record_id 索引） |

### 3.2 `llms_emp`（3 个 parquet）

| 文件 | 行数 | 内容 |
|------|------|------|
| `llms_emp_raw_samples.parquet` | 107 | 公开账本原始 107 行 |
| `llms_emp_complete_samples.parquet` | 98 | 同时含 input + output 的完整实验样本（38 STM / 21 ACT / 39 SD） |
| `llms_emp_human_review.parquet` | 192 | 公开逐样本人评结果（input + ref + pred + 评分 + 原文摘录） |

### 3.3 `ttool_ai`（5 个 parquet）

| 文件 | 行数 | 内容 |
|------|------|------|
| `ttool_ai_models.parquet` | 15 | 15 个 AVATAR 设计模型（system spec + raw XML + 块/SM panel 计数） |
| `ttool_ai_state_machine_panels.parquet` | 122 | 122 个状态机面板（panel-level XML） |
| `ttool_ai_states.parquet` | 708 | 摊平后的 708 个状态节点（含坐标、连接点） |
| `ttool_ai_transitions.parquet` | 798 | 摊平后的 798 条迁移（**含 `after_min` / `after_max` / `delay_distribution_law` / `probability` 时间约束字段**） |
| `ttool_ai_human_review.parquet` | 116 | 公开人评（含 case / split / overall 等多类记录） |

### 3.4 `light_control_nimbus`（5 个 parquet）

| 文件 | 行数 | 内容 |
|------|------|------|
| `light_control_nimbus_documents.parquet` | 2 | 2 份原文（Dagstuhl 挑战题 + Nimbus JUCS 论文） |
| `light_control_nimbus_fragments.parquet` | 4 | 4 个可实验片段（NL 需求 + RSML-e 输出） |
| `light_control_nimbus_variables.parquet` | 17 | monitored / controlled 变量（含 range_or_type） |
| `light_control_nimbus_states.parquet` | 20 | 层次状态节点（parent_state_name + depth） |
| `light_control_nimbus_rules.parquet` | 16 | RSML-e 规则（target_variable + assigned_value + condition） |

### 3.5 `structure_event_driven`（4 个 parquet）

| 文件 | 行数 | 内容 |
|------|------|------|
| `structure_event_driven_cases.parquet` | 9 | 9 个评测 case（system_description + reference 图 + nshot 来源） |
| `structure_event_driven_reference_solutions.parquet` | 9 | 9 行；其中 5 个 paper-eval + 1 个课堂 case（共 6 个）含完整 Umple `reference_solution_text`；其余 3 个 paper-eval（Bread Maker / W-UMPLE / SSC7）只有图像 + 7 类组件计数（states / transitions / guards / actions / hierarchical / history / parallel） |
| `structure_event_driven_metrics.parquet` | 512 | 逐组件 TP/FN/FP/precision/recall/f1（按 strategy × LLM × case × component） |
| `structure_event_driven_human_review.parquet` | 512 | 统一字段人评（含原始 xlsx 评分行 + 论文评审规则摘录） |

## 4. 真实数据例子（每集 1 条）

完整 3 例样本见 [discussion §3.4 / §4.4 / §5.4 / §6.4](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md)。下面给最短的 1 条快速感知：

### `llms_emp` — 火车基础制动装置 STM（5 状态 7 迁移）

```
INPUT (NL):
  This state machine model represents the train's basic braking device, which
  serves as the final execution unit for train braking operations. When the basic
  braking device receives a brake signal, it transitions from the initial state
  to the braking state. ...

OUTPUT (PlantUML):
  @startuml
  [*] --> Initial_State
  Initial_State --> Braking_State : Signal_sent_successfully
  Initial_State --> Running_State : Signal_sending_failed
  Braking_State --> Brake_Caliper_Closed_State
  Running_State --> Initial_State : Send_signal_feedback
  ...
  @enduml
```

### `ttool_ai` — Platooning Platoon1（23 状态 47 迁移 6 SM panel）

```
INPUT (input_spec_text):
  Platooning is a transportation technique that consists in grouping trucks or
  vehicles together to reduce CO2 emissions. A platoon consists of one or several
  vehicles, the first one in the platoon playing the role of the platoon leader,
  the other ones playing the role of followers. ...

OUTPUT (AVATAR XML):
  per-state coordinates + per-transition含 after_min/after_max/delay_distribution_law/probability
```

### `light_control_nimbus` — 房间状态层次（U1-U11 → 层次 RSML-e）

```
INPUT (input_requirement_text):
  U1: If a person occupies a room, the light has to be sufficient to move safely,
      if nothing else is desired by a chosen light scene.
  U3: If the room is reoccupied within T1 minutes after the last person has left
      the room, the last chosen light scene has to be reestablished.
  ...

OUTPUT (层次状态名):
  Light_Control_System_Room
    ├── Light_Maintenance_Modes (Room_Occupied / Room_Empty / Occupancy_Undetectable)
    ├── Chosen_Light_Scene (parallel)
    └── Failure_Modes (parallel: Ok / Failed)
```

### `structure_event_driven` — Printer（6 状态 17 迁移 6 guards 3 actions 2 hierarchical）

```
INPUT (system_description):
  The printer has a master switch which turns the printer on or off. Once the printer
  is turned on, a user needs to log in before being able to print or scan a document. ...

REF (Umple):
  class Printer{
   sm {
     Off { on -> On; }
     On {
       off -> Off;
       Idle { login(cardID) [idAuthorized(cardID)] / {action="none";} -> Ready; ... }
       Ready { ... start [action=="scan" && originalLoaded()] -> ScanAndEmail; ... }
   }}
```

## 5. 导出脚本（[`scripts/`](./scripts/)）

把这些 parquet 转成常见 NL→STM benchmark 范式的现成脚本，**无需自己写 pandas**：

| 脚本 | 范式 | 用途 |
|------|------|------|
| [`scripts/export_nl_input.py`](./scripts/export_nl_input.py) | 仅 NL 输入 | 跨数据集统一 NL 输入语料（用于 retrieval / clustering / NL 难度分析） |
| [`scripts/export_nl_to_stm.py`](./scripts/export_nl_to_stm.py) | NL input + reference STM | 标准 generation benchmark（input → expected output） |
| [`scripts/export_human_review.py`](./scripts/export_human_review.py) | 含 input + ref + pred + score | reviewer / judge benchmark（评估 LLM-as-judge 的训练或测试集） |
| [`scripts/export_unified_benchmark.py`](./scripts/export_unified_benchmark.py) | 统一格式总表 | 跨 4 数据集导出统一 schema 的 jsonl/parquet |

通用调用方式：

```bash
# 默认 jsonl 输出到 stdout
python scripts/export_nl_to_stm.py --dataset llms_emp

# 限定数据集 + 写文件
python scripts/export_nl_to_stm.py --dataset all --output /tmp/nl2stm.jsonl

# 同时输出 parquet（便于后续做 pandas 实验）
python scripts/export_unified_benchmark.py --dataset all --output /tmp/bench.parquet --format parquet

# 只保留 STM（剔除 ACT/SD）
python scripts/export_nl_to_stm.py --dataset llms_emp --diagram-type stm
```

每个脚本都支持 `--help` 查看完整参数。

## 6. 关联资料（反向引用）

| 资源 | 路径 |
|------|------|
| 解析与 parquet 化原始记录 | [`../../discussions/2026-04-15-01-03-52-...parquet化.md`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md) |
| baselines 文库总账（含 §数据集可获取性口径） | [`../../baselines/SUMMARY.md`](../../baselines/SUMMARY.md) |
| baselines 操作规范 | [`../../baselines/GUIDE.md`](../../baselines/GUIDE.md) |
| 4 篇论文的单篇 DESC | 见 §2 表格中的 `论文` 链接 |
| 4 篇论文的 review_extraction（人评细节） | `../../state_machine_review_corpus/<slug>/review_extraction.md`（如适用） |
| 配套讨论 — 双绿输入文本与 sources 样例对比 | [`../../discussions/2026-04-15-14-51-21-AI-讨论-baselines双绿输入文本与sources样例对比及评测口径分析.md`](../../discussions/2026-04-15-14-51-21-AI-讨论-baselines双绿输入文本与sources样例对比及评测口径分析.md) |

## 7. 给后续研究者 / AI 的导航

### 7.1 想做什么 → 该看哪个

- **比较 LLM 在 NL→STM 上的生成质量** → 用 `llms_emp_complete_samples` + `structure_event_driven_cases`；优先选这两个数据集，因为它们都是 input + reference 完整对齐
- **评估 reviewer / LLM-as-judge** → 用 `*_human_review.parquet`，特别是 `baseline_double_green_human_review_records.parquet`（820 行统一字段）
- **做带时间约束的状态机生成** → 用 `ttool_ai_transitions.parquet`，里面 `after_min` / `after_max` / `delay_distribution_law` / `probability` 字段就是时间自动机语义
- **做层次/平行状态机生成** → 用 `light_control_nimbus_states.parquet`（depth + parent）和 `structure_event_driven_reference_solutions.parquet`（hierarchical / parallel 计数）
- **构造 retrieval 语料 / clustering 输入** → 用 `scripts/export_nl_input.py --dataset all`

### 7.2 注意事项

1. **本目录是 4 个数据集的 single source of truth for parquet 落盘位置**；任何 parquet 修改都应在生成脚本（`../../discussions/.../*.assets/build_*.py`）中统一处理，不要手工编辑 parquet
2. **可获取性 / 规模 / 链接的事实源是 [`../../baselines/SUMMARY.md`](../../baselines/SUMMARY.md) §数据集与 Benchmark 清单**，本 README 是数据资产视角的派生展示；冲突时以 SUMMARY 为准
3. **不要把 parquet 复制到其他位置**；下游用 `pd.read_parquet("project_1_llm_state_machine_modeling/data/baselines_double_green/<file>.parquet")` 直接读
4. **数据扩展规则**：若新增第 5 个数据集（同样达到双绿），应在 catalog parquet 中新增一行 + 在本 README §2/§3 各加一节 + 在 generate 脚本中新增一段；新增前先确认它在 `../../baselines/SUMMARY.md` §数据集与 Benchmark 清单 中已经有 🟢/🟢 双绿评估
5. **不可作为重新审查 baselines 数据集可获取性的入口**：那是 `baselines/GUIDE.md` §5.3 / §6.7 的职责
