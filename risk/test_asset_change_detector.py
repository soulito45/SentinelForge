from backend.app.database import SessionLocal
from backend.app.models import Asset, Domain, Scan
from risk.asset_change_detector import detect_asset_changes


db = SessionLocal()

try:
    domain = (
        db.query(Domain)
        .filter(Domain.name == "sentinelforge.local")
        .first()
    )

    if domain is None:
        raise RuntimeError("Test domain not found")

    test_asset = (
        db.query(Asset)
        .filter(
            Asset.hostname == "test.sentinelforge.local"
        )
        .first()
    )

    if test_asset is None:
        raise RuntimeError("Test asset not found")

    # Get or create the simulated old asset.
    old_asset = (
        db.query(Asset)
        .filter(
            Asset.hostname == "old.sentinelforge.local"
        )
        .first()
    )

    if old_asset is None:
        old_asset = Asset(
            domain_id=domain.id,
            hostname="old.sentinelforge.local",
            asset_type="subdomain",
            status="active",
        )
        db.add(old_asset)

    # Get or create the simulated new asset.
    new_asset = (
        db.query(Asset)
        .filter(
            Asset.hostname == "new.sentinelforge.local"
        )
        .first()
    )

    if new_asset is None:
        new_asset = Asset(
            domain_id=domain.id,
            hostname="new.sentinelforge.local",
            asset_type="subdomain",
            status="active",
        )
        db.add(new_asset)

    db.commit()

    # Make sure the removed asset starts as active.
    old_asset.status = "active"

    # Make sure the new asset starts as active.
    new_asset.status = "active"

    db.commit()

    scan = Scan(
        domain_id=domain.id,
        status="running",
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    previous_assets = {
        "test.sentinelforge.local",
        "old.sentinelforge.local",
    }

    current_assets = {
        "test.sentinelforge.local",
        "new.sentinelforge.local",
    }

    changes = detect_asset_changes(
        db=db,
        domain_id=domain.id,
        scan_id=scan.id,
        previous_assets=previous_assets,
        current_assets=current_assets,
    )

    scan.status = "completed"
    db.commit()

    print()
    print("========== ASSET CHANGE DETECTION ==========")
    print(f"Changes detected: {changes}")

    print()
    print("Recorded changes:")

    from backend.app.models import Change

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