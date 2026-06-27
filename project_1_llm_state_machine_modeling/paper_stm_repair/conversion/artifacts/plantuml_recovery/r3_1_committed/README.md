# R3.1 PlantUML recovery archive

本目录保存 R3.1 PlantUML pre-SCXML normalization / recovery 的高基数运行制品。它对应 [../../../reports/plantuml_recovery_report.json](../../../reports/plantuml_recovery_report.json) 与 [../../../reports/plantuml_normalization_ledger.jsonl](../../../reports/plantuml_normalization_ledger.jsonl)，用于在不把几千个散文件暴露到 PR diff 的前提下，完整保留 raw / normalized candidate 与官方 PlantUML SCXML 证据。

## 文件说明

| 文件 | 作用 |
|---|---|
| `workdir.zip` | 全量 high-cardinality 运行目录 archive；包含 `normalized_candidates/` 与 `official_scxml/`。 |
| `workdir.zip.sha256` | `workdir.zip` 的 SHA-256 校验文件。 |
| `manifest.json` | archive 元数据：文件总数、按顶层目录 / 后缀统计、生成命令、report / ledger 路径与使用说明。 |
| `README.md` | 本说明文件。 |

`workdir/` 解压目录被 `.gitignore` 忽略，只能作为本地临时检查目录；不要提交。

## 路径映射

`plantuml_recovery_report.json` 中的以下字段是 `workdir.zip` 内部 member path，而不是仓库中的散文件路径：

- `raw_candidate_path`
- `normalized_candidate_path`
- `raw_preflight.structured_export_path`
- `normalized_preflight.structured_export_path`

例如 report 里出现 `normalized_candidates/0001__...__normalized.puml` 时，应理解为：

```text
workdir.zip
└── normalized_candidates/0001__...__normalized.puml
```

## 复验方式

在仓库根目录执行：

```bash
cd project_1_llm_state_machine_modeling/paper_stm_repair/conversion/artifacts/plantuml_recovery/r3_1_committed
sha256sum -c workdir.zip.sha256
unzip -l workdir.zip | head
mkdir -p /tmp/r3_1_plantuml_recovery_workdir
unzip -q workdir.zip -d /tmp/r3_1_plantuml_recovery_workdir
find /tmp/r3_1_plantuml_recovery_workdir -maxdepth 2 -type f | head
```

重新生成 committed report 与 archive：

```bash
export PLANTUML_JAR=/abs/path/to/plantuml.jar
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_conversion.cli recover-plantuml \
  --run-id r3.1-plantuml-recovery-v0 \
  --created-at 2026-06-25T12:00:00+00:00
```

生成后可以删除解压态目录，只保留 `workdir.zip`、`workdir.zip.sha256`、`manifest.json` 与本 README：

```bash
rm -rf project_1_llm_state_machine_modeling/paper_stm_repair/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir
```

## 学术解释边界

- archive 只证明 R3.1 转换前规范化候选和官方 SCXML 导出可复验；它不是 Better STM repair 结果。
- 主 eligibility 只能引用同时满足 low-risk rule、官方 SCXML parse、source-level semantic preservation audit 通过的条目。
- `semantic_preservation_audit` 是 raw-vs-normalized PlantUML source signature 审计，不是形式化等价证明；论文写作时应称为“source-signature-preserving / 结构签名保持”，不要写成无条件严格语义等价。
