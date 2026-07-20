from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StrictContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, strict=True)


class EvalAssertInput(StrictContractModel):
    assert_: str = Field(alias="assert", min_length=1)
    reason: str = Field(min_length=1)
