# story/：论文主线与 claim 控制

本目录维护 Path-1 第一篇论文的 story 真源。它回答“这篇论文到底讲什么、哪些 claim 可以写、哪些 claim 必须等实验完成后再写”。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | 论文 thesis、task boundary、gap、technical challenge、method insight、contributions 与 claims-to-avoid。 |
| [paper_outline.md](./paper_outline.md) | 在导师定调和 9 个五绿 direct baseline 反证压力下，固定章节大纲、RQ、反证门和投稿前证据门。 |
| [venue_readiness_gate.md](./venue_readiness_gate.md) | 固化 issue #67 的投稿策略：按 CCF-A 标准打磨，2026 夏季优先投 CCF-B 期刊，并定义 SoSyM / ASEJ / REJ 的 readiness gate。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 将每条潜在论文 claim 映射到当前证据状态，防止把计划或历史资产写成已完成结果。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认论文当前主线仍是 Path-1 baseline hard comparison。
2. 再读 [paper_outline.md](./paper_outline.md)，确认章节逻辑、RQ、9 个 direct baseline 反证门和证据门。
3. 再读 [venue_readiness_gate.md](./venue_readiness_gate.md)，确认当前投稿目标是按 CCF-A 审稿强度准备、优先投 CCF-B rolling journal。
4. 写 abstract / introduction / contribution 前，必须查 [claim_evidence_map.md](./claim_evidence_map.md)。
5. 任何依赖 frozen sample、human adjudication、baseline result 或 ablation 的结果型句子，在对应实验 gate 完成前只能写成 planned / to be evaluated。

## 边界

- `story/` 不保存实验数据和运行结果。
- 不能把 `dataset_selection/legacy_pr9_assets/` 中的历史 selection / expansion / ref draft 写成当前论文结果。
- 如果后续实验结果与当前 thesis 冲突，应先改本目录，再改 manuscript。
