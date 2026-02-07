#!/usr/bin/env python3
"""
AIXT HIA runner.

Coordinates evaluation runs only.
Security decisions must live in validators.
"""

from __future__ import annotations

import os
import sys
import json
import time
import pathlib
from datetime import datetime
from typing import Any, Dict, List

import google.generativeai as genai

# Optional dotenv support (never overrides real env vars)
try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except Exception:
    pass

from aixt.core.guardrails import build_guarded_prompt
from aixt.core.policy_engine import score_and_act
from aixt.core.response_templates import safe_abstain, soft_warn, ok_pass


# ---------- small helpers ----------
def _mk_outdir(p: str | pathlib.Path) -> pathlib.Path:
    out = pathlib.Path(p)
    out.mkdir(parents=True, exist_ok=True)
    return out


def _safe_dump_json(path: pathlib.Path, obj: Any) -> None:
    try:
        path.write_text(
            json.dumps(obj, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        print(f"[WARN] failed to write {path}: {e}", file=sys.stderr)


def _read_jsonl(path: pathlib.Path) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    if not path.exists():
        print(f"[WARN] infile not found: {path}", file=sys.stderr)
        return cases

    for ln, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        s = (line or "").strip()
        if not s:
            continue
        try:
            cases.append(json.loads(s))
        except Exception as e:
            print(f"[WARN] bad JSONL (line {ln}): {e}", file=sys.stderr)

    return cases


# ---------- core runner ----------
def run_case(
    model,
    model_name: str,
    case: Dict[str, Any],
    outdir: pathlib.Path,
    policy_path: str,
    trials: int,
    temperature: float,
    per_call_sleep_s: float,
) -> None:
    cid = case.get("id", "case")
    prompt = case.get("prompt", "")
    ocr = case.get("ocr_text", "")
    domain = case.get("domain", "generic")
    extra = {k: v for k, v in case.items() if k not in {"id", "prompt", "ocr_text"}}

    user_input = build_guarded_prompt(ocr, prompt)

    for t in range(1, trials + 1):
        trial_ts = datetime.now().isoformat(timespec="seconds")
        trial_id = f"{cid}_trial{t}"

        # ---- 1) model call ----
        try:
            resp = model.generate_content(
                user_input,
                generation_config={"temperature": float(temperature)},
            )
            raw_text = resp.text if hasattr(resp, "text") else str(resp)
            engine_err = ""
        except Exception as e:
            raw_text = ""
            engine_err = f"[ENGINE] {e}"

        # ---- 2) policy evaluation ----
        try:
            policy = score_and_act(
                ocr_text=ocr,
                model_output=raw_text or "",
                policy_path=policy_path,
                user_prompt=prompt,
                history_prompts=None,
                domain=domain,
            )
        except Exception as e:
            policy = {
                "risk": "low",
                "action": "ALLOW",
                "hits": [],
                "pressure": 0.0,
                "narrative": f"[POLICY ERROR] {e}",
            }

        action = str(policy.get("action", "ALLOW")).upper()
        base_risk = str(policy.get("risk", "low"))
        narrative = str(policy.get("narrative", ""))
        hits = policy.get("hits", [])
        pressure = float(policy.get("pressure", 0.0))

        # ---- 3) output guard ----
        if action == "ABSTAIN":
            final_text = safe_abstain(ocr, prompt, hits, pressure)
        elif action == "WARN":
            final_text = soft_warn(ocr, prompt, hits, pressure, raw_text)
        else:
            final_text = ok_pass(raw_text or "")

        if engine_err:
            final_text += f"\n\n---\n(Engine note: {engine_err})\n"

        # ---- 4) artifacts ----
        verdict = (
            f"**Verdict:** base_risk={base_risk} • action={action} • "
            f"model={model_name} • when={trial_ts}"
        )

        md = (
            f"# {cid} trial {t}\n\n"
            f"{verdict}\n\n"
            f"{narrative}\n\n"
            f"---\n\n"
            f"{final_text}\n"
        )
        (outdir / f"{trial_id}.md").write_text(md, encoding="utf-8")

        raw_payload = {
            "id": cid,
            "trial": t,
            "ts": trial_ts,
            "model": model_name,
            "temperature": temperature,
            "text": raw_text or None,
            "error": engine_err or None,
            "extra": extra or None,
            "domain": domain,
        }
        _safe_dump_json(outdir / f"{trial_id}_raw.json", raw_payload)

        if per_call_sleep_s > 0:
            time.sleep(per_call_sleep_s)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        description="Run AIXT trials with guardrails and policy scoring"
    )
    ap.add_argument("--infile", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--policy", default="policies/default.yaml")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=0.6)
    ap.add_argument("--sleep", type=float, default=0.2)
    ap.add_argument("--model", default=os.environ.get("MODEL", "gemini-2.5-pro"))
    args = ap.parse_args()

    provider_key = os.getenv("PROVIDER_API_KEY_ENV")
    if not provider_key:
        raise RuntimeError(
            "Missing provider API key (PROVIDER_API_KEY_ENV). "
            "Expected in research runs; absent in CI/offline mode."
        )

    genai.configure(api_key=provider_key)
    model = genai.GenerativeModel(args.model)

    outdir = _mk_outdir(args.outdir)
    cases = _read_jsonl(pathlib.Path(args.infile))

    if not cases:
        print(f"[WARN] No cases in {args.infile}", file=sys.stderr)
        return

    for case in cases:
        run_case(
            model=model,
            model_name=args.model,
            case=case,
            outdir=outdir,
            policy_path=args.policy,
            trials=args.trials,
            temperature=args.temperature,
            per_call_sleep_s=args.sleep,
        )


if __name__ == "__main__":
    main()
