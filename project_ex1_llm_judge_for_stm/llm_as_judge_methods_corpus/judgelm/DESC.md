# JudgeLM — DESC

> ⚠️ **PDF 待获取**。本 DESC 基于 AI 训练知识写的初稿。

## 1. 论文元信息

- **标题**：JudgeLM: Fine-tuned Large Language Models are Scalable Judges
- **作者**：Lianghui Zhu, Xinggang Wang, Xinlong Wang
- **单位**：HUST + BAAI
- **年份 / Venue**：arXiv 2023（preprint，后续 ICLR 投稿）
- **arXiv / URL**：https://arxiv.org/abs/2310.17631
- **阅读状态**：Skim only
- **fingerprint**：FT Vicuna 7B/13B/33B 在 100k+ pairwise 比较任务上做 judge；强调 cost-efficiency 比 GPT-4 judge

## 2. 一句话定位

> **Fine-tune Vicuna 系列**做 pairwise judge，用 100k+ GPT-4-distilled pairwise preferences 做训练数据，**得到 90%+ agreement with GPT-4 evaluator 的 cost-efficient open-source judge**。

## 3. 评判对象（Judging Object）

- **类型**：自由文本 candidate（pairwise / pointwise both supported）
- **典型 task**：dialog response / instruction following
- **与 STM artifact 的相似度**：⚪ unrelated

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) Question；(2) Two candidate answers (A, B)；(3) （可选）evaluation criteria；(4) （可选）reference answer |
| **输出** | (a) verdict（A wins / B wins / tie）+ explanation；或 (b) per-candidate pointwise score |

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | **Training**（FT Vicuna 7B / 13B / 33B）|
| **rubric anchor** | 弱 — 训练时 rubric 蕴含在 GPT-4 distilled prefs；inference 时不强制 explicit rubric |
| **CoT** | ✓ |
| **聚合** | n/a |
| **Calibration** | partial（论文讨论 position bias mitigation 通过训练数据 swap）|
| **Bias correction** | ✓ — 训练数据 augmentation（A/B 顺序交换增广）|

**训练数据**：100k+ samples from MT-Bench / Chatbot Arena 风格数据，由 GPT-4 自动 label

## 6. 评估方式

- **human reviewer**：用 MT-Bench 的 expert ratings 作 reference
- **metric**：agreement with GPT-4 / agreement with human
- **inter-rater agreement**：用 MT-Bench 的 reported agreement

## 7. 报告的 effect size + noise

- JudgeLM-7B agreement with GPT-4 ≈ 90%
- JudgeLM-33B agreement ≈ 95%
- **是否多 seed**：✗
- **是否有 noise floor 讨论**：✗

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ |
| **L2 Provider drift** | n/a |
| **L3 Rubric anchor** | 弱 — 隐式 rubric in 训练数据，inference 时不强制 explicit |
| **L4 STM 适配** | 🔴 fine-tune 路线 + dialog 数据不适合 STM；但 cost-efficiency 思路有借鉴：未来如能积累足够 STM judge 数据，或可 distill 一个 small judge |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Pairwise evaluation framework**：MT-Bench 同样 anchor，JudgeLM 是 fine-tune 实现。Project_ex1 的 S2-Q5 (pairwise) 可参考 JudgeLM 的 swap-augmentation
- **Cost-efficiency mindset**：长期 vision 中可考虑 distill 一个小 STM judge

### 9.2 不借鉴

- 其余基本与 Prometheus 同 — fine-tune 路线对 STM 数据不可行

### 9.3 对比 baseline

paper §Related Work 引用方式：

> "Zhu et al. [Zhu23] introduced JudgeLM, a fine-tuned Vicuna-based judge that achieves 90%+ agreement with GPT-4 evaluators on dialog tasks. Both this and Prometheus [Kim24] demonstrate that **task-specific fine-tuning can match GPT-4 judging quality at lower cost**, but require sizable training data (100k+ pairwise preferences) — making this approach unavailable for SE artifact judging where annotated data is scarce. Project_ex1 thus targets prompting-only methodology."

## 10. 引用导出

```bibtex
@article{zhu2023judgelm,
  title={JudgeLM: Fine-tuned Large Language Models are Scalable Judges},
  author={Zhu, Lianghui and Wang, Xinggang and Wang, Xinlong},
  journal={arXiv preprint arXiv:2310.17631},
  year={2023}
}
```
