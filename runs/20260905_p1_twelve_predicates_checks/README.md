# P1 predicate migration checks

Date: 2026-09-05. Scope: the current twelve-predicate method and version-aware
interpretation of stored receipts. These are functional and provenance checks,
not an experiment, quality evaluation, or predicate-subset ablation.

## Test evidence

| Report | Result | Scope |
| --- | --- | --- |
| `p1-final-current-tests.xml` | 417 passed, 14 failed | method, evidence-discovery pipeline, evaluation, and reproducibility suites |
| `p1-focused-final.xml` | 110 passed | registry, applicability, stage loss, backend conformance, historical mapping, release boundary, and predicate-gold contracts; includes the subsequently added unrelated-schema-version regression |
| `p1-baseline-tests.xml`, `p1-baseline-extra.xml` | All 14 current failure names reproduced | Targeted comparison against the pre-P1 source at `77820dace894ba4a976bd5d5d671cf9354200330` |

The fourteen failures are not waived as passes. Twelve concern existing W2,
terminal-state, frontier, native text-handling allowlist, or public-language
fixtures. Two concern historical v60 publication files whose LFS objects are
not expanded in this checkout. The baseline was extracted to a temporary tree
with unchanged representation, utility, and frozen-result dependencies; its
other failures include an archived replay fixture and an absent ledger link.
It is a failure comparison, not a claim that the whole baseline suite is green.

The full command used the following four pytest targets under the paper root:

```text
method/tests
pipeline/evidence_discovery/tests
evaluation/tests
tests/reproducibility
```

Python: `/home/zhangshaoang/oo-projects/research_ideas/venv/bin/python`.
`PYTHONPATH` explicitly selected this checkout's `method/src`, `evaluation/src`,
`judge/src`, paper root, `pyfcstm`, and repository root. No provider or Judge
was invoked. The separate live functional smoke has its own run record.

## Frozen receipt views

`v61_main_labels.json` reads `raw/v61_current/method/`;
`v61_fill0045_labels.json` reads `raw/v61_current_fill0045/`, both under
`paper_stm_issue_discover/final_results/v61_source_divergence_vs_x1v2_baseline/`.
The existing paper selection replaces failed pair 0045 round 1 with the stored
fill run. The failed original cell has no predicate receipts.

The two views retain 2436 saved receipts, including nonterminal and unbound
records. Terminal Boolean receipts remain 1114: 541 false/violation and 573
true/pass. Old S6 has seven nonterminal receipts (six in the main run and one in
the fill run) and no terminal Boolean receipt.
Retired predicates remain identifiable; old and current G3/R3/V1 are never
merged by ID text alone. Each view preserves the source registry, run identity,
manifest hash, and cell hashes. No verdict, report, W/D label, hit, precision,
or source artifact is rewritten.

Reproduce each view with `scripts/evaluation/predicate_id_view.py --run-root
<source-run> --output <new-path>` from the paper workspace. The output must be
outside the source run and `final_results`, and must not already exist.

## Standalone release check

The allowlisted release was built outside the repository from clean commit
`5fc274b8c7a0beb3a379e0515f73562791bb012a`: 74 payload files, 1668563 bytes,
zero provider calls. `p1-release-final-manifest.json` records every copied hash.
All `src/` payload hashes equal the release built from smoke commit
`71774498d65f3e3a7df5a30fbd7128236756fc1f`; only one test changed afterward.

| Report | Result | Interpretation |
| --- | --- | --- |
| `p1-release-before-fixture-fix.xml` | 12 passed, 1 failed, 19 skipped | A source-only audit-file assumption in the shipped fixture failed outside the repository |
| `p1-source-fixture-tests.xml` | 13 passed | The corrected fixture retains the source checkout's mandatory audit-file assertions |
| `p1-release-final-tests.xml` | 13 passed, 19 skipped | The same fixture verifies the published package's explicit fail-closed audit fallback |

The release branch of the fixture requires a verified embedded manifest, not
merely a missing audit file. The runtime and release allowlist were unchanged.
The nineteen skips belong to the existing v61 test module that requires frozen
pair artifacts and v60 results; those inputs are intentionally not released.
The original failed report and release manifest are retained, not overwritten.

The final release tests ran from `/tmp`, using only the release's `src/` and
this checkout's `pyfcstm` on `PYTHONPATH`, with the Python interpreter above.
No package was installed into or altered in the sibling checkout. This checks
source-tree release imports and tests, not a fresh dependency installation.
Generated pytest XML retains its original traceback whitespace.
