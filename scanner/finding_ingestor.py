from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset, Finding


def store_findings(
    db: Session,
    asset: Asset,
    scan_id: int,
    findings: list[dict],
) -> int:
    """
    Store or update Nuclei findings for an asset.

    Findings detected in the current scan are marked open.
    Findings previously open but not detected in the current scan
    are marked resolved.
    """

    now = datetime.utcnow()

    existing = {
        finding.template_id: finding
        for finding in asset.findings
    }

    current_template_ids = set()
    stored_count = 0

    for item in findings:
        template_id = item.get("template_id")
        title = item.get("name")
        severity = item.get("severity")

        if not template_id or not title:
            continue

        current_template_ids.add(template_id)

        if template_id in existing:
            finding = existing[template_id]

            finding.last_seen = now
            finding.status = "open"
            finding.scan_id = scan_id

            if severity:
                finding.severity = severity

            if item.get("evidence"):
                finding.evidence = item["evidence"]

        else:
            finding = Finding(
                asset_id=asset.id,
                scan_id=scan_id,
                template_id=template_id,
                title=title,
                severity=severity or "unknown",
                evidence=item.get("evidence"),
                status="open",
                first_seen=now,
                last_seen=now,
            )

            db.add(finding)
            stored_count += 1

    # Resolve findings that existed previously but were not
    # detected during the current scan.
    for template_id, finding in existing.items():
        if (
            finding.status == "open"
            and template_id not in current_template_ids
        ):
            finding.status = "resolved"

    db.commit()

    return stored_count