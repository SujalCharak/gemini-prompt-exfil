from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .env import ensure_run_id


@dataclass
class Trace:
    trial_id: str
    system_prompt: str
    user_input: str
    retrieved_context: str
    tool_calls: List[Dict[str, Any]]
    model_output: str
    validator_results: Dict[str, Any]
    verdict: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def write_trace(trace: Trace, base_dir: Optional[Path | str] = None) -> Path:
    """Write a trace artifact to aixt/artifacts/traces/<run_id>.

    Returns the path to the created file.
    """
    run_id = ensure_run_id()
    root = Path(base_dir or "aixt/artifacts/traces") / run_id
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{trace.trial_id}.json"
    path.write_text(json.dumps(asdict(trace), indent=2, sort_keys=True))
    return path
