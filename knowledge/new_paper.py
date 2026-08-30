"""Scaffold a paper note from _templates/paper.md.

    sconix paper https://arxiv.org/abs/2305.18290
    sconix paper "Some paper title I'm reading"

With an arXiv URL/ID it fetches title, authors, and year (stdlib only, no key).
"""

from __future__ import annotations

import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
TPL = (ROOT / "_templates" / "paper.md").read_text()


def slugify(s: str, maxwords: int = 6) -> str:
    words = re.sub(r"[^a-z0-9\s-]", "", s.lower()).split()
    return "-".join(words[:maxwords]) or "paper"


def arxiv_id(arg: str) -> str | None:
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})", arg) or re.match(
        r"^([0-9]{4}\.[0-9]{4,5})$", arg.strip()
    )
    return m.group(1) if m else None


def fetch_arxiv(aid: str) -> dict:
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    with urllib.request.urlopen(url, timeout=15) as r:
        xml = r.read()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = ET.fromstring(xml).find("a:entry", ns)
    if e is None:
        raise RuntimeError("arXiv returned no entry")
    title = " ".join(e.findtext("a:title", "", ns).split())
    authors = [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)]
    year = e.findtext("a:published", "", ns)[:4]
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "url": f"https://arxiv.org/abs/{aid}",
    }


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('usage: sconix paper <arxiv-url|"title">')
    arg = " ".join(sys.argv[1:])
    aid = arxiv_id(arg)

    meta = {"title": arg, "authors": [], "year": date.today().year, "url": ""}
    if aid:
        try:
            meta.update(fetch_arxiv(aid))
            print(f"fetched: {meta['title']}")
        except Exception as exc:  # noqa: BLE001
            print(f"arXiv fetch failed ({exc}); scaffolding a blank note")
            meta["url"] = f"https://arxiv.org/abs/{aid}"

    stem = f"{meta['year']}-{slugify(meta['title'])}"
    dest = ROOT / "papers" / f"{stem}.md"
    if dest.exists():
        sys.exit(f"already exists: {dest}")

    body = (
        TPL.replace("TITLE", meta["title"])
        .replace("YEAR", str(meta["year"]))
        .replace("URL", meta["url"] or '""')
        .replace("ADDED", date.today().isoformat())
    )
    if meta["authors"]:
        body = body.replace("authors: []", "authors: [" + ", ".join(meta["authors"]) + "]", 1)
    dest.write_text(body)
    print(f"created papers/{stem}.md")
    print("  fill the frontmatter facets from knowledge/TAXONOMY.md, then: sconix kindex")


if __name__ == "__main__":
    main()
