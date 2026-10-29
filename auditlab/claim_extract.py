"""Local-only literal claim tag index (candidate metadata, not verification)."""
import re
from pathlib import Path

TAG = re.compile(r"\[(CLAIM-[A-Z0-9.-]+)\]")


def extract_claim_candidates(text):
    if not isinstance(text, str):
        raise TypeError("input must be text")
    found = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        for tag in dict.fromkeys(TAG.findall(line)):
            found.setdefault(tag, []).append(line_no)
    return {"candidate_only": True, "claims": found}


def extract_file(path):
    return extract_claim_candidates(Path(path).read_text(encoding="utf-8"))
