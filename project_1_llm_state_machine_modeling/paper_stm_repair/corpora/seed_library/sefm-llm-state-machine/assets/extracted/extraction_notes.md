# extraction_notes

## 1. 抽取命令 / 脚本

本次抽取使用 Python 标准库 `zipfile` 读取 `assets/raw/llm_state_machine_modeling_4open.zip`，用 `ast.parse` / `ast.literal_eval` 从 `backend/resources/state_machine_descriptions.py` 提取 `SSC7_fall_2024` 字符串，并直接读取 `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_f700645345f84b5acffd751f426344ed704910d9.txt` 作为 generated `STM_0`。

## 2. 人工步骤（如有）

人工核对 ZIP 文件列表，确认：

- `backend/resources/state_machine_descriptions.py` 包含 `SSC7_fall_2024`；
- `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_f700645345f84b5acffd751f426344ed704910d9.txt` 是 Claude Sonnet 3.5 single-prompt generated output；
- `Paper Experiment Resources/Reference Solutions/*.txt` 是 reference solution，不计入 generated seed。

## 3. 异常与降级

没有抽取 8 个 reference solution 作为 generated pair；它们仅保留在 registry 的 `reference_sets`。当前只登记 SSC7 generated pair，不声称整个 4open artifact 的所有生成策略 / 所有系统均已完成抽取。

## 4. 不可提交内容说明（redaction、local_only、公开资源引用）

ZIP 已提交到 `assets/raw/` 用于仓库内复验；公开学术 artifact 按引用原作处理，许可 / 再分发不再作为升绿 blocker。本条目当前为 `final_pool_ready`，但只表示 SSC7 这一组 generated pair 可回溯复验；其余 8 个 NL 描述缺 generated text output，不能计为 generated pair。

## 5. 校验结果摘要

- raw asset count: 1
- pair count: 1
- trace verified pair count: 1
- eligible generated pair count: 1
- raw ZIP sha256: `0e553383b5bd03702d29e5f68a3624fcc143a51da1fd0c9156b32ba51a5b61b4`
- NL sha256: `a9803b9514ffe57d80c266a3c390298ca04e471d300c690045bb4479872ec1a8`
- STM_0 sha256: `22aa85b151d2802084a41096bb9f3bec6a6d3c6c8d50e7c63626db2f0f66e8b4`
