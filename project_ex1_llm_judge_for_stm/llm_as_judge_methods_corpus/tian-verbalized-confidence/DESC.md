# Verbalized Confidence (Tian et al.) — DESC

> ⚠️ **PDF 待获取**。本 DESC 基于 AI 训练知识写的初稿。

## 1. 论文元信息

- **标题**：Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
- **作者**：Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, Christopher D. Manning
- **单位**：Stanford
- **年份 / Venue**：**EMNLP 2023**
- **arXiv / URL**：https://arxiv.org/abs/2305.14975
- **阅读状态**：Skim only
- **fingerprint**：通过 prompt 让 LLM 自己 verbalize 它对答案的 confidence（"On a scale of 0-100 ..." 或 "What's the probability ..."）；发现 RLHF-tuned models 反而更校准

## 2. 一句话定位

> 让 LLM **直接说出**它对自己回答的 confidence（数字 / linguistic phrase），通过简单 prompt 工程在 **TriviaQA / NaturalQuestions** 等 QA 任务上获得**比 logprobs / CoT-derived confidence 更校准**的不确定性估计。**RLHF-tuned models 输出的 verbalized confidence 比 base models 更校准**——这是反直觉的关键发现。

## 3. 评判对象（Judging Object）

- **类型**：LLM **自己回答**的 confidence
- **典型 task**：TriviaQA / NaturalQuestions / SciQ
- **与 STM artifact 的相似度**：⚪ unrelated（QA confidence vs structured judging score）
- **应用场景**：可在 LLM-as-Judge 流程中作为 confidence-elicitation 替代 logprobs

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) Question；(2) LLM 给的回答；(3) confidence elicitation prompt（如 "What's your confidence on a scale 0-100?" 或 "How likely is this answer correct? respond as 'highly likely / likely / unlikely / highly unlikely'"）|
| **输出** | confidence score（0-100 numeric）/ linguistic phrase（mapped to numeric） |

I/O schema：QA pair + elicitation prompt → numeric confidence。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | Pure prompting（不动权重）|
| **rubric anchor** | n/a |
| **CoT** | 可选 — 论文实验了 with/without CoT 两种 |
| **聚合** | 单次取分；不依赖多 sample |
| **Calibration** | **直接评估方法本身的 calibration（ECE / Brier score）**|

**Verbalize 形式**：
- numeric: "0-100 confidence"
- linguistic: "very likely / likely / unsure / unlikely / very unlikely"
- token logprobs（baseline 对比）

## 6. 评估方式

- **数据集 ground truth**：QA 任务有标准答案；correctness 是 binary
- **calibration metrics**：ECE (Expected Calibration Error) / Brier Score / Reliability Diagrams
- **inter-rater agreement**：n/a（calibration 不需要 human reviewer）

## 7. 报告的 effect size + noise

- RLHF-tuned models（GPT-3.5 / Claude-1）verbalize 的 confidence ECE 显著低于 base GPT-3
- linguistic 形式（如 "highly likely"）有时比 numeric 更校准
- **是否多 seed**：✓ 不同 prompt template 多次跑取均
- **是否有 noise floor 讨论**：🟡 部分（讨论 prompt sensitivity 但不是 sample noise）

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | 🟡 prompt sensitivity 报告（同 prompt 不同 phrasing 结果差异）但无 sample-level σ |
| **L2 Provider drift** | ✗ 论文使用 GPT-3.5 / Claude-1 specific；不同 model checkpoint 之间的 calibration 大概率不同 |
| **L3 Rubric anchor** | n/a |
| **L4 STM 适配** | 🟡 verbalized confidence 思路**可迁移**到 STM judge：让 LLM judge 给 score 时也直接 verbalize confidence。但需要警惕 W2 §16 confidence-formula bug 的教训：confidence 输出范围必须与 downstream metric heuristic 兼容 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Verbalized confidence as Q3-v2 candidate**：W2 §16 提到 std-based confidence 公式失效后，verbalized confidence 是 next candidate；Tian paper 是直接 anchor
- **RLHF-tuned 比 base 更校准**：意味着我们应该用 instruction-tuned 模型而非 base 模型做 LLM-judge（airouter gpt-5.5 是 reasoning + RLHF tuned，符合）
- **Linguistic phrase 形式**：可作为 numeric 替代 — 实验设计可考虑

### 9.2 不借鉴

- **Pure QA-correctness setting**：QA 是 binary correct/wrong；STM judge 是连续分；calibration 维度不直接相同
- **不直接做 calibration metric 评估**：我们更关心 score-with-human alignment，不是 confidence-with-correctness

### 9.3 对比 baseline

paper §Related Work 引用方式：

> "Tian et al. [Tian23] showed that RLHF-tuned LLMs can produce verbalized confidence scores that are more calibrated (lower ECE) than logit-based confidences. **Our work extends this to LLM-as-Judge for STM artifacts**, where confidence elicitation must be compatible with downstream confidence-thresholded metrics (we expose this constraint via W2 confidence-formula bug audit)."

## 10. 引用导出

```bibtex
@inproceedings{tian2023just,
  title={Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback},
  author={Tian, Katherine and Mitchell, Eric and Zhou, Allan and Sharma, Archit and Rafailov, Rafael and Yao, Huaxiu and Finn, Chelsea and Manning, Christopher D.},
  booktitle={Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
  year={2023}
}
```
