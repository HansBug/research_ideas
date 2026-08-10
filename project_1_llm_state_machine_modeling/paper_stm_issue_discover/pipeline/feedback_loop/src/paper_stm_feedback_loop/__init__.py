"""Feedback-loop runtime package for Paper STM repair.

The package root intentionally stays lightweight: importing it must not import
legacy ``paper_stm_repair_loop`` modules or perform runtime I/O.
"""

__all__ = ["common"]
