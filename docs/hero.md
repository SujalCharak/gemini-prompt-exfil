> **aixt = Guardrails for LLMs**  
> We show a real prompt-leak in raw Gemini and a working mitigation that blocks it — with reproducible, sanitized runs.  
> **Same input → Different outcomes:**  
> - ❌ Raw model: leaks hidden preamble (“You are Gemini …”).  
> - ✅ aixt wrapper: refuses and returns evidence-grounded JSON.
