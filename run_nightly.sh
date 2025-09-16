#!/usr/bin/env bash
set -euo pipefail
export MAX_RPM=25 MAX_ATTEMPTS=2 STEP_SLEEP=0.5 GEMINI_MODEL=${GEMINI_MODEL:-gemini-1.5-pro}
python toolkit/scripts/run_seeds.py toolkit/scripts/seeds_prompt_leakage.txt prompt_leak
python toolkit/scripts/run_seeds.py toolkit/scripts/seeds_connector_abuse.txt connector_abuse
python toolkit/scripts/run_seeds.py toolkit/scripts/seeds_persistence.txt persistence
python toolkit/scripts/run_seeds.py toolkit/scripts/seeds_tool_exploit.txt tool_exploit
[ -f toolkit/scripts/seeds_rag_exfil.txt ] && python toolkit/scripts/run_seeds.py toolkit/scripts/seeds_rag_exfil.txt rag_exfil || true
sqlite3 logs/run.sqlite3 -column -header \
"SELECT attack_class, impact_label, COUNT(*) AS n FROM logs GROUP BY attack_class, impact_label ORDER BY attack_class, impact_label;"

export GEMINI_MODEL=${GEMINI_MODEL:-gemini-1.5-pro}
export CANARY_TOKEN="C@NARY-$(date +%s)-$RANDOM"
python toolkit/scripts/run_seeds_with_canary.py toolkit/scripts/seeds_canary_indirect.txt prompt_leak
python toolkit/scripts/run_seeds_with_canary.py toolkit/scripts/seeds_math_reveal.txt   prompt_leak

