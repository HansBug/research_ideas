# assets: ttool-ai-smd-subset

⚠️ 本目录只放一手来源资产及其直接抽取物；旧缓存、人工复写、二手摘要不得入内。

## 1. 一手来源说明

- 论文：*System Architects Are not Alone Anymore: Automatic System Modeling with AI*，HAL <https://telecom-paris.hal.science/hal-04483279>，DOI <https://doi.org/10.5220/0012320100003645>。
- 作者工件仓库：<https://github.com/zebradile/ttool-ai>；本目录固定 `main` 上的 commit `f2c52282cb7a826c31e7ab512356d42230c6d321`。
- 作者 README 说明：每个主案例目录包含系统规格文本和由 `TTool + ChatGPT 3.5` 生成的 TTool `.xml` 模型，除图形布局调整外无人工修改；仓库根层 `results.ods` 给出时间和质量评价。
- 当前角色：**`conditional_final_pool` / `NL+STM一手（条件）`**。它确实公开了 `NL + generated SysML/TTool XML` 工件；但这些 XML 是完整 TTool/SysML/AVATAR 工件，不是已经切好的纯 T0 FSM/HSM/EFSM/statechart，需要后续转换器明确 SMD 切片、`after` / signal / guard / action 等语义处理后才能进入最终实验池。
- 源码边界：作者仓库是公开工件 / 复现说明，不是完整 TTool-AI 实现源码；源码可用性因此标为 `🟠片段/部分`。
- 模型边界：作者 README 复现说明含 `gpt-3.5-turbo` 与 `gpt-4-0125-preview`；截至 2026-06-23，`gpt-3.5-turbo` 属 legacy 且尚未到 2026-10-23 shutdown，`gpt-4-0125-preview` 已过 2026-03-26 弃用节点，原组合不可视为稳定可 bitwise 复现。

## 2. 资源盘点表

| asset_id | 角色 | local_path | sha256 | bytes | storage | 说明 |
|---|---|---|---|---:|---|---|
| `github_repo_metadata` | GitHub metadata | `raw/github_repo.json` | 见 `manifest.json` | 5476 | committed | 作者工件仓库 metadata。 |
| `github_commit_main_metadata` | commit metadata | `raw/github_commit_main.json` | 见 `manifest.json` | 5938 | committed | 固定 `main` commit 的 metadata。 |
| `ttool_ai_source_archive` | 作者工件 ZIP | `raw/ttool-ai_f2c52282cb7a826c31e7ab512356d42230c6d321.zip` | 见 `manifest.json` | 1207033 | committed | 系统规格、生成 XML、`results.ods`、README；不是完整 TTool-AI 源码。 |

## 3. raw → extracted 映射

`assets/extracted/pairs.jsonl` 由 ZIP 中下列成员配对抽取：

| pair_id | NL member | STM_0 / XML member | 当前用途 |
|---|---|---|---|
| `ttool-ai-automatedbraking` | `AutomatedBraking/automatedbraking.md` | `AutomatedBraking/automatedbraking.xml` | 条件 pair；需切出 SMD / T0 子集。 |
| `ttool-ai-dps` | `DPS/dps.md` | `DPS/dps.xml` | 条件 pair；需切出 SMD / T0 子集。 |
| `ttool-ai-platooning` | `platooning/platoonings.md` | `platooning/platoonings.xml` | 条件 pair；需切出 SMD / T0 子集。 |
| `ttool-ai-incoherency-automatedbraking` | `incoherencies/specification_automatedbraking.md` | `incoherencies/automatedbraking.xml` | 条件 pair；含 incoherency correction 上下文，使用时需避免混入 repair 结果。 |
| `ttool-ai-incoherency-dps` | `incoherencies/specification_dps.md` | `incoherencies/dps.xml` | 条件 pair；含 incoherency correction 上下文，使用时需避免混入 repair 结果。 |
| `ttool-ai-incoherency-spacebasedsystem` | `incoherencies/specification_spacebasedsystem.md` | `incoherencies/spacebasedsystem.xml` | 条件 pair；含 incoherency correction 上下文，使用时需避免混入 repair 结果。 |

抽取文件说明：

| extracted 文件 | 说明 |
|---|---|
| `extracted/pairs.jsonl` | 6 组 `NL + generated XML` 条件 pair；每行包含 `source_locator_type=zip_member_pair` 与 `nl_member/stm0_member`。 |
| `extracted/pairs_preview.md` | 人类可读预览，展示每个 locator 与 NL/XML 片段。 |
| `extracted/field_mapping.md` | 字段映射与使用边界。 |
| `extracted/validation_summary.json` | validator 复算计数：6 raw / 6 trace / 6 conditional eligible。 |

## 4. Python 加载方法

在本条目目录运行：

```python
from pathlib import Path
import hashlib, json, zipfile

base = Path('assets')
manifest = json.loads((base / 'manifest.json').read_text(encoding='utf-8'))
assets = {item['asset_id']: item for item in manifest['assets']}
asset = assets['ttool_ai_source_archive']
raw_path = base / asset['local_path']
actual_sha = hashlib.sha256(raw_path.read_bytes()).hexdigest()
print('source_commit:', asset['version_pin'])
print('source_archive_sha256_match:', actual_sha == asset['sha256'])

pairs = [json.loads(line) for line in (base / 'extracted/pairs.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
row = pairs[0]
print('pair_count:', len(pairs))
print('pair_id:', row['pair_id'])
print('eligibility_state:', row['eligibility_state'])
print('source_locator_type:', row['source_locator_type'])
print('source_locator:', row['source_locator'])
print('source_sha256:', row['source_sha256'])
print('NL preview:', row['nl_text'][:400])
print('STM_0 preview:', row['stm0_text'][:600])

with zipfile.ZipFile(raw_path) as zf:
    locator = dict(part.split('=', 1) for part in row['source_locator'].split(';'))
    raw_nl = zf.read(locator['nl_member']).decode('utf-8')
    raw_stm = zf.read(locator['stm0_member']).decode('utf-8')
    print('nl_hash_match:', hashlib.sha256(raw_nl.encode()).hexdigest() == row['nl_sha256'])
    print('stm0_hash_match:', hashlib.sha256(raw_stm.encode()).hexdigest() == row['stm0_sha256'])
```

期望输出至少包含：

```text
source_commit: git_commit:f2c52282cb7a826c31e7ab512356d42230c6d321
source_archive_sha256_match: True
pair_count: 6
pair_id: ttool-ai-automatedbraking
eligibility_state: conditional_final_pool
source_locator_type: zip_member_pair
nl_hash_match: True
stm0_hash_match: True
```

## 5. 审计不变量

1. 本条目的 `assets/raw/` 只能保存作者 GitHub 工件仓库及其 metadata；旧 `reproduction/`、旧 parquet、`project_ex1` review extraction 不得进入 raw，也不得作为 pair 数来源。
2. `pairs.jsonl` 的 `STM_0` 是作者公开 TTool XML 工件，不是纯状态机片段；进入修正实验前必须另做 SMD/T0 切片 run record。
3. `incoherencies/` 下 3 组 pair 可能包含 correction / incoherency workflow 结果；若后续研究只需要初始 generation seed，应优先使用主案例目录，并把 incoherency outputs 排除或单独标注。
4. 复跑作者流程需要 TTool、OpenAI key 与 legacy/retired 模型替代策略；任何复跑输出都是本项目新 run，不得覆盖作者公开工件事实。
