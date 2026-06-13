# artifacts: unified-uml-multimodal-validation

## 本地文件

| 文件 | 状态 | 说明 |
|---|---|---|
| `paper.pdf` | present | TechScience PDF。 |
| `paper_content.txt` | present | text 模式抽取 28 页。 |
| `hf_state_dataset_record.json` | present | HF dataset API record。 |
| `hf_state_dataset_tree.json` | present | HF repo tree。 |
| `umlcode_state_diagram_train.parquet` | present | HF state diagram train split，999 rows。 |
| `hf_state_dataset_sample.json` | present | 前 5 行 preview；含 `uml_code_complete` 标记，便于 reviewer 快速检查，但 row-level parse/render 仍以 parquet 本体为准。 |

## 外部入口

| 入口 | URL | 说明 |
|---|---|---|
| DOI | https://doi.org/10.32604/cmes.2025.075442 | publisher landing。 |
| HTML | https://www.techscience.com/CMES/v146n1/65740/html | 全文 HTML。 |
| HF state dataset | https://huggingface.co/datasets/nguyenvanviet/UMLCode_StateDiagram | public state subset。 |
| HF 总入口 | https://huggingface.co/nguyenvanviet/datasets | 作者数据集索引。 |

## artifact 判定

当前为 `SA-2`：公开、可下载、可 hash、state subset 可隔离；但 dataset license 未在 HF API card 中明确出现，且正式进入 R2 前仍需 row-level parse / render / duplication 抽检。
