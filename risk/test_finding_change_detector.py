from backend.app.database import SessionLocal
from backend.app.models import Asset, Domain, Scan, Change
from risk.change_detector import detect_finding_changes


db = SessionLocal()

try:
    domain = (
        db.query(Domain)
        .filter(Domain.name == "sentinelforge.local")
        .first()
    )

    if domain is None:
        raise RuntimeError("Test domain not found")

    asset = (
        db.query(Asset)
        .filter(
            Asset.hostname == "test.sentinelforge.local"
        )
        .first()
    )

    if asset is None:
        raise RuntimeError("Test asset not found")

    scan = Scan(
        domain_id=domain.id,
        status="running",
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    # Findings from the previous scan.
    previous_findings = {
        "swagger-api",
        "old-finding",
    }

    # Findings from the current scan.
    # swagger-api remains.
    # old-finding is resolved.
    # new-finding is newly detected.
    current_findings = {
        "swagger-api",
        "new-finding",
    }

    changes = detect_finding_changes(
        db=db,
        asset=asset,
        scan_id=scan.id,
        previous_findings=previous_findings,
        current_findings=current_findings,
    )

    db.commit()

    scan.status = "completed"
    db.commit()

    print()
    print("========== FINDING CHANGE DETECTION ==========")
    print(f"Changes detected: {changes}")

    print()
    print("Recorded changes:")

    recorded_changes = (
        db.query(Change)
        .filter(Change.scan_id == scan.id)
        .order_by(Change.id)
        .all()
    )

    for change in recorded_changes:
        print(
            f"{change.change_type}: "
            f"{change.description}"
        )

finally:
    db.close()
