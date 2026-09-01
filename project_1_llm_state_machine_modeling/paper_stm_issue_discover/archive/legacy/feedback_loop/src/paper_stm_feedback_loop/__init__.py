"""Feedback-loop runtime package for Paper STM issue discover.

Paper 1 was narrowed to issue discover alone (repair is a separate follow-up
paper), so this package's shipped surface is the discover loop. The package name
``paper_stm_feedback_loop`` and the sibling ``paper_stm_repair_*`` distribution
names are retained deliberately -- renaming them would break every pinned import
path and every committed run record for no research benefit.

The package root intentionally stays lightweight: importing it must not import
legacy ``paper_stm_repair_loop`` modules or perform runtime I/O.
"""

__all__ = ["common"]
