# Full-population comparison: `judge-full-3a1ba5cf1-iter6cfg`

## current

- pair-rounds judged: 162; reports judged and matched to human decisions: 1271; human reports in scope not judged: 0; ledger ids in scope: 145
- K/N/I agreement: **957/1271 = 75.3%**
- K/N/I counts: judge K 628 / N 277 / I 366; human K 749 / N 231 / I 291
- report precision (K+N)/all: judge 71.2%; human 77.1%
- hit@1 FULL units: judge 292/435 = 67.1%; human 310/435 = 71.3%
- hit@3 (any round): judge 119/145; human 119/145
- hit@all (every judged round): judge 75/145; human 86/145

| judge \ human | K | N | I |
| :-- | --: | --: | --: |
| **K** | 596 | 10 | 22 |
| **N** | 63 | 153 | 61 |
| **I** | 90 | 68 | 208 |

disagreements by (human → judge, judge defect): N→I/D0=58, K→I/A0_FALSE_POSITIVE=41, K→I/D0=38, I→N/D1=37, K→N/D2=33, K→N/D1=30, I→N/D2=24, K→I/A0_NOT_A_DEFECT_CLAIM=11, N→I/A0_FALSE_POSITIVE=8, N→K/D1=8, I→K/D1=8, I→K/D2=6

## baseline

- pair-rounds judged: 162; reports judged and matched to human decisions: 512; human reports in scope not judged: 0; ledger ids in scope: 145
- K/N/I agreement: **388/512 = 75.8%**
- K/N/I counts: judge K 293 / N 134 / I 85; human K 312 / N 105 / I 95
- report precision (K+N)/all: judge 83.4%; human 81.4%
- hit@1 FULL units: judge 225/435 = 51.7%; human 227/435 = 52.2%
- hit@3 (any round): judge 105/145; human 106/145
- hit@all (every judged round): judge 47/145; human 46/145

| judge \ human | K | N | I |
| :-- | --: | --: | --: |
| **K** | 269 | 13 | 11 |
| **N** | 27 | 71 | 36 |
| **I** | 16 | 21 | 48 |

disagreements by (human → judge, judge defect): I→N/D2=18, I→N/D1=18, N→I/D0=16, K→N/D2=14, K→N/D1=13, K→I/D0=11, N→K/D2=7, K→I/A0_FALSE_POSITIVE=5, N→K/D1=5, N→I/A0_FALSE_POSITIVE=5, I→K/D2=5, I→K/D0=5

