#!/usr/bin/env python3
"""Extract every mandatory requirement statement from the regulation corpus.

This is how "strictly follow all the regulations" becomes checkable instead of
aspirational: the inventory is generated from the source text, so nothing is
missed because nobody remembered to look, and nothing is invented.

Usage:
    python3 extract_requirements.py --corpus <corpus dir> --code P4 [--code P2 ...]
    python3 extract_requirements.py --corpus <dir> --code P4 --out requirements-P4.md
    python3 extract_requirements.py --corpus <dir> --all --out requirements-all.md

Output is a Markdown table with an empty disposition column. Every row must end
up as 适用 / 不适用 + reason / 由专用条件确定. An empty disposition cell in a
submitted checklist is itself a finding.

Modal verbs counted as mandatory: 应当、必须、不得、严禁、不应、需（仅"需经/需报"等强制搭配）.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_citations import load_map, resolve  # noqa: E402  (shared citation logic)

# clause headings we can attribute a requirement to
CLAUSE_PATTERNS = [
    re.compile(r"^\s*第\s*([0-9]+\.[0-9]+(?:\.[0-9]+)*)\s*条"),
    re.compile(r"^\s*第\s*([0-9]{4})\s*[．.]"),          # QSAC criteria 1801．...
    re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,3})\s+\S"),   # 3.9.1 工程验证试验
    re.compile(r"^\s*([0-9]+)\s+[^\s\d]"),               # 1 总则
    re.compile(r"^\s*附录\s*([A-Z])"),
    re.compile(r"^\s*第\s*([sS][0-9])\s*节"),
]

# Some PDFs wrap a heading as "1." on one line and "2 设计特征及运行场景" on the
# next, which flattens "1.2 设计特征及运行场景". Track that prefix.
DANGLING_HEADING = re.compile(r"^\s*([0-9]+)\.\s*$")
SUB_HEADING = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)*)\s+[^\s\d]")

MANDATORY = re.compile(r"应当|必须|不得|严禁|不应|需经|需报|应经|应予")
SENTENCE_END = re.compile(r"[。；;]$")


def strip_ws(s: str) -> str:
    return re.sub(r"\s+", "", s)


def load_corpus(corpus: Path) -> list[dict]:
    index = corpus / "index.json"
    if not index.exists():
        raise SystemExit(f"{index} not found; run build_corpus.py first")
    return json.loads(index.read_text(encoding="utf-8"))


def current_clause(line: str, previous: str, dangling: str) -> tuple[str, str]:
    """Return (clause, dangling_prefix)."""
    m = DANGLING_HEADING.match(line)
    if m:
        return previous, m.group(1)
    if dangling:
        m = SUB_HEADING.match(line)
        if m:
            return f"{dangling}.{m.group(1)}", ""
    indent = len(line) - len(line.lstrip())
    for index, pattern in enumerate(CLAUSE_PATTERNS):
        m = pattern.match(line)
        if m:
            # Bare numeric headings (patterns 2 and 3) also appear as indented
            # continuation text mid-sentence; only trust them near the margin.
            if index in (2, 3) and indent > 8:
                continue
            token = m.group(1)
            if "附录" in pattern.pattern:
                return f"附录{token}", ""
            if "节" in pattern.pattern:
                return f"第{token}节", ""
            return token, ""
    return previous, dangling


def collect(text: str, max_len: int) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    clause = ""
    dangling = ""
    buffer = ""
    previous_line = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        clause_here, dangling = current_clause(raw, clause, dangling)
        if clause_here != clause:
            buffer = ""
            clause = clause_here
        if MANDATORY.search(line):
            # Reattach the lead-in the requirement usually started on: PDF text
            # often splits "当无人驾驶航空器系统运行时，所安装的..." across lines.
            lead = ""
            if previous_line and len(previous_line) < 80 and not MANDATORY.search(previous_line):
                if not any(p.match(previous_line) for p in CLAUSE_PATTERNS):
                    lead = previous_line
            buffer = lead + line
            continue
        if buffer:
            buffer += line
            if SENTENCE_END.search(line) or len(buffer) > max_len:
                rows.append((clause or "未定位", buffer[:max_len]))
                buffer = ""
        previous_line = line
    if buffer:
        rows.append((clause or "未定位", buffer[:max_len]))

    # de-duplicate on clause + leading characters
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for clause_, text_ in rows:
        key = (clause_, text_[:40])
        if key not in seen:
            seen.add(key)
            out.append((clause_, text_))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--code", action="append", default=[], help="document code prefix, e.g. P4")
    ap.add_argument("--all", action="store_true", help="every document in the corpus")
    ap.add_argument("--out", help="write the table here instead of stdout")
    ap.add_argument("--max-len", type=int, default=160)
    ap.add_argument(
        "--map",
        default=str(Path(__file__).resolve().parent.parent / "references" / "regulation-map.md"),
        help="regulation map holding the citation-map block",
    )
    args = ap.parse_args()

    entries = load_corpus(Path(args.corpus).expanduser().resolve())
    mapping = load_map(Path(args.map))
    if args.all:
        selected = entries
    else:
        if not args.code:
            raise SystemExit("pass --code P4 (repeatable) or --all")
        selected = []
        for code in args.code:
            entry = resolve(code, mapping, entries)
            if entry is None:
                print(f"! code '{code}' resolves to no corpus document (check --map)", file=sys.stderr)
                continue
            selected.append(entry)
    if not selected:
        raise SystemExit(
            "no documents selected; check --code against the citation-map in --map"
        )

    lines = ["| 序号 | 依据文件 | 条款 | 要求原文（截断） | 处置 | 处置理由 | 责任人 |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    total = 0
    seq = 0
    for entry in selected:
        if entry.get("status") != "ok":
            print(
                f"! {entry['name']} is flagged '{entry['status']}'; its requirements "
                "cannot be extracted reliably and must be read by eye",
                file=sys.stderr,
            )
        text = Path(entry["text"]).read_text(encoding="utf-8", errors="ignore")
        rows = collect(text, args.max_len)
        total += len(rows)
        for clause, body in rows:
            seq += 1
            body = body.replace("|", "／")
            lines.append(f"| {seq} | {entry['name']} | {clause} | {body} | | | |")
        print(f"  {len(rows):>5d} requirements  {entry['name']}", file=sys.stderr)

    output = "\n".join(lines) + "\n"
    if args.out:
        Path(args.out).expanduser().write_text(output, encoding="utf-8")
        print(f"\n{total} requirements -> {args.out}", file=sys.stderr)
    else:
        print(output)
    print(
        "\nEvery row needs a disposition: 适用 / 不适用+理由 / 由专用条件确定.\n"
        "A requirement with an empty disposition is an open finding, not a blank.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
