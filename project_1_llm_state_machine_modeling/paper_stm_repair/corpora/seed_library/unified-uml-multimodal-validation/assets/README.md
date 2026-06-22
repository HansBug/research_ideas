# assets: unified-uml-multimodal-validation

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：Nguyen et al., *A Novel Unified Framework for Automated Generation and Multimodal Validation of UML Diagrams*, CMES 2026，DOI <https://doi.org/10.32604/cmes.2025.075442>。
- 一手数据入口：HF dataset <https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram>。
- 版本：HF API 记录 `sha=e330d1afc19361ecbc970348b94cd858e5d32df6`，访问日期 2026-06-22。
- caveat：dataset license 未在当前 metadata 中明确出现；NL 是 synthetic feature description / 非控制系统需求，因此本条目最高为 `conditional_final_pool`。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | storage | license | 说明 |
|---|---|---|---|---:|---|---|---|
| `hf_state_dataset_record` | HF API metadata | `raw/hf_state_dataset_record.json` | `76c5410b732420d8c91dfed5334868065326158a87987df076e8f3f3902fd957` | 1460 | committed | unknown | 记录 dataset features / splits / revision |
| `hf_state_dataset_tree` | HF tree metadata | `raw/hf_state_dataset_tree.json` | `fdf4e8c7ace4d99c1efc0859840f284edda21116e515cc16cb18c8a9dbb79aaf` | 381 | committed | unknown | 记录 repo 文件树 |
| `hf_state_train_parquet` | `NL + STM_0` dataset | `raw/umlcode_state_diagram_train.parquet` | `02e99eef50ef722aa0c020fccbaeb59daa7cca0e303c247f50450c0eb26bc80d` | 1620142 | committed | unknown | 999 行 `input/reasoning/uml_code`；其中 989 行是有效 PlantUML，10 行为 `No valid PlantUML code found.` |

## 3. raw → extracted 映射

- `raw/umlcode_state_diagram_train.parquet` 的 `input` 列映射到 `pairs.jsonl.nl_text`。
- `raw/umlcode_state_diagram_train.parquet` 的 `uml_code` 列映射到 `pairs.jsonl.stm0_text`。
- `source_locator` 使用 `row=<idx>; columns=input,uml_code,reasoning`，可由 pandas 重新定位。
- 当前 `pairs.jsonl` 已覆盖 raw parquet 全量 999 行；validator 可逐行回到 raw parquet 复算文本与哈希。
- 只有 `uml_code` 同时满足 `@startuml` 开头且包含 `@enduml` 的 989 行计入 eligible generated seed；10 行生成失败只保留为审计证据。

## 4. Python 加载方法

在本条目目录运行：

```python
from pathlib import Path
import json, hashlib, pandas as pd
base = Path('assets')
rows = [json.loads(line) for line in (base / 'extracted/pairs.jsonl').read_text().splitlines() if line.strip()]
raw = base / rows[0]['source_local_path']
actual_sha = hashlib.sha256(raw.read_bytes()).hexdigest()
df = pd.read_parquet(raw)
eligible = [r for r in rows if r['is_generated_stm0'] and not r['is_reference'] and not r['is_postprocessed']]
failed = [r for r in rows if not r['is_generated_stm0']]
idx = int(rows[0]['source_locator'].split(';')[0].split('=')[1])
print('raw_rows:', len(df))
print('extracted_pairs:', len(rows))
print('eligible_pairs:', len(eligible))
print('generation_failure_pairs:', len(failed))
print('pair_id:', rows[0]['pair_id'])
print('source_asset_id:', rows[0]['source_asset_id'])
print('source_locator:', rows[0]['source_locator'])
print('source_sha256:', rows[0]['source_sha256'])
print('actual_sha256:', actual_sha)
print('sha256_match:', actual_sha == rows[0]['source_sha256'])
print('NL:', df.loc[idx, 'input'][:300])
print('STM_0:', df.loc[idx, 'uml_code'][:300])
print('first_failed_pair:', failed[0]['pair_id'], failed[0]['stm0_text'])
```

## 5. 期望输出字段

示例必须输出 `raw_rows=999`、`extracted_pairs=999`、`eligible_pairs=989`、`generation_failure_pairs=10`、`pair_id`、`source_asset_id`、`source_locator`、`source_sha256`、`actual_sha256`、`sha256_match=True`、`NL` 与 `STM_0`。人类读者应能直接看出：NL 是 synthetic restaurant menu feature description，`STM_0` 是对应的 PlantUML state diagram；同时能看到生成失败行被明确排除而不是静默丢弃。

期望输出形态如下（片段截断不影响审计，完整文本在 `pairs.jsonl` 与 raw parquet 对应行中）：

```text
raw_rows: 999
extracted_pairs: 999
eligible_pairs: 989
generation_failure_pairs: 10
pair_id: unified_uml_state_train_0000
source_asset_id: hf_state_train_parquet
source_locator: row=0; columns=input,uml_code,reasoning
source_sha256: 02e99eef50ef722aa0c020fccbaeb59daa7cca0e303c247f50450c0eb26bc80d
actual_sha256: 02e99eef50ef722aa0c020fccbaeb59daa7cca0e303c247f50450c0eb26bc80d
sha256_match: True
NL: Imagine you're at a restaurant and you're trying to order a meal. You want to order a burger...
STM_0: @startuml | [*] --> "Menu Created" | "Menu Created" --> "Adding Items" | "Adding Items" --> "Viewing Menu" ...
first_failed_pair: unified_uml_state_train_0060 No valid PlantUML code found.
```

## 6. 审计不变量

任一 eligible / conditional pair 必须能用 `source_asset_id + source_locator + source_sha256` 回到 `raw/umlcode_state_diagram_train.parquet` 对应行和列；hash 不一致或 locator 无法定位时，不得计入 eligible generated seed count。生成失败行必须保留但不得计入 eligible generated seed count。
