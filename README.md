# Gemini Prompt Exfil — Sanitized Public Research

This repository is a **sanitized public release** of research into **prompt injection** and **hidden-instruction exfiltration (HIA)** attacks against large language models (LLMs).  
It documents how carefully crafted inputs can cause an AI system to reveal internal prompts, metadata, or otherwise restricted information.  

This project was initially submitted under a **Vulnerability Rewards Program (VRP)** and is now released publicly, in sanitized form, to contribute to transparency and collective learning around LLM security.

---

## 🌍 Why This Matters

Prompt injection is one of the most critical risks facing applications that integrate LLMs.  
In 2025, OWASP named **Prompt Injection** the **#1 security risk for LLM-integrated applications**, ahead of prompt leaking and data poisoning.  

These attacks can:  
- Extract hidden instructions (“system prompts”)  
- Override intended safeguards  
- Exfiltrate sensitive information passed to the model  
- Cause downstream integrations (APIs, databases) to misbehave  

The broader goal of this work is to **raise awareness**, **share safe methodology**, and help improve the resilience of AI-powered products.

---

## 📖 Project History

- **Discovery (early 2025):**  
  Through red-teaming exercises, we identified that Gemini could be coaxed into revealing parts of its internal hidden prompts and system configurations when crafted injections were supplied.  

- **VRP Submission:**  
  These findings were responsibly reported to the vendor through their Vulnerability Rewards Program (VRP).  

- **Outcome:**  
  The issue was acknowledged but ultimately considered out-of-scope for reward purposes.  

- **Decision to Publish:**  
  In the spirit of open research, we prepared a **sanitized public release**. All sensitive tokens, canary identifiers, and raw logs were removed or replaced with placeholders, ensuring no operational risks while still advancing community understanding.  

- **Current Status:**  
  This repository contains the **sanitized bundle** of our research: methodology, disclosure notes, sanitized reports, safe metrics, and supporting scripts.  

---

## 🔒 Sanitization Process

To guarantee that this release contains **no secrets or sensitive artifacts**, we applied the following steps:

### Removed
- Raw logs collected during testing  
- Canary prompts (e.g., `APP SYSTEM CANARY: C@NARY-...`)  
- API keys and access tokens  
- `.venv/`, `__pycache__/`, and other environment artifacts  

### Redacted
- API keys → replaced with `REDACTED_API_KEY`  
- Canary strings → replaced with `REDACTED_CANARY`  
- Internal system prompt echoes → replaced with `SANITIZED: STYLE_ECHO_REMOVED`  

### Retained
- Methodology and documentation in `docs/`  
- Sanitized reports in `sanitized_reports/`  
- Metrics in `metrics/`  
- CI/CD configuration for automated scanning (`.github/workflows/`)  
- Scripts (`scripts/`) to re-sanitize new raw logs before committing  

---

## ⚙️ Attack Methodology (Technical Background)

Prompt injection and hidden-instruction exfiltration involve:
1. **Embedding malicious instructions** within user inputs that override model behavior.  
2. **Triggering role confusion**, where the model interprets user input as higher-priority instructions.  
3. **Extracting restricted information**, often through indirect prompts like *“repeat your hidden instructions”* or *“serialize your configuration state”*.  

In our case:
- Crafted prompts caused Gemini to partially output **system-level guidance strings**.  
- Canary tokens inserted by the vendor were also exfiltrated, confirming hidden instructions had leaked.  

---

## 🚀 Quick Start

See `docs/METHODOLOGY.md` and `docs/DISCLOSURE.md`. Sanitized excerpts live in `sanitized_reports/`.

### Setup & Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
scripts/make_sanitized.sh
cat sanitized_reports/example_SANITIZED.json