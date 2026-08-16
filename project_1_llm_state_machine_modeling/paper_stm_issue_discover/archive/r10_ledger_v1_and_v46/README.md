> **Cold archive.** ⛔ 本目录不参与任何当前结论。⭐ 当前唯一有效的台账是 [discover_matrix/ledger_v2/](../../discover_matrix/ledger_v2/)（**145** 条），入口读 [ledger_v2/README.md](../../discover_matrix/ledger_v2/README.md)。

# r10 — v46 主臂与 v46 时代评测数据（2026-08-17 归档）

## 一、这是什么

第二版台账（145 条 D2+D1）产出之后，**它所取代的 v46 主臂、v46 时代的全部判定输出与分析脚本**转入冷归档。

⚠️ **注意归档范围在 2026-08-17 当天缩小过一次。** 最初连 `manual_review/`（第一版台账 + 60 份逐 pair 复审 + `relabel/` 重标工作区）也一并归档；随后判定那样会让**台账的证据链断线** —— `ledger.json` 每一条的 `worksheet` 字段都指向 `relabel/` 的工作单，把被指向的东西放进冷归档，等于让「凭什么这么判」查不到。故 `manual_review/` 已搬回台账目录，现名 [discover_matrix/ledger_v2/provenance/](../../discover_matrix/ledger_v2/provenance/)。

## 二、为什么归档

| 理由 | 说明 |
| :-- | :-- |
| **v46 主臂停用** | v46 的全部结果、多报裁定、遥测与报告转入归档；当前活跃区只保留 **X1v2** 这一条基线臂及其在新台账上的结果 |
| **评测口径换代** | `verdicts/` · `telemetry/` · `onepass_sample/` · `blind_sample/` 是针对第一版台账（126 条）做的判定，与第二版台账的 145 条条目不可直接对齐 |
| **活跃区要干净** | 归档前 `discover_matrix/` 有 112 个顶层条目；归档后只剩 `docs/`、`ledger_v2/`、`README.md` |

## 三、目录内容

| 路径 | 内容 |
| :-- | :-- |
| `v46/` | 主臂 v46 的 preregistered、result、audit、多报裁定与遥测。⭐ 它的 `unexpected_verdicts/G*.jsonl` 是第二版台账 `INS-` / `VU-` / `DIFF-` 三族的**原始来源**，仍被 `provenance/relabel/sources.py` 读取 |
| `verdicts/` · `telemetry/` · `onepass_sample/` · `blind_sample/` | v46 时代的判定输出、遥测与抽样 |
| `scripts/` | 102 份 v46 时代的分析脚本、启动脚本、快照 JSON 与配套测试 |

⭐ **不在这里的**：第一版台账 `expected_issue_set.json`、60 份 `<pair>-review.json`、`relabel/` 重标工作区 —— 全部在 [discover_matrix/ledger_v2/provenance/](../../discover_matrix/ledger_v2/provenance/)。

## 四、⭐ 怎么重新跑起来

### 4.1 数据只读

`v46/`、`verdicts/`、`telemetry/`、`onepass_sample/`、`blind_sample/` 是纯数据，直接读即可，无需环境。

### 4.2 v46 时代的分析脚本 —— ⭐ 已修好，开箱可跑

```bash
cd project_1_llm_state_machine_modeling/paper_stm_issue_discover
python -m pytest archive/r10_ledger_v1_and_v46/scripts -q     # 387 passed / 26 skipped（2026-08-17 实测）
```

⛔ **2026-08-17 之前不是这样。** `scripts/` 下的脚本原先位于 `discover_matrix/` 顶层，按 `Path(__file__).parents[N]` 定位仓库根与同级数据；归档使深度多了两层，于是 `parents[2]` 从「仓库根」变成了「论文工作区」。⚠️ 那类错位**不报错**，只是把路径解析到不存在的目录 —— 评测代码里空输入会被读成「没有命中」而不是「路径错了」（[CLAUDE.md](../../../../CLAUDE.md) §9.5-3）。实测那一刻是 **60 failed / 301 passed + 1 个收集错误**。

修法一律是**按目录名（或标志物）向上锚定，不数层数**，共四类：

| 类别 | 症状 | 修法 |
| :-- | :-- | :-- |
| 仓库根 | 19 处 `ROOT`/`REPO` = `parents[2]`/`parents[3]`，解析到论文工作区，于是 `ROOT / "project_1_.../pipeline/..."` 变成双重前缀 | 向上找同时含 `CLAUDE.md` 与 `.git` 的那一级 |
| 同级脚本 | 10 处测试用 `HERE.parent / "discover_matrix"` 找被测脚本；归档后脚本与测试同在 `scripts/` | 直接用脚本自己所在目录 |
| 证据链目录 | 29 处 `HERE / "manual_review"`；该目录已搬到 `discover_matrix/ledger_v2/provenance/`（见 §一） | 单独锚 `_PROVENANCE`，向上找 `paper_stm_issue_discover` 再进活跃区 |
| 活跃区 `docs/` | `HERE / "docs/protocol/hit_criterion.md"`；`docs/` 从未归档 | 同上，锚到 `discover_matrix/docs/` |

⚠️ 另外修掉一个**与路径无关**的陈年缺陷：`test_run_grid_sources.py` 的负控打桩的是 `run_grid.from_frozen`，而该函数已在 `f3ea403c`（永久移除 hold-out 机制）随 holdout 一起删除 —— `monkeypatch.setattr` 直接抛 `AttributeError`，**那条负控从此没有真正跑过**。已改为打桩仍然存在的 `from_runs`，意图不变。

⭐ 更早一轮已加固的两处：`nl_scope_filter.py` 的 `SEED`（并对 `excluded_pairs()` 返回空加了硬断言 —— 那次错位曾让 `00x8` 的 27 条记录静默重新进入能力分母）；`baseline_arm/**` 的 7 个文件。

## 五、⛔ 归档时做过的核验

| 检查 | 结果 |
| :-- | :-- |
| 全程 `git mv`（`git log --follow` 不断） | ✅ |
| 机械对拍 `git ls-files -s` 的 (路径 → blob) 映射 | ✅ 归档 3663 → 3663；证据链搬回时 13235 → 13235，同名内容变动 **0**，314 条纯改名 |
| `ledger_v2/ledger.json` 的 `worksheet` 字段同步 | ✅ 145 条全部指向 `./provenance/relabel/…` 且目标存在 |
| `provenance/relabel` 归位后重跑测试 | ✅ `151 passed / 21 skipped`，54 份工作单重生成后逐字节无变化 |
| `baseline_arm` 全量测试 | ✅ 54 passed |
| 本归档 `scripts/` 全量测试 | ✅ `387 passed / 26 skipped`（修锚点前为 60 failed / 301 passed + 1 收集错误） |
| `pipeline/feedback_loop` 全量测试 | ✅ `1860 passed / 4 skipped`（`PYTHONPATH=src:<repo root>`） |

## 六、⚠️ 与另外两个 archive 的区别

| 路径 | 内容 |
| :-- | :-- |
| **本目录** | v46 主臂 + v46 时代评测数据与脚本（2026-08-17） |
| [../](../) 下的 `r1_5`–`r9` | 更早的种子语料、Better STM 全树、issue lifecycle 脚手架、论文叙事、单 Agent discover 实现 |
| [../../../archive/](../../../archive/) | project_1 层的已停用旧路线（agent loop、Path-1 评测链） |
