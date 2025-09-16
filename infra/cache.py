import hashlib, json, pathlib
CACHE_DIR = pathlib.Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

def _key(model: str, prompt: str) -> str:
    h = hashlib.sha256()
    h.update(model.encode()); h.update(prompt.encode())
    return h.hexdigest()

def get(model: str, prompt: str):
    fp = CACHE_DIR / _key(model, prompt)
    if fp.exists():
        try:
            return json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def put(model: str, prompt: str, payload):
    fp = CACHE_DIR / _key(model, prompt)
    fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
