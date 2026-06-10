# Path 1 — sources/ T0+🟢 候选选样工作区

> **任务**：从 sources/ T0+🟢 子集（323 sample）里筛 15 候选 + 15 备选，作为 `PATH1_HARD_COMPARISON_GUIDE.md`（原 PR #9 历史 guide，当前归档未复制该文件） 实验的 input。
>
> **选样准则（学术口径，方法独立）**：H 层次 / G 守卫算术 / A 动作非平凡 / F 故障恢复 — 这 4 维对应 Apvrille et al. 2025 baseline 自报 F1 最低的 3 个组件（actions=0.34 / guards=0.42 / hierarchical=~0.5）。**stress test on baseline's own documented weak components**，非 cherry-pick。
>
> **评审执行**：codex CLI (gpt-5.5 via pro provider) `--sandbox read-only`，每个 sample 强制读 `paper_content.txt` 全文 + 可选核 `paper.pdf`，输出固定 schema JSON。

## 目录结构

```text
selection/
├── README.md                  # 本文件
├── candidates.jsonl           # 323 行 — 每行一个 sample（条目级，非论文级）
├── reviews/<sample_id>.json   # codex 评审产物，断点续跑判据
├── logs/<sample_id>.attemptN.err  # 失败 attempt 日志
├── progress.json              # live 进度
├── run_main.log               # nohup 主跑日志
├── SELECTION_REPORT.md        # 聚合报告（人类阅读入口）
├── summary.csv                # 全量评分 CSV
└── scripts/
    ├── build_candidates.py    # 从 sources/*/STM.md 抽 T0+🟢 条目
    ├── review_one.py          # 单 sample codex 调用（被 run_screen 并发起来）
    ├── run_screen.py          # 并发 driver — 断点续 + retry
    └── aggregate.py           # 跑完后产 SELECTION_REPORT.md + summary.csv
```

## 接管入口

```bash
# 1. 从仓库根 source .env（必须）
cd /home/zhangshaoang/oo-projects/research_ideas
source .env

# 2. 进 selection 工作区
cd project_1_llm_state_machine_modeling/paper_v1/selection

# 3. 看当前进度
cat progress.json
ls reviews/ | wc -l                 # 已完成的 review 数
python -c "
import json
done = sum(1 for _ in open('reviews/').__iter__() if False)  # placeholder
"
# 或直接：
ls reviews/ | wc -l && wc -l candidates.jsonl

# 4. 继续跑（自动跳过已有 review）
python -m scripts.run_screen --workers 12 --timeout 600 --max-attempts 3

# 5. 跑完后聚合报告
python -m scripts.aggregate
cat SELECTION_REPORT.md | head -80
```

## 断点续跑 & 失败重跑

- `run_screen.py` 启动时调 `already_done(sample_id)`，已有 `reviews/<id>.json` 的 sample 直接 skip
- `review_one.review_sample(sample_id, max_attempts=3)` 内置 exponential backoff retry
- 任一 attempt 失败 → 写 `logs/<id>.attemptN.err`；3 次全失败 → ⚠️ 该 sample 没有 `reviews/<id>.json`，下次 run 自动 retry
- 跑完后可单独 retry 失败样本：

```bash
# 看哪些 sample 没 review JSON：
comm -23 \
  <(python -c "import json;[print(json.loads(l)['sample_id']) for l in open('candidates.jsonl')]" | sort) \
  <(ls reviews/ | sed 's/\.json$//' | sort) \
  > pending.txt
wc -l pending.txt

# 再跑一遍（worker 数可加大，failed 通常少）
python -m scripts.run_screen --workers 16 --timeout 900 --max-attempts 5
```

## 评分体系（emoji 图例）

| 分数 | Emoji | 含义 |
|:-:|:-:|---|
| 0 | ⚪ | 缺失 / 无信号 |
| 1 | 🟡 | 浅 / 表面提及 |
| 2 | 🟢 | 明确存在 |
| 3 | 💎 | 强 / 定义性特征 |

4 维（H/G/A/F）独立打分 0-3，加权 final = `1.0·H + 0.9·G + 1.0·A + 0.8·F + 0.3·baseline_difficulty + 0.3·fcstm_fit`。

权重设计依据：A=1.0、H=1.0（baseline 最弱 → 应重）；G=0.9（次弱）；F=0.8（关键但易与 H 重叠）。

## 硬排除（PATH1_HARD_COMPARISON_GUIDE §3.4）

- `has_parallel` — NL 含并行 / concurrent regions
- `has_history_restore` — NL 含 history-restore 语义
- `only_io_no_stm` — NL 只硬件 IO 没有 STM 抽象
- `too_thin_for_stm` — NL 过于稀薄无法构造 reference

任一命中 → `verdict="exclude"`，不进候选 / 备选。

## 候选池分层目标

| STM 类型 | 候选 (15) | 论据 |
|---|---:|---|
| HSM | 5-6 | fcstm 主战场，C1+C3 |
| EFSM | 4-5 | C2 Expr IR 主战场 |
| FSM | 2-3 | baseline 也应能做对的 sanity |
| Other | ≤1 | 不在 paper 主线 |

## paper 学术防御要点（reviewer 防 cherry-pick）

1. **客观难度判定**：选样准则只引用 Apvrille 2025 §IV-C 报告的 baseline F1 数字，**不引用 fcstm 任何能力**
2. **stress test framing**：paper §4 显式声明 "we stress-test on the documented-weakest components, not the average case"
3. **后续 baseline 全覆盖**：HSM + mode switching + fault recovery 是 6 个 baseline 里 ≥4 个都会涉及的 zone，正式 paper 复用同 dataset 不换

## 产出物（跑完后）

- `SELECTION_REPORT.md` — 候选 15 / 备选 15 详尽表 + rationale + 全量评分
- `summary.csv` — 机器可读 CSV
- `candidates.jsonl` — 后续 `eval/data/sources_path1.parquet` 的 source-of-truth
