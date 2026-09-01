# Baseline inventory

- branch: `paper1/m-witness-discovery`
- HEAD: `9b512558123f305971e16746b9b48560c832cd6f`
- latest commit: `9b512558123f305971e16746b9b48560c832cd6f docs(paper1): attribute current invalid reports and gate rerun`
- execution scope: provider calls `0`; method reruns `0`; Judge reruns `0`

| fact | value | frozen source |
|---|---:|---|
| current reports | 1271 | current v4 decisions |
| baseline reports | 512 | baseline v3 summary (complete denominator) |
| expected issues | 145 | reference ledger |
| round-level units | 435 | current/baseline hit@1 denominators |
| current K/N/I | 749 / 231 / 291 | current v4 summary |
| baseline K/N/I | 312 / 105 / 95 | baseline v3 summary |
| current precision | 980/1271 = 77.10% | current v4 summary |
| baseline precision | 417/512 = 81.45% | baseline v3 summary |
| current FULL hit@1 | 310/435 = 71.26% | current v4 summary |
| baseline FULL hit@1 | 227/435 = 52.18% | baseline v3 summary |
| current I composition | D0=120; A0/FP=53; A0/NADC=118 | current v4 summary |
| baseline I composition | D0=85; A0/FP=10; A0/NADC=not classified (observed count 0) | baseline v3 summary |
| predicate usage | terminal receipts 12/19; report-bound IDs 8/19; report-bound rows 825/1271; legacy markers 303/825 | current v4 summary |

The baseline decision JSON is a reviewed non-K subset; baseline report count and K/N/I above intentionally come from the complete frozen summary. HEAD changed predicate narrative/evaluation-only documentation, not conversion code, source trace, raw reports, Judge rules or headline decisions.
