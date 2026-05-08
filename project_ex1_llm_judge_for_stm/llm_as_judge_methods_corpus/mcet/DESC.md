# MCeT — DESC

## 1. 论文元信息

- **标题**：MCeT: Behavioral Model Correctness Evaluation using Large Language Models
- **作者**：Khaled Ahmed, Jialing Song, Boqi Chen, Ou Wei, Bingzhou Zheng
- **单位**：Huawei Research Canada + McGill University
- **年份 / Venue**：arXiv 2025（IEEE Conference / Xplore id 11245361 也已发表）
- **arXiv / URL**：https://arxiv.org/abs/2508.00630
- **代码**：https://github.com/Huawei-TTE/MCeT
- **阅读状态**：Skim（已读 abstract + intro + method 概述）
- **fingerprint**：**首个 LLM-as-Judge for behavioral model**（sequence diagrams）；提出"原子化 + 多视角 + 跨视角自一致性"三件套；与 STM artifact 最接近的同类工作

## 2. 一句话定位

> 把 sequence diagram 与 NL requirements 各自**拆成原子单元**，让 LLM 多视角对比并通过 self-consistency 跨视角校验，找出 sequence diagram 的正确性问题；是**SE behavioral model 域的 LLM-as-Judge 首作**。

## 3. 评判对象（Judging Object）

- **类型**：UML sequence diagram（behavioral model 的一种）
- **典型 task**：requirement → sequence diagram 的工件流；判 LLM 或 engineer 设计的 SD 与 requirements 的语义一致性
- **与 STM artifact 的相似度**：✅ **highest in corpus** — sequence diagram 与 state machine 同属 UML behavioral models，都是 graph-like 结构化制品；MCeT 的 "atomic + multi-perspective + self-consistency" 思路可以最直接借鉴到 STM judge

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) NL requirements text；(2) Sequence diagram（PlantUML 文本形式）；(3) （子任务）一个 atomic interaction（diagram 的一行）或一个 atomic requirement（split 后单条）|
| **输出** | (a) Direct check：Is the diagram correct vs requirements? Issues list；(b) Atomic-decomposed checks：每对 (atomic_diagram, atomic_requirement) 是否一致；(c) Cross-perspective consistency：多视角 vote / cross-check 后的最终 issue list（带消除 hallucination 后的 6 个 new issues per diagram） |

I/O schema：(req text + diagram) → multi-perspective LLM check → consolidated issue list。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | **Pure prompting**（无 fine-tune） |
| **rubric anchor** | partial — atomic decomposition + perspective list 是 method 内置 schema，可看作 implicit rubric |
| **CoT** | ✓ — 多视角逐步检查 + cross-check |
| **聚合** | ✓ — **multi-perspective + cross-check self-consistency**（与 Self-Consistency 相似但作用对象不是 reasoning chain 而是 perspective views） |
| **Calibration** | partial — cross-check 是为了消除 hallucination 引入的 false positive |
| **Bias correction** | ✓ — direct check precision 0.58 → 0.81 是消偏的实证 |

## 6. 评估方式

- **human reviewer**：是 — 由 experienced engineers 标注 reference issues
- **metric**：precision / recall against engineer-found issues + new issue discovery rate
- **inter-rater agreement**：未显式 $\kappa$，但报告 engineer-found issues 与 LLM-found issues 的对照表

## 7. 报告的 effect size + noise

- 直接检查 → 多视角 + 自一致性：precision 0.58 → 0.81（**+23pp**，相对提升 ~40%）
- 找出比 direct approach 多 90% 的 engineer-found issues
- 平均每个 diagram 发现 6 个 engineer 之前没发现的新 issue
- **是否多 seed**：✗
- **是否有 noise floor 讨论**：✗

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ 单次实验，未报告 LLM judge 的 stochasticity |
| **L2 Provider drift** | ✗ 不讨论；实验仅用 GPT-4-class 模型 |
| **L3 Rubric anchor** | partial — atomic + perspective 是 implicit rubric，但维度划分（completeness / correctness / standards）来自论文作者，未与 UML/SysML 社区广泛 review 维度对齐 |
| **L4 SE artifact 类型** | ✅ **同领域** — sequence diagram 与 state machine 都是 UML behavioral model；这恰恰是我们最接近的对照工作 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Atomic decomposition** 思路：把大 artifact 拆成 atomic units 再逐对比对，可借鉴到 STM judge 中——把 STM 拆成 atomic transitions 再与 atomic requirements 对照（已经在我们的 7 维 rubric 中部分体现）
- **Multi-perspective + cross-check self-consistency**：是对 LLM hallucination 的消偏机制，与我们 strict-llm + 多次 rep 取分布的纪律互补
- **Sequence diagram 与 STM 同源**：MCeT 的成功直接证明 LLM-as-Judge 可在 UML behavioral model 上达到工业可用的 precision；为我们的 STM judge 路线提供了**直接的可行性证据**

### 9.2 不借鉴

- 单 seed 实验：我们已 5-rep
- 仅 GPT-4 单 provider：我们要做 multi-provider drift 量化

### 9.3 对比 baseline

paper §Related Work 引用方式（拟稿）：

> "Ahmed et al. [Ahmed25] proposed MCeT, an atomic-decomposition + multi-perspective + cross-check LLM-as-Judge for sequence diagrams that improves precision from 0.58 to 0.81 over a direct-check baseline. **MCeT is the closest sibling work to ours in scope**: both target UML behavioral models (sequence diagram vs. state machine) and both are prompting-only LLM judges. Our work differs in three respects: (a) we target state machines, which add transition guards / temporal semantics absent from sequence diagrams; (b) we explicitly characterize evaluator stochasticity via a 5-replication noise-floor protocol that MCeT does not address; (c) we anchor our rubric in 7 dimensions distilled from prior STM expert-review practice rather than the atomic + perspective decomposition MCeT uses."

## 10. 引用导出

```bibtex
@article{ahmed2025mcet,
  title={MCeT: Behavioral Model Correctness Evaluation using Large Language Models},
  author={Ahmed, Khaled and Song, Jialing and Chen, Boqi and Wei, Ou and Zheng, Bingzhou},
  journal={arXiv preprint arXiv:2508.00630},
  year={2025}
}
```
