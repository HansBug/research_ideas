# `data/` — project_1 双绿 NL→STM 核心数据资产

## 0. 这是什么

本目录是 `project_1` 的**核心数据资产入口**：4 个公开 NL→STM baseline 论文的数据集已经被解析、清洗、parquet 化、人评字段对齐，按论文物理分子目录管理；跨 4 篇论文汇总的 4 个 parquet + 1 个 `all_simple.parquet` 直接放在本目录顶层。下游导出脚本与产物落地位置统一在 `scripts/` + `datasets/` 子目录下。

> **"双绿"含义**：在 [`../baselines/SUMMARY.md`](../baselines/SUMMARY.md) §`数据集与 Benchmark 清单` 口径下，这 4 篇论文的 `BASELINE评估` 与 `数据集可获取性` 都达到 🟢（直接 baseline 对比 + 可立即获取）。

## 1. 目录结构

```
data/
├── README.md                              # 本文档
├── all_simple.parquet                     # ★ 跨 paper 总表（723 行 = 192+15+4+512，schema = paper + simple 6 列）
├── dataset_catalog.parquet                # 4 个数据集元数据
├── human_review_availability.parquet      # 4 篇人评公开可用性
├── human_review_protocols.parquet         # 4 篇人评方法复原
├── human_review_records.parquet           # 820 行跨论文统一字段人评总表
│
├── llms_emp/                              # NL → PlantUML（最完整的数据集）
├── ttool_ai/                              # NL → AVATAR（含时间约束 + 概率字段）
├── light_control_nimbus/                  # NL → RSML-e（HSM + 平行区域经典样本）
├── structure_event_driven/                # NL → Umple（逐组件 TP/FP/FN/F1 benchmark）
│
├── scripts/                               # 现成 benchmark 范式导出脚本
│   ├── _common.py                         # 共用 schema 映射工具
│   ├── _build_simple_parquet.py           # 重生 4 个 simple.parquet + all_simple.parquet
│   ├── _migrate_paths.py                  # parquet 路径字段迁移工具
│   ├── _verify_paths.py                   # 逐字段验证文件存在
│   ├── export_nl_input.py                 # 导出仅 NL 输入语料
│   ├── export_nl_to_stm.py                # 导出 NL + reference STM
│   ├── export_human_review.py             # 导出人评 input/ref/pred/score
│   └── export_unified_benchmark.py        # 跨数据集统一 benchmark
│
└── datasets/                              # 导出脚本持久化产物落地位置（产物不进 git）
```

## 2. 4 个数据集快览

| # | 子目录 | 论文（年份） | 任务 | 输出元模型 | 公开链接 | 规模摘要 | 适合做什么 |
|---|--------|-------------|------|-----------|----------|---------|------------|
| 1 | [`llms_emp/`](./llms_emp/) | Generating SysML Behavior Models via LLMs (2025) | NL → PlantUML | SysML STM/ACT/SD | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 107 / 98 / 192 | **主样本级 benchmark**（最完整） |
| 2 | [`ttool_ai/`](./ttool_ai/) | System Architects Are not Alone Anymore (2024) | NL → AVATAR | TTool AVATAR (含 STM) | [GitHub zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) | 15 / 122 / 708 / 798 / 116 | **时间约束 + 层次** baseline |
| 3 | [`light_control_nimbus/`](./light_control_nimbus/) | Nimbus Light-Control Case Study (2000) | NL → RSML-e | RSML-e | [PDF + Dagstuhl 挑战题](https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf) | 2 / 4 / 17 / 20 / 16 | **V&V 流程 + HSM** 参考 |
| 4 | [`structure_event_driven/`](./structure_event_driven/) | Structure-Event-Driven Frameworks (2026) | NL → Umple | UML state machine | [匿名工件](https://anonymous.4open.science/r/llm_state_machine_modeling/) | 9 / 9 / 512 / 512 | **逐组件 TP/FP/FN/F1 benchmark** |

> 每个子目录都有自己的 `README.md`，含**该子目录下每个 parquet 的逐字段说明 + 示例值**。本文件只覆盖 data/ 顶层 5 个 parquet。

## 3. 路径与原始资源

✅ **已就绪，全链可追溯**（2026-05-09）：

1. 原始资源全部下载到 `<paper>/raw/`（不再依赖 `/tmp`）
2. 所有 parquet 路径字段全部迁移到相对路径（相对 parquet 文件本身）：1952 处替换 + 1108 处置空（4open 未公开图像）
3. 逐字段验证：1952 处非空路径 100% 指向真实文件，0 缺失（`scripts/_verify_paths.py` 跑通）

---

## 4. 顶层 5 个 parquet 字段详解

### 4.1 `all_simple.parquet`（723 行 × 7 列）

跨 4 个 paper 的 `simple.parquet` 合并总表。schema = `paper` 列 + 各 paper simple 6 列。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `paper` | str | 论文 slug（`llms_emp` / `ttool_ai` / `light_control_nimbus` / `structure_event_driven`） | `llms_emp` |
| `id` | str | 全数据集唯一 id | `llms_emp::STM Results:0` |
| `input` | str | 自然语言输入 | `1 The human driving mode is represented by a simple state. ...` |
| `expected` | str / None | 期望 STM 输出（论文 gold reference，nullable） | `@startuml [*] --> human_mode : power_on  ...` |
| `predicted` | str / None | 论文方法 LLM 实际输出（nullable） | `@startuml [*] --> HumanDriving  ...` |
| `model` | str / None | predicted 对应 LLM 名（nullable） | `GPT-4o` |
| `notes` | str | 切片信息（自由格式 `key=value; key=value;`） | `diagram_type=stm; sheet=STM Results; record_type=sample_level_review` |

各 `paper` 行数 + 覆盖率：

| paper | 行 | input | expected | predicted | model |
|-------|----|------|----------|-----------|-------|
| `llms_emp` | 192 | 192 | 192 | 192 | 192 |
| `ttool_ai` | 15 | 15 | 0（无 ref） | 15 | 15 |
| `light_control_nimbus` | 4 | 4 | 4 | 0（非 LLM） | 0 |
| `structure_event_driven` | 512 | 512 | 320 | 8（4open 未公开） | 512 |

---

### 4.2 `dataset_catalog.parquet`（4 行 × 8 列）

4 个数据集的元数据汇总。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `dataset_id` | str | 数据集 id | `llms_emp` |
| `paper_slug` | str | 对应 baselines/<slug>/ 目录名（与 dataset_id 通常但不一定相同：`ttool_ai` ↔ `ttool-ai`） | `llms_emp` |
| `dataset_name` | str | 数据集人类可读名 | `G_Model SysML behavior model dataset` |
| `output_metamodel` | str | 输出元模型描述 | `SysML STM / ACT / SD encoded in PlantUML` |
| `sample_granularity` | str | 一行代表什么粒度 | `one row per behavior model` |
| `raw_sample_count` | int | 原始样本数（含未筛选） | `107` |
| `experiment_ready_sample_count` | int | 实验可用样本数 | `98` |
| `notes` | str | 备注 | `Public ledger contains 107 rows; 98 rows have both requirements and PlantUML output.` |

---

### 4.3 `human_review_availability.parquet`（4 行 × 9 列）

4 篇论文公开人评的可用性总表。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `paper_slug` | str | baselines 目录名（注意 `ttool-ai` 用连字符） | `llms_emp` |
| `paper_title` | str | 论文标题 | `Generating SysML Behavior Models via Large Language Models: an Empirical Study` |
| `public_human_review_status` | str | 状态（`sample_level_available` / `summary_only_available` / `method_only_no_raw_scores`） | `sample_level_available` |
| `extracted_record_count` | int | 该 paper 提取出多少行人评 | `192` |
| `raw_artifact_path` | str | 原始 xlsx/ods/PDF 相对路径（**指向 data/<paper>/raw/...**） | `./llms_emp/raw/Experiment Results.xlsx` |
| `input_available` | bool | 该 paper 的人评是否有 input 字段 | `True` |
| `reference_output_available` | bool | 该 paper 的人评是否有 ref output | `True` |
| `prediction_available` | bool | 该 paper 的人评是否有 LLM prediction | `True` |
| `notes` | str | 缺口与说明 | `公开结果表含逐样本 input / ref / pred 与人工语法/语义评审结果。` |

---

### 4.4 `human_review_protocols.parquet`（4 行 × 15 列）

4 篇论文人评方法学复原。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `paper_slug` | str | baselines 目录名 | `llms_emp` |
| `paper_title` | str | 论文标题 | `Generating SysML Behavior Models via Large Language Models: ...` |
| `paper_local_path` | str | baselines 中 paper_content.txt 相对路径 | `../baselines/llms_emp/paper_content.txt` |
| `public_human_review_status` | str | 与 availability 表同义 | `sample_level_available` |
| `human_review_artifact` | str | 人评 raw 工件相对路径（与 `raw_artifact_path` 同源） | `./llms_emp/raw/Experiment Results.xlsx` |
| `reviewer_pool` | str | 评审人组成（来自论文原文） | `G_Model 组由 1 名高年级本科生、2 名硕士生、2 名博士生组成；...` |
| `reference_basis` | str | reference 来源说明 | `参考模型为公开 G_Model 数据集中的人工构建 PlantUML/SysML 行为模型；...` |
| `artifact_under_review` | str | 评审对象描述 | `LLM 生成的 PlantUML 行为模型，按 STM / ACT / SD 三类任务逐样本评审。` |
| `review_dimensions_json` | str (JSON list) | 评审维度列表 | `["PlantUML format accuracy (自动)", "SysML grammar accuracy (人工)", ...]` |
| `execution_steps_markdown` | str | 评审执行步骤（markdown 文本） | `1. 用论文给定 prompt 模板向 LLM 生成 PlantUML。 2. 先做 PlantUML 格式检查。 ...` |
| `matching_rules_markdown` | str | 匹配规则描述 | `语法检查逐项对照 SysML 规范；语义检查逐条对照 55 条语义规则；...` |
| `public_gap_notes` | str | 公开包的已知缺口 | `公开包给出了逐样本结果表，但没有把人工检查过程的逐条注释拆成独立日志文件。` |
| `paper_method_verbatim_excerpt` | str | 论文 §Method 原文摘录（人类可读） | `[reviewer_pool] We have two groups: G_Search ...` |
| `paper_method_verbatim_excerpt_json` | str (JSON list) | 上一字段的结构化版（含 source_path / line numbers） | `[{"end_line": 347, "label": "reviewer_pool", "source_path": "...", ...}]` |
| `paper_method_verbatim_verified` | bool | 上述摘录是否经过人工核对 | `True` |

---

### 4.5 `human_review_records.parquet`（820 行 × 34 列）

跨 4 篇论文统一字段的人评记录总表。**这是下游 reviewer / judge benchmark 的主要数据源**。

| 字段 | 类型 | 含义 | 示例值 |
|------|------|------|--------|
| `paper_slug` | str | baselines 目录名 | `llms_emp` |
| `paper_title` | str | 论文标题 | `Generating SysML Behavior Models via ...` |
| `record_source` | str | 记录来源工件路径（部分仍保留旧 /tmp 字符串作历史追溯，**不是**实际可读路径；要读用 `*_artifact_path`） | `/tmp/baseline_double_green/raw/llms_emp_gmodel/Experiment Results.xlsx` |
| `record_type` | str | 记录类型（`sample_level_review` / `case_aggregate_stat` / `summary_level_run_score` / `raw_score_row` / `summary` / `overall_aggregate_stat`） | `sample_level_review` |
| `review_record_id` | str | 该 paper 内唯一记录 id | `STM Results:0` |
| `case_id` | str / None | 案例 id（如适用） | `platooning` |
| `case_name` | str / None | 案例名 | `Platooning` |
| `split_name` | str / None | 数据切分名（如 main_results / extension） | `main_results` |
| `sheet_name` | str / None | xlsx sheet 名 | `STM Results` |
| `diagram_type` | str / None | 图类型（仅 llms_emp） | `stm` |
| `strategy_name` | str / None | strategy 名（仅 SE-Driven）：`single_prompt`/`structure_driven`/`event_driven`/`hybrid` | `single_prompt` |
| `llm_name` | str / None | LLM 名 | `GPT-4o` |
| `review_target` | str | 评审对象类（`generated_behavior_model` 等） | `generated_behavior_model` |
| `review_index` | float / None | 评审序号（同 sample 多轮时） | `1.0` |
| `component` | str / None | 评测组件（仅 SE-Driven，7 类组件之一） | `States` |
| `input_text` | str / None | NL 输入 | `1 The human driving mode is represented ...` |
| `ref_output_text` | str / None | 期望输出 | `@startuml [*] --> human_mode : power_on ...` |
| `ref_output_format` | str / None | 期望输出格式 | `PlantUML / SysML behavior model` |
| `ref_output_artifact_path` | str / None | 期望输出来源工件**相对路径**（指向 `./<paper>/raw/...`） | `./llms_emp/raw/Dataset.xlsx` |
| `pred_output_text` | str / None | LLM 输出文本 | `@startuml [*] --> HumanDriving ...` |
| `pred_output_format` | str / None | LLM 输出格式 | `PlantUML / SysML behavior model` |
| `pred_output_artifact_path` | str / None | LLM 输出来源工件相对路径 | `./llms_emp/raw/Experiment Results.xlsx` |
| `human_review_score` | float / None | 评分（数值；也可能是其他类型如 `0.81/1.0` 这种字符串） | `0.4166666667` |
| `human_review_score_unit` | str / None | 分数单位 | `semantic_f1` |
| `human_review_summary` | str / None | 评审摘要 | `Manual grammar + semantic review with reference-model TP/FP/FN accounting.` |
| `human_review_details_json` | str (JSON) | 详细评审结果 | `{"initial": {...}, "after": {...}}` |
| `human_review_source_record_json` | str (JSON) | xlsx/ods 原始行（保留所有列原貌） | `{"F1 Score": 0.4166666667, ...}` |
| `human_review_original_text` | str / None | 评审者原始备注（自由文本） | `[grammar_hallucinations] transition does not connect two state` |
| `human_review_original_text_json` | str (JSON) | 上一字段的结构化版 | `[{"column_name": "SysML Grammar Hallucinations", ...}]` |
| `paper_method_verbatim_excerpt` | str / None | 论文 §Method 摘录 | `[reviewer_pool] We have two groups: G_Search ...` |
| `paper_method_verbatim_excerpt_json` | str (JSON) | 上一字段结构化版 | `[{"end_line": 347, "label": "reviewer_pool", ...}]` |
| `verbatim_extraction_verified` | bool | 摘录是否经过人工核对 | `True` |
| `review_rubric_text` | str | 评审 rubric 一段话 | `Grammar: manual comparison against SysML v1.6 grammar points. ...` |
| `public_artifact_limitations` | str | 公开工件已知缺口 | `Workbook公开了逐样本结果，但人工审查日志只以汇总列形式保留在结果表中。` |

---

## 5. 用法（导出脚本）

| 脚本 | 范式 | 用途 |
|------|------|------|
| [`scripts/export_nl_input.py`](./scripts/export_nl_input.py) | 仅 NL 输入 | 跨数据集统一 NL 输入语料 |
| [`scripts/export_nl_to_stm.py`](./scripts/export_nl_to_stm.py) | NL input + reference STM | 标准 generation benchmark |
| [`scripts/export_human_review.py`](./scripts/export_human_review.py) | input + ref + pred + score | reviewer / judge benchmark |
| [`scripts/export_unified_benchmark.py`](./scripts/export_unified_benchmark.py) | 跨 4 数据集统一格式总表 | 一体化 benchmark |

通用调用方式：

```bash
# 默认 jsonl 输出到 stdout
python scripts/export_nl_to_stm.py --dataset llms_emp

# 持久化时落到 datasets/ 子目录
python scripts/export_nl_to_stm.py --dataset all --output datasets/nl2stm.jsonl

# parquet 输出
python scripts/export_unified_benchmark.py --strict-alignable-only --drop-no-ref \
    --format parquet --output datasets/unified.parquet
```

每个脚本支持 `--help`。**禁止** `--output /tmp/...`：仓库外路径破坏可追溯性，详见 [`datasets/README.md`](./datasets/README.md)。

## 6. 关联资料（反向引用）

| 资源 | 路径 |
|------|------|
| 解析与 parquet 化原始记录 | [`../discussions/2026-04-15-01-03-52-...parquet化.md`](../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md) |
| baselines 文库总账（含 §数据集可获取性口径） | [`../baselines/SUMMARY.md`](../baselines/SUMMARY.md) |
| baselines 操作规范 | [`../baselines/GUIDE.md`](../baselines/GUIDE.md) |
| 4 篇论文的 single source DESC | 见 §2 表格中的 `子目录` 链接 |

## 7. 给后续研究者 / AI 的导航

### 7.1 想做什么 → 该看哪个

- **比较 LLM 在 NL→STM 上的生成质量** → [`llms_emp/`](./llms_emp/) + [`structure_event_driven/`](./structure_event_driven/)；优先选这两个（input + reference 完整对齐）
- **评估 reviewer / LLM-as-judge** → [`human_review_records.parquet`](./human_review_records.parquet)（820 行统一字段）
- **做带时间约束的状态机生成** → [`ttool_ai/transitions.parquet`](./ttool_ai/transitions.parquet)（`after_min` / `after_max` / `delay_distribution_law` / `probability` 字段直接对应时间自动机语义）
- **做层次/平行状态机生成** → [`light_control_nimbus/states.parquet`](./light_control_nimbus/states.parquet)（depth + parent）+ [`structure_event_driven/reference_solutions.parquet`](./structure_event_driven/reference_solutions.parquet)（hierarchical / parallel 计数）
- **构造 retrieval 语料 / clustering 输入** → `scripts/export_nl_input.py --dataset all`
- **想要最简入口** → 直接读 [`all_simple.parquet`](./all_simple.parquet)（一行代码 `pd.read_parquet`），用 `paper` 列切片

### 7.2 注意事项

1. 本目录是 4 个数据集的 **single source of truth for parquet 落盘位置**；任何 parquet 修改都应通过 `scripts/_*.py` 重生，不要手工编辑 parquet
2. 可获取性 / 规模 / 链接的事实源是 [`../baselines/SUMMARY.md`](../baselines/SUMMARY.md) §数据集与 Benchmark 清单；本 README 与各子目录 README 是数据资产视角的派生展示，冲突时以 SUMMARY 为准
3. 不要把 parquet 复制到其他位置；下游用 `pd.read_parquet(".../<paper>/<file>.parquet")` 直接读
4. **数据扩展规则**：若新增第 5 个数据集（同样达到双绿），应：
   - 在 baselines/SUMMARY.md §数据集与 Benchmark 清单 加一行（按 GUIDE §6.7）
   - 在本目录新建 `<paper_slug>/` 子目录，写 mini README + 放 parquet
   - 在 `dataset_catalog.parquet` 中新增一行
   - 在 `scripts/_common.py` 中新增 iter_<paper>() 函数与 DATASETS 列表
   - 重跑 `scripts/_build_simple_parquet.py` 更新 `<paper>/simple.parquet` + `all_simple.parquet`
   - 重跑 `scripts/_verify_paths.py` 验证路径
