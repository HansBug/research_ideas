# artifacts: from-use-cases-to-statecharts

## 本地制品

| 项 | 状态 | size | sha256 |
|---|---:|---:|---|
| `paper.pdf` | present | 438324 bytes | `0794a9144a415170e5a4a445cdaebadce928fe8a2762ec90552a671bc476afed` |
| `paper_content.txt` | present | 45298 bytes | `899d69a03000a70a3951e9a48efcdc1228dd141fda83ab5dbc7ee375c5210c0d` |
| `bibtex.bib` | present | 388 bytes | `d6bde70e371875639c51b8ff4506b2ad29f598ea79cb8b5a63f6a566c3e5bf30` |

## 来源与稳定性

| 项 | 结论 |
|---|---|
| BibTeX URL | `https://pdfs.semanticscholar.org/51a5/02f94e69a794ac0dcc10802a86b9dcb80523.pdf` |
| DOI | BibTeX 与正文未提供。 |
| venue | Journal of Computing and Information Technology, 12(3), 223-235, 2004。 |
| publisher / official page | 本地材料未提供可核验官方页面。 |
| URL 稳定性 | Semantic Scholar PDF URL 可作为发现/备份线索；不是 publisher DOI 级稳定入口。 |
| license / redistribution | 未发现 license 或 artifact license 声明；只能记录本地研究副本，不能推断再分发许可。 |

## 可复现实验制品

| 项 | 结论 |
|---|---|
| Code / repository | absent in paper and local baseline; no GitHub/Zenodo/supplementary pointer in local materials. |
| Dataset | absent;论文使用 elevator request 说明性案例，不提供独立 benchmark。 |
| Machine-readable STM | absent; statecharts/GBS/object model 仅以 Fig. 5-8 和正文叙述出现。 |
| Raw outputs | absent;无实验输出包、XMI、XML 或 model-checking traces。 |
| R2 conversion readiness | `manual_only`: 可从 Fig. 2 与 Fig. 7 人工转写 use case/statechart pair，但需要人工 trace timing constraints、guards、events 和 added operations。 |

## artifact 判定

- artifact_usability: `SA-3`
- 排除码: `NO_CODE_OR_MACHINE_READABLE_ARTIFACT`; `PAPER_ONLY_CASE_STUDY`; `LICENSE_UNKNOWN`
- blocker: 无公开机器可读 artifact、无 license、无 DOI/publisher 稳定入口。
- pending: 若后续要进入可复现 benchmark，需要补人工转写模型、转写校验记录和可引用的授权/来源说明。
