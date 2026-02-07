from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RetrievedDocument:
    content: str
    source: str
    score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class RetrieverAdapter:
    """Retrievers return data only. Authorization lives elsewhere."""

    name: str = "base"

    def retrieve(
        self,
        *,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedDocument]:
        raise NotImplementedError("RetrieverAdapter.retrieve must be implemented")
