from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from aixt.harness.runners.run_scenario import main as run_scenario_main


if __name__ == "__main__":
    # Delegate to the scenario runner with the baseline scenario.
    scenario_path = Path("aixt/harness/scenarios/baseline.yaml")
    sys.argv = [sys.argv[0], "--scenario", str(scenario_path)]
    raise SystemExit(run_scenario_main())
