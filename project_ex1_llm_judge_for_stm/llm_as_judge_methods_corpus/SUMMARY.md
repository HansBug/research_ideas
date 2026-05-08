# LLM-as-Judge 方法学论文集 SUMMARY

## 1. 当前收录概况

- 已收录方法学论文：**7** 篇（全部为骨架 placeholder，PDF ⏳ 待获取）
- 已完成 `DESC.md`：**7** 篇（基于 AI 训练知识写的初版分析；正式 paper writing 前需读全文修订）
- 全文已读：**0** 篇
- 仅读 abstract / 部分内容：**0** 篇

## 2. 论文清单（按发表年份升序）

| Slug | 标题 | 年份 | Venue | 评判对象 | 方法核心 | 收录状态 |
|---|---|---:|---|---|---|:-:|
| [self-consistency](./self-consistency/DESC.md) | Self-Consistency Improves CoT Reasoning in Language Models | 2023 | ICLR 2023 | 推理任务输出 | 同 prompt 多次采样 + majority vote | 🟡 已起 DESC，PDF 待获取 |
| [g-eval](./g-eval/DESC.md) | G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment | 2023 | EMNLP 2023 | NLG 输出（dialog summary / news summary）| Form-filling + CoT + auto-rubric | 🟡 已起 DESC，PDF 待获取 |
| [tian-verbalized-confidence](./tian-verbalized-confidence/DESC.md) | Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models | 2023 | EMNLP 2023 | LLM 自身回答 | 让 LLM 自报 confidence（verbalize numeric / linguistic） | 🟡 已起 DESC，PDF 待获取 |
| [mt-bench](./mt-bench/DESC.md) | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | 2023 | NeurIPS 2023 | LLM dialog 回答（80 prompts × N model）| Multi-turn judge + position-bias / verbosity correction + Pairwise比较 | 🟡 已起 DESC，PDF 待获取 |
| [constitutional-ai](./constitutional-ai/DESC.md) | Constitutional AI: Harmlessness from AI Feedback | 2022 | Anthropic preprint | LLM 自身输出（critique-revise loop）| Critique-first → revise → score；RLAIF | 🟡 已起 DESC，PDF 待获取 |
| [judgelm](./judgelm/DESC.md) | JudgeLM: Fine-tuned Large Language Models are Scalable Judges | 2023 | arXiv 2023 | 自由文本 candidate（pairwise / pointwise）| Fine-tune Vicuna 系列做 judge，主打效率 | 🟡 已起 DESC，PDF 待获取 |
| [prometheus](./prometheus/DESC.md) | Prometheus: Inducing Fine-grained Evaluation Capability in Language Models | 2024 | ICLR 2024 | NLG 输出（task 多样）| Fine-tune Llama 在 1000+ rubric 上做 fine-grained scoring | 🟡 已起 DESC，PDF 待获取 |

## 3. Method 维度分类（横向看）

### 3.1 按 Prompting vs Training

| 类型 | 论文 |
|---|---|
| **Pure prompting**（不动 LLM 权重）| G-Eval, MT-Bench, Self-Consistency, Verbalized Confidence |
| **Trained judge**（fine-tune 一个 judge LLM） | JudgeLM, Prometheus |
| **RLAIF**（用 LLM feedback 做 reward）| Constitutional AI |

### 3.2 按 Output 类型

| 输出 | 论文 |
|---|---|
| **Pointwise score**（单 candidate 给绝对分） | G-Eval, Prometheus, Verbalized Confidence |
| **Pairwise preference**（两 candidate 选 better） | MT-Bench, JudgeLM, Constitutional AI |
| **Multi-step CoT 输出 + 最终 verdict** | G-Eval, MT-Bench, Self-Consistency |

### 3.3 按是否 anchor rubric

| anchor 程度 | 论文 |
|---|---|
| **无 rubric anchor**（LLM 自由判断）| Self-Consistency, Constitutional AI |
| **Auto-generated rubric** | G-Eval（自动生成 evaluation criteria）|
| **预定义 rubric** | Prometheus（1k+ rubric），JudgeLM（fine-tune 时 rubric 蕴含），MT-Bench（per-task rubric）|
| **Verbalized self-rating** | Tian Verbalized Confidence |

## 4. 评判对象的多样性 — generic 文本 vs 结构化制品

| 评判对象 | 是否 SE artifact | 论文 |
|---|:-:|---|
| Dialog / instruction 回答 | ✗ | MT-Bench, JudgeLM, Constitutional AI |
| Summary / translation / generic NLG | ✗ | G-Eval, Prometheus |
| Reasoning chain | ✗ | Self-Consistency |
| LLM 自身 confidence | ✗ | Verbalized Confidence |
| **代码 / SE artifact** | ✓ | **本论文集暂无收录**（这是 project_ex1 的目标空白点）|
| **状态机 / UML / 形式化模型** | ✓ | **本论文集暂无收录**（这是 project_ex1 的目标空白点）|

**关键观察**：**LLM-as-Judge 文献几乎全部聚焦于 generic 自由文本输出**；对 SE artifact / 结构化模型的判定几乎是文献空白。这是 project_ex1 想要填补的空缺。

## 5. 检索关键词簇

### 5.1 当前推荐

- `LLM-as-Judge / LLM as evaluator / LLM judge`
- `auto evaluation` + `language models / reasoning / generation`
- `rubric` + `LLM` + `evaluation / scoring`
- `verbalized confidence / calibration` + `LLM`
- `position bias / verbosity bias / LLM evaluator bias`
- `pairwise preference / RLAIF / Constitutional AI`
- `evaluator alignment / judge alignment / human-LLM agreement`
- `fine-grained evaluation / fine-tuned judge / Prometheus / JudgeLM`

### 5.2 未来扩展方向（暂未收录）

- **Code-specific judges**：CodeJudge / CodeBLEU / CodeBERTScore 类
- **Faithfulness / hallucination 判定**：FActScore / SAFE 类
- **结构化制品评估**：UMLEvalBench 等（如有；本研究方向的目标空白）
- **Eval-of-eval / meta-evaluation**：CheckEval 等

## 6. 失败 / 待获取记录

- 全部 7 篇 PDF **⏳ 待获取**：使用 arXiv / OpenReview / venue 链接抓取，按 single-paper [DESC_GUIDE.md](./DESC_GUIDE.md) 流程入仓
- 抓取后用 `tools/pdf_extractor.py` 生成 `paper_content.txt`
- 全文阅读后修订各 `DESC.md` 第 4-7 节

## 7. 更新日志

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-05-08 19:30 | 创建论文集 | 7 篇论文 placeholder + 骨架 DESC.md（基于 AI 训练知识初稿）|
