from backend.app.database import SessionLocal
from backend.app.models import Asset, Scan
from scanner.nuclei_pipeline import run_nuclei_pipeline


db = SessionLocal()

try:
    asset = (
        db.query(Asset)
        .filter(Asset.hostname == "test.sentinelforge.local")
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

    print(f"[+] Scan ID: {scan.id}")
    print(f"[+] Asset: {asset.hostname}")

    count = run_nuclei_pipeline(
        db=db,
        asset=asset,
        scan_id=scan.id,
    )

    scan.status = "completed"
    db.commit()

    print()
    print("========== NUCLEI PIPELINE RESULT ==========")
    print(f"Findings stored: {count}")

finally:
    db.close()
