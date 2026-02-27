def approx_tokens(txt: str) -> int:
    return max(0, len((txt or "").split()))