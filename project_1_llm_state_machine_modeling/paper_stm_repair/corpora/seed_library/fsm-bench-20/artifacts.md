# artifacts: fsm-bench-20

## 本地冻结文件

| 文件 | 状态 | 说明 |
|---|---|---|
| `zenodo_record.json` | present | Zenodo API record；license 为 MIT；文件入口为 v1.0.0 zip。 |
| `github_repo.json` | present | GitHub repository API record。 |
| `github_contents_v1.0.0.json` | present | tag `v1.0.0` 根目录 contents。 |
| `llm-fsm-local-benchmark-v1.0.0.zip` | present | Zenodo 下载包；大小约 116 KB。 |
| `extracted_sample/` | present | 抽取 README、LICENSE、REPRODUCIBILITY、prompt、schema 与两个系统 JSON 样例。 |
| `extracted_sample_manifest.json` | present | 抽样文件 SHA-256 清单。 |

## 外部入口

| 入口 | URL | 核验结果 |
|---|---|---|
| Zenodo v1.0.0 | https://doi.org/10.5281/zenodo.20517969 | open access；MIT license；zip 可下载。 |
| GitHub tag | https://github.com/cesar-andress/llm-fsm-local-benchmark/tree/v1.0.0 | public repo；tag / release 可访问。 |
| GitHub release | https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.0.0 | release 存在；需注意 assets 状态。 |

## artifact 判定

- 可用：dataset systems、prompt specification、FSM JSON schema、evaluation / run scripts、MIT license、Zenodo DOI。
- 不足：公开 ZIP 中 `benchmark/gold/*.json` 为 `{}` placeholder；未冻结 generated outputs / results / figures。
- 当前等级：`SA-2`（带条件备注），仅适合作为 R2 复跑前置候选；不直接计入已生成 `STM_0` 主 seed；条件性不作为新的 SA 枚举。

## Artifact-only 例外

本候选是 Zenodo/GitHub benchmark record，不是论文条目；无 `paper.pdf` / `paper_content.txt`。R1.6 的证据来自 DOI record、GitHub tag、ZIP、README、prompt、schema 和样例 dataset。
