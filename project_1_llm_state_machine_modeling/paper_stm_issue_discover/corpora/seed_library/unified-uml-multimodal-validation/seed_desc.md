# A Novel Unified Framework for Automated Generation and Multimodal Validation of UML Diagrams

## R1.6 strict seed 全文 / artifact 核验结论

| 字段 | 结论 |
|---|---|
| bibliographic_id | DOI `10.32604/cmes.2025.075442`，CMES 2026 |
| strict_seed_grade | `SS-B` |
| artifact_usability | `SA-2` |
| R2.0 registry 角色 | `final_pool_ready`；989 条一手 synthetic PlantUML 生成对可由 HF parquet / locator / hash 回溯，10 条 failure 行作为 NL-only 排除。 |

## P1/P2/P3/P4 核验

| 谓词 | 判定 | 证据 |
|---|---|---|
| `P1_NL_INPUT` | 有条件通过 | 输入是 LLaMA-3.2-1B-Instruct 生成的 synthetic user-focused requirements / feature descriptions，不是真实人工需求。 |
| `P2_T0_STM_FAMILY` | 通过 | 论文覆盖六类 UML diagrams；HF 中存在独立 `UMLCode_StateDiagram` 数据集，字段为 `input / reasoning / uml_code`，999 rows。 |
| `P3_GENERATION_RELATION` | 通过 | DeepSeek-R1-Distill-Qwen-32B 将 requirements 转为 PlantUML code；论文 Algorithm 2 / 3 描述生成流程。 |
| `P4_EVIDENCE_POINTER` | 通过但有 caveat | DOI/PDF、HF API record、HF parquet、样例 JSON 与 SHA-256 已本地冻结；许可 / 再分发不作为升绿阻塞，核心 caveat 是 synthetic / non-control-domain 与无逐行 VLM/human score。 |

## Artifact / 数据核验

- HF dataset：`nguyenvanviet/UMLCode_StateDiagram`。
- HF API 显示 public / non-gated，999 rows，parquet，features 为 `input`、`reasoning`、`uml_code`。
- 本地下载：`umlcode_state_diagram_train.parquet`，大小 1,620,142 bytes，SHA-256 `02e99eef50ef722aa0c020fccbaeb59daa7cca0e303c247f50450c0eb26bc80d`。
- 抽样文件：`hf_state_dataset_sample.json` 是从 parquet 前 5 行生成的 preview，记录 `input_preview` / `uml_code_preview` / `uml_code_complete`；其中完整性判断以 parquet 本体、`assets/extracted/pairs.jsonl` 与 validator 为准，不能把 preview 当作完整事实源。

## SS / SA 解释

- `SS-B`：生成关系和 T0 state diagram subset 很强，但输入需求由 LLaMA 合成，不是现实控制系统 NL，也不是人工需求文档；因此不能标 `SS-A`。
- `SA-2`：state subset 可机器下载和冻结，适合作为 R2 synthetic smoke / stress seed；本轮已完成 NL 去重、failure 行识别和 locator/hash 回溯。后续若要进入论文主实验，还应按实验设计继续做 PlantUML parser/render 与领域适配抽检。

## R2 使用建议

1. 可把该数据集作为 **synthetic smoke / stress seed**：抽样时冻结 `input`、`uml_code`、row index、parquet hash、HF commit sha，再转换为本项目统一格式。
2. 明确标注 synthetic requirement 与 dataset-generation pipeline，不把它包装成真实工业 / 控制系统需求。
3. 当前一手 registry 口径为 `final_pool_ready`，但使用时必须保留 synthetic、非控制系统和无逐行 VLM/human score caveat。
