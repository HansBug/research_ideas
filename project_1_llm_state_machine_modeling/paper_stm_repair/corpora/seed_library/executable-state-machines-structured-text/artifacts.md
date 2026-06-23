# artifacts: executable-state-machines-structured-text

## 本地制品

| 项 | 状态 | size | sha256 |
|---|---:|---:|---|
| `paper.pdf` | present | 799268 bytes | `94b98b861ff9bd176ef666816400659cb430eefa462ec23c7d3d8d0b83ea1838` |
| `paper_content.txt` | present | 35840 bytes | `c1a68658323f2215223830c52e4fb1f015abf7f5e4253b9cd913bda98ff1b794` |
| `bibtex.bib` | present | 417 bytes | `e9563ef95aec5c7fcd6dc317f2f61ba3fc53aa91370a781221703870db3ee9d6` |

## 来源与稳定性

| 项 | 结论 |
|---|---|
| DOI / URL | `https://doi.org/10.5220/0007236601930200` |
| venue | MODELSWARD 2019。 |
| publisher / official page | DOI 指向 SCITEPRESS 论文入口；本轮只使用本地 BibTeX / 全文 / PDF / 源 `DESC.md`。 |
| source `ASSETS.md` | absent：源目录未发现 `ASSETS.md`。 |
| URL 稳定性 | DOI URL 稳定；未发现 artifact DOI、Zenodo、GitHub release、commit 或长期数据集入口。 |
| 引用 / 来源说明 | 论文可作为公开学术来源引用；缺口是没有代码、数据或模型 artifact 一手包与版本/hash，许可 / 再分发不作为额外升绿阻塞。 |

## 可复现实验制品

| 项 | 结论 |
|---|---|
| Code / repository | absent in local materials；源 `DESC.md` 也记录“原文未提供公开代码/仓库获取链接”。 |
| Dataset | absent as downloadable artifact；论文称 AOLC 是 publicly available requirements/tests 案例，但本地材料没有给出 URL、ReqIF、SPS 文件或测试规格包。 |
| Machine-readable STM | absent；未发现 eTrice model、Design Cockpit 43 工程、XML/XMI、state-machine source、transition table 或 GUI 工程。 |
| Raw outputs | absent；仅有论文 Table 1 / Table 2 的规模与测试步统计，没有逐测试 raw trace。 |
| Conversion readiness | `manual_only`: 可从正文与图示人工转写若干示例，但不能作为自动 ingest 的 R2 artifact。 |

## artifact 判定

- artifact_usability: `SA-3`
- R2 status: `not_main_seed`; `related_work_or_manual_reconstruction_only`
- 主要阻塞: 无公开代码、无机器可读数据/模型、无完整测试用例、无 artifact hash/commit/release。许可 / 再分发不作为额外升绿阻塞。
- 可保留价值: 方法链和案例统计可支撑 related work、baseline taxonomy 与 structured-requirements-to-FSM 对照。
