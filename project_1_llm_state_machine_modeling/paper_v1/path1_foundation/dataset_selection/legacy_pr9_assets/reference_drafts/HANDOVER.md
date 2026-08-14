# Path 1 Phase 4b — Ref-STM Pipeline 接管文档

> **branch**: `dev/path1-hard-comparison`
> **PR**: [#9](https://github.com/HansBug/research_ideas/pull/9)
> **创建日期**：2026-05-27
> **最后更新**：2026-05-28（交班前最后一次状态固化）

新 Claude / codex 接管前**必须**按本文档第 §0 顺序读完，再决定怎么往下走。

## §0 接管前 30 秒摸排

```bash
cd /home/zhangshaoang/oo-projects/research_ideas
source .env                                  # 加载 LLM_*, CODEX_*, CLAUDE_*
git branch --show-current                    # 应为 dev/path1-hard-comparison
git log --oneline -5                         # 看最近几次 commit
cd project_1_llm_state_machine_modeling/paper_v1/selection/ref_stms

# 看本目录 README 入口（如缺）→ 本文件 + audited/{cara,cubesat}/bundle.md
ls audited/                                  # 应该有 2 个已 finalize 的 golden case 目录
ls audited/cara-infusion-pump-formal-spec__01/
ls audited/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01/

# 跑 4 关验证确认 golden 仍然干净
source ../../../../venv/bin/activate
python3 verify_pyfcstm.py audited/cara-infusion-pump-formal-spec__01/ref_model.fcstm
python3 verify_pyfcstm.py audited/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01/ref_model.fcstm
# 两条都应输出 ALL_OK + STATIC_OK 0 err / 0 warn
```

## §1 当前 Phase 进度大图

| Phase | 状态 | 备注 |
|---|---|---|
| 0-3（共同基础：method/ + eval/）| ✅ 完成 | PR #11 merged into main |
| **4a — sources/ 候选选样** | ✅ 完成 | [`selection_screening/SELECTION_REPORT.md`](../selection_screening/SELECTION_REPORT.md)；323 sample × codex 评审 + 15 候选 + 15 备选 |
| **4a' — 30 case NL 扩充** | ✅ 完成 | [`nl_expansion/`](../nl_expansion/)；30/30 严格溯源扩充 NL 落 [`path1_parquet/sources_path1.parquet`](../path1_parquet/sources_path1.parquet) |
| **4b — ref-STM pipeline + golden refs** | 🔁 **进行中（接班点）** | **本文件**；已落 2 个 golden（cara 低-V / cubesat 高-V），尚待 prompt 强化 + 批量跑 |
| 5 — 双 LLM annotator 评审 + 人类签字 | ⏸ 等待 4b 完工 | |
| 6 — `PATH1_REPORT.md` 决策报告 | ⏸ 等待 5 | |
| 7 — 收口 + PR | ⏸ 等待 6 | |

## §2 Phase 4b 的故事 — 从 path-2 搬流程 → 经历 5 轮迭代 → 现在站在哪里

### 2.1 任务定义

把隔壁 PR #10 的 ref-STM 5-stage 流程（codex draft → claude review → bundle → user audit → finalize）搬到 path-1 并适配。Path-1 的关键差异：

| 维度 | path-2 (PR #10) | path-1（本次）|
|---|---|---|
| 评测目标 | 4 intrinsic (ParseRate/SemValidRate/SimRate/ReachabilityRate) | **5-component manual eval** (TP/FP/FN) — 需要 ref |
| codex draft 产出 | `.fcstm + .scenarios.json`（要 sim coverage）| **`.fcstm + ref_components.json`**（5-component IR）|
| 验证关数 | parse + sem + sim_smoke + scenarios_all_pass | parse + sem + sim_smoke + **static analysis**（catches 逻辑死代码）|
| ref 最终位置 | `eval/data/path2_selection/ref_stms/audited/` | **`paper_v1/selection/ref_stms/audited/<case>/`**（最终复制到 `eval/data/refs/<case>/`）|
| 评审 rubric | semantic / NL 忠实 / **C-axis grounding** / scenarios | semantic / NL 忠实 / **5-component 完整性** / V 维度（H/G/A/F 视角）|

### 2.2 5 轮 ref 迭代关键时刻

| 轮次 | 改动 | 结果 | 当事 commit / file |
|---|---|---|---|
| **codex v1** | 原 path-2 prompt 直接套用，无 static analyzer | ❌ 6 ERROR / 17 WARN — 20 个 var 做 fact-flag、4 个 backManual 用 read-only var 作 guard、Wait state deadlock | `codex_drafts/cara-...result.json` 显示 status=OK 但实际死代码 |
| **codex v2** | 加 static analyzer (verify_pyfcstm_static.py)，加 5 类反模式 anti-pattern 描述到 prompt | ✅ 0/0，但 V = ∅（用 block-local temp identifier 而非 def）→ SEVT V 维度不可比 | smoke2.log dur=1181s |
| **golden v1**（手工）| 应用 D1/D2/D3 drop 纪律（mode-mirror / event-paraphrase / external-actor）+ 短动宾命名 | ✅ 0/0，2 actions，但仍 V=∅ | `audited/cara/ref_model.fcstm` 早期 |
| **golden v2** | 为 3 个 NL-grounded controller output signal 加 `def int` | ⚠️ 0err / 3warn（output signal write-only — 表面 OK 但 var 是死的 doc） | same file 中间版本 |
| **golden v3 (cara当前)** | pulse-signal handshake 模式：raise in transition / acknowledge + clear in Manual.during（var 真两侧用）| ✅ 0/0，但 var 没驱动任何 transition decision → 用户判定"为 var 而 var" | `audited/cara-infusion-pump-formal-spec__01/ref_model.fcstm` 当前版本 |
| **新增 golden — cubesat 高-V case** | 找到 cubesat NL 真有 var-gated 业务逻辑（battery_charge<86 / antenna_retries<3 / sun_visible 分支 / FDIR anomaly），手工编码 6 vars + 11 guards | ✅ 0/0，guards=11（cara=0 的 ∞ 倍）— V 真活 | `audited/reusable-and-reliable-flight-control-software-.../ref_model.fcstm` |

### 2.3 user discussion 留下的纪律

5 条纪律（D1-D5）已经在用户对话里反复确立，**必须**写进 codex prompt few-shot 给批量跑用：

| ID | 纪律 | 范围 |
|---|---|---|
| **D1** | drop mode-mirror（不要写 `<tgt>_mode_set = 1`，tgt 已表达）| transition effect actions |
| **D2** | drop event-paraphrase（不要写 `<event>_happened = 1`，event 已表达）| transition effect actions |
| **D3** | drop external-actor actions（caregiver/operator 做的不是 controller 做的）| transition effect actions |
| **D4** | output signal vars + pulse-signal handshake（raise + acknowledge-clear 两侧用）| V — output signals only |
| **D5** | case-by-case judge V necessity（NL 真有 var-gated 才声明；mode-switching only case 可以 V=0；@external 标注外部输入）| V — overall |

### 2.4 cubesat 高-V golden 的关键模式

cubesat ref 落地了**6 条 path-1 paper §3 method evidence 都依赖的关键模式**，新接班的 claude 需要学会：

1. **`@external` annotation** — 传感器/ground/FDIR 输入用 `def int X = 0; // @external [E*] ...` 标注；static analyzer 因此豁免 `unwritten_read_var` ERROR
2. **counter pattern self-read** — `boot_counter = boot_counter + 1;` 中 RHS 的 `boot_counter` 计为 read（analyzer 已支持）
3. **V-driven guard** — `Src -> Tgt : if [battery_charge < 86];` 这种是 path-1 paper §C2 contribution 的直接 evidence
4. **forced transition 无 effect 限制** — pyfcstm 语法 `! src -> tgt : if [guard];` 不允许 effect block；要"acknowledge 外部 flag"的话，effect 移到 target-state.enter
5. **event-driven vs guard-driven 分两条 transition** — pyfcstm 不允许 `: Event : if [guard]` 组合；要"on event + when condition"的拆成两条
6. **`@external` flag 的 acknowledge 模式** — 例如 `anomaly_detected` 由 SAFE.enter 清零（一进 SAFE 就 ack 把 controller 带来这里的故障 flag）

完整 cubesat 设计依据见 `audited/.../cubesat.../ref_model.fcstm` 注释 + 待写的 bundle.md。

## §3 当前未决问题（待接班人决定）

按优先级排：

### Q1 — 给 cubesat 补 bundle.md

cara 已经有完整 bundle.md（涵盖 9 节：决策摘要/NL 中英文/状态机结构/IR/验证日志/NL↔DSL 溯源/discipline 学术防御/签字区/迭代附录）。**cubesat 还缺 bundle.md**。

建议结构同 cara，但侧重不同：

- §0 决策摘要：cubesat 是 **V-rich golden** 对照 cara 的 V-poor golden，演示**两种极端 case 都能用统一纪律处理**
- §3 DSL：突出 `@external` annotation 和 6 个 var × 11 guards 的对应
- §4 IR：states=8 / transitions=18 / **guards=11** / actions=2 / hier=1 — **guards=11 是亮点**
- §7 discipline：除 D1-D5 外，加 cubesat 特有的 D6（@external annotation）、D7（forced 无 effect 的 enter-clear 模式）、D8（event vs guard 分离）

### Q2 — 把 D1-D5 + cubesat 学到的 D6-D8 + 2 个 golden few-shot 写进 codex prompt

`prompts/codex_draft_template.md` 当前只有 D1-D5 描述，**没有 few-shot 示范例**。批量跑剩 28 个 case 前必须把 cara + cubesat 完整作为 few-shot 写进 prompt，让 codex 看具体范例。

具体改动：

- 在 prompt 末尾加 §"Few-shot golden references" 段
- 引用两个 ref_model.fcstm 全文（cara 67 行 / cubesat ~150 行）
- 强调 cara 适用低-V case（mode-switching），cubesat 适用高-V case（var-gated）
- 加 D6/D7/D8 显式说明

### Q3 — source selection 是否需要重排（按 V-richness）

当前 SELECTION_REPORT 把 cubesat 排 candidate **#11**，cara 排 candidate **#7**。但实际 cara 是低-V case（不适合演示 V 体现），cubesat 才是高-V case（应该是 golden few-shot 主推）。

可选方案：
- **A** — 重新跑 selection（用 V-gated guards 维度作为打分轴），把 cubesat / microgrid-EMS / bipedal-robot 等高-V case 提到 top
- **B** — 不重排，但在 codex prompt few-shot 里**显式指出**两种 case 的处理范式（V-rich / V-poor 都要会）
- **C** — 把 D5 "case-by-case judge V necessity" 作为 codex 评估每个 case 时的第一关，让 codex 自己分类

建议 B + C 组合：不重做选样（避免又一轮 codex 评审 30 min），但在 prompt 里用 cara + cubesat 两条 golden 把 V 范式钉死，让 codex 学会分类。

### Q4 — 批量跑剩 28 case 的并发策略

`run_codex_draft.sh` 已经实装。`orchestrate_ref.sh` 需要 port 自 path-2（或写一个并发 driver 跑 selection.json 里 30 个 id，跳过 audited/ 已有的 2 个）。

建议：parallel ~6-10 worker（codex 单 case 平均 15-25 min，包括 4 关验证 + 3-5 iter）；30 case / 10 worker / 20 min = 1 hour wall clock。注意：codex draft 可能仍有 V 处理不一致问题（即使 few-shot 也可能跑偏），需要每个 case 复跑 verify + extract，对失败的 case retry 或手工兜底。

### Q5 — 跑完 batch 后的 audit 阶段

每个 case 跑完后产出 `codex_drafts/<id>.fcstm` 等，需要：

1. 自动 verify 通过（parse + sem + sim_smoke + STATIC_OK）
2. 自动 extract 5-component IR
3. claude_review.sh 评审（path-2 有，需要 port 同时改 rubric 到 path-1 5-component 视角）
4. build_bundle.py 生成 `bundles/<id>.md`（path-2 有，需要 port 同时调整结构）
5. 用户人工签字进 `audited/<id>/`

step 3-5 都是 Phase 4b 后段工作量。

## §4 文件地图（接班必读）

### 4.1 ref-STM pipeline 基础设施（已落地）

| 文件 | 状态 | 作用 |
|---|---|---|
| [`verify_pyfcstm.py`](./verify_pyfcstm.py) | ✅ stable | 4 关验证一体：parse + sem + sim_smoke + static |
| [`verify_pyfcstm_static.py`](./verify_pyfcstm_static.py) | ✅ stable | 静态分析：catch unwritten_read_var / forced_unreachable / write_only_var / deadlock_state / unreachable_state / high_var_to_state_ratio；支持 `// @external` annotation 豁免；assignment RHS self-read 也 track |
| [`extract_components.py`](./extract_components.py) | ✅ stable | 调 `eval/extract/pyfcstm.py:extract_pyfcstm` 出 5-component IR JSON |
| [`run_codex_draft.sh`](./run_codex_draft.sh) | ⚠️ 待复测 | 单 case codex draft 驱动；首次跑 cara 时 codex 实际给出 v1（fact-flag bloat）和 v2（temp identifier）两个版本，没自动达成 golden — codex 自己很难想到 D1-D5 + V handshake，**必须靠 few-shot 引导** |
| [`prompts/codex_draft_template.md`](./prompts/codex_draft_template.md) | ⚠️ **待加 few-shot** | 当前只有 D1-D5 文字描述；接班人首先要做 Q2（把 cara + cubesat 全文 + D6-D8 加进去）|
| `orchestrate_ref.sh` | ❌ 待 port | 从 path-2 搬过来 |
| `run_claude_review.sh` + `prompts/claude_review_template.md` | ❌ 待 port | 同上 |
| `build_bundle.py` | ❌ 待 port | 同上 |

### 4.2 Golden refs（已落地，paper-defense-ready）

| 路径 | 状态 |
|---|---|
| [`audited/cara-infusion-pump-formal-spec__01/ref_model.fcstm`](./audited/cara-infusion-pump-formal-spec__01/ref_model.fcstm) | ✅ golden v3 — 低-V case |
| [`audited/cara-infusion-pump-formal-spec__01/ref_components.json`](./audited/cara-infusion-pump-formal-spec__01/ref_components.json) | ✅ 5-component IR (states=6 trans=12 guards=0 actions=2 hier=1) |
| [`audited/cara-infusion-pump-formal-spec__01/bundle.md`](./audited/cara-infusion-pump-formal-spec__01/bundle.md) | ✅ 完整 9 节用户审阅入口 |
| [`audited/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01/ref_model.fcstm`](./audited/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01/ref_model.fcstm) | ✅ golden v1 — 高-V case |
| `audited/<cubesat>/ref_components.json` | ✅ IR (states=8 trans=18 **guards=11** actions=2 hier=1) |
| `audited/<cubesat>/bundle.md` | ❌ **待写**（Q1）|

### 4.3 历史 codex draft（audit trail）

| 路径 | 内容 |
|---|---|
| [`codex_drafts/cara-...__01.fcstm`](./codex_drafts/cara-infusion-pump-formal-spec__01.fcstm) | codex v2 输出（不是 golden；保留作为对比）|
| `codex_drafts/cara-...__01.notes.md` | codex v2 自报设计选择 + 自报 hallucination |
| `codex_drafts/cara-...__01.result.json` | codex v2 final JSON |
| `codex_drafts/cara-...__01.ref_components.json` | codex v2 抽出的 IR |

### 4.4 外部依赖

| 文件 | 关系 |
|---|---|
| [`../selection_screening/candidates.jsonl`](../selection_screening/candidates.jsonl) | 323 sample meta（选样 input）|
| [`../selection_screening/SELECTION_REPORT.md`](../selection_screening/SELECTION_REPORT.md) | 15 候选 + 15 备选 |
| [`../nl_expansion/expansions/<case_id>.json`](../nl_expansion/expansions/) | 30 个扩充 NL（codex draft 要读这个）|
| [`../nl_expansion/pool.tsv`](../nl_expansion/pool.tsv) | 30 case meta（run_codex_draft.sh 读这个）|
| [`../nl_expansion/selection.json`](../nl_expansion/selection.json) | 30 case manifest（orchestrator 读这个）|
| `eval/extract/pyfcstm.py`（原 PR #9 历史后端路径，当前归档未复制） | extract_components.py 的 backend |
| [`../path1_parquet/sources_path1.parquet`](../path1_parquet/sources_path1.parquet) | 15 candidate sprint 主数据集 |

## §5 待 commit 的 uncommitted 改动（接班前要清）

```
M project_1_llm_state_machine_modeling/eval/extract/pyfcstm.py    # extract_pyfcstm 完整修复（之前坏的 markdown 注入）
?? project_1_llm_state_machine_modeling/paper_v1/selection/ref_stms/    # 整个 ref_stms 工作目录
```

ref_stms/ 内含：
- 流水线脚本：verify_*.py / extract_*.py / run_codex_draft.sh / prompts/
- codex_drafts/cara-* (codex v2 输出)
- audited/cara/* (golden v3 finalize)
- audited/cubesat/* (golden v1 finalize — 待 bundle)
- verifier_logs/* (codex raw 流，已 gitignore 主体)

## §6 接班后的推荐 next-step 顺序

1. **跑 §0 摸排命令**，验证两个 golden 仍干净
2. **读 `audited/cara/bundle.md` §0 + §7**，理解 D1-D5 + cara 处理范式
3. **读 cubesat 的 `ref_model.fcstm` 注释**，理解 D6（@external）+ D7（forced 无 effect）+ D8（event/guard 分离）
4. **写 cubesat 的 bundle.md**（Q1）— 完成 V-rich golden 文档
5. **改 `prompts/codex_draft_template.md`**（Q2）— 把两个 golden 作为 few-shot 嵌入
6. **port `orchestrate_ref.sh` + `run_claude_review.sh` + `build_bundle.py`** 从 path-2
7. **批量跑 28 case**（Q4）— 跳过 audited/ 里的 2 个 already-golden case
8. **跑完 audit 后** finalize 进 `eval/data/refs/<case>/`

## §7 给接班人的诚实建议

1. **不要相信 codex 自己能输出 golden**。即使有完整 D1-D8 + few-shot，codex 也会偶尔翻车。每个 case 跑完都要人眼或第二个 LLM (claude review) 复核
2. **STATIC_OK 不等于学术 OK**。verify 通过只是低级 sanity；用户层面（bundle.md §7）才是真 audit
3. **V 在不同 case 里角色完全不同**。cara V=3 是 output signal，cubesat V=6 是真 state；不要套用 cara 经验到 cubesat-like case
4. **path-1 vs path-2 评测口径不一样**。path-2 是 reference-FREE intrinsic，path-1 是 reference-BASED 5-component manual eval。这意味着 path-1 ref 质量直接决定 paper §4 数字可信度
5. **用户判断 > codex 判断 > 静态分析判断**。优先级永远是这个

End of HANDOVER.md — 接班人通读以上后应该能续上。任何不明白的可以直接看 audited/cara/bundle.md（最完整的 paper-defense doc）。
