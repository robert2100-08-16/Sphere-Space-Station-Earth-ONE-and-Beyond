from tools.qa.safety import simulate_safety_scenarios


def test_detect_missing_evacuation_route():
    doc = "Fire suppression uses a redundant system for containment."
    result = simulate_safety_scenarios(doc)
    assert "fire" in result
    assert "missing evacuation route" in result["fire"]


def test_detect_missing_redundant_system():
    doc = "Fire emergency plan includes an evacuation route for all decks."
    result = simulate_safety_scenarios(doc)
    assert "fire" in result
    assert "missing redundant system" in result["fire"]
