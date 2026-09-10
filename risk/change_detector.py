from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models import Asset, Change


def record_change(
    db: Session,
    asset: Asset,
    scan_id: int,
    change_type: str,
    description: str,
    previous_value: str | None = None,
    current_value: str | None = None,
) -> None:
    change = Change(
        asset_id=asset.id,
        scan_id=scan_id,
        change_type=change_type,
        description=description,
        previous_value=previous_value,
        current_value=current_value,
        detected_at=datetime.utcnow(),
    )

    db.add(change)


def detect_port_changes(
    db: Session,
    asset: Asset,
    scan_id: int,
    previous_ports: set[tuple[int, str]],
    current_ports: set[tuple[int, str]],
) -> int:
    changes = 0

    new_ports = current_ports - previous_ports
    closed_ports = previous_ports - current_ports

    for port_number, protocol in sorted(new_ports):
        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="NEW_PORT",
            description=f"New open port detected: {port_number}/{protocol}",
            current_value=f"{port_number}/{protocol}",
        )
        changes += 1

    for port_number, protocol in sorted(closed_ports):
        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="CLOSED_PORT",
            description=(
                f"Previously open port is no longer open: "
                f"{port_number}/{protocol}"
            ),
            previous_value=f"{port_number}/{protocol}",
        )
        changes += 1

    return changes


def detect_technology_changes(
    db: Session,
    asset: Asset,
    scan_id: int,
    previous_technologies: set[str],
    current_technologies: set[str],
) -> int:
    changes = 0

    new_technologies = current_technologies - previous_technologies
    removed_technologies = previous_technologies - current_technologies

    for technology in sorted(new_technologies):
        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="NEW_TECHNOLOGY",
            description=f"New technology detected: {technology}",
            current_value=technology,
        )
        changes += 1

    for technology in sorted(removed_technologies):
        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="REMOVED_TECHNOLOGY",
            description=(
                f"Previously detected technology is no longer observed: "
                f"{technology}"
            ),
            previous_value=technology,
        )
        changes += 1

    return changes


def detect_finding_changes(
    db: Session,
    asset: Asset,
    scan_id: int,
    previous_findings: set[str],
    current_findings: set[str],
) -> int:
    changes = 0

    new_findings = current_findings - previous_findings
    resolved_findings = previous_findings - current_findings

    for template_id in sorted(new_findings):
        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="NEW_FINDING",
            description=f"New vulnerability finding detected: {template_id}",
            current_value=template_id,
        )
        changes += 1

    for template_id in sorted(resolved_findings):
        record_change(
            db=db,
            asset=asset,
            scan_id=scan_id,
            change_type="RESOLVED_FINDING",
            description=(
                f"Previously detected finding is no longer present: "
                f"{template_id}"
            ),
            previous_value=template_id,
        )
        changes += 1

    return changes


def detect_changes(
    db: Session,
    asset: Asset,
    scan_id: int,
    previous_ports: set[tuple[int, str]],
    current_ports: set[tuple[int, str]],
    previous_technologies: set[str],
    current_technologies: set[str],
    previous_findings: set[str],
    current_findings: set[str],
) -> dict:
    """
    Detect all changes for an asset and return
    a breakdown by change category.
    """

    port_changes = detect_port_changes(
        db=db,
        asset=asset,
        scan_id=scan_id,
        previous_ports=previous_ports,
        current_ports=current_ports,
    )

    technology_changes = detect_technology_changes(
        db=db,
        asset=asset,
        scan_id=scan_id,
        previous_technologies=previous_technologies,
        current_technologies=current_technologies,
    )

    finding_changes = detect_finding_changes(
        db=db,
        asset=asset,
        scan_id=scan_id,
        previous_findings=previous_findings,
        current_findings=current_findings,
    )

    db.commit()

    return {
        "port_changes": port_changes,
        "technology_changes": technology_changes,
        "finding_changes": finding_changes,
        "total_changes": (
            port_changes
            + technology_changes
            + finding_changes
        ),
    }