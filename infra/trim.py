def trim_text(s: str, char_budget: int) -> str:
    if s is None:
        return ""
    if char_budget <= 0:
        return ""
    return s[:char_budget]
