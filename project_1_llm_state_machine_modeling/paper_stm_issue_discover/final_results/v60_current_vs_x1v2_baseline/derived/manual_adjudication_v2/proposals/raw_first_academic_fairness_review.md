# Raw-first Academic/Fairness Review Proposal

**审查日期：** 2026-08-29
**审查身份：** independent raw-first academic/fairness reviewer
**状态：** proposal-only；不是最终人工签署、不是最终 label，也不替代后续双读/仲裁。

## 0. 审查边界

本审查只读取以下证据层：

- 冻结 raw：`final_results/v60_current_vs_x1v2_baseline/raw/v60_current/` 与 `raw/x1v2_baseline/`；
- 冻结输入/source inventory：`reference/x1v2_input_closure/` 与 `pipeline/representation/reports/llms_emp_r45_java_60/pairs/*/generated-evidence-discovery/source-inventory.json`；
- 冻结 predicate registry/source catalog：`reference/predicate_registry.json`、`reference/current_source_catalog.json`、`method/src/paper_stm_method/resources/predicate_registry.json`、`related_work/provenance/current_source_catalog.json`；
- 协议原文和 issue-facing 长期文档：`issue_189_body.md`、`discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md`、`discover_matrix/docs/protocol/semantic_judge_protocol.md`、`pipeline/evidence_discovery/PREDICATE_REGISTRY.md`、`related_work/provenance/CURRENT_SOURCE_AUDIT.md`。

未读取 `derived` 下已有 primary、proposal、frozen label 或 review decision 的内容；未把任何已有派生判断当作本审查证据。raw、协议、registry 和 source catalog 均未修改。

## 1. 结论提案

当前输入内容本身通过对称性检查，但公共 artifact closure 的 identity contract 未通过。建议在 closure identity 修复并重新产出/复核 Judge 结果前，阻断任何未经限定的 current-vs-baseline fairness claim。

predicate provenance 没有发现阻断性缺陷：19 个冻结 predicate 均有来源，28 个 source ID 均能回链，catalog 的 40 个路径在以 `paper_stm_issue_discover` 为基准目录时均存在。这里明确采用 paper1 工作区根作为 catalog path base；catalog 本身未显式写出 `path_base`，可作为后续低优先级文档改进，但不应把它误报成当前文件不存在。

## 2. 口径冻结与边界

本审查按 `issue_189_body.md:27-37, 149-166` 和 issue #195 snapshot 的现行闭合规则理解：

- `D2-lit`、`D2-impl`、`D2-norm` 才能进入 issue 集合；`D1` 与 `D0` 不能因为 W 高而进入 issue 集合。
- A/D 事实与规范性不能被 W 替代。A0/事实归因错误、只在派生表示上成立的现象，按 snapshot `:40-46` 保留在 `FALSE_POSITIVE` 或 `NOT_A_DEFECT_CLAIM` 边界；当前 backend 不支持只降低 W，不把真实事实改成 INVALID。
- W0/W1/W2 是证据强度轴，不是 relation 或 validity 的资格门；具体、可审计的 W1 仍可能是 valid/full。
- relation 只用 `FULL_MATCH`、`PARTIAL_MATCH`、`NO_MATCH`。先判报告核心有效性，再判 relation；只有 `INVALID` 是 semantic FP。`PARTIAL_MATCH` 只进入 supported coverage，不是 FP；ledger-unmatched 不能改名为 semantic FP。
- `VALID_KNOWN` 至少有一个正向 relation；`VALID_NOVEL` 要求报告成立且对全部 expected 为 `NO_MATCH`。不能从“不在 ledger”直接推出 novel。

这一区分使本提案只处理输入闭包、provenance 和公平性证据链，不对任何候选报告作最终 D/A/W、validity 或 relation 判决。

## 3. Findings

### RF-001 — High / P1：两臂公共 closure hash 全量不一致

**具体路径：**

- `final_results/v60_current_vs_x1v2_baseline/raw/v60_current/judge/composite/summary.json`
- `final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/judge/composite-summary.json`
- 两个 summary 的 `pair_receipts` 指向的 `judge/source_runs/*/inputs/{pair_id}.json` 中的 `artifact_closure`。

**观察：** 两个 composite summary 都是 162 个 pair/round receipts，覆盖相同的 54 pair 和 1/2/3 三轮。逐 pair/round 比较后：

| 检查 | 结果 |
|---|---:|
| artifact closure 数组（含 13 个 role、content/hash/basis 字段）完全相同 | 162/162 |
| 去掉 `closure_hash` 与 `basis` 后 closure 相同 | 162/162 |
| closure-level `basis` 相同 | 0/162 |
| closure-level `closure_hash` 相同 | 0/162 |

`0004/r1` 是可复核样例：

- current closure hash：`sha256:c2f774515aa2ed588ccae09691e7d567209de38a6c5b4a993157519d01f4df6c`
- baseline closure hash：`sha256:9dc58c99cbda696824e38399384b0793901e50e836c7e4da1e2c07cec695e970`
- current basis 中的 PairInput manifest：`sha256:ba524cdda8ab86d40255b760d439588810187ee42e07913006c23d83b7f2352c`
- baseline basis 中的 PairInput manifest：`sha256:4cba1f9b1212b5aa4115d60e8170e91281f3efb925ba0cdf4ea607d9f2df6637`

**Reason：** 协议原文 `semantic_judge_protocol.md:99-103` 要求两臂在 adapter 之后进入完全相同的公共 artifact closure，且相同 pair 的 closure 的顺序、内容、provenance 与 hash 不因 arm 改变。当前 artifact 内容虽然对称，但 closure basis 把 arm-specific 的 PairInput manifest 身份带进了 closure-level hash，因此发布的 closure identity 不是 arm-neutral。

**Basis：** 上述两个 frozen raw composite summary、对应 324 个 raw input closure 文件，以及 `semantic_judge_issue_195.snapshot.md:99-103`。这是公平性 contract 的确定性失败，不依赖任何 primary/proposal/frozen label。

**Proposal：** 将公共 closure 在 pair 层单次构建并复用到两臂；或者证明并固定一个不含 arm-specific method manifest 的 canonical PairInput manifest。新增 provider-free assertion：对每个 `(pair_id, round)`，两臂必须同时满足 artifact arrays、closure basis 和 closure hash 相等。修复后重新生成 Judge 派生结果；在该 assertion 通过前，不发布无条件的 current-vs-baseline 语义性能比较。

### RF-002 — Medium / P2：baseline 含 erratum recovery，current 没有相同 recovery 事件

**具体路径：** `raw/x1v2_baseline/judge/composite-summary.json` 的 `execution_erratum_commit`、`execution_erratum_paths`、`recovered_failures`；对应的 `raw/x1v2_baseline/judge/source_runs/x1v2-schema-repair-r{1,2,3}-265d977c/`。

**观察：** baseline composite 明确记录：

- `execution_erratum_commit = 265d977c81132cf6320b28dcde95ec46950f7e91`；
- affected paths 为 `utils/agent/runtime.py` 和 `tests/utils/test_agent_realtime.py`；
- 4 个 pair/round 使用 replacement run：`0057/r1`、`0033/r2`、`0011/r3`、`0019/r3`；
- 原始 run 保留为 failed，replacement run 提供最终 pair result。

current composite 的 `execution_erratum_commit` 为 `null`，`recovered_failures` 为空。两臂的 judge algorithm、protocol、prompt hash、model profile 和 judge commit 虽相同，但最终 baseline 样本混入了仅在 baseline 发生的 erratum/recovery 路径。

**Reason：** 这不是输入内容不对称，也不是把 provider failure 当成语义结果；raw 已诚实保留 failure 和 replacement provenance。但它使“同一 runtime/retry 条件下的直接公平比较”缺少对称执行条件，尤其 replacement run 可能改变 schema repair、调用时序或最终 report receipt。

**Basis：** `raw/x1v2_baseline/judge/composite-summary.json` 的 recovery records 与 `raw/v60_current/judge/composite/summary.json` 的对应 null/empty 字段；#195 对共同 retry、仲裁和指标入口的公平性要求，及 `semantic_judge_protocol.md:95, 99-103`。

**Proposal：** 在正式比较中显式标注这 4 个 replacement cells，并提供同一 erratum-fixed runtime 下 current 的敏感性复跑，或证明 replacement 只改变 provider transport 而不改变 schema/prompt/closure/result semantics。证明完成前，该项作为 P2 fairness threat，不单独把 baseline 结果判为无效。

### RF-003 — Medium / P2：baseline method records 缺少 source provenance 对象

**具体路径：** `raw/x1v2_baseline/method/run*/????-luna/record.json`；可复核样例 `raw/x1v2_baseline/method/run1/0004-luna/record.json`。

**观察：** 162 个 baseline method records 的顶层 `.source_provenance` 全部为 `null`。每条 record 仍保留 `inputs.nl_path`、`inputs.nl_sha256`、`inputs.plantuml_path`、`inputs.plantuml_sha256`，所以这不是已证实的 source content mismatch；它是 baseline method 运行记录没有显式 source-chain/provenance 对象的审计缺口。current 的 raw method summary 和 audit bundles 则保留 source-attribution/context 结构。

**Reason：** baseline 的来源仍可通过 path/hash 和公共 closure 回溯，但无法用与 current 等价的结构化 provenance 字段审计“方法读取了什么、来源角色是什么、输入闭合依据是什么”。这削弱 baseline 方法过程的可复现性，不能被 predicate catalog 的学术资格证明替代。

**Basis：** 162/162 baseline record 的结构化查询；`raw/v60_current/method/SUMMARY.md:3-30` 所记录的 current run contract/source commit/registry/162 cells；`semantic_judge_protocol.md:99-103` 的公共 closure 边界。该 finding 不改变已验证的 54/54 source-inventory hash 对称性，故不单独宣告语义结果无效。

**Proposal：** 为 baseline archive 增加等价的 immutable source-provenance manifest，至少绑定 pair、NL/PlantUML path/hash、source inventory hash、model/run contract 和 producer commit；若历史 raw 不可改，则新增旁证 manifest，不覆盖原 record。

## 4. Passed checks and non-findings

### 4.1 current/baseline frozen input symmetry

- reference closure manifest 覆盖 54 个 pair，每个 pair 保存 hash-verified NL 和 PlantUML；
- current 与 baseline judge closure 均为 162 个 pair/round；
- 13 个 closure artifact role 的数组及内容逐项相同：`162/162`；
- 54 份 frozen `source-inventory.json` 的 SHA-256 在 current、baseline 两臂均为 `54/54` 匹配；
- 两臂 composite summary 共享 `gpt-5.6-luna`、同一 prompt template hash、同一 protocol snapshot hash、同一 judge algorithm version 和同一 judge commit。

因此，本审查没有证据支持“current/baseline 读了不同 NL、PlantUML、FCSTM 或 exact source inventory”的指控。阻断点是 closure identity 的 basis/hash，而不是 artifact content。

### 4.2 predicate provenance

`reference/predicate_registry.json` 与 `method/src/paper_stm_method/resources/predicate_registry.json` 的 SHA-256 均为 `38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca`；两个 current source catalog 的 SHA-256 均为 `45ee60a378cb192ec364f1ee563e5ce8fb9cb8f79a4ed71dc8869049806a5647`。

在 registry 的 19 个 predicate leaf 上：

- 19/19 有非空 source list；
- registry 引用的 28 个 source ID 全部存在于 catalog；
- catalog 的 40 个 path，以 `paper_stm_issue_discover` 为 base directory 解析，40/40 存在；
- `PREDICATE_REGISTRY.md:5-35`、`CURRENT_SOURCE_AUDIT.md:1-16` 的 19-predicate/four-family/academic-provenance 口径与机器快照一致。

这是一项通过检查，不是对任意 predicate 具体语义或单次 W/D 结果的人工签署。

## 5. 推荐的 release gate

1. 先修复 RF-001，并以 provider-free closure identity test 证明 162/162 的 basis/hash 对称。
2. 对 RF-002 的 4 个 recovery cells 做 runtime/receipt sensitivity audit，并在正式表格单列 recovery provenance。
3. 补齐 baseline 的 source-provenance 旁证 manifest，不改写冻结 raw record。
4. 重新生成或重放受影响的 derived Judge 结果；保留失败和 replacement 记录，不把失败格静默删除。
5. 通过上述 gate 后，仍需依照 issue #195 的“先 validity、后 relation”顺序，由授权人工流程完成 D/A/W、validity 和 FULL/PARTIAL/NO 的最终裁定。

## 6. 复算命令

以下命令只读 frozen raw、reference/source inventory、registry/catalog；它不读取 `derived` 下的 primary、proposal 或 label，也不写文件。工作目录应为仓库根目录。

```bash
python - <<'PY'
import hashlib
import json
from pathlib import Path

repo = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover")
root = repo / "final_results/v60_current_vs_x1v2_baseline"
raw = root / "raw"
arms = {
    "current": (raw / "v60_current/judge/composite/summary.json",
                raw / "v60_current/judge/source_runs"),
    "baseline": (raw / "x1v2_baseline/judge/composite-summary.json",
                  raw / "x1v2_baseline/judge/source_runs"),
}

def load(path):
    return json.loads(path.read_text())

def sha256(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

maps = {}
for arm, (summary_path, runs_path) in arms.items():
    summary = load(summary_path)
    entries = {}
    for receipt in summary["pair_receipts"]:
        key = (receipt["pair_id"], receipt["round"])
        input_path = runs_path / receipt["source_run_id"] / "inputs" / f"{receipt['pair_id']}.json"
        closure = load(input_path)["artifact_closure"]
        entries[key] = closure
    maps[arm] = entries
    print(f"{arm}: receipts={len(summary['pair_receipts'])} inputs={len(entries)}")

keys = sorted(set(maps["current"]) & set(maps["baseline"]))
artifact_equal = sum(maps["current"][k]["artifacts"] == maps["baseline"][k]["artifacts"] for k in keys)
hash_equal = sum(maps["current"][k]["closure_hash"] == maps["baseline"][k]["closure_hash"] for k in keys)
basis_equal = sum(maps["current"][k]["basis"] == maps["baseline"][k]["basis"] for k in keys)
print(f"paired={len(keys)} artifacts_equal={artifact_equal}/{len(keys)} "
      f"basis_equal={basis_equal}/{len(keys)} closure_hash_equal={hash_equal}/{len(keys)}")

for key in keys:
    if maps["current"][key]["closure_hash"] != maps["baseline"][key]["closure_hash"]:
        print("first_hash_mismatch", key)
        print(" current", maps["current"][key]["closure_hash"])
        print("baseline", maps["baseline"][key]["closure_hash"])
        print(" current_basis", maps["current"][key]["basis"])
        print("baseline_basis", maps["baseline"][key]["basis"])
        break

source_dir = repo / "pipeline/representation/reports/llms_emp_r45_java_60/pairs"
pair_ids = sorted({key[0] for key in keys})
inventory_matches = {"current": 0, "baseline": 0}
inventory_count = 0
for pair_id in pair_ids:
    inventory = source_dir / pair_id / "generated-evidence-discovery/source-inventory.json"
    expected = sha256(inventory)
    inventory_count += 1
    for arm in inventory_matches:
        actual = next(a["sha256"] for a in maps[arm][(pair_id, 1)]["artifacts"]
                      if a["artifact_id"] == "artifact:exact_source_inventory")
        inventory_matches[arm] += actual == expected
print(f"source_inventory={inventory_count} "
      f"current_matches={inventory_matches['current']}/{inventory_count} "
      f"baseline_matches={inventory_matches['baseline']}/{inventory_count}")

reference = root / "reference"
registry = load(reference / "predicate_registry.json")
catalog = load(reference / "current_source_catalog.json")
predicates = [p for family in registry["families"] for p in family["predicates"]]
registry_source_ids = {source_id for p in predicates for source_id in p["sources"]}
catalog_source_ids = {source["id"] for source in catalog["sources"]}
catalog_paths = [path for source in catalog["sources"] for path in source["paths"]]
existing_paths = sum((repo / path).resolve().exists() for path in catalog_paths)
print(f"predicates={len(predicates)} predicates_with_sources="
      f"{sum(bool(p['sources']) for p in predicates)}/{len(predicates)} "
      f"source_ids={len(registry_source_ids)}/{len(catalog_source_ids)} "
      f"catalog_paths={existing_paths}/{len(catalog_paths)}")

baseline_records = list((raw / "x1v2_baseline/method").glob("run*/????-luna/record.json"))
null_provenance = sum(load(path).get("source_provenance") is None
                      for path in baseline_records)
print(f"baseline_method_records={len(baseline_records)} "
      f"null_source_provenance={null_provenance}")
PY
```

预期核心输出为：`paired=162 artifacts_equal=162/162 basis_equal=0/162 closure_hash_equal=0/162`、`source_inventory=54 current_matches=54/54 baseline_matches=54/54`、`predicates=19 predicates_with_sources=19/19 source_ids=28/28 catalog_paths=40/40`、`baseline_method_records=162 null_source_provenance=162`。
