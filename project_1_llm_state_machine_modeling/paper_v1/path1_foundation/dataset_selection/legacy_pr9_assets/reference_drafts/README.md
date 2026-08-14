# reference_drafts/：PR #9 historical ref-STM 草稿归档

本目录归档历史 PR #9 中的 reference STM pipeline 经验、CARA / CubeSat historical reference drafts、codex drafts 与辅助脚本。

## 文件说明

| 路径 | 内容 |
|---|---|
| [HANDOVER.md](./HANDOVER.md) | 历史 ref-STM pipeline 交班文档，包含 D1-D8 纪律和后续 Q1-Q5。 |
| [audited/](./audited/) | CARA 低-V 与 CubeSat 高-V historical reference draft。 |
| [codex_drafts/](./codex_drafts/) | 历史 Codex draft 输出及结果文件。 |
| [prompts/](./prompts/) | 历史 codex draft prompt 模板。 |
| [extract_components.py](./extract_components.py) / [verify_pyfcstm.py](./verify_pyfcstm.py) / [verify_pyfcstm_static.py](./verify_pyfcstm_static.py) | 历史辅助脚本，用于理解当时 ref pipeline，不是当前 main runtime 真源。 |

## 使用原则

- CARA / CubeSat draft 只能作为 reference discipline、few-shot 或 V-rich/V-poor 经验，不是最终 signed oracle。
- 如果后续正式实验使用这些 ref，需要重新走当前 pyfcstm 版本、component extraction、human adjudication 和 run record。
- 历史脚本可能与当前 `method/` / `eval/` 口径漂移；使用前必须重新核验。
