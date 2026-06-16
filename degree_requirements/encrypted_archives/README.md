# 加密 raw 原始档案

> 信息更新时间：`2026-06-16 14:45:00`（Asia/Shanghai）

本目录保存邮件与聊天原始档案的加密 zip。zip 内原文完整保留，不做脱敏、不改写。zip 使用 AES-256 加密；口令不写入仓库，由本地 `.env` 的 `DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD` 环境变量提供。

## 1. 档案文件

| 文件 | SHA256 | 生成时间 | 加密方式 | 内容 |
|---|---|---|---|---|
| [2026-06-16-degree-requirements-raw-archive.zip](./2026-06-16-degree-requirements-raw-archive.zip) | `339054de371380e3aa88148c84f29a0f9b67fe7f040e943b005c2d52283a6db4` | 2026-06-16 15:24:00 | AES-256 ZIP（pyzipper WZ_AES） | 三封邮件 raw、邮件 meta/body、fetch summary、高年级同学/学长讨论 raw、MANIFEST、SHA256SUMS |

## 2. 读取方式

```bash
source .env
python degree_requirements/scripts/archive_tool.py list
python degree_requirements/scripts/archive_tool.py test
python degree_requirements/scripts/archive_tool.py show --member MANIFEST.txt
python degree_requirements/scripts/archive_tool.py extract --output /tmp/degree_raw_check
```

## 3. zip 内文件清单

| 文件 | 说明 |
|---|---|
| `email_threads/degree-mail-001.raw.eml` | 2026-05-26 发出咨询邮件 raw |
| `email_threads/degree-mail-002.raw.eml` | 2026-06-07 再次咨询邮件 raw |
| `email_threads/degree-mail-003.raw.eml` | 2026-06-09 老师回复邮件 raw |
| `email_threads/degree-mail-001.meta.json` 等 | 邮件 header / meta 辅助信息 |
| `email_threads/degree-mail-001.body.txt` 等 | 邮件正文辅助提取 |
| `email_threads/fetch_summary.safe.json` | worker 生成的安全索引摘要 |
| `discussions/2026-06-16-senior-student-policy-discussion.raw.md` | 高年级同学/学长讨论 raw |
| `MANIFEST.txt` | zip 内文件列表 |
| `SHA256SUMS.txt` | zip 内文件 SHA256 |

## 4. 更新日志

| 时间 | 修改 | 说明 |
|---|---|---|
| 2026-06-16 14:45:00 | 初始化加密 raw 档案 | 原始邮件和讨论 raw 以加密 zip 入库 |
