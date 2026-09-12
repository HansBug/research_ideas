# Current invalid attribution v1

Evaluation-only overlay; v4 current decisions and headline are unchanged.

## Primary attribution counts

| category | count | reports rate | invalid rate |
|---|---:|---:|---:|
| `CONVERSION_LOWERING_CONFIRMED` | 0 | 0.0000% | 0.0000% |
| `COMPILER_OWNED_ARTIFACT_CONFIRMED` | 38 | 2.9898% | 13.0584% |
| `PROJECTION_TRACE_BOUNDARY_CONFIRMED` | 24 | 1.8883% | 8.2474% |
| `RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED` | 48 | 3.7766% | 16.4948% |
| `SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED` | 53 | 4.1699% | 18.2131% |
| `D0_NONVIOLATION_CONFIRMED` | 120 | 9.4414% | 41.2371% |
| `ATTRIBUTION_INDETERMINATE` | 8 | 0.6294% | 2.7491% |

All current I: 291; NADC: 118; conversion-confirmed: 0.

The conversion-confirmed numerator is zero unless a report has a concrete source absence/semantic mismatch plus a matching lowering/loss/ownership record. Identity-only traces, opaque labels, unsupported receipts and FCSTM-only facts are not sufficient.

## Cross-tabs

The following tables are deterministic projections of `i_attribution_summary_v1.json` and are diagnostic only.

### Round

| round | count |
|---:|---:|
| 1 | 85 |
| 2 | 105 |
| 3 | 101 |

### D tier

| D tier | count |
|---|---:|
| A0 | 171 |
| D0 | 120 |

### W level

| W level | count |
|---|---:|
| W1 | 138 |
| W2 | 153 |

### Predicate ID (correlation only)

| predicate | count |
|---|---:|
| G2 | 1 |
| NONE | 58 |
| R2 | 32 |
| S2 | 61 |
| S3 | 24 |
| S5 | 109 |
| V4 | 6 |

### Pair coverage

| pair | count |
|---|---:|
| 0001 | 1 |
| 0002 | 1 |
| 0003 | 6 |
| 0004 | 17 |
| 0005 | 20 |
| 0006 | 3 |
| 0009 | 4 |
| 0010 | 1 |
| 0012 | 5 |
| 0014 | 13 |
| 0015 | 7 |
| 0016 | 11 |
| 0019 | 1 |
| 0020 | 6 |
| 0021 | 1 |
| 0022 | 1 |
| 0024 | 13 |
| 0025 | 7 |
| 0026 | 3 |
| 0029 | 6 |
| 0030 | 1 |
| 0032 | 4 |
| 0033 | 7 |
| 0034 | 8 |
| 0036 | 4 |
| 0037 | 3 |
| 0039 | 8 |
| 0040 | 3 |
| 0042 | 1 |
| 0043 | 4 |
| 0044 | 23 |
| 0045 | 14 |
| 0046 | 1 |
| 0049 | 16 |
| 0050 | 1 |
| 0051 | 1 |
| 0052 | 6 |
| 0053 | 2 |
| 0054 | 16 |
| 0055 | 9 |
| 0056 | 3 |
| 0057 | 1 |
| 0059 | 28 |

## I composition and precision-gap decomposition

I is an invalid-report disposition, not a count of independent domain defects. The current 291 records comprise D0 non-violations, ordinary source-level false positives and NADC; the 189 diagnostic clusters are descriptive only.

| component | current | baseline | current-baseline rate difference |
|---|---:|---:|---:|
| D0 | 120/1271 = 9.44% | 85/512 = 16.60% | -7.16 pp |
| ordinary source-level FP | 53/1271 = 4.17% | 10/512 = 1.95% | +2.22 pp |
| NADC | 118/1271 = 9.28% | N/A (not classified in baseline-v3) | not comparable |
| total I rate | 291/1271 = 22.90% | 95/512 = 18.55% | +4.34 pp |

The component sum is an arithmetic, side-specific rate decomposition, not a counterfactual causal attribution. Baseline has no isomorphic NADC output category because it does not expose the current projection/backend contract; this missing classification must not be read as zero method risk. If the missing baseline cell is mechanically coded as zero for bookkeeping, the residual is +9.28 pp, but that residual is not a comparable cross-arm component.

## Headline boundary

Current report-level validity precision remains 980/1271 = 77.10%; baseline remains 417/512 = 81.45%. All 291 current invalid outputs remain in the primary denominator. No counterfactual precision without the projection is inferred.
The current NADC pool is 118/1271 = 9.2840% (110 confirmed method mechanisms plus 8 attribution-indeterminate records); it is a diagnostic partition, not a replacement precision definition. Strict conversion-lowering-confirmed count is 0.

## Paper-facing wording

> Under the frozen report-level protocol, the proposed method achieves higher ledger-relative discovery coverage, with FULL hit@1 improving from 52.18% to 71.26%, at the cost of a 4.34-percentage-point decrease in report-level validity precision (77.10% vs. 81.45%). The 291 invalid reports are heterogeneous: they include source-level non-violations, ordinary source-level false positives, and method-owned compiler-artifact, projection-boundary, runtime/evidence-closure, and indeterminate dispositions. We retain all of them in the precision denominator because they are user-visible costs of the end-to-end method. The frozen audit identifies no confirmed lowering-only error and therefore does not support attributing the precision gap predominantly to PlantUML-to-FCSTM conversion.
