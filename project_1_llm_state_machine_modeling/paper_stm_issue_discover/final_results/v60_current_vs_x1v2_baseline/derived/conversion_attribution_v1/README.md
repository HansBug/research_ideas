# Conversion attribution v1

Provider-free, evaluation-only attribution for v60 current invalid reports. `report_attribution_v1.json` is the fact source; TSV, summary and Markdown are generated projections. Inputs are frozen v4 decisions, raw reports, source NL/PlantUML, canonical/source inventory, FCSTM, source traces and pair READMEs. No method, Judge or provider execution occurred.

The overlay preserves the v60 headline and records `NO_RERUN`. It does not remove any invalid output from report-level precision: all 291 I records, including the 118 NADC dispositions, remain in the denominator. The strict `CONVERSION_LOWERING_CONFIRMED` count is 0; 110 NADC records have confirmed method-owned mechanisms and 8 are indeterminate.

`i_attribution_report_v1.md` contains the reviewer-facing I composition and descriptive precision-gap decomposition. The decomposition must not be read as a causal estimate of precision without the projection.
