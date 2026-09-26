#!/usr/bin/env python3
"""Check that the same value appears wherever it is expected to appear.

Expectations file, one rule per line:
    <key>|<file1>,<file2>[,...]
    # blank lines and lines starting with # are ignored

Usage:
    python3 check_consistency.py --dir <folder> --expect <rules file>

Exit code 0 only when every rule holds. Prints the full matrix first, so a
human can see where a key is present and where it is missing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def normalise(text: str) -> str:
    return re.sub(r"\s+", "", text)


def load_rules(path: Path) -> list[tuple[str, list[str]]]:
    rules: list[tuple[str, list[str]]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            raise SystemExit(f"{path}:{lineno}: expected '<key>|<file>,<file>'")
        key, files = line.split("|", 1)
        rules.append((key.strip(), [f.strip() for f in files.split(",") if f.strip()]))
    return rules


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--expect", required=True)
    args = ap.parse_args()

    folder = Path(args.dir).expanduser().resolve()
    docs = {p.name: normalise(p.read_text(encoding="utf-8", errors="ignore"))
            for p in sorted(folder.glob("*.md"))}
    if not docs:
        raise SystemExit(f"no .md files in {folder}")
    rules = load_rules(Path(args.expect).expanduser().resolve())

    keys = [k for k, _ in rules]
    width = max(len(k) for k in keys) + 2
    print("key".ljust(width) + " ".join(p[:6].ljust(6) for p in docs))
    for key in keys:
        cells = [("1" if key in docs[name] else ".").ljust(6) for name in docs]
        print(key.ljust(width) + " ".join(cells))

    failures = 0
    print()
    for key, files in rules:
        missing = [f for f in files if key not in docs.get(f, "")]
        unknown = [f for f in files if f not in docs]
        if unknown:
            print(f"FAIL  {key}: file(s) not found: {', '.join(unknown)}")
            failures += 1
        elif missing:
            print(f"FAIL  {key}: missing from {', '.join(missing)}")
            failures += 1
        else:
            print(f"ok    {key}: present in all {len(files)} expected file(s)")

    print(f"\nsummary: {len(rules)} rule(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
