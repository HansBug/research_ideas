# 恢复来源

原始 ledger 在 2026-07-29 重装系统时丢失（未被 git 跟踪）。此文件由 Issue #166 正文所链接的
证据 gist 恢复：

- gist: https://gist.github.com/HansBug/024ff833314ea6c3d30342290eda5906
- 文件: `ledger.json`（370994 字节，API 报 `truncated=false`）
- 校验: SHA-256 `03d8756650c079229dacb7fc2d7700ca98fda44f3c4648fd308e4f8e24ac955e`，
  与 Issue #166 正文「机器总账 SHA-256」逐字符一致

先前判断「原件无法从仓库、已发布 bundle 或文件系统恢复」是错的——它一直在 Issue #166
正文的链接里。`expected_issues_reconstructed.json`（仅覆盖 4 个 pair）自此仅作历史记录，
代码优先使用本文件。

覆盖范围：60 个 case、47 条 E1 expected issue、29 个 pair 含 expected issue。
category 分布：IT 17、TR 9、SH 8、GC 8、UA 2、EA 2、DA 1、TO 0。
case status：candidate_only 19、mixed 18、expected_issues_found 11、
no_supported_finding 9、representation_boundary 3。
