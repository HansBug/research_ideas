# R1 当前谓词来源审计

## 结论

截至 2026-09-02，R1 已把冻结 registry 的 source-ID pool、legacy 19、typed obligation surface 和当前四族 19 条逐项交叉映射。完整书目、全文原句、页码、责任分层、chronology、backend fragment 和逐 polarity 发表资格只见[谓词来源审计](./predicate_provenance.md)；本文件不复制第二份来源表。

冻结 registry 的标识映射是设计注册事实，而不是 runtime academic gate。R1 的结构化 audit metadata 明确将外部学术资格、方法自有执行语义和实例 authority 分开，且不改变冻结谓词、类型化约定、后端、W、D/A、relation、K/N/I 或结果数字。G2、V4 与 V5 的论文解释收窄为 publication boundary，不反写 canonical runtime record；V3 的 provider-free soundness gate 只将 `steps` 视为可执行单位，以与 native backend 一致。

## 来源与全文状态

| 标识 | 外部来源 | 核验状态与可用范围 |
| --- | --- | --- |
| D1 | Busard 等，[Verification of Railway Interlocking Systems](https://arxiv.org/pdf/1506.03554)，DOI [`10.4204/EPTCS.184.2`](https://doi.org/10.4204/EPTCS.184.2) | 全文核验；只作领域动机。 |
| F1 | [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) | 全文核验；状态、迁移、触发器、守卫、效果与生命周期槽位的元模型语义。 |
| F2 | [W3C SCXML 1.0](https://www.w3.org/TR/scxml/) | 全文核验；事件、宏步和单条执行轨迹的邻近形式语义。不能替代 FCSTM 语义证据。 |
| F3 | Heimdahl 与 Leveson，[Completeness and Consistency in Hierarchical State-Based Requirements](http://dslab.konkuk.ac.kr/Class/2012/12SIonSE/Key%20Papers/Completeness%20and%20consistency%20in%20hierarchical%20state-based%20requirements.pdf)，DOI [`10.1109/32.508311`](https://doi.org/10.1109/32.508311) | 全文核验；守卫完备性和一致性命题。UML 不将守卫互斥设为默认义务。 |
| F4 | Dwyer、Avrunin、Corbett，[Patterns in Property Specifications for Finite-State Verification](https://www.cs.colostate.edu/~france/CS614/Readings/Readings2011/PropPatterns2p411-dwyer.pdf)，DOI [`10.1145/302405.302672`](https://doi.org/10.1145/302405.302672) | 全文核验；有限状态性质模式。不能把无界模式自动改写成本文的有限界。 |
| F5 | [UPPAAL symbolic-query semantics](https://docs.uppaal.org/language-reference/query-semantics/symb_queries/) | 全文核验；区分 `E<>`、`A<>`、`A[]` 及完整状态中的位置和赋值。用于限制 G2、V4、V5。 |
| F6 | Fabian，[On Object Oriented Nondeterministic Supervisory Control](https://research.chalmers.se/publication/1126/file/1126_Fulltext.pdf) | 全文核验；G4 的共可达和非阻塞读法。 |
| F7 | Biere 等，[Linear Encodings of Bounded LTL Model Checking](https://lmcs.episciences.org/2236/pdf)，DOI [`10.2168/LMCS-2(5:5)2006`](https://doi.org/10.2168/LMCS-2%285%3A5%292006) | 全文核验；有界模型检查的界限与完整性条件。 |
| T1 | [SMT-LIB standard](https://smt-lib.org/standard.shtml) | 全文核验；有限输入域的 SMT 技术边界。 |
| T2 | [UPPAAL query semantics](https://docs.uppaal.org/language-reference/query-semantics/symb_queries/) | 全文核验；模型查询及状态空间回执的技术边界。 |

本地 `STM.md` 摘录和方法或 FCSTM 技术制品只能补充领域实例或执行语义，不能替代外部学术引文。FCSTM token/AST、`macrostep`、`called()`、hot start、projection、horizon 与 replay 由版本化方法规范、代码和测试承担；实例 finite domain、bound、scope 与 expected value 由逐 pair NL/source binding 承担，不能由 SMT-LIB 或后端能力反推。
