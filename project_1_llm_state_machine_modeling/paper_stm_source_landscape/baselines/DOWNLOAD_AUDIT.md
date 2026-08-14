# 下载审计

本文件汇总 #95 下载审计事实与 #97 / #85 的使用边界。下载事实来源为 #95 Gist 的 `issue95_fulltext_download_audit_438papers.csv`，不是本 PR 新下载。

## 1. #95 全量下载状态

| 下载状态（原始代码） | 数量 |
|---|---:|
| `exists_old` | 28 |
| `fail` | 63 |
| `no_public_pdf_url_discovered` | 288 |
| `ok` | 59 |

- 已进入自动结构分析的全文样本：`87`。
- #95 自动流程的 PDF/TXT 不在本目录重复提交；#97 的 P0/P1 源材料进入 `survey_baseline_library/` 单篇目录。

## 2. #85 初筛子集下载状态

| #95 全文状态 | 数量 |
|---|---:|
| `⚠️ 未取得公开 PDF/CLI 受限` | 44 |
| `✅ 已下载解析公开 PDF` | 25 |

## 3. 使用边界

1. `download_status=ok / exists_old` 只能说明 #95 自动流程取得并解析过公开 PDF，不等于 #85 已人工读完。
2. `no_public_pdf_url_discovered` 或失败并不代表论文不可获取；用户可通过校园网、浏览器、作者页或图书馆访问。
3. P0/P1 人工下载优先队列见 [MANUAL_DOWNLOAD_REQUESTS.md](./MANUAL_DOWNLOAD_REQUESTS.md)。


## 4. 字段级下载拆分事实

当前 `screening_audit.csv` 与 `issue85_narrowed_related_candidates_preliminary.csv` 已拆分记录 `public_pdf_url_state / auto_fulltext_state / download_failure_reason / pdf_url / pdf_url_source / pdf_access_status / pdf_status_source`。这些字段只表示 #95 自动流程和公开入口状态；人工下载与全文核验仍以 [MANUAL_DOWNLOAD_REQUESTS.md](./MANUAL_DOWNLOAD_REQUESTS.md) 的 request ledger 为准。

## 5. 用户本地私有全文 receipt

用户已通过 Zotero / 本地导出目录提供 P0/P1 共 `25` 篇 PDF。本 paper 内部文库保存这些 PDF 和抽取文本；同时在 [../survey_baseline_library/data/local_fulltext_receipt.csv](../survey_baseline_library/data/local_fulltext_receipt.csv) 记录相对路径、短哈希、页数、抽取状态和版权安全说明。全文级初检结果见 [../survey_baseline_library/SUMMARY.md](../survey_baseline_library/SUMMARY.md)。
