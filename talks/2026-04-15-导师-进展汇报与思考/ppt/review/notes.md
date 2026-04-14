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
