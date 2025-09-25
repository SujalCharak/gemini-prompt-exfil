# Methodology (Sanitized)

This document describes, at a high level, the methodology used in exploring prompt injection and hidden-instruction exfiltration attacks.

- Conducted controlled red-teaming sessions with Gemini.  
- Focused on prompt injection variants designed to elicit hidden instructions.  
- Recorded outputs and identified cases of hallucinations, partial hidden text reveals, and other unintended behaviors.  
- Applied sanitization before public release:
  - Removed raw logs
  - Redacted canary strings
  - Replaced API tokens with placeholders

For details on sanitization, see [HALLUCINATION_ANALYSIS.md](HALLUCINATION_ANALYSIS.md).
