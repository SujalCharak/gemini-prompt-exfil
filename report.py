# report.py
import json
from typing import List, Dict

def save_jsonl(results: List[Dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def to_md(results: List[Dict]) -> str:
    lines = ["# Adversarial Test Report\n"]
    fails = [r for r in results if any(not c["pass"] for c in r["checks"])]
    attempts = [r.get("attempt") for r in results if any(not c["pass"] for c in r["checks"])]
    first_bypass = (min(a for a in attempts if a is not None) if attempts else None)
    lines.append(f"- Steps: {len(results)}")
    lines.append(f"- Fails: {len(fails)}")
    lines.append(f"- First bypass attempt: {first_bypass}\n")
    for r in results:
        lines.append(f"## Step {r['step']} (attempt={r.get('attempt',0)}, fuzzed={r.get('fuzzed', False)})")
        lines.append(f"**Last user:** {r['last_user'][:500]}")
        out = r['output'] or ""
        lines.append(f"**Output (truncated):** {out[:800]}")
        lines.append("**Checks:**")
        for c in r["checks"]:
            badge = "PASS ✅" if c["pass"] else "FAIL ❌"
            lines.append(f"- {badge} `{c['check']}` — {c['reason']}")
        lines.append("")
    return "\n".join(lines)

def save_md(md: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)