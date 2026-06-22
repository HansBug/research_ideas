# assets: fsm-bench-20

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 数据集 / benchmark：FSM-Bench-20，Zenodo DOI <https://doi.org/10.5281/zenodo.20517969>。
- 作者仓库：<https://github.com/cesar-andress/llm-fsm-local-benchmark/tree/v1.0.0>。
- 许可：MIT（由 Zenodo/GitHub release metadata 与 LICENSE 指示）。
- 关键结论：公开包提供 NL requirements、prompt、schema、run/eval 脚本，但**未提供作者生成的 `STM_0` 输出**，因此本条目是 `pipeline_only`，不能直接作为现成 seed。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | 说明 |
|---|---|---|---|---:|---|
| `zenodo_record` | Zenodo metadata | `raw/zenodo_record.json` | `3f59204af9e1058057c75a4cea4257cb1479bee1360fcc38fda3c1182ecdd341` | 5619 | DOI / license / file metadata |
| `github_repo` | GitHub metadata | `raw/github_repo.json` | `8aecd85dd991232b6d5828cd01e87864d5c860112c5e4ee79929895928a92f89` | 6506 | repo metadata |
| `github_contents_v1` | GitHub tree metadata | `raw/github_contents_v1.0.0.json` | `723285b07f394c1faec7982c296fa386b6670b19ce055245d976f51ea5707c79` | 14207 | tag contents |
| `zenodo_release_zip` | pipeline zip | `raw/llm-fsm-local-benchmark-v1.0.0.zip` | `c511586daf5c2374cdcae35f616a1bb693cef6ec792582bcdead439d839b9b9a` | 116515 | NL/prompt/schema/code；无 generated STM outputs |

## 3. raw → extracted 映射

当前 registry 条目未生成 `assets/extracted/pairs.jsonl`，因为没有一手 generated `STM_0`。ZIP 中 `dataset/systems/*.json` 只提供 NL requirements；`benchmark/gold/*.json` 不能冒充 generated seed。

## 4. Python 加载方法

在本条目目录运行，检查 ZIP 内是否只有 NL 数据而无 generated output：

```python
from pathlib import Path
import zipfile, hashlib
raw = Path('assets/raw/llm-fsm-local-benchmark-v1.0.0.zip')
print('actual_sha256:', hashlib.sha256(raw.read_bytes()).hexdigest())
with zipfile.ZipFile(raw) as zf:
    names = zf.namelist()
    print('dataset_system_count:', sum('/dataset/systems/' in n and n.endswith('.json') for n in names))
    print('generated_output_files:', [n for n in names if '/outputs/' in n or '/results/' in n][:5])
```

## 5. 期望输出字段

期望看到 `dataset_system_count > 0` 且 `generated_output_files` 为空或不含可用 `STM_0`；这正是 `pipeline_only` 结论的依据。

## 6. 审计不变量

本条目没有 eligible generated pair；任何后续复跑得到的 `STM_0` 必须另建本项目 run record，不能写成本条目作者已公开的一手 generated output。
