# E2 逐格 JSON 审计原件

这里保存紧凑归档 `cells.json` 中每个格的两个直接来源：生成记录 `source` 与 Luna 裁定记录 `judge_source`。三款模型各 324 格，共 1944 个 JSON 文件、1,666,325,086 bytes；文件按原运行相对路径保留，便于从格记录跳转到完整的阶段输出、报告、诊断、两读和仲裁内容。

本目录不复制每次 HTTP/SSE 的 wire 原件，也不包含 `call_metadata/`、judge `llm/` 工作目录、`private/`、`__pycache__/` 或锁文件。需要逐调用网络事件时，仍按 E2 报告说明取得本地 ignored runs；这里的 JSON 是可直接查阅和审计的逐格研究原件。每个文件的源路径、字节数和 SHA-256 见 [`MANIFEST.json`](./MANIFEST.json)，manifest 的选择集合由对应模型的 `cells.json` 精确导出，不按发现数量筛选。

无 API 完整复算（含格覆盖、配对统计和损坏反例）仍从上级归档 README 的命令执行。逐格原件完整性可用标准库核对：

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
root = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/e2_20260907/raw")
manifest = json.loads((root / "MANIFEST.json").read_text())
for model in manifest["models"].values():
    for item in model["files"]:
        data = (root / item["path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
print(manifest["total_files"], manifest["total_bytes"])
PY
```
