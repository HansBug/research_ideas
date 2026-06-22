# assets: llms-emp-stm-subset

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：Wang et al., *Generating SysML Behavior Models via Large Language Models: an Empirical Study*, ACM/IEEE MODELS-C 2025, DOI <https://dl.acm.org/doi/10.1145/3755881.3755926>。
- 一手数据入口：论文给出的 Google Drive folder <https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link>。
- 当前状态：当前 registry 条目只登记 metadata pointer；尚未提交 `Experiment Results.xlsx` / `Dataset.xlsx`，因此不能标为 `final_pool_ready`。

## 2. 资源盘点表

| asset_id | 角色 | local_path | storage | license | 说明 |
|---|---|---|---|---|---|
| `llms_emp_drive_metadata` | Drive metadata pointer | `raw/google_drive_metadata.json` | committed metadata | unknown | 记录必须人工冻结的 workbook 与字段边界 |

## 3. raw → extracted 映射

后续下载一手 workbook 后，必须按以下字段映射抽取：

| extracted 字段 | workbook 来源 |
|---|---|
| `nl_text` | `Experiment Results.xlsx` / `STM Results` / `Requirement Description` |
| `stm0_text` | `STM Results` / `Generation PlantUML` |
| `generation_model_or_method` | `STM Results` / `LLMs` |
| reference | `PlantUML`，只能进 `reference_sets` |
| postprocessed | `Result with Format/Grammar/Semantic Checking`，不得作为原始 `STM_0` |

## 4. Python 加载方法

当前只能加载 metadata：

```python
from pathlib import Path
import json
meta = json.loads(Path('assets/raw/google_drive_metadata.json').read_text())
print(meta['drive_folder'])
print(meta['required_sheet'], meta['generated_field'])
```

## 5. 期望输出字段

期望输出 Drive folder、required sheet、generated field。因为 workbook 未落盘，本条目当前无可提交 `NL + STM_0` 示例。

## 6. 审计不变量

只有从一手 workbook 读取到的 `Requirement Description + Generation PlantUML` 且能以 sheet/row/column + workbook sha256 回溯的行，才能计入 eligible generated seed。旧 parquet 只可写入 `legacy_audit_refs`。
