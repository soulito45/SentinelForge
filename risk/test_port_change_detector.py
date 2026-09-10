from backend.app.database import SessionLocal
from backend.app.models import Asset, Domain, Scan, Change
from risk.change_detector import detect_port_changes


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
    previous_ports = {
        (22, "tcp"),
        (443, "tcp"),
        (5432, "tcp"),
    }

    # Simulate the current scan.
    # Port 22 was closed.
    # Port 8000 was newly opened.
    current_ports = {
        (443, "tcp"),
        (5432, "tcp"),
        (8000, "tcp"),
    }

    changes = detect_port_changes(
        db=db,
        asset=asset,
        scan_id=scan.id,
        previous_ports=previous_ports,
        current_ports=current_ports,
    )

    db.commit()

    scan.status = "completed"
    db.commit()

    print()
    print("========== PORT CHANGE DETECTION ==========")
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
