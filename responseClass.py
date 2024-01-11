from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class Page:
    size: int
    index: int
    total: int

@dataclass
class Metadata:
    code: str
    message: str
    page: Optional[Page] = None

@dataclass
class ApiResponse:
    metadata: Metadata
    result: Optional[Any] = None
    Extra: Optional[Dict[str, Any]] = field(default_factory=dict)
    props: Dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, item):
        return self.props.get(item, None)

    def __setitem__(self, key, value):
        self.props[key] = value
