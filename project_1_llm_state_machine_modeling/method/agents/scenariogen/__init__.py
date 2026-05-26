"""Test scenario generation pipeline (BDD-style model test cases, not LTL/CTL).

Each scenario is a (initial_vars, events, expected_final_state, expected_vars)
quadruple consumed by ``method/feedback/sim.py`` as a simulation oracle.

Currently a single-step pipeline (NL + model elements -> JSON scenarios) for
sprint speed. The MTI 3-step variant (elements_mapping -> Gherkin ->
三元组 mini-DSL) is a future-work item for paper-level ablation.
"""

from method.agents.scenariogen.generate import generate_scenarios

__all__ = ["generate_scenarios"]
