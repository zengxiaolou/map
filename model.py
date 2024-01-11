from typing import Optional, List

from pydantic import BaseModel


class QueryParams(BaseModel):
    regions: Optional[List[str]] = None
    keyword1: Optional[str] = None
    type1: Optional[str] = None
    keyword2: Optional[str] = None
    type2: Optional[str] = None
    radius: Optional[str] = None

