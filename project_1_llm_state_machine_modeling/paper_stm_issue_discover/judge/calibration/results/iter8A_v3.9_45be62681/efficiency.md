# Judge efficiency report iter8 A/B vs iter7

| run dir | pairs | reports | failed | calls | calls/report | in tok/report | out tok/report | USD | USD/report | repair-turn rate | arbitrated reports | wall min (total; per round) |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-- |
| `judge-calibration-45be62681-v39A` | 169 | 301 | 3 | 824 | 2.74 | 194,016 | 7,671 | 8.52 | 0.0283 | 42% | 89% | 207; baseline-r1:72, baseline-r2:42, baseline-r2-resume145104:15, baseline-r3:49, baseline-r3-resume150622:37, baseline-r3-resume154414:12, current-r1:92, current-r1-resume155729:7, current-r2:49, current-r2-resume151040:33, current-r2-resume154414:43, current-r3:38, current-r3-resume155654:68 |
| `judge-calibration-45be62681-v39B` | 169 | 301 | 1 | 747 | 2.48 | 83,803 | 6,419 | 4.82 | 0.0160 | 46% | 41% | 191; baseline-r1:71, baseline-r2:48, baseline-r2-resume145104:13, baseline-r3:45, baseline-r3-resume150423:39, baseline-r3-resume154414:7, current-r1:89, current-r2:41, current-r2-resume150740:9, current-r2-resume154414:34, current-r3:48, current-r3-resume155654:53 |
| `judge-calibration-8313a632f-v38` | 169 | 301 | 0 | 814 | 2.70 | 189,942 | 7,394 | 9.49 | 0.0315 | 26% | 90% | 93; baseline-r1:14, baseline-r2:13, baseline-r3:15, current-r1:28, current-r2:38, current-r3:28 |

- `judge-calibration-45be62681-v39A` calls by phase: relation_arbitration=59, relation_primary=272, validity_arbitration=151, validity_primary=342
- `judge-calibration-45be62681-v39B` calls by phase: relation_arbitration=62, relation_primary=264, validity_arbitration=81, validity_primary=340
- `judge-calibration-8313a632f-v38` calls by phase: relation_arbitration=47, relation_primary=268, validity_arbitration=157, validity_primary=342
