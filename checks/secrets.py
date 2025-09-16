# checks/secrets.py
from typing import Dict, List
import re

PATTERNS = {
    "openai_key": r"\bsk-[A-Za-z0-9]{20,}\b",
    "aws_access_key": r"\bAKIA[0-9A-Z]{16}\b",
    "aws_secret_key": r"\b(?=.*[A-Za-z0-9/+]{40})(?!AKIA)[A-Za-z0-9/+=]{40}\b",
    "google_api_key": r"\bAIza[0-9A-Za-z\-_]{35}\b",
    "github_token": r"\bghp_[A-Za-z0-9]{36}\b",
    "slack_token": r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone_generic": r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}",
}

def check_secrets_pii(output: str) -> Dict:
    text = output or ""
    hits: List[str] = []
    for name, pat in PATTERNS.items():
        if re.search(pat, text):
            hits.append(name)
    if hits:
        return {"check":"secrets_pii","pass":False,"reason":"Possible secrets/PII detected","evidence":hits}
    return {"check":"secrets_pii","pass":True,"reason":"No secrets/PII patterns detected","evidence":None}