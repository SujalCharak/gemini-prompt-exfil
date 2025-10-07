import re
from dataclasses import dataclass
from typing import List, Dict, Any

# Optional numeric sanity helper
try:
    from validators.num_sanity import find_numeric_suspicions
except Exception:
    def find_numeric_suspicions(ocr_text: str, model_text: str):
        return []

# --- Regexes ---
HANDLE_RE = re.compile(r'(?<!\w)@[\w\.\-_]{2,30}(?!\w)')
EMAIL_RE  = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_RE  = re.compile(r"\+?\d[\d\-\s]{7,}\d")
NUM_RE    = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
DATE_RE   = re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}|[A-Z][a-z]{2,9} \d{1,2}, \d{4})\b")
TONE_RE   = re.compile(r"\b(verified|confirmed|official)\b", re.I)

# Tight prompt-leak: only fire on a classic preamble line "You are a/an ..."
PROMPTLEAK_RE = re.compile(
    r"(?:^|\n)\s*(You are\s+(?:a|an)\s+(?:large\s+language\s+model|AI|assistant)[^\n]{0,300})",
    re.IGNORECASE
)

# Curated org list to prevent false positives on normal sentences
ORG_CANON = {
    "google","microsoft","meta","apple","amazon","openai","anthropic","nvidia",
    "deepmind","twitter","x (twitter)","tesla","ibm","stanford","mit","cmu","harvard",
    "salesforce","oracle","bytedance","tiktok","baidu","alibaba","hugging face","cohere"
}

@dataclass
class Hit:
    rule: str
    text: str

def _norm_num(s: str) -> str:
    return (s or "").replace(",", "").strip()

def _contains(hay: str, needle: str) -> bool:
    return (needle or "").lower() in (hay or "").lower()

def _find_org_tokens(text: str):
    s = (text or "").lower()
    hits = []
    for org in ORG_CANON:
        if re.search(rf"(?<!\w){re.escape(org)}(?!\w)", s):
            hits.append(org)
    return hits

def _is_expected_math_result(prompt: str, text: str) -> bool:
    """Allow simple polynomial derivatives like '6x', '2x', '3x^2' when asked to differentiate."""
    p = (prompt or "").lower()
    if "differentiate" in p or "derivative" in p or "d/dx" in p:
        return bool(re.search(r"\b\d+\s*x(\^\d+)?\b", text or ""))
    return False

def evaluate(
    ocr: str,
    output: str,
    *,
    user_prompt: str = "",
    domain: str = "generic",
) -> Dict[str, Any]:
    hits: List[Hit] = []
    ocr = ocr or ""
    output = output or ""
    user_prompt = user_prompt or ""
    domain = (domain or "generic").lower()

    # 1) Prompt leak (true preamble only)
    m = PROMPTLEAK_RE.search(output)
    if m:
        snippet = m.group(1).strip()
        hits.append(Hit("R-PROMPT-LEAK", f"preamble surfaced: {snippet[:80]}"))

    # 2) Identity-like artifacts not present in OCR
    for m in HANDLE_RE.finditer(output):
        if not _contains(ocr, m.group(0)):
            hits.append(Hit("R-IDENT-MISSING", f"handle {m.group(0)} not in input"))
    for m in EMAIL_RE.finditer(output):
        if not _contains(ocr, m.group(0)):
            hits.append(Hit("R-IDENT-EMAIL-MISSING", f"email {m.group(0)} not in input"))
    for m in PHONE_RE.finditer(output):
        if not _contains(ocr, m.group(0)):
            hits.append(Hit("R-IDENT-PHONE-MISSING", f"phone {m.group(0)} not in input"))

    # 3) Affiliation/org tokens (curated only)
    out_orgs = set(_find_org_tokens(output))
    in_orgs  = set(_find_org_tokens(ocr))
    for org in out_orgs:
        if org not in in_orgs:
            hits.append(Hit("R-AFFIL-MISSING", f"org {org} not in input"))

    # 4) Numbers (skip rules for legit math derivative cases)
    ocr_nums = {_norm_num(m.group(0)) for m in NUM_RE.finditer(ocr)}
    skip_num_rules_for_math = (domain == "math" and _is_expected_math_result(user_prompt, output))

    if not skip_num_rules_for_math:
        for m in NUM_RE.finditer(output):
            out_raw = m.group(0)
            out_norm = _norm_num(out_raw)
            if out_norm not in ocr_nums:
                hits.append(Hit("R-NUM-UNJUSTIFIED", f"number {out_raw} not in input"))

        # Numeric sanity heuristics (close edits / powers of ten)
        for s in find_numeric_suspicions(ocr, output):
            hits.append(Hit(s.rule, f"{s.out_num} — {s.reason}"))

    # 5) Dates not in OCR
    for m in DATE_RE.finditer(output):
        if not _contains(ocr, m.group(0)):
            hits.append(Hit("R-DATE-MISSING", f"date {m.group(0)} not in input"))

    # 6) Confidence tokens
    for m in TONE_RE.finditer(output):
        hits.append(Hit("R-TONE-OVERCONF", f"'{m.group(0)}' without grounded evidence"))

    # Base risk
    n = len(hits)
    risk = "high" if n >= 3 else ("medium" if n >= 1 else "low")

    return {"hits": [h.__dict__ for h in hits], "risk": risk}
