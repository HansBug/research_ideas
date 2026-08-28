# Paper STM Semantic Judge

This package implements the frozen two-stage issue #195 Semantic Judge. It is
independent of the method package: it reads arm-neutral reports and a
read-only STM artifact closure through `utils.stm_artifacts`, and it never
imports discovery, predicate routing, a ledger, baseline data, or evaluation
reporting code.

The packaged `semantic_judge_issue_195.snapshot.md` is byte-identical to the
frozen protocol snapshot and is checked against its published SHA-256 before a
live Judge run. Provider use remains explicit through `--allow-live`.

Repository-based development adds the root `utils/` package to the import
path. The method release intentionally excludes this Judge package.
