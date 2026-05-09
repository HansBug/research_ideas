# RESpecBench — DESC

## 1. 论文元信息

- **标题**：RESpecBench: How Reliable is LLM-as-a-Judge? Rigorous Evaluation of Specification Generation with Automated Verification
- **作者**：Anonymous（双盲评审）
- **单位**：Anonymous
- **年份 / Venue**：**Submitted to ICLR 2026**（OpenReview，under double-blind review）
- **URL**：https://openreview.net/forum?id=eFwJZIN9eI
- **fingerprint**：**直接挑战 LLM-as-Judge 可靠性的 benchmark paper**——证明 LLM-as-Judge 在 formal specification 生成上**严重高估正确性**，与本研究 noise floor / reliability concern **方法学动机高度一致**

## 2. 一句话定位

> 给 LLM-as-Judge 在 NL → formal specification 生成任务上提供 **5 个领域的 sound automated verifier**（GSM-Symbolic+ / SQL / FOL / RegEx / Rocq Prover），证明 **LLM-as-Judge 产生不可靠 verdict 且严重高估 specification 正确性** —— 是当前最直接挑战 LLM-as-Judge 可靠性的论文。

## 3. 评判对象（Judging Object）

- **类型**：NL → formal specification 生成任务的输出（spec 自身），不是 SE artifact
- **典型 task**：5 个领域的 NL → spec：math word problem → symbolic equation；NL query → SQL；statement → FOL；regex 描述 → regex；NL → Rocq proof obligation
- **与 STM artifact 的相似度**：⚪ — 不是 STM；但 **方法学态度（量化 LLM-as-Judge 不可靠）与本研究 noise floor 协议同向**

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) NL 描述；(2) LLM 生成的 specification（SQL / FOL / Rocq 等）；(3) 双轨：(a) LLM-as-Judge pipeline；(b) sound automated verifier |
| **输出** | (a) LLM judge 的 correctness verdict；(b) sound verifier 的 ground truth verdict；(c) 两者 disagreement rate |

## 5. Method 核心 — Sound verifier 作 ground truth 反向验证 LLM judge

| 维度 | 选择 |
|---|---|
| **核心创新** | **用 sound automated verifier 作 ground truth**，反向暴露 LLM-as-Judge 的不可靠 |
| **覆盖范围** | 5 个 formal domain |
| **结论** | LLM-as-Judge **严重高估** specification 正确性，**verdict unreliable** |

## 6. 评估方式

- **ground truth**：sound automated verifier（每个 domain 都有真正的 verifier 而非依赖 LLM）
- **metric**：LLM-as-Judge 与 sound verifier 的 disagreement rate；overestimation rate

## 7. 报告的 effect size + noise

- 多个 SOTA LLM 判 specification correctness 时**显著 overestimate** vs sound verifier
- LLM-as-Judge 的 verdict 在多个 domain 都不可靠

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | partial — 论文核心就是 reliability evaluation，但侧重 **bias direction**（overestimation）而非 **stability variance** |
| **L2 Provider drift** | ✗ |
| **L3 Rubric anchor** | n/a — 任务本身是 binary semantic equivalence judgment |
| **L4 SE artifact** | ⚪ — formal specification 不是 STM，但属于 SE/formal-method 领域同侧 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴（重要）

- **方法学态度**：RESpecBench 与本研究**同方向但不同手段**——他们用 sound verifier 反验 LLM judge 的偏差，我们用 5-rep 多次重复验 LLM judge 的方差
- **联合引用**：在 paper §Motivation / §Related Work 中**联合引用** RESpecBench（"LLM-as-Judge 在 formal spec 上 unreliable"）+ 本研究（"LLM-as-Judge 在 STM artifact 上需要 noise floor 协议"）形成"reliability of LLM-as-Judge in SE/formal methods is an emerging concern" 的更强论述
- **5 个 domain 设计**：可作为本研究扩展到其他 formal 领域的参考

### 9.2 重要差异

- RESpecBench 关注**单次 verdict 的偏差方向**（overestimation），本研究关注**多次 rep 之间的方差**（stochasticity）
- RESpecBench 依赖 sound verifier（formal method 领域才有），本研究 SE artifact 评估通常没有 sound oracle，所以走 5-rep 路径

### 9.3 §Related Work 引用句拟稿

> "RESpecBench [Anon26] addresses LLM-as-Judge reliability from a complementary angle: using sound automated verifiers as ground truth, they demonstrate that LLM judges substantially overestimate specification correctness in five formal domains. **Their findings strengthen our methodological position**: LLM-as-Judge in SE / formal methods is not a solved evaluation paradigm, and treating its verdict as oracle without quantifying error is methodologically unsafe. Whereas RESpecBench attacks the **bias** axis (single-shot overestimation against sound verifier), our work attacks the **variance** axis (multi-replication noise floor); together they delineate two complementary reliability concerns LLM-as-Judge users must address."

## 10. 引用导出

```bibtex
@inproceedings{anonymous2026respecbench,
  title={RESpecBench: How Reliable is LLM-as-a-Judge? Rigorous Evaluation of Specification Generation with Automated Verification},
  author={Anonymous},
  booktitle={Submitted to ICLR 2026 (under double-blind review)},
  year={2026},
  url={https://openreview.net/forum?id=eFwJZIN9eI}
}
```
