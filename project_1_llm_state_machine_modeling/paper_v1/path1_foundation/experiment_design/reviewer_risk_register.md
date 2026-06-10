# Path-1 Reviewer Risk Register

## 1. C/I/M 口径

- **C / Critical**：若不处理，会直接破坏论文可信度、实验公平性、oracle 可靠性或主 claim。
- **I / Important**：会显著削弱论文说服力，但可通过限定 claim、补实验、补说明解决。
- **M / Minor**：影响阅读体验、工程整洁度或局部措辞，不阻塞学术推进。

## 2. 当前风险总表

| ID | 等级 | 风险 | 触发条件 | 修复 / 降级策略 | 当前状态 |
|---|---|---|---|---|---|
| R1 | C | Baseline fairness 过强 | 声称 same benchmark / same protocol 打赢 prior work，但实际用了 sources / adapted protocol | 明确 reproduce / approximate / evidence-only；至少 1 个 same-sample approximate baseline | 待执行 |
| R2 | C | Reference / sample bias | 只用 PR #9 Top-15 或成功样本，且 claim 平均性能 | 冻结 full 9/101 或预注册降级样本；保留失败和排除原因 | 待执行 |
| R3 | C | Oracle weak | LLM judge 或单作者主观判断成为主结果 | `>=2` 独立 human annotator、blind coding、agreement、仲裁 | 待执行 |
| R4 | C | Claim-evidence mismatch | Abstract/Intro 写出尚未有结果的 lift / SOTA / complete verification | 用 [claim_evidence_map.md](../story/claim_evidence_map.md) gate 每个 claim | foundation 已建立，需后续执行 |
| R5 | I | E1/E2 framing 混乱 | 把 E1/E2 写成 Hybrid 方法或把 Codex/Claude 当贡献 | 写成 agent orchestration conditions / implementation study | foundation 已规避 |
| R6 | I | Formal feedback 被误读为深形式化验证 | parse/semantic/sim 被写成 model checking/theorem proving | 全文使用 formal feedback / executable simulation；BMC/LTL 放 future work | foundation 已规避 |
| R7 | I | Sample selection 是 stress-test 非代表性 | selection rationale 只基于 weak components，不能代表平均任务 | 主实验和 stress-test 分开报告；写清 sampling design | 待执行 |
| R8 | I | External baseline 不足 | 主实验只有 direct/structured/internal ablation | 至少 3 个 closest prior work 入矩阵，至少 1 个 same-sample approximate | 待执行 |
| R9 | I | Run record 不完整 | 缺 prompt/raw output/provider/usage/stage trace/eligibility | 使用仓库 run record 规范；provider error 不进入主统计 | method 已具备，主实验待执行 |
| R10 | I | PR #9 historical early reference draft 误用 | 把 CARA/CubeSat early ref 当最终 signed oracle | 明确 historical reference asset；正式复核签字 | foundation 已标注 |
| R11 | M | 术语过多 | FCSTM/pyfcstm/LangGraph/Codex/SC/SD/SL 堆叠影响阅读 | 论文主文用概念术语，工程名放 implementation/artifact | 待写作执行 |
| R12 | M | paper_v1 旧 sprint 口径残留 | 新 session 误读 2026-05 sprint 为当前事实 | 更新 [../README.md](../README.md) current overlay | 本 PR 处理 |

## 3. Reviewer mental model

希望 reviewer 形成的理解：

> This paper is not primarily a new DSL paper or a Codex workflow report. It studies whether executable formal feedback helps LLMs produce better state-machine models from control-system requirements, and it supports the claim through auditable runs, human adjudication, ablations, and careful baseline positioning.

需要避免 reviewer 形成的误解：

1. “作者只是写了一个私有 DSL 和 prompt。”
2. “实验只挑了最适合自己工具的成功例子。”
3. “LLM judge 自评自证。”
4. “formal verification claim 被夸大。”
5. “没有和近期 LLM-for-modeling 工作公平比较。”

## 4. Ready gate for this foundation PR

本 PR 只负责奠基，不负责主实验。Ready 的学术 gate：

- C 级风险均已在文档和 PR body 中显式承认，并转化为后续执行 gate。
- 不存在把历史资产误写成当前结果的表述。
- 不存在把第一篇 story 写成 Path-2 / Hybrid / DSL / LangGraph 主线的漂移。
- 后续执行计划能直接分解为样本冻结、baseline、oracle、run、写作、review 任务。
