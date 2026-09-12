# assets: fsm-bench-20

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 数据集 / benchmark：FSM-Bench-20，Zenodo DOI <https://doi.org/10.5281/zenodo.20517969>。
- 作者仓库：<https://github.com/cesar-andress/llm-fsm-local-benchmark/tree/v1.0.0>。
- 许可：MIT（由 Zenodo/GitHub release metadata 与 LICENSE 指示）。
- 关键结论：公开包提供 NL requirements、prompt、schema、run/eval 脚本，但**未提供作者生成的 `STM_0` 输出**，因此本条目是 `pipeline_only`，不能直接作为现成 seed。当前已额外记录一个 `NL+code 一手可复跑` 连通性检查：不修改作者源码，仅用本地 Ollama-compatible proxy 把 `/api/chat` 转到 `.env` 的 OpenAI-compatible `gpt-5.5`，单系统 `elevator` 跑通；该输出只证明流程连通，不计作者一手 pair。作者 campaign 中的 qwen2.5-coder、llama3.1、mistral-nemo、gemma2、phi3 等本地模型均已按 Ollama 模型页作为可定位入口登记，但模型可用性不改变 pipeline-only 角色。
- NL 数量：release ZIP 中 `dataset/systems/*.json` 共 20 个系统、252 条 requirements，exact / whitespace-normalized 去重后仍为 252 条。`benchmark/gold/*.json` 共 20 个文件但内容为空 `{}` placeholder，不能冒充 reference 或 generated `STM_0`。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | 说明 |
|---|---|---|---|---:|---|
| `zenodo_record` | Zenodo metadata | `raw/zenodo_record.json` | `3f59204af9e1058057c75a4cea4257cb1479bee1360fcc38fda3c1182ecdd341` | 5619 | DOI / license / file metadata |
| `github_repo` | GitHub metadata | `raw/github_repo.json` | `8aecd85dd991232b6d5828cd01e87864d5c860112c5e4ee79929895928a92f89` | 6506 | repo metadata |
| `github_contents_v1` | GitHub tree metadata | `raw/github_contents_v1.0.0.json` | `723285b07f394c1faec7982c296fa386b6670b19ce055245d976f51ea5707c79` | 14207 | tag contents |
| `zenodo_release_zip` | pipeline zip | `raw/llm-fsm-local-benchmark-v1.0.0.zip` | `c511586daf5c2374cdcae35f616a1bb693cef6ec792582bcdead439d839b9b9a` | 116515 | NL/prompt/schema/code；无 generated STM outputs |
| `openai_compatible_connectivity_check_record` | 复跑连通性检查记录 | `extracted/openai_compatible_connectivity_check_record.json` | `5f1086c11dc8ae0363ef469e8f5c5fb5b620997d260a73ba86519b0cabf891dd` | 2303 | 作者源码不改，通过本地 Ollama-compatible proxy 走 `.env` gpt-5.5 跑通 `elevator` 单系统；不是作者生成输出 |

## 3. raw → extracted 映射

当前 registry 条目未生成可计 pair，因为没有一手 generated `STM_0`。ZIP 中 `dataset/systems/*.json` 只提供 NL requirements；`benchmark/gold/*.json` 为空 `{}` placeholder，不能冒充 generated seed 或 reference seed。`extracted/openai_compatible_connectivity_check_record.json` 只记录“作者代码 + 本地 proxy + gpt-5.5”单系统连通性，用于证明后续可复跑构造本项目 seed。

## 4. Python 加载方法

在本条目目录运行，检查 ZIP 内是否只有 NL 数据而无 generated output：

```python
from pathlib import Path
import zipfile, hashlib
raw = Path('assets/raw/llm-fsm-local-benchmark-v1.0.0.zip')
print('actual_sha256:', hashlib.sha256(raw.read_bytes()).hexdigest())
with zipfile.ZipFile(raw) as zf:
    names = zf.namelist()
    system_files = [n for n in names if '/dataset/systems/' in n and n.endswith('.json')]
    gold_files = [n for n in names if '/benchmark/gold/' in n and n.endswith('.json')]
    requirements = []
    for name in system_files:
        import json
        data = json.loads(zf.read(name))
        requirements.extend(data.get('requirements', []))
    print('dataset_system_count:', len(system_files))
    print('requirement_count:', len(requirements))
    print('unique_requirement_count:', len(set(r.strip() for r in requirements)))
    print('gold_file_count:', len(gold_files))
    print('first_gold_content:', zf.read(gold_files[0]).decode('utf-8').strip() if gold_files else None)
    print('generated_output_files:', [n for n in names if '/outputs/' in n or '/results/' in n][:5])
```

## 5. 期望输出字段

期望看到 `dataset_system_count=20`、`requirement_count=252`、`unique_requirement_count=252`、`gold_file_count=20`、`first_gold_content={}`，且 `generated_output_files` 为空或不含可用 `STM_0`；这正是 `pipeline_only` 结论的依据。

## 6. NL+code 复跑 连通性检查

本轮连通性检查解压 Zenodo/GitHub v1.0.0 ZIP 到临时目录，不修改作者源码；只按 `REPRODUCIBILITY.md` 要求从 `docs/experimental_prompts.md` 创建本地 `prompts/` 文件，并启动本地 `/api/tags`、`/api/chat` 兼容代理，把作者 Ollama HTTP 合约转发到本仓库 `.env` 中的 OpenAI-compatible `gpt-5.5`。命令等价于：

```bash
python scripts/run_experiment.py --systems elevator --models gpt-5.5 --host <local_ollama_compatible_proxy> --skip-missing
```

`assets/extracted/openai_compatible_connectivity_check_record.json` 记录：`status=ok`、`source_code_modified=false`、`raw_output_files=[outputs/raw/gpt-5.5/elevator.json]`、`cleaned_output_files=[outputs/cleaned/gpt-5.5/elevator.json]`。样例输出是一个极小 JSON FSM，质量不足以作实验 seed；它只证明作者 pipeline 能在不改源码的前提下接入 `.env` 的 OpenAI-compatible 模型并跑完一个系统。

## 7. 审计不变量

本条目没有 eligible generated pair；任何后续复跑得到的 `STM_0` 必须另建本项目 run record，不能写成本条目作者已公开的一手 generated output。
