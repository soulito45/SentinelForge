from backend.app.database import SessionLocal
from backend.app.models import Asset, Scan
from risk.change_detector import detect_changes


db = SessionLocal()

try:
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
        domain_id=asset.domain_id,
        status="running",
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    previous_ports = {
        (22, "tcp"),
        (443, "tcp"),
        (5432, "tcp"),
    }

    current_ports = {
        (22, "tcp"),
        (443, "tcp"),
        (5432, "tcp"),
        (8443, "tcp"),
    }

    previous_technologies = {
        "Python",
        "Uvicorn",
    }

    current_technologies = {
        "Python",
        "Uvicorn",
        "FastAPI",
    }

    previous_findings = {
        "old-template",
    }

    current_findings = {
        "swagger-api",
    }

    changes = detect_changes(
        db=db,
        asset=asset,
        scan_id=scan.id,
        previous_ports=previous_ports,
        current_ports=current_ports,
        previous_technologies=previous_technologies,
        current_technologies=current_technologies,
        previous_findings=previous_findings,
        current_findings=current_findings,
    )

    scan.status = "completed"
    db.commit()

    print()
    print("========== CHANGE DETECTION ==========")
    print(f"Changes detected: {changes}")

finally:
    db.close()
