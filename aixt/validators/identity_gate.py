from __future__ import annotations

from typing import Any, Dict

from .types import ValidatorResult

try:
    from validators import identity_gate as legacy
except Exception as exc:  # pragma: no cover - legacy not available
    legacy = None
    _IMPORT_ERROR = exc


def validate(ocr_text: str, model_text: str) -> ValidatorResult:
    if legacy is None:
        return ValidatorResult(
            name="identity_gate",
            passed=False,
            evidence={"error": str(_IMPORT_ERROR)},
            details={"reason": "legacy validator unavailable"},
        )

    verdict = legacy.validate_identity_attribution(ocr_text, model_text)
    evidence: Dict[str, Any] = {
        "rule_hits": [hit.__dict__ for hit in verdict.rule_hits],
        "notes": verdict.notes,
    }
    return ValidatorResult(
        name="identity_gate",
        passed=verdict.passed,
        evidence=evidence,
        details={"hit_count": len(verdict.rule_hits)},
    )
