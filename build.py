#!/usr/bin/env python3
"""Inline the brand PNGs into site.src.html and write index.html.

Placeholders in the source look like:  __ASSET:mark-color.png__
and are replaced with a base64 data: URI from assets/.
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "site.src.html"
OUT = ROOT / "index.html"
ASSETS = ROOT / "assets"

MIME = {".png": "image/png", ".svg": "image/svg+xml", ".jpg": "image/jpeg"}


def data_uri(name):
    path = ASSETS / name
    if not path.exists():
        sys.exit(f"missing asset: {path}")
    mime = MIME[path.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


html = SRC.read_text(encoding="utf-8")
used = []


def sub(match):
    name = match.group(1)
    used.append(name)
    return data_uri(name)


html = re.sub(r"__ASSET:([^_]+?)__", sub, html)

if "__ASSET:" in html:
    sys.exit("unresolved asset placeholder remains")

OUT.write_text(html, encoding="utf-8")
print(f"inlined {len(used)} assets: {', '.join(used)}")
print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")
