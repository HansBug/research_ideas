# assets: designing-fsm-gpt4

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：*Designing Finite State Machines with GPT-4*, arXiv <https://arxiv.org/abs/2603.29140>。
- 作者代码入口：<https://github.com/Paul3246/nl2fsm>，当前固定 commit `354f9aacf51b5121abb8a2e04718232185e71928`。
- 当前角色：**`NL+code 一手可复现（条件）`**。作者仓库提供随机 / 合成 NL 生成、OpenAI 调用、CSV FSM 生成、错误刻画与若干 repair 版本代码；作者仓库内虽含 `generated_text.csv` / Graphviz 等未配对 run artifacts，但没有作者冻结的一手 `<NL, STM_0>` pair 包、pair index 或可回溯 NL locator，因此不升级为 `final_pool_ready`。这里的 NL 是运行时合成，不是冻结发布的固定输入集。
- 使用边界：只可把 `err_lim/model.py` / `err_lim/pipeline.py` 的**初始生成切片**作为可复跑线索；`v1`--`v5`、distinguishing/checking sequence、fault-model 与 oracle / repair 输出不得混入初始 seed。
- 模型边界：源码硬编码 `gpt-4o`，repair 变体中另有旧 `gpt-3.5-turbo` 字符串；当前源码 ZIP 未检出 `gpt-4o-mini` literal；`.env` 只能注入 key / endpoint，不能单靠 `LLM_MODEL=gpt-5.5` 改源码模型名。若本地 OpenAI-compatible proxy 支持 model alias，或用本地代理把 `gpt-4o` 请求转到 `.env` 中的 `gpt-5.5`，可以不改作者源码跑通初始调用路径；否则需要改代码。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | storage | license | 说明 |
|---|---|---|---|---:|---|---|---|
| `nl2fsm_source_archive` | 作者源码快照 | `raw/nl2fsm_354f9aacf51b5121abb8a2e04718232185e71928.zip` | 见 `manifest.json` | 7605808 | committed | paper_public_resource | 由作者 GitHub 仓库 commit `354f9aacf51b5121abb8a2e04718232185e71928` 生成的 git archive；源码保持不改 |

## 3. raw → extracted 映射

当前没有 `pairs.jsonl`，因为作者没有发布稳定的一手 `<NL, STM_0>` pair 包；源码 ZIP 内的 `generated_text.csv` / Graphviz outputs 只是未配对 run artifacts，缺少冻结 NL locator / pair index，因此只在 manifest 的 `skipped_assets` 中登记，不计 author first-source pair。本目录只保存：

| extracted 文件 | 说明 |
|---|---|
| `extracted/openai_compatible_smoke_record.json` | 本地用未修改源码 `err_lim/model.py::generate_text` 接入 OpenAI-compatible proxy 的最小 smoke 记录；证明初始 LLM 生成调用路径可走通 |
| `extracted/openai_compatible_smoke_output.csv` | smoke 输出的两状态 Mealy CSV 片段；只作代码连通性证据，不是作者发布 seed |

## 4. Python 加载方法

在本条目目录运行，检查源码快照和 smoke 记录：

```python
from pathlib import Path
import json, zipfile, hashlib

base = Path('assets')
manifest = json.loads((base / 'manifest.json').read_text())
asset = manifest['assets'][0]
raw = base / asset['local_path']
actual_sha = hashlib.sha256(raw.read_bytes()).hexdigest()
print('source_commit:', asset['version_pin'])
print('source_archive_sha256_match:', actual_sha == asset['sha256'])

with zipfile.ZipFile(raw) as zf:
    names = zf.namelist()
    print('has_err_lim_model:', any(n.endswith('err_lim/model.py') for n in names))
    model_py = zf.read([n for n in names if n.endswith('err_lim/model.py')][0]).decode('utf-8')
    print('source_contains_gpt4o_literal:', 'model="gpt-4o"' in model_py)

record = json.loads((base / 'extracted/openai_compatible_smoke_record.json').read_text())
print('smoke_status:', record['status'])
print('source_code_modified:', record['source_code_modified'])
print('source_model_literal:', record['source_model_literal'])
print('mock_model:', record['mock_model'])
print('expected_csv_header_seen:', record['expected_csv_header_seen'])
print('output_preview:', record['output_preview'])
```

## 5. 期望输出字段

示例必须输出 `source_commit=git_commit:354f9aacf51b5121abb8a2e04718232185e71928`、`source_archive_sha256_match=True`、`has_err_lim_model=True`、`source_contains_gpt4o_literal=True`、`smoke_status=ok`、`source_code_modified=False`、`source_model_literal=gpt-4o`、`mock_model=gpt-5.5`、`expected_csv_header_seen=True`。人类读者应能直接看出：这只是 **作者未修改源码的初始 NL→CSV 调用路径 smoke**，不是作者公开的 `<NL, STM_0>` 数据集。

期望输出片段：

```text
source_commit: git_commit:354f9aacf51b5121abb8a2e04718232185e71928
source_archive_sha256_match: True
has_err_lim_model: True
source_contains_gpt4o_literal: True
smoke_status: ok
source_code_modified: False
source_model_literal: gpt-4o
mock_model: gpt-5.5
expected_csv_header_seen: True
output_preview: State,Input,Output,Next_State
S0,a,0,S1
S1,a,1,S0
```

## 6. 最小 smoke / 复跑说明

本地 smoke 的可复验思路：

```bash
# 1) 不修改作者源码，解压或 clone 作者仓库到临时目录。
# 2) 运行真实 API 前 source 本仓库 .env。
source .env
export OPENAI_API_KEY="$LLM_API_KEY"
export OPENAI_BASE_URL="${LLM_ENDPOINT%/}/v1"

# 3) 若要让硬编码 gpt-4o 走 .env 的 gpt-5.5，需要代理层做 alias 或本地 OpenAI-compatible 转发；
#    直接把 OPENAI_BASE_URL 指向当前 sub2api 时，本轮 `gpt-4o` 直连返回 503，`.env` 中 `gpt-5.5` 可用。
# 4) 仅运行 err_lim/model.py::generate_text 或 err_lim/pipeline.py 的小样本切片。
```

本轮实际记录：

- 直接用 `.env` 的 `LLM_ENDPOINT/v1 + LLM_MODEL=gpt-5.5` 调用 OpenAI-compatible API 可成功返回 `OK`。
- 当前 sub2api 端点对 `gpt-4o` 直连返回 503；因此用本地最小代理把作者源码硬编码的 `gpt-4o` 请求转给 `.env` 的 `gpt-5.5`，未修改作者源码并成功得到 CSV。
- 尝试运行 `err_lim/pipeline.py` 的小样本 `generate_automaton_prompt(2) + err_car(...)` 时，已产出 `generated_text.csv` 和 Graphviz 图文件，但完整 product-analysis 流程在 120 秒审计 timeout 内未结束；这只说明“初始生成 + 部分处理路径可走”，不能升级为完整论文 pipeline 复现。

## 7. 审计不变量

1. 本条目的 `assets/raw/` 只能保存作者 GitHub commit / release 等一手源码快照；不得把本仓库旧 parquet、旧 predictions 或人工修补结果放入 raw。
2. `extracted/` 中的 smoke 输出只作代码可连通证据，不计 `eligible_generated_pair_count`。
3. 若后续要把本条目升级为 seed，必须另建 run record：记录随机种子、生成的 NL、prompt、模型精确 ID、endpoint、raw output、CSV、hash、错误、重试和 eligibility；且必须剥离 oracle / repair 输出。
4. 源码 ZIP 内已有 `generated_text.csv` / Graphviz outputs 也只能作为未配对 run artifacts 审计线索；任何复跑得到的 `STM_0` 都是**本项目生成的新 seed**，不是作者已经公开的一手 pair。
