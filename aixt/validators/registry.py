from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from . import claims_grounding, identity_gate, leakage_exact_match, leakage_fuzzy, tone_control
from .types import ValidatorResult

DEFAULT_VALIDATORS = [
    "claims_grounding",
    "identity_gate",
    "leakage_exact_match",
    "leakage_fuzzy",
    "tone_control",
]


def run_validators(
    names: Optional[Iterable[str]] = None,
    *,
    ocr_text: str = "",
    model_output: str = "",
    metric_units: Optional[List[str]] = None,
    secrets: Optional[Iterable[str]] = None,
    evidence_ok: Optional[bool] = None,
) -> Dict[str, ValidatorResult]:
    selected = list(names or DEFAULT_VALIDATORS)
    results: Dict[str, ValidatorResult] = {}

    for name in selected:
        if name == "claims_grounding":
            res = claims_grounding.validate(ocr_text, model_output, metric_units)
            results[name] = res
            if evidence_ok is None:
                evidence_ok = res.passed
        elif name == "identity_gate":
            results[name] = identity_gate.validate(ocr_text, model_output)
        elif name == "leakage_exact_match":
            results[name] = leakage_exact_match.validate(model_output, secrets or [])
        elif name == "leakage_fuzzy":
            results[name] = leakage_fuzzy.validate(model_output, secrets or [])
        elif name == "tone_control":
            results[name] = tone_control.validate(model_output, bool(evidence_ok))
        else:
            results[name] = ValidatorResult(
                name=name,
                passed=False,
                evidence={"error": "unknown validator"},
                details={"reason": "validator not registered"},
            )

    return results
