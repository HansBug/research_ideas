# Track C Artifact and Positive-Control Precursor Audit

This is provenance-only. It does not select a predicate, typed inputs, gold status, or semantic verdict, and it does not execute a predicate.

## Result

- Reviewer: `pane5:track-c-artifact-positive-control-audit`
- Coverage: `145/145` ledger IDs across `46` pairs
- Provenance locator/hash closure: `145` PASS, `0` FAIL
- Candidate status: `UNVERIFIED_CANDIDATE_REFERENCE` for all `145` entries
- Approved positive controls: `0`; issue-specific repaired artifacts: `0`

Every candidate still requires materialization, obligation-equivalence review, attribution closure, precommitted property/inputs, a completed Boolean true receipt, and vacuity/contamination checks.

## Boundary

predicate_execution_count=0; v60_actual_predicate_artifacts_read=0; method_runs=0; judge_runs=0; provider_calls=0. This artifact audit assigns no predicate, typed input, exactness relation, gold status, or canonical verdict.

The workbook reference and the generic `pyfcstm` fixed fixture are not positive controls in this audit. The canonical per-ledger records and hashes are in the adjacent JSON files.

## Pair Coverage

| Pair | Ledger IDs | Reference candidate locator | Reference SHA-256 |
| --- | --- | --- | --- |
| 0000 | EIS-0000-01, EIS-0000-02, INS-0000-04 | Experiment Results.xlsx#STM Results!D2 | `sha256:9ecc1af98bd062bbf8c05f424a66065e4e15a5939b299f00a52e6b0c1415eaa0` |
| 0001 | INS-0001-02, VU-0001-01 | Experiment Results.xlsx#STM Results!D3 | `sha256:376b1eff602bfa346a3003b7b9fdf862c8228e9c6d87ad128ff994fff4631c7f` |
| 0002 | EIS-0002-01, EIS-0002-02, EIS-0002-03, INS-0002-02, INS-0002-03, INS-0002-04, INS-0002-05 | Experiment Results.xlsx#STM Results!D4 | `sha256:bf0a2a11837f1f1be15484d43f07bfcbb6ee4f8b118a307293ce478492258e4a` |
| 0004 | EIS-0004-01, INS-0004-01, INS-0004-02 | Experiment Results.xlsx#STM Results!D6 | `sha256:f37e1f77c817e6605bc63fdbac1843f2dd380e8dcbf3498b0a7e97e95268809a` |
| 0005 | EIS-0005-01, EIS-0005-02, EIS-0005-03 | Experiment Results.xlsx#STM Results!D7 | `sha256:0674dfef94e20772b2993f1f49cf5cf358a09b3638a897500870934831c9ad5e` |
| 0006 | EIS-0006-02 | Experiment Results.xlsx#STM Results!D8 | `sha256:3fe0120f5bb64412b58968d711114f1091078274c52647c3b9e1ccb310dccf81` |
| 0007 | EIS-0007-01, EIS-0007-02, EIS-0007-03 | Experiment Results.xlsx#STM Results!D9 | `sha256:81cd5e94e6bdb04894e2daf05957a9dba21566c9d1693a09f3e0e3b2c415d993` |
| 0009 | EIS-0009-01, EIS-0009-02, EIS-0009-03, INS-0009-03, VU-0009-01 | Experiment Results.xlsx#STM Results!D11 | `sha256:8ebde6e24fa1e6246ea05b7ae0b00a36fb933f8b2692be8139ac632ead9a06e2` |
| 0010 | DIFF-0010-08, EIS-0010-01, EIS-0010-02, EIS-0010-03, EIS-0010-04, EIS-0010-05, VU-0010-01 | Experiment Results.xlsx#STM Results!D12 | `sha256:9ecc1af98bd062bbf8c05f424a66065e4e15a5939b299f00a52e6b0c1415eaa0` |
| 0011 | INS-0011-02, VU-0011-01 | Experiment Results.xlsx#STM Results!D13 | `sha256:376b1eff602bfa346a3003b7b9fdf862c8228e9c6d87ad128ff994fff4631c7f` |
| 0012 | EIS-0012-01, INS-0012-01 | Experiment Results.xlsx#STM Results!D14 | `sha256:5361341d3ac80dcdbc270cca4c63cc1fbbcd7f17c4dc738dbf2dbed75077824d` |
| 0013 | EIS-0013-01 | Experiment Results.xlsx#STM Results!D15 | `sha256:bf0a2a11837f1f1be15484d43f07bfcbb6ee4f8b118a307293ce478492258e4a` |
| 0014 | EIS-0014-01, EIS-0014-02, EIS-0014-03, EIS-0014-04, VU-0014-01 | Experiment Results.xlsx#STM Results!D16 | `sha256:f37e1f77c817e6605bc63fdbac1843f2dd380e8dcbf3498b0a7e97e95268809a` |
| 0015 | EIS-0015-01 | Experiment Results.xlsx#STM Results!D17 | `sha256:0674dfef94e20772b2993f1f49cf5cf358a09b3638a897500870934831c9ad5e` |
| 0016 | DIFF-0016-05, EIS-0016-01, EIS-0016-02, EIS-0016-03 | Experiment Results.xlsx#STM Results!D18 | `sha256:3fe0120f5bb64412b58968d711114f1091078274c52647c3b9e1ccb310dccf81` |
| 0017 | INS-0017-01, VU-0017-01 | Experiment Results.xlsx#STM Results!D19 | `sha256:81cd5e94e6bdb04894e2daf05957a9dba21566c9d1693a09f3e0e3b2c415d993` |
| 0019 | DIFF-0019-05, EIS-0019-01, EIS-0019-02, EIS-0019-03, INS-0019-01 | Experiment Results.xlsx#STM Results!D21 | `sha256:ea5ac91a70b25b3eae0e6d164c0392208d97c765c4b2619de99f25ce41bd7bac` |
| 0020 | EIS-0020-02 | Experiment Results.xlsx#STM Results!D22 | `sha256:9ecc1af98bd062bbf8c05f424a66065e4e15a5939b299f00a52e6b0c1415eaa0` |
| 0023 | INS-0023-01, INS-0023-02, INS-0023-03 | Experiment Results.xlsx#STM Results!D25 | `sha256:bf0a2a11837f1f1be15484d43f07bfcbb6ee4f8b118a307293ce478492258e4a` |
| 0024 | DIFF-0024-04, EIS-0024-01, EIS-0024-02, EIS-0024-03, EIS-0024-04, INS-0024-01 | Experiment Results.xlsx#STM Results!D26 | `sha256:f37e1f77c817e6605bc63fdbac1843f2dd380e8dcbf3498b0a7e97e95268809a` |
| 0025 | EIS-0025-01, EIS-0025-02 | Experiment Results.xlsx#STM Results!D27 | `sha256:0674dfef94e20772b2993f1f49cf5cf358a09b3638a897500870934831c9ad5e` |
| 0026 | EIS-0026-01, EIS-0026-02, EIS-0026-03 | Experiment Results.xlsx#STM Results!D28 | `sha256:3fe0120f5bb64412b58968d711114f1091078274c52647c3b9e1ccb310dccf81` |
| 0027 | EIS-0027-01, INS-0027-04 | Experiment Results.xlsx#STM Results!D29 | `sha256:81cd5e94e6bdb04894e2daf05957a9dba21566c9d1693a09f3e0e3b2c415d993` |
| 0029 | DIFF-0029-06, EIS-0029-01, EIS-0029-02, EIS-0029-03, EIS-0029-04, EIS-0029-05, INS-0029-01, INS-0029-05 | Experiment Results.xlsx#STM Results!D31 | `sha256:ea5ac91a70b25b3eae0e6d164c0392208d97c765c4b2619de99f25ce41bd7bac` |
| 0030 | EIS-0030-01, EIS-0030-02, EIS-0030-03, INS-0030-01 | Experiment Results.xlsx#STM Results!D32 | `sha256:9ecc1af98bd062bbf8c05f424a66065e4e15a5939b299f00a52e6b0c1415eaa0` |
| 0032 | DIFF-0032-03, EIS-0032-01 | Experiment Results.xlsx#STM Results!D34 | `sha256:5361341d3ac80dcdbc270cca4c63cc1fbbcd7f17c4dc738dbf2dbed75077824d` |
| 0033 | EIS-0033-01, EIS-0033-02, INS-0033-01 | Experiment Results.xlsx#STM Results!D35 | `sha256:bf0a2a11837f1f1be15484d43f07bfcbb6ee4f8b118a307293ce478492258e4a` |
| 0034 | EIS-0034-01, EIS-0034-02, EIS-0034-03, EIS-0034-04, EIS-0034-05, EIS-0034-06, INS-0034-01 | Experiment Results.xlsx#STM Results!D36 | `sha256:f37e1f77c817e6605bc63fdbac1843f2dd380e8dcbf3498b0a7e97e95268809a` |
| 0035 | EIS-0035-01, EIS-0035-02, EIS-0035-03, EIS-0035-04 | Experiment Results.xlsx#STM Results!D37 | `sha256:0674dfef94e20772b2993f1f49cf5cf358a09b3638a897500870934831c9ad5e` |
| 0037 | EIS-0037-01 | Experiment Results.xlsx#STM Results!D39 | `sha256:81cd5e94e6bdb04894e2daf05957a9dba21566c9d1693a09f3e0e3b2c415d993` |
| 0039 | DIFF-0039-04, EIS-0039-01, EIS-0039-02, INS-0039-03, INS-0039-04 | Experiment Results.xlsx#STM Results!D41 | `sha256:ea5ac91a70b25b3eae0e6d164c0392208d97c765c4b2619de99f25ce41bd7bac` |
| 0040 | EIS-0040-01, EIS-0040-03, VU-0040-01 | Experiment Results.xlsx#STM Results!D42 | `sha256:9ecc1af98bd062bbf8c05f424a66065e4e15a5939b299f00a52e6b0c1415eaa0` |
| 0042 | EIS-0042-01 | Experiment Results.xlsx#STM Results!D44 | `sha256:5361341d3ac80dcdbc270cca4c63cc1fbbcd7f17c4dc738dbf2dbed75077824d` |
| 0043 | EIS-0043-01, EIS-0043-02 | Experiment Results.xlsx#STM Results!D45 | `sha256:bf0a2a11837f1f1be15484d43f07bfcbb6ee4f8b118a307293ce478492258e4a` |
| 0044 | EIS-0044-01, INS-0044-03 | Experiment Results.xlsx#STM Results!D46 | `sha256:f37e1f77c817e6605bc63fdbac1843f2dd380e8dcbf3498b0a7e97e95268809a` |
| 0045 | EIS-0045-01 | Experiment Results.xlsx#STM Results!D47 | `sha256:0674dfef94e20772b2993f1f49cf5cf358a09b3638a897500870934831c9ad5e` |
| 0046 | EIS-0046-01, EIS-0046-02, INS-0046-03, VU-0046-01 | Experiment Results.xlsx#STM Results!D48 | `sha256:3fe0120f5bb64412b58968d711114f1091078274c52647c3b9e1ccb310dccf81` |
| 0047 | EIS-0047-01, EIS-0047-02, EIS-0047-03 | Experiment Results.xlsx#STM Results!D49 | `sha256:81cd5e94e6bdb04894e2daf05957a9dba21566c9d1693a09f3e0e3b2c415d993` |
| 0049 | EIS-0049-01, EIS-0049-02, INS-0049-03, VU-0049-01 | Experiment Results.xlsx#STM Results!D51 | `sha256:ea5ac91a70b25b3eae0e6d164c0392208d97c765c4b2619de99f25ce41bd7bac` |
| 0050 | EIS-0050-01, INS-0050-01 | Experiment Results.xlsx#STM Results!D52 | `sha256:9ecc1af98bd062bbf8c05f424a66065e4e15a5939b299f00a52e6b0c1415eaa0` |
| 0053 | DIFF-0053-01, EIS-0053-01, INS-0053-02 | Experiment Results.xlsx#STM Results!D55 | `sha256:bf0a2a11837f1f1be15484d43f07bfcbb6ee4f8b118a307293ce478492258e4a` |
| 0054 | INS-0054-01, INS-0054-02, VU-0054-01 | Experiment Results.xlsx#STM Results!D56 | `sha256:f37e1f77c817e6605bc63fdbac1843f2dd380e8dcbf3498b0a7e97e95268809a` |
| 0055 | EIS-0055-01 | Experiment Results.xlsx#STM Results!D57 | `sha256:0674dfef94e20772b2993f1f49cf5cf358a09b3638a897500870934831c9ad5e` |
| 0056 | EIS-0056-01, EIS-0056-02, INS-0056-01 | Experiment Results.xlsx#STM Results!D58 | `sha256:3fe0120f5bb64412b58968d711114f1091078274c52647c3b9e1ccb310dccf81` |
| 0057 | EIS-0057-01, INS-0057-01 | Experiment Results.xlsx#STM Results!D59 | `sha256:81cd5e94e6bdb04894e2daf05957a9dba21566c9d1693a09f3e0e3b2c415d993` |
| 0059 | EIS-0059-01, INS-0059-03, VU-0059-02, VU-0059-03 | Experiment Results.xlsx#STM Results!D61 | `sha256:ea5ac91a70b25b3eae0e6d164c0392208d97c765c4b2619de99f25ce41bd7bac` |

## Files

- Full audit canonical hash: `sha256:f990a9394a5c1153246b170a7fec87e46b51c7b4b19261decc1570164b33389b`
- Candidate index canonical hash: `sha256:0aeeecc459da6864c65433c355dbe22e897a04d06522987321f492bd65464fd5`
- Candidate index audit-file hash: `sha256:64ba520eaf3a50663acb3ef7a8d05b640dfc5ff6d119ac085e004b1e23b5ad89`
