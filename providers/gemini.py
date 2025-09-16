# providers/gemini.py
import os
import google.generativeai as genai

def _ensure_model(cfg=None):
    """Return (GenerativeModel, model_name) using cfg if present, else env defaults."""
    # defaults from env
    key_env = "GEMINI_API_KEY"
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

    # override from cfg if provided
    if cfg:
        key_env = cfg.get("gemini", {}).get("api_key_env", key_env)
        model_name = cfg.get("provider", {}).get("model", model_name)

    api_key = os.getenv(key_env)
    if not api_key:
        raise RuntimeError(f"Missing env var {key_env}")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name), model_name

def respond(history, cfg=None):
    """
    Main entry point. Make cfg optional so ad-hoc tests can call respond(prompt)
    while the runner can still pass a config object.
    """
    model, _ = _ensure_model(cfg)

    # Build contents in the format Gemini expects
    if isinstance(history, str):
        contents = [{"parts": [{"text": history}]}]
    else:
        # history is a list of dicts with .get("text")
        parts = []
        for m in history:
            t = m.get("text") if isinstance(m, dict) else str(m)
            if t:
                parts.append({"text": t})
        contents = [{"parts": parts or [{"text": ""}]}]

    resp = model.generate_content(contents)
    return getattr(resp, "text", "") or ""
