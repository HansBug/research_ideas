# Judge efficiency report iter9 vs iter8A vs iter7

| run dir | pairs | reports | failed | calls | calls/report | in tok/report | out tok/report | USD | USD/report | repair-turn rate | arbitrated reports | wall min (total; per round) |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-- |
| `judge-calibration-5de564dad-v310` | 169 | 301 | 1 | 758 | 2.52 | 176,554 | 6,733 | 8.38 | 0.0279 | 24% | 36% | 88; baseline-r1:17, baseline-r1-resume175628:2, baseline-r2:12, baseline-r3:16, current-r1:30, current-r2:30, current-r3-resume181311:27 |
| `judge-calibration-45be62681-v39A` | 169 | 301 | 3 | 824 | 2.74 | 194,016 | 7,671 | 8.52 | 0.0283 | 42% | 89% | 207; baseline-r1:72, baseline-r2:42, baseline-r2-resume145104:15, baseline-r3:49, baseline-r3-resume150622:37, baseline-r3-resume154414:12, current-r1:92, current-r1-resume155729:7, current-r2:49, current-r2-resume151040:33, current-r2-resume154414:43, current-r3:38, current-r3-resume155654:68 |
| `judge-calibration-8313a632f-v38` | 169 | 301 | 0 | 814 | 2.70 | 189,942 | 7,394 | 9.49 | 0.0315 | 26% | 90% | 93; baseline-r1:14, baseline-r2:13, baseline-r3:15, current-r1:28, current-r2:38, current-r3:28 |

- `judge-calibration-5de564dad-v310` calls by phase: relation_arbitration=64, relation_primary=276, validity_arbitration=78, validity_primary=340
- `judge-calibration-45be62681-v39A` calls by phase: relation_arbitration=59, relation_primary=272, validity_arbitration=151, validity_primary=342
- `judge-calibration-8313a632f-v38` calls by phase: relation_arbitration=47, relation_primary=268, validity_arbitration=157, validity_primary=342
