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
- 本 PR 不提交这些 PDF/TXT，只记录元数据、状态和 SHA256。

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
