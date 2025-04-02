"""
    Description response class
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203,C0412

from pydantic import BaseModel, Field
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

class DescriptionResponse(BaseModel):
    """Description response"""
    page_description : str = Field(description="Page description.")

@dataclass_json
@dataclass
class DescriptionResponseData:
    """Description response data"""
    response        : DescriptionResponse
    used_tokens     : Optional[int] = 0
    used_cost       : Optional[float] = 0.0
    errors          : Optional[list[str]] = Field(default=[])


@dataclass_json
@dataclass
class DescriptionResponseListData:
    """Description response data list"""
    response        : list[DescriptionResponse]
    used_tokens     : Optional[int] = 0
    used_cost       : Optional[float] = 0.0
    errors          : Optional[list[str]] = Field(default=[])
