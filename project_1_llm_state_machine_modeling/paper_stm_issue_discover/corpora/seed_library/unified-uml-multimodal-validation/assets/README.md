# assets: unified-uml-multimodal-validation

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：Nguyen et al., *A Novel Unified Framework for Automated Generation and Multimodal Validation of UML Diagrams*, CMES 2026，DOI <https://doi.org/10.32604/cmes.2025.075442>。
- 一手数据入口：HF dataset <https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram>。
- 版本：HF API 记录 `sha=e330d1afc19361ecbc970348b94cd858e5d32df6`，访问日期 2026-06-22。
- 当前角色：已提交 HF parquet、版本 pin、raw hash 与逐行 locator，989 条有效 `input + uml_code` 可回溯复验，因此按 `final_pool_ready` 处理；公开学术数据使用时在论文中引用原作即可，许可 / 再分发不再作为升绿 blocker。
- caveat：NL 是 LLaMA-3.2-1B-Instruct 生成的 synthetic feature description / 非控制系统真实需求；PlantUML 由 DeepSeek-R1-Distill-Qwen-32B 生成并经正则抽取。该条目适合 synthetic UML state-diagram smoke / stress，不应包装成控制系统需求数据。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | storage | license | 说明 |
|---|---|---|---|---:|---|---|---|
| `hf_state_dataset_record` | HF API metadata | `raw/hf_state_dataset_record.json` | `76c5410b732420d8c91dfed5334868065326158a87987df076e8f3f3902fd957` | 1460 | committed | paper_public_resource | 记录 dataset features / splits / revision |
| `hf_state_dataset_tree` | HF tree metadata | `raw/hf_state_dataset_tree.json` | `fdf4e8c7ace4d99c1efc0859840f284edda21116e515cc16cb18c8a9dbb79aaf` | 381 | committed | paper_public_resource | 记录 repo 文件树 |
| `hf_state_train_parquet` | `NL + STM_0` dataset | `raw/umlcode_state_diagram_train.parquet` | `02e99eef50ef722aa0c020fccbaeb59daa7cca0e303c247f50450c0eb26bc80d` | 1620142 | committed | paper_public_resource | 999 行 `input/reasoning/uml_code`；其中 989 行是有效 PlantUML，10 行为 `No valid PlantUML code found.` |

## 2.1 数据构造与质量抽检说明

- 论文流程：LLaMA-3.2-1B-Instruct 生成 user-focused feature descriptions；DeepSeek-R1-Distill-Qwen-32B 生成 PlantUML；随后进入渲染、多 VLM ensemble 与人类专家相关性验证。
- 论文级 validation：论文报告渲染 / VLM / expert validation，包括 Qwen2.5-VL-3B、LLaMA-3.2-11B-Vision-Instruct、Aya-Vision-8B 等 VLM ensemble，以及 94 位专家 validation、Fleiss' Kappa 0.78、Pearson r 0.82。
- 当前 HF parquet 只含 `input`、`reasoning`、`uml_code` 三列；本地抽取物没有逐行 VLM / human score。因此当前 eligible 判定只证明 raw locator、hash 与 PlantUML block 结构可回溯，不等于逐行人工质量验收。
- NL 数量：raw 999 条、unique 999 条；其中 989 条 eligible generated pair 的 NL exact / whitespace-normalized 去重后均唯一，未发现少量 NL 对多个 STM 的 1×N 形态。10 个生成失败行索引为 `[60, 101, 162, 194, 309, 418, 607, 785, 838, 890]`，已在 `assets/extracted/validation_summary.json` 的 `excluded_pair_ids` 中列出；这些行共享同一个 `No valid PlantUML code found.` sentinel，只作 NL-only / failure 审计，不参与 unique generated `STM_0` 统计。
- 质量抽检：抽检 row 0--4，NL 分别是餐厅下单 / 菜单管理、自动标签、个性化产品推荐、内容管理、任务管理等通用软件 feature，不是控制系统需求；5 行均可由 locator 回到 raw parquet，均含 `@startuml` / `@enduml` 与状态迁移箭头。

## 2.2 抽检样例

| row | pair_id | NL 摘要 | PlantUML 状态机形态 | 结论 |
|---:|---|---|---|---|
| 0 | `unified_uml_state_train_0000` | 餐厅一次性点餐 / 菜单 | 有 `@startuml` / `@enduml` 与多条 `-->` | locator / hash 可回溯；通用软件 feature |
| 1 | `unified_uml_state_train_0001` | Auto-Tagging 元数据自动打标 | 有开始 / 处理 / 成功 / 失败状态 | locator / hash 可回溯；非控制系统需求 |
| 2 | `unified_uml_state_train_0002` | 个性化产品推荐 | 有浏览、搜索、详情、推荐等状态 | locator / hash 可回溯；synthetic feature |
| 3 | `unified_uml_state_train_0003` | Smart Content Management | 有 content creation / organization / access 状态链 | locator / hash 可回溯；状态图较浅 |
| 4 | `unified_uml_state_train_0004` | 自动化任务管理 | 有 task list / assignment / notification 状态链 | locator / hash 可回溯；状态迁移较少 |

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

任一 eligible / final-pool pair 必须能用 `source_asset_id + source_locator + source_sha256` 回到 `raw/umlcode_state_diagram_train.parquet` 对应行和列；hash 不一致或 locator 无法定位时，不得计入 eligible generated seed count。生成失败行必须保留但不得计入 eligible generated seed count。
