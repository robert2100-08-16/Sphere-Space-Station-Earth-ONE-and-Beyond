# QA Pipeline

The QA pipeline runs a series of checks on a document and stores a report.

## Schritte
1. Import
2. Pre-Check
3. Semantic Analysis
4. Safety Simulation
5. Issue Tagging
6. Report-Erstellung
7. Review

## Verwendung
```python
from tools.qa.pipeline import run_pipeline

result = run_pipeline("document.json", presentation_format="pitch")
print(result["report_path"])
```

Reports are written to `reports/qa/` with chapter references and
issue categories.
