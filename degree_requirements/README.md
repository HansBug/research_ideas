# 博士毕业要求情报库

> 信息更新时间：`2026-06-16 17:20:00`（Asia/Shanghai）

本目录用于保存和整理 2022 级计算机学院**学术型博士**毕业 / 学位申请相关政策、邮件证据、非正式讨论线索和待补问题。它是毕业成果认定的证据库，不是行政最终解释；任何结论都必须能回到政策原文、老师邮件或加密 raw 档案复核。

## 1. 核心结论速览

| 问题 | 当前结论 | 证据等级 | 主要依据 | 后续动作 |
|---|---|---|---|---|
| 我的身份口径是什么？ | 2022 级计算机学院学术型博士；学科口径按计算机科学与技术及软件工程相关学术型要求处理 | 🟢 | 用户确认；2024 版 / 新版候选 CS/SE 学术型文件 | 后续若学院给出更精确学科归属，再更新 |
| 2022 级可以按哪版成果要求？ | 老师邮件确认：2022 级博士生可在 2014 版与当前新版创新成果要求之间选择参照 | 🟢 | 2026-06-09 学院老师邮件，见 [email_threads/](./email_threads/) | 继续确认“最新版”具体文件和能否混用 |
| 2014 版现在能不能直接按传闻规划？ | 已取得 2014 版官方附件 PDF、研究生院 Wayback 快照与照片转录；计算机学院条款应按原文 `SCIE 2 篇` 或 `SCIE 1 篇 + EI/CPCI-S 2 篇且至少 1 篇为 EI 收录源期刊论文` 表述，不能再写口语化“2 SCI 或 1 SCI + 2 EI” | 🟢 | [2014_policy/README.md](./2014_policy/README.md)；官方附件 PDF；Wayback；照片 | 后续仍可向老师索取研究生院官方 docx/PDF 原件 |
| 当前新版候选主依据是哪份？ | 对学术型博士，主依据应是 CS/SE 学术型创新成果要求；实施细则用于流程；电子信息文件只作专业型对照 | 🟢 | [2024_policy/README.md](./2024_policy/README.md)、[2024_policy/notes.md](./2024_policy/notes.md) | 向老师确认它是否就是邮件所说“最新版” |
| 外部论文当前怎么处理？ | 保守方案：暂不把外部论文纳入毕业成果规划；2014 版与新版均有第一署名单位北航约束，除非老师邮件明确支持特殊例外 | 🟡 | 2014 版其他说明第 2 条；新版第一署名单位要求；非正式讨论线索 | 邮件确认外部论文和第一署名单位口径 |
| 新版对论文有哪些硬约束？ | 需与学位论文密切相关、投稿前导师审阅；第一作者/导师第一作者关系与第一署名单位北航；会议主会非从会；仅允许 1 篇录用状态且最高级别论文需已刊出；证明材料按状态准备 | 🟢 | CS/SE 学术型创新成果要求 Page 1-4 | 按当期学院清单准备证明材料 |
| 原始证据如何复核？ | 完整邮件/聊天 raw 已进入仓库内 AES-256 加密 zip；Markdown 只保留语义索引，不放逐字原文 | 🟢 | [encrypted_archives/](./encrypted_archives/)、[scripts/archive_tool.py](./scripts/archive_tool.py) | 本地 `source .env` 后用脚本读取；不要在文档/评论写出口令 |

## 2. 当前定位

- 服务对象：2022 级计算机学院学术型博士。
- 核心问题：毕业 / 学位申请创新成果可以按 2014 版还是当前新版执行，论文成果如何认定。
- 当前最高置信结论：2026-06-09 老师邮件确认 2022 级博士生可在 2014 版与当前新版创新成果要求之间选择参照。
- 当前最大缺口：研究生院官方 `.docx` 附件入口已定位但下载仍受验证码/会话限制；当前主依据为自动化学院官方附件 PDF、研究生院 Wayback 快照和用户拍照原文。

## 3. 阅读顺序

1. 先读 [GUIDE.md](./GUIDE.md)：理解证据等级、加密 raw 档案、邮件归档和政策解释规则。
2. 再读 [SUMMARY.md](./SUMMARY.md)：查看当前总账、政策版本、判定矩阵和待办。
3. 如需看 2024 版 / 新版候选原文，进入 [2024_policy/README.md](./2024_policy/README.md)。
4. 如需看 2014 版证据和补取计划，进入 [2014_policy/README.md](./2014_policy/README.md)。
5. 如需复核邮件或讨论证据，先看 [email_threads/README.md](./email_threads/README.md) 与 [discussions/README.md](./discussions/README.md)，再用 [scripts/archive_tool.py](./scripts/archive_tool.py) 读取 [encrypted_archives/](./encrypted_archives/) 中的加密 raw 档案。

## 4. 子目录说明

| 路径 | 作用 | 是否含原文 |
|---|---|---|
| [2014_policy/](./2014_policy/) | 2014 版政策 PDF、照片、Wayback 快照、转录和索取计划 | 含官方附件 PDF、照片与文本 |
| [2024_policy/](./2024_policy/) | 三份 2024 版 / 新版候选政策 PDF、提取文本和条款 notes | 含政策 PDF/TXT 明文 |
| [encrypted_archives/](./encrypted_archives/) | 邮件与聊天 raw 原始档案加密 zip | 含加密原文 |
| [email_threads/](./email_threads/) | 邮件线程语义索引，不放逐字原文 | 不放明文原文 |
| [discussions/](./discussions/) | 学长讨论语义索引，不放逐字原文 | 不放明文原文 |
| [scripts/](./scripts/) | 读取加密 raw 档案的本地工具 | 不含密码 |

## 5. 原始档案入库原则

- 原始邮件与聊天记录必须完整保存。
- 原始档案以 AES-256 加密 zip 入库，密码不写入仓库；本地通过 `.env` 的 `DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD` 配置。
- Markdown 只写语义索引、关键结论、证据等级、SHA256 和 zip 内文件名；不逐字展开邮件/聊天原文。
- 复核原文时先执行 `source .env`，再运行：

```bash
python degree_requirements/scripts/archive_tool.py archives
python degree_requirements/scripts/archive_tool.py list
python degree_requirements/scripts/archive_tool.py test
python degree_requirements/scripts/archive_tool.py show --member MANIFEST.txt
python degree_requirements/scripts/archive_tool.py extract --output /tmp/degree_raw_check
```

当前只有一个加密 zip 时脚本会自动选择；未来有多个 zip 时，使用 `--archive <zip 文件名>` 或本地 `.env` 中的 `DEGREE_REQUIREMENTS_ARCHIVE_FILE` 指定目标档案。仓库文档和 PR comment 不写任何可复制的口令赋值样式。

## 6. 更新日志

| 时间 | 修改 | 证据 |
|---|---|---|
| 2026-06-16 17:20:00 | 修正 2014 版正式口径与外部论文保守结论 | PR #116 |
| 2026-06-16 16:45:00 | 补充 2014 版政策官方附件 PDF、照片原文、Wayback 快照与逐字转录 | PR #116 |
| 2026-06-16 14:45:00 | 初始化博士毕业要求情报库，归档 2024 版 / 新版候选政策、邮件语义索引、讨论语义索引和加密 raw 档案 | PR #116 |
