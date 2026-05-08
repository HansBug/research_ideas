# Constitutional AI — DESC

> ⚠️ **PDF 待获取**。本 DESC 基于 AI 训练知识写的初稿。

## 1. 论文元信息

- **标题**：Constitutional AI: Harmlessness from AI Feedback
- **作者**：Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosiute, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, Jared Kaplan
- **单位**：Anthropic
- **年份 / Venue**：2022 (Anthropic preprint, arXiv 2212.08073)
- **arXiv / URL**：https://arxiv.org/abs/2212.08073
- **阅读状态**：Skim only
- **fingerprint**：critique → revise loop driven by 16-条 constitution；RLAIF（vs RLHF）

## 2. 一句话定位

> 提出 **Constitutional AI（CAI）**：用 LLM **自批 + 自改**循环（基于一组写好的 "constitution" 原则）替代人类标注者的 RLHF 偏好数据，**让模型自己生成 preference data 来训练 reward model（RLAIF）**，最终训出 helpful + harmless 的 Claude。

## 3. 评判对象（Judging Object）

- **类型**：LLM 自身输出（response 是否符合 constitution）
- **典型 task**：red-teaming prompts → harmful response 改良；helpfulness 维持
- **与 STM artifact 的相似度**：⚪ unrelated（自由文本 dialog vs 结构化模型）

## 4. 输入 / 输出（I/O）

### 4.1 SL-CAI 阶段（Supervised Learning）

| 项 | 内容 |
|---|---|
| **输入** | (1) red-teaming prompt；(2) original LLM response；(3) **a critique principle from the constitution**；(4) revise instruction |
| **输出** | improved response |

### 4.2 RL-CAI 阶段（RLAIF）

| 项 | 内容 |
|---|---|
| **输入** | (1) prompt；(2) 两个 candidate responses (A, B)；(3) constitution-based comparison principle |
| **输出** | preference (A or B) → 用于训练 preference model（PM）|

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | **Both — Prompting 用于产生数据，Training 用于产生最终 model**（RLAIF）|
| **rubric anchor** | ✓ —— 16 条 constitution（"please choose the response that is more helpful, honest, harmless..."）|
| **CoT** | ✓（critique-first → revise；让 LLM 显式说出哪条 principle 被违反，再 revise）|
| **聚合** | n/a（每条 prompt 单次处理，但 PM 从大量 preference 数据训练）|
| **Calibration** | n/a |
| **Bias correction** | partial（论文讨论 self-preference bias）|

**算法 sketch**：

```
# SL-CAI
response_0 = LLM(prompt)
critique = LLM("critique this response per principle X: " + response_0)
revised = LLM("revise according to critique: " + critique)
# Train SL model on (prompt, revised) pairs

# RL-CAI
for prompt:
    A, B = SL_model.sample(prompt) × 2
    pref = LLM("pick more helpful per constitution: " + A + B)
    # collect prefs → train PM → RLHF (with PM as reward)
```

## 6. 评估方式

- **human reviewer**：red-teaming experts (Anthropic internal)
- **metric**：harmlessness rate（held-out red-teaming prompts）+ helpfulness rate（traditional dialog quality）
- **inter-rater agreement**：未单独报告 κ

## 7. 报告的 effect size + noise

- CAI 模型 harmlessness 大幅提升、helpfulness 不下降
- **是否多 seed**：✗ 实验大多数 single training run（资源约束）
- **是否有 noise floor 讨论**：✗

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ 训练-eval pipeline 单次实验；不考虑同 setup 多次重训的 outcome 分布 |
| **L2 Provider drift** | ✗ Anthropic in-house 实验，无 API drift 问题；不可外推 |
| **L3 Rubric anchor** | ✓ — 16 条 constitution 是 hand-crafted anchor；这是 CAI 的核心贡献之一 |
| **L4 STM 适配** | 🔴 RLAIF training pipeline 远超 prompting-only 实验的复杂度；STM judge 不适合走 fine-tune 路线（数据量不够），但 critique-first 思路可借鉴 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Critique-first → Score / Revise**：W1.5 era 我们考虑过 S2-Q2（critique-first scoring），CAI 是直接 anchor；不过 W2 §16 audit 显示 critical_issue_recall 已 0.99 接近上限，Q2 ROI 不高
- **Constitution / Principle-based rubric anchoring**：CAI 的 16-principle approach 提示我们 STM judge 的 rubric 应该有"宪章式"明确锚定（比如"评 record regime 时必须满足 8 条领域 principle"）

### 9.2 不借鉴

- **RLAIF fine-tuning**：project_ex1 是 prompting-only LLM-as-Judge，不走 fine-tune 路线
- **Self-preference / pairwise prompting**：CAI 主要是 alignment 训练，不是 judge methodology

### 9.3 对比 baseline

paper §Related Work 引用方式：

> "Bai et al. [Bai22] introduced Constitutional AI to align LLM behavior via critique-revise loops driven by 16-principle constitutions. While their RLAIF pipeline is orthogonal to prompting-only LLM-as-Judge, **the principle-anchored rubric design parallels our domain-anchored 7-dimensional STM rubric**. We extend this to SE artifact evaluation with measured noise floor."

## 10. 引用导出

```bibtex
@article{bai2022constitutional,
  title={Constitutional AI: Harmlessness from AI Feedback},
  author={Bai, Yuntao and Kadavath, Saurav and Kundu, Sandipan and Askell, Amanda and others},
  journal={arXiv preprint arXiv:2212.08073},
  year={2022}
}
```
