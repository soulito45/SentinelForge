from risk.scoring import calculate_finding_score, get_risk_level


def test_critical_internet_facing_database():
    score = calculate_finding_score(
        severity="critical",
        internet_facing=True,
        database_exposed=True,
        version_detected=True,
    )

    assert score == 100
    assert get_risk_level(score) == "CRITICAL"


def test_high_web_finding():
    score = calculate_finding_score(
        severity="high",
        internet_facing=True,
        web_exposed=True,
    )

    assert score == 85
    assert get_risk_level(score) == "CRITICAL"


def test_medium_finding():
    score = calculate_finding_score(
        severity="medium",
    )

    assert score == 50
    assert get_risk_level(score) == "HIGH"


def test_info_finding():
    score = calculate_finding_score(
        severity="info",
    )

    assert score == 10
    assert get_risk_level(score) == "LOW"


if __name__ == "__main__":
    test_critical_internet_facing_database()
    test_high_web_finding()
    test_medium_finding()
    test_info_finding()

    print("Risk scoring tests passed.")