from backend.app.database import SessionLocal
from backend.app.models import Asset, Domain, Scan, Change
from risk.change_detector import detect_technology_changes


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

    # Simulate the previous scan.
    previous_technologies = {
        "Python",
        "Uvicorn",
    }

    # Simulate the current scan.
    # FastAPI is newly detected.
    # Uvicorn is no longer detected.
    current_technologies = {
        "Python",
        "FastAPI",
    }

    changes = detect_technology_changes(
        db=db,
        asset=asset,
        scan_id=scan.id,
        previous_technologies=previous_technologies,
        current_technologies=current_technologies,
    )

    db.commit()

    scan.status = "completed"
    db.commit()

    print()
    print("========== TECHNOLOGY CHANGE DETECTION ==========")
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
