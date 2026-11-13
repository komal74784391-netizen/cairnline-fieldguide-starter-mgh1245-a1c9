# Cairnline Fieldguide Starter Kit

An open-source starter kit for content-driven field guides. Clone it, drop
Markdown entries into `site/content`, run the manifest builder, and deploy.

## What is in the box

- `site/content/` — your entries as Markdown files with YAML front matter.
- `tools/build_manifest.py` — the build step that regenerates
  `site/content/manifest.json` from the current content.
- `README.md` — this file.

## Authoring conventions

Every entry is a Markdown file named `YYYY-MM-DD-slug.md`. The front matter
carries `title`, `date`, `tags` (a YAML list), `author`, and `draft`. The site
build only renders entries with `draft: false`.

After any content change run:

```
python tools/build_manifest.py
```

The build compares `site/content/manifest.json` byte-for-byte against the
manifest it can regenerate. If they drift, deployment stops. Treat the manifest
as generated output: never edit it by hand.

## Demo content

The `site/content` folder ships with three demo entries and the matching
manifest so you can see the output shape before writing your own content.
Replace them with your own entries when you start a new site.
