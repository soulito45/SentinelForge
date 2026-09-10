from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset
from risk.scoring import calculate_finding_score, get_risk_level


def calculate_asset_risk(
    db: Session,
    asset: Asset,
) -> dict:
    """
    Calculate and persist the overall contextual risk of an asset.
    """

    internet_facing = True

    web_exposed = any(
        port.port_number in {80, 443, 8000, 8080, 8443}
        and port.state == "open"
        for port in asset.ports
    )

    ssh_exposed = any(
        port.port_number == 22
        and port.state == "open"
        for port in asset.ports
    )

    database_exposed = any(
        port.port_number in {
            1433,
            1521,
            3306,
            5432,
            6379,
            27017,
        }
        and port.state == "open"
        for port in asset.ports
    )

    version_detected = any(
        port.version
        for port in asset.ports
        if port.state == "open"
    )

    finding_scores = []

    for finding in asset.findings:
        if finding.status != "open":
            continue

        score = calculate_finding_score(
            severity=finding.severity,
            internet_facing=internet_facing,
            web_exposed=web_exposed,
            ssh_exposed=ssh_exposed,
            database_exposed=database_exposed,
            version_detected=version_detected,
        )

        finding_scores.append(score)

    if finding_scores:
        risk_score = max(finding_scores)
    else:
        risk_score = 0

    risk_level = get_risk_level(risk_score)

    # Persist the calculated risk.
    asset.risk_score = risk_score
    asset.risk_level = risk_level
    asset.risk_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(asset)

    return {
        "asset_id": asset.id,
        "hostname": asset.hostname,
        "risk_score": asset.risk_score,
        "risk_level": asset.risk_level,
        "open_findings": len(finding_scores),
        "web_exposed": web_exposed,
        "ssh_exposed": ssh_exposed,
        "database_exposed": database_exposed,
        "version_detected": version_detected,
        "risk_updated_at": asset.risk_updated_at,
    }