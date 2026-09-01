# R1 当前谓词来源审计

## 结论

截至 2026-09-01，冻结注册表的 19 个谓词都能回链到来源标识映射、主张支持和边界，但该映射不能单独支撑“19 个谓词已完成学术资格审查”的论文表述。旧目录缺少作者、年份、发表载体、DOI、稳定 URL、检索日期、全文定位与逐句核验字段，并且包含本地领域摘录和技术记录。

R1 的独立外部审阅将 8 个谓词标为“条件可写”，6 个标为 `TODO-CITATION`，5 个标为注册表语义与现有有界后端不完全同形。三种状态互相独立，逐条状态和禁止推论见[谓词来源审计](./predicate_provenance.md)。冻结来源标识目录尚未提供从其 `ST/TP/TR/BV` 标识到本审计 `D1--F7/T1--T2` 角色的完整可机读交叉映射，因此逐条角色仍是待复核的 citation audit，而非运行时元数据。这不改变已冻结的谓词标识、类型化约定、后端、W、D/A、关系、K/N/I 或结果数字。

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

本地 `STM.md` 摘录和方法或 FCSTM 技术制品仅标为“本地领域摘录”或“本地技术制品”。它们不能替代上表的外部学术引文。`TODO-CITATION` 的详细缺口是版本化 FCSTM 执行语义、G2/V3/V4/V5 的有界模型检查完备性、V1/V2 有限输入域的需求来源，以及 `called()` 的公开语义规范。
