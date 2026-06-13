# manual download queue

本文件不是正式 BibTeX 数据库，而是人工下载 PDF / artifact 的队列。每条给出候选原因、下载目标和 BibTeX 代码块。下载后必须补入对应 `papers/<slug>/` 目录，并更新 [candidate_matrix.md](./candidate_matrix.md)、[screening_ledger.md](./screening_ledger.md) 与 [SUMMARY.md](./SUMMARY.md)。

| ID | 标题 | 需要人工下载的内容 | 来源 URL | 原因 | 状态 |
|---|---|---|---|---|---|
| completion-sysml-gwt | Completion of SysML state machines from Given-When-Then requirements | publisher PDF / supplementary / artifact | https://doi.org/10.1007/s10270-024-01228-3 | 需确认是否 completion-only、是否有 partial model 输入；Springer PDF / artifact 可能需人工访问。 | pending |
| automated-transition-use-cases-uml-sm | Automated Transition from Use Cases to UML State Machines to Support State-Based Testing | PDF / DOI / artifact | ResearchGate / publisher 待定位 | 经典 use case -> UML SM 线索，需正式来源与全文。 | pending |
| generating-statechart-designs-from-scenarios | Generating Statechart Designs from Scenarios | ACM PDF | https://doi.org/10.1145/337180.337217 | 需要确认输入是否自然语言 scenario，还是 sequence diagram / MSC。 | pending |
| execution-nl-req-bt-sm | Execution of Natural Language Requirements using State Machines Synthesised from Behavior Trees | PDF / artifact | ResearchGate 线索 | NL->BT->SM 可能是 extended seed；需要正式 PDF 与 artifact。 | pending |
| requirements-analysis-prototyping-scenarios-statecharts | Requirements Analysis and Prototyping Using Scenarios and Statecharts | PDF / bibliographic metadata | 待定位 | 可能是 scenario/statechart co-evolution，需确认是否 co-exist only。 | pending |
| nl-standard-docs-state-machines | From Natural Language Standard Documents to State Machines | AIAA / publisher PDF | https://arc.aiaa.org/doi/10.2514/1.I010525 | 标准文档到状态机线索；需确认是否 protocol/standard extraction，应作为 sentinel。 | pending |

## BibTeX / placeholder snippets

```bibtex
% NOT A REAL BIBTEX DATABASE — manual download queue for human operator.

@article{debiase2024sysmlgwt,
  title = {Completion of SysML state machines from Given-When-Then requirements},
  author = {Maria Stella de Biase and Simona Bernardi and Stefano Marrone and José Merseguer and Angelo Palladino},
  journal = {Software and Systems Modeling},
  year = {2024},
  doi = {10.1007/s10270-024-01228-3},
  url = {https://doi.org/10.1007/s10270-024-01228-3}
}

@inproceedings{whittle2000generatingstatecharts,
  title = {Generating statechart designs from scenarios},
  author = {Jon Whittle and Johann Schumann},
  booktitle = {Proceedings of the 22nd International Conference on Software Engineering},
  year = {2000},
  doi = {10.1145/337180.337217},
  url = {https://doi.org/10.1145/337180.337217}
}
```
