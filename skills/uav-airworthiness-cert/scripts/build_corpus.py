#!/usr/bin/env python3
"""Extract the regulation PDFs into searchable plain text plus an index.

Usage:
    python3 build_corpus.py --src <dir> [--src <dir> ...] --out <dir>

Writes:
    <out>/text/<name>.txt   plain text per document
    <out>/index.json        [{name, source, text, chars, status}]

status is "ok" or "needs OCR" (the PDF yielded almost no text and must be
rendered and read by eye before any clause in it is quoted).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

OCR_THRESHOLD = 500  # characters; below this the PDF is treated as scanned


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def safe(name: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff.\-()（）]+", "_", name).strip("_")


def pdf_to_text(pdf: Path, out_txt: Path) -> int:
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    res = run(["pdftotext", "-layout", str(pdf), str(out_txt)])
    if res.returncode != 0:
        print(f"  ! pdftotext failed for {pdf.name}: {res.stderr.strip()}", file=sys.stderr)
        out_txt.write_text("", encoding="utf-8")
    return len(out_txt.read_text(encoding="utf-8", errors="ignore")) if out_txt.exists() else 0


def collect_pdfs(src: Path, workdir: Path) -> list[tuple[Path, str]]:
    """Return [(pdf_path, label)] for a source entry (dir, .pdf or .rar)."""
    found: list[tuple[Path, str]] = []
    if src.is_dir():
        for path in sorted(src.rglob("*")):
            if path.suffix.lower() == ".pdf":
                found.append((path, path.stem))
            elif path.suffix.lower() == ".rar":
                found.extend(extract_rar(path, workdir))
    elif src.suffix.lower() == ".pdf":
        found.append((src, src.stem))
    elif src.suffix.lower() == ".rar":
        found.extend(extract_rar(src, workdir))
    else:
        print(f"  - skipped (not a PDF or RAR): {src}", file=sys.stderr)
    return found


def extract_rar(archive: Path, workdir: Path) -> list[tuple[Path, str]]:
    target = workdir / safe(archive.stem)
    target.mkdir(parents=True, exist_ok=True)
    ok = False
    detail = "no archiver available"
    if shutil.which("bsdtar"):
        res = run(["bsdtar", "-xf", str(archive), "-C", str(target)])
        ok = res.returncode == 0
        detail = res.stderr.strip() or f"bsdtar exit {res.returncode}"
    if not ok:
        print(
            f"  - {archive.name}: could not extract ({detail}); "
            "extract it manually and pass the extracted PDF path as --src",
            file=sys.stderr,
        )
        return []
    out = []
    for pdf in sorted(target.rglob("*.pdf")):
        out.append((pdf, f"{archive.stem}-{pdf.stem}"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", action="append", required=True, help="directory, PDF or RAR; repeatable")
    ap.add_argument("--out", required=True, help="corpus output directory")
    args = ap.parse_args()

    outdir = Path(args.out).expanduser().resolve()
    (outdir / "text").mkdir(parents=True, exist_ok=True)
    index: list[dict] = []

    with tempfile.TemporaryDirectory(prefix="uav-cert-corpus-") as tmp:
        workdir = Path(tmp)
        for raw in args.src:
            src = Path(raw).expanduser().resolve()
            if not src.exists():
                print(f"  ! not found: {src}", file=sys.stderr)
                continue
            for pdf, label in collect_pdfs(src, workdir):
                txt = outdir / "text" / f"{safe(label)}.txt"
                chars = pdf_to_text(pdf, txt)
                status = "ok" if chars >= OCR_THRESHOLD else "needs OCR"
                index.append(
                    {
                        "name": label,
                        "source": str(pdf),
                        "text": str(txt),
                        "chars": chars,
                        "status": status,
                    }
                )
                print(f"  {status:9s} {chars:>8d} chars  {label}")

    (outdir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    ocr = [e["name"] for e in index if e["status"] != "ok"]
    print(f"\n{len(index)} documents -> {outdir}")
    if ocr:
        print("needs OCR (render and read before quoting): " + ", ".join(ocr))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
