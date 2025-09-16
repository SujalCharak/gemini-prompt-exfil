# runner.py
from tqdm import tqdm
from typing import List, Dict
from target import respond
from report import to_md, save_md, save_jsonl
from checks.core import check_system_prompt_leak, check_policy_override
from checks.secrets import check_secrets_pii
from utils.paraphrase import paraphrases
import pathlib, yaml, importlib

CFG = yaml.safe_load(open(pathlib.Path(__file__).with_name("aix.yaml")))
SCEN = CFG.get("scenario", "context_infection")
scen_mod = importlib.import_module(f"scenarios.{SCEN}")
build_scenario = getattr(scen_mod, "build_scenario")
MALICIOUS_TURN_INDEX = getattr(scen_mod, "MALICIOUS_TURN_INDEX", None)

def run_context_with_fuzz(paraphrase_tries: int = 8) -> List[Dict]:
    base = build_scenario()
    history: List[Dict] = []
    results: List[Dict] = []

    for i, turn in enumerate(tqdm(base, desc="Conversation", leave=False)):
        history.append(turn)
        if turn["role"] != "user":
            continue

        # Decide variants: only fuzz at malicious turn
        if MALICIOUS_TURN_INDEX is not None and i == MALICIOUS_TURN_INDEX:
            variants = [turn["content"]] + paraphrases(paraphrase_tries)
        else:
            variants = [turn["content"]]

        for attempt, payload in enumerate(variants):
            if attempt > 0:  # swap in paraphrase
                history[-1] = {"role":"user","content":payload}

            output = respond(history)
            history.append({"role":"assistant","content":output})

            checks = [
                check_system_prompt_leak(output),
                check_policy_override(output),
                check_secrets_pii(output),
            ]
            fail = any(not c["pass"] for c in checks)
            results.append({
                "id": f"{SCEN}",
                "step": i,
                "last_user": payload,
                "output": output,
                "checks": checks,
                "attempt": attempt,
                "fuzzed": attempt > 0,
            })
            if fail and (MALICIOUS_TURN_INDEX is not None and i == MALICIOUS_TURN_INDEX):
                # stop on first success at the malicious turn
                break
    return results

def main():
    tries = CFG.get("paraphrase_tries", 8)
    results = run_context_with_fuzz(paraphrase_tries=tries)
    save_jsonl(results, "run.jsonl")
    md = to_md(results)
    save_md(md, "report.md")
    total = len(results)
    fails = sum(1 for r in results if any(not c["pass"] for c in r["checks"]))
    attempts = [r.get("attempt") for r in results if any(not c["pass"] for c in r["checks"])]
    min_attempt = min(attempts) if attempts else None
    print(f"[Summary] steps={total} | fails={fails} | first_bypass_attempt={min_attempt}")

if __name__ == "__main__":
    main()