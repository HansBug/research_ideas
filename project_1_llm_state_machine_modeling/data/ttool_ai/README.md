# `ttool_ai/` — System Architects Are not Alone Anymore (2024)

## 论文与上游引用

- **论文**：Apvrille & Sultan, *System Architects Are not Alone Anymore: Automatic System Modeling with AI*, **MODELSWARD 2024**. [会议页](https://www.scitepress.org/PublishedPapers/2024/123917/)
- **baselines 单篇分析**：[`../../baselines/ttool-ai/`](../../baselines/ttool-ai/)
- **数据集公开入口**：[GitHub zebradile/ttool-ai](https://github.com/zebradile/ttool-ai)
- **可获取性**：🟢（GitHub 公开）

## 任务

NL 系统规范 → AVATAR (TTool 元模型) 设计模型，含 block diagrams + 状态机 panels。

**关键特性**：transition 字段含 `after_min` / `after_max` / `delay_distribution_law` / `probability` —— 直接编码**时间自动机语义**与**概率迁移**。

## 文件总览

| 文件 | 行数 × 列数 | 简介 |
|------|------------|------|
| [`simple.parquet`](./simple.parquet) | 15 × 6 | **格式统一表**（与其他 3 个 paper 同 schema） |
| [`models.parquet`](./models.parquet) | 15 × 21 | 15 个 AVATAR 设计模型（system spec + raw_xml + panel 计数） |
| [`state_machine_panels.parquet`](./state_machine_panels.parquet) | 122 × 15 | 122 个状态机面板（panel-level XML + state/transition 计数） |
| [`states.parquet`](./states.parquet) | 708 × 17 | 摊平后的 708 状态节点（含坐标 / 类型 / 连接点） |
| [`transitions.parquet`](./transitions.parquet) | 798 × 26 | 摊平后的 798 迁移（**含时间约束 + 概率字段**） |
| [`human_review.parquet`](./human_review.parquet) | 116 × 29 | 公开人评结果（多类记录：case-level / split-level / overall） |
| [`raw/`](./raw/) | — | 3 spec.md + 3 .xml + results.ods（GitHub） |

---

## `simple.parquet`（15 行 × 6 列）

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `id` | str | 全数据集唯一 id，格式 `ttool_ai::<case_name>::<variant_name>` | `ttool_ai::Platooning::Platoon1` |
| `input` | str | 自然语言系统规范（输入） | `Platooning is a transportation technique that consists in grouping trucks ...` |
| `expected` | str / None | 期望输出（**本数据集全 None**：论文未公开 reference output） | _None_ |
| `predicted` | str | LLM 输出 = 完整 AVATAR XML | `<?xml version="1.0" encoding="UTF-8"?><TURTLEGMODELING ...` |
| `model` | str | 论文使用的 LLM 后端（统一标 GPT-4） | `TTool-AI workflow (GPT-4)` |
| `notes` | str | 切片信息：case / variant / modeling_type / 状态数 / 迁移数 | `case=Platooning; variant=Platoon1; modeling_type=AVATAR Design; states=23; transitions=47` |

---

## `models.parquet`（15 行 × 21 列）

15 个 AVATAR 设计模型（一行一个 variant）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `ttool_ai` |
| `dataset_name` | str | 数据集名 | `TTool-AI AVATAR design artifacts` |
| `dataset_source_url` | str | GitHub URL | `https://github.com/zebradile/ttool-ai` |
| `case_id` | str | 案例 id（小写下划线） | `platooning` |
| `case_name` | str | 案例名（驼峰） | `Platooning` |
| `model_id` | str | 模型 id，格式 `<case_id>::<variant_name>` | `platooning::Platoon1` |
| `variant_name` | str | 该案例下的变体名（如 `Platoon1` / `Platoon2`） | `Platoon1` |
| `modeling_type` | str | 建模类型（固定 `AVATAR Design`） | `AVATAR Design` |
| `output_metamodel` | str | 输出元模型描述 | `TTool AVATAR design model with block diagrams and state machines` |
| `input_spec_text` | str | 系统规范输入文本 | `Platooning is a transportation technique ...` |
| `spec_path` | str | 规范文件相对路径 | `./raw/platooning/platoonings.md` |
| `xml_path` | str | XML 文件相对路径 | `./raw/platooning/platoonings.xml` |
| `raw_xml` | str | 完整 AVATAR XML 文本 | `<?xml version="1.0" encoding="UTF-8"?><TURTLEGMODELING ...` |
| `block_panel_names_json` | str (JSON list) | block diagram panel 名列表 | `["Platooning"]` |
| `state_machine_panel_names_json` | str (JSON list) | 状态机 panel 名列表 | `["Camera", "EmergencyBrake", "Engine", ...]` |
| `block_panel_count` | int | block diagram panel 数 | `1` |
| `state_machine_panel_count` | int | 状态机 panel 数 | `6` |
| `state_count` | int | 总状态节点数（跨所有 SM panel） | `23` |
| `transition_count` | int | 总迁移数 | `47` |
| `nonempty_guard_count` | int | 非空 guard 的迁移数 | `5` |
| `nonempty_action_count` | int | 非空 action 的迁移数 | `2` |

---

## `state_machine_panels.parquet`（122 行 × 15 列）

122 个状态机 panel（一行一个 panel；同一 model 通常有多个 panel，对应不同子系统）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `ttool_ai` |
| `case_id` | str | 案例 id | `platooning` |
| `case_name` | str | 案例名 | `Platooning` |
| `variant_name` | str | 变体名 | `Platoon1` |
| `model_id` | str | 所属 model id | `platooning::Platoon1` |
| `panel_id` | str | panel 全局 id（`<model_id>::<panel_name>`） | `platooning::Platoon1::Camera` |
| `panel_name` | str | panel 名 | `Camera` |
| `panel_type` | str | panel 类型（固定 `AVATARStateMachineDiagramPanel`） | `AVATARStateMachineDiagramPanel` |
| `input_spec_text` | str | 该 model 的系统规范文本（model 内 panel 共享） | `Platooning is a transportation technique ...` |
| `state_count` | int | 该 panel 的状态节点数 | `4` |
| `start_pseudostate_count` | int | 起始伪状态数 | `1` |
| `transition_count` | int | 该 panel 的迁移数 | `14` |
| `nonempty_guard_count` | int | 非空 guard 的迁移数 | `0` |
| `nonempty_action_count` | int | 非空 action 的迁移数 | `0` |
| `raw_panel_xml` | str | panel 级原始 XML | `<AVATARStateMachineDiagramPanel name="Camera" minX="10" ...` |

---

## `states.parquet`（708 行 × 17 列）

摊平后的 708 状态节点（含 panel 中所有非迁移节点：state / pseudo-state / annotation 等）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `ttool_ai` |
| `case_id` | str | 案例 id | `platooning` |
| `case_name` | str | 案例名 | `Platooning` |
| `variant_name` | str | 变体名 | `Platoon1` |
| `panel_name` | str | 所属 panel 名 | `Camera` |
| `panel_id` | str | panel 全局 id | `platooning::Platoon1::Camera` |
| `node_id` | str | TTool XML 中的节点 id（panel 内唯一） | `367` |
| `node_uid` | str | UUID 全局唯一 | `cdd0244a-66ac-44ce-aad0-43ed17664b07` |
| `node_type` | str | 节点类型分类（`state` / `start` / `final` / `other`） | `other` |
| `node_name` | str | 节点名 | `detectDistance()` |
| `component_type_code` | str | TTool 内部组件类型码（5103 = state ; 5101 = start ; etc.） | `5103` |
| `x` | int | 画布 X 坐标 | `728` |
| `y` | int | 画布 Y 坐标 | `394` |
| `width` | int | 节点宽度 | `103` |
| `height` | int | 节点高度 | `20` |
| `connecting_point_ids_json` | str (JSON list) | 该节点的连接点 id 列表（用于绘制迁移） | `["357", "358", ...]` |
| `raw_component_xml` | str | 节点原始 XML | `<COMPONENT type="5103" id="367" index="14" uid="cdd0244a-..." ...` |

---

## `transitions.parquet`（798 行 × 26 列）

摊平后的 798 迁移（**含时间约束与概率字段，是本数据集最有价值的部分**）。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `ttool_ai` |
| `case_id` | str | 案例 id | `platooning` |
| `case_name` | str | 案例名 | `Platooning` |
| `variant_name` | str | 变体名 | `Platoon1` |
| `panel_name` | str | 所属 panel 名 | `Camera` |
| `panel_id` | str | panel 全局 id | `platooning::Platoon1::Camera` |
| `transition_id` | str | TTool 迁移 id（panel 内唯一） | `265` |
| `transition_uid` | str | UUID | `99d2e706-9cc9-4d40-a394-ddb4328a7c21` |
| `source_node_id` | str | 源节点 id | `389` |
| `source_node_name` | str | 源节点名 | `detectDistance_1953()` |
| `source_node_type` | str | 源节点类型 | `other` |
| `target_node_id` | str | 目标节点 id | `641` |
| `target_node_name` | str | 目标节点名 | `Idle` |
| `target_node_type` | str | 目标节点类型 | `state` |
| `guard_or_trigger` | str | guard 表达式或事件触发器（自由文本） | `messageType > 0` |
| `actions` | str | 该迁移触发时的动作（自由文本） | `receiver=other` |
| `after_min` | str | **时间约束下界**（毫秒）—— 时间自动机里的 `after [a, b]` 的 a | `1000` |
| `after_max` | str | **时间约束上界**（毫秒） | `1000` |
| `extra_delay_1` | str | 额外延迟参数 1 | _None_ |
| `extra_delay_2` | str | 额外延迟参数 2 | _None_ |
| `delay_distribution_law` | str | 延迟分布律编码（`0` 通常表示 uniform） | `0` |
| `compute_min` | str | 计算消耗下界（用于建模 CPU 时间） | _None_ |
| `compute_max` | str | 计算消耗上界 | _None_ |
| `probability` | str | 迁移概率（用于概率自动机；空 = 确定迁移） | _None_ |
| `raw_connector_xml` | str | connector 原始 XML | `<CONNECTOR type="5102" id="265" ...` |
| `raw_transition_meta_xml` | str | 迁移属性 SUBCOMPONENT XML（含 guard / action / after 等） | `<SUBCOMPONENT type="-1" id="263" ...` |

---

## `human_review.parquet`（116 行 × 29 列）

公开人评结果（多种 record_type）。**字段大体与 `cross_paper/human_review_records.parquet` 同 schema**，参见顶层 [`README.md`](../README.md) 中关于 `human_review_records.parquet` 的字段说明。

本数据集特有的字段差异：

- 本表 `ref_output_text` / `ref_output_artifact_path` **全空**（论文未公开 reference output）
- 本表 `record_type` 取值含 `case_aggregate_stat` / `summary_level_run_score` / `raw_score_row` / `summary` / `overall_aggregate_stat` 五类
- 本表 `pred_output_text` / `pred_output_artifact_path` 部分非空（指向 `./raw/<case>/<variant>.xml`）

---

## `raw/` 原始资源（✅ 已下载）

| 文件 | 大小 | 来源 |
|------|------|------|
| `platooning/platoonings.md` + `platoonings.xml` | 33K + 92K | GitHub `zebradile/ttool-ai/platooning/` |
| `AutomatedBraking/automatedbraking.md` + `automatedbraking.xml` | 3K + 124K | GitHub `zebradile/ttool-ai/AutomatedBraking/` |
| `spacebasedsystem/spacebasedsystem.xml` | 158K | GitHub `zebradile/ttool-ai/spacebasedsystem/` |
| `incoherencies/specification_spacebasedsystem.md` | 4K | GitHub `zebradile/ttool-ai/incoherencies/` |
| `results.ods` | 15K | GitHub 仓库根的公开人评 ods 表 |

`models.parquet` / `human_review.parquet` 中的 `*_path` 字段已指向上述文件（相对当前 parquet 同级 `./raw/...`）。

## 复用性建议

- ⚠️ **summary-level human review，无 reference output**：人评 116 行只有 input + pred + 评分，没有 gold reference；**不适合**做严格 1:1 input/ref/pred 对齐
- ✅ **最适合做时间约束 + 层次状态机 baseline**：transitions 表的 `after_min/after_max` 字段直接对应时间自动机语义
- ✅ 适合方法对比：把"3 个真实欧洲项目案例 → 解析后 15 model 变体"作为人工总评分协议的 ground truth 流程
- ⚠️ 案例规模小（3 个 system），不适合做大规模数据驱动训练
