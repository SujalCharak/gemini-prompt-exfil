# aixt — Adversarial Guardrails for LLMs (Gemini Case Study)

**What this repo shows**
- How a production LLM can be prompted to **leak system preamble** and **hallucinate identity attributions**.
- A lightweight **guardrail layer** (this repo) that **prevents those failures** with evidence-first extraction, verification, and risked actions (ALLOW/WARN/ABSTAIN).
- Reproducible, sanitized artifacts (reports + verdicts) and a clean test harness.

**Key links**
- 📁 **Exhibits (human-readable)**: `reports/exhibits/`
- 🧪 **Benchmarks (sanitized cases)**: `benchmarks/`
- 🔧 **Guardrails engine**: `engine/`, `validators/`, `policies/`
- 🔐 **Disclosure & process**: `DISCLOSURE.md`, `SECURITY.md`

---

## TL;DR result (before vs after)

**Raw model (subscription)**: adversarial prompt revealed a preamble line  
**aixt-guarded**: same prompt → **refusal**, no leak, risk = low

See `demo/raw_vs_guarded.png` and `reports/exhibits/*PROMPTLEAK*`.

---

## Run a safe demo (sanitized)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY=YOUR_TEST_KEY
export MODEL=gemini-2.5-pro

python run_hia.py \
  --infile benchmarks/multidomain_adversarial.jsonl \
  --outdir reports/adversarial_run \
  --policy policies/default.yaml \
  --trials 1 --temperature 0.4
