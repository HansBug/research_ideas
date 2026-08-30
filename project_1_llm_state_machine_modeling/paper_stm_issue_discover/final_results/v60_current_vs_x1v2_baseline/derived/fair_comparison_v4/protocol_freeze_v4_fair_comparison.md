# Fair comparison v4 protocol freeze

The comparison has exactly two headline sides: current re-audit v4 and the
frozen baseline v3. Both sides use source-first D/A adjudication, complete
expected relation closure, mechanical K/N/I, W as an independent evidence
axis, and same-side/same-pair N grouping. The only side-specific semantic
subtype is current method-owned `NOT_A_DEFECT_CLAIM`; baseline does not get
that subtype by symmetry.

The primary precision denominator is raw reports. Hit denominators are the
same 145 expected IDs and three rounds for both sides. FULL contributes hit;
PARTIAL contributes supported coverage only. K is an expected-ledger unit, N
is a substantive group unit, and I is an invalid report with optional
diagnostic clusters. I clusters are not defects and are not used as a
substantive grouped precision denominator.

This layer is provider-free. It does not call method, Judge, or any provider,
and does not modify raw, reference, method, Judge, predicate, v2, or v3
artifacts. It is a deterministic projection and recomputation over saved
canonical layers.
