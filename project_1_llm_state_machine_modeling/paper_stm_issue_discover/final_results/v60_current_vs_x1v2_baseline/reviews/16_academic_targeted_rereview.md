# Academic targeted rereview：最终文档、协议边界与 predicate provenance

身份：`subagent/LLM proposal`。本文件是只读 academic targeted rereview，不是真人 adjudicator 签字，不设置 `human_confirmation`，不修改 frozen raw 或 canonical decisions。

审查日期：2026-08-29（Asia/Shanghai）
审查时 HEAD：`af7cab04aa10061febc356d62fdf6efac759ad6b`
分支：`paper1/m-witness-discovery`
范围：最终中文报告、final archive README/SCHEMA、issue `#189/#195` 对齐、D/A/K/N/I、relation、W、grouping、19 predicate registry/source catalog/provenance、双侧输入公平性和发布 manifest。

审查结论：`FAIL`。本轮 `C=0`、`I=4`、`M=3`。没有调用 provider，没有运行 method/Judge/实验。本结论是 subagent proposal，不能单独满足 ready gate。

## Shuorenhua docs 审查记录

场景为 `docs + README`，处理模式为 `minimal + audit-only`。protected spans 包括版本、issue、commit、run ID、hash、路径、命令、指标、分母、枚举、predicate ID、reviewer 身份和责任主体；这些字段未被改写。

Pass 1 保真核对：逐行检查报告、README、SCHEMA 和协议中的当前数字、D/A/K/N/I/W 定义、`not_applicable`、输入角色和限制是否仍可回指结构化 JSON、代码或冻结协议。Pass 2 residual audit：检查当前入口中的旧 headline、总结/旁白腔、无源学术断言、术语漂移和新增链接；发现的问题列为下述 finding，没有用改写掩盖证据缺口。

## Evidence basis

- registry identity：`four-family-19-core.v1`，19 predicates，family counts `6/4/4/5`；19 条 predicate mapping 使用 28 个 source ID，全部可解析到 `reference/current_source_catalog.json`。
- `reference/current_source_catalog.json` 与 `related_work/provenance/current_source_catalog.json` 的 SHA-256 均为 `45ee60a378cb192ec364f1ee563e5ce8fb9cb8f79a4ed71dc8869049806a5647`。
- source catalog 的实际 schema 只有 `id/types/title/paths/supports/boundary`，28/28 条均无 authors/year/venue/bibliography/DOI/stable-link/access-date 字段。
- `derived/manual_adjudication_v2/predicate_source_provenance.json` 有 19 predicate rows、57 source-provenance rows；57/57 的 `bibliography`、`doi_or_stable_link`、`accessed_at` 缺失或为空。
- frozen Judge raw 两侧均为 `semantic-judge.two-stage.v3.2`，commit `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`；当前协议源码声明 `semantic-judge.two-stage.v3.3`。
- `semantic_judge_issue_195.snapshot.md` 存在且 SHA-256 为 `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`；仓库内没有 issue `#189` 的正文快照或 `D_PROTOCOL.md`。
- provider-free manual validator 通过：`1271/1271`、`512/512`、`258535` dense relation rows、`provider_calls=0`。但 final archive validator 失败于过期 manifest 的 README hash mismatch。

## Previously reported findings

### ACAD-16-001 [I] Current archive README presented superseded headline results

路径：`final_results/v60_current_vs_x1v2_baseline/README.md:1-36`；对照正式报告 `report/v60_current_vs_x1v2_baseline_cn.md:1-41`。

Reason：旧版 README 曾把 `306/435`、`118/145`、`84/145`、`1165/1271` 和冻结 `721/444/106` 放在当前比较中。当前工作区 README 已改为人工 v2 的 `D/A`、`K/N/I`、`K_hit/N_group/I_group` 和人工报告入口，没有检出这些旧 headline 或“尚未逐条复审”表述。

Basis：读取当前 README 与报告，并执行旧 headline 检索；当前 README 第 3-6、24-36 行明确把旧 Judge v3.2 限定为 calibration/proposal/历史资料。

复算命令：

```bash
rg -n -i '306/435|118/145|84/145|1165/1271|尚未逐条复审|不能冒充' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md
```

Disposition：`fixed in working tree`；尚无修复 commit。旧数值仍可在明确标记的历史 Judge 文件中保留，但不能回到当前入口。

Targeted rereview：`PASS`（工作区状态）。README、SCHEMA、报告三处当前入口均指向 `derived/manual_adjudication_v2/`；完整 archive validator 仍因 ACAD-16-006 失败，不能把该失败误记为本 finding 回归。

### ACAD-16-002 [I] Archive SCHEMA used an obsolete grouping unit

路径：`final_results/v60_current_vs_x1v2_baseline/SCHEMA.md:52-74`；对照 `derived/manual_adjudication_v2/schema.md:20-23`、`protocol_freeze_v2.md:19` 和正式报告 `report/v60_current_vs_x1v2_baseline_cn.md:41`。

Reason：当前 SCHEMA 已删除旧的 `pair_id + round + root_cause_cluster_key` 发布定义，改为同一 `side + pair` 内跨 round 的人工 substantive group，并明确 `canonical_group_key`、不跨 side/pair、不按文本相似度/状态名/expected ID 自动合并，以及 operational unit 的限制。

Basis：逐行对照 archive SCHEMA、manual v2 schema、protocol freeze、`group_decisions.json` 和报告的 N/I 说明。

复算命令：

```bash
rg -n -i 'root_cause_cluster_key|same-side|same-pair|cross-round|canonical_group_key|不跨 side/pair' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/SCHEMA.md
```

Disposition：`fixed in working tree`；尚无修复 commit。旧 cluster 口径只能作为历史协议，不得用于当前 N/I。

Targeted rereview：`PASS`（工作区状态）。当前 SCHEMA、manual v2 schema、protocol freeze 和报告的 grouping contract 一致；manifest 问题另列 ACAD-16-006。

## Open findings

### ACAD-16-003 [I] Predicate provenance is identity-closed but not bibliography-closed

路径：`final_results/v60_current_vs_x1v2_baseline/reference/current_source_catalog.json:1`；`derived/manual_adjudication_v2/predicate_source_provenance.json:1`；`related_work/provenance/CURRENT_SOURCE_AUDIT.md:7-16`。

Reason：19-to-28 source mapping 和路径闭合通过，但正式 provenance 仍没有逐 source 的 authors/year/venue/bibliography、DOI/stable link、access date。57/57 rows 的这些字段为空或不存在。`defect_taxonomy.md:672-706` 的 inline bibliography 只能证明部分文档已有引用，不能替代 57 条机器 provenance；它还明确记录二手归属、未独立复核和全文未取到。因此当前数据支持“有 source mapping、supports 和 boundary”，不支持“完整、逐 predicate 可追溯的 bibliography provenance”。

Basis：实际读取 registry `families[*].predicates[*].sources`、source catalog 全部 28 records、provenance 全部 19/57 rows 和现有 bibliography 限制；没有从 title/path 共现推断学术支持。

复算命令：

```bash
jq '{registry_version,public_predicate_count,family_counts}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/predicate_registry.json
jq '{sources:(.sources|length),source_keys:([.sources[]|keys]|unique)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/current_source_catalog.json
jq '{predicate_rows:(.rows|length),source_rows:([.rows[].source_provenance[]]|length),missing_bibliography:([.rows[].source_provenance[]|select((.bibliography//"")=="")]|length),missing_link:([.rows[].source_provenance[]|select((.doi_or_stable_link//"")=="")]|length),missing_access:([.rows[].source_provenance[]|select((.accessed_at//"")=="")]|length)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/predicate_source_provenance.json
```

Disposition：`required fix or explicit claim downgrade`。补齐 28 source IDs 的可核查 bibliography/link/access 字段和每个 predicate 的具体 supporting claim；若现有证据不足，则把 `academic_eligibility=all_19_frozen_predicates_reviewed` 与“均具有完成的学术资格审查”降为分级 evidence gap，不得把 source mapping 写成独立文献验证。此 finding 不要求修改 frozen registry semantics。

Targeted rereview：`FAIL / not rerun`。当前 19/57 provenance rows 仍缺上述字段；`CURRENT_SOURCE_AUDIT.md:3,14` 仍使用无分级的完成性声称，`defect_taxonomy.md` 仍记录未独立复核/未取全文限制。

### ACAD-16-004 [I] Academic verification prose exceeds the recorded evidence level

路径：`final_results/v60_current_vs_x1v2_baseline/reference/predicate_registry.json` 的 `academic_eligibility`；`related_work/provenance/CURRENT_SOURCE_AUDIT.md:3,14`；`discover_matrix/docs/protocol/defect_taxonomy.md:62,668-706`。

Reason：registry 的值为 `all_19_frozen_predicates_reviewed`，source audit 写“均具有完成的学术资格审查”和“所有记录都已完成核验”，但同一证据库明确写明 EFSM 四类是二手归属、Hierons/Kuhn 未独立复核，Fabbri 相关全文未取到，另有仅核书目的来源。文档没有把 registry eligibility、文献存在性核验、全文逐字核对和协作核验分开。该措辞会让论文读者把不一致的证据等级误读成 19 个 predicate 均已独立学术验证。

Basis：逐项对照 registry status、source catalog 字段、`CURRENT_SOURCE_AUDIT.md` 总结和 `defect_taxonomy.md` 的 evidence-level notes；未补充外部文献结论。

复算命令：

```bash
jq '{registry_version,status,academic_eligibility,academic_priority,source_audit_path,source_catalog_path}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/predicate_registry.json
rg -n '均具有完成|所有记录都已完成|二手归属|未独立复核|全文未取到|仅核书目' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/related_work/provenance/CURRENT_SOURCE_AUDIT.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/defect_taxonomy.md
```

Disposition：`required disclosure`。保留 frozen registry identity，但将 status 分成“mapping/eligibility decision”“bibliographic verification”“full-text/source review”三层，并在 final report/README 中链接该分级证据；不要删掉现有局限说明。

Targeted rereview：`FAIL / not rerun`。主 session 改过 archive SCHEMA 的 evidence-gap 说明，但尚未修正 source-audit 的完成性声称或为 19 predicates 建立可核查的分级表。

### ACAD-16-005 [M] Issue #189 has no repository-local source snapshot

路径：`discover_matrix/docs/protocol/dtier_triage.md:5,12-28`；`discover_matrix/docs/protocol/semantic_judge_protocol.md:40-57`；`semantic_judge_issue_195.snapshot.md:3-15`。

Reason：issue `#195` 有正文快照、抓取时间和 SHA-256；D/A 规则仍主要引用外部 issue `#189` §1.3.3 和外部 gist `D_PROTOCOL.md`。仓库内 `protocol_freeze_v2.md` 是当前人工评测的操作化冻结，不是 `#189` 原文。读者可以离线复核当前 v2 规则，但不能仅靠仓库完整核验“该规则来自 #189 原文及其出处表”。

Basis：`find` 未找到 issue-189 snapshot 或 `D_PROTOCOL.md`；逐行读取两个协议入口及 issue #195 snapshot metadata。没有把外部链接当作仓库内已核验事实。

复算命令：

```bash
find project_1_llm_state_machine_modeling/paper_stm_issue_discover -type f \( -name 'D_PROTOCOL.md' -o -iname '*issue*189*' \) -print
rg -n '#189|D_PROTOCOL|gist|snapshot|SHA-256' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/dtier_triage.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md
```

Disposition：`disclose`。若政策允许且原文可保存，新增 hash-closed #189 snapshot；否则在当前协议入口明确 external-source dependency，并明确 `protocol_freeze_v2.md` 是本项目操作化冻结，不冒充 issue 原文。

Targeted rereview：`FAIL / not rerun`。现有链接仍为外部依赖，未增加本地快照或明确披露“不可离线复核原文”的边界。

### ACAD-16-006 [I] Archive and publication manifests do not cover the current release surface

路径：`final_results/v60_current_vs_x1v2_baseline/archive_manifest.json`、`publication_manifest.json`；manifest validator `evaluation/src/paper_stm_evaluation/final_results_archive.py:805-841`。

Reason：当前 top-level `archive_manifest.json` 仍是 `2674` files、`generated_at_utc=2026-08-28T19:17:53+00:00`，其中 `README.md`/`SCHEMA.md` 仍是旧 bytes/hash，且不包含 `derived/manual_adjudication_v2/` 或 `reviews/16_academic_targeted_rereview.md`。`publication_manifest.json` 为 `2675` files，同样对 manual v2 和本 review 计数为 0。archive validator 实际失败为 `ValueError: manifest mismatch`，首先指出当前 README。

Basis：读取两份 manifest 的 `included_files`、当前文件 hash，并运行 archive validator；manual validator/recompute 的 PASS 不能替代 archive-level manifest closure。

复算命令：

```bash
jq '{included_count:(.included_files|length),manual_v2:([.included_files[]|select(.path|startswith("derived/manual_adjudication_v2/"))]|length),review16:([.included_files[]|select(.path=="reviews/16_academic_targeted_rereview.md")]|length)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/archive_manifest.json \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/publication_manifest.json
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
  venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

Disposition：`required fix`。在所有当前文档、canonical JSON/TSV、schema 和 review 文件稳定后重新生成 archive/publication manifest，逐项检查 hash；不得把 proposal-only/cache/temporary `runs/` 纳入发布面。

Targeted rereview：`FAIL`。本轮实际 validator failure 为 `manifest mismatch: .../README.md`；两份 manifest 均未覆盖 manual v2 或本文件。

### ACAD-16-007 [M] Frozen Judge v3.2 and current implementation v3.3 are not explicitly mapped in the final archive entry

路径：冻结 raw composite `protocol_version`/`judge_algorithm_version`/`semantic_judge_commit`；`discover_matrix/docs/protocol/semantic_judge_protocol.md:17-25,59-74`；final archive `README.md:3-6,38-53`、`SCHEMA.md:1-6`。

Reason：raw 明确为 `semantic-judge.two-stage.v3.2` 和 commit `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`，协议入口声明后续实现版本 `semantic-judge.two-stage.v3.3`。协议第 73-74 行现在把 v3.3 运行协议称为历史 Judge 工具协议，但 final archive README/SCHEMA 只写“旧 Judge v3.2”，没有在 archive entry 中说明 v3.3 是后续 evaluator implementation、不是冻结 raw 的结果来源。读者从主入口无法直接确认这两个版本的 provenance 边界。

Basis：`jq` 读取两侧 frozen composite version fields，`rg` 读取当前 protocol constants 和 archive entry；未把源码版本回填 raw。

复算命令：

```bash
jq '{protocol_version,judge_algorithm_version,semantic_judge_commit}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/v60_current/judge/composite/summary.json \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/judge/composite-summary.json
rg -n 'semantic-judge.two-stage.v3\.[23]|历史 Judge|后续|implementation' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/SCHEMA.md
```

Disposition：`required disclosure`。在 final archive README/SCHEMA 加一条明确映射：v3.2 + frozen commit 是 raw result identity；v3.3 是后续 evaluator/protocol implementation，不产生或重命名本归档结果。

Targeted rereview：`FAIL / not rerun`。协议自身已有历史化说明，但 final archive entry 尚未写出 v3.3 的角色映射。

### ACAD-16-008 [M] Field-level paired-input fairness disclosure remains incomplete

路径：`discover_matrix/docs/protocol/semantic_judge_protocol.md:97-120`；`evaluation/src/paper_stm_evaluation/judge_input_projection.py:24-76,275-356`；`judge/src/paper_stm_judge/artifacts.py:633-680,853-868`；`reference/x1v2_input_closure/manifest.json`；报告 `report/v60_current_vs_x1v2_baseline_cn.md:64-72`。

Reason：协议仍概括为两侧进入“完全相同”的 `UnifiedJudgeInput` 和公共 artifact closure。代码显示 adapter 前的 source surface 不同：current 读取 `report_issue_clusters`，X1v2 读取 `parsed_output.issues`；X1v2 closure manifest 的 inputs 是 54 个 pair 各自的 hash-verified NL/PlantUML，而 current method record 还包含 canonical/FCSTM/native/inspection/working-contract/source-trace 等 method-owned evidence。当前报告和 reviewer projection 已正确说明 baseline predicate usage=`not_applicable`，但没有 field-level 表列出 shared、arm-specific 和 not_applicable，容易把“统一 judge schema”误读为“两侧原始证据完全同构”。

Basis：直接读取 adapter、`build_unified_input`、两侧 raw record key、X1v2 input closure manifest、reviewer projection policy 和报告；没有把 current predicate receipt 当成 baseline 必需条件，也没有用 later Judge 证据升级 baseline W2。

复算命令：

```bash
rg -n 'report_issue_clusters|parsed_output\.issues|UnifiedJudgeInput|完全相同|not_applicable|predicate' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/judge/src/paper_stm_judge/artifacts.py \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src/paper_stm_evaluation/judge_input_projection.py \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md
jq '{schema,pair_count,input_type:(.inputs|type),pair_ids:(.inputs|keys|length),sample:(.inputs["0000"]//null)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/x1v2_input_closure/manifest.json
```

Disposition：`required disclosure`。增加 field-level paired-input table，明确 shared fields、arm-specific source/artifact fields、baseline predicate `not_applicable`、人工 relation adjudication 才读取 ledger，以及 later Judge 不参与 method W2。

Targeted rereview：`FAIL / not rerun`。主 session 已补 baseline `not_applicable` 和 reviewer projection 说明，但 protocol 的“完全相同”表述和 final report 均缺 field-level mapping。

### ACAD-16-009 [I] Newly added manual-v2 links are broken from the protocol directory

路径：`discover_matrix/docs/protocol/semantic_judge_protocol.md:61-63`；`discover_matrix/docs/protocol/verdict_methodology.md:13-16`。

Reason：两处链接写为 `../../final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/README.md`。从 `discover_matrix/docs/protocol/` 解析时，该路径落到 `discover_matrix/final_results/...`，而实际目标在其上一级的 `paper_stm_issue_discover/final_results/...`，需要 `../../../final_results/...`。这会阻断读者从 issue #195 协议入口进入当前人工结果。

Basis：逐条解析 Markdown link target，并用 filesystem existence check 验证；正确的三级路径存在，当前两级路径不存在。

复算命令：

```bash
test -e project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/../../final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/README.md; printf 'two-level rc=%s\n' "$?"
test -e project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/../../../final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/README.md; printf 'three-level rc=%s\n' "$?"
```

Disposition：`required fix`。修正两个 Markdown target 后运行全仓库/论文工作区 local-link checker；不涉及 raw 或 canonical data。

Targeted rereview：`FAIL / not rerun`。本轮 existence check 为 two-level `rc=1`、three-level `rc=0`。

## Final disposition

已关闭：ACAD-16-001、ACAD-16-002（工作区修复，尚无 commit）。

未关闭：ACAD-16-003、ACAD-16-004、ACAD-16-006、ACAD-16-009（I）；ACAD-16-005、ACAD-16-007、ACAD-16-008（M）。当前 academic targeted rereview 为 `FAIL`，不是因为缺少另一位真人，而是因为上述文档、来源证据和 manifest/link 问题仍有可复核证据。所有 finding 均有专属 reason、basis、路径和复算命令；本文件不修改 frozen raw、registry、predicate semantics、Judge artifact 或 canonical decisions。

## Latest targeted rereview (2026-08-29)

身份仍为 `subagent/LLM proposal`，仅供主 session 记录和处置；本节不是真人签署，不设置 `human_confirmation`，不修改 canonical decisions、frozen raw、registry 或 source catalog。以下结果以本节为最新状态；上文较早一轮的 008/009 状态不再作为最终 disposition。

### 独立核对的 19-predicate provenance mapping

下表直接由冻结 `reference/predicate_registry.json` 和 canonical `derived/manual_adjudication_v2/predicate_source_provenance.json` 对拍得到。每个 predicate 有 3 条 source-provenance edge，共 `19/19` predicate rows、`57` edges；source catalog 有 `28/28` 个可解析 ID。

| family | predicate | source catalog IDs |
| :-- | :-- | :-- |
| S | S1 | ST1, ST2, ST4 |
| S | S2 | ST1, ST2, ST4 |
| S | S3 | ST1, ST2, ST5 |
| S | S4 | ST1, ST3, ST7 |
| S | S5 | ST1, ST2, ST3 |
| S | S6 | ST1, ST2, ST9 |
| G | G1 | TP1, TP2, ST3 |
| G | G2 | TP2, TP3, TP4 |
| G | G3 | TP3, TP3B, TP3C |
| G | G4 | TP6, G4-RP1, G4-RP2 |
| R | R1 | TR1, TR2, ST8 |
| R | R2 | TR1, TR2, ST3 |
| R | R3 | TR1, TR2, ST8 |
| R | R4 | TR4, TR5, TR6 |
| V | V1 | BV4, BV5, BV6 |
| V | V2 | BV4, BV5, BV6 |
| V | V3 | TP1, BV7, TR1 |
| V | V4 | BV8, BV7, BV9 |
| V | V5 | TP3, TP3B, TP3C |

Evidence limitation: `reference/current_source_catalog.json` actually exposes only `id/types/title/paths/supports/boundary`; it does not expose authors, year, venue, bibliography, DOI/stable link or access date. In the 57 canonical provenance edges, `bibliography`, `doi_or_stable_link` and `accessed_at` are all null/empty (`57/57` each). The catalog therefore proves identity mapping, support text and boundary, but not a complete bibliography/full-text audit for every edge. The repository's inline bibliography also records secondary attribution, unindependently checked sources and unavailable full text; those qualifications cannot be erased by the mapping table.

### Latest dispositions

Overall result: `FAIL` (`C=0`, `I=4`, `M=3`). The result is an academic review proposal, not an adjudicator sign-off.

#### ACAD-16-003 [I] Predicate provenance is not bibliography/full-text closed

Evidence: `final_results/v60_current_vs_x1v2_baseline/reference/predicate_registry.json`; `reference/current_source_catalog.json`; `derived/manual_adjudication_v2/predicate_source_provenance.json`; `related_work/provenance/CURRENT_SOURCE_AUDIT.md:3-9,13-20`; `discover_matrix/docs/protocol/defect_taxonomy.md:62,668-706`.

Reason: identity and `supports/boundary` closure passes, but all 57 edges lack the required bibliographic and access metadata. Existing bibliography prose cannot be promoted to a complete machine provenance record, and titles/paths are not evidence for missing fields.

Command/evidence pointer:

```bash
jq '{registry_version,public_predicate_count,family_counts}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/predicate_registry.json
jq '{sources:(.sources|length),source_keys:([.sources[]|keys]|unique)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/reference/current_source_catalog.json
jq '{predicate_rows:(.rows|length),source_rows:([.rows[].source_provenance[]]|length),missing_bibliography:([.rows[].source_provenance[]|select((.bibliography//"")=="")]|length),missing_link:([.rows[].source_provenance[]|select((.doi_or_stable_link//"")=="")]|length),missing_access:([.rows[].source_provenance[]|select((.accessed_at//"")=="")]|length)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/predicate_source_provenance.json
```

Disposition: `FAIL; required fix or explicit claim downgrade`. Do not alter frozen registry semantics. Either add independently checked source metadata and claim-level support, or downgrade academic provenance claims to the recorded mapping/evidence level and preserve the gaps.

Targeted rereview: `FAIL`. The counts and all 19 mappings were rechecked in this pass; metadata remains missing, so no closure claim is accepted.

#### ACAD-16-004 [I] Verification prose exceeds the evidence level

Evidence: `reference/predicate_registry.json` has `academic_eligibility=all_19_frozen_predicates_reviewed`; `related_work/provenance/CURRENT_SOURCE_AUDIT.md:3,20` says the records are completed/verified, while `CURRENT_SOURCE_AUDIT.md:5-9` and `discover_matrix/docs/protocol/defect_taxonomy.md:62,668-706` disclose missing metadata, secondary attribution, unindependent checks and unavailable full text.

Reason: “mapping/eligibility decision”, bibliographic existence, independent full-text reading and source-level claim verification are different academic claims. The current unqualified wording collapses them and overstates what the frozen files establish.

Command/evidence pointer:

```bash
rg -n '均具有完成|所有记录都已完成|二手归属|未独立复核|全文未取到|仅核书目' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/related_work/provenance/CURRENT_SOURCE_AUDIT.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/defect_taxonomy.md
```

Disposition: `FAIL; required disclosure`. Split the evidence levels in the prose and link the audit limitations; preserve the frozen registry identifier.

Targeted rereview: `FAIL`. The contradictory wording and limitations remain in the working tree.

#### ACAD-16-005 [M] Issue #189 remains an external-source dependency

Evidence: no repository-local `D_PROTOCOL.md` or issue-189 snapshot was found under `project_1_llm_state_machine_modeling/paper_stm_issue_discover/`; `discover_matrix/docs/protocol/dtier_triage.md:5,12-28` and `semantic_judge_protocol.md:40-57` cite #189/D_PROTOCOL externally. In contrast, `discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md` exists and hashes to `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`.

Reason: the local `protocol_freeze_v2.md` is an operational project freeze, not the original #189 text. The current rule is locally readable, but the provenance of the cited issue cannot be fully checked offline.

Command/evidence pointer:

```bash
find project_1_llm_state_machine_modeling/paper_stm_issue_discover -type f \
  \( -name 'D_PROTOCOL.md' -o -iname '*issue*189*' \) -print
sha256sum project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md
```

Disposition: `FAIL; disclose external dependency`, or add a hash-closed #189 snapshot only if its original bytes can be obtained and provenance recorded. Do not label the operational freeze as the issue snapshot.

Targeted rereview: `FAIL`. The absence and the external citations were rechecked; no #189 local snapshot is present.

#### ACAD-16-006 [I] Release manifests are stale

Evidence: `final_results/v60_current_vs_x1v2_baseline/archive_manifest.json` and `publication_manifest.json` still describe the earlier file set and omit `derived/manual_adjudication_v2/` and this review. Their declared README/SCHEMA hashes do not match the current bytes. The archive validator fails at manifest mismatch before release closure.

Command/evidence pointer:

```bash
jq '{included_count:(.included_files|length),manual_v2:([.included_files[]|select(.path|startswith("derived/manual_adjudication_v2/"))]|length),review16:([.included_files[]|select(.path=="reviews/16_academic_targeted_rereview.md")]|length)}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/archive_manifest.json \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/publication_manifest.json
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
  venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

Disposition: `FAIL; required fix`. Regenerate both manifests only after release files are stable, then verify every included-file hash. This review does not authorize adding proposal-only or temporary files.

Targeted rereview: `FAIL`. The validator still reports manifest mismatch and the two manifests still omit the current review surface.

#### ACAD-16-007 [M] Frozen Judge v3.2 and later v3.3 implementation are not mapped at the archive entry

Evidence: both frozen composite summaries identify `semantic-judge.two-stage.v3.2` and commit `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`; `discover_matrix/docs/protocol/semantic_judge_protocol.md:17-25,59-74` describes `semantic-judge.two-stage.v3.3`; final archive `README.md:3-6,38-53` and `SCHEMA.md:1-6` only name the old v3.2 Judge.

Reason: readers need an explicit provenance boundary: v3.2 plus its frozen commit identifies the archived raw result; v3.3 is a later evaluator/protocol implementation and must not be read as the generator of, or a relabeling of, the frozen result.

Command/evidence pointer:

```bash
jq '{protocol_version,judge_algorithm_version,semantic_judge_commit}' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/v60_current/judge/composite/summary.json \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/judge/composite-summary.json
rg -n 'semantic-judge.two-stage.v3\.[23]|历史 Judge|后续|implementation' \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/SCHEMA.md
```

Disposition: `FAIL; required disclosure` in final archive README/SCHEMA. No raw or Judge artifact change is needed.

Targeted rereview: `FAIL`. The protocol has a partial historical note, but the archive entry still lacks this explicit v3.2/v3.3 mapping.

#### ACAD-16-008 [M] Field-level paired-input fairness disclosure

Evidence: `evaluation/src/paper_stm_evaluation/judge_input_projection.py:24-76,275-356`, `judge/src/paper_stm_judge/artifacts.py:633-680,853-868`, `reference/x1v2_input_closure/manifest.json`, `discover_matrix/docs/protocol/semantic_judge_protocol.md:76-120`, and `report/v60_current_vs_x1v2_baseline_cn.md:64-72`.

Reason: the adapter makes the Judge schema uniform, but the pre-adapter source surfaces are not identical: current uses `report_issue_clusters` and method-owned artifacts; X1v2 uses `parsed_output.issues` and its hash-verified NL/PlantUML closure. Current predicate receipts are arm-specific, while baseline predicate usage must be `not_applicable`; later Judge evidence cannot raise baseline W. The current working-tree protocol/report now state this field-level distinction and the baseline `not_applicable` status.

Disposition: `PASS; disclosure accepted in working tree`.

Targeted rereview: `PASS`. Re-read protocol lines 76-95 and report lines 64-72, and confirmed the field-level mapping/baseline `not_applicable` language. The generic unified-schema statement at lines 116-120 is acceptable when read with that mapping, but must not be cited without it.

#### ACAD-16-009 [I] Protocol manual-v2 links

Evidence: re-resolved the manual-v2 links in `discover_matrix/docs/protocol/semantic_judge_protocol.md` and `verdict_methodology.md` against the filesystem. They now use `../../../final_results/v60_current_vs_x1v2_baseline/...`, which resolves from `discover_matrix/docs/protocol/` to the actual final archive.

Disposition: `PASS; fixed in working tree`.

Targeted rereview: `PASS`. The two-level target is absent as expected and the three-level target exists. A full link checker is still needed for release, but this specific finding is closed.

#### ACAD-16-010 [I] Final archive README has a broken protocol link

Evidence: `final_results/v60_current_vs_x1v2_baseline/README.md:64` uses `../../../discover_matrix/...`. From the final archive root that resolves one directory above `paper_stm_issue_discover`, while the protocol is at `../../discover_matrix/...`; the analogous three-level path in the deeper formal report is valid because that report is one directory deeper.

Command/evidence pointer:

```bash
test -e project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/../../../discover_matrix/docs/protocol/semantic_judge_protocol.md; printf 'README target rc=%s\n' "$?"
test -e project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/../../discover_matrix/docs/protocol/semantic_judge_protocol.md; printf 'correct target rc=%s\n' "$?"
```

Disposition: `FAIL; required fix`. Change only the Markdown target, then rerun the local-link checker; no canonical or frozen data change is implicated.

Targeted rereview: `FAIL`. Filesystem resolution gives the current README target `rc=1` and corrected target `rc=0`.

#### ACAD-16-011 [M] #195 protocol versus manual-v2 publication extension is not explicitly versioned

Evidence: `discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md:3-5,20-31` describes the historical published Judge view (including the D2/D1 release framing and old report-level K/N/I semantics). `derived/manual_adjudication_v2/protocol_freeze_v2.md` and `README.md` add raw-first all-report D0/A0 review and the publication-unit composition `K_hit/N_group/I_group`.

Reason: this is a legitimate versioned evaluation extension, but a reader could mistake the issue snapshot's historical release universe for the current manual-v2 publication universe. The current documents must say explicitly that v2 re-evaluates all reports, includes D0/A0 as final I under the frozen closure, and derives the operational K/N/I publication units without mixing them with the old Judge headline.

Disposition: `FAIL; required disclosure`. Add a short version boundary in the protocol/report and keep the old #195 snapshot as historical evidence. Do not rewrite the issue snapshot.

Targeted rereview: `FAIL / not rerun`. The current alignment text does not yet make this extension explicit enough.

### Shuorenhua and review-process record

The `shuorenhua` skill was read in full before this review. Scenario: `docs + README`; modes: `minimal + audit-only`. Pass 1 checked protected spans (versions, issue IDs, hashes, paths, commands, metrics/denominators, enums, predicate IDs, ownership and causal wording) against source files. Pass 2 checked residual AI-template phrasing, unsupported academic claims, terminology drift, first-screen navigation and local links. No protected span was rewritten by this review. The remaining unsupported claims and link/manifest defects are recorded as findings above rather than normalized away.

### Review conclusion

`FAIL`: ACAD-16-003, ACAD-16-004, ACAD-16-006 and ACAD-16-010 remain `I` findings; ACAD-16-005, ACAD-16-007 and ACAD-16-011 remain `M` findings. ACAD-16-008 and ACAD-16-009 targeted rereviews pass. This proposal supplies evidence paths and commands for the main session's disposition; it does not represent a human adjudicator signature and does not authorize ready/complete.

### Repair-commit accounting

This was a read-only `subagent/LLM proposal`. It produced no repair commit. PASS dispositions refer to fixes already present in the working tree; every FAIL disposition remains an explicit required fix or disclosure for the owning main session. No frozen raw, canonical decision, registry, source catalog or Judge artifact was changed by this review.

## Final post-fix academic rereview (2026-08-29)

身份：`subagent/LLM proposal`，只读 academic review。没有调用 provider，没有修改 frozen raw、canonical decisions、Judge artifact、registry 或 source catalog；本节不设置真人签名字段。结论以本节为最新状态，覆盖前文对 provenance metadata 的较早读取。

### Evidence ledger

- `reference/predicate_registry.json` 与 `method/src/paper_stm_method/resources/predicate_registry.json` SHA-256 均为 `38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca`。
- 三份 `current_source_catalog.json`（final reference、method resources、related-work provenance）SHA-256 均为 `45ee60a378cb192ec364f1ee563e5ce8fb9cb8f79a4ed71dc8869049806a5647`。
- registry/provenance 对拍为 `19` predicates、`57` edges、`28` catalog IDs，边集合完全相等且全部 ID 可解析；完整 19 行 mapping 见本文件 lines 242-262。
- canonical `predicate_source_provenance.json` 当前 `bibliography` 缺失 `57/57`、`doi_or_stable_link` 缺失 `57/57`，但 `accessed_at` 已有 `2026-08-29`（缺失 `0/57`）。因此前文把 accessed date 也记为 `57/57` 缺失的陈述在本节被更正；bibliography/stable-link gap 仍然存在。
- issue #195 snapshot 为 `discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md`，SHA-256 为 `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`。仓库内仍没有 #189 原文 snapshot 或 `D_PROTOCOL.md`。

### Protocol and scope assessment

`PASS`：manual-v2 的主协议边界在 `derived/manual_adjudication_v2/README.md:9-12,38-46`、`SCHEMA.md:41-78` 和正式报告 `report/v60_current_vs_x1v2_baseline_cn.md:7-13,45-62` 中是清楚的：先作者源事实，再 D/A，再逐 expected relation；`D0/A0 -> INVALID -> I`，`D2/D1` 依据 FULL/PARTIAL 或全 NO 派生 K/N；PARTIAL 不进入主 hit 或 FP；W 独立于 validity/relation/hit/FP；N/I 只在同 side、同 pair 跨 round 合并。`hit@1/@3/@all`、L2、W-on-hits 和 W2/all-expected 的分母也在报告 lines 19-43、62-74 中分别给出。未发现把 W、L、predicate usage 或 method self-reported label 当作 validity gate 的新表述。

`PASS`：双侧输入公平性披露在 `discover_matrix/docs/protocol/semantic_judge_protocol.md:76-95`、final archive `README.md:60-64` 和正式报告 `report/v60_current_vs_x1v2_baseline_cn.md:11` 中已到字段级。两侧共享 NL/PlantUML、raw pointer/hash 和 claim/reason/location allowlist；current 的 predicate/receipt 与 baseline 缺失字段不填零；baseline predicate usage 为 `not_applicable`，不把 later Judge 能力倒灌为 baseline W2。

`PASS`：旧 Judge 与 manual-v2 的版本边界已在 final archive `README.md:3-10`、`SCHEMA.md:3-10`、manual README `:3-7,48-53` 和 protocol `semantic_judge_protocol.md:59-74` 明确写出。冻结 raw 的 v3.2 是历史输入/输出身份，v3.3 是后续 evaluator/protocol implementation，manual-v2 才是论文人工监督结果来源。protocol links 从 `discover_matrix/docs/protocol/` 和 final archive root 的文件系统解析均通过。

`FAIL`：协议条款矩阵仍有一处读者歧义。`semantic_judge_protocol.md:113-120` 在未标注“历史 v3.3 Judge contract”的 `#195 合同`表中写着“D2+D1 是唯一发布集合；D0 不进入 Judge”，而同一文件 `:59-74` 和 manual-v2 `README.md:3-7,38-46` 将当前人工评测定义为全量报告并把 D0/A0 闭合为 I。`semantic_judge_protocol.md:73-74` 的历史说明可以消解一部分歧义，但表格行本身仍可能被当前读者当作 active manual-v2 rule。

Finding `ACAD-17-002 [M]`：将该表行显式标为 historical v3.3/Judge-only，或与 manual-v2 当前合同分成两个标题。Repair：文档-only，不能改 issue snapshot 或 canonical data。Targeted rereview：`FAIL`，本次复读仍在 lines 118 与 59-74 看到该未标注冲突。

### Findings and dispositions

#### `ACAD-16-003 [I]` remains FAIL: provenance is mapping-closed, not bibliography-closed

Evidence: `reference/predicate_registry.json`、`reference/current_source_catalog.json`、`derived/manual_adjudication_v2/predicate_source_provenance.json:1` and `related_work/provenance/CURRENT_SOURCE_AUDIT.md:3-9,13-20`。registry/source/provenance identity closure is `19/19`, `28/28`, `57/57`; however the source catalog schema is only `id/types/title/paths/supports/boundary`, and canonical provenance still has no bibliography or DOI/stable-link value on any of 57 edges. Existing `defect_taxonomy.md:668-706` explicitly distinguishes full-text, bibliography-only and unindependently checked sources; it cannot be replaced by source-title matching.

Repair/disposition: `FAIL; required fix or explicit claim downgrade`. Add only independently verified metadata, or state that the frozen evidence supports source mapping/support/boundary rather than complete literature provenance. Do not invent DOI, authors, venue or year. Targeted rereview: `FAIL`; the updated access date does not close the two remaining fields.

#### `ACAD-16-004 [I]` remains FAIL: academic verification wording is still ungraded

Evidence: `related_work/provenance/CURRENT_SOURCE_AUDIT.md:3,5-9,20` says mapping limitations are present but also says “所有记录都已完成核验”; `discover_matrix/docs/protocol/defect_taxonomy.md:62,668-706` records secondary attribution, unavailable full text and unindependent checks. The registry value `academic_eligibility=all_19_frozen_predicates_reviewed` is not by itself evidence of independent full-text verification.

Repair/disposition: `FAIL; required disclosure`. Separate mapping/eligibility, bibliographic existence and independent source-text verification in the current academic prose. Targeted rereview: `FAIL`; line 20 remains unchanged.

#### `ACAD-16-005 [M]` remains FAIL: #189 is not locally reproducible

Evidence: filesystem search under `project_1_llm_state_machine_modeling/paper_stm_issue_discover/` returns no `D_PROTOCOL.md` or issue-189 snapshot. `discover_matrix/docs/protocol/dtier_triage.md:5` and `semantic_judge_protocol.md:40-57` still use the external #189/gist dependency, while the #195 snapshot is local and hash-closed.

Repair/disposition: `FAIL; disclose external dependency`, or add a hash-closed #189 snapshot only when the original bytes and provenance are actually available. Do not present `protocol_freeze_v2.md` as the #189 source. Targeted rereview: `FAIL`; no local #189 source was found.

#### `ACAD-16-006 [I]` remains FAIL: release manifest closure is not clean

Evidence: top-level `archive_manifest.json` and `publication_manifest.json` each include 2835/2836 paths but have `21` content-hash mismatches, including `derived/manual_adjudication_v2/MANIFEST`, canonical manual outputs, report and review files. The archive validator fails at `derived/manual_adjudication_v2/MANIFEST` with `ValueError: manifest mismatch`; the internal manual MANIFEST's own 76 canonical file hashes currently match, so the failing boundary is the stale top-level release manifest entry.

Command:

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
  venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

Repair/disposition: `FAIL; regenerate top-level manifests after all release files, including this review, are stable`. Targeted rereview: `FAIL`, validator rc `1`; no raw change is implicated.

#### `ACAD-17-001 [I]` Final archive README numbers disagree with canonical summary

Evidence: final archive `README.md:33-35` reports v60 D/A `724/257/121/169`, K/N/I `750/231/290`, ledger `119/121/187`, report precision `981/1271`; it reports baseline D/A `410/0/0/102`, K/N/I `276/134/102`, ledger `104/134/102`, precision `410/512`. Canonical `derived/manual_adjudication_v2/summary.json:1` and formal report `report/v60_current_vs_x1v2_baseline_cn.md:21-57` instead establish:

- v60 D/A `721/259/120/171`, K/N/I `749/231/291`, ledger `K_hit/N_group/I_group=119/121/189`, report precision `980/1271`;
- X1v2 D/A `408/3/2/99`, K/N/I `279/132/101`, ledger `104/132/101`, report precision `411/512`.

The sums still close, but the README is not a faithful current summary and its claim “数值从 canonical JSON 离线重算” at `README.md:30` is contradicted by these values.

Repair/disposition: `FAIL; replace README:33-35 from canonical recompute output and regenerate manifests`. Do not change canonical decisions to match the README. Targeted rereview: `FAIL`; the mismatch was reproduced by reading summary JSON and report side by side.

### Final review result

Overall: `FAIL` (`C=0`, `I=4`, `M=2`). PASS: manual-v2 D/A/KNI/W/grouping semantics, field-level paired-input disclosure, v3.2/v3.3 archive boundary and corrected protocol links. FAIL: `ACAD-16-003`, `ACAD-16-004`, `ACAD-16-005`, `ACAD-16-006`, `ACAD-17-001` and `ACAD-17-002` as detailed above. The counts are reported as four I and two M because `ACAD-16-005` and `ACAD-17-002` are M; the remaining four are I. This is a read-only proposal; no repair commit was produced.

### Shuorenhua reread record

Scenario: `docs + README`; mode: `minimal + audit-only`; annotation/review mode. Pass 1 protected versions, issue IDs, hashes, paths, commands, metrics, denominators, enum names, predicate IDs and responsibility/causal relations. Pass 2 checked residual narrator language, unsupported academic claims, terminology drift, current-first navigation and local links. The review preserves formal identifiers and reports unsupported claims as evidence gaps rather than silently rewriting them. No canonical or frozen file was modified.
