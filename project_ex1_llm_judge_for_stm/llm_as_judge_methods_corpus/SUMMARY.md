# LLM-as-Judge 方法学论文集 SUMMARY

## 1. 当前收录概况

- 已收录方法学论文：**14** 篇（7 generic LLM-as-Judge + 7 SE-artifact / SE-reliability LLM-as-Judge）
- PDF 已抓取：**14 / 14**（2026-05-08 完成）
- paper_content.txt 已抽取：**14 / 14**（text 模式，无需 OCR）
- 已完成 `DESC.md`：**14** 篇（其中 7 generic 是基于 AI 训练知识写的初版骨架；7 SE-artifact 是 skim PDF 后写的较细 DESC；全文深读修订仍待）
- 全文已读：**0** 篇
- skim 后写过 DESC 但未通读：**14** 篇

## 2. 论文清单（按发表年份升序）

### 2.1 Generic LLM-as-Judge 方法学（7 篇，源自 NLP / 自由文本主流）

| Slug | 标题 | 年份 | Venue | 评判对象 | 方法核心 | 收录状态 |
|---|---|---:|---|---|---|:-:|
| [constitutional-ai](./constitutional-ai/DESC.md) | Constitutional AI: Harmlessness from AI Feedback | 2022 | Anthropic preprint | LLM 自身输出（critique-revise loop）| Critique-first → revise → score；RLAIF | ✅ PDF 已抓 |
| [self-consistency](./self-consistency/DESC.md) | Self-Consistency Improves CoT Reasoning in Language Models | 2023 | ICLR 2023 | 推理任务输出 | 同 prompt 多次采样 + majority vote | ✅ PDF 已抓 |
| [g-eval](./g-eval/DESC.md) | G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment | 2023 | EMNLP 2023 | NLG 输出（dialog summary / news summary）| Form-filling + CoT + auto-rubric | ✅ PDF 已抓 |
| [tian-verbalized-confidence](./tian-verbalized-confidence/DESC.md) | Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models | 2023 | EMNLP 2023 | LLM 自身回答 | 让 LLM 自报 confidence（verbalize numeric / linguistic） | ✅ PDF 已抓 |
| [mt-bench](./mt-bench/DESC.md) | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | 2023 | NeurIPS 2023 | LLM dialog 回答（80 prompts × N model）| Multi-turn judge + position-bias / verbosity correction + Pairwise比较 | ✅ PDF 已抓 |
| [judgelm](./judgelm/DESC.md) | JudgeLM: Fine-tuned Large Language Models are Scalable Judges | 2023 | arXiv 2023 | 自由文本 candidate（pairwise / pointwise）| Fine-tune Vicuna 系列做 judge，主打效率 | ✅ PDF 已抓 |
| [prometheus](./prometheus/DESC.md) | Prometheus: Inducing Fine-grained Evaluation Capability in Language Models | 2024 | ICLR 2024 | NLG 输出（task 多样）| Fine-tune Llama 在 1000+ rubric 上做 fine-grained scoring | ✅ PDF 已抓 |

### 2.2 SE-artifact / SE-reliability LLM-as-Judge / 同类工作（7 篇，2026-05-08 新增）

| Slug | 标题 | 年份 | Venue | 评判对象 | 方法核心 | 与 STM 接近度 |
|---|---|---:|---|---|---|:-:|
| [code-judge](./code-judge/DESC.md) | CodeJudge: Evaluating Code Generation with Large Language Models | 2024 | EMNLP 2024 | LLM 生成代码（多语言）| Pure prompting + slow-thinking（analyze-summarize 或 taxonomy-guided fault localization）| 🟡 同 SE artifact 大类，但 code 是文本流 |
| [cr-score](./cr-score/DESC.md) | CRScore: Grounding Automated Evaluation of Code Review Comments in Code Claims and Smells | 2025 | NAACL 2025 | code review comment（NL 文本）| Reference-free 多维 review-quality（concise / comprehensive / relevant），neuro-symbolic（LLM + 静态分析），Spearman 0.54 with human | ⚪ 评 review comment 不是 SE artifact，但**多维 review-quality 框架与本研究 7 维 rubric 设计高度同构** |
| [uml-diagram-assessment](./uml-diagram-assessment/DESC.md) | Toward Automated UML Diagram Assessment: Comparing LLM-Generated Scores with Teaching Assistants | 2025 | CSEDU 2025 | UML class diagram（学生作业，92 份）| Pure prompting + anchored rubric + few-shot examples；与 3 TA 对照 Pearson > 0.76 / MAE < 4 | 🟡 UML 同源但 class diagram 是 structural model |
| [mcet](./mcet/DESC.md) | MCeT: Behavioral Model Correctness Evaluation using Large Language Models | 2025 | arXiv / IEEE | UML sequence diagram | Atomic decomposition + multi-perspective + cross-check self-consistency；direct 0.58 → 0.81 precision | ✅ **最接近** — sequence diagram 与 STM 同为 UML behavioral model |
| [mermaid-seq-bench](./mermaid-seq-bench/DESC.md) | MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation | 2025 | NeurIPS 2025 workshop | Mermaid sequence diagram | Benchmark + LLM-as-Judge with 6 fine-grained dimensions（Syntax / Logic / Completeness / etc.）| ✅ **同源** — 与 MCeT 同针对 sequence diagram；DSL 文本化路线与 STM 同构 |
| [respec-bench](./respec-bench/DESC.md) | RESpecBench: How Reliable is LLM-as-a-Judge? Rigorous Evaluation of Specification Generation with Automated Verification | 2026 | ICLR 2026（under review）| NL → formal specification（5 domains）| Sound verifier 反向验证 LLM judge → 证明 LLM judge **严重高估正确性** | ⚪ 不是 STM，但**方法学动机（quantify LLM-as-Judge unreliability）与 noise floor 协议同向** |
| [code-to-courtroom](./code-to-courtroom/DESC.md) | From Code to Courtroom: LLMs as the New Software Judges | 2025 | arXiv（SE 2030 vision）| 综述 — 覆盖 SE 全谱制品 | Survey / roadmap，不是方法 | ⚪ 综述，明确把 UML / formal spec 列为 gap |

## 3. Method 维度分类（横向看）

### 3.1 按 Prompting vs Training

| 类型 | 论文 |
|---|---|
| **Pure prompting**（不动 LLM 权重）| G-Eval, MT-Bench, Self-Consistency, Verbalized Confidence, **CodeJudge**, **MCeT**, **UML-Assessment** |
| **Trained judge**（fine-tune 一个 judge LLM） | JudgeLM, Prometheus |
| **RLAIF**（用 LLM feedback 做 reward）| Constitutional AI |
| **Survey / vision**（不是方法）| **From Code to Courtroom** |

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
| **预定义 rubric** | Prometheus（1k+ rubric），JudgeLM（fine-tune 时 rubric 蕴含），MT-Bench（per-task rubric），**UML-Assessment**（教学 rubric），**CodeJudge Method B**（9 类 error taxonomy）|
| **Atomic decomposition + multi-perspective** | **MCeT**（拆 atomic interaction + atomic requirement，多视角 cross-check） |
| **Verbalized self-rating** | Tian Verbalized Confidence |

## 4. 评判对象的多样性 — generic 文本 vs 结构化制品

| 评判对象 | 是否 SE artifact | 论文 |
|---|:-:|---|
| Dialog / instruction 回答 | ✗ | MT-Bench, JudgeLM, Constitutional AI |
| Summary / translation / generic NLG | ✗ | G-Eval, Prometheus |
| Reasoning chain | ✗ | Self-Consistency |
| LLM 自身 confidence | ✗ | Verbalized Confidence |
| **代码（generic）**| ✓ | **CodeJudge** |
| **UML class diagram（structural）**| ✓ | **UML-Assessment** |
| **UML sequence diagram（behavioral）**| ✓ | **MCeT** ← 与 STM 最近 |
| **SE artifact 综述 / vision** | ✓ | **From Code to Courtroom** |
| **状态机 / formal model** | ✓ | **本论文集暂无收录** ← project_ex1 目标空白点 |

**关键观察更新（2026-05-08）**：从 4 篇新增 SE-artifact 工作可见，**LLM-as-Judge 已经开始扩展到 SE artifact**：code（CodeJudge 2024）、UML class diagram（Bouali 2025）、UML sequence diagram（MCeT 2025）；但**对 state machine 这种 timed/guarded behavioral model 仍是空白**。MCeT 是与本研究最近的同类工作，其方法（atomic + multi-perspective）可借鉴；但 sequence diagram 与 state machine 的核心差异（guards / temporal constraints / hierarchy）使 MCeT 不能直接套用——这是 project_ex1 的差异化空间。

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

- ✅ **2026-05-08 完成**：全部 11 篇 PDF + paper_content.txt 已抓取入仓（7 generic + 4 SE-artifact）
- ⏳ **待办**：全文阅读后修订各 `DESC.md` 第 4-7 节（特别是 7 篇 generic 当前是 AI 训练知识的初版）
- ⏳ **可继续扩展**：根据 [Awesome-LLMs-as-Judges](https://github.com/CSHaitao/Awesome-LLMs-as-Judges) 与 [A Survey on LLM-as-a-Judge](https://arxiv.org/abs/2411.15594)（Gu et al. 2024）持续追新

## 7. 更新日志

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-05-08 19:30 | 创建论文集 | 7 篇 generic LLM-as-Judge 论文 placeholder + 骨架 DESC.md（基于 AI 训练知识初稿）|
| 2026-05-08 20:10 | 抓取 7 篇 PDF + paper_content.txt | arXiv 直链下载 + `tools/pdf_extractor.py` 文本抽取 |
| 2026-05-08 20:35 | 新增 SE-artifact LLM-as-Judge 4 篇 | code-judge / mcet / code-to-courtroom / uml-diagram-assessment；PDF + bibtex.bib + DESC.md（skim 后写）；其中 **mcet** 是与 STM 最接近的同类工作（同为 UML behavioral model） |
| 2026-05-08 20:50 | 深读 code-to-courtroom + 第二轮检索 → 再增 3 篇 | mermaid-seq-bench（IBM NeurIPS 2025 workshop, sequence diagram benchmark）/ cr-score（CMU NAACL 2025, 多维 review-quality framework）/ respec-bench（ICLR 2026 under review, LLM-as-Judge reliability benchmark）；与 STM 最近的工作链已基本完整 |
