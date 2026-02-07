from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List


def _resolve_run_id(traces_dir: Path, run_id: str | None) -> str:
    if run_id:
        return run_id
    env_run = os.getenv("AIXT_RUN_ID")
    if env_run:
        return env_run

    if not traces_dir.exists():
        raise RuntimeError(f"No traces directory found at {traces_dir}")

    run_ids = sorted([p.name for p in traces_dir.iterdir() if p.is_dir()])
    if not run_ids:
        raise RuntimeError("No run IDs found under traces directory")
    return run_ids[-1]


def _load_traces(run_dir: Path) -> List[Dict[str, Any]]:
    traces = []
    for path in sorted(run_dir.glob("*.json")):
        try:
            traces.append(json.loads(path.read_text()))
        except json.JSONDecodeError:
            continue
    return traces


def _normalize_trace(trace: Dict[str, Any]) -> Dict[str, Any]:
    metadata = trace.get("metadata", {}) or {}
    return {
        "trial_id": trace.get("trial_id"),
        "verdict": trace.get("verdict"),
        "scenario_id": metadata.get("scenario_id"),
        "description": metadata.get("description"),
        "seed": metadata.get("seed"),
    }


def _is_negative(verdict: str | None) -> bool:
    return verdict not in ("no_exfil", "pass", "clean")


def _write_json(rows: Iterable[Dict[str, Any]], path: Path) -> None:
    path.write_text(json.dumps(list(rows), indent=2, sort_keys=True))


def _write_csv(rows: Iterable[Dict[str, Any]], path: Path) -> None:
    rows_list = list(rows)
    if not rows_list:
        path.write_text("")
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows_list[0].keys()))
        writer.writeheader()
        writer.writerows(rows_list)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AIXT scoring reports.")
    parser.add_argument("--include-negative", action="store_true", help="Include negative verdicts")
    parser.add_argument("--format", default="json", help="Comma-separated formats: json,csv")
    parser.add_argument("--run-id", default=None, help="Run ID to report")
    parser.add_argument("--traces-dir", default="aixt/artifacts/traces")
    parser.add_argument("--output-dir", default="aixt/artifacts/negative_results")
    args = parser.parse_args()

    traces_dir = Path(args.traces_dir)
    run_id = _resolve_run_id(traces_dir, args.run_id)
    run_dir = traces_dir / run_id
    traces = _load_traces(run_dir)

    rows = [_normalize_trace(t) for t in traces]
    if not args.include_negative:
        rows = [row for row in rows if not _is_negative(row.get("verdict"))]

    output_dir = Path(args.output_dir) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    formats = [f.strip().lower() for f in args.format.split(",") if f.strip()]
    for fmt in formats:
        if fmt == "json":
            _write_json(rows, output_dir / "report.json")
        elif fmt == "csv":
            _write_csv(rows, output_dir / "report.csv")
        else:
            raise RuntimeError(f"Unknown format: {fmt}")

    print(f"Report generated under: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
