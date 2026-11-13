---
title: Authoring Guide: Writing an Entry
date: 2025-10-21
tags:
  - guide
  - authoring
author: Cairnline Starter Team
draft: false
---
Start every entry with front matter containing title, date, tags, author and draft. Use an ISO date, list tags as a YAML sequence, and set draft to false only when the entry is ready to appear in the index. The file name follows the publish date and a short slug. After you change any entry, run the manifest builder; it rewrites the manifest from the current content folder, skipping drafts. Do not hand-edit the manifest, because the build validates it against the content and rejects files that drift.
