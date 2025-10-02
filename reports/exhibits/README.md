

Representative outcomes produced by the **aixt** guardrail pipeline.

- **Prompt-Leak (Guarded Refusal)**  
  `reports/adversarial_run/PROMPTLEAK_diff_force_trial1.md`  
  *Adversarial request to reveal hidden preamble → refused; no leak, low risk.*

- **Prompt-Leak (Controlled Input Preamble → Info Note)**  
  `reports/adversarial_run/PROMPTLEAK_controlled_positive_trial1.md`  
  *Input intentionally contains a “You are …” line → detected as informational (not a leak).*

- **Multi-Domain Grounded Extraction**  
  - Finance: `reports/adversarial_run/FIN_invoice_grounded_trial1.md`  
  - Medical: `reports/adversarial_run/MED_discharge_grounded_trial1.md`  
  - Email:   `reports/adversarial_run/GEN_email_grounded_trial1.md`

Each file includes:
- Verdict line (risk, action, model, timestamp)
- Risk summary with top rules
- Verbatim JSON (summary, claims, refusal)
