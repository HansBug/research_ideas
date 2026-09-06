# artifacts: unified-uml-multimodal-validation

## 本地文件

| 文件 | 状态 | 说明 |
|---|---|---|
| `paper.pdf` | present | TechScience PDF。 |
| `paper_content.txt` | present | text 模式抽取 28 页。 |
| `hf_state_dataset_record.json` | present | HF dataset API record。 |
| `hf_state_dataset_tree.json` | present | HF repo tree。 |
| `umlcode_state_diagram_train.parquet` | present | HF state diagram train split，999 rows。 |
| `hf_state_dataset_sample.json` | present | 前 5 行 preview；含 `uml_code_complete` 标记，便于 reviewer 快速检查，但 R2.0 事实以 parquet 本体、`assets/extracted/pairs.jsonl` 与 validator 为准。 |

## 外部入口

| 入口 | URL | 说明 |
|---|---|---|
| DOI | https://doi.org/10.32604/cmes.2025.075442 | publisher landing。 |
| HTML | https://www.techscience.com/CMES/v146n1/65740/html | 全文 HTML。 |
| HF state dataset | https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram | public state subset。 |
| HF 总入口 | https://huggingface.co/nguyenvanviet/datasets | 作者数据集索引。 |

## artifact 判定

当前为 `final_pool_ready` / `SA-2`：公开、可下载、可 hash、state subset 可隔离；本轮已完成 NL 去重、failure 行识别、locator/hash 回溯与 validator 复验。许可 / 再分发不作为升绿阻塞；仍需保留 synthetic、非控制系统、无逐行 VLM/human score 等学术 caveat，后续主实验可继续做 PlantUML parser/render 抽检。
