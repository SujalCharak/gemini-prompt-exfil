from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ToolResult:
    output: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


class ToolAdapter:
    """Tool adapters return data only. Authorization lives elsewhere."""

    name: str = "base"

    def invoke(
        self,
        *,
        payload: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        raise NotImplementedError("ToolAdapter.invoke must be implemented")
