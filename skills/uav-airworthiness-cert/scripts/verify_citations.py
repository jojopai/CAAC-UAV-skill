#!/usr/bin/env python3
"""Check that every clause citation in a document exists in the source corpus.

Citations use the form "<CODE> <clause>", e.g.
    P2 §3.9.1        P2 第3.3条        L2 第92.305(a)(5)条        P2 附录H
CODE is resolved through the citation-map block inside the regulation map.

Usage:
    python3 verify_citations.py --doc <file.md> --corpus <corpus dir> [--map <map.md>] [--quiet]

Exit code 0 only when every citation resolved to a corpus document and was
found in it. Output is evidence, not a verdict: a hit proves the clause number
exists in that document, not that it governs the situation being described.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MAP_BLOCK = re.compile(r"<!--\s*citation-map(.*?)-->", re.S)
MAP_LINE = re.compile(r"^\s*([A-Z]{1,3}[0-9]{0,2})\s*:\s*(.+?)\s*$", re.M)

# A line carrying this marker is skipped, and the number of skipped lines is
# reported. Waivers are meant to be rare and visible, never silent.
WAIVER = re.compile(r"citation-check:\s*ignore", re.I)

CLAUSE_PATTERNS = [
    # P2 §3.9.1  /  P2 §92.305
    re.compile(r"\b([A-Z]{1,3}[0-9]{0,2})\s*§\s*([0-9][0-9.]*)"),
    # L2 第92.305(a)(5)条  /  P3 第3.1.2条
    re.compile(r"\b([A-Z]{1,3}[0-9]{0,2})\s*第\s*([0-9][0-9.]*(?:\([0-9a-zA-Z]+\))*)\s*条"),
    # P2 附录H
    re.compile(r"\b([A-Z]{1,3}[0-9]{0,2})\s*附录\s*([A-Z])\b"),
]


def strip_ws(s: str) -> str:
    return re.sub(r"\s+", "", s)


def load_map(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    block = MAP_BLOCK.search(text)
    if not block:
        raise SystemExit(f"no <!-- citation-map ... --> block found in {path}")
    return {code.strip(): name.strip() for code, name in MAP_LINE.findall(block.group(1))}


def load_corpus(corpus: Path) -> list[dict]:
    index = corpus / "index.json"
    if not index.exists():
        raise SystemExit(f"{index} not found; run build_corpus.py first")
    entries = json.loads(index.read_text(encoding="utf-8"))
    for entry in entries:
        text_path = Path(entry["text"])
        entry["_text"] = strip_ws(text_path.read_text(encoding="utf-8", errors="ignore"))
    return entries


def resolve(code: str, mapping: dict[str, str], entries: list[dict]) -> dict | None:
    name = mapping.get(code)
    if not name:
        return None
    key = strip_ws(name)
    candidates = [e for e in entries if key in strip_ws(e["name"])]
    if not candidates:
        return None
    # longest-name match wins, so L2 does not grab L2-something-else
    candidates.sort(key=lambda e: len(e["name"]))
    return candidates[0]


def find_token(token: str, text: str) -> str | None:
    """Return the match rule, or None when the token is absent."""
    if len(token) == 1 and token.isalpha():
        return f"附录{token}" if f"附录{token}" in text else None
    if f"第{token}条" in text:
        return "第N条"
    # heading style: token at the start of a line in the original source
    if re.search(r"(?m)^\s{0,8}" + re.escape(token) + r"(?![0-9])", text):
        return "行首小标题"
    if re.search(r"(?<![0-9.])" + re.escape(token) + r"(?![0-9])", text):
        return "正文出现"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--map", default=str(Path(__file__).resolve().parent.parent / "references" / "regulation-map.md"))
    ap.add_argument("--quiet", action="store_true", help="only print problems and the summary")
    args = ap.parse_args()

    mapping = load_map(Path(args.map))
    entries = load_corpus(Path(args.corpus).expanduser().resolve())
    doc_path = Path(args.doc).expanduser().resolve()
    raw_lines = doc_path.read_text(encoding="utf-8").splitlines()
    waived = [l for l in raw_lines if WAIVER.search(l)]
    doc = "\n".join(l for l in raw_lines if not WAIVER.search(l))

    seen: list[tuple[str, str]] = []
    for pattern in CLAUSE_PATTERNS:
        for code, target in pattern.findall(doc):
            # Keep unknown codes too: a code missing from the map is a finding,
            # not something to skip silently.
            item = (code, target)
            if item not in seen:
                seen.append(item)

    problems = 0
    print(f"document : {doc_path}")
    print(f"citations: {len(seen)} unique\n")
    if waived:
        print(f"  waived   {len(waived)} line(s) carrying 'citation-check: ignore'")
        for line in waived:
            print(f"           - {line.strip()[:100]}")
        print()
    for code, target in seen:
        token = target.split("(")[0].rstrip(".")
        entry = resolve(code, mapping, entries)
        if entry is None:
            print(f"  NO-CORPUS  {code} {target}   (code not in map, or document not in corpus)")
            problems += 1
            continue
        rule = find_token(token, entry["_text"])
        if rule is None:
            print(f"  MISS       {code} {target}   not found in {entry['name']}")
            problems += 1
        elif not args.quiet:
            print(f"  ok         {code} {target}   {rule}  <- {entry['name']}")
        if entry.get("status") != "ok" and rule is not None:
            print(f"             ^ {entry['name']} is flagged '{entry['status']}'; read the page itself before quoting")

    unresolved_codes = sorted({c for c, _ in seen if c not in mapping})
    if unresolved_codes:
        print(f"\ncodes absent from the citation map: {', '.join(unresolved_codes)}")

    print(f"\nsummary: {len(seen)} citations, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
