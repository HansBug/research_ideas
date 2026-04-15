# Review Notes

| Slide ID | Issue | Route To | Status |
|---|---|---|---|
| `s01-cover` | 封面标题原先含“与导师讨论”，用户反馈口吻尴尬；已统一改成 `2026-04-15-讨论`。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s08-baseline-evidence` | LibreOffice 渲染后图表坐标轴出现负刻度，影响阅读；已把正值图表统一从 `0` 起始。 | `generate_ppt.py` | `fixed` |
| `s09-sources-curation` | 原版只有 warning 和流程，因果关系不够显式；已补“前因 / 因此”因果条。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s10-sources-stats` | 统计页前因后果不够清楚，且 big-number 说明过长；已补因果条并压缩上排说明。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s11-sources-main-types` | 原版容易看成“只有数字，没有解释”；已补因果条并保留右侧定义表。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s12-sources-time-structure` | 原版没有明确说明“为什么离散主链仍需要更强结构”；已补因果条并收紧双结论卡。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s13-sources-examples` | 原 5 列表过密且前因不足；已改成 framing sentence + 4 列解释表。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s14-sm-family` | 原版 family slide 与 `project_1` 的关系说得不够直；已补因果条与底部“因此”结论。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s17-pyfcstm-role` | 贡献点卡片过多，导致框体拥挤；已从 6 张缩到 4 张更大的贡献卡。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s18-pyudbm-progress` | 标题偏长、左侧栈过密、容易误读成“什么都没有”；已缩短标题、增加因果条并把能力层压成 4 层。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s19-infra-feedback` | 原版闭环页偏结论堆砌；已补因果条并重排中央闭环与四角 evidence cards。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `global` | 多处短条仍在使用普通 card 组件，导致框尺寸不自然；已为小高度卡片加 compact layout 分支。 | `generate_ppt.py` | `fixed` |
| `s02-agenda` | 三张决策卡标题过长，render 后出现明显断裂，读者需要二次拼句；已改成更短的 audience-facing 文案。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s03-summary` | 结论卡中 `control-state` 等长标题仍偏挤，摘要页阅读节奏不够干净；已压缩标题与解释语句。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s04-why-project1-now` | 当前页已有时间窗和 readiness，但“为什么因此先做 project_1”的因果仍不够直接；已补因果条并收成更短的结论带。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s06-project1-evidence-chain` | `state_machine_types/` 卡片断裂成 `state_machine_ty / pes`，属于明显视觉缺陷；同时该页还缺一条更直接的因果收束；已改成 audience-facing 四卡片并补因果条。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s20-decisions-next-steps` | 决策卡文案偏长，Closing 卡也略挤；需要进一步压缩并补上“为什么这五件事能决定后续 6 周”的因果条；现已压缩文案并补因果条。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `global` | 可见文本里仍出现反引号包裹的 markdown 样式，例如 project_1、pyfcstm 等，不符合最终 PPT 质感要求；现已在所有可见文本路径上统一去除。 | `generate_ppt.py` | `fixed` |
| `s07-baselines-overview` | 原版更像“数量 + 卡片说明”，方法线不够清楚；现已重构为“左侧状态分布 + 右侧方法概述表”，并把 Umple baseline 单独拉成一行。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s11-sources-main-types` | 原版仍容易被读成自然分布说明；现已改成“不能这样解读 / 可以这样解读”双表结构，显式把样例池口径和领域总体分布分开。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s12-sources-time-structure` | 原版双图统计太像“又一页分布图”；现已改成 control-state 主模式解释表，并补一张结构证据表，强调收束对象不等于退化对象。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s14-sm-family` | 原版 family-tree 风格信息分散，且大量依赖框体堆砌；现已改成“主分支表 + 贡献形态表”，把 profile / DSL / infrastructure 的论点直接讲清。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s15-control-state-definition` | 原版还是偏抽象的离散 vs 连续对照，不足以说明控制系统 control-state 的核心语义；现已改成 6 行语义表，显式写出模式层次、联锁、恢复链、事件作用域、生命周期动作和局部 timer。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s16-pyfcstm-progress` | 原版没有站在 STM 文库角度明确说明 pyfcstm 属于什么、近邻是谁；现已改成 STM 近邻对照表，并把 Umple / UmpleRun 提升为重点比较对象。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
| `s17-pyfcstm-role` | 原版贡献点仍是卡片堆砌，且“研究贡献”和“当前落地能力”没有并置；现已改成左右双表，左侧讲贡献，右侧讲 parser/runtime/symbolic/codegen/tooling 落地。 | `PPT_GUIDE.md` + `generate_ppt.py` | `fixed` |
