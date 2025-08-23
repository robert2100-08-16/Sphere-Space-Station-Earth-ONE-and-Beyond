---
id: ""
title: ""
version: v0.0.0
state: DRAFT
evolution: ""
discipline: ""
system: []
system_id: []
seq: []
owner: ""
reviewers: []
source_of_truth: true
supersedes: null
superseded_by: null
rfc_links: []
adr_links: []
cr_links: []
date: 1970-01-01
lang: EN
---

# Git Issues

## Long Filename Error

If you encounter the error "filename too long" while pulling the repository, follow these steps:

1. Open a terminal/shell as administrator (Windows) or use sudo (Linux/Mac)
2. Run the following command:
   ```bash
   git config --system core.longpaths true
   ```
3. Try your git operation again

This setting enables support for long file paths in Git, which is especially important for Windows systems. 
