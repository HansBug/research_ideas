# `degree_requirements/` GUIDE

> 信息更新时间：`2026-06-16 17:20:00`（Asia/Shanghai）

本 GUIDE 规定博士毕业要求情报库的证据等级、政策解释优先级、邮件/讨论 raw 档案入库方式、更新流程和验收标准。

## 1. 目标与边界

本库应做：

1. 保存 2022 级学术型博士毕业 / 学位申请创新成果要求相关证据。
2. 区分政策原文、老师邮件、电话咨询、非正式讨论和待确认线索。
3. 保存完整 raw 证据，但 raw 邮件/聊天只以加密 zip 入库。
4. 在 Markdown 中提供完整语义抽取和证据索引，方便快速判断与后续复核。

本库不应做：

1. 不替代学院或学校的正式行政解释。
2. 不把 2014 版的口语化传闻或照片手写批注写成官方事实。
3. 不在 Markdown 中逐字展开邮件或聊天原文。
4. 不把专业型电子信息政策当作本用户学术型博士主依据。

## 2. 证据等级规则

| 等级 | 含义 | 示例 |
|---|---|---|
| 🟢 | 官方政策 PDF / 学院老师正式邮件 / 已邮件复核的官方答复 | 2026-06-09 老师邮件、2024 版政策 PDF |
| 🟡 | 学长或同学经验 / 微信讨论 / 电话咨询但未邮件复核 | 2026-06-16 学长讨论 |
| 🟠 | 网上搜索线索 / 候选入口 / 已定位但未成功取回的附件 | 研究生院 2014 版 `.docx` 附件入口 |
| ⚪ | 待确认或仅作为问题记录 | 待问老师问题 |

## 3. 政策解释优先级

1. 用户当前明确身份与口径。
2. 学院老师正式邮件。
3. 政策 PDF 原文。
4. 学校/学院官网正式页面。
5. 电话咨询、微信讨论、非正式讨论只作为线索；经邮件复核后可提升证据等级。

## 4. 加密 raw 档案规则

1. 邮件与聊天原始信息必须完整保存。
2. raw 文件以 AES-256 加密 zip 入库到 [encrypted_archives/](./encrypted_archives/)。
3. zip 密码不写入仓库；本地 `.env` 中使用 `DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD` 环境变量保存。
4. 加密 zip 不是单文件假设；后续可按日期、线程或材料批次新增多个 zip。脚本不得硬编码某一个 zip 文件名；多 zip 时必须通过 `--archive <zip 文件名>` 或本地 `.env` 中的 `DEGREE_REQUIREMENTS_ARCHIVE_FILE` 指定目标档案。
5. 仓库文档、PR body、PR comment、review comment 不得写出口令明文，也不得写任何可复制的口令赋值样式；只允许写变量名和安全描述。
6. 使用前必须在仓库根目录执行：

```bash
source .env
```

7. 读取 raw 档案统一使用 [scripts/archive_tool.py](./scripts/archive_tool.py)，脚本依赖 `pyzipper` 读取 AES-256 zip；其中 `archives` 列出当前可用 zip，`show --member` 用于不落盘读取单个 zip 内文件，`extract` 用于显式解压到本地临时目录：

```bash
python degree_requirements/scripts/archive_tool.py archives
python degree_requirements/scripts/archive_tool.py list
python degree_requirements/scripts/archive_tool.py test
python degree_requirements/scripts/archive_tool.py show --member MANIFEST.txt
python degree_requirements/scripts/archive_tool.py extract --output /tmp/degree_raw_check
```

8. Markdown 文件只写语义索引，不写逐字原文；每条索引必须能指向 zip 内 raw 文件名、SHA256 和证据等级。
9. 不维护“脱敏原文副本”，避免出现多个原文版本。

## 5. 邮件归档规则

1. 与毕业要求、创新成果、政策适用、论文认定相关邮件必须进入 [email_threads/](./email_threads/) 语义索引，并进入加密 zip raw 档案。
2. 同一邮件线程放入同一个 Markdown 索引文件。
3. 归档前尽量核验 `Subject`、`Message-ID`、`In-Reply-To`、`References` 或 IMAP 线程关系；无法证明同线程时标为“主题相近但线程关系待确认”。
4. 每封邮件索引至少包含：归档序号、方向、日期、主题、发件人角色、收件人角色、邮箱来源类别、zip 内 raw 文件名、SHA256、原文完整性状态、附件状态、证据等级、关键语义。
5. 发件邮件来源标为 `Sent Items` 或等价发件箱；收件邮件来源标为 `INBOX` 或等价收件箱。
6. 关键结论必须尽量保留原句核心意思，不能只写泛泛概括。

## 6. 电话咨询规则

若后续电话咨询老师或学院，应在事后立即记录：时间、对方角色、问题、答复要点、是否邮件复核。未经邮件复核的电话答复证据等级为 🟡；经邮件复核后可升为 🟢。

## 7. 2014 版原文与视觉转录规则

1. 2014 版当前已有官方附件 PDF、研究生院 Wayback 快照、用户拍照原文和逐字转录；后续毕业规划可引用原文条款，但仍应保留“研究生院官方 `.docx` / PDF 原件待补取”的待办。
2. 任何地方不得再写口语化“2 SCI 或 1 SCI + 2 EI”作为正式结论；必须按原文写 `SCIE 2 篇` 或 `SCIE 1 篇 + EI/CPCI-S 2 篇且至少 1 篇为 EI 收录源期刊论文`。
3. 对照片材料的转录必须只转录印刷原文，手写批注不得混入政策正文；如需记录批注，应单独建“批注说明”。
4. 后续 review 阶段，具备视觉能力的 reviewer 必须逐字对照 [2014_policy/source_images/](./2014_policy/source_images/) 与 [2014_policy/extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md](./2014_policy/extracted_text/2014-buaa-phd-publication-requirements-photo-transcription.md)；无视觉模态 reviewer 可审查官方 PDF 提取文本、证据链和表述一致性。
5. 若官方附件 PDF、照片转录、Wayback 文本之间存在差异，优先回到官方附件 PDF 原件；若仍不确定，标为待人工核验并邮件询问老师。

## 8. 外部论文保守规划规则

当前保守方案：暂不把外部论文纳入毕业成果规划。2014 版与新版均包含“第一作者及申请者第一署名单位只能是北京航空航天大学”这类约束；若后续老师邮件明确说明特殊外部合作、联合培养或历史版本适用例外，再修订。

## 9. 2024 版 / 新版候选版本核验规则

每份政策文件必须记录：正式文件名、适用对象、发布/生效日期（若原文有）、来源路径或 URL、抓取时间、SHA256、提取方式、页数/行数、是否被确认为截至核验日的最新版。若无法确认最新版，统一写为“2024 版 / 当前已取得新版候选”。

## 10. README 与 SUMMARY 纪律

[README.md](./README.md) 必须承担“入口即可决策”的职责：开头保留核心结论速览表，让读者不跳转也能看到身份口径、可选政策版本、2014 原文证据、新版候选主依据、外部论文保守口径、新版关键硬约束、raw 复核方式与后续动作。后续新增政策或邮件时，若改变任何毕业规划结论，必须同步更新 README 速览表。

[SUMMARY.md](./SUMMARY.md) 只做总账，不堆 PR 流水。至少保留：当前总览、政策版本总表、8 维判定矩阵、待问问题、更新日志。

## 11. 更新日志规则

所有更新日志表格按时间降序排列，最新记录置顶。

## 12. 更新日志

| 时间 | 修改 | 说明 |
|---|---|---|
| 2026-06-16 17:20:00 | 修正 2014 版制度化规则 | 明确官方附件 PDF / Wayback / 照片三路证据、SCIE/EI/CPCI-S 原文口径和 reviewer 视觉逐字核对要求 |
| 2026-06-16 16:45:00 | 补充 2014 版原文与视觉转录规则 | 固化 SCIE 原文口径、照片转录边界和 reviewer 视觉核对要求 |
| 2026-06-16 14:45:00 | 初始化 GUIDE | 建立证据等级、加密 raw 档案、邮件归档和政策证据补取规则 |
