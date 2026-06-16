# 2014 版《北京航空航天大学关于申请博士学位发表论文的规定》

> 信息更新时间：`2026-06-16 17:20:00`（Asia/Shanghai）

## 1. 当前状态

2014 版政策原文已经通过三路证据入库：

1. **官方附件 PDF（当前主依据）**：从自动化学院官方通知附件下载得到 [source_pdfs/2014-buaa-phd-publication-requirements-official-attachment.pdf](./source_pdfs/2014-buaa-phd-publication-requirements-official-attachment.pdf)，文件头为 `PDF-1.7`，共 7 页；已用仓库 `venv` 与 `tools.pdf_extractor.py` 文字模式提取为 [extracted_text/2014-buaa-phd-publication-requirements-official-attachment.txt](./extracted_text/2014-buaa-phd-publication-requirements-official-attachment.txt)。
2. **研究生院官方页面快照**：研究生院原页面 `https://graduate.buaa.edu.cn/info/1039/6007.htm` 当前 404，但 Wayback 快照仍可见正文与官方 `.docx` 附件入口；本地快照见 [web_evidence/wayback_graduate_6007_20240727053355.html](./web_evidence/wayback_graduate_6007_20240727053355.html)，抽取文本见 [extracted_text/2014-buaa-phd-publication-requirements-wayback-text.txt](./extracted_text/2014-buaa-phd-publication-requirements-wayback-text.txt)。
3. **用户拍照原文证据**：12 张纸质文件照片已入库到 [source_images/](./source_images/)，并合成为非官方便读 PDF [source_pdfs/2014-policy-photo-bundle-nonofficial.pdf](./source_pdfs/2014-policy-photo-bundle-nonofficial.pdf)；照片逐字转录见 [extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md](./extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md)。

当前毕业规划可引用 2014 版条款，但仍建议后续向学院老师索取研究生院官方 `.docx` 或 PDF 原件，用于替代自动化学院附件副本与 Wayback 快照。

## 2. 与本用户最相关的计算机学院条款

按 2014 版第 4 条“计算机科学与技术、软件工程、网络空间安全学科（计算机学院）”：

- 申请者在相关学科领域的国内外重要学术期刊或学术会议上发表论文不少于 3 篇，其中至少 1 篇用外文撰写。
- 基本要求满足以下两个条件之一：
  1. 在 SCIE 收录源刊物上发表 2 篇论文；
  2. 在 SCIE 收录源刊物上发表 1 篇论文，另外在 EI 或 CPCI-S 收录源刊物上发表 2 篇论文，其中至少 1 篇为 EI 收录源期刊论文。
- 免盲审要求满足以下三个条件之一：
  1. 在 SCIE 收录源期刊上发表 1 篇论文的影响因子达到 1.5（含）以上；
  2. 在计算机学会推荐 A 类或 B 类期刊上 1 篇论文已刊出；
  3. 在计算机学会推荐 A 类会议上 1 篇论文已发表。

注意：2014 版原文使用 `SCIE`，不是口语中的 `SCI`；后续写毕业规划时应使用原文术语。

## 3. 关键共性约束

2014 版“二、其他说明”中对毕业规划影响较大的条款包括：

- 论文及其他学术成果均应与申请者学位论文密切相关，投稿前应经指导教师审阅同意。
- 除有明确规定的学科外，申请者必须是论文第一作者，或申请者为第二作者时其指导教师（含副指导教师）是第一作者；第一作者及申请者的第一署名单位只能是北京航空航天大学。
- 联合培养博士生存在最多 1 篇合作方导师 / 合作方第一署名单位相关例外。
- “发表”包含学术期刊论文已刊出或正式录用；学术会议论文已公开发表并收入论文集。
- 允许仅有 1 篇期刊论文处于录用状态，但各要求中级别最高的一篇必须正式刊出。
- 即将达到最长学习年限时存在“先毕业、暂缓审议学位、24 个月内补齐论文”的特殊机制。
- 同一篇论文或成果原则上不能用于申请两个学位。
- 共同第一作者论文按权重折算，且用于申请学位的论文合计不超过 1 篇；特殊情况需导师认定、共同一作声明与分委员会审核。
- 本规定自 2014 年入学的研究生开始实施，解释权在校学位办公室。

## 4. 证据文件总表

| 文件 | 类型 | SHA256 | 说明 |
|---|---|---|---|
| [source_pdfs/2014-buaa-phd-publication-requirements-official-attachment.pdf](./source_pdfs/2014-buaa-phd-publication-requirements-official-attachment.pdf) | 官方附件 PDF | `8eef9889dc2cca6b7c8b61cfd12914e6dfc9ec0aa6dc1e7616987134350737de` | 从自动化学院官方附件入口通过验证码下载；PDF 元数据显示 WPS 文字，7 页 |
| [extracted_text/2014-buaa-phd-publication-requirements-official-attachment.txt](./extracted_text/2014-buaa-phd-publication-requirements-official-attachment.txt) | PDF 提取文本 | `bdded02c16ac0903b427ee02d22a20afb129b63c1f9efaea454496e916bfbc5b` | 使用 `tools.pdf_extractor.py -m text` 提取 |
| [source_pdfs/2014-policy-photo-bundle-nonofficial.pdf](./source_pdfs/2014-policy-photo-bundle-nonofficial.pdf) | 照片合订 PDF（非官方） | `c091fa9d1f582f56eb41de78233d7ab3afe3874fa17f04cccc2b8f39551c6848` | 由 12 张用户拍照图片合成，方便翻阅，不替代官方 PDF |
| [extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md](./extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md) | 照片逐字转录 | `8aab6f54be41dd53301e39c4da1fc53f8409c7695fc4e09040bda1355369f700` | 仅转录印刷原文，未转录手写批注 |
| [extracted_text/2014-buaa-phd-publication-requirements-wayback-text.txt](./extracted_text/2014-buaa-phd-publication-requirements-wayback-text.txt) | 研究生院 Wayback 页面抽取文本 | `0a32652be8fcb80abaa504d6e277ae7b57f1d1d1f7a52f5f5f6d629bde790fd2` | 官方页面快照抽取，包含页面正文与附表文本 |
| [web_evidence/web_search_2026-06-16.md](./web_evidence/web_search_2026-06-16.md) | 线上检索记录 | `7970a327d73357ac2bc8a199d45551b35285f412fae6d67cab00b81b142aebe9` | 记录研究生院列表、Wayback、自动化学院附件、验证码阻塞与人工验证码下载成功 |

## 5. 照片页序与源图

| 页序 | 原始文件名 | 入库文件 | SHA256 |
|---|---|---|---|
| 01 | `微信图片_20260616162816_307_17.jpg` | [2014-policy-photo-page-01-307.jpg](./source_images/2014-policy-photo-page-01-307.jpg) | `227f6a440816aeb388236b97e68523a45397d1933197997d61cb666e5a0fe163` |
| 02 | `微信图片_20260616162820_308_17.jpg` | [2014-policy-photo-page-02-308.jpg](./source_images/2014-policy-photo-page-02-308.jpg) | `c5baa3809b696350e9705ccf52d0c8edf5ab2ac51fae90a93927d6d3ae68c41f` |
| 03 | `微信图片_20260616162824_309_17.jpg` | [2014-policy-photo-page-03-309.jpg](./source_images/2014-policy-photo-page-03-309.jpg) | `99e9b2a25cdc7807f11bcc2cb52b484e50f8e4a4571dbbf28ea223bcae8257c1` |
| 04 | `微信图片_20260616162828_310_17.jpg` | [2014-policy-photo-page-04-310.jpg](./source_images/2014-policy-photo-page-04-310.jpg) | `64afa9024f33fa33ddfd886378a57bc65e804673185a1a23c2fbd8b71f8a96dc` |
| 05 | `微信图片_20260616162832_311_17.jpg` | [2014-policy-photo-page-05-311.jpg](./source_images/2014-policy-photo-page-05-311.jpg) | `76f809a48031fa851b26868d543e0826653e7568544bbec4f420e0a365f6faa9` |
| 06 | `微信图片_20260616162835_312_17.jpg` | [2014-policy-photo-page-06-312.jpg](./source_images/2014-policy-photo-page-06-312.jpg) | `b1e747c5d9cc1bab11b1b18f8b16b9d6dc73dded4ef991281c55ba09a5147e4a` |
| 07 | `微信图片_20260616162839_313_17.jpg` | [2014-policy-photo-page-07-313.jpg](./source_images/2014-policy-photo-page-07-313.jpg) | `a939d88020f1edf0d1d86184bdf2486d6ea93441d97f18565e203fb3b710c3f8` |
| 08 | `微信图片_20260616162843_314_17.jpg` | [2014-policy-photo-page-08-314.jpg](./source_images/2014-policy-photo-page-08-314.jpg) | `1700f268acde683fabe1b5c2746addd8bec3d70fabf52f262cd808a4f1c6bf54` |
| 09 | `微信图片_20260616162847_315_17.jpg` | [2014-policy-photo-page-09-315.jpg](./source_images/2014-policy-photo-page-09-315.jpg) | `5c49932ad9e359e618b50ea0dbb80f1aaf901f75fbbfa8cc965f91a06f11be4f` |
| 10 | `微信图片_20260616162851_316_17.jpg` | [2014-policy-photo-page-10-316.jpg](./source_images/2014-policy-photo-page-10-316.jpg) | `173e9ef6dea856dd9802168870f88b944fc85a7eb68bde4518afb89f4a66002f` |
| 11 | `微信图片_20260616162855_317_17.jpg` | [2014-policy-photo-page-11-317.jpg](./source_images/2014-policy-photo-page-11-317.jpg) | `3f1cc7667c47e9b0a874bb8030e4dcf350acad44943717338c9f33c5a7a9d588` |
| 12 | `微信图片_20260616162858_318_17.jpg` | [2014-policy-photo-page-12-318.jpg](./source_images/2014-policy-photo-page-12-318.jpg) | `2eb596dd51db9315579841036152f7527faeaf424d866a6561becd0c9b3536c7` |

## 6. 待补与复核

| 优先级 | 待办 | 原因 | 状态 |
|---|---|---|---|
| P0 | 后续 reviewer 对 [source_images/](./source_images/) 与 [extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md](./extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md) 做逐字视觉复核 | 用户明确要求 codex / claude reviewer 做视觉核对 | 待 review |
| P0 | 用官方附件 PDF 文本与照片转录交叉核对计算机学院条款、第一署名单位、录用/刊出、共同一作等关键段落 | 这些条款直接影响毕业规划 | 待 review |
| P1 | 向老师索取研究生院官方 `.docx` 或 PDF 原件 | 研究生院附件入口存在但自动下载未成功 | 待邮件 |
| P1 | 如获得官方 `.docx`，重新提取并更新本目录 | 形成更高可信主源 | 待文件 |

## 7. 更新日志

| 时间 | 修改 | 说明 |
|---|---|---|
| 2026-06-16 18:20:00 | 修正照片转录数学学科条款 | 根据 claude reviewer 视觉逐字核对补回 `MEDLINE 收录源刊物` 的“源”字，并同步转录 SHA256 |
| 2026-06-16 17:20:00 | 补齐检索记录 hash 与复核规则 | 明确 web evidence SHA256、研究生院 docx 待补与视觉逐字复核要求 |
| 2026-06-16 16:45:00 | 入库 2014 版政策 PDF、照片、Wayback 快照与转录 | 自动化学院附件 PDF 已下载；研究生院 Wayback 页面与用户照片作为交叉证据 |
| 2026-06-16 14:45:00 | 初始化 2014 版待补记录 | 明确当时官方原件待补与非正式线索边界 |
