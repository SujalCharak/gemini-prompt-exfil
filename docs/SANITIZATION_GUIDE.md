# Sanitization Rules
- Do NOT publish raw *_raw.json, logs, request IDs, provider metadata, or tokens.
- Truncate any leak text to 8–12 words then replace with …REDACTED….
- Replace token-like strings with REDACTED_TOKEN.
