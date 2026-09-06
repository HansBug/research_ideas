# artifacts: pushing-generative-envelope-mbse

## Artifact 结论

| 项 | 当前状态 | 结论 |
|---|---|---|
| PDF | present | 本地 `paper.pdf` 已从 baseline 目录复制；ACL Anthology / DOI 是稳定论文入口。 |
| paper_content.txt | present | 本地 `paper_content.txt` 已存在，可支撑任务、模型、prompt 技术和实验设置核验。 |
| BibTeX | present | 本地 `bibtex.bib` 指向 RANLP 2025 / DOI `10.26615/978-954-452-098-4-137`。 |
| Code | not found | 源 [`ASSETS.md`](../../../../baselines/pushing-the-generative-envelope-mbse-artifacts/ASSETS.md) 未发现 paper-specific GitHub / supplementary / OSF / Zenodo / code。 |
| Data / benchmark | paper-only | 仅论文中记录 air purifier 与 vacuum 两个题项；无独立下载页、split 或机器可读 benchmark 包。 |
| Generated `<NL, STM>` outputs | not available as package | 论文报告 state machine diagram 生成实验与指标，但无逐次 raw outputs / generated diagrams bundle。 |
| 引用 / 来源说明 | citation note | 论文可引用；核心缺口是实验数据和输出未形成一手 artifact，许可 / 再分发不作为额外升绿阻塞。 |
| Conversion readiness | manual reconstruction only | 若后续使用，需要人工从论文中转写题项 / 生成流程 / 输出线索，并另记 reconstruction provenance。 |

## 已核 artifact 指针

| 类型 | URL / 路径 | 稳定性判断 |
|---|---|---|
| ACL Anthology | <https://aclanthology.org/2025.ranlp-1.137/> | 稳定论文页；未发现 supplementary。 |
| DOI | <https://doi.org/10.26615/978-954-452-098-4-137> | 稳定论文 DOI。 |
| 源目录资源账本 | [`ASSETS.md`](../../../../baselines/pushing-the-generative-envelope-mbse-artifacts/ASSETS.md) | 本次 code/data/output/license 判断的主要本地证据源。 |
| 源目录分析 | [`DESC.md`](../../../../baselines/pushing-the-generative-envelope-mbse-artifacts/DESC.md) | 本次输入/输出/方法/模型信息判断的主要本地整理源。 |

## 当前 artifact grade

`SA-3`：论文与元数据完整，任务关系清楚，但缺少可冻结的原装 `<NL, STM>` 样本包、源码和 prompt/output 结果包。适合作为 seed 方法证据与 related work，不适合作为当前 PR-R2 主四例样本。
