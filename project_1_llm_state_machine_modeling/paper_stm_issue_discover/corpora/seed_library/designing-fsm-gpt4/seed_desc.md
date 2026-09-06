# Designing FSM Specifications from Requirements with GPT-4

## R1.5 strict seed 全文核验结论

| 字段 | 当前判断 |
|---|---|
| candidate_id | `designing-fsm-gpt4` |
| source_batch | baseline / local fulltext |
| local_source | [`baselines/designing-fsm-specifications-from-requirements-gpt4/`](../../../../baselines/designing-fsm-specifications-from-requirements-gpt4/) |
| bibliographic_id | arXiv:2603.29140, 2026 |
| strict_seed_grade | `SS-B` |
| artifact_usability | `SA-2` |
| R2_seed_usability | `initial-generation-only conditional seed candidate` |
| repair_oracle_sections | `excluded-from-seed / reference-only` |
| 当前结论 | 可作为 `NL requirement -> DFSM/Mealy CSV` 的条件 strict seed 候选，但只限初始生成链路；不得把论文 repair/oracle/fault-model 实验整体当作 seed，也不得标为 `SS-A`。 |

## P1/P2/P3/P4 核验

| 谓词 | 判断 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | `paper_content.txt` Page 1 abstract 称从 requirements 设计 FSM；Page 4 Listing 1.1 给出英文 DFSM description；Page 9 说明随机生成 oracle DFSM 后由英文 sentence patterns 生成 description；Appendix Listing 1.5-1.7 给出 NL pattern。 |
| P2_T0_STM_FAMILY | pass | Page 3 定义 FSM 五元组 $S = (S, s_0, X, Y, T)$；Page 3-4 明确研究 deterministic finite state machine / Mealy machine；Page 6 Listing 1.2 要求输出 `State,Input,Output,Next_State` CSV，且 complete and deterministic。 |
| P3_GENERATION_RELATION | pass | Page 2-3 明确目标是用 GPT-4 从 textual descriptions 生成 specification / DFSM；Page 5-6 描述 prompt-based generation；Listing 1.2 是 `DFSM_description -> CSV DFSM` 的直接生成 prompt。 |
| P4_EVIDENCE_POINTER | pass | 本地全文、BibTeX、PDF 和 baseline `DESC.md` / `ASSETS.md` 已给出可追溯证据；关键页码见上三行。 |

## SS / SA / 排除码

| 维度 | 判断 | 说明 |
|---|---|---|
| SS | `SS-B` | 初始生成链路严格满足 P1-P4，但输入是模板合成英文描述，不是真实控制系统需求；输出是平坦 DFSM/Mealy，不含层次、并发、guard、action、time；代码入口不是论文正文给出，artifact 稳定性不足。 |
| SA | `SA-2` | 有本地论文材料与额外核到的 GitHub 代码/样例数据，可用于探索复现；但无 release、无依赖锁、无标准 split，结果表与仓库文件仍需人工对齐。许可 / 再分发不作为额外升绿阻塞。 |
| 排除码 | none for initial seed | 初始 `NL -> DFSM CSV` 不触发 protocol-only、trace-only、T1+ only、non-STM、no-generation 排除。 |
| 局部排除 | `EX-REPAIR-ORACLE-AS-SEED` | 论文的 syntactic fault、distinguishing sequence、checking sequence、fault-model repair 依赖 oracle/专家反馈或修复域搜索，只能作为 R2/repair 方法参考，不能替代初始 seed 样本。 |

## 可抽取 seed 边界

可抽取的 seed 只包括：

1. 输入：英文自然语言 DFSM 描述，例如 Page 4 Listing 1.1。
2. 目标输出：GPT-4o 生成的 CSV DFSM，字段为 `State,Input,Output,Next_State`。
3. 形式化对象：deterministic finite state machine / Mealy machine。
4. 评价证据：与 oracle DFSM 的 syntactic / semantic comparison 结果可作为质量标签。

不应纳入 seed 的内容：

1. 用 oracle 直接暴露的 transition delta 修复 prompt。
2. distinguishing/checking sequence repair prompt 中的专家答案。
3. fault-model / mutation-machine mining 产生的 repaired DFSM。
4. 论文表格中的 aggregate repair success rate，除非另建 R2 repair benchmark。

## R2 seed 可用性

`initial-generation-only conditional seed candidate`。可交接给 PR-R2 的仅是初始 `NL description -> DFSM/Mealy CSV` seed 切片：输入为英文自然语言 DFSM 描述，输出 schema 为 `State,Input,Output,Next_State` CSV，形式化对象为 deterministic finite state machine / Mealy machine。该切片仍带合成数据、无 release / split 冻结等 caveat；许可 / 再分发不作为额外升绿阻塞。

### repair / oracle 部分只作参考，不作 seed

论文提供四类修复思路，适合作为 Project 1 后续修复反馈设计的参考：

- syntactic fault prompt repair：可映射到 missing transition / wrong output / wrong target。
- distinguishing sequence repair：可作为 trace feedback 负例或对照组。
- checking sequence repair：可借鉴“专家只回答行为 trace”的低负担查询思想。
- fault-model repair domain：可借鉴“限制候选修复空间，而不是让 LLM 自由改写全模型”。

这些 repair / oracle 部分当前不计入 seed：真实 artifact 未冻结，repair domain 构造依赖论文外代码与 oracle 增强，且实验数据是合成描述。PR-R2 若使用该候选，必须物理或逻辑隔离 initial-generation seed 切片，并在 provenance 中记录未使用 oracle / distinguishing sequence / checking sequence / fault-model 修复输出。

## 证据文件与 hash

| 文件 | SHA-256 |
|---|---|
| `bibtex.bib` | `b76108c18dc429d5cf112672930943de045cdf83e7f1a8abf00073f0210717b5` |
| `paper_content.txt` | `6d90ebc9e302574df1cb4ba033a9a348b1110388109495146956dc478eefb947` |
| `paper.pdf` | `d49fd30733aaa7c7d6dd7aeb9f28f72ecc59d0594dcf7bd9da373bbe9ac1628f` |

## 待补 / 主要阻塞

| 等级 | 项 | 影响 |
|---|---|---|
| 待补 | GitHub repo 与论文版本关系需作者确认或 release 固化 | 影响复现实验严谨性，不影响 P1-P4 seed 判定。 |
| 引用说明 | 许可 / 再分发不作为升绿阻塞 | 后续使用公开学术资源时引用原作，并优先补 commit/hash。 |
| 待补 | 合成数据未冻结 split | 影响把该工作纳入正式 baseline matrix 的统计复现。 |
| blocker-for-SS-A | 非真实控制系统需求、无冻结 artifact / release | 阻止升为 `SS-A`。 |

## 全文阅读状态

- `bibtex.bib`：已核，arXiv preprint，无 DOI。
- `paper_content.txt`：已通读 Page 1-21，正文、表格、附录和参考文献完整覆盖本轮判定。
- `paper.pdf`：本地存在；因文本提取已覆盖关键证据，本轮未额外 OCR。
- `ASSETS.md` / `DESC.md`：已读；采纳其中 GitHub 资产、HEAD、release / 版本冻结风险判断。
