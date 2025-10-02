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

-Raw Gemini **leaked** its system prompt. The **aixt wrapper** refused and returned verifiable JSON.

**Raw model (subscription)**: adversarial prompt revealed a preamble line  
**aixt-guarded**: same prompt → **refusal**, no leak, risk = low

## 🔒 Before vs After: Prompt Injection Contained

<table>
  <tr>
    <td><img src="docs/screenshots/gemini_raw_leak.png" width="430" alt="Raw Gemini leaked hidden preamble"></td>
    <td><img src="docs/screenshots/guardrail_refusal.png" width="430" alt="aixt guardrail refused; returned grounded JSON"></td>
  </tr>
  <tr>
    <td align="center"><b>Raw Gemini</b>: leaked its hidden system prompt</td>
    <td align="center"><b>aixt Guardrail</b>: blocked leak, returned grounded JSON</td>
  </tr>
</table>

## Why this matters

LLMs often fail *between* “works on my prompt” and “safe in production.”  
This repo demonstrates a reproducible **guardrail layer** that:
- Blocks prompt-leaks and overconfident fabrications with an evidence-first policy.
- Forces **verifiable, structured JSON** (claims + verbatim evidence + refusal).
- Works **without** retraining or fine-tuning — it’s a drop-in wrapper.
- Aligns with common AI risk categories (e.g., prompt manipulation & information disclosure).

## How it works (in 4 steps)

1. **OCR / Input** → Text is extracted (or provided directly) as `[INPUT]`.
2. **Guarded prompt** → The model is asked for **JSON only**, grounded in verbatim spans from `[INPUT]`, with a dedicated `refusal` field.
3. **Validators** → Domain-agnostic checks (identity/affiliation, numbers, dates, tone) compute a risk score → `ALLOW / WARN / ABSTAIN`.
4. **Verdict** → Human-readable markdown + machine-readable JSON artifacts are written to `reports/`.

> See the full technical appendix: [`report.md`](report.md)  
> Explore concrete exhibits: [`reports/exhibits`](reports/exhibits)

##  Results at a Glance

| Case                | Raw Gemini            | aixt Guardrail Verdict |
|---------------------|----------------------|------------------------|
| Prompt injection    | ❌ Leaked system preamble | ✅ Refusal + grounded JSON |
| Finance invoice     | –                    | ✅ ALLOW (low risk)     |
| Medical discharge   | –                    | ⚠️ WARN (medium)        |
| Email extract       | –                    | ✅ ALLOW (low risk)     |

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

## 🔒 Before vs After: Prompt Injection Contained

> See also: [Full exhibit](reports/exhibits/PRIYU_PROMPTLEAK.md) for exact files and timestamps.

<div align="center">
  <table>
    <tr>
      <td align="center"><b>Gemini (raw)</b><br><sub>leaks hidden preamble</sub></td>
      <td align="center"><b>Guardrail (aixt)</b><br><sub>refuses + returns grounded JSON</sub></td>
    </tr>
    <tr>
      <td><img src="docs/screenshots/gemini_raw_leak.png" width="430"></td>
      <td><img src="docs/screenshots/guardrail_refusal.png" width="430"></td>
    </tr>
  </table>
</div>

**What’s happening:**  
- ❌ *Raw* Gemini reveals system instructions when given an adversarial, emotionally loaded prompt.  
- ✅ *Guarded* run enforces “evidence-first” JSON, detects that no system text exists in input, and records a **refusal** instead of leaking.

**Why it matters:** This is a reproducible containment layer. Same input, different outcome — the wrapper removes the leak path and logs why.
