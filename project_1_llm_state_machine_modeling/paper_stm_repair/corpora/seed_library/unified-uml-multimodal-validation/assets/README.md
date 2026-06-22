# assets: unified-uml-multimodal-validation

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：Nguyen et al., *A Novel Unified Framework for Automated Generation and Multimodal Validation of UML Diagrams*, CMES 2026，DOI <https://doi.org/10.32604/cmes.2025.075442>。
- 一手数据入口：HF dataset <https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram>。
- 版本：HF API 记录 `sha=e330d1afc19361ecbc970348b94cd858e5d32df6`，访问日期 2026-06-22。
- caveat：dataset license 未在当前 metadata 中明确出现；NL 是 synthetic feature description，因此本条目最高为 `conditional_final_pool`。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | storage | license | 说明 |
|---|---|---|---|---:|---|---|---|
| `hf_state_dataset_record` | HF API metadata | `raw/hf_state_dataset_record.json` | `76c5410b732420d8c91dfed5334868065326158a87987df076e8f3f3902fd957` | 1460 | committed | unknown | 记录 dataset features / splits / revision |
| `hf_state_dataset_tree` | HF tree metadata | `raw/hf_state_dataset_tree.json` | `fdf4e8c7ace4d99c1efc0859840f284edda21116e515cc16cb18c8a9dbb79aaf` | 381 | committed | unknown | 记录 repo 文件树 |
| `hf_state_train_parquet` | `NL + STM_0` dataset | `raw/umlcode_state_diagram_train.parquet` | `02e99eef50ef722aa0c020fccbaeb59daa7cca0e303c247f50450c0eb26bc80d` | 1620142 | committed | unknown | 999 行 `input/reasoning/uml_code` |

## 3. raw → extracted 映射

- `raw/umlcode_state_diagram_train.parquet` 的 `input` 列映射到 `pairs.jsonl.nl_text`。
- `raw/umlcode_state_diagram_train.parquet` 的 `uml_code` 列映射到 `pairs.jsonl.stm0_text`。
- `source_locator` 使用 `row=<idx>; columns=input,uml_code,reasoning`，可由 pandas 重新定位。

## 4. Python 加载方法

在本条目目录运行：

```python
from pathlib import Path
import json, hashlib, pandas as pd
base = Path('assets')
row = json.loads((base / 'extracted/pairs.jsonl').read_text().splitlines()[0])
raw = base / row['source_local_path']
actual_sha = hashlib.sha256(raw.read_bytes()).hexdigest()
df = pd.read_parquet(raw)
idx = int(row['source_locator'].split(';')[0].split('=')[1])
print('pair_id:', row['pair_id'])
print('source_asset_id:', row['source_asset_id'])
print('source_locator:', row['source_locator'])
print('source_sha256:', row['source_sha256'])
print('actual_sha256:', actual_sha)
print('sha256_match:', actual_sha == row['source_sha256'])
print('NL:', df.loc[idx, 'input'][:300])
print('STM_0:', df.loc[idx, 'uml_code'][:300])
```

## 5. 期望输出字段

示例必须输出 `pair_id`、`source_asset_id`、`source_locator`、`source_sha256`、`actual_sha256`、`sha256_match=True`、`NL` 与 `STM_0`。

## 6. 审计不变量

任一 eligible / conditional pair 必须能用 `source_asset_id + source_locator + source_sha256` 回到 `raw/umlcode_state_diagram_train.parquet` 对应行和列；hash 不一致或 locator 无法定位时，不得计入 eligible generated seed count。
