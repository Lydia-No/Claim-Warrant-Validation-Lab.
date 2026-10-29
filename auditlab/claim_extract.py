"""Public claim-tag indexing helpers."""
import re
TAG = re.compile(r"\[(CLAIM-[A-Z0-9.-]+)\]")
