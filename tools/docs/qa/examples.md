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
source_of_truth: false
supersedes: null
superseded_by: null
rfc_links: []
adr_links: []
cr_links: []
date: 1970-01-01
lang: EN
---

# QA Report Examples

Demonstration of how `MISSING` entries appear when sections are absent.

```python
from tools.qa.checklist import CHECKLISTS, check_completeness

document = {
    "chapters": ["Introduction"],
    "tables": ["Requirements"],
}
template = CHECKLISTS["technical_report"]
missing = check_completeness(document, template)
print(missing)
```

Output:

```
{'chapters': ['System Overview', 'Testing', 'Conclusion'], 'tables': ['Results']}
```

QA report rendering:

```
Chapters
- Introduction
- MISSING: System Overview
- MISSING: Testing
- MISSING: Conclusion

Tables
- Requirements
- MISSING: Results
```
