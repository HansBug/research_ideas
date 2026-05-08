# Prometheus — DESC

> ⚠️ **PDF 待获取**。本 DESC 基于 AI 训练知识写的初稿。

## 1. 论文元信息

- **标题**：Prometheus: Inducing Fine-grained Evaluation Capability in Language Models
- **作者**：Seungone Kim, Jamin Shin, Yejin Cho, Joel Jang, Shayne Longpre, Hwaran Lee, Sangdoo Yun, Seongjin Shin, Sungdong Kim, James Thorne, Minjoon Seo
- **单位**：KAIST AI / Microsoft Research / NAVER
- **年份 / Venue**：**ICLR 2024**
- **arXiv / URL**：https://arxiv.org/abs/2310.08491
- **阅读状态**：Skim only
- **fingerprint**：FT Llama2-13B 在 1000+ 自定义 rubric 上做 fine-grained scoring；7 个 evaluation benchmark 上接近 GPT-4 evaluator 表现

## 2. 一句话定位

> 提出 **Prometheus**：在 1k+ 自动生成的 fine-grained rubric 上 fine-tune **Llama2-13B**，让一个 open-source 小模型获得**与 GPT-4 同水平的 fine-grained 评分能力**，覆盖任意自定义 rubric 而无需 retrain。

## 3. 评判对象（Judging Object）

- **类型**：generic NLG 输出（任意 task 的 candidate 输出）
- **典型 task**：summarization / dialog / code / instruction following / 各种 fine-grained quality 维度
- **与 STM artifact 的相似度**：⚪ unrelated（generic NLG vs structured artifact）

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) Instruction（被评 task 描述）；(2) Response （candidate 输出）；(3) Reference answer（gold output，可选）；(4) **Score rubric description**（如 "rate 1-5 based on coherence with the topic"）；(5) **Score description for each level**（"5: perfectly coherent ... 1: completely off-topic"）|
| **输出** | (1) Free-text feedback（评判说明）；(2) Numeric score 1-5 |

I/O schema：rubric-anchored prompt → (feedback, score) tuple。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | **Training**（FT Llama2-13B）|
| **rubric anchor** | ✓ — 1k+ 自定义 rubric 训练 + inference 时输入新 rubric |
| **CoT** | ✓ — 输出 feedback 然后 score（CoT-style）|
| **聚合** | n/a |
| **Calibration** | n/a |
| **Bias correction** | partial（fine-tune data 设计时考虑了 bias）|

**训练数据**：~100k feedback-score pairs，由 GPT-4 在 1k 自定义 rubric 上自动生成

## 6. 评估方式

- **human reviewer**：是 — 论文有 human rating 实验
- **metric**：
  - 与 GPT-4 evaluator 的 score 相关性（Pearson / Kendall）
  - 与 human rating 的 agreement
  - 在 7 个 benchmark 上 evaluate
- **inter-rater agreement**：报告

## 7. 报告的 effect size + noise

- Prometheus（13B）与 GPT-4 evaluator 的 Pearson ≈ 0.85（在 fine-grained rubric 评估上）
- 与 human rating 的 agreement 接近 GPT-4
- **是否多 seed**：✗ 单次 fine-tune
- **是否有 noise floor 讨论**：✗

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ 单次实验 |
| **L2 Provider drift** | n/a（self-hosted Llama2，无 API drift）|
| **L3 Rubric anchor** | ✓ —— rubric anchor 是核心贡献；inference 时支持任意自定义 rubric |
| **L4 STM 适配** | 🟡 rubric design 思路可借鉴，但 fine-tune 路径不可走（STM artifact 数据量 < 1k 不够训练）|

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Rubric description + per-level score description**：这正是我们 7-dim rubric 的设计，比 G-Eval 的 auto-generated 更严格
- **Feedback + Score 双输出**：rubric_dim_score.py 的 form-filling JSON schema 类似设计

### 9.2 不借鉴

- **FT 13B model**：data 不够；project_ex1 走 prompting-only 路线
- **Generic rubric library**：STM judge 的 rubric 是 7 个固定 domain-anchored 维度，不需要 1k+

### 9.3 对比 baseline

paper §Related Work 引用方式：

> "Kim et al. [Kim24] introduced Prometheus, a fine-tuned 13B Llama judge with comparable performance to GPT-4 on fine-grained rubric evaluation. **Our setting differs in two key respects**: (a) we focus on prompting-only LLM-as-Judge for STM artifacts where data is insufficient for fine-tuning; (b) Prometheus targets generic NLG output, while STM artifacts have explicit structural / behavioral semantics requiring domain-anchored rubrics rather than auto-generated ones."

## 10. 引用导出

```bibtex
@inproceedings{kim2024prometheus,
  title={Prometheus: Inducing Fine-grained Evaluation Capability in Language Models},
  author={Kim, Seungone and Shin, Jamin and Cho, Yejin and Jang, Joel and Longpre, Shayne and Lee, Hwaran and Yun, Sangdoo and Shin, Seongjin and Kim, Sungdong and Thorne, James and Seo, Minjoon},
  booktitle={The Twelfth International Conference on Learning Representations (ICLR)},
  year={2024}
}
```
