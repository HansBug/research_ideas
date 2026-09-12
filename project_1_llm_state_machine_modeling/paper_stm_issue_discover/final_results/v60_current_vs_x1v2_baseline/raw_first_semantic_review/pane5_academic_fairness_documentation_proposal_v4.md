# Paper1 academic/fairness/documentation raw-first review proposal v4

身份：`subagent/LLM proposal`。本文件是独立只读审查结果，不是真人 adjudicator 签字，不设置 `human_confirmation`，不冒充最终人工真值。

结论：`FAIL`。发现 6 项：`I=3`、`M=3`。本 proposal 不修改 frozen raw、canonical decisions、method/Judge 制品或正式汇总；未调用 provider，未运行 method、Judge 或实验。

审查仓库：`/home/zhangshaoang/oo-projects/research_ideas`
审查时间：2026-08-29 Asia/Shanghai
HEAD：`af7cab04aa10061febc356d62fdf6efac759ad6b`
分支：`paper1/m-witness-discovery`

## Raw-first boundary

首轮独立 proposal 在提交前只读取了冻结 raw/source、current evaluator/judge source、issue/protocol 文档和当前 Markdown；没有读取 `derived/manual_adjudication_v2/` 的 canonical decision、summary、group/relation decisions，也没有读取 frozen N/I reference labels。当前 Markdown 的一致性问题作为 documentation evidence 记录，不把任何旧 Judge 标签当作人工真值。

Protected spans：issue `#189`、`#195`；冻结 Judge commit `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`；协议 hash `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`；`162` cells/arm、`145` expected、`435` round-level rows、L2 `39/117`；`D2/D1/D0/A0`、`FULL_MATCH/PARTIAL_MATCH/NO_MATCH`、`VALID_KNOWN/VALID_NOVEL/INVALID`、`W0/W1/W2`、`not_applicable`；`report_issue_clusters` 与 `parsed_output.issues`；current source IR/FCSTM/inspection-equivalent/native facts 的角色边界。

`shuorenhua` 场景：`docs + README`，档位 `minimal`，无源判断使用 `audit-only`，输出为 annotation/review。已读取 skill 主文件及 protected-spans、positive-style、operation-manual、structures、scene-packs、scene-guardrails、severity、examples 和 real-samples。Pass 1 保留了路径、命令、版本、hash、数字、分母、枚举、issue、责任主体和输入角色；Pass 2 只检查开场/总结/narrator/空泛判断/节奏残留，没有为了文风改变技术事实。

## Findings

### AFD-RAW-001 [I] Predicate provenance cannot be audited from the frozen catalog

路径：`final_results/v60_current_vs_x1v2_baseline/reference/current_source_catalog.json` 的全部 28 个 source records；`related_work/provenance/CURRENT_SOURCE_AUDIT.md:3,7-16`。

Reason：catalog 实际只含 `id/types/title/paths/supports/boundary`，缺 authors、year、venue、DOI/stable link 和 accessed date。仅凭该机器真源，无法逐 predicate 核验完整书目信息、来源身份和 claim 支持范围；文档不应把 19 predicates 统一写成已经完成可审计的学术资格审查。

Basis：逐项读取 catalog key 集合，与 `predicate_registry.json` 的 registry/source mapping 对照；未用旧 audit 标签替代书目证据。

复算命令：

```bash
jq '{source_count:(.sources|length),source_key_sets:([.sources[]|keys]|unique)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/current_source_catalog.json
```

Disposition：`required`。修复 commit：`none`。Targeted rereview：逐 19 predicate/28 source ID 核对 authors、year、venue、DOI 或稳定链接、访问日期、具体支持 claim、boundary 和证据等级，并检查 JSON 与文档一致。

### AFD-RAW-002 [I] Source-audit prose overstates independent verification

路径：`related_work/provenance/CURRENT_SOURCE_AUDIT.md:3,14`；`discover_matrix/docs/protocol/defect_taxonomy.md:62,668-680`。

Reason：source audit 的“均具有完成的学术资格审查”“所有记录都已完成核验”没有保留证据档位，而 taxonomy 明确记录二手归属、本人未独立复核、全文未取到等限制。按 docs 的 `audit-only` 规则，这会把有条件的 provenance 误读为统一已核验事实。

Basis：逐行对照总括结论与 taxonomy 的取证档位；未为未读取的论文补充任何外部结论。

复算命令：

```bash
rg -n '均具有完成|所有记录都已完成|未独立复核|全文未取到|仅核书目' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/related_work/provenance/CURRENT_SOURCE_AUDIT.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/defect_taxonomy.md
```

Disposition：`required`。修复 commit：`none`。Targeted rereview：补齐证据等级后，逐项检查正文 claim 是否不超过对应来源等级；未核内容必须保留为限制或缺口。

### AFD-RAW-003 [M] Frozen Judge v3.2 and current evaluator v3.3 need an explicit boundary

路径：两侧冻结 composite 的 `protocol_version`、`judge_algorithm_version`、`semantic_judge_commit`；`judge/src/paper_stm_judge/protocol.py:11-12`；`discover_matrix/docs/protocol/semantic_judge_protocol.md:17-25`。

Reason：raw 实验 identity 是 `semantic-judge.two-stage.v3.2`、commit `05cf0da6...`，而源码已存在 v3.3。两者可以共存，但 current-facing 文档必须明确“冻结实验协议/实现”与“当前源码版本”的区别，否则读者可能把 v3.3 误读成冻结结果的来源。

Basis：直接读取两侧 raw composite version fields，并与当前 protocol constants 对照；没有把当前源码版本回填到 raw。

复算命令：

```bash
jq '{protocol_version,judge_algorithm_version,semantic_judge_commit}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/v60_current/judge/composite/summary.json \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/judge/composite-summary.json
rg -n 'PROTOCOL_VERSION|JUDGE_ALGORITHM_VERSION' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/judge/src/paper_stm_judge/protocol.py
```

Disposition：`required`。修复 commit：`none`。Targeted rereview：逐个检查 report、README、SCHEMA、protocol 和 review 文本，确认 v3.2 raw identity 与 v3.3 implementation 没有混写。

### AFD-RAW-004 [M] `Hit Rate` and hit denominators need an explicit bridge

路径：`discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md:125-145`；`evaluation/README.md:7-19`；`final_results/v60_current_vs_x1v2_baseline/SCHEMA.md:9-17`。

Reason：issue snapshot 的 `Hit Rate` 以 unique expected issue 为分母；当前 evaluation 的 `hit@1` 使用 435 个 round-level units，而 `hit@3/all` 使用 145 个 unique expected。它们可同时存在，但同一入口必须逐项写清 numerator/denominator，且明确 issue snapshot 的历史口径，避免 145 和 435 被读成同一个指标。

Basis：逐行对照冻结 issue snapshot、evaluation README 与 archive schema；没有根据比例反推缺失分子。

复算命令：

```bash
rg -n 'Hit Rate|hit@1|round-level|435|145|L2|117|39' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/README.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/SCHEMA.md
```

Disposition：`required`。修复 commit：`none`。Targeted rereview：检查主报告、README、SCHEMA 和 issue-facing 文本是否共同说明 overall `435`、unique expected `145`、L2 `117/39` 以及旧 snapshot 的分母。

### AFD-RAW-005 [M] Dual-arm input projection requires a field-level fairness table

路径：`evaluation/src/paper_stm_evaluation/judge_input_projection.py:24-76,633-680,684-766`；`judge/src/paper_stm_judge/artifacts.py:344-550,633-680`；`reference/x1v2_input_closure/manifest.json`；两侧 raw method records。

Reason：两侧输入 schema 不同：current report 位于 `report_issue_clusters`，baseline finding 位于 `parsed_output.issues`；baseline closure manifest 明确只保留 hash-verified NL/PlantUML，而 current artifact closure 还包括 canonical source IR、FCSTM、native/inspection facts、working contract 和 source trace。差异不自动证明不公平，但文档必须给出 shared、arm-specific、`not_applicable` 字段的逐字段表，并写清 expected ledger 只能在人工 relation adjudication 使用的时点。不能只写“两侧完全相同输入”。

Basis：直接读取两侧 raw record、baseline closure manifest、adapter 和 artifact-closure source；没有把 current predicate receipt 当成 baseline 的必需条件，也没有把 later Judge 能力当成 baseline method witness。

复算命令：

```bash
jq '{keys:keys,report_count:(.report_issue_clusters|length)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method/method/0037/round-1.json
jq '{keys:keys,issue_count:(.parsed_output.issues|length)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/method/run1/0000-luna/record.json
nl -ba project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src/paper_stm_evaluation/judge_input_projection.py | sed -n '24,90p;633,766p'
nl -ba project_1_llm_state_machine_modeling/paper_stm_issue_discover/judge/src/paper_stm_judge/artifacts.py | sed -n '344,550p;633,680p'
```

Disposition：`required`。修复 commit：`none`。Targeted rereview：检查 fairness/leakage review 是否给出 field-level paired-input evidence，baseline predicate usage 是否为 `not_applicable`，以及 baseline W2 没有使用后验 Judge 证据。

### AFD-DOC-006 [I] Current-facing Markdown still contains superseded headline facts

路径：`paper_stm_issue_discover/README.md:21-24,28`；`STATUS.md:16`；`story/paper_story.md:19`；`story/claim_evidence_map.md:7`；`final_results/v60_current_vs_x1v2_baseline/README.md:23,25,32-38`；当前中文报告 `report/v60_current_vs_x1v2_baseline_cn.md:3-23`。

Reason：current-facing README、STATUS、story 和 archive README 仍列 `306/435`、`118/145`、`84/145`，并称 721 条 K 尚未逐条复审；同一 current 中文报告第一屏已经声称使用 `derived/manual_adjudication_v2/` 的最终人工监督裁定并列出另一组 headline。读者会同时看到两套互相冲突的当前结果，无法判断哪一套是论文事实源。旧 Judge 结果可以保留，但只能标为 historical/diagnostic 并移出当前 headline。

Basis：逐文件 grep 当前 Markdown 的数字、状态和“未完成”措辞；本 finding 不把任何旧或新标签当作 raw-first 人工真值，只判断导航与文本之间的事实一致性。

复算命令：

```bash
rg -n '306/435|118/145|84/145|721|未完成|尚未逐条复审|不能替换' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/{README.md,STATUS.md,story,final_results/v60_current_vs_x1v2_baseline}
```

Disposition：`required`。修复 commit：`none`。Targeted rereview：重新生成或核对 current-facing 文档，逐表检查 numerator/denominator/percentage、绝对差和百分点差；旧 v3.2 headline 必须带 historical/diagnostic 标签且不进入主结果表。

## Review result and handoff

所有 finding 当前均为 `required`，没有可直接 `accepted-with-reason` 的项；不存在 targeted rereview 通过记录，修复 commit 均为 `none`。主 session 修复后应针对每项运行上列命令，并对受影响文档和 provenance 逐项回读；若新增 canonical 数字或 manifest，必须另行读取其机器真源并更新对应 review。

本文件是 subagent/LLM proposal，不能单独满足 human adjudication、FINAL 或 ready gate。
