# assets: sefm-llm-state-machine

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：Abdulkarim et al., arXiv:2604.00275, <https://arxiv.org/abs/2604.00275>。
- 一手制品入口：4open artifact <https://anonymous.4open.science/#!/r/llm_state_machine_modeling/>，ZIP API <https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip>。
- 当前状态：当前 registry 条目只登记 4open 一手入口；未提交 ZIP，因此不能标为 `final_pool_ready`。

## 2. 资源盘点表

| asset_id | 角色 | local_path | storage | license | 说明 |
|---|---|---|---|---|---|
| `sefm_4open_metadata` | 一手制品 metadata pointer | `raw/4open_metadata.json` | committed metadata | unknown | 指向 4open browser/ZIP 与必须冻结的文件路径 |

## 3. raw → extracted 映射

当前 registry 条目未抽取 `pairs.jsonl`。后续要升级时，必须从 4open ZIP 中直接读取：

- `backend/resources/state_machine_descriptions.py` 的 `SSC7_fall_2024` 作为 NL；
- `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt` 作为 generated `STM_0`；
- `Paper Experiment Resources/Reference Solutions/*.txt` 只能进 `reference_sets`，不得计入 generated seed。

## 4. Python 加载方法

当前只能加载 metadata：

```python
from pathlib import Path
import json
meta = json.loads(Path('assets/raw/4open_metadata.json').read_text())
print(meta['artifact_browser'])
print(meta['known_required_files'])
```

## 5. 期望输出字段

期望输出 artifact browser、ZIP URL 和 required file list。由于没有 committed raw ZIP，本条目不能展示可回溯 `NL + STM_0` 示例，最高只能是 `conditional_final_pool`。

## 6. 审计不变量

在 ZIP 未落盘并完成 hash / locator / 文本回溯前，任何 `sefm` pair 不得计入 eligible generated seed count。reference solutions 永远不能冒充 generated `STM_0`。
