from tools.qa.checklist import CHECKLISTS, check_completeness


def test_completeness_all_present():
    doc = {
        "chapters": ["Introduction", "System Overview", "Testing", "Conclusion"],
        "tables": ["Requirements", "Results"],
    }
    template = CHECKLISTS["technical_report"]
    assert check_completeness(doc, template) == {}


def test_completeness_missing_sections():
    doc = {"chapters": ["Introduction"], "tables": []}
    template = CHECKLISTS["technical_report"]
    assert check_completeness(doc, template) == {
        "chapters": ["System Overview", "Testing", "Conclusion"],
        "tables": ["Requirements", "Results"],
    }
