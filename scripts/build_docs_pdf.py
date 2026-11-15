#!/usr/bin/env python3
"""
scripts/build_docs_pdf.py
Convert the Markdown documents in docs/ to PDF.

Each file is converted with pandoc to a standalone HTML page (styled by
scripts/docs_pdf/style.css, with GitHub alert boxes rendered by
scripts/docs_pdf/alerts.lua and math as MathML), then printed to PDF with
headless Google Chrome. Chrome renders the Korean text, emoji and wide tables in
these documents more reliably than a LaTeX engine.

Usage:
    python scripts/build_docs_pdf.py                 # all docs/*.md -> docs/pdf/*.pdf
    python scripts/build_docs_pdf.py docs/README.md  # selected files only

Requires pandoc and google-chrome (or chromium) on PATH.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
OUT_DIR = DOCS_DIR / "pdf"
ASSETS = Path(__file__).resolve().parent / "docs_pdf"

INPUT_FORMAT = "gfm+tex_math_dollars"


def find_chrome() -> str:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    sys.exit("Error: google-chrome or chromium was not found on PATH.")


def first_heading(md: Path) -> str:
    for line in md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md.stem


def display(path: Path) -> str:
    """Path relative to the repository root when possible, otherwise absolute."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def md_to_html(md: Path, html: Path) -> None:
    subprocess.run(
        [
            "pandoc", str(md),
            "-f", INPUT_FORMAT,
            "-t", "html5",
            "--standalone",
            "--mathml",
            "--embed-resources",
            "--css", str(ASSETS / "style.css"),
            "--lua-filter", str(ASSETS / "alerts.lua"),
            "--metadata", f"pagetitle={first_heading(md)}",
            "--resource-path", str(md.parent),
            "-o", str(html),
        ],
        check=True,
    )


def html_to_pdf(chrome: str, html: Path, pdf: Path, profile: Path) -> None:
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-first-run",
            f"--user-data-dir={profile}",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=5000",
            f"--print-to-pdf={pdf}",
            html.as_uri(),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main(argv: list) -> int:
    if not shutil.which("pandoc"):
        sys.exit("Error: pandoc was not found on PATH.")
    chrome = find_chrome()
    files = [Path(a).resolve() for a in argv] if argv else sorted(DOCS_DIR.glob("*.md"))
    if not files:
        print("No Markdown files found.")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for md in files:
            pdf = OUT_DIR / f"{md.stem}.pdf"
            try:
                html = tmp / f"{md.stem}.html"
                md_to_html(md, html)
                html_to_pdf(chrome, html, pdf, tmp / "chrome-profile")
                if not pdf.is_file() or pdf.stat().st_size == 0:
                    raise RuntimeError("Chrome produced no PDF")
                print(f"OK    {display(md)} -> {display(pdf)}")
            except Exception as exc:
                failed.append(md.name)
                print(f"FAIL  {md.name}: {exc}", file=sys.stderr)

    print(f"\n{len(files) - len(failed)} of {len(files)} file(s) converted.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
