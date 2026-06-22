# assets: llms-emp-stm-subset

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：Wang et al., *Generating SysML Behavior Models via Large Language Models: an Empirical Study*, ACM/IEEE MODELS-C 2025, DOI <https://dl.acm.org/doi/10.1145/3755881.3755926>。
- 一手数据入口：论文给出的 Google Drive folder <https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link>。
- 当前状态：已用 `gdown.download_folder` 下载并提交 seed registry 所需最小一手资源：`Experiment Results.xlsx`、`Dataset.xlsx`、Drive `README.md` 与下载元数据。
- caveat：数据许可与再分发状态未知；同一 workbook 中同时存在 reference `PlantUML` 和检查后结果列，后续使用必须严格只取 `Generation PlantUML` 作为原始 $STM_0$，避免 reference / repair leakage。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | storage | license | 说明 |
|---|---|---|---|---:|---|---|---|
| `llms_emp_drive_metadata` | 下载元数据 | `raw/google_drive_metadata.json` | 见 `manifest.json` | 849 | committed | unknown | 记录 Drive folder、下载工具、提交最小资产和跳过项 |
| `llms_emp_experiment_results_xlsx` | `NL + STM_0` 实验主表 | `raw/drive_download/Experiment Results.xlsx` | 见 `manifest.json` | 11561182 | committed | unknown | `STM Results` sheet 含 60 行 `Requirement Description + Generation PlantUML` |
| `llms_emp_dataset_xlsx` | 数据集上下文 | `raw/drive_download/Dataset.xlsx` | 见 `manifest.json` | 36392 | committed | unknown | 记录模型名称、来源和原始需求 / PlantUML 上下文 |
| `llms_emp_drive_readme` | Drive 说明 | `raw/drive_download/README.md` | 见 `manifest.json` | 1239 | committed | unknown | Drive 文件夹说明 |

`llm4sysml_exp/` demo 代码、向量索引、`visualization code/` 与重复 / 二级 `ESE Expriment Results.xlsx` 不进入 committed seed assets；跳过理由写在 `manifest.json.skipped_assets` 与 `raw/google_drive_metadata.json`。

## 3. raw → extracted 映射

| extracted 字段 | workbook 来源 |
|---|---|
| `nl_text` | `raw/drive_download/Experiment Results.xlsx` / `STM Results` / `Requirement Description` |
| `stm0_text` | 同一 workbook / `STM Results` / `Generation PlantUML` |
| `generation_model_or_method` | `STM Results` / `LLMs` |
| `model_source` | `STM Results` / `Model Source` |
| `model_name` | `STM Results` / `Model Name` |
| reference | `STM Results` / `PlantUML`，只能进 reference，不计原始 $STM_0$ |
| postprocessed | `Result with Format/Grammar/Semantic Checking`，不得作为原始 $STM_0$ |

当前 `pairs.jsonl` 已覆盖 `STM Results` 全量 60 行：Claude、DeepSeek、GPT-4、GPT-4o、Kimi、Llama 各 10 行。

## 4. Python 加载方法

在本条目目录运行：

```python
from pathlib import Path
import json, hashlib, pandas as pd
base = Path('assets')
rows = [json.loads(line) for line in (base / 'extracted/pairs.jsonl').read_text().splitlines() if line.strip()]
raw = base / rows[0]['source_local_path']
actual_sha = hashlib.sha256(raw.read_bytes()).hexdigest()
df = pd.read_excel(raw, sheet_name='STM Results')
print('workbook_rows:', len(df))
print('extracted_pairs:', len(rows))
print('llm_distribution:', df.groupby('LLMs').size().to_dict())
print('pair_id:', rows[0]['pair_id'])
print('source_asset_id:', rows[0]['source_asset_id'])
print('source_locator:', rows[0]['source_locator'])
print('source_sha256:', rows[0]['source_sha256'])
print('actual_sha256:', actual_sha)
print('sha256_match:', actual_sha == rows[0]['source_sha256'])
print('LLM:', rows[0]['llm'])
print('NL:', rows[0]['nl_text'][:300])
print('STM_0:', rows[0]['stm0_text'][:300])
```

## 5. 期望输出字段

示例必须输出 `workbook_rows=60`、`extracted_pairs=60`、`llm_distribution={'Claude': 10, 'DeepSeek': 10, 'GPT-4': 10, 'GPT-4o': 10, 'Kimi': 10, 'Llama': 10}`、`pair_id`、`source_asset_id`、`source_locator`、`source_sha256`、`actual_sha256`、`sha256_match=True`、`LLM`、`NL` 与 `STM_0`。人类读者应能直接看出：NL 是 SysML 行为模型需求描述，`STM_0` 是该 LLM 在 `Generation PlantUML` 列给出的原始 PlantUML 状态机。

期望输出形态如下（片段截断不影响审计，完整文本在 `pairs.jsonl` 与 workbook 对应行中）：

```text
workbook_rows: 60
extracted_pairs: 60
llm_distribution: {'Claude': 10, 'DeepSeek': 10, 'GPT-4': 10, 'GPT-4o': 10, 'Kimi': 10, 'Llama': 10}
pair_id: llms_emp_stm_results_0000
source_asset_id: llms_emp_experiment_results_xlsx
source_locator: sheet=STM Results; row=0; columns=Requirement Description,Generation PlantUML,LLMs,Model Source,Model Name,PlantUML
sha256_match: True
LLM: GPT-4o
NL: 1 The human driving mode is represented by a simple state...
STM_0: @startuml | [*] --> HumanDriving ...
```

## 6. 审计不变量

只有从一手 workbook 读取到的 `Requirement Description + Generation PlantUML`，且能以 sheet / row / column + workbook SHA-256 回溯的行，才能计入 eligible generated seed。旧 parquet 只可写入 `legacy_audit_refs`。Reference `PlantUML` 与检查后结果列必须显式排除，不能混入原始 $STM_0$。
