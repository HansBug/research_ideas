# conversion/artifacts

本目录用于保存 `paper_stm_issue_discover/conversion` 下需要长期复验、但文件数量过高的运行证据。这里不是根目录 `runs/`，也不承载 PR 进度信息；它只保存可复现实验 / 转换证据链中需要随代码一起审阅的稳定制品。

## 目录纪律

1. 高基数制品（成百上千个候选 `.puml`、官方 `.scxml` 等）必须压缩为少量 archive 文件提交，避免 PR diff 出现几千个散文件。
2. archive 必须配套 `manifest.json`、校验和文件和本地 `README.md`，说明生成命令、文件数量、路径映射和复验方式。
3. 解压后的 `workdir/` 只允许作为本地临时检查目录，不应提交进 Git。
4. report / summary / ledger 等便于 review 的小型文本证据仍放在 [../reports/](../reports/)。

## 当前制品

- [plantuml_recovery/r3_1_committed/README.md](./plantuml_recovery/r3_1_committed/README.md)：R3.1 PlantUML recovery 全量 raw / normalized candidate / official SCXML archive。
