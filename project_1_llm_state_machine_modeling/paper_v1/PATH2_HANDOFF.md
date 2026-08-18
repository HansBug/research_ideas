# Path 2 Sprint — 任务接管手册（handoff）

> **生成日期**：2026-05-28
> **当前 branch**：`dev/path2-differentiation`
> **当前 commit**：`dadc7356` (push 到 `origin/dev/path2-differentiation`)
> **PR**：[#10](https://github.com/HansBug/research_ideas/pull/10)
> **本文目的**：让另一台机器或新 Claude/codex session 能完全接得上目前的状态，无任何信息缺失。

---

## 1. 接管前必读（按顺序）

1. **本文档** — 整个 sprint 当前状态 + 下一步动作
2. [`PATH2_DIFFERENTIATION_GUIDE.md`](./PATH2_DIFFERENTIATION_GUIDE.md) v5.1 — Path 2 主指引 (~800 行)
   - §1 categorical-differentiation framing（论证骨架 7 节）
   - §3 数据规则（T0 严格 + 3 桶）
   - §4 5-condition 实验矩阵
   - §6 VGC（主指标）+ 4 intrinsic（辅）+ ref STM 起草 pipeline
   - §8 PATH2_REPORT 产出 outline
   - §11.3 三段论 mapping（pyfcstm feature → LLM 能力 → 控制系统价值）
3. [`PATH2_REPORT.md`](./PATH2_REPORT.md) v5 outline — 待 sprint 末填数据
4. [`../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md`](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) — meta-level 冲刺计划
5. [`../eval/data/path2_selection/REPORT.md`](../eval/data/path2_selection/REPORT.md) — 15+15 选样详细报告
6. [`../method/STATUS.md`](../method/STATUS.md) — method/ 实装进度

---

## 2. Sprint 整体进度

| Phase | 状态 | 备注 |
|---|---|---|
| 0–3 method/ + eval/ 共同基础 | ✅ 完成（PR #11 已 merge 到 main）| Phase A-G + I 全套 |
| 4 — sources_path2.parquet 选样 | ✅ 完成（commit `259e6ea7`）| 15 candidates + 15 backup，30 case 严格溯源扩充 NL |
| **4.5 — Reference STMs 起草** | **✅ 完成（commit `dadc7356`）** | **15/15 APPROVE / 0 warning / 全 scenarios pass** |
| **5 — Stage E: 用户人工审阅签字** | **🔁 BLOCKING — 等用户** | 15 个 bundle .md 等用户逐一审阅 |
| 5.1 — `method/run_path2.py` 实装 | 待 Phase 5 后 | 5-condition 分发 + checkpoint + token tracking |
| 5.2 — 跑 75 主行实验 | 待 5.1 完成 | A0_single_umple / A0_hybrid_umple / A0_single_pyfcstm / A0_hybrid_pyfcstm / A_full_ours |
| 6 — VGC + 4 intrinsic 聚合 | 待 5.2 完成 | summary.json + PATH2_REPORT.md §4-§7 |
| 7 — REPORT 收口 + PR mark Ready | sprint 末 | 不自动合并，由用户综合决策 |

---

## 3. Commit 链 + 工件落盘

| commit | 内容 |
|---|---|
| `dadc7356` | **097 + 114 revise → 全 15 APPROVE**（含 codex_revise_template + driver）|
| `9f26e751` | 15 ref STMs 全部重做 — 0 warning lint gate 通过（v2）|
| `8b303b36` | 标准化 reference STM 生成 pipeline（097 示范）|
| `a7ba6e09` | GUIDE v5.1 §6 FUR→VGC + Reference STM pipeline 定义 |
| `28876278` | GUIDE v5 categorical-differentiation framing + REPORT v5 outline |
| `259e6ea7` | 落 sources_path2.parquet — 15 候选 sprint 主数据集 + 15 备选 |
| `105acf43` | 30 候选/备选 case 严格溯源扩充 NL + REPORT v2 |
| `7a5c05c1` | codex 全量 239 评审 + 15+15 候选/备选选样 checkpoint |

---

## 4. 当前 BLOCKING 状态 — 用户审阅 15 个 ref STM bundle

### 4.1 待审阅工件位置

```
project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms/
├── bundles/<id>.md       # ★ 用户审阅入口（8 节单文件，含全部信息）
├── codex_drafts/<id>.fcstm        # ref DSL
├── codex_drafts/<id>.scenarios.json
├── codex_drafts/<id>.notes.md
├── codex_drafts/<id>.result.json
├── codex_drafts/<id>.v1.*          # 097 + 114 的初版（archived，未删）
├── claude_reviews/<id>.json
├── claude_reviews/<id>.v1.json     # 097 + 114 初版评审（archived）
├── diagrams/<id>.svg               # pyfcstm visualize 出的状态机图
├── diagrams/<id>.puml              # PlantUML 源
├── translations/<id>.cn.txt        # claude 翻译的中文 NL
└── audited/                        # ★ 用户签字后产物落这（目前空）
    ├── <id>.fcstm                  # 用户最终签字的 ref DSL
    └── <id>.audit.md               # 用户审阅笔记 + 签字日期 + 修订要求
```

### 4.2 15 case 最终状态总表

| id | bucket | domain | verdict | revision | states | scenarios | warns |
|---|---|---|---|---|---:|---:|---:|
| 008 | EFSM | 🌡️ | APPROVE | v1 | 12 | 13/13 | 0 |
| 009 | HSM | 🚗 | APPROVE | v1 | 9 | 10/10 | 0 |
| 018 | FSM | ✈️ | APPROVE | v1 | 6 | 6/6 | 0 |
| 090 | EFSM | ⚙️ | APPROVE | v1 | 14 | 7/7 | 0 |
| **097** | FSM | ✈️ | **APPROVE** | **v2** | 6 | 14/14 | 0 |
| **114** | EFSM | 🅿️ | **APPROVE** | **v2** | 12 | 10/10 | 0 |
| 118 | HSM | ⚙️ | APPROVE | v1 | 10 | 8/8 | 0 |
| 138 | HSM | ⚙️ | APPROVE | v1 | 14 | 12/12 | 0 |
| 142 | EFSM | 🏭 | APPROVE | v1 | 13 | 11/11 | 0 |
| 160 | HSM | ✈️ | APPROVE | v1 | 10 | 12/12 | 0 |
| 169 | HSM | ⚙️ | APPROVE | v1 | 8 | 9/9 | 0 |
| 181 | EFSM | 🏢 | APPROVE | v1 | 10 | 10/10 | 0 |
| 194 | FSM | 🌡️ | APPROVE | v1 | 18 | 7/7 | 0 |
| 207 | HSM | 🏭 | APPROVE | v1 | 10 | 13/13 | 0 |
| 234 | EFSM | 🅿️ | APPROVE | v1 | 11 | 8/8 | 0 |

### 4.3 审阅工作流（给用户）

每个 case 打开 `bundles/<id>.md` 一个文件即可。8 节速读：

1. §1 英文 NL（含 [E] 溯源 markers）
2. §2 中文译文（保留 markers）
3. §3.1 状态机 SVG 图 + §3.2 pyfcstm DSL 源
4. §4 scenarios JSON（覆盖 NL 全特性）
5. §5 pyfcstm 验证日志（parse + sem + sim + scenarios + lint 0 warning）
6. §6 codex 起草笔记（设计 rationale + 迭代历史 + NL 对应关系）
7. §7 claude 评审（4 维 + hallucination + 建议）
8. §8 用户审阅区（待签字）

**签字流程**：

```bash
# 审阅通过后落盘
cd /home/zhangshaoang/oo-projects/research_ideas-2
RS=project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms

# 对每个签字通过的 case：
cp $RS/codex_drafts/<id>.fcstm $RS/audited/<id>.fcstm
# 把 bundles/<id>.md §8 的签字内容写入 audit.md
cat > $RS/audited/<id>.audit.md <<EOF
# Case <id> Audit — 2026-05-XX
## 审阅状态: ✅ approve
## 审阅笔记
- ...
## 修订要求
- 无 / 见下
## 签字
HansBug, 2026-05-XX
EOF
```

如果某条需要 revise / rewrite，可以直接编辑 `audited/<id>.fcstm` 后落 audit 笔记。

---

## 5. 接管后下一步动作（Phase 5.1 — `method/run_path2.py` 实装）

用户全 15 case 审阅完后启动。详细规范见 [GUIDE §5](./PATH2_DIFFERENTIATION_GUIDE.md#5-实验脚本-methodrun_path2py)。

### 5.1.1 待实装内容

1. **`method/loop.py` 加字段**：
   - `target_dsl`: `"umple"` | `"pyfcstm"`
   - `modeling_mode="hybrid"` 分支（4-step Hybrid strategy）
2. **`method/prompts/modeler/hybrid_*.txt`** — 新增 8 个 prompt（umple/pyfcstm × single_draft/structure_review/event_review/merge）
3. **`method/run_path2.py`** — 5-condition CLI 分发（GUIDE §5）
4. **`eval/data/path2_selection/aggregate.py`** — 加 VGC 指标 grep 函数 + axis-stratified 分组

### 5.1.2 5 condition 矩阵

| Condition | target_dsl | strategy | n_iter | feedback |
|---|---|---|---:|---|
| `A0_single_umple` | umple | single-prompt | 1 | 空 |
| `A0_hybrid_umple` | umple | hybrid 4-step | 4 | 空 |
| `A0_single_pyfcstm` | pyfcstm | single-prompt | 1 | 空 |
| `A0_hybrid_pyfcstm` | pyfcstm | hybrid 4-step | 4 | 空（**主对照**）|
| `A_full_ours` | pyfcstm | agent loop（MTI 6-step + cascaded repair）| 3 | parse / sem / sim |

### 5.1.3 资源预算

- 总 LLM calls: ~345 (5 conditions × 15 cases × strategy step count)
- Wall time: ~25-30 min (并发 -P 6) / ~2.5 hr (单线程)
- Token 消耗: ~1.5M

### 5.1.4 主报道指标（VGC）

每 case × 每 grounding semantic 给 binary score (1=verifiably grounded / 0=not)：

| Semantic | pyfcstm verifier | Umple verifier | C-axis |
|---|---|---|---|
| Per-cycle behavior | `during {}` / `>> during` aspect | **无 cycle-level verifier** | C1 |
| Numerical guard reasoning | `Expr` IR + Z3 solver | **无 SMT** | C2 |
| Forced fault path | `! * -> Error :: Event` + 静态展开 | **无层次自动展开** | C3 |
| Hardware effector decoupling | `abstract action` + handler | **无 abstract 层** | C4 |

主 lift: **`A_full_ours` vs `A0_hybrid_pyfcstm` VGC mean lift** — 隔离 deterministic feedback 收益。

---

## 6. 环境 / 工具 / 依赖（接管前自检）

### 6.1 接管前 sanity check

```bash
cd /home/zhangshaoang/oo-projects/research_ideas-2

# 1. branch + commit
git branch --show-current   # 应是 dev/path2-differentiation
git log --oneline -1        # 最新应为 dadc7356 或更新

# 2. 工作区干净
git status -s                # 应空

# 3. submodule
git submodule status pyfcstm  # 应有 commit 693fcf57

# 4. venv + pyfcstm
source venv/bin/activate
python3 -c "from pyfcstm.dsl import parse_with_grammar_entry; print('pyfcstm OK')"

# 5. env keys
source .env
[ -n "$LLM_ENDPOINT" ] && [ -n "$LLM_API_KEY" ] && [ -n "$LLM_MODEL" ] && echo "LLM env OK"

# 6. CLI tools
which codex
codex --version
which claude
claude --version

# 7. ref STM tools
ls project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms/
# 应有: verify_pyfcstm.py / verify_pyfcstm_full.py / lint_pyfcstm.py
#       run_codex_draft.sh / run_claude_review.sh / run_codex_revise.sh
#       build_bundle.py / orchestrate_ref.sh
#       prompts/ codex_drafts/ claude_reviews/ diagrams/ translations/ bundles/

# 8. gh CLI identity (执行任何 gh 操作前)
gh auth status                # active account 必须是 HansBug
git config user.name          # 应是 HansBug
# 如果 active 不是 HansBug：gh auth switch --user HansBug
```

### 6.2 关键依赖版本

- **pyfcstm**: submodule pinned at `693fcf57` (Merge PR #66 vscode 集成)
- **Python venv**: `pyfcstm`, `antlr4-python3-runtime`, `z3-solver`, `pandas`, `pyarrow`, `pdf2image`, `pytesseract`, `Pillow`, `PyPDF2`
- **codex CLI**: provider `pro`, model `gpt-5.5`, reasoning `xhigh`（profile in `~/.codex/config.toml`）
- **claude CLI**: Claude Code 2.1.150+
- **Node.js**: v24.14.1（用于 PlantUML remote renderer，pyfcstm visualize 调用）

### 6.3 LLM 三件套（实验主路）

`.env` 提供（已 gitignored）：
- `LLM_ENDPOINT`: OpenAI-compatible proxy
- `LLM_API_KEY`: proxy key
- `LLM_MODEL`: 默认 gpt-5.5

切换实验模型只改 `.env` 中 `LLM_MODEL` 后 `source .env`，代码不动（参 `method/gpt_client.py`）。

---

## 7. 核心工件清单

### 7.1 文档（paper_v1/）

```
paper_v1/
├── PATH2_DIFFERENTIATION_GUIDE.md   # v5.1, ~800 行，Path 2 主指引
├── PATH2_REPORT.md                  # v5 outline，待 sprint 末填数据
├── PATH2_HANDOFF.md                 # ★ 本文档
└── PATH1_HARD_COMPARISON_GUIDE.md   # Path 1 文档（参考）
```

### 7.2 数据集（eval/data/）

```
eval/data/
├── sources_path2.parquet            # 15 candidate sprint 主数据集（含纯 NL，无 [E] markers）
├── sources_path2_backup.parquet     # 15 backup
└── path2_selection/
    ├── pool.tsv                     # 239 候选元数据
    ├── selection.json               # 稳定 15+15 manifest
    ├── pool.tsv / build_parquet.py
    ├── REPORT.md                    # ~2000 行选样详细报告
    ├── briefs/                      # 2 份调研：baselines NL 风格 + pyfcstm grounding
    ├── prompts/                     # 3 个 codex prompt 模板（review / expand / revise）
    ├── expansions/*.json            # 30 case 严格溯源扩充 NL
    ├── results/*.json               # 239 case codex 评审
    ├── results_runtime/             # (待 Phase 5.2 跑出 predictions.parquet 落这)
    └── ref_stms/
        ├── verify_pyfcstm{,_full}.py
        ├── lint_pyfcstm.py          # IDE-equivalent warning 检测
        ├── run_codex_draft.sh
        ├── run_codex_revise.sh
        ├── run_claude_review.sh
        ├── build_bundle.py
        ├── orchestrate_ref.sh
        ├── prompts/                 # codex_draft + codex_revise + claude_review templates
        ├── codex_drafts/<id>.{fcstm,scenarios.json,notes.md,result.json}
        ├── codex_drafts/<id>.v1.*   # 097 + 114 archived
        ├── claude_reviews/<id>.json
        ├── claude_reviews/<id>.v1.json   # 097 + 114 archived
        ├── diagrams/<id>.{svg,puml}
        ├── translations/<id>.cn.txt
        ├── bundles/<id>.md          # ★ 用户审阅入口
        └── audited/                 # ★ 用户签字后产物（目前空）
```

### 7.3 method 实装（method/）

- ✅ Phase A-G + I 全套（PR #11 已合到 main）
- 🔁 Phase 5.1 待实装：`run_path2.py` + hybrid prompts + `target_dsl` 字段

---

## 8. 已知问题与 caveats

1. **pyfcstm issue [#99](https://github.com/HansBug/pyfcstm/issues/99)**：jsfcstm IDE 误报 forced transition 内引用的 event 为 unused。我们的 Python lint (`lint_pyfcstm.py`) 正确处理，但用户用 VSCode 打开会看到误报。**不阻塞 PATH2 实验主路**。
2. **Bundle orchestrator 偶发早退**：build_bundle.py 内嵌 claude inline 翻译调用可能挂起，导致 orchestrator 的 `while ... done` 循环没跑完。**Workaround**：直接 `xargs -n1 -P8 bash run_codex_draft.sh` 后 `xargs -n1 -P8 python3 build_bundle.py`，跳过 orchestrate_ref.sh 的 stage D 部分。
3. **Claude truncate JSON**：claude CLI 在长 JSON 输出可能 truncate 缺尾 `}`。`run_claude_review.sh` 已加 robust fallback（append 缺失的 `}` 后重 parse）。
4. **codex / claude 身份切换**：执行 `gh` 前必须确认 `gh auth status` active = HansBug，且 `git config user.name` = HansBug。
5. **VGC 主指标尚未实装**：`aggregate.py` 还没有 VGC grep 函数；Phase 5.2 跑实验前需要补，否则实验跑出来无法直接 aggregate。

---

## 9. 给接管者的极速 onboarding

按以下顺序在 5 分钟内进入工作状态：

```bash
cd /home/zhangshaoang/oo-projects/research_ideas-2

# 1. 自检（按 §6.1）
git status; git log --oneline -5
source venv/bin/activate
source .env

# 2. 看 handoff（本文）
cat project_1_llm_state_machine_modeling/paper_v1/PATH2_HANDOFF.md | head -100

# 3. 看主 GUIDE 的 §1（论证骨架）
sed -n '/^## 1\./,/^## 2\./p' project_1_llm_state_machine_modeling/paper_v1/PATH2_DIFFERENTIATION_GUIDE.md | head -100

# 4. 看 15 case bundle 概况（用户即将审阅）
ls project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms/bundles/
# 打开任一 .md（如 097.md）看格式

# 5. 检查 audited/ 是否有用户签字进展
ls project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms/audited/

# 6. 如果 audited/ 已有部分文件 → 用户已开始审阅，等用户完成
# 如果 audited/ 还是空 → 等用户开始审阅；同时可以预备 Phase 5.1 的 run_path2.py 实装
```

如有不明，直接读源码 — 所有工具脚本都是 self-documenting 的。
