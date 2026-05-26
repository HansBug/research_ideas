# 博士研究方向 SCI / EI / CCF 投稿名录全对照

> 服务对象：本仓库的博士研究主题
> **基于大语言模型（LLM）的控制系统状态机建模与验证方法**
>
> 数据基准：CCF 推荐目录第七版（2026 年 3 月发布）/ 中科院期刊分区表 2025 升级版 / JCR 2024 / EI Compendex 2025
> 编制日期：2026-05-26
> 维护原则：本表只覆盖与本研究**强相关**的 venue，不做全行业 catalog。

---

## 一、研究方向与领域映射

研究主题覆盖四大子任务，每个子任务有明显不同的最佳投稿目标：

| 子任务 | 关键词 | 最对口的学术圈 |
|---|---|---|
| 内容一：LLM 状态机结构化建模 | LLM4Modeling, NL2Model, MDE | 软件建模 (MoDELS/SoSyM)、需求工程 (RE/REFSQ)、软工综合 (ICSE/ASE/FSE) |
| 内容二：验证场景与性质生成 | property mining, scenario generation, LTL/CTL synthesis | 软工综合 (ICSE/ASE/FSE/ISSTA)、形式化方法 (FM)、需求 (RE) |
| 内容三：基于验证剖面的状态机验证 | model checking, timed automata, UPPAAL | 形式化验证 (CAV/FM/TACAS/VMCAI/SAS/ATVA/SPIN)、可靠性 (ISSRE/STVR) |
| 内容四：迭代式模型修复 | model repair, automated program repair (APR), LLM-based repair | 软工综合 A 类 (ICSE/FSE/ASE/ISSTA)、维护 (ICSME/SANER) |
| 横向：LLM 方法本身 | LLM, agent, RAG, fine-tuning | AI/NLP A 类 (NeurIPS/ICML/ICLR/ACL/AAAI) |
| 横向：控制系统与功能安全 | embedded, real-time, ISO 26262 | 嵌入式实时 (RTSS/EMSOFT)、工业安全期刊 |

## 二、相关性分级口径

为了便于快速判断投稿优先级，本文档使用统一 emoji 列：

| Emoji | 含义 |
|:-:|---|
| 🟢 | 极强相关：方法、对象、评测口径都贴本研究，**默认主战场** |
| 🟡 | 强相关：某个子任务对口或方法层面对口，**可作为分流目标** |
| 🟠 | 中等相关：边缘对口，适合**附带成果**（如控制系统案例、工业验证） |

CCF 字段格式：`E-A` = E 类（软件工程/系统软件/程序设计语言）A 类；其他领域代码：

- **A** = 人工智能
- **B** = 计算机体系结构/并行与分布计算/存储系统
- **E** = 软件工程/系统软件/程序设计语言
- **F** = 数据库/数据挖掘/内容检索
- **理论** = 计算机科学理论（CCF 第七版新增/独立标注）
- **T** = 交叉/综合/新兴

---

## 三、期刊总表

### 3.1 软件工程主线期刊（CCF E 类，🟢 主战场）

| 缩写 | 全称 | 出版商 | CCF | 中科院 | JCR | IF (2024) | EI | 相关性 | 主要对口子任务 |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| TSE | IEEE Transactions on Software Engineering | IEEE | E-A | 1 区 Top | Q1 | ~6.5 | ✓ | 🟢 | 一/二/三/四（综合软工顶刊） |
| TOSEM | ACM Transactions on Software Engineering and Methodology | ACM | E-A | 1 区 | Q1 | ~6.6 | ✓ | 🟢 | 一/二/四 |
| TOPLAS | ACM Transactions on Programming Languages and Systems | ACM | E-A | 1 区 | Q2 | ~1.6 | ✓ | 🟡 | 偏 PL，仅修复/分析相关可投 |
| TSC | IEEE Transactions on Services Computing | IEEE | E-A | 1 区 Top | Q1 | ~5.5 | ✓ | 🟠 | 服务计算方向偏弱，控制系统不直接对口 |
| EMSE | Empirical Software Engineering | Springer | E-B | 2 区 | Q1 | 4.1 | ✓ | 🟢 | 任何带"LLM + 实证 + benchmark"的工作 |
| ASE (Journal) | Automated Software Engineering | Springer | E-B | 2 区 | Q2 | ~2.5 | ✓ | 🟢 | 一/四，自动化是核心匹配点 |
| JSS | Journal of Systems and Software | Elsevier | E-B | 2 区 | Q1 | 4.1 | ✓ | 🟢 | 一/三，控制系统案例研究友好 |
| IST | Information and Software Technology | Elsevier | E-B | 2 区 | Q1 | ~3.9 | ✓ | 🟢 | 一/二，性价比高 |
| RE | Requirements Engineering | Springer | E-B | 3 区 | Q2 | ~3.0 | ✓ | 🟢 | 内容一直接对口（需求→模型） |
| SoSyM | Software and Systems Modeling | Springer | E-B | 3 区 | Q2 | ~2.4 | ✓ | 🟢 | 内容一直接对口（模型驱动工程） |
| STVR | Software Testing, Verification and Reliability | Wiley | E-B | 4 区 | Q3 | ~1.7 | ✓ | 🟢 | 内容二/三直接对口 |
| SCP | Science of Computer Programming | Elsevier | E-B | 4 区 | Q3 | ~1.5 | ✓ | 🟡 | 形式化/PL 方向相关 |
| JSEP | Journal of Software: Evolution and Process | Wiley | E-B | 4 区 | Q3 | ~1.7 | ✓ | 🟢 | 内容四直接对口（演化与过程） |
| SPE | Software: Practice and Experience | Wiley | E-B | 4 区 | Q3 | ~2.1 | ✓ | 🟡 | 偏工程实践，作为案例研究归属 |
| JFP | Journal of Functional Programming | Cambridge UP | E-B | 4 区 | Q3 | ~1.4 | ✓ | 🟠 | 几乎不对口（函数式 PL） |
| IET Software | IET Software | IET / Wiley | E-B | 4 区 | Q4 | ~1.5 | ✓ | 🟡 | 兜底 B 类期刊 |
| STTT | International Journal of Software Tools for Technology Transfer | Springer | E-C | 4 区 | Q3 | ~1.4 | ✓ | 🟢 | 工具化产物（pyfcstm）友好 |
| SQJ | Software Quality Journal | Springer | E-C | 4 区 | Q3 | ~1.7 | ✓ | 🟡 | 二/三相关 |
| JLAMP | Journal of Logical and Algebraic Methods in Programming | Elsevier | E-C | 4 区 | Q3 | ~0.9 | ✓ | 🟡 | 形式化逻辑相关 |
| IJSEKE | International Journal of Software Engineering and Knowledge Engineering | World Scientific | E-C | — | ESCI | — | ✓ | 🟡 | LLM+知识库相关 |
| SOCA | Service Oriented Computing and Applications | Springer | E-C | 4 区 | Q3 | ~2.0 | ✓ | 🟠 | 偏服务计算 |
| JWE | Journal of Web Engineering | River Publishers | E-C | — | ESCI | — | ✓ | 🟠 | 不对口 |
| TPLP | Theory and Practice of Logic Programming | Cambridge UP | E-C | 4 区 | Q3 | ~1.4 | ✓ | 🟠 | 逻辑编程，弱相关 |
| PACM PL | Proceedings of the ACM on Programming Languages | ACM | E-C | — | ESCI | — | ✓ | 🟡 | POPL/PLDI/OOPSLA 论文挂这本，实际按 A 看 |

### 3.2 AI / 机器学习期刊（CCF A 类人工智能，🟡 强相关）

LLM 方法部分的工作可以走 AI 通道：

| 缩写 | 全称 | 出版商 | CCF | 中科院 | JCR | IF (2024) | EI | 相关性 | 备注 |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| TPAMI | IEEE Trans. on Pattern Analysis and Machine Intelligence | IEEE | A-A | 1 区 Top | Q1 | ~20+ | ✓ | 🟠 | 偏 CV，文本/代码工作较少 |
| AIJ | Artificial Intelligence | Elsevier | A-A | 2 区 | Q1 | ~5.0 | ✓ | 🟡 | LLM+符号推理混合工作友好 |
| JMLR | Journal of Machine Learning Research | MIT Press | A-A | 3 区 | Q1 | ~4.0 | ✓ | 🟡 | 偏理论 |
| TKDE | IEEE Trans. on Knowledge and Data Engineering | IEEE | F-A | 2 区 Top | Q1 | ~8+ | ✓ | 🟠 | F 类，知识抽取相关可投 |
| TACL | Transactions of the ACL | MIT Press | A-B | 2 区 | Q1 | ~10+ | ✓ | 🟡 | NLP 期刊，LLM 工作走 NLP 路线时可选 |

### 3.3 嵌入式 / 实时 / EDA 期刊（CCF B 类，🟠 中等相关）

控制系统/工业案例相关的成果可以走这条线：

| 缩写 | 全称 | 出版商 | CCF | 中科院 | JCR | IF (2024) | EI | 相关性 | 备注 |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| TCAD | IEEE Trans. on Computer-Aided Design of Integrated Circuits and Systems | IEEE | B-A | 1 区 Top | Q1 | ~3.0 | ✓ | 🟠 | EDA/形式化交叉 |
| TECS | ACM Trans. on Embedded Computing Systems | ACM | B-B | 3 区 | Q3 | ~2.0 | ✓ | 🟠 | 嵌入式系统验证可投 |
| Real-Time Systems | Real-Time Systems | Springer | B-B | 3 区 | Q3 | ~1.7 | ✓ | 🟠 | 时间属性强相关时可投 |

### 3.4 国内中文期刊（CCF 计算领域高质量目录 T1/T2/T3，🟢/🟡 用于评审与中期）

国内博士盲审/中期评审一般认中文 T1，可与英文论文搭配使用：

| 缩写 | 全称 | 主办 | CCF | T 分级 (2025) | EI / SCI | 相关性 |
|---|---|---|:-:|:-:|:-:|:-:|
| 计算机学报 | 计算机学报 | 中国计算机学会 | E-A 国内一类 | T1 | EI ✓ | 🟢 |
| 软件学报 | 软件学报 | 中国科学院软件所 | E-A 国内一类 | T1 | EI ✓ | 🟢 |
| 计算机研究与发展 | 计算机研究与发展 | 中国科学院计算所 | E-A 国内一类 | T1 | EI ✓ | 🟢 |
| 中国科学：信息科学 | 中国科学：信息科学 | 中国科学院 | E-A 国内一类 | T1 | EI ✓ | 🟢 |
| 自动化学报 | 自动化学报 | 中国自动化学会 | — | T1（控制） | EI ✓ | 🟡 |
| 控制理论与应用 | 控制理论与应用 | 华南理工 / CAA | — | T2（控制） | EI ✓ | 🟡 |
| 电子学报 | 电子学报 | 中国电子学会 | — | T2 | EI ✓ | 🟡 |
| 计算机科学 | 计算机科学 | 重庆西南信息有限公司 | — | T2 | 核心 | 🟡 |
| Frontiers of Computer Science (FCS) | Frontiers of Computer Science | Springer / 高教社 | T-B | T2 | SCI Q3 / EI ✓ | 🟡 |
| Science China Information Sciences | Science China Information Sciences | Springer / 中国科学 | — | T1 英文版 | SCI Q1 / EI ✓ | 🟢 |

> 中文期刊推荐策略：内容一/二落在 **软件学报 / 计算机学报**；内容三可考虑 **计算机研究与发展**；控制案例可走 **自动化学报**。

---

## 四、会议总表

### 4.1 软件工程顶会（CCF E 类 A，🟢 主战场，全部 EI 收录）

| 缩写 | 全称 | 出版 | CCF | 相关性 | 主要对口子任务 |
|---|---|---|:-:|:-:|---|
| ICSE | International Conference on Software Engineering | IEEE/ACM | E-A | 🟢 | 一/二/三/四 全部子任务的最高目标 |
| FSE / ESEC-FSE | ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering | ACM | E-A | 🟢 | 同上 |
| ASE | International Conference on Automated Software Engineering | IEEE/ACM | E-A | 🟢 | 自动化建模/修复直接对口 |
| ISSTA | International Symposium on Software Testing and Analysis | ACM | E-A | 🟢 | 内容二/三/四（测试与分析） |
| OOPSLA | Conference on Object-Oriented Programming Systems, Languages, and Applications | ACM | E-A | 🟡 | 走 PACM PL，对口修复/分析 |
| POPL | ACM Symposium on Principles of Programming Languages | ACM | E-A | 🟡 | 形式化语义/逻辑相关 |
| PLDI | ACM Conference on Programming Language Design and Implementation | ACM | E-A | 🟡 | 程序分析对口 |
| FM | International Symposium on Formal Methods | Springer (FME) | E-A | 🟢 | 内容三主战场 |
| SOSP / OSDI | OS Symposia | ACM / USENIX | E-A | 🟠 | 不对口（系统层） |

### 4.2 软件工程 B 类会议（🟢/🟡 强相关，全部 EI 收录）

| 缩写 | 全称 | 出版 | CCF | 相关性 | 主要对口子任务 |
|---|---|---|:-:|:-:|---|
| MoDELS | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | ACM/IEEE | E-B | 🟢 | 内容一**核心对口** |
| RE | IEEE International Requirements Engineering Conference | IEEE | E-B | 🟢 | 内容一/二**核心对口** |
| SANER | IEEE Int. Conf. on Software Analysis, Evolution, and Reengineering | IEEE | E-B | 🟢 | 内容四对口 |
| ICSME | International Conference on Software Maintenance and Evolution | IEEE | E-B | 🟢 | 内容四对口 |
| ICPC | IEEE International Conference on Program Comprehension | IEEE/ACM | E-B | 🟡 | 程序理解 |
| ESEM | International Symposium on Empirical Software Engineering and Measurement | IEEE/ACM | E-B | 🟢 | LLM+实证评估对口 |
| ISSRE | IEEE International Symposium on Software Reliability Engineering | IEEE | E-B | 🟢 | 内容三对口（可靠性） |
| VMCAI | International Conference on Verification, Model Checking, and Abstract Interpretation | Springer | E-B | 🟢 | 内容三**核心对口** |
| SAS | International Static Analysis Symposium | Springer | E-B | 🟡 | 静态分析 |
| ETAPS (含 TACAS / FoSSaCS / ESOP) | European Joint Conferences on Theory and Practice of Software | Springer | E-B | 🟢 | TACAS 是验证领域顶会之一 |
| ECOOP | European Conference on Object-Oriented Programming | Dagstuhl | E-B | 🟡 | OO 相关 |
| CAiSE | International Conference on Advanced Information Systems Engineering | Springer | E-B | 🟡 | 信息系统建模 |
| ICFP | ACM Int. Conf. on Functional Programming | ACM | E-B | 🟠 | 函数式 PL |
| LCTES | ACM SIGPLAN/SIGBED Conf. on Languages, Compilers and Tools for Embedded Systems | ACM | E-B | 🟡 | 嵌入式 PL 相关 |
| CC | International Conference on Compiler Construction | ACM | E-B | 🟠 | 编译器 |
| CP | International Conference on Principles and Practice of Constraint Programming | Springer | E-B | 🟡 | 约束求解 |
| ICSOC | International Conference on Service Oriented Computing | Springer | E-B | 🟠 | 服务计算 |
| ICWS | IEEE International Conference on Web Services | IEEE | E-B | 🟠 | Web 服务 |
| Middleware | ACM/IFIP/USENIX International Middleware Conference | ACM/IFIP | E-B | 🟠 | 中间件 |
| HotOS | USENIX Workshop on Hot Topics in OS | USENIX | E-B | 🟠 | OS workshop |

### 4.3 形式化验证（CCF 理论类 / E 类 C，🟢 内容三主战场）

| 缩写 | 全称 | 出版 | CCF | 相关性 | 备注 |
|---|---|---|:-:|:-:|---|
| CAV | International Conference on Computer Aided Verification | Springer | 理论-A | 🟢 | **形式化验证全球顶会**，内容三最高目标 |
| LICS | ACM/IEEE Symposium on Logic in Computer Science | IEEE/ACM | 理论-A | 🟡 | 偏理论，时序逻辑相关 |
| TACAS | International Conference on Tools and Algorithms for the Construction and Analysis of Systems | Springer (ETAPS) | E-B（随 ETAPS） | 🟢 | TACAS Tool Paper 适合发布 pyfcstm |
| ICFEM | International Conference on Formal Engineering Methods | Springer | E-C | 🟢 | 工业向形式化方法，对口 |
| ATVA | International Symposium on Automated Technology for Verification and Analysis | Springer | E-C | 🟢 | 自动验证，对口内容三 |
| SPIN | International Symposium on Model Checking of Software | Springer | E-C | 🟢 | 软件模型检查，直接对口 |
| RV | International Conference on Runtime Verification | Springer | E-C | 🟡 | 运行时验证 |
| MEMOCODE | Int. Conf. on Formal Methods and Models for System Design | IEEE/ACM | E-C | 🟡 | 协同设计形式化 |
| LOPSTR | International Symposium on Logic-based Program Synthesis and Transformation | Springer | E-C | 🟡 | 程序合成 |
| ICECCS | International Conference on Engineering of Complex Computer Systems | IEEE | E-C | 🟡 | 复杂系统工程 |
| TASE | Theoretical Aspects of Software Engineering | IEEE | E-C | 🟡 | 国内主办，对口 |
| SCAM | IEEE Int. Working Conf. on Source Code Analysis and Manipulation | IEEE | E-C | 🟡 | 源码分析 |
| ICST | IEEE International Conference on Software Testing, Verification and Validation | IEEE | E-C | 🟢 | 测试验证 |
| MSR | Mining Software Repositories | IEEE/ACM | E-C | 🟡 | LLM4SE 实证常发 |
| QRS | International Conference on Software Quality, Reliability and Security | IEEE | E-C | 🟡 | 质量与可靠性 |
| REFSQ | Requirements Engineering: Foundation for Software Quality | Springer | E-C | 🟢 | 内容一/二对口 |
| EASE | International Conference on Evaluation and Assessment in Software Engineering | ACM | E-C | 🟢 | 实证类对口 |
| SEKE | International Conference on Software Engineering and Knowledge Engineering | KSI | E-C | 🟡 | 知识+软工，国内常投 |
| APSEC | Asia-Pacific Software Engineering Conference | IEEE | E-C | 🟡 | 区域性软工 |
| ICSR | International Conference on Software Reuse | Springer | E-C | 🟠 | 软件复用 |

### 4.4 AI / NLP / 机器学习顶会（CCF A 类人工智能，🟡 LLM 子工作的分流去处）

> ⚠️ **CCF 第七版重要变化**：IJCAI 从 A 类降为 B 类，COLM/TMLR 等新刊不在 CCF 推荐里。

| 缩写 | 全称 | 出版 | CCF | 相关性 | 备注 |
|---|---|---|:-:|:-:|---|
| NeurIPS | Conference on Neural Information Processing Systems | NeurIPS Foundation | A-A | 🟡 | LLM/Agent 工作主流目标 |
| ICML | International Conference on Machine Learning | PMLR | A-A | 🟡 | 同上 |
| ICLR | International Conference on Learning Representations | OpenReview | A-A | 🟡 | LLM 评估/微调相关常发 |
| AAAI | AAAI Conference on Artificial Intelligence | AAAI | A-A | 🟡 | AI 综合，LLM+符号融合常发 |
| ACL | Annual Meeting of the Association for Computational Linguistics | ACL | A-A | 🟡 | NLP 顶会，LLM4Code 常发 |
| IJCAI | International Joint Conference on Artificial Intelligence | IJCAI | **A-B**（第七版降级） | 🟡 | 注意已不是 A 类 |
| EMNLP | Conference on Empirical Methods in Natural Language Processing | ACL | A-B | 🟡 | LLM4Code 实证 |
| NAACL | Annual Conference of the North American Chapter of the ACL | ACL | A-B | 🟡 | 同上 |
| COLING | International Conference on Computational Linguistics | ACL/ICCL | A-B | 🟡 | 偏弱 |
| KDD | ACM Knowledge Discovery and Data Mining | ACM | F-A | 🟠 | 偏数据挖掘 |

### 4.5 嵌入式 / 实时 / EDA 会议（🟠 控制系统案例相关）

| 缩写 | 全称 | 出版 | CCF | 相关性 | 备注 |
|---|---|---|:-:|:-:|---|
| RTSS | IEEE Real-Time Systems Symposium | IEEE | T-A | 🟠 | 实时系统顶会，时间属性建模可投 |
| RTAS | IEEE Real-Time and Embedded Technology and Applications Symposium | IEEE | B-B | 🟠 | 实时与嵌入式 |
| EMSOFT | International Conference on Embedded Software | ACM/IEEE | T-B | 🟠 | 嵌入式软件，控制系统案例 |
| DAC | Design Automation Conference | ACM/IEEE | B-A | 🟠 | EDA 顶会，硬件味儿浓 |
| ICCAD | International Conference on Computer-Aided Design | IEEE/ACM | B-B | 🟠 | 同上 |
| DATE | Design Automation and Test in Europe | IEEE | B-B | 🟠 | 同上 |
| ISORC | IEEE Int. Symposium on Real-Time Distributed Computing | IEEE | E-C 邻近 | 🟠 | 实时分布式 |

---

## 五、按四大子课题的投稿决策矩阵

### 5.1 内容一：LLM 状态机结构化建模

| 档位 | 顶配（CCF-A） | 主推（CCF-B） | 兜底（CCF-C / 中文） |
|---|---|---|---|
| **会议** | ICSE / FSE / ASE | MoDELS（首推）/ RE / SANER / ICPC | REFSQ / TASE / APSEC / SEKE |
| **期刊** | TSE / TOSEM | **SoSyM（首推）/ RE / IST / JSS / EMSE** | 软件学报 / 计算机学报 / SQJ / STTT |
| **配套** | — | — | 自动化学报（控制系统案例分拆论文） |

### 5.2 内容二：验证场景与待验证性质生成

| 档位 | 顶配（CCF-A） | 主推（CCF-B） | 兜底（CCF-C / 中文） |
|---|---|---|---|
| **会议** | ICSE / FSE / ASE / ISSTA / FM | RE / ESEM / ISSRE / VMCAI | REFSQ / EASE / ICST / TASE |
| **期刊** | TSE / TOSEM | **STVR / JSS / IST / RE / EMSE** | 软件学报 / 计算机研究与发展 |

### 5.3 内容三：基于验证剖面的状态机验证

| 档位 | 顶配（CCF-A） | 主推（CCF-B） | 兜底（CCF-C / 中文） |
|---|---|---|---|
| **会议** | **CAV（首推）/ FM / ICSE / ASE / ISSTA** | **VMCAI / SAS / TACAS（随 ETAPS）/ ISSRE** | **ATVA / SPIN / ICFEM / RV / TASE** |
| **期刊** | TSE / TOSEM | **STVR（首推）/ JSS / SoSyM / SCP** | STTT / JLAMP / 软件学报 |
| **配套** | — | TCAD（嵌入式形式化交叉） | TECS / Real-Time Systems |

### 5.4 内容四：迭代式模型修复

| 档位 | 顶配（CCF-A） | 主推（CCF-B） | 兜底（CCF-C / 中文） |
|---|---|---|---|
| **会议** | **ICSE / FSE / ASE / ISSTA** | **SANER / ICSME / ESEM / VMCAI** | MSR / SCAM / QRS / TASE |
| **期刊** | **TSE / TOSEM** | **EMSE / JSEP（首推）/ JSS / IST** | SQJ / 软件学报 / 计算机学报 |

### 5.5 横向：LLM 方法学本身（如：多步建模框架、agent 设计、prompt 策略）

| 档位 | 推荐 |
|---|---|
| **AI 顶会** | NeurIPS / ICML / ICLR / AAAI / ACL（IJCAI 已降 B） |
| **AI 期刊** | AIJ / JMLR / TPAMI（CV 弱不优先） |
| **跨界 SE 顶刊** | TOSEM / TSE 的 "AI4SE" special issue |

---

## 六、毕业/盲审视角的优先级建议

按"博士毕业论文成果论"角度，结合 2027 春答辩窗口：

### 6.1 推荐组合 A（高目标·安全）

- 1 篇 CCF-A 会议（ICSE / FSE / ASE / ISSTA，任一）
- 1–2 篇 CCF-B 期刊（SoSyM / RE / EMSE / JSS / STVR）
- 1 篇国内 T1 中文期刊（软件学报 / 计算机学报）
- 1 篇工具/Artifact 论文（TACAS Tool Track 或 STTT）

### 6.2 推荐组合 B（中等目标·稳）

- 2–3 篇 CCF-B 期刊（覆盖 SoSyM / JSS / STVR / EMSE）
- 1 篇 CCF-B 会议（MoDELS / VMCAI / SANER）
- 1 篇国内 T1 中文期刊

### 6.3 推荐组合 C（兜底但合规）

- 3–4 篇 CCF-C 会议或期刊（ATVA / SPIN / ICFEM / TASE / STTT）
- 1 篇国内 T1 中文期刊

> 国内多数顶尖院校的博士盲审要求至少有 1 篇 CCF-B 及以上 SCI 期刊或 CCF-A 会议；本研究路线非常容易凑齐 B 类成果（SoSyM / RE / STVR / EMSE / JSS / IST 都很对口）。

---

## 七、可发表"工具/Artifact 论文"的特定渠道

pyfcstm（自研 DSL）以及未来的"LLM-生成-验证-修复"开源工具链可以单独发**工具/工件类论文**：

| 渠道 | 类型 | CCF | 备注 |
|---|---|:-:|---|
| ICSE Demonstrations Track | 工具 demo | E-A | 短文 |
| ICSE Software Engineering in Practice (SEIP) | 工业实践 | E-A | 与航天三院/17 所合作可走 |
| ASE Tool Demonstrations | 工具 demo | E-A | — |
| FSE Demonstrations | 工具 demo | E-A | — |
| TACAS Tool Paper / Tool Demo | 验证工具 | E-B（随 ETAPS） | 验证工具最对口 |
| CAV Artifact Evaluation | 工件评估 | 理论-A | 高质量必选 |
| STTT (Tool Paper) | 工具期刊 | E-C | 工具长文 |
| Empirical Software Engineering – Replication Package | 复现包 | E-B | 已收录论文配套 |

---

## 八、快速发表通道（投稿→见刊 ≤2 个月）

> **使用场景**：博士中期 / 盲审前补成果 / 工业合作产出快速落地 / 工具与小论文。
> **共同特征**：均为 OA 期刊；EI Compendex 收录稳定；SCIE 当前在册；审稿走"二元"或轻流程。
> **风险口径**：MDPI / Frontiers / IEEE Access 在 **2025 年中科院预警名单中已清零**，但部分单位仍有内部限制（如限篇数、不报销 APC、不计入科研绩效），投稿前**务必查所在单位最新政策**。

### 8.1 优先推荐（与本研究方向 🟢/🟡 对口）

| 期刊 | 出版社 | SCI | 中科院（2025） | JCR | IF | EI | CCF | 投→录中位 | 录→刊 | **总周期** | 相关性 | 适配子任务 |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| **Electronics** | MDPI | ✓ | 3 区 | Q2 | ~2.6 | ✓ | — | 30–45 天 | 2–5 天 | **~40–50 天** | 🟡 | 一/三（嵌入式/控制系统案例） |
| **Information** | MDPI | ✓ | 4 区 | Q3 | ~3.0 | ✓ | — | 25–40 天 | 2–5 天 | **~35–45 天** | 🟢 | 一/二（信息系统建模、LLM 应用） |
| **Computers** | MDPI | ✓ | 3 区 | Q1 | ~4.2 | ✓ | — | 30–45 天 | 2–5 天 | **~40–50 天** | 🟢 | 一/二/四（计算机综合） |
| **Algorithms** | MDPI | ✓ | 4 区 | Q3 | ~2.0 | ✓ | — | 25–40 天 | 2–5 天 | **~35–45 天** | 🟢 | 三/四（验证/修复算法） |
| **Mathematics** | MDPI | ✓ | 1 区（数学小类）/ 综合 3 区 | Q1 | ~2.4 | ✓ | — | 20–35 天 | 2–5 天 | **~30–40 天** | 🟡 | 三（形式化逻辑/时序逻辑/算法证明） |
| **Symmetry** | MDPI | ✓ | 3 区 | Q2 | ~2.2 | ✓ | — | 25–40 天 | 2–5 天 | **~30–45 天** | 🟡 | 收稿范围宽，状态机/约束类可投 |
| **Applied Sciences** | MDPI | ✓ | 3 区 | Q2 | ~2.5 | ✓ | — | 30–45 天 | 2–5 天 | **~40–50 天** | 🟡 | 工业案例研究（航天三院/17 所对口） |
| **Sensors** | MDPI | ✓ | 3 区 | Q2 | ~3.5 | ✓ | — | 25–40 天 | 2–5 天 | **~30–45 天** | 🟠 | 仅嵌入式/传感器场景可投 |
| **Future Internet** | MDPI | ✓ | 4 区 | Q3 | ~2.5 | ✓ | — | 25–40 天 | 2–5 天 | **~30–45 天** | 🟠 | 偏网络/Web，弱对口 |
| **MAKE** (Machine Learning and Knowledge Extraction) | MDPI | ✓ | 4 区 | Q3 | ~4.0 | ✓ | — | 30–45 天 | 2–5 天 | **~40–55 天** | 🟡 | 横向：LLM 方法/知识抽取 |

> 📌 MDPI 共同特征：录用即在线发表，无所谓"卷期排队"；版面费 APC ≈ ¥9k–¥18k；80% 录用率（高于学界平均）；二审重图表与代码可复现性。

### 8.2 可备选（非 MDPI 系，速度略慢但口碑更稳）

| 期刊 | 出版社 | SCI | 中科院（2025） | JCR | IF | EI | CCF | 投→刊总周期 | 相关性 | 备注 |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| **IEEE Access** | IEEE | ✓ | 4 区（已降级） | Q2 | ~3.6 | ✓ | — | **4–6 周** | 🟡 | 二元审稿，21 天可录。曾入预警，2025 已出。IEEE 名头国内多数认 |
| **SoftwareX** | Elsevier | ✓ | 4 区 | Q3 | ~2.4 | ✓ | — | 2–4 个月 | 🟢 | **专门发软件工具论文**，pyfcstm / LLM 工具链非常对口；不止于"快"，更是合适 |
| **Heliyon** | Elsevier (Cell Press) | ✓ | 3 区（On Hold） | Q2 | ~3.4 | ✓ | — | 1.5–3 个月 | 🟠 | 综合刊，On Hold 状态，慎投 |
| **PeerJ Computer Science** | PeerJ | ✓ | 4 区（小类 3 区） | Q2 | ~2.5 | ✓ | — | 3–5 个月 | 🟡 | 速度偏慢但口碑较好，强制开放数据/代码 |
| **Frontiers in Computer Science** | Frontiers | ESCI | — | — | ~2.0 | ✓ | — | 2–3 个月 | 🟡 | ESCI 不是 SCI，国内部分单位不算 |

### 8.3 与本研究方向的"快速通道 + 子任务"映射

| 子任务 | 首选快刊 | 备选 | 理由 |
|---|---|---|---|
| 内容一：LLM 状态机建模 | **Computers** / **Information** | Applied Sciences、Electronics | 收"LLM + 软件建模"类工作较友好；计算机综合刊范围广 |
| 内容二：验证场景/性质生成 | **Computers** / **Algorithms** | Mathematics（偏理论时） | 算法刊对"性质生成算法"接受度高 |
| 内容三：基于剖面的验证 | **Mathematics** / **Algorithms** | Electronics（嵌入式向） | 形式化/时序逻辑/时间自动机对口数学/算法刊 |
| 内容四：迭代修复 | **Computers** / **Algorithms** | Information | 修复算法/LLM4APR 工作对口 |
| 工具论文（pyfcstm 等） | **SoftwareX** | Computers | SoftwareX 是软件工具类论文的最佳归属，虽然不在 ≤2 个月范围 |
| LLM 方法学小论文 | **MAKE** / **Information** | Mathematics | 横向 LLM/RAG 小工作的快速出口 |

### 8.4 ≤2 个月投稿的实操要点

1. **投稿时间窗**：MDPI 录用→见刊一般 3–7 天，但避开**圣诞/春节/暑假**编辑部档期，平均会延后 1–2 周。
2. **首轮决定加速**：在 cover letter 里明确指出"已自查 figures / data 可复现 / code 已上传 anonymous repo"，可缩短 reviewer 选派时间。
3. **避免大修陷阱**：MDPI 的 "minor revision" 大多 7 天内必须回复，超时即重投；预留好时间。
4. **APC 报销前置确认**：你单位是否报销 MDPI？是否需要发票抬头特定？APC 一般 1900–2400 CHF，建议**先和导师确认资金来源**再投。
5. **Special Issue 优先**：MDPI 每个期刊都有大量 SI（Special Issue），SI 的 reviewer 池经常更窄、决定更快，但需先和 SI 编辑联系确认 scope 匹配。
6. **不重复一稿多投**：MDPI 跨刊共享投稿历史，被 Electronics 拒稿后改投 Sensors 编辑可见。
7. **预警动态**：投稿日和录用日两个时点都查 https://earlywarning.fenqubiao.com/ ，若投稿后该刊新入预警，应在 cover letter 中保留底稿证明。

### 8.5 不推荐 / 慎选清单

| 期刊 | 不推荐原因 |
|---|---|
| Wireless Personal Communications | **2025 中科院预警**（论文工厂） |
| Computers & Electrical Engineering | **2025 中科院预警**（论文工厂） |
| Scalable Computing-Practice and Experience | **2025 中科院预警**（论文工厂） |
| Multimedia Tools and Applications | 历史预警，争议大 |
| Soft Computing | 历史预警，谨慎 |
| Cluster Computing | 偏弱 |
| 任何"承诺一周录用"的非主流期刊 | 掠夺性嫌疑 |

---

## 九、注意事项与避坑

| 项 | 说明 |
|---|---|
| **中科院分区 2026 后停更** | 论文里若需写"中科院分区"应注明数据年份，2027 年后此评价体系会逐渐被 CCF + JCR + T1/T2/T3 替代 |
| **国际期刊预警** | 投稿前必查 https://earlywarning.fenqubiao.com/ ；当前列表里 IT 领域有几本 OA 期刊被列入观察名单 |
| **AAAI/NeurIPS/ICML 的盲审** | 这些 AI 会议要求严格双盲，pre-print（arXiv）必须在投稿前一定时间外提交，且匿名 |
| **CCF 升降级风险** | 第七版 IJCAI 已从 A 降到 B；若投稿周期长，注意论文录用时所使用的目录版本 |
| **EI 收录确认** | 会议名义上 EI 收录但实际某届可能未被收录，需查具体年份的 EI Compendex 检索；尤其是中文核心+EI 期刊 |
| **CCF 之外的高质量 venue** | COLM、TMLR、PACMSE（PACM on Software Engineering）等不在 CCF 推荐里但学界认可度极高；国内评审通常不予承认，谨慎选择 |
| **PACMSE 新动向** | ACM 已宣布 ICSE/FSE/ISSTA 的成果将逐渐改通过 PACMSE 期刊发表（类似 PACM PL），CCF 暂未跟进，需观察 |
| **盲审材料一致性** | 博士盲审时，材料里"已发表/录用论文"应标注 CCF 等级与索引类型，不一致会扣分 |

---

## 十、官方数据出处

| 来源 | 链接 |
|---|---|
| CCF 推荐目录官方专页（E 类） | https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/ |
| CCF 总目录入口 | https://www.ccf.org.cn/Academic_Evaluation/By_category/ |
| CCF 第七版在线版（2026） | https://ccf.atom.im/ |
| CCF 计算领域高质量科技期刊分级目录 | https://www.ccf.org.cn/ccftjgjxskwml/ |
| 中科院期刊分区表 | https://www.fenqubiao.com/ |
| 国际期刊预警名单 | https://earlywarning.fenqubiao.com/ |
| LetPub（中科院/JCR/IF 综合查询） | https://www.letpub.com.cn/ |
| EI Compendex 官方源刊列表 | https://www.elsevier.com/products/engineering-village/databases/compendex |
| ShowJCR 离线查询工具 | https://github.com/hitfyd/ShowJCR |
| Call4Papers CCF 列表（按领域查会议 deadline） | https://www.call4papers.cn/ccf/ccf-1.html |

---

## 十一、维护说明

1. 本文档随 CCF 推荐目录、中科院分区、JCR IF 更新而调整。
2. 若有新发现的 venue（如 PACMSE 进入 CCF）或子任务发生 pivot，应及时在第三/四/五节追加并打上 emoji 列。
3. emoji 列只放一个 emoji，不要在表格里再附中文释义（口径见第二节）。
4. 与 [TARGET.md](./TARGET.md) 中"研究目标"配合阅读；若研究内容发生重大调整，本文档第五节"决策矩阵"应同步更新。

**最后更新**：2026-05-26
