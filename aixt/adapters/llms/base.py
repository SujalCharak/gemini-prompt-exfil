from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LLMResult:
    text: str
    raw: Any
    tokens: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class LLMAdapter:
    """LLM adapters return data only. Authorization lives elsewhere."""

    name: str = "base"

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        tools: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> LLMResult:
        raise NotImplementedError("LLMAdapter.generate must be implemented")
