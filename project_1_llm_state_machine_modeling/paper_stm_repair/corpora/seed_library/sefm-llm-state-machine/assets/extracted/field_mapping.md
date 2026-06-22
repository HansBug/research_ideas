# field_mapping

| extracted 字段 | raw 来源 |
|---|---|
| `source_asset_id` | `assets/manifest.json` 中的 `sefm_4open_zip` |
| `source_local_path` | `assets/raw/llm_state_machine_modeling_4open.zip` |
| `nl_text` | ZIP member `backend/resources/state_machine_descriptions.py` 中 Python 字符串 `SSC7_fall_2024` |
| `stm0_text` | ZIP member `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_f700645345f84b5acffd751f426344ed704910d9.txt` 的全文 |
| `source_locator_type` | `zip_python_symbol_and_text_file` |
| `source_locator` | `nl_member=backend/resources/state_machine_descriptions.py; nl_symbol=SSC7_fall_2024; stm0_member=Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_f700645345f84b5acffd751f426344ed704910d9.txt` |
| `generation_model_or_method` | 由文件路径 `Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt` 与论文方法共同支撑；reference solutions 不计入 generated `STM_0`。 |

本映射只登记一个作者原生 generated pair：SSC7 的自然语言系统描述与 Claude Sonnet 3.5 single-prompt 输出。`Paper Experiment Resources/Reference Solutions/*.txt` 是参考解，只能进入 `reference_sets`。
