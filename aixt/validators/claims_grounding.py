from __future__ import annotations

from typing import Any, Dict, List, Optional

from .types import ValidatorResult

try:
    from validators import claims_grounding as legacy
except Exception as exc:  # pragma: no cover - legacy not available
    legacy = None
    _IMPORT_ERROR = exc


def validate(
    ocr_text: str,
    model_output: str,
    metric_units: Optional[List[str]] = None,
) -> ValidatorResult:
    if legacy is None:
        return ValidatorResult(
            name="claims_grounding",
            passed=False,
            evidence={"error": str(_IMPORT_ERROR)},
            details={"reason": "legacy validator unavailable"},
        )

    result: Dict[str, Any] = legacy.validate_claims(
        ocr_text=ocr_text,
        model_output=model_output,
        metric_units=metric_units,
    )
    hits = result.get("hits", [])
    return ValidatorResult(
        name="claims_grounding",
        passed=len(hits) == 0,
        evidence=hits,
        details={"hit_count": len(hits)},
    )
