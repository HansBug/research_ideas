# From Code to Courtroom — DESC

## 1. 论文元信息

- **标题**：From Code to Courtroom: LLMs as the New Software Judges
- **作者**：Junda He, Jieke Shi, Terry Yue Zhuo, Christoph Treude, Jiamou Sun, Zhenchang Xing, Xiaoning Du, David Lo
- **单位**：Singapore Management University + Monash + CSIRO Data61 + ANU
- **年份 / Venue**：arXiv 2025 03（"SE 2030 forward-looking paper"）
- **arXiv / URL**：https://arxiv.org/abs/2503.02246
- **阅读状态**：Skim（已读 abstract + introduction）
- **fingerprint**：**SE 域 LLM-as-Judge 的第一篇 forward-looking 综述 / roadmap**；不是方法论文，是 SE 社区视角的总览 + 未来路线图

## 2. 一句话定位

> 站在 **SE 2030 视角**总览"LLM 作为 software 制品评判者"的研究现状，识别关键 research gaps，给出到 2030 年实现"reliable, robust, scalable LLM-as-Judge for SE artifacts"的 roadmap。

## 3. 评判对象（Judging Object）

- **类型**：survey 性质，不评判具体制品；论述 LLM-as-Judge 在以下 SE artifacts 上的应用：code generation、code summarization、commit message、bug report、test case、issue 等
- **典型 task**：综述性，覆盖 SE 全谱
- **与 STM artifact 的相似度**：⚪ **不直接** — survey 不深入 STM；但**论述了 LLM-as-Judge 应进一步覆盖 UML / formal specs / state machines 等结构化制品**，恰好为我们提供了"why STM judge is timely"的引用支撑

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | survey 性质，不直接评判 |
| **输出** | (1) 现有 SE-domain LLM-as-Judge 工作综述；(2) Limitations 分类表；(3) Research gaps；(4) 2030 roadmap |

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **类型** | Survey / vision / roadmap paper（不是方法论文）|
| **覆盖范围** | code generation / summarization / repair / 等 SE 任务的 LLM-as-Judge 实践 |
| **关键论点** | (a) human eval 贵且慢；(b) BLEU/ROUGE 等 reference-based metric 抓不到 readability/usefulness 等 nuanced quality；(c) LLM-as-Judge 是 cost-efficient surrogate，但当前研究 still in early stages |

## 6. 评估方式

n/a — 综述论文不做实验。

## 7. 报告的 effect size + noise

n/a — 综述论文。

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 / L2 / L3 / L4** | survey 范畴，不评估自身 |
| **作为引用源的局限** | 是 vision paper，未必给出每个 sub-claim 的实验证据；引用时应交叉对原论文核实 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Vision-level 引用**：在 paper §1 Introduction / §Related Work 引用 He25 作为 "SE 社区已经认识到 LLM-as-Judge 重要性，但当前研究不够" 的支撑
- **research gap 列表**：作者列出的 SE-domain LLM-as-Judge 当前缺失，可作为我们 §Motivation 的 anchor
- **2030 roadmap**：把我们的工作放进这个 roadmap 中（"a step toward the SE 2030 vision of reliable LLM-as-Judge for structured SE artifacts"）

### 9.2 不借鉴

- 不是方法论文，无法借鉴具体方法
- 综述论文的 limitation 分类未必精准，引用前需对照原论文

### 9.3 对比 baseline

paper §Introduction 引用方式（拟稿）：

> "He et al. [He25] articulate a SE 2030 vision in which LLM-as-Judge frameworks become reliable, robust, and scalable surrogates for human evaluators of software artifacts. **Their analysis identifies that existing SE-domain LLM-as-Judge research has thus far concentrated on free-form artifacts (code, summaries, commit messages) and pays limited attention to structured behavioral models such as state machines.** This paper takes a concrete step toward that vision by addressing LLM-as-Judge for state machine artifacts under a methodologically rigorous noise-floor protocol."

## 10. 引用导出

```bibtex
@article{he2025codecourtroom,
  title={From Code to Courtroom: LLMs as the New Software Judges},
  author={He, Junda and Shi, Jieke and Zhuo, Terry Yue and Treude, Christoph and Sun, Jiamou and Xing, Zhenchang and Du, Xiaoning and Lo, David},
  journal={arXiv preprint arXiv:2503.02246},
  year={2025}
}
```
