from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aixt.core.env import ensure_run_id, init_determinism
from aixt.core.trace import Trace, write_trace
from aixt.validators.registry import run_validators


def _load_scenario(path: Path) -> Dict[str, Any]:
    text = path.read_text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except Exception as exc:
            raise RuntimeError(
                "Scenario is not JSON and PyYAML is not installed"
            ) from exc
        return yaml.safe_load(text)


def _write_negative(trace: Trace, base_dir: Path) -> Path:
    run_id = os.getenv("AIXT_RUN_ID") or ensure_run_id()
    root = base_dir / run_id
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{trace.trial_id}.json"
    path.write_text(json.dumps(asdict(trace), indent=2, sort_keys=True))
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a single AIXT scenario.")
    parser.add_argument("--scenario", required=True, help="Path to scenario YAML/JSON")
    parser.add_argument("--seed", type=int, default=None, help="Override AIXT_SEED")
    parser.add_argument("--run-id", default=None, help="Override AIXT_RUN_ID")
    parser.add_argument("--negative-dir", default="aixt/artifacts/negative_results")
    args = parser.parse_args()

    if args.run_id:
        os.environ["AIXT_RUN_ID"] = args.run_id

    init_determinism(args.seed)
    run_id = ensure_run_id()

    scenario_path = Path(args.scenario)
    scenario = _load_scenario(scenario_path)

    scenario_id = scenario.get("id", scenario_path.stem)
    prompts = scenario.get("prompts", {})
    inputs = scenario.get("inputs", {})
    mock = scenario.get("mock", {})

    ocr_text = inputs.get("ocr_text", "")
    retrieved_context = inputs.get("retrieved_context", "")
    model_output = mock.get("model_output", "")
    tool_calls = mock.get("tool_calls", [])

    validator_names = scenario.get("validators")
    secrets = scenario.get("secrets", [])
    metric_units = scenario.get("metric_units")

    results = run_validators(
        validator_names,
        ocr_text=ocr_text,
        model_output=model_output,
        metric_units=metric_units,
        secrets=secrets,
    )

    passed = all(result.passed for result in results.values()) if results else False
    verdict = "no_exfil" if passed else "failed"

    trace = Trace(
        trial_id=f"{scenario_id}-{run_id}",
        system_prompt=prompts.get("system", ""),
        user_input=prompts.get("user", ""),
        retrieved_context=retrieved_context,
        tool_calls=tool_calls,
        model_output=model_output,
        validator_results={k: v.__dict__ for k, v in results.items()},
        verdict=verdict,
        metadata={
            "scenario_id": scenario_id,
            "description": scenario.get("description", ""),
            "seed": int(os.getenv("AIXT_SEED", "0")),
        },
    )

    trace_path = write_trace(trace)

    if not passed:
        _write_negative(trace, Path(args.negative_dir))

    print(f"Trace written: {trace_path}")
    if not passed:
        print(f"Negative result recorded under: {args.negative_dir}/{run_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
