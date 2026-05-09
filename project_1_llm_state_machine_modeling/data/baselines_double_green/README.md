# `baselines_double_green/` — 双绿 NL→STM 核心数据资产

## 0. 这是什么

本目录是 `project_1` 的 **核心数据资产入口**：4 个公开 NL→STM baseline 论文的数据集已经被解析、清洗、parquet 化、人评字段对齐，按论文物理分子目录管理；跨论文汇总单独放 `cross_paper/`。下游导出脚本与产物落地位置统一在 `scripts/` + `datasets/` 子目录下。

> **"双绿"含义**：在 [`../../baselines/SUMMARY.md`](../../baselines/SUMMARY.md) §`数据集与 Benchmark 清单` 口径下，这 4 篇论文的 `BASELINE评估` 与 `数据集可获取性` 都达到 🟢（直接 baseline 对比 + 可立即获取）。

## 1. 目录结构

```
baselines_double_green/
├── README.md                       # 本文档
├── llms_emp/                       # 数据集一：Generating SysML Behavior Models via LLMs (2025)
│   ├── README.md                   # 该论文 mini README（来路 / 字段 / 例子）
│   ├── simple.parquet              # ★ 格式统一表（6 列：id/input/expected/predicted/model/notes）
│   ├── raw_samples.parquet         # 公开账本原始 107 行
│   ├── complete_samples.parquet    # 清洗后 98 个完整样本
│   ├── human_review.parquet        # 192 行逐样本人评
│   └── raw/                        # Dataset.xlsx + Experiment Results.xlsx + ESE 扩展版 + README
├── ttool_ai/                       # 数据集二：System Architects Are not Alone Anymore (2024)
│   ├── README.md
│   ├── simple.parquet              # ★ 格式统一表
│   ├── models.parquet              # 15 个 AVATAR 设计模型
│   ├── state_machine_panels.parquet # 122 个 SM panel
│   ├── states.parquet              # 708 状态摊平
│   ├── transitions.parquet         # 798 迁移摊平（含时间约束 + 概率字段）
│   ├── human_review.parquet        # 116 行人评
│   └── raw/                        # 3 spec.md + 3 .xml + results.ods（GitHub zebradile/ttool-ai）
├── light_control_nimbus/           # 数据集三：Nimbus Light-Control Case Study (2000)
│   ├── README.md
│   ├── simple.parquet              # ★ 格式统一表（predicted/model 全 None，论文非 LLM 工作）
│   ├── documents.parquet           # 2 份原始文档全文
│   ├── fragments.parquet           # 4 个可实验片段
│   ├── variables.parquet           # 17 monitored/controlled 变量
│   ├── states.parquet              # 20 层次状态
│   ├── rules.parquet               # 16 RSML-e 规则
│   └── raw/                        # 2 PDF + 2 txt 抽取本
├── structure_event_driven/         # 数据集四：Structure-Event-Driven Frameworks (2026)
│   ├── README.md
│   ├── simple.parquet              # ★ 格式统一表（predicted 几乎全空，4open 未公开 prediction 文本）
│   ├── cases.parquet               # 9 个 case
│   ├── reference_solutions.parquet # 9 行 Umple ref + 7 类组件计数
│   ├── metrics.parquet             # 512 行逐组件 TP/FN/FP/F1
│   ├── human_review.parquet        # 512 行逐组件人评
│   └── raw/                        # 8 reference Umple txt + xlsx F1 表 + backend prompts
├── cross_paper/                    # 跨 4 篇论文统一汇总
│   ├── README.md
│   ├── dataset_catalog.parquet     # 4 数据集元数据
│   ├── human_review_availability.parquet  # 人评 input/ref/pred 可用性
│   ├── human_review_protocols.parquet     # 人评方法复原
│   └── human_review_records.parquet       # 820 行统一字段人评总表
├── scripts/                        # 4 个 benchmark 范式现成导出脚本
│   ├── _common.py                  # 共用 schema 映射工具
│   ├── export_nl_input.py
│   ├── export_nl_to_stm.py
│   ├── export_human_review.py
│   └── export_unified_benchmark.py
└── datasets/                       # 导出脚本持久化产物落地位置（产物本身不进 git）
    ├── README.md
    └── .gitignore
```

### `simple.parquet` 是什么

每个论文子目录都放了一个 6 列、schema 一致的 [`simple.parquet`](./llms_emp/simple.parquet)，是**最简单的入口**：

| 列 | 含义 |
|----|------|
| `id` | 全数据集唯一 id（`<paper>::<sub-id>`） |
| `input` | 自然语言输入 |
| `expected` | 期望 STM 输出（论文 gold reference，nullable —— 如 ttool_ai 没公开 ref） |
| `predicted` | 论文方法的 LLM 实际输出（nullable —— 如 light_control_nimbus 非 LLM 工作） |
| `model` | predicted 的 LLM 名（nullable） |
| `notes` | 备注（含 case_name / strategy / record_type 等切片信息） |

各论文的 `simple.parquet` 行数 + 覆盖率：

| 论文 | 行 | input | expected | predicted | model |
|------|----|----- -|----------|-----------|-------|
| `llms_emp` | 192 | 192 | 192 | 192 | 192（GPT-4 / GPT-4o / Claude / Kimi / Llama / DeepSeek 6 个 LLM） |
| `ttool_ai` | 15 | 15 | 0（论文未公开 ref） | 15 | 15（统一标 "TTool-AI workflow (GPT-4)"） |
| `light_control_nimbus` | 4 | 4 | 4 | 0（非 LLM 工作） | 0 |
| `structure_event_driven` | 512 | 512 | 320 | 8 | 512（GPT-4o + Claude 3.5 Sonnet） |

## 2. 4 个数据集快览

| # | 子目录 | 论文（年份） | 任务 | 输出元模型 | 公开链接 | 规模摘要 | 适合做什么 |
|---|--------|-------------|------|-----------|----------|---------|------------|
| 1 | [`llms_emp/`](./llms_emp/) | Generating SysML Behavior Models via LLMs (2025) | NL → PlantUML | SysML STM/ACT/SD | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 107 / 98 / 192 | **主样本级 benchmark**（最完整） |
| 2 | [`ttool_ai/`](./ttool_ai/) | System Architects Are not Alone Anymore (2024) | NL → AVATAR | TTool AVATAR (含 STM) | [GitHub zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) | 15 / 122 / 708 / 798 / 116 | **时间约束 + 层次** baseline |
| 3 | [`light_control_nimbus/`](./light_control_nimbus/) | Nimbus Light-Control Case Study (2000) | NL → RSML-e | RSML-e | [PDF + Dagstuhl 挑战题](https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf) | 2 / 4 / 17 / 20 / 16 | **V&V 流程 + HSM** 参考 |
| 4 | [`structure_event_driven/`](./structure_event_driven/) | Structure-Event-Driven Frameworks (2026) | NL → Umple | UML state machine | [匿名工件](https://anonymous.4open.science/r/llm_state_machine_modeling/) | 9 / 9 / 512 / 512 | **逐组件 TP/FP/FN/F1 benchmark** |

> **§11 复用性最终判断（来自 discussion）**：`llms_emp` 主样本级 + `structure_event_driven` 组件级，两者并用是最适合的统一 benchmark 主干；`ttool_ai` 保留为人工总评分协议 + 工具链对比来源；`light_control_nimbus` 保留为 V&V 流程参考。

## 3. 来路

- **原始解析记录**：[`../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md)（1885 行，含每个数据集的原始来源 / 字段说明 / 3 个真实例子 / §11 复用性判断）
- **生成脚本**：[`../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_parquets.py`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_parquets.py) 与 [`build_baseline_double_green_human_review_parquets.py`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_human_review_parquets.py)（保留在原 discussion 资产目录，作为该 discussion 的产物历史）
- **物理迁移**：21 个 parquet 在 2026-05-09 从原 `.assets/` 移到本目录，并按 4 篇论文拆到 4 个子目录 + `cross_paper/`；parquet 名称去掉了 `<paper>_` 前缀（目录名已含上下文）

## 4. 路径与原始资源现状（✅ 已就绪，全链可追溯）

**已完成**（2026-05-09）：

1. ✅ **原始资源全部下载到 `<paper>/raw/`**（不再依赖 `/tmp`）：
   - llms_emp: Google Drive 4 文件（Dataset.xlsx + Experiment Results.xlsx + ESE 扩展 + README）
   - ttool_ai: GitHub `zebradile/ttool-ai` 7 文件（3 spec.md + 3 .xml + results.ods）
   - light_control_nimbus: 2 PDF + 2 txt 抽取本
   - structure_event_driven: 8 reference Umple txt + xlsx F1 表 + backend prompts + 1 prediction txt
2. ✅ **parquet 中所有路径字段全部迁移到相对路径**（相对于 parquet 文件本身）：1952 处替换 + 1108 处置空（4open 未公开的 prediction 图像）
3. ✅ **逐字段验证通过**：1952 处非空路径 100% 指向真实存在文件，0 缺失

**已知缺口**（不影响 parquet 真源使用）：

- structure_event_driven 的 LLM prediction 图像（512 处）4open.science 未公开，相关字段已置空
- `Final Single Prompt/Claude Sonnet 3.5/SSC7_*.txt` 是仅有的 1 个 prediction 文本（其他 511 个 prediction 仅有 metric 数字）
- ttool_ai/human_review.parquet 的 reference output 全空（论文未公开 gold reference）

**`build_*.py` 重跑指南**：build 脚本里仍硬编码 `RAW_ROOT_DEFAULT = Path("/tmp/baseline_double_green/raw")`；要在本仓库重跑需要把脚本默认指到 `<本目录>/<paper>/raw/`，或者通过环境变量覆盖。这一改造留作后续工作。

## 5. 用法（导出脚本）

把这些 parquet 转成常见 NL→STM benchmark 范式的现成脚本，**无需自己写 pandas**：

| 脚本 | 范式 | 用途 |
|------|------|------|
| [`scripts/export_nl_input.py`](./scripts/export_nl_input.py) | 仅 NL 输入 | 跨数据集统一 NL 输入语料（用于 retrieval / clustering / NL 难度分析） |
| [`scripts/export_nl_to_stm.py`](./scripts/export_nl_to_stm.py) | NL input + reference STM | 标准 generation benchmark（input → expected output） |
| [`scripts/export_human_review.py`](./scripts/export_human_review.py) | 含 input + ref + pred + score | reviewer / judge benchmark |
| [`scripts/export_unified_benchmark.py`](./scripts/export_unified_benchmark.py) | 统一格式总表 | 跨 4 数据集导出统一 schema 的 jsonl/parquet |

通用调用方式：

```bash
# 默认 jsonl 输出到 stdout（推荐：流式管道给下游）
python scripts/export_nl_to_stm.py --dataset llms_emp

# 需要持久化时 —— 写到本目录的 datasets/ 子目录（git 可追溯位置）
python scripts/export_nl_to_stm.py --dataset all --output datasets/nl2stm.jsonl

# parquet 输出（便于后续做 pandas 实验）
python scripts/export_unified_benchmark.py --strict-alignable-only --drop-no-ref \
    --format parquet --output datasets/unified.parquet

# 只保留 STM（剔除 ACT/SD）
python scripts/export_nl_to_stm.py --dataset llms_emp --diagram-type stm
```

每个脚本都支持 `--help` 查看完整参数。

### 产物输出规范

为了保持数据资产**全链可追溯**，导出脚本的产物有以下硬性规范：

1. **优先 stdout 流式产出，不落盘**：脚本默认写到 stdout（jsonl 模式），适合一次性用、直接管道给下游模型 / 评测程序。这是最推荐的"轻量调用"方式。
2. **必须持久化时落 [`datasets/`](./datasets/)**：当确实需要把产物固化保留（比如要给协作者 / 别的会话复用），用 `--output datasets/<name>.{jsonl,parquet}`。该目录有自己的 [`README.md`](./datasets/README.md) 与 `.gitignore`：派生产物本身不进 git，但目录占位结构进 git，作为"产物固化约定"。
3. **不允许写到 `/tmp` 或仓库外路径**：仓库外路径破坏可追溯性 —— 如果需要短期临时文件，用 stdout + 进程内变量（`<(cmd)`、`subprocess`）；不要 `--output /tmp/xxx`。
4. **任何下游产物都应能由 `scripts/` 在 21 parquet 上一键重生**：如果某个 ad-hoc 后处理无法重生，把逻辑沉淀进 `scripts/` 而不是让产物孤立存在。

## 6. 关联资料（反向引用）

| 资源 | 路径 |
|------|------|
| 解析与 parquet 化原始记录 | [`../../discussions/2026-04-15-01-03-52-...parquet化.md`](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md) |
| baselines 文库总账（含 §数据集可获取性口径） | [`../../baselines/SUMMARY.md`](../../baselines/SUMMARY.md) |
| baselines 操作规范 | [`../../baselines/GUIDE.md`](../../baselines/GUIDE.md) |
| 4 篇论文的单篇 DESC | 见 §2 表格中的 `子目录` 链接（每个子目录 README 都反向链接到 baselines/<slug>/） |
| 4 篇论文的 review_extraction（人评细节） | `../../state_machine_review_corpus/<slug>/review_extraction.md`（如适用） |

## 7. 给后续研究者 / AI 的导航

### 7.1 想做什么 → 该看哪个

- **比较 LLM 在 NL→STM 上的生成质量** → [`llms_emp/`](./llms_emp/) + [`structure_event_driven/`](./structure_event_driven/)；优先选这两个（input + reference 完整对齐）
- **评估 reviewer / LLM-as-judge** → [`cross_paper/human_review_records.parquet`](./cross_paper/human_review_records.parquet)（820 行统一字段）
- **做带时间约束的状态机生成** → [`ttool_ai/transitions.parquet`](./ttool_ai/transitions.parquet)（`after_min` / `after_max` / `delay_distribution_law` / `probability` 字段直接对应时间自动机语义）
- **做层次/平行状态机生成** → [`light_control_nimbus/states.parquet`](./light_control_nimbus/states.parquet)（depth + parent）+ [`structure_event_driven/reference_solutions.parquet`](./structure_event_driven/reference_solutions.parquet)（hierarchical / parallel 计数）
- **构造 retrieval 语料 / clustering 输入** → `scripts/export_nl_input.py --dataset all`

### 7.2 注意事项

1. **本目录是 4 个数据集的 single source of truth for parquet 落盘位置**；任何 parquet 修改都应在生成脚本（`../../discussions/.../*.assets/build_*.py`）中统一处理，不要手工编辑 parquet
2. **可获取性 / 规模 / 链接的事实源是 [`../../baselines/SUMMARY.md`](../../baselines/SUMMARY.md) §数据集与 Benchmark 清单**；本 README 与各子目录 README 是数据资产视角的派生展示，冲突时以 SUMMARY 为准
3. **不要把 parquet 复制到其他位置**；下游用 `pd.read_parquet(".../<paper>/<file>.parquet")` 直接读
4. **数据扩展规则**：若新增第 5 个数据集（同样达到双绿），应：
   - 在 baselines/SUMMARY.md §数据集与 Benchmark 清单 加一行（按 GUIDE §6.7）
   - 在本目录新建 `<paper_slug>/` 子目录，写 mini README + 放 parquet
   - 在 `cross_paper/dataset_catalog.parquet` 中新增一行
   - 在 `scripts/_common.py` 中新增 iter_<paper>() 函数与 DATASETS 列表
5. **不可作为重新审查 baselines 数据集可获取性的入口**：那是 `baselines/GUIDE.md` §5.3 / §6.7 的职责
