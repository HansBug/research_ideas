> **Cold archive.** ⛔ 本目录不参与任何当前结论。当前唯一有效的台账是 [discover_matrix/ledger_v2/](../../discover_matrix/ledger_v2/)。

# r10 — 第一版台账与 v46 主臂（2026-08-17 整体归档）

## 一、这是什么

第二版台账（145 条 D2+D1）产出之后，**产出它的整条生产链、它所取代的第一版台账、以及 v46 主臂的全部评测数据**一并转入冷归档。归档不是删除：这里的每一份文件都是 `ledger_v2` 的证据链，`ledger.json` 的 `worksheet` 字段就逐条指向本目录下的工作单。

## 二、为什么归档

| 理由 | 说明 |
| :-- | :-- |
| **台账换代** | 第一版台账（`manual_review/expected_issue_set.json`，99 条）是 v46 与 X1 两轮判定的比对对象。它已被 [ledger_v2/ledger.json](../../discover_matrix/ledger_v2/ledger.json)（145 条，每条带 D 档与 L 档）取代 |
| **v46 主臂停用** | v46 的全部结果、多报裁定、遥测与报告转入归档；当前活跃区只保留 **X1v2** 这一条基线臂及其在新台账上的结果 |
| **生产链已完成使命** | `manual_review/relabel/` 是把 321 条三方判读变成 145 条台账的**工具**。⭐ `ledger_v2/ledger.json` 自包含（statement / 五轴 / D 档 / L 档 / 判定依据 / 人工裁决理由全部内联），不再依赖该链路运行 |
| **活跃区要干净** | 归档前 `discover_matrix/` 有 112 个顶层条目；归档后只剩 `docs/`、`ledger_v2/`、`README.md` |

## 三、目录内容

| 路径 | 内容 |
| :-- | :-- |
| `manual_review/` | 第一版台账 `expected_issue_set.json`、60 份 `<pair>-review.json`、分层文档，以及 **`relabel/`** —— 54 份工作单（含**全部人工裁决与逐条 meta review**）、三方 D 档判读包、去重台账、生成/回收/校验工具与 172 个测试 |
| `v46/` | 主臂 v46 的 preregistered、result、audit、多报裁定与遥测 |
| `verdicts/` · `telemetry/` · `onepass_sample/` · `blind_sample/` | v46 时代的判定输出、遥测与抽样 |
| `scripts/` | 102 份 v46 时代的分析脚本、启动脚本、快照 JSON 与配套测试 |

## 四、⭐ 怎么重新跑起来

### 4.1 relabel 工作单（最常见的复活需求）

```bash
cd archive/r10_ledger_v1_and_v46/manual_review/relabel
python3 generate.py          # 重新渲染 54 份工作单
python3 -m pytest test_relabel.py -q   # 151 passed / 21 skipped（归档后实测）
```

⭐ **归档后实测通过：`151 passed / 21 skipped`，54 份工作单重生成后逐字节无变化。**

⛔ **但归档当时并不是开箱即跑的 —— 深度变了，修过三类东西**（⚠️ 这正是 [CLAUDE.md](../../../../CLAUDE.md) §9.5-3 警告的目录深度锚点问题，记在这里以免日后再搬时重蹈）：

| 症状 | 修法 |
| :-- | :-- |
| ⛔ `sources.py` 的 `PAPER = dirname(DISCOVER_MATRIX)` 解析到了 `archive/`，`selected_seed_examples` 直接找不到 | 改为 `_find_up("paper_stm_issue_discover")` —— **按目录名锚定，不数层数**。⭐ 再搬只会**报错**，不会静默解析到错的地方 |
| ⛔ 全部相对链接断（到仓库根多了一层、到 `discover_matrix/docs` 要绕回去） | 逐类精确改：`CLAUDE.md` 5 上→6 上（`translations/` 下的再 +1，`nl_XXXX/` 下的同理）；`../../docs/` → `../../../../discover_matrix/docs/`；指向已归档脚本的改到 `../../scripts/` |
| ⛔ `test_relabel.py` 里写死五层 `..` 去读 `CLAUDE.md` | 同样改为向上找到含 `CLAUDE.md` 的那一级 |

⚠️ **依赖**：该链路读同目录下的 `../expected_issue_set.json`、`../<pair>-review.json`、`../../v46/unexpected_verdicts/G*.jsonl`（三者都在本归档内，相对关系未变），以及活跃区的 `baseline_arm/results/unexpected_verdicts/X1-*.jsonl`、`corpora/`、`selected_seed_examples/`（都由 `_find_up` 定位，不受深度影响）。

### 4.2 v46 时代的分析脚本

`scripts/` 下的脚本原先位于 `discover_matrix/` 顶层，按 `Path(__file__).parents[N]` 或相对路径定位仓库根与同级数据。⛔ **它们的目录深度变了**（多了两层 `archive/r10_ledger_v1_and_v46/scripts/`），⚠️ 直接运行会静默解析到错误目录 —— 评测类代码尤其危险，空输入会被读成「没有命中」而不是「路径错了」。⭐ 复活时必须先改锚点或把脚本临时复制回 `discover_matrix/` 再跑。

### 4.3 数据只读

`v46/`、`verdicts/`、`telemetry/`、`onepass_sample/`、`blind_sample/` 是纯数据，直接读即可，无需环境。

## 五、⛔ 归档时做过的核验

| 检查 | 结果 |
| :-- | :-- |
| 全程 `git mv`（`git log --follow` 不断） | ✅ |
| 机械对拍 `git ls-files -s` 的 (路径 → blob) 映射 | ✅ 3663 → 3663，blob 多重集完全一致，同名内容变动 **0**，477 条纯改名 |
| `ledger_v2/ledger.json` 的 `worksheet` 字段同步指向归档路径 | ✅ 145 条全部更新并验证目标存在 |

## 六、⚠️ 与另外两个 archive 的区别

| 路径 | 内容 |
| :-- | :-- |
| **本目录** | 第一版台账 + v46 主臂 + relabel 生产链（2026-08-17） |
| [../](../) 下的 `r1_5`–`r9` | 更早的种子语料、Better STM 全树、issue lifecycle 脚手架、论文叙事、单 Agent discover 实现 |
| [../../../archive/](../../../archive/) | project_1 层的已停用旧路线（agent loop、Path-1 评测链） |
