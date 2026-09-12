# Artifact targeted rereview

**身份**：`subagent:artifact-reviewer`；本文件是独立 proposal/review，不是人工语义裁定，也不修改 canonical decision 或 frozen raw。

**复核时间**：`2026-08-29T17:38:06+08:00`

**结论**：`FAIL`。冻结 raw 本身的 manifest hash 未变，当前 JSON/TSV 和 dense relation 的机械规模闭合可见；但当前 canonical inventory/MANIFEST 的输入 hash 已落后于顶层 manifest，导致专用 manual validator 当前不能通过。canonical 目录也尚未被 Git 跟踪。不能把本次 artifact review 标为 PASS。

## 检查范围

只读检查了：

- `raw/v60_current/archive_manifest.json`、`raw/x1v2_baseline/archive_manifest.json` 及 raw 文件 hash；
- `derived/manual_adjudication_v2/inventory.json`、canonical JSON/TSV、`relation_decisions.json`、`hit_max_witness.json`、`group_decisions.json`；
- `derived/manual_adjudication_v2/MANIFEST`；
- 顶层 `archive_manifest.json`、`publication_manifest.json`；
- archive 内 Markdown 链接及 provider-free validator。

未读取旧 artifact review 结论，未调用 provider，未运行 method/Judge，也没有修改 `raw/` 或 canonical JSON/TSV。

## 通过项

1. Raw archive manifest hash 当前为：
   - v60/current：`sha256:8c2105dd7025f360500709e25ac9b483b907fdd91a3c39144798158ca1a25ba0`
   - X1v2 baseline：`sha256:8e9fa28071ba4acbbc0483c5ba84029ac69e7d0a618311ec85f7992081b374d0`
   当前 `git diff --numstat -- final_results/v60_current_vs_x1v2_baseline/raw` 为 `0`，raw status 行数为 `0`。
2. `inventory.json` 记录的规模为 `162/162` cells、`1271/512` reports/findings，分轮为 v60 `415/446/410`、X1v2 `173/163/176`。
3. canonical report decision 文件当前分别有 `1271` 和 `512` 条；TSV 文件存在。`relation_decisions.json` 有 `258535` 行，`(side, report_id, expected_id)` 唯一键也是 `258535`；关系计数为 `FULL_MATCH=953`、`PARTIAL_MATCH=386`、`NO_MATCH=257196`。每条 decision 的 nested relation 数为 `145`，两侧合计行数与 `(1271+512)*145` 一致。
4. `hit_max_witness.json` 有 `870` 条（两侧各 `435`），`group_decisions.json` 有 `544` 条（v60 `308`、X1v2 `236`）。这些是结构计数，不替代最终语义正确性。
5. 在顶层 manifest 更新后的当前快照上，以下命令通过：

   ```bash
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=evaluation/src \
   python -m paper_stm_evaluation.final_results_archive validate \
     --archive-root final_results/v60_current_vs_x1v2_baseline \
     --repository-root /home/zhangshaoang/oo-projects/research_ideas
   ```

   在本文件写入之前，输出为：`final-results archive validation passed`。archive-scoped Markdown link check 也为 `0` 条失效引用。

   本文件写入后再次运行同一 archive validator，当前失败于 `reviews/14_artifact_targeted_rereview.md` 的 manifest hash。这是 review 文件加入/更新后尚未重新生成顶层 manifest 的直接结果，不能把写入前的 PASS 当作当前 PASS。

## Findings

### ART-001 [I] FAIL: canonical input hashes 与当前顶层 manifests 不一致

**路径/行号**：

- `derived/manual_adjudication_v2/inventory.json` 的 `source_manifests`；文件为单 JSON 对象，当前 `generated_at_utc` 为 `2026-08-29T03:09:25+00:00`；
- `derived/manual_adjudication_v2/MANIFEST` 第 1 行的 `raw_input_hashes`；
- `archive_manifest.json`、`publication_manifest.json` 的 `generated_at_utc` 分别为 `2026-08-29T09:32:52+00:00`、`2026-08-29T09:32:54+00:00`。

**Reason**：inventory 和 manual MANIFEST 仍引用旧的顶层 hash：`archive_manifest.json=sha256:93e31be21628b5ae6343d47ec4b7ecf228ef5bf19a6cb58bd1dde40838a6cfce`、`publication_manifest.json=sha256:b0d494bae61635fba3763ed796393d305e85f7559f0e5f72c2a9ef2e0189e56d`；当前文件实际 hash 已为 `sha256:1c88343f854ef0019c6f1e29c81c898272568422f2b4e18fbef395cfe1033289`、`sha256:ab93ecbe0aee265f6ff5ecb74cf761520fbbccaeed06b1be5791146d47c6df78`。raw 两侧 hash 仍与记录一致，但 canonical 输入闭包不再自洽。

**Basis / 复算命令**：

```bash
sha256sum raw/v60_current/archive_manifest.json \
  raw/x1v2_baseline/archive_manifest.json archive_manifest.json publication_manifest.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=evaluation/src \
python scripts/evaluation/validate_manual_adjudication.py \
  --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

当前第二条命令失败于 `validate_raw_inventory`：`ValueError: inventory does not equal a fresh enumeration of the frozen archive`。独立比较 fresh inventory 与存档 inventory 显示差异位于 `source_manifests`，其余冻结规模仍为 `162/162`、`1271/512` 和相同分轮计数。该失败发生在 pointer/W2/TSV 后续检查之前，因此本快照不能声称专用 validator 的完整闭合已通过。

**Disposition**：`FAIL / fix-required`。主 session 必须在顶层 manifests 稳定后 provider-free 重建 `inventory.json` 和 `MANIFEST` 的输入 hash，再重新运行 manual validator，并保存新的 hash。不能通过手填或沿用旧 hash 修复。

**修复 commit**：无；本 reviewer 只读，未实施修复。

**Targeted rereview**：未通过。修复后重新运行上述两条命令，并重新核对 raw manifest hash；在该复核完成前，ART-001 保持 FAIL。

### ART-002 [I] FAIL: canonical manual-adjudication 目录尚未进入 Git

**路径/证据**：`derived/manual_adjudication_v2/`；`git ls-files final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2 | wc -l` 输出 `0`，对应 `git status --untracked-files=all` 输出 `142` 条未跟踪文件。

**Reason**：用户要求 canonical JSON/TSV、manifest、审计和 supporting artifacts 纳入 Git，当前工作树中它们仍是 untracked，独立 clone 无法取得这套人工评测闭包。

**Disposition**：`FAIL / fix-required`。由主 session 按 scope 选择性 add/commit；不得 add `.omx/`、`.worktrees/`、`runs/` 或其他无关用户改动。提交后复核 `git ls-files`、commit tree 和 manifest path closure。

**修复 commit**：无；本 reviewer 只读，未实施修复。

**Targeted rereview**：未通过。提交后需在干净 tree 或等价 Git tree 上重新检查 canonical 文件数、MANIFEST hashes 和 archive validator。

### ART-003 [M] repository-wide link-check scope note

`tools/check_md_links.py` 在仓库根执行报告 `239` 条失效引用（`235` relative、`4` blob-url），其中包含 `.worktrees/` 镜像和仓库其他既有文档；对本次 final archive 定向执行则为 `0` 条失效引用。该结果不构成 final archive 内部链接失败，但主 goal 若要求全仓库 zero-link gate，需要由 owner 单独处理或明确排除用户工作树，不能把 archive-scoped PASS 扩大解释为全仓库 PASS。

**Disposition**：`accepted-with-scope`，不修改用户现有 `.worktrees/` 或无关文档。证据命令：

```bash
python tools/check_md_links.py final_results/v60_current_vs_x1v2_baseline
python tools/check_md_links.py
```

## Final targeted rereview status

`artifact review = FAIL`；不存在可签署的 artifact PASS。当前已验证 raw manifest hash 未变、canonical 结构计数和 dense 行数闭合、archive-scoped link check 通过；但当前 manual validator 因 ART-001 失败，top-level archive validator 因本 review 文件更新后的 stale hash 失败，且 ART-002 的 Git untracked 状态仍需主 session 修复后重审。以上 proposal 不产生或确认任何新的人工语义标签。

## Final post-fix rereview

**时间**：`2026-08-29T18:00:54+08:00`
**身份**：`subagent:artifact-reviewer`；独立 provider-free proposal。未修改 frozen raw 或 canonical JSON/TSV。

**最终结论**：`FAIL`。

### Final checks

- Raw manifest file checks：v60 `1508/1508` files, `0` mismatches；X1v2 `842/842` files, `0` mismatches。
- Raw manifest SHA-256：v60 `sha256:8c2105dd7025f360500709e25ac9b483b907fdd91a3c39144798158ca1a25ba0`；X1v2 `sha256:8e9fa28071ba4acbbc0483c5ba84029ac69e7d0a618311ec85f7992081b374d0`。
- Fresh raw inventory：`162/162` cells；`1271/512` reports/findings；分轮 v60 `415/446/410`、X1v2 `173/163/176`；总 inventory items `1783`。
- Canonical decisions：v60 `1271`、X1v2 `512`；两侧每条 report 均有 `145` nested relations，分别为 `184295` 和 `74240` 行。
- Dense projection：`258535` rows，唯一 `(side, report_id, expected_id)` keys `258535`。
- Canonical JSON/TSV and raw identity check：Pydantic decision validation、raw identity/pointer closure、TSV mirror equality 均为 PASS；W2 receipt closure 为 PASS。
- `derived/manual_adjudication_v2/MANIFEST` canonical file hash 对拍：PASS。
- Archive-scoped Markdown links：`0` invalid links。
- `git diff --check`：PASS；raw `git diff` lines `0`，raw status lines `0`。

### Remaining failures

1. **`ART-001 [I] FAIL` remains.** `inventory.json` still stores top-level source hashes `sha256:93e31be...` and `sha256:b0d494...`, while current top-level `archive_manifest.json` and `publication_manifest.json` are `sha256:1c88343f854ef0019c6f1e29c81c898272568422f2b4e18fbef395cfe1033289` and `sha256:ab93ecbe0aee265f6ff5ecb74cf761520fbbccaeed06b1be5791146d47c6df78`. `validate_manual_adjudication.py` still fails at `validate_raw_inventory` with `inventory does not equal a fresh enumeration of the frozen archive`. The current manual `MANIFEST` has the newer top-level hashes, so inventory and MANIFEST are also mutually inconsistent.
2. **`ART-002 [I] FAIL` remains.** `git ls-files .../derived/manual_adjudication_v2 | wc -l` is `0`; the directory has `142` untracked status entries. A fresh clone cannot retrieve the canonical audit set.
3. **Top-level publication hash closure is still stale.** Direct comparison reports `20` stale listed files in both `archive_manifest.json` and `publication_manifest.json` (including `derived/manual_adjudication_v2` canonical outputs and review files); publication has one expected extra `archive_manifest.json`. The final archive validator currently fails at `derived/manual_adjudication_v2/group_decisions.json` because its listed hash is stale. This is separate from the raw manifest checks, which pass.

### Commands and evidence

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=evaluation/src \
python scripts/evaluation/validate_manual_adjudication.py \
  --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
# FAIL: ValueError: inventory does not equal a fresh enumeration of the frozen archive

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=evaluation/src \
python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root final_results/v60_current_vs_x1v2_baseline \
  --repository-root /home/zhangshaoang/oo-projects/research_ideas
# FAIL: manifest mismatch: .../derived/manual_adjudication_v2/group_decisions.json

python tools/check_md_links.py \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
# 失效引用 0 条（无）

git diff --numstat -- \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/raw
# 0 lines
```

**Disposition / targeted rereview**：`FAIL / fix-required`。没有修复 commit；artifact reviewer 只读。主 session 需要在所有 canonical 输出和 review 文件稳定后，重新生成 inventory、manual `MANIFEST` 及顶层 archive/publication manifests，按 scope 将 canonical 文件纳入 Git，然后重新运行上述全部命令。当前不能签署最终 PASS，也没有调用 provider。

## Independent raw/source closure review

**时间**：`2026-08-29T18:05:57+08:00`
**身份**：`subagent:artifact-reviewer`；独立 provider-free proposal。未修改 frozen raw、reference 或 canonical decision。

**结论**：`FAIL`。

### Verified evidence

1. 两个 raw manifest 的实际 SHA-256 仍为：
   - `raw/v60_current/archive_manifest.json`：`sha256:8c2105dd7025f360500709e25ac9b483b907fdd91a3c39144798158ca1a25ba0`
   - `raw/x1v2_baseline/archive_manifest.json`：`sha256:8e9fa28071ba4acbbc0483c5ba84029ac69e7d0a618311ec85f7992081b374d0`
   对 manifest 的逐项 bytes/SHA-256 独立对拍为 v60 `1508` files/`0` mismatch，X1v2 `842` files/`0` mismatch。`git diff` 和 `git status` 对 raw 均为 `0`。
2. Fresh provider-free inventory 从当前 raw 重新枚举到 `162/162` cells、v60 `1271` 和 X1v2 `512` reports/findings、总 `1783` items；round 分布 v60 `415/446/410`、X1v2 `173/163/176`。记录的 reference ledger 是 `145` items，hash `sha256:b5a38d3d24a51e980e5b9f5afc7c8c66aded59f3b51f16afe67e0deb592d0e36`；X1v2 input-closure manifest hash 为 `sha256:a68bc45acf1a6dafb42e363358c1a82e0caf4898077a9dcb5e275e21d848db95`。
3. 独立调用 Pydantic decision validation（使用 fresh raw inventory）、raw report identity/pointer closure 和 TSV projection equality 均通过：`v60_report_decisions.json PASS 1271`，`x1v2_report_decisions.json PASS 512`；W2 receipt/artifact closure 也为 PASS。
4. 两个 decision 集每条恰有 `145` relation：v60 `184295`、X1v2 `74240`；dense projection 为 `258535` rows 和 `258535` unique `(side, report_id, expected_id)` keys。
5. 独立运行 `validate_human_process_files`、`validate_structured_supporting_files`、`validate_group_decisions` 与 `validate_source_refs` 的组合检查通过。这覆盖了 `pane5_evidence_reads.json`、逐条 raw/source digest、JSON pointer、author NL/PlantUML hash、review log、aggregate、group 和全部 decision/relation source refs。
6. Manual `MANIFEST` 内列出的 canonical file hashes 对拍通过；archive-scoped Markdown link check 为 `0` invalid links。

### Findings

#### ART-004 [I] FAIL: final manual validator cannot establish immutable inventory closure

**路径**：`derived/manual_adjudication_v2/inventory.json` 的 `source_manifests`；`derived/manual_adjudication_v2/MANIFEST` 的 `raw_input_hashes`。

**Reason / basis**：stored inventory 保留顶层 archive/publication hash `sha256:93e31be...` 和 `sha256:b0d494...`，当前 top-level manifest hash 是 `sha256:1c88343f854ef0019c6f1e29c81c898272568422f2b4e18fbef395cfe1033289` 和 `sha256:ab93ecbe0aee265f6ff5ecb74cf761520fbbccaeed06b1be5791146d47c6df78`。因此规范入口：

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=evaluation/src \
python scripts/evaluation/validate_manual_adjudication.py \
  --directory final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

失败于 `ValueError: inventory does not equal a fresh enumeration of the frozen archive`。本 finding 不表示 raw record/pointer 失败，上述独立重新枚举和 pointer/TSV 检查均通过；它表示 canonical input closure 在当前顶层发布状态下不可复现。

**Disposition**：`fix-required`。在顶层 manifest 最终稳定后重新生成 inventory 和 manual `MANIFEST`，并从该一致快照完整运行专用 validator。

#### ART-005 [I] FAIL: top-level manifests are stale and omit current review files

**路径**：`archive_manifest.json`、`publication_manifest.json`。

**Reason / basis**：当前 archive manifest 预期 `2836` 文件、列出 `2835`，有 `21` 个 stale hashes，缺少 `reviews/16_semantic_targeted_rereview.md` 和 `reviews/17_fairness_raw_first_targeted_proposal_v2.md`；publication manifest 同样有 `21` 个 stale hashes、缺同两文件，并多出作为正常自引用候选的 `archive_manifest.json`。当前命令：

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=evaluation/src \
python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root final_results/v60_current_vs_x1v2_baseline \
  --repository-root /home/zhangshaoang/oo-projects/research_ideas
```

失败于 `manifest mismatch: .../derived/manual_adjudication_v2/MANIFEST`。

**Disposition**：`fix-required`。先完成所有 canonical/review 更新，后一次性运行 archive finalization 重新生成两个顶层 manifest，再运行 archive validator。

#### ART-006 [I] FAIL: canonical audit is not Git tracked

**路径**：`derived/manual_adjudication_v2/`。

**Reason / basis**：`git ls-files .../derived/manual_adjudication_v2 | wc -l` 为 `0`；`git status --untracked-files=all` 为 `142`。因此新 clone 不包含 canonical JSON/TSV/manifest/审计记录。

**Disposition**：`fix-required`。仅 add 本 goal 的 canonical audit、scripts、tests 和 review；不 add `.omx/`、`.worktrees/`、`runs/` 或无关用户文件。提交后检查 commit tree 中所有 manifest paths，并在 clean clone 或 Git tree 中 rerun closure。

### Targeted rereview

`FAIL`，无修复 commit。本 reviewer 没有修改任何 frozen raw 或 canonical data。修复 ART-004 至 ART-006 后，应从当前稳定 worktree 依次重跑：manual validator、final archive validator、archive link checker、raw manifest hash check 与 `git ls-files` tracking check。只有全部为 PASS，artifact reviewer 才能签署 PASS。
