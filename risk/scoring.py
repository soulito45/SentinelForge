SEVERITY_SCORES = {
    "critical": 90,
    "high": 70,
    "medium": 50,
    "low": 25,
    "info": 10,
    "unknown": 5,
}


def calculate_finding_score(
    severity: str,
    internet_facing: bool = False,
    web_exposed: bool = False,
    ssh_exposed: bool = False,
    database_exposed: bool = False,
    version_detected: bool = False,
) -> int:
    """
    Calculate a contextual SentinelForge risk score.

    This is an internal prioritization score and is not CVSS.
    """

    score = SEVERITY_SCORES.get(
        severity.lower(),
        SEVERITY_SCORES["unknown"],
    )

    if internet_facing:
        score += 10

    if web_exposed:
        score += 5

    if ssh_exposed:
        score += 5

    if database_exposed:
        score += 10

    if version_detected:
        score += 5

    return min(score, 100)


def get_risk_level(score: int) -> str:
    """
    Convert a numeric risk score into a SentinelForge risk level.
    """

    if score >= 75:
        return "CRITICAL"

    if score >= 50:
        return "HIGH"

    if score >= 25:
        return "MEDIUM"

    return "LOW"