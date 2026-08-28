# Paper STM Method

This package contains only the current typed evidence-discovery method. It
does not include the Semantic Judge, evaluation logic, ledgers, expected
answers, baselines, frozen results, runs, or legacy implementations.

## Installation

Build the release tree from a clean repository checkout:

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/build_method_release.py \
  --output /tmp/paper-stm-method-release
python -m pip install /tmp/paper-stm-method-release
```

The release metadata pins the required `pyfcstm` revision. A real run also
requires a valid `utils.llm` profile configuration supplied by the operator;
credentials are never included in the package.

When running an extracted release package without a Git checkout, set
`PAPER_STM_RELEASE_SOURCE_COMMIT` to the exact `source_commit` in the generated
`release_manifest.json`; retain that manifest beside the run records. This preserves the live-run provenance gate without
rewriting installed source files.

## Method CLI

```bash
paper-stm-method --help
paper-stm-method \
  --report-root /path/to/frozen-stm-input-closure \
  --output-dir /path/to/new-method-artifacts \
  --profile gpt-5.6-luna \
  --pair-id 0001 --rounds 1 --allow-live
```

The input closure must provide `pairs/`, `canonical/`, `parse_inspect/`,
`source_traces/`, `working_contracts/`, and `case_reports/`. The method writes
only its designated output directory and never reads a ledger or Judge result.

## Provider-Free Check

```bash
python -c "from paper_stm_method.inputs import parse_fcstm; print(parse_fcstm('state Root { state A; [*] -> A; }').algorithm_version)"
```

The packaged resources are `paper_stm_method.resources.predicate_registry.json`
and `current_source_catalog.json`. They are byte-identical mirrors of the
frozen method registry and scholarly catalog. The catalog is provenance
metadata, not an evaluation answer source.

## Experiment Provenance

This release structure is not the experiment implementation commit. The v60
method ran from `66b5d71aecd73f6eeddac082037f7c34e04da057`; the Semantic Judge
ran from `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`. The release manifest and
repository documentation retain these immutable references.
