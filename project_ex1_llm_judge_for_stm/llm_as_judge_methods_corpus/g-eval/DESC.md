# G-Eval — DESC

> ⚠️ **PDF 待获取**。本 DESC 基于 AI 训练知识 + 公开摘要写的初稿，正式 paper writing 前需读全文修订。

## 1. 论文元信息

- **标题**：G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment
- **作者**：Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, Chenguang Zhu
- **单位**：Microsoft Research
- **年份 / Venue**：**EMNLP 2023**
- **arXiv / URL**：https://arxiv.org/abs/2303.16634
- **阅读状态**：Skim only（abstract + key figures from training data）
- **fingerprint**：form-filling prompt + auto-generated CoT evaluation steps + Spearman correlation with human

## 2. 一句话定位

> 用 **GPT-4 + 自动生成的 evaluation steps（CoT 形式）+ form-filling prompt** 给 NLG 输出打分，与 human 评分的 Spearman 相关性比 BLEU/ROUGE 等 reference-based metric 高出显著一档。

## 3. 评判对象（Judging Object）

- **类型**：NLG 输出（自由文本）
- **典型 task**：
  - SummEval（dialog summary 质量）
  - Topical-Chat（dialog response quality）
  - QAGS（QA-based fact alignment）
- **与 STM artifact 的相似度**：⚪ unrelated（自由文本 vs 结构化制品）

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) 被评 candidate text（如 dialog summary）；(2) 任务定义；(3) 评分标准 description；(4) **auto-generated CoT evaluation steps**（由 GPT-4 自己根据 task definition 生成的"step 1: ... step 2: ..."流程）|
| **输出** | 单个 score（连续 1-5 / 1-10 取决于任务），通过 form-filling 让 LLM 填到结构化 schema |

I/O schema：结构化 prompt → 结构化 score。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | Pure prompting（不动权重）|
| **rubric anchor** | **auto-generated**（GPT-4 自动生成 evaluation steps）|
| **CoT** | ✓（让 LLM 列出评分推理步骤）|
| **聚合** | 单次取分（论文也尝试了取多次平均，效果略提升）|
| **Calibration** | 无显式校正 |
| **Form-filling** | ✓（结构化 prompt 强制结构化输出）|

**算法 sketch**（简化）：

```
prompt = task_def + criteria + auto_generated_eval_steps
candidate_score = LLM(prompt + candidate)  # 输出 1-5 score
```

## 6. 评估方式 — 与 human 对齐协议

- **human reviewer**：原 dataset（SummEval / Topical-Chat / QAGS）已含 human ratings
- **评分尺度**：Likert 1-5（per dimension）
- **与方法对齐**：Spearman / Kendall τ / Pearson 与 human aggregate 比
- **inter-rater agreement**：dataset 自带

**主要 metric**：Spearman correlation with human (per dataset, per dimension)

## 7. 报告的 effect size + noise

- 在 SummEval 4 维度（coherence/consistency/fluency/relevance）上，G-Eval（GPT-4）Spearman 显著高于 BLEU/ROUGE/BERTScore 等 reference-based
- **是否多 seed**：未报告（典型 single-shot LLM 实验）
- **是否有 noise floor 讨论**：✗ 未报告
- **典型对比 baseline**：BLEU, ROUGE, BERTScore, BARTScore, GPTScore, UniEval

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ 单次实验无 σ；论文用 dataset-level Spearman 作为单 number，无 confidence interval |
| **L2 Provider drift** | ✗ 论文使用 GPT-4 specific date；不同 GPT-4 checkpoint / temperature 设置下行为差异未报告 |
| **L3 Rubric anchor** | 🟡 auto-generated 评分流程；优点是 task-agnostic，**缺点是无 domain expert anchoring**——对 SE artifact 这种 domain-heavy 评判对象不一定适用 |
| **L4 STM 适配** | 🔴 STM 是结构化模型（state / transition / guard），不是自由文本；G-Eval 的 form-filling rubric 可能可平移，但 evaluation steps 自动生成对 STM 的语义结构不敏感 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Form-filling prompt** 的结构化输出范式 —— project_ex1 的 rubric_dim_score.py 已采纳类似设计
- **Per-dimension Spearman** 评估 —— project_ex1 的 7 维 framework 评估时也用 Spearman with human

### 9.2 不借鉴

- **Auto-generated evaluation steps**：不适合 STM artifact，因为 STM 评判维度需要 domain expert 锚定（结构 / 语义 / 时序约束 ...），auto-generated 的 step 没有 domain knowledge 信息
- **单次取分**：W3 noise floor 实证 single-shot 不可信

### 9.3 对比 baseline

作为 paper §Related Work 的关键 anchor 引用，对比口径：

> "G-Eval [Liu23] proposed an auto-rubric LLM-as-Judge framework for NLG evaluation but: (a) targets free-form text without structural semantics; (b) reports single-shot scores without noise floor estimation; (c) has no domain anchoring for SE artifacts. We extend it to STM artifacts with anchored rubric + strict-llm protocol + measured noise floor."

## 10. 引用导出

```bibtex
@inproceedings{liu2023geval,
  title={G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment},
  author={Liu, Yang and Iter, Dan and Xu, Yichong and Wang, Shuohang and Xu, Ruochen and Zhu, Chenguang},
  booktitle={Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
  year={2023}
}
```

Key argument 摘录（待全文读后修订）：
> "G-Eval with GPT-4 achieves significantly higher correlation with humans than all previous methods on the SummEval benchmark."
