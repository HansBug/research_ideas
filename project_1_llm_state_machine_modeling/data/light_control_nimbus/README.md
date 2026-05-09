# `light_control_nimbus/` — Nimbus Light-Control Case Study (2000)

## 论文与上游引用

- **论文**：Thompson, Whalen, Heimdahl, *Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study*, **JUCS** 6(7), 2000. [PDF](https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf)
- **配套挑战题**：[Dagstuhl Light Control System Case Study](https://www.cs.uni-saarland.de/lehre/2005/advanced_st/papers/Light%20Control%20Case%20Study.pdf)
- **baselines 单篇分析**：[`../../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/`](../../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/)
- **可获取性**：🟢（两份 PDF 公开下载；案例规格在论文正文）

## 任务

经典 NL → RSML-e 层次状态机案例。**不是公开的 LLM benchmark**，而是把论文中"Light Control 参考问题 + RSML-e 状态机规格"重建为可实验片段。

## 文件总览

| 文件 | 行数 × 列数 | 简介 |
|------|------------|------|
| [`simple.parquet`](./simple.parquet) | 4 × 6 | **格式统一表**（与其他 3 个 paper 同 schema：id/input/expected/predicted/model/notes）；本数据集 predicted/model 全 None |
| [`fragments.parquet`](./fragments.parquet) | 4 × 11 | 4 个可实验 NL→RSML-e 片段（input + output） |
| [`documents.parquet`](./documents.parquet) | 2 × 8 | 2 份原始文档全文 |
| [`variables.parquet`](./variables.parquet) | 17 × 7 | 17 个 monitored / controlled 变量 |
| [`states.parquet`](./states.parquet) | 20 × 7 | 20 个层次状态节点 |
| [`rules.parquet`](./rules.parquet) | 16 × 8 | 16 条 RSML-e 规则 |
| [`raw/`](./raw/) | — | 2 PDF + 2 txt 抽取本（已下载） |

---

## `simple.parquet`（4 行 × 6 列）

最简单的入口。各 paper 的 `simple.parquet` schema 相同，便于跨数据集统一处理。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `id` | str | 全数据集唯一 id，格式 `light_control_nimbus::<case_id>::<fragment_id>` | `light_control_nimbus::light_control_room::room_state_hierarchy_req` |
| `input` | str | 自然语言输入（U1-U11 等需求条目） | `U1: If a person occupies a room, the light has to be sufficient ...` |
| `expected` | str | 期望的 RSML-e 输出片段（层次状态名 / 变量 / 规则） | `Light_Control_System_Room Light_Maintenance_Modes Room_Occupied ...` |
| `predicted` | str / None | LLM 预测输出（**本数据集全 None**：论文非 LLM 工作） | `_None_` |
| `model` | str / None | LLM 名（**本数据集全 None**） | `_None_` |
| `notes` | str | 切片信息：case / fragment / abstraction / sample_kind | `case=light_control_room; fragment=room_state_hierarchy_req; abstraction=REQ; sample_kind=state_hierarchy` |

---

## `fragments.parquet`（4 行 × 11 列）

4 个 NL→RSML-e 重建片段，每行一个独立可实验单元。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id（固定 `light_control_nimbus`） | `light_control_nimbus` |
| `case_id` | str | 案例 id（4 个片段同属一个 case `light_control_room`） | `light_control_room` |
| `fragment_id` | str | 片段 id，全局唯一 | `room_state_hierarchy_req` |
| `fragment_title` | str | 片段标题（人类可读） | `Room-level RSML-e state hierarchy` |
| `abstraction_level` | str | 抽象层级（`REQ` 需求层 / `SOFT` 软件层） | `REQ` |
| `sample_kind` | str | 样本种类（`state_hierarchy` / `occupancy_logic` / `failure_modes` 等） | `state_hierarchy` |
| `input_requirement_ids_json` | str (JSON list) | 该片段引用的需求条目 id 列表 | `["U1", "U2", "U3", "U4", "U11", "U12", ...]` |
| `input_requirement_text` | str | 需求原文（U1-U11 等） | `U1: If a person occupies a room, the light has to be sufficient ...` |
| `output_metamodel` | str | 输出元模型（RSML-e 哪一类对象） | `RSML-e hierarchical and parallel state variables` |
| `output_fragment_excerpt` | str | RSML-e 输出片段（状态名 / 规则的文本表示） | `Light_Control_System_Room Light_Maintenance_Modes Room_Occupied ...` |
| `source_line_refs_json` | str (JSON dict) | 输出来源在原文中的行号定位 | `{"nimbus_case_study": [295, 309]}` |

---

## `documents.parquet`（2 行 × 8 列）

2 份原始文档（Dagstuhl 挑战题 + Nimbus JUCS 论文）的全文。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `light_control_nimbus` |
| `document_id` | str | 文档 id | `dagstuhl_light_control_case_study` |
| `title` | str | 文档标题 | `Dagstuhl Light Control System case study` |
| `document_role` | str | 角色：`Original informal requirements` 或 `Formal RSML-e specification` | `Original informal requirements` |
| `source_url` | str | 原始下载 URL | `https://www.cs.uni-saarland.de/lehre/2005/advanced_st/papers/Light Control Case Study.pdf` |
| `local_path` | str | **相对本 parquet 文件**的本地路径 | `./raw/light-control-original-case-study.txt` |
| `text` | str | 文档全文（PDF → txt 抽取后的文本） | `--- Page 1 --- Dagstuhl Seminar - Case Study Page 1 ...` |
| `alternate_source_url` | str | 备用下载 URL | `https://www.jucs.org/jucs_6_7/requirements_capture_and_evaluation/...` |

---

## `variables.parquet`（17 行 × 7 列）

17 个 monitored / controlled 变量字典。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `light_control_nimbus` |
| `case_id` | str | 案例 id | `light_control_room` |
| `variable_name` | str | 变量名（自由文本） | `Light Level` |
| `variable_group` | str | 变量类别（`monitored` 输入 / `controlled` 输出） | `monitored` |
| `range_or_type` | str | 取值范围或类型 | `0..10000 lux` |
| `description` | str | 变量含义说明 | `The amount of light in the room` |
| `output_metamodel` | str | 元模型分类 | `RSML-e monitored / controlled variable dictionary` |

---

## `states.parquet`（20 行 × 7 列）

20 个层次状态节点摊平表。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `light_control_nimbus` |
| `case_id` | str | 案例 id | `light_control_room` |
| `fragment_id` | str | 所属 fragment id | `room_state_hierarchy_req` |
| `state_name` | str | 状态名 | `Light_Control_System_Room` |
| `parent_state_name` | str | 父状态名（顶层状态自指） | `Light_Control_System_Room` |
| `depth` | int | 层次深度（0 = 顶层；2 = 二级嵌套；以此类推） | `0` |
| `output_metamodel` | str | 元模型类别 | `RSML-e state hierarchy` |

---

## `rules.parquet`（16 行 × 8 列）

16 条 RSML-e 规则（target_variable 在某个 condition 下被赋为 assigned_value）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `light_control_nimbus` |
| `case_id` | str | 案例 id | `light_control_room` |
| `fragment_id` | str | 所属 fragment id | `room_state_hierarchy_req` |
| `target_variable` | str | 被赋值的状态变量名 | `Light_Maintenance_Modes` |
| `assigned_value` | str | 赋的值（状态/变量名或常量） | `Room_Occupied` |
| `condition` | str | 触发条件（自然语言或形式化表达式） | `Occupied_InVar = TRUE && Occupied_Detectable_InVar = TRUE` |
| `abstraction_level` | str | 规则抽象层级 | `REQ` |
| `output_metamodel` | str | 元模型类别 | `RSML-e assignment / transition rule` |

---

## `raw/` 原始资源（✅ 已下载）

| 文件 | 大小 | 来源 |
|------|------|------|
| `light-case-jucs.pdf` | 211K | [umn.edu](https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf) |
| `light-case-jucs.txt` | 68K | 上面 PDF 的 `tools/pdf_extractor` 文本提取本 |
| `Light_Control_Case_Study.pdf` | 12K | [Semantic Scholar synopsis](https://pdfs.semanticscholar.org/3a2f/1fb69fa1fa109e9a25343c379a81cb3744f2.pdf)（原 Dagstuhl 1992 链接已失效，用 4 页 synopsis 替代） |
| `light-control-original-case-study.txt` | 9K | 上面 PDF 的文本提取本 |

`documents.parquet` 中 `local_path` 字段已指向上述 txt 文件（相对当前 parquet 同级 `./raw/...`）。

## 复用性建议

- ❌ **不是公开评分数据集**：0 行人评，仅 2 文档原文 + 4 重建片段
- ✅ **最适合做 V&V 流程参考**：人工 inspection / formal verification / simulation 三联流程的方法学样本
- ✅ **HSM + 时间约束**经典样本：U3/U4 中 `T1 分钟`、平行区域、故障模式都是控制系统建模的常见诉求
- ⚠️ 输入是已被论文重建的 NL 片段，不是开放原文需求；做对比时记得它本质是"案例改写后的样本"
