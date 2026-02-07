from __future__ import annotations

from typing import Any, Dict

from .types import ValidatorResult

try:
    from validators import tone_control as legacy
except Exception as exc:  # pragma: no cover - legacy not available
    legacy = None
    _IMPORT_ERROR = exc


def validate(model_text: str, evidence_ok: bool) -> ValidatorResult:
    if legacy is None:
        return ValidatorResult(
            name="tone_control",
            passed=False,
            evidence={"error": str(_IMPORT_ERROR)},
            details={"reason": "legacy validator unavailable"},
        )

    verdict = legacy.validate_tone(model_text, evidence_ok)
    evidence: Dict[str, Any] = {
        "notes": verdict.notes,
        "hits": verdict.hits,
    }
    return ValidatorResult(
        name="tone_control",
        passed=verdict.passed,
        evidence=evidence,
        details={"hit_count": len(verdict.hits)},
    )
