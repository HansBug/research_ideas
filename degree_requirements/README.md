# 博士毕业要求情报库

> 信息更新时间：`2026-06-16 14:45:00`（Asia/Shanghai）

本目录用于保存和整理 2022 级计算机学院**学术型博士**毕业 / 学位申请相关政策、邮件证据、非正式讨论线索和待补问题。它是毕业成果认定的证据库，不是行政最终解释；任何结论都必须能回到政策原文、老师邮件或加密 raw 档案复核。

## 1. 当前定位

- 服务对象：2022 级计算机学院学术型博士。
- 核心问题：毕业 / 学位申请创新成果可以按 2014 版还是当前新版执行，论文成果如何认定。
- 当前最高置信结论：2026-06-09 老师邮件说明老师答复确认 2022 级博士生可在 2014 版与当前新版创新成果要求之间选择参照。
- 当前最大缺口：2014 版原文尚未取得。

## 2. 阅读顺序

1. 先读 [GUIDE.md](./GUIDE.md)：理解证据等级、加密 raw 档案、邮件归档和政策解释规则。
2. 再读 [SUMMARY.md](./SUMMARY.md)：查看当前总账、政策版本、判定矩阵和待办。
3. 如需看 2024 版 / 新版候选原文，进入 [2024_policy/README.md](./2024_policy/README.md)。
4. 如需看 2014 版缺口和索取计划，进入 [2014_policy/README.md](./2014_policy/README.md)。
5. 如需复核邮件或讨论证据，先看 [email_threads/README.md](./email_threads/README.md) 与 [discussions/README.md](./discussions/README.md)，再用 [scripts/archive_tool.py](./scripts/archive_tool.py) 读取 [encrypted_archives/](./encrypted_archives/) 中的加密 raw 档案。

## 3. 子目录说明

| 路径 | 作用 | 是否含原文 |
|---|---|---|
| [2014_policy/](./2014_policy/) | 2014 版政策原文缺口、索取计划和后续入库位置 | 暂无原文 |
| [2024_policy/](./2024_policy/) | 三份 2024 版 / 新版候选政策 PDF、提取文本和条款 notes | 含政策 PDF/TXT 明文 |
| [encrypted_archives/](./encrypted_archives/) | 邮件与聊天 raw 原始档案加密 zip | 含加密原文 |
| [email_threads/](./email_threads/) | 邮件线程语义索引，不放逐字原文 | 不放明文原文 |
| [discussions/](./discussions/) | 学长讨论语义索引，不放逐字原文 | 不放明文原文 |
| [scripts/](./scripts/) | 读取加密 raw 档案的本地工具 | 不含密码 |

## 4. 原始档案入库原则

- 原始邮件与聊天记录必须完整保存。
- 原始档案以 AES-256 加密 zip 入库，密码不写入仓库；本地通过 `.env` 的 `DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD` 配置。
- Markdown 只写语义索引、关键结论、证据等级、SHA256 和 zip 内文件名；不逐字展开邮件/聊天原文。
- 复核原文时先执行 `source .env`，再运行：

```bash
python degree_requirements/scripts/archive_tool.py list
python degree_requirements/scripts/archive_tool.py test
python degree_requirements/scripts/archive_tool.py show --member MANIFEST.txt
python degree_requirements/scripts/archive_tool.py extract --output /tmp/degree_raw_check
```

## 5. 更新日志

| 时间 | 修改 | 证据 |
|---|---|---|
| 2026-06-16 14:45:00 | 初始化博士毕业要求情报库，归档 2024 版 / 新版候选政策、邮件语义索引、讨论语义索引和加密 raw 档案 | PR #116 |
