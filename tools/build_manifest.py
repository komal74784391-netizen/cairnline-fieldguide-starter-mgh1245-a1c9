#!/usr/bin/env python3
"""Build the content manifest consumed by the field guide site.

Usage:
    python tools/build_manifest.py [content_dir]

Defaults to <repo>/site/content.  The manifest is written next to the
content files as manifest.json.  Do not hand-edit the manifest: the site
build compares it against the content and refuses to deploy when they drift.
"""
import json
import re
import sys
from pathlib import Path

DEFAULT_DIR = Path(__file__).resolve().parents[1] / "site" / "content"

EXCERPT_LIMIT = 140


def parse_front_matter(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("entry is missing front matter")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("entry front matter is not closed")
    meta = {}
    current = None
    for line in lines[1:end]:
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- ") and current is not None:
            meta.setdefault(current, [])
            meta[current].append(stripped[2:].strip())
        elif ":" in stripped:
            key, value = stripped.split(":", 1)
            key, value = key.strip(), value.strip()
            current = key
            meta[key] = [] if value == "" else value
    body = "\n".join(lines[end + 1:]).strip()
    return meta, body


def excerpt(body):
    text = re.sub(r"\s+", " ", body).strip()
    if len(text) > EXCERPT_LIMIT:
        return text[:EXCERPT_LIMIT].rstrip() + "..."
    return text


def build(content_dir):
    content_dir = Path(content_dir)
    entries = []
    for path in sorted(content_dir.glob("*.md")):
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if str(meta.get("draft", "false")).lower() == "true":
            continue
        slug = path.stem[11:] if re.match(r"\d{4}-\d{2}-\d{2}-", path.stem) else path.stem
        entries.append({
            "id": "fg-" + slug,
            "title": meta.get("title", ""),
            "date": meta.get("date", ""),
            "tags": list(meta.get("tags", [])),
            "author": meta.get("author", ""),
            "status": "live",
            "excerpt": excerpt(body),
            "path": "content/" + path.name,
        })
    entries.sort(key=lambda e: (-int(str(e["date"]).replace("-", "")), e["id"]))
    manifest = {
        "schema": "fieldguide-manifest/1",
        "generated_from": "site/content",
        "count": len(entries),
        "entries": entries,
    }
    out = content_dir / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s with %d entries" % (out, len(entries)))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR)
