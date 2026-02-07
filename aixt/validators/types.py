from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ValidatorResult:
    name: str
    passed: bool
    evidence: Any
    details: Dict[str, Any] = field(default_factory=dict)
