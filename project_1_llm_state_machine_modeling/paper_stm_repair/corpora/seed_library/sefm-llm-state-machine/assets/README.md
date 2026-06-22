# assets: sefm-llm-state-machine

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：Abdulkarim et al., arXiv:2604.00275, <https://arxiv.org/abs/2604.00275>。
- 一手制品入口：4open artifact <https://anonymous.4open.science/#!/r/llm_state_machine_modeling/>，ZIP API <https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip>。
- 当前状态：4open ZIP 已 committed 到 `assets/raw/`，并已抽取 1 组 SSC7 `NL + generated STM_0`。该 pair 已通过 raw ZIP hash、ZIP member locator、Python symbol 和文本 hash 回溯；但 artifact license / redistribution / release pin 仍未闭合，因此本条目仍是 `conditional_final_pool`，不是 `final_pool_ready`。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | storage | license | 说明 |
|---|---|---|---|---:|---|---|---|
| `sefm_4open_zip` | 作者 4open artifact ZIP | `raw/llm_state_machine_modeling_4open.zip` | `0e553383b5bd03702d29e5f68a3624fcc143a51da1fd0c9156b32ba51a5b61b4` | 3357298 | committed | unknown | 含 `state_machine_descriptions.py`、Final Single Prompt generated output、reference solutions、代码和 F1 workbook；license / release / DOI 未闭合 |

## 3. raw → extracted 映射

- `assets/raw/llm_state_machine_modeling_4open.zip` 中 `backend/resources/state_machine_descriptions.py` 的 Python 字符串 `SSC7_fall_2024` 映射到 `pairs.jsonl.nl_text`。
- 同一 ZIP 中 `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_f700645345f84b5acffd751f426344ed704910d9.txt` 的全文映射到 `pairs.jsonl.stm0_text`。
- `source_locator_type` 为 `zip_python_symbol_and_text_file`；validator 会重新打开 ZIP、解析 Python 字符串并读取 generated Umple 文本。
- `Paper Experiment Resources/Reference Solutions/*.txt` 只能作为 reference solution，不得计入 generated `STM_0`。

## 4. Python 加载方法

在本条目目录运行下列代码。它会真实读取 `assets/extracted/pairs.jsonl` 的第一组 pair，并输出一段可读的 SSC7 NL 与 Claude Sonnet 3.5 single-prompt generated Umple：

```python
from pathlib import Path
import json

base = Path('assets')
row = json.loads((base / 'extracted/pairs.jsonl').read_text().splitlines()[0])

print('pair_id:', row['pair_id'])
print('source_asset_id:', row['source_asset_id'])
print('source_locator_type:', row['source_locator_type'])
print('source_locator:', row['source_locator'])
print('source_sha256:', row['source_sha256'])
print('trace_verified:', row['trace_verified'])
print('eligibility_state:', row['eligibility_state'])

# 人类可读输出：NL 应该是 SSC7 自助结账系统的自然语言系统描述；
# STM_0 应该是 Claude Sonnet 3.5 single-prompt 生成的 Umple 状态机，
# 能看到 Ready、WeighingItem、SecurityCheck、Payment、Override、Timeout 等状态。
print('NL snippet:', row['nl_text'][:360].replace('\n', ' '))
print('STM_0 snippet:', row['stm0_text'][:360].replace('\n', ' | '))
```

期望输出形态如下（片段截断不影响审计；完整文本在 `pairs.jsonl` 与 raw ZIP locator 中）：

```text
pair_id: sefm_ssc7_single_prompt_claude_sonnet35_0001
source_asset_id: sefm_4open_zip
source_locator_type: zip_python_symbol_and_text_file
source_locator: nl_member=backend/resources/state_machine_descriptions.py; nl_symbol=SSC7_fall_2024; stm0_member=Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_f700645345f84b5acffd751f426344ed704910d9.txt
source_sha256: 0e553383b5bd03702d29e5f68a3624fcc143a51da1fd0c9156b32ba51a5b61b4
trace_verified: True
eligibility_state: conditional_final_pool
NL snippet: The Self-Service Checkout SSC7 is used by supermarkets to allow customers to scan their purchases and pay for them, often without any help of supermarket staff. As shown in the figure on the right, the SSC7 consists of the following parts...
STM_0 snippet:  | class SSC7S { |   sm { |     Ready { |       scanBarcode [isValidBarcode] -> SecurityCheck; |       scanBarcode [!isValidBarcode] -> /{showError();} Ready; |       enterCode [isValidCode] -> WeighingItem; ...
```

## 5. 期望输出字段

示例必须输出 `pair_id`、`source_asset_id`、`source_locator_type`、`source_locator`、`source_sha256`、`trace_verified=True`、`eligibility_state`、`NL snippet` 与 `STM_0 snippet`。人类读者应能直接看出：这是一组 **SSC7 自助结账系统自然语言描述 → Claude Sonnet 3.5 single-prompt generated Umple 状态机** 的作者制品 pair。

## 6. 审计不变量

任一 `sefm` generated pair 必须能用 `source_asset_id + source_locator + source_sha256` 回到 committed raw ZIP。reference solutions 永远不能冒充 generated `STM_0`。若后续继续抽取其他系统或其他策略输出，必须逐条补 ZIP member locator、hash 与 `validation_summary.json`，并保持 license / redistribution caveat 可见。
