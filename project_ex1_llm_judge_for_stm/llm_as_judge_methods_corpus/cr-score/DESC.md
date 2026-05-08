# CRScore — DESC

## 1. 论文元信息

- **标题**：CRScore: Grounding Automated Evaluation of Code Review Comments in Code Claims and Smells
- **作者**：Atharva Naik, Marcus Alenius, Daniel Fried, Carolyn Rosé
- **单位**：Carnegie Mellon University, LTI
- **年份 / Venue**：**NAACL 2025**
- **arXiv / URL**：https://arxiv.org/abs/2409.19801
- **fingerprint**：reference-free 多维 review-quality metric for code review comments；neuro-symbolic（LLM + 静态分析工具）；与本研究 7 维 review-quality 框架最对齐的同类工作

## 2. 一句话定位

> 提出 **CRScore**：reference-free 评估 code review comment 质量的多维度 metric（conciseness / comprehensiveness / relevance），通过 LLM 抽取 code claims + 静态分析工具检测 code smells 作为 grounded reference，与人评 Spearman 0.54。

## 3. 评判对象（Judging Object）

- **类型**：code review comment（人或 LLM 写的 review 文本）
- **典型 task**：评估自动 code review systems 生成的 review comments 与 GitHub 真实 review comments 的质量
- **与 STM artifact 的相似度**：⚪ — 评判对象是 review comment（自由文本），不是 SE artifact 本身；但**评判方法学（多维 review-quality framework）与本研究 7 维 rubric 高度同构**

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) Code diff（被评 code change）；(2) Review comment（待评质量的 NL 文本）；(3) **pseudo-references**（LLM 抽取 + 静态分析生成的 code claims 与 issues 列表）|
| **输出** | (a) Conciseness score；(b) Comprehensiveness score；(c) Relevance score；(d) Overall score |

## 5. Method 核心 — Neuro-symbolic + 多维 review-quality

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | Pure prompting + 静态分析工具组合（neuro-symbolic）|
| **rubric anchor** | ✓ — **3 维 anchored** review-quality rubric，每维有清晰的语义定义 |
| **CoT** | partial |
| **聚合** | 多维 → STS-based alignment 与 pseudo-references 比对 |
| **Calibration** | 报告与人评 Spearman correlation |
| **数据集** | 释放 2.9k 人工标注 review-quality scores |

## 6. 评估方式

- **human reviewer**：是 — 2.9k 人工标注作 ground truth
- **metric**：CRScore 与人评的 Spearman correlation = **0.54**（开源 metric 中最高）
- 与 reference-based metric（BLEU / ROUGE）对比：CRScore 更敏感（catch fine-grained quality 差异）

## 7. 报告的 effect size + noise

- Spearman 0.54 with human judgment（开源 metric 最高）
- 比 reference-based metric 更敏感
- **是否多 seed**：✗
- **是否报告 noise floor**：✗

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ |
| **L2 Provider drift** | ✗ |
| **L3 Rubric anchor** | ✓ — 3 维 anchored；与我们 7 维 rubric 设计同思路 |
| **L4 STM 适配** | ⚪ — 评判对象是 review comment（NL）非 SE artifact；但**多维 review-quality framework** 设计可借鉴 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴（重要）

- **多维 review-quality 设计**：CRScore 用 conciseness / comprehensiveness / relevance 三维评 review 文本质量；本研究用 7 维评 review report；**设计哲学高度一致**——都把 review-quality 作为多维可分解对象，每维 anchored 定义
- **Neuro-symbolic grounding** 思路：CRScore 用 LLM 抽 claims + 静态分析检 smells 作为 grounded reference；本研究的 evidence-quoting + per-dim score 是同类思路在 prompting-only 路径的简化版
- **2.9k human-annotated dataset 设计**：是 Path C human review benchmark 的可借鉴模板
- **0.54 Spearman 是基线参考**：我们 LLM-as-Judge 与人评对齐度的目标 baseline

### 9.2 重要差异

- 评判对象不同：CRScore 评的是 review comment 质量（NL），本研究评的是 SE artifact 质量
- 同一研究方向**review-quality** 的两条腿——他们做 review comment 的 review-quality，我们做 SE artifact 的 review-quality

### 9.3 §Related Work 引用句拟稿

> "Naik et al. [Naik25] proposed CRScore, a reference-free metric for evaluating code review comments along three review-quality dimensions (conciseness, comprehensiveness, relevance), grounded by LLM-extracted code claims and static-analyzer-detected smells. **CRScore is methodologically the closest cousin to our 7-dimensional review-quality framework**: both decompose review-quality into multiple anchored dimensions and use neuro-symbolic grounding (LLM + auxiliary signals) to produce per-dimension scores. The two works differ in the object being evaluated — CRScore evaluates the **review comment**, while our work evaluates the **SE artifact** that is being reviewed. Together they evidence a converging methodology in SE: multi-dimensional anchored evaluation grounded by neuro-symbolic signals."

## 10. 引用导出

```bibtex
@inproceedings{naik2025crscore,
  title={CRScore: Grounding Automated Evaluation of Code Review Comments in Code Claims and Smells},
  author={Naik, Atharva and Alenius, Marcus and Fried, Daniel and Ros{\'e}, Carolyn},
  booktitle={Proceedings of NAACL 2025},
  year={2025}
}
```
