# manual download queue

本文件不是正式 BibTeX 数据库，而是人工下载 PDF / artifact 的队列。每条给出候选原因、下载目标和 BibTeX 代码块。下载后必须补入对应 `papers/<slug>/` 目录，并更新 [candidate_matrix.md](./candidate_matrix.md)、[screening_ledger.md](./screening_ledger.md) 与 [SUMMARY.md](./SUMMARY.md)。R1.6 已能自动下载或本地已有的条目从 pending 队列移出；保留在本表中的都是仍需人工 / 机构访问或后续专项核验的对象。

| ID | 标题 | 需要人工下载的内容 | 来源 URL | 原因 | 状态 |
|---|---|---|---|---|---|
| automated-transition-use-cases-uml-sm | Automated Transition from Use Cases to UML State Machines to Support State-Based Testing | Springer PDF / artifact | https://doi.org/10.1007/978-3-642-21470-7_9 | 经典 use case -> UML SM 线索，需正式来源与全文。 | pending |
| execution-nl-req-bt-sm | Execution of Natural Language Requirements using State Machines Synthesised from Behavior Trees | JSS PDF / artifact | https://doi.org/10.1016/j.jss.2012.06.013 | NL->BT->SM 可能是 extended seed；需要正式 PDF 与 artifact。 | pending |
| maritaca-use-case-behavior-models | MARITACA: From Textual Use Case Descriptions to Behavior Models | IEEE PDF / artifact | https://doi.org/10.1109/DSN-W.2017.33 | classic textual use case -> behavior/state-machine extraction；metadata 强相关但无 OA artifact。 | pending |
| dependable-product-families-usecases-state-machines | Modeling Dependable Product-Families: From Use Cases to State Machine Models | IEEE PDF / artifact | https://doi.org/10.1109/LADC.2016.28 | restricted use cases -> state machine；需核 variability 是否可隔离。 | pending |
| statechart-use-case-validation-event-driven | Statechart-based use case requirement validation of event-driven systems | ACM PDF | https://doi.org/10.1145/2245276.2231947 | 题名相关但可能是 validation 而非 generation；需确认方向。 | pending |
| semi-auto-efsm-standard-docs | Semi-automatic Generation of Extended Finite State Machines from Natural Language Standard Documents | IEEE PDF / artifact | https://doi.org/10.1109/DSN-W.2015.17 | standard/protocol risk sentinel；需确认是否可作为控制标准例外。 | pending |
| rscharter-statechart-elements | Rscharter: A Framework for Extracting Statechart Diagram Elements from the Requirements Specification | SSRN PDF / possible artifact | https://doi.org/10.2139/ssrn.4964857 | requirements -> statechart elements 新线索；需全文确认是否完整 STM。 | pending |
| nl-standard-docs-state-machines | From Natural Language Standard Documents to State Machines: Advantages and Drawbacks | AIAA / publisher PDF | https://doi.org/10.2514/1.I010525 | 标准文档到状态机线索；需确认是否 protocol/standard extraction，应作为 sentinel。 | pending |
| requirements-analysis-prototyping-scenarios-statecharts | Requirements Analysis and Prototyping Using Scenarios and Statecharts | PDF / bibliographic metadata | 待定位 | 可能是 scenario/statechart co-evolution，需确认是否 co-exist only。 | pending / low priority |
| towards-automatic-model-completion | Towards Automatic Model Completion: from Requirements to SysML State Machines | arXiv/PDF or preprint if available | 待定位 | GWT / completion 近邻；需确认是否 partial model 输入。 | pending / low priority |
| most-states-modes | Modeling and Verification of Natural Language Requirements based on States and Modes | ACM TOSEM PDF | https://doi.org/10.1145/3640822 | states/modes formalization 线索；需确认是否输出 STM family。 | pending / related-work |

## 已处理 / 移出 pending 队列

| ID | 处理结论 | 移出原因 | 交叉引用 |
|---|---|---|---|
| completion-sysml-gwt | downloaded / excluded | 已有 PDF/全文并确认 `X_REPAIR_ONLY`，不再需要人工下载。 | [papers/completion-sysml-gwt/seed_desc.md](./papers/completion-sysml-gwt/seed_desc.md) |
| generating-statechart-designs-from-scenarios | excluded by metadata | DOI / metadata / classic knowledge 已足以确认主要输入为 sequence/scenario diagrams，`X_SEQUENCE_CLASS`；若未来要写 related work 可另行下载，但不阻塞 strict seed。 | [exclusion_ledger.md](./exclusion_ledger.md) |

## BibTeX / placeholder snippets

```bibtex
% NOT A REAL BIBTEX DATABASE — manual download queue for human operator.

@incollection{yue2011automatedtransitionusecasesstatemachines,
  title = {Automated Transition from Use Cases to UML State Machines to Support State-Based Testing},
  author = {Tao Yue and Shaukat Ali and Lionel Briand},
  booktitle = {Model Driven Engineering Languages and Systems},
  year = {2011},
  doi = {10.1007/978-3-642-21470-7_9},
  url = {https://doi.org/10.1007/978-3-642-21470-7_9}
}

@article{kim2012executionnlbtstatemachines,
  title = {Execution of natural language requirements using State Machines synthesised from Behavior Trees},
  author = {Soon-Kyeong Kim and Toby Myers and Marc-Florian Wendland and Peter A. Lindsay},
  journal = {Journal of Systems and Software},
  year = {2012},
  doi = {10.1016/j.jss.2012.06.013},
  url = {https://doi.org/10.1016/j.jss.2012.06.013}
}

@inproceedings{erazo2017maritaca,
  title = {MARITACA: From Textual Use Case Descriptions to Behavior Models},
  author = {Erazo, M. A. and others},
  booktitle = {2017 IEEE/IFIP International Conference on Dependable Systems and Networks Workshops (DSN-W)},
  year = {2017},
  doi = {10.1109/DSN-W.2017.33},
  url = {https://doi.org/10.1109/DSN-W.2017.33}
}

@inproceedings{erazo2016dependableproductfamilies,
  title = {Modeling Dependable Product-Families: From Use Cases to State Machine Models},
  booktitle = {2016 Latin-American Symposium on Dependable Computing (LADC)},
  year = {2016},
  doi = {10.1109/LADC.2016.28},
  url = {https://doi.org/10.1109/LADC.2016.28}
}

@inproceedings{statechartusecase2012validation,
  title = {Statechart-based use case requirement validation of event-driven systems},
  year = {2012},
  doi = {10.1145/2245276.2231947},
  url = {https://doi.org/10.1145/2245276.2231947}
}

@inproceedings{efsmstandarddocs2015,
  title = {Semi-automatic Generation of Extended Finite State Machines from Natural Language Standard Documents},
  year = {2015},
  doi = {10.1109/DSN-W.2015.17},
  url = {https://doi.org/10.1109/DSN-W.2015.17}
}

@article{greghi2018naturallanguagestandardstatemachines,
  title = {From Natural Language Standard Documents to State Machines: Advantages and Drawbacks},
  author = {Juliana Galvani Greghi and Eliane Martins and Ariadne M. B. R. Carvalho and Ana Maria Ambrosio},
  journal = {Journal of Aerospace Information Systems},
  year = {2018},
  doi = {10.2514/1.I010525},
  url = {https://doi.org/10.2514/1.I010525}
}

@misc{rscharter2024,
  title = {Rscharter: A Framework for Extracting Statechart Diagram Elements from the Requirements Specification},
  year = {2024},
  doi = {10.2139/ssrn.4964857},
  url = {https://doi.org/10.2139/ssrn.4964857}
}

@article{nakagawa2024statesmodes,
  title = {Modeling and Verification of Natural Language Requirements based on States and Modes},
  journal = {ACM Transactions on Software Engineering and Methodology},
  year = {2024},
  doi = {10.1145/3640822},
  url = {https://doi.org/10.1145/3640822}
}

% TODO: requirements-analysis-prototyping-scenarios-statecharts / towards-automatic-model-completion metadata 待正式来源核验后补齐。
```
